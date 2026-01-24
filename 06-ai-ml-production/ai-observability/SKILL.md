---
name: AI/ML Observability and Monitoring
description: Comprehensive guide to monitoring AI/ML systems in production, including LLMs, RAG applications, and traditional ML models.
---

# AI/ML Observability and Monitoring

## Overview

Comprehensive guide to monitoring AI/ML systems in production, including LLMs, RAG applications, and traditional ML models. This skill covers monitoring stack setup (Prometheus, Grafana, Jaeger, Phoenix), metrics tracking (latency, throughput, token usage, cost, errors), model performance monitoring, data drift detection, LLM interaction logging, tracing with LangSmith/Phoenix, alerting strategies, dashboards, A/B test monitoring, cost optimization, debugging patterns, and production deployment checklists.

## Prerequisites

- Understanding of observability concepts (metrics, logs, traces)
- Familiarity with monitoring tools (Prometheus, Grafana)
- Knowledge of LLM APIs and their pricing models
- Understanding of statistical concepts for drift detection
- Familiarity with Docker and container orchestration
- Knowledge of FastAPI and middleware patterns

## Key Concepts

### Monitoring Stack Components

- **Prometheus**: Metrics collection and storage
- **Grafana**: Visualization and dashboards
- **Loki/Promtail**: Log aggregation
- **Jaeger**: Distributed tracing
- **Phoenix/Arize**: AI-specific observability
- **LangSmith**: LangChain tracing and debugging

### Key Metrics

- **Latency**: Request/response time (P50, P95, P99)
- **Throughput**: Requests per second/minute
- **Token Usage**: Input/output tokens per model
- **Cost**: USD cost per model and endpoint
- **Error Rates**: Rate limit, timeout, validation errors

### Model Performance Metrics

- **Classification**: Accuracy, F1, precision, recall
- **Generation**: ROUGE scores, BLEU, semantic similarity
- **RAG**: Precision@K, Recall@K, MRR, NDCG

### Drift Detection

- **Statistical Drift**: KS test, JS divergence, population stability index
- **Embedding Drift**: Centroid distance, similarity shift
- **Concept Drift**: Changes in model behavior over time

### Tracing

- **OpenTelemetry**: Standard tracing framework
- **LangSmith Tracer**: LangChain-specific tracing
- **Phoenix Instrumentor**: Automatic tracing for LangChain

## Implementation Guide

### Monitoring Stack

#### Docker Compose Setup

```yaml
# docker-compose.yml for observability stack
version: '3.8'

services:
  # Metrics Collection
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  # Visualization
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-storage:/var/lib/grafana

  # Logs
  loki:
    image: grafana/loki:latest
    ports:
      - "3100:3100"

  promtail:
    image: grafana/promtail:latest
    volumes:
      - ./promtail.yml:/etc/promtail/promtail.yml
      - /var/log:/var/log:ro

  # Tracing
  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686"
      - "14268:14268"

  # AI-Specific Observability
  arize:
    image: arizephoenix/phoenix:latest
    ports:
      - "6006:6006"

volumes:
  grafana-storage:
```

#### LangSmith Setup

```python
# langsmith_config.py
import os
from langsmith import Client

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-api-key"
os.environ["LANGCHAIN_PROJECT"] = "my-ai-app"

client = Client()
```

### Metrics to Track

#### Latency Tracking

```python
# metrics_collector.py
from prometheus_client import Histogram, Counter, Gauge
import time

# Request latency histogram
request_latency = Histogram(
    'llm_request_latency_seconds',
    'LLM request latency',
    ['model', 'endpoint']
)

@request_latency.time()
def track_llm_request(model: str, endpoint: str):
    # Decorator for tracking latency
    pass

# Manual tracking
start_time = time.time()
response = call_llm()
duration = time.time() - start_time
request_latency.labels(model='gpt-4', endpoint='/chat').observe(duration)
```

#### Throughput Tracking

