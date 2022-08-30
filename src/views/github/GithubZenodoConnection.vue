<template>
  <div class="flex h-full w-full max-w-screen-xl flex-col items-center justify-center p-3 pr-5">
    <div class="flex h-full w-full flex-col">
      <h1 class="pb-1 text-left text-lg font-medium">Connect your GitHub account to Zenodo</h1>
      <p class="text-left">
        The easiest way to publish from GitHub to Zenodo is to leverage the existing linkage between
        the two platforms. Basically, you can link your GitHub account to Zenodo, and select
        directly from Zenodo, the GitHub repository you wish to publish on Zenodo. Then, everytime
        you publish a release on GitHub, it will be automatically deposited on Zenodo. We refer to
        the
        <span
          class="text-url"
          @click="
            openWebsite(
              'https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content'
            )
          "
        >
          relevant documentation on GitHub docs</span
        >
        for more details.
        <br />
        <br />
        FAIRshare will help you link your GitHub account with Zenodo then create a draft release on
        GitHub (after adding any requested metadata files to your GitHub repository) that you can
        publish from FAIRshare or the GitHub webpage to automatically create a deposit on Zenodo.
      </p>

      <div v-if="finishedLoading">
        <line-divider />
        <transition name="fade" mode="out-in" appear>
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
              Your account has been setup for Zenodo integration. Let's move on to the next step.
            </p>
          </div>
          <!-- show how to connect to zenodo if no hook is found -->
          <div v-else class="flex w-full flex-col">
            <div class="mb-5 flex items-center justify-center">
              <h3 class="mx-2 font-normal text-secondary-600">
                We are not seeing any Zenodo connections already setup with GitHub.
              </h3>
              <Vue3Lottie
                animationLink="https://assets1.lottiefiles.com/private_files/lf30_lkauxe8i.json"
                :width="45"
                :height="45"
              />
            </div>

            <div>
              <p class="mb-2">
                To connect your GitHub account with Zenodo there are a few steps you need to do from
                your side.
              </p>
              <ul class="ml-2 list-inside list-disc">
                <li>
                  Login to Zenodo and go to the GitHub connections in your profile settings.
                  Alternatively, you can also click the button below to take you to the appropriate
                  page.
                </li>

                <div class="my-2 flex w-full items-center justify-center">
                  <button class="secondary-plain-button my-1" @click="openWebsite">
                    Connect GitHub to Zenodo
                  </button>
                </div>

                <li>
                  Authenticate with GitHub and wait for your list of GitHub repositories to show up.
                </li>

                <li>
                  Toggle the switch for the
                  <span class="font-bold">
                    {{ selectedRepo }}
                  </span>
                  repository to the 'ON' position.
                </li>

                <li>Wait for FAIRshare to notice the change. This may take up to 30 seconds.</li>
              </ul>
            </div>
          </div>
        </transition>
      </div>

      <transition name="fade" mode="out-in" appear>
        <div class="flex w-full flex-row justify-center space-x-4 py-2" v-if="finishedLoading">
          <router-link
            :to="`/datasets/${this.$route.params.datasetID}/${this.$route.params.workflowID}/zenodo/metadata`"
            class=""
          >
            <button class="primary-plain-button">
              <el-icon><d-arrow-left /></el-icon> Back
            </button>
          </router-link>

          <button class="primary-button" @click="showSummary" v-if="validZenodoHookTokenFound">
            Continue
            <el-icon> <d-arrow-right /> </el-icon>
          </button>
        </div>
      </transition>
    </div>
    <app-docs-link url="curate-and-share/connect-github-zenodo" position="bottom-4" />
  </div>
</template>

<script>
import { useDatasetsStore } from "@/store/datasets";
import { useTokenStore } from "@/store/access.js";

import axios from "axios";
import { ElLoading } from "element-plus";

import rippleLottieJSON from "@/assets/lotties/rippleLottie.json";

