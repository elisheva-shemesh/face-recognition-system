import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  login(data: any) {
    return fetch('http://127.0.0.1:5000/login', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data)
    }).then(res => res.json());
  }

  setUser(user: any) {
    localStorage.setItem('user', JSON.stringify(user));
  }

  getUser() {
    return JSON.parse(localStorage.getItem('user') || 'null');
  }

  logout() {
    localStorage.removeItem('user');
  }

  isLoggedIn() {
    return !!localStorage.getItem('user');
  }

  isAdmin() {
    const user = this.getUser();
    return user?.role === 'admin';
  }
}