# File Upload Handling

## Overview

Secure file upload handling is critical for web applications. This skill covers various upload methods, validation strategies, security considerations, and production-ready patterns for handling file uploads.

## Table of Contents

1. [Upload Methods](#upload-methods)
2. [Validation](#validation)
3. [Temporary Storage](#temporary-storage)
4. [Progress Tracking](#progress-tracking)
5. [Error Handling](#error-handling)
6. [Security Considerations](#security-considerations)
7. [Image Processing](#image-processing)
8. [Metadata Extraction](#metadata-extraction)
9. [Database Records](#database-records)
10. [Production Patterns](#production-patterns)

---

## Upload Methods

### 1. Form Upload (Multipart/Form-Data)

#### Node.js/Express

```typescript
// server.ts
import express from 'express';
import multer from 'multer';
import path from 'path';

const app = express();

// Configure multer storage
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/');
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1e9);
    cb(null, file.fieldname + '-' + uniqueSuffix + path.extname(file.originalname));
  },
});

const upload = multer({
  storage,
  limits: {
    fileSize: 10 * 1024 * 1024, // 10MB
  },
  fileFilter: (req, file, cb) => {
    const allowedTypes = /jpeg|jpg|png|gif|pdf|doc|docx/;
    const extname = allowedTypes.test(path.extname(file.originalname).toLowerCase());
    const mimetype = allowedTypes.test(file.mimetype);

    if (extname && mimetype) {
      cb(null, true);
    } else {
      cb(new Error('Invalid file type'));
    }
  },
});

// Single file upload
app.post('/upload', upload.single('file'), (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: 'No file uploaded' });
  }

  res.json({
    filename: req.file.filename,
    originalName: req.file.originalname,
    size: req.file.size,
    mimetype: req.file.mimetype,
    path: req.file.path,
  });
});

// Multiple files upload
app.post('/upload/multiple', upload.array('files', 5), (req, res) => {
  if (!req.files || !Array.isArray(req.files)) {
    return res.status(400).json({ error: 'No files uploaded' });
  }

  res.json({
    count: req.files.length,
    files: req.files.map(file => ({
      filename: file.filename,
      originalName: file.originalname,
      size: file.size,
    })),
  });
});

app.listen(3000);
```

#### Python/FastAPI

```python
# server.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
import aiofiles
import os

app = FastAPI()
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Allowed file types
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".pdf", ".doc", ".docx"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def validate_file(file: UploadFile) -> bool:
    """Validate file type and size."""
    if file.size > MAX_FILE_SIZE:
        return False
    
    ext = Path(file.filename).suffix.lower()
    return ext in ALLOWED_EXTENSIONS

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a single file."""
    if not validate_file(file):
        raise HTTPException(status_code=400, detail="Invalid file type or size")
    
    # Generate unique filename
    import uuid
    file_ext = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = UPLOAD_DIR / unique_filename
    
    # Save file
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    return JSONResponse({
        "filename": unique_filename,
        "originalName": file.filename,
        "size": len(content),
        "mimetype": file.content_type
    })

@app.post("/upload/multiple")
async def upload_multiple_files(files: list[UploadFile] = File(...)):
    """Upload multiple files."""
    uploaded_files = []
    
    for file in files:
        if not validate_file(file):
            continue
        
        import uuid
        file_ext = Path(file.filename).suffix
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = UPLOAD_DIR / unique_filename
        
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        uploaded_files.append({
            "filename": unique_filename,
            "originalName": file.filename,
            "size": len(content)
        })
    
    return JSONResponse({
        "count": len(uploaded_files),
        "files": uploaded_files
    })
```

### 2. Direct S3 Upload

#### Presigned URL Generation

```typescript
// s3-upload.ts
import { getSignedUrl } from '@aws-sdk/s3-request-presigner';
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3';

const s3Client = new S3Client({
  region: process.env.AWS_REGION,
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID!,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY!,
  },
});

interface UploadUrlParams {
  bucket: string;
  key: string;
  contentType: string;
  expiresIn?: number;
}

async function generateUploadUrl(params: UploadUrlParams): Promise<string> {
  const command = new PutObjectCommand({
    Bucket: params.bucket,
    Key: params.key,
    ContentType: params.contentType,
  });

  return await getSignedUrl(s3Client, command, {
    expiresIn: params.expiresIn || 3600,
  });
}

// Express endpoint
app.post('/upload/url', async (req, res) => {
  const { filename, contentType } = req.body;
  
  const key = `uploads/${Date.now()}-${filename}`;
  const uploadUrl = await generateUploadUrl({
    bucket: 'my-bucket',
    key,
    contentType,
  });

  res.json({ uploadUrl, key });
});
```

```python
# s3_upload.py
import boto3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import timedelta

s3_client = boto3.client('s3')

class UploadUrlRequest(BaseModel):
    filename: str
    content_type: str

app = FastAPI()

@app.post("/upload/url")
async def generate_upload_url(request: UploadUrlRequest):
    """Generate a presigned URL for direct S3 upload."""
    import time
    key = f"uploads/{int(time.time())}-{request.filename}"
    
    upload_url = s3_client.generate_presigned_url(
        'put_object',
        Params={
            'Bucket': 'my-bucket',
            'Key': key,
            'ContentType': request.content_type
        },
        ExpiresIn=3600
    )
    
    return {"upload_url": upload_url, "key": key}
```

#### Client-Side Upload with Presigned URL

```typescript
// client-upload.ts
async function uploadToS3(
  file: File,
  uploadUrl: string,
  onProgress?: (progress: number) => void
): Promise<void> {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();

    xhr.upload.addEventListener('progress', (e) => {
      if (e.lengthComputable && onProgress) {
        onProgress((e.loaded / e.total) * 100);
      }
    });

    xhr.addEventListener('load', () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        resolve();
      } else {
        reject(new Error('Upload failed'));
      }
    });

    xhr.addEventListener('error', () => {
      reject(new Error('Upload failed'));
    });

    xhr.open('PUT', uploadUrl);
    xhr.setRequestHeader('Content-Type', file.type);
    xhr.send(file);
  });
}

// React component
import React, { useState } from 'react';

function FileUpload() {
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    try {
      setUploading(true);
      
      // Get upload URL
      const response = await fetch('/upload/url', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          filename: file.name,
          contentType: file.type,
        }),
      });
      
      const { uploadUrl } = await response.json();
      
      // Upload directly to S3
      await uploadToS3(file, uploadUrl, (p) => setProgress(p));
      
      alert('Upload complete!');
    } catch (error) {
      console.error('Upload failed:', error);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <input type="file" onChange={handleUpload} disabled={uploading} />
      {uploading && <div>Progress: {progress.toFixed(1)}%</div>}
    </div>
  );
}
```

### 3. Chunked Upload

#### Server-Side Chunk Handling

```typescript
// chunked-upload.ts
import express from 'express';
import fs from 'fs';
import path from 'path';

const app = express();
const CHUNKS_DIR = path.join(__dirname, 'chunks');
const UPLOADS_DIR = path.join(__dirname, 'uploads');

// Ensure directories exist
[CHUNKS_DIR, UPLOADS_DIR].forEach(dir => {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
});

// Upload chunk
app.post('/upload/chunk', express.raw({ type: 'application/octet-stream', limit: '100mb' }), (req, res) => {
  const { fileId, chunkIndex, totalChunks, fileName } = req.headers;
  
  if (!fileId || !chunkIndex || !totalChunks || !fileName) {
    return res.status(400).json({ error: 'Missing headers' });
  }

  const chunkPath = path.join(CHUNKS_DIR, `${fileId}-${chunkIndex}`);
  fs.writeFileSync(chunkPath, req.body);

  res.json({ received: true });
});

// Complete upload
app.post('/upload/complete', express.json(), (req, res) => {
  const { fileId, fileName, totalChunks } = req.body;
  
  const outputPath = path.join(UPLOADS_DIR, fileName);
  const writeStream = fs.createWriteStream(outputPath);

  for (let i = 0; i < totalChunks; i++) {
    const chunkPath = path.join(CHUNKS_DIR, `${fileId}-${i}`);
    const chunk = fs.readFileSync(chunkPath);
    writeStream.write(chunk);
    fs.unlinkSync(chunkPath); // Delete chunk after writing
  }

  writeStream.end();

  res.json({ success: true, path: outputPath });
});
```

#### Client-Side Chunk Upload

```typescript
// chunked-upload-client.ts
async function uploadInChunks(
  file: File,
  chunkSize: number = 5 * 1024 * 1024, // 5MB
  onProgress?: (progress: number) => void
): Promise<void> {
  const fileId = `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  const totalChunks = Math.ceil(file.size / chunkSize);

  for (let chunkIndex = 0; chunkIndex < totalChunks; chunkIndex++) {
    const start = chunkIndex * chunkSize;
    const end = Math.min(start + chunkSize, file.size);
    const chunk = file.slice(start, end);

    await fetch('/upload/chunk', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/octet-stream',
        'file-id': fileId,
        'chunk-index': chunkIndex.toString(),
        'total-chunks': totalChunks.toString(),
        'file-name': file.name,
      },
      body: chunk,
    });

    if (onProgress) {
      onProgress(((chunkIndex + 1) / totalChunks) * 100);
    }
  }

  // Complete upload
  await fetch('/upload/complete', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      fileId,
      fileName: file.name,
      totalChunks,
    }),
  });
}
```

---

## Validation

### 1. File Type Validation

```typescript
// validation.ts
import path from 'path';

// Allowed MIME types
const ALLOWED_MIME_TYPES = new Set([
  'image/jpeg',
  'image/jpg',
  'image/png',
  'image/gif',
  'image/webp',
  'application/pdf',
  'application/msword',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
]);

// Allowed extensions
const ALLOWED_EXTENSIONS = new Set([
  '.jpg', '.jpeg', '.png', '.gif', '.webp',
  '.pdf', '.doc', '.docx',
]);

function validateFileType(file: Express.Multer.File): boolean {
  // Check extension
  const ext = path.extname(file.originalname).toLowerCase();
  if (!ALLOWED_EXTENSIONS.has(ext)) {
    return false;
  }

  // Check MIME type
  if (!ALLOWED_MIME_TYPES.has(file.mimetype)) {
    return false;
  }

  // Additional: Check file signature (magic bytes)
  return checkFileSignature(file.buffer, ext);
}

function checkFileSignature(buffer: Buffer, ext: string): boolean {
  const signatures: Record<string, number[]> = {
    '.jpg': [0xFF, 0xD8, 0xFF],
    '.png': [0x89, 0x50, 0x4E, 0x47],
    '.gif': [0x47, 0x49, 0x46],
    '.pdf': [0x25, 0x50, 0x44, 0x46],
  };

  const signature = signatures[ext];
  if (!signature) return true; // No signature check available

  for (let i = 0; i < signature.length; i++) {
    if (buffer[i] !== signature[i]) {
      return false;
    }
  }

  return true;
}
```

```python
# validation.py
import magic
from pathlib import Path

ALLOWED_MIME_TYPES = {
    'image/jpeg',
    'image/png',
    'image/gif',
    'image/webp',
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
}

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.pdf', '.doc', '.docx'}

def validate_file_type(file_content: bytes, filename: str) -> bool:
    """Validate file type using both extension and MIME type."""
    # Check extension
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False
    
    # Check MIME type using python-magic
    mime = magic.from_buffer(file_content, mime=True)
    return mime in ALLOWED_MIME_TYPES
```

### 2. File Size Validation

```typescript
// size-validation.ts
const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB

function validateFileSize(file: Express.Multer.File): boolean {
  return file.size <= MAX_FILE_SIZE;
}

// Express middleware
function fileSizeLimit(limit: number) {
  return (req: any, res: any, next: any) => {
    const contentLength = parseInt(req.headers['content-length'] || '0');
    
    if (contentLength > limit) {
      return res.status(413).json({
        error: `File size exceeds limit of ${limit / 1024 / 1024}MB`,
      });
    }
    
    next();
  };
}

app.post('/upload', fileSizeLimit(MAX_FILE_SIZE), upload.single('file'), ...);
```

```python
# size_validation.py
from fastapi import HTTPException, Request

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

async def validate_file_size(request: Request):
    """Validate file size before processing."""
    content_length = request.headers.get('content-length')
    if content_length and int(content_length) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File size exceeds limit of {MAX_FILE_SIZE / 1024 / 1024}MB"
        )
```

### 3. Virus Scanning

```typescript
// virus-scan.ts
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

async function scanForVirus(filePath: string): Promise<boolean> {
  try {
    // Using ClamAV
    const { stdout } = await execAsync(`clamscan --no-summary ${filePath}`);
    
    if (stdout.includes('OK')) {
      return true; // No virus found
    } else {
      return false; // Virus found
    }
  } catch (error) {
    console.error('Virus scan failed:', error);
    throw new Error('Virus scan failed');
  }
}

// Integration with upload
app.post('/upload', upload.single('file'), async (req, res) => {
  try {
    const isClean = await scanForVirus(req.file.path);
    
    if (!isClean) {
      fs.unlinkSync(req.file.path); // Delete infected file
      return res.status(400).json({ error: 'File contains virus' });
    }
    
    // Process clean file
    res.json({ success: true });
  } catch (error) {
    res.status(500).json({ error: 'Upload failed' });
  }
});
```

```python
# virus_scan.py
import subprocess
from fastapi import HTTPException

async def scan_for_virus(file_path: str) -> bool:
    """Scan file for viruses using ClamAV."""
    try:
        result = subprocess.run(
            ['clamscan', '--no-summary', file_path],
            capture_output=True,
            text=True
        )
        
        if 'OK' in result.stdout:
            return True  # No virus found
        else:
            return False  # Virus found
    except subprocess.CalledProcessError as e:
        print(f"Virus scan failed: {e}")
        raise HTTPException(status_code=500, detail="Virus scan failed")
```

---

## Temporary Storage

### Temporary Upload Directory

```typescript
// temp-storage.ts
import fs from 'fs';
import path from 'path';
import { v4 as uuidv4 } from 'uuid';

const TEMP_DIR = path.join(__dirname, 'temp-uploads');

// Ensure temp directory exists
if (!fs.existsSync(TEMP_DIR)) {
  fs.mkdirSync(TEMP_DIR, { recursive: true });
}

interface TempFile {
  id: string;
  path: string;
  originalName: string;
  createdAt: Date;
}

const tempFiles = new Map<string, TempFile>();

function saveTempFile(buffer: Buffer, originalName: string): TempFile {
  const id = uuidv4();
  const filename = `${id}-${originalName}`;
  const filePath = path.join(TEMP_DIR, filename);
  
  fs.writeFileSync(filePath, buffer);
  
  const tempFile: TempFile = {
    id,
    path: filePath,
    originalName,
    createdAt: new Date(),
  };
  
  tempFiles.set(id, tempFile);
  
  // Auto-cleanup after 1 hour
  setTimeout(() => cleanupTempFile(id), 60 * 60 * 1000);
  
  return tempFile;
}

function cleanupTempFile(id: string): void {
  const tempFile = tempFiles.get(id);
  if (tempFile && fs.existsSync(tempFile.path)) {
    fs.unlinkSync(tempFile.path);
    tempFiles.delete(id);
  }
}

function getTempFile(id: string): TempFile | undefined {
  return tempFiles.get(id);
}

// Cleanup old files periodically
setInterval(() => {
  const now = new Date();
  for (const [id, tempFile] of tempFiles) {
    const age = now.getTime() - tempFile.createdAt.getTime();
    if (age > 60 * 60 * 1000) { // 1 hour
      cleanupTempFile(id);
    }
  }
}, 5 * 60 * 1000); // Check every 5 minutes
```

```python
# temp_storage.py
import os
import shutil
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict

TEMP_DIR = Path("temp-uploads")
TEMP_DIR.mkdir(exist_ok=True)

class TempFile:
    def __init__(self, id: str, path: Path, original_name: str, created_at: datetime):
        self.id = id
        self.path = path
        self.original_name = original_name
        self.created_at = created_at

temp_files: Dict[str, TempFile] = {}

def save_temp_file(content: bytes, original_name: str) -> TempFile:
    """Save a file to temporary storage."""
    file_id = str(uuid.uuid4())
    filename = f"{file_id}-{original_name}"
    file_path = TEMP_DIR / filename
    
    with open(file_path, 'wb') as f:
        f.write(content)
    
    temp_file = TempFile(
        id=file_id,
        path=file_path,
        original_name=original_name,
        created_at=datetime.now()
    )
    
    temp_files[file_id] = temp_file
    return temp_file

def cleanup_temp_file(file_id: str) -> None:
    """Remove a file from temporary storage."""
    temp_file = temp_files.get(file_id)
    if temp_file and temp_file.path.exists():
        temp_file.path.unlink()
        del temp_files[file_id]

def get_temp_file(file_id: str) -> TempFile | None:
    """Get a file from temporary storage."""
    return temp_files.get(file_id)

def cleanup_old_files(max_age: timedelta = timedelta(hours=1)) -> None:
    """Clean up files older than max_age."""
    now = datetime.now()
    to_delete = []
    
    for file_id, temp_file in temp_files.items():
        age = now - temp_file.created_at
        if age > max_age:
            to_delete.append(file_id)
    
    for file_id in to_delete:
        cleanup_temp_file(file_id)
```

---

## Progress Tracking

### WebSocket Progress Tracking

```typescript
// progress-websocket.ts
import WebSocket from 'ws';
import { v4 as uuidv4 } from 'uuid';

const wss = new WebSocket.Server({ port: 8080 });

const uploads = new Map<string, { progress: number; status: string }>();

wss.on('connection', (ws) => {
  ws.on('message', (message) => {
    const data = JSON.parse(message.toString());
    
    if (data.type === 'subscribe') {
      uploads.set(data.uploadId, { progress: 0, status: 'pending' });
    }
  });
});

function updateProgress(uploadId: string, progress: number, status: string): void {
  const upload = uploads.get(uploadId);
  if (!upload) return;
  
  upload.progress = progress;
  upload.status = status;
  
  wss.clients.forEach((client) => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(JSON.stringify({
        type: 'progress',
        uploadId,
        progress,
        status,
      }));
    }
  });
}

// Usage in upload handler
app.post('/upload', upload.single('file'), async (req, res) => {
  const uploadId = req.headers['x-upload-id'] as string;
  
  updateProgress(uploadId, 0, 'uploading');
  
  // Simulate upload progress
  for (let i = 0; i <= 100; i += 10) {
    await new Promise(resolve => setTimeout(resolve, 100));
    updateProgress(uploadId, i, 'uploading');
  }
  
  updateProgress(uploadId, 100, 'complete');
  
  res.json({ success: true, uploadId });
});
```

### Client-Side Progress

```typescript
// progress-client.ts
function uploadWithProgress(
  file: File,
  url: string,
  onProgress: (progress: number) => void
): Promise<void> {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();

    xhr.upload.addEventListener('progress', (e) => {
      if (e.lengthComputable) {
        const progress = (e.loaded / e.total) * 100;
        onProgress(progress);
      }
    });

    xhr.addEventListener('load', () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        resolve();
      } else {
        reject(new Error('Upload failed'));
      }
    });

    xhr.addEventListener('error', () => {
      reject(new Error('Upload failed'));
    });

    xhr.open('POST', url);
    xhr.send(file);
  });
}
```

---

## Error Handling

### Comprehensive Error Handling

```typescript
// error-handling.ts
import { MulterError } from 'multer';

