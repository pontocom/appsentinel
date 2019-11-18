import os
import requests
from urllib.parse import urlparse

from tqdm import tqdm
import math
import json
import configparser
import logging as log
import owasp_engine as oe
import databaseMG as dbMG

config = configparser.ConfigParser()
config.read('config.ini')

log.basicConfig(filename=config['GENERAL']['logDir'] + "appsentinel.log", filemode='a', format='%(asctime)s,%(msecs)d | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s', datefmt='%H:%M:%S', level=log.DEBUG)


aptoide_API_endpoint = config['DOWNLOAD']['aptoideAPIEndpoint']
dir = config['DOWNLOAD']['apkDownloadDir']
json_dir = config['DOWNLOAD']['jsonDir']


def download_apk(which_apk):
    # check if the download dir exists or not
    if not os.path.exists(dir):
        os.system("mkdir " + dir)

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


def get_json_data(which_apk):
    response = requests.get(aptoide_API_endpoint + which_apk)
    jsondata = response.json()
    return jsondata


def write_json_data(jsondata, whick_apk):
    # check if the json dir exists or not
    if not os.path.exists(json_dir):
        os.system("mkdir " + json_dir)

    filename = json_dir + "/" + whick_apk + ".json"
    with open(filename, 'w') as f:
        f.write(json.dumps(jsondata))
    f.close()
    return True


if __name__=="__main__":
    VERSION = '0.1'
    banner = "APK Downloader"
    print(str(banner))

    log.debug("------------------------")
    log.debug("APPSENTINEL MANAGER HAS BEEN INVOKED!!!!")

    # 1. Go to the database and check if there are APKs to download
    #apks = db.get_all_apk2scan()
    n_apks = dbMG.count_apks_to_analyze()
    # 2. For each APK on the database, download it locally, add to the apk table and delete from the table
    if n_apks > 0:
        apks = dbMG.get_all_apk2scan()
        for apk in apks:
            print(apk['md5'])
            jsondata = get_json_data(apk['md5'])
            # check what is the return of the API call -> check if the APK exists!!!
            if jsondata["info"]["status"] == "FAIL":
                # that APK can't be found
                log.debug("This APK doesn't exist on APTOIDE -> APK = " + apk[1])
                #db.delete_apk2scan(apk[1])
                print(apk[1])
                dbMG.delete_apk2scan(apk['md5'])
                #db.insert_results(apk[1], "", "", -1, "This APK does not exist, or it could not be downloaded from the Aptoide app store!")
                dbMG.insert_results(apk[-1],"",{},-1)

            else:
                applicationName = jsondata["nodes"]["meta"]["data"]["name"]
                applicationPackage = jsondata["nodes"]["meta"]["data"]["package"]
                appVersion = jsondata["nodes"]["meta"]["data"]["file"]["vername"]
                appMD5 = jsondata["nodes"]["meta"]["data"]["file"]["md5sum"]
                appPath = jsondata["nodes"]["meta"]["data"]["file"]["path"]
                apkfile = appPath[appPath.rfind("/") + 1:]
                print("Getting the following APK => " + applicationName)
                log.debug("Getting the following APK => " + applicationName)
                print(applicationPackage + " (" + appVersion + ") -> " + appMD5)
                log.debug(applicationPackage + " (" + appVersion + ") -> " + appMD5)
                print(appPath)
                log.debug(appPath)
                download_apk(appPath)
                write_json_data(jsondata, apk['md5'])
                #db.insert_new_apk(apk['md5'], applicationName, applicationPackage, appVersion, appPath, apkfile)
                log.debug(config['GENERAL']['python3cmd'] + " scanner.py --md5 " + appMD5 + " --file " + dir + "/" + apkfile)
                os.system(config['GENERAL']['python3cmd'] + " scanner.py --md5 " + appMD5 + " --file " + dir + "/" + apkfile)
                dbMG.insert_new_apk(apk['md5'], applicationName, applicationPackage, appVersion, appPath, apkfile)
                dbMG.delete_apk2scan(apk['md5'])
                oe.startEngine(appMD5)
    else:
        print("No apks yet... waiting patiently!!!")
        log.debug("No apks yet... waiting patiently!!!")
