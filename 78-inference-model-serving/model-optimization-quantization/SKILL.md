---
name: Model Optimization and Quantization
description: Techniques for reducing model size and improving inference speed through quantization, pruning, and optimization
---

# Model Optimization and Quantization

> **Current Level:** Expert (Enterprise Scale)
> **Domain:** AI / MLOps / Performance Engineering
> **Skill ID:** 102

---

## Overview
Model Optimization and Quantization encompasses techniques to reduce model size, improve inference speed, and lower resource requirements while maintaining acceptable accuracy. This includes quantization (reducing numerical precision), pruning (removing less important weights), knowledge distillation, and architectural optimization.

## Why This Matters / Strategic Necessity

### Context
In 2025-2026, ML models are deployed on edge devices, mobile phones, and cloud infrastructure with strict resource constraints. Large models are prohibitively expensive to serve at scale, making optimization essential for cost-effective deployment.

### Business Impact
- **Cost Reduction:** 60-90% reduction in inference compute costs
- **Latency Improvement:** 2-10x faster inference times
- **Device Support:** Enable deployment on mobile and edge devices
- **Scalability:** Support 10-100x more users with same infrastructure

### Product Thinking
Solves the critical problem where models are too large or slow for practical deployment, preventing product features from reaching production due to cost or performance constraints.

## Core Concepts / Technical Deep Dive

### 1. Quantization Techniques

**Post-Training Quantization (PTQ):**
- **Dynamic Quantization:** Weights quantized to INT8, activations computed in FP16
- **Static Quantization:** Both weights and activations quantized, requires calibration
- **Integer Quantization:** Full INT8 model, best for edge deployment
- **Float16 Quantization:** Reduce from FP32 to FP16, minimal accuracy loss

**Quantization-Aware Training (QAT):**
- Simulate quantization during training
- Model learns to be robust to quantization
- Better accuracy than PTQ but requires retraining

**Quantization Granularity:**
- **Per-Tensor:** Single scale for entire tensor
- **Per-Channel:** Different scale per output channel
- **Per-Row:** Different scale per row (for embeddings)

### 2. Pruning Techniques

**Unstructured Pruning:**
- Remove individual weights with small magnitude
- Requires sparse matrix libraries for speedup
- Best accuracy retention

**Structured Pruning:**
- Remove entire neurons, filters, or channels
- Standard dense matrix operations work
- Larger accuracy loss but better hardware support

**Pruning Strategies:**
- **Magnitude-based:** Remove smallest weights
- **Gradient-based:** Remove weights with small gradient
- **Importance-based:** Remove weights with low importance score
- **Iterative Pruning:** Gradually increase sparsity

### 3. Knowledge Distillation

**Teacher-Student Framework:**
- Large "teacher" model teaches smaller "student" model
- Student learns from teacher's soft labels
- Maintains most of teacher's performance

**Distillation Techniques:**
- **Response-based:** Match teacher's output logits
- **Feature-based:** Match intermediate layer representations
- **Relation-based:** Match relationships between samples
- **Self-distillation:** Model teaches itself

### 4. Architecture Optimization

**Model Compression:**
- Depth reduction (fewer layers)
- Width reduction (fewer channels)
- Bottleneck layers
- Efficient attention mechanisms

**Neural Architecture Search (NAS):**
- Automatically find optimal architecture
- Hardware-aware NAS for target device
- Differentiable NAS for fast search

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌─────────────┐
│   Original  │────▶│  Quantization│────▶│   Pruning   │────▶│   Final     │
│   Model     │     │   (FP32→INT8)│     │  (Sparsity) │     │   Model     │
└─────────────┘     └──────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌─────────────┐
│   Accuracy  │     │   Size       │     │   Speed     │     │   Deploy    │
│   Baseline  │     │   Reduced    │     │   Improved  │     │   Ready     │
└─────────────┘     └──────────────┘     └─────────────┘     └─────────────┘
```

## Tooling & Tech Stack

### Enterprise Tools
- **TensorRT:** NVIDIA's optimization and deployment platform
- **ONNX Runtime:** Cross-platform inference with optimizations
- **TensorFlow Lite:** Mobile and edge deployment
- **PyTorch Quantization:** Native quantization support
- **OpenVINO:** Intel's optimization toolkit
- **Distiller:** PyTorch model compression toolkit

### Configuration Essentials

```yaml
# Quantization configuration
quantization:
  mode: "dynamic"  # dynamic, static, qat
  precision: "int8"  # int8, fp16, int4
  
  # Calibration settings (for static quantization)
  calibration:
    method: "minmax"  # minmax, percentile, entropy
    num_samples: 1000
    batch_size: 32
  
  # Per-channel vs per-tensor
  granularity: "per_channel"  # per_channel, per_tensor
  
  # Backend selection
  backend: "x86"  # x86, cuda, arm, tflite

