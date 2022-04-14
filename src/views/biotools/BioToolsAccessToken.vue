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

            <button class="primary-button" @click="showBioToolsConnectionPrompt">
              Connect to bio.tools
            </button>

            <login-prompt
              ref="loginPrompt"
              title="Login to bio.tools"
              confirmButtonText="Login"
              :preConfirm="checkUsernameAndPassword"
              :showErrors="showErrorMessage"
              @messageConfirmed="loginSuccess"
            >
              <div w-full>
                <p class="mb-3 w-full text-left text-base text-gray-500">
                  Please enter your login information to let us connect your bio.tools account.
                </p>

                <el-form
                  ref="loginForm"
                  :model="loginForm"
                  :rules="rules"
                  label-width="120px"
                  size="large"
                >
                  <el-form-item label="Username" prop="username">
                    <el-input
                      v-model="loginForm.username"
                      placeholder="username@bio.tools"
                      clearable
                      class="w-full"
                    />
                  </el-form-item>

                  <el-form-item label="Password" prop="password">
                    <el-input
                      v-model="loginForm.password"
                      type="password"
                      placeholder="**********"
                      clearable
                      class="w-full"
                    />
                  </el-form-item>
                </el-form>

                <fade-transition>
                  <p v-if="errorMessage !== ''" class="w-full text-center text-base text-red-600">
                    {{ errorMessage }}
                  </p>
                </fade-transition>
              </div>
            </login-prompt>
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
    <app-docs-link url="curate-and-share/zenodo-upload-summary" position="bottom-4" />
  </div>
</template>

<script>
import LoadingFoldingCube from "@/components/spinners/LoadingFoldingCube";

import { useDatasetsStore } from "@/store/datasets";
import { useTokenStore } from "@/store/access.js";

import axios from "axios";

import { ElLoading } from "element-plus";

export default {
  name: "BioToolsAccessToken",
  components: { LoadingFoldingCube },
  data() {
    return {
      datasetStore: useDatasetsStore(),
      tokenStore: useTokenStore(),
      dataset: {},
      folderPath: "",
      workflowID: this.$route.params.workflowID,
      workflow: {},
      validTokenAvailable: false,
      errorMessage: "",
      biotoolsAccessToken: "",
      loginForm: {
        username: "",
        password: "",
      },
      rules: {
        username: [{ required: true, message: "Please enter your username", trigger: "blur" }],
        password: [{ required: true, message: "Please enter your password", trigger: "blur" }],
      },

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
            this.$router.push({
              path: `/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/zenodo/publish`,
            });
          }
        }
      }
    },
    showBioToolsConnectionPrompt() {
      this.$refs.loginPrompt.show();
    },
    loginSuccess() {
      this.$notify({
        title: "Success",
        message: "You have successfully logged in to bio.tools",
        type: "success",
        position: "bottom-right",
      });
      this.validTokenAvailable = true;
    },
    async checkUsernameAndPassword() {
      if (this.loginForm.username === "" || this.loginForm.password === "") {
        return "empty";
      } else {
        const response = await axios
          .post(`${this.$server_url}/biotools/login`, {
            username: this.loginForm.username,
            password: this.loginForm.password,
          })
          .then(async (response) => {
            if ("general_errors" in response.data) {
              return "invalid";
            }

            if ("key" in response.data) {
              const token = response.data.key;
              const userDetails = await axios
                .get(`${this.$server_url}/biotools/user`, {
                  params: {
                    token,
                  },
                })
                .then(async (res) => {
                  if ("email" in res.data) {
                    return res.data;
                  }
                });

              let tokenObject = {};

              tokenObject.token = token;
              tokenObject.name = userDetails.email;
              tokenObject.type = "token";

              await this.tokenStore.saveToken("biotools", tokenObject);
              this.$track("Connections", "bio.tools", "connected");

              return "valid";
            }
          })
          .catch((error) => {
            console.error(error);
            return "ERROR";
          });

        return response;
      }
    },
    startBioToolsRegistration() {
      const routerPath = `/datasets/${this.datasetID}/${this.workflowID}/biotools/metadata`;
      this.$router.push({ path: routerPath });
    },
    showErrorMessage(message) {
      this.errorMessage = message;
    },
  },
  async mounted() {
    this.dataset = await this.datasetStore.getCurrentDataset();
    this.workflow = this.dataset.workflows[this.workflowID];

    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(6);

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
