---
name: Real-time Monitoring
description: Providing live visibility into IoT device status and sensor data through real-time dashboards, alerts, WebSocket implementation, and time-series data visualization.
---

# Real-time Monitoring

> **Current Level:** Intermediate  
> **Domain:** IoT / Monitoring / Real-time

---

## Overview

Real-time monitoring provides live visibility into IoT device status and sensor data. This guide covers dashboards, alerts, and WebSocket implementation for building monitoring systems that provide instant insights into IoT device health and performance.

## Monitoring Architecture

```
Devices → MQTT → Backend → WebSocket → Dashboard
                    ↓
              TimescaleDB
```

## Real-time Data Streaming

```typescript
// services/realtime-stream.service.ts
import { Server as SocketIOServer } from 'socket.io';
import mqtt from 'mqtt';

export class RealtimeStreamService {
  private io: SocketIOServer;
  private mqttClient: mqtt.MqttClient;

  constructor(io: SocketIOServer, mqttBroker: string) {
    this.io = io;
    this.mqttClient = mqtt.connect(mqttBroker);

    this.setupMQTTHandlers();
    this.setupSocketIOHandlers();
  }

  private setupMQTTHandlers(): void {
    this.mqttClient.on('connect', () => {
      console.log('Connected to MQTT broker');
      this.mqttClient.subscribe('sensors/#');
      this.mqttClient.subscribe('devices/+/status');
    });

    this.mqttClient.on('message', (topic, message) => {
      const data = JSON.parse(message.toString());
      
      // Broadcast to all connected clients
      this.io.emit('sensor-data', {
        topic,
        data,
        timestamp: Date.now()
      });

      // Emit to specific device room
      const deviceId = this.extractDeviceId(topic);
      if (deviceId) {
        this.io.to(`device:${deviceId}`).emit('device-update', data);
      }
    });
  }

  private setupSocketIOHandlers(): void {
    this.io.on('connection', (socket) => {
      console.log('Client connected:', socket.id);

      socket.on('subscribe-device', (deviceId: string) => {
        socket.join(`device:${deviceId}`);
        console.log(`Client subscribed to device ${deviceId}`);
      });

      socket.on('unsubscribe-device', (deviceId: string) => {
        socket.leave(`device:${deviceId}`);
      });

      socket.on('disconnect', () => {
        console.log('Client disconnected:', socket.id);
      });
    });
  }

  private extractDeviceId(topic: string): string | null {
    const match = topic.match(/devices\/([^\/]+)\//);
    return match ? match[1] : null;
  }
}
```

## Dashboard Design

```typescript
// components/MonitoringDashboard.tsx
import { useEffect, useState } from 'react';
import { io, Socket } from 'socket.io-client';

export function MonitoringDashboard() {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [devices, setDevices] = useState<Device[]>([]);
  const [sensorData, setSensorData] = useState<SensorReading[]>([]);

  useEffect(() => {
    const socketInstance = io('http://localhost:3000');

    socketInstance.on('connect', () => {
      console.log('Connected to monitoring server');
    });

    socketInstance.on('sensor-data', (data) => {
      setSensorData(prev => [...prev.slice(-99), data]);
    });

    socketInstance.on('device-update', (data) => {
      updateDeviceStatus(data);
    });

    setSocket(socketInstance);

    return () => {
      socketInstance.close();
    };
  }, []);

  const updateDeviceStatus = (data: any) => {
    setDevices(prev => prev.map(device => 
      device.id === data.deviceId 
        ? { ...device, ...data }
        : device
    ));
  };

  return (
    <div className="monitoring-dashboard">
      <div className="grid grid-cols-3 gap-4">
        <DeviceStatusPanel devices={devices} />
        <LiveChartsPanel sensorData={sensorData} />
        <AlertsPanel />
      </div>
    </div>
  );
}

interface Device {
  id: string;
  name: string;
  status: string;
  lastSeen: Date;
}

interface SensorReading {
  deviceId: string;
  sensorType: string;
  value: number;
  timestamp: number;
}
```

## Live Charts

