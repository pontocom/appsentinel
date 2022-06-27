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

log.basicConfig(filename=config['GENERAL']['logDir'] + "appsentinel.log", filemode='a',
                format='%(asctime)s,%(msecs)d | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s',
                datefmt='%H:%M:%S', level=log.DEBUG)

pluginName = "Super"
enable = False

superLocation = config['SUPER']['superLocation']

jsonResultsLocation = config['SCANNER']['jsonResultsLocation'] + "/" + pluginName + "/"


class PluginClass:
    def __init__(self):
        ''' constructor '''

    def run(self, apk_file, md5, package=''):
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
            print("PATH -> " + str(os.getcwd()))
            print(config['SUPER']['supercmd'] + " " + "--json " + config['GENERAL']['appsentinel'] + apk_file[2:])
            log.debug(config['SUPER']['supercmd'] + " " + "--json " + config['GENERAL']['appsentinel'] + apk_file[2:])
            # run the tool and move the json results to proper folder
            os.system(config['SUPER']['supercmd'] + " " + "--json " + config['GENERAL']['appsentinel'] + apk_file[2:])
            # os.system('mv results/'+)
            # os.chdir('../../')
            os.chdir(config['GENERAL']['appsentinel'])
            print("PATH -> " + str(os.getcwd()))
            # print(superLocation + config['SUPER']['supercmd'] + " " + "--json " + apk_file)
            # log.debug(superLocation + config['SUPER']['supercmd'] + " " + "--json " + apk_file)
            path = '../tools/super/results/'
            fileName = glob.glob(path + "*")
            print('Filename ---> ' + str(fileName))
            if not os.path.isdir(fileName[0]):
                if package == '':
                    os.system('mv ' + fileName[0] + ' ./json_results/Super/' + md5 + '.json')
                    self.build_scan_format(md5)
                    os.system('rm -r ../tools/super/results/')
                else:
                    os.system('mv ' + fileName[0] + ' ./json_results/Super/' + package + '.json')
                    self.build_scan_format(package)
                    os.system('rm -r ../tools/super/results/')
            else:
                if package == '':
                    directory = glob.glob(path + os.path.basename(fileName[0]) + '/*')
                    os.system('mv ' + fileName[0] + '/' + os.path.basename(
                        directory[0]) + ' ./json_results/Super/' + md5 + '.json')
                    self.build_scan_format(md5)
                    os.system('rm -r ../tools/super/results/')
                else:
                    directory = glob.glob(path + os.path.basename(fileName[0]) + '/*')
                    os.system('mv ' + fileName[0] + '/' + os.path.basename(
                        directory[0]) + ' ./json_results/Super/' + package + '.json')
                    self.build_scan_format(package)
                    os.system('rm -r ../tools/super/results/')

    def build_scan_format(self, md5):
        data = {}
        data_formated = {}
        data_formated['results'] = []

        with open(jsonResultsLocation + md5 + '.json', 'r') as json_file:
            content = json.load(json_file)

        for key in content['criticals']:
            data[key['name']] = [key['description'], 'Critical']

        for key in content['highs']:
            data[key['name']] = [key['description'], 'Critical']

        for key in content['mediums']:
            data[key['name']] = [key['description'], 'Warning']

        for key in content['lows']:
            data[key['name']] = [key['description'], 'Notice']

        for key in content['warnings']:
            data[key['name']] = [key['description'], 'Notice']

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
