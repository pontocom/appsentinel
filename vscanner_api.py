from flask import (jsonify, Blueprint, request)
import database as db
import json
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

vscanner_api = Blueprint('vscanner_api', __name__)


@vscanner_api.route('/apkscan', methods=['POST'])
def apkscan():
    data = request.values
    # check if an MD5 has been passed
    if "md5" not in data:
        return jsonify({'status': False, 'message': 'Hey...! Where is my MD5???'}), 201
    else:
        md5Apk = data["md5"]
        # 1. add the apk to scan to the database
        db.insert_new_apk2scan(md5Apk)
        return jsonify({'status': True, 'message': 'APK was passed to the scanning engine... please hold on!'}), 201


@vscanner_api.route('/apkfeedback/<id>', methods=['GET'])
def apkfeedback(id):
    if not id:
        jsonify({'status': False, 'message': 'No MD5 APK id was passed'}), 400
    else:
        results_data = db.get_apk_status(id)
        if results_data:
            print(results_data[0]['results_location'])
            file = open(results_data[0]['results_location'])
            json_data = json.load(file);
            return jsonify({'status': True, 'results_history': results_data, 'results': json_data}), 201
        else:
            return jsonify({'status': False, 'message': 'APK work was not finished... please come back l8r!'}), 400


