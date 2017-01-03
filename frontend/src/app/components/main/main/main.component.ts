import { Component, OnInit } from '@angular/core';
import { WebsocketService } from '../../../services/websocket/websocket.service';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
})
export class MainComponent implements OnInit {

  private currentlyCooking : boolean = false;

  private wss : WebsocketService;

  constructor(private wss_ : WebsocketService)
  {
    this.wss = wss_;
  }

  ngOnInit()
  {
    this.wss.on('cooking', (data) => this.receivedStatus(data));
  }

  private startCooking(){
    this.wss.send('cooking', true);
  }

  private stopCooking(){
    this.wss.send('cooking', false);
  }

  private receivedStatus(data){
    this.currentlyCooking = data;
  }
}
