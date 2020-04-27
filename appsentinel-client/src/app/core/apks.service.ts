import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { map, tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ApksService {

  private readonly SERVER_ENDPOINT='http://127.0.0.1:5000/vulnerabilities/levels'

  constructor(private httpClient: HttpClient) { }


  getApks() {
    console.log(this.httpClient.get(this.SERVER_ENDPOINT))
    this.httpClient
      .get(this.SERVER_ENDPOINT)
      .subscribe(apks => {
        console.log(apks);
      });
  }
}
