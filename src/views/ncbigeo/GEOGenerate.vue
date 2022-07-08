<template>
  <div class="flex h-full w-full max-w-screen-xl flex-col items-center justify-center p-3 pr-5">
    <div class="flex h-full w-full flex-col">
      <span class="text-left text-lg font-medium"> Generate dataset </span>
      <span class="text-left">
        FAIRshare will generate a local version of your dataset in this step.
      </span>

      <el-divider class="my-4"> </el-divider>

      <div>
        <p class="mb-5">
          A list of all the files and folders that could be uploaded to NCBI GEO is shown below.
        </p>
        <div class="overflow-auto" :class="{ 'h-[150px]': finishedLoading }">
          <fade-transition>
            <el-tree-v2 v-if="finishedLoading" :data="fileData" :props="defaultProps">
              <template #default="{ node, data }">
                <el-icon v-if="!node.isLeaf"><folder-icon /></el-icon>
                <el-icon v-if="node.isLeaf"><document-icon /></el-icon>
                <div
                  class="inline-flex items-center"
                  :class="
                    node.label == 'metadata.xlsx' &&
                    workflow.generateNextGenHighThroughputSequencingMetadata
                      ? 'text-secondary-500'
                      : ''
                  "
                >
                  <span>
                    {{ node.label }}
                  </span>

                  <button
                    v-if="node.isLeaf"
                    @click="handleNodeClick(data, 'view')"
                    class="ml-2 flex items-center rounded-lg bg-primary-100 py-[3px] shadow-sm transition-all hover:bg-primary-200"
                  >
                    <el-icon><view-icon /></el-icon>
                  </button>
                  <button
                    @click="handleNodeClick(data, 'download')"
                    class="ml-2 flex items-center rounded-lg bg-primary-100 py-[3px] shadow-sm transition-all hover:bg-primary-200"
                    v-if="
                      node.label == 'metadata.xlsx' &&
                      workflow.generateNextGenHighThroughputSequencingMetadata
                    "
                  >
                    <el-icon><download-icon /> </el-icon>
                  </button>
                </div>
              </template>
            </el-tree-v2>
            <div class="flex items-center justify-center" v-else>
              <Vue3Lottie
                animationLink="https://assets1.lottiefiles.com/packages/lf20_nninlpvr.json"
                :width="150"
                :height="150"
              />
            </div>
          </fade-transition>
        </div>
        <el-drawer
          v-if="anyFilePreview"
          v-model="drawerModel"
          :title="fileTitle"
          direction="rtl"
          size="60%"
          :before-close="handleCloseDrawer"
          :lock-scroll="false"
        >
          <el-scrollbar style="height: calc(100vh - 45px)"> </el-scrollbar>
        </el-drawer>
      </div>

      <line-divider></line-divider>
      <fade-transition>
        <div v-if="ready">
          <p v-if="uploadToGEO" class="my-10 w-full text-center">
            Please pick the folder in where to generate your dataset <br />
            <span class="text-xs"> Some additional text here to explain what to do next. </span>
          </p>
          <!-- I think these two should be flipped but we shall see in the future. Also add a folder destination selector -->
          <div v-else class="flex flex-col py-10">
            <p class="mb-5">
              You can review your dataset before uploading it to NCBI GEO. FAIRShare will help you
              with your upload to NCBI GEO in the next step.
            </p>
            <span>
              Please provide a folder path to generate the final dataset on your computer. <br />
            </span>

            <folder-path-input v-model="folderPath" @folderSelected="setDestinationFolderPath" />
          </div>
        </div>
        <LoadingFoldingCube v-else></LoadingFoldingCube>
      </fade-transition>

      <lottie-dialog
        ref="generateDialog"
        animationURL="https://assets4.lottiefiles.com/packages/lf20_45rapv.json"
        title="Please wait while we generate your dataset"
        :width="400"
        :height="250"
        content=""
        :showCancelButton="false"
        :showConfirmButton="false"
      >
      </lottie-dialog>

      <success-confirm
        ref="successConfirm"
        title="Your dataset has been generated"
        :preventOutsideClick="true"
        cancelButtonText="No, I'll do it later"
        confirmButtonText="Yes, Upload to GEO"
        @messageConfirmed="navigateToFinalPage"
      >
        <p class="text-center text-base text-gray-500">
          Do you want us to upload this dataset to GEO?
        </p>
      </success-confirm>

      <fade-transition>
        <div class="flex w-full flex-row justify-center space-x-4 py-2" v-if="finishedLoading">
          <router-link
            :to="`/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/selectDestination`"
            class=""
          >
            <button class="primary-plain-button">
              <el-icon><d-arrow-left /></el-icon> Back
            </button>
          </router-link>

          <button class="primary-button" @click="navigateToUploadToGEO(false)" v-if="uploadToGEO">
            Start upload
            <el-icon> <d-arrow-right /> </el-icon>
          </button>
          <button
            class="primary-button"
            @click="generateDataset"
            v-else
            :disabled="folderPath === ''"
          >
            Generate at folder location
            <el-icon> <d-arrow-right /> </el-icon>
          </button>
        </div>
      </fade-transition>
    </div>
    <app-docs-link url="curate-and-share/zenodo-upload-summary" position="bottom-4" />
  </div>
