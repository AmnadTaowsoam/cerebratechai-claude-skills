---
name: ML Model Serving
description: Deploying ML models for predictions through REST APIs, batch prediction, model optimization, deployment strategies, and serving infrastructure for production ML systems.
---

# ML Model Serving

> **Current Level:** Advanced  
> **Domain:** Data Science / ML / DevOps

---

## Overview

Model serving deploys ML models for predictions. This guide covers REST APIs, batch prediction, optimization, and deployment strategies for building production ML systems that serve predictions reliably and efficiently.

## Model Serving Patterns

```
Client → API Gateway → Model Server → Model → Prediction
```

**Patterns:**
- **REST API** - Synchronous requests
- **Batch** - Process large datasets
- **Streaming** - Real-time data streams
- **Edge** - On-device inference

## REST API Serving

### FastAPI

```python
# FastAPI model serving
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np

# Load model
model = joblib.load('model.pkl')

app = FastAPI(title="ML Model API")

class PredictionRequest(BaseModel):
    features: list[float]

class PredictionResponse(BaseModel):
    prediction: float
    probability: float = None

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Make prediction"""
    try:
        # Prepare input
        X = np.array(request.features).reshape(1, -1)
        
        # Predict
        prediction = model.predict(X)[0]
        
        # Get probability if available
        probability = None
        if hasattr(model, 'predict_proba'):
            probability = float(model.predict_proba(X)[0].max())
        
        return PredictionResponse(
            prediction=float(prediction),
            probability=probability
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy"}

@app.get("/model/info")
async def model_info():
    """Model information"""
    return {
        "model_type": type(model).__name__,
        "features": model.n_features_in_ if hasattr(model, 'n_features_in_') else None
    }

# Run: uvicorn main:app --reload
```

### Flask

```python
# Flask model serving
from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)
model = joblib.load('model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    """Make prediction"""
    try:
        data = request.get_json()
        features = np.array(data['features']).reshape(1, -1)
        
        prediction = model.predict(features)[0]
        
        return jsonify({
            'prediction': float(prediction)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

## TorchServe

```python
# TorchServe handler
import torch
import json

class ModelHandler:
    def __init__(self):
        self.model = None
        self.initialized = False
    
    def initialize(self, context):
        """Initialize model"""
        properties = context.system_properties
        model_dir = properties.get("model_dir")
        
        # Load model
        self.model = torch.jit.load(f"{model_dir}/model.pt")
        self.model.eval()
        
        self.initialized = True
    
    def preprocess(self, data):
        """Preprocess input"""
        input_data = data[0].get("data") or data[0].get("body")
        
        if isinstance(input_data, (bytes, bytearray)):
            input_data = input_data.decode('utf-8')
        
        input_dict = json.loads(input_data)
        
        # Convert to tensor
        tensor = torch.FloatTensor(input_dict['features'])
        
        return tensor
    
    def inference(self, data):
        """Run inference"""
        with torch.no_grad():
            output = self.model(data)
        
        return output
    
    def postprocess(self, data):
        """Postprocess output"""
        return [data.tolist()]

# Package model
# torch-model-archiver --model-name my_model --version 1.0 --serialized-file model.pt --handler handler.py
# torchserve --start --model-store model_store --models my_model=my_model.mar
```

## TensorFlow Serving

```python
# Prepare model for TF Serving
import tensorflow as tf

# Save model in SavedModel format
model.save('saved_model/1')

# Start TF Serving
# docker run -p 8501:8501 --mount type=bind,source=/path/to/saved_model,target=/models/my_model -e MODEL_NAME=my_model -t tensorflow/serving

# Client code
import requests
import json

def predict(features):
    """Make prediction via TF Serving"""
    url = 'http://localhost:8501/v1/models/my_model:predict'
    
    data = json.dumps({
        "signature_name": "serving_default",
        "instances": [features]
    })
    
    response = requests.post(url, data=data)
    predictions = response.json()['predictions']
    
    return predictions[0]
```

## Batch Prediction

```python
# Batch prediction pipeline
import pandas as pd
import joblib
from typing import List

