<template>
  <div
    class="flex h-full w-full max-w-screen-xl flex-col items-center justify-center p-3 pr-5"
  >
    <div class="flex h-full w-full flex-col">
      <span class="text-left text-lg font-medium">
        Provide the location of the files you want to include in your research
        software dataset
      </span>

      <el-divider class="my-4"> </el-divider>
      <span class="mb-2">
        Where are your research software files located?
      </span>
      <div class="item-center flex justify-center gap-8 pt-8">
        <div
          class="single-check-box flex h-[200px] w-[200px] cursor-pointer flex-col items-center justify-evenly rounded-lg p-4 shadow-md transition-all"
          :class="{ 'selected-location': locationID === 'local' }"
          @click="selectSourceLocation('local')"
        >
          <monitor-icon class="h-24 w-16" />
          <span class="mx-5 text-lg"> My computer </span>
        </div>

        <div>
          <div
            class="single-check-box flex h-[200px] w-[200px] cursor-pointer flex-col items-center justify-evenly rounded-lg p-4 shadow-md transition-all"
            :class="{ 'selected-location': locationID === 'github' }"
            @click="selectSourceLocation('github')"
          >
            <img
              src="../../../assets/images/githublogo.jpeg"
              alt=""
              class="h-24 w-full"
            />
            <span class="mx-5 text-lg"> On GitHub </span>
          </div>
        </div>
      </div>

      <div class="flex w-full flex-col pt-20" v-if="locationID === 'local'">
        <span class="mb-2">
          Please select the folder where your
          {{ combineDataTypes }} files are stored.
        </span>

        <el-input
          v-model="folderPath"
          placeholder="Click here to select a folder"
          class="my-3 w-full"
          size="large"
          @click="selectFolderPath"
        />
      </div>

      <div class="flex w-full flex-col pt-20" v-if="locationID === 'github'">
        <h3 class="text-center">
          Continue to select the repository you want to use.
        </h3>
      </div>

      <div class="flex w-full flex-row justify-center space-x-4 py-2 pt-8">
        <router-link :to="`/datasets/${datasetID}/landing`" class="">
          <button class="primary-plain-button">
            <el-icon><d-arrow-left /></el-icon> Back
          </button>
        </router-link>

        <button
          class="primary-button"
          :disabled="emptyInput"
          @click="startCuration"
          id="continue"
          v-if="locationID != ''"
        >
          Continue
          <el-icon> <d-arrow-right /> </el-icon>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { dialog } from "@electron/remote";
