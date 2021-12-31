<template>
  <div class="h-full w-full flex flex-col justify-center items-center pr-5 p-3">
    <div class="flex flex-col h-full w-full items-center">
      <div class="empty-Padding"></div>
      <div class="title1">
        <span class="text-5xl 2xl:text-7xl transition-all">
          SODA for COVID-19 Research
        </span>
      </div>
      <div class="title2">
        <span class="text-2xl 2xl:text-4xl transition-all">
          Make your COVID-19 related data, and beyond, FAIR
        </span>
      </div>
      <div class="svg-containers">
        <div class="flex flex-col w-72 item-center justify-center gap-4">
          <div class="w-72 flex item-center justify-center">
            <img
              src="../assets/1.svg"
              class="h-36 w-36 2xl:w-48 transition-all"
            />
          </div>
          <div>
            Example text text text text text text text text text text text text
            text text text text text text
          </div>
        </div>
        <div class="flex flex-col w-72 item-center justify-center gap-4">
          <div class="w-72 flex item-center justify-center">
            <img
              src="../assets/2.svg"
              class="h-36 w-36 2xl:w-48 transition-all"
            />
          </div>
          <div>
            Example text text text text text text text text text text text text
            text text text text text text
          </div>
        </div>
        <div class="flex flex-col w-72 item-center justify-center gap-4">
          <div class="w-72 flex item-center justify-center">
            <img
              src="../assets/1.svg"
              class="h-36 w-36 2xl:w-48 transition-all"
            />
          </div>
          <div>
            Example text text text text text text text text text text text text
            text text text text text text
          </div>
        </div>
      </div>
      <div class="button-container">
        <div class="button-area">
          <div class="square-buttons">
            <button
              class="secondary-plain-button"
              @click="
                openWebsite(
                  'https://github.com/fairdataihub/SODA-for-COVID-19-Research-Docs'
                )
              "
            >
              <span class="text-md 2xl:text-xl transition-all"
                >See documentation</span
              >
            </button>
            <button class="primary-plain-button" @click="startCuratingProject">
              <span class="text-md 2xl:text-xl transition-all"
                >Getting started</span
              >
              <el-icon> <d-arrow-right /> </el-icon>
            </button>
          </div>
          <div class="text-buttons">
            <div
              class="flex flex-row items-center w-max text-primary-600 cursor-pointer hover-underline-animation my-3"
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
    </div>
  </div>
</template>

<script>
// import licensesJSON from "../assets/supplementalFiles/licenses.json";
import { Icon } from "@iconify/vue";
export default {
  name: "HomePage",
  components: {
    Icon,
  },
  data() {
    return {
      // licenseOptions: licensesJSON.licenses,
      // sortedLicenses: [],
    };
  },
  methods: {
    // SortArray(x, y) {
    //   return x.name.localeCompare(y.name);
    // },
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
    // sort licenses alphabetically
    // this.sortedLicenses = this.licenseOptions.sort(this.SortArray);
    // console.log(this.sortedLicenses);
  },
};
</script>

<style scoped>
.empty-Padding {
  @apply w-full h-20;
}
.svg-containers {
  display: flex;
  align-items: center;
  justify-content: center;
  @apply w-full h-72 gap-28;
}
.title1 {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  @apply w-full h-28;
}
.title2 {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  @apply w-full h-28;
}
.button-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  box-sizing: border-box;
  @apply w-full h-48;
}
.button-area {
  width: 60%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  @apply h-48 gap-8;
}

.square-buttons {
  height: 30%;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  @apply gap-8;
}
.text-buttons {
  height: 10%;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
</style>