class BatchPredictor:
    def __init__(self, model_path: str, batch_size: int = 1000):
        self.model = joblib.load(model_path)
        self.batch_size = batch_size
    
    def predict_csv(self, input_path: str, output_path: str):
        """Predict on CSV file"""
        # Read in chunks
        chunks = pd.read_csv(input_path, chunksize=self.batch_size)
        
        results = []
        
        for chunk in chunks:
            # Prepare features
            X = chunk.drop('id', axis=1).values
            
            # Predict
            predictions = self.model.predict(X)
            
            # Add predictions
            chunk['prediction'] = predictions
            results.append(chunk)
        
        # Combine and save
        pd.concat(results).to_csv(output_path, index=False)
    
    def predict_batch(self, features: List[List[float]]) -> List[float]:
        """Predict on batch"""
        import numpy as np
        
        X = np.array(features)
        predictions = self.model.predict(X)
        
        return predictions.tolist()

# Usage
predictor = BatchPredictor('model.pkl', batch_size=1000)
predictor.predict_csv('input.csv', 'output.csv')
```

## Model Optimization

```python
# Model optimization techniques

# 1. Quantization (PyTorch)
import torch

model = torch.load('model.pth')
model.eval()

# Dynamic quantization
quantized_model = torch.quantization.quantize_dynamic(
    model,
    {torch.nn.Linear},
    dtype=torch.qint8
)

# 2. ONNX conversion
import torch.onnx

dummy_input = torch.randn(1, 10)
torch.onnx.export(
    model,
    dummy_input,
    "model.onnx",
    export_params=True,
    opset_version=11,
    input_names=['input'],
    output_names=['output']
)

# 3. TensorRT optimization
import tensorrt as trt

# Convert ONNX to TensorRT
logger = trt.Logger(trt.Logger.WARNING)
builder = trt.Builder(logger)
network = builder.create_network()
parser = trt.OnnxParser(network, logger)

with open('model.onnx', 'rb') as model:
    parser.parse(model.read())

# Build engine
config = builder.create_builder_config()
config.max_workspace_size = 1 << 30  # 1GB

engine = builder.build_engine(network, config)
```

## Caching Strategies

```python
# Caching predictions
from functools import lru_cache
import hashlib
import json
import redis

# In-memory cache
@lru_cache(maxsize=1000)
def predict_cached(features_tuple):
    """Cached prediction"""
    features = list(features_tuple)
    return model.predict([features])[0]

# Redis cache
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def predict_with_redis_cache(features):
    """Prediction with Redis cache"""
    # Create cache key
    key = hashlib.md5(json.dumps(features).encode()).hexdigest()
    
    # Check cache
    cached = redis_client.get(key)
    if cached:
        return json.loads(cached)
    
    # Predict
    prediction = model.predict([features])[0]
    
    # Cache result (expire in 1 hour)
    redis_client.setex(key, 3600, json.dumps(float(prediction)))
    
    return prediction
```

## A/B Testing Models

```python
# A/B testing multiple models
import random

class ModelABTester:
    def __init__(self, model_a, model_b, traffic_split=0.5):
        self.model_a = model_a
        self.model_b = model_b
        self.traffic_split = traffic_split
    
    def predict(self, features, user_id=None):
        """Predict with A/B testing"""
        # Determine which model to use
        if user_id:
            # Consistent assignment based on user_id
            use_model_a = hash(user_id) % 100 < (self.traffic_split * 100)
        else:
            # Random assignment
            use_model_a = random.random() < self.traffic_split
        
        model = self.model_a if use_model_a else self.model_b
        model_version = 'A' if use_model_a else 'B'
        
        prediction = model.predict([features])[0]
        
        # Log for analysis
        self.log_prediction(user_id, model_version, features, prediction)
        
        return {
            'prediction': prediction,
            'model_version': model_version
        }
    
    def log_prediction(self, user_id, model_version, features, prediction):
        """Log prediction for analysis"""
        # Log to database or analytics platform
        pass
