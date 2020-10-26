import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpParams } from '@angular/common/http'
import { KeywordInfo } from './keyword-info.model';
import { ɵangular_packages_platform_browser_platform_browser_k } from '@angular/platform-browser';



@Injectable({
  providedIn: 'root'
})
export class KnowledgeBaseService {

  private readonly SERVER_ENDPOINT = 'http://localhost:5000/knowledgeBase/content'

  constructor(private httpClient: HttpClient) { }

  showKnowledgeBase(): Observable<KeywordInfo[]>{
    return this.httpClient
    .get<KeywordInfo[]>(this.SERVER_ENDPOINT);
  }

  postKnowledgeBase(category: string, keywords: string,link: string, book: string, article : string) {
    const endpoint = 'http://localhost:5000/knowledgeBase/add'
    const httpOptions = link? { 
      params: new HttpParams()
      .set('category', category)
      .append('keyword', keywords)
      .append('link', link)
      .append('book',book)
      .append('article', article)
    } : {};
    console.log('Parameters: '+httpOptions.params)
    return this.httpClient
      .post(endpoint, null, httpOptions)
  }
  
  
}
