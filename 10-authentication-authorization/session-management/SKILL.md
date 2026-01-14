# Session Management

## Overview

Comprehensive guide to session management patterns for web applications.

## Table of Contents

1. [Session vs Token-Based Auth](#session-vs-token-based-auth)
2. [Server-Side Sessions](#server-side-sessions)
3. [Session Lifecycle](#session-lifecycle)
4. [Session Fixation Prevention](#session-fixation-prevention)
5. [CSRF Protection](#csrf-protection)
6. [Session Timeout](#session-timeout)
7. [Remember Me Functionality](#remember-me-functionality)
8. [Concurrent Session Handling](#concurrent-session-handling)
9. [Session Migration](#session-migration)
10. [Security Best Practices](#security-best-practices)

---

## Session vs Token-Based Auth

### Comparison

```markdown
## Session vs Token-Based Authentication

### Session-Based Auth
**Pros:**
- Server-controlled invalidation
- Easy to implement
- No storage on client
- Automatic cleanup

**Cons:**
- Server memory usage
- Scalability challenges
- Requires sticky sessions for horizontal scaling

**Use Cases:**
- Traditional web apps
- Simple applications
- Monolithic architectures

### Token-Based Auth (JWT)
**Pros:**
- Stateless servers
- Better scalability
- Works well with mobile/native apps
- Fine-grained permissions

**Cons:**
- Client-side storage concerns
- Token revocation complexity
- Larger payload size

**Use Cases:**
- REST APIs
- Mobile apps
- Microservices
- SPAs
```

### Decision Framework

```typescript
// auth-strategy-selector.ts
export interface AuthContext {
  applicationType: 'traditional' | 'spa' | 'mobile' | 'api';
  scaleRequirements: 'small' | 'medium' | 'large';
  securityLevel: 'standard' | 'high';
  sessionManagement: 'simple' | 'advanced';
}

export class AuthStrategySelector {
  static recommendStrategy(context: AuthContext): 'session' | 'token' | 'hybrid' {
    // Mobile apps always use tokens
    if (context.applicationType === 'mobile') {
      return 'token';
    }
    
    // APIs use tokens
    if (context.applicationType === 'api') {
      return 'token';
    }
    
    // SPAs use tokens
    if (context.applicationType === 'spa') {
      return 'token';
    }
    
    // Large scale needs tokens
    if (context.scaleRequirements === 'large') {
      return 'token';
    }
    
    // High security might need sessions for better control
    if (context.securityLevel === 'high' && context.sessionManagement === 'advanced') {
      return 'session';
    }
    
    // Default to sessions for traditional apps
    return 'session';
  }
}

// Usage
const strategy = AuthStrategySelector.recommendStrategy({
  applicationType: 'traditional',
  scaleRequirements: 'medium',
  securityLevel: 'standard',
  sessionManagement: 'simple'
});
```

---

## Server-Side Sessions

### Express Session

```typescript
// session-config.ts
import session from 'express-session';
import RedisStore from 'connect-redis';
import { createClient } from 'redis';

// Redis session store
const redisClient = createClient({
  host: process.env.REDIS_HOST || 'localhost',
  port: parseInt(process.env.REDIS_PORT || '6379'),
  password: process.env.REDIS_PASSWORD,
  db: parseInt(process.env.REDIS_DB || '0')
});

const sessionStore = new RedisStore({
  client: redisClient,
  prefix: 'sess:'
});

export const sessionConfig = {
  store: sessionStore,
  secret: process.env.SESSION_SECRET || 'your-secret-key',
  name: 'sessionId',
  resave: false,
  saveUninitialized: false,
  cookie: {
    httpOnly: true,    // Prevents XSS
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',   // CSRF protection
    maxAge: 24 * 60 * 60 * 1000, // 24 hours
    path: '/'
  }
};
```

### Session Middleware

```typescript
// session-middleware.ts
import express from 'express';
import { sessionConfig } from './session-config';

const app = express();

// Configure session
app.use(session(sessionConfig));

// Session routes
app.post('/login', async (req, res) => {
  const { email, password } = req.body;
  
  // Validate credentials
  const user = await validateCredentials(email, password);
  
  if (!user) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }
  
  // Set session data
  req.session.userId = user.id;
  req.session.userEmail = user.email;
  req.session.userRole = user.role;
  req.session.loginAt = new Date();
  
  // Regenerate session ID (prevents session fixation)
  req.session.regenerate(() => {
    res.json({ success: true, user: { id: user.id, email: user.email } });
  });
});

app.get('/api/me', (req, res) => {
  if (!req.session.userId) {
    return res.status(401).json({ error: 'Not authenticated' });
  }
  
  res.json({
    id: req.session.userId,
    email: req.session.userEmail,
    role: req.session.userRole
  });
});

app.post('/logout', (req, res) => {
  req.session.destroy((err) => {
    if (err) {
      console.error('Error destroying session:', err);
    }
  });
  
  res.json({ success: true });
});
```

### FastAPI Session

```python
# session_config.py
from fastapi import FastAPI, Request, Response, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.sessions import SessionMiddleware
from starlette.middleware.sessions import SessionMiddleware
from redis import Redis

app = FastAPI()

# Redis session store
redis = Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    password=os.getenv('REDIS_PASSWORD'),
    db=int(os.getenv('REDIS_DB', 0),
    decode_responses=True
)

# Session middleware
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv('SESSION_SECRET', 'your-secret-key'),
    session_cookie='session_id',
    max_age=24 * 60 * 60,  # 24 hours
    same_site='lax',
    https_only=True,
    httponly=True
)

@app.post('/login')
async def login(request: Request):
    """Login endpoint"""
    data = await request.json()
    email = data.get('email')
    password = data.get('password')
    
    # Validate credentials
    user = await validate_credentials(email, password)
    
    if not user:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    
    # Set session data
    request.session['user_id'] = user['id']
    request.session['user_email'] = user['email']
    request.session['user_role'] = user['role']
    request.session['login_at'] = datetime.utcnow().isoformat()
    
    # Regenerate session ID
    request.session.regenerate_id()
    
    return {'success': True, 'user': {'id': user['id'], 'email': user['email']}}

@app.get('/api/me')
async def get_me(request: Request):
    """Get current user"""
    user_id = request.session.get('user_id')
    
    if not user_id:
        raise HTTPException(status_code=401, detail='Not authenticated')
    
    return {
        'id': user_id,
        'email': request.session.get('user_email'),
        'role': request.session.get('user_role')
    }

@app.post('/logout')
async def logout(request: Request):
    """Logout endpoint"""
    # Clear session
    request.session.clear()
    
    return {'success': True}
```

---

## Session Lifecycle

### Session Events

```typescript
// session-lifecycle.ts
import session from 'express-session';

export class SessionLifecycle {
  static setup(app: express.Application): void {
    // Session creation
    app.use((req, res, next) => {
      req.sessionStore.on('create', (sessionId, session) => {
        console.log(`Session created: ${sessionId}`);
        this.onCreate(sessionId, session);
      });
      next();
    });
    
    // Session save
    app.use((req, res, next) => {
      const originalSend = res.send;
      res.send = function (chunk, encoding) {
        res.send = originalSend;
        res.send(chunk, encoding);
      };
      
      next();
    });
    
    // Session destruction
    app.use((req, res, next) => {
      req.sessionStore.on('destroy', (sessionId) => {
        console.log(`Session destroyed: ${sessionId}`);
        this.onDestroy(sessionId);
      });
      next();
    });
  }
  
  private static onCreate(sessionId: string, session: any): void {
    // Log session creation
    console.log(`Session created at ${new Date().toISOString()}`);
    
    // Track active sessions
    this.trackActiveSession(sessionId);
  }
  
  private static onDestroy(sessionId: string): void {
    // Log session destruction
    console.log(`Session destroyed at ${new Date().toISOString()}`);
    
    // Remove from active sessions
    this.removeActiveSession(sessionId);
  }
  
  private static trackActiveSession(sessionId: string): void {
    // Implementation - track in Redis or database
  }
  
  private static removeActiveSession(sessionId: string): void {
    // Implementation - remove from tracking
  }
}
```

### Session Cleanup

```typescript
// session-cleanup.ts
import cron from 'node-cron';

export class SessionCleanupService {
  constructor(private sessionStore: any) {}
  
  start(): void {
    // Clean up expired sessions every hour
    cron.schedule('0 * * * *', async () => {
      await this.cleanupExpiredSessions();
    });
    
    // Clean up idle sessions every 6 hours
    cron.schedule('0 */6 * * *', async () => {
      await this.cleanupIdleSessions();
    });
  }
  
  private async cleanupExpiredSessions(): Promise<void> {
    const expiredThreshold = new Date(Date.now() - 24 * 60 * 60 * 1000); // 24 hours
    
    // Get all sessions
    const sessions = await this.sessionStore.all((err, sessions) => {
      if (err) {
        console.error('Error getting sessions:', err);
        return;
      }
      
      // Destroy expired sessions
      for (const [sessionId, session] of Object.entries(sessions)) {
        if (session.cookie.expires < expiredThreshold) {
          this.sessionStore.destroy(sessionId, (err) => {
            if (err) {
              console.error(`Error destroying session ${sessionId}:`, err);
            } else {
              console.log(`Destroyed expired session: ${sessionId}`);
            }
          });
        }
      }
    });
  }
  
  private async cleanupIdleSessions(): Promise<void> {
    const idleThreshold = new Date(Date.now() - 6 * 60 * 60 * 1000); // 6 hours
    
    // Get all sessions
    const sessions = await this.sessionStore.all((err, sessions) => {
      if (err) {
        console.error('Error getting sessions:', err);
        return;
      }
      
      // Destroy idle sessions
      for (const [sessionId, session] of Object.entries(sessions)) {
        if (session.lastAccess < idleThreshold) {
          this.sessionStore.destroy(sessionId, (err) => {
            if (err) {
              console.error(`Error destroying session ${sessionId}:`, err);
            } else {
              console.log(`Destroyed idle session: ${sessionId}`);
            }
          });
        }
      }
    });
  }
}
```

---

## Session Fixation Prevention

### Session Regeneration

```typescript
// session-fixation.ts
import { Request, Response, NextFunction } from 'express';

export class SessionFixationPrevention {
  static setup(app: express.Application): void {
    // Regenerate session on login
    app.post('/login', this.regenerateSession.bind(this));
    
    // Regenerate session on privilege escalation
    app.post('/api/users/promote', this.requireAuth, this.regenerateSession.bind(this));
  }
  
  private regenerateSession(req: Request, res: Response, next: NextFunction): void {
    // Regenerate session ID
    req.session.regenerate((err) => {
      if (err) {
        console.error('Error regenerating session:', err);
        return next(err);
      }
      
      console.log(`Session regenerated: ${req.sessionID}`);
      next();
    });
  }
  
  private static requireAuth(req: Request, res: Response, next: NextFunction): void {
    if (!req.session.userId) {
      return res.status(401).json({ error: 'Not authenticated' });
    }
    next();
  }
}
```

---

## CSRF Protection

### CSRF Middleware

```typescript
// csrf-protection.ts
import crypto from 'crypto';
import { Request, Response, NextFunction } from 'express';

export class CSRFProtection {
  private static readonly TOKEN_LENGTH = 32;
  
  static generateToken(): string {
    return crypto.randomBytes(this.TOKEN_LENGTH).toString('hex');
  }
  
  static setup(app: express.Application): void {
    // Generate and store CSRF token
    app.get('/csrf-token', (req, res) => {
      const token = this.generateToken();
      req.session.csrfToken = token;
      res.json({ token });
    });
    
    // Validate CSRF token on state-changing requests
    app.use((req, res, next) => {
      const stateChangingMethods = ['POST', 'PUT', 'PATCH', 'DELETE'];
      
      if (stateChangingMethods.includes(req.method)) {
        const token = req.headers['x-csrf-token'] || req.body._csrf;
        const sessionToken = req.session.csrfToken;
        
        if (!token || !sessionToken || token !== sessionToken) {
          return res.status(403).json({ error: 'Invalid CSRF token' });
        }
      }
      
      next();
    });
  }
}

// Usage
CSRFProtection.setup(app);
```

### CSRF in Forms

```typescript
// csrf-form.ts
export class CSRFFormHelper {
  static generateHiddenField(token: string): string {
    return `<input type="hidden" name="_csrf" value="${token}" />`;
  }
  
  static generateForm(token: string, action: string, method: string = 'POST'): string {
    return `
      <form action="${action}" method="${method}">
        ${this.generateHiddenField(token)}
        <!-- Other form fields -->
        <button type="submit">Submit</button>
      </form>
    `;
  }
}

// Usage in template
// Get CSRF token
const csrfToken = await fetch('/csrf-token').then(r => r.json()).then(data => data.token);

// Generate form
const formHTML = CSRFFormHelper.generateForm(
  csrfToken,
  '/api/users',
  'POST'
);
```

---

## Session Timeout

### Timeout Configuration

```typescript
// session-timeout.ts
export interface SessionTimeoutConfig {
  idleTimeout: number;  // seconds of inactivity
  absoluteTimeout: number; // seconds from creation
  rollingTimeout: boolean; // Reset timer on activity
}

export const timeoutConfigs: Record<string, SessionTimeoutConfig> = {
  default: {
    idleTimeout: 30 * 60,      // 30 minutes
    absoluteTimeout: 24 * 60 * 60, // 24 hours
    rollingTimeout: true
  },
  short: {
    idleTimeout: 15 * 60,      // 15 minutes
    absoluteTimeout: 12 * 60 * 60, // 12 hours
    rollingTimeout: true
  },
  long: {
    idleTimeout: 60 * 60,      // 60 minutes
    absoluteTimeout: 7 * 24 * 60 * 60, // 7 days
    rollingTimeout: true
  }
};

export class SessionTimeoutManager {
  static setup(app: express.Application, config: SessionTimeoutConfig): void {
    app.use((req, res, next) => {
      const now = Date.now();
      
      // Check absolute timeout
      if (req.session.createdAt && (now - req.session.createdAt) > config.absoluteTimeout * 1000) {
        req.session.destroy(() => {
          console.log('Session expired due to absolute timeout');
        });
        return res.status(401).json({ error: 'Session expired' });
      }
      
      // Check idle timeout
      if (req.session.lastAccess && (now - req.session.lastAccess) > config.idleTimeout * 1000) {
        req.session.destroy(() => {
          console.log('Session expired due to inactivity');
        });
        return res.status(401).json({ error: 'Session expired' });
      }
      
      // Update last access time
      req.session.lastAccess = now;
      
      // Set creation time if not set
      if (!req.session.createdAt) {
        req.session.createdAt = now;
      }
      
      next();
    });
  }
}

// Usage
SessionTimeoutManager.setup(app, timeoutConfigs.default);
```

### Timeout Warning

```typescript
// session-timeout-warning.ts
export class SessionTimeoutWarning {
  static setup(app: express.Application): void {
    app.use((req, res, next) => {
      const warningThreshold = 5 * 60 * 1000; // 5 minutes
      
      // Check for timeout warning
      if (req.session.lastAccess) {
        const timeSinceActivity = Date.now() - req.session.lastAccess;
        
        if (timeSinceActivity > warningThreshold) {
          req.session.timeoutWarning = true;
        } else {
          req.session.timeoutWarning = false;
        }
      }
      
      next();
    });
  }
  
  static getWarningMessage(req: any): string | null {
    if (req.session?.timeoutWarning) {
      return 'Your session will expire soon due to inactivity';
    }
    return null;
  }
}

// Usage
app.get('/api/me', SessionTimeoutWarning.setup.bind(SessionTimeoutWarning), (req, res) => {
  const warning = SessionTimeoutWarning.getWarningMessage(req);
  
  const response = {
    user: req.session.userId,
    timeoutWarning: warning
  };
  
  res.json(response);
});
```

---

## Remember Me Functionality

### Remember Me Implementation

```typescript
// remember-me.ts
import { Request, Response, NextFunction } from 'express';

export class RememberMe {
  static setup(app: express.Application): void {
    // Login with remember me
    app.post('/login', async (req, res) => {
      const { email, password, remember } = req.body;
      
      // Validate credentials
      const user = await validateCredentials(email, password);
      
      if (!user) {
        return res.status(401).json({ error: 'Invalid credentials' });
      }
      
      // Set session data
      req.session.userId = user.id;
      req.session.userEmail = user.email;
      req.session.loginAt = new Date();
      
      // Set remember me cookie
      if (remember) {
        this.setRememberMeCookie(res, user.id, user.email);
      }
      
      req.session.regenerate(() => {
        res.json({ success: true, user: { id: user.id, email: user.email } });
      });
    });
    
    // Check remember me on login page load
    app.get('/api/remembered-user', (req, res) => {
      const rememberedUser = this.getRememberedUser(req);
      
      if (rememberedUser) {
        res.json({ remembered: true, user: rememberedUser });
      } else {
        res.json({ remembered: false });
      }
    });
  }
  
  private static setRememberMeCookie(res: Response, userId: string, email: string): void {
    const token = this.generateRememberToken(userId, email);
    
    res.cookie('remember_me', token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'strict',
      maxAge: 30 * 24 * 60 * 60 * 1000, // 30 days
      path: '/'
    });
  }
  
  private static getRememberedUser(req: Request): any | null {
    const token = req.cookies.remember_me;
    
    if (!token) return null;
    
    try {
      const payload = this.verifyRememberToken(token);
      return {
        id: payload.userId,
        email: payload.email
      };
    } catch (error) {
      return null;
    }
  }
  
  private static generateRememberToken(userId: string, email: string): string {
    const payload = {
      userId,
      email,
      exp: Math.floor(Date.now() / 1000) + 30 * 24 * 60 * 60 // 30 days
    };
    
    return Buffer.from(JSON.stringify(payload)).toString('base64');
  }
  
  private static verifyRememberToken(token: string): any {
    const payload = JSON.parse(Buffer.from(token, 'base64').toString());
    
    if (Date.now() / 1000 > payload.exp) {
      throw new Error('Token expired');
    }
    
    return payload;
  }
}

// Usage
RememberMe.setup(app);
```

---

## Concurrent Session Handling

### Concurrent Session Limit

```typescript
// concurrent-sessions.ts
export class ConcurrentSessionManager {
  private maxSessionsPerUser: number;
  
  constructor(maxSessionsPerUser: number = 3) {
    this.maxSessionsPerUser = maxSessionsPerUser;
  }
  
  async checkAndEnforceLimit(userId: string, currentSessionId: string): Promise<void> {
    const activeSessions = await this.getUserSessions(userId);
    
    if (activeSessions.length >= this.maxSessionsPerUser) {
      // Find oldest session
      const oldestSession = activeSessions.sort((a, b) => 
        a.createdAt - b.createdAt
      )[0];
      
      // Destroy oldest session
      await this.destroySession(oldestSession.sessionId);
    }
  }
  
  async getUserSessions(userId: string): Promise<any[]> {
    // Implementation - get all active sessions for user
    return [];
  }
  
  async destroySession(sessionId: string): Promise<void> {
    // Implementation - destroy session
  }
  
  async getActiveSessionCount(userId: string): Promise<number> {
    const sessions = await this.getUserSessions(userId);
    return sessions.length;
  }
}

// Middleware
export class ConcurrentSessionMiddleware {
  constructor(
    private sessionManager: ConcurrentSessionManager
  ) {}
  
  middleware() {
    return async (req: Request, res: Response, next: NextFunction) => {
      if (!req.session.userId) {
        return next();
      }
      
      // Check and enforce concurrent session limit
      await this.sessionManager.checkAndEnforceLimit(
        req.session.userId,
        req.sessionID
      );
      
      next();
    };
  }
}

// Usage
const sessionManager = new ConcurrentSessionManager(3);
const middleware = new ConcurrentSessionMiddleware(sessionManager);

app.use(middleware.middleware());
```

### Session List Management

```typescript
// session-list.ts
export class SessionListManager {
  async listUserSessions(userId: string): Promise<any[]> {
    // Implementation - get all sessions for user
    const sessions = await this.getSessionRepository.findByUserId(userId);
    
    return sessions.map(session => ({
      id: session.id,
      device: session.device,
      browser: session.browser,
      ipAddress: session.ipAddress,
      createdAt: session.createdAt,
      lastAccess: session.lastAccess,
      isCurrent: session.id === req.sessionID
    }));
  }
  
  async revokeSession(userId: string, sessionId: string): Promise<void> {
    // Verify ownership
    const session = await this.getSessionRepository.findById(sessionId);
    
    if (!session || session.userId !== userId) {
      throw new Error('Session not found or access denied');
    }
    
    // Destroy session
    await this.getSessionRepository.delete(sessionId);
  }
  
  async revokeAllSessions(userId: string): Promise<void> {
    await this.getSessionRepository.deleteByUserId(userId);
  }
}

// API routes
app.get('/api/sessions', async (req, res) => {
  if (!req.session.userId) {
    return res.status(401).json({ error: 'Not authenticated' });
  }
  
  const sessions = await sessionListManager.listUserSessions(req.session.userId);
  res.json(sessions);
});

app.delete('/api/sessions/:id', async (req, res) => {
  if (!req.session.userId) {
    return res.status(401).json({ error: 'Not authenticated' });
  }
  
  await sessionListManager.revokeSession(req.session.userId, req.params.id);
  res.status(204).send();
});
```

---

## Session Migration

### Session Migration Strategy

```typescript
// session-migration.ts
export class SessionMigrator {
  async migrateSessions(oldStore: any, newStore: any): Promise<void> {
    // Get all sessions from old store
    const sessions = await oldStore.all((err, sessions) => {
      if (err) {
        console.error('Error getting sessions:', err);
        return;
      }
      return sessions;
    });
    
    // Migrate each session
    for (const [sessionId, session] of Object.entries(sessions)) {
      await newStore.set(sessionId, session);
      console.log(`Migrated session: ${sessionId}`);
    }
    
    console.log(`Migrated ${Object.keys(sessions).length} sessions`);
  }
  
  async migrateWithValidation(oldStore: any, newStore: any): Promise<void> {
    // Get all sessions from old store
    const sessions = await oldStore.all((err, sessions) => {
      if (err) {
        console.error('Error getting sessions:', err);
        return;
      }
      return sessions;
    });
    
    // Validate and migrate each session
    for (const [sessionId, session] of Object.entries(sessions)) {
      // Validate session data
      if (this.isValidSession(session)) {
        await newStore.set(sessionId, session);
        console.log(`Migrated session: ${sessionId}`);
      } else {
        console.warn(`Skipping invalid session: ${sessionId}`);
      }
    }
    
    console.log(`Migrated ${Object.keys(sessions).length} valid sessions`);
  }
  
  private isValidSession(session: any): boolean {
    // Validate session structure
    return session && session.userId && session.createdAt;
  }
}
```

---

## Security Best Practices

### Security Checklist

```markdown
## Session Security Best Practices

### Cookie Security
- [ ] Set httpOnly flag
- [ ] Set secure flag (HTTPS only)
- [ ] Set sameSite attribute
- [ ] Use appropriate maxAge
- [ ] Set path appropriately
- [ ] Don't store sensitive data in cookies

### Session Management
- [ ] Regenerate session ID on login
- [ ] Implement session timeout
- [ ] Limit concurrent sessions
- [ ] Implement session fixation prevention
- [ ] Store minimal data in session
- [ ] Implement proper session cleanup

### CSRF Protection
- [ ] Generate CSRF tokens
- [ ] Validate on state-changing requests
- [ ] Use double-submit cookie pattern
- [ ] Include CSRF token in forms
- [ ] Validate token on server

### Session Storage
- [ ] Use secure session store (Redis)
- [ ] Don't store secrets in session
- [ ] Encrypt sensitive data
- [ ] Implement proper access controls
- [ ] Use secure connection to Redis

### Transport Security
- [ ] Always use HTTPS
- [ ] Implement HSTS headers
- [ ] Use secure cipher suites
- [ ] Validate certificates
- [ ] Implement proper CSP

### Monitoring
- [ ] Track session creation/destruction
- [ ] Monitor for suspicious activity
- [ ] Track concurrent sessions per user
- [ ] Alert on unusual patterns
- [ ] Implement session analytics
```

---

## Additional Resources

- [Express Session Documentation](https://github.com/expressjs/session)
- [FastAPI Sessions](https://fastapi.tiangolo.com/tutorial/dependencies/working-with-cookies/)
- [OWASP Session Management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- [CSRF Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)
