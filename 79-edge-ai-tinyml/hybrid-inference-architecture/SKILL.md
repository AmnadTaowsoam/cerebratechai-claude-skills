---
name: Hybrid Inference Architecture
description: Coordinating cloud and edge inference for optimal performance, cost, and accuracy across distributed AI systems
---

# Hybrid Inference Architecture

## Current Level: Expert (Enterprise Scale)

## Domain: Edge AI & TinyML
## Skill ID: 112

---

## Executive Summary

Hybrid Inference Architecture enables intelligent coordination between cloud and edge inference systems, dynamically routing inference requests based on latency requirements, model complexity, resource availability, and cost considerations. This architecture is essential for enterprises deploying AI at scale across heterogeneous environments while optimizing for performance, cost, and accuracy.

### Strategic Necessity

- **Optimal Performance**: Route requests to best-suited compute resources
- **Cost Efficiency**: Minimize cloud infrastructure costs through edge offloading
- **Latency Reduction**: Sub-millisecond response for time-critical applications
- **Scalability**: Handle variable workloads across distributed infrastructure
- **Resilience**: Graceful degradation when components fail

---

## Technical Deep Dive

### Architecture Components

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Application Layer                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   Mobile    │  │   IoT Edge   │  │   Gateway    │  │   Web App    │    │
│  │   Client    │  │   Device     │  │   Service    │  │   Client     │    │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘    │
└─────────┼─────────────────┼─────────────────┼─────────────────┼─────────────┘
          │                 │                 │                 │
┌─────────┼─────────────────┼─────────────────┼─────────────────┼─────────────┐
│         │      Inference Router / Orchestrator                  │             │
│  ┌──────▼──────────────────────────────────────────────────────▼───────┐    │
│  │               Request Classification & Routing Engine              │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │    │
│  │  │   Latency    │  │   Model      │  │   Resource   │               │    │
│  │  │   Analyzer   │  │   Selector   │  │   Monitor    │               │    │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘               │    │
│  └─────────┼─────────────────┼─────────────────┼─────────────────────────┘    │
└────────────┼─────────────────┼─────────────────┼────────────────────────────┘
             │                 │                 │
┌────────────┼─────────────────┼─────────────────┼────────────────────────────┐
│             │                 │                 │                            │
│  ┌──────────▼───────┐  ┌──────▼───────┐  ┌──────▼───────┐                 │
│  │   Edge Layer    │  │  Cloud Layer  │  │  Fallback     │                 │
│  │                 │  │               │  │  Layer        │                 │
│  │  ┌──────────┐   │  │  ┌──────────┐  │  │  ┌──────────┐  │                 │
│  │  │   MCU    │   │  │  │  GPU     │  │  │  │  Backup  │  │                 │
│  │  │   AI     │   │  │  │  Cluster │  │  │  │  Cloud   │  │                 │
│  │  └──────────┘   │  │  └──────────┘  │  │  └──────────┘  │                 │
│  │  ┌──────────┐   │  │  ┌──────────┐  │  │  ┌──────────┐  │                 │
│  │  │   Edge   │   │  │  │  Server  │  │  │  │  Cache   │  │                 │
│  │  │   GPU    │   │  │  │  Less    │  │  │  │  Layer   │  │                 │
│  │  └──────────┘   │  │  └──────────┘  │  │  └──────────┘  │                 │
│  └─────────────────┘  └───────────────┘  └─────────────────┘                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Routing Decision Framework

**Decision Factors:**

1. **Latency Requirements**
   - Real-time (<10ms): Edge MCU
   - Near-real-time (<100ms): Edge GPU
   - Batch (>1s): Cloud

2. **Model Complexity**
   - Simple (<1MB, <10K params): Edge MCU
   - Medium (<10MB, <1M params): Edge GPU
   - Complex (>10MB, >1M params): Cloud

3. **Resource Availability**
   - Edge resources free: Use edge
   - Edge resources busy: Route to cloud
   - Edge offline: Use cached fallback

4. **Cost Considerations**
   - High volume: Prefer edge
   - Low volume: Cloud acceptable
   - Peak load: Cloud burst

5. **Accuracy Requirements**
   - High accuracy: Cloud model
   - Acceptable accuracy: Edge model
   - Adaptive: Hybrid approach

### Request Classification

