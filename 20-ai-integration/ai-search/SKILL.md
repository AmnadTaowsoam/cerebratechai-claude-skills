---
name: AI Search
description: AI-powered search using language models and vector embeddings to provide intelligent, contextual search results with semantic understanding.
---

# AI Search

> **Current Level:** Expert (Enterprise Scale)
> **Domain:** AI Integration / Search

---

## Overview

AI-powered search uses language models and vector embeddings to provide more intelligent and contextual search results. Unlike traditional keyword search, AI search understands intent, semantics, and context to deliver more relevant results through semantic understanding, vector similarity, and re-ranking.

---

## 1. Executive Summary & Strategic Necessity

* **Context:** ในปี 2025-2026 AI Search ด้วย ReAct Pattern และ Vector Embeddings ช่วย Semantic Search ที่มีอัตโนมาติการทำงานอัตโนมาติ (Semantic Search) ใน Enterprise Scale

* **Business Impact:** AI Search ช่วยลด Downtime ของระบบ Customer Support ผ่านการตอบคำถามอัตโนมาติการค้นหา (Reduce search failures), ลดต้นทุนการจัดการทำงาน (Increase conversion rates), และปรับประสบทำงาน (Consistent experience)

* **Product Thinking:** AI Search ช่วยแก้ปัญหา (Pain Point) ความต้องการค้นหาข้อมูลที่ซ่อน (Users struggle to find relevant content) ผ่านการทำงานอัตโนมาติ (Semantic understanding of queries)

---

## 2. Technical Deep Dive (The "How-to")

* **Core Logic:** AI Search ใช้ ReAct Pattern และ Vector Embeddings ช่วย Semantic Search ทำงานอัตโนมาติ:
  1. **Query Understanding**: วิเคคิดความต้องการ (Intent classification, Entity extraction, Query expansion)
  2. **Vector Embedding**: แปลงข้อความเป็นเวกเตอร (Text → Vector) สำหรับการค้นหา Semantic similarity
  3. **Hybrid Search**: ผสมกัน Keyword Search และ Vector Search สำหรับการค้นหา Re-ranking
  4. **Re-ranking**: Cross-encoder สำหรับการจัดลำลังผลลัพธ์ผลลัพธ์

* **Architecture Diagram Requirements:** แผนผังระบบ AI Search ต้องมีองค์ประกอบ:
  1. **Query Processing Layer**: และประสบคิดความต้องการ (Query analyzer, Intent classifier, Query expander)
  2. **Embedding Layer**: สำหรับการจัดเก็บ Embeddings ด้วย Vector Database (OpenAI Embeddings, Pinecone)
  3. **Retrieval Layer**: Vector search ด้วย Keyword Search (BM25, Elasticsearch)
  4. **Re-ranking Layer**: Cross-encoder สำหรับการจัดลำลังผลลัพธ์ผลลัพธ์
  5. **LLM Layer**: Language Model สำหรับการจัดลำลังผลลัพธ์ผลลัพธ์
  6. **API Gateway**: REST API ด้วย Rate limiting และ Authentication

* **Implementation Workflow:** ขั้นตอนการนำ AI Search ไปใช้งานจริง:
  1. **Planning Phase**: กำหนด Requirement และเลือก Vector Database
  2. **Data Preparation**: จัดเก็บ Documents และ Generate Embeddings
  3. **Indexing**: Store embeddings ใน Vector Database
  4. **Search Implementation**: สร้าง Search API ด้วย Vector similarity และ Keyword search
  5. **Re-ranking**: เพิ่ม Cross-encoder สำหรับการจัดลำลังผลลัพธ์
  6. **Testing Phase**: Unit test, Integration test, E2E test
  7. **Deployment**: Deploy ด้วย Monitoring และ Load balancing
  8. **Optimization**: Cache embeddings, Tune parameters, Scale horizontally

---

## 3. Tooling & Tech Stack

* **Enterprise Tools:** เครื่องมือระดับอุตสาหกรรมที่เลือกใช้สำหรับ AI Search ใน Enterprise Scale:
  1. **OpenAI**: GPT-4, Embeddings (text-embedding-3-small, text-embedding-3-large)
  2. **Pinecone**: Vector Database สำหรับการจัดเก็บ Embeddings และ Semantic search
  3. **Weaviate**: Vector Database ด้วย Hybrid search และ Filtering
  4. **Cohere**: Embeddings (embed-multilingual-v3.0) และ Rerank API
  5. **Sentence Transformers**: Open-source embeddings (all-MiniLM-L6-v2)
  6. **LangChain**: Framework สำหรับสร้าง AI Agents และ Search integration
  7. **Elasticsearch**: Keyword search ด้วย BM25 algorithm
  8. **Redis**: Cache สำหรับการจัดเก็บ Embeddings และ Search results
  9. **Prometheus**: Monitoring สำหรับ Metrics (Latency, Throughput, Error rate)
  10. **Grafana**: Visualization dashboard สำหรับ Observability

