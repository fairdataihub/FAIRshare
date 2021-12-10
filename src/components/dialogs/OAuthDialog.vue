<template>
  <el-dialog
    width="400px"
    destroy-on-close
    :before-close="beforeCloseRootLevel"
  >
    <div class="dialog-Container">
      <el-button @click="connect('apple')">test</el-button>
    </div>
  </el-dialog>
</template>

<script>
export default {
  setup() {},
  methods: {
    connect(s) {
      window.ipcRenderer.send("OAuth-Github", s);
    },
  },
};
</script>

<style scoped>
.el-button--text {
  font-size: 15px;
}

.dialog-Container {
  height: 80vh;
  display: flex;
  flex-direction: column;
  gap: 15px;
}
.inputField {
  display: flex;
  flex-direction: column;
}
.inputBar-Header {
  font-size: 13.5px;
  padding-left: 3px;
  box-sizing: border-box;
}
.inputBar {
  width: 100%;
}
.bottom {
  padding-top: 5px;
  box-sizing: border-box;
  display: flex;
  align-items: flex-end;
  justify-content: flex-end;
}
</style>

<style>
.el-overlay-dialog {
  display: flex;
  align-items: center;
  justify-content: center;
}

.el-dialog {
  margin: 0 !important;
}

.el-dialog__header {
  padding: 0 !important;
}
</style>
