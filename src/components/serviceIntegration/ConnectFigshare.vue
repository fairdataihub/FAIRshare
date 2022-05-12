<template>
  <div>
    <fade-transition>
      <button
        @click="changeConnectionStatus"
        :class="{ 'danger-plain-button': connected, 'primary-plain-button': !connected }"
        v-if="ready"
      >
        {{ connected ? "Disconnect from" : "Connect to" }} Figshare
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
          Please enter your token information to let us connect to your Figshare account.
        </p>

        <div
          class="hover-underline-animation mb-4 flex w-max cursor-pointer flex-row items-center text-sm text-primary-600"
          @click="openWebsite('https://figshare.com/account/applications')"
        >
          <span class="font-medium"> Create a token on Figshare? </span>
          <Icon icon="grommet-icons:form-next-link" class="ml-2 h-5 w-5" />
        </div>

        <el-form ref="loginForm" :model="loginForm" :rules="rules" label-width="130px" size="large">
          <el-form-item label="Personal token" prop="token">
            <el-input
              v-model="loginForm.token"
              placeholder="Your personal token"
              clearable
              class="w-full"
            />
          </el-form-item>

          <el-form-item label="Token name" prop="name">
            <el-input
              v-model="loginForm.name"
              placeholder="FAIRshare Token"
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
  name: "ConnectFigshare",
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
        token: "",
        name: "",
      },
      rules: {
        token: [
          { required: true, message: "Please enter your personal access token", trigger: "blur" },
        ],
        name: [
          {
            required: true,
            message: "Please enter a name to identify this token",
            trigger: "blur",
          },
        ],
      },
    };
  },
  computed: {},
  methods: {
    confirmDeleteToken() {
      this.deleteToken("figshare");
    },
    async deleteToken(key) {
      let errorFound = false;
      try {
        await this.tokenStore.deleteToken(key);
        this.$track("Connections", "figshare", "disconnected");
        this.statusChangeFunction("disconnected");
      } catch (e) {
        errorFound = true;
        console.log(e);
      }
      if (!errorFound) {
        this.$notify({
          duration: 2000,
          title: "Deleted",
          text: "Successfully disconnected from Figshare",
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
        message: "You have successfully logged in to Figshare",
        type: "success",
        position: "bottom-right",
      });
      this.connected = true;
    },
    async checkUsernameAndPassword() {
      if (this.loginForm.token === "" || this.loginForm.name === "") {
        return "empty";
      } else {
        const config = {
          method: "get",
          url: `${process.env.VUE_APP_FIGSHARE_SERVER_URL}/token`,
          headers: {
            Authorization: `token ${this.loginForm.token}`,
          },
        };

        const response = await axios(config)
          .then(async (response) => {
            if (response.status === 200) {
              let tokenObject = {};

              tokenObject.token = this.loginForm.token;
              tokenObject.name = this.loginForm.name;
              tokenObject.type = "token";

              await this.tokenStore.saveToken("figshare", tokenObject);

              // WILL NEED TO COME BACK TO THIS. Can't have returns be read in a prop function.
              // calling the hide and notification methods directly from this component for now.
              this.loginSuccess();
              this.$refs.loginPrompt.hide();

              return "valid";
            } else {
              return "invalid";
            }
          })
          .catch((error) => {
            console.log(error);
          });

        console.log(response);

        // const response = await axios
        //   .post(`${this.$server_url}/biotools/login`, {
        //     username: this.loginForm.username,
        //     password: this.loginForm.password,
        //   })
        //   .then(async (response) => {
        //     if ("general_errors" in response.data) {
        //       return "invalid";
        //     }

        //     if ("key" in response.data) {
        //       const token = response.data.key;
        //       const userDetails = await axios
        //         .get(`${this.$server_url}/biotools/user`, {
        //           params: {
        //             token,
        //           },
        //         })
        //         .then(async (res) => {
        //           if ("email" in res.data) {
        //             return res.data;
        //           }
        //         });

        //       let tokenObject = {};

        //       tokenObject.token = this.loginForm.password;
        //       tokenObject.name = userDetails.username;
        //       tokenObject.type = "password";

        //       await this.tokenStore.saveToken("biotools", tokenObject);
        //       this.$track("Connections", "bio.tools", "connected");

        //       this.connected = true;
        //       this.statusChangeFunction("connected");

        //       return "valid";
        //     }
        //   })
        //   .catch((error) => {
        //     console.error(error);
        //     return "ERROR";
        //   });

        // return response;
      }
    },
    showErrorMessage(message) {
      this.errorMessage = message;
    },
  },
  async mounted() {
    const validFigshareConnection = await this.tokenStore.verifyFigshareConnection();

    if (validFigshareConnection) {
      this.connected = true;
    } else {
      this.connected = false;
    }
    this.ready = true;
  },
};
</script>
