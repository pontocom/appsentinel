import configparser
import json
import database as db
import os
import os.path
from os import path
from vulnCalculator import calculatorClass
import requests
import plugin_DroidStatX as plugDroid
import plugin_Androbugs as plugAbugs

config = configparser.ConfigParser()
config.read('config.ini')

plugins_name ={'Androbugs'}
plugins_name_sorted={'DroidStatX'}

jsonResultsLocation = config['SCANNER']['jsonResultsLocation']
resultsOWASP = config['OWASP_OUTPUT']['owasp_OutputLocation']
resultsFeedback = config['OWASP_OUTPUT']['feedbackResultsLocation']
resultsFeedbackLevels = config['OWASP_OUTPUT']['feedback_levelsResultsLocation']
resultsFeedbackVulnerabilityLevels = config['OWASP_OUTPUT']['feedback_vuln_levelsResultsLocation']

dictionaryAndrobugs = config['DICTIONARY']['androbugsDict']

def startEngine(md5):
    init()
    feedback(md5)
    feedback_vulnerability_levels(md5)
    feedback_levels(md5)


def init():
    if not os.path.exists(resultsOWASP):
        os.system("mkdir " + resultsOWASP)
    if not os.path.exists(resultsFeedback):
        os.system("mkdir " + resultsFeedback)
    if not os.path.exists(resultsFeedbackLevels):
        os.system("mkdir " + resultsFeedbackLevels)
    if not os.path.exists(resultsFeedbackVulnerabilityLevels):
        os.system("mkdir " + resultsFeedbackVulnerabilityLevels)


def feedback(md5):
    data = {}
    owasp_category = ['M1','M2','M3','M4','M5','M6','M7','M8','M9','M10']
    for o in owasp_category:
       data[o]= []
    if plugAbugs.enable:
        for name in plugins_name:
            if path.isfile(jsonResultsLocation + '/' + name + '/' + md5 + '.json') and os.stat(jsonResultsLocation + '/' + name + '/' + md5 + '.json').st_size > 0:
                with open(jsonResultsLocation + '/' + name + '/' + md5 + '.json') as plugin_output:
                    print("OEngine: Reading -> " + jsonResultsLocation + '/' + name + '/' + md5 + '.json')
                    read_data = json.load(plugin_output)
                with open(dictionaryAndrobugs, 'r') as d:
                    dict = json.load(d)
                for x in read_data['results']:
                    for z in owasp_category:
                        for y in dict['results']:

                            if y['category'] == z:

                                if y['name'] == x['vulnerability'] and y['level'] == x['severity']:

                                    data[z].append({
                                        'vulnerability': x['vulnerability'],
                                        'details': x['details'],
                                        'severity': x['severity'],
                                        'detectedby': 'Androbugs',
                                        'feedback': [{ "url": "Nothing to show"},
                                            {"video": y["book"]},
                                            {"book": y["video"]},
                                            {"other": "Nothing to show"}]
                                    })
                                    break                 

    if plugDroid.enable:
        for name in plugins_name_sorted:
            if path.isfile(jsonResultsLocation + '/' + name + '/' + md5 + '.json') and os.stat(jsonResultsLocation + '/' + name + '/' + md5 + '.json').st_size > 0:
                with open(jsonResultsLocation + '/' + name + '/' + md5 + '.json') as plugin_output:
                    read_data = json.load(plugin_output)
                for category in owasp_category:
                    for x in read_data[category]:
                        data[category].append({
                                            'vulnerability': x['vulnerability'],
                                            'details': x['details'],
                                            'severity': x['severity'],
                                            'detectedby': 'DroidStatX',
                                            'feedback': [{ "url": x['link']},
                                                {"video": "Nothing to show"},
                                                {"book": "Nothing to show"},
                                                {"other": "Nothing to show"}]
                                        })
                else:
                    print('DroidStatx failed!')

    with open(resultsFeedback+'/'+md5+'.json', 'w') as f:
        json.dump(data, f)
    db.insert_final_results(md5, resultsFeedback + '/' + md5 + ".json", 0, "NOT YET IN THE FINAL FORMAT")


