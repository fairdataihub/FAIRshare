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
        fairshare_folder_path = os.path.join(
            home_path, ".fairshare", "dataset"
        )  # noqa: E501

        if not os.path.exists(fairshare_folder_path):
            os.makedirs(fairshare_folder_path)

        zip_path = os.path.join(fairshare_folder_path, "dataset")

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


def readFolderContents(dir):
    try:

        def dfs(dir):
            result = []
            for filename in os.listdir(dir):
                newDic = {
                    "label": "",
                    "isDir": "",
                    "children": [],
                    "fullpath": "",
                }  # noqa: E501
                fileFullName = os.path.join(dir, filename)
                if os.path.isdir(fileFullName):
                    newDic["label"] = filename
                    newDic["isDir"] = True
                    newDic["children"] = dfs(fileFullName)
                    newDic["fullpath"] = fileFullName
                else:
                    newDic["label"] = filename
                    newDic["isDir"] = False
                    newDic["fullpath"] = fileFullName
                result.append(newDic)
            return result

        root = {
            "label": dir,
            "children": dfs(dir),
            "fullPath": dir,
            "isDir": True,
        }  # noqa: E501
        return root
    except Exception as e:
        raise e


def fileExistInFolder(folder_path, file_name):
    try:
        for filename in os.listdir(folder_path):
            if filename == file_name:
                import json

                fileFullName = os.path.join(folder_path, filename)
                f = open(fileFullName)
                return json.load(f)
        return "Not Found"
    except Exception as e:
        raise e
