<template>
  <div
    class="h-screen w-full flex flex-row items-center"
    :class="{ 'justify-center': datasetStore.datasetCount === 0 }"
  >
    <div
      ref="startCuration"
      class="px-3 h-full flex flex-row items-center"
      :class="{ 'w-full': datasetStore.datasetCount > 0 }"
    >
      <div
        ref="continueCurating"
        class="h-full w-full"
        v-if="datasetStore.datasetCount > 0"
      >
        <div class="flex flex-col h-full">
          <span class="font-medium"> Continue curating your datasets </span>

          <span>
            You have some unpublished projects. Do you want to continue working
            on these items?
          </span>

          <el-divider content-position="left">
            Click on one of the projects below</el-divider
          >

          <div
            ref="unpublishedDatasets"
            id="unpublishedDatasets"
            class="
              divide-y divide-gray-200
              px-4
              flex-grow
              h-full
              overflow-y-auto
            "
          >
            <div
              v-for="dataset in datasetStore.datasets"
              :key="dataset"
              class="
                flex flex-row
                justify-between
                items-center
                w-full
                p-3
                hover:bg-gray-100
                transition-all
                cursor-pointer
              "
              @click="navigateToDataset(`${dataset.id}`)"
            >
              <div class="flex flex-row items-center">
                <img :src="dataset.image" alt="" class="w-14" />
                <div class="flex flex-col px-4">
                  <span class="text-sm font-medium">
                    {{ dataset.name }}
                  </span>
                  <p class="text-sm line-clamp-3">
                    {{ dataset.description }}
                  </p>
                </div>
              </div>
              <div class="flex items-center ml-2">
                <Icon icon="ic:round-navigate-next" class="h-8 w-8" />
              </div>
            </div>
          </div>
          <el-divider> </el-divider>
          <router-link to="/datasets/new">
            <div
              ref="startFromEmpty"
              class="
                flex flex-row
                items-center
                w-max
                text-purple-800
                cursor-pointer
                mb-5
                pb-1
                hover-underline-animation
              "
            >
              <span class="font-medium"> Or start from an empty project </span>
              <Icon icon="grommet-icons:form-next-link" class="ml-2 h-5 w-5" />
            </div>
          </router-link>
        </div>
      </div>
      <div
        ref="startCurating"
        class="flex flex-row justify-center items-center p-10"
        v-else
      >
        <router-link to="/datasets/new">
          <div
            class="
              flex flex-col
              justify-center
              items-center
              border-2 border-dashed
              hover:border-solid
              w-max
              p-10
              rounded-lg
              hover:bg-gray-100
              transition-all
              cursor-pointer
            "
          >
            <Icon
              icon="fluent:quiz-new-24-regular"
              class="h-20 w-10/12 text-gray-700"
            />
            <span class="font-medium text-large"> Create a new dataset </span>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { Icon } from "@iconify/vue";

import { useDatasetsStore } from "../../store/datasets";

export default {
  name: "ShowAllProjects",
  components: { Icon },

  data() {
    return {
      datasetStore: useDatasetsStore(),
    };
  },
  methods: {
    navigateToDataset(datasetID) {
      this.datasetStore.getDataset(datasetID);
      const routerPath = `/datasets/${datasetID}`;
      // const routerPath = `/datasets/0387b979-4b45-46bb-bb27-84aaf32c4cdb/workflow1/zenodo/metadata`;
      // const routerPath = `/datasets/0387b979-4b45-46bb-bb27-84aaf32c4cdb/workflow1/zenodo/review`;
      // const routerPath = `/datasets/0387b979-4b45-46bb-bb27-84aaf32c4cdb/workflow1/createMetadata`;
      // const routerPath = `/datasets/0387b979-4b45-46bb-bb27-84aaf32c4cdb/workflow1/zenodo/accessToken`;
      this.$router.push({ path: routerPath });
    },
  },
  mounted() {},
};
</script>
