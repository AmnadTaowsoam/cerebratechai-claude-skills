---
name: AutoML
description: Automating machine learning pipeline creation including feature engineering, model selection, hyperparameter tuning, and ensemble creation using Auto-sklearn, H2O, TPOT, and AutoKeras.
---

# AutoML

> **Current Level:** Advanced  
> **Domain:** Data Science / ML / Automation

---

## Overview

AutoML automates machine learning pipeline creation. This guide covers Auto-sklearn, H2O, TPOT, AutoKeras, and when to use AutoML for accelerating ML development by automating repetitive tasks.

## AutoML Concepts

```
Data → AutoML → Best Model + Hyperparameters
```

**Automated Steps:**
- Feature engineering
- Model selection
- Hyperparameter tuning
- Ensemble creation

## Auto-sklearn

```python
# Auto-sklearn for classification
import autosklearn.classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Create AutoML classifier
automl = autosklearn.classification.AutoSklearnClassifier(
    time_left_for_this_task=3600,  # 1 hour
    per_run_time_limit=300,  # 5 minutes per model
    memory_limit=3072,  # MB
    n_jobs=-1
)

# Fit
automl.fit(X_train, y_train)

# Predict
y_pred = automl.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred)}")

# Show models
print(automl.show_models())

# Get statistics
print(automl.sprint_statistics())

# Refit on full dataset
automl.refit(X, y)
```

### Regression

```python
# Auto-sklearn for regression
import autosklearn.regression

automl = autosklearn.regression.AutoSklearnRegressor(
    time_left_for_this_task=3600,
    per_run_time_limit=300
)

automl.fit(X_train, y_train)
y_pred = automl.predict(X_test)

from sklearn.metrics import mean_squared_error
print(f"MSE: {mean_squared_error(y_test, y_pred)}")
```

## H2O AutoML

```python
# H2O AutoML
import h2o
from h2o.automl import H2OAutoML

# Initialize H2O
h2o.init()

# Load data
df = h2o.H2OFrame(data)

# Split data
train, test = df.split_frame(ratios=[0.8])

# Define features and target
x = df.columns
y = 'target'
x.remove(y)

# Run AutoML
aml = H2OAutoML(
    max_models=20,
    max_runtime_secs=3600,
    seed=42,
    balance_classes=True,
    sort_metric='AUC'
)

aml.train(x=x, y=y, training_frame=train)

# View leaderboard
lb = aml.leaderboard
print(lb.head())

# Best model
best_model = aml.leader

# Predictions
preds = best_model.predict(test)

# Model performance
perf = best_model.model_performance(test)
print(perf)

# Explain model
best_model.explain(test)

# Save model
h2o.save_model(best_model, path="./models")
```

## TPOT

```python
# TPOT for automated pipeline optimization
from tpot import TPOTClassifier
from sklearn.model_selection import train_test_split

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Create TPOT classifier
tpot = TPOTClassifier(
    generations=5,
    population_size=50,
    verbosity=2,
    random_state=42,
    n_jobs=-1,
    config_dict='TPOT light'  # or 'TPOT sparse', 'TPOT MDR'
)

# Fit
tpot.fit(X_train, y_train)

# Score
print(f"Accuracy: {tpot.score(X_test, y_test)}")

# Export pipeline
tpot.export('tpot_pipeline.py')

# Generated pipeline example:
"""
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

pipeline = make_pipeline(
    StandardScaler(),
    RandomForestClassifier(n_estimators=100, max_depth=10)
)
"""
```

### TPOT Regression

```python
# TPOT for regression
from tpot import TPOTRegressor

tpot = TPOTRegressor(
    generations=5,
    population_size=50,
    scoring='neg_mean_squared_error',
    verbosity=2
)

tpot.fit(X_train, y_train)
print(f"MSE: {-tpot.score(X_test, y_test)}")
```

## AutoKeras

```python
# AutoKeras for neural architecture search
import autokeras as ak
import tensorflow as tf

# Image classification
clf = ak.ImageClassifier(
    max_trials=10,
    overwrite=True,
    directory='autokeras_output'
)

clf.fit(x_train, y_train, epochs=10)

# Evaluate
accuracy = clf.evaluate(x_test, y_test)
print(f"Accuracy: {accuracy}")

# Predict
y_pred = clf.predict(x_test)

# Export model
model = clf.export_model()
model.save('my_model.h5')

# Text classification
clf = ak.TextClassifier(max_trials=10)
clf.fit(x_train, y_train, epochs=10)

# Structured data
clf = ak.StructuredDataClassifier(max_trials=10)
clf.fit(x_train, y_train, epochs=10)
```

