import nltk
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import database as db
import configparser
import json
import sklearn
import re
import time
import requests
import statistics
import datetime

nltk.download('punkt')
nltk.download('stopwords')

class calculatorClass:

    URL_NVD_API_ANDROID = 'https://services.nvd.nist.gov/rest/json/cves/1.0?keyword=android'
    URL_NVD_API_KEYWORD = 'https://services.nvd.nist.gov/rest/json/cves/1.0?keyword='


    # test_score_results = {}
    # test_score_results['results']=[]

    categories = ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10"]
    cve_ids = []
    cve_descriptions = []
    cve_scores = []
    cve_score_vectors = []
    final_cves = []

    cve_id = ''
    cve_score = 0.0
    cve_score_vector = ''

    vectorizer = CountVectorizer(stop_words='english')
    non_welcome_words = {'android', 'no', 'mode'}

    def __init__(self, md5):
        ''' constructor '''
        self.md5 = md5
        self.test_score_results = {}
        self.test_score_results['results'] = []
    
    def calculate_all_test(self):
        self.calculate_method_simple()
        self.calculate_method_points()
        self.calculate_method_API()

    def calculate_method_simple(self):
        start = datetime.datetime.now()

        with open('json_results/final_output/feedback_vulnerability_levels/'+ self.md5 + ".json", "r") as json_file:
            read_content = json.load(json_file)
        
        notice = 0
        warning = 0
        critical = 0
        total_vulns = 0

        notice_score = 0.1
        warning_score = 0.5
        critical_score = 1
        
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
        score = final_score * 10
        end = datetime.datetime.now()
        duration = end-start
        self.test_score_results['results'].append({
            'simple': {
                'duration':str(duration),
                'level': score
            }
        })
        return score
    
    def get_riskLevel(self, final_cves):
        return -1


    def get_exact_match_url(self, matching_string):
        URL_NVD_API_EXACTMATCH = f'https://services.nvd.nist.gov/rest/json/cves/1.0?keyword={matching_string}&isExactMatch=true'
        return URL_NVD_API_EXACTMATCH


    def get_score(self, content):
        score = 0
        score_vector = ''
        if 'baseMetricV3' not in content:
            score = content['baseMetricV2']['cvssV2']['baseScore']
            score_vector = content['baseMetricV2']['cvssV2']['vectorString']
        else:
            score = content['baseMetricV3']['cvssV3']['baseScore']
            score_vector = content['baseMetricV2']['cvssV2']['vectorString']
        return [score, score_vector]


    def is_exact_match(self, n_results):
        # TODO TODO TODO commented for test pruposes !!!!!!!!!!!!!!!!!!!!!
        if n_results > 0:
            return True
        else:
            return False


    def get_results_info(self, response_content):
        if response_content['totalResults'] == 1:
            print('Single result found!!')
            self.cve_ids.append(response_content['result']['CVE_Items'][0]['cve']['CVE_data_meta']['ID'])
            print('CVE: '+self.cve_ids[0])
            for details in response_content['result']['CVE_Items'][0]['cve']['description']['description_data']:
                self.cve_descriptions.append(details['value'])
            if 'impact' in response_content['result']['CVE_Items'][0]:
                results = self.get_score(response_content['result']['CVE_Items'][0]['impact'])
                self.cve_scores.append(results[0])
                self.cve_score_vectors.append(results[1])
                print('Score: '+str(self.cve_scores[0]))
        elif response_content['totalResults'] > 0:
            print('Total results found: ' + str(response_content['totalResults']))
            for item in response_content['result']['CVE_Items']:
                self.cve_ids.append(item['cve']['CVE_data_meta']['ID'])
                for details in item['cve']['description']['description_data']:
                    self.cve_descriptions.append(details['value'])
                    if 'impact' in item:
                        results = self.get_score(item['impact'])
                        self.cve_scores.append(results[0])
                        self.cve_score_vectors.append(results[1])
                    else:
                        self.cve_scores.append(0.0)
                        self.cve_score_vectors.append('ND')


    def get_similar_feature(self, features):
        lowest_distance = 1000
        count = 0
        position = 0
        for cve in features:
            # print('\n'+str(lowest_distance)+'\n')
            distance = euclidean_distances(features[len(features)-1], cve)
            if distance == 0:
                count += 1
                continue
            else:
                if distance < lowest_distance:
                    lowest_distance = distance
                    position = count
                    count += 1

                else:
                    count += 1
                    continue
        return position


    def is_int(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False


    def calculate_method_API(self):
        start = datetime.datetime.now()

        with open('json_results/final_output/feedback/'+ self.md5 + ".json", "r") as json_file:
            read_content = json.load(json_file)
        
        if read_content:
            for cat in self.categories:
                print('\nStarting in category: '+cat+'\n')
                iterator = 0
                # Get the vulnerability name and details from appsentinel output
                for vuln in read_content[cat]:
                    # Reset all reusable variables
                    self.cve_ids.clear()
                    self.cve_descriptions.clear()
                    self.cve_scores.clear()
                    self.cve_score_vectors.clear()
                    cve_id = ''
                    cve_score = 0.0
                    cve_score_vector = ''
                    name = vuln['vulnerability']
                    vulnerability_name = re.sub(r"[^a-zA-Z0-9]+", ' ', name)
                    vulnerability_details = re.sub(r"[^a-zA-Z0-9]+", ' ', vuln['details'])

                    if vulnerability_details == 'nothing':
                        vulnerability_details = vulnerability_name

                    matching_string = vulnerability_name.replace(' ', '+')
                    url = self.get_exact_match_url(matching_string)
                    response_content = requests.get(url).json()
                    print('Matching string: '+ matching_string)
                    if self.is_exact_match(response_content['totalResults']):
                        print('EXACT MATCH!!!')
                        self.get_results_info(response_content)
                    else:
                        vulnerability_name_tokens = word_tokenize(vulnerability_name)
                        tokens_without_sw = [word for word in vulnerability_name_tokens if not word in stopwords.words()]
                        # Lets split the vulnerability name in single words and use them as keywords
                        words = tokens_without_sw
                        print('\n'+str(words)+'\n')
                        for word in words:
                            if word.lower() in self.non_welcome_words or self.is_int(word):
                                continue
                            resp_content = requests.get(self.URL_NVD_API_KEYWORD + word).json()
                            if resp_content['totalResults'] == 0:
                                continue
                            else:
                               self. get_results_info(resp_content)
                    # invlude the vulnerability details in the descriptions array and then make the comparsion
                    self.cve_descriptions.append(vulnerability_details)
                    features = self.vectorizer.fit_transform(self.cve_descriptions).todense()
                    position = self.get_similar_feature(features)
                    print('Position: '+str(position)+' ;length cve_scores: '+str(len(self.cve_scores)))
                    iterator += 1
                    self.final_cves.append(self.cve_scores[position])
        end = datetime.datetime.now()
        mean = statistics.mean(self.final_cves)
        duration = end-start
        self.test_score_results['results'].append({
            'API': {
                'duration':str(duration),
                'level': mean
            }
        })

    # Points method scoring calculation
    def calculate_method_points(self):
        start = datetime.datetime.now()
        with open('json_results/final_output/feedback_vulnerability_levels/'+ self.md5 + ".json", "r") as json_file:
            read_content = json.load(json_file)
        
        notice = 0
        warning = 0
        critical = 0
        total_vulns = 0

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

        if total_vulns == 1:
            final_score = -0.5
        elif total_vulns < 5:
            final_score = 0.5
        elif total_vulns < 10:
            final_score = 1
        elif total_vulns < 15:
            final_score = 1.5
        elif total_vulns < 20:
            final_score = 2
        elif total_vulns < 25:
            final_score = 2.5
        elif total_vulns < 30:
            final_score = 3
        else :
            final_score = 3.5

        final_score = final_score + (notice/total_vulns)
        final_score = final_score + (warning/total_vulns) * 3
        final_score = final_score + (critical/total_vulns) * 6

        if final_score > 10:
            final_score = 10
        score = round(final_score, 2)
        end = datetime.datetime.now()
        duration = end-start
        self.test_score_results['results'].append({
            'points':{
                'duration': str(duration),
                'level':score
            }
        })