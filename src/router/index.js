import { createRouter, createWebHistory } from "vue-router";

import HomePage from "../views/HomePage.vue";
import DatasetsShowAll from "../views/DatasetsShowAll.vue";
import DatasetsCreateNew from "../views/DatasetsCreateNew.vue";
import DatasetsCreateNewConfirm from "../views/DatasetsCreateNewConfirm.vue";
import DatasetsCurateSelectFolder from "../views/DatasetsCurateSelectFolder.vue";
import DatasetsCurateCreateMetadata from "../views/DatasetsCurateCreateMetadata.vue";
import DatasetsCurateSelectDestination from "../views/DatasetsCurateSelectDestination.vue";
import DatasetsCurateZenodoMetadata from "../views/DatasetsCurateZenodoMetadata.vue";
import DatasetsCurateHome from "../views/DatasetsCurateHome.vue";
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
  {
    path: "/datasets/:datasetID/:workflowID/selectFolder",
    component: DatasetsCurateSelectFolder,
  },
  {
    path: "/datasets/:datasetID/:workflowID/createMetadata",
    component: DatasetsCurateCreateMetadata,
  },
  {
    path: "/datasets/:datasetID/:workflowID/selectDestination",
    component: DatasetsCurateSelectDestination,
  },
  {
    path: "/datasets/:datasetID/:workflowID/zenodo/metadata",
    component: DatasetsCurateZenodoMetadata,
    name: "ZenodoMetadata",
  },
  {
    path: "/datasets/:datasetID/:workflowID/figshare/metadata",
    component: DatasetsCurateSelectDestination,
    name: "FigshareMetadata",
  },
  { path: "/datasets/:datasetID", component: DatasetsCurateHome },
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
