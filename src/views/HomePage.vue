<template>
  <div
    class="h-full w-full flex flex-col justify-center items-center pr-5 p-3 max-w-screen-xl"
  >
    <div class="flex flex-col h-full w-full items-center">
      <div
        class="w-full flex justify-center items-center text-5xl xl:text-6xl py-5"
      >
        SODA for COVID-19 Research
      </div>
      <div
        class="w-full flex justify-center items-center text-2xl xl:text-4xl py-3 mb-10"
      >
        Make your COVID-19 related data, and beyond, FAIR
      </div>
      <div class="w-full flex justify-evenly py-5 space-x-14">
        <div class="flex flex-col w-1/3 item-center justify-center">
          <div class="w-full flex item-center justify-center py-3">
            <img
              src="../assets/1.svg"
              class="w-full h-auto pointer-events-none"
            />
          </div>
          <p>
            Example text text text text text text text text text text text text
            text text text text text text
          </p>
        </div>
        <div class="flex flex-col w-1/3 item-center justify-center">
          <div class="w-full flex item-center justify-center py-3">
            <img
              src="../assets/1.svg"
              class="w-full h-auto pointer-events-none"
            />
          </div>
          <p>
            Example text text text text text text text text text text text text
            text text text text text text
          </p>
        </div>
        <div class="flex flex-col w-1/3 item-center justify-center">
          <div class="w-full flex item-center justify-center py-3">
            <img
              src="../assets/1.svg"
              class="w-full h-auto pointer-events-none"
            />
          </div>
          <p>
            Example text text text text text text text text text text text text
            text text text text text text
          </p>
        </div>
      </div>
      <div class="flex flex-col justify-center items-center w-full py-3">
        <div class="flex justify-center space-x-4 py-3">
          <button
            class="secondary-plain-button text-base"
            @click="
              openWebsite(
                'https://github.com/fairdataihub/SODA-for-COVID-19-Research-Docs'
              )
            "
          >
            See documentation
          </button>
          <button
            class="primary-plain-button text-base"
            @click="startCuratingProject"
          >
            Getting started
            <el-icon> <d-arrow-right /> </el-icon>
          </button>
        </div>

        <div
          class="flex flex-row items-center text-primary-600 cursor-pointer hover-underline-animation py-3"
        >
          <span
            class="font-medium"
            @click="openWebsite('https://www.go-fair.org/fair-principles/')"
          >
            Learn more about FAIR
          </span>
          <Icon icon="grommet-icons:form-next-link" class="ml-2 h-5 w-5" />
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
