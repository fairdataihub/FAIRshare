<template>
  <div>
    <button
      :class="zenodoDetails.buttonStyle"
      @click="interactWithService('zenodo')"
    >
      {{ zenodoDetails.action }}
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
import ZenodoTokenConnection from "@/components/serviceIntegration/ZenodoTokenConnection";
import ButtonInputDialog from "@/components/dialogs/ButtonInputDialog";
import { useTokenStore } from "@/store/access";
import { markRaw } from "vue";
import { ElNotification, ElMessageBox } from "element-plus";
export default {
  name: "ConnectZenodo",
  components: {
    ZenodoTokenConnection: ZenodoTokenConnection,
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
      if (serviceName == "zenodo") {
        if ("zenodo" in this.manager.accessTokens) {
          this.APIkeyWarning("zenodo");
        } else {
          this.buttonList = [markRaw(ZenodoTokenConnection)];
          this.dialogNumInput = 1;
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
    zenodoDetails() {
      let zenodoObject = {
        status: "Not Connected",
        name: "",
        action: "Connect",
        buttonStyle: "primary-plain-button",
      };
      if ("zenodo" in this.manager.accessTokens) {
        zenodoObject.status = "Connected";
        zenodoObject.name = this.manager.accessTokens.zenodo.name;
        zenodoObject.action = "Disconnect";
        zenodoObject.buttonStyle = "danger-plain-button";
      }
      return zenodoObject;
    },
  },
};
</script>