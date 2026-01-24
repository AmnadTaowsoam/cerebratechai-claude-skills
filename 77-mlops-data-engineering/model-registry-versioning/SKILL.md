---
name: Model Registry and Versioning
description: Centralized repository for managing ML model lifecycle, versions, artifacts, and deployment metadata at enterprise scale
---

# Model Registry and Versioning

> **Current Level:** Expert (Enterprise Scale)
> **Domain:** AI / MLOps / Data Engineering
> **Skill ID:** 93

---

## Overview
Model Registry is a centralized system for managing the complete lifecycle of machine learning models, including versioning, artifact storage, lineage tracking, and deployment metadata. It provides a single source of truth for all models across the organization, enabling reproducibility, governance, and controlled rollouts.

## Why This Matters / Strategic Necessity

### Context
In 2025-2026, enterprise ML organizations deploy hundreds to thousands of models across multiple environments. Without a proper model registry, teams struggle with model version confusion, inability to reproduce results, lack of audit trails, and difficulty in managing model promotions across environments.

### Business Impact
- **Reduced Deployment Risk:** 80% reduction in production incidents from wrong model versions
- **Faster Rollbacks:** 90% faster rollback times when issues are detected
- **Improved Compliance:** Complete audit trail for regulatory requirements (GDPR, SOC 2)
- **Team Efficiency:** 60% reduction in time spent tracking model versions manually

### Product Thinking
Solves the critical problem of "model chaos" where teams lose track of which model version is in production, cannot reproduce training results, and lack visibility into model lineage and dependencies.

## Core Concepts / Technical Deep Dive

### 1. Model Lifecycle Stages

**Development:** Initial model training and experimentation phase.

**Staging:** Model validation and testing in pre-production environment.

**Production:** Model deployed to production serving endpoints.

**Archived:** Model no longer in use but retained for audit purposes.

**Deprecated:** Model marked for removal after retention period.

**Stage Transition Rules:**
- Development → Staging: Requires passing validation tests
- Staging → Production: Requires approval and performance benchmarks
- Production → Archived: After replacement or end-of-life
- All transitions must be logged with approver and timestamp

### 2. Model Versioning Strategy

**Semantic Versioning:** MAJOR.MINOR.PATCH format
- MAJOR: Breaking changes in model architecture or API
- MINOR: New features or significant performance improvements
- PATCH: Bug fixes or minor parameter tweaks

**Git-Style Versioning:** Using commit hashes or timestamps
- Example: `model-abc123def` or `model-20250124-120000`
- Provides traceability to training code and data

**Immutable Artifacts:** Once a model is registered, it cannot be modified
- All changes create new versions
- Ensures reproducibility and auditability

### 3. Model Metadata and Lineage

**Essential Metadata:**
- Model name and version
- Training timestamp
- Training data version/hash
- Hyperparameters
- Performance metrics (accuracy, precision, recall, etc.)
- Framework and library versions
- Author and team
- Tags and labels
- Deployment status

**Lineage Tracking:**
- Training code version (Git commit)
- Feature store version
- Data pipeline version
- Dependencies and requirements
- Parent model (for transfer learning or fine-tuning)

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌─────────────┐
│   Training  │────▶│   Model      │────▶│   Staging   │────▶│ Production  │
│   Pipeline  │     │   Registry   │     │   Testing   │     │   Serving   │
└─────────────┘     └──────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌─────────────┐
│   Code      │     │   Artifacts  │     │   Metrics   │     │   Monitoring│
│   Version   │     │   Storage    │     │   Tracking  │     │   Alerts    │
└─────────────┘     └──────────────┘     └─────────────┘     └─────────────┘
```

## Tooling & Tech Stack

### Enterprise Tools
- **MLflow:** Open-source ML lifecycle platform with model registry
- **Weights & Biases:** Experiment tracking with model registry
- **Vertex AI Model Registry:** Google Cloud's managed model registry
- **SageMaker Model Registry:** AWS model management service
- **Azure ML Model Registry:** Microsoft's model registry solution
- **Databricks MLflow:** Managed MLflow on Databricks platform

### Configuration Essentials

```yaml
# MLflow model registry configuration
model_registry:
  backend_store: sqlite:///mlflow.db
  default_artifact_root: s3://ml-platform/artifacts
  
  # Stage definitions
  stages:
    - name: "development"
      description: "Initial development phase"
      can_deploy: false
    - name: "staging"
      description: "Pre-production testing"
      can_deploy: false
      requires_approval: true
    - name: "production"
      description: "Live production deployment"
      can_deploy: true
      requires_approval: true
      approvers: ["ml-team-lead", "data-science-manager"]
    - name: "archived"
      description: "Retired models"
      can_deploy: false
  
  # Versioning strategy
  versioning:
    strategy: "semantic"  # semantic, git, timestamp
    auto_increment: true
    
  # Retention policy
  retention:
    development_days: 30
    staging_days: 90
    production_days: 365
    archived_days: 1095  # 3 years
