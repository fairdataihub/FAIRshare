<template>
  <div
    class="flex flex-col items-center justify-center w-full h-full max-w-screen-lg p-3 pr-5"
  >
    <div class="flex flex-col w-full h-full">
      <h1 class="pt-5 pb-1 text-3xl font-bold text-slate-700">
        Application Settings
      </h1>

      <line-divider></line-divider>

      <el-tabs v-model="activeName" class="w-11/12 py-5" tab-position="right">
        <el-tab-pane label="General" name="general" c>
          <div class="flex flex-col px-3 space-y-4">
            <div class="p-4 border-2 rounded-lg border-slate-100">
              <h2 class="py-2 text-lg font-semibold text-slate-600">Backup</h2>
              <p>Some explanation text for the setting</p>
            </div>
            <div class="p-4 border-2 rounded-lg border-slate-100">
              <h2 class="py-2 text-lg font-semibold text-slate-600">
                Some other setting
              </h2>
              <p>Some explanation text for the setting</p>
            </div>
          </div>
        </el-tab-pane>
        <el-tab-pane label="Advanced" name="proxy">
          <div class="flex flex-col px-3 space-y-4">
            <div class="p-4 border-2 rounded-lg border-slate-100">
              <h2 class="py-2 text-lg font-semibold text-slate-600">
                Advanced Backup
              </h2>
              <p>Some explanation text for the setting</p>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
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
