<template>
  <div
    class="h-full w-full flex flex-col justify-center items-center pr-5 p-3 max-w-screen-xl"
  >
    <div class="flex flex-col h-full w-full">
      <span class="text-lg font-medium text-left">
        Where is your data located?
      </span>

      <el-divider class="my-4"> </el-divider>

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

      <div class="w-full flex flex-row justify-center py-2">
        <router-link :to="`/datasets/${datasetID}`" class="mx-6">
          <el-button type="danger" plain> Back </el-button>
        </router-link>

        <el-button
          type="primary"
          :disabled="emptyInput"
          class="flex flex-row items-center"
          @click="startCuration"
          id="continue"
        >
          Continue
          <el-icon>
            <ArrowRightBold />
          </el-icon>
        </el-button>
      </div>
    </div>
  </div>
</template>

<script>
// import { Icon } from "@iconify/vue";
import { ArrowRightBold } from "@element-plus/icons";
import { dialog } from "@electron/remote";

import { useDatasetsStore } from "../../store/datasets";

export default {
  name: "SelectSourceFolder",
  components: { ArrowRightBold },
  data() {
    return {
      datasetStore: useDatasetsStore(),
      dataset: {},
      folderPath: "",
      datasetID: this.$route.params.datasetID,
      workflowID: this.$route.params.workflowID,
      workflow: {},
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
    selectFolderPath() {
      dialog.showOpenDialog({ properties: ["openDirectory"] }).then((data) => {
        if (!data.canceled) {
          this.folderPath = data.filePaths[0];
        }
      });
    },
    startCuration() {
      const dataTypes = this.workflow.type;

      let that = this;
      // At this moment, add the same folder path to all the data types provided
      // subject to change when we separate the data types folder locations.
      dataTypes.forEach((type, _index) => {
        that.dataset.data[type].folderPath = that.folderPath;
      });

      this.workflow.folderSelected = true;

      this.datasetStore.updateCurrentDataset(this.dataset);
      this.datasetStore.syncDatasets();

      // console.log(
      //   `/datasets/${this.dataset.id}/${this.workflowID}/createMetadata`
      // );

      this.$router.push({
        path: `/datasets/${this.dataset.id}/${this.workflowID}/createMetadata`,
      });
    },
  },
  async mounted() {
    this.dataset = await this.datasetStore.getCurrentDataset();
    this.workflow = this.dataset.workflows[this.workflowID];

    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(1);

    // split this up when separate
    if (this.workflow.folderSelected) {
      this.folderPath = this.dataset.data[this.workflow.type[0]].folderPath;
    }

    // if (this.workflow.folderPath) {
    //   this.folderPath = this.workflow.folderPath;
    // }
  },
};
</script>
