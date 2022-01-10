<template>
  <div class="buttonContainer">
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
  // empty component, only has a hidden dialog for accepting and process user-inputs
  name: "ZenodoTokenConnection",
  components: { AppDialog },
  props: {
    onStatusChange: { type: Function, required: false, default: () => {} },
    // callback function for cleaning
    callback: { type: Function },
  },

  data() {
    return {
      manager: useTokenStore(),
      dialogVisible: false,
      dialogHeaders: null,
      dialogNumInput: null,
    };
  },

  computed: {
    // connection status
    connectedToZenodoByToken() {
      return (
        "zenodo" in this.manager.accessTokens &&
        this.manager.accessTokens.zenodo.type == "token"
      );
    },
  },

  methods: {
    // spinner
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
    // receive results from user-inputs
    async getInputs(response) {
      this.dialogVisible = false;
      if (response[0] == "OK") {
        await this.processZenodo(response[1]);
      } else {
        // ElNotification({
        //   type: "info",
        //   message: "Input canceled",
        //   position: "bottom-right",
        //   duration: 2000,
        // });
        this.callback();
      }
    },
    // check token, save token and return notification
    async processZenodo(userInput) {
      let key = "zenodo";
      let value = userInput[0];
      let spinner = this.createLoading();
      let errorFound = false;
      if (await this.manager.verifyZenodoToken(value)) {
        let tokenObject = {};
        let name = userInput[1];
        try {
          tokenObject.token = value;
          tokenObject.name = name;
          tokenObject.type = "token";
          await this.manager.saveToken(key, tokenObject);
        } catch (e) {
          // console.log(e);
          errorFound = true;
        }
        if (!errorFound) {
          ElNotification({
            type: "success",
            message: "Connected to Zenodo successfully",
            position: "bottom-right",
            duration: 2000,
          });
          this.callback();
          this.onStatusChange("connected");
        }
      } else {
        ElNotification({
          type: "error",
          message: "Could not verify the token provided",
          position: "bottom-right",
          duration: 2000,
        });
        this.callback();
      }
      spinner.close();
    },
    // call a dialog for accepting user-inputs
    useAPIkey() {
      this.dialogNumInput = 2;
      this.dialogHeaders = [
        "Zenodo access token",
        "Token nick name of your choice",
      ];
      this.dialogVisible = true;
    },
  },
  // call a dialog immediately when teh empty div was mounted
  async mounted() {
    await this.manager.loadTokens();
    this.openDialog();
  },
};
</script>
