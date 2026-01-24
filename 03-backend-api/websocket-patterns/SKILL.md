---
name: WebSocket Patterns
description: Advanced WebSocket patterns for real-time bidirectional communication in web applications.
---

# WebSocket Patterns

## Overview

WebSocket is a communication protocol that provides full-duplex communication channels over a single TCP connection. It enables real-time, event-driven communication between clients and servers, making it ideal for applications requiring instant updates such as chat applications, live dashboards, and collaborative tools.

## Prerequisites

- Understanding of HTTP protocol and REST APIs
- Knowledge of JavaScript/Node.js or equivalent backend language
- Basic understanding of TCP/IP networking
- Familiarity with asynchronous programming patterns

## Key Concepts

### WebSocket Fundamentals

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

### Connection Lifecycle

#### Handshake

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

#### Connection States

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

## Implementation Guide

### Basic WebSocket Server (Node.js)

```javascript
const WebSocket = require('ws');
const http = require('http');

const server = http.createServer();
const wss = new WebSocket.Server({ server });

wss.on('connection', (ws, req) => {
  console.log('New client connected');

  // Send welcome message
  ws.send(JSON.stringify({
    type: 'welcome',
    message: 'Connected to WebSocket server',
  }));

  // Handle incoming messages
  ws.on('message', (data) => {
    try {
      const message = JSON.parse(data);
      handleMessage(ws, message);
    } catch (error) {
      ws.send(JSON.stringify({
        type: 'error',
        message: 'Invalid JSON format',
      }));
    }
  });

  // Handle disconnection
  ws.on('close', () => {
    console.log('Client disconnected');
  });

  // Handle errors
  ws.onerror = (error) => {
    console.error('WebSocket error:', error);
  };
});

function handleMessage(ws, message) {
  switch (message.type) {
    case 'echo':
      ws.send(JSON.stringify({
        type: 'echo',
        data: message.data,
      }));
      break;

    case 'broadcast':
      wss.clients.forEach((client) => {
        if (client.readyState === WebSocket.OPEN) {
          client.send(JSON.stringify({
            type: 'broadcast',
            data: message.data,
          }));
        }
      });
      break;

    default:
      ws.send(JSON.stringify({
        type: 'error',
        message: 'Unknown message type',
      }));
  }
}

server.listen(8080, () => {
  console.log('WebSocket server running on port 8080');
});
```

### Basic WebSocket Client

```javascript
class WebSocketClient {
  constructor(url) {
    this.url = url;
    this.ws = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectInterval = 1000;
    this.messageHandlers = {};
  }

  connect() {
    this.ws = new WebSocket(this.url);

    this.ws.onopen = () => {
      console.log('Connected to WebSocket server');
      this.reconnectAttempts = 0;
    };

    this.ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        this.handleMessage(message);
      } catch (error) {
        console.error('Failed to parse message:', error);
      }
    };

    this.ws.onclose = () => {
      console.log('Disconnected from server');
      this.attemptReconnect();
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }

  handleMessage(message) {
    const handler = this.messageHandlers[message.type];
    if (handler) {
      handler(message);
    } else {
      console.warn('No handler for message type:', message.type);
    }
  }

  on(type, handler) {
    this.messageHandlers[type] = handler;
  }

  send(type, data) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ type, data }));
    } else {
      console.warn('WebSocket is not connected');
    }
  }

  attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = this.reconnectInterval * Math.pow(2, this.reconnectAttempts - 1);
      console.log(`Reconnecting in ${delay}ms...`);
      setTimeout(() => this.connect(), delay);
    } else {
      console.error('Max reconnection attempts reached');
    }
  }

  close() {
    if (this.ws) {
      this.ws.close();
    }
  }
}

// Usage
const client = new WebSocketClient('ws://localhost:8080');
client.connect();

client.on('welcome', (message) => {
  console.log('Welcome:', message.message);
});

client.on('broadcast', (message) => {
  console.log('Broadcast:', message.data);
});

client.send('echo', { text: 'Hello, Server!' });
```

### Room-Based Messaging

