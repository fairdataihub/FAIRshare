<template>
  <div
    class="h-full w-full flex flex-col justify-center items-center p-3 px-5 max-w-screen-xl"
  >
    <div class="flex flex-col h-full w-full">
      <span class="font-medium text-left"> FAIRifying </span>

      <span> Let's make your research software FAIR. </span>

      <!-- <p class="py-1">
        In order to do this, SODA will automatically try to group up similar
        data into their own datasets.
      </p> -->

      <line-divider> </line-divider>

      <p class="py-2">
        FAIRShare will help you make you research software by guiding you
        step-by-step through the following process:
      </p>

      <ul class="list-decimal m-5">
        <li class="pb-3">
          <b> Select data files to be included </b>
          <p class="text-xs">
            You will be asked to select the location of the files (source code,
            executable, etc.) you want to include
          </p>
        </li>

        <li class="pb-3">
          <b> Ensure standard development practices are followed </b>
          <p class="text-xs">
            You will be asked a series a question to ensure standard practices
            have been followed when developing your software
          </p>
        </li>

        <li class="pb-3">
          <b> Provide metadata </b>
          <p class="text-xs">
            Information about your software will be requested and will be used
            to include the standard codemeta.json file in your dataset
          </p>
        </li>

        <li class="pb-3">
          <b> Select a suitable repository </b>
          <p class="text-xs">
            You will be prompted to select one of the suitable repositories for
            research software currently supported by FAIRShare
          </p>
        </li>

        <li class="pb-3">
          <b> Provide repository-specific metadata </b>
          <p class="text-xs">
            Metadata required by the selected repository will be requested
            (pre-populated from step #3 where there is an overlap)
          </p>
        </li>

        <li class="pb-3">
          <b> Upload dataset </b>
          <p class="text-xs">
            The standard codemeta.json and citation.json metadata files will be
            automatically included amongst your data files before uploading
            everything on the repository
          </p>
        </li>

        <li class="pb-3">
          <b> Publish dataset </b>
          <p class="text-xs">
            You will be requested to make the dataset visible on the repository
            to complete the process
          </p>
        </li>
      </ul>

      <div class="w-full flex flex-row justify-center py-6">
        <router-link to="/datasets" class="hidden">
          <el-button type="danger" plain> Cancel </el-button>
        </router-link>

        <button class="primary-button" @click="createWorkflows">
          Start curating
          <el-icon> <d-arrow-right /> </el-icon>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { useDatasetsStore } from "../../store/datasets";

export default {
  name: "CreateNewProjectConfirm",

  data() {
    return {
      datasetStore: useDatasetsStore(),
      dataset: {},
      datasetID: this.$route.params.datasetID,
    };
  },
  methods: {
    createWorkflows() {
      const dataTypes = this.dataset.dataType;

      // do some logic here to split up by workflow.

      // right now its all unique workflows.
      this.dataset.workflows = {};

      let that = this;
      dataTypes.forEach((type, index) => {
        const key = `workflow${index + 1}`;
        that.dataset.workflows[key] = {};
        that.dataset.workflows[key].type = [type];
        that.dataset.workflows[key].folderSelected = false;
        that.dataset.workflows[key].destinationSelected = false;
        that.dataset.workflows[key].datasetUploaded = false;
        that.dataset.workflows[key].datasetPublished = false;
        that.dataset.workflows[key].destination = {
          name: "",
          questions: [],
        };
        that.dataset.workflows[key].expandOptions = [];
      });

      this.dataset.workflowConfirmed = true;

      this.datasetStore.updateCurrentDataset(this.dataset);
      this.datasetStore.syncDatasets();

      this.$router.push({ path: `/datasets/${this.datasetID}` });
    },
  },
  mounted() {
    this.datasetStore.getDataset(this.datasetID);
    this.dataset = this.datasetStore.currentDataset;

    this.datasetStore.hideProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(1);
  },
};
</script>
