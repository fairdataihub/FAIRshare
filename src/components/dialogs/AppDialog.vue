<template>
  <el-dialog
    width="450px"
    destroy-on-close
    title="Enter token information"
    :before-close="beforeCloseRootLevel"
  >
    <div class="dialog-Container">
      <!-- <div class="inputField" v-for="i in this.numInput" :key="i">
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
      </div> -->
      <el-form ref="formRef" :model="userInputs" label-position="top">
        <div class="inputField" v-for="i in this.numInput" :key="i">
          <el-form-item
            :label="this.headers[i - 1]"
            :prop="this.headers[i - 1]"
            required
          >
            <el-input
              class="inputBar"
              size="large"
              v-model="userInputs[this.headers[i - 1]]"
            />
          </el-form-item>
        </div>
        <div
          class="flex flex-row items-center w-max text-primary-500 cursor-pointer hover-underline-animation my-3"
          @click="openWebsite(this.headers[0])"
        >
          <span class="font-medium">
            How to generate a {{ this.headers[0].split(" ")[0] }} personal
            access token?
          </span>
          <Icon icon="grommet-icons:form-next-link" class="ml-2 h-5 w-5" />
        </div>
        <el-form-item>
          <div class="bottom gap-[5px]">
            <button
              class="danger-plain-button h-8"
              @click="closeDialog('Cancelled')"
            >
              Cancel
            </button>
            <button class="primary-button h-8" @click="confirmInput('formRef')">
              OK
            </button>
          </div>
        </el-form-item>
      </el-form>
    </div>
  </el-dialog>
</template>

<script>
import { ref } from "vue";
import { Icon } from "@iconify/vue";
export default {
  components: { Icon },
  props: {
    numInput: { type: Number },
    headers: { type: Array },
    callback: { type: Function },
  },
  setup(props) {
    const userInputs = ref({});
    for (let i = 0; i < props.numInput; i++) {
      let key = props.headers[i];
      userInputs.value[key] = "";
    }
    console.log("user inputs: ", userInputs.value);
    return {
      userInputs,
    };
  },
  methods: {
    openWebsite(header) {
      if (header == "GitHub access token") {
        window.ipcRenderer.send(
          "open-link-in-browser",
          "https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token"
        );
      } else if (header == "Zenodo access token") {
        window.ipcRenderer.send(
          "open-link-in-browser",
          "https://developers.zenodo.org/"
        );
      }
    },
    async closeDialog(status) {
      await this.callback([status, Object.values(this.userInputs)]);
      this.clearInput();
    },

    async confirmInput(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          console.log("user inputs: ", this.userInputs);
          this.closeDialog("OK");
        }
      });
    },

    async beforeCloseRootLevel() {
      this.closeDialog("Cancelled");
    },

    clearInput() {
      Object.keys(this.userInputs).forEach((key) => {
        this.userInputs[key] = "";
      });
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
