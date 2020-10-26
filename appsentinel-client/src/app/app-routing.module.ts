import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { FeedbackComponent } from './feedback/feedback.component';
import { FeedbackDetailComponent } from './feedback/feedback-detail/feedback-detail.component';

import { KnowledgeBaseComponent } from './knowledge-base/knowledge-base.component';
import { KnowledgeBaseAddComponent } from './knowledge-base/knowledge-base-add/knowledge-base-add.component';

const routes: Routes = [
  { path: 'core', loadChildren: './core/core.module#CoreModule' },
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'feedback', component: FeedbackComponent},
  { path: 'feedback/detail/:md5', component: FeedbackDetailComponent },
  { path: 'knowledge-base', component: KnowledgeBaseComponent},
  { path: 'knowledge-base/add', component: KnowledgeBaseAddComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
