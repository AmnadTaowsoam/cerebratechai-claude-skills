---
name: Collaborative Editing
description: Enabling multiple users to edit the same document simultaneously using Operational Transformation, CRDTs, and implementation with Yjs for conflict-free collaborative editing.
---

# Collaborative Editing

> **Current Level:** Advanced  
> **Domain:** Real-time / Collaboration

---

## Overview

Collaborative editing enables multiple users to edit the same document simultaneously. This guide covers Operational Transformation, CRDTs, and implementation with Yjs for building real-time collaborative editors that handle concurrent edits without conflicts.

## Collaborative Editing Concepts

```
User A: "Hello"  →  Server  →  User B: "Hello"
User A: "Hello!" ←  Sync   ←  User B: "Hello World"
Result: "Hello World!"
```

**Challenges:**
- Concurrent edits
- Conflict resolution
- Network latency
- User presence
- Cursor synchronization

## Operational Transformation (OT)

```typescript
// Simple OT implementation
class Operation {
  constructor(
    public type: 'insert' | 'delete',
    public position: number,
    public content?: string
  ) {}
}

function transform(op1: Operation, op2: Operation): Operation {
  if (op1.type === 'insert' && op2.type === 'insert') {
    if (op1.position < op2.position) {
      return op2; // No change needed
    } else {
      // Adjust position
      return new Operation(
        op2.type,
        op2.position + (op1.content?.length || 0),
        op2.content
      );
    }
  }

  if (op1.type === 'delete' && op2.type === 'insert') {
    if (op1.position < op2.position) {
      return new Operation(
        op2.type,
        op2.position - 1,
        op2.content
      );
    }
  }

  // More transformation rules...
  return op2;
}
```

## CRDT (Conflict-free Replicated Data Types)

```typescript
// Simple CRDT character implementation
interface Character {
  id: string;
  value: string;
  position: number[];
  userId: string;
  timestamp: number;
}

class CRDTDocument {
  private characters: Character[] = [];

  insert(char: Character): void {
    const index = this.findInsertIndex(char.position);
    this.characters.splice(index, 0, char);
  }

  delete(charId: string): void {
    const index = this.characters.findIndex(c => c.id === charId);
    if (index !== -1) {
      this.characters.splice(index, 1);
    }
  }

  toString(): string {
    return this.characters.map(c => c.value).join('');
  }

  private findInsertIndex(position: number[]): number {
    // Binary search based on position
    let left = 0;
    let right = this.characters.length;

    while (left < right) {
      const mid = Math.floor((left + right) / 2);
      if (this.comparePositions(this.characters[mid].position, position) < 0) {
        left = mid + 1;
      } else {
        right = mid;
      }
    }

    return left;
  }

  private comparePositions(pos1: number[], pos2: number[]): number {
    const minLength = Math.min(pos1.length, pos2.length);
    
    for (let i = 0; i < minLength; i++) {
      if (pos1[i] !== pos2[i]) {
        return pos1[i] - pos2[i];
      }
    }

    return pos1.length - pos2.length;
  }
}
```

## Yjs Library

```typescript
// Install: npm install yjs y-websocket

import * as Y from 'yjs';
import { WebsocketProvider } from 'y-websocket';

// Create shared document
const ydoc = new Y.Doc();

// Create shared text type
const ytext = ydoc.getText('content');

// Connect to WebSocket server
const provider = new WebsocketProvider(
  'ws://localhost:1234',
  'my-document',
  ydoc
);

// Listen to changes
ytext.observe((event) => {
  console.log('Text changed:', event);
  console.log('Current text:', ytext.toString());
});

// Make changes
ytext.insert(0, 'Hello ');
ytext.insert(6, 'World');

// Delete text
ytext.delete(0, 5);

// Get awareness (user presence)
const awareness = provider.awareness;

awareness.setLocalStateField('user', {
  name: 'John Doe',
  color: '#ff0000'
});

awareness.on('change', () => {
  console.log('Awareness changed:', awareness.getStates());
});
```

## TipTap Editor Integration

