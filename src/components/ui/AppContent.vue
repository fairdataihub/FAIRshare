<template>
  <div
    id="main-frame"
    class="h-screen w-full flex flex-row justify-center overflow-y-auto"
  >
    <div class="flex flex-col w-full">
      <WorkflowProgressBar class="pt-2" />

      <div class="h-full w-full overflow-y-auto">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script>
import WorkflowProgressBar from "./WorkflowProgressBar.vue";

export default {
  name: "AppContent",
  components: {
    WorkflowProgressBar,
  },
  data() {
    return {};
  },
  mounted() {},
};
</script>

<style>
.el-step {
  @apply flex flex-row items-center justify-center;
}
</style>
