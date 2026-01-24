---
name: Local LLM Deployment
description: Comprehensive guide for deploying LLMs locally using Ollama, vLLM, and llama.cpp
---

# Local LLM Deployment

## Overview
Comprehensive guide for deploying LLMs locally using Ollama, vLLM, and llama.cpp.

## Prerequisites

- Basic understanding of Docker and containerization
- GPU hardware knowledge (NVIDIA CUDA)
- Python programming skills
- Linux command line familiarity
- Understanding of model quantization and optimization

## Key Concepts

- **Ollama**: User-friendly tool for running LLMs locally with simple CLI and API
- **vLLM**: High-performance LLM serving engine with optimized inference
- **llama.cpp**: Lightweight C++ implementation for running LLMs on consumer hardware
- **GGUF Format**: Efficient binary format for quantized models used by llama.cpp
- **Quantization**: Reducing model precision to decrease memory usage and improve speed
- **Tensor Parallelism**: Splitting model layers across multiple GPUs
- **Pipeline Parallelism**: Splitting model pipeline stages across multiple GPUs
- **Modelfile**: Ollama's configuration file for custom models
- **Context Window**: Maximum number of tokens a model can process
- **GPU Memory Utilization**: Percentage of GPU memory allocated to the model
- **Swap Space**: CPU memory used as overflow for GPU memory
- **Batch Processing**: Processing multiple prompts simultaneously for efficiency
- **Streaming**: Real-time token-by-token response delivery

---

## 1. Ollama Setup and Usage

### 1.1 Installation

```bash
# Linux/macOS
curl -fsSL https://ollama.com/install.sh | sh

# macOS (Homebrew)
brew install ollama

# Windows
# Download installer from https://ollama.com/download

# Docker
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

### 1.2 Model Management

```bash
# Pull a model
ollama pull llama2
ollama pull mistral
ollama pull codellama

# List available models
ollama list

# Show model information
ollama show llama2

# Remove a model
ollama rm llama2

# Create custom model
ollama create mymodel -f Modelfile

# Update a model
ollama pull llama2:latest
```

### 1.3 API Integration

```python
import requests
import json

class OllamaClient:
    """Ollama API client."""

    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url

    def generate(
        self,
        model: str,
        prompt: str,
        stream: bool = False,
        options: dict = None
    ):
        """Generate completion."""
        url = f"{self.base_url}/api/generate"

        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream
        }

        if options:
            payload["options"] = options

        if stream:
            return self._stream_response(url, payload)
        else:
            response = requests.post(url, json=payload)
            return response.json()

    def chat(
        self,
        model: str,
        messages: list,
        stream: bool = False
    ):
        """Chat completion."""
        url = f"{self.base_url}/api/chat"

        payload = {
            "model": model,
            "messages": messages,
            "stream": stream
        }

        if stream:
            return self._stream_response(url, payload)
        else:
            response = requests.post(url, json=payload)
            return response.json()

    def _stream_response(self, url: str, payload: dict):
        """Handle streaming response."""
        response = requests.post(url, json=payload, stream=True)

        for line in response.iter_lines():
            if line:
                chunk = json.loads(line)
                yield chunk.get("response", "")

    def list_models(self):
        """List available models."""
        url = f"{self.base_url}/api/tags"
        response = requests.get(url)
        return response.json()

# Usage
client = OllamaClient()

# Generate completion
response = client.generate(
    model="llama2",
    prompt="What is the capital of France?"
)
print(response["response"])

# Chat completion
messages = [
    {"role": "user", "content": "Hello!"}
]
response = client.chat(model="llama2", messages=messages)
print(response["message"]["content"])

# Streaming
for chunk in client.generate(
    model="llama2",
    prompt="Tell me a story",
    stream=True
):
    print(chunk, end="", flush=True)
```

### 1.4 Modelfile Customization

```dockerfile
# Modelfile for custom model
FROM llama2

PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40
PARAMETER num_ctx 4096

SYSTEM """
You are a helpful assistant with expertise in Python programming.
Always provide clear, well-commented code examples.
"""

TEMPLATE """
{{- if .System }}<|start_header_id|>system<|end_header_id|>
{{ .System }}<|end_header_id|>
{{- end if }}
{{- range .Messages }}
{{- if eq .Role "user" }}<|start_header_id|>user<|end_header_id|>
{{- else if eq .Role "assistant" }}<|start_header_id|>assistant<|end_header_id|>
{{- end if }}
{{ .Content }}
<|end_header_id|>
{{- end }}
<|start_header_id|>assistant<|end_header_id|>
"""
```

```bash
# Build custom model
ollama create python-assistant -f Modelfile

