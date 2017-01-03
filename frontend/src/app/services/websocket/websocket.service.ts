import { Injectable, EventEmitter } from '@angular/core';
import * as io from 'socket.io-client';
import { MaterializeAction } from 'angular2-materialize';

@Injectable()
export class WebsocketService {

  private websocket : any;
  public isConnected : boolean = false;

  constructor()
  {
    this.connect();
  }

  public connect()
  {
    this.websocket = io("http://localhost:5000");
    this.websocket.on('connect', () => this.onConnect());
    this.websocket.on('disconnect', () => this.onDisconnect());
  }

  public disconnect()
  {
    this.websocket.disconnect();
  }

  private onConnect()
  {
    this.isConnected = true;
  }

  private onDisconnect()
  {
    this.isConnected = false;
  }
}
