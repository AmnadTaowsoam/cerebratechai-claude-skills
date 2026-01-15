# ML Model Testing

A comprehensive guide to ML model testing patterns.

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

### Unit Tests for Models

```python
import pytest
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

def test_model_initialization():
    """Test that model initializes correctly"""
    model = LogisticRegression()
    assert hasattr(model, 'coef_')
    assert hasattr(model, 'intercept_')

def test_model_shape():
    """Test that model has correct shape after fitting"""
    X = np.random.rand(100, 10)
    y = np.random.randint(0, 2, 100)

    model = LogisticRegression()
    model.fit(X, y)

    assert model.coef_.shape == (1, 10)
    assert model.intercept_.shape == (1,)
```

### Integration Tests for Pipeline

```python
import pytest
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

def test_full_pipeline():
    """Test that the full pipeline works end-to-end"""
    # Create sample data
    data = pd.DataFrame({
        'feature1': np.random.rand(100),
        'feature2': np.random.rand(100),
        'target': np.random.randint(0, 2, 100)
    })

    X = data[['feature1', 'feature2']]
    y = data['target']

    # Create pipeline
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', RandomForestClassifier())
    ])

    # Fit and predict
    pipeline.fit(X, y)
    predictions = pipeline.predict(X)

    # Assertions
    assert len(predictions) == 100
    assert all(p in [0, 1] for p in predictions)
```

### Model Validation Tests

```python
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def test_model_performance():
    """Test that model meets minimum performance requirements"""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LogisticRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    # Performance thresholds
    assert accuracy_score(y_test, predictions) >= 0.8
    assert precision_score(y_test, predictions) >= 0.8
    assert recall_score(y_test, predictions) >= 0.8
    assert f1_score(y_test, predictions) >= 0.8
```

---

## Testing Training Pipeline

### Data Loading Test

```python
import pytest
import pandas as pd

def test_data_loading():
    """Test that data loads correctly"""
    # Load data
    data = pd.read_csv('data/train.csv')

    # Assertions
    assert data is not None
    assert len(data) > 0
    assert 'target' in data.columns
    assert data['target'].notna().all()
```

### Preprocessing Test

```python
from sklearn.preprocessing import StandardScaler
import numpy as np

def test_preprocessing():
    """Test that preprocessing works correctly"""
    X = np.random.rand(100, 5)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Assertions
    assert X_scaled.shape == X.shape
    assert np.allclose(X_scaled.mean(axis=0), 0, atol=1e-10)
    assert np.allclose(X_scaled.std(axis=0), 1, atol=1e-10)
```

### Feature Engineering Test

```python
import pandas as pd
import numpy as np

def test_feature_engineering():
    """Test that feature engineering creates expected features"""
    data = pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=100),
        'value': np.random.rand(100)
    })

    # Extract features
    data['year'] = data['date'].dt.year
    data['month'] = data['date'].dt.month
    data['day_of_week'] = data['date'].dt.dayofweek

    # Assertions
    assert 'year' in data.columns
    assert 'month' in data.columns
    assert 'day_of_week' in data.columns
    assert data['year'].min() >= 2024
```

### Training Test

```python
from sklearn.ensemble import RandomForestClassifier

def test_training():
    """Test that model training completes"""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=10)
    model.fit(X_train, y_train)

    # Assertions
    assert hasattr(model, 'estimators_')
    assert len(model.estimators_) == 10
```

---

## Testing Inference

### Prediction Test

```python
import numpy as np
from sklearn.linear_model import LogisticRegression

def test_single_prediction():
    """Test single prediction"""
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Single prediction
    prediction = model.predict(X_test[0].reshape(1, -1))

    # Assertions
    assert prediction.shape == (1,)
    assert prediction[0] in [0, 1]
```

### Batch Prediction Test

```python
def test_batch_prediction():
    """Test batch prediction"""
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Batch prediction
    predictions = model.predict(X_test)

    # Assertions
    assert predictions.shape == X_test.shape[0]
    assert all(p in [0, 1] for p in predictions)
```

### Prediction Probability Test

```python
def test_prediction_probability():
    """Test prediction probabilities"""
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Get probabilities
    probabilities = model.predict_proba(X_test)

    # Assertions
    assert probabilities.shape == (len(X_test), 2)
    assert np.allclose(probabilities.sum(axis=1), 1)
    assert all(probabilities >= 0).all()
    assert all(probabilities <= 1).all()
```

---

## Data Validation

### Schema Validation

