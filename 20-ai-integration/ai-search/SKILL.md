# AI Search

## Overview

AI-powered search uses language models and vector embeddings to provide more intelligent and contextual search results.

---

## 1. AI Search Concepts

### Traditional vs AI Search

```markdown
# Traditional vs AI Search

## Traditional Search
- **Keyword Matching**: Exact or partial matches
- **Boolean Logic**: AND, OR, NOT operators
- **Ranking**: PageRank, backlinks
- **Limitations**: Limited semantic understanding

## AI Search
- **Semantic Understanding**: Understands meaning
- **Context Awareness**: Considers user intent
- **Vector Similarity**: Finds related content
- **Natural Language**: Conversational queries
- **Personalization**: Learns from user behavior

## When to Use AI Search
- **Complex Queries**: Multi-part questions
- **Ambiguous Queries**: Unclear intent
- **Exploratory Search**: Discovering information
- **Domain-Specific**: Specialized knowledge
- **Conversational**: Follow-up questions
```

### Search Types

```markdown
# Search Types

## Keyword Search
- **Use Case**: Finding specific information
- **Example**: "Python programming tutorial"
- **Best For**: Precise queries

## Semantic Search
- **Use Case**: Finding related information
- **Example**: "How to learn programming"
- **Best For**: Exploratory queries

## Conversational Search
- **Use Case**: Multi-turn conversations
- **Example**: "What is Python?" → "How do I install it?"
- **Best For**: Complex tasks

## Hybrid Search
- **Use Case**: Combining approaches
- **Example**: "Python tutorial for beginners"
- **Best For**: Most use cases
```

---

## 2. Semantic Search

### Vector Embeddings

```markdown
# Vector Embeddings

## What are Embeddings?
Vector representations of text that capture semantic meaning.

## How They Work
1. **Text Processing**: Tokenize and process text
2. **Vector Generation**: Convert to numerical vectors
3. **Similarity**: Similar concepts have similar vectors
4. **Search**: Find similar vectors for queries

## Common Models
- **OpenAI**: text-embedding-ada-002, text-embedding-3-small
- **Sentence Transformers**: all-MiniLM-L6-v2
- **Cohere**: embed-multilingual-v3.0
- **HuggingFace**: Various models available

## Vector Dimensions
- **Small**: 256-384 dimensions
- **Medium**: 768-1024 dimensions
- **Large**: 1536-3072 dimensions

## Trade-offs
- **Higher Dimensions**: Better accuracy, more storage
- **Lower Dimensions**: Faster, less storage
```

### Embedding Implementation

```python
# OpenAI Embeddings
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

# Generate embeddings
response = client.embeddings.create(
    input="Search query about machine learning",
    model="text-embedding-ada-002"
)

embeddings = response.data[0].embedding
print(f"Embedding dimensions: {len(embeddings)}")

# Batch embeddings
texts = [
    "Machine learning is a subset of artificial intelligence",
    "Deep learning uses neural networks",
    "Natural language processing deals with text"
]

response = client.embeddings.create(
    input=texts,
    model="text-embedding-ada-002"
)

for i, embedding in enumerate(response.data):
    print(f"Text {i}: {texts[i]}")
    print(f"Embedding dimensions: {len(embedding)}")
```

### Vector Database

```python
# Chroma Vector Store
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.documents import Document

# Create embeddings
embeddings = OpenAIEmbeddings()

# Create documents
documents = [
    Document(page_content="Machine learning introduction", metadata={"source": "ml-guide"}),
    Document(page_content="Deep learning with neural networks", metadata={"source": "dl-guide"}),
    Document(page_content="Natural language processing basics", metadata={"source": "nlp-guide"}),
]

# Create text splitter
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

# Create vector store
vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    text_splitter=text_splitter
)

# Search
query = "What is neural network?"
results = vectorstore.similarity_search(query, k=3)

for doc, score in results:
    print(f"Score: {score:.4f}")
    print(f"Content: {doc.page_content}")
    print(f"Source: {doc.metadata['source']}")
    print("---")
```

---

## 3. Hybrid Search (Keyword + Semantic)

### Hybrid Search Architecture

```markdown
# Hybrid Search Architecture

## Components
1. **Keyword Search**: Traditional keyword matching
2. **Semantic Search**: Vector similarity search
3. **Ranking**: Combine and rerank results
4. **Personalization**: Learn from user behavior

## Flow
```
User Query
    ↓
