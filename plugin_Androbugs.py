# Plugin to handle the tools capable of setting the input for "DroidstatX" and handle the output
import os
import database as db
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

pluginName = "Androbugs"
enable = True

jsonResultsLocation = config['SCANNER']['jsonResultsLocation'] + "/" + pluginName + "/"
androbugsLocation = config['ANDROBUGS']['androbugsLocation']


class PluginClass:
    def __init__(self):
        ''' constructor '''
        
    def run(self, apk_file, md5):
        print(pluginName + ": Running the Androbugs plugin!...")
        # test the existence of the results directory
        if not os.path.exists(jsonResultsLocation):
            os.system("mkdir " + jsonResultsLocation)

        # don't know why, but Androbugs requires running from the APK dir
        # print("ANDROBUGS cd " + apkLocation)
        # os.system("cd " + apkLocation)
        if apk_file[-4:] == ".apk":
            print(pluginName + ": Running on -> " + apk_file)
            print(pluginName + ": Executing -> python2 " + androbugsLocation + "androbugs.py -f " + apk_file + " --md5file " + md5 + " -o " + jsonResultsLocation)
            # run the tool
            os.system("python2 " + androbugsLocation + "androbugs.py -v -f " + apk_file + " --md5file " + md5 +" -o " + jsonResultsLocation)
            # this tool produces a text-based output... we need to consider what to do with this
            # TODO: output in TXT format - needs to be handled in a different manner

