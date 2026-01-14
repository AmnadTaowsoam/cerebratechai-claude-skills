# OAuth 2.0 Implementation

## Overview

Comprehensive guide to OAuth 2.0 implementation for web applications.

## Table of Contents

1. [OAuth 2.0 Flows](#oauth-20-flows)
2. [Provider Setup](#provider-setup)
3. [NextAuth.js Setup](#nextauthjs-setup)
4. [Passport.js Strategies](#passportjs-strategies)
5. [Token Management](#token-management)
6. [Scopes and Permissions](#scopes-and-permissions)
7. [Social Login Integration](#social-login-integration)
8. [Security Considerations](#security-considerations)
9. [Error Handling](#error-handling)
10. [Production Setup](#production-setup)

---

## OAuth 2.0 Flows

### Authorization Code Flow

```typescript
// oauth-flows.ts
export interface OAuthConfig {
  clientId: string;
  clientSecret: string;
  redirectUri: string;
  scopes: string[];
  authUrl: string;
  tokenUrl: string;
}

export class AuthorizationCodeFlow {
  constructor(private config: OAuthConfig) {}
  
  getAuthorizationUrl(state: string): string {
    const params = new URLSearchParams({
      response_type: 'code',
      client_id: this.config.clientId,
      redirect_uri: this.config.redirectUri,
      scope: this.config.scopes.join(' '),
      state: state
    });
    
    return `${this.config.authUrl}?${params.toString()}`;
  }
  
  async exchangeCodeForTokens(code: string, state: string): Promise<any> {
    // Verify state (CSRF protection)
    if (!this.verifyState(state)) {
      throw new Error('Invalid state parameter');
    }
    
    const response = await fetch(this.config.tokenUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: new URLSearchParams({
        grant_type: 'authorization_code',
        code: code,
        redirect_uri: this.config.redirectUri,
        client_id: this.config.clientId,
        client_secret: this.config.clientSecret
      })
    });
    
    return response.json();
  }
  
  async refreshAccessToken(refreshToken: string): Promise<any> {
    const response = await fetch(this.config.tokenUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: new URLSearchParams({
        grant_type: 'refresh_token',
        refresh_token: refreshToken,
        client_id: this.config.clientId,
        client_secret: this.config.clientSecret
      })
    });
    
    return response.json();
  }
  
  private verifyState(state: string): boolean {
    // Implement state verification
    return true;
  }
  
  generateState(): string {
    return Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
  }
}
```

### Client Credentials Flow

```typescript
// client-credentials-flow.ts
export class ClientCredentialsFlow {
  constructor(private config: OAuthConfig) {}
  
  async getClientCredentials(): Promise<any> {
    const response = await fetch(this.config.tokenUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: new URLSearchParams({
        grant_type: 'client_credentials',
        scope: this.config.scopes.join(' '),
        client_id: this.config.clientId,
        client_secret: this.config.clientSecret
      })
    });
    
    return response.json();
  }
}
```

### PKCE Flow

```typescript
// pkce-flow.ts
import crypto from 'crypto';

export class PKCEFlow {
  private codeVerifier: string;
  private codeChallenge: string;
  
  constructor() {
    this.generatePKCE();
  }
  
  private generatePKCE(): void {
    // Generate code verifier (random string)
    this.codeVerifier = crypto.randomBytes(32).toString('base64url');
    
    // Generate code challenge (SHA256 hash of verifier)
    this.codeChallenge = crypto
      .createHash('sha256')
      .update(this.codeVerifier)
      .digest('base64url');
  }
  
  getAuthorizationUrl(config: OAuthConfig): string {
    const state = this.generateState();
    const params = new URLSearchParams({
      response_type: 'code',
      client_id: config.clientId,
      redirect_uri: config.redirectUri,
      scope: config.scopes.join(' '),
      state: state,
      code_challenge: this.codeChallenge,
      code_challenge_method: 'S256'
    });
    
    return `${config.authUrl}?${params.toString()}`;
  }
  
  async exchangeCodeForTokens(code: string, state: string, config: OAuthConfig): Promise<any> {
    // Verify state
    if (!this.verifyState(state)) {
      throw new Error('Invalid state parameter');
    }
    
    const response = await fetch(config.tokenUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: new URLSearchParams({
        grant_type: 'authorization_code',
        code: code,
        redirect_uri: config.redirectUri,
        client_id: config.clientId,
        client_secret: config.clientSecret,
        code_verifier: this.codeVerifier
      })
    });
    
    return response.json();
  }
  
  private generateState(): string {
    return Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
  }
  
  private verifyState(state: string): boolean {
    // Implement state verification
    return true;
  }
}
```

---

## Provider Setup

### Google OAuth

```typescript
// google-oauth.ts
export class GoogleOAuth {
  private config: OAuthConfig = {
    clientId: process.env.GOOGLE_CLIENT_ID!,
    clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    redirectUri: process.env.GOOGLE_REDIRECT_URI!,
    scopes: [
      'openid',
      'email',
      'profile'
    ],
    authUrl: 'https://accounts.google.com/o/oauth2/v2/auth',
    tokenUrl: 'https://oauth2.googleapis.com/token'
  };
  
  getAuthUrl(state: string): string {
    const flow = new AuthorizationCodeFlow(this.config);
    return flow.getAuthorizationUrl(state);
  }
  
  async exchangeCode(code: string, state: string): Promise<any> {
    const flow = new AuthorizationCodeFlow(this.config);
    return flow.exchangeCodeForTokens(code, state);
  }
  
  async getUserInfo(accessToken: string): Promise<any> {
    const response = await fetch('https://www.googleapis.com/oauth2/v2/userinfo', {
      headers: {
        'Authorization': `Bearer ${accessToken}`
      }
    });
    
    return response.json();
  }
}
```

### GitHub OAuth

```typescript
// github-oauth.ts
export class GitHubOAuth {
  private config: OAuthConfig = {
    clientId: process.env.GITHUB_CLIENT_ID!,
    clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    redirectUri: process.env.GITHUB_REDIRECT_URI!,
    scopes: ['user:email', 'read:user'],
    authUrl: 'https://github.com/login/oauth/authorize',
    tokenUrl: 'https://github.com/login/oauth/access_token'
  };
  
  getAuthUrl(state: string): string {
    const flow = new AuthorizationCodeFlow(this.config);
    return flow.getAuthorizationUrl(state);
  }
  
  async exchangeCode(code: string, state: string): Promise<any> {
    const flow = new AuthorizationCodeFlow(this.config);
    return flow.exchangeCodeForTokens(code, state);
  }
  
  async getUserInfo(accessToken: string): Promise<any> {
    const response = await fetch('https://api.github.com/user', {
      headers: {
        'Authorization': `Bearer ${accessToken}`
      }
    });
    
    return response.json();
  }
}
```

### Facebook OAuth

```typescript
// facebook-oauth.ts
export class FacebookOAuth {
  private config: OAuthConfig = {
    clientId: process.env.FACEBOOK_APP_ID!,
    clientSecret: process.env.FACEBOOK_APP_SECRET!,
    redirectUri: process.env.FACEBOOK_REDIRECT_URI!,
    scopes: ['email', 'public_profile'],
    authUrl: 'https://www.facebook.com/v18.0/dialog/oauth',
    tokenUrl: 'https://graph.facebook.com/v18.0/oauth/access_token'
  };
  
  getAuthUrl(state: string): string {
    const flow = new AuthorizationCodeFlow(this.config);
    return flow.getAuthorizationUrl(state);
  }
  
  async exchangeCode(code: string, state: string): Promise<any> {
    const flow = new AuthorizationCodeFlow(this.config);
    return flow.exchangeCodeForTokens(code, state);
  }
  
  async getUserInfo(accessToken: string): Promise<any> {
    const response = await fetch(
      'https://graph.facebook.com/me?fields=id,name,email',
      {
        headers: {
          'Authorization': `Bearer ${accessToken}`
        }
      }
    );
    
    return response.json();
  }
}
```

---

## NextAuth.js Setup

### Configuration

```typescript
// next-auth.config.ts
import type { NextAuthConfig } from 'next-auth';
import GoogleProvider from 'next-auth/providers/google';
import GitHubProvider from 'next-auth/providers/github';
import FacebookProvider from 'next-auth/providers/facebook';

export const authOptions: NextAuthConfig = {
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
      authorization: {
        params: {
          prompt: 'consent',
          access_type: 'offline',
          response_type: 'code'
        }
      }
    }),
    GitHubProvider({
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!
    }),
    FacebookProvider({
      clientId: process.env.FACEBOOK_CLIENT_ID!,
      clientSecret: process.env.FACEBOOK_CLIENT_SECRET!
    })
  ],
  callbacks: {
    async signIn({ user, account, profile }) {
      console.log('User signed in:', user);
      return true;
    },
    async redirect({ url, baseUrl }) {
      return url.startsWith('/') ? url : `${baseUrl}${url}`;
    },
    async session({ session, token, user }) {
      return {
        ...session,
        accessToken: token.accessToken,
        user
      };
    },
    async jwt({ token, user, account }) {
      return {
        ...token,
        id: user.id,
        email: user.email,
        image: user.image
      };
    }
  },
  pages: {
    signIn: '/auth/signin',
    error: '/auth/error',
    signOut: '/auth/signout'
  },
  session: {
    strategy: 'jwt',
    maxAge: 30 * 24 * 60 * 60, // 30 days
    updateAge: 24 * 60 * 60 // 24 hours
  }
};
```

### API Routes

```typescript
// app/api/auth/[...nextauth]/route.ts
import NextAuth from 'next-auth';
import { authOptions } from '@/lib/auth';

const handler = NextAuth(authOptions);

export { GET, POST } as const;
```

### Custom Callback

```typescript
// app/api/auth/callback/route.ts
import { NextResponse } from 'next/server';
import { authOptions } from '@/lib/auth';
import NextAuth from 'next-auth';

const handler = NextAuth({
  ...authOptions,
  callbacks: {
    async signIn({ user, account, profile }) {
      // Check if user exists in database
      const existingUser = await User.findOne({ email: user.email });
      
      if (existingUser) {
        // Link OAuth account to existing user
        await User.update(existingUser.id, {
          [`${account.provider}AccountId`]: account.providerAccountId
        });
        return true;
      }
      
      // Create new user
      const newUser = await User.create({
        email: user.email,
        name: user.name,
        image: user.image,
        [`${account.provider}AccountId`]: account.providerAccountId,
        provider: account.provider
      });
      
      return true;
    }
  }
});

export { GET, POST } as const;
```

---

## Passport.js Strategies

### Google Strategy

```typescript
// passport-google.ts
import passport from 'passport';
import { Strategy as GoogleStrategy } from 'passport-google-oauth20';

passport.use(new GoogleStrategy({
  clientID: process.env.GOOGLE_CLIENT_ID!,
  clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
  callbackURL: process.env.GOOGLE_CALLBACK_URL!,
  passReqToCallback: true
},
async (req, accessToken, refreshToken, profile, done) => {
  try {
    // Find or create user
    let user = await User.findOne({ googleId: profile.id });
    
    if (!user) {
      user = await User.create({
        googleId: profile.id,
        email: profile.emails[0].value,
        name: profile.displayName,
        image: profile.photos?.[0]?.value,
        provider: 'google'
      });
    }
    
    // Update OAuth tokens
    await User.update(user.id, {
      googleAccessToken: accessToken,
      googleRefreshToken: refreshToken
    });
    
    done(null, user);
  } catch (error) {
    done(error as Error);
  }
}));
```

### GitHub Strategy

```typescript
// passport-github.ts
import passport from 'passport';
import { Strategy as GitHubStrategy } from 'passport-github2';

passport.use(new GitHubStrategy({
  clientID: process.env.GITHUB_CLIENT_ID!,
  clientSecret: process.env.GITHUB_CLIENT_SECRET!,
  callbackURL: process.env.GITHUB_CALLBACK_URL!,
  passReqToCallback: true
},
async (req, accessToken, refreshToken, profile, done) => {
  try {
    // Find or create user
    let user = await User.findOne({ githubId: profile.id });
    
    if (!user) {
      // Fetch additional user info
      const response = await fetch('https://api.github.com/user', {
        headers: { 'Authorization': `Bearer ${accessToken}` }
      });
      const githubUser = await response.json();
      
      user = await User.create({
        githubId: profile.id,
        email: githubUser.email,
        name: githubUser.name || githubUser.login,
        image: githubUser.avatar_url,
        provider: 'github'
      });
    }
    
    // Update OAuth tokens
    await User.update(user.id, {
      githubAccessToken: accessToken
    });
    
    done(null, user);
  } catch (error) {
    done(error as Error);
  }
}));
```

### Express Integration

```typescript
// auth-routes.ts
import express from 'express';
import passport from 'passport';
import { Strategy as GoogleStrategy } from 'passport-google-oauth20';

const router = express.Router();

// Google OAuth routes
router.get('/google', passport.authenticate('google', {
  scope: ['profile', 'email']
}));

router.get('/google/callback', passport.authenticate('google', {
  failureRedirect: '/login',
  successRedirect: '/dashboard'
}));

// GitHub OAuth routes
router.get('/github', passport.authenticate('github', {
  scope: ['user:email']
}));

router.get('/github/callback', passport.authenticate('github', {
  failureRedirect: '/login',
  successRedirect: '/dashboard'
}));

export default router;
```

---

## Token Management

### Token Storage

```typescript
// token-storage.ts
export class TokenStorage {
  static async storeTokens(userId: string, tokens: any): Promise<void> {
    // Store in database
    await User.update(userId, {
      accessToken: tokens.access_token,
      refreshToken: tokens.refresh_token,
      tokenExpiresAt: new Date(Date.now() + tokens.expires_in * 1000)
    });
  }
  
  static async getTokens(userId: string): Promise<any> {
    const user = await User.findById(userId);
    return {
      accessToken: user.accessToken,
      refreshToken: user.refreshToken,
      expiresAt: user.tokenExpiresAt
    };
  }
  
  static async refreshTokens(userId: string, provider: string): Promise<any> {
    const user = await User.findById(userId);
    
    if (!user.refreshToken) {
      throw new Error('No refresh token available');
    }
    
    let newTokens;
    switch (provider) {
      case 'google':
        newTokens = await this.refreshGoogleTokens(user.refreshToken);
        break;
      case 'github':
        newTokens = await this.refreshGitHubTokens(user.refreshToken);
        break;
      default:
        throw new Error(`Unknown provider: ${provider}`);
    }
    
    await this.storeTokens(userId, newTokens);
    return newTokens;
  }
  
  private static async refreshGoogleTokens(refreshToken: string): Promise<any> {
    const response = await fetch('https://oauth2.googleapis.com/token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: new URLSearchParams({
        grant_type: 'refresh_token',
        refresh_token: refreshToken,
        client_id: process.env.GOOGLE_CLIENT_ID!,
        client_secret: process.env.GOOGLE_CLIENT_SECRET!
      })
    });
    
    return response.json();
  }
  
  private static async refreshGitHubTokens(refreshToken: string): Promise<any> {
    const response = await fetch('https://github.com/login/oauth/access_token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
      },
      body: new URLSearchParams({
        grant_type: 'refresh_token',
        refresh_token: refreshToken,
        client_id: process.env.GITHUB_CLIENT_ID!,
        client_secret: process.env.GITHUB_CLIENT_SECRET!
      })
    });
    
    return response.json();
  }
}
```

---

## Scopes and Permissions

### Scope Management

```typescript
// scopes.ts
export interface ScopeConfig {
  name: string;
  description: string;
  permissions: string[];
}

export const OAuthScopes: Record<string, ScopeConfig> = {
  google: {
    name: 'google',
    description: 'Google OAuth scopes',
    permissions: [
      'openid',
      'email',
      'profile'
    ]
  },
  github: {
    name: 'github',
    description: 'GitHub OAuth scopes',
    permissions: [
      'user:email',
      'read:user',
      'repo'
    ]
  },
  facebook: {
    name: 'facebook',
    description: 'Facebook OAuth scopes',
    permissions: [
      'email',
      'public_profile'
    ]
  }
};

export class ScopeManager {
  static getScopes(provider: string, requiredPermissions: string[]): string[] {
    const providerConfig = OAuthScopes[provider];
    
    if (!providerConfig) {
      throw new Error(`Unknown provider: ${provider}`);
    }
    
    return requiredPermissions.filter(perm => 
      providerConfig.permissions.includes(perm)
    );
  }
  
  static validateScopes(provider: string, grantedScopes: string[], requiredScopes: string[]): boolean {
    const providerConfig = OAuthScopes[provider];
    
    if (!providerConfig) {
      return false;
    }
    
    return requiredScopes.every(scope => grantedScopes.includes(scope));
  }
}
```

---

## Social Login Integration

### User Profile Sync

```typescript
// social-login.ts
export class SocialLoginService {
  static async handleSocialLogin(provider: string, profile: any, tokens: any): Promise<any> {
    // Find existing user by provider ID
    const providerIdField = `${provider}Id`;
    const existingUser = await User.findOne({ [providerIdField]: profile.id });
    
    if (existingUser) {
      // Update user info
      await User.update(existingUser.id, {
        name: profile.name,
        image: profile.picture,
        email: profile.email,
        [`providerAccessToken`]: tokens.access_token,
        [`providerRefreshToken`]: tokens.refresh_token
      });
      
      return existingUser;
    }
    
    // Find existing user by email
    const userByEmail = await User.findOne({ email: profile.email });
    
    if (userByEmail) {
      // Link social account
      await User.update(userByEmail.id, {
        [providerIdField]: profile.id,
        [`providerAccessToken`]: tokens.access_token,
        [`providerRefreshToken`]: tokens.refresh_token
      });
      
      return userByEmail;
    }
    
    // Create new user
    const newUser = await User.create({
      email: profile.email,
      name: profile.name,
      image: profile.picture,
      [providerIdField]: profile.id,
      provider: provider,
      [`providerAccessToken`]: tokens.access_token,
      [`providerRefreshToken`]: tokens.refresh_token,
      emailVerified: true,
      role: 'user'
    });
    
    return newUser;
  }
  
  static async unlinkSocialAccount(userId: string, provider: string): Promise<void> {
    const providerIdField = `${provider}Id`;
    const providerTokenField = `${provider}AccessToken`;
    const providerRefreshTokenField = `${provider}RefreshToken`;
    
    await User.update(userId, {
      [providerIdField]: null,
      [providerTokenField]: null,
      [providerRefreshTokenField]: null
    });
  }
}
```

---

## Security Considerations

### Security Best Practices

```typescript
// oauth-security.ts
export class OAuthSecurity {
  static validateState(state: string, storedState: string): boolean {
    // Validate state parameter (CSRF protection)
    return state === storedState;
  }
  
  static validateRedirectUri(redirectUri: string, allowedUris: string[]): boolean {
    // Validate redirect URI (prevent open redirect)
    return allowedUris.some(uri => redirectUri.startsWith(uri));
  }
  
  static generateState(): string {
    // Generate cryptographically secure random state
    return crypto.randomBytes(32).toString('base64url');
  }
  
  static storeState(state: string, session: any): void {
    // Store state in session
    session.oauthState = state;
    session.oauthStateExpires = Date.now() + 600000; // 10 minutes
  }
  
  static verifyAndClearState(state: string, session: any): boolean {
    if (!session.oauthState || session.oauthState !== state) {
      return false;
    }
    
    if (Date.now() > session.oauthStateExpires) {
      delete session.oauthState;
      delete session.oauthStateExpires;
      return false;
    }
    
    delete session.oauthState;
    delete session.oauthStateExpires;
    return true;
  }
}
```

---

## Error Handling

### OAuth Errors

```typescript
// oauth-errors.ts
export class OAuthError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number = 400
  ) {
    super(message);
    this.name = 'OAuthError';
  }
}

export class InvalidStateError extends OAuthError {
  constructor() {
    super('Invalid state parameter', 'INVALID_STATE', 400);
  }
}

export class AccessDeniedError extends OAuthError {
  constructor() {
    super('User denied access', 'ACCESS_DENIED', 401);
  }
}

export class InvalidCodeError extends OAuthError {
  constructor() {
    super('Invalid authorization code', 'INVALID_CODE', 400);
  }
}

export class TokenExchangeError extends OAuthError {
  constructor(originalError: Error) {
    super('Failed to exchange code for tokens', 'TOKEN_EXCHANGE_ERROR', 500);
    this.cause = originalError;
  }
}

// Error handler middleware
export function oauthErrorHandler(err: Error, req: any, res: any, next: any) {
  if (err instanceof OAuthError) {
    return res.status(err.statusCode).json({
      error: err.code,
      message: err.message
    });
  }
  
  next(err);
}
```

---

## Production Setup

### Environment Variables

```bash
# .env.example
# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:3000/auth/google/callback

# GitHub OAuth
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
GITHUB_REDIRECT_URI=http://localhost:3000/auth/github/callback

# Facebook OAuth
FACEBOOK_CLIENT_ID=your-facebook-app-id
FACEBOOK_CLIENT_SECRET=your-facebook-app-secret
FACEBOOK_REDIRECT_URI=http://localhost:3000/auth/facebook/callback

# NextAuth
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-nextauth-secret-at-least-32-characters-long
```

### Production Configuration

```typescript
// oauth-production.ts
export const productionConfig = {
  // Use HTTPS in production
  redirectUris: [
    'https://yourdomain.com/auth/google/callback',
    'https://yourdomain.com/auth/github/callback',
    'https://yourdomain.com/auth/facebook/callback'
  ],
  
  // Session configuration
  session: {
    maxAge: 30 * 24 * 60 * 60, // 30 days
    updateAge: 24 * 60 * 60 // 24 hours
  },
  
  // Security
  security: {
    // Enable CSRF protection
    csrfProtection: true,
    
    // Validate redirect URIs
    validateRedirectUri: true,
    
    // Use secure cookies
    secureCookies: true,
    
    // SameSite cookies
    sameSite: 'strict'
  },
  
  // Logging
  logging: {
    level: process.env.NODE_ENV === 'production' ? 'error' : 'debug',
    logOAuthErrors: true
  }
};
```

---

## Additional Resources

- [OAuth 2.0 Specification](https://oauth.net/2/)
- [NextAuth.js Documentation](https://next-auth.js.org/)
- [Passport.js Documentation](http://www.passportjs.org/)
- [Google OAuth 2.0](https://developers.google.com/identity/protocols/oauth2)
- [GitHub OAuth Apps](https://github.com/settings/apps)
- [Facebook Login](https://developers.facebook.com/docs/facebook-login)
