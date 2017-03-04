import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CookerService } from '../services/cooker.service';

@Component({
  selector: 'navbar',
  templateUrl: './navbar.component.html',
})
export class NavbarComponent implements OnInit {

  loadingActive: boolean = false;

  constructor(private router: Router, private cs : CookerService)
  {
  }

  ngOnInit() {
  }

}
