# Image Optimization

## Overview

Image optimization reduces file size while maintaining visual quality, improving page load times and reducing bandwidth costs. This skill covers image formats, compression techniques, and optimization strategies.

## Table of Contents

1. [Image Formats](#image-formats)
2. [Compression](#compression)
3. [Resizing and Scaling](#resizing-and-scaling)
4. [Responsive Images](#responsive-images)
5. [Lazy Loading](#lazy-loading)
6. [Image CDN](#image-cdn)
7. [Next.js Image Component](#nextjs-image-component)
8. [Sharp Library (Node.js)](#sharp-library-nodejs)
9. [Pillow (Python)](#pillow-python)
10. [Automated Optimization](#automated-optimization)
11. [Performance Metrics](#performance-metrics)
12. [Best Practices](#best-practices)

---

## Image Formats

### JPEG (Joint Photographic Experts Group)

- **Use Case**: Photographs, complex images with gradients
- **Compression**: Lossy
- **Transparency**: No
- **Browser Support**: Universal
- **Best Quality**: 80-90%

```typescript
// jpeg.ts
import sharp from 'sharp';

async function optimizeJPEG(inputPath: string, outputPath: string, quality: number = 85): Promise<void> {
  await sharp(inputPath)
    .jpeg({
      quality,
      progressive: true, // Progressive JPEG for faster loading
      mozjpeg: true,    // Better compression
    })
    .toFile(outputPath);
}
```

```python
# jpeg.py
from PIL import Image

def optimize_jpeg(input_path: str, output_path: str, quality: int = 85) -> None:
    """Optimize JPEG image."""
    img = Image.open(input_path)
    
    # Convert to RGB if necessary
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    img.save(
        output_path,
        'JPEG',
        quality=quality,
        optimize=True,
        progressive=True
    )
```

### PNG (Portable Network Graphics)

- **Use Case**: Graphics, logos, images with transparency
- **Compression**: Lossless
- **Transparency**: Yes (alpha channel)
- **Browser Support**: Universal
- **Best For**: Images with few colors or requiring transparency

```typescript
// png.ts
import sharp from 'sharp';

async function optimizePNG(inputPath: string, outputPath: string): Promise<void> {
  await sharp(inputPath)
    .png({
      compressionLevel: 9,  // Maximum compression
      adaptiveFiltering: true,
      palette: true,  // Use palette for images with few colors
    })
    .toFile(outputPath);
}
```

```python
# png.py
from PIL import Image

def optimize_png(input_path: str, output_path: str) -> None:
    """Optimize PNG image."""
    img = Image.open(input_path)
    
    # Convert to RGBA if necessary
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    img.save(
        output_path,
        'PNG',
        optimize=True,
        compress_level=9
    )
```

### WebP

- **Use Case**: Modern web applications
- **Compression**: Lossy and lossless
- **Transparency**: Yes
- **Browser Support**: Modern browsers (95%+)
- **Best For**: General web images

```typescript
// webp.ts
import sharp from 'sharp';

async function convertToWebP(inputPath: string, outputPath: string, quality: number = 80): Promise<void> {
  await sharp(inputPath)
    .webp({
      quality,
      nearLossless: true,
      smartSubsample: true,
    })
    .toFile(outputPath);
}
```

```python
# webp.py
from PIL import Image

def convert_to_webp(input_path: str, output_path: str, quality: int = 80) -> None:
    """Convert image to WebP format."""
    img = Image.open(input_path)
    
    # Convert to RGBA if necessary
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    img.save(
        output_path,
        'WEBP',
        quality=quality,
        method=6,  # Compression method (0-6, higher = slower but better)
        lossless=False
    )
```

### AVIF

- **Use Case**: Next-generation web images
- **Compression**: Superior to WebP
- **Transparency**: Yes
- **Browser Support**: Modern browsers (70%+)
- **Best For**: Maximum compression

```typescript
// avif.ts
import sharp from 'sharp';

async function convertToAVIF(inputPath: string, outputPath: string, quality: number = 75): Promise<void> {
  await sharp(inputPath)
    .avif({
      quality,
      effort: 6,  // Compression effort (0-9, higher = slower but better)
    })
    .toFile(outputPath);
}
```

```python
# avif.py
from PIL import Image

def convert_to_avif(input_path: str, output_path: str, quality: int = 75) -> None:
    """Convert image to AVIF format."""
    img = Image.open(input_path)
    
    # AVIF requires pillow-heif
    try:
        from pillow_heif import register_heif_opener
        register_heif_opener()
    except ImportError:
        raise ImportError("pillow-heif is required for AVIF support")
    
    img.save(
        output_path,
        'AVIF',
        quality=quality,
        speed=4  # Encoding speed (0-10, lower = slower but better)
    )
```

### Format Comparison

| Format | Compression | Transparency | Size | Browser Support | Best Use Case |
|--------|-------------|--------------|------|-----------------|---------------|
| JPEG | Lossy | No | Medium | 100% | Photos |
| PNG | Lossless | Yes | Large | 100% | Graphics, logos |
| WebP | Both | Yes | Small | 95% | Web images |
| AVIF | Both | Yes | Smallest | 70% | Modern web |

---

## Compression

### Lossy vs Lossless

```typescript
// compression-types.ts
import sharp from 'sharp';

// Lossy compression (JPEG, WebP)
async function lossyCompression(input: Buffer, quality: number = 80): Promise<Buffer> {
  return sharp(input)
    .jpeg({ quality })
    .toBuffer();
}

// Lossless compression (PNG)
async function losslessCompression(input: Buffer): Promise<Buffer> {
  return sharp(input)
    .png({ compressionLevel: 9 })
    .toBuffer();
}
```

### Quality Settings

```typescript
// quality-settings.ts
import sharp from 'sharp';

interface QualityLevels {
  low: number;    // 50-60 - Smallest file, visible artifacts
  medium: number; // 70-80 - Good balance
  high: number;   // 85-95 - Best quality, larger file
}

const qualityPresets: Record<string, QualityLevels> = {
  thumbnail: { low: 50, medium: 60, high: 70 },
  web: { low: 70, medium: 80, high: 85 },
  print: { low: 85, medium: 90, high: 95 },
};

async function optimizeWithQuality(
  input: Buffer,
  format: 'jpeg' | 'webp' | 'avif',
  preset: keyof typeof qualityPresets,
  level: keyof QualityLevels
): Promise<Buffer> {
  const quality = qualityPresets[preset][level];

  switch (format) {
    case 'jpeg':
      return sharp(input).jpeg({ quality }).toBuffer();
    case 'webp':
      return sharp(input).webp({ quality }).toBuffer();
    case 'avif':
      return sharp(input).avif({ quality }).toBuffer();
  }
}
```

```python
# quality_settings.py
from PIL import Image
from typing import Literal

def optimize_with_quality(
    input_path: str,
    output_path: str,
    format: Literal['JPEG', 'WEBP', 'AVIF'],
    quality: int = 80
) -> None:
    """Optimize image with specific quality."""
    img = Image.open(input_path)
    
    if format == 'JPEG':
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img.save(output_path, 'JPEG', quality=quality, optimize=True)
    
    elif format == 'WEBP':
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        img.save(output_path, 'WEBP', quality=quality, method=6)
    
    elif format == 'AVIF':
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        img.save(output_path, 'AVIF', quality=quality, speed=4)
```

---

## Resizing and Scaling

### Basic Resizing

```typescript
// resizing.ts
import sharp from 'sharp';

async function resizeImage(
  input: Buffer,
  width: number,
  height?: number,
  options?: {
    fit?: 'cover' | 'contain' | 'fill' | 'inside' | 'outside';
    position?: 'top' | 'bottom' | 'left' | 'right' | 'center';
  }
): Promise<Buffer> {
  return sharp(input)
    .resize(width, height, {
      fit: options?.fit || 'cover',
      position: options?.position || 'center',
      withoutEnlargement: true,  // Don't upscale
    })
    .toBuffer();
}
```

```python
# resizing.py
from PIL import Image
from typing import Optional, Literal

def resize_image(
    input_path: str,
    output_path: str,
    width: int,
    height: Optional[int] = None,
    fit: Literal['cover', 'contain', 'fill'] = 'cover'
) -> None:
    """Resize image with specified dimensions."""
    img = Image.open(input_path)
    
    if fit == 'cover':
        # Crop to fill the exact dimensions
        img = ImageOps.fit(
            img,
            (width, height or width),
            method=Image.Resampling.LANCZOS,
            centering=(0.5, 0.5)
        )
    elif fit == 'contain':
        # Resize to fit within dimensions
        img.thumbnail((width, height or width), Image.Resampling.LANCZOS)
    elif fit == 'fill':
        # Resize and stretch
        img = img.resize((width, height or width), Image.Resampling.LANCZOS)
    
    img.save(output_path)
```

### Generate Multiple Sizes

```typescript
// multiple-sizes.ts
import sharp from 'sharp';

interface ImageSize {
  name: string;
  width: number;
  height?: number;
  quality?: number;
}

async function generateImageSizes(
  input: Buffer,
  sizes: ImageSize[],
  format: 'jpeg' | 'webp' | 'png' = 'webp'
): Promise<Record<string, Buffer>> {
  const results: Record<string, Buffer> = {};

  for (const size of sizes) {
    let pipeline = sharp(input);

    if (size.width || size.height) {
      pipeline = pipeline.resize(size.width, size.height, {
        fit: 'inside',
        withoutEnlargement: true,
      });
    }

    switch (format) {
      case 'jpeg':
        pipeline = pipeline.jpeg({ quality: size.quality || 80 });
        break;
      case 'webp':
        pipeline = pipeline.webp({ quality: size.quality || 80 });
        break;
      case 'png':
        pipeline = pipeline.png({ compressionLevel: 9 });
        break;
    }

    results[size.name] = await pipeline.toBuffer();
  }

  return results;
}

// Usage
const sizes = [
  { name: 'thumbnail', width: 150, height: 150, quality: 70 },
  { name: 'small', width: 300, quality: 75 },
  { name: 'medium', width: 600, quality: 80 },
  { name: 'large', width: 1200, quality: 85 },
];

const variants = await generateImageSizes(inputBuffer, sizes, 'webp');
```

```python
# multiple_sizes.py
from PIL import Image
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class ImageSize:
    name: str
    width: int
    height: int = None
    quality: int = 80

def generate_image_sizes(
    input_path: str,
    sizes: List[ImageSize],
    format: str = 'WEBP'
) -> Dict[str, bytes]:
    """Generate multiple image sizes."""
    img = Image.open(input_path)
    results = {}
    
    for size in sizes:
        resized = img.copy()
        
        if size.width or size.height:
            resized.thumbnail((size.width, size.height or size.width), Image.Resampling.LANCZOS)
        
        output = io.BytesIO()
        
        if format == 'JPEG':
            if resized.mode != 'RGB':
                resized = resized.convert('RGB')
            resized.save(output, 'JPEG', quality=size.quality, optimize=True)
        elif format == 'WEBP':
            if resized.mode != 'RGBA':
                resized = resized.convert('RGBA')
            resized.save(output, 'WEBP', quality=size.quality, method=6)
        elif format == 'PNG':
            if resized.mode != 'RGBA':
                resized = resized.convert('RGBA')
            resized.save(output, 'PNG', optimize=True, compress_level=9)
        
        results[size.name] = output.getvalue()
    
    return results
```

---

## Responsive Images

### srcset and sizes

```html
<!-- responsive-images.html -->
<img
  src="image-800.webp"
  srcset="
    image-400.webp 400w,
    image-800.webp 800w,
    image-1200.webp 1200w,
    image-1600.webp 1600w
  "
  sizes="
    (max-width: 600px) 400px,
    (max-width: 1200px) 800px,
    (max-width: 1600px) 1200px,
    1600px
  "
  alt="Responsive image"
  loading="lazy"
/>
```

### Picture Element

```html
<!-- picture-element.html -->
<picture>
  <source
    srcset="image.avif"
    type="image/avif"
  />
  <source
    srcset="image.webp"
    type="image/webp"
  />
  <img
    src="image.jpg"
    alt="Fallback image"
    loading="lazy"
  />
</picture>
```

### Generate Responsive Images

```typescript
// responsive-generator.ts
import sharp from 'sharp';

interface ResponsiveConfig {
  widths: number[];
  formats: Array<{ name: string; format: 'jpeg' | 'webp' | 'avif'; quality?: number }>;
}

async function generateResponsiveImages(
  input: Buffer,
  config: ResponsiveConfig
): Promise<Record<string, Buffer>> {
  const results: Record<string, Buffer> = {};

  for (const format of config.formats) {
    for (const width of config.widths) {
      const filename = `${format.name}-${width}.${format.format}`;

      results[filename] = await sharp(input)
        .resize(width, null, {
          fit: 'inside',
          withoutEnlargement: true,
        })
        .toFormat(format.format, { quality: format.quality || 80 })
        .toBuffer();
    }
  }

  return results;
}

// Generate HTML
function generateResponsiveHTML(
  baseName: string,
  config: ResponsiveConfig
): string {
  const webpFormat = config.formats.find(f => f.format === 'webp');
  const avifFormat = config.formats.find(f => f.format === 'avif');
  const jpegFormat = config.formats.find(f => f.format === 'jpeg');

  const webpSrcset = webpFormat
    ? config.widths.map(w => `${baseName}-${w}.webp ${w}w`).join(', ')
    : '';

  const avifSrcset = avifFormat
    ? config.widths.map(w => `${baseName}-${w}.avif ${w}w`).join(', ')
    : '';

  const jpegSrcset = jpegFormat
    ? config.widths.map(w => `${baseName}-${w}.jpg ${w}w`).join(', ')
    : '';

  const sizes = config.widths.map(w => `(max-width: ${w}px) ${w}px`).join(', ');

  return `
<picture>
  ${avifFormat ? `<source srcset="${avifSrcset}" type="image/avif" />` : ''}
  ${webpFormat ? `<source srcset="${webpSrcset}" type="image/webp" />` : ''}
  <img
    src="${baseName}-${config.widths[0]}.jpg"
    srcset="${jpegSrcset}"
    sizes="${sizes}"
    alt="Responsive image"
    loading="lazy"
  />
</picture>
  `.trim();
}

// Usage
const config: ResponsiveConfig = {
  widths: [400, 800, 1200, 1600],
  formats: [
    { name: 'image', format: 'avif', quality: 75 },
    { name: 'image', format: 'webp', quality: 80 },
    { name: 'image', format: 'jpeg', quality: 85 },
  ],
};

const images = await generateResponsiveImages(inputBuffer, config);
const html = generateResponsiveHTML('image', config);
```

---

## Lazy Loading

### Native Lazy Loading

```html
<!-- native-lazy-loading.html -->
<img
  src="image.jpg"
  alt="Lazy loaded image"
  loading="lazy"
  width="800"
  height="600"
/>
```

### JavaScript Lazy Loading (Intersection Observer)

```typescript
// lazy-loading.ts
class LazyLoader {
  private observer: IntersectionObserver;

  constructor() {
    this.observer = new IntersectionObserver(
      this.handleIntersect.bind(this),
      {
        rootMargin: '50px 0px',
        threshold: 0.01,
      }
    );
  }

  observe(element: HTMLImageElement): void {
    this.observer.observe(element);
  }

  private handleIntersect(entries: IntersectionObserverEntry[]): void {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target as HTMLImageElement;
        const src = img.dataset.src;
        const srcset = img.dataset.srcset;

        if (src) {
          img.src = src;
        }

        if (srcset) {
          img.srcset = srcset;
        }

        img.onload = () => {
          img.classList.add('loaded');
        };

        this.observer.unobserve(img);
      }
    });
  }
}

// Usage
const lazyLoader = new LazyLoader();
document.querySelectorAll('img[data-src]').forEach(img => {
  lazyLoader.observe(img as HTMLImageElement);
});
```

### React Lazy Loading Component

```tsx
// LazyImage.tsx
import React, { useRef, useEffect, useState } from 'react';

interface LazyImageProps {
  src: string;
  srcset?: string;
  alt: string;
  width?: number;
  height?: number;
  className?: string;
}

export function LazyImage({
  src,
  srcset,
  alt,
  width,
  height,
  className,
}: LazyImageProps) {
  const imgRef = useRef<HTMLImageElement>(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [isInView, setIsInView] = useState(false);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsInView(true);
          observer.disconnect();
        }
      },
      { rootMargin: '50px' }
    );

    if (imgRef.current) {
      observer.observe(imgRef.current);
    }

    return () => observer.disconnect();
  }, []);

  return (
    <img
      ref={imgRef}
      src={isInView ? src : undefined}
      srcSet={isInView ? srcset : undefined}
      alt={alt}
      width={width}
      height={height}
      className={`${className || ''} ${isLoaded ? 'loaded' : 'loading'}`}
      onLoad={() => setIsLoaded(true)}
      loading="lazy"
    />
  );
}
```

---

## Image CDN

### Cloudinary

```typescript
// cloudinary.ts
import { v2 as cloudinary } from 'cloudinary';

cloudinary.config({
  cloud_name: process.env.CLOUDINARY_CLOUD_NAME,
  api_key: process.env.CLOUDINARY_API_KEY,
  api_secret: process.env.CLOUDINARY_API_SECRET,
});

function generateCloudinaryURL(
  publicId: string,
  options?: {
    width?: number;
    height?: number;
    quality?: number;
    format?: 'jpg' | 'png' | 'webp' | 'avif';
    crop?: 'fill' | 'fit' | 'limit' | 'mfit' | 'pad' | 'scale';
  }
): string {
  const transformations: string[] = [];

  if (options?.width) transformations.push(`w_${options.width}`);
  if (options?.height) transformations.push(`h_${options.height}`);
  if (options?.quality) transformations.push(`q_${options.quality}`);
  if (options?.format) transformations.push(`f_${options.format}`);
  if (options?.crop) transformations.push(`c_${options.crop}`);

  const transformation = transformations.join(',');

  return cloudinary.url(publicId, {
    transformation: transformation || undefined,
    fetch_format: options?.format || 'auto',
    quality: options?.quality || 'auto',
  });
}

// Usage
const url = generateCloudinaryURL('sample', {
  width: 800,
  height: 600,
  quality: 80,
  format: 'webp',
  crop: 'fill',
});
```

### Imgix

```typescript
// imgix.ts
function generateImgixURL(
  baseUrl: string,
  imagePath: string,
  options?: {
    width?: number;
    height?: number;
    quality?: number;
    format?: 'jpg' | 'png' | 'webp' | 'avif';
    fit?: 'fill' | 'fit' | 'max' | 'min' | 'scale';
    auto?: 'format' | 'compress' | 'enhance';
  }
): string {
  const params = new URLSearchParams();

  if (options?.width) params.set('w', options.width.toString());
  if (options?.height) params.set('h', options.height.toString());
  if (options?.quality) params.set('q', options.quality.toString());
  if (options?.format) params.set('fm', options.format);
  if (options?.fit) params.set('fit', options.fit);
  if (options?.auto) params.set('auto', options.auto);

  const queryString = params.toString();
  return `${baseUrl}${imagePath}${queryString ? `?${queryString}` : ''}`;
}

// Usage
const url = generateImgixURL('https://example.imgix.net', '/image.jpg', {
  width: 800,
  height: 600,
  quality: 80,
  format: 'webp',
  fit: 'fill',
  auto: 'format,compress',
});
```

---

## Next.js Image Component

### Basic Usage

```tsx
// ImageComponent.tsx
import Image from 'next/image';

export function OptimizedImage() {
  return (
    <Image
      src="/images/photo.jpg"
      alt="Optimized image"
      width={800}
      height={600}
      priority  // Load above the fold
    />
  );
}
```

### Responsive Images

```tsx
// ResponsiveImage.tsx
import Image from 'next/image';

export function ResponsiveImage() {
  return (
    <Image
      src="/images/photo.jpg"
      alt="Responsive image"
      width={800}
      height={600}
      sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
      priority
    />
  );
}
```

### Remote Images

```tsx
// RemoteImage.tsx
import Image from 'next/image';

export function RemoteImage() {
  return (
    <Image
      src="https://example.com/image.jpg"
      alt="Remote image"
      width={800}
      height={600}
      loader={({ src, width, quality }) => {
        return `${src}?w=${width}&q=${quality || 75}`;
      }}
    />
  );
}
```

### Next.js Config

```javascript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    domains: ['example.com', 'cdn.example.com'],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
    formats: ['image/avif', 'image/webp'],
    minimumCacheTTL: 60,
  },
};

module.exports = nextConfig;
```

---

## Sharp Library (Node.js)

### Basic Operations

```typescript
// sharp-basics.ts
import sharp from 'sharp';

// Resize
async function resize(input: Buffer, width: number, height: number): Promise<Buffer> {
  return sharp(input)
    .resize(width, height)
    .toBuffer();
}

// Crop
async function crop(
  input: Buffer,
  left: number,
  top: number,
  width: number,
  height: number
): Promise<Buffer> {
  return sharp(input)
    .extract({ left, top, width, height })
    .toBuffer();
}

// Rotate
async function rotate(input: Buffer, angle: number): Promise<Buffer> {
  return sharp(input)
    .rotate(angle)
    .toBuffer();
}

// Flip and flop
async function flip(input: Buffer): Promise<Buffer> {
  return sharp(input)
    .flip()
    .toBuffer();
}

async function flop(input: Buffer): Promise<Buffer> {
  return sharp(input)
    .flop()
    .toBuffer();
}
```

### Advanced Operations

```typescript
// sharp-advanced.ts
import sharp from 'sharp';

// Blur
async function blur(input: Buffer, sigma: number = 3): Promise<Buffer> {
  return sharp(input)
    .blur(sigma)
    .toBuffer();
}

// Sharpen
async function sharpen(input: Buffer, options?: {
  sigma?: number;
  flat?: number;
  jagged?: number;
}): Promise<Buffer> {
  return sharp(input)
    .sharpen(options)
    .toBuffer();
}

// Adjust brightness, contrast, saturation
async function adjustColors(
  input: Buffer,
  options: {
    brightness?: number;  // -1 to 1
    contrast?: number;    // -1 to 1
    saturation?: number;   // -1 to 1
  }
): Promise<Buffer> {
  return sharp(input)
    .modulate({
      brightness: options.brightness,
      contrast: options.contrast,
      saturation: options.saturation,
    })
    .toBuffer();
}

// Add watermark
async function addWatermark(
  input: Buffer,
  watermark: Buffer,
  gravity: 'southeast' | 'southwest' | 'northeast' | 'northwest' | 'center' = 'southeast'
): Promise<Buffer> {
  return sharp(input)
    .composite([
      {
        input: watermark,
        gravity,
      },
    ])
    .toBuffer();
}

// Remove metadata
async function stripMetadata(input: Buffer): Promise<Buffer> {
  return sharp(input)
    .withMetadata({})  // Remove all metadata
    .toBuffer();
}
```

---

## Pillow (Python)

### Basic Operations

```python
# pillow_basics.py
from PIL import Image, ImageOps, ImageFilter
from typing import Tuple

def resize(input_path: str, output_path: str, size: Tuple[int, int]) -> None:
    """Resize image to specified dimensions."""
    img = Image.open(input_path)
    resized = img.resize(size, Image.Resampling.LANCZOS)
    resized.save(output_path)

def crop(input_path: str, output_path: str, box: Tuple[int, int, int, int]) -> None:
    """Crop image to specified box (left, top, right, bottom)."""
    img = Image.open(input_path)
    cropped = img.crop(box)
    cropped.save(output_path)

def rotate(input_path: str, output_path: str, angle: float) -> None:
    """Rotate image by specified angle."""
    img = Image.open(input_path)
    rotated = img.rotate(angle, expand=True)
    rotated.save(output_path)

def flip(input_path: str, output_path: str) -> None:
    """Flip image vertically."""
    img = Image.open(input_path)
    flipped = ImageOps.flip(img)
    flipped.save(output_path)

def mirror(input_path: str, output_path: str) -> None:
    """Mirror image horizontally."""
    img = Image.open(input_path)
    mirrored = ImageOps.mirror(img)
    mirrored.save(output_path)
```

### Advanced Operations

```python
# pillow_advanced.py
from PIL import Image, ImageEnhance, ImageDraw, ImageFont

def blur(input_path: str, output_path: str, radius: int = 3) -> None:
    """Apply blur filter to image."""
    img = Image.open(input_path)
    blurred = img.filter(ImageFilter.GaussianBlur(radius))
    blurred.save(output_path)

def sharpen(input_path: str, output_path: str) -> None:
    """Apply sharpen filter to image."""
    img = Image.open(input_path)
    sharpened = img.filter(ImageFilter.SHARPEN)
    sharpened.save(output_path)

def adjust_brightness(input_path: str, output_path: str, factor: float = 1.0) -> None:
    """Adjust image brightness (factor > 1 = brighter, < 1 = darker)."""
    img = Image.open(input_path)
    enhancer = ImageEnhance.Brightness(img)
    adjusted = enhancer.enhance(factor)
    adjusted.save(output_path)

def adjust_contrast(input_path: str, output_path: str, factor: float = 1.0) -> None:
    """Adjust image contrast (factor > 1 = more contrast, < 1 = less)."""
    img = Image.open(input_path)
    enhancer = ImageEnhance.Contrast(img)
    adjusted = enhancer.enhance(factor)
    adjusted.save(output_path)

def add_watermark(
    input_path: str,
    output_path: str,
    watermark_text: str,
    position: str = 'bottom-right'
) -> None:
    """Add text watermark to image."""
    img = Image.open(input_path)
    
    # Convert to RGBA if necessary
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Create transparent overlay
    overlay = Image.new('RGBA', img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Use default font or load custom font
    try:
        font = ImageFont.truetype('arial.ttf', 36)
    except:
        font = ImageFont.load_default()
    
    # Calculate position
    bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    if position == 'bottom-right':
        x = img.width - text_width - 20
        y = img.height - text_height - 20
    elif position == 'bottom-left':
        x = 20
        y = img.height - text_height - 20
    elif position == 'top-right':
        x = img.width - text_width - 20
        y = 20
    else:  # top-left
        x = 20
        y = 20
    
    # Draw text
    draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 128))
    
    # Composite overlay onto image
    watermarked = Image.alpha_composite(img, overlay)
    watermarked.save(output_path)
```

---

## Automated Optimization

### Build-Time Optimization

```typescript
// build-optimizer.ts
import fs from 'fs';
import path from 'path';
import sharp from 'sharp';

interface OptimizationConfig {
  inputDir: string;
  outputDir: string;
  formats: Array<{ format: 'jpeg' | 'webp' | 'avif'; quality?: number }>;
  sizes: Array<{ name: string; width: number; height?: number }>;
}

async function optimizeImages(config: OptimizationConfig): Promise<void> {
  const files = await fs.promises.readdir(config.inputDir, { recursive: true });

  for (const file of files) {
    const filePath = path.join(config.inputDir, file as string);
    const stat = await fs.promises.stat(filePath);

    if (stat.isFile() && /\.(jpg|jpeg|png|webp)$/i.test(file)) {
      const input = await fs.promises.readFile(filePath);
      const baseName = path.basename(file, path.extname(file));

      for (const format of config.formats) {
        for (const size of config.sizes) {
          let pipeline = sharp(input);

          if (size.width || size.height) {
            pipeline = pipeline.resize(size.width, size.height, {
              fit: 'inside',
              withoutEnlargement: true,
            });
          }

          pipeline = pipeline.toFormat(format.format, {
            quality: format.quality || 80,
          });

          const outputFileName = `${baseName}-${size.name}.${format.format}`;
          const outputPath = path.join(config.outputDir, outputFileName);

          await pipeline.toFile(outputPath);
          console.log(`Optimized: ${outputFileName}`);
        }
      }
    }
  }
}

// Usage
await optimizeImages({
  inputDir: './src/images',
  outputDir: './public/images',
  formats: [
    { format: 'avif', quality: 75 },
    { format: 'webp', quality: 80 },
    { format: 'jpeg', quality: 85 },
  ],
  sizes: [
    { name: 'thumbnail', width: 150, height: 150 },
    { name: 'small', width: 300 },
    { name: 'medium', width: 600 },
    { name: 'large', width: 1200 },
  ],
});
```

### Runtime Optimization API

```typescript
// optimize-api.ts
import express from 'express';
import sharp from 'sharp';

const app = express();

app.get('/image/:filename', async (req, res) => {
  const { filename } = req.params;
  const width = parseInt(req.query.w as string) || undefined;
  const height = parseInt(req.query.h as string) || undefined;
  const quality = parseInt(req.query.q as string) || 80;
  const format = (req.query.f as string) || 'webp';

  try {
    const inputPath = path.join('./images', filename);
    const input = await fs.promises.readFile(inputPath);

    let pipeline = sharp(input);

    if (width || height) {
      pipeline = pipeline.resize(width, height, {
        fit: 'inside',
        withoutEnlargement: true,
      });
    }

    switch (format) {
      case 'jpeg':
        pipeline = pipeline.jpeg({ quality });
        break;
      case 'png':
        pipeline = pipeline.png({ compressionLevel: 9 });
        break;
      case 'webp':
        pipeline = pipeline.webp({ quality });
        break;
      case 'avif':
        pipeline = pipeline.avif({ quality });
        break;
    }

    const output = await pipeline.toBuffer();

    res.setHeader('Content-Type', `image/${format}`);
    res.setHeader('Cache-Control', 'public, max-age=31536000, immutable');
    res.send(output);
  } catch (error) {
    res.status(404).send('Image not found');
  }
});

app.listen(3000);
```

---

## Performance Metrics

### Calculate Savings

```typescript
// metrics.ts
interface ImageMetrics {
  originalSize: number;
  optimizedSize: number;
  savedBytes: number;
  savedPercentage: number;
  format: string;
  width: number;
  height: number;
}

async function calculateMetrics(
  original: Buffer,
  optimized: Buffer,
  format: string
): Promise<ImageMetrics> {
  const metadata = await sharp(original).metadata();

  return {
    originalSize: original.length,
    optimizedSize: optimized.length,
    savedBytes: original.length - optimized.length,
    savedPercentage: ((original.length - optimized.length) / original.length) * 100,
    format,
    width: metadata.width || 0,
    height: metadata.height || 0,
  };
}

// Usage
const metrics = await calculateMetrics(
  originalBuffer,
  optimizedBuffer,
  'webp'
);

console.log(`Original: ${(metrics.originalSize / 1024).toFixed(2)} KB`);
console.log(`Optimized: ${(metrics.optimizedSize / 1024).toFixed(2)} KB`);
console.log(`Saved: ${metrics.savedPercentage.toFixed(1)}%`);
```

### Lighthouse Image Audit

```typescript
// lighthouse.ts
import lighthouse from 'lighthouse';
import * as chromeLauncher from 'chrome-launcher';

async function auditImages(url: string): Promise<any> {
  const chrome = await chromeLauncher.launch({ chromeFlags: ['--headless'] });

  const options = {
    logLevel: 'info',
    output: 'json',
    port: chrome.port,
    onlyCategories: ['performance'],
  };

  const runnerResult = await lighthouse(url, options);

  await chrome.kill();

  const audits = runnerResult.lhr.audits;
  const imageMetrics = {
    'modern-image-formats': audits['modern-image-formats'],
    'uses-responsive-images': audits['uses-responsive-images'],
    'efficient-animated-content': audits['efficient-animated-content'],
    'offscreen-images': audits['offscreen-images'],
    'unsized-images': audits['unsized-images'],
  };

  return imageMetrics;
}
```

---

## Best Practices

### 1. Choose the Right Format

```typescript
// format-selection.ts
function getOptimalFormat(
  imageType: 'photo' | 'graphic' | 'logo',
  hasTransparency: boolean,
  browserSupport: 'modern' | 'legacy'
): string {
  if (browserSupport === 'modern') {
    return 'avif';
  }

  if (imageType === 'photo') {
    return 'webp';
  }

  if (hasTransparency) {
    return 'png';
  }

  return 'webp';
}
```

### 2. Set Dimensions

```html
<!-- Always set width and height to prevent layout shift -->
<img
  src="image.jpg"
  alt="Image with dimensions"
  width="800"
  height="600"
  loading="lazy"
/>
```

### 3. Use Progressive Loading

```typescript
// progressive.ts
import sharp from 'sharp';

async function createProgressiveJPEG(input: Buffer): Promise<Buffer> {
  return sharp(input)
    .jpeg({
      progressive: true,
      quality: 80,
    })
    .toBuffer();
}
```

### 4. Remove Metadata

```typescript
// strip-metadata.ts
import sharp from 'sharp';

async function stripAllMetadata(input: Buffer): Promise<Buffer> {
  return sharp(input)
    .withMetadata({})  // Remove all metadata
    .toBuffer();
}
```

### 5. Cache Optimized Images

```typescript
// cache.ts
import { createHash } from 'crypto';
import fs from 'fs';
import path from 'path';

const cacheDir = './cache';

async function getCachedImage(
  key: string,
  generator: () => Promise<Buffer>
): Promise<Buffer> {
  const hash = createHash('md5').update(key).digest('hex');
  const cachePath = path.join(cacheDir, `${hash}.bin`);

  try {
    // Try to load from cache
    const cached = await fs.promises.readFile(cachePath);
    return cached;
  } catch {
    // Generate and cache
    const image = await generator();
    await fs.promises.writeFile(cachePath, image);
    return image;
  }
}
```

---

## Summary

This skill covers comprehensive image optimization techniques including:

- **Image Formats**: JPEG, PNG, WebP, AVIF with comparison
- **Compression**: Lossy vs lossless, quality settings
- **Resizing and Scaling**: Basic and advanced resizing
- **Responsive Images**: srcset, sizes, picture element
- **Lazy Loading**: Native and JavaScript-based
- **Image CDN**: Cloudinary and Imgix integration
- **Next.js Image Component**: Optimized images in Next.js
- **Sharp Library**: Node.js image processing
- **Pillow**: Python image processing
- **Automated Optimization**: Build-time and runtime optimization
- **Performance Metrics**: Calculating savings and Lighthouse audits
- **Best Practices**: Format selection, dimensions, progressive loading, metadata removal, caching
