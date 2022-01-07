<template>
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
      v-model="dialogVisible"
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
                <button
                  class="primary-plain-button"
                  @click="showZenodoOAuthConnect"
                  disabled
                >
                  Connect with username
                </button>
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
      :onStatusChange="statusChangeFunction"
    ></ZenodoTokenConnection>
    <!-- <ZenodoOAuthConnection v-if="showOAuthConnect" v-model="showOAuthConnect" :callback = "hideZenodoOAuthConnect"></ZenodoOAuthConnection> -->
  </div>
</template>

<script>
import ZenodoTokenConnection from "@/components/serviceIntegration/ZenodoTokenConnection";

import { useTokenStore } from "@/store/access";

import { ElNotification, ElMessageBox } from "element-plus";

export default {
  name: "ConnectZenodo",
  components: {
    ZenodoTokenConnection: ZenodoTokenConnection,
  },
  props: {
    statusChangeFunction: {
      type: Function,
      required: false,
      default: () => {},
    },
  },
  data() {
    return {
      manager: useTokenStore(),
      dialogVisible: false,
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
      this.dialogVisible = false;
    },
    showZenodoOAuthConnect() {
      this.showOAuthConnect = true;
      this.dialogVisible = false;
    },
    interactWithService(serviceName) {
      if (serviceName == "zenodo") {
        if ("zenodo" in this.manager.accessTokens) {
          this.APIkeyWarning("zenodo");
        } else {
          this.dialogVisible = true;
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
        this.statusChangeFunction("disconnected");
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
