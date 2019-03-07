# Plugin to handle the tools capable of setting the input for "DroidstatX" and handle the output
import os

pluginName = "Androbugs"
enable = True

jsonResultsLocation = "./json_results/" + pluginName + "/"

class PluginClass:
    def run(self, apkLocation):
        print("Running the Androbugs plugin!...")
        # test the existence of the results directory
        if not os.path.exists(jsonResultsLocation):
            os.system("mkdir " + jsonResultsLocation)
