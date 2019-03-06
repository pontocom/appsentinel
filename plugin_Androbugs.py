# Plugin to handle the tools capable of setting the input for "DroidstatX" and handle the output
import os

pluginName = "Androbugs"
enable = True


class PluginClass:
    def run(self):
        print("Running the Androbugs plugin!...")
        os.system("python2 ../droidstatx/droidstatx.py --apk ")

