<template>
  <Popper
    :hover="true"
    offsetDistance="0"
    :content="popoverContent"
    class="z-10 pl-4"
  >
    <el-icon
      class="ml-4 cursor-help flex justify-center items-center text-gray-500 hover:text-black z-0"
      size="17"
    >
      <el-icon><question-filled /></el-icon>
    </el-icon>
  </Popper>
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

<style></style>
