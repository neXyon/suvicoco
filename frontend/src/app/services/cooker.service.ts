import { Injectable } from '@angular/core';
import { Headers, Http } from '@angular/http';

import * as io from 'socket.io-client';
import 'rxjs/add/operator/toPromise';

@Injectable()
export class CookerService {

  private websocket : any;
  public isConnected : boolean = false;
  public clientId : string;

  public status : boolean = false;
  public data : any = [];
  public temperature : number = 0.0;

  private baseUrl = '/control/';
  private startUrl = this.baseUrl + 'start/';
  private stopUrl = this.baseUrl + 'stop';
  private statusUrl = this.baseUrl + 'status';
  private setUrl = this.baseUrl + 'set/';
  private dataUrl = this.baseUrl + 'data';

  constructor(private http: Http)
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

  public start_cooking(temperature) : Promise<boolean>
  {
    return this.http.get(`${this.startUrl}/${temperature}`)
               .toPromise()
               .then(response => response.json() as boolean)
               .then(status => {if(status) this.status = true; console.log(status); return status})
               .catch((error: any) => console.log('Error', error));
  }

  public stop_cooking() : Promise<boolean>
  {
    return this.http.get(this.stopUrl)
               .toPromise()
               .then(response => response.json() as boolean)
               .then(status => {if(status) this.status = false; return status})
               .catch((error: any) => console.log('Error', error));
  }

  public get_status() : Promise<boolean>
  {
    return this.http.get(this.statusUrl)
               .toPromise()
               .then(response => response.json() as boolean)
               .then(status => this.status = status)
               .catch((error: any) => console.log('Error', error));
  }

  public get_data() : Promise<any>
  {
    return this.http.get(this.dataUrl)
               .toPromise()
               .then(response => response.json())
               .catch((error: any) => console.log('Error', error));
  }

  private set_temperature(temperature : number) : Promise<boolean>
  {
    return this.http.get(`${this.setUrl}/${temperature}`)
               .toPromise()
               .then(response => response.json() as boolean)
               .catch((error: any) => console.log('Error', error));
  }

  private update(data)
  {
    console.log('update');
    console.log(data);
    /*console.log(when);
    console.log(value);
    this.data[what] += [when, value];*/
  }

  public onUpdate(func)
  {
    this.websocket.on('update', (data) => func(data));
  }

  public disconnect()
  {
    this.websocket.disconnect();
  }

  private onConnect()
  {
    this.clientId = this.websocket.io.engine.id;
    this.isConnected = true;

    this.websocket.on('stopped', () => this.status = false);
    this.websocket.on('started', () => this.status = true);
    //this.websocket.on('temperature', (data) => this.set_temperature(data.temperature));
    this.websocket.on('update', (data) => this.update(data));
  }

  private onDisconnect()
  {
    this.isConnected = false;
  }

  private onError()
  {
    console.log("error");
  }
}
