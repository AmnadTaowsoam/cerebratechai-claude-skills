---
name: Model Training
description: Comprehensive guide for machine learning model training workflows using PyTorch, covering data preparation, training loops, hyperparameter tuning, and experiment tracking.
---

# Model Training

## Overview

Model training is the process of teaching machine learning models to make predictions or decisions based on data. This skill covers comprehensive training workflows including pipeline design, data preparation, training loops, hyperparameter tuning, experiment tracking, checkpoint management, early stopping, learning rate scheduling, distributed training, and model evaluation.

## Prerequisites

- Understanding of PyTorch and deep learning fundamentals
- Knowledge of neural network architectures
- Familiarity with data preprocessing and augmentation
- Understanding of loss functions and optimizers
- Basic knowledge of machine learning metrics

## Key Concepts

### Training Pipeline Architecture

- **Modular Design**: Separation of data, model, optimizer, and training logic
- **Configuration Management**: YAML-based configuration for reproducibility
- **Checkpoint Management**: Saving and loading model states
- **Early Stopping**: Preventing overfitting by stopping early
- **Experiment Tracking**: Recording metrics and hyperparameters

### Data Preparation

- **Train/Val/Test Splits**: Proper data partitioning for model evaluation
- **Custom Datasets**: Implementing PyTorch Dataset classes
- **Data Loaders**: Efficient data loading with batching and shuffling
- **Data Augmentation**: Increasing data diversity for better generalization

### Training Loop Patterns

- **Basic Training Loop**: Standard forward/backward pass
- **Mixed Precision Training**: Using FP16 for faster training
- **Gradient Accumulation**: Simulating larger batch sizes
- **Distributed Training**: Multi-GPU and multi-node training

### Hyperparameter Tuning

- **Grid Search**: Exhaustive search over parameter space
- **Random Search**: Random sampling of parameters
- **Bayesian Optimization**: Smart parameter exploration with Optuna

### Learning Rate Scheduling

- **StepLR**: Periodic learning rate decay
- **CosineAnnealingLR**: Cosine annealing schedule
- **ReduceLROnPlateau**: Adaptive learning rate based on metrics
- **OneCycleLR**: One cycle learning rate policy

## Implementation Guide

### Training Pipeline Design

