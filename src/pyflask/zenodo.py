import json
import os
import time

import config
import requests


def getAZenodoDeposition(access_token, deposition_id):
    # get a specific dataset on Zenodo
    try:
        url = f"{config.ZENODO_SERVER_URL}/deposit/depositions/{deposition_id}?access_token={access_token}"  # noqa: E501

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        return response.json()
    except Exception as e:
        raise e


def getAllZenodoDepositions(access_token):
    # get a list of all unpublished datasets on Zenodo

    try:
        parameters = {"access_token": access_token}
        r = requests.get(
            f"{config.ZENODO_SERVER_URL}/deposit/depositions",
            params=parameters,
        )
        return r.json()
    except Exception as e:
        raise e


def createNewZenodoDeposition(access_token):
    # Create a new Zenodo deposition

    try:
        headers = {"Content-Type": "application/json"}
        params = {"access_token": access_token}
        r = requests.post(
            f"{config.ZENODO_SERVER_URL}/deposit/depositions",
            params=params,
            json={},
            headers=headers,
        )
        return r.json()
    except Exception as e:
        raise e


def uploadFileToZenodoDeposition(access_token, bucket_url, file_path):
    # Upload a file to a Zenodo deposition

    try:
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            raise Exception("Error: Could not find a file at the path provided.")

        params = {"access_token": access_token}
        filename = os.path.basename(file_path)

        with open(file_path, "rb") as fileContent:
            r = requests.put(
                f"{bucket_url}/{filename}", data=fileContent, params=params
            )

        # Adding a sleep function to avoid hitting the rate limit
        time.sleep(1.5)

        return r.json()
    except Exception as e:
        raise e


def addMetadataToZenodoDeposition(access_token, deposition_id, metadata):
    # Add metadata to a Zenodo deposition

    try:
        headers = {"Content-Type": "application/json"}
        params = {"access_token": access_token}
        data = json.dumps(metadata)
        r = requests.put(
            f"{config.ZENODO_SERVER_URL}/deposit/depositions/{deposition_id}",
            params=params,
            data=data,
            headers=headers,
        )
        return r.json()
    except Exception as e:
        raise e


def publishZenodoDeposition(access_token, deposition_id):
    # Publish a Zenodo deposition

    try:
        headers = {"Content-Type": "application/json"}
        params = {"access_token": access_token}
        r = requests.post(
            f"{config.ZENODO_SERVER_URL}/deposit/depositions/{deposition_id}/actions/publish",  # noqa: E501
            params=params,
            headers=headers,
        )
        return r.json()
    except Exception as e:
        raise e


def deleteZenodoDeposition(access_token, deposition_id):
    # Delete an unpublished Zenodo deposition

    try:
        headers = {"Content-Type": "application/json"}
        params = {"access_token": access_token}
        r = requests.delete(
            f"{config.ZENODO_SERVER_URL}/deposit/depositions/{deposition_id}",
            params=params,
            headers=headers,
        )
        statusCode = r.status_code

        return "Delete successful" if statusCode == 204 else "Delete failed"
    except Exception as e:
        raise e


def createNewZenodoDepositionVersion(access_token, deposition_id):
    # Create a new version of an existing Zenodo deposition

    try:
        url = f"{config.ZENODO_SERVER_URL}/deposit/depositions/{deposition_id}/actions/newversion?access_token={access_token}"  # noqa: E501

        payload = {}
        headers = {}

        response = requests.request("POST", url, headers=headers, data=payload)

        latest_draft_url = (response.json())["links"]["latest_draft"]
        last_slash = latest_draft_url.rfind("/") + 1

        return latest_draft_url[last_slash:]

    except Exception as e:
        raise e


def removeFileFromZenodoDeposition(access_token, deposition_id, file_id):
    # Remove file from an unpublished Zenodo deposition

    try:
        url = f"{config.ZENODO_SERVER_URL}/deposit/depositions/{deposition_id}/files/{file_id}?access_token={access_token}"  # noqa: E501

        payload = {}
        headers = {}

        response = requests.request("DELETE", url, headers=headers, data=payload)

        if response.status_code == 204:
            return "Delete successful"

    except Exception as e:
        raise e
