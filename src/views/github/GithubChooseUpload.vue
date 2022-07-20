<template>
  <div class="flex h-full w-full max-w-screen-xl flex-col items-center justify-center p-3 pr-5">
    <div class="flex h-full w-full flex-col">
      <h1 class="pb-1 text-left text-lg font-medium">Let's decide what to upload</h1>
      <p class="text-left">
        In this step you can decide what to upload to the data repository. Your source code will be
        automatically saved but you can also add additional files.
      </p>

      <line-divider />
    </div>
    <app-docs-link url="curate-and-share/connect-github-zenodo" position="bottom-4" />
  </div>
</template>

<script>
import { useDatasetsStore } from "@/store/datasets";
import { useTokenStore } from "@/store/access.js";

import { ElLoading } from "element-plus";

import rippleLottieJSON from "@/assets/lotties/rippleLottie.json";

export default {
  name: "GithubChooseUpload",
  components: {},
  data() {
    return {
      datasetStore: useDatasetsStore(),
      tokens: useTokenStore(),
      dataset: {},
      folderPath: "",
      workflowID: this.$route.params.workflowID,
      workflow: {},
      GithubAccessToken: "",
      validZenodoHookTokenFound: false,
      errorMessage: "",
      zenodoAccessToken: "",
      selectedRepo: "",
      currentBranch: "",
      rippleLottieJSON,
      finishedLoading: false,
      interval: null,
    };
  },

  methods: {
    createLoading() {
      const loading = ElLoading.service({
        lock: true,
        text: "Reading GitHub repository...",
        background: "rgba(255, 255, 255, 0.97)",
      });
      return loading;
    },

    openWebsite() {
      const url = `${process.env.VUE_APP_ZENODO_URL}/account/settings/github`;
      window.ipcRenderer.send("open-link-in-browser", url);
    },

    async showSummary() {
      const routerPath = `/datasets/${this.datasetID}/${this.workflowID}/github/summary`;

      this.$router.push({ path: routerPath });
    },
  },

  async mounted() {
    this.dataset = await this.datasetStore.getCurrentDataset();
    this.workflow = this.dataset.workflows[this.workflowID];

    this.selectedRepo = this.workflow.github.repo;

    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(6);

    const tokenObject = await this.tokens.getToken("github");
    this.GithubAccessToken = tokenObject.token;

    // }

    this.workflow.currentRoute = this.$route.path;
  },
};
</script>
