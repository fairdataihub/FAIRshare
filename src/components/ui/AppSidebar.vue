<template>
  <!-- component -->
  <div
    class="flex flex-col min-h-screen mr-3 debug-screens bg-gray-50"
    :class="{
      'w-64': sideBarOpen,
      'w-12': !sideBarOpen,
      'debug-screens': process.env.NODE_ENV === 'production',
    }"
    style="transition: width 0.3s"
  >
    <div class="flex flex-col w-full text-gray-700 ">
      <div class="p-2 flex flex-row justify-center relative">
        <img
          v-if="sideBarOpen"
          class="w-28"
          src="https://www.freepnglogos.com/uploads/shape/shape-vector-red-abstract-png-vector-psd-and-clipart-with-13.png"
        />
        <div class="absolute top-0 right-2" @click="sideBarOpen = !sideBarOpen">
          <div id="menu-hamburger" :class="{ open: sideBarOpen }">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
        <div class="invisible">
          <div id="menu-hamburger">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>
      <nav class="flex-grow px-4 pb-0 overflow-y-auto" v-show="sideBarOpen">
        <router-link to="/home" class="sideBarMenuItem"> Overview </router-link>
        <router-link to="/datasets" :class="[`sideBarMenuItem`, isDataset()]">
          Continue curation
        </router-link>
        <router-link to="/about" class="sideBarMenuItem"> About </router-link>
        <router-link
          to="/datasets/new/f1f6c588-d79c-4235-b9ef-7cb7bfb95b8e/confirm"
          class="sideBarMenuItem"
        >
          Confirm
        </router-link>
      </nav>
    </div>
  </div>
</template>

<script>
export default {
  name: "AppSidebar",
  components: {},
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

<style lang="postcss">
.sideBarFade-enter-active,
.sideBarFade-leave-active {
  @apply transition-all;
}

.sideBarFade-enter-to,
.sideBarFade-leave {
  @apply opacity-100 scale-100;
}

.sideBarFade-enter,
.sideBarFade-leave-to {
  @apply opacity-0 scale-95;
}
</style>

<style lang="postcss">
#menu-hamburger {
  width: 23px;
  height: 10px;
  position: relative;
  margin: 10px 0;
  transform: rotate(0deg);
  transition: 0.5s ease-in-out;
  cursor: pointer;
}

#menu-hamburger span {
  display: block;
  position: absolute;
  height: 4px;
  width: 100%;
  background: #5f5d5b;
  border-radius: 9px;
  opacity: 1;
  left: 0;
  transform: rotate(0deg);
  transition: 0.25s ease-in-out;
}

#menu-hamburger span:nth-child(1) {
  top: 0px;
  transform-origin: left center;
}

#menu-hamburger span:nth-child(2) {
  top: 8px;
  transform-origin: left center;
}

#menu-hamburger span:nth-child(3) {
  top: 16px;
  transform-origin: left center;
}

#menu-hamburger.open span:nth-child(1) {
  width: 23px;
  transform: rotate(45deg);
  top: 0px;
  left: 6px;
}

#menu-hamburger.open span:nth-child(2) {
  width: 0%;
  opacity: 0;
}

#menu-hamburger.open span:nth-child(3) {
  width: 23px;
  transform: rotate(-45deg);
  top: 16px;
  left: 6px;
}
</style>
