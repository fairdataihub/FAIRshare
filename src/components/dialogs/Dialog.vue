<template>
  <el-dialog width="400px">
    <div class="dialog-Container">

      <div class="inputField">
        <div class="inputBar-Header">Password</div>
        <el-input class="inputBar" size="large" v-model="input2" />
      </div>

      <div class="inputField">
        <div class="inputBar-Header">Password</div>
        <el-input class="inputBar" size="large" v-model="input2" />
      </div>


      <div class="bottom">
        <el-button class="button" size="small" @click="closeDialogFromParent">Cancel</el-button>
        <el-button class="button" size="small" type="primary" @click="closeDialogFromParent">OK</el-button>
      </div>
    </div>
  </el-dialog>
</template>

<script>
import { ref } from 'vue'
export default {
  props: {
    callback: { type: Function },
    numInput: { type: Number},
    headers: { type: Array }
  },
  setup() {
    return {
      userInputs: ref([])
    }
  },
  methods: {
    async closeDialogFromParent() {
      await this.callback()
      return this.userInputs
    },
  },
};
</script>

<style scoped>
.el-button--text {
  font-size: 15px;
}

.dialog-Container{
    display: flex;
    flex-direction: column;
    gap: 15px;
}
.inputField {
  display: flex;
  flex-direction: column;
}
.inputBar-Header{
    font-size: 13.5px;
    padding-left: 3px;
    box-sizing: border-box;
}
.inputBar{
    width: 100%;
}
.bottom{
    padding-top: 5px;
    box-sizing: border-box;
    display: flex;
    align-items: flex-end;
    justify-content: flex-end;
}
</style>

<style>
.el-overlay-dialog{
  display: flex;
  align-items: center;
  justify-content: center;
}

.el-dialog{
  margin: 0 !important;
}

.el-dialog__header{
  padding: 0 !important;
}
</style>