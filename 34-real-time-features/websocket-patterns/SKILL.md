---
name: WebSocket Patterns
description: Implementing full-duplex communication between client and server using WebSockets, Socket.IO, scaling strategies, and production patterns for real-time applications.
---

# WebSocket Patterns

> **Current Level:** Intermediate  
> **Domain:** Real-time / Backend

---

## Overview

WebSockets enable full-duplex communication between client and server. This guide covers Socket.IO implementation, scaling, and production patterns for building real-time applications like chat, notifications, live updates, and collaborative features.

---

## Core Concepts

### WebSocket Protocol

```
Client                    Server
  |                          |
  |--- HTTP Upgrade -------->|
  |<-- 101 Switching --------|
  |                          |
  |<====== WebSocket =======>|
  |                          |
```

**Features:**
- Full-duplex communication
- Low latency
- Persistent connection
- Binary and text data

## Socket.IO Server Setup

```typescript
// server.ts
import express from 'express';
import { createServer } from 'http';
import { Server } from 'socket.io';
import { createAdapter } from '@socket.io/redis-adapter';
import { createClient } from 'redis';

const app = express();
const httpServer = createServer(app);

const io = new Server(httpServer, {
  cors: {
    origin: process.env.CLIENT_URL,
    credentials: true
  },
  pingTimeout: 60000,
  pingInterval: 25000
});

// Redis adapter for scaling
const pubClient = createClient({ url: process.env.REDIS_URL });
const subClient = pubClient.duplicate();

Promise.all([pubClient.connect(), subClient.connect()]).then(() => {
  io.adapter(createAdapter(pubClient, subClient));
});

// Middleware
io.use(async (socket, next) => {
  try {
    const token = socket.handshake.auth.token;
    const user = await verifyToken(token);
    socket.data.user = user;
    next();
  } catch (error) {
    next(new Error('Authentication failed'));
  }
});

// Connection handler
io.on('connection', (socket) => {
  console.log(`User connected: ${socket.data.user.id}`);

  // Join user's personal room
  socket.join(`user:${socket.data.user.id}`);

  // Handle events
  socket.on('message', handleMessage);
  socket.on('join-room', handleJoinRoom);
  socket.on('leave-room', handleLeaveRoom);
  socket.on('typing', handleTyping);

  socket.on('disconnect', (reason) => {
    console.log(`User disconnected: ${socket.data.user.id}`, reason);
  });
});

httpServer.listen(3000, () => {
  console.log('Server running on port 3000');
});

async function verifyToken(token: string): Promise<User> {
  // Verify JWT token
  return { id: '123', name: 'User' };
}

interface User {
  id: string;
  name: string;
}
```

## Socket.IO Client Setup

```typescript
// hooks/useSocket.ts
import { useEffect, useState } from 'react';
import { io, Socket } from 'socket.io-client';

export function useSocket(url: string, token: string) {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    const socketInstance = io(url, {
      auth: { token },
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      reconnectionAttempts: 5
    });

    socketInstance.on('connect', () => {
      console.log('Connected to server');
      setConnected(true);
    });

    socketInstance.on('disconnect', (reason) => {
      console.log('Disconnected:', reason);
      setConnected(false);
    });

    socketInstance.on('connect_error', (error) => {
      console.error('Connection error:', error);
    });

    setSocket(socketInstance);

    return () => {
      socketInstance.close();
    };
  }, [url, token]);

  return { socket, connected };
}

// Usage in component
function ChatComponent() {
  const { socket, connected } = useSocket('http://localhost:3000', token);

  useEffect(() => {
    if (!socket) return;

    socket.on('message', (data) => {
      console.log('Received message:', data);
    });

    return () => {
      socket.off('message');
    };
  }, [socket]);

  const sendMessage = (message: string) => {
    socket?.emit('message', { text: message });
  };

  return (
    <div>
      <div>Status: {connected ? 'Connected' : 'Disconnected'}</div>
      {/* UI */}
    </div>
  );
}
```

## Rooms and Namespaces

