import database as db
import json
import configparser
import os
import os.path
from os import path
from statistics import mean

class calculatorClass:

    config = configparser.ConfigParser()
    config.read('config.ini')

    def __init__(self, md5):
        ''' constructor '''
        self.md5=md5
        self.plugin_scores={}
        self.enabled_plugins=[]
        self.setup()
        self.notices = 0
        self.warnings = 0
        self.criticals = 0

    # Seting up the calculator, getting the enabled plugins and their correspondent scores
    def setup(self):
        # print('Setting up the Calculator')
        n_plugins=0
        enabled_plugins_name=[]

        # looking for the plugins
        pluginDir = os.path.dirname(os.path.abspath(__file__))
        for file in os.listdir(pluginDir):
            if file[0:7] == "plugin_" and file[-3:] == ".py":
                # print(file)
                # we need to do something with them... need to check if it is better to import or to spawn (decide later)
                thisPlugin = __import__(".".join(file.split(".")[0:-1]))
                # print(thisPlugin.pluginName +' is enabled:'+ str(thisPlugin.enable))
                if thisPlugin.enable and thisPlugin not in self.enabled_plugins:
                    # print('Adding '+thisPlugin.pluginName)
                    self.enabled_plugins.append(thisPlugin)
                    enabled_plugins_name.append(thisPlugin.pluginName.lower())

        print(str(self.enabled_plugins))
        print(str(enabled_plugins_name))

        for section in self.config.sections():
            if str(section) == 'TOOL_SCORES':
                for (name, val) in self.config.items(section):
                    if name in enabled_plugins_name:
                        self.plugin_scores[name]=val
                        n_plugins +=1
        print(self.plugin_scores)

    def calculate(self):

        plugin_vuln_scores={}

        try:
            with open('json_results/final_output/feedback/'+self.md5+'.json', "r") as json_file:
                        feedback_content = json.load(json_file)
            with open('dictionaries/baseKnowledge.json', "r") as json_file:
                        baseKnowledge = json.load(json_file)
        except Exception as e:
            print('ERROR in VulnCalculator: ' +e)
            print('Type od error: '+type(e))

        for category in feedback_content:
            for vuln in feedback_content[category]:
                if vuln['severity'] == 'Notice':
                    self.notices+=1
                elif vuln['severity'] == 'Warning':
                    self.warnings+=1
                else:
                    self.criticals+=1
                vuln_name = vuln['vulnerability']
                # print('Checking for '+vuln_name)
                detectedby=""
                if isinstance(vuln['detectedby'], list):
                    detectedby = []
                    for plug in vuln['detectedby']:
                        detectedby.append(plug.lower())
                else:
                    # print('IS NOT A LIST')
                    break
                    # detectedby = vuln['detectedby'].lower()  # this detectedby has to be an array
                # for detectedby as an Array
                for p in detectedby:
                    # print('checking if '+p+' is in '+str(plugin_vuln_scores))
                    if p not in plugin_vuln_scores:
                        # print('Plugin: '+p+' plug_vulns: '+str(plugin_vuln_scores))
                        # print('Adding '+p+' in plugin_vuln_scores')
                        plugin_vuln_scores[p] = []
                for plug in detectedby:
                    if plug not in plugin_vuln_scores:
                        # print('Adding '+plug+' in plugin_vuln_scores')
                        plugin_vuln_scores[plug] = []
                    with open('dictionaries/'+plug+'_dict.json', "r") as json_file:
                        plugin_dict = json.load(json_file)
                    for result in plugin_dict['results']:
                        if result['name'] == vuln_name and len(result['keywords']) > 0:
                            # print('Checking: '+vuln_name+' is equal to '+result['name'])
                            keywords=result['keywords']
                            # print('These are the keywords for this vuln: '+str(keywords))
                            for data in baseKnowledge['results']:
                                if category == data['category']:
                                    _aux = {}
                                    _aux_score = 0
                                    for score in data['scores']:
                                        # print('Comparing: '+str(keywords)+' with '+str(score['keywords']))
                                        # checking if there are more matching keywords
                                        if len(_aux)<len(set(keywords)&set(score['keywords'])):
                                            # print('NEW CANDIDATE')
                                            _aux = set(keywords)&set(score['keywords'])
                                            _aux_score = score['score']
                                        # print('Test: '+str(_aux))
                                        if keywords==score['keywords']:
                                            _aux_score = score['score']
                                            break
                                    fscore = _aux_score
                                     ## MÉTODO 2 dar um extra a vulnerabilidades criticas e warnings
                                    # print('Fscore before: '+str(fscore))
                                    # if fscore >= 7.0 and fscore < 9.0:
                                    #     fscore += 0.5
                                    # elif fscore >= 9.0:
                                    #     fscore += 1
                                    # elif fscore >= 6.0 and fscore < 7.0:
                                    #     fscore += 0.2
                                    # elif fscore >= 4.0 and fscore < 6.0:
                                    #     fscore += 0.1
                                    # print('Fscore after: '+str(fscore))
                                    # if fscore > 10.0:
                                    #     fscore = 10.0
                                    ##

                                    # Adding the score for each plugin that detected it
                                    for plugin in detectedby:
                                        plugin_vuln_scores[plugin].append(fscore)
                                    #     print('plugin_vuln_scores: '+str(plugin_vuln_scores))
                                    # print('Score: '+str(score))
                # if detectedby not in plugin_vuln_scores:
                #     plugin_vuln_scores[detectedby] = []
                # with open('dictionaries/'+detectedby+'_dict.json', "r") as json_file:
                #     plugin_dict = json.load(json_file)
                # for result in plugin_dict['results']:
                #     if result['name'] == vuln_name and len(result['keywords']) > 0:
                #         print('Checking: '+vuln_name+' is equal to '+result['name'])
                #         keywords=result['keywords']
                #         for data in baseKnowledge['results']:
                #             if category == data['category']:
                #                 for score in data['scores']:
                #                     print('Comparing: '+str(keywords)+' with '+str(score['keywords']))
                #                     if keywords==score['keywords']:
                #                         print(str(keywords)+' is equal to '+str(score['keywords']))
                #                         fscore = score['score']
                #                         plugin_vuln_scores[detectedby].append(fscore)
                #                         print('Score: '+str(score)) 
        # print('\n'+str(plugin_vuln_scores))

        #### TODO ####
        # Check how many plugins analysed the current apk and adjust the scores
        # check plugin_vuln_scores and change plugin_scores
        if len(plugin_vuln_scores) == 0:
            return 0
        
        # print('BEFORE plugin_scores: '+str(self.plugin_scores))
        if len(plugin_vuln_scores) < len(self.enabled_plugins):
            self.plugin_scores = self.adjust_plugin_scores(plugin_vuln_scores)
        #### TODO ####
        dividend_total=0
        # print('New plugin_scores '+str(self.plugin_scores))
        for plugin in plugin_vuln_scores:
            # print("\nCalculando "+plugin)
            dividend_total += (mean(plugin_vuln_scores[plugin])*0.1) * float(self.plugin_scores[plugin])
            # if len(plugin_vuln_scores[plugin]) > 0:
            #     print("Calculando "+plugin)
            #     dividend_total += (mean(plugin_vuln_scores[plugin])*0.1) * float(plugin_scores[plugin])
            # else:
            #     dividend_total += 0
        final_score = dividend_total/float(len(plugin_vuln_scores))
        
        # print("Score before ---> "+str(final_score))
        # Add bonus
        if self.criticals >= 10 or self.warnings >= 10:
            final_score = self.add_weights(final_score)            

        # print('Final Score ---> '+str(final_score))
        return round(final_score,2)

    def adjust_plugin_scores(self, plugin_vuln_scores):
        # print('\nSTARTING ADJSUTMENT')
        # print('plugin_vuln_scores: '+str(plugin_vuln_scores))
        # print('\nOld plugin scores: '+str(self.plugin_scores))
        new_plugin_scores = {}
        for plug in plugin_vuln_scores:
            # print('The plug is: '+plug)
            new_plugin_scores[plug] = self.plugin_scores[plug]
            # print('The new one! ' + str(new_plugin_scores))
        if len(new_plugin_scores) == 1:
            for plug in plugin_vuln_scores:
                new_plugin_scores[plug] = 1
        else:
            new_scores = []
            for plug in plugin_vuln_scores:
                new_scores.append(float(new_plugin_scores[plug]))
            # print(new_scores)
            bro = sum(new_scores)
            # print('The sum of new scores is: '+str(bro))
            if bro < len(plugin_vuln_scores):
                while sum(new_scores) < len(plugin_vuln_scores):
                    for i in range(len(new_scores)):
                        new_scores[i] += 0.1
                if sum(new_scores) > len(plugin_vuln_scores):
                    for i in range(len(new_scores)):
                        new_scores[i] -= 0.05
                i=0
                for plug in new_plugin_scores:
                    new_plugin_scores[plug]=new_scores[i]
                    i+=1
            else:
                while sum(new_scores) > len(plugin_vuln_scores):
                    for i in range(len(new_scores)):
                        new_scores[i] -= 0.1
                if sum(new_scores) < len(plugin_vuln_scores):
                    for i in range(len(new_scores)):
                        new_scores[i] += 0.05
                i=0
                for plug in new_plugin_scores:
                    new_plugin_scores[plug]=new_scores[i]
                    i+=1
            print(sum(new_scores))

        # print('What about now!! ' + str(new_plugin_scores))
        return new_plugin_scores
    
    def add_weights(self, final_score):
        if self.criticals >= 10:
            bonus = self.criticals * 0.01
            final_score += bonus
        if self.warnings >= 10:
            bonus = self.warnings * 0.002
            final_score += bonus
        return final_score