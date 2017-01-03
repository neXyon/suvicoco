import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { WebsocketService } from '../../../services/websocket/websocket.service';

@Component({
  selector: 'navbar',
  templateUrl: './navbar.component.html',
})
export class NavbarComponent implements OnInit {

  loadingActive: boolean = false;
  router : Router;
  wss : WebsocketService;

  constructor(private router_: Router, private wss_ : WebsocketService)
  {
    this.router = router_;
    this.wss = wss_;
  }

  ngOnInit() {
  }

}
