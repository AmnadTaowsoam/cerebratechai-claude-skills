---
name: Data Augmentation
description: Comprehensive guide for data augmentation techniques across images, text, audio, and tabular data.
---

# Data Augmentation

## Overview

Data augmentation is a technique used to artificially increase the size and diversity of training datasets by creating modified versions of existing data. This skill covers augmentation techniques for images, text, audio, and tabular data, including popular libraries like Albumentations, NLPAug, and custom augmentation strategies.

## Prerequisites

- Understanding of machine learning concepts
- Knowledge of Python programming
- Familiarity with data preprocessing
- Understanding of overfitting and generalization
- Basic knowledge of image, text, audio processing

## Key Concepts

### Augmentation Types

- **Image Augmentation**: Geometric transformations, color adjustments, noise injection
- **Text Augmentation**: Back-translation, synonym replacement, word insertion/deletion
- **Audio Augmentation**: Time stretching, pitch shifting, noise addition, masking
- **Tabular Augmentation**: SMOTE, ADASYN, Gaussian noise, feature mixup

### Augmentation Strategies

- **Online Augmentation**: Apply augmentation during training
- **Offline Augmentation**: Pre-compute augmented samples
- **Test-Time Augmentation (TTA)**: Apply multiple augmentations at inference time
- **AutoAugment**: Automatically search for optimal augmentation policies

### Common Libraries

- **Albumentations**: Fast and flexible image augmentation library
- **Torchvision**: PyTorch's built-in transforms
- **ImgAug**: Powerful image augmentation library
- **NLPAug**: Text augmentation library
- **Imbalanced-learn**: Tabular data augmentation (SMOTE, ADASYN)

## Implementation Guide

### Image Augmentation

#### Albumentations

```python
import albumentations as A
from albumentations.pytorch import ToTensorV2
import cv2
import numpy as np

class AlbumentationsAugmentor:
    """Image augmentation using Albumentations."""

    def __init__(self, mode='train', image_size=(224, 224)):
        self.mode = mode
        self.image_size = image_size
        self.transform = self._get_transform()

    def _get_transform(self):
        """Get transformation pipeline."""
        if self.mode == 'train':
            return A.Compose([
                A.Resize(height=self.image_size[0], width=self.image_size[1]),
                A.HorizontalFlip(p=0.5),
                A.VerticalFlip(p=0.2),
                A.RandomRotate90(p=0.5),
                A.Rotate(limit=30, p=0.5),
                A.ShiftScaleRotate(
                    shift_limit=0.1,
                    scale_limit=0.1,
                    rotate_limit=15,
                    p=0.5
                ),
                A.OneOf([
                    A.GaussNoise(p=1.0),
                    A.ISONoise(p=1.0),
                    A.MultiplicativeNoise(p=1.0),
                ], p=0.2),
                A.OneOf([
                    A.MotionBlur(p=1.0),
                    A.MedianBlur(p=1.0),
                    A.GaussianBlur(p=1.0),
                ], p=0.2),
                A.OneOf([
                    A.OpticalDistortion(p=1.0),
                    A.GridDistortion(p=1.0),
                    A.IAAPiecewiseAffine(p=1.0),
                ], p=0.2),
                A.OneOf([
                    A.CLAHE(clip_limit=2),
                    A.IAASharpen(),
                    A.IAAEmboss(),
                    A.RandomBrightnessContrast(),
                ], p=0.3),
                A.HueSaturationValue(p=0.3),
                A.RandomBrightnessContrast(p=0.3),
                A.Cutout(num_holes=8, max_h_size=16, max_w_size=16, p=0.3),
                A.CoarseDropout(
                    max_holes=8,
                    max_height=32,
                    max_width=32,
                    min_holes=1,
                    min_height=8,
                    min_width=8,
                    p=0.3
                ),
                A.Normalize(
                    mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225]
                ),
                ToTensorV2()
            ])
        else:
            return A.Compose([
                A.Resize(height=self.image_size[0], width=self.image_size[1]),
                A.Normalize(
                    mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225]
                ),
                ToTensorV2()
            ])

    def __call__(self, image):
        """Apply augmentation."""
        return self.transform(image=image)['image']

# Usage
train_augmentor = AlbumentationsAugmentor(mode='train', image_size=(224, 224))
val_augmentor = AlbumentationsAugmentor(mode='val', image_size=(224, 224))

# Apply augmentation
augmented_image = train_augmentor(original_image)
```

