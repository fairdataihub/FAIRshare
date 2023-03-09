import ftplib
import json
import os

UPLOAD_STATUS = {
    "status": "",
}


def uploadFolderToGeo(
    FTP_SERVER, FTP_USER, FTP_PASSWORD, ftpFolderPath, localFolderPath
):
    global UPLOAD_STATUS
    numberOfFiles = 0

    def uploadFolder(folderPath):
        global UPLOAD_STATUS
        nonlocal session

        files = os.listdir(folderPath)
        os.chdir(folderPath)

        for f in files:
            filePath = f"{folderPath}/{f}"

            if os.path.isfile(filePath):
                UPLOAD_STATUS["currentFileNumber"] = (
                    UPLOAD_STATUS["currentFileNumber"] + 1
                )

                UPLOAD_STATUS["message"] = f"Uploading {f}"

                with open(f, "rb") as fh:
                    session.storbinary(f"STOR {f}", fh)
            elif os.path.isdir(filePath):
                session.mkd(f)
                session.cwd(f)

                uploadFolder(filePath)

        session.cwd("..")
        os.chdir("..")

    try:
        UPLOAD_STATUS["message"] = "Connecting to FTP server..."
        UPLOAD_STATUS["currentFileNumber"] = 0

        session = ftplib.FTP(FTP_SERVER, FTP_USER, FTP_PASSWORD)
        session.cwd(ftpFolderPath)

        localFolderName = os.path.basename(localFolderPath)

        numberOfFiles = sum([len(files) for r, d, files in os.walk(localFolderPath)])
        UPLOAD_STATUS["totalFiles"] = numberOfFiles

        session.mkd(localFolderName)
        session.cwd(localFolderName)

        uploadFolder(localFolderPath)

        UPLOAD_STATUS["currentFileNumber"] = 0

        session.quit()

        UPLOAD_STATUS["message"] = ""

        return "SUCCESS"

    except Exception as e:
        raise e


def getFilesAndFoldersAtLocation(FTP_SERVER, FTP_USER, FTP_PASSWORD, ftpFolderPath):
    try:
        session = ftplib.FTP(FTP_SERVER, FTP_USER, FTP_PASSWORD)
        session.cwd(ftpFolderPath)

        files = session.nlst()
        folders = session.dir()

        session.quit()

        return files, folders

    except Exception as e:
        raise e


def getGEOFileUploadStatus():
    return json.dumps(UPLOAD_STATUS)
