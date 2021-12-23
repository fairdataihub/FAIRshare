<template>
  <el-dialog
    width="600px"
    destroy-on-close
    :before-close="beforeCloseRootLevel"
  >
    <div class="dialog-Container">
      <div class="inputField">
        <div v-for="i in this.numInput" :key="i">
          <component v-bind:is="buttons[i - 1]"> </component>
        </div>
      </div>
    </div>
  </el-dialog>
</template>

<script>
export default {
  props: {
    numInput: { type: Number },
    buttons: { type: Array },
    callback: { type: Function },
  },
  setup() {},
  methods: {
    async closeDialog(status) {
      await this.callback([status]);
    },

    async beforeCloseRootLevel() {
      this.closeDialog("Cancelled");
    },
  },
};
</script>

<style scoped>
.el-button--text {
  @apply text-base;
}

.dialog-Container {
  @apply flex flex-col justify-center items-center gap-3 h-32;
}
.inputField {
  @apply flex gap-6;
}
.inputBar-Header {
  @apply text-base pl-3 box-border;
}
.inputBar {
  @apply w-full;
}
.bottom {
  @apply pt-3 box-border flex items-end justify-end;
}
</style>
