<template>
  <div class="flex h-full w-full max-w-screen-xl flex-col items-center justify-center p-3 pr-5">
    <div class="flex h-full w-full flex-col">
      <span class="text-left text-lg font-medium"> Summary </span>

      <el-divider class="my-2"> </el-divider>

      <div>
        <p class="mb-5">
          You have selected to not upload your dataset on a repository. An overview of your dataset
          is provided below. Metadata files that will be generated and included by FAIRshare (if
          any) at your source folder selected in Step 1 are highlighted in orange. Click continue
          below to generate these files.
        </p>
        <div class="h-[200px] overflow-auto">
          <transition name="fade" mode="out-in" appear>
            <el-tree-v2 v-if="finishedLoading" :data="fileData" :props="defaultProps">
              <template #default="{ node, data }">
                <el-icon v-if="!node.isLeaf"><folder-icon /></el-icon>
                <el-icon v-if="node.isLeaf"><document-icon /></el-icon>
                <div
                  class="inline-flex items-center"
                  :class="
                    (node.label == 'codemeta.json' && workflow.generateCodeMeta) ||
                    (node.label == 'CITATION.cff' && workflow.generateCodeMeta) ||
                    (node.label == 'LICENSE' && workflow.generateLicense)
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
                      (node.label == 'codemeta.json' && workflow.generateCodeMeta) ||
                      (node.label == 'CITATION.cff' && workflow.generateCodeMeta) ||
                      (node.label == 'LICENSE' && workflow.generateLicense)
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
          </transition>
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
          <el-scrollbar style="height: calc(100vh - 45px)">
            <div v-if="PreviewNewlyCreatedMetadataFile" class="pb-20">
              <el-table
                :data="tableData"
                style="width: 100%"
                row-key="id"
                border
                default-expand-all
              >
                <el-table-column prop="Name" label="Name" />
                <el-table-column prop="Value" label="Value" />
              </el-table>
            </div>

            <div v-if="PreviewNewlyCreatedCitationFile" class="pb-20">
              <el-table
                :data="citationData"
                style="width: 100%"
                row-key="id"
                border
                default-expand-all
              >
                <el-table-column prop="Name" label="Name" />
                <el-table-column prop="Value" label="Value" class="break-normal" />
              </el-table>
              <p class="pt-4 text-sm text-zinc-400">
                # This CITATION.cff file was generated with FAIRshare.
              </p>
              <p class="text-sm text-zinc-400">
                # Visit https://fairdataihub.org/fairshare to learn more!
              </p>
            </div>

            <div v-if="PreviewNewlyCreatedLicenseFile" class="">
              <div class="prose prose-base prose-slate pb-20" v-html="compiledLicense"></div>
            </div>
          </el-scrollbar>
        </el-drawer>
      </div>

      <line-divider></line-divider>

      <transition name="fade" mode="out-in" appear>
        <div class="flex w-full flex-row justify-center space-x-4 py-2">
          <router-link
            :to="`/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/selectDestination`"
            class=""
          >
            <button class="primary-plain-button">
              <el-icon><d-arrow-left /></el-icon> Back
            </button>
          </router-link>

          <button class="primary-button" @click="generateMetadataFiles">
            Continue
            <el-icon> <d-arrow-right /> </el-icon>
          </button>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
import { useDatasetsStore } from "@/store/datasets";
import { useTokenStore } from "@/store/access.js";

import axios from "axios";
import fs from "fs-extra";
import path from "path";
import { app, dialog } from "@electron/remote";
import { ElLoading } from "element-plus";
import { marked } from "marked";
import { v4 as uuidv4 } from "uuid";

