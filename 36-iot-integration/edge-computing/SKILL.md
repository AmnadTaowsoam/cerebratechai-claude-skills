---
name: Edge Computing
description: Processing data closer to IoT devices to reduce latency and bandwidth usage, including edge devices, local processing, filtering, and cloud synchronization.
---

# Edge Computing

> **Current Level:** Advanced  
> **Domain:** IoT / Edge Computing / Architecture

---

## Overview

Edge computing processes data closer to IoT devices, reducing latency and bandwidth. This guide covers edge devices, local processing, and cloud synchronization for building efficient IoT systems that process data at the edge while maintaining cloud connectivity.

## Edge Computing Concepts

```
Cloud: Heavy processing, storage, analytics
  ↕
Edge: Local processing, filtering, aggregation
  ↕
Devices: Data collection, basic control
```

**Benefits:**
- Reduced latency
- Lower bandwidth usage
- Offline capabilities
- Privacy and security
- Cost savings

## Edge vs Cloud Decision

| Factor | Edge | Cloud |
|--------|------|-------|
| **Latency** | <10ms | 50-200ms |
| **Bandwidth** | Low | High |
| **Processing** | Limited | Unlimited |
| **Cost** | Hardware | Subscription |
| **Offline** | Yes | No |

**Use Edge for:**
- Real-time control
- Video analytics
- Anomaly detection
- Data filtering

**Use Cloud for:**
- Long-term storage
- Complex analytics
- ML training
- Dashboards

## Edge Devices

### Raspberry Pi Setup

```python
# edge_processor.py
import time
import json
from typing import Dict, List
import paho.mqtt.client as mqtt

class EdgeProcessor:
    def __init__(self, mqtt_broker: str):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
        self.client.connect(mqtt_broker, 1883, 60)
        
        self.sensor_buffer = []
        self.buffer_size = 10
    
    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        client.subscribe("sensors/local/#")
    
    def on_message(self, client, userdata, msg):
        data = json.loads(msg.payload.decode())
        
        # Process locally
        processed = self.process_sensor_data(data)
        
        # Send to cloud only if significant
        if self.is_significant(processed):
            self.send_to_cloud(processed)
    
    def process_sensor_data(self, data: Dict) -> Dict:
        """Local processing on edge device"""
        # Add to buffer
        self.sensor_buffer.append(data['value'])
        if len(self.sensor_buffer) > self.buffer_size:
            self.sensor_buffer.pop(0)
        
        # Calculate local statistics
        avg = sum(self.sensor_buffer) / len(self.sensor_buffer)
        
        return {
            **data,
            'local_avg': avg,
            'processed_at_edge': True
        }
    
    def is_significant(self, data: Dict) -> bool:
        """Determine if data should be sent to cloud"""
        # Only send if value differs significantly from average
        if 'local_avg' in data:
            return abs(data['value'] - data['local_avg']) > 2.0
        return True
    
    def send_to_cloud(self, data: Dict):
        """Send processed data to cloud"""
        self.client.publish("cloud/sensor-data", json.dumps(data))
    
    def start(self):
        self.client.loop_forever()

# Usage
processor = EdgeProcessor('mqtt://localhost')
processor.start()
```

## Local Processing

```python
# local_ml_inference.py
import numpy as np
import tensorflow as tf
from typing import List

class EdgeMLInference:
    def __init__(self, model_path: str):
        # Load TensorFlow Lite model for edge
        self.interpreter = tf.lite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
    
    def predict(self, input_data: np.ndarray) -> np.ndarray:
        """Run inference on edge device"""
        # Prepare input
        input_data = input_data.astype(np.float32)
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        
        # Run inference
        self.interpreter.invoke()
        
        # Get output
        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
        return output_data
    
    def detect_anomaly(self, sensor_values: List[float]) -> bool:
        """Detect anomalies using edge ML model"""
        input_array = np.array(sensor_values).reshape(1, -1)
        prediction = self.predict(input_array)
        
        # Threshold-based decision
        return prediction[0][0] > 0.5

# Image processing on edge
class EdgeImageProcessor:
    def __init__(self):
        self.model = tf.lite.Interpreter(model_path='mobilenet_v2.tflite')
        self.model.allocate_tensors()
    
    def process_image(self, image_path: str) -> Dict:
        """Process image locally on edge device"""
        import cv2
        
        # Load and preprocess image
        image = cv2.imread(image_path)
        image = cv2.resize(image, (224, 224))
        image = image.astype(np.float32) / 255.0
        
        # Run inference
        input_data = np.expand_dims(image, axis=0)
        self.model.set_tensor(self.model.get_input_details()[0]['index'], input_data)
        self.model.invoke()
        
        # Get results
        output = self.model.get_tensor(self.model.get_output_details()[0]['index'])
        
        return {
            'classification': np.argmax(output),
            'confidence': float(np.max(output))
        }
```

