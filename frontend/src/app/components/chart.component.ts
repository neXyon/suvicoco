import { Component, OnInit } from '@angular/core';

//import { CHART_DIRECTIVES } from 'ng2-charts/ng2-charts';

import { CookerService } from '../services/cooker.service';

@Component({
  selector: 'chart',
  //directives: [CHART_DIRECTIVES],
  templateUrl: './chart.component.html',
})
export class ChartComponent implements OnInit {
  public datasets:Array<any> = [//{data: [{x: 0, y: 0}, {x: 1, y: 1}], label: 'Series A', steppedLine: true, fill: false}];
      {
          label: 'Scatter Dataset',
          data: [{
              x: -10,
              y: 0
          }, {
              x: 0,
              y: 10
          }, {
              x: 10,
              y: 5
          }]
      }
  ];//*/
  private options = {
    scales: {
      yAxes: [{
        ticks: {
          beginAtZero: true
        }
      }]
    }
  };
  public options2:any = {
    responsive: true,
    legend: {
      position: 'bottom'
    },
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

  constructor(private cs : CookerService)
  {
  }

  setData(data) {
    console.log(data);
    console.log(Object.keys(data).length);

    let chart_data:Array<any> = new Array(Object.keys(data).length);

    let i = 0;
    for(let key in data) {
      let list = data[key];

      let points:Array<any> = new Array(list.length);

      for(let j = 0; j < list.length; j++) {
        let entry = list[j];

        points[j] = {x: entry[0], y: entry[1]};
      }

      chart_data[i] = {data: points, label: key, steppedLine: true, fill: false};

      i++;
    }

    console.log(chart_data);
    //this.datasets = chart_data;

    this.datasets = [
        {
          label: "# of Votes",
          data: [{x: 1, y: 19}, {x: 2, y: 3}, {x: 3, y: 5}, {x: 4, y: 2}, {x: 5, y: 3}, {x: 6, y: 12}]
        },
        {
          label: "# 2 of Votes",
          data: [{x: 1, y: 1}, {x: 2, y: 19}, {x: 3, y: 3}, {x: 4, y: 5}, {x: 5, y: 2}, {x: 6, y: 3}]
        }
      ];

    return data;
  }

  ngOnInit() : void {
    console.log('Init');
    this.cs.get_data().then(data => this.setData(data));
  }

  /*public randomize():void {
    let _lineChartData:Array<any> = new Array(this.lineChartData.length);
    for (let i = 0; i < this.lineChartData.length; i++) {
      _lineChartData[i] = {data: new Array(this.lineChartData[i].data.length), label: this.lineChartData[i].label};
      for (let j = 0; j < this.lineChartData[i].data.length; j++) {
        _lineChartData[i].data[j] = Math.floor((Math.random() * 100) + 1);
      }
    }
    this.lineChartData = _lineChartData;
  }*/

  // events
  public chartClicked(e:any):void {
    console.log(e);
  }

  public chartHovered(e:any):void {
    console.log(e);
  }
}
