<script setup>
import "@/assets/css/index.css";
import "element-plus/dist/index.css";

import FileDropZone from "./FileDropZone.vue";
</script>

<template>
  <Story title="File Drop Zone">
    <Variant title="About" icon="bi:filetype-doc">
      <p>All these spinners are CSS only.</p>
      <p>Might need explicit sizes to be defined</p>
    </Variant>
    <Variant title="Cube grid" icon="fa:spinner">
      <FileDropZone />
    </Variant>
  </Story>
</template>