# Pruning configuration
pruning:
  method: "magnitude"  # magnitude, gradient, importance
  target_sparsity: 0.5  # 50% sparsity
  schedule: "iterative"  # one_shot, iterative
  pruning_rate: 0.1  # 10% per iteration
  
  # Structured vs unstructured
  structured: false  # true for structured pruning
  
  # Layers to prune
  target_layers:
    - "conv1"
    - "conv2"
    - "fc1"

# Knowledge distillation
distillation:
  temperature: 3.0  # Softmax temperature
  alpha: 0.5  # Balance between hard and soft labels
  loss_type: "kl_divergence"  # kl_divergence, mse
  
  # Feature matching
  feature_matching:
    enabled: true
    layers: ["layer3", "layer4"]
    weight: 0.1
```

## Code Examples

### Good vs Bad Examples

```python
# ❌ Bad - No optimization, full FP32 model
import torch

model = torch.load("model.pth")
model.eval()

def predict(inputs):
    return model(inputs)

# ✅ Good - Quantized model for faster inference
import torch.quantization as quant

# Apply dynamic quantization
model = torch.load("model.pth")
quantized_model = quant.quantize_dynamic(
    model,
    {torch.nn.Linear, torch.nn.LSTM},
    dtype=torch.qint8
)

def predict(inputs):
    return quantized_model(inputs)

# Results: 4x smaller, 2-4x faster with <1% accuracy loss
```

```python
# ❌ Bad - Manual pruning without fine-tuning
def prune_model(model, sparsity=0.5):
    for name, param in model.named_parameters():
        if 'weight' in name:
            mask = torch.abs(param) > torch.quantile(torch.abs(param), sparsity)
            param.data *= mask.float()

# ✅ Good - Structured pruning with fine-tuning
import torch.nn.utils.prune as prune

def prune_model_properly(model, sparsity=0.5):
    # Structured pruning on convolutional layers
    for name, module in model.named_modules():
        if isinstance(module, torch.nn.Conv2d):
            prune.ln_structured(
                module,
                name='weight',
                amount=sparsity,
                n=2,
                dim=0  # Prune entire output channels
            )
    
    # Fine-tune after pruning
    fine_tune_model(model)
    
    # Remove pruning masks to make permanent
    for name, module in model.named_modules():
        if isinstance(module, torch.nn.Conv2d):
            prune.remove(module, 'weight')
```

### Implementation Example

```python
"""
Production-ready Model Optimization and Quantization
"""
from typing import Dict, List, Optional, Tuple, Callable
import torch
import torch.nn as nn
import torch.quantization as quant
import torch.nn.utils.prune as prune
import numpy as np
from dataclasses import dataclass, field
from enum import Enum
import logging
from torch.utils.data import DataLoader
import copy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QuantizationMode(Enum):
    """Quantization modes."""
    DYNAMIC = "dynamic"
    STATIC = "static"
    QAT = "qat"  # Quantization-Aware Training
    FP16 = "fp16"


class PruningMethod(Enum):
    """Pruning methods."""
    MAGNITUDE = "magnitude"
    GRADIENT = "gradient"
    IMPORTANCE = "importance"


