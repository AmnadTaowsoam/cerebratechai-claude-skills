---
name: Feature Engineering
description: Creating meaningful features from raw data to improve model performance, including numerical, categorical, text, and time-based feature engineering techniques.
---

# Feature Engineering

> **Current Level:** Advanced  
> **Domain:** Data Science / Machine Learning

---

## Overview

Feature engineering creates meaningful features from raw data to improve model performance. This guide covers numerical, categorical, text, and time-based features for building better machine learning models through domain knowledge and data transformation.

## Feature Engineering Concepts

```
Raw Data → Feature Engineering → Model Training → Better Performance
```

**Goals:**
- Improve model accuracy
- Reduce overfitting
- Enable better interpretability
- Capture domain knowledge

## Numerical Features

### Scaling

```python
# Feature scaling techniques
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
import pandas as pd
import numpy as np

# Standard Scaling (z-score normalization)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
# Result: mean=0, std=1

# Min-Max Scaling
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)
# Result: values between 0 and 1

# Robust Scaling (resistant to outliers)
scaler = RobustScaler()
X_scaled = scaler.fit_transform(X)
# Uses median and IQR

# Log transformation
X_log = np.log1p(X)  # log(1 + x) to handle zeros

# Box-Cox transformation
from scipy.stats import boxcox
X_boxcox, lambda_param = boxcox(X + 1)  # Requires positive values
```

### Binning

```python
# Binning continuous variables
import pandas as pd

# Equal-width binning
df['age_bin'] = pd.cut(df['age'], bins=5, labels=['Very Young', 'Young', 'Middle', 'Senior', 'Elderly'])

# Custom bins
df['income_bin'] = pd.cut(
    df['income'],
    bins=[0, 30000, 60000, 100000, float('inf')],
    labels=['Low', 'Medium', 'High', 'Very High']
)

# Quantile-based binning
df['score_quartile'] = pd.qcut(df['score'], q=4, labels=['Q1', 'Q2', 'Q3', 'Q4'])
```

### Polynomial Features

```python
# Polynomial and interaction features
from sklearn.preprocessing import PolynomialFeatures

# Create polynomial features
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X)

# Example: [x1, x2] → [x1, x2, x1², x1*x2, x2²]

# Manual interaction features
df['price_per_sqft'] = df['price'] / df['sqft']
df['total_rooms'] = df['bedrooms'] + df['bathrooms']
```

## Categorical Features

### One-Hot Encoding

```python
# One-hot encoding
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

# Pandas get_dummies
df_encoded = pd.get_dummies(df, columns=['category', 'color'], drop_first=True)

# Scikit-learn OneHotEncoder
encoder = OneHotEncoder(sparse=False, drop='first')
encoded = encoder.fit_transform(df[['category']])

# Handle unknown categories
encoder = OneHotEncoder(handle_unknown='ignore')
```

### Label Encoding

```python
# Label encoding for ordinal features
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder

# Label Encoder
le = LabelEncoder()
df['size_encoded'] = le.fit_transform(df['size'])
# ['Small', 'Medium', 'Large'] → [0, 1, 2]

# Ordinal Encoder with custom order
encoder = OrdinalEncoder(categories=[['Small', 'Medium', 'Large']])
df['size_encoded'] = encoder.fit_transform(df[['size']])
```

### Target Encoding

```python
# Target encoding (mean encoding)
class TargetEncoder:
    def __init__(self, smoothing=1.0):
        self.smoothing = smoothing
        self.mapping = {}
        self.global_mean = None
    
    def fit(self, X, y):
        """Fit encoder"""
        self.global_mean = y.mean()
        
        for col in X.columns:
            # Calculate mean target per category
            agg = pd.DataFrame({'X': X[col], 'y': y})
            counts = agg.groupby('X').size()
            means = agg.groupby('X')['y'].mean()
            
            # Apply smoothing
            smooth_means = (
                (counts * means + self.smoothing * self.global_mean) /
                (counts + self.smoothing)
            )
            
            self.mapping[col] = smooth_means.to_dict()
        
        return self
    
    def transform(self, X):
        """Transform data"""
        X_encoded = X.copy()
        
        for col in X.columns:
            X_encoded[col] = X[col].map(self.mapping[col]).fillna(self.global_mean)
        
        return X_encoded

# Usage
encoder = TargetEncoder(smoothing=10)
encoder.fit(X_train[['category']], y_train)
X_train_encoded = encoder.transform(X_train[['category']])
```

