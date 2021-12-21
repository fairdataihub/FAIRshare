<template>
  <div
    id="main-frame"
    class="h-screen w-full flex flex-row justify-center overflow-y-auto"
  >
    <div class="flex flex-col w-full items-center justify-center">
      <WorkflowProgressBar class="pt-2 max-w-screen-xl" />

      <div class="h-full w-full overflow-y-auto flex justify-center">
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
