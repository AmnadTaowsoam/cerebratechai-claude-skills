---
name: On-Device Model Training
description: Federated learning and on-device training techniques for privacy-preserving AI model updates
---

# On-Device Model Training

## Current Level: Expert (Enterprise Scale)

## Domain: Edge AI & TinyML
## Skill ID: 113

---

## Executive Summary

On-Device Model Training enables training and updating machine learning models directly on edge devices without transferring raw data to the cloud. This approach is essential for privacy-sensitive applications, reduces bandwidth costs, enables personalized models, and provides continuous learning capabilities even in offline environments.

### Strategic Necessity

- **Data Privacy**: Raw data never leaves the device
- **Bandwidth Efficiency**: Only model updates transmitted
- **Personalization**: Models adapt to individual user patterns
- **Offline Learning**: Continuous improvement without connectivity
- **Regulatory Compliance**: Meet GDPR, HIPAA, and other data protection requirements

---

## Technical Deep Dive

### Federated Learning Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Cloud Server                                       │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Federated Learning Coordinator                    │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │   │
│  │  │   Global    │  │   Aggregation│  │   Model      │              │   │
│  │  │   Model     │  │   Strategy   │  │   Versioning │              │   │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │   │
│  └─────────┼─────────────────┼─────────────────┼──────────────────────┘   │
└────────────┼─────────────────┼─────────────────┼──────────────────────────┘
             │                 │                 │
             │  Model Updates  │                 │
             │  (Gradients)    │                 │
             ▼                 ▼                 ▼
┌────────────┼─────────────────┼─────────────────┼──────────────────────────┐
│             │                 │                 │                          │
│  ┌──────────▼───────┐  ┌──────▼───────┐  ┌──────▼───────┐                  │
│  │   Client 1       │  │   Client 2   │  │   Client N   │                  │
│  │   (Mobile)       │  │   (IoT)      │  │   (Edge)     │                  │
│  │                 │  │              │  │              │                  │
│  │  ┌──────────┐   │  │  ┌──────────┐  │  │  ┌──────────┐  │              │
│  │  │   Local   │   │  │  │   Local   │  │  │  │   Local   │  │              │
│  │  │   Data    │   │  │  │   Data    │  │  │  │   Data    │  │              │
│  │  └─────┬────┘   │  │  └─────┬────┘   │  │  └─────┬────┘   │              │
│  │        │         │  │        │         │  │        │         │              │
│  │  ┌─────▼────┐   │  │  ┌─────▼────┐   │  │  ┌─────▼────┐   │              │
│  │  │   Local   │   │  │  │   Local   │   │  │  │   Local   │   │              │
│  │  │   Training│   │  │  │   Training│   │  │  │   Training│   │              │
│  │  └─────┬────┘   │  │  └─────┬────┘   │  │  └─────┬────┘   │              │
│  │        │         │  │        │         │  │        │         │              │
│  │  ┌─────▼────┐   │  │  ┌─────▼────┐   │  │  ┌─────▼────┐   │              │
│  │  │   Model   │   │  │  │   Model   │   │  │  │   Model   │   │              │
│  │  │   Update  │   │  │  │   Update  │   │  │  │   Update  │   │              │
│  │  └──────────┘   │  │  └──────────┘   │  │  └──────────┘   │              │
│  └─────────────────┘  └───────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Federated Learning Protocol

