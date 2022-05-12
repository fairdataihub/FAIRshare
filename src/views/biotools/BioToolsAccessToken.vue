<template>
  <div class="flex h-full w-full max-w-screen-xl flex-col items-center justify-center p-3 pr-5">
    <div class="flex h-full w-full flex-col">
      <span class="text-left text-lg font-medium"> Login to bio.tools </span>
      <!-- <span class="text-left">
        We will use this to upload and edit your dataset on your Zenodo account.
      </span> -->

      <el-divider class="my-4"> </el-divider>

      <fade-transition>
        <div v-if="ready">
          <p v-if="validTokenAvailable" class="my-10 w-full text-center">
            It looks like you have already connected your bio.tools account with FAIRshare. <br />
            Click on the 'Continue' button below to start the registration process of your software
            <br />
          </p>
          <!-- show error message if token is not valid -->
          <div v-else class="flex flex-col items-center justify-center py-10 text-center">
            <p class="mb-5">
              We couldn't find your bio.tools account details. <br />
              Please click on the button below to connect to your bio.tools account to register your
              software.
            </p>

            <!-- <button class="primary-button" @click="showBioToolsConnectionPrompt">
              Connect to bio.tools
            </button> -->
            <ConnectBioTools :statusChangeFunction="showConnection" />
          </div>
        </div>
        <LoadingFoldingCube v-else></LoadingFoldingCube>
      </fade-transition>

      <fade-transition>
        <div class="flex w-full flex-row justify-center space-x-4 py-2" v-if="validTokenAvailable">
          <button class="primary-plain-button" @click="navigateBack">
            <el-icon><d-arrow-left /></el-icon> Back
          </button>

          <button
            class="primary-button"
            @click="startBioToolsRegistration"
            v-if="validTokenAvailable"
          >
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
import ConnectBioTools from "@/components/serviceIntegration/ConnectBioTools";

import { useDatasetsStore } from "@/store/datasets";
import { useTokenStore } from "@/store/access.js";

import { ElLoading } from "element-plus";

export default {
  name: "BioToolsAccessToken",
  components: { LoadingFoldingCube, ConnectBioTools },
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
      if ("uploadToRepo" in this.workflow && this.workflow.uploadToRepo === true) {
        if ("source" in this.workflow) {
          if (this.workflow.source.type === "github") {
            this.$router.push({
              path: `/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/githubNoUpload/finalPage`,
            });
          }
          if (this.workflow.source.type === "local") {
            this.$router.push({
              path: `/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/localNoUpload/finalPage`,
            });
          }
        }
      } else {
        if ("source" in this.workflow) {
          if (this.workflow.source.type === "github") {
            this.$router.push({
              path: `/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/github/publish`,
            });
          }
          if (this.workflow.source.type === "local") {
            this.workflow.destination.name;
            if ("name" in this.workflow.destination) {
              const destination = this.workflow.destination.name;
              this.$router.push({
                path: `/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/${destination}/publish`,
              });
            } else {
              this.$router.push({
                path: `/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}`,
              });
            }
          }
        }
      }
    },

    startBioToolsRegistration() {
      const routerPath = `/datasets/${this.datasetID}/${this.workflowID}/biotools/metadata`;
      this.$router.push({ path: routerPath });
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

    const validBioToolsConnection = await this.tokenStore.verifyBioToolsConnection();

    if (validBioToolsConnection) {
      this.validTokenAvailable = true;
    } else {
      this.validTokenAvailable = false;
    }

    this.ready = true;
  },
};
</script>
