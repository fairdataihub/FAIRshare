<template>
  <div class="h-screen w-full flex flex-row lg:justify-center items-center">
    <div class="p-3 h-full flex flex-row items-center">
      <div class="h-full w-full">
        <div class="flex flex-col h-full overflow-y-auto">
          <span class="font-inter text-lg font-medium text-left">
            Where is your data located?
          </span>

          <el-divider> </el-divider>

          <span class="font-inter text-base mb-4">
            Please select the folder where your {{ dataType }} files are stored.
          </span>

          <el-input
            v-model="folderPath"
            :placeholder="folderPathPlaceholder"
            class="my-4"
            @click="selectFolderPath"
          />

          <div class="w-full flex flex-row justify-center py-2">
            <router-link to="/datasets" class="mx-6">
              <el-button type="danger" plain> Cancel </el-button>
            </router-link>

            <el-button
              type="primary"
              :disabled="emptyInput"
              class="flex flex-row items-center"
              @click="startCuration"
            >
              Continue
              <el-icon>
                <ArrowRightBold />
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
import { ArrowRightBold } from "@element-plus/icons";
import { dialog } from "@electron/remote";

import { useDatasetsStore } from "../store/datasets";

export default {
  name: "DatasetsCurateSelectFolder",
  components: { ArrowRightBold },
  props: ["datasetID", "dataType"],
  data() {
    return {
      datasetStore: useDatasetsStore(),
      dataset: {},
      folderPathPlaceholder: "Click here to select a folder",
      folderPath: "",
    };
  },
  computed: {
    emptyInput() {
      if (this.folderPath.trim() === "") {
        return true;
      } else {
        return false;
      }
    },
  },
  methods: {
    selectFolderPath() {
      dialog.showOpenDialog({ properties: ["openDirectory"] }).then((data) => {
        if (!data.canceled) {
          this.folderPath = data.filePaths[0];
        }
      });
    },
    startCuration() {
      if (this.datasetStore.currentOptions.dataType === "single") {
        return;
      }
    },
  },
  mounted() {
    this.dataset = this.datasetStore.currentDataset;
  },
};
</script>
