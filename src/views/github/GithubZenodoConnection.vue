<template>
  <div
    class="flex h-full w-full max-w-screen-xl flex-col items-center justify-center p-3 pr-5"
  >
    <div class="flex h-full w-full flex-col">
      <h1 class="pb-1 text-left text-lg font-medium">
        Connect your GitHub account to Zenodo
      </h1>
      <h2 class="text-left">
        Let's see if you GitHub account is already connected to Zenodo.
      </h2>

      <el-divider class="my-4"> </el-divider>

      <div>
        <div v-if="validZenodoHookTokenFound" class="my-10">
          <div class="flex items-center justify-center">
            <p class="my-3 mx-2 font-medium text-emerald-400">
              We found a Zenodo webhook on your GitHub repository.
            </p>
            <Vue3Lottie
              animationLink="https://assets2.lottiefiles.com/packages/lf20_xvusaxau.json"
              :width="30"
              :height="30"
              :loop="1"
            />
          </div>
          <p class="my-3 w-full text-center">
            Your account has been setup for Zenodo integration. Let's move on to
            the next step.
          </p>
        </div>
        <!-- show how to connect to zenodo if no hook is found -->
        <div v-else class="flex w-full flex-col">
          <div class="mb-5 flex items-center justify-center">
            <h3 class="mx-2 font-normal text-secondary-600">
              We are not seeing any Zenodo connections already setup with
              GitHub.
            </h3>
            <Vue3Lottie
              animationLink="https://assets1.lottiefiles.com/private_files/lf30_lkauxe8i.json"
              :width="45"
              :height="45"
            />
          </div>

          <div>
            <p class="mb-2">
              To connect your GitHub account with Zenodo there are a few steps
              you need to do from your side.
            </p>
            <ul class="ml-2 list-inside list-disc">
              <li>
                Login to Zenodo and go to the GitHub connections in your profile
                settings. Alternatively, you can also click the button below to
                take you to the appropriate page.
              </li>

              <div class="my-2 flex w-full items-center justify-center">
                <button
                  class="secondary-plain-button my-1"
                  @click="openWebsite"
                >
                  Connect GitHub to Zenodo
                </button>
              </div>

              <li>
                Authenticate with GitHub and wait for your list of repositories
                to show up.
              </li>

              <li>
                Toggle the switch for the
                <span class="font-bold">
                  {{ selectedRepo }}
                </span>
                repository to the 'ON' position.
              </li>

              <li>Wait for Fairshare to notice the change.</li>
            </ul>
            <p class="mt-2">
              You will only need to do this once. For any future GitHub
              repositories, Fair Share will automatically add the relevant
              connections for you.
            </p>
          </div>
        </div>
      </div>

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
          v-if="validZenodoHookTokenFound"
        >
          <el-icon><checked-icon /></el-icon>
          View files ready for upload
        </button>

        <button
          class="primary-button"
          @click="uploadToZenodo"
          v-if="validZenodoHookTokenFound"
        >
          Start upload
          <el-icon> <d-arrow-right /> </el-icon>
        </button>
      </div>
      <transition appear mode="out-in" name="fade">
        <div v-if="showFilePreviewSection" class="py-5">
          <line-divider />
          <p class="text=lg my-5">
            We will be adding some files to your GitHub repository. A preview of
            what it will look like after is shown below.
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
                  node.label == 'CITATION.cff' ||
                  node.label == '.zenodo.json' ||
                  (node.label == 'LICENSE' && workflow.generateLicense)
                    ? 'text-secondary-500'
                    : ''
                "
                >{{ node.label }}</span
              >
            </template>
          </el-tree>

          <el-drawer
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

              <div v-if="PreviewNewlyCreatedZenodoFile" class="pb-20">
                <el-table
                  :data="zenodoData"
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
    <transition name="fade" mode="out-in" appear>
      <div class="fixed bottom-2 right-3" v-show="showSpinner">
        <Vue3Lottie :animationData="$helix_spinner" :width="80" :height="80" />
      </div>
    </transition>
  </div>
</template>

<script>
import { useDatasetsStore } from "@/store/datasets";
import { useTokenStore } from "@/store/access.js";