```typescript
// Install: npm install @tiptap/react @tiptap/starter-kit @tiptap/extension-collaboration

import { useEditor, EditorContent } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';
import Collaboration from '@tiptap/extension-collaboration';
import CollaborationCursor from '@tiptap/extension-collaboration-cursor';
import * as Y from 'yjs';
import { WebsocketProvider } from 'y-websocket';

function CollaborativeEditor({ documentId, user }: EditorProps) {
  const ydoc = useMemo(() => new Y.Doc(), []);

  const provider = useMemo(
    () => new WebsocketProvider(
      'ws://localhost:1234',
      documentId,
      ydoc
    ),
    [documentId, ydoc]
  );

  const editor = useEditor({
    extensions: [
      StarterKit.configure({
        history: false // Disable default history
      }),
      Collaboration.configure({
        document: ydoc
      }),
      CollaborationCursor.configure({
        provider,
        user: {
          name: user.name,
          color: user.color
        }
      })
    ]
  });

  useEffect(() => {
    return () => {
      provider.destroy();
      ydoc.destroy();
    };
  }, [provider, ydoc]);

  return (
    <div>
      <EditorContent editor={editor} />
      <UserList provider={provider} />
    </div>
  );
}

interface EditorProps {
  documentId: string;
  user: {
    name: string;
    color: string;
  };
}
```

## WebSocket Server (Yjs)

```typescript
// server.ts
import { WebSocketServer } from 'ws';
import { setupWSConnection } from 'y-websocket/bin/utils';

const wss = new WebSocketServer({ port: 1234 });

wss.on('connection', (ws, req) => {
  setupWSConnection(ws, req);
});

console.log('Yjs WebSocket server running on port 1234');

// With authentication
wss.on('connection', (ws, req) => {
  const token = new URL(req.url!, 'ws://localhost').searchParams.get('token');
  
  if (!verifyToken(token)) {
    ws.close(1008, 'Unauthorized');
    return;
  }

  setupWSConnection(ws, req);
});
```

## Cursor Position Sharing

```typescript
// components/CollaborativeCursor.tsx
import { useEffect, useState } from 'react';

interface CursorPosition {
  userId: string;
  userName: string;
  color: string;
  position: { x: number; y: number };
}

function CollaborativeCursors({ provider }: { provider: WebsocketProvider }) {
  const [cursors, setCursors] = useState<CursorPosition[]>([]);

  useEffect(() => {
    const awareness = provider.awareness;

    const updateCursors = () => {
      const states = Array.from(awareness.getStates().entries());
      const cursorPositions = states
        .filter(([clientId]) => clientId !== awareness.clientID)
        .map(([clientId, state]) => ({
          userId: clientId.toString(),
          userName: state.user?.name || 'Anonymous',
          color: state.user?.color || '#000000',
          position: state.cursor || { x: 0, y: 0 }
        }));

      setCursors(cursorPositions);
    };

    awareness.on('change', updateCursors);
    updateCursors();

    return () => {
      awareness.off('change', updateCursors);
    };
  }, [provider]);

  return (
    <>
      {cursors.map((cursor) => (
        <div
          key={cursor.userId}
          className="cursor"
          style={{
            position: 'absolute',
            left: cursor.position.x,
            top: cursor.position.y,
            pointerEvents: 'none'
          }}
        >
          <svg width="20" height="20">
            <path
              d="M0 0 L0 16 L6 12 L9 18 L11 17 L8 11 L14 11 Z"
              fill={cursor.color}
            />
          </svg>
          <span
            style={{
              backgroundColor: cursor.color,
              color: 'white',
              padding: '2px 6px',
              borderRadius: '4px',
              fontSize: '12px',
              marginLeft: '20px'
            }}
          >
            {cursor.userName}
          </span>
        </div>
      ))}
    </>
  );
}
```

## User Presence

