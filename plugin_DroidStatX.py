# Plugin to handle the tools capable of setting the input for "DroidstatX" and handle the output
import os
import subprocess

pluginName = "DroidStatX"
enable = True

# TODO: depends on ´aapt2´ tool -> hardcode path, needs to be replaced - needed to get package name!
aapt2ToolLocation = "/usr/local/Caskroom/android-sdk/4333796/build-tools/28.0.3/"
# TODO: hardcoded -> needs to be customised
droidStatXLocation = "../tools/droidstatx/"

jsonResultsLocation = "./json_results/" + pluginName + "/"


class PluginClass:
    def __init__(self):
        ''' constructor '''
        
    def run(self, apkLocation):
        print("Running the DroidStatX plugin!...")
        # test the existence of the results directory
        if not os.path.exists(jsonResultsLocation):
            os.system("mkdir " + jsonResultsLocation)

        # loop through all the APKs on the location and analyse them
        for file in os.listdir(apkLocation):
            if file[-4:] == ".apk":
                print("Running on -> " + file)
                print("Executing -> python2 " + droidStatXLocation + " --apk " + apkLocation + file)
                # run the tool
                os.system("python2 " + droidStatXLocation + "droidstatx.py --apk " + apkLocation + file)
                cmd = aapt2ToolLocation + "aapt2 dump " + apkLocation + file + " | grep 'Package name'"
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                (output, err) = p.communicate()
                apkPackageName = str(output)[15:-9]
                # convert .xmind file to JSON -> using xmindparser (already installed)
                # from here: https://github.com/tobyqin/xmindparser
                print("Executing -> xmindparser " + droidStatXLocation + "output_xmind/" + os.path.basename(apkLocation + apkPackageName) + ".xmind -json")
                os.system("xmindparser " + droidStatXLocation + "output_xmind/" + os.path.basename(apkLocation + apkPackageName) + ".xmind -json")
                # move the json results to proper folder
                os.system("mv " + droidStatXLocation + "output_xmind/" + os.path.basename(apkLocation + apkPackageName) + ".json " + jsonResultsLocation)

