<template>
  <div>
    <fade-transition>
      <button
        @click="changeConnectionStatus"
        :class="{ 'danger-plain-button': connected, 'primary-plain-button': !connected }"
        v-if="ready"
      >
        {{ connected ? "Disconnect from" : "Connect to" }} GitHub
      </button>
      <div v-else class="flex justify-center">
        <Vue3Lottie
          animationLink="https://assets3.lottiefiles.com/packages/lf20_69bpyfie.json"
          :width="50"
          :height="50"
        />
      </div>
    </fade-transition>

    <lottie-dialog
      ref="lottieDialog"
      animationURL="https://assets3.lottiefiles.com/packages/lf20_jcikwtux.json"
      title="Redirecting to GitHub..."
      confirmButtonText="Open auth.fairshareapp.io"
      @messageConfirmed="openBrowserAuth"
    >
      <div w-full>
        <p class="mb-2 w-full text-center text-base">
          FAIRshare will take you to `auth.fairshareapp.io` to login via GitHub. This step will be
          done in your browser. You will be redirected back to FAIRshare after you have logged in.
        </p>
      </div>
    </lottie-dialog>

    <login-prompt
      ref="loginPrompt"
      title="Login to GitHub"
      confirmButtonText="Login"
      :preConfirm="checkGithubToken"
      :showErrors="showErrorMessage"
      @messageConfirmed="loginSuccess"
    >
      <div w-full>
        <p class="mb-5 w-full text-left text-sm text-gray-500">
          Please enter your authentication token below from the authentication platform.
        </p>

        <el-form ref="loginForm" :model="loginForm" :rules="rules" label-width="120px" size="large">
          <el-form-item label="Access Token" prop="token">
            <el-input
              v-model="loginForm.token"
              placeholder="71d23243c2c40b6fad"
              clearable
              class="w-full"
            />
          </el-form-item>
        </el-form>

        <fade-transition>
          <p v-if="errorMessage !== ''" class="my-3 w-full text-center text-base text-red-600">
            {{ errorMessage }}
          </p>
        </fade-transition>
      </div>
    </login-prompt>

    <warning-confirm ref="warningConfirm" title="Warning" @messageConfirmed="confirmDeleteToken">
      <p class="text-center text-base text-gray-500">
        Disconnecting will delete the access token stored. Would you like to continue?
      </p>
    </warning-confirm>
  </div>
</template>

<script>
import { useTokenStore } from "@/store/access";
import { ElNotification } from "element-plus";

export default {
  // output component: return a button which can open a dialog that contains two buttons
  name: "ConnectGithub",
  components: {},
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
      ready: false,
      connected: false,
      errorMessage: "",
      loginForm: {
        token: "",
      },
      rules: {
        token: [{ required: true, message: "Please enter your token", trigger: "blur" }],
      },
    };
  },
  methods: {
    openWebsite(url) {
      window.ipcRenderer.send("open-link-in-browser", url);
    },

    changeConnectionStatus() {
      console.log(this.connected);
      if (this.connected) {
        this.$refs.warningConfirm.show();
      } else {
        this.$refs.lottieDialog.show();
      }
    },

    openBrowserAuth() {
      window.ipcRenderer.send("fairshare-auth", "github");
      this.$refs.loginPrompt.show();
    },

    async checkGithubToken() {
      if (this.loginForm.token === "") {
        return "empty";
      } else {
        const response = await this.manager.verifyGithubToken(this.loginForm.token);

        if (response) {
          const tokenObject = {};
          const key = "github";
          const name = await this.manager.getGithubUser(this.loginForm.token);

          let errorFound = false;

          try {
            tokenObject.token = this.loginForm.token;
            tokenObject.name = name;
            tokenObject.type = "OAuth";

            await this.manager.saveToken(key, tokenObject);
          } catch (e) {
            errorFound = true;

            return "ERROR";
          }

          if (!errorFound) {
            ElNotification({
              type: "success",
              message: "Saved successfully",
              position: "bottom-right",
              duration: 2000,
            });

            this.$track("Connections", "GitHub", "connected");

            this.statusChangeFunction("connected");

            return "valid";
          }
        } else {
          return "invalid";
        }
      }
    },

    loginSuccess() {
      this.$notify({
        title: "Success",
        message: "You have successfully logged in to GitHub",
        type: "success",
        position: "bottom-right",
      });
      this.connected = true;
    },

    showErrorMessage(message) {
      this.errorMessage = message;
    },

    confirmDeleteToken() {
      this.deleteToken("github");
    },

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

      this.connected = false;
    },
  },

  async mounted() {
    window.ipcRenderer.on("github-auth-token", (_e, arg) => {
      this.loginForm.token = arg;
      this.$refs.loginPrompt.confirm();
    });

    const validGitHubConnection = await this.manager.verifyGithubConnection();

    if (validGitHubConnection) {
      this.connected = true;
    } else {
      this.connected = false;
    }

    this.ready = true;
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
