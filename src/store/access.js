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

export const useTokenStore = defineStore({
  id: "TokenStore",
  state: () => ({
    accessTokens: {},
  }),
  actions: {
    async loadTokens() {
      try {
        this.accessTokens = await loadFile();
      } catch (error) {
        console.error(error);
      }
    },
    // save an encrypted version of the token in the store also save it to the file.
    async saveToken(key, value) {
      this.accessTokens[key] = await encrypt(value);
      await this.syncTokens();
    },
    async writeDatasetsToFile() {
      fs.ensureFileSync(TOKEN_STORE_PATH);
      fs.writeJsonSync(TOKEN_STORE_PATH, this.accessTokens);
    },
    async syncTokens() {
      this.writeDatasetsToFile();
    },
    // decrypt the token and return it
    async getToken(key) {
      if (key in this.accessTokens) {
        return await decrypt(this.accessTokens[key]);
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
      if (response.status === 200) {
        return true;
      } else if (response.status === 401) {
        return false;
      } else {
        return false;
      }
    },

    async getGithubUser(token) {
      return await axios.get(`${process.env.VUE_APP_GITHUB_SERVER_URL}user`, {
        headers: {
          'Authorization': `token ${token}`
        }
      })
        .then((response) => {
          return { data: response.data, status: response.status };
        })
        .catch((error) => {
          return { data: error.response.data, status: error.response.status };
        })
    },

    async checkGithubToken(token) {
      const response = await this.getGithubUser(token);
      if (response.status === 200) {
        return true;
      } else if (response.status === 401) {
        return false;
      } else {
        return false;
      }
    },
  },
});
