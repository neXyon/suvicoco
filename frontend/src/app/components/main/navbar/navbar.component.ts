import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'navbar',
  templateUrl: './navbar.component.html',
})
export class NavbarComponent implements OnInit {

  loadingActive: boolean = false;

  constructor() { }

  ngOnInit() { }

}