```typescript
// Namespaces
const chatNamespace = io.of('/chat');
const notificationNamespace = io.of('/notifications');

chatNamespace.on('connection', (socket) => {
  console.log('Connected to chat namespace');
});

// Rooms
io.on('connection', (socket) => {
  // Join room
  socket.on('join-room', (roomId: string) => {
    socket.join(roomId);
    socket.to(roomId).emit('user-joined', {
      userId: socket.data.user.id,
      userName: socket.data.user.name
    });
  });

  // Leave room
  socket.on('leave-room', (roomId: string) => {
    socket.leave(roomId);
    socket.to(roomId).emit('user-left', {
      userId: socket.data.user.id
    });
  });

  // Send message to room
  socket.on('room-message', ({ roomId, message }) => {
    io.to(roomId).emit('message', {
      userId: socket.data.user.id,
      message,
      timestamp: Date.now()
    });
  });
});
```

## Authentication

```typescript
// JWT-based authentication
import jwt from 'jsonwebtoken';

io.use(async (socket, next) => {
  const token = socket.handshake.auth.token;

  if (!token) {
    return next(new Error('Authentication token required'));
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET!) as JWTPayload;
    
    // Load user from database
    const user = await db.user.findUnique({
      where: { id: decoded.userId }
    });

    if (!user) {
      return next(new Error('User not found'));
    }

    socket.data.user = user;
    next();
  } catch (error) {
    next(new Error('Invalid token'));
  }
});

interface JWTPayload {
  userId: string;
  exp: number;
}
```

## Connection Management

```typescript
// services/connection-manager.service.ts
export class ConnectionManager {
  private connections = new Map<string, Set<string>>();

  addConnection(userId: string, socketId: string): void {
    if (!this.connections.has(userId)) {
      this.connections.set(userId, new Set());
    }
    this.connections.get(userId)!.add(socketId);
  }

  removeConnection(userId: string, socketId: string): void {
    const userSockets = this.connections.get(userId);
    if (userSockets) {
      userSockets.delete(socketId);
      if (userSockets.size === 0) {
        this.connections.delete(userId);
      }
    }
  }

  getUserSockets(userId: string): string[] {
    return Array.from(this.connections.get(userId) || []);
  }

  isUserOnline(userId: string): boolean {
    return this.connections.has(userId);
  }

  getOnlineUsers(): string[] {
    return Array.from(this.connections.keys());
  }
}

const connectionManager = new ConnectionManager();

io.on('connection', (socket) => {
  const userId = socket.data.user.id;
  
  connectionManager.addConnection(userId, socket.id);

  socket.on('disconnect', () => {
    connectionManager.removeConnection(userId, socket.id);
  });
});
```

## Reconnection Strategies

```typescript
// Client-side reconnection
const socket = io(url, {
  reconnection: true,
  reconnectionDelay: 1000,
  reconnectionDelayMax: 5000,
  reconnectionAttempts: Infinity,
  timeout: 20000
});

socket.on('connect', () => {
  console.log('Connected');
  
  // Rejoin rooms after reconnection
  const rooms = getStoredRooms();
  rooms.forEach(roomId => {
    socket.emit('join-room', roomId);
  });
});

socket.on('reconnect', (attemptNumber) => {
  console.log(`Reconnected after ${attemptNumber} attempts`);
});

socket.on('reconnect_attempt', (attemptNumber) => {
  console.log(`Reconnection attempt ${attemptNumber}`);
});

socket.on('reconnect_error', (error) => {
  console.error('Reconnection error:', error);
});

socket.on('reconnect_failed', () => {
  console.error('Failed to reconnect');
  // Show offline UI
});
```

## Message Patterns

### Broadcasting

```typescript
// Broadcast to all clients
io.emit('announcement', { message: 'Server maintenance in 5 minutes' });

// Broadcast to all except sender
socket.broadcast.emit('user-joined', { userId: socket.data.user.id });

// Broadcast to room
io.to('room-123').emit('message', { text: 'Hello room' });

// Broadcast to multiple rooms
io.to('room-1').to('room-2').emit('event', data);

// Broadcast to all in namespace
io.of('/chat').emit('notification', data);
```

### Private Messages

```typescript
// Send to specific user
socket.on('private-message', async ({ recipientId, message }) => {
  const recipientSockets = connectionManager.getUserSockets(recipientId);

  recipientSockets.forEach(socketId => {
    io.to(socketId).emit('private-message', {
      senderId: socket.data.user.id,
      message,
      timestamp: Date.now()
    });
  });

  // Save to database
  await db.message.create({
    data: {
      senderId: socket.data.user.id,
      recipientId,
      content: message
    }
  });
});
```

### Acknowledgments

