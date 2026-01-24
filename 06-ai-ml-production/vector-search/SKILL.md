---
name: Vector Search
description: Comprehensive guide for vector search implementation
---

# Vector Search

## Overview
Comprehensive guide for vector search implementation.

## Prerequisites

- Understanding of vector mathematics and linear algebra
- Familiarity with numpy and numerical computing
- Knowledge of similarity metrics (cosine, Euclidean, dot product)
- Understanding of indexing and data structures
- Experience with FAISS or similar libraries
- Knowledge of GPU computing concepts

## Key Concepts

- **Vector Search**: Finding nearest neighbors in high-dimensional vector space using similarity metrics
- **HNSW (Hierarchical Navigable Small World)**: Approximate nearest neighbor algorithm using graph-based indexing
- **IVF (Inverted File Index)**: Clustering vectors into Voronoi cells for faster search
- **Flat Index**: Exact nearest neighbor search without approximation
- **Cosine Similarity**: Measures similarity between vectors using cosine of the angle between them
- **Euclidean Distance**: Measures straight-line distance between two vectors in vector space
- **Dot Product**: Measures similarity by computing the dot product of vectors
- **FAISS**: Facebook AI Similarity Search library for efficient vector search
- **GPU Acceleration**: Using GPU for faster vector operations and search
- **Metadata Filtering**: Filtering search results based on associated metadata
- **Hybrid Search**: Combining vector search with keyword search for better results
- **Query Optimization**: Techniques for improving query performance (normalization, expansion, augmentation)
- **Re-ranking**: Improving search results using secondary scoring methods
- **Index Compression**: Reducing index size using quantization techniques
- **Sharding**: Distributing vector index across multiple shards for horizontal scaling
- **Replication**: Creating multiple copies of vector index for high availability
- **Recall@K**: Evaluation metric measuring recall at different k values
- **MAP (Mean Average Precision)**: Evaluation metric for ranking quality
- **Incremental Updates**: Adding new vectors without rebuilding entire index
- **Batch Processing**: Processing multiple operations together for efficiency

---

## 1. Vector Search Algorithms

### 1.1 HNSW (Hierarchical Navigable Small World)

```python
import numpy as np
from typing import List, Tuple
import faiss

class HNSWIndex:
    """HNSW index for efficient approximate nearest neighbor search."""

    def __init__(self, dimension: int, M: int = 16, ef_construction: int = 200):
        """
        Args:
            dimension: Dimension of vectors
            M: Maximum number of connections per node
            ef_construction: Size of dynamic candidate list for construction
        """
        self.dimension = dimension
        self.M = M
        self.ef_construction = ef_construction
        self.index = None

    def build_index(self, vectors: np.ndarray):
        """Build HNSW index from vectors."""
        # HNSW index using IndexFlatIP (inner product)
        quantizer = faiss.IndexFlatIP(self.dimension)
        index = faiss.IndexHNSW(quantizer, self.M)
        index.hnsw.efConstruction = self.ef_construction
        index.hnsw.efSearch = 32

        index.add(vectors)
        self.index = index

    def search(
        self,
        query_vector: np.ndarray,
        k: int = 10
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Search for k nearest neighbors."""
        distances, indices = self.index.search(
            query_vector.reshape(1, -1),
            k=k
        )
        return distances, indices

    def search_batch(
        self,
        query_vectors: np.ndarray,
        k: int = 10
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Batch search for multiple queries."""
        distances, indices = self.index.search(
            query_vectors,
            k=k
        )
        return distances, indices

    def save(self, filepath: str):
        """Save index to file."""
        faiss.write_index(self.index, filepath)

    def load(self, filepath: str):
        """Load index from file."""
        self.index = faiss.read_index(filepath)

# Usage
# Generate sample data
np.random.seed(42)
vectors = np.random.randn(1000, 384).astype(np.float32)

# Build HNSW index
hnsw_index = HNSWIndex(dimension=384, M=16)
hnsw_index.build_index(vectors)

# Search
query = np.random.randn(384).astype(np.float32)
distances, indices = hnsw_index.search(query, k=5)

print(f"Nearest neighbors at distances: {distances[0]}")
print(f"Neighbor indices: {indices[0]}")
```

### 1.2 IVF (Inverted File Index)

```python
import numpy as np
import faiss

class IVFIndex:
    """IVF index for fast approximate nearest neighbor search."""

    def __init__(
        self,
        dimension: int,
        nlist: int = 100,
        quantizer: str = "Flat"
    ):
        """
        Args:
            dimension: Dimension of vectors
            nlist: Number of Voronoi cells (clusters)
            quantizer: Type of quantizer (Flat, PQ, etc.)
        """
        self.dimension = dimension
        self.nlist = nlist
        self.quantizer_type = quantizer
        self.index = None

    def build_index(self, vectors: np.ndarray):
        """Build IVF index from vectors."""
        quantizer = faiss.IndexFlat(self.dimension)
        index = faiss.IndexIVFF(quantizer, self.dimension, self.nlist)

        # Train the index
        index.train(vectors)
        index.add(vectors)

        self.index = index

    def search(
        self,
        query_vector: np.ndarray,
        k: int = 10,
        nprobe: int = 1
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Search for k nearest neighbors."""
        distances, indices = self.index.search(
            query_vector.reshape(1, -1),
            k=k,
            nprobe=nprobe
        )
        return distances, indices

    def set_nprobe(self, nprobe: int):
        """Set number of probes for search."""
        self.index.nprobe = nprobe

# Usage
# Generate sample data
np.random.seed(42)
vectors = np.random.randn(10000, 768).astype(np.float32)

# Build IVF index
ivf_index = IVFIndex(dimension=768, nlist=100)
ivf_index.build_index(vectors)

# Search with multiple probes
query = np.random.randn(768).astype(np.float32)
ivf_index.set_nprobe(8)
distances, indices = ivf_index.search(query, k=10)

print(f"Nearest neighbors: {indices[0]}")
```

### 1.3 Flat Index

