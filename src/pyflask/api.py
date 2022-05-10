import json
import logging
import logging.handlers
import os
import sys

import config
from biotools import getUserDetails, loginToBioTools, registerTool, validateTool
from figshare import (
    createNewFigshareItem,
    deleteFigshareArticle,
    getFigshareFileUploadStatus,
    uploadFileToFigshare,
    publishFigshareArticle,
)
from flask import Flask, request
from flask_cors import CORS
from flask_restx import Api, Resource, reqparse
from github import (
    getFileFromRepo,
    getRepoContentTree,
    getRepoContributors,
    getRepoReleases,
    getUserRepositories,
    uploadFileToGithub,
)
from metadata import createCitationCFF, createMetadata
from utilities import (
    createFile,
    deleteFile,
    fileExistInFolder,
    foldersPresent,
    openFileExplorer,
    readFolderContents,
    requestJSON,
    zipFolder,
)
from zenodo import (
    addMetadataToZenodoDeposition,
    createNewZenodoDeposition,
    createNewZenodoDepositionVersion,
    deleteZenodoDeposition,
    getAllZenodoDepositions,
    getAZenodoDeposition,
    publishZenodoDeposition,
    removeFileFromZenodoDeposition,
    uploadFileToZenodoDeposition,
)

API_VERSION = "1.4.0"


app = Flask(__name__)
# full if you want to see all the details
app.config.SWAGGER_UI_DOC_EXPANSION = "list"
CORS(app)

# configure root logger
LOG_FOLDER = os.path.join(os.path.expanduser("~"), ".fairshare", "logs")
LOG_FILENAME = "api.log"
LOG_PATH = os.path.join(LOG_FOLDER, LOG_FILENAME)

if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)

# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler(
    LOG_PATH, maxBytes=5 * 1024 * 1024, backupCount=3
)

# create logging formatter
logFormatter = logging.Formatter(
    fmt="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
handler.setFormatter(logFormatter)

app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)

api = Api(
    app,
    version=API_VERSION,
    title="FAIRshare backend api",
    description="The backend api system for the Electron Vue app",
    doc="/docs",
)


@api.route("/fairshare_server_shutdown", endpoint="shutdown")
class Shutdown(Resource):
    def post(self):
        func = request.environ.get("werkzeug.server.shutdown")
        api.logger.info("Shutting down server")

        if func is None:
            print("Not running with the Werkzeug Server")
            return

        func()


@api.route("/api_version", endpoint="apiVersion")
class ApiVersion(Resource):
    def get(self):
        """Returns the semver version number of the current API"""
        api.logger.info(f"API_VERSION: {API_VERSION}")
        return API_VERSION


@api.route("/echo", endpoint="echo")
class HelloWorld(Resource):
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def get(self):
        """Returns a simple 'Server Active' message"""

        response = "Server active!"

        return response


###############################################################################
# bio.tools operations
###############################################################################

biotools = api.namespace("biotools", description="bio.tools operations")


@biotools.route("/env", endpoint="BiotoolsURL")
class BiotoolsURL(Resource):
    def get(self):
        """Returns the bio.tools endpoint url. If the response is dev.bio.tools, this corresponds to the testing environment. bio.tools only will correspond to the production environment."""  # noqa: E501
        return config.BIO_TOOLS_SERVER_URL


@biotools.route("/login", endpoint="BioToolsLogin")
class BioToolsLogin(Resource):
    @biotools.doc(
        responses={200: "Success"},
        params={
            "username": "Username of the account",
            "password": "Password of the account",
        },
    )
    def post(self):
        """Login to bio.tools"""

        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, required=True)
        parser.add_argument("password", type=str, required=True)
        args = parser.parse_args()

        username = args["username"]
        password = args["password"]

        return loginToBioTools(username, password)


@biotools.route("/user", endpoint="BioToolsUserDetails")
class BioToolsUserDetails(Resource):
    @biotools.doc(
        responses={200: "Success"},
        params={
            "token": "Token of the account",
        },
    )
    def get(self):
        """Get user details"""

        parser = reqparse.RequestParser()
        parser.add_argument("token", type=str, required=True)
        args = parser.parse_args()

        token = args["token"]

        return getUserDetails(token)


