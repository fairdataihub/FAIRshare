<template>
  <div
    class="flex h-full w-full max-w-screen-xl flex-col items-center justify-center p-3 pr-5"
  >
    <div class="flex h-full w-full flex-col">
      <h1 class="pb-1 text-left text-lg font-medium">
        Connect your GitHub account to Zenodo
      </h1>
      <h2 class="text-left">
        Let's see if you GitHub account is already connected to Zenodo.
      </h2>

      <el-divider class="my-4"> </el-divider>

      <div>
        <div v-if="validZenodoHookTokenFound" class="my-10">
          <div class="flex items-center justify-center">
            <p class="my-3 mx-2 font-medium text-emerald-400">
              We found a Zenodo webhook on your GitHub repository.
            </p>
            <Vue3Lottie
              animationLink="https://assets2.lottiefiles.com/packages/lf20_xvusaxau.json"
              :width="30"
              :height="30"
              :loop="1"
            />
          </div>
          <p class="my-3 w-full text-center">
            Your account has been setup for Zenodo integration. Let's move on to
            the next step.
          </p>
        </div>
        <!-- show how to connect to zenodo if no hook is found -->
        <div v-else class="flex w-full flex-col">
          <div class="mb-5 flex items-center justify-center">
            <h3 class="mx-2 font-normal text-secondary-600">
              We are not seeing any Zenodo connections already setup with
              GitHub.
            </h3>
            <Vue3Lottie
              animationLink="https://assets1.lottiefiles.com/private_files/lf30_lkauxe8i.json"
              :width="45"
              :height="45"
            />
          </div>

          <div>
            <p class="mb-2">
              To connect your GitHub account with Zenodo there are a few steps
              you need to do from your side.
            </p>
            <ul class="ml-2 list-inside list-disc">
              <li>
                Login to Zenodo and go to the Github connections in your profile
                settings. Alternatively, you can also click the button below to
                take you to the appropriate page.
              </li>

              <div class="my-2 flex w-full items-center justify-center">
                <button
                  class="secondary-plain-button my-1"
                  @click="openWebsite"
                >
                  Connect Github to Zenodo
                </button>
              </div>

              <li>
                Authenticate with Github and wait for your list of repositories
                to show up.
              </li>

              <li>
                Toggle the switch for the
                <span class="font-bold">
                  {{ selectedRepo }}
                </span>
                repository to the 'ON' position.
              </li>

              <li>Wait for FairShare to notice the change.</li>
            </ul>
            <p class="mt-2">
              You will only need to do this once. For any future GitHub
              repositories, Fair Share will automatically add the relevant
              connections for you.
            </p>
          </div>
        </div>
      </div>

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
          class="secondary-plain-button hidden"
          @click="showFilePreview"
          v-if="validZenodoHookTokenFound"
        >
          <el-icon><checked-icon /></el-icon>
          View files ready for upload
        </button>

        <button
          class="primary-button"
          :disabled="disableContinue"
          @click="uploadToZenodo"
          v-if="validZenodoHookTokenFound"
        >
          Start upload
          <el-icon> <d-arrow-right /> </el-icon>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { useDatasetsStore } from "@/store/datasets";
import { useTokenStore } from "@/store/access.js";

import axios from "axios";
import Vue3Lottie from "vue3-lottie";
import { ElLoading, ElNotification } from "element-plus";

import rippleLottieJSON from "@/assets/lotties/rippleLottie.json";

