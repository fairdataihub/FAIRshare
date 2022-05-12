import json
import os

import yaml


def createCodeMetadata(code_data, general_data, folder_path, virtual_file):
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

    if "identifier" in code_data:
        if code_data["identifier"] != "":
            metadata["identifier"] = code_data["identifier"]

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
            metadata["isPartOf"] = code_data["isPartOf"]

    if "referencePublication" in general_data:
        if general_data["referencePublication"] != "":
            metadata["referencePublication"] = general_data["referencePublication"]

    if "funding" in general_data:
        if "organization" in general_data["funding"]:
            if general_data["funding"]["organization"] != "":
                metadata["funder"] = {}

                metadata["funder"]["@type"] = "Organization"
                metadata["funder"]["@name"] = general_data["funding"]["organization"]

    if "keywords" in general_data:
        if len(general_data["keywords"]) > 0:
            metadata["keywords"] = []

            for item in general_data["keywords"]:
                metadata["keywords"].append(item["keyword"])

    if "programmingLanguage" in code_data:
        if len(code_data["programmingLanguage"]) > 0:
            metadata["programmingLanguage"] = code_data["programmingLanguage"]

    if "runtimePlatform" in code_data:
        if len(code_data["runtimePlatform"]) > 0:
            metadata["runtimePlatform"] = code_data["runtimePlatform"]

    if "operatingSystem" in code_data:
        if len(code_data["operatingSystem"]) > 0:
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
                    if item["orcid"] != "":
                        new_author["@id"] = "https://orcid.org/" + item["orcid"]

                if "givenName" in item:
                    new_author["givenName"] = item["givenName"]

                if "familyName" in item:
                    if item["familyName"] != "":
                        new_author["familyName"] = item["familyName"]

                if "email" in item:
                    if item["email"] != "":
                        new_author["email"] = item["email"]

                if "affiliation" in item:
                    if item["affiliation"] != "":
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
                    if item["orcid"] != "":
                        new_contributor["@id"] = "https://orcid.org/" + item["orcid"]

                if "givenName" in item:
                    new_contributor["givenName"] = item["givenName"]

                if "familyName" in item:
                    if item["familyName"] != "":
                        new_contributor["familyName"] = item["familyName"]

                if "email" in item:
                    if item["email"] != "":
                        new_contributor["email"] = item["email"]

                if "affiliation" in item:
                    if item["affiliation"] != "":
                        new_contributor["affiliation"] = {}
                        new_contributor["affiliation"]["@type"] = "Organization"
                        new_contributor["affiliation"]["name"] = item["affiliation"]

                metadata["contributor"].append(new_contributor)

    # return the code metadata object if virtual is set to true
    if virtual_file:
        return json.dumps(metadata)

    # If the folder doesn't exist (for some weird reason), create it
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Create the metadata file
    with open(os.path.join(folder_path, "codemeta.json"), "w") as f:
        f.write(json.dumps(metadata))

    return True


