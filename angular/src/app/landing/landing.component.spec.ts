// import { async, ComponentFixture, TestBed } from '@angular/core/testing';
// import { RouterTestingModule } from '@angular/router/testing'; 
// import { DebugElement } from '@angular/core';
// import { By } from '@angular/platform-browser';

// import { LandingComponent } from './landing.component';
// import { MenuModule,DialogModule,FieldsetModule } from 'primeng/primeng';
// import {TreeModule,TreeNode} from 'primeng/primeng';

// import { Collaspe } from './collapseDirective/collapse.directive';
// import {DescriptionComponent} from './description.component';
// import { MetadataComponent } from './metadata/metadata.component';
// import { FileDetailsComponent } from './fileDetails/filedetails.component';
// // import { Ng2StickyModule } from 'ng2-sticky';
// import { FormsModule } from '@angular/forms';
// import { CUSTOM_ELEMENTS_SCHEMA,NO_ERRORS_SCHEMA } from '@angular/core';
// import { HttpModule } from '@angular/http';
// import { HttpClientModule } from '@angular/common/http'; 
// import { SearchService } from '../shared/index';
// import { Observable } from 'rxjs/Observable';
// import 'rxjs/add/observable/from';
// import {
//   MockBackend,
//   MockConnection
//  } from '@angular/http/testing';
//  import { SearchResolve } from './search-service.resolve';



