<template>
  <div
    class="h-full w-full flex flex-row justify-center items-center p-3"
    v-loading="loading"
  >
    <div class="h-full flex flex-col justify-center items-center">
      <span class="text-center">
        Based on your data requirements, we suggest uploading your data to one
        of these repositories.
      </span>
      <span class="text-sm text-center">
        Please click one of the following options:
      </span>

      <div class="grid grid-cols-3 my-8 gap-8">
        <div class="flex flex-col justify-center items-center">
          <div
            class="flex flex-col justify-evenly items-center p-4 shadow-md rounded-lg transition-all cursor-pointer h-[200px] w-[200px] single-check-box"
            :class="{ 'selected-repo': repoID === 'zenodo' }"
            @click="selectRepo($event, 'zenodo')"
          >
            <img
              src="https://api.iconify.design/simple-icons/zenodo.svg"
              alt=""
              class="h-16 w-16 mb-3"
            />
            <span class="text-lg mx-5"> Zenodo </span>
          </div>
          <div
            class="flex flex-row items-center w-max text-primary-600 cursor-pointer hover-underline-animation my-3"
            v-if="repoID === 'zenodo'"
            @click="openWebsite('https://zenodo.org')"
          >
            <span class="font-medium"> Learn more... </span>
            <Icon icon="grommet-icons:form-next-link" class="ml-2 h-5 w-5" />
          </div>
        </div>

        <el-popover placement="bottom" trigger="hover" content="Coming soon...">
          <template #reference>
            <div>
              <div
                class="disabled-card flex flex-col justify-evenly items-center p-4 shadow-md rounded-lg transition-all cursor-pointer h-[200px] w-[200px] pointer-events-none text-stone-400 single-check-box"
                :class="{ 'selected-repo': repoID === 'figshare' }"
                @click="selectRepo($event, 'figshare')"
              >
                <img
                  src="https://www.digital-science.com/wp-content/uploads/2020/11/Figshare-no-padding.png"
                  alt=""
                  class="h-16 mb-3 opacity-50"
                />
                <span class="text-lg mx-5"> Figshare </span>
              </div>
            </div>
          </template>
        </el-popover>
        <el-popover placement="bottom" trigger="hover" content="Coming soon...">
          <template #reference>
            <div>
              <div
                class="disabled-card flex flex-col justify-evenly items-center p-4 shadow-md rounded-lg hover:shadow-lg transition-all cursor-pointer h-[200px] w-[200px] pointer-events-none text-stone-400 single-check-box"
                :class="{ 'selected-repo': repoID === 'softwareheritage' }"
                @click="selectRepo($event, 'softwareheritage')"
              >
                <img
                  src="https://www.softwareheritage.org/wp-content/uploads/2015/08/swh-logo.png"
                  alt=""
                  class="h-16 mb-3 opacity-50"
                />
                <span class="text-lg mx-5 w-full text-center">
                  Software Heritage
                </span>
              </div>
            </div>
          </template>
        </el-popover>
      </div>

      <!-- This will be enabled in the future. -->
      <!-- change to grid-cols-2 -->
      <!-- <div class="grid grid-cols-1 gap-4">
        <div
          v-for="repo of repositories"
          :key="repo.id"
          class="flex flex-col justify-between items-center bg-gray-200 p-4 my-5 shadow-md rounded-lg hover:bg-gray-300 hover:shadow-lg transition-all cursor-pointer h-30 w-30"
          :class="{ 'selected-repo': repoID === repo.id }"
          @click="selectRepo($event, repo.id)"
        >
          <img :src="repo.imgURL" alt="" class="h-16 mb-3" />
          <span class="text-lg mx-5"> {{ repo.name }} </span>
        </div>
      </div> -->

      <div
        class="absolute bottom-0 w-max-content flex flex-row justify-center py-2 space-x-4"
      >
        <router-link
          :to="`/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/Code/pickLicense`"
          class=""
        >
          <el-button type="danger" plain>
            <el-icon><d-arrow-left /></el-icon> Back
          </el-button>
        </router-link>

        <button
          class="primary-button"
          @click="addMetadata"
          :disabled="repoID === ''"
          id="continue"
        >
          Continue <el-icon> <d-arrow-right /> </el-icon>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { useDatasetsStore } from "../../store/datasets";
import { Icon } from "@iconify/vue";

export default {
  name: "SelectRepositoryDestination",
  components: { Icon },
  data() {
    return {
      datasetStore: useDatasetsStore(),
      dataset: {},
      workflowID: this.$route.params.workflowID,
      datasetID: this.$route.params.datasetID,
      workflow: {},
      loading: false,
      repoID: "",
      repositories: [
        {
          id: "zenodo",
          name: "Zenodo",
          imgURL: "https://api.iconify.design/simple-icons/zenodo.svg",
        },
        {
          id: "figshare",
          name: "Figshare",
          imgURL: "https://api.iconify.design/simple-icons/figshare.svg",
        },
      ],
    };
  },
  computed: {},
  methods: {
    selectRepo(event, repoID) {
      this.repoID = repoID;
      if (event && event.detail === 2) {
        this.addMetadata();
      }
    },
    openWebsite(url) {
      window.ipcRenderer.send("open-link-in-browser", url);
    },
    addMetadata() {
      this.dataset.destinationSelected = true;

      if (!("destination" in this.workflow)) {
        this.workflow.destination = {};
      }

      if (!this.workflow.destination[this.repoID]) {
        this.workflow.destination[this.repoID] = {
          id: this.repoID,
          questions: {},
          status: {},
        };
      }

      console.log(this.workflow.destination);

      if (this.workflow.destination.name === this.repoID) {
        //do nothing
        this.workflow.destination.name = this.repoID;
      } else {
        // warn the user that they are changing repos (add a sweetalert or something)
        this.workflow.destination.name = this.repoID;
      }

      console.log(this.workflow.destination);

      this.datasetStore.updateCurrentDataset(this.dataset);
      this.datasetStore.syncDatasets();

      const redirectURL = `/datasets/${this.datasetID}/${this.workflowID}/${this.repoID}/metadata`;
      this.$router.push(redirectURL);
    },
  },
  async mounted() {
    this.loading = true;

    this.dataset = await this.datasetStore.getCurrentDataset();
    this.workflow = this.dataset.workflows[this.workflowID];

    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(4);

    if (this.workflow.destination) {
      this.repoID = this.workflow.destination.name;
    }

    console.log(this.workflow.destination);

    this.loading = false;
  },
};
</script>

<style scoped>
.single-check-box {
  @apply transition-all flex justify-center items-center w-48 h-48;
}

.single-check-box:not(.disabled-card):hover {
  @apply border border-secondary-500 shadow-lg shadow-secondary-500/50 transition-all;
}
</style>
