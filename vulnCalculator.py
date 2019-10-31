import database as db
import json
import configparser

def caclculate(md5):

    notice_score = 0.1
    warning_score = 0.5
    critical_score = 1
    count_values = 0

    with open('json_results/Final_Output/feedback_levels/'+ md5 + ".json", "r") as json_file:
        read_content = json.load(json_file)
    
    if read_content:
        for level, value in read_content['levelsForApk'].items():
            if level == 'Notice':
                notice_score = notice_score * float(value)
                count_values += value
            if level == 'Warning':
                warning_score = warning_score * float(value)
                count_values += value
            if level == 'Critical':
                critical_score = critical_score * float(value)
                count_values += value

    final_score = (notice_score+warning_score+critical_score)/count_values
    
    return final_score

