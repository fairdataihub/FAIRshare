<template>
  <div class="flex h-full w-full max-w-screen-xl flex-col items-center justify-center p-3 pr-5">
    <div class="flex h-full w-full flex-col">
      <span class="text-left text-lg font-medium"> Login to Figshare </span>
      <!-- <span class="text-left">
        We will use this to upload and edit your dataset on your Figshare account.
      </span> -->

      <el-divider class="my-4"> </el-divider>

      <fade-transition>
        <div v-if="ready">
          <div class="flex justify-center pt-3 pb-1" v-if="validTokenAvailable">
            <Vue3Lottie
              animationLink="https://assets9.lottiefiles.com/packages/lf20_0jomt6wm.json"
              :width="100"
              :height="100"
              :loop="1"
            />
          </div>

          <p v-if="validTokenAvailable" class="my-10 w-full text-center">
            <span class="text-lg">
              It looks like you have already connected your Figshare account with FAIRshare. <br />
            </span>
            Click on the 'Continue' button below to start the upload process of your dataset.
            <br />
          </p>
          <!-- show error message if token is not valid -->
          <div v-else class="flex flex-col items-center justify-center py-10 text-center">
            <p class="mb-5">
              We couldn't find your Figshare account details. <br />
              Please click on the button below to connect to your Figshare account to upload your
              dataset.
            </p>

            <!-- <button class="primary-button" @click="showBioToolsConnectionPrompt">
              Connect to bio.tools
            </button> -->
            <ConnectFigshare :statusChangeFunction="showConnection" />
          </div>
        </div>
        <LoadingFoldingCube v-else></LoadingFoldingCube>
      </fade-transition>

      <fade-transition>
        <div class="flex w-full flex-row justify-center space-x-4 py-2">
          <button class="primary-plain-button" @click="navigateBack">
            <el-icon><d-arrow-left /></el-icon> Back
          </button>

          <button class="primary-button" @click="uploadToFigshare" v-if="validTokenAvailable">
            Continue
            <el-icon> <d-arrow-right /> </el-icon>
          </button>
        </div>
      </fade-transition>
    </div>

    <!-- <app-docs-link url="curate-and-share/zenodo-upload-summary" position="bottom-4" /> -->
  </div>
</template>

<script>
import LoadingFoldingCube from "@/components/spinners/LoadingFoldingCube";
import ConnectFigshare from "@/components/serviceIntegration/ConnectFigshare";

import { useDatasetsStore } from "@/store/datasets";
import { useTokenStore } from "@/store/access.js";

import { ElLoading } from "element-plus";

export default {
  name: "FigshareAccessToken",
  components: { LoadingFoldingCube, ConnectFigshare },
  data() {
    return {
      datasetStore: useDatasetsStore(),
      tokenStore: useTokenStore(),
      dataset: {},
      folderPath: "",
      workflowID: this.$route.params.workflowID,
      workflow: {},
      validTokenAvailable: false,
      ready: false,
      showContinueSection: false,
      showLoading: false,
    };
  },
  methods: {
    createLoading() {
      const loading = ElLoading.service({
        lock: true,
        text: "Reading data...",
      });
      return loading;
    },
    openWebsite(url) {
      window.ipcRenderer.send("open-link-in-browser", url);
    },
    navigateBack() {
      this.$router.push({
        path: `/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/figshare/metadata`,
      });
    },

    uploadToFigshare() {
      const routerPath = `/datasets/${this.datasetID}/${this.workflowID}/figshare/upload`;
      if (this.validTokenAvailable) {
        this.$router.push({ path: routerPath });
      }
    },

    async showConnection(status) {
      console.log(status);
      if (status === "connected") {
        this.validTokenAvailable = true;
      }
    },
  },
  async mounted() {
    this.dataset = await this.datasetStore.getCurrentDataset();
    this.workflow = this.dataset.workflows[this.workflowID];

    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(8);

    // this.workflow.currentRoute = this.$route.path;

    const validFigshareConnection = await this.tokenStore.verifyFigshareConnection();

    if (validFigshareConnection) {
      this.validTokenAvailable = true;
    } else {
      this.validTokenAvailable = false;
    }

    this.ready = true;
  },
};
</script>
