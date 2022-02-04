<template>
  <div
    class="flex h-full w-full max-w-screen-xl flex-col items-center justify-center p-3 pr-5"
  >
    <div class="flex h-full w-full flex-col">
      <span class="pb-1 text-left text-lg font-medium">
        Connect your GitHub account to Zenodo
      </span>
      <span class="text-left">
        Let's see if you GitHub account is already connected to Zenodo.
      </span>

      <el-divider class="my-4"> </el-divider>

      <div>
        <p v-if="validTokenAvailable" class="my-10 w-full text-center">
          Looks like we already have your Zenodo login details. Click on the
          'Start upload' button below.
        </p>
        <!-- show error message if token is not valid -->
        <div v-else class="flex flex-col items-center justify-center py-10">
          <p class="mb-5">
            We couldn't find your Zenodo login details. Please click on the
            button below to connect to your Zenodo account.
          </p>

          <!-- <ConnectZenodo :statusChangeFunction="showConnection"></ConnectZenodo> -->
        </div>
      </div>
      <!-- <LoadingFoldingCube v-else></LoadingFoldingCube> -->

      <div class="flex w-full flex-row justify-center space-x-4 py-2">
        <router-link
          :to="`/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/zenodo/metadata`"
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
          @click="uploadToZenodo"
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
// import LoadingFoldingCube from "@/components/spinners/LoadingFoldingCube";
// import ConnectZenodo from "@/components/serviceIntegration/ConnectZenodo";

import { useDatasetsStore } from "@/store/datasets";
// import { useTokenStore } from "@/store/access.js";

// import path from "path";
// import axios from "axios";
import { ElLoading } from "element-plus";

export default {
  name: "ZenodoGithubConnection",
  // components: { LoadingFoldingCube, ConnectZenodo },
  data() {
    return {
      datasetStore: useDatasetsStore(),
      // tokens: useTokenStore(),
      dataset: {},
      folderPath: "",
      workflowID: this.$route.params.workflowID,
      workflow: {},
      validTokenAvailable: false,
      errorMessage: "",
      zenodoAccessToken: "",
    };
  },
  //el-tree-node__content
  computed: {},
  methods: {
    createLoading() {
      const loading = ElLoading.service({
        lock: true,
        text: "Reading data...",
      });
      return loading;
    },

    async uploadToZenodo() {
      const routerPath = `/datasets/${this.datasetID}/${this.workflowID}/zenodo/upload`;
      if (this.validTokenAvailable) {
        this.$router.push({ path: routerPath });
      } else {
        const zenodoToken = this.zenodoAccessToken;
        const res = await this.checkToken(zenodoToken);

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
      // this.uploadToZenodo(); console.log(this.workflow.licenseText)
    },
  },
  async mounted() {
    this.dataset = await this.datasetStore.getCurrentDataset();
    this.workflow = this.dataset.workflows[this.workflowID];

    let spinner = this.createLoading();

    spinner.close();

    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(6);

    // prefill the zenodo secret value
    // create an interval based function and have it check through all the webhooks for the key

    this.workflow.currentRoute = this.$route.path;
  },
};
</script>
