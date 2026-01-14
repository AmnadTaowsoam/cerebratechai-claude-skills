# Local LLM Deployment Guide

## Overview
Deploy and run LLMs locally using Ollama, vLLM, or llama.cpp

## Option 1: Ollama (Easiest)

### Installation
```bash
# macOS/Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows
# Download from ollama.com
```

### Basic Usage
```bash
# Pull a model
ollama pull llama2
ollama pull mistral
ollama pull codellama

# Run model
ollama run llama2

# List models
ollama list

# Remove model
ollama rm llama2
```

### API Integration (TypeScript)
```typescript
interface OllamaResponse {
  model: string
  response: string
  done: boolean
}

async function generateCompletion(
  prompt: string,
  model: string = 'llama2'
): Promise<string> {
  const response = await fetch('http://localhost:11434/api/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model,
      prompt,
      stream: false,
    }),
  })
  
  const data: OllamaResponse = await response.json()
  return data.response
}

// Streaming
async function* generateStream(
  prompt: string,
  model: string = 'llama2'
): AsyncIterable<string> {
  const response = await fetch('http://localhost:11434/api/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model,
      prompt,
      stream: true,
    }),
  })
  
  const reader = response.body!.getReader()
  const decoder = new TextDecoder()
  
  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    
    const chunk = decoder.decode(value)
    const lines = chunk.split('\n').filter(Boolean)
    
    for (const line of lines) {
      const data: OllamaResponse = JSON.parse(line)
      if (data.response) {
        yield data.response
      }
    }
  }
}
```

### Python Integration
```python
import requests
import json
from typing import Iterator

def generate_completion(prompt: str, model: str = "llama2") -> str:
    """Generate completion using Ollama."""
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False},
    )
    return response.json()["response"]

def generate_stream(prompt: str, model: str = "llama2") -> Iterator[str]:
    """Stream completion from Ollama."""
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": True},
        stream=True,
    )
    
    for line in response.iter_lines():
        if line:
            data = json.loads(line)
            if data.get("response"):
                yield data["response"]
```

### Modelfile (Custom Models)
```dockerfile
# Custom model configuration
FROM llama2

# Set temperature
PARAMETER temperature 0.7

# Set system message
SYSTEM """
You are a helpful coding assistant specialized in Python.
Always provide clear explanations with code examples.
"""

# Set prompt template
TEMPLATE """
{{ if .System }}System: {{ .System }}{{ end }}
User: {{ .Prompt }}
Assistant: 
"""
```
```bash
# Create custom model
ollama create my-coding-assistant -f ./Modelfile

# Use it
ollama run my-coding-assistant "Write a Python function to sort a list"
```

## Option 2: vLLM (Production Grade)

### Installation
```bash
pip install vllm
```

### Basic Server
```python
# serve.py
from vllm import LLM, SamplingParams

# Initialize model
llm = LLM(model="meta-llama/Llama-2-7b-chat-hf")

# Sampling parameters
sampling_params = SamplingParams(
    temperature=0.7,
    top_p=0.9,
    max_tokens=512,
)

def generate(prompts: list[str]) -> list[str]:
    """Generate completions for multiple prompts."""
    outputs = llm.generate(prompts, sampling_params)
    return [output.outputs[0].text for output in outputs]

# Example
prompts = [
    "Explain quantum computing",
    "Write a Python quicksort",
]
results = generate(prompts)
for prompt, result in zip(prompts, results):
    print(f"Prompt: {prompt}\nResult: {result}\n")
```

