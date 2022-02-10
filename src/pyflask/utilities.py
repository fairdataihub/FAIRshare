from __future__ import print_function
import os
import json
import shutil
import requests
import platform
import subprocess


def foldersPresent(folder_path):
    try:
        folder_content = os.listdir(folder_path)

        for item in folder_content:
            item_path = os.path.join(folder_path, item)

            if os.path.isdir(item_path):
                return True

        return False
    except Exception as e:
        raise e


def zipFolder(folder_path):
    try:
        home_path = os.path.expanduser("~")
        soda_folder_path = os.path.join(
            home_path, ".sodaforcovid19research", "dataset"
        )  # noqa: E501

        if not os.path.exists(soda_folder_path):
            os.makedirs(soda_folder_path)

        zip_path = os.path.join(soda_folder_path, "dataset")

        if os.path.exists(zip_path + ".zip"):
            os.remove(zip_path + ".zip")

        zipped_path = shutil.make_archive(zip_path, "zip", folder_path)

        return zipped_path
    except Exception as e:
        raise e


def deleteFile(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)

        return "SUCCESS"
    except Exception as e:
        raise e


def requestJSON(url):
    try:
        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        return response.json()
    except Exception as e:
        raise e


def createFile(folder_path, file_name, file_content, content_type):
    try:
        file_path = os.path.join(folder_path, file_name)

        if content_type == "text":
            with open(file_path, "w") as file:
                file.write(file_content)

        if content_type == "json":
            with open(os.path.join(folder_path, file_name), "w") as f:
                f.write(json.dumps(file_content))

        return "SUCCESS"
    except Exception as e:
        raise e


def openFileExplorer(file_path):
    try:
        if platform.system() == "Windows":
            subprocess.Popen(r"explorer /select," + str(file_path))
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", file_path])
        else:
            subprocess.Popen(["xdg-open", file_path])

        return "SUCCESS"
    except Exception as e:
        raise e
