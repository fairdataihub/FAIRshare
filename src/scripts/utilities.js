"use strict";

import { app, ipcMain, shell, clipboard } from "electron";

ipcMain.on("open-link-in-browser", async (_event, link) => {
  shell.openExternal(link).then(() => {
    console.log("opened link", link);
  });
});

ipcMain.on("restart-fairshare", async (_event) => {
  app.relaunch();
  app.quit();
});

ipcMain.on("write-to-clipboard", async (_event, data, type) => {
  if (type === "text") {
    clipboard.writeText(data);
  }
  if (type === "html") {
    clipboard.writeHTML(data);
  }
  if (type === "image") {
    clipboard.writeImage(data);
  }
});

ipcMain.on("read-clipboard-contents", async (_event, type) => {
  if (type === "text") {
    const clipboardText = clipboard.readText();
    // eslint-disable-next-line no-undef
    mainWindow.webContents.send("read-clipboard-contents-response", clipboardText);
  }

  if (type === "image") {
    const clipboardImage = clipboard.readImage();
    // eslint-disable-next-line no-undef
    mainWindow.webContents.send("read-clipboard-contents-response", clipboardImage);
  }

  if (type === "html") {
    const clipboardHtml = clipboard.readHTML();
    // eslint-disable-next-line no-undef
    mainWindow.webContents.send("read-clipboard-contents-response", clipboardHtml);
  }
});
