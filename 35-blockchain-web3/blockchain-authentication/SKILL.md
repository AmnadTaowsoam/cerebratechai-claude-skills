---
name: Blockchain Authentication
description: Using cryptographic signatures to verify user identity without passwords through Sign-In with Ethereum (SIWE), message signing, signature verification, and session management.
---

# Blockchain Authentication

> **Current Level:** Advanced  
> **Domain:** Blockchain / Authentication

---

## Overview

Web3 authentication uses cryptographic signatures to verify user identity without passwords. This guide covers Sign-In with Ethereum (SIWE), message signing, and session management for building passwordless authentication systems using blockchain wallets.

## Web3 Authentication Concepts

```
User → Connect Wallet → Sign Message → Verify Signature → Create Session
```

**Benefits:**
- No passwords to manage
- Cryptographically secure
- User owns their identity
- Works across applications

## Sign-In with Ethereum (SIWE)

```typescript
// lib/siwe.ts
import { SiweMessage } from 'siwe';
import { ethers } from 'ethers';

export class SIWEService {
  async generateMessage(address: string, nonce: string): Promise<string> {
    const domain = window.location.host;
    const origin = window.location.origin;

    const message = new SiweMessage({
      domain,
      address,
      statement: 'Sign in with Ethereum to the app.',
      uri: origin,
      version: '1',
      chainId: 1,
      nonce,
      issuedAt: new Date().toISOString()
    });

    return message.prepareMessage();
  }

  async verifyMessage(
    message: string,
    signature: string
  ): Promise<SiweMessage> {
    const siweMessage = new SiweMessage(message);
    const fields = await siweMessage.verify({ signature });

    if (!fields.success) {
      throw new Error('Signature verification failed');
    }

    return siweMessage;
  }

  async signIn(
    address: string,
    signer: ethers.Signer
  ): Promise<{ message: string; signature: string }> {
    const nonce = this.generateNonce();
    const message = await this.generateMessage(address, nonce);
    const signature = await signer.signMessage(message);

    return { message, signature };
  }

  private generateNonce(): string {
    return Math.random().toString(36).substring(2, 15);
  }
}
```

## Message Signing

```typescript
// services/message-signing.service.ts
export class MessageSigningService {
  async signMessage(
    message: string,
    signer: ethers.Signer
  ): Promise<string> {
    return signer.signMessage(message);
  }

  async signTypedData(
    domain: ethers.TypedDataDomain,
    types: Record<string, ethers.TypedDataField[]>,
    value: Record<string, any>,
    signer: ethers.Signer
  ): Promise<string> {
    return signer._signTypedData(domain, types, value);
  }

  verifyMessage(message: string, signature: string): string {
    return ethers.utils.verifyMessage(message, signature);
  }

  verifyTypedData(
    domain: ethers.TypedDataDomain,
    types: Record<string, ethers.TypedDataField[]>,
    value: Record<string, any>,
    signature: string
  ): string {
    return ethers.utils.verifyTypedData(domain, types, value, signature);
  }

  async createAuthMessage(address: string, nonce: string): Promise<string> {
    return `Welcome to our dApp!

Click "Sign" to authenticate.

This request will not trigger a blockchain transaction or cost any gas fees.

Wallet address:
${address}

Nonce:
${nonce}`;
  }
}
```

## Signature Verification

```typescript
// services/signature-verification.service.ts
export class SignatureVerificationService {
  verifySignature(
    message: string,
    signature: string,
    expectedAddress: string
  ): boolean {
    try {
      const recoveredAddress = ethers.utils.verifyMessage(message, signature);
      return recoveredAddress.toLowerCase() === expectedAddress.toLowerCase();
    } catch (error) {
      return false;
    }
  }

  async verifyWithTimestamp(
    message: string,
    signature: string,
    expectedAddress: string,
    maxAge: number = 5 * 60 * 1000 // 5 minutes
  ): Promise<boolean> {
    // Verify signature
    if (!this.verifySignature(message, signature, expectedAddress)) {
      return false;
    }

    // Extract timestamp from message
    const timestampMatch = message.match(/Timestamp: (\d+)/);
    if (!timestampMatch) {
      return false;
    }

    const timestamp = parseInt(timestampMatch[1]);
    const now = Date.now();

    // Check if message is not too old
    return now - timestamp < maxAge;
  }
}
```

## Nonce Generation

```typescript
// services/nonce.service.ts
import crypto from 'crypto';

export class NonceService {
  private nonces = new Map<string, { nonce: string; expiresAt: number }>();

  generateNonce(address: string): string {
    const nonce = crypto.randomBytes(16).toString('hex');
    const expiresAt = Date.now() + 5 * 60 * 1000; // 5 minutes

    this.nonces.set(address.toLowerCase(), { nonce, expiresAt });

    return nonce;
  }

  verifyNonce(address: string, nonce: string): boolean {
    const stored = this.nonces.get(address.toLowerCase());

    if (!stored) {
      return false;
    }

    if (Date.now() > stored.expiresAt) {
      this.nonces.delete(address.toLowerCase());
      return false;
    }

    if (stored.nonce !== nonce) {
      return false;
    }

    // Nonce can only be used once
    this.nonces.delete(address.toLowerCase());

    return true;
  }

  cleanup(): void {
    const now = Date.now();
    
    for (const [address, data] of this.nonces.entries()) {
      if (now > data.expiresAt) {
        this.nonces.delete(address);
      }
    }
  }
}

// Run cleanup periodically
setInterval(() => {
  nonceService.cleanup();
}, 60 * 1000); // Every minute
```

