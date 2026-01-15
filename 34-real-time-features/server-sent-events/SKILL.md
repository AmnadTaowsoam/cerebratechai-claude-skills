# Server-Sent Events (SSE)

## Overview

Server-Sent Events (SSE) enable servers to push updates to clients over HTTP. This guide covers implementation, use cases, and best practices.

## SSE Concepts

```
Client                    Server
  |                          |
  |--- HTTP Request -------->|
  |<-- Event Stream ---------|
  |<-- Event 1 --------------|
  |<-- Event 2 --------------|
  |<-- Event 3 --------------|
```

**Features:**
- Unidirectional (server to client)
- Built on HTTP
- Auto-reconnection
- Text-based protocol
- Simple implementation

## SSE vs WebSocket

| Feature | SSE | WebSocket |
|---------|-----|-----------|
| Direction | Server → Client | Bidirectional |
| Protocol | HTTP | WebSocket |
| Reconnection | Automatic | Manual |
| Data Format | Text | Binary/Text |
| Use Case | Updates, notifications | Chat, gaming |

**Use SSE when:**
- One-way communication needed
- Simple implementation preferred
- HTTP infrastructure required
- Auto-reconnection desired

## Server Implementation (Node.js/Express)

```typescript
// server.ts
import express from 'express';
import cors from 'cors';

const app = express();
app.use(cors());

interface Client {
  id: string;
  response: express.Response;
  userId?: string;
}

const clients: Client[] = [];

app.get('/events', (req, res) => {
  // Set SSE headers
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');
  res.setHeader('X-Accel-Buffering', 'no'); // Disable nginx buffering

  // Authentication
  const token = req.query.token as string;
  const userId = verifyToken(token);

  const clientId = Date.now().toString();
  const client: Client = { id: clientId, response: res, userId };

  clients.push(client);

  // Send initial connection event
  sendEvent(res, 'connected', { clientId });

  // Heartbeat to keep connection alive
  const heartbeat = setInterval(() => {
    res.write(': heartbeat\n\n');
  }, 30000);

  // Cleanup on disconnect
  req.on('close', () => {
    clearInterval(heartbeat);
    const index = clients.findIndex(c => c.id === clientId);
    if (index !== -1) {
      clients.splice(index, 1);
    }
    console.log(`Client ${clientId} disconnected`);
  });
});

function sendEvent(res: express.Response, event: string, data: any): void {
  res.write(`event: ${event}\n`);
  res.write(`data: ${JSON.stringify(data)}\n`);
  res.write(`id: ${Date.now()}\n`);
  res.write('\n');
}

function broadcast(event: string, data: any): void {
  clients.forEach(client => {
    sendEvent(client.response, event, data);
  });
}

function sendToUser(userId: string, event: string, data: any): void {
  clients
    .filter(client => client.userId === userId)
    .forEach(client => {
      sendEvent(client.response, event, data);
    });
}

// Example: Send notification
app.post('/notify', (req, res) => {
  const { userId, message } = req.body;
  sendToUser(userId, 'notification', { message });
  res.json({ success: true });
});

// Example: Broadcast to all
app.post('/broadcast', (req, res) => {
  const { message } = req.body;
  broadcast('announcement', { message });
  res.json({ success: true });
});

app.listen(3000, () => {
  console.log('SSE server running on port 3000');
});

function verifyToken(token: string): string {
  // Verify JWT and return userId
  return 'user-123';
}
```

## Next.js API Routes

```typescript
// pages/api/events.ts
import type { NextApiRequest, NextApiResponse } from 'next';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');

  // Send initial event
  res.write(`data: ${JSON.stringify({ type: 'connected' })}\n\n`);

  // Send updates every 5 seconds
  const interval = setInterval(() => {
    res.write(`data: ${JSON.stringify({
      type: 'update',
      timestamp: Date.now()
    })}\n\n`);
  }, 5000);

  // Cleanup
  req.on('close', () => {
    clearInterval(interval);
    res.end();
  });
}

// Disable body parsing for SSE
export const config = {
  api: {
    bodyParser: false
  }
};
```

