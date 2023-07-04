<template>
  <div class="flex h-full w-full flex-col items-center justify-center p-3 pr-5">
    <div class="flex h-full w-full flex-col">
      <span class="text-left text-lg font-medium"> Final step </span>
      <span class="text-left">
        Looks like your dataset was generated for a Next Gen High Throughput Sequencing (NGS)
        experiment.
      </span>

      <line-divider />

      <div class="flex h-full flex-col items-center justify-center px-10">
        <Vue3Lottie
          animationLink="https://assets4.lottiefiles.com/packages/lf20_lg6lh7fp.json"
          class="pointer-events-none absolute left-0 top-0 h-full w-full"
          :loop="1"
        />
        <p class="pb-5 text-center">
          Looks like your dataset was generated and uploaded to GEO successfully. <br />
          You will need to notify GEO using the 'Submit to GEO' web form.
        </p>
        <div class="flex space-x-4">
          <button
            class="secondary-plain-button mr-4"
            @click="openWebPage('https://submit.ncbi.nlm.nih.gov/geo/submission/')"
          >
            Notify GEO <el-icon><chat-dot-round /></el-icon>
          </button>
          <button class="blob primary-button transition-all" @click="openGeneratedDataset">
            View generated dataset <el-icon><star-icon /></el-icon>
          </button>
        </div>
      </div>
    </div>
    <!-- <app-docs-link url="curate-and-share/zenodo-publish" position="bottom-4" /> -->
  </div>
</template>

<script>
import axios from "axios";
import path from "path";
import { ElLoading } from "element-plus";

import { useDatasetsStore } from "@/store/datasets";
import { useTokenStore } from "@/store/access.js";

export default {
  name: "GEOPublish",
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
  computed: {},
  methods: {
    async sleep(ms) {
      return new Promise((resolve) => setTimeout(resolve, ms));
    },
    async openWebPage(url) {
      window.ipcRenderer.send("open-link-in-browser", url);
    },
    async openGeneratedDataset() {
      const file_path = path.join(this.workflow.destinationFolderPath, "metadata.xlsx");

      this.showLoading = ElLoading.service({
        lock: true,
        text: "Loading",
        background: "rgba(0, 0, 0, 0.7)",
      });

      await axios
        .post(`${this.$server_url}/utilities/openfileexplorer`, {
          file_path,
        })
        .then((response) => {
          this.showLoading.close();
          return response.data;
        })
        .catch((error) => {
          this.showLoading.close();
          console.error(error);
          return "ERROR";
        });

      return;
    },
  },
  async mounted() {
    this.dataset = await this.datasetStore.getCurrentDataset();
    this.workflow = this.dataset.workflows[this.workflowID];

    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("geo");
    this.datasetStore.setCurrentStep(6);

    this.workflow.currentRoute = this.$route.path;
  },
};
</script>

<style lang="css" scoped>
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
