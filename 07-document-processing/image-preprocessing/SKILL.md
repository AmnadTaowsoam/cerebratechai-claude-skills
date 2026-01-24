---
name: Image Preprocessing
description: Comprehensive guide to image preprocessing for OCR and computer vision tasks using Python and OpenCV
---

# Image Preprocessing

## Overview

Comprehensive guide to image preprocessing for OCR and computer vision tasks using Python and OpenCV.

## Prerequisites

- **Python Programming**: Intermediate level Python knowledge
- **OpenCV Basics**: Understanding of image processing fundamentals
- **NumPy**: Familiarity with array operations and matrix manipulations
- **PIL/Pillow**: Basic knowledge of image loading and manipulation
- **Computer Vision Concepts**: Understanding of pixels, color spaces, and image representations

## Key Concepts

- **Color Spaces**: RGB, Grayscale, HSV, LAB, and YUV color models
- **Image Filtering**: Gaussian blur, median filter, bilateral filter for noise reduction
- **Thresholding**: Binary, Otsu's, and adaptive thresholding techniques
- **Morphological Operations**: Erosion, dilation, opening, closing for shape manipulation
- **Edge Detection**: Canny, Sobel, and Laplacian edge detection algorithms
- **Deskewing**: Image rotation and skew correction using Hough transform and projection profiles
- **Contrast Enhancement**: Histogram equalization and CLAHE for improving image quality
- **OCR Optimization**: Text region extraction, line removal, and document enhancement

## Table of Contents

