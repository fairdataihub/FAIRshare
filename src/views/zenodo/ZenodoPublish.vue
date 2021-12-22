<template>
  <div class="h-full w-full flex flex-col justify-center items-center pr-5 p-3">
    <div class="flex flex-col h-full w-full">
      <span class="text-lg font-medium text-left">
        Let's publish your work to Zenodo
      </span>
      <span class="text-left">
        All your data has been uploaded to Zenodo. It's now time to publish your
        work.
      </span>

      <el-divider class="my-4"> </el-divider>

      <div class="flex flex-col justify-center items-center h-full px-10">
        <p class="text-center pb-5">
          Once the record is published you will no longer be able to change the
          files in this upload. This is because a Digital Object Identifier
          (DOI) will be registered immediately after publishing. You will still
          be able to update the record's metadata later.
        </p>
        <el-button
          type="primary"
          plain
          class="blob transition-all"
          @click="publishDeposition"
        >
          Publish <el-icon><star /></el-icon>
        </el-button>
      </div>
    </div>
  </div>
</template>

<script>
// import axios from "axios";
import { ElMessageBox, ElLoading } from "element-plus";

import { useDatasetsStore } from "../../store/datasets";
import { useTokenStore } from "../../store/access.js";

export default {
  name: "ZenodoPublish",
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
  },
  async mounted() {
    this.dataset = await this.datasetStore.getCurrentDataset();
    this.workflow = this.dataset.workflows[this.workflowID];

    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(6);

    const tokenObject = await this.tokens.getToken("zenodoToken");
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