**1. Server Initialization:**
```python
class FederatedLearningServer:
    """Federated learning coordinator"""
    
    def __init__(self, config: Dict[str, Any]):
        self.global_model = self._initialize_model()
        self.aggregation_strategy = config.get('aggregation', 'fedavg')
        self.min_clients = config.get('min_clients', 10)
        self.max_clients = config.get('max_clients', 100)
        self.round_timeout = config.get('round_timeout', 300)
        self.model_version = 1
        
    def _initialize_model(self) -> torch.nn.Module:
        """Initialize global model"""
        model = create_model()
        return model
    
    def start_training_round(self) -> str:
        """Start a new training round"""
        round_id = f"round_{self.model_version}_{int(time.time())}"
        
        # Select clients for this round
        selected_clients = self._select_clients()
        
        # Distribute model to clients
        model_update = self._prepare_model_update()
        
        # Send to clients
        for client_id in selected_clients:
            self._send_model_to_client(client_id, model_update, round_id)
        
        return round_id
    
    def _select_clients(self) -> List[str]:
        """Select clients for training round"""
        available_clients = self._get_available_clients()
        
        # Select based on various criteria
        # - Random sampling
        # - Data quality
        # - Device capabilities
        # - Recent activity
        
        selected = random.sample(
            available_clients,
            min(len(available_clients), self.max_clients)
        )
        
        return selected
    
    def aggregate_updates(self, updates: List[ModelUpdate]) -> torch.nn.Module:
        """Aggregate model updates from clients"""
        if self.aggregation_strategy == 'fedavg':
            return self._federated_averaging(updates)
        elif self.aggregation_strategy == 'fedprox':
            return self._federated_proximal(updates)
        elif self.aggregation_strategy == 'fedadam':
            return self._federated_adam(updates)
        else:
            raise ValueError(f"Unknown aggregation: {self.aggregation_strategy}")
    
    def _federated_averaging(
        self, 
        updates: List[ModelUpdate]
    ) -> torch.nn.Module:
        """Federated Averaging algorithm"""
        # Weight by number of training samples
        total_samples = sum(u.num_samples for u in updates)
        
        # Initialize aggregated model
        aggregated_state = {}
        
        for key in self.global_model.state_dict().keys():
            weighted_sum = torch.zeros_like(
                self.global_model.state_dict()[key]
            )
            
            for update in updates:
                weight = update.num_samples / total_samples
                weighted_sum += weight * update.state_dict[key]
            
            aggregated_state[key] = weighted_sum
        
        # Update global model
        self.global_model.load_state_dict(aggregated_state)
        self.model_version += 1
        
        return self.global_model
```

**2. Client Training:**
```python
class FederatedLearningClient:
    """Federated learning client"""
    
    def __init__(self, config: Dict[str, Any]):
        self.local_model = None
        self.local_data = None
        self.epochs = config.get('epochs', 5)
        self.batch_size = config.get('batch_size', 32)
        self.learning_rate = config.get('learning_rate', 0.01)
        self.privacy_budget = config.get('privacy_budget', 1.0)
        
    def receive_model(self, model_update: ModelUpdate) -> None:
        """Receive global model from server"""
        self.local_model = self._load_model(model_update)
    
    def train_local(self) -> ModelUpdate:
        """Train model on local data"""
        if self.local_model is None or self.local_data is None:
            raise ValueError("Model or data not loaded")
        
        # Create optimizer
        optimizer = torch.optim.SGD(
            self.local_model.parameters(),
            lr=self.learning_rate
        )
        
        # Training loop
        self.local_model.train()
        for epoch in range(self.epochs):
            for batch in self._get_batches():
                optimizer.zero_grad()
                
                # Forward pass
                outputs = self.local_model(batch['input'])
                loss = self._compute_loss(outputs, batch['target'])
                
                # Backward pass
                loss.backward()
                optimizer.step()
        
        # Create model update
        update = ModelUpdate(
            state_dict=self.local_model.state_dict(),
            num_samples=len(self.local_data),
            client_id=self.client_id,
            timestamp=time.time()
        )
        
        return update
    
    def _get_batches(self) -> Iterator[Dict[str, torch.Tensor]]:
        """Get data batches"""
        dataset = self._create_dataset(self.local_data)
        loader = torch.utils.data.DataLoader(
            dataset,
            batch_size=self.batch_size,
            shuffle=True
        )
        return iter(loader)
    
    def apply_differential_privacy(self, gradients: torch.Tensor) -> torch.Tensor:
        """Apply differential privacy to gradients"""
        # Add Gaussian noise
        noise_scale = self._compute_noise_scale()
        noise = torch.randn_like(gradients) * noise_scale
        
        # Clip gradients
        clipped_gradients = self._clip_gradients(gradients)
        
        return clipped_gradients + noise
    
    def _compute_noise_scale(self) -> float:
        """Compute noise scale for DP"""
        # Based on privacy budget and sensitivity
        sigma = np.sqrt(2 * np.log(1.25 / 0.00001)) / self.privacy_budget
        return sigma
    
    def _clip_gradients(self, gradients: torch.Tensor) -> torch.Tensor:
        """Clip gradients to bound sensitivity"""
        max_norm = 1.0
        grad_norm = torch.norm(gradients)
        
        if grad_norm > max_norm:
            gradients = gradients * (max_norm / grad_norm)
        
        return gradients
```

