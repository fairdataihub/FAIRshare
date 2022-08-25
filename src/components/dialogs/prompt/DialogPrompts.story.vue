<script setup>
import "@/assets/css/index.css";
import { ref } from "vue";
import AddPrompt from "./AddPrompt.vue";

const addPrompt = ref(null);

const showPrompt = () => {
  addPrompt.value.show();
};
</script>

<template>
  <Story title="Prompts">
    <Variant title="About" icon="bi:filetype-doc">
      <p>All these spinners are CSS only.</p>
      <p>Might need explicit sizes to be defined</p>
    </Variant>
    <Variant title="Add prompt" icon="fa:spinner">
      <button @click="showPrompt">Show Prompt</button>
      <AddPrompt ref="addPrompt" />
    </Variant>
  </Story>
</template>