```python
import numpy as np
import faiss

class FlatIndex:
    """Flat (exact) index for precise nearest neighbor search."""

    def __init__(self, dimension: int, metric: str = "L2"):
        """
        Args:
            dimension: Dimension of vectors
            metric: Distance metric (L2, IP, etc.)
        """
        self.dimension = dimension
        self.metric = metric
        self.index = None

    def build_index(self, vectors: np.ndarray):
        """Build flat index from vectors."""
        if self.metric == "L2":
            self.index = faiss.IndexFlatL2(self.dimension)
        elif self.metric == "IP":
            self.index = faiss.IndexFlatIP(self.dimension)
        else:
            raise ValueError(f"Unknown metric: {self.metric}")

        self.index.add(vectors)

    def search(
        self,
        query_vector: np.ndarray,
        k: int = 10
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Search for k nearest neighbors."""
        distances, indices = self.index.search(
            query_vector.reshape(1, -1),
            k=k
        )
        return distances, indices

    def search_with_threshold(
        self,
        query_vector: np.ndarray,
        threshold: float = 1.0
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Search with distance threshold."""
        distances, indices = self.search(query_vector, k=100)

        # Filter by threshold
        mask = distances[0] < threshold
        filtered_distances = distances[0][mask]
        filtered_indices = indices[0][mask]

        return filtered_distances, filtered_indices

# Usage
# Generate sample data
np.random.seed(42)
vectors = np.random.randn(1000, 512).astype(np.float32)

# Build flat index
flat_index = FlatIndex(dimension=512, metric="L2")
flat_index.build_index(vectors)

# Search with threshold
query = np.random.randn(512).astype(np.float32)
distances, indices = flat_index.search_with_threshold(query, threshold=0.5)

print(f"Found {len(indices[0])} neighbors within threshold")
```

---

## 2. Distance Metrics

### 2.1 Cosine Similarity

```python
import numpy as np
from typing import List

class CosineSimilarity:
    """Cosine similarity calculations."""

    @staticmethod
    def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors."""
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    @staticmethod
    def cosine_distance(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine distance (1 - similarity)."""
        return 1.0 - CosineSimilarity.cosine_similarity(vec1, vec2)

    @staticmethod
    def batch_cosine_similarity(
        vectors: np.ndarray,
        query_vector: np.ndarray
    ) -> np.ndarray:
        """Calculate cosine similarity for batch."""
        # Normalize vectors
        vectors_norm = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)
        query_norm = query_vector / np.linalg.norm(query_vector)

        # Compute similarities
        similarities = np.dot(vectors_norm, query_norm.T).flatten()
        return similarities

    @staticmethod
    def compute_similarity_matrix(vectors: np.ndarray) -> np.ndarray:
        """Compute pairwise similarity matrix."""
        # Normalize vectors
        vectors_norm = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)

        # Compute similarity matrix
        similarity_matrix = np.dot(vectors_norm, vectors_norm.T)
        return similarity_matrix

# Usage
vec1 = np.array([1, 2, 3], dtype=np.float32)
vec2 = np.array([2, 4, 6], dtype=np.float32)

similarity = CosineSimilarity.cosine_similarity(vec1, vec2)
distance = CosineSimilarity.cosine_distance(vec1, vec2)

print(f"Cosine similarity: {similarity:.4f}")
print(f"Cosine distance: {distance:.4f}")

# Batch similarity
vectors = np.random.randn(10, 128).astype(np.float32)
query = np.random.randn(128).astype(np.float32)

similarities = CosineSimilarity.batch_cosine_similarity(vectors, query)
print(f"Similarities: {similarities}")
```

### 2.2 Euclidean Distance

```python
import numpy as np

class EuclideanDistance:
    """Euclidean distance calculations."""

    @staticmethod
    def euclidean_distance(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate Euclidean distance between two vectors."""
        return np.linalg.norm(vec1 - vec2)

    @staticmethod
    def manhattan_distance(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate Manhattan distance between two vectors."""
        return np.sum(np.abs(vec1 - vec2))

    @staticmethod
    def batch_euclidean_distance(
        vectors: np.ndarray,
        query_vector: np.ndarray
    ) -> np.ndarray:
        """Calculate Euclidean distance for batch."""
        distances = np.linalg.norm(vectors - query_vector, axis=1)
        return distances

    @staticmethod
    def squared_euclidean_distance(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate squared Euclidean distance (faster, no sqrt)."""
        return np.sum((vec1 - vec2) ** 2)

# Usage
vec1 = np.array([1, 2, 3], dtype=np.float32)
vec2 = np.array([2, 4, 6], dtype=np.float32)

euclidean_dist = EuclideanDistance.euclidean_distance(vec1, vec2)
manhattan_dist = EuclideanDistance.manhattan_distance(vec1, vec2)

print(f"Euclidean distance: {euclidean_dist:.4f}")
print(f"Manhattan distance: {manhattan_dist:.4f}")
```

### 2.3 Dot Product

```python
import numpy as np

class DotProductSimilarity:
    """Dot product similarity calculations."""

    @staticmethod
    def dot_product(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate dot product between two vectors."""
        return np.dot(vec1, vec2)

    @staticmethod
    def batch_dot_product(
        vectors: np.ndarray,
        query_vector: np.ndarray
    ) -> np.ndarray:
        """Calculate dot product for batch."""
        return np.dot(vectors, query_vector)

    @staticmethod
    def normalized_dot_product(
        vec1: np.ndarray,
        vec2: np.ndarray
    ) -> float:
        """Calculate normalized dot product."""
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return np.dot(vec1, vec2) / (norm1 * norm2)

# Usage
vec1 = np.array([1, 2, 3], dtype=np.float32)
vec2 = np.array([2, 4, 6], dtype=np.float32)

dot_prod = DotProductSimilarity.dot_product(vec1, vec2)
normalized_dot = DotProductSimilarity.normalized_dot_product(vec1, vec2)

print(f"Dot product: {dot_prod:.2f}")
print(f"Normalized dot product: {normalized_dot:.4f}")
```

---

## 3. Implementation with FAISS

### 3.1 Basic FAISS Setup

