import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'navbar',
  templateUrl: './navbar.component.html',
})
export class NavbarComponent implements OnInit {

  loadingActive: boolean = false;
  activeRoute : string;
  router: Router;

  constructor(private router_: Router) {
    this.router = router_;
   }

  ngOnInit() {
  }

}
