import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { RouterModule, Routes } from '@angular/router';

import { MaterializeModule } from 'angular2-materialize';
import { ChartsModule } from 'ng2-charts';

import { AppComponent } from './components/app.component';
import { ChartComponent } from './components/chart.component';
import { LoadingLinearComponent } from './components/linear.component';
import { MainComponent } from './components/main.component';
import { NavbarComponent } from './components/navbar.component';

import { CookerService } from './services/cooker.service';

const appRoutes: Routes = [

  { path: '**', component: MainComponent }
];


@NgModule({
  declarations: [
    AppComponent,
    LoadingLinearComponent,
    MainComponent,
    NavbarComponent,
    ChartComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    MaterializeModule,
    ChartsModule,
    RouterModule.forRoot(appRoutes)
  ],
  providers: [CookerService],
  bootstrap: [AppComponent]
})
export class AppModule { }
