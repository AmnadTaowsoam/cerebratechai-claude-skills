# JWT Authentication

## Overview

Comprehensive guide to JWT (JSON Web Token) authentication implementation for web applications.

## Table of Contents

1. [JWT Concepts](#jwt-concepts)
2. [Token Generation](#token-generation)
3. [Token Verification](#token-verification)
4. [Access Token vs Refresh Token](#access-token-vs-refresh-token)
5. [Token Storage (httpOnly Cookies)](#token-storage-httponly-cookies)
6. [Implementation](#implementation)
7. [Security Best Practices](#security-best-practices)
8. [Token Refresh Flow](#token-refresh-flow)
9. [Token Revocation](#token-revocation)
10. [Error Handling](#error-handling)
11. [Testing](#testing)
12. [Production Checklist](#production-checklist)

---

## JWT Concepts

### JWT Structure

```typescript
// jwt-types.ts
export interface JWTPayload {
  sub: string;           // Subject (user ID)
  iat: number;          // Issued at
  exp: number;          // Expiration time
  iss?: string;         // Issuer
  aud?: string;         // Audience
  nbf?: number;         // Not before
  jti?: string;         // JWT ID (for revocation)
  typ?: string;         // Type
}

export interface JWTHeader {
  alg: string;          // Algorithm (HS256, RS256, etc.)
  typ: string;          // Type (JWT)
  kid?: string;         // Key ID (for multiple keys)
}

export interface TokenPair {
  accessToken: string;
  refreshToken: string;
  expiresIn: number;
}
```

### JWT Components

```markdown
## JWT Structure

### Header
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

### Payload
```json
{
  "sub": "user-123",
  "iat": 1516239022,
  "exp": 1516242622,
  "iss": "my-app",
  "aud": "my-app-users"
}
```

### Signature
```
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret
)
```
```

---

## Token Generation

### Token Generation (Node.js)

```typescript
// jwt-generator.ts
import jwt from 'jsonwebtoken';
import crypto from 'crypto';

export class JWTGenerator {
  constructor(
    private accessTokenSecret: string,
    private refreshTokenSecret: string,
    private accessTokenExpiry: string = '15m',
    private refreshTokenExpiry: string = '7d'
  ) {}
  
  generateAccessToken(payload: any): string {
    return jwt.sign(
      {
        ...payload,
        type: 'access',
        jti: crypto.randomUUID()
      },
      this.accessTokenSecret,
      {
        expiresIn: this.accessTokenExpiry,
        issuer: 'my-app',
        audience: 'my-app-users'
      }
    );
  }
  
  generateRefreshToken(userId: string): string {
    return jwt.sign(
      {
        sub: userId,
        type: 'refresh',
        jti: crypto.randomUUID()
      },
      this.refreshTokenSecret,
      {
        expiresIn: this.refreshTokenExpiry,
        issuer: 'my-app'
      }
    );
  }
  
  generateTokenPair(userId: string, additionalPayload?: any): TokenPair {
    const payload = {
      sub: userId,
      ...additionalPayload
    };
    
    const accessToken = this.generateAccessToken(payload);
    const refreshToken = this.generateRefreshToken(userId);
    const decoded = jwt.decode(accessToken) as any;
    
    return {
      accessToken,
      refreshToken,
      expiresIn: decoded.exp - decoded.iat
    };
  }
}

// Usage
const generator = new JWTGenerator(
  process.env.JWT_ACCESS_SECRET!,
  process.env.JWT_REFRESH_SECRET!
);

const tokens = generator.generateTokenPair('user-123', {
  role: 'user',
  permissions: ['read', 'write']
});
```

### Token Generation (Python)

```python
# jwt_generator.py
import jwt
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any

class JWTGenerator:
    def __init__(
        self,
        access_token_secret: str,
        refresh_token_secret: str,
        access_token_expiry: str = '15m',
        refresh_token_expiry: str = '7d'
    ):
        self.access_token_secret = access_token_secret
        self.refresh_token_secret = refresh_token_secret
        self.access_token_expiry = access_token_expiry
        self.refresh_token_expiry = refresh_token_expiry
    
    def generate_access_token(self, payload: Dict[str, Any]) -> str:
        """Generate access token"""
        token_payload = {
            **payload,
            'type': 'access',
            'jti': str(uuid.uuid4()),
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=15),
            'iss': 'my-app',
            'aud': 'my-app-users'
        }
        
        return jwt.encode(token_payload, self.access_token_secret, algorithm='HS256')
    
    def generate_refresh_token(self, user_id: str) -> str:
        """Generate refresh token"""
        token_payload = {
            'sub': user_id,
            'type': 'refresh',
            'jti': str(uuid.uuid4()),
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(days=7),
            'iss': 'my-app'
        }
        
        return jwt.encode(token_payload, self.refresh_token_secret, algorithm='HS256')
    
    def generate_token_pair(self, user_id: str, additional_payload: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate both access and refresh tokens"""
        payload = {
            'sub': user_id,
            **(additional_payload or {})
        }
        
        access_token = self.generate_access_token(payload)
        refresh_token = self.generate_refresh_token(user_id)
        decoded = jwt.decode(access_token)
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'expires_in': decoded['exp'] - decoded['iat']
        }

# Usage
generator = JWTGenerator(
    os.getenv('JWT_ACCESS_SECRET'),
    os.getenv('JWT_REFRESH_SECRET')
)

tokens = generator.generate_token_pair('user-123', {
    'role': 'user',
    'permissions': ['read', 'write']
})
```

---

## Token Verification

### Token Verification (Node.js)

```typescript
// jwt-verifier.ts
import jwt from 'jsonwebtoken';
import { Request, Response, NextFunction } from 'express';

export interface AuthRequest extends Request {
  user?: any;
}

export class JWTVerifier {
  constructor(
    private accessTokenSecret: string,
    private refreshTokenSecret: string
  ) {}
  
  verifyAccessToken(token: string): any {
    try {
      return jwt.verify(token, this.accessTokenSecret, {
        issuer: 'my-app',
        audience: 'my-app-users'
      });
    } catch (error) {
      if (error instanceof jwt.TokenExpiredError) {
        throw new Error('Token expired');
      } else if (error instanceof jwt.JsonWebTokenError) {
        throw new Error('Invalid token');
      }
      throw error;
    }
  }
  
  verifyRefreshToken(token: string): any {
    try {
      return jwt.verify(token, this.refreshTokenSecret, {
        issuer: 'my-app'
      });
    } catch (error) {
      if (error instanceof jwt.TokenExpiredError) {
        throw new Error('Refresh token expired');
      } else if (error instanceof jwt.JsonWebTokenError) {
        throw new Error('Invalid refresh token');
      }
      throw error;
    }
  }
  
  middleware(req: AuthRequest, res: Response, next: NextFunction): void {
    const authHeader = req.headers.authorization;
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res.status(401).json({ error: 'No token provided' });
    }
    
    const token = authHeader.substring(7);
    
    try {
      const decoded = this.verifyAccessToken(token);
      req.user = decoded;
      next();
    } catch (error) {
      res.status(401).json({ error: (error as Error).message });
    }
  }
}

// Usage
const verifier = new JWTVerifier(
  process.env.JWT_ACCESS_SECRET!,
  process.env.JWT_REFRESH_SECRET!
);

app.get('/protected', verifier.middleware.bind(verifier), (req, res) => {
  res.json({ user: (req as AuthRequest).user });
});
```

### Token Verification (Python)

```python
# jwt_verifier.py
import jwt
from functools import wraps
from flask import request, jsonify, g
from typing import Callable

class JWTVerifier:
    def __init__(
        self,
        access_token_secret: str,
        refresh_token_secret: str
    ):
        self.access_token_secret = access_token_secret
        self.refresh_token_secret = refresh_token_secret
    
    def verify_access_token(self, token: str) -> dict:
        """Verify access token"""
        try:
            return jwt.decode(
                token,
                self.access_token_secret,
                algorithms=['HS256'],
                issuer='my-app',
                audience='my-app-users'
            )
        except jwt.ExpiredSignatureError:
            raise ValueError('Token expired')
        except jwt.InvalidTokenError:
            raise ValueError('Invalid token')
    
    def verify_refresh_token(self, token: str) -> dict:
        """Verify refresh token"""
        try:
            return jwt.decode(
                token,
                self.refresh_token_secret,
                algorithms=['HS256'],
                issuer='my-app'
            )
        except jwt.ExpiredSignatureError:
            raise ValueError('Refresh token expired')
        except jwt.InvalidTokenError:
            raise ValueError('Invalid refresh token')
    
    def middleware(self, f: Callable) -> Callable:
        """Flask middleware for token verification"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({'error': 'No token provided'}), 401
            
            token = auth_header.split(' ')[1]
            
            try:
                decoded = self.verify_access_token(token)
                g.user = decoded
                return f(*args, **kwargs)
            except ValueError as e:
                return jsonify({'error': str(e)}), 401
        
        return decorated_function

# Usage
verifier = JWTVerifier(
    os.getenv('JWT_ACCESS_SECRET'),
    os.getenv('JWT_REFRESH_SECRET')
)

@app.route('/protected')
@verifier.middleware
def protected_route():
    return jsonify({'user': g.user})
```

---

## Access Token vs Refresh Token

### Token Strategy

```typescript
// token-strategy.ts
export interface TokenStrategy {
  accessTokenExpiry: string;
  refreshTokenExpiry: string;
  rotateRefreshTokens: boolean;
}

export class TokenManager {
  constructor(
    private generator: JWTGenerator,
    private verifier: JWTVerifier,
    private strategy: TokenStrategy
  ) {}
  
  async login(credentials: { email: string; password: string }): Promise<TokenPair> {
    // Validate credentials
    const user = await this.validateCredentials(credentials);
    
    // Generate tokens
    const tokens = this.generator.generateTokenPair(user.id, {
      email: user.email,
      role: user.role
    });
    
    // Store refresh token
    await this.storeRefreshToken(user.id, tokens.refreshToken);
    
    return tokens;
  }
  
  async refreshTokens(refreshToken: string): Promise<TokenPair> {
    // Verify refresh token
    const decoded = this.verifier.verifyRefreshToken(refreshToken);
    
    // Check if token is revoked
    const isRevoked = await this.isTokenRevoked(decoded.jti);
    if (isRevoked) {
      throw new Error('Refresh token revoked');
    }
    
    // Generate new tokens
    const tokens = this.generator.generateTokenPair(decoded.sub);
    
    // If rotating refresh tokens
    if (this.strategy.rotateRefreshTokens) {
      // Revoke old refresh token
      await this.revokeRefreshToken(decoded.jti);
      // Store new refresh token
      await this.storeRefreshToken(decoded.sub, tokens.refreshToken);
    }
    
    return tokens;
  }
  
  async logout(refreshToken: string): Promise<void> {
    const decoded = this.verifier.verifyRefreshToken(refreshToken);
    await this.revokeRefreshToken(decoded.jti);
  }
  
  private async validateCredentials(credentials: any): Promise<any> {
    // Implementation
    return { id: 'user-123', email: credentials.email, role: 'user' };
  }
  
  private async storeRefreshToken(userId: string, token: string): Promise<void> {
    // Implementation - store in database
  }
  
  private async isTokenRevoked(jti: string): Promise<boolean> {
    // Implementation - check revocation list
    return false;
  }
  
  private async revokeRefreshToken(jti: string): Promise<void> {
    // Implementation - add to revocation list
  }
}
```

---

## Token Storage (httpOnly Cookies)

### Cookie Storage

```typescript
// cookie-storage.ts
import { Response } from 'express';

export class TokenCookieManager {
  static setAuthCookies(res: Response, tokens: TokenPair): void {
    // Access token - short-lived, httpOnly
    res.cookie('accessToken', tokens.accessToken, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'strict',
      maxAge: tokens.expiresIn,
      path: '/'
    });
    
    // Refresh token - longer-lived, httpOnly
    res.cookie('refreshToken', tokens.refreshToken, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'strict',
      maxAge: 7 * 24 * 60 * 60, // 7 days
      path: '/'
    });
  }
  
  static clearAuthCookies(res: Response): void {
    res.clearCookie('accessToken', { path: '/' });
    res.clearCookie('refreshToken', { path: '/' });
  }
  
  static getAccessTokenFromCookie(req: any): string | null {
    return req.cookies?.accessToken || null;
  }
  
  static getRefreshTokenFromCookie(req: any): string | null {
    return req.cookies?.refreshToken || null;
  }
}

// Usage
app.post('/login', async (req, res) => {
  const tokens = await tokenManager.login(req.body);
  TokenCookieManager.setAuthCookies(res, tokens);
  res.json({ success: true });
});

app.post('/logout', (req, res) => {
  TokenCookieManager.clearAuthCookies(res);
  res.json({ success: true });
});
```

---

## Implementation

### Node.js/Express Implementation

```typescript
// auth-service.ts
import express from 'express';
import bcrypt from 'bcryptjs';
import { JWTGenerator, JWTVerifier, TokenManager, TokenCookieManager } from './jwt';

const app = express();
app.use(express.json());

// Initialize JWT
const generator = new JWTGenerator(
  process.env.JWT_ACCESS_SECRET!,
  process.env.JWT_REFRESH_SECRET!
);

const verifier = new JWTVerifier(
  process.env.JWT_ACCESS_SECRET!,
  process.env.JWT_REFRESH_SECRET!
);

const tokenManager = new TokenManager(
  generator,
  verifier,
  {
    accessTokenExpiry: '15m',
    refreshTokenExpiry: '7d',
    rotateRefreshTokens: true
  }
);

// Login endpoint
app.post('/auth/login', async (req, res) => {
  try {
    const { email, password } = req.body;
    
    // Validate credentials
    const user = await User.findOne({ email });
    if (!user || !await bcrypt.compare(password, user.passwordHash)) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }
    
    // Generate tokens
    const tokens = await tokenManager.login({ email, password });
    
    // Set cookies
    TokenCookieManager.setAuthCookies(res, tokens);
    
    res.json({
      success: true,
      user: {
        id: user.id,
        email: user.email,
        name: user.name
      }
    });
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Refresh token endpoint
app.post('/auth/refresh', async (req, res) => {
  try {
    const refreshToken = TokenCookieManager.getRefreshTokenFromCookie(req);
    
    if (!refreshToken) {
      return res.status(401).json({ error: 'No refresh token' });
    }
    
    const tokens = await tokenManager.refreshTokens(refreshToken);
    
    TokenCookieManager.setAuthCookies(res, tokens);
    
    res.json({ success: true });
  } catch (error) {
    res.status(401).json({ error: (error as Error).message });
  }
});

// Logout endpoint
app.post('/auth/logout', async (req, res) => {
  try {
    const refreshToken = TokenCookieManager.getRefreshTokenFromCookie(req);
    
    if (refreshToken) {
      await tokenManager.logout(refreshToken);
    }
    
    TokenCookieManager.clearAuthCookies(res);
    
    res.json({ success: true });
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Protected route
app.get('/api/protected', verifier.middleware.bind(verifier), (req, res) => {
  res.json({
    message: 'Protected data',
    user: (req as any).user
  });
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
```

### FastAPI Implementation

```python
# auth_service.py
from fastapi import FastAPI, HTTPException, Depends, Cookie, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from datetime import timedelta
from typing import Optional

from jwt_generator import JWTGenerator
from jwt_verifier import JWTVerifier

app = FastAPI()

# Initialize JWT
generator = JWTGenerator(
    os.getenv('JWT_ACCESS_SECRET'),
    os.getenv('JWT_REFRESH_SECRET')
)

verifier = JWTVerifier(
    os.getenv('JWT_ACCESS_SECRET'),
    os.getenv('JWT_REFRESH_SECRET')
)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user from JWT token"""
    try:
        token = credentials.credentials
        decoded = verifier.verify_access_token(token)
        return decoded
    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
            headers={'WWW-Authenticate': 'Bearer'}
        )

@app.post('/auth/login')
async def login(email: str, password: str, response: Response):
    """Login endpoint"""
    # Validate credentials
    user = await User.get_by_email(email)
    if not user or not pwd_context.verify(password, user.password_hash):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    
    # Generate tokens
    tokens = generator.generate_token_pair(str(user.id), {
        'email': user.email,
        'role': user.role
    })
    
    # Set cookies
    response.set_cookie(
        key='accessToken',
        value=tokens['access_token'],
        httponly=True,
        secure=True,
        samesite='strict',
        max_age=tokens['expires_in']
    )
    
    response.set_cookie(
        key='refreshToken',
        value=tokens['refresh_token'],
        httponly=True,
        secure=True,
        samesite='strict',
        max_age=7 * 24 * 60 * 60
    )
    
    return {
        'success': True,
        'user': {
            'id': str(user.id),
            'email': user.email,
            'name': user.name
        }
    }

@app.post('/auth/refresh')
async def refresh_token(
    refresh_token: Optional[str] = Cookie(None),
    response: Response
):
    """Refresh access token"""
    if not refresh_token:
        raise HTTPException(status_code=401, detail='No refresh token')
    
    try:
        tokens = generator.generate_token_pair(
            verifier.verify_refresh_token(refresh_token)['sub']
        )
        
        # Set new cookies
        response.set_cookie(
            key='accessToken',
            value=tokens['access_token'],
            httponly=True,
            secure=True,
            samesite='strict',
            max_age=tokens['expires_in']
        )
        
        return {'success': True}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@app.get('/api/protected')
async def protected_route(current_user: dict = Depends(get_current_user)):
    """Protected route"""
    return {
        'message': 'Protected data',
        'user': current_user
    }
```

### Next.js Implementation

```typescript
// lib/auth.ts
import { cookies } from 'next/headers';
import { SignJWT, jwtVerify } from 'jose';

const JWT_SECRET = new TextEncoder().encode(process.env.JWT_SECRET!);

export async function createToken(payload: any): Promise<string> {
  const token = await new SignJWT(payload)
    .setProtectedHeader({ alg: 'HS256' })
    .setIssuedAt()
    .setExpirationTime('15m')
    .sign(JWT_SECRET);
  
  return token;
}

export async function verifyToken(token: string): Promise<any> {
  try {
    const { payload } = await jwtVerify(token, JWT_SECRET);
    return payload;
  } catch (error) {
    throw new Error('Invalid token');
  }
}

export async function getSession(): Promise<any | null> {
  const cookieStore = cookies();
  const token = cookieStore.get('accessToken')?.value;
  
  if (!token) return null;
  
  try {
    return await verifyToken(token);
  } catch {
    return null;
  }
}

// api/auth/login/route.ts
import { NextResponse } from 'next/server';
import { createToken } from '@/lib/auth';
import bcrypt from 'bcryptjs';

export async function POST(request: Request) {
  const { email, password } = await request.json();
  
  // Validate credentials
  const user = await User.findOne({ email });
  if (!user || !await bcrypt.compare(password, user.passwordHash)) {
    return NextResponse.json({ error: 'Invalid credentials' }, { status: 401 });
  }
  
  // Create token
  const token = await createToken({
    userId: user.id,
    email: user.email
  });
  
  const response = NextResponse.json({
    success: true,
    user: { id: user.id, email: user.email }
  });
  
  // Set cookie
  response.cookies.set('accessToken', token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'strict',
    maxAge: 15 * 60,
    path: '/'
  });
  
  return response;
}
```

---

## Security Best Practices

### Security Checklist

```markdown
## JWT Security Best Practices

### Secret Management
- [ ] Use strong, random secrets (256+ bits)
- [ ] Store secrets in environment variables
- [ ] Rotate secrets regularly
- [ ] Use different secrets for access/refresh tokens
- [ ] Never commit secrets to version control

### Token Configuration
- [ ] Use short expiry for access tokens (5-15 min)
- [ ] Use longer expiry for refresh tokens (7-30 days)
- [ ] Set appropriate issuer and audience
- [ ] Include unique JWT ID (jti) for revocation
- [ ] Use strong algorithms (RS256 preferred over HS256)

### Token Storage
- [ ] Use httpOnly cookies for tokens
- [ ] Set secure flag (HTTPS only)
- [ ] Set sameSite to 'strict' or 'lax'
- [ ] Don't store tokens in localStorage
- [ ] Implement token rotation

### Token Validation
- [ ] Verify issuer and audience
- [ ] Check token expiration
- [ ] Validate token type (access vs refresh)
- [ ] Implement token revocation
- [ ] Check token blacklist/whitelist

### Transport Security
- [ ] Always use HTTPS in production
- [ ] Implement CSRF protection
- [ ] Set appropriate CORS headers
- [ ] Implement rate limiting
- [ ] Monitor for suspicious activity
```

---

## Token Refresh Flow

### Refresh Flow Diagram

```typescript
// token-refresh-flow.ts
export class TokenRefreshFlow {
  constructor(private tokenManager: TokenManager) {}
  
  async refreshTokenIfNeeded(req: any, res: any): Promise<void> {
    const accessToken = TokenCookieManager.getAccessTokenFromCookie(req);
    
    if (!accessToken) {
      // No access token, try to refresh
      await this.refreshToken(req, res);
      return;
    }
    
    try {
      // Verify access token
      this.tokenManager.verifier.verifyAccessToken(accessToken);
      // Token is valid, continue
    } catch (error) {
      if ((error as Error).message === 'Token expired') {
        // Token expired, try to refresh
        await this.refreshToken(req, res);
      } else {
        // Invalid token, clear cookies
        TokenCookieManager.clearAuthCookies(res);
        throw error;
      }
    }
  }
  
  private async refreshToken(req: any, res: any): Promise<void> {
    const refreshToken = TokenCookieManager.getRefreshTokenFromCookie(req);
    
    if (!refreshToken) {
      TokenCookieManager.clearAuthCookies(res);
      throw new Error('No refresh token available');
    }
    
    try {
      const tokens = await this.tokenManager.refreshTokens(refreshToken);
      TokenCookieManager.setAuthCookies(res, tokens);
    } catch (error) {
      TokenCookieManager.clearAuthCookies(res);
      throw error;
    }
  }
}

// Middleware
export const refreshMiddleware = (tokenManager: TokenManager) => {
  const flow = new TokenRefreshFlow(tokenManager);
  
  return async (req: any, res: any, next: any) => {
    try {
      await flow.refreshTokenIfNeeded(req, res);
      next();
    } catch (error) {
      res.status(401).json({ error: 'Authentication required' });
    }
  };
};
```

---

## Token Revocation

### Token Revocation

```typescript
// token-revocation.ts
export class TokenRevocationStore {
  private revokedTokens: Map<string, number> = new Map();
  
  async revokeToken(jti: string, expiry: number): Promise<void> {
    this.revokedTokens.set(jti, expiry);
  }
  
  async isTokenRevoked(jti: string): Promise<boolean> {
    const expiry = this.revokedTokens.get(jti);
    
    if (!expiry) return false;
    
    // Check if token has expired
    if (Date.now() / 1000 > expiry) {
      this.revokedTokens.delete(jti);
      return false;
    }
    
    return true;
  }
  
  async cleanExpiredTokens(): Promise<void> {
    const now = Date.now() / 1000;
    
    for (const [jti, expiry] of this.revokedTokens.entries()) {
      if (now > expiry) {
        this.revokedTokens.delete(jti);
      }
    }
  }
}

// Redis-based revocation store
export class RedisTokenRevocationStore {
  constructor(private redis: any) {}
  
  async revokeToken(jti: string, expiry: number): Promise<void> {
    await this.redis.setex(
      `revoked:${jti}`,
      expiry,
      '1'
    );
  }
  
  async isTokenRevoked(jti: string): Promise<boolean> {
    return (await this.redis.exists(`revoked:${jti}`)) === 1;
  }
}
```

---

## Error Handling

### Error Types

```typescript
// auth-errors.ts
export class AuthError extends Error {
  constructor(
    message: string,
    public statusCode: number = 500,
    public code: string = 'AUTH_ERROR'
  ) {
    super(message);
    this.name = 'AuthError';
  }
}

export class InvalidCredentialsError extends AuthError {
  constructor() {
    super('Invalid email or password', 401, 'INVALID_CREDENTIALS');
  }
}

export class TokenExpiredError extends AuthError {
  constructor() {
    super('Token has expired', 401, 'TOKEN_EXPIRED');
  }
}

export class InvalidTokenError extends AuthError {
  constructor() {
    super('Invalid token', 401, 'INVALID_TOKEN');
  }
}

export class TokenRevokedError extends AuthError {
  constructor() {
    super('Token has been revoked', 401, 'TOKEN_REVOKED');
  }
}

export class RefreshTokenExpiredError extends AuthError {
  constructor() {
    super('Refresh token has expired', 401, 'REFRESH_TOKEN_EXPIRED');
  }
}

// Error handler middleware
export function authErrorHandler(err: Error, req: any, res: any, next: any) {
  if (err instanceof AuthError) {
    return res.status(err.statusCode).json({
      error: err.code,
      message: err.message
    });
  }
  
  next(err);
}
```

---

## Testing

### JWT Tests

```typescript
// jwt.test.ts
import { describe, it, expect, beforeEach } from '@jest/globals';
import { JWTGenerator, JWTVerifier } from './jwt-generator';

describe('JWT Authentication', () => {
  let generator: JWTGenerator;
  let verifier: JWTVerifier;
  
  beforeEach(() => {
    generator = new JWTGenerator('test-secret', 'test-refresh-secret');
    verifier = new JWTVerifier('test-secret', 'test-refresh-secret');
  });
  
  describe('Token Generation', () => {
    it('should generate access token', () => {
      const token = generator.generateAccessToken({
        sub: 'user-123',
        role: 'user'
      });
      
      expect(token).toBeDefined();
      expect(typeof token).toBe('string');
    });
    
    it('should generate refresh token', () => {
      const token = generator.generateRefreshToken('user-123');
      
      expect(token).toBeDefined();
      expect(typeof token).toBe('string');
    });
    
    it('should generate token pair', () => {
      const tokens = generator.generateTokenPair('user-123');
      
      expect(tokens.accessToken).toBeDefined();
      expect(tokens.refreshToken).toBeDefined();
      expect(tokens.expiresIn).toBeGreaterThan(0);
    });
  });
  
  describe('Token Verification', () => {
    it('should verify valid access token', () => {
      const token = generator.generateAccessToken({ sub: 'user-123' });
      const decoded = verifier.verifyAccessToken(token);
      
      expect(decoded.sub).toBe('user-123');
    });
    
    it('should throw error for expired token', () => {
      const expiredToken = generator.generateAccessToken(
        { sub: 'user-123' },
        '-1s' // Expired
      );
      
      expect(() => verifier.verifyAccessToken(expiredToken)).toThrow('Token expired');
    });
    
    it('should throw error for invalid token', () => {
      expect(() => verifier.verifyAccessToken('invalid.token')).toThrow('Invalid token');
    });
  });
});
```

---

## Production Checklist

```markdown
## JWT Authentication Production Checklist

### Configuration
- [ ] JWT secrets configured in environment variables
- [ ] Appropriate token expiry times set
- [ ] Issuer and audience configured
- [ ] Algorithm set to HS256 or RS256
- [ ] Different secrets for access/refresh tokens

### Security
- [ ] HTTPS enabled
- [ ] httpOnly cookies configured
- [ ] Secure flag set on cookies
- [ ] SameSite attribute configured
- [ ] CSRF protection implemented
- [ ] Rate limiting on auth endpoints

### Token Management
- [ ] Token refresh flow implemented
- [ ] Token revocation implemented
- [ ] Refresh token rotation enabled
- [ ] Token blacklist/whitelist configured
- [ ] Token cleanup job scheduled

### Error Handling
- [ ] Proper error messages
- [ ] Error logging implemented
- [ ] Security headers set
- [ ] Graceful degradation

### Monitoring
- [ ] Authentication events logged
- [ ] Failed login attempts tracked
- [ ] Token refresh rate monitored
- [ ] Revoked tokens tracked
- [ ] Security alerts configured
```

---

## Additional Resources

- [JWT.io](https://jwt.io/)
- [jsonwebtoken Documentation](https://www.npmjs.com/package/jsonwebtoken)
- [PyJWT Documentation](https://pyjwt.readthedocs.io/)
- [jose Documentation](https://github.com/panva/jose)
- [OWASP JWT Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)
