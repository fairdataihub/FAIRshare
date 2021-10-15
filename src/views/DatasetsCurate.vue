<template>
  <div class="h-screen w-full flex flex-row justify-center items-center">
    <div ref="" class="p-3 h-full flex flex-row items-center">
      <div ref="" class="h-full w-full">
        <div class="flex flex-col h-full overflow-y-auto">
          <span class="font-medium text-left">
            Start the curation process
          </span>

          <span class="">
            When you are ready, click on the curation buttons below to fill out
            some metadata information.
          </span>

          <el-divider> </el-divider>

          <div
            class="flex flex-col p-2"
            v-for="type in dataset.dataType"
            :key="type"
          >
            <div class="bg-gray-300 px-4 py-2">
              <span class="text-lg"> {{ type }} </span>
            </div>
            <div class="bg-gray-200 px-4 py-2">
              <router-link to="/" class="">
                <el-button type="primary">
                  Curate {{ type }}
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
  </div>
</template>

<script>
// import { Icon } from "@iconify/vue";
import { ArrowRightBold } from "@element-plus/icons";

import { useDatasetsStore } from "../store/datasets";

export default {
  name: "DatasetsCurate",
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
