---
name: PDF Processing
description: Comprehensive guide to PDF processing, manipulation, and extraction using Python libraries
---

# PDF Processing

## Overview

Comprehensive guide to PDF processing, manipulation, and extraction using Python libraries.

## Prerequisites

- **Python 3.7+**: Required for most PDF processing libraries
- **PyPDF2**: For basic PDF reading, merging, and manipulation
- **pdfplumber**: For better text extraction and table extraction
- **PyMuPDF (fitz)**: For fast PDF processing and image extraction
- **ReportLab**: For creating PDFs programmatically
- **WeasyPrint**: For HTML to PDF conversion
- **pdf2image**: For PDF to image conversion
- **Camelot**: For advanced table extraction

## Key Concepts

- **PDF Structure**: Understanding of PDF objects, pages, and streams
- **Text Extraction**: Methods for extracting text with layout preservation
- **Image Extraction**: Extracting embedded images from PDFs
- **Table Extraction**: Identifying and extracting tabular data
- **PDF Manipulation**: Merging, splitting, rotating, and watermarking
- **Form Filling**: Populating PDF form fields programmatically
- **PDF to Image**: Converting PDF pages to raster images
- **Batch Processing**: Efficient processing of multiple PDF files

## Table of Contents

1. [Reading PDFs](#reading-pdfs)
2. [Extracting Content](#extracting-content)
3. [Creating PDFs](#creating-pdfs)
4. [Manipulating PDFs](#manipulating-pdfs)
5. [Form Filling](#form-filling)
6. [PDF to Image Conversion](#pdf-to-image-conversion)
7. [Batch Processing](#batch-processing)
8. [Performance Optimization](#performance-optimization)
9. [Common Issues and Solutions](#common-issues-and-solutions)

---

## Reading PDFs

### PyPDF2

```python
import PyPDF2

def read_pdf_basic(pdf_path: str) -> str:
    """Read PDF using PyPDF2"""
    text = ""
    
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        for page in reader.pages:
            text += page.extract_text() + "\n"
    
    return text

def get_pdf_info(pdf_path: str) -> dict:
    """Get PDF information"""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        return {
            'num_pages': len(reader.pages),
            'is_encrypted': reader.is_encrypted,
            'metadata': reader.metadata,
            'page_sizes': [(page.mediabox.width, page.mediabox.height) for page in reader.pages]
        }

def read_specific_page(pdf_path: str, page_num: int) -> str:
    """Read specific page (0-indexed)"""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        page = reader.pages[page_num]
        return page.extract_text()
```

### pdfplumber

```python
import pdfplumber

def read_pdf_pdfplumber(pdf_path: str) -> str:
    """Read PDF using pdfplumber (better text extraction)"""
    text = ""
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    
    return text

def read_with_layout(pdf_path: str) -> list:
    """Read with layout preservation"""
    with pdfplumber.open(pdf_path) as pdf:
        pages = []
        
        for page in pdf.pages:
            pages.append({
                'text': page.extract_text(),
                'width': page.width,
                'height': page.height,
                'chars': page.chars,
                'words': page.words,
                'lines': page.lines
            })
    
    return pages

def extract_with_crops(pdf_path: str, crop_box: tuple) -> str:
    """Extract text from cropped region"""
    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[0]
        
        # Crop: (left, top, right, bottom)
        cropped = first_page.crop(crop_box)
        return cropped.extract_text()
```

### PyMuPDF (fitz)

```python
import fitz  # PyMuPDF

def read_pdf_fitz(pdf_path: str) -> str:
    """Read PDF using PyMuPDF (fastest)"""
    doc = fitz.open(pdf_path)
    text = ""
    
    for page in doc:
        text += page.get_text()
    
    doc.close()
    return text

def read_with_blocks(pdf_path: str) -> list:
    """Read text blocks with positions"""
    doc = fitz.open(pdf_path)
    blocks = []
    
    for page in doc:
        text_blocks = page.get_text("blocks")
        for block in text_blocks:
            blocks.append({
                'text': block[4],
                'bbox': block[:4],
                'type': block[5]
            })
    
    doc.close()
    return blocks

def read_with_words(pdf_path: str) -> list:
    """Read words with positions"""
    doc = fitz.open(pdf_path)
    words = []
    
    for page in doc:
        page_words = page.get_text("words")
        for word in page_words:
            words.append({
                'text': word[4],
                'bbox': word[:4],
                'block_no': word[5],
                'line_no': word[6],
                'span_no': word[7]
            })
    
    doc.close()
    return words
```

---

## Extracting Content

### Text Extraction

```python
import pdfplumber
import fitz

def extract_text_with_formatting(pdf_path: str) -> list:
    """Extract text with formatting info"""
    doc = fitz.open(pdf_path)
    formatted_text = []
    
    for page in doc:
        # Get text with font info
        text_dict = page.get_text("dict")
        
        for block in text_dict["blocks"]:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        formatted_text.append({
                            'text': span["text"],
                            'font': span["font"],
                            'size': span["size"],
                            'color': span["color"],
                            'flags': span["flags"]
                        })
    
    doc.close()
    return formatted_text

def extract_text_by_region(pdf_path: str, regions: dict) -> dict:
    """Extract text from specific regions"""
    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[0]
        results = {}
        
        for region_name, crop_box in regions.items():
            cropped = first_page.crop(crop_box)
            results[region_name] = cropped.extract_text()
        
        return results

# Example regions
REGIONS = {
    'header': (0, 0, 600, 100),
    'body': (0, 100, 600, 700),
    'footer': (0, 700, 600, 800)
}
```

### Image Extraction

```python
import fitz
import io
from PIL import Image

def extract_images(pdf_path: str, output_dir: str = 'extracted_images'):
    """Extract all images from PDF"""
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    doc = fitz.open(pdf_path)
    image_count = 0
    
    for page_index, page in enumerate(doc):
        image_list = page.get_images()
        
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_data = base_image["image"]
            
            # Save image
            image = Image.open(io.BytesIO(image_data))
            image_path = os.path.join(output_dir, f'page_{page_index}_img_{img_index}.png')
            image.save(image_path)
            image_count += 1
    
    doc.close()
    return image_count

def extract_image_metadata(pdf_path: str) -> list:
    """Extract image metadata"""
    doc = fitz.open(pdf_path)
    metadata = []
    
    for page_index, page in enumerate(doc):
        image_list = page.get_images()
        
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            
            metadata.append({
                'page': page_index,
                'index': img_index,
                'xref': xref,
                'ext': base_image["ext"],
                'width': base_image["width"],
                'height': base_image["height"],
                'colorspace': base_image["colorspace"],
                'bpc': base_image["bpc"]
            })
    
    doc.close()
    return metadata
```

### Table Extraction

```python
import pdfplumber
import camelot

def extract_tables_pdfplumber(pdf_path: str) -> list:
    """Extract tables using pdfplumber"""
    tables = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            page_tables = page.extract_tables()
            if page_tables:
                for table in page_tables:
                    tables.append({
                        'page': page_num,
                        'data': table
                    })
    
    return tables

def extract_tables_camelot(pdf_path: str) -> list:
    """Extract tables using Camelot"""
    tables = camelot.read_pdf(pdf_path, pages='all')
    
    result = []
    for i, table in enumerate(tables):
        result.append({
            'index': i,
            'page': table.page,
            'data': table.df.to_dict('records'),
            'accuracy': table.accuracy,
            'whitespace': table.whitespace,
            'order': table.order
        })
    
    return result

def extract_tables_with_settings(pdf_path: str) -> list:
    """Extract tables with custom settings"""
    tables = camelot.read_pdf(
        pdf_path,
        pages='all',
        flavor='lattice',  # or 'stream'
        line_scale=40,
        shift_text=[''],
        copy_text=['h'],
        layout=True
    )
    
    return [table.df for table in tables]
```

### Metadata Extraction

```python
import PyPDF2
import fitz

def extract_metadata_pypdf2(pdf_path: str) -> dict:
    """Extract metadata using PyPDF2"""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        metadata = reader.metadata
    
    return {
        'title': metadata.get('/Title'),
        'author': metadata.get('/Author'),
        'subject': metadata.get('/Subject'),
        'creator': metadata.get('/Creator'),
        'producer': metadata.get('/Producer'),
        'creation_date': metadata.get('/CreationDate'),
        'modification_date': metadata.get('/ModDate'),
        'keywords': metadata.get('/Keywords')
    }

def extract_metadata_fitz(pdf_path: str) -> dict:
    """Extract metadata using PyMuPDF"""
    doc = fitz.open(pdf_path)
    metadata = doc.metadata
    
    doc.close()
    return metadata

def get_pdf_stats(pdf_path: str) -> dict:
    """Get PDF statistics"""
    doc = fitz.open(pdf_path)
    
    stats = {
        'num_pages': doc.page_count,
        'metadata': doc.metadata,
        'page_sizes': [],
        'total_words': 0,
        'total_chars': 0
    }
    
    for page in doc:
        stats['page_sizes'].append((page.rect.width, page.rect.height))
        text = page.get_text()
        stats['total_words'] += len(text.split())
        stats['total_chars'] += len(text)
    
    doc.close()
    return stats
```

---

## Creating PDFs

### ReportLab

```python
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, Image
from reportlab.lib.units import inch
from reportlab.lib import colors

def create_simple_pdf(output_path: str, text: str):
    """Create simple PDF"""
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Add title
    title = Paragraph("Document Title", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))
    
    # Add content
    content = Paragraph(text, styles['Normal'])
    story.append(content)
    
    doc.build(story)

def create_pdf_with_table(output_path: str, data: list):
    """Create PDF with table"""
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    story = []
    
    # Create table
    table = Table(data)
    table.setStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    
    story.append(table)
    doc.build(story)

def create_pdf_with_image(output_path: str, image_path: str, text: str):
    """Create PDF with image"""
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Add image
    img = Image(image_path, width=4*inch, height=3*inch)
    story.append(img)
    story.append(Spacer(1, 12))
    
    # Add text
    content = Paragraph(text, styles['Normal'])
    story.append(content)
    
    doc.build(story)
```

### WeasyPrint

```python
from weasyprint import HTML

def create_pdf_from_html(output_path: str, html_content: str):
    """Create PDF from HTML"""
    HTML(string=html_content).write_pdf(output_path)

def create_pdf_from_template(output_path: str, template_path: str, context: dict):
    """Create PDF from HTML template"""
    from jinja2 import Template
    
    # Load template
    with open(template_path, 'r') as f:
        template = Template(f.read())
    
    # Render template
    html_content = template.render(**context)
    
    # Create PDF
    HTML(string=html_content).write_pdf(output_path)

# Example HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; }
        .header { background: #f0f0f0; padding: 20px; }
        .content { padding: 20px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <div class="header">
        <h1>{{ title }}</h1>
        <p>Date: {{ date }}</p>
    </div>
    <div class="content">
        {{ content }}
    </div>
</body>
</html>
"""
```

---

## Manipulating PDFs

### Merge PDFs

```python
import PyPDF2

def merge_pdfs(output_path: str, pdf_paths: list):
    """Merge multiple PDFs"""
    merger = PyPDF2.PdfMerger()
    
    for pdf_path in pdf_paths:
        merger.append(pdf_path)
    
    merger.write(output_path)
    merger.close()

def merge_with_bookmarks(output_path: str, pdf_paths: list, bookmark_names: list):
    """Merge PDFs with bookmarks"""
    merger = PyPDF2.PdfMerger()
    
    for pdf_path, bookmark_name in zip(pdf_paths, bookmark_names):
        merger.append(pdf_path, bookmark_name)
    
    merger.write(output_path)
    merger.close()
```

### Split PDFs

```python
import PyPDF2

def split_pdf_by_pages(input_path: str, output_dir: str, pages_per_file: int = 1):
    """Split PDF into multiple files"""
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    with open(input_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        total_pages = len(reader.pages)
        
        for i in range(0, total_pages, pages_per_file):
            writer = PyPDF2.PdfWriter()
            
            for j in range(i, min(i + pages_per_file, total_pages)):
                writer.add_page(reader.pages[j])
            
            output_path = os.path.join(output_dir, f'part_{i//pages_per_file + 1}.pdf')
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)

def extract_pages(input_path: str, output_path: str, page_numbers: list):
    """Extract specific pages"""
    with open(input_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()
        
        for page_num in page_numbers:
            if 0 <= page_num < len(reader.pages):
                writer.add_page(reader.pages[page_num])
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
```

### Rotate PDFs

```python
import PyPDF2

def rotate_pdf(input_path: str, output_path: str, angle: int = 90):
    """Rotate all pages"""
    with open(input_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()
        
        for page in reader.pages:
            rotated_page = page.rotate(angle)
            writer.add_page(rotated_page)
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)

def rotate_specific_pages(input_path: str, output_path: str, page_angles: dict):
    """Rotate specific pages"""
    with open(input_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()
        
        for i, page in enumerate(reader.pages):
            if i in page_angles:
                rotated_page = page.rotate(page_angles[i])
                writer.add_page(rotated_page)
            else:
                writer.add_page(page)
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
```

### Add Watermarks

```python
import PyPDF2

def add_watermark(input_path: str, watermark_path: str, output_path: str):
    """Add watermark to all pages"""
    with open(watermark_path, 'rb') as watermark_file:
        watermark_reader = PyPDF2.PdfReader(watermark_file)
        watermark_page = watermark_reader.pages[0]
    
    with open(input_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()
        
        for page in reader.pages:
            page.merge_page(watermark_page)
            writer.add_page(page)
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)

def add_text_watermark(input_path: str, output_path: str, text: str):
    """Add text watermark using ReportLab"""
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    import io
    
    # Create watermark PDF
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Helvetica", 50)
    can.setFillColorRGB(0.8, 0.8, 0.8, alpha=0.3)
    can.rotate(45)
    can.drawString(100, 100, text)
    can.save()
    
    # Merge watermark
    packet.seek(0)
    watermark = PyPDF2.PdfReader(packet)
    watermark_page = watermark.pages[0]
    
    with open(input_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()
        
        for page in reader.pages:
            page.merge_page(watermark_page)
            writer.add_page(page)
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
```

### Add Annotations

```python
import PyPDF2

def add_text_annotation(input_path: str, output_path: str, annotations: list):
    """Add text annotations to PDF"""
    with open(input_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()
        
        for i, page in enumerate(reader.pages):
            for annotation in annotations:
                if annotation['page'] == i:
                    page.add_annotation(
                        PyPDF2.generic.RectangleObject([
                            annotation['x'],
                            annotation['y'],
                            annotation['x'] + annotation['width'],
                            annotation['y'] + annotation['height']
                        ]),
                        PyPDF2.generic.TextStringObject(annotation['text'])
                    )
            writer.add_page(page)
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
```

---

## Form Filling

### Fill PDF Forms

```python
import PyPDF2

def fill_pdf_form(input_path: str, output_path: str, form_data: dict):
    """Fill PDF form fields"""
    with open(input_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()
        
        for page in reader.pages:
            writer.add_page(page)
        
        # Get form fields
        if '/AcroForm' in reader.trailer['/Root']:
            fields = reader.get_fields()
            
            for field_name, value in form_data.items():
                if field_name in fields:
                    writer.update_page_form_field_values(
                        writer.pages[0],
                        {field_name: value}
                    )
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)

def get_form_fields(pdf_path: str) -> dict:
    """Get all form fields from PDF"""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        fields = reader.get_fields()
    
    result = {}
    for field_name, field in fields.items():
        result[field_name] = {
            'type': field.get('/FT'),
            'value': field.get('/V'),
            'default': field.get('/DV')
        }
    
    return result
```

---

## PDF to Image Conversion

### Using pdf2image

```python
from pdf2image import convert_from_path

def pdf_to_images(pdf_path: str, output_dir: str = 'output_images', dpi: int = 300):
    """Convert PDF to images"""
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    # Convert PDF to images
    images = convert_from_path(pdf_path, dpi=dpi)
    
    # Save images
    image_paths = []
    for i, image in enumerate(images):
        image_path = os.path.join(output_dir, f'page_{i+1}.png')
        image.save(image_path, 'PNG')
        image_paths.append(image_path)
    
    return image_paths

def convert_specific_pages(pdf_path: str, page_numbers: list, output_dir: str = 'output_images'):
    """Convert specific pages to images"""
    images = convert_from_path(
        pdf_path,
        first_page=min(page_numbers) + 1,
        last_page=max(page_numbers) + 1
    )
    
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    result = {}
    for i, page_num in enumerate(page_numbers):
        if i < len(images):
            image_path = os.path.join(output_dir, f'page_{page_num+1}.png')
            images[i].save(image_path, 'PNG')
            result[page_num] = image_path
    
    return result
```

### Using PyMuPDF

```python
import fitz

def pdf_to_images_fitz(pdf_path: str, output_dir: str = 'output_images', zoom: int = 2):
    """Convert PDF to images using PyMuPDF"""
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    doc = fitz.open(pdf_path)
    image_paths = []
    
    for page_num, page in enumerate(doc):
        # Create transformation matrix
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        
        # Save image
        image_path = os.path.join(output_dir, f'page_{page_num+1}.png')
        pix.save(image_path)
        image_paths.append(image_path)
    
    doc.close()
    return image_paths
```

---

## Batch Processing

### Batch Extract Text

```python
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

def batch_extract_text(input_dir: str, output_dir: str, max_workers: int = 4):
    """Batch extract text from PDFs"""
    os.makedirs(output_dir, exist_ok=True)
    
    pdf_files = [
        os.path.join(input_dir, f)
        for f in os.listdir(input_dir)
        if f.lower().endswith('.pdf')
    ]
    
    results = {}
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(extract_text_pdfplumber, pdf_path): pdf_path
            for pdf_path in pdf_files
        }
        
        for future in as_completed(futures):
            pdf_path = futures[future]
            try:
                text = future.result()
                output_path = os.path.join(output_dir, f'{os.path.basename(pdf_path)}.txt')
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                
                results[pdf_path] = output_path
            except Exception as e:
                results[pdf_path] = {'error': str(e)}
    
    return results
```

### Batch Merge

```python
import os

def batch_merge_pdfs(input_dir: str, output_dir: str, batch_size: int = 10):
    """Batch merge PDFs"""
    os.makedirs(output_dir, exist_ok=True)
    
    pdf_files = sorted([
        os.path.join(input_dir, f)
        for f in os.listdir(input_dir)
        if f.lower().endswith('.pdf')
    ])
    
    for i in range(0, len(pdf_files), batch_size):
        batch = pdf_files[i:i + batch_size]
        output_path = os.path.join(output_dir, f'merged_{i//batch_size + 1}.pdf')
        merge_pdfs(output_path, batch)
```

---

## Performance Optimization

### Memory Optimization

```python
import fitz

def process_large_pdf_memory_efficient(pdf_path: str, process_func: callable):
    """Process large PDF with memory efficiency"""
    doc = fitz.open(pdf_path)
    
    for page_num in range(doc.page_count):
        # Process one page at a time
        page = doc[page_num]
        result = process_func(page)
        yield result
    
    doc.close()

def extract_text_streaming(pdf_path: str):
    """Stream text extraction"""
    doc = fitz.open(pdf_path)
    
    for page in doc:
        yield page.get_text()
    
    doc.close()
```

### Parallel Processing

```python
from concurrent.futures import ProcessPoolExecutor
import fitz

def process_page(page_data: tuple) -> dict:
    """Process single page"""
    pdf_path, page_num = page_data
    doc = fitz.open(pdf_path)
    page = doc[page_num]
    text = page.get_text()
    doc.close()
    
    return {'page': page_num, 'text': text}

def process_pdf_parallel(pdf_path: str, max_workers: int = 4) -> list:
    """Process PDF in parallel"""
    doc = fitz.open(pdf_path)
    total_pages = doc.page_count
    doc.close()
    
    page_data = [(pdf_path, i) for i in range(total_pages)]
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(process_page, page_data))
    
    return sorted(results, key=lambda x: x['page'])
```

---

## Common Issues and Solutions

### Encrypted PDFs

```python
import PyPDF2

def handle_encrypted_pdf(pdf_path: str, password: str = None) -> bool:
    """Handle encrypted PDFs"""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        if reader.is_encrypted:
            if password:
                if reader.decrypt(password):
                    return True
            else:
                # Try empty password
                if reader.decrypt(""):
                    return True
        
        return not reader.is_encrypted

def try_decrypt_with_passwords(pdf_path: str, passwords: list) -> bool:
    """Try multiple passwords"""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        if not reader.is_encrypted:
            return True
        
        for password in passwords:
            if reader.decrypt(password):
                return True
        
        return False
```

### Corrupted PDFs

```python
import fitz

def validate_pdf(pdf_path: str) -> tuple:
    """Validate PDF integrity"""
    try:
        doc = fitz.open(pdf_path)
        is_valid = True
        num_pages = doc.page_count
        error = None
        doc.close()
    except Exception as e:
        is_valid = False
        num_pages = 0
        error = str(e)
    
    return is_valid, num_pages, error

def recover_pdf(pdf_path: str, output_path: str):
    """Attempt to recover corrupted PDF"""
    try:
        doc = fitz.open(pdf_path)
        new_doc = fitz.open()
        
        for page in doc:
            new_doc.insert_pdf(doc, from_page=page.number, to_page=page.number)
        
        new_doc.save(output_path, garbage=4, deflate=True)
        new_doc.close()
        doc.close()
        
        return True
    except Exception as e:
        return False
```

---

## Related Skills

- [Document Ingestion Pipeline](../07-document-processing/document-ingestion-pipeline/SKILL.md) - Document loading and processing workflows
- [Document Parsing](../07-document-processing/document-parsing/SKILL.md) - Structured data extraction from documents
- [Image Preprocessing](../07-document-processing/image-preprocessing/SKILL.md) - Image enhancement for better OCR accuracy
- [OCR with Tesseract](../07-document-processing/ocr-tesseract/SKILL.md) - Text extraction using Tesseract OCR
- [OCR with PaddleOCR](../07-document-processing/ocr-paddleocr/SKILL.md) - Text extraction using PaddleOCR
- [RAG Implementation](../06-ai-ml-production/rag-implementation/SKILL.md) - Retrieval-Augmented Generation patterns

## Additional Resources

- [PyPDF2 Documentation](https://pypdf2.readthedocs.io/)
- [pdfplumber Documentation](https://github.com/jsvine/pdfplumber)
- [PyMuPDF Documentation](https://pymupdf.readthedocs.io/)
- [ReportLab Documentation](https://www.reportlab.com/documentation/)
- [WeasyPrint Documentation](https://weasyprint.readthedocs.io/)
- [pdf2image Documentation](https://pdf2image.readthedocs.io/)
