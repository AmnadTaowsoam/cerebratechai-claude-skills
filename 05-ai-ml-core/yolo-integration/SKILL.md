---
name: YOLO Integration
description: Comprehensive guide for integrating YOLO (You Only Look Once) object detection models (YOLOv8, YOLOv9) using Ultralytics library.
---

# YOLO Integration

## Overview

YOLO (You Only Look Once) is a state-of-the-art object detection model known for its speed and accuracy. This skill covers YOLO integration using the Ultralytics library, including YOLOv8 and YOLOv9 models, model loading and inference, custom training, object detection, instance segmentation, pose estimation, real-time inference, batch processing, API integration, performance optimization, and production deployment.

## Prerequisites

- Understanding of computer vision and object detection concepts
- Knowledge of PyTorch and deep learning
- Familiarity with OpenCV and image processing
- Understanding of dataset formats (COCO, YOLO)
- Basic knowledge of FastAPI and REST APIs

## Key Concepts

### YOLO Models

- **YOLOv8**: State-of-the-art object detection with anchor-free detection
- **YOLOv9**: Latest YOLO version with improved accuracy
- **Model Sizes**: n (nano), s (small), m (medium), l (large), x (extra-large)
- **Task Variants**: Detection, segmentation, pose estimation, classification

### Ultralytics Library

- **YOLO Class**: Main interface for model loading and inference
- **Training Pipeline**: Built-in training with data augmentation
- **Export Formats**: ONNX, TensorRT, CoreML, TFLite
- **Result Objects**: Structured detection results with boxes, masks, keypoints

### Dataset Formats

- **YOLO Format**: Normalized bounding boxes with class IDs
- **COCO Format**: Industry-standard annotation format
- **Data.yaml**: Dataset configuration for training
- **Directory Structure**: Organized images and labels folders

### Deployment Patterns

- **FastAPI Server**: REST API for YOLO inference
- **Docker Deployment**: Containerized YOLO service
- **Kubernetes**: Scalable deployment with GPU support
- **Real-Time Inference**: Webcam and video stream processing

## Implementation Guide

### YOLO Setup (Ultralytics)

#### Installation

```bash
# Basic installation
pip install ultralytics

# Install with GPU support
pip install ultralytics[torch]

# Install with all dependencies
pip install ultralytics[all]

# Install from source
git clone https://github.com/ultralytics/ultralytics
cd ultralytics
pip install -e .
```

#### Verify Installation

```python
from ultralytics import YOLO
import torch

# Check version
from ultralytics import __version__
print(f"Ultralytics version: {__version__}")

# Check CUDA availability
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA device count: {torch.cuda.device_count()}")

# Test model loading
model = YOLO("yolov8n.pt")  # Load pretrained model
print(f"Model loaded successfully: {model.names}")
```

#### Available Models

```python
from ultralytics import YOLO

# YOLOv8 models (n, s, m, l, x)
yolov8_models = {
    "nano": "yolov8n.pt",      # Fastest, lowest accuracy
    "small": "yolov8s.pt",     # Fast, good accuracy
    "medium": "yolov8m.pt",    # Balanced
    "large": "yolov8l.pt",     # Slower, higher accuracy
    "xlarge": "yolov8x.pt",    # Slowest, highest accuracy
}

# YOLOv9 models
yolov9_models = {
    "nano": "yolov9c.pt",
    "small": "yolov9s.pt",
    "medium": "yolov9m.pt",
    "large": "yolov9e.pt",
}

# Segmentation models
seg_models = {
    "yolov8n-seg.pt",
    "yolov8s-seg.pt",
}

# Pose estimation models
pose_models = {
    "yolov8n-pose.pt",
    "yolov8s-pose.pt",
}
```

### Model Loading and Inference

#### Basic Inference

