<template>
  <div class="h-screen w-full flex flex-row lg:justify-center items-center">
    <div class="p-3 h-full w-full lg:w-auto flex flex-row items-center">
      <div class="h-full w-full">
        <div class="flex flex-col h-full overflow-y-auto pr-5">
          <workflow-progress-bar :currentStep="6" />

          <span class="text-lg font-medium text-left">
            Lets publish your work to Zenodo
          </span>
          <span class="text-left">
            All your data has been uploaded to Zenodo. It's now time to publish
            your work.
          </span>

          <el-divider class="my-4"> </el-divider>

          <div class="flex flex-col justify-center items-center h-full px-10">
            <p class="text-center pb-5">
              Once the record is published you will no longer be able to change
              the files in this upload. This is because a Digital Object
              Identifier (DOI) will be registered immediately after publishing.
              You will still be able to update the record's metadata later.
            </p>
            <el-button
              type="primary"
              plain
              class="blob transition-all"
              @click="publishDeposition"
            >
              Publish <el-icon> <Star /> </el-icon>
            </el-button>
          </div>

          <div class="w-full flex-row justify-center py-2 hidden">
            <router-link to="/datasets" class="mx-6">
              <el-button type="danger" plain> Cancel </el-button>
            </router-link>

            <el-button type="primary" class="flex flex-row items-center">
              Continue
              <el-icon>
                <!-- <ArrowRightBold /> -->
              </el-icon>
            </el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import { Icon } from "@iconify/vue";
import { Star } from "@element-plus/icons";
// import axios from "axios";
import { ElMessageBox, ElLoading } from "element-plus";

import { useDatasetsStore } from "../../store/datasets";
import { useTokenStore } from "../../store/access.js";

export default {
  name: "ZenodoPublish",
  components: { Star },
  data() {
    return {
      datasetStore: useDatasetsStore(),
      tokens: useTokenStore(),
      dataset: {},
      folderPath: "",
      workflowID: this.$route.params.workflowID,
      workflow: {},
      zenodoToken: "",
    };
  },
  computed: {},
  methods: {
    async sleep(ms) {
      return new Promise((resolve) => setTimeout(resolve, ms));
    },
    async publishDeposition() {
      // const depositionID = this.workflow.destination.zenodo.deposition_id;

      // const response = await axios
      //   .post(`${this.$server_url}/zenodo/publish`, {
      //     access_token: this.zenodoToken,
      //     deposition_id: depositionID,
      //   })
      //   .then((response) => {
      //     return response.data;
      //   })
      //   .catch((error) => {
      //     console.error(error);
      //     return "ERROR";
      //   });

      const loading = ElLoading.service({
        lock: true,
        text: "Loading",
        background: "rgba(0, 0, 0, 0.7)",
      });

      await this.sleep(3000);

      const response = {
        id: "https://stackoverflow.com/questions/50949594/axios-having-cors-issue",
      };

      if (response === "ERROR") {
        this.statusMessage =
          "There was an error when adding metadata to the deposition";
        return "FAIL";
      } else {
        ElMessageBox.alert(
          "Your dataset was published to Zenodo. Click 'OK' to view this record on Zenodo.",
          "Published to Zenodo",
          {
            confirmButtonText: "OK",
            callback: (action) => {
              console.log(action);
              if (action === "confirm") {
                console.log(`Opening ${response.id}`);
                window.ipcRenderer.send(
                  "open-link-in-browser",
                  `https://sandbox.zenodo.org/record/${response.id}`
                );
              }
            },
          }
        );
      }

      loading.close();
    },
  },
  async mounted() {
    this.dataset = await this.datasetStore.getCurrentDataset();
    this.workflow = this.dataset.workflows[this.workflowID];

    this.zenodoToken = await this.tokens.getToken("zenodo");
    // console.log(this.zenodoToken);
  },
};
</script>

<style lang="postcss" scoped>
.blob {
  box-shadow: 0 0 0 0 rgba(52, 172, 224, 1);
  animation: pulse-blue 2s infinite;
}

@keyframes pulse-blue {
  0% {
    transform: scale(0.95);
    box-shadow: 0 0 0 0 rgba(52, 172, 224, 0.7);
  }

  70% {
    transform: scale(1);
    box-shadow: 0 0 0 10px rgba(52, 172, 224, 0);
  }

  100% {
    transform: scale(0.95);
    box-shadow: 0 0 0 0 rgba(52, 172, 224, 0);
  }
}
</style>
