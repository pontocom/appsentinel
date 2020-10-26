import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { FeedbackComponent } from './feedback/feedback.component';
import { FeedbackDetailComponent } from './feedback/feedback-detail/feedback-detail.component';


const routes: Routes = [
  { path: 'core', loadChildren: './core/core.module#CoreModule' },
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'feedback', component: FeedbackComponent},
  { path: 'feedback/detail/:md5', component: FeedbackDetailComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