def createOtherMetadata(other_data, general_data, folder_path, virtual_file):
    metadata = {}

    if "license" in other_data:
        metadata["license"] = other_data["license"]

    if "creationDate" in other_data:
        if other_data["creationDate"] != "":
            metadata["dateCreated"] = other_data["creationDate"]

    if "firstReleaseDate" in other_data:
        if other_data["firstReleaseDate"] != "":
            metadata["dateCreated"] = other_data["firstReleaseDate"]

    if "name" in other_data:
        if other_data["name"] != "":
            metadata["name"] = other_data["name"]

    if "identifier" in other_data:
        if other_data["identifier"] != "":
            metadata["identifier"] = other_data["identifier"]

    if "description" in other_data:
        if other_data["description"] != "":
            metadata["description"] = other_data["description"]

    if "fundingCode" in other_data:
        if other_data["fundingCode"] != "":
            metadata["fundingCode"] = other_data["fundingCode"]

    if "fundingOrganization" in other_data:
        if other_data["fundingOrganization"] != "":
            metadata["fundingOrganization"] = other_data["fundingOrganization"]

    if "developmentStatus" in other_data:
        if other_data["developmentStatus"] != "":
            metadata["developmentStatus"] = other_data["developmentStatus"]

    if "isPartOf" in other_data:
        if other_data["isPartOf"] != "":
            metadata["isPartOf"] = other_data["isPartOf"]

    if "referencePublication" in other_data:
        if other_data["referencePublication"] != "":
            metadata["referencePublication"] = other_data["referencePublication"]

    if "keywords" in other_data:
        if len(other_data["keywords"]) > 0:
            metadata["keywords"] = []

            for item in other_data["keywords"]:
                metadata["keywords"].append(item["keyword"])

    if "relatedLinks" in other_data:
        if len(other_data["relatedLinks"]) > 0:
            metadata["relatedLink"] = []

            for item in other_data["relatedLinks"]:
                metadata["relatedLink"].append(item["link"])

    if "authors" in other_data:
        if len(other_data["authors"]) > 0:
            metadata["author"] = []

            for item in other_data["authors"]:
                new_author = {}

                new_author["@type"] = "Person"

                if "orcid" in item:
                    if item["orcid"] != "":
                        new_author["@id"] = "https://orcid.org/" + item["orcid"]

                if "givenName" in item:
                    new_author["givenName"] = item["givenName"]

                if "familyName" in item:
                    if item["familyName"] != "":
                        new_author["familyName"] = item["familyName"]

                if "email" in item:
                    if item["email"] != "":
                        new_author["email"] = item["email"]

                if "affiliation" in item:
                    if item["affiliation"] != "":
                        new_author["affiliation"] = {}
                        new_author["affiliation"]["@type"] = "Organization"
                        new_author["affiliation"]["name"] = item["affiliation"]

                metadata["author"].append(new_author)

    if "contributors" in other_data:
        if len(other_data["contributors"]) > 0:
            metadata["contributor"] = []

            for item in other_data["contributors"]:
                new_contributor = {}

                new_contributor["@type"] = "Person"

                if "orcid" in item:
                    if item["orcid"] != "":
                        new_contributor["@id"] = "https://orcid.org/" + item["orcid"]

                if "givenName" in item:
                    new_contributor["givenName"] = item["givenName"]

                if "familyName" in item:
                    if item["familyName"] != "":
                        new_contributor["familyName"] = item["familyName"]

                if "email" in item:
                    if item["email"] != "":
                        new_contributor["email"] = item["email"]

                if "affiliation" in item:
                    if item["affiliation"] != "":
                        new_contributor["affiliation"] = {}
                        new_contributor["affiliation"]["@type"] = "Organization"
                        new_contributor["affiliation"]["name"] = item["affiliation"]

                metadata["contributor"].append(new_contributor)

    # return the code metadata object if virtual is set to true
    if virtual_file:
        return json.dumps(metadata)

    # If the folder doesn't exist (for some weird reason), create it
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Create the metadata file
    with open(os.path.join(folder_path, "metadata.json"), "w") as f:
        f.write(json.dumps(metadata))
    return True


def createMetadata(data_types, data, virtual_file):
    try:
        if "Code" in data_types:
            code_data = data["Code"]["questions"]
            general_data = data["general"]["questions"]
            folder_path = ""
            if "folderPath" in data["Code"]:
                folder_path = data["Code"]["folderPath"]
            result = createCodeMetadata(
                code_data, general_data, folder_path, virtual_file
            )
            if virtual_file:
                return result

        if "Other" in data_types:
            other_data = data["Other"]["questions"]
            general_data = data["general"]["questions"]
            folder_path = ""
            if "folderPath" in data["Other"]:
                folder_path = data["Other"]["folderPath"]
            result = createOtherMetadata(
                other_data, general_data, folder_path, virtual_file
            )
            if virtual_file:
                return result

        return "SUCCESS"
    except Exception as e:
        raise e