## Data Synchronization

```python
# sync_manager.py
import sqlite3
import requests
from typing import List, Dict
import time

class DataSyncManager:
    def __init__(self, local_db: str, cloud_api: str):
        self.conn = sqlite3.connect(local_db)
        self.cloud_api = cloud_api
        self.sync_interval = 60  # seconds
    
    def store_locally(self, data: Dict):
        """Store data in local SQLite database"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO sensor_data (device_id, sensor_type, value, timestamp, synced)
            VALUES (?, ?, ?, ?, 0)
        """, (data['device_id'], data['sensor_type'], data['value'], data['timestamp']))
        self.conn.commit()
    
    def sync_to_cloud(self):
        """Sync unsynced data to cloud"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM sensor_data WHERE synced = 0 LIMIT 100")
        rows = cursor.fetchall()
        
        if not rows:
            return
        
        # Batch upload to cloud
        batch_data = [
            {
                'device_id': row[1],
                'sensor_type': row[2],
                'value': row[3],
                'timestamp': row[4]
            }
            for row in rows
        ]
        
        try:
            response = requests.post(
                f"{self.cloud_api}/sensor-data/batch",
                json=batch_data,
                timeout=10
            )
            
            if response.status_code == 200:
                # Mark as synced
                ids = [row[0] for row in rows]
                cursor.execute(
                    f"UPDATE sensor_data SET synced = 1 WHERE id IN ({','.join('?' * len(ids))})",
                    ids
                )
                self.conn.commit()
                print(f"Synced {len(rows)} records to cloud")
        
        except requests.exceptions.RequestException as e:
            print(f"Sync failed: {e}")
    
    def start_sync_loop(self):
        """Continuously sync data to cloud"""
        while True:
            self.sync_to_cloud()
            time.sleep(self.sync_interval)
```

## Offline Capabilities

```python
# offline_handler.py
class OfflineHandler:
    def __init__(self):
        self.is_online = False
        self.offline_queue = []
        self.max_queue_size = 1000
    
    def check_connectivity(self) -> bool:
        """Check if cloud is reachable"""
        try:
            response = requests.get('https://api.example.com/health', timeout=5)
            self.is_online = response.status_code == 200
        except:
            self.is_online = False
        
        return self.is_online
    
    def handle_data(self, data: Dict):
        """Handle data with offline support"""
        if self.is_online:
            # Send directly to cloud
            self.send_to_cloud(data)
            
            # Process offline queue
            self.process_offline_queue()
        else:
            # Queue for later
            self.queue_data(data)
    
    def queue_data(self, data: Dict):
        """Queue data for offline processing"""
        if len(self.offline_queue) < self.max_queue_size:
            self.offline_queue.append(data)
        else:
            # Remove oldest data
            self.offline_queue.pop(0)
            self.offline_queue.append(data)
    
    def process_offline_queue(self):
        """Process queued data when back online"""
        while self.offline_queue and self.is_online:
            data = self.offline_queue.pop(0)
            self.send_to_cloud(data)
    
    def send_to_cloud(self, data: Dict):
        """Send data to cloud"""
        try:
            requests.post('https://api.example.com/data', json=data, timeout=5)
        except:
            self.queue_data(data)
```

