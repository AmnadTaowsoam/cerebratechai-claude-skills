---
name: IoT Protocols
description: Communication protocols for IoT devices including MQTT, CoAP, AMQP, and protocol selection strategies for efficient device-to-cloud communication.
---

# IoT Protocols

> **Current Level:** Intermediate  
> **Domain:** IoT / Networking

---

## Overview

IoT protocols enable communication between devices, gateways, and cloud services. This guide covers MQTT, CoAP, AMQP, and protocol selection strategies for building efficient IoT systems that handle constrained devices, low bandwidth, and unreliable networks.

---

---

## Core Concepts

### IoT Protocol Comparison

| Protocol | Transport | Overhead | Use Case | QoS |
|----------|-----------|----------|----------|-----|
| **MQTT** | TCP | Low | Pub/Sub messaging | 0, 1, 2 |
| **CoAP** | UDP | Very Low | Constrained devices | Confirmable/Non-confirmable |
| **AMQP** | TCP | Medium | Enterprise messaging | At-most-once, At-least-once, Exactly-once |
| **HTTP/HTTPS** | TCP | High | Request/Response | None |
| **WebSocket** | TCP | Low | Bidirectional | None |

## When to Use Each Protocol

### MQTT
- **Use when:**
  - Low bandwidth required
  - Unreliable networks
  - Pub/Sub pattern needed
  - Battery-powered devices
- **Examples:** Sensors, smart home, telemetry

### CoAP
- **Use when:**
  - Extremely constrained devices
  - UDP preferred
  - RESTful API needed
- **Examples:** Microcontrollers, mesh networks

### AMQP
- **Use when:**
  - Enterprise integration
  - Complex routing needed
  - Guaranteed delivery critical
- **Examples:** Industrial IoT, financial systems

### HTTP/HTTPS
- **Use when:**
  - Simple request/response
  - Existing infrastructure
  - Not resource-constrained
- **Examples:** Web-connected devices, APIs

## MQTT Deep Dive

### Basic MQTT Client

```typescript
// mqtt-client.ts
import mqtt from 'mqtt';

export class MQTTClient {
  private client: mqtt.MqttClient;

  constructor(brokerUrl: string, options?: mqtt.IClientOptions) {
    this.client = mqtt.connect(brokerUrl, {
      clientId: `mqtt_${Math.random().toString(16).slice(3)}`,
      clean: true,
      connectTimeout: 4000,
      username: process.env.MQTT_USERNAME,
      password: process.env.MQTT_PASSWORD,
      reconnectPeriod: 1000,
      ...options
    });

    this.setupEventHandlers();
  }

  private setupEventHandlers(): void {
    this.client.on('connect', () => {
      console.log('MQTT connected');
    });

    this.client.on('error', (error) => {
      console.error('MQTT error:', error);
    });

    this.client.on('reconnect', () => {
      console.log('MQTT reconnecting...');
    });

    this.client.on('offline', () => {
      console.log('MQTT offline');
    });
  }

  subscribe(topic: string, qos: 0 | 1 | 2 = 0): void {
    this.client.subscribe(topic, { qos }, (error) => {
      if (error) {
        console.error('Subscribe error:', error);
      } else {
        console.log(`Subscribed to ${topic}`);
      }
    });
  }

  publish(topic: string, message: string | Buffer, qos: 0 | 1 | 2 = 0, retain: boolean = false): void {
    this.client.publish(topic, message, { qos, retain }, (error) => {
      if (error) {
        console.error('Publish error:', error);
      }
    });
  }

  onMessage(callback: (topic: string, message: Buffer) => void): void {
    this.client.on('message', callback);
  }

  disconnect(): void {
    this.client.end();
  }
}

// Usage
const mqttClient = new MQTTClient('mqtt://broker.hivemq.com:1883');

mqttClient.subscribe('sensors/temperature', 1);

mqttClient.onMessage((topic, message) => {
  console.log(`Received on ${topic}:`, message.toString());
});

mqttClient.publish('sensors/temperature', JSON.stringify({
  value: 23.5,
  unit: 'celsius',
  timestamp: Date.now()
}), 1);
```

