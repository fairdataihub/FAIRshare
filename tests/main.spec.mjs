import { expect, test } from "@playwright/test";
import {
  // clickMenuItemById,
  // ipcMainCallFirstListener,
  // ipcRendererCallFirstListener,
  parseElectronApp,
} from "electron-playwright-helpers";
// import jimp from "jimp";
import path from "path";
import axiosRetry from "axios-retry";
import axios from "axios";
import { _electron as electron } from "playwright";
import { exit } from "process";

let electronApp;

test.beforeAll(async () => {
  /**
   * Find the latest build in the dist_electron directory
   * Currently this test runner has only been setup for windows
   *
   * @returns {string} The path to the latest build
   */
  const latestBuild = path.join(process.cwd(), "dist_electron", "win-unpacked", "FAIRshare.exe");

  // parse the directory and find paths and other info
  const appInfo = parseElectronApp(latestBuild);

  // set the CI environment variable to true
  process.env.CI = "e2e";

  electronApp = await electron.launch({
    args: [appInfo.main],
    executablePath: appInfo.executable,
  });

  const client = axios.create({ baseURL: `http://127.0.0.1:7632` });
  axiosRetry(client, { retries: 10 });

  await client
    .get("/echo", {
      "axios-retry": {
        retries: 10,
        retryDelay: axiosRetry.exponentialDelay,
      },
    })
    .then((echo_response) => {
      console.log("echo_response:", echo_response.data);
    })
    .catch((error) => {
      console.error(error);
      exit();
    });

  electronApp.on("window", async (page) => {
    const filename = page.url()?.split("/").pop();
    console.log(`Window opened: ${filename}`);

    // capture errors
    page.on("pageerror", (error) => {
      console.error(error);
    });
    // capture console messages
    page.on("console", (msg) => {
      console.log(msg.text());
    });
  });
});

test.afterAll(async () => {
  await electronApp.close();
});

let page;

test("renders the first page", async () => {
  page = await electronApp.firstWindow();
  await page.waitForSelector("h2");
  const text = await page.$eval("h2", (el) => el.textContent);
  expect(text.trim()).toBe("Make your biomedical research data and software");
  const title = await page.title();
  expect(title.trim()).toBe(
    "FAIRshare - Make your biomedical research data and software Findable, Accessible, Interoperable, and Reusable (FAIR)"
  );
});

test(`"Getting started" button exists`, async () => {
  expect(await page.$("#getting-started")).toBeTruthy();
});

// test("click the button to open new window", async () => {
//   await page.click("#new-window");
//   const newPage = await electronApp.waitForEvent("window");
//   expect(newPage).toBeTruthy();
//   page = newPage;
// });

// test("window 2 has correct title", async () => {
//   const title = await page.title();
//   expect(title).toBe("Window 2");
// });

// test("trigger IPC listener via main process", async () => {
//   electronApp.evaluate(({ ipcMain }) => {
//     ipcMain.emit("new-window");
//   });
//   const newPage = await electronApp.waitForEvent("window");
//   expect(newPage).toBeTruthy();
//   expect(await newPage.title()).toBe("Window 3");
//   page = newPage;
// });

// test("send IPC message from renderer", async () => {
//   // evaluate this script in render process
//   // requires webPreferences.nodeIntegration true and contextIsolation false
//   await page.evaluate(() => {
//     require("electron").ipcRenderer.send("new-window");
//   });
//   const newPage = await electronApp.waitForEvent("window");
//   expect(newPage).toBeTruthy();
//   expect(await newPage.title()).toBe("Window 4");
//   page = newPage;
// });

// test("receive IPC invoke/handle via renderer", async () => {
//   // evaluate this script in render process and collect the result
//   const result = await page.evaluate(async () => {
//     const { ipcRenderer } = require("electron");
//     return await ipcRenderer.invoke("how-many-windows");
//   });
//   expect(result).toBe(4);
// });

// test("receive synchronous data via ipcRendererCallFirstListener()", async () => {
//   const data = await ipcRendererCallFirstListener(page, "get-sychronous-data");
//   expect(data).toBe("Synchronous Data");
// });

// test("receive asynchronous data via ipcRendererCallFirstListener()", async () => {
//   const data = await ipcRendererCallFirstListener(page, "get-asynchronous-data");
//   expect(data).toBe("Asynchronous Data");
// });

// test("receive synchronous data via ipcMainCallFirstListener()", async () => {
//   const data = await ipcMainCallFirstListener(electronApp, "main-sychronous-data");
//   expect(data).toBe("Main Synchronous Data");
// });

// test("receive asynchronous data via ipcMainCallFirstListener()", async () => {
//   const data = await ipcMainCallFirstListener(electronApp, "main-asynchronous-data");
//   expect(data).toBe("Main Asynchronous Data");
// });

// test("select a menu item via the main process", async () => {
//   await clickMenuItemById(electronApp, "new-window");
//   const newPage = await electronApp.waitForEvent("window");
//   expect(newPage).toBeTruthy();
//   expect(await newPage.title()).toBe("Window 5");
//   page = newPage;
// });

// test("make sure two screenshots of the same page match", async ({ page }) => {
//   // take a screenshot of the current page
//   const screenshot1 = await page.screenshot();
//   // create a visual hash using Jimp
//   const screenshot1hash = (await jimp.read(screenshot1)).hash();
//   // take a screenshot of the page
//   const screenshot2 = await page.screenshot();
//   // create a visual hash using Jimp
//   const screenshot2hash = (await jimp.read(screenshot2)).hash();
//   // compare the two hashes
//   expect(screenshot1hash).toEqual(screenshot2hash);
// });
