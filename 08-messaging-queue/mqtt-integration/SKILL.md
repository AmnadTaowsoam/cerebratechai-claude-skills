# MQTT Integration

## Overview
This skill covers MQTT integration for IoT applications.

## Key Topics
- MQTT brokers
- Topic patterns
- QoS levels
- Last will and testament
- Security and authentication
## Overview

MQTT (Message Queuing Telemetry Transport) is a lightweight publish/subscribe messaging protocol designed for IoT and low-bandwidth, high-latency networks. It provides a simple and efficient way to communicate between devices and servers.

### Key Features

- **Lightweight**: Minimal protocol overhead (2-byte header)
- **Publish/Subscribe**: Decouples publishers and subscribers
- **QoS Levels**: Three levels of message delivery guarantees
- **Last Will and Testament**: Notification when client disconnects unexpectedly
- **Retained Messages**: Store latest message for new subscribers
- **Topic Wildcards**: Subscribe to multiple topics with patterns
- **Session Persistence**: Maintain state across connections

### Use Cases

- IoT device communication
- Sensor data collection
- Home automation
- Industrial monitoring
- Real-time dashboards
- Mobile push notifications

---

## MQTT Concepts

### QoS Levels

```python
# MQTT QoS Levels
"""
QoS 0 - At most once: Fire and forget, no delivery guarantee
QoS 1 - At least once: Message delivered at least once, may duplicate
QoS 2 - Exactly once: Message delivered exactly once, no duplicates
"""
```

### Topic Structure

```python
# MQTT Topic Structure
"""
Topics are hierarchical using / separator
Examples:
  - home/livingroom/temperature
  - sensors/+/temperature (wildcard for single level)
  - sensors/# (wildcard for multiple levels)
  - $SYS/broker/uptime (system topics start with $)
"""
```

### Connection Flow

```python
# MQTT Connection Flow
"""
1. Client connects to broker with CONNECT packet
2. Broker responds with CONNACK packet
3. Client subscribes to topics with SUBSCRIBE packet
4. Broker responds with SUBACK packet
5. Client publishes messages with PUBLISH packet
6. Broker delivers to subscribers based on QoS
7. Client disconnects with DISCONNECT packet
"""
```

---

## Basic Setup

### MQTT Broker Setup (Mosquitto)

```bash
# mosquitto.conf
listener 1883
allow_anonymous false
password_file /etc/mosquitto/passwd
persistence true
persistence_location /var/lib/mosquitto/
log_dest file /var/log/mosquitto/mosquitto.log
```

### Python Client Setup

