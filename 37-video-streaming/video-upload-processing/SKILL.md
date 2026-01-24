---
name: Video Upload & Processing
description: Handling video file uploads, transcoding, thumbnail generation, and delivery using S3 storage, FFmpeg processing, job queues, and CDN delivery for scalable video processing pipelines.
---

# Video Upload & Processing

> **Current Level:** Advanced  
> **Domain:** Video Streaming / Media Processing

---

## Overview

Video upload and processing handles file uploads, transcoding, thumbnail generation, and delivery. This guide covers S3 storage, FFmpeg processing, and CDN delivery for building video processing systems that handle uploads efficiently and deliver optimized content.

## Video Upload Patterns

### Direct Upload

```typescript
// services/video-upload.service.ts
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3';
import { getSignedUrl } from '@aws-sdk/s3-request-presigner';

export class VideoUploadService {
  private s3Client: S3Client;
  private bucket = process.env.S3_BUCKET!;

  constructor() {
    this.s3Client = new S3Client({
      region: process.env.AWS_REGION!,
      credentials: {
        accessKeyId: process.env.AWS_ACCESS_KEY_ID!,
        secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY!
      }
    });
  }

  async generateUploadUrl(
    fileName: string,
    fileType: string,
    fileSize: number
  ): Promise<UploadUrl> {
    const key = `videos/${Date.now()}-${fileName}`;

    const command = new PutObjectCommand({
      Bucket: this.bucket,
      Key: key,
      ContentType: fileType,
      ContentLength: fileSize,
      Metadata: {
        originalName: fileName
      }
    });

    const uploadUrl = await getSignedUrl(this.s3Client, command, {
      expiresIn: 3600 // 1 hour
    });

    return {
      uploadUrl,
      key,
      expiresIn: 3600
    };
  }

  async uploadVideo(file: File): Promise<string> {
    const { uploadUrl, key } = await this.generateUploadUrl(
      file.name,
      file.type,
      file.size
    );

    // Upload directly to S3
    await fetch(uploadUrl, {
      method: 'PUT',
      body: file,
      headers: {
        'Content-Type': file.type
      }
    });

    return key;
  }
}

interface UploadUrl {
  uploadUrl: string;
  key: string;
  expiresIn: number;
}
```

### Resumable Upload

```typescript
// services/resumable-upload.service.ts
import { Upload } from '@aws-sdk/lib-storage';
import { S3Client } from '@aws-sdk/client-s3';

export class ResumableUploadService {
  private s3Client: S3Client;

  constructor() {
    this.s3Client = new S3Client({ region: process.env.AWS_REGION! });
  }

  async uploadWithProgress(
    file: File,
    onProgress: (progress: number) => void
  ): Promise<string> {
    const key = `videos/${Date.now()}-${file.name}`;

    const upload = new Upload({
      client: this.s3Client,
      params: {
        Bucket: process.env.S3_BUCKET!,
        Key: key,
        Body: file,
        ContentType: file.type
      },
      queueSize: 4, // concurrent parts
      partSize: 5 * 1024 * 1024, // 5MB parts
      leavePartsOnError: false
    });

    upload.on('httpUploadProgress', (progress) => {
      const percentage = ((progress.loaded || 0) / (progress.total || 1)) * 100;
      onProgress(percentage);
    });

    await upload.done();

    return key;
  }
}

// Client-side usage
function VideoUploader() {
  const [progress, setProgress] = useState(0);

  const handleUpload = async (file: File) => {
    const service = new ResumableUploadService();
    
    const key = await service.uploadWithProgress(file, (progress) => {
      setProgress(progress);
    });

    console.log('Upload complete:', key);
  };

  return (
    <div>
      <input type="file" accept="video/*" onChange={(e) => {
        if (e.target.files?.[0]) {
          handleUpload(e.target.files[0]);
        }
      }} />
      <progress value={progress} max={100} />
    </div>
  );
}
```

### Multipart Upload