#### Torchvision Transforms

```python
import torchvision.transforms as transforms
from torchvision.transforms import functional as F

class TorchvisionAugmentor:
    """Image augmentation using torchvision."""

    def __init__(self, mode='train', image_size=224):
        self.mode = mode
        self.image_size = image_size
        self.transform = self._get_transform()

    def _get_transform(self):
        """Get transformation pipeline."""
        if self.mode == 'train':
            return transforms.Compose([
                transforms.Resize((self.image_size, self.image_size)),
                transforms.RandomHorizontalFlip(p=0.5),
                transforms.RandomVerticalFlip(p=0.2),
                transforms.RandomRotation(degrees=30),
                transforms.RandomAffine(
                    degrees=0,
                    translate=(0.1, 0.1),
                    scale=(0.9, 1.1),
                    shear=10
                ),
                transforms.ColorJitter(
                    brightness=0.3,
                    contrast=0.3,
                    saturation=0.3,
                    hue=0.1
                ),
                transforms.RandomGrayscale(p=0.1),
                transforms.RandomPerspective(distortion_scale=0.2, p=0.3),
                transforms.RandomResizedCrop(
                    self.image_size,
                    scale=(0.8, 1.0),
                    ratio=(0.9, 1.1)
                ),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225]
                )
            ])
        else:
            return transforms.Compose([
                transforms.Resize((self.image_size, self.image_size)),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225]
                )
            ])

    def __call__(self, image):
        """Apply augmentation."""
        return self.transform(image)

# Usage
train_transform = TorchvisionAugmentor(mode='train', image_size=224)
augmented_image = train_transform(pil_image)
```

#### ImgAug

```python
import imgaug as ia
import imgaug.augmenters as iaa

class ImgAugAugmentor:
    """Image augmentation using imgaug."""

    def __init__(self, mode='train'):
        self.mode = mode
        self.augmenter = self._get_augmenter()

    def _get_augmenter(self):
        """Get augmentation pipeline."""
        if self.mode == 'train':
            return iaa.Sequential([
                iaa.Fliplr(0.5),  # Horizontal flip
                iaa.Flipud(0.2),  # Vertical flip
                iaa.Affine(
                    rotate=(-30, 30),
                    scale=(0.9, 1.1),
                    translate_percent=(-0.1, 0.1)
                ),
                iaa.Multiply((0.8, 1.2)),  # Brightness
                iaa.LinearContrast((0.8, 1.2)),  # Contrast
                iaa.AdditiveGaussianNoise(scale=(0, 0.05 * 255)),
                iaa.GaussianBlur(sigma=(0, 1.0)),
                iaa.Dropout(p=(0, 0.2)),
                iaa.CoarseDropout(
                    (0.0, 0.05),
                    size_percent=(0.02, 0.05)
                ),
                iaa.Crop(percent=(0, 0.1)),
                iaa.Pad(percent=(0, 0.1)),
                iaa.ElasticTransformation(alpha=(0, 50), sigma=(0, 5)),
                iaa.PiecewiseAffine(scale=(0.01, 0.05)),
            ])
        else:
            return iaa.Sequential([])

    def __call__(self, image):
        """Apply augmentation."""
        if self.mode == 'train':
            image_aug = self.augmenter.augment_image(image)
            return image_aug
        return image

# Usage
train_augmentor = ImgAugAugmentor(mode='train')
augmented_image = train_augmentor(numpy_image)
```

### Text Augmentation

#### Back-Translation

