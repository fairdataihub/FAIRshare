<template>
  <div class="flex h-full w-full flex-col items-center justify-center p-3 pr-5">
    <div class="flex h-full w-full flex-col">
      <span class="text-left text-lg font-medium">
        Let's upload all your files to the correct places.
      </span>
      <span class="text-left">
        This one is on us. We're working hard to get your files up to GitHub and your dataset to
        Figshare.
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
        <div class="flex flex-row items-start justify-start py-3" v-else>
          <LoadingCubeGrid class="h-5 w-5" v-if="percentage !== 100"></LoadingCubeGrid>

          <div class="flex flex-col items-start">
            <p class="pl-4">
              {{ statusMessage }}
              <LoadingEllipsis v-if="percentage !== 100"></LoadingEllipsis>
            </p>
            <p class="whitespace-pre pl-4 text-sm">
              {{ subStatusMessage }}
              <LoadingEllipsis v-if="subStatusMessage !== ' '"></LoadingEllipsis>
            </p>
          </div>
        </div>
        <div class="pt-2 pl-2" v-if="errorMessage != ''">
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
import path from "path";
import fs from "fs-extra";
// import klawSync from "klaw-sync";

import LoadingCubeGrid from "@/components/spinners/LoadingCubeGrid.vue";
import LoadingEllipsis from "@/components/spinners/LoadingEllipsis.vue";

import { useDatasetsStore } from "@/store/datasets";
import { useTokenStore } from "@/store/access.js";

import figshareMetadataOptions from "@/assets/supplementalFiles/figshareMetadataOptions.json";

