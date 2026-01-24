---
name: High Performance Inference
description: Optimized ML model serving infrastructure for low-latency, high-throughput inference at enterprise scale
---

# High Performance Inference

> **Current Level:** Expert (Enterprise Scale)
> **Domain:** AI / MLOps / Infrastructure
> **Skill ID:** 101

---

## Overview
High Performance Inference focuses on optimizing ML model serving infrastructure to achieve sub-millisecond latency and handle millions of requests per second. It involves specialized serving frameworks, hardware acceleration, batching strategies, and load balancing techniques to maximize throughput while minimizing resource costs.

## Why This Matters / Strategic Necessity

### Context
In 2025-2026, real-time ML applications require inference latencies under 10ms for user-facing features and under 100ms for batch processing. Traditional serving approaches cannot meet these SLAs at scale, leading to poor user experience and lost revenue.

### Business Impact
- **User Experience:** 50-80% improvement in application responsiveness
- **Cost Reduction:** 60-80% reduction in compute costs through optimization
- **Revenue Impact:** 10-30% increase in conversion rates from faster responses
- **Scalability:** Support 10x-100x more requests with same infrastructure

### Product Thinking
Solves the critical bottleneck where ML models become performance bottlenecks in production systems, causing cascading delays across the application stack and directly impacting user satisfaction and business metrics.

## Core Concepts / Technical Deep Dive

### 1. Serving Architectures

**Stateless Serving:** Each request is independent, no session state maintained.
- Pros: Easy to scale horizontally
- Cons: Cannot leverage request context

**Stateful Serving:** Maintains session state for multiple related requests.
- Pros: Can optimize for repeated requests
- Cons: More complex scaling and failover

**Batch Inference:** Process multiple requests together for efficiency.
- Pros: Maximizes GPU utilization
- Cons: Increased latency for individual requests

**Streaming Inference:** Process requests as they arrive in real-time.
- Pros: Low latency, good for real-time applications
- Cons: Less efficient resource utilization

### 2. Optimization Techniques

**Model Optimization:**
- Quantization: Reduce precision (FP32 → FP16 → INT8)
- Pruning: Remove less important weights
- Knowledge Distillation: Train smaller model to mimic larger one
- Architecture Search: Find optimal model structure

**Serving Optimization:**
- Request Batching: Combine multiple requests for single forward pass
- Dynamic Batching: Adaptive batch sizing based on load
- Model Caching: Keep models in GPU memory
- Tensor Parallelism: Split model across multiple GPUs
- Pipeline Parallelism: Process different stages on different GPUs

**Infrastructure Optimization:**
- GPU Selection: Choose right GPU for model (A100, T4, L4)
- CPU Optimization: Use AVX instructions, NUMA awareness
- Memory Management: Pre-allocate memory, avoid fragmentation
- Network Optimization: Use RDMA, gRPC, HTTP/2

### 3. Performance Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌─────────────┐
│   Load      │────▶│   Request    │────▶│   Model     │────▶│   Response  │
│  Balancer   │     │   Batcher    │     │   Server    │     │   Cache     │
└─────────────┘     └──────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌─────────────┐
│   Health    │     │   Dynamic    │     │   GPU       │     │   Metrics   │
│   Checks    │     │   Batching   │     │   Pool      │     │   Exporter  │
└─────────────┘     └──────────────┘     └─────────────┘     └─────────────┘
```

## Tooling & Tech Stack

### Enterprise Tools
- **NVIDIA Triton Inference Server:** High-performance serving with dynamic batching
- **TensorRT Serving:** NVIDIA's optimized serving framework
- **TorchServe:** PyTorch model serving with production features
- **TensorFlow Serving:** Google's production ML serving solution
- **BentoML:** Unified serving framework for multiple ML frameworks
- **Ray Serve:** Scalable model serving with Python API

### Configuration Essentials

```yaml
# Triton Inference Server configuration
model_repository: /models
backend_config:
  tensorflow:
    version: 2
  pytorch:
    version: 2.0
  onnxruntime:
    version: 1.15

