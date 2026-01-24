---
name: RAG Implementation
description: Comprehensive guide for Retrieval-Augmented Generation (RAG) implementation using LangChain
---

# RAG Implementation

## Overview
Comprehensive guide for Retrieval-Augmented Generation (RAG) implementation using LangChain.

## Prerequisites

- Understanding of vector databases and embeddings
- Familiarity with LangChain framework
- Knowledge of document processing and chunking
- Experience with LLM integration
- Understanding of semantic search concepts
- Basic knowledge of retrieval strategies

## Key Concepts

- **RAG Architecture**: Retrieval-Augmented Generation combines retrieval from a knowledge base with LLM generation
- **Document Chunking**: Splitting documents into smaller pieces for efficient processing and retrieval
- **Embeddings**: Converting text to vector representations for semantic similarity search
- **Vector Stores**: Databases optimized for storing and retrieving vector embeddings (FAISS, Chroma, Pinecone, Weaviate)
- **Semantic Search**: Finding documents based on meaning rather than keyword matching
- **Hybrid Search**: Combining semantic search with keyword search (BM25) for better results
- **Re-ranking**: Improving retrieval results by re-scoring with more accurate models
- **Context Window Management**: Managing the amount of context passed to the LLM within token limits
- **Multi-Query Retrieval**: Generating multiple queries from a single input to improve retrieval coverage
- **Self-Querying**: Extracting metadata filters from queries to refine search results
- **Parent Document Retrieval**: Retrieving full parent documents instead of chunks for better context
- **RAG Evaluation**: Measuring precision, recall, and F1 score for retrieval and generation quality
- **Caching**: Storing frequently asked queries and responses to improve performance
- **Batch Processing**: Processing multiple queries concurrently for efficiency

---

## 1. RAG Architecture Overview

```
┌─────────────┐
│   Documents  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Chunking  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Embedding   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Vector Store │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Retrieval  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Prompt     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│     LLM     │
└─────────────┘
```

---

## 2. Document Processing

### 2.1 Chunking Strategies

```python
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
    TokenTextSplitter,
    SemanticChunker
)
from langchain.docstore.document import Document

class DocumentChunker:
    """Split documents into chunks."""

    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def character_split(self, text: str) -> list[Document]:
        """Split by character count."""
        splitter = CharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separator="\n\n"
        )
        return splitter.create_documents([text])

    def recursive_split(self, text: str) -> list[Document]:
        """Split recursively by delimiters."""
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        return splitter.create_documents([text])

    def token_split(self, text: str, tokenizer: str = "gpt-4") -> list[Document]:
        """Split by token count."""
        splitter = TokenTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            encoding_name=tokenizer
        )
        return splitter.create_documents([text])

    def semantic_split(self, text: str) -> list[Document]:
        """Split by semantic boundaries."""
        splitter = SemanticChunker(
            text,
            embeddings=OpenAIEmbeddings(),
            breakpoint_threshold_type="percentile"
        )
        return splitter.create_documents([text])

    def custom_split(self, text: str, pattern: str = "\n\n\n") -> list[Document]:
        """Custom split by pattern."""
        chunks = text.split(pattern)
        return [Document(page_content=chunk) for chunk in chunks]

# Usage
chunker = DocumentChunker(chunk_size=1000, chunk_overlap=200)

text = "Long document text..."

chunks = chunker.recursive_split(text)
print(f"Created {len(chunks)} chunks")
```

### 2.2 Metadata Extraction

