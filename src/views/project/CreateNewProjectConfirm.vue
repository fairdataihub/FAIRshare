<template>
  <div class="flex h-full w-full max-w-screen-xl flex-col items-center justify-center p-3 px-5">
    <div class="flex h-full w-full flex-col" id="scroll">
      <span class="text-left font-medium"> FAIRifying </span>

      <span> Let's make your research software FAIR </span>

      <line-divider> </line-divider>

      <div class="flex h-full flex-col items-center justify-center">
        <Vue3Lottie
          animationLink="https://assets6.lottiefiles.com/packages/lf20_qqtavvc0.json"
          :width="200"
          :height="200"
        />

        <div class="flex w-full flex-row justify-center py-6" id="button-area">
          <router-link to="/datasets" class="hidden">
            <el-button type="danger" plain> Cancel </el-button>
          </router-link>

          <button class="primary-button" @click="createWorkflows">
            Let's start curating
            <el-icon> <d-arrow-right /> </el-icon>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useDatasetsStore } from "@/store/datasets";

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
        that.dataset.workflows[key].sourceSelected = false;
        that.dataset.workflows[key].source = {};
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