## FastAPI Implementation

```python
# main.py
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse
import asyncio
import json

app = FastAPI()

clients = []

@app.get("/events")
async def events(request: Request):
    async def event_generator():
        client_id = str(len(clients))
        clients.append(client_id)
        
        try:
            # Send initial connection event
            yield {
                "event": "connected",
                "data": json.dumps({"clientId": client_id})
            }
            
            # Keep connection alive
            while True:
                if await request.is_disconnected():
                    break
                
                # Send heartbeat
                yield {
                    "event": "heartbeat",
                    "data": json.dumps({"timestamp": asyncio.get_event_loop().time()})
                }
                
                await asyncio.sleep(30)
                
        finally:
            clients.remove(client_id)
    
    return EventSourceResponse(event_generator())

@app.post("/broadcast")
async def broadcast(message: dict):
    # Broadcast to all clients
    # Implementation depends on your architecture
    return {"success": True}
```

## Client Implementation

```typescript
// hooks/useSSE.ts
import { useEffect, useState, useCallback } from 'react';

interface SSEOptions {
  url: string;
  token?: string;
  onMessage?: (event: MessageEvent) => void;
  onError?: (error: Event) => void;
}

export function useSSE({ url, token, onMessage, onError }: SSEOptions) {
  const [connected, setConnected] = useState(false);
  const [eventSource, setEventSource] = useState<EventSource | null>(null);

  useEffect(() => {
    const urlWithToken = token ? `${url}?token=${token}` : url;
    const es = new EventSource(urlWithToken);

    es.onopen = () => {
      console.log('SSE connected');
      setConnected(true);
    };

    es.onmessage = (event) => {
      console.log('SSE message:', event.data);
      onMessage?.(event);
    };

    es.onerror = (error) => {
      console.error('SSE error:', error);
      setConnected(false);
      onError?.(error);
    };

    setEventSource(es);

    return () => {
      es.close();
    };
  }, [url, token]);

  return { connected, eventSource };
}

// Usage
function NotificationComponent() {
  const [notifications, setNotifications] = useState<any[]>([]);

  const { connected } = useSSE({
    url: '/api/events',
    token: 'your-token',
    onMessage: (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'notification') {
        setNotifications(prev => [...prev, data]);
      }
    }
  });

  return (
    <div>
      <div>Status: {connected ? 'Connected' : 'Disconnected'}</div>
      {notifications.map((notif, i) => (
        <div key={i}>{notif.message}</div>
      ))}
    </div>
  );
}
```

## Event Streams

```typescript
// Server: Named events
app.get('/events', (req, res) => {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');

  // Send different event types
  setInterval(() => {
    // Notification event
    res.write('event: notification\n');
    res.write(`data: ${JSON.stringify({ message: 'New notification' })}\n\n`);
  }, 10000);

  setInterval(() => {
    // Update event
    res.write('event: update\n');
    res.write(`data: ${JSON.stringify({ count: 42 })}\n\n`);
  }, 5000);
});

// Client: Listen to specific events
const eventSource = new EventSource('/api/events');

eventSource.addEventListener('notification', (event) => {
  const data = JSON.parse(event.data);
  console.log('Notification:', data);
});

eventSource.addEventListener('update', (event) => {
  const data = JSON.parse(event.data);
  console.log('Update:', data);
});
```

## Reconnection

