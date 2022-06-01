# Plugin to handle the tools capable of setting the input for "DroidstatX" and handle the output
import os
import database as db
import configparser
import logging as log
import linecache
import json
import datetime

config = configparser.ConfigParser()
config.read('config.ini')

log.basicConfig(filename=config['GENERAL']['logDir'] + "appsentinel.log", filemode='a',
                format='%(asctime)s,%(msecs)d | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s',
                datefmt='%H:%M:%S', level=log.DEBUG)

pluginName = "Androbugs"
vullevelfolder = "vulnerabilities_level"
levelsfolder = "levels_for_apk"

enable = True

jsonResultsLocation = config['SCANNER']['jsonResultsLocation'] + "/" + pluginName + "/"
jsonResultsLocationVulnLevel = config['SCANNER']['jsonResultsLocation'] + "/" + pluginName + "/" + vullevelfolder + "/"
jsonResultsLocationLevels = config['SCANNER']['jsonResultsLocation'] + "/" + pluginName + "/" + levelsfolder + "/"

androbugsLocation = config['ANDROBUGS']['androbugsLocation']

dictionary = config['DICTIONARY']['androbugsDict']


class PluginClass:
    def __init__(self):
        ''' constructor '''

    def convert_to_json(self, md5):
        txt_file = open(jsonResultsLocation + md5 + ".txt", "r")
        lines = txt_file.readlines()
        line_counter = 1
        critical = []
        warning = []
        notice = []
        info = []

        critical_status = False
        warning_status = False
        notice_status = False
        info_status = False
        add = True
        for line in lines:
            if line.startswith("[Critical]"):
                critical.append("Critical")
                critical_status = True
                warning_status = False
                notice_status = False
                info_status = False
                add = True
            if line.startswith("[Warning]"):
                warning.append("Warning")
                critical_status = False
                warning_status = True
                notice_status = False
                info_status = False
                add = True
            if line.startswith("[Notice]"):
                notice.append("Notice")
                critical_status = False
                warning_status = False
                notice_status = True
                info_status = False
                add = True
            if line.startswith("[Info]"):
                info.append("Info")
                critical_status = False
                warning_status = False
                notice_status = False
                info_status = True
                add = True
            if line.startswith("-------"):
                add = False
            if critical_status and add:
                critical.append(line_counter)
            if warning_status and add:
                warning.append(line_counter)
            if notice_status and add:
                notice.append(line_counter)
            if info_status and add:
                info.append(line_counter)
            line_counter = line_counter + 1

        # now let's try to put everything on a JSON format :-)
        json_file = open(jsonResultsLocation + md5 + ".json", "w")
        json_file.write("{")
        json_file.write("\"results\": ")
        json_file.write("{\"critical_level\": [")
        text2write = ""
        is_first = True
        for critical_line in critical:
            if critical_line == 'Critical' and is_first:
                text2write = text2write + "{\"critical\": \""
                is_first = False
                continue
            if critical_line == 'Critical' and not is_first:
                text2write = text2write + "\"}, {\"critical\": \""
            else:
                what2write = linecache.getline(jsonResultsLocation + md5 + ".txt", critical_line)
                text2write = text2write + what2write.replace('"', '\\"')[:-1]
        text2write = text2write + "\"}]"
        json_file.write(text2write)
        json_file.write(",")
        json_file.write("\"warning_level\": [")
        text2write = ""
        is_first = True
        for warning_line in warning:
            if warning_line == 'Warning' and is_first:
                text2write = text2write + "{\"warning\": \""
                is_first = False
                continue
            if warning_line == 'Warning' and not is_first:
                text2write = text2write + "\"}, {\"warning\": \""
            else:
                what2write = linecache.getline(jsonResultsLocation + md5 + ".txt", warning_line)
                text2write = text2write + what2write.replace('"', '\\"')[:-1]
        text2write = text2write + "\"}"
        json_file.write(text2write)
        json_file.write("],")
        json_file.write("\"notice_level\": [")
        text2write = ""
        is_first = True
        for notice_line in notice:
            if notice_line == 'Notice' and is_first:
                text2write = text2write + "{\"notice\": \""
                is_first = False
                continue
            if notice_line == 'Notice' and not is_first:
                text2write = text2write + "\"}, {\"notice\": \""
            else:
                what2write = linecache.getline(jsonResultsLocation + md5 + ".txt", notice_line)
                text2write = text2write + what2write.replace('"', '\\"')[:-1]
        text2write = text2write + "\"}"
        json_file.write(text2write)
        json_file.write("],")
        json_file.write("\"info_level\": [")
        text2write = ""
        is_first = True
        for info_line in info:
            if info_line == 'Info' and is_first:
                text2write = text2write + "{\"info\": \""
                is_first = False
                continue
            if info_line == 'Info' and not is_first:
                text2write = text2write + "\"}, {\"info\": \""
            else:
                what2write = linecache.getline(jsonResultsLocation + md5 + ".txt", info_line)
                text2write = text2write + what2write.replace('"', '\\"')[:-1]
        text2write = text2write + "\"}"
        json_file.write(text2write)
        json_file.write("]")
        json_file.write("}")
        json_file.write("}")

    def convert_to_new_json(self, md5):
        txt_file = open(jsonResultsLocation + md5 + ".txt", "r")
        lines = txt_file.readlines()
        line_counter = 1
        critical = []
        warning = []
        notice = []
        info = []

        critical_status = False
        warning_status = False
        notice_status = False
        info_status = False
        add = True
        for line in lines:
            if line.startswith("[Critical]"):
                critical.append("Critical")
                critical_status = True
                warning_status = False
                notice_status = False
                info_status = False
                add = True
            if line.startswith("[Warning]"):
                warning.append("Warning")
                critical_status = False
                warning_status = True
                notice_status = False
                info_status = False
                add = True
            if line.startswith("[Notice]"):
                notice.append("Notice")
                critical_status = False
                warning_status = False
                notice_status = True
                info_status = False
                add = True
            if line.startswith("[Info]"):
                info.append("Info")
                critical_status = False
                warning_status = False
                notice_status = False
                info_status = True
                add = True
            if line.startswith("-------"):
                add = False
            if critical_status and add:
                critical.append(line_counter)
            if warning_status and add:
                warning.append(line_counter)
            if notice_status and add:
                notice.append(line_counter)
            if info_status and add:
                info.append(line_counter)
            line_counter = line_counter + 1

        # now let's try to put everything on a JSON format :-)
        json_file = open(jsonResultsLocation + md5 + ".json", "w")
        # json_file.write("{")
        # json_file.write("\"results\": ")
        # json_file.write("{\"M1\": [")
        text2write = ""
        is_first = True
        hasM1 = False
        hasM2 = False
        hasM3 = False
        hasM4 = False
        hasM5 = False
        hasM6 = False
        hasM7 = False
        hasM8 = False
        hasM9 = False
        hasM10 = False
        json_file.write("{")
        for critical_line in critical:
            if critical_line == 'Critical' and is_first:
                json_file.write("\"M1\": [")
                text2write = text2write + "{\"vulnerability\": \""
                is_first = False
                hasM1 = True
                continue
            if critical_line == 'Critical' and not is_first:
                text2write = text2write + "\", "
                text2write = text2write + "\"details\": \"\", \"severity\": \"Critical\", \"detectedby\": [\"Androbugs\"],"
                text2write = text2write + "\"feedback\": [{\"url\":\"\"}, {\"video\":\"\"}, {\"book\":\"\"}, {\"other\":\"\"}]"
                text2write = text2write + "}, {\"vulnerability\": \""
            else:
                what2write = linecache.getline(jsonResultsLocation + md5 + ".txt", critical_line)
                text2write = text2write + what2write.replace('"', '\\"')[:-1]
        if hasM1:
            text2write = text2write + "\", "
            text2write = text2write + "\"details\": \"\", \"severity\": \"Critical\", \"detectedby\": [\"Androbugs\"],"
            text2write = text2write + "\"feedback\": [{\"url\":\"\"}, {\"video\":\"\"}, {\"book\":\"\"}, {\"other\":\"\"}]"
            text2write = text2write + "}]"
            json_file.write(text2write)
            # print(text2write)
            json_file.write(",")
        # json_file.write("\"M2\": [")
        text2write = ""
        is_first = True
        for warning_line in warning:
            if warning_line == 'Warning' and is_first:
                json_file.write("\"M2\": [")
                text2write = text2write + "{\"vulnerability\": \""
                is_first = False
                hasM2 = True
                continue
            if warning_line == 'Warning' and not is_first:
                text2write = text2write + "\", "
                text2write = text2write + "\"details\": \"\", \"severity\": \"Warning\", \"detectedby\": [\"Androbugs\"],"
                text2write = text2write + "\"feedback\": [{\"url\":\"\"}, {\"video\":\"\"}, {\"book\":\"\"}, {\"other\":\"\"}]"
                text2write = text2write + "}, {\"vulnerability\": \""
            else:
                what2write = linecache.getline(jsonResultsLocation + md5 + ".txt", warning_line)
                text2write = text2write + what2write.replace('"', '\\"')[:-1]
        if hasM2:
            text2write = text2write + "\", "
            text2write = text2write + "\"details\": \"\", \"severity\": \"Critical\", \"detectedby\": [\"Androbugs\"],"
            text2write = text2write + "\"feedback\": [{\"url\":\"\"}, {\"video\":\"\"}, {\"book\":\"\"}, {\"other\":\"\"}]"
            text2write = text2write + "}]"
            json_file.write(text2write)
            # print(text2write)
            json_file.write(",")
        # json_file.write("\"M3\": [")
        text2write = ""
        is_first = True
        for notice_line in notice:
            if notice_line == 'Notice' and is_first:
                json_file.write("\"M3\": [")
                text2write = text2write + "{\"vulnerability\": \""
                is_first = False
                hasM3 = True
                continue
            if notice_line == 'Notice' and not is_first:
                text2write = text2write + "\", "
                text2write = text2write + "\"details\": \"\", \"severity\": \"Notice\", \"detectedby\": [\"Androbugs\"],"
                text2write = text2write + "\"feedback\": [{\"url\":\"\"}, {\"video\":\"\"}, {\"book\":\"\"}, {\"other\":\"\"}]"
                text2write = text2write + "}, {\"vulnerability\": \""
            else:
                what2write = linecache.getline(jsonResultsLocation + md5 + ".txt", notice_line)
                text2write = text2write + what2write.replace('"', '\\"')[:-1]
        if hasM3:
            text2write = text2write + "\", "
            text2write = text2write + "\"details\": \"\", \"severity\": \"Critical\", \"detectedby\": [\"Androbugs\"],"
            text2write = text2write + "\"feedback\": [{\"url\":\"\"}, {\"video\":\"\"}, {\"book\":\"\"}, {\"other\":\"\"}]"
            text2write = text2write + "}]"
            json_file.write(text2write)
            # print(text2write)
            json_file.write(",")
        # json_file.write("\"M4\": [")
        text2write = ""
        is_first = True
        for info_line in info:
            if info_line == 'Info' and is_first:
                json_file.write("\"M4\": [")
                text2write = text2write + "{\"vulnerability\": \""
                is_first = False
                hasM4 = True
                continue
            if info_line == 'Info' and not is_first:
                text2write = text2write + "\", "
                text2write = text2write + "\"details\": \"\", \"severity\": \"Info\", \"detectedby\": [\"Androbugs\"],"
                text2write = text2write + "\"feedback\": [{\"url\":\"\"}, {\"video\":\"\"}, {\"book\":\"\"}, {\"other\":\"\"}]"
                text2write = text2write + "}, {\"vulnerability\": \""
            else:
                what2write = linecache.getline(jsonResultsLocation + md5 + ".txt", info_line)
                text2write = text2write + what2write.replace('"', '\\"')[:-1]
        if hasM4:
            text2write = text2write + "\", "
            text2write = text2write + "\"details\": \"\", \"severity\": \"Critical\", \"detectedby\": [\"Androbugs\"],"
            text2write = text2write + "\"feedback\": [{\"url\":\"\"}, {\"video\":\"\"}, {\"book\":\"\"}, {\"other\":\"\"}]"
            text2write = text2write + "}"
            # print(text2write)
            json_file.write(text2write)
            json_file.write("]")
        if hasM5:
            json_file.write(", \"M5\": [")
            json_file.write("],")
        if hasM6:
            json_file.write(", \"M6\": [")
            json_file.write("],")
        if hasM7:
            json_file.write(", \"M7\": [")
            json_file.write("],")
        if hasM8:
            json_file.write(", \"M8\": [")
            json_file.write("],")
        if hasM9:
            json_file.write(", \"M9\": [")
            json_file.write("],")
        if hasM10:
            json_file.write(", \"M10\": [")
            json_file.write("]")
        json_file.write("}")
        # json_file.write("}")

    def build_scan_format(self, md5):
        print("plugin_Androbugs: trying to read " + jsonResultsLocation + md5 + ".txt")
        with open(jsonResultsLocation + md5 + ".txt", "r") as json_file:
            read_content = json.load(json_file)

        data = {}
        data['results'] = []

        # data_vuln_level ={}
        # data_vuln_level['vulnerabilities&level'] = []

        # data_level_for_apk = {}
        # data_level_for_apk['levelsForApk'] = []

        # info = 0
        # notice = 0
        # warning = 0
        # critical = 0

        for x in read_content:
            if not x['level'].lower() == 'info':
                data['results'].append({
                    'vulnerability': x['vulnerability'],
                    'details': x['details'],
                    'severity': x['level'],
                    'detectedby': 'Androbugs',
                    'feedback': [{"url": "Nothing to show"},
                                 {"video": "Nothing to show"},
                                 {"book": "Nothing to show"},
                                 {"other": "Nothing to show"}]
                })

            # data_vuln_level['vulnerabilities&level'].append({
            #    'vulnerability': x['tag'],
            #    'severity': x['level'],
            # })

            # if 'Info' in x['level']:
            #    info += 1
            # if 'Notice' in x['level']:
            #    notice += 1
            # if 'Warning' in x['level']:
            #    warning += 1
            # if 'Critical' in x['level']:
            #    critical += 1

        # data_level_for_apk['levelsForApk']=({
        #    'Info':info,
        #    'Notice': notice,
        #    'Warning': warning,
        #    'Critical': critical
        # })

        with open(jsonResultsLocation + md5 + ".json", "w") as save_file:
            json.dump(data, save_file)

        # with open(jsonResultsLocationVulnLevel + md5 + ".json", "a") as save_file:
        #    json.dump(data_vuln_level, save_file)

        # with open(jsonResultsLocationLevels + md5 + ".json", "a") as save_file:
        #    json.dump(data_level_for_apk, save_file)

    def run(self, apk_file, md5, package=''):
        print(pluginName + ": Running the Androbugs plugin!...")
        log.debug(pluginName + ": Running the Androbugs plugin!...")
        # test the existence of the results directory
        if not os.path.exists(jsonResultsLocation):
            os.system("mkdir " + jsonResultsLocation)
        # if not os.path.exists(jsonResultsLocationVulnLevel):
        #   os.system("mkdir " + jsonResultsLocationVulnLevel)
        # if not os.path.exists(jsonResultsLocationLevels):
        #   os.system("mkdir " + jsonResultsLocationLevels)

        # don't know why, but Androbugs requires running from the APK dir
        # print("ANDROBUGS cd " + apkLocation)
        # os.system("cd " + apkLocation)
        if apk_file[-4:] == ".apk":
            print(pluginName + ": Running on -> " + apk_file)
            log.debug(pluginName + ": Running on -> " + apk_file)
            if package == '':
                print(pluginName + ": Executing -> " + config['GENERAL'][
                    'python2cmd'] + " " + androbugsLocation + "androbugs.py -v -f " + apk_file + " --md5file " + md5 + " -o " + jsonResultsLocation)
                log.debug(pluginName + ": Executing -> " + config['GENERAL'][
                    'python2cmd'] + " " + androbugsLocation + "androbugs.py -v -f " + apk_file + " --md5file " + md5 + " -o " + jsonResultsLocation)
            else:
                print(pluginName + ": Executing -> " + config['GENERAL'][
                    'python2cmd'] + " " + androbugsLocation + "androbugs.py -v -f " + apk_file + " --package " + package + " -o " + jsonResultsLocation)
                log.debug(pluginName + ": Executing -> " + config['GENERAL'][
                    'python2cmd'] + " " + androbugsLocation + "androbugs.py -v -f " + apk_file + " --package " + package + " -o " + jsonResultsLocation)
            # run the tool
            # ----- Start Time ------
            startTime = datetime.datetime.now()
            if package == '':
                os.system(config['GENERAL'][
                              'python2cmd'] + " " + androbugsLocation + "androbugs.py -v -f " + apk_file + " --md5file " + md5 + " -o " + jsonResultsLocation)
            else:
                os.system(config['GENERAL'][
                              'python2cmd'] + " " + androbugsLocation + "androbugs.py -v -f " + apk_file + " --package " + package + " -o " + jsonResultsLocation)
            # this tool produces a text-based output... we need to consider what to do with this
            # convert to JSON
            # self.convert_to_json(md5)
            # self.convert_to_new_json(md5)
            if package == '':
                self.build_scan_format(md5)
                # have also the information registered on the database
                db.insert_results(md5, pluginName, jsonResultsLocation + md5 + ".json", 0,
                                  "NOT YET IN THE FINAL FORMAT")
            else:
                self.build_scan_format(package)
                # have also the information registered on the database
                db.insert_results(package, pluginName, jsonResultsLocation + package + ".json", 0,
                                  "NOT YET IN THE FINAL FORMAT")

            endTime = datetime.datetime.now()

            dir = './apkTimeAnalysis'
            if not os.path.exists(dir):
                os.system("mkdir " + dir)

            if package == '':
                data = md5 + ' ' + pluginName + ' ' + str(endTime - startTime) + '\n'
            else:
                data = package + ' ' + pluginName + ' ' + str(endTime - startTime) + '\n'

            with open(dir + '.txt', 'a') as f:
                f.write(data)

            # add vulnerability and level information to database
            # db.insert_results_vullevel(md5, pluginName, jsonResultsLocationVulnLevel + md5 + ".json", 0, "TRY TO SEE BETTER WAY")
            # add level information to database
            # db.insert_results_levels(md5, pluginName, jsonResultsLocationLevels + md5 + ".json", 0, "TRY TO SEE BETTER WAY")
