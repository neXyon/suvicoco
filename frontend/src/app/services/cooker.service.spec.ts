/* tslint:disable:no-unused-variable */

import { TestBed, async, inject } from '@angular/core/testing';
import { CookerService } from './cooker.service';

describe('CookerService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [CookerService]
    });
  });

  it('should ...', inject([CookerService], (service: CookerService) => {
    expect(service).toBeTruthy();
  }));
});
