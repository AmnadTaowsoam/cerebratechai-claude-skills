---
name: WebSocket Patterns
description: Advanced WebSocket patterns for real-time bidirectional communication in web applications.
---

# WebSocket Patterns

## Overview

WebSocket is a communication protocol that provides full-duplex communication channels over a single TCP connection. It enables real-time, event-driven communication between clients and servers, making it ideal for applications requiring instant updates such as chat applications, live dashboards, and collaborative tools.

## WebSocket Fundamentals

### What is WebSocket?

WebSocket is a protocol that:
- Provides persistent, bidirectional communication
- Uses a single TCP connection
- Operates over HTTP/1.1 during handshake, then upgrades
- Has low overhead compared to HTTP polling
- Supports both text and binary data

### WebSocket vs HTTP Polling vs SSE

| Feature | WebSocket | HTTP Polling | Server-Sent Events (SSE) |
|---------|-----------|--------------|--------------------------|
| **Direction** | Bidirectional | Client → Server | Server → Client only |
| **Connection** | Persistent | New per request | Persistent |
| **Overhead** | Low | High | Low |
| **Browser Support** | Excellent | Excellent | Excellent |
| **Binary Data** | Yes | Yes | No (text only) |
| **Reconnection** | Manual | N/A | Browser handles |
| **Use Case** | Interactive real-time | Simple updates | One-way streaming |

**When to use WebSocket:**
- Real-time chat applications
- Live collaboration tools
- Multiplayer games
- Real-time dashboards
- Stock trading platforms

**When to use HTTP Polling:**
- Simple, infrequent updates
- Legacy browser support needed
- Low complexity requirements

**When to use SSE:**
- One-way server-to-client updates
- News feeds, notifications
- Stock tickers

## Connection Lifecycle

### Handshake

The WebSocket connection starts with an HTTP upgrade request:

```http
GET /ws HTTP/1.1
Host: example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13
```

Server response:

```http
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
```

### Connection States

```javascript
const ws = new WebSocket('ws://example.com/ws');

// 0 = CONNECTING - Connection not yet open
console.log(ws.readyState === WebSocket.CONNECTING);

// 1 = OPEN - Connection is open and ready
ws.onopen = () => {
  console.log(ws.readyState === WebSocket.OPEN);
};

// 2 = CLOSING - Connection is in the process of closing
ws.onclose = () => {
  console.log(ws.readyState === WebSocket.CLOSING);
};

// 3 = CLOSED - Connection is closed
ws.onclose = () => {
  console.log(ws.readyState === WebSocket.CLOSED);
};
```

### Message Flow

```javascript
// Client sends message
ws.send(JSON.stringify({ type: 'ping', timestamp: Date.now() }));

// Server receives and responds
ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  console.log('Received:', message);
};

// Connection closes
ws.onclose = (event) => {
  console.log('Connection closed:', event.code, event.reason);
};

// Error handling
ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};
```

## Message Formats

### Text Messages

```javascript
// Sending JSON
ws.send(JSON.stringify({
  type: 'message',
  channel: 'general',
  content: 'Hello, world!',
  userId: '123',
}));

// Receiving JSON
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  switch (data.type) {
    case 'message':
      displayMessage(data);
      break;
    case 'user_joined':
      notifyUserJoined(data.user);
      break;
  }
};
```

### Binary Messages

```javascript
// Sending binary data (ArrayBuffer)
const buffer = new ArrayBuffer(1024);
const view = new DataView(buffer);
view.setUint32(0, 42);
ws.send(buffer);

// Sending binary data (Blob)
const blob = new Blob(['Hello'], { type: 'text/plain' });
ws.send(blob);

// Receiving binary data
ws.binaryType = 'arraybuffer'; // or 'blob'
ws.onmessage = (event) => {
  if (event.data instanceof ArrayBuffer) {
    const view = new DataView(event.data);
    const value = view.getUint32(0);
    console.log('Received value:', value);
  }
};
```

### Message Protocol Design

```javascript
// Standard message envelope
interface WebSocketMessage {
  id: string;           // Unique message ID
  type: string;         // Message type
  timestamp: number;    // Unix timestamp
  payload: any;         // Actual data
  correlationId?: string; // For request-response
}

// Request-response pattern
function sendRequest(ws, type, payload) {
  return new Promise((resolve, reject) => {
    const correlationId = generateId();
    const message = {
      id: generateId(),
      type,
      timestamp: Date.now(),
      payload,
      correlationId,
    };
    
    ws.send(JSON.stringify(message));
    
    const timeout = setTimeout(() => {
      pendingRequests.delete(correlationId);
      reject(new Error('Request timeout'));
    }, 5000);
    
    pendingRequests.set(correlationId, { resolve, reject, timeout });
  });
}

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  
  if (message.correlationId) {
    const pending = pendingRequests.get(message.correlationId);
    if (pending) {
      clearTimeout(pending.timeout);
      pendingRequests.delete(message.correlationId);
      if (message.error) {
        pending.reject(new Error(message.error));
      } else {
        pending.resolve(message.payload);
      }
    }
  }
};
```

## Heartbeat and Keep-Alive

### Ping-Pong Mechanism

