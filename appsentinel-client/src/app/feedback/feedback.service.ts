import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Apk } from './apk.model'
import { Observable } from 'rxjs'

@Injectable({
  providedIn: 'root'
})
export class FeedbackService {

  private readonly SERVER_ENDPOINT = 'http://localhost:5000/vulnerabilities/apks/list'

  constructor(private httpClient: HttpClient) { }

  getApksList(): Observable<Apk[]> {
    return this.httpClient
    .get<Apk[]>(this.SERVER_ENDPOINT);
    
  }
}
