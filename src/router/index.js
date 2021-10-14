import { createRouter, createWebHistory } from "vue-router";

import HomePage from "../views/HomePage.vue";
import DatasetsShowAll from "../views/DatasetsShowAll.vue";
import DatasetsCreateNew from "../views/DatasetsCreateNew.vue";
import DatasetsCreateNewConfirm from "../views/DatasetsCreateNewConfirm.vue";
import About from "../views/about.vue";

const routes = [
  { path: "/", redirect: "/datasets" },
  { path: "/home", component: HomePage },
  { path: "/datasets", component: DatasetsShowAll, name: "DatasetsShowAll" },
  {
    path: "/datasets/new",
    component: DatasetsCreateNew,
    name: "DatasetsCreateNew",
  },
  {
    path: "/datasets/new/:datasetID/confirm",
    component: DatasetsCreateNewConfirm,
  },
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
