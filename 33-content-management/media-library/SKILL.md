---
name: Media Library
description: Managing digital assets including images, videos, and documents with upload, processing, optimization, organization, metadata, and CDN integration for efficient media delivery.
---

# Media Library

> **Current Level:** Intermediate  
> **Domain:** Content Management / Media

---

## Overview

A media library manages digital assets including images, videos, and documents. This guide covers upload, processing, organization, and CDN integration for building scalable media management systems.

## Media Library Architecture

```
Upload → Processing → Storage → CDN → Delivery
   ↓         ↓          ↓
Validation  Optimization  Metadata
```

## Database Schema

```sql
-- media table
CREATE TABLE media (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  filename VARCHAR(255) NOT NULL,
  original_filename VARCHAR(255) NOT NULL,
  mime_type VARCHAR(100) NOT NULL,
  file_size BIGINT NOT NULL,
  
  storage_path VARCHAR(500) NOT NULL,
  cdn_url VARCHAR(500),
  
  type VARCHAR(50) NOT NULL,
  
  width INTEGER,
  height INTEGER,
  duration INTEGER,
  
  metadata JSONB,
  
  folder_id UUID REFERENCES media_folders(id),
  uploaded_by UUID REFERENCES users(id),
  
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  INDEX idx_type (type),
  INDEX idx_folder (folder_id),
  INDEX idx_uploaded_by (uploaded_by),
  FULLTEXT idx_search (filename, original_filename)
);

-- media_folders table
CREATE TABLE media_folders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  parent_id UUID REFERENCES media_folders(id),
  path VARCHAR(500) NOT NULL,
  
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW(),
  
  INDEX idx_parent (parent_id),
  INDEX idx_path (path)
);

-- media_tags table
CREATE TABLE media_tags (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(100) UNIQUE NOT NULL,
  
  created_at TIMESTAMP DEFAULT NOW()
);

-- media_tag_relations table
CREATE TABLE media_tag_relations (
  media_id UUID REFERENCES media(id) ON DELETE CASCADE,
  tag_id UUID REFERENCES media_tags(id) ON DELETE CASCADE,
  
  PRIMARY KEY (media_id, tag_id)
);

-- media_collections table
CREATE TABLE media_collections (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  description TEXT,
  
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- media_collection_items table
CREATE TABLE media_collection_items (
  collection_id UUID REFERENCES media_collections(id) ON DELETE CASCADE,
  media_id UUID REFERENCES media(id) ON DELETE CASCADE,
  sort_order INTEGER DEFAULT 0,
  
  added_at TIMESTAMP DEFAULT NOW(),
  
  PRIMARY KEY (collection_id, media_id)
);
```

## File Upload and Processing

