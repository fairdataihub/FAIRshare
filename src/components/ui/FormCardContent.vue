<template>
  <div v-if="currentStepId == stepId" :key="stepId">
    <div
      class="form-card-content mb-4 rounded-lg border-2 border-slate-100 shadow-md"
    >
      <div class="w-full bg-gray-100 px-4 py-2">
        <span
          class="text-primary-600 pointer-events-none text-lg font-semibold"
        >
          {{ stepTitle }}
        </span>
      </div>
      <div class="p-4">
        <slot> </slot>
      </div>
    </div>
    <div
      class="form-navigation-buttons flex w-full justify-center space-x-4 px-5"
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
