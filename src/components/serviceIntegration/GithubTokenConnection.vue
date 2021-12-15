<template>
  <div class="buttonContainer">
    <el-button
      plain
      :type="status[1]"
      class="button"
      @click="openDialog('githubToken')"
      >{{ status[0] }}</el-button
    >
    <Dialog
      v-model="dialogVisable"
      :numInput="dialogNumInput"
      :headers="dialogHeaders"
      :callback="getInputs"
    ></Dialog>
  </div>
</template>

<script>
import { useTokenStore } from "../../store/access";
import { ref } from "vue";
import { ElNotification } from "element-plus";
import { ElLoading } from "element-plus";
import { ElMessageBox } from "element-plus";
import Dialog from "../dialogs/Dialog";
export default {
  name: "GithubTokenConnection",
  components: { Dialog },
  props: {
    callback: { type: Function },
  },
  setup() {
    const status = ref(["Connect token", ""]);
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
  methods: {
    createLoading() {
      const loading = ElLoading.service({
        lock: true,
        text: "Verifying...",
      });
      return loading;
    },
    openDialog(s) {
      // Show the dialog to get the token
      // verifyToken(token)     // this function should be defined in the store
      // Add token to store
      // set githubConnected in store to true
      //when its ready the ouath items can also be added to here
      this.manager.getGithubTokenConnected().then((res) => {
        if (!res) {
          // console.log("!!");
          this.useAPIkey();
        } else {
          this.APIkeyWarning(s);
        }
      });
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
        this.callback();
      }
    },

    async processGithub(userInput) {
      let key = "githubToken";
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
        this.manager.confirmGithubTokenConnected();
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

    useAPIkey() {
      this.dialogNumInput = 1;
      this.dialogHeaders = ["Github access token"];
      this.dialogVisable = true;
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
      this.manager.getGithubTokenConnected().then((res) => {
        // console.log("current: ", res);
        if (!res) {
          this.status = ["Connect token", ""];
        } else {
          this.status = ["Disconnect token", "danger"];
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
        this.manager.confirmGithubTokenDisconnected();
        this.callback();
      }
      this.updateStatus();
    },
  },
  async mounted() {
    //await this.manager.loadTokens();
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
