#!/usr/bin/python3
import sys
import requests
import json
import xlsxwriter
import datetime
import configparser
from urllib.parse import urlparse
from tqdm import tqdm
import math
import os

config = configparser.ConfigParser()
config.read('../config.ini')
aptoide_API_endpoint = config['DOWNLOAD']['aptoideAPIEndpoint']
dir = "./downloads"

urlApsList = 'http://ws75.aptoide.com/api/7/apps/get/sort=downloads/order=DESC/limit='

APPS_PER_GROUP = 1

# -------- get apks list -------
totalApps = 0
grpNumber = 0

dataResult = []

workbook = xlsxwriter.Workbook("./tests/testResults-init-" + str(datetime.datetime.now()) + ".xlsx")


def check_and_create_dirs():
    # check if the download dir exists or not
    if not os.path.exists('./downloads'):
        os.system("mkdir " + dir)
        os.system("chmod 775 " + dir)

    # check if the download dir exists or not
    if not os.path.exists('./tests'):
        os.system("mkdir " + './tests')
        os.system("chmod 775 " + './tests')


def get_json_data(which_apk):
    response = requests.get(aptoide_API_endpoint + which_apk)
    jsondata = response.json()
    return jsondata


def download_apk(which_apk):
    # write the file to the filesystem
    a = urlparse(which_apk)
    filename = dir + "/" + os.path.basename(a.path)

    # Streaming, so we can iterate over the response.
    r = requests.get(which_apk, stream=True)

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


if __name__ == "__main__":
    check_and_create_dirs()

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

    with open('aptoideGroups.txt', 'r') as f:
        allGroups = f.readlines()
        for group in allGroups:
            print('[' + str(grpNumber + 1) + '][' + group.rstrip('\r\n').upper() + ']')
            print('Requesting [' + urlApsList + str(APPS_PER_GROUP) + '/group_name=' + group.rstrip('\r\n') + ']')
            response = requests.get(urlApsList + str(APPS_PER_GROUP) + '/group_name=' + group.rstrip('\r\n'))
            content = response.json()
            try:
                for i in range(0, APPS_PER_GROUP):
                    sheet.write(rows, 0, totalApps + 1)
                    name = content['datalist']['list'][i]['name']
                    package = content['datalist']['list'][i]['package']
                    md5 = content['datalist']['list'][i]['file']['md5sum']
                    size = content['datalist']['list'][i]['file']['filesize']
                    sheet.write(rows, 1, content['datalist']['list'][i]['file']['md5sum'])
                    sheet.write(rows, 2, content['datalist']['list'][i]['name'])
                    sheet.write(rows, 3, content['datalist']['list'][i]['package'])
                    sheet.write(rows, 4, group.rstrip('\r\n').upper())
                    sheet.write(rows, 5, content['datalist']['list'][i]['stats']['downloads'])
                    sheet.write(rows, 6, content['datalist']['list'][i]['file']['filesize'])
                    sheet.write(rows, 7, content['datalist']['list'][i]['file']['vername'])
                    sheet.write(rows, 8, content['datalist']['list'][i]['file']['vercode'])
                    data = get_json_data(md5)
                    print('[' + str(totalApps + 1) + '][' + str(grpNumber + 1) + '][' + str(
                        i + 1) + '][' + md5 + '][' + name + '][' + package + ']')
                    if data['info']['status'] != 'FAIL':
                        download_apk(data['nodes']['meta']['data']['file']['path'])
                        dataResult.append({
                            'md5': md5,
                            'size': size
                        })
                    totalApps += 1
                    rows += 1
            except:
                print('exception')
                continue
            grpNumber += 1

    with open('dataApk.json', 'w') as f:
        json.dump(dataResult, f)

    print('\nTOTAL APPS DOWNLOADED = ' + str(totalApps))

    workbook.close()