* **Configuration Essentials:** การตั้งค่าสำคัญสำหรับให้ระบบเสถียร AI Search:
  1. **Model Selection**: เลือก Model ตามความต้องการ (GPT-4 สำหรับ Speed vs GPT-3.5-turbo สำหรับ Accuracy)
  2. **Embedding Configuration**: Dimension (768 สำหรับ 3072), Batch size (100), Normalization
  3. **Search Parameters**: Top-K results (k=10-20), Similarity threshold (0.7), Hybrid weights (0.5 keyword, 0.5 vector)
  4. **Cache Configuration**: TTL (3600s), Redis connection pool, Cache hit rate target (>80%)
  5. **Rate Limiting**: Per-user limits (100 requests/minute), Per-endpoint limits (1000 requests/hour)
  6. **Timeout Settings**: Search timeout (5s), Tool timeout (3s), LLM timeout (30s)
  7. **Retry Policy**: Exponential backoff (base: 2, max: 5, jitter: true)
  8. **Monitoring**: Track success rate, latency (p50 < 500ms), error rate (<1%), cache hit rate

---

## 4. Standards, Compliance & Security

* **International Standards:** มาตรฐานที่เกี่ยวข้อง:
  1. **ISO/IEC 27001**: Information Security Management - สำหรับการจัดเก็บ Sensitive Data และ Access Control
  2. **ISO/IEC 27017**: Code of Practice for Information Security Controls - สำหรับ Secure Development
  3. **GDPR**: General Data Protection Regulation - สำหรับการจัดเก็บ Personal Data และ User Consent
  4. **SOC 2 Type II**: Security Controls - สำหรับการ Audit และ Compliance
  5. **OWASP Top 10**: Web Application Security - สำหรับการป้องกัน Prompt Injection และ Data Exposure

* **Security Protocol:** กลไกการป้องกัน AI Search:
  1. **Input Validation**: Validate และ Sanitize ทุก Input ก่อน LLM หรือ Tools (Prevent prompt injection, SQL injection, XSS)
  2. **Output Sanitization**: Filter sensitive information จาก LLM output (PII, Secrets, Internal URLs)
  3. **Tool Permission Model**: RBAC (Role-Based Access Control) สำหรับ Tools - บาง Tools Admin permission, บาง Tools เปิดให้ทุก User
  4. **Audit Trail**: Log ทุก Search query, Tool call, LLM decision, และ Result (สำหรับ Forensics และ Compliance)
  5. **Rate Limiting**: Per-user และ Per-API rate limits สำหรับป้องกัน Abuse (100-1000 requests/hour)
  6. **Secure Communication**: mTLS สำหรับ internal services, TLS 1.3 สำหรับ external APIs
  7. **Secret Rotation**: Rotate API keys ทุก 30-90 วัน (Automated key rotation)
  8. **Sandboxing**: Run Tools ใน isolated environment (Docker containers, Lambda functions)
  9. **Content Filtering**: Block malicious content, Adult content, และ Violations (Content moderation APIs)
  10. **Data Encryption**: Encrypt sensitive data ที่ rest ใน Database (AES-256 หรือ Customer-managed keys)

* **Explainability:** (สำหรับ AI) ความสามารถในการอธิบายผลลัพธ์ผ่านเทคนิค:
  1. **Search Result Scoring**: Explain why results were ranked this way
  2. **Query Expansion**: Show how query was expanded
  3. **Tool Selection**: Justify which tools were used
  4. **Re-ranking Rationale**: Explain why results were re-ordered

---

## 5. Unit Economics & Performance Metrics (KPIs)

