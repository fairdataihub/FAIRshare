import { ipcRenderer } from "electron";
window.ipcRenderer = ipcRenderer;

// import { contextBridge, ipcRenderer } from "electron";

// // Expose protected methods that allow the renderer process to use
// // the ipcRenderer without exposing the entire object
// contextBridge.exposeInMainWorld("ipcRenderer", {
//   send: (channel, data) => {
//     // whitelist channels
//     let validChannels = ["open-link-in-browser", "OAuth-Github"];
//     if (validChannels.includes(channel)) {
//       ipcRenderer.send(channel, data);
//     }
//   },
//   receive: (channel, func) => {
//     let validChannels = ["open-link-in-browser", "OAuth-Github"];
//     if (validChannels.includes(channel)) {
//       // Deliberately strip event as it includes `sender`
//       ipcRenderer.on(channel, (_event, ...args) => func(...args));
//     }
//   },
// });