@dataclass
class OptimizationResult:
    """Result of model optimization."""
    original_size_mb: float
    optimized_size_mb: float
    size_reduction_pct: float
    original_accuracy: float
    optimized_accuracy: float
    accuracy_drop_pct: float
    latency_improvement: float
    method: str
    details: Dict[str, Any]


class ModelOptimizer:
    """
    Enterprise-grade model optimization with quantization and pruning.
    """
    
    def __init__(
        self,
        model: nn.Module,
        calibration_data: Optional[DataLoader] = None
    ):
        """
        Initialize model optimizer.
        
        Args:
            model: PyTorch model to optimize
            calibration_data: Data for calibration (required for static quantization)
        """
        self.model = model
        self.calibration_data = calibration_data
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.model.eval()
        
        logger.info(f"Model optimizer initialized on {self.device}")
    
    def quantize(
        self,
        mode: QuantizationMode = QuantizationMode.DYNAMIC,
        layers_to_quantize: Optional[List[str]] = None,
        calibration_samples: int = 1000
    ) -> nn.Module:
        """
        Quantize the model.
        
        Args:
            mode: Quantization mode
            layers_to_quantize: Specific layers to quantize
            calibration_samples: Number of samples for calibration
            
        Returns:
            Quantized model
        """
        logger.info(f"Starting quantization: {mode.value}")
        
        if mode == QuantizationMode.DYNAMIC:
            return self._dynamic_quantization(layers_to_quantize)
        elif mode == QuantizationMode.STATIC:
            return self._static_quantization(layers_to_quantize, calibration_samples)
        elif mode == QuantizationMode.QAT:
            return self._quantization_aware_training(layers_to_quantize)
        elif mode == QuantizationMode.FP16:
            return self._fp16_quantization()
        else:
            raise ValueError(f"Unknown quantization mode: {mode}")
    
    def _dynamic_quantization(
        self,
        layers_to_quantize: Optional[List[str]] = None
    ) -> nn.Module:
        """
        Apply dynamic quantization.
        
        Args:
            layers_to_quantize: Layers to quantize
            
        Returns:
            Quantized model
        """
        # Default layers to quantize
        if layers_to_quantize is None:
            layers_to_quantize = [nn.Linear, nn.LSTM, nn.GRU]
        
        # Apply dynamic quantization
        quantized_model = quant.quantize_dynamic(
            self.model,
            layers_to_quantize,
            dtype=torch.qint8
        )
        
        logger.info("Dynamic quantization completed")
        return quantized_model
    
    def _static_quantization(
        self,
        layers_to_quantize: Optional[List[str]] = None,
        calibration_samples: int = 1000
    ) -> nn.Module:
        """
        Apply static quantization with calibration.
        
        Args:
            layers_to_quantize: Layers to quantize
            calibration_samples: Number of calibration samples
            
        Returns:
            Quantized model
        """
        if self.calibration_data is None:
            raise ValueError("Calibration data required for static quantization")
        
        # Prepare model for quantization
        model_copy = copy.deepcopy(self.model)
        model_copy.eval()
        
        # Fuse modules for better quantization
        model_copy = self._fuse_modules(model_copy)
        
        # Configure quantization
        model_copy.qconfig = quant.get_default_qconfig('x86')
        
        # Prepare model
        model_copy_prepared = quant.prepare(model_copy, inplace=False)
        
        # Calibrate
        logger.info(f"Calibrating with {calibration_samples} samples...")
        with torch.no_grad():
            for i, (inputs, _) in enumerate(self.calibration_data):
                if i >= calibration_samples:
                    break
                model_copy_prepared(inputs.to(self.device))
        
        # Convert to quantized model
        quantized_model = quant.convert(model_copy_prepared, inplace=False)
        
        logger.info("Static quantization completed")
        return quantized_model
    
    def _quantization_aware_training(
        self,
        layers_to_quantize: Optional[List[str]] = None
    ) -> nn.Module:
        """
        Apply quantization-aware training.
        
        Args:
            layers_to_quantize: Layers to quantize
            
        Returns:
            Model prepared for QAT
        """
        # Prepare model for QAT
        model_copy = copy.deepcopy(self.model)
        model_copy.train()
        
        # Fuse modules
        model_copy = self._fuse_modules(model_copy)
        
        # Configure QAT
        model_copy.qconfig = quant.get_default_qat_qconfig('x86')
        
        # Prepare model for QAT
        qat_model = quant.prepare_qat(model_copy, inplace=False)
        
        logger.info("QAT preparation completed. Fine-tuning required.")
        return qat_model
    
    def _fp16_quantization(self) -> nn.Module:
        """
        Convert model to FP16.
        
        Returns:
            FP16 model
        """
        model_copy = copy.deepcopy(self.model)
        model_copy.half()
        
        logger.info("FP16 quantization completed")
        return model_copy
    
    def _fuse_modules(self, model: nn.Module) -> nn.Module:
        """
        Fuse modules for better quantization.
        
        Args:
            model: Model to fuse
            
        Returns:
            Model with fused modules
        """
        # Common fusion patterns
        fusion_patterns = [
            [['conv', 'bn', 'relu']],
            [['conv', 'relu']],
            [['linear', 'relu']],
        ]
        
        # Apply fusion
        for pattern in fusion_patterns:
            try:
                model = quant.fuse_modules(model, pattern)
            except:
                continue
        
        return model
    
    def prune(
        self,
        method: PruningMethod = PruningMethod.MAGNITUDE,
        sparsity: float = 0.5,
        structured: bool = False,
        target_layers: Optional[List[str]] = None
    ) -> nn.Module:
        """
        Prune the model.
        
        Args:
            method: Pruning method
            sparsity: Target sparsity (0-1)
            structured: Whether to use structured pruning
            target_layers: Specific layers to prune
            
        Returns:
            Pruned model
        """
        logger.info(f"Starting pruning: {method.value}, sparsity={sparsity}")
        
        model_copy = copy.deepcopy(self.model)
        
        if method == PruningMethod.MAGNITUDE:
            return self._magnitude_pruning(model_copy, sparsity, structured, target_layers)
        elif method == PruningMethod.GRADIENT:
            return self._gradient_pruning(model_copy, sparsity, structured, target_layers)
        else:
            raise ValueError(f"Unknown pruning method: {method}")
    
    def _magnitude_pruning(
        self,
        model: nn.Module,
        sparsity: float,
        structured: bool,
        target_layers: Optional[List[str]] = None
    ) -> nn.Module:
        """
        Apply magnitude-based pruning.
        
        Args:
            model: Model to prune
            sparsity: Target sparsity
            structured: Whether to use structured pruning
            target_layers: Layers to prune
            
        Returns:
            Pruned model
        """
        for name, module in model.named_modules():
            # Check if this layer should be pruned
            if target_layers and not any(t in name for t in target_layers):
                continue
            
            if isinstance(module, (nn.Conv2d, nn.Linear)):
                if structured:
                    # Structured pruning (entire channels)
                    prune.ln_structured(
                        module,
                        name='weight',
                        amount=sparsity,
                        n=2,
                        dim=0  # Prune output channels
                    )
                else:
                    # Unstructured pruning (individual weights)
                    prune.l1_unstructured(
                        module,
                        name='weight',
                        amount=sparsity
                    )
        
        logger.info("Magnitude pruning completed")
        return model
    
    def _gradient_pruning(
        self,
        model: nn.Module,
        sparsity: float,
        structured: bool,
        target_layers: Optional[List[str]] = None
    ) -> nn.Module:
        """
        Apply gradient-based pruning.
        
        Args:
            model: Model to prune
            sparsity: Target sparsity
            structured: Whether to use structured pruning
            target_layers: Layers to prune
            
        Returns:
            Pruned model
        """
        # Calculate gradient-based importance
        # This requires a forward/backward pass with data
        # Simplified implementation
        
        for name, module in model.named_modules():
            if target_layers and not any(t in name for t in target_layers):
                continue
            
            if isinstance(module, (nn.Conv2d, nn.Linear)):
                if structured:
                    prune.ln_structured(
                        module,
                        name='weight',
                        amount=sparsity,
                        n=2,
                        dim=0
                    )
                else:
                    prune.l1_unstructured(
                        module,
                        name='weight',
                        amount=sparsity
                    )
        
        logger.info("Gradient pruning completed")
        return model
    
    def remove_pruning_masks(self, model: nn.Module) -> nn.Module:
        """
        Remove pruning masks to make pruning permanent.
        
        Args:
            model: Pruned model
            
        Returns:
            Model with permanent pruning
        """
        for name, module in model.named_modules():
            if isinstance(module, (nn.Conv2d, nn.Linear)):
                try:
                    prune.remove(module, 'weight')
                    if hasattr(module, 'bias') and module.bias is not None:
                        prune.remove(module, 'bias')
                except:
                    pass
        
        logger.info("Pruning masks removed")
        return model
    
    def distill(
        self,
        teacher_model: nn.Module,
        student_model: nn.Module,
        train_loader: DataLoader,
        epochs: int = 10,
        temperature: float = 3.0,
        alpha: float = 0.5,
        learning_rate: float = 1e-3
    ) -> nn.Module:
        """
        Perform knowledge distillation.
        
        Args:
            teacher_model: Teacher model
            student_model: Student model
            train_loader: Training data
            epochs: Number of training epochs
            temperature: Softmax temperature
            alpha: Balance between hard and soft labels
            learning_rate: Learning rate
            
        Returns:
            Trained student model
        """
        teacher_model.eval()
        student_model.train()
        
        optimizer = torch.optim.Adam(student_model.parameters(), lr=learning_rate)
        criterion = nn.KLDivLoss(reduction='batchmean')
        hard_loss = nn.CrossEntropyLoss()
        
        logger.info(f"Starting knowledge distillation for {epochs} epochs")
        
        for epoch in range(epochs):
            total_loss = 0.0
            for inputs, targets in train_loader:
                inputs, targets = inputs.to(self.device), targets.to(self.device)
                
                optimizer.zero_grad()
                
                # Teacher predictions
                with torch.no_grad():
                    teacher_outputs = teacher_model(inputs)
                
                # Student predictions
                student_outputs = student_model(inputs)
                
                # Soft targets from teacher
                soft_targets = torch.nn.functional.softmax(
                    teacher_outputs / temperature, dim=1
                )
                soft_student = torch.nn.functional.log_softmax(
                    student_outputs / temperature, dim=1
                )
                
                # Distillation loss
                distillation_loss = criterion(soft_student, soft_targets)
                
                # Hard loss
                student_loss = hard_loss(student_outputs, targets)
                
                # Combined loss
                loss = alpha * (temperature ** 2) * distillation_loss + (1 - alpha) * student_loss
                
                loss.backward()
                optimizer.step()
                
                total_loss += loss.item()
            
            avg_loss = total_loss / len(train_loader)
            logger.info(f"Epoch {epoch+1}/{epochs}, Loss: {avg_loss:.4f}")
        
        logger.info("Knowledge distillation completed")
        return student_model
    
    def measure_model_size(self, model: nn.Module) -> float:
        """
        Measure model size in MB.
        
        Args:
            model: Model to measure
            
        Returns:
            Model size in MB
        """
        param_size = 0
        buffer_size = 0
        
        for param in model.parameters():
            param_size += param.nelement() * param.element_size()
        
        for buffer in model.buffers():
            buffer_size += buffer.nelement() * buffer.element_size()
        
        size_mb = (param_size + buffer_size) / 1024 / 1024
        return size_mb
    
    def compare_models(
        self,
        original_model: nn.Module,
        optimized_model: nn.Module,
        test_loader: DataLoader,
        method: str
    ) -> OptimizationResult:
        """
        Compare original and optimized models.
        
        Args:
            original_model: Original model
            optimized_model: Optimized model
            test_loader: Test data
            method: Optimization method used
            
        Returns:
            OptimizationResult
        """
        # Measure sizes
        original_size = self.measure_model_size(original_model)
        optimized_size = self.measure_model_size(optimized_model)
        
        # Measure accuracy
        original_acc = self._evaluate_model(original_model, test_loader)
        optimized_acc = self._evaluate_model(optimized_model, test_loader)
        
        # Calculate metrics
        size_reduction = (1 - optimized_size / original_size) * 100
        accuracy_drop = (1 - optimized_acc / original_acc) * 100
        
        # Measure latency (simplified)
        original_latency = self._measure_latency(original_model, test_loader)
        optimized_latency = self._measure_latency(optimized_model, test_loader)
        latency_improvement = (1 - optimized_latency / original_latency) * 100
        
        result = OptimizationResult(
            original_size_mb=original_size,
            optimized_size_mb=optimized_size,
            size_reduction_pct=size_reduction,
            original_accuracy=original_acc,
            optimized_accuracy=optimized_acc,
            accuracy_drop_pct=accuracy_drop,
            latency_improvement=latency_improvement,
            method=method,
            details={}
        )
        
        logger.info(f"Optimization complete: {size_reduction:.1f}% size reduction, {accuracy_drop:.2f}% accuracy drop")
        return result
    
    def _evaluate_model(self, model: nn.Module, test_loader: DataLoader) -> float:
        """
        Evaluate model accuracy.
        
        Args:
            model: Model to evaluate
            test_loader: Test data
            
        Returns:
            Accuracy
        """
        model.eval()
        correct = 0
        total = 0
        
        with torch.no_grad():
            for inputs, targets in test_loader:
                inputs, targets = inputs.to(self.device), targets.to(self.device)
                outputs = model(inputs)
                _, predicted = torch.max(outputs.data, 1)
                total += targets.size(0)
                correct += (predicted == targets).sum().item()
        
        accuracy = 100 * correct / total
        return accuracy
    
    def _measure_latency(self, model: nn.Module, test_loader: DataLoader, samples: int = 100) -> float:
        """
        Measure model inference latency.
        
        Args:
            model: Model to measure
            test_loader: Test data
            samples: Number of samples to measure
            
        Returns:
            Average latency in ms
        """
        model.eval()
        latencies = []
        
        with torch.no_grad():
            for i, (inputs, _) in enumerate(test_loader):
                if i >= samples:
                    break
                
                inputs = inputs.to(self.device)
                
                # Warm up
                if i < 10:
                    model(inputs)
                    continue
                
                # Measure latency
                start = torch.cuda.Event(enable_timing=True)
                end = torch.cuda.Event(enable_timing=True)
                
                start.record()
                model(inputs)
                end.record()
                
                torch.cuda.synchronize()
                latency_ms = start.elapsed_time(end)
                latencies.append(latency_ms)
        
        return np.mean(latencies)


