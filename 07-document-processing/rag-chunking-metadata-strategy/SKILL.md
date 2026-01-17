# RAG Chunking Metadata Strategy

## Overview

RAG chunking metadata strategy covers the systematic approach to adding, managing, and leveraging metadata throughout the RAG pipeline. This skill includes metadata schemas, chunk-level metadata, document-level metadata, and metadata-driven retrieval strategies.

**When to use this skill:** When designing or implementing RAG systems that need rich metadata for improved retrieval accuracy and context management.

## Table of Contents

1. [Metadata Schema Design](#metadata-schema-design)
2. [Chunk-Level Metadata](#chunk-level-metadata)
3. [Document-Level Metadata](#document-level-metadata)
4. [Metadata-Driven Retrieval](#metadata-driven-retrieval)
5. [Metadata Storage](#metadata-storage)
6. [Chunking Metadata Checklist](#chunking-metadata-checklist)
7. [Quick Reference](#quick-reference)

---

## Metadata Schema Design

### Core Metadata Fields

| Field | Type | Description | Example |
|-------|------|-------------|----------|
| `chunk_id` | string | Unique identifier for chunk | `doc_123_chunk_45` |
| `document_id` | string | Parent document identifier | `doc_123` |
| `chunk_index` | integer | Position within document | `0, 1, 2` |
| `text` | string | Chunk content | `"The quick brown fox..."` |
| `token_count` | integer | Number of tokens | `150` |
| `embedding_id` | string | Vector database reference | `vec_abc123` |
| `created_at` | timestamp | Creation time | `2024-01-15T10:30:00Z` |
| `updated_at` | timestamp | Last update time | `2024-01-15T10:30:00Z` |
| `source_type` | enum | Content origin | `pdf`, `web`, `database` |
| `content_type` | enum | Document section type | `introduction`, `methodology`, `results` |
| `language` | string | Detected language | `en`, `es`, `fr` |

### Extended Metadata Fields

| Field | Type | Description | Example |
|-------|------|-------------|----------|
| `title` | string | Chunk title | `"Introduction to Machine Learning"` |
| `summary` | string | Chunk summary | `"Overview of ML concepts"` |
| `keywords` | array | Search keywords | `["machine learning", "AI", "data"]` |
| `entities` | array | Named entities | `[{"type": "PERSON", "text": "John Doe"}]` |
| `section_hierarchy` | array | Document structure | `["chapter", "section", "subsection"]` |
| `cross_references` | array | Links to other chunks | `["doc_123_chunk_44", "doc_123_chunk_46"]` |
| `quality_score` | float | Content quality score | `0.95` |
| `access_level` | enum | Permission level | `public`, `internal`, `restricted` |

### Metadata JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "RAG Chunk Metadata",
  "type": "object",
  "required": ["chunk_id", "document_id", "text"],
  "properties": {
    "chunk_id": {
      "type": "string",
      "description": "Unique chunk identifier"
    },
    "document_id": {
      "type": "string",
      "description": "Parent document identifier"
    },
    "text": {
      "type": "string",
      "description": "Chunk content text"
    },
    "chunk_index": {
      "type": "integer",
      "description": "Position within document"
    },
    "token_count": {
      "type": "integer",
      "description": "Number of tokens in chunk"
    },
    "embedding_id": {
      "type": "string",
      "description": "Vector database reference"
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "description": "Creation timestamp"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time",
      "description": "Last update timestamp"
    },
    "source_type": {
      "type": "string",
      "enum": ["pdf", "web", "database", "api", "manual"],
      "description": "Content origin"
    },
    "content_type": {
      "type": "string",
      "enum": ["introduction", "methodology", "results", "conclusion", "appendix", "references"],
      "description": "Document section type"
    },
    "language": {
      "type": "string",
      "description": "Detected content language"
    },
    "title": {
      "type": "string",
      "description": "Chunk title"
    },
    "summary": {
      "type": "string",
      "description": "Chunk summary"
    },
    "keywords": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Search keywords"
    },
    "entities": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "type": {
            "type": "string",
            "enum": ["PERSON", "ORG", "LOCATION", "DATE", "MONEY", "PERCENT"]
          },
          "text": {
            "type": "string"
          }
        }
      }
    },
    "section_hierarchy": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Document structure hierarchy"
    },
    "cross_references": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Links to related chunks"
    },
    "quality_score": {
      "type": "number",
      "minimum": 0,
      "maximum": 1,
      "description": "Content quality score"
    },
    "access_level": {
      "type": "string",
      "enum": ["public", "internal", "restricted"],
      "description": "Permission level"
    }
  }
}
```

---

## Chunk-Level Metadata

### Automatic Metadata Extraction

```python
# Automatic metadata extraction
class MetadataExtractor:
    def __init__(self):
        pass
    
    def extract_chunk_metadata(self, chunk: str, chunk_index: int, document_id: str) -> dict:
        """Extract metadata for a single chunk"""
        # Basic metadata
        metadata = {
            'chunk_id': f"{document_id}_chunk_{chunk_index}",
            'document_id': document_id,
            'chunk_index': chunk_index,
            'text': chunk,
            'token_count': len(chunk.split()),
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        # Content type inference
        metadata['content_type'] = self._infer_content_type(chunk)
        
        # Language detection
        metadata['language'] = self._detect_language(chunk)
        
        # Entity extraction
        metadata['entities'] = self._extract_entities(chunk)
        
        # Keyword extraction
        metadata['keywords'] = self._extract_keywords(chunk)
        
        # Title generation
        metadata['title'] = self._generate_title(chunk)
        
        # Summary generation
        metadata['summary'] = self._generate_summary(chunk)
        
        return metadata
    
    def _infer_content_type(self, text: str) -> str:
        """Infer content type from text"""
        # Simple heuristic-based inference
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['abstract', 'introduction', 'overview']):
            return 'introduction'
        elif any(word in text_lower for word in ['method', 'approach', 'algorithm', 'implementation']):
            return 'methodology'
        elif any(word in text_lower for word in ['result', 'conclusion', 'finding', 'data']):
            return 'results'
        elif any(word in text_lower for word in ['conclusion', 'summary', 'final']):
            return 'conclusion'
        else:
            return 'body'
    
    def _detect_language(self, text: str) -> str:
        """Detect language from text"""
        # Simple language detection
        # In production, use proper language detection library
        # This is a placeholder implementation
        return 'en'  # Default to English
    
    def _extract_entities(self, text: str) -> list:
        """Extract named entities from text"""
        # Simple pattern-based entity extraction
        # In production, use NER model
        entities = []
        
        # Extract dates
        import re
        date_pattern = r'\d{1,2}[-/]\d{1,2}[-/]\d{4}'
        dates = re.findall(date_pattern, text)
        for date in dates:
            entities.append({'type': 'DATE', 'text': date})
        
        # Extract emails
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9._%+-]+\.[A-Za-z]{2,}'
        emails = re.findall(email_pattern, text)
        for email in emails:
            entities.append({'type': 'EMAIL', 'text': email})
        
        # Extract URLs
        url_pattern = r'https?://(?:www\.)?[-a-zA-Z0-9._%]+(?:\.[a-zA-Z]{2,})?[/\S]*'
        urls = re.findall(url_pattern, text)
        for url in urls:
            entities.append({'type': 'URL', 'text': url})
        
        return entities
    
    def _extract_keywords(self, text: str) -> list:
        """Extract keywords from text"""
        # Simple keyword extraction
        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'been', 'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'seem', 'appear', 'look', 'feel', 'try', 'leave', 'called', 'found', 'located', 'created', 'made', 'taken', 'get', 'got', 'went', 'put', 'said', 'told', 'asked', 'answer', 'seems', 'means', 'tends', 'kind', 'sort', 'set', 'begin', 'seem', 'help', 'talk', 'turn', 'start', 'might', 'show', 'hear', 'play', 'run', 'move', 'like', 'live', 'believe', 'hold', 'bring', 'happen', 'write', 'provide', 'sit', 'stand', 'lose', 'pay', 'meet', 'include', 'continue', 'set', 'learn', 'change', 'lead', 'understand', 'watch', 'follow', 'stop', 'create', 'speak', 'read', 'allow', 'add', 'spend', 'grow', 'open', 'walk', 'win', 'offer', 'remember', 'love', 'consider', 'appear', 'buy', 'wait', 'serve', 'die', 'send', 'expect', 'build', 'stay', 'fall', 'cut', 'reach', 'kill', 'remain'}
        words = text.lower().split()
        keywords = [word for word in words if word not in stop_words and len(word) > 3]
        
        # Remove duplicates
        keywords = list(set(keywords))
        
        return keywords[:10]  # Return top 10 keywords
    
    def _generate_title(self, chunk: str) -> str:
        """Generate title from chunk"""
        # Take first sentence or first 50 characters
        sentences = chunk.split('. ')
        first_sentence = sentences[0] if sentences else chunk
        
        # Truncate to reasonable length
        title = first_sentence[:100]
        
        return title
    
    def _generate_summary(self, chunk: str) -> str:
        """Generate summary from chunk"""
        # Take first sentence or first 100 characters
        sentences = chunk.split('. ')
        first_sentence = sentences[0] if sentences else chunk
        
        # Truncate to reasonable length
        summary = first_sentence[:200]
        
        return summary
