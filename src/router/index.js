import { createRouter, createWebHistory } from "vue-router";

import ShowAllProjects from "../views/project/ShowAllProjects.vue";
import CreateNewProject from "../views/project/CreateNewProject.vue";
import CreateNewProjectConfirm from "../views/project/CreateNewProjectConfirm.vue";
import ShowAllWorkflows from "../views/project/ShowAllWorkflows.vue";

import SelectSourceFolder from "../views/workflow/SelectSourceFolder.vue";
import CreateMetadata from "../views/workflow/CreateMetadata.vue";
import CreateMetadataReview from "../views/workflow/CreateMetadataReview.vue";
import SelectRepositoryDestination from "../views/workflow/SelectRepositoryDestination.vue";

import ZenodoMetadata from "../views/zenodo/ZenodoMetadata.vue";
import ZenodoMetadataReview from "../views/zenodo/ZenodoMetadataReview.vue";
import ZenodoAccessToken from "../views/zenodo/ZenodoAccessToken.vue";
import ZenodoUpload from "../views/zenodo/ZenodoUpload.vue";
import ZenodoPublish from "../views/zenodo/ZenodoPublish.vue";

// not used for any purpose yet
import HomePage from "../views/HomePage.vue";
import About from "../views/about.vue";

const routes = [
  { path: "/", redirect: "/datasets" },
  { path: "/home", component: HomePage },
  { path: "/datasets", component: ShowAllProjects, name: "ShowAllProjects" },
  {
    path: "/datasets/new",
    component: CreateNewProject,
    name: "CreateNewProject",
  },
  {
    path: "/datasets/new/:datasetID/confirm",
    component: CreateNewProjectConfirm,
  },
  {
    path: "/datasets/:datasetID/:workflowID/selectFolder",
    component: SelectSourceFolder,
  },
  {
    path: "/datasets/:datasetID/:workflowID/createMetadata",
    component: CreateMetadata,
  },
  {
    path: "/datasets/:datasetID/:workflowID/createMetadata/review",
    component: CreateMetadataReview,
  },
  {
    path: "/datasets/:datasetID/:workflowID/selectDestination",
    component: SelectRepositoryDestination,
  },
  {
    path: "/datasets/:datasetID/:workflowID/zenodo/metadata",
    component: ZenodoMetadata,
    name: "ZenodoMetadata",
  },
  {
    path: "/datasets/:datasetID/:workflowID/zenodo/review",
    component: ZenodoMetadataReview,
    name: "ZenodoMetadataReview",
  },
  {
    path: "/datasets/:datasetID/:workflowID/zenodo/accessToken",
    component: ZenodoAccessToken,
    name: "ZenodoAccessToken",
  },
  {
    path: "/datasets/:datasetID/:workflowID/zenodo/upload",
    component: ZenodoUpload,
    name: "ZenodoUpload",
  },
  {
    path: "/datasets/:datasetID/:workflowID/zenodo/publish",
    component: ZenodoPublish,
    name: "ZenodoPublish",
  },
  {
    path: "/datasets/:datasetID/:workflowID/figshare/metadata",
    name: "FigshareMetadata",
  },
  { path: "/datasets/:datasetID", component: ShowAllWorkflows },
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