export default {
  name: "GithubFigshareUpload",
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
      figshareToken: "",
      statusMessage: "some status message here",
      subStatusMessage: " ",
      errorMessage: "",
      showAlert: false,
      alertTitle: "",
      alertMessage: "",
      licenseOptions: figshareMetadataOptions.licenseOptions,
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
    async createFigshareDeposition() {
      this.errorMessage = "";
      this.statusMessage = "Creating a metadata object for the Figshare deposition";
      await this.sleep(300);

      const figshareMetadata = this.workflow.destination.figshare.questions;
      let metadata = {};

      if ("uploadType" in figshareMetadata && figshareMetadata.uploadType != "") {
        metadata.defined_type = figshareMetadata.uploadType;
      }

      if ("title" in figshareMetadata && figshareMetadata.title != "") {
        metadata.title = figshareMetadata.title;
      }

      if ("description" in figshareMetadata && figshareMetadata.description != "") {
        metadata.description = figshareMetadata.description;
      }

      if ("authors" in figshareMetadata) {
        metadata.authors = [];
        figshareMetadata.authors.forEach((author) => {
          const creatorObject = {};

          creatorObject.first_name = author.givenName;
          creatorObject.last_name = author.familyName;

          if (author.email != "") {
            creatorObject.email = author.email;
          }

          if (author.orcid !== "") {
            creatorObject.orcid = author.orcid;
          }

          metadata.authors.push(creatorObject);
        });
      }

      if ("categories" in figshareMetadata && figshareMetadata.categories.length > 0) {
        metadata.categories = figshareMetadata.categories;

        if (process.env.NODE_ENV === "development") {
          // A random category from the dev environment for testing
          metadata.categories = [26200];
        }
      }

      if ("keywords" in figshareMetadata && figshareMetadata.keywords.length > 0) {
        metadata.keywords = [];
        figshareMetadata.keywords.forEach((keyword) => {
          metadata.keywords.push(keyword.keyword);
        });
      }

      if ("references" in figshareMetadata && figshareMetadata.references.length > 0) {
        metadata.references = [];
        figshareMetadata.references.forEach((reference) => {
          metadata.references.push(reference.reference);
        });
      }

      if ("funding" in figshareMetadata) {
        metadata.funding_list = [];
        figshareMetadata.funding.forEach((funder) => {
          const funderObject = {};

          funderObject.title = funder.funding;

          metadata.funding_list.push(funderObject);
        });
      }

      if ("license" in figshareMetadata) {
        if ("licenseName" in figshareMetadata.license) {
          const licenseObject = await this.licenseOptions.find(
            (license) => license.licenseId === figshareMetadata.license.licenseName
          );

          metadata.license = licenseObject.id;
        }
      }

      this.statusMessage = "Created a metadata object successfully";
      await this.sleep(300);

      this.percentage = 4;
      this.indeterminate = false;

      this.statusMessage = "Creating an article shell on Figshare";
      await this.sleep(300);

      metadata = JSON.stringify(metadata);

      return axios
        .post(`${this.$server_url}/figshare/item`, {
          access_token: this.figshareToken,
          metadata,
        })
        .then((response) => {
          this.$track("Figshare", "Create empty deposition", "success");
          return response.data;
        })
        .catch((error) => {
          this.$track("Figshare", "Create empty deposition", "failed");
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
            access_token: this.figshareToken,
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
    async checkUploadStatus() {
      const response = await axios
        .get(`${this.$server_url}/figshare/item/files/upload`, {})
        .then((response) => {
          return response.data;
        })
        .catch((error) => {
          console.error(error);
          return JSON.stringify({ status: "ERROR", message: "error" });
        });

      if (response !== "" || response !== "ERROR") {
        this.subStatusMessage = response;
      }

      return;
    },
    async uploadToFigshare(article_id, file_path) {
      this.statusMessage = `Uploading ${path.basename(file_path)} to Figshare`;
      await this.sleep(100);

      this.subStatusMessage = " ";
      let interval = setInterval(() => {
        this.checkUploadStatus();
      }, 500);

      const response = await axios
        .post(`${this.$server_url}/figshare/item/files/upload`, {
          access_token: this.figshareToken,
          article_id,
          file_path,
        })
        .then((response) => {
          this.$track("Figshare", "Uploaded file to Figshare", "success");
          return response.data;
        })
        .catch((error) => {
          this.$track("Figshare", "Uploaded file to Figshare", "failed");
          console.error(error);
          return "ERROR";
        });

      clearInterval(interval);
      this.subStatusMessage = " ";

      this.statusMessage = `Uploaded ${path.basename(file_path)} to Figshare successfully`;
      await this.sleep(300);
      return response;
    },
    async uploadDatasetToFigshare() {
      this.statusMessage = "Checking folder path";
      await this.sleep(300);

      const folderPath = this.dataset.data.Code.folderPath;

      this.statusMessage = "Getting ready to upload dataset to Figshare";
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
        const response = await this.uploadToFigshare(
          this.workflow.destination.figshare.article_id,
          file
        );

        if (response === "ERROR") {
          return "ERROR";
        }

        this.percentage = ((index + 1) / contents.length) * 60 + 40;
        this.percentage = Math.round(this.percentage);
      }

      this.statusMessage = "Uploaded all files to Figshare successfully";
      await this.sleep(300);

      this.percentage = 100;
      this.indeterminate = false;

      return "SUCCESS";
    },
    async uploadWorkflow() {
      let response = {};

      if (this.workflow.destination.figshare.newVersion) {
        this.statusMessage = "Creating a new version of the Zenodo Deposition";

        await this.sleep(300);

        const original_deposition_id = this.workflow.destination.zenodo.selectedDeposition.id;

        let res = null;

        res = await axios
          .post(`${this.$server_url}/zenodo/deposition/newversion`, {
            access_token: this.figshareToken,
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
              access_token: this.figshareToken,
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
                access_token: this.figshareToken,
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
        response = await this.createFigshareDeposition();
        console.log(response);
        response = JSON.parse(response);

        if ("status" in response && response.status === "ERROR") {
          this.alertMessage = "There was an error with creating the deposition on Figshare";
          this.errorMessage = response.message;
          return "FAIL";
        } else {
          this.statusMessage = "Article shell created on Figshare";
        }
      }

      this.percentage = 5;
      this.indeterminate = false;

      await this.sleep(300);

      this.workflow.destination.figshare.status.depositionCreated = true;

      const responseObject = response;

      this.workflow.destination.figshare.article_id = responseObject.article_id;
      this.workflow.destination.figshare.doi = responseObject.doi;

      await this.datasetStore.updateCurrentDataset(this.dataset);
      await this.datasetStore.syncDatasets();

      await this.sleep(300);

      // create codemeta.json
      if (this.workflow.generateCodeMeta) {
        if (this.codePresent) {
          this.dataset.data.Code.questions.identifier = responseObject.doi;

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
        response = await this.uploadDatasetToFigshare();
      }

      if (response === "ERROR") {
        this.alertMessage = "There was an error with uploading the dataset to Figshare";
        return "FAIL";
      } else {
        this.statusMessage = "Uploaded the dataset to Figshare successfully";
      }

      if (this.workflow.uploadToRepo) {
        this.workflow.destination.figshare.status.filesUploaded = true;
      }

      this.percentage = 100;
      this.indeterminate = false;

      return "SUCCESS";
    },
    async deleteDraftFigshareArticle() {
      if ("article_id" in this.workflow.destination.figshare) {
        const response = await axios
          .delete(`${this.$server_url}/figshare/item`, {
            data: {
              access_token: this.figshareToken,
              article_id: this.workflow.destination.figshare.article_id,
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

        this.deleteDraftFigshareArticle();

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

      const routerPath = `/datasets/${this.datasetID}/${this.workflowID}/figshare/publish`;

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

    const figshareTokenObject = await this.tokens.getToken("figshare");
    this.figshareToken = figshareTokenObject.token;

    const tempFolderPath = await this.resetTempFolder();

    this.dataset.data.Code.folderPath = tempFolderPath;

    this.runUploadWorkflow();
  },
};
</script>
