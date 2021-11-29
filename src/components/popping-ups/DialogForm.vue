<template>
  <el-dialog title="Please provide">
    <template #footer>
      <el-button type="text" class="button" @click="closeDialogFromParent"
        >SAVE</el-button
      >
    </template>
  </el-dialog>
</template>

<script>
// import { reactive, toRefs } from "vue";

export default {
  props: {
    callback: { type: Function },
  },
  setup() {},
  methods: {
    closeDialogFromParent() {
      this.callback();
    },
  },
};
</script>

<style scoped>
.el-button--text {
  font-size: 2vmin;
}
</style>