```python
import pytest
import pandas as pd
from pandera import Column, DataFrameSchema, Check

# Define schema
schema = DataFrameSchema({
    'feature1': Column(float, Check(lambda x: x >= 0)),
    'feature2': Column(float, Check(lambda x: x >= 0)),
    'target': Column(int, Check.isin([0, 1])),
})

def test_data_schema():
    """Test that data matches expected schema"""
    data = pd.DataFrame({
        'feature1': np.random.rand(100),
        'feature2': np.random.rand(100),
        'target': np.random.randint(0, 2, 100)
    })

    # Validate schema
    validated_data = schema.validate(data)

    # Assertions
    assert validated_data is not None
```

### Great Expectations

```python
import great_expectations as ge

def test_data_expectations():
    """Test data expectations"""
    df = pd.read_csv('data/train.csv')

    # Create expectation suite
    ge_df = ge.from_pandas(df)

    # Define expectations
    ge_df.expect_column_to_exist('feature1')
    ge_df.expect_column_values_to_be_between('feature1', min_value=0, max_value=100)
    ge_df.expect_column_values_to_not_be_null('target')

    # Validate expectations
    results = ge_df.validate()

    # Assertions
    assert results['success']
```

### Data Drift Detection

```python
from evidently import ColumnDriftMetric
from evidently.metric_preset import DataDriftPreset
from evidently.report import Report

def test_data_drift():
    """Test for data drift"""
    # Reference data (training)
    reference_data = pd.read_csv('data/train.csv')

    # Current data (production)
    current_data = pd.read_csv('data/production.csv')

    # Calculate drift
    data_drift_report = Report(metrics=[
        DataDriftPreset(),
    ])

    data_drift_report.run(
        reference_data=reference_data,
        current_data=current_data
    )

    # Assertions
    drift_score = data_drift_report.as_dict()['metrics'][0]['result']['drift_score']
    assert drift_score < 0.5  # Threshold for acceptable drift
```

---

## Model Performance Tests

### Accuracy Test

```python
from sklearn.metrics import accuracy_score

def test_accuracy():
    """Test model accuracy"""
    model = LogisticRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    # Assertions
    assert accuracy >= 0.8
```

### Precision and Recall Test

```python
from sklearn.metrics import precision_score, recall_score

def test_precision_recall():
    """Test model precision and recall"""
    model = LogisticRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    precision = precision_score(y_test, predictions)
    recall = recall_score(y_test, predictions)

    # Assertions
    assert precision >= 0.8
    assert recall >= 0.8
```

### ROC-AUC Test

```python
from sklearn.metrics import roc_auc_score

def test_roc_auc():
    """Test model ROC-AUC"""
    model = LogisticRegression()
    model.fit(X_train, y_train)
    probabilities = model.predict_proba(X_test)[:, 1]

    roc_auc = roc_auc_score(y_test, probabilities)

    # Assertions
    assert roc_auc >= 0.85
```

### Confusion Matrix Test

```python
from sklearn.metrics import confusion_matrix

def test_confusion_matrix():
    """Test confusion matrix"""
    model = LogisticRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    cm = confusion_matrix(y_test, predictions)

    # Assertions
    assert cm.shape == (2, 2)
    assert cm[0, 0] > 0  # True negatives
    assert cm[1, 1] > 0  # True positives
```

---

## Regression Tests

### Model Performance Regression

```python
import pytest
import joblib
from sklearn.metrics import accuracy_score

def test_no_performance_regression():
    """Test that model performance doesn't regress"""
    # Load baseline model
    baseline_model = joblib.load('models/baseline.pkl')

    # Load new model
    new_model = joblib.load('models/new.pkl')

    # Get predictions
    baseline_predictions = baseline_model.predict(X_test)
    new_predictions = new_model.predict(X_test)

    # Calculate accuracy
    baseline_accuracy = accuracy_score(y_test, baseline_predictions)
    new_accuracy = accuracy_score(y_test, new_predictions)

    # Assertions
    assert new_accuracy >= baseline_accuracy - 0.01  # Allow 1% degradation
```

### Feature Importance Regression

```python
def test_feature_importance_stability():
    """Test that feature importance is stable"""
    # Train model on full data
    model_full = RandomForestClassifier(n_estimators=100)
    model_full.fit(X, y)

    # Train model on subset
    X_subset, _, y_subset, _ = train_test_split(X, y, test_size=0.5, random_state=42)
    model_subset = RandomForestClassifier(n_estimators=100)
    model_subset.fit(X_subset, y_subset)

    # Compare feature importance
    full_importance = model_full.feature_importances_
    subset_importance = model_subset.feature_importances_

    # Assertions
    correlation = np.corrcoef(full_importance, subset_importance)[0, 1]
    assert correlation > 0.7  # High correlation expected
```

