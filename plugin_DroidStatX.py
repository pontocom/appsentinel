# Plugin to handle the tools capable of setting the input for "DroidstatX" and handle the output
import os
import database as db
import subprocess
import configparser
import logging as log

config = configparser.ConfigParser()
config.read('config.ini')

log.basicConfig(filename=config['GENERAL']['logDir'] + "appsentinel.log", filemode='a', format='%(asctime)s,%(msecs)d | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s', datefmt='%H:%M:%S', level=log.DEBUG)

pluginName = "DroidStatX"
enable = False

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
        if not os.path.exists(jsonResultsLocation):
            os.system("mkdir " + jsonResultsLocation)

        print(pluginName + ": FILE -> " + apk_file)
        log.debug(pluginName + ": FILE -> " + apk_file)

        if apk_file[-4:] == ".apk":
            print(pluginName + ": Running on -> " + apk_file)
            log.debug(pluginName + ": Running on -> " + apk_file)
            print(pluginName + ": Executing -> " + config['GENERAL']['python3cmd'] + droidStatXLocation + "droidstatx.py --apk " + apk_file)
            log.debug(pluginName + ": Executing -> " + config['GENERAL']['python3cmd'] + droidStatXLocation + "droidstatx.py --apk " + apk_file)
            # run the tool
            os.system(config['GENERAL']['python3cmd'] + " " + droidStatXLocation + "droidstatx.py --apk " + apk_file)
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
            os.system("mv " + droidStatXLocation + "output_xmind/" + apkPackageName + ".json " + jsonResultsLocation + md5 + ".json")
            # have also the information registered on the database
            db.insert_results(md5, pluginName, jsonResultsLocation + md5 + ".json", 0, "")

