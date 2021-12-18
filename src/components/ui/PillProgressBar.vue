<template>
  <div class="flex items-stretch gap-2">
    <div
      v-for="step in totalSteps"
      :key="step"
      class="h-2 w-full rounded text-purple-500"
      style="border: 1px solid"
      :class="{ 'bg-purple-500 ': step <= currentStep }"
    ></div>
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
  },
  data() {
    return {};
  },
  methods: {},
  async mounted() {},
};
</script>

<style lang="postcss" scoped></style>
