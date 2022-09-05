"use strict";

import { app, protocol, BrowserWindow, ipcMain, Menu, shell, dialog } from "electron";
import { enable as enableWebContents } from "@electron/remote/main";
import { createProtocol } from "vue-cli-plugin-electron-builder/lib";
import { autoUpdater } from "electron-updater";
import installExtension, { VUEJS3_DEVTOOLS } from "electron-devtools-installer";

import axios from "axios";
import uniqid from "uniqid";

import menuTemplate from "./scripts/menu";
import "./scripts/utilities";
import "./scripts/auth";
import "./scripts/dialogs";

const fp = require("find-free-port");
const fs = require("fs-extra");
const path = require("path");
const log = require("electron-log");
const nodeUrl = require("url");

const USER_PATH = app.getPath("home");
const CONFIG_STORE_PATH = path.join(USER_PATH, ".fairshare", "config.json");

const SESSION_ID = uniqid();

log.transports.file.resolvePath = () => path.join(USER_PATH, ".fairshare", "logs", "app.log");
log.transports.console.format = "{h}:{i}:{s} {text}";

log.info("starting log");

if (process.platform === 'win32') {
  app.setAppUserModelId(app.name);
}

const getReleaseChannel = () => {
  const exists = fs.pathExistsSync(CONFIG_STORE_PATH);

  if (!exists) {
    return "latest";
  } else {
    try {
      let config = fs.readJsonSync(CONFIG_STORE_PATH);
      if ("releaseChannel" in config) {
        if (config.releaseChannel == "beta") {
          return "beta";
        } else {
          return "latest";
        }
      }
    } catch (err) {
      console.error(err);
      return "latest";
    }
  }
};

const updateChannel = getReleaseChannel();

autoUpdater.channel = updateChannel;
autoUpdater.logger = require("electron-log");
autoUpdater.logger.transports.file.level = "info";

const isDevelopment = process.env.NODE_ENV !== "production";

require("@electron/remote/main").initialize();

// Scheme must be registered before the app is ready
protocol.registerSchemesAsPrivileged([
  { scheme: "app", privileges: { secure: true, standard: true } },
]);

const PY_FOLDER = "pyflask";
const PY_MODULE = "api";
let mainWindow;

let pyProc = null;
let pyPort = null;

global.PY_PORT = pyPort;

const startingPort = 7632;
const portRange = 100;

const guessPackaged = () => {
  const unixPath = path.join(process.resourcesPath, PY_MODULE);
  const winPath = path.join(process.resourcesPath, PY_MODULE + ".exe");

  return require("fs").existsSync(unixPath) || require("fs").existsSync(winPath);
};

// check if the python dist folder exists
const getScriptPath = () => {
  if (!guessPackaged()) {
    return path.join(__dirname, PY_FOLDER, PY_MODULE + ".py");
  }

  if (process.platform === "win32") {
    return path.join(process.resourcesPath, PY_MODULE + ".exe");
  }

  return path.join(process.resourcesPath, PY_MODULE);
};

const killAllPreviousProcesses = async () => {
  console.log("Killing all previous processes");

  // kill all previous python processes that could be running.
  let promisesArray = [];

  // create a loop of 100
  for (let i = 0; i < portRange; i++) {
    promisesArray.push(
      axios.post(`http://127.0.0.1:${startingPort + i}/fairshare_server_shutdown`, {})
    );
  }

  // wait for all the promises to resolve
  await Promise.allSettled(promisesArray);
};

// create the python process
const createPyProc = async () => {
  let script = getScriptPath();

  await killAllPreviousProcesses();

  fp(startingPort, startingPort + portRange)
    .then(([freeport]) => {
      console.log(`Found a free port at ${freeport}. Using port ${freeport} for python process.`);
      pyPort = freeport;
      global.PY_PORT = pyPort;

      console.log(`Starting python process at ${script}`);
      console.log(`API documentation hosted at http://127.0.0.1:${pyPort}/docs`);
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
    })
    .catch((err) => {
      console.error(err);
    });
};

