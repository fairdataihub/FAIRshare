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
                class="
                  project
                  my-4
                  rounded-lg
                  border border-zinc-200
                  px-6
                  py-4
                  shadow-md
                  transition-all
                  hover:border-transparent
                "
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
                    <p class="text-sm line-clamp-3">
                      {{ dataset.description }}
                    </p>
                    <div class="h-[2px]"></div>
                    <div class="flex flex-wrap">
                      <div class="justify-left flex items-center">
                        <Icon icon="codicon:history" />
                        <span class="px-2" v-if="showDetail != dataset.id">
                          date created: {{ dataset.meta.dateCreated }}
                        </span>
                        <span class="px-2" v-if="showDetail == dataset.id">
                          date created: {{ dataset.meta.dateCreatedDetail }}
                        </span>
                      </div>
                      <div class="justify-left flex items-center">
                        <Icon icon="codicon:history" />
                        <span class="px-2" v-if="showDetail != dataset.id">
                          last modified:
                          {{ dataset.meta.dateLastModified }}</span
                        >
                        <span class="px-2" v-if="showDetail == dataset.id">
                          date created:
                          {{ dataset.meta.dateLastModifiedDetail }}
                        </span>
                      </div>
                      <div class="justify-left flex items-center">
                        <Icon icon="clarity:upload-cloud-line" />
                        <span class="px-2">
                          destination: {{ dataset.meta.destination }}</span
                        >
                      </div>
                      <div class="justify-left flex items-center">
                        <Icon icon="ep:location" />
                        <span class="px-2">
                          location: {{ dataset.meta.location }}</span
                        >
                      </div>
                    </div>
                    <div class="flex flex-warp">
                      <el-button @click="PublishNewVersion(dataset)"
                        >publish a new version</el-button
                      >
                      <el-button
                        v-if="showDetail == ''"
                        @click="showDetail = dataset.id"
                        >detail</el-button
                      >
                      <el-button
                        v-if="showDetail != ''"
                        @click="showDetail = ''"
                        >hide detail</el-button
                      >
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
                class="
                  project
                  my-4
                  rounded-lg
                  border border-zinc-200
                  px-6
                  py-4
                  shadow-md
                  transition-all
                  hover:border-transparent
                "
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
                    <p class="text-sm line-clamp-3">
                      {{ dataset.description }}
                    </p>
                    <div class="flex flex-wrap">
                      <div class="justify-left flex items-center">
                        <Icon icon="codicon:history" />
                        <span class="px-2" v-if="showDetail != dataset.id">
                          date created: {{ dataset.meta.dateCreated }}
                        </span>
                        <span class="px-2" v-if="showDetail == dataset.id">
                          date created: {{ dataset.meta.dateCreatedDetail }}
                        </span>
                      </div>
                      <div class="justify-left flex items-center">
                        <Icon icon="codicon:history" />
                        <span class="px-2" v-if="showDetail != dataset.id">
                          last modified:
                          {{ dataset.meta.dateLastModified }}</span
                        >
                        <span class="px-2" v-if="showDetail == dataset.id">
                          date created:
                          {{ dataset.meta.dateLastModifiedDetail }}
                        </span>
                      </div>
                      <div class="justify-left flex items-center">
                        <Icon icon="clarity:upload-cloud-line" />
                        <span class="px-2">
                          destination: {{ dataset.meta.destination }}</span
                        >
                      </div>
                      <div class="justify-left flex items-center">
                        <Icon icon="ep:location" />
                        <span class="px-2">
                          location: {{ dataset.meta.location }}</span
                        >
                      </div>
                    </div>
                    <div class="flex flex-warp">
                      <el-button @click="PublishNewVersion(dataset)"
                        >publish a new version</el-button
                      >
                      <el-button @click="showDetail = dataset.id"
                        >detail</el-button
                      >
                      <el-button
                        v-if="showDetail != ''"
                        @click="showDetail = ''"
                        >hide detail</el-button
                      >
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
              class="
                hover-underline-animation
                my-3
                flex
                w-max
                cursor-pointer
                flex-row
                items-center
                text-primary-600
              "
            >
              <span class="font-medium">
                Or start a new data curation project
              </span>
              <Icon icon="grommet-icons:form-next-link" class="ml-2 h-5 w-5" />
            </div>
          </router-link>
          <div
            class="flex flex-row space-x-4 px-2"
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
            class="
              flex
              w-max
              cursor-pointer
              flex-col
              items-center
              justify-center
              rounded-lg
              border-2 border-dashed
              p-10
              transition-all
              hover:border-solid hover:bg-gray-100
            "
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
import { v4 as uuidv4 } from "uuid";
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
      showDetail: "",
    };
  },
  computed: {},
  methods: {
    readUntilDash(s) {
      for (let i = s.length - 1; i >= 0; i--) {
        if (s[i] == "-") {
          return i;
        }
      }
      return -1;
    },
    getOriginal(s) {
      let last = this.readUntilDash(s);
      return s.slice(0, last + 1);
    },
    PublishNewVersion(dataset) {
      console.log("publish a new version", dataset);
    },
    async duplicateDataset(targetDataset) {
      this.selectedDataset = "";
      let datasetID = uuidv4();
      let newname = targetDataset.name;
      newname = newname.concat("-COPY");

      let allDatasets = await this.datasetStore.getAllDatasets();
      const datasets = JSON.parse(JSON.stringify(allDatasets));
      let exist = false;
      for (const key in datasets) {
        if (datasets[key].name == newname) {
          exist = true;
          break;
        }
      }
      if (!exist) {
        let newDataset = Object.assign({}, targetDataset);
        let today = new Date();
        let currentDate =
          today.getFullYear() +
          "-" +
          (today.getMonth() + 1) +
          "-" +
          today.getDate();
        let currentTime =
          today.getHours() +
          ":" +
          today.getMinutes() +
          ":" +
          today.getSeconds();
        let dateTime = currentDate + " " + currentTime;
        let now = dayjs().format("MMMM D, YYYY");
        newDataset.id = datasetID;
        newDataset.name = newDataset.name.concat("-COPY");
        newDataset.meta.dateCreated = now;
        newDataset.meta.dateCreatedDetail = dateTime;
        this.datasetStore.addDataset(newDataset, datasetID);
        await this.updateDataset();
      } else {
        console.log("already");
      }
    },
    async updateDataset() {
      await this.buildDataset();
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
      // routerPath = `/datasets/${datasetID}/workflow1/github/zenodoConnection`;
      // routerPath = `/datasets/${datasetID}/workflow1/github/publish`;

      this.$router.push({ path: routerPath });
    },
    async buildDataset() {
      (this.datasetsInProgress = []), (this.datasetsPublished = []);
      let allDatasets = await this.datasetStore.getAllDatasets();

      // make a local copy of the datasets object
      const datasets = JSON.parse(JSON.stringify(allDatasets));

      // filter datasets in progress
      let datasetsInProgressIDs = [];

      for (const key in datasets) {
        if ("workflows" in datasets[key]) {
          for (const workflow in datasets[key].workflows) {
            console.log(
              "datasets[key].workflows[workflow]",
              datasets[key].workflows[workflow],
              datasets[key].data.Code.folderPath
            );
            if (!("meta" in datasets[key])) {
              datasets[key].meta = {
                dateCreated: "Unknown",
                dateCreatedDetail: "Unknown",
                dateLastModified: "Unknown",
                dateLastModifiedDetail: "Unknown",
                location: "Unknown",
                destination: "Unknown",
              };
            }
            if (datasets[key].workflows[workflow].destination.name != "") {
              datasets[key].meta.destination =
                datasets[key].workflows[workflow].destination.name;
            }
            if (
              "folderPath" in
                datasets[key].data[datasets[key].workflows[workflow].type[0]] &&
              datasets[key].data[datasets[key].workflows[workflow].type[0]]
                .folderPath != ""
            ) {
              datasets[key].meta.location =
                datasets[key].data[
                  datasets[key].workflows[workflow].type[0]
                ].folderPath;
            }
            if (
              "folderPath" in datasets[key].data.Code &&
              datasets[key].data.Code.folderPath != ""
            ) {
              datasets[key].meta.location = datasets[key].data.Code.folderPath;
            }
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
  },
  async mounted() {
    this.datasetStore.hideProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(1);
    await this.buildDataset();
  },
};
</script>
