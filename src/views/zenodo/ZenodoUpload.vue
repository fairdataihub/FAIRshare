<template>
  <div class="h-screen w-full flex flex-row lg:justify-center items-center">
    <div class="p-3 h-full w-full lg:w-auto flex flex-row items-center">
      <div class="h-full w-full">
        <div class="flex flex-col h-full overflow-y-auto pr-5">
          <span class="text-lg font-medium text-left">
            Uploading your data to Zenodo
          </span>
          <span class="text-left">
            This ones on us. SODA is creating a Zenodo record for you and
            uploading all your files with the relevant metadata.
          </span>

          <el-divider class="my-4"> </el-divider>

          <div class="flex flex-col justify-center h-full">
            <el-progress
              :percentage="percentage"
              :indeterminate="indeterminate"
              :stroke-width="10"
            />
            <div class="flex flex-row justify-start items-center py-3">
              <LoadingCubeGrid
                class="w-5 h-5"
                v-if="percentage !== 100"
              ></LoadingCubeGrid>
              <p class="pl-4">
                {{ statusMessage }}
                <LoadingEllipsis v-if="percentage !== 100"></LoadingEllipsis>
              </p>
            </div>
          </div>
        </div>
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
      zenodoToken: "",
      statusMessage: "some status message here",
    };
  },
  computed: {},
  methods: {
    async sleep(ms) {
      return new Promise((resolve) => setTimeout(resolve, ms));
    },
    async createZenodoDeposition() {
      this.statusMessage = "Creating an empty dataset on Zenodo";
      await this.sleep(300);

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
        metadata.creators.push({
          name: author.name,
          affiliation: author.affiliation,
          orcid: author.orcid,
        });
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

      metadata.contributors = [];
      zenodoMetadata.contributors.forEach((contributor) => {
        metadata.contributors.push({
          name: contributor.name,
          affiliation: contributor.affiliation,
          orcid: contributor.orcid,
          type: contributor.contributorType,
        });
      });

      metadata.references = [];
      zenodoMetadata.references.forEach((reference) => {
        metadata.references.push(reference.reference);
      });

      if ("journal" in zenodoMetadata) {
        metadata.journal_title = zenodoMetadata.journal.title;
        metadata.journal_volume = zenodoMetadata.journal.volume;
        metadata.journal_issue = zenodoMetadata.journal.issue;
        metadata.journal_pages = zenodoMetadata.journal.pages;
      }

      if ("conference" in zenodoMetadata) {
        metadata.conference_title = zenodoMetadata.conference.title;
        metadata.conference_acronym = zenodoMetadata.conference.acronym;

        if (zenodoMetadata.conference.dates.length === 2) {
          metadata.conference_dates =
            dayjs(zenodoMetadata.conference.dates[0]).format("MMMM D, YYYY") +
            " - " +
            dayjs(zenodoMetadata.conference.dates[1]).format("MMMM D, YYYY");
        }

        metadata.conference_place = zenodoMetadata.conference.place;
        metadata.conference_url = zenodoMetadata.conference.url;
        metadata.conference_session = zenodoMetadata.conference.session;
        metadata.conference_session_part = zenodoMetadata.conference.part;
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

      metadata.version = zenodoMetadata.version;
      metadata.language = zenodoMetadata.language;

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
          return response.data;
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
      console.log(folderPath);

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

        console.log(zippedPath);

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
        }

        this.statusMessage = "Uploaded all files to Zenodo successfully";
        await this.sleep(300);
      }

      this.percentage = 100;
      this.indeterminate = false;

      return "SUCCESS";
    },
    async createCodeMetadataFile() {
      await axios
        .post(`${this.$server_url}/metadata/create`, {
          data_types: JSON.stringify(this.workflow.type),
          data: JSON.stringify(this.dataset.data),
        })
        .then((response) => {
          return response.data;
        })
        .catch((error) => {
          console.error(error);
          return "ERROR";
        });
    },
    async uploadWorkflow() {
      let response = "";
      response = await this.createZenodoDeposition();

      if (response === "ERROR") {
        this.statusMessage = "There was an error creating the deposition";
        return "FAIL";
      } else {
        this.statusMessage = "Empty deposition created on Zenodo";
      }

      this.percentage = 10;
      this.indeterminate = false;

      if (this.codePresent() && "doi" in response) {
        this.dataset.data.Code.question.uniqueIdentifier = response.doi;
        response = await this.createCodeMetadataFile();

        if (response === "ERROR") {
          this.statusMessage =
            "There was an error with creating the code metadata file.";
          return "FAIL";
        } else {
          this.statusMessage = "Empty deposition created on Zenodo";
        }
      }

      this.percentage = 15;
      this.indeterminate = false;

      this.workflow.destination.zenodo.status.depositionCreated = true;

      this.workflow.destination.zenodo.bucket = response.links.bucket;
      this.workflow.destination.zenodo.deposition_id = response.id;
      this.workflow.destination.zenodo.originalDeposition = response;
      this.workflow.destination.zenodo.deposition = response;

      await this.datasetStore.updateCurrentDataset(this.dataset);
      await this.datasetStore.syncDatasets();

      await this.sleep(300);

      response = await this.addMetadaToZenodoDeposition();

      if (response === "ERROR") {
        this.statusMessage =
          "There was an error when adding metadata to the deposition";
        return "FAIL";
      } else {
        this.statusMessage =
          "Metadata successfully added to the Zenodo deposition";
      }

      this.percentage = 20;
      this.indeterminate = false;

      this.workflow.destination.zenodo.status.metadataAdded = true;

      await this.sleep(300);

      response = await this.checkForFoldersAndUpload();

      if (response === "ERROR") {
        this.statusMessage =
          "There was an error with uploading files to the Zenodo deposition";
        return "FAIL";
      } else {
        this.statusMessage = "Uploaded all files to Zenodo successfully.";
      }

      this.workflow.destination.zenodo.status.filesUploaded = true;

      return "SUCCESS";
    },
    codePresent() {
      if ("type" in this.workflow) {
        return this.workflow.type.includes("Code");
      }
      return false;
    },
  },
  async mounted() {
    this.dataset = await this.datasetStore.getCurrentDataset();
    this.workflow = this.dataset.workflows[this.workflowID];

    this.zenodoToken = await this.tokens.getToken("zenodo");
    // console.log(this.zenodoToken);

    this.statusMessage = "Preparing backend services...";
    await this.sleep(300);

    let response = await this.uploadWorkflow();

    if (response === "FAIL") {
      alert("Something went wrong. Please try again at a later time.");
      return;
    } else {
      const routerPath = `/datasets/${this.datasetID}/${this.workflowID}/zenodo/publish`;
      this.$router.push({ path: routerPath });
    }
  },
};
</script>

<style lang="postcss" scoped></style>