class UploadError extends Error {
  constructor(
    public code: string,
    message: string,
    public details?: any
  ) {
    super(message);
    this.name = 'UploadError';
  }
}

function handleUploadError(error: unknown): UploadError {
  if (error instanceof MulterError) {
    switch (error.code) {
      case 'LIMIT_FILE_SIZE':
        return new UploadError('FILE_TOO_LARGE', 'File size exceeds limit');
      case 'LIMIT_UNEXPECTED_FILE':
        return new UploadError('UNEXPECTED_FILE', 'Unexpected file field');
      case 'LIMIT_FILE_COUNT':
        return new UploadError('TOO_MANY_FILES', 'Too many files uploaded');
      default:
        return new UploadError('UPLOAD_ERROR', error.message);
    }
  }

  if (error instanceof UploadError) {
    return error;
  }

  if (error instanceof Error) {
    return new UploadError('UNKNOWN_ERROR', error.message);
  }

  return new UploadError('UNKNOWN_ERROR', 'An unknown error occurred');
}

app.post('/upload', upload.single('file'), (req, res) => {
  try {
    if (!req.file) {
      throw new UploadError('NO_FILE', 'No file uploaded');
    }

    res.json({ success: true, file: req.file });
  } catch (error) {
    const uploadError = handleUploadError(error);
    
    res.status(400).json({
      error: uploadError.message,
      code: uploadError.code,
      details: uploadError.details,
    });
  }
});
```

```python
# error_handling.py
from fastapi import HTTPException, UploadFile
from fastapi.responses import JSONResponse
from typing import Optional

