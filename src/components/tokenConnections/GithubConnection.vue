<template>
  <div class="w-auto">
    <el-button plain> Connect </el-button>
    <el-button type="danger" plain> Disconnect </el-button>
  </div>
</template>

<script>
import { useTokenStore } from "../../store/access";

export default {
  name: "GithubConnection",
  data() {
    return {
      manager: useTokenStore(),
    };
  },
};
</script>

<style></style>
