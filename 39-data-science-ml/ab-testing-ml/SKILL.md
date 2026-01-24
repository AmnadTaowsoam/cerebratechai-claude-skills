---
name: A/B Testing for ML
description: Comparing ML models in production through experiment design, statistical testing, multi-armed bandits, traffic splitting, and monitoring to determine which model performs better.
---

# A/B Testing for ML

> **Current Level:** Advanced  
> **Domain:** Data Science / ML / Experimentation

---

## Overview

A/B testing compares ML models in production. This guide covers experiment design, statistical testing, multi-armed bandits, and monitoring for safely deploying and comparing ML models to determine which performs better on business metrics.

## A/B Testing for ML

```
Users → Traffic Split → Model A / Model B → Metrics → Winner
```

**Goals:**
- Compare model performance
- Minimize risk
- Maximize business metrics
- Statistical significance

## Experiment Design

```python
# A/B test design
class ABTestDesign:
    def __init__(
        self,
        model_a,
        model_b,
        traffic_split: float = 0.5,
        min_sample_size: int = 1000
    ):
        self.model_a = model_a
        self.model_b = model_b
        self.traffic_split = traffic_split
        self.min_sample_size = min_sample_size
        
        self.results_a = []
        self.results_b = []
    
    def assign_variant(self, user_id: str) -> str:
        """Assign user to variant"""
        # Consistent hashing for user assignment
        hash_value = hash(user_id) % 100
        
        if hash_value < (self.traffic_split * 100):
            return 'A'
        else:
            return 'B'
    
    def predict(self, user_id: str, features):
        """Make prediction based on variant"""
        variant = self.assign_variant(user_id)
        
        if variant == 'A':
            prediction = self.model_a.predict([features])[0]
            model = self.model_a
        else:
            prediction = self.model_b.predict([features])[0]
            model = self.model_b
        
        return {
            'prediction': prediction,
            'variant': variant,
            'model': model
        }
    
    def log_result(self, variant: str, metric_value: float):
        """Log experiment result"""
        if variant == 'A':
            self.results_a.append(metric_value)
        else:
            self.results_b.append(metric_value)
    
    def has_enough_data(self) -> bool:
        """Check if enough data collected"""
        return (
            len(self.results_a) >= self.min_sample_size and
            len(self.results_b) >= self.min_sample_size
        )
```

## Statistical Testing

```python
# Statistical significance testing
from scipy import stats
import numpy as np

class StatisticalTester:
    def __init__(self, alpha: float = 0.05):
        self.alpha = alpha
    
    def t_test(self, results_a: list, results_b: list) -> dict:
        """Perform t-test"""
        t_stat, p_value = stats.ttest_ind(results_a, results_b)
        
        mean_a = np.mean(results_a)
        mean_b = np.mean(results_b)
        
        is_significant = p_value < self.alpha
        
        return {
            't_statistic': t_stat,
            'p_value': p_value,
            'is_significant': is_significant,
            'mean_a': mean_a,
            'mean_b': mean_b,
            'difference': mean_b - mean_a,
            'relative_improvement': ((mean_b - mean_a) / mean_a) * 100
        }
    
    def mann_whitney_test(self, results_a: list, results_b: list) -> dict:
        """Non-parametric test (doesn't assume normal distribution)"""
        u_stat, p_value = stats.mannwhitneyu(results_a, results_b, alternative='two-sided')
        
        return {
            'u_statistic': u_stat,
            'p_value': p_value,
            'is_significant': p_value < self.alpha
        }
    
    def calculate_confidence_interval(self, data: list, confidence: float = 0.95) -> tuple:
        """Calculate confidence interval"""
        mean = np.mean(data)
        sem = stats.sem(data)
        
        interval = stats.t.interval(
            confidence,
            len(data) - 1,
            loc=mean,
            scale=sem
        )
        
        return interval
    
    def calculate_sample_size(
        self,
        baseline_mean: float,
        mde: float,  # Minimum detectable effect
        power: float = 0.8,
        alpha: float = 0.05
    ) -> int:
        """Calculate required sample size"""
        from statsmodels.stats.power import tt_ind_solve_power
        
        effect_size = mde / baseline_mean
        
        sample_size = tt_ind_solve_power(
            effect_size=effect_size,
            alpha=alpha,
            power=power,
            alternative='two-sided'
        )
        
        return int(np.ceil(sample_size))
```

## Multi-armed Bandits