```python
# Requests per second
requests_total = Counter(
    'llm_requests_total',
    'Total LLM requests',
    ['model', 'status']
)

requests_per_minute = Gauge(
    'llm_requests_per_minute',
    'LLM requests per minute',
    ['model']
)

# Track throughput
def track_request(model: str, status: str):
    requests_total.labels(model=model, status=status).inc()
```

#### Token Usage Tracking

```python
# Token usage tracking
token_usage = Counter(
    'llm_token_usage_total',
    'Total tokens used',
    ['model', 'type']  # type: input, output
)

token_cost = Counter(
    'llm_token_cost_usd',
    'Total cost in USD',
    ['model']
)

def track_tokens(model: str, input_tokens: int, output_tokens: int):
    token_usage.labels(model=model, type='input').inc(input_tokens)
    token_usage.labels(model=model, type='output').inc(output_tokens)

    # Calculate cost
    input_cost = input_tokens * INPUT_COST_PER_1K[model] / 1000
    output_cost = output_tokens * OUTPUT_COST_PER_1K[model] / 1000
    token_cost.labels(model=model).inc(input_cost + output_cost)
```

#### Cost Tracking

```python
# Cost tracking configuration
COST_PER_1K_TOKENS = {
    'gpt-4': {'input': 0.03, 'output': 0.06},
    'gpt-3.5-turbo': {'input': 0.0015, 'output': 0.002},
    'claude-3-opus': {'input': 0.015, 'output': 0.075},
}

def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    costs = COST_PER_1K_TOKENS.get(model, {'input': 0, 'output': 0})
    return (input_tokens * costs['input'] + output_tokens * costs['output']) / 1000

# Daily cost tracking
daily_cost = Gauge(
    'llm_daily_cost_usd',
    'Daily LLM cost',
    ['model', 'date']
)
```

#### Error Rate Tracking

```python
# Error tracking
error_total = Counter(
    'llm_errors_total',
    'Total LLM errors',
    ['model', 'error_type']
)

error_rate = Gauge(
    'llm_error_rate',
    'LLM error rate',
    ['model']
)

ERROR_TYPES = [
    'rate_limit_exceeded',
    'invalid_request',
    'timeout',
    'content_filter',
    'model_not_found',
]

def track_error(model: str, error_type: str):
    if error_type in ERROR_TYPES:
        error_total.labels(model=model, error_type=error_type).inc()
```

### Model Performance Monitoring

#### Quality Metrics

```python
# quality_metrics.py
from sklearn.metrics import accuracy_score, f1_score, precision_recall_fscore_support
from rouge_score import rouge_scorer
import numpy as np

class QualityMonitor:
    def __init__(self):
        self.rouge_scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)

    def track_classification(self, y_true, y_pred):
        """Track classification metrics"""
        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'f1': f1_score(y_true, y_pred, average='weighted'),
            'precision_recall': precision_recall_fscore_support(y_true, y_pred)
        }
        return metrics

    def track_generation_quality(self, reference: str, generated: str):
        """Track text generation quality"""
        scores = self.rouge_scorer.score(reference, generated)
        return {
            'rouge1': scores['rouge1'].fmeasure,
            'rouge2': scores['rouge2'].fmeasure,
            'rougeL': scores['rougeL'].fmeasure
        }

    def track_rag_retrieval(self, relevant_docs: list, retrieved_docs: list, k: int = 10):
        """Track RAG retrieval quality"""
        # Precision@K
        precision = len(set(relevant_docs) & set(retrieved_docs[:k])) / k

        # Recall@K
        recall = len(set(relevant_docs) & set(retrieved_docs[:k])) / len(relevant_docs) if relevant_docs else 0

        # MRR (Mean Reciprocal Rank)
        mrr = 0
        for i, doc in enumerate(retrieved_docs[:k], 1):
            if doc in relevant_docs:
                mrr = 1 / i
                break

        return {'precision_at_k': precision, 'recall_at_k': recall, 'mrr': mrr}
```

#### Feedback Collection

