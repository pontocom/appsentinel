import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { KnowledgeBaseAddComponent } from './knowledge-base-add.component';

describe('KnowledgeBaseAddComponent', () => {
  let component: KnowledgeBaseAddComponent;
  let fixture: ComponentFixture<KnowledgeBaseAddComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ KnowledgeBaseAddComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(KnowledgeBaseAddComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
