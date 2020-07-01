import sys
import requests
import json
import os
# import manager
import xlsxwriter
import datetime

baseAPIURL = 'https://api.apptweak.com/android/categories/'
APIKEY = 'zj3KJJShkBsvomVrxv8T16hD2IQ'

APPS_PER_GROUP = 10

totalApps = 0
grpNumber = 0

dataResult = []

workbook = xlsxwriter.Workbook("./tests/testResults-GPlay-init-" + str(datetime.datetime.now()) + ".xlsx")

vars = ["#", "Name", "Package", "Category"]
sheet = workbook.add_worksheet("Results")
bold = workbook.add_format({'bold': True})
# write the header
cols = 0
for var in vars:
    sheet.write(0, cols, var, bold)
    cols = cols + 1

count = 0
rows = 1

# Run all the categories and download top apps as JSON format
# with open('./gplay_categories.txt', 'r') as f:
#    allGroups = f.readlines()
#    for group in allGroups:
#        print('[' + str(grpNumber + 1) + '][' + group.rstrip('\r\n').upper() + ']')
#        print('Requesting [' + baseAPIURL + group.rstrip('\r\n') + '/top.json?country=us&language=us&type=free]')
#        response = requests.get(baseAPIURL + group.rstrip('\r\n') + '/top.json?country=us&language=us&type=free', headers={"X-Apptweak-Key": APIKEY})
#        content = response.json()
#        print('./tops/' + group.rstrip('\r\n') + '.json')
#        with open('./tops/' + group.rstrip('\r\n') + '.json', 'w') as s:
#            json.dump(content, s)
#        grpNumber += 1


# Run through all the JSON files and process the results
for file in os.listdir("./tops"):
    if file[-5:] == ".json":
        print("CATEGORY NAME = " + file[:-5])
        with open('./tops/' + file, 'r') as f:
            # data = f.read()
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

workbook.close()
