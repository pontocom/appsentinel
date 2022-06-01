# vulnScanManager, will be responsible for checking a specific directory for apks and for processing them!
import os.path
import argparse
import multiprocessing
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# location of the results of the tool
jsonResultsLocation = config['SCANNER']['jsonResultsLocation']
jsonResultsLocation = config['SCANNER']['jsonResultsLocation']

plugins = []
thisPlugin = None
counter_plugins = 0


# location of the unprocessed APKs
# apkDir = "/Users/cserrao/Documents/Development/AppSentinel/apks/unprocessed/"

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
    thisPlugin = plugins[pluginNum]
    return thisPlugin


def runSelectedPlugin():
    if thisPlugin == 0:
        raise Exception("you didn't assign a module yet.")
    c = thisPlugin.PluginClass()
    c.run()


def run_this_plugin(plugin_number, apk_location, apk_md5, package):
    thisPlugin = plugins[plugin_number]
    c = thisPlugin.PluginClass()
    c.run(apk_location, apk_md5, package)


'''
A tool to scan APKs and look for vulnerabilities
'''
if __name__ == "__main__":
    VERSION = '0.1'
    banner = "SCANNER"
    print(str(banner))

    text = "Tool that scans APKs and looks for vulnerabilities"
    parser = argparse.ArgumentParser(description=text)
    parser.add_argument('-v', '--version', action='version', version='Vulnerability Scan Manager ' + VERSION)
    parser.add_argument('-f', '--file', help='The APK file to analyse.',
                        action='store', dest='apkfile', nargs=1, default='')
    parser.add_argument('-m', '--md5', help='The APK file MD5 id to analyse.',
                        action='store', dest='md5Id', nargs=1, default='')
    parser.add_argument('-p', '--package', help='The package name of the APK.',
                        action='store', dest='packageName', nargs=1, default='')
    args = parser.parse_args()

    print(args)

    apkFile = args.apkfile[0]
    md5Id = args.md5Id[0]

    package = ''
    if args.packageName != '':
        package = args.packageName[0]

    # if args.apkfile != "":
    #    apkFile = args.apkfile[0]
    #    print("APK FILE -> " + apkFile)
    # else:
    #    md5Id = args.md5Id[0]
    #    print("APK MD5 -> " + md5Id)

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
                counter_plugins = counter_plugins + 1

    # we use the same approach to look for the APKs to analyse
    listPlugins()

    # this version runs the plugins concurrently
    # runPlugins(apkDir)

    # an alternative testing to run the tools in parallel
    for i in range(counter_plugins):
        jobs = []
        p = multiprocessing.Process(target=run_this_plugin, args=(i, apkFile, md5Id, package))
        jobs.append(p)
        p.start()
