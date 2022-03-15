<template>
  <div class="flex h-full w-full flex-col items-center justify-center p-3 pr-5">
    <div class="flex h-full w-full flex-col">
      <span class="text-left text-lg font-medium"> Uploading your metadata files to GitHub </span>
      <span class="text-left">
        This one is on us. We're working hard to get your files up to GitHub.
      </span>

      <el-divider class="my-4"> </el-divider>

      <div class="flex h-full flex-col justify-center">
        <el-progress
          :percentage="percentage"
          :indeterminate="indeterminate"
          :status="progressStatus"
          :stroke-width="10"
          class="my-2"
        />
        <el-alert
          v-if="showAlert"
          :title="alertTitle"
          type="error"
          :description="alertMessage"
          show-icon
        >
        </el-alert>
        <div class="flex flex-row items-center justify-start py-3" v-else>
          <LoadingCubeGrid class="h-5 w-5" v-if="percentage !== 100"></LoadingCubeGrid>
          <p class="pl-4">
            {{ statusMessage }}
            <LoadingEllipsis v-if="percentage !== 100"></LoadingEllipsis>
          </p>
        </div>
        <div class="pt-2 pl-2" v-if="errorMessage != ''">
          <p style="white-space: pre-line">
            {{ errorMessage }}
          </p>
        </div>
      </div>

      <div class="flex w-full flex-row justify-center py-2" v-if="showAlert">
        <router-link
          :to="`/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/zenodo/metadata`"
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
import { app } from "@electron/remote";
import axios from "axios";
import dayjs from "dayjs";
import path from "path";
import fs from "fs-extra";

import LoadingCubeGrid from "@/components/spinners/LoadingCubeGrid.vue";
import LoadingEllipsis from "@/components/spinners/LoadingEllipsis.vue";

import { useDatasetsStore } from "@/store/datasets";
import { useTokenStore } from "@/store/access.js";

