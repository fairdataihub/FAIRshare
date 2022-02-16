<template>
  <div
    class="flex h-full w-full max-w-screen-lg flex-col items-center justify-center p-3 pr-5"
  >
    <div class="flex h-full w-full flex-col">
      <h1 class="pt-5 pb-1 text-3xl font-bold text-slate-700">Contact Us</h1>

      <line-divider></line-divider>

      <h2>
        If you have any issues with FAIRShare, please create an issue on GitHub.
        For any other questions, please contact us at using the links below.
      </h2>

      <div class="flex h-full w-full flex-col items-center justify-start">
        <div>
          <Vue3Lottie
            animationLink="https://assets3.lottiefiles.com/packages/lf20_u25cckyh.json"
            :width="300"
            :height="300"
          />
        </div>
        <div class="flex items-center justify-center space-x-4">
          <button
            class="secondary-plain-button"
            @click="
              openURL(
                'https://github.com/fairdataihub/SODA-for-COVID-19-Research/issues/new/choose'
              )
            "
          >
            <el-icon><ticket-icon /></el-icon> I have an issue with FAIRShare
          </button>
          <button
            class="primary-plain-button"
            @click="openURL('https://fairdataihub.org/contact-us')"
          >
            Send us a message <el-icon><chat-dot-round /></el-icon>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useDatasetsStore } from "@/store/datasets";

export default {
  name: "ContactUs",
  components: {},
  data() {
    return {
      datasetStore: useDatasetsStore(),
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

<style scoped></style>
