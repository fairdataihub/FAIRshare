<template>
  <div class="h-screen w-full flex flex-row justify-center items-center">
    <div ref="" class="p-3 h-full flex flex-row items-center">
      <div ref="" class="h-full w-full">
        <div class="flex flex-col h-full overflow-y-auto">
          <span class="font-medium text-left">
            Start the curation process
          </span>

          <span class="">
            When you are ready, click on the curation buttons below to fill out
            some metadata information.
          </span>

          <el-divider> </el-divider>

          <div
            class="flex flex-col p-2"
            v-for="(workflow, key) in dataset.workflows"
            :key="key"
          >
            <div class="bg-gray-300 px-4 py-2">
              <span class="text-lg">
                {{ combineDataTypes(workflow.type) }}
              </span>
            </div>
            <div class="bg-gray-200 px-4 py-2">
              <el-button
                type="primary"
                @click="navigateToCurate(`${key}`)"
                :disabled="workflow.completed"
              >
                Curate {{ combineDataTypes(workflow.type) }}
                <el-icon>
                  <ArrowRightBold />
                </el-icon>
              </el-button>
              <br />
              <span>{{ workflow }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import { Icon } from "@iconify/vue";
import { ArrowRightBold } from "@element-plus/icons";

import { useDatasetsStore } from "../../store/datasets";

export default {
  name: "ShowAllWorkflows",
  components: { ArrowRightBold },
  data() {
    return {
      datasetStore: useDatasetsStore(),
      dataset: {},
      currentOptions: {},
      datasetID: this.$route.params.datasetID,
    };
  },
  methods: {
    combineDataTypes(dataTypes) {
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
    },
    navigateToCurate(workflowID) {
      this.datasetStore.updateCurrentDataset(this.dataset);

      const routerPath = `/datasets/${this.datasetID}/${workflowID}/selectFolder`;
      console.log(routerPath);
      this.$router.push({ path: routerPath });
    },
  },
  mounted() {
    this.dataset = this.datasetStore.currentDataset;

    if (!this.dataset.workflowConfirmed) {
      this.$router.push({ path: `/datasets/new/${this.dataset.id}/confirm` });
    }
  },
};
</script>
