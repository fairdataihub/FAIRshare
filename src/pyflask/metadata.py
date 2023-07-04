import hashlib
import json
import os
import csv
import shutil
import datetime

import xlsxwriter
import yaml


def createCodeMetadata(code_data, general_data, folder_path, virtual_file):
    # sourcery skip: low-code-quality
    metadata = {
        "@context": "https://doi.org/10.5063/schema/codemeta-2.0",
        "@type": "SoftwareSourceCode",
    }

    if "license" in code_data:
        metadata["license"] = "https://spdx.org/licenses/" + code_data["license"]

    if "codeRepository" in code_data and code_data["codeRepository"] != "":
        metadata["codeRepository"] = code_data["codeRepository"]

    if (
        "continuousIntegration" in code_data
        and code_data["continuousIntegration"] != ""
    ):
        metadata["contIntegration"] = code_data["continuousIntegration"]

    if "creationDate" in code_data and code_data["creationDate"] != "":
        metadata["dateCreated"] = code_data["creationDate"]

    if "firstReleaseDate" in code_data and code_data["firstReleaseDate"] != "":
        metadata["datePublished"] = code_data["firstReleaseDate"]

    if (
        "currentVersionReleaseDate" in code_data
        and code_data["currentVersionReleaseDate"] != ""
    ):
        metadata["dateModified"] = code_data["currentVersionReleaseDate"]

    if (
        "currentVersionDownloadLink" in code_data
        and code_data["currentVersionDownloadLink"] != ""
    ):
        metadata["downloadUrl"] = code_data["currentVersionDownloadLink"]

    if "issueTracker" in code_data and code_data["issueTracker"] != "":
        metadata["issueTracker"] = code_data["issueTracker"]

    if "name" in general_data and general_data["name"] != "":
        metadata["name"] = general_data["name"]

    if "currentVersion" in code_data and code_data["currentVersion"] != "":
        metadata["version"] = code_data["currentVersion"]

    if "identifier" in code_data and code_data["identifier"] != "":
        metadata["identifier"] = code_data["identifier"]

    if "description" in general_data and general_data["description"] != "":
        metadata["description"] = general_data["description"]

    if "applicationCategory" in code_data and code_data["applicationCategory"] != "":
        metadata["applicationCategory"] = code_data["applicationCategory"]

    if (
        "currentVersionReleaseNotes" in code_data
        and code_data["currentVersionReleaseNotes"] != ""
    ):
        metadata["releaseNotes"] = code_data["currentVersionReleaseNotes"]

    if (
        "funding" in general_data
        and "code" in general_data["funding"]
        and general_data["funding"]["code"] != ""
    ):
        metadata["funding"] = general_data["funding"]["code"]

    if "developmentStatus" in code_data and code_data["developmentStatus"] != "":
        metadata["developmentStatus"] = code_data["developmentStatus"]

    if "isPartOf" in code_data and code_data["isPartOf"] != "":
        metadata["isPartOf"] = code_data["isPartOf"]

    if (
        "referencePublication" in general_data
        and general_data["referencePublication"] != ""
    ):
        metadata["referencePublication"] = general_data["referencePublication"]

    if (
        "funding" in general_data
        and "organization" in general_data["funding"]
        and general_data["funding"]["organization"] != ""
    ):
        metadata["funder"] = {
            "@type": "Organization",
            "@name": general_data["funding"]["organization"],
        }

    if "keywords" in general_data and len(general_data["keywords"]) > 0:
        metadata["keywords"] = [item["keyword"] for item in general_data["keywords"]]

    if "programmingLanguage" in code_data and len(code_data["programmingLanguage"]) > 0:
        metadata["programmingLanguage"] = code_data["programmingLanguage"]

    if "runtimePlatform" in code_data and len(code_data["runtimePlatform"]) > 0:
        metadata["runtimePlatform"] = code_data["runtimePlatform"]

    if "operatingSystem" in code_data and len(code_data["operatingSystem"]) > 0:
        metadata["operatingSystem"] = code_data["operatingSystem"]

    if (
        "otherSoftwareRequirements" in code_data
        and len(code_data["otherSoftwareRequirements"]) > 0
    ):
        metadata["softwareRequirements"] = [
            item["link"] for item in code_data["otherSoftwareRequirements"]
        ]
    if "relatedLinks" in code_data and len(code_data["relatedLinks"]) > 0:
        metadata["relatedLink"] = []

        for item in code_data["relatedLinks"]:
            metadata["relatedLink"].append(item["link"])

    if "authors" in general_data and len(general_data["authors"]) > 0:
        metadata["author"] = []

        for item in general_data["authors"]:
            new_author = {"@type": "Person"}

            if "orcid" in item and item["orcid"] != "":
                new_author["@id"] = "https://orcid.org/" + item["orcid"]

            if "givenName" in item:
                new_author["givenName"] = item["givenName"]

            if "familyName" in item and item["familyName"] != "":
                new_author["familyName"] = item["familyName"]

            if "email" in item and item["email"] != "":
                new_author["email"] = item["email"]

            if "affiliation" in item and item["affiliation"] != "":
                new_author["affiliation"] = {
                    "@type": "Organization",
                    "name": item["affiliation"],
                }
            metadata["author"].append(new_author)

    if "contributors" in general_data and len(general_data["contributors"]) > 0:
        metadata["contributor"] = []

        for item in general_data["contributors"]:
            new_contributor = {"@type": "Person"}

            if "orcid" in item and item["orcid"] != "":
                new_contributor["@id"] = "https://orcid.org/" + item["orcid"]

            if "givenName" in item:
                new_contributor["givenName"] = item["givenName"]

            if "familyName" in item and item["familyName"] != "":
                new_contributor["familyName"] = item["familyName"]

            if "email" in item and item["email"] != "":
                new_contributor["email"] = item["email"]

            if "affiliation" in item and item["affiliation"] != "":
                new_contributor["affiliation"] = {"@type": "Organization"}
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
        f.write(json.dumps(metadata, indent=4))

    return True


