<template>
  <!-- component -->
  <div
    class="flex flex-col min-h-screen h-full mr-3 debug-screens bg-gray-50 relative w-full max-w-xs pb-10 pt-2"
    :class="{
      'w-72': sideBarOpen,
      'w-12': !sideBarOpen,
      'debug-screens': environment !== 'production',
    }"
    style="transition: width 0.3s"
  >
    <div class="flex flex-col w-full text-gray-700">
      <div class="p-2 flex flex-row justify-center relative">
        <img
          v-if="sideBarOpen"
          class="w-28"
          src="https://www.freepnglogos.com/uploads/shape/shape-vector-red-abstract-png-vector-psd-and-clipart-with-13.png"
        />
        <div
          class="absolute top-0 right-2 cursor-pointer p-1 transition-all transform scale-100 hover:scale-110 flex justify-center items-center group"
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
      <nav class="flex-grow px-4 pb-0 overflow-y-auto" v-show="sideBarOpen">
        <router-link to="/home" class="sideBarMenuItem">
          <el-icon><home-filled /></el-icon> Overview
        </router-link>
        <router-link to="/datasets" :class="[`sideBarMenuItem`, isDataset()]">
          <el-icon><data-line /></el-icon> Curate & Share
        </router-link>
        <router-link to="/manageAccount" class="sideBarMenuItem">
          <el-icon><user /></el-icon> Manage Accounts
        </router-link>
        <!-- <router-link to="/about" class="sideBarMenuItem"> About </router-link>
        <router-link
          to="/datasets/0387b979-4b45-46bb-bb27-84aaf32c4cdb/workflow1/zenodo/metadata"
          class="sideBarMenuItem"
        >
          Confirm
        </router-link> -->
      </nav>
    </div>
    <div class="absolute bottom-0 right-3">
      <span class="text-gray-400 text-xs">{{ environment }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: "AppSidebar",
  components: {},
  props: ["environment"],
  data() {
    return { dropdownOpen: false, sideBarOpen: true, process: process };
  },
  methods: {
    isDataset: function () {
      if (this.$route.path.search("datasets") != -1) {
        return "router-link-active";
      }
      return "";
    },
  },
};
</script>