export default {
  name: "GithubZenodoConnection",
  components: {},
  data() {
    return {
      datasetStore: useDatasetsStore(),
      tokens: useTokenStore(),
      dataset: {},
      folderPath: "",
      workflowID: this.$route.params.workflowID,
      workflow: {},
      GithubAccessToken: "",
      validZenodoHookTokenFound: false,
      errorMessage: "",
      zenodoAccessToken: "",
      selectedRepo: "",
      currentBranch: "",
      rippleLottieJSON,
      finishedLoading: false,
      interval: null,
    };
  },

  methods: {
    createLoading() {
      const loading = ElLoading.service({
        lock: true,
        text: "Reading GitHub repository...",
        background: "rgba(255, 255, 255, 0.97)",
      });
      return loading;
    },

    openWebsite() {
      const url = `${process.env.VUE_APP_ZENODO_URL}/account/settings/github`;
      window.ipcRenderer.send("open-link-in-browser", url);
    },

    async showSummary() {
      const routerPath = `/datasets/${this.datasetID}/${this.workflowID}/github/summary`;

      this.$router.push({ path: routerPath });
    },

    async checkIfZenodoHookIsPresent() {
      const tokenObject = await this.tokens.getToken("github");
      const GithubAccessToken = tokenObject.token;

      let response = "";

      response = await axios
        .get(`${process.env.VUE_APP_GITHUB_SERVER_URL}/repos/${this.selectedRepo}/hooks`, {
          params: {
            per_page: 100,
          },
          headers: {
            Accept: "application/vnd.github.v3+json",
            Authorization: `Bearer ${GithubAccessToken}`,
          },
        })
        .then((response) => {
          return response.data;
        })
        .catch((error) => {
          console.error(error);
          return "ERROR";
        });

      this.finishedLoading = true;

      if (response !== "ERROR" && response.length > 0) {
        for (const webhook of response) {
          if (
            typeof webhook === "object" &&
            "config" in webhook &&
            "events" in webhook &&
            webhook.events.includes("release") &&
            "url" in webhook.config &&
            webhook.config.url.includes(
              `${process.env.VUE_APP_ZENODO_SERVER_URL}/hooks/receivers/github/events/?access_token=`
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
          url: `${process.env.VUE_APP_ZENODO_SERVER_URL}/hooks/receivers/github/events/?access_token=${GithubZenodoConnectionToken}`,
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
    this.GithubAccessToken = tokenObject.token;
    // const GithubZenodoConnectionToken = tokenObject.zenodoHookToken;
    // const GithubZenodoConnectionToken = false;

    // if (GithubZenodoConnectionToken) {
    // const response = await this.checkIfZenodoHookIsPresent();

    // if (response) {
    //   this.validZenodoHookTokenFound = true;
    // } else {
    // this.$notify({
    //   title: "Info",
    //   message: "Creating a Zenodo webhook for this repository.",
    //   type: "info",
    // });
    // const tokenCreated = await this.createGithubZenodoWebhook(GithubZenodoConnectionToken);
    // if (tokenCreated) {
    //   ElNotification({
    //     title: "Success",
    //     message: "Created a zenodo webhook for this repo successfully.",
    //     type: "success",
    //   });
    //   setTimeout(() => {
    //     this.validZenodoHookTokenFound = true;
    //   }, 1000);
    // } else {
    //   ElNotification({
    //     title: "Error",
    //     message:
    //       "Could not create the Zenodo webhook automatically. Please connect your Zenodo account to the GitHub repository manually.",
    //     type: "error",
    //     duration: 10000,
    //   });
    // }
    // }
    // spinner.close();
    // } else {

    this.interval = setInterval(async () => {
      const response = await this.checkIfZenodoHookIsPresent();

      spinner.close();

      if (response) {
        // if (response.length > 0) {
        //   for (const webhook of response) {
        //     if (
        //       "config" in webhook &&
        //       "events" in webhook &&
        //       webhook.events.includes("release") &&
        //       "url" in webhook.config &&
        //       webhook.config.url.includes(
        //         `${process.env.VUE_APP_ZENODO_SERVER_URL}/hooks/receivers/github/events/?access_token=`
        //       )
        //     ) {
        //       const webhookConfigURL = webhook.config.url;
        //       const webhookConfigURLArray = webhookConfigURL.split("access_token=");
        //       const webhookConfigURLToken = webhookConfigURLArray[1];

        //       if (webhookConfigURLToken) {
        //         const newTokenObject = JSON.parse(
        //           JSON.stringify(await this.tokens.getToken("github"))
        //         );
        //         newTokenObject.zenodoHookToken = webhookConfigURLToken;
        //         await this.tokens.saveToken("github", newTokenObject);
        //       }
        //     }
        //   }
        // }

        this.validZenodoHookTokenFound = true;

        this.interval = clearInterval(this.interval);
      }
    }, 5000);

    // }

    this.workflow.currentRoute = this.$route.path;
  },
  beforeUnmount() {
    if (this.interval) {
      clearInterval(this.interval);
    }
  },
};
</script>