```typescript
// services/multipart-upload.service.ts
import {
  CreateMultipartUploadCommand,
  UploadPartCommand,
  CompleteMultipartUploadCommand,
  AbortMultipartUploadCommand
} from '@aws-sdk/client-s3';

export class MultipartUploadService {
  private s3Client: S3Client;
  private chunkSize = 5 * 1024 * 1024; // 5MB

  async uploadLargeFile(file: File, onProgress: (progress: number) => void): Promise<string> {
    const key = `videos/${Date.now()}-${file.name}`;

    // Initiate multipart upload
    const createCommand = new CreateMultipartUploadCommand({
      Bucket: process.env.S3_BUCKET!,
      Key: key,
      ContentType: file.type
    });

    const { UploadId } = await this.s3Client.send(createCommand);

    if (!UploadId) {
      throw new Error('Failed to initiate multipart upload');
    }

    try {
      const parts: { ETag: string; PartNumber: number }[] = [];
      const totalParts = Math.ceil(file.size / this.chunkSize);

      for (let partNumber = 1; partNumber <= totalParts; partNumber++) {
        const start = (partNumber - 1) * this.chunkSize;
        const end = Math.min(start + this.chunkSize, file.size);
        const chunk = file.slice(start, end);

        const uploadCommand = new UploadPartCommand({
          Bucket: process.env.S3_BUCKET!,
          Key: key,
          UploadId,
          PartNumber: partNumber,
          Body: chunk
        });

        const { ETag } = await this.s3Client.send(uploadCommand);

        if (ETag) {
          parts.push({ ETag, PartNumber: partNumber });
        }

        onProgress((partNumber / totalParts) * 100);
      }

      // Complete multipart upload
      const completeCommand = new CompleteMultipartUploadCommand({
        Bucket: process.env.S3_BUCKET!,
        Key: key,
        UploadId,
        MultipartUpload: { Parts: parts }
      });

      await this.s3Client.send(completeCommand);

      return key;
    } catch (error) {
      // Abort on error
      const abortCommand = new AbortMultipartUploadCommand({
        Bucket: process.env.S3_BUCKET!,
        Key: key,
        UploadId
      });

      await this.s3Client.send(abortCommand);
      throw error;
    }
  }
}
```

## Video Processing Pipeline

```typescript
// services/video-processing.service.ts
import { Queue } from 'bullmq';
import { PrismaClient } from '@prisma/client';

const db = new PrismaClient();

export class VideoProcessingService {
  private queue: Queue;

  constructor() {
    this.queue = new Queue('video-processing', {
      connection: {
        host: process.env.REDIS_HOST,
        port: parseInt(process.env.REDIS_PORT || '6379')
      }
    });
  }

  async processVideo(videoId: string, s3Key: string): Promise<void> {
    // Add to processing queue
    await this.queue.add('process-video', {
      videoId,
      s3Key,
      tasks: [
        'extract-metadata',
        'generate-thumbnail',
        'transcode-720p',
        'transcode-480p',
        'transcode-360p'
      ]
    });

    // Update video status
    await db.video.update({
      where: { id: videoId },
      data: { status: 'processing' }
    });
  }

  async onProcessingComplete(videoId: string): Promise<void> {
    await db.video.update({
      where: { id: videoId },
      data: {
        status: 'ready',
        processedAt: new Date()
      }
    });
  }

  async onProcessingFailed(videoId: string, error: string): Promise<void> {
    await db.video.update({
      where: { id: videoId },
      data: {
        status: 'failed',
        error
      }
    });
  }
}
```

## FFmpeg Usage

```typescript
// workers/video-processor.worker.ts
import { Worker } from 'bullmq';
import ffmpeg from 'fluent-ffmpeg';
import { S3Client, GetObjectCommand, PutObjectCommand } from '@aws-sdk/client-s3';
import { Readable } from 'stream';
import fs from 'fs';
import path from 'path';

const worker = new Worker('video-processing', async (job) => {
  const { videoId, s3Key, tasks } = job.data;

  try {
    // Download video from S3
    const localPath = await downloadFromS3(s3Key);

    for (const task of tasks) {
      await job.updateProgress({ currentTask: task });

      switch (task) {
        case 'extract-metadata':
          await extractMetadata(videoId, localPath);
          break;
        case 'generate-thumbnail':
          await generateThumbnail(videoId, localPath);
          break;
        case 'transcode-720p':
          await transcodeVideo(videoId, localPath, '720p');
          break;
        case 'transcode-480p':
          await transcodeVideo(videoId, localPath, '480p');
          break;
        case 'transcode-360p':
          await transcodeVideo(videoId, localPath, '360p');
          break;
      }
    }

    // Cleanup
    fs.unlinkSync(localPath);

    return { success: true };
  } catch (error) {
    console.error('Processing failed:', error);
    throw error;
  }
});

async function downloadFromS3(key: string): Promise<string> {
  const s3Client = new S3Client({ region: process.env.AWS_REGION! });
  
  const command = new GetObjectCommand({
    Bucket: process.env.S3_BUCKET!,
    Key: key
  });

  const response = await s3Client.send(command);
  const localPath = `/tmp/${path.basename(key)}`;

  const writeStream = fs.createWriteStream(localPath);
  await new Promise((resolve, reject) => {
    (response.Body as Readable).pipe(writeStream)
      .on('finish', resolve)
      .on('error', reject);
  });

  return localPath;
}
```