def createImmunologyMetadata(immunology_data, folder_path, virtual_file):
    def createBasicStudyDesign(immunology_data, folder_path, virtual_file):
        row_content = []
        virtual_metadata = {}

        homeFolderPath = os.path.expanduser("~")
        tempFolderPath = os.path.join(
            homeFolderPath, ".fairshare", "temp", "basic_study_design"
        )
        metadataFilePath = os.path.join(tempFolderPath, "basic_study_design.txt")

        os.makedirs(tempFolderPath, exist_ok=True)

        if os.path.exists(metadataFilePath):
            os.remove(metadataFilePath)

        # write as a tsv file
        with open(metadataFilePath, "w", newline="") as tsvfile:
            basic_study_design = csv.writer(
                tsvfile, delimiter="\t", lineterminator="\n"
            )

            row_content = ["basic_study_design", "Schema Version 3.36"]
            basic_study_design.writerow(row_content)

            row_content = [
                "Please do not delete or edit this column",
                "The basic study design template defines and annotates key elements of a study including the purpose, subject grouping, schedule of events, personnel, and references (weblinks, publications). Use the study_design_edit template to add additional information for a study after a study is defined in ImmPort. The basic study design template consists of several sections or compound templates. Some compound templates are required: study, arm_or_cohort, inclusion_exclusion, planned_visit, study_2_condition_or_disease, study_2_protocol, study_categorization, study_personnel.  Other compound templates are optional: study_file, study_link, and study_pubmed.",  # noqa: E501
            ]
            basic_study_design.writerow(row_content)

            row_content = ["Column Name"]
            basic_study_design.writerow(row_content)

            row_content = []
            basic_study_design.writerow(row_content)

            row_content = []
            basic_study_design.writerow(row_content)

            row_content = ["study"]
            basic_study_design.writerow(row_content)
            virtual_metadata["study"] = {}

            row_content = ["User Defined ID", immunology_data["studyID"]]
            virtual_metadata["study"]["User Defined ID"] = immunology_data["briefTitle"]
            basic_study_design.writerow(row_content)

            row_content = ["Brief Title", immunology_data["briefTitle"]]
            virtual_metadata["study"]["Brief Title"] = immunology_data["briefTitle"]
            basic_study_design.writerow(row_content)

            row_content = ["Official Title", immunology_data["officialTitle"]]
            virtual_metadata["study"]["Official Title"] = immunology_data[
                "officialTitle"
            ]
            basic_study_design.writerow(row_content)

            row_content = ["Brief Description", immunology_data["briefDescription"]]
            virtual_metadata["study"]["Brief Description"] = immunology_data[
                "briefDescription"
            ]
            basic_study_design.writerow(row_content)

            row_content = ["Description", immunology_data["description"]]
            virtual_metadata["study"]["Description"] = immunology_data["description"]
            basic_study_design.writerow(row_content)

            row_content = ["Intervention Agent", immunology_data["interventionAgent"]]
            virtual_metadata["study"]["Intervention Agent"] = immunology_data[
                "interventionAgent"
            ]
            basic_study_design.writerow(row_content)

            row_content = ["Endpoints", immunology_data["endpoints"]]
            virtual_metadata["study"]["Endpoints"] = immunology_data["endpoints"]
            basic_study_design.writerow(row_content)

            row_content = [
                "Sponsoring Organization",
                immunology_data["sponsoringOrganization"],
            ]
            virtual_metadata["study"]["Sponsoring Organization"] = immunology_data[
                "sponsoringOrganization"
            ]
            basic_study_design.writerow(row_content)

            row_content = ["Age Unit", immunology_data["ageUnit"]]
            virtual_metadata["study"]["Age Unit"] = immunology_data["ageUnit"]
            basic_study_design.writerow(row_content)

            row_content = [
                "Actual Start Date",
                immunology_data.get("actualStartDate", None),
            ]
            virtual_metadata["study"]["Actual Start Date"] = immunology_data.get(
                "actualStartDate", None
            )
            basic_study_design.writerow(row_content)

            row_content = [
                "Hypothesis",
                immunology_data.get("hypothesis", None),
            ]
            virtual_metadata["study"]["Hypothesis"] = immunology_data.get(
                "hypothesis", None
            )
            basic_study_design.writerow(row_content)

            row_content = [
                "Objectives",
                immunology_data.get("objectives", None),
            ]
            virtual_metadata["study"]["Objectives"] = immunology_data.get(
                "objectives", None
            )
            basic_study_design.writerow(row_content)

            row_content = [
                "Target Enrollment",
                immunology_data.get("targetEnrollment", None),
            ]
            virtual_metadata["study"]["Target Enrollment"] = immunology_data.get(
                "targetEnrollment", None
            )
            basic_study_design.writerow(row_content)

            row_content = [
                "Minimum Age",
                immunology_data.get("minimumAge", None),
            ]
            virtual_metadata["study"]["Minimum Age"] = immunology_data.get(
                "minimumAge", None
            )
            basic_study_design.writerow(row_content)

            row_content = [
                "Maximum Age",
                immunology_data.get("maximumAge", None),
            ]
            virtual_metadata["study"]["Maximum Age"] = immunology_data.get(
                "maximumAge", None
            )
            basic_study_design.writerow(row_content)

            row_content = []
            basic_study_design.writerow(row_content)

            row_content = ["study_categorization"]
            basic_study_design.writerow(row_content)
            virtual_metadata["study_categorization"] = {}

            row_content = [
                "Research Focus",
                immunology_data["researchFocus"],
            ]
            virtual_metadata["study_categorization"][
                "Research Focus"
            ] = immunology_data["researchFocus"]
            basic_study_design.writerow(row_content)

            row_content = []
            basic_study_design.writerow(row_content)

            row_content = ["study_2_condition_or_disease"]
            virtual_metadata["study_2_condition_or_disease"] = {}
            basic_study_design.writerow(row_content)

            row_content = ["Condition Reported"]
            virtual_metadata["study_2_condition_or_disease"]["Condition Reported"] = []
            for condition in immunology_data["condition"]:
                row_content.append(condition)
                virtual_metadata["study_2_condition_or_disease"][
                    "Condition Reported"
                ].append(condition)

            basic_study_design.writerow(row_content)

            row_content = []
            basic_study_design.writerow(row_content)

            row_content = ["arm_or_cohort"]
            virtual_metadata["arm_or_cohort"] = []
            basic_study_design.writerow(row_content)

            row_content = ["User Defined ID", "Name", "Description", "Type Reported"]
            basic_study_design.writerow(row_content)

            for arm in immunology_data["arms"]:
                row_content = [
                    arm["armID"],
                    arm["name"],
                    arm["description"],
                    arm["type"],
                ]
                virtual_metadata["arm_or_cohort"].append(
                    {
                        "User Defined ID": arm["armID"],
                        "Name": arm["name"],
                        "Description": arm["description"],
                        "Type Reported": arm["type"],
                    }
                )
                basic_study_design.writerow(row_content)

            row_content = []
            basic_study_design.writerow(row_content)

            row_content = ["study_personnel"]
            virtual_metadata["study_personnel"] = []
            basic_study_design.writerow(row_content)

            row_content = [
                "User Defined ID",
                "Honorific",
                "Last Name",
                "First Name",
                "Suffixes",
                "Organization",
                "ORCID ID",
                "Email",
                " Title In Study",
                "Role in Study",
                "Site Name",
            ]
            basic_study_design.writerow(row_content)

            for person in immunology_data["studyPersonnel"]:
                row_content = [
                    person["personnelID"],
                    person.get("honorific", None),
                    person["lastName"],
                    person["firstName"],
                    person.get("suffix", None),
                    person["organization"],
                    person.get("orcid", None),
                    person["email"],
                    person["titleInStudy"],
                    person["roleInStudy"],
                    person["siteName"],
                ]
                virtual_metadata["study_personnel"].append(
                    {
                        "User Defined ID": person["personnelID"],
                        "Honorific": person.get("honorific", None),
                        "Last Name": person["lastName"],
                        "First Name": person["firstName"],
                        "Suffixes": person.get("suffix", None),
                        "Organization": person["organization"],
                        "ORCID ID": person.get("orcid", None),
                        "Email": person["email"],
                        "Title In Study": person["titleInStudy"],
                        "Role in Study": person["roleInStudy"],
                        "Site Name": person["siteName"],
                    }
                )
                basic_study_design.writerow(row_content)

            row_content = []
            basic_study_design.writerow(row_content)

            row_content = ["planned_visit"]
            virtual_metadata["planned_visit"] = []
            basic_study_design.writerow(row_content)

            row_content = [
                "User Defined ID",
                "Name",
                "Order Number",
                "Min Start Day",
                "Max Start Day",
                "Start Rule",
                "End Rule",
            ]
            basic_study_design.writerow(row_content)

            for visit in immunology_data["plannedVisits"]:
                row_content = [
                    visit["visitID"],
                    visit["name"],
                    visit["orderNumber"],
                    visit["minStartDay"],
                    visit.get("maxStartDay", visit["minStartDay"]),
                    visit.get("startRule", None),
                    visit.get("endRule", None),
                ]
                virtual_metadata["planned_visit"].append(
                    {
                        "User Defined ID": visit["visitID"],
                        "Name": visit["name"],
                        "Order Number": visit["orderNumber"],
                        "Min Start Day": visit["minStartDay"],
                        "Max Start Day": visit.get("maxStartDay", visit["minStartDay"]),
                        "Start Rule": visit.get("startRule", None),
                        "End Rule": visit.get("endRule", None),
                    }
                )
                basic_study_design.writerow(row_content)

            row_content = []
            basic_study_design.writerow(row_content)

            row_content = ["inclusion_exclusion"]
            virtual_metadata["inclusion_exclusion"] = []
            basic_study_design.writerow(row_content)

            row_content = [
                "User Defined ID",
                "Criterion",
                "Criterion Category",
            ]
            basic_study_design.writerow(row_content)

            for inexclusion in immunology_data["inexclusions"]:
                row_content = [
                    inexclusion["userDefinedID"],
                    inexclusion["criterion"],
                    inexclusion["criterionCategory"],
                ]
                virtual_metadata["inclusion_exclusion"].append(
                    {
                        "User Defined ID": inexclusion["userDefinedID"],
                        "Criterion": inexclusion["criterion"],
                        "Criterion Category": inexclusion["criterionCategory"],
                    }
                )
                basic_study_design.writerow(row_content)

            row_content = []
            basic_study_design.writerow(row_content)

            row_content = ["study_2_protocol"]
            virtual_metadata["study_2_protocol"] = {}
            basic_study_design.writerow(row_content)

            row_content = ["Condition Reported"]
            virtual_metadata["study_2_protocol"]["Protocol ID"] = []
            for protocol in immunology_data["protocols"]:
                row_content.append(protocol["userDefinedID"])
                virtual_metadata["study_2_protocol"]["Protocol ID"].append(
                    protocol["userDefinedID"]
                )
            basic_study_design.writerow(row_content)

            row_content = []
            basic_study_design.writerow(row_content)

            row_content = ["study_file"]
            virtual_metadata["study_file"] = []
            basic_study_design.writerow(row_content)

            row_content = [
                "File Name",
                "Description",
                "Study File Type",
            ]
            basic_study_design.writerow(row_content)

            for study_file in immunology_data["studyFiles"]:
                for file in study_file["filePaths"]:
                    file_name = os.path.basename(file)

                    row_content = [
                        file_name,
                        study_file["description"],
                        study_file["type"],
                    ]
                    virtual_metadata["study_file"].append(
                        {
                            "File Name": file_name,
                            "Description": study_file["description"],
                            "Study File Type": study_file["type"],
                        }
                    )
                    basic_study_design.writerow(row_content)

            row_content = []
            basic_study_design.writerow(row_content)

            row_content = ["study_link"]
            virtual_metadata["study_link"] = []
            basic_study_design.writerow(row_content)

            row_content = ["Name", "Value"]
            basic_study_design.writerow(row_content)

            for link in immunology_data["studyLinks"]:
                row_content = [
                    link["name"],
                    link["url"],
                ]
                virtual_metadata["study_link"].append(
                    {
                        "Name": link["name"],
                        "Value": link["url"],
                    }
                )
                basic_study_design.writerow(row_content)

            row_content = []
            basic_study_design.writerow(row_content)

            row_content = ["study_pubmed"]
            virtual_metadata["study_pubmed"] = []
            basic_study_design.writerow(row_content)

            row_content = [
                "PubMed ID",
                "DOI",
                "Title",
                "Journal",
                "Year",
                "Month",
                "Issue",
                "Pages",
                "Authors",
            ]
            basic_study_design.writerow(row_content)

            for publication in immunology_data["studyPublications"]:
                year = None
                month = None

                if "date" in publication:
                    # date is in format YYYY-MM-DDTHH:MM:SS.000Z
                    date = publication["date"]

                    year = date[:4]
                    month = date[5:7]

                    # convert month to month name
                    month = datetime.datetime.strptime(month, "%m").strftime("%B")

                row_content = [
                    publication["publicationID"],
                    publication.get("doi", None),
                    publication.get("title", None),
                    publication.get("journal", None),
                    year,
                    month,
                    publication.get("issue", None),
                    publication.get("pages", None),
                    publication.get("authors", None),
                ]
                virtual_metadata["study_pubmed"].append(
                    {
                        "PubMed ID": publication["publicationID"],
                        "DOI": publication.get("doi", None),
                        "Title": publication.get("title", None),
                        "Journal": publication.get("journal", None),
                        "Year": year,
                        "Month": month,
                        "Issue": publication.get("issue", None),
                        "Pages": publication.get("pages", None),
                        "Authors": publication.get("authors", None),
                    }
                )
                basic_study_design.writerow(row_content)

        tsvfile.close()

        if virtual_file:
            return virtual_metadata

        # check if the file exists and remove before moving
        destination = os.path.join(folder_path, "basic_study_design.txt")

        if os.path.exists(destination):
            os.remove(destination)

        # move the file from temp to the folder path
        shutil.move(metadataFilePath, folder_path)

        return

    def createBasicStudyProtocols(immunology_data, folder_path, virtual_file):
        row_content = []
        virtual_metadata = {}

        homeFolderPath = os.path.expanduser("~")
        tempFolderPath = os.path.join(
            homeFolderPath, ".fairshare", "temp", "basic_study_design"
        )
        metadataFilePath = os.path.join(tempFolderPath, "protocols.txt")

        os.makedirs(tempFolderPath, exist_ok=True)

        if os.path.exists(metadataFilePath):
            os.remove(metadataFilePath)

        # write as a tsv file
        with open(metadataFilePath, "w", newline="") as tsvfile:
            basic_study_protocols = csv.writer(
                tsvfile, delimiter="\t", lineterminator="\n"
            )

            row_content = ["protocols	", "Schema Version 3.36"]
            basic_study_protocols.writerow(row_content)

            row_content = [
                "Please do not delete or edit this column",
            ]
            basic_study_protocols.writerow(row_content)

            virtual_metadata["protocols"] = []

            row_content = [
                "Column Name",
                "User Defined ID",
                "File Name",
                "Name",
                "Description",
                "Type",
            ]
            basic_study_protocols.writerow(row_content)

            for protocol in immunology_data["protocols"]:
                file_path = protocol["filePath"]
                file_name = os.path.basename(file_path)
                row_content = [
                    "",
                    protocol["userDefinedID"],
                    file_name,
                    protocol["name"],
                    protocol.get("description", None),
                    protocol.get("type", None),
                ]
                virtual_metadata["protocols"].append(
                    {
                        "Column Name": "",
                        "User Defined ID": protocol["userDefinedID"],
                        "File Name": file_name,
                        "Name": protocol["name"],
                        "Description": protocol.get("description", None),
                        "Type": protocol.get("type", None),
                    }
                )
                basic_study_protocols.writerow(row_content)

        tsvfile.close()

        if virtual_file:
            return virtual_metadata

        # check if the file exists and remove before moving
        destination = os.path.join(folder_path, "protocols.txt")

        if os.path.exists(destination):
            os.remove(destination)

        # move the file from temp to the folder path and replace if it exists
        shutil.move(metadataFilePath, folder_path)

    basic_study_design_file = createBasicStudyDesign(
        immunology_data, folder_path, virtual_file
    )
    basic_study_protocols_file = createBasicStudyProtocols(
        immunology_data, folder_path, virtual_file
    )

    if virtual_file:
        metadata = {
            "basic_study_design": basic_study_design_file,
            "basic_study_protocols": basic_study_protocols_file,
        }
        return json.dumps(metadata)

    return True


