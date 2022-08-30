<template>
  <hr class="my-4" :class="[type]" />
</template>

<script>
export default {
  name: "LineDivider",
  props: {
    type: {
      type: String,
      default: "solid",
    },
  },
};
</script>

<style scoped>
hr.dashed {
  border-style: dashed;
}

hr.dotted {
  border-style: dotted;
}

hr.solid {
  border-style: solid;
}

hr.rounded {
  border-style: solid;
}
</style>
