import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'loading-circular',
  templateUrl: './circular.component.html',
})
export class LoadingCircularComponent implements OnInit {

  @Input() color: string = "blue";
  @Input() size: string = "";

  constructor() { }

  ngOnInit() { }

}