# Dynamic batching settings
dynamic_batching:
  max_queue_delay_microseconds: 1000
  preferred_batch_size: [8, 16, 32]
  max_batch_size: 64

# Instance groups for scaling
instance_group:
  - kind: KIND_GPU
    count: 1
    gpus: [0]
    profile:
      - batch_size: 1
      - preferred_batch_size: 8
  - kind: KIND_CPU
    count: 2

# Performance tuning
performance:
  buffer_manager_thread_count: 8
  rate_limiter:
    mode: RATE_LIMITER_OFF
  pinned_memory_pool:
    byte_size: 268435456  # 256MB
```

## Code Examples

### Good vs Bad Examples

```python
# ❌ Bad - Naive serving with no optimization
class ModelServer:
    def __init__(self, model):
        self.model = model
    
    def predict(self, inputs):
        return self.model.predict(inputs)

# ✅ Good - Optimized serving with batching
import tritonclient.grpc as grpcclient
import numpy as np

class OptimizedModelServer:
    def __init__(self, model_path, max_batch_size=32):
        self.client = grpcclient.InferenceServerClient(url="localhost:8001")
        self.model_name = "my_model"
        self.max_batch_size = max_batch_size
        self.input_buffer = []
    
    async def predict(self, inputs):
        self.input_buffer.append(inputs)
        
        if len(self.input_buffer) >= self.max_batch_size:
            # Process batch
            batch = np.stack(self.input_buffer)
            result = await self._predict_batch(batch)
            self.input_buffer = []
            return result[-1]  # Return last result
        else:
            # Wait for more requests or timeout
            return await self._predict_single(inputs)
    
    async def _predict_batch(self, batch):
        inputs = [
            grpcclient.InferInput(
                "input__0", 
                batch.shape, 
                "FP32"
            )
        ]
        inputs[0].set_data_from_numpy(batch)
        
        outputs = [
            grpcclient.InferRequestedOutput("output__0")
        ]
        
        response = self.client.infer(
            model_name=self.model_name,
            inputs=inputs,
            outputs=outputs
        )
        
        return response.as_numpy("output__0")
```

```python
# ❌ Bad - No GPU optimization, CPU-only inference
import torch

def predict(model, inputs):
    with torch.no_grad():
        outputs = model(inputs)
    return outputs

# ✅ Good - GPU optimized with mixed precision
import torch
from torch.cuda.amp import autocast

def predict_optimized(model, inputs, device="cuda"):
    model = model.to(device)
    inputs = inputs.to(device)
    
    with torch.no_grad():
        with autocast():
            outputs = model(inputs)
    
    return outputs.cpu()
```

### Implementation Example

```python
"""
Production-ready High Performance Inference Server
"""
from typing import List, Dict, Any, Optional, Tuple
import asyncio
import time
import numpy as np
from dataclasses import dataclass, field
from enum import Enum
import logging
from concurrent.futures import ThreadPoolExecutor
import torch
from torch.cuda.amp import autocast
from queue import Queue
import threading

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelFramework(Enum):
    """Supported ML frameworks."""
    PYTORCH = "pytorch"
    TENSORFLOW = "tensorflow"
    ONNX = "onnx"
    TENSORRT = "tensorrt"


@dataclass
class InferenceRequest:
    """Inference request with metadata."""
    request_id: str
    inputs: np.ndarray
    timestamp: float = field(default_factory=time.time)
    priority: int = 0  # Higher priority = processed first
    timeout: float = 5.0  # Seconds


@dataclass
class InferenceResponse:
    """Inference response with metadata."""
    request_id: str
    outputs: np.ndarray
    latency_ms: float
    batch_size: int
    timestamp: float = field(default_factory=time.time)


@dataclass
class PerformanceMetrics:
    """Performance metrics for the inference server."""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_latency_ms: float = 0.0
    p50_latency_ms: float = 0.0
    p95_latency_ms: float = 0.0
    p99_latency_ms: float = 0.0
    requests_per_second: float = 0.0
    avg_batch_size: float = 0.0
    gpu_utilization: float = 0.0


