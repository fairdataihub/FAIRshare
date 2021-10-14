<template>
  <div>
    <ul>
      <li v-for="post in posts.datasets" :key="post">{{ post }}</li>
    </ul>
    <el-button @click="addPost">Add Post</el-button>
    <span>{{posts.datasets}}</span>
    <!-- <p>{{user.name}}</p> -->
    <router-link to="/home">Home</router-link>
  </div>
</template>

<script>
import { usePostsStore } from "../store/posts";

export default {
  name: "About",
  data() {
    return {
      posts: usePostsStore(),
    };
  },
  methods: {
    addPost() {
      // this.$store.dispatch("insertPost", "post5");

      this.posts.insertPost("post5")
    },
  },
  mounted() {
    this.posts.loadposts();
    console.log(this.$route);
    console.log(this.posts.datasets)
    // console.log(this.$store.state.user.name);
    // console.log(this.$store.getters.postsCount);
  },
};
</script>

<style></style>
