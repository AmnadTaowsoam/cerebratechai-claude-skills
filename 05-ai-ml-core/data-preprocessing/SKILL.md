# Data Preprocessing

## Overview
Comprehensive guide for data preprocessing patterns in ML, covering data cleaning, feature engineering, normalization, and pipeline creation.

---

## 1. Data Cleaning

### 1.1 Missing Values

```python
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer, KNNImputer

class MissingValueHandler:
    """Handle missing values in datasets."""

    def __init__(self, strategy='mean', numeric_strategy='mean', categorical_strategy='most_frequent'):
        self.strategy = strategy
        self.numeric_strategy = numeric_strategy
        self.categorical_strategy = categorical_strategy
        self.numeric_imputer = None
        self.categorical_imputer = None

    def fit(self, X):
        """Fit imputers on data."""
        if isinstance(X, pd.DataFrame):
            numeric_cols = X.select_dtypes(include=[np.number]).columns
            categorical_cols = X.select_dtypes(exclude=[np.number]).columns
        else:
            # Assume all columns are numeric for numpy arrays
            numeric_cols = list(range(X.shape[1]))
            categorical_cols = []

        if len(numeric_cols) > 0:
            self.numeric_imputer = SimpleImputer(strategy=self.numeric_strategy)
            if isinstance(X, pd.DataFrame):
                self.numeric_imputer.fit(X[numeric_cols])
            else:
                self.numeric_imputer.fit(X[:, numeric_cols])

        if len(categorical_cols) > 0:
            self.categorical_imputer = SimpleImputer(strategy=self.categorical_strategy)
            self.categorical_imputer.fit(X[categorical_cols])

        return self

    def transform(self, X):
        """Transform data using fitted imputers."""
        X_transformed = X.copy()

        if isinstance(X, pd.DataFrame):
            numeric_cols = X.select_dtypes(include=[np.number]).columns
            categorical_cols = X.select_dtypes(exclude=[np.number]).columns

            if self.numeric_imputer is not None and len(numeric_cols) > 0:
                X_transformed[numeric_cols] = self.numeric_imputer.transform(X[numeric_cols])

            if self.categorical_imputer is not None and len(categorical_cols) > 0:
                X_transformed[categorical_cols] = self.categorical_imputer.transform(X[categorical_cols])
        else:
            if self.numeric_imputer is not None:
                X_transformed = self.numeric_imputer.transform(X)

        return X_transformed

    def fit_transform(self, X):
        """Fit and transform in one step."""
        return self.fit(X).transform(X)

# Usage
handler = MissingValueHandler(numeric_strategy='mean', categorical_strategy='most_frequent')
X_clean = handler.fit_transform(X_train)

# KNN Imputation for more sophisticated handling
knn_imputer = KNNImputer(n_neighbors=5)
X_knn = knn_imputer.fit_transform(X_train)
```

### 1.2 Outliers

