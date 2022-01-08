<template>
  <div></div>
</template>

<script>
import { useTokenStore } from "../../store/access";
import { ElNotification, ElLoading } from "element-plus";

export default {
  // empty component, only has functionalities
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
  methods: {
    // connect with backend to call a window for getting the github username/password
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
    // spinner function
    createLoading() {
      const loading = ElLoading.service({
        lock: true,
        text: "Verifying...",
      });
      return loading;
    },
  },
  async mounted() {
    // when the empty div was mounted, call the connection function immediately
    await this.manager.loadTokens();
    this.connectOAuth();
  },
};
</script>
