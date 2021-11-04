import { createRouter, createWebHistory } from "vue-router";

import HomePage from "../views/HomePage.vue";
import ProjectsShowAll from "../views/ProjectsShowAll.vue";
import ProjectsCreateNew from "../views/ProjectsCreateNew.vue";
import ProjectsCreateNewConfirm from "../views/ProjectsCreateNewConfirm.vue";
import DatasetsCurateSelectFolder from "../views/DatasetsCurateSelectFolder.vue";
import DatasetsCurateCreateMetadata from "../views/DatasetsCurateCreateMetadata.vue";
import DatasetsCurateMetadataReview from "../views/DatasetsCurateMetadataReview.vue";
import DatasetsCurateSelectDestination from "../views/DatasetsCurateSelectDestination.vue";
import DatasetsCurateZenodoMetadata from "../views/DatasetsCurateZenodoMetadata.vue";
import DatasetsCurateZenodoReview from "../views/DatasetsCurateZenodoReview.vue";
import DatasetsCurateHome from "../views/DatasetsCurateHome.vue";
import About from "../views/about.vue";

const routes = [
  { path: "/", redirect: "/datasets" },
  { path: "/home", component: HomePage },
  { path: "/datasets", component: ProjectsShowAll, name: "ProjectsShowAll" },
  {
    path: "/datasets/new",
    component: ProjectsCreateNew,
    name: "ProjectsCreateNew",
  },
  {
    path: "/datasets/new/:datasetID/confirm",
    component: ProjectsCreateNewConfirm,
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
    path: "/datasets/:datasetID/:workflowID/createMetadata/review",
    component: DatasetsCurateMetadataReview,
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
    path: "/datasets/:datasetID/:workflowID/zenodo/review",
    component: DatasetsCurateZenodoReview,
    name: "ZenodoReview",
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
