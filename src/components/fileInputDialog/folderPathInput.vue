<template>
  <el-input
    v-model="folderPath"
    placeholder="Click here to select a folder"
    class="my-3 w-full"
    size="large"
    @click="selectFolderPath"
  />
</template>

<script>
import { dialog } from "@electron/remote";

export default {
  name: "folderPathInput",
  props: {},
  emits: ["folderSelected"],
  data() {
    return {
      folderPath: "",
    };
  },
  computed: {},
  methods: {
    selectFolderPath() {
      let that = this;
      dialog.showOpenDialog({ properties: ["openDirectory"] }).then((data) => {
        if (!data.canceled) {
          this.folderPath = data.filePaths[0];

          that.$emit("folderSelected", this.folderPath);
        }
      });
    },
  },

  mounted() {},
};
</script>
