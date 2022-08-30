"use strict";

import { ipcMain, dialog } from "electron";

ipcMain.handle("show-open-file-dialog", (_event, data) => {
  const result = dialog.showOpenDialogSync(null, data);

  return result;
});
