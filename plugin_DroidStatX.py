# Plugin to handle the tools capable of setting the input for "DroidstatX" and handle the output
import os
import database as db
import subprocess
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

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
        # test the existence of the results directory
        if not os.path.exists(jsonResultsLocation):
            os.system("mkdir " + jsonResultsLocation)

        print("FILE -> " + apk_file)

        if apk_file[-4:] == ".apk":
            print("Running on -> " + apk_file)
            print("Executing -> python2 " + droidStatXLocation + "droidstatx.py --apk " + apk_file)
            # run the tool
            os.system("python2 " + droidStatXLocation + "droidstatx.py --apk " + apk_file)
            cmd = aapt2ToolLocation + "aapt2 dump " + apk_file + " | grep 'Package name'"
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            apkPackageName = str(output)[15:-9]
            # convert .xmind file to JSON -> using xmindparser (already installed)
            # from here: https://github.com/tobyqin/xmindparser
            print("Executing -> xmindparser " + droidStatXLocation + "output_xmind/" + apkPackageName + ".xmind -json")
            os.system("xmindparser " + droidStatXLocation + "output_xmind/" + apkPackageName + ".xmind -json")
            # move the json results to proper folder
            print("mv " + droidStatXLocation + "output_xmind/" + apkPackageName + ".json " + jsonResultsLocation + md5 + ".json")
            os.system("mv " + droidStatXLocation + "output_xmind/" + apkPackageName + ".json " + jsonResultsLocation + md5 + ".json")
            # have also the information registered on the database
            db.insert_results(md5, pluginName, jsonResultsLocation + md5 + ".json")