```

### Manual Metadata Enhancement

```python
# Manual metadata enhancement
class MetadataEnhancer:
    def __init__(self):
        pass
    
    def add_cross_references(self, metadata: dict, references: list) -> dict:
        """Add cross-references to metadata"""
        metadata['cross_references'] = references
        return metadata
    
    def update_quality_score(self, metadata: dict, score: float) -> dict:
        """Update quality score"""
        metadata['quality_score'] = score
        metadata['updated_at'] = datetime.utcnow().isoformat()
        return metadata
    
    def add_access_level(self, metadata: dict, level: str) -> dict:
        """Add access level to metadata"""
        metadata['access_level'] = level
        metadata['updated_at'] = datetime.utcnow().isoformat()
        return metadata
    
    def add_section_hierarchy(self, metadata: dict, hierarchy: list) -> dict:
        """Add section hierarchy to metadata"""
        metadata['section_hierarchy'] = hierarchy
        metadata['updated_at'] = datetime.utcnow().isoformat()
        return metadata
```

---

## Document-Level Metadata

### Document Metadata Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Document Metadata",
  "type": "object",
  "required": ["document_id", "title", "created_at", "chunk_count"],
  "properties": {
    "document_id": {
      "type": "string",
      "description": "Unique document identifier"
    },
    "title": {
      "type": "string",
      "description": "Document title"
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "description": "Creation timestamp"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time",
      "description": "Last update timestamp"
    },
    "chunk_count": {
      "type": "integer",
      "description": "Total number of chunks"
    },
    "source_type": {
      "type": "string",
      "enum": ["pdf", "web", "database", "api", "manual"],
      "description": "Content origin"
    },
    "language": {
      "type": "string",
      "description": "Detected primary language"
    },
    "file_path": {
      "type": "string",
      "description": "Original file path"
    },
    "file_size": {
      "type": "integer",
      "description": "File size in bytes"
    },
    "total_tokens": {
      "type": "integer",
      "description": "Total tokens across all chunks"
    },
    "authors": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Document authors"
    },
    "tags": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Document tags"
    },
    "version": {
      "type": "string",
      "description": "Document version"
    },
    "status": {
      "type": "string",
      "enum": ["draft", "processing", "indexed", "published", "archived"],
      "description": "Document processing status"
    }
  }
}
```

