// import { MatDialog } from '@angular/material/dialog';
// import { Injectable } from '@angular/core';
// import { HubConnection, HubConnectionBuilder } from '@aspnet/signalr';
// import { Subject } from 'rxjs';
// import { SnackBarService } from './snack-bar.service';
// import { environment } from 'src/environments/environment';
// @Injectable({
//   providedIn: 'root'
// })
// export class MonitoringEventsService {

//   rootUrl = environment.apiHost;
//   public hubConnection: HubConnection;
//   eventsReceived = new Subject<any>();

//   constructor(
//     public dialog: MatDialog,
//     public snackBarService: SnackBarService
//   ) {
//     this.createConnection();
//     this.startConnection();
//   }

//   private createConnection() {
//     this.hubConnection = new HubConnectionBuilder()
//       .withUrl(this.rootUrl + '/event-stream', { accessTokenFactory: () => localStorage.getItem('token') })
//       .build();
//   }

//   changeConnection(filterId = null) {
//     if (this.hubConnection.state) {
//       this.hubConnection.stop().then(() => {
//         if (!this.hubConnection.state) {
//           this.startConnection(filterId);
//         }
//       });
//     }
//   }

//   closeConnection() {
//     this.hubConnection.stop().then(() => console.log('Event monitoring connection closed'));
//   }

//   startConnection(filterId = null) {
//     this.hubConnection.start().then(() => {
//       this.startStream(filterId).subscribe({
//         next: (item) => {
//           this.eventsReceived.next(item);
//         },
//         complete: () => {
//           console.log('Completed');
//         },
//         error: (err) => { }
//       });
//     });
//   }

//   startStream(filterId) {
//     if (JSON.parse(localStorage.getItem('filter'))) {
//       return this.hubConnection.stream('GetStream', JSON.parse(localStorage.getItem('filter')).id);
//     } else {
//       return this.hubConnection.stream('GetStream', filterId);
//     }
//   }

// }
