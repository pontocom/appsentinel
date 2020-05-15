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
import plugin_Super as plugSuper

config = configparser.ConfigParser()
config.read('config.ini')

plugins_name_sorted={'DroidStatX'}

jsonResultsLocation = config['SCANNER']['jsonResultsLocation']
resultsOWASP = config['OWASP_OUTPUT']['owasp_OutputLocation']
resultsFeedback =config['OWASP_OUTPUT']['feedbackResultsLocation']
resultsFeedbackLevels = config['OWASP_OUTPUT']['feedback_levelsResultsLocation']
resultsFeedbackVulnerabilityLevels = config['OWASP_OUTPUT']['feedback_vuln_levelsResultsLocation']

dictionaryAndrobugs = config['DICTIONARY']['androbugsDict']
dictionaryDroidstatx = config['DICTIONARY']['droidstatxDict']
dictionarySuper = config['DICTIONARY']['superDict']

plugins_dict ={ 'DroidStatX': [dictionaryDroidstatx, plugDroid], 'Androbugs': [dictionaryAndrobugs, plugAbugs],'Super':[dictionarySuper, plugSuper]}

baseknowledge = config['DICTIONARY']['baseKnowledge']

enabled_plugins=[]


def startEngine(md5):
    init()
    feedback(md5)
    #feedback_vulnerability_levels(md5)
    #feedback_levels(md5)

def init():
    if not os.path.exists(resultsOWASP):
        os.system("mkdir " + resultsOWASP)
    if not os.path.exists(resultsFeedback):
        os.system("mkdir " + resultsFeedback)
    if not os.path.exists(resultsFeedbackLevels):
        os.system("mkdir " + resultsFeedbackLevels)
    if not os.path.exists(resultsFeedbackVulnerabilityLevels):
        os.system("mkdir " + resultsFeedbackVulnerabilityLevels)
    # looking for the plugins
    pluginDir = os.path.dirname(os.path.abspath(__file__))

    for file in os.listdir(pluginDir):
        if file[0:7] == "plugin_" and file[-3:] == ".py":
            print(file)
            # we need to do something with them... need to check if it is better to import or to spawn (decide later)
            thisPlugin = __import__(".".join(file.split(".")[0:-1]))
            if thisPlugin.enable:
                enabled_plugins.append(thisPlugin)


def feedback(md5):
    data={}
    owasp_category = ['M1','M2','M3','M4','M5','M6','M7','M8','M9','M10']
    for o in owasp_category:
       data[o]= []
    with open(baseknowledge, 'r') as bk_file:
        bk_content = json.load(bk_file)
    for plugin in enabled_plugins:
        if path.isfile(jsonResultsLocation + '/' + plugin.pluginName + '/' + md5 + '.json') and os.stat(jsonResultsLocation + '/' + plugin.pluginName + '/' + md5 + '.json').st_size > 0:
            with open(jsonResultsLocation + '/' + plugin.pluginName + '/' + md5 + '.json') as plugin_output:
                print("OEngine: Reading -> " + jsonResultsLocation + '/' + plugin.pluginName + '/' + md5 + '.json')
                read_data = json.load(plugin_output)
            dict_plugin_name = plugin.pluginName.lower()
            with open('./dictionaries/'+dict_plugin_name+'_dict.json', 'r') as d:
                dict = json.load(d)
            for x in read_data['results']:
                
                for z in owasp_category:
                    for y in dict['results']:

                        if y['category'] == z:

                            if y['name'] == x['vulnerability'] :
                                q = """and y['level'] == x['severity']"""
                                data[z].append({
                                    'vulnerability': x['vulnerability'],
                                    'details': x['details'],
                                    'severity': x['severity'],
                                    'detectedby': plugin.pluginName,
                                    'feedback': {
                                        "url": [] ,
                                        "video": "",
                                        "book": [],
                                        "other": "Nothing to show"
                                    }
                                })
                                                
            for category in owasp_category:                     
                for d in data[category]:
                    for info in dict['results']:
                        if d['vulnerability']== info['name']:

                            for content in bk_content['results']:
                                for bk_info in content['keywords']:
                                    for keyword in info['keywords']:
                                        
                                        if keyword==bk_info['name']:
                                            for link in bk_info['links']:
                                                d['feedback']['url'].append(link)
                                                                

    # if plugDroid.enable:
    #     with open(dictionaryDroidstatx, 'r') as d:
    #         dict = json.load(d)
    #     for name in plugins_name_sorted:
    #         if path.isfile(jsonResultsLocation + '/' + name + '/' + md5 + '.json') and os.stat(jsonResultsLocation + '/' + name + '/' + md5 + '.json').st_size > 0:
    #             with open(jsonResultsLocation + '/' + name + '/' + md5 + '.json') as plugin_output:
    #                 read_data = json.load(plugin_output)
    #             for category in owasp_category:
    #                 for x in read_data[category]:
    #                     data[category].append({
    #                                         'vulnerability': x['vulnerability'],
    #                                         'details': x['details'],
    #                                         'severity': x['severity'],
    #                                         'detectedby': 'DroidStatX',
    #                                         'feedback':{
    #                                             "url": [] ,
    #                                             "video": "",
    #                                             "book": [],
    #                                             "other": "Nothing to show"
    #                                         }
                                            
    #                                     })
    #     for category in owasp_category:                     
    #         for d in data[category]:
    #             #print(d['vulnerability'])
    #             for info in dict['results']:
    #                 if d['vulnerability']== info['name']:

    #                     for content in bk_content['results']:
    #                         for bk_info in content['keywords']:
    #                             for keyword in info['keywords']:
                                    
    #                                 if keyword==bk_info['name']:
    #                                     for link in bk_info['links']:
    #                                         d['feedback']['url'].append(link)
            
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

    data = {'status': 'OK', 'value': calculatorClass.calculate(md5)}

    with open(resultsFeedbackLevels +'/'+ md5 + ".json", "w") as save_file:
        json.dump(data, save_file)
    db.insert_results_levels(md5, resultsFeedbackLevels + '/' + md5 + ".json", 0, "NOT YET IN THE FINAL FORMAT")
    try:
        payload = {'md5': md5, 'Vulnerability_level': calculatorClass.calculate(md5)}
        r = requests.post("https://5.79.81.140:5001/autoFeedback/send", data=payload)
        print(r)
    except:
        print('not sended')

        
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
