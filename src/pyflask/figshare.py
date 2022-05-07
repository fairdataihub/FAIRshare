import hashlib
import json
import os

import config
import requests


def createNewFigshareItem(access_token, data):
    url = f"{config.FIGSHARE_SERVER_URL}/account/articles"

    payload = data
    headers = {
        "Authorization": f"token {access_token}",
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 201:
        response = response.json()
        article_id = response["entity_id"]

        url = f"{config.FIGSHARE_SERVER_URL}/account/articles/{article_id}/authors"

        payload = {}
        headers = {
            "Authorization": f"token {access_token}",
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        response = response.json()

        if len(response) > 0:
            figshare_author = response[0]
            figshare_author_id = figshare_author["id"]

            url = f"{config.FIGSHARE_SERVER_URL}/account/articles/{article_id}/authors/{figshare_author_id}"  # noqa: E501

            payload = {}
            headers = {
                "Authorization": f"token {access_token}",
            }

            response = requests.request("DELETE", url, headers=headers, data=payload)

            if response.status_code != 204:
                return {"status": "ERROR", "message": "Could not delete default author"}

        url = f"{config.FIGSHARE_SERVER_URL}/account/articles/{article_id}/reserve_doi"

        payload = {}
        headers = {
            "Authorization": f"token {access_token}",
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code == 200:
            response = response.json()

            doi = response["doi"]

            return json.dumps({"doi": doi, "article_id": article_id})
        else:
            return {"status": "ERROR", "message": "Could not create DOI"}
    else:
        return {
            "status": "ERROR",
            "message": response.json()["message"],
        }


def deleteFigshareArticle(access_token, article_id):
    url = f"{config.FIGSHARE_SERVER_URL}/account/articles/{article_id}"

    payload = {}
    headers = {
        "Authorization": f"token {access_token}",
    }

    response = requests.request("DELETE", url, headers=headers, data=payload)

    if response.status_code == 204:
        return "SUCCESS"
    else:
        return "ERROR"


def uploadFileToFigshare(access_token, article_id, file_path):
    file_name = os.path.basename(file_path)

    # get a list of all the files in the article.
    # If a file with the same name already exists, replace it

    url = f"{config.FIGSHARE_SERVER_URL}/account/articles/{article_id}/files"

    payload = {}
    headers = {
        "Authorization": f"token {access_token}",
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        response = response.json()
        for file in response:
            if file["name"] == file_name:
                url = f"{config.FIGSHARE_SERVER_URL}/account/articles/{article_id}/files/{file['id']}"  # noqa: E501

                payload = {}
                headers = {
                    "Authorization": f"token {access_token}",
                }

                response = requests.request(
                    "DELETE", url, headers=headers, data=payload
                )

                if response.status_code != 204:
                    return json.dumps(
                        {
                            "status": "ERROR",
                            "message": "Something went wrong with removing a previous file in the Figshare article",  # noqa: E501
                        }
                    )
    else:
        return json.dumps(
            {"status": "ERROR", "message": "Could not read files in article"}
        )

    # Get the md5 sum and file size in bytes

    md5_hash = hashlib.md5()
    md5_sum = ""

    with open(file_path, "rb") as f:
        # Read and update hash in chunks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            md5_hash.update(byte_block)
        md5_sum = md5_hash.hexdigest()

    file_size = os.path.getsize(file_path)

    # Create the file imprint on figshare.
    url = f"{config.FIGSHARE_SERVER_URL}/account/articles/{article_id}/files"

    payload = json.dumps({"name": file_name, "md5": md5_sum, "size": file_size})
    headers = {
        "Authorization": f"token {access_token}",
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    response = response.json()
    file_location = response["location"]

    last_slash_position = file_location.rfind("/")
    file_id = file_location[last_slash_position + 1 :]  # noqa: E203

    # Get the upload path and the number of file parts to push up

    url = f"{config.FIGSHARE_SERVER_URL}/account/articles/{article_id}/files/{file_id}"

    payload = {}
    headers = {
        "Authorization": f"token {access_token}",
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    response = response.json()

    upload_url = response["upload_url"]

    payload = {}
    headers = {
        "Authorization": f"token {access_token}",
    }

    response = requests.request("GET", upload_url, headers=headers, data=payload)

    response = response.json()

    parts = response["parts"]

    # Read the file and start seperating it into partitions
    # upload each partition individually

    with open(file_path, "rb") as stream:
        for part in parts:

            url = f"{upload_url}/{part['partNo']}"

            stream.seek(part["startOffset"])
            data = stream.read(part["endOffset"] - part["startOffset"] + 1)
            headers = {"Authorization": f"token {access_token}"}

            response = requests.request("PUT", url, headers=headers, data=data)

            if response.status_code != 200:
                return json.dumps(
                    {
                        "status": "ERROR",
                        "message": "Something went wrong with uploading a file partition",  # noqa: E501
                    }
                )

    # Signal to figshare that the upload is complete for the file

    payload = json.dumps({})
    headers = {
        "Authorization": f"token {access_token}",
        "Content-Type": "application/json",
    }
    url = f"{config.FIGSHARE_SERVER_URL}/account/articles/{article_id}/files/{file_id}"

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 202:
        return json.dumps({"status": "SUCCESS", "message": ""})
    else:
        return json.dumps(
            {"status": "ERROR", "message": "Could not confirm file upload completion"}
        )
