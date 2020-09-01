import { Component, OnInit } from '@angular/core';
import { FeedbackService } from './feedback.service';
import { Apk} from './apk.model'

@Component({
  selector: 'app-feedback',
  templateUrl: './feedback.component.html',
  styleUrls: ['./feedback.component.css']
})
export class FeedbackComponent implements OnInit {

  apks: Apk[]
  headers = ['md5', 'notice', 'warning', 'critical']

  constructor(private feedbackService: FeedbackService) { }

  ngOnInit(): void {
    this.feedbackService.getApksList().subscribe(
      data => this.toApk(data), 
      (error) => console.log(error))

  }

  toApk(data: Object): void{
    this.apks = new Array()
    const jsonData = JSON.stringify(data)
    let obj = JSON.parse(jsonData);
    console.log(obj.list)
    console.log('Data from service: '+obj.list);
    obj.list.forEach(element => {
      const apk = new Apk()
      apk.md5 = element.apk_md5
      console.log('The list of levels: '+element.vulnerability_levels)
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
            apk.critical = elementItem.Critical
          }
        }
      })
      
      this.apks.push(apk)
      
    })
    console.log(this.apks)
    
    

  }

}
