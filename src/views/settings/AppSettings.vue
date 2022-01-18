<template>
  <div
    class="
      flex flex-col
      items-center
      justify-center
      w-full
      h-full
      max-w-screen-lg
      p-3
      pr-5
    "
  >
    <div class="flex flex-col items-center w-full h-full">
      <div class="flex item-left w-full">
        <span class="text-[30px] font-medium pt-[30px] pb-[30px]"> Application Settings</span>
      </div>
      <div class="flex item-left w-full">
        <el-tabs v-model="activeName" class="w-11/12">
          <el-tab-pane label="Open log folder" name="first">Open log folder</el-tab-pane>
          <el-tab-pane label="Allow beta updates" name="second">Allow beta updates</el-tab-pane>
          <el-tab-pane label="Dark mode toggle" name="third">Dark mode toggle</el-tab-pane>
          <el-tab-pane label="Manage accounts" name="fourth">Manage accounts</el-tab-pane>
        </el-tabs>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "AppSettings",

  components: {},

  data() {
    return {
      activeName: "1",
    };
  },

  methods: {
  },

  computed: {},

  async mounted() {},
};
</script>

<style scoped>
</style>
