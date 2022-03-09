<template>
  <div
    class="flex h-full w-full flex-row items-center"
    :class="{ 'justify-center': datasetStore.datasetCount === 0 }"
  >
    <div
      class="flex h-full flex-row items-center px-3"
      :class="{ 'w-full': datasetStore.datasetCount > 0 }"
    >
      <div
        class="flex h-full w-full flex-col"
        v-if="datasetStore.datasetCount > 0"
      >
        <!-- <div class="flex flex-col h-full"> -->
        <span class="text-lg font-medium">
          Continue curating your datasets
        </span>

        <span>
          You have some incomplete projects. Select one to continue working on
          it.
        </span>

        <!-- <el-divider> </el-divider> -->

        <div class="h-full flex-grow overflow-y-auto">
          <div>
            <el-divider content-position="left">
              Projects currently in progress
            </el-divider>

            <div class="w-full px-10">
              <div
                v-for="dataset in datasetsInProgress"
                :key="dataset"
                class="project my-4 rounded-lg border border-zinc-200 px-6 py-4 shadow-md transition-all hover:border-transparent"
                :class="{ 'selected-project': dataset.id === selectedDataset }"
                @click="selectDataset($event, dataset.id, 'draft')"
              >
                <!-- @click="navigateToDataset(`${dataset.id}`)" -->
                <div class="flex flex-row items-center">
                  <img :src="dataset.image" alt="" class="w-20" />
                  <div class="mt-1 flex flex-col px-4 text-zinc-600">
                    <span class="text-md font-medium">
                      {{ dataset.name }}
                    </span>
                    <p class="text-sm line-clamp-3">
                      {{ dataset.description }}
                    </p>
                    <div class="h-[2px]"></div>
                    <div class="flex flex-wrap items-end space-x-3">
                      <el-tooltip
                        effect="dark"
                        :content="`Created on ${longDate(
                          dataset.meta.dateCreated
                        )}`"
                        placement="bottom"
                      >
                        <div class="flex items-center">
                          <Icon icon="clarity:date-outline-badged" />
                          <span class="pr-2 pl-1 text-sm">
                            {{ shortDate(dataset.meta.dateCreated) }}
                          </span>
                        </div>
                      </el-tooltip>

                      <el-tooltip
                        effect="dark"
                        :content="`Last modified on ${longDate(
                          dataset.meta.dateModified
                        )}`"
                        placement="bottom"
                      >
                        <div class="flex items-center">
                          <Icon icon="bx:time" />
                          <span class="pr-2 pl-1 text-sm">
                            {{ dateDifference(dataset.meta.dateModified) }} ago
                          </span>
                        </div>
                      </el-tooltip>

                      <div v-if="dataset.meta.destination != 'Unknown'">
                        <el-tooltip
                          effect="dark"
                          content="This dataset will be made FAIR using the Zenodo repository"
                          placement="bottom"
                          v-if="dataset.meta.destination === 'zenodo'"
                        >
                          <div class="flex items-center">
                            <Icon icon="clarity:upload-cloud-line" />
                            <span class="pr-2 pl-1 text-sm"> Zenodo </span>
                          </div>
                        </el-tooltip>
                      </div>

                      <div v-if="dataset.meta.location != 'Unknown'">
                        <el-tooltip
                          effect="dark"
                          :content="`The source for this dataset is the local folder at ${dataset.meta.locationPath} `"
                          placement="bottom"
                          v-if="dataset.meta.location === 'local'"
                        >
                          <div class="flex items-center">
                            <Icon icon="ic:outline-source" />
                            <span class="pr-2 pl-1 text-sm"> Local </span>
                          </div>
                        </el-tooltip>

                        <el-tooltip
                          effect="dark"
                          :content="`The source for this dataset is the GitHub repository ${dataset.meta.locationPath} `"
                          placement="bottom"
                          v-if="dataset.meta.location === 'github'"
                        >
                          <div class="flex items-center">
                            <Icon icon="ic:outline-source" />
                            <span class="pr-2 pl-1 text-sm"> GitHub </span>
                          </div>
                        </el-tooltip>
                      </div>

                      <div>
                        <el-tag
                          v-for="workflow in dataset.dataType"
                          :key="workflow"
                          size="small"
                        >
                          {{
                            workflow === "Code" ? "Research software" : workflow
                          }}
                        </el-tag>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="ml-2 hidden items-center">
                  <Icon icon="ic:round-navigate-next" class="h-8 w-8" />
                </div>
              </div>
            </div>
          </div>

          <div class="mt-5" v-if="datasetsPublished.length > 0">
            <el-divider content-position="left">
              Fully published projects
            </el-divider>

            <div class="w-full px-10">
              <div
                v-for="dataset in datasetsPublished"
                :key="dataset"
                class="project my-4 rounded-lg border border-zinc-200 px-6 py-4 shadow-md transition-all hover:border-transparent"
                :class="{ 'selected-project': dataset.id === selectedDataset }"
                @click="selectDataset($event, dataset.id, 'published')"
              >
                <!-- @click="navigateToDataset(`${dataset.id}`)" -->
                <div class="flex flex-row items-center">
                  <img :src="dataset.image" alt="" class="w-20" />
                  <div class="flex flex-col px-4">
                    <span class="text-md font-medium">
                      {{ dataset.name }}
                    </span>
                    <p class="text-sm line-clamp-3">
                      {{ dataset.description }}
                    </p>
                    <div
                      class="mt-1 flex flex-wrap items-end space-x-3 text-zinc-600"
                    >
                      <el-tooltip
                        effect="dark"
                        :content="`Created on ${longDate(
                          dataset.meta.dateCreated
                        )}`"
                        placement="bottom"
                      >
                        <div class="flex items-center">
                          <Icon icon="clarity:date-outline-badged" />
                          <span class="pr-2 pl-1 text-sm">
                            {{ shortDate(dataset.meta.dateCreated) }}
                          </span>
                        </div>
                      </el-tooltip>

                      <el-tooltip
                        effect="dark"
                        :content="`Last modified on ${longDate(
                          dataset.meta.dateModified
                        )}`"
                        placement="bottom"
                      >
                        <div class="flex items-center">
                          <Icon icon="bx:time" />
                          <span class="pr-2 pl-1 text-sm">
                            {{ dateDifference(dataset.meta.dateModified) }} ago
                          </span>
                        </div>
                      </el-tooltip>

                      <el-tooltip
                        effect="dark"
                        :content="`This dataset will be made FAIR using the ${dataset.meta.destination} repository`"
                        placement="bottom"
                        v-if="dataset.meta.destination != 'Unknown'"
                      >
                        <div class="flex items-center">
                          <Icon icon="clarity:upload-cloud-line" />
                          <span class="pr-2 pl-1 text-sm capitalize">
                            {{ dataset.meta.destination }}
                          </span>
                        </div>
                      </el-tooltip>

                      <div v-if="dataset.meta.location != 'Unknown'">
                        <el-tooltip
                          effect="dark"
                          :content="`The source for this dataset is ${dataset.meta.locationPath} `"
                          placement="bottom"
                          v-if="dataset.meta.location === 'local'"
                        >
                          <div class="flex items-center">
                            <Icon icon="ic:outline-source" />
                            <span class="pr-2 pl-1 text-sm"> Local </span>
                          </div>
                        </el-tooltip>

                        <el-tooltip
                          effect="dark"
                          :content="`The source for this dataset is the GitHub repository ${dataset.meta.locationPath} `"
                          placement="bottom"
                          v-if="dataset.meta.location === 'github'"
                        >
                          <div class="flex items-center">
                            <Icon icon="ic:outline-source" />
                            <span class="pr-2 pl-1 text-sm"> GitHub </span>
                          </div>
                        </el-tooltip>
                      </div>

                      <div>
                        <el-tag
                          v-for="workflow in dataset.workflows.workflow1.type"
                          :key="workflow"
                          size="small"
                        >
                          {{
                            workflow === "Code" ? "Research software" : workflow
                          }}
                        </el-tag>
                      </div>
                    </div>

                    <div class="hidden flex-wrap">
                      <el-button @click="PublishNewVersion(dataset)">
                        publish a new version
                      </el-button>
                    </div>
                  </div>
                </div>
                <div class="ml-2 hidden items-center">
                  <Icon icon="ic:round-navigate-next" class="h-8 w-8" />
                </div>
              </div>
            </div>
          </div>
        </div>

        <el-divider> </el-divider>

        <div class="mb-5 flex flex-row justify-between">
          <router-link to="/datasets/new">
            <div
              class="hover-underline-animation my-3 flex w-max cursor-pointer flex-row items-center text-primary-600"
            >
              <span class="font-medium">
                Or start a new data curation project
              </span>
              <Icon icon="grommet-icons:form-next-link" class="ml-2 h-5 w-5" />
            </div>
          </router-link>
          <div
            class="flex flex-row space-x-4 pr-2 pl-1"
            v-if="selectedDataset !== ''"
          >
            <button class="secondary-plain-button" @click="editProject">
              <el-icon><setting-icon /></el-icon> Project settings
            </button>
            <button class="primary-button" @click="startCuratingProject">
              Continue working on this project
              <el-icon class="icon-animate">
                <d-arrow-right />
              </el-icon>
            </button>
          </div>
        </div>
        <!-- </div> -->
      </div>
      <div class="flex flex-row items-center justify-center p-10" v-else>
        <router-link to="/datasets/new">
          <div
            class="flex w-max cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-dashed p-10 transition-all hover:border-solid hover:bg-gray-100"
          >
            <Icon
              icon="fluent:quiz-new-24-regular"
              class="h-20 w-10/12 text-blue-500"
            />
            <span class="text-large font-medium">
              Start a new data curation project
            </span>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { Icon } from "@iconify/vue";
import { useDatasetsStore } from "@/store/datasets";
import dayjs from "dayjs";
export default {
  name: "ShowAllProjects",
  components: { Icon },

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
    shortDate(date) {
      return dayjs(date).format("MMM DD");
    },
    longDate(date) {
      return dayjs(date).format("MMM DD, YYYY - hh:mm A");
    },
    dateDifference(date) {
      const now = dayjs();

      let difference = "";

      difference = now.diff(date, "second");

      if (difference < 60) {
        return `a few seconds`;
      }

      difference = now.diff(date, "minute");

      if (difference < 60) {
        if (difference === 1) {
          return `a minute`;
        } else if (difference < 10) {
          return `a few minutes`;
        } else {
          return `${difference} minutes`;
        }
      }

      difference = now.diff(date, "hour");

      if (difference < 24) {
        if (difference === 1) {
          return `an hour`;
        } else {
          return `${difference} hours`;
        }
      }

      difference = now.diff(date, "day");

      if (difference < 30) {
        if (difference === 1) {
          return `a day`;
        } else {
          return `${difference} days`;
        }
      }

      difference = now.diff(date, "month");

      if (difference < 12) {
        if (difference === 1) {
          return `a month`;
        } else {
          return `${difference} months`;
        }
      }

      difference = now.diff(date, "year");

      if (difference === 1) {
        return `a year`;
      } else {
        return `${difference} years`;
      }
    },
    PublishNewVersion(dataset) {
      console.log("publish a new version", dataset);
    },
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

      routerPath = `/datasets/${datasetID}/landing`;
      // routerPath = `/datasets/${datasetID}`;
      // routerPath = `/datasets/new/${datasetID}/confirm`;
      // routerPath = `/datasets/${datasetID}/workflow1/zenodo/metadata`;
      // routerPath = `/datasets/${datasetID}/workflow1/zenodo/metadata`;
      // routerPath = `/datasets/${datasetID}/workflow1/zenodo/review`;
      // routerPath = `/datasets/${datasetID}/workflow1/Code/reviewStandards`;
      // routerPath = `/datasets/${datasetID}/workflow1/Code/pickLicense`;
      // routerPath = `/datasets/${datasetID}/workflow1/Code/createMetadata`;
      // routerPath = `/datasets/${datasetID}/workflow1/zenodo/accessToken`;
      // routerPath = `/datasets/${datasetID}/workflow1/zenodo/publish`;
      routerPath = `/datasets/${datasetID}/workflow1/github/zenodoConnection`;
      // routerPath = `/datasets/${datasetID}/workflow1/github/publish`;

      this.$router.push({ path: routerPath });
    },
  },
  async mounted() {
    this.datasetStore.hideProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(1);

    let allDatasets = await this.datasetStore.getAllDatasets();
    // make a local copy of the datasets object
    const datasets = JSON.parse(JSON.stringify(allDatasets));
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