class UploadError(Exception):
    def __init__(self, code: str, message: str, details: Optional[dict] = None):
        self.code = code
        self.message = message
        self.details = details
        super().__init__(message)

def handle_upload_error(error: Exception) -> UploadError:
    """Handle upload errors and return standardized error."""
    if isinstance(error, UploadError):
        return error
    
    if isinstance(error, HTTPException):
        return UploadError('HTTP_ERROR', error.detail)
    
    return UploadError('UNKNOWN_ERROR', str(error))

@app.exception_handler(UploadError)
async def upload_error_handler(request, exc: UploadError):
    return JSONResponse(
        status_code=400,
        content={
            'error': exc.message,
            'code': exc.code,
            'details': exc.details
        }
    )
```

---

## Security Considerations

### 1. File Name Sanitization

```typescript
// sanitization.ts
import path from 'path';

function sanitizeFileName(fileName: string): string {
  // Remove path traversal attempts
  const sanitized = path.basename(fileName);
  
  // Remove special characters
  return sanitized
    .replace(/[^a-zA-Z0-9._-]/g, '_')
    .replace(/_{2,}/g, '_')
    .substring(0, 255);
}

// Usage
const safeName = sanitizeFileName('../../../etc/passwd'); // 'etc_passwd'
```

```python
# sanitization.py
import re
from pathlib import Path

