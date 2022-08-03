import base64
import json
import uuid

import requests


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

        asciiEncoded = baseFileContent.encode()
        base64Encoded = base64.b64encode(asciiEncoded)
        base64FileContent = base64Encoded.decode()

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
        url = f"https://api.github.com/user/repos?per_page=100&page={page}&affiliation=owner,organization_member"  # noqa E501

        payload = {}
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"Bearer {access_token}",
        }

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


def getRepoContributors(access_token, owner, repo):
    def getContributors(page):
        url = f"https://api.github.com/repos/{owner}/{repo}/contributors?per_page=100&page={page}"  # noqa E501

        payload = {}
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"Bearer {access_token}",
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        return response.json()

    page = 1
    fullContributorList = []

    try:
        while True:
            contributorsPage = getContributors(page)
            fullContributorList.extend(contributorsPage)
            page += 1
            if len(contributorsPage) < 100:
                break

        return fullContributorList
    except Exception as e:
        raise e


def getRepoReleases(access_token, owner, repo):
    def getReleases(page):
        url = f"https://api.github.com/repos/{owner}/{repo}/releases?per_page=100&page={page}"  # noqa E501

        payload = {}
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"Bearer {access_token}",
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        return response.json()

    page = 1
    fullReleasesList = []

    try:
        while True:
            releasesPage = getReleases(page)
            fullReleasesList.extend(releasesPage)
            page += 1
            if len(releasesPage) < 100:
                break

        return fullReleasesList
    except Exception as e:
        raise e


def getRepoContentTree(access_token, owner, repo):
    def getRepoTree(branch):
        def createContentTree(inputTreeArray):
            def addFolderToTree(fullTree, item):
                fullPath = item["path"]
                splitPaths = fullPath.split("/")

                if len(splitPaths) == 1:
                    if fullPath not in fullTree:
                        fullTree[fullPath] = {
                            "sha": item["sha"],
                            "url": item["url"],
                            "path": item["path"],
                            "type": "tree",
                            "children": {},
                        }
                else:
                    tree = fullTree
                    for path in splitPaths:
                        if path not in tree:
                            tree[path] = {
                                "sha": item["sha"],
                                "url": item["url"],
                                "path": item["path"],
                                "type": "tree",
                                "children": {},
                            }
                        else:
                            tree = tree[path]["children"]
                return

            def addFileToTree(fullTree, item):
                fullPath = item["path"]
                splitPaths = fullPath.split("/")

                if len(splitPaths) == 1:
                    if fullPath not in fullTree:
                        fullTree[fullPath] = {
                            "sha": item["sha"],
                            "url": item["url"],
                            "size": item["size"],
                            "path": item["path"],
                            "type": "blob",
                        }
                else:
                    tree = fullTree
                    for path in splitPaths:
                        if path not in tree:
                            tree[path] = {
                                "sha": item["sha"],
                                "url": item["url"],
                                "size": item["size"],
                                "path": item["path"],
                                "type": "blob",
                            }
                        else:
                            tree = tree[path]["children"]
                return

            contentTree = {}

            for item in inputTreeArray:
                if item["type"] == "tree":
                    addFolderToTree(contentTree, item)
                elif item["type"] == "blob":
                    addFileToTree(contentTree, item)

            return contentTree

        def convertContentTree(contentTree):

            outputList = []
            for item in contentTree:
                if "children" in contentTree[item]:
                    outputList.append(
                        {
                            "id": uuid.uuid1().int,
                            "label": item,
                            "sha": contentTree[item]["sha"],
                            "url": contentTree[item]["url"],
                            "path": contentTree[item]["path"],
                            "type": contentTree[item]["type"],
                            "isLeaf": False,
                            "children": convertContentTree(
                                contentTree[item]["children"]
                            ),
                        }
                    )
                else:
                    outputList.append(
                        {
                            "id": uuid.uuid1().int,
                            "label": item,
                            "sha": contentTree[item]["sha"],
                            "url": contentTree[item]["url"],
                            "size": contentTree[item]["size"],
                            "path": contentTree[item]["path"],
                            "type": contentTree[item]["type"],
                            "isLeaf": True,
                        }
                    )

            return outputList

        url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=true"  # noqa E501

        payload = {}
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"Bearer {access_token}",
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        res = response.json()

        if res["truncated"] is False:
            contentTree = createContentTree(res["tree"])
            convertedContentTree = convertContentTree(contentTree)
            return convertedContentTree
        else:
            # get simplified tree
            # THIS ONE NEEDS TO CHANGE
            contentTree = createContentTree(res["tree"])
            convertedContentTree = convertContentTree(contentTree)
            return convertedContentTree

    def getDefaultBranch():
        url = f"https://api.github.com/repos/{owner}/{repo}"

        payload = {}
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"Bearer {access_token}",
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        res = response.json()
        return res["default_branch"] if "default_branch" in res else "master"

    defaultBranch = getDefaultBranch()

    contentTree = getRepoTree(defaultBranch)
    return json.dumps(contentTree)


def getFileFromRepo(access_token, owner, repo, file_name):
    try:
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_name}"

        payload = {}
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"Bearer {access_token}",
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code != 200:
            return "NOT_FOUND"

        response = response.json()

        if "content" not in response:
            return "NOT_FOUND"
        base64EncodedContent = response["content"]
        asciiEncoded = base64EncodedContent.encode("ascii")
        base64Decoded = base64.b64decode(asciiEncoded)
        return base64Decoded.decode("ascii")
    except Exception as e:
        raise e


def getRepoZipball(access_token, repo, default_branch, file_path):
    try:
        url = f"https://api.github.com/repos/{repo}/zipball/{default_branch}"

        payload = {}
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"Bearer {access_token}",
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code != 200:
            return "NOT_FOUND"

        with open(file_path, "wb") as fc:
            fc.write(response.content)

    except Exception as e:
        raise e