```typescript
// services/media-upload.service.ts
import multer from 'multer';
import sharp from 'sharp';
import { S3 } from 'aws-sdk';
import { v4 as uuidv4 } from 'uuid';

export class MediaUploadService {
  private s3: S3;

  constructor() {
    this.s3 = new S3({
      accessKeyId: process.env.AWS_ACCESS_KEY_ID,
      secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
      region: process.env.AWS_REGION
    });
  }

  async uploadFile(file: Express.Multer.File, userId: string): Promise<Media> {
    // Validate file
    this.validateFile(file);

    // Generate unique filename
    const filename = `${uuidv4()}-${file.originalname}`;
    const storagePath = `uploads/${new Date().getFullYear()}/${filename}`;

    // Process based on type
    let processedBuffer = file.buffer;
    let metadata: any = {};

    if (file.mimetype.startsWith('image/')) {
      const result = await this.processImage(file.buffer);
      processedBuffer = result.buffer;
      metadata = result.metadata;
    } else if (file.mimetype.startsWith('video/')) {
      metadata = await this.extractVideoMetadata(file.buffer);
    }

    // Upload to S3
    await this.s3.upload({
      Bucket: process.env.AWS_S3_BUCKET!,
      Key: storagePath,
      Body: processedBuffer,
      ContentType: file.mimetype,
      ACL: 'public-read'
    }).promise();

    const cdnUrl = `${process.env.CDN_URL}/${storagePath}`;

    // Save to database
    const media = await db.media.create({
      data: {
        filename,
        originalFilename: file.originalname,
        mimeType: file.mimetype,
        fileSize: processedBuffer.length,
        storagePath,
        cdnUrl,
        type: this.getMediaType(file.mimetype),
        width: metadata.width,
        height: metadata.height,
        duration: metadata.duration,
        metadata,
        uploadedBy: userId
      }
    });

    return media;
  }

  private validateFile(file: Express.Multer.File): void {
    const maxSize = 50 * 1024 * 1024; // 50MB

    if (file.size > maxSize) {
      throw new Error('File too large');
    }

    const allowedTypes = [
      'image/jpeg',
      'image/png',
      'image/gif',
      'image/webp',
      'video/mp4',
      'video/quicktime',
      'application/pdf'
    ];

    if (!allowedTypes.includes(file.mimetype)) {
      throw new Error('File type not allowed');
    }
  }

  private async processImage(buffer: Buffer): Promise<ProcessedImage> {
    const image = sharp(buffer);
    const metadata = await image.metadata();

    // Optimize image
    const optimized = await image
      .resize(2000, 2000, {
        fit: 'inside',
        withoutEnlargement: true
      })
      .jpeg({ quality: 85, progressive: true })
      .toBuffer();

    return {
      buffer: optimized,
      metadata: {
        width: metadata.width,
        height: metadata.height,
        format: metadata.format
      }
    };
  }

  private async extractVideoMetadata(buffer: Buffer): Promise<VideoMetadata> {
    // Use ffprobe or similar
    return {
      duration: 0,
      width: 0,
      height: 0
    };
  }

  private getMediaType(mimeType: string): string {
    if (mimeType.startsWith('image/')) return 'image';
    if (mimeType.startsWith('video/')) return 'video';
    if (mimeType.startsWith('audio/')) return 'audio';
    return 'document';
  }
}

interface ProcessedImage {
  buffer: Buffer;
  metadata: {
    width?: number;
    height?: number;
    format?: string;
  };
}

interface VideoMetadata {
  duration: number;
  width: number;
  height: number;
}
```

## Image Optimization

```typescript
// services/image-optimization.service.ts
export class ImageOptimizationService {
  async generateThumbnails(mediaId: string): Promise<Thumbnail[]> {
    const media = await db.media.findUnique({ where: { id: mediaId } });

    if (!media || media.type !== 'image') {
      throw new Error('Not an image');
    }

    const sizes = [
      { name: 'thumbnail', width: 150, height: 150 },
      { name: 'small', width: 300, height: 300 },
      { name: 'medium', width: 600, height: 600 },
      { name: 'large', width: 1200, height: 1200 }
    ];

    const thumbnails: Thumbnail[] = [];

    for (const size of sizes) {
      const buffer = await this.downloadFromS3(media.storagePath);
      
      const resized = await sharp(buffer)
        .resize(size.width, size.height, {
          fit: 'cover',
          position: 'center'
        })
        .jpeg({ quality: 80 })
        .toBuffer();

      const path = `thumbnails/${media.filename}-${size.name}.jpg`;
      
      await this.uploadToS3(path, resized, 'image/jpeg');

      thumbnails.push({
        size: size.name,
        width: size.width,
        height: size.height,
        url: `${process.env.CDN_URL}/${path}`
      });
    }

    // Update media metadata
    await db.media.update({
      where: { id: mediaId },
      data: {
        metadata: {
          ...media.metadata,
          thumbnails
        }
      }
    });

    return thumbnails;
  }

  async optimizeImage(buffer: Buffer, options: OptimizeOptions): Promise<Buffer> {
    let image = sharp(buffer);

    if (options.width || options.height) {
      image = image.resize(options.width, options.height, {
        fit: options.fit || 'cover',
        position: 'center'
      });
    }

    if (options.format === 'webp') {
      return image.webp({ quality: options.quality || 80 }).toBuffer();
    }

    return image.jpeg({ quality: options.quality || 85 }).toBuffer();
  }

  private async downloadFromS3(key: string): Promise<Buffer> {
    const result = await this.s3.getObject({
      Bucket: process.env.AWS_S3_BUCKET!,
      Key: key
    }).promise();

    return result.Body as Buffer;
  }

  private async uploadToS3(key: string, buffer: Buffer, contentType: string): Promise<void> {
    await this.s3.upload({
      Bucket: process.env.AWS_S3_BUCKET!,
      Key: key,
      Body: buffer,
      ContentType: contentType,
      ACL: 'public-read'
    }).promise();
  }
}

interface Thumbnail {
  size: string;
  width: number;
  height: number;
  url: string;
}

interface OptimizeOptions {
  width?: number;
  height?: number;
  quality?: number;
  format?: 'jpeg' | 'png' | 'webp';
  fit?: 'cover' | 'contain' | 'fill' | 'inside' | 'outside';
}
```

