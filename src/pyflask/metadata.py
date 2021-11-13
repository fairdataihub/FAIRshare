from __future__ import print_function


def createCodeMetadata(code_data, general_data, folder_path):
    metadata = {
        "@context": "https://doi.org/10.5063/schema/codemeta-2.0",
        "@type": "SoftwareSourceCode",
    }

    if "license" in code_data:
        metadata["license"] = "https://spdx.org/licenses/" + code_data["license"]

    if "codeRepository" in code_data:
        metadata["codeRepository"] = code_data["codeRepository"]

    if "continuousIntegration" in code_data:
        metadata["contIntegration"] = code_data["continuousIntegration"]

    if "creationDate" in code_data:
        metadata["dateCreated"] = code_data["creationDate"]

    if "firstReleaseDate" in code_data:
        metadata["dateCreated"] = code_data["firstReleaseDate"]

    if "currentVersionReleaseDate" in code_data:
        metadata["dateModified"] = code_data["currentVersionReleaseDate"]

    if "currentVersionDownloadLink" in code_data:
        metadata["downloadUrl"] = code_data["currentVersionDownloadLink"]

    if "issueTracker" in code_data:
        metadata["issueTracker"] = code_data["issueTracker"]

    if "name" in general_data:
        metadata["name"] = general_data["name"]

    if "currentVersion" in code_data:
        metadata["version"] = code_data["currentVersion"]

    if "uniqueIdentifier" in code_data:
        metadata["identifier"] = code_data["uniqueIdentifier"]

    if "description" in general_data:
        metadata["description"] = general_data["description"]

    if "applicationCategory" in code_data:
        metadata["applicationCategory"] = code_data["applicationCategory"]

    if "currentVersionReleaseNotes" in code_data:
        metadata["releaseNotes"] = code_data["currentVersionReleaseNotes"]

    if "funding" in general_data:
        if "code" in general_data["funding"]:
            metadata["funding"] = general_data["funding"]["code"]

    if "developmentStatus" in code_data:
        metadata["developmentStatus"] = code_data["developmentStatus"]

    if "isPartOf" in code_data:
        metadata["isPartOf"] = code_data["isPartOf"]

    if "referencePublication" in general_data:
        metadata["referencePublication"] = general_data["referencePublication"]

    if "funding" in general_data:
        if "organization" in general_data["funding"]:
            metadata["funding"] = {}

            metadata["funding"]["@type"] = "Organization"
            metadata["funding"]["@name"] = general_data["funding"]["organization"]

    if "keywords" in general_data:
        metadata["keywords"] = []

        for item in general_data["keywords"]:
            metadata["keywords"].append(item["keyword"])

    if "programmingLanguage" in code_data:
        metadata["programmingLanguage"] = code_data["programmingLanguage"]

    if "runtimePlatform" in code_data:
        metadata["runtimePlatform"] = code_data["runtimePlatform"]

    if "operatingSystem" in code_data:
        metadata["operatingSystem"] = code_data["operatingSystem"]

    if "otherSoftwareRequirements" in code_data:
        metadata["softwareRequirements"] = []

        for item in code_data["otherSoftwareRequirements"]:
            metadata["softwareRequirements"].append(item["link"])

    if "relatedLinks" in code_data:
        metadata["relatedLink"] = []

        for item in code_data["relatedLinks"]:
            metadata["relatedLink"].append(item["link"])

    if "authors" in general_data:
        metadata["author"] = []

        for item in general_data["authors"]:
            new_author = {}

            new_author["@type"] = "Person"
            new_author["givenName"] = item["givenName"]
            new_author["familyName"] = item["familyName"]
            new_author["email"] = item["email"]

            new_author["affiliation"] = {}
            new_author["affiliation"]["@type"] = "Organization"
            new_author["affiliation"]["name"] = item["affiliation"]

            metadata["author"].append(new_author)

    if "contributors" in general_data:
        metadata["contributor"] = []

        for item in general_data["contributors"]:
            new_contributor = {}

            new_contributor["@type"] = "Person"
            new_contributor["givenName"] = item["givenName"]
            new_contributor["familyName"] = item["familyName"]
            new_contributor["email"] = item["email"]

            new_contributor["affiliation"] = {}
            new_contributor["affiliation"]["@type"] = "Organization"
            new_contributor["affiliation"]["name"] = item["affiliation"]

            metadata["contributor"].append(new_contributor)

    # Create the metadata file
    with open(folder_path + "\\codemetadata.json", "w") as f:
        f.write(metadata)
    return True


def createMetadata(data_types, data, folder_path):
    try:
        if "Code" in data_types:
            createCodeMetadata(data["Code"], data["general"], folder_path)

        return "SUCCESS"
    except Exception as e:
        raise e
