import { Component, OnInit } from '@angular/core';
import { HomeService } from '../home.service';  

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  apkFileToUpload: File = null;
  inputMD5 = '';

  constructor(private homeService: HomeService) { }

  ngOnInit(): void {
  }

  handleFileInput(files: FileList) {
    this.apkFileToUpload = files.item(0);
  }

  onAnalyze() {
    // Dont forget about validations, specialy to avoid security problems

    if(this.inputMD5 === ''){
      console.log('Start Analyzing ' + this.apkFileToUpload.name)
      this.homeService.postFile(this.apkFileToUpload).subscribe(data => {
        // do something, if upload success
        console.log('SUCESS');
        }, error => {
          console.log(error);
        });
    }else{
      console.log('The md5 is: '+this.inputMD5)
      this.homeService.postMd5(this.inputMD5);
    }
  }

}
