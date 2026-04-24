import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../core/auth.service';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule,CommonModule],
  templateUrl: './login.component.html'
})
export class LoginComponent {

  username = '';
  password = '';
  error = false;

  constructor(private auth: AuthService, private router: Router) {}

  async login() {

    const res = await this.auth.login({
      username: this.username,
      password: this.password
    });

    if (res.success) {
      this.auth.setUser(res);
      this.router.navigate(['/']);
    } else {
      this.error = true;
    }
  }
}