1. [Image Loading](#image-loading)
2. [Color Space Conversion](#color-space-conversion)
3. [Resizing and Scaling](#resizing-and-scaling)
4. [Noise Reduction](#noise-reduction)
5. [Thresholding](#thresholding)
6. [Morphological Operations](#morphological-operations)
7. [Edge Detection](#edge-detection)
8. [Deskewing](#deskewing)
9. [Contrast Enhancement](#contrast-enhancement)
10. [OCR-Specific Preprocessing](#ocr-specific-preprocessing)
11. [Pipeline Creation](#pipeline-creation)
12. [Best Practices](#best-practices)

---

## Image Loading

### Using PIL (Pillow)

```python
from PIL import Image
import numpy as np

def load_image_pil(image_path: str) -> Image.Image:
    """Load image using PIL"""
    image = Image.open(image_path)
    return image

def load_image_with_mode(image_path: str, mode: str = 'L') -> Image.Image:
    """Load image with specific mode"""
    image = Image.open(image_path)
    
    # Convert mode
    if mode:
        image = image.convert(mode)
    
    return image

# Modes: 'L' (grayscale), 'RGB', 'RGBA', 'CMYK'
image = load_image_with_mode('document.png', mode='L')
```

### Using OpenCV

```python
import cv2
import numpy as np

def load_image_opencv(image_path: str, flags: int = cv2.IMREAD_COLOR) -> np.ndarray:
    """Load image using OpenCV"""
    image = cv2.imread(image_path, flags)
    
    if image is None:
        raise ValueError(f"Failed to load image: {image_path}")
    
    return image

def load_image_as_grayscale(image_path: str) -> np.ndarray:
    """Load image as grayscale"""
    return cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

def load_image_with_alpha(image_path: str) -> np.ndarray:
    """Load image with alpha channel"""
    return cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
```

### Image Information

```python
def get_image_info(image: np.ndarray) -> dict:
    """Get image information"""
    if len(image.shape) == 2:
        height, width = image.shape
        channels = 1
    else:
        height, width, channels = image.shape
    
    return {
        'height': height,
        'width': width,
        'channels': channels,
        'dtype': image.dtype,
        'size': image.size,
        'shape': image.shape
    }

# Usage
info = get_image_info(image)
print(f"Image: {info['width']}x{info['height']}, {info['channels']} channels")
```

---

## Color Space Conversion

### RGB to Grayscale

```python
import cv2

def rgb_to_grayscale(image: np.ndarray) -> np.ndarray:
    """Convert RGB to grayscale"""
    if len(image.shape) == 2:
        return image  # Already grayscale
    
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def rgb_to_grayscale_pil(image: Image.Image) -> Image.Image:
    """Convert RGB to grayscale using PIL"""
    return image.convert('L')
```

### Other Color Conversions

```python
def convert_color_space(image: np.ndarray, conversion: str) -> np.ndarray:
    """Convert between color spaces"""
    conversions = {
        'BGR2GRAY': cv2.COLOR_BGR2GRAY,
        'BGR2RGB': cv2.COLOR_BGR2RGB,
        'BGR2HSV': cv2.COLOR_BGR2HSV,
        'BGR2LAB': cv2.COLOR_BGR2LAB,
        'BGR2YUV': cv2.COLOR_BGR2YUV,
        'RGB2GRAY': cv2.COLOR_RGB2GRAY,
        'RGB2HSV': cv2.COLOR_RGB2HSV,
        'RGB2LAB': cv2.COLOR_RGB2LAB,
    }
    
    if conversion in conversions:
        return cv2.cvtColor(image, conversions[conversion])
    else:
        raise ValueError(f"Unknown conversion: {conversion}")

# Examples
gray = convert_color_space(image, 'BGR2GRAY')
hsv = convert_color_space(image, 'BGR2HSV')
lab = convert_color_space(image, 'BGR2LAB')
```

---

## Resizing and Scaling

### Basic Resizing

```python
import cv2

def resize_image(image: np.ndarray, width: int = None, height: int = None) -> np.ndarray:
    """Resize image maintaining aspect ratio"""
    if width is None and height is None:
        return image
    
    # Get original dimensions
    h, w = image.shape[:2]
    
    # Calculate new dimensions
    if width is None:
        ratio = height / h
        new_width = int(w * ratio)
        new_height = height
    elif height is None:
        ratio = width / w
        new_width = width
        new_height = int(h * ratio)
    else:
        new_width = width
        new_height = height
    
    # Resize
    return cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)

def resize_to_fixed_size(image: np.ndarray, width: int, height: int) -> np.ndarray:
    """Resize to fixed size (may distort)"""
    return cv2.resize(image, (width, height))
```

### Smart Resizing

```python
def resize_with_padding(image: np.ndarray, target_width: int, target_height: int) -> np.ndarray:
    """Resize with padding to maintain aspect ratio"""
    h, w = image.shape[:2]
    
    # Calculate scaling factor
    scale = min(target_width / w, target_height / h)
    new_w = int(w * scale)
    new_h = int(h * scale)
    
    # Resize
    resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
    
    # Create canvas with padding
    canvas = np.zeros((target_height, target_width, 3), dtype=np.uint8)
    
    # Calculate padding
    pad_x = (target_width - new_w) // 2
    pad_y = (target_height - new_h) // 2
    
    # Place image on canvas
    if len(resized.shape) == 2:
        canvas[pad_y:pad_y+new_h, pad_x:pad_x+new_w] = resized
    else:
        canvas[pad_y:pad_y+new_h, pad_x:pad_x+new_w] = resized
    
    return canvas

def resize_ocr_optimized(image: np.ndarray, min_width: int = 2000) -> np.ndarray:
    """Resize for optimal OCR"""
    h, w = image.shape[:2]
    
    if w < min_width:
        scale = min_width / w
        new_w = min_width
        new_h = int(h * scale)
        return cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
    
    return image
```

---

## Noise Reduction

### Gaussian Blur

```python
import cv2

def gaussian_blur(image: np.ndarray, kernel_size: int = 5, sigma: float = 0) -> np.ndarray:
    """Apply Gaussian blur"""
    # Kernel size must be odd and positive
    if kernel_size % 2 == 0:
        kernel_size += 1
    
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)

def adaptive_gaussian_blur(image: np.ndarray, sigma: float = 1.0) -> np.ndarray:
    """Adaptive Gaussian blur based on image size"""
    h, w = image.shape[:2]
    kernel_size = max(3, min(w, h) // 50)
    if kernel_size % 2 == 0:
        kernel_size += 1
    
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)
```

### Median Filter

```python
def median_filter(image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
    """Apply median filter (good for salt-and-pepper noise)"""
    # Kernel size must be odd
    if kernel_size % 2 == 0:
        kernel_size += 1
    
    return cv2.medianBlur(image, kernel_size)

def denoise_image(image: np.ndarray) -> np.ndarray:
    """Apply denoising"""
    # For color images
    if len(image.shape) == 3:
        return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
    # For grayscale
    else:
        return cv2.fastNlMeansDenoising(image, None, 10, 7, 21)
```

### Bilateral Filter

```python
def bilateral_filter(image: np.ndarray, d: int = 9, sigma_color: float = 75, sigma_space: float = 75) -> np.ndarray:
    """Apply bilateral filter (edge-preserving)"""
    return cv2.bilateralFilter(image, d, sigma_color, sigma_space)

def denoise_preserve_edges(image: np.ndarray) -> np.ndarray:
    """Denoise while preserving edges"""
    return bilateral_filter(image, d=9, sigma_color=75, sigma_space=75)
```

---

## Thresholding

### Binary Thresholding

```python
import cv2

def binary_threshold(image: np.ndarray, threshold: int = 127) -> np.ndarray:
    """Apply binary thresholding"""
    _, binary = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
    return binary

def binary_threshold_inverse(image: np.ndarray, threshold: int = 127) -> np.ndarray:
    """Apply inverse binary thresholding"""
    _, binary = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY_INV)
    return binary
```

### Otsu's Thresholding

```python
def otsu_threshold(image: np.ndarray) -> np.ndarray:
    """Apply Otsu's automatic thresholding"""
    _, binary = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary

def otsu_with_threshold_value(image: np.ndarray) -> tuple:
    """Apply Otsu's and return threshold value"""
    threshold, binary = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return threshold, binary
```

### Adaptive Thresholding

```python
def adaptive_threshold_mean(image: np.ndarray, block_size: int = 11, c: int = 2) -> np.ndarray:
    """Apply adaptive thresholding with mean"""
    return cv2.adaptiveThreshold(
        image, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY, block_size, c
    )

def adaptive_threshold_gaussian(image: np.ndarray, block_size: int = 11, c: int = 2) -> np.ndarray:
    """Apply adaptive thresholding with Gaussian"""
    return cv2.adaptiveThreshold(
        image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, block_size, c
    )
```

### Thresholding Pipeline

```python
def smart_threshold(image: np.ndarray) -> np.ndarray:
    """Smart thresholding based on image characteristics"""
    # Try Otsu first
    _, otsu = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Check if Otsu produced good results
    white_ratio = np.sum(otsu == 255) / otsu.size
    
    if 0.1 < white_ratio < 0.9:
        return otsu
    else:
        # Fall back to adaptive thresholding
        return adaptive_threshold_gaussian(image)
```

---

## Morphological Operations

### Erosion and Dilation

```python
import cv2
import numpy as np

def erode(image: np.ndarray, kernel_size: int = 3, iterations: int = 1) -> np.ndarray:
    """Apply erosion"""
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.erode(image, kernel, iterations=iterations)

def dilate(image: np.ndarray, kernel_size: int = 3, iterations: int = 1) -> np.ndarray:
    """Apply dilation"""
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.dilate(image, kernel, iterations=iterations)
```

### Opening and Closing

```python
def opening(image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
    """Apply opening (erosion followed by dilation)"""
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

def closing(image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
    """Apply closing (dilation followed by erosion)"""
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
```

### Advanced Morphology

```python
def morphological_gradient(image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
    """Apply morphological gradient"""
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel)

def top_hat(image: np.ndarray, kernel_size: int = 9) -> np.ndarray:
    """Apply top-hat transform"""
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    return cv2.morphologyEx(image, cv2.MORPH_TOPHAT, kernel)

def black_hat(image: np.ndarray, kernel_size: int = 9) -> np.ndarray:
    """Apply black-hat transform"""
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    return cv2.morphologyEx(image, cv2.MORPH_BLACKHAT, kernel)
```

### Custom Kernels

```python
def custom_kernel_operation(image: np.ndarray, kernel: np.ndarray, operation: str = 'dilate') -> np.ndarray:
    """Apply custom kernel operation"""
    operations = {
        'erode': cv2.MORPH_ERODE,
        'dilate': cv2.MORPH_DILATE,
        'open': cv2.MORPH_OPEN,
        'close': cv2.MORPH_CLOSE
    }
    
    if operation in operations:
        return cv2.morphologyEx(image, operations[operation], kernel)
    else:
        raise ValueError(f"Unknown operation: {operation}")

# Create custom kernel
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
result = custom_kernel_operation(image, kernel, 'dilate')
```

---

## Edge Detection

### Canny Edge Detection

```python
import cv2

def canny_edges(image: np.ndarray, threshold1: int = 50, threshold2: int = 150) -> np.ndarray:
    """Apply Canny edge detection"""
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    return cv2.Canny(gray, threshold1, threshold2)

def auto_canny(image: np.ndarray, sigma: float = 0.33) -> np.ndarray:
    """Auto Canny edge detection with automatic thresholds"""
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    # Compute median
    v = np.median(gray)
    
    # Apply automatic Canny edge detection
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    
    return cv2.Canny(gray, lower, upper)
```

### Sobel Edge Detection

```python
def sobel_edges(image: np.ndarray) -> tuple:
    """Apply Sobel edge detection"""
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    # Sobel in x and y directions
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    
    # Convert to absolute values
    sobel_x = np.uint8(np.absolute(sobel_x))
    sobel_y = np.uint8(np.absolute(sobel_y))
    
    # Combine
    sobel_combined = cv2.addWeighted(sobel_x, 0.5, sobel_y, 0.5, 0)
    
    return sobel_x, sobel_y, sobel_combined
```

### Laplacian Edge Detection

```python
def laplacian_edges(image: np.ndarray) -> np.ndarray:
    """Apply Laplacian edge detection"""
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    # Apply Laplacian
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    laplacian = np.uint8(np.absolute(laplacian))
    
    return laplacian
```

---

## Deskewing

### Hough Transform Deskewing

```python
import cv2
import numpy as np

def deskew_hough(image: np.ndarray) -> np.ndarray:
    """Deskew image using Hough transform"""
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    # Threshold
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Detect lines
    lines = cv2.HoughLinesP(binary, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)
    
    if lines is None:
        return image
    
    # Calculate angles
    angles = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
        angles.append(angle)
    
    # Use median angle
    median_angle = np.median(angles)
    
    # Rotate image
    return rotate_image(image, -median_angle)
```

### Projection Profile Deskewing

```python
def deskew_projection(image: np.ndarray) -> np.ndarray:
    """Deskew using projection profile"""
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    # Threshold
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Find angle
    coords = np.column_stack(np.where(binary > 0))
    angle = cv2.minAreaRect(coords)[-1]
    
    # Adjust angle
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    
    # Rotate image
    return rotate_image(image, angle)
```

### Image Rotation

```python
def rotate_image(image: np.ndarray, angle: float) -> np.ndarray:
    """Rotate image by angle"""
    # Get image dimensions
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    
    # Get rotation matrix
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    
    # Calculate new dimensions
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    new_w = int((h * sin) + (w * cos))
    new_h = int((h * cos) + (w * sin))
    
    # Adjust rotation matrix
    M[0, 2] += (new_w / 2) - center[0]
    M[1, 2] += (new_h / 2) - center[1]
    
    # Rotate
    rotated = cv2.warpAffine(image, M, (new_w, new_h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    
    return rotated
```

---

## Contrast Enhancement

### Histogram Equalization

```python
import cv2

def histogram_equalization(image: np.ndarray) -> np.ndarray:
    """Apply histogram equalization"""
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    return cv2.equalizeHist(gray)

def clahe(image: np.ndarray, clip_limit: float = 2.0, tile_grid_size: tuple = (8, 8)) -> np.ndarray:
    """Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)"""
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    return clahe.apply(gray)
```

### Brightness and Contrast Adjustment

```python
def adjust_brightness_contrast(image: np.ndarray, brightness: int = 0, contrast: int = 0) -> np.ndarray:
    """Adjust brightness and contrast"""
    # Brightness: -100 to 100
    # Contrast: -100 to 100
    
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow) / 255
        gamma_b = shadow
        buf = cv2.addWeighted(image, alpha_b, image, 0, gamma_b)
    else:
        buf = image.copy()
    
    if contrast != 0:
        f = 131 * (contrast + 127) / (127 * (131 - contrast))
        alpha_c = f
        gamma_c = 127 * (1 - f)
        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)
    
    return buf

def gamma_correction(image: np.ndarray, gamma: float = 1.0) -> np.ndarray:
    """Apply gamma correction"""
    # Build lookup table
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    
    # Apply gamma correction
    return cv2.LUT(image, table)
```

---

## OCR-Specific Preprocessing

### Document Enhancement

```python
import cv2
import numpy as np

def enhance_for_ocr(image: np.ndarray) -> np.ndarray:
    """Enhance image for OCR"""
    # Convert to grayscale
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    # Denoise
    denoised = cv2.medianBlur(gray, 3)
    
    # Apply CLAHE
    enhanced = clahe(denoised, clip_limit=2.0)
    
    # Threshold
    _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Dilate to connect text
    kernel = np.ones((2, 2), np.uint8)
    dilated = cv2.dilate(binary, kernel, iterations=1)
    
    return dilated
```

### Text Region Extraction

```python
def extract_text_regions(image: np.ndarray, min_area: int = 100) -> list:
    """Extract text regions from image"""
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    # Threshold
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter contours
    regions = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = w * h
        
        if area > min_area:
            # Filter by aspect ratio (text is usually wider than tall)
            aspect_ratio = w / h
            if 0.2 < aspect_ratio < 10:
                regions.append({
                    'bbox': (x, y, w, h),
                    'area': area,
                    'contour': contour
                })
    
    return regions
```

### Remove Lines and Grids

```python
def remove_horizontal_lines(image: np.ndarray) -> np.ndarray:
    """Remove horizontal lines"""
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    # Threshold
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Define horizontal kernel
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
    
    # Detect horizontal lines
    horizontal_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    
    # Remove lines
    result = cv2.inpaint(binary, horizontal_lines, 3, cv2.INPAINT_TELEA)
    
    return result

def remove_vertical_lines(image: np.ndarray) -> np.ndarray:
    """Remove vertical lines"""
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    # Threshold
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Define vertical kernel
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
    
    # Detect vertical lines
    vertical_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
    
    # Remove lines
    result = cv2.inpaint(binary, vertical_lines, 3, cv2.INPAINT_TELEA)
    
    return result
```

---

## Pipeline Creation

### Basic Preprocessing Pipeline

```python
from typing import Callable, List

class PreprocessingPipeline:
    def __init__(self):
        self.steps: List[Callable] = []
    
    def add_step(self, step: Callable, name: str = None):
        """Add preprocessing step"""
        self.steps.append({
            'step': step,
            'name': name or step.__name__
        })
    
    def process(self, image: np.ndarray) -> np.ndarray:
        """Process image through pipeline"""
        result = image
        
        for step_config in self.steps:
            step = step_config['step']
            result = step(result)
        
        return result

# Create pipeline
pipeline = PreprocessingPipeline()
pipeline.add_step(rgb_to_grayscale, 'grayscale')
pipeline.add_step(gaussian_blur, 'denoise')
pipeline.add_step(clahe, 'enhance')
pipeline.add_step(smart_threshold, 'threshold')

# Process image
processed = pipeline.process(image)
```

### Configurable Pipeline

```python
class ConfigurablePipeline:
    def __init__(self, config: dict):
        self.config = config
    
    def process(self, image: np.ndarray) -> np.ndarray:
        """Process based on configuration"""
        result = image
        
        # Grayscale
        if self.config.get('grayscale', True):
            result = rgb_to_grayscale(result)
        
        # Denoise
        if self.config.get('denoise', False):
            kernel_size = self.config.get('denoise_kernel', 3)
            result = median_filter(result, kernel_size)
        
        # Enhance
        if self.config.get('enhance', False):
            clip_limit = self.config.get('clahe_clip', 2.0)
            result = clahe(result, clip_limit=clip_limit)
        
        # Threshold
        if self.config.get('threshold', False):
            threshold_type = self.config.get('threshold_type', 'otsu')
            if threshold_type == 'otsu':
                result = otsu_threshold(result)
            elif threshold_type == 'adaptive':
                result = adaptive_threshold_gaussian(result)
        
        return result

# Example configuration
config = {
    'grayscale': True,
    'denoise': True,
    'denoise_kernel': 3,
    'enhance': True,
    'clahe_clip': 2.0,
    'threshold': True,
    'threshold_type': 'otsu'
}

pipeline = ConfigurablePipeline(config)
processed = pipeline.process(image)
```

---

## Best Practices

### Image Quality Assessment

```python
def assess_image_quality(image: np.ndarray) -> dict:
    """Assess image quality for OCR"""
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    # Calculate metrics
    metrics = {
        'blur_score': calculate_blur_score(gray),
        'contrast_score': calculate_contrast_score(gray),
        'brightness_score': calculate_brightness_score(gray),
        'noise_level': calculate_noise_level(gray)
    }
    
    # Overall quality
    metrics['overall_quality'] = np.mean(list(metrics.values()))
    
    return metrics

def calculate_blur_score(image: np.ndarray) -> float:
    """Calculate blur score using Laplacian variance"""
    laplacian = cv2.Laplacian(image, cv2.CV_64F)
    return np.var(laplacian) / 1000.0

def calculate_contrast_score(image: np.ndarray) -> float:
    """Calculate contrast score"""
    return np.std(image) / 128.0

def calculate_brightness_score(image: np.ndarray) -> float:
    """Calculate brightness score"""
    mean_brightness = np.mean(image)
    return 1.0 - abs(mean_brightness - 128) / 128.0

def calculate_noise_level(image: np.ndarray) -> float:
    """Calculate noise level"""
    return 1.0 - (np.std(image) / 128.0)
```

### Memory Management

```python
def process_large_image(image_path: str, output_path: str, chunk_size: int = 1000):
    """Process large image in chunks"""
    image = cv2.imread(image_path)
    height, width = image.shape[:2]
    
    # Process in chunks
    for y in range(0, height, chunk_size):
        for x in range(0, width, chunk_size):
            # Extract chunk
            chunk = image[y:y+chunk_size, x:x+chunk_size]
            
            # Process chunk
            processed_chunk = enhance_for_ocr(chunk)
            
            # Write back
            image[y:y+chunk_size, x:x+chunk_size] = processed_chunk
    
    # Save result
    cv2.imwrite(output_path, image)
```

### Error Handling

```python
def safe_preprocess(image_path: str, fallback_image: np.ndarray = None) -> np.ndarray:
    """Safely preprocess image with error handling"""
    try:
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Failed to load image")
        
        # Process
        processed = enhance_for_ocr(image)
        return processed
    
    except Exception as e:
        print(f"Error processing image: {e}")
        return fallback_image
```

---

## Related Skills

- [Document Ingestion Pipeline](../07-document-processing/document-ingestion-pipeline/SKILL.md) - Document loading and processing workflows
- [Document Parsing](../07-document-processing/document-parsing/SKILL.md) - Structured data extraction from documents
- [OCR with Tesseract](../07-document-processing/ocr-tesseract/SKILL.md) - Text extraction using Tesseract OCR
- [OCR with PaddleOCR](../07-document-processing/ocr-paddleocr/SKILL.md) - Text extraction using PaddleOCR
- [PDF Processing](../07-document-processing/pdf-processing/SKILL.md) - PDF-specific processing techniques
- [RAG Implementation](../06-ai-ml-production/rag-implementation/SKILL.md) - Retrieval-Augmented Generation patterns

## Additional Resources

- [OpenCV Documentation](https://docs.opencv.org/)
- [OpenCV Python Tutorials](https://docs.opencv.org/master/d6/d00/tutorial_py_root.html)
- [Pillow Documentation](https://pillow.readthedocs.io/)
- [Image Processing with Python](https://pyimagesearch.com/)
