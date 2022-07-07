import ftplib
import os


def uploadFolderToGeo(
    FTP_SERVER, FTP_USER, FTP_PASSWORD, ftpFolderPath, localFolderPath
):
    def uploadFolder(folderPath):
        nonlocal session

        files = os.listdir(folderPath)
        os.chdir(folderPath)

        for f in files:
            filePath = f"{folderPath}/{f}"

            if os.path.isfile(filePath):
                with open(f, "rb") as fh:
                    session.storbinary(f"STOR {f}", fh)
            elif os.path.isdir(filePath):
                session.mkd(f)
                session.cwd(f)

                uploadFolder(filePath)

        session.cwd("..")
        os.chdir("..")

    try:
        session = ftplib.FTP(FTP_SERVER, FTP_USER, FTP_PASSWORD)
        session.cwd(ftpFolderPath)

        localFolderName = os.path.basename(localFolderPath)

        session.mkd(localFolderName)
        session.cwd(localFolderName)

        uploadFolder(localFolderPath)

        session.quit()

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