```python
from enum import Enum
from dataclasses import dataclass
from typing import Optional, Dict, Any

class LatencyRequirement(Enum):
    REALTIME = "realtime"      # < 10ms
    NEAR_REALTIME = "near"      # < 100ms
    INTERACTIVE = "interactive"  # < 500ms
    BATCH = "batch"             # > 1s

class ModelComplexity(Enum):
    SIMPLE = "simple"           # < 1MB, < 10K params
    MEDIUM = "medium"           # < 10MB, < 1M params
    COMPLEX = "complex"         # > 10MB, > 1M params

class InferenceTarget(Enum):
    EDGE_MCU = "edge_mcu"
    EDGE_GPU = "edge_gpu"
    CLOUD_GPU = "cloud_gpu"
    CLOUD_SERVERLESS = "cloud_serverless"
    FALLBACK = "fallback"

@dataclass
class InferenceRequest:
    """Inference request metadata"""
    request_id: str
    model_name: str
    input_data: Any
    latency_requirement: LatencyRequirement
    model_complexity: ModelComplexity
    priority: int = 5  # 1-10, 10 highest
    max_retries: int = 3
    timeout_ms: int = 1000
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class ResourceStatus:
    """Resource availability status"""
    edge_mcu_available: bool
    edge_mcu_load: float  # 0.0-1.0
    edge_gpu_available: bool
    edge_gpu_load: float
    cloud_available: bool
    cloud_cost_per_request: float
    edge_cost_per_request: float = 0.0
```

### Routing Engine Implementation

```python
import time
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)

class InferenceRouter:
    """Hybrid inference routing engine"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.edge_mcu_client = EdgeMCUClient(config['edge_mcu'])
        self.edge_gpu_client = EdgeGPUClient(config['edge_gpu'])
        self.cloud_client = CloudInferenceClient(config['cloud'])
        self.fallback_cache = FallbackCache(config['fallback'])
        
        # Cost thresholds
        self.max_cloud_cost = config.get('max_cloud_cost', 0.01)
        self.edge_preference_threshold = config.get('edge_preference', 0.7)
        
    def route_request(self, request: InferenceRequest) -> InferenceTarget:
        """Determine optimal inference target"""
        resource_status = self._get_resource_status()
        
        # Check for offline/edge unavailable
        if not resource_status.edge_mcu_available and not resource_status.edge_gpu_available:
            logger.info(f"Edge unavailable, routing to cloud: {request.request_id}")
            return InferenceTarget.CLOUD_GPU
        
        # Analyze routing decision
        targets = self._evaluate_targets(request, resource_status)
        
        # Select best target
        best_target = self._select_best_target(targets, request)
        
        logger.info(f"Routing request {request.request_id} to {best_target.value}")
        return best_target
    
    def _evaluate_targets(
        self, 
        request: InferenceRequest, 
        status: ResourceStatus
    ) -> List[Tuple[InferenceTarget, float]]:
        """Evaluate all possible targets with scores"""
        targets = []
        
        # Evaluate Edge MCU
        if status.edge_mcu_available:
            score = self._score_edge_mcu(request, status)
            targets.append((InferenceTarget.EDGE_MCU, score))
        
        # Evaluate Edge GPU
        if status.edge_gpu_available:
            score = self._score_edge_gpu(request, status)
            targets.append((InferenceTarget.EDGE_GPU, score))
        
        # Evaluate Cloud
        if status.cloud_available:
            score = self._score_cloud(request, status)
            targets.append((InferenceTarget.CLOUD_GPU, score))
        
        return targets
    
    def _score_edge_mcu(
        self, 
        request: InferenceRequest, 
        status: ResourceStatus
    ) -> float:
        """Score Edge MCU as inference target"""
        score = 0.0
        
        # Latency match
        if request.latency_requirement == LatencyRequirement.REALTIME:
            score += 0.4
        elif request.latency_requirement == LatencyRequirement.NEAR_REALTIME:
            score += 0.3
        
        # Model complexity match
        if request.model_complexity == ModelComplexity.SIMPLE:
            score += 0.3
        elif request.model_complexity == ModelComplexity.MEDIUM:
            score += 0.1
        
        # Resource availability
        score += 0.2 * (1.0 - status.edge_mcu_load)
        
        # Cost preference
        score += 0.1  # Edge is always cheaper
        
        return min(score, 1.0)
    
    def _score_edge_gpu(
        self, 
        request: InferenceRequest, 
        status: ResourceStatus
    ) -> float:
        """Score Edge GPU as inference target"""
        score = 0.0
        
        # Latency match
        if request.latency_requirement in [LatencyRequirement.REALTIME, 
                                           LatencyRequirement.NEAR_REALTIME]:
            score += 0.35
        elif request.latency_requirement == LatencyRequirement.INTERACTIVE:
            score += 0.3
        
        # Model complexity match
        if request.model_complexity == ModelComplexity.MEDIUM:
            score += 0.35
        elif request.model_complexity == ModelComplexity.COMPLEX:
            score += 0.2
        
        # Resource availability
        score += 0.2 * (1.0 - status.edge_gpu_load)
        
        # Cost preference
        score += 0.1
        
        return min(score, 1.0)
    
    def _score_cloud(
        self, 
        request: InferenceRequest, 
        status: ResourceStatus
    ) -> float:
        """Score Cloud as inference target"""
        score = 0.0
        
        # Latency match
        if request.latency_requirement in [LatencyRequirement.INTERACTIVE,
                                           LatencyRequirement.BATCH]:
            score += 0.4
        
        # Model complexity match
        if request.model_complexity == ModelComplexity.COMPLEX:
            score += 0.4
        elif request.model_complexity == ModelComplexity.MEDIUM:
            score += 0.2
        
        # Cost penalty
        if status.cloud_cost_per_request > self.max_cloud_cost:
            score -= 0.2
        
        # Always available
        score += 0.2
        
        return min(max(score, 0.0), 1.0)
    
    def _select_best_target(
        self, 
        targets: List[Tuple[InferenceTarget, float]],
        request: InferenceRequest
    ) -> InferenceTarget:
        """Select best target based on scores and priority"""
        if not targets:
            return InferenceTarget.FALLBACK
        
        # Sort by score
        targets.sort(key=lambda x: x[1], reverse=True)
        
        # For high priority requests, prefer highest score
        if request.priority >= 8:
            return targets[0][0]
        
        # For normal priority, consider cost
        best_target, best_score = targets[0]
        second_best, second_score = targets[1] if len(targets) > 1 else (None, 0)
        
        # If edge is close to cloud in score, prefer edge for cost
        if (best_target in [InferenceTarget.CLOUD_GPU, InferenceTarget.CLOUD_SERVERLESS] and
            second_best and second_score >= best_score * self.edge_preference_threshold):
            return second_best
        
        return best_target
    
    def _get_resource_status(self) -> ResourceStatus:
        """Get current resource availability status"""
        return ResourceStatus(
            edge_mcu_available=self.edge_mcu_client.is_available(),
            edge_mcu_load=self.edge_mcu_client.get_load(),
            edge_gpu_available=self.edge_gpu_client.is_available(),
            edge_gpu_load=self.edge_gpu_client.get_load(),
            cloud_available=self.cloud_client.is_available(),
            cloud_cost_per_request=self.cloud_client.get_cost_per_request()
        )
```

