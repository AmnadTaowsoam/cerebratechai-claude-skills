# Conversational UI

## Overview

Conversational UI design focuses on creating natural, intuitive interfaces for human-AI interactions.

---

## 1. Conversational UI Principles

### Core Principles

```markdown
# Conversational UI Principles

## 1. Natural Language
- Use conversational language
- Avoid technical jargon
- Be helpful and friendly
- Provide clear guidance

## 2. Context Awareness
- Maintain conversation context
- Reference previous messages
- Understand user intent
- Adapt to user's expertise level

## 3. Clarity and Simplicity
- Keep messages concise
- Use simple language
- Avoid unnecessary complexity
- Be direct and clear

## 4. Responsiveness
- Respond quickly
- Provide timely feedback
- Show typing indicators
- Handle errors gracefully

## 5. Personality and Tone
- Define consistent personality
- Match brand voice
- Be authentic and genuine
- Adapt to user's communication style

## 6. Accessibility
- Support keyboard navigation
- Screen reader compatible
- High contrast ratios
- Clear focus indicators
- Error messages are descriptive

## 7. Multi-Turn Support
- Handle concurrent conversations
- Maintain separate contexts
- Allow topic switching
- Preserve conversation history

## 8. Error Recovery
- Handle errors gracefully
- Provide helpful error messages
- Suggest alternatives
- Allow for recovery

## 9. Progressive Disclosure
- Start with high-level information
- Provide details on request
- Balance completeness with conciseness
- Avoid overwhelming users

## 10. Mobile Considerations
- Touch-friendly interface
- Responsive design
- Optimized for mobile
- Fast load times
```

---

## 2. Message Design

### Message Structure

```markdown
# Message Structure

## Message Components

### 1. Content
- Main message text
- Rich media (images, cards, tables)
- Code blocks with syntax highlighting
- Links and references

### 2. Metadata
- Timestamp
- Message type (user/assistant/system)
- Status indicators
- Attribution (if applicable)

### 3. Actions
- Quick actions (buttons, links)
- Copy to clipboard
- Share functionality
- Feedback options

### 4. Context
- Referenced messages
- Related information
- Supporting resources
```

### Message Types

```markdown
# Message Types

## User Messages
```
User: "What's the weather today?"
```

## Assistant Messages
```
Assistant: "The weather today is sunny with a high of 75°F."
```

## System Messages
```
System: "Your session has expired. Please log in again."
```

## Error Messages
```
Error: "I apologize, but I encountered an error. Please try again."
```

## Typing Indicators
```
Typing...
```

## Thinking Indicators
```
Thinking...
```
```

---

## 3. User Input Patterns

### Text Input

```typescript
// Text Input Component
'use client'

import { useState, useRef, useEffect } from 'react'

interface TextInputProps {
  onSend: (message: string) => void
  disabled?: boolean
  placeholder?: string
  multiline?: boolean
}

export default function TextInput({ onSend, disabled, placeholder, multiline }: TextInputProps) {
  const [input, setInput] = useState('')
  const [isFocused, setIsFocused] = useState(false)
  const inputRef = useRef<HTMLTextAreaElement>(null)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (input.trim() && !disabled) {
      onSend(input)
      setInput('')
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey && !multiline) {
      e.preventDefault()
      handleSubmit(e)
    } else if (e.key === 'Enter' && e.shiftKey && multiline) {
      // Allow new line in multiline mode
    }
  }

  const autoResize = () => {
    if (inputRef.current) {
      inputRef.current.style.height = 'auto'
      inputRef.current.style.height = inputRef.current.scrollHeight + 'px'
    }
  }

  useEffect(() => {
    if (isFocused && inputRef.current) {
      inputRef.current.focus()
    }
  }, [isFocused])

  return (
    <form onSubmit={handleSubmit} className="text-input">
      <textarea
        ref={inputRef}
        value={input}
        onChange={e => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        onInput={autoResize}
        placeholder={placeholder || 'Type a message...'}
        disabled={disabled}
        rows={multiline ? 4 : 1}
        className="chat-input"
      />
      <button type="submit" disabled={disabled || !input.trim()}>
        Send
      </button>
    </form>
  )
}
```

### Voice Input

