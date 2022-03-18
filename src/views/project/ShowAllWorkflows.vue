<template>
  <div class="flex h-screen w-full flex-row items-center justify-center">
    <div ref="" class="flex h-full flex-row items-center p-3">
      <div class="flex h-full flex-col overflow-y-auto">
        <span class="text-left text-lg font-medium"> Start the curation process </span>

        <span class="">
          When you are ready, click on the curation buttons below to fill out some metadata
          information.
        </span>

        <el-divider> </el-divider>

        <div class="flex flex-col p-2" v-for="(workflow, key) in dataset.workflows" :key="key">
          <div class="bg-gray-300 px-4 py-2">
            <span class="text-lg">
              {{ combineDataTypes(workflow.type) }}
            </span>
          </div>
          <div class="flex items-center justify-start bg-gray-200 px-4 py-2">
            <!-- <el-button
              type="primary"
              @click="navigateToCurate(`${key}`)"
              :disabled="workflow.datasetPublished"
            >
              Curate {{ combineDataTypes(workflow.type) }}
              <el-icon><arrow-right-bold /></el-icon>
            </el-button> -->
            <button
              class="primary-plain-button"
              @click="navigateToCurate(`${key}`)"
              ref="continueButton"
            >
              Curate {{ combineDataTypes(workflow.type) }}
              <el-icon><arrow-right-bold /></el-icon>
            </button>
            <br />
          </div>
        </div>
        <info-confirm
          ref="infoConfirmWorkflowPublished"
          title="Dataset is already published"
          @messageConfirmed="navigateToSelectFolder"
          confirmButtonText="I want to publish a new version"
        >
          <p class="text-center text-base text-gray-500">
            It looks like you've already published this dataset. Would you like to go through this
            workflow again to publish a new version?
          </p>
        </info-confirm>
        <info-confirm
          ref="infoConfirmLocalZenodoUploadNoPublish"
          title="You haven't published this dataset yet"
          @messageConfirmed="localZenodoUploadNoPublishResponse('ok')"
          @messageCancel="localZenodoUploadNoPublishResponse('cancel')"
          confirmButtonText="I want to publish"
          cancelButtonText="I want to upload my data again"
        >
          <p class="text-center text-base text-gray-500">
            It looks like you have already uploaded this dataset to Zenodo but you haven't published
            it yet. Would you like to publish this now or create a new upload for this specific
            workflow?
          </p>
        </info-confirm>
        <info-confirm
          ref="infoConfirmGithubUploadNoPublish"
          title="You haven't published this dataset yet"
          @messageConfirmed="localGithubUploadNoPublishResponse('ok')"
          @messageCancel="localGithubUploadNoPublishResponse('cancel')"
          confirmButtonText="I want to publish"
          cancelButtonText="I want to upload my data again"
        >
          <p class="text-center text-base text-gray-500">
            It looks like you have already uploaded this dataset to GitHub but you haven't published
            it yet. Would you like to publish this now or create a new upload for this specific
            workflow?
          </p>
        </info-confirm>
        <info-confirm
          ref="infoConfirmContinueCuration"
          title="Continue where you left off"
          @messageConfirmed="continueCuration('ok')"
          @messageCancel="continueCuration('cancel')"
          confirmButtonText="Yes, continue"
          cancelButtonText="No, start from the beginning"
        >
          <p class="text-center text-base text-gray-500">
            It looks like you were working on this workflow before. Would you like to continue where
            you left off?
          </p>
        </info-confirm>
      </div>
    </div>
    <app-docs-link url="curate-and-share/your-workflows" position="bottom-4" />
  </div>
</template>

<script>
import { useDatasetsStore } from "@/store/datasets";

