import database as db
import json
import configparser

## Testing Try to lool config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

plugin_scores={}
for section in config.sections():
    if str(section) == 'TOOL_SCORES':
        for (key, val) in config.items(section):
            plugin_scores[key]=val
print(plugin_scores)
############################
class calculatorClass:

    config = configparser.ConfigParser()
    config.read('config.ini')


    def __init__(self, md5):
        ''' constructor '''
        self.md5=md5
        self.plugin_scores={}

    def get_tools(self):
        for section in config.sections():
            if str(section) == 'TOOL_SCORES':
                for (key, val) in config.items(section):
                    self.plugin_scores[key]=val

    def calculate(self):

        notice = 0
        warning = 0
        critical = 0

        notice_score = 0.1
        warning_score = 0.5 
        critical_score = 1
        
        count_values = 0

        with open('json_results/final_output/feedback_vulnerability_levels/'+ self.md5 + ".json", "r") as json_file:
            read_content = json.load(json_file)
        
        if read_content:
            if read_content['vulnerabilities']:
                for vulnerability in read_content['vulnerabilities']:
                    if vulnerability['severity'] == 'Notice':
                        notice += 1
                    if vulnerability['severity'] == 'Warning':
                        warning += 1
                    if vulnerability['severity'] == 'Critical':
                        critical += 1
            else:
                return 0

        count_values = notice+warning+critical
        
        notice_score *= notice
        warning_score *= warning
        critical_score *= critical

        return round((notice_score+warning_score+critical_score)/count_values ,2)