```typescript
// Voice Input Component
'use client'

import { useState, useRef, useEffect } from 'react'

interface VoiceInputProps {
  onTranscript: (transcript: string) => void
  disabled?: boolean
}

export default function VoiceInput({ onTranscript, disabled }: VoiceInputProps) {
  const [isListening, setIsListening] = useState(false)
  const [transcript, setTranscript] = useState('')
  const recognitionRef = useRef<any>(null)

  const toggleListening = async () => {
    if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
      alert('Speech recognition is not supported in this browser.')
      return
    }

    if (isListening) {
      recognitionRef.current?.stop()
      setIsListening(false)
    } else {
      try {
        const recognition = new (window as any).webkitSpeechRecognition || (window as any).SpeechRecognition()
        recognition.continuous = false
        recognition.lang = 'en-US'
        recognition.interimResults = true

        recognition.onresult = (event: any) => {
          setTranscript(event.results[0].transcript)
        }

        recognition.onerror = () => {
          console.error('Speech recognition error')
          setIsListening(false)
        }

        recognition.onend = () => {
          setIsListening(false)
        }

        recognitionRef.current = recognition
        recognition.start()
        setIsListening(true)
      } catch (error) {
        console.error('Speech recognition error:', error)
      }
    }
  }

  const handleSubmit = () => {
    if (transcript.trim()) {
      onTranscript(transcript)
      setTranscript('')
    }
  }

  return (
    <div className="voice-input">
      <button
        type="button"
        onClick={toggleListening}
        disabled={disabled}
        className={`voice-button ${isListening ? 'listening' : ''}`}
      >
        {isListening ? 'Stop' : 'Start'} Voice Input
      </button>
      <div className="transcript">
        {transcript || 'Listening...'}
      </div>
      <button
        type="button"
        onClick={handleSubmit}
        disabled={disabled || !transcript.trim()}
        className="send-button"
      >
        Send
      </button>
    </div>
  )
}
```

### Quick Replies

```typescript
// Quick Replies Component
'use client'

interface QuickReplyProps {
  replies: string[]
  onSelect: (reply: string) => void
}

export default function QuickReplies({ replies, onSelect }: QuickReplyProps) {
  return (
    <div className="quick-replies">
      {replies.map((reply, index) => (
        <button
          key={index}
          onClick={() => onSelect(reply)}
          className="quick-reply-button"
        >
          {reply}
        </button>
      ))}
    </div>
  )
}
```

### File Upload

```typescript
// File Upload Component
'use client'

import { useState, useRef } from 'react'

interface FileUploadProps {
  onUpload: (files: File[]) => void
  disabled?: boolean
  accept?: string
  maxSize?: number
}

export default function FileUpload({ onUpload, disabled, accept, maxSize }: FileUploadProps) {
  const [isDragging, setIsDragging] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)

    const files = e.dataTransfer.files
    if (files.length > 0) {
      const validFiles = Array.from(files).filter(file => {
        if (maxSize && file.size > maxSize * 1024 * 1024) {
          return false
        }
        if (accept && !file.type.match(new RegExp(accept))) {
          return false
        }
        return true
      })

      if (validFiles.length > 0) {
        onUpload(validFiles)
      }
    }
  }

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files
    if (files.length > 0) {
      const validFiles = Array.from(files).filter(file => {
        if (maxSize && file.size > maxSize * 1024 * 10**6) {
          return false
        }
        return true
      })

      if (validFiles.length > 0) {
        onUpload(validFiles)
      }
    }
  }

  return (
    <div
      className={`file-upload ${isDragging ? 'dragging' : ''}`}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
    >
      <input
        ref={fileInputRef}
        type="file"
        onChange={handleFileSelect}
        accept={accept}
        disabled={disabled}
        style={{ display: 'none' }}
        id="file-input"
      />
      <label htmlFor="file-input" className="upload-area">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 5v14m0a5 5 12h14" />
        </svg>
        <p>Drop files here or click to upload</p>
      </label>
      {uploadProgress > 0 && (
        <div className="progress-bar">
          <div
            className="progress-fill"
            style={{ width: `${uploadProgress}%` }}
          />
        </div>
      )}
    </div>
  )
}
```

---

## 4. Response Formatting

### Text Formatting