def createOtherMetadata(other_data, general_data, folder_path, virtual_file):
    # sourcery skip: low-code-quality
    metadata = {}

    if "license" in other_data:
        metadata["license"] = other_data["license"]

    if "creationDate" in other_data and other_data["creationDate"] != "":
        metadata["dateCreated"] = other_data["creationDate"]

    if "firstReleaseDate" in other_data and other_data["firstReleaseDate"] != "":
        metadata["dateCreated"] = other_data["firstReleaseDate"]

    if "name" in other_data and other_data["name"] != "":
        metadata["name"] = other_data["name"]

    if "identifier" in other_data and other_data["identifier"] != "":
        metadata["identifier"] = other_data["identifier"]

    if "description" in other_data and other_data["description"] != "":
        metadata["description"] = other_data["description"]

    if "fundingCode" in other_data and other_data["fundingCode"] != "":
        metadata["fundingCode"] = other_data["fundingCode"]

    if "fundingOrganization" in other_data and other_data["fundingOrganization"] != "":
        metadata["fundingOrganization"] = other_data["fundingOrganization"]

    if "developmentStatus" in other_data and other_data["developmentStatus"] != "":
        metadata["developmentStatus"] = other_data["developmentStatus"]

    if "isPartOf" in other_data and other_data["isPartOf"] != "":
        metadata["isPartOf"] = other_data["isPartOf"]

    if (
        "referencePublication" in other_data
        and other_data["referencePublication"] != ""
    ):
        metadata["referencePublication"] = other_data["referencePublication"]

    if "keywords" in other_data and len(other_data["keywords"]) > 0:
        metadata["keywords"] = [item["keyword"] for item in other_data["keywords"]]

    if "relatedLinks" in other_data and len(other_data["relatedLinks"]) > 0:
        metadata["relatedLink"] = [item["link"] for item in other_data["relatedLinks"]]

    if "authors" in other_data and len(other_data["authors"]) > 0:
        metadata["author"] = []

        for item in other_data["authors"]:
            new_author = {"@type": "Person"}

            if "orcid" in item and item["orcid"] != "":
                new_author["@id"] = "https://orcid.org/" + item["orcid"]

            if "givenName" in item:
                new_author["givenName"] = item["givenName"]

            if "familyName" in item and item["familyName"] != "":
                new_author["familyName"] = item["familyName"]

            if "email" in item and item["email"] != "":
                new_author["email"] = item["email"]

            if "affiliation" in item and item["affiliation"] != "":
                new_author["affiliation"] = {
                    "@type": "Organization",
                    "name": item["affiliation"],
                }

            metadata["author"].append(new_author)

    if "contributors" in other_data and len(other_data["contributors"]) > 0:
        metadata["contributor"] = []

        for item in other_data["contributors"]:
            new_contributor = {"@type": "Person"}

            if "orcid" in item and item["orcid"] != "":
                new_contributor["@id"] = "https://orcid.org/" + item["orcid"]

            if "givenName" in item:
                new_contributor["givenName"] = item["givenName"]

            if "familyName" in item and item["familyName"] != "":
                new_contributor["familyName"] = item["familyName"]

            if "email" in item and item["email"] != "":
                new_contributor["email"] = item["email"]

            if "affiliation" in item and item["affiliation"] != "":
                new_contributor["affiliation"] = {"@type": "Organization"}
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
        f.write(json.dumps(metadata, indent=4))
    return True