```python
import numpy as np
import faiss
from typing import List, Tuple

class FAISSVectorStore:
    """FAISS-based vector store."""

    def __init__(self, dimension: int, index_type: str = "HNSW"):
        """
        Args:
            dimension: Dimension of vectors
            index_type: Type of FAISS index (HNSW, IVF, Flat)
        """
        self.dimension = dimension
        self.index_type = index_type
        self.index = None
        self.vectors = []

    def add_vectors(self, vectors: np.ndarray):
        """Add vectors to the index."""
        if self.index is None:
            self._build_index(vectors)
        else:
            self.index.add(vectors)
        self.vectors.append(vectors)

    def _build_index(self, vectors: np.ndarray):
        """Build FAISS index."""
        if self.index_type == "HNSW":
            quantizer = faiss.IndexFlatIP(self.dimension)
            self.index = faiss.IndexHNSW(quantizer, 16)
            self.index.hnsw.efConstruction = 200
            self.index.hnsw.efSearch = 32
        elif self.index_type == "IVF":
            quantizer = faiss.IndexFlatIP(self.dimension)
            self.index = faiss.IndexIVFF(quantizer, self.dimension, 100)
        elif self.index_type == "Flat":
            self.index = faiss.IndexFlatIP(self.dimension)
        else:
            raise ValueError(f"Unknown index type: {self.index_type}")

        self.index.train(vectors)
        self.index.add(vectors)

    def search(
        self,
        query_vector: np.ndarray,
        k: int = 10
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Search for k nearest neighbors."""
        distances, indices = self.index.search(
            query_vector.reshape(1, -1),
            k=k
        )
        return distances, indices

    def search_batch(
        self,
        query_vectors: np.ndarray,
        k: int = 10
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Batch search for multiple queries."""
        distances, indices = self.index.search(
            query_vectors,
            k=k
        )
        return distances, indices

    def save_index(self, filepath: str):
        """Save index to file."""
        faiss.write_index(self.index, filepath)

    def load_index(self, filepath: str):
        """Load index from file."""
        self.index = faiss.read_index(filepath)

    def get_stats(self) -> dict:
        """Get index statistics."""
        return {
            "total_vectors": self.index.ntotal,
            "dimension": self.dimension,
            "index_type": self.index_type,
            "is_trained": self.index.is_trained
        }

# Usage
# Generate sample data
np.random.seed(42)
vectors = np.random.randn(10000, 384).astype(np.float32)

# Create vector store
vector_store = FAISSVectorStore(dimension=384, index_type="HNSW")
vector_store.add_vectors(vectors)

# Search
query = np.random.randn(384).astype(np.float32)
distances, indices = vector_store.search(query, k=5)

print(f"Nearest neighbors at indices: {indices[0]}")
print(f"Distances: {distances[0]}")
```

### 3.2 FAISS with GPU

```python
import numpy as np
import faiss

class GPUFAISSVectorStore:
    """GPU-accelerated FAISS vector store."""

    def __init__(self, dimension: int, use_gpu: bool = True):
        self.dimension = dimension
        self.use_gpu = use_gpu
        self.index = None

        if use_gpu:
            # Use GPU resources
            self.res = faiss.StandardGpuResources()
            self.res.setTemporaryMemory(1 << 20)  # 1GB GPU memory
        self.index = faiss.IndexFlatIP(self.dimension, self.res)
        else:
            self.index = faiss.IndexFlatIP(self.dimension)

    def add_vectors(self, vectors: np.ndarray):
        """Add vectors to the index."""
        if self.use_gpu:
            # Copy vectors to GPU
            vectors_gpu = faiss.index_cpu_to_gpu(vectors)
            self.index.add(vectors_gpu)
        else:
            self.index.add(vectors)

    def search(
        self,
        query_vector: np.ndarray,
        k: int = 10
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Search for k nearest neighbors."""
        if self.use_gpu:
            # Copy query to GPU
            query_gpu = faiss.index_cpu_to_gpu(query_vector.reshape(1, -1))
            distances, indices = self.index.search(query_gpu, k=k)
            # Copy results back to CPU
            distances = faiss.index_gpu_to_cpu(distances)
            indices = faiss.index_gpu_to_cpu(indices)
        else:
            distances, indices = self.index.search(
                query_vector.reshape(1, -1),
                k=k
            )

        return distances, indices

    def search_batch(
        self,
        query_vectors: np.ndarray,
        k: int = 10
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Batch search for multiple queries."""
        if self.use_gpu:
            query_vectors_gpu = faiss.index_cpu_to_gpu(query_vectors)
            distances, indices = self.index.search(query_vectors_gpu, k=k)
            distances = faiss.index_gpu_to_cpu(distances)
            indices = faiss.index_gpu_to_cpu(indices)
        else:
            distances, indices = self.index.search(query_vectors, k=k)

        return distances, indices

# Usage
# Generate sample data
np.random.seed(42)
vectors = np.random.randn(10000, 768).astype(np.float32)

# Create GPU vector store
gpu_store = GPUFAISSVectorStore(dimension=768, use_gpu=True)
gpu_store.add_vectors(vectors)

# Search
query = np.random.randn(768).astype(np.float32)
distances, indices = gpu_store.search(query, k=5)

print(f"Nearest neighbors: {indices[0]}")
```

---

## 4. Metadata Filtering

### 4.1 Filter by Metadata

