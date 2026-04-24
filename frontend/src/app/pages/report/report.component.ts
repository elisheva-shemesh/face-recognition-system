import { Component, ElementRef, ViewChild, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../core/api.service';

@Component({
  selector: 'app-report',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './report.component.html'
})

export class ReportComponent implements AfterViewInit {

  @ViewChild('video') video?: ElementRef; // ❗ לא עם !

  report: any[] = [];
  totalHours = 0;
  loading = false;
  stream: any;
  showCamera = true;
  constructor(private api: ApiService) {}
  stopCamera() {
    if (this.stream) {
      this.stream.getTracks().forEach((track: any) => track.stop());
    }
  }
  async ngAfterViewInit() {
    try {
      this.stream = await navigator.mediaDevices.getUserMedia({ video: true });

if (this.video) {
  this.video.nativeElement.srcObject = this.stream;
}

    } catch (err) {
      console.error("Camera error:", err);
    }
  }

  async capture() {

    if (!this.video) {
      console.log("Video not ready");
      return;
    }

    this.loading = true;

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

    try {

      const result = await this.api.identify(blob);
      console.log("Recognize result:", result);
      const name = result.name;

      if (name && name !== 'Unknown') {
        this.stopCamera();
        this.showCamera = false;
        await this.loadReport(name);
      } else {
        alert("User not recognized");
      }

    } catch (err) {
      console.error("Recognition error:", err);
    }
    

    this.loading = false;
  }

  async loadReport(name: string) {

    try {
      this.report = await this.api.getReport(name);

      console.log("Report data:", this.report);

      this.calculateHours();

    } catch (err) {
      console.error("Report error:", err);
    }
  }

  calculateHours() {

    this.totalHours = 0;

    if (!this.report || this.report.length === 0) return;

    this.report.forEach((r: any) => {

      const checkIn = r[1];
      const checkOut = r[2];

      if (checkIn && checkOut) {

        const inTime = new Date(`1970-01-01T${checkIn}`);
        const outTime = new Date(`1970-01-01T${checkOut}`);

        this.totalHours += (outTime.getTime() - inTime.getTime()) / 3600000;
      }

    });
  }
}