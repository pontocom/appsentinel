import { Component, OnInit, Input } from '@angular/core';
import { Apk } from '../../models/apk.model';
import { Router } from '@angular/router';
import { FeedbackService } from '../../feedback.service';

@Component({
  selector: 'app-feedback-item',
  templateUrl: './feedback-item.component.html',
  styleUrls: ['./feedback-item.component.css']
})
export class FeedbackItemComponent implements OnInit {

  @Input() apk: Apk;
  @Input() headers: string[];

  constructor(private feedbackService: FeedbackService, private router: Router) { }

  ngOnInit(): void {}

  onSelect(): void {
    console.log('VOU ENVIAR ---> MD5: '+this.apk.md5);
    this.feedbackService.apkSelected.emit(this.apk);
  }

}
