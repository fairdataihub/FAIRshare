import os
import ftplib

# TODO: Clean all of this up

myFTP = ftplib.FTP(FTP_SERVER, FTP_USER, FTP_PASSWORD)
myFTP.cwd(FTP_UPLOAD_SPACE)


myPath = os.path.join(home, "Downloads", "thumbnails", "geo_submission_june28-4f702")

folderName = os.path.basename(myPath)

myFTP.mkd(folderName)
myFTP.cwd(folderName)


def uploadThis(folderPath):
    files = os.listdir(folderPath)
    os.chdir(folderPath)
    for f in files:
        filePath = f"{folderPath}/{f}"
        if os.path.isfile(filePath):
            fh = open(f, "rb")
            myFTP.storbinary("STOR %s" % f, fh)
            fh.close()
        elif os.path.isdir(filePath):
            myFTP.mkd(f)
            myFTP.cwd(f)
            uploadThis(filePath)
    myFTP.cwd("..")
    os.chdir("..")


uploadThis(myPath)
