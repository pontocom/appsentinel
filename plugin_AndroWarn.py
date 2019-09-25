# Plugin to handle the tools capable of setting the input for "AndroWarn" and handle the output
import os
import database as db
import subprocess
import configparser
import logging as log


config = configparser.ConfigParser()
config.read('config.ini')

log.basicConfig(filename=config['GENERAL']['logDir'] + "appsentinel.log", filemode='a', format='%(asctime)s,%(msecs)d | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s', datefmt='%H:%M:%S', level=log.DEBUG)

pluginName = "AndroWarn"
enable = True

# Define any specific configuration directives here
androWarnLocation = config['ANDROWARN']['androWarnLocation']

# this one is mandatory -> where to place the results of the tool
jsonResultsLocation = config['SCANNER']['jsonResultsLocation'] + "/" + pluginName + "/"


class PluginClass:
    def __init__(self):
        ''' constructor '''
        
    def run(self, apk_file, md5):
        print("Running the AndroWarn plugin!...")
        log.debug("Running the AndroWarn plugin!...")
        # test the existence of the results directory
        if not os.path.exists(jsonResultsLocation):
            os.system("mkdir " + jsonResultsLocation)

        print(pluginName + ": FILE -> " + apk_file)
        log.debug(pluginName + ": FILE -> " + apk_file)

        if apk_file[-4:] == ".apk":
            print(pluginName + ": Running on -> " + apk_file)
            log.debug(pluginName + ": Running on -> " + apk_file)
            print(pluginName + ": Executing -> " + config['GENERAL']['python2cmd'] + androWarnLocation + " androwarn.py -i " + apk_file + " -r json -v 3")
            log.debug(pluginName + ": Executing -> " + config['GENERAL']['python2cmd'] + androWarnLocation + " androwarn.py -i " + apk_file + " -r json -v 3")

