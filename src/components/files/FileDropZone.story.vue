<script setup>
import "@/assets/css/utilities-theme.css";
import "@/assets/css/index.css";
import "element-plus/dist/index.css";
import "vue3-lottie/dist/style.css";

import FileDropZone from "./FileDropZone.vue";
</script>

<template>
  <Story title="File Drop Zone">
    <Variant title="About" icon="bi:filetype-doc">
      <p>All these spinners are CSS only.</p>
      <p>Might need explicit sizes to be defined</p>
    </Variant>
    <Variant title="Component" icon="akar-icons:file">
      <FileDropZone />
    </Variant>
  </Story>
</template>