```javascript
class RoomManager {
  constructor() {
    this.rooms = new Map();
  }

  join(ws, roomId, userId) {
    if (!this.rooms.has(roomId)) {
      this.rooms.set(roomId, new Map());
    }

    const room = this.rooms.get(roomId);
    room.set(ws, { userId, joinedAt: Date.now() });

    // Notify room
    this.broadcastToRoom(roomId, {
      type: 'user_joined',
      roomId,
      userId,
    }, ws);

    // Send current room state to new user
    const users = Array.from(room.values()).map(u => u.userId);
    ws.send(JSON.stringify({
      type: 'room_joined',
      roomId,
      users,
    }));
  }

  leave(ws) {
    for (const [roomId, room] of this.rooms) {
      if (room.has(ws)) {
        const { userId } = room.get(ws);
        room.delete(ws);

        // Notify room
        this.broadcastToRoom(roomId, {
          type: 'user_left',
          roomId,
          userId,
        });

        // Clean up empty rooms
        if (room.size === 0) {
          this.rooms.delete(roomId);
        }
        break;
      }
    }
  }

  broadcastToRoom(roomId, message, excludeWs = null) {
    const room = this.rooms.get(roomId);
    if (!room) return;

    room.forEach((_, ws) => {
      if (ws !== excludeWs && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify(message));
      }
    });
  }

  getRoomInfo(roomId) {
    const room = this.rooms.get(roomId);
    if (!room) return null;

    return {
      roomId,
      userCount: room.size,
      users: Array.from(room.values()).map(u => u.userId),
    };
  }
}

// Integration with WebSocket server
const roomManager = new RoomManager();

wss.on('connection', (ws, req) => {
  const userId = getUserIdFromRequest(req);

  ws.on('message', (data) => {
    const message = JSON.parse(data);

    switch (message.type) {
      case 'join_room':
        roomManager.join(ws, message.roomId, userId);
        break;

      case 'leave_room':
        roomManager.leave(ws);
        break;

      case 'room_message':
        roomManager.broadcastToRoom(message.roomId, {
          type: 'room_message',
          roomId: message.roomId,
          userId,
          content: message.content,
        });
        break;

      case 'get_room_info':
        const info = roomManager.getRoomInfo(message.roomId);
        ws.send(JSON.stringify({
          type: 'room_info',
          ...info,
        }));
        break;
    }
  });

  ws.on('close', () => {
    roomManager.leave(ws);
  });
});

function getUserIdFromRequest(req) {
  // Extract user ID from session, token, or query parameter
  const url = new URL(req.url, `http://${req.headers.host}`);
  return url.searchParams.get('userId') || 'anonymous';
}
```

### Heartbeat/Ping-Pong

```javascript
class HeartbeatManager {
  constructor(wss, options = {}) {
    this.wss = wss;
    this.interval = options.interval || 30000; // 30 seconds
    this.timeout = options.timeout || 10000; // 10 seconds
    this.clients = new Map();
    this.startHeartbeat();
  }

  startHeartbeat() {
    setInterval(() => {
      this.wss.clients.forEach((ws) => {
        if (ws.readyState === WebSocket.OPEN) {
          // Send ping
          const pingId = Date.now();
          ws.send(JSON.stringify({
            type: 'ping',
            id: pingId,
          }));

          // Set timeout for pong response
          const timeoutId = setTimeout(() => {
            console.log('Client did not respond to ping, closing connection');
            ws.terminate();
          }, this.timeout);

          this.clients.set(ws, { pingId, timeoutId });
        }
      });
    }, this.interval);
  }

  handlePong(ws, pongId) {
    const clientData = this.clients.get(ws);
    if (clientData && clientData.pingId === pongId) {
      clearTimeout(clientData.timeoutId);
      this.clients.set(ws, { pingId: null, timeoutId: null });
    }
  }

  cleanup(ws) {
    const clientData = this.clients.get(ws);
    if (clientData && clientData.timeoutId) {
      clearTimeout(clientData.timeoutId);
    }
    this.clients.delete(ws);
  }
}

// Usage
const heartbeatManager = new HeartbeatManager(wss, {
  interval: 30000,
  timeout: 10000,
});

wss.on('connection', (ws) => {
  ws.on('message', (data) => {
    const message = JSON.parse(data);
    if (message.type === 'pong') {
      heartbeatManager.handlePong(ws, message.id);
    }
  });

  ws.on('close', () => {
    heartbeatManager.cleanup(ws);
  });
});
```

### Message Queue and Acknowledgment

```javascript
class MessageQueue {
  constructor() {
    this.queues = new Map();
    this.pendingAcks = new Map();
  }

  enqueue(ws, message) {
    const clientId = getClientId(ws);
    if (!this.queues.has(clientId)) {
      this.queues.set(clientId, []);
    }

    const queue = this.queues.get(clientId);
    const messageId = generateMessageId();

    const queuedMessage = {
      id: messageId,
      message,
      timestamp: Date.now(),
      retries: 0,
    };

    queue.push(queuedMessage);
    this.sendQueuedMessage(ws, queuedMessage);

    return messageId;
  }