export default {
  name: "GithubUpload",
  components: { LoadingCubeGrid, LoadingEllipsis },
  data() {
    return {
      datasetStore: useDatasetsStore(),
      tokens: useTokenStore(),
      dataset: {},
      tempFolderPath: "",
      workflowID: this.$route.params.workflowID,
      workflow: {},
      percentage: 0,
      indeterminate: true,
      progressStatus: "",
      githubToken: "",
      statusMessage: "some status message here",
      errorMessage: "",
      showAlert: false,
      alertTitle: "",
      alertMessage: "",
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

    async createCodeMetadataFile() {
      const response = await axios
        .post(`${this.$server_url}/metadata/create`, {
          data_types: JSON.stringify(this.workflow.type),
          data_object: JSON.stringify(this.dataset.data),
          virtual_file: false,
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
    async createCitationFile() {
      const response = await axios
        .post(`${this.$server_url}/metadata/citation/create`, {
          data_types: JSON.stringify(this.workflow.type),
          data_object: JSON.stringify(this.dataset.data),
          virtual_file: false,
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
    async createLicenseFile() {
      const folderPath = this.dataset.data.Code.folderPath;

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
    async createZenodoJSON() {
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

      const metadataObject = JSON.stringify(metadata);

      const folderPath = this.dataset.data.Code.folderPath;

      const response = await axios
        .post(`${this.$server_url}/utilities/createfile`, {
          folder_path: folderPath,
          file_name: ".zenodo.json",
          file_content: metadataObject,
          content_type: "json",
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

    async uploadToGithub(filePath, fileName, repoName) {
      this.statusMessage = `Uploading ${fileName} to GitHub`;
      await this.sleep(100);

      const response = await axios
        .post(`${this.$server_url}/github/upload`, {
          access_token: this.githubToken,
          file_path: filePath,
          file_name: fileName,
          repo_name: repoName,
        })
        .then((response) => {
          return response.data;
        })
        .catch((error) => {
          console.error(error);
          return "ERROR";
        });

      if (response === "ERROR") {
        if (fileName === "LICENSE") {
          this.alertMessage = `Error uploading ${fileName} to GitHub. There may be illegal characters in the contents of the file. Please verify that the file is valid and try again.`;
        } else {
          this.alertMessage = `Error uploading ${fileName} to GitHub. Please verify that the file is valid and try again.`;
        }
        await this.sleep(300);
        this.statusMessage = "";
      } else {
        this.statusMessage = `${fileName} uploaded to GitHub`;
        await this.sleep(300);
        this.alertMessage = "";
      }

      return response;
    },

    async uploadMetadataFiles() {
      const folderPath = this.dataset.data.Code.folderPath;
      const repoName = this.workflow.github.repo;

      this.statusMessage = "Getting ready to upload metadata files to GitHub...";
      await this.sleep(300);

      const contents = fs.readdirSync(folderPath);

      for (const [index, file] of contents.entries()) {
        const filePath = path.join(folderPath, file);

        const response = await this.uploadToGithub(filePath, file, repoName);

        if (response === "ERROR") {
          return response;
        }

        this.percentage = ((index + 1) / contents.length) * 75 + 25;
        this.percentage = Math.round(this.percentage);
      }

      return "SUCCESS";
    },

    async uploadWorkflow() {
      let response = "";

      if (this.workflow.generateCodeMeta) {
        if (this.codePresent) {
          response = await this.createCodeMetadataFile();

          if (response === "ERROR") {
            this.alertMessage = "There was an error with creating the code metadata file";
            return "FAIL";
          } else {
            this.statusMessage = "Created a temporary codemeta.json file";
          }
        }
      }

      this.percentage = 5;
      this.indeterminate = false;

      await this.sleep(300);

      if (this.workflow.generateCodeMeta) {
        if (this.codePresent) {
          response = await this.createCitationFile();

          if (response === "ERROR") {
            this.alertMessage = "There was an error with creating the CITATION.cff file";
            return "FAIL";
          } else {
            this.statusMessage = "Created a temporary CITATION.cff file";
          }
        }
      }

      this.percentage = 10;
      this.indeterminate = false;

      await this.sleep(300);

      if (this.workflow.generateLicense) {
        response = await this.createLicenseFile();

        if (response === "ERROR") {
          this.alertMessage = "There was an error with creating the LICENSE file";
          return "FAIL";
        } else {
          this.statusMessage = "Created a temporary LICENSE file";
        }
      }

      this.percentage = 15;
      this.indeterminate = false;

      await this.sleep(300);

      if (this.workflow.uploadToRepo) {
        response = await this.createZenodoJSON();

        if (response === "ERROR") {
          this.alertMessage = "There was an error with creating the .zenodo.json file";
          return "FAIL";
        } else {
          this.statusMessage = "Created a temporary .zenodo.json file";
        }

        this.percentage = 20;
        this.indeterminate = false;

        this.workflow.destination.zenodo.status.metadataAdded = true;
      }

      await this.sleep(300);

      response = await this.uploadMetadataFiles();

      if (response === "ERROR") {
        // this.alertMessage =
        //   "There was an error with uploading files to the GitHub repository";
        return "FAIL";
      } else {
        this.statusMessage = "Uploaded all files to GitHub successfully.";
      }

      if (this.workflow.uploadToRepo) {
        this.workflow.destination.zenodo.status.filesUploaded = true;
      }

      return "SUCCESS";
    },

    async runGithubUpload() {
      await this.datasetStore.hideSidebar();

      this.statusMessage = "Preparing backend services...";
      await this.sleep(300);

      let response = await this.uploadWorkflow();

      await this.datasetStore.showSidebar();

      this.dataset.data.Code.folderPath = "";

      if (response === "FAIL" || response === "ERROR") {
        this.indeterminate = true;
        this.progressStatus = "exception";
        this.showAlert = true;

        this.workflow.datasetUploaded = false;
        this.workflow.datasetPublished = false;

        await this.datasetStore.updateCurrentDataset(this.dataset);
        await this.datasetStore.syncDatasets();

        return;
      } else {
        this.workflow.datasetUploaded = true;
        this.workflow.datasetPublished = false;
        this.workflow.generateLicense = false;

        await this.datasetStore.updateCurrentDataset(this.dataset);
        await this.datasetStore.syncDatasets();

        let routerPath = "";

        if (this.workflow.uploadToRepo) {
          routerPath = `/datasets/${this.datasetID}/${this.workflowID}/github/publish`;
        } else {
          routerPath = `/datasets/${this.datasetID}/${this.workflowID}/githubNoUpload/finalPage`;
        }

        this.$router.push({ path: routerPath });
      }
    },
    async retryUpload() {
      this.indeterminate = false;
      this.progressStatus = "";
      this.showAlert = false;

      const tempFolderPath = path.join(app.getPath("home"), ".fairshare", "temp");

      // delete the temp folder if it exists
      // starting from a clean slate
      if (fs.existsSync(tempFolderPath)) {
        fs.rmdirSync(tempFolderPath, { recursive: true, force: true });
      }

      // recreate the temp folder
      if (!fs.existsSync(tempFolderPath)) {
        fs.mkdirSync(tempFolderPath);
      }

      this.dataset.data.Code.folderPath = tempFolderPath;

      this.runGithubUpload();
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

    const tokenObject = await this.tokens.getToken("github");
    this.githubToken = tokenObject.token;

    const tempFolderPath = path.join(app.getPath("home"), ".fairshare", "temp");

    // delete the temp folder if it exists
    // starting from a clean slate
    if (fs.existsSync(tempFolderPath)) {
      fs.rmdirSync(tempFolderPath, { recursive: true, force: true });
    }

    // recreate the temp folder
    if (!fs.existsSync(tempFolderPath)) {
      fs.mkdirSync(tempFolderPath);
    }

    this.dataset.data.Code.folderPath = tempFolderPath;

    this.runGithubUpload();
  },
};
</script>

<style lang="postcss" scoped></style>
