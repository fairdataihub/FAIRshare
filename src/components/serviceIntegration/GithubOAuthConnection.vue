<template>
  <div></div>
</template>

<script>
import { useTokenStore } from "../../store/access";

import { ElNotification, ElLoading } from "element-plus";

export default {
  name: "GithubOAuthConnection",
  props: {
    callback: { type: Function },
  },
  data() {
    return {
      manager: useTokenStore(),
      backgroundHasResponse: false,
      spinnerGlobal: null,
    };
  },
  computed: {
    buttonStatus() {
      let githubObject = {
        buttonText: "Connect github account",
        buttonStyle: "primary-plain-button",
      };
      if (
        "github" in this.manager.accessTokens &&
        this.manager.accessTokens.github.type == "OAuth"
      ) {
        githubObject.buttonText = "Disconnect github account";
        githubObject.buttonStyle = "danger-plain-button";
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
          this.callback();
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
            this.callback();
          }
        } else {
          ElNotification({
            type: "error",
            message: "Cannot verify the token provided",
            position: "bottom-right",
            duration: 2000,
          });
          this.callback();
        }
        this.spinnerGlobal.close();
      });
    },

    createLoading() {
      const loading = ElLoading.service({
        lock: true,
        text: "Verifying...",
      });
      return loading;
    },
  },
  async mounted() {
    //await this.manager.loadTokens();
    await this.manager.loadTokens();
    this.connectOAuth();
  },
};
</script>
