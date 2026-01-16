---
name: Model Serving & Inference
description: Comprehensive guide to deploying and serving LLM models including optimization, batching, caching, and production infrastructure
---

# Model Serving & Inference

## Overview

Model serving is the process of deploying ML models to production and handling inference requests efficiently at scale.

---

## Serving Architectures

### Synchronous (Request-Response)
```
Client → API → Model → Response

Use for: Real-time applications (chatbots, search)
Latency: Low (milliseconds to seconds)
```

### Asynchronous (Queue-Based)
```
Client → Queue → Worker → Model → Result Store → Client polls

Use for: Batch processing, long-running tasks
Latency: Higher (seconds to minutes)
```

### Streaming
```
Client ← Stream ← Model (generates tokens)

Use for: Chat interfaces, real-time generation
Latency: Progressive (first token fast, then streaming)
```

---

## Inference Optimization

### Model Quantization
```python
# Reduce model size and increase speed

# FP16 (half precision)
model = AutoModelForCausalLM.from_pretrained(
    "gpt2",
    torch_dtype=torch.float16
)

# INT8 quantization
from transformers import BitsAndBytesConfig

quantization_config = BitsAndBytesConfig(load_in_8bit=True)
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b",
    quantization_config=quantization_config
)

# INT4 (GPTQ)
from auto_gptq import AutoGPTQForCausalLM

model = AutoGPTQForCausalLM.from_quantized(
    "TheBloke/Llama-2-7B-GPTQ",
    use_safetensors=True
)
```

### Dynamic Batching
```python
# Batch multiple requests together

class DynamicBatcher:
    def __init__(self, model, max_batch_size=8, max_wait_ms=100):
        self.model = model
        self.max_batch_size = max_batch_size
        self.max_wait_ms = max_wait_ms
        self.queue = []
    
    async def add_request(self, request):
        future = asyncio.Future()
        self.queue.append((request, future))
        
        # Trigger batch if full
        if len(self.queue) >= self.max_batch_size:
            await self.process_batch()
        
        return await future
    
    async def process_batch(self):
        if not self.queue:
            return
        
        batch = self.queue[:self.max_batch_size]
        self.queue = self.queue[self.max_batch_size:]
        
        # Batch inference
        inputs = [req for req, _ in batch]
        outputs = self.model.generate_batch(inputs)
        
        # Return results
        for (_, future), output in zip(batch, outputs):
            future.set_result(output)
```

### KV Cache Optimization
```python
# Reuse key-value cache for faster generation

# Enable KV cache
model.config.use_cache = True

# Generate with cache
outputs = model.generate(
    input_ids,
    max_length=100,
    use_cache=True,  # Reuse KV cache
    past_key_values=past_kv  # From previous generation
)
```

---

## Caching Strategies

### Prompt Caching
```python
import hashlib
from functools import lru_cache

class PromptCache:
    def __init__(self):
        self.cache = {}
    
    def get_cache_key(self, prompt, params):
        # Hash prompt + parameters
        key = hashlib.md5(
            f"{prompt}{params}".encode()
        ).hexdigest()
        return key
    
    def get(self, prompt, params):
        key = self.get_cache_key(prompt, params)
        return self.cache.get(key)
    
    def set(self, prompt, params, response):
        key = self.get_cache_key(prompt, params)
        self.cache[key] = response

cache = PromptCache()

# Check cache before inference
cached = cache.get(prompt, params)
if cached:
    return cached

# Generate and cache
response = model.generate(prompt)
cache.set(prompt, params, response)
```

### Semantic Caching
```python
from sentence_transformers import SentenceTransformer
import numpy as np

class SemanticCache:
    def __init__(self, threshold=0.95):
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.cache = []  # [(embedding, response)]
        self.threshold = threshold
    
    def get(self, prompt):
        if not self.cache:
            return None
        
        # Encode prompt
        embedding = self.encoder.encode(prompt)
        
        # Find similar cached prompts
        for cached_emb, cached_response in self.cache:
            similarity = np.dot(embedding, cached_emb)
            if similarity >= self.threshold:
                return cached_response
        
        return None
    
    def set(self, prompt, response):
        embedding = self.encoder.encode(prompt)
        self.cache.append((embedding, response))

semantic_cache = SemanticCache()

# Check semantic cache
cached = semantic_cache.get(prompt)
if cached:
    return cached
```

---

## Serving Frameworks

### vLLM (High-Throughput)
```python
from vllm import LLM, SamplingParams

# Initialize model
llm = LLM(model="meta-llama/Llama-2-7b-hf")

# Sampling parameters
sampling_params = SamplingParams(
    temperature=0.7,
    top_p=0.9,
    max_tokens=100
)

# Generate
prompts = ["Hello, my name is", "The capital of France is"]
outputs = llm.generate(prompts, sampling_params)

for output in outputs:
    print(output.outputs[0].text)
```

**vLLM Server:**
```bash
# Start server
python -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Llama-2-7b-hf \
    --port 8000

# Call API
curl http://localhost:8000/v1/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "meta-llama/Llama-2-7b-hf",
        "prompt": "Hello, my name is",
        "max_tokens": 50
    }'
```

