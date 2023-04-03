import json

import config
import requests


def loginToBioTools(username, password):
    # Create a new Zenodo deposition

    try:
        data = json.dumps({"username": username, "password": password})
        headers = {
            "Content-Type": "application/json",
        }

        response = requests.request(
            "POST",
            f"{config.BIO_TOOLS_SERVER_URL}/rest-auth/login/",
            headers=headers,
            data=data,
        )

        return response.json()

    except Exception as e:
        raise e


def getBioToolsUserDetails(token):
    # Get user details

    try:
        headers = {
            "Authorization": f"Token {token}",
        }

        response = requests.request(
            "GET",
            f"{config.BIO_TOOLS_SERVER_URL}/rest-auth/user/?format=json",
            headers=headers,
        )

        if response.status_code != 200:
            return "Invalid username", response.status_code
        else:
            return response.json()

    except Exception as e:
        raise e


def validateTool(token, data):
    # Validate tool

    try:
        data = json.dumps(data)
        headers = {
            "Authorization": f"Token {token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        response = requests.request(
            "POST",
            f"{config.BIO_TOOLS_SERVER_URL}/tool/validate",
            headers=headers,
            data=data,
        )

        return {
            "status": "error" if response.status_code != 200 else "success",
            "data": response.json(),
        }

    except Exception as e:
        raise e


def registerTool(token, data):
    # Register tool with BioTools

    try:
        data = json.dumps(data)
        headers = {
            "Authorization": f"Token {token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        response = requests.request(
            "POST",
            f"{config.BIO_TOOLS_SERVER_URL}/tool",
            headers=headers,
            data=data,
        )

        return {
            "status": "error" if response.status_code != 201 else "success",
            "data": response.json(),
        }

    except Exception as e:
        raise e
