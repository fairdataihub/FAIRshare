<template>
  <el-dialog
    width="400px"
    destroy-on-close
    :before-close="beforeCloseRootLevel"
  >
    <div class="dialog-Container">
      <div class="inputField" v-for="i in this.numInput" :key="i">
        <div class="inputBar-Header">{{ this.headers[i - 1] }}</div>
        <el-input class="inputBar" size="large" v-model="userInputs[i - 1]" />
      </div>

      <div class="bottom">
        <el-button class="button" size="small" @click="closeDialog('Cancelled')"
          >Cancel</el-button
        >
        <el-button
          class="button"
          size="small"
          type="primary"
          @click="confirmInput"
          >OK</el-button
        >
      </div>
    </div>
  </el-dialog>
</template>

<script>
import { ref } from "vue";
export default {
  name: "AppDialog",
  props: {
    numInput: { type: Number },
    headers: { type: Array },
    callback: { type: Function },
  },
  setup(props) {
    const userInputs = ref([]);
    const dialogVisable = ref(false);
    for (let i = 0; i < props.numInput - 1; i++) {
      userInputs.value.push("");
    }
    //console.log("user inputs: ", userInputs);
    return {
      userInputs,
      dialogVisable,
    };
  },
  methods: {
    async closeDialog(status) {
      await this.callback([status, this.userInputs]);
      this.clearInput();
    },

    async confirmInput() {
      this.closeDialog("OK");
    },

    async beforeCloseRootLevel() {
      this.closeDialog("Cancelled");
    },

    clearInput() {
      for (let i = 0; i < this.userInputs.length; i++) {
        this.userInputs[i] = "";
      }
    },
  },
};
</script>

<style scoped>
.el-button--text {
  font-size: 15px;
}

.dialog-Container {
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
