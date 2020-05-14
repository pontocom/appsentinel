# Plugin to handle the tools capable of setting the input for "Super" and handle the output
import os
import database as db
import subprocess
import configparser
import logging as log
import json
import glob

config = configparser.ConfigParser()
config.read('config.ini')

log.basicConfig(filename=config['GENERAL']['logDir'] + "appsentinel.log", filemode='a', format='%(asctime)s,%(msecs)d | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s', datefmt='%H:%M:%S', level=log.DEBUG)

pluginName = "Super"
enable = True

superLocation = config['SUPER']['superLocation']

jsonResultsLocation = config['SCANNER']['jsonResultsLocation'] + "/" + pluginName + "/"



class PluginClass:
    def __init__(self):
        ''' constructor '''

    def run(self, apk_file, md5):
        print('\nRunning the Super plugin!...')
        log.debug('Running the Super plugin!...')
        if not os.path.exists(jsonResultsLocation):
            os.system('chmod 755 ' + superLocation)
            os.system('mkdir ' + jsonResultsLocation)

        print(pluginName + ': FILE -> ' + apk_file)
        log.debug(pluginName + ': FILE -> ' + apk_file)

        if apk_file[-4:] == ".apk":
            print(pluginName + ': Running on -> ' + apk_file)
            log.debug(pluginName + ': Running on -> ' + apk_file)
            os.chdir(superLocation)
            print(superLocation + config['GENERAL']['supercmd'] + " " + "--json ../." + apk_file)
            log.debug(superLocation + config['GENERAL']['supercmd'] + " " + "--json ../." + apk_file)
            # run the tool and move the json results to proper folder
            os.system(config['GENERAL']['supercmd'] + " " + "--json ../." + apk_file)
            #os.system('mv results/'+)
            print(os.system)
            print(superLocation + config['GENERAL']['supercmd'] + " " + "--json " + apk_file)
            log.debug(superLocation + config['GENERAL']['supercmd'] + " " + "--json " + apk_file)
            os.chdir('../../')
            b = './tools/super/results/'
            a = glob.glob(b+"*")
            c = glob.glob(b + os.path.basename(a[0]) + '/*')
            os.system('mv ' + a[0]+'/'+os.path.basename(c[0]) + ' ./json_results/Super/'+md5+'.json')
            self.build_scan_format(md5)

    
    def build_scan_format(self, md5):
        data = {}
        data_formated = {}
        data_formated['results'] = []
        
        with open(jsonResultsLocation + md5 + '.json', 'r' ) as json_file:
            content = json.load(json_file)

        for key in content['criticals']:
            data[key['name']]=[key['description'], key['criticality']]

        for key in content['highs']:
            data[key['name']]=[key['description'], key['criticality']]

        for key in content['mediums']:
            data[key['name']]=[key['description'], key['criticality']]

        for key in content['lows']:
            data[key['name']]=[key['description'], key['criticality']]

        for key in content['warnings']:
            data[key['name']]=[key['description'], key['criticality']]

        
        for key in data:
            data_formated['results'].append({
                'vulnerability': key,
                'details': data[key][0],
                'severity': data[key][1],
                'detectedby': 'Super',
                'feedback': [{"url": ""},
                                {"video": ""},
                                {"book": ""},
                                {"other": ""}]
            })


        with open(jsonResultsLocation + md5 + '.json', 'w') as outfile:
            json.dump(data_formated, outfile)










