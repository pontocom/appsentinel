# Plugin to handle the tools capable of setting the input for "TEMPLATE" and handle the output
import os
import configparser
import logging as log


config = configparser.ConfigParser()
config.read('config.ini')

log.basicConfig(filename=config['GENERAL']['logDir'] + "appsentinel.log", filemode='a', format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S', level=log.DEBUG)

pluginName = "Template"
enable = False

# Define any specific configuration directives here
TOOLSPECIFICLocation = config['TOOLSPECIFIC']['TOOLSPECIFICLocation']

# this one is mandatory -> where to place the results of the tool
jsonResultsLocation = config['SCANNER']['jsonResultsLocation'] + "/" + pluginName + "/"


class PluginClass:
    def __init__(self):
        ''' constructor '''
        
    def run(self, apk_file, md5):
        print("Running the TEMPLATE plugin!...")
        # test the existence of the results directory
        if not os.path.exists(jsonResultsLocation):
            os.system("mkdir " + jsonResultsLocation)

        # everything bellow this is specific of your plugin

