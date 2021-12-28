<template>
  <div class="h-full w-full flex flex-col justify-center items-center pr-5 p-3">
    <div class="flex flex-col h-full w-full">
      <span class="text-lg font-medium text-left">
        Uploading your data to Zenodo
      </span>
      <span class="text-left">
        This one is on us. SODA is creating a Zenodo record for you and
        uploading all your files with the relevant metadata.
      </span>

      <el-divider class="my-4"> </el-divider>

      <div class="flex flex-col justify-center h-full">
        <el-progress
          :percentage="percentage"
          :indeterminate="indeterminate"
          :status="progressStatus"
          :stroke-width="10"
        />
        <el-alert
          class="my-2"
          v-if="showAlert"
          :title="alertTitle"
          type="error"
          :description="alertMessage"
          show-icon
        >
        </el-alert>
        <div class="flex flex-row justify-start items-center py-3" v-else>
          <LoadingCubeGrid
            class="w-5 h-5"
            v-if="percentage !== 100"
          ></LoadingCubeGrid>
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

      <div class="w-full flex flex-row justify-center py-2" v-if="showAlert">
        <router-link
          :to="`/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/zenodo/review`"
          class="mx-6"
        >
          <el-button type="danger" plain> Back </el-button>
        </router-link>

        <button class="primary-plain-button" @click="retryUpload">Retry</button>

        <!-- <el-button
          type="primary"
          class="flex flex-row items-center"
          @click="retryUpload"
        >
          Retry
        </el-button> -->
      </div>
    </div>
  </div>
</template>

<script>
// import { Icon } from "@iconify/vue";
import axios from "axios";
import dayjs from "dayjs";
import path from "path";
import fs from "fs-extra";

import LoadingCubeGrid from "../../components/spinners/LoadingCubeGrid.vue";
import LoadingEllipsis from "../../components/spinners/LoadingEllipsis.vue";

import { useDatasetsStore } from "../../store/datasets";
import { useTokenStore } from "../../store/access.js";

