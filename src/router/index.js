import { createRouter, createWebHistory } from "vue-router";

import HomePage from "../views/HomePage.vue";
import AllDatasets from "../views/AllDatasets.vue";
import NewDataset from "../views/NewDataset.vue";
import About from "../views/about.vue";

const routes = [
  { path: "/", redirect: "/datasets" },
  { path: "/home", component: HomePage },
  { path: "/datasets", component: AllDatasets },
  { path: "/datasets/new", component: NewDataset },
  { path: "/datasets/new/:datasetID/confirm", component: HomePage },
  { path: "/datasets/:datasetID", component: HomePage },
  { path: "/about", component: About },
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
