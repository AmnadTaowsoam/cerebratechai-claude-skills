---
name: Document Parsing
description: Comprehensive guide to structured document parsing and information extraction from various document types
---

---
name: Document Parsing
description: Comprehensive guide to structured document parsing and information extraction from various document types
---

# Document Parsing

## Overview

Comprehensive guide to structured document parsing and information extraction from various document types.

## Prerequisites

- Understanding of document formats (PDF, images, scanned documents)
- Knowledge of OCR (Optical Character Recognition) techniques
- Familiarity with regular expressions for pattern matching
- Experience with data structures and validation schemas
- Understanding of NLP (Natural Language Processing) and named entity recognition
- Familiarity with computer vision and image processing
- Knowledge of document layout analysis
- Experience with PDF parsing libraries

## Key Concepts

- **Document Types**: Invoices, receipts, forms, contracts, reports, tables
- **Extraction Techniques**: Template-based, rule-based, ML-based extraction
- **Libraries**: pdfplumber, PyPDF2, Camelot, Tabula, pdfplumber, Spacy, Transformers
- **Layout Analysis**: Detecting document structure, regions, columns
- **Table Extraction**: Extracting tables from PDFs using various libraries
- **Information Extraction**: Key-value pairs, entities, dates, amounts
- **Post-processing**: Data normalization, validation, error handling
- **Caching**: Storing extracted data to improve performance
- **Production Patterns**: Pipeline architecture, monitoring, error handling

## Table of Contents