```

## Code Examples

### Good vs Bad Examples

```python
# ❌ Bad - No versioning, manual file management
def save_model(model):
    model.save("models/my_model.pkl")

def load_model():
    return joblib.load("models/my_model.pkl")

# ✅ Good - Using model registry with versioning
import mlflow

def register_model(model, model_name, metrics):
    with mlflow.start_run():
        # Log parameters and metrics
        mlflow.log_params(model.get_params())
        mlflow.log_metrics(metrics)
        
        # Log the model
        mlflow.sklearn.log_model(model, "model")
        
        # Register the model
        model_uri = f"runs:/{mlflow.active_run().info.run_id}/model"
        mlflow.register_model(model_uri, model_name)

def load_model(model_name, stage="production"):
    return mlflow.sklearn.load_model(f"models:/{model_name}/{stage}")
```

```python
# ❌ Bad - No lineage tracking, cannot reproduce
def train_and_save():
    model = train_model(data)
    model.save("model.pkl")

# ✅ Good - Complete lineage tracking
def train_and_register():
    with mlflow.start_run():
        # Track data version
        data_version = get_data_version()
        mlflow.log_param("data_version", data_version)
        
        # Track code version
        code_version = get_git_commit()
        mlflow.log_param("code_version", code_version)
        
        # Train and log
        model = train_model(data)
        mlflow.sklearn.log_model(model, "model")
        
        # Track dependencies
        mlflow.log_dict(get_requirements(), "requirements.txt")
        
        # Register with lineage
        register_model_with_lineage(model, data_version, code_version)