## Session Management

```typescript
// services/session.service.ts
import jwt from 'jsonwebtoken';

export class SessionService {
  private jwtSecret = process.env.JWT_SECRET!;

  createSession(address: string): string {
    const token = jwt.sign(
      {
        address: address.toLowerCase(),
        iat: Math.floor(Date.now() / 1000)
      },
      this.jwtSecret,
      {
        expiresIn: '7d'
      }
    );

    return token;
  }

  verifySession(token: string): { address: string } | null {
    try {
      const decoded = jwt.verify(token, this.jwtSecret) as {
        address: string;
        iat: number;
      };

      return { address: decoded.address };
    } catch (error) {
      return null;
    }
  }

  refreshSession(token: string): string | null {
    const session = this.verifySession(token);
    
    if (!session) {
      return null;
    }

    return this.createSession(session.address);
  }
}
```

## Backend Implementation

```typescript
// pages/api/auth/nonce.ts
import type { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { address } = req.body;

  if (!address || !ethers.utils.isAddress(address)) {
    return res.status(400).json({ error: 'Invalid address' });
  }

  const nonce = nonceService.generateNonce(address);

  res.json({ nonce });
}

// pages/api/auth/verify.ts
export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { message, signature } = req.body;

  try {
    // Verify SIWE message
    const siweMessage = new SiweMessage(message);
    const fields = await siweMessage.verify({ signature });

    if (!fields.success) {
      return res.status(401).json({ error: 'Invalid signature' });
    }

    // Verify nonce
    if (!nonceService.verifyNonce(siweMessage.address, siweMessage.nonce)) {
      return res.status(401).json({ error: 'Invalid nonce' });
    }

    // Create session
    const token = sessionService.createSession(siweMessage.address);

    res.json({ token, address: siweMessage.address });
  } catch (error: any) {
    res.status(401).json({ error: error.message });
  }
}

// pages/api/auth/me.ts
export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const token = req.headers.authorization?.replace('Bearer ', '');

  if (!token) {
    return res.status(401).json({ error: 'No token provided' });
  }

  const session = sessionService.verifySession(token);

  if (!session) {
    return res.status(401).json({ error: 'Invalid token' });
  }

  res.json({ address: session.address });
}
```

## Frontend Implementation

```typescript
// hooks/useAuth.ts
import { useState } from 'react';
import { useAccount, useSignMessage } from 'wagmi';
import { SiweMessage } from 'siwe';

export function useAuth() {
  const { address } = useAccount();
  const { signMessageAsync } = useSignMessage();
  const [isLoading, setIsLoading] = useState(false);

  const signIn = async () => {
    if (!address) throw new Error('No address');

    setIsLoading(true);

    try {
      // Get nonce
      const nonceRes = await fetch('/api/auth/nonce', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ address })
      });

      const { nonce } = await nonceRes.json();

      // Create SIWE message
      const message = new SiweMessage({
        domain: window.location.host,
        address,
        statement: 'Sign in with Ethereum to the app.',
        uri: window.location.origin,
        version: '1',
        chainId: 1,
        nonce
      });

      const preparedMessage = message.prepareMessage();

      // Sign message
      const signature = await signMessageAsync({
        message: preparedMessage
      });

      // Verify signature
      const verifyRes = await fetch('/api/auth/verify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: preparedMessage,
          signature
        })
      });

      const { token } = await verifyRes.json();

      // Store token
      localStorage.setItem('auth_token', token);

      return token;
    } finally {
      setIsLoading(false);
    }
  };

  const signOut = () => {
    localStorage.removeItem('auth_token');
  };

  return { signIn, signOut, isLoading };
}

// Usage
function LoginButton() {
  const { signIn, isLoading } = useAuth();

  return (
    <button onClick={signIn} disabled={isLoading}>
      {isLoading ? 'Signing in...' : 'Sign in with Ethereum'}
    </button>
  );
}
```

## NextAuth.js + Web3

