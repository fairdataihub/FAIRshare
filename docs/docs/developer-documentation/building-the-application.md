---
sidebar_position: 3
---

# Building the application

To build the complete application, you will need to build the python executable and the Electron portion separately.

:::caution
You will not be able to do cross compatible builds for MacOS, Linux and Windows. The Python executable will be OS specific so you will need to build on each target OS separately. 

For macOS you will need an Apple Developer Certificate. You can get one of these [here](https://developer.apple.com/support/certificates/).
:::

### Create Python executable

To first build the Python exectuable run:

```shell
yarn python:build
```

This should create a single file named `api` or (`api.exe` on Windows) in the `pyflaskdist` directory. We use pyinstaller since we can't guarantee that a user will have python on their system. Using Pyinstaller allows us to have a portable python environment alongside our flask application. When you bundle the Electron application (in the next step), the python application will be automatically included in the Electron bundle.

### Create Electron application

#### Local build

To now build the final electron application you can use the following command:

```shell
yarn electron:build
```

This will create the installer needed to share your application. The final installer will be saved in the `dist_electron` folder.

#### Build and release to Github

You can also push your build to a draft release on GitHub. You will need to have a Github token in your environment to push items to github. Create your github token [here](https://github.com/settings/tokens). You will need the `repo` permissions on your token. Follow the [electron-builder](https://www.electron.build/configuration/publish) instructions on setting up your token.

```shell
yarn electron:build-release
```
