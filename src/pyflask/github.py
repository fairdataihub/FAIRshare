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
        url = f"https://api.github.com/repos/{owner}/{repo}/contributors?per_page=100&page={page}"

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
                            "children": {},
                        }
                else:
                    tree = fullTree
                    for path in splitPaths:
                        if path not in tree:
                            tree[path] = {
                                "sha": item["sha"],
                                "url": item["url"],
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
                        }
                else:
                    tree = fullTree
                    for path in splitPaths:
                        if path not in tree:
                            tree[path] = {
                                "sha": item["sha"],
                                "url": item["url"],
                                "size": item["size"],
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
                            "label": item,
                            "sha": contentTree[item]["sha"],
                            "url": contentTree[item]["url"],
                            "children": convertContentTree(
                                contentTree[item]["children"]
                            ),
                        }
                    )
                else:
                    outputList.append(
                        {
                            "label": item,
                            "sha": contentTree[item]["sha"],
                            "url": contentTree[item]["url"],
                            "size": contentTree[item]["size"],
                        }
                    )

            return outputList

        url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=true"

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
        if "default_branch" in res:
            return res["default_branch"]
        else:
            return "master"

    defaultBranch = getDefaultBranch()

    # print(defaultBranch)
    # defaultBranch = "main"

    contentTree = getRepoTree(defaultBranch)
    return contentTree
