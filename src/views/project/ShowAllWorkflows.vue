<template>
  <div class="flex h-screen w-full flex-row items-center justify-center">
    <div ref="" class="flex h-full flex-row items-center p-3">
      <div class="flex h-full flex-col overflow-y-auto">
        <span class="text-left font-medium"> Start the curation process </span>

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
          <div class="flex items-center justify-start bg-gray-200 px-4 py-2">
            <!-- <el-button
              type="primary"
              @click="navigateToCurate(`${key}`)"
              :disabled="workflow.datasetPublished"
            >
              Curate {{ combineDataTypes(workflow.type) }}
              <el-icon><arrow-right-bold /></el-icon>
            </el-button> -->
            <button
              class="primary-plain-button"
              @click="navigateToCurate(`${key}`)"
              :disabled="workflow.datasetPublished"
              ref="continueButton"
            >
              Curate {{ combineDataTypes(workflow.type) }}
              <el-icon><arrow-right-bold /></el-icon>
            </button>
            <br />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useDatasetsStore } from "@/store/datasets";

import { ElMessageBox } from "element-plus";

export default {
  name: "ShowAllWorkflows",

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
      let routerPath = "";

      if (
        "datasetUploaded" in this.dataset.workflows[workflowID] &&
        this.dataset.workflows[workflowID].datasetUploaded
      ) {
        ElMessageBox.confirm(
          "It looks like you have already uploaded this dataset to Zenodo but you haven't published it yet. Would you like to publish this now or create a new upload for this specific workflow?",
          "You haven't published this dataset yet",
          {
            confirmButtonText: "I want to publish",
            cancelButtonText: "I want to upload my data again",
            type: "info",
          }
        )
          .then(() => {
            routerPath = `/datasets/${this.datasetID}/${workflowID}/zenodo/publish`;
            this.$router.push({ path: routerPath });
          })
          .catch(() => {
            routerPath = `/datasets/${this.datasetID}/${workflowID}/Code/selectFolder`;
            this.$router.push({ path: routerPath });
          });
      } else {
        if ("currentRoute" in this.dataset.workflows[workflowID]) {
          if (
            this.dataset.workflows[workflowID].currentRoute != "" &&
            this.dataset.workflows[workflowID].currentRoute !=
              `/datasets/${this.datasetID}/${workflowID}/Code/selectFolder`
          ) {
            ElMessageBox.confirm(
              "It looks like you were working on this workflow before. Would you like to continue where you left off?",
              "Continue where you left off",
              {
                confirmButtonText: "Yes, continue",
                cancelButtonText: "No, start from the beginning",
                distinguishCancelAndClose: true,
                type: "info",
              }
            )
              .then(() => {
                routerPath = this.dataset.workflows[workflowID].currentRoute;
                this.$router.push({ path: routerPath });
              })
              .catch((action) => {
                if (action === "cancel") {
                  routerPath = `/datasets/${this.datasetID}/${workflowID}/Code/selectFolder`;
                  this.$router.push({ path: routerPath });
                }
              });
          } else {
            routerPath = `/datasets/${this.datasetID}/${workflowID}/Code/selectFolder`;
            this.$router.push({ path: routerPath });
          }
        } else {
          routerPath = `/datasets/${this.datasetID}/${workflowID}/Code/selectFolder`;
          this.$router.push({ path: routerPath });
        }
      }

      // if ("datasetUploaded" in this.dataset.workflows[workflowID]) {
      //   if (this.dataset.workflows[workflowID].datasetUploaded) {
      //     routerPath = `/datasets/${this.datasetID}/${workflowID}/zenodo/publish`;
      //   } else {
      //     routerPath = `/datasets/${this.datasetID}/${workflowID}/Code/selectFolder`;
      //   }
      // } else {
      //   routerPath = `/datasets/${this.datasetID}/${workflowID}/Code/selectFolder`;
      // }
      // console.log(routerPath);
      // this.$router.push({ path: routerPath });
    },
  },
  async mounted() {
    this.dataset = await this.datasetStore.getCurrentDataset();

    if (!this.dataset.workflowConfirmed) {
      this.$router.push({ path: `/datasets/new/${this.dataset.id}/confirm` });
    }

    this.navigateToCurate("workflow1");
  },
};
</script>