## Containerization (Docker)

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run edge application
CMD ["python", "edge_processor.py"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  edge-processor:
    build: .
    restart: always
    volumes:
      - ./data:/app/data
      - ./models:/app/models
    environment:
      - MQTT_BROKER=mqtt://broker.local
      - CLOUD_API=https://api.example.com
    devices:
      - /dev/ttyUSB0:/dev/ttyUSB0  # Serial device
```

## AWS IoT Greengrass

```python
# greengrass_component.py
import greengrasssdk
import json

# Create IoT client
iot_client = greengrasssdk.client('iot-data')

def lambda_handler(event, context):
    """Greengrass Lambda function"""
    
    # Process sensor data
    sensor_data = json.loads(event['body'])
    
    # Local processing
    processed = process_locally(sensor_data)
    
    # Publish to local MQTT
    iot_client.publish(
        topic='local/processed',
        payload=json.dumps(processed)
    )
    
    # Send to cloud if needed
    if should_send_to_cloud(processed):
        iot_client.publish(
            topic='$aws/things/device/shadow/update',
            payload=json.dumps({
                'state': {
                    'reported': processed
                }
            })
        )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Processed successfully')
    }

def process_locally(data):
    """Local edge processing"""
    return {
        **data,
        'processed_at_edge': True,
        'timestamp': time.time()
    }

def should_send_to_cloud(data):
    """Determine if data should be sent to cloud"""
    return data.get('value', 0) > 100
```

## Best Practices

1. **Edge Selection** - Choose appropriate edge hardware
2. **Local Processing** - Process data locally when possible
3. **Bandwidth** - Minimize cloud communication
4. **Offline** - Design for offline operation
5. **Sync** - Implement robust sync mechanism
6. **ML Models** - Use lightweight models (TFLite)
7. **Security** - Secure edge devices
8. **Updates** - Support OTA updates
9. **Monitoring** - Monitor edge device health
10. **Containerization** - Use Docker for deployment

---

## Quick Start

### AWS IoT Greengrass

```python
import greengrasssdk

client = greengrasssdk.client('iot-data')

def lambda_handler(event, context):
    # Process data at edge
    processed_data = process_sensor_data(event['sensor_data'])
    
    # Send to cloud
    client.publish(
        topic='sensor/processed',
        payload=json.dumps(processed_data)
    )
    
    return processed_data
```

### Edge Device Setup

```bash
# Install Greengrass Core
sudo ./greengrass-linux-x86-64-1.11.0.tar.gz

# Configure
sudo /greengrass/ggc/core/greengrassd start
```

---

## Production Checklist

- [ ] **Edge Devices**: Select appropriate edge devices
- [ ] **Local Processing**: Implement local data processing
- [ ] **Cloud Sync**: Set up cloud synchronization
- [ ] **Offline Support**: Handle offline scenarios
- [ ] **Security**: Secure edge devices
- [ ] **Updates**: Support OTA updates
- [ ] **Monitoring**: Monitor edge device health
- [ ] **Containerization**: Use Docker for deployment
- [ ] **Resource Management**: Manage device resources
- [ ] **Testing**: Test edge processing
- [ ] **Documentation**: Document edge architecture
- [ ] **Scalability**: Scale edge deployment

---

## Anti-patterns

### ❌ Don't: Process Everything in Cloud

```javascript
// ❌ Bad - All processing in cloud
device → send all data → cloud processes → response
// High latency, high bandwidth!
```

```javascript
// ✅ Good - Process at edge
device → edge processes → send summary → cloud
// Low latency, low bandwidth
```

### ❌ Don't: No Offline Support

```javascript
// ❌ Bad - Requires cloud connection
if (!isOnline()) {
  return error('No connection')  // Device stops working!
}
```

```javascript
// ✅ Good - Offline processing
if (!isOnline()) {
  processLocally(data)  // Continue processing
  queueForSync(data)  // Sync when online
}
```

---

## Integration Points

- **Device Management** (`36-iot-integration/device-management/`) - Device lifecycle
- **IoT Protocols** (`36-iot-integration/iot-protocols/`) - Device communication
- **IoT Security** (`36-iot-integration/iot-security/`) - Edge security

---

## Further Reading

- [AWS IoT Greengrass](https://aws.amazon.com/greengrass/)
- [Azure IoT Edge](https://azure.microsoft.com/en-us/services/iot-edge/)
- [TensorFlow Lite](https://www.tensorflow.org/lite)
- [NVIDIA Jetson](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/)
