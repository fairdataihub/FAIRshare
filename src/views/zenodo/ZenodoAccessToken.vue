<template>
  <div
    class="flex flex-col items-center justify-center w-full h-full max-w-screen-xl p-3 pr-5"
  >
    <div class="flex flex-col w-full h-full">
      <span class="text-lg font-medium text-left">
        Zenodo connection details
      </span>
      <span class="text-left">
        We will use this to upload and edit your dataset on your Zenodo account.
      </span>

      <el-divider class="my-4"> </el-divider>

      <div v-if="ready">
        <p v-if="validTokenAvailable" class="w-full my-10 text-center">
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

      <div class="flex flex-row justify-center w-full py-2 space-x-4">
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
          <p class="my-5 text=lg">
            A list of all the file that we are going to upload to Zenodo is
            shown below. You can click on any of them to view the content or
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
              <div
                v-if="
                  PreviewNewlyCreatedMetadataFile
                "
              >
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

              <div
                v-if="
                  PreviewNewlyCreatedCitationFile
                "
              >
                <el-table
                  :data="citationData"
                  style="width: 100%"
                  row-key="id"
                  border
                  default-expand-all
                >
                  <el-table-column prop="Name" label="Name" />
                  <el-table-column prop="Value" label="Value" />
                </el-table>
              </div>

              <div
                v-if="PreviewNewlyCreatedLicenseFile"
              >
                <el-table
                  :data="licenseData"
                  style="width: 100%"
                  row-key="id"
                  border
                  default-expand-all
                >
                  <el-table-column prop="Name" label="Name" />
                  <el-table-column prop="Value" label="Value" />
                </el-table>
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
import axios from "axios";
import ConnectZenodo from "@/components/serviceIntegration/ConnectZenodo";
import path from 'path';
import { useDatasetsStore } from "@/store/datasets";
import { useTokenStore } from "@/store/access.js";
import { ElLoading } from "element-plus";
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
      licenseData: [{"license content":""}],
      tableData: [],
      citationData: [],
      fileData: [],
      defaultProps: {
        children: "children",
        label: "label",
      },
      fileTitle: "",
      showFilePreviewSection: true,
      PreviewNewlyCreatedLicenseFile: false,
      PreviewNewlyCreatedMetadataFile: false,
      PreviewNewlyCreatedCitationFile: false,
      drawerModel: true
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

    anyfilePreview(){
      if(this.PreviewNewlyCreatedMetadataFile || this.PreviewNewlyCreatedLicenseFile || this.PreviewNewlyCreatedCitationFile){
        return true
      } else {
        return false
      }
    }
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
          return JSON.parse(response.data)
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
          return JSON.parse(response.data)
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
      const response = await axios
        .post(`${this.$server_url}/utilities/openFileExplorer`, {
          folder_path: path
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
      this.fileTitle = title;
    },
    async handleNodeClick(data) {
      if (!data.isDir) {
        if (data.label == "LICENSE") {
          this.PreviewNewlyCreatedLicenseFile = true;
        } else if (data.label == "codemeta.json") {
          this.PreviewNewlyCreatedMetadataFile = true;
        }else if (data.label == "citation.cff") {
          this.PreviewNewlyCreatedCitationFile = true;
        } else if (!data.isDir){
          await this.openFileExplorer(data.fullPath)
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
          if (i == 0) {
            newName = String(i + 1) + "st" + " in " + parentName;
          } else if (i == 1) {
            newName = String(i + 1) + "nd" + " in " + parentName;
          } else if (i == 2) {
            newName = String(i + 1) + "rd" + " in " + parentName;
          } else {
            newName = String(i + 1) + "th" + " in " + parentName;
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
    this.tableData = await this.createCodeMetadataFile()
    this.citationData = await this.createCitationFile()
    this.getAllFilesFromFolder(this.dataset.data.Code.folderPath);
    this.tableData = this.jsonToTableDataRecursive(
      this.tableData,
      1,
      "ROOT"
    );

    this.citationData = this.jsonToTableDataRecursive(
      this.citationData,
      1,
      "ROOT"
    );
    if(this.workflow.licenseText){
      await this.createLicenseFile()
      this.licenseData[0]["license content"] = this.workflow.licenseText
    }
    spinner.close();

    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(6);

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

<style lang="postcss" scoped></style>
