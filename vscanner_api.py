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
    return jsonify({'status': True, 'message': 'APK was passed to the scanning engine... please hold on!'})


@vscanner_api.route('/apkfeedback/<id>', methods=['GET'])
def apkfeedback(id):
    return jsonify({'status': False, 'message': 'APK work was not finished... please come back l8r!'})