#### Pipeline Architecture

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from pathlib import Path
import yaml
from typing import Dict, Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TrainingPipeline:
    """Complete training pipeline with modularity."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.train_loader = None
        self.val_loader = None
        self.optimizer = None
        self.scheduler = None
        self.criterion = None

    def setup_data(self):
        """Setup data loaders."""
        raise NotImplementedError

    def setup_model(self):
        """Setup model architecture."""
        raise NotImplementedError

    def setup_optimizer(self):
        """Setup optimizer and scheduler."""
        raise NotImplementedError

    def train_epoch(self, epoch: int):
        """Train for one epoch."""
        raise NotImplementedError

    def validate(self, epoch: int):
        """Validate model."""
        raise NotImplementedError

    def train(self):
        """Main training loop."""
        logger.info(f"Starting training on {self.device}")

        best_metric = float('inf') if self.config.get('minimize_metric', True) else 0.0
        patience_counter = 0

        for epoch in range(self.config['epochs']):
            # Train
            train_metrics = self.train_epoch(epoch)

            # Validate
            val_metrics = self.validate(epoch)

            # Log metrics
            self._log_metrics(epoch, train_metrics, val_metrics)

            # Learning rate scheduling
            if self.scheduler:
                if isinstance(self.scheduler, torch.optim.lr_scheduler.ReduceLROnPlateau):
                    self.scheduler.step(val_metrics[self.config['monitor_metric']])
                else:
                    self.scheduler.step()

            # Save checkpoint
            self._save_checkpoint(epoch, val_metrics)

            # Early stopping
            current_metric = val_metrics[self.config['monitor_metric']]
            is_better = (current_metric < best_metric) if self.config.get('minimize_metric', True) \
                       else (current_metric > best_metric)

            if is_better:
                best_metric = current_metric
                patience_counter = 0
                self._save_best_model(epoch, val_metrics)
            else:
                patience_counter += 1
                if patience_counter >= self.config.get('early_stopping_patience', 10):
                    logger.info(f"Early stopping at epoch {epoch}")
                    break

    def _log_metrics(self, epoch: int, train_metrics: Dict, val_metrics: Dict):
        """Log training and validation metrics."""
        logger.info(f"Epoch {epoch}: Train {train_metrics} | Val {val_metrics}")

    def _save_checkpoint(self, epoch: int, metrics: Dict):
        """Save training checkpoint."""
        checkpoint = {
            'epoch': epoch,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'scheduler_state_dict': self.scheduler.state_dict() if self.scheduler else None,
            'metrics': metrics,
            'config': self.config
        }

        path = Path(self.config['checkpoint_dir']) / f"checkpoint_epoch_{epoch}.pt"
        path.parent.mkdir(parents=True, exist_ok=True)
        torch.save(checkpoint, path)

    def _save_best_model(self, epoch: int, metrics: Dict):
        """Save best model."""
        path = Path(self.config['checkpoint_dir']) / "best_model.pt"
        path.parent.mkdir(parents=True, exist_ok=True)

        torch.save({
            'model_state_dict': self.model.state_dict(),
            'epoch': epoch,
            'metrics': metrics
        }, path)

    def load_checkpoint(self, checkpoint_path: str):
        """Load training checkpoint."""
        checkpoint = torch.load(checkpoint_path, map_location=self.device)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        if self.scheduler and checkpoint['scheduler_state_dict']:
            self.scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
        return checkpoint['epoch'], checkpoint['metrics']
```

#### Configuration Management

```python
# config.yaml
model:
  name: "resnet50"
  num_classes: 10
  pretrained: true

data:
  data_dir: "./data"
  batch_size: 32
  num_workers: 4
  train_split: 0.8
  val_split: 0.1
  test_split: 0.1

training:
  epochs: 100
  learning_rate: 0.001
  weight_decay: 0.0001
  momentum: 0.9

optimizer:
  type: "Adam"
  betas: [0.9, 0.999]

scheduler:
  type: "CosineAnnealingLR"
  T_max: 100
  eta_min: 0.00001

early_stopping:
  patience: 10
  monitor_metric: "val_loss"
  minimize_metric: true

checkpoint_dir: "./checkpoints"
log_dir: "./logs"
```

```python
import yaml

def load_config(config_path: str) -> Dict:
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

# Usage
config = load_config("config.yaml")
pipeline = TrainingPipeline(config)
```

### Data Preparation

#### Train/Val/Test Splits

```python
from torch.utils.data import random_split, DataLoader
from sklearn.model_selection import train_test_split
import numpy as np

def create_splits(dataset, train_ratio=0.8, val_ratio=0.1, test_ratio=0.1, seed=42):
    """Create train/val/test splits."""
    assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-6, "Ratios must sum to 1"

    total_size = len(dataset)
    train_size = int(train_ratio * total_size)
    val_size = int(val_ratio * total_size)
    test_size = total_size - train_size - val_size

    train_dataset, val_dataset, test_dataset = random_split(
        dataset,
        [train_size, val_size, test_size],
        generator=torch.Generator().manual_seed(seed)
    )

    return train_dataset, val_dataset, test_dataset

def stratified_split(dataset, labels, train_ratio=0.8, val_ratio=0.1, seed=42):
    """Create stratified splits for classification."""
    train_indices, temp_indices = train_test_split(
        np.arange(len(dataset)),
        test_size=(1 - train_ratio),
        stratify=labels,
        random_state=seed
    )

    val_ratio_adjusted = val_ratio / (val_ratio + (1 - train_ratio - val_ratio))
    val_indices, test_indices = train_test_split(
        temp_indices,
        test_size=(1 - val_ratio_adjusted),
        stratify=[labels[i] for i in temp_indices],
        random_state=seed
    )

    return train_indices, val_indices, test_indices
```

#### Custom Dataset

```python
from torch.utils.data import Dataset
from PIL import Image
import json
from pathlib import Path

class CustomImageDataset(Dataset):
    """Custom image dataset."""

    def __init__(self, data_dir, transform=None, split='train'):
        self.data_dir = Path(data_dir)
        self.transform = transform
        self.split = split

        # Load annotations
        annotation_file = self.data_dir / f"{split}_annotations.json"
        with open(annotation_file, 'r') as f:
            self.annotations = json.load(f)

        self.image_paths = list(self.annotations.keys())

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        # Load image
        image_path = self.data_dir / self.split / "images" / self.image_paths[idx]
        image = Image.open(image_path).convert('RGB')

        # Get label
        label = self.annotations[self.image_paths[idx]]['label']

        # Apply transforms
        if self.transform:
            image = self.transform(image)

        return image, label

class CustomTextDataset(Dataset):
    """Custom text dataset."""

    def __init__(self, texts, labels, tokenizer, max_length=512):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = str(self.texts[idx])
        label = self.labels[idx]

        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )

        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }
```

#### Data Loaders

```python
from torchvision import transforms

def create_data_loaders(config):
    """Create data loaders with transforms."""

    # Define transforms
    train_transform = transforms.Compose([
        transforms.Resize((config['data']['image_size'], config['data']['image_size'])),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(degrees=15),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    val_transform = transforms.Compose([
        transforms.Resize((config['data']['image_size'], config['data']['image_size'])),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    # Create datasets
    full_dataset = CustomImageDataset(
        config['data']['data_dir'],
        transform=None
    )

    train_dataset, val_dataset, test_dataset = create_splits(full_dataset)

    # Apply transforms
    train_dataset.dataset.transform = train_transform
    val_dataset.dataset.transform = val_transform
    test_dataset.dataset.transform = val_transform

    # Create data loaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=config['data']['batch_size'],
        shuffle=True,
        num_workers=config['data']['num_workers'],
        pin_memory=True,
        drop_last=True
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=config['data']['batch_size'],
        shuffle=False,
        num_workers=config['data']['num_workers'],
        pin_memory=True
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=config['data']['batch_size'],
        shuffle=False,
        num_workers=config['data']['num_workers'],
        pin_memory=True
    )

    return train_loader, val_loader, test_loader
```

#### Data Augmentation

```python
from torchvision import transforms
import albumentations as A
from albumentations.pytorch import ToTensorV2

# PyTorch transforms
advanced_transforms = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.RandomCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.RandomVerticalFlip(),
    transforms.RandomRotation(30),
    transforms.RandomAffine(degrees=0, translate=(0.1, 0.1), scale=(0.9, 1.1)),
    transforms.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.3, hue=0.1),
    transforms.RandomGrayscale(p=0.1),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Albumentations transforms
albumentations_transform = A.Compose([
    A.Resize(256, 256),
    A.RandomCrop(224, 224),
    A.HorizontalFlip(p=0.5),
    A.VerticalFlip(p=0.2),
    A.Rotate(limit=30, p=0.5),
    A.OneOf([
        A.GaussNoise(p=1.0),
        A.ISONoise(p=1.0),
    ], p=0.2),
    A.OneOf([
        A.MotionBlur(p=1.0),
        A.MedianBlur(p=1.0),
        A.GaussianBlur(p=1.0),
    ], p=0.2),
    A.ShiftScaleRotate(shift_limit=0.1, scale_limit=0.1, rotate_limit=15, p=0.5),
    A.RandomBrightnessContrast(p=0.5),
    A.HueSaturationValue(p=0.3),
    A.Cutout(num_holes=8, max_h_size=16, max_w_size=16, p=0.3),
    A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ToTensorV2(),
])

class AlbumentationsDataset(Dataset):
    """Dataset using Albumentations transforms."""

    def __init__(self, images, labels, transform=None):
        self.images = images
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        image = self.images[idx]
        label = self.labels[idx]

        if self.transform:
            image = self.transform(image=image)['image']

        return image, label
```

### Training Loop Patterns

#### Basic Training Loop

```python
import torch
import torch.nn as nn
from tqdm import tqdm

def train_epoch(model, train_loader, criterion, optimizer, device):
    """Train for one epoch."""
    model.train()
    total_loss = 0.0
    correct = 0
    total = 0

    pbar = tqdm(train_loader, desc="Training")
    for batch_idx, (inputs, targets) in enumerate(pbar):
        inputs, targets = inputs.to(device), targets.to(device)

        # Forward pass
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)

        # Backward pass
        loss.backward()
        optimizer.step()

        # Metrics
        total_loss += loss.item()
        _, predicted = outputs.max(1)
        total += targets.size(0)
        correct += predicted.eq(targets).sum().item()

        # Update progress bar
        pbar.set_postfix({
            'loss': total_loss / (batch_idx + 1),
            'acc': 100. * correct / total
        })

    avg_loss = total_loss / len(train_loader)
    accuracy = 100. * correct / total

    return {'loss': avg_loss, 'accuracy': accuracy}
```

#### Validation Loop

```python
def validate(model, val_loader, criterion, device):
    """Validate model."""
    model.eval()
    total_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():
        for inputs, targets in tqdm(val_loader, desc="Validation"):
            inputs, targets = inputs.to(device), targets.to(device)

            outputs = model(inputs)
            loss = criterion(outputs, targets)

            total_loss += loss.item()
            _, predicted = outputs.max(1)
            total += targets.size(0)
            correct += predicted.eq(targets).sum().item()

    avg_loss = total_loss / len(val_loader)
    accuracy = 100. * correct / total

    return {'loss': avg_loss, 'accuracy': accuracy}
```

#### Training with Mixed Precision

```python
from torch.cuda.amp import autocast, GradScaler

def train_epoch_amp(model, train_loader, criterion, optimizer, device, scaler=None):
    """Train with automatic mixed precision."""
    model.train()
    total_loss = 0.0
    correct = 0
    total = 0

    if scaler is None:
        scaler = GradScaler()

    for inputs, targets in tqdm(train_loader, desc="Training (AMP)"):
        inputs, targets = inputs.to(device), targets.to(device)

        optimizer.zero_grad()

        with autocast():
            outputs = model(inputs)
            loss = criterion(outputs, targets)

        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()

        total_loss += loss.item()
        _, predicted = outputs.max(1)
        total += targets.size(0)
        correct += predicted.eq(targets).sum().item()

    avg_loss = total_loss / len(train_loader)
    accuracy = 100. * correct / total

    return {'loss': avg_loss, 'accuracy': accuracy}
```

#### Training with Gradient Accumulation

```python
def train_epoch_accumulation(model, train_loader, criterion, optimizer, device, accumulation_steps=4):
    """Train with gradient accumulation for larger effective batch size."""
    model.train()
    total_loss = 0.0
    correct = 0
    total = 0

    optimizer.zero_grad()

    for batch_idx, (inputs, targets) in enumerate(tqdm(train_loader, desc="Training")):
        inputs, targets = inputs.to(device), targets.to(device)

        # Forward pass
        outputs = model(inputs)
        loss = criterion(outputs, targets) / accumulation_steps

        # Backward pass
        loss.backward()

        # Accumulate gradients
        if (batch_idx + 1) % accumulation_steps == 0:
            optimizer.step()
            optimizer.zero_grad()

        # Metrics
        total_loss += loss.item() * accumulation_steps
        _, predicted = outputs.max(1)
        total += targets.size(0)
        correct += predicted.eq(targets).sum().item()

    # Handle remaining batches
    if (batch_idx + 1) % accumulation_steps != 0:
        optimizer.step()
        optimizer.zero_grad()

    avg_loss = total_loss / len(train_loader)
    accuracy = 100. * correct / total

    return {'loss': avg_loss, 'accuracy': accuracy}
```

### Hyperparameter Tuning

#### Grid Search

```python
import itertools
from copy import deepcopy

def grid_search(model_class, train_loader, val_loader, param_grid, device):
    """Perform grid search over hyperparameters."""
    results = []

    # Generate all combinations
    keys, values = zip(*param_grid.items())
    combinations = [dict(zip(keys, v)) for v in itertools.product(*values)]

    for params in combinations:
        print(f"\nTesting params: {params}")

        # Create model with current params
        model = model_class(**params)
        model = model.to(device)

        optimizer = torch.optim.Adam(
            model.parameters(),
            lr=params.get('learning_rate', 0.001)
        )

        criterion = nn.CrossEntropyLoss()

        # Train for a few epochs
        val_acc = 0
        for epoch in range(5):  # Quick training
            train_metrics = train_epoch(model, train_loader, criterion, optimizer, device)
            val_metrics = validate(model, val_loader, criterion, device)
            val_acc = val_metrics['accuracy']

        results.append({
            'params': params,
            'val_accuracy': val_acc
        })

    # Sort by validation accuracy
    results.sort(key=lambda x: x['val_accuracy'], reverse=True)

    return results

# Usage
param_grid = {
    'learning_rate': [0.001, 0.0001, 0.00001],
    'dropout': [0.1, 0.3, 0.5],
    'hidden_size': [128, 256, 512]
}

results = grid_search(MyModel, train_loader, val_loader, param_grid, device)
print(f"Best params: {results[0]['params']}")
```

#### Random Search

```python
import random

def random_search(model_class, train_loader, val_loader, param_ranges, n_iterations=20, device='cuda'):
    """Perform random search over hyperparameters."""
    results = []

    for i in range(n_iterations):
        # Sample random parameters
        params = {}
        for key, (min_val, max_val, is_log) in param_ranges.items():
            if is_log:
                params[key] = 10 ** random.uniform(min_val, max_val)
            else:
                params[key] = random.uniform(min_val, max_val)

        print(f"\nIteration {i+1}/{n_iterations}: {params}")

        # Train and evaluate
        model = model_class(**params)
        model = model.to(device)

        optimizer = torch.optim.Adam(model.parameters(), lr=params['learning_rate'])
        criterion = nn.CrossEntropyLoss()

        val_acc = 0
        for epoch in range(5):
            train_metrics = train_epoch(model, train_loader, criterion, optimizer, device)
            val_metrics = validate(model, val_loader, criterion, device)
            val_acc = val_metrics['accuracy']

        results.append({
            'params': params,
            'val_accuracy': val_acc
        })

    results.sort(key=lambda x: x['val_accuracy'], reverse=True)
    return results

# Usage
param_ranges = {
    'learning_rate': (-4, -2, True),  # Log scale: 10^-4 to 10^-2
    'dropout': (0.1, 0.5, False),
    'hidden_size': (128, 512, False)
}
```

#### Bayesian Optimization with Optuna

```python
import optuna

def objective(trial, model_class, train_loader, val_loader, device):
    """Optuna objective function."""

    # Suggest hyperparameters
    learning_rate = trial.suggest_float('learning_rate', 1e-5, 1e-2, log=True)
    dropout = trial.suggest_float('dropout', 0.1, 0.5)
    hidden_size = trial.suggest_categorical('hidden_size', [128, 256, 512])

    # Create model
    model = model_class(dropout=dropout, hidden_size=hidden_size)
    model = model.to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    criterion = nn.CrossEntropyLoss()

    # Train
    best_val_acc = 0
    for epoch in range(10):
        train_metrics = train_epoch(model, train_loader, criterion, optimizer, device)
        val_metrics = validate(model, val_loader, criterion, device)
        val_acc = val_metrics['accuracy']

        if val_acc > best_val_acc:
            best_val_acc = val_acc

        # Prune unpromising trials
        trial.report(val_acc, epoch)
        if trial.should_prune():
            raise optuna.TrialPruned()

    return best_val_acc

def run_optuna_study(model_class, train_loader, val_loader, device, n_trials=50):
    """Run Optuna study."""
    study = optuna.create_study(direction='maximize')

    study.optimize(
        lambda trial: objective(trial, model_class, train_loader, val_loader, device),
        n_trials=n_trials,
        timeout=None,
        show_progress_bar=True
    )

    print("\nBest trial:")
    trial = study.best_trial
    print(f"  Value: {trial.value}")
    print(f"  Params: {trial.params}")

    return study

# Usage
study = run_optuna_study(MyModel, train_loader, val_loader, device, n_trials=50)
```

### Experiment Tracking

#### MLflow Integration

```python
import mlflow
import mlflow.pytorch
from mlflow.tracking import MlflowClient

class MLflowTracker:
    """MLflow experiment tracker."""

    def __init__(self, experiment_name, tracking_uri=None):
        if tracking_uri:
            mlflow.set_tracking_uri(tracking_uri)

        self.experiment = mlflow.set_experiment(experiment_name)
        self.run = None

    def start_run(self, run_name=None, params=None):
        """Start MLflow run."""
        self.run = mlflow.start_run(run_name=run_name)

        if params:
            mlflow.log_params(params)

    def log_metrics(self, metrics, step=None):
        """Log metrics."""
        mlflow.log_metrics(metrics, step=step)

    def log_model(self, model, model_name="model"):
        """Log PyTorch model."""
        mlflow.pytorch.log_model(model, model_name)

    def log_artifact(self, file_path):
        """Log artifact."""
        mlflow.log_artifact(file_path)

    def end_run(self, status="FINISHED"):
        """End MLflow run."""
        mlflow.end_run(status=status)

# Usage
tracker = MLflowTracker("my_experiment")

tracker.start_run(run_name="experiment_1", params={
    'learning_rate': 0.001,
    'batch_size': 32,
    'epochs': 100
})

for epoch in range(100):
    train_metrics = train_epoch(model, train_loader, criterion, optimizer, device)
    val_metrics = validate(model, val_loader, criterion, device)

    tracker.log_metrics({f"train_{k}": v for k, v in train_metrics.items()}, step=epoch)
    tracker.log_metrics({f"val_{k}": v for k, v in val_metrics.items()}, step=epoch)

tracker.log_model(model)
tracker.end_run()
```

#### Weights & Biases Integration

```python
import wandb

class WandBTracker:
    """Weights & Biases tracker."""

    def __init__(self, project_name, config=None):
        wandb.init(project=project_name, config=config)
        self.config = wandb.config

    def log_metrics(self, metrics, step=None):
        """Log metrics."""
        wandb.log(metrics, step=step)

    def log_model(self, model, model_name="model"):
        """Log model."""
        torch.save(model.state_dict(), f"{model_name}.pt")
        wandb.save(f"{model_name}.pt")

    def log_image(self, image, caption):
        """Log image."""
        wandb.log({caption: wandb.Image(image)})

    def finish(self):
        """Finish W&B run."""
        wandb.finish()

# Usage
tracker = WandBTracker("my_project", config={
    'learning_rate': 0.001,
    'batch_size': 32,
    'epochs': 100
})

for epoch in range(100):
    train_metrics = train_epoch(model, train_loader, criterion, optimizer, device)
    val_metrics = validate(model, val_loader, criterion, device)

    tracker.log_metrics({**{f"train_{k}": v for k, v in train_metrics.items()},
                        **{f"val_{k}": v for k, v in val_metrics.items()}}, step=epoch)

tracker.log_model(model)
tracker.finish()
```

#### TensorBoard Integration

```python
from torch.utils.tensorboard import SummaryWriter
import torchvision

class TensorBoardTracker:
    """TensorBoard tracker."""

    def __init__(self, log_dir):
        self.writer = SummaryWriter(log_dir)

    def log_metrics(self, metrics, step, prefix=""):
        """Log metrics."""
        for key, value in metrics.items():
            self.writer.add_scalar(f"{prefix}/{key}", value, step)

    def log_images(self, images, step, tag="images"):
        """Log images."""
        grid = torchvision.utils.make_grid(images)
        self.writer.add_image(tag, grid, step)

    def log_model_graph(self, model, inputs):
        """Log model graph."""
        self.writer.add_graph(model, inputs)

    def log_histograms(self, model, step):
        """Log parameter histograms."""
        for name, param in model.named_parameters():
            self.writer.add_histogram(name, param, step)

    def close(self):
        """Close writer."""
        self.writer.close()

# Usage
tracker = TensorBoardTracker("./logs")

for epoch in range(100):
    train_metrics = train_epoch(model, train_loader, criterion, optimizer, device)
    val_metrics = validate(model, val_loader, criterion, device)

    tracker.log_metrics(train_metrics, epoch, "train")
    tracker.log_metrics(val_metrics, epoch, "val")
    tracker.log_histograms(model, epoch)

tracker.close()
```

### Checkpoint Management

#### Checkpoint Saving and Loading

```python
import os
from pathlib import Path
import shutil

class CheckpointManager:
    """Manage model checkpoints."""

    def __init__(self, checkpoint_dir, max_to_keep=5):
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.max_to_keep = max_to_keep
        self.checkpoints = []

    def save_checkpoint(self, model, optimizer, scheduler, epoch, metrics, filename=None):
        """Save checkpoint."""
        if filename is None:
            filename = f"checkpoint_epoch_{epoch}.pt"

        checkpoint_path = self.checkpoint_dir / filename

        checkpoint = {
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'scheduler_state_dict': scheduler.state_dict() if scheduler else None,
            'metrics': metrics
        }

        torch.save(checkpoint, checkpoint_path)
        self.checkpoints.append(checkpoint_path)

        # Keep only max_to_keep checkpoints
        if len(self.checkpoints) > self.max_to_keep:
            oldest = self.checkpoints.pop(0)
            if oldest.exists():
                oldest.unlink()

        return checkpoint_path

    def load_checkpoint(self, checkpoint_path, model, optimizer=None, scheduler=None):
        """Load checkpoint."""
        checkpoint = torch.load(checkpoint_path, map_location='cpu')

        model.load_state_dict(checkpoint['model_state_dict'])

        if optimizer and 'optimizer_state_dict' in checkpoint:
            optimizer.load_state_dict(checkpoint['optimizer_state_dict'])

        if scheduler and 'scheduler_state_dict' in checkpoint and checkpoint['scheduler_state_dict']:
            scheduler.load_state_dict(checkpoint['scheduler_state_dict'])

        return checkpoint['epoch'], checkpoint.get('metrics', {})

    def get_latest_checkpoint(self):
        """Get path to latest checkpoint."""
        if not self.checkpoints:
            return None
        return max(self.checkpoints, key=os.path.getctime)

    def get_best_checkpoint(self, metric_name, minimize=True):
        """Get checkpoint with best metric."""
        best_checkpoint = None
        best_value = float('inf') if minimize else float('-inf')

        for checkpoint_path in self.checkpoints:
            checkpoint = torch.load(checkpoint_path)
            value = checkpoint['metrics'].get(metric_name)

            if value is not None:
                if (minimize and value < best_value) or (not minimize and value > best_value):
                    best_value = value
                    best_checkpoint = checkpoint_path

        return best_checkpoint
```

### Early Stopping

```python
class EarlyStopping:
    """Early stopping to stop training when validation metric stops improving."""

    def __init__(self, patience=10, min_delta=0, mode='min', verbose=True):
        """
        Args:
            patience: Number of epochs to wait before stopping
            min_delta: Minimum change to qualify as improvement
            mode: 'min' for metrics to minimize, 'max' for metrics to maximize
            verbose: Print messages
        """
        self.patience = patience
        self.min_delta = min_delta
        self.mode = mode
        self.verbose = verbose
        self.counter = 0
        self.best_score = None
        self.early_stop = False

    def __call__(self, metric):
        """Check if should stop training."""
        if self.best_score is None:
            self.best_score = metric
        elif self._is_improvement(metric):
            self.best_score = metric
            self.counter = 0
        else:
            self.counter += 1
            if self.verbose:
                print(f'EarlyStopping counter: {self.counter} out of {self.patience}')
            if self.counter >= self.patience:
                self.early_stop = True

        return self.early_stop

    def _is_improvement(self, metric):
        """Check if metric is an improvement."""
        if self.mode == 'min':
            return metric < self.best_score - self.min_delta
        else:
            return metric > self.best_score + self.min_delta

# Usage
early_stopping = EarlyStopping(patience=10, mode='min')

for epoch in range(100):
    train_metrics = train_epoch(model, train_loader, criterion, optimizer, device)
    val_metrics = validate(model, val_loader, criterion, device)

    if early_stopping(val_metrics['loss']):
        print(f'Early stopping at epoch {epoch}')
        break
```

### Learning Rate Scheduling

#### Common Schedulers

```python
import torch.optim as optim

# StepLR - Decay LR by gamma every step_size epochs
scheduler_step = optim.lr_scheduler.StepLR(
    optimizer,
    step_size=30,
    gamma=0.1
)

# ExponentialLR - Decay LR by gamma every epoch
scheduler_exp = optim.lr_scheduler.ExponentialLR(
    optimizer,
    gamma=0.95
)

# CosineAnnealingLR - Cosine annealing
scheduler_cosine = optim.lr_scheduler.CosineAnnealingLR(
    optimizer,
    T_max=100,
    eta_min=1e-6
)

# ReduceLROnPlateau - Reduce LR when metric plateaus
scheduler_plateau = optim.lr_scheduler.ReduceLROnPlateau(
    optimizer,
    mode='min',
    factor=0.1,
    patience=5,
    verbose=True
)

# OneCycleLR - One cycle policy
scheduler_onecycle = optim.lr_scheduler.OneCycleLR(
    optimizer,
    max_lr=0.01,
    total_steps=1000,
    pct_start=0.3,
    anneal_strategy='cos'
)

# CosineAnnealingWarmRestarts
scheduler_warm = optim.lr_scheduler.CosineAnnealingWarmRestarts(
    optimizer,
    T_0=10,
    T_mult=2
)
```

#### Custom Scheduler

```python
from torch.optim.lr_scheduler import _LRScheduler
import numpy as np

class WarmupCosineScheduler(_LRScheduler):
    """Learning rate scheduler with warmup and cosine annealing."""

    def __init__(self, optimizer, warmup_epochs, max_epochs, min_lr=0, max_lr=None):
        self.warmup_epochs = warmup_epochs
        self.max_epochs = max_epochs
        self.min_lr = min_lr
        self.max_lr = max_lr if max_lr else optimizer.param_groups[0]['lr']
        super().__init__(optimizer)

    def get_lr(self):
        if self.last_epoch < self.warmup_epochs:
            # Linear warmup
            return [self.max_lr * (self.last_epoch + 1) / self.warmup_epochs
                    for _ in self.base_lrs]
        else:
            # Cosine annealing
            progress = (self.last_epoch - self.warmup_epochs) / (self.max_epochs - self.warmup_epochs)
            cosine_factor = 0.5 * (1 + np.cos(np.pi * progress))
            return [self.min_lr + (self.max_lr - self.min_lr) * cosine_factor
                    for _ in self.base_lrs]

# Usage
scheduler = WarmupCosineScheduler(
    optimizer,
    warmup_epochs=10,
    max_epochs=100,
    min_lr=1e-6
)
```

### Distributed Training

#### DataParallel (Single Node, Multi-GPU)

```python
import torch.nn as nn

# Wrap model with DataParallel
if torch.cuda.device_count() > 1:
    print(f"Using {torch.cuda.device_count()} GPUs")
    model = nn.DataParallel(model)

model = model.to(device)

# Training loop remains the same
for epoch in range(epochs):
    train_metrics = train_epoch(model, train_loader, criterion, optimizer, device)
    val_metrics = validate(model, val_loader, criterion, device)
```

#### DistributedDataParallel (Multi-Node, Multi-GPU)

```python
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data.distributed import DistributedSampler

def setup_distributed():
    """Setup distributed training."""
    dist.init_process_group(backend='nccl')
    local_rank = int(os.environ['LOCAL_RANK'])
    torch.cuda.set_device(local_rank)
    return local_rank

def cleanup_distributed():
    """Cleanup distributed training."""
    dist.destroy_process_group()

def create_dataloader_distributed(dataset, batch_size, num_workers, rank, world_size):
    """Create distributed data loader."""
    sampler = DistributedSampler(
        dataset,
        num_replicas=world_size,
        rank=rank,
        shuffle=True
    )

    dataloader = DataLoader(
        dataset,
        batch_size=batch_size,
        sampler=sampler,
        num_workers=num_workers,
        pin_memory=True
    )

    return dataloader, sampler

# Training script
def train_distributed(rank, world_size, config):
    """Distributed training function."""
    local_rank = setup_distributed()
    device = torch.device(f"cuda:{local_rank}")

    # Create model
    model = MyModel().to(device)
    model = DDP(model, device_ids=[local_rank])

    # Create dataloaders
    train_dataset = CustomDataset(...)
    train_loader, train_sampler = create_dataloader_distributed(
        train_dataset, config['batch_size'], config['num_workers'], rank, world_size
    )

    # Training loop
    for epoch in range(config['epochs']):
        train_sampler.set_epoch(epoch)

        for batch_idx, (inputs, targets) in enumerate(train_loader):
            inputs, targets = inputs.to(device), targets.to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()

    cleanup_distributed()

# Launch with torchrun
# torchrun --nproc_per_node=4 train_script.py
```

### Model Evaluation

#### Classification Metrics

```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, classification_report
)
import numpy as np

def evaluate_classification(model, dataloader, device, num_classes):
    """Evaluate classification model."""
    model.eval()

    all_predictions = []
    all_targets = []
    all_probabilities = []

    with torch.no_grad():
        for inputs, targets in dataloader:
            inputs, targets = inputs.to(device), targets.to(device)

            outputs = model(inputs)
            probabilities = torch.softmax(outputs, dim=1)
            _, predictions = outputs.max(1)

            all_predictions.extend(predictions.cpu().numpy())
            all_targets.extend(targets.cpu().numpy())
            all_probabilities.extend(probabilities.cpu().numpy())

    # Convert to numpy arrays
    predictions = np.array(all_predictions)
    targets = np.array(all_targets)
    probabilities = np.array(all_probabilities)

    # Calculate metrics
    metrics = {
        'accuracy': accuracy_score(targets, predictions),
        'precision': precision_score(targets, predictions, average='weighted'),
        'recall': recall_score(targets, predictions, average='weighted'),
        'f1': f1_score(targets, predictions, average='weighted'),
        'confusion_matrix': confusion_matrix(targets, predictions).tolist(),
        'classification_report': classification_report(targets, predictions, output_dict=True)
    }

    return metrics, predictions, probabilities
```

#### Object Detection Metrics

```python
from collections import defaultdict
import numpy as np

def calculate_iou(box1, box2):
    """Calculate IoU between two boxes."""
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    intersection = max(0, x2 - x1) * max(0, y2 - y1)

    area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])

    union = area1 + area2 - intersection

    return intersection / union if union > 0 else 0

def calculate_ap(predictions, targets, iou_threshold=0.5, num_classes=80):
    """Calculate Average Precision for object detection."""
    ap_per_class = []

    for class_id in range(num_classes):
        # Filter predictions and targets for this class
        class_preds = [p for p in predictions if p['class_id'] == class_id]
        class_targets = [t for t in targets if t['class_id'] == class_id]

        if len(class_targets) == 0:
            continue

        # Sort predictions by confidence
        class_preds.sort(key=lambda x: x['confidence'], reverse=True)

        # Calculate TP and FP
        tp = np.zeros(len(class_preds))
        fp = np.zeros(len(class_preds))
        matched_targets = set()

        for i, pred in enumerate(class_preds):
            best_iou = 0
            best_target_idx = -1

            for j, target in enumerate(class_targets):
                if j in matched_targets:
                    continue

                iou = calculate_iou(pred['bbox'], target['bbox'])
                if iou > best_iou:
                    best_iou = iou
                    best_target_idx = j

            if best_iou >= iou_threshold:
                tp[i] = 1
                matched_targets.add(best_target_idx)
            else:
                fp[i] = 1

        # Calculate precision and recall
        tp_cumsum = np.cumsum(tp)
        fp_cumsum = np.cumsum(fp)
        recalls = tp_cumsum / len(class_targets)
        precisions = tp_cumsum / (tp_cumsum + fp_cumsum + 1e-10)

        # Calculate AP using 11-point interpolation
        ap = 0
        for t in np.arange(0, 1.1, 0.1):
            mask = recalls >= t
            if np.any(mask):
                p = np.max(precisions[mask])
                ap += p / 11

        ap_per_class.append(ap)

    # Calculate mAP
    mAP = np.mean(ap_per_class) if ap_per_class else 0

    return mAP, ap_per_class
```

## Best Practices

### Training Tips

1. **Set Random Seeds for Reproducibility**
   ```python
   def set_seed(seed=42):
       torch.manual_seed(seed)
       torch.cuda.manual_seed(seed)
       torch.cuda.manual_seed_all(seed)
       np.random.seed(seed)
       torch.backends.cudnn.deterministic = True
       torch.backends.cudnn.benchmark = False
   ```

2. **Use Gradient Clipping**
   ```python
   torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
   ```

3. **Use Learning Rate Finder**
   ```python
   def find_lr(model, train_loader, criterion, device, init_lr=1e-7, final_lr=10, num_iter=100):
       """Find optimal learning rate."""
       model.train()
       optimizer = torch.optim.Adam(model.parameters(), lr=init_lr)
       gamma = (final_lr / init_lr) ** (1 / num_iter)

       lrs = []
       losses = []

       for i, (inputs, targets) in enumerate(train_loader):
           if i >= num_iter:
               break

           inputs, targets = inputs.to(device), targets.to(device)

           optimizer.zero_grad()
           outputs = model(inputs)
           loss = criterion(outputs, targets)
           loss.backward()
           optimizer.step()

           lrs.append(optimizer.param_groups[0]['lr'])
           losses.append(loss.item())

           optimizer.param_groups[0]['lr'] *= gamma

       return lrs, losses
   ```

4. **Use Model Checkpointing with Best Validation Metric**
   ```python
   best_val_loss = float('inf')
   for epoch in range(epochs):
       val_loss = validate(model, val_loader, criterion, device)['loss']
       if val_loss < best_val_loss:
           best_val_loss = val_loss
           torch.save(model.state_dict(), 'best_model.pt')
   ```

5. **Use Gradient Accumulation for Larger Effective Batch Size**
   ```python
   accumulation_steps = 4
   for i, (inputs, targets) in enumerate(train_loader):
       loss = criterion(model(inputs), targets) / accumulation_steps
       loss.backward()

       if (i + 1) % accumulation_steps == 0:
           optimizer.step()
           optimizer.zero_grad()
   ```

### Debugging Tips

1. **Overfit a Single Batch**
   ```python
   def overfit_single_batch(model, train_loader, criterion, optimizer, device, epochs=100):
       """Overfit a single batch to verify model."""
       model.train()

       inputs, targets = next(iter(train_loader))
       inputs, targets = inputs.to(device), targets.to(device)

       for epoch in range(epochs):
           optimizer.zero_grad()
           outputs = model(inputs)
           loss = criterion(outputs, targets)
           loss.backward()
           optimizer.step()

           if epoch % 10 == 0:
               print(f"Epoch {epoch}, Loss: {loss.item():.4f}")
   ```

2. **Check for NaN in Gradients**
   ```python
   def check_nan_gradients(model):
       """Check for NaN in gradients."""
       for name, param in model.named_parameters():
           if param.grad is not None:
               if torch.isnan(param.grad).any():
                   print(f"NaN gradient found in {name}")
                   return True
       return False
   ```

3. **Monitor Gradient Norms**
   ```python
   def get_gradient_norm(model):
       """Calculate gradient norm."""
       total_norm = 0
       for p in model.parameters():
           if p.grad is not None:
               param_norm = p.grad.data.norm(2)
               total_norm += param_norm.item() ** 2
       total_norm = total_norm ** 0.5
       return total_norm
   ```

### Common Pitfalls

1. **Forgetting to Call model.eval() During Validation**
   ```python
   # WRONG:
   for inputs, targets in val_loader:
       outputs = model(inputs)  # Model is still in train mode!

   # CORRECT:
   model.eval()
   with torch.no_grad():
       for inputs, targets in val_loader:
           outputs = model(inputs)
   ```

2. **Not Using .to(device) Consistently**
   ```python
   # WRONG:
   inputs = inputs.to(device)
   outputs = model(inputs)  # Model might be on CPU!

   # CORRECT:
   model = model.to(device)
   inputs, targets = inputs.to(device), targets.to(device)
   outputs = model(inputs)
   ```

3. **Using Softmax Before CrossEntropyLoss**
   ```python
   # WRONG:
   outputs = model(inputs)
   outputs = torch.softmax(outputs, dim=1)
   loss = criterion(outputs, targets)  # Double softmax!

   # CORRECT:
   outputs = model(inputs)
   loss = criterion(outputs, targets)  # CrossEntropyLoss includes LogSoftmax
   ```

4. **Not Shuffling Training Data**
   ```python
   # WRONG:
   train_loader = DataLoader(dataset, batch_size=32, shuffle=False)

   # CORRECT:
   train_loader = DataLoader(dataset, batch_size=32, shuffle=True)
   ```

5. **Using Test Data for Hyperparameter Tuning**
   ```python
   # WRONG:
   # Tuning hyperparameters on test set leads to overfitting

   # CORRECT:
   # Use validation set for tuning, keep test set separate
   ```

### Performance Optimization

1. **Increase num_workers for Faster Data Loading**
   ```python
   train_loader = DataLoader(
       dataset,
       batch_size=32,
       num_workers=8,  # Increase based on CPU cores
       pin_memory=True  # Faster GPU transfer
   )
   ```

2. **Use Mixed Precision Training**
   ```python
   scaler = GradScaler()
   with autocast():
       outputs = model(inputs)
       loss = criterion(outputs, targets)
   scaler.scale(loss).backward()
   scaler.step(optimizer)
   scaler.update()
   ```

3. **Use Gradient Checkpointing for Memory Efficiency**
   ```python
   from torch.utils.checkpoint import checkpoint

   class CheckpointedModel(nn.Module):
       def forward(self, x):
           # Use checkpointing for memory-intensive layers
           x = checkpoint(self.layer1, x)
           x = checkpoint(self.layer2, x)
           return x
   ```

4. **Handle Out of Memory Issues**
   ```python
   # Option 1: Reduce batch size
   batch_size = 16  # Instead of 32

   # Option 2: Use gradient accumulation
   accumulation_steps = 4
   for i, (inputs, targets) in enumerate(train_loader):
       loss = criterion(model(inputs), targets) / accumulation_steps
       loss.backward()
       if (i + 1) % accumulation_steps == 0:
           optimizer.step()
           optimizer.zero_grad()
   ```

## Related Skills

- [`05-ai-ml-core/data-augmentation`](05-ai-ml-core/data-augmentation/SKILL.md)
- [`05-ai-ml-core/data-preprocessing`](05-ai-ml-core/data-preprocessing/SKILL.md)
- [`05-ai-ml-core/model-optimization`](05-ai-ml-core/model-optimization/SKILL.md)
- [`05-ai-ml-core/label-studio-setup`](05-ai-ml-core/label-studio-setup/SKILL.md)
- [`06-ai-ml-production/llm-integration`](06-ai-ml-production/llm-integration/SKILL.md)