@biotools.route("/tool/validate", endpoint="BioToolsValidate")
class BioToolsValidate(Resource):
    @biotools.doc(
        responses={200: "Success"},
        params={
            "token": "Token of the account",
            "data": "Data to validate",
        },
    )
    def post(self):
        """Validate data"""

        parser = reqparse.RequestParser()
        parser.add_argument("token", type=str, required=True)
        parser.add_argument("data", type=str, required=True)
        args = parser.parse_args()

        token = args["token"]
        data = json.loads(args["data"])

        return validateTool(token, data)


@biotools.route("/tool/register", endpoint="BioToolsRegisterTool")
class BioToolsRegisterTool(Resource):
    @biotools.doc(
        responses={200: "Success"},
        params={
            "token": "Token of the account",
            "data": "Data for tool registration",
        },
    )
    def post(self):
        """Register a new tool"""

        parser = reqparse.RequestParser()
        parser.add_argument("token", type=str, required=True)
        parser.add_argument("data", type=str, required=True)
        args = parser.parse_args()

        token = args["token"]
        data = json.loads(args["data"])

        return registerTool(token, data)


###############################################################################
# Metadata operations
###############################################################################

metadata = api.namespace("metadata", description="Metadata operations")


@metadata.route("/create", endpoint="CreateMetadata")
class CreateMetadata(Resource):
    @metadata.doc(
        responses={200: "Success"},
        params={
            "data_types": "Types of data.",
            "data_object": "Full data object to create metadata from. Should have keys from the `data_types` parameter",  # noqa: E501
            "virtual_file": "Parameter to generate a virtual file",
        },
    )
    def post(self):
        """Create the codemetadata json file"""
        parser = reqparse.RequestParser()

        parser.add_argument("data_types", type=str, help="Types of data ")
        parser.add_argument(
            "data_object",
            type=str,
            help="Complete data object to create metadata",
        )
        parser.add_argument(
            "virtual_file",
            type=bool,
            help="Parameter to generate a virtual file",
        )

        args = parser.parse_args()

        data_types = json.loads(args["data_types"])
        data = json.loads(args["data_object"])
        virtual_file = args["virtual_file"]

        return createMetadata(data_types, data, virtual_file)


@metadata.route("/citation/create", endpoint="CreateCitationCFF")
class CreateCitationCFF(Resource):
    @metadata.doc(
        responses={200: "Success"},
        params={
            "data_types": "Types of data.",
            "data_object": "Full data object to create metadata from. Should have keys from the `data_types` parameter",  # noqa: E501
            "virtual_file": "Parameter to generate a virtual file",
        },
    )
    def post(self):
        """Create the citation cff file"""
        parser = reqparse.RequestParser()

        parser.add_argument("data_types", type=str, help="Types of data ")
        parser.add_argument(
            "data_object",
            type=str,
            help="Complete data object to create metadata",
        )
        parser.add_argument(
            "virtual_file",
            type=bool,
            help="Parameter to generate a virtual file",
        )

        args = parser.parse_args()

        data_types = json.loads(args["data_types"])
        data = json.loads(args["data_object"])
        virtual_file = args["virtual_file"]

        return createCitationCFF(data_types, data, virtual_file)


###############################################################################
# Figshare operations
###############################################################################

figshare = api.namespace("figshare", description="Figshare operations")


