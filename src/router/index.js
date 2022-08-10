import { createRouter, createWebHistory } from "vue-router";

// project related components
import ShowAllProjects from "../views/project/ShowAllProjects.vue";
import CreateNewProject from "../views/project/CreateNewProject.vue";
import CreateNewProjectConfirm from "../views/project/CreateNewProjectConfirm.vue";
import EditProject from "../views/project/EditProject.vue";
import ShowAllWorkflows from "../views/project/ShowAllWorkflows.vue";

// Code metadata related components
import CodeLanding from "../views/workflow/Code/CodeLanding.vue";
import CodeSelectSourceFolder from "../views/workflow/Code/SelectSourceFolder.vue";
import CodeCreateMetadata from "../views/workflow/Code/CreateMetadata.vue";
import CodeCreateMetadataReview from "../views/workflow/Code/CreateMetadataReview.vue";
import CodeReviewStandards from "../views/workflow/Code/ReviewStandards.vue";
import CodePickLicense from "../views/workflow/Code/PickLicense.vue";
import CodeSelectGithubRepo from "../views/workflow/Code/SelectGithubRepo.vue";

// Other metadata related components
import OtherLanding from "../views/workflow/Other/OtherLanding.vue";
import OtherSelectSourceFolder from "../views/workflow/Other/SelectSourceFolder.vue";
import OtherReviewStandards from "../views/workflow/Other/ReviewStandards.vue";
import OtherCreateMetadata from "../views/workflow/Other/CreateMetadata.vue";
import OtherPickLicense from "../views/workflow/Other/PickLicense.vue";

// NextGenHighThroughputSequencing metadata related components
import NextGenHighThroughputSequencingLanding from "../views/workflow/NextGenHighThroughputSequencing/NextGenHighThroughputSequencingLanding.vue";
import NextGenHighThroughputSequencingSelectSourceFolder from "../views/workflow/NextGenHighThroughputSequencing/SelectSourceFolder.vue";
import NextGenHighThroughputSequencingReviewStandards from "../views/workflow/NextGenHighThroughputSequencing/ReviewStandards.vue";
import NextGenHighThroughputSequencingCreateMetadata from "../views/workflow/NextGenHighThroughputSequencing/CreateMetadata.vue";

// workflow related components
import SelectRepositoryDestination from "../views/workflow/SelectRepositoryDestination.vue";

// zenodo related components
import ZenodoMetadata from "../views/zenodo/ZenodoMetadata.vue";
import ZenodoMetadataReview from "../views/zenodo/ZenodoMetadataReview.vue";
import ZenodoAccessToken from "../views/zenodo/ZenodoAccessToken.vue";
import ZenodoUpload from "../views/zenodo/ZenodoUpload.vue";
import ZenodoPublish from "../views/zenodo/ZenodoPublish.vue";

// figshare related components
import FigshareMetadata from "../views/figshare/FigshareMetadata.vue";
import FigshareAccessToken from "../views/figshare/FigshareAccessToken.vue";
import FigshareUpload from "../views/figshare/FigshareUpload.vue";
import FigsharePublish from "../views/figshare/FigsharePublish.vue";

// github related components
import GithubZenodoConnection from "../views/github/GithubZenodoConnection.vue";
import GithubChooseUpload from "../views/github/GithubChooseUpload.vue";
import GithubSummary from "../views/github/GithubSummary.vue";
import GithubZenodoUpload from "../views/github/GithubZenodoUpload.vue";
import GithubFigshareUpload from "../views/github/GithubFigshareUpload.vue";
import GithubPublish from "../views/github/GithubPublish.vue";

// bio.tools related components
import BioToolsAccessToken from "../views/biotools/BioToolsAccessToken.vue";
import BioToolsMetadata from "../views/biotools/BioToolsMetadata.vue";
import BioToolsReview from "../views/biotools/BioToolsReview.vue";

