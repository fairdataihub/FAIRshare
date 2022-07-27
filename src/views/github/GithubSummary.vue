<template>
  <div class="flex h-full w-full max-w-screen-xl flex-col items-center justify-center p-3 pr-5">
    <div class="flex h-full w-full flex-col">
      <h1 class="pb-1 text-left text-lg font-medium">Let's look into the future</h1>

      <el-divider class="my-2"> </el-divider>

      <div>
        <p class="my-2">
          We will be adding some files to your GitHub repository. A preview of what your GitHub
          repository will look like after is shown below (files that will be added by FAIRshare are
          highlighted in orange):
        </p>
        <div class="overflow-auto" :class="{ 'h-[200px]': finishedLoading }">
          <transition name="fade" mode="out-in" appear>
            <el-tree-v2 v-if="!showSpinner" :data="fileData" :props="defaultProps">
              <template #default="{ node, data }">
                <el-icon v-if="!node.isLeaf"><folder-icon /></el-icon>
                <el-icon v-if="node.isLeaf"><document-icon /></el-icon>
                <div
                  class="inline-flex items-center"
                  :class="
                    (node.label == 'codemeta.json' && workflow.generateCodeMeta) ||
                    (node.label == 'CITATION.cff' && workflow.generateCodeMeta) ||
                    node.label == '.zenodo.json' ||
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
                      node.label == '.zenodo.json' ||
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

            <div v-if="PreviewNewlyCreatedZenodoFile" class="pb-20">
              <el-table
                :data="zenodoData"
                style="width: 100%"
                row-key="id"
                border
                default-expand-all
              >
                <el-table-column prop="Name" label="Name" />
                <el-table-column prop="Value" label="Value" class="break-normal" />
              </el-table>
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
import dayjs from "dayjs";

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
      fileData: [],
      tree: [],
      fileTitle: "",
      PreviewNewlyCreatedLicenseFile: false,
      PreviewNewlyCreatedCodeMetaFile: false,
      PreviewNewlyCreatedCitationFile: false,
      PreviewNewlyCreatedZenodoFile: false,
      licenseData: "",
      tableData: [],
      tableDataRecord: [],
      zenodoData: [],
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

    async createZenodoJsonFile() {
      const zenodoMetadata = this.workflow.destination.zenodo.questions;
      let metadata = {};

      metadata.upload_type = "software";

      if ("title" in zenodoMetadata && zenodoMetadata.title != "") {
        metadata.title = zenodoMetadata.title;
      }
      if ("publicationDate" in zenodoMetadata && zenodoMetadata.publicationDate != "") {
        metadata.publication_date = zenodoMetadata.publicationDate;
      }

      if ("authors" in zenodoMetadata) {
        metadata.creators = [];
        zenodoMetadata.authors.forEach((author) => {
          const creatorObject = {};

          creatorObject.name = author.name;
          creatorObject.affiliation = author.affiliation;

          if (author.orcid !== "") {
            creatorObject.orcid = author.orcid;
          }

          metadata.creators.push(creatorObject);
        });
      }

      if ("description" in zenodoMetadata && zenodoMetadata.description != "") {
        metadata.description = zenodoMetadata.description;
      }
      if ("license" in zenodoMetadata) {
        if ("accessRight" in zenodoMetadata.license) {
          metadata.access_right = zenodoMetadata.license.accessRight;
        }
        if ("licenseName" in zenodoMetadata.license) {
          metadata.license = zenodoMetadata.license.licenseName;
        }
      }

      if ("keywords" in zenodoMetadata) {
        if (zenodoMetadata.keywords.length > 0) {
          metadata.keywords = [];
          zenodoMetadata.keywords.forEach((keyword) => {
            metadata.keywords.push(keyword.keyword);
          });
        }
      }

      if ("version" in zenodoMetadata && zenodoMetadata.version !== "") {
        metadata.version = zenodoMetadata.version;
      }

      if ("language" in zenodoMetadata && zenodoMetadata.language !== "") {
        metadata.language = zenodoMetadata.language;
      }

      if ("additionalNotes" in zenodoMetadata && zenodoMetadata.additionalNotes != "") {
        metadata.notes = zenodoMetadata.additionalNotes;
      }

      if ("relatedIdentifiers" in zenodoMetadata) {
        if (zenodoMetadata.relatedIdentifiers.length > 0) {
          metadata.related_identifiers = [];
          zenodoMetadata.relatedIdentifiers.forEach((relatedIdentifier) => {
            metadata.related_identifiers.push({
              relation: relatedIdentifier.relationship,
              identifier: relatedIdentifier.identifier,
              resource_type: relatedIdentifier.resourceType,
            });
          });
        }
      }

      if ("contributors" in zenodoMetadata) {
        if (zenodoMetadata.contributors.length > 0) {
          metadata.contributors = [];
          zenodoMetadata.contributors.forEach((contributor) => {
            const contributorObject = {};

            contributorObject.name = contributor.name;
            contributorObject.affiliation = contributor.affiliation;
            contributorObject.type = contributor.contributorType;

            if (contributor.orcid !== "") {
              contributorObject.orcid = contributor.orcid;
            }

            metadata.contributors.push(contributorObject);
          });
        }
      }

      if ("references" in zenodoMetadata) {
        if (zenodoMetadata.references.length > 0) {
          metadata.references = [];
          zenodoMetadata.references.forEach((reference) => {
            metadata.references.push(reference.reference);
          });
        }
      }

      if ("journal" in zenodoMetadata) {
        if ("title" in zenodoMetadata.journal && zenodoMetadata.journal.title !== "") {
          metadata.journal_title = zenodoMetadata.journal.title;
        }
        if ("volume" in zenodoMetadata.journal && zenodoMetadata.journal.volume !== "") {
          metadata.journal_volume = zenodoMetadata.journal.volume;
        }
        if ("issue" in zenodoMetadata.journal && zenodoMetadata.journal.issue !== "") {
          metadata.journal_issue = zenodoMetadata.journal.issue;
        }
        if ("pages" in zenodoMetadata.journal && zenodoMetadata.journal.pages !== "") {
          metadata.journal_pages = zenodoMetadata.journal.pages;
        }
      }

      if ("conference" in zenodoMetadata) {
        if ("title" in zenodoMetadata.conference && zenodoMetadata.conference.title !== "") {
          metadata.conference_title = zenodoMetadata.conference.title;
        }
        if ("acronym" in zenodoMetadata.conference && zenodoMetadata.conference.acronym !== "") {
          metadata.conference_acronym = zenodoMetadata.conference.acronym;
        }

        if ("dates" in zenodoMetadata.conference) {
          if (zenodoMetadata.conference.dates.length === 2) {
            metadata.conference_dates =
              dayjs(zenodoMetadata.conference.dates[0]).format("MMMM D, YYYY") +
              " - " +
              dayjs(zenodoMetadata.conference.dates[1]).format("MMMM D, YYYY");
          }
        }

        if ("place" in zenodoMetadata.conference && zenodoMetadata.conference.place !== "") {
          metadata.conference_place = zenodoMetadata.conference.place;
        }
        if ("url" in zenodoMetadata.conference && zenodoMetadata.conference.url !== "") {
          metadata.conference_url = zenodoMetadata.conference.url;
        }
        if ("session" in zenodoMetadata.conference && zenodoMetadata.conference.session !== "") {
          metadata.conference_session = zenodoMetadata.conference.session;
        }
        if ("part" in zenodoMetadata.conference && zenodoMetadata.conference.part !== "") {
          metadata.conference_session_part = zenodoMetadata.conference.part;
        }
      }

      if ("bookReportChapter" in zenodoMetadata) {
        if (
          "publisher" in zenodoMetadata.bookReportChapter &&
          zenodoMetadata.bookReportChapter.publisher !== ""
        ) {
          metadata.imprint_publisher = zenodoMetadata.bookReportChapter.publisher;
        }
        if (
          "isbn" in zenodoMetadata.bookReportChapter &&
          zenodoMetadata.bookReportChapter.isbn !== ""
        ) {
          metadata.imprint_isbn = zenodoMetadata.bookReportChapter.isbn;
        }
        if (
          "place" in zenodoMetadata.bookReportChapter &&
          zenodoMetadata.bookReportChapter.place !== ""
        ) {
          metadata.imprint_place = zenodoMetadata.bookReportChapter.place;
        }
        if (
          "title" in zenodoMetadata.bookReportChapter &&
          zenodoMetadata.bookReportChapter.title !== ""
        ) {
          metadata.partof_title = zenodoMetadata.bookReportChapter.title;
        }
        if (
          "pages" in zenodoMetadata.bookReportChapter &&
          zenodoMetadata.bookReportChapter.pages !== ""
        ) {
          metadata.partof_pages = zenodoMetadata.bookReportChapter.pages;
        }
      }

      if ("thesis" in zenodoMetadata) {
        if (
          "awardingUniversity" in zenodoMetadata.thesis &&
          zenodoMetadata.thesis.awardingUniversity !== ""
        ) {
          metadata.thesis_university = zenodoMetadata.thesis.awardingUniversity;
        }

        if (
          "thesis_supervisors" in zenodoMetadata.thesis &&
          zenodoMetadata.thesis.thesis_supervisors.length > 0
        ) {
          metadata.thesis_supervisors = [];
          zenodoMetadata.thesis.supervisors.forEach((supervisor) => {
            metadata.thesis_supervisors.push({
              name: supervisor.name,
              affiliation: supervisor.affiliation,
              orcid: supervisor.orcid,
            });
          });
        }
      }

      if ("subjects" in zenodoMetadata && zenodoMetadata.subjects.length > 0) {
        metadata.subjects = [];
        zenodoMetadata.subjects.forEach((subject) => {
          metadata.subjects.push({
            term: subject.term,
            identifier: subject.identifier,
            scheme: "url",
          });
        });
      }

      return metadata;
    },

    async handleNodeClick(data, action) {
      if (
        (data.label === "LICENSE" && this.workflow.generateLicense) ||
        data.label === "codemeta.json" ||
        data.label === "CITATION.cff" ||
        data.label === ".zenodo.json"
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
        } else if (data.label === ".zenodo.json") {
          if (action === "view") {
            this.PreviewNewlyCreatedZenodoFile = true;
          }
          if (action === "download") {
            this.exportToJson(this.zenodoData, ".zenodo.json");
          }
        }
        let title = data.label;
        this.handleOpenDrawer(title);
      } else {
        const githubURL = `https://github.com/${this.selectedRepo}/${data.type}/${this.currentBranch}/${data.label}`;
        window.ipcRenderer.send("open-link-in-browser", githubURL);
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
      this.PreviewNewlyCreatedZenodoFile = false;
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
        this.fileData = JSON.parse(response);

        // check if label exists in fileData

        if (!this.fileData.some((el) => el.label === "codemeta.json")) {
          if (this.workflow.generateCodeMeta) {
            let newObj = {};
            newObj.label = "codemeta.json";
            newObj.isDir = false;

            this.fileData.push(newObj);
          }
        }

        if (!this.fileData.some((el) => el.label === "CITATION.cff")) {
          if (this.workflow.generateCodeMeta) {
            let newObj = {};
            newObj.label = "CITATION.cff";
            newObj.isDir = false;

            this.fileData.push(newObj);
          }
        }

        if (!this.fileData.some((el) => el.label === ".zenodo.json")) {
          let newObj = {};
          newObj.label = ".zenodo.json";
          newObj.isDir = false;

          this.fileData.push(newObj);
        }

        if (!this.fileData.some((el) => el.label === "LICENSE")) {
          if (this.workflow.generateLicense) {
            let newObj = {};
            newObj.label = "LICENSE";
            newObj.isDir = false;

            this.fileData.push(newObj);
          }
        }

        console.log(this.fileData);
      } else {
        this.$message({
          message: "Could not get the contents of the repository",
          type: "error",
        });
      }
    },

    async showFilePreview() {
      this.fileData = [];
      this.showSpinner = true;

      await this.showGithubRepoContents();
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

    this.zenodoData = await this.createZenodoJsonFile();
    this.zenodoData = this.jsonToTableDataRecursive(this.zenodoData, 1, "ROOT");

    if (this.workflow.generateLicense) {
      this.licenseData = this.workflow.licenseText;
    }

    this.workflow.currentRoute = this.$route.path;
  },
};
</script>
