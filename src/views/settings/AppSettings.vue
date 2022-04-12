<template>
  <div class="flex h-full w-full max-w-screen-lg flex-col items-center justify-center p-3 pr-5">
    <div class="flex h-full w-full flex-col">
      <h1 class="pt-5 pb-1 text-3xl font-bold text-slate-700">Application Settings</h1>

      <line-divider></line-divider>

      <el-tabs v-model="activeName" class="settings-tabs w-11/12 py-5" tab-position="right">
        <el-tab-pane label="General" name="general">
          <div class="flex flex-col space-y-4 px-3">
            <!-- settings panel -->
            <div class="rounded-lg border-2 border-slate-100 p-4">
              <h2 class="mb-2 text-lg font-semibold text-neutral-700">Allow beta versions?</h2>
              <div class="flex flex-col items-start">
                <p class="mb-2 text-sm">
                  Do you want to allow FAIRshare to download and update to beta versions of the
                  application? Beta versions may not yet be stable and may contain bugs but you will
                  be able to preview and test the latest features ahead of time.
                </p>
                <div class="flex w-full justify-between">
                  <div class="flex items-center">
                    <div
                      class="flex items-center transition-all"
                      :class="{
                        'text-secondary-500': !betaRelease,
                        'text-secondary-200': betaRelease,
                      }"
                    >
                      <el-icon> <circle-close-filled /> </el-icon>
                    </div>
                    <el-tooltip :content="betaRelease ? 'Enabled' : 'Disabled'" placement="bottom">
                      <el-switch
                        v-model="betaRelease"
                        class="mx-1"
                        active-color="#2563eb"
                        inactive-color="#fdba74"
                        @change="changeUpdateChannel"
                      />
                    </el-tooltip>
                    <div
                      class="flex items-center transition-all"
                      :class="{
                        'text-primary-200': !betaRelease,
                        'text-primary-500': betaRelease,
                      }"
                    >
                      <el-icon> <circle-check-filled /> </el-icon>
                    </div>
                  </div>
                  <fade-transition>
                    <button
                      class="secondary-plain-button mx-3 px-2 py-0"
                      @click="checkForUpdates"
                      v-if="showCheckForUpdates"
                    >
                      Check for Updates
                      <el-icon class="ml-2"><refresh-icon /></el-icon>
                    </button>
                  </fade-transition>
                </div>
                <p class="mt-2 text-xs text-neutral-500">
                  Modifying this value will allow you to update to beta versions the next time you
                  start the app.
                </p>
              </div>
            </div>
          </div>
        </el-tab-pane>
        <el-tab-pane label="Advanced" name="proxy">
          <div class="flex flex-col space-y-4 px-3">
            <div class="rounded-lg border-2 border-slate-100 p-4">
              <h2 class="py-2 text-lg font-semibold text-slate-600">Configuration Folder</h2>
              <div class="flex flex-col items-start">
                <p class="mb-2">
                  The FAIRshare configuration folder holds key information regarding your projects,
                  access tokens and datasets.
                  <br />
                  <span class="text-xs font-medium text-zinc-500">
                    You should not modify this folder unless you know what you are doing.
                  </span>
                </p>
                <button @click="openFileExplorer('configFolder')" class="secondary-plain-button">
                  Open the config folder
                </button>
              </div>
            </div>

            <div class="rounded-lg border-2 border-slate-100 p-4">
              <h2 class="py-2 text-lg font-semibold text-slate-600">Logs Folder</h2>
              <div class="flex flex-col items-start">
                <p class="mb-2">
                  Our backend service will create logs for errors that are shown in the UI. Click
                  the button to open the logs folder.
                  <br />
                  <span class="text-xs font-medium text-zinc-500">
                    This is only intended to be used for debugging purposes.
                  </span>
                </p>
                <button @click="openFileExplorer('backendLogs')" class="secondary-plain-button">
                  Open the logs folder
                </button>
              </div>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
    <transition name="fade" mode="out-in" appear>
      <div class="fixed bottom-2 right-3" v-show="loadingSpinner">
        <Vue3Lottie
          animationLink="https://assets7.lottiefiles.com/packages/lf20_WXXDFD.json"
          :width="100"
          :height="100"
          :loop="1"
        />
      </div>
    </transition>
    <app-docs-link url="manage-app-settings/overview" position="bottom-4" />
  </div>
</template>

<script>
import { app } from "@electron/remote";
import axios from "axios";
import path from "path";

import { useDatasetsStore } from "@/store/datasets";
import { useConfigStore } from "@/store/config";
import FadeTransition from "@/components/transitions/FadeTransition.vue";

export default {
  name: "AppSettings",
  components: { FadeTransition },
  data() {
    return {
      datasetStore: useDatasetsStore(),
      configStore: useConfigStore(),
      activeName: "general",
      loadingSpinner: false,
      config: {},
      betaRelease: false,
      showCheckForUpdates: false,
    };
  },
  methods: {
    async changeUpdateChannel(enabled) {
      this.showCheckForUpdates = true;
      if (enabled) {
        this.config.releaseChannel = "beta";
      } else {
        this.config.releaseChannel = "latest";
      }
      await this.configStore.addConfig("releaseChannel", this.config.releaseChannel);
    },
    openFileExplorer(type) {
      this.loadingSpinner = true;

      let customPath = "";

      if (type === "configFolder") {
        customPath = path.join(app.getPath("home"), ".fairshare", "accessTokens.json");
      } else if (type === "backendLogs") {
        customPath = path.join(app.getPath("home"), ".fairshare", "logs", "api.log");
      }

      axios
        .post(`${this.$server_url}/utilities/openfileexplorer`, {
          file_path: customPath,
        })
        .then((_response) => {
          this.loadingSpinner = false;
          return;
        })
        .catch((error) => {
          this.loadingSpinner = false;
          console.error(error);
          return "ERROR";
        });
    },
    checkForUpdates() {
      // Could probably add more logic here to check if there are updates for the channels with semver
      window.ipcRenderer.send("check-for-updates", this.config.releaseChannel);
    },
  },
  computed: {},
  async mounted() {
    this.datasetStore.hideProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(1);

    let loading = this.$loading({
      lock: true,
      text: "Loading settings...",
      spinner: "el-icon-loading",
    });

    this.config = await this.configStore.getConfig();

    loading.close();

    if ("releaseChannel" in this.config) {
      this.betaRelease = this.config.releaseChannel === "beta";
    }
  },
};
</script>

<style scoped></style>
