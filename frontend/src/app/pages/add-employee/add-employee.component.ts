import { Component } from '@angular/core';
import { ApiService } from '../../core/api.service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-add-employee',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './add-employee.component.html'
})
export class AddEmployeeComponent {

  name = '';
  file!: File;

  constructor(private api: ApiService) {}

  onFile(event: any) {
    this.file = event.target.files[0];
  }

  async upload() {
    await this.api.addEmployee(this.name, this.file);
    alert('Saved');
  }
}