</template>

<script>
import LoadingFoldingCube from "@/components/spinners/LoadingFoldingCube";

import { useDatasetsStore } from "@/store/datasets";
import { useTokenStore } from "@/store/access.js";

import axios from "axios";
import path from "path";
import dayjs from "dayjs";

import { v4 as uuidv4 } from "uuid";
import { ElLoading } from "element-plus";

export default {
  name: "GEOGenerate",
  components: { LoadingFoldingCube },
  data() {
    return {
      datasetStore: useDatasetsStore(),
      tokens: useTokenStore(),
      dataset: {},
      folderPath: "",
      workflowID: this.$route.params.workflowID,
      workflow: {},
      uploadToGEO: false,
      errorMessage: "",
      ready: false,
      showFiles: "1",
      licenseData: "",
      folder_path: "",
      datasetFolderName: "",
      tableData: [],
      tableDataRecord: [],
      fileData: [],
      defaultProps: {
        value: "id",
        children: "children",
        label: "label",
      },
      fileTitle: "",
      showContinueSection: false,
      drawerModel: true,
      showLoading: false,
      finishedLoading: false,
    };
  },
  //el-tree-node__content
  computed: {
    codePresent() {
      if ("type" in this.workflow) {
        return this.workflow.type.includes("Code");
      }
      return false;
    },

    anyFilePreview() {
      return false;
    },
  },
  methods: {
    async sleep(ms) {
      return new Promise((resolve) => setTimeout(resolve, ms));
    },

    async openFileExplorer(path) {
      this.showLoading = ElLoading.service({
        lock: true,
        text: "Loading",
        background: "rgba(0, 0, 0, 0.7)",
      });
      const response = await axios
        .post(`${this.$server_url}/utilities/openfileexplorer`, {
          file_path: path,
        })
        .then((response) => {
          this.showLoading.close();
          return response.data;
        })
        .catch((error) => {
          this.showLoading.close();

          console.error(error);
          return "ERROR";
        });
      return response;
    },
    async readFolderContents(dir) {
      const response = await axios
        .post(`${this.$server_url}/utilities/readfoldercontents`, {
          folder_path: dir,
        })
        .then((response) => {
          return response.data;
        })
        .catch((error) => {
          console.log(error);
          return "ERROR";
        });
      return response;
    },
    async showFilePreview() {
      this.finishedLoading = false;

      this.fileData = [];

      this.tableDataRecord = [];

      this.fileData.push(
        await this.readFolderContents(this.dataset.data.NextGenHighThroughputSequencing.folderPath)
      );

      this.ready = true;
      this.finishedLoading = true;
    },
    handleCloseDrawer() {},
    async handleOpenDrawer(title) {
      this.fileTitle = title;
    },
    async handleNodeClick(data) {
      if (!data.isDir) {
        if (!data.isDir) {
          await this.openFileExplorer(data.fullpath);
        }

        let title = data.label;
        this.handleOpenDrawer(title);
      }
    },

    jsonToTableDataRecursive(jsonObject, parentId, parentName) {
      // console.log("obj: ", jsonObject)
      if (
        jsonObject &&
        typeof jsonObject === "object" &&
        Object.keys(jsonObject).length != 0 &&
        !Array.isArray(jsonObject)
      ) {
        // object child
        let result = [];
        let count = 1;
        for (let property in jsonObject) {
          //console.log(property, jsonObject);
          let newObj = { Name: "", Value: "" };
          let newId = parentId + String(count);
          let value = this.jsonToTableDataRecursive(jsonObject[property], newId, property);
          // console.log(property, value)
          if (Array.isArray(value)) {
            newObj.id = newId;
            newObj.Name = property;
            newObj.Value = "";
            newObj.children = value;
          } else {
            newObj.id = newId;
            newObj.Name = property;
            newObj.Value = value;
          }
          result.push(newObj);
          count += 1;
        }
        return result;
      } else if (jsonObject && Array.isArray(jsonObject) && jsonObject.length != 0) {
        // array
        let result = [];
        for (let i = 0; i < jsonObject.length; i++) {
          let newObj = { Name: "", Value: "" };
          let newId = parentId + String(i);
          let newName = "";

          let customName = "";

          switch (parentName) {
            case "keywords":
              customName = "keyword";
              break;
            case "authors":
              customName = "author";
              break;
            case "contributors":
              customName = "contributor";
              break;
            default:
              customName = parentName;
              break;
          }

          const readableIndex = i + 1;

          if (readableIndex % 10 == 1 && readableIndex % 100 != 11) {
            newName = String(i + 1) + "st " + customName;
          } else if (readableIndex % 10 == 2 && readableIndex % 100 != 12) {
            newName = String(i + 1) + "nd " + customName;
          } else if (readableIndex % 10 == 3 && readableIndex % 100 != 13) {
            newName = String(i + 1) + "rd " + customName;
          } else {
            newName = String(i + 1) + "th " + customName;
          }

          let value = this.jsonToTableDataRecursive(jsonObject[i], newId, newName);

          if (Array.isArray(value)) {
            newObj.id = newId;
            newObj.Name = newName;
            newObj.Value = "";
            newObj.children = value;
          } else {
            newObj.id = newId;
            newObj.Name = newName;
            newObj.Value = value;
            newObj.children = [];
          }

          result.push(newObj);
        }
        return result;
      } else {
        // string, empty obj, empty arr
        return jsonObject;
      }
    },

    async checkToken(token) {
      console.log(token);
      const response = await this.tokens.getDepositions(token);

      if (response.status === 200) {
        this.uploadToGEO = true;
        this.tokens.saveToken("zenodo", token);
        return true;
      } else if (response.status === 401) {
        this.errorMessage =
          "Invalid Zenodo access token. Please enter a valid Zenodo access token.";
        this.uploadToGEO = false;
        return false;
      } else {
        this.errorMessage = "Something went wrong. Please try again.";
        this.uploadToGEO = false;
        return false;
      }
    },
    /**
     * Uploads the dataset to GEO
     * TODO: handle skip upload
     * @param {boolean} _skipUpload
     * @returns {Promise<void>}
     */
    async navigateToUploadToGEO(_skipUpload = false) {
      const routerPath = `/datasets/${this.datasetID}/${this.workflowID}/ncbigeo/upload`;
      if (this.uploadToGEO) {
        this.$router.push({ path: routerPath });
      } else {
        this.$router.push({ path: routerPath });
      }
    },

    setDestinationFolderPath(path) {
      this.folderPath = path;
    },

    async generateDataset() {
      this.$refs.generateDialog.show();

      await this.sleep(1000);

      const now = dayjs();
      const destinationFolderPath = this.folderPath;

      /**
       * create a unique ID for the dataset and append to dataset folder
       * TODO: handle if dataset folder already exists
       * */
      const ID = uuidv4();

      this.datasetFolderName = `geo_submission_${now.format("MMMMDD")}-${ID.substring(
        ID.length - 5
      )}`.toLocaleLowerCase();

      let response = await axios
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

      if (response === "ERROR") {
        this.errorMessage =
          "Something went wrong with generating the metadata file. Please try again.";
        this.$refs.generateDialog.hide();
        return;
      }

      const source_file_path = path.join(this.$home_path, ".fairshare", "temp", "metadata.xlsx");
      const destination_file_path = path.join(
        destinationFolderPath,
        this.datasetFolderName,
        "metadata.xlsx"
      );

      response = await axios
        .post(`${this.$server_url}/utilities/copyfile`, {
          source_file_path,
          destination_file_path,
        })
        .then((response) => {
          this.$track("Metadata", "Move geoMetadata", "success");
          return response.data;
        })
        .catch((error) => {
          this.$track("Metadata", "Move geoMetadata", "failed");
          console.error(error);
          return "ERROR";
        });

      if (response === "ERROR") {
        this.errorMessage = "Something went wrong with moving the metadata file. Please try again.";
        this.$refs.generateDialog.hide();
        return;
      }

      const metadataObject = this.dataset.data.NextGenHighThroughputSequencing.questions;

      let allFiles = [];

      for (const sample of metadataObject.samples) {
        for (const file of sample.rawFiles) {
          allFiles.push(file);
        }
        for (const file of sample.processedDataFiles) {
          allFiles.push(file);
        }
      }

      allFiles = [...new Set(allFiles)]; // remove duplicates

      for (const file of allFiles) {
        const fileName = path.basename(file);

        const destination_file_path = path.join(
          destinationFolderPath,
          this.datasetFolderName,
          fileName
        );

        response = await axios
          .post(`${this.$server_url}/utilities/copyfile`, {
            source_file_path: file,
            destination_file_path,
          })
          .then((response) => {
            this.$track("Metadata", "Copy geo file", "success");
            return response.data;
          })
          .catch((error) => {
            this.$track("Metadata", "Copy geo file", "failed");
            console.error(error);
            return "ERROR";
          });

        if (response === "ERROR") {
          this.errorMessage = "Something went wrong with copying your files. Please try again.";
          this.$refs.generateDialog.hide();
          return;
        }
      }

      this.$refs.generateDialog.hide();

      this.$refs.successConfirm.show();
    },

    async navigateToFinalPage() {
      this.workflow.destinationFolderPath = path.join(this.folderPath, this.datasetFolderName);

      await this.datasetStore.updateCurrentDataset(this.dataset);
      await this.datasetStore.syncDatasets();

      const routerPath = `/datasets/${this.datasetID}/${this.workflowID}/ncbigeo/upload`;

      this.$router.push({ path: routerPath });
    },
  },
  async mounted() {
    this.dataset = await this.datasetStore.getCurrentDataset();
    this.workflow = this.dataset.workflows[this.workflowID];

    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("geo");
    this.datasetStore.setCurrentStep(5);

    this.workflow.currentRoute = this.$route.path;

    this.uploadToGEO = false;

    this.showFilePreview();
  },
};
</script>
