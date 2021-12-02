---
sidebar_position: 2
---

# Running the application

FairShare has been developed as an Electron application running a Vue 3 based front end. 

### Vue frontend running in Electron

To compile the front end application and open it an Electron instance, use the following command:

```shell
yarn electron:serve
```

Using this command should compile your application and also allow hot-reloads for development. The `dist_electron` folder will be created at the root of your project and is your final actual electron application with an automatically generated `package.json` and `index.js` files. You don't have to worry about this folder too much. It should also automatically copy the `pyflask` folder to the dist_electron directory. If you would like to change/modify this functionality, change the path locations in the `package.json` file under the `electron:serve-precopy` script.

### Vue frontend only (not recommended)

To run only the Vue frontend on your browser you can just use the following commands:

```shell
yarn serve
```

This will compile your application and also allow hot-reloads for development. If you want to test any components that don't use OS native calls this is a good alternative to have. In my opinion I would recommend using the [electron compilation command](#vue-frontend-running-in-electron) because this should you the most up to date state of your application.

:::caution
This instance will still not have access to the native node libraries since these are provided through the `@electron/remote` module.
:::

If you want the backend to also run alongside the browser instance, just open a new terminal instance and run the following command:

```shell
yarn python:dev
```
