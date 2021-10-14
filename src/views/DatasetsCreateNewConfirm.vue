<template>
  <div class="h-screen w-full flex flex-row items-center">
    <div ref="" class="p-3 h-full flex flex-row items-center">
      <div ref="" class="h-full w-full">
        <div class="flex flex-col h-full overflow-y-auto">
          <span class="font-inter text-base font-medium">
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
            <el-button type="danger" plain> Cancel </el-button>
            <el-button type="primary"> Continue </el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import { Icon } from "@iconify/vue";

import { useDatasetsStore } from "../store/datasets";

export default {
  name: "DatasetsCreateNewConfirm",
  // components: { Icon },
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

<style>
#unpublishedDatasets::-webkit-scrollbar-track {
  -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
  background-color: #f5f5f5;
}

#unpublishedDatasets::-webkit-scrollbar {
  width: 6px;
  background-color: #f5f5f5;
}

#unpublishedDatasets::-webkit-scrollbar-thumb {
  background-color: #424242;
}

::-webkit-scrollbar-track {
  -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
  background-color: #f5f5f5;
}

::-webkit-scrollbar {
  width: 6px;
  background-color: #f5f5f5;
}

::-webkit-scrollbar-thumb {
  background-color: #424242;
}
</style>