```typescript
// Server
socket.on('message', (data, callback) => {
  console.log('Received:', data);
  
  // Process message
  const result = processMessage(data);
  
  // Send acknowledgment
  callback({ status: 'ok', messageId: result.id });
});

// Client
socket.emit('message', { text: 'Hello' }, (response) => {
  console.log('Server acknowledged:', response);
});

// With timeout
socket.timeout(5000).emit('message', data, (err, response) => {
  if (err) {
    console.error('Timeout or error');
  } else {
    console.log('Response:', response);
  }
});
```

## Scaling with Redis

```typescript
// Redis adapter configuration
import { createAdapter } from '@socket.io/redis-adapter';
import { createClient } from 'redis';

const pubClient = createClient({ url: process.env.REDIS_URL });
const subClient = pubClient.duplicate();

await Promise.all([pubClient.connect(), subClient.connect()]);

io.adapter(createAdapter(pubClient, subClient));

// Emit to all servers
io.emit('global-event', data);

// Server-to-server communication
io.serverSideEmit('server-event', data);

io.on('server-event', (data) => {
  console.log('Received from another server:', data);
});
```

## Error Handling

```typescript
// Server-side error handling
io.on('connection', (socket) => {
  socket.on('error', (error) => {
    console.error('Socket error:', error);
  });

  socket.on('message', async (data) => {
    try {
      await processMessage(data);
    } catch (error) {
      socket.emit('error', {
        message: 'Failed to process message',
        code: 'PROCESS_ERROR'
      });
    }
  });
});

// Client-side error handling
socket.on('error', (error) => {
  console.error('Socket error:', error);
  showErrorNotification(error.message);
});

socket.on('connect_error', (error) => {
  console.error('Connection error:', error);
  if (error.message === 'Authentication failed') {
    // Redirect to login
  }
});
```

## Security Considerations

```typescript
// Rate limiting
import rateLimit from 'socket.io-rate-limit';

io.use(rateLimit({
  tokensPerInterval: 10,
  interval: 1000,
  fireImmediately: true
}));

// Input validation
socket.on('message', (data) => {
  if (!isValidMessage(data)) {
    socket.emit('error', { message: 'Invalid message format' });
    return;
  }
  
  processMessage(data);
});

// CORS configuration
const io = new Server(httpServer, {
  cors: {
    origin: process.env.ALLOWED_ORIGINS?.split(','),
    methods: ['GET', 'POST'],
    credentials: true
  }
});

// Disconnect malicious clients
socket.on('suspicious-activity', () => {
  socket.disconnect(true);
});
```

## Testing WebSocket

```typescript
// __tests__/socket.test.ts
import { io as Client, Socket } from 'socket.io-client';
import { createServer } from 'http';
import { Server } from 'socket.io';

describe('Socket.IO', () => {
  let io: Server;
  let serverSocket: Socket;
  let clientSocket: Socket;

  beforeAll((done) => {
    const httpServer = createServer();
    io = new Server(httpServer);
    httpServer.listen(() => {
      const port = (httpServer.address() as any).port;
      clientSocket = Client(`http://localhost:${port}`);
      
      io.on('connection', (socket) => {
        serverSocket = socket;
      });
      
      clientSocket.on('connect', done);
    });
  });

  afterAll(() => {
    io.close();
    clientSocket.close();
  });

  test('should emit and receive message', (done) => {
    clientSocket.on('hello', (arg) => {
      expect(arg).toBe('world');
      done();
    });
    
    serverSocket.emit('hello', 'world');
  });

  test('should acknowledge message', (done) => {
    serverSocket.on('message', (data, callback) => {
      callback({ status: 'ok' });
    });

    clientSocket.emit('message', 'test', (response) => {
      expect(response.status).toBe('ok');
      done();
    });
  });
});
```

## Alternative: ws Library

```typescript
// Using native ws library
import { WebSocketServer, WebSocket } from 'ws';

const wss = new WebSocketServer({ port: 8080 });

wss.on('connection', (ws: WebSocket) => {
  console.log('Client connected');

  ws.on('message', (data: Buffer) => {
    const message = JSON.parse(data.toString());
    console.log('Received:', message);

    // Echo back
    ws.send(JSON.stringify({ type: 'echo', data: message }));
  });

  ws.on('close', () => {
    console.log('Client disconnected');
  });

  ws.on('error', (error) => {
    console.error('WebSocket error:', error);
  });
});

// Client
const ws = new WebSocket('ws://localhost:8080');

