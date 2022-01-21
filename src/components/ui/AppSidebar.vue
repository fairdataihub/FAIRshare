<template>
  <!-- component -->
  <div
    class="relative flex flex-col w-full h-screen max-w-xs min-h-screen pt-2 pb-5 mr-3 debug-screens bg-gray-50"
    :class="{
      'w-72': sideBarOpen,
      'w-[85px]': !sideBarOpen,
      'debug-screens': environment !== 'production',
    }"
    style="transition: width 0.3s"
  >
    <div class="flex flex-col w-full h-full text-gray-700">
      <div class="relative flex flex-row justify-center p-2">
        <img
          v-if="sideBarOpen"
          class="m-4 w-28"
          src="../../assets/brand/logo.png"
        />

        <div
          class="absolute top-0 flex items-center justify-center p-1 transition-all transform scale-100 cursor-pointer right-2 hover:scale-110 group"
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
        class="flex flex-col justify-between flex-grow h-full px-4"
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
          <router-link to="/appSettings" class="sideBarMenuItem">
            <el-icon><setting-icon /></el-icon>
            <span v-show="sideBarOpen"> Settings </span>
          </router-link>
          <router-link to="/appDocumentation" class="sideBarMenuItem">
            <el-icon><collection-icon /></el-icon>
            <span v-show="sideBarOpen"> Documentation </span>
          </router-link>
          <router-link to="/ContactUs" class="sideBarMenuItem">
            <el-icon><chat-dot-round /></el-icon>
            <span v-show="sideBarOpen"> Contact Us </span>
          </router-link>
          <div class="absolute bottom-0 hidden right-3">
            <span class="text-xs text-gray-400">{{ environment }}</span>
          </div>
        </div>
      </nav>
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
