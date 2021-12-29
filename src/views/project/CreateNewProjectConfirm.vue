<template>
  <div
    class="h-full w-full flex flex-col justify-center items-center p-3 px-5 max-w-screen-xl"
  >
    <div class="flex flex-col h-full w-full" id="scroll">
      <span class="font-medium text-left"> FAIRifying </span>

      <span> Let's make your research software FAIR. </span>

      <line-divider> </line-divider>

      <p class="py-2">
        In order to do this, SODA will automatically try to group up similar
        data into their own datasets.
      </p>
      <!-- <p class="py-2">
        FAIRShare will help you make you research software by guiding you
        step-by-step through the following process:
      </p> -->

      <div class="w-full flex flex-row justify-center py-6" id="button-area">
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

      this.$router.push({ path: `/datasets/${this.datasetID}/landing` });
    },
  },
  async mounted() {
    this.datasetStore.getDataset(this.datasetID);
    this.dataset = this.datasetStore.currentDataset;

    this.datasetStore.hideProgressBar();
    this.datasetStore.setProgressBarType("zenodo");
    this.datasetStore.setCurrentStep(1);
  },
};
</script>

<style scoped>
#step1,
#step2,
#step3,
#step4,
#step5,
#step6 {
  animation-name: card-animation;
  animation-duration: 2s;
}
@keyframes card-animation {
  from {
    opacity: 0;
    transform: scale(0.5, 0.5);
  }
  to {
    opacity: 1;
    transform: scale(1, 1);
  }
}

#button-area {
  animation-name: button-animation;
  animation-duration: 1.5s;
}

@keyframes button-animation {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>
