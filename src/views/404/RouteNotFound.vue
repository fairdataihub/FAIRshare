<template>
  <div class="flex h-full w-full max-w-screen-lg flex-col items-center justify-center p-3 pr-5">
    <div class="flex h-full w-full flex-col">
      <div class="flex h-full w-full flex-col items-center justify-start">
        <Vue3Lottie
          animationLink="https://assets1.lottiefiles.com/packages/lf20_dunbcj4q.json"
          :width="500"
          :height="500"
        />

        <p class="pb-5">Please submit an issue if this problem persists.</p>

        <div class="flex items-center justify-center space-x-4">
          <router-link :to="`/contactUs`">
            <button class="primary-plain-button">
              <el-icon><chat-dot-round /></el-icon> Report an issue
            </button>
          </router-link>
          <router-link :to="`/datasets`">
            <button class="primary-button">
              <el-icon><data-line /></el-icon> Go to the homepage
            </button>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useDatasetsStore } from "@/store/datasets";

export default {
  name: "RouteNotFound",
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

    this.$track("Error", "Routing ", this.$route.path);
  },
};
</script>

<style scoped></style>
