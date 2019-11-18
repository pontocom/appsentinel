# Plugin to handle the tools capable of setting the input for "DroidstatX" and handle the output
import os

import subprocess
import configparser
import logging as log
import json
import databaseMG as dbMG

config = configparser.ConfigParser()
config.read('config.ini')

log.basicConfig(filename=config['GENERAL']['logDir'] + "appsentinel.log", filemode='a', format='%(asctime)s,%(msecs)d | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s', datefmt='%H:%M:%S', level=log.DEBUG)

pluginName = "DroidStatX"
enable = True

aapt2ToolLocation = config['DROIDSTATX']['aapt2ToolLocation']
droidStatXLocation = config['DROIDSTATX']['droidStatXLocation']

jsonResultsLocation = config['SCANNER']['jsonResultsLocation'] + "/" + pluginName + "/"


class PluginClass:
    def __init__(self):
        ''' constructor '''
        
    def run(self, apk_file, md5):
        print("Running the DroidStatX plugin!...")
        log.debug("Running the DroidStatX plugin!...")
        # test the existence of the results directory
        # if not os.path.exists(jsonResultsLocation):
        #     os.system("mkdir " + jsonResultsLocation)

        print(pluginName + ": FILE -> " + apk_file)
        log.debug(pluginName + ": FILE -> " + apk_file)

        if apk_file[-4:] == ".apk":
            print(pluginName + ": Running on -> " + apk_file)
            log.debug(pluginName + ": Running on -> " + apk_file)
            print(pluginName + ": Executing -> " + config['GENERAL']['python3cmd'] + droidStatXLocation + "droidstatx.py --apk " + apk_file)
            log.debug(pluginName + ": Executing -> " + config['GENERAL']['python3cmd'] + droidStatXLocation + "droidstatx.py --apk " + apk_file)
            # run the tool
            os.system(config['GENERAL']['python3cmd'] + " " + droidStatXLocation + "droidstatx.py --apk " + apk_file)
            # probably it is not necessary to have this... maybe apktool is enough for this
            cmd = aapt2ToolLocation + "aapt2 dump " + apk_file + " | grep 'Package name'"
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            apkPackageName = str(output)[15:-9]
            # convert .xmind file to JSON -> using xmindparser (already installed)
            # from here: https://github.com/tobyqin/xmindparser
            print(pluginName + ": Executing -> xmindparser " + droidStatXLocation + "output_xmind/" + apkPackageName + ".xmind -json")
            log.debug(pluginName + ": Executing -> xmindparser " + droidStatXLocation + "output_xmind/" + apkPackageName + ".xmind -json")
            os.system("xmindparser " + droidStatXLocation + "output_xmind/" + apkPackageName + ".xmind -json")
            # move the json results to proper folder
            print(pluginName + ": mv " + droidStatXLocation + "output_xmind/" + apkPackageName + ".json " + jsonResultsLocation + md5 + ".json")
            log.debug(pluginName + ": mv " + droidStatXLocation + "output_xmind/" + apkPackageName + ".json " + jsonResultsLocation + md5 + ".json")
            #os.system("mv " + droidStatXLocation + "output_xmind/" + apkPackageName + ".json " + jsonResultsLocation + md5 + ".json")
            # insert data to DB
            results_location = droidStatXLocation + "output_xmind/" + apkPackageName + ".json"
            with open (results_location, 'r') as read_data:
                results = json.load(read_data)
                dbMG.insert_temporary_results_by_tool(md5, pluginName, results)
                os.system("rm " + droidStatXLocation + "output_xmind/" + apkPackageName + ".json")

            self.analyseVulnerability(md5)


            # have also the information registered on the database
            #db.insert_results(md5, pluginName, jsonResultsLocation + md5 + ".json", 0, "")




    def analyseVulnerability(self, md5):
        output={}
        m_aux_array= {'M1','M2','M3','M4','M5','M6','M7','M8','M9','M10'}
        for level in m_aux_array:
            output[level] = []
        #with open(jsonResultsLocation + md5 + '.json', 'r') as f:
             #read_data = json.load(f)
        read_data = dbMG.get_temporary_results_by_tool(md5, pluginName)[0]['results']
        data = read_data[0]
        methodology = data['topic']['topics'][1]['topics']

        for m_level in methodology:
            m_title=m_level['title']
            for vulnerability in m_level['topics']:
                if 'makers' in vulnerability:
                    if 'green' in vulnerability['makers'][0]:
                        continue
                    else:
               # if '?' not in vulnerability['title']:
                        _link = ''
                        _severity = ''
                        _details = 'nothing'
                        #if hasMoreVulnerabilities(vulnerability):
                        #    analyseVulnerability(vulnerability['topics'])
                        # inside a vulnerabilities there is another JSON array with some details
                        # if 'topics' in vulnerability:
                        #     i = 0
                        #     for detail in vulnerability['topics']:
                        #         if '?' not in detail['title']:
                        #             _details[i]=detail['title']
                        #         i = i+1
                        # else:
                        #     _details = 'nothing'

                        # some vulnerabilities dont have flags

                        #if 'makers' not in vulnerability:
                        #    _severity = 'info'
                        #else:
                        _severity = self.flag_to_severity(vulnerability['makers'][0])

                        # some vulnerabilities dont have links
                        if 'link' not in vulnerability:
                            _link = 'nothing'
                        else:
                            _link = vulnerability['link']

                        output[self.owasp_level(m_title)].append({
                            'vulnerability': vulnerability['title'],
                            'severity': _severity,
                            'link': _link,
                            'details' : _details,
                            'detectedby': 'droidstatx'})

        # with open(jsonResultsLocation + md5 + '.json', 'w') as outfile:
        #     json.dump(output, outfile)

        dbMG.insert_results(md5, pluginName, output, 0)
        dbMG.delete_temporary_results(md5, pluginName)

    # set the current OWASP M level
    def owasp_level(self, argument):
        switcher = {
            'Improper Platform Usage': "M1",
            'Insecure Data Storage': "M2",
            'Insecure Communication': "M3",
            'Insecure Authentication': 'M4',
            'Insufficient Cryptography': 'M5',
            'Insecure Authorization': 'M6',
            'Client Code Quality': 'M7',
            'Code Tampering': 'M8',
            'Reverse Engineering': 'M9',
            'Extraneous Functionality' : 'M10',
        }
        return switcher.get(argument, "nothing")

    # according to given flag passes it to severity level
    def flag_to_severity(self, flag):
        switcher = {
            #'flag-green': 'info',
            'flag-yellow': 'Warning',
            'flag-red': 'Critical'
        }
        return switcher.get(flag, "nothing")

    # some vulnerabilities have topics that contains more vulnerabilites
    def hasMoreVulnerabilities(vulnerability):
        if 'topics' not in vulnerability:
            return False
        else:
            for newVulnerability in vulnerability['topics']:
                if 'makers' in newVulnerability:
                    return True
            return False
