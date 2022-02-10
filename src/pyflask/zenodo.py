from __future__ import print_function
import config
import requests
import json
import os
import time


def getAllZenodoDepositions(access_token):
    # get a list of all unpublished datasets on Zenodo
    # print(
    #     f"{config.ZENODO_SERVER_URL}/deposit/depositions?access_token={access_token}"
    #     config.ZENODO_SERVER_URL + "deposit/depositions?access_token=%s" % access_token # noqa: E501
    # )
    try:
        parameters = {"access_token": access_token}
        r = requests.get(
            f"{config.ZENODO_SERVER_URL}/deposit/depositions",
            params=parameters,  # noqa: E501
        )
        return r.json()
    except Exception as e:
        raise e


def createNewZenodoDeposition(access_token):
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
    try:
        if os.path.exists(file_path) and os.path.isfile(file_path):
            pass
        else:
            raise Exception(
                "Error: Could not find a file at the path provided."
            )  # noqa: E501

        params = {"access_token": access_token}
        filename = os.path.basename(file_path)

        with open(file_path, "rb") as fileContent:
            r = requests.put(
                "%s/%s" % (bucket_url, filename),
                data=fileContent,
                params=params,
            )

        # Adding a sleep function to avoid hitting the rate limit
        time.sleep(1.5)

        return r.json()
    except Exception as e:
        raise e


def addMetadataToZenodoDeposition(access_token, deposition_id, metadata):
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
    try:
        headers = {"Content-Type": "application/json"}
        params = {"access_token": access_token}
        r = requests.delete(
            f"{config.ZENODO_SERVER_URL}/deposit/depositions/{deposition_id}",
            params=params,
            headers=headers,
        )
        statusCode = r.status_code

        if statusCode == 204:
            return "Delete successful"
        else:
            return "Delete failed"

    except Exception as e:
        raise e