### Inference Execution with Fallback

```python
from typing import Optional
import asyncio

class HybridInferenceEngine:
    """Execute inference with automatic fallback"""
    
    def __init__(self, router: InferenceRouter):
        self.router = router
        self.edge_mcu = EdgeMCUClient()
        self.edge_gpu = EdgeGPUClient()
        self.cloud = CloudInferenceClient()
        self.cache = FallbackCache()
        self.metrics = InferenceMetrics()
    
    async def execute(self, request: InferenceRequest) -> Optional[Dict[str, Any]]:
        """Execute inference with fallback chain"""
        start_time = time.time()
        target = self.router.route_request(request)
        
        for attempt in range(request.max_retries):
            try:
                result = await self._execute_on_target(request, target)
                
                # Cache successful results
                if target != InferenceTarget.FALLBACK:
                    self.cache.store(request.request_id, result)
                
                # Record metrics
                self.metrics.record_success(
                    request.request_id,
                    target,
                    time.time() - start_time
                )
                
                return result
                
            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed for {target.value}: {e}")
                
                # Fallback to next target
                target = self._get_fallback_target(target)
                
                if target == InferenceTarget.FALLBACK:
                    # Try cache
                    cached = self.cache.retrieve(request.request_id)
                    if cached:
                        logger.info(f"Using cached result for {request.request_id}")
                        return cached
        
        # All attempts failed
        self.metrics.record_failure(request.request_id)
        return None
    
    async def _execute_on_target(
        self, 
        request: InferenceRequest, 
        target: InferenceTarget
    ) -> Dict[str, Any]:
        """Execute inference on specific target"""
        if target == InferenceTarget.EDGE_MCU:
            return await self.edge_mcu.infer(
                request.model_name,
                request.input_data,
                timeout=request.timeout_ms
            )
        elif target == InferenceTarget.EDGE_GPU:
            return await self.edge_gpu.infer(
                request.model_name,
                request.input_data,
                timeout=request.timeout_ms
            )
        elif target == InferenceTarget.CLOUD_GPU:
            return await self.cloud.infer(
                request.model_name,
                request.input_data,
                timeout=request.timeout_ms
            )
        else:
            raise ValueError(f"Unknown target: {target}")
    
    def _get_fallback_target(self, current: InferenceTarget) -> InferenceTarget:
        """Get fallback target in order of preference"""
        fallback_chain = {
            InferenceTarget.EDGE_MCU: InferenceTarget.EDGE_GPU,
            InferenceTarget.EDGE_GPU: InferenceTarget.CLOUD_GPU,
            InferenceTarget.CLOUD_GPU: InferenceTarget.FALLBACK,
            InferenceTarget.FALLBACK: InferenceTarget.FALLBACK
        }
        return fallback_chain.get(current, InferenceTarget.FALLBACK)
```

