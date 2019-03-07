# vulnScanManager, will be responsible for checking a specific directory for apks and for processing them!
import os.path
import argparse

# location of the results of the tool
jsonResultsLocation = "./json_results"
# location of the unprocessed APKs
apkDir = "/Users/cserrao/Documents/Development/AppSentinel/apks/unprocessed/"

def listPlugins():
    print("These are the available plugins:")
    for m in plugins:
        print(m.pluginName)


def runPlugins(apkLocation):
    print("Running all the available plugins:")
    for m in plugins:
        c = m.PluginClass()
        c.run(apkLocation)


def selectPlugin(pluginNum):
    thisPlugin = plugins[modNum]


def runSelectedPlugin():
    if thisPlugin == 0:
        raise ArgumentError("you didn't assign a module yet.")
    c = thisPlugin.PluginClass()
    c.run()


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
    args = parser.parse_args()

    print(args)

    # looking for the plugins
    pluginDir = os.path.dirname(os.path.abspath(__file__))
    print(pluginDir)

    # test the existence of the results directory
    if not os.path.exists(jsonResultsLocation):
        os.system("mkdir " + jsonResultsLocation)

    for file in os.listdir(pluginDir):
        if file[0:7] == "plugin_" and file[-3:] == ".py":
            print(file)
            # we need to do something with them... need to check if it is better to import or to spawn (decide later)
            print("Importing -> " + ".".join(file.split(".")[0:-1]))
            thisPlugin = __import__(".".join(file.split(".")[0:-1]))
            if thisPlugin.enable:
                plugins.append(thisPlugin)

    # we use the same approach to look for the APKs to analyse
    listPlugins()
    runPlugins(apkDir)