# Run custom model
ollama run python-assistant
```

---

## 2. vLLM Deployment

### 2.1 Installation

```bash
# Install from PyPI
pip install vllm

# Install from source
git clone https://github.com/vllm-project/vllm.git
cd vllm
pip install -e .

# Install with GPU support
pip install vllm --extra-index-url https://download.pytorch.org/whl/cu118
```

### 2.2 Server Setup

```python
from vllm import LLM, SamplingParams
from vllm.entrypoints.api_server import serve

# Start vLLM server
serve(
    model="meta-llama/Llama-2-7b-hf",
    tensor-parallel-size=1,
    pipeline-parallel-size=1,
    host="0.0.0.0",
    port=8000,
    dtype="auto",
    max-model-len=4096,
    gpu-memory-utilization=0.9,
    enforce-eager=True,
)
```

```bash
# Start server from command line
python -m vllm.entrypoints.api_server \
    --model meta-llama/Llama-2-7b-hf \
    --tensor-parallel-size 1 \
    --pipeline-parallel-size 1 \
    --host 0.0.0.0 \
    --port 8000 \
    --dtype auto \
    --max-model-len 4096
```

### 2.3 Configuration

```python
from vllm import LLM, SamplingParams

# Initialize LLM
llm = LLM(
    model="meta-llama/Llama-2-7b-hf",
    tensor_parallel_size=1,
    pipeline_parallel_size=1,
    dtype="auto",
    max_model_len=4096,
    trust_remote_code=False,
    download_dir="./models",
    load_format="auto",
    quantization=None,  # "awq", "gptq", "squeezellm"
    enforce_eager=True,
    gpu_memory_utilization=0.9,
    swap_space=4,
)

# Sampling parameters
sampling_params = SamplingParams(
    n=1,                    # Number of output sequences
    best_of=1,               # Number of best sequences
    presence_penalty=0.0,      # Presence penalty
    frequency_penalty=0.0,     # Frequency penalty
    repetition_penalty=1.0,     # Repetition penalty
    temperature=0.7,          # Sampling temperature
    top_p=0.9,               # Nucleus sampling
    top_k=-1,                # Top-k sampling
    min_p=0.0,               # Minimum probability
    use_beam_search=False,     # Use beam search
    length_penalty=1.0,       # Length penalty
    early_stopping=False,      # Early stopping
    stop=[],                  # Stop tokens
    stop_token_ids=[],          # Stop token IDs
    ignore_eos=False,          # Ignore EOS token
    max_tokens=100,           # Max tokens to generate
    logprobs=None,             # Return log probabilities
    prompt_logprobs=None,      # Return prompt log probabilities
    skip_special_tokens=True,  # Skip special tokens
    spaces_between_special_tokens=True,
)

# Generate
outputs = llm.generate(
    prompts=["Hello, how are you?"],
    sampling_params=sampling_params
)

for output in outputs:
    print(f"Output: {output.outputs[0].text}")
```

### 2.4 Performance Tuning

```python
from vllm import LLM

# For multiple GPUs
llm = LLM(
    model="meta-llama/Llama-2-7b-hf",
    tensor_parallel_size=2,  # Split model across 2 GPUs
    pipeline_parallel_size=1,
)

# For pipeline parallelism
llm = LLM(
    model="meta-llama/Llama-2-70b-hf",
    tensor_parallel_size=1,
    pipeline_parallel_size=4,  # Split across 4 pipeline stages
)

# For quantized models
llm = LLM(
    model="meta-llama/Llama-2-7b-hf",
    quantization="awq",  # or "gptq", "squeezellm"
)

# For memory optimization
llm = LLM(
    model="meta-llama/Llama-2-7b-hf",
    gpu_memory_utilization=0.9,  # Use 90% of GPU memory
    swap_space=4,  # Swap 4GB to CPU if needed
)
```

---

## 3. llama.cpp

### 3.1 Building

```bash
# Clone repository
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp

# Build
cmake -B build
cmake --build build --config Release

# Or using make
make

# Install Python bindings
pip install llama-cpp-python
```

### 3.2 Model Formats (GGUF)

```python
from llama_cpp import Llama

