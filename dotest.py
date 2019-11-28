import xlsxwriter
import os
import datetime
import requests
import manager as man
import owasp_engine as oe
import os.path
import configparser
import json

config = configparser.ConfigParser()
config.read('config.ini')

workbook = xlsxwriter.Workbook("./tests/testResults-analysis-"+str(datetime.datetime.now())+".xlsx")
aptoide_API_endpoint = config['DOWNLOAD']['aptoideAPIEndpoint']
dir = config['DOWNLOAD']['apkDownloadDir']
dir_results = config['SCANNER']['jsonResultsLocation']
resultsFeedback = config['OWASP_OUTPUT']['feedbackResultsLocation']


def put_the_results_on_database():
    count = 0
    for file in os.listdir(dir_results + "/Androbugs"):
        if file[-5:] == ".json":
            id_app = file[-37:-5]
            if os.path.exists(dir_results + "/Androbugs/" + file) and os.path.exists(dir_results + "/DroidStatX/" + file):
                if os.path.getsize(dir_results + "/DroidStatX/" + file) != 0:
                    count = count + 1
                    print("[ANDROBUGS][" + str(count) + "][" + id_app + "][" + file + "]")
                    oe.startEngine(id_app)

    print("[ANDROBUGS COUNT]" + str(count))


def get_num_vulns():
    count = 0
    vars = ["#", "MD5", "M1", "M2", "M2", "M4", "M5", "M6", "M7", "M8", "M9", "M10"]
    sheet = workbook.add_worksheet("Results - OWASP")
    bold = workbook.add_format({'bold': True})
    # write the header
    cols = 0
    for var in vars:
        sheet.write(0, cols, var, bold)
        cols = cols + 1

    rows = 1
    for file in os.listdir(resultsFeedback):
        id_app = file[-37:-5]
        count = count + 1
        print("[ANDROBUGS][" + str(count) + "][" + id_app + "][" + file + "]")
        m1 = 0
        m2 = 0
        m3 = 0
        m4 = 0
        m5 = 0
        m6 = 0
        m7 = 0
        m8 = 0
        m9 = 0
        m10 = 0
        with open(resultsFeedback + '/' + id_app + ".json", "r") as json_file:
            read_content = json.load(json_file)

        m1 = len(read_content["M1"])
        m2 = len(read_content["M2"])
        m3 = len(read_content["M3"])
        m4 = len(read_content["M4"])
        m5 = len(read_content["M5"])
        m6 = len(read_content["M6"])
        m7 = len(read_content["M7"])
        m8 = len(read_content["M8"])
        m9 = len(read_content["M9"])
        m10 = len(read_content["M10"])

        sheet.write(rows, 0, count)
        sheet.write(rows, 1, id_app)
        sheet.write(rows, 2, m1)
        sheet.write(rows, 3, m2)
        sheet.write(rows, 4, m3)
        sheet.write(rows, 5, m4)
        sheet.write(rows, 6, m5)
        sheet.write(rows, 7, m6)
        sheet.write(rows, 8, m7)
        sheet.write(rows, 9, m8)
        sheet.write(rows, 10, m9)
        sheet.write(rows, 11, m10)
        print("M1:" + str(m1) + ":M2:" + str(m2) + ":M3:" + str(m3) + ":M4:" + str(m4) + ":M5:" + str(
            m5) + ":M6:" + str(m6) + ":M7:" + str(m7) + ":M8:" + str(m8) + ":M9:" + str(
            m9) + ":M10:" + str(m10))
        rows = rows + 1

    print("[ANDROBUGS COUNT]" + str(count))

    # for file in os.listdir(dir_results + "/Androbugs"):
    #     if file[-5:] == ".json":
    #         id_app = file[-37:-5]
    #         count = count + 1
    #         print("[ANDROBUGS][" + str(count) + "][" + id_app + "][" + file + "]")
    #         if os.path.exists(dir_results + "/DroidStatX/" + file):
    #             if os.path.getsize(dir_results + "/DroidStatX/" + file) != 0:
    #                 print(dir_results + "/Androbugs/" + file)
    #                 print(dir_results + "/DroidStatX/" + file)
    #                 print(resultsFeedback + '/' + id_app + ".json")
    #                 print(os.path.exists(resultsFeedback + '/' + id_app + ".json"))
    #                 m1 = 0
    #                 m2 = 0
    #                 m3 = 0
    #                 m4 = 0
    #                 m5 = 0
    #                 m6 = 0
    #                 m7 = 0
    #                 m8 = 0
    #                 m9 = 0
    #                 m10 = 0
    #                 if os.path.exists(resultsFeedback + '/' + id_app + ".json"):
    #                     with open(resultsFeedback + '/' + id_app + ".json", "r") as json_file:
    #                         read_content = json.load(json_file)
    #
    #                     if read_content:
    #                         m1 = len(read_content["M1"])
    #                         m2 = len(read_content["M2"])
    #                         m3 = len(read_content["M3"])
    #                         m4 = len(read_content["M4"])
    #                         m5 = len(read_content["M5"])
    #                         m6 = len(read_content["M6"])
    #                         m7 = len(read_content["M7"])
    #                         m8 = len(read_content["M8"])
    #                         m9 = len(read_content["M9"])
    #                         m10 = len(read_content["M10"])
    #
    #                 sheet.write(rows, 0, count)
    #                 sheet.write(rows, 1, id_app)
    #                 sheet.write(rows, 2, m1)
    #                 sheet.write(rows, 3, m2)
    #                 sheet.write(rows, 4, m3)
    #                 sheet.write(rows, 5, m4)
    #                 sheet.write(rows, 6, m5)
    #                 sheet.write(rows, 7, m6)
    #                 sheet.write(rows, 8, m7)
    #                 sheet.write(rows, 9, m8)
    #                 sheet.write(rows, 10, m9)
    #                 sheet.write(rows, 11, m10)
    #                 print("M1:" + str(m1) + ":M2:" + str(m2) + ":M3:" + str(m3) + ":M4:" + str(m4) + ":M5:" + str(
    #                     m5) + ":M6:" + str(m6) + ":M7:" + str(m7) + ":M8:" + str(m8) + ":M9:" + str(
    #                     m9) + ":M10:" + str(m10))
    #                 rows = rows + 1
    # print("[ANDROBUGS COUNT]" + str(count))