### On-Device Training Pipeline

```python
class OnDeviceTrainer:
    """Complete on-device training pipeline"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model = self._load_model()
        self.data_collector = DataCollector(config['data'])
        self.preprocessor = DataPreprocessor(config['preprocessing'])
        self.trainer = LocalTrainer(config['training'])
        self.privacy_manager = PrivacyManager(config['privacy'])
        
    async def train_on_new_data(self, raw_data: Any) -> TrainingResult:
        """Train model on new data"""
        # Collect and preprocess data
        processed_data = await self._process_data(raw_data)
        
        # Check if enough data for training
        if not self._has_enough_data(processed_data):
            return TrainingResult(status='insufficient_data')
        
        # Train locally
        training_result = await self._train(processed_data)
        
        # Apply privacy protection
        protected_update = self.privacy_manager.protect_update(
            training_result.model_update
        )
        
        # Prepare for upload
        upload_package = self._prepare_upload(protected_update)
        
        return TrainingResult(
            status='success',
            model_update=upload_package,
            metrics=training_result.metrics
        )
    
    async def _process_data(self, raw_data: Any) -> ProcessedData:
        """Process raw data for training"""
        # Collect data
        collected = await self.data_collector.collect(raw_data)
        
        # Preprocess
        processed = await self.preprocessor.process(collected)
        
        # Validate
        validated = self._validate_data(processed)
        
        return validated
    
    async def _train(self, data: ProcessedData) -> LocalTrainingResult:
        """Train model on processed data"""
        # Create dataset
        dataset = self._create_dataset(data)
        
        # Train
        result = await self.trainer.train(self.model, dataset)
        
        # Evaluate
        metrics = self._evaluate_model(self.model, dataset)
        
        return LocalTrainingResult(
            model_update=result.model_update,
            metrics=metrics
        )
    
    def _prepare_upload(self, update: ModelUpdate) -> UploadPackage:
        """Prepare model update for upload"""
        # Compress
        compressed = self._compress_update(update)
        
        # Encrypt
        encrypted = self._encrypt_update(compressed)
        
        # Add metadata
        package = UploadPackage(
            model_update=encrypted,
            metadata={
                'client_id': self.config['client_id'],
                'timestamp': time.time(),
                'data_size': len(update.data),
                'privacy_budget_used': self.privacy_manager.get_budget_used()
            }
        )
        
        return package
```

### Privacy-Preserving Techniques

**1. Differential Privacy:**
```python
class DifferentialPrivacy:
    """Differential privacy for model updates"""
    
    def __init__(self, epsilon: float = 1.0, delta: float = 1e-5):
        self.epsilon = epsilon
        self.delta = delta
        self.sensitivity = 1.0
        
    def add_noise(self, gradients: torch.Tensor) -> torch.Tensor:
        """Add Gaussian mechanism noise"""
        sigma = self._compute_sigma()
        noise = torch.randn_like(gradients) * sigma
        return gradients + noise
    
    def _compute_sigma(self) -> float:
        """Compute noise scale"""
        return np.sqrt(2 * np.log(1.25 / self.delta)) * self.sensitivity / self.epsilon
    
    def clip_gradients(self, gradients: torch.Tensor) -> torch.Tensor:
        """Clip gradients to bound sensitivity"""
        norm = torch.norm(gradients)
        if norm > self.sensitivity:
            gradients = gradients * (self.sensitivity / norm)
        return gradients
```

**2. Secure Aggregation:**
```python
class SecureAggregation:
    """Secure aggregation of model updates"""
    
    def __init__(self, num_clients: int):
        self.num_clients = num_clients
        self.shares_per_client = num_clients - 1
        
    def create_shares(
        self, 
        update: torch.Tensor
    ) -> List[torch.Tensor]:
        """Create secret shares of update"""
        shares = []
        
        for _ in range(self.shares_per_client):
            # Generate random share
            share = torch.randn_like(update)
            shares.append(share)
        
        # Final share is update minus sum of other shares
        final_share = update - sum(shares)
        shares.append(final_share)
        
        return shares
    
    def aggregate_shares(
        self, 
        all_shares: List[List[torch.Tensor]]
    ) -> torch.Tensor:
        """Aggregate shares from all clients"""
        aggregated = torch.zeros_like(all_shares[0][0])
        
        for client_shares in all_shares:
            for share in client_shares:
                aggregated += share
        
        return aggregated / self.num_clients
```