## Video Processing

```typescript
// services/video-processing.service.ts
import ffmpeg from 'fluent-ffmpeg';

export class VideoProcessingService {
  async processVideo(mediaId: string): Promise<void> {
    const media = await db.media.findUnique({ where: { id: mediaId } });

    if (!media || media.type !== 'video') {
      throw new Error('Not a video');
    }

    // Generate thumbnail
    await this.generateVideoThumbnail(media);

    // Transcode to multiple formats
    await this.transcodeVideo(media);
  }

  private async generateVideoThumbnail(media: Media): Promise<void> {
    const inputPath = await this.downloadFromS3(media.storagePath);
    const outputPath = `thumbnails/${media.filename}-thumb.jpg`;

    return new Promise((resolve, reject) => {
      ffmpeg(inputPath)
        .screenshots({
          timestamps: ['50%'],
          filename: outputPath,
          size: '640x360'
        })
        .on('end', async () => {
          await this.uploadToS3(outputPath, outputPath, 'image/jpeg');
          resolve();
        })
        .on('error', reject);
    });
  }

  private async transcodeVideo(media: Media): Promise<void> {
    const qualities = [
      { name: '720p', width: 1280, height: 720, bitrate: '2500k' },
      { name: '480p', width: 854, height: 480, bitrate: '1000k' },
      { name: '360p', width: 640, height: 360, bitrate: '500k' }
    ];

    for (const quality of qualities) {
      await this.transcodeToQuality(media, quality);
    }
  }

  private async transcodeToQuality(media: Media, quality: any): Promise<void> {
    const inputPath = await this.downloadFromS3(media.storagePath);
    const outputPath = `videos/${media.filename}-${quality.name}.mp4`;

    return new Promise((resolve, reject) => {
      ffmpeg(inputPath)
        .size(`${quality.width}x${quality.height}`)
        .videoBitrate(quality.bitrate)
        .output(outputPath)
        .on('end', async () => {
          await this.uploadToS3(outputPath, outputPath, 'video/mp4');
          resolve();
        })
        .on('error', reject)
        .run();
    });
  }
}
```

## Metadata Extraction