// Set up a custom protocol handler for the fairshare:// protocol.
if (process.defaultApp) {
  if (process.argv.length >= 2) {
    app.setAsDefaultProtocolClient("fairshare", process.execPath, [path.resolve(process.argv[1])]);
  }
} else {
  app.setAsDefaultProtocolClient("fairshare");
}

// We should prevent the user from running multiple instances of the app.
const gotTheLock = app.requestSingleInstanceLock();

if (!gotTheLock) {
  app.quit();
} else {
  app.on("second-instance", (_event, args, _workingDirectory) => {
    if (process.platform !== "darwin") {
      // Find the arg that is our custom protocol url and store it
      const deepLinkedUrl = args.find((arg) => arg.startsWith("fairshare://"));

      getAuthUrl(deepLinkedUrl);
    }

    // Someone tried to run a second instance, we should focus our window.
    if (mainWindow) {
      if (mainWindow.isMinimized()) mainWindow.restore();
      mainWindow.focus();
    }
  });
}

// Set the default menu of the application
const menu = Menu.buildFromTemplate(menuTemplate);
Menu.setApplicationMenu(menu);

async function createWindow() {
  // Create the browser window.
  console.log(path.join(__dirname, "Icon.png"));

  mainWindow = new BrowserWindow({
    width: 1200,
    height: 850,
    minWidth: 1200,
    minHeight: 850,
    icon: path.join(__dirname, "Icon.png"),
    show: false,
    webPreferences: {
      // Use pluginOptions.nodeIntegration, leave this alone
      // See nklayman.github.io/vue-cli-plugin-electron-builder/guide/security.html#node-integration for more info
      nodeIntegration: process.env.ELECTRON_NODE_INTEGRATION,
      contextIsolation: !process.env.ELECTRON_NODE_INTEGRATION,
      // nodeIntegration: false,
      // contextIsolation: true,
      enableRemoteModule: true,
      preload: path.join(__dirname, "preload.js"),
    },
  });

  // splash screen

  const splash = new BrowserWindow({
    width: 500,
    height: 500,
    frame: false,
    show: true,
    icon: path.join(__dirname, "Icon.png"),
    alwaysOnTop: true,
    transparent: true,
    hasShadow: false,
    resizable: false,
    movable: false,
  });
  splash.loadURL(path.join("file://", __dirname, "/splash-screen.html"));

  // splash screen end

  mainWindow.once("ready-to-show", () => {
    setTimeout(function () {
      splash.close();
      mainWindow.show();
    }, 500);
  });

  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    console.log("Intercepting new browser tab/window", url);

    return {
      action: "allow",
      overrideBrowserWindowOptions: {
        frame: true,
        fullScreenable: true,
        backgroundColor: "white",
        webPreferences: {
          allowRunningInsecureContent: false,
          contextIsolation: true,
          devTools: false,
          disableDialogs: true,
          enableRemoteModule: false,
          experimentalFeatures: false,
          nodeIntegration: false,
          nodeIntegrationInWorker: false,
          nodeIntegrationInSubFrames: false,
          plugins: false,
          sandbox: true,
          webSecurity: true,
        },
      },
    };
  });

  enableWebContents(mainWindow.webContents);

  if (process.env.WEBPACK_DEV_SERVER_URL) {
    // Load the url of the dev server if in development mode
    await mainWindow.loadURL(process.env.WEBPACK_DEV_SERVER_URL);

    if (!process.env.IS_TEST) {
      console.log("Opening dev tools");

      mainWindow.webContents.openDevTools({ mode: "detach" });
    }
  } else {
    console.log(`Registering the 'app' protocol...`);
    createProtocol("app");

    // Load the index.html when not in development
    mainWindow.loadURL("app://./index.html");
  }
}

