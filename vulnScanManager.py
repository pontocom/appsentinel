# vulnScanManager, will be responsible for checking a specific directory for apks and for processing them!
import os.path
import argparse

if __name__=="__main__":
    VERSION = '0.1'
    banner = """
                .__           _________                        _____                                             
    ___  ____ __|  |   ____  /   _____/ ____ _____    ____    /     \ _____    ____ _____     ____   ___________ 
    \  \/ /  |  \  |  /    \ \_____  \_/ ___\\\\__  \  /    \  /  \ /  \\\\__  \  /    \\\\__  \   / ___\_/ __ \_  __ \ 
     \   /|  |  /  |_|   |  \/        \  \___ / __ \|   |  \/    Y    \/ __ \|   |  \/ __ \_/ /_/  >  ___/|  | \/ 
      \_/ |____/|____/___|  /_______  /\___  >____  /___|  /\____|__  (____  /___|  (____  /\___  / \___  >__|   
                          \/        \/     \/     \/     \/         \/     \/     \/     \//_____/      \/       """

    plugins = []
    thisPlugin = 0

    print(str(banner))

    text = "Tool that scans APKs and looks for vulnerabilities"
    parser = argparse.ArgumentParser(description = text)
    parser.add_argument('-v', '--version', action='version', version='Vulnerability Scan Manager ' + VERSION)
    parser.add_argument('-d', '--directory', help='Location to the directory that contains APKs to analyse.', action='store', dest='apkdir', nargs=1, default='./')
    parser.add_argument('-p', '--plugins', help='Location of the plugins directory.',
                        action='store', dest='plugdir', nargs=1, default='./')
    args = parser.parse_args()

    print(args)

    # looking for the plugins
    pluginDir = os.path.dirname(os.path.abspath(__file__))
    print(pluginDir)

    for file in os.listdir(pluginDir + "/plugins"):
        if file[0:7] == "plugin_" and file[-3:] == ".py":
            print(file)
            # we need to do something with them... need to check if it is beter ti import or to spawn
            print("Importing -> " + ".".join(file.split(".")[0:-1]))
            thisPlugin = __import__("plugins." + ".".join(file.split(".")[0:-1]))
            if thisPlugin.enable == True:
                plugins.append(thisPlugin)

    # looking for the APKs to analyse
    # we use the same approach to look for the APKs to analyse