```python
# Multi-armed bandit for adaptive testing
import numpy as np

class EpsilonGreedyBandit:
    def __init__(self, n_arms: int, epsilon: float = 0.1):
        self.n_arms = n_arms
        self.epsilon = epsilon
        
        self.counts = np.zeros(n_arms)
        self.values = np.zeros(n_arms)
    
    def select_arm(self) -> int:
        """Select arm using epsilon-greedy strategy"""
        if np.random.random() < self.epsilon:
            # Explore: random arm
            return np.random.randint(self.n_arms)
        else:
            # Exploit: best arm
            return np.argmax(self.values)
    
    def update(self, arm: int, reward: float):
        """Update arm statistics"""
        self.counts[arm] += 1
        n = self.counts[arm]
        
        # Incremental average
        self.values[arm] = ((n - 1) / n) * self.values[arm] + (1 / n) * reward

class ThompsonSamplingBandit:
    def __init__(self, n_arms: int):
        self.n_arms = n_arms
        
        # Beta distribution parameters
        self.alpha = np.ones(n_arms)
        self.beta = np.ones(n_arms)
    
    def select_arm(self) -> int:
        """Select arm using Thompson sampling"""
        samples = np.random.beta(self.alpha, self.beta)
        return np.argmax(samples)
    
    def update(self, arm: int, reward: float):
        """Update Beta distribution"""
        if reward > 0:
            self.alpha[arm] += 1
        else:
            self.beta[arm] += 1

# Usage
bandit = ThompsonSamplingBandit(n_arms=2)  # 2 models

for i in range(1000):
    # Select model
    arm = bandit.select_arm()
    
    # Get prediction and reward
    prediction = models[arm].predict(features)
    reward = get_reward(prediction)  # 1 for success, 0 for failure
    
    # Update bandit
    bandit.update(arm, reward)
```

## Model Comparison Metrics

```python
# Compare models on multiple metrics
class ModelComparator:
    def __init__(self):
        self.metrics = {
            'A': {'predictions': [], 'actuals': [], 'latencies': []},
            'B': {'predictions': [], 'actuals': [], 'latencies': []}
        }
    
    def log_prediction(
        self,
        variant: str,
        prediction: float,
        actual: float,
        latency: float
    ):
        """Log prediction result"""
        self.metrics[variant]['predictions'].append(prediction)
        self.metrics[variant]['actuals'].append(actual)
        self.metrics[variant]['latencies'].append(latency)
    
    def compare_accuracy(self) -> dict:
        """Compare accuracy metrics"""
        from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
        
        results = {}
        
        for variant in ['A', 'B']:
            y_true = self.metrics[variant]['actuals']
            y_pred = self.metrics[variant]['predictions']
            
            results[variant] = {
                'mse': mean_squared_error(y_true, y_pred),
                'mae': mean_absolute_error(y_true, y_pred),
                'r2': r2_score(y_true, y_pred)
            }
        
        return results
    
    def compare_latency(self) -> dict:
        """Compare latency"""
        results = {}
        
        for variant in ['A', 'B']:
            latencies = self.metrics[variant]['latencies']
            
            results[variant] = {
                'mean': np.mean(latencies),
                'median': np.median(latencies),
                'p95': np.percentile(latencies, 95),
                'p99': np.percentile(latencies, 99)
            }
        
        return results
    
    def compare_business_metrics(self) -> dict:
        """Compare business metrics"""
        # Example: conversion rate, revenue, etc.
        results = {}
        
        for variant in ['A', 'B']:
            predictions = self.metrics[variant]['predictions']
            
            # Calculate business metric (example: conversion rate)
            conversions = sum(1 for p in predictions if p > 0.5)
            conversion_rate = conversions / len(predictions)
            
            results[variant] = {
                'conversion_rate': conversion_rate,
                'total_conversions': conversions
            }
        
        return results
```

## Implementation Patterns

