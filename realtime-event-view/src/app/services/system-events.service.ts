// import { MatDialog } from '@angular/material/dialog';
// import { Injectable } from '@angular/core';
// import { HubConnection, HubConnectionBuilder } from '@aspnet/signalr';
// import { Subject } from 'rxjs';
// import { environment } from '../../../../environments/environment';
// import SystemEvent from '../model/system-event.model';
// import ISystemEventResponse from '../interfaces/system-event-response.interface';
// import { SnackBarService } from './snack-bar.service';
// import { ServiceErrorDialogComponent } from 'src/app/dashboard/components/dialogs/service-error-dialog/service-error-dialog.component';
// import { LicensingIssueComponent } from 'src/app/dashboard/components/notifications-list/notification-types/licensing-issue/licensing-issue.component';
// import { LicenseExpirationDialogComponent } from 'src/app/dashboard/components/dialogs/license-expiration-dialog/license-expiration-dialog.component';
// import { DIALOG_SIZE } from 'src/app/dashboard/dashboard.constants';

// @Injectable({
//   providedIn: 'root'
// })
// export class SystemEventsService {
//   rootUrl = environment.apiHost;
//   public hubConnection: HubConnection;
//   eventsReceived = new Subject<SystemEvent>();
//   connectionEstablished = new Subject<boolean>();

//   constructor(
//     private snackBarService: SnackBarService,
//     public dialog: MatDialog
//   ) {
//     this.createConnection();
//     this.startConnection();
//   }

//   private createConnection() {
//     this.hubConnection = new HubConnectionBuilder()
//       .withUrl(this.rootUrl + '/system-event-stream', { accessTokenFactory: () => localStorage.getItem('token') })
//       .build();
//   }

//   private startConnection() {
//     this.hubConnection.start().then(() => {
//       this.dialog.closeAll();
//       console.clear();
//       this.connectionEstablished.next(true);
//       this.startStream().subscribe({
//         next: (item: ISystemEventResponse) => {
//           this.eventsReceived.next(
//             new SystemEvent(item)
//           );
//         },
//         complete: () => {
//           console.log('Completed');
//         },
//         error: (err) => {
//           this.openError();
//           console.log('Error while establishing connection... Retrying...');
//           setTimeout(() => this.startConnection(), 5000);
//         }
//       });
//     },
//       () => {
//         console.log('Error while establishing connection... Retrying...');
//         setTimeout(() => this.startConnection(), 5000);
//       });
//   }

//   startStream() {
//     return this.hubConnection.stream('GetStream');
//   }

//   openError() {
//     const dialogRef = this.dialog.open(ServiceErrorDialogComponent, {
//       width: DIALOG_SIZE.BIG,
//       disableClose: true
//     });
//     dialogRef.afterClosed().subscribe(res => {
//       if (res) {
//         location.reload();
//       }
//     });
//   }

//   // For future
//   openLicenseExpiration() {
//     const dialogRef = this.dialog.open(LicenseExpirationDialogComponent, {
//       width: '300px',
//       disableClose: true
//     });
//     dialogRef.afterClosed().subscribe(res => {

//     });
//   }

// }