```python
import numpy as np
from typing import List, Dict, Any
import faiss

class MetadataFilteredVectorStore:
    """Vector store with metadata filtering support."""

    def __init__(self, dimension: int):
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)
        self.metadata: List[Dict[str, Any]] = []

    def add_vectors(
        self,
        vectors: np.ndarray,
        metadata: List[Dict[str, Any]]
    ):
        """Add vectors with metadata."""
        self.index.add(vectors)
        self.metadata.extend(metadata)

    def search(
        self,
        query_vector: np.ndarray,
        k: int = 10,
        filters: Dict[str, Any] = None
    ) -> Tuple[np.ndarray, np.ndarray, List[Dict[str, Any]]]:
        """Search with metadata filtering."""
        # Get all results
        distances, indices = self.index.search(
            query_vector.reshape(1, -1),
            k=len(self.metadata)
        )

        # Filter by metadata
        if filters:
            filtered_indices = []
            filtered_distances = []
            filtered_metadata = []

            for dist, idx in zip(distances[0], indices[0]):
                metadata = self.metadata[idx]

                # Check all filter conditions
                match = True
                for key, value in filters.items():
                    if metadata.get(key) != value:
                        match = False
                        break

                if match:
                    filtered_indices.append(idx)
                    filtered_distances.append(dist)
                    filtered_metadata.append(metadata)

                if len(filtered_indices) >= k:
                    break

            return (
                np.array(filtered_distances),
                np.array(filtered_indices),
                filtered_metadata
            )
        else:
            return distances, indices, self.metadata

    def search_by_category(
        self,
        query_vector: np.ndarray,
        category: str,
        k: int = 10
    ) -> Tuple[np.ndarray, np.ndarray, List[Dict[str, Any]]]:
        """Search within a specific category."""
        return self.search(
            query_vector,
            k=k,
            filters={"category": category}
        )

    def search_by_date_range(
        self,
        query_vector: np.ndarray,
        start_date: str,
        end_date: str,
        k: int = 10
    ) -> Tuple[np.ndarray, np.ndarray, List[Dict[str, Any]]]:
        """Search within a date range."""
        return self.search(
            query_vector,
            k=k,
            filters={
                "date": lambda x: start_date <= x <= end_date
            }
        )

    def search_by_multiple_filters(
        self,
        query_vector: np.ndarray,
        filters: Dict[str, Any]
    ) -> Tuple[np.ndarray, np.ndarray, List[Dict[str, Any]]]:
        """Search with multiple filters."""
        return self.search(query_vector, k=100, filters=filters)

# Usage
# Create vector store
store = MetadataFilteredVectorStore(dimension=384)

# Add vectors with metadata
vectors = np.random.randn(100, 384).astype(np.float32)
metadata = [
    {"id": 0, "category": "tech", "date": "2024-01-01"},
    {"id": 1, "category": "tech", "date": "2024-01-02"},
    {"id": 2, "category": "news", "date": "2024-01-01"},
    {"id": 3, "category": "news", "date": "2024-01-03"},
]

store.add_vectors(vectors, metadata)

# Search with category filter
query = np.random.randn(384).astype(np.float32)
distances, indices, filtered_metadata = store.search_by_category(
    query, category="tech", k=2
)

print(f"Filtered results: {len(filtered_metadata)} items")
```

### 4.2 Hybrid Search (Vector + Keyword)

```python
import numpy as np
from typing import List, Tuple, Dict
import faiss

class HybridSearchEngine:
    """Hybrid search combining vector and keyword search."""

    def __init__(self, dimension: int):
        self.dimension = dimension
        self.vector_index = faiss.IndexFlatIP(dimension)
        self.documents = []
        self.keyword_index = {}

    def add_documents(
        self,
        vectors: np.ndarray,
        documents: List[str]
    ):
        """Add documents with vectors."""
        self.vector_index.add(vectors)
        self.documents.extend(documents)

        # Build keyword index
        for i, doc in enumerate(documents):
            words = doc.lower().split()
            for word in words:
                if word not in self.keyword_index:
                    self.keyword_index[word] = []
                self.keyword_index[word].append(i)

    def vector_search(
        self,
        query_vector: np.ndarray,
        k: int = 10
    ) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """Vector search."""
        distances, indices = self.vector_index.search(
            query_vector.reshape(1, -1),
            k=k
        )
        return distances, indices, [self.documents[i] for i in indices[0]]

    def keyword_search(
        self,
        query: str,
        k: int = 10
    ) -> List[str]:
        """Keyword search."""
        query_words = query.lower().split()
        scores = {}

        for word in query_words:
            if word in self.keyword_index:
                for doc_id in self.keyword_index[word]:
                    scores[doc_id] = scores.get(doc_id, 0) + 1

        # Get top-k documents
        sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [self.documents[doc_id] for doc_id, _ in sorted_docs[:k]]

    def hybrid_search(
        self,
        query_vector: np.ndarray,
        query_text: str,
        vector_weight: float = 0.7,
        k: int = 10
    ) -> List[Tuple[str, float]]:
        """Hybrid search combining vector and keyword results."""
        # Vector search
        vec_distances, vec_indices, vec_docs = self.vector_search(query_vector, k=k)

        # Keyword search
        kw_docs = self.keyword_search(query_text, k=k)

        # Combine results
        results = []

        # Add vector results with scores
        for i, (doc, dist) in enumerate(zip(vec_docs, vec_distances[0])):
            score = vector_weight * (1.0 / (1 + dist))
            results.append((doc, score))

        # Add keyword results with lower scores
        for doc in kw_docs:
            if doc not in [r[0] for r in results]:
                results.append((doc, 0.3 * (1 - vector_weight)))

        # Sort by score
        results.sort(key=lambda x: x[1], reverse=True)

        return results[:k]

# Usage
engine = HybridSearchEngine(dimension=384)

# Add documents
vectors = np.random.randn(100, 384).astype(np.float32)
documents = [
    "This is about machine learning and AI.",
    "Python is a programming language.",
    "JavaScript is used for web development.",
    "React is a JavaScript framework.",
    "Node.js is a JavaScript runtime."
]

engine.add_documents(vectors, documents)

# Hybrid search
query_vector = np.random.randn(384).astype(np.float32)
results = engine.hybrid_search(
    query_vector,
    query_text="machine learning",
    vector_weight=0.7,
    k=5
)

for doc, score in results:
    print(f"Score: {score:.3f} | {doc}")
```

---

## 5. Query Optimization

### 5.1 Query Processing

