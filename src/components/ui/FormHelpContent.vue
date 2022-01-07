<template>
  <div
    class="flex flex-row justify-center items-center text-gray-500 hover:text-black"
  >
    <el-popover
      placement="bottom"
      :width="`full`"
      trigger="hover"
      class="cursor-help text-gray-500 hover:text-black"
    >
      <template #reference>
        <el-icon
          class="px-2 text-gray-500 hover:text-black text-lg cursor-help"
          size="18"
        >
          <question-filled />
        </el-icon>
      </template>
      <p v-html="popoverContent"></p>
    </el-popover>
  </div>
</template>

<script>
export default {
  name: "FormHelpContent",
  props: {
    popoverContent: {
      type: String,
      default: "",
    },
  },
};
</script>