┌─────────────┴─────────────┐
│  Keyword    │   Semantic      │
│  Search     │   Search        │
└─────────────┴─────────────┘
    ↓
    ↓
┌──────────────────────────────┐
│   Combined & Reranked    │
└──────────────────────────────┘
    ↓
    ↓
┌──────────────────────────────┐
│   Personalized Results    │
└──────────────────────────────┘
```

### Implementation

```python
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

# Create embeddings
embeddings = OpenAIEmbeddings()

# Create vector store
vectorstore = Chroma.from_texts(
    texts=["text1", "text2", "text3", "text4", "text5"],
    embedding=embeddings,
    metadatas=[{"source": "db"}, {"source": "api"}, {"source": "docs"}]
)

# Create retrievers
keyword_retriever = BM25Retriever.from_texts(
    texts=["text1", "text2", "text3", "text4", "text5"]
)

vector_retriever = vectorstore.as_retriever()

# Create ensemble retriever
retriever = EnsembleRetriever(
    retrievers=[keyword_retriever, vector_retriever],
    weights=[0.5, 0.5]
)

# Search
query = "search query"
results = retriever.get_relevant_documents(query)

for doc in results:
    print(f"Content: {doc.page_content}")
    print(f"Source: {doc.metadata}")
    print("---")
```

---

## 4. Vector Embeddings

### OpenAI Embeddings

```python
# OpenAI Embeddings
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

# Text embedding
response = client.embeddings.create(
    input="Your text here",
    model="text-embedding-ada-002"
)

embedding = response.data[0].embedding
print(f"Dimensions: {len(embedding)}")

# Batch embeddings
inputs = ["text 1", "text 2", "text 3"]
response = client.embeddings.create(
    input=inputs,
    model="text-embedding-ada-002"
)

for i, data in enumerate(response.data):
    print(f"Text {i}: {inputs[i]}")
    print(f"Embedding dimensions: {len(data.embedding)}")
```

### HuggingFace Embeddings

```python
# HuggingFace Embeddings
from sentence_transformers import SentenceTransformer

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings
embeddings = model.encode(["text 1", "text 2", "text 3"])

for i, embedding in enumerate(embeddings):
    print(f"Text {i}: dimensions {len(embedding)}")
```

### Cohere Embeddings

```python
# Cohere Embeddings
import cohere

co = cohere.Client(api_key="your-api-key")

# Generate embeddings
response = co.embed(
    texts=["text 1", "text 2", "text 3"],
    model='embed-multilingual-v3.0'
)

for i, embedding in enumerate(response.embeddings):
    print(f"Text {i}: dimensions {len(embedding)}")
```

---

## 5. Re-ranking

### Re-ranking Strategies

```markdown
# Re-ranking Strategies

## Cross-Encoder Re-ranking
- **Concept**: Use a cross-encoder to rerank results
- **Benefits**: Better relevance
- **Implementation**: Use ColBERT or similar

## Learning to Rank
- **Concept**: Learn ranking from user feedback
- **Benefits**: Personalized results
- **Implementation**: Use user clicks as labels

## Diversity-Based Reranking
- **Concept**: Ensure diverse results
- **Benefits**: Better coverage
- **Implementation**: Use clustering

## Time-Based Reranking
- **Concept**: Prioritize recent content
- **Benefits**: Fresh information
- **Implementation**: Use timestamps
```

### Cross-Encoder Implementation

```python
from sentence_transformers import CrossEncoder
from langchain.retrievers import ContextualCompressionRetriever

# Load cross-encoder
encoder = CrossEncoder('ms-marco-MiniLM-L-6-v2')

# Create retriever with compression
retriever = ContextualCompressionRetriver(
    base_compressor=encoder,
    base_retriever=vectorstore.as_retriever(),
    k_query=10
)

# Search
query = "search query"
results = retriever.get_relevant_documents(query)

for i, doc in enumerate(results):
    print(f"Rank {i}: {doc.page_content}")
```

---

## 6. Query Understanding

### Query Analysis

```python
# Query Analysis with LLM
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate

