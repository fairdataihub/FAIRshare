<template>
  <div class="flex h-full w-full flex-col items-center justify-center p-3 pr-5">
    <div class="flex h-full w-full flex-col">
      <span class="text-left text-lg font-medium"> Final step </span>
      <span class="text-left"> All your requested data has been generated and uploaded. </span>

      <el-divider class="my-4"> </el-divider>

      <div class="flex h-full flex-col items-center justify-center px-10">
        <p class="pb-5 text-center">
          It does not look like you have selected a data repository to upload to. This is not
          recommended if you are trying to make your dataset FAIR. You can come back to this page
          later and select a repository to make your dataset completely FAIR.
        </p>
        <div class="flex space-x-4">
          <router-link :to="`/datasets`" class="">
            <button class="primary-plain-button">
              <el-icon><data-line /></el-icon> Go to the homepage
            </button>
          </router-link>
          <button class="secondary-plain-button" @click="openRepository">
            <el-icon><fold-icon /></el-icon>
            View repository
          </button>
          <button class="primary-button blob transition-all" @click="navigateToBioToolsPublishing">
            <el-icon><suitcase-icon /></el-icon> Register on bio.tools
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useDatasetsStore } from "@/store/datasets";

export default {
  name: "LocalNoUploadEnd",
  data() {
    return {
      datasetStore: useDatasetsStore(),
      dataset: {},
      folderPath: "",
      datasetID: this.$route.params.datasetID,
      workflowID: this.$route.params.workflowID,
      workflow: {},
      zenodoToken: "",
      published: false,
      zenodoDatasetID: "",
    };
  },
  computed: {},
  methods: {
    async sleep(ms) {
      return new Promise((resolve) => setTimeout(resolve, ms));
    },
    navigateToBioToolsPublishing() {
      this.$router.push(`/datasets/${this.datasetID}/${this.workflowID}/biotools/login`);
    },
    async openRepository() {
      const githubURL = `https://github.com/${this.dataset.meta.locationPath}`;
      window.ipcRenderer.send("open-link-in-browser", githubURL);
    },
  },
  async mounted() {
    this.dataset = await this.datasetStore.getCurrentDataset();
    this.workflow = this.dataset.workflows[this.workflowID];

    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(7);

    this.workflow.currentRoute = this.$route.path;
  },
};
</script>

<style lang="postcss" scoped>
.blob {
  box-shadow: 0 0 0 0 rgba(52, 172, 224, 1);
  animation: pulse-blue 2s infinite;
}

@keyframes pulse-blue {
  0% {
    transform: scale(0.95);
    box-shadow: 0 0 0 0 rgba(52, 172, 224, 0.7);
  }

  70% {
    transform: scale(1);
    box-shadow: 0 0 0 10px rgba(52, 172, 224, 0);
  }

  100% {
    transform: scale(0.95);
    box-shadow: 0 0 0 0 rgba(52, 172, 224, 0);
  }
}
</style>
