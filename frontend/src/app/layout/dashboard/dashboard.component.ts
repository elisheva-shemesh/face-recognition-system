import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../core/api.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.component.html'
})
export class DashboardComponent implements OnInit {

  employees: any[] = [];

  constructor(private api: ApiService) {}

  async ngOnInit() {
    this.employees = await this.api.getEmployees();
  }

  getStatus(e: any) {

    const checkIn = e[2];
    const checkOut = e[3];
  
    if (checkIn && checkOut) {
      return 'done';
    }
  
    if (checkIn && !checkOut) {
      return 'inside';
    }
  
    return 'none';
  }
}