```python
from deep_translator import GoogleTranslator
import random

class BackTranslationAugmentor:
    """Text augmentation using back-translation."""

    def __init__(self, languages=['fr', 'de', 'es']):
        self.languages = languages

    def augment(self, text, num_augmentations=1):
        """Augment text using back-translation."""
        augmented_texts = []

        for _ in range(num_augmentations):
            # Select random intermediate language
            intermediate_lang = random.choice(self.languages)

            try:
                # Translate to intermediate language
                translated = GoogleTranslator(
                    source='auto',
                    target=intermediate_lang
                ).translate(text)

                # Translate back to English
                back_translated = GoogleTranslator(
                    source=intermediate_lang,
                    target='en'
                ).translate(translated)

                augmented_texts.append(back_translated)
            except Exception as e:
                print(f"Back-translation failed: {e}")
                augmented_texts.append(text)

        return augmented_texts

# Usage
augmentor = BackTranslationAugmentor(languages=['fr', 'de', 'es'])
augmented_texts = augmentor.augment("This is a sample text for augmentation.")
```

#### Synonym Replacement

```python
import nltk
from nltk.corpus import wordnet
import random

nltk.download('wordnet')
nltk.download('omw-1.4')

class SynonymReplacementAugmentor:
    """Text augmentation using synonym replacement."""

    def __init__(self, replacement_prob=0.3):
        self.replacement_prob = replacement_prob

    def get_synonyms(self, word):
        """Get synonyms for a word."""
        synonyms = set()
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonym = lemma.name().replace('_', ' ')
                if synonym.lower() != word.lower():
                    synonyms.add(synonym)
        return list(synonyms)

    def augment(self, text):
        """Augment text with synonym replacement."""
        words = text.split()
        augmented_words = []

        for word in words:
            if random.random() < self.replacement_prob:
                synonyms = self.get_synonyms(word)
                if synonyms:
                    augmented_words.append(random.choice(synonyms))
                else:
                    augmented_words.append(word)
            else:
                augmented_words.append(word)

        return ' '.join(augmented_words)

# Usage
augmentor = SynonymReplacementAugmentor(replacement_prob=0.3)
augmented_text = augmentor.augment("The quick brown fox jumps over lazy dog")
```

#### NLPAug

```python
import nlpaug.augmenter.word as naw
import nlpaug.augmenter.char as nac
import nlpaug.augmenter.sentence as nas

class NLPAugAugmentor:
    """Text augmentation using NLPAug."""

    def __init__(self):
        # Word-level augmenters
        self.synonym_aug = naw.SynonymAug(aug_src='wordnet')
        self.contextual_aug = naw.ContextualWordEmbsAug(model_path='bert-base-uncased')
        self.back_translation_aug = naw.BackTranslationAug(
            from_model_name='facebook/wmt19-en-de',
            to_model_name='facebook/wmt19-de-en'
        )
        self.insertion_aug = naw.RandomWordAug(action="insert")
        self.swap_aug = naw.RandomWordAug(action="swap")
        self.deletion_aug = naw.RandomWordAug(action="delete")

        # Character-level augmenters
        self.ocr_aug = nac.OcrAug()
        self.keyboard_aug = nac.KeyboardAug()

        # Sentence-level augmenters
        self.synonym_sentence_aug = nas.ContextualWordEmbsForSentenceAug(
            model_path='bert-base-uncased'
        )

    def augment_word_level(self, text, method='synonym', num_augmentations=1):
        """Word-level augmentation."""
        augmented_texts = []

        for _ in range(num_augmentations):
            if method == 'synonym':
                augmented = self.synonym_aug.augment(text)
            elif method == 'contextual':
                augmented = self.contextual_aug.augment(text)
            elif method == 'insert':
                augmented = self.insertion_aug.augment(text)
            elif method == 'swap':
                augmented = self.swap_aug.augment(text)
            elif method == 'delete':
                augmented = self.deletion_aug.augment(text)
            else:
                augmented = text

            augmented_texts.append(augmented)

        return augmented_texts

    def augment_char_level(self, text, method='ocr', num_augmentations=1):
        """Character-level augmentation."""
        augmented_texts = []

        for _ in range(num_augmentations):
            if method == 'ocr':
                augmented = self.ocr_aug.augment(text)
            elif method == 'keyboard':
                augmented = self.keyboard_aug.augment(text)
            else:
                augmented = text

            augmented_texts.append(augmented)

        return augmented_texts

    def augment_sentence_level(self, text, num_augmentations=1):
        """Sentence-level augmentation."""
        augmented_texts = []

        for _ in range(num_augmentations):
            augmented = self.synonym_sentence_aug.augment(text)
            augmented_texts.append(augmented)

        return augmented_texts

# Usage
augmentor = NLPAugAugmentor()

# Word-level augmentation
augmented_texts = augmentor.augment_word_level(
    "This is a sample text.",
    method='synonym',
    num_augmentations=3
)

# Character-level augmentation
augmented_texts = augmentor.augment_char_level(
    "This is a sample text.",
    method='ocr',
    num_augmentations=3
)
```