### Document Metadata Management

```python
# Document metadata management
class DocumentMetadata:
    def __init__(self):
        pass
    
    def create_document_metadata(self, file_path: str, title: str) -> dict:
        """Create document metadata"""
        metadata = {
            'document_id': self._generate_id(file_path),
            'title': title,
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat(),
            'source_type': self._infer_source_type(file_path),
            'file_path': file_path,
            'file_size': self._get_file_size(file_path),
            'chunk_count': 0,
            'status': 'processing',
            'language': 'en'  # Default
        }
        
        return metadata
    
    def update_document_status(self, document_id: str, status: str) -> dict:
        """Update document status"""
        # This would update in the database
        metadata = {
            'document_id': document_id,
            'status': status,
            'updated_at': datetime.utcnow().isoformat()
        }
        
        return metadata
    
    def add_chunk_count(self, document_id: str, count: int) -> dict:
        """Add chunk count to document metadata"""
        # This would update in the database
        metadata = {
            'document_id': document_id,
            'chunk_count': count,
            'updated_at': datetime.utcnow().isoformat()
        }
        
        return metadata
    
    def _generate_id(self, file_path: str) -> str:
        """Generate unique document ID"""
        # Use file path or UUID
        import uuid
        return str(uuid.uuid4())
    
    def _infer_source_type(self, file_path: str) -> str:
        """Infer source type from file path"""
        extension = file_path.lower().split('.')[-1]
        
        source_types = {
            'pdf': 'pdf',
            'docx': 'pdf',
            'doc': 'pdf',
            'txt': 'web',
            'html': 'web',
            'md': 'web'
        }
        
        return source_types.get(extension, 'manual')
    
    def _get_file_size(self, file_path: str) -> int:
        """Get file size in bytes"""
        import os
        return os.path.getsize(file_path)
```

