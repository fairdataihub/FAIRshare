module.exports = {
  pluginOptions: {
    electronBuilder: {
      externals: ["electron-log"],
      nodeIntegration: true,
      preload: { preload: "src/preload.js" },
      builderOptions: {
        // afterPack: "./scripts/postbuild.js",
        appId: "com.fairdataihub.sodaforcovid19research",
        asar: true,
        afterSign: "./scripts/notarize.js",
        generateUpdatesFilesForAllChannels: true,
        files: ["**/*", "!pyflask/", "!build/", "!api.spec", "!index.css"],
        win: {
          target: "nsis",
          icon: "./src/assets/app-icons/windowsAppIcon.ico",
          extraResources: [{ from: "./src/pyflaskdist/api.exe" }],
        },
        mac: {
          target: ["dmg", "zip"],
          icon: "./src/assets/app-icons/macAppIcon.icns",
          extraResources: [{ from: "./src/pyflaskdist/api" }],
          darkModeSupport: false,
          hardenedRuntime: true,
          gatekeeperAssess: false,
          entitlements: "./entitlements.mac.inherit.plist",
          entitlementsInherit: "./entitlements.mac.inherit.plist",
        },
        linux: {
          target: "AppImage",
          icon: "./src/assets/app-icons/linuxAppIcon.png",
        },
        nsis: {
          createDesktopShortcut: "always",
          oneClick: true,
          deleteAppDataOnUninstall: true,
          installerIcon: "./src/assets/app-icons/windowsAppIcon.ico",
        },
        publish: {
          provider: "github",
          repo: "https://github.com/fairdataihub/SODA-for-COVID-19-Research.git",
        },
      },
    },
  },
};
