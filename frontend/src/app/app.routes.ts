import { Routes } from '@angular/router';

import { HomeComponent } from './pages/home/home.component';
import { AddEmployeeComponent } from './pages/add-employee/add-employee.component';
import { AttendanceComponent } from './pages/attendance/attendance.component';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'add', component: AddEmployeeComponent },
  { path: 'attendance', component: AttendanceComponent }
];