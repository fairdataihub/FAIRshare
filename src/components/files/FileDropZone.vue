<template>
  <div class="pt-5 pb-3">
    <div
      class="dropzone group flex w-full cursor-pointer items-center justify-center space-x-4 rounded-md border-2 border-dashed transition-all hover:border-primary-400"
      :class="{ 'border-primary-400': highlightBox }"
      @click="openFileDialog"
      @drop.prevent="onDrop"
      @dragenter.prevent="highlightBox = true"
      @dragover.prevent="highlightBox = true"
      @dragleave.prevent="highlightBox = false"
      @dragend.prevent="highlightBox = false"
    >
      <Vue3Lottie
        animationLink="https://assets3.lottiefiles.com/packages/lf20_GxMZME.json"
        :width="120"
        :height="120"
        class="scale-95 transition-all group-hover:scale-100"
        :class="{ '!scale-100': highlightBox }"
      />

      <span class="font-medium transition-all group-hover:text-primary-500">
        Drag and drop files here or click to select files
      </span>
    </div>

    <div class="file-list py-2">
      <div
        v-for="file in localFileList"
        :key="file"
        class="flex cursor-default flex-row items-center justify-between rounded-lg py-1 px-3 transition-all hover:bg-primary-50"
      >
        <div class="flex items-center">
          <Icon icon="akar-icons:file" width="20" height="20" />

          <div class="ml-2 flex flex-col">
            <p class="text-sm">{{ baseName(file) }}</p>

            <span class="text-xs text-gray-600">{{ file }}</span>
          </div>
        </div>

        <div class="cursor-pointer text-gray-500 hover:text-gray-800">
          <el-popconfirm title="Are you sure to remove this?" @confirm="removeFile(file)">
            <template #reference>
              <Icon icon="ep:delete" width="20" height="20" class="outline-0" />
            </template>
          </el-popconfirm>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Icon } from "@iconify/vue";
import path from "path";

export default {
  name: "FileDropZone",
  emits: ["filesUpdated"],
  components: {
    Icon,
  },
  props: {
    title: {
      type: String,
      required: false,
      default: "Select file",
    },
    buttonLabel: {
      type: String,
      required: false,
      default: "Select file",
    },
    multiple: {
      type: Boolean,
      default: false,
    },
    showHiddenFiles: {
      type: Boolean,
      default: false,
    },
    allowFiles: {
      type: Boolean,
      default: true,
    },
    allowDirectories: {
      type: Boolean,
      default: false,
    },
    fileList: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      localFileList: [],
      highlightBox: false,
      events: ["dragenter", "dragover", "dragleave", "drop"],
    };
  },
  methods: {
    baseName(filePath) {
      return path.basename(filePath);
    },
    removeFile(file) {
      this.localFileList = this.localFileList.filter((f) => f !== file);
      this.$emit("filesUpdated", this.localFileList);
    },
    onDrop(event) {
      const droppedFiles = event.dataTransfer.files;

      if (droppedFiles && droppedFiles.length > 0) {
        for (const file of droppedFiles) {
          if (!this.localFileList.includes(file.path)) {
            this.localFileList.push(file.path);
          }
        }

        this.$emit("filesUpdated", this.localFileList);
      }

      this.highlightBox = false;
    },
    openFileDialog() {
      let data = {};

      data.title = this.title;
      data.buttonLabel = this.buttonLabel;
      data.properties = [];

      if (this.allowFiles) {
        data.properties.push("openFile");
      }

      if (this.allowDirectories) {
        data.properties.push("openDirectory");
      }

      if (this.multiple) {
        data.properties.push("multiSelections");
      }

      if (this.showHiddenFiles) {
        data.properties.push("showHiddenFiles");
      }

      window.ipcRenderer.invoke("show-open-file-dialog", data).then((result) => {
        if (result && result.length > 0) {
          for (const file of result) {
            if (!this.localFileList.includes(file)) {
              this.localFileList.push(file);
            }
          }
          this.$emit("filesUpdated", this.localFileList);
        }
      });
    },
  },
  mounted() {
    if (this.fileList && this.fileList.length > 0) {
      this.localFileList = this.fileList;
    }
  },
};
</script>