```javascript
class WebSocketHeartbeat {
  constructor(ws, options = {}) {
    this.ws = ws;
    this.interval = options.interval || 30000; // 30 seconds
    this.timeout = options.timeout || 5000;    // 5 seconds
    this.timer = null;
    this.timeoutTimer = null;
    this.isAlive = true;
  }
  
  start() {
    this.timer = setInterval(() => {
      if (this.isAlive) {
        this.isAlive = false;
        this.ws.ping();
        
        this.timeoutTimer = setTimeout(() => {
          if (!this.isAlive) {
            console.log('Heartbeat timeout, closing connection');
            this.ws.terminate();
          }
        }, this.timeout);
      }
    }, this.interval);
  }
  
  stop() {
    clearInterval(this.timer);
    clearTimeout(this.timeoutTimer);
  }
  
  onPong() {
    this.isAlive = true;
    clearTimeout(this.timeoutTimer);
  }
}

// Usage
const ws = new WebSocket('ws://example.com/ws');
const heartbeat = new WebSocketHeartbeat(ws);

ws.onopen = () => {
  heartbeat.start();
};

ws.on('pong', () => {
  heartbeat.onPong();
});

ws.onclose = () => {
  heartbeat.stop();
};
```

### Application-Level Heartbeat

```javascript
class ApplicationHeartbeat {
  constructor(ws, options = {}) {
    this.ws = ws;
    this.interval = options.interval || 30000;
    this.timer = null;
  }
  
  start() {
    this.timer = setInterval(() => {
      this.sendHeartbeat();
    }, this.interval);
  }
  
  sendHeartbeat() {
    this.ws.send(JSON.stringify({
      type: 'heartbeat',
      timestamp: Date.now(),
    }));
  }
  
  stop() {
    clearInterval(this.timer);
  }
}

// Server-side heartbeat handler
function handleHeartbeat(ws, message) {
  if (message.type === 'heartbeat') {
    ws.send(JSON.stringify({
      type: 'heartbeat_ack',
      timestamp: Date.now(),
      originalTimestamp: message.timestamp,
    }));
  }
}
```

## Connection Management

### Connection Pooling

```javascript
class WebSocketPool {
  constructor(url, options = {}) {
    this.url = url;
    this.maxConnections = options.maxConnections || 5;
    this.connections = [];
    this.pendingRequests = [];
  }
  
  async getConnection() {
    // Find available connection
    const available = this.connections.find(
      conn => conn.readyState === WebSocket.OPEN && conn.activeRequests < 10
    );
    
    if (available) {
      return available;
    }
    
    // Create new connection if under limit
    if (this.connections.length < this.maxConnections) {
      const ws = await this.createConnection();
      this.connections.push(ws);
      return ws;
    }
    
    // Wait for available connection
    return new Promise((resolve) => {
      this.pendingRequests.push(resolve);
    });
  }
  
  async createConnection() {
    return new Promise((resolve, reject) => {
      const ws = new WebSocket(this.url);
      ws.activeRequests = 0;
      
      ws.onopen = () => {
        resolve(ws);
      };
      
      ws.onerror = reject;
      
      ws.onclose = () => {
        const index = this.connections.indexOf(ws);
        if (index > -1) {
          this.connections.splice(index, 1);
        }
      };
    });
  }
  
  releaseConnection(ws) {
    ws.activeRequests--;
    
    if (this.pendingRequests.length > 0) {
      const resolve = this.pendingRequests.shift();
      resolve(ws);
    }
  }
}
```

### Reconnection Strategies

```javascript
class WebSocketReconnector {
  constructor(url, options = {}) {
    this.url = url;
    this.maxRetries = options.maxRetries || Infinity;
    this.retryDelay = options.retryDelay || 1000;
    this.maxRetryDelay = options.maxRetryDelay || 30000;
    this.backoffMultiplier = options.backoffMultiplier || 2;
    
    this.ws = null;
    this.retryCount = 0;
    this.currentDelay = this.retryDelay;
    this.shouldReconnect = true;
  }
  
  connect() {
    this.ws = new WebSocket(this.url);
    
    this.ws.onopen = () => {
      console.log('WebSocket connected');
      this.retryCount = 0;
      this.currentDelay = this.retryDelay;
    };
    
    this.ws.onclose = (event) => {
      console.log('WebSocket closed:', event.code, event.reason);
      
      if (this.shouldReconnect && this.retryCount < this.maxRetries) {
        this.scheduleReconnect();
      }
    };
    
    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
    
    return this.ws;
  }
  
  scheduleReconnect() {
    this.retryCount++;
    const delay = Math.min(
      this.currentDelay,
      this.maxRetryDelay
    );
    
    console.log(`Reconnecting in ${delay}ms (attempt ${this.retryCount})`);
    
    setTimeout(() => {
      this.connect();
      this.currentDelay *= this.backoffMultiplier;
    }, delay);
  }
  
  disconnect() {
    this.shouldReconnect = false;
    if (this.ws) {
      this.ws.close();
    }
  }
}

// Usage
const reconnector = new WebSocketReconnector('ws://example.com/ws', {
  maxRetries: 10,
  retryDelay: 1000,
  maxRetryDelay: 30000,
  backoffMultiplier: 2,
});

const ws = reconnector.connect();
```

### Exponential Backoff with Jitter

