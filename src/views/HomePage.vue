<template>
  <div
    class="flex h-full w-full max-w-screen-lg flex-col items-center justify-center p-3 pr-5"
  >
    <div class="flex h-full w-full flex-col items-center justify-evenly">
      <div class="pointer-events-none">
        <div class="flex w-full items-center justify-center py-5">
          <h1 class="text-3xl font-bold text-slate-800 xl:text-4xl">
            SODA for COVID-19 Research
          </h1>
        </div>
        <div class="mb-1 flex w-full flex-col items-center justify-center py-3">
          <h2 class="text-2xl font-medium text-slate-700 xl:text-3xl">
            Make your COVID-19 research data, and beyond,
          </h2>
          <h2 class="text-2xl font-medium text-slate-700 xl:text-3xl">
            Findable, Accessible, Interoperable, and Reusable (FAIR)
          </h2>
        </div>
      </div>

      <div class="flex w-full justify-evenly space-x-14 py-3">
        <div class="item-center flex flex-col justify-center">
          <div class="item-center flex w-full justify-center py-3">
            <img src="../assets/images/overview.svg" class="h-auto w-11/12" />
          </div>
        </div>
      </div>

      <div class="flex w-full flex-col items-center justify-center py-3">
        <div class="flex justify-center space-x-4 py-3">
          <button
            class="secondary-plain-button text-base"
            @click="
              openWebsite('https://soda-for-covid-19-research-docs.vercel.app/')
            "
          >
            <el-icon><notebook-icon /></el-icon>
            Read the documentation
          </button>

          <button
            class="primary-plain-button text-base"
            @click="startCuratingProject"
          >
            Getting started
            <el-icon class="icon-animate"> <d-arrow-right /> </el-icon>
          </button>

          <button
            class="danger-plain-button hidden text-base"
            @click="datasetStore.hideSidebar"
          >
            Hide sidebar
          </button>

          <button
            class="danger-button hidden text-base"
            @click="datasetStore.showSidebar"
          >
            Show sidebar
          </button>
        </div>

        <div
          class="hover-underline-animation text-primary-600 flex cursor-pointer flex-row items-center py-1 pt-3"
        >
          <span
            class="font-medium"
            @click="openWebsite('https://www.go-fair.org/fair-principles/')"
          >
            Learn more about FAIR
          </span>
          <Icon
            icon="grommet-icons:form-next-link"
            class="icon-animate ml-2 h-5 w-5"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Icon } from "@iconify/vue";

import { useDatasetsStore } from "@/store/datasets";

export default {
  name: "HomePage",
  components: {
    Icon,
  },
  data() {
    return {
      datasetStore: useDatasetsStore(),
    };
  },
  methods: {
    openWebsite(url) {
      window.ipcRenderer.send("open-link-in-browser", url);
    },
    startCuratingProject() {
      this.navigateToDataset();
    },
    async navigateToDataset() {
      let routerPath;
      routerPath = `/datasets`;
      this.$router.push({ path: routerPath });
    },
  },
  mounted() {
    this.datasetStore.hideProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(1);
  },
};
</script>
