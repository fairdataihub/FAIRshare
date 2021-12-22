from __future__ import print_function
import json
import os


def createCodeMetadata(code_data, general_data, folder_path):
    metadata = {
        "@context": "https://doi.org/10.5063/schema/codemeta-2.0",
        "@type": "SoftwareSourceCode",
    }

    if "license" in code_data:
        metadata["license"] = "https://spdx.org/licenses/" + code_data["license"]

    if "codeRepository" in code_data:
        if code_data["codeRepository"] != "":
            metadata["codeRepository"] = code_data["codeRepository"]

    if "continuousIntegration" in code_data:
        if code_data["continuousIntegration"] != "":
            metadata["contIntegration"] = code_data["continuousIntegration"]

    if "creationDate" in code_data:
        if code_data["creationDate"] != "":
            metadata["dateCreated"] = code_data["creationDate"]

    if "firstReleaseDate" in code_data:
        if code_data["firstReleaseDate"] != "":
            metadata["dateCreated"] = code_data["firstReleaseDate"]

    if "currentVersionReleaseDate" in code_data:
        if code_data["currentVersionReleaseDate"] != "":
            metadata["dateModified"] = code_data["currentVersionReleaseDate"]

    if "currentVersionDownloadLink" in code_data:
        if code_data["currentVersionDownloadLink"] != "":
            metadata["downloadUrl"] = code_data["currentVersionDownloadLink"]

    if "issueTracker" in code_data:
        if code_data["issueTracker"] != "":
            metadata["issueTracker"] = code_data["issueTracker"]

    if "name" in general_data:
        if general_data["name"] != "":
            metadata["name"] = general_data["name"]

    if "currentVersion" in code_data:
        if code_data["currentVersion"] != "":
            metadata["version"] = code_data["currentVersion"]

    if "uniqueIdentifier" in code_data:
        if code_data["uniqueIdentifier"] != "":
            metadata["identifier"] = code_data["uniqueIdentifier"]

    if "description" in general_data:
        if general_data["description"] != "":
            metadata["description"] = general_data["description"]

    if "applicationCategory" in code_data:
        if code_data["applicationCategory"] != "":
            metadata["applicationCategory"] = code_data["applicationCategory"]

    if "currentVersionReleaseNotes" in code_data:
        if code_data["currentVersionReleaseNotes"] != "":
            metadata["releaseNotes"] = code_data["currentVersionReleaseNotes"]

    if "funding" in general_data:
        if "code" in general_data["funding"]:
            if general_data["funding"]["code"] != "":
                metadata["funding"] = general_data["funding"]["code"]

    if "developmentStatus" in code_data:
        if code_data["developmentStatus"] != "":
            metadata["developmentStatus"] = code_data["developmentStatus"]

    if "isPartOf" in code_data:
        if code_data["isPartOf"] != "":
            if code_data["isPartOf"] != "":
                metadata["isPartOf"] = code_data["isPartOf"]

    if "referencePublication" in general_data:
        if general_data["referencePublication"] != "":
            metadata["referencePublication"] = general_data["referencePublication"]

    if "funding" in general_data:
        if "organization" in general_data["funding"]:
            if general_data["funding"]["organization"] != "":
                metadata["funding"] = {}

                metadata["funding"]["@type"] = "Organization"
                metadata["funding"]["@name"] = general_data["funding"]["organization"]

    if "keywords" in general_data:
        if len(general_data["keywords"]) > 0:
            metadata["keywords"] = []

            for item in general_data["keywords"]:
                metadata["keywords"].append(item["keyword"])

    if "programmingLanguage" in code_data:
        if code_data["programmingLanguage"] != "":
            metadata["programmingLanguage"] = code_data["programmingLanguage"]

    if "runtimePlatform" in code_data:
        if code_data["runtimePlatform"] != "":
            metadata["runtimePlatform"] = code_data["runtimePlatform"]

    if "operatingSystem" in code_data:
        if code_data["operatingSystem"] != "":
            metadata["operatingSystem"] = code_data["operatingSystem"]

    if "otherSoftwareRequirements" in code_data:
        if len(code_data["otherSoftwareRequirements"]) > 0:
            metadata["softwareRequirements"] = []

            for item in code_data["otherSoftwareRequirements"]:
                metadata["softwareRequirements"].append(item["link"])

    if "relatedLinks" in code_data:
        if len(code_data["relatedLinks"]) > 0:
            metadata["relatedLink"] = []

            for item in code_data["relatedLinks"]:
                metadata["relatedLink"].append(item["link"])

    if "authors" in general_data:
        if len(general_data["authors"]) > 0:
            metadata["author"] = []

            for item in general_data["authors"]:
                new_author = {}

                new_author["@type"] = "Person"

                if "orcid" in item:
                    new_author["@id"] = "https://orcid.org/" + item["orcid"]

                if "givenName" in item:
                    new_author["givenName"] = item["givenName"]

                if "familyName" in item:
                    new_author["familyName"] = item["familyName"]

                if "email" in item:
                    new_author["email"] = item["email"]

                if "affiliation" in item:
                    new_author["affiliation"] = {}
                    new_author["affiliation"]["@type"] = "Organization"
                    new_author["affiliation"]["name"] = item["affiliation"]

                metadata["author"].append(new_author)

    if "contributors" in general_data:
        if len(general_data["contributors"]) > 0:
            metadata["contributor"] = []

            for item in general_data["contributors"]:
                new_contributor = {}

                new_contributor["@type"] = "Person"

                if "orcid" in item:
                    new_contributor["@id"] = "https://orcid.org/" + item["orcid"]

                if "givenName" in item:
                    new_contributor["givenName"] = item["givenName"]

                if "familyName" in item:
                    new_contributor["familyName"] = item["familyName"]

                if "email" in item:
                    new_contributor["email"] = item["email"]

                if "affiliation" in item:
                    new_contributor["affiliation"] = {}
                    new_contributor["affiliation"]["@type"] = "Organization"
                    new_contributor["affiliation"]["name"] = item["affiliation"]

                metadata["contributor"].append(new_contributor)

    # Create the metadata file
    with open(os.path.join(folder_path, "codemeta.json"), "w") as f:
        f.write(json.dumps(metadata))
    return True


def createMetadata(data_types, data):
    try:
        if "Code" in data_types:
            code_data = data["Code"]["questions"]
            general_data = data["general"]["questions"]
            folder_path = data["Code"]["folderPath"]
            createCodeMetadata(code_data, general_data, folder_path)

        return "SUCCESS"
    except Exception as e:
        raise e
