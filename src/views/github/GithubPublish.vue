<template>
  <div class="flex h-full w-full flex-col items-center justify-center p-3 pr-5">
    <div class="flex h-full w-full flex-col">
      <span class="text-left text-lg font-medium">
        Publish your work to Zenodo
      </span>
      <span class="text-left">
        All your metadata files have been uploaded to GitHub. It's now time to
        publish your work to Zenodo.
      </span>

      <el-divider class="my-4"> </el-divider>

      <div class="flex h-full flex-col items-center justify-center px-10">
        <p class="text-secondary-600 pb-5 text-center">
          Once the record is published you will no longer be able to change the
          files in this upload. This is because a Digital Object Identifier
          (DOI) will be registered immediately after publishing. You will still
          be able to update the record's metadata later.
        </p>
        <div class="flex space-x-4">
          <button class="primary-plain-button" @click="openCommitList">
            View commits
          </button>
          <button class="primary-plain-button" @click="openDraftRelease">
            View draft release
          </button>
          <button
            class="blob primary-button transition-all"
            @click="publishDeposition"
          >
            Publish <el-icon><star-icon /></el-icon>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import axios from "axios";
import { ElMessageBox, ElLoading } from "element-plus";

import { useDatasetsStore } from "@/store/datasets";
import { useTokenStore } from "@/store/access.js";

export default {
  name: "GithubPublish",
  data() {
    return {
      datasetStore: useDatasetsStore(),
      tokens: useTokenStore(),
      dataset: {},
      folderPath: "",
      datasetID: this.$route.params.datasetID,
      workflowID: this.$route.params.workflowID,
      workflow: {},
      zenodoToken: "",
    };
  },
  computed: {},
  methods: {
    async sleep(ms) {
      return new Promise((resolve) => setTimeout(resolve, ms));
    },
    async publishDeposition() {
      // const depositionID = this.workflow.destination.zenodo.deposition_id;

      // const response = await axios
      //   .post(`${this.$server_url}/zenodo/publish`, {
      //     access_token: this.zenodoToken,
      //     deposition_id: depositionID,
      //   })
      //   .then((response) => {
      //     return response.data;
      //   })
      //   .catch((error) => {
      //     console.error(error);
      //     return "ERROR";
      //   });

      const loading = ElLoading.service({
        lock: true,
        text: "Loading",
        background: "rgba(0, 0, 0, 0.7)",
      });

      await this.sleep(3000);

      const response = {
        id: "5750415",
      };

      if (response === "ERROR") {
        this.workflow.datasetPublished = false;

        await this.datasetStore.updateCurrentDataset(this.dataset);
        await this.datasetStore.syncDatasets();

        this.statusMessage =
          "There was an error when adding metadata to the deposition";
        return "FAIL";
      } else {
        this.datasetStore.showProgressBar();
        this.datasetStore.setProgressBarType("zenodo");
        this.datasetStore.setCurrentStep(7);

        this.workflow.datasetPublished = true;

        await this.datasetStore.updateCurrentDataset(this.dataset);
        await this.datasetStore.syncDatasets();

        ElMessageBox.alert(
          "Your dataset was published to Zenodo. Click 'OK' to view this record on Zenodo.",
          "Published to Zenodo",
          {
            confirmButtonText: "OK",
            callback: (action) => {
              if (action === "confirm") {
                console.log(`Opening ${response.id}`);

                window.ipcRenderer.send(
                  "open-link-in-browser",
                  `https://sandbox.zenodo.org/record/${response.id}`
                );

                this.$router.push({ path: `/datasets/${this.datasetID}` });
              }
            },
          }
        );
      }

      loading.close();
    },
    async openCommitList() {
      const repoName = this.workflow.github.repo;
      const githubURL = `https://github.com/${repoName}/commits`;

      window.ipcRenderer.send("open-link-in-browser", githubURL);
    },
    async openDraftRelease() {
      const repoName = this.workflow.github.repo;
      const githubURL = `https://github.com/${repoName}/releases`;

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

    const tokenObject = await this.tokens.getToken("zenodo");
    this.zenodoToken = tokenObject.token;
    // console.log(this.zenodoToken);
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
