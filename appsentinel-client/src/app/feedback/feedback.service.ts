import { Injectable, EventEmitter} from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ApkFeedback } from './models/apk-feedback.model'
import { Apk } from './models/apk.model'
import { Observable } from 'rxjs'
import { ApkLevel } from './models/apk-level.model';

@Injectable({
  providedIn: 'root'
})
export class FeedbackService {

  private readonly SERVER_ENDPOINT = 'http://localhost:5000/';
  private readonly GET_APK_METADA = 'http://ws75.aptoide.com/api/7/app/getMeta/apk_md5sum=';
  public apkSelected = new EventEmitter<Apk>();

  constructor(private httpClient: HttpClient) { }

  /**
   * GET all APKs that were analysed
   */
  getApksList(): Observable<Apk[]> {
    const AP = this.SERVER_ENDPOINT+'vulnerabilities/apks/list';
    return this.httpClient
    .get<Apk[]>(AP);    
  }

  /**
   * GET report analysis of the selected app
   * @param md5 
   */
  async getApkFeedback(md5: string){
    console.log('GET feedback')
    const AP = this.SERVER_ENDPOINT+'apkfeedback/'+md5;
    console.log('Fui chamado: ' +AP)
    return await this.httpClient.get<ApkFeedback[]>(AP).toPromise();
  }

  /**
   * GET ASRS of selected app
   * @param md5 
   */
  async getApkLevel(md5: string){
    console.log('GET feedback');
    const AP = this.SERVER_ENDPOINT+'vulnerabilities/levels/'+md5;
    console.log('Fui chamado: ' +AP);
    return await this.httpClient.get<ApkLevel[]>(AP).toPromise();
  }

  /**
   * TODO
   * @param md5 
   */
  async getApkMetaData(md5: string){
    const AP = this.GET_APK_METADA+md5;
    return await this.httpClient.get(AP).toPromise();
  }
}