```python
# feedback_collector.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from datetime import datetime

class Feedback(BaseModel):
    request_id: str
    user_id: str
    rating: int  # 1-5 stars
    comment: str = None
    helpful: bool = None

app = FastAPI()

@app.post("/feedback")
async def collect_feedback(feedback: Feedback):
    """Collect user feedback on AI responses"""
    feedback_data = {
        **feedback.dict(),
        'timestamp': datetime.utcnow().isoformat()
    }

    # Store feedback
    await store_feedback(feedback_data)

    # Update metrics
    update_feedback_metrics(feedback.rating, feedback.helpful)

    return {"status": "recorded"}

def update_feedback_metrics(rating: int, helpful: bool):
    """Update feedback metrics"""
    # Track average rating
    # Track helpful percentage
    pass
```

### Data Drift Detection

#### Statistical Drift Detection

```python
# drift_detection.py
import numpy as np
from scipy import stats
from scipy.spatial.distance import jensenshannon
import pandas as pd

class DriftDetector:
    def __init__(self, reference_data: pd.DataFrame):
        self.reference_data = reference_data
        self.reference_stats = self._calculate_stats(reference_data)

    def _calculate_stats(self, data: pd.DataFrame):
        """Calculate reference statistics"""
        stats_dict = {}
        for column in data.select_dtypes(include=[np.number]).columns:
            stats_dict[column] = {
                'mean': data[column].mean(),
                'std': data[column].std(),
                'min': data[column].min(),
                'max': data[column].max(),
                'percentiles': data[column].quantile([0.25, 0.5, 0.75]).to_dict()
            }
        return stats_dict

    def detect_drift(self, current_data: pd.DataFrame, threshold: float = 0.05):
        """Detect statistical drift"""
        drift_results = {}

        for column in current_data.select_dtypes(include=[np.number]).columns:
            if column in self.reference_stats:
                # Kolmogorov-Smirnov test
                ks_stat, p_value = stats.ks_2samp(
                    self.reference_data[column],
                    current_data[column]
                )

                drift_results[column] = {
                    'ks_statistic': ks_stat,
                    'p_value': p_value,
                    'drift_detected': p_value < threshold
                }

        return drift_results

    def detect_distribution_drift(self, current_data: pd.DataFrame):
        """Detect distribution drift using JS divergence"""
        drift_results = {}

        for column in current_data.select_dtypes(include=[np.number]).columns:
            # Create histograms
            ref_hist, ref_bins = np.histogram(self.reference_data[column], bins=20, density=True)
            curr_hist, _ = np.histogram(current_data[column], bins=ref_bins, density=True)

            # Calculate Jensen-Shannon divergence
            js_divergence = jensenshannon(ref_hist, curr_hist)

            drift_results[column] = {
                'js_divergence': js_divergence,
                'drift_detected': js_divergence > 0.1  # Threshold
            }

        return drift_results
```

#### Embedding Drift Detection

```python
# embedding_drift.py
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class EmbeddingDriftDetector:
    def __init__(self, reference_embeddings: np.ndarray):
        self.reference_embeddings = reference_embeddings
        self.reference_centroid = np.mean(reference_embeddings, axis=0)

    def detect_drift(self, current_embeddings: np.ndarray, threshold: float = 0.1):
        """Detect drift in embedding space"""
        current_centroid = np.mean(current_embeddings, axis=0)

        # Calculate centroid distance
        centroid_distance = 1 - cosine_similarity(
            [self.reference_centroid],
            [current_centroid]
        )[0][0]

        # Calculate average pairwise similarity
        ref_similarities = []
        curr_similarities = []

        for i in range(min(100, len(self.reference_embeddings))):
            ref_sim = np.mean(cosine_similarity(
                [self.reference_embeddings[i]],
                self.reference_embeddings[:100]
            ))
            ref_similarities.append(ref_sim)

        for i in range(min(100, len(current_embeddings))):
            curr_sim = np.mean(cosine_similarity(
                [current_embeddings[i]],
                current_embeddings[:100]
            ))
            curr_similarities.append(curr_sim)

        similarity_shift = abs(np.mean(ref_similarities) - np.mean(curr_similarities))

        return {
            'centroid_distance': centroid_distance,
            'similarity_shift': similarity_shift,
            'drift_detected': centroid_distance > threshold or similarity_shift > threshold
        }
```