```python
import numpy as np
from typing import List

class QueryProcessor:
    """Process and optimize queries."""

    @staticmethod
    def normalize_query(query_vector: np.ndarray) -> np.ndarray:
        """Normalize query vector."""
        norm = np.linalg.norm(query_vector)
        if norm > 0:
            return query_vector / norm
        return query_vector

    @staticmethod
    def expand_query(
        query_vector: np.ndarray,
        expansion_factor: float = 1.2
    ) -> np.ndarray:
        """Expand query for better recall."""
        return query_vector * expansion_factor

    @staticmethod
    def query_augmentation(
        query_vector: np.ndarray,
        noise_level: float = 0.01
    ) -> np.ndarray:
        """Add noise to query for robustness."""
        noise = np.random.randn(*query_vector.shape) * noise_level
        return query_vector + noise

    @staticmethod
    def multi_query_ensemble(
        query_vector: np.ndarray,
        variations: int = 3
    ) -> List[np.ndarray]:
        """Generate multiple query variations."""
        variations_list = []

        for _ in range(variations):
            # Add noise
            noisy_query = QueryProcessor.query_augmentation(query_vector, noise_level=0.02)
            variations_list.append(noisy_query)

            # Expand
            expanded = QueryProcessor.expand_query(query_vector, expansion_factor=1.1)
            variations_list.append(expanded)

            # Shrink
            shrunk = QueryProcessor.expand_query(query_vector, expansion_factor=0.9)
            variations_list.append(shrunk)

        return variations_list

# Usage
query_vector = np.random.randn(384).astype(np.float32)

# Normalize query
normalized_query = QueryProcessor.normalize_query(query_vector)

# Generate query variations
variations = QueryProcessor.multi_query_ensemble(normalized_query, variations=3)

print(f"Generated {len(variations)} query variations")
```

### 5.2 Result Re-ranking

```python
import numpy as np
from typing import List, Tuple

class ReRanker:
    """Re-rank search results."""

    @staticmethod
    def reciprocal_rank_fusion(
        vector_scores: np.ndarray,
        keyword_scores: List[float],
        alpha: float = 0.5
    ) -> List[float]:
        """Combine vector and keyword scores."""
        combined_scores = []

        for vec_score, kw_score in zip(vector_scores, keyword_scores):
            combined = alpha * vec_score + (1 - alpha) * kw_score
            combined_scores.append(combined)

        return combined_scores

    @staticmethod
    def rrf_re_ranking(
        query_vector: np.ndarray,
        documents: List[np.ndarray],
        top_k: int = 10
    ) -> Tuple[np.ndarray, List[int]]:
        """Reciprocal Rank Fusion (RRF) re-ranking."""
        # Initial vector search
        from sklearn.metrics.pairwise import cosine_similarity

        # Compute relevance scores
        similarities = cosine_similarity(query_vector, documents)

        # RRF re-ranking
        final_scores = np.zeros(len(documents))

        for i in range(len(documents)):
            for j in range(len(documents)):
                if i != j:
                    # Compute similarity between doc i and doc j
                    sim = similarities[i][j]

                    # Score: higher similarity to query = higher score
                    final_scores[i] += sim

        # Get top-k
        top_indices = np.argsort(final_scores)[-top_k:]

        return final_scores[top_indices], top_indices.tolist()

    @staticmethod
    def cross_encoder_rerank(
        query_vector: np.ndarray,
        documents: List[np.ndarray],
        cross_encoder,
        top_k: int = 10
    ) -> List[int]:
        """Re-rank using cross-encoder."""
        # Score documents with cross-encoder
        scores = cross_encoder.predict(query_vector, documents)

        # Get top-k
        top_indices = np.argsort(scores)[-top_k:]

        return top_indices.tolist()

# Usage
# Generate sample data
query_vector = np.random.randn(384).astype(np.float32)
documents = np.random.randn(100, 384).astype(np.float32)

# RRF re-ranking
scores, indices = ReRanker.rrf_re_ranking(query_vector, documents, top_k=5)

print(f"Re-ranked indices: {indices}")
```

---

## 6. Index Optimization

### 6.1 Index Building Strategies

```python
import numpy as np
import faiss

class IndexOptimizer:
    """Optimize FAISS index for performance."""

    @staticmethod
    def optimize_ivf_index(
        dimension: int,
        vectors: np.ndarray,
        nlist: int = 100
    ) -> faiss.Index:
        """Optimize IVF index parameters."""
        # Try different nlist values
        best_nlist = nlist
        best_index = None
        best_speed = float('inf')

        for test_nlist in [50, 100, 200, 400]:
            quantizer = faiss.IndexFlatIP(dimension)
            index = faiss.IndexIVFF(quantizer, dimension, test_nlist)

            # Measure build time
            import time
            start = time.time()
            index.train(vectors)
            build_time = time.time() - start

            # Measure query time
            start = time.time()
            for _ in range(100):
                index.search(vectors[:1], k=10)
            query_time = time.time() - start

            total_time = build_time + query_time

            if total_time < best_speed:
                best_speed = total_time
                best_nlist = test_nlist
                best_index = index

        return best_index

    @staticmethod
    def optimize_hnsw_index(
        dimension: int,
        vectors: np.ndarray,
        M: int = 16
    ) -> faiss.Index:
        """Optimize HNSW index parameters."""
        # Try different M values
        best_M = M
        best_index = None
        best_speed = float('inf')

        for test_M in [8, 16, 32, 64]:
            quantizer = faiss.IndexFlatIP(dimension)
            index = faiss.IndexHNSW(quantizer, test_M)
            index.hnsw.efConstruction = 200
            index.hnsw.efSearch = 32

            # Measure build time
            import time
            start = time.time()
            index.train(vectors)
            build_time = time.time() - start

            # Measure query time
            start = time.time()
            for _ in range(100):
                index.search(vectors[:1], k=10)
            query_time = time.time() - start

            total_time = build_time + query_time

            if total_time < best_speed:
                best_speed = total_time
                best_M = test_M
                best_index = index

        return best_index

# Usage
# Generate sample data
vectors = np.random.randn(10000, 768).astype(np.float32)

# Optimize IVF index
ivf_index = IndexOptimizer.optimize_ivf_index(768, vectors)

# Optimize HNSW index
hnsw_index = IndexOptimizer.optimize_hnsw_index(768, vectors)

print(f"Optimized IVF nlist: {ivf_index.nlist}")
print(f"Optimized HNSW M: {hnsw_index.hnsw.M}")
```

### 6.2 Index Compression

