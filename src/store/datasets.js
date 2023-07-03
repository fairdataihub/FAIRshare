"use strict";

import fs from "fs-extra";
import path from "path";
import { app } from "@electron/remote";
import { defineStore } from "pinia";
import semver from "semver";

// const USER_PATH = app.getPath("userData");
// const DATASETS_STORE_PATH = path.join(
//   USER_PATH,
//   "Store",
//   "unpublishedDatasets.json"
// );
const FILE_NAME =
  process.env.NODE_ENV === "development"
    ? "unpublishedDatasets-dev.json"
    : "unpublishedDatasets.json";
const USER_PATH = app.getPath("home");
const DATASETS_STORE_PATH = path.join(USER_PATH, ".fairshare", FILE_NAME);

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
    progressBar: {
      show: false,
      type: "",
      currentStep: 0,
    },
    loading: false,
    sidebarVisible: true,
  }),
  getters: {
    datasetCount: function () {
      const keys = Object.keys(this.datasets);
      let datasetCount = keys.length;

      if (keys.includes("version")) {
        return datasetCount - 1;
      } else {
        return datasetCount;
      }
    },
    // getAllDatasets() {
    //   return this.datasets;
    // },
  },
  actions: {
    async loadDatasets() {
      try {
        const datasets = await loadFile();
        this.datasets = datasets;

        await this.upgradeSavedDatasets();
      } catch (error) {
        console.error(error);
      }
    },
    async loadAndReturnDatasets() {
      try {
        const datasets = await loadFile();

        return datasets;
      } catch (error) {
        return {};
      }
    },
    async writeDatasetsToFile() {
      fs.ensureFileSync(DATASETS_STORE_PATH);
      fs.writeJsonSync(DATASETS_STORE_PATH, this.datasets, {
        spaces: 4,
      });
    },
    async addDataset(dataset, datasetID) {
      try {
        this.datasets[datasetID] = dataset;
        this.currentDataset = dataset;
        await this.writeDatasetsToFile();
      } catch (error) {
        console.log(error);
      }
    },
    async deleteDataset(datasetID) {
      try {
        delete this.datasets[datasetID];
        await this.writeDatasetsToFile();
      } catch (error) {
        console.log(error);
      }
    },
    async syncDatasets() {
      const datasetID = this.currentDataset.id;
      this.datasets[datasetID] = this.currentDataset;
      await this.writeDatasetsToFile();
    },
    async updateCurrentDataset(dataset) {
      try {
        const now = new Date();
        dataset.meta.dateModified = now;
        this.currentDataset = dataset;
      } catch (error) {
        console.log(error);
      }
    },
    async getCurrentDataset() {
      return this.currentDataset;
    },
    async getDataset(datasetID) {
      if (datasetID in this.datasets) {
        this.currentDataset = this.datasets[datasetID];
        return this.currentDataset;
      } else {
        return "NO_DATASET_FOUND";
      }
    },
    async getAllDatasets() {
      return this.loadAndReturnDatasets();
    },
    async getProgressBar() {
      return this.progressBar;
    },
    showProgressBar() {
      this.progressBar.show = true;
    },
    hideProgressBar() {
      this.progressBar.show = false;
    },
    setProgressBarType(type) {
      this.progressBar.type = type;
    },
    setCurrentStep(step) {
      this.progressBar.currentStep = step - 1;
    },
    async showSidebar() {
      console.log("Showing Sidebar");
      this.sidebarVisible = true;
    },
    async hideSidebar() {
      console.log("Hiding Sidebar");
      this.sidebarVisible = false;
    },

    /**
     * Function to upgrade the datasets store to the latest version
     * @returns {Promise<void>}
     */

    async upgradeSavedDatasets() {
      if (!("version" in this.datasets)) {
        this.datasets.version = semver.clean("2.0.0");
      }

      /**
       * Adding code to upgrade datasets incrementally here. This is to ensure
       * that the save datasets are not broken if the user upgrades the app.
       *
       * Refer to https://www.npmjs.com/package/semver for semver syntax
       */

      if (semver.satisfies(this.datasets.version, "1.3.x")) {
        console.log("Upgrading datasets to 1.4.0");

        // for (let dataset of this.datasets) {
        // do something with this
        // }

        this.datasets.version = semver.clean("1.4.0");
        await this.writeDatasetsToFile();
      }

      if (semver.satisfies(this.datasets.version, "1.4.x")) {
        console.log("Upgrading datasets to 2.0.0");

        this.datasets.version = semver.clean("2.0.0");
        await this.writeDatasetsToFile();
      }

      await this.writeDatasetsToFile(); // write the datasets to file

      return;
    },
  },
});
