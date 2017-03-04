import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';

import { CookerService } from '../services/cooker.service';

import { Observable }        from 'rxjs/Observable';
import { Subject }           from 'rxjs/Subject';

import 'rxjs/add/observable/of';
import 'rxjs/add/operator/sampleTime';
import 'rxjs/add/operator/distinctUntilChanged';
import 'rxjs/add/operator/switchMap';

declare var $:any;

/*
TODO:
- show label value because of hover...
*/

@Component({
  selector: 'chart',
  templateUrl: './chart.component.html',
  styleUrls: ['./chart.component.css']
})
export class ChartComponent implements OnInit {
  public options: any = {
    legend: {
      show: false,
    },
    xaxis: {
      mode: 'time',
      timeformat: '%H:%M:%S'
    },
		grid: {
			hoverable: true,
			autoHighlight: false
		},
    series: {
      lines: {
        steps: true
      }
    },
    colors: ["#ef5350", "#ab47bc", "#5c6bc0", "#29b6f6", "#26a69a", "#9ccc65", "#ffee58", "#ffa726", "#8d6e63", "#78909c"],
		crosshair: {
			mode: "x"
		}
  };

  public labels = [];
  public datasets = {};
  private currentValues = {}
  private currentTime = new Subject<Date>();

  private plot: any = null;
  private updateLegendTimeout = null;
  private latestPosition = null;

  @ViewChild('placeholder') placeholder :ElementRef;

  constructor(private cs : CookerService)
  {
  }

  refresh() {
    let data = []

    for(let key in this.datasets) {
      let ds = this.datasets[key];

      if(ds.lines.show) {
        data.push(ds);
      }
    }

    if(data.length == 0)
      return;

    if(this.plot) {
      this.plot.setData(data);
      this.plot.setupGrid();
      this.plot.draw();
    }
    else {
      this.plot = $.plot(this.placeholder.nativeElement, data, this.options );

      this.currentTime.sampleTime(50).distinctUntilChanged()
        .switchMap(time => Observable.of<any>(this.closestValues(time)))
        .subscribe(values => this.currentValues = values);

      $(this.placeholder.nativeElement).bind("plothover", (event, pos, item) => this.hover(event, pos, item));
    }
  }

  addDataset(label, data) {
    let color = this.labels.length;
    this.labels.push(label);
    this.datasets[label] = {label: label, data: data, color: color, lines: {show: label == 'temperature'}};
    this.labels.sort();
  }

  setData(data) {
    let maxDate = null;

    for(let key in data) {
      let list = data[key];

      let last_value = 0;

      for(let j = 0; j < list.length; j++) {
        list[j][0] = new Date(list[j][0]);

        if(!maxDate || list[j][0] > maxDate)
          maxDate = list[j][0];

        last_value = list[j][1];
      }

      this.addDataset(key, data[key]);

      //this.currentValues[key] = last_value;
    }

    if(this.labels.length > 0) {
      this.refresh();
      this.currentTime.next(maxDate);
    }

    this.cs.onUpdate(data => this.update(data));

    return data;
  }

  update(data : any) {
    if(this.labels.indexOf(data.what) == -1) {
      this.addDataset(data.what, []);
    }

    let entry = this.datasets[data.what];
    let date = new Date(data.when);
    entry.data.push([date, data.value]);

    if(this.datasets[data.what].lines.show) {
      this.refresh();
      this.currentTime.next(date);
    }
  }

  hover(event, pos, item) {
    this.currentTime.next(new Date(pos.x));
  }

  closestValues(time) {
    let values = {};

    for(let label in this.labels) {
      label = this.labels[label];
      let data = this.datasets[label].data;

      let i = 0;

      for(i = 0; i < data.length; i++) {
        if(data[i][0] > time) {
          break;
        }
      }

      values[label] = i == 0 ? null : (+data[i - 1][1]).toFixed(2);
    }

    return values;
  }

  ngOnInit() : void {
    this.cs.get_data().then(data => this.setData(data));
  }

  // events
  public chartClicked(e:any):void {
    console.log(e);
  }

  public chartHovered(e:any):void {
    console.log(e);
  }
}
