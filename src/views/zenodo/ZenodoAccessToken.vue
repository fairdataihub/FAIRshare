<template>
  <div class="flex h-full w-full max-w-screen-xl flex-col items-center justify-center p-3 pr-5">
    <div class="flex h-full w-full flex-col">
      <span class="text-left text-lg font-medium"> Summary </span>
      <!-- <span class="text-left">
        We will use this to upload and edit your dataset on your Zenodo account.
      </span> -->

      <line-divider />

      <div>
        <p class="mb-5">
          A list of all the files and folders that we are going to upload to Zenodo is shown below.
          Files that will be created by FAIRshare are highlighted in orange. You can click on any of
          them to view their contents or open the file in your file browser.
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
                    (node.label == 'codemeta.json' && workflow.generateCodeMeta) ||
                    (node.label == 'CITATION.cff' && workflow.generateCodeMeta) ||
                    (node.label == 'LICENSE' && workflow.generateLicense) ||
                    (node.label == 'basic_study_design.txt' &&
                      workflow.generateImmunologyMetadata) ||
                    (node.label == 'protocols.txt' && workflow.generateImmunologyMetadata) ||
                    (node.label == 'metadata.json' && workflow.generateOtherMetadata)
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
                      (node.label == 'LICENSE' && workflow.generateLicense) ||
                      (node.label == 'basic_study_design.txt' &&
                        workflow.generateImmunologyMetadata) ||
                      (node.label == 'protocols.txt' && workflow.generateImmunologyMetadata) ||
                      (node.label == 'metadata.json' && workflow.generateOtherMetadata)
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
          <el-scrollbar style="height: calc(100vh - 45px)">
            <div v-if="PreviewNewlyCreatedCodemetaFile" class="pb-20">
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

            <div v-if="PreviewNewlyCreatedImmunologyMetadataFile" class="pb-20">
              <el-table
                :data="immunologyMetadata"
                style="width: 100%"
                row-key="id"
                border
                default-expand-all
              >
                <el-table-column prop="Name" label="Name" />
                <el-table-column prop="Value" label="Value" />
              </el-table>
            </div>

            <div v-if="PreviewNewlyCreatedImmunologyProtocolMetadataFile" class="pb-20">
              <el-table
                :data="immunologyProtocolMetadata"
                style="width: 100%"
                row-key="id"
                border
                default-expand-all
              >
                <el-table-column prop="Name" label="Name" />
                <el-table-column prop="Value" label="Value" />
              </el-table>
            </div>

            <div v-if="PreviewNewlyCreatedOtherMetadataFile" class="pb-20">
              <el-table
                :data="otherMetadata"
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

      <fade-transition>
        <div v-if="ready">
          <p v-if="validTokenAvailable" class="my-10 w-full text-center">
            It looks like you have already connected your Zenodo account with FAIRshare. <br />
            Click on the 'Start upload' button below to upload your dataset. <br />
            <span class="text-xs">
              Note that this will create a draft of the dataset on Zenodo that is only visible to
              you. <br />
              You will be prompted to Publish the dataset and make it openly available after the
              upload.
            </span>
          </p>
          <!-- show error message if token is not valid -->
          <div v-else class="flex flex-col items-center justify-center py-10">
            <p class="mb-5">
              We couldn't find your Zenodo account details. Please click on the button below to
              connect to your Zenodo account for uploading your dataset.
            </p>

            <ConnectZenodo :statusChangeFunction="showConnection"></ConnectZenodo>
          </div>
        </div>
        <LoadingFoldingCube v-else></LoadingFoldingCube>
      </fade-transition>

      <fade-transition>
        <div class="flex w-full flex-row justify-center space-x-4 py-2" v-if="finishedLoading">
          <router-link
            :to="`/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/zenodo/metadata`"
            class=""
          >
            <button class="primary-plain-button">
              <el-icon><d-arrow-left /></el-icon> Back
            </button>
          </router-link>

          <button
            class="secondary-plain-button hidden"
            @click="showFilePreview"
            v-if="validTokenAvailable"
          >
            <el-icon><checked-icon /></el-icon>
            View files ready for upload
          </button>

          <button
            class="primary-button"
            :disabled="disableContinue"
            @click="uploadToZenodo"
            v-if="validTokenAvailable"
          >
            Start upload
            <el-icon> <d-arrow-right /> </el-icon>
          </button>
        </div>
      </fade-transition>
    </div>
    <app-docs-link url="curate-and-share/zenodo/zenodo-upload-summary" position="bottom-4" />
  </div>
</template>