### Audio Augmentation

```python
import numpy as np
import librosa
import soundfile as sf
from scipy.signal import butter, lfilter

class AudioAugmentor:
    """Audio augmentation for speech and music."""

    def __init__(self, sample_rate=16000):
        self.sample_rate = sample_rate

    def add_noise(self, audio, noise_factor=0.005):
        """Add Gaussian noise."""
        noise = np.random.randn(len(audio))
        augmented = audio + noise_factor * noise
        return augmented

    def time_shift(self, audio, shift_max=0.2):
        """Randomly shift audio in time."""
        shift = int(np.random.uniform(-shift_max, shift_max) * len(audio))
        return np.roll(audio, shift)

    def pitch_shift(self, audio, n_steps=2):
        """Shift pitch."""
        return librosa.effects.pitch_shift(audio, sr=self.sample_rate, n_steps=n_steps)

    def speed_change(self, audio, speed_factor=1.2):
        """Change speed."""
        return librosa.effects.time_stretch(audio, rate=speed_factor)

    def time_stretch(self, audio, rate=1.2):
        """Time stretching (changes duration)."""
        return librosa.effects.time_stretch(audio, rate=rate)

    def add_reverb(self, audio, decay=0.5):
        """Add reverberation."""
        delay = int(0.05 * self.sample_rate)
        impulse = np.zeros(delay + int(decay * self.sample_rate))
        impulse[delay] = 1
        impulse[delay:] *= np.exp(-np.arange(len(impulse) - delay) / (decay * self.sample_rate))

        augmented = np.convolve(audio, impulse)[:len(audio)]
        return augmented

    def frequency_mask(self, audio, freq_mask_param=10):
        """Frequency masking (for spectrograms)."""
        freq_mask = np.random.randint(0, freq_mask_param + 1)
        f0 = np.random.uniform(0, freq_mask_param - freq_mask)
        f0 = int(f0)
        augmented = audio.copy()
        augmented[f0:f0 + freq_mask, :] = 0
        return augmented

    def time_mask(self, audio, time_mask_param=10):
        """Time masking (for spectrograms)."""
        time_mask = np.random.randint(0, time_mask_param + 1)
        t0 = np.random.uniform(0, time_mask_param - time_mask)
        t0 = int(t0)
        augmented = audio.copy()
        augmented[:, t0:t0 + time_mask] = 0
        return augmented

    def augment(self, audio, augmentations=None):
        """Apply random augmentations."""
        if augmentations is None:
            augmentations = [
                ('noise', 0.3),
                ('time_shift', 0.3),
                ('pitch_shift', 0.2),
                ('speed_change', 0.2)
            ]

        augmented = audio.copy()

        for aug_name, prob in augmentations:
            if np.random.random() < prob:
                if aug_name == 'noise':
                    augmented = self.add_noise(augmented)
                elif aug_name == 'time_shift':
                    augmented = self.time_shift(augmented)
                elif aug_name == 'pitch_shift':
                    n_steps = np.random.randint(-2, 3)
                    augmented = self.pitch_shift(augmented, n_steps)
                elif aug_name == 'speed_change':
                    speed = np.random.uniform(0.8, 1.2)
                    augmented = self.speed_change(augmented, speed)

        return augmented

# Usage
augmentor = AudioAugmentor(sample_rate=16000)
augmented_audio = augmentor.augment(original_audio)
```

### Tabular Data Augmentation