### Adaptive Model Selection

```python
class AdaptiveModelSelector:
    """Select optimal model variant based on context"""
    
    def __init__(self, model_registry: Dict[str, List[ModelVariant]]):
        self.model_registry = model_registry
        self.accuracy_tracker = ModelAccuracyTracker()
    
    def select_model(
        self, 
        base_model: str, 
        request: InferenceRequest
    ) -> ModelVariant:
        """Select best model variant for request"""
        variants = self.model_registry.get(base_model, [])
        
        if not variants:
            raise ValueError(f"No variants found for {base_model}")
        
        # Score each variant
        scored_variants = []
        for variant in variants:
            score = self._score_variant(variant, request)
            scored_variants.append((variant, score))
        
        # Select best
        scored_variants.sort(key=lambda x: x[1], reverse=True)
        return scored_variants[0][0]
    
    def _score_variant(
        self, 
        variant: ModelVariant, 
        request: InferenceRequest
    ) -> float:
        """Score model variant for request"""
        score = 0.0
        
        # Accuracy score
        accuracy = self.accuracy_tracker.get_accuracy(variant.name)
        score += 0.4 * accuracy
        
        # Size score (smaller is better for edge)
        if variant.target in ['edge_mcu', 'edge_gpu']:
            size_score = 1.0 - (variant.size_mb / 10.0)  # Normalize
            score += 0.3 * size_score
        
        # Latency score
        latency_score = 1.0 - (variant.avg_latency_ms / 100.0)
        score += 0.3 * latency_score
        
        return min(score, 1.0)

@dataclass
class ModelVariant:
    name: str
    base_model: str
    target: str  # edge_mcu, edge_gpu, cloud
    size_mb: float
    avg_latency_ms: float
    accuracy: float
    quantization: str  # int8, fp16, fp32
```

---

## Tooling & Tech Stack

### Core Frameworks
- **TensorFlow Serving**: Cloud inference serving
- **TensorFlow Lite Micro**: Edge MCU inference
- **TensorRT**: GPU optimization
- **ONNX Runtime**: Cross-platform inference

### Infrastructure
- **Kubernetes**: Cloud orchestration
- **K3s/KubeEdge**: Edge orchestration
- **Istio**: Service mesh for routing
- **Redis**: Caching layer

### Monitoring
- **Prometheus**: Metrics collection
- **Grafana**: Visualization
- **Jaeger**: Distributed tracing
- **ELK Stack**: Logging

### Development Tools
- **Python 3.9+**: Primary language
- **TypeScript**: Frontend routing logic
- **Docker**: Containerization
- **Terraform**: Infrastructure as Code

---

## Configuration Essentials

### Router Configuration

```yaml
# config/router_config.yaml
routing:
  max_cloud_cost: 0.01  # $0.01 per request
  edge_preference: 0.7  # Prefer edge if within 70% of cloud score
  
  latency_thresholds:
    realtime: 10       # ms
    near_realtime: 100  # ms
    interactive: 500    # ms
    batch: 1000         # ms
  
  model_size_thresholds:
    edge_mcu: 1.0       # MB
    edge_gpu: 10.0      # MB
    cloud: 1000.0       # MB

edge_mcu:
  endpoint: "http://edge-mcu:8080"
  timeout_ms: 50
  max_concurrent: 10
  health_check_interval: 5  # seconds

edge_gpu:
  endpoint: "http://edge-gpu:8081"
  timeout_ms: 200
  max_concurrent: 5
  health_check_interval: 5

cloud:
  endpoint: "https://api.cloud-inference.com"
  timeout_ms: 5000
  max_concurrent: 100
  api_key: "${CLOUD_API_KEY}"
  region: "us-west-2"

fallback:
  cache_ttl: 3600  # seconds
  max_cache_size: 10000
  enable_stale_results: true
  stale_ttl: 86400  # 24 hours

monitoring:
  enable_metrics: true
  enable_tracing: true
  metrics_port: 9090
  tracing_endpoint: "http://jaeger:14268/api/traces"
```

