---
name: Retrieval Quality
description: Comprehensive guide to improving RAG retrieval quality including chunking strategies, embedding optimization, reranking, and hybrid search
---

# Retrieval Quality

## Why Retrieval Quality Matters

**RAG Pipeline:** Retrieval → Generation

```
Bad retrieval → Irrelevant context → Wrong answer
Good retrieval → Relevant context → Correct answer
```

---

## Chunking Strategies

### Fixed-Size Chunking
```python
def chunk_fixed_size(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap  # Overlap for context
    
    return chunks

chunks = chunk_fixed_size(document, chunk_size=500, overlap=50)
```

### Semantic Chunking
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " ", ""]  # Try these in order
)

chunks = splitter.split_text(document)
```

### Sentence-Based Chunking
```python
import nltk

def chunk_by_sentences(text, sentences_per_chunk=5):
    sentences = nltk.sent_tokenize(text)
    chunks = []
    
    for i in range(0, len(sentences), sentences_per_chunk):
        chunk = " ".join(sentences[i:i+sentences_per_chunk])
        chunks.append(chunk)
    
    return chunks
```

---

## Embedding Optimization

### Choose Right Model
```python
from sentence_transformers import SentenceTransformer

# General purpose
model = SentenceTransformer('all-MiniLM-L6-v2')

# Better quality (larger)
model = SentenceTransformer('all-mpnet-base-v2')

# Domain-specific (legal)
model = SentenceTransformer('nlpaueb/legal-bert-base-uncased')
```

### Fine-Tune Embeddings
```python
from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader

# Prepare training data
train_examples = [
    InputExample(texts=['query1', 'relevant_doc1'], label=1.0),
    InputExample(texts=['query1', 'irrelevant_doc'], label=0.0),
]

# Fine-tune
model = SentenceTransformer('all-MiniLM-L6-v2')
train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16)
train_loss = losses.CosineSimilarityLoss(model)

model.fit(
    train_objectives=[(train_dataloader, train_loss)],
    epochs=1
)
```

---

## Hybrid Search

### Combine Dense + Sparse
```python
from rank_bm25 import BM25Okapi

class HybridSearch:
    def __init__(self, documents):
        self.documents = documents
        
        # Dense (embeddings)
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.doc_embeddings = self.embedder.encode(documents)
        
        # Sparse (BM25)
        tokenized_docs = [doc.split() for doc in documents]
        self.bm25 = BM25Okapi(tokenized_docs)
    
    def search(self, query, top_k=5, alpha=0.5):
        # Dense search
        query_emb = self.embedder.encode(query)
        dense_scores = cosine_similarity([query_emb], self.doc_embeddings)[0]
        
        # Sparse search
        tokenized_query = query.split()
        sparse_scores = self.bm25.get_scores(tokenized_query)
        
        # Combine scores
        combined_scores = alpha * dense_scores + (1 - alpha) * sparse_scores
        
        # Get top-k
        top_indices = np.argsort(combined_scores)[-top_k:][::-1]
        
        return [self.documents[i] for i in top_indices]
```

---

## Reranking

### Cross-Encoder Reranking
```python
from sentence_transformers import CrossEncoder

class Reranker:
    def __init__(self):
        self.reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    
    def rerank(self, query, documents, top_k=5):
        # Score all query-document pairs
        pairs = [[query, doc] for doc in documents]
        scores = self.reranker.predict(pairs)
        
        # Sort by score
        ranked_indices = np.argsort(scores)[::-1][:top_k]
        
        return [documents[i] for i in ranked_indices]

# Usage
retriever = HybridSearch(documents)
candidates = retriever.search(query, top_k=20)  # Get 20 candidates

reranker = Reranker()
final_results = reranker.rerank(query, candidates, top_k=5)  # Rerank to 5
```

### LLM-Based Reranking
```python
def llm_rerank(query, documents, top_k=5):
    prompt = f"""
    Query: {query}
    
    Rank the following documents by relevance (1 = most relevant):
    
    {chr(10).join(f"{i+1}. {doc}" for i, doc in enumerate(documents))}
    
    Return only the ranking (e.g., "3,1,4,2,5"):
    """
    
    ranking = llm.generate(prompt)
    indices = [int(x)-1 for x in ranking.split(',')]
    
    return [documents[i] for i in indices[:top_k]]
```

---

## Query Expansion

### Synonym Expansion
```python
from nltk.corpus import wordnet

def expand_query(query):
    words = query.split()
    expanded = []
    
    for word in words:
        expanded.append(word)
        
        # Add synonyms
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                if lemma.name() != word:
                    expanded.append(lemma.name())
    
    return " ".join(set(expanded))

