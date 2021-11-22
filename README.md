# SODA for COVID-19 Research

## Project setup

Use a python environment (Anaconda) to separate your dev and release instance.

You will need two different instructions for windows and macOS/linux. `NVM` is required for macOS and Linux at the moment while the conda-forge release channel is updated.

### Windows

```shell 
# create the conda environment from the file
conda env create -f .\dev\sodacovid-dev.yml

# activate the anaconda environment 
conda activate sodacovid-dev

# install all the project dependencies
yarn install
```

### macOS/Linux

```shell
# create the conda environment from the file
conda env create -f .\dev\sodacovid-dev.yml

# activate the conda environment
conda activate sodacovid-dev

# if you don't have nvm installed use the following instruction
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# install nodejs
nvm install 16

# activate nodejs
nvm use 16

# verify that you are on node v16.13.0 or higher
node -v

# install yarn
npm install -g yarn

# install all the project dependencies
yarn install
```

`Note:` These instructions are subject to change. At the moment, Node v16.13.0 is not available in the conda-forge release channel. When that version gets added, the macOS and linux project setup will use the same instructions as windows.

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
yarn python:dev
```

`Note:` This instance will still not have access to the native node libraries since these are provided through the remote Electron module.

## Building the application

To build the complete application, you will need to build the python executable and the Electron portion separately.

`Note:` You will not be able to do cross compatible builds for MacOS, Linux and Windows. The Python executable will be OS specific so you will need to build on each target OS separately. For macOS you will need an Apple Developer Certificate. You can get one of these [here](https://developer.apple.com/support/certificates/).

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

### Flask application and Swagger documentaion

For the python portion of this application, Flask-RESTX is used to generate the API specific portion. In this example template, I have used a very small subsection of all the features it provides but you are welcome to read more about all the provided options in their documentation. To learn more about Flask-RESTX, click [here](https://flask-restx.readthedocs.io/en/latest/).

One of the biggest reasons for using this library was the automatic generation of API documentation. If you are working in a team and have different front-end and back-end developers, this should allow you to document your application as you go through your development cycle. To view the documentation, I have set it up under the `/docs` endpoint. This can be accessed by either running `yarn electron:serve` (for the full application) or just running `python pyflask/api.py`. You can then visit the url at [http://127.0.0.1:5000/docs](http://127.0.0.1:5000/docs) and explore the Swagger documentation.