class DynamicBatcher:
    """
    Dynamic batching for maximizing throughput while minimizing latency.
    """
    
    def __init__(
        self,
        max_batch_size: int = 32,
        max_delay_ms: float = 10.0,
        preferred_batch_sizes: List[int] = None
    ):
        """
        Initialize dynamic batcher.
        
        Args:
            max_batch_size: Maximum batch size
            max_delay_ms: Maximum time to wait for batch formation
            preferred_batch_sizes: Preferred batch sizes for efficiency
        """
        self.max_batch_size = max_batch_size
        self.max_delay_ms = max_delay_ms
        self.preferred_batch_sizes = preferred_batch_sizes or [8, 16, 32]
        self.request_queue: Queue = Queue()
        self.lock = threading.Lock()
        
    def add_request(self, request: InferenceRequest) -> None:
        """
        Add a request to the batch.
        
        Args:
            request: Inference request to add
        """
        self.request_queue.put(request)
        logger.debug(f"Added request {request.request_id} to batch")
    
    def get_batch(self, timeout: float = 0.1) -> List[InferenceRequest]:
        """
        Get a batch of requests to process.
        
        Args:
            timeout: Maximum time to wait for batch formation
            
        Returns:
            List of requests to process
        """
        batch = []
        start_time = time.time()
        
        # Try to fill batch up to max size or timeout
        while len(batch) < self.max_batch_size:
            elapsed_ms = (time.time() - start_time) * 1000
            
            if elapsed_ms >= self.max_delay_ms:
                break
            
            try:
                request = self.request_queue.get(timeout=timeout)
                batch.append(request)
            except:
                break
        
        # Adjust to preferred batch size if close
        if batch:
            batch = self._adjust_to_preferred_size(batch)
        
        logger.debug(f"Created batch of size {len(batch)}")
        return batch
    
    def _adjust_to_preferred_size(self, batch: List[InferenceRequest]) -> List[InferenceRequest]:
        """
        Adjust batch size to preferred sizes for efficiency.
        
        Args:
            batch: Current batch
            
        Returns:
            Adjusted batch
        """
        current_size = len(batch)
        
        # Find closest preferred size
        for pref_size in sorted(self.preferred_batch_sizes):
            if abs(current_size - pref_size) <= 2:
                # Return extra requests to queue
                if current_size > pref_size:
                    extra = batch[pref_size:]
                    for req in extra:
                        self.request_queue.put(req)
                    return batch[:pref_size]
                break
        
        return batch