```python
from ultralytics import YOLO

# Load model
model = YOLO("yolov8n.pt")

# Inference on image
results = model("path/to/image.jpg")

# Access results
for result in results:
    boxes = result.boxes  # Bounding boxes
    masks = result.masks  # Segmentation masks
    keypoints = result.keypoints  # Pose keypoints
    probs = result.probs  # Classification probabilities

    # Get detections
    for box in boxes:
        class_id = int(box.cls[0])
        class_name = model.names[class_id]
        confidence = float(box.conf[0])
        bbox = box.xyxy[0].tolist()  # [x1, y1, x2, y2]

        print(f"{class_name}: {confidence:.2f} at {bbox}")
```

#### Inference with Parameters

```python
# Inference with custom parameters
results = model(
    "path/to/image.jpg",
    conf=0.25,        # Confidence threshold
    iou=0.45,         # NMS IoU threshold
    max_det=100,      # Maximum detections
    device="0",       # GPU device
    half=True,        # Half precision (FP16)
    verbose=False,    # Suppress output
    save=True,        # Save results
    show=True,        # Show results
    stream=True,      # Stream results
)

# Inference on multiple images
results = model(["image1.jpg", "image2.jpg", "image3.jpg"])
```

#### Video Inference

```python
# Inference on video file
results = model("video.mp4", save=True)

# Inference on webcam
results = model(source=0, show=True)

# Inference on RTSP stream
results = model("rtsp://username:password@ip:port/stream", stream=True)

# Process video frame by frame
for result in model("video.mp4", stream=True):
    # Process each frame
    boxes = result.boxes
    # Your processing logic here
```

### Custom Training

#### Dataset Preparation

**Dataset Structure:**

```
dataset/
├── data.yaml
├── train/
│   ├── images/
│   │   ├── image1.jpg
│   │   ├── image2.jpg
│   │   └── ...
│   └── labels/
│       ├── image1.txt
│       ├── image2.txt
│       └── ...
├── val/
│   ├── images/
│   └── labels/
└── test/
    ├── images/
    └── labels/
```

**data.yaml Configuration:**

```yaml
# Dataset configuration
path: /path/to/dataset  # Dataset root dir
train: train/images      # Train images relative to 'path'
val: val/images          # Val images relative to 'path'
test: test/images        # Test images (optional)

# Classes
names:
  0: person
  1: car
  2: dog
  3: cat

# Number of classes
nc: 4
```

**Label Format (YOLO format):**

```
# Each line in label file: class_id center_x center_y width height
# Values are normalized [0, 1]
0 0.5 0.5 0.3 0.4    # class 0 at center (0.5, 0.5) with size (0.3, 0.4)
1 0.2 0.3 0.1 0.2    # class 1 at (0.2, 0.3) with size (0.1, 0.2)
```

**Dataset Conversion Script:**

```python
import json
import os
from pathlib import Path

def coco_to_yolo(coco_json_path, output_dir, image_width, image_height):
    """Convert COCO format to YOLO format."""
    with open(coco_json_path, 'r') as f:
        coco_data = json.load(f)

    # Create mapping from image_id to filename
    image_id_to_name = {img['id']: img['file_name'] for img in coco_data['images']}

    # Create output directories
    os.makedirs(f"{output_dir}/labels", exist_ok=True)

    # Process annotations
    for annotation in coco_data['annotations']:
        image_id = annotation['image_id']
        image_name = image_id_to_name[image_id]
        label_name = os.path.splitext(image_name)[0] + '.txt'
        label_path = os.path.join(output_dir, 'labels', label_name)

        # Convert bbox to YOLO format
        x, y, width, height = annotation['bbox']
        x_center = (x + width / 2) / image_width
        y_center = (y + height / 2) / image_height
        width_norm = width / image_width
        height_norm = height / image_height

        # Write to label file
        with open(label_path, 'a') as f:
            f.write(f"{annotation['category_id']} {x_center} {y_center} {width_norm} {height_norm}\n")

# Usage
coco_to_yolo(
    coco_json_path="annotations.json",
    output_dir="dataset",
    image_width=640,
    image_height=640
)
```

#### Training Configuration