```python
import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE, ADASYN
from imblearn.under_sampling import RandomUnderSampler

class TabularAugmentor:
    """Augmentation for tabular data."""

    def __init__(self):
        self.smote = None
        self.adasyn = None

    def smote_augmentation(self, X, y, sampling_strategy='auto'):
        """SMOTE oversampling."""
        self.smote = SMOTE(sampling_strategy=sampling_strategy, random_state=42)
        X_resampled, y_resampled = self.smote.fit_resample(X, y)
        return X_resampled, y_resampled

    def adasyn_augmentation(self, X, y, sampling_strategy='auto'):
        """ADASYN oversampling."""
        self.adasyn = ADASYN(sampling_strategy=sampling_strategy, random_state=42)
        X_resampled, y_resampled = self.adasyn.fit_resample(X, y)
        return X_resampled, y_resampled

    def random_oversampling(self, X, y):
        """Random oversampling."""
        from imblearn.over_sampling import RandomOverSampler
        ros = RandomOverSampler(random_state=42)
        X_resampled, y_resampled = ros.fit_resample(X, y)
        return X_resampled, y_resampled

    def random_undersampling(self, X, y, sampling_strategy='auto'):
        """Random undersampling."""
        rus = RandomUnderSampler(sampling_strategy=sampling_strategy, random_state=42)
        X_resampled, y_resampled = rus.fit_resample(X, y)
        return X_resampled, y_resampled

    def gaussian_noise_augmentation(self, X, noise_level=0.01):
        """Add Gaussian noise to features."""
        noise = np.random.normal(0, noise_level, X.shape)
        X_augmented = X + noise
        return X_augmented

    def feature_mixup(self, X, y, alpha=0.2, n_samples=100):
        """Feature mixup augmentation."""
        X_augmented = []
        y_augmented = []

        for _ in range(n_samples):
            # Sample two random indices
            idx1, idx2 = np.random.choice(len(X), 2, replace=False)

            # Mix features
            lam = np.random.beta(alpha, alpha)
            x_mixed = lam * X[idx1] + (1 - lam) * X[idx2]

            X_augmented.append(x_mixed)
            y_augmented.append(y[idx1])  # Use label from first sample

        return np.array(X_augmented), np.array(y_augmented)

    def bootstrap_sampling(self, X, y, n_samples=None):
        """Bootstrap sampling."""
        if n_samples is None:
            n_samples = len(X)

        indices = np.random.choice(len(X), n_samples, replace=True)
        X_bootstrapped = X[indices]
        y_bootstrapped = y[indices]

        return X_bootstrapped, y_bootstrapped

# Usage
augmentor = TabularAugmentor()

# SMOTE augmentation
X_augmented, y_augmented = augmentor.smote_augmentation(X_train, y_train)

# Gaussian noise augmentation
X_noisy = augmentor.gaussian_noise_augmentation(X_train, noise_level=0.01)

# Feature mixup
X_mixup, y_mixup = augmentor.feature_mixup(X_train, y_train, n_samples=100)
```

### Augmentation Strategies

#### Online vs Offline Augmentation

```python
class OnlineAugmentation:
    """Apply augmentation during training (online)."""

    def __init__(self, augmentor):
        self.augmentor = augmentor

    def __call__(self, batch):
        """Apply augmentation to batch."""
        augmented_batch = []
        for item in batch:
            augmented_item = self.augmentor(item)
            augmented_batch.append(augmented_item)
        return augmented_batch

# Usage with PyTorch DataLoader
from torch.utils.data import Dataset, DataLoader

class OnlineAugmentedDataset(Dataset):
    """Dataset with online augmentation."""

    def __init__(self, data, labels, augmentor):
        self.data = data
        self.labels = labels
        self.augmentor = augmentor

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        label = self.labels[idx]

        # Apply augmentation during training
        augmented_item = self.augmentor(item)

        return augmented_item, label

# Create dataset with online augmentation
dataset = OnlineAugmentedDataset(X_train, y_train, augmentor)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
```

```python
class OfflineAugmentation:
    """Pre-compute augmented samples (offline)."""

    def __init__(self, augmentor, augmentations_per_sample=2):
        self.augmentor = augmentor
        self.augmentations_per_sample = augmentations_per_sample

    def augment_dataset(self, X, y):
        """Create augmented dataset."""
        X_augmented = []
        y_augmented = []

        for i in range(len(X)):
            # Add original sample
            X_augmented.append(X[i])
            y_augmented.append(y[i])

            # Add augmented samples
            for _ in range(self.augmentations_per_sample):
                augmented = self.augmentor(X[i])
                X_augmented.append(augmented)
                y_augmented.append(y[i])

        return np.array(X_augmented), np.array(y_augmented)

# Usage
offline_augmentor = OfflineAugmentation(augmentor, augmentations_per_sample=2)
X_augmented, y_augmented = offline_augmentor.augment_dataset(X_train, y_train)
```

