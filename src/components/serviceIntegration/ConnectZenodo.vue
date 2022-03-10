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
          <button
            class="primary-plain-button w-52"
            @click="showZenodoTokenConnect"
          >
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
    <!-- <ZenodoOAuthConnection
      v-if="showOAuthConnect"
      v-model="showOAuthConnect"
      :callback="hideZenodoOAuthConnect"
      :onStatusChange="statusChangeFunction"
    ></ZenodoOAuthConnection> -->

    <warning-confirm
      ref="warningConfirm"
      title="Warning"
      @messageConfirmed="confirmDeleteToken"
    >
      <p class="text-center text-base text-gray-500">
        Disconnecting will delete the access token stored. Would you like to
        continue?
      </p>
    </warning-confirm>
  </div>
</template>

<script>
import ZenodoTokenConnection from "@/components/serviceIntegration/ZenodoTokenConnection";
// import ZenodoOAuthConnection from "@/components/serviceIntegration/ZenodoOAuthConnection";
import { useTokenStore } from "@/store/access";
import { ElNotification } from "element-plus";

export default {
  // output component: return a button which can open a dialog that contains two buttons
  name: "ConnectZenodo",
  components: {
    ZenodoTokenConnection,
    //  ZenodoOAuthConnection,
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
    // callbacks for cleaning
    hideZenodoTokenConnect() {
      this.showTokenConnect = false;
    },
    hideZenodoOAuthConnect() {
      this.showOAuthConnect = false;
    },
    // call child components
    showZenodoTokenConnect() {
      this.showTokenConnect = true;
      this.dialogVisible = false;
    },
    showZenodoOAuthConnect() {
      this.showOAuthConnect = true;
      this.dialogVisible = false;
    },
    // delete key or add key
    interactWithService(serviceName) {
      if (serviceName == "zenodo") {
        if ("zenodo" in this.manager.accessTokens) {
          this.$refs.warningConfirm.show();
        } else {
          this.dialogVisible = true;
        }
      }
    },
    // delete key
    confirmDeleteToken() {
      this.deleteToken("zenodo");
    },
    // // delete key and give notification
    // APIkeyWarning(_key) {
    //   this.$refs.warningConfirm.show();
    // },
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
    // zneodo status
    zenodoDetails() {
      let zenodoObject = {
        status: "Not Connected",
        name: "",
        action: "Connect to Zenodo",
        buttonStyle: "primary-plain-button",
      };
      if ("zenodo" in this.manager.accessTokens) {
        zenodoObject.status = "Connected";
        zenodoObject.name = this.manager.accessTokens.zenodo.name;
        zenodoObject.action = "Disconnect from Zenodo";
        zenodoObject.buttonStyle = "danger-plain-button";
      }
      return zenodoObject;
    },
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