### QoS Levels

```typescript
// QoS 0: At most once (Fire and forget)
mqttClient.publish('sensors/data', message, 0);

// QoS 1: At least once (Acknowledged delivery)
mqttClient.publish('sensors/data', message, 1);

// QoS 2: Exactly once (Assured delivery)
mqttClient.publish('sensors/data', message, 2);
```

### Topics

```typescript
// Topic structure
const topics = {
  // Hierarchical topics
  temperature: 'home/livingroom/temperature',
  humidity: 'home/livingroom/humidity',
  
  // Wildcards
  allSensors: 'home/+/temperature',      // + matches single level
  everything: 'home/#',                   // # matches multiple levels
  
  // Best practices
  deviceData: 'devices/{deviceId}/data',
  deviceStatus: 'devices/{deviceId}/status',
  deviceCommands: 'devices/{deviceId}/commands'
};

// Subscribe to wildcards
mqttClient.subscribe('home/+/temperature', 1);
mqttClient.subscribe('devices/#', 1);
```

### Retained Messages

```typescript
// Publish retained message (last known good value)
mqttClient.publish('sensors/temperature', '23.5', 1, true);

// New subscribers immediately receive retained message
mqttClient.subscribe('sensors/temperature', 1);
// Will receive '23.5' immediately

// Clear retained message
mqttClient.publish('sensors/temperature', '', 1, true);
```

### Last Will and Testament (LWT)

```typescript
const mqttClient = mqtt.connect('mqtt://broker.hivemq.com:1883', {
  will: {
    topic: 'devices/device123/status',
    payload: JSON.stringify({ status: 'offline' }),
    qos: 1,
    retain: true
  }
});

// When client disconnects unexpectedly, broker publishes LWT
```

## CoAP Basics

```typescript
// coap-client.ts
import coap from 'coap';

export class CoAPClient {
  async get(url: string): Promise<any> {
    return new Promise((resolve, reject) => {
      const req = coap.request(url);

      req.on('response', (res) => {
        resolve(JSON.parse(res.payload.toString()));
      });

      req.on('error', reject);

      req.end();
    });
  }

  async post(url: string, data: any): Promise<any> {
    return new Promise((resolve, reject) => {
      const req = coap.request({
        method: 'POST',
        hostname: new URL(url).hostname,
        pathname: new URL(url).pathname,
        confirmable: true
      });

      req.write(JSON.stringify(data));

      req.on('response', (res) => {
        resolve(JSON.parse(res.payload.toString()));
      });

      req.on('error', reject);

      req.end();
    });
  }

  observe(url: string, callback: (data: any) => void): () => void {
    const req = coap.request({
      method: 'GET',
      hostname: new URL(url).hostname,
      pathname: new URL(url).pathname,
      observe: true
    });

    req.on('response', (res) => {
      res.on('data', (data) => {
        callback(JSON.parse(data.toString()));
      });
    });

    req.end();

    // Return cleanup function
    return () => {
      req.close();
    };
  }
}

// CoAP Server
import { createServer } from 'coap';

const server = createServer();

server.on('request', (req, res) => {
  if (req.url === '/temperature') {
    res.end(JSON.stringify({
      value: 23.5,
      unit: 'celsius'
    }));
  }
});

server.listen(5683, () => {
  console.log('CoAP server listening on port 5683');
});
```

## Security (TLS/DTLS)

### MQTT with TLS

```typescript
import fs from 'fs';

const mqttClient = mqtt.connect('mqtts://broker.example.com:8883', {
  ca: fs.readFileSync('ca.crt'),
  cert: fs.readFileSync('client.crt'),
  key: fs.readFileSync('client.key'),
  rejectUnauthorized: true
});
```

### CoAP with DTLS

