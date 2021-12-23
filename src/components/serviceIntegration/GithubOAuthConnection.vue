<template>
  <div class="buttonContainer">
    <el-button
      plain
      class="button"
      @click="connectOAuth()"
      :type="buttonStatus.buttonStyle"
      >{{ buttonStatus.buttonText }}</el-button
    >
  </div>
</template>

<script>
import { useTokenStore } from "../../store/access";
import { ref } from "vue";
import { ElNotification } from "element-plus";
import { ElLoading } from "element-plus";
import { ElMessageBox } from "element-plus";
export default {
  name: "GithubOAuthConnection",
  props: {
    callback: { type: Function },
  },
  setup() {
    const backgroundHasResponse = ref(false);
    const spinnerGlobal = ref(null);
    return {
      backgroundHasResponse,
      spinnerGlobal,
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
        buttonText: "Connect github account",
        buttonStyle: "",
      };
      if (
        "github" in this.manager.accessTokens &&
        this.manager.accessTokens.github.type == "OAuth"
      ) {
        githubObject.buttonText = "Disconnect github account";
        githubObject.buttonStyle = "danger";
      }
      return githubObject;
    },
    connectedToGithubByOAuth() {
      return (
        "github" in this.manager.accessTokens &&
        this.manager.accessTokens.github.type == "OAuth"
      );
    },
  },
  methods: {
    async connectOAuth() {
      if (
        "github" in this.manager.accessTokens &&
        this.manager.accessTokens.github.type == "OAuth"
      ) {
        this.APIkeyWarning();
      } else {
        this.spinnerGlobal = this.createLoading();
        window.ipcRenderer.send("OAuth-Github", "test");
        window.ipcRenderer.once("OAuth-Github-Reply", async (_e, _arg) => {
          if (_arg == "failed") {
            ElNotification({
              type: "error",
              message: "Login failed",
              position: "bottom-right",
              duration: 2000,
            });
          } else if (this.manager.verifyGithubToken(_arg)) {
            let key = "github";
            let errorFound = false;
            let name = await this.manager.getGithubUser(_arg);
            let tokenObject = {};
            try {
              tokenObject.token = _arg;
              tokenObject.name = name;
              tokenObject.type = "OAuth";
              await this.manager.saveToken(key, tokenObject);
            } catch (e) {
              errorFound = true;
            }
            await this.manager.saveToken("github", tokenObject);
            this.backgroundHasResponse = true;
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
          this.spinnerGlobal.close();
        });
      }
    },

    createLoading() {
      const loading = ElLoading.service({
        lock: true,
        text: "Verifying...",
      });
      return loading;
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
    //await this.manager.loadTokens();
    await this.manager.loadTokens();
  },
};
</script>
