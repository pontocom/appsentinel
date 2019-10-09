import xlsxwriter
import json
import datetime
import requests
import configparser

config = configparser.ConfigParser()
config.read('../config.ini')

workbook = xlsxwriter.Workbook("tests.xlsx")
aptoide_API_endpoint = config['DOWNLOAD']['aptoideAPIEndpoint']


def get_json_data(which_apk):
    response = requests.get(aptoide_API_endpoint + which_apk)
    jsondata = response.json()
    return jsondata


def run_multiple_tests(number_apk):
    vars = ["#", "MD5", "Start Time", "End Time", "Duration", "Name", "Package", "Downloads", "APK Size", "Version Name", "Version Code"]
    sheet = workbook.add_worksheet("Results - Multiple (" + str(number_apk) + ")")


def run_sequence_tests():
    vars = ["#", "MD5", "Start Time", "End Time", "Duration", "Name", "Package", "Downloads", "APK Size", "Version Name", "Version Code"]
    sheet = workbook.add_worksheet("Results - Sequence")
    bold = workbook.add_format({'bold': True})
    # write the header
    cols = 0
    for var in vars:
        sheet.write(0, cols, var, bold)
        cols = cols + 1

    count = 0
    rows = 1
    with open('apks.txt') as f:
        for line in f:
            id_app = line
            data = get_json_data(id_app)
            count = count + 1
            sheet.write(rows, 0, count)
            sheet.write(rows, 1, data["nodes"]["meta"]["data"]["file"]["md5sum"])
            print(data["nodes"]["meta"]["data"]["file"]["md5sum"])
            sheet.write(rows, 2, datetime.datetime.now().timestamp())
            # all the relevant stuff should happen here
            #######
            sheet.write(rows, 3, datetime.datetime.now().timestamp())
            sheet.write(rows, 4, "=D"+str(rows+1)+"-C"+str(rows+1))
            sheet.write(rows, 5, data["nodes"]["meta"]["data"]["name"])
            sheet.write(rows, 6, data["nodes"]["meta"]["data"]["package"])
            sheet.write(rows, 7, data["nodes"]["meta"]["data"]["store"]["stats"]["downloads"])
            sheet.write(rows, 8, data["nodes"]["meta"]["data"]["size"])
            sheet.write(rows, 9, data["nodes"]["meta"]["data"]["file"]["vername"])
            sheet.write(rows, 10, data["nodes"]["meta"]["data"]["file"]["vercode"])
            rows = rows + 1



if __name__=="__main__":
    run_sequence_tests()
    run_multiple_tests(10)
    workbook.close()