def createCitationFromCode(code_data, general_data, folder_path, virtual_file):
    # Create the citation file
    citationObject = {
        "cff-version": "1.2.0",
    }

    if "name" in general_data:
        if general_data["name"] != "":
            citationObject["title"] = general_data["name"]

    citationObject["message"] = "If you use this software, please cite it as below."
    citationObject["type"] = "software"

    if "authors" in general_data:
        if len(general_data["authors"]) > 0:
            citationObject["authors"] = []

            for item in general_data["authors"]:
                new_author = {}

                if "orcid" in item:
                    if item["orcid"] != "":
                        new_author["orcid"] = item["orcid"]

                if "givenName" in item:
                    new_author["given-names"] = item["givenName"]

                if "familyName" in item:
                    new_author["family-names"] = item["familyName"]

                if "email" in item:
                    if item["email"] != "":
                        new_author["email"] = item["email"]

                if "affiliation" in item:
                    if item["affiliation"] != "":
                        new_author["affiliation"] = item["affiliation"]

                citationObject["authors"].append(new_author)

    if "identifier" in code_data:
        if code_data["identifier"] != "":
            citationObject["identifiers"] = []

            identifier = {}
            identifier["type"] = "doi"
            identifier["value"] = code_data["identifier"]
            identifier["description"] = "DOI for this software's record on Zenodo"

            citationObject["identifiers"].append(identifier)

    if "codeRepository" in code_data:
        if code_data["codeRepository"] != "":
            citationObject["repository-code"] = code_data["codeRepository"]

    if "isPartOf" in code_data:
        if code_data["isPartOf"] != "":
            citationObject["url"] = code_data["isPartOf"]

    if "currentVersionDownloadLink" in code_data:
        if code_data["currentVersionDownloadLink"] != "":
            citationObject["repository-artifact"] = code_data[
                "currentVersionDownloadLink"
            ]

    if "description" in general_data:
        if general_data["description"] != "":
            citationObject["abstract"] = general_data["description"]

    if "keywords" in general_data:
        if len(general_data["keywords"]) > 0:
            citationObject["keywords"] = []

            for item in general_data["keywords"]:
                citationObject["keywords"].append(item["keyword"])

    if "license" in code_data:
        citationObject["license"] = code_data["license"]

    if "currentVersion" in code_data:
        if code_data["currentVersion"] != "":
            citationObject["version"] = code_data["currentVersion"]

    if "currentVersionReleaseDate" in code_data:
        if code_data["currentVersionReleaseDate"] != "":
            citationObject["date-released"] = code_data["currentVersionReleaseDate"]

    # return the CITATION.cff object if virtual is set to true
    if virtual_file:
        return json.dumps(citationObject)

    # If the folder doesn't exist (for some weird reason), create it
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Create the CITATION.cff file
    with open(os.path.join(folder_path, "CITATION.cff"), "w") as file:
        yaml.dump(citationObject, file)

    def line_prepender(filename, line):
        with open(filename, "r+") as f:
            content = f.read()
            f.seek(0, 0)
            f.write(line.rstrip("\r\n") + "\n" + content)

    line_prepender(os.path.join(folder_path, "CITATION.cff"), "\n")
    line_prepender(
        os.path.join(folder_path, "CITATION.cff"),
        "# Visit https://fairdataihub.org/fairshare to learn more!",
    )
    line_prepender(
        os.path.join(folder_path, "CITATION.cff"),
        "# This CITATION.cff file was generated with FAIRshare.",
    )

    return True


def createCitationCFF(data_types, data, virtual_file):
    try:
        if "Code" in data_types:
            code_data = data["Code"]["questions"]
            general_data = data["general"]["questions"]
            folder_path = ""
            if "folderPath" in data["Code"]:
                folder_path = data["Code"]["folderPath"]
            result = createCitationFromCode(
                code_data, general_data, folder_path, virtual_file
            )
            if virtual_file:
                return result

        return "SUCCESS"
    except Exception as e:
        raise e
