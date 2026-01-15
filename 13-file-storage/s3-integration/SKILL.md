# AWS S3 / MinIO Integration

## Overview

Amazon S3 (Simple Storage Service) is an object storage service that offers industry-leading scalability, data availability, security, and performance. MinIO is an S3-compatible object storage server that can be self-hosted.

## Table of Contents

1. [S3 Concepts](#s3-concepts)
2. [AWS SDK Setup](#aws-sdk-setup)
3. [MinIO Setup](#minio-setup)
4. [File Upload](#file-upload)
5. [File Download](#file-download)
6. [Presigned URLs](#presigned-urls)
7. [Access Control](#access-control)
8. [CORS Configuration](#cors-configuration)
9. [Lifecycle Policies](#lifecycle-policies)
10. [Versioning](#versioning)
11. [Server-Side Encryption](#server-side-encryption)
12. [Cost Optimization](#cost-optimization)
13. [Best Practices](#best-practices)

---

## S3 Concepts

### Buckets

A bucket is a container for objects stored in Amazon S3. Every object is contained in a bucket.

```typescript
// Bucket naming rules
// - 3-63 characters long
// - Only lowercase letters, numbers, dots, and hyphens
// - Must start with a letter or number
// - Must not end with a hyphen
// - Must not have consecutive periods
```

### Objects

Objects are the fundamental entities stored in S3. Objects consist of:
- **Key**: The unique identifier for an object within a bucket
- **Data**: The actual content
- **Metadata**: Information about the object (content-type, last-modified, etc.)

### Keys

The key is the unique identifier for an object in a bucket. Keys can include prefixes that create a hierarchical structure.

```
bucket/
├── images/
│   ├── profile/user123.jpg
│   └── products/item456.png
└── documents/
    └── contracts/contract.pdf
```

---

## AWS SDK Setup

### Node.js Setup

```bash
npm install @aws-sdk/client-s3 @aws-sdk/s3-request-presigner
```

```typescript
// s3-client.ts
import { S3Client } from '@aws-sdk/client-s3';

// Initialize S3 client
const s3Client = new S3Client({
  region: process.env.AWS_REGION || 'us-east-1',
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID!,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY!,
  },
});

// For local development with MinIO
const minioClient = new S3Client({
  endpoint: 'http://localhost:9000',
  region: 'us-east-1',
  credentials: {
    accessKeyId: 'minioadmin',
    secretAccessKey: 'minioadmin',
  },
  forcePathStyle: true, // Required for MinIO
});

export { s3Client, minioClient };
```

### Python Setup

```bash
pip install boto3
```

```python
# s3_client.py
import os
import boto3

# Initialize S3 client
s3_client = boto3.client(
    's3',
    region_name=os.getenv('AWS_REGION', 'us-east-1'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

# For local development with MinIO
minio_client = boto3.client(
    's3',
    endpoint_url='http://localhost:9000',
    region_name='us-east-1',
    aws_access_key_id='minioadmin',
    aws_secret_access_key='minioadmin'
)
```

---

## MinIO Setup

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  minio:
    image: minio/minio:latest
    command: server /data --console-address ":9001"
    ports:
      - "9000:9000"  # API
      - "9001:9001"  # Console
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    volumes:
      - minio_data:/data

volumes:
  minio_data:
```

### Configuration

```typescript
// MinIO configuration with AWS SDK
import { S3Client } from '@aws-sdk/client-s3';

export const minioClient = new S3Client({
  endpoint: process.env.MINIO_ENDPOINT || 'http://localhost:9000',
  region: process.env.MINIO_REGION || 'us-east-1',
  credentials: {
    accessKeyId: process.env.MINIO_ACCESS_KEY || 'minioadmin',
    secretAccessKey: process.env.MINIO_SECRET_KEY || 'minioadmin',
  },
  forcePathStyle: true, // Required for MinIO
});
```

```python
# MinIO configuration with boto3
import os
import boto3

minio_client = boto3.client(
    's3',
    endpoint_url=os.getenv('MINIO_ENDPOINT', 'http://localhost:9000'),
    region_name=os.getenv('MINIO_REGION', 'us-east-1'),
    aws_access_key_id=os.getenv('MINIO_ACCESS_KEY', 'minioadmin'),
    aws_secret_access_key=os.getenv('MINIO_SECRET_KEY', 'minioadmin')
)
```

---

## File Upload

### Simple Upload

#### Node.js

```typescript
// upload.ts
import { PutObjectCommand } from '@aws-sdk/client-s3';
import { s3Client } from './s3-client';

interface UploadParams {
  bucket: string;
  key: string;
  body: Buffer | string | ReadableStream;
  contentType?: string;
  metadata?: Record<string, string>;
}

async function uploadFile(params: UploadParams): Promise<string> {
  const command = new PutObjectCommand({
    Bucket: params.bucket,
    Key: params.key,
    Body: params.body,
    ContentType: params.contentType,
    Metadata: params.metadata,
  });

  const response = await s3Client.send(command);
  return response.ETag || '';
}

// Usage
const fileUrl = await uploadFile({
  bucket: 'my-bucket',
  key: 'uploads/images/profile.jpg',
  body: fileBuffer,
  contentType: 'image/jpeg',
  metadata: {
    originalName: 'profile.jpg',
    uploadedBy: 'user123',
  },
});
```

#### Python

```python
# upload.py
import os
from typing import Dict, Optional
from s3_client import s3_client

def upload_file(
    bucket: str,
    key: str,
    body: bytes,
    content_type: Optional[str] = None,
    metadata: Optional[Dict[str, str]] = None
) -> str:
    """Upload a file to S3."""
    params = {
        'Bucket': bucket,
        'Key': key,
        'Body': body,
    }
    
    if content_type:
        params['ContentType'] = content_type
    if metadata:
        params['Metadata'] = metadata
    
    response = s3_client.put_object(**params)
    return response['ETag']

# Usage
file_etag = upload_file(
    bucket='my-bucket',
    key='uploads/images/profile.jpg',
    body=file_data,
    content_type='image/jpeg',
    metadata={
        'originalName': 'profile.jpg',
        'uploadedBy': 'user123'
    }
)
```

### Multipart Upload

#### Node.js

```typescript
// multipart-upload.ts
import {
  CreateMultipartUploadCommand,
  UploadPartCommand,
  CompleteMultipartUploadCommand,
  AbortMultipartUploadCommand,
} from '@aws-sdk/client-s3';
import { s3Client } from './s3-client';

interface MultipartUploadParams {
  bucket: string;
  key: string;
  body: Buffer;
  partSize: number; // in bytes (e.g., 5 * 1024 * 1024 for 5MB)
  contentType?: string;
}

async function multipartUpload(params: MultipartUploadParams): Promise<string> {
  const { bucket, key, body, partSize, contentType } = params;
  
  // Step 1: Initiate multipart upload
  const createCommand = new CreateMultipartUploadCommand({
    Bucket: bucket,
    Key: key,
    ContentType: contentType,
  });
  
  const { UploadId } = await s3Client.send(createCommand);
  if (!UploadId) throw new Error('Failed to create multipart upload');
  
  const parts = [];
  
  try {
    // Step 2: Upload parts
    for (let partNumber = 1; partNumber * partSize <= body.length; partNumber++) {
      const start = (partNumber - 1) * partSize;
      const end = Math.min(partNumber * partSize, body.length);
      const partBuffer = body.subarray(start, end);
      
      const uploadCommand = new UploadPartCommand({
        Bucket: bucket,
        Key: key,
        PartNumber: partNumber,
        UploadId,
        Body: partBuffer,
      });
      
      const { ETag } = await s3Client.send(uploadCommand);
      parts.push({ PartNumber: partNumber, ETag: ETag! });
    }
    
    // Step 3: Complete multipart upload
    const completeCommand = new CompleteMultipartUploadCommand({
      Bucket: bucket,
      Key: key,
      UploadId,
      MultipartUpload: { Parts: parts },
    });
    
    const response = await s3Client.send(completeCommand);
    return response.Location || '';
    
  } catch (error) {
    // Abort on error
    await s3Client.send(new AbortMultipartUploadCommand({
      Bucket: bucket,
      Key: key,
      UploadId,
    }));
    throw error;
  }
}

// Usage
const location = await multipartUpload({
  bucket: 'my-bucket',
  key: 'large-files/video.mp4',
  body: largeFileBuffer,
  partSize: 5 * 1024 * 1024, // 5MB parts
  contentType: 'video/mp4',
});
```

#### Python

```python
# multipart_upload.py
import math
from typing import List
from botocore.exceptions import ClientError
from s3_client import s3_client

def multipart_upload(
    bucket: str,
    key: str,
    body: bytes,
    part_size: int = 5 * 1024 * 1024,  # 5MB
    content_type: str = None
) -> str:
    """Upload a large file using multipart upload."""
    
    # Step 1: Initiate multipart upload
    response = s3_client.create_multipart_upload(
        Bucket=bucket,
        Key=key,
        ContentType=content_type
    )
    upload_id = response['UploadId']
    
    parts = []
    
    try:
        # Step 2: Upload parts
        total_parts = math.ceil(len(body) / part_size)
        
        for part_number in range(1, total_parts + 1):
            start = (part_number - 1) * part_size
            end = min(part_number * part_size, len(body))
            part_data = body[start:end]
            
            response = s3_client.upload_part(
                Bucket=bucket,
                Key=key,
                PartNumber=part_number,
                UploadId=upload_id,
                Body=part_data
            )
            
            parts.append({
                'PartNumber': part_number,
                'ETag': response['ETag']
            })
        
        # Step 3: Complete multipart upload
        response = s3_client.complete_multipart_upload(
            Bucket=bucket,
            Key=key,
            UploadId=upload_id,
            MultipartUpload={'Parts': parts}
        )
        
        return response['Location']
        
    except ClientError as e:
        # Abort on error
        s3_client.abort_multipart_upload(
            Bucket=bucket,
            Key=key,
            UploadId=upload_id
        )
        raise e

# Usage
location = multipart_upload(
    bucket='my-bucket',
    key='large-files/video.mp4',
    body=large_file_data,
    part_size=5 * 1024 * 1024,  # 5MB
    content_type='video/mp4'
)
```

---

## File Download

### Simple Download

#### Node.js

```typescript
// download.ts
import { GetObjectCommand } from '@aws-sdk/client-s3';
import { s3Client } from './s3-client';

interface DownloadParams {
  bucket: string;
  key: string;
}

async function downloadFile(params: DownloadParams): Promise<Buffer> {
  const command = new GetObjectCommand({
    Bucket: params.bucket,
    Key: params.key,
  });

  const response = await s3Client.send(command);
  const chunks: Uint8Array[] = [];

  // @ts-ignore - Body is a ReadableStream
  for await (const chunk of response.Body) {
    chunks.push(chunk);
  }

  return Buffer.concat(chunks);
}

// Usage
const fileBuffer = await downloadFile({
  bucket: 'my-bucket',
  key: 'uploads/images/profile.jpg',
});
```

#### Python

```python
# download.py
from s3_client import s3_client

def download_file(bucket: str, key: str) -> bytes:
    """Download a file from S3."""
    response = s3_client.get_object(Bucket=bucket, Key=key)
    return response['Body'].read()

# Usage
file_data = download_file(
    bucket='my-bucket',
    key='uploads/images/profile.jpg'
)
```

### Streaming Download

#### Node.js

```typescript
// streaming-download.ts
import { GetObjectCommand } from '@aws-sdk/client-s3';
import { s3Client } from './s3-client';
import { Readable } from 'stream';

async function downloadStream(params: { bucket: string; key: string }): Promise<Readable> {
  const command = new GetObjectCommand({
    Bucket: params.bucket,
    Key: params.key,
  });

  const response = await s3Client.send(command);
  return response.Body as Readable;
}

// Usage with Express
import express from 'express';

const app = express();

app.get('/download/:key', async (req, res) => {
  try {
    const stream = await downloadStream({
      bucket: 'my-bucket',
      key: req.params.key,
    });
    
    stream.pipe(res);
  } catch (error) {
    res.status(500).json({ error: 'Download failed' });
  }
});
```

#### Python

```python
# streaming_download.py
from flask import Flask, Response
from s3_client import s3_client

app = Flask(__name__)

@app.route('/download/<path:key>')
def download_file(key: str):
    """Stream a file from S3."""
    response = s3_client.get_object(Bucket='my-bucket', Key=key)
    
    return Response(
        response['Body'].read(),
        mimetype=response['ContentType'],
        headers={
            'Content-Disposition': f'attachment; filename={key}'
        }
    )
```

---

## Presigned URLs

Presigned URLs allow temporary access to private S3 objects without requiring AWS credentials.

### Generate Presigned URL

#### Node.js

```typescript
// presigned-url.ts
import { GetObjectCommand, PutObjectCommand } from '@aws-sdk/client-s3';
import { getSignedUrl } from '@aws-sdk/s3-request-presigner';
import { s3Client } from './s3-client';

// Download presigned URL
async function getDownloadUrl(
  bucket: string,
  key: string,
  expiresIn: number = 3600
): Promise<string> {
  const command = new GetObjectCommand({
    Bucket: bucket,
    Key: key,
  });

  return await getSignedUrl(s3Client, command, { expiresIn });
}

// Upload presigned URL
async function getUploadUrl(
  bucket: string,
  key: string,
  contentType: string,
  expiresIn: number = 3600
): Promise<string> {
  const command = new PutObjectCommand({
    Bucket: bucket,
    Key: key,
    ContentType: contentType,
  });

  return await getSignedUrl(s3Client, command, { expiresIn });
}

// Usage
const downloadUrl = await getDownloadUrl('my-bucket', 'files/document.pdf', 3600);
const uploadUrl = await getUploadUrl('my-bucket', 'uploads/image.jpg', 'image/jpeg', 3600);
```

#### Python

```python
# presigned_url.py
from datetime import datetime, timedelta
from s3_client import s3_client

def get_download_url(bucket: str, key: str, expires_in: int = 3600) -> str:
    """Generate a presigned URL for downloading."""
    return s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket, 'Key': key},
        ExpiresIn=expires_in
    )

def get_upload_url(bucket: str, key: str, content_type: str, expires_in: int = 3600) -> str:
    """Generate a presigned URL for uploading."""
    return s3_client.generate_presigned_url(
        'put_object',
        Params={
            'Bucket': bucket,
            'Key': key,
            'ContentType': content_type
        },
        ExpiresIn=expires_in
    )

# Usage
download_url = get_download_url('my-bucket', 'files/document.pdf', 3600)
upload_url = get_upload_url('my-bucket', 'uploads/image.jpg', 'image/jpeg', 3600)
```

### Client-Side Upload with Presigned URL

```typescript
// client-upload.ts
async function uploadWithPresignedUrl(
  file: File,
  presignedUrl: string,
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

    xhr.open('PUT', presignedUrl);
    xhr.setRequestHeader('Content-Type', file.type);
    xhr.send(file);
  });
}

// Usage
const file = document.querySelector('input[type="file"]').files[0];
await uploadWithPresignedUrl(file, uploadUrl, (progress) => {
  console.log(`Upload progress: ${progress}%`);
});
```

---

## Access Control

### IAM Policies

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::my-bucket/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket"
      ],
      "Resource": "arn:aws:s3:::my-bucket"
    }
  ]
}
```

### Bucket Policies

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-public-bucket/*"
    },
    {
      "Sid": "AllowSpecificIP",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-bucket/*",
      "Condition": {
        "IpAddress": {
          "aws:SourceIp": ["192.0.2.0/24"]
        }
      }
    }
  ]
}
```

### Bucket ACLs (Deprecated)

```typescript
// Set bucket ACL (not recommended, use bucket policies instead)
import { PutBucketAclCommand } from '@aws-sdk/client-s3';

await s3Client.send(new PutBucketAclCommand({
  Bucket: 'my-bucket',
  ACL: 'private', // private | public-read | public-read-write | authenticated-read
}));
```

---

## CORS Configuration

### CORS Configuration

```json
{
  "CORSRules": [
    {
      "AllowedHeaders": ["*"],
      "AllowedMethods": ["GET", "PUT", "POST", "DELETE", "HEAD"],
      "AllowedOrigins": ["https://example.com", "https://www.example.com"],
      "ExposeHeaders": ["ETag", "Content-Length"],
      "MaxAgeSeconds": 3600
    },
    {
      "AllowedHeaders": ["*"],
      "AllowedMethods": ["GET"],
      "AllowedOrigins": ["*"],
      "MaxAgeSeconds": 3000
    }
  ]
}
```

### Setting CORS via CLI

```bash
aws s3api put-bucket-cors \
  --bucket my-bucket \
  --cors-configuration file://cors-config.json
```

### Setting CORS via SDK

#### Node.js

```typescript
import { PutBucketCorsCommand } from '@aws-sdk/client-s3';
import { s3Client } from './s3-client';

await s3Client.send(new PutBucketCorsCommand({
  Bucket: 'my-bucket',
  CORSConfiguration: {
    CORSRules: [
      {
        AllowedHeaders: ['*'],
        AllowedMethods: ['GET', 'PUT', 'POST', 'DELETE'],
        AllowedOrigins: ['https://example.com'],
        ExposeHeaders: ['ETag'],
        MaxAgeSeconds: 3600,
      },
    ],
  },
}));
```

#### Python

```python
cors_configuration = {
    'CORSRules': [
        {
            'AllowedHeaders': ['*'],
            'AllowedMethods': ['GET', 'PUT', 'POST', 'DELETE'],
            'AllowedOrigins': ['https://example.com'],
            'ExposeHeaders': ['ETag'],
            'MaxAgeSeconds': 3600
        }
    ]
}

s3_client.put_bucket_cors(
    Bucket='my-bucket',
    CORSConfiguration=cors_configuration
)
```

---

## Lifecycle Policies

Lifecycle policies automatically manage objects throughout their lifecycle.

### Lifecycle Configuration

```json
{
  "Rules": [
    {
      "ID": "DeleteOldVersions",
      "Status": "Enabled",
      "Prefix": "logs/",
      "NoncurrentVersionExpiration": {
        "NoncurrentDays": 30
      }
    },
    {
      "ID": "ArchiveOldFiles",
      "Status": "Enabled",
      "Prefix": "archive/",
      "Transitions": [
        {
          "Days": 30,
          "StorageClass": "STANDARD_IA"
        },
        {
          "Days": 90,
          "StorageClass": "GLACIER"
        },
        {
          "Days": 180,
          "StorageClass": "DEEP_ARCHIVE"
        }
      ]
    },
    {
      "ID": "DeleteTempFiles",
      "Status": "Enabled",
      "Prefix": "temp/",
      "Expiration": {
        "Days": 7
      }
    }
  ]
}
```

### Setting Lifecycle Policy

#### Node.js

```typescript
import { PutBucketLifecycleConfigurationCommand } from '@aws-sdk/client-s3';
import { s3Client } from './s3-client';

await s3Client.send(new PutBucketLifecycleConfigurationCommand({
  Bucket: 'my-bucket',
  LifecycleConfiguration: {
    Rules: [
      {
        Id: 'DeleteTempFiles',
        Status: 'Enabled',
        Prefix: 'temp/',
        Expiration: { Days: 7 },
      },
    ],
  },
}));
```

#### Python

```python
lifecycle_configuration = {
    'Rules': [
        {
            'ID': 'DeleteTempFiles',
            'Status': 'Enabled',
            'Prefix': 'temp/',
            'Expiration': {'Days': 7}
        }
    ]
}

s3_client.put_bucket_lifecycle_configuration(
    Bucket='my-bucket',
    LifecycleConfiguration=lifecycle_configuration
)
```

---

## Versioning

Versioning keeps multiple variants of an object in the same bucket.

### Enable Versioning

#### Node.js

```typescript
import { PutBucketVersioningCommand } from '@aws-sdk/client-s3';
import { s3Client } from './s3-client';

await s3Client.send(new PutBucketVersioningCommand({
  Bucket: 'my-bucket',
  VersioningConfiguration: {
    Status: 'Enabled', // Enabled | Suspended
    MFADelete: 'Disabled', // Disabled | Enabled
  },
}));
```

#### Python

```python
s3_client.put_bucket_versioning(
    Bucket='my-bucket',
    VersioningConfiguration={
        'Status': 'Enabled',
        'MFADelete': 'Disabled'
    }
)
```

### List Object Versions

#### Node.js

```typescript
import { ListObjectVersionsCommand } from '@aws-sdk/client-s3';

const response = await s3Client.send(new ListObjectVersionsCommand({
  Bucket: 'my-bucket',
  Prefix: 'files/',
}));

console.log('Versions:', response.Versions);
console.log('DeleteMarkers:', response.DeleteMarkers);
```

#### Python

```python
response = s3_client.list_object_versions(
    Bucket='my-bucket',
    Prefix='files/'
)

print('Versions:', response.get('Versions', []))
print('DeleteMarkers:', response.get('DeleteMarkers', []))
```

---

## Server-Side Encryption

### SSE-S3 (Amazon S3-Managed Keys)

#### Node.js

```typescript
import { PutObjectCommand } from '@aws-sdk/client-s3';

await s3Client.send(new PutObjectCommand({
  Bucket: 'my-bucket',
  Key: 'sensitive-file.txt',
  Body: 'Secret content',
  ServerSideEncryption: 'AES256', // SSE-S3
}));
```

#### Python

```python
s3_client.put_object(
    Bucket='my-bucket',
    Key='sensitive-file.txt',
    Body='Secret content',
    ServerSideEncryption='AES256'  # SSE-S3
)
```

### SSE-KMS (AWS KMS-Managed Keys)

#### Node.js

```typescript
await s3Client.send(new PutObjectCommand({
  Bucket: 'my-bucket',
  Key: 'sensitive-file.txt',
  Body: 'Secret content',
  ServerSideEncryption: 'aws:kms',
  SSEKMSKeyId: 'arn:aws:kms:us-east-1:123456789012:key/abcd1234',
}));
```

#### Python

```python
s3_client.put_object(
    Bucket='my-bucket',
    Key='sensitive-file.txt',
    Body='Secret content',
    ServerSideEncryption='aws:kms',
    SSEKMSKeyId='arn:aws:kms:us-east-1:123456789012:key/abcd1234'
)
```

### SSE-C (Customer-Provided Keys)

#### Node.js

```typescript
import crypto from 'crypto';

const encryptionKey = crypto.randomBytes(32);

await s3Client.send(new PutObjectCommand({
  Bucket: 'my-bucket',
  Key: 'sensitive-file.txt',
  Body: 'Secret content',
  SSECustomerAlgorithm: 'AES256',
  SSECustomerKey: encryptionKey,
  SSECustomerKeyMD5: crypto.createHash('md5').update(encryptionKey).digest('base64'),
}));
```

#### Python

```python
import hashlib
import os

encryption_key = os.urandom(32)
encryption_key_md5 = hashlib.md5(encryption_key).hexdigest()

s3_client.put_object(
    Bucket='my-bucket',
    Key='sensitive-file.txt',
    Body='Secret content',
    SSECustomerAlgorithm='AES256',
    SSECustomerKey=encryption_key,
    SSECustomerKeyMD5=encryption_key_md5
)
```

---

## Cost Optimization

### Storage Classes

| Storage Class | Use Case | Cost |
|---------------|----------|------|
| STANDARD | Frequently accessed data | Higher |
| STANDARD_IA | Infrequently accessed data | Lower |
| ONEZONE_IA | Same as STANDARD_IA, single AZ | Lowest |
| GLACIER | Long-term archival | Very Low |
| DEEP_ARCHIVE | Rarely accessed archival | Lowest |
| INTELLIGENT_TIERING | Unknown access patterns | Variable |

### Cost Optimization Strategies

#### 1. Use Appropriate Storage Classes

```typescript
// Move old files to cheaper storage
import { CopyObjectCommand, DeleteObjectCommand } from '@aws-sdk/client-s3';

async function moveToGlacier(bucket: string, key: string): Promise<void> {
  await s3Client.send(new CopyObjectCommand({
    Bucket: bucket,
    Key: key,
    CopySource: `${bucket}/${key}`,
    StorageClass: 'GLACIER',
  }));
}
```

#### 2. Use Lifecycle Policies

```json
{
  "Rules": [
    {
      "ID": "TransitionToIA",
      "Status": "Enabled",
      "Transitions": [
        {
          "Days": 30,
          "StorageClass": "STANDARD_IA"
        },
        {
          "Days": 90,
          "StorageClass": "GLACIER"
        }
      ]
    }
  ]
}
```

#### 3. Use S3 Transfer Acceleration

```typescript
import { PutObjectCommand } from '@aws-sdk/client-s3';

await s3Client.send(new PutObjectCommand({
  Bucket: 'my-bucket',
  Key: 'large-file.zip',
  Body: fileBuffer,
  // Transfer acceleration is enabled at bucket level
}));
```

#### 4. Use Multipart Upload for Large Files

```typescript
// Already covered in Multipart Upload section
```

---

## Best Practices

### 1. Security

- **Use IAM policies** instead of bucket ACLs
- **Enable bucket policies** for fine-grained access control
- **Enable server-side encryption** for sensitive data
- **Use presigned URLs** for temporary access
- **Enable MFA Delete** for critical buckets
- **Block public access** for sensitive buckets

```typescript
// Block public access
import { PutPublicAccessBlockCommand } from '@aws-sdk/client-s3';

await s3Client.send(new PutPublicAccessBlockCommand({
  Bucket: 'my-bucket',
  PublicAccessBlockConfiguration: {
    BlockPublicAcls: true,
    IgnorePublicAcls: true,
    BlockPublicPolicy: true,
    RestrictPublicBuckets: true,
  },
}));
```

### 2. Performance

- **Use multipart upload** for files larger than 100MB
- **Use appropriate storage classes** based on access patterns
- **Enable transfer acceleration** for long-distance transfers
- **Use CloudFront CDN** for frequently accessed content

### 3. Cost Optimization

- **Use lifecycle policies** to transition data to cheaper storage
- **Clean up incomplete multipart uploads**
- **Use S3 Analytics** to optimize storage classes
- **Monitor storage usage** with CloudWatch metrics

### 4. Reliability

- **Enable versioning** for important data
- **Use cross-region replication** for disaster recovery
- **Implement retry logic** with exponential backoff
- **Use S3 Event Notifications** for processing triggers

```typescript
// Retry with exponential backoff
async function uploadWithRetry(
  command: PutObjectCommand,
  maxRetries: number = 3
): Promise<any> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await s3Client.send(command);
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, Math.pow(2, i) * 1000));
    }
  }
}
```

### 5. Naming Conventions

```typescript
// Good naming conventions
const goodKeys = [
  'uploads/2024/01/15/user123/profile.jpg',
  'documents/contracts/contract-2024-001.pdf',
  'images/products/thumbnails/item456.png',
];

// Avoid
const badKeys = [
  'file.jpg', // No structure
  'My File.jpg', // Spaces
  'file.txt', // Wrong extension
];
```

### 6. Error Handling

```typescript
import { S3ServiceException } from '@aws-sdk/client-s3';

try {
  await s3Client.send(command);
} catch (error) {
  if (error instanceof S3ServiceException) {
    if (error.name === 'NoSuchBucket') {
      console.error('Bucket does not exist');
    } else if (error.name === 'NoSuchKey') {
      console.error('Object does not exist');
    } else if (error.name === 'AccessDenied') {
      console.error('Access denied');
    }
  }
}
```

---

## Summary

This skill covers comprehensive AWS S3 and MinIO integration including:

- **S3 Concepts**: Buckets, objects, and keys
- **AWS SDK Setup**: Node.js and Python client initialization
- **MinIO Setup**: S3-compatible self-hosted storage
- **File Upload**: Simple and multipart upload patterns
- **File Download**: Simple and streaming downloads
- **Presigned URLs**: Temporary access for uploads and downloads
- **Access Control**: IAM policies and bucket policies
- **CORS Configuration**: Cross-origin resource sharing setup
- **Lifecycle Policies**: Automatic object management
- **Versioning**: Keeping multiple object versions
- **Server-Side Encryption**: SSE-S3, SSE-KMS, and SSE-C
- **Cost Optimization**: Storage classes and strategies
- **Best Practices**: Security, performance, cost, reliability, and more