```typescript
// components/LiveChart.tsx
import { Line } from 'react-chartjs-2';
import { useEffect, useState } from 'react';

export function LiveChart({ deviceId, sensorType }: LiveChartProps) {
  const [dataPoints, setDataPoints] = useState<DataPoint[]>([]);
  const maxPoints = 50;

  useEffect(() => {
    const socket = io('http://localhost:3000');

    socket.emit('subscribe-device', deviceId);

    socket.on('device-update', (data) => {
      if (data.sensorType === sensorType) {
        setDataPoints(prev => {
          const newPoints = [...prev, {
            timestamp: data.timestamp,
            value: data.value
          }];
          return newPoints.slice(-maxPoints);
        });
      }
    });

    return () => {
      socket.emit('unsubscribe-device', deviceId);
      socket.close();
    };
  }, [deviceId, sensorType]);

  const chartData = {
    labels: dataPoints.map(p => new Date(p.timestamp).toLocaleTimeString()),
    datasets: [{
      label: sensorType,
      data: dataPoints.map(p => p.value),
      borderColor: 'rgb(75, 192, 192)',
      tension: 0.4,
      fill: false
    }]
  };

  const options = {
    responsive: true,
    animation: { duration: 0 },
    scales: {
      x: { display: false },
      y: { beginAtZero: false }
    }
  };

  return <Line data={chartData} options={options} />;
}

interface LiveChartProps {
  deviceId: string;
  sensorType: string;
}

interface DataPoint {
  timestamp: number;
  value: number;
}
```

## Gauges

```typescript
// components/GaugeWidget.tsx
import { useEffect, useState } from 'react';

export function GaugeWidget({ deviceId, sensorType, min, max }: GaugeProps) {
  const [value, setValue] = useState(0);

  useEffect(() => {
    const socket = io('http://localhost:3000');

    socket.emit('subscribe-device', deviceId);

    socket.on('device-update', (data) => {
      if (data.sensorType === sensorType) {
        setValue(data.value);
      }
    });

    return () => {
      socket.close();
    };
  }, [deviceId, sensorType]);

  const percentage = ((value - min) / (max - min)) * 100;
  const rotation = (percentage / 100) * 180 - 90;

  return (
    <div className="gauge">
      <svg viewBox="0 0 200 120">
        <path
          d="M 20 100 A 80 80 0 0 1 180 100"
          fill="none"
          stroke="#e0e0e0"
          strokeWidth="20"
        />
        <path
          d="M 20 100 A 80 80 0 0 1 180 100"
          fill="none"
          stroke="#4caf50"
          strokeWidth="20"
          strokeDasharray={`${percentage * 2.51} 251`}
        />
        <line
          x1="100"
          y1="100"
          x2="100"
          y2="40"
          stroke="#333"
          strokeWidth="3"
          transform={`rotate(${rotation} 100 100)`}
        />
      </svg>
      <div className="gauge-value">{value.toFixed(1)}</div>
    </div>
  );
}

interface GaugeProps {
  deviceId: string;
  sensorType: string;
  min: number;
  max: number;
}
```

## Alert System

```typescript
// services/alert.service.ts
export class AlertService {
  async checkThresholds(deviceId: string, sensorType: string, value: number): Promise<void> {
    const rules = await db.alertRule.findMany({
      where: {
        deviceId,
        sensorType,
        enabled: true
      }
    });

    for (const rule of rules) {
      if (this.isThresholdExceeded(value, rule)) {
        await this.createAlert(deviceId, sensorType, value, rule);
      }
    }
  }

  private isThresholdExceeded(value: number, rule: AlertRule): boolean {
    switch (rule.condition) {
      case 'greater_than':
        return value > rule.threshold;
      case 'less_than':
        return value < rule.threshold;
      case 'equals':
        return value === rule.threshold;
      default:
        return false;
    }
  }

  private async createAlert(
    deviceId: string,
    sensorType: string,
    value: number,
    rule: AlertRule
  ): Promise<void> {
    const alert = await db.alert.create({
      data: {
        deviceId,
        sensorType,
        value,
        ruleId: rule.id,
        severity: rule.severity,
        message: `${sensorType} ${rule.condition} ${rule.threshold}. Current: ${value}`,
        acknowledged: false
      }
    });

    // Send notifications
    await this.sendNotifications(alert);

    // Emit WebSocket event
    io.emit('alert-created', alert);
  }

  private async sendNotifications(alert: Alert): Promise<void> {
    // Send email
    if (alert.severity === 'critical') {
      await emailService.sendAlert(alert);
    }

    // Send push notification
    await pushService.sendAlert(alert);
  }
}

interface AlertRule {
  id: string;
  deviceId: string;
  sensorType: string;
  condition: string;
  threshold: number;
  severity: string;
  enabled: boolean;
}
```

