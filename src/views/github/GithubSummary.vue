<template>
  <div class="flex h-full w-full max-w-screen-xl flex-col items-center justify-center p-3 pr-5">
    <div class="flex h-full w-full flex-col">
      <h1 class="pb-1 text-left text-lg font-medium">Let's look into the future</h1>

      <line-divider class="" />

      <div>
        <p class="mb-2">
          We will be adding some files to your GitHub repository. A preview of what your GitHub
          repository will look like after is shown below (files that will be added by FAIRshare are
          highlighted in orange):
        </p>
        <div class="overflow-auto" :class="{ 'h-[200px]': finishedLoading }">
          <transition name="fade" mode="out-in" appear>
            <el-tree-v2 v-if="!showSpinner" :data="githubFileData" :props="defaultProps">
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
                  <span> {{ node.label }} </span>
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
                animationLink="https://assets3.lottiefiles.com/private_files/lf30_t26law.json"
                :width="200"
                :height="200"
              />
            </div>
          </transition>
        </div>

        <line-divider class="" />

        <p class="mb-2">
          Your uploaded dataset on Zenodo will look like this (files that will be added by FAIRshare
          to your final upload are highlighted in orange):
        </p>

        <div class="overflow-auto" :class="{ 'h-[200px]': finishedLoading }">
          <transition name="fade" mode="out-in" appear>
            <el-tree-v2 v-if="!showSpinner" :data="zenodoFileData" :props="defaultProps">
              <template #default="{ node, data }">
                <el-icon v-if="!node.isLeaf"><folder-icon /></el-icon>
                <el-icon v-if="node.isLeaf"><document-icon /></el-icon>
                <div
                  class="inline-flex items-center"
                  :class="
                    (node.label == 'codemeta.json' && workflow.generateCodeMeta) ||
                    (node.label == 'CITATION.cff' && workflow.generateCodeMeta) ||
                    (node.label == 'LICENSE' && workflow.generateLicense) ||
                    data.customAddition
                      ? 'text-secondary-500'
                      : ''
                  "
                >
                  <span> {{ node.label }} </span>
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
                animationLink="https://assets3.lottiefiles.com/private_files/lf30_t26law.json"
                :width="200"
                :height="200"
              />
            </div>
          </transition>
        </div>

        <el-drawer
          v-model="drawerModel"
          :title="fileTitle"
          direction="rtl"
          size="60%"
          :before-close="handleCloseDrawer"
          :lock-scroll="false"
        >
          <el-scrollbar style="height: calc(100vh - 45px)">
            <div v-if="PreviewNewlyCreatedCodeMetaFile" class="pb-20">
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

      <transition name="fade" mode="out-in" appear>
        <div class="flex w-full flex-row justify-center space-x-4 py-2" v-if="finishedLoading">
          <router-link
            :to="`/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/github/chooseUpload`"
            class=""
          >
            <button class="primary-plain-button">
              <el-icon><d-arrow-left /></el-icon> Back
            </button>
          </router-link>

          <button class="primary-button" @click="uploadToZenodo">
            Start upload
            <el-icon> <d-arrow-right /> </el-icon>
          </button>
        </div>
      </transition>
    </div>
    <app-docs-link url="curate-and-share/github-upload-summary" position="bottom-4" />
  </div>
</template>

<script>
import { useDatasetsStore } from "@/store/datasets";
import { useTokenStore } from "@/store/access.js";

import { marked } from "marked";
import DOMPurify from "dompurify";
import axios from "axios";
import fs from "fs-extra";
import path from "path";
import { dialog } from "@electron/remote";

import rippleLottieJSON from "@/assets/lotties/rippleLottie.json";

