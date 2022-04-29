const menuTemplate = [
  {
    label: "Edit",
    submenu: [
      {
        role: "undo",
      },
      {
        role: "redo",
      },
      {
        type: "separator",
      },
      {
        role: "cut",
      },
      {
        role: "copy",
      },
      {
        role: "paste",
      },
    ],
  },

  {
    label: "View",
    submenu: [
      {
        role: "reload",
      },
      {
        role: "toggledevtools",
      },
      {
        type: "separator",
      },
      {
        role: "resetzoom",
      },
      {
        role: "zoomin",
      },
      {
        role: "zoomout",
      },
      {
        type: "separator",
      },
      {
        role: "togglefullscreen",
      },
    ],
  },

  {
    role: "window",
    submenu: [
      {
        role: "minimize",
      },
      {
        role: "close",
      },
    ],
  },

  {
    role: "help",
    submenu: [
      {
        label: "View the documentation",
        accelerator: "F1",
        click: async () => {
          const { shell } = require("electron");
          await shell.openExternal("https://docs.fairshareapp.io");
        },
      },
      {
        label: "Learn more about Fairshare",
        click: async () => {
          const { shell } = require("electron");
          await shell.openExternal("https://fairdataihub.org/fairshare");
        },
      },
    ],
  },
];

export default menuTemplate;