@figshare.route("/item", endpoint="FigshareItem")
class FigshareItem(Resource):
    @figshare.doc(
        responses={200: "Success", 401: "Authentication error"},
        params={
            "access_token": "figshare access token required with every request.",
            "metadata": "json string with metadata to add to the item",
        },
    )
    def post(self):
        """Create a new figshare article and add metadata. Returns the figshare article id."""  # noqa: E501
        parser = reqparse.RequestParser()

        parser.add_argument(
            "access_token",
            type=str,
            required=True,
            help="access_token is required. accessToken needs to be of type str",
        )
        parser.add_argument(
            "metadata",
            type=str,
            required=True,
            help="metadata is required. metadata needs to be a json string",
        )

        args = parser.parse_args()

        access_token = args["access_token"]
        metadata = args["metadata"]

        return createNewFigshareItem(access_token, metadata)

    @figshare.doc(
        responses={200: "Success", 401: "Authentication error"},
        params={
            "access_token": "figshare access token required with every request.",
            "article_id": "article id for the item",
        },
    )
    def delete(self):
        """Delete a zenodo deposition"""
        parser = reqparse.RequestParser()

        parser.add_argument(
            "access_token",
            type=str,
            required=True,
            help="access_token is required. accessToken needs to be of type str",
        )
        parser.add_argument(
            "article_id",
            type=str,
            required=True,
            help="article_id is required. article_id needs to be of type str",
        )

        args = parser.parse_args()

        access_token = args["access_token"]
        article_id = args["article_id"]

        return deleteFigshareArticle(access_token, article_id)


@figshare.route("/item/publish", endpoint="FigsharePublish")
class FigsharePublish(Resource):
    @figshare.doc(
        responses={200: "Success", 401: "Authentication error"},
        params={
            "access_token": "Figshare access token required with every request",
            "article_id": "article id for the item",
        },
    )
    def post(self):
        """Publish a Figshare article"""
        parser = reqparse.RequestParser()

        parser.add_argument(
            "access_token",
            type=str,
            required=True,
            help="access_token is required. accessToken needs to be of type str",
        )
        parser.add_argument(
            "article_id",
            type=str,
            required=True,
            help="article_id is required. article_id needs to be of type str",
        )

        args = parser.parse_args()

        access_token = args["access_token"]
        article_id = args["article_id"]

        return publishFigshareArticle(access_token, article_id)


@figshare.route("/item/files/upload", endpoint="FigshareFileUpload")
class FigshareFileUpload(Resource):
    @figshare.doc(
        responses={200: "Success", 401: "Authentication error"},
        params={
            "access_token": "figshare access token required with every request.",
            "article_id": "figshare article id",
            "file_path": "path to the file to upload",
        },
    )
    def post(self):
        """Upload file to Figshare"""
        parser = reqparse.RequestParser()

        parser.add_argument(
            "access_token",
            type=str,
            required=True,
            help="access_token is required. accessToken needs to be of type str",
        )
        parser.add_argument(
            "article_id",
            type=str,
            required=True,
            help="article_id is required. article_id needs to be of type str",
        )
        parser.add_argument(
            "file_path",
            type=str,
            required=True,
            help="file_path is required. file_path needs to be of type str",
        )

        args = parser.parse_args()

        access_token = args["access_token"]
        article_id = args["article_id"]
        file_path = args["file_path"]

        return uploadFileToFigshare(access_token, article_id, file_path)

    @figshare.doc(
        responses={200: "Success", 401: "Authentication error"},
        params={},
    )
    def get(self):
        """Get file upload status"""

        return getFigshareFileUploadStatus()


###############################################################################
# Zenodo API operations
###############################################################################

zenodo = api.namespace("zenodo", description="Zenodo operations")


@zenodo.route("/env", endpoint="zenodoURL")
class zenodoURL(Resource):
    def get(self):
        """Returns the zenodo endpoint url. If the response is sandbox.zenodo.org, this corresponds to the testing environment. zenodo.org only will correspond to the production environment."""  # noqa: E501
        return config.ZENODO_SERVER_URL


