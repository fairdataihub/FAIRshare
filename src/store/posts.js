"use strict";

import fs from "fs-extra";
import path from "path";
import { app } from "@electron/remote";
import { defineStore } from "pinia";

const createFile = async (datasetsFilePath) => {
  fs.ensureFileSync(datasetsFilePath);
  fs.writeJsonSync(datasetsFilePath, []);
};

const loadFile = async () => {
  const userPath = app.getPath("userData");
  const datasetsFilePath = path.join(
    userPath,
    "Store",
    "unpublishedDatasets.soda"
  );
  console.log(datasetsFilePath);
  const exists = await fs.pathExists(datasetsFilePath);

  if (!exists) {
    createFile(datasetsFilePath);
    return [];
  } else {
    let unpublishedDatasets = fs.readJsonSync(datasetsFilePath);
    return unpublishedDatasets;
  }
};

export const usePostsStore = defineStore({
  id: "PostsStore",
  state: () => ({
    posts: ["post 1", "post 2", "post 3", "post 4"],
    datasets: [],
  }),
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
    async loadposts() {
      try {
        const datasets = await loadFile();
        console.log(datasets);
        this.datasets = datasets;
      } catch (error) {
        console.log(error);
      }
    },
  },
});