## Automated Feature Engineering

```python
# Feature engineering with Featuretools
import featuretools as ft

# Create entity set
es = ft.EntitySet(id='data')

# Add dataframe
es = es.add_dataframe(
    dataframe_name='transactions',
    dataframe=df,
    index='transaction_id',
    time_index='timestamp'
)

# Deep feature synthesis
feature_matrix, feature_defs = ft.dfs(
    entityset=es,
    target_dataframe_name='transactions',
    max_depth=2,
    verbose=True
)

print(f"Generated {len(feature_defs)} features")
```

## Model Selection

```python
# Automated model selection
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

models = {
    'RandomForest': RandomForestClassifier(),
    'GradientBoosting': GradientBoostingClassifier(),
    'LogisticRegression': LogisticRegression(),
    'SVM': SVC()
}

results = {}

for name, model in models.items():
    scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
    results[name] = {
        'mean': scores.mean(),
        'std': scores.std()
    }
    print(f"{name}: {scores.mean():.4f} (+/- {scores.std():.4f})")

# Select best model
best_model_name = max(results, key=lambda x: results[x]['mean'])
print(f"\nBest model: {best_model_name}")
```

## Hyperparameter Tuning

```python
# Automated hyperparameter tuning with Optuna
import optuna
from sklearn.ensemble import RandomForestClassifier

def objective(trial):
    """Objective function for Optuna"""
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 50, 300),
        'max_depth': trial.suggest_int('max_depth', 3, 20),
        'min_samples_split': trial.suggest_int('min_samples_split', 2, 20),
        'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 10)
    }
    
    model = RandomForestClassifier(**params, random_state=42)
    
    scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
    
    return scores.mean()

# Create study
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=100)

# Best parameters
print(f"Best params: {study.best_params}")
print(f"Best value: {study.best_value}")

# Train final model
best_model = RandomForestClassifier(**study.best_params, random_state=42)
best_model.fit(X_train, y_train)
```

## Ensemble Methods

```python
# Automated ensemble creation
from sklearn.ensemble import VotingClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression

# Voting ensemble
voting_clf = VotingClassifier(
    estimators=[
        ('rf', RandomForestClassifier()),
        ('gb', GradientBoostingClassifier()),
        ('lr', LogisticRegression())
    ],
    voting='soft'
)

voting_clf.fit(X_train, y_train)

# Stacking ensemble
stacking_clf = StackingClassifier(
    estimators=[
        ('rf', RandomForestClassifier()),
        ('gb', GradientBoostingClassifier())
    ],
    final_estimator=LogisticRegression()
)

stacking_clf.fit(X_train, y_train)
```

## Neural Architecture Search

```python
# NAS with Keras Tuner
import keras_tuner as kt
import tensorflow as tf

def build_model(hp):
    """Build model with hyperparameters"""
    model = tf.keras.Sequential()
    
    # Tune number of layers
    for i in range(hp.Int('num_layers', 1, 3)):
        model.add(tf.keras.layers.Dense(
            units=hp.Int(f'units_{i}', min_value=32, max_value=512, step=32),
            activation='relu'
        ))
        
        # Tune dropout
        if hp.Boolean('dropout'):
            model.add(tf.keras.layers.Dropout(
                rate=hp.Float('dropout_rate', 0, 0.5, step=0.1)
            ))
    
    model.add(tf.keras.layers.Dense(10, activation='softmax'))
    
    # Tune learning rate
    model.compile(
        optimizer=tf.keras.optimizers.Adam(
            hp.Float('learning_rate', 1e-4, 1e-2, sampling='log')
        ),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

# Create tuner
tuner = kt.RandomSearch(
    build_model,
    objective='val_accuracy',
    max_trials=10,
    directory='nas_output',
    project_name='my_nas'
)

# Search
tuner.search(x_train, y_train, epochs=10, validation_data=(x_val, y_val))

# Best model
best_model = tuner.get_best_models(num_models=1)[0]
```

## When to Use AutoML

**Use AutoML when:**
- Quick baseline needed
- Limited ML expertise
- Exploring new datasets
- Time constraints
- Standard problems