```javascript
class ExponentialBackoffReconnector {
  constructor(url, options = {}) {
    this.url = url;
    this.baseDelay = options.baseDelay || 1000;
    this.maxDelay = options.maxDelay || 30000;
    this.multiplier = options.multiplier || 2;
    this.jitter = options.jitter || 0.1; // 10% jitter
    
    this.retryCount = 0;
    this.ws = null;
  }
  
  calculateDelay() {
    const exponentialDelay = Math.min(
      this.baseDelay * Math.pow(this.multiplier, this.retryCount),
      this.maxDelay
    );
    
    // Add jitter to prevent thundering herd
    const jitterAmount = exponentialDelay * this.jitter;
    const randomJitter = (Math.random() * 2 - 1) * jitterAmount;
    
    return Math.max(0, exponentialDelay + randomJitter);
  }
  
  async connect() {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(this.url);
      
      this.ws.onopen = () => {
        this.retryCount = 0;
        resolve(this.ws);
      };
      
      this.ws.onclose = () => {
        this.scheduleReconnect();
      };
      
      this.ws.onerror = reject;
    });
  }
  
  scheduleReconnect() {
    const delay = this.calculateDelay();
    this.retryCount++;
    
    console.log(`Reconnecting in ${Math.round(delay)}ms (attempt ${this.retryCount})`);
    
    setTimeout(() => {
      this.connect();
    }, delay);
  }
}
```

## Authentication and Authorization

### Token-Based Authentication

```javascript
class AuthenticatedWebSocket {
  constructor(url, token) {
    this.url = url;
    this.token = token;
    this.ws = null;
  }
  
  connect() {
    // Append token as query parameter
    const wsUrl = `${this.url}?token=${encodeURIComponent(this.token)}`;
    this.ws = new WebSocket(wsUrl);
    
    // Or send token in first message
    this.ws.onopen = () => {
      this.ws.send(JSON.stringify({
        type: 'auth',
        token: this.token,
      }));
    };
    
    return this.ws;
  }
}
```

### Server-Side Authentication Middleware

```javascript
const WebSocket = require('ws');
const jwt = require('jsonwebtoken');

const wss = new WebSocket.Server({ 
  port: 8080,
  verifyClient: async (info, cb) => {
    // Extract token from query parameter
    const url = new URL(info.req.url, `http://${info.req.headers.host}`);
    const token = url.searchParams.get('token');
    
    if (!token) {
      return cb(false, 401, 'Unauthorized');
    }
    
    try {
      const decoded = jwt.verify(token, process.env.JWT_SECRET);
      info.req.user = decoded;
      cb(true);
    } catch (error) {
      cb(false, 401, 'Invalid token');
    }
  },
});

wss.on('connection', (ws, req) => {
  const user = req.user;
  console.log(`User ${user.id} connected`);
  
  ws.on('message', (data) => {
    // Handle authenticated messages
  });
});
```

### Message-Level Authorization

```javascript
function authorizeMessage(ws, message, user) {
  const { type, payload } = message;
  
  switch (type) {
    case 'join_channel':
      // Check if user can join channel
      if (!canJoinChannel(user, payload.channelId)) {
        sendError(ws, 'Forbidden', 'Cannot join this channel');
        return false;
      }
      break;
      
    case 'send_message':
      // Check if user can send to channel
      if (!canSendToChannel(user, payload.channelId)) {
        sendError(ws, 'Forbidden', 'Cannot send to this channel');
        return false;
      }
      break;
  }
  
  return true;
}

function sendError(ws, code, message) {
  ws.send(JSON.stringify({
    type: 'error',
    code,
    message,
  }));
}
```

## Room/Channel Patterns

### Basic Room Implementation

```javascript
class RoomManager {
  constructor() {
    this.rooms = new Map(); // roomId -> Set of WebSocket connections
    this.userRooms = new Map(); // ws -> Set of roomIds
  }
  
  join(ws, roomId) {
    if (!this.rooms.has(roomId)) {
      this.rooms.set(roomId, new Set());
    }
    
    this.rooms.get(roomId).add(ws);
    
    if (!this.userRooms.has(ws)) {
      this.userRooms.set(ws, new Set());
    }
    this.userRooms.get(ws).add(roomId);
    
    // Notify room
    this.broadcastToRoom(roomId, {
      type: 'user_joined',
      userId: ws.userId,
      roomId,
    }, ws);
  }
  
  leave(ws, roomId) {
    const room = this.rooms.get(roomId);
    if (room) {
      room.delete(ws);
      if (room.size === 0) {
        this.rooms.delete(roomId);
      }
    }
    
    const userRooms = this.userRooms.get(ws);
    if (userRooms) {
      userRooms.delete(roomId);
    }
    
    // Notify room
    this.broadcastToRoom(roomId, {
      type: 'user_left',
      userId: ws.userId,
      roomId,
    });
  }
  
  leaveAll(ws) {
    const rooms = this.userRooms.get(ws);
    if (rooms) {
      for (const roomId of rooms) {
        this.leave(ws, roomId);
      }
    }
  }
  
  broadcastToRoom(roomId, message, excludeWs = null) {
    const room = this.rooms.get(roomId);
    if (!room) return;
    
    const data = JSON.stringify(message);
    
    for (const ws of room) {
      if (ws !== excludeWs && ws.readyState === WebSocket.OPEN) {
        ws.send(data);
      }
    }
  }
  
  sendToUser(ws, message) {
    if (ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(message));
    }
  }
}

// Usage
const roomManager = new RoomManager();

