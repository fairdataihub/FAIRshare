<template>
  <div
    class="h-screen w-full flex flex-row items-center"
    :class="{ 'justify-center': datasetStore.datasets.length === 0 }"
  >
    <div
      ref="startCuration"
      class="p-3 h-full flex flex-row items-center"
      :class="{ 'w-full': datasetStore.datasets.length > 0 }"
    >
      <div
        ref="continueCurating"
        class="h-full w-full"
        v-if="datasetStore.datasets.length > 0"
      >
        <div class="flex flex-col h-full">
          <span class="font-inter text-base font-medium">
            Continue curating your datasets
          </span>
          <span class="font-inter text-base">
            You have some unpublished datasets. Do you want to continue working
            on these items?
          </span>
          <el-divider content-position="left" class="font-inter">
            Click on one of the datasets below</el-divider
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
            >
              <div class="flex flex-row items-center">
                <img :src="dataset.image" alt="" class="w-14" />
                <div class="flex flex-col px-4">
                  <span class="font-inter text-sm font-medium">
                    {{ dataset.name }}
                  </span>
                  <p class="font-inter text-sm line-clamp-3">
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
              <span class="font-inter text-base font-medium">
                Or start from an empty project
              </span>
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
            <span class="font-inter font-medium text-large">
              Create a new dataset
            </span>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { Icon } from "@iconify/vue";

import { useDatasetsStore } from "../store/datasets";

export default {
  name: "DatasetsShowAll",
  components: { Icon },

  data() {
    return {
      datasetStore: useDatasetsStore(),
    };
  },
  methods: {},
  mounted() {
    
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
