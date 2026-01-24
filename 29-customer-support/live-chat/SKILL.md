---
name: Live Chat Implementation
description: Real-time communication between users and support agents using WebSockets, providing instant customer support, chat history, and agent assignment features.
---

# Live Chat Implementation

> **Current Level:** Intermediate  
> **Domain:** Customer Support / Real-time

---

## Overview

Live chat implementation enables real-time communication between users and support agents, providing instant customer support and improving user satisfaction. Effective live chat systems handle real-time messaging, typing indicators, file sharing, chat history, and agent assignment.

---

---

## Core Concepts

### Table of Contents

1. [Live Chat Architecture](#live-chat-architecture)
2. [Real-Time Communication](#real-time-communication)
3. [Chat UI Components](#chat-ui-components)
4. [Online/Offline Status](#onlineoffline-status)
5. [Typing Indicators](#typing-indicators)
6. [File Sharing](#file-sharing)
7. [Chat History](#chat-history)
8. [Agent Assignment](#agent-assignment)
9. [Canned Responses](#canned-responses)
10. [Chat Analytics](#chat-analytics)
11. [Mobile Support](#mobile-support)
12. [Integration with Helpdesk](#integration-with-helpdesk)
13. [Performance Optimization](#performance-optimization)
14. [Examples with Socket.io](#examples-with-socketio)

---

## Live Chat Architecture

### System Architecture

```typescript
// Live chat system architecture
interface ChatSystem {
  servers: ChatServer[];
  database: ChatDatabase;
  messageQueue: MessageQueue;
  analytics: ChatAnalytics;
  integrations: ChatIntegration[];
}

interface ChatServer {
  id: string;
  type: 'websocket' | 'sse';
  capacity: number;
  currentConnections: number;
}

// Live chat configuration
interface ChatConfig {
  maxConnections: number;
  messageRateLimit: number;
  sessionTimeout: number; // in milliseconds
  maxMessageSize: number;
  maxFileSize: number;
  allowedFileTypes: string[];
}

const defaultChatConfig: ChatConfig = {
  maxConnections: 1000,
  messageRateLimit: 10, // messages per second
  sessionTimeout: 30 * 60 * 1000, // 30 minutes
  maxMessageSize: 10000, // 10KB
  maxFileSize: 10 * 1024 * 1024, // 10MB
  allowedFileTypes: ['image/jpeg', 'image/png', 'image/gif', 'application/pdf'],
};
```

### Database Schema

```sql
-- Chat sessions
CREATE TABLE chat_sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL,
  agent_id UUID,
  status VARCHAR(50) NOT NULL DEFAULT 'active',
  started_at TIMESTAMP DEFAULT NOW(),
  ended_at TIMESTAMP,
  channel VARCHAR(50) NOT NULL DEFAULT 'web',
  user_agent TEXT,
  ip_address INET,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Chat messages
CREATE TABLE chat_messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id UUID REFERENCES chat_sessions(id) ON DELETE CASCADE,
  sender_id UUID NOT NULL,
  sender_type VARCHAR(50) NOT NULL, -- 'user' or 'agent'
  message_type VARCHAR(50) NOT NULL DEFAULT 'text', -- 'text', 'file', 'image', 'system'
  content TEXT,
  file_url VARCHAR(500),
  file_name VARCHAR(255),
  file_size INTEGER,
  is_internal BOOLEAN DEFAULT FALSE,
  read_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Agent status
CREATE TABLE agent_status (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_id UUID NOT NULL,
  status VARCHAR(50) NOT NULL, -- 'online', 'away', 'busy', 'offline'
  current_session_id UUID REFERENCES chat_sessions(id),
  max_concurrent_chats INTEGER DEFAULT 5,
  current_chats INTEGER DEFAULT 0,
  last_active_at TIMESTAMP DEFAULT NOW(),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Canned responses
CREATE TABLE canned_responses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  category VARCHAR(100),
  content TEXT NOT NULL,
  tags TEXT[],
  created_by UUID NOT NULL,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_chat_sessions_user_id ON chat_sessions(user_id);
CREATE INDEX idx_chat_sessions_agent_id ON chat_sessions(agent_id);
CREATE INDEX idx_chat_sessions_status ON chat_sessions(status);
CREATE INDEX idx_chat_messages_session_id ON chat_messages(session_id);
CREATE INDEX idx_chat_messages_created_at ON chat_messages(created_at);
CREATE INDEX idx_agent_status_agent_id ON agent_status(agent_id);
CREATE INDEX idx_agent_status_status ON agent_status(status);
```

---

## Real-Time Communication

### WebSocket Implementation

```typescript
// npm install socket.io
import { Server as SocketIOServer, Socket } from 'socket.io';

class ChatServer {
  private io: SocketIOServer;
  private activeSessions: Map<string, string> = new Map(); // sessionId -> socketId
  private agentSessions: Map<string, string[]> = new Map(); // agentId -> sessionIds

  constructor(httpServer: any) {
    this.io = new SocketIOServer(httpServer, {
      cors: {
        origin: process.env.CLIENT_URL,
        credentials: true,
      },
      pingTimeout: 60000,
      pingInterval: 25000,
    });

    this.setupEventHandlers();
  }

  private setupEventHandlers(): void {
    this.io.on('connection', (socket) => this.handleConnection(socket));
  }

  private handleConnection(socket: Socket): void {
    console.log('Client connected:', socket.id);

    // User joins chat
    socket.on('join_chat', async (data: { sessionId: string; userId: string }) => {
      await this.handleJoinChat(socket, data);
    });

    // Agent joins chat
    socket.on('agent_join', async (data: { sessionId: string; agentId: string }) => {
      await this.handleAgentJoin(socket, data);
    });

    // Send message
    socket.on('send_message', async (data: SendMessageData) => {
      await this.handleSendMessage(socket, data);
    });

    // Typing indicator
    socket.on('typing', (data: { sessionId: string; isTyping: boolean }) => {
      this.handleTyping(socket, data);
    });

    // Read receipt
    socket.on('message_read', async (data: { messageId: string }) => {
      await this.handleMessageRead(socket, data);
    });

    // Disconnect
    socket.on('disconnect', () => this.handleDisconnect(socket));
  }

  private async handleJoinChat(
    socket: Socket,
    data: { sessionId: string; userId: string }
  ): Promise<void> {
    const { sessionId, userId } = data;

    // Join socket room
    socket.join(sessionId);
    this.activeSessions.set(sessionId, socket.id);

    // Get or create session
    const session = await this.getOrCreateSession(sessionId, userId);

    // Send session info
    socket.emit('session_info', {
      sessionId: session.id,
      status: session.status,
      agentId: session.agentId,
    });

    // Notify if agent is assigned
    if (session.agentId) {
      this.io.to(sessionId).emit('agent_joined', {
        agentId: session.agentId,
      });
    }
  }

  private async handleAgentJoin(
    socket: Socket,
    data: { sessionId: string; agentId: string }
  ): Promise<void> {
    const { sessionId, agentId } = data;

    // Join socket room
    socket.join(sessionId);

    // Update session with agent
    await this.updateSessionAgent(sessionId, agentId);

    // Update agent status
    await this.updateAgentChats(agentId, sessionId, 1);

    // Notify user
    this.io.to(sessionId).emit('agent_joined', { agentId });

    // Send chat history
    const history = await this.getChatHistory(sessionId);
    socket.emit('chat_history', history);
  }

  private async handleSendMessage(
    socket: Socket,
    data: SendMessageData
  ): Promise<void> {
    const { sessionId, senderId, senderType, messageType, content, file } = data;

    // Save message
    const message = await this.saveMessage({
      sessionId,
      senderId,
      senderType,
      messageType,
      content,
      file,
    });

    // Broadcast to room
    this.io.to(sessionId).emit('new_message', {
      id: message.id,
      sessionId,
      senderId,
      senderType,
      messageType,
      content,
      file: message.file_url,
      createdAt: message.created_at,
    });
  }

  private handleTyping(
    socket: Socket,
    data: { sessionId: string; isTyping: boolean }
  ): void {
    socket.to(data.sessionId).emit('user_typing', {
      senderId: socket.data.userId,
      isTyping: data.isTyping,
    });
  }

  private async handleMessageRead(
    socket: Socket,
    data: { messageId: string }
  ): Promise<void> {
    await this.markMessageAsRead(data.messageId);

    // Notify sender
    const message = await this.getMessage(data.messageId);
    if (message) {
      this.io.to(message.session_id).emit('message_read', {
        messageId: data.messageId,
        readAt: new Date(),
      });
    }
  }

  private handleDisconnect(socket: Socket): void {
    console.log('Client disconnected:', socket.id);

    // Find and update session
    for (const [sessionId, socketId] of this.activeSessions.entries()) {
      if (socketId === socket.id) {
        this.activeSessions.delete(sessionId);
        this.io.to(sessionId).emit('user_disconnected', { sessionId });
        break;
      }
    }
  }

  private async getOrCreateSession(sessionId: string, userId: string): Promise<any> {
    let session = await this.prisma.chatSession.findUnique({
      where: { id: sessionId },
    });

    if (!session) {
      session = await this.prisma.chatSession.create({
        data: {
          id: sessionId,
          userId,
          status: 'active',
        },
      });
    }

    return session;
  }

  private async updateSessionAgent(sessionId: string, agentId: string): Promise<void> {
    await this.prisma.chatSession.update({
      where: { id: sessionId },
      data: { agentId },
    });
  }

  private async updateAgentChats(
    agentId: string,
    sessionId: string,
    increment: number
  ): Promise<void> {
    await this.prisma.agentStatus.update({
      where: { agentId },
      data: {
        currentChats: { increment },
        lastActiveAt: new Date(),
      },
    });
  }

  private async saveMessage(message: any): Promise<any> {
    return await this.prisma.chatMessage.create({
      data: message,
    });
  }

  private async getChatHistory(sessionId: string): Promise<any[]> {
    return await this.prisma.chatMessage.findMany({
      where: { sessionId },
      orderBy: { createdAt: 'asc' },
    });
  }

  private async markMessageAsRead(messageId: string): Promise<void> {
    await this.prisma.chatMessage.update({
      where: { id: messageId },
      data: { readAt: new Date() },
    });
  }

  private async getMessage(messageId: string): Promise<any> {
    return await this.prisma.chatMessage.findUnique({
      where: { id: messageId },
    });
  }

  constructor(private prisma: PrismaClient) {}
}

interface SendMessageData {
  sessionId: string;
  senderId: string;
  senderType: 'user' | 'agent';
  messageType: 'text' | 'file' | 'image';
  content?: string;
  file?: {
    url: string;
    name: string;
    size: number;
  };
}
```

### Server-Sent Events (SSE)

```typescript
class SSEChatServer {
  private clients: Map<string, Response> = new Map();

  constructor(private prisma: PrismaClient) {}

  /**
   * Handle SSE connection
   */
  async handleSSE(req: express.Request, res: express.Response): Promise<void> {
    const { sessionId, userId } = req.params;

    // Set SSE headers
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');
    res.setHeader('X-Accel-Buffering', 'no');

    // Store client
    this.clients.set(sessionId, res);

    // Send initial data
    await this.sendInitialData(res, sessionId);

    // Keep connection alive
    const heartbeat = setInterval(() => {
      res.write(': heartbeat\n\n');
    }, 30000);

    req.on('close', () => {
      clearInterval(heartbeat);
      this.clients.delete(sessionId);
    });
  }

  /**
   * Send message to client
   */
  sendMessage(sessionId: string, message: any): void {
    const client = this.clients.get(sessionId);
    if (client) {
      client.write(`data: ${JSON.stringify(message)}\n\n`);
    }
  }

  /**
   * Send initial data
   */
  private async sendInitialData(res: Response, sessionId: string): Promise<void> {
    const history = await this.prisma.chatMessage.findMany({
      where: { sessionId },
      orderBy: { createdAt: 'asc' },
    });

    res.write(`data: ${JSON.stringify({ type: 'history', messages: history })}\n\n`);
  }
}
```

---

## Chat UI Components

### React Chat Component

```tsx
import React, { useState, useEffect, useRef } from 'react';
import { io, Socket } from 'socket.io-client';

interface Message {
  id: string;
  senderId: string;
  senderType: 'user' | 'agent';
  messageType: 'text' | 'file' | 'image';
  content?: string;
  file?: {
    url: string;
    name: string;
    size: number;
  };
  createdAt: Date;
}

interface ChatProps {
  sessionId: string;
  userId: string;
  userName: string;
  isAgent?: boolean;
}

const LiveChat: React.FC<ChatProps> = ({
  sessionId,
  userId,
  userName,
  isAgent = false,
}) => {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [agentId, setAgentId] = useState<string | null>(null);
  const [isConnected, setIsConnected] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    // Connect to socket
    const newSocket = io(process.env.CHAT_SERVER_URL!, {
      auth: { sessionId, userId, isAgent },
    });

    setSocket(newSocket);

    newSocket.on('connect', () => {
      setIsConnected(true);
      console.log('Connected to chat server');
    });

    newSocket.on('disconnect', () => {
      setIsConnected(false);
      console.log('Disconnected from chat server');
    });

    newSocket.on('session_info', (data) => {
      setAgentId(data.agentId || null);
    });

    newSocket.on('agent_joined', (data) => {
      setAgentId(data.agentId);
    });

    newSocket.on('new_message', (message) => {
      setMessages(prev => [...prev, message]);
      scrollToBottom();
    });

    newSocket.on('chat_history', (history) => {
      setMessages(history);
      scrollToBottom();
    });

    newSocket.on('user_typing', (data) => {
      if (data.senderId !== userId) {
        setIsTyping(data.isTyping);
      }
    });

    newSocket.on('message_read', (data) => {
      setMessages(prev =>
        prev.map(msg =>
          msg.id === data.messageId
            ? { ...msg, readAt: data.readAt }
            : msg
        )
      );
    });

    return () => {
      newSocket.disconnect();
    };
  }, [sessionId, userId, isAgent]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = () => {
    if (!inputValue.trim() || !socket) return;

    socket.emit('send_message', {
      sessionId,
      senderId: userId,
      senderType: isAgent ? 'agent' : 'user',
      messageType: 'text',
      content: inputValue,
    });

    setInputValue('');
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleTyping = () => {
    if (!socket) return;
    socket.emit('typing', { sessionId, isTyping: true });

    setTimeout(() => {
      socket.emit('typing', { sessionId, isTyping: false });
    }, 1000);
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file || !socket) return;

    // Upload file
    uploadFile(file).then(url => {
      socket.emit('send_message', {
        sessionId,
        senderId: userId,
        senderType: isAgent ? 'agent' : 'user',
        messageType: file.type.startsWith('image/') ? 'image' : 'file',
        file: {
          url,
          name: file.name,
          size: file.size,
        },
      });
    });
  };

  const uploadFile = async (file: File): Promise<string> => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('/api/chat/upload', {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();
    return data.url;
  };

  return (
    <div className="live-chat">
      <div className="chat-header">
        <div className="status-indicator">
          <span className={`status ${isConnected ? 'online' : 'offline'}`} />
          {isConnected ? 'Connected' : 'Disconnected'}
        </div>
        {agentId && (
          <div className="agent-info">
            <span className="agent-badge">Support Agent</span>
          </div>
        )}
      </div>

      <div className="chat-messages">
        {messages.map(message => (
          <div
            key={message.id}
            className={`message ${message.senderType === isAgent ? 'agent' : 'user'}`}
          >
            <div className="message-sender">
              {message.senderType === 'agent' ? 'Agent' : 'You'}
            </div>
            {message.messageType === 'text' ? (
              <div className="message-content">{message.content}</div>
            ) : (
              <div className="message-file">
                <a href={message.file?.url} target="_blank" rel="noopener">
                  {message.file?.name}
                </a>
              </div>
            )}
            <div className="message-time">
              {new Date(message.createdAt).toLocaleTimeString()}
            </div>
          </div>
        ))}
        {isTyping && <div className="typing-indicator">Agent is typing...</div>}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input">
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileUpload}
          style={{ display: 'none' }}
          accept="image/*,.pdf"
        />
        <button
          className="attach-button"
          onClick={() => fileInputRef.current?.click()}
        >
          📎
        </button>
        <input
          type="text"
          value={inputValue}
          onChange={e => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          onInput={handleTyping}
          placeholder="Type a message..."
          disabled={!isConnected}
        />
        <button
          className="send-button"
          onClick={handleSendMessage}
          disabled={!inputValue.trim() || !isConnected}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default LiveChat;
```

---

## Online/Offline Status

### Agent Status Management

```typescript
class AgentStatusManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Set agent status
   */
  async setStatus(
    agentId: string,
    status: 'online' | 'away' | 'busy' | 'offline'
  ): Promise<void> {
    await this.prisma.agentStatus.upsert({
      where: { agentId },
      create: {
        agentId,
        status,
        currentChats: 0,
        lastActiveAt: new Date(),
      },
      update: {
        status,
        lastActiveAt: new Date(),
      },
    });
  }

  /**
   * Get available agents
   */
  async getAvailableAgents(): Promise<Array<{
    agentId: string;
    currentChats: number;
    maxConcurrentChats: number;
  }>> {
    const agents = await this.prisma.agentStatus.findMany({
      where: {
        status: 'online',
        currentChats: { lt: this.prisma.agentStatus.fields.maxConcurrentChats },
      },
    });

    return agents.map(agent => ({
      agentId: agent.agentId,
      currentChats: agent.currentChats,
      maxConcurrentChats: agent.maxConcurrentChats,
    }));
  }

  /**
   * Get agent status
   */
  async getStatus(agentId: string): Promise<{
    status: string;
    currentChats: number;
    lastActiveAt: Date;
  } | null> {
    const agent = await this.prisma.agentStatus.findUnique({
      where: { agentId },
    });

    if (!agent) return null;

    return {
      status: agent.status,
      currentChats: agent.currentChats,
      lastActiveAt: agent.lastActiveAt,
    };
  }

  /**
   * Update agent activity
   */
  async updateActivity(agentId: string): Promise<void> {
    await this.prisma.agentStatus.update({
      where: { agentId },
      data: { lastActiveAt: new Date() },
    });
  }

  /**
   * Auto-away inactive agents
   */
  async autoAwayAgents(inactiveMinutes: number = 5): Promise<void> {
    const inactiveTime = new Date(Date.now() - inactiveMinutes * 60 * 1000);

    await this.prisma.agentStatus.updateMany({
      where: {
        status: 'online',
        lastActiveAt: { lt: inactiveTime },
      },
      data: { status: 'away' },
    });
  }
}
```

---

## Typing Indicators

### Typing Implementation

```typescript
class TypingManager {
  private typingUsers: Map<string, Set<string>> = new Map(); // sessionId -> userIds
  private timeouts: Map<string, NodeJS.Timeout> = new Map(); // userId -> timeout

  /**
   * User started typing
   */
  startTyping(sessionId: string, userId: string): void {
    // Add to typing users
    if (!this.typingUsers.has(sessionId)) {
      this.typingUsers.set(sessionId, new Set());
    }
    this.typingUsers.get(sessionId)!.add(userId);

    // Clear existing timeout
    if (this.timeouts.has(userId)) {
      clearTimeout(this.timeouts.get(userId)!);
    }

    // Set timeout to stop typing
    const timeout = setTimeout(() => {
      this.stopTyping(sessionId, userId);
    }, 3000); // 3 seconds

    this.timeouts.set(userId, timeout);

    // Notify others
    this.notifyTyping(sessionId, userId, true);
  }

  /**
   * User stopped typing
   */
  stopTyping(sessionId: string, userId: string): void {
    // Remove from typing users
    const typingUsers = this.typingUsers.get(sessionId);
    if (typingUsers) {
      typingUsers.delete(userId);
      if (typingUsers.size === 0) {
        this.typingUsers.delete(sessionId);
      }
    }

    // Clear timeout
    if (this.timeouts.has(userId)) {
      clearTimeout(this.timeouts.get(userId)!);
      this.timeouts.delete(userId);
    }

    // Notify others
    this.notifyTyping(sessionId, userId, false);
  }

  /**
   * Get typing users for session
   */
  getTypingUsers(sessionId: string): string[] {
    return Array.from(this.typingUsers.get(sessionId) || []);
  }

  /**
   * Notify typing status
   */
  private notifyTyping(sessionId: string, userId: string, isTyping: boolean): void {
    // Emit to socket room
    io.to(sessionId).emit('user_typing', {
      userId,
      isTyping,
    });
  }
}
```

---

## File Sharing

### File Upload Handler

```typescript
import multer from 'multer';
import path from 'path';

// Configure multer
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const uploadPath = path.join(process.cwd(), 'uploads', 'chat');
    cb(null, uploadPath);
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1e9);
    cb(null, file.fieldname + '-' + uniqueSuffix + path.extname(file.originalname));
  },
});

const upload = multer({
  storage,
  limits: {
    fileSize: 10 * 1024 * 1024, // 10MB
  },
  fileFilter: (req, file, cb) => {
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf'];
    if (allowedTypes.includes(file.mimetype)) {
      cb(null, true);
    } else {
      cb(new Error('Invalid file type'));
    }
  },
});

// Express route for file upload
app.post('/api/chat/upload', upload.single('file'), async (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: 'No file uploaded' });
  }

  try {
    // Store file info in database
    const fileInfo = await prisma.chatFile.create({
      data: {
        originalName: req.file.originalname,
        fileName: req.file.filename,
        mimeType: req.file.mimetype,
        size: req.file.size,
        path: req.file.path,
      },
    });

    // Return file URL
    const fileUrl = `${process.env.APP_URL}/uploads/chat/${req.file.filename}`;
    res.json({ url: fileUrl, fileId: fileInfo.id });
  } catch (error) {
    console.error('Error uploading file:', error);
    res.status(500).json({ error: 'Failed to upload file' });
  }
});
```

---

## Chat History

### Chat History Manager

```typescript
class ChatHistoryManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Get chat history
   */
  async getHistory(
    sessionId: string,
    options?: {
      limit?: number;
      before?: Date;
    }
  ): Promise<any[]> {
    const where: any = { sessionId };

    if (options?.before) {
      where.createdAt = { lt: options.before };
    }

    return await this.prisma.chatMessage.findMany({
      where,
      orderBy: { createdAt: 'desc' },
      take: options?.limit || 50,
    });
  }

  /**
   * Get user's chat sessions
   */
  async getUserSessions(userId: string): Promise<any[]> {
    return await this.prisma.chatSession.findMany({
      where: { userId },
      orderBy: { startedAt: 'desc' },
      take: 20,
      include: {
        messages: {
          orderBy: { createdAt: 'asc' },
          take: 1,
        },
      },
    });
  }

  /**
   * Search messages
   */
  async searchMessages(
    sessionId: string,
    query: string
  ): Promise<any[]> {
    return await this.prisma.chatMessage.findMany({
      where: {
        sessionId,
        content: {
          contains: query,
          mode: 'insensitive',
        },
      },
      orderBy: { createdAt: 'desc' },
      take: 50,
    });
  }

  /**
   * Export chat transcript
   */
  async exportTranscript(sessionId: string): Promise<string> {
    const messages = await this.prisma.chatMessage.findMany({
      where: { sessionId },
      orderBy: { createdAt: 'asc' },
    });

    let transcript = `Chat Transcript - ${new Date().toISOString()}\n\n`;

    for (const message of messages) {
      const sender = message.sender_type === 'agent' ? 'Agent' : 'User';
      const timestamp = new Date(message.created_at).toLocaleString();
      const content = message.message_type === 'text'
        ? message.content
        : `[${message.message_type}] ${message.file_name}`;

      transcript += `[${timestamp}] ${sender}: ${content}\n`;
    }

    return transcript;
  }
}
```

---

## Agent Assignment

### Agent Assignment Strategy

```typescript
interface AssignmentStrategy {
  type: 'round_robin' | 'least_busy' | 'skill_based' | 'priority';
  assign(sessionId: string, availableAgents: string[]): Promise<string | null>;
}

class RoundRobinAssignment implements AssignmentStrategy {
  private currentIndex = 0;

  type = 'round_robin' as const;

  async assign(sessionId: string, availableAgents: string[]): Promise<string | null> {
    if (availableAgents.length === 0) return null;

    const agentId = availableAgents[this.currentIndex];
    this.currentIndex = (this.currentIndex + 1) % availableAgents.length;

    return agentId;
  }
}

class LeastBusyAssignment implements AssignmentStrategy {
  type = 'least_busy' as const;

  constructor(private agentStatusManager: AgentStatusManager) {}

  async assign(sessionId: string, availableAgents: string[]): Promise<string | null> {
    if (availableAgents.length === 0) return null;

    const agentStatuses = await Promise.all(
      availableAgents.map(async agentId => ({
        agentId,
        status: await this.agentStatusManager.getStatus(agentId),
      }))
    );

    // Sort by current chats (ascending)
    agentStatuses.sort((a, b) => {
      const aChats = a.status?.currentChats || 0;
      const bChats = b.status?.currentChats || 0;
      return aChats - bChats;
    });

    return agentStatuses[0].agentId;
  }
}

class AgentAssigner {
  constructor(
    private agentStatusManager: AgentStatusManager,
    private strategy: AssignmentStrategy
  ) {}

  /**
   * Assign agent to session
   */
  async assignAgent(sessionId: string): Promise<string | null> {
    // Get available agents
    const availableAgents = await this.agentStatusManager.getAvailableAgents();

    if (availableAgents.length === 0) {
      return null;
    }

    // Use strategy to assign
    const agentId = await this.strategy.assign(
      sessionId,
      availableAgents.map(a => a.agentId)
    );

    if (agentId) {
      // Update session
      await this.prisma.chatSession.update({
        where: { id: sessionId },
        data: { agentId },
      });

      // Update agent chats
      await this.agentStatusManager.updateAgentChats(agentId, sessionId, 1);
    }

    return agentId;
  }

  /**
   * Release agent from session
   */
  async releaseAgent(sessionId: string, agentId: string): Promise<void> {
    await this.prisma.chatSession.update({
      where: { id: sessionId },
      data: { agentId: null },
    });

    await this.agentStatusManager.updateAgentChats(agentId, sessionId, -1);
  }

  constructor(private prisma: PrismaClient) {}
}
```

---

## Canned Responses

### Canned Response Manager

```typescript
class CannedResponseManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Create canned response
   */
  async createResponse(response: {
    name: string;
    category?: string;
    content: string;
    tags?: string[];
    createdBy: string;
  }): Promise<string> {
    const created = await this.prisma.cannedResponse.create({
      data: response,
    });

    return created.id;
  }

  /**
   * Get all responses
   */
  async getResponses(filters?: {
    category?: string;
    tags?: string[];
    isActive?: boolean;
  }): Promise<any[]> {
    const where: any = {};

    if (filters?.category) {
      where.category = filters.category;
    }

    if (filters?.tags && filters.tags.length > 0) {
      where.tags = {
        hasSome: filters.tags,
      };
    }

    if (filters?.isActive !== undefined) {
      where.isActive = filters.isActive;
    }

    return await this.prisma.cannedResponse.findMany({
      where,
      orderBy: { name: 'asc' },
    });
  }

  /**
   * Search responses
   */
  async searchResponses(query: string): Promise<any[]> {
    return await this.prisma.cannedResponse.findMany({
      where: {
        OR: [
          { name: { contains: query, mode: 'insensitive' } },
          { content: { contains: query, mode: 'insensitive' } },
          { tags: { has: query } },
        ],
        isActive: true,
      },
      orderBy: { name: 'asc' },
    });
  }

  /**
   * Update response
   */
  async updateResponse(
    id: string,
    updates: Partial<typeof response>
  ): Promise<void> {
    await this.prisma.cannedResponse.update({
      where: { id },
      data: updates,
    });
  }

  /**
   * Delete response
   */
  async deleteResponse(id: string): Promise<void> {
    await this.prisma.cannedResponse.delete({
      where: { id },
    });
  }
}
```

---

## Chat Analytics

### Analytics Implementation

```typescript
interface ChatMetrics {
  totalSessions: number;
  activeSessions: number;
  averageSessionDuration: number;
  averageResponseTime: number;
  messagesPerSession: number;
  satisfactionScore: number;
}

class ChatAnalytics {
  constructor(private prisma: PrismaClient) {}

  /**
   * Get chat metrics
   */
  async getMetrics(params: {
    startDate: Date;
    endDate: Date;
  }): Promise<ChatMetrics> {
    const where = {
      startedAt: {
        gte: params.startDate,
        lte: params.endDate,
      },
    };

    const [totalSessions, activeSessions, sessions] = await Promise.all([
      this.prisma.chatSession.count({ where }),
      this.prisma.chatSession.count({
        where: { ...where, status: 'active' },
      }),
      this.prisma.chatSession.findMany({
        where,
        include: { messages: true },
      }),
    ]);

    // Calculate average session duration
    const completedSessions = sessions.filter(s => s.endedAt);
    const totalDuration = completedSessions.reduce(
      (sum, s) => sum + (s.endedAt!.getTime() - s.startedAt.getTime()),
      0
    );
    const averageSessionDuration =
      completedSessions.length > 0 ? totalDuration / completedSessions.length : 0;

    // Calculate average response time
    const responseTimes = await this.calculateResponseTimes(sessions);
    const averageResponseTime =
      responseTimes.length > 0
        ? responseTimes.reduce((sum, t) => sum + t, 0) / responseTimes.length
        : 0;

    // Calculate messages per session
    const messagesPerSession =
      sessions.length > 0
        ? sessions.reduce((sum, s) => sum + s.messages.length, 0) / sessions.length
        : 0;

    return {
      totalSessions,
      activeSessions,
      averageSessionDuration,
      averageResponseTime,
      messagesPerSession,
      satisfactionScore: 0, // Implement satisfaction tracking
    };
  }

  /**
   * Calculate response times
   */
  private async calculateResponseTimes(sessions: any[]): Promise<number[]> {
    const responseTimes: number[] = [];

    for (const session of sessions) {
      const messages = session.messages.filter((m: any) => m.senderType === 'agent');

      for (const message of messages) {
        // Find previous user message
        const prevMessage = session.messages.find(
          (m: any) =>
            m.senderType === 'user' &&
            m.createdAt < message.createdAt
        );

        if (prevMessage) {
          responseTimes.push(
            message.createdAt.getTime() - prevMessage.createdAt.getTime()
          );
        }
      }
    }

    return responseTimes;
  }
}
```

---

## Mobile Support

### React Native Chat Component

```tsx
import React, { useState, useEffect, useRef } from 'react';
import { View, Text, TextInput, ScrollView, TouchableOpacity, Image } from 'react-native';
import io from 'socket.io-client';

interface Message {
  id: string;
  senderId: string;
  senderType: 'user' | 'agent';
  messageType: 'text' | 'image';
  content?: string;
  imageUrl?: string;
  createdAt: string;
}

const MobileChat: React.FC<{ sessionId: string; userId: string }> = ({
  sessionId,
  userId,
}) => {
  const [socket, setSocket] = useState<any>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const scrollViewRef = useRef<ScrollView>(null);

  useEffect(() => {
    const newSocket = io(process.env.CHAT_SERVER_URL!);
    setSocket(newSocket);

    newSocket.on('connect', () => {
      console.log('Connected');
    });

    newSocket.on('new_message', (message: Message) => {
      setMessages(prev => [...prev, message]);
      setTimeout(() => scrollViewRef.current?.scrollToEnd({ animated: true }), 100);
    });

    newSocket.on('chat_history', (history: Message[]) => {
      setMessages(history);
      setTimeout(() => scrollViewRef.current?.scrollToEnd({ animated: true }), 100);
    });

    return () => newSocket.disconnect();
  }, []);

  const sendMessage = () => {
    if (!inputText.trim() || !socket) return;

    socket.emit('send_message', {
      sessionId,
      senderId: userId,
      senderType: 'user',
      messageType: 'text',
      content: inputText,
    });

    setInputText('');
  };

  return (
    <View style={styles.container}>
      <ScrollView
        ref={scrollViewRef}
        style={styles.messagesContainer}
        contentContainerStyle={styles.messagesContent}
      >
        {messages.map(message => (
          <View
            key={message.id}
            style={[
              styles.messageBubble,
              message.senderType === 'user' ? styles.userMessage : styles.agentMessage,
            ]}
          >
            {message.messageType === 'text' ? (
              <Text style={styles.messageText}>{message.content}</Text>
            ) : (
              <Image
                source={{ uri: message.imageUrl }}
                style={styles.messageImage}
              />
            )}
          </View>
        ))}
      </ScrollView>

      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          value={inputText}
          onChangeText={setInputText}
          placeholder="Type a message..."
        />
        <TouchableOpacity style={styles.sendButton} onPress={sendMessage}>
          <Text style={styles.sendButtonText}>Send</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = {
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  messagesContainer: {
    flex: 1,
  },
  messagesContent: {
    padding: 10,
  },
  messageBubble: {
    maxWidth: '80%',
    padding: 10,
    borderRadius: 10,
    marginBottom: 10,
  },
  userMessage: {
    alignSelf: 'flex-end',
    backgroundColor: '#007bff',
  },
  agentMessage: {
    alignSelf: 'flex-start',
    backgroundColor: '#e9ecef',
  },
  messageText: {
    color: '#fff',
  },
  messageImage: {
    width: 200,
    height: 200,
    borderRadius: 10,
  },
  inputContainer: {
    flexDirection: 'row',
    padding: 10,
    borderTopWidth: 1,
    borderTopColor: '#e9ecef',
  },
  input: {
    flex: 1,
    padding: 10,
    backgroundColor: '#f8f9fa',
    borderRadius: 20,
    marginRight: 10,
  },
  sendButton: {
    backgroundColor: '#007bff',
    padding: 10,
    borderRadius: 20,
  },
  sendButtonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
};

export default MobileChat;
```

---

## Integration with Helpdesk

### Ticket Creation from Chat

```typescript
class ChatToTicketIntegration {
  constructor(
    private prisma: PrismaClient,
    private zendeskManager: ZendeskTicketManager
  ) {}

  /**
   * Create ticket from chat session
   */
  async createTicketFromSession(sessionId: string): Promise<number> {
    const session = await this.prisma.chatSession.findUnique({
      where: { id: sessionId },
      include: {
        messages: true,
        user: true,
      },
    });

    if (!session) {
      throw new Error('Session not found');
    }

    // Generate transcript
    const transcript = this.generateTranscript(session.messages);

    // Create Zendesk ticket
    const ticketId = await this.zendeskManager.createTicket({
      subject: `Chat Session - ${session.id}`,
      description: transcript,
      requester: {
        name: session.user.name,
        email: session.user.email,
      },
      type: 'question',
      tags: ['chat', `session-${sessionId}`],
      customFields: {
        chat_session_id: sessionId,
        user_id: session.userId,
      },
    });

    // Update session with ticket ID
    await this.prisma.chatSession.update({
      where: { id: sessionId },
      data: { zendeskTicketId: ticketId },
    });

    return ticketId;
  }

  /**
   * Generate transcript
   */
  private generateTranscript(messages: any[]): string {
    let transcript = 'Chat Transcript:\n\n';

    for (const message of messages) {
      const sender = message.senderType === 'agent' ? 'Agent' : 'User';
      const timestamp = new Date(message.createdAt).toLocaleString();
      const content = message.messageType === 'text'
        ? message.content
        : `[${message.messageType}] ${message.fileName}`;

      transcript += `[${timestamp}] ${sender}: ${content}\n`;
    }

    return transcript;
  }

  /**
   * Add message to ticket
   */
  async addMessageToTicket(
    sessionId: string,
    message: any
  ): Promise<void> {
    const session = await this.prisma.chatSession.findUnique({
      where: { id: sessionId },
    });

    if (!session?.zendeskTicketId) return;

    await this.zendeskManager.addComment(
      session.zendeskTicketId,
      `${message.senderType === 'agent' ? 'Agent' : 'User'}: ${message.content}`,
      false // Internal comment
    );
  }
}
```

---

## Performance Optimization

### Message Compression

```typescript
import { compress, decompress } from 'lz4';

class MessageCompressor {
  /**
   * Compress message
   */
  static compressMessage(message: any): string {
    const json = JSON.stringify(message);
    const compressed = compress(json);
    return compressed.toString('base64');
  }

  /**
   * Decompress message
   */
  static decompressMessage(compressed: string): any {
    const buffer = Buffer.from(compressed, 'base64');
    const decompressed = decompress(buffer);
    return JSON.parse(decompressed.toString());
  }
}

// Usage in socket handler
socket.on('new_message', (compressedMessage) => {
  const message = MessageCompressor.decompressMessage(compressedMessage);
  setMessages(prev => [...prev, message]);
});
```

---

## Examples with Socket.io

### Complete Socket.io Server

```typescript
import express from 'express';
import { createServer } from 'http';
import { Server as SocketIOServer } from 'socket.io';

const app = express();
const httpServer = createServer(app);
const io = new SocketIOServer(httpServer, {
  cors: {
    origin: process.env.CLIENT_URL,
    credentials: true,
  },
});

const typingManager = new TypingManager();
const agentAssigner = new AgentAssigner(
  new AgentStatusManager(prisma),
  new LeastBusyAssignment(new AgentStatusManager(prisma))
);

io.on('connection', (socket) => {
  console.log('User connected:', socket.id);

  socket.on('join_chat', async (data) => {
    const { sessionId, userId } = data;
    socket.join(sessionId);
    socket.data.sessionId = sessionId;
    socket.data.userId = userId;

    // Try to assign agent
    const agentId = await agentAssigner.assignAgent(sessionId);
    if (agentId) {
      io.to(sessionId).emit('agent_joined', { agentId });
    }
  });

  socket.on('send_message', async (data) => {
    const message = await prisma.chatMessage.create({
      data: {
        sessionId: data.sessionId,
        senderId: data.senderId,
        senderType: data.senderType,
        messageType: data.messageType,
        content: data.content,
      },
    });

    io.to(data.sessionId).emit('new_message', message);
  });

  socket.on('typing', (data) => {
    typingManager.startTyping(data.sessionId, socket.data.userId);
  });

  socket.on('disconnect', () => {
    console.log('User disconnected:', socket.id);
  });
});

httpServer.listen(3000, () => {
  console.log('Chat server running on port 3000');
});
```

---

---

## Quick Start

### Basic Chat Server

```javascript
const io = require('socket.io')(server)

io.on('connection', (socket) => {
  socket.on('message', (data) => {
    // Broadcast to all clients
    io.emit('message', {
      user: data.user,
      text: data.text,
      timestamp: new Date()
    })
  })
})
```

### Basic Chat Client

```javascript
const socket = io('http://localhost:3000')

socket.on('connect', () => {
  console.log('Connected to chat')
})

socket.on('message', (data) => {
  displayMessage(data)
})

function sendMessage(text) {
  socket.emit('message', {
    user: currentUser,
    text: text
  })
}
```

---

## Production Checklist

- [ ] **WebSocket Server**: WebSocket server configured
- [ ] **Authentication**: Chat connections authenticated
- [ ] **Message Storage**: Chat history persisted
- [ ] **Typing Indicators**: Typing indicators implemented
- [ ] **Online Status**: Online/offline status tracking
- [ ] **File Sharing**: File upload and sharing
- [ ] **Agent Assignment**: Agent routing and assignment
- [ ] **Canned Responses**: Quick response templates
- [ ] **Analytics**: Chat analytics and metrics
- [ ] **Mobile Support**: Mobile-optimized chat UI
- [ ] **Helpdesk Integration**: Integration with ticketing system
- [ ] **Rate Limiting**: Prevent message spam

---

## Anti-patterns

### ❌ Don't: No Message Persistence

```javascript
// ❌ Bad - Messages lost on disconnect
socket.on('message', (data) => {
  io.emit('message', data)  // Not saved!
})
```

```javascript
// ✅ Good - Persist messages
socket.on('message', async (data) => {
  // Save to database
  await db.messages.create({
    userId: data.userId,
    text: data.text,
    timestamp: new Date()
  })
  
  // Then broadcast
  io.emit('message', data)
})
```

### ❌ Don't: No Authentication

```javascript
// ❌ Bad - Anyone can connect
io.on('connection', (socket) => {
  // No auth check!
})
```

```javascript
// ✅ Good - Authenticate
io.use((socket, next) => {
  const token = socket.handshake.auth.token
  if (verifyToken(token)) {
    socket.userId = getUserId(token)
    next()
  } else {
    next(new Error('Authentication failed'))
  }
})
```

---

## Integration Points

- **WebSocket Patterns** (`34-real-time-features/websocket-patterns/`) - WebSocket implementation
- **Ticketing System** (`29-customer-support/ticketing-system/`) - Support integration
- **Helpdesk Integration** (`29-customer-support/helpdesk-integration/`) - Helpdesk tools

---

## Further Reading

- [Socket.io Documentation](https://socket.io/docs/)
- [WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
