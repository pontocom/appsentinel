from flask import (
    Flask,
    jsonify,
    request
)
import database as db
from flasgger import Swagger
from flasgger.utils import swag_from
import json
import logging as log
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

template = {
  "swagger": "2.0",
  "info": {
    "title": "APK scanner API",
    "description": "An API that scans APKs looking for security vulnerabilities",
    "contact": {
      "responsibleOrganization": "ISCTE - Instituto Universitário de Lisboa",
      "responsibleDeveloper": "Carlos Serrão",
      "email": "carlos.serrao@iscte-iul.pt",
      "url": "istar.iscte-iul.pt",
    },
    "termsOfService": "http://me.com/terms",
    "version": "0.0.1"
  },
  "host": "127.0.0.1:5000",  # overrides localhost:500
  "basePath": "/",  # base bash for blueprint registration
  "schemes": [
    "http",
    "https"
  ],
  "operationId": "getmyData"
}

# Create the application instance
app = Flask(__name__, template_folder="templates")
Swagger(app, template=template)

log.basicConfig(filename=config['GENERAL']['logDir'] + "appsentinel.log", filemode='a', format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S', level=log.DEBUG)

# Create a URL route in our application for "/"
# This is purely to see if the server is running, there is currently no website planned
@app.route('/')
def home():
    return jsonify({'status': True, 'message': 'API is responding... keep trying!'}), 200


@app.route('/apkscan', methods=['POST'])
@swag_from('./docs/apkscan.yml')
def apkscan():
    log.debug("APKSCAN REQUEST RECEIVED")
    data = request.values
    # check if an MD5 has been passed
    if "md5" not in data:
        return jsonify({'status': False, 'message': 'Hey...! Where is my MD5???'}), 200
    else:
        md5Apk = data["md5"]
        log.debug("APK MD5 = " + md5Apk)
        # 1. add the apk to scan to the database
        if db.apk_id_exists(md5Apk, 'apkresults'):
            return jsonify({'status': False,
                            'message': 'That APK was previously processed and exists on the results database. Please check the results using the appropriate API call!'}), 200
        else:
            if db.apk_id_exists(md5Apk, 'apk2scan'):
                return jsonify({'status': False, 'message': 'That APK is already in the pipeline to be processed... wait for the results!'}), 200
            else:
                db.insert_new_apk2scan(md5Apk)
                return jsonify({'status': True, 'message': 'APK was passed to the scanning engine... please hold on!'}), 200


@app.route('/apkfeedback/<id>', methods=['GET'])
@swag_from('./docs/apkfeedback.yml')
def apkfeedback(id):
    log.debug("APKSCAN REQUEST RECEIVED")
    log.debug("APK MD5 = " + id)
    if not id:
        jsonify({'status': False, 'message': 'No MD5 APK id was passed'}), 500
    else:
        results_data = db.get_apk_status(id)
        if results_data:
            print(results_data[0]['results_location'])
            file = open(results_data[0]['results_location'])
            json_data = json.load(file)
            return jsonify({'status': True, 'results_history': results_data, 'results': json_data}), 200
        else:
            return jsonify({'status': False, 'message': 'APK work was not finished... please come back l8r!'}), 500


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True )
