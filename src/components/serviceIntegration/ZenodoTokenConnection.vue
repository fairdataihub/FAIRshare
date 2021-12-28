<template>
  <div class="buttonContainer">
    <!-- <el-button
      plain
      class="button"
      @click="openDialog()"
      :type="buttonStatus.buttonStyle"
      >{{ buttonStatus.buttonText }}</el-button
    > -->
    <button :class="buttonStatus.buttonStyle" @click="openDialog()">
      {{ buttonStatus.buttonText }}
    </button>
    <AppDialog
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
import { ElMessageBox } from "element-plus";
import AppDialog from "../dialogs/AppDialog";
export default {
  name: "ZenodoTokenConnection",
  components: { AppDialog },
  setup() {
    const dialogVisable = ref(false);
    const dialogHeaders = ref(null);
    const dialogNumInput = ref(null);
    return {
      dialogVisable,
      dialogHeaders,
      dialogNumInput,
    };
  },
  props: {
    callbackFunction: {
      type: Function,
      required: false,
      default: () => {},
    },
  },
  data() {
    return {
      manager: useTokenStore(),
    };
  },
  computed: {
    buttonStatus() {
      let zenodoObject = {
        buttonText: "Connect zenodo token",
        buttonStyle: "primary-plain-button",
      };
      if (
        "zenodo" in this.manager.accessTokens &&
        this.manager.accessTokens.zenodo.type == "token"
      ) {
        zenodoObject.buttonText = "Disconnect zenodo token";
        zenodoObject.buttonStyle = "danger-plain-button";
      }
      return zenodoObject;
    },
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
      if (
        "zenodo" in this.manager.accessTokens &&
        this.manager.accessTokens.github.type == "token"
      ) {
        this.APIkeyWarning();
      } else {
        this.useAPIkey();
      }
    },
    async getInputs(response) {
      this.dialogVisable = false;
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
          this.callbackFunction();
          ElNotification({
            type: "success",
            message: "Connected to Zenodo successfully",
            position: "bottom-right",
            duration: 2000,
          });
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
      this.dialogHeaders = ["Zenodo access token", "Token nick name"];
      this.dialogVisable = true;
    },

    APIkeyWarning() {
      ElMessageBox.confirm(
        "Do you want to remove the connection to Zenodo?",
        "Warning",
        {
          confirmButtonText: "OK",
          cancelButtonText: "Cancel",
          type: "warning",
        }
      )
        .then(async () => {
          this.deleteToken("zenodo");
          this.callbackFunction();
        })
        .catch(() => {
          // ElNotification({
          //   type: "info",
          //   message: "Delete canceled",
          //   position: "bottom-right",
          //   duration: 2000,
          // });
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
          message: "Successfully disconnected from Zenodo",
          position: "bottom-right",
          duration: 2000,
        });
      }
    },
  },
  async mounted() {
    await this.manager.loadTokens();
  },
};
</script>
