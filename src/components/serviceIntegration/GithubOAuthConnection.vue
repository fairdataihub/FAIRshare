<template>
  <div class="buttonContainer">
    <el-button
      plain
      class="button"
      :type="status[1]"
      @click="connectOAuth('githubOAuth')"
      >{{ status[0] }}</el-button
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
    const status = ref(["Connect token", ""]);
    const backgroundHasResponse = ref(false);
    const spinnerGlobal = ref(null);
    return {
      status,
      backgroundHasResponse,
      spinnerGlobal,
    };
  },
  data() {
    return {
      manager: useTokenStore(),
    };
  },
  methods: {
    async connectOAuth() {
      this.manager.getGithubOAuthConnected().then((res) => {
        if (!res) {
          this.spinnerGlobal = this.createLoading();
          window.ipcRenderer.send("OAuth-Github", "test");
        } else {
          this.APIkeyWarning("githubOAuth");
        }
      });
    },

    createLoading() {
      const loading = ElLoading.service({
        lock: true,
        text: "Verifying...",
      });
      return loading;
    },

    APIkeyWarning(key) {
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
          this.deleteToken(key);
        })
        .catch(() => {
          ElNotification({
            type: "info",
            message: "Delete canceled",
            position: "bottom-right",
            duration: 2000,
          });
          this.callback();
        });
    },

    updateStatus() {
      this.manager.getGithubOAuthConnected().then((res) => {
        // console.log("current: ", res);
        if (!res) {
          this.status = ["Connect account", ""];
        } else {
          this.status = ["Disconnect account", "danger"];
        }
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
        //this.manager.confirmGithubOAuthDisconnected();
        this.callback();
      }
      this.updateStatus();
    },

    async processGithub(userInput) {
      let key = "githubOAuth";
      let value = userInput[0];
      let spinner = this.createLoading();
      let errorFound = false;
      if (await this.manager.checkGithubToken(value)) {
        let tokenObject = {};
        try {
          tokenObject.token = value;
          await this.manager.saveToken(key, tokenObject);
        } catch (e) {
          // console.log(e);
          errorFound = true;
        }
        let name = await this.manager.getGithubUser(key);
        let newTokenObject = {};
        newTokenObject.name = name;
        newTokenObject.token = value;
        // console.log("save token: ", newTokenObject);
        await this.manager.saveToken(key, newTokenObject);
        //this.manager.confirmGithubOAuthConnected();
        this.updateStatus();
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
      spinner.close();
    },
  },
  watch: {
    // whenever question changes, this function will run
    backgroundHasResponse: function () {
      // console.log("catched!");
      this.manager.getToken("githubOAuth").then((res) => {
        this.processGithub([res.token]);
        this.spinnerGlobal.close();
        this.OAuthButtonVisable = false;
        // this.manager.checkGithubToken(res.token).then((res) => {
        //   // console.log("check???: ", res);
        // });
      });
    },
  },
  async mounted() {
    //await this.manager.loadTokens();
    window.ipcRenderer.on("OAuth-Github-Reply", async (_e, _arg) => {
      if (_arg == "failed") {
        ElNotification({
          type: "error",
          message: "Login failed",
          position: "bottom-right",
          duration: 2000,
        });
        this.spinnerGlobal.close();
        this.callback();
      } else if (this.manager.checkGithubToken(_arg)) {
        // console.log("passed!");
        let tokenObject = {};
        tokenObject.token = _arg;
        await this.manager.saveToken("githubOAuth", tokenObject);
        let name = await this.manager.getGithubUser("githubOAuth");
        let newObject = {};
        newObject.token = _arg;
        newObject.name = name;
        await this.manager.saveToken("githubOAuth", newObject);
        this.backgroundHasResponse = true;
      }
    });
    await this.manager.loadTokens();
    await this.manager.loadStatus()
    this.updateStatus();
  },
};
</script>

<style scoped>
.el-button {
  padding: 0px;
  min-height: 0px;
  padding-top: 1vh;
  padding-bottom: 1vh;
  padding-left: 1vw;
  padding-right: 1vw;
}
</style>
