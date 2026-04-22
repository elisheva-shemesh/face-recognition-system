import { Component, ElementRef, ViewChild, AfterViewInit } from '@angular/core';
import { ApiService } from '../../core/api.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-attendance',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './attendance.component.html'
})
export class AttendanceComponent implements AfterViewInit {

  @ViewChild('video') video!: ElementRef;
  result: any;

  constructor(private api: ApiService) {}

  async ngAfterViewInit() {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    this.video.nativeElement.srcObject = stream;
  }

  async capture() {
    const videoEl = this.video.nativeElement;

    const canvas = document.createElement('canvas');
    canvas.width = videoEl.videoWidth;
    canvas.height = videoEl.videoHeight;

    const ctx = canvas.getContext('2d')!;
    ctx.drawImage(videoEl, 0, 0);

    const blob = await new Promise<Blob>(resolve =>
      canvas.toBlob(resolve as any, 'image/jpeg')
    );

    this.result = await this.api.recognize(blob);
  }
}