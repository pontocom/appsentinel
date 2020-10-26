import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HomeModule } from './home/home.module';
import { CoreModule } from './core/core.module';
import { FormsModule } from '@angular/forms'

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { FeedbackComponent } from './feedback/feedback.component';
import { FeedbackListComponent } from './feedback/feedback-list/feedback-list.component';
import { FeedbackDetailComponent } from './feedback/feedback-detail/feedback-detail.component';
import { FeedbackItemComponent } from './feedback/feedback-list/feedback-item/feedback-item.component';
import { FeedbackReportComponent } from './feedback/feedback-detail/feedback-report/feedback-report.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatTableModule } from '@angular/material/table';
import { KnowledgeBaseComponent } from './knowledge-base/knowledge-base.component';
import { KnowledgeBaseAddComponent } from './knowledge-base/knowledge-base-add/knowledge-base-add.component';

@NgModule({
  declarations: [
    AppComponent,
    FeedbackComponent,
    FeedbackListComponent,
    FeedbackDetailComponent,
    FeedbackItemComponent,
    FeedbackReportComponent,
    KnowledgeBaseComponent,
    KnowledgeBaseAddComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HomeModule,
    NgbModule,
    CoreModule,
    BrowserAnimationsModule,
    MatTableModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