wss.on('connection', (ws, req) => {
  ws.userId = req.user.id;
  
  ws.on('message', (data) => {
    const message = JSON.parse(data);
    
    switch (message.type) {
      case 'join':
        roomManager.join(ws, message.roomId);
        break;
        
      case 'leave':
        roomManager.leave(ws, message.roomId);
        break;
        
      case 'message':
        roomManager.broadcastToRoom(message.roomId, {
          type: 'message',
          userId: ws.userId,
          content: message.content,
          roomId: message.roomId,
        });
        break;
    }
  });
  
  ws.on('close', () => {
    roomManager.leaveAll(ws);
  });
});
```

### Presence System

```javascript
class PresenceManager {
  constructor() {
    this.presence = new Map(); // userId -> { roomId, lastSeen }
  }
  
  update(userId, roomId) {
    this.presence.set(userId, {
      roomId,
      lastSeen: Date.now(),
    });
  }
  
  remove(userId) {
    this.presence.delete(userId);
  }
  
  getUsersInRoom(roomId) {
    const users = [];
    for (const [userId, data] of this.presence) {
      if (data.roomId === roomId) {
        users.push({ userId, ...data });
      }
    }
    return users;
  }
  
  isUserOnline(userId, timeout = 30000) {
    const presence = this.presence.get(userId);
    if (!presence) return false;
    return Date.now() - presence.lastSeen < timeout;
  }
  
  broadcastPresence(roomManager, roomId) {
    const users = this.getUsersInRoom(roomId);
    roomManager.broadcastToRoom(roomId, {
      type: 'presence',
      users,
    });
  }
}
```

## Pub/Sub Patterns

### Redis Pub/Sub

```javascript
const Redis = require('ioredis');
const WebSocket = require('ws');

const redis = new Redis();
const pub = new Redis();
const wss = new WebSocket.Server({ port: 8080 });

// Subscribe to channels
const subscriber = new Redis();
subscriber.psubscribe('room:*');

subscriber.on('pmessage', (pattern, channel, message) => {
  const roomId = channel.split(':')[1];
  const data = JSON.parse(message);
  
  // Broadcast to WebSocket clients in room
  const room = roomManager.rooms.get(roomId);
  if (room) {
    for (const ws of room) {
      if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify(data));
      }
    }
  }
});

// Publish messages
function publishToRoom(roomId, message) {
  pub.publish(`room:${roomId}`, JSON.stringify(message));
}

wss.on('connection', (ws, req) => {
  ws.on('message', (data) => {
    const message = JSON.parse(data);
    
    if (message.type === 'message') {
      // Publish to Redis for all servers
      publishToRoom(message.roomId, {
        type: 'message',
        userId: ws.userId,
        content: message.content,
      });
    }
  });
});
```

### Message Broker Integration (RabbitMQ)

```javascript
const amqp = require('amqplib');
const WebSocket = require('ws');

class WebSocketBroker {
  constructor() {
    this.connection = null;
    this.channel = null;
    this.exchanges = new Map();
  }
  
  async connect() {
    this.connection = await amqp.connect(process.env.RABBITMQ_URL);
    this.channel = await this.connection.createChannel();
  }
  
  async declareExchange(exchangeName, type = 'topic') {
    await this.channel.assertExchange(exchangeName, type, { durable: false });
    this.exchanges.set(exchangeName, exchangeName);
  }
  
  async publish(exchangeName, routingKey, message) {
    const exchange = this.exchanges.get(exchangeName);
    if (!exchange) {
      throw new Error(`Exchange ${exchangeName} not found`);
    }
    
    this.channel.publish(
      exchange,
      routingKey,
      Buffer.from(JSON.stringify(message))
    );
  }
  
  async subscribe(exchangeName, routingKey, callback) {
    const exchange = this.exchanges.get(exchangeName);
    if (!exchange) {
      throw new Error(`Exchange ${exchangeName} not found`);
    }
    
    const queue = await this.channel.assertQueue('', { exclusive: true });
    await this.channel.bindQueue(queue.queue, exchange, routingKey);
    
    await this.channel.consume(queue.queue, (msg) => {
      if (msg) {
        const message = JSON.parse(msg.content.toString());
        callback(message);
        this.channel.ack(msg);
      }
    });
  }
}

// Usage
const broker = new WebSocketBroker();
await broker.connect();
await broker.declareExchange('websocket');

// Subscribe to room messages
await broker.subscribe('websocket', 'room.*', (message) => {
  roomManager.broadcastToRoom(message.roomId, message);
});

// Publish messages
broker.publish('websocket', `room.${roomId}`, {
  type: 'message',
  userId: ws.userId,
  content: message.content,
  roomId,
});
```

## Broadcasting Strategies

### Broadcast to All Clients

```javascript
function broadcastToAll(message) {
  const data = JSON.stringify(message);
  
  wss.clients.forEach((client) => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(data);
    }
  });
}
```

### Selective Broadcasting

```javascript
function broadcastToUsers(userIds, message) {
  const data = JSON.stringify(message);
  
  wss.clients.forEach((client) => {
    if (client.readyState === WebSocket.OPEN && userIds.includes(client.userId)) {
      client.send(data);
    }
  });
}

function broadcastToRoles(roles, message) {
  const data = JSON.stringify(message);
  
  wss.clients.forEach((client) => {
    if (client.readyState === WebSocket.OPEN && 
        client.roles && client.roles.some(r => roles.includes(r))) {
      client.send(data);
    }
  });
}
```

### Fanout with Filtering

```javascript
class MessageRouter {
  constructor() {
    this.subscriptions = new Map(); // clientId -> Set of topics
    this.topicSubscribers = new Map(); // topic -> Set of clientIds
  }
  
