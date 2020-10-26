import { Component, OnInit, Input } from '@angular/core';
import { Apk } from '../models/apk.model';
import { FeedbackService } from '../feedback.service';
import { ActivatedRoute } from '@angular/router';
import { JsonPipe } from '@angular/common';
import { stringify } from 'querystring';
import { ApkFeedback } from '../models/apk-feedback.model';
import { Vulnerability } from '../models/vulnerability.model';
import { VulnerabilityFeedback } from '../models/vulnerability-feedback.model';
import { ApkLevel } from '../models/apk-level.model';
import * as CanvasJS from '../../../assets/canvasjs.min';

@Component({
  selector: 'app-feedback-detail',
  templateUrl: './feedback-detail.component.html',
  styleUrls: ['./feedback-detail.component.css']
})

export class FeedbackDetailComponent implements OnInit {

  @Input() apkSelected: Apk;
  public showModal: boolean = false;
  public showModal2: boolean = false;

  apkMd5: string;
  apkFeedbackByCategories: ApkFeedback[];
  apkLevel: ApkLevel;
  showReport: boolean;

  // Shitty way to display level summary but it works 
  detections = {};
  vuln_scores = {};
  weigth_by_tool = {};
  detected_high_weigthed_vulns: number;

  categories = [
    {
      item: {
        cat: 'M1',
        description: 'Improper platform usage',
        vulnerabilities: 0
      }
    },
    {
      item: {
        cat: 'M2',
        description: 'Insecure data storage',
        vulnerabilities: 0
      }
    },
    {
      item: {
        cat: 'M3',
        description: 'Insecure Communication',
        vulnerabilities: 0
      }
    },
    {
      item: {
        cat: 'M4',
        description: 'Insecure Authentication',
        vulnerabilities: 0
      }
    },
    {
      item: {
        cat: 'M5',
        description: 'Insufficient Cryptography',
        vulnerabilities: 0
      }
    },
    {
      item: {
        cat: 'M6',
        description: 'Insecure Authorization',
        vulnerabilities: 0
      }
    },
    {
      item: {
        cat: 'M7',
        description: 'Client Code Quality',
        vulnerabilities: 0
      }
    },
    {
      item: {
        cat: 'M8',
        description: 'Code Tampering',
        vulnerabilities: 0
      }
    },
    {
      item: {
        cat: 'M9',
        description: 'Reverse Engineering',
        vulnerabilities: 0
      }
    },
    {
      item: {
        cat: 'M10',
        description: 'Extraneous Functionality',
        vulnerabilities: 0
      }
    },
  ]

  summary = {
    "detected_by_each_tool": {
      "details": "Each tool has its own impact in the final App Risk Score, vulnerabilities found by the most weigthed tool will add more impact.",
      "detections": {},
      "vuln_socres": {
        "androbugs": [],
        "droidstatx": [],
        "super": []
      },
      "weigth_by_tool": {}
    },
    "high_weigthed_vulns": {
      "details": "this vulnerabilities have more impact in the App Risk Score, they have a CVSS greater than 7.0 and they are detected by the majority of the available scanning tools",
      "detected": 0
    },
    "summary": "This score is achived accordingly to the number, type and severity of the detected vulnerabilities and by wich tool detects those vulnerabilities."
  }

  constructor(private feedbackService: FeedbackService, private route: ActivatedRoute) { 
    this.showReport=false;
  }

  async ngOnInit() {
    console.log(this.showReport)
    this.apkMd5 = JSON.stringify(this.route.params['value']['md5']);
    this.apkMd5 = this.apkMd5.split('"').join('');
    console.log('MD5: ' + this.apkMd5);
    await this.feedbackService.getApkFeedback(this.apkMd5).then(
      data => this.toFeedback(data),
      (error) => console.log(error)
    );
    await this.feedbackService.getApkLevel(this.apkMd5).then(
      data => this.toLevel(data),
      (error) => console.log(error)
    )
    this.createChart();
  }

  toLevel(data: any) {
    this.apkLevel = new ApkLevel();
    const jsonData = JSON.stringify(data);
    let obj = JSON.parse(jsonData);
    if (obj.status === 'OK') {
      console.log('Value of this app: ' + obj.value);
      this.apkLevel.value = obj.value;
      this.apkLevel.summary = obj.summary;
      this.populateSummary(this.apkLevel.summary);

    }
  }
  populateSummary(summary: JSON) {
    const jsonData = JSON.stringify(summary);
    let obj = JSON.parse(jsonData);
    this.detections = obj.detected_by_each_tool.detections;
    this.vuln_scores = obj.detected_by_each_tool.vuln_socres;
    this.weigth_by_tool = obj.detected_by_each_tool.weigth_by_tool;
    this.detected_high_weigthed_vulns = obj.high_weigthed_vulns.detected;
  }

  toFeedback(data: any): void {
    this.apkFeedbackByCategories = new Array();
    const categories = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9', 'M10'];
    const jsonData = JSON.stringify(data);
    let obj = JSON.parse(jsonData);
    let iterator = 0;
    for (let category of categories) {
      console.log('Current category: ' + category);
      const apkFeedback = new ApkFeedback();
      apkFeedback.OWASPCategory = category;
      let vulnerabilities = new Array<Vulnerability>();
      this.categories[iterator].item.vulnerabilities = obj[category].length;
      obj[category].forEach(element => {
        const vulnerability = new Vulnerability();
        vulnerability.description = element.vulnerability;
        vulnerability.detailedDescreption = element.details;
        vulnerability.detectedby = element.detectedby;
        vulnerability.severity = element.severity;
        vulnerability.cvss = 5.3;
        vulnerability.vectorString = "CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L";
        const vulnerabilityFeedback = new VulnerabilityFeedback();
        vulnerabilityFeedback.book = element.feedback.book;
        vulnerabilityFeedback.url = element.feedback.url;
        vulnerabilityFeedback.video = element.feedback.video;
        vulnerabilityFeedback.other = element.feedback.other;
        vulnerability.feedback = vulnerabilityFeedback;
        vulnerabilities.push(vulnerability);
      });
      apkFeedback.detailedFeedback = vulnerabilities;
      this.apkFeedbackByCategories.push(apkFeedback);
      iterator++;
    }
  }

  goToReport(option: boolean){
    if(option===true)
      this.showReport = true;
    else
      this.showReport = false;
  }

  createChart(){
    let dataPointsTmp = new Array<Object>();
    this.apkFeedbackByCategories.forEach(element => {
      dataPointsTmp.push({y: element.detailedFeedback.length, label: element.OWASPCategory})
    });
    console.log(dataPointsTmp)
    let chart = new CanvasJS.Chart("chartContainer", {
      animationEnabled: true,
      exportEnabled: false,
      title: {
        text: "Vulnerabilities by OWASP TOP 10"
      },
      data: [{
        type: "column",
        dataPoints: dataPointsTmp
      }]
    });

    let chartBySeverity = new CanvasJS.Chart("chartBySeverity", {
      theme: "light2",
      animationEnabled: true,
      exportEnabled: false,
      title: {
        text: "Vulnerabilities by severity"
      },
      data: [{
        type: "pie",
        showInLegend: true,
        toolTipContent: "<b>{name}</b>: {y} (#percent%)",
        indexLabel: "{name} - #percent%",
        dataPoints: [
          { y: 450, name: "Notice" },
          { y: 120, name: "Warning" },
          { y: 300, name: "Critical" }
        ]
      }]
    });
      
    chart.render();
    chartBySeverity.render();
  }
}
