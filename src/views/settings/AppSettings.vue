<template>
  <div
    class="flex h-full w-full max-w-screen-lg flex-col items-center justify-center p-3 pr-5"
  >
    <div class="flex h-full w-full flex-col">
      <h1 class="pt-5 pb-1 text-3xl font-bold text-slate-700">
        Application Settings
      </h1>

      <line-divider></line-divider>

      <el-tabs v-model="activeName" class="w-11/12 py-5" tab-position="right">
        <el-tab-pane label="General" name="general" c>
          <div class="flex flex-col space-y-4 px-3">
            <div class="rounded-lg border-2 border-slate-100 p-4">
              <h2 class="py-2 text-lg font-semibold text-slate-600">
                Configuration Folder
              </h2>
              <div class="flex flex-col">
                <p>Some explanation text for the setting</p>
              </div>
            </div>
            <div class="rounded-lg border-2 border-slate-100 p-4">
              <h2 class="py-2 text-lg font-semibold text-slate-600">
                Some other setting
              </h2>
              <p>Some explanation text for the setting</p>
            </div>
          </div>
        </el-tab-pane>
        <el-tab-pane label="Advanced" name="proxy">
          <div class="flex flex-col space-y-4 px-3">
            <div class="rounded-lg border-2 border-slate-100 p-4">
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