  subscribe(clientId, topic) {
    if (!this.subscriptions.has(clientId)) {
      this.subscriptions.set(clientId, new Set());
    }
    this.subscriptions.get(clientId).add(topic);
    
    if (!this.topicSubscribers.has(topic)) {
      this.topicSubscribers.set(topic, new Set());
    }
    this.topicSubscribers.get(topic).add(clientId);
  }
  
  unsubscribe(clientId, topic) {
    const subscriptions = this.subscriptions.get(clientId);
    if (subscriptions) {
      subscriptions.delete(topic);
    }
    
    const subscribers = this.topicSubscribers.get(topic);
    if (subscribers) {
      subscribers.delete(clientId);
    }
  }
  
  publish(topic, message) {
    const subscribers = this.topicSubscribers.get(topic);
    if (!subscribers) return;
    
    for (const clientId of subscribers) {
      const ws = getClientById(clientId);
      if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify(message));
      }
    }
  }
}
```

## Scaling WebSockets

### Sticky Sessions

```nginx
# Nginx configuration for sticky sessions
upstream websocket_backend {
    ip_hash;  # Sticky sessions based on client IP
    server ws1.example.com:8080;
    server ws2.example.com:8080;
    server ws3.example.com:8080;
}

server {
    listen 80;
    server_name ws.example.com;
    
    location /ws {
        proxy_pass http://websocket_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 86400;
    }
}
```

### Redis Adapter for Horizontal Scaling

```javascript
const Redis = require('ioredis');
const WebSocket = require('ws');

class RedisAdapter {
  constructor() {
    this.pub = new Redis();
    this.sub = new Redis();
    this.rooms = new Map(); // Local rooms
  }
  
  async init() {
    // Subscribe to all room messages
    await this.sub.psubscribe('room:*');
    
    this.sub.on('pmessage', (pattern, channel, message) => {
      const roomId = channel.split(':')[1];
      const data = JSON.parse(message);
      
      // Broadcast to local clients only
      this.broadcastToLocal(roomId, data);
    });
  }
  
  join(ws, roomId) {
    if (!this.rooms.has(roomId)) {
      this.rooms.set(roomId, new Set());
    }
    this.rooms.get(roomId).add(ws);
    
    // Notify other servers
    this.pub.publish('room:*', JSON.stringify({
      type: 'user_joined',
      roomId,
      userId: ws.userId,
      serverId: process.env.SERVER_ID,
    }));
  }
  
  leave(ws, roomId) {
    const room = this.rooms.get(roomId);
    if (room) {
      room.delete(ws);
      if (room.size === 0) {
        this.rooms.delete(roomId);
      }
    }
    
    // Notify other servers
    this.pub.publish('room:*', JSON.stringify({
      type: 'user_left',
      roomId,
      userId: ws.userId,
      serverId: process.env.SERVER_ID,
    }));
  }
  
  broadcastToRoom(roomId, message) {
    // Publish to Redis for all servers
    this.pub.publish(`room:${roomId}`, JSON.stringify({
      ...message,
      serverId: process.env.SERVER_ID,
    }));
  }
  
  broadcastToLocal(roomId, message) {
    // Skip messages from this server
    if (message.serverId === process.env.SERVER_ID) {
      return;
    }
    
    const room = this.rooms.get(roomId);
    if (!room) return;
    
    const data = JSON.stringify(message);
    for (const ws of room) {
      if (ws.readyState === WebSocket.OPEN) {
        ws.send(data);
      }
    }
  }
}
```

### Message Broker for Scaling

```javascript
const amqp = require('amqplib');

class RabbitMQAdapter {
  constructor() {
    this.connection = null;
    this.channel = null;
    this.replyQueue = null;
  }
  
  async connect() {
    this.connection = await amqp.connect(process.env.RABBITMQ_URL);
    this.channel = await this.connection.createChannel();
    
    // Create fanout exchange for broadcasting
    await this.channel.assertExchange('websocket.broadcast', 'fanout', {
      durable: false,
    });
    
    // Create topic exchange for routing
    await this.channel.assertExchange('websocket.routing', 'topic', {
      durable: false,
    });
  }
  
  async broadcast(message) {
    this.channel.publish(
      'websocket.broadcast',
      '',
      Buffer.from(JSON.stringify(message))
    );
  }
  
  async publish(routingKey, message) {
    this.channel.publish(
      'websocket.routing',
      routingKey,
      Buffer.from(JSON.stringify(message))
    );
  }
  
  async subscribe(exchange, routingKey, callback) {
    const queue = await this.channel.assertQueue('', { exclusive: true });
    await this.channel.bindQueue(queue.queue, exchange, routingKey);
    
    await this.channel.consume(queue.queue, (msg) => {
      if (msg) {
        const message = JSON.parse(msg.content.toString());
        callback(message);
        this.channel.ack(msg);
      }
    });
  }
}
```

## WebSocket Libraries

### Socket.IO

```javascript
const express = require('express');
const { createServer } = 'http';
const { Server } = require('socket.io');

const app = express();
const httpServer = createServer(app);
const io = new Server(httpServer, {
  cors: {
    origin: '*',
  },
});