export default {
  name: "ZenodoUpload",
  components: { LoadingCubeGrid, LoadingEllipsis },
  data() {
    return {
      datasetStore: useDatasetsStore(),
      tokens: useTokenStore(),
      dataset: {},
      folderPath: "",
      workflowID: this.$route.params.workflowID,
      workflow: {},
      percentage: 0,
      indeterminate: true,
      progressStatus: "",
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
    async createZenodoDeposition() {
      this.statusMessage = "Creating an empty dataset on Zenodo";
      await this.sleep(300);
      // return "ERROR";
      return axios
        .post(`${this.$server_url}/zenodo/new`, {
          access_token: this.zenodoToken,
        })
        .then((response) => {
          return response.data;
        })
        .catch((error) => {
          console.error(error);
          return "ERROR";
        });
    },
    async addMetadaToZenodoDeposition() {
      this.statusMessage = "Adding metadata to Zenodo";
      await this.sleep(300);

      const zenodoMetadata = this.workflow.destination.zenodo.questions;
      let metadata = {};

      metadata.upload_type = "software";
      metadata.title = zenodoMetadata.title;
      metadata.publication_date = zenodoMetadata.publicationDate;

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

      metadata.description = zenodoMetadata.description;
      metadata.access_right = zenodoMetadata.license.accessRight;
      metadata.license = zenodoMetadata.license.licenseName;
      metadata.prereserve_doi = true;

      metadata.keywords = [];
      zenodoMetadata.keywords.forEach((keyword) => {
        metadata.keywords.push(keyword.keyword);
      });

      metadata.notes = zenodoMetadata.additionalNotes;

      metadata.related_identifiers = [];
      zenodoMetadata.relatedIdentifiers.forEach((relatedIdentifier) => {
        metadata.related_identifiers.push({
          relation: relatedIdentifier.relationship,
          identifier: relatedIdentifier.identifier,
          resource_type: relatedIdentifier.resourceType,
        });
      });

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
        if (zenodoMetadata.journal.title !== "") {
          metadata.journal_title = zenodoMetadata.journal.title;
        }
        if (zenodoMetadata.journal.volume !== "") {
          metadata.journal_volume = zenodoMetadata.journal.volume;
        }
        if (zenodoMetadata.journal.issue !== "") {
          metadata.journal_issue = zenodoMetadata.journal.issue;
        }
        if (zenodoMetadata.journal.pages !== "") {
          metadata.journal_pages = zenodoMetadata.journal.pages;
        }
      }

      if ("conference" in zenodoMetadata) {
        if (zenodoMetadata.conference.title !== "") {
          metadata.conference_title = zenodoMetadata.conference.title;
        }
        if (zenodoMetadata.conference.acronym !== "") {
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

        if (zenodoMetadata.conference.place !== "") {
          metadata.conference_place = zenodoMetadata.conference.place;
        }
        if (zenodoMetadata.conference.url !== "") {
          metadata.conference_url = zenodoMetadata.conference.url;
        }
        if (zenodoMetadata.conference.session !== "") {
          metadata.conference_session = zenodoMetadata.conference.session;
        }
        if (zenodoMetadata.conference.part !== "") {
          metadata.conference_session_part = zenodoMetadata.conference.part;
        }
      }

      if ("bookReportChapter" in zenodoMetadata) {
        metadata.imprint_publisher = zenodoMetadata.bookReportChapter.publisher;
        metadata.imprint_isbn = zenodoMetadata.bookReportChapter.isbn;
        metadata.imprint_place = zenodoMetadata.bookReportChapter.place;
        metadata.partof_title = zenodoMetadata.bookReportChapter.title;
        metadata.partof_pages = zenodoMetadata.bookReportChapter.pages;
      }

      if ("thesis" in zenodoMetadata) {
        metadata.thesis_university = zenodoMetadata.thesis.awardingUniversity;

        metadata.thesis_supervisors = [];
        zenodoMetadata.thesis.supervisors.forEach((supervisor) => {
          metadata.thesis_supervisors.push({
            name: supervisor.name,
            affiliation: supervisor.affiliation,
            orcid: supervisor.orcid,
          });
        });
      }

      if ("subjects" in zenodoMetadata) {
        metadata.subjects = [];
        zenodoMetadata.subjects.forEach((subject) => {
          metadata.subjects.push({
            term: subject.term,
            identifier: subject.identifier,
            scheme: "url",
          });
        });
      }

      if ("version" in zenodoMetadata) {
        if (zenodoMetadata.version !== "") {
          metadata.version = zenodoMetadata.version;
        }
      }

      if ("language" in zenodoMetadata) {
        if (zenodoMetadata.language !== "") {
          metadata.language = zenodoMetadata.language;
        }
      }

      console.log(metadata);

      const metadataObject = JSON.stringify({
        metadata: metadata,
      });

      return axios
        .post(`${this.$server_url}/zenodo/metadata`, {
          access_token: this.zenodoToken,
          deposition_id: this.workflow.destination.zenodo.deposition_id,
          metadata: metadataObject,
        })
        .then((response) => {
          console.log(response);
          if ("status" in response.data && response.data.status != 200) {
            if ("errors" in response.data) {
              response.data.errors.forEach((error) => {
                this.errorMessage += `${error.field} - ${error.message} \n`;
              });
            }
            this.alertTitle = "Metadata error";
            this.alertMessage =
              "Could not add your metadata to the dataset. Please try again.";
            return "ERROR";
          } else {
            return response.data;
          }
        })
        .catch((error) => {
          console.error(error);
          return "ERROR";
        });
    },
    async uploadToZenodo(bucket_url, file_path) {
      this.statusMessage = `Uploading ${path.basename(file_path)} to Zenodo`;
      await this.sleep(100);

      await axios
        .post(`${this.$server_url}/zenodo/upload`, {
          access_token: this.zenodoToken,
          bucket_url: bucket_url,
          file_path: file_path,
        })
        .then((response) => {
          return response.data;
        })
        .catch((error) => {
          console.error(error);
          return "ERROR";
        });

      this.statusMessage = `Uploaded ${path.basename(
        file_path
      )} to Zenodo successfully`;
      await this.sleep(300);
      return;
    },
    async checkForFoldersAndUpload() {
      this.statusMessage = "Checking folder path";
      await this.sleep(300);

      const folderPath = this.dataset.data[this.workflow.type[0]].folderPath;
      // console.log(folderPath);

      const response = await axios
        .post(`${this.$server_url}/utilities/checkforfolders`, {
          folder_path: folderPath,
        })
        .then((response) => {
          return response.data;
        })
        .catch((error) => {
          console.error(error);
          return "ERROR";
        });

      if (response) {
        this.statusMessage =
          "Found sub folders. Creating a zip of the requested folder";
        await this.sleep(300);

        const zippedPath = await axios
          .post(`${this.$server_url}/utilities/zipfolder`, {
            folder_path: folderPath,
          })
          .then((response) => {
            return response.data;
          })
          .catch((error) => {
            console.error(error);
            return "ERROR";
          });

        // console.log(zippedPath);

        this.statusMessage =
          "Created a zipped folder successfully. Getting ready to upload to Zenodo";
        await this.sleep(300);

        await this.uploadToZenodo(
          this.workflow.destination.zenodo.bucket,
          zippedPath
        );
      } else {
        this.statusMessage = "Getting ready to upload to Zenodo";
        await this.sleep(300);

        const contents = fs.readdirSync(folderPath);

        for (const [index, file] of contents.entries()) {
          await this.uploadToZenodo(
            this.workflow.destination.zenodo.bucket,
            path.join(folderPath, file)
          );
          this.percentage = ((index + 1) / contents.length) * 80 + 20;
          this.percentage = Math.round(this.percentage);
        }

        this.statusMessage = "Uploaded all files to Zenodo successfully";
        await this.sleep(300);
      }

      this.percentage = 100;
      this.indeterminate = false;

      return "SUCCESS";
    },
    async createCodeMetadataFile() {
      const response = await axios
        .post(`${this.$server_url}/metadata/create`, {
          data_types: JSON.stringify(this.workflow.type),
          data_object: JSON.stringify(this.dataset.data),
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
    async uploadWorkflow() {
      let response = "";
      response = await this.createZenodoDeposition();

      if (response === "ERROR") {
        this.alertMessage = "There was an error creating the deposition";
        return "FAIL";
      } else {
        this.statusMessage = "Empty deposition created on Zenodo";
      }

      this.percentage = 10;
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

      if (this.codePresent && "metadata" in response) {
        this.dataset.data.Code.questions.uniqueIdentifier =
          response.metadata.prereserve_doi.doi;

        response = await this.createCodeMetadataFile();
        // console.log(response);

        if (response === "ERROR") {
          this.alertMessage =
            "There was an error with creating the code metadata file";
          return "FAIL";
        } else {
          this.statusMessage =
            "Created the codemeta.json file in the target folder";

          await this.datasetStore.updateCurrentDataset(this.dataset);
          await this.datasetStore.syncDatasets();
        }
      }

      this.percentage = 15;
      this.indeterminate = false;

      await this.sleep(300);

      response = await this.addMetadaToZenodoDeposition();

      if (response === "ERROR") {
        this.alertMessage =
          "There was an error when adding metadata to the deposition";
        return "FAIL";
      } else {
        console.log(response);
        this.statusMessage =
          "Metadata successfully added to the Zenodo deposition";
      }

      this.percentage = 20;
      this.indeterminate = false;

      this.workflow.destination.zenodo.status.metadataAdded = true;

      await this.sleep(300);

      response = await this.checkForFoldersAndUpload();

      if (response === "ERROR") {
        this.alertMessage =
          "There was an error with uploading files to the Zenodo deposition";
        return "FAIL";
      } else {
        this.statusMessage = "Uploaded all files to Zenodo successfully.";
      }

      this.workflow.destination.zenodo.status.filesUploaded = true;

      return "SUCCESS";
    },
    async deleteDraftZenodoDeposition() {
      if ("deposition_id" in this.workflow.destination.zenodo) {
        console.log(
          this.zenodoToken,
          this.workflow.destination.zenodo.deposition_id
        );
        const response = await axios
          .delete(`${this.$server_url}/zenodo/delete`, {
            data: {
              access_token: this.zenodoToken,
              deposition_id: this.workflow.destination.zenodo.deposition_id,
            },
          })
          .then((response) => {
            console.log(response.data);
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
    async runZenodoUpload() {
      this.statusMessage = "Preparing backend services...";
      await this.sleep(300);

      let response = await this.uploadWorkflow();

      if (response === "FAIL") {
        this.indeterminate = true;
        this.progressStatus = "exception";
        this.showAlert = true;

        this.deleteDraftZenodoDeposition();

        this.workflow.datasetUploaded = false;
        this.workflow.datasetPublished = false;

        await this.datasetStore.updateCurrentDataset(this.dataset);
        await this.datasetStore.syncDatasets();

        return;
      } else {
        this.workflow.datasetUploaded = true;
        this.workflow.datasetPublished = false;

        await this.datasetStore.updateCurrentDataset(this.dataset);
        await this.datasetStore.syncDatasets();

        const routerPath = `/datasets/${this.datasetID}/${this.workflowID}/zenodo/publish`;
        this.$router.push({ path: routerPath });
      }
    },
    async retryUpload() {
      this.runZenodoUpload();
    },
  },
  async mounted() {
    this.dataset = await this.datasetStore.getCurrentDataset();
    this.workflow = this.dataset.workflows[this.workflowID];

    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(5);

    const tokenObject = await this.tokens.getToken("zenodo");
    this.zenodoToken = tokenObject.token;
    console.log(this.zenodoToken);

    this.runZenodoUpload();
  },
};
</script>

<style lang="postcss" scoped></style>
