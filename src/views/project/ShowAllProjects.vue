<template>
  <div
    class="h-full w-full flex flex-row items-center"
    :class="{ 'justify-center': datasetStore.datasetCount === 0 }"
  >
    <div
      class="px-3 h-full flex flex-row items-center"
      :class="{ 'w-full': datasetStore.datasetCount > 0 }"
    >
      <div
        class="h-full w-full flex flex-col"
        v-if="datasetStore.datasetCount > 0"
      >
        <!-- <div class="flex flex-col h-full"> -->
        <span class="font-medium"> Continue curating your datasets </span>

        <span>
          You have some unpublished projects. Do you want to continue working on
          these items?
        </span>

        <!-- <el-divider> </el-divider> -->

        <div class="flex-grow h-full overflow-y-auto">
          <div>
            <el-divider content-position="left">
              Projects currently in progress
            </el-divider>

            <div class="divide-y divide-gray-200 px-4">
              <div
                v-for="dataset in datasetsInProgress"
                :key="dataset"
                class="flex flex-row justify-between items-center w-full p-3 hover:bg-gray-100 transition-all cursor-pointer"
                :class="{ 'selected-project': dataset.id === selectedDataset }"
                @click="selectDataset($event, dataset.id)"
              >
                <!-- @click="navigateToDataset(`${dataset.id}`)" -->
                <div class="flex flex-row items-center">
                  <img :src="dataset.image" alt="" class="w-20" />
                  <div class="flex flex-col px-4">
                    <span class="text-md font-medium">
                      {{ dataset.name }}
                    </span>
                    <p class="text-sm line-clamp-4">
                      {{ dataset.description }}
                    </p>
                  </div>
                </div>
                <div class="items-center ml-2 hidden">
                  <Icon icon="ic:round-navigate-next" class="h-8 w-8" />
                </div>
              </div>
            </div>
          </div>

          <div class="mt-5" v-if="datasetsPublished.length > 0">
            <el-divider content-position="left">
              Fully published projects
            </el-divider>

            <div class="divide-y divide-gray-200 px-4">
              <div
                v-for="dataset in datasetsPublished"
                :key="dataset"
                class="flex flex-row justify-between items-center w-full p-3 hover:bg-gray-100 transition-all cursor-pointer"
                :class="{ 'selected-project': dataset.id === selectedDataset }"
                @click="selectDataset($event, dataset.id)"
              >
                <!-- @click="navigateToDataset(`${dataset.id}`)" -->
                <div class="flex flex-row items-center">
                  <img :src="dataset.image" alt="" class="w-20" />
                  <div class="flex flex-col px-4">
                    <span class="text-md font-medium">
                      {{ dataset.name }}
                    </span>
                    <p class="text-sm line-clamp-4">
                      {{ dataset.description }}
                    </p>
                  </div>
                </div>
                <div class="items-center ml-2 hidden">
                  <Icon icon="ic:round-navigate-next" class="h-8 w-8" />
                </div>
              </div>
            </div>
          </div>
        </div>

        <el-divider> </el-divider>

        <div class="flex flex-row justify-between mb-5">
          <router-link to="/datasets/new">
            <div
              class="flex flex-row items-center w-max text-purple-800 cursor-pointer hover-underline-animation py-3"
            >
              <span class="font-medium"> Or start from an empty project </span>
              <Icon icon="grommet-icons:form-next-link" class="ml-2 h-5 w-5" />
            </div>
          </router-link>
          <div class="flex flex-row" v-if="selectedDataset !== ''">
            <el-button type="info" plain @click="editProject">
              Edit project details
            </el-button>
            <el-button
              type="primary"
              plain
              class="flex flex-row items-center"
              @click="startCuratingProject"
            >
              Start curating this dataset
              <el-icon>
                <ArrowRightBold />
              </el-icon>
            </el-button>
          </div>
        </div>
        <!-- </div> -->
      </div>
      <div class="flex flex-row justify-center items-center p-10" v-else>
        <router-link to="/datasets/new">
          <div
            class="flex flex-col justify-center items-center border-2 border-dashed hover:border-solid w-max p-10 rounded-lg hover:bg-gray-100 transition-all cursor-pointer"
          >
            <Icon
              icon="fluent:quiz-new-24-regular"
              class="h-20 w-10/12 text-gray-700"
            />
            <span class="font-medium text-large"> Create a new dataset </span>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { Icon } from "@iconify/vue";