### Model Registry Configuration

```yaml
# config/model_registry.yaml
models:
  image_classification:
    base_model: "resnet50"
    variants:
      - name: "resnet50-int8"
        target: "edge_mcu"
        size_mb: 0.5
        avg_latency_ms: 15
        accuracy: 0.92
        quantization: "int8"
        path: "/models/resnet50-int8.tflite"
      
      - name: "resnet50-fp16"
        target: "edge_gpu"
        size_mb: 5.0
        avg_latency_ms: 5
        accuracy: 0.95
        quantization: "fp16"
        path: "/models/resnet50-fp16.trt"
      
      - name: "resnet50-fp32"
        target: "cloud"
        size_mb: 100.0
        avg_latency_ms: 50
        accuracy: 0.97
        quantization: "fp32"
        path: "/models/resnet50-fp32.h5"
  
  object_detection:
    base_model: "yolov5"
    variants:
      - name: "yolov5n-int8"
        target: "edge_mcu"
        size_mb: 0.8
        avg_latency_ms: 25
        accuracy: 0.78
        quantization: "int8"
        path: "/models/yolov5n-int8.tflite"
      
      - name: "yolov5s-fp16"
        target: "edge_gpu"
        size_mb: 8.0
        avg_latency_ms: 10
        accuracy: 0.85
        quantization: "fp16"
        path: "/models/yolov5s-fp16.trt"
      
      - name: "yolov5m-fp32"
        target: "cloud"
        size_mb: 150.0
        avg_latency_ms: 80
        accuracy: 0.91
        quantization: "fp32"
        path: "/models/yolov5m-fp32.pt"
```

### Kubernetes Deployment

```yaml
# k8s/hybrid-router-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hybrid-inference-router
  namespace: ai-inference
spec:
  replicas: 3
  selector:
    matchLabels:
      app: hybrid-router
  template:
    metadata:
      labels:
        app: hybrid-router
    spec:
      containers:
      - name: router
        image: registry.example.com/hybrid-router:1.0.0
        ports:
        - containerPort: 8080
        - containerPort: 9090  # metrics
        env:
        - name: CLOUD_API_KEY
          valueFrom:
            secretKeyRef:
              name: cloud-secrets
              key: api-key
        - name: LOG_LEVEL
          value: "INFO"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
        volumeMounts:
        - name: config
          mountPath: /app/config
      volumes:
      - name: config
        configMap:
          name: router-config
---
apiVersion: v1
kind: Service
metadata:
  name: hybrid-router-service
  namespace: ai-inference
spec:
  selector:
    app: hybrid-router
  ports:
  - port: 80
    targetPort: 8080
    name: http
  - port: 9090
    targetPort: 9090
    name: metrics
  type: LoadBalancer
```

---

## Code Examples

### Good: Complete Hybrid Router Implementation

