<template>
  <div class="flex h-full w-full max-w-screen-lg flex-col items-center justify-center p-3 pr-5">
    <div class="flex h-full w-full flex-col items-center justify-evenly">
      <div class="pointer-events-none">
        <div class="flex w-full items-center justify-center pt-5 pb-1">
          <img class="w-[350px] xl:w-[400px]" src="../../assets/brand/logo-with-name.png" />
        </div>
        <div class="mb-1 flex w-full flex-col items-center justify-center pt-4 pb-3">
          <h2 class="text-xl font-medium text-slate-700">
            Make your biomedical research data and software
          </h2>
          <h2 class="text-xl font-medium text-slate-700">
            Findable, Accessible, Interoperable, and Reusable (FAIR)
          </h2>
        </div>
      </div>

      <div class="grid h-auto w-full grid-cols-3 gap-6">
        <div
          class="flex h-full flex-col items-center justify-between rounded-2xl border border-zinc-100 p-6 shadow-xl"
          v-for="item in heroData"
          :key="item.title"
        >
          <h3 class="textlgd text-center font-medium">
            {{ item.title }}
          </h3>
          <div>
            <Vue3Lottie
              :animationLink="item.lottieURL"
              :width="item.lottieWidth"
              :height="item.lottieWidth"
            />
          </div>
          <p class="px-3 text-center text-sm font-normal">
            {{ item.subtitle }}
          </p>
        </div>
      </div>

      <div class="flex w-full flex-col items-center justify-center py-3">
        <div class="flex justify-center space-x-4 py-3">
          <button
            class="secondary-plain-button text-base"
            @click="openWebsite('https://docs.fairshareapp.io/')"
          >
            <el-icon><notebook-icon /></el-icon>
            Read the documentation
          </button>

          <button class="primary-plain-button text-base" @click="startCuratingProject">
            Getting started
            <el-icon class="icon-animate"> <d-arrow-right /> </el-icon>
          </button>

          <button class="danger-plain-button hidden text-base" @click="datasetStore.hideSidebar">
            Hide sidebar
          </button>

          <button class="danger-button hidden text-base" @click="datasetStore.showSidebar">
            Show sidebar
          </button>
        </div>

        <div
          class="hover-underline-animation flex cursor-pointer flex-row items-center py-1 pt-3 text-primary-600"
        >
          <span
            class="font-medium"
            @click="openWebsite('https://www.go-fair.org/fair-principles/')"
          >
            Learn more about FAIR
          </span>
          <Icon icon="grommet-icons:form-next-link" class="icon-animate ml-2 h-5 w-5" />
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
      heroData: [
        {
          title: "1. Find applicable FAIR guidelines for your data",
          subtitle:
            "Answer questions related to your data to find applicable guidelines for making it FAIR",
          lottieURL: "https://assets3.lottiefiles.com/packages/lf20_zjycbtqy.json",
          lottieWidth: 250,
          lottieHeight: 250,
        },
        {
          title: "2. Follow our step-by-step process for curating your data",
          subtitle:
            "Implement the FAIR data and metadata requirements easily through our intuitive interface",
          lottieURL: "https://assets2.lottiefiles.com/packages/lf20_31cmhkzs.json",
          lottieWidth: 250,
          lottieHeight: 250,
        },
        {
          title: "3. Share resulting dataset on a suitable repository",
          subtitle:
            "Upload your dataset conveniently in a few click to a suitable FAIR data repository",
          lottieURL: "https://assets9.lottiefiles.com/packages/lf20_t4rx36wr.json",
          lottieWidth: 250,
          lottieHeight: 250,
        },
      ],
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