```typescript
// Message Formatter
interface MessageFormatter {
  formatMarkdown(content: string): string
  formatCode(content: string): string
  formatLinks(content: string): string
  formatLists(content: string): string
}

class MessageFormatter implements MessageFormatter {
  formatMarkdown(content: string): string {
    // Basic markdown formatting
    return content
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/`(.*?)`/g, '<code>$1</code>')
      .replace(/\n/g, '<br>')
  }

  formatCode(content: string): string {
    // Format code blocks
    return content.replace(/```(\w+)?\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
  }

  formatLinks(content: string): string {
    // Format links
    return content.replace(
      /(https?:\/\/[^\s]+)/g,
      '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>'
    )
  }

  formatLists(content: string): string {
    // Format lists
    return content
      .replace(/^\s*[-*+]\s+(.*)$/gm, '<li>$1</li>')
      .replace(/^(\s*\d+\.\s+(.*)$/gm, '<li>$1</li>')
      .replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>')
  }

  format(content: string): string {
    return this.formatLinks(
      this.formatCode(
        this.formatLists(
          this.formatMarkdown(content)
        )
      )
    )
  }
}

// Usage
const formatter = new MessageFormatter()

const formatted = formatter.format(`
# Hello World

This is **bold** and *italic*.

\`\`\`const x = 1;

Visit https://example.com
`)
```

### Rich Media

```typescript
// Rich Media Component
interface RichMediaProps {
  media: {
    type: 'image' | 'video' | 'audio' | 'file'
    url: string
    title?: string
    description?: string
  }
}

export default function RichMedia({ media }: RichMediaProps) {
  const renderMedia = () => {
    switch (media.type) {
      case 'image':
        return (
          <div className="media-container">
            <img src={media.url} alt={media.title} />
            {media.description && <p className="media-description">{media.description}</p>}
          </div>
        )
      case 'video':
        return (
          <div className="media-container">
            <video controls>
              <source src={media.url} />
              Your browser does not support the video tag.
            </video>
            {media.description && <p className="media-description">{media.description}</p>}
          </div>
        )
      case 'audio':
        return (
          <div className="media-container">
            <audio controls>
              <source src={media.url} />
              Your browser does not support the audio element.
            </audio>
            {media.description && <p className="media-description">{media.description}</p>}
          </div>
        )
      case 'file':
        return (
          <div className="media-container">
            <a href={media.url} download className="file-link">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 5v14m0a5 5 12h14" />
              </svg>
              <span>{media.title}</span>
            </a>
            {media.description && <p className="media-description">{media.description}</p>}
          </div>
        )
      default:
        return null
    }
  }

  return renderMedia()
}
```

### Cards

```typescript
// Card Component
interface CardProps {
  title: string
  description: string
  image?: string
  actions?: Array<{
    label: string
    onClick: () => void
  }>
}

