<template>
  <div class="flex h-full w-full max-w-screen-lg flex-col items-center justify-center p-3 pr-5">
    <div class="flex h-full w-full flex-col">
      <h1 class="pb-1 pt-5 text-3xl font-bold text-slate-700">Manage Accounts</h1>

      <line-divider></line-divider>

      <h2>
        An overview of all your accounts connected to FAIRshare and the actions you can take are
        shown below.
      </h2>

      <div class="flex w-full flex-col items-center justify-center pt-5">
        <div class="card-container">
          <div class="image-container">
            <img src="../../assets/images/zenodologo.png" class="image" alt="zenodo logo" />
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

              <div class="centering-container tag-container" v-if="connectedToZenodo">
                <el-tag type="success" effect="plain" class="border-green-400 text-green-600">
                  <el-icon> <user-filled /> </el-icon>
                  <span class="px-2">
                    {{ zenodoDetails.name }}
                  </span>
                </el-tag>
              </div>
            </div>
            <div class="centering-container center">
              <p class="mt-1">
                Connect FAIRshare with your Zenodo account to allow us to upload your data directly
                to Zenodo. To learn more about connecting FAIRshare to Zenodo, please visit the
                <span
                  class="text-url"
                  @click="
                    openWebsite(
                      'https://docs.fairshareapp.io/docs/manage-accounts/connect-to-zenodo'
                    )
                  "
                >
                  Zenodo documentation</span
                >
                page.
              </p>
            </div>
            <div class="centering-container bottom">
              <ConnectZenodo></ConnectZenodo>
            </div>
          </div>
        </div>

        <div class="card-container">
          <div class="image-container">
            <img src="../../assets/images/githublogo.jpeg" class="image" alt="GitHub logo" />
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

              <div class="centering-container tag-container" v-if="connectedToGithub">
                <el-tag type="success" effect="plain" class="border-green-400 text-green-600">
                  <el-icon> <user-filled /> </el-icon>
                  <span class="px-2">
                    {{ githubDetails.name }}
                  </span>
                </el-tag>
              </div>
            </div>
            <div class="centering-container center">
              <p>
                Connect your GitHub account to FAIRshare to allow us to upload your data directly to
                GitHub. To learn more about connecting FAIRshare to GitHub, please visit the
                <span
                  class="text-url"
                  @click="
                    openWebsite(
                      'https://docs.fairshareapp.io/docs/manage-accounts/connect-to-github'
                    )
                  "
                >
                  GitHub documentation</span
                >
                page.
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
              src="../../assets/images/biotoolslogo.png"
              class="image p-6"
              alt="bio.tools logo"
            />
          </div>
          <div class="card-container-content">
            <div class="card-container-status">
              <div class="centering-container">
                <span
                  class="dot"
                  :class="{
                    'bg-green-600': connectedToBioTools,
                    'bg-gray-600': !connectedToBioTools,
                  }"
                ></span>
              </div>

              <div class="centering-container">
                <div
                  class="mr-2"
                  :class="{
                    'text-green-600': connectedToBioTools,
                    'text-gray-600': !connectedToBioTools,
                  }"
                >
                  {{ connectedToBioTools ? "Connected" : "Not Connected" }}
                </div>
              </div>

              <div class="centering-container tag-container" v-if="connectedToBioTools">
                <el-tag type="success" effect="plain" class="border-green-400 text-green-600">
                  <el-icon> <user-filled /> </el-icon>
                  <span class="px-2">
                    {{ bioToolsDetails.name }}
                  </span>
                </el-tag>
              </div>
            </div>
            <div class="centering-container center">
              <p>
                Connect your bio.tools account to FAIRshare to allow us to upload register your
                software directly through FAIRshare. To learn more about connecting FAIRshare to
                bio.tools, please visit the
                <span
                  class="text-url"
                  @click="
                    openWebsite(
                      'https://docs.fairshareapp.io/docs/manage-accounts/connect-to-bio-tools'
                    )
                  "
                >
                  bio.tools documentation</span
                >
                page.
              </p>
            </div>
            <div class="centering-container bottom">
              <ConnectBioTools></ConnectBioTools>
            </div>
          </div>
        </div>

        <div class="card-container">
          <div class="image-container">
            <img src="../../assets/images/figsharelogo.png" class="image p-6" alt="figshare logo" />
          </div>
          <div class="card-container-content">
            <div class="card-container-status">
              <div class="centering-container">
                <span
                  class="dot"
                  :class="{
                    'bg-green-600': connectedToFigshare,
                    'bg-gray-600': !connectedToFigshare,
                  }"
                ></span>
              </div>

              <div class="centering-container">
                <div
                  class="mr-2"
                  :class="{
                    'text-green-600': connectedToFigshare,
                    'text-gray-600': !connectedToFigshare,
                  }"
                >
                  {{ connectedToFigshare ? "Connected" : "Not Connected" }}
                </div>
              </div>

              <div class="centering-container tag-container" v-if="connectedToFigshare">
                <el-tag type="success" effect="plain" class="border-green-400 text-green-600">
                  <el-icon> <user-filled /> </el-icon>
                  <span class="px-2">
                    {{ figshareDetails.name }}
                  </span>
                </el-tag>
              </div>
            </div>
            <div class="centering-container center">
              <p>
                Connect your Figshare account to FAIRshare to allow us to upload register your
                software directly through FAIRshare. To learn more about connecting FAIRshare to
                Figshare, please visit the
                <span
                  class="text-url"
                  @click="
                    openWebsite(
                      'https://docs.fairshareapp.io/docs/manage-accounts/connect-to-figshare'
                    )
                  "
                >
                  Figshare documentation</span
                >
                page.
              </p>
            </div>
            <div class="centering-container bottom">
              <ConnectFigshare></ConnectFigshare>
            </div>
          </div>
        </div>
      </div>
    </div>
    <app-docs-link url="manage-accounts/overview" position="bottom-4" />
  </div>
</template>

<script>
import { useTokenStore } from "@/store/access";
import { useDatasetsStore } from "@/store/datasets";

import ConnectGithub from "@/components/serviceIntegration/ConnectGithub";
import ConnectZenodo from "@/components/serviceIntegration/ConnectZenodo";
import ConnectFigshare from "@/components/serviceIntegration/ConnectFigshare";
import ConnectBioTools from "@/components/serviceIntegration/ConnectBioTools";

export default {
  name: "ManageAccount",

  components: {
    ConnectGithub,
    ConnectZenodo,
    ConnectFigshare,
    ConnectBioTools,
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
    bioToolsDetails() {
      let bioToolsObject = {
        name: "",
      };
      if ("biotools" in this.manager.accessTokens) {
        bioToolsObject.name = this.manager.accessTokens.biotools.name;
      }
      return bioToolsObject;
    },
    connectedToBioTools() {
      return "biotools" in this.manager.accessTokens;
    },
    figshareDetails() {
      let figshareObject = {
        name: "",
      };
      if ("figshare" in this.manager.accessTokens) {
        figshareObject.name = this.manager.accessTokens.figshare.name;
      }
      return figshareObject;
    },
    connectedToFigshare() {
      return "figshare" in this.manager.accessTokens;
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

<style scoped lang="css">
.card-container {
  @apply my-5 flex  w-4/5 flex-row rounded-md border border-gray-200 py-3 shadow-lg transition-all;
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
  @apply flex  items-center justify-center;
}
.center {
  @apply py-3 pr-3;
}
.bottom {
  @apply items-end justify-end pb-3 pr-5;
}
.tag-container {
  @apply ml-2;
}
</style>