---

## Metadata-Driven Retrieval

### Metadata-Based Filtering

```python
# Metadata-driven retrieval
class MetadataRetriever:
    def __init__(self, vector_db, metadata_store):
        self.vector_db = vector_db
        self.metadata_store = metadata_store
    
    async def retrieve_by_metadata(self, filters: dict) -> list:
        """Retrieve chunks based on metadata filters"""
        # Build query from filters
        query = self._build_metadata_query(filters)
        
        # Search vector database
        results = await self.vector_db.search(query)
        
        # Filter by metadata
        filtered_results = self._filter_by_metadata(results, filters)
        
        return filtered_results
    
    def _build_metadata_query(self, filters: dict) -> str:
        """Build query from metadata filters"""
        query_parts = []
        
        # Content type filter
        if 'content_type' in filters:
            query_parts.append(f"content_type:{filters['content_type']}")
        
        # Language filter
        if 'language' in filters:
            query_parts.append(f"language:{filters['language']}")
        
        # Access level filter
        if 'access_level' in filters:
            query_parts.append(f"access_level:{filters['access_level']}")
        
        # Date range filter
        if 'date_from' in filters:
            query_parts.append(f"created_at:>{filters['date_from']}")
        if 'date_to' in filters:
            query_parts.append(f"created_at:<{filters['date_to']}")
        
        # Keywords filter
        if 'keywords' in filters:
            keywords = ' '.join(filters['keywords'])
            query_parts.append(f"keywords:{keywords}")
        
        return ' '.join(query_parts)
    
    def _filter_by_metadata(self, results: list, filters: dict) -> list:
        """Filter results by metadata"""
        filtered = []
        
        for result in results:
            metadata = result.get('metadata', {})
            
            # Content type filter
            if 'content_type' in filters:
                if metadata.get('content_type') != filters['content_type']:
                    continue
            
            # Language filter
            if 'language' in filters:
                if metadata.get('language') != filters['language']:
                    continue
            
            # Access level filter
            if 'access_level' in filters:
                if metadata.get('access_level') != filters['access_level']:
                    continue
            
            # Date range filter
            if 'date_from' in filters:
                if metadata.get('created_at') < filters['date_from']:
                    continue
            if 'date_to' in filters:
                if metadata.get('created_at') > filters['date_to']:
                    continue
            
            # Keywords filter
            if 'keywords' in filters:
                result_keywords = set(metadata.get('keywords', []))
                filter_keywords = set(filters['keywords'])
                if not result_keywords.intersection(filter_keywords):
                    continue
            
            filtered.append(result)
        
        return filtered
```

### Metadata-Augmented Search

```python
# Metadata-augmented search
class MetadataAugmentedSearch:
    def __init__(self, vector_db, metadata_store):
        self.vector_db = vector_db
        self.metadata_store = metadata_store
    
    async def search_with_metadata_boost(self, query: str, metadata_filters: dict) -> list:
        """Search with metadata boost"""
        # Standard vector search
        vector_results = await self.vector_db.search(query)
        
        # Get metadata for results
        for result in vector_results:
            metadata = await self.metadata_store.get(result['id'])
            result['metadata'] = metadata
        
        # Apply metadata filters
        filtered_results = self._apply_metadata_filters(vector_results, metadata_filters)
        
        # Rerank with metadata score
        reranked = self._rerank_with_metadata(filtered_results)
        
        return reranked
    
    def _apply_metadata_filters(self, results: list, filters: dict) -> list:
        """Apply metadata filters to results"""
        filtered = []
        
        for result in results:
            metadata = result.get('metadata', {})
            
            # Content type boost
            if 'content_type' in filters:
                if metadata.get('content_type') == filters['content_type']:
                    result['boost'] = result.get('boost', 1.0) + 0.5
                else:
                    continue
            
            # Language boost
            if 'language' in filters:
                if metadata.get('language') == filters['language']:
                    result['boost'] = result.get('boost', 1.0) + 0.3
                else:
                    continue
            
            filtered.append(result)
        
        return filtered
    
    def _rerank_with_metadata(self, results: list) -> list:
        """Rerank results with metadata scores"""
        for result in results:
            base_score = result.get('score', 0.5)
            metadata = result.get('metadata', {})
            
            # Add metadata boost
            boost = metadata.get('boost', 0.0)
            result['score'] = base_score + boost
        
        # Sort by new score
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return results
```

