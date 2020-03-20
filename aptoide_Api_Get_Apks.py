import requests
import json
import manager


urlApsList = 'http://ws75.aptoide.com/api/7/apps/get/store_name=apps/limit='



#-------- get apks list -------
totalApps = 0

with open('aptoideGroups.txt', 'r') as f:
    allGroups = f.readlines()
    for group in allGroups:
        limitAppsPerGroup = 1
        response = requests.get(urlApsList + str(limitAppsPerGroup) +'/group_name=' + group)
        content = response.json()
        try:
            for i in range(0,limitAppsPerGroup):
                md5 = content['datalist']['list'][i]['file']['md5sum']
                data = manager.get_json_data(md5)
                print(md5)
                if (data['info']['status'] != 'FAIL'):
                    manager.download_apk(data['nodes']['meta']['data']['file']['path'])
                
                totalApps+=1
        except:
            continue
        
        
        
       

print('\n' + str(totalApps))





# user 	User id (email)
# passhash 	SHA1 hash of the user password
# repo 	Repository name
# mode 	Return mode/format ('xml' or 'json') 