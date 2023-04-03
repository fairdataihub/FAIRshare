<template>
  <div class="flex h-full w-full max-w-screen-xl flex-col items-center justify-center p-3 pr-5">
    <div class="flex h-full w-full flex-col">
      <span class="text-left text-lg font-medium"> Publish your work to Figshare </span>
      <span class="text-left">
        All your data has been uploaded to Figshare. It's now time to publish your work.
      </span>

      <line-divider />

      <div class="flex h-full flex-col items-center justify-center px-10" v-if="!published">
        <p class="pb-5 text-center">
          Once the record is published you will no longer be able to change the files in this
          upload. This is because a Digital Object Identifier (DOI) will be registered immediately
          after publishing.
        </p>
        <div class="flex space-x-4">
          <button class="primary-plain-button" @click="openDraftDataset">View draft</button>

          <button class="blob primary-button transition-all" @click="showPublishWarning">
            Publish <el-icon><star-icon /></el-icon>
          </button>

          <warning-confirm
            ref="figsharePublishWarning"
            title="Are you sure you want to publish?"
            @messageConfirmed="publishDeposition"
            confirmButtonText="Yes, I want to publish"
          >
            <p class="text-center text-base text-gray-500">
              This is a permanent action. You will not be able to change the files in this version
              of the dataset after it is published.
            </p>
          </warning-confirm>
        </div>
      </div>
      <div class="flex h-full flex-col items-center justify-center px-10" v-else>
        <Vue3Lottie
          animationLink="https://assets4.lottiefiles.com/packages/lf20_lg6lh7fp.json"
          class="pointer-events-none absolute top-0 left-0 h-full w-full"
          :loop="1"
        />

        <p class="pb-5 text-center text-lg font-medium">
          Your dataset was successfully published. You can now view it on Figshare.
        </p>

        <div class="flex flex-col">
          <div class="my-4 flex space-x-4">
            <router-link :to="`/datasets`" class="">
              <button class="primary-plain-button">
                <el-icon><data-line /></el-icon> Go to the homepage
              </button>
            </router-link>
            <button class="secondary-plain-button" @click="viewDatasetOnFigshare">
              <el-icon><star-icon /></el-icon> View dataset on Figshare
            </button>
          </div>
        </div>

        <div v-if="showCreateGithubRelease" class="w-full">
          <line-divider class="w-full" />

          <div class="flex items-center justify-center space-x-4">
            <p class="text-center">
              Would you also like to make a release on GitHub of this dataset?
            </p>

            <button class="primary-button transition-all" @click="createGitHubRelease">
              <el-icon><suitcase-icon /></el-icon> Create GitHub release
            </button>
          </div>
        </div>
        <div v-if="showBioToolsRegister">
          <line-divider class="w-full" />

          <p class="max-w-lg pb-5 text-center text-sm">
            To increase the FAIRness of your software, we also recommend to register it on the
            <span @click="openWebPage('https://bio.tools/')" class="text-url">bio.tools</span>
            registry. It is also suggested to publish about your software in a suitable journal such
            as the Journal of Open Research Software or any other suitable Journal (a list of
            suitable Journals can be found
            <span
              @click="
                openWebPage(
                  'https://www.software.ac.uk/which-journals-should-i-publish-my-software'
                )
              "
              class="text-url"
              >here</span
            >).
          </p>

          <div class="flex flex-col">
            <div class="flex justify-center space-x-4">
              <button
                class="blob primary-button transition-all"
                @click="navigateToBioToolsPublishing"
              >
                <el-icon><suitcase-icon /></el-icon> Register on bio.tools
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <app-docs-link url="curate-and-share/figshare/figshare-publish" position="bottom-4" />
  </div>
</template>

<script>
import axios from "axios";
import { ElLoading } from "element-plus";

import { useDatasetsStore } from "@/store/datasets";
import { useTokenStore } from "@/store/access.js";

