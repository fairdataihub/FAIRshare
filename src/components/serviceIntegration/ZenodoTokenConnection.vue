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
  name: "ZenodoTokenConnection",

  components: { AppDialog },

  props: {
    onStatusChange: { type: Function, required: false, default: () => {} },
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
    connectedToZenodoByToken() {
      return (
        "zenodo" in this.manager.accessTokens &&
        this.manager.accessTokens.zenodo.type == "token"
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
        await this.processZenodo(response[1]);
      } else {
        // ElNotification({
        //   type: "info",
        //   message: "Input canceled",
        //   position: "bottom-right",
        //   duration: 2000,
        // });
      }
    },
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

          this.onStatusChange("connected");
        }
      } else {
        ElNotification({
          type: "error",
          message: "Could not verify the token provided",
          position: "bottom-right",
          duration: 2000,
        });
      }
      spinner.close();
    },

    useAPIkey() {
      this.dialogNumInput = 2;
      this.dialogHeaders = [
        "Zenodo access token",
        "Token nick name of your choice",
      ];
      this.dialogVisible = true;
    },
  },

  async mounted() {
    await this.manager.loadTokens();
    this.openDialog();
  },
};
</script>