#### Probability Settings

```python
class ProbabilisticAugmentor:
    """Augmentor with probability-based application."""

    def __init__(self):
        self.augmentations = []

    def add_augmentation(self, augmentor, probability=0.5):
        """Add augmentation with probability."""
        self.augmentations.append((augmentor, probability))

    def augment(self, data):
        """Apply augmentations based on probabilities."""
        augmented_data = data

        for augmentor, prob in self.augmentations:
            if np.random.random() < prob:
                augmented_data = augmentor(augmented_data)

        return augmented_data

# Usage
prob_augmentor = ProbabilisticAugmentor()
prob_augmentor.add_augmentation(horizontal_flip, probability=0.5)
prob_augmentor.add_augmentation(rotation, probability=0.3)
prob_augmentor.add_augmentation(color_jitter, probability=0.4)

augmented_data = prob_augmentor.augment(original_data)
```

### Custom Augmentations

```python
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

class CustomAugmentor:
    """Custom augmentation functions."""

    @staticmethod
    def cutout(image, n_holes=8, max_h_size=16, max_w_size=16):
        """Cutout augmentation."""
        if isinstance(image, Image.Image):
            image = np.array(image)

        h, w = image.shape[:2]

        for _ in range(n_holes):
            y = np.random.randint(h)
            x = np.random.randint(w)

            y1 = np.clip(y - max_h_size // 2, 0, h)
            y2 = np.clip(y + max_h_size // 2, 0, h)
            x1 = np.clip(x - max_w_size // 2, 0, w)
            x2 = np.clip(x + max_w_size // 2, 0, w)

            if len(image.shape) == 3:
                image[y1:y2, x1:x2, :] = 0
            else:
                image[y1:y2, x1:x2] = 0

        return image

    @staticmethod
    def mixup(image1, image2, alpha=0.2):
        """Mixup augmentation."""
        if isinstance(image1, Image.Image):
            image1 = np.array(image1)
        if isinstance(image2, Image.Image):
            image2 = np.array(image2)

        lam = np.random.beta(alpha, alpha)
        mixed = lam * image1 + (1 - lam) * image2

        return mixed.astype(np.uint8)

    @staticmethod
    def cutmix(image1, image2, alpha=1.0):
        """CutMix augmentation."""
        if isinstance(image1, Image.Image):
            image1 = np.array(image1)
        if isinstance(image2, Image.Image):
            image2 = np.array(image2)

        h, w = image1.shape[:2]

        # Generate random bounding box
        lam = np.random.beta(alpha, alpha)
        cut_rat = np.sqrt(1. - lam)
        cut_w = int(w * cut_rat)
        cut_h = int(h * cut_rat)

        cx = np.random.randint(w)
        cy = np.random.randint(h)

        bbx1 = np.clip(cx - cut_w // 2, 0, w)
        bby1 = np.clip(cy - cut_h // 2, 0, h)
        bbx2 = np.clip(cx + cut_w // 2, 0, w)
        bby2 = np.clip(cy + cut_h // 2, 0, h)

        # Apply cutmix
        mixed = image1.copy()
        mixed[bby1:bby2, bbx1:bbx2] = image2[bby1:bby2, bbx1:bbx2]

        return mixed

    @staticmethod
    def mosaic(images):
        """Mosaic augmentation (4 images)."""
        if len(images) != 4:
            raise ValueError("Mosaic requires exactly 4 images")

        h, w = images[0].shape[:2]
        mosaic = np.zeros((h * 2, w * 2, images[0].shape[2]), dtype=images[0].dtype)

        # Place images in 2x2 grid
        mosaic[:h, :w] = images[0]
        mosaic[:h, w:] = images[1]
        mosaic[h:, :w] = images[2]
        mosaic[h:, w:] = images[3]

        return mosaic

# Usage
# Cutout
cutout_image = CustomAugmentor.cutout(image, n_holes=8, max_h_size=32)

# Mixup
mixed_image = CustomAugmentor.mixup(image1, image2, alpha=0.2)

# CutMix
cutmix_image = CustomAugmentor.cutmix(image1, image2, alpha=1.0)

# Mosaic
mosaic_image = CustomAugmentor.mosaic([img1, img2, img3, img4])
```

