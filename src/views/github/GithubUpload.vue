<template>
  <div class="flex h-full w-full flex-col items-center justify-center p-3 pr-5">
    <div class="flex h-full w-full flex-col">
      <span class="text-left text-lg font-medium"> Uploading your metadata files to GitHub </span>
      <span class="text-left">
        This one is on us. We're working hard to get your files up to GitHub.
      </span>

      <el-divider class="my-4"> </el-divider>

      <div class="flex h-full flex-col justify-center">
        <el-progress
          :percentage="percentage"
          :indeterminate="indeterminate"
          :status="progressStatus"
          :stroke-width="10"
          class="my-2"
        />
        <el-alert
          v-if="showAlert"
          :title="alertTitle"
          type="error"
          :description="alertMessage"
          show-icon
        >
        </el-alert>
        <div class="flex flex-row items-center justify-start py-3" v-else>
          <LoadingCubeGrid class="h-5 w-5" v-if="percentage !== 100"></LoadingCubeGrid>
          <p class="pl-4">
            {{ statusMessage }}
            <LoadingEllipsis v-if="percentage !== 100"></LoadingEllipsis>
          </p>
        </div>
        <div class="pt-2 pl-2" v-if="errorMessage != ''">
          <p style="white-space: pre-line">
            {{ errorMessage }}
          </p>
        </div>
      </div>

      <div class="flex w-full flex-row justify-center py-2" v-if="showAlert">
        <router-link
          :to="`/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/github/summary`"
          class="mx-6"
        >
          <button class="primary-plain-button">Back</button>
        </router-link>

        <button class="primary-button" @click="retryUpload">Retry</button>
      </div>
    </div>
  </div>
</template>

<script>
import { app } from "@electron/remote";
import axios from "axios";
import path from "path";
import fs from "fs-extra";

import LoadingCubeGrid from "@/components/spinners/LoadingCubeGrid.vue";
import LoadingEllipsis from "@/components/spinners/LoadingEllipsis.vue";

import { useDatasetsStore } from "@/store/datasets";
import { useTokenStore } from "@/store/access.js";

