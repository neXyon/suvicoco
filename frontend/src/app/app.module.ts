import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { RouterModule, Routes } from '@angular/router';

import { MaterializeModule } from 'angular2-materialize';
import { AppComponent } from './app.component';
import { LoadingCircularComponent } from './components/misc/loading/circular/circular.component';
import { LoadingLinearComponent } from './components/misc/loading/linear/linear.component';
import { MainComponent } from './components/main/main/main.component';
import { NavbarComponent } from './components/main/navbar/navbar.component';

import { WebsocketService } from './services/websocket/websocket.service';

const appRoutes: Routes = [

  { path: '**', component: MainComponent }
];


@NgModule({
  declarations: [
    AppComponent,
    LoadingCircularComponent,
    LoadingLinearComponent,
    MainComponent,
    NavbarComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    MaterializeModule,
    RouterModule.forRoot(appRoutes)
  ],
  providers: [WebsocketService],
  bootstrap: [AppComponent]
})
export class AppModule { }
