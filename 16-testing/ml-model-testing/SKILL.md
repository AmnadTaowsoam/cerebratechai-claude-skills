# ML Model Testing

## Overview

ML model testing ensures machine learning models perform correctly and reliably. This skill covers model testing types, training pipeline testing, inference testing, data validation, performance tests, regression tests, A/B testing, shadow testing, and production monitoring.

## Table of Contents

1. [Model Testing Types](#model-testing-types)
2. [Testing Training Pipeline](#testing-training-pipeline)
3. [Testing Inference](#testing-inference)
4. [Data Validation](#data-validation)
5. [Model Performance Tests](#model-performance-tests)
6. [Regression Tests](#regression-tests)
7. [A/B Testing](#ab-testing)
8. [Shadow Testing](#shadow-testing)
9. [Monitoring in Production](#monitoring-in-production)
10. [Best Practices](#best-practices)

---

## Model Testing Types

### Unit Tests

```python
# test/unit/model_test.py
import pytest
import numpy as np
from src.models import MyModel

def test_model_initialization():
    """Test model initialization."""
    model = MyModel(input_dim=10, hidden_dim=20, output_dim=5)
    assert model.input_dim == 10
    assert model.hidden_dim == 20
    assert model.output_dim == 5

def test_model_forward_pass():
    """Test model forward pass."""
    model = MyModel(input_dim=10, hidden_dim=20, output_dim=5)
    x = np.random.randn(3, 10)  # Batch of 3 samples
    output = model.forward(x)
    
    assert output.shape == (3, 5)
    assert not np.any(np.isnan(output))
    assert not np.any(np.isinf(output))

def test_model_gradient_flow():
    """Test gradient flow through model."""
    model = MyModel(input_dim=10, hidden_dim=20, output_dim=5)
    x = np.random.randn(3, 10)
    y = np.random.randn(3, 5)
    
    loss = model.compute_loss(x, y)
    gradients = model.compute_gradients(x, y)
    
    assert loss > 0
    assert all(g is not None for g in gradients)
    assert all(not np.any(np.isnan(g)) for g in gradients)
```

### Integration Tests

```python
# test/integration/pipeline_test.py
import pytest
from src.pipeline import TrainingPipeline
from src.data import DataLoader

def test_full_training_pipeline():
    """Test complete training pipeline."""
    # Setup
    config = {
        'epochs': 2,
        'batch_size': 32,
        'learning_rate': 0.001,
    }
    
    pipeline = TrainingPipeline(config)
    data_loader = DataLoader('test-data.csv')
    
    # Run pipeline
    model = pipeline.train(data_loader)
    
    # Verify
    assert model is not None
    assert hasattr(model, 'predict')
    assert hasattr(model, 'evaluate')

def test_pipeline_with_validation():
    """Test pipeline with validation data."""
    config = {
        'epochs': 5,
        'batch_size': 32,
        'learning_rate': 0.001,
        'validation_split': 0.2,
    }
    
    pipeline = TrainingPipeline(config)
    data_loader = DataLoader('test-data.csv')
    
    history = pipeline.train(data_loader)
    
    assert 'train_loss' in history
    assert 'val_loss' in history
    assert len(history['train_loss']) == config['epochs']
```

### Model Validation Tests

```python
# test/validation/model_validation_test.py
import pytest
import numpy as np
from src.validation import ModelValidator

def test_model_accuracy():
    """Test model accuracy."""
    model = MyModel()
    validator = ModelValidator(model)
    
    X_test, y_test = load_test_data()
    accuracy = validator.evaluate_accuracy(X_test, y_test)
    
    assert accuracy >= 0.8  # Minimum acceptable accuracy

def test_model_precision_recall():
    """Test model precision and recall."""
    model = MyModel()
    validator = ModelValidator(model)
    
    X_test, y_test = load_test_data()
    metrics = validator.evaluate_classification(X_test, y_test)
    
    assert metrics['precision'] >= 0.75
    assert metrics['recall'] >= 0.75

def test_model_calibration():
    """Test model calibration."""
    model = MyModel()
    validator = ModelValidator(model)
    
    X_test, y_test = load_test_data()
    calibration = validator.evaluate_calibration(X_test, y_test)
    
    assert calibration['expected_calibration_error'] < 0.1
```

---

## Testing Training Pipeline

### Data Loading Tests

```python
# test/pipeline/data_loading_test.py
import pytest
import pandas as pd
from src.data import DataLoader

def test_data_loading():
    """Test data loading functionality."""
    loader = DataLoader('test-data.csv')
    data = loader.load()
    
    assert isinstance(data, pd.DataFrame)
    assert len(data) > 0
    assert not data.isnull().all().any()

def test_data_splitting():
    """Test train/validation/test splitting."""
    loader = DataLoader('test-data.csv')
    train, val, test = loader.split(train_ratio=0.7, val_ratio=0.15)
    
    assert len(train) > 0
    assert len(val) > 0
    assert len(test) > 0
    assert len(train) + len(val) + len(test) == len(loader.load())

def test_data_preprocessing():
    """Test data preprocessing."""
    loader = DataLoader('test-data.csv')
    data = loader.load()
    processed = loader.preprocess(data)
    
    assert processed.isnull().sum().sum() == 0
    assert processed.dtypes.apply(lambda x: x in [np.float64, np.int64]).all()
```

### Feature Engineering Tests

```python
# test/pipeline/feature_engineering_test.py
import pytest
import numpy as np
from src.features import FeatureEngineer

def test_feature_extraction():
    """Test feature extraction."""
    engineer = FeatureEngineer()
    data = load_sample_data()
    features = engineer.extract_features(data)
    
    assert features.shape[0] == len(data)
    assert features.shape[1] > 0
    assert not np.any(np.isnan(features))

def test_feature_scaling():
    """Test feature scaling."""
    engineer = FeatureEngineer()
    data = load_sample_data()
    features = engineer.extract_features(data)
    scaled = engineer.scale_features(features)
    
    assert np.allclose(scaled.mean(), 0, atol=1e-6)
    assert np.allclose(scaled.std(), 1, atol=1e-6)

def test_feature_selection():
    """Test feature selection."""
    engineer = FeatureEngineer()
    data = load_sample_data()
    features = engineer.extract_features(data)
    selected = engineer.select_features(features, n_features=10)
    
    assert selected.shape[1] == 10
```

### Training Process Tests

```python
# test/pipeline/training_test.py
import pytest
from src.pipeline import TrainingPipeline

def test_training_convergence():
    """Test that training converges."""
    config = {
        'epochs': 50,
        'batch_size': 32,
        'learning_rate': 0.001,
        'early_stopping': True,
        'patience': 5,
    }
    
    pipeline = TrainingPipeline(config)
    data_loader = DataLoader('test-data.csv')
    
    history = pipeline.train(data_loader)
    
    # Loss should decrease
    assert history['train_loss'][0] > history['train_loss'][-1]
    
    # Early stopping should work
    if config['early_stopping']:
        assert len(history['train_loss']) <= config['epochs']

def test_training_with_checkpointing():
    """Test training with checkpointing."""
    config = {
        'epochs': 10,
        'checkpoint_dir': './checkpoints',
        'checkpoint_frequency': 2,
    }
    
    pipeline = TrainingPipeline(config)
    data_loader = DataLoader('test-data.csv')
    
    pipeline.train(data_loader)
    
    # Check checkpoints exist
    import os
    checkpoints = os.listdir(config['checkpoint_dir'])
    assert len(checkpoints) > 0

def test_training_with_logging():
    """Test training with logging."""
    config = {
        'epochs': 5,
        'log_dir': './logs',
    }
    
    pipeline = TrainingPipeline(config)
    data_loader = DataLoader('test-data.csv')
    
    pipeline.train(data_loader)
    
    # Check logs exist
    import os
    assert os.path.exists(config['log_dir'])
```

---

## Testing Inference

### Prediction Tests

```python
# test/inference/prediction_test.py
import pytest
import numpy as np
from src.models import MyModel

def test_single_prediction():
    """Test single prediction."""
    model = MyModel()
    model.load('model.h5')
    
    x = np.random.randn(10)
    prediction = model.predict(x)
    
    assert prediction is not None
    assert not np.isnan(prediction)
    assert not np.isinf(prediction)

def test_batch_prediction():
    """Test batch prediction."""
    model = MyModel()
    model.load('model.h5')
    
    X = np.random.randn(100, 10)
    predictions = model.predict_batch(X)
    
    assert predictions.shape == (100,)
    assert not np.any(np.isnan(predictions))
    assert not np.any(np.isinf(predictions))

def test_prediction_consistency():
    """Test prediction consistency."""
    model = MyModel()
    model.load('model.h5')
    
    x = np.random.randn(10)
    prediction1 = model.predict(x)
    prediction2 = model.predict(x)
    
    assert np.allclose(prediction1, prediction2)
```

### Inference Performance Tests

```python
# test/inference/performance_test.py
import pytest
import time
import numpy as np
from src.models import MyModel

def test_inference_latency():
    """Test inference latency."""
    model = MyModel()
    model.load('model.h5')
    
    x = np.random.randn(10)
    
    start_time = time.time()
    for _ in range(100):
        model.predict(x)
    end_time = time.time()
    
    avg_latency = (end_time - start_time) / 100
    assert avg_latency < 0.1  # 100ms per prediction

def test_batch_inference_throughput():
    """Test batch inference throughput."""
    model = MyModel()
    model.load('model.h5')
    
    X = np.random.randn(1000, 10)
    
    start_time = time.time()
    predictions = model.predict_batch(X)
    end_time = time.time()
    
    throughput = len(X) / (end_time - start_time)
    assert throughput > 100  # 100 predictions per second
```

### Edge Case Tests

```python
# test/inference/edge_cases_test.py
import pytest
import numpy as np
from src.models import MyModel

def test_empty_input():
    """Test handling of empty input."""
    model = MyModel()
    model.load('model.h5')
    
    with pytest.raises(ValueError):
        model.predict(np.array([]))

def test_out_of_range_input():
    """Test handling of out-of-range input."""
    model = MyModel()
    model.load('model.h5')
    
    x = np.random.randn(10) * 1000  # Very large values
    prediction = model.predict(x)
    
    assert not np.isnan(prediction)
    assert not np.isinf(prediction)

def test_missing_values():
    """Test handling of missing values."""
    model = MyModel()
    model.load('model.h5')
    
    x = np.random.randn(10)
    x[0] = np.nan  # Missing value
    
    with pytest.raises(ValueError):
        model.predict(x)
```

---

## Data Validation

### Great Expectations

```python
# test/validation/great_expectations_test.py
import great_expectations as ge
from great_expectations.core import ExpectationSuite, ExpectationConfiguration

def test_data_expectations():
    """Test data using Great Expectations."""
    df = ge.read_csv('test-data.csv')
    
    # Create expectation suite
    suite = ExpectationSuite(expectation_suite_name='test_data_suite')
    
    # Add expectations
    suite.add_expectation(
        ExpectationConfiguration(
            expectation_type='expect_column_to_exist',
            kwargs={'column': 'feature_1'}
        )
    )
    
    suite.add_expectation(
        ExpectationConfiguration(
            expectation_type='expect_column_values_to_not_be_null',
            kwargs={'column': 'feature_1'}
        )
    )
    
    suite.add_expectation(
        ExpectationConfiguration(
            expectation_type='expect_column_values_to_be_between',
            kwargs={'column': 'feature_1', 'min_value': 0, 'max_value': 100}
        )
    )
    
    # Validate data
    results = df.validate(suite)
    
    assert results['success']

def test_data_drift_detection():
    """Test data drift detection."""
    reference_data = ge.read_csv('reference-data.csv')
    current_data = ge.read_csv('current-data.csv')
    
    # Compare distributions
    for column in reference_data.columns:
        reference_mean = reference_data[column].mean()
        current_mean = current_data[column].mean()
        
        # Check for significant drift
        drift = abs(reference_mean - current_mean) / reference_mean
        assert drift < 0.1  # Less than 10% drift
```

### Schema Validation

```python
# test/validation/schema_test.py
import pytest
import pandas as pd
from pandera import DataFrameSchema, Column, Check

def test_data_schema():
    """Test data schema validation."""
    schema = DataFrameSchema({
        'id': Column(int, Check(lambda x: x > 0)),
        'feature_1': Column(float, Check(lambda x: x >= 0)),
        'feature_2': Column(float, Check(lambda x: x >= 0)),
        'target': Column(int, Check.isin([0, 1])),
    })
    
    df = pd.read_csv('test-data.csv')
    validated_df = schema.validate(df)
    
    assert len(validated_df) == len(df)

def test_data_type_validation():
    """Test data type validation."""
    df = pd.read_csv('test-data.csv')
    
    assert df['id'].dtype == 'int64'
    assert df['feature_1'].dtype == 'float64'
    assert df['target'].dtype == 'int64'
```

---

## Model Performance Tests

### Accuracy Tests

```python
# test/performance/accuracy_test.py
import pytest
import numpy as np
from src.models import MyModel
from src.metrics import MetricsCalculator

def test_model_accuracy():
    """Test model accuracy on test set."""
    model = MyModel()
    model.load('model.h5')
    
    X_test, y_test = load_test_data()
    y_pred = model.predict(X_test)
    
    metrics = MetricsCalculator()
    accuracy = metrics.accuracy(y_test, y_pred)
    
    assert accuracy >= 0.85  # Minimum acceptable accuracy

def test_model_precision():
    """Test model precision."""
    model = MyModel()
    model.load('model.h5')
    
    X_test, y_test = load_test_data()
    y_pred = model.predict(X_test)
    
    metrics = MetricsCalculator()
    precision = metrics.precision(y_test, y_pred)
    
    assert precision >= 0.80

def test_model_recall():
    """Test model recall."""
    model = MyModel()
    model.load('model.h5')
    
    X_test, y_test = load_test_data()
    y_pred = model.predict(X_test)
    
    metrics = MetricsCalculator()
    recall = metrics.recall(y_test, y_pred)
    
    assert recall >= 0.80
```

### F1 Score Tests

```python
# test/performance/f1_score_test.py
import pytest
from src.models import MyModel
from src.metrics import MetricsCalculator

def test_f1_score():
    """Test F1 score."""
    model = MyModel()
    model.load('model.h5')
    
    X_test, y_test = load_test_data()
    y_pred = model.predict(X_test)
    
    metrics = MetricsCalculator()
    f1 = metrics.f1_score(y_test, y_pred)
    
    assert f1 >= 0.80

def test_f1_score_per_class():
    """Test F1 score per class."""
    model = MyModel()
    model.load('model.h5')
    
    X_test, y_test = load_test_data()
    y_pred = model.predict(X_test)
    
    metrics = MetricsCalculator()
    f1_per_class = metrics.f1_score_per_class(y_test, y_pred)
    
    for class_f1 in f1_per_class.values():
        assert class_f1 >= 0.75
```

### ROC AUC Tests

```python
# test/performance/roc_auc_test.py
import pytest
from src.models import MyModel
from src.metrics import MetricsCalculator

def test_roc_auc():
    """Test ROC AUC score."""
    model = MyModel()
    model.load('model.h5')
    
    X_test, y_test = load_test_data()
    y_proba = model.predict_proba(X_test)
    
    metrics = MetricsCalculator()
    roc_auc = metrics.roc_auc(y_test, y_proba)
    
    assert roc_auc >= 0.85

def test_pr_auc():
    """Test Precision-Recall AUC."""
    model = MyModel()
    model.load('model.h5')
    
    X_test, y_test = load_test_data()
    y_proba = model.predict_proba(X_test)
    
    metrics = MetricsCalculator()
    pr_auc = metrics.pr_auc(y_test, y_proba)
    
    assert pr_auc >= 0.80
```

---

## Regression Tests

### Model Performance Regression

```python
# test/regression/performance_regression_test.py
import pytest
import json
from src.models import MyModel
from src.metrics import MetricsCalculator

def test_performance_regression():
    """Test that model performance hasn't regressed."""
    # Load baseline metrics
    with open('baseline_metrics.json', 'r') as f:
        baseline = json.load(f)
    
    # Evaluate current model
    model = MyModel()
    model.load('model.h5')
    
    X_test, y_test = load_test_data()
    y_pred = model.predict(X_test)
    
    metrics = MetricsCalculator()
    current_accuracy = metrics.accuracy(y_test, y_pred)
    
    # Check for regression
    regression_threshold = 0.02  # 2% regression allowed
    assert current_accuracy >= baseline['accuracy'] - regression_threshold

def test_performance_improvement():
    """Test that model has improved over baseline."""
    # Load baseline metrics
    with open('baseline_metrics.json', 'r') as f:
        baseline = json.load(f)
    
    # Evaluate current model
    model = MyModel()
    model.load('model.h5')
    
    X_test, y_test = load_test_data()
    y_pred = model.predict(X_test)
    
    metrics = MetricsCalculator()
    current_f1 = metrics.f1_score(y_test, y_pred)
    
    # Check for improvement
    improvement_threshold = 0.01  # 1% improvement expected
    assert current_f1 >= baseline['f1_score'] + improvement_threshold
```

### Prediction Consistency Tests

```python
# test/regression/prediction_consistency_test.py
import pytest
import numpy as np
from src.models import MyModel

def test_prediction_consistency_across_versions():
    """Test predictions are consistent across model versions."""
    # Load old model
    old_model = MyModel()
    old_model.load('model_v1.h5')
    
    # Load new model
    new_model = MyModel()
    new_model.load('model_v2.h5')
    
    # Test on same data
    X_test = load_test_data()[0]
    
    old_predictions = old_model.predict(X_test)
    new_predictions = new_model.predict(X_test)
    
    # Check that predictions are similar
    similarity = np.mean(np.abs(old_predictions - new_predictions) < 0.1)
    assert similarity >= 0.95  # 95% of predictions should be similar
```

---

## A/B Testing

### A/B Test Setup

```python
# test/ab_testing/ab_test_setup.py
import pytest
import numpy as np
from src.models import ModelA, ModelB
from src.ab_testing import ABTest

def test_ab_test_setup():
    """Test A/B test setup."""
    ab_test = ABTest(
        model_a=ModelA(),
        model_b=ModelB(),
        traffic_split=0.5,  # 50/50 split
    )
    
    # Verify setup
    assert ab_test.model_a is not None
    assert ab_test.model_b is not None
    assert ab_test.traffic_split == 0.5

def test_ab_test_routing():
    """Test A/B test traffic routing."""
    ab_test = ABTest(
        model_a=ModelA(),
        model_b=ModelB(),
        traffic_split=0.5,
    )
    
    # Test routing
    X_test = load_test_data()[0]
    
    # Route 100 requests
    model_a_count = 0
    model_b_count = 0
    
    for x in X_test[:100]:
        model = ab_test.route(x)
        if model == 'A':
            model_a_count += 1
        else:
            model_b_count += 1
    
    # Check roughly 50/50 split
    assert 40 <= model_a_count <= 60
    assert 40 <= model_b_count <= 60
```

### A/B Test Analysis

```python
# test/ab_testing/ab_test_analysis.py
import pytest
from src.ab_testing import ABTestAnalyzer

def test_ab_test_significance():
    """Test A/B test statistical significance."""
    analyzer = ABTestAnalyzer()
    
    # Mock results
    results_a = {
        'conversions': 100,
        'total': 1000,
    }
    
    results_b = {
        'conversions': 120,
        'total': 1000,
    }
    
    # Calculate significance
    p_value = analyzer.calculate_significance(results_a, results_b)
    
    # Check significance
    assert p_value < 0.05  # Significant difference

def test_ab_test_winner():
    """Test A/B test winner determination."""
    analyzer = ABTestAnalyzer()
    
    # Mock results
    results_a = {
        'conversions': 100,
        'total': 1000,
    }
    
    results_b = {
        'conversions': 120,
        'total': 1000,
    }
    
    # Determine winner
    winner = analyzer.determine_winner(results_a, results_b)
    
    assert winner == 'B'
```

---

## Shadow Testing

### Shadow Test Setup

```python
# test/shadow_testing/shadow_test_setup.py
import pytest
from src.models import ProductionModel, CandidateModel
from src.shadow_testing import ShadowTester

def test_shadow_test_setup():
    """Test shadow testing setup."""
    shadow_tester = ShadowTester(
        production_model=ProductionModel(),
        candidate_model=CandidateModel(),
    )
    
    # Verify setup
    assert shadow_tester.production_model is not None
    assert shadow_tester.candidate_model is not None

def test_shadow_test_predictions():
    """Test shadow testing predictions."""
    shadow_tester = ShadowTester(
        production_model=ProductionModel(),
        candidate_model=CandidateModel(),
    )
    
    # Get predictions
    X_test = load_test_data()[0]
    
    production_predictions = shadow_tester.production_model.predict(X_test)
    candidate_predictions = shadow_tester.candidate_model.predict(X_test)
    
    # Verify predictions
    assert production_predictions is not None
    assert candidate_predictions is not None
    assert len(production_predictions) == len(candidate_predictions)
```

### Shadow Test Analysis

```python
# test/shadow_testing/shadow_test_analysis.py
import pytest
import numpy as np
from src.shadow_testing import ShadowTestAnalyzer

def test_shadow_test_agreement():
    """Test shadow test agreement between models."""
    analyzer = ShadowTestAnalyzer()
    
    # Mock predictions
    production_predictions = np.array([0, 1, 0, 1, 0])
    candidate_predictions = np.array([0, 1, 1, 1, 0])
    
    # Calculate agreement
    agreement = analyzer.calculate_agreement(
        production_predictions,
        candidate_predictions
    )
    
    # Check agreement
    assert agreement >= 0.8  # 80% agreement

def test_shadow_test_improvement():
    """Test shadow test improvement."""
    analyzer = ShadowTestAnalyzer()
    
    # Mock predictions and ground truth
    production_predictions = np.array([0, 1, 0, 1, 0])
    candidate_predictions = np.array([0, 1, 1, 1, 0])
    ground_truth = np.array([0, 1, 1, 1, 0])
    
    # Calculate improvement
    improvement = analyzer.calculate_improvement(
        production_predictions,
        candidate_predictions,
        ground_truth
    )
    
    # Check improvement
    assert improvement > 0  # Candidate model is better
```

---

## Monitoring in Production

### Performance Monitoring

```python
# test/monitoring/performance_monitoring_test.py
import pytest
from src.monitoring import ModelMonitor

def test_model_performance_monitoring():
    """Test model performance monitoring."""
    monitor = ModelMonitor(
        model=MyModel(),
        threshold=0.8,  # Minimum acceptable accuracy
    )
    
    # Simulate predictions
    X_test, y_test = load_test_data()
    y_pred = monitor.model.predict(X_test)
    
    # Monitor performance
    performance = monitor.monitor(y_test, y_pred)
    
    # Check performance
    assert performance['accuracy'] >= monitor.threshold

def test_model_drift_detection():
    """Test model drift detection."""
    monitor = ModelMonitor(
        model=MyModel(),
        drift_threshold=0.1,  # 10% drift threshold
    )
    
    # Simulate drift
    reference_data = load_reference_data()
    current_data = load_current_data()
    
    # Detect drift
    drift_detected = monitor.detect_drift(reference_data, current_data)
    
    # Check drift detection
    if drift_detected:
        print('Drift detected!')
```

### Data Drift Monitoring

```python
# test/monitoring/data_drift_monitoring_test.py
import pytest
from src.monitoring import DataDriftMonitor

def test_data_drift_monitoring():
    """Test data drift monitoring."""
    monitor = DataDriftMonitor(
        reference_data=load_reference_data(),
        drift_threshold=0.1,  # 10% drift threshold
    )
    
    # Monitor current data
    current_data = load_current_data()
    drift_detected = monitor.monitor(current_data)
    
    # Check drift detection
    assert isinstance(drift_detected, bool)

def test_feature_drift_monitoring():
    """Test feature drift monitoring."""
    monitor = DataDriftMonitor(
        reference_data=load_reference_data(),
        drift_threshold=0.1,
    )
    
    # Monitor current data
    current_data = load_current_data()
    feature_drift = monitor.monitor_features(current_data)
    
    # Check feature drift
    for feature, drift in feature_drift.items():
        assert drift < monitor.drift_threshold
```

---

## Best Practices

### 1. Test Data Quality

```python
# Good: Test data quality
def test_data_quality():
    """Test data quality."""
    data = load_test_data()
    
    # Check for missing values
    assert not data.isnull().any().any()
    
    # Check for duplicates
    assert not data.duplicated().any()
    
    # Check for outliers
    for column in data.select_dtypes(include=[np.number]).columns:
        q1 = data[column].quantile(0.25)
        q3 = data[column].quantile(0.75)
        iqr = q3 - q1
        outliers = data[(data[column] < q1 - 1.5 * iqr) | (data[column] > q3 + 1.5 * iqr)]
        assert len(outliers) < len(data) * 0.05  # Less than 5% outliers

# Bad: No data quality checks
def test_data_loading():
    """Test data loading."""
    data = load_test_data()
    assert len(data) > 0
```

### 2. Test Model Robustness

```python
# Good: Test model robustness
def test_model_robustness():
    """Test model robustness to noise."""
    model = MyModel()
    model.load('model.h5')
    
    X_test, y_test = load_test_data()
    
    # Add noise
    noisy_X = X_test + np.random.normal(0, 0.1, X_test.shape)
    
    # Test predictions
    clean_predictions = model.predict(X_test)
    noisy_predictions = model.predict(noisy_X)
    
    # Check robustness
    similarity = np.mean(np.abs(clean_predictions - noisy_predictions) < 0.1)
    assert similarity >= 0.9  # 90% similarity

# Bad: No robustness testing
def test_model_predictions():
    """Test model predictions."""
    model = MyModel()
    model.load('model.h5')
    
    X_test = load_test_data()[0]
    predictions = model.predict(X_test)
    
    assert predictions is not None
```

### 3. Test Model Fairness

```python
# Good: Test model fairness
def test_model_fairness():
    """Test model fairness across groups."""
    model = MyModel()
    model.load('model.h5')
    
    X_test, y_test = load_test_data()
    
    # Group by protected attribute
    group_a = X_test[X_test['protected_attribute'] == 0]
    group_b = X_test[X_test['protected_attribute'] == 1]
    
    # Evaluate each group
    metrics = MetricsCalculator()
    accuracy_a = metrics.accuracy(y_test[group_a.index], model.predict(group_a))
    accuracy_b = metrics.accuracy(y_test[group_b.index], model.predict(group_b))
    
    # Check fairness
    fairness_threshold = 0.05  # 5% difference allowed
    assert abs(accuracy_a - accuracy_b) < fairness_threshold

# Bad: No fairness testing
def test_model_accuracy():
    """Test model accuracy."""
    model = MyModel()
    model.load('model.h5')
    
    X_test, y_test = load_test_data()
    y_pred = model.predict(X_test)
    
    metrics = MetricsCalculator()
    accuracy = metrics.accuracy(y_test, y_pred)
    
    assert accuracy >= 0.8
```

### 4. Test Model Explainability

```python
# Good: Test model explainability
def test_model_explainability():
    """Test model explainability."""
    model = MyModel()
    model.load('model.h5')
    
    X_test = load_test_data()[0]
    
    # Get feature importance
    importance = model.get_feature_importance(X_test)
    
    # Check explainability
    assert importance is not None
    assert len(importance) > 0
    assert all(0 <= imp <= 1 for imp in importance)

# Bad: No explainability testing
def test_model_predictions():
    """Test model predictions."""
    model = MyModel()
    model.load('model.h5')
    
    X_test = load_test_data()[0]
    predictions = model.predict(X_test)
    
    assert predictions is not None
```

### 5. Test Model Deployment

```python
# Good: Test model deployment
def test_model_deployment():
    """Test model deployment."""
    from src.deployment import ModelDeployment
    
    deployment = ModelDeployment(model_path='model.h5')
    
    # Test deployment
    X_test = load_test_data()[0]
    predictions = deployment.predict(X_test)
    
    # Verify deployment
    assert predictions is not None
    assert len(predictions) == len(X_test)

# Bad: No deployment testing
def test_model_predictions():
    """Test model predictions."""
    model = MyModel()
    model.load('model.h5')
    
    X_test = load_test_data()[0]
    predictions = model.predict(X_test)
    
    assert predictions is not None
```

---

## Summary

This skill covers comprehensive ML model testing patterns including:

- **Model Testing Types**: Unit tests, integration tests, model validation tests
- **Testing Training Pipeline**: Data loading, feature engineering, training process tests
- **Testing Inference**: Prediction tests, inference performance tests, edge case tests
- **Data Validation**: Great Expectations, schema validation
- **Model Performance Tests**: Accuracy, F1 score, ROC AUC tests
- **Regression Tests**: Performance regression, prediction consistency tests
- **A/B Testing**: A/B test setup, analysis
- **Shadow Testing**: Shadow test setup, analysis
- **Monitoring in Production**: Performance monitoring, data drift monitoring
- **Best Practices**: Data quality, robustness, fairness, explainability, deployment testing
