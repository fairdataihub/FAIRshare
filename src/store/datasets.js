"use strict";

import fs from "fs-extra";
import path from "path";
import { app } from "@electron/remote";
import { defineStore } from "pinia";

const USER_PATH = app.getPath("userData");
const DATASETS_STORE_PATH = path.join(
  USER_PATH,
  "Store",
  "unpublishedDatasets.soda"
);

// function to create the dataset store file in the user path
const createFile = async () => {
  fs.ensureFileSync(DATASETS_STORE_PATH);
  fs.writeJsonSync(DATASETS_STORE_PATH, []);
};

// function to load the dataset file into the store.
const loadFile = async () => {
  const exists = await fs.pathExists(DATASETS_STORE_PATH);

  if (!exists) {
    createFile();
    return [];
  } else {
    try {
      let unpublishedDatasets = fs.readJsonSync(DATASETS_STORE_PATH);
      return unpublishedDatasets;
    } catch (err) {
      console.error(err);
      return [];
    }
  }
};

// Schema to follow
// datasets = [
//   ...
//   {id: uuid, image: url, name: String, desciption: String}
//   ...
// ]

export const useDatasetsStore = defineStore({
  id: "DatasetsStore",
  state: () => ({
    datasets: [],
  }),
  getters: {
    datasetCount: function () {
      return this.datasets.length;
    },

    getAllDatasets() {
      return this.datasets;
    },
  },
  actions: {
    async addDataset(dataset) {
      // contains logic for altering different pieces of state
      try {
        this.datasets.push(dataset);
        // OR alternatively use .$patch to group change of posts and user.postsCount in devtools timeline
        // this.$patch((state) => {
        //   state.posts.push(post);
        // });
      } catch (error) {
        console.log(error);
      }
    },
    async loadDatasets() {
      try {
        const datasets = await loadFile();
        this.datasets = datasets;
      } catch (error) {
        console.error(error);
      }
    },
    async writeDatasetsToFile() {
      fs.ensureFileSync(DATASETS_STORE_PATH);
      fs.writeJsonSync(DATASETS_STORE_PATH, this.datasets);
    },
    getDataset(datasetID) {
      for (let dataset of this.datasets) {
        console.log(dataset.id, datasetID);
        if (dataset.id === datasetID) {
          return dataset;
        }
      }
      return "NO_DATASET_FOUND";
    },
  },
});