---

## A/B Testing

### A/B Test Setup

```python
import pytest
import numpy as np
from scipy import stats

def test_ab_test():
    """Test that new model performs better than baseline"""
    # Get predictions from both models
    baseline_predictions = baseline_model.predict(X_test)
    new_predictions = new_model.predict(X_test)

    # Calculate accuracy
    baseline_accuracy = accuracy_score(y_test, baseline_predictions)
    new_accuracy = accuracy_score(y_test, new_predictions)

    # Perform statistical test
    n1 = len(baseline_predictions)
    n2 = len(new_predictions)
    p1 = baseline_accuracy
    p2 = new_accuracy

    # Two-proportion z-test
    pooled_prop = (n1 * p1 + n2 * p2) / (n1 + n2)
    se = np.sqrt(pooled_prop * (1 - pooled_prop) * (1/n1 + 1/n2))
    z_score = (p2 - p1) / se

    # Assertions
    p_value = 1 - stats.norm.cdf(z_score)
    assert p_value < 0.05  # Significant improvement
    assert new_accuracy > baseline_accuracy
```

### Multi-Arm Bandit Testing

```python
from bandit import Bandit

def test_bandit_algorithm():
    """Test bandit algorithm for model selection"""
    bandit = Bandit(arms=['model_a', 'model_b', 'model_c'])

    # Simulate rewards
    for _ in range(100):
        arm = bandit.select_arm()
        reward = get_reward(arm)
        bandit.update(arm, reward)

    # Assertions
    best_arm = bandit.best_arm()
    assert best_arm is not None
```

---

## Shadow Testing

### Shadow Deployment Test

```python
import pytest
import requests

def test_shadow_deployment():
    """Test shadow deployment"""
    # Prepare input data
    input_data = {'feature1': 1.0, 'feature2': 2.0}

    # Get predictions from both models
    baseline_response = requests.post('http://baseline-api/predict', json=input_data)
    new_response = requests.post('http://new-api/predict', json=input_data)

    baseline_prediction = baseline_response.json()['prediction']
    new_prediction = new_response.json()['prediction']

    # Assertions
    assert baseline_response.status_code == 200
    assert new_response.status_code == 200
    assert baseline_prediction in [0, 1]
    assert new_prediction in [0, 1]

    # Log differences
    if baseline_prediction != new_prediction:
        print(f"Prediction differs: baseline={baseline_prediction}, new={new_prediction}")
```

### Shadow Performance Test

```python
import time

def test_shadow_performance():
    """Test shadow deployment performance"""
    input_data = {'feature1': 1.0, 'feature2': 2.0}

    # Measure baseline latency
    start = time.time()
    baseline_response = requests.post('http://baseline-api/predict', json=input_data)
    baseline_latency = time.time() - start

    # Measure new model latency
    start = time.time()
    new_response = requests.post('http://new-api/predict', json=input_data)
    new_latency = time.time() - start

    # Assertions
    assert baseline_latency < 1.0  # Max 1 second
    assert new_latency < 1.0
    assert new_latency <= baseline_latency * 1.5  # Allow 50% overhead
```

---

## Monitoring in Production

### Model Performance Monitoring

```python
import prometheus_client
from sklearn.metrics import accuracy_score

# Create Prometheus metrics
accuracy_metric = prometheus_client.Gauge('model_accuracy', 'Model accuracy')
prediction_count = prometheus_client.Counter('model_predictions_total', 'Total predictions')

def monitor_model_performance():
    """Monitor model performance in production"""
    # Get recent predictions
    recent_data = get_recent_predictions()

    # Calculate metrics
    predictions = recent_data['predictions']
    actuals = recent_data['actuals']
    accuracy = accuracy_score(actuals, predictions)

    # Update metrics
    accuracy_metric.set(accuracy)
    prediction_count.inc(len(predictions))

    # Check for performance degradation
    if accuracy < 0.8:
        send_alert('Model performance degraded')
```

### Data Drift Monitoring

```python
def monitor_data_drift():
    """Monitor for data drift in production"""
    # Get reference data
    reference_data = load_reference_data()

    # Get current data
    current_data = load_current_data()

    # Calculate drift
    drift_score = calculate_drift(reference_data, current_data)

    # Update metric
    drift_metric.set(drift_score)

    # Check for significant drift
    if drift_score > 0.5:
        send_alert('Data drift detected')
```

### Prediction Distribution Monitoring