* **Cost Calculation:** สูตรการคำนวณต้นทุนต่อหน่วย AI Search:
  1. **Embedding Cost** = (Input Tokens + Output Tokens) × Price per 1K tokens
     - OpenAI text-embedding-3-small: $0.00002/1K tokens
     - OpenAI text-embedding-3-large: $0.00013/1K tokens
     - Cohere embed-multilingual-v3.0: $0.0001/1M tokens
  2. **Vector Search Cost** = $0.001 per query (Pinecone)
  3. **Keyword Search Cost** = $0.0005 per query (Elasticsearch)
  4. **LLM Cost per Request** = (Input Tokens + Output Tokens) × Price per 1K tokens
     - GPT-4: $0.03/1K input + $0.06/1K output
     - GPT-3.5-turbo: $0.001/1K input + $0.002/1K output
  5. **Total Cost per Search** = Embedding Cost + Vector Search Cost + LLM Cost
  6. **Monthly Cost** = (Cost per Search × Searches per Month) + Infrastructure Costs
  7. **Infrastructure Costs** = Compute ($20-100/month) + Storage ($0.023/GB/month) + Monitoring ($10/month) + Vector DB ($70/month)

* **Key Performance Indicators:** ตัวชี้วัดความสำเร็จทางเทคนิค:
  1. **Search Success Rate**: อัตราการสำเร็จของ Search (Target: >95%)
  2. **Average Latency**: เวลาการตอบกลับ (Target: <500ms p95)
  3. **Token Usage per Request**: เฉลี่ย Token เฉลี่ย Request (Target: <2,000 tokens)
  4. **Vector Search Latency**: เวลาการทำงาน Vector Database (Target: <100ms)
  5. **Cache Hit Rate**: อัตราการ Cache hit (Target: >80% สำหรับ repeated queries)
  6. **Re-ranking Accuracy**: เวลาการจัดลำลังผลลัพธ์ผลลัพธ์ (Target: >90% NDCG@10)
  7. **User Satisfaction Score**: 1-5 rating จาก User feedback (Target: >4.0)
  8. **Error Rate**: อัตราการ Error (Target: <1%)
  9. **Concurrent Users**: จำนวยผู้ใช้งานพร้อมกัน (Peak: 1000 concurrent sessions)
  10. **Query Expansion Rate**: อัตราการจำนวย Query expansion (Target: >70%)
  11. **Tool Call Success Rate**: อัตราการสำเร็จของ Tool calls (Target: >98%)

---

## 6. Strategic Recommendations (CTO Insights)

* **Phase Rollout:** คำแนะนำในการทยอยเริ่มใช้งาน AI Search เพื่อลดความสำเร็จทางเทคนิค:
  1. **Phase 1: MVP (1-2 เดือน)**: Deploy Simple AI Search ด้วย 1 Vector Database (Pinecone) และ 1 LLM (GPT-3.5-turbo)
     - **Goal**: Validate AI Search architecture และ gather feedback
     - **Success Criteria**: >90% success rate, <1s latency, >80% cache hit rate
     - **Risk Mitigation**: Rate limiting, Manual review ก่อน Auto-approve
  2. **Phase 2: Beta (2-3 เดือน)**: Expand ด้วย 5-10 Tools และ Memory system (Redis + Vector DB)
     - **Goal**: Test scalability และ Tool reliability
     - **Success Criteria**: >95% success rate, <5s latency, >90% cache hit rate
     - **Risk Mitigation**: Canary deployment, Feature flags, Gradual rollout
  3. **Phase 3: GA (3-6 เดือน)**: Full rollout ด้วย 10-20 Tools, Advanced Memory, Re-ranking
     - **Goal**: Enterprise-grade reliability และ Performance
     - **Success Criteria**: >95% success rate, <3s latency, >90% cache hit rate, 99.9% uptime
     - **Risk Mitigation**: Load testing, Blue-green deployment, Disaster recovery

* **Pitfalls to Avoid:** ข้อควรระวังที่มักจะผิดพลาดในระดับ Enterprise Scale:
  1. **Over-engineering**: สร้าง Search ที่ซ้อนเกินไป (Too many tools, Complex memory) → เริ่มจาก Simple และ iterate
  2. **No Rate Limiting**: ไม่มี Rate limits ทำให้ Cost blowout และ API abuse → Implement per-user และ per-endpoint limits ด้วย Redis
  3. **Infinite Loops**: Agent วนลูปไม่มีทางออก (Max iterations = ∞) → Set max_iterations=10 และ timeout=60s
  4. **Ignoring Tool Errors**: Tool failures crash Agent → Wrap Tools ด้วย try-catch และ return fallback response
  5. **No Context Management**: ส่งทุก message เป็น Independent → Implement sliding window และ summary
  6. **Hardcoding API Keys**: Keys ใน code ที่เปิดให้ Public → Use Environment variables หรือ Secret Manager
  7. **No Observability**: ไม่มี Logging/Tracing → Add structured logging ด้วย correlation IDs
  8. **Skipping Validation**: ไม่ Validate Tool inputs/outputs → Implement schema validation และ sanitization
  9. **Poor Prompt Design**: Vague prompts ทำให้ Agent hallucinate → Use specific, testable prompts ด้วย examples
  10. **Single Point of Failure**: ไม่มี Redundancy หรือ Fallback → Deploy multiple instances ด้วย Load balancer