```typescript
// hooks/usePresence.ts
import { useEffect, useState } from 'react';
import { WebsocketProvider } from 'y-websocket';

interface User {
  id: string;
  name: string;
  color: string;
  cursor?: { x: number; y: number };
}

export function usePresence(provider: WebsocketProvider) {
  const [users, setUsers] = useState<User[]>([]);

  useEffect(() => {
    const awareness = provider.awareness;

    const updateUsers = () => {
      const states = Array.from(awareness.getStates().entries());
      const activeUsers = states
        .filter(([clientId]) => clientId !== awareness.clientID)
        .map(([clientId, state]) => ({
          id: clientId.toString(),
          name: state.user?.name || 'Anonymous',
          color: state.user?.color || '#000000',
          cursor: state.cursor
        }));

      setUsers(activeUsers);
    };

    awareness.on('change', updateUsers);
    updateUsers();

    return () => {
      awareness.off('change', updateUsers);
    };
  }, [provider]);

  return users;
}

// Usage
function UserList({ provider }: { provider: WebsocketProvider }) {
  const users = usePresence(provider);

  return (
    <div className="user-list">
      <h3>Active Users ({users.length})</h3>
      {users.map((user) => (
        <div key={user.id} className="user">
          <div
            className="user-avatar"
            style={{ backgroundColor: user.color }}
          />
          <span>{user.name}</span>
        </div>
      ))}
    </div>
  );
}
```

## Saving and Persistence

```typescript
// services/document-persistence.service.ts
import * as Y from 'yjs';

export class DocumentPersistenceService {
  async saveDocument(documentId: string, ydoc: Y.Doc): Promise<void> {
    const state = Y.encodeStateAsUpdate(ydoc);
    
    await db.document.upsert({
      where: { id: documentId },
      create: {
        id: documentId,
        content: Buffer.from(state)
      },
      update: {
        content: Buffer.from(state),
        updatedAt: new Date()
      }
    });
  }

  async loadDocument(documentId: string): Promise<Uint8Array | null> {
    const doc = await db.document.findUnique({
      where: { id: documentId }
    });

    return doc ? new Uint8Array(doc.content) : null;
  }

  async applyUpdate(documentId: string, update: Uint8Array): Promise<void> {
    const doc = await this.loadDocument(documentId);
    
    if (doc) {
      const ydoc = new Y.Doc();
      Y.applyUpdate(ydoc, doc);
      Y.applyUpdate(ydoc, update);
      
      await this.saveDocument(documentId, ydoc);
    }
  }
}

// Auto-save on changes
ydoc.on('update', async (update: Uint8Array) => {
  await documentPersistenceService.applyUpdate(documentId, update);
});
```

## Performance Optimization

```typescript
// Debounce updates
import { debounce } from 'lodash';

const debouncedSave = debounce(async (documentId: string, ydoc: Y.Doc) => {
  await documentPersistenceService.saveDocument(documentId, ydoc);
}, 2000);

ydoc.on('update', () => {
  debouncedSave(documentId, ydoc);
});

// Lazy loading
const editor = useEditor({
  extensions: [
    StarterKit,
    Collaboration.configure({
      document: ydoc,
      field: 'content'
    })
  ],
  editorProps: {
    attributes: {
      class: 'prose max-w-none'
    }
  },
  onCreate: ({ editor }) => {
    // Load initial content
    loadInitialContent(editor);
  }
});

// Optimize rendering
const MemoizedEditor = memo(EditorContent);
```

## Example Implementation