```python
from scipy import stats
from sklearn.preprocessing import RobustScaler

class OutlierHandler:
    """Detect and handle outliers."""

    @staticmethod
    def z_score_detection(X, threshold=3):
        """Detect outliers using Z-score."""
        if isinstance(X, pd.DataFrame):
            numeric_cols = X.select_dtypes(include=[np.number]).columns
            z_scores = np.abs(stats.zscore(X[numeric_cols], nan_policy='omit'))
            outliers = (z_scores > threshold).any(axis=1)
        else:
            z_scores = np.abs(stats.zscore(X, nan_policy='omit'))
            outliers = (z_scores > threshold).any(axis=1)

        return outliers

    @staticmethod
    def iqr_detection(X, multiplier=1.5):
        """Detect outliers using IQR method."""
        if isinstance(X, pd.DataFrame):
            numeric_cols = X.select_dtypes(include=[np.number]).columns
            outliers = pd.Series(False, index=X.index)

            for col in numeric_cols:
                Q1 = X[col].quantile(0.25)
                Q3 = X[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - multiplier * IQR
                upper_bound = Q3 + multiplier * IQR
                outliers |= (X[col] < lower_bound) | (X[col] > upper_bound)
        else:
            Q1 = np.percentile(X, 25, axis=0)
            Q3 = np.percentile(X, 75, axis=0)
            IQR = Q3 - Q1
            lower_bound = Q1 - multiplier * IQR
            upper_bound = Q3 + multiplier * IQR
            outliers = ((X < lower_bound) | (X > upper_bound)).any(axis=1)

        return outliers

    @staticmethod
    def cap_outliers(X, method='iqr', multiplier=1.5):
        """Cap outliers to bounds instead of removing."""
        if isinstance(X, pd.DataFrame):
            X_capped = X.copy()
            numeric_cols = X.select_dtypes(include=[np.number]).columns

            for col in numeric_cols:
                if method == 'iqr':
                    Q1 = X[col].quantile(0.25)
                    Q3 = X[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - multiplier * IQR
                    upper_bound = Q3 + multiplier * IQR
                elif method == 'zscore':
                    mean = X[col].mean()
                    std = X[col].std()
                    lower_bound = mean - multiplier * std
                    upper_bound = mean + multiplier * std

                X_capped[col] = X[col].clip(lower_bound, upper_bound)

            return X_capped
        else:
            if method == 'iqr':
                Q1 = np.percentile(X, 25, axis=0)
                Q3 = np.percentile(X, 75, axis=0)
                IQR = Q3 - Q1
                lower_bound = Q1 - multiplier * IQR
                upper_bound = Q3 + multiplier * IQR
            elif method == 'zscore':
                mean = np.mean(X, axis=0)
                std = np.std(X, axis=0)
                lower_bound = mean - multiplier * std
                upper_bound = mean + multiplier * std

            return np.clip(X, lower_bound, upper_bound)

# Usage
outlier_handler = OutlierHandler()

# Detect outliers
outliers = outlier_handler.z_score_detection(X_train, threshold=3)

# Cap outliers
X_capped = outlier_handler.cap_outliers(X_train, method='iqr')

# Remove outliers
X_clean = X_train[~outliers]
y_clean = y_train[~outliers]
```

### 1.3 Duplicates

```python
class DuplicateHandler:
    """Handle duplicate rows."""

    @staticmethod
    def find_duplicates(X, subset=None):
        """Find duplicate rows."""
        if isinstance(X, pd.DataFrame):
            duplicates = X.duplicated(subset=subset, keep='first')
        else:
            # For numpy arrays
            _, indices = np.unique(X, axis=0, return_index=True)
            duplicates = np.ones(len(X), dtype=bool)
            duplicates[indices] = False

        return duplicates

    @staticmethod
    def remove_duplicates(X, y=None, subset=None):
        """Remove duplicate rows."""
        if isinstance(X, pd.DataFrame):
            if y is not None:
                df = X.copy()
                df['target'] = y
                df_clean = df.drop_duplicates(subset=subset, keep='first')
                return df_clean.drop(columns=['target']), df_clean['target']
            else:
                return X.drop_duplicates(subset=subset, keep='first')
        else:
            if y is not None:
                combined = np.column_stack([X, y])
                _, indices = np.unique(combined, axis=0, return_index=True)
                return X[indices], y[indices]
            else:
                _, indices = np.unique(X, axis=0, return_index=True)
                return X[indices]

# Usage
dup_handler = DuplicateHandler()

# Find duplicates
duplicates = dup_handler.find_duplicates(X_train)

# Remove duplicates
X_clean, y_clean = dup_handler.remove_duplicates(X_train, y_train)
```

---

## 2. Feature Engineering

### 2.1 Polynomial Features

```python
from sklearn.preprocessing import PolynomialFeatures
import numpy as np

class FeatureEngineer:
    """Create new features from existing ones."""

    def __init__(self):
        self.polynomial_features = None

    def create_polynomial_features(self, X, degree=2, include_bias=False):
        """Create polynomial features."""
        self.polynomial_features = PolynomialFeatures(
            degree=degree,
            include_bias=include_bias,
            interaction_only=False
        )
        return self.polynomial_features.fit_transform(X)

    def create_interaction_features(self, X):
        """Create pairwise interaction features."""
        n_features = X.shape[1]
        interaction_features = []

        for i in range(n_features):
            for j in range(i + 1, n_features):
                interaction_features.append(X[:, i] * X[:, j])

        return np.column_stack([X] + interaction_features)

    def create_ratio_features(self, X, pairs):
        """Create ratio features from column pairs."""
        ratio_features = X.copy()

        for col1, col2 in pairs:
            # Avoid division by zero
            ratio = np.divide(X[:, col1], X[:, col2],
                           out=np.zeros_like(X[:, col1]),
                           where=X[:, col2] != 0)
            ratio_features = np.column_stack([ratio_features, ratio])

        return ratio_features

    def create_bin_features(self, X, bins=10, strategy='uniform'):
        """Create binned features."""
        from sklearn.preprocessing import KBinsDiscretizer

        discretizer = KBinsDiscretizer(
            n_bins=bins,
            encode='onehot',
            strategy=strategy
        )

        return discretizer.fit_transform(X)

# Usage
engineer = FeatureEngineer()

# Polynomial features
X_poly = engineer.create_polynomial_features(X_train, degree=2)

# Interaction features
X_interaction = engineer.create_interaction_features(X_train)

# Ratio features
X_ratio = engineer.create_ratio_features(X_train, pairs=[(0, 1), (0, 2)])
```

