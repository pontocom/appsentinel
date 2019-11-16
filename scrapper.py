import requests
import xlsxwriter
import os
import datetime
from bs4 import BeautifulSoup
import manager as man
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

aptoide_API_endpoint = config['DOWNLOAD']['aptoideAPIEndpoint']
dir = config['DOWNLOAD']['apkDownloadDir']

DEFAULT_URL = "https://en.aptoide.com/group/applications"

workbook = xlsxwriter.Workbook("./tests/testResults-init-"+str(datetime.datetime.now())+".xlsx")


def run_scrapper():
    print("Starting web scrapping of Aptoide web site.... :-)")
    print("... getting stuff from ->" + DEFAULT_URL)
    response = requests.get(DEFAULT_URL)
    html = BeautifulSoup(response.text, 'html.parser')

    vars = ["#", "MD5", "Name", "Package", "Category", "Downloads", "APK Size", "Version Name", "Version Code"]
    sheet = workbook.add_worksheet("Results - Sequence")
    bold = workbook.add_format({'bold': True})
    # write the header
    cols = 0
    for var in vars:
        sheet.write(0, cols, var, bold)
        cols = cols + 1

    count = 0
    rows = 1

    # print("Extracting categories...")
    categories = html.find_all(class_="aptweb-button aptweb-button--see-more")

    for category in categories:
        category_location = category.find("a")['href']
        print("Entering -> " + category_location)

        category_page_response = requests.get(category_location)
        category_page_html = BeautifulSoup(category_page_response.text, 'html.parser')

        category_name = category_page_html.find("h1").text.strip()
        # print(category_name)

        # bundle = category_page_html.find_all(class_="bundle")
        cat_button_more_location = \
        category_page_html.find_all(class_="bundle")[2].find(class_="aptweb-button aptweb-button--see-more").find("a")[
            'href']
        # print("Now getting -> " + cat_button_more_location)

        apps_page_response = requests.get(cat_button_more_location)
        apps_page_html = BeautifulSoup(apps_page_response.text, 'html.parser')

        apps_html = apps_page_html.find_all(class_="bundle-item__info__span bundle-item__info__span--big")

        for app in apps_html:
            if app.find("a") != "None":
                app_location = app.find("a")['href']

                # print("Entering App Page -> " + app_location)

                app_page_response = requests.get(app_location)
                if app_page_response:
                    app_page_html = BeautifulSoup(app_page_response.text, 'html.parser')

                    info_table = app_page_html.find_all(class_="app-info__row")
                    id_app = info_table[8].find_all("td")[1].get_text()
                    # download the APK to local temp dir
                    data = man.get_json_data(id_app)

                    count = count + 1
                    print("[" + str(count) + "][" + category_name + "][" + data["nodes"]["meta"]["data"]["file"]["md5sum"] + "][" + info_table[0].find_all("td")[1].get_text() + " : " + info_table[8].find_all("td")[1].get_text() + "]")

                    sheet.write(rows, 0, count)
                    sheet.write(rows, 1, data["nodes"]["meta"]["data"]["file"]["md5sum"])

                    appPath = data["nodes"]["meta"]["data"]["file"]["path"]
                    man.download_apk(appPath)

                    sheet.write(rows, 2, data["nodes"]["meta"]["data"]["name"])
                    sheet.write(rows, 3, data["nodes"]["meta"]["data"]["package"])
                    sheet.write(rows, 4, category_name)
                    sheet.write(rows, 5, data["nodes"]["meta"]["data"]["store"]["stats"]["downloads"])
                    sheet.write(rows, 6, data["nodes"]["meta"]["data"]["size"])
                    sheet.write(rows, 7, data["nodes"]["meta"]["data"]["file"]["vername"])
                    sheet.write(rows, 8, data["nodes"]["meta"]["data"]["file"]["vercode"])
                    rows = rows + 1


def run_analyse_downloads():
    vars = ["#", "MD5", "Name", "Package", "Category", "Downloads", "APK Size", "Version Name", "Version Code"]
    sheet = workbook.add_worksheet("Results - Sequence")
    bold = workbook.add_format({'bold': True})
    # write the header
    cols = 0
    for var in vars:
        sheet.write(0, cols, var, bold)
        cols = cols + 1

    count = 0
    rows = 1

    for file in os.listdir(dir):
        if file[-4:] == ".apk":
            id_app = file[-36:-4]
            count = count + 1
            sheet.write(rows, 0, count)
            sheet.write(rows, 1, id_app)
            # download the APK to local temp dir
            data = man.get_json_data(id_app)

            print("[" + str(count) + "][" + data["nodes"]["meta"]["data"]["file"]["md5sum"] + "][" + data["nodes"]["meta"]["data"]["name"] + "]")
            sheet.write(rows, 0, count)
            sheet.write(rows, 1, data["nodes"]["meta"]["data"]["file"]["md5sum"])
            sheet.write(rows, 2, data["nodes"]["meta"]["data"]["name"])
            sheet.write(rows, 3, data["nodes"]["meta"]["data"]["package"])
            sheet.write(rows, 4, "")
            sheet.write(rows, 5, data["nodes"]["meta"]["data"]["store"]["stats"]["downloads"])
            sheet.write(rows, 6, data["nodes"]["meta"]["data"]["size"])
            sheet.write(rows, 7, data["nodes"]["meta"]["data"]["file"]["vername"])
            sheet.write(rows, 8, data["nodes"]["meta"]["data"]["file"]["vercode"])
            rows = rows + 1


'''
A tool to scan APKs and look for vulnerabilities
'''
if __name__ == "__main__":
    run_scrapper()
    #run_analyse_downloads()
    workbook.close()
