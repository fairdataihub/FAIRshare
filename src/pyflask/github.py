from __future__ import print_function
import requests
import json
import base64


def uploadFileToGithub(access_token, file_name, file_path, repo_name):
    def getFileSHA(file_name, repo_name, access_token):
        url = f"https://api.github.com/repos/{repo_name}/contents/{file_name}"

        payload = {}
        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code != 200:
            return False

        fileSHA = response.json()["sha"]

        if fileSHA == "":
            return False

        return fileSHA

    try:
        baseFileContent = open(file_path, "r").read()

        asciiEncoded = baseFileContent.encode("ascii")
        base64Encoded = base64.b64encode(asciiEncoded)
        base64FileContent = base64Encoded.decode("ascii")

        payload = {}

        fileSHA = getFileSHA(file_name, repo_name, access_token)

        if fileSHA is False:
            payload = json.dumps(
                {
                    "message": f"Added {file_name}",
                    "content": base64FileContent,
                }
            )
        else:
            payload = json.dumps(
                {
                    "message": f"Updated {file_name}",
                    "content": base64FileContent,
                    "sha": fileSHA,
                }
            )

        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        url = f"https://api.github.com/repos/{repo_name}/contents/{file_name}"

        print(headers)

        response = requests.request("PUT", url, headers=headers, data=payload)

        print(response.status_code, response.json())
        if response.status_code == 200:
            return response.json()
        else:
            return "FAILURE"
    except Exception as e:
        raise e


def getUserRepositories(access_token):
    def getGithubRepos(page):
        url = f"https://api.github.com/user/repos?per_page=100&page={page}"

        payload = {}
        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.request("GET", url, headers=headers, data=payload)

        return response.json()

    page = 1
    fullRepoList = []

    try:
        while True:
            reposPage = getGithubRepos(page)
            fullRepoList.extend(reposPage)
            page += 1
            if len(reposPage) < 100:
                break

        return fullRepoList
    except Exception as e:
        raise e