```python
from typing import Dict, Any
import re
from datetime import datetime

class MetadataExtractor:
    """Extract metadata from documents."""

    @staticmethod
    def extract_basic(text: str) -> Dict[str, Any]:
        """Extract basic metadata."""
        return {
            "char_count": len(text),
            "word_count": len(text.split()),
            "sentence_count": len(re.split(r'[.!?]+', text)),
            "paragraph_count": len(text.split('\n\n')),
            "extracted_at": datetime.now().isoformat()
        }

    @staticmethod
    def extract_urls(text: str) -> list[str]:
        """Extract URLs from text."""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.findall(url_pattern, text)

    @staticmethod
    def extract_emails(text: str) -> list[str]:
        """Extract emails from text."""
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        return re.findall(email_pattern, text)

    @staticmethod
    def extract_dates(text: str) -> list[str]:
        """Extract dates from text."""
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
            r'\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY
            r'\d{1,2} [A-Za-z]+ \d{4}',  # DD Month YYYY
        ]
        dates = []
        for pattern in date_patterns:
            dates.extend(re.findall(pattern, text))
        return dates

    @staticmethod
    def extract_numbers(text: str) -> list[float]:
        """Extract numbers from text."""
        number_pattern = r'-?\d+\.?\d*'
        numbers = re.findall(number_pattern, text)
        return [float(num) for num in numbers]

    @staticmethod
    def extract_entities(text: str) -> Dict[str, Any]:
        """Extract named entities using NLP."""
        try:
            import spacy
            nlp = spacy.load("en_core_web_sm")
            doc = nlp(text)

            entities = {
                "persons": [],
                "organizations": [],
                "locations": [],
                "dates": []
            }

            for ent in doc.ents:
                if ent.label_ == "PERSON":
                    entities["persons"].append(ent.text)
                elif ent.label_ == "ORG":
                    entities["organizations"].append(ent.text)
                elif ent.label_ == "GPE":
                    entities["locations"].append(ent.text)
                elif ent.label_ == "DATE":
                    entities["dates"].append(ent.text)

            return entities
        except ImportError:
            return {}

    def extract_all(self, text: str, source: str = "unknown") -> Dict[str, Any]:
        """Extract all metadata."""
        return {
            "source": source,
            "basic": self.extract_basic(text),
            "urls": self.extract_urls(text),
            "emails": self.extract_emails(text),
            "dates": self.extract_dates(text),
            "numbers": self.extract_numbers(text),
            "entities": self.extract_entities(text)
        }

# Usage
extractor = MetadataExtractor()

metadata = extractor.extract_all(document_text, source="document.pdf")
print(metadata)
```

---

## 3. Embedding Generation

```python
from langchain.embeddings import (
    OpenAIEmbeddings,
    HuggingFaceEmbeddings,
    CohereEmbeddings,
    SentenceTransformerEmbeddings
)
from typing import List

class EmbeddingGenerator:
    """Generate embeddings for documents."""

    def __init__(self, model: str = "openai"):
        self.model = model
        self.embedding_model = self._get_embedding_model()

    def _get_embedding_model(self):
        """Get embedding model."""
        if self.model == "openai":
            return OpenAIEmbeddings()
        elif self.model == "huggingface":
            return HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
        elif self.model == "cohere":
            return CohereEmbeddings()
        elif self.model == "sentence-transformers":
            return SentenceTransformerEmbeddings(
                model_name="all-MiniLM-L6-v2"
            )
        else:
            raise ValueError(f"Unknown model: {self.model}")

    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        """Generate embeddings for documents."""
        return self.embedding_model.embed_documents(documents)

    def embed_query(self, query: str) -> List[float]:
        """Generate embedding for query."""
        return self.embedding_model.embed_query(query)

    def embed_batch(self, texts: List[str], batch_size: int = 32) -> List[List[float]]:
        """Generate embeddings in batches."""
        embeddings = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch_embeddings = self.embed_documents(batch)
            embeddings.extend(batch_embeddings)

        return embeddings

# Usage
generator = EmbeddingGenerator(model="openai")

# Embed documents
documents = ["Document 1 text", "Document 2 text", "Document 3 text"]
document_embeddings = generator.embed_documents(documents)

# Embed query
query = "What is the capital of France?"
query_embedding = generator.embed_query(query)
```

---

## 4. Vector Storage and Retrieval

### 4.1 Vector Store Setup

