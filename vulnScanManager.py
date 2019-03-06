#vulnScanManager, will be responsible for checking a specific directory for apks and for processing them!
import os.path

pluginDir = os.path.dirname(os.path.abspath(__file__))
print(pluginDir)

for file in os.listdir(pluginDir + "/plugins"):
    if file[0:7] == "plugin_" and file[-3:] == ".py":
        print(file)
