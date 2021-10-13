<template>
  <!-- <div class="container mt-2">Current App Path: {{ appPath }}</div> -->
  <div class="flex flex-row">
    <AppSidebar></AppSidebar>
    <router-view> </router-view>
  </div>
</template>

<script>
// import { app } from "@electron/remote";
import semver from "semver";
import axios from "axios";
import AppSidebar from "./components/ui/AppSidebar.vue";

const MIN_API_VERSION = "0.0.1";

export default {
  name: "App",
  components: {
    AppSidebar,
  },
  data() {
    return {
      // appPath: app.getAppPath(),
    };
  },
  mounted() {
    axios
      .get(`${this.SERVERURL}/echo`)
      .then((response) => {
        console.log(response.data);
        axios
          .get(`${this.SERVERURL}/api_version`)
          .then((response) => {
            if (
              semver.lte(
                semver.clean(MIN_API_VERSION),
                semver.clean(response.data)
              )
            ) {
              console.log("API version satisfied");
            } else {
              alert("Invalid API version");
            }
          })
          .catch((error) => {
            console.error(error);
          });
      })
      .catch((error) => {
        console.error(error);
      });

    console.log(this.appPath);
  },
};
</script>
