import { Injectable } from '@angular/core';
import {Router, NavigationEnd} from '@angular/router';
import { environment } from '../../../environments/environment';
declare var gas:Function; 

@Injectable()
export class GoogleAnalyticsServiceMock {
  constructor(router: Router) {
  }
}