export default {
  name: "ShowAllWorkflows",

  data() {
    return {
      datasetStore: useDatasetsStore(),
      dataset: {},
      currentOptions: {},
      datasetID: this.$route.params.datasetID,
      workflowID: "",
    };
  },
  methods: {
    combineDataTypes(dataTypes) {
      if (dataTypes.length === 1) {
        return dataTypes[0] === "Code" ? "Research Software" : dataTypes[0];
      } else if (dataTypes.length === 2) {
        return `${dataTypes[0]} and ${dataTypes[1]}`;
      } else if (dataTypes.length > 2) {
        let returnString = "";
        dataTypes.forEach((type, index) => {
          if (index === dataTypes.length - 1) {
            returnString += `and ${type}`;
          } else {
            returnString += `${type}, `;
          }
        });
        return returnString;
      }
    },
    async navigateToSelectFolder() {
      this.dataset.workflows[this.workflowID].datasetUploaded = false;
      this.dataset.workflows[this.workflowID].datasetPublished = false;

      this.datasetStore.updateCurrentDataset(this.dataset);
      this.datasetStore.syncDatasets();

      const routerPath = `/datasets/${this.datasetID}/${this.workflowID}/Code/selectFolder`;
      this.$router.push({ path: routerPath });
    },
    async localZenodoUploadNoPublishResponse(response) {
      let routerPath = "";
      if (response === "ok") {
        routerPath = `/datasets/${this.datasetID}/${this.workflowID}/zenodo/publish`;
        this.$router.push({ path: routerPath });
      } else if (response === "cancel") {
        this.dataset.workflows[this.workflowID].datasetUploaded = false;
        this.dataset.workflows[this.workflowID].datasetPublished = false;

        await this.datasetStore.updateCurrentDataset(this.dataset);
        await this.datasetStore.syncDatasets();

        routerPath = `/datasets/${this.datasetID}/${this.workflowID}/Code/selectFolder`;
        this.$router.push({ path: routerPath });
      }
    },
    localGithubUploadNoPublishResponse(response) {
      let routerPath = "";
      if (response === "ok") {
        routerPath = `/datasets/${this.datasetID}/${this.workflowID}/github/publish`;
        this.$router.push({ path: routerPath });
      } else if (response === "cancel") {
        routerPath = `/datasets/${this.datasetID}/${this.workflowID}/Code/selectFolder`;
        this.$router.push({ path: routerPath });
      }
    },
    continueCuration(response) {
      let routerPath = "";
      if (response === "ok") {
        routerPath = this.dataset.workflows[this.workflowID].currentRoute;
        this.$router.push({ path: routerPath });
      } else if (response === "cancel") {
        routerPath = `/datasets/${this.datasetID}/${this.workflowID}/Code/selectFolder`;
        this.$router.push({ path: routerPath });
      }
    },
    navigateToCurate(workflowID) {
      let routerPath = "";
      this.workflowID = workflowID;

      // add published checks before the upload ones
      // This hasn't been done yet since we need to figure out where we want to put them for this specific workflow.

      if (
        "datasetPublished" in this.dataset.workflows[workflowID] &&
        this.dataset.workflows[workflowID].datasetPublished &&
        "source" in this.dataset.workflows[workflowID] &&
        (this.dataset.workflows[workflowID].source.type === "local" ||
          this.dataset.workflows[workflowID].source.type === "github")
      ) {
        this.$refs.infoConfirmWorkflowPublished.show();
        return;
      }

      if (
        "datasetUploaded" in this.dataset.workflows[workflowID] &&
        this.dataset.workflows[workflowID].datasetUploaded &&
        "source" in this.dataset.workflows[workflowID] &&
        this.dataset.workflows[workflowID].source.type === "local"
      ) {
        this.$refs.infoConfirmLocalZenodoUploadNoPublish.show();
        return;
      }

      if (
        "datasetUploaded" in this.dataset.workflows[workflowID] &&
        this.dataset.workflows[workflowID].datasetUploaded &&
        "source" in this.dataset.workflows[workflowID] &&
        this.dataset.workflows[workflowID].source.type === "github"
      ) {
        this.$refs.infoConfirmGithubUploadNoPublish.show();
        return;
      }

      if ("currentRoute" in this.dataset.workflows[workflowID]) {
        if (
          this.dataset.workflows[workflowID].currentRoute != "" &&
          this.dataset.workflows[workflowID].currentRoute !=
            `/datasets/${this.datasetID}/${workflowID}/Code/selectFolder`
        ) {
          this.$refs.infoConfirmContinueCuration.show();
        } else {
          routerPath = `/datasets/${this.datasetID}/${workflowID}/Code/selectFolder`;
          this.$router.push({ path: routerPath });
        }
      } else {
        routerPath = `/datasets/${this.datasetID}/${workflowID}/Code/selectFolder`;
        this.$router.push({ path: routerPath });
      }

      // if ("datasetUploaded" in this.dataset.workflows[workflowID]) {
      //   if (this.dataset.workflows[workflowID].datasetUploaded) {
      //     routerPath = `/datasets/${this.datasetID}/${workflowID}/zenodo/publish`;
      //   } else {
      //     routerPath = `/datasets/${this.datasetID}/${workflowID}/Code/selectFolder`;
      //   }
      // } else {
      //   routerPath = `/datasets/${this.datasetID}/${workflowID}/Code/selectFolder`;
      // }
      // console.log(routerPath);
      // this.$router.push({ path: routerPath });
    },
  },
  async mounted() {
    this.dataset = await this.datasetStore.getCurrentDataset();

    if (!this.dataset.workflowConfirmed) {
      this.$router.push({ path: `/datasets/new/${this.dataset.id}/confirm` });
    }

    this.navigateToCurate("workflow1");
  },
};
</script>
