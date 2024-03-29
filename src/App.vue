<template>
  <div class="flex flex-row bg-white">
    <AppSidebar :environment="environment"></AppSidebar>

    <AppContent>
      <router-view v-slot="{ Component }" class="pt-2">
        <transition name="fade" appear mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </AppContent>

    <error-confirm
      ref="errorConfirmNoBackend"
      title="Could not connect to backend server"
      :showCancelButton="false"
      :preventOutsideClick="true"
      confirmButtonText="Restart FAIRshare"
      @messageConfirmed="restartApplication"
    >
      <p class="text-center text-base text-gray-500">
        FAIRshare could not connect to the backend server. Please try restarting the application. If
        the problem persists, please contact us
        <span class="text-url" @click="goToContactPage">here</span>.
      </p>
    </error-confirm>

    <error-confirm
      ref="errorConfirmInvalidAPIVersion"
      title="Invalid API version"
      :showCancelButton="false"
      :preventOutsideClick="true"
      confirmButtonText="Restart FAIRshare"
      @messageConfirmed="restartApplication"
    >
      <p class="text-center text-base text-gray-500">
        Invalid app versions were found. Please try restarting the application. If the problem
        persists, restart your computer and then reinstall FAIRshare.
      </p>
    </error-confirm>

    <app-announcement
      ref="appAnnouncement"
      title=""
      :showCancelButton="false"
      confirmButtonText="Okay"
    >
      <p class="text-center text-base text-gray-500">
        {{ announcementText }}
      </p>
    </app-announcement>

    <fade-transition>
      <div
        class="fixed bottom-4 right-4 flex w-[255px] flex-col items-center justify-center rounded-lg border border-zinc-300 bg-white px-4 py-2 shadow-xl"
        v-if="showConnectingMessage"
      >
        <Vue3Lottie
          animationLink="https://assets7.lottiefiles.com/packages/lf20_rwvsnibi.json"
          :width="210"
          :height="180"
        />
        <div
          class="absolute top-2 right-2 hidden cursor-pointer text-zinc-400 transition-all hover:text-zinc-700"
          @click="closeNotification"
        >
          <el-icon><circle-close-filled /></el-icon>
        </div>
        <p class="text-center text-sm">
          FAIRshare is connecting to the backend server <LoadingEllipsis />
        </p>
      </div>
    </fade-transition>

    <fade-transition>
      <div
        class="fixed bottom-4 right-4 flex w-[230px] flex-col items-center justify-center rounded-lg border border-zinc-300 bg-white px-4 py-2 shadow-xl"
        v-if="showDownloadingMessage"
      >
        <div
          class="absolute top-2 right-2 cursor-pointer text-zinc-400 transition-all hover:text-zinc-700"
          @click="closeNotification"
        >
          <el-icon><circle-close-filled /></el-icon>
        </div>
        <Vue3Lottie
          animationLink="https://assets5.lottiefiles.com/private_files/lf30_t26law.json"
          :width="100"
          :height="100"
        />
        <p class="text-center text-sm">FAIRshare is downloading the latest version of the app...</p>
      </div>
    </fade-transition>

    <fade-transition>
      <div
        class="fixed bottom-4 right-4 flex w-[250px] flex-col items-center justify-center rounded-lg border border-zinc-300 bg-white px-6 py-3 shadow-xl"
        v-if="showRestartMessage"
      >
        <div
          class="absolute top-2 right-2 cursor-pointer text-zinc-400 transition-all hover:text-zinc-700"
          @click="closeNotification"
        >
          <el-icon><circle-close-filled /></el-icon>
        </div>
        <Vue3Lottie
          animationLink="https://assets8.lottiefiles.com/packages/lf20_dv9qkzg7.json"
          :width="50"
          :height="50"
        />
        <p class="py-3 text-center text-sm">
          {{
            platform == "darwin"
              ? "Update downloaded. It will be installed when you close and relaunch the app."
              : "Restart FAIRshare to install the latest version of the app."
          }}
        </p>
        <button class="primary-plain-button py-1 px-2" @click="restartAppForUpdate">
          {{ platform == "darwin" ? "Close FAIRshare" : "Restart FAIRshare" }}
        </button>
      </div>
    </fade-transition>
  </div>
</template>

<script>
import AppSidebar from "./components/ui/AppSidebar.vue";
import AppContent from "./components/ui/AppContent.vue";

import LoadingEllipsis from "@/components/spinners/LoadingEllipsis.vue";

import { app } from "@electron/remote";
import semver from "semver";
import axios from "axios";
import Mousetrap from "mousetrap";

import { useDatasetsStore } from "./store/datasets";
import { useTokenStore } from "./store/access.js";
import { useConfigStore } from "./store/config.js";

const MIN_API_VERSION = "2.0.0";