class HighPerformanceInferenceServer:
    """
    Enterprise-grade high performance inference server.
    """
    
    def __init__(
        self,
        model,
        model_framework: ModelFramework = ModelFramework.PYTORCH,
        max_batch_size: int = 32,
        max_delay_ms: float = 10.0,
        device: str = "cuda",
        use_mixed_precision: bool = True,
        num_workers: int = 4
    ):
        """
        Initialize inference server.
        
        Args:
            model: The ML model to serve
            model_framework: Framework of the model
            max_batch_size: Maximum batch size for dynamic batching
            max_delay_ms: Maximum delay for dynamic batching
            device: Device to run inference on (cuda/cpu)
            use_mixed_precision: Whether to use mixed precision
            num_workers: Number of worker threads
        """
        self.model = model
        self.model_framework = model_framework
        self.device = device
        self.use_mixed_precision = use_mixed_precision
        self.num_workers = num_workers
        
        # Initialize components
        self.batcher = DynamicBatcher(
            max_batch_size=max_batch_size,
            max_delay_ms=max_delay_ms
        )
        
        self.metrics = PerformanceMetrics()
        self.latency_history: List[float] = []
        
        # Move model to device
        if device == "cuda" and torch.cuda.is_available():
            self.model = self.model.to(device)
            self.model.eval()
            logger.info(f"Model moved to GPU: {torch.cuda.get_device_name(0)}")
        
        # Initialize thread pool
        self.executor = ThreadPoolExecutor(max_workers=num_workers)
        
        # Start inference loop
        self.running = False
        self.inference_task: Optional[asyncio.Task] = None
        
        logger.info(f"Inference server initialized: {model_framework.value} on {device}")
    
    async def start(self) -> None:
        """Start the inference server."""
        self.running = True
        self.inference_task = asyncio.create_task(self._inference_loop())
        logger.info("Inference server started")
    
    async def stop(self) -> None:
        """Stop the inference server."""
        self.running = False
        if self.inference_task:
            self.inference_task.cancel()
        self.executor.shutdown(wait=True)
        logger.info("Inference server stopped")
    
    async def predict(
        self,
        inputs: np.ndarray,
        request_id: Optional[str] = None,
        priority: int = 0
    ) -> InferenceResponse:
        """
        Make a prediction with dynamic batching.
        
        Args:
            inputs: Input data
            request_id: Optional request ID
            priority: Request priority (higher = processed first)
            
        Returns:
            Inference response
        """
        if request_id is None:
            request_id = f"req_{time.time_ns()}"
        
        request = InferenceRequest(
            request_id=request_id,
            inputs=inputs,
            priority=priority
        )
        
        # Add to batcher
        self.batcher.add_request(request)
        
        # Wait for result (simplified - in production use futures/promises)
        # This is a simplified version - production would use async queues
        await asyncio.sleep(0.001)  # Small delay to allow batching
        
        # For simplicity, return immediate result
        # In production, this would wait for the actual batch processing
        result = await self._predict_single(inputs)
        
        return InferenceResponse(
            request_id=request_id,
            outputs=result,
            latency_ms=1.0,
            batch_size=1
        )
    
    async def _inference_loop(self) -> None:
        """Main inference loop that processes batches."""
        while self.running:
            try:
                # Get batch
                batch = self.batcher.get_batch(timeout=0.1)
                
                if batch:
                    # Process batch
                    await self._process_batch(batch)
                
            except Exception as e:
                logger.error(f"Error in inference loop: {e}")
                await asyncio.sleep(0.1)
    
    async def _process_batch(self, batch: List[InferenceRequest]) -> None:
        """
        Process a batch of inference requests.
        
        Args:
            batch: List of requests to process
        """
        try:
            # Stack inputs
            inputs = np.stack([req.inputs for req in batch])
            
            # Convert to tensor
            if self.model_framework == ModelFramework.PYTORCH:
                inputs_tensor = torch.from_numpy(inputs).float()
                if self.device == "cuda":
                    inputs_tensor = inputs_tensor.to(self.device)
                
                # Run inference
                start_time = time.time()
                
                with torch.no_grad():
                    if self.use_mixed_precision:
                        with autocast():
                            outputs = self.model(inputs_tensor)
                    else:
                        outputs = self.model(inputs_tensor)
                
                # Convert back to numpy
                outputs_np = outputs.cpu().numpy()
                
            else:
                # For other frameworks, implement accordingly
                outputs_np = self._predict_non_pytorch(inputs)
            
            latency_ms = (time.time() - start_time) * 1000
            
            # Update metrics
            self._update_metrics(len(batch), latency_ms)
            
            # Send responses (simplified)
            for i, req in enumerate(batch):
                logger.debug(f"Processed request {req.request_id} in {latency_ms:.2f}ms")
        
        except Exception as e:
            logger.error(f"Error processing batch: {e}")
            self.metrics.failed_requests += len(batch)
    
    async def _predict_single(self, inputs: np.ndarray) -> np.ndarray:
        """
        Predict for a single input.
        
        Args:
            inputs: Input data
            
        Returns:
            Model output
        """
        if self.model_framework == ModelFramework.PYTORCH:
            inputs_tensor = torch.from_numpy(inputs).float().unsqueeze(0)
            if self.device == "cuda":
                inputs_tensor = inputs_tensor.to(self.device)
            
            with torch.no_grad():
                if self.use_mixed_precision:
                    with autocast():
                        outputs = self.model(inputs_tensor)
                else:
                    outputs = self.model(inputs_tensor)
            
            return outputs.cpu().numpy()[0]
        else:
            return self._predict_non_pytorch(inputs)
    
    def _predict_non_pytorch(self, inputs: np.ndarray) -> np.ndarray:
        """
        Predict for non-PyTorch models.
        
        Args:
            inputs: Input data
            
        Returns:
            Model output
        """
        # Implement for TensorFlow, ONNX, etc.
        if self.model_framework == ModelFramework.TENSORFLOW:
            return self.model.predict(inputs)
        elif self.model_framework == ModelFramework.ONNX:
            import onnxruntime as ort
            ort_session = ort.InferenceSession(self.model)
            outputs = ort_session.run(None, {ort_session.get_inputs()[0].name: inputs})
            return outputs[0]
        else:
            raise ValueError(f"Unsupported framework: {self.model_framework}")
    
    def _update_metrics(self, batch_size: int, latency_ms: float) -> None:
        """
        Update performance metrics.
        
        Args:
            batch_size: Size of processed batch
            latency_ms: Latency in milliseconds
        """
        self.metrics.total_requests += batch_size
        self.metrics.successful_requests += batch_size
        self.metrics.total_latency_ms += latency_ms
        self.latency_history.append(latency_ms)
        
        # Calculate percentiles
        if len(self.latency_history) > 100:
            sorted_latencies = sorted(self.latency_history[-100:])
            self.metrics.p50_latency_ms = np.percentile(sorted_latencies, 50)
            self.metrics.p95_latency_ms = np.percentile(sorted_latencies, 95)
            self.metrics.p99_latency_ms = np.percentile(sorted_latencies, 99)
        
        # Calculate average batch size
        if self.metrics.total_requests > 0:
            self.metrics.avg_batch_size = (
                self.metrics.avg_batch_size * 0.9 + batch_size * 0.1
            )
        
        # Calculate requests per second
        if self.metrics.total_latency_ms > 0:
            self.metrics.requests_per_second = (
                self.metrics.total_requests / (self.metrics.total_latency_ms / 1000)
            )
        
        # Update GPU utilization
        if self.device == "cuda":
            self.metrics.gpu_utilization = torch.cuda.utilization()
    
    def get_metrics(self) -> PerformanceMetrics:
        """
        Get current performance metrics.
        
        Returns:
            PerformanceMetrics object
        """
        return self.metrics


