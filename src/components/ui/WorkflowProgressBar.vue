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
        v-for="step in zenodoSteps"
        :key="step.description"
        :description="step.description"
      ></el-step>
    </el-steps>

    <el-steps
      :active="progressBar.currentStep"
      align-center
      finish-status="success"
      v-if="progressBar.type === 'geo'"
      class="pt-3"
    >
      <el-step
        v-for="step in nihGeoSteps"
        :key="step.description"
        :description="step.description"
      ></el-step>
    </el-steps>

    <el-steps
      :active="progressBar.currentStep"
      align-center
      finish-status="success"
      v-if="progressBar.type === 'immport'"
      class="pt-3"
    >
      <el-step
        v-for="step in immportSteps"
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
      zenodoSteps: [
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
      nihGeoSteps: [
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
          description: "Select repository",
        },
        {
          description: "Generate dataset",
        },
        {
          description: "Upload dataset",
        },
      ],
      immportSteps: [
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
          description: "Generate dataset",
        },
        {
          description: "Upload dataset",
        },
        {
          description: "Publish dataset",
        },
      ],
    };
  },
  async mounted() {
    this.progressBar = await this.datasetStore.getProgressBar();
  },
};
</script>
