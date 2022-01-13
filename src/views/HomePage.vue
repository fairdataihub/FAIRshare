<template>
  <div
    class="flex flex-col items-center justify-center w-full h-full max-w-screen-lg p-3 pr-5"
  >
    <div class="flex flex-col items-center w-full h-full justify-evenly">
      <div class="pointer-events-none">
        <div class="flex items-center justify-center w-full py-5">
          <h1 class="text-3xl font-bold xl:text-4xl text-slate-800">
            SODA for COVID-19 Research
          </h1>
        </div>
        <div class="flex items-center justify-center w-full py-3 mb-1">
          <h2 class="text-2xl font-medium xl:text-3xl text-slate-700">
            Make your COVID-19 research data, and beyond, Findable, Accessible, Interoperable, and Reusable (FAIR)
          </h2>
        </div>
      </div>

      <div class="flex w-full py-3 justify-evenly space-x-14">
        <div class="flex flex-col justify-center  item-center">
          <div class="flex justify-center w-full py-3 item-center">
            <img
              src="../assets/overview.svg"
              class="w-full h-auto pointer-events-none"
            />
          </div>
        </div>
      </div>

      <div class="flex flex-col items-center justify-center w-full py-3">
        <div class="flex justify-center py-3 space-x-4">
          <button
            class="text-base secondary-plain-button"
            @click="
              openWebsite('https://soda-for-covid-19-research-docs.vercel.app/')
            "
          >
            <el-icon><notebook-icon /></el-icon>
            Read the documentation
          </button>

          <button
            class="text-base primary-plain-button"
            @click="startCuratingProject"
          >
            Getting started
            <el-icon class="icon-animate"> <d-arrow-right /> </el-icon>
          </button>
        </div>

        <div
          class="flex flex-row items-center py-1 pt-3 cursor-pointer text-primary-600 hover-underline-animation"
        >
          <span
            class="font-medium"
            @click="openWebsite('https://www.go-fair.org/fair-principles/')"
          >
            Learn more about FAIR
          </span>
          <Icon
            icon="grommet-icons:form-next-link"
            class="w-5 h-5 ml-2 icon-animate"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Icon } from "@iconify/vue";

export default {
  name: "HomePage",
  components: {
    Icon,
  },
  data() {
    return {};
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
  mounted() {},
};
</script>
