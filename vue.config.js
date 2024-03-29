module.exports = {
  pluginOptions: {
    electronBuilder: {
      externals: ["electron-log"],
      nodeIntegration: true,
      preload: { preload: "src/preload.js" },
      builderOptions: {
        appId: "com.fairdataihub.fairshare",
        productName: "FAIRshare",
        executableName: "FAIRshare",
        copyright: "Copyright © 2022 Fair Data Innovations Hub",

        asar: true,

        afterSign: "./build-scripts/notarize.js",
        generateUpdatesFilesForAllChannels: true,

        files: ["**/*", "!pyflask/", "!build/", "!api.spec", "!index.css"],

        fileAssociations: { ext: "fairshare" },
        protocols: [
          {
            name: "fairshare",
            schemes: ["fairshare"],
          },
        ],

        win: {
          target: "nsis",
          icon: "./src/assets/app-icons/Icon.ico",
          extraResources: [{ from: "./src/pyflaskdist/api.exe" }],
        },
        nsis: {
          createDesktopShortcut: "always",
          oneClick: true,
          deleteAppDataOnUninstall: true,
          installerIcon: "./src/assets/app-icons/Icon.ico",
        },

        mac: {
          target: ["dmg", "zip"],
          icon: "./src/assets/app-icons/Icon.png",
          extraResources: [{ from: "./src/pyflaskdist/api" }],
          darkModeSupport: false,
          hardenedRuntime: true,
          gatekeeperAssess: false,
          entitlements: "./entitlements.mac.inherit.plist",
          entitlementsInherit: "./entitlements.mac.inherit.plist",
        },

        linux: {
          target: "AppImage",
          icon: "./src/assets/app-icons/Icon.png",
          extraResources: [{ from: "./src/pyflaskdist/api" }],
        },

        publish: {
          provider: "github",
          vPrefixedTagName: true,
          publishAutoUpdate: true,
        },
      },
    },
  },
};