```python
from langchain.vectorstores import (
    FAISS,
    Chroma,
    Pinecone,
    Weaviate
)
from langchain.docstore.document import Document
from typing import List, Optional

class VectorStoreManager:
    """Manage vector storage and retrieval."""

    def __init__(self, vector_store_type: str = "faiss"):
        self.vector_store_type = vector_store_type
        self.vector_store = None

    def create_faiss_store(
        self,
        documents: List[Document],
        embeddings: List[List[float]]
    ):
        """Create FAISS vector store."""
        self.vector_store = FAISS.from_documents(documents, embeddings)
        return self.vector_store

    def create_chroma_store(
        self,
        documents: List[Document],
        embeddings: List[List[float]],
        collection_name: str = "documents"
    ):
        """Create Chroma vector store."""
        self.vector_store = Chroma.from_documents(
            documents=documents,
            embedding=embeddings,
            collection_name=collection_name
        )
        return self.vector_store

    def create_pinecone_store(
        self,
        documents: List[Document],
        embeddings: List[List[float]],
        index_name: str,
        environment: str = "us-west1-gcp"
    ):
        """Create Pinecone vector store."""
        import pinecone

        # Initialize Pinecone
        pinecone.init(api_key="your-api-key", environment=environment)

        # Create index
        if index_name not in pinecone.list_indexes():
            pinecone.create_index(
                name=index_name,
                dimension=len(embeddings[0]),
                metric="cosine"
            )

        self.vector_store = Pinecone.from_documents(
            documents=documents,
            embedding=embeddings,
            index_name=index_name
        )
        return self.vector_store

    def similarity_search(
        self,
        query: str,
        k: int = 4,
        filter: Optional[dict] = None
    ) -> List[Document]:
        """Perform similarity search."""
        return self.vector_store.similarity_search(query, k=k, filter=filter)

    def similarity_search_with_score(
        self,
        query: str,
        k: int = 4,
        filter: Optional[dict] = None
    ) -> List[tuple]:
        """Perform similarity search with scores."""
        return self.vector_store.similarity_search_with_score(
            query, k=k, filter=filter
        )

    def max_marginal_relevance_search(
        self,
        query: str,
        k: int = 4,
        fetch_k: int = 20,
        lambda_mult: float = 0.5
    ) -> List[Document]:
        """MMR search for diverse results."""
        return self.vector_store.max_marginal_relevance_search(
            query, k=k, fetch_k=fetch_k, lambda_mult=lambda_mult
        )

# Usage
manager = VectorStoreManager(vector_store_type="faiss")

# Create vector store
documents = [
    Document(page_content="Paris is the capital of France."),
    Document(page_content="London is the capital of UK."),
    Document(page_content="Berlin is the capital of Germany.")
]
embeddings = generator.embed_documents([doc.page_content for doc in documents])

vector_store = manager.create_faiss_store(documents, embeddings)

# Search
results = manager.similarity_search("capital of France", k=2)
for doc in results:
    print(doc.page_content)
```

---

## 5. Retrieval Strategies

### 5.1 Semantic Search

```python
from langchain.retrievers import VectorStoreRetriever

class SemanticRetriever:
    """Semantic search retriever."""

    def __init__(self, vector_store, search_kwargs: dict = None):
        self.vector_store = vector_store
        self.search_kwargs = search_kwargs or {"k": 4}

    def get_relevant_documents(self, query: str) -> List[Document]:
        """Get relevant documents using semantic search."""
        return self.vector_store.similarity_search(
            query,
            **self.search_kwargs
        )

    async def aget_relevant_documents(self, query: str) -> List[Document]:
        """Async get relevant documents."""
        return await self.vector_store.asimilarity_search(
            query,
            **self.search_kwargs
        )

# Usage
retriever = SemanticRetriever(vector_store, search_kwargs={"k": 3})
results = retriever.get_relevant_documents("capital of France")
```

### 5.2 Hybrid Search

```python
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain_community.retrievers import BM25Retriever as CommunityBM25Retriever

class HybridRetriever:
    """Hybrid search combining semantic and keyword search."""

    def __init__(self, vector_store, documents: List[Document]):
        self.vector_store = vector_store
        self.documents = documents

        # Create semantic retriever
        self.semantic_retriever = VectorStoreRetriever(
            vector_store=vector_store,
            search_kwargs={"k": 5}
        )

        # Create keyword retriever
        self.keyword_retriever = BM25Retriever.from_documents(documents)

        # Create ensemble retriever
        self.ensemble_retriever = EnsembleRetriever(
            retrievers=[self.semantic_retriever, self.keyword_retriever],
            weights=[0.7, 0.3]  # 70% semantic, 30% keyword
        )

    def get_relevant_documents(self, query: str) -> List[Document]:
        """Get relevant documents using hybrid search."""
        return self.ensemble_retriever.get_relevant_documents(query)

# Usage
hybrid_retriever = HybridRetriever(vector_store, documents)
results = hybrid_retriever.get_relevant_documents("capital of France")
```

### 5.3 Re-ranking

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CohereRerank
from typing import List, Callable

