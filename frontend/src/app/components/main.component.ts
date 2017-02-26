import { Component, OnInit } from '@angular/core';
import { CookerService } from '../services/cooker.service';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
})
export class MainComponent implements OnInit {

  private cs : CookerService;

  private currentlyCooking : boolean = false;
  private elapsedTime : number = 0;

  private temperature : number;

  constructor(private cs_ : CookerService)
  {
    this.cs = cs_;
  }

  ngOnInit()
  {
    this.currentlyCooking = this.cs.get_status();
  }

  private startCooking(){
    this.cs.start_cooking(this.temperature);
    this.currentlyCooking = true;
  }

  private stopCooking(){
    this.cs.stop_cooking();
    this.currentlyCooking = false;
  }

  private updateTimer(data){
    this.elapsedTime = data;
  }
}
