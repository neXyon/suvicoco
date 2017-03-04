import { Component, OnInit } from '@angular/core';

import { CookerService } from '../services/cooker.service';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
})
export class MainComponent implements OnInit {

  private temperature : number;

  constructor(private cs : CookerService) {
  }

  ngOnInit() {
    this.cs.get_status();
    this.cs.onStarted(temperature => this.temperature = temperature);
    this.cs.onTemperature(temperature => this.temperature = temperature);
    this.cs.get_temperature().then(temperature => this.temperature = temperature);
  }

  private startCooking() {
    this.cs.start_cooking(this.temperature);
  }

  private stopCooking() {
    this.cs.stop_cooking();
  }

  private setTemperature() {
    this.cs.set_temperature(this.temperature);
  }
}