**3. Homomorphic Encryption:**
```python
class HomomorphicEncryption:
    """Homomorphic encryption for model updates"""
    
    def __init__(self, key_size: int = 2048):
        self.key_size = key_size
        self.public_key, self.private_key = self._generate_keys()
        
    def _generate_keys(self):
        """Generate encryption keys"""
        # Using Paillier encryption
        from phe import paillier
        public_key, private_key = paillier.generate_paillier_keypair(
            n_length=self.key_size
        )
        return public_key, private_key
    
    def encrypt_update(self, update: torch.Tensor) -> torch.Tensor:
        """Encrypt model update"""
        encrypted = []
        for value in update.flatten():
            encrypted_value = self.public_key.encrypt(float(value))
            encrypted.append(encrypted_value)
        return torch.tensor(encrypted)
    
    def decrypt_aggregate(
        self, 
        encrypted_aggregate: torch.Tensor
    ) -> torch.Tensor:
        """Decrypt aggregated update"""
        decrypted = []
        for encrypted_value in encrypted_aggregate:
            decrypted_value = self.private_key.decrypt(encrypted_value)
            decrypted.append(decrypted_value)
        return torch.tensor(decrypted)
```

---

## Tooling & Tech Stack

### Core Frameworks
- **TensorFlow Federated**: Federated learning framework
- **PySyft**: Privacy-preserving deep learning
- **Flower**: Federated learning framework
- **OpenMined**: Privacy-focused ML tools

### Privacy Tools
- **PyDP**: Differential privacy
- **Microsoft SEAL**: Homomorphic encryption
- **OpenFHE**: Fully homomorphic encryption
- **TenSEAL**: Encryption for ML

### Development Tools
- **Python 3.9+**: Primary language
- **PyTorch/TensorFlow**: ML frameworks
- **Docker**: Containerization
- **Kubernetes**: Orchestration

### Monitoring
- **TensorBoard**: Training visualization
- **Weights & Biases**: Experiment tracking
- **Prometheus**: Metrics collection
- **Grafana**: Visualization

---

## Configuration Essentials

### Federated Learning Configuration

```yaml
# config/federated_learning.yaml
server:
  host: "0.0.0.0"
  port: 8080
  aggregation_strategy: "fedavg"  # fedavg, fedprox, fedadam
  min_clients: 10
  max_clients: 100
  round_timeout: 300  # seconds
  model_save_interval: 5  # rounds

training:
  epochs: 5
  batch_size: 32
  learning_rate: 0.01
  optimizer: "sgd"
  local_steps: 10

privacy:
  enable_differential_privacy: true
  epsilon: 1.0
  delta: 0.00001
  max_grad_norm: 1.0
  
  enable_secure_aggregation: true
  encryption_scheme: "paillier"  # paillier, bfv, ckks
  
  enable_homomorphic_encryption: false
  key_size: 2048

data:
  min_samples_per_client: 100
  max_samples_per_client: 10000
  data_augmentation: true
  validation_split: 0.1

communication:
  protocol: "grpc"  # grpc, http, mqtt
  compression: "gzip"
  max_message_size: 10485760  # 10MB
  retry_attempts: 3
  retry_delay: 5  # seconds

monitoring:
  enable_metrics: true
  enable_logging: true
  log_level: "INFO"
  metrics_port: 9090
```

### Client Configuration

```yaml
# config/client_config.yaml
client:
  client_id: "${CLIENT_ID}"
  server_url: "https://federated-server.example.com"
  
training:
  epochs: 5
  batch_size: 32
  learning_rate: 0.01
  local_steps: 10
  
privacy:
  enable_differential_privacy: true
  epsilon: 1.0
  delta: 0.00001
  max_grad_norm: 1.0
  
data:
  data_path: "/data/local"
  max_data_size: 10000
  data_retention_days: 30
  
communication:
  upload_interval: 3600  # seconds
  bandwidth_limit: 1048576  # 1MB/s
  offline_support: true
  
monitoring:
  enable_metrics: true
  enable_logging: true
  log_level: "INFO"
```

