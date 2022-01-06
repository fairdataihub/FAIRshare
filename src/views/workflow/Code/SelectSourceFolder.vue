<template>
  <div
    class="h-full w-full flex flex-col justify-center items-center pr-5 p-3 max-w-screen-xl"
  >
    <div class="flex flex-col h-full w-full">
      <span class="text-lg font-medium text-left">
        Where is your data located?
      </span>

      <el-divider class="my-4"> </el-divider>

      <div class="flex item-center justify-center gap-8 pr-[90px] pt-8">
        <div
          class="flex flex-col justify-evenly items-center p-4 shadow-md rounded-lg transition-all cursor-pointer h-[200px] w-[200px] single-check-box"
          :class="{ 'selected-repo': repoID === 'My computer' }"
          @click="selectRepo('My computer')"
        >
          <monitor class="h-24 w-16"></monitor>
          <span class="text-lg mx-5"> My computer </span>
        </div>

        <el-popover placement="bottom" trigger="hover" content="Coming soon...">
          <template #reference>
            <div>
              <div
                class="disabled-card flex flex-col justify-evenly items-center p-4 shadow-md rounded-lg transition-all cursor-pointer h-[200px] w-[200px] pointer-events-none text-stone-400 single-check-box"
              >
                <img
                  src="../../../assets/github.jpeg"
                  alt=""
                  class="h-24 w-full opacity-50"
                />
                <span class="text-lg mx-5"> On Github </span>
              </div>
            </div>
          </template>
        </el-popover>
      </div>

      <div class="flex flex-col w-full pt-20" v-if="repoID === 'My computer'">
        <span class="mb-2">
          Please select the folder where your
          {{ combineDataTypes }} files are stored.
        </span>

        <el-input
          v-model="folderPath"
          placeholder="Click here to select a folder"
          class="my-3 w-full"
          @click="selectFolderPath"
        />
      </div>

      <div
        class="w-full flex flex-row justify-center py-2 space-x-4 pt-8 pr-[61px]"
        v-if="repoID != ''"
      >
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
  data() {
    return {
      datasetStore: useDatasetsStore(),
      dataset: {},
      folderPath: "",
      folderDialogOpen: false,
      datasetID: this.$route.params.datasetID,
      workflowID: this.$route.params.workflowID,
      workflow: {},
      repoID: "",
    };
  },
  computed: {
    emptyInput() {
      if (this.folderPath.trim() === "") {
        return true;
      } else {
        return false;
      }
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
    selectRepo(repoID) {
      this.repoID = repoID;
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

      let that = this;
      // At this moment, add the same folder path to all the data types provided
      // subject to change when we separate the data types folder locations.
      dataTypes.forEach((type, _index) => {
        that.dataset.data[type].folderPath = that.folderPath;
      });

      this.workflow.sourceSelected = true;

      if ("source" in this.workflow) {
        this.workflow.source.type = this.repoID;
      } else {
        this.workflow.source = {
          type: this.repoID,
        };
      }

      this.datasetStore.updateCurrentDataset(this.dataset);
      this.datasetStore.syncDatasets();

      this.$router.push({
        path: `/datasets/${this.dataset.id}/${this.workflowID}/Code/reviewStandards`,
      });
    },
  },
  async mounted() {
    this.dataset = await this.datasetStore.getCurrentDataset();
    this.workflow = this.dataset.workflows[this.workflowID];
    console.log(this.workflow);

    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(1);

    // split this up when separate
    if (this.workflow.sourceSelected) {
      this.repoID = this.workflow.source.type;
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
  @apply transition-all flex justify-center items-center w-48 h-48;
}

.single-check-box:not(.disabled-card, .selected-repo):hover {
  @apply border border-secondary-500 shadow-lg shadow-secondary-500/50 transition-all;
}
</style>