```typescript
// services/metadata-extraction.service.ts
import exifr from 'exifr';

export class MetadataExtractionService {
  async extractMetadata(mediaId: string): Promise<void> {
    const media = await db.media.findUnique({ where: { id: mediaId } });

    if (!media) throw new Error('Media not found');

    let metadata: any = {};

    if (media.type === 'image') {
      metadata = await this.extractImageMetadata(media.storagePath);
    }

    await db.media.update({
      where: { id: mediaId },
      data: {
        metadata: {
          ...media.metadata,
          ...metadata
        }
      }
    });
  }

  private async extractImageMetadata(storagePath: string): Promise<any> {
    const buffer = await this.downloadFromS3(storagePath);
    const exif = await exifr.parse(buffer);

    return {
      camera: exif?.Make,
      model: exif?.Model,
      dateTaken: exif?.DateTimeOriginal,
      iso: exif?.ISO,
      aperture: exif?.FNumber,
      shutterSpeed: exif?.ExposureTime,
      focalLength: exif?.FocalLength,
      gps: exif?.latitude && exif?.longitude ? {
        latitude: exif.latitude,
        longitude: exif.longitude
      } : null
    };
  }
}
```

## Search and Filtering

```typescript
// services/media-search.service.ts
export class MediaSearchService {
  async searchMedia(query: SearchQuery): Promise<SearchResult> {
    const where: any = {};

    if (query.search) {
      where.OR = [
        { filename: { contains: query.search, mode: 'insensitive' } },
        { originalFilename: { contains: query.search, mode: 'insensitive' } }
      ];
    }

    if (query.type) {
      where.type = query.type;
    }

    if (query.folderId) {
      where.folderId = query.folderId;
    }

    if (query.tags && query.tags.length > 0) {
      where.tags = {
        some: {
          tagId: { in: query.tags }
        }
      };
    }

    const [media, total] = await Promise.all([
      db.media.findMany({
        where,
        skip: query.skip || 0,
        take: query.limit || 20,
        orderBy: query.orderBy || { createdAt: 'desc' },
        include: {
          folder: true,
          tags: {
            include: { tag: true }
          }
        }
      }),
      db.media.count({ where })
    ]);

    return { media, total };
  }
}

interface SearchQuery {
  search?: string;
  type?: string;
  folderId?: string;
  tags?: string[];
  skip?: number;
  limit?: number;
  orderBy?: any;
}

interface SearchResult {
  media: Media[];
  total: number;
}
```

## Folders and Organization

```typescript
// services/media-folder.service.ts
export class MediaFolderService {
  async createFolder(name: string, parentId?: string, userId?: string): Promise<MediaFolder> {
    const parent = parentId
      ? await db.mediaFolder.findUnique({ where: { id: parentId } })
      : null;

    const path = parent ? `${parent.path}/${name}` : name;

    return db.mediaFolder.create({
      data: {
        name,
        parentId,
        path,
        createdBy: userId
      }
    });
  }

  async moveMedia(mediaId: string, folderId: string): Promise<void> {
    await db.media.update({
      where: { id: mediaId },
      data: { folderId }
    });
  }

  async getFolderTree(): Promise<FolderNode[]> {
    const folders = await db.mediaFolder.findMany({
      include: {
        _count: {
          select: { media: true }
        }
      }
    });

    return this.buildTree(folders, null);
  }

  private buildTree(folders: any[], parentId: string | null): FolderNode[] {
    return folders
      .filter(f => f.parentId === parentId)
      .map(folder => ({
        id: folder.id,
        name: folder.name,
        path: folder.path,
        mediaCount: folder._count.media,
        children: this.buildTree(folders, folder.id)
      }));
  }
}

interface FolderNode {
  id: string;
  name: string;
  path: string;
  mediaCount: number;
  children: FolderNode[];
}
```

## CDN Integration

```typescript
// services/cdn.service.ts
export class CDNService {
  async getSignedUrl(mediaId: string, expiresIn: number = 3600): Promise<string> {
    const media = await db.media.findUnique({ where: { id: mediaId } });

    if (!media) throw new Error('Media not found');

    const params = {
      Bucket: process.env.AWS_S3_BUCKET!,
      Key: media.storagePath,
      Expires: expiresIn
    };

    return this.s3.getSignedUrl('getObject', params);
  }

  async invalidateCache(paths: string[]): Promise<void> {
    // CloudFront invalidation
    const cloudfront = new AWS.CloudFront();

    await cloudfront.createInvalidation({
      DistributionId: process.env.CLOUDFRONT_DISTRIBUTION_ID!,
      InvalidationBatch: {
        CallerReference: Date.now().toString(),
        Paths: {
          Quantity: paths.length,
          Items: paths
        }
      }
    }).promise();
  }
}
```

