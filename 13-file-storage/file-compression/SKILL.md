# File Compression

## Overview

File compression reduces file size by encoding data more efficiently. This skill covers various compression algorithms, implementation patterns, and best practices for both Node.js and Python.

## Table of Contents

1. [Compression Algorithms](#compression-algorithms)
2. [Implementation](#implementation)
3. [Archive Creation](#archive-creation)
4. [Streaming Compression](#streaming-compression)
5. [Decompression](#decompression)
6. [When to Compress](#when-to-compress)
7. [Performance Considerations](#performance-considerations)
8. [Storage Savings](#storage-savings)
9. [CDN Compression](#cdn-compression)
10. [Best Practices](#best-practices)

---

## Compression Algorithms

### Gzip

- **Compression Ratio**: Good (60-70%)
- **Speed**: Fast
- **Compatibility**: Universal
- **Use Case**: General-purpose compression

```typescript
// Gzip compression
import zlib from 'zlib';

const input = Buffer.from('Hello, World! This is a test string for compression.');
const compressed = zlib.gzipSync(input);

console.log(`Original size: ${input.length} bytes`);
console.log(`Compressed size: ${compressed.length} bytes`);
console.log(`Compression ratio: ${((1 - compressed.length / input.length) * 100).toFixed(1)}%`);
```

```python
# Gzip compression
import gzip
import io

input_data = b'Hello, World! This is a test string for compression.'

# Compress
compressed = gzip.compress(input_data)

print(f'Original size: {len(input_data)} bytes')
print(f'Compressed size: {len(compressed)} bytes')
print(f'Compression ratio: {(1 - len(compressed) / len(input_data)) * 100:.1f}%')
```

### Brotli

- **Compression Ratio**: Excellent (70-80%)
- **Speed**: Slower than gzip
- **Compatibility**: Modern browsers only
- **Use Case**: Web content where size matters most

```typescript
// Brotli compression
import zlib from 'zlib';

const input = Buffer.from('Hello, World! This is a test string for compression.');
const compressed = zlib.brotliCompressSync(input);

console.log(`Original size: ${input.length} bytes`);
console.log(`Compressed size: ${compressed.length} bytes`);
console.log(`Compression ratio: ${((1 - compressed.length / input.length) * 100).toFixed(1)}%`);
```

```python
# Brotli compression
import brotli

input_data = b'Hello, World! This is a test string for compression.'

# Compress
compressed = brotli.compress(input_data)

print(f'Original size: {len(input_data)} bytes')
print(f'Compressed size: {len(compressed)} bytes')
print(f'Compression ratio: {(1 - len(compressed) / len(input_data)) * 100:.1f}%')
```

### Zlib (DEFLATE)

- **Compression Ratio**: Good (similar to gzip)
- **Speed**: Fast
- **Compatibility**: Universal
- **Use Case**: When gzip header is not needed

```typescript
// Zlib compression
import zlib from 'zlib';

const input = Buffer.from('Hello, World! This is a test string for compression.');
const compressed = zlib.deflateSync(input);

console.log(`Original size: ${input.length} bytes`);
console.log(`Compressed size: ${compressed.length} bytes`);
console.log(`Compression ratio: ${((1 - compressed.length / input.length) * 100).toFixed(1)}%`);
```

```python
# Zlib compression
import zlib

input_data = b'Hello, World! This is a test string for compression.'

# Compress
compressed = zlib.compress(input_data)

print(f'Original size: {len(input_data)} bytes')
print(f'Compressed size: {len(compressed)} bytes')
print(f'Compression ratio: {(1 - len(compressed) / len(input_data)) * 100:.1f}%')
```

---

## Implementation

### Node.js (zlib)

#### Synchronous Compression

```typescript
// sync-compression.ts
import zlib from 'zlib';
import fs from 'fs';

// Compress a string
function compressString(input: string, algorithm: 'gzip' | 'deflate' | 'brotli' = 'gzip'): Buffer {
  const buffer = Buffer.from(input);

  switch (algorithm) {
    case 'gzip':
      return zlib.gzipSync(buffer);
    case 'deflate':
      return zlib.deflateSync(buffer);
    case 'brotli':
      return zlib.brotliCompressSync(buffer);
    default:
      throw new Error(`Unknown algorithm: ${algorithm}`);
  }
}

// Decompress a string
function decompressString(compressed: Buffer, algorithm: 'gzip' | 'deflate' | 'brotli' = 'gzip'): string {
  let decompressed: Buffer;

  switch (algorithm) {
    case 'gzip':
      decompressed = zlib.gunzipSync(compressed);
      break;
    case 'deflate':
      decompressed = zlib.inflateSync(compressed);
      break;
    case 'brotli':
      decompressed = zlib.brotliDecompressSync(compressed);
      break;
    default:
      throw new Error(`Unknown algorithm: ${algorithm}`);
  }

  return decompressed.toString();
}

// Compress a file
function compressFile(inputPath: string, outputPath: string, algorithm: 'gzip' | 'deflate' | 'brotli' = 'gzip'): void {
  const input = fs.readFileSync(inputPath);
  let compressed: Buffer;

  switch (algorithm) {
    case 'gzip':
      compressed = zlib.gzipSync(input);
      break;
    case 'deflate':
      compressed = zlib.deflateSync(input);
      break;
    case 'brotli':
      compressed = zlib.brotliCompressSync(input);
      break;
  }

  fs.writeFileSync(outputPath, compressed);
}

// Usage
const input = 'This is a long string that will compress well because it contains repeated patterns and common words that can be represented more efficiently.';

const compressed = compressString(input, 'gzip');
const decompressed = decompressString(compressed, 'gzip');

console.log('Original:', input);
console.log('Decompressed:', decompressed);
console.log('Match:', input === decompressed);
```

#### Asynchronous Compression

```typescript
// async-compression.ts
import zlib from 'zlib';
import { promisify } from 'util';

const gzip = promisify(zlib.gzip);
const gunzip = promisify(zlib.gunzip);
const deflate = promisify(zlib.deflate);
const inflate = promisify(zlib.inflate);
const brotliCompress = promisify(zlib.brotliCompress);
const brotliDecompress = promisify(zlib.brotliDecompress);

async function compressAsync(input: Buffer, algorithm: 'gzip' | 'deflate' | 'brotli' = 'gzip'): Promise<Buffer> {
  switch (algorithm) {
    case 'gzip':
      return gzip(input);
    case 'deflate':
      return deflate(input);
    case 'brotli':
      return brotliCompress(input);
    default:
      throw new Error(`Unknown algorithm: ${algorithm}`);
  }
}

async function decompressAsync(compressed: Buffer, algorithm: 'gzip' | 'deflate' | 'brotli' = 'gzip'): Promise<Buffer> {
  switch (algorithm) {
    case 'gzip':
      return gunzip(compressed);
    case 'deflate':
      return inflate(compressed);
    case 'brotli':
      return brotliDecompress(compressed);
    default:
      throw new Error(`Unknown algorithm: ${algorithm}`);
  }
}

// Usage
async function example() {
  const input = Buffer.from('This is a test string for async compression.');

  const compressed = await compressAsync(input, 'gzip');
  const decompressed = await decompressAsync(compressed, 'gzip');

  console.log('Original size:', input.length);
  console.log('Compressed size:', compressed.length);
  console.log('Decompressed matches:', decompressed.equals(input));
}

example();
```

#### Streaming Compression

```typescript
// streaming-compression.ts
import zlib from 'zlib';
import fs from 'fs';
import { pipeline } from 'stream/promises';

async function compressStream(inputPath: string, outputPath: string): Promise<void> {
  const readStream = fs.createReadStream(inputPath);
  const writeStream = fs.createWriteStream(outputPath);
  const gzip = zlib.createGzip();

  await pipeline(readStream, gzip, writeStream);
}

async function decompressStream(inputPath: string, outputPath: string): Promise<void> {
  const readStream = fs.createReadStream(inputPath);
  const writeStream = fs.createWriteStream(outputPath);
  const gunzip = zlib.createGunzip();

  await pipeline(readStream, gunzip, writeStream);
}

// Express middleware for compression
import express from 'express';

function compressionMiddleware(algorithm: 'gzip' | 'deflate' | 'brotli' = 'gzip') {
  return (req: express.Request, res: express.Response, next: express.NextFunction) => {
    const acceptEncoding = req.headers['accept-encoding'] || '';

    if (acceptEncoding.includes('br')) {
      res.setHeader('Content-Encoding', 'br');
      res.removeHeader('Content-Length');
      req.pipe(zlib.createBrotliCompress()).pipe(res);
    } else if (acceptEncoding.includes('gzip')) {
      res.setHeader('Content-Encoding', 'gzip');
      res.removeHeader('Content-Length');
      req.pipe(zlib.createGzip()).pipe(res);
    } else if (acceptEncoding.includes('deflate')) {
      res.setHeader('Content-Encoding', 'deflate');
      res.removeHeader('Content-Length');
      req.pipe(zlib.createDeflate()).pipe(res);
    } else {
      next();
    }
  };
}

// Usage
const app = express();

app.get('/api/data', compressionMiddleware('gzip'), (req, res) => {
  const data = { message: 'This data will be compressed' };
  res.json(data);
});
```

### Python (gzip, zipfile)

#### Gzip Compression

```python
# gzip_compression.py
import gzip
import io
from pathlib import Path

def compress_string(input_str: str, compression_level: int = 6) -> bytes:
    """Compress a string using gzip."""
    input_bytes = input_str.encode('utf-8')
    return gzip.compress(input_bytes, compresslevel=compression_level)

def decompress_string(compressed: bytes) -> str:
    """Decompress a gzip-compressed string."""
    decompressed = gzip.decompress(compressed)
    return decompressed.decode('utf-8')

def compress_file(input_path: Path, output_path: Path, compression_level: int = 6) -> None:
    """Compress a file using gzip."""
    with open(input_path, 'rb') as f_in:
        with gzip.open(output_path, 'wb', compresslevel=compression_level) as f_out:
            f_out.writelines(f_in)

def decompress_file(input_path: Path, output_path: Path) -> None:
    """Decompress a gzip-compressed file."""
    with gzip.open(input_path, 'rb') as f_in:
        with open(output_path, 'wb') as f_out:
            f_out.writelines(f_in)

# Streaming compression
def compress_stream(input_stream, output_stream, compression_level: int = 6) -> None:
    """Compress a stream using gzip."""
    with gzip.GzipFile(fileobj=output_stream, mode='wb', compresslevel=compression_level) as gzip_file:
        for chunk in input_stream:
            gzip_file.write(chunk)

# Usage
if __name__ == '__main__':
    input_text = 'This is a test string for compression.'
    
    # Compress
    compressed = compress_string(input_text)
    
    # Decompress
    decompressed = decompress_string(compressed)
    
    print(f'Original: {len(input_text)} bytes')
    print(f'Compressed: {len(compressed)} bytes')
    print(f'Compression ratio: {(1 - len(compressed) / len(input_text)) * 100:.1f}%')
    print(f'Match: {input_text == decompressed}')
```

#### Zipfile Compression

```python
# zipfile_compression.py
import zipfile
import io
from pathlib import Path
from typing import List, Optional

def create_zip(files: List[Path], output_path: Path, compression: int = zipfile.ZIP_DEFLATED) -> None:
    """Create a ZIP archive from multiple files."""
    with zipfile.ZipFile(output_path, 'w', compression=compression) as zipf:
        for file_path in files:
            if file_path.is_file():
                zipf.write(file_path, arcname=file_path.name)

def create_zip_from_memory(files: dict[str, bytes], output_path: Path) -> None:
    """Create a ZIP archive from in-memory data."""
    with zipfile.ZipFile(output_path, 'w') as zipf:
        for filename, content in files.items():
            zipf.writestr(filename, content)

def extract_zip(zip_path: Path, output_dir: Path) -> None:
    """Extract a ZIP archive."""
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        zipf.extractall(output_dir)

def list_zip_contents(zip_path: Path) -> List[str]:
    """List contents of a ZIP archive."""
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        return zipf.namelist()

def read_file_from_zip(zip_path: Path, filename: str) -> bytes:
    """Read a file from a ZIP archive."""
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        return zipf.read(filename)

def add_file_to_zip(zip_path: Path, file_path: Path, arcname: Optional[str] = None) -> None:
    """Add a file to an existing ZIP archive."""
    with zipfile.ZipFile(zip_path, 'a') as zipf:
        zipf.write(file_path, arcname=arcname or file_path.name)

# Usage
if __name__ == '__main__':
    # Create ZIP from files
    files = [Path('file1.txt'), Path('file2.txt')]
    create_zip(files, Path('archive.zip'))
    
    # List contents
    contents = list_zip_contents(Path('archive.zip'))
    print(f'Archive contents: {contents}')
    
    # Extract
    extract_zip(Path('archive.zip'), Path('extracted'))
    
    # Create ZIP from memory
    in_memory_files = {
        'file1.txt': b'Content of file 1',
        'file2.txt': b'Content of file 2',
    }
    create_zip_from_memory(in_memory_files, Path('memory.zip'))
```

---

## Archive Creation

### ZIP Archive (Node.js)

```typescript
// zip-archive.ts
import archiver from 'archiver';
import fs from 'fs';
import path from 'path';

async function createZipArchive(
  sourceDir: string,
  outputPath: string,
  options?: { rootDir?: string }
): Promise<void> {
  const output = fs.createWriteStream(outputPath);
  const archive = archiver('zip', {
    zlib: { level: 9 }, // Maximum compression
  });

  return new Promise((resolve, reject) => {
    output.on('close', () => {
      console.log(`${archive.pointer()} total bytes`);
      console.log('Archive has been finalized');
      resolve();
    });

    archive.on('error', (err) => {
      reject(err);
    });

    archive.pipe(output);

    if (options?.rootDir) {
      archive.directory(sourceDir, options.rootDir);
    } else {
      archive.directory(sourceDir, false);
    }

    archive.finalize();
  });
}

async function createZipFromFiles(
  files: Array<{ path: string; name: string }>,
  outputPath: string
): Promise<void> {
  const output = fs.createWriteStream(outputPath);
  const archive = archiver('zip', {
    zlib: { level: 9 },
  });

  return new Promise((resolve, reject) => {
    output.on('close', resolve);
    archive.on('error', reject);

    archive.pipe(output);

    for (const file of files) {
      archive.file(file.path, { name: file.name });
    }

    archive.finalize();
  });
}

// Usage
await createZipArchive('./dist', './dist.zip', { rootDir: 'project' });
```

### TAR Archive (Node.js)

```typescript
// tar-archive.ts
import tar from 'tar';
import fs from 'fs';
import path from 'path';

async function createTarArchive(
  sourceDir: string,
  outputPath: string,
  options?: { rootDir?: string }
): Promise<void> {
  const files = await fs.promises.readdir(sourceDir, { recursive: true });

  await tar.create(
    {
      gzip: true,
      file: outputPath,
      cwd: options?.rootDir || sourceDir,
    },
    files.map((file) => path.relative(sourceDir, path.join(sourceDir, file as string)))
  );
}

async function extractTarArchive(
  archivePath: string,
  outputDir: string
): Promise<void> {
  await tar.extract({
    file: archivePath,
    cwd: outputDir,
  });
}

// Usage
await createTarArchive('./dist', './dist.tar.gz');
```

### TAR Archive (Python)

```python
# tar_archive.py
import tarfile
from pathlib import Path
from typing import Optional

def create_tar_archive(
    source_dir: Path,
    output_path: Path,
    compression: str = 'gz',
    arcname: Optional[str] = None
) -> None:
    """Create a TAR archive from a directory."""
    mode = f'w:{compression}'
    with tarfile.open(output_path, mode) as tar:
        tar.add(source_dir, arcname=arcname or source_dir.name)

def create_tar_from_files(
    files: list[tuple[Path, str]],
    output_path: Path,
    compression: str = 'gz'
) -> None:
    """Create a TAR archive from multiple files."""
    mode = f'w:{compression}'
    with tarfile.open(output_path, mode) as tar:
        for file_path, arcname in files:
            tar.add(file_path, arcname=arcname)

def extract_tar_archive(
    archive_path: Path,
    output_dir: Path
) -> None:
    """Extract a TAR archive."""
    with tarfile.open(archive_path, 'r:*') as tar:
        tar.extractall(output_dir)

def list_tar_contents(archive_path: Path) -> list[str]:
    """List contents of a TAR archive."""
    with tarfile.open(archive_path, 'r:*') as tar:
        return tar.getnames()

# Usage
if __name__ == '__main__':
    # Create TAR archive
    create_tar_archive(
        Path('./dist'),
        Path('./dist.tar.gz'),
        compression='gz'
    )
    
    # List contents
    contents = list_tar_contents(Path('./dist.tar.gz'))
    print(f'Archive contents: {contents}')
    
    # Extract
    extract_tar_archive(Path('./dist.tar.gz'), Path('./extracted'))
```

---

## Streaming Compression

### Node.js Streaming

```typescript
// streaming-compression-advanced.ts
import zlib from 'zlib';
import { Transform, pipeline } from 'stream';

class CompressionStream extends Transform {
  private compressor: zlib.Gzip | zlib.Deflate | zlib.BrotliCompress;

  constructor(algorithm: 'gzip' | 'deflate' | 'brotli' = 'gzip', level: number = 6) {
    super();

    switch (algorithm) {
      case 'gzip':
        this.compressor = zlib.createGzip({ level });
        break;
      case 'deflate':
        this.compressor = zlib.createDeflate({ level });
        break;
      case 'brotli':
        this.compressor = zlib.createBrotliCompress({ params: { [zlib.constants.BROTLI_PARAM_QUALITY]: level } });
        break;
    }

    this.compressor.on('data', (chunk) => this.push(chunk));
    this.compressor.on('end', () => this.push(null));
  }

  _transform(chunk: Buffer, encoding: BufferEncoding, callback: () => void): void {
    this.compressor.write(chunk);
    callback();
  }

  _flush(callback: () => void): void {
    this.compressor.end();
    callback();
  }
}

// Usage with HTTP
import http from 'http';

const server = http.createServer((req, res) => {
  const acceptEncoding = req.headers['accept-encoding'] || '';

  if (acceptEncoding.includes('br')) {
    res.writeHead(200, { 'Content-Encoding': 'br' });
    const stream = new CompressionStream('brotli', 4);
    req.pipe(stream).pipe(res);
  } else if (acceptEncoding.includes('gzip')) {
    res.writeHead(200, { 'Content-Encoding': 'gzip' });
    const stream = new CompressionStream('gzip', 6);
    req.pipe(stream).pipe(res);
  } else {
    res.writeHead(200);
    req.pipe(res);
  }
});

server.listen(3000);
```

### Python Streaming

```python
# streaming_compression.py
import gzip
import io
from typing import Iterator, Optional

class StreamingCompressor:
    """Streaming compression for large data."""
    
    def __init__(self, compression_level: int = 6):
        self.buffer = io.BytesIO()
        self.compressor = gzip.GzipFile(
            fileobj=self.buffer,
            mode='wb',
            compresslevel=compression_level
        )
    
    def compress(self, data: bytes) -> bytes:
        """Compress a chunk of data."""
        self.compressor.write(data)
        self.compressor.flush()
        result = self.buffer.getvalue()
        self.buffer.seek(0)
        self.buffer.truncate(0)
        return result
    
    def finalize(self) -> bytes:
        """Finalize compression and return remaining data."""
        self.compressor.close()
        return self.buffer.getvalue()

def compress_streaming(
    data_iterator: Iterator[bytes],
    chunk_size: int = 8192,
    compression_level: int = 6
) -> Iterator[bytes]:
    """Compress data from an iterator."""
    compressor = StreamingCompressor(compression_level)
    
    for chunk in data_iterator:
        yield compressor.compress(chunk)
    
    yield compressor.finalize()

# Usage
def data_generator():
    """Generate large data in chunks."""
    for i in range(100):
        yield b'Large data chunk ' * 1000

compressed_chunks = list(compress_streaming(data_generator()))
total_compressed = sum(len(chunk) for chunk in compressed_chunks)
print(f'Total compressed size: {total_compressed} bytes')
```

---

## Decompression

### Node.js Decompression

```typescript
// decompression.ts
import zlib from 'zlib';
import fs from 'fs';

function decompressBuffer(compressed: Buffer, algorithm: 'gzip' | 'deflate' | 'brotli' = 'gzip'): Buffer {
  switch (algorithm) {
    case 'gzip':
      return zlib.gunzipSync(compressed);
    case 'deflate':
      return zlib.inflateSync(compressed);
    case 'brotli':
      return zlib.brotliDecompressSync(compressed);
    default:
      throw new Error(`Unknown algorithm: ${algorithm}`);
  }
}

async function decompressFile(inputPath: string, outputPath: string): Promise<void> {
  const compressed = await fs.promises.readFile(inputPath);
  const decompressed = zlib.gunzipSync(compressed);
  await fs.promises.writeFile(outputPath, decompressed);
}

// Detect compression type
function detectCompressionType(buffer: Buffer): 'gzip' | 'deflate' | 'brotli' | 'unknown' {
  // Gzip magic number: 0x1f 0x8b
  if (buffer[0] === 0x1f && buffer[1] === 0x8b) {
    return 'gzip';
  }

  // Brotli magic number: varies, but typically starts with specific patterns
  // This is a simplified check
  if (buffer.length > 2 && buffer[0] === 0x1f && buffer[1] === 0x8b) {
    return 'brotli';
  }

  // Deflate doesn't have a magic number, assume it's deflate if not gzip
  return 'deflate';
}

// Auto-detect and decompress
function autoDecompress(buffer: Buffer): Buffer {
  const type = detectCompressionType(buffer);
  return decompressBuffer(buffer, type);
}
```

### Python Decompression

```python
# decompression.py
import gzip
import zlib
import brotli
from pathlib import Path

def decompress_buffer(compressed: bytes, algorithm: str = 'gzip') -> bytes:
    """Decompress a buffer."""
    if algorithm == 'gzip':
        return gzip.decompress(compressed)
    elif algorithm == 'deflate':
        return zlib.decompress(compressed)
    elif algorithm == 'brotli':
        return brotli.decompress(compressed)
    else:
        raise ValueError(f'Unknown algorithm: {algorithm}')

def decompress_file(input_path: Path, output_path: Path) -> None:
    """Decompress a file."""
    with open(input_path, 'rb') as f_in:
        compressed = f_in.read()
    
    decompressed = gzip.decompress(compressed)
    
    with open(output_path, 'wb') as f_out:
        f_out.write(decompressed)

def detect_compression_type(buffer: bytes) -> str:
    """Detect compression type from buffer."""
    # Gzip magic number: 0x1f 0x8b
    if len(buffer) >= 2 and buffer[0] == 0x1f and buffer[1] == 0x8b:
        return 'gzip'
    
    # Brotli detection (simplified)
    if len(buffer) >= 4:
        # Try to decompress as brotli
        try:
            brotli.decompress(buffer[:100])
            return 'brotli'
        except:
            pass
    
    # Default to deflate
    return 'deflate'

def auto_decompress(buffer: bytes) -> bytes:
    """Auto-detect and decompress."""
    algorithm = detect_compression_type(buffer)
    return decompress_buffer(buffer, algorithm)
```

---

## When to Compress

### Files That Compress Well

- **Text files**: HTML, CSS, JavaScript, JSON, XML
- **Log files**: Server logs, application logs
- **Source code**: Any programming language source files
- **Documents**: Plain text, Markdown, CSV
- **Configuration files**: INI, YAML, TOML

### Files That Don't Compress Well

- **Already compressed**: ZIP, GZIP, MP3, MP4, PNG, JPG
- **Binary executables**: EXE, DLL, SO files
- **Encrypted data**: Already randomized
- **Random data**: No patterns to compress

### Decision Tree

```typescript
// compression-decision.ts
interface CompressionDecision {
  shouldCompress: boolean;
  algorithm: 'gzip' | 'brotli' | 'none';
  reason: string;
}

function shouldCompressFile(
  filePath: string,
  contentType?: string
): CompressionDecision {
  const ext = filePath.split('.').pop()?.toLowerCase();

  // Don't compress already compressed formats
  const noCompressExtensions = [
    'zip', 'gz', 'bz2', '7z', 'rar',
    'mp3', 'mp4', 'avi', 'mkv',
    'jpg', 'jpeg', 'png', 'gif', 'webp',
    'exe', 'dll', 'so', 'dylib',
  ];

  if (ext && noCompressExtensions.includes(ext)) {
    return {
      shouldCompress: false,
      algorithm: 'none',
      reason: 'File is already compressed',
    };
  }

  // Compress text-based files
  const textExtensions = [
    'html', 'css', 'js', 'json', 'xml',
    'txt', 'md', 'csv', 'log',
    'yaml', 'yml', 'toml', 'ini',
  ];

  if (ext && textExtensions.includes(ext)) {
    return {
      shouldCompress: true,
      algorithm: 'brotli',
      reason: 'Text-based file, compresses well',
    };
  }

  // Check content type
  if (contentType) {
    if (contentType.startsWith('text/')) {
      return {
        shouldCompress: true,
        algorithm: 'brotli',
        reason: 'Text content type',
      };
    }

    if (contentType.includes('json') || contentType.includes('xml')) {
      return {
        shouldCompress: true,
        algorithm: 'brotli',
        reason: 'Structured data',
      };
    }
  }

  // Default: don't compress
  return {
    shouldCompress: false,
    algorithm: 'none',
    reason: 'Unknown file type',
  };
}
```

---

## Performance Considerations

### Compression Level Trade-offs

```typescript
// compression-levels.ts
import zlib from 'zlib';

interface CompressionBenchmark {
  level: number;
  originalSize: number;
  compressedSize: number;
  ratio: number;
  time: number;
  speed: number;
}

function benchmarkCompressionLevels(data: Buffer): CompressionBenchmark[] {
  const results: CompressionBenchmark[] = [];

  for (let level = 1; level <= 9; level++) {
    const start = Date.now();
    const compressed = zlib.gzipSync(data, { level });
    const time = Date.now() - start;

    results.push({
      level,
      originalSize: data.length,
      compressedSize: compressed.length,
      ratio: compressed.length / data.length,
      time,
      speed: data.length / (time / 1000),
    });
  }

  return results;
}

// Typical results:
// Level 1: Fastest, ~60% of original size
// Level 6: Balanced, ~50% of original size (default)
// Level 9: Slowest, ~45% of original size
```

```python
# compression_levels.py
import gzip
import time
from dataclasses import dataclass
from typing import List

@dataclass
class CompressionBenchmark:
    level: int
    original_size: int
    compressed_size: int
    ratio: float
    time: float
    speed: float

def benchmark_compression_levels(data: bytes) -> List[CompressionBenchmark]:
    """Benchmark different compression levels."""
    results = []
    
    for level in range(1, 10):
        start = time.time()
        compressed = gzip.compress(data, compresslevel=level)
        elapsed = time.time() - start
        
        results.append(CompressionBenchmark(
            level=level,
            original_size=len(data),
            compressed_size=len(compressed),
            ratio=len(compressed) / len(data),
            time=elapsed,
            speed=len(data) / elapsed
        ))
    
    return results
```

### Memory Usage

```typescript
// memory-usage.ts
import zlib from 'zlib';

function compressWithMemoryLimit(
  data: Buffer,
  maxMemoryMB: number = 100
): Buffer {
  const maxMemory = maxMemoryMB * 1024 * 1024;

  if (data.length > maxMemory) {
    // Use streaming compression for large files
    throw new Error('File too large, use streaming compression');
  }

  return zlib.gzipSync(data);
}

// Streaming compression for large files
async function compressLargeFile(
  inputPath: string,
  outputPath: string,
  chunkSize: number = 1024 * 1024 // 1MB chunks
): Promise<void> {
  const readStream = fs.createReadStream(inputPath, { highWaterMark: chunkSize });
  const writeStream = fs.createWriteStream(outputPath);
  const gzip = zlib.createGzip({ chunkSize });

  await pipeline(readStream, gzip, writeStream);
}
```

---

## Storage Savings

### Calculate Savings

```typescript
// storage-savings.ts
interface StorageReport {
  originalSize: number;
  compressedSize: number;
  savedBytes: number;
  savedPercentage: number;
  savedMB: number;
  savedGB: number;
}

function calculateStorageSavings(
  originalSize: number,
  compressedSize: number
): StorageReport {
  const savedBytes = originalSize - compressedSize;
  const savedPercentage = (savedBytes / originalSize) * 100;
  const savedMB = savedBytes / (1024 * 1024);
  const savedGB = savedMB / 1024;

  return {
    originalSize,
    compressedSize,
    savedBytes,
    savedPercentage,
    savedMB,
    savedGB,
  };
}

// Example: Calculate savings for a website
const report = calculateStorageSavings(
  100 * 1024 * 1024, // 100MB original
  30 * 1024 * 1024    // 30MB compressed
);

console.log(`Original: ${(report.originalSize / 1024 / 1024).toFixed(2)} MB`);
console.log(`Compressed: ${(report.compressedSize / 1024 / 1024).toFixed(2)} MB`);
console.log(`Saved: ${report.savedMB.toFixed(2)} MB (${report.savedPercentage.toFixed(1)}%)`);
```

---

## CDN Compression

### CloudFront Compression

```typescript
// cloudfront-compression.ts
// CloudFront automatically compresses files with these extensions:
// .html, .css, .js, .json, .xml, .txt, .svg, .ttf, .otf, .woff, .woff2

// Enable compression via CloudFormation
const cloudfrontDistribution = {
  Type: 'AWS::CloudFront::Distribution',
  Properties: {
    DistributionConfig: {
      DefaultCacheBehavior: {
        Compress: true, // Enable compression
        TargetOriginId: 'myOrigin',
        ViewerProtocolPolicy: 'redirect-to-https',
        ForwardedValues: {
          QueryString: false,
          Cookies: { Forward: 'none' },
        },
      },
      // ...
    },
  },
};
```

### Cloudflare Compression

```typescript
// Cloudflare automatically compresses text-based content
// No configuration needed

// To disable compression for specific files:
// Add header: Cache-Control: no-transform
```

### NGINX Compression

```nginx
# nginx.conf
http {
    # Enable gzip compression
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript
               application/json application/javascript application/xml+rss
               application/rss+xml font/truetype font/opentype
               application/vnd.ms-fontobject image/svg+xml;

    # Enable Brotli compression (requires ngx_brotli module)
    brotli on;
    brotli_comp_level 6;
    brotli_types text/plain text/css text/xml text/javascript
                 application/json application/javascript application/xml+rss
                 application/rss+xml font/truetype font/opentype
                 application/vnd.ms-fontobject image/svg+xml;
}
```

---

## Best Practices

### 1. Use Appropriate Compression Levels

```typescript
// best-practices.ts

// For real-time API responses: Use level 1-3 (fast)
function compressApiResponse(data: any): Buffer {
  return zlib.gzipSync(JSON.stringify(data), { level: 3 });
}

// For static assets: Use level 6-9 (better compression)
function compressStaticAsset(content: Buffer): Buffer {
  return zlib.gzipSync(content, { level: 9 });
}
```

### 2. Pre-compress Static Assets

```typescript
// pre-compress.ts
import fs from 'fs';
import path from 'path';

async function preCompressAssets(dir: string): Promise<void> {
  const files = await fs.promises.readdir(dir, { recursive: true });

  for (const file of files) {
    const filePath = path.join(dir, file as string);
    const stat = await fs.promises.stat(filePath);

    if (stat.isFile()) {
      const content = await fs.promises.readFile(filePath);
      const compressed = zlib.gzipSync(content, { level: 9 });

      const gzPath = `${filePath}.gz`;
      await fs.promises.writeFile(gzPath, compressed);

      console.log(`Compressed: ${file}`);
    }
  }
}
```

### 3. Use Brotli for Modern Browsers

```typescript
// brotli-fallback.ts

function getBestCompressionAlgorithm(acceptEncoding: string): 'brotli' | 'gzip' | 'none' {
  if (acceptEncoding.includes('br')) {
    return 'brotli';
  }
  if (acceptEncoding.includes('gzip')) {
    return 'gzip';
  }
  return 'none';
}
```

### 4. Cache Compressed Responses

```typescript
// cache-compressed.ts

function setCompressionHeaders(res: any, algorithm: 'gzip' | 'brotli'): void {
  res.setHeader('Content-Encoding', algorithm);
  res.setHeader('Vary', 'Accept-Encoding');
  res.setHeader('Cache-Control', 'public, max-age=31536000, immutable');
}
```

### 5. Monitor Compression Ratios

```typescript
// monitor-compression.ts

class CompressionMonitor {
  private stats: Map<string, { original: number; compressed: number }> = new Map();

  record(fileType: string, originalSize: number, compressedSize: number): void {
    const existing = this.stats.get(fileType) || { original: 0, compressed: 0 };
    this.stats.set(fileType, {
      original: existing.original + originalSize,
      compressed: existing.compressed + compressedSize,
    });
  }

  getReport(): Record<string, { ratio: number; savings: number }> {
    const report: Record<string, { ratio: number; savings: number }> = {};

    for (const [type, data] of this.stats) {
      report[type] = {
        ratio: data.compressed / data.original,
        savings: data.original - data.compressed,
      };
    }

    return report;
  }
}
```

---

## Summary

This skill covers comprehensive file compression techniques including:

- **Compression Algorithms**: Gzip, Brotli, and Zlib (DEFLATE)
- **Implementation**: Node.js (zlib) and Python (gzip, zipfile)
- **Archive Creation**: ZIP and TAR archives
- **Streaming Compression**: Handling large files efficiently
- **Decompression**: Auto-detection and decompression
- **When to Compress**: Decision tree for file types
- **Performance Considerations**: Compression levels and memory usage
- **Storage Savings**: Calculating compression benefits
- **CDN Compression**: CloudFront, Cloudflare, and NGINX
- **Best Practices**: Compression levels, pre-compression, algorithm selection, caching, and monitoring
