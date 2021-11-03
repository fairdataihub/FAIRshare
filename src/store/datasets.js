"use strict";

import fs from "fs-extra";
import path from "path";
import { app } from "@electron/remote";
import { defineStore } from "pinia";

const USER_PATH = app.getPath("userData");
const DATASETS_STORE_PATH = path.join(
  USER_PATH,
  "Store",
  "unpublishedDatasets.json"
);

// function to create the dataset store file in the user path
const createFile = async () => {
  fs.ensureFileSync(DATASETS_STORE_PATH);
  fs.writeJsonSync(DATASETS_STORE_PATH, {});
};

// function to load the dataset file into the store.
const loadFile = async () => {
  const exists = await fs.pathExists(DATASETS_STORE_PATH);

  if (!exists) {
    createFile();
    return {};
  } else {
    try {
      let unpublishedDatasets = fs.readJsonSync(DATASETS_STORE_PATH);
      return unpublishedDatasets;
    } catch (err) {
      console.error(err);
      return {};
    }
  }
};

// Schema to follow
// datasets = {
//   datasetID: {
//     id: uuid,
//     image: url,
//     name: String,
//     description: String,
//   },
// };

export const useDatasetsStore = defineStore({
  id: "DatasetsStore",
  state: () => ({
    datasets: {},
    currentDataset: {},
  }),
  getters: {
    datasetCount: function () {
      return Object.keys(this.datasets).length;
    },

    getAllDatasets() {
      return this.datasets;
    },
  },
  actions: {
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
    async addDataset(dataset, datasetID) {
      try {
        this.datasets[datasetID] = dataset;
        this.currentDataset = dataset;
        this.writeDatasetsToFile();
      } catch (error) {
        console.log(error);
      }
    },
    async syncDatasets() {
      const datasetID = this.currentDataset.id;
      this.datasets[datasetID] = this.currentDataset;
      this.writeDatasetsToFile();
    },
    async updateCurrentDataset(dataset) {
      try {
        this.currentDataset = dataset;
      } catch (error) {
        console.log(error);
      }
    },
    async getCurrentDataset() {
      return this.currentDataset;
    },
    getDataset(datasetID) {
      if (datasetID in this.datasets) {
        this.currentDataset = this.datasets[datasetID];
        return this.currentDataset;
      } else {
        return "NO_DATASET_FOUND";
      }
    },
  },
});