---

## Metadata Storage

### Storage Strategy

| Storage Type | Use Case | Advantages |
|-------------|----------|-----------|
| **Document Store** | Document metadata | Fast document lookup |
| **Chunk Store** | Chunk metadata | Fast chunk filtering |
| **Vector Store** | Vector + metadata | Combined retrieval |
| **Hybrid Store** | Document + chunk + vector | Complete metadata management |

### Storage Implementation

```python
# Metadata storage implementation
class MetadataStore:
    def __init__(self, storage_backend):
        self.storage = storage_backend
    
    async def store_chunk_metadata(self, metadata: dict) -> str:
        """Store chunk metadata"""
        # Store in document store with chunk_id as key
        await self.storage.put(
            key=f"chunk:{metadata['chunk_id']}",
            value=metadata
        )
        
        return metadata['chunk_id']
    
    async def store_document_metadata(self, metadata: dict) -> str:
        """Store document metadata"""
        # Store in document store with document_id as key
        await self.storage.put(
            key=f"document:{metadata['document_id']}",
            value=metadata
        )
        
        return metadata['document_id']
    
    async def get_chunk_metadata(self, chunk_id: str) -> dict:
        """Get chunk metadata"""
        metadata = await self.storage.get(f"chunk:{chunk_id}")
        return metadata
    
    async def get_document_metadata(self, document_id: str) -> dict:
        """Get document metadata"""
        metadata = await self.storage.get(f"document:{document_id}")
        return metadata
    
    async def update_metadata(self, id: str, updates: dict) -> dict:
        """Update metadata"""
        current = await self.storage.get(id)
        updated = {**current, **updates}
        await self.storage.put(id, updated)
        
        return updated
```

---

## Chunking Metadata Checklist

### Pre-Processing

```markdown
## Pre-Processing Checklist

### Document Analysis
- [ ] Document structure analyzed
- [ ] Content types identified
- [ ] Language detected
- [ ] Entities extracted
- [ ] Keywords extracted
- [ ] Section hierarchy mapped

### Metadata Schema
- [ ] Schema designed
- [ ] Required fields defined
- [ ] Optional fields defined
- [ ] Validation rules defined
- [ ] JSON schema created
```

### Chunking Process

```markdown
## Chunking Process Checklist

### Chunk Creation
- [ ] Chunk boundaries determined
- [ ] Metadata extracted for each chunk
- [ ] Cross-references added
- [ ] Quality scores calculated
- [ ] Token counts verified
- [ ] Embeddings generated

### Metadata Storage
- [ ] Chunk metadata stored
- [ ] Document metadata stored
- [ ] Indexes created
- [ ] Storage optimized
- [ ] Backup configured
```

### Quality Control

```markdown
## Quality Control Checklist

### Validation
- [ ] Schema validation passed
- [ ] Required fields present
- [ ] Data types correct
- [ ] Format validation passed
- [ ] Quality scores in range
- [ ] Duplicate detection passed

### Monitoring
- [ ] Metadata completeness tracked
- [ ] Quality metrics calculated
- [ ] Storage performance monitored
- [ ] Query performance measured
```

---

## Quick Reference

### Metadata Operations

```python
# Metadata operations
from typing import Dict, List

class MetadataOperations:
    def __init__(self, metadata_store):
        self.store = metadata_store
    
    async def create_document(self, file_path: str, title: str) -> str:
        """Create document with metadata"""
        # Create document metadata
        doc_metadata = {
            'document_id': self._generate_id(file_path),
            'title': title,
            'created_at': datetime.utcnow().isoformat(),
            'source_type': self._infer_source_type(file_path),
            'file_path': file_path,
            'file_size': self._get_file_size(file_path),
            'status': 'processing',
            'chunk_count': 0,
            'language': 'en'
        }
        
        # Store document metadata
        await self.store.store_document_metadata(doc_metadata)
        
        return doc_metadata['document_id']
    
    async def add_chunk(self, document_id: str, chunk: str, chunk_index: int) -> str:
        """Add chunk with metadata"""
        # Create chunk metadata
        chunk_metadata = {
            'chunk_id': f"{document_id}_chunk_{chunk_index}",
            'document_id': document_id,
            'chunk_index': chunk_index,
            'text': chunk,
            'token_count': len(chunk.split()),
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat(),
            'content_type': self._infer_content_type(chunk),
            'language': 'en'
        }
        
        # Store chunk metadata
        await self.store.store_chunk_metadata(chunk_metadata)
        
        return chunk_metadata['chunk_id']
    
    async def search_by_metadata(self, filters: Dict[str, str]) -> List[Dict]:
        """Search documents by metadata"""
        # Build metadata query
        query = self._build_metadata_query(filters)
        
        # Search vector database
        results = await self.store.search(query)
        
        # Filter by metadata
        filtered = self._filter_by_metadata(results, filters)
        
        return filtered
    
    async def get_document_info(self, document_id: str) -> Dict[str, str]:
        """Get complete document information"""
        # Get document metadata
        doc_metadata = await self.store.get_document_metadata(document_id)
        
        # Get all chunks
        chunks = await self.store.get_chunks_by_document(document_id)
        
        return {
            'document': doc_metadata,
            'chunks': chunks
        }
```

