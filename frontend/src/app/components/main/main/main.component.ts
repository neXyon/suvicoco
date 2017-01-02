import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
})
export class MainComponent implements OnInit {

  currentlyCooking : boolean = false;

  constructor() { }

  ngOnInit() {
  }


  startCooking(){
    this.currentlyCooking = true;
  }

  stopCooking(){
    this.currentlyCooking = false;
  }

}
