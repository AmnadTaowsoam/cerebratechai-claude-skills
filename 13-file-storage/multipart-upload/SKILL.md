# Multipart Upload

## Overview

Multipart upload allows you to upload a single object as a set of parts. Each part is a contiguous portion of the object's data. You can upload these object parts independently and in any order. If transmission of any part fails, you can retransmit that part without affecting other parts.

## Table of Contents

1. [Multipart Upload Concepts](#multipart-upload-concepts)
2. [S3 Multipart Upload API](#s3-multipart-upload-api)
3. [Chunking Strategies](#chunking-strategies)
4. [Client-Side Implementation](#client-side-implementation)
5. [Server-Side Handling](#server-side-handling)
6. [Resume Capability](#resume-capability)
7. [Progress Tracking](#progress-tracking)
8. [Parallel Uploads](#parallel-uploads)
9. [Error Handling and Retry](#error-handling-and-retry)
10. [Completion and Verification](#completion-and-verification)
11. [Best Practices](#best-practices)

---

## Multipart Upload Concepts

### Why Use Multipart Upload?

1. **Large Files**: Upload files larger than 100MB efficiently
2. **Network Resilience**: Retry failed parts without restarting entire upload
3. **Parallel Uploads**: Upload multiple parts simultaneously
4. **Pause/Resume**: Pause and resume uploads
5. **Bandwidth Optimization**: Better utilize available bandwidth

### Multipart Upload Flow

```
1. Create Multipart Upload
   ↓
2. Upload Parts (in parallel)
   ↓
3. Complete Multipart Upload
   ↓
4. (Optional) Abort if failed
```

---

## S3 Multipart Upload API

### API Operations

| Operation | Description |
|-----------|-------------|
| `CreateMultipartUpload` | Initiates a multipart upload |
| `UploadPart` | Uploads a part in a multipart upload |
| `CompleteMultipartUpload` | Completes a multipart upload |
| `AbortMultipartUpload` | Aborts a multipart upload |
| `ListParts` | Lists the parts that have been uploaded |
| `ListMultipartUploads` | Lists all in-progress multipart uploads |

### Minimum Part Size

- **Minimum part size**: 5MB (except the last part)
- **Maximum number of parts**: 10,000
- **Maximum object size**: 5TB

---

## Chunking Strategies

### Fixed Size Chunking

```typescript
// chunking.ts
interface Chunk {
  index: number;
  start: number;
  end: number;
  size: number;
}

function calculateChunks(fileSize: number, chunkSize: number = 5 * 1024 * 1024): Chunk[] {
  const chunks: Chunk[] = [];
  const numChunks = Math.ceil(fileSize / chunkSize);

  for (let i = 0; i < numChunks; i++) {
    chunks.push({
      index: i,
      start: i * chunkSize,
      end: Math.min((i + 1) * chunkSize, fileSize),
      size: Math.min(chunkSize, fileSize - i * chunkSize),
    });
  }

  return chunks;
}

// Usage
const chunks = calculateChunks(500 * 1024 * 1024, 10 * 1024 * 1024); // 500MB file, 10MB chunks
console.log(`Total chunks: ${chunks.length}`);
```

### Adaptive Chunking

```typescript
// adaptive-chunking.ts
interface NetworkInfo {
  bandwidth: number; // bytes per second
  latency: number; // milliseconds
}

function calculateAdaptiveChunkSize(
  fileSize: number,
  networkInfo: NetworkInfo
): number {
  const { bandwidth, latency } = networkInfo;

  // Calculate optimal chunk size based on network conditions
  // Aim for chunks that take ~10-30 seconds to upload
  const targetUploadTime = 20; // seconds
  const optimalChunkSize = bandwidth * targetUploadTime;

  // Clamp between minimum and maximum
  const minChunkSize = 5 * 1024 * 1024; // 5MB
  const maxChunkSize = 5 * 1024 * 1024 * 1024; // 5GB

  return Math.max(minChunkSize, Math.min(maxChunkSize, optimalChunkSize));
}

// Usage
const networkInfo = {
  bandwidth: 10 * 1024 * 1024, // 10 Mbps
  latency: 50, // 50ms
};

const chunkSize = calculateAdaptiveChunkSize(500 * 1024 * 1024, networkInfo);
console.log(`Adaptive chunk size: ${(chunkSize / 1024 / 1024).toFixed(2)} MB`);
```

### Dynamic Chunking Based on File Size

```typescript
// dynamic-chunking.ts
function getOptimalChunkSize(fileSize: number): number {
  // Smaller files: smaller chunks
  if (fileSize < 100 * 1024 * 1024) {
    return 5 * 1024 * 1024; // 5MB
  }

  // Medium files: medium chunks
  if (fileSize < 1024 * 1024 * 1024) {
    return 10 * 1024 * 1024; // 10MB
  }

  // Large files: larger chunks
  if (fileSize < 10 * 1024 * 1024 * 1024) {
    return 25 * 1024 * 1024; // 25MB
  }

  // Very large files: largest chunks
  return 50 * 1024 * 1024; // 50MB
}
```

---

## Client-Side Implementation

### Browser-Based Multipart Upload

```typescript
// client-multipart.ts
import { S3Client, CreateMultipartUploadCommand, UploadPartCommand, CompleteMultipartUploadCommand, AbortMultipartUploadCommand } from '@aws-sdk/client-s3';

interface MultipartUploadOptions {
  file: File;
  bucket: string;
  key: string;
  chunkSize?: number;
  parallelUploads?: number;
  onProgress?: (progress: number) => void;
}

interface UploadedPart {
  PartNumber: number;
  ETag: string;
}

class MultipartUploader {
  private s3Client: S3Client;
  private uploadId?: string;
  private uploadedParts: UploadedPart[] = [];
  private abortController: AbortController;

  constructor(private options: MultipartUploadOptions) {
    this.s3Client = new S3Client({
      region: process.env.AWS_REGION,
      credentials: {
        accessKeyId: process.env.AWS_ACCESS_KEY_ID!,
        secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY!,
      },
    });
    this.abortController = new AbortController();
  }

  async start(): Promise<void> {
    const { file, bucket, key, chunkSize = 5 * 1024 * 1024, parallelUploads = 3, onProgress } = this.options;

    try {
      // Step 1: Create multipart upload
      const createCommand = new CreateMultipartUploadCommand({
        Bucket: bucket,
        Key: key,
        ContentType: file.type,
      });

      const createResponse = await this.s3Client.send(createCommand);
      this.uploadId = createResponse.UploadId;

      if (!this.uploadId) {
        throw new Error('Failed to create multipart upload');
      }

      // Step 2: Calculate chunks
      const chunks = this.calculateChunks(file.size, chunkSize);
      const totalChunks = chunks.length;

      // Step 3: Upload parts in parallel
      const uploadQueue: Promise<void>[] = [];
      let completedChunks = 0;

      for (let i = 0; i < chunks.length; i += parallelUploads) {
        const batch = chunks.slice(i, i + parallelUploads);

        for (const chunk of batch) {
          const uploadPromise = this.uploadPart(file, chunk)
            .then((part) => {
              this.uploadedParts.push(part);
              completedChunks++;

              if (onProgress) {
                onProgress((completedChunks / totalChunks) * 100);
              }
            });

          uploadQueue.push(uploadPromise);
        }

        // Wait for batch to complete before next batch
        await Promise.all(uploadQueue);
        uploadQueue.length = 0;
      }

      // Step 4: Sort parts by part number
      this.uploadedParts.sort((a, b) => a.PartNumber - b.PartNumber);

      // Step 5: Complete multipart upload
      const completeCommand = new CompleteMultipartUploadCommand({
        Bucket: bucket,
        Key: key,
        UploadId: this.uploadId,
        MultipartUpload: { Parts: this.uploadedParts },
      });

      await this.s3Client.send(completeCommand);

    } catch (error) {
      // Abort on error
      if (this.uploadId) {
        await this.abort();
      }
      throw error;
    }
  }

  private async uploadPart(file: File, chunk: { index: number; start: number; end: number }): Promise<UploadedPart> {
    const { bucket, key } = this.options;

    const blob = file.slice(chunk.start, chunk.end);
    const buffer = await blob.arrayBuffer();

    const command = new UploadPartCommand({
      Bucket: bucket,
      Key: key,
      PartNumber: chunk.index + 1,
      UploadId: this.uploadId,
      Body: new Uint8Array(buffer),
    });

    const response = await this.s3Client.send(command);

    return {
      PartNumber: chunk.index + 1,
      ETag: response.ETag!,
    };
  }

  private calculateChunks(fileSize: number, chunkSize: number) {
    const chunks = [];
    const numChunks = Math.ceil(fileSize / chunkSize);

    for (let i = 0; i < numChunks; i++) {
      chunks.push({
        index: i,
        start: i * chunkSize,
        end: Math.min((i + 1) * chunkSize, fileSize),
      });
    }

    return chunks;
  }

  async abort(): Promise<void> {
    if (!this.uploadId) return;

    const { bucket, key } = this.options;

    const command = new AbortMultipartUploadCommand({
      Bucket: bucket,
      Key: key,
      UploadId: this.uploadId,
    });

    await this.s3Client.send(command);
    this.uploadId = undefined;
    this.uploadedParts = [];
  }

  cancel(): void {
    this.abortController.abort();
  }
}

// Usage
const uploader = new MultipartUploader({
  file: selectedFile,
  bucket: 'my-bucket',
  key: `uploads/${selectedFile.name}`,
  chunkSize: 10 * 1024 * 1024, // 10MB
  parallelUploads: 3,
  onProgress: (progress) => {
    console.log(`Upload progress: ${progress.toFixed(1)}%`);
  },
});

await uploader.start();
```

### React Component

```typescript
// MultipartUpload.tsx
import React, { useState, useRef } from 'react';
import { MultipartUploader } from './client-multipart';

export function MultipartUpload() {
  const [file, setFile] = useState<File | null>(null);
  const [progress, setProgress] = useState(0);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const uploaderRef = useRef<MultipartUploader | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
      setProgress(0);
      setError(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);
    setError(null);

    const uploader = new MultipartUploader({
      file,
      bucket: 'my-bucket',
      key: `uploads/${Date.now()}-${file.name}`,
      chunkSize: 10 * 1024 * 1024,
      parallelUploads: 3,
      onProgress: setProgress,
    });

    uploaderRef.current = uploader;

    try {
      await uploader.start();
      alert('Upload complete!');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload failed');
    } finally {
      setUploading(false);
      uploaderRef.current = null;
    }
  };

  const handleCancel = () => {
    if (uploaderRef.current) {
      uploaderRef.current.cancel();
      setUploading(false);
      setProgress(0);
    }
  };

  return (
    <div className="multipart-upload">
      <input
        type="file"
        onChange={handleFileChange}
        disabled={uploading}
      />

      {file && (
        <div>
          <p>Selected: {file.name} ({(file.size / 1024 / 1024).toFixed(2)} MB)</p>

          {!uploading && (
            <button onClick={handleUpload}>Start Upload</button>
          )}

          {uploading && (
            <button onClick={handleCancel}>Cancel</button>
          )}

          {uploading && (
            <div className="progress">
              <div className="progress-bar" style={{ width: `${progress}%` }} />
              <span>{progress.toFixed(1)}%</span>
            </div>
          )}

          {error && <div className="error">{error}</div>}
        </div>
      )}
    </div>
  );
}
```

---

## Server-Side Handling

### Express Server with Multipart Upload Support

```typescript
// server-multipart.ts
import express from 'express';
import { S3Client, CreateMultipartUploadCommand, UploadPartCommand, CompleteMultipartUploadCommand, AbortMultipartUploadCommand, ListPartsCommand } from '@aws-sdk/client-s3';

const app = express();
const s3Client = new S3Client({ region: 'us-east-1' });

// Store upload state
const uploads = new Map<string, {
  uploadId: string;
  bucket: string;
  key: string;
  parts: Array<{ PartNumber: number; ETag: string }>;
  createdAt: Date;
}>();

// Initiate multipart upload
app.post('/upload/initiate', express.json(), async (req, res) => {
  try {
    const { bucket, key, contentType, fileName, fileSize } = req.body;

    const command = new CreateMultipartUploadCommand({
      Bucket: bucket,
      Key: key,
      ContentType: contentType,
      Metadata: {
        originalName: fileName,
        fileSize: fileSize.toString(),
      },
    });

    const response = await s3Client.send(command);

    if (!response.UploadId) {
      return res.status(500).json({ error: 'Failed to create upload' });
    }

    const uploadId = response.UploadId;

    uploads.set(uploadId, {
      uploadId,
      bucket,
      key,
      parts: [],
      createdAt: new Date(),
    });

    res.json({ uploadId });
  } catch (error) {
    res.status(500).json({ error: 'Failed to initiate upload' });
  }
});

// Upload part
app.post('/upload/part', express.raw({ type: 'application/octet-stream', limit: '100mb' }), async (req, res) => {
  try {
    const { uploadId, partNumber } = req.headers;

    if (!uploadId || !partNumber) {
      return res.status(400).json({ error: 'Missing headers' });
    }

    const upload = uploads.get(uploadId as string);
    if (!upload) {
      return res.status(404).json({ error: 'Upload not found' });
    }

    const command = new UploadPartCommand({
      Bucket: upload.bucket,
      Key: upload.key,
      PartNumber: parseInt(partNumber as string),
      UploadId: uploadId as string,
      Body: req.body,
    });

    const response = await s3Client.send(command);

    if (!response.ETag) {
      return res.status(500).json({ error: 'Failed to upload part' });
    }

    upload.parts.push({
      PartNumber: parseInt(partNumber as string),
      ETag: response.ETag,
    });

    res.json({ success: true, ETag: response.ETag });
  } catch (error) {
    res.status(500).json({ error: 'Failed to upload part' });
  }
});

// Complete multipart upload
app.post('/upload/complete', express.json(), async (req, res) => {
  try {
    const { uploadId } = req.body;

    const upload = uploads.get(uploadId);
    if (!upload) {
      return res.status(404).json({ error: 'Upload not found' });
    }

    // Sort parts by part number
    upload.parts.sort((a, b) => a.PartNumber - b.PartNumber);

    const command = new CompleteMultipartUploadCommand({
      Bucket: upload.bucket,
      Key: upload.key,
      UploadId: upload.uploadId,
      MultipartUpload: { Parts: upload.parts },
    });

    const response = await s3Client.send(command);

    // Clean up
    uploads.delete(uploadId);

    res.json({
      success: true,
      location: response.Location,
      bucket: upload.bucket,
      key: upload.key,
    });
  } catch (error) {
    res.status(500).json({ error: 'Failed to complete upload' });
  }
});

// Abort multipart upload
app.post('/upload/abort', express.json(), async (req, res) => {
  try {
    const { uploadId } = req.body;

    const upload = uploads.get(uploadId);
    if (!upload) {
      return res.status(404).json({ error: 'Upload not found' });
    }

    const command = new AbortMultipartUploadCommand({
      Bucket: upload.bucket,
      Key: upload.key,
      UploadId: upload.uploadId,
    });

    await s3Client.send(command);

    // Clean up
    uploads.delete(uploadId);

    res.json({ success: true });
  } catch (error) {
    res.status(500).json({ error: 'Failed to abort upload' });
  }
});

// List uploaded parts
app.get('/upload/parts/:uploadId', async (req, res) => {
  try {
    const { uploadId } = req.params;

    const upload = uploads.get(uploadId);
    if (!upload) {
      return res.status(404).json({ error: 'Upload not found' });
    }

    const command = new ListPartsCommand({
      Bucket: upload.bucket,
      Key: upload.key,
      UploadId: upload.uploadId,
    });

    const response = await s3Client.send(command);

    res.json({
      parts: response.Parts || [],
    });
  } catch (error) {
    res.status(500).json({ error: 'Failed to list parts' });
  }
});

app.listen(3000);
```

---

## Resume Capability

### Upload State Persistence

```typescript
// resume-upload.ts
import { S3Client, ListPartsCommand } from '@aws-sdk/client-s3';

interface UploadState {
  uploadId: string;
  bucket: string;
  key: string;
  fileName: string;
  fileSize: number;
  chunkSize: number;
  uploadedParts: number[];
  createdAt: Date;
}

class ResumableUploader {
  private state: UploadState | null = null;

  constructor(private s3Client: S3Client) {}

  async saveState(state: UploadState): Promise<void> {
    // Save to localStorage or IndexedDB
    localStorage.setItem(`upload_${state.uploadId}`, JSON.stringify(state));
  }

  async loadState(uploadId: string): Promise<UploadState | null> {
    const stored = localStorage.getItem(`upload_${uploadId}`);
    if (!stored) return null;

    return JSON.parse(stored) as UploadState;
  }

  async resumeUpload(uploadId: string, file: File): Promise<void> {
    const state = await this.loadState(uploadId);
    if (!state) {
      throw new Error('Upload state not found');
    }

    // Verify file matches
    if (state.fileName !== file.name || state.fileSize !== file.size) {
      throw new Error('File does not match saved state');
    }

    // List uploaded parts from S3
    const command = new ListPartsCommand({
      Bucket: state.bucket,
      Key: state.key,
      UploadId: state.uploadId,
    });

    const response = await this.s3Client.send(command);
    const uploadedPartNumbers = new Set((response.Parts || []).map(p => p.PartNumber));

    // Calculate remaining chunks
    const chunks = this.calculateChunks(file.size, state.chunkSize);
    const remainingChunks = chunks.filter(c => !uploadedPartNumbers.has(c.index + 1));

    // Upload remaining parts
    for (const chunk of remainingChunks) {
      await this.uploadPart(file, chunk, state);
    }

    // Complete upload
    await this.completeUpload(state);

    // Clean up state
    localStorage.removeItem(`upload_${uploadId}`);
  }

  private calculateChunks(fileSize: number, chunkSize: number) {
    const chunks = [];
    const numChunks = Math.ceil(fileSize / chunkSize);

    for (let i = 0; i < numChunks; i++) {
      chunks.push({
        index: i,
        start: i * chunkSize,
        end: Math.min((i + 1) * chunkSize, fileSize),
      });
    }

    return chunks;
  }

  private async uploadPart(file: File, chunk: any, state: UploadState): Promise<void> {
    // Upload part logic
  }

  private async completeUpload(state: UploadState): Promise<void> {
    // Complete upload logic
  }
}
```

### IndexedDB Storage

```typescript
// indexeddb-storage.ts
class UploadStateDB {
  private db: IDBDatabase | null = null;

  async init(): Promise<void> {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open('UploadStateDB', 1);

      request.onerror = () => reject(request.error);
      request.onsuccess = () => {
        this.db = request.result;
        resolve();
      };

      request.onupgradeneeded = (event) => {
        const db = (event.target as IDBOpenDBRequest).result;
        if (!db.objectStoreNames.contains('uploads')) {
          db.createObjectStore('uploads', { keyPath: 'uploadId' });
        }
      };
    });
  }

  async saveState(state: UploadState): Promise<void> {
    if (!this.db) await this.init();

    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction(['uploads'], 'readwrite');
      const store = transaction.objectStore('uploads');
      const request = store.put(state);

      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve();
    });
  }

  async loadState(uploadId: string): Promise<UploadState | null> {
    if (!this.db) await this.init();

    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction(['uploads'], 'readonly');
      const store = transaction.objectStore('uploads');
      const request = store.get(uploadId);

      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve(request.result || null);
    });
  }

  async deleteState(uploadId: string): Promise<void> {
    if (!this.db) await this.init();

    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction(['uploads'], 'readwrite');
      const store = transaction.objectStore('uploads');
      const request = store.delete(uploadId);

      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve();
    });
  }

  async listStates(): Promise<UploadState[]> {
    if (!this.db) await this.init();

    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction(['uploads'], 'readonly');
      const store = transaction.objectStore('uploads');
      const request = store.getAll();

      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve(request.result || []);
    });
  }
}
```

---

## Progress Tracking

### Detailed Progress Tracking

```typescript
// progress-tracking.ts
interface UploadProgress {
  uploadId: string;
  fileName: string;
  fileSize: number;
  uploadedBytes: number;
  totalBytes: number;
  percentage: number;
  speed: number; // bytes per second
  eta: number; // seconds remaining
  partsCompleted: number;
  totalParts: number;
  currentPart: number;
}

class ProgressTracker {
  private startTime: number = 0;
  private lastUpdateTime: number = 0;
  private lastUploadedBytes: number = 0;
  private uploadedBytes: number = 0;
  private partsCompleted: number = 0;

  constructor(private totalBytes: number, private totalParts: number) {
    this.startTime = Date.now();
    this.lastUpdateTime = this.startTime;
  }

  updateProgress(partSize: number): UploadProgress {
    this.uploadedBytes += partSize;
    this.partsCompleted++;

    const now = Date.now();
    const timeElapsed = (now - this.startTime) / 1000; // seconds

    // Calculate speed
    const bytesSinceLastUpdate = this.uploadedBytes - this.lastUploadedBytes;
    const timeSinceLastUpdate = (now - this.lastUpdateTime) / 1000;
    const speed = bytesSinceLastUpdate / timeSinceLastUpdate;

    this.lastUploadedBytes = this.uploadedBytes;
    this.lastUpdateTime = now;

    // Calculate ETA
    const remainingBytes = this.totalBytes - this.uploadedBytes;
    const eta = speed > 0 ? remainingBytes / speed : 0;

    return {
      uploadId: '',
      fileName: '',
      fileSize: this.totalBytes,
      uploadedBytes: this.uploadedBytes,
      totalBytes: this.totalBytes,
      percentage: (this.uploadedBytes / this.totalBytes) * 100,
      speed,
      eta,
      partsCompleted: this.partsCompleted,
      totalParts: this.totalParts,
      currentPart: this.partsCompleted,
    };
  }

  formatProgress(progress: UploadProgress): string {
    return [
      `Progress: ${progress.percentage.toFixed(1)}%`,
      `Speed: ${(progress.speed / 1024 / 1024).toFixed(2)} MB/s`,
      `ETA: ${this.formatTime(progress.eta)}`,
      `Parts: ${progress.partsCompleted}/${progress.totalParts}`,
    ].join(' | ');
  }

  private formatTime(seconds: number): string {
    if (seconds < 60) return `${Math.round(seconds)}s`;
    if (seconds < 3600) return `${Math.round(seconds / 60)}m ${Math.round(seconds % 60)}s`;
    return `${Math.floor(seconds / 3600)}h ${Math.round((seconds % 3600) / 60)}m`;
  }
}
```

### WebSocket Progress Broadcasting

```typescript
// websocket-progress.ts
import WebSocket from 'ws';

const wss = new WebSocket.Server({ port: 8080 });

interface ProgressMessage {
  type: 'progress';
  uploadId: string;
  data: UploadProgress;
}

wss.on('connection', (ws) => {
  ws.on('message', (message) => {
    const data = JSON.parse(message.toString());

    if (data.type === 'subscribe') {
      // Subscribe to progress updates for a specific upload
      ws.uploadId = data.uploadId;
    }
  });
});

function broadcastProgress(uploadId: string, progress: UploadProgress): void {
  const message: ProgressMessage = {
    type: 'progress',
    uploadId,
    data: progress,
  };

  wss.clients.forEach((client) => {
    if (client.readyState === WebSocket.OPEN && client.uploadId === uploadId) {
      client.send(JSON.stringify(message));
    }
  });
}
```

---

## Parallel Uploads

### Parallel Upload Manager

```typescript
// parallel-upload.ts
interface UploadTask {
  chunk: { index: number; start: number; end: number };
  file: File;
  bucket: string;
  key: string;
  uploadId: string;
}

class ParallelUploadManager {
  private concurrency: number;
  private queue: UploadTask[] = [];
  private activeUploads: Set<Promise<any>> = new Set();
  private results: Array<{ PartNumber: number; ETag: string }> = [];

  constructor(concurrency: number = 3) {
    this.concurrency = concurrency;
  }

  async uploadParts(file: File, chunks: any[], bucket: string, key: string, uploadId: string): Promise<any[]> {
    // Create upload tasks
    this.queue = chunks.map((chunk) => ({
      chunk,
      file,
      bucket,
      key,
      uploadId,
    }));

    // Process queue
    await this.processQueue();

    // Sort results by part number
    this.results.sort((a, b) => a.PartNumber - b.PartNumber);

    return this.results;
  }

  private async processQueue(): Promise<void> {
    while (this.queue.length > 0 || this.activeUploads.size > 0) {
      // Start new uploads if under concurrency limit
      while (this.activeUploads.size < this.concurrency && this.queue.length > 0) {
        const task = this.queue.shift()!;
        const uploadPromise = this.uploadPart(task);
        this.activeUploads.add(uploadPromise);

        uploadPromise
          .then((result) => {
            this.results.push(result);
          })
          .finally(() => {
            this.activeUploads.delete(uploadPromise);
          });
      }

      // Wait for at least one upload to complete
      if (this.activeUploads.size > 0) {
        await Promise.race(this.activeUploads);
      }
    }
  }

  private async uploadPart(task: UploadTask): Promise<{ PartNumber: number; ETag: string }> {
    const { chunk, file, bucket, key, uploadId } = task;

    const blob = file.slice(chunk.start, chunk.end);
    const buffer = await blob.arrayBuffer();

    const command = new UploadPartCommand({
      Bucket: bucket,
      Key: key,
      PartNumber: chunk.index + 1,
      UploadId: uploadId,
      Body: new Uint8Array(buffer),
    });

    const response = await s3Client.send(command);

    return {
      PartNumber: chunk.index + 1,
      ETag: response.ETag!,
    };
  }
}
```

### Adaptive Concurrency

```typescript
// adaptive-concurrency.ts
class AdaptiveConcurrencyManager {
  private minConcurrency: number = 1;
  private maxConcurrency: number = 10;
  private currentConcurrency: number = 3;
  private successCount: number = 0;
  private errorCount: number = 0;
  private lastAdjustment: number = Date.now();

  adjustConcurrency(success: boolean): number {
    const now = Date.now();
    const timeSinceLastAdjustment = now - this.lastAdjustment;

    // Only adjust every 5 seconds
    if (timeSinceLastAdjustment < 5000) {
      return this.currentConcurrency;
    }

    if (success) {
      this.successCount++;
    } else {
      this.errorCount++;
    }

    // Adjust based on success/error ratio
    const total = this.successCount + this.errorCount;
    const successRate = this.successCount / total;

    if (successRate > 0.95 && this.currentConcurrency < this.maxConcurrency) {
      // Increase concurrency
      this.currentConcurrency = Math.min(this.maxConcurrency, this.currentConcurrency + 1);
    } else if (successRate < 0.8 && this.currentConcurrency > this.minConcurrency) {
      // Decrease concurrency
      this.currentConcurrency = Math.max(this.minConcurrency, this.currentConcurrency - 1);
    }

    // Reset counters
    this.successCount = 0;
    this.errorCount = 0;
    this.lastAdjustment = now;

    return this.currentConcurrency;
  }
}
```

---

## Error Handling and Retry

### Exponential Backoff Retry

```typescript
// retry.ts
interface RetryOptions {
  maxRetries: number;
  baseDelay: number;
  maxDelay: number;
  backoffMultiplier: number;
}

class RetryHandler {
  constructor(private options: RetryOptions = {
    maxRetries: 3,
    baseDelay: 1000,
    maxDelay: 30000,
    backoffMultiplier: 2,
  }) {}

  async retry<T>(
    fn: () => Promise<T>,
    context: string
  ): Promise<T> {
    let lastError: Error | null = null;

    for (let attempt = 0; attempt <= this.options.maxRetries; attempt++) {
      try {
        return await fn();
      } catch (error) {
        lastError = error as Error;

        // Don't retry on certain errors
        if (this.shouldNotRetry(error)) {
          throw error;
        }

        if (attempt < this.options.maxRetries) {
          const delay = this.calculateDelay(attempt);
          console.warn(`Retry ${attempt + 1}/${this.options.maxRetries} for ${context} after ${delay}ms`);

          await this.sleep(delay);
        }
      }
    }

    throw lastError;
  }

  private calculateDelay(attempt: number): number {
    const delay = this.options.baseDelay * Math.pow(this.options.backoffMultiplier, attempt);
    return Math.min(delay, this.options.maxDelay);
  }

  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  private shouldNotRetry(error: any): boolean {
    // Don't retry on authentication errors
    if (error.name === 'InvalidAccessKeyId' || error.name === 'SignatureDoesNotMatch') {
      return true;
    }

    // Don't retry on file not found
    if (error.name === 'NoSuchUpload') {
      return true;
    }

    return false;
  }
}

// Usage
const retryHandler = new RetryHandler();

await retryHandler.retry(
  () => uploadPart(file, chunk, uploadId),
  `Part ${chunk.index + 1}`
);
```

### Part-Level Error Handling

```typescript
// part-error-handler.ts
interface PartUploadResult {
  partNumber: number;
  success: boolean;
  etag?: string;
  error?: Error;
  retries: number;
}

class PartUploadHandler {
  private results: Map<number, PartUploadResult> = new Map();
  private retryHandler: RetryHandler;

  constructor(retryHandler: RetryHandler) {
    this.retryHandler = retryHandler;
  }

  async uploadPartWithRetry(
    file: File,
    chunk: any,
    bucket: string,
    key: string,
    uploadId: string
  ): Promise<PartUploadResult> {
    const partNumber = chunk.index + 1;
    let retries = 0;

    try {
      const etag = await this.retryHandler.retry(
        () => this.uploadPart(file, chunk, bucket, key, uploadId),
        `Part ${partNumber}`
      );

      const result: PartUploadResult = {
        partNumber,
        success: true,
        etag,
        retries: this.retryHandler['options'].maxRetries - this.retryHandler['options'].maxRetries,
      };

      this.results.set(partNumber, result);
      return result;

    } catch (error) {
      const result: PartUploadResult = {
        partNumber,
        success: false,
        error: error as Error,
        retries: this.retryHandler['options'].maxRetries,
      };

      this.results.set(partNumber, result);
      return result;
    }
  }

  private async uploadPart(
    file: File,
    chunk: any,
    bucket: string,
    key: string,
    uploadId: string
  ): Promise<string> {
    const blob = file.slice(chunk.start, chunk.end);
    const buffer = await blob.arrayBuffer();

    const command = new UploadPartCommand({
      Bucket: bucket,
      Key: key,
      PartNumber: chunk.index + 1,
      UploadId: uploadId,
      Body: new Uint8Array(buffer),
    });

    const response = await s3Client.send(command);
    return response.ETag!;
  }

  getResults(): PartUploadResult[] {
    return Array.from(this.results.values());
  }

  getFailedParts(): PartUploadResult[] {
    return this.getResults().filter(r => !r.success);
  }
}
```

---

## Completion and Verification

### Complete Multipart Upload

```typescript
// completion.ts
async function completeMultipartUpload(
  bucket: string,
  key: string,
  uploadId: string,
  parts: Array<{ PartNumber: number; ETag: string }>
): Promise<string> {
  const command = new CompleteMultipartUploadCommand({
    Bucket: bucket,
    Key: key,
    UploadId: uploadId,
    MultipartUpload: { Parts: parts },
  });

  const response = await s3Client.send(command);
  return response.Location!;
}
```

### Verify Upload

```typescript
// verification.ts
import { HeadObjectCommand, GetObjectCommand } from '@aws-sdk/client-s3';

async function verifyUpload(
  bucket: string,
  key: string,
  expectedSize: number
): Promise<{ success: boolean; actualSize: number }> {
  try {
    const command = new HeadObjectCommand({
      Bucket: bucket,
      Key: key,
    });

    const response = await s3Client.send(command);

    const actualSize = response.ContentLength || 0;

    return {
      success: actualSize === expectedSize,
      actualSize,
    };
  } catch (error) {
    console.error('Verification failed:', error);
    return {
      success: false,
      actualSize: 0,
    };
  }
}

async function verifyWithChecksum(
  bucket: string,
  key: string,
  expectedChecksum: string
): Promise<boolean> {
  const command = new GetObjectCommand({
    Bucket: bucket,
    Key: key,
  });

  const response = await s3Client.send(command);

  // Calculate checksum of downloaded object
  const chunks: Uint8Array[] = [];
  // @ts-ignore
  for await (const chunk of response.Body) {
    chunks.push(chunk);
  }

  const buffer = Buffer.concat(chunks);
  const actualChecksum = calculateChecksum(buffer);

  return actualChecksum === expectedChecksum;
}

function calculateChecksum(buffer: Buffer): string {
  // Implement your checksum algorithm (MD5, SHA256, etc.)
  const crypto = require('crypto');
  return crypto.createHash('md5').update(buffer).digest('hex');
}
```

---

## Best Practices

### 1. Choose Appropriate Chunk Size

```typescript
// best-practices.ts

// For files < 100MB: Use simple upload
function shouldUseMultipartUpload(fileSize: number): boolean {
  return fileSize >= 100 * 1024 * 1024; // 100MB threshold
}

// For files 100MB - 1GB: 5-10MB chunks
function getOptimalChunkSize(fileSize: number): number {
  if (fileSize < 1024 * 1024 * 1024) {
    return 5 * 1024 * 1024; // 5MB
  }

  if (fileSize < 5 * 1024 * 1024 * 1024) {
    return 10 * 1024 * 1024; // 10MB
  }

  return 25 * 1024 * 1024; // 25MB
}
```

### 2. Handle Network Interruptions

```typescript
// network-handling.ts

class NetworkAwareUploader {
  private isOnline: boolean = navigator.onLine;

  constructor() {
    window.addEventListener('online', () => this.handleOnline());
    window.addEventListener('offline', () => this.handleOffline());
  }

  private handleOnline(): void {
    this.isOnline = true;
    console.log('Network is online. Resuming uploads...');
    // Resume uploads
  }

  private handleOffline(): void {
    this.isOnline = false;
    console.log('Network is offline. Pausing uploads...');
    // Pause uploads
  }

  async uploadWithNetworkCheck(file: File): Promise<void> {
    if (!this.isOnline) {
      throw new Error('Network is offline');
    }

    // Proceed with upload
  }
}
```

### 3. Clean Up Incomplete Uploads

```typescript
// cleanup.ts

async function cleanupIncompleteUploads(bucket: string, maxAge: number = 24 * 60 * 60 * 1000): Promise<void> {
  const command = new ListMultipartUploadsCommand({
    Bucket: bucket,
  });

  const response = await s3Client.send(command);

  if (!response.Uploads) return;

  const now = Date.now();

  for (const upload of response.Uploads) {
    const initiatedDate = upload.Initiated?.getTime() || 0;
    const age = now - initiatedDate;

    if (age > maxAge) {
      console.log(`Aborting old upload: ${upload.UploadId}`);

      await s3Client.send(new AbortMultipartUploadCommand({
        Bucket: bucket,
        Key: upload.Key!,
        UploadId: upload.UploadId!,
      }));
    }
  }
}
```

### 4. Monitor Upload Progress

```typescript
// monitoring.ts

class UploadMonitor {
  private uploads: Map<string, UploadProgress> = new Map();

  startMonitoring(uploadId: string, fileName: string, fileSize: number): void {
    this.uploads.set(uploadId, {
      uploadId,
      fileName,
      fileSize,
      uploadedBytes: 0,
      totalBytes: fileSize,
      percentage: 0,
      speed: 0,
      eta: 0,
      partsCompleted: 0,
      totalParts: 0,
      currentPart: 0,
    });
  }

  updateProgress(uploadId: string, uploadedBytes: number): void {
    const progress = this.uploads.get(uploadId);
    if (!progress) return;

    progress.uploadedBytes = uploadedBytes;
    progress.percentage = (uploadedBytes / progress.totalBytes) * 100;

    // Calculate speed and ETA
    const now = Date.now();
    const elapsed = (now - this.startTime) / 1000;
    progress.speed = uploadedBytes / elapsed;
    progress.eta = (progress.totalBytes - uploadedBytes) / progress.speed;

    // Log progress
    console.log(`Upload ${uploadId}: ${progress.percentage.toFixed(1)}%`);
  }

  completeUpload(uploadId: string): void {
    const progress = this.uploads.get(uploadId);
    if (!progress) return;

    console.log(`Upload ${uploadId} completed in ${progress.eta.toFixed(0)}s`);
    this.uploads.delete(uploadId);
  }
}
```

### 5. Use Presigned URLs for Client-Side Uploads

```typescript
// presigned-multipart.ts

async function getPresignedUrlsForParts(
  bucket: string,
  key: string,
  uploadId: string,
  partCount: number
): Promise<string[]> {
  const urls: string[] = [];

  for (let partNumber = 1; partNumber <= partCount; partNumber++) {
    const command = new UploadPartCommand({
      Bucket: bucket,
      Key: key,
      PartNumber: partNumber,
      UploadId: uploadId,
    });

    const url = await getSignedUrl(s3Client, command, { expiresIn: 3600 });
    urls.push(url);
  }

  return urls;
}
```

---

## Summary

This skill covers comprehensive multipart upload implementation including:

- **Multipart Upload Concepts**: Understanding when and why to use multipart upload
- **S3 Multipart Upload API**: All API operations and their usage
- **Chunking Strategies**: Fixed size, adaptive, and dynamic chunking
- **Client-Side Implementation**: Browser-based upload with React component
- **Server-Side Handling**: Express server with multipart upload endpoints
- **Resume Capability**: Upload state persistence with localStorage and IndexedDB
- **Progress Tracking**: Detailed progress tracking and WebSocket broadcasting
- **Parallel Uploads**: Parallel upload manager with adaptive concurrency
- **Error Handling and Retry**: Exponential backoff and part-level error handling
- **Completion and Verification**: Completing uploads and verifying integrity
- **Best Practices**: Chunk size selection, network handling, cleanup, monitoring, and presigned URLs