```python
from ultralytics import YOLO

# Load model
model = YOLO("yolov8n.pt")  # Load pretrained model

# Train model
results = model.train(
    data="data.yaml",           # Dataset configuration
    epochs=100,                 # Number of epochs
    batch=16,                   # Batch size
    imgsz=640,                  # Image size
    device="0",                 # GPU device
    workers=8,                  # Number of workers
    patience=50,                # Early stopping patience
    save=True,                  # Save checkpoints
    save_period=10,             # Save every N epochs
    cache=True,                 # Cache images
    project="runs/train",       # Project directory
    name="experiment",          # Experiment name
    exist_ok=False,             # Overwrite existing experiment
    pretrained=True,            # Use pretrained weights
    optimizer="SGD",            # Optimizer (SGD, Adam, AdamW)
    lr0=0.01,                   # Initial learning rate
    lrf=0.01,                   # Final learning rate fraction
    momentum=0.937,             # SGD momentum
    weight_decay=0.0005,        # Weight decay
    warmup_epochs=3,            # Warmup epochs
    warmup_momentum=0.8,        # Warmup momentum
    warmup_bias_lr=0.1,         # Warmup bias learning rate
    box=7.5,                    # Box loss gain
    cls=0.5,                    # Cls loss gain
    dfl=1.5,                    # DFL loss gain
    mosaic=1.0,                 # Mosaic augmentation probability
    mixup=0.0,                  # Mixup augmentation probability
    copy_paste=0.0,             # Copy-paste augmentation probability
    auto_augment="randaugment", # Auto augmentation
    erasing=0.4,                # Random erasing probability
    crop_fraction=1.0,          # Fraction of image to crop
    hsv_h=0.015,                # HSV-Hue augmentation
    hsv_s=0.7,                  # HSV-Saturation augmentation
    hsv_v=0.4,                  # HSV-Value augmentation
    degrees=0.0,                # Rotation degrees
    translate=0.1,              # Translation
    scale=0.5,                  # Scale
    shear=0.0,                  # Shear
    perspective=0.0,             # Perspective
    flipud=0.0,                 # Vertical flip probability
    fliplr=0.5,                 # Horizontal flip probability
    bgr=0.0,                    # BGR flip probability
    mosaic_prob=1.0,            # Mosaic probability
    mixup_prob=0.0,             # Mixup probability
    copy_paste_prob=0.0,        # Copy-paste probability
)
```

#### Fine-Tuning

```python
from ultralytics import YOLO

# Load pretrained model
model = YOLO("yolov8n.pt")

# Freeze backbone layers (optional)
for i, (name, param) in enumerate(model.named_parameters()):
    if "backbone" in name:
        param.requires_grad = False

# Fine-tune with lower learning rate
results = model.train(
    data="data.yaml",
    epochs=50,
    batch=16,
    imgsz=640,
    lr0=0.001,  # Lower learning rate for fine-tuning
    optimizer="Adam",
    project="runs/train",
    name="fine_tune",
    pretrained=True,
)

# Unfreeze and continue training (optional)
for param in model.parameters():
    param.requires_grad = True

results = model.train(
    data="data.yaml",
    epochs=50,
    batch=16,
    imgsz=640,
    lr0=0.0001,  # Even lower learning rate
    optimizer="Adam",
    project="runs/train",
    name="fine_tune_unfrozen",
    resume=True,  # Resume from last checkpoint
)
```

#### Resume Training

```python
# Resume from last checkpoint
model = YOLO("runs/train/experiment/weights/last.pt")

results = model.train(
    data="data.yaml",
    epochs=200,  # Total epochs (will continue from where it left off)
    resume=True,
)
```

### Object Detection

#### Basic Detection

```python
from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")

# Detect objects
results = model("image.jpg")

# Process results
for result in results:
    # Get image with detections drawn
    annotated_image = result.plot()

    # Save annotated image
    cv2.imwrite("result.jpg", annotated_image)

    # Get detections as pandas DataFrame
    df = result.to_df()
    print(df)

    # Get detections as JSON
    detections = result.tojson()
    print(detections)
```

#### Custom Detection Pipeline