// Close the webserver process on app exit
const exitPyProc = async (main_pid) => {
  console.log("killing python process...");

  await killAllPreviousProcesses();

  if (process.platform == "darwin" || process.platform == "linux") {
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

// Quit when all windows are closed.
app.on("window-all-closed", () => {
  // clean up - remove the custom protocol handler
  app.removeAsDefaultProtocolClient("fairshare");

  // This might need to be moved into the `will-quit` event. Would need some checking on app updates.
  exitPyProc(process.pid).then(() => {
    app.quit();
  });

  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  // if (process.platform !== "darwin") {
  //   app.quit();
  // }
});

app.on("activate", () => {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (BrowserWindow.getAllWindows().length === 0) createWindow();
});

// This will catch clicks on links such as <a href="fairshare://abc=1">open in foobar</a>
// Protocol handler for macOS
app.on("open-url", (event, deepLinkedUrl) => {
  event.preventDefault();
  console.log("deepLinkingUrl", deepLinkedUrl);

  getAuthUrl(deepLinkedUrl);
});

ipcMain.on("fairshare-auth", async (_event, app) => {
  // adding a session ID to the auth url to prevent unauthorized requests
  const authUrl = `https://auth.fairshareapp.io/${app}?session=${SESSION_ID}`;

  shell.openExternal(authUrl);
});

const getAuthUrl = async (deepLinkedUrl) => {
  let url;
  try {
    url = new URL(deepLinkedUrl);
  } catch (e) {
    return;
  }

  const query = url.searchParams;

  const session_id = query.get("session");

  if (!session_id || (session_id && session_id !== SESSION_ID)) {
    dialog.showErrorBox(
      "Unauthorized request",
      "This request did not originate from FAIRshare. An unauthorized app tried to open FAIRshare from your browser. Please contact the FAIRshare team if you think this is a mistake."
    );

    return;
  }

  if (url && url.protocol === "fairshare:") {
    if (url.hostname === "auth-github") {
      const token = query.get("token");

      mainWindow.webContents.send("github-auth-token", token);
    }

    if (url.hostname === "auth-zenodo") {
      const token = query.get("token");
      const refresh_token = query.get("refresh_token");

      mainWindow.webContents.send("zenodo-auth-token", token, refresh_token);
    }

    if (url.hostname === "auth-figshare") {
      const token = query.get("token");
      const refresh_token = query.get("refresh_token");

      mainWindow.webContents.send("figshare-auth-token", token, refresh_token);
    }
  }
};

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

  // Check if the current app has the lock instance
  if (gotTheLock) {
    createPyProc();
    createWindow();
  }
});

autoUpdater.on("update-available", () => {
  mainWindow.webContents.send("update-available", true);
  log.info("update_available");
});

autoUpdater.on("update-downloaded", () => {
  log.info("update_downloaded");
  mainWindow.webContents.send("update-downloaded", true);
});

ipcMain.on("check-for-updates", async (_event, channel = "") => {
  // Check for app updates
  if (channel !== "") {
    autoUpdater.channel = channel;
  }
  autoUpdater.checkForUpdatesAndNotify();
});

ipcMain.on("restart-fairshare-for-update", (_event) => {
  exitPyProc(process.pid).then(() => {
    const isSilent = true;
    const isForceRunAfter = true;
    autoUpdater.quitAndInstall(isSilent, isForceRunAfter);
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

    function newLink(url) {
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

    // probably needs to add an additional listener to make zenodo oauth working
    // see here https://www.electronjs.org/docs/latest/api/web-contents
    authWindow.webContents.on("will-navigate", (_event, url) => {
      console.log("will-navigate", url);
      newLink(url);
    });

    authWindow.webContents.on("did-get-redirect-request", (_event, _oldUrl, newUrl) => {
      console.log("did-get-redirect-request");
      newLink(newUrl);
    });
  });
}

ipcMain.on("OAuth-Zenodo", async (_event, _test) => {
  // complete this part to make zenodo oauth working
  // api calls are given at the bottom of your zenodo app page
  let success = false;
  const CLIENT_ID_ZENODO = "";
  const CLIENT_SECRET_ZENODO = "";

  await axios
    .get("https://sandbox.zenodo.org/oauth/authorize", {
      params: {
        client_id: CLIENT_ID_ZENODO,
        response_type: "code",
        redirect_uri: "http://localhost:8080",
        scope: "deposit:write deposit:actions",
      },
    })
    .then(async (responseCode) => {
      let authUrl = responseCode.request.res.responseUrl;
      await retrieveCode(authUrl).then(async (code) => {
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
    mainWindow.webContents.send("OAuth-Zenodo-Reply", "failed");
  }

  mainWindow.webContents.session.clearStorageData();
});
