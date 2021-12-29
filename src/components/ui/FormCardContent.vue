<template>
  <div v-if="currentStepId == stepId" :key="stepId">
    <div
      class="form-card-content border-2 border-slate-100 rounded-lg mb-4 shadow-md"
    >
      <div class="w-full bg-gray-100 px-4 py-2">
        <span
          class="font-semibold text-primary-600 text-lg pointer-events-none"
        >
          {{ stepTitle }}
        </span>
      </div>
      <div class="p-4">
        <slot> </slot>
      </div>
    </div>
    <div class="form-navigation-buttons w-full flex justify-end px-5 space-x-4">
      <el-button
        @click="prevStep"
        :type="prevType"
        plain
        size="medium"
        :disabled="checkInvalidStatus"
      >
        <el-icon v-if="!firstStep"><back /></el-icon>
        <el-icon v-else><d-arrow-left /></el-icon> {{ prevText }}
      </el-button>
      <!-- :plain="!lastStep" -->
      <button
        class="primary-button"
        @click="nextStep"
        :disabled="checkInvalidStatus"
      >
        {{ nextText }}
        <el-icon v-if="lastStep"><d-arrow-right /></el-icon>
        <el-icon v-else><right /></el-icon>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "FormCardContent",
  props: {
    stepId: {
      type: Number,
      default: 1,
      required: true,
    },
    currentStepId: {
      type: Number,
    },
    nextStep: {
      type: Function,
    },
    prevStep: {
      type: Function,
    },
    validityCheck: {
      type: Object,
      default: () => {},
    },
    lastStep: {
      type: Boolean,
      default: false,
    },
    stepTitle: {
      type: String,
      default: "",
    },
  },
  data() {
    return {};
  },
  computed: {
    firstStep() {
      return this.currentStepId === 1;
    },
    nextText() {
      return this.lastStep ? "Next" : "Continue";
    },
    prevText() {
      if (this.currentStepId === 1) {
        return "Back";
      } else {
        return "Previous";
      }
    },
    prevType() {
      if (this.currentStepId === 1) {
        return "danger";
      } else {
        return "info";
      }
    },
    checkInvalidStatus() {
      for (const key in this.validityCheck) {
        if (this.validityCheck[key]) {
          return true;
        }
      }
      return false;
    },
  },
  methods: {},
  async mounted() {},
};
</script>