```python
from ultralytics import YOLO
import cv2
import numpy as np

class YOLODetector:
    def __init__(self, model_path="yolov8n.pt", conf_threshold=0.25):
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold

    def detect(self, image, filter_classes=None):
        """
        Detect objects in image.

        Args:
            image: Input image (numpy array or path)
            filter_classes: List of class names to filter (None for all)

        Returns:
            List of detections with class, confidence, bbox
        """
        results = self.model(image, conf=self.conf_threshold, verbose=False)

        detections = []
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                class_name = self.model.names[class_id]
                confidence = float(box.conf[0])
                bbox = box.xyxy[0].cpu().numpy().astype(int)

                # Filter by class if specified
                if filter_classes is None or class_name in filter_classes:
                    detections.append({
                        "class": class_name,
                        "class_id": class_id,
                        "confidence": confidence,
                        "bbox": bbox.tolist()  # [x1, y1, x2, y2]
                    })

        return detections

    def draw_detections(self, image, detections):
        """Draw detections on image."""
        image = image.copy()

        for det in detections:
            x1, y1, x2, y2 = det["bbox"]
            class_name = det["class"]
            confidence = det["confidence"]

            # Draw bounding box
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Draw label
            label = f"{class_name}: {confidence:.2f}"
            label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
            cv2.rectangle(image, (x1, y1 - label_size[1] - 10),
                         (x1 + label_size[0], y1), (0, 255, 0), -1)
            cv2.putText(image, label, (x1, y1 - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

        return image

# Usage
detector = YOLODetector("yolov8n.pt", conf_threshold=0.5)

# Detect
image = cv2.imread("image.jpg")
detections = detector.detect(image, filter_classes=["person", "car"])

# Draw
annotated = detector.draw_detections(image, detections)
cv2.imwrite("detections.jpg", annotated)
```

#### Batch Processing

```python
from ultralytics import YOLO
import os
from pathlib import Path

def batch_detect(input_dir, output_dir, model_path="yolov8n.pt"):
    """Process all images in a directory."""
    model = YOLO(model_path)

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Process images
    for image_path in Path(input_dir).glob("*.jpg"):
        print(f"Processing {image_path.name}...")

        # Detect
        results = model(str(image_path), save=False)

        # Save annotated image
        for result in results:
            output_path = os.path.join(output_dir, f"detected_{image_path.name}")
            result.save(output_path)

        # Save detections as JSON
        for result in results:
            json_path = os.path.join(output_dir, f"{image_path.stem}.json")
            with open(json_path, "w") as f:
                f.write(result.tojson())

# Usage
batch_detect(
    input_dir="images/",
    output_dir="output/",
    model_path="yolov8n.pt"
)
```

### Instance Segmentation

#### Segmentation Inference

```python
from ultralytics import YOLO
import cv2
import numpy as np

# Load segmentation model
model = YOLO("yolov8n-seg.pt")

# Run segmentation
results = model("image.jpg")

# Process segmentation results
for result in results:
    # Get masks
    masks = result.masks

    if masks:
        # Get mask data
        mask_data = masks.data.cpu().numpy()  # (N, H, W)

        # Get segmentation polygons
        for i, mask in enumerate(masks.xy):
            class_id = int(result.boxes.cls[i])
            class_name = model.names[class_id]
            confidence = float(result.boxes.conf[i])

            print(f"{class_name}: {confidence:.2f}")
            print(f"Mask shape: {mask.shape}")

        # Draw segmentation masks
        annotated = result.plot()
        cv2.imwrite("segmentation.jpg", annotated)
```

#### Mask Processing

```python
import numpy as np
import cv2

def extract_object(image, mask):
    """Extract object from image using mask."""
    # Convert mask to uint8
    mask_uint8 = (mask * 255).astype(np.uint8)

    # Create 3-channel mask
    mask_3ch = cv2.cvtColor(mask_uint8, cv2.COLOR_GRAY2BGR)

    # Apply mask to image
    result = cv2.bitwise_and(image, image, mask=mask_uint8)

    # Create transparent background
    result_rgba = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
    result_rgba[:, :, 3] = mask_uint8

    return result_rgba

# Usage
for result in results:
    if result.masks:
        for i, mask in enumerate(result.masks.data):
            mask_np = mask.cpu().numpy()
            extracted = extract_object(image, mask_np)
            cv2.imwrite(f"object_{i}.png", extracted)
```

