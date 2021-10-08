<template>
  <!-- component -->
  <div class="md:flex flex-col md:flex-row md:min-h-screen w-full">
    <div
      class="
        flex flex-col
        w-full
        md:w-64
        text-gray-700
        bg-white
        flex-shrink-0
      "
    >
      <div
        class="
          flex-shrink-0
          px-8
          py-4
          flex flex-row
          items-center
          justify-between
        "
      >
        <p
          href="#"
          class="
            text-lg
            font-semibold
            tracking-widest
            text-gray-900
            uppercase
            rounded-lg
            dark-mode:text-white
            focus:outline-none focus:shadow-outline
          "
        >
          SODA for COVID-19 Research
        </p>
        <button
          class="rounded-lg md:hidden focus:outline-none focus:shadow-outline"
          @click="open = !open"
        >
          <svg fill="currentColor" viewBox="0 0 20 20" class="w-6 h-6">
            <path
              x-show="!open"
              fill-rule="evenodd"
              d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM9 15a1 1 0 011-1h6a1 1 0 110 2h-6a1 1 0 01-1-1z"
              clip-rule="evenodd"
            ></path>
            <path
              x-show="open"
              fill-rule="evenodd"
              d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
              clip-rule="evenodd"
            ></path>
          </svg>
        </button>
      </div>
      <nav
        :class="{ block: open, hidden: !open }"
        class="flex-grow md:block px-4 pb-4 md:pb-0 md:overflow-y-auto"
      >
        <router-link
          to="/home"
          class="
            block
            px-4
            py-2
            mt-2
            text-sm
            font-semibold
            text-gray-900
            rounded-lg
            hover:text-gray-900
            focus:text-gray-900
            hover:bg-gray-200
            focus:bg-gray-200 focus:outline-none focus:shadow-outline
          "
        >
          Blog
        </router-link>
        <router-link
          to="/portfolio"
          class="
            block
            px-4
            py-2
            mt-2
            text-sm
            font-semibold
            text-gray-900
            rounded-lg
            hover:text-gray-900
            focus:text-gray-900
            hover:bg-gray-200
            focus:bg-gray-200 focus:outline-none focus:shadow-outline
          "
        >
          Portfolio
        </router-link>

        <div class="relative" x-data="{ open: false }">
          <button
            @click="dropdownOpen = !dropdownOpen"
            class="
              flex flex-row
              items-center
              w-full
              px-4
              py-2
              mt-2
              text-sm
              font-semibold
              text-left
              bg-transparent
              rounded-lg
              md:block
              hover:text-gray-900
              focus:text-gray-900
              hover:bg-gray-200
              focus:bg-gray-200 focus:outline-none focus:shadow-outline
            "
          >
            <span>Dropdown</span>
            <svg
              fill="currentColor"
              viewBox="0 0 20 20"
              :class="{ 'rotate-180': open, 'rotate-0': !open }"
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
          <div
            v-show="dropdownOpen"
            x-transition:enter="transition ease-out duration-100"
            x-transition:enter-start="transform opacity-0 scale-95"
            x-transition:enter-end="transform opacity-100 scale-100"
            x-transition:leave="transition ease-in duration-75"
            x-transition:leave-start="transform opacity-100 scale-100"
            x-transition:leave-end="transform opacity-0 scale-95"
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
              class="px-2 py-2 bg-white rounded-md shadow dark-mode:bg-gray-800"
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
                  focus:bg-gray-200 focus:outline-none focus:shadow-outline
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
                  focus:bg-gray-200 focus:outline-none focus:shadow-outline
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
                  focus:bg-gray-200 focus:outline-none focus:shadow-outline
                "
                href="#"
                >Link #3</a
              >
            </div>
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
  data() {
    return { dropdownOpen: false };
  },
};
</script>

<style></style>