### Validation Set Handling

```python
class ValidationAugmentation:
    """Handle augmentation for validation sets."""

    def __init__(self, augmentor):
        self.augmentor = augmentor

    def augment_with_test_time_augmentation(self, data, n_augmentations=5):
        """Test-time augmentation (TTA)."""
        augmented_samples = []

        # Create multiple augmented versions
        for _ in range(n_augmentations):
            augmented = self.augmentor(data)
            augmented_samples.append(augmented)

        return augmented_samples

    def average_predictions(self, predictions):
        """Average predictions from TTA."""
        return np.mean(predictions, axis=0)

# Usage
val_augmentor = ValidationAugmentation(augmentor)

# Test-time augmentation
augmented_samples = val_augmentor.augment_with_test_time_augmentation(
    validation_sample,
    n_augmentations=5
)

# Get predictions for each augmented sample
predictions = [model.predict(sample) for sample in augmented_samples]

# Average predictions
final_prediction = val_augmentor.average_predictions(predictions)
```

### Production Considerations

#### Efficient Augmentation

```python
import multiprocessing as mp
from functools import partial

class EfficientAugmentor:
    """Efficient augmentation using multiprocessing."""

    def __init__(self, augmentor, n_workers=None):
        self.augmentor = augmentor
        self.n_workers = n_workers or mp.cpu_count()

    def augment_batch(self, batch):
        """Augment a batch of samples."""
        with mp.Pool(self.n_workers) as pool:
            augmented_batch = pool.map(self.augmentor, batch)
        return augmented_batch

    def augment_dataset(self, dataset, batch_size=32):
        """Augment entire dataset efficiently."""
        augmented_data = []

        for i in range(0, len(dataset), batch_size):
            batch = dataset[i:i + batch_size]
            augmented_batch = self.augment_batch(batch)
            augmented_data.extend(augmented_batch)

        return augmented_data

# Usage
efficient_augmentor = EfficientAugmentor(augmentor, n_workers=4)
augmented_data = efficient_augmentor.augment_dataset(X_train, batch_size=32)
```

#### Augmentation Caching

```python
import hashlib
import pickle
from pathlib import Path

class CachedAugmentor:
    """Augmentor with caching for reproducibility."""

    def __init__(self, augmentor, cache_dir='./augmentation_cache'):
        self.augmentor = augmentor
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_key(self, data):
        """Generate cache key for data."""
        if isinstance(data, np.ndarray):
            data_bytes = data.tobytes()
        elif isinstance(data, (str, bytes)):
            data_bytes = data.encode() if isinstance(data, str) else data
        else:
            data_bytes = pickle.dumps(data)

        return hashlib.md5(data_bytes).hexdigest()

    def augment(self, data, use_cache=True):
        """Augment with caching."""
        cache_key = self._get_cache_key(data)
        cache_file = self.cache_dir / f"{cache_key}.pkl"

        if use_cache and cache_file.exists():
            with open(cache_file, 'rb') as f:
                return pickle.load(f)

        # Apply augmentation
        augmented = self.augmentor(data)

        # Cache result
        if use_cache:
            with open(cache_file, 'wb') as f:
                pickle.dump(augmented, f)

        return augmented

# Usage
cached_augmentor = CachedAugmentor(augmentor)
augmented_data = cached_augmentor.augment(original_data)
```

### Common Patterns

#### AutoAugment

