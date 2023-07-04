<template>
  <div class="flex h-full w-full max-w-screen-lg flex-col items-center justify-center p-3 pr-5">
    <div class="flex h-full w-full flex-col">
      <h1 class="pb-1 pt-5 text-3xl font-bold text-slate-700">Documentation</h1>

      <line-divider></line-divider>

      <h2>
        We have created a documentation page for each component or feature in FAIRshare. You can
        find the documentation site by clicking on the button below:
      </h2>

      <div class="flex h-full w-full flex-col items-center justify-start">
        <div>
          <Vue3Lottie
            animationLink="https://assets1.lottiefiles.com/packages/lf20_16bo07fy.json"
            :width="300"
            :height="300"
          />
        </div>
        <div>
          <button class="primary-plain-button" @click="openURL('https://docs.fairshareapp.io/')">
            View the Documentation <el-icon><notebook-icon /></el-icon>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useDatasetsStore } from "@/store/datasets";

export default {
  name: "AppDocumentation",
  components: {},
  data() {
    return {
      datasetStore: useDatasetsStore(),
      open: true,
    };
  },
  methods: {
    openURL(url) {
      window.ipcRenderer.send("open-link-in-browser", url);
    },
  },
  computed: {},
  async mounted() {
    this.datasetStore.hideProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(1);
  },
};
</script>

<style scoped lang="css"></style>
