<template>
  <div>
    <!-- <ul>
      <li v-for="post in datasets.datasets" :key="post">{{ post }}</li>
    </ul>
    <el-button @click="addPost">Add Post</el-button> -->
    <span>{{ datasets.datasets }}</span>
    <!-- <p>{{user.name}}</p> -->
    <router-link to="/home">Home</router-link>
  </div>
</template>

<script>
import { useDatasetsStore } from "../store/datasets";

export default {
  /* eslint-disable */
  name: "About",
  data() {
    return {
      datasets: useDatasetsStore(),
    };
  },
  methods: {
    addPost() {
      // this.$store.dispatch("insertPost", "post5");

      this.datasets.insertPost("post5");
    },
  },
  mounted() {
    // console.log(this.$route);
    // console.log(this.datasets.datasets);
    // console.log(this.$store.state.user.name);
    // console.log(this.$store.getters.postsCount);
  },
};
</script>