### TGI (Text Generation Inference)
```bash
# Run with Docker
docker run --gpus all --shm-size 1g -p 8080:80 \
    ghcr.io/huggingface/text-generation-inference:latest \
    --model-id meta-llama/Llama-2-7b-hf

# Call API
curl http://localhost:8080/generate \
    -X POST \
    -d '{"inputs":"What is deep learning?","parameters":{"max_new_tokens":50}}' \
    -H 'Content-Type: application/json'
```

### TensorRT-LLM (NVIDIA)
```python
# Optimized for NVIDIA GPUs
# Compile model to TensorRT
trtllm-build \
    --checkpoint_dir ./llama-7b \
    --output_dir ./llama-7b-trt \
    --gemm_plugin float16

# Serve with Triton
tritonserver --model-repository=./model_repo
```

---

## Load Balancing

### Round Robin
```python
class LoadBalancer:
    def __init__(self, endpoints):
        self.endpoints = endpoints
        self.current = 0
    
    def get_endpoint(self):
        endpoint = self.endpoints[self.current]
        self.current = (self.current + 1) % len(self.endpoints)
        return endpoint

lb = LoadBalancer([
    "http://gpu1:8000",
    "http://gpu2:8000",
    "http://gpu3:8000"
])

endpoint = lb.get_endpoint()
response = requests.post(f"{endpoint}/generate", json=payload)
```

### Least Connections
```python
class LeastConnectionsLB:
    def __init__(self, endpoints):
        self.endpoints = {ep: 0 for ep in endpoints}
    
    def get_endpoint(self):
        # Return endpoint with fewest connections
        return min(self.endpoints, key=self.endpoints.get)
    
    def increment(self, endpoint):
        self.endpoints[endpoint] += 1
    
    def decrement(self, endpoint):
        self.endpoints[endpoint] -= 1
```

---

## Monitoring

### Latency Tracking
```python
import time

class LatencyTracker:
    def __init__(self):
        self.latencies = []
    
    def track(self, func):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            latency = (time.time() - start) * 1000  # ms
            
            self.latencies.append(latency)
            
            # Log metrics
            print(f"Latency: {latency:.2f}ms")
            
            return result
        return wrapper

tracker = LatencyTracker()

@tracker.track
def generate(prompt):
    return model.generate(prompt)
```

### Throughput Monitoring
```python
from collections import deque
import time

class ThroughputMonitor:
    def __init__(self, window_seconds=60):
        self.window = window_seconds
        self.requests = deque()
    
    def record_request(self):
        now = time.time()
        self.requests.append(now)
        
        # Remove old requests
        cutoff = now - self.window
        while self.requests and self.requests[0] < cutoff:
            self.requests.popleft()
    
    def get_throughput(self):
        return len(self.requests) / self.window

monitor = ThroughputMonitor()

# Record each request
monitor.record_request()

# Get requests per second
rps = monitor.get_throughput()
print(f"Throughput: {rps:.2f} req/s")
```

---

## Auto-Scaling

### Horizontal Scaling
```yaml
# Kubernetes HPA
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: llm-server
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: llm-server
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### Queue-Based Scaling
```python
# Scale based on queue depth

def check_scaling():
    queue_depth = get_queue_depth()
    current_workers = get_worker_count()
    
    # Scale up if queue is backing up
    if queue_depth > 100 and current_workers < 10:
        scale_up()
    
    # Scale down if queue is empty
    elif queue_depth < 10 and current_workers > 2:
        scale_down()
```

---

## Best Practices

### 1. Use Appropriate Hardware
```
Small models (< 7B): CPU or single GPU
Medium models (7-13B): Single GPU (A100, H100)
Large models (70B+): Multi-GPU or model parallelism
```

### 2. Optimize Batch Size
```python
# Find optimal batch size
batch_sizes = [1, 2, 4, 8, 16]
for batch_size in batch_sizes:
    throughput = benchmark(batch_size)
    print(f"Batch {batch_size}: {throughput} req/s")
```

### 3. Monitor GPU Utilization
```python
import nvidia_smi

nvidia_smi.nvmlInit()
handle = nvidia_smi.nvmlDeviceGetHandleByIndex(0)

# Get GPU utilization
util = nvidia_smi.nvmlDeviceGetUtilizationRates(handle)
print(f"GPU: {util.gpu}%, Memory: {util.memory}%")
```

### 4. Implement Timeouts
```python
import asyncio

async def generate_with_timeout(prompt, timeout=30):
    try:
        return await asyncio.wait_for(
            model.generate(prompt),
            timeout=timeout
        )
    except asyncio.TimeoutError:
        return "Request timeout"
```

---

## Summary

**Model Serving:** Deploy and serve ML models at scale

**Architectures:**
- Synchronous (real-time)
- Asynchronous (batch)
- Streaming (progressive)

**Optimization:**
- Quantization (FP16, INT8, INT4)
- Dynamic batching
- KV cache
- Prompt caching

**Frameworks:**
- vLLM (high throughput)
- TGI (Hugging Face)
- TensorRT-LLM (NVIDIA)

**Scaling:**
- Load balancing
- Auto-scaling
- Multi-GPU

**Monitoring:**
- Latency
- Throughput
- GPU utilization
