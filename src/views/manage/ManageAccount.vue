<template>
  <div class="h-full w-full flex flex-col justify-center items-center pr-5 p-3">
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
              Connect with your github account by using an access token or
              OAuth. Please see more details at
              <span
                class="text-url"
                @click="
                  openWebsite(
                    'https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token'
                  )
                "
              >
                github access token documentation
              </span>
            </p>
          </div>
          <div class="centering-container bottom">
            <!-- <el-button
              plain
              class="button"
              @click="interactWithService('github')"
              :type="githubDetails.buttonStyle"
              >{{ githubDetails.action }}</el-button
            > -->
            <button
              :class="githubDetails.buttonStyle"
              @click="interactWithService('github')"
            >
              {{ githubDetails.action }}
            </button>
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
            <!-- <el-button
              plain
              class="button"
              @click="interactWithService('zenodo')"
              :type="zenodoDetails.buttonStyle"
              >{{ zenodoDetails.action }}</el-button
            > -->
            <button
              :class="zenodoDetails.buttonStyle"
              @click="interactWithService('zenodo')"
            >
              {{ zenodoDetails.action }}
            </button>
          </div>
        </div>
      </div>
    </div>
    <ButtonInputDialog
      v-model="dialogVisable"
      :numInput="dialogNumInput"
      :buttons="this.buttonList"
      :callback="closeButtonDialog"
    ></ButtonInputDialog>
  </div>
</template>

<script>
/* eslint-disable vue/no-unused-components */
import { useTokenStore } from "@/store/access";
import { useDatasetsStore } from "@/store/datasets";

import ButtonInputDialog from "@/components/dialogs/ButtonInputDialog";
import GithubTokenConnection from "@/components/serviceIntegration/GithubTokenConnection";
import ZenodoTokenConnection from "@/components/serviceIntegration/ZenodoTokenConnection";
import GithubOAuthConnection from "@/components/serviceIntegration/GithubOAuthConnection";

import { markRaw } from "vue";
import { ElNotification, ElMessageBox } from "element-plus";

export default {
  name: "ManageAccount",
  components: {
    GithubTokenConnection: GithubTokenConnection,
    ZenodoTokenConnection: ZenodoTokenConnection,
    GithubOAuthConnection: GithubOAuthConnection,
    ButtonInputDialog,
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
    closeButtonDialog() {
      this.dialogVisable = false;
      this.buttonList = [];
      this.dialogNumInput = 0;
    },
    APIkeyWarning(key) {
      ElMessageBox.confirm(
        "Disconnecting will delete the access token stored. Continue?",
        "Warning",
        {
          confirmButtonText: "OK",
          cancelButtonText: "Cancel",
          type: "warning",
        }
      )
        .then(async () => {
          this.deleteToken(key);
        })
        .catch(() => {
          ElNotification({
            type: "info",
            message: "Delete canceled",
            position: "bottom-right",
            duration: 2000,
          });
        });
    },
    async deleteToken(key) {
      let errorFound = false;
      try {
        await this.manager.deleteToken(key);
      } catch (e) {
        errorFound = true;
      }
      if (!errorFound) {
        ElNotification({
          type: "success",
          message: "Deleted",
          position: "bottom-right",
          duration: 2000,
        });
      }
    },
    interactWithService(serviceName) {
      if (serviceName == "github") {
        if ("github" in this.manager.accessTokens) {
          this.APIkeyWarning("github");
        } else {
          this.buttonList = [
            markRaw(GithubTokenConnection),
            markRaw(GithubOAuthConnection),
          ];
          this.dialogNumInput = 2;
          this.dialogVisable = true;
        }
      } else if (serviceName == "zenodo") {
        if ("zenodo" in this.manager.accessTokens) {
          this.APIkeyWarning("zenodo");
        } else {
          this.buttonList = [markRaw(ZenodoTokenConnection)];
          this.dialogNumInput = 1;
          this.dialogVisable = true;
        }
      }
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
  width: 800px;
  @apply flex flex-row h-44 py-3 my-5 rounded-sm shadow-lg;
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
