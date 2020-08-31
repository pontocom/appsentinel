import { Component, OnInit } from '@angular/core';
import { HomeService } from '../home.service';  

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  apkFileToUpload: File = null;

  constructor(private homeService: HomeService) { }

  ngOnInit(): void {
  }

  handleFileInput(files: FileList) {
    this.apkFileToUpload = files.item(0);
  }

  onAnalyze() {
    console.log('Start Analyzing ' + this.apkFileToUpload.name)
    this.homeService.postFile(this.apkFileToUpload).subscribe(data => {
      // do something, if upload success
      console.log('SUCESS');
      }, error => {
        console.log(error);
      });
  }

}