export default function Card({ title, description, image, actions }: CardProps) {
  return (
    <div className="card">
      {image && <img src={image} alt={title} className="card-image" />}
      <div className="card-content">
        <h3 className="card-title">{title}</h3>
        <p className="card-description">{description}</p>
        {actions && (
          <div className="card-actions">
            {actions.map((action, index) => (
              <button
                key={index}
                onClick={action.onClick}
                className="card-action-button"
              >
                {action.label}
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
```

### Tables

```typescript
// Table Component
interface TableProps {
  headers: string[]
  rows: string[][]
}

export default function Table({ headers, rows }: TableProps) {
  return (
    <div className="table-container">
      <table>
        <thead>
          <tr>
            {headers.map((header, index) => (
              <th key={index}>{header}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {row.split('|').map((cell, cellIndex) => (
                <td key={cellIndex}>{cell}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
```

---

## 5. Conversation Flow Design

### Conversation States

```typescript
// Conversation State Management
interface ConversationState {
  isActive: boolean
  isTyping: boolean
  hasError: boolean
  lastActivity: Date
}

export class ConversationManager {
  private state: ConversationState = {
    isActive: false,
    isTyping: false,
    hasError: false,
    lastActivity: new Date(),
  }

  get isActive(): boolean {
    return this.state.isActive
  }

  set isActive(value: boolean): void {
    this.state.isActive = value
    this.state.lastActivity = new Date()
  }

  get isTyping(): boolean {
    return this.state.isTyping
  }

  set isTyping(value: boolean): void {
    this.state.isTyping = value
    if (value) {
      this.state.lastActivity = new Date()
    }
  }

  get hasError(): boolean {
    return this.state.hasError
  }

  setError(value: boolean): void {
    this.state.hasError = value
  }

  get lastActivity(): Date {
    return this.state.lastActivity
  }

  updateActivity(): void {
    this.state.lastActivity = new Date()
  }
}
```

### Conversation Flow

```typescript
// Conversation Flow
interface ConversationFlow {
  states: string[]
  transitions: Record<string, string[]>
}

const conversationFlow: ConversationFlow = {
  states: ['idle', 'active', 'typing', 'error', 'completed'],
  transitions: {
    idle: ['active', 'error'],
    active: ['idle', 'typing', 'completed', 'error'],
    typing: ['active', 'idle', 'error'],
    error: ['idle', 'active'],
    completed: ['idle'],
  },
}

class ConversationFlowManager {
  private currentState: string = 'idle'
  private flow: ConversationFlow = conversationFlow

  getCurrentState(): string {
    return this.currentState
  }

  transition(newState: string): boolean {
    const allowedTransitions = this.flow.transitions[this.currentState]
    
    if (!allowedTransitions.includes(newState)) {
      return false
    }
    
    this.currentState = newState
    return true
  }
}
```

---

## 6. Error Handling

### Error Display

```typescript
// Error Component
interface ErrorProps {
  error: {
    message: string
    code?: string
    details?: string
  }
  onRetry?: () => void
  onDismiss?: () => void
}

export default function Error({ error, onRetry, onDismiss }: ErrorProps) {
  return (
    <div className="error-message">
      <div className="error-icon">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 2v12a10 10 10 10H12M12 12 2a10 10 10 10H12" />
        </svg>
      </div>
      <div className="error-content">
        <h3 className="error-title">Something went wrong</h3>
        <p className="error-message">{error.message}</p>
        {error.details && (
          <details className="error-details">
            <summary>Details</summary>
            <pre className="error-details-content">{error.details}</pre>
          </details>
        )}
      </div>
      <div className="error-actions">
        {onRetry && (
          <button onClick={onRetry} className="error-button error-retry">
            Try Again
          </button>
        )}
        <button onClick={onDismiss} className="error-button error-dismiss">
          Dismiss
        </button>
      </div>
    </div>
  )
}
```

### Error Recovery

```typescript
// Error Recovery Component
interface ErrorRecoveryProps {
  error: Error
  onRetry?: () => void
  onAlternative?: () => void
}

export default function ErrorRecovery({ error, onRetry, onAlternative }: ErrorRecoveryProps) {
  return (
    <div className="error-recovery">
      <h2 className="error-recovery-title">We encountered an error</h2>
      <p className="error-recovery-message">{error.message}</p>
      <div className="error-recovery-suggestions">
        <h3>What would you like to do?</h3>
        <button onClick={onRetry} className="recovery-option">
          Try again
        </button>
        {onAlternative && (
          <button onClick={onAlternative} className="recovery-option">
          Try a different approach
          </button>
        )}
        <button onClick={() => window.location.reload()} className="recovery-option">
          Refresh page
        </button>
      </div>
    </div>
  )
}
```

---

## 7. Context Switching

### Context Manager

```typescript
// Context Manager
interface ConversationContext {
  id: string
  title: string
  messages: Message[]
  metadata: Record<string, any>
  createdAt: Date
  updatedAt: Date
}

interface Message {
  id: string
  role: 'user' | 'assistant' | 'system'
  content: string
  timestamp: Date
  metadata?: any
}

class ContextManager {
  private contexts: Map<string, ConversationContext> = new Map()

  createContext(id: string, title?: string): ConversationContext {
    const context: ConversationContext = {
      id: id || Date.now().toString(),
      title: title || 'New Conversation',
      messages: [],
      metadata: {},
      createdAt: new Date(),
      updatedAt: new Date(),
    }

    this.contexts.set(context.id, context)
    return context
  }

  getContext(id: string): ConversationContext | undefined {
    return this.contexts.get(id)
  }

  addMessage(contextId: string, message: Message): void {
    const context = this.getContext(contextId)
    if (context) {
      context.messages.push(message)
      context.updatedAt = new Date()
      this.contexts.set(contextId, context)
    }
  }

  getContextMessages(contextId: string): Message[] {
    const context = this.getContext(contextId)
    return context?.messages || []
  }

  switchContext(contextId: string): void {
    this.currentContextId = contextId
  }

  private currentContextId: string = 'default'

  deleteContext(id: string): void {
    this.contexts.delete(id)
    if (this.currentContextId === id) {
      this.currentContextId = 'default'
    }
  }
}
```

### Context Switcher Component

```typescript
// Context Switcher Component
'use client'

import { useState } from 'react'

interface ContextSwitcherProps {
  contexts: Array<{
    id: string
    title: string
    messageCount: number
  }>
  onSwitch: (contextId: string) => void
}

export default function ContextSwitcher({ contexts, onSwitch }: ContextSwitcherProps) {
  const [activeContext, setActiveContext] = useState(contexts[0].id)

  const handleSwitch = (contextId: string) => {
    setActiveContext(contextId)
    onSwitch(contextId)
  }

  return (
    <div className="context-switcher">
      {contexts.map(context => (
        <button
          key={context.id}
          className={`context-item ${activeContext === context.id ? 'active' : ''}`}
          onClick={() => handleSwitch(context.id)}
        >
          <span className="context-title">{context.title}</span>
          <span className="context-count">({context.messageCount})</span>
        </button>
      ))}
    </div>
  )
}
```

---

## 8. Personality and Tone

### Personality Definition

```typescript
// Personality Configuration
interface Personality {
  name: string
  description: string
  tone: 'formal' | 'casual' | 'friendly' | 'professional'
  traits: string[]
}

const personalities: Record<string, Personality> = {
  professional: {
    name: 'Professional',
    description: 'Professional and efficient',
    tone: 'formal',
    traits: [
      'Concise and direct',
      'Focuses on facts',
      'Avoids slang and humor',
      'Uses proper grammar',
      'Provides clear explanations',
    ],
  },
  friendly: {
    name: 'Friendly',
    description: 'Warm and approachable',
    tone: 'casual',
    traits: [
      'Uses emojis appropriately',
      'Shows empathy',
      'Uses conversational language',
      'Asks clarifying questions',
      'Provides helpful suggestions',
    ],
  },
  casual: {
    name: 'Casual',
    description: 'Relaxed and informal',
    tone: 'casual',
    traits: [
      'Uses informal language',
      'Uses emojis and slang',
      'Shows personality',
      'Uses humor appropriately',
      'Engages in small talk',
    ],
  },
}

// Personality Selector
interface PersonalitySelectorProps {
  personality: Personality
  onPersonalityChange: (personality: Personality) => void
}

export default function PersonalitySelector({ personality, onPersonalityChange }: PersonalitySelectorProps) {
  const options = Object.values(personalities)

  return (
    <div className="personality-selector">
      <h3>Choose your AI assistant personality</h3>
      <div className="personality-options">
        {options.map(option => (
          <button
            key={option.name}
            className={`personality-option ${personality.name === option.name ? 'selected' : ''}`}
            onClick={() => onPersonalityChange(option)}
          >
            <div className="personality-info">
              <div className="personality-name">{option.name}</div>
              <div className="personality-description">{option.description}</div>
              <div className="personality-tone">Tone: {option.tone}</div>
            </div>
          </button>
        ))}
      </div>
    </div>
  )
}
```

---

## 9. Accessibility

### Accessibility Features

```typescript
// Accessible Chat Component
'use client'

import { useState, useRef, useEffect } from 'react'

interface AccessibleChatProps {
  messages: Array<{
    id: string
    role: 'user' | 'assistant' | 'system'
    content: string
  }>
  onSendMessage: (message: string) => void
}

export default function AccessibleChat({ messages, onSendMessage }: AccessibleChatProps) {
  const [input, setInput] = useState('')
  const [isFocused, setIsFocused] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (input.trim()) {
      onSendMessage(input)
      setInput('')
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const sendMessage = () => {
    messagesEndRef.current?.focus()
    setIsFocused(true)
  }

  return (
    <div className="accessible-chat">
      <div
        ref={messagesEndRef}
        className="messages-container"
        role="log"
        aria-live="polite"
        aria-label="Chat messages"
      >
        {messages.map(message => (
          <div
            key={message.id}
            className={`message ${message.role}`}
            data-role={message.role}
          >
            <div className="message-content">
              {message.content}
            </div>
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit} className="chat-input-form">
        <label htmlFor="chat-input">Type your message</label>
        <input
          id="chat-input"
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type a message..."
          aria-label="Chat input"
          disabled={!isFocused}
        />
        <button
          type="button"
          onClick={sendMessage}
          disabled={!isFocused}
        >
          Send
        </button>
      </form>
    </div>
  )
}
```

### Keyboard Navigation

```typescript
// Keyboard Navigation Hook
'use client'

export function useKeyboardNavigation() {
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      // Ctrl/Cmd + K to focus input
      if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
        event.preventDefault()
        const input = document.getElementById('chat-input') as HTMLInputElement
        input?.focus()
      }

      // Escape to clear focus
      if (event.key === 'Escape') {
        const input = document.getElementById('chat-input') as HTMLInputElement
        input?.blur()
      }

      // Tab to switch focus
      if (event.key === 'Tab') {
        event.preventDefault()
        // Tab navigation between messages
      }
    }

    document.addEventListener('keydown', handleKeyDown)

    return () => {
      document.removeEventListener('keydown', handleKeyDown)
    }
  }, [])
}
```

### Screen Reader Support

```typescript
// Screen Reader Announcements
interface AnnouncerProps {
  message: string
  role: 'user' | 'assistant' | 'system'
}

export function announceMessage(message: string, role: string): void {
  const announcement = `${role}: ${message}`
  
  // Use ARIA live regions for dynamic content
  const announcer = document.getElementById('chat-announcer') as HTMLElement
  if (announcer) {
    announcer.textContent = announcement
  }
}
```

---

## 10. Mobile Considerations

### Mobile-Optimized UI

```typescript
// Mobile-Optimized Chat Component
'use client'

import { useState } from 'react'

interface MobileChatProps {
  messages: Array<{
    id: string
    role: 'user' | 'assistant' | 'system'
    content: string
  }>
  onSendMessage: (message: string) => void
}

export default function MobileChat({ messages, onSendMessage }: MobileChatProps) {
  const [isKeyboardOpen, setIsKeyboardOpen] = useState(false)
  const [input, setInput] = useState('')

  const handleSubmit = () => {
    if (input.trim()) {
      onSendMessage(input)
      setInput('')
    }
  }

  return (
    <div className="mobile-chat">
      <div className="messages-container">
        {messages.map(message => (
          <div
            key={message.id}
            className={`message ${message.role}`}
          >
            <div className="message-content">
              {message.content}
            </div>
          </div>
        ))}
      </div>
      <div className="mobile-input-container">
        {!isKeyboardOpen && (
          <button
            onClick={() => setIsKeyboardOpen(true)}
            className="keyboard-toggle"
          >
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 3.5 12 5 12 5 12H12M17 3.5 12 5 12H12" />
            </svg>
          </button>
        )}
        {isKeyboardOpen && (
          <form onSubmit={handleSubmit} className="mobile-input-form">
            <input
              type="text"
              value={input}
              onChange={e => setInput(e.target.value)}
              placeholder="Type a message..."
              autoFocus
            />
            <button
              type="submit"
              className="send-button"
            >
              Send
            </button>
            <button
              type="button"
              onClick={() => setIsKeyboardOpen(false)}
              className="close-button"
            >
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6-6 6 6H18" />
              </svg>
            </button>
          </form>
        )}
      </div>
    </div>
  )
}
```

### Touch-Friendly Interface

```typescript
// Touch-Friendly Components
'use client'

interface TouchButtonProps {
  onClick: () => void
  disabled?: boolean
  children: React.ReactNode
}

export default function TouchButton({ onClick, disabled, children }: TouchButtonProps) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className="touch-button"
      style={{
        minHeight: '44px',
        minWidth: '44px',
        padding: '12px 24px',
      }}
    >
      {children}
    </button>
  )
}
```

---

## 11. Testing Conversational Flows

### Testing Checklist

```markdown
# Conversational Flow Testing Checklist

## User Journey Testing
- [ ] User can start a conversation
- [ ] User can send messages
- [ ] User can receive responses
- [ ] User can handle errors
- [ ] User can switch contexts
- [ ] User can end conversation

## Edge Cases
- [ ] Empty message handling
- [ ] Very long messages
- [ ] Special characters
- [ ] Rapid sending
- [ ] Network disconnection
- [ ] Server errors
- [ ] Timeout scenarios

## Error Scenarios
- [ ] Invalid input
- [ ] API failures
- [ ] Network errors
- [ ] Timeouts
- [ ] Rate limits
- [ ] Authentication failures

## Multi-User Testing
- [ ] Multiple concurrent conversations
- [ ] Context isolation
- [ ] Message routing
- [ ] State management

## Mobile Testing
- [ ] Touch interactions
- [ ] Keyboard support
- [ ] Screen reader compatibility
- [ ] Performance on slow networks
- [ ] Responsive design
```

### User Testing Script

```typescript
// User Testing Script
const testCases = [
  {
    name: 'Basic Conversation',
    steps: [
      'Navigate to chat page',
      'Send "Hello"',
      'Verify response received',
      'Send "What is the weather?"',
      'Verify response received',
      'End conversation',
    ],
  },
  {
    name: 'Error Recovery',
    steps: [
      'Navigate to chat page',
      'Send invalid input',
      'Verify error message displayed',
      'Click "Try Again"',
      'Verify retry works',
    ],
  },
  {
    name: 'Context Switching',
    steps: [
      'Navigate to chat page',
      'Send "Start conversation 1"',
      'Receive response',
      'Click "Start conversation 2"',
      'Verify context switched',
      'Send message in new context',
      'Verify response in new context',
    ],
  },
  {
    name: 'Mobile Experience',
    steps: [
      'Open chat on mobile',
      'Tap to focus input',
      'Type message',
      'Send message',
      'Verify response',
      'Scroll through conversation',
      'Send another message',
      'Verify both messages visible',
    ],
  },
]

// Execute test
async function runTestCases() {
  for (const testCase of testCases) {
    console.log(`\n=== Testing: ${testCase.name} ===`)
    
    for (const step of testCase.steps) {
      console.log(`Step: ${step}`)
      // Execute step and verify
      await new Promise(resolve => setTimeout(resolve, 1000))
    }
  }
}
```

---

## 12. Best Practices

### Conversational UI Best Practices

```markdown
# Conversational UI Best Practices

## 1. User-Centric Design
- Focus on user needs
- Make interactions natural
- Provide helpful guidance
- Anticipate user intent

## 2. Clear Communication
- Be concise and clear
- Avoid technical jargon
- Provide context
- Ask clarifying questions

## 3. Responsive Feedback
- Show typing indicators
- Provide status updates
- Handle errors gracefully
- Acknowledge user actions

## 4. Context Awareness
- Maintain conversation history
- Reference previous messages
- Understand user's knowledge level
- Adapt explanations accordingly

## 5. Error Recovery
- Provide helpful error messages
- Suggest alternatives
- Allow easy recovery
- Learn from mistakes

## 6. Performance Optimization
- Minimize re-renders
- Use virtualization
- Implement lazy loading
- Optimize bundle size

## 7. Accessibility
- Support keyboard navigation
- Screen reader compatible
- High contrast ratios
- Clear focus indicators
- ARIA labels

## 8. Mobile First
- Touch-friendly interface
- Responsive design
- Fast load times
- Optimized for touch

## 9. State Management
- Maintain conversation state
- Handle connection states
- Manage loading states
- Persist conversations

## 10. Testing and Iteration
- Test with real users
- Gather feedback
- Analyze usage patterns
- Iterate and improve

## 11. Privacy and Security
- Protect user data
- Implement authentication
- Use secure communication
- Follow privacy regulations

## 12. Analytics and Monitoring
- Track user interactions
- Measure engagement
- Identify pain points
- Optimize based on data
```

---

## Quick Reference

### Component Templates

```markdown
# Component Quick Reference

## Message Bubble Template
```
<div className={`message ${role}`}>
  <div className="message-content">
    {content}
  </div>
  <div className="message-metadata">
    <span className="timestamp">{timestamp}</span>
  </div>
</div>
```

## Input Field Template
```
<form onSubmit={handleSubmit}>
  <input
    type="text"
    value={input}
    onChange={handleChange}
    onKeyDown={handleKeyDown}
    placeholder="Type a message..."
    disabled={disabled}
  />
  <button type="submit" disabled={disabled}>
    Send
  </button>
</form>
```

## Typing Indicator Template
```
<div className="typing-indicator">
  <span className="dot"></span>
  <span className="dot"></span>
  <span className="dot"></span>
</div>
```

## Error Message Template
```
<div className="error-message">
  <div className="error-icon">
    <svg>...</svg>
  </div>
  <div className="error-content">
    <h3>Error Title</h3>
    <p>Error message</p>
    <div className="error-actions">
      <button onClick={onRetry}>Try Again</button>
      <button onClick={onDismiss}>Dismiss</button>
    </div>
  </div>
</div>
```
```
