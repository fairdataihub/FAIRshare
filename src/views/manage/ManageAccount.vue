<template>
  <div
    class="flex h-full w-full max-w-screen-lg flex-col items-center justify-center p-3 pr-5"
  >
    <div class="flex h-full w-full flex-col">
      <h1 class="pt-5 pb-1 text-3xl font-bold text-slate-700">
        Manage Accounts
      </h1>

      <line-divider></line-divider>

      <h2>
        An overview of all your accounts connected to FAIRshare and the actions
        you can take are shown below.
      </h2>

      <div class="flex w-full flex-col items-center justify-center pt-5">
        <div class="card-container">
          <div class="image-container">
            <img src="../../assets/images/zenodologo.png" class="image" />
          </div>
          <div class="card-container-content">
            <div class="card-container-status">
              <div class="centering-container">
                <span
                  class="dot"
                  :class="{
                    'bg-green-600': connectedToZenodo,
                    'bg-gray-600': !connectedToZenodo,
                  }"
                ></span>
              </div>

              <div class="centering-container">
                <div
                  class="mr-2"
                  :class="{
                    'text-green-600': connectedToZenodo,
                    'text-gray-600': !connectedToZenodo,
                  }"
                >
                  {{ zenodoDetails.status }}
                </div>
              </div>

              <div
                class="centering-container tag-container"
                v-if="connectedToZenodo"
              >
                <el-tag
                  type="success"
                  effect="plain"
                  class="border-green-400 text-green-600"
                >
                  <el-icon> <user-filled /> </el-icon>
                  <span class="px-2">
                    {{ zenodoDetails.name }}
                  </span>
                </el-tag>
              </div>
            </div>
            <div class="centering-container center">
              <p>
                Connect with your zenodo account by using an access token.
                Please see more details at
                <span
                  class="text-url"
                  @click="
                    openWebsite(
                      'https://developers.zenodo.org/#quickstart-upload'
                    )
                  "
                >
                  zenodo access token documentation.
                </span>
              </p>
            </div>
            <div class="centering-container bottom">
              <ConnectZenodo></ConnectZenodo>
            </div>
          </div>
        </div>

        <div class="card-container">
          <div class="image-container">
            <img src="../../assets/images/githublogo.jpeg" class="image" />
          </div>
          <div class="card-container-content">
            <div class="card-container-status">
              <div class="centering-container">
                <span
                  class="dot"
                  :class="{
                    'bg-green-600': connectedToGithub,
                    'bg-gray-600': !connectedToGithub,
                  }"
                ></span>
              </div>

              <div class="centering-container">
                <div
                  class="mr-2"
                  :class="{
                    'text-green-600': connectedToGithub,
                    'text-gray-600': !connectedToGithub,
                  }"
                >
                  {{ githubDetails.status }}
                </div>
              </div>

              <div
                class="centering-container tag-container"
                v-if="connectedToGithub"
              >
                <el-tag
                  type="success"
                  effect="plain"
                  class="border-green-400 text-green-600"
                >
                  <el-icon> <user-filled /> </el-icon>
                  <span class="px-2">
                    {{ githubDetails.name }}
                  </span>
                </el-tag>
              </div>
            </div>
            <div class="centering-container center">
              <p>
                Connect with your GitHub account by using an access token or
                OAuth. Please see more details at
                <span
                  class="text-url"
                  @click="
                    openWebsite(
                      'https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token'
                    )
                  "
                >
                  GitHub access token documentation.
                </span>
              </p>
            </div>
            <div class="centering-container bottom">
              <ConnectGithub></ConnectGithub>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useTokenStore } from "@/store/access";
import { useDatasetsStore } from "@/store/datasets";

import ConnectGithub from "@/components/serviceIntegration/ConnectGithub";
import ConnectZenodo from "@/components/serviceIntegration/ConnectZenodo";

export default {
  name: "ManageAccount",

  components: {
    ConnectGithub,
    ConnectZenodo,
  },

  data() {
    return {
      datasetStore: useDatasetsStore(),
      manager: useTokenStore(),
      buttonList: [],
      dialogVisible: false,
      dialogNumInput: 0,
    };
  },

  methods: {
    openWebsite(url) {
      window.ipcRenderer.send("open-link-in-browser", url);
    },
  },

  computed: {
    // zenodo status
    zenodoDetails() {
      let zenodoObject = {
        status: "Not Connected",
        name: "",
        action: "Connect",
        buttonStyle: "primary-plain-button",
      };
      if ("zenodo" in this.manager.accessTokens) {
        zenodoObject.status = "Connected";
        zenodoObject.name = this.manager.accessTokens.zenodo.name;
        zenodoObject.action = "Disconnect";
        zenodoObject.buttonStyle = "danger-plain-button";
      }
      return zenodoObject;
    },
    connectedToZenodo() {
      return "zenodo" in this.manager.accessTokens;
    },
    // github status
    githubDetails() {
      let githubObject = {
        status: "Not Connected",
        name: "",
        action: "Connect",
        buttonStyle: "primary-plain-button",
      };
      if ("github" in this.manager.accessTokens) {
        githubObject.status = "Connected";
        githubObject.name = this.manager.accessTokens.github.name;
        githubObject.action = "Disconnect";
        githubObject.buttonStyle = "danger-plain-button";
      }
      return githubObject;
    },
    connectedToGithub() {
      return "github" in this.manager.accessTokens;
    },
  },

  async mounted() {
    this.datasetStore.hideProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(1);

    await this.manager.loadTokens();
  },
};
</script>

<style scoped>
.card-container {
  @apply my-5 flex h-[220px] w-4/5 flex-row rounded-md border border-gray-200 py-3 shadow-lg transition-all;
}
.image-container {
  @apply flex h-full w-4/12 items-center justify-center;
}
.card-container-content {
  @apply flex h-full w-8/12 flex-col px-2;
}
.dot {
  @apply mr-2 h-[12px] w-[12px] rounded-full;
}
.card-container-status {
  @apply flex h-1/5 flex-row items-center justify-start;
}
.centering-container {
  @apply flex h-2/5 items-center justify-center;
}
.center {
  @apply py-3 pr-3;
}
.bottom {
  @apply items-end justify-end pr-5 pb-3;
}
.tag-container {
  @apply ml-2;
}
</style>
