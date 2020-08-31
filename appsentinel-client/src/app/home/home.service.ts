import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class HomeService {
  handleError: any;

  constructor(private httpClient: HttpClient) { }

  postFile(fileToUpload: File): Observable<boolean> {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json',
        Authorization: 'my-auth-token'
      })
    };
    const endpoint = 'http://localhost:5000/apkfiles';
    const formData: FormData = new FormData();
    formData.append('fileKey', fileToUpload, fileToUpload.name);
    console.log('Endpoint: '+endpoint+'; Data: '+formData);
    return this.httpClient
      .post(endpoint, formData)
      .pipe(catchError(this.handleError('apkToAnalyze', fileToUpload)))
  }
}
