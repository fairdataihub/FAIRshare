<template>
  <div
    class="flex h-full w-full max-w-screen-xl flex-col items-center justify-center p-3 pr-5"
  >
    <div class="flex h-full w-full flex-col">
      <span class="text-left text-lg font-medium">
        Zenodo connection details
      </span>
      <span class="text-left">
        We will use this to upload and edit your dataset on your Zenodo account.
      </span>

      <el-divider class="my-4"> </el-divider>

      <div v-if="ready">
        <p v-if="validTokenAvailable" class="my-10 w-full text-center">
          Looks like we already have your Zenodo login details. Click on the
          'Start upload' button below.
        </p>
        <!-- show error message if token is not valid -->
        <div v-else class="flex flex-col items-center justify-center py-10">
          <p class="mb-5">
            We couldn't find your Zenodo login details. Please click on the
            button below to connect to your Zenodo account.
          </p>

          <ConnectZenodo :statusChangeFunction="showConnection"></ConnectZenodo>
        </div>
      </div>
      <LoadingFoldingCube v-else></LoadingFoldingCube>

      <div class="flex w-full flex-row justify-center space-x-4 py-2">
        <router-link
          :to="`/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/zenodo/metadata`"
          class=""
        >
          <button class="primary-plain-button">
            <el-icon><d-arrow-left /></el-icon> Back
          </button>
        </router-link>

        <button
          class="secondary-plain-button"
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
      <transition appear mode="out-in" name="fade">
        <div v-if="showFilePreviewSection" class="py-5">
          <line-divider />
          <p class="text=lg my-5">
            A list of all the files that we are going to upload to Zenodo is
            shown below. You can click on any of them to view their contents or
            open in your file browser.
          </p>
          <el-tree
            :data="fileData"
            :props="defaultProps"
            @node-click="handleNodeClick"
          >
            <template #default="{ node }">
              <el-icon v-if="!node.isLeaf"><folder-icon /></el-icon>
              <el-icon v-if="node.isLeaf"><document-icon /></el-icon>
              <span
                :class="
                  node.label == 'codemeta.json' ||
                  node.label == 'citation.cff' ||
                  node.label == 'LICENSE'
                    ? 'text-secondary-500'
                    : ''
                "
                >{{ node.label }}</span
              >
            </template>
          </el-tree>

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
                  <el-table-column
                    prop="Value"
                    label="Value"
                    class="break-normal"
                  />
                </el-table>
              </div>

              <div v-if="PreviewNewlyCreatedLicenseFile" class="">
                <div
                  class="prose prose-base prose-slate pb-20"
                  v-html="compiledLicense"
                ></div>
              </div>
            </el-scrollbar>
          </el-drawer>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
import LoadingFoldingCube from "@/components/spinners/LoadingFoldingCube";
import ConnectZenodo from "@/components/serviceIntegration/ConnectZenodo";

import { useDatasetsStore } from "@/store/datasets";
import { useTokenStore } from "@/store/access.js";

import path from "path";
import axios from "axios";
import { ElLoading } from "element-plus";
import { marked } from "marked";

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
      showFiles: "1",
      licenseData: "",
      tableData: [],
      citationData: [],
      fileData: [],
      defaultProps: {
        children: "children",
        label: "label",
      },
      fileTitle: "",
      showFilePreviewSection: false,
      PreviewNewlyCreatedLicenseFile: false,
      PreviewNewlyCreatedMetadataFile: false,
      PreviewNewlyCreatedCitationFile: false,
      drawerModel: true,
      showLoading: false,
    };
  },
  //el-tree-node__content
  computed: {
    disableContinue() {
      if (this.validTokenAvailable) {
        return false;
      }
      if (!this.validTokenAvailable && this.zenodoAccessToken !== "") {
        return false;
      }
      return true;
    },

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
        .post(`${this.$server_url}/utilities/openFileExplorer`, {
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
    showFilePreview() {
      this.showFilePreviewSection = !this.showFilePreviewSection;
    },
    handleCloseDrawer() {
      this.fileTitle = "";
      this.PreviewNewlyCreatedLicenseFile = false;
      this.PreviewNewlyCreatedMetadataFile = false;
      this.PreviewNewlyCreatedCitationFile = false;
    },
    async handleOpenDrawer(title) {
      if (title == "LICENSE") {
        title +=
          " (This preview may not be completely representative of the final license)";
      }

      this.fileTitle = title;
    },
    async handleNodeClick(data) {
      if (!data.isDir) {
        if (data.label == "LICENSE") {
          this.PreviewNewlyCreatedLicenseFile = true;
        } else if (data.label == "codemeta.json") {
          this.PreviewNewlyCreatedMetadataFile = true;
        } else if (data.label == "citation.cff") {
          this.PreviewNewlyCreatedCitationFile = true;
        } else if (!data.isDir) {
          await this.openFileExplorer(data.fullPath);
        }

        let title = data.label;
        this.handleOpenDrawer(title);
      }
    },
    getAllFilesFromFolder(dir) {
      let filesystem = require("fs");
      function dfs(dir) {
        let results = [];
        filesystem.readdirSync(dir).forEach(function (file) {
          let newObj = {};
          let filefullname = path.join(dir, file);
          let stat = filesystem.statSync(filefullname);
          if (stat && stat.isDirectory()) {
            newObj.label = file;
            newObj.isDir = true;
            newObj.children = dfs(filefullname);
            newObj.fullPath = filefullname;
          } else {
            newObj.label = file;
            newObj.isDir = false;
            newObj.fullPath = filefullname;
          }
          results.push(newObj);
        });
        return results;
      }
      let root = { label: dir, children: dfs(dir), fullPath: dir, isDir: true };
      this.fileData.push(root);
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
          let value = this.jsonToTableDataRecursive(
            jsonObject[property],
            newId,
            property
          );
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
      } else if (
        jsonObject &&
        Array.isArray(jsonObject) &&
        jsonObject.length != 0
      ) {
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

          let value = this.jsonToTableDataRecursive(
            jsonObject[i],
            newId,
            newName
          );

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
      console.log(status);
      if (status === "connected") {
        this.validTokenAvailable = true;
      }
      // this.uploadToZenodo(); console.log(this.workflow.licenseText)
    },
  },
  async mounted() {
    this.dataset = await this.datasetStore.getCurrentDataset();
    this.workflow = this.dataset.workflows[this.workflowID];

    let spinner = this.createLoading();
    this.tableData = await this.createCodeMetadataFile();
    this.citationData = await this.createCitationFile();
    this.getAllFilesFromFolder(this.dataset.data.Code.folderPath);
    this.tableData = this.jsonToTableDataRecursive(this.tableData, 1, "ROOT");

    this.citationData = this.jsonToTableDataRecursive(
      this.citationData,
      1,
      "ROOT"
    );
    console.log(this.workflow.licenseText);
    if (this.workflow.licenseText) {
      // await this.createLicenseFile();
      this.licenseData = this.workflow.licenseText;
    }
    spinner.close();

    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(6);

    this.workflow.currentRoute = this.$route.path;

    const validZenodoConnection = await this.tokens.verifyZenodoConnection();

    if (validZenodoConnection) {
      this.validTokenAvailable = true;
      this.ready = true;
    } else {
      this.validTokenAvailable = false;
      this.ready = true;
    }
  },
};
</script>