@zenodo.route("/deposition", endpoint="zenodoDeposition")
class zenodoDeposition(Resource):
    @zenodo.doc(
        responses={
            200: "Success",
            401: "Authentication error",
            400: "Bad request",
        },
        params={"access_token": "Zenodo access token required with every request."},
    )
    def post(self):
        """Create a new empty Zenodo deposition"""
        parser = reqparse.RequestParser()

        parser.add_argument(
            "access_token",
            type=str,
            required=True,
            help="access_token is required. accessToken needs to be of type str",
        )

        args = parser.parse_args()

        access_token = args["access_token"]

        response = createNewZenodoDeposition(access_token)
        return response

    @zenodo.doc(
        responses={200: "Success", 401: "Authentication error"},
        params={
            "access_token": "Zenodo access token required with every request.",
            "deposition_id": "Zenodo deposition id. For new versions the new deposit id is required",  # noqa: E501
        },
    )
    def get(self):
        """Get a single Zenodo deposition"""
        parser = reqparse.RequestParser()

        parser.add_argument(
            "access_token",
            type=str,
            required=True,
            help="access_token is required. accessToken needs to be of type str",
        )
        parser.add_argument(
            "deposition_id",
            type=str,
            required=True,
            help="deposition_id is required. deposition_id needs to be of type str",
        )

        args = parser.parse_args()

        access_token = args["access_token"]
        deposition_id = args["deposition_id"]

        response = getAZenodoDeposition(access_token, deposition_id)
        return response

    @zenodo.doc(
        responses={200: "Success", 401: "Authentication error"},
        params={
            "access_token": "Zenodo access token required with every request.",
            "deposition_id": "Zenodo deposition id. For new versions the new deposit id is required",  # noqa: E501
        },
    )
    def delete(self):
        """Delete a zenodo deposition"""
        parser = reqparse.RequestParser()

        parser.add_argument(
            "access_token",
            type=str,
            required=True,
            help="access_token is required. accessToken needs to be of type str",
        )
        parser.add_argument(
            "deposition_id",
            type=str,
            required=True,
            help="deposition_id is required. deposition_id needs to be of type str",
        )

        args = parser.parse_args()

        access_token = args["access_token"]
        deposition_id = args["deposition_id"]

        return deleteZenodoDeposition(access_token, deposition_id)


@zenodo.route("/depositions", endpoint="zenodoGetAll")
class zenodoGetAll(Resource):
    @zenodo.doc(
        responses={200: "Success", 401: "Authentication error"},
        params={"access_token": "Zenodo access token required with every request."},
    )
    def get(self):
        """Get a list of all the Zenodo depositions"""
        parser = reqparse.RequestParser()

        parser.add_argument(
            "access_token",
            type=str,
            required=True,
            help="access_token is required. accessToken needs to be of type str",
        )

        args = parser.parse_args()

        access_token = args["access_token"]

        response = getAllZenodoDepositions(access_token)
        return response


@zenodo.route("/deposition/files/upload", endpoint="zenodoUploadFile")
class zenodoUploadFile(Resource):
    @zenodo.doc(
        responses={200: "Success", 401: "Authentication error"},
        params={
            "access_token": "Zenodo access token required with every request.",
            "bucket_url": "bucket url is found in zenodo.links.bucket",
            "file_path": "file path of file to upload",
        },
    )
    def post(self):
        """Upload a file into a zenodo deposition"""
        parser = reqparse.RequestParser()

        parser.add_argument(
            "access_token",
            type=str,
            required=True,
            help="access_token is required. accessToken needs to be of type str",
        )
        parser.add_argument(
            "bucket_url",
            type=str,
            required=True,
            help="bucket_url is required. bucket_url needs to be of type str",
        )
        parser.add_argument(
            "file_path",
            type=str,
            required=True,
            help="file_path is required. accessToken needs to be of type str",
        )

        args = parser.parse_args()

        access_token = args["access_token"]
        bucket_url = args["bucket_url"]
        file_path = args["file_path"]

        return uploadFileToZenodoDeposition(access_token, bucket_url, file_path)


