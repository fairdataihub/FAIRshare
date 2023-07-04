<template>
  <div class="flex h-full w-full flex-col items-center justify-center p-3 pr-5">
    <div class="flex h-full w-full flex-col">
      <span class="text-left text-lg font-medium"> Let's upload your dataset </span>

      <span class="text-left">
        Looks like your dataset was generated for a Next Gen High Throughput Sequencing (NGS)
        experiment. Let's upload it to GEO.
      </span>

      <line-divider />

      <div class="flex w-full flex-col">
        <p class="mb-2">Please provide the link to your personalized GEO folder:</p>

        <el-input
          size="large"
          v-model="geoFolderPath"
          placeholder="uploads/username@orcid_UHs3vJap"
          class="w-full"
        />

        <p class="mb-2 mt-2 text-xs text-slate-600">
          Refer to the documentation provided by GEO for instructions on how to get your
          personalized upload folder.
          <a href="https://www.ncbi.nlm.nih.gov/geo/info/seq.html" class="text-url">
            Click here to read the official documentation.
          </a>
        </p>

        <div class="mt-4 flex flex-row items-center justify-center space-x-4">
          <router-link
            :to="`/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/ncbigeo/generate`"
          >
            <button class="primary-plain-button" :disabled="showUploadProgress">Back</button>
          </router-link>

          <button
            class="primary-button"
            @click="startUpload"
            :disabled="showUploadProgress || geoFolderPath.trim() == ''"
          >
            Connect and upload
          </button>
        </div>
      </div>

      <div class="flex h-full flex-col justify-center" v-if="showUploadProgress">
        <el-progress
          :percentage="percentage"
          :indeterminate="indeterminate"
          :status="progressStatus"
          :stroke-width="10"
        />
        <div class="my-2" v-if="showAlert">
          <el-alert :title="alertTitle" type="error" :description="alertMessage" show-icon />
        </div>

        <div class="flex flex-row items-start justify-start py-3" v-else>
          <LoadingCubeGrid class="h-5 w-5" v-if="percentage !== 100"></LoadingCubeGrid>
          <div class="flex flex-col items-start">
            <p class="pl-4">
              {{ statusMessage }}
              <LoadingEllipsis v-if="percentage !== 100"></LoadingEllipsis>
            </p>
            <p class="whitespace-pre pl-4 text-sm">
              {{ subStatusMessage }}
              <LoadingEllipsis v-if="subStatusMessage !== ' '"></LoadingEllipsis>
            </p>
          </div>
        </div>
        <div class="pl-2 pt-2" v-if="errorMessage != ''">
          <p style="white-space: pre-line">
            {{ errorMessage }}
          </p>
        </div>
      </div>

      <div class="flex w-full flex-row justify-center space-x-4 py-2" v-if="showAlert">
        <router-link
          :to="`/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/figshare/metadata`"
        >
          <button class="primary-plain-button">Back</button>
        </router-link>

        <button class="primary-button" @click="retryUpload">Retry</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
// import path from "path";
// import fs from "fs-extra";
import klawSync from "klaw-sync";

import LoadingCubeGrid from "@/components/spinners/LoadingCubeGrid.vue";
import LoadingEllipsis from "@/components/spinners/LoadingEllipsis.vue";

import { useDatasetsStore } from "@/store/datasets";
import { useTokenStore } from "@/store/access.js";

