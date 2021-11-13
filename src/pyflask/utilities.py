from __future__ import print_function
import config
import os
import shutil
import json


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
        soda_folder_path = os.path.join(home_path, ".sodaforcovid19research", "dataset")

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
