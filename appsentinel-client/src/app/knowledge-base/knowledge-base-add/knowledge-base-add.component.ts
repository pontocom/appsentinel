import { Component, OnInit } from '@angular/core';
import { KnowledgeBaseService } from '../knowledge-base.service';


@Component({
  selector: 'app-knowledge-base-add',
  templateUrl: './knowledge-base-add.component.html',
  styleUrls: ['./knowledge-base-add.component.css']
})
export class KnowledgeBaseAddComponent implements OnInit {

  category = '';
  keywords = '';
  links = "";
  books = '';
  articles = '';
  responseMessage : string = '';

  constructor(private knowledgeBaseService: KnowledgeBaseService) { }

  ngOnInit(): void {
  }

   onSave(){
  //   // Dont forget about validations, specialy to avoid security problems

    
    this.knowledgeBaseService.postKnowledgeBase(this.category, this.keywords, this.links, this.books, this.articles).subscribe(response => {
      const responseData = JSON.stringify(response)
      const obj = JSON.parse(responseData)
      this.responseMessage = obj.message;
      console.log(responseData)
    })
    
    
   }

}
