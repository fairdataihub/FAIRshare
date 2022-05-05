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

        import requests

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

            url = f"https://api.figshare.com/v2/account/articles/{article_id}/authors/{figshare_author_id}"  # noqa: E501

            payload = {}
            headers = {
                "Authorization": f"token {access_token}",
            }

            response = requests.request("DELETE", url, headers=headers, data=payload)

            if response.status_code == 204:
                return article_id
            else:
                return "ERROR"
        else:
            return article_id
    else:
        return "ERROR"
