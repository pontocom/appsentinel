from flask import (jsonify, Blueprint, request)
import manager as dnl
import database as db
import scanner as scan
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

vscanner_api = Blueprint('vscanner_api', __name__)


@vscanner_api.route('/apkscan', methods=['POST'])
def apkscan():
    data = request.values

    # check if an MD5 has been passed
    if "md5" not in data:
        return jsonify({'status': False, 'message': 'Hey...! Where is my MD5???'}), 400
    else:
        md5Apk = data["md5"]
        # 1. add the new APK md5 to the list of APKs to scan
        db.insert_new_apk2scan(md5Apk)

        jsondata = dnl.get_apk_info(md5Apk)
        if not jsondata:
            return jsonify({'status': False, 'message': 'There is no information about that APK!'}), 201

        applicationName = jsondata["nodes"]["meta"]["data"]["name"]
        applicationPackage = jsondata["nodes"]["meta"]["data"]["package"]
        appVersion = jsondata["nodes"]["meta"]["data"]["file"]["vername"]
        appMD5 = jsondata["nodes"]["meta"]["data"]["file"]["md5sum"]
        appPath = jsondata["nodes"]["meta"]["data"]["file"]["path"]

        apkfile = appPath[appPath.rfind("/")+1:]

        print("Getting the following APK => " + applicationName)
        print("Package = " + applicationPackage + " (" + appVersion + ") -> " + appMD5)
        print("Application package = " + appPath)
        print("APK file = " + apkfile)

        dnl.download_apk(appPath)

        # 2. register some information on the database
        db.insert_new_apk(md5Apk, applicationName, applicationPackage, appVersion, appPath, apkfile)

        # 3. start running the scanner -> check vulnScanManager.py
        scan.scan_apk(apkfile)

        # 4. when it ends... well, update the database (in particular, saying that is has completed the task!!!)
        return jsonify({'status': True, 'message': 'APK was passed to the scanning engine... please hold on!'}), 201


@vscanner_api.route('/apkfeedback/<id>', methods=['GET'])
def apkfeedback(id):
    return jsonify({'status': False, 'message': 'APK work was not finished... please come back l8r!'})