---

## Core Concepts

### 1. AI Search Concepts

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
- **Hybrid Search**: Combines approaches
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
- **Example**: "How to learn programming?"
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
- **OpenAI**: text-embedding-ada-002, text-embedding-3-small, text-embedding-3-large
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
```

### Vector Database

```python
# Chroma Vector Store
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

# Create embeddings
embeddings = OpenAIEmbeddings()

# Create vector store
vectorstore = Chroma.from_texts(
    texts=["text 1", "text 2", "text 3", "text 4", "text 5"],
    embedding=embeddings,
)

# Search
query = "What is neural network?"
results = vectorstore.similarity_search(query, k=3)

for doc, score in results:
    print(f"Score: {score:.4f}")
    print(f"Content: {doc.page_content}")
```
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
│  Search      │   Search        │
└─────────────┴─────────────┘
    ↓
    ↓
┌──────────────────────────────────────┐
│      Combined & Reranked Results    │
└──────────────────────────────────────┘
    ↓
    ↓
┌──────────────────────────────────────┐
│      Personalized Results             │
└──────────────────────────────────────┘
```
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
    texts=["text 1", "text 2", "text 3", "text 4", "text 5"],
    embedding=embeddings,
)

# Create retrievers
keyword_retriever = BM25Retriever.from_texts(
    texts=["text 1", "text 2", "text 3", "text 4", "text 5"]
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
```
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
    input="Search query about machine learning",
    model="text--embedding-ada-002"
)

embeddings = response.data[0].embedding
print(f"Embedding dimensions: {len(embeddings)}")

# Batch embeddings
texts = ["text 1", "text 2", "text 3", "text 4", "text 5"]
response = client.embeddings.create(
    input=texts,
    model="text-embedding-ada-002"
)

for i, embedding in enumerate(response.data):
    print(f"Text {i}: {len(embedding)} dimensions")
```

### HuggingFace Embeddings

```python
# HuggingFace Embeddings
from sentence_transformers import SentenceTransformer

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings
embeddings = model.encode(["text 1", "text 2", "text 3"])

print(f"Embeddings shape: {embeddings.shape}")
```

### Cohere Embeddings

```python
# Cohere Embeddings
import cohere

co = cohere.Client(api_key="your-api-key")

# Generate embeddings
response = cohere.embed(
    texts=["text 1", "text 2", "text 3"],
    model='embed-multilingual-v3.0'
)

embeddings = response.embeddings
print(f"Embeddings shape: {embeddings.shape}")
```
```

---

## 5. Re-ranking

### Cross-Encoder Re-ranking

```python
# Cross-Encoder Re-ranking
from sentence_transformers import CrossEncoder

# Load cross-encoder
cross_encoder = CrossEncoder('ms-marco-MiniLM-L-6-v2')

# Re-rank results
def rerank_results(query: str, results: list, top_k: int = 10):
    # Create query-result pairs
    pairs = [[query, doc.page_content] for doc in results[:top_k]]
    
    # Score all pairs
    scores = cross_encoder.predict(pairs)
    
    # Sort by score
    ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    
    # Return ranked results
    return [results[i] for i in ranked_indices]
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
  const [suggestions, setSuggestions] = useState<string[]>([])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!query.trim()) return
    
    onSearch(query)
    setQuery('')
    setSuggestions([])
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="search-container">
      <input
        type="text"
        value={query}
        onChange={e => setQuery(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={placeholder || "Search..."}
        className="search-input"
      />
      <button type="submit" disabled={!query.trim()}>
        Search
      </button>
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
    </form>
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
      [facet]: [value]
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
                  onChange={(e) => handleFacetChange(facet.name, option.value)}
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

  const filteredSuggestions = suggestions.filter(s =>
    s.toLowerCase().includes(input.toLowerCase())
  )

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'ArrowDown') {
      e.preventDefault()
      setSelectedIndex((prev) => (prev + 1) % filteredSuggestions.length))
    } else if (e.key === 'ArrowUp') {
      e.preventDefault()
      setSelectedIndex((prev) => (prev - 1 + filteredSuggestions.length) % filteredSuggestions.length))
    } else if (e.key === 'Enter') {
      e.preventDefault()
      if (selectedIndex >= 0) {
        onSelect(filteredSuggestions[selectedIndex])
      setInput('')
        setIsOpen(false)
        setSelectedIndex(-1)
      }
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
                setSelectedIndex(-1)
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
  type: 'search' | 'click' | 'error' | 'filter'
  userId?: string
  sessionId: string
  data?: any
}

