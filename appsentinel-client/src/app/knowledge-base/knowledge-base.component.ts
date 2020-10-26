import { Component, OnInit } from '@angular/core';
import { KnowledgeBaseService } from './knowledge-base.service';
import { KeywordInfo } from './keyword-info.model'
import { Router } from '@angular/router';

@Component({
  selector: 'app-knowledge-base',
  templateUrl: './knowledge-base.component.html',
  styleUrls: ['./knowledge-base.component.css']
})
export class KnowledgeBaseComponent implements OnInit {

  keywordInfoList: KeywordInfo[]
  headers = ['category','keywords', 'links','books', 'articles']

  a = ""
  c=""

  test = ["a", "b","c"]

  add: boolean = false

  constructor(private knowledgeBaseService: KnowledgeBaseService, private router: Router) { }


  ngOnInit(): void {
    this.knowledgeBaseService.showKnowledgeBase().subscribe(
      data => this.showContent(data),
      (error) => console.log(error)
    )
  }

  onClick(): void{
    this.add = true
  }

  showContent(data: Object): void{
    //console.log(JSON.parse(JSON.stringify(data)));
    //const content = (JSON.stringify(data));
    //this.a = content[0]
    this.keywordInfoList = new Array();
    const jsonData = JSON.stringify(data)
    let obj = JSON.parse(jsonData)
    console.log(obj.Data)
    console.log('Data2 from service: '+obj.results);
    obj.results.forEach(element => {

      console.log('The knowledgebase: '+element.name)
      const keywordInfo = new KeywordInfo()
      keywordInfo.category = element.category
      keywordInfo.keywords = element.name
      keywordInfo.links = element.links
      keywordInfo.books = element.books
      keywordInfo.articles = element.articles

      
      this.keywordInfoList.push(keywordInfo)
    })
    console.log(this.keywordInfoList)
  }

}