export default {
  name: "GithubUpload",
  components: { LoadingCubeGrid, LoadingEllipsis },
  data() {
    return {
      datasetStore: useDatasetsStore(),
      tokens: useTokenStore(),
      dataset: {},
      tempFolderPath: "",
      workflowID: this.$route.params.workflowID,
      workflow: {},
      percentage: 0,
      indeterminate: true,
      progressStatus: "",
      githubToken: "",
      statusMessage: "some status message here",
      errorMessage: "",
      showAlert: false,
      alertTitle: "",
      alertMessage: "",
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

    async createCodeMetadataFile() {
      const response = await axios
        .post(`${this.$server_url}/metadata/create`, {
          data_types: JSON.stringify(this.workflow.type),
          data_object: JSON.stringify(this.dataset.data),
          virtual_file: false,
        })
        .then((response) => {
          this.$track("Metadata", "Create codemeta", "success");
          return response.data;
        })
        .catch((error) => {
          this.$track("Metadata", "Create codemeta", "failed");
          console.error(error);
          return "ERROR";
        });
      return response;
    },
    async createCitationFile() {
      const response = await axios
        .post(`${this.$server_url}/metadata/citation/create`, {
          data_types: JSON.stringify(this.workflow.type),
          data_object: JSON.stringify(this.dataset.data),
          virtual_file: false,
        })
        .then((response) => {
          this.$track("Metadata", "Create citation", "success");
          return response.data;
        })
        .catch((error) => {
          this.$track("Metadata", "Create citation", "failed");

          console.error(error);
          return "ERROR";
        });
      return response;
    },
    async createLicenseFile() {
      const folderPath = this.dataset.data.Code.folderPath;

      const response = await axios
        .post(`${this.$server_url}/utilities/createfile`, {
          folder_path: folderPath,
          file_name: "LICENSE",
          file_content: this.workflow.licenseText,
          content_type: "text",
        })
        .then((response) => {
          this.$track("Metadata", "Create license", "success");
          return response.data;
        })
        .catch((error) => {
          this.$track("Metadata", "Create license", "failed");
          console.error(error);
          return "ERROR";
        });
      return response;
    },

    async uploadToGithub(filePath, fileName, repoName) {
      this.statusMessage = `Uploading ${fileName} to GitHub`;
      await this.sleep(100);

      const response = await axios
        .post(`${this.$server_url}/github/upload`, {
          access_token: this.githubToken,
          file_path: filePath,
          file_name: fileName,
          repo_name: repoName,
        })
        .then((response) => {
          this.$track("GitHub", "Uploaded file to GitHub", "success");
          return response.data;
        })
        .catch((error) => {
          this.$track("GitHub", "Uploaded file to GitHub", "success");
          console.error(error);
          return "ERROR";
        });

      if (response === "ERROR") {
        if (fileName === "LICENSE") {
          this.alertMessage = `Error uploading ${fileName} to GitHub. There may be illegal characters in the contents of the file. Please verify that the file is valid and try again.`;
        } else {
          this.alertMessage = `Error uploading ${fileName} to GitHub. Please verify that the file is valid and try again.`;
        }
        await this.sleep(300);
        this.statusMessage = "";
      } else {
        this.statusMessage = `${fileName} uploaded to GitHub`;
        await this.sleep(300);
        this.alertMessage = "";
      }

      return response;
    },

    async uploadMetadataFiles() {
      const folderPath = this.dataset.data.Code.folderPath;
      const repoName = this.workflow.github.repo;

      this.$track("GitHub", "Repository name", repoName);

      this.statusMessage = "Getting ready to upload metadata files to GitHub...";
      await this.sleep(300);

      const contents = fs.readdirSync(folderPath);

      for (const [index, file] of contents.entries()) {
        const filePath = path.join(folderPath, file);

        const response = await this.uploadToGithub(filePath, file, repoName);

        if (response === "ERROR") {
          return response;
        }

        this.percentage = ((index + 1) / contents.length) * 75 + 25;
        this.percentage = Math.round(this.percentage);
      }

      return "SUCCESS";
    },

    async uploadWorkflow() {
      let response = "";

      if (this.workflow.generateCodeMeta) {
        if (this.codePresent) {
          response = await this.createCodeMetadataFile();

          if (response === "ERROR") {
            this.alertMessage = "There was an error with creating the code metadata file";
            return "FAIL";
          } else {
            this.statusMessage = "Created a temporary codemeta.json file";
          }
        }
      }

      this.percentage = 5;
      this.indeterminate = false;

      await this.sleep(300);

      if (this.workflow.generateCodeMeta) {
        if (this.codePresent) {
          response = await this.createCitationFile();

          if (response === "ERROR") {
            this.alertMessage = "There was an error with creating the CITATION.cff file";
            return "FAIL";
          } else {
            this.statusMessage = "Created a temporary CITATION.cff file";
          }
        }
      }

      this.percentage = 10;
      this.indeterminate = false;

      await this.sleep(300);

      if (this.workflow.generateLicense) {
        response = await this.createLicenseFile();

        if (response === "ERROR") {
          this.alertMessage = "There was an error with creating the LICENSE file";
          return "FAIL";
        } else {
          this.statusMessage = "Created a temporary LICENSE file";
        }
      }

      this.percentage = 15;
      this.indeterminate = false;

      await this.sleep(300);

      response = await this.uploadMetadataFiles();

      if (response === "ERROR") {
        // this.alertMessage =
        //   "There was an error with uploading files to the GitHub repository";
        return "FAIL";
      } else {
        this.statusMessage = "Uploaded all files to GitHub successfully.";
      }

      if (this.workflow.uploadToRepo) {
        this.workflow.destination.zenodo.status.filesUploaded = true;
      }

      return "SUCCESS";
    },

    async runGithubUpload() {
      await this.datasetStore.hideSidebar();

      this.statusMessage = "Preparing backend services...";
      await this.sleep(300);

      let response = await this.uploadWorkflow();

      await this.datasetStore.showSidebar();

      this.dataset.data.Code.folderPath = "";

      if (response === "FAIL" || response === "ERROR") {
        this.indeterminate = true;
        this.progressStatus = "exception";
        this.showAlert = true;

        this.workflow.datasetUploaded = false;
        this.workflow.datasetPublished = false;

        await this.datasetStore.updateCurrentDataset(this.dataset);
        await this.datasetStore.syncDatasets();

        return;
      } else {
        this.workflow.datasetUploaded = true;
        this.workflow.datasetPublished = false;
        this.workflow.generateLicense = false;

        await this.datasetStore.updateCurrentDataset(this.dataset);
        await this.datasetStore.syncDatasets();

        let routerPath = "";

        if (this.workflow.uploadToRepo) {
          routerPath = `/datasets/${this.datasetID}/${this.workflowID}/github/publish`;
        } else {
          routerPath = `/datasets/${this.datasetID}/${this.workflowID}/githubNoUpload/finalPage`;
        }

        this.$router.push({ path: routerPath });
      }
    },
    async retryUpload() {
      this.indeterminate = false;
      this.progressStatus = "";
      this.showAlert = false;

      const tempFolderPath = path.join(app.getPath("home"), ".fairshare", "temp");

      // delete the temp folder if it exists
      // starting from a clean slate
      if (fs.existsSync(tempFolderPath)) {
        fs.rmdirSync(tempFolderPath, { recursive: true, force: true });
      }

      // recreate the temp folder
      if (!fs.existsSync(tempFolderPath)) {
        fs.mkdirSync(tempFolderPath);
      }

      this.dataset.data.Code.folderPath = tempFolderPath;

      this.runGithubUpload();
    },
  },
  async mounted() {
    this.dataset = await this.datasetStore.getCurrentDataset();
    this.workflow = this.dataset.workflows[this.workflowID];

    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(6);

    // not saving this page since it will start a random upload when saving progress
    // this.workflow.currentRoute = this.$route.path;

    const tokenObject = await this.tokens.getToken("github");
    this.githubToken = tokenObject.token;

    const tempFolderPath = path.join(app.getPath("home"), ".fairshare", "temp");

    // delete the temp folder if it exists
    // starting from a clean slate
    if (fs.existsSync(tempFolderPath)) {
      fs.rmdirSync(tempFolderPath, { recursive: true, force: true });
    }

    // recreate the temp folder
    if (!fs.existsSync(tempFolderPath)) {
      fs.mkdirSync(tempFolderPath);
    }

    this.dataset.data.Code.folderPath = tempFolderPath;

    this.runGithubUpload();
  },
};
</script>
