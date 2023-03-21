<template>
  <div class="flex h-full w-full max-w-screen-xl flex-col items-center justify-center p-3 pr-5">
    <div class="flex h-full w-full flex-col">
      <span class="text-left text-lg font-medium">
        Provide the location of the files you want to include in your dataset
      </span>

      <line-divider />

      <span class="mb-2"> Where are your files located? </span>

      <div class="item-center flex justify-center gap-8 pt-8">
        <div
          class="single-check-box flex h-[200px] w-[200px] cursor-pointer flex-col items-center justify-evenly rounded-lg p-4 shadow-md transition-all"
          :class="{ 'selected-location': locationID === 'local' }"
          @click="selectSourceLocation('local')"
        >
          <monitor-icon class="h-24 w-16" />
          <span class="mx-5 text-lg"> My computer </span>
        </div>

        <!-- hidden for now. Will probably be replaced by another file storage location in the future -->
        <div class="hidden">
          <div
            class="single-check-box flex h-[200px] w-[200px] cursor-pointer flex-col items-center justify-evenly rounded-lg p-4 shadow-md transition-all"
            :class="{ 'selected-location': locationID === 'github' }"
            @click="selectSourceLocation('github')"
          >
            <img
              src="../../../assets/images/githublogo.jpeg"
              alt="GitHub logo"
              class="h-24 w-full"
            />
            <span class="mx-5 text-lg"> On GitHub </span>
          </div>
        </div>
      </div>

      <div class="flex w-full flex-col pt-20" v-if="locationID === 'local'">
        <span class="mb-2">
          Please select the folder where your
          <span class="font-medium"> Immunology </span>
          files are stored. It is highly recommended to include all your data files.
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
        <h3 class="text-center">Continue to select the repository you want to use.</h3>
      </div>

      <div class="flex w-full flex-row justify-center space-x-4 py-2 pt-8">
        <router-link :to="`/datasets/${datasetID}`" class="">
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
    <app-docs-link
      url="curate-and-share/select-local-folder"
      position="bottom-4"
      v-if="locationID === 'local'"
    />
    <app-docs-link
      url="curate-and-share/select-github-option"
      position="bottom-4"
      v-if="locationID === 'github'"
    />
  </div>
</template>

<script>
import { dialog } from "@electron/remote";

import { useDatasetsStore } from "@/store/datasets";

export default {
  name: "ImmunologySelectSourceFolder",
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
      locationID: "local",
    };
  },
  computed: {
    emptyInput() {
      if (this.locationID === "local") {
        if (this.folderPath === "" || this.folderPath === null || this.folderPath === undefined) {
          return true;
        }
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
  },
  methods: {
    selectSourceLocation(locationID) {
      this.locationID = locationID;
    },

    selectFolderPath() {
      if (!this.folderDialogOpen) {
        this.folderDialogOpen = true;
        dialog.showOpenDialog({ properties: ["openDirectory"] }).then((data) => {
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
        // At this moment, add the same folder path to all the data types provided in the workflow
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
          `/datasets/${this.datasetID}/${this.workflowID}/Immunology/selectGithubRepo`
        );
      } else {
        this.$router.push({
          path: `/datasets/${this.dataset.id}/${this.workflowID}/Immunology/reviewStandards`,
        });
      }
    },
  },
  async mounted() {
    this.dataset = await this.datasetStore.getCurrentDataset();
    this.workflow = this.dataset.workflows[this.workflowID];

    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("immport");
    this.datasetStore.setCurrentStep(1);

    this.workflow.currentRoute = this.$route.path;

    // split this up when separate
    if (this.workflow.sourceSelected) {
      this.locationID = this.workflow.source.type;
      this.folderPath = this.dataset.data[this.workflow.type[0]].folderPath;
    }
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