# Load GGUF model
model = Llama(
    model_path="./models/llama-2-7b-chat.Q4_K_M.gguf",
    n_ctx=4096,              # Context size
    n_gpu_layers=-1,          # -1 = all layers on GPU
    seed=42,
    f16_kv=True,              # Use FP16 for KV cache
    logits_all=False,          # Return all logits
    vocab_only=False,
    use_mmap=True,            # Use memory mapping
    use_mlock=False,           # Lock memory
    embedding=False,           # Return embeddings
    n_threads=8,             # Number of threads
    n_batch=512,              # Batch size
)

# Generate
output = model(
    "Hello, how are you?",
    max_tokens=100,
    stop=["\n", "User:", "Assistant:"],
    echo=False,
    temperature=0.7,
    top_p=0.9,
    top_k=40,
    repeat_penalty=1.0,
    presence_penalty=0.0,
    frequency_penalty=0.0,
)

print(output['choices'][0]['text'])
```

### 3.3 Server Mode

```bash
# Start llama.cpp server
./server \
    --model ./models/llama-2-7b-chat.Q4_K_M.gguf \
    --host 0.0.0.0 \
    --port 8080 \
    --ctx-size 4096 \
    --n-gpu-layers -1 \
    --threads 8 \
    --n-parallel 4 \
    --batch-size 512 \
    --temperature 0.7 \
    --top-p 0.9

# Start with OpenAI-compatible API
./server \
    --model ./models/llama-2-7b-chat.Q4_K_M.gguf \
    --port 8080 \
    --host 0.0.0.0 \
    --ctx-size 4096 \
    --n-gpu-layers -1 \
    --log-format json
```

```python
import requests

# Use llama.cpp server
url = "http://localhost:8080/completion"

payload = {
    "prompt": "Hello, how are you?",
    "n_predict": 100,
    "temperature": 0.7,
    "top_p": 0.9,
    "stop": ["\n", "User:", "Assistant:"]
}

response = requests.post(url, json=payload)
print(response.json())
```

---

## 4. Docker Deployment

### 4.1 Ollama Docker

```dockerfile
# Dockerfile for Ollama
FROM ollama/ollama

# Copy custom models
COPY models /root/.ollama/models

# Set environment
ENV OLLAMA_HOST=0.0.0.0
ENV OLLAMA_PORT=11434

# Expose port
EXPOSE 11434

# Start server
CMD ["ollama", "serve"]
```

```yaml
# docker-compose.yml
version: '3.3'

services:
  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    ports:
      - 11434:11434
    volumes:
      - ./ollama-data:/root/.ollama
    environment:
      - OLLAMA_HOST=0.0.0.0
      - OLLAMA_PORT=11434
    restart: unless-stopped
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

### 4.2 vLLM Docker

```dockerfile
# Dockerfile for vLLM
FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04

# Install Python
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install vLLM
RUN pip install vllm

# Expose port
EXPOSE 8000

# Start server
CMD ["python", "-m", "vllm.entrypoints.api_server", \
     "--model", "meta-llama/Llama-2-7b-hf", \
     "--host", "0.0.0.0", \
     "--port", "8000"]
```

### 4.3 llama.cpp Docker

```dockerfile
# Dockerfile for llama.cpp
FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    git \
    cmake \
    build-essential \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Clone and build llama.cpp
RUN git clone https://github.com/ggerganov/llama.cpp.git /app/llama.cpp
WORKDIR /app/llama.cpp
RUN cmake -B build && cmake --build build --config Release

# Install Python bindings
RUN pip install llama-cpp-python

# Expose port
EXPOSE 8080

# Start server
CMD ["./build/bin/server", \
     "--model", "/models/llama-2-7b-chat.Q4_K_M.gguf", \
     "--host", "0.0.0.0", \
     "--port", "8080"]
```

---

## 5. Model Selection Guide

### 5.1 Model Comparison

| Model | Parameters | VRAM Required | Speed | Use Case |
|-------|------------|---------------|-------|----------|
| Llama-2-7B | 7B | 6GB | Fast | General purpose |
| Llama-2-13B | 13B | 12GB | Medium | Complex tasks |
| Llama-2-70B | 70B | 40GB | Slow | High quality |
| Mistral-7B | 7B | 6GB | Fast | General purpose |
| CodeLlama-7B | 7B | 6GB | Fast | Code generation |
| Phi-2 | 2.7B | 4GB | Very Fast | Edge deployment |
| TinyLlama-1.1B | 1.1B | 2GB | Very Fast | Mobile/embedded |

