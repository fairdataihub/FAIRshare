<template>
  <div
    class="flex h-full w-full max-w-screen-lg flex-col items-center justify-center p-3 pr-5"
  >
    <div class="flex h-full w-full flex-col">
      <h1 class="pt-5 pb-1 text-3xl font-bold text-slate-700">
        About FAIRshare
      </h1>

      <line-divider></line-divider>

      <div class="flex w-full flex-col items-center justify-start">
        <Vue3Lottie
          animationLink="https://assets5.lottiefiles.com/packages/lf20_q7zl3bxr.json"
          :width="300"
          :height="300"
        />
      </div>
      <div>
        <el-descriptions :column="3" size="large" border>
          <el-descriptions-item v-for="item in about" :key="item">
            <template #label>
              <div class="cell-item">{{ item.label }}</div>
            </template>
            {{ item.value }}
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </div>
    <div class="flex w-full items-center justify-center pb-2">
      <p class="mr-2">Made with</p>
      <Vue3Lottie
        animationLink="https://assets4.lottiefiles.com/packages/lf20_jiniaoj3.json"
        :width="20"
        :height="20"
        :speed="0.7"
      />
      <p class="ml-2">by FAIR Data Innovations Hub</p>
    </div>
  </div>
</template>

<script>
import { useDatasetsStore } from "@/store/datasets";
import { app } from "@electron/remote";

export default {
  name: "AppDocumentation",
  components: {},
  data() {
    return {
      datasetStore: useDatasetsStore(),
      about: [],
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

    this.about.push({
      label: "FAIRshare version",
      value: app.getVersion(),
      span: 1,
    });

    this.about.push({ label: "Locale", value: app.getLocale(), span: 1 });

    this.about.push({
      label: "Electron",
      value: process.versions.electron,
      span: 1,
    });

    this.about.push({
      label: "Node.js",
      value: process.versions.node,
      span: 1,
    });

    this.about.push({
      label: "Chromium",
      value: process.versions.chrome,
      span: 1,
    });

    this.about.push({
      label: "V8",
      value: process.versions.v8,
      span: 1,
    });

    this.about.push({
      label: "OS",
      value: process.platform,
      span: 1,
    });

    this.about.push({
      label: "pid",
      value: process.pid,
      span: 1,
    });

    this.about.push({
      label: "ppid",
      value: process.ppid,
      span: 1,
    });

    this.about.push({
      label: "Application path",
      value: app.getAppPath(),
      span: 1,
    });
  },
};
</script>

<style scoped></style>