def createCitationFromCode(code_data, general_data, folder_path, virtual_file):
    # Create the citation file
    citationObject = {
        "cff-version": "1.2.0",
    }

    if "name" in general_data and general_data["name"] != "":
        citationObject["title"] = general_data["name"]

    citationObject["message"] = "If you use this software, please cite it as below."
    citationObject["type"] = "software"

    if "authors" in general_data and len(general_data["authors"]) > 0:
        citationObject["authors"] = []

        for item in general_data["authors"]:
            new_author = {}

            if "orcid" in item and item["orcid"] != "":
                new_author["orcid"] = item["orcid"]

            if "givenName" in item:
                new_author["given-names"] = item["givenName"]

            if "familyName" in item:
                new_author["family-names"] = item["familyName"]

            if "email" in item and item["email"] != "":
                new_author["email"] = item["email"]

            if "affiliation" in item and item["affiliation"] != "":
                new_author["affiliation"] = item["affiliation"]

            citationObject["authors"].append(new_author)

    if "identifier" in code_data and code_data["identifier"] != "":
        citationObject["identifiers"] = []

        identifier = {}
        identifier["type"] = "doi"
        identifier["value"] = code_data["identifier"]
        identifier["description"] = "DOI for this software's record on Zenodo"

        citationObject["identifiers"].append(identifier)

    if "codeRepository" in code_data and code_data["codeRepository"] != "":
        citationObject["repository-code"] = code_data["codeRepository"]

    if "isPartOf" in code_data and code_data["isPartOf"] != "":
        citationObject["url"] = code_data["isPartOf"]

    if (
        "currentVersionDownloadLink" in code_data
        and code_data["currentVersionDownloadLink"] != ""
    ):
        citationObject["repository-artifact"] = code_data["currentVersionDownloadLink"]

    if "description" in general_data and general_data["description"] != "":
        citationObject["abstract"] = general_data["description"]

    if "keywords" in general_data and len(general_data["keywords"]) > 0:
        citationObject["keywords"] = []

        for item in general_data["keywords"]:
            citationObject["keywords"].append(item["keyword"])

    if "license" in code_data:
        citationObject["license"] = code_data["license"]

    if "currentVersion" in code_data and code_data["currentVersion"] != "":
        citationObject["version"] = code_data["currentVersion"]

    if (
        "currentVersionReleaseDate" in code_data
        and code_data["currentVersionReleaseDate"] != ""
    ):
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