**Don't use AutoML when:**
- Complex custom requirements
- Domain-specific features needed
- Interpretability critical
- Production constraints
- Research/innovation needed

## Limitations

1. **Black Box** - Less interpretable
2. **Computational Cost** - Resource intensive
3. **Generic Solutions** - May not be optimal
4. **Limited Customization** - Hard to add custom logic
5. **Overfitting Risk** - May overfit to validation set

## Production Deployment

```python
# Deploy AutoML model
import joblib

# Save Auto-sklearn model
joblib.dump(automl, 'automl_model.pkl')

# Load and predict
loaded_model = joblib.load('automl_model.pkl')
predictions = loaded_model.predict(new_data)

# Deploy H2O model
import h2o

h2o.init()
loaded_model = h2o.load_model('path/to/model')

# Convert to MOJO for production
loaded_model.download_mojo(path='./mojo')
```

## Best Practices

1. **Baseline** - Use AutoML for baseline
2. **Time Limits** - Set reasonable time limits
3. **Validation** - Use proper validation
4. **Interpretability** - Check if interpretability needed
5. **Resources** - Allocate sufficient resources
6. **Iteration** - Iterate on AutoML results
7. **Custom Features** - Add domain features
8. **Monitoring** - Monitor in production
9. **Documentation** - Document AutoML config
10. **Hybrid** - Combine AutoML with manual tuning

---

## Quick Start

### Auto-sklearn

```python
from autosklearn.classification import AutoSklearnClassifier

# Create AutoML classifier
automl = AutoSklearnClassifier(
    time_left_for_this_task=3600,  # 1 hour
    per_run_time_limit=300,  # 5 min per model
    memory_limit=4096  # 4GB
)

# Fit
automl.fit(X_train, y_train)

# Get best model
best_model = automl.get_models_with_weights()[0][1]
print(f"Best model: {best_model}")
```

### H2O AutoML

```python
import h2o
from h2o.automl import H2OAutoML

h2o.init()

# Load data
df = h2o.import_file("data.csv")

# AutoML
aml = H2OAutoML(max_models=10, seed=1)
aml.train(y="target", training_frame=df)

# Get leaderboard
print(aml.leaderboard)
```

---

## Production Checklist

- [ ] **Tool Selection**: Choose AutoML tool
- [ ] **Time Budget**: Set time budget
- [ ] **Resource Limits**: Set resource limits
- [ ] **Feature Engineering**: Review auto features
- [ ] **Model Selection**: Review selected models
- [ ] **Hyperparameter Tuning**: Review hyperparameters
- [ ] **Validation**: Validate AutoML results
- [ ] **Iteration**: Iterate on results
- [ ] **Custom Features**: Add domain features
- [ ] **Monitoring**: Monitor in production
- [ ] **Documentation**: Document AutoML config
- [ ] **Hybrid**: Combine with manual tuning

---

## Anti-patterns

### ❌ Don't: Blind Trust

```python
# ❌ Bad - Use without review
best_model = automl.fit(X, y)
deploy(best_model)  # No understanding!
```

```python
# ✅ Good - Review and understand
best_model = automl.fit(X, y)
review_model(best_model)  # Understand model
validate_on_holdout(best_model)  # Validate
deploy(best_model)
```

### ❌ Don't: No Domain Knowledge

```python
# ❌ Bad - Pure AutoML
automl.fit(X, y)
# Missing domain features!
```

```python
# ✅ Good - Add domain features
X_with_domain = add_domain_features(X)
automl.fit(X_with_domain, y)
# Better features!
```

---

## Integration Points

- **Feature Engineering** (`39-data-science-ml/feature-engineering/`) - Feature creation
- **Model Training** (`05-ai-ml-core/model-training/`) - Model development
- **Model Experiments** (`39-data-science-ml/model-experiments/`) - Experiment tracking

---

## Further Reading

- [AutoML Best Practices](https://www.automl.org/automl/)
- [When to Use AutoML](https://towardsdatascience.com/when-to-use-automl-7c0b0c0b0b0b)

## Resources

- [Auto-sklearn](https://automl.github.io/auto-sklearn/)
- [H2O AutoML](https://docs.h2o.ai/h2o/latest-stable/h2o-docs/automl.html)
- [TPOT](http://epistasislab.github.io/tpot/)
- [AutoKeras](https://autokeras.com/)
- [PyCaret](https://pycaret.org/)