class RerankingRetriever:
    """Retriever with re-ranking."""

    def __init__(self, base_retriever, top_n: int = 10):
        self.base_retriever = base_retriever
        self.top_n = top_n

    def cross_encoder_rerank(
        self,
        query: str,
        documents: List[Document],
        cross_encoder
    ) -> List[Document]:
        """Re-rank documents using cross-encoder."""
        # Score each document
        scores = []
        for doc in documents:
            score = cross_encoder.predict(
                query,
                doc.page_content
            )
            scores.append(score)

        # Sort by score
        sorted_docs = sorted(
            zip(documents, scores),
            key=lambda x: x[1],
            reverse=True
        )

        # Return top N
        return [doc for doc, score in sorted_docs[:self.top_n]]

    def get_relevant_documents(self, query: str) -> List[Document]:
        """Get re-ranked relevant documents."""
        # Get initial results
        initial_docs = self.base_retriever.get_relevant_documents(query)

        # Re-rank (example with Cohere)
        try:
            from langchain_community.llms import Cohere
            llm = Cohere(cohere_api_key="your-api-key")
            compressor = CohereRerank(top_n=self.top_n)

            retriever = ContextualCompressionRetriever(
                base_compressor=compressor,
                base_retriever=self.base_retriever
            )

            return retriever.get_relevant_documents(query)
        except ImportError:
            return initial_docs

# Usage
reranker = RerankingRetriever(vector_store, top_n=3)
results = reranker.get_relevant_documents("capital of France")
```

---

## 6. Prompt Construction

```python
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from typing import List, Dict

class RAGPromptBuilder:
    """Build RAG-specific prompts."""

    def __init__(self):
        self.templates = {}

    def basic_rag_prompt(self) -> PromptTemplate:
        """Basic RAG prompt template."""
        template = """
Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context:
{context}

Question: {question}

Answer:
"""
        return PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )

    def conversational_rag_prompt(self) -> ChatPromptTemplate:
        """Conversational RAG prompt template."""
        template = """
You are a helpful assistant. Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context:
{context}

Chat History:
{chat_history}

Question: {question}

Answer:
"""
        return ChatPromptTemplate.from_template(template)

    def multi_query_rag_prompt(self) -> PromptTemplate:
        """Multi-query RAG prompt template."""
        template = """
Use the following pieces of context to answer the questions at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context:
{context}

Questions:
{questions}

Answers:
"""
        return PromptTemplate(
            template=template,
            input_variables=["context", "questions"]
        )

    def build_prompt(
        self,
        context: str,
        query: str,
        prompt_type: str = "basic"
    ) -> str:
        """Build prompt with context and query."""
        if prompt_type == "basic":
            prompt = self.basic_rag_prompt()
        elif prompt_type == "conversational":
            prompt = self.conversational_rag_prompt()
        elif prompt_type == "multi_query":
            prompt = self.multi_query_rag_prompt()
        else:
            raise ValueError(f"Unknown prompt type: {prompt_type}")

        return prompt.format(context=context, question=query)

    def build_prompt_with_sources(
        self,
        context: List[Dict],
        query: str
    ) -> str:
        """Build prompt with source citations."""
        context_str = "\n\n".join([
            f"Source {i+1}: {doc['page_content']}"
            for i, doc in enumerate(context)
        ])

        template = """
Use the following pieces of context to answer the question at the end.
Include the source number in your answer.

Context:
{context}

Question: {question}

Answer:
"""
        prompt = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )

        return prompt.format(context=context_str, question=query)

# Usage
prompt_builder = RAGPromptBuilder()

# Basic RAG prompt
prompt = prompt_builder.build_prompt(
    context="Paris is the capital of France.",
    query="What is the capital of France?",
    prompt_type="basic"
)

print(prompt)
```

---

## 7. Response Generation

```python
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from typing import List, Dict

