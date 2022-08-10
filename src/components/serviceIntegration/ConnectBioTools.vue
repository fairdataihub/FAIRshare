<template>
  <div>
    <fade-transition>
      <button
        @click="changeConnectionStatus"
        :class="{ 'danger-plain-button': connected, 'primary-plain-button': !connected }"
        v-if="ready"
      >
        {{ connected ? "Disconnect from" : "Connect to" }} bio.tools
      </button>
      <div v-else>
        <Vue3Lottie
          animationLink="https://assets3.lottiefiles.com/packages/lf20_69bpyfie.json"
          :width="50"
          :height="50"
        />
      </div>
    </fade-transition>

    <login-prompt
      ref="loginPrompt"
      title="Login to bio.tools"
      confirmButtonText="Login"
      :preConfirm="checkUsernameAndPassword"
      :showErrors="showErrorMessage"
      @messageConfirmed="loginSuccess"
    >
      <div w-full>
        <p class="mb-1 w-full text-left text-base text-gray-500">
          Please enter your login information to let us connect your bio.tools account.
        </p>

        <div
          class="hover-underline-animation mb-4 flex w-max cursor-pointer flex-row items-center text-sm text-primary-600"
          @click="openWebsite('https://bio.tools/signup')"
        >
          <span class="font-medium"> Register for an account on bio.tools? </span>
          <Icon icon="grommet-icons:form-next-link" class="ml-2 h-5 w-5" />
        </div>

        <el-form ref="loginForm" :model="loginForm" :rules="rules" label-width="120px" size="large">
          <el-form-item label="Username" prop="username">
            <el-input
              v-model="loginForm.username"
              placeholder="username@bio.tools"
              clearable
              class="w-full"
            />
          </el-form-item>

          <el-form-item label="Password" prop="password">
            <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="**********"
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

import axios from "axios";
import { Icon } from "@iconify/vue";

export default {
  name: "ConnectBioTools",
  components: { Icon },
  props: {
    statusChangeFunction: {
      type: Function,
      required: false,
      default: () => {},
    },
  },
  data() {
    return {
      tokenStore: useTokenStore(),
      connected: false,
      ready: false,
      errorMessage: "",
      loginForm: {
        username: "",
        password: "",
      },
      rules: {
        username: [{ required: true, message: "Please enter your username", trigger: "blur" }],
        password: [{ required: true, message: "Please enter your password", trigger: "blur" }],
      },
    };
  },
  computed: {},
  methods: {
    openWebsite(url) {
      window.ipcRenderer.send("open-link-in-browser", url);
    },
    confirmDeleteToken() {
      this.deleteToken("biotools");
    },
    async deleteToken(key) {
      let errorFound = false;
      try {
        await this.tokenStore.deleteToken(key);
        this.$track("Connections", "bio.tools", "disconnected");
        this.statusChangeFunction("disconnected");
      } catch (e) {
        errorFound = true;
        console.error(e);
      }
      if (!errorFound) {
        this.$notify({
          duration: 2000,
          title: "Deleted",
          text: "Successfully disconnected from bio.tools",
          type: "success",
          position: "bottom-right",
        });
        this.connected = false;
      }
    },
    changeConnectionStatus() {
      if (this.connected) {
        this.$refs.warningConfirm.show();
      } else {
        this.$refs.loginPrompt.show();
      }
    },
    loginSuccess() {
      this.$notify({
        title: "Success",
        message: "You have successfully logged in to bio.tools",
        type: "success",
        position: "bottom-right",
      });
      this.connected = true;
    },
    async checkUsernameAndPassword() {
      if (this.loginForm.username === "" || this.loginForm.password === "") {
        return "empty";
      } else {
        const response = await axios
          .post(`${this.$server_url}/biotools/login`, {
            username: this.loginForm.username,
            password: this.loginForm.password,
          })
          .then(async (response) => {
            if ("general_errors" in response.data) {
              return "invalid";
            }

            if ("key" in response.data) {
              const token = response.data.key;
              const userDetails = await axios
                .get(`${this.$server_url}/biotools/user`, {
                  params: {
                    token,
                  },
                })
                .then(async (res) => {
                  if ("email" in res.data) {
                    return res.data;
                  }
                });

              let tokenObject = {};

              tokenObject.token = this.loginForm.password;
              tokenObject.name = userDetails.username;
              tokenObject.type = "password";

              await this.tokenStore.saveToken("biotools", tokenObject);
              this.$track("Connections", "bio.tools", "connected");

              this.connected = true;
              this.statusChangeFunction("connected");

              return "valid";
            }
          })
          .catch((error) => {
            console.error(error);
            return "ERROR";
          });

        return response;
      }
    },
    showErrorMessage(message) {
      this.errorMessage = message;
    },
  },
  async mounted() {
    const validBioToolsConnection = await this.tokenStore.verifyBioToolsConnection();

    if (validBioToolsConnection) {
      this.connected = true;
    } else {
      this.connected = false;
    }
    this.ready = true;
  },
};
</script>
