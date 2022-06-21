<template>
  <div class="flex h-full w-full max-w-screen-xl flex-col items-center justify-center p-3 pr-5">
    <div class="flex h-full w-full flex-col">
      <span class="text-left text-lg font-medium"> Summary </span>

      <el-divider class="my-4"> </el-divider>

      <div>
        <p class="mb-5">
          A list of all the files and folders that could be uploaded to NCBI GEO is shown below.
        </p>
        <div class="overflow-auto" :class="{ 'h-[200px]': finishedLoading }">
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
          v-if="anyfilePreview"
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
          <div v-else class="flex flex-col items-center justify-center py-10">
            <p class="mb-5 text-center">
              FAIRshare does not currently support the upload process to GEO. <br />
              We can generate the metadata file for you, but you will need to upload the data files
              to GEO manually.
            </p>
          </div>
        </div>
        <LoadingFoldingCube v-else></LoadingFoldingCube>
      </fade-transition>

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

          <button class="secondary-plain-button hidden" @click="showFilePreview">
            <el-icon><checked-icon /></el-icon>
            View files ready for upload
          </button>

          <button class="primary-button" @click="navigateToUploadToGEO(false)" v-if="uploadToGEO">
            Start upload
            <el-icon> <d-arrow-right /> </el-icon>
          </button>
          <button class="primary-button" @click="navigateToUploadToGEO(true)" v-else>
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
import fs from "fs-extra";
import path from "path";
import { app, dialog } from "@electron/remote";
import { ElLoading } from "element-plus";
import { marked } from "marked";

export default {
  name: "ZenodoAccessToken",
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
      zenodoAccessToken: "",
      ready: false,
      showFiles: "1",
      licenseData: "",
      tableData: [],
      citationData: [],
      otherMetadata: [],
      tableDataRecord: [],
      citationDataRecord: [],
      otherMetadataRecord: [],
      fileData: [],
      defaultProps: {
        value: "id",
        children: "children",
        label: "label",
      },
      fileTitle: "",
      showContinueSection: false,
      PreviewNewlyCreatedLicenseFile: false,
      PreviewNewlyCreatedCodemetaFile: false,
      PreviewNewlyCreatedCitationFile: false,
      PreviewNewlyCreatedOtherMetadataFile: false,
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

    anyfilePreview() {
      if (
        this.PreviewNewlyCreatedCodemetaFile ||
        this.PreviewNewlyCreatedLicenseFile ||
        this.PreviewNewlyCreatedCitationFile ||
        this.PreviewNewlyCreatedOtherMetadataFile
      ) {
        return true;
      } else {
        return false;
      }
    },

    compiledLicense() {
      return marked(this.licenseData);
    },
  },
  methods: {
    exportToJson(obj, file_name) {
      let contentType = "application/json;charset=utf-8;";

      if (window.navigator && window.navigator.msSaveOrOpenBlob) {
        var blob = new Blob([decodeURIComponent(encodeURI(JSON.stringify(obj)))], {
          type: contentType,
        });
        navigator.msSaveOrOpenBlob(blob, file_name);
      } else {
        dialog
          .showSaveDialog({
            title: `Save ${file_name}`,
            defaultPath: path.join(app.getPath("downloads"), file_name),
          })
          .then((result) => {
            const fileData = typeof obj === "object" ? JSON.stringify(obj) : obj;
            console.log(result.filePath);
            fs.writeFile(result.filePath, fileData, (err) => {
              if (err) {
                console.log(err);
                this.$notify({
                  title: "Error",
                  type: "error",
                  message: "Something went wrong while saving the file",
                });
              } else {
                this.$notify({
                  title: "Success",
                  message: `${file_name} saved successfully`,
                  type: "success",
                  position: "bottom-right",
                });
                this.openFileExplorer(path.join(app.getPath("downloads"), file_name));
              }
            });
          })
          .catch((err) => {
            console.log(err);
          });
      }
    },
    createLoading() {
      const loading = ElLoading.service({
        lock: true,
        text: "Reading data...",
      });
      return loading;
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
      this.citationDataRecord = [];
      this.otherMetadataRecord = [];

      if (this.workflow.generateCodeMeta) {
        this.tableData = await this.createCodeMetadataFile();
        this.citationData = await this.createCitationFile();
        this.tableDataRecord = Object.assign({}, this.tableData);
        this.citationDataRecord = Object.assign({}, this.citationData);
      }

      if (this.workflow.generateOtherMetadata) {
        this.otherMetadata = await this.createOtherMetadataFile();
        this.otherMetadataRecord = Object.assign({}, this.otherMetadata);
      }

      this.fileData.push(
        await this.readFolderContents(this.dataset.data.NextGenHighThroughputSequencing.folderPath)
      );

      this.ready = true;
      this.finishedLoading = true;
    },
    handleCloseDrawer() {
      this.fileTitle = "";
      this.PreviewNewlyCreatedLicenseFile = false;
      this.PreviewNewlyCreatedCodemetaFile = false;
      this.PreviewNewlyCreatedOtherMetadataFile = false;
      this.PreviewNewlyCreatedCitationFile = false;
    },
    async handleOpenDrawer(title) {
      if (title == "LICENSE") {
        title += " (This preview may not be completely representative of the final license)";
      }

      this.fileTitle = title;
    },
    async handleNodeClick(data, action) {
      if (!data.isDir) {
        if (data.label == "codemeta.json" && this.workflow.generateCodeMeta) {
          if (action === "view") {
            this.PreviewNewlyCreatedCodemetaFile = true;
          }
          if (action === "download") {
            this.exportToJson(this.tableDataRecord, "codemeta.json");
          }
        } else if (data.label == "CITATION.cff" && this.workflow.generateCodeMeta) {
          if (action === "view") {
            this.PreviewNewlyCreatedCitationFile = true;
          }
          if (action === "download") {
            this.exportToJson(this.citationDataRecord, "CITATION.cff");
          }
        } else if (data.label == "metadata.json" && this.workflow.generateOtherMetadata) {
          if (action === "view") {
            this.PreviewNewlyCreatedOtherMetadataFile = true;
          }
          if (action === "download") {
            this.exportToJson(this.otherMetadataRecord, "metadata.json");
          }
        } else if (!data.isDir) {
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
  },
  async mounted() {
    this.dataset = await this.datasetStore.getCurrentDataset();
    this.workflow = this.dataset.workflows[this.workflowID];

    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(6);

    this.workflow.currentRoute = this.$route.path;

    this.uploadToGEO = false;

    this.showFilePreview();
  },
};
</script>