def feedback_levels(md5):
    with open(resultsFeedback +'/'+ md5 + ".json", "r") as json_file:
        read_content = json.load(json_file)
    data_apk_levels = {}
    data_apk_levels['value'] = []
    data = {}
    
    info = 0
    notice = 0
    warning = 0
    critical = 0

    # category = ['M1','M2','M3','M4','M5','M6','M7','M8','M9','M10']
    # for c in category:
    #     for x in read_content[c]:
    #         if 'Info' in x['severity']:
    #             info += 1
    #         if 'Notice' in x['severity']:
    #             notice += 1
    #         if 'Warning' in x['severity']:
    #             warning += 1
    #         if 'Critical' in x['severity']:
    #             critical += 1

    # data_apk_levels['value']=({
    #     'Info':info,
    #     'Notice': notice,
    #     'Warning': warning,
    #     'Critical': critical
    # })

    score_calculator = calculatorClass(md5)

    # Here the calculator is being used for test purposes
    score_calculator.calculate_all_test()
    data = {'status':'OK', 'value':score_calculator.test_score_results}
    with open(resultsFeedbackLevels +'/'+ md5 + ".json", "w") as save_file:
        json.dump(data, save_file)
    
    # Normal usage of the calculator
    # data = {'status': 'OK', 'value': score_calculator.calculate_method_simple()}

    # with open(resultsFeedbackLevels +'/'+ md5 + ".json", "w") as save_file:
    #     json.dump(data, save_file)
    # db.insert_results_levels(md5, resultsFeedbackLevels + '/' + md5 + ".json", 0, "NOT YET IN THE FINAL FORMAT")
    # try:
    #     payload = {'md5': md5, 'Vulnerability_level': calculatorClass.calculate(md5)}
    #     r = requests.post("https://5.79.81.140:5001/autoFeedback/send", data=payload)
    #     print(r)
    # except:
    #     print('not sended')

        
def feedback_vulnerability_levels(md5):
    with open(resultsFeedback + '/' + md5 + ".json", "r") as json_file:
        read_content = json.load(json_file)
    data_vuln_level ={}
    data_vuln_level['vulnerabilities'] = []

    data={}

    category = ['M1','M2','M3','M4','M5','M6','M7','M8','M9','M10']

    for c in category:
        for x in read_content[c]:
            data_vuln_level['vulnerabilities'].append({
                'vulnerability': x['vulnerability'],
                'severity': x['severity'],
            })

    data = {'status':'OK', 'vulnerabilities': data_vuln_level['vulnerabilities']}

    with open(resultsFeedbackVulnerabilityLevels + '/' + md5 + ".json", "w") as save_file:
        json.dump(data, save_file)
    db.insert_results_vulnerabilitylevel(md5, resultsFeedbackVulnerabilityLevels + '/' + md5 + ".json", 0, "NOT YET IN THE FINAL FORMAT")


def get_number_owasp_vulns(md5):
    read_content = {}
    m1 = 0,
    m2 = 0
    m3 = 0
    m4 = 0
    m5 = 0
    m6 = 0
    m7 = 0
    m8 = 0
    m9 = 0
    m10 = 0

    print(resultsFeedback + '/' + md5 + ".json")
    print(os.path.exists(resultsFeedback + '/' + md5 + ".json"))
    if os.path.exists(resultsFeedback + '/' + md5 + ".json"):
        with open(resultsFeedback + '/' + md5 + ".json", "r") as json_file:
            read_content = json.load(json_file)

        if read_content:
            m1 = len(read_content["M1"])
            m2 = len(read_content["M2"])
            m3 = len(read_content["M3"])
            m4 = len(read_content["M4"])
            m5 = len(read_content["M5"])
            m6 = len(read_content["M6"])
            m7 = len(read_content["M7"])
            m8 = len(read_content["M8"])
            m9 = len(read_content["M9"])
            m10 = len(read_content["M10"])

    print("M1:" + str(m1) + ":M2:" + str(m2) + ":M3:" + str(m3) + ":M4:" + str(m4) + ":M5:" + str(m5) + ":M6:" + str(m6) + ":M7:" + str(m7) + ":M8:" + str(m8) + ":M9:" + str(m9) + ":M10:" + str(m10))

    data = {'status': 'OK', 'M1': str(m1), 'M2': str(m2), 'M3': str(m3), 'M4': str(m4), 'M5': str(m5), 'M6': str(m6), 'M7': str(m7), 'M8': str(m8), 'M9': str(m9), 'M10': str(m10)}


