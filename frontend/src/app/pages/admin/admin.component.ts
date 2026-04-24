import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../core/api.service';

@Component({
  selector: 'app-admin',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin.component.html'
})
export class AdminComponent {

  employees: string[] = [];
  filteredEmployees: string[] = [];
  searchText = '';

  constructor(private api: ApiService, private router: Router) {}

  async loadEmployees() {
    const res = await fetch('http://127.0.0.1:5000/employees');
    this.employees = await res.json();
    this.filteredEmployees = this.employees;
  }

  goToAdd() {
    this.router.navigate(['/add-employee']);
  }

  logout() {
    localStorage.removeItem('user');
    this.router.navigate(['/']);
  }

  ngDoCheck() {
    this.filteredEmployees = this.employees.filter(e =>
      e.toLowerCase().includes(this.searchText.toLowerCase())
    );
  }
}