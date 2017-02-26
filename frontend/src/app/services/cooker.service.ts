import { Injectable, EventEmitter } from '@angular/core';
import * as io from 'socket.io-client';

@Injectable()
export class CookerService {

  private websocket : any;
  public isConnected : boolean = false;
  public clientId : string;

  constructor()
  {
    this.connect();
  }

  public connect()
  {
    this.websocket = io("http://localhost:5000");
    this.websocket.on('connect', () => this.onConnect());
    this.websocket.on('disconnect', () => this.onDisconnect());
    this.websocket.on('error', () => this.onError());
  }

  public send(event, data)
  {
    this.websocket.emit(event, data)
  }

  public on(event, func)
  {
    this.websocket.on(event, (data) => func(data));
  }

  public disconnect()
  {
    this.websocket.disconnect();
  }

  private onConnect()
  {
    this.clientId = this.websocket.io.engine.id;
    this.isConnected = true;
  }

  private onDisconnect()
  {
    this.isConnected = false;
  }

  private onError()
  {

  }
}
