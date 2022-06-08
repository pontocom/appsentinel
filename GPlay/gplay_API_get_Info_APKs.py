#!/usr/bin/python3
import sys
import requests
import json
import os
# import manager
import xlsxwriter
import datetime
import hashlib

baseAPIURL = 'https://api.apptweak.com/android/categories/'
APIKEY = 'zj3KJJShkBsvomVrxv8T16hD2IQ'

baseAPIURL2 = 'https://api.appmonsta.com/v1/stores/android/details/'
APIKEY2 = 'ea67957f7f28f0b01183c872412c1d649ce94046'

APPS_PER_GROUP = 10

totalApps = 0
grpNumber = 0

dataResult = []

workbook = xlsxwriter.Workbook("./tests/testResults-GPlay-init-" + str(datetime.datetime.now()) + ".xlsx")

count = 0


def get_top_apks():
    grpNumber = 0
    vars = ["#", "Name", "Package", "Category"]
    sheet = workbook.add_worksheet("Results")
    bold = workbook.add_format({'bold': True})
    # write the header
    cols = 0
    for var in vars:
        sheet.write(0, cols, var, bold)
        cols = cols + 1

    # Run all the categories and download top apps as JSON format
    with open('./gplay_categories.txt', 'r') as f:
        allGroups = f.readlines()
        for group in allGroups:
            print('[' + str(grpNumber + 1) + '][' + group.rstrip('\r\n').upper() + ']')
            print('Requesting [' + baseAPIURL + group.rstrip('\r\n') + '/top.json?country=pt&language=en&type=free]')
            response = requests.get(baseAPIURL + group.rstrip('\r\n') + '/top.json?country=pt&language=en&type=free',
                                    headers={"X-Apptweak-Key": APIKEY})
            content = response.json()
            print('./tops/' + group.rstrip('\r\n') + '.json')
            with open('./tops/' + group.rstrip('\r\n') + '.json', 'w') as s:
                json.dump(content, s)
            grpNumber += 1


# Run through all the JSON files and process the results
def download_apks():
    rows = 1
    for file in os.listdir("./tops"):
        if file[-5:] == ".json":
            print("CATEGORY NAME = " + file[:-5])
            with open('./tops/' + file, 'r') as f:
                content = json.load(f)
                for i in range(0, APPS_PER_GROUP):
                    name = content['content'][i]['title']
                    package = content['content'][i]['id']
                    category = file[:-5]
                    sheet.write(rows, 0, count + 1)
                    sheet.write(rows, 1, name)
                    sheet.write(rows, 2, package)
                    sheet.write(rows, 3, category)
                    print('[' + str(count + 1) + '][' + category + '][' + package + ']')
                    print('EXECUTING: gplaycli -d ' + package + ' -f ./downloads')
                    os.system('gplaycli -d ' + package + ' -f ./downloads')
                    rows += 1
                    count += 1


# Run get detailed information for APKs
def get_apk_info():
    count = 0
    rows = 1
    vars = ["Package", "Downloads", "Version", "Release Date"]
    sheet = workbook.add_worksheet("APK Details")
    bold = workbook.add_format({'bold': True})
    # write the header
    cols = 0
    for var in vars:
        sheet.write(0, cols, var, bold)
        cols = cols + 1

    for file in os.listdir("../download-GPlay"):
        if file[-4:] == ".apk":
            print('[' + str(count + 1) + '][' + file[:-4] + '] Requesting [' + baseAPIURL2 + file[:-4] + ".json")
            if count >= 200:  # just to overcome the API limitations
                response = requests.get(baseAPIURL2 + file[:-4] + ".json",
                                        auth=(APIKEY2, "X"),
                                        params={"country": "US"},
                                        headers={'Accept-Encoding': 'deflate, gzip'},
                                        stream=True)
                content = response.json()
                print(response)
                if response.status_code == 200:
                    sheet.write(rows, 0, file[:-4])
                    sheet.write(rows, 1, content['downloads'])
                    sheet.write(rows, 2, content['version'])
                    sheet.write(rows, 3, content['release_date'])
                    print('[' + str(count + 1) + '][' + file[:-4] + '][' + content['downloads'] + '][' + content[
                        'version'] + '][' + content[
                              'release_date'] + ']')
                    count += 1
                    rows += 1
                else:
                    print(content)
                    count += 1
                    continue
            else:
                count += 1
                continue


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


if __name__ == "__main__":
    get_top_apks()
    # download_apks()
    # get_apk_info()
    # compute_md5()
    workbook.close()

# curl -u "ea67957f7f28f0b01183c872412c1d649ce94046:X" "https://api.appmonsta.com/v1/stores/android/details/com.facebook.orca.json?country=PT"
