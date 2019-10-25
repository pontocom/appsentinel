from flask import (
    Flask,
    jsonify,
    request,
    Response
)
import database as db
from flasgger import Swagger
from flasgger.utils import swag_from
import json
import logging as log
import configparser
import datetime
import time

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

log.basicConfig(filename=config['GENERAL']['logDir'] + "appsentinel.log", filemode='a', format='%(asctime)s,%(msecs)d | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s', datefmt='%H:%M:%S', level=log.DEBUG)

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
        return jsonify({'status': False, 'message': 'Hey...! Where is my MD5???'}), 200, {'Access-Control-Allow-Origin':'*'}
    else:
        md5Apk = data["md5"]
        log.debug("APK MD5 = " + md5Apk)
        # 1. add the apk to scan to the database
        if db.apk_id_exists(md5Apk, 'apkresults'):
            return jsonify({'status': False,
                            'message': 'That APK was previously processed and exists on the results database. Please check the results using the appropriate API call!'}), 200, {'Access-Control-Allow-Origin':'*'}
        else:
            if db.apk_id_exists(md5Apk, 'apk2scan'):
                return jsonify({'status': False, 'message': 'That APK is already in the pipeline to be processed... wait for the results!'}), 200, {'Access-Control-Allow-Origin':'*'}
            else:
                db.insert_new_apk2scan(md5Apk)

                return jsonify({'status': True, 'message': 'APK was passed to the scanning engine... please hold on!'}), 200, {'Access-Control-Allow-Origin':'*'}


@app.route('/apkfeedback/<id>', methods=['GET'])
@swag_from('./docs/apkfeedback.yml')
def apkfeedback(id):
    log.debug("APKSCAN REQUEST RECEIVED")
    log.debug("APK MD5 = " + id)
    if not id:
        return jsonify({'status': False, 'message': 'No MD5 APK id was passed'}), 500, {'Access-Control-Allow-Origin':'*'}
    else:
        results_data = db.get_apk_status(id)
        if results_data:
            # we need to check the status...
            if results_data[0]['status'] != -1:
                print(results_data[0]['results_location'])
                file = open(results_data[0]['results_location'])
                json_data = json.load(file)

                # OWASP_category=['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9', 'M10']
                # data = {}
                # for m_level in OWASP_category:
                #     data = data + {m_level : json_data[m_level]}

                data = {'status': 'OK', 
                'M1': json_data['M1'], 
                'M2': json_data['M2'],
                'M3': json_data['M3'],
                'M4': json_data['M4'],
                'M5': json_data['M5'],
                'M6': json_data['M6'],
                'M7': json_data['M7'],
                'M8': json_data['M8'],
                'M9': json_data['M9'],
                'M10': json_data['M10']}

                return jsonify(data), 200, {'Access-Control-Allow-Origin':'*'}
            else:
                return jsonify({'status': False, 'message': results_data[0]['details']}), 500, {'Access-Control-Allow-Origin':'*'}
        else:
            return jsonify({'status': False, 'message': 'APK work was not finished... please come back l8r!'}), 500, {'Access-Control-Allow-Origin':'*'}


@app.route('/vulnerabilities/<id>', methods=['GET'])
@swag_from('./docs/vulnerabilities.yml')
def apkvullevel(id):
    log.debug("REQUEST TO GET VULNERABILITIES LEVEL")
    log.debug("APK MD5 = " + id)
    if not id:
        return jsonify({'status': False, 'message': 'No MD5 APK id was passed'}), 500, {'Access-Control-Allow-Origin':'*'}
    else:
        results_data = db.get_apk_vuln_level(id)
        if results_data:
            # we need to check the status...
            if results_data[0]['status'] != -1:
                print(results_data[0]['results_location'])
                file = open(results_data[0]['results_location'])
                json_data = json.load(file)
                data = {'status': 'OK', 'vulnerabilities': json_data['vulnerabilities']}
                return jsonify(data), 200, {'Access-Control-Allow-Origin':'*'}
            else:
                return jsonify({'status': False, 'message': results_data[0]['details']}), 500, {'Access-Control-Allow-Origin':'*'}
        else:
            return jsonify({'status': False, 'message': 'APK work was not finished... please come back l8r!'}), 500, {'Access-Control-Allow-Origin':'*'}