### 2.2 Date/Time Features

```python
import pandas as pd
from datetime import datetime

class DateTimeFeatureEngineer:
    """Extract features from datetime columns."""

    @staticmethod
    def extract_features(X, datetime_cols):
        """Extract features from datetime columns."""
        if isinstance(X, pd.DataFrame):
            X_features = X.copy()

            for col in datetime_cols:
                if col in X.columns:
                    # Convert to datetime if not already
                    if not pd.api.types.is_datetime64_any_dtype(X[col]):
                        X_features[col] = pd.to_datetime(X[col])

                    # Extract features
                    X_features[f'{col}_year'] = X_features[col].dt.year
                    X_features[f'{col}_month'] = X_features[col].dt.month
                    X_features[f'{col}_day'] = X_features[col].dt.day
                    X_features[f'{col}_dayofweek'] = X_features[col].dt.dayofweek
                    X_features[f'{col}_dayofyear'] = X_features[col].dt.dayofyear
                    X_features[f'{col}_weekofyear'] = X_features[col].dt.isocalendar().week
                    X_features[f'{col}_hour'] = X_features[col].dt.hour
                    X_features[f'{col}_minute'] = X_features[col].dt.minute
                    X_features[f'{col}_is_weekend'] = (X_features[col].dt.dayofweek >= 5).astype(int)
                    X_features[f'{col}_is_month_start'] = (X_features[col].dt.day <= 7).astype(int)
                    X_features[f'{col}_is_month_end'] = (X_features[col].dt.day >= 24).astype(int)

                    # Cyclical features
                    X_features[f'{col}_month_sin'] = np.sin(2 * np.pi * X_features[col].dt.month / 12)
                    X_features[f'{col}_month_cos'] = np.cos(2 * np.pi * X_features[col].dt.month / 12)
                    X_features[f'{col}_dayofweek_sin'] = np.sin(2 * np.pi * X_features[col].dt.dayofweek / 7)
                    X_features[f'{col}_dayofweek_cos'] = np.cos(2 * np.pi * X_features[col].dt.dayofweek / 7)

            # Drop original datetime columns
            X_features = X_features.drop(columns=datetime_cols)

            return X_features
        else:
            raise ValueError("DateTimeFeatureEngineer only supports pandas DataFrames")

# Usage
dt_engineer = DateTimeFeatureEngineer()
X_dt_features = dt_engineer.extract_features(X_train, datetime_cols=['date_column'])
```

### 2.3 Text Features

```python
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import re

class TextFeatureEngineer:
    """Extract features from text columns."""

    def __init__(self):
        self.tfidf_vectorizer = None
        self.count_vectorizer = None

    def create_tfidf_features(self, texts, max_features=1000, ngram_range=(1, 2)):
        """Create TF-IDF features."""
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=ngram_range,
            stop_words='english',
            lowercase=True
        )
        return self.tfidf_vectorizer.fit_transform(texts)

    def create_count_features(self, texts, max_features=1000, ngram_range=(1, 1)):
        """Create count features."""
        self.count_vectorizer = CountVectorizer(
            max_features=max_features,
            ngram_range=ngram_range,
            stop_words='english',
            lowercase=True
        )
        return self.count_vectorizer.fit_transform(texts)

    def create_basic_features(self, texts):
        """Create basic text features."""
        features = []

        for text in texts:
            # Length features
            features.append([
                len(text),  # Character count
                len(text.split()),  # Word count
                len(text.splitlines()),  # Sentence count
                sum(1 for c in text if c.isupper()),  # Uppercase count
                sum(1 for c in text if c.islower()),  # Lowercase count
                sum(1 for c in text if c.isdigit()),  # Digit count
                sum(1 for c in text if c in '.,!?;:'),  # Punctuation count
                text.count(' '),  # Space count
                len(set(text.split())) / max(len(text.split()), 1)  # Unique word ratio
            ])

        return np.array(features)

    def clean_text(self, text):
        """Clean text."""
        # Remove special characters
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        # Convert to lowercase
        text = text.lower()
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text

# Usage
text_engineer = TextFeatureEngineer()

# TF-IDF features
X_tfidf = text_engineer.create_tfidf_features(text_data)

# Basic features
X_basic = text_engineer.create_basic_features(text_data)
```