### 5.2 Selection Criteria

```python
def select_model(
    available_vram_gb: int,
    use_case: str = "general",
    speed_preference: str = "fast"
) -> str:
    """Select model based on constraints."""

    # Model specifications
    models = {
        "llama-2-7b": {
            "vram": 6,
            "speed": "fast",
            "use_cases": ["general", "chat"]
        },
        "llama-2-13b": {
            "vram": 12,
            "speed": "medium",
            "use_cases": ["general", "chat", "reasoning"]
        },
        "mistral-7b": {
            "vram": 6,
            "speed": "fast",
            "use_cases": ["general", "chat", "code"]
        },
        "codellama-7b": {
            "vram": 6,
            "speed": "fast",
            "use_cases": ["code", "technical"]
        },
        "phi-2": {
            "vram": 4,
            "speed": "very_fast",
            "use_cases": ["general", "edge"]
        },
    }

    # Filter by VRAM
    suitable_models = {
        name: spec for name, spec in models.items()
        if spec["vram"] <= available_vram_gb
    }

    # Filter by use case
    if use_case != "all":
        suitable_models = {
            name: spec for name, spec in suitable_models.items()
            if use_case in spec["use_cases"]
        }

    # Sort by speed preference
    speed_order = {"very_fast": 0, "fast": 1, "medium": 2, "slow": 3}
    suitable_models = sorted(
        suitable_models.items(),
        key=lambda x: speed_order.get(x[1]["speed"], 4)
    )

    if not suitable_models:
        raise ValueError("No suitable model found")

    return suitable_models[0][0]

# Usage
model = select_model(
    available_vram_gb=8,
    use_case="general",
    speed_preference="fast"
)
print(f"Recommended model: {model}")
```

---

## 6. Quantization Strategies

### 6.1 Quantization Levels

| Quantization | Size Reduction | Quality Loss | VRAM Saving |
|-------------|----------------|---------------|--------------|
| FP16 | 2x | None | ~50% |
| Q8_0 | 4x | Minimal | ~75% |
| Q4_K_M | 6x | Low | ~85% |
| Q4_K_S | 6x | Medium | ~85% |
| Q2_K | 10x | High | ~95% |

### 6.2 Quantization with llama.cpp

```bash
# Quantize model to Q4
./quantize ./models/llama-2-7b-f16.gguf \
    ./models/llama-2-7b-q4.gguf \
    Q4_K_M

# Quantize to Q8
./quantize ./models/llama-2-7b-f16.gguf \
    ./models/llama-2-7b-q8.gguf \
    Q8_0

# Quantize with custom settings
./quantize ./models/llama-2-7b-f16.gguf \
    ./models/llama-2-7b-q4.gguf \
    Q4_K_M \
    --imatrix ./models/llama-2-7b-imatrix.dat
```

### 6.3 Quantization with AutoGPTQ

```python
from auto_gptq import AutoGPTQForCausalLM, BaseQuantizeConfig
from transformers import AutoTokenizer

# Load model
model_id = "meta-llama/Llama-2-7b-hf"
tokenizer = AutoTokenizer.from_pretrained(model_id)

# Quantization config
quantize_config = BaseQuantizeConfig(
    bits=4,
    group_size=128,
    damp_percent=0.01,
    desc_act=False,
    sym=True,
    true_sequential=True,
    model_name_base=model_id,
    model_file_name_base="llama-2-7b-gptq",
)

# Load quantized model
model = AutoGPTQForCausalLM.from_pretrained(
    model_id,
    quantize_config=quantize_config,
    use_triton=False,
    inject_fused_attention=False,
    inject_fused_mlp=False,
    use_cuda_fp16=True,
)
```

---

## 7. GPU Configuration

### 7.1 Multi-GPU Setup

```python
# vLLM with tensor parallelism
from vllm import LLM

llm = LLM(
    model="meta-llama/Llama-2-70b-hf",
    tensor_parallel_size=4,  # Split across 4 GPUs
    pipeline_parallel_size=1,
)
```

```bash
# Start with multiple GPUs
python -m vllm.entrypoints.api_server \
    --model meta-llama/Llama-2-70b-hf \
    --tensor-parallel-size 4 \
    --pipeline-parallel-size 1 \
    --host 0.0.0.0 \
    --port 8000
```

