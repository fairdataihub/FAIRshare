from dotenv import dotenv_values

ZENODO_SERVER_URL = "https://zenodo.org/api/"
GITHUB_SERVER_URL = "https://api.github.com"

envcfg = dotenv_values(".env.local")  # take environment variables from .env.local

if "VUE_APP_ZENODO_SERVER_URL" in envcfg:
    ZENODO_SERVER_URL = envcfg["VUE_APP_ZENODO_SERVER_URL"]

print("ZENODO_SERVER_URL:", ZENODO_SERVER_URL)