def run_post_processing():
    vars1 = ["#", "MD5", "Androbugs"]
    vars2 = ["#", "MD5", "Droidstatx"]
    sheet1 = workbook.add_worksheet("Androbugs")
    sheet2 = workbook.add_worksheet("Droidstatx")
    bold = workbook.add_format({'bold': True})
    # write the header
    cols = 0
    for var in vars1:
        sheet1.write(0, cols, var, bold)
        cols = cols + 1
    cols = 0
    for var in vars2:
        sheet2.write(0, cols, var, bold)
        cols = cols + 1

    count = 0
    rows = 1

    for file in os.listdir(dir_results + "/Androbugs"):
        if file[-5:] == ".json":
            id_app = file[-37:-5]
            count = count + 1
            print("[ANDROBUGS][" + str(count) + "][" + id_app + "][" + file + "]")
            sheet1.write(rows, 0, count)
            sheet1.write(rows, 1, id_app)
            if os.path.getsize(dir_results + "/Androbugs/" + file) == 0:
                sheet1.write(rows, 2, "N")
            else:
                sheet1.write(rows, 2, "Y")
            rows = rows + 1

    print("[ANDROBUGS COUNT]" + str(count))

    count = 0
    rows = 1

    for file in os.listdir(dir_results + "/DroidStatX"):
        if file[-5:] == ".json":
            id_app = file[-37:-5]
            count = count + 1
            sheet2.write(rows, 0, count)
            sheet2.write(rows, 1, id_app)
            print("[DROIDSTATX][" + str(count) + "][" + id_app + "][" + file + "]")
            if os.path.getsize(dir_results + "/DroidStatX/" + file) == 0:
                sheet2.write(rows, 2, "N")
            else:
                sheet2.write(rows, 2, "Y")
            rows = rows + 1

    print("[DROIDSTATX COUNT]" + str(count))


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
    vars = ["#", "MD5", "Start Time", "End Time", "Duration"]
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
            count = count + 1
            sheet.write(rows, 0, count)
            sheet.write(rows, 1, id_app)
            starttime = datetime.datetime.now()
            format2 = workbook.add_format({'num_format': 'dd/mm/yy hh:mm:ss'})
            sheet.write(rows, 2, starttime, format2)
            # all the relevant stuff should happen here
            #######
            print(config['GENERAL']['python3cmd'] + " scanner.py --md5 " + id_app + " --file " + dir + "/" + file)
            os.system(config['GENERAL']['python3cmd'] + " scanner.py --md5 " + id_app + " --file " + dir + "/" + file)
            format3 = workbook.add_format({'num_format': 'dd/mm/yy hh:mm:ss'})
            endtime = datetime.datetime.now()
            sheet.write(rows, 3, endtime, format3)
            format4 = workbook.add_format({'num_format': 'mm:ss'})
            sheet.write(rows, 4, "=D" + str(rows + 1) + "-C" + str(rows + 1), format4)
            rows = rows + 1


if __name__=="__main__":
    #run_sequence_tests_from_scraping()
    #run_multiple_tests(10)
    #run_post_processing()
    #put_the_results_on_database()
    get_num_vulns()
    workbook.close()