### 7.2 GPU Memory Optimization

```python
# Memory-efficient configuration
llm = LLM(
    model="meta-llama/Llama-2-7b-hf",
    gpu_memory_utilization=0.9,  # Leave 10% free
    swap_space=4,              # 4GB swap to CPU
    max_model_len=4096,        # Limit context
    enforce_eager=True,         # Eager mode
)
```

### 7.3 GPU Selection

```python
import torch

def select_gpu(gpu_memory_gb: int) -> int:
    """Select appropriate GPU based on memory requirements."""
    available_gpus = torch.cuda.device_count()

    for i in range(available_gpus):
        props = torch.cuda.get_device_properties(i)
        total_memory_gb = props.total_memory / 1024**3

        if total_memory_gb >= gpu_memory_gb:
            return i

    raise ValueError(f"No GPU with {gpu_memory_gb}GB available")

# Usage
gpu_id = select_gpu(gpu_memory_gb=12)
torch.cuda.set_device(gpu_id)
```

---

## 8. Performance Optimization

### 8.1 Batch Processing

```python
from vllm import LLM, SamplingParams

llm = LLM(model="meta-llama/Llama-2-7b-hf")

# Batch generation
prompts = [
    "Hello, how are you?",
    "What is the capital of France?",
    "Tell me a joke."
]

sampling_params = SamplingParams(
    temperature=0.7,
    top_p=0.9,
    max_tokens=100
)

outputs = llm.generate(prompts, sampling_params)

for i, output in enumerate(outputs):
    print(f"Prompt {i}: {output.outputs[0].text}")
```

### 8.2 Caching

```python
from functools import lru_cache
import hashlib
import pickle
from pathlib import Path

class ModelCache:
    """Cache model outputs."""

    def __init__(self, cache_dir="./cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def _get_cache_key(self, prompt: str, model: str) -> str:
        """Generate cache key."""
        key = f"{model}:{prompt}"
        return hashlib.md5(key.encode()).hexdigest()

    def get(self, prompt: str, model: str) -> str:
        """Get cached output."""
        cache_key = self._get_cache_key(prompt, model)
        cache_file = self.cache_dir / f"{cache_key}.pkl"

        if cache_file.exists():
            with open(cache_file, "rb") as f:
                return pickle.load(f)
        return None

    def set(self, prompt: str, model: str, output: str):
        """Cache output."""
        cache_key = self._get_cache_key(prompt, model)
        cache_file = self.cache_dir / f"{cache_key}.pkl"

        with open(cache_file, "wb") as f:
            pickle.dump(output, f)

# Usage
cache = ModelCache()

# Check cache
cached_output = cache.get("Hello, how are you?", "llama-2-7b")
if cached_output:
    print(f"Cached: {cached_output}")
else:
    # Generate output
    output = model.generate("Hello, how are you?")
    cache.set("Hello, how are you?", "llama-2-7b", output)
```

### 8.3 Streaming Optimization

```python
from vllm import LLM, SamplingParams

llm = LLM(model="meta-llama/Llama-2-7b-hf")

# Streaming generation
sampling_params = SamplingParams(
    temperature=0.7,
    top_p=0.9,
    max_tokens=100
)

prompts = ["Tell me a story about a robot."]

outputs = llm.generate(prompts, sampling_params)

for output in outputs:
    for token in output.outputs[0].token_ids:
        # Process each token
        print(token, end="", flush=True)
```

---

## 9. Monitoring

### 9.1 Performance Metrics

