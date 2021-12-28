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
        <el-button class="button" size="small" @click="confirmInput"
          >OK</el-button
        >
      </div>
    </div>
  </el-dialog>
</template>

<script>
import { ref } from "vue";
export default {
  props: {
    numInput: { type: Number },
    headers: { type: Array },
    callback: { type: Function },
  },
  setup(props) {
    const userInputs = ref([]);
    for (let i = 0; i < props.numInput - 1; i++) {
      userInputs.value.push("");
    }
    //console.log("user inputs: ", userInputs);
    return {
      userInputs,
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
  @apply text-base;
}

.dialog-Container {
  @apply flex flex-col gap-3;
}
.inputField {
  @apply flex flex-col;
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