### Logging LLM Interactions

#### Structured Logging

```python
# llm_logger.py
import json
import uuid
from datetime import datetime
from typing import Dict, Any, Optional

class LLMLogger:
    def __init__(self, log_file: str = "llm_interactions.jsonl"):
        self.log_file = log_file

    def log_interaction(
        self,
        model: str,
        prompt: str,
        response: str,
        input_tokens: int,
        output_tokens: int,
        latency: float,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Log LLM interaction"""
        interaction = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "model": model,
            "prompt": prompt,
            "response": response,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "latency_seconds": latency,
            "metadata": metadata or {}
        }

        with open(self.log_file, 'a') as f:
            f.write(json.dumps(interaction) + '\n')

        return interaction["id"]

    def log_rag_interaction(
        self,
        query: str,
        retrieved_docs: list,
        response: str,
        retrieval_scores: list,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Log RAG interaction"""
        interaction = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "type": "rag",
            "query": query,
            "retrieved_docs": retrieved_docs,
            "retrieval_scores": retrieval_scores,
            "response": response,
            "metadata": metadata or {}
        }

        with open(self.log_file, 'a') as f:
            f.write(json.dumps(interaction) + '\n')

        return interaction["id"]
```

#### Middleware for FastAPI

```python
# llm_middleware.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
import json

class LLMMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, logger: LLMLogger):
        super().__init__(app)
        self.logger = logger

    async def dispatch(self, request: Request, call_next):
        # Start timer
        start_time = time.time()

        # Process request
        response = await call_next(request)

        # Calculate latency
        process_time = time.time() - start_time

        # Log if it's an LLM endpoint
        if request.url.path.startswith("/api/llm"):
            # Extract request body (if available)
            body = await request.body()

            # Log interaction
            self.logger.log_interaction(
                model=request.headers.get("X-Model", "unknown"),
                prompt=body.decode(),
                response="",
                input_tokens=0,
                output_tokens=0,
                latency=process_time
            )

        # Add latency header
        response.headers["X-Process-Time"] = str(process_time)

        return response
```

### Tracing with LangSmith/Phoenix

#### LangSmith Integration

```python
# langsmith_tracing.py
from langchain_openai import ChatOpenAI
from langchain.callbacks.tracers import LangChainTracer
from langchain.schema import HumanMessage

# Initialize tracer
tracer = LangChainTracer(project_name="my-ai-app")

# Initialize LLM with tracing
llm = ChatOpenAI(
    model="gpt-4",
    temperature=0,
    callbacks=[tracer]
)

# Run with automatic tracing
response = llm.invoke([HumanMessage(content="Hello, world!")])
print(response.content)
```

#### Phoenix Integration

```python
# phoenix_tracing.py
import phoenix as px
from phoenix.trace.langchain import LangChainInstrumentor
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

# Start Phoenix UI
px.launch_app()

# Instrument LangChain
LangChainInstrumentor().instrument()

# Use LangChain as normal
llm = ChatOpenAI(model="gpt-4")
response = llm.invoke([HumanMessage(content="Hello, world!")])
```

#### Custom Tracing

```python
# custom_tracing.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

# Setup tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Setup Jaeger exporter
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)
span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Trace LLM call
def traced_llm_call(prompt: str):
    with tracer.start_as_current_span("llm_call") as span:
        span.set_attribute("prompt", prompt)

        # Call LLM
        response = call_llm(prompt)

        span.set_attribute("response", response)
        span.set_attribute("tokens", count_tokens(response))

        return response
```

### Alerting Strategies

#### Prometheus Alerting Rules

