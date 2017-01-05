import { Component, OnInit } from '@angular/core';
import { WebsocketService } from '../../../services/websocket/websocket.service';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
})
export class MainComponent implements OnInit {

  private wss : WebsocketService;

  private currentlyCooking : boolean = false;
  private elapsedTime : number = 0;

  private temperature : number;

  constructor(private wss_ : WebsocketService)
  {
    this.wss = wss_;
  }

  ngOnInit()
  {

  }

  private startCooking(){
    this.wss.send('cooking_action', {cmd: 'start', temp: this.temperature});
  }

  private stopCooking(){
  }

  private updateTimer(data){
    this.elapsedTime = data;
  }
}