export default {
  name: "LocalNoUploadSummary",

  data() {
    return {
      datasetStore: useDatasetsStore(),
      tokens: useTokenStore(),
      dataset: {},
      folderPath: "",
      workflowID: this.$route.params.workflowID,
      workflow: {},
      ready: false,
      showFiles: "1",
      licenseData: "",
      tableData: [],
      citationData: [],
      tableDataRecord: [],
      citationDataRecord: [],
      fileData: [],
      defaultProps: {
        value: "id",
        children: "children",
        label: "label",
      },
      fileTitle: "",
      showContinueSection: false,
      PreviewNewlyCreatedLicenseFile: false,
      PreviewNewlyCreatedMetadataFile: false,
      PreviewNewlyCreatedCitationFile: false,
      drawerModel: true,
      showLoading: false,
      finishedLoading: false,
    };
  },
  //el-tree-node__content
  computed: {
    anyfilePreview() {
      if (
        this.PreviewNewlyCreatedMetadataFile ||
        this.PreviewNewlyCreatedLicenseFile ||
        this.PreviewNewlyCreatedCitationFile
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
    async createCodeMetadataFile() {
      const response = await axios
        .post(`${this.$server_url}/metadata/create`, {
          data_types: JSON.stringify(this.workflow.type),
          data_object: JSON.stringify(this.dataset.data),
          virtual_file: true,
        })
        .then((response) => {
          return JSON.parse(response.data);
        })
        .catch((error) => {
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
          virtual_file: true,
        })
        .then((response) => {
          return JSON.parse(response.data);
        })
        .catch((error) => {
          console.error(error);
          return "ERROR";
        });
      return response;
    },
    async createLicenseFile() {
      const folderPath = this.dataset.data[this.workflow.type[0]].folderPath;
      const response = await axios
        .post(`${this.$server_url}/utilities/createfile`, {
          folder_path: folderPath,
          file_name: "LICENSE",
          file_content: this.workflow.licenseText,
          content_type: "text",
        })
        .then((response) => {
          return response.data;
        })
        .catch((error) => {
          console.error(error);
          return "ERROR";
        });
      return response;
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
      this.fileData = [];

      this.tableDataRecord = [];
      this.citationDataRecord = [];
      this.tableData = await this.createCodeMetadataFile();
      this.citationData = await this.createCitationFile();
      this.tableDataRecord = Object.assign({}, this.tableData);
      this.citationDataRecord = Object.assign({}, this.citationData);

      this.fileData.push(await this.readFolderContents(this.dataset.data.Code.folderPath));

      let root = this.fileData[0];

      if (!root.children.some((el) => el.label === "codemeta.json")) {
        if (this.workflow.generateCodeMeta) {
          let newObj = {};
          newObj.id = uuidv4();
          newObj.label = "codemeta.json";
          newObj.isDir = false;

          root.children.push(newObj);
        }
      }

      if (!root.children.some((el) => el.label === "CITATION.cff")) {
        if (this.workflow.generateCodeMeta) {
          let newObj = {};
          newObj.id = uuidv4();
          newObj.label = "CITATION.cff";
          newObj.isDir = false;

          root.children.push(newObj);
        }
      }

      if (!root.children.some((el) => el.label === "LICENSE")) {
        if (this.workflow.generateLicense) {
          let newObj = {};
          newObj.id = uuidv4();
          newObj.label = "LICENSE";
          newObj.isDir = false;

          root.children.push(newObj);
        }
      }

      this.tableData = this.jsonToTableDataRecursive(this.tableData, 1, "ROOT");

      this.citationData = this.jsonToTableDataRecursive(this.citationData, 1, "ROOT");

      if (this.workflow.generateLicense) {
        this.licenseData = this.workflow.licenseText;
      }

      this.ready = true;
      this.finishedLoading = true;
    },
    handleCloseDrawer() {
      this.fileTitle = "";
      this.PreviewNewlyCreatedLicenseFile = false;
      this.PreviewNewlyCreatedMetadataFile = false;
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
        if (data.label == "LICENSE" && this.workflow.generateLicense) {
          if (action === "view") {
            this.PreviewNewlyCreatedLicenseFile = true;
          }

          if (action === "download") {
            this.exportToJson(this.licenseData, "LICENSE");
          }
        } else if (data.label == "codemeta.json") {
          if (action === "view") {
            this.PreviewNewlyCreatedMetadataFile = true;
          }
          if (action === "download") {
            this.exportToJson(this.tableDataRecord, "codemeta.json");
          }
        } else if (data.label == "CITATION.cff") {
          if (action === "view") {
            this.PreviewNewlyCreatedCitationFile = true;
          }
          if (action === "download") {
            this.exportToJson(this.citationDataRecord, "CITATION.cff");
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

    async generateMetadataFiles() {
      const routerPath = `/datasets/${this.datasetID}/${this.workflowID}/localNoUpload/generate`;

      this.$router.push({ path: routerPath });
    },
  },
  async mounted() {
    this.dataset = await this.datasetStore.getCurrentDataset();
    this.workflow = this.dataset.workflows[this.workflowID];

    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(6);

    this.workflow.currentRoute = this.$route.path;

    this.showFilePreview();
  },
};
</script>