@app.route('/vulnerabilities', methods=['GET'])
@swag_from('./docs/apkmonthlevels.yml')
def apkmonthlevels():
    log.debug("REQUEST TO GET VULNERABILITIES LEVEL BY MONTH")
    info=0
    notice=0
    warning=0
    critical=0
    data={}
    data_month={}
    lista=[]
    month_list={}
    

    id = request.args.get('sort')
    if int(id) not in range(3, 13):
        return jsonify({'status': False, 'message': 'sort value must be between 3 and 12'}), 500, {'Access-Control-Allow-Origin':'*'}
    
    else:

        now = datetime.datetime.now()
        for number in range(0,int(id)):
            month = datetime.date(now.year,abs(now.month-number),now.day).strftime('%B')
            lista.append(month)
            month_list[month]=False
            #print(month_list)
        

        results_data = db.get_apk_month_level(id)
        if results_data:
            for x in results_data:
                month = time.strftime('%B', time.struct_time((0,x['created_at'].month,0,)+(0,)*6))
                print(month)
                file = open(x['results_location'])
                json_data = json.load(file)
                month_list[month]=True
                #print(month)
                print(lista)
                try:
                    lista.remove(month)
                except:
                    pass
                for p in json_data['vulnerabilities']:
                    if 'Info' in p['severity']:
                        info += 1
                    if 'Notice' in p['severity']:
                        notice += 1
                    if 'Warning' in p['severity']:
                        warning += 1
                    if 'Critical' in p['severity']:
                        critical += 1

                data_month[month] = []
                data_month[month] = ({
                    'Info': info,
                    'Notice': notice,
                    'Warning': warning,
                    'Critical': critical
                })

                data_month['info'] = []
                data_month['info'].append({
                    'month': month,
                    'values': [
                        {'Info': info},
                        {'Notice': notice},
                        {'Warning': warning},
                        {'Critical': critical}]
                })

                data = {'status': 'OK', 'info': data_month['info']}

            #json_data = json.dumps(data)
            for empty_values in lista:
                data_month['info'].append({
                    'month': empty_values,
                    'values': [
                        {'Info': 0},
                        {'Notice': 0},
                        {'Warning': 0},
                        {'Critical': 0}]
                })
            print(month_list)
            return jsonify(data), 200, {'Access-Control-Allow-Origin':'*'}
        else:
            return jsonify({'status': False, 'message': 'Error'}), 500, {'Access-Control-Allow-Origin':'*'}


@app.route('/vulnerabilities/levels/<id>', methods=['GET'])
@swag_from('./docs/apklevels.yml')
def apklevels(id):

    log.debug("APK MD5 = " + id)
    if not id:
        return jsonify({'status': False, 'message': 'No MD5 APK id was passed'}), 500, {'Access-Control-Allow-Origin':'*'}
    else:
        results_data = db.get_apk_levels(id)
        if results_data:
            # we need to check the status...
            if results_data[0]['status'] != -1:
                print(results_data[0]['results_location'])
                file = open(results_data[0]['results_location'])
                json_data = json.load(file)
                data={'status':'OK', 'value': 0.5}
                return jsonify(data), 200, {'Access-Control-Allow-Origin':'*'}
            else:
                return jsonify({'status': False, 'message': results_data[0]['details']}), 500, {'Access-Control-Allow-Origin':'*'}
        else:
            return jsonify({'status': False, 'message': 'APK work was not finished... please come back l8r!'}), 500, {'Access-Control-Allow-Origin':'*'}


