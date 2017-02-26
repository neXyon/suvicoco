import { Injectable, EventEmitter } from '@angular/core';
import * as io from 'socket.io-client';

@Injectable()
export class CookerService {

  private websocket : any;
  public isConnected : boolean = false;
  public clientId : string;

  public status : boolean = false;
  public data : any = [];
  public temperature : number = 0.0;

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

  public start_cooking(temperature)
  {
    this.websocket.emit('start cooking', {temperature: temperature});
  }

  public stop_cooking()
  {
    this.websocket.emit('stop cooking');
  }

  public get_status() : boolean
  {
    return this.status;
  }

  private set_status(status: boolean)
  {
    console.log(status);
    this.status = status;
  }

  public get_data()
  {
    return this.data;
  }

  private set_data(data)
  {
    console.log(data);
    this.data = data;
  }

  public get_temperature() : number
  {
    return this.temperature;
  }

  private set_temperature(temperature : number)
  {
    console.log(temperature);
    this.temperature = temperature;
  }

  public send(event, data)
  {
    this.websocket.emit(event, data)
  }

  private update(data)
  {
    console.log('update');
    console.log(data);
    /*console.log(when);
    console.log(value);
    this.data[what] += [when, value];*/
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

    this.websocket.on('status', (status) => this.set_status(status));
    this.websocket.on('data', (data) => this.set_data(data));
    this.websocket.on('stopped', () => this.set_status(false));
    this.websocket.on('start', () => this.set_status(true));
    this.websocket.on('temperature', (data) => this.set_temperature(data.temperature));
    this.websocket.on('update', (data) => this.update(data));
    console.log('Registered, now emitting');
    this.websocket.emit('get_status');
    this.websocket.emit('get_data');
  }

  private onDisconnect()
  {
    this.isConnected = false;
  }

  private onError()
  {

  }
}
