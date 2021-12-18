<template>
  <!-- <div
    class="mx-auto w-auto py-2 mb-4 px-10"
    :style="{ '--barWidth': barWidth }"
  >
    <ul class="steps">
      <li
        v-for="(step, index) in steps"
        :key="index"
        class="step"
        :class="{ active: lastActiveStep(index + 1) }"
      >
        <span class="step-number">{{ index + 1 }}</span>
        <span class="hover-content">{{ step.description }}</span>
      </li>
    </ul>
  </div> -->
  <div v-if="progressBar.show" class="w-full">
    <el-steps
      :active="progressBar.currentStep"
      align-center
      finish-status="success"
      v-if="progressBar.type === 'zenodo'"
    >
      <el-step
        v-for="step in steps"
        :key="step.description"
        :description="step.description"
      ></el-step>
    </el-steps>
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
      barWidth: "0%",
      steps: [
        {
          description: "Pick data source",
        },
        {
          description: "Provide metadata",
        },
        {
          description: "Select repository",
        },
        {
          description: "Add repository metadata",
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
  methods: {
    lastActiveStep(index) {
      if (!this.currentStep) {
        this.barWidth = "0%";
      }
      if (index <= this.currentStep) {
        const totalSteps = this.steps.length;

        const percentage = ((this.currentStep - 1) / (totalSteps - 1)) * 100;
        this.barWidth = `${percentage}%`;
        return true;
      }
      return false;
    },
  },
  async mounted() {
    this.progressBar = await this.datasetStore.getProgressBar();
  },
};
</script>

<style lang="postcss">
.el-step__description {
  @apply py-2;
}

/* ul {
  @apply sm:w-[500px] md:w-[600px] lg:w-[750px] xl:w-[900px] 2xl:w-[1200px];
  display: flex;
  align-items: center;
  justify-content: space-between;
  list-style: none;
  padding: 0px;
  position: relative;
  @apply transition-all;
}
ul::before {
  content: "";
  width: 100%;
  height: 2px;
  display: block;
  background: #e1e1e1;
  position: absolute;
  z-index: 1;
}
ul::after {
  content: "";
  height: 2px;
  display: block;
  background: #88e790;
  position: absolute;
  z-index: 2;
}

.step {
  z-index: 3;
  position: relative;
}

ul.steps::after {
  width: var(--barWidth);
}

ul li .step-number {
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #e0e0e0;
  color: #999;
  border-radius: 50px;
  border: 2px solid white;
  box-shadow: 0px 0px 5px #ccc;
  font-weight: bold;
}
ul li.active .step-number {
  background: #88e790;
  box-shadow: 0px 0px 5px #5fdb6a;
  color: white;
}

.hover-content {
  @apply opacity-0 absolute w-max text-xs text-gray-600 py-1;
  left: 50%;
  -webkit-transform: translateX(-50%);
  transform: translateX(-50%);
  z-index: 10;
}

.step:hover .hover-content {
  @apply opacity-100 transition-all;
} */
</style>
