<template>
  <!-- component -->
  <div
    class="md:flex flex-col md:flex-row md:min-h-screen mr-3"
    :class="{ 'w-40': sideBarOpen, 'w-10': !sideBarOpen }"
    style="transition: width 0.3s"
  >
    <div class="flex flex-col w-full text-gray-700 bg-white flex-shrink-0">
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
      <nav
        class="flex-grow px-4 md:pb-0 md:overflow-y-auto"
        v-show="sideBarOpen"
      >
        <router-link to="/home" class="sideBarMenuItem"> Overview </router-link>
        <router-link to="/about" class="sideBarMenuItem"> About </router-link>

        <div class="relative">
          <button
            @click="dropdownOpen = !dropdownOpen"
            class="
              flex flex-row
              items-end
              w-full
              px-4
              py-2
              mt-2
              text-sm
              font-semibold
              rounded-lg
              hover:bg-gray-200
              focus:bg-gray-200 focus:outline-none focus:shadow-outline
            "
          >
            <span>Dropdown</span>
            <svg
              fill="currentColor"
              viewBox="0 0 20 20"
              :class="{ 'rotate-180': dropdownOpen, 'rotate-0': !dropdownOpen }"
              class="
                inline
                w-4
                h-4
                mt-1
                ml-1
                transition-transform
                duration-200
                transform
                md:-mt-1
              "
            >
              <path
                fill-rule="evenodd"
                d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                clip-rule="evenodd"
              ></path>
            </svg>
          </button>
          <transition name="sideBarFade">
            <div
              v-if="dropdownOpen"
              class="
                absolute
                right-0
                w-full
                mt-2
                origin-top-right
                rounded-md
                shadow-lg
              "
            >
              <div
                class="
                  px-2
                  py-2
                  bg-white
                  rounded-md
                  shadow
                  dark-mode:bg-gray-800
                "
              >
                <a
                  class="
                    block
                    px-4
                    py-2
                    mt-2
                    text-sm
                    font-semibold
                    bg-transparent
                    rounded-lg
                    md:mt-0
                    hover:text-gray-900 hover:bg-gray-200
                  "
                  href="#"
                  >Link #1</a
                >
                <a
                  class="
                    block
                    px-4
                    py-2
                    mt-2
                    text-sm
                    font-semibold
                    bg-transparent
                    rounded-lg
                    md:mt-0
                    hover:text-gray-900
                    focus:text-gray-900
                    hover:bg-gray-200
                    focus:bg-gray-200
                  "
                  href="#"
                  >Link #2</a
                >
                <a
                  class="
                    block
                    px-4
                    py-2
                    mt-2
                    text-sm
                    font-semibold
                    bg-transparent
                    rounded-lg
                    md:mt-0
                    hover:text-gray-900
                    focus:text-gray-900
                    hover:bg-gray-200
                    focus:bg-gray-200
                  "
                  href="#"
                  >Link #3</a
                >
              </div>
            </div>
          </transition>
        </div>
      </nav>
    </div>
  </div>
</template>

<script>
export default {
  name: "AppSidebar",
  components: {},
  data() {
    return { dropdownOpen: false, sideBarOpen: true };
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