---

## Code Examples

### Good: Complete Federated Learning Implementation

```python
# server/main.py
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio
import logging
from datetime import datetime

from federated.server import FederatedLearningServer
from federated.models import ModelUpdate, TrainingRound, ClientInfo
from config.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Federated Learning Server",
    description="Privacy-preserving federated learning coordinator",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global server instance
server: Optional[FederatedLearningServer] = None

@app.on_event("startup")
async def startup():
    """Initialize federated learning server"""
    global server
    logger.info("Initializing federated learning server...")
    server = FederatedLearningServer(settings.federated_config)
    await server.start()

@app.on_event("shutdown")
async def shutdown():
    """Shutdown federated learning server"""
    global server
    if server:
        await server.stop()

class ModelUpdateRequest(BaseModel):
    """Model update request from client"""
    client_id: str
    round_id: str
    model_update: Dict[str, Any]
    num_samples: int
    metrics: Dict[str, float]
    privacy_metadata: Optional[Dict[str, Any]] = None

class ModelDownloadResponse(BaseModel):
    """Model download response"""
    model_version: int
    model_data: bytes
    round_id: str
    server_timestamp: float

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "server_status": server is not None,
        "current_round": server.current_round if server else None
    }

@app.get("/model", response_model=ModelDownloadResponse)
async def download_model():
    """Download current global model"""
    if not server:
        raise HTTPException(status_code=503, detail="Server not ready")
    
    model_data = server.get_model_data()
    
    return ModelDownloadResponse(
        model_version=server.model_version,
        model_data=model_data,
        round_id=server.current_round_id,
        server_timestamp=datetime.utcnow().timestamp()
    )

@app.post("/update")
async def submit_update(
    request: ModelUpdateRequest,
    background_tasks: BackgroundTasks
):
    """Submit model update from client"""
    if not server:
        raise HTTPException(status_code=503, detail="Server not ready")
    
    # Validate round ID
    if request.round_id != server.current_round_id:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid round ID. Current: {server.current_round_id}"
        )
    
    # Create model update object
    update = ModelUpdate(
        client_id=request.client_id,
        round_id=request.round_id,
        state_dict=request.model_update,
        num_samples=request.num_samples,
        metrics=request.metrics,
        privacy_metadata=request.privacy_metadata,
        timestamp=datetime.utcnow().timestamp()
    )
    
    # Process update in background
    background_tasks.add_task(server.process_update, update)
    
    return {
        "status": "accepted",
        "message": "Update received and queued for processing"
    }

@app.get("/rounds")
async def get_rounds():
    """Get training round information"""
    if not server:
        raise HTTPException(status_code=503, detail="Server not ready")
    
    return {
        "current_round": server.current_round,
        "current_round_id": server.current_round_id,
        "model_version": server.model_version,
        "clients_participating": server.get_client_count(),
        "updates_received": server.get_update_count(),
        "round_status": server.get_round_status()
    }

@app.get("/metrics")
async def get_metrics():
    """Get federated learning metrics"""
    if not server:
        raise HTTPException(status_code=503, detail="Server not ready")
    
    return server.get_metrics()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
```

```python
# client/main.py
import asyncio
import logging
from typing import Optional
from datetime import datetime

from federated.client import FederatedLearningClient
from federated.privacy import DifferentialPrivacy
from data.collector import DataCollector
from config.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OnDeviceTrainingApp:
    """On-device training application"""
    
    def __init__(self):
        self.client = FederatedLearningClient(settings.client_config)
        self.privacy = DifferentialPrivacy(
            epsilon=settings.privacy_config.epsilon,
            delta=settings.privacy_config.delta
        )
        self.data_collector = DataCollector(settings.data_config)
        self.running = False
        
    async def start(self):
        """Start on-device training"""
        self.running = True
        logger.info("Starting on-device training...")
        
        # Connect to server
        await self.client.connect()
        
        # Main training loop
        while self.running:
            try:
                await self._training_round()
                await asyncio.sleep(settings.training_config.upload_interval)
            except Exception as e:
                logger.error(f"Training round failed: {e}")
                await asyncio.sleep(60)  # Wait before retry
    
    async def _training_round(self):
        """Execute one training round"""
        # Download current model
        logger.info("Downloading current model...")
        model_update = await self.client.download_model()
        
        # Load model
        self.client.receive_model(model_update)
        
        # Collect local data
        logger.info("Collecting local data...")
        local_data = await self.data_collector.collect()
        
        # Check if enough data
        if len(local_data) < settings.data_config.min_samples:
            logger.info("Not enough data for training")
            return
        
        # Train locally
        logger.info("Training locally...")
        training_result = await self.client.train_local(local_data)
        
        # Apply privacy protection
        logger.info("Applying privacy protection...")
        protected_update = self.privacy.protect_update(
            training_result.model_update
        )
        
        # Submit update
        logger.info("Submitting update to server...")
        await self.client.submit_update(protected_update)
        
        logger.info("Training round completed")
    
    async def stop(self):
        """Stop on-device training"""
        self.running = False
        await self.client.disconnect()

async def main():
    """Main entry point"""
    app = OnDeviceTrainingApp()
    
    try:
        await app.start()
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
```

