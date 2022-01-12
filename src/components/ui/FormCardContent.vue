<template>
  <div v-if="currentStepId == stepId" :key="stepId">
    <div
      class="mb-4 border-2 rounded-lg shadow-md form-card-content border-slate-100"
    >
      <div class="w-full px-4 py-2 bg-gray-100">
        <span
          class="text-lg font-semibold pointer-events-none text-primary-600"
        >
          {{ stepTitle }}
        </span>
      </div>
      <div class="p-4">
        <slot> </slot>
      </div>
    </div>
    <div
      class="flex justify-center w-full px-5 space-x-4 form-navigation-buttons"
    >
      <button
        @click="prevStep"
        :class="
          this.currentStepId === 1
            ? 'primary-plain-button'
            : 'secondary-plain-button'
        "
        size="medium"
        :disabled="checkInvalidStatus"
      >
        <el-icon v-if="!firstStep"><back-icon /></el-icon>
        <el-icon v-else><d-arrow-left /></el-icon> {{ prevText }}
      </button>
      <!-- :plain="!lastStep" -->
      <button
        class="primary-button"
        @click="nextStep"
        :disabled="checkInvalidStatus"
      >
        {{ nextText }}
        <el-icon v-if="lastStep"><d-arrow-right /></el-icon>
        <el-icon v-else><right-icon /></el-icon>
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
      return this.lastStep ? "Continue" : "Next";
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
