import { Component, ElementRef, ViewChild, AfterViewInit } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../core/api.service';

@Component({
  selector: 'app-admin-login',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './admin-login.component.html'
})
export class AdminLoginComponent implements AfterViewInit {

  @ViewChild('video') video?: ElementRef;
  stream: any;

  constructor(private api: ApiService, private router: Router) {}

  async ngAfterViewInit() {
    this.stream = await navigator.mediaDevices.getUserMedia({ video: true });

    if (this.video) {
      this.video.nativeElement.srcObject = this.stream;
    }
  }

  stopCamera() {
    if (this.stream) {
      this.stream.getTracks().forEach((t: any) => t.stop());
    }
  }

  async capture() {

    if (!this.video) return;

    const videoEl = this.video.nativeElement;

    const canvas = document.createElement('canvas');
    canvas.width = videoEl.videoWidth;
    canvas.height = videoEl.videoHeight;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    ctx.drawImage(videoEl, 0, 0);

    const blob: Blob = await new Promise(resolve =>
      canvas.toBlob(resolve as any, 'image/jpeg')
    );

    const result = await this.api.identify(blob);

    if (result.is_admin) {

      this.stopCamera();

      // שמירת משתמש
      localStorage.setItem('user', JSON.stringify(result));

      this.router.navigate(['/admin']);

    } else {
      alert("אין לך הרשאות מנהל");
    }
  }
}