### Bad: Anti-pattern Example

```python
# BAD: No privacy protection
async def bad_training(data):
    # No differential privacy
    model.train(data)
    return model.get_update()

# BAD: Sending raw data
async def bad_data_upload(data):
    # Sends raw data to server
    await server.upload(data)

# BAD: No secure aggregation
async def bad_aggregation(updates):
    # Plain aggregation - vulnerable to attacks
    return sum(updates) / len(updates)

# BAD: No validation
async def bad_model_update(update):
    # No validation of client updates
    server.aggregate(update)

# BAD: No rate limiting
async def bad_client():
    # Can submit unlimited updates
    while True:
        await server.submit_update(get_update())
```

---

## Standards, Compliance & Security

### Industry Standards
- **GDPR**: Data protection and privacy
- **HIPAA**: Healthcare data protection
- **ISO/IEC 27001**: Information security
- **NIST Privacy Framework**: Privacy risk management

### Security Best Practices
- **End-to-End Encryption**: TLS 1.3 for all communications
- **Secure Aggregation**: Prevent server from seeing individual updates
- **Differential Privacy**: Protect individual contributions
- **Client Authentication**: JWT tokens for client identification

### Compliance Requirements
- **Data Minimization**: Only send model updates
- **Consent Management**: Explicit user consent for training
- **Audit Logging**: Track all training activities
- **Model Versioning**: Track model provenance

---

## Quick Start

### 1. Clone and Install

```bash
git clone https://github.com/example/federated-learning.git
cd federated-learning

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Server

```bash
# Copy example config
cp config/server_config.yaml.example config/server_config.yaml

# Edit configuration
vim config/server_config.yaml
```

### 3. Start Server

```bash
# Start federated learning server
python -m server.main

# Or using uvicorn
uvicorn server.main:app --host 0.0.0.0 --port 8080 --reload
```

### 4. Configure Client

```bash
# Copy example config
cp config/client_config.yaml.example config/client_config.yaml

# Edit configuration
vim config/client_config.yaml
```

### 5. Start Client

```bash
# Start federated learning client
python -m client.main
```

### 6. Monitor Training

```bash
# Check server status
curl http://localhost:8080/health

# Get training metrics
curl http://localhost:8080/metrics

