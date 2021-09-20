<template>
  <div class="container mt-2">Current App Path: {{ appPath }}</div>
  <div>
    <TheCalculator></TheCalculator>
  </div>
</template>

<script>
import { app } from "@electron/remote";
import semver from "semver";
import axios from "axios";

const MIN_API_VERSION = "1.0.0";

import TheCalculator from "./components/TheCalculator.vue";

export default {
  name: "App",
  components: { TheCalculator },
  data() {
    return {
      appPath: app.getAppPath(),
    };
  },
  mounted() {
    axios
      .get(`${this.SERVERURL}/api_version`)
      .then((response) => {
        if (
          semver.lte(semver.clean(MIN_API_VERSION), semver.clean(response.data))
        ) {
          console.log("Api Version satisfied");
        } else {
          alert("Invalid API Version");
        }
      })
      .catch((error) => {
        console.error(error);
      });
  },
};
</script>
