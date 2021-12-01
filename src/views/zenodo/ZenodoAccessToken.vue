<template>
  <div class="h-screen w-full flex flex-row lg:justify-center items-center">
    <div class="p-3 h-full w-full lg:w-auto flex flex-row items-center">
      <div class="h-full w-full">
        <div class="flex flex-col h-full overflow-y-auto pr-5">
          <workflow-progress-bar :currentStep="5" />

          <span class="text-lg font-medium text-left">
            Zenodo Access Token Verification
          </span>
          <span class="text-left">
            Let's see if we already have your Zenodo login details
          </span>

          <el-divider class="my-4"> </el-divider>

          <div v-if="ready">
            <span v-if="validTokenAvailable" class="mb-10">
              Looks like we already have your Zenodo login details. Click on the
              continue button below.
            </span>
            <!-- show error message if token is not valid -->
            <div v-if="errorMessage !== ''">
              <p class="mb-5">
                {{ errorMessage }}
              </p>

              <el-input
                v-model="zenodoAccessToken"
                placeholder="Zenodo Access Token"
                class="mb-10"
              />
            </div>
          </div>
          <LoadingFoldingCube v-else></LoadingFoldingCube>

          <div class="w-full flex flex-row justify-center py-2">
            <router-link
              :to="`/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/zenodo/review`"
              class="mx-6"
            >
              <el-button type="danger" plain> Back </el-button>
            </router-link>

            <el-button
              type="primary"
              class="flex flex-row items-center"
              :disabled="disableContinue"
              @click="uploadToZenodo"
            >
              Continue
              <el-icon>
                <ArrowRightBold />
              </el-icon>
            </el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import { Icon } from "@iconify/vue";
import { ArrowRightBold } from "@element-plus/icons";
import axios from "axios";

import LoadingFoldingCube from "../../components/spinners/LoadingFoldingCube.vue";

import { useDatasetsStore } from "../../store/datasets";
import { useTokenStore } from "../../store/access.js";

export default {
  name: "ZenodoAccessToken",
  components: { ArrowRightBold, LoadingFoldingCube },
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
    async getDepositions(token) {
      return await axios
        .get(`${process.env.VUE_APP_ZENODO_SERVER_URL}deposit/depositions`, {
          params: {
            access_token: token,
          },
        })
        .then((response) => {
          return { data: response.data, status: response.status };
        })
        .catch((error) => {
          return { data: error.response.data, status: error.response.status };
        });
    },
    async checkToken(token) {
      const response = await this.getDepositions(token);

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
  },
  async mounted() {
    this.dataset = await this.datasetStore.getCurrentDataset();
    this.workflow = this.dataset.workflows[this.workflowID];

    const zenodoToken = await this.tokens.getToken("zenodo");
    if (zenodoToken === "NO_TOKEN_FOUND") {
      this.errorMessage =
        "No Zenodo access token found. Please enter a valid Zenodo access token.";
      this.validTokenAvailable = false;
      this.ready = true;
    } else {
      await this.checkToken(zenodoToken);
      this.ready = true;
    }
  },
};
</script>

<style lang="postcss" scoped></style>