## Map Visualization

```typescript
// components/DeviceMap.tsx
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';

export function DeviceMap({ devices }: { devices: Device[] }) {
  return (
    <MapContainer center={[0, 0]} zoom={2} style={{ height: '500px' }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; OpenStreetMap contributors'
      />
      {devices.map(device => (
        device.location && (
          <Marker
            key={device.id}
            position={[device.location.lat, device.location.lng]}
          >
            <Popup>
              <div>
                <h3>{device.name}</h3>
                <p>Status: {device.status}</p>
                <p>Last Seen: {new Date(device.lastSeen).toLocaleString()}</p>
              </div>
            </Popup>
          </Marker>
        )
      ))}
    </MapContainer>
  );
}
```

## Performance Optimization

```typescript
// hooks/useThrottledSocket.ts
import { useEffect, useRef } from 'react';
import { throttle } from 'lodash';

export function useThrottledSocket(
  event: string,
  callback: (data: any) => void,
  delay: number = 1000
) {
  const throttledCallback = useRef(throttle(callback, delay)).current;

  useEffect(() => {
    const socket = io('http://localhost:3000');

    socket.on(event, throttledCallback);

    return () => {
      socket.off(event, throttledCallback);
      socket.close();
    };
  }, [event, throttledCallback]);
}

// Data aggregation
export class DataAggregator {
  private buffer: any[] = [];
  private flushInterval: NodeJS.Timeout;

  constructor(private flushCallback: (data: any[]) => void, interval: number = 1000) {
    this.flushInterval = setInterval(() => this.flush(), interval);
  }

  add(data: any): void {
    this.buffer.push(data);
  }

  private flush(): void {
    if (this.buffer.length > 0) {
      this.flushCallback([...this.buffer]);
      this.buffer = [];
    }
  }

  destroy(): void {
    clearInterval(this.flushInterval);
    this.flush();
  }
}
```

## Best Practices

1. **WebSocket** - Use WebSocket for real-time updates
2. **Throttling** - Throttle high-frequency updates
3. **Aggregation** - Aggregate data before sending
4. **Caching** - Cache dashboard data
5. **Lazy Loading** - Load historical data on demand
6. **Alerts** - Implement threshold-based alerts
7. **Performance** - Optimize chart rendering
8. **Mobile** - Design responsive dashboards
9. **Offline** - Handle offline gracefully
10. **Security** - Authenticate WebSocket connections

---

## Quick Start

### Real-time Dashboard

```typescript
// Server - WebSocket
io.on('connection', (socket) => {
  // Send initial data
  socket.emit('dashboard:data', getDashboardData())
  
  // Send updates every second
  const interval = setInterval(() => {
    socket.emit('dashboard:update', getDashboardData())
  }, 1000)
  
  socket.on('disconnect', () => {
    clearInterval(interval)
  })
})

// Client
socket.on('dashboard:update', (data) => {
  updateDashboard(data)
})
```

---

## Production Checklist

- [ ] **WebSocket**: WebSocket connection for real-time
- [ ] **Data Aggregation**: Aggregate data on backend
- [ ] **Throttling**: Throttle high-frequency updates
- [ ] **Caching**: Cache dashboard data
- [ ] **Lazy Loading**: Load historical data on demand
- [ ] **Alerts**: Threshold-based alerts
- [ ] **Performance**: Optimize chart rendering
- [ ] **Mobile**: Responsive dashboards
- [ ] **Offline**: Handle offline gracefully
- [ ] **Security**: Authenticate WebSocket connections
- [ ] **Testing**: Test with real devices
- [ ] **Documentation**: Document monitoring system