```python
# Complete A/B testing implementation
from fastapi import FastAPI, Request
import time

app = FastAPI()

class MLABTest:
    def __init__(self, model_a, model_b):
        self.model_a = model_a
        self.model_b = model_b
        self.comparator = ModelComparator()
    
    def predict(self, user_id: str, features: list) -> dict:
        """Make prediction with A/B testing"""
        # Assign variant
        variant = self.assign_variant(user_id)
        
        # Select model
        model = self.model_a if variant == 'A' else self.model_b
        
        # Measure latency
        start_time = time.time()
        prediction = model.predict([features])[0]
        latency = time.time() - start_time
        
        return {
            'prediction': float(prediction),
            'variant': variant,
            'latency': latency
        }
    
    def assign_variant(self, user_id: str) -> str:
        """Assign user to variant"""
        return 'A' if hash(user_id) % 2 == 0 else 'B'
    
    def log_outcome(
        self,
        user_id: str,
        variant: str,
        prediction: float,
        actual: float,
        latency: float
    ):
        """Log experiment outcome"""
        self.comparator.log_prediction(variant, prediction, actual, latency)

ab_test = MLABTest(model_a, model_b)

@app.post("/predict")
async def predict(request: Request):
    """Prediction endpoint with A/B testing"""
    data = await request.json()
    
    user_id = data['user_id']
    features = data['features']
    
    result = ab_test.predict(user_id, features)
    
    return result

@app.post("/feedback")
async def feedback(request: Request):
    """Log actual outcome"""
    data = await request.json()
    
    ab_test.log_outcome(
        user_id=data['user_id'],
        variant=data['variant'],
        prediction=data['prediction'],
        actual=data['actual'],
        latency=data['latency']
    )
    
    return {"status": "logged"}
```

## Traffic Splitting

```python
# Advanced traffic splitting strategies
class TrafficSplitter:
    def __init__(self):
        self.splits = {
            'A': 0.5,
            'B': 0.5
        }
    
    def update_split(self, variant: str, new_split: float):
        """Update traffic split"""
        self.splits[variant] = new_split
    
    def gradual_rollout(self, target_variant: str, steps: int = 10):
        """Gradually increase traffic to target variant"""
        import time
        
        current_split = self.splits[target_variant]
        step_size = (1.0 - current_split) / steps
        
        for i in range(steps):
            new_split = current_split + (i + 1) * step_size
            self.update_split(target_variant, new_split)
            
            print(f"Step {i+1}: {target_variant} = {new_split:.2%}")
            time.sleep(60)  # Wait 1 minute between steps
```

## Feature Flags for Models

```python
# Feature flags for model selection
class ModelFeatureFlags:
    def __init__(self):
        self.flags = {
            'use_model_b': False,
            'model_b_percentage': 0,
            'model_b_users': set()
        }
    
    def should_use_model_b(self, user_id: str) -> bool:
        """Determine if user should get model B"""
        # Check if globally enabled
        if not self.flags['use_model_b']:
            return False
        
        # Check if user is in whitelist
        if user_id in self.flags['model_b_users']:
            return True
        
        # Check percentage rollout
        if hash(user_id) % 100 < self.flags['model_b_percentage']:
            return True
        
        return False
    
    def enable_for_user(self, user_id: str):
        """Enable model B for specific user"""
        self.flags['model_b_users'].add(user_id)
    
    def set_percentage(self, percentage: int):
        """Set percentage of users to get model B"""
        self.flags['model_b_percentage'] = percentage
```

## Monitoring Experiments

```python
# Monitor A/B test in real-time
import pandas as pd
import matplotlib.pyplot as plt

class ExperimentMonitor:
    def __init__(self):
        self.data = []
    
    def log_event(self, variant: str, metric: float, timestamp: float):
        """Log experiment event"""
        self.data.append({
            'variant': variant,
            'metric': metric,
            'timestamp': timestamp
        })
    
    def get_running_stats(self) -> pd.DataFrame:
        """Get running statistics"""
        df = pd.DataFrame(self.data)
        
        stats = df.groupby('variant')['metric'].agg([
            'count',
            'mean',
            'std',
            'min',
            'max'
        ])
        
        return stats
    
    def plot_results(self):
        """Plot experiment results"""
        df = pd.DataFrame(self.data)
        
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        
        # Distribution
        df.boxplot(column='metric', by='variant', ax=axes[0])
        axes[0].set_title('Metric Distribution by Variant')
        
        # Over time
        for variant in df['variant'].unique():
            variant_data = df[df['variant'] == variant]
            axes[1].plot(
                variant_data['timestamp'],
                variant_data['metric'].cumsum() / range(1, len(variant_data) + 1),
                label=f'Variant {variant}'
            )
        
        axes[1].set_title('Cumulative Average Over Time')
        axes[1].legend()
        
        plt.tight_layout()
        plt.show()
```

## Early Stopping

