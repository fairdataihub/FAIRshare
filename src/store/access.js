"use strict";

import fs from "fs-extra";
import path from "path";
import { app } from "@electron/remote";
import { defineStore } from "pinia";
import CryptoJS from "crypto-js";
import axios from "axios";

const USER_PATH = app.getPath("home");
const TOKEN_STORE_PATH = path.join(
  USER_PATH,
  ".sodaforcovid19research",
  "accessTokens.json"
);
const CONNECTION_STATUS_PATH = path.join(
  USER_PATH,
  ".sodaforcovid19research",
  "connectionStatus.json"
);

// will change to use an actual secret key
const SECRET_KEY = "TEST_SECRET_KEY";

const encrypt = async (plainToken) => {
  return CryptoJS.AES.encrypt(plainToken, SECRET_KEY).toString();
};

const decrypt = async (ciphertext) => {
  const bytes = CryptoJS.AES.decrypt(ciphertext, SECRET_KEY);
  return bytes.toString(CryptoJS.enc.Utf8);
};

// function to create the dataset store file in the user path
const createFile = async () => {
  fs.ensureFileSync(TOKEN_STORE_PATH);
  fs.writeJsonSync(TOKEN_STORE_PATH, {});
};

const loadFile = async () => {
  const exists = await fs.pathExists(TOKEN_STORE_PATH);

  if (!exists) {
    createFile();
    return {};
  } else {
    try {
      let allTokens = fs.readJsonSync(TOKEN_STORE_PATH);
      return allTokens;
    } catch (err) {
      console.error(err);
      return {};
    }
  }
};

const loadStatusFile = async () => {
  const exists = await fs.pathExists(CONNECTION_STATUS_PATH);

  if (!exists) {
    createFile();
    return {};
  } else {
    try {
      let allStatus = fs.readJsonSync(CONNECTION_STATUS_PATH);
      return allStatus;
    } catch (err) {
      console.error(err);
      return {};
    }
  }
};

const converter = { false: false, true: true };

export const useTokenStore = defineStore({
  id: "TokenStore",
  state: () => ({
    accessTokens: {},
    connnectionStatus: {
      // "zenodoTokenConnected": false,
      // "githubTokenConnected": false,
      // "githubOAuthConnected": false
    },
  }),
  actions: {
    async getGithubTokenConnected() {
      await this.loadStatus();
      //console.log("this.connnectionStatus: ", this.connnectionStatus, "githubTokenConnected" in this.connnectionStatus)
      if ("githubTokenConnected" in this.connnectionStatus) {
        let result = this.connnectionStatus["githubTokenConnected"];
        result = await decrypt(result);
        return converter[result];
      } else {
        return false;
      }
    },
    confirmGithubTokenConnected() {
      this.saveStatus("githubTokenConnected", "true");
    },
    confirmGithubTokenDisconnected() {
      this.saveStatus("githubTokenConnected", "false");
    },
    async loadStatus() {
      try {
        this.connnectionStatus = await loadStatusFile();
      } catch (error) {
        console.error(error);
      }
    },
    async loadTokens() {
      try {
        this.accessTokens = await loadFile();
      } catch (error) {
        console.error(error);
      }
      return Object.keys(this.accessTokens);
    },
    // save an encrypted version of the token in the store also save it to the file.
    async saveToken(key, tokenObject) {
      tokenObject.token = await encrypt(tokenObject.token);
      this.accessTokens[key] = tokenObject;
      await this.syncTokens();
    },
    async writeDatasetsToFile() {
      fs.ensureFileSync(TOKEN_STORE_PATH);
      fs.writeJsonSync(TOKEN_STORE_PATH, this.accessTokens);
    },
    async syncTokens() {
      this.writeDatasetsToFile();
    },

    async saveStatus(key, status) {
      let encryptedStatus = await encrypt(status);
      this.connnectionStatus[key] = encryptedStatus;
      await this.syncStatus();
    },
    async writeStatusToFile() {
      fs.ensureFileSync(CONNECTION_STATUS_PATH);
      fs.writeJsonSync(CONNECTION_STATUS_PATH, this.connnectionStatus);
    },
    async syncStatus() {
      this.writeStatusToFile();
    },

    // decrypt the token and return it
    async getToken(key) {
      //await this.loadTokens()
      if (key in this.accessTokens) {
        const tokenObject = Object.assign({}, this.accessTokens[key]);
        console.log("Old object: ", this.accessTokens[key]);
        tokenObject.token = await decrypt(this.accessTokens[key].token);
        console.log("new Object: ", this.accessTokens[key]);
        return tokenObject;
      } else {
        return "NO_TOKEN_FOUND";
      }
    },

    async deleteToken(key) {
      delete this.accessTokens[key];
      await this.syncTokens();
    },

    async getDepositions(token) {
      return await axios
        .get(`${process.env.VUE_APP_ZENODO_SERVER_URL}deposit/depositions`, {
          params: {
            access_token: token,
          },
        })
        .then((response) => {
          return { data: response.data, status: response.status };
        })
        .catch((error) => {
          return { data: error.response.data, status: error.response.status };
        });
    },

    async checkZenodoToken(token) {
      const response = await this.getDepositions(token);
      console.log("************** ****", response);
      if (response.status === 200) {
        return true;
      } else if (response.status === 401) {
        return false;
      } else {
        return false;
      }
    },

    async verifyGithub(token) {
      return await axios
        .get(`${process.env.VUE_APP_GITHUB_SERVER_URL}`, {
          headers: {
            Authorization: `token ${token}`,
          },
        })
        .then((response) => {
          return { data: response.data, status: response.status };
        })
        .catch((error) => {
          return { data: error.response.data, status: error.response.status };
        });
    },

    async checkGithubToken(token) {
      const response = await this.verifyGithub(token);
      if (response.status === 200) {
        return true;
      } else if (response.status === 401) {
        return false;
      } else {
        return false;
      }
    },

    async getGithubUser(key) {
      const tokenObject = await this.getToken(key);
      const token = tokenObject.token;
      console.log("??: ", token);
      let response = await axios
        .get(`${process.env.VUE_APP_GITHUB_SERVER_URL}user`, {
          headers: {
            Authorization: `token ${token}`,
          },
        })
        .then((response) => {
          return { data: response.data, status: response.status };
        })
        .catch((error) => {
          return { data: error.response.data, status: error.response.status };
        });

      if (response.status === 200) {
        return response.data.login;
      } else if (response.status === 401) {
        return "??";
      }
    },

    async getZenodoUser() {
      return "";
    },
  },
});
