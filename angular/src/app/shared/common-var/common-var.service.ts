import { Injectable } from '@angular/core';
import { Subject } from 'rxjs/Subject';
import { Observable } from 'rxjs';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';

@Injectable()
export class CommonVarService {

  private userlogin: boolean = false;
  public userObservable = new Subject<boolean>();
  ediid: string = null;
  private _storage = localStorage;
  private random_minimum: number = 1;
  private random_maximum: number = 100000;
  private download_maximum: number = 2;

  processingSub = new BehaviorSubject<boolean>(false);
  showDatacartSub = new BehaviorSubject<boolean>(false);

  constructor() { }

  // setLogin(setlogin : boolean){
  //     this.userlogin = setlogin;
  // }

  // getLogin(){
  //     return this.userlogin;
  // }

  userConfig(val) {
    this.userObservable.next(val);
  }

  setEdiid(ediid: string) {
    this._storage.setItem("ediid", ediid);
  }

  getEdiid() {
    return this._storage.getItem("ediid");
  }

  getRandomMaximum() {
    return this.random_maximum;
  }

  getRandomMinimum() {
    return this.random_minimum;
  }

  getDownloadMaximum() {
    return this.download_maximum;
  }

  /**
   * Set processing flag
   **/
  setProcessing(value: boolean) {
    this.processingSub.next(value);
  }

  /**
  * Watching processing flag
  **/
  watchProcessing(): Observable<any> {
    return this.processingSub.asObservable();
  }

  /**
   * Set show-datacart flag
   **/
  setShowDatacart(value: boolean) {
    this.showDatacartSub.next(value);
  }

  /**
  * Watching show-datacart flag
  **/
  watchShowDatacart(): Observable<any> {
    return this.showDatacartSub.asObservable();
  }
}