# View training rounds
curl http://localhost:8080/rounds
```

---

## Production Checklist

### Deployment
- [ ] Server deployed to production
- [ ] Client distribution configured
- [ ] Load balancing configured
- [ ] Auto-scaling enabled
- [ ] Backup and recovery in place

### Security
- [ ] TLS encryption enabled
- [ ] Client authentication configured
- [ ] Rate limiting enabled
- [ ] Input validation implemented
- [ ] Security audit completed

### Privacy
- [ ] Differential privacy enabled
- [ ] Secure aggregation configured
- [ ] Data minimization enforced
- [ ] Consent management implemented
- [ ] Privacy impact assessment completed

### Monitoring
- [ ] Metrics collection enabled
- [ ] Logging configured
- [ ] Alerting set up
- [ ] Dashboard configured
- [ ] Performance monitoring active

### Compliance
- [ ] GDPR compliance verified
- [ ] HIPAA compliance verified (if applicable)
- [ ] Audit logging enabled
- [ ] Data retention policies configured
- [ ] Legal review completed

---

## Anti-patterns

### ❌ Avoid These Practices

1. **No Privacy Protection**
   ```python
   # BAD: Sends raw gradients
   server.send_update(model.gradients)
   ```

2. **Sending Raw Data**
   ```python
   # BAD: Sends raw user data
   server.upload(user_data)
   ```

3. **No Secure Aggregation**
   ```python
   # BAD: Plain aggregation
   aggregated = sum(updates) / len(updates)
   ```

4. **No Validation**
   ```python
   # BAD: No client validation
   server.aggregate(client_update)
   ```

5. **No Rate Limiting**
   ```python
   # BAD: Unlimited submissions
   while True:
       server.submit_update(update)
   ```

### ✅ Follow These Practices

1. **Differential Privacy**
   ```python
   # GOOD: Adds noise to updates
   noisy_update = dp.add_noise(update)
   server.send_update(noisy_update)
   ```

2. **Send Only Updates**
   ```python
   # GOOD: Only sends model updates
   server.send_update(model.get_update())
   ```

3. **Secure Aggregation**
   ```python
   # GOOD: Secure aggregation
   aggregated = secure_agg.aggregate(updates)
   ```

4. **Validate Updates**
   ```python
   # GOOD: Validates client updates
   if validate_update(update):
       server.aggregate(update)
   ```

5. **Rate Limiting**
   ```python
   # GOOD: Rate limited submissions
   if can_submit_update(client_id):
       server.submit_update(update)
   ```

---

## Unit Economics & KPIs

### Development Costs
- **Initial Development**: 200-300 hours
- **Privacy Implementation**: 80-120 hours
- **Testing & Validation**: 100-150 hours
- **Total**: 380-570 hours

### Operational Costs
- **Server Infrastructure**: $500-2000/month
- **Bandwidth**: $100-500/month
- **Monitoring**: $100-300/month
- **Support**: 20-40 hours/month

### ROI Metrics
- **Bandwidth Savings**: 95-99% vs data upload
- **Privacy Compliance**: Meets GDPR/HIPAA requirements
- **Model Accuracy**: 90-95% of centralized training
- **User Trust**: Increased trust and adoption

### KPI Targets
- **Client Participation**: > 70% of active clients
- **Round Completion Time**: < 5 minutes
- **Model Convergence**: 10-20 rounds
- **Privacy Budget**: < 5% epsilon per round
- **Update Success Rate**: > 95%

---

## Integration Points / Related Skills

### Upstream Skills
- **91. Feature Store Implementation**: Feature extraction
- **92. Drift Detection and Retraining**: Model drift monitoring
- **93. Model Registry and Versioning**: Model lifecycle

### Parallel Skills
- **111. TinyML Microcontroller AI**: Edge inference
- **112. Hybrid Inference Architecture**: Cloud-edge coordination
- **114. Edge Model Compression**: Model optimization
- **115. Edge AI Development Workflow**: End-to-end pipeline

### Downstream Skills
- **101. High Performance Inference**: Inference optimization
- **102. Model Optimization and Quantization**: Model compression
- **103. Serverless Inference**: Cloud fallback
- **116. Agentic AI Frameworks**: Agent-based learning

### Cross-Domain Skills
- **76. Hardware Rooted Identity**: Device authentication
- **77. mTLS PKI Management**: Secure communication
- **78. Micro Segmentation Policy**: Network security
- **84. Compliance AI Governance**: Regulatory compliance

---

## References & Resources

### Documentation
- [TensorFlow Federated](https://www.tensorflow.org/federated)
- [PySyft](https://github.com/OpenMined/PySyft)
- [Flower](https://flower.dev/)
- [OpenMined](https://www.openmined.org/)

### Privacy Tools
- [PyDP](https://github.com/OpenMined/PyDP)
- [Microsoft SEAL](https://github.com/microsoft/SEAL)
- [OpenFHE](https://github.com/openfheorg/openfhe-development)
- [TenSEAL](https://github.com/OpenMined/TenSEAL)

### Papers & Research
- [Communication-Efficient Learning](https://arxiv.org/abs/1602.05629)
- [Federated Averaging](https://arxiv.org/abs/1602.05629)
- [Differential Privacy](https://arxiv.org/abs/1602.05629)
- [Secure Aggregation](https://arxiv.org/abs/1706.03986)
