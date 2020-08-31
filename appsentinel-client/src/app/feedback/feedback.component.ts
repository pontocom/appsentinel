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
    data.list.forEach(element => {
      const apk = new Apk()
      apk.md5 = element.apk_md5
      element.vulnerability_levels.forEach(elementItem => {
        if(elementItem == 'Notice')
        apk.notice = elementItem.Info
        apk.warning = elementItem.Warning
        apk.critical = elementItem.Critical
      })
      
      this.apks.push(apk)
      
    })
    console.log(this.apks)
    
    

  }

}
