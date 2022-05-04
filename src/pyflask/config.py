from dotenv import dotenv_values

ZENODO_SERVER_URL = "https://zenodo.org/api"
BIO_TOOLS_SERVER_URL = "https://bio.tools/api"
FIGSHARE_SERVER_URL = "https://api.figshare.com/v2"

# take environment variables from .env.local
envcfg = dotenv_values(".env.local")

if "VUE_APP_ZENODO_SERVER_URL" in envcfg:
    ZENODO_SERVER_URL = envcfg["VUE_APP_ZENODO_SERVER_URL"]

if "VUE_APP_BIO_TOOLS_SERVER_URL" in envcfg:
    BIO_TOOLS_SERVER_URL = envcfg["VUE_APP_BIO_TOOLS_SERVER_URL"]

print("ZENODO_SERVER_URL:", ZENODO_SERVER_URL)
print("BIO_TOOLS_SERVER_URL:", BIO_TOOLS_SERVER_URL)
print("FIGSHARE_SERVER_URL:", FIGSHARE_SERVER_URL)
