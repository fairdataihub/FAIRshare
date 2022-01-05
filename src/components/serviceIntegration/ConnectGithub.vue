<template>
  <div>
    <button
      :class="githubDetails.buttonStyle"
      @click="interactWithService('github')"
    >
      {{ githubDetails.action }}
    </button>
    <ButtonInputDialog
      v-model="dialogVisable"
      :numInput="dialogNumInput"
      :buttons="this.buttonList"
      :callback="closeButtonDialog"
    ></ButtonInputDialog>
  </div>
</template>

<script>
/* eslint-disable vue/no-unused-components */
import GithubTokenConnection from "@/components/serviceIntegration/GithubTokenConnection";
import GithubOAuthConnection from "@/components/serviceIntegration/GithubOAuthConnection";
import ButtonInputDialog from "@/components/dialogs/ButtonInputDialog";
import { useTokenStore } from "@/store/access";
import { markRaw } from "vue";
import { ElNotification, ElMessageBox } from "element-plus";
export default {
  name: "ConnectGithub",
  components: {
    GithubTokenConnection: GithubTokenConnection,
    GithubOAuthConnection: GithubOAuthConnection,
    ButtonInputDialog,
  },
  setup() {
    const manager = useTokenStore();
    return {
      manager,
    };
  },
  data() {
    return {
      buttonList: [],
      dialogVisable: false,
      dialogNumInput: 0,
    };
  },
  methods: {
    closeButtonDialog() {
      this.dialogVisable = false;
      this.buttonList = [];
      this.dialogNumInput = 0;
    },
    interactWithService(serviceName) {
      if (serviceName == "github") {
        if ("github" in this.manager.accessTokens) {
          this.APIkeyWarning("github");
        } else {
          this.buttonList = [
            markRaw(GithubTokenConnection),
            markRaw(GithubOAuthConnection),
          ];
          this.dialogNumInput = 2;
          this.dialogVisable = true;
        }
      }
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
  computed: {
    githubDetails() {
      let githubObject = {
        status: "Not Connected",
        name: "",
        action: "Connect",
        buttonStyle: "primary-plain-button",
      };
      if ("github" in this.manager.accessTokens) {
        githubObject.status = "Connected";
        githubObject.name = this.manager.accessTokens.github.name;
        githubObject.action = "Disconnect";
        githubObject.buttonStyle = "danger-plain-button";
      }
      return githubObject;
    },
  },
};
</script>