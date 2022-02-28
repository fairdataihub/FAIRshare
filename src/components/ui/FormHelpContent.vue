<template>
  <div
    class="flex flex-row items-center justify-center text-gray-500 hover:text-black"
  >
    <el-popover
      placement="bottom"
      :width="`full`"
      trigger="hover"
      class="cursor-help text-gray-500 hover:text-black"
    >
      <template #reference>
        <div
          class="flex cursor-help items-center justify-center px-2 text-lg text-neutral-500 hover:text-neutral-800"
        >
          <el-icon size="18">
            <question-filled />
          </el-icon>
        </div>
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
