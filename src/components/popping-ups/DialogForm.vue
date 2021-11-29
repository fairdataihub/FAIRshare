<template>
  <el-dialog title="Shipping address">
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="closeDialogFromParent">Cancel</el-button>
        <el-button type="primary" @click="closeDialogFromParent"
          >Confirm</el-button
        >
      </span>
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
