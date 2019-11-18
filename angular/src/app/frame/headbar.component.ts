import { Component, ElementRef } from '@angular/core';
import { AppConfig } from '../config/config';
import { CartService } from '../datacart/cart.service';
import { CartEntity } from '../datacart/cart.entity';
import { Router } from '@angular/router';
import { NotificationService } from '../shared/notification-service/notification.service';
import { EditStatusService } from '../landing/editcontrol/editstatus.service';

/**
 * A Component that serves as the header of the landing page.  
 * 
 * Features include:
 * * Set as black bar at the top of the page
 * * NIST PDR logo that links to the PDR home page (currently the SDP)
 * * PDR-wide links:
 *   * About page
 *   * Search page (the SDP)
 *   * User's Datacart
 * * Labels indicating the version and status of the PDR
 *   * this uses the badge style from bootstrap
 */
@Component({
    moduleId: module.id,
    selector: 'pdr-headbar',
    templateUrl: 'headbar.component.html',
    styleUrls: ['headbar.component.css']
})
export class HeadbarComponent {

    layoutCompact: boolean = true;
    layoutMode: string = 'horizontal';
    searchLink: string = "";
    status: string = "";
    appVersion: string = "";
    cartLength: number = 0;
    editEnabled: any;
    // ediid: any;

    constructor(
        private el: ElementRef,
        private cfg: AppConfig,
        public cartService: CartService,
        private router: Router,
        private notificationService: NotificationService,
        public editstatsvc: EditStatusService)
    {
        if (!(cfg instanceof AppConfig))
            throw new Error("HeadbarComponent: Wrong config type provided: " + cfg);
        this.searchLink = cfg.get("locations.pdrSearch", "/sdp/");
        this.status = cfg.get("status", "");
        this.appVersion = cfg.get("appVersion", "");
        this.editEnabled = cfg.get("editEnabled", "");

        this.cartService.watchStorage().subscribe(value => {
            this.cartLength = value;
        });

        // this.editControlService.watchEdiid().subscribe(value => {
        //     this.ediid = value;
        // });
    }

    /*
    *   init
    */
    ngOnInit() {
        this.cartLength = this.cartService.getCartSize();
    }

    /**
     * Return true if the user is logged in
     */
    loggedIn() {
        return Boolean(this.editstatsvc.userID);
    }

    /**
     * ensure that the data cart display is up to date
     */
    updateCartStatus() {
        this.cartService.updateCartDisplayStatus(true);
        this.cartService.setCurrentCart('cart');
    }

    /*
     *   Open about window if not in edit mode. Otherwise do nothing.
     */
    openRootPage() {
        if (!this.editstatsvc.editMode)
            window.open('/', '_self');
    }

    /*
     *   Open about window if not in edit mode. Otherwise do nothing.
     */
    openAboutPage() {
        if (!this.editstatsvc.editMode)
            window.open('/pdr/about', '_blank');
    }

    /*
     *   Open search window if not in edit mode. Otherwise do nothing.
     */
    openSearchPage() {
        if (!this.editstatsvc.editMode)
            window.open(this.searchLink, '_blank');
    }

    /*
     *   In edit mode, top menu will be disabled - text color set to grey
     */
    getMenuTextColor() {
        if (this.editstatsvc.editMode)
            return 'grey';
        else
            return 'white';
    }

    /*
     *   In edit mode, mouse cursor set to normal
     */
    getCursor() {
        if (this.editstatsvc.editMode)
            return 'default';
        else
            return 'pointer';
    }

    showUserId(){
        this.notificationService.showSuccessWithTimeout(this.editstatsvc.userID, "", 3000);
    }
}