```python
# router/main.py
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import asyncio
import logging
from contextlib import asynccontextmanager

from inference.router import InferenceRouter, InferenceRequest, LatencyRequirement, ModelComplexity
from inference.engine import HybridInferenceEngine
from inference.monitoring import MetricsCollector
from config.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global instances
router: Optional[InferenceRouter] = None
engine: Optional[HybridInferenceEngine] = None
metrics: Optional[MetricsCollector] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global router, engine, metrics
    
    # Initialize components
    logger.info("Initializing hybrid inference router...")
    router = InferenceRouter(settings.router_config)
    engine = HybridInferenceEngine(router)
    metrics = MetricsCollector(settings.monitoring_config)
    
    # Start metrics collection
    await metrics.start()
    
    yield
    
    # Cleanup
    logger.info("Shutting down hybrid inference router...")
    await metrics.stop()

app = FastAPI(
    title="Hybrid Inference Router",
    description="Intelligent routing for cloud and edge inference",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InferenceRequestModel(BaseModel):
    """API request model"""
    model_name: str
    input_data: Dict[str, Any]
    latency_requirement: str = "interactive"
    priority: int = 5
    timeout_ms: int = 1000
    metadata: Optional[Dict[str, Any]] = None

class InferenceResponse(BaseModel):
    """API response model"""
    request_id: str
    target: str
    result: Dict[str, Any]
    latency_ms: float
    cached: bool = False

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "router_status": router is not None,
        "engine_status": engine is not None
    }

@app.get("/ready")
async def readiness_check():
    """Readiness check endpoint"""
    if not router or not engine:
        raise HTTPException(status_code=503, detail="Not ready")
    
    # Check resource availability
    status = router._get_resource_status()
    
    if not (status.edge_mcu_available or status.edge_gpu_available or status.cloud_available):
        raise HTTPException(status_code=503, detail="No inference targets available")
    
    return {
        "status": "ready",
        "edge_mcu_available": status.edge_mcu_available,
        "edge_gpu_available": status.edge_gpu_available,
        "cloud_available": status.cloud_available
    }

@app.get("/metrics")
async def get_metrics():
    """Get inference metrics"""
    if not metrics:
        raise HTTPException(status_code=503, detail="Metrics not available")
    
    return await metrics.get_summary()

@app.post("/infer", response_model=InferenceResponse)
async def infer(
    request: InferenceRequestModel,
    background_tasks: BackgroundTasks
):
    """Execute inference with automatic routing"""
    if not router or not engine:
        raise HTTPException(status_code=503, detail="Service not ready")
    
    # Create request object
    inference_req = InferenceRequest(
        request_id=f"req_{asyncio.get_event_loop().time()}",
        model_name=request.model_name,
        input_data=request.input_data,
        latency_requirement=LatencyRequirement(request.latency_requirement),
        model_complexity=ModelComplexity.MEDIUM,  # Could be derived from model registry
        priority=request.priority,
        timeout_ms=request.timeout_ms,
        metadata=request.metadata
    )
    
    # Execute inference
    result = await engine.execute(inference_req)
    
    if result is None:
        raise HTTPException(status_code=500, detail="Inference failed")
    
    # Record metrics in background
    background_tasks.add_task(
        metrics.record_inference,
        inference_req.request_id,
        result['target'],
        result['latency_ms']
    )
    
    return InferenceResponse(
        request_id=inference_req.request_id,
        target=result['target'],
        result=result['output'],
        latency_ms=result['latency_ms'],
        cached=result.get('cached', False)
    )

@app.get("/status")
async def get_status():
    """Get current system status"""
    if not router:
        raise HTTPException(status_code=503, detail="Router not available")
    
    status = router._get_resource_status()
    
    return {
        "resources": {
            "edge_mcu": {
                "available": status.edge_mcu_available,
                "load": status.edge_mcu_load
            },
            "edge_gpu": {
                "available": status.edge_gpu_available,
                "load": status.edge_gpu_load
            },
            "cloud": {
                "available": status.cloud_available,
                "cost_per_request": status.cloud_cost_per_request
            }
        },
        "routing_config": {
            "max_cloud_cost": router.max_cloud_cost,
            "edge_preference_threshold": router.edge_preference_threshold
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
```

```python
# monitoring/metrics.py
from prometheus_client import Counter, Histogram, Gauge, start_http_server
from typing import Dict, Any
import asyncio
from datetime import datetime

class MetricsCollector:
    """Collect and expose inference metrics"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # Prometheus metrics
        self.inference_requests = Counter(
            'inference_requests_total',
            'Total inference requests',
            ['target', 'status']
        )
        
        self.inference_latency = Histogram(
            'inference_latency_ms',
            'Inference latency in milliseconds',
            ['target']
        )
        
        self.active_requests = Gauge(
            'active_inference_requests',
            'Number of active inference requests'
        )
        
        self.resource_availability = Gauge(
            'resource_availability',
            'Resource availability status',
            ['resource']
        )
        
        self.cost_tracker = Counter(
            'inference_cost_total',
            'Total inference cost',
            ['target']
        )
        
        self._collection_task = None
    
    async def start(self):
        """Start metrics collection"""
        if self.config.get('enable_metrics'):
            start_http_server(self.config.get('metrics_port', 9090))
            
            # Start periodic collection
            self._collection_task = asyncio.create_task(
                self._collect_periodically()
            )
    
    async def stop(self):
        """Stop metrics collection"""
        if self._collection_task:
            self._collection_task.cancel()
            try:
                await self._collection_task
            except asyncio.CancelledError:
                pass
    
    async def _collect_periodically(self):
        """Periodically collect resource metrics"""
        while True:
            # Collect resource availability
            # This would query actual resource status
            await asyncio.sleep(5)
    
    def record_inference(
        self, 
        request_id: str, 
        target: str, 
        latency_ms: float
    ):
        """Record inference metrics"""
        self.inference_requests.labels(target=target, status='success').inc()
        self.inference_latency.labels(target=target).observe(latency_ms)
        
        # Track cost
        cost = self._calculate_cost(target)
        self.cost_tracker.labels(target=target).inc(cost)
    
    def record_failure(self, request_id: str, target: str = 'unknown'):
        """Record inference failure"""
        self.inference_requests.labels(target=target, status='failure').inc()
    
    def _calculate_cost(self, target: str) -> float:
        """Calculate cost for inference"""
        costs = {
            'edge_mcu': 0.0,
            'edge_gpu': 0.001,
            'cloud_gpu': 0.01,
            'cloud_serverless': 0.005
        }
        return costs.get(target, 0.0)
    
    async def get_summary(self) -> Dict[str, Any]:
        """Get metrics summary"""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "metrics": {
                "total_requests": self._get_metric_value(self.inference_requests),
                "avg_latency": self._get_avg_latency(),
                "total_cost": self._get_metric_value(self.cost_tracker)
            }
        }
    
    def _get_metric_value(self, metric) -> float:
        """Get current metric value"""
        # Simplified - would use proper metric collection
        return 0.0
    
    def _get_avg_latency(self) -> float:
        """Get average latency across all targets"""
        # Simplified - would use proper histogram collection
        return 0.0
```

