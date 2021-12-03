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
        await this.unpublishedDatasets.loadDatasets();
        await this.tokens.loadTokens();

        // sample implementation of access tokens
        // await this.tokens.saveToken(
        //   "zenodo",
        //   process.env.VUE_APP_ZENODO_ACCESS_TOKEN
        // );
        console.log(await this.tokens.getToken("zenodo"));

        this.loading.close();
      } catch (error) {
        console.error("Error with loading stores...");
        console.error(error);
        this.loading.close();
      }
    },
  },
  mounted() {
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
  },
};
</script>

<style lang="postcss">
.fade-enter-active,
.fade-leave-active {
  transition: all 0.2s ease-in-out;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  /* transform: translateY(-20px); */
}
</style>