import { marked } from "marked";
import DOMPurify from "dompurify";
import axios from "axios";
import dayjs from "dayjs";
import { ElLoading, ElNotification } from "element-plus";

import rippleLottieJSON from "@/assets/lotties/rippleLottie.json";

export default {
  name: "GithubZenodoConnection",
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
      validZenodoHookTokenFound: false,
      errorMessage: "",
      showFilePreviewSection: "",
      zenodoAccessToken: "",
      selectedRepo: "",
      currentBranch: "",
      rippleLottieJSON,
      defaultProps: {
        children: "children",
        label: "label",
      },
      fileData: [],
      tree: [],
      fileTitle: "",
      PreviewNewlyCreatedLicenseFile: false,
      PreviewNewlyCreatedMetadataFile: false,
      PreviewNewlyCreatedCitationFile: false,
      PreviewNewlyCreatedZenodoFile: false,
      licenseData: "",
      tableData: [],
      zenodoData: [],
      citationData: [],
      fullNameDictionary: {},
      ownerDictionary: {},
      nameDictionary: {},
      branchDictionary: {},
      drawerModel: false,
      showSpinner: false,
    };
  },
  computed: {
    compiledLicense() {
      const markdownToHTML = marked(this.licenseData);
      return DOMPurify.sanitize(markdownToHTML);
    },
  },
  methods: {
    createLoading() {
      const loading = ElLoading.service({
        lock: true,
        text: "Reading GitHub repository...",
        background: "rgba(255, 255, 255, 0.97)",
      });
      return loading;
    },

    openWebsite() {
      const url = `${process.env.VUE_APP_ZENODO_URL}/account/settings/github`;
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
          let value = this.jsonToTableDataRecursive(
            jsonObject[property],
            newId,
            property
          );

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
      if (
        "publicationDate" in zenodoMetadata &&
        zenodoMetadata.publicationDate != ""
      ) {
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

      if (
        "additionalNotes" in zenodoMetadata &&
        zenodoMetadata.additionalNotes != ""
      ) {
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
        if (
          "title" in zenodoMetadata.journal &&
          zenodoMetadata.journal.title !== ""
        ) {
          metadata.journal_title = zenodoMetadata.journal.title;
        }
        if (
          "volume" in zenodoMetadata.journal &&
          zenodoMetadata.journal.volume !== ""
        ) {
          metadata.journal_volume = zenodoMetadata.journal.volume;
        }
        if (
          "issue" in zenodoMetadata.journal &&
          zenodoMetadata.journal.issue !== ""
        ) {
          metadata.journal_issue = zenodoMetadata.journal.issue;
        }
        if (
          "pages" in zenodoMetadata.journal &&
          zenodoMetadata.journal.pages !== ""
        ) {
          metadata.journal_pages = zenodoMetadata.journal.pages;
        }
      }

      if ("conference" in zenodoMetadata) {
        if (
          "title" in zenodoMetadata.conference &&
          zenodoMetadata.conference.title !== ""
        ) {
          metadata.conference_title = zenodoMetadata.conference.title;
        }
        if (
          "acronym" in zenodoMetadata.conference &&
          zenodoMetadata.conference.acronym !== ""
        ) {
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

        if (
          "place" in zenodoMetadata.conference &&
          zenodoMetadata.conference.place !== ""
        ) {
          metadata.conference_place = zenodoMetadata.conference.place;
        }
        if (
          "url" in zenodoMetadata.conference &&
          zenodoMetadata.conference.url !== ""
        ) {
          metadata.conference_url = zenodoMetadata.conference.url;
        }
        if (
          "session" in zenodoMetadata.conference &&
          zenodoMetadata.conference.session !== ""
        ) {
          metadata.conference_session = zenodoMetadata.conference.session;
        }
        if (
          "part" in zenodoMetadata.conference &&
          zenodoMetadata.conference.part !== ""
        ) {
          metadata.conference_session_part = zenodoMetadata.conference.part;
        }
      }

      if ("bookReportChapter" in zenodoMetadata) {
        if (
          "publisher" in zenodoMetadata.bookReportChapter &&
          zenodoMetadata.bookReportChapter.publisher !== ""
        ) {
          metadata.imprint_publisher =
            zenodoMetadata.bookReportChapter.publisher;
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

    async handleNodeClick(data) {
      if (
        (data.label === "LICENSE" && this.workflow.generateLicense) ||
        data.label === "codemeta.json" ||
        data.label === "CITATION.cff" ||
        data.label === ".zenodo.json"
      ) {
        this.drawerModel = true;
        if (data.label === "LICENSE" && this.workflow.generateLicense) {
          this.PreviewNewlyCreatedLicenseFile = true;
        } else if (data.label === "codemeta.json") {
          this.PreviewNewlyCreatedMetadataFile = true;
        } else if (data.label === "CITATION.cff") {
          this.PreviewNewlyCreatedCitationFile = true;
        } else if (data.label === ".zenodo.json") {
          this.PreviewNewlyCreatedZenodoFile = true;
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
        title +=
          " (This preview may not be completely representative of the final license)";
      }

      this.fileTitle = title;
    },

    handleCloseDrawer() {
      this.fileTitle = "";
      this.PreviewNewlyCreatedLicenseFile = false;
      this.PreviewNewlyCreatedMetadataFile = false;
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
        .get(
          `${process.env.VUE_APP_GITHUB_SERVER_URL}/repos/${this.selectedRepo}`,
          {
            params: {},
            headers: {
              Accept: "application/vnd.github.v3+json",
              Authorization: `Bearer ${GithubAccessToken}`,
            },
          }
        )
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

        let newObj = {};

        if (!this.fileData.some((el) => el.label === "codemeta.json")) {
          newObj.label = "codemeta.json";
          newObj.isDir = false;

          this.fileData.push(newObj);
        }

        if (!this.fileData.some((el) => el.label === "CITATION.cff")) {
          newObj = {};
          newObj.label = "CITATION.cff";
          newObj.isDir = false;

          this.fileData.push(newObj);
        }

        if (!this.fileData.some((el) => el.label === ".zenodo.json")) {
          newObj = {};
          newObj.label = ".zenodo.json";
          newObj.isDir = false;

          this.fileData.push(newObj);
        }

        if (!this.fileData.some((el) => el.label === "LICENSE")) {
          if (this.workflow.generateLicense) {
            newObj = {};
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
      this.showFilePreviewSection = !this.showFilePreviewSection;

      if (this.showFilePreviewSection) {
        this.fileData = [];
        this.showSpinner = true;

        await this.showGithubRepoContents();
        this.showSpinner = false;
      }
    },

    async checkIfZenodoHookIsPresent() {
      const tokenObject = await this.tokens.getToken("github");
      const GithubAccessToken = tokenObject.token;
      // console.log(GithubAccessToken);

      let response = "";

      response = await axios
        .get(
          `${process.env.VUE_APP_GITHUB_SERVER_URL}/repos/${this.selectedRepo}/hooks`,
          {
            params: {
              per_page: 100,
            },
            headers: {
              Accept: "application/vnd.github.v3+json",
              Authorization: `Bearer ${GithubAccessToken}`,
            },
          }
        )
        .then((response) => {
          return response.data;
        })
        .catch((error) => {
          console.error(error);
          return "ERROR";
        });

      if (response !== "ERROR" && response.length > 0) {
        for (const webhook of response) {
          if (
            "config" in webhook &&
            "events" in webhook &&
            webhook.events.includes("release") &&
            "url" in webhook.config &&
            webhook.config.url.includes(
              `${process.env.VUE_APP_ZENODO_SERVER_URL}/hooks/receivers/github/events/?access_token=`
            )
          ) {
            return response;
          } else {
            return false;
          }
        }
      } else {
        return false;
      }
    },

    async createGithubZenodoWebhook(GithubZenodoConnectionToken) {
      const tokenObject = await this.tokens.getToken("github");
      const GithubAccessToken = tokenObject.token;

      let response = "";

      const data = JSON.stringify({
        name: "web",
        config: {
          url: `${process.env.VUE_APP_ZENODO_SERVER_URL}/hooks/receivers/github/events/?access_token=${GithubZenodoConnectionToken}`,
          content_type: "json",
          secret: "secret",
          insecure_ssl: 0,
        },
        events: ["release"],
        active: true,
      });

      const config = {
        method: "post",
        url: `${process.env.VUE_APP_GITHUB_SERVER_URL}/repos/${this.selectedRepo}/hooks`,
        headers: {
          Accept: "application/vnd.github.v3+json",
          Authorization: `Bearer ${GithubAccessToken}`,
          "Content-Type": "application/json",
        },
        data: data,
      };

      response = await axios(config)
        .then((response) => {
          console.log(response);
          if (response.status === 200 || response.status === 201) {
            return true;
          } else {
            return false;
          }
        })
        .catch((error) => {
          console.error(error);
          return "ERROR";
        });

      if (response !== "ERROR") {
        return response;
      } else {
        return false;
      }
    },
  },

  async mounted() {
    let spinner = this.createLoading();
    this.dataset = await this.datasetStore.getCurrentDataset();
    this.workflow = this.dataset.workflows[this.workflowID];

    this.selectedRepo = this.workflow.github.repo;

    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(6);

    const tokenObject = await this.tokens.getToken("github");
    this.GithubAccessToken = tokenObject.token;
    const GithubZenodoConnectionToken = tokenObject.zenodoHookToken;
    // const GithubZenodoConnectionToken = false;

    if (GithubZenodoConnectionToken) {
      const response = await this.checkIfZenodoHookIsPresent();

      if (response) {
        this.validZenodoHookTokenFound = true;
      } else {
        ElNotification({
          title: "Info",
          message: "Creating a Zenodo webhook for this repository.",
          type: "info",
        });

        const tokenCreated = await this.createGithubZenodoWebhook(
          GithubZenodoConnectionToken
        );

        if (tokenCreated) {
          ElNotification({
            title: "Success",
            message: "Created a zenodo webhook for this repo successfully.",
            type: "success",
          });

          setTimeout(() => {
            this.validZenodoHookTokenFound = true;
          }, 1000);
        } else {
          ElNotification({
            title: "Error",
            message:
              "Could not create the Zenodo webhook automatically. Please connect your Zenodo account to the GitHub repository manually.",
            type: "error",
            duration: 10000,
          });
        }
      }
      spinner.close();
    } else {
      let interval = setInterval(async () => {
        const response = await this.checkIfZenodoHookIsPresent();
        console.log(response);

        spinner.close();

        if (response) {
          if (response.length > 0) {
            for (const webhook of response) {
              if (
                "config" in webhook &&
                "events" in webhook &&
                webhook.events.includes("release") &&
                "url" in webhook.config &&
                webhook.config.url.includes(
                  `${process.env.VUE_APP_ZENODO_SERVER_URL}/hooks/receivers/github/events/?access_token=`
                )
              ) {
                const webhookConfigURL = webhook.config.url;
                const webhookConfigURLArray =
                  webhookConfigURL.split("access_token=");
                const webhookConfigURLToken = webhookConfigURLArray[1];

                if (webhookConfigURLToken) {
                  const newTokenObject = JSON.parse(
                    JSON.stringify(await this.tokens.getToken("github"))
                  );
                  newTokenObject.zenodoHookToken = webhookConfigURLToken;

                  await this.tokens.saveToken("github", newTokenObject);
                }
              }
            }
          }

          this.validZenodoHookTokenFound = true;

          clearInterval(interval);
        }
      }, 5000);
    }

    this.tableData = await this.createCodeMetadataFile();
    this.tableData = this.jsonToTableDataRecursive(this.tableData, 1, "ROOT");

    this.citationData = await this.createCitationFile();
    this.citationData = this.jsonToTableDataRecursive(
      this.citationData,
      1,
      "ROOT"
    );

    this.zenodoData = await this.createZenodoJsonFile();
    this.zenodoData = this.jsonToTableDataRecursive(this.zenodoData, 1, "ROOT");

    if (this.workflow.generateLicense) {
      this.licenseData = this.workflow.licenseText;
    }

    this.workflow.currentRoute = this.$route.path;
  },
};
</script>