import { ArrowRightBold } from "@element-plus/icons";

import { useDatasetsStore } from "../../store/datasets";

export default {
  name: "ShowAllProjects",
  components: { Icon, ArrowRightBold },

  data() {
    return {
      datasetStore: useDatasetsStore(),
      selectedDataset: "",
      datasetsInProgress: [],
      datasetsPublished: [],
    };
  },
  computed: {},
  methods: {
    selectDataset(event, datasetID) {
      if (datasetID === this.selectedDataset) {
        this.selectedDataset = "";
      } else {
        this.selectedDataset = datasetID;
      }

      if (event && event.detail === 2) {
        this.selectedDataset = "";
        this.navigateToDataset(datasetID);
      }
    },
    startCuratingProject() {
      this.navigateToDataset(this.selectedDataset);
    },
    async editProject() {
      await this.datasetStore.getDataset(this.selectedDataset);
      const routerPath = `/datasets/${this.selectedDataset}/edit`;
      this.$router.push({ path: routerPath });
    },
    async navigateToDataset(datasetID) {
      let routerPath;

      await this.datasetStore.getDataset(datasetID);

      routerPath = `/datasets/${datasetID}`;
      // routerPath = `/datasets/new/${datasetID}/confirm`;
      // routerPath = `/datasets/${datasetID}/workflow1/zenodo/metadata`;
      // routerPath = `/datasets/${datasetID}/workflow1/zenodo/review`;
      // routerPath = `/datasets/${datasetID}/workflow1/createMetadata`;
      // routerPath = `/datasets/${datasetID}/workflow1/zenodo/accessToken`;
      // routerPath = `/datasets/${datasetID}/workflow1/zenodo/publish`;

      this.$router.push({ path: routerPath });
    },
  },
  async mounted() {
    this.datasetStore.hideProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(1);

    let test = await this.datasetStore.getAllDatasets();

    // make a local copy of the datasets object
    const datasets = JSON.parse(JSON.stringify(test));

    // filter datasets in progress
    let datasetsInProgressIDs = [];

    for (const key in datasets) {
      if ("workflows" in datasets[key]) {
        for (const workflow in datasets[key].workflows) {
          if (!("datasetPublished" in datasets[key].workflows[workflow])) {
            datasetsInProgressIDs.push(key);
          } else {
            if (
              "datasetPublished" in datasets[key].workflows[workflow] &&
              !datasets[key].workflows[workflow].datasetPublished
            ) {
              datasetsInProgressIDs.push(key);
            }
          }
        }
      } else {
        datasetsInProgressIDs.push(key);
      }
    }

    // remove duplicates from array
    datasetsInProgressIDs = [...new Set(datasetsInProgressIDs)];

    // filter datasets that are in progress based on the IDs
    for (const datasetID of datasetsInProgressIDs) {
      this.datasetsInProgress.push(datasets[datasetID]);
    }

    // get list of all IDs
    let datasetIDs = [];
    for (const key in datasets) {
      datasetIDs.push(key);
    }

    // get the difference of array of datasetIds
    let datasetsPublishedIDs = datasetIDs.filter(
      (datasetID) => !datasetsInProgressIDs.includes(datasetID)
    );

    // filter datasets that are published based on the IDs
    for (const datasetID of datasetsPublishedIDs) {
      this.datasetsPublished.push(datasets[datasetID]);
    }
  },
};
</script>

<style lang="postcss" scoped>
.selected-project {
  background-color: #e0dede;
}
</style>