```yaml
# alert_rules.yml
groups:
  - name: llm_alerts
    interval: 30s
    rules:
      # High latency alert
      - alert: HighLLMLatency
        expr: histogram_quantile(0.95, llm_request_latency_seconds_bucket) > 30
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High LLM latency detected"
          description: "95th percentile latency is {{ $value }}s for model {{ $labels.model }}"

      # High error rate alert
      - alert: HighLLMErrorRate
        expr: rate(llm_errors_total[5m]) / rate(llm_requests_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High LLM error rate detected"
          description: "Error rate is {{ $value | humanizePercentage }}"

      # Cost alert
      - alert: HighDailyCost
        expr: llm_daily_cost_usd > 100
        labels:
          severity: warning
        annotations:
          summary: "Daily cost exceeds threshold"
          description: "Daily cost is ${{ $value }}"

      # Data drift alert
      - alert: DataDriftDetected
        expr: data_drift_detected == 1
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Data drift detected"
          description: "Drift detected in {{ $labels.feature }}"
```

#### Custom Alerting

```python
# alert_manager.py
from typing import Callable, Dict, Any
import smtplib
from email.mime.text import MIMEText

class AlertManager:
    def __init__(self):
        self.alert_handlers: Dict[str, Callable] = {}
        self.alert_history = []

    def register_handler(self, alert_type: str, handler: Callable):
        """Register alert handler"""
        self.alert_handlers[alert_type] = handler

    def trigger_alert(self, alert_type: str, data: Dict[str, Any]):
        """Trigger an alert"""
        self.alert_history.append({
            'type': alert_type,
            'data': data,
            'timestamp': datetime.utcnow().isoformat()
        })

        if alert_type in self.alert_handlers:
            self.alert_handlers[alert_type](data)

    def email_alert(self, data: Dict[str, Any]):
        """Send email alert"""
        msg = MIMEText(data['message'])
        msg['Subject'] = data['subject']
        msg['From'] = 'alerts@example.com'
        msg['To'] = data['recipient']

        with smtplib.SMTP('smtp.example.com') as server:
            server.send_message(msg)

    def slack_alert(self, data: Dict[str, Any]):
        """Send Slack alert"""
        import requests

        webhook_url = data['webhook_url']
        payload = {
            'text': data['message'],
            'attachments': data.get('attachments', [])
        }

        requests.post(webhook_url, json=payload)

# Usage
alert_manager = AlertManager()
alert_manager.register_handler('high_latency', alert_manager.email_alert)
alert_manager.register_handler('high_error_rate', alert_manager.slack_alert)
```

### Dashboards

#### Grafana Dashboard Configuration

```json
{
  "dashboard": {
    "title": "AI/ML Observability",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [
          {
            "expr": "rate(llm_requests_total[5m])",
            "legendFormat": "{{model}}"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Latency (P95)",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, llm_request_latency_seconds_bucket)",
            "legendFormat": "{{model}}"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Token Usage",
        "targets": [
          {
            "expr": "rate(llm_token_usage_total[5m])",
            "legendFormat": "{{model}} - {{type}}"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Error Rate",
        "targets": [
          {
            "expr": "rate(llm_errors_total[5m]) / rate(llm_requests_total[5m])",
            "legendFormat": "{{model}}"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Daily Cost",
        "targets": [
          {
            "expr": "llm_daily_cost_usd",
            "legendFormat": "{{model}}"
          }
        ],
        "type": "stat"
      }
    ]
  }
}
```

### A/B Test Monitoring

#### A/B Test Setup

```python
# ab_test_monitor.py
from typing import Dict, Any
import numpy as np
from scipy import stats

class ABTestMonitor:
    def __init__(self):
        self.experiments = {}

    def create_experiment(self, name: str, variants: list):
        """Create A/B test experiment"""
        self.experiments[name] = {
            'variants': {v: {'metrics': []} for v in variants},
            'created_at': datetime.utcnow()
        }

    def record_metric(self, experiment: str, variant: str, metric: float):
        """Record metric for variant"""
        if experiment in self.experiments:
            self.experiments[experiment]['variants'][variant]['metrics'].append(metric)

    def analyze_experiment(self, experiment: str, metric_name: str = "metric"):
        """Analyze A/B test results"""
        if experiment not in self.experiments:
            return None

        variants = self.experiments[experiment]['variants']
        results = {}

        for variant_name, data in variants.items():
            metrics = data['metrics']
            results[variant_name] = {
                'mean': np.mean(metrics),
                'std': np.std(metrics),
                'count': len(metrics)
            }

        # Statistical significance test
        variant_names = list(results.keys())
        if len(variant_names) == 2:
            t_stat, p_value = stats.ttest_ind(
                variants[variant_names[0]]['metrics'],
                variants[variant_names[1]]['metrics']
            )
            results['significance'] = {
                't_statistic': t_stat,
                'p_value': p_value,
                'significant': p_value < 0.05
            }

        return results

# Usage
monitor = ABTestMonitor()
monitor.create_experiment('model_comparison', ['gpt-4', 'gpt-3.5-turbo'])

# Record metrics (e.g., user satisfaction ratings)
monitor.record_metric('model_comparison', 'gpt-4', 4.5)
monitor.record_metric('model_comparison', 'gpt-3.5-turbo', 4.2)

# Analyze
results = monitor.analyze_experiment('model_comparison')
```

