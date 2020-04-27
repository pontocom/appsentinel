import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';

import { SideMenuComponent } from './side-menu/side-menu.component';
import { NavBarComponent } from './nav-bar/nav-bar.component';
import { AppRoutingModule } from '../app-routing.module';

import { ApksService } from './apks.service'


@NgModule({
  declarations: [
    SideMenuComponent,
    NavBarComponent
    ],
  imports: [
    CommonModule,
    HttpClientModule,
    AppRoutingModule
  ],
  exports: [
    AppRoutingModule,
    NavBarComponent,
    SideMenuComponent
  ],
  providers: [
    ApksService
  ]
})
export class CoreModule { }
