<template>
  <div
    class="flex h-full w-full max-w-screen-xl flex-col items-center justify-center p-3 pr-5"
  >
    <div class="flex h-full w-full flex-col">
      <span class="text-left text-lg font-medium">
        Github connection details
      </span>
      <span class="text-left">
        We will use this to upload and edit your dataset on your Github account.
      </span>

      <el-divider class="my-4"> </el-divider>

      <div v-if="ready">
        <p v-if="validTokenAvailable" class="my-10 w-full text-center">
          Looks like we already have your Github login details. Click on the
          'Start upload' button below.
        </p>
        <!-- show error message if token is not valid -->
        <div v-else class="flex flex-col items-center justify-center py-10">
          <p class="mb-5">
            We couldn't find your Github login details. Please click on the
            button below to connect to your Github account.
          </p>

          <ConnectGithub :statusChangeFunction="showConnection"></ConnectGithub>
        </div>
      </div>
      <LoadingFoldingCube v-else></LoadingFoldingCube>

      <div class="flex w-full flex-row justify-center space-x-4 py-2">
        <router-link
          :to="`/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/Github/metadata`"
          class=""
        >
          <button class="primary-plain-button">
            <el-icon><d-arrow-left /></el-icon> Back
          </button>
        </router-link>

        <button
          class="secondary-plain-button"
          @click="showFilePreview"
          v-if="validTokenAvailable"
        >
          <el-icon><checked-icon /></el-icon>
          View files ready for upload
        </button>

        <button
          class="primary-button"
          :disabled="disableContinue"
          @click="uploadToGithub"
          v-if="validTokenAvailable"
        >
          Start upload
          <el-icon> <d-arrow-right /> </el-icon>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import LoadingFoldingCube from "@/components/spinners/LoadingFoldingCube";
import ConnectGithub from "@/components/serviceIntegration/ConnectGithub";

import { useDatasetsStore } from "@/store/datasets";
import { useTokenStore } from "@/store/access.js";

import { ElLoading } from "element-plus";

export default {
  name: "SelectGithubRepo",
  components: { LoadingFoldingCube, ConnectGithub },
  data() {
    return {
      datasetStore: useDatasetsStore(),
      tokens: useTokenStore(),
      dataset: {},
      folderPath: "",
      workflowID: this.$route.params.workflowID,
      workflow: {},
      validTokenAvailable: false,
      errorMessage: "",
      GithubAccessToken: "",
      ready: false,
    };
  },
  //el-tree-node__content
  computed: {
    disableContinue() {
      if (this.validTokenAvailable) {
        return false;
      }
      if (!this.validTokenAvailable && this.GithubAccessToken !== "") {
        return false;
      }
      return true;
    },
  },
  methods: {
    createLoading() {
      const loading = ElLoading.service({
        lock: true,
        text: "Reading data...",
      });
      return loading;
    },
    async checkToken(token) {
      console.log(token);
      const response = await this.tokens.getDepositions(token);

      if (response.status === 200) {
        this.validTokenAvailable = true;
        this.tokens.saveToken("Github", token);
        return true;
      } else if (response.status === 401) {
        this.errorMessage =
          "Invalid Github access token. Please enter a valid Github access token.";
        this.validTokenAvailable = false;
        return false;
      } else {
        this.errorMessage = "Something went wrong. Please try again.";
        this.validTokenAvailable = false;
        return false;
      }
    },
    async uploadToGithub() {
      const routerPath = `/datasets/${this.datasetID}/${this.workflowID}/Github/upload`;
      if (this.validTokenAvailable) {
        this.$router.push({ path: routerPath });
      } else {
        const GithubToken = this.GithubAccessToken;
        const res = await this.checkToken(GithubToken);

        if (res) {
          this.$router.push({ path: routerPath });
        }
      }
    },
    async showConnection(status) {
      console.log(status);
      if (status === "connected") {
        this.validTokenAvailable = true;
      }
      // this.uploadToGithub(); console.log(this.workflow.licenseText)
    },
  },
  async mounted() {
    this.dataset = await this.datasetStore.getCurrentDataset();
    this.workflow = this.dataset.workflows[this.workflowID];

    let spinner = this.createLoading();

    spinner.close();

    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(1);

    this.workflow.currentRoute = this.$route.path;

    const validGithubConnection = await this.tokens.verifyGithubConnection();

    if (validGithubConnection) {
      this.validTokenAvailable = true;
      this.ready = true;
    } else {
      this.validTokenAvailable = false;
      this.ready = true;
    }
  },
};
</script>