export default {
  name: "GithubZenodoConnection",
  components: {
    Vue3Lottie,
  },
  data() {
    return {
      datasetStore: useDatasetsStore(),
      tokens: useTokenStore(),
      dataset: {},
      folderPath: "",
      workflowID: this.$route.params.workflowID,
      workflow: {},
      validZenodoHookTokenFound: false,
      errorMessage: "",
      zenodoAccessToken: "",
      selectedRepo: "",
      rippleLottieJSON,
    };
  },
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
      if (this.validZenodoHookTokenFound) {
        this.$router.push({ path: routerPath });
      } else {
        const zenodoToken = this.zenodoAccessToken;
        const res = await this.checkToken(zenodoToken);

        if (res) {
          this.$router.push({ path: routerPath });
        }
      }
    },

    openWebsite() {
      const url = `${process.env.VUE_APP_ZENODO_URL}/account/settings/github`;
      window.ipcRenderer.send("open-link-in-browser", url);
    },

    async checkIfZenodoHookIsPresent() {
      const tokenObject = await this.tokens.getToken("github");
      const GithubAccessToken = tokenObject.token;
      // console.log(GithubAccessToken);

      let response = "";

      response = await axios
        .get(
          `${process.env.VUE_APP_GITHUB_SERVER_URL}/repos/${this.selectedRepo}/hooks`,
          {
            params: {
              per_page: 100,
            },
            headers: {
              Accept: "application/vnd.github.v3+json",
              Authorization: `Bearer ${GithubAccessToken}`,
            },
          }
        )
        .then((response) => {
          return response.data;
        })
        .catch((error) => {
          console.error(error);
          return "ERROR";
        });

      if (response !== "ERROR" && response.length > 0) {
        for (const webhook of response) {
          if (
            "config" in webhook &&
            "events" in webhook &&
            webhook.events.includes("release") &&
            "url" in webhook.config &&
            webhook.config.url.includes(
              `${process.env.VUE_APP_ZENODO_SERVER_URL}hooks/receivers/github/events/?access_token=`
            )
          ) {
            return response;
          } else {
            return false;
          }
        }
      } else {
        return false;
      }
    },

    async createGithubZenodoWebhook(GithubZenodoConnectionToken) {
      const tokenObject = await this.tokens.getToken("github");
      const GithubAccessToken = tokenObject.token;

      let response = "";

      const data = JSON.stringify({
        name: "web",
        config: {
          url: `https://sandbox.zenodo.org/api/hooks/receivers/github/events/?access_token=${GithubZenodoConnectionToken}`,
          content_type: "json",
          secret: "secret",
          insecure_ssl: 0,
        },
        events: ["release"],
        active: true,
      });

      const config = {
        method: "post",
        url: `${process.env.VUE_APP_GITHUB_SERVER_URL}/repos/${this.selectedRepo}/hooks`,
        headers: {
          Accept: "application/vnd.github.v3+json",
          Authorization: `Bearer ${GithubAccessToken}`,
          "Content-Type": "application/json",
        },
        data: data,
      };

      response = await axios(config)
        .then((response) => {
          console.log(response);
          if (response.status === 200 || response.status === 201) {
            return true;
          } else {
            return false;
          }
        })
        .catch((error) => {
          console.error(error);
          return "ERROR";
        });

      if (response !== "ERROR") {
        return response;
      } else {
        return false;
      }
    },
  },

  async mounted() {
    let spinner = this.createLoading();
    this.dataset = await this.datasetStore.getCurrentDataset();
    this.workflow = this.dataset.workflows[this.workflowID];

    this.selectedRepo = this.workflow.github.repo;

    this.datasetStore.showProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(6);

    const tokenObject = await this.tokens.getToken("github");
    const GithubZenodoConnectionToken = tokenObject.zenodoHookToken;
    // const GithubZenodoConnectionToken = false;

    if (GithubZenodoConnectionToken) {
      const response = await this.checkIfZenodoHookIsPresent();
      console.log(response);
      if (response) {
        this.validZenodoHookTokenFound = true;
      } else {
        ElNotification({
          title: "Info",
          message: "Creating a Zenodo webhook for this repository.",
          type: "info",
        });

        const tokenCreated = await this.createGithubZenodoWebhook(
          GithubZenodoConnectionToken
        );

        if (tokenCreated) {
          ElNotification({
            title: "Success",
            message: "Created a zenodo webhook for this repo successfully.",
            type: "success",
          });

          setTimeout(() => {
            this.validZenodoHookTokenFound = true;
          }, 1000);
        } else {
          ElNotification({
            title: "Error",
            message:
              "Could not create the Zenodo webhook automatically. Please connect your Zenodo account to the GitHub repository manually.",
            type: "error",
            duration: 10000,
          });
        }
      }
    } else {
      let interval = setInterval(async () => {
        const response = await this.checkIfZenodoHookIsPresent();
        console.log(response);
        if (response) {
          if (response.length > 0) {
            for (const webhook of response) {
              if (
                "config" in webhook &&
                "events" in webhook &&
                webhook.events.includes("release") &&
                "url" in webhook.config &&
                webhook.config.url.includes(
                  `${process.env.VUE_APP_ZENODO_SERVER_URL}hooks/receivers/github/events/?access_token=`
                )
              ) {
                const webhookConfigURL = webhook.config.url;
                const webhookConfigURLArray =
                  webhookConfigURL.split("access_token=");
                const webhookConfigURLToken = webhookConfigURLArray[1];
                console.log(webhookConfigURLToken);

                if (webhookConfigURLToken) {
                  const newTokenObject = JSON.parse(
                    JSON.stringify(await this.tokens.getToken("github"))
                  );
                  newTokenObject.zenodoHookToken = webhookConfigURLToken;

                  await this.tokens.saveToken("github", newTokenObject);
                }
              }
            }
          }

          this.validZenodoHookTokenFound = true;

          clearInterval(interval);
        }
      }, 5000);
    }

    this.workflow.currentRoute = this.$route.path;

    spinner.close();
  },
};
</script>
