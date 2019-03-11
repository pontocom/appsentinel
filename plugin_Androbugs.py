# Plugin to handle the tools capable of setting the input for "DroidstatX" and handle the output
import os

pluginName = "Androbugs"
enable = True

jsonResultsLocation = "./json_results/" + pluginName + "/"

androbugsLocation = "../tools/AndroBugs/"

class PluginClass:
    def __init__(self):
        ''' constructor '''
        
    def run(self, apkLocation):
        print("Running the Androbugs plugin!...")
        # test the existence of the results directory
        if not os.path.exists(jsonResultsLocation):
            os.system("mkdir " + jsonResultsLocation)

        # don't know why, but Androbugs requires running from the APK dir
        os.system("cd " + apkLocation)
        # loop through all the APKs on the location and analyse them
        for file in os.listdir(apkLocation):
            if file[-4:] == ".apk":
                print("Running on -> " + file)
                print("Executing -> python2 " + androbugsLocation + "androbugs.py -f " + apkLocation + file + " -o " + jsonResultsLocation)
                # run the tool
                os.system("python2 " + androbugsLocation + "androbugs.py -v -f " + apkLocation + file + " -o " + jsonResultsLocation)
                # this tool produces a text-based output... we need to consider what to do with this
                # TODO: output in TXT format - needs to be handled in a different manner

