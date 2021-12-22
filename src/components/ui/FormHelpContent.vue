<template>
  <div
    class="flex flex-row justify-center items-center text-gray-500 hover:text-black"
  >
    <el-popover
      placement="bottom"
      :width="`full`"
      trigger="hover"
      :content="popoverContent"
      class="cursor-help text-gray-500 hover:text-black"
    >
      <template #reference>
        <el-icon
          class="px-2 cursor-help flex justify-center items-center text-gray-500 hover:text-black z-0"
          size="18"
        >
          <question-filled />
        </el-icon>
      </template>
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
