"use strict";

import fs from "fs-extra";
import path from "path";
import { app } from "@electron/remote";
import { defineStore } from "pinia";

const USER_PATH = app.getPath("home");
const CONFIG_STORE_PATH = path.join(
  USER_PATH,
  ".sodaforcovid19research",
  "config.json"
);

// function to create the dataset store file in the user path
const createFile = async () => {
  fs.ensureFileSync(CONFIG_STORE_PATH);
  fs.writeJsonSync(CONFIG_STORE_PATH, {});
};

// function to load the dataset file into the store.
const loadFile = async () => {
  const exists = await fs.pathExists(CONFIG_STORE_PATH);

  if (!exists) {
    createFile();
    return {};
  } else {
    try {
      let config = fs.readJsonSync(CONFIG_STORE_PATH);
      return config;
    } catch (err) {
      console.error(err);
      return {};
    }
  }
};

export const useConfigStore = defineStore({
  id: "ConfigStore",
  state: () => ({
    config: {},
  }),

  actions: {
    async loadConfig() {
      try {
        const config = await loadFile();
        this.config = config;
      } catch (error) {
        console.error(error);
      }
    },
    async getConfig() {
      return this.config;
    },
    async writeConfigToFile() {
      fs.ensureFileSync(CONFIG_STORE_PATH);
      fs.writeJsonSync(CONFIG_STORE_PATH, this.config);
    },
    async addConfig(key, value) {
      try {
        this.config[key] = value;
        this.writeConfigToFile();
      } catch (error) {
        console.log(error);
      }
    },
    async deleteConfig(key) {
      try {
        delete this.config[key];
        this.writeConfigToFile();
      } catch (error) {
        console.log(error);
      }
    },
    async syncConfig() {
      this.writeConfigToFile();
    },
  },
});
