"use strict";

import fs from "fs-extra";
import path from "path";
import { app } from "@electron/remote";
import { defineStore } from "pinia";
import CryptoJS from "crypto-js";
import axios from "axios";

const USER_PATH = app.getPath("home");
const TOKEN_STORE_PATH = path.join(USER_PATH, ".fairshare", "accessTokens.json");

// will change to use an actual secret key
const SECRET_KEY = process.env.VUE_APP_ENCRYPTION_KEY;

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

    async getToken(key) {
      if (key in this.accessTokens) {
        const tokenObject = Object.assign({}, this.accessTokens[key]);
        tokenObject.token = await decrypt(this.accessTokens[key].token);
        return tokenObject;
      } else {
        return "NO_TOKEN_FOUND";
      }
    },

    async deleteToken(key) {
      delete this.accessTokens[key];
      await this.syncTokens();
    },

    async verifyZenodoTokenByDepositions(token) {
      return await axios
        .get(`${process.env.VUE_APP_ZENODO_SERVER_URL}/deposit/depositions`, {
          params: {
            access_token: token,
          },
        })
        .then((response) => {
          return { data: response.data, status: response.status };
        })
        .catch((error) => {
          return { data: error.response, status: error.response.status };
        });
    },

    async verifyZenodoToken(token) {
      const response = await this.verifyZenodoTokenByDepositions(token);
      if (response.status === 200) {
        return true;
      } else if (response.status === 401) {
        return false;
      } else {
        return false;
      }
    },

    async verifyZenodoConnection() {
      const tokenObject = await this.getToken("zenodo");

      if (tokenObject === "NO_TOKEN_FOUND") {
        return false;
      } else {
        const token = tokenObject.token;

        const response = await this.verifyZenodoToken(token);

        return response;
      }
    },

    async verifyGithubTokenByTokenConnection(token) {
      return await axios
        .get(`${process.env.VUE_APP_GITHUB_SERVER_URL}/rate_limit`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then((response) => {
          return { data: response.data, status: response.status };
        })
        .catch((error) => {
          return { data: error.response.data, status: error.response.status };
        });
    },

    async verifyGithubToken(token) {
      const response = await this.verifyGithubTokenByTokenConnection(token);
      if (response.status === 200) {
        return true;
      } else if (response.status === 401) {
        return false;
      } else {
        return false;
      }
    },

    async verifyGithubTokenScopeByTokenConnection(token) {
      return await axios
        .get(`${process.env.VUE_APP_GITHUB_SERVER_URL}`, {
          headers: {
            Authorization: `token ${token}`,
          },
        })
        .then((response) => {
          return { scope: response.headers["x-oauth-scopes"] };
        })
        .catch((error) => {
          console.log(error);
          return "Error Found";
        });
    },

    async verifyGithubTokenScope(token) {
      const scope = ["admin:org_hook", "admin:repo_hook", "repo", "user"];
      const response = await this.verifyGithubTokenScopeByTokenConnection(token);
      if (response != "Error Found") {
        if (scope.every((item) => response.scope.includes(item))) {
          return true;
        } else {
          return false;
        }
      } else {
        return false;
      }
    },

    async verifyGithubConnection() {
      const tokenObject = await this.getToken("github");

      if (tokenObject === "NO_TOKEN_FOUND") {
        return false;
      } else {
        const token = tokenObject.token;

        const response = await this.verifyGithubToken(token);

        return response;
      }
    },

    async getGithubUser(token) {
      let response = await axios
        .get(`${process.env.VUE_APP_GITHUB_SERVER_URL}/user`, {
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
        return "No user found";
      }
    },

    async verifyAllConnections() {
      this.verifyZenodoConnection();
      this.verifyGithubConnection();
    },

    // github operations
    async githubAPI_listCurrentRepoBranches(token, repo, owner) {
      // return both repo names and repo full names
      let response = await axios
        .get(`${process.env.VUE_APP_GITHUB_SERVER_URL}/repos/` + owner + `/` + repo + `/branches`, {
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
      return response.data;
    },

    async githubAPI_getTreeFromRepo(token, repo, owner, branch) {
      let response = await axios
        .get(
          `${process.env.VUE_APP_GITHUB_SERVER_URL}/repos/` +
            owner +
            `/` +
            repo +
            `/git/trees/` +
            branch +
            `?recursive=1`,
          {
            headers: {
              Authorization: `token ${token}`,
            },
          }
        )
        .then((response) => {
          return { data: response.data, status: response.status };
        })
        .catch((error) => {
          return { data: error.response.data, status: error.response.status };
        });
      return response.data;
    },
    async githubAPI_getRepoAtPageK(token, k) {
      let response = await axios
        .get(`${process.env.VUE_APP_GITHUB_SERVER_URL}/user/repos`, {
          params: {
            accept: "application/vnd.github.v3+json",
            per_page: 10,
            page: k,
          },
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
      return response.data;
    },
    async githubAPI_getAllRepo(token) {
      if (await this.verifyGithubToken(token)) {
        let k = 1;
        let result = [""];
        let allResult = [];
        while (result.length != 0) {
          result = await this.githubAPI_getRepoAtPageK(token, k);
          allResult = allResult.concat(result);
          k += 1;
        }
        return allResult;
      } else {
        console.error("token is invalid");
        return [];
      }
    },
  },
});