@zenodo.route("/deposition/metadata", endpoint="zenodoAddMetadata")
class zenodoAddMetadata(Resource):
    @zenodo.doc(
        responses={200: "Success", 401: "Authentication error"},
        params={
            "access_token": "Zenodo access token required with every request.",
            "deposition_id": "deposition id is found in zenodo.id",
            "metadata": "json string with metadata to add to the deposition",
        },
    )
    def post(self):
        """Add metadata to a zenodo deposition"""
        parser = reqparse.RequestParser()

        parser.add_argument(
            "access_token",
            type=str,
            required=True,
            help="access_token is required. accessToken needs to be of type str",
        )
        parser.add_argument(
            "deposition_id",
            type=str,
            required=True,
            help="deposition_id is required. deposition_id needs to be of type str",
        )
        parser.add_argument(
            "metadata",
            type=str,
            required=True,
            help="metadata is required. metadata needs to be a json string",
        )

        args = parser.parse_args()

        access_token = args["access_token"]
        deposition_id = args["deposition_id"]
        metadata = json.loads(args["metadata"])

        return addMetadataToZenodoDeposition(access_token, deposition_id, metadata)


@zenodo.route("/deposition/publish", endpoint="zenodoPublish")
class zenodoPublish(Resource):
    @zenodo.doc(
        responses={200: "Success", 401: "Authentication error"},
        params={
            "access_token": "Zenodo access token required with every request.",
            "deposition_id": "deposition id of the zenodo object",
        },
    )
    def post(self):
        """Publish a zenodo deposition"""
        parser = reqparse.RequestParser()

        parser.add_argument(
            "access_token",
            type=str,
            required=True,
            help="access_token is required. accessToken needs to be of type str",
        )
        parser.add_argument(
            "deposition_id",
            type=str,
            required=True,
            help="deposition_id is required. deposition_id needs to be of type str",
        )

        args = parser.parse_args()

        access_token = args["access_token"]
        deposition_id = args["deposition_id"]

        return publishZenodoDeposition(access_token, deposition_id)


@zenodo.route("/deposition/files", endpoint="zenodoDeleteFile")
class zenodoDeleteFile(Resource):
    @zenodo.doc(
        responses={200: "Success", 401: "Authentication error"},
        params={
            "access_token": "Zenodo access token required with every request.",
            "deposition_id": "deposition id of the zenodo object",
            "file_id": "file id of the file to delete",
        },
    )
    def delete(self):
        """Delete a zenodo deposition file"""
        parser = reqparse.RequestParser()

        parser.add_argument(
            "access_token",
            type=str,
            required=True,
            help="access_token is required. accessToken needs to be of type str",
        )
        parser.add_argument(
            "deposition_id",
            type=str,
            required=True,
            help="deposition_id is required. deposition_id needs to be of type str",
        )
        parser.add_argument(
            "file_id",
            type=str,
            required=True,
            help="file_id is required. file_id needs to be of type str",
        )

        args = parser.parse_args()

        access_token = args["access_token"]
        deposition_id = args["deposition_id"]
        file_id = args["file_id"]

        return removeFileFromZenodoDeposition(access_token, deposition_id, file_id)


@zenodo.route("/deposition/newversion", endpoint="zenodoNewVersion")
class zenodoNewVersion(Resource):
    @zenodo.doc(
        responses={200: "Success", 401: "Authentication error"},
        params={
            "access_token": "Zenodo access token required with every request.",
            "deposition_id": "deposition id of the zenodo object",
        },
    )
    def post(self):
        """Delete a zenodo deposition"""
        parser = reqparse.RequestParser()

        parser.add_argument(
            "access_token",
            type=str,
            required=True,
            help="access_token is required. accessToken needs to be of type str",
        )
        parser.add_argument(
            "deposition_id",
            type=str,
            required=True,
            help="deposition_id is required. deposition_id needs to be of type str",
        )

        args = parser.parse_args()

        access_token = args["access_token"]
        deposition_id = args["deposition_id"]

        return createNewZenodoDepositionVersion(access_token, deposition_id)


###############################################################################
# GitHub API endpoints
###############################################################################


github = api.namespace("github", description="GitHub operations")