  sendQueuedMessage(ws, queuedMessage) {
    const payload = {
      ...queuedMessage.message,
      _id: queuedMessage.id,
      _ack: true,
    };

    ws.send(JSON.stringify(payload));

    // Set timeout for acknowledgment
    const timeoutId = setTimeout(() => {
      this.retryMessage(ws, queuedMessage);
    }, 5000);

    this.pendingAcks.set(queuedMessage.id, { ws, timeoutId });
  }

  acknowledge(messageId) {
    const pending = this.pendingAcks.get(messageId);
    if (pending) {
      clearTimeout(pending.timeoutId);
      this.pendingAcks.delete(messageId);

      // Remove from queue
      const clientId = getClientId(pending.ws);
      const queue = this.queues.get(clientId);
      if (queue) {
        const index = queue.findIndex(m => m.id === messageId);
        if (index !== -1) {
          queue.splice(index, 1);
        }
      }
    }
  }

  retryMessage(ws, queuedMessage) {
    queuedMessage.retries++;

    if (queuedMessage.retries >= 3) {
      console.log('Max retries reached for message:', queuedMessage.id);
      this.acknowledge(queuedMessage.id);
      return;
    }

    console.log(`Retrying message ${queuedMessage.id}, attempt ${queuedMessage.retries}`);
    this.sendQueuedMessage(ws, queuedMessage);
  }
}

// Usage
const messageQueue = new MessageQueue();

wss.on('connection', (ws) => {
  ws.on('message', (data) => {
    const message = JSON.parse(data);

    if (message._ack) {
      messageQueue.acknowledge(message._id);
    } else {
      // Process regular message
      const messageId = messageQueue.enqueue(ws, {
        type: 'response',
        data: message.data,
      });
    }
  });
});

function generateMessageId() {
  return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}

function getClientId(ws) {
  return ws._socket.remoteAddress;
}
```

### Reconnection Strategy

```javascript
class ReconnectionManager {
  constructor(url, options = {}) {
    this.url = url;
    this.ws = null;
    this.shouldReconnect = true;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = options.maxReconnectAttempts || Infinity;
    this.initialReconnectDelay = options.initialReconnectDelay || 1000;
    this.maxReconnectDelay = options.maxReconnectDelay || 30000;
    this.reconnectDelay = this.initialReconnectDelay;
    this.messageQueue = [];
  }

  connect() {
    this.ws = new WebSocket(this.url);

    this.ws.onopen = () => {
      console.log('Connected');
      this.reconnectAttempts = 0;
      this.reconnectDelay = this.initialReconnectDelay;
      this.flushMessageQueue();
    };

    this.ws.onclose = (event) => {
      console.log('Disconnected:', event.code, event.reason);
      if (this.shouldReconnect) {
        this.scheduleReconnect();
      }
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    this.ws.onmessage = (event) => {
      this.handleMessage(event.data);
    };
  }

  scheduleReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('Max reconnection attempts reached');
      return;
    }

    this.reconnectAttempts++;
    const delay = Math.min(
      this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1),
      this.maxReconnectDelay
    );

    console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`);
    setTimeout(() => this.connect(), delay);
  }

  send(data) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(data);
    } else {
      console.log('Queueing message (not connected)');
      this.messageQueue.push(data);
    }
  }

  flushMessageQueue() {
    while (this.messageQueue.length > 0) {
      const message = this.messageQueue.shift();
      this.ws.send(message);
    }
  }

  disconnect() {
    this.shouldReconnect = false;
    if (this.ws) {
      this.ws.close();
    }
  }
}

// Usage
const reconnectionManager = new ReconnectionManager('ws://localhost:8080', {
  maxReconnectAttempts: 10,
  initialReconnectDelay: 1000,
  maxReconnectDelay: 30000,
});

reconnectionManager.connect();

// Send messages even when disconnected
reconnectionManager.send(JSON.stringify({ type: 'test', data: 'hello' }));
```

### Rate Limiting

```javascript
class Throttler {
  constructor(options = {}) {
    this.minInterval = options.minInterval || 100;
    this.lastSent = new Map();
  }

  shouldThrottle(clientId) {
    const now = Date.now();
    const lastSent = this.lastSent.get(clientId);

    if (!lastSent) {
      this.lastSent.set(clientId, now);
      return false;
    }

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

## Testing

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

- [`34-real-time-features/websocket-integration`](34-real-time-features/websocket-integration/SKILL.md)
- [`08-messaging-queue/redis-pubsub`](08-messaging-queue/redis-pubsub/SKILL.md)
- [`03-backend-api/express-rest`](03-backend-api/express-rest/SKILL.md)
- [`03-backend-api/middleware`](03-backend-api/middleware/SKILL.md)