---

## 3. Data Normalization/Standardization

### 3.1 Standardization

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, MaxAbsScaler

class DataScaler:
    """Scale and normalize data."""

    def __init__(self, method='standard'):
        self.method = method
        self.scaler = None

        if method == 'standard':
            self.scaler = StandardScaler()
        elif method == 'minmax':
            self.scaler = MinMaxScaler()
        elif method == 'robust':
            self.scaler = RobustScaler()
        elif method == 'maxabs':
            self.scaler = MaxAbsScaler()
        else:
            raise ValueError(f"Unknown scaling method: {method}")

    def fit(self, X):
        """Fit scaler on data."""
        self.scaler.fit(X)
        return self

    def transform(self, X):
        """Transform data using fitted scaler."""
        return self.scaler.transform(X)

    def fit_transform(self, X):
        """Fit and transform in one step."""
        return self.scaler.fit_transform(X)

    def inverse_transform(self, X):
        """Inverse transform scaled data."""
        return self.scaler.inverse_transform(X)

# Usage
scaler = DataScaler(method='standard')
X_scaled = scaler.fit_transform(X_train)

# Transform test data
X_test_scaled = scaler.transform(X_test)
```

### 3.2 Normalization

```python
from sklearn.preprocessing import Normalizer

class DataNormalizer:
    """Normalize samples individually."""

    def __init__(self, norm='l2'):
        self.norm = norm
        self.normalizer = Normalizer(norm=norm)

    def fit(self, X):
        """Fit normalizer (no-op for Normalizer)."""
        return self

    def transform(self, X):
        """Transform data using normalizer."""
        return self.normalizer.transform(X)

    def fit_transform(self, X):
        """Fit and transform in one step."""
        return self.normalizer.fit_transform(X)

# Usage
normalizer = DataNormalizer(norm='l2')
X_normalized = normalizer.fit_transform(X_train)
```

---

## 4. Encoding Categorical Variables

### 4.1 Label Encoding

```python
from sklearn.preprocessing import LabelEncoder
import pandas as pd

class CategoricalEncoder:
    """Encode categorical variables."""

    def __init__(self, method='label'):
        self.method = method
        self.encoders = {}
        self.onehot_encoder = None

    def fit(self, X, categorical_cols=None):
        """Fit encoders on data."""
        if isinstance(X, pd.DataFrame):
            if categorical_cols is None:
                categorical_cols = X.select_dtypes(include=['object', 'category']).columns

            for col in categorical_cols:
                if self.method == 'label':
                    encoder = LabelEncoder()
                    encoder.fit(X[col].astype(str))
                    self.encoders[col] = encoder
                elif self.method == 'onehot':
                    from sklearn.preprocessing import OneHotEncoder
                    self.onehot_encoder = OneHotEncoder(
                        sparse_output=False,
                        handle_unknown='ignore'
                    )
                    self.onehot_encoder.fit(X[categorical_cols])
        else:
            raise ValueError("CategoricalEncoder only supports pandas DataFrames")

        return self

    def transform(self, X):
        """Transform data using fitted encoders."""
        if isinstance(X, pd.DataFrame):
            X_transformed = X.copy()

            if self.method == 'label':
                for col, encoder in self.encoders.items():
                    X_transformed[col] = encoder.transform(X[col].astype(str))
            elif self.method == 'onehot' and self.onehot_encoder is not None:
                categorical_cols = list(self.encoders.keys())
                onehot_features = self.onehot_encoder.transform(X[categorical_cols])
                feature_names = self.onehot_encoder.get_feature_names_out(categorical_cols)

                # Drop original categorical columns
                X_transformed = X_transformed.drop(columns=categorical_cols)

                # Add one-hot encoded columns
                onehot_df = pd.DataFrame(onehot_features, columns=feature_names, index=X.index)
                X_transformed = pd.concat([X_transformed, onehot_df], axis=1)

            return X_transformed
        else:
            raise ValueError("CategoricalEncoder only supports pandas DataFrames")

    def fit_transform(self, X, categorical_cols=None):
        """Fit and transform in one step."""
        return self.fit(X, categorical_cols).transform(X)

