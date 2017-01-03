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

  ngOnInit() {
  }

  startCooking(){
    this.currentlyCooking = true;
  }

  stopCooking(){
    this.currentlyCooking = false;
  }

}
