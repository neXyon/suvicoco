/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';

import { LinearComponent } from './linear.component';

describe('LinearComponent', () => {
  let component: LinearComponent;
  let fixture: ComponentFixture<LinearComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LinearComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LinearComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
