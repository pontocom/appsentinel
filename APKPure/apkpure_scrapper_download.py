import requests
import xlsxwriter
import os
import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from tqdm import tqdm
import math
import hashlib
import pyfiglet

baseURL = 'https://apkpure.com'
APPS_PER_GROUP = 1

workbook = xlsxwriter.Workbook("./tests/testResults-APKpure-init-" + str(datetime.datetime.now()) + ".xlsx")

def download_apk(apk, link):
    # check if the download dir exists or not
    if not os.path.exists('./downloads'):
        os.system("mkdir " + './downloads')

    # write the file to the filesystem
    # a = urlparse(which_apk)
    # filename = dir + "/" + os.path.basename(a.path)
    filename = './downloads/' + apk + '.apk'

    # print(filename)

    # Streaming, so we can iterate over the response.
    r = requests.get(link, stream=True)

    # Total size in bytes.
    total_size = int(r.headers.get('content-length', 0))
    block_size = 1024
    wrote = 0
    with open(filename, 'wb') as f:
       for data in tqdm(r.iter_content(block_size), total=math.ceil(total_size // block_size), unit='KB',
                        unit_scale=True):
           wrote = wrote + len(data)
           f.write(data)
    if total_size != 0 and wrote != total_size:
       print("ERROR, something went wrong")


def run_scrapper():
    vars = ["#", "Name", "Package", "Category"]
    sheet = workbook.add_worksheet("Results - Sequence")
    bold = workbook.add_format({'bold': True})
    # write the header
    cols = 0
    for var in vars:
        sheet.write(0, cols, var, bold)
        cols = cols + 1

    count = 1
    rows = 1
    grpNumber = 0
    print("Starting web scrapping of APKPure web site.... :-)")

    # Run all the categories and download top apps as JSON format
    with open('apkpure_categories.txt', 'r') as f:
        allGroups = f.readlines()
        for group in allGroups:
            print('[' + str(grpNumber + 1) + '][' + group.rstrip('\r\n').upper() + ']')

            # run the scrapper for this category
            print('Getting...: ' + baseURL + '/' + group.rstrip('\r\n'))

            headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"}
            response = requests.get(baseURL + '/' + group.rstrip('\r\n'), headers=headers)
            print("Response -> " + str(response))

            html = BeautifulSoup(response.text, 'html.parser')

            # print("HTML ->" + str(html))

            apps = html.find_all(class_="category-template-img")
            # print("apps ->" + str(apps))
            apps_number = 1

            for app in apps:
                if apps_number <= APPS_PER_GROUP:
                    sheet.write(rows, 0, count)
                    app_name = app.find("a")['title']
                    app_location = app.find("a")['href']
                    print('[' + str(count) + '][' + app_name[:-4] + ']')
                    print("Entering -> " + baseURL + app_location)
                    a = urlparse(baseURL + app_location)
                    app_package = os.path.basename(a.path)
                    appresponse = requests.get(baseURL + app_location, headers=headers)
                    html2 = BeautifulSoup(appresponse.text, 'html.parser')
                    download_link = html2.find(class_="ny-down").find("a")['href']
                    print('Getting...: ' + baseURL + download_link)
                    response = requests.get(baseURL + download_link, headers=headers)
                    html3 = BeautifulSoup(response.text, 'html.parser')
                    download_link_apk = html3.find(class_="down-click").find("a")['href']
                    sheet.write(rows, 1, app_name[:-4])
                    sheet.write(rows, 2, app_package)
                    sheet.write(rows, 3, group.rstrip('\r\n').upper())

                    # print("Downloading -> " + download_link_apk)
                    download_apk(app_package, download_link_apk)
                    apps_number += 1
                    rows += 1
                    count += 1
                else:
                    break

            grpNumber += 1


def compute_md5():
    count = 0
    rows = 1
    vars = ["Package", "Md5"]
    sheet = workbook.add_worksheet("APK Md5")
    bold = workbook.add_format({'bold': True})
    # write the header
    cols = 0
    for var in vars:
        sheet.write(0, cols, var, bold)
        cols = cols + 1

    for file in os.listdir("./downloads"):
        if file[-4:] == ".apk":
            sheet.write(rows, 0, file[:-4])
            hashvalue = hashlib.md5(open('./downloads/' + file, 'rb').read()).hexdigest()
            sheet.write(rows, 1, hashvalue)
            print('[' + str(count+1) + '][' + file[:-4] + '][' + hashvalue + ']')
            count += 1
            rows += 1


def run_sequence_tests_from_scraping():
    vars = ["#", "Package", "Start Time", "End Time", "Duration"]
    sheet = workbook.add_worksheet("Results - Sequence")
    bold = workbook.add_format({'bold': True})
    # write the header
    cols = 0
    for var in vars:
        sheet.write(0, cols, var, bold)
        cols = cols + 1

    count = 0
    rows = 1

    # print(dir)
    # print(ext_apps)

    for file in os.listdir('./downloads'):
        if file[-4:] == ".apk":
            id_app = file[:-4]
            count = count + 1
            print(pyfiglet.figlet_format(str(count)))
            print("[" + str(count) + "] TESTING APP ===========================>>>>>>>>>> " + id_app)
            sheet.write(rows, 0, count)
            sheet.write(rows, 1, id_app)
            starttime = datetime.datetime.now()
            format2 = workbook.add_format({'num_format': 'dd/mm/yy hh:mm:ss'})
            sheet.write(rows, 2, starttime, format2)
            # all the relevant stuff should happen here
            #######
            print("python3 scanner.py --md5 " + id_app + " --file " + "./downloads/" + file)
            # os.system(config['GENERAL']['python3cmd'] + " scanner.py --md5 " + id_app + " --file " + dir + "/" + file)
            format3 = workbook.add_format({'num_format': 'dd/mm/yy hh:mm:ss'})
            endtime = datetime.datetime.now()
            sheet.write(rows, 3, endtime, format3)
            format4 = workbook.add_format({'num_format': 'mm:ss'})
            sheet.write(rows, 4, "=D" + str(rows + 1) + "-C" + str(rows + 1), format4)
            rows = rows + 1


if __name__ == "__main__":
    run_scrapper()
    # compute file MD5
    # compute_md5()
    # run_sequence_tests_from_scraping()
    workbook.close()
