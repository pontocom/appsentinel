from flask import (jsonify, Blueprint, request)
# import databaseConnection as db
import uuid
import datetime
import configparser
import bcrypt
import hashlib
import jwt

vscanner_api = Blueprint('vscanner_api', __name__)


@vscanner_api.route('/apkscan', methods=['POST'])
def apkscan():
    data = request.values

    # check if an MD5 has been passed
    if "md5" not in data:
        return jsonify({'status': False, 'message': 'Hey...! Where is my MD5???'}), 400
    else:
        # 1. start by downloading the APK from Aptoide
        # 2. register some information on the database
        # 3. start running the scanner -> check vulnScanManager.py
        # 4. when it ends... well, update the database (in particular, saying that is has completed the task!!!)
        return jsonify({'status': True, 'message': 'APK was passed to the scanning engine... please hold on!'}), 201


@vscanner_api.route('/apkfeedback/<id>', methods=['GET'])
def apkfeedback(id):
    return jsonify({'status': False, 'message': 'APK work was not finished... please come back l8r!'})