1. [Document Types](#document-types)
2. [Extraction Techniques](#extraction-techniques)
3. [Libraries](#libraries)
4. [Layout Analysis](#layout-analysis)
5. [Table Extraction](#table-extraction)
6. [Information Extraction](#information-extraction)
7. [Post-processing](#post-processing)
8. [Validation](#validation)
9. [Error Handling](#error-handling)
10. [Production Patterns](#production-patterns)

---

## Document Types

### Invoices

```python
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

@dataclass
class Invoice:
    invoice_number: str
    date: datetime
    due_date: Optional[datetime] = None
    vendor: Optional[str] = None
    vendor_address: Optional[str] = None
    billing_address: Optional[str] = None
    line_items: List[dict] = None
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    total: Optional[float] = None
    currency: str = "USD"
    notes: Optional[str] = None

    def __post_init__(self):
        if self.line_items is None:
            self.line_items = []
```

### Receipts

```python
@dataclass
class Receipt:
    merchant: str
    date: datetime
    time: Optional[datetime.time] = None
    items: List[dict] = None
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    tip: Optional[float] = None
    total: Optional[float] = None
    payment_method: Optional[str] = None
    transaction_id: Optional[str] = None

    def __post_init__(self):
        if self.items is None:
            self.items = []
```

### Forms

```python
@dataclass
class FormField:
    name: str
    value: str
    field_type: str
    confidence: float = 1.0
    bbox: Optional[tuple] = None

@dataclass
class Form:
    form_type: str
    fields: List[FormField]
    page_count: int = 1

    def get_field(self, name: str) -> Optional[FormField]:
        for field in self.fields:
            if field.name == name:
                return field
        return None
```

### Contracts

```python
@dataclass
class Contract:
    title: str
    parties: List[str]
    effective_date: datetime
    expiration_date: Optional[datetime] = None
    clauses: List[dict] = None
    signatures: List[dict] = None

    def __post_init__(self):
        if self.clauses is None:
            self.clauses = []
        if self.signatures is None:
            self.signatures = []
```

---

## Extraction Techniques

### Template-Based Extraction

```python
import re
from typing import Dict, Any

class TemplateExtractor:
    def __init__(self, template: Dict[str, Any]):
        self.template = template
    
    def extract(self, text: str) -> Dict[str, Any]:
        """Extract fields based on template patterns"""
        result = {}
        
        for field_name, pattern_config in self.template.items():
            pattern = pattern_config['pattern']
            extraction_type = pattern_config.get('type', 'first')
            
            if extraction_type == 'first':
                match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
                if match:
                    result[field_name] = match.group(1) if match.groups() else match.group()
            
            elif extraction_type == 'all':
                matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
                result[field_name] = matches
            
            elif extraction_type == 'date':
                result[field_name] = self._extract_date(text, pattern)
            
            elif extraction_type == 'amount':
                result[field_name] = self._extract_amount(text, pattern)
        
        return result
    
    def _extract_date(self, text: str, pattern: str) -> datetime:
        """Extract and parse date"""
        from dateutil import parser
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return parser.parse(match.group())
        return None
    
    def _extract_amount(self, text: str, pattern: str) -> float:
        """Extract and parse amount"""
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            amount_str = match.group(1).replace(',', '').replace('$', '')
            return float(amount_str)
        return None

# Invoice template example
INVOICE_TEMPLATE = {
    'invoice_number': {
        'pattern': r'invoice\s*#?\s*[:#]?\s*([A-Z0-9-]+)',
        'type': 'first'
    },
    'date': {
        'pattern': r'(?:date|invoice\s*date)\s*[:]\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        'type': 'date'
    },
    'total': {
        'pattern': r'(?:total|amount\s*due|grand\s*total)\s*[:$]?\s*[$]?\s*([\d,]+\.\d{2})',
        'type': 'amount'
    }
}

# Usage
extractor = TemplateExtractor(INVOICE_TEMPLATE)
invoice_data = extractor.extract(invoice_text)
```

### Rule-Based Extraction

```python
class RuleBasedExtractor:
    def __init__(self):
        self.rules = []
    
    def add_rule(self, rule_name: str, condition: callable, extractor: callable):
        """Add extraction rule"""
        self.rules.append({
            'name': rule_name,
            'condition': condition,
            'extractor': extractor
        })
    
    def extract(self, text: str) -> Dict[str, Any]:
        """Extract using rules"""
        result = {}
        
        for rule in self.rules:
            if rule['condition'](text):
                extracted = rule['extractor'](text)
                result[rule['name']] = extracted
        
        return result

# Example rules
extractor = RuleBasedExtractor()

# Rule: Extract email addresses
extractor.add_rule(
    'emails',
    lambda text: '@' in text,
    lambda text: re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)
)

# Rule: Extract phone numbers
extractor.add_rule(
    'phone_numbers',
    lambda text: any(c.isdigit() for c in text),
    lambda text: re.findall(r'\+?[\d\s-]{10,}', text)
)

# Rule: Extract URLs
extractor.add_rule(
    'urls',
    lambda text: 'http' in text.lower(),
    lambda text: re.findall(r'https?://[^\s]+', text)
)
```

### ML-Based Extraction

```python
from transformers import pipeline
import spacy

class MLExtractor:
    def __init__(self):
        # Named Entity Recognition
        self.ner = pipeline('ner', aggregation_strategy='simple')
        
        # Spacy for additional NLP tasks
        self.nlp = spacy.load('en_core_web_sm')
    
    def extract_entities(self, text: str) -> Dict[str, list]:
        """Extract named entities"""
        entities = self.ner(text)
        
        # Group by entity type
        grouped = {}
        for entity in entities:
            entity_type = entity['entity_group']
            if entity_type not in grouped:
                grouped[entity_type] = []
            grouped[entity_type].append({
                'text': entity['word'],
                'confidence': entity['score']
            })
        
        return grouped
    
    def extract_dates(self, text: str) -> list:
        """Extract dates using Spacy"""
        doc = self.nlp(text)
        dates = [ent.text for ent in doc.ents if ent.label_ == 'DATE']
        return dates
    
    def extract_money(self, text: str) -> list:
        """Extract money amounts"""
        doc = self.nlp(text)
        money = [ent.text for ent in doc.ents if ent.label_ == 'MONEY']
        return money
    
    def extract_organizations(self, text: str) -> list:
        """Extract organization names"""
        doc = self.nlp(text)
        orgs = [ent.text for ent in doc.ents if ent.label_ == 'ORG']
        return orgs
```

---

## Libraries

### pdfplumber

```python
import pdfplumber

def extract_text_pdfplumber(pdf_path: str) -> str:
    """Extract text using pdfplumber"""
    text = ""
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    
    return text

def extract_tables_pdfplumber(pdf_path: str) -> list:
    """Extract tables using pdfplumber"""
    tables = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_tables = page.extract_tables()
            if page_tables:
                tables.extend(page_tables)
    
    return tables

def extract_with_settings(pdf_path: str) -> dict:
    """Extract with custom settings"""
    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[0]
        
        # Custom extraction settings
        text = first_page.extract_text(
            x_tolerance=2,
            y_tolerance=2,
            layout=False,
            x_density=7.25,
            y_density=7.25
        )
        
        # Extract tables with settings
        tables = first_page.extract_tables({
            "vertical_strategy": "text",
            "horizontal_strategy": "text",
            "min_words_vertical": 3,
            "min_words_horizontal": 3
        })
    
    return {'text': text, 'tables': tables}
```

### PyPDF2

```python
import PyPDF2

def extract_text_pypdf2(pdf_path: str) -> str:
    """Extract text using PyPDF2"""
    text = ""
    
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        for page in reader.pages:
            text += page.extract_text() + "\n"
    
    return text

def extract_metadata_pypdf2(pdf_path: str) -> dict:
    """Extract PDF metadata"""
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
        'modification_date': metadata.get('/ModDate')
    }

def merge_pdfs(output_path: str, pdf_paths: list):
    """Merge multiple PDFs"""
    merger = PyPDF2.PdfMerger()
    
    for pdf_path in pdf_paths:
        merger.append(pdf_path)
    
    merger.write(output_path)
    merger.close()
```

### Camelot

```python
import camelot

def extract_tables_camelot(pdf_path: str, pages: str = '1') -> list:
    """Extract tables using Camelot"""
    tables = camelot.read_pdf(pdf_path, pages=pages, flavor='lattice')
    
    # Convert to list of DataFrames
    table_list = [table.df for table in tables]
    
    return table_list

def extract_tables_stream(pdf_path: str) -> list:
    """Extract tables using stream mode (for unstructured tables)"""
    tables = camelot.read_pdf(pdf_path, flavor='stream')
    
    # Get table accuracy
    for i, table in enumerate(tables):
        print(f"Table {i} accuracy: {table.accuracy}")
    
    return [table.df for table in tables]

def export_tables(tables: list, output_format: str = 'csv', output_dir: str = 'output'):
    """Export tables to various formats"""
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    for i, table in enumerate(tables):
        output_path = os.path.join(output_dir, f'table_{i}.{output_format}')
        table.to_csv(output_path, index=False)
```

### Tabula

```python
import tabula

def extract_tables_tabula(pdf_path: str) -> list:
    """Extract tables using Tabula"""
    tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
    return tables

def extract_with_area(pdf_path: str, area: list) -> list:
    """Extract tables from specific area"""
    # Area format: [top, left, bottom, right]
    tables = tabula.read_pdf(pdf_path, area=area, pages='all')
    return tables

def convert_to_dataframe(pdf_path: str) -> list:
    """Convert PDF tables to DataFrames"""
    import pandas as pd
    dfs = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
    
    # Convert to pandas DataFrames
    dataframes = [pd.DataFrame(table) for table in dfs]
    
    return dataframes
```

---

## Layout Analysis

### Document Layout Detection

```python
import cv2
import numpy as np

class LayoutAnalyzer:
    def __init__(self):
        pass
    
    def detect_blocks(self, image_path: str) -> list:
        """Detect text blocks in document"""
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Threshold
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Find contours
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        blocks = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            
            # Filter small blocks
            if w > 50 and h > 20:
                blocks.append({
                    'bbox': (x, y, w, h),
                    'area': w * h
                })
        
        return blocks
    
    def detect_columns(self, image_path: str) -> int:
        """Detect number of columns"""
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Project vertical histogram
        vertical_projection = np.sum(gray, axis=0)
        
        # Find valleys (gaps between columns)
        threshold = np.mean(vertical_projection) * 0.5
        gaps = vertical_projection < threshold
        
        # Count column transitions
        column_count = 1
        prev_gap = False
        
        for is_gap in gaps:
            if is_gap and not prev_gap:
                column_count += 1
            prev_gap = is_gap
        
        return column_count
    
    def detect_regions(self, image_path: str) -> dict:
        """Detect different regions (header, body, footer)"""
        image = cv2.imread(image_path)
        height = image.shape[0]
        
        regions = {
            'header': (0, int(height * 0.15)),
            'body': (int(height * 0.15), int(height * 0.85)),
            'footer': (int(height * 0.85), height)
        }
        
        return regions
```

### Text Region Classification

```python
from sklearn.cluster import KMeans

class TextClassifier:
    def __init__(self):
        pass
    
    def classify_by_font_size(self, blocks: list) -> dict:
        """Classify blocks by font size"""
        font_sizes = [block['height'] for block in blocks]
        
        # Cluster by height
        kmeans = KMeans(n_clusters=3)
        labels = kmeans.fit_predict([[fs] for fs in font_sizes])
        
        # Classify based on clusters
        classified = {}
        for block, label in zip(blocks, labels):
            if label == 0:
                classification = 'small'
            elif label == 1:
                classification = 'medium'
            else:
                classification = 'large'
            
            if classification not in classified:
                classified[classification] = []
            classified[classification].append(block)
        
        return classified
    
    def detect_headers(self, blocks: list) -> list:
        """Detect header blocks (large font, top of page)"""
        headers = []
        
        for block in blocks:
            y = block['bbox'][1]
            height = block['bbox'][3]
            
            # Top of page and large font
            if y < 200 and height > 30:
                headers.append(block)
        
        return headers
```

---

## Table Extraction

### Table Detection

```python
import cv2
import numpy as np

class TableDetector:
    def __init__(self):
        pass
    
    def detect_tables(self, image_path: str) -> list:
        """Detect tables in document image"""
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect horizontal lines
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
        horizontal_lines = cv2.morphologyEx(gray, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
        
        # Detect vertical lines
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
        vertical_lines = cv2.morphologyEx(gray, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
        
        # Combine lines
        table_mask = cv2.addWeighted(horizontal_lines, 0.5, vertical_lines, 0.5, 0.0)
        
        # Find contours
        contours, _ = cv2.findContours(table_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        tables = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            
            # Filter by aspect ratio and size
            aspect_ratio = w / h
            if 0.5 < aspect_ratio < 5 and w > 100 and h > 50:
                tables.append({
                    'bbox': (x, y, w, h),
                    'area': w * h
                })
        
        return tables
```

### Table Structure Parsing

```python
class TableParser:
    def __init__(self):
        pass
    
    def parse_table(self, image: np.ndarray, bbox: tuple) -> list:
        """Parse table structure from image region"""
        x, y, w, h = bbox
        table_region = image[y:y+h, x:x+w]
        
        # Detect horizontal lines
        gray = cv2.cvtColor(table_region, cv2.COLOR_BGR2GRAY)
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
        horizontal_lines = cv2.morphologyEx(gray, cv2.MORPH_OPEN, horizontal_kernel)
        
        # Detect vertical lines
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
        vertical_lines = cv2.morphologyEx(gray, cv2.MORPH_OPEN, vertical_kernel)
        
        # Find row and column positions
        rows = self._find_lines(horizontal_lines, axis=0)
        cols = self._find_lines(vertical_lines, axis=1)
        
        # Create cell grid
        cells = []
        for i in range(len(rows) - 1):
            for j in range(len(cols) - 1):
                cell_bbox = (
                    cols[j],
                    rows[i],
                    cols[j + 1] - cols[j],
                    rows[i + 1] - rows[i]
                )
                cells.append({
                    'row': i,
                    'col': j,
                    'bbox': cell_bbox
                })
        
        return {
            'rows': len(rows) - 1,
            'cols': len(cols) - 1,
            'cells': cells
        }
    
    def _find_lines(self, image: np.ndarray, axis: int) -> list:
        """Find line positions"""
        projection = np.sum(image, axis=axis)
        threshold = np.mean(projection) * 0.8
        
        lines = []
        in_line = False
        line_start = 0
        
        for i, value in enumerate(projection):
            if value > threshold and not in_line:
                line_start = i
                in_line = True
            elif value <= threshold and in_line:
                lines.append((line_start + i) // 2)
                in_line = False
        
        return lines
```

---

## Information Extraction

### Key-Value Extraction

```python
import re

class KeyValueExtractor:
    def __init__(self):
        self.patterns = {
            'date': r'(?:date|dated|on)[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            'amount': r'(?:amount|total|sum)[:\s]*[$]?\s*([\d,]+\.\d{2})',
            'email': r'email[:\s]*([\w\.-]+@[\w\.-]+\.\w+)',
            'phone': r'(?:phone|tel|mobile)[:\s]*([\d\s-]+)',
            'address': r'(?:address|addr)[:\s]*(.+?)(?:\n|$)'
        }
    
    def extract(self, text: str) -> dict:
        """Extract key-value pairs"""
        result = {}
        
        for key, pattern in self.patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                result[key] = match.group(1).strip()
        
        return result
    
    def extract_with_context(self, text: str, context_window: int = 50) -> dict:
        """Extract with surrounding context"""
        result = {}
        
        for key, pattern in self.patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                start = max(0, match.start() - context_window)
                end = min(len(text), match.end() + context_window)
                result[key] = {
                    'value': match.group(1).strip(),
                    'context': text[start:end]
                }
        
        return result
```

### Entity Extraction

```python
import spacy

class EntityExtractor:
    def __init__(self, model_name: str = 'en_core_web_sm'):
        self.nlp = spacy.load(model_name)
    
    def extract_all_entities(self, text: str) -> dict:
        """Extract all named entities"""
        doc = self.nlp(text)
        
        entities = {}
        for ent in doc.ents:
            label = ent.label_
            if label not in entities:
                entities[label] = []
            entities[label].append({
                'text': ent.text,
                'start': ent.start_char,
                'end': ent.end_char,
                'confidence': 1.0  # Spacy doesn't provide confidence
            })
        
        return entities
    
    def extract_specific_entities(self, text: str, entity_types: list) -> dict:
        """Extract specific entity types"""
        doc = self.nlp(text)
        
        entities = {}
        for ent in doc.ents:
            if ent.label_ in entity_types:
                if ent.label_ not in entities:
                    entities[ent.label_] = []
                entities[ent.label_].append(ent.text)
        
        return entities

# Usage
extractor = EntityExtractor()
entities = extractor.extract_specific_entities(
    invoice_text,
    entity_types=['ORG', 'PERSON', 'DATE', 'MONEY']
)
```

---

## Post-processing

### Data Normalization

```python
from datetime import datetime
from dateutil import parser

class DataNormalizer:
    @staticmethod
    def normalize_date(date_str: str) -> datetime:
        """Normalize date string to datetime object"""
        try:
            return parser.parse(date_str)
        except:
            return None
    
    @staticmethod
    def normalize_amount(amount_str: str) -> float:
        """Normalize amount string to float"""
        # Remove currency symbols and commas
        cleaned = amount_str.replace('$', '').replace(',', '').strip()
        try:
            return float(cleaned)
        except:
            return None
    
    @staticmethod
    def normalize_phone(phone_str: str) -> str:
        """Normalize phone number"""
        # Remove non-digit characters
        digits = ''.join(c for c in phone_str if c.isdigit())
        return digits
    
    @staticmethod
    def normalize_email(email_str: str) -> str:
        """Normalize email"""
        return email_str.strip().lower()
```

### Data Validation

```python
import re

class DataValidator:
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number"""
        digits = ''.join(c for c in phone if c.isdigit())
        return len(digits) >= 10
    
    @staticmethod
    def validate_date(date_obj: datetime) -> bool:
        """Validate date is reasonable"""
        now = datetime.now()
        min_date = datetime(1900, 1, 1)
        max_date = datetime(now.year + 1, 12, 31)
        return min_date <= date_obj <= max_date
    
    @staticmethod
    def validate_amount(amount: float) -> bool:
        """Validate amount is positive"""
        return amount is not None and amount >= 0
```

---

## Validation

### Field Validation

```python
class FieldValidator:
    def __init__(self, schema: dict):
        self.schema = schema
    
    def validate(self, data: dict) -> tuple:
        """Validate data against schema"""
        errors = []
        warnings = []
        
        for field_name, field_config in self.schema.items():
            # Check required fields
            if field_config.get('required', False) and field_name not in data:
                errors.append(f"Missing required field: {field_name}")
                continue
            
            # Skip validation if field is not present
            if field_name not in data:
                continue
            
            value = data[field_name]
            
            # Type validation
            expected_type = field_config.get('type')
            if expected_type and not isinstance(value, expected_type):
                errors.append(f"Field {field_name} should be {expected_type.__name__}")
            
            # Pattern validation
            pattern = field_config.get('pattern')
            if pattern and isinstance(value, str):
                if not re.match(pattern, value):
                    errors.append(f"Field {field_name} doesn't match pattern")
            
            # Range validation
            min_val = field_config.get('min')
            max_val = field_config.get('max')
            if isinstance(value, (int, float)):
                if min_val is not None and value < min_val:
                    errors.append(f"Field {field_name} below minimum")
                if max_val is not None and value > max_val:
                    errors.append(f"Field {field_name} above maximum")
        
        return errors, warnings

# Example schema
INVOICE_SCHEMA = {
    'invoice_number': {
        'type': str,
        'required': True,
        'pattern': r'^[A-Z0-9-]+$'
    },
    'date': {
        'type': datetime,
        'required': True
    },
    'total': {
        'type': float,
        'required': True,
        'min': 0
    }
}
```

---

## Error Handling

### Robust Extraction

```python
from typing import Optional, Dict, Any
import traceback

class RobustExtractor:
    def __init__(self):
        self.extractors = []
    
    def add_extractor(self, extractor: callable, priority: int = 0):
        """Add extractor with priority"""
        self.extractors.append({
            'extractor': extractor,
            'priority': priority
        })
        self.extractors.sort(key=lambda x: x['priority'], reverse=True)
    
    def extract(self, text: str) -> Dict[str, Any]:
        """Extract with fallback to other extractors"""
        result = {}
        
        for extractor_config in self.extractors:
            extractor = extractor_config['extractor']
            
            try:
                extracted = extractor(text)
                
                # Merge results
                for key, value in extracted.items():
                    if key not in result:
                        result[key] = value
                
            except Exception as e:
                print(f"Extractor failed: {str(e)}")
                continue
        
        return result
    
    def extract_with_retry(self, text: str, max_retries: int = 3) -> Dict[str, Any]:
        """Extract with retry logic"""
        last_error = None
        
        for attempt in range(max_retries):
            try:
                return self.extract(text)
            except Exception as e:
                last_error = e
                print(f"Attempt {attempt + 1} failed: {str(e)}")
        
        raise last_error
```

---

## Production Patterns

### Pipeline Pattern

```python
from typing import List, Callable

class DocumentPipeline:
    def __init__(self):
        self.steps: List[Callable] = []
    
    def add_step(self, step: Callable, name: str = None):
        """Add processing step"""
        self.steps.append({
            'step': step,
            'name': name or step.__name__
        })
    
    def process(self, document: Any) -> dict:
        """Process document through pipeline"""
        result = {
            'document': document,
            'steps': []
        }
        
        for step_config in self.steps:
            step = step_config['step']
            step_name = step_config['name']
            
            try:
                document = step(document)
                result['steps'].append({
                    'name': step_name,
                    'status': 'success'
                })
            except Exception as e:
                result['steps'].append({
                    'name': step_name,
                    'status': 'failed',
                    'error': str(e)
                })
                break
        
        result['document'] = document
        return result

# Example pipeline
pipeline = DocumentPipeline()
pipeline.add_step(load_document, 'load')
pipeline.add_step(extract_text, 'extract_text')
pipeline.add_step(extract_entities, 'extract_entities')
pipeline.add_step(validate_data, 'validate')

result = pipeline.process('invoice.pdf')
```

### Caching Pattern

```python
from functools import lru_cache
import hashlib
import pickle
import os

class CachedExtractor:
    def __init__(self, cache_dir: str = '.cache'):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_cache_key(self, text: str) -> str:
        """Generate cache key from text"""
        return hashlib.md5(text.encode()).hexdigest()
    
    def _get_cache_path(self, key: str) -> str:
        """Get cache file path"""
        return os.path.join(self.cache_dir, f'{key}.pkl')
    
    def extract_with_cache(self, text: str, extractor: callable) -> dict:
        """Extract with caching"""
        cache_key = self._get_cache_key(text)
        cache_path = self._get_cache_path(cache_key)
        
        # Check cache
        if os.path.exists(cache_path):
            with open(cache_path, 'rb') as f:
                return pickle.load(f)
        
        # Extract and cache
        result = extractor(text)
        
        with open(cache_path, 'wb') as f:
            pickle.dump(result, f)
        
        return result
```

---

## Additional Resources

- [pdfplumber Documentation](https://github.com/jsvine/pdfplumber)
- [Camelot Documentation](https://camelot-py.readthedocs.io/)
- [Tabula Documentation](https://tabula-py.readthedocs.io/)
- [Spacy Documentation](https://spacy.io/)
- [Transformers Documentation](https://huggingface.co/docs/transformers)
