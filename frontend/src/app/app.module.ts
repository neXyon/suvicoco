import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { MaterializeModule } from 'angular2-materialize';
import { AppComponent } from './app.component';
import { LoadingCircularComponent } from './components/misc/loading/circular/circular.component';
import { LoadingLinearComponent } from './components/misc/loading/linear/linear.component';

@NgModule({
  declarations: [
    AppComponent,
    LoadingCircularComponent,
    LoadingLinearComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    MaterializeModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
