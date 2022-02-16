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
  </div>
</template>

<script>
import AppSidebar from "./components/ui/AppSidebar.vue";
import AppContent from "./components/ui/AppContent.vue";

import { app } from "@electron/remote";
import semver from "semver";
import axios from "axios";
import axiosRetry from "axios-retry";
import { ElLoading } from "element-plus";
import Mousetrap from "mousetrap";

import { useDatasetsStore } from "./store/datasets";
import { useTokenStore } from "./store/access.js";

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
      unpublishedDatasets: useDatasetsStore(),
      tokens: useTokenStore(),
      loading: "",
      environment: "",
    };
  },
  methods: {
    async loadStores() {
      try {
        // show Sidebar

        // await this.unpublishedDatasets.showSidebar();
        // await this.unpublishedDatasets.hideSidebar();

        // Load all the projects
        await this.unpublishedDatasets.loadDatasets();

        // Load all the access tokens
        await this.tokens.loadTokens();

        // Run all the integrations checks
        this.tokens.verifyAllConnections();

        this.loading.close();
      } catch (error) {
        console.error("Error with loading stores...");
        console.error(error);
        this.loading.close();
      }
    },
  },
  mounted() {
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
    axiosRetry(client, { retries: 3 });

    this.loading = ElLoading.service({
      lock: true,
      text: "Connecting to backend systems and loading data...",
      background: "rgba(255, 255, 255, 0.95)",
    });

    client
      .get("/echo", {
        "axios-retry": {
          retries: 5,
          retryDelay: axiosRetry.exponentialDelay,
        },
      })
      .then((response) => {
        console.log(response.data);
        axios
          .get(`${this.$server_url}/api_version`)
          .then((response) => {
            if (
              semver.lte(
                semver.clean(MIN_API_VERSION),
                semver.clean(response.data)
              )
            ) {
              console.log("API version satisfied");

              this.loadStores();
            } else {
              // will need to change this to a more user friendly message
              alert("Invalid API version");
              this.loading.close();
            }
          })
          .catch((error) => {
            console.error(error);
          });
      })
      .catch((error) => {
        console.error(error);
      });

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

    window.ipcRenderer.on("update-available", (_e, _arg) => {
      console.log("New update available");
    });

    window.ipcRenderer.on("update-downloaded", (_e, _arg) => {
      console.log("Update downloaded");
    });

    console.log(this.appPath);

    this.$router.push({
      path: "/",
    });
  },
};
</script>
