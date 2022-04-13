<template>
  <div class="flex h-full w-full flex-col items-center justify-center p-3 pr-5">
    <div class="flex h-full w-full flex-col">
      <span class="text-left text-lg font-medium"> Publish your work to Zenodo </span>
      <span class="text-left">
        All your data has been uploaded to Zenodo. It's now time to publish your work.
      </span>

      <el-divider class="my-4"> </el-divider>

      <div class="flex h-full flex-col items-center justify-center px-10" v-if="!published">
        <p class="pb-5 text-center">
          Once the record is published you will no longer be able to change the files in this
          upload. This is because a Digital Object Identifier (DOI) will be registered immediately
          after publishing. You will still be able to update the record's metadata later.
        </p>
        <div class="flex space-x-4">
          <button class="primary-plain-button" @click="openDraftDataset">View draft</button>
          <button
            class="secondary-plain-button"
            @click="navigateToBioToolsPublishing"
            v-if="showBioToolsRegister"
          >
            Register on bio.tools <el-icon><suitcase-icon /></el-icon>
          </button>
          <button class="blob primary-button transition-all" @click="publishDeposition">
            Publish <el-icon><star-icon /></el-icon>
          </button>
        </div>
      </div>
      <div class="flex h-full flex-col items-center justify-center px-10" v-else>
        <Vue3Lottie
          animationLink="https://assets4.lottiefiles.com/packages/lf20_lg6lh7fp.json"
          class="pointer-events-none absolute top-0 left-0 h-full w-full"
          :loop="1"
        />
        <p class="pb-5 text-center text-lg font-medium">
          Your dataset was successfully published. You can now view it on Zenodo.
        </p>
        <p class="max-w-lg pb-5 text-center text-sm">
          To increase the FAIRness of your software, we recommend to register it on the
          <span @click="openWebPage('https://bio.tools/')" class="text-url">bio.tools</span>
          registry. It is also suggested to publish about your software in a suitable journal such
          as the Journal of Open Research Software or any other suitable Journal (a list of suitable
          Journals can be found
          <span
            @click="
              openWebPage('https://www.software.ac.uk/which-journals-should-i-publish-my-software')
            "
            class="text-url"
            >here</span
          >).
        </p>
        <div class="flex space-x-4">
          <router-link :to="`/datasets`" class="">
            <button class="primary-plain-button">
              <el-icon><data-line /></el-icon> Go to the homepage
            </button>
          </router-link>
          <button class="secondary-plain-button" @click="viewDatasetOnZenodo">
            View dataset on Zenodo <el-icon><star-icon /></el-icon>
          </button>
          <button class="blob primary-button transition-all" @click="navigateToBioToolsPublishing">
            Register on bio.tools <el-icon><suitcase-icon /></el-icon>
          </button>
        </div>
      </div>
    </div>
    <app-docs-link url="curate-and-share/zenodo-publish" position="bottom-4" />
  </div>
</template>

<script>
import axios from "axios";
import { ElLoading } from "element-plus";

import { useDatasetsStore } from "@/store/datasets";
import { useTokenStore } from "@/store/access.js";

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
      published: false,
      zenodoDatasetID: "",
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
    async updateForNewVersion() {
      const response = await axios
        .get(`${this.$server_url}/zenodo/depositions`, {
          params: {
            access_token: this.zenodoToken,
          },
        })
        .then((response) => {
          return response.data;
        })
        .catch((error) => {
          console.error(error);
          return "ERROR";
        });

      const filteredDepositions = response.filter((deposition) => {
        return deposition.submitted === true;
      });

      const selectedDeposition = filteredDepositions[0];

      this.workflow.destination.zenodo.selectedDeposition = selectedDeposition;
      this.workflow.destination.zenodo.newVersion = true;
    },
    async publishDeposition() {
      const depositionID = this.workflow.destination.zenodo.deposition_id;

      const loading = ElLoading.service({
        lock: true,
        text: "Publishing dataset on Zenodo...",
        background: "rgba(0, 0, 0, 0.7)",
      });

      const response = await axios
        .post(`${this.$server_url}/zenodo/deposition/publish`, {
          access_token: this.zenodoToken,
          deposition_id: depositionID,
        })
        .then((response) => {
          this.$track("Zenodo", "Publish deposition", "success");

          if (
            "newVersion" in this.workflow.destination.zenodo &&
            this.workflow.destination.zenodo.newVersion === true
          ) {
            this.$track("Zenodo", "Publish new version", "success");
          }

          return response.data;
        })
        .catch((error) => {
          this.$track("Zenodo", "Publish deposition", "failed");

          if (
            "newVersion" in this.workflow.destination.zenodo &&
            this.workflow.destination.zenodo.newVersion === true
          ) {
            this.$track("Zenodo", "Publish new version", "failed");
          }

          console.error(error);
          return "ERROR";
        });

      // await this.sleep(1000);

      // const response = {
      //   id: "5750415",
      // };

      this.zenodoDatasetID = response.id;
      console.log(this.zenodoDatasetID);

      if (response === "ERROR") {
        this.workflow.datasetPublished = false;

        await this.datasetStore.updateCurrentDataset(this.dataset);
        await this.datasetStore.syncDatasets();

        this.statusMessage = "There was an error when publishing the deposition";
        return "FAIL";
      } else {
        this.datasetStore.showProgressBar();
        this.datasetStore.setProgressBarType("zenodo");
        this.datasetStore.setCurrentStep(8);

        this.workflow.datasetPublished = true;

        this.published = true;

        if (
          "newVersion" in this.workflow.destination.zenodo &&
          this.workflow.destination.zenodo.newVersion === false
        ) {
          await this.updateForNewVersion();
        }

        await this.datasetStore.updateCurrentDataset(this.dataset);
        await this.datasetStore.syncDatasets();
      }

      loading.close();
    },
    async viewDatasetOnZenodo() {
      window.ipcRenderer.send(
        "open-link-in-browser",
        `${process.env.VUE_APP_ZENODO_URL}/record/${this.zenodoDatasetID}`
      );
    },
    async openDraftDataset() {
      const depositionID = this.workflow.destination.zenodo.deposition_id;

      window.ipcRenderer.send(
        "open-link-in-browser",
        `${process.env.VUE_APP_ZENODO_URL}/deposit/${depositionID}`
      );
    },
    navigateToBioToolsPublishing() {
      this.$router.push(`/datasets/${this.datasetID}/${this.workflowID}/biotools/login`);
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
