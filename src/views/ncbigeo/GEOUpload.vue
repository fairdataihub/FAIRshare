<template>
  <div class="flex h-full w-full flex-col items-center justify-center p-3 pr-5">
    <div class="flex h-full w-full flex-col">
      <span class="text-left text-lg font-medium"> Generating your final dataset </span>
      <span class="text-left">
        This one is on us. FAIRshare is generating all the relevant metadata files and o
      </span>

      <el-divider class="my-4"> </el-divider>

      <div class="flex h-full flex-col justify-center">
        <el-progress
          :percentage="percentage"
          :indeterminate="indeterminate"
          :status="progressStatus"
          :stroke-width="10"
        />
        <el-alert
          class="my-2"
          v-if="showAlert"
          :title="alertTitle"
          type="error"
          :description="alertMessage"
          show-icon
        >
        </el-alert>
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
        <div class="pt-2 pl-2" v-if="errorMessage != ''">
          <p style="white-space: pre-line">
            {{ errorMessage }}
          </p>
        </div>
      </div>

      <div class="flex w-full flex-row justify-center py-2" v-if="showAlert">
        <router-link
          :to="`/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/figshare/metadata`"
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
import axios from "axios";
// import path from "path";
// import fs from "fs-extra";
import klawSync from "klaw-sync";

import LoadingCubeGrid from "@/components/spinners/LoadingCubeGrid.vue";
import LoadingEllipsis from "@/components/spinners/LoadingEllipsis.vue";

import { useDatasetsStore } from "@/store/datasets";
import { useTokenStore } from "@/store/access.js";