### Metadata Query Examples

```python
# Metadata query examples
# Query by content type
filters = {
    'content_type': 'introduction'
}
results = await metadata_ops.search_by_metadata(filters)

# Query by language
filters = {
    'language': 'en'
}
results = await metadata_ops.search_by_metadata(filters)

# Query by date range
filters = {
    'date_from': '2024-01-01',
    'date_to': '2024-01-31'
}
results = await metadata_ops.search_by_metadata(filters)

# Query by keywords
filters = {
    'keywords': ['machine learning', 'AI', 'data']
}
results = await metadata_ops.search_by_metadata(filters)

# Combined filters
filters = {
    'content_type': 'methodology',
    'language': 'en',
    'date_from': '2024-01-01'
}
results = await metadata_ops.search_by_metadata(filters)
```

### Metadata Validation

```python
# Metadata validation
class MetadataValidator:
    def __init__(self, schema: dict):
        self.schema = schema
    
    def validate_chunk_metadata(self, metadata: dict) -> bool:
        """Validate chunk metadata against schema"""
        # Check required fields
        required_fields = ['chunk_id', 'document_id', 'text']
        for field in required_fields:
            if field not in metadata:
                return False
        
        # Check data types
        if not isinstance(metadata['chunk_id'], str):
            return False
        if not isinstance(metadata['document_id'], str):
            return False
        if not isinstance(metadata['text'], str):
            return False
        
        # Check enum values
        if 'content_type' in metadata:
            valid_types = ['introduction', 'methodology', 'results', 'conclusion', 'appendix', 'references', 'body']
            if metadata['content_type'] not in valid_types:
                return False
        
        if 'access_level' in metadata:
            valid_levels = ['public', 'internal', 'restricted']
            if metadata['access_level'] not in valid_levels:
                return False
        
        # Check ranges
        if 'quality_score' in metadata:
            if not 0 <= metadata['quality_score'] <= 1:
                return False
        
        return True
    
    def validate_document_metadata(self, metadata: dict) -> bool:
        """Validate document metadata against schema"""
        # Check required fields
        required_fields = ['document_id', 'title', 'created_at']
        for field in required_fields:
            if field not in metadata:
                return False
        
        # Check data types
        if not isinstance(metadata['document_id'], str):
            return False
        if not isinstance(metadata['title'], str):
            return False
        
        # Check enum values
        if 'status' in metadata:
            valid_statuses = ['draft', 'processing', 'indexed', 'published', 'archived']
            if metadata['status'] not in valid_statuses:
                return False
        
        # Check ranges
        if 'chunk_count' in metadata:
            if not isinstance(metadata['chunk_count'], int) or metadata['chunk_count'] < 0:
                return False
        
        return True
```

---

## Common Pitfalls

1. **Missing metadata** - Always extract and store metadata for each chunk
2. **Inconsistent schemas** - Use consistent metadata schemas across documents
3. **No validation** - Validate metadata before storing
4. **Poor quality scores** - Use objective quality metrics
5. **No cross-references** - Link related chunks for better context
6. **Ignoring language** - Use language detection for better retrieval
7. **No access control** - Implement access levels for security
8. **Not updating metadata** - Keep metadata up to date

## Additional Resources

- [JSON Schema Documentation](https://json-schema.org/)
- [RAG Metadata Best Practices](https://arize.org/blog/retrieval-augmented-generation)
- [Vector Database Metadata](https://www.pinecone.io/learn/metadata-filtering/)
- [Document Processing Libraries](https://python.langchain.com/docs/modules/data_connection/document_loaders/)
