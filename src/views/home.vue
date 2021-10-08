<template>
    <el-container>
      <el-aside width="200px">sid2</el-aside>
      <el-main>Main</el-main>
    </el-container>
</template>

<script>
export default {
  name: "HomePage",
  components: {},
  data() {
    return {};
  },
  methods: {},
  mounted() {
    console.log(this.$route);
    // console.log(this.$store.state.user.name);
    // console.log(this.$store.getters.postsCount);
  },
};
</script>

<style></style>
