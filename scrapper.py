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

BASE_URL = "https://en.aptoide.com"
DEFAULT_URL = BASE_URL + "/group/applications"

APPS_PER_CATEGORY = 1

workbook = xlsxwriter.Workbook("./tests/testResults-init-" + str(datetime.datetime.now()) + ".xlsx")


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
    categories = html.find_all(class_="bundle-header__ButtonContainer-sc-5qh14w-2")

    for category in categories:
        category_location = category.find("a")['href']
        print("Entering -> " + BASE_URL + category_location)

        category_page_response = requests.get(BASE_URL + category_location)
        category_page_html = BeautifulSoup(category_page_response.text, 'html.parser')

        category_name = category_page_html.find("h1").text.strip()
        print("CATEGORY = [" + category_name + "]")

        # bundle = category_page_html.find_all(class_="bundle")
        # cat_button_more_location = category_page_html.find_all(class_="bundle")[0].find(class_="aptweb-button aptweb-button--see-more").find("a")['href']
        # print("Now getting -> " + cat_button_more_location)

        # apps_page_response = requests.get(cat_button_more_location)
        # apps_page_html = BeautifulSoup(apps_page_response.text, 'html.parser')

        apps_html = apps_page_html.find_all(class_="bundle-item__info__span bundle-item__info__span--big")

        # small modification to consider only the top 10 apps in each category 
        count_apps = 0
        for app in apps_html:
            if app.find("a") != "None" and count_apps <= APPS_PER_CATEGORY:
                app_location = app.find("a")['href']

                print("Entering App Page -> " + app_location)

                app_page_response = requests.get(app_location)
                if app_page_response:
                    app_page_html = BeautifulSoup(app_page_response.text, 'html.parser')

                    info_table = app_page_html.find_all(class_="app-info__row")
                    id_app = info_table[8].find_all("td")[1].get_text()
                    # download the APK to local temp dir
                    data = man.get_json_data(id_app)

                    count = count + 1
                    print("[" + str(count) + "][" + category_name + "][" + str(count_apps + 1) + "][" +
                          data["nodes"]["meta"]["data"]["file"]["md5sum"] + "][" + info_table[0].find_all("td")[
                              1].get_text() + " : " + info_table[8].find_all("td")[1].get_text() + "]")

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
                    count_apps = count_apps + 1
            if count_apps == 10:
                break


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
            print(data)
            exit(0)

            print("[" + str(count) + "][" + data["nodes"]["meta"]["data"]["file"]["md5sum"] + "][" +
                  data["nodes"]["meta"]["data"]["name"] + "]")
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


def download_all_apks():
    count = 1
    w = open('./apks_failed.txt', 'w')
    with open('./apks.txt') as f:
        for line in f:
            id_app = line
            data = man.get_json_data(id_app)
            # print(data)
            if (data["info"]["status"] != "FAIL"):
                appPath = data["nodes"]["meta"]["data"]["file"]["path"]
                print("[" + str(count) + "][" + appPath + "]")
                man.download_apk(appPath)
            else:
                w.write(str(id_app))
            count = count + 1
    w.close()


'''
A tool to scan APKs and look for vulnerabilities
'''
if __name__ == "__main__":
    # run_scrapper()
    # download_all_apks()
    run_analyse_downloads()
    workbook.close()