@github.route("/upload", endpoint="uploadToGithub")
class uploadToGithub(Resource):
    @github.doc(
        responses={200: "Success", 401: "Validation error"},
        params={
            "access_token": "GitHub authorization token to upload files",
            "repo_name": "name of the repository to upload to",
            "file_name": "file name of file to upload",
            "file_path": "file path of file to upload",
        },
    )
    def post(self):
        """Upload a file into a GitHub repository"""
        parser = reqparse.RequestParser()

        parser.add_argument(
            "file_path",
            type=str,
            required=True,
            help="file path of file to upload. file_path needs to be of type str",
        )
        parser.add_argument(
            "file_name",
            type=str,
            required=True,
            help="file_name is required. file_name needs to be of type str",
        )
        parser.add_argument(
            "access_token",
            type=str,
            required=True,
            help="access_token is required. accessToken needs to be of type str",
        )
        parser.add_argument(
            "repo_name",
            type=str,
            required=True,
            help="repo_name is required. repo_name needs to be of type str",
        )

        args = parser.parse_args()

        access_token = args["access_token"]
        file_name = args["file_name"]
        file_path = args["file_path"]
        repo_name = args["repo_name"]

        return uploadFileToGithub(access_token, file_name, file_path, repo_name)


@github.route("/user/repos", endpoint="GetAllRepos")
class GetAllRepos(Resource):
    @github.doc(
        responses={200: "Success", 401: "Validation error"},
        params={
            "access_token": "GitHub authorization token for the user",
        },
    )
    def get(self):
        """Get all repositories for a user"""
        parser = reqparse.RequestParser()

        parser.add_argument(
            "access_token",
            type=str,
            required=True,
            help="access_token is required. accessToken needs to be of type str",
        )

        args = parser.parse_args()

        access_token = args["access_token"]

        return getUserRepositories(access_token)


@github.route("/repo/contributors", endpoint="GetAllContributorsForRepo")
class GetAllContributorsForRepo(Resource):
    @github.doc(
        responses={200: "Success", 401: "Validation error"},
        params={
            "access_token": "GitHub authorization token for the user",
            "owner": "owner of the repository",
            "repo": "repository name",
        },
    )
    def get(self):
        """Get all contributors for a repository"""
        parser = reqparse.RequestParser()

        parser.add_argument(
            "access_token",
            type=str,
            required=True,
            help="access_token is required. accessToken needs to be of type str",
        )
        parser.add_argument(
            "owner",
            type=str,
            required=True,
            help="owner is required. owner needs to be of type str",
        )
        parser.add_argument(
            "repo",
            type=str,
            required=True,
            help="repo is required. repo needs to be of type str",
        )

        args = parser.parse_args()

        access_token = args["access_token"]
        owner = args["owner"]
        repo = args["repo"]

        return getRepoContributors(access_token, owner, repo)


@github.route("/repo/releases", endpoint="GetAllReleasesForRepo")
class GetAllReleasesForRepo(Resource):
    @github.doc(
        responses={200: "Success", 401: "Validation error"},
        params={
            "access_token": "GitHub authorization token for the user",
            "owner": "owner of the repository",
            "repo": "repository name",
        },
    )
    def get(self):
        """Get all releases for a repository"""
        parser = reqparse.RequestParser()

        parser.add_argument(
            "access_token",
            type=str,
            required=True,
            help="access_token is required. accessToken needs to be of type str",
        )
        parser.add_argument(
            "owner",
            type=str,
            required=True,
            help="owner is required. owner needs to be of type str",
        )
        parser.add_argument(
            "repo",
            type=str,
            required=True,
            help="repo is required. repo needs to be of type str",
        )

        args = parser.parse_args()

        access_token = args["access_token"]
        owner = args["owner"]
        repo = args["repo"]

        return getRepoReleases(access_token, owner, repo)