```python
import faiss
import numpy as np

class CompressedIndex:
    """Compressed FAISS index for memory efficiency."""

    def __init__(self, dimension: int, bits: int = 8):
        """
        Args:
            dimension: Dimension of vectors
            bits: Number of bits for quantization (4 or 8)
        """
        self.dimension = dimension
        self.bits = bits
        self.index = None

    def build_index(self, vectors: np.ndarray):
        """Build compressed index."""
        # Scalar quantizer
        quantizer = faiss.ScalarQuantizer(
            vectors,
            qtype=faiss.ScalarQuantizer.QT_fp16 if self.bits == 8 else faiss.ScalarQuantizer.QT_int8
        )

        # Build index
        index = faiss.IndexFlatIP(self.dimension)
        index = faiss.IndexIDMap2(index, quantizer)

        index.add(vectors)

        self.index = index

    def search(
        self,
        query_vector: np.ndarray,
        k: int = 10
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Search in compressed index."""
        distances, indices = self.index.search(
            query_vector.reshape(1, -1),
            k=k
        )
        return distances, indices

    def get_compression_ratio(self) -> float:
        """Get compression ratio."""
        original_size = self.dimension * 4 * len(self.index.xb)
        compressed_size = self.index.code_size

        return 1.0 - (compressed_size / original_size)

    def save_index(self, filepath: str):
        """Save compressed index."""
        faiss.write_index(self.index, filepath)

# Usage
# Generate sample data
vectors = np.random.randn(10000, 768).astype(np.float32)

# Build compressed index
compressed_index = CompressedIndex(dimension=768, bits=8)
compressed_index.build_index(vectors)

# Search
query = np.random.randn(768).astype(np.float32)
distances, indices = compressed_index.search(query, k=5)

print(f"Compression ratio: {compressed_index.get_compression_ratio():.2%}")
print(f"Nearest neighbors: {indices[0]}")
```

---

## 7. Scaling Strategies

### 7.1 Sharding

```python
import numpy as np
from typing import List, Dict
import faiss

class ShardedVectorStore:
    """Sharded vector store for horizontal scaling."""

    def __init__(self, dimension: int, num_shards: int = 4):
        self.dimension = dimension
        self.num_shards = num_shards
        self.shards = []

        for _ in range(num_shards):
            self.shards.append({
                "index": faiss.IndexFlatIP(dimension),
                "vectors": [],
                "metadata": []
            })

    def add_vectors(self, shard_id: int, vectors: np.ndarray, metadata: List[Dict] = None):
        """Add vectors to specific shard."""
        if shard_id >= len(self.shards):
            raise ValueError(f"Invalid shard ID: {shard_id}")

        shard = self.shards[shard_id]
        shard["vectors"].append(vectors)

        if metadata:
            shard["metadata"].extend(metadata)

    def build_shard(self, shard_id: int):
        """Build index for specific shard."""
        shard = self.shards[shard_id]
        if shard["vectors"]:
            vectors = np.array(shard["vectors"])
            shard["index"].train(vectors)

    def build_all_shards(self):
        """Build all shard indices."""
        for shard_id in range(self.num_shards):
            self.build_shard(shard_id)

    def search(
        self,
        query_vector: np.ndarray,
        k: int = 10
    ) -> List[Tuple[np.ndarray, np.ndarray, List[Dict]]]:
        """Search across all shards."""
        all_results = []

        for shard_id, shard in enumerate(self.shards):
            if shard["index"].is_trained:
                distances, indices = shard["index"].search(
                    query_vector.reshape(1, -1),
                    k=k
                )

                for dist, idx in zip(distances[0], indices[0]):
                    all_results.append({
                        "shard_id": shard_id,
                        "distance": dist,
                        "index": idx,
                        "metadata": shard["metadata"][idx] if shard["metadata"] else None
                    })

        # Sort by distance
        all_results.sort(key=lambda x: x["distance"])

        return all_results[:k]

    def get_shard_stats(self) -> List[Dict]:
        """Get statistics for all shards."""
        stats = []

        for shard_id, shard in enumerate(self.shards):
            stats.append({
                "shard_id": shard_id,
                "num_vectors": len(shard["vectors"]),
                "is_trained": shard["index"].is_trained
            })

        return stats

# Usage
# Create sharded store
store = ShardedVectorStore(dimension=384, num_shards=4)

# Add vectors to shards
for i in range(4):
    vectors = np.random.randn(2500, 384).astype(np.float32)
    metadata = [{"id": f"doc_{i}_{j}", "shard": i} for j in range(2500)]
    store.add_vectors(i, vectors, metadata)

# Build all shards
store.build_all_shards()

# Search across shards
query = np.random.randn(384).astype(np.float32)
results = store.search(query, k=5)

print(f"Found {len(results)} results from {len(store.shards)} shards")
```

### 7.2 Replication

```python
import numpy as np
import faiss
from typing import List

class ReplicatedVectorStore:
    """Replicated vector store for high availability."""

    def __init__(self, dimension: int, num_replicas: int = 3):
        self.dimension = dimension
        self.num_replicas = num_replicas
        self.replicas = []

        for _ in range(num_replicas):
            self.replicas.append({
                "index": faiss.IndexFlatIP(dimension),
                "vectors": [],
                "is_ready": False
            })

    def add_vectors(self, vectors: np.ndarray):
        """Add vectors to all replicas."""
        for replica in self.replicas:
            replica["vectors"].append(vectors)

    def build_replicas(self):
        """Build all replica indices."""
        for replica in self.replicas:
            if replica["vectors"]:
                vectors = np.array(replica["vectors"])
                replica["index"].train(vectors)
                replica["is_ready"] = True

    def search(
        self,
        query_vector: np.ndarray,
        k: int = 10
    ) -> List[Tuple[np.ndarray, np.ndarray, int]]:
        """Search across all replicas."""
        # Search from first available replica
        for i, replica in enumerate(self.replicas):
            if replica["is_ready"]:
                try:
                    distances, indices = replica["index"].search(
                        query_vector.reshape(1, -1),
                        k=k
                    )
                    return distances, indices, i
                except Exception as e:
                    print(f"Replica {i} error: {e}")
                    continue

        # If all replicas fail, return empty results
        return np.array([]), np.array([]), -1

    def get_replica_status(self) -> List[Dict]:
        """Get status of all replicas."""
        return [
            {
                "replica_id": i,
                "num_vectors": len(replica["vectors"]),
                "is_ready": replica["is_ready"]
            }
            for i, replica in enumerate(self.replicas)
        ]

# Usage
# Create replicated store
store = ReplicatedVectorStore(dimension=384, num_replicas=3)

# Add vectors
vectors = np.random.randn(10000, 384).astype(np.float32)
store.add_vectors(vectors)

# Build replicas
store.build_replicas()

# Search
query = np.random.randn(384).astype(np.float32)
distances, indices, replica_id = store.search(query, k=5)

print(f"Results from replica {replica_id}")
```

