
import json
import configparser
import databaseMG as dbMG

def caclculate(md5):

    notice = 0
    warning = 0
    critical = 0

    notice_score = 0.1
    warning_score = 0.5
    critical_score = 1
    
    count_values = 0

    #with open('json_results/final_output/feedback_vulnerability_levels/'+ md5 + ".json", "r") as json_file:
    #    read_content = json.load(json_file)

    read_content = dbMG.get_apk_vuln_level(md5)
    
    if read_content:
        if read_content[0]['results']['vulnerabilities']:
            for vulnerability in read_content[0]['results']['vulnerabilities']:
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

    return (notice_score+warning_score+critical_score)/count_values

