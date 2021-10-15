<template>
  <div class="h-screen w-full flex flex-row lg:justify-center items-center">
    <div class="p-3 h-full flex flex-row items-center">
      <div class="h-full w-full">
        <div class="flex flex-col h-full overflow-y-auto">
          <span class="font-inter text-base font-medium text-left">
            SODA suggestions
          </span>

          <span class="font-inter text-base">
            Based on your selected data types, this is what we suggest you
            should use for FAIR sharing of your data.
          </span>

          <el-divider> </el-divider>

          <span class="font-inter text-base">
            We recommend the following repositories for your selected data
            types.
          </span>

          <div class="grid grid-cols-3 gap-4">
            <div class="flex flex-col divide-y-2 p-4">
              <span class="font-bold p-2"> Code </span>
              <div class="flex flex-col">
                <span class="p-1"> Zenodo </span>
                <span class="p-1"> FigShare </span>
              </div>
            </div>
            <div class="flex flex-col divide-y-2 p-4">
              <span class="font-bold p-2"> Genomic Data </span>
              <div class="flex flex-col">
                <span class="p-1"> Zenodo </span>
                <span class="p-1"> FigShare </span>
              </div>
            </div>
          </div>

          <span class="font-inter text-base">
            SODA will automatically split up your data and upload it to the
            relevant repository. Do you want to continue?
          </span>

          <div class="w-full flex flex-row justify-center py-2">
            <router-link to="/datasets" class="mx-6">
              <el-button type="danger" plain> Cancel </el-button>
            </router-link>
            <router-link :to="`/datasets/${datasetID}`" class="mx-6">
              <el-button type="primary" class="flex flex-row items-center">
                Continue
                <el-icon>
                  <ArrowRightBold />
                </el-icon>
              </el-button>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import { Icon } from "@iconify/vue";
import { ArrowRightBold } from "@element-plus/icons";

import { useDatasetsStore } from "../store/datasets";

export default {
  name: "DatasetsCreateNewConfirm",
  components: { ArrowRightBold },
  data() {
    return {
      datasetStore: useDatasetsStore(),
      dataset: {},
      datasetID: this.$route.params.datasetID,
    };
  },
  methods: {},
  mounted() {
    this.dataset = this.datasetStore.getDataset(this.datasetID);
    console.log(this.dataset);
  },
};
</script>
