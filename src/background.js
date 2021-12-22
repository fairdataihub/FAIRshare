"use strict";

import { app, protocol, BrowserWindow, ipcMain, shell } from "electron";
import { enable as enableWebContents } from "@electron/remote/main";
import { createProtocol } from "vue-cli-plugin-electron-builder/lib";
import { autoUpdater } from "electron-updater";
import installExtension, { VUEJS3_DEVTOOLS } from "electron-devtools-installer";

const log = require("electron-log");
log.info("starting log");
autoUpdater.logger = require("electron-log");
autoUpdater.logger.transports.file.level = "info";

const isDevelopment = process.env.NODE_ENV !== "production";
const path = require("path");

require("@electron/remote/main").initialize();
// require("@electron/remote/main").enable(webContents);

// Scheme must be registered before the app is ready
protocol.registerSchemesAsPrivileged([
  { scheme: "app", privileges: { secure: true, standard: true } },
]);

// const PY_DIST_FOLDER = "pyflaskdist";
const PY_FOLDER = "pyflask";
const PY_MODULE = "api";
let mainWindow;

let pyProc = null;
const pyPort = "7632";

const guessPackaged = () => {
  const unixPath = path.join(process.resourcesPath, PY_MODULE);
  const winPath = path.join(process.resourcesPath, PY_MODULE + ".exe");

  if (require("fs").existsSync(unixPath) || require("fs").existsSync(winPath)) {
    return true;
  } else {
    return false;
  }
};

// check if the python dist folder exists
const getScriptPath = () => {
  if (!guessPackaged()) {
    return path.join(__dirname, PY_FOLDER, PY_MODULE + ".py");
  }

  if (process.platform === "win32") {
    log.info(path.join(process.resourcesPath, PY_MODULE + ".exe"));
    return path.join(process.resourcesPath, PY_MODULE + ".exe");
  }

  return path.join(process.resourcesPath, PY_MODULE);
};

// create the python process
const createPyProc = () => {
  let script = getScriptPath();

  console.log(`Starting python process at ${script}`);
  console.log(`API documentation hosted at http://127.0.0.1:7632/docs`);
  if (guessPackaged()) {
    pyProc = require("child_process").execFile(script, [pyPort], {
      stdio: "ignore",
    });
  } else {
    pyProc = require("child_process").spawn("python", [script, pyPort], {
      stdio: "ignore",
    });
  }

  if (pyProc != null) {
    console.log("child process success on port " + pyPort);
  } else {
    console.error("child process failed to start on port" + pyPort);
  }
};

async function createWindow() {
  // Create the browser window.
  mainWindow = new BrowserWindow({
    width: 1069,
    height: 600,
    minWidth: 1069,
    minHeight: 600,
    show: false,
    webPreferences: {
      // Use pluginOptions.nodeIntegration, leave this alone
      // See nklayman.github.io/vue-cli-plugin-electron-builder/guide/security.html#node-integration for more info
      nodeIntegration: process.env.ELECTRON_NODE_INTEGRATION,
      contextIsolation: !process.env.ELECTRON_NODE_INTEGRATION,
      enableRemoteModule: true,
      preload: path.join(__dirname, "preload.js"),
    },
  });

  ///// splash screen
  // remove this section if not good.
  // Also remove from the copy-files script from package.json

  const splash = new BrowserWindow({
    width: 1022,
    height: 600,
    frame: false,
    icon: __dirname + "/assets/menu-icon/soda_icon.png",
    alwaysOnTop: true,
    transparent: true,
  });
  splash.loadURL(path.join("file://", __dirname, "/splash-screen.html"));

  mainWindow.once("ready-to-show", () => {
    setTimeout(function () {
      splash.close();
      mainWindow.show();
    }, 500);
  });

  ////// splash screen end

  enableWebContents(mainWindow.webContents);

  if (process.env.WEBPACK_DEV_SERVER_URL) {
    // Load the url of the dev server if in development mode
    await mainWindow.loadURL(process.env.WEBPACK_DEV_SERVER_URL);
    if (!process.env.IS_TEST) mainWindow.webContents.openDevTools();
  } else {
    createProtocol("app");
    // Load the index.html when not in development
    mainWindow.loadURL("app://./index.html");

    // exitPyProc();
    // Check for updates
    autoUpdater.checkForUpdatesAndNotify();
  }
}