## Thumbnail Generation

```typescript
// utils/thumbnail-generator.ts
async function generateThumbnail(videoId: string, videoPath: string): Promise<void> {
  const thumbnailPath = `/tmp/${videoId}-thumbnail.jpg`;

  await new Promise<void>((resolve, reject) => {
    ffmpeg(videoPath)
      .screenshots({
        timestamps: ['10%', '50%', '90%'],
        filename: `${videoId}-%i.jpg`,
        folder: '/tmp',
        size: '1280x720'
      })
      .on('end', () => resolve())
      .on('error', reject);
  });

  // Upload thumbnails to S3
  for (let i = 1; i <= 3; i++) {
    const thumbPath = `/tmp/${videoId}-${i}.jpg`;
    const s3Key = `thumbnails/${videoId}-${i}.jpg`;

    await uploadToS3(thumbPath, s3Key, 'image/jpeg');
    fs.unlinkSync(thumbPath);
  }

  // Save thumbnail URLs to database
  await db.video.update({
    where: { id: videoId },
    data: {
      thumbnails: [
        `${process.env.CDN_URL}/thumbnails/${videoId}-1.jpg`,
        `${process.env.CDN_URL}/thumbnails/${videoId}-2.jpg`,
        `${process.env.CDN_URL}/thumbnails/${videoId}-3.jpg`
      ]
    }
  });
}
```

## Metadata Extraction

```typescript
// utils/metadata-extractor.ts
async function extractMetadata(videoId: string, videoPath: string): Promise<void> {
  const metadata = await new Promise<any>((resolve, reject) => {
    ffmpeg.ffprobe(videoPath, (err, metadata) => {
      if (err) reject(err);
      else resolve(metadata);
    });
  });

  const videoStream = metadata.streams.find((s: any) => s.codec_type === 'video');
  const audioStream = metadata.streams.find((s: any) => s.codec_type === 'audio');

  await db.video.update({
    where: { id: videoId },
    data: {
      duration: metadata.format.duration,
      width: videoStream?.width,
      height: videoStream?.height,
      fps: eval(videoStream?.r_frame_rate || '0'),
      videoCodec: videoStream?.codec_name,
      audioCodec: audioStream?.codec_name,
      bitrate: metadata.format.bit_rate,
      fileSize: metadata.format.size
    }
  });
}
```

## Progress Tracking

```typescript
// services/progress-tracker.service.ts
export class ProgressTrackerService {
  async updateProgress(videoId: string, progress: number, status: string): Promise<void> {
    await db.videoProcessing.upsert({
      where: { videoId },
      create: {
        videoId,
        progress,
        status,
        startedAt: new Date()
      },
      update: {
        progress,
        status,
        updatedAt: new Date()
      }
    });

    // Emit WebSocket event
    io.to(`video:${videoId}`).emit('processing-progress', {
      videoId,
      progress,
      status
    });
  }

  async getProgress(videoId: string): Promise<ProcessingProgress | null> {
    return db.videoProcessing.findUnique({
      where: { videoId }
    });
  }
}

interface ProcessingProgress {
  videoId: string;
  progress: number;
  status: string;
  startedAt: Date;
  updatedAt: Date;
}
```

## Storage Optimization

