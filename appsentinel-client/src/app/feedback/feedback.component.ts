import { Component, OnInit } from '@angular/core';
import { FeedbackService } from './feedback.service';
import { Apk} from './models/apk.model'

@Component({
  selector: 'app-feedback',
  templateUrl: './feedback.component.html',
  styleUrls: ['./feedback.component.css']
})
export class FeedbackComponent implements OnInit {

  selectedAPK: Apk;

  constructor(private feedbackService: FeedbackService) { }

  ngOnInit(): void {
    this.feedbackService.apkSelected.subscribe(
      (apk: Apk) =>{
        this.selectedAPK = apk
      }
    );
  }

}