```python
# Early stopping for A/B tests
class EarlyStopping:
    def __init__(
        self,
        min_samples: int = 1000,
        alpha: float = 0.05,
        check_interval: int = 100
    ):
        self.min_samples = min_samples
        self.alpha = alpha
        self.check_interval = check_interval
        self.samples_seen = 0
    
    def should_stop(self, results_a: list, results_b: list) -> dict:
        """Check if experiment should stop early"""
        self.samples_seen += 1
        
        # Don't check until minimum samples
        if len(results_a) < self.min_samples or len(results_b) < self.min_samples:
            return {'should_stop': False, 'reason': 'Not enough samples'}
        
        # Only check at intervals
        if self.samples_seen % self.check_interval != 0:
            return {'should_stop': False, 'reason': 'Not at check interval'}
        
        # Perform statistical test
        t_stat, p_value = stats.ttest_ind(results_a, results_b)
        
        if p_value < self.alpha:
            winner = 'A' if np.mean(results_a) > np.mean(results_b) else 'B'
            return {
                'should_stop': True,
                'reason': 'Significant difference found',
                'winner': winner,
                'p_value': p_value
            }
        
        return {'should_stop': False, 'reason': 'No significant difference yet'}
```

## Best Practices

1. **Sample Size** - Calculate required sample size
2. **Randomization** - Ensure proper randomization
3. **Metrics** - Define clear success metrics
4. **Duration** - Run for appropriate duration
5. **Significance** - Check statistical significance
6. **Business Impact** - Consider business metrics
7. **Monitoring** - Monitor experiments continuously
8. **Early Stopping** - Stop early if clear winner
9. **Documentation** - Document experiment design
10. **Rollback** - Have rollback plan ready

---

## Quick Start

### Model A/B Test

```python
import random

def assign_model(user_id: str) -> str:
    # Consistent assignment
    hash_value = hash(user_id)
    return 'model_a' if hash_value % 2 == 0 else 'model_b'

# Track predictions
def track_prediction(user_id: str, model: str, prediction: float, actual: float):
    metrics.track('ml_prediction', {
        'user_id': user_id,
        'model': model,
        'prediction': prediction,
        'actual': actual,
        'error': abs(prediction - actual)
    })
```

---

## Production Checklist

- [ ] **Experiment Design**: Clear experiment design
- [ ] **Traffic Splitting**: Proper traffic splitting
- [ ] **Statistical Testing**: Statistical significance tests
- [ ] **Metrics**: Business and ML metrics
- [ ] **Monitoring**: Continuous monitoring
- [ ] **Early Stopping**: Early stopping rules
- [ ] **Documentation**: Document experiment
- [ ] **Rollback**: Rollback plan
- [ ] **Testing**: Test implementation
- [ ] **Documentation**: Document results
- [ ] **Action**: Act on results
- [ ] **Learning**: Document learnings

---

## Anti-patterns

### ❌ Don't: No Statistical Testing

```python
# ❌ Bad - No significance test
if model_b_accuracy > model_a_accuracy:
    return 'B wins'  # Could be random!
```

```python
# ✅ Good - Statistical test
from scipy import stats

t_stat, p_value = stats.ttest_ind(model_a_errors, model_b_errors)
if p_value < 0.05 and model_b_accuracy > model_a_accuracy:
    return 'B wins (statistically significant)'
```

### ❌ Don't: Ignore Business Metrics

```python
# ❌ Bad - Only ML metrics
if model_b_accuracy > model_a_accuracy:
    return 'B wins'
# But what about revenue?
```

```python
# ✅ Good - Business metrics too
if (model_b_accuracy > model_a_accuracy and 
    model_b_revenue >= model_a_revenue):
    return 'B wins'
```

---

## Integration Points

- **ML Serving** (`39-data-science-ml/ml-serving/`) - Model serving
- **Model Experiments** (`39-data-science-ml/model-experiments/`) - Experiment tracking
- **A/B Testing Analysis** (`23-business-analytics/ab-testing-analysis/`) - Testing methodology

---

## Further Reading

- [ML A/B Testing Guide](https://www.datacamp.com/tutorial/ab-testing-machine-learning)
- [Multi-Armed Bandits](https://en.wikipedia.org/wiki/Multi-armed_bandit)

## Resources

- [Statsmodels](https://www.statsmodels.org/)
- [SciPy Stats](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [Optimizely](https://www.optimizely.com/)
- [Google Optimize](https://optimize.google.com/)
- [A/B Testing Book](https://www.oreilly.com/library/view/trustworthy-online-controlled/9781108724265/)