## Bulk Operations

```typescript
// services/media-bulk.service.ts
export class MediaBulkService {
  async bulkDelete(mediaIds: string[]): Promise<number> {
    const media = await db.media.findMany({
      where: { id: { in: mediaIds } }
    });

    // Delete from S3
    await Promise.all(
      media.map(m => this.deleteFromS3(m.storagePath))
    );

    // Delete from database
    const result = await db.media.deleteMany({
      where: { id: { in: mediaIds } }
    });

    return result.count;
  }

  async bulkMove(mediaIds: string[], folderId: string): Promise<number> {
    const result = await db.media.updateMany({
      where: { id: { in: mediaIds } },
      data: { folderId }
    });

    return result.count;
  }

  async bulkTag(mediaIds: string[], tagIds: string[]): Promise<void> {
    const relations = mediaIds.flatMap(mediaId =>
      tagIds.map(tagId => ({ mediaId, tagId }))
    );

    await db.mediaTagRelation.createMany({
      data: relations,
      skipDuplicates: true
    });
  }
}
```

## Best Practices

1. **Validation** - Validate file types and sizes
2. **Optimization** - Optimize images automatically
3. **Thumbnails** - Generate multiple sizes
4. **CDN** - Use CDN for delivery
5. **Metadata** - Extract and store metadata
6. **Organization** - Provide folders and tags
7. **Search** - Implement full-text search
8. **Permissions** - Control access to media
9. **Bulk Operations** - Support bulk actions
10. **Performance** - Lazy load thumbnails
```

---

## Quick Start

### Media Upload

```typescript
interface Media {
  id: string
  filename: string
  mimeType: string
  size: number
  url: string
  thumbnailUrl?: string
  metadata: Record<string, any>
}

async function uploadMedia(file: File): Promise<Media> {
  // Validate
  validateFile(file)
  
  // Upload to S3
  const s3Key = `media/${Date.now()}-${file.name}`
  await s3.upload({
    Bucket: process.env.S3_BUCKET,
    Key: s3Key,
    Body: file.buffer,
    ContentType: file.mimetype
  })
  
  // Generate thumbnail
  const thumbnail = await generateThumbnail(file)
  
  // Save metadata
  return await db.media.create({
    data: {
      filename: file.name,
      mimeType: file.mimetype,
      size: file.size,
      url: `https://cdn.example.com/${s3Key}`,
      thumbnailUrl: thumbnail ? `https://cdn.example.com/thumbnails/${s3Key}` : undefined,
      metadata: await extractMetadata(file)
    }
  })
}
```

---

## Production Checklist

- [ ] **Upload**: File upload functionality
- [ ] **Validation**: File type and size validation
- [ ] **Processing**: Image/video processing
- [ ] **Optimization**: Automatic optimization
- [ ] **Thumbnails**: Thumbnail generation
- [ ] **Storage**: Cloud storage (S3, etc.)
- [ ] **CDN**: CDN for delivery
- [ ] **Metadata**: Extract and store metadata
- [ ] **Organization**: Folders and tags
- [ ] **Search**: Full-text search
- [ ] **Permissions**: Access control
- [ ] **Performance**: Optimize for large files

---

## Anti-patterns

### ❌ Don't: No Validation

```typescript
// ❌ Bad - No validation
await uploadFile(file)
// Could be malicious file!
```

```typescript
// ✅ Good - Validate
if (!isValidFileType(file.mimetype)) {
  throw new Error('Invalid file type')
}
if (file.size > MAX_FILE_SIZE) {
  throw new Error('File too large')
}
await uploadFile(file)
```

### ❌ Don't: No Optimization

```typescript
// ❌ Bad - Upload as-is
await uploadFile(file)
// Large file, slow loading!
```

```typescript
// ✅ Good - Optimize
const optimized = await optimizeImage(file)
await uploadFile(optimized)
// Smaller file, faster loading
```

---

## Integration Points

- **Contentful Integration** (`33-content-management/contentful-integration/`) - CMS media
- **CDN Delivery** (`37-video-streaming/cdn-delivery/`) - Media CDN
- **File Storage** (`13-file-storage/`) - Storage patterns

---

## Further Reading

- [Media Library Best Practices](https://www.contentful.com/developers/docs/concepts/media/)
- [Image Optimization](https://web.dev/fast/#optimize-your-images)

---

## Quick Start

### Media Upload

```typescript
interface Media {
  id: string
  filename: string
  mimeType: string
  size: number
  url: string
  thumbnailUrl?: string
  metadata: Record<string, any>
}

