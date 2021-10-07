import { defineStore } from "pinia";

export const usePostsStore = defineStore({
  id: "PostsStore",
  state: () => ({ posts: ["post 1", "post 2", "post 3", "post 4"] }),
  getters: {
    // traditional function
    // postsCount: function(){
    //   return this.posts.length
    // },
    // method shorthand
    postsCount() {
      return this.posts.length;
    },
  },
  actions: {
    async insertPost(post) {
      // contains logic for altering different pieces of state
      try {
        // await doAjaxRequest(post);

        // directly alter the state via the action and
        // change multiple pieces of state
        this.posts.push(post);
        // this.user.postsCount++;

        // OR alternatavley use .$patch to group change of posts and user.postsCount in devtools timeline
        // this.$patch((state) => {
        //   state.posts.push(post);
        // //   state.user.postsCount++;
        // });
      } catch (error) {
        this.errors.push(error);
      }
    },
  },
});
