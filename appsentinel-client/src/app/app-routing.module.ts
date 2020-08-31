import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { FeedbackComponent } from './feedback/feedback.component';


const routes: Routes = [
  { path: 'core', loadChildren: './core/core.module#CoreModule' },
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'feedback', component: FeedbackComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
