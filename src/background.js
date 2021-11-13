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
    width: 1022,
    height: 600,
    minWidth: 1022,
    minHeight: 600,
    webPreferences: {
      // Use pluginOptions.nodeIntegration, leave this alone
      // See nklayman.github.io/vue-cli-plugin-electron-builder/guide/security.html#node-integration for more info
      nodeIntegration: process.env.ELECTRON_NODE_INTEGRATION,
      contextIsolation: !process.env.ELECTRON_NODE_INTEGRATION,
      enableRemoteModule: true,
      preload: path.join(__dirname, "preload.js"),
    },
  });

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
  console.log("opening link", link);
  shell.openExternal("https://google.com").then(() => {
    console.log("hello");
  });
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