def createNextGenHighThroughputSequencingMetadata(metadata):
    # sourcery skip: low-code-quality

    def generateChecksum(filePath):
        with open(filePath, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()

    homeFolderPath = os.path.expanduser("~")
    tempFolderPath = os.path.join(homeFolderPath, ".fairshare", "temp")
    metadataFilePath = os.path.join(tempFolderPath, "metadata.xlsx")

    os.makedirs(tempFolderPath, exist_ok=True)

    if os.path.exists(metadataFilePath):
        os.remove(metadataFilePath)

    workbook = xlsxwriter.Workbook(metadataFilePath)

    header_text_cell_format = workbook.add_format(
        {"bold": True, "font_name": "Arial", "font_size": 10}
    )
    red_text_cell_format = workbook.add_format(
        {"bold": True, "font_name": "Arial", "font_size": 10, "font_color": "red"}
    )
    comment_text_cell_format = workbook.add_format(
        {
            "bold": True,
            "font_name": "Arial",
            "font_size": 10,
            "bg_color": "#DBDBDB",
            "font_color": "#305496",
        }
    )

    blue_header_text_cell_format = workbook.add_format(
        {
            "bold": True,
            "font_name": "Arial",
            "font_size": 10,
            "bg_color": "#BDD7EE",
            "font_color": "#833C0C",
        }
    )
    default_text_cell_format = workbook.add_format(
        {"font_name": "Arial", "font_size": 10}
    )

    blue_heading_cell_format = workbook.add_format(
        {"bold": True, "font_name": "Arial", "font_size": 10, "bg_color": "#BDD7EE"}
    )
    green_heading_cell_format = workbook.add_format(
        {"bold": True, "font_name": "Arial", "font_size": 10, "bg_color": "#E2EFDA"}
    )

    header_row_format = workbook.add_format({"bg_color": "#BDD7EE"})
    comment_row_format = workbook.add_format({"bg_color": "#DBDBDB"})

    comment_text_cell_format.set_bottom()
    comment_text_cell_format.set_top()

    comment_row_format.set_bottom()
    comment_row_format.set_top()

    metadataWorksheet = workbook.add_worksheet("Metadata")

    column = 0
    row = 0

    metadataWorksheet.write(row, column, "STUDY", header_text_cell_format)
    metadataWorksheet.write(row, column + 1, metadata["study"], red_text_cell_format)

    row += 1

    metadataWorksheet.write(row, column, "title", blue_header_text_cell_format)
    metadataWorksheet.write(
        row, column + 1, metadata["title"], default_text_cell_format
    )

    row += 1

    metadataWorksheet.write(
        row, column, "summary (abstract)", blue_header_text_cell_format
    )
    metadataWorksheet.write(
        row, column + 1, metadata["summary"], default_text_cell_format
    )

    row += 1

    metadataWorksheet.write(
        row, column, "experimental design", blue_header_text_cell_format
    )
    metadataWorksheet.write(
        row, column + 1, metadata["experimentalDesign"], default_text_cell_format
    )

    for item in metadata["contributors"]:
        row += 1

        metadataWorksheet.write(
            row, column, "contributor", blue_header_text_cell_format
        )
        metadataWorksheet.write(
            row, column + 1, item["contributor"], default_text_cell_format
        )

    for filepath in metadata["supplementaryFiles"]:
        row += 1

        metadataWorksheet.write(
            row, column, "supplementary file", blue_header_text_cell_format
        )
        metadataWorksheet.write(
            row, column + 1, os.path.basename(filepath), default_text_cell_format
        )

    row += 4  # 3 rows of empty space

    metadataWorksheet.write(row, column, "SAMPLES", header_text_cell_format)

    row += 1

    metadataWorksheet.write(row, column, "library name", blue_heading_cell_format)
    metadataWorksheet.write(row, column + 1, "title", blue_heading_cell_format)
    metadataWorksheet.write(row, column + 2, "organism", blue_heading_cell_format)

    i = 0

    for key in metadata["samples"][0]["characteristics"]:
        metadataWorksheet.write(row, column + 3 + i, key, green_heading_cell_format)
        i += 1

    column = column + 3 + i  # reset the column index to 0 for the next section

    metadataWorksheet.write(row, column + 0, "molecule", blue_heading_cell_format)
    metadataWorksheet.write(
        row, column + 1, "single or paired-end", blue_heading_cell_format
    )
    metadataWorksheet.write(
        row, column + 2, "instrument model", blue_heading_cell_format
    )
    metadataWorksheet.write(row, column + 3, "description", blue_heading_cell_format)

    max_processed_files = 0
    max_raw_files = 0

    for sample in metadata["samples"]:
        if len(sample["processedDataFiles"]) > max_processed_files:
            max_processed_files = len(sample["processedDataFiles"])
        if len(sample["rawFiles"]) > max_raw_files:
            max_raw_files = len(sample["rawFiles"])

    i = 0

    processedDataFilesIndex = column + 4 + i

    while i < max_processed_files:
        metadataWorksheet.write(
            row, column + 4 + i, "processed data file", green_heading_cell_format
        )
        i += 1

    rawFilesIndex = column = (
        column + 4 + i
    )  # reset the column index to 0 for the next section

    i = 0

    while i < max_raw_files:
        metadataWorksheet.write(row, column + i, "raw file", green_heading_cell_format)
        i += 1

    for sample in metadata["samples"]:
        row += 1
        column = 0  # reset the column index to 0 for the next section

        metadataWorksheet.write(
            row, column, sample["libraryName"], default_text_cell_format
        )
        metadataWorksheet.write(
            row, column + 1, sample["title"], default_text_cell_format
        )
        metadataWorksheet.write(
            row, column + 2, sample["organism"], default_text_cell_format
        )

        i = 0

        for key in sample["characteristics"]:
            metadataWorksheet.write(
                row,
                column + 3 + i,
                sample["characteristics"][key],
                default_text_cell_format,
            )
            i += 1

        column = column + 3 + i  # reset the column index to 0 for the next section

        metadataWorksheet.write(
            row, column + 0, sample["molecule"], default_text_cell_format
        )
        metadataWorksheet.write(
            row, column + 1, sample["singleOrPairedEnd"], default_text_cell_format
        )
        metadataWorksheet.write(
            row, column + 2, sample["instrumentModel"], default_text_cell_format
        )
        metadataWorksheet.write(
            row, column + 3, sample["description"], default_text_cell_format
        )

        for i, processedDataFile in enumerate(sample["processedDataFiles"]):
            metadataWorksheet.write(
                row,
                processedDataFilesIndex + i,
                os.path.basename(processedDataFile),
                default_text_cell_format,
            )

        for i, rawFile in enumerate(sample["rawFiles"]):
            metadataWorksheet.write(
                row,
                rawFilesIndex + i,
                os.path.basename(rawFile),
                default_text_cell_format,
            )

    row += 3  # 2 rows of empty space
    column = 0  # reset the column index to 0 for the next section

    metadataWorksheet.write(row, column, "PROTOCOLS", header_text_cell_format)

    row += 1

    metadataWorksheet.write(
        row, column, "growth protocol", blue_header_text_cell_format
    )
    metadataWorksheet.write(row, column + 1, metadata["growthProtocol"])

    row += 1

    metadataWorksheet.write(
        row, column, "treatment protocol", blue_header_text_cell_format
    )
    metadataWorksheet.write(row, column + 1, metadata["treatmentProtocol"])

    row += 1

    metadataWorksheet.write(
        row, column, "extract protocol", blue_header_text_cell_format
    )
    metadataWorksheet.write(row, column + 1, metadata["extractProtocol"])

    row += 1

    metadataWorksheet.write(
        row, column, "library construction protocol", blue_header_text_cell_format
    )
    metadataWorksheet.write(row, column + 1, metadata["libraryConstructionProtocol"])

    row += 1

    libraryStrategy = metadata["libraryStrategy"]

    if libraryStrategy == "OTHER:":
        libraryStrategy = f"{libraryStrategy} {metadata['otherLibraryStrategy']}"

    metadataWorksheet.write(
        row, column, "library strategy", blue_header_text_cell_format
    )
    metadataWorksheet.write(row, column + 1, libraryStrategy)

    row += 1

    # Weird empty cell in the middle of the protocols section in the template
    # TODO: Figure out why this is necessary
    metadataWorksheet.write(row, column, "", blue_header_text_cell_format)
    metadataWorksheet.write(row, column + 1, "")

    for item in metadata["dataProcessingSteps"]:
        row += 1

        metadataWorksheet.write(
            row, column, "data processing step", blue_header_text_cell_format
        )
        metadataWorksheet.write(row, column + 1, item["step"], default_text_cell_format)

    row += 1

    metadataWorksheet.write(
        row, column, "genome build/assembly", blue_header_text_cell_format
    )
    metadataWorksheet.write(row, column + 1, metadata["genomeBuild"])

    row += 1

    metadataWorksheet.write(
        row,
        column,
        "processed data files format and content",
        blue_header_text_cell_format,
    )
    metadataWorksheet.write(row, column + 1, metadata["processedDataFilesFormat"])

    row += 3  # 2 rows of empty space

    max_raw_files = 0
    pairedEndPresent = False

    for sample in metadata["samples"]:
        if sample["singleOrPairedEnd"] == "paired-end":
            pairedEndPresent = True

            if len(sample["rawFiles"]) > max_raw_files:
                max_raw_files = len(sample["rawFiles"])

    if pairedEndPresent:
        metadataWorksheet.write(
            row, column, "PAIRED-END EXPERIMENTS", header_text_cell_format
        )

    row += 1

    i = 0

    while i < max_raw_files:
        metadataWorksheet.write(
            row, column + i, f"file name {i + 1}", blue_heading_cell_format
        )
        i += 1

    for sample in metadata["samples"]:
        if sample["singleOrPairedEnd"] == "paired-end":
            row += 1
            column = 0

            for i, rawFile in enumerate(sample["rawFiles"]):
                metadataWorksheet.write(
                    row, column + i, os.path.basename(rawFile), default_text_cell_format
                )

    # Add the checksums worksheet to the metadata file.

    checksumsWorksheet = workbook.add_worksheet("MD5 Checksums")

    column = 0
    row = 0

    checksumsWorksheet.write(row, column, "RAW FILES", header_text_cell_format)

    row += 1

    checksumsWorksheet.set_row(row, cell_format=header_row_format)
    checksumsWorksheet.write(row, column, "file name", blue_heading_cell_format)
    checksumsWorksheet.write(row, column + 1, "file checksum", blue_heading_cell_format)

    for sample in metadata["samples"]:
        for file in sample["rawFiles"]:
            row += 1

            checksumsWorksheet.write(
                row, column, os.path.basename(file), default_text_cell_format
            )
            checksumsWorksheet.write(row, column + 1, generateChecksum(file))

    workbook.close()


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

        if "Immunology" in data_types:
            immunology_data = data["Immunology"]["questions"]
            folder_path = ""

            if "folderPath" in data["Immunology"]:
                folder_path = data["Immunology"]["folderPath"]
            result = createImmunologyMetadata(
                immunology_data, folder_path, virtual_file
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

        if "NextGenHighThroughputSequencing" in data_types:
            next_gen_high_throughput_sequencing_data = data[
                "NextGenHighThroughputSequencing"
            ]["questions"]

            result = createNextGenHighThroughputSequencingMetadata(
                next_gen_high_throughput_sequencing_data,
            )

        return "SUCCESS"
    except Exception as e:
        raise e
