"use strict";

const path = require("path");
const deleteitemsRecursive = require("./clean.js");

module.exports = async () => {
  let pathArgs = [
    path.join(__dirname, "..", "src", "pyflaskdist"),
    path.join(__dirname, "..", "build"),
    path.join(__dirname, "..", "api.spec"),
  ];
  console.log("Removing additional folders and files before build...");

  pathArgs.forEach((pathToDelete) => deleteitemsRecursive(pathToDelete));

  console.log("Successfully removed!");
};