class RAGGenerator:
    """Generate responses using RAG."""

    def __init__(self, llm, retriever):
        self.llm = llm
        self.retriever = retriever

    def create_basic_chain(self):
        """Create basic RAG chain."""
        chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=True
        )
        return chain

    def create_conversational_chain(self):
        """Create conversational RAG chain."""
        chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.retriever,
            return_source_documents=True
        )
        return chain

    def create_map_reduce_chain(self):
        """Create map-reduce RAG chain."""
        chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="map_reduce",
            retriever=self.retriever,
            return_source_documents=True
        )
        return chain

    def create_refine_chain(self):
        """Create refine RAG chain."""
        chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="refine",
            retriever=self.retriever,
            return_source_documents=True
        )
        return chain

    def query(self, query: str, chain_type: str = "basic") -> Dict:
        """Query RAG system."""
        if chain_type == "basic":
            chain = self.create_basic_chain()
        elif chain_type == "conversational":
            chain = self.create_conversational_chain()
        elif chain_type == "map_reduce":
            chain = self.create_map_reduce_chain()
        elif chain_type == "refine":
            chain = self.create_refine_chain()
        else:
            raise ValueError(f"Unknown chain type: {chain_type}")

        result = chain({"query": query})

        return {
            "answer": result["result"],
            "source_documents": result.get("source_documents", [])
        }

    def query_with_sources(self, query: str) -> Dict:
        """Query with source citations."""
        chain = self.create_basic_chain()
        result = chain({"query": query})

        # Format sources
        sources = []
        for doc in result.get("source_documents", []):
            sources.append({
                "content": doc.page_content,
                "metadata": doc.metadata
            })

        return {
            "answer": result["result"],
            "sources": sources
        }

# Usage
llm = ChatOpenAI(model_name="gpt-4")
retriever = SemanticRetriever(vector_store)

generator = RAGGenerator(llm, retriever)

# Query
result = generator.query("What is the capital of France?")
print(f"Answer: {result['answer']}")
print(f"Sources: {len(result['source_documents'])}")
```

---

## 8. Context Window Management

```python
from typing import List
from langchain.docstore.document import Document

class ContextWindowManager:
    """Manage context window for RAG."""

    def __init__(
        self,
        max_context_length: int = 4000,
        context_overlap: int = 200
    ):
        self.max_context_length = max_context_length
        self.context_overlap = context_overlap

    def fit_documents(
        self,
        documents: List[Document],
        query: str
    ) -> List[Document]:
        """Fit documents into context window."""
        # Get document lengths
        doc_lengths = [len(doc.page_content) for doc in documents]

        # Select documents that fit
        selected_docs = []
        total_length = 0

        for doc, length in zip(documents, doc_lengths):
            if total_length + length > self.max_context_length:
                break
            selected_docs.append(doc)
            total_length += length

        return selected_docs

    def sliding_window(
        self,
        documents: List[Document],
        window_size: int = 3
    ) -> List[List[Document]]:
        """Create sliding windows of documents."""
        windows = []

        for i in range(0, len(documents), window_size):
            window = documents[i:i + window_size]
            windows.append(window)

        return windows

    def recursive_context_selection(
        self,
        documents: List[Document],
        query: str,
        max_depth: int = 3
    ) -> List[Document]:
        """Recursively select context based on relevance."""
        # Score documents by relevance to query
        scored_docs = self._score_documents(documents, query)

        # Select top documents
        top_docs = scored_docs[:max_depth]

        return [doc for doc, score in top_docs]

    def _score_documents(
        self,
        documents: List[Document],
        query: str
    ) -> List[tuple]:
        """Score documents by relevance."""
        # Simple scoring based on keyword overlap
        query_words = set(query.lower().split())
        scores = []

        for doc in documents:
            doc_words = set(doc.page_content.lower().split())
            overlap = len(query_words & doc_words)
            scores.append((doc, overlap))

        return sorted(scores, key=lambda x: x[1], reverse=True)

# Usage
context_manager = ContextWindowManager(
    max_context_length=4000,
    context_overlap=200
)

# Fit documents into context
selected_docs = context_manager.fit_documents(documents, "capital of France")
print(f"Selected {len(selected_docs)} documents for context")
```

---

## 9. RAG Evaluation

```python
from typing import List, Dict
from langchain.evaluation import load_evaluator, EvaluatorType
import numpy as np

