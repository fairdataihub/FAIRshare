<template>
  <transition name="fade" mode="out-in">
    <div v-if="currentStepId == stepId">
      <div class="form-card-content">
        <slot> </slot>
      </div>
      <div class="form-navigation-buttons w-full flex justify-end px-5">
        <el-button @click="prevStep" :disabled="prevDisabled">
          Previous
        </el-button>
        <el-button @click="nextStep"> Next </el-button>
      </div>
    </div>
  </transition>
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
  },
  data() {
    return {};
  },
  computed: {
    prevDisabled() {
      return this.currentStepId === 1;
    },
  },
  methods: {},
  async mounted() {
    console.log(this.currentStepId);
  },
};
</script>

<style></style>
