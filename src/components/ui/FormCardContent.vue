<template>
  <!-- <transition name="lightfadeleft"> -->
  <div v-if="currentStepId == stepId">
    <div class="form-card-content">
      <slot> </slot>
    </div>
    <div class="form-navigation-buttons w-full flex justify-end px-5">
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
      <el-button
        @click="nextStep"
        type="primary"
        :plain="!lastStep"
        size="medium"
        :disabled="checkInvalidStatus"
      >
        {{ nextText }}
        <el-icon v-if="lastStep"><d-arrow-right /></el-icon>
        <el-icon v-else><right /></el-icon>
      </el-button>
    </div>
  </div>
  <!-- </transition> -->
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
  async mounted() {
    console.log(this.lastStep);
  },
};
</script>

<style></style>