```typescript
import coap from 'coap';

const req = coap.request({
  hostname: 'coaps://server.example.com',
  port: 5684,
  method: 'GET',
  pathname: '/sensor',
  agent: new coap.Agent({
    type: 'udp6',
    socket: {
      type: 'dtls',
      key: fs.readFileSync('client-key.pem'),
      cert: fs.readFileSync('client-cert.pem')
    }
  })
});
```

## Protocol Bridging

```typescript
// mqtt-to-http-bridge.ts
export class MQTTtoHTTPBridge {
  private mqttClient: MQTTClient;

  constructor(mqttBroker: string, httpEndpoint: string) {
    this.mqttClient = new MQTTClient(mqttBroker);

    this.mqttClient.subscribe('sensors/#', 1);

    this.mqttClient.onMessage(async (topic, message) => {
      await this.forwardToHTTP(topic, message, httpEndpoint);
    });
  }

  private async forwardToHTTP(topic: string, message: Buffer, endpoint: string): Promise<void> {
    try {
      const data = JSON.parse(message.toString());

      await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          topic,
          data,
          timestamp: Date.now()
        })
      });
    } catch (error) {
      console.error('Bridge error:', error);
    }
  }
}

// Usage
const bridge = new MQTTtoHTTPBridge(
  'mqtt://broker.hivemq.com:1883',
  'https://api.example.com/iot/data'
);
```

## AMQP Example

```typescript
// amqp-client.ts
import amqp from 'amqplib';

export class AMQPClient {
  private connection: amqp.Connection | null = null;
  private channel: amqp.Channel | null = null;

  async connect(url: string): Promise<void> {
    this.connection = await amqp.connect(url);
    this.channel = await this.connection.createChannel();
  }

  async publish(exchange: string, routingKey: string, message: any): Promise<void> {
    if (!this.channel) throw new Error('Not connected');

    await this.channel.assertExchange(exchange, 'topic', { durable: true });

    this.channel.publish(
      exchange,
      routingKey,
      Buffer.from(JSON.stringify(message)),
      { persistent: true }
    );
  }

  async consume(queue: string, callback: (message: any) => void): Promise<void> {
    if (!this.channel) throw new Error('Not connected');

    await this.channel.assertQueue(queue, { durable: true });

    this.channel.consume(queue, (msg) => {
      if (msg) {
        const data = JSON.parse(msg.content.toString());
        callback(data);
        this.channel!.ack(msg);
      }
    });
  }

  async close(): Promise<void> {
    await this.channel?.close();
    await this.connection?.close();
  }
}

// Usage
const amqpClient = new AMQPClient();
await amqpClient.connect('amqp://localhost');

await amqpClient.publish('iot', 'sensors.temperature', {
  value: 23.5,
  timestamp: Date.now()
});

await amqpClient.consume('sensor-data', (message) => {
  console.log('Received:', message);
});
```

## WebSocket for IoT

```typescript
// websocket-iot.ts
import WebSocket from 'ws';

export class IoTWebSocketServer {
  private wss: WebSocket.Server;
  private clients = new Map<string, WebSocket>();

  constructor(port: number) {
    this.wss = new WebSocket.Server({ port });

    this.wss.on('connection', (ws, req) => {
      const deviceId = new URL(req.url!, 'ws://localhost').searchParams.get('deviceId');

      if (deviceId) {
        this.clients.set(deviceId, ws);

        ws.on('message', (data) => {
          this.handleMessage(deviceId, data.toString());
        });

        ws.on('close', () => {
          this.clients.delete(deviceId);
        });
      }
    });
  }

  private handleMessage(deviceId: string, message: string): void {
    const data = JSON.parse(message);
    console.log(`Device ${deviceId}:`, data);

    // Broadcast to all clients
    this.broadcast({
      deviceId,
      data,
      timestamp: Date.now()
    });
  }

  broadcast(message: any): void {
    const payload = JSON.stringify(message);

    this.clients.forEach((client) => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(payload);
      }
    });
  }

  sendToDevice(deviceId: string, message: any): void {
    const client = this.clients.get(deviceId);

    if (client && client.readyState === WebSocket.OPEN) {
      client.send(JSON.stringify(message));
    }
  }
}
```

