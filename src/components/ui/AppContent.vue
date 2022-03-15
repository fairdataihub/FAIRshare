<template>
  <div id="main-frame" class="flex h-screen w-full flex-row justify-center overflow-y-auto">
    <div class="flex w-full flex-col items-center justify-center">
      <WorkflowProgressBar class="max-w-screen-xl pt-2" />

      <div class="flex h-full w-full justify-center overflow-y-auto">
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
