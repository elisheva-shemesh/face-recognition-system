import { HomeComponent } from './pages/home/home.component';
import { AttendanceComponent } from './pages/attendance/attendance.component';
import { LoginComponent } from './pages/login/login.component';
import { ReportComponent } from './pages/report/report.component';
import { AdminLoginComponent } from './pages/admin-login/admin-login.component';
import { AdminComponent } from './pages/admin/admin.component';
import { AddEmployeeComponent } from './pages/add-employee/add-employee.component';

export const routes = [
  { path: '', component: HomeComponent },
  { path: 'attendance', component: AttendanceComponent },
  { path: 'report', component: ReportComponent },
  { path: 'admin-login', component: AdminLoginComponent },
  { path: 'admin', component: AdminComponent },
  { path: 'add-employee', component: AddEmployeeComponent },
];