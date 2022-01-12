<template>
  <div
    id="main-frame"
    class="flex flex-row justify-center w-full h-screen overflow-y-auto"
  >
    <div class="flex flex-col items-center justify-center w-full">
      <WorkflowProgressBar class="max-w-screen-xl pt-2" />

      <div class="flex justify-center w-full h-full overflow-y-auto">
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
