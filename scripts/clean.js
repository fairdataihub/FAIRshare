"use strict";

const fs = require("fs");
const pathlib = require("path");

const deleteitemsRecursive = (path) => {
  if (!fs.existsSync(path)) return console.log(`${path} does not exist!`);
  if (fs.existsSync(path) && fs.lstatSync(path).isDirectory()) {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    fs.readdirSync(path).forEach(function(file, _index) {
      const curPath = pathlib.join(path, file);

      if (fs.lstatSync(curPath).isDirectory()) {
        // recurse
        deleteitemsRecursive(curPath);
      } else {
        // delete file
        fs.unlinkSync(curPath);
      }
    });

    console.log(`Deleting directory "${path}"...`);
    fs.rmdirSync(path);
  }
  if (fs.existsSync(path) && fs.lstatSync(path).isFile()) {
    console.log(`Deleting file "${path}"...`);
    fs.unlinkSync(path);
  }
};

module.exports = async (pathToDelete) => {
  deleteitemsRecursive(pathToDelete);
};