### FastAPI Server
```python
from fastapi import FastAPI
from pydantic import BaseModel
from vllm import LLM, SamplingParams
from typing import Optional

app = FastAPI()

# Initialize model (done once on startup)
llm = LLM(
    model="meta-llama/Llama-2-7b-chat-hf",
    tensor_parallel_size=1,  # Number of GPUs
)

class CompletionRequest(BaseModel):
    prompt: str
    temperature: float = 0.7
    max_tokens: int = 512
    top_p: float = 0.9

class CompletionResponse(BaseModel):
    text: str
    tokens: int

@app.post("/v1/completions", response_model=CompletionResponse)
async def create_completion(request: CompletionRequest):
    sampling_params = SamplingParams(
        temperature=request.temperature,
        top_p=request.top_p,
        max_tokens=request.max_tokens,
    )
    
    outputs = llm.generate([request.prompt], sampling_params)
    output = outputs[0].outputs[0]
    
    return CompletionResponse(
        text=output.text,
        tokens=len(output.token_ids),
    )

@app.get("/health")
async def health():
    return {"status": "ok"}
```
```bash
# Run server
uvicorn serve:app --host 0.0.0.0 --port 8000
```

## Option 3: llama.cpp (Lightweight)

### Installation
```bash
# Clone and build
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
make

# Or with CUDA support
make LLAMA_CUBLAS=1
```

### Download Model
```bash
# Download GGUF model from Hugging Face
wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf
```

### Run Server
```bash
./server \
  -m llama-2-7b-chat.Q4_K_M.gguf \
  -c 2048 \
  --host 0.0.0.0 \
  --port 8080
```

### Client Integration
```typescript
async function generateCompletion(prompt: string): Promise<string> {
  const response = await fetch('http://localhost:8080/completion', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      prompt,
      n_predict: 512,
      temperature: 0.7,
      top_p: 0.9,
    }),
  })
  
  const data = await response.json()
  return data.content
}
```

## Docker Deployment

### Ollama Docker
```dockerfile
# docker-compose.yml
version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama-data:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

volumes:
  ollama-data:
```

### vLLM Docker
```dockerfile
FROM nvidia/cuda:12.1.0-base-ubuntu22.04

RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install vllm

COPY serve.py /app/serve.py
WORKDIR /app

EXPOSE 8000

CMD ["python3", "-m", "uvicorn", "serve:app", "--host", "0.0.0.0"]
```

## Model Selection Guide

### Small (< 10GB)
- **Llama 2 7B**: General purpose, good quality
- **Mistral 7B**: Better than Llama 2 7B
- **CodeLlama 7B**: Code generation
- **Phi-2**: Very capable for size

### Medium (10-30GB)
- **Llama 2 13B**: Better reasoning
- **CodeLlama 13B**: Better code
- **Mixtral 8x7B**: Best in class

### Large (> 30GB)
- **Llama 2 70B**: Enterprise grade
- **CodeLlama 70B**: Advanced code

## Performance Optimization

### Quantization
```bash
# GGUF quantization levels (smaller = faster, less accurate)
# Q4_K_M - Recommended balance (4-bit)
# Q5_K_M - Better quality (5-bit)
# Q8_0   - Highest quality (8-bit)

# Example: Use Q4_K_M for production
ollama pull llama2:7b-chat-q4_K_M
```

### GPU Configuration
```python
# vLLM with multiple GPUs
llm = LLM(
    model="meta-llama/Llama-2-70b-chat-hf",
    tensor_parallel_size=4,  # Use 4 GPUs
    dtype="float16",
)
```

### Batch Processing
```python
# Process multiple prompts efficiently
prompts = ["prompt1", "prompt2", "prompt3"]
results = llm.generate(prompts, sampling_params)  # Batched
```

## Monitoring

### Health Check
```python
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "model": MODEL_NAME,
        "gpu_memory": get_gpu_memory(),
    }
```

### Metrics
```python
from prometheus_client import Counter, Histogram

request_count = Counter('llm_requests_total', 'Total requests')
request_duration = Histogram('llm_request_duration_seconds', 'Request duration')

@app.post("/v1/completions")
@request_duration.time()
async def create_completion(request: CompletionRequest):
    request_count.inc()
    # ... implementation
```

## Best Practices

- [ ] Use quantized models (Q4_K_M) for production
- [ ] Implement request queuing for high load
- [ ] Set up health checks and monitoring
- [ ] Cache common prompts
- [ ] Use batch processing when possible
- [ ] Monitor GPU memory usage
- [ ] Implement rate limiting
- [ ] Have model hot-swap capability
- [ ] Log all generations for debugging
- [ ] Test thoroughly before production