## Text Features

### TF-IDF

```python
# TF-IDF vectorization
from sklearn.feature_extraction.text import TfidfVectorizer

# Basic TF-IDF
vectorizer = TfidfVectorizer(
    max_features=1000,
    min_df=2,
    max_df=0.8,
    ngram_range=(1, 2)
)

X_tfidf = vectorizer.fit_transform(documents)

# With preprocessing
vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words='english',
    strip_accents='unicode',
    analyzer='word',
    token_pattern=r'\w{3,}'
)

# Get feature names
feature_names = vectorizer.get_feature_names_out()
```

### Word Embeddings

```python
# Word embeddings with Word2Vec
from gensim.models import Word2Vec
import numpy as np

# Train Word2Vec
sentences = [text.split() for text in documents]
model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, workers=4)

# Get document vectors (average of word vectors)
def document_vector(doc, model):
    """Average word vectors for document"""
    vectors = [model.wv[word] for word in doc.split() if word in model.wv]
    
    if vectors:
        return np.mean(vectors, axis=0)
    else:
        return np.zeros(model.vector_size)

doc_vectors = np.array([document_vector(doc, model) for doc in documents])

# Using pre-trained embeddings (GloVe, FastText)
import gensim.downloader as api

# Load pre-trained model
glove_model = api.load('glove-wiki-gigaword-100')
```

## Time-based Features

```python
# Extract time-based features
import pandas as pd

df['datetime'] = pd.to_datetime(df['timestamp'])

# Basic time features
df['year'] = df['datetime'].dt.year
df['month'] = df['datetime'].dt.month
df['day'] = df['datetime'].dt.day
df['hour'] = df['datetime'].dt.hour
df['dayofweek'] = df['datetime'].dt.dayofweek
df['quarter'] = df['datetime'].dt.quarter
df['is_weekend'] = df['dayofweek'].isin([5, 6]).astype(int)

# Cyclical encoding (for periodic features)
df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)

df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)

# Lag features
df['sales_lag_1'] = df['sales'].shift(1)
df['sales_lag_7'] = df['sales'].shift(7)

# Rolling window features
df['sales_rolling_mean_7'] = df['sales'].rolling(window=7).mean()
df['sales_rolling_std_7'] = df['sales'].rolling(window=7).std()

# Time since event
df['days_since_last_purchase'] = (df['datetime'] - df['last_purchase_date']).dt.days
```

## Feature Interactions

```python
# Create interaction features
from sklearn.preprocessing import PolynomialFeatures

# Automatic interactions
poly = PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)
X_interactions = poly.fit_transform(X)

# Manual domain-specific interactions
df['price_per_bedroom'] = df['price'] / df['bedrooms']
df['income_to_debt_ratio'] = df['income'] / (df['debt'] + 1)
df['bmi'] = df['weight'] / (df['height'] ** 2)

# Ratio features
df['click_through_rate'] = df['clicks'] / df['impressions']
df['conversion_rate'] = df['conversions'] / df['clicks']
```

## Feature Selection

```python
# Feature selection methods
from sklearn.feature_selection import (
    SelectKBest,
    f_classif,
    mutual_info_classif,
    RFE,
    SelectFromModel
)
from sklearn.ensemble import RandomForestClassifier

# Univariate selection
selector = SelectKBest(f_classif, k=10)
X_selected = selector.fit_transform(X, y)

# Mutual information
selector = SelectKBest(mutual_info_classif, k=10)
X_selected = selector.fit_transform(X, y)

# Recursive Feature Elimination
estimator = RandomForestClassifier()
selector = RFE(estimator, n_features_to_select=10)
X_selected = selector.fit_transform(X, y)

# Model-based selection
selector = SelectFromModel(RandomForestClassifier(), threshold='median')
X_selected = selector.fit_transform(X, y)

# Variance threshold
from sklearn.feature_selection import VarianceThreshold
selector = VarianceThreshold(threshold=0.1)
X_selected = selector.fit_transform(X)
```

