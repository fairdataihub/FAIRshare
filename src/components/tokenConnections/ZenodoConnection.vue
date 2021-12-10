<template>
  <div class="w-auto">
    <el-button plain> Connect </el-button>
    <el-button type="danger" plain> Disconnect </el-button>
  </div>
</template>

<script>
import { useTokenStore } from "../../store/access";

export default {
  name: "ZenodoConnection",
  data() {
    return {
      manager: useTokenStore(),
    };
  },
  methods: {
    showConnectionPrompt() {
      // Show the dialog to get the token
      // verifyToken(token)          // this function should be defined in the store
      // Add token to store
      // set zenodoConnected in store to true
    },
    disconnect() {
      // delete token from store
      // set zenodoConnected in store to false
    },
  },
};
</script>

<style></style>