io.on('connection', (socket) => {
  console.log('Client connected:', socket.id);
  
  // Join room
  socket.on('join', (roomId) => {
    socket.join(roomId);
    socket.to(roomId).emit('user_joined', { userId: socket.id });
  });
  
  // Leave room
  socket.on('leave', (roomId) => {
    socket.leave(roomId);
    socket.to(roomId).emit('user_left', { userId: socket.id });
  });
  
  // Send message to room
  socket.on('message', (data) => {
    io.to(data.roomId).emit('message', {
      userId: socket.id,
      content: data.content,
    });
  });
  
  socket.on('disconnect', () => {
    console.log('Client disconnected:', socket.id);
  });
});

httpServer.listen(3000);
```

### ws (Node.js)

```javascript
const WebSocket = require('ws');

const wss = new WebSocket.Server({ port: 8080 });

wss.on('connection', (ws, req) => {
  console.log('New connection');
  
  ws.on('message', (message) => {
    console.log('Received:', message.toString());
    
    // Echo back
    ws.send(`Echo: ${message}`);
  });
  
  ws.on('close', () => {
    console.log('Connection closed');
  });
  
  ws.on('error', (error) => {
    console.error('WebSocket error:', error);
  });
});
```

### WebSocket API (Browser)

```javascript
// Basic connection
const ws = new WebSocket('ws://localhost:8080');

ws.onopen = () => {
  console.log('Connected');
  ws.send('Hello, server!');
};

ws.onmessage = (event) => {
  console.log('Received:', event.data);
};

ws.onclose = (event) => {
  console.log('Disconnected:', event.code, event.reason);
};

ws.onerror = (error) => {
  console.error('Error:', error);
};

// With subprotocol
const ws = new WebSocket('ws://localhost:8080', ['chat', 'superchat']);

// With custom headers (not supported in browser API)
// Use server-side WebSocket library for custom headers
```

## Error Handling and Graceful Degradation

### Error Handling

```javascript
class RobustWebSocket {
  constructor(url, options = {}) {
    this.url = url;
    this.options = options;
    this.ws = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = options.maxReconnectAttempts || 10;
    this.reconnectDelay = options.reconnectDelay || 1000;
  }
  
  connect() {
    try {
      this.ws = new WebSocket(this.url);
      this.setupEventHandlers();
      return this.ws;
    } catch (error) {
      console.error('Failed to create WebSocket:', error);
      this.handleConnectionError(error);
    }
  }
  
  setupEventHandlers() {
    this.ws.onopen = () => {
      console.log('WebSocket connected');
      this.reconnectAttempts = 0;
      if (this.options.onOpen) {
        this.options.onOpen();
      }
    };
    
    this.ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (this.options.onMessage) {
          this.options.onMessage(data);
        }
      } catch (error) {
        console.error('Failed to parse message:', error);
      }
    };
    
    this.ws.onclose = (event) => {
      console.log('WebSocket closed:', event.code, event.reason);
      if (this.options.onClose) {
        this.options.onClose(event);
      }
      this.scheduleReconnect();
    };
    
    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      if (this.options.onError) {
        this.options.onError(error);
      }
    };
  }
  
  scheduleReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
      
      console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`);
      
      setTimeout(() => {
        this.connect();
      }, delay);
    } else {
      console.error('Max reconnect attempts reached');
      if (this.options.onMaxReconnectReached) {
        this.options.onMaxReconnectReached();
      }
    }
  }
  
  send(data) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    } else {
      console.warn('WebSocket not connected, message not sent');
    }
  }
  
  close() {
    if (this.ws) {
      this.ws.close();
    }
  }
}
```

### Graceful Degradation

```javascript
class DegradableWebSocket {
  constructor(url, fallbackUrl) {
    this.url = url;
    this.fallbackUrl = fallbackUrl;
    this.ws = null;
    this.mode = 'websocket'; // 'websocket' or 'polling'
    this.pollingInterval = null;
  }
  
  async connect() {
    try {
      this.ws = await this.createWebSocket();
      this.mode = 'websocket';
      return this.ws;
    } catch (error) {
      console.warn('WebSocket failed, falling back to polling');
      this.mode = 'polling';
      return this.startPolling();
    }
  }
  
  createWebSocket() {
    return new Promise((resolve, reject) => {
      const ws = new WebSocket(this.url);
      
      const timeout = setTimeout(() => {
        ws.close();
        reject(new Error('WebSocket connection timeout'));
      }, 5000);
      
      ws.onopen = () => {
        clearTimeout(timeout);
        resolve(ws);
      };
      
      ws.onerror = () => {
        clearTimeout(timeout);
        reject(new Error('WebSocket connection failed'));
      };
    });
  }
  
  startPolling() {
    // Return a mock WebSocket-like object
    const mockWs = {
      readyState: 1, // OPEN
      send: (data) => {
        fetch(this.fallbackUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: data,
        });
      },
      close: () => {
        if (this.pollingInterval) {
          clearInterval(this.pollingInterval);
        }
      },
      onmessage: null,
      onopen: null,
      onclose: null,
    };
    
    // Start polling for messages
    this.pollingInterval = setInterval(async () => {
      try {
        const response = await fetch(this.fallbackUrl);
        const messages = await response.json();
        
        if (mockWs.onmessage) {
          messages.forEach(msg => {
            mockWs.onmessage({ data: JSON.stringify(msg) });
          });
        }
      } catch (error) {
        console.error('Polling error:', error);
      }
    }, 1000);
    
    if (mockWs.onopen) {
      setTimeout(() => mockWs.onopen(), 0);
    }
    
    return mockWs;
  }
}
```