---

## Anti-patterns

### ❌ Don't: Too Frequent Updates

```typescript
// ❌ Bad - Update every millisecond
setInterval(() => {
  socket.emit('update', data)
}, 1)  // Too frequent!
```

```typescript
// ✅ Good - Throttled updates
const throttle = require('lodash/throttle')
const sendUpdate = throttle((data) => {
  socket.emit('update', data)
}, 1000)  // Max once per second
```

### ❌ Don't: No Aggregation

```typescript
// ❌ Bad - Send raw data
socket.emit('update', rawSensorData)  // Too much data!
```

```typescript
// ✅ Good - Aggregate first
const aggregated = aggregateSensorData(rawSensorData)
socket.emit('update', aggregated)  // Summary data
```

---

## Integration Points

- **Device Management** (`36-iot-integration/device-management/`) - Device data
- **IoT Protocols** (`36-iot-integration/iot-protocols/`) - Device communication
- **Real-time Dashboard** (`34-real-time-features/real-time-dashboard/`) - Dashboard patterns

---

## Further Reading

- [Socket.IO](https://socket.io/)
- [IoT Monitoring Best Practices](https://aws.amazon.com/iot-core/features/device-management/)

---

## Quick Start

### Real-time Dashboard

```typescript
// Server - WebSocket
io.on('connection', (socket) => {
  // Send initial data
  socket.emit('dashboard:data', getDashboardData())
  
  // Send updates every second
  const interval = setInterval(() => {
    socket.emit('dashboard:update', getDashboardData())
  }, 1000)
  
  socket.on('disconnect', () => {
    clearInterval(interval)
  })
})

// Client
socket.on('dashboard:update', (data) => {
  updateDashboard(data)
})
```

---

## Production Checklist

- [ ] **WebSocket**: WebSocket connection for real-time
- [ ] **Data Aggregation**: Aggregate data on backend
- [ ] **Throttling**: Throttle high-frequency updates
- [ ] **Caching**: Cache dashboard data
- [ ] **Lazy Loading**: Load historical data on demand
- [ ] **Alerts**: Threshold-based alerts
- [ ] **Performance**: Optimize chart rendering
- [ ] **Mobile**: Responsive dashboards
- [ ] **Offline**: Handle offline gracefully
- [ ] **Security**: Authenticate WebSocket connections
- [ ] **Testing**: Test with real devices
- [ ] **Documentation**: Document monitoring system

---

## Anti-patterns

### ❌ Don't: Too Frequent Updates

```typescript
// ❌ Bad - Update every millisecond
setInterval(() => {
  socket.emit('update', data)
}, 1)  // Too frequent!
```

```typescript
// ✅ Good - Throttled updates
const throttle = require('lodash/throttle')
const sendUpdate = throttle((data) => {
  socket.emit('update', data)
}, 1000)  // Max once per second
```

### ❌ Don't: No Aggregation

```typescript
// ❌ Bad - Send raw data
socket.emit('update', rawSensorData)  // Too much data!
```

```typescript
// ✅ Good - Aggregate first
const aggregated = aggregateSensorData(rawSensorData)
socket.emit('update', aggregated)  // Summary data
```

---

## Integration Points

- **Device Management** (`36-iot-integration/device-management/`) - Device data
- **IoT Protocols** (`36-iot-integration/iot-protocols/`) - Device communication
- **Real-time Dashboard** (`34-real-time-features/real-time-dashboard/`) - Dashboard patterns

---

## Further Reading

- [Socket.IO](https://socket.io/)
- [IoT Monitoring Best Practices](https://aws.amazon.com/iot-core/features/device-management/)

## Resources
- [Chart.js](https://www.chartjs.org/)
- [Leaflet](https://leafletjs.com/)
- [React Leaflet](https://react-leaflet.js.org/)