# Example usage
if __name__ == "__main__":
    import torchvision.models as models
    from torchvision import datasets, transforms
    from torch.utils.data import DataLoader
    
    # Load a pre-trained model
    model = models.resnet18(pretrained=True)
    
    # Create dummy data for calibration
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
    ])
    
    # Create optimizer
    optimizer = ModelOptimizer(model)
    
    # Apply dynamic quantization
    quantized_model = optimizer.quantize(mode=QuantizationMode.DYNAMIC)
    
    # Measure sizes
    original_size = optimizer.measure_model_size(model)
    quantized_size = optimizer.measure_model_size(quantized_model)
    
    print(f"Original size: {original_size:.2f} MB")
    print(f"Quantized size: {quantized_size:.2f} MB")
    print(f"Size reduction: {(1 - quantized_size/original_size)*100:.1f}%")
    
    # Apply pruning
    pruned_model = optimizer.prune(
        method=PruningMethod.MAGNITUDE,
        sparsity=0.3,
        structured=False
    )
    
    # Remove pruning masks
    pruned_model = optimizer.remove_pruning_masks(pruned_model)
    pruned_size = optimizer.measure_model_size(pruned_model)
    
    print(f"Pruned size: {pruned_size:.2f} MB")
    print(f"Size reduction: {(1 - pruned_size/original_size)*100:.1f}%")