@app.route('/vulnerabilities/levels', methods=['GET'])
@swag_from('./docs/allapksvulnlevels.yml')
def allapksvulnlevels():
    log.debug("REQUEST TO GET APKS LIST INFORMATION")
    info=0
    notice=0
    warning=0
    critical=0
    data={}
    data_list={}
    data_list['list'] = []

    results_data = db.get_all_apk_levels()

    if results_data:
        for x in results_data:
            file = open(x['results_location'])
            json_data = json.load(file)

            for p in json_data['vulnerabilities']:
                if 'Info' in p['severity']:
                    info += 1
                if 'Notice' in p['severity']:
                    notice += 1
                if 'Warning' in p['severity']:
                    warning += 1
                if 'Critical' in p['severity']:
                    critical += 1

            # to do download and rating

        data_list['list'] = [{
            'level': 'Info',
            'value': info},
            {'level': 'Notice',
            'value': notice},
            {'level': 'Warinig',
            'value': warning},
            {'level': 'Critical',
            'value': critical}]

        data = {'status': 'OK', 'list': data_list['list']}

        #json_data = json.dumps(data)
        return jsonify(data), 200, {'Access-Control-Allow-Origin':'*'}
    else:
        return jsonify({'status': False, 'message': 'Error'}), 500, {'Access-Control-Allow-Origin':'*'}

@app.route('/vulnerabilities/apks/list/', methods=['GET'])
@swag_from('./docs/apkslist.yml')
def apkslist():
    log.debug("REQUEST TO GET APKS LIST INFORMATION")
    info = 0
    notice = 0
    warning = 0
    critical = 0
    data_list = {}
    data_list['apkslistinfo'] = []
    data = {}

    results_data = db.get_all_apk_levels()

    if results_data:
        for x in results_data:
            file = open(x['results_location'])
            print("File to open: " + x['results_location'])
            json_data = json.load(file)
            print("JSON data: " + str(json_data))

            for p in json_data['vulnerabilities']:
                if 'Notice' in p['severity']:
                    notice += 1
                if 'Warning' in p['severity']:
                    warning += 1
                if 'Critical' in p['severity']:
                    critical += 1

            # to do download and rating
            #'status': x['status'],

            data_list['apkslistinfo'].append({
                'apk_md5': x['md5'],
                'vulnerability_levels': [{'Info': info},
                                        {'Notice': notice},
                                        {'Warning': warning},
                                        {'Critical': critical}],
                'download': '23456',
                'rating': '5'
            })

        data = {'status': 'OK', 'list': data_list['apkslistinfo']}
        return jsonify(data), 200, {'Access-Control-Allow-Origin':'*'}
    else:
        return jsonify({'status': False, 'message': 'Error'}), 500, {'Access-Control-Allow-Origin':'*'}


@app.route('/feedback/rules/', methods=['GET'])
@swag_from('./docs/getrules.yml')
def getrules():
    log.debug("REQUEST TO GET RULES INFORMATION")
    results_data = db.get_rules()

    data = {}
    data['rules'] = []
    if results_data:
        for row in results_data:
            data['rules'] = ({
                'status': 'OK',
                'vulnerability_levels':[{
                    'info': row['info'],
                    'notice': row['notice'],
                    'warning': row['warning'],
                    'critical': row['critical']
                    }],
                'vulnerability_name': row['vulnerability_name'],
                'videos': row['videos'],
                'links': row['link'],
                'severity_levels': row['severity_levels'],
                'email_template': row['email_template']
            })
        return jsonify(data['rules']), 200, {'Access-Control-Allow-Origin':'*'}
    else:
        return jsonify({'status': False, 'message': 'Error'}), 500, {'Access-Control-Allow-Origin':'*'}


@app.route('/feedback/rules/', methods=['PUT'])
@swag_from('./docs/updaterules.yml')
def updaterules():
    log.debug("UPDATE RULES INFORMATION")
    data = request.values
    if db.insert_rules(data['info'], data['notice'], data['warning'], data['critical'], data['vulnerability_name'], data['videos'], data['link'], data['severity_levels'], data['email_template']):
        return jsonify({'status': True, 'message': 'This was called and returns something!'}), 200, {'Access-Control-Allow-Origin': '*'}
    else:
        return jsonify({'status': True, 'message': 'Some error occured while updating the feedback rules!!!'}), 200, {'Access-Control-Allow-Origin': '*'}


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