async function uploadMedia(file: File): Promise<Media> {
  // Validate
  validateFile(file)
  
  // Upload to S3
  const s3Key = `media/${Date.now()}-${file.name}`
  await s3.upload({
    Bucket: process.env.S3_BUCKET,
    Key: s3Key,
    Body: file.buffer,
    ContentType: file.mimetype
  })
  
  // Generate thumbnail
  const thumbnail = await generateThumbnail(file)
  
  // Save metadata
  return await db.media.create({
    data: {
      filename: file.name,
      mimeType: file.mimetype,
      size: file.size,
      url: `https://cdn.example.com/${s3Key}`,
      thumbnailUrl: thumbnail ? `https://cdn.example.com/thumbnails/${s3Key}` : undefined,
      metadata: await extractMetadata(file)
    }
  })
}
```

---

## Production Checklist

- [ ] **Upload**: File upload functionality
- [ ] **Validation**: File type and size validation
- [ ] **Processing**: Image/video processing
- [ ] **Optimization**: Automatic optimization
- [ ] **Thumbnails**: Thumbnail generation
- [ ] **Storage**: Cloud storage (S3, etc.)
- [ ] **CDN**: CDN for delivery
- [ ] **Metadata**: Extract and store metadata
- [ ] **Organization**: Folders and tags
- [ ] **Search**: Full-text search
- [ ] **Permissions**: Access control
- [ ] **Performance**: Optimize for large files

---

## Anti-patterns

### ❌ Don't: No Validation

```typescript
// ❌ Bad - No validation
await uploadFile(file)
// Could be malicious file!
```

```typescript
// ✅ Good - Validate
if (!isValidFileType(file.mimetype)) {
  throw new Error('Invalid file type')
}
if (file.size > MAX_FILE_SIZE) {
  throw new Error('File too large')
}
await uploadFile(file)
```

### ❌ Don't: No Optimization

```typescript
// ❌ Bad - Upload as-is
await uploadFile(file)
// Large file, slow loading!
```

```typescript
// ✅ Good - Optimize
const optimized = await optimizeImage(file)
await uploadFile(optimized)
// Smaller file, faster loading
```

---

## Integration Points

- **Contentful Integration** (`33-content-management/contentful-integration/`) - CMS media
- **CDN Delivery** (`37-video-streaming/cdn-delivery/`) - Media CDN
- **File Storage** (`13-file-storage/`) - Storage patterns

---

## Further Reading

- [Media Library Best Practices](https://www.contentful.com/developers/docs/concepts/media/)
- [Image Optimization](https://web.dev/fast/#optimize-your-images)

## Resources

- [Sharp](https://sharp.pixelplumbing.com/)
- [FFmpeg](https://ffmpeg.org/)
- [AWS S3](https://aws.amazon.com/s3/)
- [CloudFront](https://aws.amazon.com/cloudfront/)
