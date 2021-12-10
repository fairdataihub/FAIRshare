<template>
  <div class="h-full w-full flex flex-col justify-center items-center p-3 px-5">
    <div class="flex flex-col h-full w-full">
      <span class="font-medium text-left"> Split up data types </span>

      <span> Lets maximise the FAIRness of your data. </span>

      <el-divider> </el-divider>

      <p>
        When multiple data types are used in a single dataset, it is important
        to split up the data types into separate datasets to ensure that the
        relevant metadata for each data type is also present.
      </p>
      <!-- <p class="py-1">
        In order to do this, SODA will automatically try to group up similar
        data into their own datasets.
      </p> -->

      <line-divider> </line-divider>

      <p class="py-2">
        Based on your selections, we would suggest you split up your data into
        the following separate datasets:
      </p>

      <div class="flex flex-col divide-y-2 divide-gray-200 py-4">
        <el-descriptions :column="2" border class="py-4">
          <el-descriptions-item
            label="Data type"
            label-align="left"
            align="left"
          >
            Code
          </el-descriptions-item>
          <el-descriptions-item
            label="Repository destination"
            label-align="left"
            align="left"
          >
            Zenodo
          </el-descriptions-item>
        </el-descriptions>
        <!-- <el-descriptions :column="2" border title="Dataset 2" class="py-4">
          <el-descriptions-item
            label="Data type"
            label-align="left"
            align="left"
          >
            Code
          </el-descriptions-item>
          <el-descriptions-item
            label="Repository destination"
            label-align="left"
            align="left"
          >
            Zenodo
          </el-descriptions-item>
        </el-descriptions> -->
      </div>

      <!-- <div class="grid grid-cols-2 gap-4 py-4">
        <div
          class="
            w-full
            bg-white
            h-full
            border border-black-800
            mx-1
            rounded-lg
            relative
          "
        >
          <div class="w-1 h-20 bg-blue-600 absolute rounded-tl-md"></div>
          <h5 class="text-lg font-semibold px-6 pt-6 pb-2">Data Type: Code</h5>
          <p class="text-md font-regular p-6 pt-2 text-gray-500">
            Destination: Zenodo
          </p>
        </div>
      </div> -->

      <!-- <div class="grid grid-cols-3 gap-4">
        <div class="flex flex-col divide-y-2 p-4">
          <span class="font-bold p-2"> Code </span>
          <div class="flex flex-col">
            <span class="p-1"> Zenodo </span>
            <span class="p-1"> FigShare </span>
          </div>
        </div>
        <div class="flex flex-col divide-y-2 p-4">
          <span class="font-bold p-2"> Genomic Data </span>
          <div class="flex flex-col">
            <span class="p-1"> Zenodo </span>
            <span class="p-1"> FigShare </span>
          </div>
        </div>
      </div> -->

      <p class="text-center">
        SODA will help you split up your data into multiple datasets and add the
        relevant metadata to each dataset.
        <br />
        Do you want to continue?
      </p>

      <div class="w-full flex flex-row justify-center py-6">
        <router-link to="/datasets" class="mx-6 hidden">
          <el-button type="danger" plain> Cancel </el-button>
        </router-link>

        <el-button
          type="primary"
          class="flex flex-row items-center"
          @click="createWorkflows"
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

import { useDatasetsStore } from "../../store/datasets";

export default {
  name: "CreateNewProjectConfirm",
  components: { ArrowRightBold },
  data() {
    return {
      datasetStore: useDatasetsStore(),
      dataset: {},
      datasetID: this.$route.params.datasetID,
    };
  },
  methods: {
    createWorkflows() {
      const dataTypes = this.dataset.dataType;

      // do some logic here to split up by workflow.

      // right now its all unique workflows.
      this.dataset.workflows = {};

      let that = this;
      dataTypes.forEach((type, index) => {
        const key = `workflow${index + 1}`;
        that.dataset.workflows[key] = {};
        that.dataset.workflows[key].type = [type];
        that.dataset.workflows[key].folderSelected = false;
        that.dataset.workflows[key].destinationSelected = false;
        that.dataset.workflows[key].datasetUploaded = false;
        that.dataset.workflows[key].datasetPublished = false;
        that.dataset.workflows[key].destination = {
          name: "",
          questions: [],
        };
        that.dataset.workflows[key].expandOptions = [];
      });

      this.dataset.workflowConfirmed = true;

      this.datasetStore.updateCurrentDataset(this.dataset);
      this.datasetStore.syncDatasets();

      this.$router.push({ path: `/datasets/${this.datasetID}` });
    },
  },
  mounted() {
    this.datasetStore.getDataset(this.datasetID);
    this.dataset = this.datasetStore.currentDataset;

    this.datasetStore.hideProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(1);
  },
};
</script>