//   describe('Landing Component', () => {
//     let component: LandingComponent;
//     let fixture: ComponentFixture<LandingComponent>;
//     let de: DebugElement;
//     let sampleData = {"_id":{"timestamp":1504895173,"machineIdentifier":6147944,"processIdentifier":294,"counter":15850762,"date":1504895173000,"time":1504895173000,"timeSecond":1504895173},"_schema":"https://www.nist.gov/od/dm/nerdm-schema/v0.1#","topic":[{"scheme":"https://www.nist.gov/od/dm/nist-themes/v1.0","tag":"Information Technology","@type":"Concept"},{"scheme":"https://www.nist.gov/od/dm/nist-themes/v1.0","tag":"Information Technology: Biometrics","@type":"Concept"}],"references":[{"refType":"IsReferencedBy","_extensionSchemas":["https://www.nist.gov/od/dm/nerdm-schema/v0.1#/definitions/DCiteDocumentReference"],"@id":"#ref:nist-srd/SD4/readme_sd04.pdf","@type":"deo:BibliographicReference","location":"https://s3.amazonaws.com/nist-srd/SD4/readme_sd04.pdf"}],"_extensionSchemas":["https://www.nist.gov/od/dm/nerdm-schema/pub/v0.1#/definitions/PublicDataResource"],"landingPage":"https://www.nist.gov/srd/nist-special-database-4","dataHierarchy":[{"filepath":"NISTSpecialDatabase4GrayScaleImagesofFIGS.zip"},{"filepath":"HashNISTSpecialDatabase4GrayScaleImagesofFIGS.txt"}],"title":"NIST 8-Bit Gray Scale Images of Fingerprint Image Groups (FIGS) - NIST Special Database 4","theme":["Information Technology","Biometrics"],"inventory":[{"forCollection":"","descCount":2,"childCollections":[],"childCount":2,"byType":[{"descCount":2,"forType":"dcat:Distribution","childCount":2},{"descCount":2,"forType":"nrdp:DataFile","childCount":2}]}],"programCode":["006:052"],"@context":["https://www.nist.gov/od/dm/nerdm-pub-context.jsonld",{"@base":"ark:/88434/mds0157g0g"}],"description":["This NIST database of fingerprint images contains 2,000 8-bit gray scale fingerprint image pairs. Each image is 512-by-512 pixels (32 rows of white space at the bottom), scanning resolution was 19.7 pixels per millimeter, and classified using one of the five following classes: A=Arch, L=Left Loop, R=Right Loop, T=Tented Arch, W=Whorl. The database is evenly distributed over each of the five classifications with 400 fingerprint pairs from each class. \r\n\r\n The images are PNG formatted with a text file that accompanies each image that gives the Gender, Class and History information extracted from the ANSI/NIST-ITL formatted (AN2) file. \r\n\r\n It is suitable for automated fingerprint classification research, the database can be used for algorithm development or system training and testing."],"language":["en"],"bureauCode":["006:55"],"contactPoint":{"hasEmail":"mailto:patricia.flanagan@nist.gov","fn":"Patricia Flanagan"},"accessLevel":"public","@id":"ark:/88434/mds0157g0g","publisher":{"@type":"org:Organization","name":"National Institute of Standards and Technology"},"keyword":["8 bit gray scales","biometrics","finger pairs","finger print matching","finger print software","fingerprint classifications","fingerprintings","fingerprints","fingers","forensics","identification","images","law enforcement","matching","paired fingerprint images","pattern classifications","verifications"],"license":"https://www.nist.gov/open/license","modified":"2015-12-11","ediid":"FF429BC1786C8B3EE0431A570681E858219","components":[{"description":"The database consists of one zip file. The zip file holds PNG formatted image files and TXT formatted files that accompany each image that gives the Gender, Class and History information extracted from the ANSI/NIST-ITL formatted (AN2) file. There is also an RTF file that gives an explanation of the database and the directory structure. The size of the zip file 7895 MB with the extracted database being 807 MB.","format":{"description":"Zip with PNG formatted images"},"filepath":"NISTSpecialDatabase4GrayScaleImagesofFIGS.zip","mediaType":"application/zip","downloadURL":"https://s3.amazonaws.com/nist-srd/SD4/NISTSpecialDatabase4GrayScaleImagesofFIGS.zip","title":"Zip file of NIST Special Database 4","@id":"cmps/NISTSpecialDatabase4GrayScaleImagesofFIGS.zip","@type":["nrdp:DataFile","dcat:Distribution"],"_extensionSchemas":["https://www.nist.gov/od/dm/nerdm-schema/pub/v0.1#/definitions/DataFile"]},{"description":"SHA-256 hash of data download file for NIST Special Database 4","filepath":"HashNISTSpecialDatabase4GrayScaleImagesofFIGS.txt","title":"SHA-256 hash of data download file for NIST Special Database 4","mediaType":"text/plain","downloadURL":"https://s3.amazonaws.com/nist-srd/SD4/HashNISTSpecialDatabase4GrayScaleImagesofFIGS.txt","@id":"cmps/HashNISTSpecialDatabase4GrayScaleImagesofFIGS.txt","@type":["nrdp:DataFile","dcat:Distribution"],"_extensionSchemas":["https://www.nist.gov/od/dm/nerdm-schema/pub/v0.1#/definitions/DataFile"]}],"@type":["nrdp:PublicDataResource"]};
    
//     beforeEach(async(() => {
//       TestBed.configureTestingModule({
//       declarations: [ LandingComponent, Collaspe,DescriptionComponent,
//                       MetadataComponent ,FileDetailsComponent
//                     ],
//       imports:[ MenuModule,DialogModule, FormsModule, TreeModule,FieldsetModule, HttpModule ,RouterTestingModule],
//       schemas: [ CUSTOM_ELEMENTS_SCHEMA ,NO_ERRORS_SCHEMA],
//       providers: [
//         SearchService
//       ]
      
//       })
//       .compileComponents();
//     }));

//     beforeEach(() => {
//       fixture = TestBed.createComponent(LandingComponent);
//       component = fixture.componentInstance;
//       fixture.detectChanges();
//     });

//     // it('should check the landing component', async(() => {
//     //   expect(component).toBeTruthy();
//     // }));

//     it('should return one record per landing page', () => {
//       let service = TestBed.get(SearchService);
//       spyOn(service,'searchById').and.returnValue(Observable.from([[sampleData]]));
//       fixture.detectChanges();
//       expect(1).toBe(1);
//     });
// });