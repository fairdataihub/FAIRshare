<template>
  <div>
    <AppDialog
      v-if="dialogVisible"
      v-model="dialogVisible"
      :numInput="dialogNumInput"
      :headers="dialogHeaders"
      :callback="getInputs"
    ></AppDialog>
  </div>
</template>

<script>
import { useTokenStore } from "@/store/access";

import AppDialog from "@/components/dialogs/AppDialog";

import { ElNotification, ElLoading } from "element-plus";

export default {
  name: "GithubTokenConnection",

  components: { AppDialog },

  props: {
    callback: { type: Function },
  },

  data() {
    return {
      manager: useTokenStore(),
      status: ["Connect GitHub token", ""],
      dialogVisible: false,
      dialogHeaders: null,
      dialogNumInput: null,
    };
  },

  computed: {
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
      this.useAPIkey();
    },
    async getInputs(response) {
      this.dialogVisible = false;
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
      this.dialogHeaders = ["GitHub access token"];
      this.dialogVisible = true;
    },
  },

  async mounted() {
    await this.manager.loadTokens();
    this.openDialog();
  },
};
</script>