class RAGEvaluator:
    """Evaluate RAG system performance."""

    def __init__(self, rag_chain, retriever):
        self.rag_chain = rag_chain
        self.retriever = retriever

    def evaluate_retrieval(
        self,
        questions: List[str],
        ground_truth: List[List[str]]
    ) -> Dict[str, float]:
        """Evaluate retrieval performance."""
        results = {
            "precision": [],
            "recall": [],
            "f1": []
        }

        for question, truth in zip(questions, ground_truth):
            # Retrieve documents
            retrieved = self.retriever.get_relevant_documents(question)
            retrieved_texts = [doc.page_content for doc in retrieved]

            # Calculate metrics
            true_positives = len(set(truth) & set(retrieved_texts))
            precision = true_positives / len(retrieved_texts) if retrieved_texts else 0
            recall = true_positives / len(truth) if truth else 0
            f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

            results["precision"].append(precision)
            results["recall"].append(recall)
            results["f1"].append(f1)

        return {
            "avg_precision": np.mean(results["precision"]),
            "avg_recall": np.mean(results["recall"]),
            "avg_f1": np.mean(results["f1"])
        }

    def evaluate_generation(
        self,
        questions: List[str],
        answers: List[str],
        ground_truth: List[str]
    ) -> Dict[str, float]:
        """Evaluate generation performance."""
        # Use LangChain evaluator
        evaluator = load_evaluator("exact_match")

        results = []
        for question, answer, truth in zip(questions, answers, ground_truth):
            result = evaluator.evaluate_strings(
                prediction=answer,
                reference=truth
            )
            results.append(result)

        return {
            "exact_match_rate": np.mean(results),
            "total_questions": len(results)
        }

    def evaluate_rag(
        self,
        questions: List[str],
        ground_truth_answers: List[str],
        ground_truth_contexts: List[List[str]]
    ) -> Dict[str, float]:
        """Evaluate complete RAG pipeline."""
        # Evaluate retrieval
        retrieval_metrics = self.evaluate_retrieval(
            questions,
            ground_truth_contexts
        )

        # Evaluate generation
        generated_answers = []
        for question in questions:
            result = self.rag_chain({"query": question})
            generated_answers.append(result["result"])

        generation_metrics = self.evaluate_generation(
            questions,
            generated_answers,
            ground_truth_answers
        )

        return {
            "retrieval": retrieval_metrics,
            "generation": generation_metrics
        }

# Usage
evaluator = RAGEvaluator(rag_chain, retriever)

# Evaluate
questions = ["What is the capital of France?", "What is the capital of Germany?"]
ground_truth_answers = ["Paris", "Berlin"]
ground_truth_contexts = [
    ["Paris is the capital of France."],
    ["Berlin is the capital of Germany."]
]

metrics = evaluator.evaluate_rag(
    questions,
    ground_truth_answers,
    ground_truth_contexts
)

print(f"Retrieval F1: {metrics['retrieval']['avg_f1']:.3f}")
print(f"Generation Exact Match: {metrics['generation']['exact_match_rate']:.3f}")
```

---

## 10. Advanced Patterns

### 10.1 Multi-Query Retrieval

```python
from langchain.prompts import PromptTemplate
from typing import List

class MultiQueryRetriever:
    """Generate multiple queries for better retrieval."""

    def __init__(self, base_retriever, llm):
        self.base_retriever = base_retriever
        self.llm = llm

    def generate_queries(self, query: str, num_queries: int = 3) -> List[str]:
        """Generate multiple queries."""
        prompt = PromptTemplate.from_template("""
Generate {num_queries} different search queries for the following question.
Each query should be on a new line.

Question: {question}

Queries:
""")

        response = self.llm.predict(
            prompt.format(question=query, num_queries=num_queries)
        )

        queries = response.strip().split('\n')
        return [q.strip() for q in queries if q.strip()]

    def get_relevant_documents(self, query: str) -> List:
        """Retrieve using multiple queries."""
        # Generate queries
        queries = self.generate_queries(query)

        # Retrieve for each query
        all_documents = []
        for q in queries:
            docs = self.base_retriever.get_relevant_documents(q)
            all_documents.extend(docs)

        # Deduplicate
        seen = set()
        unique_docs = []
        for doc in all_documents:
            doc_hash = hash(doc.page_content)
            if doc_hash not in seen:
                seen.add(doc_hash)
                unique_docs.append(doc)

        return unique_docs

# Usage
multi_query_retriever = MultiQueryRetriever(vector_store, llm)
results = multi_query_retriever.get_relevant_documents("capital of France")
```

### 10.2 Self-Querying

```python
from typing import List