```

## Shadow Testing

```python
# Shadow testing (compare models without affecting users)
class ShadowTester:
    def __init__(self, primary_model, shadow_model):
        self.primary_model = primary_model
        self.shadow_model = shadow_model
    
    def predict(self, features):
        """Predict with shadow testing"""
        # Primary prediction (returned to user)
        primary_pred = self.primary_model.predict([features])[0]
        
        # Shadow prediction (logged but not returned)
        try:
            shadow_pred = self.shadow_model.predict([features])[0]
            
            # Log comparison
            self.log_comparison(features, primary_pred, shadow_pred)
        except Exception as e:
            # Don't fail if shadow model errors
            print(f"Shadow model error: {e}")
        
        return primary_pred
    
    def log_comparison(self, features, primary_pred, shadow_pred):
        """Log predictions for comparison"""
        # Log to database for analysis
        pass
```

## Docker Deployment

```dockerfile
# Dockerfile for model serving
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy model and code
COPY model.pkl .
COPY app.py .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Build and run
docker build -t ml-model-api .
docker run -p 8000:8000 ml-model-api
```

## Kubernetes Deployment

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-model-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ml-model
  template:
    metadata:
      labels:
        app: ml-model
    spec:
      containers:
      - name: ml-model
        image: ml-model-api:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: ml-model-service
spec:
  selector:
    app: ml-model
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

## Best Practices

1. **Versioning** - Version models and APIs
2. **Monitoring** - Monitor latency and errors
3. **Caching** - Cache frequent predictions
4. **Batching** - Batch requests when possible
5. **Optimization** - Optimize model size/speed
6. **Health Checks** - Implement health endpoints
7. **Logging** - Log predictions for debugging
8. **A/B Testing** - Test new models safely
9. **Scaling** - Auto-scale based on load
10. **Security** - Secure API endpoints

---

## Quick Start

### FastAPI Model Serving

```python
from fastapi import FastAPI
import torch

app = FastAPI()
model = torch.load('model.pth')
model.eval()

@app.post('/predict')
async def predict(data: PredictionRequest):
    # Preprocess
    input_tensor = preprocess(data.features)
    
    # Predict
    with torch.no_grad():
        prediction = model(input_tensor)
    
    # Postprocess
    result = postprocess(prediction)
    
    return {'prediction': result}
```

### Batch Prediction

```python
async def batch_predict(data: List[PredictionRequest]):
    # Batch processing
    inputs = [preprocess(d.features) for d in data]
    batch = torch.stack(inputs)
    
    with torch.no_grad():
        predictions = model(batch)
    
    return [postprocess(p) for p in predictions]
```

---

## Production Checklist

- [ ] **API**: REST API for predictions
- [ ] **Batch Processing**: Batch prediction support
- [ ] **Model Loading**: Efficient model loading
- [ ] **Caching**: Cache predictions if appropriate
- [ ] **Monitoring**: Monitor prediction performance
- [ ] **Health Checks**: Health endpoints
- [ ] **Logging**: Log predictions for debugging
- [ ] **A/B Testing**: Test new models safely
- [ ] **Scaling**: Auto-scale based on load
- [ ] **Security**: Secure API endpoints
- [ ] **Documentation**: Document API
- [ ] **Testing**: Test model serving

---

## Anti-patterns

### ❌ Don't: Load Model Every Request

```python
# ❌ Bad - Load on every request
@app.post('/predict')
async def predict(data):
    model = torch.load('model.pth')  # Slow!
    return model(data)
```

```python
# ✅ Good - Load once
model = torch.load('model.pth')  # Load at startup

@app.post('/predict')
async def predict(data):
    return model(data)  # Fast!
```

### ❌ Don't: No Error Handling

```python
# ❌ Bad - No error handling
@app.post('/predict')
async def predict(data):
    return model(data)  # What if model fails?
```

```python
# ✅ Good - Error handling
@app.post('/predict')
async def predict(data):
    try:
        return model(data)
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed")
```

---

## Integration Points

- **Model Training** (`05-ai-ml-core/model-training/`) - Model development
- **Model Optimization** (`05-ai-ml-core/model-optimization/`) - Model optimization
- **API Design** (`01-foundations/api-design/`) - API patterns

---

## Further Reading

- [FastAPI](https://fastapi.tiangolo.com/)
- [TorchServe](https://pytorch.org/serve/)
- [ML Model Serving Best Practices](https://www.tensorflow.org/tfx/guide/serving)

## Resources
- [TensorFlow Serving](https://www.tensorflow.org/tfx/guide/serving)
- [BentoML](https://www.bentoml.com/)
- [Seldon Core](https://www.seldon.io/)
