import xlsxwriter
import os
import datetime
import requests
import manager as man
import os.path
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

workbook = xlsxwriter.Workbook("./tests/testResults-"+str(datetime.datetime.now())+".xlsx")
aptoide_API_endpoint = config['DOWNLOAD']['aptoideAPIEndpoint']
dir = config['DOWNLOAD']['apkDownloadDir']


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
            id_app = line[:len(line) - 1]
            data = man.get_json_data(id_app)
            count = count + 1
            sheet.write(rows, 0, count)
            sheet.write(rows, 1, data["nodes"]["meta"]["data"]["file"]["md5sum"])
            print(data["nodes"]["meta"]["data"]["file"]["md5sum"])
            appPath = data["nodes"]["meta"]["data"]["file"]["path"]
            print("appPath = " + appPath)
            apkfile = appPath[appPath.rfind("/") + 1:]
            print("apkFile = " + apkfile)
            man.download_apk(appPath)
            starttime = datetime.datetime.now()
            format2 = workbook.add_format({'num_format': 'dd/mm/yy hh:mm:ss'})
            sheet.write(rows, 2, starttime, format2)
            # all the relevant stuff should happen here
            #######
            man.write_json_data(data, id_app)
            print(config['GENERAL']['python3cmd'] + " scanner.py --md5 " + id_app + " --file " + dir + "/" + apkfile)
            os.system(config['GENERAL']['python3cmd'] + " scanner.py --md5 " + id_app + " --file " + dir + "/" + apkfile)
            format3 = workbook.add_format({'num_format': 'dd/mm/yy hh:mm:ss'})
            endtime = datetime.datetime.now()
            sheet.write(rows, 3, endtime, format3)
            format4 = workbook.add_format({'num_format': 'mm:ss'})
            sheet.write(rows, 4, "=D"+str(rows+1)+"-C"+str(rows+1), format4)
            sheet.write(rows, 5, data["nodes"]["meta"]["data"]["name"])
            sheet.write(rows, 6, data["nodes"]["meta"]["data"]["package"])
            sheet.write(rows, 7, data["nodes"]["meta"]["data"]["store"]["stats"]["downloads"])
            sheet.write(rows, 8, data["nodes"]["meta"]["data"]["size"])
            sheet.write(rows, 9, data["nodes"]["meta"]["data"]["file"]["vername"])
            sheet.write(rows, 10, data["nodes"]["meta"]["data"]["file"]["vercode"])
            rows = rows + 1


def run_sequence_tests_from_scraping():
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

    print(dir)

    for file in os.listdir(dir):
        if file[-4:] == ".apk":
            id_app = file[-36:-4]
            data = man.get_json_data(id_app)
            count = count + 1
            sheet.write(rows, 0, count)
            sheet.write(rows, 1, data["nodes"]["meta"]["data"]["file"]["md5sum"])
            starttime = datetime.datetime.now()
            format2 = workbook.add_format({'num_format': 'dd/mm/yy hh:mm:ss'})
            sheet.write(rows, 2, starttime, format2)
            # all the relevant stuff should happen here
            #######
            man.write_json_data(data, id_app)
            print(config['GENERAL']['python3cmd'] + " scanner.py --md5 " + id_app + " --file " + dir + "/" + file)
            os.system(config['GENERAL']['python3cmd'] + " scanner.py --md5 " + id_app + " --file " + dir + "/" + file)
            format3 = workbook.add_format({'num_format': 'dd/mm/yy hh:mm:ss'})
            endtime = datetime.datetime.now()
            sheet.write(rows, 3, endtime, format3)
            format4 = workbook.add_format({'num_format': 'mm:ss'})
            sheet.write(rows, 4, "=D" + str(rows + 1) + "-C" + str(rows + 1), format4)
            sheet.write(rows, 5, data["nodes"]["meta"]["data"]["name"])
            sheet.write(rows, 6, data["nodes"]["meta"]["data"]["package"])
            sheet.write(rows, 7, data["nodes"]["meta"]["data"]["store"]["stats"]["downloads"])
            sheet.write(rows, 8, data["nodes"]["meta"]["data"]["size"])
            sheet.write(rows, 9, data["nodes"]["meta"]["data"]["file"]["vername"])
            sheet.write(rows, 10, data["nodes"]["meta"]["data"]["file"]["vercode"])
            rows = rows + 1


if __name__=="__main__":
    run_sequence_tests_from_scraping()
    run_multiple_tests(10)
    workbook.close()