```typescript
// utils/storage-optimizer.ts
export class StorageOptimizer {
  async optimizeStorage(videoId: string): Promise<void> {
    const video = await db.video.findUnique({ where: { id: videoId } });

    if (!video) return;

    // Delete original after transcoding
    if (video.status === 'ready' && video.originalKey) {
      await this.deleteFromS3(video.originalKey);
      
      await db.video.update({
        where: { id: videoId },
        data: { originalKey: null }
      });
    }

    // Set lifecycle policies
    await this.setLifecyclePolicy();
  }

  private async setLifecyclePolicy(): Promise<void> {
    // Move to Glacier after 90 days
    // Delete after 1 year
  }

  private async deleteFromS3(key: string): Promise<void> {
    const s3Client = new S3Client({ region: process.env.AWS_REGION! });
    
    await s3Client.send(new DeleteObjectCommand({
      Bucket: process.env.S3_BUCKET!,
      Key: key
    }));
  }
}
```

## Best Practices

1. **Resumable Uploads** - Support resumable uploads for large files
2. **Queue Processing** - Use queues for async processing
3. **Progress Tracking** - Track and display progress
4. **Error Handling** - Handle all processing errors
5. **Thumbnails** - Generate multiple thumbnail options
6. **Metadata** - Extract and store video metadata
7. **Storage** - Optimize storage costs
8. **CDN** - Use CDN for delivery
9. **Cleanup** - Clean up temporary files
10. **Monitoring** - Monitor processing pipeline

---

## Quick Start

### Video Upload

```typescript
// Presigned URL for direct upload
async function getUploadUrl(filename: string): Promise<string> {
  const s3Client = new S3Client({})
  const command = new PutObjectCommand({
    Bucket: process.env.S3_BUCKET,
    Key: `videos/${filename}`,
    ContentType: 'video/mp4'
  })
  
  return await getSignedUrl(s3Client, command, { expiresIn: 3600 })
}

// Process video after upload
async function processVideo(s3Key: string) {
  // Download from S3
  const video = await downloadFromS3(s3Key)
  
  // Transcode
  await transcodeVideo(video, [
    { resolution: '1080p', bitrate: '5M' },
    { resolution: '720p', bitrate: '2.5M' },
    { resolution: '480p', bitrate: '1M' }
  ])
  
  // Generate thumbnail
  await generateThumbnail(video)
}
```

---

## Production Checklist

- [ ] **Upload**: Resumable uploads for large files
- [ ] **Queue Processing**: Queue for async processing
- [ ] **Progress Tracking**: Track and display progress
- [ ] **Error Handling**: Handle processing errors
- [ ] **Thumbnails**: Generate multiple thumbnails
- [ ] **Transcoding**: Transcode to multiple formats
- [ ] **Metadata**: Extract video metadata
- [ ] **Storage**: Optimize storage costs
- [ ] **CDN**: Use CDN for delivery
- [ ] **Cleanup**: Clean up temporary files
- [ ] **Monitoring**: Monitor processing pipeline
- [ ] **Documentation**: Document processing workflow

---

## Anti-patterns

### ❌ Don't: Synchronous Processing

```typescript
// ❌ Bad - Blocking
await uploadVideo(file)
await transcodeVideo(file)  // Blocks!
await generateThumbnail(file)
// User waits!
```

```typescript
// ✅ Good - Async processing
await uploadVideo(file)
await queueProcessing(file.id)  // Non-blocking
// User can continue
```

### ❌ Don't: No Progress

```typescript
// ❌ Bad - No progress
await uploadVideo(file)
// User doesn't know progress!
```

```typescript
// ✅ Good - Progress tracking
const upload = await uploadVideo(file, {
  onProgress: (progress) => {
    updateProgressBar(progress)
  }
})
```

---

## Integration Points

- **Video Transcoding** (`37-video-streaming/video-transcoding/`) - Transcoding patterns
- **CDN Delivery** (`37-video-streaming/cdn-delivery/`) - Video delivery
- **Adaptive Bitrate** (`37-video-streaming/adaptive-bitrate/`) - ABR streaming

---

## Further Reading

- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [AWS S3](https://aws.amazon.com/s3/)
- [Video Processing Best Practices](https://www.brightcove.com/en/resources/video-processing/)

## Resources
- [BullMQ](https://docs.bullmq.io/)
- [fluent-ffmpeg](https://github.com/fluent-ffmpeg/node-fluent-ffmpeg)