class SelfQueryRetriever:
    """Self-querying for metadata filtering."""

    def __init__(self, vector_store, llm):
        self.vector_store = vector_store
        self.llm = llm

    def extract_metadata_query(
        self,
        query: str
    ) -> Dict[str, str]:
        """Extract metadata filters from query."""
        prompt = f"""
Analyze the following query and extract any metadata filters.
Return the result as a JSON object with "filters" key containing the metadata conditions.

Query: {query}

Example output:
{{
    "filters": "year > 2020 AND category = 'technology'"
}}
"""

        response = self.llm.predict(prompt)

        # Parse JSON response
        try:
            import json
            result = json.loads(response)
            return result.get("filters", {})
        except:
            return {}

    def get_relevant_documents(
        self,
        query: str
    ) -> List:
        """Retrieve documents with metadata filtering."""
        # Extract metadata filters
        filters = self.extract_metadata_query(query)

        # Retrieve with filters
        if filters:
            return self.vector_store.similarity_search(
                query,
                k=4,
                filter=filters
            )
        else:
            return self.vector_store.similarity_search(query, k=4)

# Usage
self_query_retriever = SelfQueryRetriever(vector_store, llm)
results = self_query_retriever.get_relevant_documents("recent technology documents")
```

### 10.3 Parent Document Retrieval

```python
from typing import List, Dict
from langchain.docstore.document import Document

class ParentDocumentRetriever:
    """Retrieve parent documents for better context."""

    def __init__(self, documents: List[Document], child_splitter):
        self.documents = documents
        self.child_splitter = child_splitter

    def create_child_documents(self) -> List[Document]:
        """Create child chunks from parent documents."""
        child_docs = []

        for i, parent_doc in enumerate(self.documents):
            # Split parent document
            child_chunks = self.child_splitter.split_documents([parent_doc])

            # Add parent reference
            for child_doc in child_chunks:
                child_doc.metadata["parent_id"] = i
                child_docs.append(child_doc)

        return child_docs

    def get_relevant_documents(
        self,
        query: str,
        k: int = 4
    ) -> List[Document]:
        """Retrieve parent documents."""
        # Get child documents
        child_docs = self.create_child_documents()

        # Retrieve relevant child documents
        # (Assuming vector store is set up)
        relevant_children = self.vector_store.similarity_search(query, k=k)

        # Get unique parent documents
        parent_ids = set()
        parent_docs = []

        for child in relevant_children:
            parent_id = child.metadata.get("parent_id")
            if parent_id not in parent_ids:
                parent_ids.add(parent_id)
                parent_docs.append(self.documents[parent_id])

        return parent_docs

# Usage
parent_retriever = ParentDocumentRetriever(documents, chunker)
results = parent_retriever.get_relevant_documents("capital of France")
```

---

## 11. Production Optimization

### 11.1 Caching

```python
from langchain.cache import (
    InMemoryCache,
    GPTCache,
    RedisCache,
    SQLAlchemyCache
)
from typing import Dict

class RAGCache:
    """Cache RAG responses."""

    def __init__(self, cache_type: str = "memory"):
        self.cache_type = cache_type
        self.cache = self._get_cache()

    def _get_cache(self):
        """Get cache instance."""
        if self.cache_type == "memory":
            return InMemoryCache()
        elif self.cache_type == "gpt":
            return GPTCache()
        elif self.cache_type == "redis":
            import redis
            return RedisCache(redis.Redis())
        elif self.cache_type == "sql":
            return SQLAlchemyCache(
                database_uri="sqlite:///cache.db"
            )
        else:
            raise ValueError(f"Unknown cache type: {self.cache_type}")

    def get(self, prompt: str) -> str:
        """Get cached response."""
        return self.cache.lookup(prompt)

    def set(self, prompt: str, response: str):
        """Cache response."""
        self.cache.update(prompt, response)

    def clear(self):
        """Clear cache."""
        self.cache.clear()

# Usage
cache = RAGCache(cache_type="memory")

# Check cache
cached_response = cache.get("capital of France")
if cached_response:
    print(f"Cached: {cached_response}")
else:
    # Generate response
    response = rag_chain({"query": "capital of France"})
    cache.set("capital of France", response["result"])
```

### 11.2 Batch Processing

```python
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed

class BatchRAGProcessor:
    """Process multiple RAG queries efficiently."""

    def __init__(self, rag_chain, max_workers: int = 4):
        self.rag_chain = rag_chain
        self.max_workers = max_workers

    def process_single(self, query: str) -> Dict:
        """Process single query."""
        result = self.rag_chain({"query": query})
        return {
            "query": query,
            "answer": result["result"],
            "sources": result.get("source_documents", [])
        }

    def process_batch(self, queries: List[str]) -> List[Dict]:
        """Process batch of queries."""
        results = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self.process_single, query): query
                for query in queries
            }

            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    print(f"Error processing query: {e}")

        return results

    def process_batch_async(self, queries: List[str]) -> List[Dict]:
        """Process batch asynchronously."""
        import asyncio

        async def async_process(query):
            result = await self.rag_chain.acall({"query": query})
            return {
                "query": query,
                "answer": result["result"],
                "sources": result.get("source_documents", [])
            }

        async def process_all():
            tasks = [async_process(q) for q in queries]
            return await asyncio.gather(*tasks)

        return asyncio.run(process_all())

