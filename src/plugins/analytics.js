import ua from "universal-analytics";
import { v4 as uuidv4 } from "uuid";

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
      usr
        .event({
          ec: category,
          ea: action,
          el: label,
          ev: value,
        })
        .send();

      return;
    };
  },
};