# Usage
encoder = CategoricalEncoder(method='label')
X_encoded = encoder.fit_transform(X_train, categorical_cols=['category_col'])

# One-hot encoding
encoder_onehot = CategoricalEncoder(method='onehot')
X_onehot = encoder_onehot.fit_transform(X_train, categorical_cols=['category_col'])
```

### 4.2 Target Encoding

```python
from sklearn.model_selection import KFold
import numpy as np

class TargetEncoder:
    """Target encoding for categorical variables."""

    def __init__(self, smoothing=1.0, min_samples_leaf=1):
        self.smoothing = smoothing
        self.min_samples_leaf = min_samples_leaf
        self.encodings = {}
        self.global_mean = None

    def fit(self, X, y, categorical_cols=None):
        """Fit target encoder."""
        if isinstance(X, pd.DataFrame):
            if categorical_cols is None:
                categorical_cols = X.select_dtypes(include=['object', 'category']).columns

            self.global_mean = y.mean()

            for col in categorical_cols:
                # Calculate mean target per category
                category_means = y.groupby(X[col]).mean()
                category_counts = X[col].value_counts()

                # Apply smoothing
                smoothing_factor = 1 / (1 + np.exp(-(category_counts - self.min_samples_leaf) / self.smoothing))
                smoothed_means = self.global_mean * (1 - smoothing_factor) + category_means * smoothing_factor

                self.encodings[col] = smoothed_means
        else:
            raise ValueError("TargetEncoder only supports pandas DataFrames")

        return self

    def transform(self, X):
        """Transform data using fitted encoder."""
        if isinstance(X, pd.DataFrame):
            X_transformed = X.copy()

            for col, encoding in self.encodings.items():
                X_transformed[f'{col}_encoded'] = X[col].map(encoding).fillna(self.global_mean)

            return X_transformed
        else:
            raise ValueError("TargetEncoder only supports pandas DataFrames")

    def fit_transform(self, X, y, categorical_cols=None):
        """Fit and transform in one step."""
        return self.fit(X, y, categorical_cols).transform(X)

# Usage
target_encoder = TargetEncoder(smoothing=1.0, min_samples_leaf=10)
X_encoded = target_encoder.fit_transform(X_train, y_train, categorical_cols=['category_col'])
```

---

## 5. Feature Scaling

### 5.1 Min-Max Scaling

```python
from sklearn.preprocessing import MinMaxScaler

class MinMaxScalerCustom:
    """Custom Min-Max scaling."""

    def __init__(self, feature_range=(0, 1)):
        self.feature_range = feature_range
        self.min_ = None
        self.max_ = None
        self.scale_ = None

    def fit(self, X):
        """Fit scaler on data."""
        self.min_ = np.min(X, axis=0)
        self.max_ = np.max(X, axis=0)

        data_range = self.max_ - self.min_
        data_range[data_range == 0] = 1  # Avoid division by zero

        self.scale_ = (self.feature_range[1] - self.feature_range[0]) / data_range

        return self

    def transform(self, X):
        """Transform data."""
        X_scaled = (X - self.min_) * self.scale_
        X_scaled += self.feature_range[0]
        return X_scaled

    def fit_transform(self, X):
        """Fit and transform in one step."""
        return self.fit(X).transform(X)

# Usage
scaler = MinMaxScalerCustom(feature_range=(0, 1))
X_scaled = scaler.fit_transform(X_train)
```

### 5.2 Robust Scaling

```python
from sklearn.preprocessing import RobustScaler

class RobustScalerCustom:
    """Robust scaling using median and IQR."""

    def __init__(self, with_centering=True, with_scaling=True, quantile_range=(25.0, 75.0)):
        self.with_centering = with_centering
        self.with_scaling = with_scaling
        self.quantile_range = quantile_range
        self.center_ = None
        self.scale_ = None

    def fit(self, X):
        """Fit scaler on data."""
        if self.with_centering:
            self.center_ = np.median(X, axis=0)

        if self.with_scaling:
            q_min, q_max = self.quantile_range
            q1 = np.percentile(X, q_min, axis=0)
            q3 = np.percentile(X, q_max, axis=0)
            iqr = q3 - q1
            iqr[iqr == 0] = 1  # Avoid division by zero
            self.scale_ = iqr

        return self

    def transform(self, X):
        """Transform data."""
        X_scaled = X.copy()

        if self.with_centering:
            X_scaled -= self.center_

        if self.with_scaling:
            X_scaled /= self.scale_

        return X_scaled

    def fit_transform(self, X):
        """Fit and transform in one step."""
        return self.fit(X).transform(X)