ws.on('open', () => {
  ws.send(JSON.stringify({ type: 'message', text: 'Hello' }));
});

ws.on('message', (data) => {
  console.log('Received:', JSON.parse(data.toString()));
});
```

## Best Practices

1. **Authentication** - Always authenticate connections
2. **Validation** - Validate all incoming data
3. **Rate Limiting** - Prevent abuse
4. **Error Handling** - Handle all errors gracefully
5. **Reconnection** - Implement robust reconnection
6. **Scaling** - Use Redis adapter for multiple servers
7. **Monitoring** - Monitor connection counts and errors
8. **Security** - Use HTTPS/WSS in production
9. **Rooms** - Use rooms for efficient broadcasting
10. **Cleanup** - Clean up event listeners

---

## Quick Start

### Basic Socket.IO Server

```javascript
const express = require('express')
const { createServer } = require('http')
const { Server } = require('socket.io')

const app = express()
const httpServer = createServer(app)
const io = new Server(httpServer, {
  cors: {
    origin: '*'
  }
})

io.on('connection', (socket) => {
  console.log('Client connected:', socket.id)
  
  socket.on('message', (data) => {
    io.emit('message', data)
  })
  
  socket.on('disconnect', () => {
    console.log('Client disconnected:', socket.id)
  })
})

httpServer.listen(3000)
```

### Basic Socket.IO Client

```javascript
import { io } from 'socket.io-client'

const socket = io('http://localhost:3000')

socket.on('connect', () => {
  console.log('Connected:', socket.id)
})

socket.on('message', (data) => {
  console.log('Received:', data)
})

socket.emit('message', { text: 'Hello!' })
```

---

## Production Checklist

- [ ] **Connection Management**: Handle reconnections and disconnections
- [ ] **Authentication**: Authenticate WebSocket connections
- [ ] **Rate Limiting**: Implement rate limiting per connection
- [ ] **Scaling**: Use Redis adapter for multi-server scaling
- [ ] **Rooms**: Use rooms for efficient message broadcasting
- [ ] **Error Handling**: Handle connection errors gracefully
- [ ] **Heartbeat**: Implement ping/pong for connection health
- [ ] **Message Validation**: Validate all incoming messages
- [ ] **Monitoring**: Monitor connection counts and message rates
- [ ] **Security**: Use WSS (WebSocket Secure) in production
- [ ] **CORS**: Configure CORS properly
- [ ] **Resource Limits**: Set connection and message size limits

---

## Anti-patterns

### ❌ Don't: No Authentication

```javascript
// ❌ Bad - Anyone can connect
io.on('connection', (socket) => {
  socket.on('message', (data) => {
    // No auth check!
  })
})
```

```javascript
// ✅ Good - Authenticate connections
io.use((socket, next) => {
  const token = socket.handshake.auth.token
  if (verifyToken(token)) {
    next()
  } else {
    next(new Error('Authentication failed'))
  }
})
```

### ❌ Don't: No Rate Limiting

```javascript
// ❌ Bad - No rate limiting
socket.on('message', (data) => {
  // Can spam messages!
  broadcast(data)
})
```

```javascript
// ✅ Good - Rate limit messages
const rateLimiter = require('socket.io-rate-limiter')

io.use(rateLimiter({
  windowMs: 1000,
  max: 10  // Max 10 messages per second
}))
```

### ❌ Don't: Broadcast to All

```javascript
// ❌ Bad - Broadcasts to everyone
socket.on('message', (data) => {
  io.emit('message', data)  // All clients!
})
```

```javascript
// ✅ Good - Use rooms
socket.on('join-room', (roomId) => {
  socket.join(roomId)
})

socket.on('message', (data) => {
  io.to(data.roomId).emit('message', data)  // Only room members
})
```

---

## Integration Points

- **WebSocket Patterns** (`03-backend-api/websocket-patterns/`) - WebSocket API patterns
- **Error Handling** (`03-backend-api/error-handling/`) - Connection error handling
- **Authentication** (`10-authentication-authorization/`) - WebSocket auth

---

## Further Reading

- [Socket.IO Documentation](https://socket.io/docs/)
- [WebSocket Protocol](https://datatracker.ietf.org/doc/html/rfc6455)
- [ws Library](https://github.com/websockets/ws)
- [Socket.IO Redis Adapter](https://socket.io/docs/v4/redis-adapter/)
