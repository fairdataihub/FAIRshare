<template>
  <div>
    <TheCalculator> </TheCalculator>
  </div>
</template>

<script>
import TheCalculator from "../components/TheCalculator.vue";

export default {
  name: "HomePage",
  components: { TheCalculator },
  mounted() {
    console.log(this.$route);
  },
};
</script>

<style></style>