```python
import numpy as np
from scipy import stats

def monitor_prediction_distribution():
    """Monitor prediction distribution"""
    predictions = get_recent_predictions()

    # Calculate statistics
    mean = np.mean(predictions)
    std = np.std(predictions)

    # Check for distribution shift
    reference_mean = 0.5  # Expected mean
    z_score = (mean - reference_mean) / std

    # Alert if significant shift
    if abs(z_score) > 3:
        send_alert(f'Prediction distribution shifted: z={z_score:.2f}')
```

---

## Best Practices

### 1. Test Data Quality

```python
def test_data_quality():
    """Test data quality before training"""
    assert data.isnull().sum().sum() == 0
    assert (data.dtypes == expected_dtypes).all()
```

### 2. Test Model Persistence

```python
import joblib

def test_model_persistence():
    """Test model can be saved and loaded"""
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Save model
    joblib.dump(model, 'model.pkl')

    # Load model
    loaded_model = joblib.load('model.pkl')

    # Test predictions
    original_predictions = model.predict(X_test)
    loaded_predictions = loaded_model.predict(X_test)

    assert np.array_equal(original_predictions, loaded_predictions)
```

### 3. Test Model Versioning

```python
import pytest

@pytest.mark.parametrize('model_version', ['v1', 'v2', 'v3'])
def test_model_version(model_version):
    """Test each model version"""
    model = load_model(model_version)
    predictions = model.predict(X_test)

    # Version-specific assertions
    if model_version == 'v1':
        assert len(predictions) == len(X_test)
    elif model_version == 'v2':
        assert len(predictions) == len(X_test)
```

### 4. Test Edge Cases

```python
def test_edge_cases():
    """Test model on edge cases"""
    # Empty input
    with pytest.raises(ValueError):
        model.predict([])

    # Single sample
    prediction = model.predict(X_test[0].reshape(1, -1))
    assert prediction.shape == (1,)
```

### 5. Test Model Robustness

```python
def test_model_robustness():
    """Test model robustness to noise"""
    # Add noise to test data
    X_noisy = X_test + np.random.normal(0, 0.1, X_test.shape)

    predictions = model.predict(X_noisy)

    # Check predictions are still valid
    assert all(p in [0, 1] for p in predictions)
```

### 6. Test Model Fairness

```python
from sklearn.metrics import confusion_matrix

def test_model_fairness():
    """Test model fairness across groups"""
    # Get predictions by group
    group_a_predictions = model.predict(X_test[group_a_indices])
    group_b_predictions = model.predict(X_test[group_b_indices])

    # Calculate accuracy by group
    group_a_accuracy = accuracy_score(y_test[group_a_indices], group_a_predictions)
    group_b_accuracy = accuracy_score(y_test[group_b_indices], group_b_predictions)

    # Check for fairness
    accuracy_diff = abs(group_a_accuracy - group_b_accuracy)
    assert accuracy_diff < 0.1  # Max 10% difference
```

### 7. Test Model Explainability

```python
import shap

def test_model_explainability():
    """Test model explainability"""
    # Calculate SHAP values
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)

    # Assertions
    assert shap_values is not None
    assert shap_values.shape == X_test.shape
```

### 8. Test Model Inference Speed

```python
import time

def test_inference_speed():
    """Test model inference speed"""
    # Warm up
    model.predict(X_test[:10])

    # Measure inference time
    start = time.time()
    predictions = model.predict(X_test)
    inference_time = time.time() - start

    # Assertions
    assert inference_time < 1.0  # Max 1 second for 1000 samples
```

### 9. Test Model Memory Usage

```python
import tracemalloc

def test_memory_usage():
    """Test model memory usage"""
    tracemalloc.start()

    # Load and use model
    model = load_model()
    predictions = model.predict(X_test)

    # Get memory usage
    current, peak = tracemalloc.get_traced_memory()

    # Assertions
    assert peak < 100 * 1024 * 1024  # Max 100 MB
```

### 10. Test Model Deployment

```python
import requests

def test_model_deployment():
    """Test model deployment"""
    response = requests.post(
        'http://model-api/predict',
        json={'feature1': 1.0, 'feature2': 2.0}
    )

    # Assertions
    assert response.status_code == 200
    assert 'prediction' in response.json()
```

---

## Resources

- [Scikit-learn Documentation](https://scikit-learn.org/)
- [Great Expectations](https://docs.greatexpectations.io/)
- [Evidently AI](https://docs.evidentlyai.com/)
- [MLflow](https://mlflow.org/docs/latest/index.html)
- [Prometheus Client](https://prometheus_client.readthedocs.io/)
