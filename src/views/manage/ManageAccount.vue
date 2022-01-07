<template>
  <div
    class="h-full w-full flex flex-col justify-center items-center pr-5 p-3 max-w-screen-lg"
  >
    <div class="flex flex-col h-full w-full items-center">
      <div class="card-container">
        <div class="image-container">
          <img src="../../assets/github.jpeg" class="image" />
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
                class="text-green-600 border-green-400"
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
                GitHub access token documentation
              </span>
            </p>
          </div>
          <div class="centering-container bottom">
            <ConnectGithub></ConnectGithub>
          </div>
        </div>
      </div>

      <div class="card-container">
        <div class="image-container">
          <img
            src="https://about.zenodo.org/static/img/logos/zenodo-black-2500.png"
            class="image"
          />
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
                class="text-green-600 border-green-400"
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
              Connect with your zenodo account by using an access token. Please
              see more details at
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
    </div>
  </div>
</template>

<script>
/* eslint-disable vue/no-unused-components */
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
  setup() {
    const manager = useTokenStore();
    return {
      manager,
    };
  },
  data() {
    return {
      datasetStore: useDatasetsStore(),
      buttonList: [],
      dialogVisable: false,
      dialogNumInput: 0,
    };
  },
  methods: {
    openWebsite(url) {
      window.ipcRenderer.send("open-link-in-browser", url);
    },
  },
  computed: {
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

    this.datasetStore.hideProgressBar();
    this.datasetStore.setProgressBarType("github");
    this.datasetStore.setCurrentStep(2);

    await this.manager.loadTokens();
  },
};
</script>

<style scoped>
.card-container {
  @apply flex flex-row  py-3 my-5 rounded-sm shadow-lg w-4/5 h-[220px] transition-all;
}
.image-container {
  @apply h-full w-4/12 flex justify-center items-center;
}
.card-container-content {
  @apply flex flex-col w-8/12 px-2 h-full;
}
.dot {
  @apply h-[12px] w-[12px] rounded-full mr-2;
}
.card-container-status {
  @apply flex flex-row justify-start items-center h-1/5;
}
.centering-container {
  @apply flex justify-center items-center h-2/5;
}
.center {
  @apply py-3 pr-3;
}
.bottom {
  @apply justify-end items-end pr-5 pb-3;
}
.tag-container {
  @apply ml-2;
}
</style>
