const fs = require("fs");
const path = require("path");
const electron_notarize = require("electron-notarize");

require("dotenv").config();

module.exports = async function (params) {
  // Only notarize the app on Mac OS only.
  if (process.platform !== "darwin") {
    console.log(
      "No notarization needed for current platform. This process is only intended for macOS."
    );
    return;
  }
  console.log("afterSign hook triggered", params);

  // Same appId in electron-builder.
  let appId = "com.fairdataihub.fairshare";

  let appPath = path.join(params.appOutDir, `${params.packager.appInfo.productFilename}.app`);
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