# Create query analysis prompt
query_analysis_prompt = PromptTemplate.from_template(
    """Analyze the following search query and extract:
1. Main topic
2. Specific details needed
3. Intent (informational, navigational, transactional)
4. Key terms

Query: {query}

Analysis:"""
)

# Create chain
chain = ConversationChain(
    llm=llm,
    prompt=query_analysis_prompt,
    verbose=True
)

# Analyze query
query = "best restaurants in San Francisco for Italian food"
analysis = chain.run(query)
print(analysis)
```

### Query Expansion

```python
# Query Expansion
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Create expansion prompt
expansion_prompt = PromptTemplate.from_template(
    """Expand the following search query with related terms and synonyms:

Query: {query}

Related terms:"""
)

# Create chain
chain = LLMChain(
    llm=llm,
    prompt=expansion_prompt,
    verbose=True
)

# Expand query
query = "machine learning"
expansion = chain.run(query)
print(expansion)
```

---

## 7. Search UI Patterns

### Search Input Component

```typescript
// Search Input Component
'use client'

import { useState } from 'react'

interface SearchInputProps {
  onSearch: (query: string) => void
  placeholder?: string
}

export default function SearchInput({ onSearch, placeholder }: SearchInputProps) {
  const [query, setQuery] = useState('')
  const [isFocused, setIsFocused] = useState(false)
  const [suggestions, setSuggestions] = useState<string[]>([])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (query.trim()) {
      onSearch(query)
      setQuery('')
      setSuggestions([])
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      handleSubmit(e)
    }
  }

  return (
    <div className="search-container">
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={query}
          onChange={e => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder || "Search..."}
          className="search-input"
        />
        <button type="submit" className="search-button">
          Search
        </button>
      </form>
      {suggestions.length > 0 && (
        <div className="suggestions">
          {suggestions.map((suggestion, index) => (
            <div
              key={index}
              className="suggestion-item"
              onClick={() => {
                setQuery(suggestion)
                setSuggestions([])
                onSearch(suggestion)
              }}
            >
              {suggestion}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
```

### Results Display Component

```typescript
// Search Results Component
interface SearchResult {
  id: string
  title: string
  snippet: string
  url: string
  score?: number
}

interface SearchResultsProps {
  results: SearchResult[]
  onResultClick?: (result: SearchResult) => void
}

export default function SearchResults({ results, onResultClick }: SearchResultsProps) {
  if (results.length === 0) {
    return <div className="no-results">No results found</div>
  }

  return (
    <div className="search-results">
      {results.map((result, index) => (
        <div
          key={result.id}
          className="result-item"
          onClick={() => onResultClick?.(result)}
        >
          <h3 className="result-title">{result.title}</h3>
          <p className="result-snippet">{result.snippet}</p>
          <a href={result.url} className="result-link" target="_blank">
            {result.url}
          </a>
          {result.score && (
            <div className="result-score">
              Score: {result.score.toFixed(2)}
            </div>
          )}
        </div>
      ))}
    </div>
  )
}
```

### Faceted Search

```typescript
// Faceted Search Component
interface Facet {
  name: string
  options: { value: string; count: number }[]
}

interface FacetedSearchProps {
  facets: Facet[]
  results: SearchResult[]
  onFacetChange: (facet: string, value: string) => void
}

export default function FacetedSearch({ facets, results, onFacetChange }: FacetedSearchProps) {
  const [selectedFacets, setSelectedFacets] = useState<Record<string, string[]>>({})

  const handleFacetChange = (facet: string, value: string) => {
    setSelectedFacets(prev => ({
      ...prev,
      [facet]: [value],
    }))
    onFacetChange(facet, value)
  }

  const filteredResults = results.filter(result => {
    return Object.entries(selectedFacets).every(([facet, values]) =>
      values.includes(result[facet as keyof SearchResult])
    )
  })

  return (
    <div className="faceted-search">
      <aside className="facets">
        {facets.map(facet => (
          <div key={facet.name} className="facet">
            <h3>{facet.name}</h3>
            {facet.options.map(option => (
              <label key={option.value}>
                <input
                  type="checkbox"
                  checked={selectedFacets[facet.name]?.includes(option.value)}
                  onChange={() => handleFacetChange(facet.name, option.value)}
                />
                {option.value} ({option.count})
              </label>
            ))}
          </div>
        ))}
      </aside>
      <div className="results">
        <SearchResults results={filteredResults} />
      </div>
    </div>
  )
}
```

---

## 8. Autocomplete and Suggestions

### Autocomplete Component

```typescript
// Autocomplete Component
'use client'

import { useState, useEffect, useRef } from 'react'

interface AutocompleteProps {
  suggestions: string[]
  onSelect: (suggestion: string) => void
}

export default function Autocomplete({ suggestions, onSelect }: AutocompleteProps) {
  const [input, setInput] = useState('')
  const [isOpen, setIsOpen] = useState(false)
  const [selectedIndex, setSelectedIndex] = useState(-1)
  const containerRef = useRef<HTMLDivElement>(null)

  const filteredSuggestions = suggestions.filter(s =>
    s.toLowerCase().includes(input.toLowerCase())
  )

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
        setIsOpen(false)
        setSelectedIndex(-1)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [suggestions])

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'ArrowDown') {
      e.preventDefault()
      setSelectedIndex(prev => (prev + 1) % filteredSuggestions.length)
    } else if (e.key === 'ArrowUp') {
      e.preventDefault()
      setSelectedIndex(prev => (prev - 1 + filteredSuggestions.length) % filteredSuggestions.length)
    } else if (e.key === 'Enter') {
      e.preventDefault()
      if (selectedIndex >= 0) {
        onSelect(filteredSuggestions[selectedIndex])
      }
      setInput('')
      setIsOpen(false)
      setSelectedIndex(-1)
    } else if (e.key === 'Escape') {
      setIsOpen(false)
      setSelectedIndex(-1)
    }
  }

  return (
    <div ref={containerRef} className="autocomplete">
      <input
        type="text"
        value={input}
        onChange={e => {
          setInput(e.target.value)
          setIsOpen(true)
        }}
        onKeyDown={handleKeyDown}
        placeholder="Type to search..."
        className="autocomplete-input"
      />
      {isOpen && filteredSuggestions.length > 0 && (
        <ul className="suggestions-list">
          {filteredSuggestions.map((suggestion, index) => (
            <li
              key={index}
              className={`suggestion-item ${index === selectedIndex ? 'selected' : ''}`}
              onClick={() => {
                onSelect(suggestion)
                setInput(suggestion)
                setIsOpen(false)
              }}
            >
              {suggestion}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
```

---

## 9. Search Analytics

### Search Analytics Implementation

```typescript
// Search Analytics
interface SearchEvent {
  query: string
  resultsCount: number
  clickedResult?: string
  timeToFirstClick?: number
  filters?: Record<string, string[]>
}

class SearchAnalytics {
  private events: SearchEvent[] = []

  trackSearch(event: SearchEvent): void {
    this.events.push({
      ...event,
      timestamp: new Date(),
    })

    // Send to analytics
    this.sendToAnalytics(event)
  }

  trackResultClick(resultId: string): void {
    const lastEvent = this.events[this.events.length - 1]
    if (lastEvent) {
      lastEvent.clickedResult = resultId
      this.sendToAnalytics(lastEvent)
    }
  }

  getSearchMetrics(): {
    totalSearches: number
    averageResults: number
    clickThroughRate: number
  } {
    const searches = this.events.filter(e => e.query)
    const clicks = searches.filter(e => e.clickedResult)

    return {
      totalSearches: searches.length,
      averageResults: searches.reduce((sum, e) => sum + e.resultsCount, 0) / searches.length,
      clickThroughRate: clicks.length / searches.length,
    }
  }

  private sendToAnalytics(event: SearchEvent): void {
    // Send to your analytics service
    fetch('/api/analytics/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(event),
    })
      .catch(error => {
        console.error('Analytics error:', error)
      })
  }
}

// Usage
const analytics = new SearchAnalytics()

// Track search
analytics.trackSearch({
  query: 'machine learning',
  resultsCount: 10,
  filters: { category: 'tutorials', level: 'beginner' },
})

// Track result click
analytics.trackResultClick('result-123')
```

---

## 10. Performance Optimization

### Caching Strategies

```python
# Search Result Caching
import hashlib
import json
import time

class SearchCache:
    def __init__(self):
        self.cache: dict = {}
        self.ttl = 3600  # 1 hour

    def get_cache_key(self, query: str, filters: dict) -> str:
        cache_data = {
            'query': query,
            'filters': json.dumps(filters, sort_keys=True),
        }
        return hashlib.md5(json.dumps(cache_data).hexdigest()

    def get(self, query: str, filters: dict):
        key = self.get_cache_key(query, filters)
        
        if key in self.cache:
            cached = self.cache[key]
            if time.time() - cached['timestamp'] < self.ttl:
                return cached['results']
        
        return None

    def set(self, query: str, results: list, filters: dict):
        key = self.get_cache_key(query, filters)
        
        self.cache[key] = {
            'results': results,
            'timestamp': time.time(),
        }
        }

    def invalidate(self, query: str, filters: dict):
        key = self.get_cache_key(query, filters)
        if key in self.cache:
            del self.cache[key]

# Usage
cache = SearchCache()

# Try cache first
results = cache.get('search query', {})

if results is None:
    # Perform search
    results = perform_search('search query', {})
    cache.set('search query', results, {})
```

### Query Optimization

```python
# Query Optimization
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Create query optimization prompt
optimization_prompt = PromptTemplate.from_template(
    """Optimize the following search query for better results:

Original query: {query}

Optimized query:"""
)

# Create chain
chain = LLMChain(
    llm=llm,
    prompt=optimization_prompt,
    verbose=True
)

# Optimize query
query = "best restaurants San Francisco"
optimized = chain.run(query)
print(optimized)
```

---

## 11. Implementation Examples

### OpenAI + Vector Search

```python
# OpenAI + Vector Search Example
from openai import OpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA

# Initialize
client = OpenAI(api_key="your-api-key")
embeddings = OpenAIEmbeddings()

# Create documents
documents = [
    "Python is a high-level programming language",
    "JavaScript is used for web development",
    "TypeScript adds static typing to JavaScript",
    "React is a JavaScript library for building UIs",
]

# Create vector store
vectorstore = Chroma.from_texts(
    texts=documents,
    embedding=embeddings,
)

# Create retrieval chain
qa = RetrievalQA.from_chain_type(
    llm=client,
    retriever=vectorstore.as_retriever(),
    return_source_documents=True,
)

# Search
query = "What is React?"
response = qa.run(query)
print(response)
```

### Hybrid Search Example

```python
# Hybrid Search Example
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

# Initialize
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_texts(
    texts=["text 1", "text 2", "text 3", "text 4"],
    embedding=embeddings,
)

# Create retrievers
keyword_retriever = BM25Retriever.from_texts(
    texts=["text 1", "text 2", "text 3", "text 4"],
)

vector_retriever = vectorstore.as_retriever()

# Create ensemble retriever
retriever = EnsembleRetriever(
    retrievers=[keyword_retriever, vector_retriever],
    weights=[0.5, 0.5]
)

# Search
query = "search query"
results = retriever.get_relevant_documents(query)

for doc, score in results:
    print(f"Document: {doc.page_content}")
    print(f"Score: {score}")
    print("---")
```

---

## 12. Best Practices

### Search Best Practices

```markdown
# Search Best Practices

## 1. Understand User Intent
- Analyze query meaning
- Consider context
- Handle ambiguity
- Ask clarifying questions

## 2. Provide Relevant Results
- Focus on user's actual need
- Prioritize quality over quantity
- Consider user's expertise level

## 3. Handle Edge Cases
- No results: Provide helpful suggestions
- Too many results: Use pagination
- Ambiguous queries: Ask for clarification
- Technical terms: Provide explanations

## 4. Optimize Performance
- Use caching
- Optimize queries
- Use appropriate models
- Monitor performance

## 5. Provide Context
- Show search context
- Highlight matched terms
- Provide result snippets
- Show related results

## 6. Enable Exploration
- Provide suggestions
- Show related topics
- Enable filtering and sorting
- Support faceted navigation

## 7. Learn from Users
- Track search behavior
- Analyze click patterns
- Improve based on feedback
- Personalize results

## 8. Handle Errors Gracefully
- Provide helpful error messages
- Suggest alternatives
- Log errors for debugging
- Fallback to basic search

## 9. Test Thoroughly
- Test with various queries
- Test edge cases
- Test performance
- Test with real users

## 10. Iterate and Improve
- Monitor search metrics
- Analyze user feedback
- Make incremental improvements
- Stay updated with best practices
```
