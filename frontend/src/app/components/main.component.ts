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
    this.cs.get_status();//.then(status => this.currentlyCooking = status);
  }

  private startCooking(){
    this.cs.start_cooking(this.temperature);//.then(status => {if(status) this.currentlyCooking = true;});
    //this.currentlyCooking = true;
  }

  private stopCooking(){
    this.cs.stop_cooking();//.then(status => {if(status) this.currentlyCooking = false;});
    //this.currentlyCooking = false;
  }
}
