import { Component, OnInit } from '@angular/core';
import { CookerService } from '../services/cooker.service';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
})
export class MainComponent implements OnInit {

  private wss : CookerService;

  private currentlyCooking : boolean = false;
  private elapsedTime : number = 0;

  private temperature : number;

  constructor(private wss_ : CookerService)
  {
    this.wss = wss_;
  }

  ngOnInit()
  {

  }

  private startCooking(){
    this.wss.send('start cooking', {temperature: this.temperature});
    this.currentlyCooking = true;
  }

  private stopCooking(){
    this.wss.send('stop cooking', {});
    this.currentlyCooking = false;
  }

  private updateTimer(data){
    this.elapsedTime = data;
  }
}