# Usage
robust_scaler = RobustScalerCustom()
X_scaled = robust_scaler.fit_transform(X_train)
```

---

## 6. Data Augmentation

### 6.1 Image Augmentation

```python
import numpy as np
from PIL import Image, ImageEnhance, ImageOps
import random

class ImageAugmentor:
    """Augment images for training."""

    def __init__(self):
        self.transforms = []

    def add_transform(self, transform, probability=0.5):
        """Add transform to augmentation pipeline."""
        self.transforms.append((transform, probability))

    def apply(self, image):
        """Apply random transforms to image."""
        for transform, prob in self.transforms:
            if random.random() < prob:
                image = transform(image)
        return image

    @staticmethod
    def random_flip(image):
        """Random horizontal flip."""
        if random.random() > 0.5:
            return ImageOps.mirror(image)
        return image

    @staticmethod
    def random_rotation(image, max_angle=30):
        """Random rotation."""
        angle = random.uniform(-max_angle, max_angle)
        return image.rotate(angle)

    @staticmethod
    def random_crop(image, crop_ratio=0.8):
        """Random crop."""
        width, height = image.size
        crop_width = int(width * crop_ratio)
        crop_height = int(height * crop_ratio)

        left = random.randint(0, width - crop_width)
        top = random.randint(0, height - crop_height)

        return image.crop((left, top, left + crop_width, top + crop_height))

    @staticmethod
    def random_brightness(image, factor_range=(0.8, 1.2)):
        """Random brightness adjustment."""
        factor = random.uniform(*factor_range)
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(factor)

    @staticmethod
    def random_contrast(image, factor_range=(0.8, 1.2)):
        """Random contrast adjustment."""
        factor = random.uniform(*factor_range)
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(factor)

# Usage
augmentor = ImageAugmentor()
augmentor.add_transform(ImageAugmentor.random_flip, probability=0.5)
augmentor.add_transform(lambda img: ImageAugmentor.random_rotation(img, max_angle=15), probability=0.5)
augmentor.add_transform(ImageAugmentor.random_brightness, probability=0.5)

augmented_image = augmentor.apply(original_image)
```

### 6.2 Text Augmentation

```python
import random
from typing import List

class TextAugmentor:
    """Augment text for training."""

    @staticmethod
    def random_deletion(text, p=0.1):
        """Randomly delete words."""
        words = text.split()
        words = [word for word in words if random.random() > p]
        return ' '.join(words)

    @staticmethod
    def random_swap(text, n=1):
        """Randomly swap two words."""
        words = text.split()
        for _ in range(n):
            if len(words) >= 2:
                idx1, idx2 = random.sample(range(len(words)), 2)
                words[idx1], words[idx2] = words[idx2], words[idx1]
        return ' '.join(words)

    @staticmethod
    def synonym_replacement(text, n=1):
        """Replace words with synonyms."""
        # This is a simplified version - in practice, use WordNet or a synonym API
        words = text.split()
        for _ in range(n):
            if words:
                idx = random.randint(0, len(words) - 1)
                # In practice, replace with actual synonym
                words[idx] = words[idx]  # Placeholder
        return ' '.join(words)

    @staticmethod
    def random_insertion(text, n=1):
        """Randomly insert words."""
        words = text.split()
        for _ in range(n):
            idx = random.randint(0, len(words))
            # In practice, insert a relevant word
            words.insert(idx, "random")  # Placeholder
        return ' '.join(words)

# Usage
text_augmentor = TextAugmentor()
augmented_text = text_augmentor.random_deletion(original_text, p=0.1)
```

---

## 7. Pipeline Creation

### 7.1 Scikit-learn Pipeline

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

def create_preprocessing_pipeline(numeric_features, categorical_features):
    """Create sklearn preprocessing pipeline."""

    # Numeric preprocessing
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler())
    ])

    # Categorical preprocessing
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    # Column transformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ]
    )

    return preprocessor

# Usage
numeric_features = ['age', 'income', 'score']
categorical_features = ['gender', 'education', 'city']

preprocessor = create_preprocessing_pipeline(numeric_features, categorical_features)

# Fit and transform
X_processed = preprocessor.fit_transform(X_train)

# Transform test data
X_test_processed = preprocessor.transform(X_test)
```

### 7.2 Custom Pipeline

