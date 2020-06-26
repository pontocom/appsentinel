import sys
import requests
import json
import manager
import xlsxwriter
import datetime


urlApsList = 'http://ws75.aptoide.com/api/7/apps/get/sort=downloads/order=DESC/limit='

APPS_PER_GROUP = 1

# -------- get apks list -------
totalApps = 0
grpNumber = 0

dataResult = []

workbook = xlsxwriter.Workbook("./tests/testResults-init-"+str(datetime.datetime.now())+".xlsx")

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
                data = manager.get_json_data(md5)
                print('[' + str(totalApps + 1) + ']['+str(grpNumber+1)+']['+str(i+1)+'][' + md5 + '][' + name + '][' + package + ']')
                if data['info']['status'] != 'FAIL':
                    manager.download_apk(data['nodes']['meta']['data']['file']['path'])
                    dataResult.append({
                        'md5': md5,
                        'size': size
                    })
                totalApps += 1
                rows += 1
        except:
            print('exception')
            continue
        grpNumber +=1

with open('dataApk.json', 'w') as f:
    json.dump(dataResult, f)

print('\nTOTAL APPS DOWNLOADED = ' + str(totalApps))

workbook.close()
