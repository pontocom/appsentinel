from pymongo import MongoClient
import datetime
import logging as log
import configparser



config = configparser.ConfigParser()
config.read('config.ini')

log.basicConfig(filename=config['GENERAL']['logDir'] + "appsentinel.log", filemode='a', format='%(asctime)s,%(msecs)d | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s', datefmt='%H:%M:%S', level=log.DEBUG)

def insert_results(md5, tool, results, status):
    client = MongoClient('localhost',27017)
    db = client['apkscanner']
    apkresults = db.apkresults
    # todo logs
    try:
        data = {
            'md5': md5,
            'tool': tool,
            'results': results,
            'status': status,
            'created_at': datetime.datetime.today()
        }

        apkresults.insert_one(data)
        client.close()
        
    except:
        print("AN ERROR OCCURED WHILE INSERTING DATA")
        log.debug("AN ERROR OCCURED WHILE INSERTING DATA " + data)

def insert_temporary_results_by_tool(md5, tool, results):
    client = MongoClient('localhost',27017)
    db = client['apkscanner']
    apkresults = db.apktemporaryresults
    # todo logs
    try:
        data = {
            'md5': md5,
            'tool': tool,
            'results': results,
            'created_at': datetime.datetime.today()
        }

        apkresults.insert_one(data)
        client.close()
    except:
        print("AN ERROR OCCURED WHILE INSERTING DATA")
        log.debug("AN ERROR OCCURED WHILE INSERTING DATA " + data)
    
def delete_temporary_results(md5, tool):
    client = MongoClient('localhost',27017)
    db = client['apkscanner']
    apk2scan = db.apktemporaryresults

    apk2scan.delete_one({
        'md5':md5,
        'tool':tool
    })
    client.close()

def get_temporary_results_by_tool(md5, tool):
    client = MongoClient('localhost',27017)
    db = client['apkscanner']
    apkresults = db.apktemporaryresults
    result = apkresults.find({
        'md5':md5,
        'tool': tool
    })
    client.close()

    return result

def insert_final_results(md5, results, status):
    client = MongoClient('localhost',27017)
    db = client['apkscanner']
    apkfinalresults = db.apkfinalresults
    # todo logs
    try:
        data = {
            'md5': md5,
            'results': results,
            'status': status,
            'created_at': datetime.datetime.today()
        }
        apkfinalresults.insert_one(data)
        client.close()
    except:
        print("AN ERROR OCCURED WHILE INSERTING DATA")
        log.debug("AN ERROR OCCURED WHILE INSERTING DATA " + data)

def insert_results_vulnerabilitylevel(md5, results, status):
    client = MongoClient('localhost',27017)
    db = client['apkscanner']
    apkvulnerabilitylevel = db.apkvulnerabilitylevel
    # todo logs
    try:
        data = {
            'md5': md5,
            'results': results,
            'status': status,
            'created_at': datetime.datetime.today()
        }
        apkvulnerabilitylevel.insert_one(data)
        client.close()
    except:
        print("AN ERROR OCCURED WHILE INSERTING DATA")
        log.debug("AN ERROR OCCURED WHILE INSERTING DATA " + data)

def insert_results_levels(md5, results, status):
    client = MongoClient('localhost',27017)
    db = client['apkscanner']
    apklevels = db.apklevels
    # todo logs
    try:
        data = {
            'md5': md5,
            'results': results,
            'status': status,
            'created_at': datetime.datetime.today()
        }
        apklevels.insert_one(data)
        client.close()
    except:
        print("AN ERROR OCCURED WHILE INSERTING DATA")
        log.debug("AN ERROR OCCURED WHILE INSERTING DATA " + data)

def insert_new_apk2scan(md5):
    client = MongoClient('localhost',27017)
    db = client['apkscanner']
    apk2scan = db.apk2scan
    # todo logs
    try:
        data = {
            'md5': md5,
            'created_at': datetime.datetime.today()
        }
        apk2scan.insert_one(data)
        client.close()
    except:
        print("AN ERROR OCCURED WHILE INSERTING DATA")
        log.debug("AN ERROR OCCURED WHILE INSERTING DATA " + data)

def get_all_apk2scan():
    client = MongoClient('localhost',27017)
    db = client['apkscanner']
    apk2scan = db.apk2scan
    apks = apk2scan.find()
    client.close()

    return apks

def delete_apk2scan(md5):
    client = MongoClient('localhost',27017)
    db = client['apkscanner']
    apk2scan = db.apk2scan

    apk2scan.delete_one({
        'md5':md5
    })
    client.close()