---

## 8. Performance Tuning

### 8.1 Benchmarking

```python
import time
import numpy as np
from typing import Dict, List

class VectorStoreBenchmark:
    """Benchmark vector store performance."""

    def __init__(self):
        self.results = []

    def benchmark_index_building(
        self,
        index_type: str,
        vectors: np.ndarray,
        num_iterations: int = 10
    ) -> Dict[str, float]:
        """Benchmark index building performance."""
        times = []

        for _ in range(num_iterations):
            start = time.time()

            if index_type == "flat":
                import faiss
                index = faiss.IndexFlatIP(vectors.shape[1])
                index.add(vectors)
            elif index_type == "hnsw":
                import faiss
                quantizer = faiss.IndexFlatIP(vectors.shape[1])
                index = faiss.IndexHNSW(quantizer, 16)
                index.hnsw.efConstruction = 200
                index.add(vectors)
            else:
                raise ValueError(f"Unknown index type: {index_type}")

            elapsed = time.time() - start
            times.append(elapsed)

        return {
            "avg_time_ms": np.mean(times) * 1000,
            "min_time_ms": np.min(times) * 1000,
            "max_time_ms": np.max(times) * 1000,
            "std_time_ms": np.std(times) * 1000
        }

    def benchmark_search(
        self,
        index,
        query_vector: np.ndarray,
        k: int = 10,
        num_iterations: int = 100
    ) -> Dict[str, float]:
        """Benchmark search performance."""
        times = []

        for _ in range(num_iterations):
            start = time.time()
            distances, indices = index.search(query_vector.reshape(1, -1), k=k)
            elapsed = time.time() - start
            times.append(elapsed)

        return {
            "avg_time_ms": np.mean(times) * 1000,
            "min_time_ms": np.min(times) * 1000,
            "max_time_ms": np.max(times) * 1000,
            "std_time_ms": np.std(times) * 1000,
            "throughput_per_sec": num_iterations / np.sum(times)
        }

    def benchmark_batch_search(
        self,
        index,
        query_vectors: np.ndarray,
        k: int = 10
    ) -> Dict[str, float]:
        """Benchmark batch search performance."""
        times = []

        for _ in range(100):
            start = time.time()
            distances, indices = index.search(query_vectors, k=k)
            elapsed = time.time() - start
            times.append(elapsed)

        return {
            "avg_time_ms": np.mean(times) * 1000,
            "min_time_ms": np.min(times) * 1000,
            "max_time_ms": np.max(times) * 1000,
            "std_time_ms": np.std(times) * 1000,
            "throughput_per_sec": 100 / np.sum(times)
        }

    def run_full_benchmark(
        self,
        vectors: np.ndarray,
        index_types: List[str]
    ) -> Dict[str, Dict]:
        """Run full benchmark."""
        results = {}

        for index_type in index_types:
            print(f"Benchmarking {index_type}...")

            # Build index
            build_metrics = self.benchmark_index_building(
                index_type, vectors, num_iterations=10
            )

            # Create index
            if index_type == "flat":
                import faiss
                index = faiss.IndexFlatIP(vectors.shape[1])
                index.add(vectors)
            elif index_type == "hnsw":
                import faiss
                quantizer = faiss.IndexFlatIP(vectors.shape[1])
                index = faiss.IndexHNSW(quantizer, 16)
                index.hnsw.efConstruction = 200
                index.add(vectors)

            # Benchmark search
            query = vectors[0]
            search_metrics = self.benchmark_search(index, query, k=10)

            results[index_type] = {
                "build": build_metrics,
                "search": search_metrics
            }

        return results

# Usage
# Generate sample data
vectors = np.random.randn(10000, 768).astype(np.float32)

# Run benchmark
benchmark = VectorStoreBenchmark()
results = benchmark.run_full_benchmark(vectors, ["flat", "hnsw"])

for index_type, metrics in results.items():
    print(f"\n{index_type.upper()}:")
    print(f"  Build: {metrics['build']['avg_time_ms']:.2f}ms")
    print(f"  Search: {metrics['search']['avg_time_ms']:.2f}ms")
    print(f"  Throughput: {metrics['search']['throughput_per_sec']:.2f} queries/sec")
```

### 8.2 Memory Optimization

```python
import numpy as np
import faiss

class MemoryOptimizedVectorStore:
    """Memory-optimized vector store."""

    def __init__(self, dimension: int):
        self.dimension = dimension
        self.index = None

    def build_memory_efficient_index(
        self,
        vectors: np.ndarray,
        use_pq: bool = True
    ):
        """Build memory-efficient index."""
        if use_pq:
            # Product Quantization (PQ) for memory efficiency
            nbits = 8  # 8 bits per dimension
            quantizer = faiss.IndexPQ(self.dimension, nbits=nbits)
            self.index = faiss.IndexPQ(quantizer)
            self.index.train(vectors)
        else:
            # Standard index
            self.index = faiss.IndexFlatIP(self.dimension)
            self.index.train(vectors)

    def search_with_memory_limit(
        self,
        query_vector: np.ndarray,
        k: int = 10,
        max_memory_mb: float = 100
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Search with memory limit."""
        # Check current memory usage
        import psutil
        current_memory = psutil.Process().memory_info().rss / 1024**2  # GB

        if current_memory > max_memory_mb:
            # Reduce k to fit memory
            k = max(1, int(k * (max_memory_mb / current_memory)))

        distances, indices = self.index.search(
            query_vector.reshape(1, -1),
            k=k
        )

        return distances, indices

    def get_memory_usage(self) -> float:
        """Get current memory usage in GB."""
        return psutil.Process().memory_info().rss / 1024**2

# Usage
# Generate sample data
vectors = np.random.randn(100000, 768).astype(np.float32)

# Build memory-efficient index
store = MemoryOptimizedVectorStore(dimension=768)
store.build_memory_efficient_index(vectors, use_pq=True)

# Search with memory limit
query = np.random.randn(768).astype(np.float32)
distances, indices = store.search_with_memory_limit(query, k=100)

print(f"Memory usage: {store.get_memory_usage():.2f}GB")
```