```python
# mqtt_client.py
import paho.mqtt.client as mqtt
import json
import logging
from typing import Callable, Optional

class MQTTClient:
    def __init__(
        self,
        broker_host: str = 'localhost',
        broker_port: int = 1883,
        client_id: str = None,
        username: str = None,
        password: str = None
    ):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.client_id = client_id or f'mqtt_client_{id(self)}'
        
        self.client = mqtt.Client(client_id=self.client_id)
        
        if username and password:
            self.client.username_pw_set(username, password)
        
        self.setup_callbacks()
    
    def setup_callbacks(self):
        """Setup MQTT client callbacks"""
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        self.client.on_subscribe = self.on_subscribe
        self.client.on_unsubscribe = self.on_unsubscribe
    
    def on_connect(self, client, userdata, flags, rc):
        """Callback when connected to broker"""
        if rc == 0:
            logging.info(f"Connected to {self.broker_host}:{self.broker_port}")
        else:
            logging.error(f"Connection failed with code {rc}")
    
    def on_disconnect(self, client, userdata, rc):
        """Callback when disconnected from broker"""
        if rc != 0:
            logging.warning(f"Unexpected disconnect, code: {rc}")
        else:
            logging.info("Disconnected from broker")
    
    def on_message(self, client, userdata, msg):
        """Callback when message received"""
        logging.info(f"Received on {msg.topic}: {msg.payload.decode()}")
    
    def on_publish(self, client, userdata, mid):
        """Callback when message published"""
        logging.info(f"Message {mid} published successfully")
    
    def on_subscribe(self, client, userdata, mid, granted_qos):
        """Callback when subscribed to topic"""
        logging.info(f"Subscribed with QoS {granted_qos}")
    
    def on_unsubscribe(self, client, userdata, mid):
        """Callback when unsubscribed"""
        logging.info(f"Unsubscribed successfully")
    
    def connect(self) -> None:
        """Connect to MQTT broker"""
        try:
            self.client.connect(self.broker_host, self.broker_port, 60)
            self.client.loop_start()
        except Exception as e:
            logging.error(f"Connection error: {e}")
            raise
    
    def disconnect(self) -> None:
        """Disconnect from MQTT broker"""
        self.client.loop_stop()
        self.client.disconnect()
    
    def publish(
        self,
        topic: str,
        payload: any,
        qos: int = 0,
        retain: bool = False
    ) -> None:
        """Publish message to topic"""
        if isinstance(payload, dict):
            payload = json.dumps(payload)
        
        result = self.client.publish(topic, payload, qos=qos, retain=retain)
        result.wait_for_publish()
    
    def subscribe(
        self,
        topic: str,
        qos: int = 0,
        callback: Callable = None
    ) -> None:
        """Subscribe to topic"""
        if callback:
            self.client.message_callback_add(topic, callback)
        
        self.client.subscribe(topic, qos=qos)
    
    def unsubscribe(self, topic: str) -> None:
        """Unsubscribe from topic"""
        self.client.unsubscribe(topic)
    
    def set_last_will(
        self,
        topic: str,
        payload: str,
        qos: int = 0,
        retain: bool = False
    ) -> None:
        """Set last will and testament"""
        self.client.will_set(topic, payload, qos=qos, retain=retain)

# Usage
client = MQTTClient(
    broker_host='localhost',
    broker_port=1883,
    username='user',
    password='pass'
)

# Set last will
client.set_last_will('status/client', 'offline', retain=True)

# Connect
client.connect()

# Subscribe
client.subscribe('sensors/+/temperature', qos=1)

# Publish
client.publish('sensors/room1/temperature', {'value': 22.5, 'unit': 'C'}, qos=1)
```

---

## QoS Levels

### QoS 0 - At Most Once

```python
# qos0_publisher.py
client.publish('sensors/temperature', {'value': 22.5}, qos=0)
# Fire and forget, no delivery guarantee
```

### QoS 1 - At Least Once

```python
# qos1_publisher.py
# Message delivered at least once, may receive duplicates
client.publish('alerts/critical', {'alert': 'High temperature'}, qos=1)
```

### QoS 2 - Exactly Once

```python
# qos2_publisher.py
# Message delivered exactly once, no duplicates
client.publish('commands/valve', {'action': 'close'}, qos=2)
```

---

## Topic Patterns

### Single Level Wildcard (+)

```python
# Subscribe to all temperature sensors
client.subscribe('sensors/+/temperature')
# Matches: sensors/room1/temperature, sensors/outdoor/temperature
# Does not match: sensors/room1/temperature/status
```

### Multi Level Wildcard (#)

```python
# Subscribe to all sensor data
client.subscribe('sensors/#')
# Matches: sensors/room1/temperature, sensors/room1/humidity
# Does not match: sensors (must have at least one level after)
```

### Topic Filters

```python
# Subscribe to specific room data
client.subscribe('home/livingroom/+')
# Matches: home/livingroom/temperature, home/livingroom/light
```

---

## Last Will and Testament

### Setting LWT

```python
# lwt_example.py
client.set_last_will(
    topic='status/client',
    payload='offline',
    qos=1,
    retain=True
)

client.connect()

# If client disconnects unexpectedly, broker will publish:
# topic: status/client
# payload: offline
# retain: true (so new subscribers see the status)
```

### Monitoring LWT

```python
# lwt_monitor.py
def on_lwt_message(client, userdata, msg):
    status = msg.payload.decode()
    topic = msg.topic
    print(f"Client status: {status} on {topic}")

client.subscribe('status/+', callback=on_lwt_message)
```

---

## Retained Messages

### Publishing Retained Messages

```python
# retained_messages.py
# Publish retained message
client.publish('config/valve', {'position': 'closed'}, retain=True)

# New subscribers will immediately receive this message
```

### Clearing Retained Messages

```python
# Clear retained message by publishing empty payload
client.publish('config/valve', '', retain=True)
```

---

## Best Practices

### Topic Design

- **Use hierarchical topic structure**: Organize topics logically (e.g., `home/livingroom/temperature`)
- **Keep topic names descriptive**: Use clear, meaningful names
- **Avoid deep hierarchies**: Limit to 3-5 levels for clarity
- **Use consistent naming**: Follow naming conventions (e.g., lowercase, underscores)
- **Plan for wildcards**: Structure topics to support wildcard subscriptions