## Rate Limiting and Throttling

### Rate Limiting

```javascript
class RateLimiter {
  constructor(options = {}) {
    this.maxRequests = options.maxRequests || 100;
    this.windowMs = options.windowMs || 60000; // 1 minute
    this.clients = new Map();
  }
  
  check(clientId) {
    const now = Date.now();
    let clientData = this.clients.get(clientId);
    
    if (!clientData) {
      clientData = { count: 0, resetTime: now + this.windowMs };
      this.clients.set(clientId, clientData);
    }
    
    // Reset if window expired
    if (now > clientData.resetTime) {
      clientData.count = 0;
      clientData.resetTime = now + this.windowMs;
    }
    
    clientData.count++;
    
    return {
      allowed: clientData.count <= this.maxRequests,
      remaining: Math.max(0, this.maxRequests - clientData.count),
      resetTime: clientData.resetTime,
    };
  }
}

// Usage
const rateLimiter = new RateLimiter({ maxRequests: 100, windowMs: 60000 });

wss.on('connection', (ws, req) => {
  const clientId = getClientId(req);
  
  ws.on('message', (data) => {
    const result = rateLimiter.check(clientId);
    
    if (!result.allowed) {
      ws.send(JSON.stringify({
        type: 'error',
        code: 'RATE_LIMIT_EXCEEDED',
        message: 'Too many requests',
        retryAfter: Math.ceil((result.resetTime - Date.now()) / 1000),
      }));
      return;
    }
    
    // Process message
  });
});
```

### Throttling

```javascript
class Throttler {
  constructor(options = {}) {
    this.minInterval = options.minInterval || 100; // 100ms between messages
    this.lastSent = new Map();
  }
  
  shouldThrottle(clientId) {
    const now = Date.now();
    const lastSent = this.lastSent.get(clientId) || 0;
    
    if (now - lastSent < this.minInterval) {
      return true;
    }
    
    this.lastSent.set(clientId, now);
    return false;
  }
}

// Usage
const throttler = new Throttler({ minInterval: 100 });

wss.on('connection', (ws, req) => {
  const clientId = getClientId(req);
  
  ws.on('message', (data) => {
    if (throttler.shouldThrottle(clientId)) {
      // Drop or queue message
      return;
    }
    
    // Process message
  });
});
```

## Security Considerations

### WSS (WebSocket Secure)

Always use `wss://` instead of `ws://` in production:

```javascript
// Secure WebSocket connection
const wss = new WebSocket.Server({
  port: 443,
  ssl: {
    key: fs.readFileSync('server.key'),
    cert: fs.readFileSync('server.crt'),
    ca: fs.readFileSync('ca.crt'),
  },
});
```

### Origin Validation

```javascript
const wss = new WebSocket.Server({
  port: 8080,
  verifyClient: (info, cb) => {
    const origin = info.origin;
    const allowedOrigins = ['https://example.com', 'https://app.example.com'];
    
    if (allowedOrigins.includes(origin)) {
      cb(true);
    } else {
      console.log('Blocked connection from origin:', origin);
      cb(false, 403, 'Forbidden');
    }
  },
});
```

### Input Validation

```javascript
function validateMessage(message) {
  if (!message || typeof message !== 'object') {
    return false;
  }
  
  if (!message.type || typeof message.type !== 'string') {
    return false;
  }
  
  // Validate based on message type
  switch (message.type) {
    case 'message':
      return message.content && typeof message.content === 'string' &&
             message.content.length <= 1000;
      
    case 'join':
      return message.roomId && typeof message.roomId === 'string';
      
    default:
      return false;
  }
}

ws.on('message', (data) => {
  try {
    const message = JSON.parse(data);
    
    if (!validateMessage(message)) {
      ws.send(JSON.stringify({
        type: 'error',
        code: 'INVALID_MESSAGE',
        message: 'Invalid message format',
      }));
      return;
    }
    
    // Process valid message
  } catch (error) {
    ws.send(JSON.stringify({
      type: 'error',
      code: 'PARSE_ERROR',
      message: 'Failed to parse message',
    }));
  }
});
```

### CSRF Protection

```javascript
const wss = new WebSocket.Server({
  port: 8080,
  verifyClient: (info, cb) => {
    // Check for CSRF token in query parameter
    const url = new URL(info.req.url, `http://${info.req.headers.host}`);
    const csrfToken = url.searchParams.get('csrf_token');
    
    if (validateCSRFToken(csrfToken, info.req)) {
      cb(true);
    } else {
      cb(false, 403, 'Invalid CSRF token');
    }
  },
});

function validateCSRFToken(token, req) {
  // Validate token against session
  const sessionToken = getSessionCSRFToken(req);
  return token && token === sessionToken;
}
```

## Testing WebSocket Applications

### Unit Testing

```javascript
const WebSocket = require('ws');

