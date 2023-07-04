<template>
  <div class="flex h-full w-full flex-col items-center justify-center p-3 pr-5">
    <div class="flex h-full w-full flex-col">
      <span class="text-left text-lg font-medium">
        Let's upload all your files to the correct places.
      </span>
      <span class="text-left">
        This one is on us. We're working hard to get your files up to GitHub and your dataset to
        Zenodo.
      </span>

      <line-divider />

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
        <div class="pl-2 pt-2" v-if="errorMessage != ''">
          <p style="white-space: pre-line">
            {{ errorMessage }}
          </p>
        </div>
      </div>

      <div class="flex w-full flex-row justify-center py-2" v-if="showAlert">
        <router-link
          :to="`/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/github/summary`"
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
import axios from "axios";
import dayjs from "dayjs";
import path from "path";
import fs from "fs-extra";
// import klawSync from "klaw-sync";

import LoadingCubeGrid from "@/components/spinners/LoadingCubeGrid.vue";
import LoadingEllipsis from "@/components/spinners/LoadingEllipsis.vue";

import { useDatasetsStore } from "@/store/datasets";
import { useTokenStore } from "@/store/access.js";

export default {
  name: "GithubZenodoUpload",
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
      zenodoToken: "",
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
          this.$track("Metadata", "Create codemeta", "success");
          return response.data;
        })
        .catch((error) => {
          this.$track("Metadata", "Create codemeta", "failed");
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
          this.$track("Metadata", "Create citation", "success");
          return response.data;
        })
        .catch((error) => {
          this.$track("Metadata", "Create citation", "failed");

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
          this.$track("Metadata", "Create license", "success");
          return response.data;
        })
        .catch((error) => {
          this.$track("Metadata", "Create license", "failed");
          console.error(error);
          return "ERROR";
        });
      return response;
    },
    async addMetadataToZenodoDeposition() {
      this.statusMessage = "Adding metadata to Zenodo";
      await this.sleep(300);

      const zenodoMetadata = this.workflow.destination.zenodo.questions;
      let metadata = {};

      if ("uploadType" in zenodoMetadata) {
        metadata.upload_type = zenodoMetadata.uploadType;
      } else {
        metadata.upload_type = "software";
      }

      metadata.prereserve_doi = true;

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
          "supervisors" in zenodoMetadata.thesis &&
          zenodoMetadata.thesis.supervisors.length > 0
        ) {
          metadata.thesis_supervisors = [];
          zenodoMetadata.thesis.supervisors.forEach(({ name, affiliation, orcid }) => {
            metadata.thesis_supervisors.push({
              name,
              affiliation,
              orcid,
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

      const metadataObject = JSON.stringify({
        metadata: metadata,
      });

      return axios
        .post(`${this.$server_url}/zenodo/deposition/metadata`, {
          access_token: this.zenodoToken,
          deposition_id: this.workflow.destination.zenodo.deposition_id,
          metadata: metadataObject,
        })
        .then((response) => {
          if ("status" in response.data && response.data.status != 200) {
            if ("errors" in response.data) {
              response.data.errors.forEach((error) => {
                this.errorMessage += `${error.field} - ${error.message} \n`;
              });
            }
            this.alertTitle = "Metadata error";
            this.alertMessage = "Could not add your metadata to the dataset. Please try again.";
            this.$track("Zenodo", "Add metadata to Zenodo deposition", "failed");
            return "ERROR";
          } else {
            this.$track("Zenodo", "Add metadata to Zenodo deposition", "success");
            return response.data;
          }
        })
        .catch((error) => {
          this.$track("Zenodo", "Add metadata to Zenodo deposition", "failed");
          console.error(error);
          return "ERROR";
        });
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
          this.$track("GitHub", "Uploaded file to GitHub", "success");
          return response.data;
        })
        .catch((error) => {
          this.$track("GitHub", "Uploaded file to GitHub", "success");
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

      this.$track("GitHub", "Repository name", repoName);

      this.statusMessage = "Getting ready to upload metadata files to GitHub...";
      await this.sleep(300);

      const contents = fs.readdirSync(folderPath);

      for (const [index, file] of contents.entries()) {
        const filePath = path.join(folderPath, file);

        const response = await this.uploadToGithub(filePath, file, repoName);
        // const response = filePath;

        if (response === "ERROR") {
          return response;
        }

        this.percentage = ((index + 1) / contents.length) * 8 + 17;
        this.percentage = Math.round(this.percentage);
      }

      return "SUCCESS";
    },
    async createZenodoDeposition() {
      this.statusMessage = "Creating an empty dataset on Zenodo";
      await this.sleep(300);
      // return "ERROR";
      return axios
        .post(`${this.$server_url}/zenodo/deposition`, {
          access_token: this.zenodoToken,
        })
        .then((response) => {
          this.$track("Zenodo", "Create empty deposition", "success");
          return response.data;
        })
        .catch((error) => {
          this.$track("Zenodo", "Create empty deposition", "failed");
          console.error(error);
          return "ERROR";
        });
    },
    async getGithubRepoZipball() {
      const repo = this.workflow.github.repo;
      const default_branch = this.workflow.github.fullObject.default_branch;

      const tempFolderPath = this.dataset.data.Code.folderPath;

      const zip_file_name = `${repo.split("/")[1]}.zip`;
      const zip_file_path = path.join(tempFolderPath, zip_file_name);

      this.statusMessage = `Downloading ${zip_file_name} to ${zip_file_path}`;

      const res = await axios
        .get(`${this.$server_url}/github/repo/zipball`, {
          params: {
            access_token: this.githubToken,
            repo,
            default_branch,
            file_path: zip_file_path,
          },
        })
        .then((response) => {
          return response.data;
        })
        .catch((error) => {
          console.error(error);
          return "ERROR";
        });

      return res;
    },
    async getAssetFromGithubRelease(browser_download_url, file_name) {
      const tempFolderPath = this.dataset.data.Code.folderPath;
      const file_path = path.join(tempFolderPath, file_name);

      this.statusMessage = `Writing ${file_name} to ${file_path}`;

      const res = await axios
        .get(`${this.$server_url}/github/release/asset`, {
          params: {
            access_token: this.zenodoToken,
            browser_download_url,
            file_path,
          },
        })
        .then((response) => {
          return response.data;
        })
        .catch((error) => {
          console.error(error);
          return "ERROR";
        });

      return res;
    },
    async uploadFileToZenodo(bucket_url, file_path) {
      this.statusMessage = `Uploading ${path.basename(file_path)} to Zenodo`;
      await this.sleep(100);

      const response = await axios
        .post(`${this.$server_url}/zenodo/deposition/files/upload`, {
          access_token: this.zenodoToken,
          bucket_url: bucket_url,
          file_path: file_path,
        })
        .then((response) => {
          this.$track("Zenodo", "Uploaded file to Zenodo", "success");
          return response.data;
        })
        .catch((error) => {
          this.$track("Zenodo", "Uploaded file to Zenodo", "failed");
          console.error(error);
          return "ERROR";
        });

      this.statusMessage = `Uploaded ${path.basename(file_path)} to Zenodo successfully`;
      await this.sleep(300);
      return response;
    },
    async uploadDatasetToZenodo() {
      this.statusMessage = "Checking folder path";
      await this.sleep(300);

      const folderPath = this.dataset.data.Code.folderPath;

      this.statusMessage = "Getting ready to upload to Zenodo";
      await this.sleep(300);

      const tempFolderContents = fs.readdirSync(folderPath);
      const contents = [];

      for (const file of tempFolderContents) {
        const filePath = path.join(folderPath, file);
        contents.push(filePath);
      }

      if ("addAdditionalFiles" in this.workflow && this.workflow.addAdditionalFiles) {
        if (
          "additionalFilesLocation" in this.workflow &&
          this.workflow.additionalFilesLocation === "local" &&
          "localFileList" in this.workflow &&
          this.workflow.localFileList.length > 0
        ) {
          contents.push(...this.workflow.localFileList);
        }
      }

      for (const [index, file] of contents.entries()) {
        const response = await this.uploadFileToZenodo(
          this.workflow.destination.zenodo.bucket,
          file
        );

        if (response === "ERROR") {
          return "ERROR";
        }

        this.percentage = ((index + 1) / contents.length) * 60 + 40;
        this.percentage = Math.round(this.percentage);
      }

      this.statusMessage = "Uploaded all files to Zenodo successfully";
      await this.sleep(300);

      this.percentage = 100;
      this.indeterminate = false;

      return "SUCCESS";
    },
    async uploadWorkflow() {
      let response = {};

      if (this.workflow.destination.zenodo.newVersion) {
        this.statusMessage = "Creating a new version of the Zenodo Deposition";

        await this.sleep(300);

        const original_deposition_id = this.workflow.destination.zenodo.selectedDeposition.id;

        let res = null;

        res = await axios
          .post(`${this.$server_url}/zenodo/deposition/newversion`, {
            access_token: this.zenodoToken,
            deposition_id: original_deposition_id,
          })
          .then((response) => {
            this.$track("Zenodo", "Create new version", "success");
            return response.data;
          })
          .catch((error) => {
            this.$track("Zenodo", "Create new version", "failed");
            console.error(error);
            return "ERROR";
          });

        const deposition_id = res;

        if (res === "ERROR") {
          this.alertMessage = "There was an error with creating a new version";
          return "FAIL";
        }

        this.percentage = 1;
        this.indeterminate = false;

        this.statusMessage = "Requesting new Zenodo deposition version data";

        await this.sleep(300);

        res = await axios
          .get(`${this.$server_url}/zenodo/deposition`, {
            params: {
              access_token: this.zenodoToken,
              deposition_id,
            },
          })
          .then((response) => {
            return response.data;
          })
          .catch((error) => {
            console.error(error);
            return "ERROR";
          });

        if (res === "ERROR") {
          this.alertMessage = "There was an error with requesting data from Zenodo";
          return "FAIL";
        } else {
          //create a copy of the res object
          response = JSON.parse(JSON.stringify(res));

          this.statusMessage =
            "Succeeded in requesting data from the new version of the zenodo deposition";
        }

        this.percentage = 3;
        this.indeterminate = false;

        const files_list = res.files;

        for (let file of files_list) {
          this.statusMessage = `Removing pre-existing file '${file.filename}' from new Zenodo deposition version`;

          await this.sleep(100);

          await axios
            .delete(`${this.$server_url}/zenodo/deposition/files`, {
              data: {
                access_token: this.zenodoToken,
                deposition_id,
                file_id: file.id,
              },
            })
            .then((response) => {
              return response.data;
            })
            .catch((error) => {
              console.error(error);
              return "ERROR";
            });
        }

        this.statusMessage = "Succeeded in removing all old pre-existing files";
      } else {
        response = await this.createZenodoDeposition();

        if (response === "ERROR") {
          this.alertMessage = "There was an error creating the deposition";
          return "FAIL";
        } else {
          this.statusMessage = "Empty deposition created on Zenodo";
        }
      }

      this.percentage = 5;
      this.indeterminate = false;

      await this.sleep(300);

      this.workflow.destination.zenodo.status.depositionCreated = true;

      this.workflow.destination.zenodo.bucket = response.links.bucket;
      this.workflow.destination.zenodo.deposition_id = response.id;
      this.workflow.destination.zenodo.originalDeposition = response;
      this.workflow.destination.zenodo.deposition = response;

      await this.datasetStore.updateCurrentDataset(this.dataset);
      await this.datasetStore.syncDatasets();

      await this.sleep(300);

      // create codemeta.json
      if (this.workflow.generateCodeMeta) {
        if (this.codePresent) {
          this.dataset.data.Code.questions.identifier = response.metadata.prereserve_doi.doi;

          response = await this.createCodeMetadataFile();

          if (response === "ERROR") {
            this.alertMessage = "There was an error with creating the code metadata file";
            return "FAIL";
          } else {
            this.statusMessage = "Created the codemeta.json file in the target folder";

            await this.datasetStore.updateCurrentDataset(this.dataset);
            await this.datasetStore.syncDatasets();
          }
        }
      }

      this.percentage = 12;
      this.indeterminate = false;

      await this.sleep(300);

      // create citation.cff
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

      this.percentage = 14;
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
        response = await this.addMetadataToZenodoDeposition();

        if (response === "ERROR") {
          this.alertMessage = "There was an error when adding metadata to the deposition";
          return "FAIL";
        } else {
          this.statusMessage = "Metadata successfully added to the Zenodo deposition";
        }

        this.workflow.destination.zenodo.status.metadataAdded = true;
      }

      this.percentage = 17;
      this.indeterminate = false;

      await this.sleep(300);

      // for now this is going to be mandatory.
      // will have to figure out  where to ask this question
      response = await this.uploadMetadataFiles();

      await this.resetTempFolder();

      if (response === "ERROR") {
        this.alertMessage = "There was an error with uploading files to the GitHub repository";
        return "FAIL";
      } else {
        this.statusMessage = "Uploaded all files to GitHub successfully.";
      }

      this.percentage = 25;
      this.indeterminate = false;

      await this.sleep(300);

      this.statusMessage = "Preparing to extract source code from the repository";

      await this.sleep(300);

      response = await this.getGithubRepoZipball();

      if (response === "ERROR") {
        this.alertMessage = "There was an error with downloading the repository source code";
        return "FAIL";
      } else {
        this.statusMessage = "Downloaded the repository source code successfully";
      }

      this.percentage = 30;
      this.indeterminate = false;

      if ("addAdditionalFiles" in this.workflow && this.workflow.addAdditionalFiles) {
        this.statusMessage = "Preparing to add additional files to the repository";

        await this.sleep(300);

        if (
          "additionalFilesLocation" in this.workflow &&
          this.workflow.additionalFilesLocation === "github" &&
          "addedReleaseAssets" in this.workflow &&
          this.workflow.addedReleaseAssets.length > 0
        ) {
          const contents = this.workflow.addedReleaseAssets;

          for (const [index, file] of contents.entries()) {
            response = await this.getAssetFromGithubRelease(file, path.basename(file));

            this.percentage = ((index + 1) / contents.length) * 10 + 30;
            this.percentage = Math.round(this.percentage);

            if (response === "ERROR") {
              this.alertMessage =
                "There was an error with downloading a release asset from the GitHub repository";
              return "FAIL";
            } else {
              this.statusMessage = "Downloaded asset from the GitHub repository successfully";
            }
          }
        }
      }

      if (this.workflow.uploadToRepo) {
        response = await this.uploadDatasetToZenodo();
      }

      if (response === "ERROR") {
        this.alertMessage = "There was an error with uploading the dataset to Zenodo";
        return "FAIL";
      } else {
        this.statusMessage = "Uploaded the dataset to Zenodo successfully";
      }

      if (this.workflow.uploadToRepo) {
        this.workflow.destination.zenodo.status.filesUploaded = true;
      }

      this.percentage = 100;
      this.indeterminate = false;

      return "SUCCESS";
    },
    async deleteDraftZenodoDeposition() {
      if ("deposition_id" in this.workflow.destination.zenodo) {
        const response = await axios
          .delete(`${this.$server_url}/zenodo/deposition`, {
            data: {
              access_token: this.zenodoToken,
              deposition_id: this.workflow.destination.zenodo.deposition_id,
            },
          })
          .then((response) => {
            return response.data;
          })
          .catch((error) => {
            console.error(error);
            return "ERROR";
          });
        return response.data;
      }
      return "NO_DEPOSITION_FOUND";
    },
    async runUploadWorkflow() {
      await this.datasetStore.hideSidebar();

      this.statusMessage = "Preparing backend services...";
      await this.sleep(300);

      let response = await this.uploadWorkflow();

      this.dataset.data.Code.folderPath = "";

      if (response === "FAIL" || response === "ERROR") {
        await this.datasetStore.showSidebar();

        this.indeterminate = true;
        this.progressStatus = "exception";
        this.showAlert = true;

        this.workflow.datasetUploaded = false;
        this.workflow.datasetPublished = false;

        await this.datasetStore.updateCurrentDataset(this.dataset);
        await this.datasetStore.syncDatasets();

        return;
      }

      this.workflow.datasetUploaded = true;
      this.workflow.datasetPublished = false;
      this.workflow.generateLicense = false;

      await this.datasetStore.updateCurrentDataset(this.dataset);
      await this.datasetStore.syncDatasets();

      await this.sleep(300);

      this.datasetStore.showSidebar(); // can show the sidebar regardless of the response

      if (response === "FAIL" || response === "ERROR") {
        this.indeterminate = true;
        this.progressStatus = "exception";
        this.showAlert = true;

        this.deleteDraftZenodoDeposition();

        this.workflow.datasetUploaded = false;
        this.workflow.datasetPublished = false;

        await this.datasetStore.updateCurrentDataset(this.dataset);
        await this.datasetStore.syncDatasets();

        return;
      }

      this.workflow.datasetUploaded = true;
      this.workflow.datasetPublished = false;
      this.workflow.generateLicense = false;

      await this.datasetStore.updateCurrentDataset(this.dataset);
      await this.datasetStore.syncDatasets();

      const routerPath = `/datasets/${this.datasetID}/${this.workflowID}/zenodo/publish`;

      this.$router.push({ path: routerPath });
    },
    async retryUpload() {
      this.indeterminate = false;
      this.progressStatus = "";
      this.showAlert = false;

      const tempFolderPath = await this.resetTempFolder();

      this.dataset.data.Code.folderPath = tempFolderPath;

      this.runUploadWorkflow();
    },
    async resetTempFolder() {
      const tempFolderPath = path.join(this.$home_path, ".fairshare", "temp");

      // delete the temp folder if it exists
      // starting from a clean slate
      if (fs.existsSync(tempFolderPath)) {
        fs.rmdirSync(tempFolderPath, { recursive: true, force: true });
      }

      // recreate the temp folder
      if (!fs.existsSync(tempFolderPath)) {
        fs.mkdirSync(tempFolderPath);
      }

      return tempFolderPath;
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

    const githubTokenObject = await this.tokens.getToken("github");
    this.githubToken = githubTokenObject.token;

    const zenodoTokenObject = await this.tokens.getToken("zenodo");
    this.zenodoToken = zenodoTokenObject.token;

    const tempFolderPath = await this.resetTempFolder();

    this.dataset.data.Code.folderPath = tempFolderPath;

    this.runUploadWorkflow();
  },
};
</script>