```

## Standards, Compliance & Security

### International Standards
- **ISO/IEC 27001:** Security of optimized model artifacts
- **GDPR:** Model optimization should not impact explainability requirements
- **SOC 2 Type II:** Integrity of optimization processes

### Security Protocol
- **Model Verification:** Verify optimized model behavior matches original
- **Secure Optimization:** Protect training data during optimization
- **Audit Trail:** Log all optimization steps and parameters
- **Version Control:** Track all optimization iterations

### Explainability
- **Accuracy Tracking:** Monitor accuracy impact of optimizations
- **Ablation Studies:** Document impact of each optimization technique
- **Visualization:** Visualize pruning patterns and quantization effects

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install torch torchvision onnxruntime
   ```

2. **Apply dynamic quantization:**
   ```python
   import torch.quantization as quant
   
   quantized_model = quant.quantize_dynamic(
       model,
       {torch.nn.Linear, torch.nn.LSTM},
       dtype=torch.qint8
   )
   ```

3. **Apply pruning:**
   ```python
   import torch.nn.utils.prune as prune
   
   prune.l1_unstructured(model.fc1, name='weight', amount=0.3)
   ```

4. **Export to ONNX for deployment:**
   ```python
   torch.onnx.export(
       quantized_model,
       dummy_input,
       "model.onnx",
       opset_version=14
   )
   ```