def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent security issues."""
    # Remove path traversal attempts
    sanitized = Path(filename).name
    
    # Remove special characters
    sanitized = re.sub(r'[^a-zA-Z0-9._-]', '_', sanitized)
    sanitized = re.sub(r'_{2,}', '_', sanitized)
    
    return sanitized[:255]
```

### 2. Content-Type Validation

```typescript
// content-type-validation.ts
function validateContentType(file: Express.Multer.File, expectedType: string): boolean {
  return file.mimetype === expectedType;
}

// Strict content-type check
function strictContentTypeCheck(file: Express.Multer.File): boolean {
  const allowedTypes = {
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.png': 'image/png',
    '.gif': 'image/gif',
    '.pdf': 'application/pdf',
  };

  const ext = path.extname(file.originalname).toLowerCase();
  const expectedType = allowedTypes[ext as keyof typeof allowedTypes];

  if (!expectedType) return false;

  return file.mimetype === expectedType;
}
```

### 3. Rate Limiting

```typescript
// rate-limiting.ts
import rateLimit from 'express-rate-limit';

const uploadRateLimit = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 10, // 10 uploads per window
  message: 'Too many upload requests, please try again later',
  standardHeaders: true,
  legacyHeaders: false,
});

app.use('/upload', uploadRateLimit);
```

```python
# rate_limiting.py
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request

limiter = Limiter(key_func=get_remote_address)

@app.post("/upload")
@limiter.limit("10/15minutes")
async def upload_file(request: Request, file: UploadFile = File(...)):
    """Upload with rate limiting."""
    # Upload logic
    pass
```

---

## Image Processing

### Resize and Optimize

```typescript
// image-processing.ts
import sharp from 'sharp';

interface ImageProcessingOptions {
  width?: number;
  height?: number;
  quality?: number;
  format?: 'jpeg' | 'png' | 'webp';
}

async function processImage(
  inputBuffer: Buffer,
  options: ImageProcessingOptions
): Promise<Buffer> {
  let pipeline = sharp(inputBuffer);

  if (options.width || options.height) {
    pipeline = pipeline.resize(options.width, options.height, {
      fit: 'inside',
      withoutEnlargement: true,
    });
  }

  const format = options.format || 'jpeg';
  const quality = options.quality || 80;

  switch (format) {
    case 'jpeg':
      pipeline = pipeline.jpeg({ quality });
      break;
    case 'png':
      pipeline = pipeline.png({ quality });
      break;
    case 'webp':
      pipeline = pipeline.webp({ quality });
      break;
  }

  return pipeline.toBuffer();
}

// Usage
app.post('/upload/image', upload.single('file'), async (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: 'No file uploaded' });
  }

  // Process image
  const processed = await processImage(req.file.buffer, {
    width: 800,
    height: 600,
    quality: 85,
    format: 'webp',
  });

  // Save or upload processed image
  // ...

  res.json({ success: true });
});
```

```python
# image_processing.py
from PIL import Image, ImageOps
import io
from typing import Optional

class ImageProcessingOptions:
    width: Optional[int] = None
    height: Optional[int] = None
    quality: int = 80
    format: str = 'JPEG'

def process_image(
    input_buffer: bytes,
    options: ImageProcessingOptions
) -> bytes:
    """Process image with resize and optimization."""
    img = Image.open(io.BytesIO(input_buffer))
    
    # Resize if dimensions specified
    if options.width or options.height:
        img = ImageOps.fit(
            img,
            (options.width or img.width, options.height or img.height),
            method=Image.Resampling.LANCZOS
        )
    
    # Convert to RGB if saving as JPEG
    if options.format.upper() == 'JPEG' and img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Save to buffer
    output_buffer = io.BytesIO()
    img.save(
        output_buffer,
        format=options.format,
        quality=options.quality,
        optimize=True
    )
    
    return output_buffer.getvalue()
```

### Generate Thumbnails

```typescript
// thumbnail.ts
async function generateThumbnail(
  inputBuffer: Buffer,
  size: number = 150
): Promise<Buffer> {
  return sharp(inputBuffer)
    .resize(size, size, {
      fit: 'cover',
      position: 'center',
    })
    .jpeg({ quality: 70 })
    .toBuffer();
}

// Generate multiple sizes
async function generateImageVariants(
  inputBuffer: Buffer
): Promise<Record<string, Buffer>> {
  const sizes = {
    thumbnail: 150,
    small: 300,
    medium: 600,
    large: 1200,
  };

  const variants: Record<string, Buffer> = {};

  for (const [name, size] of Object.entries(sizes)) {
    variants[name] = await sharp(inputBuffer)
      .resize(size, size, { fit: 'inside' })
      .webp({ quality: 80 })
      .toBuffer();
  }

  return variants;
}
```

---

## Metadata Extraction

### Extract Image Metadata

```typescript
// metadata.ts
import sharp from 'sharp';

interface ImageMetadata {
  width: number;
  height: number;
  format: string;
  size: number;
  dpi?: number;
  hasAlpha?: boolean;
}

async function extractImageMetadata(buffer: Buffer): Promise<ImageMetadata> {
  const metadata = await sharp(buffer).metadata();

  return {
    width: metadata.width || 0,
    height: metadata.height || 0,
    format: metadata.format || 'unknown',
    size: buffer.length,
    dpi: metadata.density,
    hasAlpha: metadata.hasAlpha,
  };
}

// Usage
app.post('/upload', upload.single('file'), async (req, res) => {
  if (!req.file) return res.status(400).json({ error: 'No file' });

  const metadata = await extractImageMetadata(req.file.buffer);

  res.json({
    file: req.file.filename,
    metadata,
  });
});
```

```python
# metadata.py
from PIL import Image
import io
from typing import Dict, Any

def extract_image_metadata(buffer: bytes) -> Dict[str, Any]:
    """Extract metadata from image buffer."""
    img = Image.open(io.BytesIO(buffer))
    
    return {
        'width': img.width,
        'height': img.height,
        'format': img.format,
        'mode': img.mode,
        'size': len(buffer),
        'has_transparency': img.mode in ('RGBA', 'LA', 'P'),
    }
```

### Extract EXIF Data

```typescript
// exif.ts
import exifReader from 'exifreader';

function extractExif(buffer: Buffer): Record<string, any> {
  try {
    const tags = exifReader.load(buffer);
    
    return {
      make: tags['Make']?.description,
      model: tags['Model']?.description,
      dateTime: tags['DateTime']?.description,
      orientation: tags['Orientation']?.value,
      gpsLatitude: tags['GPSLatitude']?.description,
      gpsLongitude: tags['GPSLongitude']?.description,
    };
  } catch (error) {
    return {};
  }
}
```

---

## Database Records

### Store File Information

```typescript
// file-record.ts
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

interface FileRecord {
  id: string;
  originalName: string;
  fileName: string;
  mimeType: string;
  size: number;
  path: string;
  bucket?: string;
  uploadedBy: string;
  metadata?: any;
}

async function saveFileRecord(record: Omit<FileRecord, 'id'>): Promise<FileRecord> {
  return prisma.file.create({
    data: record,
  });
}

// Usage in upload handler
app.post('/upload', upload.single('file'), async (req, res) => {
  if (!req.file) return res.status(400).json({ error: 'No file' });

  const fileRecord = await saveFileRecord({
    originalName: req.file.originalname,
    fileName: req.file.filename,
    mimeType: req.file.mimetype,
    size: req.file.size,
    path: req.file.path,
    uploadedBy: req.user?.id || 'anonymous',
  });

  res.json({ success: true, file: fileRecord });
});
```

```python
# file_record.py
from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()

class FileRecord(Base):
    __tablename__ = 'files'
    
    id = Column(String, primary_key=True)
    original_name = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    mime_type = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    path = Column(String, nullable=False)
    bucket = Column(String)
    uploaded_by = Column(String)
    metadata = Column(Text)

def save_file_record(db: Session, record: dict) -> FileRecord:
    """Save file record to database."""
    db_file = FileRecord(**record)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file
```

---

## Production Patterns

### 1. Upload Queue

```typescript
// upload-queue.ts
import { Queue, Worker, Job } from 'bullmq';
import { uploadToS3 } from './s3';

const uploadQueue = new Queue('uploads', {
  connection: { host: 'localhost', port: 6379 },
});

const uploadWorker = new Worker(
  'uploads',
  async (job: Job) => {
    const { filePath, key, bucket } = job.data;
    await uploadToS3(filePath, key, bucket);
  },
  { connection: { host: 'localhost', port: 6379 } }
);

// Queue upload
app.post('/upload', upload.single('file'), async (req, res) => {
  if (!req.file) return res.status(400).json({ error: 'No file' });

  await uploadQueue.add('upload', {
    filePath: req.file.path,
    key: `uploads/${req.file.filename}`,
    bucket: 'my-bucket',
  });

  res.json({ success: true, message: 'Upload queued' });
});
```

### 2. CDN Integration

```typescript
// cdn.ts
async function uploadToCDN(
  file: Express.Multer.File,
  cdnPath: string
): Promise<string> {
  // Upload to Cloudflare Images, Cloudinary, or similar
  const response = await fetch('https://api.cloudflare.com/client/v4/accounts/:account_id/images/v1', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.CLOUDFLARE_API_TOKEN}`,
    },
    body: file.buffer,
  });

  const data = await response.json();
  return data.result.variants[0]; // CDN URL
}
```

### 3. Multi-Region Upload

```typescript
// multi-region.ts
async function uploadToMultipleRegions(
  file: Buffer,
  key: string
): Promise<string[]> {
  const regions = ['us-east-1', 'eu-west-1', 'ap-southeast-1'];
  const uploadPromises = regions.map(region =>
    uploadToS3InRegion(file, key, region)
  );

  return Promise.all(uploadPromises);
}
```

---

## Summary

This skill covers comprehensive file upload handling including:

- **Upload Methods**: Form upload, direct S3 upload, chunked upload
- **Validation**: File type, size, virus scanning
- **Temporary Storage**: Managing temporary files with auto-cleanup
- **Progress Tracking**: WebSocket and client-side progress
- **Error Handling**: Comprehensive error handling patterns
- **Security Considerations**: Sanitization, content-type validation, rate limiting
- **Image Processing**: Resize, optimize, generate thumbnails
- **Metadata Extraction**: Image metadata and EXIF data
- **Database Records**: Storing file information
- **Production Patterns**: Upload queues, CDN integration, multi-region uploads