import axios from "axios";
import { useDatasetsStore } from "@/store/datasets";
import { v4 as uuidv4 } from "uuid";
export default {
  name: "CodeSelectSourceFolder",
  components: {},
  data() {
    return {
      datasetStore: useDatasetsStore(),
      dataset: {},
      folderPath: "",
      folderDialogOpen: false,
      datasetID: this.$route.params.datasetID,
      workflowID: this.$route.params.workflowID,
      workflow: {},
      locationID: "",
      step1Form: {
        name: "",
        description: "",
        creationDate: "",
        firstReleaseDate: "",
      },
      step2Form: {
        authors: [],
        contributors: [],
      },
      step3Form: {
        applicationCategory: "",
        keywords: [],
        funding: {
          code: "",
          organization: "",
        },
      },
      step4Form: {
        codeRepository: "",
        continuousIntegration: "",
        issueTracker: "",
        relatedLinks: [],
      },
      step5Form: {
        programmingLanguage: [],
        runtimePlatform: [],
        operatingSystem: [],
        otherSoftwareRequirements: [],
      },
      step6Form: {
        currentVersion: "",
        currentVersionReleaseDate: "",
        currentVersionDownloadLink: "",
        currentVersionReleaseNotes: "",
      },
      step7Form: {
        referencePublication: "",
        developmentStatus: "",
        isPartOf: "",
      },
    };
  },
  computed: {
    codePresent() {
      if ("type" in this.workflow) {
        return this.workflow.type.includes("Code");
      }
      return false;
    },
    emptyInput() {
      if (this.locationID === "local") {
        if (this.folderPath.trim() === "") {
          return true;
        } else {
          return false;
        }
      }
      if (this.locationID === "github") {
        return false;
      }
      return true;
    },
    combineDataTypes() {
      if ("type" in this.workflow) {
        const dataTypes = this.workflow.type;

        if (dataTypes.length === 1) {
          return dataTypes[0];
        } else if (dataTypes.length === 2) {
          return `${dataTypes[0]} and ${dataTypes[1]}`;
        } else if (dataTypes.length > 2) {
          let returnString = "";
          dataTypes.forEach((type, index) => {
            if (index === dataTypes.length - 1) {
              returnString += `and ${type}`;
            } else {
              returnString += `${type}, `;
            }
          });
          return returnString;
        }
      }

      return "";
    },
  },
  methods: {
    async fileExistInFolder(dir, target) {
      const response = await axios
        .post(`${this.$server_url}/utilities/fileexistinfolder`, {
          folder_path: dir,
          file_name: target,
        })
        .then((response) => {
          return response.data;
        })
        .catch((error) => {
          console.log(error);
          return "ERROR";
        });
      return response;
    },

    selectSourceLocation(locationID) {
      this.locationID = locationID;
    },
    addIds(array) {
      array.forEach((element) => {
        element.id = uuidv4();
      });
    },
    async updateDataset(target) {
      /* eslint-disable */
      console.log(target.description);
      this.step1Form.name = target.name;
      this.step1Form.description = target.description;
      this.step1Form.creationDate = target.creationDate;
      this.step1Form.firstReleaseDate = target.firstReleaseDate;

      this.step2Form.authors = target.author;
      this.step2Form.authors.forEach((element) => {
        delete element["@type"];
        delete element["@id"];
        element.affiliation = element.affiliation.name;
        element.orcid = "";
      });
      this.step2Form.contributors = target.contributor;
      this.step2Form.contributors.forEach((element) => {
        delete element["@type"];
        delete element["@id"];
        element.affiliation = element.affiliation.name;
        element.orcid = "";
      });
      this.addIds(this.step2Form.authors);
      this.addIds(this.step2Form.contributors);

      this.step3Form.applicationCategory = target.applicationCategory;
      target.keywords.forEach((element) => {
        this.step3Form.keywords.push({ keyword: element, id: uuidv4() });
      });
      this.step3Form.funding.organization = target.funding["@name"];

      this.step4Form.codeRepository = target.codeRepository;
      this.step4Form.continuousIntegration = target.contIntegration;
      this.step4Form.issueTracker = target.issueTracker;
      target.relatedLink.forEach((element) => {
        this.step4Form.relatedLinks.push({ link: element, id: uuidv4() });
      });

      this.step5Form.programmingLanguage = target.programmingLanguage;
      this.step5Form.runtimePlatform = target.runtimePlatform;
      this.step5Form.operatingSystem = target.operatingSystem;
      target.softwareRequirements.forEach((element) => {
        this.step5Form.otherSoftwareRequirements.push({
          link: element,
          id: uuidv4(),
        });
      });

      this.step6Form.currentVersion = target.version;
      this.step6Form.currentVersionReleaseDate = "";
      this.step6Form.currentVersionDownloadLink = target.downloadUrl;
      this.step6Form.currentVersionReleaseNotes = target.releaseNotes;

      this.step7Form.referencePublication = target.referencePublication;
      this.step7Form.developmentStatus = target.developmentStatus;
      this.step7Form.isPartOf = target.isPartOf;
      await this.saveCurrentEntries();
      console.log(this.dataset);
    },
    filterArrayOfObjects(array, key) {
      return array.filter((element) => {
        return element[key] !== "";
      });
    },
    async saveCurrentEntries() {
      this.dataset.data.general.questions.name = this.step1Form.name;
      this.dataset.data.general.questions.description =
        this.step1Form.description;

      this.step3Form.keywords = this.filterArrayOfObjects(
        this.step3Form.keywords,
        "keyword"
      );

      this.dataset.data.general.questions.keywords = this.step3Form.keywords;
      this.dataset.data.general.questions.authors = this.step2Form.authors;
      this.dataset.data.general.questions.contributors =
        this.step2Form.contributors;
      this.dataset.data.general.questions.funding = this.step3Form.funding;
      this.dataset.data.general.questions.referencePublication =
        this.step7Form.referencePublication;

      this.step4Form.relatedLinks = this.filterArrayOfObjects(
        this.step4Form.relatedLinks,
        "link"
      );

      this.step5Form.otherSoftwareRequirements = this.filterArrayOfObjects(
        this.step5Form.otherSoftwareRequirements,
        "link"
      );

      if (this.codePresent) {
        let codeForm = {};

        codeForm.name = this.step1Form.name;
        codeForm.description = this.step1Form.description;
        codeForm.creationDate = this.step1Form.creationDate;
        codeForm.firstReleaseDate = this.step1Form.firstReleaseDate;

        codeForm.authors = this.step2Form.authors;
        codeForm.contributors = this.step2Form.contributors;

        codeForm.keywords = this.step3Form.keywords;
        codeForm.funding = this.step3Form.funding;
        codeForm.applicationCategory = this.step3Form.applicationCategory;

        codeForm.codeRepository = this.step4Form.codeRepository;
        codeForm.continuousIntegration = this.step4Form.continuousIntegration;
        codeForm.issueTracker = this.step4Form.issueTracker;
        codeForm.relatedLinks = this.step4Form.relatedLinks;

        codeForm.programmingLanguage = this.step5Form.programmingLanguage;
        codeForm.runtimePlatform = this.step5Form.runtimePlatform;
        codeForm.operatingSystem = this.step5Form.operatingSystem;
        codeForm.otherSoftwareRequirements =
          this.step5Form.otherSoftwareRequirements;

        codeForm.currentVersion = this.step6Form.currentVersion;
        codeForm.currentVersionReleaseDate =
          this.step6Form.currentVersionReleaseDate;
        codeForm.currentVersionDownloadLink =
          this.step6Form.currentVersionDownloadLink;
        codeForm.currentVersionReleaseNotes =
          this.step6Form.currentVersionReleaseNotes;

        codeForm.referencePublication = this.step7Form.referencePublication;
        codeForm.developmentStatus = this.step7Form.developmentStatus;
        codeForm.isPartOf = this.step7Form.isPartOf;

        this.dataset.data.Code.questions = codeForm;
      }
      await this.datasetStore.updateCurrentDataset(this.dataset);
      await this.datasetStore.syncDatasets();
    },
    selectFolderPath() {
      if (!this.folderDialogOpen) {
        this.folderDialogOpen = true;
        dialog
          .showOpenDialog({ properties: ["openDirectory"] })
          .then(async (data) => {
            if (!data.canceled) {
              this.folderPath = data.filePaths[0];
              /* eslint-disable */
              let check = await this.fileExistInFolder(
                this.folderPath,
                "codemeta.json"
              );
              if (check != "Not Found") {
                this.updateDataset(check);
              }
            }
            this.folderDialogOpen = false;
          });
      }
    },
    startCuration() {
      const dataTypes = this.workflow.type;

      if (this.locationID === "local") {
        // At this moment, add the same folder path to all the data types provided
        // subject to change when we separate the data types folder locations.
        dataTypes.forEach((type, _index) => {
          this.dataset.data[type].folderPath = this.folderPath;
        });

        if (!("meta" in this.dataset)) {
          this.dataset.meta = {};
        }

        this.dataset.meta.location = "local";
        this.dataset.meta.locationPath = this.folderPath;
      }

      if (this.locationID === "github") {
        if (!("github" in this.workflow)) {
          this.workflow.github = {};
        }

        if (!("meta" in this.dataset)) {
          this.dataset.meta = {};
        }

        this.dataset.meta.location = "github";
        this.dataset.meta.locationPath = "";
      }

      this.workflow.sourceSelected = true;

      if ("source" in this.workflow) {
        this.workflow.source.type = this.locationID;
      } else {
        this.workflow.source = {
          type: this.locationID,
        };
      }

      this.datasetStore.updateCurrentDataset(this.dataset);
      this.datasetStore.syncDatasets();

      if (this.locationID === "github") {
        this.$router.push(
          `/datasets/${this.datasetID}/${this.workflowID}/Code/selectGithubRepo`
        );
      } else {
        this.$router.push({
          path: `/datasets/${this.dataset.id}/${this.workflowID}/Code/reviewStandards`,
        });
      }
    },
  },
  async mounted() {
    this.dataset = await this.datasetStore.getCurrentDataset();
    this.workflow = this.dataset.workflows[this.workflowID];

    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(1);

    this.workflow.currentRoute = this.$route.path;

    // split this up when separate
    if (this.workflow.sourceSelected) {
      this.locationID = this.workflow.source.type;
      this.folderPath = this.dataset.data[this.workflow.type[0]].folderPath;
    }

    // console.log(this.dataset.data[this.workflow.type[0]].folderPath);

    // if (this.workflow.folderPath) {
    //   this.folderPath = this.workflow.folderPath;
    // }
  },
};
</script>
<style scoped>
.single-check-box {
  @apply flex h-48 w-48 items-center justify-center transition-all;
}

.single-check-box:not(.disabled-card, .selected-repo):hover {
  @apply border border-secondary-500 shadow-lg shadow-secondary-500/50 transition-all;
}
</style>
