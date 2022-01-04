<template>
  <div class="buttonContainer">
    <!-- <el-button
      plain
      class="button"
      @click="openDialog()"
      :type="buttonStatus.buttonStyle"
      >{{ buttonStatus.buttonText }}</el-button
    > -->
    <button :class="buttonStatus.buttonStyle" @click="openDialog()">
      {{ buttonStatus.buttonText }}
    </button>
    <AppDialog
      v-if="dialogVisable"
      v-model="dialogVisable"
      :numInput="dialogNumInput"
      :headers="dialogHeaders"
      :callback="getInputs"
    ></AppDialog>
  </div>
</template>

<script>
import { useTokenStore } from "../../store/access";
import { ref } from "vue";
import { ElNotification } from "element-plus";
import { ElLoading } from "element-plus";
import { ElMessageBox } from "element-plus";
import AppDialog from "../dialogs/AppDialog";
export default {
  name: "GithubTokenConnection",
  components: { AppDialog },
  setup() {
    const status = ref(["Connect github token", ""]);
    const dialogVisable = ref(false);
    const dialogHeaders = ref(null);
    const dialogNumInput = ref(null);
    return {
      status,
      dialogVisable,
      dialogHeaders,
      dialogNumInput,
    };
  },
  data() {
    return {
      manager: useTokenStore(),
    };
  },
  computed: {
    buttonStatus() {
      let githubObject = {
        buttonText: "Connect github token",
        buttonStyle: "primary-plain-button",
      };
      if (
        "github" in this.manager.accessTokens &&
        this.manager.accessTokens.github.type == "token"
      ) {
        githubObject.buttonText = "Disconnect github token";
        githubObject.buttonStyle = "danger-plain-button";
      }
      return githubObject;
    },
    connectedToGithubByToken() {
      return (
        "github" in this.manager.accessTokens &&
        this.manager.accessTokens.github.type == "token"
      );
    },
  },
  methods: {
    createLoading() {
      const loading = ElLoading.service({
        lock: true,
        text: "Verifying...",
      });
      return loading;
    },
    openDialog() {
      if (
        "github" in this.manager.accessTokens &&
        this.manager.accessTokens.github.type == "token"
      ) {
        this.APIkeyWarning();
      } else {
        this.useAPIkey();
      }
    },
    async getInputs(response) {
      this.dialogVisable = false;
      if (response[0] == "OK") {
        await this.processGithub(response[1]);
      } else {
        ElNotification({
          type: "info",
          message: "Input canceled",
          position: "bottom-right",
          duration: 2000,
        });
      }
    },

    async processGithub(userInput) {
      let key = "github";
      let value = userInput[0];
      let spinner = this.createLoading();
      let errorFound = false;
      if (await this.manager.verifyGithubToken(value)) {
        let tokenObject = {};
        let name = await this.manager.getGithubUser(value);
        try {
          tokenObject.token = value;
          tokenObject.name = name;
          tokenObject.type = "token";
          await this.manager.saveToken(key, tokenObject);
        } catch (e) {
          errorFound = true;
        }
        if (!errorFound) {
          ElNotification({
            type: "success",
            message: "Saved successfully",
            position: "bottom-right",
            duration: 2000,
          });
        }
      } else {
        ElNotification({
          type: "error",
          message: "Cannot verify the token provided",
          position: "bottom-right",
          duration: 2000,
        });
      }
      spinner.close();
    },

    useAPIkey() {
      this.dialogNumInput = 1;
      this.dialogHeaders = ["Github access token"];
      this.dialogVisable = true;
    },

    APIkeyWarning() {
      ElMessageBox.confirm(
        "Disconnecting will delete the access token stored. Continue?",
        "Warning",
        {
          confirmButtonText: "OK",
          cancelButtonText: "Cancel",
          type: "warning",
        }
      )
        .then(async () => {
          this.deleteToken("github");
        })
        .catch(() => {
          ElNotification({
            type: "info",
            message: "Delete canceled",
            position: "bottom-right",
            duration: 2000,
          });
        });
    },

    async deleteToken(key) {
      let errorFound = false;
      try {
        await this.manager.deleteToken(key);
      } catch (e) {
        errorFound = true;
      }
      if (!errorFound) {
        ElNotification({
          type: "success",
          message: "Deleted",
          position: "bottom-right",
          duration: 2000,
        });
      }
    },
  },
  async mounted() {
    await this.manager.loadTokens();
  },
};
</script>
