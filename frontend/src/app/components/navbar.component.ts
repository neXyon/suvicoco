import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CookerService } from '../services/cooker.service';

@Component({
  selector: 'navbar',
  templateUrl: './navbar.component.html',
})
export class NavbarComponent implements OnInit {

  loadingActive: boolean = false;
  router : Router;
  wss : CookerService;

  constructor(private router_: Router, private wss_ : CookerService)
  {
    this.router = router_;
    this.wss = wss_;
  }

  ngOnInit() {
  }

}
