<template>
  <div>
    <!-- <el-popover
      placement="bottom"
      :hide-after="0"
      trigger="hover"
      content="Coming soon..."
    >
      <template #reference> -->
    <div>
      <button @click="interactWithService('github')" :class="githubDetails.buttonStyle">
        {{ githubDetails.action }}
      </button>
    </div>
    <!-- </template>
    </el-popover> -->
    <el-dialog
      width="600px"
      title="Select an option to connect to GitHub"
      destroy-on-close
      v-model="dialogVisible"
    >
      <div class="dialog-Container">
        <div class="inputField">
          <button class="primary-plain-button w-52" @click="showGithubTokenConnect">
            Connect with token
          </button>
          <button class="primary-plain-button w-52" @click="showGithubOAuthConnect">
            Connect with username
          </button>
        </div>
      </div>
      <p class="break-normal text-center text-sm text-gray-500">
        To learn more about the permissions required by FAIRshare from your GitHub account
        <span
          class="text-url"
          @click="
            openWebsite(
              'https://docs.fairshareapp.io/docs/manage-accounts/connect-to-github#scopes'
            )
          "
        >
          visit our documentation.
        </span>
      </p>
    </el-dialog>
    <GithubTokenConnection
      v-if="showTokenConnect"
      v-model="showTokenConnect"
      :callback="hideGithubTokenConnect"
      :onStatusChange="statusChangeFunction"
    ></GithubTokenConnection>
    <GithubOAuthConnection
      v-if="showOAuthConnect"
      v-model="showOAuthConnect"
      :callback="hideGithubOAuthConnect"
      :onStatusChange="statusChangeFunction"
    ></GithubOAuthConnection>
    <warning-confirm ref="warningConfirm" title="Warning" @messageConfirmed="confirmDeleteToken">
      <p class="text-center text-base text-gray-500">
        Disconnecting will delete the access token stored. Would you like to continue?
      </p>
    </warning-confirm>
  </div>
</template>

<script>
import GithubTokenConnection from "@/components/serviceIntegration/GithubTokenConnection";
import GithubOAuthConnection from "@/components/serviceIntegration/GithubOAuthConnection";

import { useTokenStore } from "@/store/access";
import { ElNotification } from "element-plus";

export default {
  // output component: return a button which can open a dialog that contains two buttons
  name: "ConnectGithub",
  components: {
    GithubTokenConnection: GithubTokenConnection,
    GithubOAuthConnection: GithubOAuthConnection,
  },
  props: {
    statusChangeFunction: {
      type: Function,
      required: false,
      default: () => {},
    },
  },
  setup() {
    const manager = useTokenStore();
    return {
      manager,
    };
  },
  data() {
    return {
      dialogVisible: false,
      showTokenConnect: false,
      showOAuthConnect: false,
    };
  },
  methods: {
    openWebsite(url) {
      window.ipcRenderer.send("open-link-in-browser", url);
    },
    // callbacks for cleaning
    hideGithubTokenConnect() {
      this.showTokenConnect = false;
    },
    hideGithubOAuthConnect() {
      this.showOAuthConnect = false;
    },
    // call child components
    showGithubTokenConnect() {
      this.showTokenConnect = true;
      this.dialogVisible = false;
    },
    showGithubOAuthConnect() {
      this.showOAuthConnect = true;
      this.dialogVisible = false;
    },
    // delete key or add key
    interactWithService(serviceName) {
      if (serviceName == "github") {
        if ("github" in this.manager.accessTokens) {
          this.$refs.warningConfirm.show();
        } else {
          this.dialogVisible = true;
        }
      }
    },
    confirmDeleteToken() {
      this.deleteToken("github");
    },
    // delete key and give notification
    // APIkeyWarning(_key) {
    //   this.$refs.warningConfirm.show();
    // },
    async deleteToken(key) {
      let errorFound = false;
      try {
        await this.manager.deleteToken(key);
        this.$track("Connections", "GitHub", "disconnected");
        this.statusChangeFunction("disconnected");
      } catch (e) {
        errorFound = true;
        console.error(e);
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
    // github status for the button
    githubDetails() {
      let githubObject = {
        status: "Not Connected",
        name: "",
        action: "Connect to GitHub",
        buttonStyle: "primary-plain-button",
      };
      if ("github" in this.manager.accessTokens) {
        githubObject.status = "Connected";
        githubObject.name = this.manager.accessTokens.github.name;
        githubObject.action = "Disconnect from GitHub";
        githubObject.buttonStyle = "danger-plain-button";
      }
      return githubObject;
    },
  },
  mounted() {
    window.ipcRenderer.on("github-auth-token", (_e, arg, arg2) => {
      console.log(arg, arg2);
    });
  },
  unmounted() {
    window.ipcRenderer.removeAllListeners("github-auth-token");
  },
};
</script>
<style scoped>
.dialog-Container {
  @apply flex h-32 flex-col items-center justify-center gap-3;
}
.inputField {
  @apply flex gap-6;
}
</style>