```python
from sklearn.base import BaseEstimator, TransformerMixin

class CustomPreprocessor(BaseEstimator, TransformerMixin):
    """Custom preprocessing pipeline."""

    def __init__(self, steps=None):
        self.steps = steps or []

    def add_step(self, name, transformer):
        """Add preprocessing step."""
        self.steps.append((name, transformer))
        return self

    def fit(self, X, y=None):
        """Fit all transformers."""
        for name, transformer in self.steps:
            transformer.fit(X, y)
        return self

    def transform(self, X):
        """Transform data through all steps."""
        X_transformed = X.copy()
        for name, transformer in self.steps:
            X_transformed = transformer.transform(X_transformed)
        return X_transformed

    def fit_transform(self, X, y=None):
        """Fit and transform in one step."""
        return self.fit(X, y).transform(X)

# Usage
preprocessor = CustomPreprocessor()
preprocessor.add_step('missing_values', MissingValueHandler())
preprocessor.add_step('scaler', DataScaler(method='standard'))
preprocessor.add_step('encoder', CategoricalEncoder(method='label'))

X_processed = preprocessor.fit_transform(X_train)
```

---

## 8. Preprocessing for Different Data Types

### 8.1 Image Preprocessing

```python
import torchvision.transforms as transforms
from PIL import Image
import numpy as np

class ImagePreprocessor:
    """Preprocess images for ML."""

    def __init__(self, image_size=(224, 224), normalize=True, augment=False):
        self.image_size = image_size
        self.normalize = normalize
        self.augment = augment

        # Base transforms
        transform_list = [
            transforms.Resize(image_size),
            transforms.ToTensor()
        ]

        # Add normalization
        if normalize:
            transform_list.append(
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225]
                )
            )

        # Add augmentation
        if augment:
            transform_list.insert(1, transforms.RandomHorizontalFlip(p=0.5))
            transform_list.insert(2, transforms.RandomRotation(degrees=15))
            transform_list.insert(3, transforms.ColorJitter(
                brightness=0.2, contrast=0.2, saturation=0.2
            ))

        self.transform = transforms.Compose(transform_list)

    def preprocess(self, image):
        """Preprocess single image."""
        if isinstance(image, str):
            image = Image.open(image).convert('RGB')
        elif isinstance(image, np.ndarray):
            image = Image.fromarray(image)

        return self.transform(image)

    def preprocess_batch(self, images):
        """Preprocess batch of images."""
        return torch.stack([self.preprocess(img) for img in images])

# Usage
preprocessor = ImagePreprocessor(image_size=(224, 224), augment=True)
processed_image = preprocessor.preprocess("image.jpg")
```

### 8.2 Text Preprocessing

```python
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

class TextPreprocessor:
    """Preprocess text for ML."""

    def __init__(self, remove_stopwords=True, lemmatize=True, lowercase=True):
        self.remove_stopwords = remove_stopwords
        self.lemmatize = lemmatize
        self.lowercase = lowercase

        if remove_stopwords:
            nltk.download('stopwords')
            self.stop_words = set(stopwords.words('english'))

        if lemmatize:
            nltk.download('wordnet')
            self.lemmatizer = WordNetLemmatizer()

    def clean_text(self, text):
        """Clean text."""
        # Remove URLs
        text = re.sub(r'http\S+', '', text)
        # Remove email addresses
        text = re.sub(r'\S*@\S*', '', text)
        # Remove special characters
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        # Remove extra whitespace
        text = ' '.join(text.split())

        return text

    def tokenize(self, text):
        """Tokenize text."""
        return text.split()

    def preprocess(self, text):
        """Complete preprocessing pipeline."""
        # Clean text
        text = self.clean_text(text)

        # Lowercase
        if self.lowercase:
            text = text.lower()

        # Tokenize
        tokens = self.tokenize(text)

        # Remove stopwords
        if self.remove_stopwords:
            tokens = [token for token in tokens if token not in self.stop_words]

        # Lemmatize
        if self.lemmatize:
            tokens = [self.lemmatizer.lemmatize(token) for token in tokens]

        return ' '.join(tokens)

# Usage
preprocessor = TextPreprocessor(remove_stopwords=True, lemmatize=True)
processed_text = preprocessor.preprocess("This is a sample text for preprocessing!")
```

### 8.3 Tabular Preprocessing