export default {
  name: "App",
  components: {
    AppSidebar,
    AppContent,
    LoadingEllipsis,
  },
  data() {
    return {
      appPath: app.getAppPath(),
      allDatasets: useDatasetsStore(),
      config: useConfigStore(),
      tokens: useTokenStore(),
      loading: "",
      environment: "",
      showConnectingMessage: true,
      showDownloadingMessage: false,
      showRestartMessage: false,
      platform: process.platform,
      announcementText: "",
    };
  },
  methods: {
    async loadStores() {
      try {
        // Load all the projects
        await this.allDatasets.loadDatasets();

        // Load all the access tokens
        await this.tokens.loadTokens(this.$server_url);

        // Load app config
        await this.config.loadConfig();

        // Run all the integrations checks
        this.tokens.verifyAllConnections();

        this.showConnectingMessage = false;

        this.checkForAnnouncements();
        window.ipcRenderer.send("check-for-updates");
      } catch (error) {
        console.error("Error with loading stores...");
        console.error(error);

        this.showConnectingMessage = false;

        this.checkForAnnouncements();
        window.ipcRenderer.send("check-for-updates");
      }
    },
    restartAppForUpdate() {
      window.ipcRenderer.send("restart-fairshare-for-update");
    },
    closeNotification() {
      this.showConnectingMessage = false;
      this.showDownloadingMessage = false;
      this.showRestartMessage = false;
    },
    restartApplication() {
      window.ipcRenderer.send("restart-fairshare");
    },
    goToContactPage() {
      this.$refs.errorConfirmNoBackend.close();
      this.$router.push({
        path: "/contactUs",
      });
    },
    checkForAnnouncements() {
      const url = `https://raw.githubusercontent.com/fairdataihub/FAIRshare/geo/meta/announcements.json?timestamp=${new Date().getTime()}`;

      axios
        .get(url)
        .then((response) => {
          const announcements = response.data;
          const currentVersion = app.getVersion();
          const platform = process.platform;

          if (currentVersion in announcements) {
            const currentVersionObject = announcements[currentVersion];
            let announcement = {};

            if ("all" in currentVersionObject) {
              announcement = currentVersionObject["all"];
            } else if (platform in currentVersionObject) {
              announcement = currentVersionObject[platform];
            }

            if ("show" in announcement && announcement.show) {
              if ("type" in announcement && announcement.type === "warning") {
                this.announcementText = announcement.message;

                this.$refs.appAnnouncement.setTitle(announcement.title);
                this.$refs.appAnnouncement.show();
              }
            }
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },
    async checkForBackend() {
      /**
       * TODO: Make this into a composable
       *
       * @param {*} ms - milliseconds to wait
       */
      const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

      let retriesSuccess = false;
      const timeout = 1000;

      // retry request 30 times with a 1 second delay
      for (let i = 0; i < 30 && !retriesSuccess; i++) {
        console.log(`Retry ${i}...`);
        axios.get(`${this.$server_url}/api_version`).then((echo_response) => {
          console.log(`Server Status: ${echo_response.data}`);
          axios
            .get(`${this.$server_url}/api_version`)
            .then((api_version_response) => {
              this.config.setGlobals("minAPIVersion", MIN_API_VERSION);
              this.config.setGlobals("backendAPIVersion", api_version_response.data);

              if (
                semver.lte(semver.clean(MIN_API_VERSION), semver.clean(api_version_response.data))
              ) {
                console.log("API version satisfied");

                this.loadStores();

                retriesSuccess = true;

                axios
                  .get(`${this.$server_url}/zenodo/env`)
                  .then((response) => {
                    if (response.data.search("sandbox") === -1) {
                      this.environment = "production";
                    } else {
                      this.environment = "sandbox";
                    }
                  })
                  .catch((error) => {
                    console.error(error);
                  });
              } else {
                this.$refs.errorConfirmInvalidAPIVersion.show();

                retriesSuccess = false;

                this.showConnectingMessage = false;
              }
            })
            .catch((error) => {
              console.error(error);
              retriesSuccess = false;
            });
        });
        await sleep(timeout);
      }

      if (retriesSuccess) {
        this.showConnectingMessage = false;
      } else {
        this.$refs.errorConfirmNoBackend.show();
      }
    },
  },
  async mounted() {
    this.$track("App Launched", "OS", process.platform);
    this.$track("App Launched", "Version", app.getVersion());
    this.$track("App Launched", "Arch", process.arch);

    // disable the mouse back and forward buttons
    window.addEventListener("mouseup", (e) => {
      if (e.button === 3 || e.button === 4) {
        e.preventDefault();
      }
    });

    function disableReload() {
      if (process.env.NODE_ENV !== "development") {
        return false;
      }
    }

    // disable the refresh button on macOS
    Mousetrap.bind("command+r", disableReload);

    // disable the refresh button on Windows
    Mousetrap.bind("ctrl+r", disableReload);

    this.checkForBackend();

    window.ipcRenderer.on("update-available", (_e, _arg) => {
      this.showDownloadingMessage = true;
      this.$track("App Update", "Update available", `${app.getVersion()}`);
      window.ipcRenderer.removeAllListeners("update-available");
    });

    window.ipcRenderer.on("update-downloaded", (_e, _arg) => {
      this.showDownloadingMessage = false;
      this.showRestartMessage = true;
      this.$track("App Update", "Update downloaded", `${app.getVersion()}`);
      window.ipcRenderer.removeAllListeners("update-downloaded");
    });

    console.log(`Current app path: ${this.appPath}`);

    this.$router.push({
      path: "/home",
    });
  },
};
</script>