@github.route("/repo/tree", endpoint="getRepoContentsTree")
class getRepoContentsTree(Resource):
    @github.doc(
        responses={200: "Success", 401: "Validation error"},
        params={
            "access_token": "GitHub authorization token for the user",
            "owner": "owner of the repository",
            "repo": "repository name",
        },
    )
    def get(self):
        """Get repository contents as a tree"""
        parser = reqparse.RequestParser()

        parser.add_argument(
            "access_token",
            type=str,
            required=True,
            help="access_token is required. accessToken needs to be of type str",
        )
        parser.add_argument(
            "owner",
            type=str,
            required=True,
            help="owner is required. owner needs to be of type str",
        )
        parser.add_argument(
            "repo",
            type=str,
            required=True,
            help="repo is required. repo needs to be of type str",
        )

        args = parser.parse_args()

        access_token = args["access_token"]
        owner = args["owner"]
        repo = args["repo"]

        return getRepoContentTree(access_token, owner, repo)


@github.route("/repo/file/contents", endpoint="getRepoFileContents")
class getRepoFileContents(Resource):
    @github.doc(
        responses={200: "Success", 401: "Validation error"},
        params={
            "access_token": "GitHub authorization token for the user",
            "owner": "owner of the repository",
            "repo": "repository name",
            "file_name": "name of file to be read",
        },
    )
    def get(self):
        """Get the contents of a file in a repository"""
        parser = reqparse.RequestParser()

        parser.add_argument(
            "access_token",
            type=str,
            required=True,
            help="access_token is required. accessToken needs to be of type str",
        )
        parser.add_argument(
            "owner",
            type=str,
            required=True,
            help="owner is required. owner needs to be of type str",
        )
        parser.add_argument(
            "repo",
            type=str,
            required=True,
            help="repo is required. repo needs to be of type str",
        )
        parser.add_argument(
            "file_name",
            type=str,
            required=True,
            help="file_name is required. fileName needs to be of type str",
        )

        args = parser.parse_args()

        access_token = args["access_token"]
        owner = args["owner"]
        repo = args["repo"]
        file_name = args["file_name"]

        return getFileFromRepo(access_token, owner, repo, file_name)


###############################################################################
# Utilities
###############################################################################


utilities = api.namespace("utilities", description="utilities for random tasks")


@utilities.route("/checkforfolders", endpoint="checkForFolders")
class checkForFolders(Resource):
    @utilities.doc(
        responses={200: "Success", 400: "Validation error"},
        params={
            "folder_path": "folder path to check if sub folders are present.",
        },
    )
    def post(self):
        """Checks if folders are present in the currently provided path"""
        parser = reqparse.RequestParser()

        parser.add_argument(
            "folder_path",
            type=str,
            required=True,
            help="folder path to check if sub folders are present.",
        )

        args = parser.parse_args()

        folder_path = args["folder_path"]

        return foldersPresent(folder_path)


@utilities.route("/zipfolder", endpoint="ZipFolder")
class ZipFolder(Resource):
    @utilities.doc(
        responses={200: "Success", 400: "Validation error"},
        params={
            "folder_path": "folder path to zip.",
        },
    )
    def post(self):
        """Zips a folder"""
        parser = reqparse.RequestParser()

        parser.add_argument(
            "folder_path",
            type=str,
            required=True,
            help="folder path to zip.",
        )

        args = parser.parse_args()

        folder_path = args["folder_path"]

        return zipFolder(folder_path)


@utilities.route("/deletefile", endpoint="deleteFile")
class DeleteFile(Resource):
    @utilities.doc(
        responses={200: "Success", 400: "Validation error"},
        params={
            "file_path": "file path to delete.",
        },
    )
    def delete(self):
        """Deletes a file"""
        parser = reqparse.RequestParser()

        parser.add_argument(
            "file_path",
            type=str,
            required=True,
            help="file path to delete.",
        )

        args = parser.parse_args()

        file_path = args["file_path"]
        return deleteFile(file_path)


@utilities.route("/requestjson", endpoint="RequestJSON")
class RequestJSON(Resource):
    @utilities.doc(
        responses={200: "Success", 400: "Validation error"},
        params={
            "url": "url to request from the web.",
        },
    )
    def get(self):
        """request a json file from the web"""
        parser = reqparse.RequestParser()

        parser.add_argument(
            "url",
            type=str,
            required=True,
            help="url that needs a CORS proxy",
        )

        args = parser.parse_args()

        url = args["url"]
        return requestJSON(url)