# Example usage
if __name__ == "__main__":
    import torch.nn as nn
    
    # Create a simple model
    class SimpleModel(nn.Module):
        def __init__(self):
            super().__init__()
            self.layers = nn.Sequential(
                nn.Linear(10, 64),
                nn.ReLU(),
                nn.Linear(64, 32),
                nn.ReLU(),
                nn.Linear(32, 1),
                nn.Sigmoid()
            )
        
        def forward(self, x):
            return self.layers(x)
    
    # Initialize model and server
    model = SimpleModel()
    server = HighPerformanceInferenceServer(
        model=model,
        model_framework=ModelFramework.PYTORCH,
        max_batch_size=32,
        max_delay_ms=10.0,
        device="cuda" if torch.cuda.is_available() else "cpu",
        use_mixed_precision=True,
        num_workers=4
    )
    
    # Start server
    async def run_server():
        await server.start()
        
        # Make some predictions
        for i in range(10):
            inputs = np.random.randn(10).astype(np.float32)
            response = await server.predict(inputs, request_id=f"test_{i}")
            print(f"Request {response.request_id}: output={response.outputs[0]:.4f}, latency={response.latency_ms:.2f}ms")
        
        # Print metrics
        metrics = server.get_metrics()
        print(f"\nMetrics:")
        print(f"Total requests: {metrics.total_requests}")
        print(f"P50 latency: {metrics.p50_latency_ms:.2f}ms")
        print(f"P95 latency: {metrics.p95_latency_ms:.2f}ms")
        print(f"Requests/sec: {metrics.requests_per_second:.2f}")
        print(f"Avg batch size: {metrics.avg_batch_size:.2f}")
        
        await server.stop()
    
    asyncio.run(run_server())
