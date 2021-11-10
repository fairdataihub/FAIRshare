from __future__ import print_function
import config
from flask import Flask

from flask_cors import CORS
from flask_restx import Api, Resource, reqparse
from zenodo import (
    getAllZenodoDepositions,
    createNewZenodoDeposition,
    uploadFileToZenodoDeposition,
    addMetadataToZenodoDeposition,
    publishZenodoDeposition,
)


API_VERSION = "0.0.1"


app = Flask(__name__)
app.config.SWAGGER_UI_DOC_EXPANSION = 'list' # full if you want to see all the details
CORS(app)

api = Api(
    app,
    version=API_VERSION,
    title="SODA for COVID-19 Research backend api",
    description="The backend api system for the Electron Vue app",
    doc="/docs",
)


@api.route("/api_version", endpoint="apiVersion")
class ApiVersion(Resource):
    def get(self):
        """Returns the semver version number of the current API"""
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
# Zenodo API documentation
###############################################################################

zenodo = api.namespace("zenodo", description="Zenodo operations")


@zenodo.route("/env", endpoint="zenodoURL")
class zenodoURL(Resource):
    def get(self):
        """Returns the zenodo endpoint url. If the response is sandbox.zenodo.org, this corresponds to the testing environment. zenodo.org only will correspond to the production environment."""
        return config.ZENODO_SERVER_URL


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


@zenodo.route("/new", endpoint="zenodoCreateNew")
class zenodoCreateNew(Resource):
    @zenodo.doc(
        responses={200: "Success", 401: "Authentication error"},
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


@zenodo.route("/upload", endpoint="zenodoUploadFile")
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


@zenodo.route("/metadata", endpoint="zenodoAddMetadata")
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
        '''Add metadata to a zenodo deposition'''
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
        metadata = json.load(args["metadata"])

        return addMetadataToZenodoDeposition(access_token, deposition_id, metadata)


@zenodo.route("/publish", endpoint="zenodoPublish")
class zenodoPublish(Resource):
    @zenodo.doc(
        responses={200: "Success", 401: "Authentication error"},
        params={
            "access_token": "Zenodo access token required with every request.",
        },
    )
    def post(self):
        '''Publish a zenodo deposition'''
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


# KEY

# 5000 is the flask default port.
# Using 7632 since it spells SODA lol.
# Remove `debug=True` when creating the standalone pyinstaller file
if __name__ == "__main__":
    # app.run(host="127.0.0.1", port=7632)
    app.run(host="127.0.0.1", port=7632, debug=True)