---

## Quick Start

### MQTT Client Setup

```javascript
const mqtt = require('mqtt')

const client = mqtt.connect('mqtt://broker.example.com', {
  clientId: 'device-001',
  username: 'device-user',
  password: 'device-password'
})

client.on('connect', () => {
  // Subscribe to topic
  client.subscribe('devices/001/data')
  
  // Publish message
  client.publish('devices/001/data', JSON.stringify({
    temperature: 25.5,
    humidity: 60
  }))
})

client.on('message', (topic, message) => {
  const data = JSON.parse(message.toString())
  console.log('Received:', data)
})
```

### MQTT Server (Mosquitto)

```bash
# Install Mosquitto
sudo apt-get install mosquitto mosquitto-clients

# Start broker
mosquitto -c /etc/mosquitto/mosquitto.conf
```

---

## Production Checklist

- [ ] **Protocol Selection**: Choose appropriate protocol (MQTT, CoAP, AMQP)
- [ ] **QoS Levels**: Use appropriate QoS for message reliability
- [ ] **Topic Design**: Hierarchical topic structure
- [ ] **Security**: TLS/DTLS encryption in production
- [ ] **Authentication**: Device authentication configured
- [ ] **Error Handling**: Handle disconnections gracefully
- [ ] **Reconnection**: Exponential backoff for reconnection
- [ ] **Message Size**: Keep messages small for constrained devices
- [ ] **Retained Messages**: Use for last known state
- [ ] **Monitoring**: Monitor device connectivity and message rates
- [ ] **Rate Limiting**: Prevent message flooding
- [ ] **Testing**: Test with real devices

---

## Anti-patterns

### ❌ Don't: No Security

```javascript
// ❌ Bad - No encryption
const client = mqtt.connect('mqtt://broker.example.com')  // Plain text!
```

```javascript
// ✅ Good - TLS encryption
const client = mqtt.connect('mqtts://broker.example.com', {
  ca: fs.readFileSync('ca.crt'),
  cert: fs.readFileSync('client.crt'),
  key: fs.readFileSync('client.key')
})
```

### ❌ Don't: Large Messages

```javascript
// ❌ Bad - Large payload
client.publish('topic', largeJsonString)  // Too big for IoT!
```

```javascript
// ✅ Good - Small, efficient messages
client.publish('topic', JSON.stringify({
  t: 25.5,  // temperature
  h: 60     // humidity
}))
```

### ❌ Don't: No Reconnection Logic

```javascript
// ❌ Bad - No reconnection
client.on('close', () => {
  // Device stays disconnected!
})
```

```javascript
// ✅ Good - Automatic reconnection
client.on('close', () => {
  setTimeout(() => {
    client.reconnect()  // Reconnect with backoff
  }, 5000)
})
```

---

## Integration Points

- **IoT Security** (`36-iot-integration/iot-security/`) - Device security
- **Device Management** (`36-iot-integration/device-management/`) - Device lifecycle
- **MQTT Integration** (`08-messaging-queue/mqtt-integration/`) - MQTT patterns

---

## Further Reading

- [MQTT Specification](https://mqtt.org/mqtt-specification/)
- [Eclipse Mosquitto](https://mosquitto.org/)
- [CoAP Specification](https://coap.technology/)
9. **LWT** - Implement Last Will and Testament
10. **Monitoring** - Monitor protocol performance

## Resources

- [MQTT Specification](https://mqtt.org/)
- [CoAP RFC](https://datatracker.ietf.org/doc/html/rfc7252)
- [AMQP](https://www.amqp.org/)
- [HiveMQ](https://www.hivemq.com/)
- [Eclipse Mosquitto](https://mosquitto.org/)