## Production Checklist

- [ ] Baseline model performance measured
- [ ] Optimization targets defined (size, speed, accuracy)
- [ ] Calibration dataset prepared (for static quantization)
- [ ] Accuracy impact quantified
- [ ] Latency improvements measured
- [ ] Model tested on target hardware
- [ ] Rollback plan documented
- [ ] Monitoring for performance degradation
- [ ] Version control for optimized models
- [ ] A/B testing with original model

## Anti-patterns

1. **Blind Quantization:** Quantizing without measuring accuracy impact
   - **Why it's bad:** Can cause significant accuracy loss
   - **Solution:** Always measure accuracy before and after optimization

2. **No Calibration:** Skipping calibration for static quantization
   - **Why it's bad:** Poor quantization, high accuracy loss
   - **Solution:** Use representative calibration data

3. **Pruning Without Fine-tuning:** Pruning without retraining
   - **Why it's bad:** Significant accuracy degradation
   - **Solution:** Always fine-tune after pruning

4. **Over-optimization:** Aggressively optimizing beyond acceptable accuracy loss
   - **Why it's bad:** Model becomes unusable
   - **Solution:** Set accuracy thresholds and stop when reached

## Unit Economics & KPIs

### Cost Calculation
```
Optimization ROI = (Cost Savings - Optimization Cost) / Optimization Cost

Cost Savings = (Original Inference Cost - Optimized Inference Cost) × Traffic
Optimization Cost = Engineering Time + Compute Resources for Training
```

