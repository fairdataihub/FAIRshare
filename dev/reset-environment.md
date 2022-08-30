# Easy to copy instructions to reset the environment cross platform

```shell
conda activate base
conda remove --name fairshare-dev --all

conda create -n fairshare-dev python=3

conda activate fairshare-dev
conda install -c conda-forge nodejs=16.14 yarn pip

pip install flask flask-restx flask-cors flask-wtf requests pyinstaller python-dotenv pyyaml xlsxwriter

conda env export --no-builds > test-fairshare-dev.yml
```

## Test

```shell
yarn install
yarn python:dev
```