# "fast car" → "fast car quick automobile vehicle"
```

### LLM Query Expansion
```python
def llm_expand_query(query):
    prompt = f"""
    Generate 3 alternative phrasings of this query:
    
    Original: {query}
    
    Alternatives (one per line):
    """
    
    alternatives = llm.generate(prompt).split('\n')
    
    # Search with all variants
    all_results = []
    for variant in [query] + alternatives:
        results = search(variant)
        all_results.extend(results)
    
    # Deduplicate and return
    return list(set(all_results))
```

---

## Metadata Filtering

### Filter Before Search
```python
class MetadataSearch:
    def __init__(self, documents, metadata):
        self.documents = documents
        self.metadata = metadata  # [{"date": "2024-01", "category": "tech"}, ...]
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.embeddings = self.embedder.encode(documents)
    
    def search(self, query, filters=None, top_k=5):
        # Apply filters
        if filters:
            valid_indices = []
            for i, meta in enumerate(self.metadata):
                if all(meta.get(k) == v for k, v in filters.items()):
                    valid_indices.append(i)
        else:
            valid_indices = list(range(len(self.documents)))
        
        # Search only filtered documents
        query_emb = self.embedder.encode(query)
        filtered_embs = self.embeddings[valid_indices]
        
        scores = cosine_similarity([query_emb], filtered_embs)[0]
        top_indices = np.argsort(scores)[-top_k:][::-1]
        
        return [self.documents[valid_indices[i]] for i in top_indices]

# Usage
results = search.search(
    query="machine learning",
    filters={"category": "tech", "date": "2024-01"},
    top_k=5
)
```

---

## Evaluation Metrics

### Retrieval Metrics
```python
def precision_at_k(retrieved, relevant, k):
    """Precision@k: % of top-k that are relevant"""
    top_k = retrieved[:k]
    return len(set(top_k) & set(relevant)) / k

def recall_at_k(retrieved, relevant, k):
    """Recall@k: % of relevant docs in top-k"""
    top_k = retrieved[:k]
    return len(set(top_k) & set(relevant)) / len(relevant)

def mrr(retrieved, relevant):
    """Mean Reciprocal Rank"""
    for i, doc in enumerate(retrieved):
        if doc in relevant:
            return 1 / (i + 1)
    return 0

def ndcg_at_k(retrieved, relevant, k):
    """Normalized Discounted Cumulative Gain"""
    dcg = sum(
        (1 if retrieved[i] in relevant else 0) / np.log2(i + 2)
        for i in range(min(k, len(retrieved)))
    )
    
    idcg = sum(1 / np.log2(i + 2) for i in range(min(k, len(relevant))))
    
    return dcg / idcg if idcg > 0 else 0
```

---

## Best Practices

### 1. Optimize Chunk Size
```python
# Test different chunk sizes
chunk_sizes = [200, 500, 1000, 2000]

for size in chunk_sizes:
    chunks = chunk_text(document, size)
    score = evaluate_retrieval(chunks, test_queries)
    print(f"Size {size}: {score}")
```

### 2. Add Context to Chunks
```python
def chunk_with_context(text, chunk_size=500):
    chunks = []
    
    # Add document title to each chunk
    title = extract_title(text)
    
    for chunk in split_text(text, chunk_size):
        chunk_with_context = f"Document: {title}\n\n{chunk}"
        chunks.append(chunk_with_context)
    
    return chunks
```

### 3. Use Hybrid Search
```
Dense search: Semantic similarity
Sparse search: Keyword matching

Combine both for best results
```

### 4. Rerank Results
```
Retrieve 20 candidates (fast)
Rerank to top 5 (accurate)

Better than retrieving 5 directly
```

### 5. Monitor Quality
```python
# Track retrieval metrics
def monitor_retrieval(query, retrieved, relevant):
    metrics = {
        "precision@5": precision_at_k(retrieved, relevant, 5),
        "recall@5": recall_at_k(retrieved, relevant, 5),
        "mrr": mrr(retrieved, relevant),
        "ndcg@5": ndcg_at_k(retrieved, relevant, 5)
    }
    
    log_metrics(metrics)
    
    return metrics
```

---

## Summary

**Retrieval Quality:** Critical for RAG performance

**Chunking:**
- Fixed-size
- Semantic
- Sentence-based

**Optimization:**
- Choose right embedding model
- Fine-tune embeddings
- Hybrid search (dense + sparse)
- Reranking

**Advanced:**
- Query expansion
- Metadata filtering
- Cross-encoder reranking

**Metrics:**
- Precision@k
- Recall@k
- MRR
- NDCG@k

**Best Practices:**
- Optimize chunk size
- Add context
- Use hybrid search
- Rerank results
- Monitor quality