### Cost Optimization

#### Cost Tracking and Optimization

```python
# cost_optimizer.py
from typing import Dict, List
import heapq

class CostOptimizer:
    def __init__(self):
        self.usage_history = []

    def recommend_model(
        self,
        task_type: str,
        complexity: str,
        budget_constraint: float
    ) -> str:
        """Recommend model based on task and budget"""
        model_recommendations = {
            'simple': {
                'low': 'gpt-3.5-turbo',
                'medium': 'gpt-3.5-turbo',
                'high': 'gpt-4'
            },
            'complex': {
                'low': 'gpt-3.5-turbo',
                'medium': 'gpt-4',
                'high': 'gpt-4'
            }
        }

        return model_recommendations.get(complexity, {}).get(task_type, 'gpt-3.5-turbo')

    def optimize_token_usage(self, prompt: str, max_tokens: int = 1000) -> str:
        """Optimize prompt to reduce token usage"""
        # Remove redundant content
        # Summarize long contexts
        # Use system prompts efficiently
        optimized = prompt[:max_tokens * 4]  # Rough approximation
        return optimized

    def batch_requests(self, requests: List[Dict], batch_size: int = 10):
        """Batch requests for efficiency"""
        for i in range(0, len(requests), batch_size):
            batch = requests[i:i + batch_size]
            yield batch

    def cache_responses(self, cache_key: str, response: str, ttl: int = 3600):
        """Cache responses to avoid duplicate calls"""
        # Implement caching logic
        pass
```

### Debugging Patterns

#### Common Issues and Solutions

```python
# debugging_patterns.py

class LLMDbugger:
    @staticmethod
    def debug_high_latency(latency: float, model: str):
        """Debug high latency issues"""
        issues = []

        if latency > 30:
            issues.append("Consider using a faster model")
            issues.append("Check network connectivity")
            issues.append("Review prompt complexity")

        if model == 'gpt-4' and latency > 60:
            issues.append("GPT-4 has higher latency, consider GPT-3.5 for simpler tasks")

        return issues

    @staticmethod
    def debug_high_error_rate(error_rate: float, error_types: Dict[str, int]):
        """Debug high error rate"""
        issues = []

        if 'rate_limit_exceeded' in error_types and error_types['rate_limit_exceeded'] > 10:
            issues.append("Implement rate limiting and retry logic")
            issues.append("Consider upgrading API tier")

        if 'timeout' in error_types and error_types['timeout'] > 5:
            issues.append("Increase timeout duration")
            issues.append("Check for network issues")

        return issues

    @staticmethod
    def debug_quality_degradation(quality_metrics: Dict[str, float]):
        """Debug quality degradation"""
        issues = []

        if quality_metrics.get('rougeL', 1.0) < 0.5:
            issues.append("Check for data drift")
            issues.append("Review prompt templates")
            issues.append("Consider fine-tuning model")

        return issues
```

### Production Checklist

#### Pre-Deployment Checklist

