<template>
  <div v-if="progressBar.show" class="w-full">
    <el-steps
      :active="progressBar.currentStep"
      align-center
      finish-status="success"
      v-if="progressBar.type === 'zenodo'"
      class="pt-3"
    >
      <el-step
        v-for="step in steps"
        :key="step.description"
        :description="step.description"
      ></el-step>
    </el-steps>
    <line-divider></line-divider>
  </div>
</template>

<script>
import { useDatasetsStore } from "../../store/datasets";

export default {
  name: "WorkflowProgressBar",
  props: {
    currentStep: {
      type: Number,
      default: 3,
    },
  },
  data() {
    return {
      datasetStore: useDatasetsStore(),
      progressBar: {},
      steps: [
        {
          description: "Select data files",
        },
        {
          description: "Review standards",
        },
        {
          description: "Provide metadata",
        },
        {
          description: "Select a license",
        },
        {
          description: "Select repository",
        },
        {
          description: "Upload dataset",
        },
        {
          description: "Publish dataset",
        },
        {
          description: "Register application",
        },
      ],
    };
  },
  async mounted() {
    this.progressBar = await this.datasetStore.getProgressBar();
  },
};
</script>
