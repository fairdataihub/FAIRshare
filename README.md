# electron-vue3-flask-template

This is a template that creates an Electron application with a Flask backend and uses Vue3 and TailwindCSS ([optional](#removing-tailwindcss)) for the frontend. At the current time, this application template uses Electron.js version 13.0+ as it is the most recent version of electron that I was able to use with Vue. I will update this template with later versions when supported.

### Project Use Cases

In the current world of serverless functions and cloud hosted servers, it is nice to have an always accessible backend server but if you want to run some code that uses quite a lot of processing power, this can be a challenge. If your application can have some processing handled by Python on the user's computer, this is a good alternative to have. Some potential use cases are listed below:

- If your application uses ML/AI or something within that area of research, having your backend run Python locally is a great option.
- If your application concept uses Pandas or some other data processing python package that you do not want to host, using Python locally as a backend is possible.
- If you have sensitive data that you would like to process on a user's computer and not have to deal with transferring files to a server.

## Project setup

```shell
yarn install
cd src/pyflask
pip install -r requirements.txt
```

## Running the application

### Vue frontend running in Electron

To compile the front end application and open it an Electron instance, use the following command:

```shell
yarn electron:serve
```

Using this command should compile your application and also allow hot-reloads for development. The `dist_electron` folder will be created at the root of your project and is your final actual electron application with an automatically generated 'package.json' and 'index.js' files. You don't have to worry about this folder too much. It should also automatically copy the `pyflask` folder to the dist_electron directory. If you would like to change/modify this functionality, change the path locations in the `package.json` file under the `electron:serve-precopy` script.

### Vue frontend only (not recommended)

To run only the Vue frontend on your browser you can just use the following commands:

```shell
yarn serve
```

This will compile your application and also allow hot-reloads for development. If you want to test any components that don't use OS native calls this is a good alternative to have. In my opinion I would recommend using the [electron compilation command](#vue-frontend-running-in-electron) because this should you the most up to date state of your application. If you want the backend to also run alongside the browser instance, just open a new terminal instance and run the following command:

```shell
python pyflask/api.py
```

`Note:` This instance will still not have access to the native node libraries since these are provided through the remote Electron mopdule.

## Building the application

To build the complete application, you will need to build the python executable and the Electron portion seperately.

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

### Project Inspiration

This template starts as a Vue application that Electron was added into using this amazing plugin created by [@nklayman](https://nklayman.github.io/vue-cli-plugin-electron-builder/). I created this template to allow users who would like to use Vue as their frontend for an Electron application while using Flask for a backend. If you wanted to let a user of your application use their own computer to provide some processing power, this repo should hopefully work for you.

The original repository for Vue-Electron can be found here: [@codingwithjustin/vue3-electron](https://github.com/codingwithjustin/vue3-electron)

The original repository for using Electron with a Python backend can be found here: [@fyears/electron-python-example](https://github.com/fyears/electron-python-example). This repo uses zerorpc and zeromq to pass messaged between the backend and the Electron application but the original [zerorpc-node](https://github.com/0rpc/zerorpc-node) library hasn't been updated in over 3 years so using Flask and regular http calls is much more simpler and robust. Further more, using Flask as the backend allows you to use newer versions of Electron and Vue to create your application.

### Removing TailwindCSS

If you would like to use a different CSS framwork or use a library like bootstrap, you can remove the tailwind library from this project.

```shell
yarn remove tailwindcss postcss
rm tailwind.config.js
rm postcss.config.js
```

In your `src/index.css` file remove the following lines:

```postcss
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### Made with Electron, Vue and Flask

Take a look at some of the amazing projects built with this template. Want to have your own project listed? Feel free to add your project at the bottom of the list below then submit a pull request.

- Your project here

### Still To-Do

- [ ] Add tests (Spectron)

<br/>

<p align="center">
 Made with ❤️ by <a href="https://sanjaysoundarajan.dev">@megasanjay</a>
</p>
