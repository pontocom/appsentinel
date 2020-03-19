import database as db
import json
import configparser

class calculatorClass:

    def __init__(self):
        ''' constructor '''

    def calculate(md5):

        notice = 0
        warning = 0
        critical = 0
        total_vulns = 0

        notice_score = 0.1
        warning_score = 0.5
        critical_score = 1

        with open('json_results/final_output/feedback_vulnerability_levels/'+ md5 + ".json", "r") as json_file:
            read_content = json.load(json_file)
        
        if read_content:
            if read_content['vulnerabilities']:
                total_vulns = len(read_content['vulnerabilities'])
                for vulnerability in read_content['vulnerabilities']:
                    if vulnerability['severity'] == 'Notice':
                        notice += 1
                    if vulnerability['severity'] == 'Warning':
                        warning += 1
                    if vulnerability['severity'] == 'Critical':
                        critical += 1
            else:
                return 0

        total_vulns = notice+warning+critical
        
        # Calculate with the simple scoring method
        
        notice_score *= notice
        warning_score *= warning
        critical_score *= critical

        final_score = round((notice_score+warning_score+critical_score)/total_vulns ,2)
        return final_score * 10

        ##############################################################################################

        # # Calculate with point system

        # if total_vulns < 5:
        #     final_score = 0.5
        # elif total_vulns < 10:
        #     final_score = 1
        # elif total_vulns < 15:
        #     final_score = 1.5
        # elif total_vulns < 20:
        #     final_score = 2
        # elif total_vulns < 25:
        #     final_score = 2.5
        # elif total_vulns < 30:
        #     final_score = 3
        # else :
        #     final_score = 3.5

        # final_score = final_score + (notice/total_vulns)
        # final_score = final_score + (warning/total_vulns) * 3
        # final_score = final_score + (critical/total_vulns) * 6

        # if final_score > 10:
        #     final_score = 10
        
        # return round(final_score, 2)