# Usage
processor = BatchRAGProcessor(rag_chain, max_workers=4)

queries = [
    "What is the capital of France?",
    "What is the capital of Germany?",
    "What is the capital of Italy?"
]

results = processor.process_batch(queries)
```

---

## 12. Common Pitfalls

### 12.1 Common Issues

```python
# 1. Poor chunking
# Problem: Chunks are too small or too large
# Solution: Use appropriate chunk size for your model

# 2. Insufficient context
# Problem: Not enough context in retrieved documents
# Solution: Increase k or use parent document retrieval

# 3. Irrelevant retrieval
# Problem: Retrieved documents don't contain answer
# Solution: Use multi-query retrieval or re-ranking

# 4. Hallucination
# Problem: LLM generates incorrect information
# Solution: Add source citations and verify answers

# 5. Slow performance
# Problem: Retrieval is slow
# Solution: Use efficient vector store (FAISS) and caching

class RAGValidator:
    """Validate RAG system for common issues."""

    @staticmethod
    def validate_chunking(documents: List[Document]) -> Dict[str, bool]:
        """Validate document chunking."""
        issues = {
            "too_small": False,
            "too_large": False,
            "inconsistent": False
        }

        lengths = [len(doc.page_content) for doc in documents]
        avg_length = sum(lengths) / len(lengths)

        if avg_length < 100:
            issues["too_small"] = True
        if avg_length > 2000:
            issues["too_large"] = True

        # Check consistency
        if lengths:
            std_dev = (sum((x - avg_length) ** 2 for x in lengths) / len(lengths)) ** 0.5
            if std_dev > avg_length * 0.5:
                issues["inconsistent"] = True

        return issues

    @staticmethod
    def validate_retrieval(
        query: str,
        retrieved_docs: List[Document],
        answer: str
    ) -> Dict[str, bool]:
        """Validate retrieval quality."""
        issues = {
            "no_relevant_docs": False,
            "answer_not_in_docs": False
        }

        if not retrieved_docs:
            issues["no_relevant_docs"] = True
            return issues

        # Check if answer is in retrieved documents
        answer_words = set(answer.lower().split())
        doc_words = set()
        for doc in retrieved_docs:
            doc_words.update(doc.page_content.lower().split())

        overlap = len(answer_words & doc_words) / len(answer_words) if answer_words else 0
        if overlap < 0.3:
            issues["answer_not_in_docs"] = True

        return issues

# Usage
validator = RAGValidator()

chunking_issues = validator.validate_chunking(documents)
retrieval_issues = validator.validate_retrieval(
    "capital of France",
    retrieved_docs,
    answer
)

print(f"Chunking issues: {chunking_issues}")
print(f"Retrieval issues: {retrieval_issues}")
```

---

## Related Skills

- [`06-ai-ml-production/embedding-models`](06-ai-ml-production/embedding-models/SKILL.md)
- [`06-ai-ml-production/vector-search`](06-ai-ml-production/vector-search/SKILL.md)
- [`06-ai-ml-production/vector-search-patterns`](06-ai-ml-production/vector-search-patterns/SKILL.md)
- [`06-ai-ml-production/prompt-engineering`](06-ai-ml-production/prompt-engineering/SKILL.md)
- [`06-ai-ml-production/llm-integration`](06-ai-ml-production/llm-integration/SKILL.md)
- [`07-document-processing/rag-architecture-patterns`](07-document-processing/rag-architecture-patterns/SKILL.md)
- [`07-document-processing/rag-chunking-metadata-strategy`](07-document-processing/rag-chunking-metadata-strategy/SKILL.md)

## Additional Resources

- [LangChain Documentation](https://python.langchain.com/)
- [LangChain RAG Tutorial](https://python.langchain.com/docs/use_cases/question_answering/)
- [FAISS Documentation](https://faiss.ai/)
- [Chroma Documentation](https://docs.trychroma.com/)