describe('RoomManager', () => {
  let roomManager;
  let client1, client2, client3;
  
  beforeEach(() => {
    roomManager = new RoomManager();
    
    // Create mock WebSocket clients
    client1 = createMockWebSocket('user1');
    client2 = createMockWebSocket('user2');
    client3 = createMockWebSocket('user3');
  });
  
  it('should join users to room', () => {
    roomManager.join(client1, 'room1');
    roomManager.join(client2, 'room1');
    
    const room = roomManager.rooms.get('room1');
    expect(room.size).toBe(2);
    expect(room.has(client1)).toBe(true);
    expect(room.has(client2)).toBe(true);
  });
  
  it('should broadcast to room', () => {
    roomManager.join(client1, 'room1');
    roomManager.join(client2, 'room1');
    roomManager.join(client3, 'room2');
    
    const message = { type: 'test', content: 'Hello' };
    roomManager.broadcastToRoom('room1', message);
    
    expect(client1.sentMessages.length).toBe(1);
    expect(client2.sentMessages.length).toBe(1);
    expect(client3.sentMessages.length).toBe(0);
  });
});

function createMockWebSocket(userId) {
  const ws = {
    userId,
    sentMessages: [],
    readyState: 1, // OPEN
    send: function(data) {
      this.sentMessages.push(JSON.parse(data));
    },
  };
  return ws;
}
```

### Integration Testing

```javascript
const WebSocket = require('ws');

describe('WebSocket Server Integration', () => {
  let server;
  let client;
  
  beforeAll((done) => {
    server = createWebSocketServer(8081);
    done();
  });
  
  afterAll((done) => {
    server.close(done);
  });
  
  beforeEach((done) => {
    client = new WebSocket('ws://localhost:8081');
    client.on('open', done);
  });
  
  afterEach(() => {
    client.close();
  });
  
  it('should receive welcome message', (done) => {
    client.on('message', (data) => {
      const message = JSON.parse(data);
      expect(message.type).toBe('welcome');
      done();
    });
  });
  
  it('should handle join room', (done) => {
    const roomId = 'test-room';
    
    client.on('message', (data) => {
      const message = JSON.parse(data);
      
      if (message.type === 'user_joined') {
        expect(message.roomId).toBe(roomId);
        done();
      }
    });
    
    client.send(JSON.stringify({
      type: 'join',
      roomId,
    }));
  });
});
```

## Monitoring and Debugging

### Logging

```javascript
class WebSocketLogger {
  constructor(ws, userId) {
    this.ws = ws;
    this.userId = userId;
    this.messages = [];
    this.setupLogging();
  }
  
  setupLogging() {
    this.ws.on('message', (data) => {
      const message = JSON.parse(data);
      this.log('received', message);
    });
    
    const originalSend = this.ws.send.bind(this.ws);
    this.ws.send = (data) => {
      const message = JSON.parse(data);
      this.log('sent', message);
      return originalSend(data);
    };
    
    this.ws.on('close', (event) => {
      this.log('close', { code: event.code, reason: event.reason });
    });
    
    this.ws.onerror = (error) => {
      this.log('error', { message: error.message });
    };
  }
  
  log(direction, data) {
    const entry = {
      timestamp: new Date().toISOString(),
      userId: this.userId,
      direction,
      data,
    };
    
    this.messages.push(entry);
    console.log(JSON.stringify(entry));
    
    // Send to monitoring service
    sendToMonitoring(entry);
  }
}
```

### Metrics Collection

```javascript
class WebSocketMetrics {
  constructor() {
    this.connections = 0;
    this.messagesSent = 0;
    this.messagesReceived = 0;
    this.errors = 0;
    this.roomSizes = new Map();
  }
  
  recordConnection() {
    this.connections++;
  }
  
  recordDisconnection() {
    this.connections--;
  }
  
  recordMessageSent() {
    this.messagesSent++;
  }
  
  recordMessageReceived() {
    this.messagesReceived++;
  }
  
  recordError() {
    this.errors++;
  }
  
  recordRoomJoin(roomId) {
    const size = this.roomSizes.get(roomId) || 0;
    this.roomSizes.set(roomId, size + 1);
  }
  
  recordRoomLeave(roomId) {
    const size = this.roomSizes.get(roomId) || 0;
    if (size > 0) {
      this.roomSizes.set(roomId, size - 1);
    }
  }
  
  getMetrics() {
    return {
      connections: this.connections,
      messagesSent: this.messagesSent,
      messagesReceived: this.messagesReceived,
      errors: this.errors,
      roomSizes: Object.fromEntries(this.roomSizes),
    };
  }
}
```

## Best Practices

1. **Connection Management**
   - Implement proper reconnection with exponential backoff
   - Use heartbeat/ping-pong to detect dead connections
   - Clean up resources on disconnect
   - Handle connection timeouts gracefully

2. **Security**
   - Always use WSS in production
   - Implement proper authentication
   - Validate origin headers
   - Sanitize and validate all inputs

3. **Performance**
   - Use binary data for large payloads
   - Implement message batching when possible
   - Use connection pooling for multiple connections
   - Consider message compression

4. **Scalability**
   - Use Redis or message brokers for horizontal scaling
   - Implement sticky sessions with load balancers
   - Design stateless services where possible
   - Use proper partitioning strategies

5. **Error Handling**
   - Implement comprehensive error handling
   - Provide meaningful error messages
   - Log errors for debugging
   - Implement graceful degradation

6. **Monitoring**
   - Track connection metrics
   - Monitor message throughput
   - Alert on error rates
   - Log important events

## Related Skills

- `34-real-time-features/websocket-integration`
- `08-messaging-queue/redis-pubsub`
