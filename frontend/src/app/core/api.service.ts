import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  baseUrl = 'http://127.0.0.1:5000';

  async addEmployee(name: string, file: File) {
    const formData = new FormData();
    formData.append('name', name);
    formData.append('image', file);

    return fetch(`${this.baseUrl}/add_employee`, {
      method: 'POST',
      body: formData
    });
  }

  async recognize(blob: Blob) {
    const formData = new FormData();
    formData.append('image', blob);

    return fetch(`${this.baseUrl}/recognize`, {
      method: 'POST',
      body: formData
    }).then(res => res.json());
  }
}