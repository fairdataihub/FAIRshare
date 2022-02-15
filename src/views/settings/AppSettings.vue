<template>
  <div
    class="flex h-full w-full max-w-screen-lg flex-col items-center justify-center p-3 pr-5"
  >
    <div class="flex h-full w-full flex-col">
      <h1 class="pt-5 pb-1 text-3xl font-bold text-slate-700">
        Application Settings
      </h1>

      <line-divider></line-divider>

      <el-tabs v-model="activeName" class="w-11/12 py-5" tab-position="right">
        <el-tab-pane label="General" name="general" c>
          <div class="flex flex-col space-y-4 px-3">
            <!-- settings panel -->
            <div class="rounded-lg border-2 border-slate-100 p-4">
              <h2 class="py-2 text-lg font-semibold text-slate-600">
                Allow beta versions?
              </h2>
              <div class="flex flex-col items-start">
                <p class="mb-2 text-sm">
                  Do you want to allow FAIRShare to download beta versions of
                  the application? Beta versions are not yet stable and may
                  contain bugs but you will be able to preview the latest
                  features ahead of time.
                </p>
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
                  <el-tooltip
                    :content="betaRelease ? 'Enabled' : 'Disabled'"
                    placement="bottom"
                  >
                    <el-switch
                      v-model="betaRelease"
                      class="mx-1"
                      active-color="#2563eb"
                      inactive-color="#fdba74"
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
              </div>
            </div>
          </div>
        </el-tab-pane>
        <el-tab-pane label="Advanced" name="proxy">
          <div class="flex flex-col space-y-4 px-3">
            <div class="rounded-lg border-2 border-slate-100 p-4">
              <h2 class="py-2 text-lg font-semibold text-slate-600">
                Configuration Folder
              </h2>
              <div class="flex flex-col items-start">
                <p class="mb-2">
                  The FAIRShare config folder holds key information regarding
                  your projects, access tokens and datasets.
                </p>
                <button
                  @click="openFileExplorer('configFolder')"
                  class="secondary-plain-button"
                >
                  Open the config folder
                </button>
              </div>
            </div>

            <div class="rounded-lg border-2 border-slate-100 p-4">
              <h2 class="py-2 text-lg font-semibold text-slate-600">
                Logs Folder
              </h2>
              <div class="flex flex-col items-start">
                <p class="mb-2">
                  Our backend service will create logs for errors that are shown
                  in the UI. Click the button to open the logs folder.
                </p>
                <button
                  @click="openFileExplorer('backendLogs')"
                  class="secondary-plain-button"
                >
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
        />
      </div>
    </transition>
  </div>
</template>

<script>
import { app } from "@electron/remote";
import axios from "axios";
import path from "path";

import { useDatasetsStore } from "@/store/datasets";

export default {
  name: "AppSettings",
  components: {},
  data() {
    return {
      datasetStore: useDatasetsStore(),
      activeName: "general",
      loadingSpinner: false,
      betaRelease: false,
    };
  },
  methods: {
    openFileExplorer(type) {
      this.loadingSpinner = true;

      let customPath = "";

      if (type === "configFolder") {
        customPath = path.join(
          app.getPath("home"),
          ".sodaforcovid19research",
          "accessTokens.json"
        );
      } else if (type === "backendLogs") {
        customPath = path.join(
          app.getPath("home"),
          ".sodaforcovid19research",
          "logs",
          "api.log"
        );
      }

      axios
        .post(`${this.$server_url}/utilities/openFileExplorer`, {
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
  },
  computed: {},
  async mounted() {
    this.datasetStore.hideProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(1);
  },
};
</script>

<style scoped></style>