// ncbi geo related components
import GEOGenerate from "../views/ncbigeo/GEOGenerate.vue";
import GEOUpload from "../views/ncbigeo/GEOUpload.vue";
import GEOPublish from "../views/ncbigeo/GEOPublish.vue";

// integration related components
import ManageAccount from "../views/accounts/ManageAccount.vue";

// components required for options that can be skipped
import LocalNoUploadSummary from "../views/noUpload/LocalNoUploadSummary.vue";
import LocalNoUploadGenerate from "../views/noUpload/LocalNoUploadGenerate.vue";
import LocalNoUploadEnd from "../views/noUpload/LocalNoUploadEnd.vue";
import GithubNoUploadEnd from "../views/noUpload/GithubNoUploadEnd.vue";

import HomePage from "../views/home/HomePage.vue";
import AppSettings from "../views/settings/AppSettings.vue";
import AppDocumentation from "../views/documentation/AppDocumentation.vue";
import ContactUs from "../views/contact/ContactUs.vue";
import AppAbout from "../views/about/AppAbout.vue";
import RouteNotFound from "../views/404/RouteNotFound.vue";

const routes = [
  { path: "/", component: HomePage }, // not used for any purpose yet; use `/home` instead
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
    path: "/datasets/:datasetID/:workflowID/Code/landing",
    component: CodeLanding,
  },
  {
    path: "/datasets/:datasetID/:workflowID/Other/landing",
    component: OtherLanding,
  },
  {
    path: "/datasets/:datasetID/:workflowID/NextGenHighThroughputSequencing/landing",
    component: NextGenHighThroughputSequencingLanding,
  },
  {
    path: "/datasets/:datasetID/:workflowID/Code/selectFolder",
    component: CodeSelectSourceFolder,
  },
  {
    path: "/datasets/:datasetID/:workflowID/Other/selectFolder",
    component: OtherSelectSourceFolder,
  },
  {
    path: "/datasets/:datasetID/:workflowID/NextGenHighThroughputSequencing/selectFolder",
    component: NextGenHighThroughputSequencingSelectSourceFolder,
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
    path: "/datasets/:datasetID/:workflowID/Other/reviewStandards",
    component: OtherReviewStandards,
  },
  {
    path: "/datasets/:datasetID/:workflowID/NextGenHighThroughputSequencing/reviewStandards",
    component: NextGenHighThroughputSequencingReviewStandards,
  },
  {
    path: "/datasets/:datasetID/:workflowID/Code/createMetadata",
    component: CodeCreateMetadata,
    name: "CodeCreateMetadata",
  },
  {
    path: "/datasets/:datasetID/:workflowID/Other/createMetadata",
    component: OtherCreateMetadata,
    name: "OtherCreateMetadata",
  },
  {
    path: "/datasets/:datasetID/:workflowID/NextGenHighThroughputSequencing/createMetadata",
    component: NextGenHighThroughputSequencingCreateMetadata,
    name: "NextGenHighThroughputSequencingCreateMetadata",
  },
  {
    path: "/datasets/:datasetID/:workflowID/Code/pickLicense",
    component: CodePickLicense,
    name: "CodePickLicense",
  },
  {
    path: "/datasets/:datasetID/:workflowID/Other/pickLicense",
    component: OtherPickLicense,
    name: "OtherPickLicense",
  },
  {
    path: "/datasets/:datasetID/:workflowID/Code/createMetadata/review",
    component: CodeCreateMetadataReview,
    name: "CodeCreateMetadataReview",
  },
  {
    path: "/datasets/:datasetID/:workflowID/selectDestination",
    component: SelectRepositoryDestination,
    name: "SelectRepositoryDestination",
  },
  {
    path: "/datasets/:datasetID/:workflowID/zenodo/metadata",
    component: ZenodoMetadata,
    name: "ZenodoMetadata",
  },
  {
    path: "/datasets/:datasetID/:workflowID/figshare/metadata",
    component: FigshareMetadata,
    name: "FigshareMetadata",
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
    path: "/datasets/:datasetID/:workflowID/figshare/accessToken",
    component: FigshareAccessToken,
    name: "FigshareAccessToken",
  },
  {
    path: "/datasets/:datasetID/:workflowID/zenodo/upload",
    component: ZenodoUpload,
    name: "ZenodoUpload",
  },
  {
    path: "/datasets/:datasetID/:workflowID/figshare/upload",
    component: FigshareUpload,
    name: "FigshareUpload",
  },
  {
    path: "/datasets/:datasetID/:workflowID/ncbigeo/upload",
    component: GEOUpload,
    name: "GEOUpload",
  },

  {
    path: "/datasets/:datasetID/:workflowID/zenodo/publish",
    component: ZenodoPublish,
    name: "ZenodoPublish",
  },
  {
    path: "/datasets/:datasetID/:workflowID/figshare/publish",
    component: FigsharePublish,
    name: "FigsharePublish",
  },
  {
    path: "/datasets/:datasetID/:workflowID/ncbigeo/publish",
    component: GEOPublish,
    name: "GEOPublish",
  },
  {
    path: "/datasets/:datasetID/:workflowID/github/zenodoConnection",
    component: GithubZenodoConnection,
    name: "GithubZenodoConnection",
  },
  {
    path: "/datasets/:datasetID/:workflowID/github/summary",
    component: GithubSummary,
    name: "GithubSummary",
  },
  {
    path: "/datasets/:datasetID/:workflowID/ncbigeo/generate",
    component: GEOGenerate,
    name: "GEOGenerate",
  },
  {
    path: "/datasets/:datasetID/:workflowID/github/uploadZenodo",
    component: GithubZenodoUpload,
    name: "GithubZenodoUpload",
  },
  {
    path: "/datasets/:datasetID/:workflowID/github/uploadFigshare",
    component: GithubFigshareUpload,
    name: "GithubFigshareUpload",
  },
  {
    path: "/datasets/:datasetID/:workflowID/github/chooseUpload",
    component: GithubChooseUpload,
    name: "GithubChooseUpload",
  },
  {
    path: "/datasets/:datasetID/:workflowID/github/publish",
    component: GithubPublish,
    name: "GithubPublish",
  },
  {
    path: "/datasets/:datasetID/:workflowID/biotools/login",
    component: BioToolsAccessToken,
    name: "BioToolsAccessToken",
  },
  {
    path: "/datasets/:datasetID/:workflowID/biotools/metadata",
    component: BioToolsMetadata,
    name: "BioToolsMetadata",
  },
  {
    path: "/datasets/:datasetID/:workflowID/biotools/review",
    component: BioToolsReview,
    name: "BioToolsReview",
  },
  {
    path: "/datasets/:datasetID/:workflowID/localNoUpload/summary",
    component: LocalNoUploadSummary,
    name: "LocalNoUploadSummary",
  },
  {
    path: "/datasets/:datasetID/:workflowID/localNoUpload/generate",
    component: LocalNoUploadGenerate,
    name: "LocalNoUploadGenerate",
  },
  {
    path: "/datasets/:datasetID/:workflowID/localNoUpload/finalPage",
    component: LocalNoUploadEnd,
    name: "LocalNoUploadEnd",
  },
  {
    path: "/datasets/:datasetID/:workflowID/githubNoUpload/finalPage",
    component: GithubNoUploadEnd,
    name: "GithubNoUploadEnd",
  },

  { path: "/datasets/:datasetID", component: ShowAllWorkflows },
  { path: "/manageAccount", component: ManageAccount },
  { path: "/settings", component: AppSettings },
  { path: "/documentation", component: AppDocumentation },
  { path: "/contactUs", component: ContactUs },
  { path: "/about", component: AppAbout },

  { path: "/404", name: "404", component: RouteNotFound },
  { path: "/:pathMatch(.*)*", name: "404", component: RouteNotFound },
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
