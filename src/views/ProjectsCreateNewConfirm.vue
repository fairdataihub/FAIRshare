<template>
  <div class="h-screen w-full flex flex-row lg:justify-center items-center">
    <div class="p-3 h-full flex flex-row items-center">
      <div class="h-full w-full">
        <div class="flex flex-col h-full overflow-y-auto">
          <span class="font-medium text-left"> SODA suggestions </span>

          <span>
            Based on your selected data types, this is what we suggest you
            should use for FAIR sharing of your data.
          </span>

          <el-divider> </el-divider>

          <span>
            We recommend the following repositories for your selected data
            types.
          </span>

          <div class="grid grid-cols-3 gap-4">
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
          </div>

          <span>
            SODA will automatically split up your data and upload it to the
            relevant repository. Do you want to continue?
          </span>

          <div class="w-full flex flex-row justify-center py-2">
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
    </div>
  </div>
</template>

<script>
// import { Icon } from "@iconify/vue";
import { ArrowRightBold } from "@element-plus/icons";

import { useDatasetsStore } from "../store/datasets";

export default {
  name: "ProjectsCreateNewConfirm",
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
        that.dataset.workflows[key].completed = false;
        that.dataset.workflows[key].folderSelected = false;
        that.dataset.workflows[key].destinationSelected = false;
        that.dataset.workflows[key].destination = {
          name: "",
          questions: [],
        };
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
  },
};
</script>
