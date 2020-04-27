import { TestBed } from '@angular/core/testing';

import { ApksService } from './apks.service';

describe('ApksService', () => {
  let service: ApksService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ApksService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
