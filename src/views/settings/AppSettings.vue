<template>
  <div
    class="flex flex-col items-center justify-center w-full h-full max-w-screen-lg p-3 pr-5"
  >
    <div class="flex flex-col items-center w-full h-full">
      <div class="flex w-full">
        <span class="py-5 text-3xl font-bold text-slate-700">
          Application Settings
        </span>
      </div>
      <div class="flex w-full">
        <el-tabs v-model="activeName" class="w-11/12">
          <el-tab-pane label="General" name="general"> General </el-tab-pane>
          <el-tab-pane label="Advanced" name="proxy">
            Allow beta updates
          </el-tab-pane>
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
      activeName: "general",
    };
  },
  methods: {},
  computed: {},
  async mounted() {},
};
</script>

<style scoped></style>