### Pose Estimation

#### Pose Detection

```python
from ultralytics import YOLO
import cv2

# Load pose model
model = YOLO("yolov8n-pose.pt")

# Detect poses
results = model("image.jpg")

# Process pose results
for result in results:
    keypoints = result.keypoints

    if keypoints:
        # Keypoints shape: (N, 17, 3) - N persons, 17 keypoints, (x, y, confidence)
        for i, kpts in enumerate(keypoints.xy):
            print(f"Person {i}:")
            for j, (x, y) in enumerate(kpts):
                conf = keypoints.conf[i][j]
                print(f"  Keypoint {j}: ({x:.1f}, {y:.1f}) conf={conf:.2f}")

        # Draw pose
        annotated = result.plot()
        cv2.imwrite("pose.jpg", annotated)
```

#### Pose Analysis

```python
import numpy as np

class PoseAnalyzer:
    def __init__(self):
        # COCO 17 keypoints
        self.keypoint_names = [
            "nose", "left_eye", "right_eye", "left_ear", "right_ear",
            "left_shoulder", "right_shoulder", "left_elbow", "right_elbow",
            "left_wrist", "right_wrist", "left_hip", "right_hip",
            "left_knee", "right_knee", "left_ankle", "right_ankle"
        ]

    def calculate_angle(self, a, b, c):
        """Calculate angle between three points."""
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)

        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - \
                  np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)

        if angle > 180.0:
            angle = 360 - angle

        return angle

    def analyze_pose(self, keypoints):
        """Analyze pose and return joint angles."""
        # Keypoints indices
        left_shoulder = 5
        left_elbow = 7
        left_wrist = 9
        right_shoulder = 6
        right_elbow = 8
        right_wrist = 10
        left_hip = 11
        right_hip = 12
        left_knee = 13
        right_knee = 14

        angles = {}

        # Left arm angle
        angles["left_arm"] = self.calculate_angle(
            keypoints[left_shoulder],
            keypoints[left_elbow],
            keypoints[left_wrist]
        )

        # Right arm angle
        angles["right_arm"] = self.calculate_angle(
            keypoints[right_shoulder],
            keypoints[right_elbow],
            keypoints[right_wrist]
        )

        # Left leg angle
        angles["left_leg"] = self.calculate_angle(
            keypoints[left_hip],
            keypoints[left_knee],
            keypoints[15]  # left_ankle
        )

        # Right leg angle
        angles["right_leg"] = self.calculate_angle(
            keypoints[right_hip],
            keypoints[right_knee],
            keypoints[16]  # right_ankle
        )

        return angles

# Usage
model = YOLO("yolov8n-pose.pt")
analyzer = PoseAnalyzer()

results = model("image.jpg")
for result in results:
    if result.keypoints:
        for i, kpts in enumerate(result.keypoints.xy):
            angles = analyzer.analyze_pose(kpts.cpu().numpy())
            print(f"Person {i} angles: {angles}")
```

### Real-Time Inference

#### Webcam Inference

```python
from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")

# Open webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    # Read frame
    success, frame = cap.read()
    if not success:
        break

    # Run inference
    results = model(frame, verbose=False)

    # Draw results
    annotated_frame = results[0].plot()

    # Display
    cv2.imshow("YOLO Inference", annotated_frame)

    # Break on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

#### Real-Time with FPS Counter

```python
from ultralytics import YOLO
import cv2
import time

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(0)

