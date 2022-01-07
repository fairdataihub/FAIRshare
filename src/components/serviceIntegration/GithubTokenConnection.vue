<template>
  <div>
    <AppDialog
      v-if="dialogVisable"
      v-model="dialogVisable"
      :numInput="dialogNumInput"
      :headers="dialogHeaders"
      :callback="getInputs"
    ></AppDialog>
  </div>
</template>

<script>
import { useTokenStore } from "../../store/access";
import { ref } from "vue";
import { ElNotification } from "element-plus";
import { ElLoading } from "element-plus";
import AppDialog from "../dialogs/AppDialog";
export default {
  name: "GithubTokenConnection",
  components: { AppDialog },
  props: {
    callback: { type: Function },
  },
  setup() {
    const status = ref(["Connect GitHub token", ""]);
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
      this.dialogVisable = true;
    },
  },
  async mounted() {
    await this.manager.loadTokens();
    this.openDialog();
  },
};
</script>
