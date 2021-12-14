<template>
  <Popper
    :hover="true"
    offsetDistance="0"
    :content="popoverContent"
    class="z-10"
  >
    <el-icon
      class="
        ml-4
        cursor-help
        flex
        justify-center
        items-center
        text-gray-500
        hover:text-black
        z-0
      "
      size="17"
    >
      <QuestionFilled class="z-0" />
    </el-icon>
  </Popper>
</template>

<script>
import { QuestionFilled } from "@element-plus/icons";

export default {
  name: "FormHelpContent",
  components: { QuestionFilled },
  props: {
    popoverContent: {
      type: String,
      default: "",
    },
  },
};
</script>

<style></style>
