import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class HomeService {

  handleError: any;

  // httpOptions = {
  //   headers: new HttpHeaders({
  //     'Content-Type':  'application/json',
  //     Authorization: 'my-auth-token'
  //   })
  // };

  constructor(private httpClient: HttpClient) { }

  postFile(fileToUpload: File): Observable<boolean> {
    const endpoint = 'http://localhost:5000/apkfiles';
    const formData: FormData = new FormData();
    formData.append('fileKey', fileToUpload, fileToUpload.name);
    console.log('Endpoint: '+endpoint+'; Data: '+formData);
    return this.httpClient
      .post(endpoint, formData)
      .pipe(catchError(this.handleError('apkToAnalyze', fileToUpload)))
  }

  postMd5(md5: string) {
    const endpoint = 'http://localhost:5000/apkscan';
    const httpOptions = md5 ? { 
      params: new HttpParams().set('md5', md5)
    } : {};
    console.log('Parameters: '+httpOptions.params)
    return this.httpClient
      .post(endpoint, null, httpOptions).subscribe(
        response => {console.log('Response: '+JSON.stringify(response))}
      )
  }
}