```typescript
// pages/document/[id].tsx
import { useState, useEffect, useMemo } from 'react';
import * as Y from 'yjs';
import { WebsocketProvider } from 'y-websocket';
import { useEditor, EditorContent } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';
import Collaboration from '@tiptap/extension-collaboration';
import CollaborationCursor from '@tiptap/extension-collaboration-cursor';

export default function DocumentPage({ documentId, user }: Props) {
  const ydoc = useMemo(() => new Y.Doc(), []);
  const [provider, setProvider] = useState<WebsocketProvider | null>(null);

  useEffect(() => {
    const wsProvider = new WebsocketProvider(
      process.env.NEXT_PUBLIC_WS_URL!,
      documentId,
      ydoc,
      {
        params: { token: user.token }
      }
    );

    setProvider(wsProvider);

    return () => {
      wsProvider.destroy();
      ydoc.destroy();
    };
  }, [documentId, ydoc, user.token]);

  const editor = useEditor({
    extensions: [
      StarterKit,
      Collaboration.configure({
        document: ydoc
      }),
      CollaborationCursor.configure({
        provider: provider!,
        user: {
          name: user.name,
          color: user.color
        }
      })
    ]
  });

  if (!provider || !editor) {
    return <div>Loading...</div>;
  }

  return (
    <div className="collaborative-editor">
      <Toolbar editor={editor} />
      <UserList provider={provider} />
      <EditorContent editor={editor} />
      <CollaborativeCursors provider={provider} />
    </div>
  );
}

interface Props {
  documentId: string;
  user: {
    name: string;
    color: string;
    token: string;
  };
}
```

## Best Practices

1. **Conflict Resolution** - Use CRDTs or OT
2. **Persistence** - Save documents regularly
3. **Performance** - Debounce updates
4. **User Presence** - Show active users
5. **Cursors** - Display user cursors
6. **Authentication** - Secure WebSocket connections
7. **Error Handling** - Handle connection errors
8. **Offline Support** - Support offline editing
9. **Version History** - Track document versions
10. **Testing** - Test with multiple users

---

## Quick Start

### Yjs Integration

```javascript
import * as Y from 'yjs'
import { WebsocketProvider } from 'y-websocket'

// Create Yjs document
const ydoc = new Y.Doc()

// Connect via WebSocket
const provider = new WebsocketProvider(
  'ws://localhost:1234',
  'room-name',
  ydoc
)

// Create text type
const ytext = ydoc.getText('content')

// Observe changes
ytext.observe(event => {
  console.log('Content changed:', ytext.toString())
})

// Update content
ytext.insert(0, 'Hello')
```

---

## Production Checklist

- [ ] **Conflict Resolution**: CRDT or OT implementation
- [ ] **WebSocket**: WebSocket connection for real-time sync
- [ ] **User Presence**: Show user cursors and selections
- [ ] **Authentication**: Authenticate WebSocket connections
- [ ] **Error Handling**: Handle connection errors
- [ ] **Offline Support**: Support offline editing
- [ ] **Version History**: Track document versions
- [ ] **Performance**: Optimize for large documents
- [ ] **Testing**: Test with multiple concurrent users
- [ ] **Documentation**: Document collaboration features
- [ ] **Monitoring**: Monitor collaboration performance
- [ ] **Security**: Secure collaborative editing

---

## Anti-patterns

### ❌ Don't: No Conflict Resolution

```javascript
// ❌ Bad - Last write wins
function updateDocument(userId, content) {
  document.content = content  // Overwrites other users' changes!
}
```

```javascript
// ✅ Good - CRDT for conflict-free
const ytext = ydoc.getText('content')
ytext.insert(0, 'Hello')  // CRDT handles conflicts automatically
```

### ❌ Don't: No User Presence

```markdown
# ❌ Bad - No indication of other users
User A: Editing document
User B: Also editing (but doesn't know!)
```

```markdown
# ✅ Good - Show user presence
User A: Editing document
User B: Sees "User A is editing" and cursor position
```

---

## Integration Points

- **WebSocket Patterns** (`34-real-time-features/websocket-patterns/`) - WebSocket implementation
- **Presence Detection** (`34-real-time-features/presence-detection/`) - User presence
- **Real-time Dashboard** (`34-real-time-features/real-time-dashboard/`) - Real-time updates

---

## Further Reading

- [Yjs](https://docs.yjs.dev/)
- [TipTap](https://tiptap.dev/)
- [Operational Transformation](https://en.wikipedia.org/wiki/Operational_transformation)
- [CRDTs](https://crdt.tech/)
- [ProseMirror](https://prosemirror.net/)
- [Quill](https://quilljs.com/)
- [Operational Transformation](https://en.wikipedia.org/wiki/Operational_transformation)