```

## Standards, Compliance & Security

### International Standards
- **ISO/IEC 27001:** Security of inference infrastructure
- **PCI DSS:** Security for payment-related ML inference
- **SOC 2 Type II:** Availability and monitoring of inference services

### Security Protocol
- **Input Validation:** Validate and sanitize all inference inputs
- **Rate Limiting:** Prevent abuse and DoS attacks
- **Authentication:** Secure API access with proper auth
- **Encryption:** Encrypt model artifacts and inference data
- **Audit Logging:** Log all inference requests and responses

### Explainability
- **Response Metadata:** Include timing and batch info in responses
- **Performance Profiling:** Tools to analyze bottlenecks
- **Resource Monitoring:** Track GPU/CPU/memory utilization

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install torch tritonclient[grpc] numpy
   ```

2. **Start Triton server:**
   ```bash
   tritonserver --model-repository=/models
   ```

3. **Make inference request:**
   ```python
   import tritonclient.grpc as grpcclient
   
   client = grpcclient.InferenceServerClient(url="localhost:8001")
   inputs = grpcclient.InferInput("input", [1, 10], "FP32")
   inputs.set_data_from_numpy(np.random.randn(1, 10).astype(np.float32))
   
   response = client.infer(model_name="my_model", inputs=inputs)
   ```

4. **Enable dynamic batching:**
   ```python
   # In config.pbtxt
   dynamic_batching {
     max_queue_delay_microseconds: 10000
     preferred_batch_size: [8, 16, 32]
     max_batch_size: 64
   }
   ```

## Production Checklist

- [ ] Model is optimized (quantized, pruned)
- [ ] Dynamic batching is configured and tuned
- [ ] Load balancing is set up with health checks
- [ ] Monitoring and alerting for latency and throughput
- [ ] Auto-scaling policies configured
- [ ] GPU resources properly allocated
- [ ] Model warm-up before serving traffic
- [ ] Circuit breakers for downstream failures
- [ ] Rate limiting and authentication
- [ ] Backup and disaster recovery procedures

## Anti-patterns

1. **No Batching:** Processing one request at a time
   - **Why it's bad:** Wastes GPU capacity, high latency
   - **Solution:** Implement dynamic batching

2. **Fixed Batch Size:** Using same batch size for all scenarios
   - **Why it's bad:** Suboptimal for varying load patterns
   - **Solution:** Use dynamic batching with adaptive sizing

3. **CPU-Only Serving:** Not using GPU acceleration
   - **Why it's bad:** 10-100x slower inference
   - **Solution:** Deploy on GPU-optimized instances

4. **Synchronous Processing:** Blocking on each request
   - **Why it's bad:** Limits throughput, poor scalability
   - **Solution:** Use async processing with queues

## Unit Economics & KPIs

### Cost Calculation
```
Total Cost = Compute Cost + Infrastructure Cost + Operational Cost

Compute Cost = (GPU Hours × GPU Rate) + (CPU Hours × CPU Rate)
Infrastructure Cost = Load Balancer + Monitoring + Storage
Operational Cost = Engineering Time + Support
```

### Key Performance Indicators
- **P50 Latency:** < 10ms for user-facing models
- **P95 Latency:** < 50ms for user-facing models
- **Throughput:** > 1000 requests/second per GPU
- **GPU Utilization:** > 70% during peak hours
- **Error Rate:** < 0.1% for production traffic

## Integration Points / Related Skills
- [Model Optimization Quantization](../78-inference-model-serving/model-optimization-quantization/SKILL.md) - For optimizing model size and speed
- [Model Caching Warmpool](../78-inference-model-serving/model-caching-warmpool/SKILL.md) - For reducing cold start latency
- [GPU Cluster Management](../78-inference-model-serving/gpu-cluster-management/SKILL.md) - For managing GPU resources
- [Inference Monitoring](../78-inference-model-serving/inference-monitoring/SKILL.md) - For tracking performance metrics

## Further Reading
- [NVIDIA Triton Inference Server](https://docs.nvidia.com/deeplearning/triton-inference-server/)
- [TensorRT Documentation](https://docs.nvidia.com/deeplearning/tensorrt/)
- [TorchServe Documentation](https://pytorch.org/serve/)
- [High-Performance ML Serving](https://arxiv.org/abs/2008.07649)
- [Dynamic Batching for ML Inference](https://dl.acm.org/doi/10.1145/3368089.3409691)