---

## 9. Evaluation

### 9.1 Recall@K Evaluation

```python
import numpy as np
from typing import List, Tuple
import faiss

class RecallAtKEvaluator:
    """Evaluate recall@K metric."""

    @staticmethod
    def compute_recall_at_k(
        index: faiss.Index,
        query_vectors: np.ndarray,
        ground_truth_indices: List[List[int]],
        k_values: List[int]
    ) -> Dict[int, float]:
        """Compute recall@K for different k values."""
        results = {k: [] for k in k_values}

        for k in k_values:
            recalls = []

            for query_idx, ground_truth in enumerate(ground_truth_indices):
                distances, indices = index.search(
                    query_vectors[query_idx].reshape(1, -1),
                    k=k
                )

                # Check if any ground truth in results
                recall = 1 if any(idx in ground_truth for idx in indices[0]) else 0
                recalls.append(recall)

            avg_recall = np.mean(recalls)
            results[k] = avg_recall

        return results

    @staticmethod
    def compute_map(
        index: faiss.Index,
        query_vectors: np.ndarray,
        ground_truth_indices: List[List[int]],
        k: int = 10
    ) -> Dict[str, float]:
        """Compute Mean Average Precision (MAP)."""
        precisions = []

        for query_idx, ground_truth in enumerate(ground_truth_indices):
            distances, indices = index.search(
                query_vectors[query_idx].reshape(1, -1),
                k=k
            )

            # Calculate precision
            relevant = set(ground_truth)
            retrieved = set(indices[0])
            precision = len(retrieved & relevant) / k
            precisions.append(precision)

        return {
            "map": np.mean(precisions),
            "precisions": precisions
        }

# Usage
# Generate sample data
np.random.seed(42)
vectors = np.random.randn(1000, 768).astype(np.float32)
query_vectors = np.random.randn(100, 768).astype(np.float32)

# Ground truth (top-10 for each query)
ground_truth_indices = [
    list(range(10)) for _ in range(100)
]

# Build index
index = faiss.IndexFlatIP(768)
index.train(vectors)

# Evaluate Recall@K
k_values = [1, 5, 10, 20, 50, 100]
recall_results = RecallAtKEvaluator.compute_recall_at_k(
    index, query_vectors, ground_truth_indices, k_values
)

for k, recall in recall_results.items():
    print(f"Recall@{k}: {recall:.3f}")
```

---

## 10. Common Patterns

### 10.1 Incremental Updates

```python
import numpy as np
from typing import List
import faiss

class IncrementalVectorStore:
    """Incrementally update vector store."""

    def __init__(self, dimension: int):
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)
        self.vectors_added = 0

    def add_vectors(self, vectors: np.ndarray):
        """Add new vectors to the index."""
        self.index.add(vectors)
        self.vectors_added += len(vectors)

    def rebuild_index(self):
        """Rebuild index from scratch."""
        # Get all vectors (assuming we keep track of them)
        # In production, you'd load from storage
        pass

    def search(
        self,
        query_vector: np.ndarray,
        k: int = 10
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Search the index."""
        return self.index.search(
            query_vector.reshape(1, -1),
            k=k
        )

    def get_stats(self) -> Dict:
        """Get store statistics."""
        return {
            "total_vectors": self.vectors_added,
            "dimension": self.dimension,
            "is_trained": self.index.is_trained
        }

# Usage
store = IncrementalVectorStore(dimension=384)

# Add vectors in batches
for i in range(10):
    batch = np.random.randn(1000, 384).astype(np.float32)
    store.add_vectors(batch)
    print(f"Added batch {i+1}: {store.get_stats()}")
```

### 10.2 Batch Processing

```python
import numpy as np
from typing import List, Tuple
import faiss

class BatchVectorStore:
    """Batch processing for vector operations."""

    def __init__(self, dimension: int):
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)

    def batch_add_vectors(self, vectors: np.ndarray):
        """Add vectors in batch."""
        self.index.add(vectors)

    def batch_search(
        self,
        query_vectors: np.ndarray,
        k: int = 10
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Batch search for multiple queries."""
        distances, indices = self.index.search(query_vectors, k=k)
        return distances, indices

    def batch_delete_vectors(self, ids: List[int]):
        """Delete vectors by IDs."""
        # In production, implement with ID tracking
        pass

    def batch_update_vectors(
        self,
        ids: List[int],
        new_vectors: np.ndarray
    ):
        """Update vectors by IDs."""
        # In production, implement with ID tracking
        pass

# Usage
# Generate sample data
vectors = np.random.randn(10000, 768).astype(np.float32)
queries = np.random.randn(100, 768).astype(np.float32)

# Batch add
store = BatchVectorStore(dimension=768)
store.batch_add_vectors(vectors)

# Batch search
distances, indices = store.batch_search(queries, k=10)

print(f"Found {len(indices[0])} results for {len(queries)} queries")
```

---

## Related Skills

- [`06-ai-ml-production/embedding-models`](06-ai-ml-production/embedding-models/SKILL.md)
- [`06-ai-ml-production/rag-implementation`](06-ai-ml-production/rag-implementation/SKILL.md)
- [`06-ai-ml-production/vector-search-patterns`](06-ai-ml-production/vector-search-patterns/SKILL.md)
- [`04-database/vector-database`](04-database/vector-database/SKILL.md)

## Additional Resources

- [FAISS Documentation](https://faiss.ai/)
- [FAISS GitHub](https://github.com/facebookresearch/faiss)
- [Vector Database Comparison](https://zilliz.com/learn/ann-guide/)
