import { createRouter, createWebHistory } from "vue-router";

import HomePage from "../views/home.vue";

const routes = [
  { path: "/", redirect: "/home" },
  { path: "/home", component: HomePage },
];

export const router = createRouter({
  history: createWebHistory(),
  scrollBehavior: function (to) {
    if (to.hash) {
      return {
        el: to.hash,
        behavior: "smooth",
      };
    } else {
      window.scrollTo(0, 0);
    }
  },
  routes,
});
