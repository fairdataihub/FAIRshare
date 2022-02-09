import { createRouter, createWebHistory } from "vue-router";

// project related components
import ShowAllProjects from "../views/project/ShowAllProjects.vue";
import CreateNewProject from "../views/project/CreateNewProject.vue";
import CreateNewProjectConfirm from "../views/project/CreateNewProjectConfirm.vue";
import EditProject from "../views/project/EditProject.vue";
import ShowAllWorkflows from "../views/project/ShowAllWorkflows.vue";
import ProjectLanding from "../views/project/ProjectLanding.vue";

// Code metadata related components
import CodeSelectSourceFolder from "../views/workflow/Code/SelectSourceFolder.vue";
import CodeCreateMetadata from "../views/workflow/Code/CreateMetadata.vue";
import CodeCreateMetadataReview from "../views/workflow/Code/CreateMetadataReview.vue";
import CodeReviewStandards from "../views/workflow/Code/ReviewStandards.vue";
import CodePickLicense from "../views/workflow/Code/PickLicense.vue";
import CodeSelectGithubRepo from "../views/workflow/Code/SelectGithubRepo.vue";

// workflow related components
import SelectRepositoryDestination from "../views/workflow/SelectRepositoryDestination.vue";

// zenodo related components
import ZenodoMetadata from "../views/zenodo/ZenodoMetadata.vue";
import ZenodoMetadataReview from "../views/zenodo/ZenodoMetadataReview.vue";
import ZenodoAccessToken from "../views/zenodo/ZenodoAccessToken.vue";
import ZenodoUpload from "../views/zenodo/ZenodoUpload.vue";
import ZenodoPublish from "../views/zenodo/ZenodoPublish.vue";

// github related components
import GithubZenodoConnection from "../views/github/GithubZenodoConnection.vue";
import GithubUpload from "../views/github/GithubUpload.vue";

// integration related components
import ManageAccount from "../views/manage/ManageAccount.vue";

import AppSettings from "../views/settings/AppSettings.vue";
import AppDocumentation from "../views/documentation/AppDocumentation.vue";
import ContactUs from "../views/contact/ContactUs.vue";

// not used for any purpose yet
import HomePage from "../views/HomePage.vue";

const routes = [
  { path: "/", component: HomePage },
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
    path: "/datasets/:datasetID/edit",
    component: EditProject,
  },
  {
    path: "/datasets/:datasetID/landing",
    component: ProjectLanding,
  },
  {
    path: "/datasets/:datasetID/:workflowID/Code/selectFolder",
    component: CodeSelectSourceFolder,
  },
  {
    path: "/datasets/:datasetID/:workflowID/Code/selectGithubRepo",
    component: CodeSelectGithubRepo,
  },
  {
    path: "/datasets/:datasetID/:workflowID/Code/reviewStandards",
    component: CodeReviewStandards,
  },
  {
    path: "/datasets/:datasetID/:workflowID/Code/createMetadata",
    component: CodeCreateMetadata,
  },
  {
    path: "/datasets/:datasetID/:workflowID/Code/pickLicense",
    component: CodePickLicense,
  },
  {
    path: "/datasets/:datasetID/:workflowID/Code/createMetadata/review",
    component: CodeCreateMetadataReview,
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
    path: "/datasets/:datasetID/:workflowID/github/zenodoConnection",
    component: GithubZenodoConnection,
    name: "GithubZenodoConnection",
  },
  {
    path: "/datasets/:datasetID/:workflowID/github/upload",
    component: GithubUpload,
    name: "GithubUpload",
  },
  {
    path: "/datasets/:datasetID/:workflowID/figshare/metadata",
    name: "FigshareMetadata",
  },
  { path: "/datasets/:datasetID", component: ShowAllWorkflows },
  { path: "/manageAccount", component: ManageAccount },
  { path: "/settings", component: AppSettings },
  { path: "/documentation", component: AppDocumentation },
  { path: "/contactUs", component: ContactUs },
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