```typescript
// pages/api/auth/[...nextauth].ts
import NextAuth from 'next-auth';
import CredentialsProvider from 'next-auth/providers/credentials';
import { SiweMessage } from 'siwe';

export default NextAuth({
  providers: [
    CredentialsProvider({
      name: 'Ethereum',
      credentials: {
        message: { label: 'Message', type: 'text' },
        signature: { label: 'Signature', type: 'text' }
      },
      async authorize(credentials) {
        try {
          const siwe = new SiweMessage(credentials?.message || '');
          
          const result = await siwe.verify({
            signature: credentials?.signature || ''
          });

          if (!result.success) {
            return null;
          }

          return {
            id: siwe.address,
            address: siwe.address
          };
        } catch (error) {
          return null;
        }
      }
    })
  ],
  session: {
    strategy: 'jwt'
  },
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.address = user.address;
      }
      return token;
    },
    async session({ session, token }) {
      session.address = token.address;
      return session;
    }
  }
});

// Usage
import { useSession, signIn, signOut } from 'next-auth/react';

function AuthButton() {
  const { data: session } = useSession();

  if (session) {
    return (
      <div>
        <p>Signed in as {session.address}</p>
        <button onClick={() => signOut()}>Sign out</button>
      </div>
    );
  }

  return <button onClick={() => signIn('ethereum')}>Sign in</button>;
}
```

## Security Considerations

```typescript
// middleware/auth.middleware.ts
export function authMiddleware(
  req: NextApiRequest,
  res: NextApiResponse,
  next: () => void
) {
  const token = req.headers.authorization?.replace('Bearer ', '');

  if (!token) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  const session = sessionService.verifySession(token);

  if (!session) {
    return res.status(401).json({ error: 'Invalid token' });
  }

  // Attach address to request
  (req as any).userAddress = session.address;

  next();
}

// Rate limiting
import rateLimit from 'express-rate-limit';

const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 requests per window
  message: 'Too many authentication attempts'
});

// CSRF protection
import csrf from 'csurf';

const csrfProtection = csrf({ cookie: true });
```

## Best Practices

1. **Nonce Usage** - Use nonces to prevent replay attacks
2. **Message Expiry** - Set expiration times for messages
3. **Signature Verification** - Always verify signatures server-side
4. **Session Management** - Use secure session tokens
5. **HTTPS Only** - Always use HTTPS in production
6. **Rate Limiting** - Limit authentication attempts
7. **CSRF Protection** - Implement CSRF protection
8. **Secure Storage** - Store tokens securely
9. **Token Refresh** - Implement token refresh mechanism
10. **Audit Logging** - Log all authentication events

---

## Quick Start

### Sign-In with Ethereum (SIWE)

```typescript
import { SiweMessage } from 'siwe'

// Generate message
const message = new SiweMessage({
  domain: 'example.com',
  address: userAddress,
  statement: 'Sign in with Ethereum',
  uri: 'https://example.com',
  version: '1',
  chainId: 1,
  nonce: generateNonce(),
  expirationTime: new Date(Date.now() + 5 * 60 * 1000).toISOString()
})

const messageToSign = message.prepareMessage()

// User signs message with wallet
const signature = await wallet.signMessage(messageToSign)

// Verify on server
const siweMessage = new SiweMessage(messageToSign)
const result = await siweMessage.verify({ signature })
```

---

## Production Checklist

- [ ] **SIWE Implementation**: Sign-In with Ethereum
- [ ] **Nonce Usage**: Use nonces to prevent replay attacks
- [ ] **Message Expiry**: Set expiration times
- [ ] **Signature Verification**: Verify signatures server-side
- [ ] **Session Management**: Secure session tokens
- [ ] **HTTPS Only**: Always use HTTPS
- [ ] **Wallet Support**: Support multiple wallets
- [ ] **Error Handling**: Handle wallet errors
- [ ] **Testing**: Test with different wallets
- [ ] **Documentation**: Document auth flow
- [ ] **Security**: Security best practices
- [ ] **Compliance**: Meet compliance requirements

---

## Anti-patterns

### ❌ Don't: No Nonce

```typescript
// ❌ Bad - No nonce
const message = 'Sign in'
const signature = await wallet.signMessage(message)
// Replay attack possible!
```

```typescript
// ✅ Good - With nonce
const nonce = generateNonce()
const message = `Sign in with nonce: ${nonce}`
const signature = await wallet.signMessage(message)
// Nonce prevents replay
```

### ❌ Don't: Trust Client Verification

```typescript
// ❌ Bad - Client verification
const isValid = await verifySignatureOnClient(signature)
if (isValid) {
  login()  // Client can fake!
}
```

```typescript
// ✅ Good - Server verification
const isValid = await verifySignatureOnServer(signature, message)
if (isValid) {
  createSession(userAddress)
}
```

---

## Integration Points

- **Wallet Connection** (`35-blockchain-web3/wallet-connection/`) - Wallet integration
- **Web3 Integration** (`35-blockchain-web3/web3-integration/`) - Web3 patterns
- **OAuth2** (`10-authentication-authorization/oauth2/`) - Auth patterns

---

## Further Reading

- [Sign-In with Ethereum](https://login.xyz/)
- [EIP-4361](https://eips.ethereum.org/EIPS/eip-4361)

## Resources

- [Sign-In with Ethereum](https://login.xyz/)
- [SIWE Library](https://github.com/spruceid/siwe)
- [NextAuth.js](https://next-auth.js.org/)
- [Wagmi](https://wagmi.sh/)
- [EIP-4361](https://eips.ethereum.org/EIPS/eip-4361)