### Bad: Anti-pattern Example

```python
# BAD: No fallback mechanism
async def bad_inference(request):
    # No fallback if edge fails
    result = await edge_mcu.infer(request)
    return result

# BAD: Hard-coded routing
async def bad_routing(request):
    # Always routes to cloud regardless of cost/latency
    if request.priority > 5:
        return await cloud.infer(request)
    else:
        return await edge.infer(request)

# BAD: No resource awareness
async def bad_resource_aware(request):
    # Doesn't check if edge is available
    return await edge.infer(request)

# BAD: No cost tracking
async def bad_cost_tracking(request):
    # Doesn't track inference costs
    result = await cloud.infer(request)
    return result

# BAD: No metrics
async def bad_metrics(request):
    # No metrics collection
    result = await router.route(request)
    return result
```

---

## Standards, Compliance & Security

### Industry Standards
- **ISO/IEC 27001**: Information security management
- **SOC 2 Type II**: Security and availability
- **GDPR**: Data protection and privacy
- **HIPAA**: Healthcare data protection

### Security Best Practices
- **API Authentication**: JWT tokens for all requests
- **Encryption**: TLS 1.3 for all communications
- **Data Masking**: Sanitize sensitive data in logs
- **Rate Limiting**: Prevent abuse and DoS attacks

### Compliance Requirements
- **Data Residency**: Store data in specified regions
- **Audit Logging**: Record all inference requests
- **Model Versioning**: Track model provenance
- **Explainability**: Provide inference explanations when required

---

## Quick Start

### 1. Clone and Install

```bash
git clone https://github.com/example/hybrid-inference-router.git
cd hybrid-inference-router

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure

```bash
# Copy example config
cp config/router_config.yaml.example config/router_config.yaml

# Edit configuration
vim config/router_config.yaml
```

### 3. Run Locally

```bash
# Start router
python -m router.main

# Or using uvicorn
uvicorn router.main:app --host 0.0.0.0 --port 8080 --reload
```

### 4. Deploy to Kubernetes

```bash
# Apply configuration
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/deployment.yaml

# Check status
kubectl get pods -n ai-inference
kubectl logs -f deployment/hybrid-inference-router -n ai-inference
```

### 5. Test

```bash
# Health check
curl http://localhost:8080/health

# Inference request
curl -X POST http://localhost:8080/infer \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "resnet50",
    "input_data": {"image": "base64_encoded_image"},
    "latency_requirement": "interactive",
    "priority": 5
  }'