## Feature Importance

```python
# Calculate feature importance
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Get feature importance
importances = model.feature_importances_
feature_names = X_train.columns

# Sort by importance
indices = np.argsort(importances)[::-1]

# Plot
plt.figure(figsize=(10, 6))
plt.bar(range(len(importances)), importances[indices])
plt.xticks(range(len(importances)), [feature_names[i] for i in indices], rotation=90)
plt.title('Feature Importance')
plt.tight_layout()
plt.show()

# SHAP values for feature importance
import shap

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

shap.summary_plot(shap_values, X_test)
```

## Pipeline Automation

```python
# Feature engineering pipeline
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

# Define transformers for different column types
numeric_features = ['age', 'income', 'score']
categorical_features = ['category', 'region']

numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Combine transformers
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ]
)

# Full pipeline
from sklearn.ensemble import RandomForestClassifier

pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier())
])

# Fit and predict
pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)
```

---

## Quick Start

### Numerical Feature Engineering

```python
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Create features
df['price_per_sqft'] = df['price'] / df['sqft']
df['age'] = pd.Timestamp.now().year - df['year_built']
df['log_price'] = np.log1p(df['price'])

# Scale features
scaler = StandardScaler()
df[['price', 'sqft']] = scaler.fit_transform(df[['price', 'sqft']])
```

### Categorical Encoding

```python
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

# Label encoding
le = LabelEncoder()
df['category_encoded'] = le.fit_transform(df['category'])

# One-hot encoding
df_encoded = pd.get_dummies(df, columns=['category'])
```

---

## Production Checklist

- [ ] **Domain Knowledge**: Use domain expertise
- [ ] **Data Exploration**: Explore data thoroughly
- [ ] **Missing Values**: Handle missing values
- [ ] **Feature Creation**: Create meaningful features
- [ ] **Scaling**: Scale features appropriately
- [ ] **Encoding**: Choose right encoding method
- [ ] **Interactions**: Create feature interactions
- [ ] **Feature Selection**: Remove irrelevant features
- [ ] **Validation**: Use cross-validation
- [ ] **Documentation**: Document feature logic
- [ ] **Automation**: Use pipelines for reproducibility
- [ ] **Testing**: Test feature engineering

---

## Anti-patterns

### ❌ Don't: Data Leakage

```python
# ❌ Bad - Using future information
df['future_price'] = df['price'].shift(-1)  # Leakage!
model.fit(X, df['future_price'])
```

```python
# ✅ Good - No leakage
# Only use past/current data
df['past_avg_price'] = df['price'].rolling(30).mean()
model.fit(X, df['price'])
```

### ❌ Don't: Ignore Missing Values

```python
# ❌ Bad - Ignore missing values
model.fit(X, y)  # NaN values cause errors!
```

```python
# ✅ Good - Handle missing values
df['age'].fillna(df['age'].median(), inplace=True)
# Or
df['age_missing'] = df['age'].isna().astype(int)
```

---

## Integration Points

- **Data Preprocessing** (`05-ai-ml-core/data-preprocessing/`) - Data cleaning
- **Model Training** (`05-ai-ml-core/model-training/`) - Model training
- **ML Serving** (`39-data-science-ml/ml-serving/`) - Feature serving

---

## Further Reading

- [Feature Engineering Guide](https://www.kaggle.com/learn/feature-engineering)
- [Feature Engineering Best Practices](https://towardsdatascience.com/feature-engineering-best-practices)

## Resources

- [Scikit-learn Preprocessing](https://scikit-learn.org/stable/modules/preprocessing.html)
- [Feature Engine](https://feature-engine.readthedocs.io/)
- [Category Encoders](https://contrib.scikit-learn.org/category_encoders/)
- [Feature Engineering Book](https://www.oreilly.com/library/view/feature-engineering-for/9781491953235/)
