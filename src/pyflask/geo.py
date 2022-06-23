import hashlib
import os

import xlsxwriter


def generateGeoChecksums(metadata):
    def generateChecksum(filePath):
        with open(filePath, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()

    homeFolderPath = os.path.expanduser("~")
    tempFolderPath = os.path.join(homeFolderPath, ".fairshare", "temp")
    metadataFilePath = os.path.join(tempFolderPath, "geoChecksums.xlsx")

    os.makedirs(tempFolderPath, exist_ok=True)

    try:

        if os.path.exists(metadataFilePath):
            os.remove(metadataFilePath)

        workbook = xlsxwriter.Workbook(metadataFilePath)

        header_text_cell_format = workbook.add_format(
            {"bold": True, "font_name": "Arial", "font_size": 10}
        )

        default_text_cell_format = workbook.add_format(
            {"font_name": "Arial", "font_size": 10}
        )

        comment_row_format = workbook.add_format({"bg_color": "#BDD7EE"})
        blue_heading_cell_format = workbook.add_format(
            {"bold": True, "font_name": "Arial", "font_size": 10, "bg_color": "#BDD7EE"}
        )

        worksheet = workbook.add_worksheet()

        column = 0
        row = 0

        worksheet.write(row, column, "RAW FILES", header_text_cell_format)

        row += 1

        worksheet.set_row(row, cell_format=comment_row_format)
        worksheet.write(row, column, "file name", blue_heading_cell_format)
        worksheet.write(row, column + 1, "file checksum", blue_heading_cell_format)

        for sample in metadata["samples"]:
            for file in sample["rawFiles"]:
                row += 1

                worksheet.write(
                    row, column, os.path.basename(file), default_text_cell_format
                )
                worksheet.write(row, column + 1, generateChecksum(file))

        workbook.close()

        return metadataFilePath

    except Exception as e:
        raise e
