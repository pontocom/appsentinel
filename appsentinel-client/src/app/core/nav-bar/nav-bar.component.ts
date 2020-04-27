import { Component, OnInit } from '@angular/core';
import { ApksService } from '../apks.service';

@Component({
  selector: 'app-nav-bar',
  templateUrl: './nav-bar.component.html',
  styleUrls: ['./nav-bar.component.css']
})
export class NavBarComponent implements OnInit {

  constructor( private apksService: ApksService) { }

  ngOnInit(): void {
    console.log('Started');
    this.apksService.getApks();
  }

}