fps_counter = 0
fps_start_time = time.time()

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Run inference
    results = model(frame, verbose=False)

    # Draw results
    annotated_frame = results[0].plot()

    # Calculate FPS
    fps_counter += 1
    if time.time() - fps_start_time >= 1.0:
        fps = fps_counter
        fps_counter = 0
        fps_start_time = time.time()
        cv2.putText(annotated_frame, f"FPS: {fps}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("YOLO Inference", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

#### Multi-Threaded Inference

```python
from ultralytics import YOLO
import cv2
import threading
import queue

class YOLOInferenceThread:
    def __init__(self, model_path="yolov8n.pt"):
        self.model = YOLO(model_path)
        self.input_queue = queue.Queue(maxsize=1)
        self.output_queue = queue.Queue(maxsize=1)
        self.running = False

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._run_inference)
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()

    def _run_inference(self):
        while self.running:
            try:
                frame = self.input_queue.get(timeout=0.1)
                results = self.model(frame, verbose=False)
                self.output_queue.put(results)
            except queue.Empty:
                continue

    def predict(self, frame):
        self.input_queue.put(frame)
        try:
            return self.output_queue.get(timeout=1.0)
        except queue.Empty:
            return None

# Usage
inference_thread = YOLOInferenceThread("yolov8n.pt")
inference_thread.start()

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Non-blocking inference
    results = inference_thread.predict(frame)

    if results:
        annotated_frame = results[0].plot()
        cv2.imshow("YOLO Inference", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

inference_thread.stop()
cap.release()
cv2.destroyAllWindows()
```

### Batch Processing

#### Efficient Batch Inference

```python
from ultralytics import YOLO
import torch
from pathlib import Path
import cv2

def batch_inference(image_paths, model_path="yolov8n.pt", batch_size=32):
    """Process images in batches."""
    model = YOLO(model_path)

    results = []
    for i in range(0, len(image_paths), batch_size):
        batch = image_paths[i:i + batch_size]
        print(f"Processing batch {i//batch_size + 1}/{(len(image_paths)-1)//batch_size + 1}")

        batch_results = model(batch, verbose=False)
        results.extend(batch_results)

    return results

# Usage
image_paths = list(Path("images/").glob("*.jpg"))
results = batch_inference(image_paths, batch_size=16)
```

#### Parallel Batch Processing

```python
from ultralytics import YOLO
import torch.multiprocessing as mp
from pathlib import Path

def process_batch(args):
    """Worker function for parallel processing."""
    image_paths, model_path, device = args
    model = YOLO(model_path)
    model.to(device)

    results = []
    for image_path in image_paths:
        result = model(str(image_path), device=device, verbose=False)
        results.append((image_path, result))

    return results

def parallel_batch_inference(image_paths, model_path="yolov8n.pt", num_workers=4):
    """Process images in parallel."""
    # Split images among workers
    chunk_size = len(image_paths) // num_workers
    chunks = [image_paths[i:i + chunk_size] for i in range(0, len(image_paths), chunk_size)]

    # Prepare arguments
    args = [(chunk, model_path, i % torch.cuda.device_count())
            for i, chunk in enumerate(chunks)]

    # Run in parallel
    with mp.Pool(num_workers) as pool:
        results = pool.map(process_batch, args)

    # Flatten results
    all_results = []
    for chunk_results in results:
        all_results.extend(chunk_results)

    return all_results

# Usage
image_paths = list(Path("images/").glob("*.jpg"))
results = parallel_batch_inference(image_paths, num_workers=4)
```

### API Integration

#### FastAPI YOLO Server

```python
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from ultralytics import YOLO
import cv2
import numpy as np
import io
from typing import List
from pydantic import BaseModel

app = FastAPI(title="YOLO Detection API")

# Load model
model = YOLO("yolov8n.pt")

class Detection(BaseModel):
    class_name: str
    class_id: int
    confidence: float
    bbox: List[float]  # [x1, y1, x2, y2]

class DetectionResponse(BaseModel):
    detections: List[Detection]
    image_width: int
    image_height: int

@app.post("/detect", response_model=DetectionResponse)
async def detect(file: UploadFile = File(...)):
    """Detect objects in uploaded image."""
    try:
        # Read image
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Run inference
        results = model(image, verbose=False)

        # Process results
        detections = []
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                class_name = model.names[class_id]
                confidence = float(box.conf[0])
                bbox = box.xyxy[0].tolist()

                detections.append(Detection(
                    class_name=class_name,
                    class_id=class_id,
                    confidence=confidence,
                    bbox=bbox
                ))

        return DetectionResponse(
            detections=detections,
            image_width=image.shape[1],
            image_height=image.shape[0]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/classes")
async def get_classes():
    """Get available classes."""
    return model.names

@app.get("/health")
async def health():
    """Health check."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

#### Client Usage

```python
import requests

# Upload image and detect
with open("image.jpg", "rb") as f:
    response = requests.post(
        "http://localhost:8000/detect",
        files={"file": f}
    )

result = response.json()
print(f"Found {len(result['detections'])} objects")

for detection in result["detections"]:
    print(f"{detection['class_name']}: {detection['confidence']:.2f}")
```

### Performance Optimization

#### Model Optimization

```python
from ultralytics import YOLO
import torch

# Load model
model = YOLO("yolov8n.pt")

# Export to ONNX for faster inference
model.export(format="onnx", opset=12)

# Export to TensorRT for NVIDIA GPUs
model.export(format="engine", device=0)

# Export to CoreML for Apple devices
model.export(format="coreml")

# Use half precision (FP16)
model = YOLO("yolov8n.pt")
model.half()  # Convert to FP16

# Inference with FP16
results = model("image.jpg", half=True)
```

#### Inference Optimization

```python
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

# Optimize inference settings
results = model(
    "image.jpg",
    imgsz=640,           # Lower image size for faster inference
    conf=0.5,            # Higher confidence threshold for fewer detections
    max_det=50,          # Limit max detections
    half=True,           # Use FP16
    device="0",          # Use GPU
    verbose=False,       # Disable verbose output
    augment=False,        # Disable augmentation for faster inference
    agnostic_nms=False,  # Disable class-agnostic NMS
    classes=None,        # Filter specific classes
)
```

#### TensorRT Optimization

```python
from ultralytics import YOLO

# Export to TensorRT
model = YOLO("yolov8n.pt")
model.export(format="engine", device=0, half=True, workspace=4)

# Use TensorRT engine
model = YOLO("yolov8n.engine")
results = model("image.jpg")
```

### Post-Processing Results

#### Result Filtering

```python
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

# Run inference
results = model("image.jpg")

# Filter by confidence
filtered_results = []
for result in results:
    for box in result.boxes:
        if float(box.conf[0]) > 0.7:  # Only keep high confidence
            filtered_results.append(box)

# Filter by class
person_boxes = [box for box in result.boxes if int(box.cls[0]) == 0]  # class 0 = person

# Filter by size
large_boxes = []
for box in result.boxes:
    x1, y1, x2, y2 = box.xyxy[0]
    width = x2 - x1
    height = y2 - y1
    if width * height > 10000:  # Only keep large objects
        large_boxes.append(box)
```

#### Non-Maximum Suppression (Custom)

```python
import numpy as np

def custom_nms(boxes, scores, iou_threshold=0.45):
    """Custom NMS implementation."""
    if len(boxes) == 0:
        return []

    # Sort by score
    indices = np.argsort(scores)[::-1]

    keep = []
    while len(indices) > 0:
        # Keep the highest score box
        current = indices[0]
        keep.append(current)

        # Calculate IoU with remaining boxes
        ious = calculate_iou(boxes[current], boxes[indices[1:]])

        # Remove boxes with high IoU
        indices = indices[1:][ious < iou_threshold]

    return keep

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
```

#### Result Visualization

```python
from ultralytics import YOLO
import cv2
import numpy as np

model = YOLO("yolov8n.pt")
results = model("image.jpg")

# Custom visualization
image = cv2.imread("image.jpg")

for result in results:
    for box in result.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        class_id = int(box.cls[0])
        class_name = model.names[class_id]
        confidence = float(box.conf[0])

        # Color based on class
        color = get_color(class_id)

        # Draw bounding box
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

        # Draw label
        label = f"{class_name}: {confidence:.2f}"
        (label_width, label_height), _ = cv2.getTextSize(
            label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2
        )

        cv2.rectangle(image, (x1, y1 - label_height - 10),
                     (x1 + label_width, y1), color, -1)
        cv2.putText(image, label, (x1, y1 - 5),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

cv2.imwrite("custom_result.jpg", image)

def get_color(class_id):
    """Generate consistent color for each class."""
    np.random.seed(class_id)
    return tuple(np.random.randint(0, 255, 3).tolist())
```

### Production Deployment

#### Docker Deployment

**Dockerfile:**

```dockerfile
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app.py .
COPY models/ ./models/

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

**requirements.txt:**

```
ultralytics>=8.0.0
fastapi>=0.100.0
uvicorn>=0.23.0
python-multipart>=0.0.6
```

#### Kubernetes Deployment

**deployment.yaml:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: yolo-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: yolo-api
  template:
    metadata:
      labels:
        app: yolo-api
    spec:
      containers:
      - name: yolo-api
        image: yolo-api:latest
        ports:
        - containerPort: 8000
        resources:
          limits:
            nvidia.com/gpu: 1
          requests:
            memory: "2Gi"
            cpu: "1"
---
apiVersion: v1
kind: Service
metadata:
  name: yolo-api
spec:
  selector:
    app: yolo-api
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

#### Production Best Practices

```python
from ultralytics import YOLO
import torch
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class YOLOModel:
    _instance = None
    _model = None

    def __new__(cls, model_path="yolov8n.pt"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._model = YOLO(model_path)
            logger.info(f"Model loaded from {model_path}")
        return cls._instance

    @classmethod
    def predict(cls, image, **kwargs):
        """Thread-safe prediction."""
        try:
            results = cls._model(image, verbose=False, **kwargs)
            return results
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            raise

# Usage - singleton pattern ensures model is loaded once
model = YOLOModel("yolov8n.pt")
results = model.predict("image.jpg")
```

## Best Practices

### Model Selection

1. **Choose Model Size Based on Requirements**
   - Use `yolov8n` for real-time applications
   - Use `yolov8s/m` for balanced performance
   - Use `yolov8l/x` for maximum accuracy

2. **Use Task-Specific Models**
   - Use `yolov8n-seg.pt` for instance segmentation
   - Use `yolov8n-pose.pt` for pose estimation
   - Use detection models for object detection only

### Training Best Practices

1. **Dataset Preparation**
   - Use high-quality annotations
   - Ensure consistent image sizes
   - Balance class distribution
   - Use data augmentation

2. **Training Configuration**
   - Start with pretrained weights
   - Use appropriate learning rate
   - Monitor validation metrics
   - Save checkpoints regularly

3. **Fine-Tuning**
   - Freeze backbone layers initially
   - Use lower learning rates
   - Gradually unfreeze layers
   - Monitor for overfitting

### Inference Optimization

1. **Use Half Precision**
   ```python
   model = YOLO("yolov8n.pt")
   results = model("image.jpg", half=True)
   ```

2. **Optimize Inference Parameters**
   - Set appropriate confidence threshold
   - Limit maximum detections
   - Disable verbose output
   - Use GPU acceleration

3. **Export Optimized Models**
   - Export to ONNX for cross-platform deployment
   - Export to TensorRT for NVIDIA GPUs
   - Export to CoreML for Apple devices

### Production Deployment

1. **Use Singleton Pattern**
   - Load model once at startup
   - Reuse model across requests
   - Avoid loading model per request

2. **Implement Error Handling**
   - Handle invalid inputs gracefully
   - Log errors appropriately
   - Provide meaningful error messages

3. **Monitor Performance**
   - Track inference latency
   - Monitor GPU memory usage
   - Set up alerts for performance degradation

4. **Use Appropriate Hardware**
   - Use GPU for real-time applications
   - Consider edge devices for mobile deployment
   - Optimize for target platform

## Related Skills

- [`05-ai-ml-core/model-training`](05-ai-ml-core/model-training/SKILL.md)
- [`05-ai-ml-core/model-optimization`](05-ai-ml-core/model-optimization/SKILL.md)
- [`05-ai-ml-core/pytorch-deployment`](05-ai-ml-core/pytorch-deployment/SKILL.md)
- [`07-document-processing/image-preprocessing`](07-document-processing/image-preprocessing/SKILL.md)
- [`06-ai-ml-production/llm-integration`](06-ai-ml-production/llm-integration/SKILL.md)
