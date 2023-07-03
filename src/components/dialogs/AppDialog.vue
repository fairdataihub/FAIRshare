<template>
  <el-dialog
    width="450px"
    destroy-on-close
    title="Enter token information"
    :before-close="beforeCloseRootLevel"
  >
    <div class="dialog-Container">
      <p class="pb-2 text-sm" v-if="headers[0].search('Zenodo') !== -1">
        You will need the
        <span class="font-semibold">deposit:actions</span>
        and <span class="font-semibold">deposit:write</span> scopes <br />
        to access this resource.
      </p>
      <p class="pb-2 text-sm" v-if="headers[0].search('GitHub') !== -1">
        You will need the following scopes on your personal access <br />
        token:
        <span class="font-semibold">admin:org_hook</span>,
        <span class="font-semibold">admin:repo_hook</span>, <span class="font-semibold">repo</span>,
        <span class="font-semibold">user</span>
      </p>
      <el-form ref="formRef" :model="userInputs" label-position="top">
        <div class="inputField" v-for="i in this.numInput" :key="i">
          <el-form-item :label="this.headers[i - 1]" :prop="this.headers[i - 1]" required>
            <el-input class="inputBar" size="large" v-model="userInputs[this.headers[i - 1]]" />
          </el-form-item>
        </div>
        <div
          class="hover-underline-animation my-3 flex w-max cursor-pointer flex-row items-center text-primary-600"
          @click="openWebsite(this.headers[0])"
        >
          <span class="font-medium">
            How to generate a {{ this.headers[0].split(" ")[0] }} personal access token?
          </span>
          <Icon icon="grommet-icons:form-next-link" class="ml-2 h-5 w-5" />
        </div>
        <el-form-item>
          <div class="bottom gap-[5px]">
            <button class="danger-plain-button h-9" @click="closeDialog('Cancelled')">
              Cancel
            </button>
            <button class="primary-button h-9" @click="confirmInput('formRef')">OK</button>
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
    // user inputs. in the order of from top to the bottom
    const userInputs = ref({});
    for (let i = 0; i < props.numInput; i++) {
      userInputs.value[props.headers[i]] = "";
    }

    return {
      userInputs,
    };
  },
  methods: {
    openWebsite(header) {
      if (header == "GitHub access token") {
        window.ipcRenderer.send(
          "open-link-in-browser",
          "https://docs.fairshareapp.io/docs/manage-accounts/connect-to-github"
        );
      } else if (header == "Zenodo token") {
        window.ipcRenderer.send(
          "open-link-in-browser",
          "https://docs.fairshareapp.io/docs/manage-accounts/connect-to-zenodo"
        );
      }
    },
    // return inputs as an array (values only, in the order of from top to the bottom)
    async closeDialog(status) {
      await this.callback([status, Object.values(this.userInputs)]);
      this.clearInput();
    },
    // validate and cleaning
    async confirmInput(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.closeDialog("OK");
        }
      });
    },
    // close by clicking "x"
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

<style scoped lang="css">
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
  @apply box-border pl-3 text-base;
}
.inputBar {
  @apply w-full;
}
.bottom {
  @apply box-border flex items-end justify-end pt-3;
}
</style>