export default {
  name: "FigsharePublish",
  data() {
    return {
      datasetStore: useDatasetsStore(),
      tokens: useTokenStore(),
      dataset: {},
      folderPath: "",
      datasetID: this.$route.params.datasetID,
      workflowID: this.$route.params.workflowID,
      workflow: {},
      figshareToken: "",
      published: false,
    };
  },
  computed: {
    showBioToolsRegister() {
      const allowedDataTypes = ["Code"];

      if ("type" in this.workflow) {
        for (const dataType of this.workflow.type) {
          if (allowedDataTypes.includes(dataType)) {
            return true;
          }
        }
      }

      return false;
    },
    showCreateGithubRelease() {
      if (
        "source" in this.workflow &&
        "type" in this.workflow.source &&
        this.workflow.source.type === "github"
      ) {
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
        .get(`${this.$server_url}/figshare/depositions`, {
          params: {
            access_token: this.figshareToken,
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

      this.workflow.destination.figshare.selectedDeposition = selectedDeposition;
      this.workflow.destination.figshare.newVersion = true;
    },
    async showPublishWarning() {
      this.$refs.figsharePublishWarning.show();
    },
    async publishDeposition() {
      const article_id = this.workflow.destination.figshare.article_id;

      const loading = ElLoading.service({
        lock: true,
        text: "Publishing dataset on Figshare...",
        background: "rgba(0, 0, 0, 0.7)",
      });

      const response = await axios
        .post(`${this.$server_url}/figshare/item/publish`, {
          access_token: this.figshareToken,
          article_id: article_id,
        })
        .then((response) => {
          response = JSON.parse(response.data);

          if ("status" in response && response.status === "ERROR") {
            console.error(response.message, response.details);
            return "ERROR";
          }

          this.$track("Figshare", "Publish deposition", "success");

          if (
            "newVersion" in this.workflow.destination.figshare &&
            this.workflow.destination.figshare.newVersion === true
          ) {
            this.$track("Figshare", "Publish new version", "success");
          }

          return response;
        })
        .catch((error) => {
          this.$track("Figshare", "Publish deposition", "failed");

          if (
            "newVersion" in this.workflow.destination.figshare &&
            this.workflow.destination.figshare.newVersion === true
          ) {
            this.$track("Figshare", "Publish new version", "failed");
          }

          console.error(error);
          return "ERROR";
        });

      if (response === "ERROR") {
        this.workflow.datasetPublished = false;

        await this.datasetStore.updateCurrentDataset(this.dataset);
        await this.datasetStore.syncDatasets();

        this.statusMessage = "There was an error with publishing the dataset.";
        return "FAIL";
      } else {
        this.datasetStore.showProgressBar();
        this.datasetStore.setProgressBarType("zenodo");
        this.datasetStore.setCurrentStep(8);

        this.workflow.datasetPublished = true;
        this.workflow.destination.figshare.location = response.message; //doi is being sent in the message key for now

        this.published = true;

        if (
          "newVersion" in this.workflow.destination.figshare &&
          this.workflow.destination.figshare.newVersion === false
        ) {
          /**
           * TODO: this one will have to be updated when I add new version support
           */
          // await this.updateForNewVersion();
        }

        await this.datasetStore.updateCurrentDataset(this.dataset);
        await this.datasetStore.syncDatasets();
      }

      loading.close();
    },
    async viewDatasetOnFigshare() {
      const doi = this.workflow.destination.figshare.doi;

      window.ipcRenderer.send("open-link-in-browser", `https://dx.doi.org/${doi}`);
    },
    async openDraftDataset() {
      const article_id = this.workflow.destination.figshare.article_id;

      this.openWebPage(`${process.env.VUE_APP_FIGSHARE_URL}/account/articles/${article_id}`);
    },
    navigateToBioToolsPublishing() {
      this.$router.push(`/datasets/${this.datasetID}/${this.workflowID}/biotools/login`);
    },
    createGitHubRelease() {
      this.$router.push(`/datasets/${this.datasetID}/${this.workflowID}/github/publish`);
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

    const tokenObject = await this.tokens.getToken("figshare");
    this.figshareToken = tokenObject.token;
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
