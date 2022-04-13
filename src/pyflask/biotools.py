from __future__ import print_function
import requests
import json


def loginToBioTools(username, password):
    # Create a new Zenodo deposition

    try:
        data = json.dumps({"username": username, "password": password})
        headers = {
            "Content-Type": "application/json",
        }

        response = requests.request(
            "POST",
            "https://bio.tools/api/rest-auth/login/",
            headers=headers,
            data=data,
        )

        return response.json()

    except Exception as e:
        raise e


def getUserDetails(token):
    # Get user details

    try:
        headers = {
            "Authorization": f"Token {token}",
        }

        response = requests.request(
            "GET",
            "https://bio.tools/api/rest-auth/user/?format=json",
            headers=headers,
        )

        return response.json()

    except Exception as e:
        raise e
