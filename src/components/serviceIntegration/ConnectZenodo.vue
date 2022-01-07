<template>
  <!-- <div>
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
  </div> -->
  <div>
    <button
      :class="zenodoDetails.buttonStyle"
      @click="interactWithService('zenodo')"
    >
      {{ zenodoDetails.action }}
    </button>
    <el-dialog
      width="600px"
      destroy-on-close
      v-model="dialogVisable"
      title="Select an option to connect to Zenodo"
    >
      <div class="dialog-Container">
        <div class="inputField">
          <button class="primary-plain-button" @click="showZenodoTokenConnect">
            Connect with token
          </button>
          <el-popover
            placement="top"
            :hide-after="0"
            trigger="hover"
            content="Coming soon..."
          >
            <template #reference>
              <div>
                <el-button
                  class="primary-plain-button"
                  @click="showZenodoOAuthConnect"
                  disabled
                  >Connect with username</el-button
                >
              </div>
            </template>
          </el-popover>
        </div>
      </div>
    </el-dialog>
    <ZenodoTokenConnection
      v-if="showTokenConnect"
      v-model="showTokenConnect"
      :callback="hideZenodoTokenConnect"
    ></ZenodoTokenConnection>
    <!-- <ZenodoOAuthConnection v-if="showOAuthConnect" v-model="showOAuthConnect" :callback = "hideZenodoOAuthConnect"></ZenodoOAuthConnection> -->
  </div>
</template>

<script>
/* eslint-disable vue/no-unused-components */
import ZenodoTokenConnection from "@/components/serviceIntegration/ZenodoTokenConnection";
import ButtonInputDialog from "@/components/dialogs/ButtonInputDialog";
import { useTokenStore } from "@/store/access";
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
      dialogVisable: false,

      showTokenConnect: false,
      showOAuthConnect: false,
    };
  },
  methods: {
    hideZenodoTokenConnect() {
      this.showTokenConnect = false;
    },
    hideZenodoOAuthConnect() {
      this.showOAuthConnect = false;
    },
    showZenodoTokenConnect() {
      this.showTokenConnect = true;
      this.dialogVisable = false;
    },
    showZenodoOAuthConnect() {
      this.showOAuthConnect = true;
      this.dialogVisable = false;
    },
    interactWithService(serviceName) {
      if (serviceName == "zenodo") {
        if ("zenodo" in this.manager.accessTokens) {
          this.APIkeyWarning("zenodo");
        } else {
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
<style scoped>
.dialog-Container {
  @apply flex flex-col justify-center items-center gap-3 h-32;
}
.inputField {
  @apply flex gap-6;
}
</style>
