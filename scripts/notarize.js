const fs = require("fs");
const path = require("path");
require("dotenv").config();
var electron_notarize = require("electron-notarize");

module.exports = async function (params) {
  // Only notarize the app on Mac OS only.
  if (process.platform !== "darwin") {
    console.log("Not building on macOS. Cancelling notarize...");
    return;
  }
  console.log("afterSign hook triggered", params);

  // Same appId in electron-builder.
  let appId = "com.megasanjay.electronvueflask";

  let appPath = path.join(
    params.appOutDir,
    `${params.packager.appInfo.productFilename}.app`
  );
  if (!fs.existsSync(appPath)) {
    throw new Error(`Cannot find application at: ${appPath}`);
  }

  console.log(`Notarizing ${appId} found at ${appPath}`);

  try {
    await electron_notarize.notarize({
      appBundleId: appId,
      appPath: appPath,
      appleId: process.env.appleId,
      appleIdPassword: process.env.appleIdPassword,
    });
  } catch (error) {
    console.error(error);
  }

  console.log(`Done notarizing ${appId}`);
};
