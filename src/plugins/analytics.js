import ua from "universal-analytics";
import { v4 as uuidv4 } from "uuid";
import fs from "fs-extra";
import { app as electronApp } from "@electron/remote";
import path from "path";

// Handle DNT settings. Hopefuly this won't be needed after we switch to our custom analytics.
// Might also add this to a config object rather than using a file.
const config_folder_path = path.join(electronApp.getPath("home"), ".fairshare");

let dnt = false;

if (!fs.existsSync(config_folder_path)) {
  fs.mkdirSync(config_folder_path);
  dnt = false;
  console.log("No DNT settings found, using default settings.");
} else {
  let dnt_file_path = path.join(config_folder_path, "dnt.fdih");
  if (fs.existsSync(dnt_file_path)) {
    dnt = true;
    console.log("DNT settings found, using them.");
  } else {
    dnt = false;
    console.log("No DNT settings found, using default settings.");
  }
}

export default {
  install: (app, options) => {
    // inject a globally available $track() method
    app.config.globalProperties.$track = (category = "", action = "", label = "", value = "") => {
      let clientID = "";

      // Check to see if a previous clientID exists
      if (localStorage.clientID) {
        clientID = localStorage.clientID;
      } else {
        clientID = uuidv4();

        // save the clientID to localStorage
        localStorage.clientID = clientID;
      }

      // create a new visitor
      const usr = ua(options.trackingID, clientID);

      // send the event
      if (!dnt) {
        usr
          .event({
            ec: category,
            ea: action,
            el: label,
            ev: value,
          })
          .send();
      }

      return;
    };
  },
};
