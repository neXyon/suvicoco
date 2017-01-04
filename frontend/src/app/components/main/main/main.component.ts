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
    this.wss.on('timer_status', (data) => this.receivedStatus(data));
    this.wss.on('timer_elapsed', (data) => this.updateTimer(data));
  }

  private startCooking(){
    this.wss.send('timer_action', 'start');
    this.wss.send('cooking_action', {cmd: 'start', temp: this.temperature});
  }

  private stopCooking(){
    this.wss.send('timer_action', 'stop');
  }

  private receivedStatus(data){
    if(data == 'active')
      this.currentlyCooking = true;
    else if(data == 'inactive')
      this.currentlyCooking = false;
  }

  private updateTimer(data){
    this.elapsedTime = data;
  }
}