```python
import pandas as pd
import numpy as np

class TabularPreprocessor:
    """Preprocess tabular data for ML."""

    def __init__(self):
        self.numeric_features = None
        self.categorical_features = None
        self.datetime_features = None

    def identify_features(self, X):
        """Identify feature types."""
        if isinstance(X, pd.DataFrame):
            self.numeric_features = X.select_dtypes(include=[np.number]).columns.tolist()
            self.categorical_features = X.select_dtypes(include=['object', 'category']).columns.tolist()
            self.datetime_features = X.select_dtypes(include=['datetime64']).columns.tolist()

        return {
            'numeric': self.numeric_features,
            'categorical': self.categorical_features,
            'datetime': self.datetime_features
        }

    def preprocess(self, X, handle_missing=True, scale=True, encode=True):
        """Complete preprocessing pipeline."""
        X_processed = X.copy()

        # Identify features
        feature_types = self.identify_features(X)

        # Handle missing values
        if handle_missing:
            handler = MissingValueHandler()
            X_processed = handler.fit_transform(X_processed)

        # Encode categorical variables
        if encode and self.categorical_features:
            encoder = CategoricalEncoder(method='onehot')
            X_processed = encoder.fit_transform(X_processed, self.categorical_features)

        # Scale numeric features
        if scale and self.numeric_features:
            scaler = DataScaler(method='standard')
            if isinstance(X_processed, pd.DataFrame):
                numeric_cols = X_processed.select_dtypes(include=[np.number]).columns
                X_processed[numeric_cols] = scaler.fit_transform(X_processed[numeric_cols])
            else:
                X_processed = scaler.fit_transform(X_processed)

        return X_processed

# Usage
preprocessor = TabularPreprocessor()
X_processed = preprocessor.preprocess(X_train)
```

---

## 9. Reproducibility

### 9.1 Random Seed Setting

```python
import random
import numpy as np
import torch

def set_seed(seed=42):
    """Set random seed for reproducibility."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

# Usage
set_seed(42)
```

### 9.2 Deterministic Preprocessing

```python
class DeterministicPreprocessor:
    """Deterministic preprocessing for reproducibility."""

    def __init__(self, seed=42):
        self.seed = seed
        set_seed(seed)

    def train_test_split(self, X, y, test_size=0.2, random_state=None):
        """Deterministic train-test split."""
        from sklearn.model_selection import train_test_split
        return train_test_split(
            X, y,
            test_size=test_size,
            random_state=random_state or self.seed,
            stratify=y
        )

    def kfold_split(self, X, y, n_splits=5, random_state=None):
        """Deterministic K-Fold split."""
        from sklearn.model_selection import StratifiedKFold
        kfold = StratifiedKFold(
            n_splits=n_splits,
            shuffle=True,
            random_state=random_state or self.seed
        )
        return kfold.split(X, y)

# Usage
preprocessor = DeterministicPreprocessor(seed=42)
X_train, X_test, y_train, y_test = preprocessor.train_test_split(X, y)
```

---

## 10. Testing Preprocessing

### 10.1 Unit Tests

```python
import unittest
import pandas as pd
import numpy as np

class TestPreprocessing(unittest.TestCase):
    """Unit tests for preprocessing."""

    def setUp(self):
        """Set up test data."""
        self.X = pd.DataFrame({
            'numeric': [1, 2, 3, 4, 5],
            'categorical': ['A', 'B', 'A', 'B', 'A'],
            'missing': [1, np.nan, 3, np.nan, 5]
        })

    def test_missing_value_handler(self):
        """Test missing value handler."""
        handler = MissingValueHandler()
        X_clean = handler.fit_transform(self.X)

        # Check no missing values
        self.assertFalse(X_clean.isnull().any().any())

    def test_data_scaler(self):
        """Test data scaler."""
        scaler = DataScaler(method='standard')
        X_scaled = scaler.fit_transform(self.X[['numeric']])

        # Check mean is approximately 0
        self.assertAlmostEqual(X_scaled.mean(), 0, places=5)

        # Check std is approximately 1
        self.assertAlmostEqual(X_scaled.std(), 1, places=5)

    def test_categorical_encoder(self):
        """Test categorical encoder."""
        encoder = CategoricalEncoder(method='label')
        X_encoded = encoder.fit_transform(self.X, ['categorical'])

        # Check categorical column is numeric
        self.assertTrue(pd.api.types.is_numeric_dtype(X_encoded['categorical']))

if __name__ == '__main__':
    unittest.main()
```

---

## Additional Resources

- [Scikit-learn Preprocessing](https://scikit-learn.org/stable/modules/preprocessing.html)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Feature Engineering Guide](https://www.kaggle.com/learn/feature-engineering)
