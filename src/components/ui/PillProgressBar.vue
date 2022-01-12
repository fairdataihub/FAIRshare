<template>
  <div class="flex items-stretch w-9/12 max-w-screen-md gap-2 mx-auto">
    <div
      v-for="step in totalSteps"
      :key="step"
      class="h-[7px] w-full rounded text-secondary-500 transition-all cursor-pointer hover:bg-secondary-400 relative group"
      style="border: 1px solid"
      :class="{ 'bg-secondary-500 ': step <= currentStep }"
      @click="setCurrentStep(step)"
    >
      <span
        class="absolute hidden w-full px-2 pt-3 text-xs text-center text-gray-400"
      >
        {{ titles[step - 1] }}
      </span>
      <!-- Add this if we want to show title on active step 
      :class="{ hidden: step !== currentStep }" -->
    </div>
  </div>
</template>

<script>
export default {
  name: "PillProgressBar",
  props: {
    totalSteps: {
      type: Number,
      default: 3,
    },
    currentStep: {
      type: Number,
      default: 1,
    },
    titles: {
      type: Array,
      default: () => [],
    },
  },
  emits: ["updateCurrentStep"],
  data() {
    return {};
  },
  methods: {
    setCurrentStep(step) {
      this.$emit("updateCurrentStep", step);
    },
  },
  async mounted() {},
};
</script>

<style lang="postcss" scoped></style>
