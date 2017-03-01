import { Component, OnInit } from '@angular/core';

import { CookerService } from '../services/cooker.service';

@Component({
  selector: 'chart',
  templateUrl: './chart.component.html',
})
export class ChartComponent implements OnInit {
  public datasets:Array<any> = [ { label: 'No Data', data: [0, 0], steppedLine: true, fill: false } ];
  public labels: Array<any> = [0, 1];
  public options:any = {
    responsive: true,
    tooltips: {
      mode: 'x',
      intersect: false,

    },
    elements: {
      point:{
        radius: 0
      }
    },
    annotation: {
      annotations: [{
        id: 'a-line-1',
        type: 'line',
        mode: 'horizontal',
        scaleID: 'y-axis-1',
        value: 50,
        borderColor: 'red',
        borderWidth: 2,
      }]
    }
  };
  public graphs: Array<any> = [];
  public graphData: Array<any> = [];
  public selected: string = null;

  constructor(private cs : CookerService)
  {
  }

  onSelect(graph) {
    let data = this.graphData[graph];
    this.datasets[0].data = data.data;
    this.labels = data.labels;
    this.selected = graph;
  }

  setData(data) {
    let labels = new Array(Object.keys(data).length);

    let i = 0;
    for(let key in data) {
      let list = data[key];

      let x:Array<any> = new Array(list.length);
      let y:Array<any> = new Array(list.length);

      for(let j = 0; j < list.length; j++) {
        let entry = list[j];

        x[j] = entry[1];
        y[j] = entry[0];
      }

      data[key] = {data: x, labels: y};
      labels[i++] = key;
    }

    labels.sort();

    this.graphs = labels;
    this.graphData = data;

    if(Object.keys(data).length > 0) {
      if(labels.indexOf(this.selected) == -1) {
        if(labels.indexOf("temperature") != -1) {
          this.onSelect("temperature");
        }
        else {
          this.onSelect(labels[0]);
        }
      }
      else {
        this.onSelect(this.selected);
      }
    }
    else {
      this.selected = null;
    }

    this.cs.onUpdate(data => this.update(data));

    return data;
  }

  update(data : any) {
    if(this.graphs.indexOf(data.what) == -1) {
      this.graphData[data.what] = {data: [], labels: []};
      this.graphs.push(data.what);
      this.graphs.sort();
    }

    let entry = this.graphData[data.what];
    entry.data.push(data.value);
    entry.labels.push(data.when);

    if(this.selected == data.what) {
      this.labels = entry.labels.slice();
    }
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