export default {
  name: "FigshareUpload",
  components: { LoadingCubeGrid, LoadingEllipsis },
  data() {
    return {
      datasetStore: useDatasetsStore(),
      tokens: useTokenStore(),
      dataset: {},
      folderPath: "",
      workflowID: this.$route.params.workflowID,
      workflow: {},
      percentage: 0,
      indeterminate: true,
      progressStatus: "",
      figshareToken: "",
      statusMessage: "some status message here",
      subStatusMessage: " ",
      errorMessage: "",
      showAlert: false,
      alertTitle: "",
      alertMessage: "",
      geoFolderPath: "",
      showUploadProgress: false,
    };
  },
  computed: {
    codePresent() {
      if ("type" in this.workflow) {
        return this.workflow.type.includes("Code");
      }
      return false;
    },
  },
  methods: {
    async sleep(ms) {
      return new Promise((resolve) => setTimeout(resolve, ms));
    },

    async retryUpload() {
      this.startUpload();
    },
    async checkUploadStatus() {
      const response = await axios
        .get(`${this.$server_url}/ncbigeo/upload`, {})
        .then((response) => {
          return response.data;
        })
        .catch((error) => {
          console.error(error);
          return JSON.stringify({ status: "ERROR", message: "error" });
        });

      if (response !== "" || response !== "ERROR" || "message" in response) {
        const res = JSON.parse(response);

        if (typeof res.currentFileNumber === "number" && typeof res.totalFiles === "number") {
          this.percentage = Math.floor((res.currentFileNumber / res.totalFiles) * 100);
        } else {
          this.percentage = 0;
        }

        this.subStatusMessage = res.status;
      }

      return;
    },
    async uploadFiles() {
      this.datasetStore.hideSidebar();
      let that = this;

      this.indeterminate = false;

      let interval = setInterval(() => {
        that.checkUploadStatus();
      }, 200);

      if ("destinationFolderPath" in this.workflow) {
        const destinationFolderPath = this.workflow.destinationFolderPath;

        const response = await axios
          .post(`${this.$server_url}/ncbigeo/upload`, {
            ftp_host: process.env.VUE_APP_GEO_FTP_SERVER_URL,
            ftp_username: process.env.VUE_APP_GEO_FTP_SERVER_USER,
            ftp_password: process.env.VUE_APP_GEO_FTP_SERVER_PASSWORD,
            ftp_folder_path: this.geoFolderPath.trim(),
            folder_path: destinationFolderPath,
          })
          .then((response) => {
            return response.data;
          })
          .catch((error) => {
            this.alertMessage =
              "Something went wrong with uploading your dataset to GEO. Please verify your folder and try again.";
            this.showAlert = true;

            console.error(error);

            return "ERROR";
          });

        this.datasetStore.showSidebar();

        clearInterval(interval);

        if (response === "ERROR") {
          this.subStatusMessage = " ";

          this.workflow.datasetUploaded = false;
          this.workflow.datasetPublished = false;

          await this.datasetStore.updateCurrentDataset(this.dataset);
          await this.datasetStore.syncDatasets();

          this.$track("GEO", "Upload dataset", "failed");

          this.alertMessage = "There was an error with uploading files to GEO";
          return "FAIL";
        } else {
          this.subStatusMessage = " ";

          const files = klawSync(destinationFolderPath, {
            nodir: true,
          });

          let totalSize = 0;

          for (let file of files) {
            totalSize += file.stats.size;
          }

          this.$track("GEO", "Files uploaded size", totalSize);

          this.$track("GEO", "Files uploaded", files.length);

          this.$track("GEO", "Dataset uploaded", "success");

          this.statusMessage = "Uploaded all files to GEO successfully.";

          this.percentage = 100;
          this.indeterminate = false;

          this.datasetStore.showSidebar();

          this.workflow.datasetUploaded = true;
          this.workflow.datasetPublished = false;

          await this.datasetStore.updateCurrentDataset(this.dataset);
          await this.datasetStore.syncDatasets();

          const routerPath = `/datasets/${this.datasetID}/${this.workflowID}/ncbigeo/publish`;
          this.$router.push({ path: routerPath });

          return "SUCCESS";
        }
      } else {
        this.$message({
          message: "Could not find the destination folder path",
          type: "error",
        });
      }
    },
    async startUpload() {
      const response = await axios
        .get(`${this.$server_url}/ncbigeo/files`, {
          params: {
            ftp_host: process.env.VUE_APP_GEO_FTP_SERVER_URL,
            ftp_username: process.env.VUE_APP_GEO_FTP_SERVER_USER,
            ftp_password: process.env.VUE_APP_GEO_FTP_SERVER_PASSWORD,
            ftp_folder_path: this.geoFolderPath.trim(),
          },
        })
        .then((response) => {
          this.$track("Connections", "GEO", "success");
          this.showUploadProgress = true;

          return response.data;
        })
        .catch((_error) => {
          this.$track("Connections", "GEO", "failed");
          this.$message({
            message: "There was an error with connecting to the FTP server",
            type: "error",
          });
          return "ERROR";
        });

      if (response === "ERROR") {
        return;
      }

      this.workflow.geoFolderPath = this.geoFolderPath.trim();

      await this.datasetStore.updateCurrentDataset(this.dataset);
      await this.datasetStore.syncDatasets();

      this.indeterminate = true;
      this.percentage = 0;
      this.progressStatus = "";
      this.showAlert = false;

      this.statusMessage = "Connected to the FTP server";
      await this.sleep(300);

      this.statusMessage = "Uploading files to the FTP server";
      await this.sleep(300);

      await this.uploadFiles();
    },
  },
  async mounted() {
    this.dataset = await this.datasetStore.getCurrentDataset();
    this.workflow = this.dataset.workflows[this.workflowID];

    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("geo");
    this.datasetStore.setCurrentStep(6);

    // Saving on this page since we can return back to this page after uploading to GEO
    this.workflow.currentRoute = this.$route.path;

    if ("geoFolderPath" in this.workflow) {
      this.geoFolderPath = this.workflow.geoFolderPath;
    }
  },
};
</script>