// import ignoreFilesJSON from "@/assets/supplementalFiles/ignoreFilesList.json";
import figshareMetadataOptions from "@/assets/supplementalFiles/figshareMetadataOptions.json";

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
      overwriteCodeMeta: false,
      overwriteOtherMeta: false,
      licenseOptions: figshareMetadataOptions.licenseOptions,
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
    async uploadWorkflow() {
      let response = {};

      if (this.workflow.destination.figshare.newVersion) {
        this.statusMessage = "Creating a new version of the Figshare article";

        await this.sleep(300);

        const original_deposition_id = this.workflow.destination.zenodo.selectedDeposition.id;

        let res = null;

        res = await axios
          .post(`${this.$server_url}/zenodo/deposition/newversion`, {
            access_token: this.figshareToken,
            deposition_id: original_deposition_id,
          })
          .then((response) => {
            this.$track("Zenodo", "Create new version", "success");
            return response.data;
          })
          .catch((error) => {
            this.$track("Zenodo", "Create new version", "failed");
            console.error(error);
            return "ERROR";
          });

        const deposition_id = res;

        if (res === "ERROR") {
          this.alertMessage = "There was an error with creating a new version";
          return "FAIL";
        }

        this.statusMessage = "Requesting new Zenodo deposition version data";

        await this.sleep(300);

        res = await axios
          .get(`${this.$server_url}/zenodo/deposition`, {
            params: {
              access_token: this.figshareToken,
              deposition_id,
            },
          })
          .then((response) => {
            return response.data;
          })
          .catch((error) => {
            console.error(error);
            return "ERROR";
          });

        if (res === "ERROR") {
          this.alertMessage = "There was an error with requesting data from Zenodo";
          return "FAIL";
        } else {
          //create a copy of the res object
          response = JSON.parse(JSON.stringify(res));

          this.statusMessage =
            "Succeeded in requesting data from the new version of the zenodo deposition";
        }

        const files_list = res.files;

        for (let file of files_list) {
          this.statusMessage = `Removing pre-existing file '${file.filename}' from new Zenodo deposition version`;

          await this.sleep(100);

          await axios
            .delete(`${this.$server_url}/zenodo/deposition/files`, {
              data: {
                access_token: this.figshareToken,
                deposition_id,
                file_id: file.id,
              },
            })
            .then((response) => {
              return response.data;
            })
            .catch((error) => {
              console.error(error);
              return "ERROR";
            });
        }

        this.statusMessage = "Succeeded in removing all old pre-existing files";
      } else {
        response = await this.createFigshareDeposition();

        response = JSON.parse(response);

        if ("status" in response && response.status === "ERROR") {
          this.alertMessage = "There was an error with creating the deposition on Figshare";
          this.errorMessage = response.message;
          return "FAIL";
        } else {
          this.statusMessage = "Article shell created on Figshare";
        }

        this.percentage = 20;
        this.indeterminate = false;
      }

      await this.sleep(300);

      this.workflow.destination.figshare.status.depositionCreated = true;

      const responseObject = response;

      this.workflow.destination.figshare.article_id = responseObject.article_id;
      this.workflow.destination.figshare.doi = responseObject.doi;

      await this.datasetStore.updateCurrentDataset(this.dataset);
      await this.datasetStore.syncDatasets();

      await this.sleep(300);

      if (this.workflow.generateCodeMeta) {
        if (this.codePresent) {
          if (
            "metadata" in response &&
            "identifier" in this.dataset.data.Code.questions &&
            this.dataset.data.Code.questions.identifier == ""
          ) {
            this.dataset.data.Code.questions.identifier = responseObject.doi;
            this.overwriteCodeMeta = true;
          }

          response = await this.createCodeMetadataFile();
          // console.log(response);

          if (response === "ERROR") {
            this.alertMessage = "There was an error with creating the code metadata file";
            return "FAIL";
          } else {
            this.statusMessage = "Created the codemeta.json file in the target folder";

            await this.datasetStore.updateCurrentDataset(this.dataset);
            await this.datasetStore.syncDatasets();
          }
        }
      }

      this.percentage = 15;
      this.indeterminate = false;

      if (this.workflow.generateOtherMetadata) {
        console.log(this.dataset.data.Other.questions.identifier);
        if (
          "metadata" in response &&
          "identifier" in this.dataset.data.Other.questions &&
          this.dataset.data.Other.questions.identifier == ""
        ) {
          this.dataset.data.Other.questions.identifier = responseObject.doi;
          this.overwriteOtherMeta = true;
        }

        response = await this.createOtherMetadataFile();
        // console.log(response);

        if (response === "ERROR") {
          this.alertMessage = "There was an error with creating the required metadata.json file";
          return "FAIL";
        } else {
          this.statusMessage = "Created the metadata.json file in the target folder";

          await this.datasetStore.updateCurrentDataset(this.dataset);
          await this.datasetStore.syncDatasets();
        }
      }

      this.percentage = 18;
      this.indeterminate = false;

      await this.sleep(300);

      if (this.workflow.generateCodeMeta) {
        if (this.codePresent) {
          response = await this.createCitationFile();

          if (response === "ERROR") {
            this.alertMessage = "There was an error with creating the CITATION.cff file";
            return "FAIL";
          } else {
            this.statusMessage = "Created the CITATION.cff file in the target folder";
          }
        }
      }

      this.percentage = 20;
      this.indeterminate = false;

      await this.sleep(300);

      if (this.workflow.generateLicense) {
        response = await this.createLicenseFile();

        if (response === "ERROR") {
          this.alertMessage = "There was an error with creating the LICENSE file";
          return "FAIL";
        } else {
          this.statusMessage = "Created the LICENSE file in the target folder";
        }
      }

      this.percentage = 20;
      this.indeterminate = false;

      await this.sleep(300);

      response = await this.checkForFoldersAndUpload();

      if (response === "ERROR") {
        this.$track("Figshare", "Dataset uploaded", "failed");
        this.alertMessage = "There was an error with uploading files to Figshare";
        return "FAIL";
      } else {
        const files = klawSync(this.dataset.data[this.workflow.type[0]].folderPath, {
          nodir: true,
        });

        let totalSize = 0;

        for (let file of files) {
          totalSize += file.stats.size;
        }

        this.$track("Figshare", "Files uploaded size", totalSize);

        this.$track("Figshare", "Files uploaded", files.length);

        this.$track("Figshare", "Dataset uploaded", "success");

        this.statusMessage = "Uploaded all files to Figshare successfully.";
      }

      this.workflow.destination.figshare.status.filesUploaded = true;

      return "SUCCESS";
    },
    async createGeoMetadataFile() {
      const response = await axios
        .post(`${this.$server_url}/metadata/create`, {
          data_types: JSON.stringify(this.workflow.type),
          data_object: JSON.stringify(this.dataset.data),
          virtual_file: false,
        })
        .then((response) => {
          this.$track("Metadata", "Create geoMetadata", "success");
          return response.data;
        })
        .catch((error) => {
          this.$track("Metadata", "Create geoMetadata", "failed");
          console.error(error);
          return "ERROR";
        });
      return response;
    },
    async generateWorkflow() {
      let response = {};

      this.statusMessage = "Getting ready to generate the required metadata files";

      await this.sleep(300);

      response = await this.createGeoMetadataFile();

      if (response === "ERROR") {
        this.alertMessage = "There was an error with creating the metadata.xlsx file";
        return "FAIL";
      } else {
        this.statusMessage = "Created the metadata.xlsx file";
      }

      await this.sleep(300);

      console.log(response);

      return "SUCCESS";
    },
    async runGeoGenerate() {
      this.datasetStore.hideSidebar();

      this.indeterminate = true;
      this.percentage = 0;
      this.progressStatus = "";
      this.showAlert = false;

      this.statusMessage = "Preparing backend services...";
      await this.sleep(300);

      let response = await this.generateWorkflow();

      console.log(response);

      return;

      // let response = await this.uploadWorkflow();

      // this.datasetStore.showSidebar();

      // if (response === "FAIL") {
      //   this.indeterminate = true;
      //   this.progressStatus = "exception";
      //   this.showAlert = true;

      //   this.deleteDraftFigshareArticle();

      //   if (this.overwriteCodeMeta) {
      //     this.dataset.data.Code.questions.identifier = "";
      //   }
      //   if (this.overwriteOtherMeta) {
      //     this.dataset.data.Other.questions.identifier = "";
      //   }

      //   this.workflow.datasetUploaded = false;
      //   this.workflow.datasetPublished = false;

      //   await this.datasetStore.updateCurrentDataset(this.dataset);
      //   await this.datasetStore.syncDatasets();

      //   return;
      // } else {
      //   if (this.overwriteCodeMeta) {
      //     this.dataset.data.Code.questions.identifier = "";
      //   }
      //   if (this.overwriteOtherMeta) {
      //     this.dataset.data.Other.questions.identifier = "";
      //   }

      //   this.workflow.datasetUploaded = true;
      //   this.workflow.datasetPublished = false;
      //   this.workflow.generateLicense = false;

      //   await this.datasetStore.updateCurrentDataset(this.dataset);
      //   await this.datasetStore.syncDatasets();

      // const routerPath = `/datasets/${this.datasetID}/${this.workflowID}/figshare/publish`;
      // this.$router.push({ path: routerPath });
      // }
    },
    async retryUpload() {
      this.runGeoGenerate();
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

    this.runGeoGenerate();
  },
};
</script>
