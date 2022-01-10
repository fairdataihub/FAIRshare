<template>
  <div>
    <el-popover
      placement="bottom"
      :hide-after="0"
      trigger="hover"
      content="Coming soon..."
    >
      <template #reference>
        <div>
          <!-- <button class="w-48" @click="interactWithService('github')" :class="githubDetails.buttonStyle">
            {{ githubDetails.action }}
          </button> -->
          <el-button class="w-48" @click="interactWithService('github')" disabled>
            {{ githubDetails.action }}
          </el-button>
        </div>
      </template>
    </el-popover>
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
    </el-dialog>
    <GithubTokenConnection
      v-if="showTokenConnect"
      v-model="showTokenConnect"
      :callback="hideGithubTokenConnect"
    ></GithubTokenConnection>
    <GithubOAuthConnection
      v-if="showOAuthConnect"
      v-model="showOAuthConnect"
      :callback="hideGithubOAuthConnect"
    ></GithubOAuthConnection>
  </div>
</template>

<script>
import GithubTokenConnection from "@/components/serviceIntegration/GithubTokenConnection";
import GithubOAuthConnection from "@/components/serviceIntegration/GithubOAuthConnection";
import { useTokenStore } from "@/store/access";
import { ElNotification, ElMessageBox } from "element-plus";
export default {
  // output component: return a button which can open a dialog that contains two buttons
  name: "ConnectGithub",
  components: {
    GithubTokenConnection: GithubTokenConnection,
    GithubOAuthConnection: GithubOAuthConnection,
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
          this.APIkeyWarning("github");
        } else {
          this.dialogVisible = true;
        }
      }
    },
    // delete key and give notification
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
        console.log(e);
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
};
</script>
<style scoped>
.dialog-Container {
  @apply flex flex-col justify-center items-center gap-3 h-32;
}
.inputField {
  @apply flex gap-6;
}
</style>
