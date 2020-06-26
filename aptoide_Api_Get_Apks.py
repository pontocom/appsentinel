import requests
import json
import manager


urlApsList = 'http://ws75.aptoide.com/api/7/apps/get/store_name=apps/limit='

APPS_PER_GROUP = 1

#-------- get apks list -------
totalApps = 0

dataResult=[]


with open('aptoideGroups.txt', 'r') as f:
    allGroups = f.readlines()
    for group in allGroups:
        print('antes')
        response = requests.get(urlApsList + str(APPS_PER_GROUP) +'/group_name=' + group)
        content = response.json()
        #print(content)
        try:
            for i in range(0,APPS_PER_GROUP):
                md5 = content['datalist']['list'][i]['file']['md5sum']
                size = content['datalist']['list'][i]['file']['filesize']
                data = manager.get_json_data(md5)
                print(md5)
                if (data['info']['status'] != 'FAIL'):
                    manager.download_apk(data['nodes']['meta']['data']['file']['path'])
                    dataResult.append({
                        'md5': md5,
                        'size': size
                    })
                totalApps+=1
        except:
            print('exception')
            continue
        
with open('dataApk.json', 'w') as f:
    json.dump(dataResult, f)
    
        
       

print('\n' + str(totalApps))





# user 	User id (email)
# passhash 	SHA1 hash of the user password
# repo 	Repository name
# mode 	Return mode/format ('xml' or 'json') 