export default {
  name: "GithubSummary",
  components: {},
  data() {
    return {
      datasetStore: useDatasetsStore(),
      tokens: useTokenStore(),
      dataset: {},
      folderPath: "",
      workflowID: this.$route.params.workflowID,
      workflow: {},
      GithubAccessToken: "",
      errorMessage: "",
      selectedRepo: "",
      currentBranch: "",
      rippleLottieJSON,
      defaultProps: {
        value: "id",
        children: "children",
        label: "label",
      },
      githubFileData: [],
      zenodoFileData: [],
      tree: [],
      fileTitle: "",
      PreviewNewlyCreatedLicenseFile: false,
      PreviewNewlyCreatedCodeMetaFile: false,
      PreviewNewlyCreatedCitationFile: false,
      licenseData: "",
      tableData: [],
      tableDataRecord: [],
      citationData: [],
      citationDataRecord: [],
      fullNameDictionary: {},
      ownerDictionary: {},
      nameDictionary: {},
      branchDictionary: {},
      drawerModel: false,
      showSpinner: false,
      finishedLoading: false,
      interval: null,
    };
  },
  computed: {
    compiledLicense() {
      const markdownToHTML = marked(this.licenseData);
      return DOMPurify.sanitize(markdownToHTML);
    },
  },
  methods: {
    exportToJson(obj, file_name) {
      /* eslint-disable */
      let filename = file_name;
      let contentType = "application/json;charset=utf-8;";
      if (window.navigator && window.navigator.msSaveOrOpenBlob) {
        var blob = new Blob([decodeURIComponent(encodeURI(JSON.stringify(obj)))], {
          type: contentType,
        });
        navigator.msSaveOrOpenBlob(blob, filename);
      } else {
        dialog
          .showSaveDialog({
            title: `Save ${file_name}`,
            defaultPath: path.join(this.$downloads_path, file_name),
          })
          .then((result) => {
            const githubFileData = typeof obj === "object" ? JSON.stringify(obj) : obj;

            fs.writeFile(result.filePath, githubFileData, (err) => {
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
                this.openFileExplorer(path.join(this.$downloads_path, file_name));
              }
            });
          })
          .catch((err) => {
            console.log(err);
          });
      }
    },

    openWebsite(url) {
      window.ipcRenderer.send("open-link-in-browser", url);
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
          console.log(error);
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

    async openFileExplorer(path) {
      const response = await axios
        .post(`${this.$server_url}/utilities/openfileexplorer`, {
          file_path: path,
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

    async handleNodeClick(data, action) {
      if (
        (data.label === "LICENSE" && this.workflow.generateLicense) ||
        data.label === "codemeta.json" ||
        data.label === "CITATION.cff"
      ) {
        if (action === "view") {
          this.drawerModel = true;
        }
        if (data.label === "LICENSE" && this.workflow.generateLicense) {
          if (action === "view") {
            this.PreviewNewlyCreatedLicenseFile = true;
          }
          if (action === "download") {
            this.exportToJson({ licenseData: this.licenseData }, "LICENSE");
          }
        } else if (data.label === "codemeta.json") {
          if (action === "view") {
            this.PreviewNewlyCreatedCodeMetaFile = true;
          }
          if (action === "download") {
            this.exportToJson(this.tableDataRecord, "codemeta.json");
          }
        } else if (data.label === "CITATION.cff") {
          if (action === "view") {
            this.PreviewNewlyCreatedCitationFile = true;
          }
          if (action === "download") {
            this.exportToJson(this.citationDataRecord, "CITATION.cff");
          }
        }
        let title = data.label;
        this.handleOpenDrawer(title);
      } else if (!data.isDir) {
        if (data.location === "local") {
          await this.openFileExplorer(data.fullPath);
        } else {
          const githubURL = `https://github.com/${this.selectedRepo}/${
            data.type ? data.type : "blob"
          }/${this.currentBranch}/${data.label}`;
          window.ipcRenderer.send("open-link-in-browser", githubURL);
        }
      }
    },

    async handleOpenDrawer(title) {
      if (title == "LICENSE") {
        title += " (This preview may not be completely representative of the final license)";
      }

      this.fileTitle = title;
    },

    handleCloseDrawer() {
      this.fileTitle = "";
      this.PreviewNewlyCreatedLicenseFile = false;
      this.PreviewNewlyCreatedCodeMetaFile = false;
      this.PreviewNewlyCreatedCitationFile = false;

      this.drawerModel = false;
    },

    async uploadToZenodo() {
      const routerPath = `/datasets/${this.datasetID}/${this.workflowID}/github/upload`;

      this.$router.push({ path: routerPath });
    },

    async showGithubRepoContents() {
      const tokenObject = await this.tokens.getToken("github");
      const GithubAccessToken = tokenObject.token;

      let response = "";

      const fullRepoName = this.selectedRepo.split("/");

      response = await axios
        .get(`${process.env.VUE_APP_GITHUB_SERVER_URL}/repos/${this.selectedRepo}`, {
          params: {},
          headers: {
            Accept: "application/vnd.github.v3+json",
            Authorization: `Bearer ${GithubAccessToken}`,
          },
        })
        .then((res) => {
          return res.data;
        })
        .catch((error) => {
          console.error(error);
          return "ERROR";
        });

      if (response !== "ERROR") {
        this.currentBranch = response.default_branch;
      }

      response = await axios
        .get(`${this.$server_url}/github/repo/tree`, {
          params: {
            access_token: GithubAccessToken,
            owner: fullRepoName[0],
            repo: fullRepoName[1],
          },
        })
        .then((response) => {
          return response.data;
        })
        .catch((error) => {
          console.error(error);
          return "ERROR";
        });

      if (response !== "ERROR") {
        this.githubFileData = JSON.parse(response);

        // check if label exists in githubFileData

        if (!this.githubFileData.some((el) => el.label === "codemeta.json")) {
          if (this.workflow.generateCodeMeta) {
            let newObj = {};
            newObj.label = "codemeta.json";
            newObj.isDir = false;

            this.githubFileData.push(newObj);
          }
        }

        if (!this.githubFileData.some((el) => el.label === "CITATION.cff")) {
          if (this.workflow.generateCodeMeta) {
            let newObj = {};
            newObj.label = "CITATION.cff";
            newObj.isDir = false;

            this.githubFileData.push(newObj);
          }
        }

        if (!this.githubFileData.some((el) => el.label === "LICENSE")) {
          if (this.workflow.generateLicense) {
            let newObj = {};
            newObj.label = "LICENSE";
            newObj.isDir = false;

            this.githubFileData.push(newObj);
          }
        }
      } else {
        this.$message({
          message: "Could not get the contents of the repository",
          type: "error",
        });
      }
    },

    async showFilePreview() {
      this.githubFileData = [];
      this.showSpinner = true;

      await this.showGithubRepoContents();

      this.zenodoFileData = JSON.parse(JSON.stringify(this.githubFileData));

      // add additional files to zenodoFileData

      if (
        "addAdditionalFiles" in this.workflow &&
        this.workflow.addAdditionalFiles &&
        "additionalFilesLocation" in this.workflow
      ) {
        if (this.workflow.additionalFilesLocation === "local" && "localFileList" in this.workflow) {
          for (const el of this.workflow.localFileList) {
            let newObj = {};
            newObj.label = path.basename(el);
            newObj.isDir = false;
            newObj.customAddition = true;
            newObj.location = "local";
            newObj.fullPath = el;

            this.zenodoFileData.push(newObj);
          }
        } else if (
          this.workflow.additionalFilesLocation === "github" &&
          `addedReleaseAssets` in this.workflow
        ) {
          for (const el of this.workflow.addedReleaseAssets) {
            let newObj = {};
            newObj.label = path.basename(el);
            newObj.isDir = false;
            newObj.customAddition = true;
            newObj.location = "github";

            this.zenodoFileData.push(newObj);
          }
        }
      }

      this.showSpinner = false;
      this.finishedLoading = true;
    },
  },

  async mounted() {
    this.dataset = await this.datasetStore.getCurrentDataset();
    this.workflow = this.dataset.workflows[this.workflowID];

    this.selectedRepo = this.workflow.github.repo;

    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(6);

    const tokenObject = await this.tokens.getToken("github");
    this.GithubAccessToken = tokenObject.token;

    this.showFilePreview();

    this.tableDataRecord = [];
    this.citationDataRecord = [];
    this.tableData = await this.createCodeMetadataFile();
    this.tableDataRecord = Object.assign({}, this.tableData);
    this.tableData = this.jsonToTableDataRecursive(this.tableData, 1, "ROOT");

    this.citationData = await this.createCitationFile();
    this.citationDataRecord = Object.assign({}, this.citationData);
    this.citationData = this.jsonToTableDataRecursive(this.citationData, 1, "ROOT");

    if (this.workflow.generateLicense) {
      this.licenseData = this.workflow.licenseText;
    }

    this.workflow.currentRoute = this.$route.path;
  },
};
</script>