```

---

## Production Checklist

### Deployment
- [ ] Kubernetes deployment configured
- [ ] Secrets management configured
- [ ] Health checks enabled
- [ ] Readiness probes configured
- [ ] Resource limits set

### Monitoring
- [ ] Prometheus metrics enabled
- [ ] Grafana dashboards configured
- [ ] Distributed tracing enabled
- [ ] Alert rules configured
- [ ] Log aggregation set up

### Security
- [ ] TLS encryption enabled
- [ ] API authentication configured
- [ ] Rate limiting enabled
- [ ] Network policies configured
- [ ] Security audit completed

### Performance
- [ ] Load testing completed
- [ ] Latency targets met
- [ ] Cost optimization verified
- [ ] Auto-scaling configured
- [ ] CDN configured for static assets

### Reliability
- [ ] Fallback mechanisms tested
- [ ] Circuit breakers configured
- [ ] Retry policies set
- [ ] Cache layer configured
- [ ] Disaster recovery plan in place

---

## Anti-patterns

### ❌ Avoid These Practices

1. **No Fallback Mechanism**
   ```python
   # BAD: Single point of failure
   result = await edge.infer(request)
   ```

2. **Hard-coded Routing**
   ```python
   # BAD: No dynamic routing
   if request.priority > 5:
       return await cloud.infer(request)
   ```

3. **Ignoring Resource Status**
   ```python
   # BAD: No resource awareness
   return await edge.infer(request)
   ```

4. **No Cost Tracking**
   ```python
   # BAD: Uncontrolled cloud costs
   result = await cloud.infer(request)
   ```

5. **No Metrics**
   ```python
   # BAD: No observability
   result = await router.route(request)
   ```

### ✅ Follow These Practices

1. **Fallback Chain**
   ```python
   # GOOD: Graceful degradation
   for target in fallback_chain:
       try:
           return await target.infer(request)
       except:
           continue
   ```

2. **Dynamic Routing**
   ```python
   # GOOD: Context-aware routing
   target = router.evaluate(request, resources)
   return await target.infer(request)
   ```

3. **Resource Awareness**
   ```python
   # GOOD: Resource-based routing
   if edge.available() and edge.load() < threshold:
       return await edge.infer(request)
   ```

4. **Cost Tracking**
   ```python
   # GOOD: Cost-aware routing
   if cloud_cost > threshold:
       return await edge.infer(request)
   ```

5. **Comprehensive Metrics**
   ```python
   # GOOD: Full observability
   metrics.record_inference(target, latency, cost)
   ```

---

## Unit Economics & KPIs

### Development Costs
- **Initial Development**: 160-240 hours
- **Testing & Validation**: 80-120 hours
- **Documentation**: 40-60 hours
- **Total**: 280-420 hours

### Operational Costs
- **Cloud Infrastructure**: $500-2000/month
- **Edge Infrastructure**: $100-500/month per location
- **Monitoring**: $100-300/month
- **Support**: 20-40 hours/month

### ROI Metrics
- **Cloud Cost Reduction**: 70-90% through edge offloading
- **Latency Improvement**: 80-95% reduction vs cloud-only
- **Reliability**: 99.9%+ uptime with fallback
- **Scalability**: Handle 10K+ concurrent requests

### KPI Targets
- **P95 Latency**: < 100ms
- **Routing Accuracy**: > 95%
- **Cost per Inference**: < $0.01
- **Fallback Rate**: < 5%
- **Edge Utilization**: > 70%

---

## Integration Points / Related Skills

### Upstream Skills
- **91. Feature Store Implementation**: Feature extraction for routing
- **92. Drift Detection and Retraining**: Model drift monitoring
- **93. Model Registry and Versioning**: Model variant management

### Parallel Skills
- **111. TinyML Microcontroller AI**: Edge MCU inference
- **113. On-Device Model Training**: Federated learning
- **114. Edge Model Compression**: Model optimization
- **115. Edge AI Development Workflow**: End-to-end pipeline

### Downstream Skills
- **101. High Performance Inference**: Inference optimization
- **102. Model Optimization and Quantization**: Model compression
- **103. Serverless Inference**: Cloud fallback
- **116. Agentic AI Frameworks**: Agent-based inference

### Cross-Domain Skills
- **14. Monitoring and Observability**: Metrics and tracing
- **15. DevOps Infrastructure**: Kubernetes deployment
- **81. SaaS FinOps Pricing**: Cost optimization
- **84. Compliance AI Governance**: Regulatory compliance

---

## References & Resources

### Documentation
- [TensorFlow Serving](https://www.tensorflow.org/tfx/guide/serving)
- [TensorFlow Lite Micro](https://www.tensorflow.org/lite/microcontrollers)
- [TensorRT](https://developer.nvidia.com/tensorrt)
- [Kubernetes Documentation](https://kubernetes.io/docs/)

### Architecture Patterns
- [Edge Computing Patterns](https://aws.amazon.com/blogs/architecture/edge-computing-patterns/)
- [Hybrid Cloud Architecture](https://azure.microsoft.com/en-us/solutions/hybrid-cloud-app/)
- [Multi-Cloud Strategies](https://www.gartner.com/en/information-technology/insights/multicloud-strategies)

### Papers & Research
- [Hybrid Cloud-Edge Computing](https://arxiv.org/abs/2002.04203)
- [Adaptive Inference Offloading](https://arxiv.org/abs/1908.06304)
- [Cost-Aware Inference Routing](https://arxiv.org/abs/2010.06292)