class SearchAnalytics {
  private events: SearchEvent[] = []

  track(event: SearchEvent): void {
    event.timestamp = new Date()
    this.events.push(event)
    this.sendToAnalytics(event)
  }

  trackClick(resultId: string): void {
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
    const searches = this.events.filter(e => e.type === 'search')
    const clicks = searches.filter(e => e.clickedResult !== undefined)
    
    return {
      totalSearches: searches.length,
      averageResults: searches.reduce((sum, e) => sum + (e.data?.resultsCount || 0), 0) / searches.length,
      clickThroughRate: clicks.length / searches.length,
    }
  }

  private sendToAnalytics(event: SearchEvent): void {
    // Send to your analytics service
    fetch('/api/analytics/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(event),
    }).catch(error => {
      console.error('Analytics error:', error)
      })
  }
}

// Usage
const analytics = new SearchAnalytics()

// Track search
analytics.track({
  type: 'search',
  userId: 'user-123',
  sessionId: 'session-123',
  data: { query: 'machine learning', filters: { category: 'tutorials' }
})

// Track click
analytics.trackClick('result-123')
```

---

## 10. Performance Optimization

### Caching Strategies

```python
# Search Result Caching
import hashlib
import json
import time
import redis

class SearchCache:
    def __init__(self):
        self.cache: dict = {}
        self.ttl = 3600  # 1 hour

    def get_cache_key(self, query: str, filters: dict) -> str:
        cache_data = {
            'query': query,
            'filters': json.dumps(filters, sort_keys=True),
        }
        return hashlib.md5(json.dumps(cache_data)).hexdigest()

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
    cache.set('search query', results)
```

### Query Optimization

```python
# Query Optimization
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Create optimization prompt
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
query = "best restaurants San Francisco Italian"
optimized = chain.run(query)
print(optimized)
```
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
vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
)

# Create retrieval chain
qa = RetrievalQA.from_chain_type(
    llm=client,
    retriever=vectorstore.as_retriever(),
    return_source_documents=True,
    verbose=True
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

# Create vector store
vectorstore = Chroma.from_texts(
    texts=["text 1", "text 2", "text 3", "text 4", "text 5"],
    embedding=embeddings,
)

# Create retrievers
keyword_retriever = BM25Retriever.from_texts(
    texts=["text 1", "text 2", "text 3", "text 4", "text 5"]
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
```
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
- Implement rate limiting

## 5. Enable Exploration
- Provide suggestions
- Show related topics
- Enable filtering and sorting
- Support faceted navigation

## 6. Learn from Users
- Track search behavior
- Analyze click patterns
- Personalize results
- Improve based on feedback

## 7. Handle Errors Gracefully
- Provide helpful error messages
- Suggest alternatives
- Log errors for debugging
- Fallback to basic search

## 8. Test Thoroughly
- Test with various queries
- Test edge cases
- Test performance
- Test with real users

## 9. Iterate and Improve
- Monitor search metrics
- Analyze user feedback
- Make incremental improvements
- Stay updated with best practices
```

---

## Quick Start

### Basic AI Search with Vector Embeddings

```python
from openai import OpenAI
import numpy as np
from typing import List, Dict

client = OpenAI(api_key="your-api-key")

# 1. Create embeddings for documents
documents = [
    "Python is a high-level programming language",
    "JavaScript is used for web development",
    "TypeScript adds static typing to JavaScript",
    "React is a JavaScript library for building UIs",
]

def create_embeddings(texts: List[str]) -> List[List[float]]:
    response = client.embeddings.create(
        input=texts,
        model="text-embedding-ada-002"
    )
    return [item.embedding for item in response.data]

document_embeddings = create_embeddings(documents)

# 2. Store embeddings
document_data = [
    {
        "id": i,
        "text": documents[i],
        "embedding": document_embeddings[i]
    }
    for i in range(len(documents))
]

# 3. Search function
def search(query: str, top_k: int = 3) -> List[Dict]:
    # Create query embedding
    query_embedding = create_embeddings([query])[0]
    
    # Calculate similarities
    similarities = []
    for doc in document_data:
        similarity = np.dot(query_embedding, doc["embedding"])
        similarities.append((doc["id"], similarity))
    
    # Sort by similarity
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    # Return top results
    return [
        {
            "id": doc_id,
            "text": doc["text"],
            "score": float(similarity)
        }
        for doc_id, similarity in similarities[:top_k]
    ]

# 4. Use search
results = search("What is Python?", top_k=3)
for result in results:
    print(f"{result['text']} (score: {result['score']:.2f})")
```

### Installation

```bash
pip install openai langchain numpy
export OPENAI_API_KEY="your-api-key"
```

### Next Steps

1. Add more documents to index
2. Implement caching for embeddings
3. Add error handling and fallbacks
4. Set up monitoring and logging
```

---

## Production Checklist

- [ ] **Embedding Model**: Choose appropriate embedding model (OpenAI, Cohere, etc.)
- [ ] **Vector Database**: Use vector DB for large-scale search (Pinecone, Weaviate)
- [ ] **Hybrid Search**: Combine vector search with keyword search
- [ ] **Re-ranking**: Implement re-ranking for better results
- [ ] **Caching**: Cache embeddings and frequent queries
- [ ] **Rate Limiting**: Limit API calls to embedding service
- [ ] **Error Handling**: Handle API failures gracefully
- [ ] **Monitoring**: Track search quality, latency, costs
- [ ] **A/B Testing**: Test different models and strategies
- [ ] **Query Preprocessing**: Normalize and clean queries
- [ ] **Result Filtering**: Filter results by relevance threshold
- [ ] **Fallback**: Fallback to keyword search if vector search fails
- [ ] **Logging**: Track all search operations for debugging
- [ ] **Cost Tracking**: Monitor API costs per search

---

## Anti-patterns

### ❌ Don't: No Query Preprocessing

```python
# ❌ Bad - Raw query
def search(query: str):
    embedding = create_embedding(query)  # May have typos, extra spaces
    return vector_search(embedding)
```

```python
# ✅ Good - Preprocess query
def search(query: str):
    # Normalize
    query = query.strip().lower()
    
    # Remove stop words (optional)
    # query = remove_stop_words(query)
    
    embedding = create_embedding(query)
    return vector_search(embedding)
```

### ❌ Don't: No Result Filtering

```python
# ❌ Bad - Returns all results
def search(query: str, min_score: float = 0.7):
    results = vector_search(query_embedding)
    return results  # May include irrelevant results
```

```python
# ✅ Good - Filter by relevance threshold
def search(query: str, min_score: float = 0.7):
    results = vector_search(query_embedding)
    filtered = [r for r in results if r['score'] >= min_score]
    return filtered
```

### ❌ Don't: No Caching

```python
# ❌ Bad - Recomputes embeddings every time
def search(query: str):
    embedding = create_embedding(query)  # Expensive API call!
    return vector_search(embedding)
```

```python
# ✅ Good - Cache embeddings
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_embedding(text: str):
    return create_embedding(text)

def search(query: str):
    embedding = get_embedding(query)  # Cached!
    return vector_search(embedding)
```

### ❌ Don't: No Fallback Strategy

```python
# ❌ Bad - Fails if vector search fails
def search(query: str):
    try:
        return vector_search(query)
    except Exception as e:
        logger.error(f"Vector search failed: {e}")
        return keyword_search(query)  # No fallback
```

```python
# ✅ Good - Fallback to keyword search
def search(query: str):
    try:
        return vector_search(query)
    except Exception as e:
        logger.error(f"Vector search failed: {e}")
        return keyword_search(query)  # Fallback
```

---

## Integration Points

- **Vector Search** (`06-ai-ml-production/vector-search/`) - Vector search implementation
- **Embedding Models** (`06-ai-ml-production/embedding-models/`) - Embedding model selection
- **RAG Implementation** (`06-ai-ml-production/rag-implementation/`) - Adding knowledge retrieval
- **LLM Integration** (`06-ai-ml-production/llm-integration/`) - LLM API setup
- **Error Handling** (`03-backend-api/error-handling/`) - Error patterns

---

## Further Reading

- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings/)
- [Vector Search Best Practices](https://www.pinecone.io/learn/vector-search-best-practices/)
- [Semantic Search Guide](https://www.algolia.com/blog/ai/what-is-semantic-search/)
- [Hybrid Search Patterns](https://www.algolia.com/blog/hybrid-search/)
- [LangChain Documentation](https://python.langchain.com/docs/modules/agents/)