def insert_new_apk(md5, applicationName, applicationPackage, applicationVersion, applicationPath, apkFile):
    client = MongoClient('localhost',27017)
    db = client['apkscanner']
    apk = db.apk

    try:
        data = {
            'md5': md5,
            'applicationName': applicationName,
            'applicationPackage': applicationPackage,
            'applicationVersion': applicationVersion,
            'applicationPath': applicationPath,
            'apkFile': apkFile,
            'status': 1,
            'created_at': datetime.datetime.today(),
            'updated_at': datetime.datetime.today()
        }
        apk.insert_one(data)
        client.close()
    except:
        print("AN ERROR OCCURED WHILE INSERTING DATA")
        log.debug("AN ERROR OCCURED WHILE INSERTING DATA " + data)

def apk_id_exists(md5, collection):
    client = MongoClient('localhost',27017)
    db = client['apkscanner']
    collection = db[collection]

    result = collection.find_one({
        'md5':md5
    })
    client.close()

    if result:
        return True
    else:
        return False

def get_apk_results_by_tool(md5, tool):
    client = MongoClient('localhost',27017)
    db = client['apkscanner']
    apkresults = db.apkresults
    result = apkresults.find({
        'md5':md5,
        'tool': tool
    })
    client.close()

    return result

def count_apks_to_analyze():
    client = MongoClient('localhost',27017)
    db = client['apkscanner']
    n_apks = db.apk2scan.count_documents({})
    client.close()
    return n_apks

def get_apk_status(md5):
    client = MongoClient('localhost',27017)
    db = client['apkscanner']
    apkfinalresults = db.apkfinalresults
    result = apkfinalresults.find({
        'md5': md5
    })
    client.close()

    return result

def get_apk_vuln_level(md5):
    client = MongoClient('localhost',27017)
    db = client['apkscanner']
    apkvulnerabilitylevel = db.apkvulnerabilitylevel
    result = apkvulnerabilitylevel.find({
        'md5': md5
    })
    client.close()

    return result

def get_apk_month_level(id):
    client = MongoClient('localhost',27017)
    db = client['apkscanner']
    apkvulnerabilitylevel = db.apkvulnerabilitylevel
    start = datetime.datetime.now()
    now = datetime.datetime.now()
    if int(id) <= now.month:
        start = datetime.datetime(now.year, (now.month-int(id)), (now.day))
    if int(id) > now.month:
        start = datetime.datetime((now.year - 1), (12 - int(id) + now.month + 1),now.day)

    #result = courses.insert_one(courseStruct)
    result = apkvulnerabilitylevel.find({
        'created_at':{'$gt': start}
    })
    client.close()

    return result

def get_apk_levels(md5):
    client = MongoClient('localhost',27017)
    db = client['apkscanner']
    apklevels = db.apklevels
    result = apklevels.find({
        'md5': md5
    })
    client.close()

    return result

def get_apk_finalresults(md5):
    client = MongoClient('localhost',27017)
    db = client['apkscanner']
    apkfinalresults = db.apkfinalresults
    result = apkfinalresults.find({
        'md5': md5
    })
    client.close()

    return result

def get_all_apk_levels():
    client = MongoClient('localhost',27017)
    db = client['apkscanner']
    apkvulnerabilitylevel = db.apkvulnerabilitylevel
    result = apkvulnerabilitylevel.find()
    client.close()

    return result

def get_rules():
    client = MongoClient('localhost',27017)
    db = client['apkscanner']
    rules = db.apkrules
    try:
        result = rules.find()
        client.close()


        return(result[0])

    except:

         doc = {'_id':1,
               'info': 0,
               'notice': 0,
               'warning': 0,
               'critical': 0,
               'vulnerability_name': 0,
               'videos': 0,
               'link':0,
               'severity_levels': 0,
               'email_template': 'Email'
                }

         rules.insert_one(doc)
         client.close()
         return doc

def insert_rules(info, notice, warning, critical, vulnerability_name, videos, link, severity_levels, email_template):
    client = MongoClient('localhost',27017)
    db = client['apkscanner']
    apkrules = db.apkrules

    try:
        apkrules.update(
            {'_id':{'$eq': 1}},
            {'$set':
                 {'info': info,
                       'notice': notice,
                       'warning': warning,
                       'critical': critical,
                       'vulnerability_name': vulnerability_name,
                       'videos': videos,
                       'link':link,
                       'severity_levels': severity_levels,
                       'email_template': email_template}
             }
        )
        client.close()
    except:
        print("AN ERROR OCCURED WHILE UPDATING DATA -> ")
        log.debug("AN ERROR OCCURED WHILE UPDATING DATA -> ")
        return False

    return True