// Close the webserver process on app exit
const exitPyProc = (main_pid) => {
  console.log("killling python process...");
  if ((process.platform == "darwin") | (process.platform == "linux")) {
    pyProc.kill();
    return new Promise(function (resolve) {
      resolve();
    });
  } else {
    const python_script_name = path.basename(getScriptPath());
    let cleanup_completed = false;
    const psTree = require("ps-tree");
    psTree(main_pid, function (_err, children) {
      let python_pids = children
        .filter(function (el) {
          return el.COMMAND == python_script_name;
        })
        .map(function (p) {
          return p.PID;
        });
      // kill all the spawned python processes
      python_pids.forEach(function (pid) {
        process.kill(pid);
      });
      pyProc = null;
      cleanup_completed = true;
    });
    return new Promise(function (resolve) {
      (function waitForSubProcessCleanup() {
        if (cleanup_completed) return resolve();
        setTimeout(waitForSubProcessCleanup, 30);
      })();
    });
  }
};

// app.on("will-quit", () => {
//   exitPyProc();
// });

// Quit when all windows are closed.
app.on("window-all-closed", () => {
  // This might need to be moved into the `will-quit` event. Would need some checking on autoupdates.
  exitPyProc(process.pid).then(() => {
    app.quit();
  });

  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  // if (process.platform !== "darwin") {
  //   app.quit();
  // }
});

// app.on("activate", () => {
//   // On macOS it's common to re-create a window in the app when the
//   // dock icon is clicked and there are no other windows open.
//   if (BrowserWindow.getAllWindows().length === 0) createWindow();
// });

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on("ready", async () => {
  if (isDevelopment && !process.env.IS_TEST) {
    // Install Vue Devtools
    try {
      await installExtension(VUEJS3_DEVTOOLS);
    } catch (e) {
      console.error("Vue Devtools failed to install:", e.toString());
    }
  }
  createPyProc();
  createWindow();
});

autoUpdater.on("update-available", () => {
  mainWindow.webContents.send("update-available", true);
  log.info("update_available");
});

autoUpdater.on("update-downloaded", () => {
  log.info("update_downloaded");
  mainWindow.webContents.send("update-downloaded", true);
  // exitPyProc(process.pid).then(() => {
  // autoUpdater.quitAndInstall();
  // });
});

ipcMain.on("open-link-in-browser", async (_event, link) => {
  shell.openExternal(link).then(() => {
    console.log("opened link", link);
  });
});

// OAuth
//import { useTokenStore } from "./store/access";
import axios from "axios";
const nodeUrl = require("url");
const CLIENT_ID = "3282f35bdcceeb2cc9f8";
const CLIENT_SECRET = "c603c25b557624f5b07cad52c0da798ee7ca4300";

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

    authWindow.webContents.on("will-navigate", (_event, url) => {
      newlink(url);
    });

    authWindow.webContents.on(
      "did-get-redirect-request",
      (_event, _oldUrl, newUrl) => {
        newlink(newUrl);
      }
    );
  });
}
ipcMain.on("OAuth-Github", async (_event, _test) => {
  // console.log(test)
  let success = false;
  await axios
    .get("https://github.com/login/oauth/authorize", {
      params: {
        client_id: CLIENT_ID,
      },
    })
    .then(async (responseCode) => {
      let authUrl = responseCode.request.res.responseUrl;
      await retrieveCode(authUrl).then(async (code) => {
        console.log("code:", code);
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
            console.log("response after code: ", response.data.access_token);
            mainWindow.webContents.send(
              "OAuth-Github-Reply",
              response.data.access_token
            );
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
    mainWindow.webContents.send("OAuth-Github-Reply", "failed");
  }
  mainWindow.webContents.session.clearStorageData();
});

// Exit cleanly on request from parent process in development mode.
if (isDevelopment) {
  if (process.platform === "win32") {
    process.on("message", (data) => {
      if (data === "graceful-exit") {
        app.quit();
      }
    });
  } else {
    process.on("SIGTERM", () => {
      app.quit();
    });
  }
}