<script>
import LoadingFoldingCube from "@/components/spinners/LoadingFoldingCube";
import ConnectZenodo from "@/components/serviceIntegration/ConnectZenodo";

import { useDatasetsStore } from "@/store/datasets";
import { useTokenStore } from "@/store/access.js";

import axios from "axios";
import fs from "fs-extra";
import path from "path";
import { dialog } from "@electron/remote";
import { ElLoading } from "element-plus";
import { marked } from "marked";
import { v4 as uuidv4 } from "uuid";

export default {
  name: "ZenodoAccessToken",
  components: { LoadingFoldingCube, ConnectZenodo },
  data() {
    return {
      datasetStore: useDatasetsStore(),
      tokens: useTokenStore(),
      dataset: {},
      folderPath: "",
      workflowID: this.$route.params.workflowID,
      workflow: {},
      validTokenAvailable: false,
      errorMessage: "",
      zenodoAccessToken: "",
      ready: false,
      licenseData: "",
      tableData: [],
      citationData: [],
      immunologyMetadata: [],
      immunologyProtocolMetadata: [],
      otherMetadata: [],
      tableDataRecord: [],
      citationDataRecord: [],
      immunologyMetadataRecord: [],
      immunologyProtocolMetadataRecord: [],
      otherMetadataRecord: [],
      fileData: [],
      defaultProps: {
        value: "id",
        children: "children",
        label: "label",
      },
      fileTitle: "",
      PreviewNewlyCreatedLicenseFile: false,
      PreviewNewlyCreatedCodemetaFile: false,
      PreviewNewlyCreatedImmunologyMetadataFile: false,
      PreviewNewlyCreatedImmunologyProtocolMetadataFile: false,
      PreviewNewlyCreatedCitationFile: false,
      PreviewNewlyCreatedOtherMetadataFile: false,
      drawerModel: true,
      showLoading: false,
      finishedLoading: false,
    };
  },

  computed: {
    codePresent() {
      if ("type" in this.workflow) {
        return this.workflow.type.includes("Code");
      }
      return false;
    },
    immunologyPresent() {
      if ("type" in this.workflow) {
        return this.workflow.type.includes("Immunology");
      }
      return false;
    },
    disableContinue() {
      if (this.validTokenAvailable) {
        return false;
      }
      if (!this.validTokenAvailable && this.zenodoAccessToken !== "") {
        return false;
      }
      return true;
    },

    anyFilePreview() {
      if (
        this.PreviewNewlyCreatedCodemetaFile ||
        this.PreviewNewlyCreatedLicenseFile ||
        this.PreviewNewlyCreatedCitationFile ||
        this.PreviewNewlyCreatedImmunologyMetadataFile ||
        this.PreviewNewlyCreatedImmunologyProtocolMetadataFile ||
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
            defaultPath: path.join(this.$downloads_path, file_name),
          })
          .then((result) => {
            const fileData = typeof obj === "object" ? JSON.stringify(obj) : obj;
            fs.writeFile(result.filePath, fileData, (err) => {
              if (err) {
                console.error(err);
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
                this.openFileExplorer(path.join(this.$downloads_path, file_name));
              }
            });
          })
          .catch((err) => {
            console.error(err);
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
    async createImmunologyMetadataFile() {
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
    // Other is identical to code endpoint. Not sure if i'll leave it this way. Adding separate ones for now.
    async createOtherMetadataFile() {
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
      // return { name: "metadata.json" };
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
          console.error(error);
          return "ERROR";
        });
      return response;
    },
    async showFilePreview() {
      this.finishedLoading = false;

      this.fileData = [];

      this.tableDataRecord = [];
      this.citationDataRecord = [];
      this.immunologyMetadataRecod = [];
      this.immunologyProtocolMetadataRecord = [];
      this.otherMetadataRecord = [];

      if (this.workflow.generateCodeMeta) {
        this.tableData = await this.createCodeMetadataFile();
        this.citationData = await this.createCitationFile();
        this.tableDataRecord = Object.assign({}, this.tableData);
        this.citationDataRecord = Object.assign({}, this.citationData);
      }

      if (this.workflow.generateImmunologyMetadata) {
        const combinedImmunologyMetadata = await this.createImmunologyMetadataFile();

        this.immunologyMetadata = combinedImmunologyMetadata.basic_study_design;
        this.immunologyProtocolMetadata = combinedImmunologyMetadata.basic_study_protocols;

        this.immunologyMetadataRecord = Object.assign(
          {},
          this.immunologyMetadata.basic_study_design
        );
        this.immunologyProtocolMetadataRecord = Object.assign(
          {},
          this.immunologyMetadata.basic_study_protocols
        );
      }

      if (this.workflow.generateOtherMetadata) {
        this.otherMetadata = await this.createOtherMetadataFile();
        this.otherMetadataRecord = Object.assign({}, this.otherMetadata);
      }

      if (this.codePresent) {
        this.fileData.push(await this.readFolderContents(this.dataset.data.Code.folderPath));
      } else if (this.immunologyPresent) {
        this.fileData.push(await this.readFolderContents(this.dataset.data.Immunology.folderPath));
      } else {
        this.fileData.push(await this.readFolderContents(this.dataset.data.Other.folderPath));
      }

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

      if (!root.children.some((el) => el.label === "basic_study_design.txt")) {
        if (this.workflow.generateImmunologyMetadata) {
          let newObj = {};
          newObj.id = uuidv4();
          newObj.label = "basic_study_design.txt";
          newObj.isDir = false;

          root.children.push(newObj);
        }
      }

      if (!root.children.some((el) => el.label === "protocols.txt")) {
        if (this.workflow.generateImmunologyMetadata) {
          let newObj = {};
          newObj.id = uuidv4();
          newObj.label = "protocols.txt";
          newObj.isDir = false;

          root.children.push(newObj);
        }
      }

      if (!root.children.some((el) => el.label === "metadata.json")) {
        if (this.workflow.generateOtherMetadata) {
          let newObj = {};
          newObj.id = uuidv4();
          newObj.label = "metadata.json";
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

      this.immunologyMetadata = this.jsonToTableDataRecursive(this.immunologyMetadata, 1, "ROOT");
      this.immunologyProtocolMetadata = this.jsonToTableDataRecursive(
        this.immunologyProtocolMetadata,
        1,
        "ROOT"
      );

      this.otherMetadata = this.jsonToTableDataRecursive(this.otherMetadata, 1, "ROOT");

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
      this.PreviewNewlyCreatedCodemetaFile = false;
      this.PreviewNewlyCreatedImmunologyMetadataFile = false;
      this.PreviewNewlyCreatedImmunologyProtocolMetadataFile = false;
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
        if (data.label == "LICENSE" && this.workflow.generateLicense) {
          if (action === "view") {
            this.PreviewNewlyCreatedLicenseFile = true;
          }

          if (action === "download") {
            this.exportToJson(this.licenseData, "LICENSE");
          }
        } else if (data.label == "codemeta.json" && this.workflow.generateCodeMeta) {
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
        } else if (
          data.label == "basic_study_design.txt" &&
          this.workflow.generateImmunologyMetadata
        ) {
          if (action === "view") {
            this.PreviewNewlyCreatedImmunologyMetadataFile = true;
          }
          if (action === "download") {
            this.exportToJson(this.immunologyMetadataRecord, "basic_study_design.txt");
          }
        } else if (data.label == "protocols.txt" && this.workflow.generateImmunologyMetadata) {
          if (action === "view") {
            this.PreviewNewlyCreatedImmunologyProtocolMetadataFile = true;
          }
          if (action === "download") {
            this.exportToJson(this.immunologyProtocolMetadata, "protocols.txt");
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
          let newObj = { Name: "", Value: "" };
          let newId = parentId + String(count);
          let value = this.jsonToTableDataRecursive(jsonObject[property], newId, property);
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
      const response = await this.tokens.getDepositions(token);

      if (response.status === 200) {
        this.validTokenAvailable = true;
        this.tokens.saveToken("zenodo", token);
        return true;
      } else if (response.status === 401) {
        this.errorMessage =
          "Invalid Zenodo access token. Please enter a valid Zenodo access token.";
        this.validTokenAvailable = false;
        return false;
      } else {
        this.errorMessage = "Something went wrong. Please try again.";
        this.validTokenAvailable = false;
        return false;
      }
    },
    async uploadToZenodo() {
      const routerPath = `/datasets/${this.datasetID}/${this.workflowID}/zenodo/upload`;
      if (this.validTokenAvailable) {
        this.$router.push({ path: routerPath });
      } else {
        const zenodoToken = this.zenodoAccessToken;
        const res = await this.checkToken(zenodoToken);

        if (res) {
          this.$router.push({ path: routerPath });
        }
      }
    },
    async showConnection(status) {
      if (status === "connected") {
        this.validTokenAvailable = true;
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

    const validZenodoConnection = await this.tokens.verifyZenodoConnection();

    if (validZenodoConnection) {
      this.validTokenAvailable = true;
    } else {
      this.validTokenAvailable = false;
    }

    this.showFilePreview();
  },
};
</script>
