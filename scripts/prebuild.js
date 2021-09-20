"use strict";
const path = require("path");
const deleteitemsRecursive = require("./clean.js");

const pathArgs = [
  path.join(__dirname, "..", "src", "pyflaskdist"),
  path.join(__dirname, "..", "dist_electron"),
];

console.log("Cleaning folders and files before build...");

pathArgs.forEach((pathToDelete) => deleteitemsRecursive(pathToDelete));

console.log("Successfully cleaned!");
