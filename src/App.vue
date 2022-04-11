<template>
  <!-- <div class="container mt-2">Current App Path: {{ appPath }}</div> -->
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
          class="absolute top-2 right-2 cursor-pointer text-zinc-400 transition-all hover:text-zinc-700"
          @click="closeNotification"
        >
          <el-icon><circle-close-filled /></el-icon>
        </div>
        <p class="text-center text-sm">FAIRshare is connecting to the backend server...</p>
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

import { app } from "@electron/remote";
import semver from "semver";
import axios from "axios";
import axiosRetry from "axios-retry";
import Mousetrap from "mousetrap";

import { useDatasetsStore } from "./store/datasets";
import { useTokenStore } from "./store/access.js";
import { useConfigStore } from "./store/config.js";

const MIN_API_VERSION = "0.0.1";

export default {
  name: "App",
  components: {
    AppSidebar,
    AppContent,
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
        await this.tokens.loadTokens();

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
      axios
        .get(
          "https://raw.githubusercontent.com/fairdataihub/FAIRshare/server-check/meta/announcements.json"
        )
        .then((response) => {
          const announcements = response.data;
          const currentVersion = app.getVersion();

          if (currentVersion in announcements) {
            const announcement = announcements[currentVersion];

            if (announcement.type === "warning") {
              this.announcementText = announcement.message;
              this.$refs.appAnnouncement.show();
            }
          }
        });
      // const url =
      //   "https://raw.githubusercontent.com/fairdataihub/FAIRshare/main/meta/warnings.json";
      // fetch(url).then(function (response) {
      //   response.text().then(function (text) {
      //     console.log(text);
      //     let warning_obj = JSON.parse(text);

      //     console.log(warning_obj, app.getVersion(), "test");
      //   });
      // });
    },
  },
  mounted() {
    this.$track("App Launched", "OS", process.platform);
    this.$track("App Launched", "Version", app.getVersion());
    this.$track("App Launched", "Arch", process.arch);

    // disable the mouse back and forward buttons
    window.addEventListener("mouseup", (e) => {
      if (e.button === 3 || e.button === 4) {
        e.preventDefault();
      }
    });

    // disable the refresh button on macOS
    Mousetrap.bind("command+r", function () {
      if (process.env.NODE_ENV !== "development") {
        return false;
      }
    });

    // disable the refresh button on Windows
    Mousetrap.bind("ctrl+r", function () {
      if (process.env.NODE_ENV !== "development") {
        return false;
      }
    });

    const client = axios.create({ baseURL: `${this.$server_url}` });
    axiosRetry(client, { retries: 10 });

    client
      .get("/echo", {
        "axios-retry": {
          retries: 10,
          retryDelay: axiosRetry.exponentialDelay,
        },
      })
      .then((response) => {
        console.log(`Server Status: ${response.data}`);
        axios
          .get(`${this.$server_url}/api_version`)
          .then((response) => {
            if (semver.lte(semver.clean(MIN_API_VERSION), semver.clean(response.data))) {
              console.log("API version satisfied");

              this.loadStores();

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

              this.showConnectingMessage = false;
            }
          })
          .catch((error) => {
            console.error(error);
          });
      })
      .catch((error) => {
        this.$refs.errorConfirmNoBackend.show();
        console.error(error);
      });

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