### QoS Selection

- **QoS 0**: Use for non-critical, high-frequency data (e.g., sensor readings)
- **QoS 1**: Use for important messages where duplicates are acceptable (e.g., alerts)
- **QoS 2**: Use for critical commands where duplicates are unacceptable (e.g., control commands)
- **Match QoS to use case**: Don't use higher QoS than necessary
- **Consider bandwidth impact**: Higher QoS increases protocol overhead

### Connection Management

- **Use unique client IDs**: Ensure each client has a unique identifier
- **Implement reconnection logic**: Handle network failures gracefully
- **Use keepalive**: Configure appropriate keepalive interval
- **Set reasonable timeouts**: Configure connection and operation timeouts
- **Handle disconnects cleanly**: Use DISCONNECT packet when possible

### Security

- **Enable authentication**: Use username/password or certificates
- **Use TLS encryption**: Encrypt connections in production
- **Disable anonymous access**: Require authentication for all clients
- **Use ACLs**: Restrict topic access based on user roles
- **Rotate credentials**: Regularly update passwords and certificates

### Performance

- **Use retained messages sparingly**: They consume broker memory
- **Batch messages when possible**: Reduce number of PUBLISH packets
- **Use appropriate keepalive**: Balance between responsiveness and overhead
- **Monitor broker resources**: Track memory, CPU, and connection counts
- **Use topic aliases**: Reduce bandwidth for repeated topic names

### Reliability

- **Use Last Will and Testament**: Detect unexpected disconnections
- **Implement message acknowledgment**: Handle QoS properly
- **Monitor message delivery**: Track published and received messages
- **Handle duplicate messages**: Design consumers to handle duplicates (QoS 1)
- **Test failure scenarios**: Verify behavior under network failures

### Monitoring

- **Track client connections**: Monitor connected clients and disconnections
- **Monitor message rates**: Track publish and subscribe rates
- **Alert on broker issues**: Set up alerts for broker failures
- **Log important events**: Record connections, publishes, and errors
- **Use metrics**: Collect and visualize broker and client metrics

## Checklist

### Setup and Configuration
- [ ] Install and configure MQTT broker (Mosquitto/EMQX/HiveMQ)
- [ ] Enable authentication (username/password or certificates)
- [ ] Configure TLS encryption for secure connections
- [ ] Set up access control lists (ACLs)
- [ ] Configure broker persistence and logging

### Client Configuration
- [ ] Use unique client IDs for all clients
- [ ] Configure appropriate keepalive interval
- [ ] Set up reconnection logic
- [ ] Configure connection and operation timeouts
- [ ] Implement error handling and logging

### Topic Design
- [ ] Design hierarchical topic structure
- [ ] Define topic naming conventions
- [ ] Plan for wildcard subscriptions
- [ ] Document topic structure and usage
- [ ] Set up topic monitoring

### QoS Configuration
- [ ] Select appropriate QoS levels for each message type
- [ ] Implement QoS 0 for non-critical data
- [ ] Implement QoS 1 for important messages
- [ ] Implement QoS 2 for critical commands
- [ ] Test QoS behavior under failures

### Security Setup
- [ ] Enable broker authentication
- [ ] Configure TLS/SSL encryption
- [ ] Set up user roles and permissions
- [ ] Configure ACLs for topic access
- [ ] Implement credential rotation

### Reliability Features
- [ ] Configure Last Will and Testament
- [ ] Use retained messages for configuration/status
- [ ] Implement message acknowledgment
- [ ] Set up duplicate message handling
- [ ] Test failure scenarios

### Monitoring and Alerting
- [ ] Set up broker metrics collection
- [ ] Configure client connection monitoring
- [ ] Monitor message publish/subscribe rates
- [ ] Set up alerts for broker issues
- [ ] Configure log aggregation and analysis

### Testing
- [ ] Test client connection and reconnection
- [ ] Verify QoS behavior
- [ ] Test wildcard subscriptions
- [ ] Validate retained message behavior
- [ ] Test Last Will and Testament

### Documentation
- [ ] Document broker configuration
- [ ] Document topic structure and naming
- [ ] Create client usage documentation
- [ ] Document security setup
- [ ] Create runbooks for common issues