```python
import time
import psutil
import torch

class PerformanceMonitor:
    """Monitor model performance."""

    def __init__(self):
        self.metrics = []

    def measure_inference(
        self,
        model,
        prompt: str,
        max_tokens: int = 100
    ):
        """Measure inference performance."""
        # Start timing
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024**2  # GB

        # Generate
        output = model(prompt, max_tokens=max_tokens)

        # End timing
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss / 1024**2  # GB

        # GPU memory
        if torch.cuda.is_available():
            gpu_memory = torch.cuda.max_memory_allocated() / 1024**3  # GB
            torch.cuda.reset_peak_memory_stats()
        else:
            gpu_memory = 0

        metrics = {
            "prompt_length": len(prompt),
            "output_length": len(output),
            "latency_ms": (end_time - start_time) * 1000,
            "tokens_per_second": len(output) / (end_time - start_time),
            "memory_delta_gb": end_memory - start_memory,
            "gpu_memory_gb": gpu_memory
        }

        self.metrics.append(metrics)
        return metrics

    def get_summary(self):
        """Get performance summary."""
        if not self.metrics:
            return {}

        return {
            "avg_latency_ms": sum(m["latency_ms"] for m in self.metrics) / len(self.metrics),
            "avg_tokens_per_second": sum(m["tokens_per_second"] for m in self.metrics) / len(self.metrics),
            "avg_gpu_memory_gb": sum(m["gpu_memory_gb"] for m in self.metrics) / len(self.metrics),
        "total_inferences": len(self.metrics)
        }

# Usage
monitor = PerformanceMonitor()

for i in range(10):
    monitor.measure_inference(model, "Hello, how are you?")

summary = monitor.get_summary()
print(f"Average latency: {summary['avg_latency_ms']:.2f}ms")
print(f"Average tokens/sec: {summary['avg_tokens_per_second']:.2f}")
```

### 9.2 Resource Monitoring

```python
import GPUtil
import psutil
import time

class ResourceMonitor:
    """Monitor system resources."""

    def __init__(self, interval=1.0):
        self.interval = interval
        self.running = False

    def start(self):
        """Start monitoring."""
        self.running = True
        while self.running:
            # GPU stats
            gpus = GPUtil.getGPUs()
            for i, gpu in enumerate(gpus):
                print(f"GPU {i}: {gpu.load*100:.1f}% load, {gpu.memoryUsed:.1f}GB/{gpu.memoryTotal:.1f}GB")

            # CPU stats
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()

            print(f"CPU: {cpu_percent:.1f}%")
            print(f"Memory: {memory.percent:.1f}% used ({memory.used/1024**3:.2f}GB/{memory.total/1024**3:.2f}GB)")

            time.sleep(self.interval)

    def stop(self):
        """Stop monitoring."""
        self.running = False

# Usage
monitor = ResourceMonitor(interval=1.0)
monitor.start()

# ... run your inference ...

monitor.stop()
```

---

## 10. Production Checklist

### 10.1 Pre-Deployment Checklist

- [ ] **Model Selection**
  - [ ] Model tested and validated
  - [ ] Model quantized if needed
  - [ ] Model size fits available VRAM

- [ ] **Performance**
  - [ ] Latency meets requirements
  - [ ] Throughput tested
  - [ ] Memory usage optimized

- [ ] **Reliability**
  - [ ] Error handling implemented
  - [ ] Graceful degradation for failures
  - [ ] Retry logic for transient failures

- [ ] **Security**
  - [ ] API authentication configured
  - [ ] Rate limiting enabled
  - [ ] Input validation implemented

- [ ] **Monitoring**
  - [ ] Metrics collection configured
  - [ ] Logging enabled
  - [ ] Alert thresholds set

- [ ] **Deployment**
  - [ ] Docker image created
  - [ ] Environment variables configured
  - [ ] Health check endpoint
  - [ ] Auto-restart policy

### 10.2 Post-Deployment Checklist

- [ ] **Validation**
  - [ ] Smoke tests passed
  - [ ] Load testing completed
  - [ ] Performance metrics monitored

- [ ] **Documentation**
  - [ ] API documentation updated
  - [ ] Deployment guide created
  - [ ] Known issues documented

---

## Related Skills

- [`06-ai-ml-production/llm-integration`](06-ai-ml-production/llm-integration/SKILL.md)
- [`06-ai-ml-production/ai-observability`](06-ai-ml-production/ai-observability/SKILL.md)
- [`06-ai-ml-production/embedding-models`](06-ai-ml-production/embedding-models/SKILL.md)
- [`06-ai-ml-production/agent-patterns`](06-ai-ml-production/agent-patterns/SKILL.md)
- [`05-ai-ml-core/pytorch-deployment`](05-ai-ml-core/pytorch-deployment/SKILL.md)

## Additional Resources

- [Ollama Documentation](https://ollama.com/docs/)
- [vLLM Documentation](https://docs.vllm.ai/)
- [llama.cpp Documentation](https://github.com/ggerganov/llama.cpp)
- [AutoGPTQ Documentation](https://github.com/AutoGPTQ/AutoGPTQ)
