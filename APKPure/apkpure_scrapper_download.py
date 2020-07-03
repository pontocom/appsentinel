import requests
import xlsxwriter
import os
import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from tqdm import tqdm
import math

baseURL = 'https://apkpure.com'
APPS_PER_GROUP = 10

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
    with open('./apkpure_categories.txt', 'r') as f:
        allGroups = f.readlines()
        for group in allGroups:
            print('[' + str(grpNumber + 1) + '][' + group.rstrip('\r\n').upper() + ']')

            # run the scrapper for this category
            print('Getting...: ' + baseURL + '/' + group.rstrip('\r\n'))
            response = requests.get(baseURL + '/' + group.rstrip('\r\n'))
            html = BeautifulSoup(response.text, 'html.parser')

            apps = html.find_all(class_="category-template-img")
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
                    appresponse = requests.get(baseURL + app_location)
                    html2 = BeautifulSoup(appresponse.text, 'html.parser')
                    download_link = html2.find(class_="ny-down").find("a")['href']
                    print('Getting...: ' + baseURL + download_link)
                    response = requests.get(baseURL + download_link)
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


if __name__ == "__main__":
    run_scrapper()
    workbook.close()