```python
import random

class AutoAugment:
    """AutoAugment policy."""

    def __init__(self):
        self.policies = [
            ('rotate', 30, 0.5),
            ('translate_x', 0.1, 0.5),
            ('translate_y', 0.1, 0.5),
            ('shear_x', 0.1, 0.5),
            ('shear_y', 0.1, 0.5),
            ('contrast', 0.3, 0.5),
            ('brightness', 0.3, 0.5),
            ('sharpness', 0.3, 0.5),
            ('posterize', 4, 0.5),
            ('solarize', 256, 0.5),
        ]

    def apply_policy(self, image):
        """Apply random policy."""
        # Select 2 random policies
        selected_policies = random.sample(self.policies, 2)

        augmented = image
        for policy_name, magnitude, prob in selected_policies:
            if random.random() < prob:
                augmented = self._apply_transform(augmented, policy_name, magnitude)

        return augmented

    def _apply_transform(self, image, transform_name, magnitude):
        """Apply specific transform."""
        # Implement each transform
        if transform_name == 'rotate':
            return self._rotate(image, magnitude)
        elif transform_name == 'translate_x':
            return self._translate_x(image, magnitude)
        # ... other transforms

        return image

# Usage
autoaugment = AutoAugment()
augmented_image = autoaugment.apply_policy(original_image)
```

#### RandAugment

```python
class RandAugment:
    """RandAugment policy."""

    def __init__(self, n=2, m=10):
        self.n = n  # Number of augmentations
        self.m = m  # Magnitude

        self.augmentations = [
            self._rotate,
            self._translate_x,
            self._translate_y,
            self._shear_x,
            self._shear_y,
            self._contrast,
            self._brightness,
            self._sharpness,
        ]

    def __call__(self, image):
        """Apply RandAugment."""
        # Select n random augmentations
        selected = random.choices(self.augmentations, k=self.n)

        augmented = image
        for aug in selected:
            augmented = aug(augmented, self.m)

        return augmented

    def _rotate(self, image, magnitude):
        """Random rotation."""
        angle = random.uniform(-magnitude, magnitude)
        return self._rotate_image(image, angle)

    def _contrast(self, image, magnitude):
        """Random contrast."""
        factor = random.uniform(1 - magnitude/10, 1 + magnitude/10)
        return self._adjust_contrast(image, factor)

    # ... other augmentation methods

# Usage
randaugment = RandAugment(n=2, m=10)
augmented_image = randaugment(original_image)
```

## Best Practices

1. **Start Simple**
   - Begin with basic augmentations (flip, rotate)
   - Gradually increase complexity
   - Monitor impact on model performance

2. **Use Appropriate Augmentations**
   - Classification: More aggressive augmentations
   - Detection: Careful with spatial augmentations (need to adjust bounding boxes)
   - Segmentation: Apply same augmentations to both image and mask

3. **Don't Augment Validation/Test Sets**
   - Only apply normalization, not augmentation
   - Use test-time augmentation (TTA) for inference

4. **Monitor Performance**
   - Track training/validation loss with and without augmentation
   - Use visualization to verify augmentations
   - Check label preservation after augmentation

5. **Use Probability-Based Application**
   - Apply augmentations with appropriate probabilities
   - Avoid over-augmentation that distorts data
   - Balance between diversity and data quality

6. **Handle Class Imbalance**
   - Use SMOTE or ADASYN for tabular data
   - Apply more augmentation to minority classes
   - Consider weighted sampling

7. **Optimize Performance**
   - Use multiprocessing for batch augmentation
   - Cache augmented samples when possible
   - Use efficient libraries like Albumentations

8. **Debug Augmentations**
   - Visualize augmented samples
   - Check label preservation
   - Verify augmentation pipeline correctness

9. **Consider Task-Specific Needs**
   - Medical imaging: Limited augmentations
   - Satellite imagery: Rotation-invariant augmentations
   - Text: Preserve semantic meaning

10. **Reproducibility**
    - Set random seeds for consistent results
    - Cache augmentations for debugging
    - Document augmentation pipeline

## Related Skills

- [`05-ai-ml-core/data-preprocessing`](05-ai-ml-core/data-preprocessing/SKILL.md)
- [`05-ai-ml-core/model-training`](05-ai-ml-core/model-training/SKILL.md)
- [`05-ai-ml-core/model-optimization`](05-ai-ml-core/model-optimization/SKILL.md)
- [`06-ai-ml-production/llm-integration`](06-ai-ml-production/llm-integration/SKILL.md)
