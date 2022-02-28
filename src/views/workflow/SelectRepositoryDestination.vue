<template>
  <div
    class="flex h-full w-full flex-row items-center justify-center p-3"
    v-loading="loading"
  >
    <div class="flex h-full flex-col items-center justify-center">
      <span class="text-center">
        Based on your dataset requirements, we suggest uploading your data to
        one of these repositories.
      </span>
      <span class="text-center text-sm">
        Please click one of the following options:
      </span>

      <div class="my-8 grid grid-cols-3 gap-8">
        <div>
          <div class="flex flex-col items-center justify-center">
            <div
              class="single-check-box flex h-[200px] w-[200px] cursor-pointer flex-col items-center justify-evenly rounded-lg p-4 shadow-md transition-all"
              :class="{ 'selected-repo': repoID === 'zenodo' }"
              @click="selectRepo($event, 'zenodo')"
            >
              <img
                src="https://api.iconify.design/simple-icons/zenodo.svg"
                alt=""
                class="mb-3 h-16 w-16"
              />
              <span class="mx-5 text-lg"> Zenodo </span>
            </div>
            <div
              class="hover-underline-animation my-5 flex w-max cursor-pointer flex-row items-center text-primary-600"
              v-if="repoID === 'zenodo'"
              @click="openWebsite('https://zenodo.org')"
            >
              <span class="font-medium"> Learn more... </span>
              <Icon icon="grommet-icons:form-next-link" class="ml-2 h-5 w-5" />
            </div>
          </div>
        </div>

        <div>
          <el-popover
            placement="bottom"
            trigger="hover"
            content="Coming soon..."
          >
            <template #reference>
              <div>
                <div
                  class="disabled-card single-check-box pointer-events-none flex h-[200px] w-[200px] cursor-pointer flex-col items-center justify-evenly rounded-lg p-4 text-stone-400 shadow-md transition-all"
                  :class="{ 'selected-repo': repoID === 'figshare' }"
                  @click="selectRepo($event, 'figshare')"
                >
                  <img
                    src="https://www.digital-science.com/wp-content/uploads/2020/11/Figshare-no-padding.png"
                    alt=""
                    class="mb-3 h-16 opacity-50"
                  />
                  <span class="mx-5 text-lg"> Figshare </span>
                </div>
              </div>
            </template>
          </el-popover>
        </div>

        <div>
          <el-popover
            placement="bottom"
            trigger="hover"
            content="Coming soon..."
          >
            <template #reference>
              <div>
                <div
                  class="disabled-card single-check-box pointer-events-none flex h-[200px] w-[200px] cursor-pointer flex-col items-center justify-evenly rounded-lg p-4 text-stone-400 shadow-md transition-all hover:shadow-lg"
                  :class="{ 'selected-repo': repoID === 'softwareheritage' }"
                  @click="selectRepo($event, 'softwareheritage')"
                >
                  <img
                    src="https://www.softwareheritage.org/wp-content/uploads/2015/08/swh-logo.png"
                    alt=""
                    class="mb-3 h-16 opacity-50"
                  />
                  <span class="mx-5 w-full text-center text-lg">
                    Software Heritage
                  </span>
                </div>
              </div>
            </template>
          </el-popover>
        </div>
      </div>

      <!-- This will be enabled in the future. -->
      <!-- change to grid-cols-2 -->
      <!-- <div class="grid grid-cols-1 gap-4">
        <div
          v-for="repo of repositories"
          :key="repo.id"
          class="flex flex-col items-center justify-between p-4 my-5 transition-all bg-gray-200 rounded-lg shadow-md cursor-pointer hover:bg-gray-300 hover:shadow-lg h-30 w-30"
          :class="{ 'selected-repo': repoID === repo.id }"
          @click="selectRepo($event, repo.id)"
        >
          <img :src="repo.imgURL" alt="" class="h-16 mb-3" />
          <span class="mx-5 text-lg"> {{ repo.name }} </span>
        </div>
      </div> -->

      <div
        class="w-max-content absolute bottom-0 flex flex-row justify-center space-x-4 py-6"
      >
        <router-link
          :to="`/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/Code/pickLicense`"
          class=""
        >
          <button class="primary-plain-button">
            <el-icon><d-arrow-left /></el-icon> Back
          </button>
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
    this.datasetStore.setCurrentStep(5);

    this.workflow.currentRoute = this.$route.path;

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
  @apply flex h-48 w-48 items-center justify-center transition-all;
}

.single-check-box:not(.disabled-card, .selected-repo):hover {
  @apply border border-secondary-500 shadow-lg shadow-secondary-500/50 transition-all;
}
</style>
