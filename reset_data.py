import pymysql
import configparser
import logging as log
import json
import datetime
import os
import logging
import database as db

config = configparser.ConfigParser()
config.read('config.ini')

appsentinel = config['GENERAL']['appsentinel']

locations = [
    #config['DOWNLOAD']['apkDownloadDir'],
    #config['DOWNLOAD']['jsonDir'], 
    config['DROIDSTATX']['dstatx_out_txt'], 
    config['DROIDSTATX']['dstatx_out_xmind'], 
    config['OWASP_OUTPUT']['feedbackResultsLocation'], 
    config['OWASP_OUTPUT']['feedback_levelsResultsLocation'],
    config['OWASP_OUTPUT']['feedback_vuln_levelsResultsLocation'],
    config['SCANNER']['json_results_androbugs'],
    config['SCANNER']['json_results_droidstatx'],
    config['DROIDSTATX']['dstatx_out_apktool'],
    config['SCANNER']['json_results_super']
    ]

# First delete files in file system
print(os.system("pwd"))
for location in locations:
    try:
        if location:
            print('Location: ' + location + ' ' + str(len(location)))
            if len(location) > 0:
                os.chdir(location)
                if location == config['DROIDSTATX']['dstatx_out_apktool']:
                    os.system("rm -R -- */")
                else:
                    os.system("rm *")
                print("Deleted files in: " + location)
                print("... \n")
                os.chdir(appsentinel)
            else:
                print('Directory is alredy empty \n')
    except:
        print('ERROR ON DIRECTORY -> ' + location)
        logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

# Delete all entries in all tables
tables = [
    'apk',
    'apk2scan',
    'apkfinalresults',
    'apklevels',
    'apkresults',
    'apkrules',
    'apkscantools',
    'apkvulnerabilitylevel'
]
db.reset_database(tables)

