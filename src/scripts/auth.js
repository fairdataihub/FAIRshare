import { BrowserWindow, ipcMain } from "electron";
import axios from "axios";
const nodeUrl = require("url");

const CLIENT_ID = process.env.VUE_APP_GITHUB_OAUTH_CLIENT_ID;
const CLIENT_SECRET = process.env.VUE_APP_GITHUB_OAUTH_CLIENT_SECRET;

function retrieveCode(url) {
  return new Promise(function (resolve, reject) {
    let authWindow = new BrowserWindow({
      width: 800,
      height: 600,
      show: false,
      "node-integration": false,
      "web-security": false,
    });

    authWindow.loadURL(url, { userAgent: "Chrome" });
    authWindow.show();
    authWindow.on("closed", () => {
      reject(new Error("closed"));
    });

    function newlink(url) {
      let parsedURL = nodeUrl.parse(url, true);
      let query = parsedURL.query;
      let code = query.code;
      let error = query.error;

      //   console.log("parsed: ", parsedURL);

      if (error) {
        reject(error);
        authWindow.removeAllListeners("closed");

        setImmediate(function () {
          authWindow.close();
        });
      } else if (code) {
        resolve(code);
        authWindow.removeAllListeners("closed");

        setImmediate(function () {
          authWindow.close();
        });
      }
    }

    // probabaly needs to add an additional listener to make zenodo oauth working
    // see here https://www.electronjs.org/docs/latest/api/web-contents
    authWindow.webContents.on("will-navigate", (_event, url) => {
      console.log("will-navigate", url);
      newlink(url);
    });

    authWindow.webContents.on("did-get-redirect-request", (_event, _oldUrl, newUrl) => {
      console.log("did-get-redirect-request");
      newlink(newUrl);
    });
  });
}

ipcMain.on("OAuth-Github", async (_event, _test) => {
  // console.log(test)
  let success = false;

  await axios
    .get("https://github.com/login/oauth/authorize", {
      params: {
        client_id: CLIENT_ID,
        scope: "repo admin:repo_hook admin:org_hook user",
      },
    })
    .then(async (responseCode) => {
      let authUrl = responseCode.request.res.responseUrl;

      await retrieveCode(authUrl).then(async (code) => {
        // console.log("code:", code);
        await axios
          .post(
            "https://github.com/login/oauth/access_token",
            {
              client_id: CLIENT_ID,
              client_secret: CLIENT_SECRET,
              code: code,
            },
            {
              headers: {
                Accept: "application/json",
              },
            }
          )
          .then(async (response) => {
            // console.log("response after code: ", response.data.access_token);

            // eslint-disable-next-line no-undef
            mainWindow.webContents.send("OAuth-Github-Reply", response.data.access_token);
            success = true;
          })
          .catch((error) => {
            console.log("request token error: ", error);
          });
      });
    })
    .catch((error) => {
      console.log("request code error: ", error);
    });
  if (!success) {
    // eslint-disable-next-line no-undef
    mainWindow.webContents.send("OAuth-Github-Reply", "failed");
  }

  // eslint-disable-next-line no-undef
  mainWindow.webContents.session.clearStorageData();
});

ipcMain.on("OAuth-Zenodo", async (_event, _test) => {
  // console.log(test)
  // complete this part to make zenodo oauth working
  // api calls are given at the buttom of your zenodo app page
  let success = false;
  const CLIENT_ID_ZENODO = "";
  const CLIENT_SECRET_ZENODO = "";

  await axios
    .get("https://sandbox.zenodo.org/oauth/authorize", {
      params: {
        client_id: CLIENT_ID_ZENODO,
        response_type: "code",
        redirect_uri: "http://localhost:8080",
        scope: "deposite:write deposite:actions",
      },
    })
    .then(async (responseCode) => {
      //   console.log("code:", responseCode.request.res.responseUrl);
      let authUrl = responseCode.request.res.responseUrl;
      await retrieveCode(authUrl).then(async (code) => {
        // console.log("code:", code);
        await axios
          .post(
            "https://sandbox.zenodo.org/oauth/token",
            {
              client_id: CLIENT_ID_ZENODO,
              client_secret: CLIENT_SECRET_ZENODO,
              grant_type: "authorization_code",
              code: code,
            },
            {
              headers: {
                Accept: "application/json",
              },
            }
          )
          .then(async (response) => {
            // console.log("response after code: ", response.data.access_token);

            // eslint-disable-next-line no-undef
            mainWindow.webContents.send("OAuth-Zenodo-Reply", response.data.access_token);
            success = true;
          })
          .catch(() => {
            console.log("request token error: ");
          });
      });
    })
    .catch(() => {
      console.log("request code error: ");
    });
  if (!success) {
    // eslint-disable-next-line no-undef
    mainWindow.webContents.send("OAuth-Zenodo-Reply", "failed");
  }

  // eslint-disable-next-line no-undef
  mainWindow.webContents.session.clearStorageData();
});