```

### Implementation Example

```python
"""
Production-ready Model Registry Implementation using MLflow
"""
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import mlflow
import mlflow.sklearn
import mlflow.pytorch
import mlflow.tensorflow
from mlflow.tracking import MlflowClient
from mlflow.entities.model_registry import ModelVersion
import logging
import json
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelStage(Enum):
    """Model lifecycle stages."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    ARCHIVED = "archived"
    DEPRECATED = "deprecated"


@dataclass
class ModelMetadata:
    """Metadata for a registered model."""
    model_name: str
    version: str
    stage: ModelStage
    created_at: datetime
    created_by: str
    description: str
    framework: str
    metrics: Dict[str, float]
    hyperparameters: Dict[str, Any]
    data_version: str
    code_version: str
    tags: Dict[str, str]
    parent_model: Optional[str] = None


class ModelRegistryManager:
    """
    Enterprise-grade model registry manager with comprehensive lifecycle management.
    """
    
    def __init__(
        self,
        tracking_uri: str = None,
        registry_uri: str = None,
        default_artifact_root: str = None
    ):
        """
        Initialize model registry manager.
        
        Args:
            tracking_uri: MLflow tracking server URI
            registry_uri: Model registry URI
            default_artifact_root: Default location for model artifacts
        """
        if tracking_uri:
            mlflow.set_tracking_uri(tracking_uri)
        if registry_uri:
            mlflow.set_registry_uri(registry_uri)
        
        self.client = MlflowClient()
        self.default_artifact_root = default_artifact_root
        
        logger.info(f"Model Registry initialized: tracking_uri={tracking_uri}, registry_uri={registry_uri}")
    
    def register_model(
        self,
        model,
        model_name: str,
        model_type: str = "sklearn",
        description: str = "",
        metrics: Dict[str, float] = None,
        hyperparameters: Dict[str, Any] = None,
        tags: Dict[str, str] = None,
        stage: ModelStage = ModelStage.DEVELOPMENT
    ) -> ModelVersion:
        """
        Register a new model version.
        
        Args:
            model: The trained model object
            model_name: Name for the registered model
            model_type: Type of model (sklearn, pytorch, tensorflow)
            description: Description of the model
            metrics: Performance metrics
            hyperparameters: Model hyperparameters
            tags: Additional tags
            stage: Initial stage for the model
            
        Returns:
            Registered model version
        """
        try:
            with mlflow.start_run():
                # Log hyperparameters
                if hyperparameters:
                    mlflow.log_params(hyperparameters)
                
                # Log metrics
                if metrics:
                    mlflow.log_metrics(metrics)
                
                # Log the model
                if model_type == "sklearn":
                    mlflow.sklearn.log_model(model, "model")
                elif model_type == "pytorch":
                    mlflow.pytorch.log_model(model, "model")
                elif model_type == "tensorflow":
                    mlflow.tensorflow.log_model(model, "model")
                else:
                    raise ValueError(f"Unsupported model type: {model_type}")
                
                # Register the model
                model_uri = f"runs:/{mlflow.active_run().info.run_id}/model"
                model_version = mlflow.register_model(
                    model_uri=model_uri,
                    name=model_name,
                    tags=tags
                )
                
                # Set initial stage
                self.client.transition_model_version_stage(
                    name=model_name,
                    version=model_version.version,
                    stage=stage.value
                )
                
                # Add description
                self.client.update_model_version(
                    name=model_name,
                    version=model_version.version,
                    description=description
                )
                
                logger.info(f"Model registered: {model_name} v{model_version.version}")
                return model_version
                
        except Exception as e:
            logger.error(f"Failed to register model: {e}")
            raise
    
    def get_model(
        self,
        model_name: str,
        stage: ModelStage = ModelStage.PRODUCTION,
        version: Optional[int] = None
    ):
        """
        Load a model from the registry.
        
        Args:
            model_name: Name of the model
            stage: Stage to load from (ignored if version is specified)
            version: Specific version to load (overrides stage)
            
        Returns:
            Loaded model object
        """
        try:
            if version:
                model_uri = f"models:/{model_name}/{version}"
            else:
                model_uri = f"models:/{model_name}/{stage.value}"
            
            model = mlflow.sklearn.load_model(model_uri)
            logger.info(f"Model loaded: {model_uri}")
            return model
            
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    
    def transition_stage(
        self,
        model_name: str,
        version: int,
        new_stage: ModelStage,
        description: str = ""
    ) -> None:
        """
        Transition a model to a new stage.
        
        Args:
            model_name: Name of the model
            version: Version number
            new_stage: Target stage
            description: Reason for transition
        """
        try:
            self.client.transition_model_version_stage(
                name=model_name,
                version=version,
                stage=new_stage.value,
                description=description
            )
            
            logger.info(f"Model transitioned: {model_name} v{version} -> {new_stage.value}")
            
        except Exception as e:
            logger.error(f"Failed to transition model: {e}")
            raise
    
    def get_model_metadata(
        self,
        model_name: str,
        version: int
    ) -> ModelMetadata:
        """
        Get comprehensive metadata for a model version.
        
        Args:
            model_name: Name of the model
            version: Version number
            
        Returns:
            ModelMetadata object
        """
        try:
            model_version = self.client.get_model_version(model_name, version)
            run = self.client.get_run(model_version.run_id)
            
            metadata = ModelMetadata(
                model_name=model_name,
                version=str(version),
                stage=ModelStage(model_version.current_stage),
                created_at=datetime.fromtimestamp(model_version.creation_timestamp / 1000),
                created_by=model_version.user_id,
                description=model_version.description,
                framework=run.data.tags.get("mlflow.model.flavor", "unknown"),
                metrics=run.data.metrics,
                hyperparameters=run.data.params,
                data_version=run.data.params.get("data_version", "unknown"),
                code_version=run.data.params.get("code_version", "unknown"),
                tags=run.data.tags
            )
            
            return metadata
            
        except Exception as e:
            logger.error(f"Failed to get model metadata: {e}")
            raise
    
    def list_model_versions(
        self,
        model_name: str,
        stage: Optional[ModelStage] = None
    ) -> List[ModelVersion]:
        """
        List all versions of a model.
        
        Args:
            model_name: Name of the model
            stage: Filter by stage (optional)
            
        Returns:
            List of model versions
        """
        try:
            filter_string = f"name='{model_name}'"
            if stage:
                filter_string += f" AND stage='{stage.value}'"
            
            versions = self.client.search_model_versions(filter_string)
            logger.info(f"Found {len(versions)} versions for {model_name}")
            return versions
            
        except Exception as e:
            logger.error(f"Failed to list model versions: {e}")
            raise
    
    def compare_models(
        self,
        model_name: str,
        version1: int,
        version2: int
    ) -> Dict[str, Any]:
        """
        Compare two model versions.
        
        Args:
            model_name: Name of the model
            version1: First version to compare
            version2: Second version to compare
            
        Returns:
            Comparison results
        """
        try:
            metadata1 = self.get_model_metadata(model_name, version1)
            metadata2 = self.get_model_metadata(model_name, version2)
            
            comparison = {
                "model_name": model_name,
                "version1": version1,
                "version2": version2,
                "metrics_diff": {},
                "hyperparameters_diff": {},
                "data_version_changed": metadata1.data_version != metadata2.data_version,
                "code_version_changed": metadata1.code_version != metadata2.code_version
            }
            
            # Compare metrics
            for metric in set(metadata1.metrics.keys()) | set(metadata2.metrics.keys()):
                val1 = metadata1.metrics.get(metric, 0)
                val2 = metadata2.metrics.get(metric, 0)
                comparison["metrics_diff"][metric] = {
                    "v1": val1,
                    "v2": val2,
                    "diff": val2 - val1,
                    "pct_change": ((val2 - val1) / abs(val1) * 100) if val1 != 0 else 0
                }
            
            # Compare hyperparameters
            for param in set(metadata1.hyperparameters.keys()) | set(metadata2.hyperparameters.keys()):
                val1 = metadata1.hyperparameters.get(param, None)
                val2 = metadata2.hyperparameters.get(param, None)
                comparison["hyperparameters_diff"][param] = {
                    "v1": val1,
                    "v2": val2,
                    "changed": val1 != val2
                }
            
            return comparison
            
        except Exception as e:
            logger.error(f"Failed to compare models: {e}")
            raise
    
    def archive_old_versions(
        self,
        model_name: str,
        keep_latest: int = 5,
        stage: ModelStage = ModelStage.DEVELOPMENT
    ) -> int:
        """
        Archive old model versions to reduce clutter.
        
        Args:
            model_name: Name of the model
            keep_latest: Number of latest versions to keep
            stage: Stage to archive from
            
        Returns:
            Number of versions archived
        """
        try:
            versions = self.list_model_versions(model_name, stage)
            versions.sort(key=lambda v: v.version, reverse=True)
            
            archived_count = 0
            for version in versions[keep_latest:]:
                self.transition_stage(
                    model_name=model_name,
                    version=version.version,
                    new_stage=ModelStage.ARCHIVED,
                    description=f"Auto-archived (keeping latest {keep_latest})"
                )
                archived_count += 1
            
            logger.info(f"Archived {archived_count} versions of {model_name}")
            return archived_count
            
        except Exception as e:
            logger.error(f"Failed to archive versions: {e}")
            raise
    
    def get_model_lineage(
        self,
        model_name: str,
        version: int
    ) -> Dict[str, Any]:
        """
        Get the complete lineage of a model.
        
        Args:
            model_name: Name of the model
            version: Version number
            
        Returns:
            Lineage information
        """
        try:
            metadata = self.get_model_metadata(model_name, version)
            
            lineage = {
                "model": {
                    "name": model_name,
                    "version": version,
                    "stage": metadata.stage.value
                },
                "training": {
                    "data_version": metadata.data_version,
                    "code_version": metadata.code_version,
                    "created_at": metadata.created_at.isoformat(),
                    "created_by": metadata.created_by
                },
                "performance": metadata.metrics,
                "hyperparameters": metadata.hyperparameters
            }
            
            # Get parent model if exists
            if metadata.parent_model:
                lineage["parent_model"] = metadata.parent_model
            
            return lineage
            
        except Exception as e:
            logger.error(f"Failed to get model lineage: {e}")
            raise


# Example usage
if __name__ == "__main__":
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.datasets import make_classification
    import numpy as np
    
    # Initialize registry manager
    registry = ModelRegistryManager(
        tracking_uri="sqlite:///mlflow.db",
        default_artifact_root="./artifacts"
    )
    
    # Train a model
    X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X, y)
    
    # Evaluate
    accuracy = model.score(X, y)
    
    # Register the model
    registered = registry.register_model(
        model=model,
        model_name="fraud_detection",
        model_type="sklearn",
        description="Random Forest for fraud detection",
        metrics={"accuracy": accuracy, "n_estimators": 100},
        hyperparameters=model.get_params(),
        tags={"team": "fraud", "priority": "high"},
        stage=ModelStage.DEVELOPMENT
    )
    
    print(f"Registered model: fraud_detection v{registered.version}")
    
    # Transition to staging
    registry.transition_stage(
        model_name="fraud_detection",
        version=registered.version,
        new_stage=ModelStage.STAGING,
        description="Passed validation tests"
    )
    
    # Get model metadata
    metadata = registry.get_model_metadata("fraud_detection", registered.version)
    print(f"Model stage: {metadata.stage.value}")
    print(f"Accuracy: {metadata.metrics.get('accuracy')}")
    
    # Load model for inference
    loaded_model = registry.get_model("fraud_detection", stage=ModelStage.STAGING)
    predictions = loaded_model.predict(X[:5])
    print(f"Predictions: {predictions}")
```

## Standards, Compliance & Security

### International Standards
- **ISO/IEC 27001:** Security of model artifacts and metadata
- **GDPR:** Right to explanation and data minimization for model decisions
- **SOC 2 Type II:** Auditability and integrity of model lifecycle
- **Model Risk Management (SR 11-7):** Financial industry model governance standards

### Security Protocol
- **Artifact Encryption:** Encrypt model artifacts at rest and in transit
- **Access Control:** Role-based access for model registration and deployment
- **Audit Logging:** Complete audit trail of all model operations
- **Digital Signatures:** Sign model artifacts for integrity verification
- **Secrets Management:** Secure storage of API keys and credentials

### Explainability
- **Model Documentation:** Auto-generated documentation for each model version
- **Performance Tracking:** Historical performance metrics across versions
- **Change Logs:** Detailed changelog between model versions
- **Impact Analysis:** Tools to assess impact of model changes

## Quick Start

1. **Install MLflow:**
   ```bash
   pip install mlflow
   ```

2. **Start MLflow tracking server:**
   ```bash
   mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./artifacts
   ```

3. **Register a model:**
   ```python
   import mlflow
   
   with mlflow.start_run():
       mlflow.log_params({"n_estimators": 100})
       mlflow.log_metrics({"accuracy": 0.95})
       mlflow.sklearn.log_model(model, "model")
       mlflow.register_model("runs:/<run-id>/model", "my_model")
   ```

4. **Load model from registry:**
   ```python
   model = mlflow.sklearn.load_model("models:/my_model/production")
   ```

## Production Checklist

- [ ] MLflow tracking server is deployed and highly available
- [ ] Artifact storage is configured with appropriate backup
- [ ] Access control policies are implemented
- [ ] Model stages are defined and documented
- [ ] Approval workflows for production deployments
- [ ] Automated testing before stage transitions
- [ ] Monitoring and alerting for model performance
- [ ] Retention policies for old model versions
- [ ] Backup and disaster recovery procedures
- [ ] Integration with CI/CD pipelines

## Anti-patterns

1. **Skipping Versioning:** Overwriting model files instead of versioning
   - **Why it's bad:** Cannot reproduce results or rollback issues
   - **Solution:** Always use model registry with immutable versions

2. **Missing Lineage:** Not tracking data and code versions
   - **Why it's bad:** Cannot reproduce training conditions
   - **Solution:** Log all dependencies and versions with each model

3. **No Stage Gating:** Direct deployment to production without validation
   - **Why it's bad:** Increases risk of production issues
   - **Solution:** Implement stage transitions with required approvals

4. **Ignoring Old Models:** Keeping all versions indefinitely
   - **Why it's bad:** Increases storage costs and confusion
   - **Solution:** Implement retention policies and archive old versions

## Unit Economics & KPIs

### Cost Calculation
```
Total Registry Cost = Storage Cost + Compute Cost + Operational Cost

Storage Cost = (Model Size × Version Count × Retention Period) × Storage Rate
Compute Cost = (Registry Operations × Compute Resources) × Compute Rate
Operational Cost = (Monitoring + Maintenance + Support)
```

### Key Performance Indicators
- **Registration Time:** < 30 seconds per model registration
- **Model Retrieval Time:** < 5 seconds for model loading
- **Stage Transition Time:** < 1 hour for approval workflow
- **Storage Efficiency:** Compression ratio > 50% for model artifacts
- **Audit Trail Completeness:** 100% of operations logged

## Integration Points / Related Skills
- [Feature Store Implementation](../77-mlops-data-engineering/feature-store-implementation/SKILL.md) - For tracking feature versions used in training
- [Drift Detection Retraining](../77-mlops-data-engineering/drift-detection-retraining/SKILL.md) - For triggering retraining based on drift
- [Experiment Tracking](../77-mlops-data-engineering/experiment-tracking/SKILL.md) - For linking experiments to registered models
- [Continuous Training Pipelines](../77-mlops-data-engineering/continuous-training-pipelines/SKILL.md) - For automated model registration

## Further Reading
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [Weights & Biases Model Registry](https://docs.wandb.ai/guides/artifacts/model_registry)
- [Google Cloud Vertex AI Model Registry](https://cloud.google.com/vertex-ai/docs/model-registry)
- [AWS SageMaker Model Registry](https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry.html)
- [Model Management in MLOps](https://arxiv.org/abs/2005.03138)
