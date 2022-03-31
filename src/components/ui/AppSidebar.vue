<template>
  <!-- component -->
  <div
    class="relative mr-3 flex h-screen min-h-screen w-full max-w-xs flex-col bg-gray-50 pt-2 pb-5"
    :class="{
      'w-72': sideBarOpen,
      'w-[85px]': !sideBarOpen,
      'debug-screens': environment !== 'production',
      'cursor-not-allowed': !datasetStore.sidebarVisible,
    }"
    style="transition: width 0.3s"
  >
    <div
      class="flex h-full w-full flex-col text-gray-700"
      :class="{ 'pointer-events-none': !datasetStore.sidebarVisible }"
    >
      <div class="relative flex flex-row justify-center p-2">
        <img v-if="sideBarOpen" class="m-4 w-28" src="../../assets/brand/logo.svg" />

        <div
          class="group absolute top-0 right-2 flex scale-100 transform cursor-pointer items-center justify-center p-1 transition-all hover:scale-110"
          :class="{ 'right-6': !sideBarOpen }"
          @click="sideBarOpen = !sideBarOpen"
          title="Open or close the sidebar"
        >
          <div id="menu-hamburger" :class="{ open: sideBarOpen }" class="">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>
      <nav
        class="flex h-full flex-grow flex-col justify-between px-4"
        :class="{ 'pt-10': !sideBarOpen }"
      >
        <div>
          <router-link to="/home" class="sideBarMenuItem">
            <el-icon><home-filled /></el-icon>
            <span v-show="sideBarOpen"> Overview </span>
          </router-link>
          <router-link to="/datasets" :class="[`sideBarMenuItem`, isDataset()]">
            <el-icon><data-line /></el-icon>
            <span v-show="sideBarOpen"> Curate & Share </span>
          </router-link>
        </div>
        <div>
          <router-link to="/manageAccount" class="sideBarMenuItem">
            <el-icon><user-icon /></el-icon>
            <span v-show="sideBarOpen"> Manage Accounts </span>
          </router-link>
          <router-link to="/settings" class="sideBarMenuItem">
            <el-icon><setting-icon /></el-icon>
            <span v-show="sideBarOpen"> Settings </span>
          </router-link>
          <router-link to="/documentation" class="sideBarMenuItem">
            <el-icon><collection-icon /></el-icon>
            <span v-show="sideBarOpen"> Documentation </span>
          </router-link>
          <router-link to="/contactUs" class="sideBarMenuItem">
            <el-icon><chat-dot-round /></el-icon>
            <span v-show="sideBarOpen"> Contact Us </span>
          </router-link>
          <router-link to="/about" class="sideBarMenuItem">
            <el-icon><postcard-icon /></el-icon>
            <span v-show="sideBarOpen"> About </span>
          </router-link>
          <div class="sideBarMenuItem !pointer-events-none !mb-0 !pb-0" v-if="sideBarOpen">
            <img src="../../assets/brand/fair-data-innovations-hub-logo.svg" class="w-[150px]" />
          </div>
          <div class="absolute bottom-0 right-3 hidden">
            <span class="text-xs text-gray-400">{{ environment }}</span>
          </div>
        </div>
      </nav>
    </div>
  </div>
</template>

<script>
import { useDatasetsStore } from "../../store/datasets";

export default {
  name: "AppSidebar",
  components: {},
  props: ["environment"],
  data() {
    return {
      dropdownOpen: false,
      datasetStore: useDatasetsStore(),
      process: process,
      sideBarOpen: true,
    };
  },
  watch: {
    "datasetStore.sidebarVisible": {
      handler(val) {
        this.sideBarOpen = val;
      },
      deep: true,
    },
  },
  methods: {
    isDataset: function () {
      if (this.$route.path.search("datasets") != -1) {
        return "router-link-active";
      }
      return "";
    },
  },
  created() {
    this.sideBarOpen = this.datasetStore.sidebarVisible;
  },
};
</script>