```typescript
// Client-side reconnection handling
class SSEClient {
  private eventSource: EventSource | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;

  constructor(private url: string) {}

  connect(): void {
    this.eventSource = new EventSource(this.url);

    this.eventSource.onopen = () => {
      console.log('Connected');
      this.reconnectAttempts = 0;
    };

    this.eventSource.onerror = (error) => {
      console.error('Error:', error);
      this.eventSource?.close();
      this.reconnect();
    };

    this.eventSource.onmessage = (event) => {
      console.log('Message:', event.data);
    };
  }

  private reconnect(): void {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('Max reconnection attempts reached');
      return;
    }

    this.reconnectAttempts++;
    const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);

    console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`);

    setTimeout(() => {
      this.connect();
    }, delay);
  }

  disconnect(): void {
    this.eventSource?.close();
  }
}

// Usage
const client = new SSEClient('/api/events');
client.connect();
```

## Multiple Channels

```typescript
// Server: Multiple event streams
app.get('/events/:channel', (req, res) => {
  const channel = req.params.channel;

  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');

  // Subscribe to channel
  subscribeToChannel(channel, (data) => {
    res.write(`data: ${JSON.stringify(data)}\n\n`);
  });

  req.on('close', () => {
    unsubscribeFromChannel(channel);
  });
});

// Client: Multiple connections
function useMultipleChannels(channels: string[]) {
  const [data, setData] = useState<Record<string, any>>({});

  useEffect(() => {
    const eventSources = channels.map(channel => {
      const es = new EventSource(`/api/events/${channel}`);
      
      es.onmessage = (event) => {
        setData(prev => ({
          ...prev,
          [channel]: JSON.parse(event.data)
        }));
      };

      return es;
    });

    return () => {
      eventSources.forEach(es => es.close());
    };
  }, [channels]);

  return data;
}
```

## Authentication

```typescript
// Server: Token-based auth
app.get('/events', (req, res) => {
  const token = req.query.token as string;

  try {
    const user = verifyToken(token);
    
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');

    // Send user-specific events
    sendUserEvents(user.id, res);
  } catch (error) {
    res.status(401).json({ error: 'Unauthorized' });
  }
});

// Client: Pass token in URL
const eventSource = new EventSource(`/api/events?token=${authToken}`);

// Or use custom headers (requires polyfill)
import { EventSourcePolyfill } from 'event-source-polyfill';

const eventSource = new EventSourcePolyfill('/api/events', {
  headers: {
    'Authorization': `Bearer ${authToken}`
  }
});
```

## Scaling Considerations

```typescript
// Using Redis for pub/sub across servers
import { createClient } from 'redis';

const publisher = createClient({ url: process.env.REDIS_URL });
const subscriber = publisher.duplicate();

await Promise.all([publisher.connect(), subscriber.connect()]);

// Subscribe to events
await subscriber.subscribe('notifications', (message) => {
  const data = JSON.parse(message);
  
  // Send to connected clients
  clients.forEach(client => {
    if (client.userId === data.userId) {
      sendEvent(client.response, 'notification', data);
    }
  });
});

// Publish event (from any server)
app.post('/notify', async (req, res) => {
  const { userId, message } = req.body;
  
  await publisher.publish('notifications', JSON.stringify({
    userId,
    message,
    timestamp: Date.now()
  }));

  res.json({ success: true });
});
```

## Best Practices

1. **Heartbeat** - Send periodic heartbeats to keep connection alive
2. **Reconnection** - Implement exponential backoff
3. **Authentication** - Secure event streams
4. **Event IDs** - Use event IDs for tracking
5. **Error Handling** - Handle connection errors gracefully
6. **Buffering** - Disable proxy buffering
7. **Cleanup** - Clean up on disconnect
8. **Scaling** - Use Redis for multi-server setups
9. **Monitoring** - Monitor connection counts
10. **Fallback** - Provide polling fallback for old browsers

## Resources

- [SSE Specification](https://html.spec.whatwg.org/multipage/server-sent-events.html)
- [EventSource API](https://developer.mozilla.org/en-US/docs/Web/API/EventSource)
- [SSE vs WebSocket](https://ably.com/topic/server-sent-events-vs-websockets)
- [sse-starlette](https://github.com/sysid/sse-starlette)
