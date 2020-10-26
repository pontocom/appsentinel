import { Component, OnInit } from '@angular/core';
import { Apk } from '../models/apk.model';
import { FeedbackService } from '../feedback.service';

@Component({
  selector: 'app-feedback-list',
  templateUrl: './feedback-list.component.html',
  styleUrls: ['./feedback-list.component.css']
})
export class FeedbackListComponent implements OnInit {

  apks: Apk[]
  headers = ['#', 'icon', 'name', 'notices','warnings','criticals', 'inspect']
  
  constructor(private feedbackService: FeedbackService) { }

  ngOnInit(): void {
    this.feedbackService.getApksList().subscribe(
      data => this.toApk(data), 
      (error) => console.log(error)
    );
  }

  addApkInfo(data: any): Object {
    const obj = new Object();
    obj['appName'] = data.data.name;
    obj['iconPath'] = data.data.icon;
    obj['package'] = data.data.package;
    obj['filesize'] = data.data.size;
    return obj;
  }

  async toApk(data: Object) {
    this.apks = new Array()
    const jsonData = JSON.stringify(data)
    let obj = JSON.parse(jsonData);
    console.log(obj.list)
    console.log('Data from service: '+obj.list);
    obj.list.forEach(async element => {
      const apk = new Apk()
      apk.md5 = element.apk_md5;
      let apkInfo = new Object();
      console.log('The list of levels: '+element.vulnerability_levels);

      await this.feedbackService.getApkMetaData(apk.md5).then(
        data => apkInfo = this.addApkInfo(data),
        (error) => console.log(error)
      );
      this.delay(9000);
      apk.appName = apkInfo['appName'];
      apk.iconPath = apkInfo['iconPath'];
      apk.package = apkInfo['package'];
      apk.filesize = apkInfo['filesize'];


      element.vulnerability_levels.forEach(elementItem => {
        console.log('what is happening here: '+Object.keys(elementItem))
        switch(Object.keys(elementItem)[0]){
          case 'Notice': {
            apk.notice = elementItem.Notice;
          }
          case 'Warning': {
            apk.warning = elementItem.Warning;
          }
          case 'Critical': {
            apk.critical = elementItem.Critical;
          }
        }
      });
      console.log(apkInfo);
      
      this.apks.push(apk);      
    })
    console.log(this.apks)
  }

  delay(ms: number) {
    return new Promise( resolve => setTimeout(resolve, ms) );
  }
}