### Key Performance Indicators
- **Size Reduction:** > 50% for quantization, > 30% for pruning
- **Latency Improvement:** > 2x for quantization, > 1.5x for pruning
- **Accuracy Loss:** < 1% for quantization, < 2% for pruning
- **Optimization Time:** < 1 hour for PTQ, < 1 day for QAT
- **Resource Efficiency:** > 70% GPU utilization after optimization

## Integration Points / Related Skills
- [High Performance Inference](../78-inference-model-serving/high-performance-inference/SKILL.md) - For serving optimized models
- [Model Registry Versioning](../77-mlops-data-engineering/model-registry-versioning/SKILL.md) - For tracking optimized model versions
- [GPU Cluster Management](../78-inference-model-serving/gpu-cluster-management/SKILL.md) - For managing GPU resources
- [Model Testing Validation](../77-mlops-data-engineering/model-testing-validation/SKILL.md) - For validating optimized models

## Further Reading
- [PyTorch Quantization Documentation](https://pytorch.org/docs/stable/quantization.html)
- [TensorRT Documentation](https://docs.nvidia.com/deeplearning/tensorrt/)
- [ONNX Runtime Quantization](https://onnxruntime.ai/docs/performance/quantization.html)
- [Model Compression Survey](https://arxiv.org/abs/2002.08673)
- [Knowledge Distillation Tutorial](https://arxiv.org/abs/1503.02531)
