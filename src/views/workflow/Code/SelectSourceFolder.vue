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

import { useDatasetsStore } from "@/store/datasets";

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
    };
  },
  computed: {
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
    selectSourceLocation(locationID) {
      this.locationID = locationID;
    },
    selectFolderPath() {
      if (!this.folderDialogOpen) {
        this.folderDialogOpen = true;
        dialog
          .showOpenDialog({ properties: ["openDirectory"] })
          .then((data) => {
            if (!data.canceled) {
              this.folderPath = data.filePaths[0];
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
      }

      if (this.locationID === "github") {
        if (!("github" in this.workflow)) {
          this.workflow.github = {};
        }
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
    console.log(this.workflow);

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
  @apply border-secondary-500 shadow-secondary-500/50 border shadow-lg transition-all;
}
</style>
