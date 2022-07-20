<template>
  <div class="flex h-full w-full flex-col items-center justify-center p-3 pr-5">
    <div class="flex h-full w-full flex-col">
      <span class="text-left text-lg font-medium"> Registered on bio.tools </span>

      <line-divider />

      <div class="flex h-full flex-col items-center justify-center px-10">
        <Vue3Lottie
          animationLink="https://assets4.lottiefiles.com/packages/lf20_lg6lh7fp.json"
          class="pointer-events-none absolute top-0 left-0 h-full w-full"
          :loop="1"
        />

        <p class="pb-5 text-center text-lg font-medium">
          Your software was successfully registered. You can now view it on bio.tools.
        </p>

        <p class="max-w-lg pb-5 text-center text-sm">
          If you need to edit your registration, you can do so by clicking on the <br />
          'View on bio.tools' button below. You will also be able to edit your details on there as
          well.
        </p>

        <div class="flex space-x-4">
          <router-link :to="`/datasets`" class="">
            <button class="primary-plain-button">
              <el-icon><data-line /></el-icon> Go to the homepage
            </button>
          </router-link>
          <button class="blob primary-button transition-all" @click="viewDatasetOnBioTools">
            View on bio.tools <el-icon><star-icon /></el-icon>
          </button>
        </div>
      </div>
    </div>
    <app-docs-link url="curate-and-share/zenodo-publish" position="bottom-4" />
  </div>
</template>

<script>
import { useDatasetsStore } from "@/store/datasets";
import { useTokenStore } from "@/store/access.js";

export default {
  name: "BioToolsReview",
  data() {
    return {
      datasetStore: useDatasetsStore(),
      tokens: useTokenStore(),
      dataset: {},
      folderPath: "",
      datasetID: this.$route.params.datasetID,
      workflowID: this.$route.params.workflowID,
      workflow: {},
    };
  },
  computed: {
    showBioToolsRegister() {
      if ("biotools" in this.workflow) {
        return true;
      } else {
        return false;
      }
    },
  },
  methods: {
    async sleep(ms) {
      return new Promise((resolve) => setTimeout(resolve, ms));
    },
    async viewDatasetOnBioTools() {
      const biotoolsID = this.workflow.biotools.biotoolsID;
      window.ipcRenderer.send(
        "open-link-in-browser",
        `${process.env.VUE_APP_BIO_TOOLS_URL}/${biotoolsID}`
      );
    },
    async openWebPage(url) {
      window.ipcRenderer.send("open-link-in-browser", url);
    },
  },
  async mounted() {
    this.dataset = await this.datasetStore.getCurrentDataset();
    this.workflow = this.dataset.workflows[this.workflowID];

    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(9);

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