```markdown
## Monitoring
- [ ] All metrics are being collected
- [ ] Dashboards are configured and tested
- [ ] Alert rules are set up
- [ ] Alert notifications are configured
- [ ] Log retention policy is defined

## Performance
- [ ] Latency SLAs are defined
- [ ] Throughput capacity is tested
- [ ] Cost budget is set
- [ ] Rate limiting is configured
- [ ] Caching strategy is implemented

## Reliability
- [ ] Retry logic is implemented
- [ ] Fallback mechanisms are in place
- [ ] Circuit breakers are configured
- [ ] Health checks are implemented
- [ ] Graceful degradation is tested

## Security
- [ ] API keys are stored securely
- [ ] Sensitive data is masked in logs
- [ ] Access controls are implemented
- [ ] Audit logging is enabled
- [ ] Content filtering is configured

## Quality
- [ ] Quality metrics are tracked
- [ ] A/B testing framework is ready
- [ ] Feedback collection is implemented
- [ ] Data drift detection is configured
- [ ] Model performance is monitored

## Operations
- [ ] Deployment pipeline is tested
- [ ] Rollback procedure is documented
- [ ] On-call rotation is defined
- [ ] Runbook is created
- [ ] Incident response plan is ready
```

#### Post-Deployment Monitoring

```python
# post_deployment_monitor.py

class PostDeploymentMonitor:
    def __init__(self, baseline_metrics: Dict[str, float]):
        self.baseline = baseline_metrics

    def check_deployment_health(self, current_metrics: Dict[str, float]) -> Dict[str, bool]:
        """Check if deployment is healthy"""
        health_status = {}

        # Check latency
        health_status['latency'] = (
            current_metrics['latency'] <= self.baseline['latency'] * 1.5
        )

        # Check error rate
        health_status['error_rate'] = (
            current_metrics['error_rate'] <= self.baseline['error_rate'] * 2
        )

        # Check quality
        health_status['quality'] = (
            current_metrics['quality'] >= self.baseline['quality'] * 0.9
        )

        return health_status

    def should_rollback(self, health_status: Dict[str, bool]) -> bool:
        """Determine if rollback is needed"""
        critical_failures = [
            not health_status.get('error_rate', True),
            not health_status.get('quality', True)
        ]

        return any(critical_failures)
```

## Best Practices

### Monitoring Setup

- **Use a comprehensive monitoring stack**
  - Prometheus for metrics
  - Grafana for visualization
  - Loki for logs
  - Jaeger for tracing
  - Phoenix for AI-specific observability

- **Track all key metrics**
  - Latency (P50, P95, P99)
  - Throughput (requests per second)
  - Token usage and cost
  - Error rates by type

### Alerting

- **Set appropriate thresholds**
  - Latency: Alert on P95 > 30s
  - Error rate: Alert on > 5%
  - Cost: Alert on daily budget exceeded

- **Use multiple alert channels**
  - Email for critical alerts
  - Slack for warnings
  - PagerDuty for emergencies

### Logging

- **Log all LLM interactions**
  - Include model, prompt, response, tokens, latency
  - Use structured logging (JSON)
  - Mask sensitive data

- **Implement middleware for automatic logging**
  - Use FastAPI middleware
  - Track request/response cycles
  - Add correlation IDs

### Drift Detection

- **Monitor for data drift**
  - Use statistical tests (KS test)
  - Track embedding drift
  - Set appropriate thresholds

- **Detect concept drift**
  - Monitor model performance over time
  - Track quality metrics
  - Compare to baseline

### Cost Management

- **Track costs per model**
  - Monitor token usage
  - Calculate cost per request
  - Set daily budgets

- **Optimize for cost**
  - Use appropriate models for tasks
  - Cache responses
  - Batch requests

### Production Deployment

- **Follow the checklist**
  - Complete all pre-deployment items
  - Test monitoring and alerting
  - Document runbooks

- **Monitor post-deployment**
  - Compare to baseline metrics
  - Watch for anomalies
  - Be ready to rollback

## Related Skills

- [`06-ai-ml-production/llm-integration`](06-ai-ml-production/llm-integration/SKILL.md)
- [`06-ai-ml-production/agent-patterns`](06-ai-ml-production/agent-patterns/SKILL.md)
- [`14-monitoring-observability`](14-monitoring-observability/SKILL.md)
- [`42-cost-engineering`](42-cost-engineering/SKILL.md)
