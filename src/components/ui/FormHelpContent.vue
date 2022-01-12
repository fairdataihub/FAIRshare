<template>
  <div
    class="flex flex-row items-center justify-center text-gray-500 hover:text-black"
  >
    <el-popover
      placement="bottom"
      :width="`full`"
      trigger="hover"
      class="text-gray-500 cursor-help hover:text-black"
    >
      <template #reference>
        <el-icon
          class="px-2 text-lg text-gray-500 hover:text-black cursor-help"
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
