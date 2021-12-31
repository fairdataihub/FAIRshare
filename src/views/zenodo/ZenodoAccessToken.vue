<template>
  <div class="h-full w-full flex flex-col justify-center items-center pr-5 p-3">
    <div class="flex flex-col h-full w-full">
      <span class="text-lg font-medium text-left">
        Zenodo connection details
      </span>
      <span class="text-left">
        Let's see if we already have your Zenodo login details. We will use this
        to upload and edit your dataset on your Zenodo account.
      </span>

      <el-divider class="my-4"> </el-divider>

      <div v-if="ready">
        <p v-if="validTokenAvailable" class="my-10 text-center w-full">
          Looks like we already have your Zenodo login details. Click on the
          continue button below.
        </p>
        <!-- show error message if token is not valid -->
        <div v-else class="flex flex-col justify-center items-center py-10">
          <p class="mb-5">
            We couldn't find your Zenodo login details. Please click on the
            button below to connect to your Zenodo account.
          </p>

          <ZenodoTokenConnectionVue
            :callbackFunction="showConnection"
          ></ZenodoTokenConnectionVue>

          <!-- <el-input
            v-model="zenodoAccessToken"
            placeholder="Zenodo Access Token"
            class="mb-10"
          /> -->
        </div>
      </div>
      <LoadingFoldingCube v-else></LoadingFoldingCube>

      <div class="w-full flex flex-row justify-center py-2 space-x-4">
        <router-link
          :to="`/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/zenodo/metadata`"
          class=""
        >
          <el-button type="danger" plain>
            <el-icon><d-arrow-left /></el-icon> Back
          </el-button>
        </router-link>

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
// import axios from "axios";

import LoadingFoldingCube from "@/components/spinners/LoadingFoldingCube.vue";
import ZenodoTokenConnectionVue from "@/components/serviceIntegration/ZenodoTokenConnection.vue";

import { useDatasetsStore } from "@/store/datasets";
import { useTokenStore } from "@/store/access.js";

export default {
  name: "ZenodoAccessToken",
  components: { LoadingFoldingCube, ZenodoTokenConnectionVue },
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
      zenodoAccessToken: "",
      ready: false,
    };
  },
  computed: {
    disableContinue() {
      if (this.validTokenAvailable) {
        return false;
      }
      if (!this.validTokenAvailable && this.zenodoAccessToken !== "") {
        return false;
      }
      return true;
    },
  },
  methods: {
    // async getDepositions(token) {
    //   return await axios
    //     .get(`${process.env.VUE_APP_ZENODO_SERVER_URL}deposit/depositions`, {
    //       params: {
    //         access_token: token,
    //       },
    //     })
    //     .then((response) => {
    //       return { data: response.data, status: response.status };
    //     })
    //     .catch((error) => {
    //       return { data: error.response.data, status: error.response.status };
    //     });
    // },
    async checkToken(token) {
      console.log(token);
      const response = await this.tokens.getDepositions(token);

      if (response.status === 200) {
        this.validTokenAvailable = true;
        this.tokens.saveToken("zenodo", token);
        return true;
      } else if (response.status === 401) {
        this.errorMessage =
          "Invalid Zenodo access token. Please enter a valid Zenodo access token.";
        this.validTokenAvailable = false;
        return false;
      } else {
        this.errorMessage = "Something went wrong. Please try again.";
        this.validTokenAvailable = false;
        return false;
      }
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
    async showConnection() {
      this.validTokenAvailable = true;
      // this.uploadToZenodo();
    },
  },
  async mounted() {
    this.dataset = await this.datasetStore.getCurrentDataset();
    this.workflow = this.dataset.workflows[this.workflowID];

    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(5);

    const validZenodoConnection = await this.tokens.verifyZenodoConnection();

    // console.log(validZenodoConnection);

    if (validZenodoConnection) {
      this.validTokenAvailable = true;
      this.ready = true;
    } else {
      this.validTokenAvailable = false;
      this.ready = true;
    }

    // const zenodoTokenObject = await this.tokens.getToken("zenodo");
    // const zenodoToken = zenodoTokenObject.token;
    // console.log(zenodoTokenObject);
    // if (zenodoToken === "NO_TOKEN_FOUND") {
    //   this.errorMessage =
    //     "No Zenodo access token found. Please enter a valid Zenodo access token.";
    //   this.validTokenAvailable = false;
    //   this.ready = true;
    // } else {
    //   await this.checkToken(zenodoToken);
    //   this.ready = true;
    // }
  },
};
</script>

<style lang="postcss" scoped></style>