@utilities.route("/createfile", endpoint="CreateFile")
class CreateFile(Resource):
    @utilities.doc(
        responses={200: "Success", 400: "Validation error"},
        params={
            "file_name": "name of the file to generate",
            "folder_path": "folder path to generate files in",
            "file_content": "content of the file. Will be string",
            "content_type": "content type to determine what it is written with",
        },
    )
    def post(self):
        """create a file in the provided folder path"""
        parser = reqparse.RequestParser()

        parser.add_argument(
            "folder_path",
            type=str,
            required=True,
            help="folder path to generate files in",
        )
        parser.add_argument(
            "file_name",
            type=str,
            required=True,
            help="name of the file to generate",
        )
        parser.add_argument(
            "file_content",
            type=str,
            required=True,
            help="content of the file",
        )
        parser.add_argument(
            "content_type",
            type=str,
            required=True,
            help="content type to determine what it is written with",
        )

        args = parser.parse_args()

        folder_path = args["folder_path"]
        file_name = args["file_name"]
        file_content = args["file_content"]
        content_type = args["content_type"]

        if content_type == "text":
            # No need to do anything
            pass

        if content_type == "json":
            # This might not be necessary but adding
            # this in case there are some weird json inconsistencies.
            file_content = json.loads(file_content)

        return createFile(folder_path, file_name, file_content, content_type)


@utilities.route("/openfileexplorer", endpoint="OpenFileExplorer")
class OpenFileExplorer(Resource):
    @utilities.doc(
        responses={200: "Success", 400: "Validation error"},
        params={
            "file_path": "file path to open the explorer window at",
        },
    )
    def post(self):
        """create a file in the provided folder path"""
        parser = reqparse.RequestParser()

        parser.add_argument(
            "file_path",
            type=str,
            required=True,
            help="file path to open file explorer at",
        )
        args = parser.parse_args()
        file_path = args["file_path"]

        return openFileExplorer(file_path)


@utilities.route("/readfoldercontents", endpoint="ReadFolderContents")
class ReadFolderContents(Resource):
    @utilities.doc(
        responses={200: "Success", 400: "Validation error"},
        params={
            "folder_path": "read file names from the selected directory recursively",  # noqa:501
        },
    )
    def post(self):
        """read files in the provided folder path"""
        parser = reqparse.RequestParser()

        parser.add_argument(
            "folder_path",
            type=str,
            required=True,
            help="folder path to read files at",
        )
        args = parser.parse_args()
        folder_path = args["folder_path"]

        return readFolderContents(folder_path)


@utilities.route("/fileexistinfolder", endpoint="FileExistInFolder")
class FileExistInFolder(Resource):
    @utilities.doc(
        responses={200: "Success", 400: "Validation error"},
        params={
            "folder_path": "check if the file exists in the folder",  # noqa:501
            "file_name": "name of the target file",
        },
    )
    def post(self):
        """read files in the provided folder path"""
        parser = reqparse.RequestParser()

        parser.add_argument(
            "folder_path",
            type=str,
            required=True,
            help="folder path to find files at",
        )
        parser.add_argument(
            "file_name",
            type=str,
            required=True,
            help="name of the target file",
        )
        args = parser.parse_args()
        folder_path = args["folder_path"]
        file_name = args["file_name"]
        return fileExistInFolder(folder_path, file_name)


# 5000 is the flask default port.
# Using 7632 since it spells SODA lol.
# Remove `debug=True` when creating the standalone pyinstaller file
if __name__ == "__main__":
    requested_port = 5000  # default port to run on

    # Check for a port override
    if len(sys.argv) > 1:
        requested_port = int(sys.argv[1])

    api.logger.info(f"PORT_NUMBER: {requested_port}")

    print(f"Running on port {requested_port}.")
    print(f"API documentation hosted at http://127.0.0.1:{requested_port}/docs")

    api.logger.info("Starting FAIRshare server")

    app.run(host="127.0.0.1", port=requested_port)
    # app.run(host="127.0.0.1", port=requested_port, debug=True)
