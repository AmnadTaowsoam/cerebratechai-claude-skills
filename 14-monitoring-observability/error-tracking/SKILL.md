# Error Tracking

## Overview

Error tracking helps you identify, diagnose, and fix errors in your applications. This skill covers Sentry setup, error capture, releases, and best practices.

## Table of Contents

1. [Error Tracking Concepts](#error-tracking-concepts)
2. [Sentry Setup](#sentry-setup)
3. [Error Capture](#error-capture)
4. [Source Maps](#source-maps)
5. [Releases and Environments](#releases-and-environments)
6. [User Feedback](#user-feedback)
7. [Performance Monitoring](#performance-monitoring)
8. [Alerts and Notifications](#alerts-and-notifications)
9. [Custom Error Handlers](#custom-error-handlers)
10. [Privacy Considerations](#privacy-considerations)
11. [Best Practices](#best-practices)

---

## Error Tracking Concepts

### Why Track Errors?

1. **Proactive Detection**: Know about errors before users report them
2. **Context**: Get stack traces, user info, and environment details
3. **Prioritization**: Focus on high-impact errors
4. **Trends**: Track error rates over time
5. **Releases**: Correlate errors with deployments

### Key Concepts

| Concept | Description |
|---------|-------------|
| **Event** | A single error occurrence |
| **Issue** | Group of similar events |
| **Project** | Application or service being tracked |
| **Release** | Version of your application |
| **Environment** | Development, staging, production |
| **Breadcrumbs** | Trail of events leading to error |
| **Context** | Additional data (user, request, tags) |

---

## Sentry Setup

### Frontend (React)

```bash
npm install @sentry/react
```

```tsx
// src/sentry.ts
import * as Sentry from '@sentry/react';
import { BrowserTracing } from '@sentry/tracing';

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  integrations: [
    new BrowserTracing({
      tracePropagationTargets: ['localhost', /^https:\/\/yourdomain\.com/],
    }),
    new Sentry.Replay({
      maskAllText: true,
      blockAllMedia: true,
    }),
  ],
  tracesSampleRate: 1.0,
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
  environment: process.env.NODE_ENV,
  release: process.env.APP_VERSION,
  beforeSend(event, hint) {
    // Filter out certain errors
    if (event.exception) {
      const error = hint.originalException;
      if (error instanceof Error && error.message.includes('ResizeObserver')) {
        return null; // Don't send
      }
    }
    return event;
  },
});

// src/index.tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './sentry';

const root = ReactDOM.createRoot(document.getElementById('root')!);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

### Backend (Node.js)

```bash
npm install @sentry/node
```

```typescript
// sentry.ts
import * as Sentry from '@sentry/node';
import { nodeProfilingIntegration } from '@sentry/profiling-node';

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  integrations: [
    nodeProfilingIntegration(),
  ],
  tracesSampleRate: 1.0,
  profilesSampleRate: 1.0,
  environment: process.env.NODE_ENV,
  release: process.env.APP_VERSION,
});

// Express middleware
import express from 'express';

const app = express();

// Sentry request handler
app.use(Sentry.Handlers.requestHandler());

// Sentry error handler
app.use(Sentry.Handlers.errorHandler());
```

### Backend (Python)

```bash
pip install sentry-sdk
```

```python
# sentry.py
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    integrations=[
        FlaskIntegration(),
    ],
    traces_sample_rate=1.0,
    environment=os.getenv('NODE_ENV', 'production'),
    release=os.getenv('APP_VERSION', '1.0.0'),
)

# Flask app
from flask import Flask

app = Flask(__name__)
```

---

## Error Capture

### Automatic Error Capture

```typescript
// React - Automatic capture
// No additional code needed
// Errors in components are automatically captured

// Node.js - Automatic capture
// Uncaught exceptions and unhandled rejections are captured
```

```python
# Python - Automatic capture
# Uncaught exceptions are automatically captured
```

### Manual Error Capture

```typescript
// manual-capture.ts
import * as Sentry from '@sentry/react';

// Capture exception
try {
  throw new Error('Something went wrong');
} catch (error) {
  Sentry.captureException(error);
}

// Capture message
Sentry.captureMessage('User performed action X');

// Capture with context
Sentry.captureException(new Error('Database connection failed'), {
  tags: {
    component: 'database',
    action: 'connect',
  },
  user: {
    id: '123',
    email: 'user@example.com',
  },
  extra: {
    database: 'production',
    host: 'db.example.com',
  },
});

// Capture with level
Sentry.captureException(error, {
  level: 'warning', // fatal, error, warning, log, info, debug
});
```

```python
# manual_capture.py
import sentry_sdk

# Capture exception
try:
    raise Exception('Something went wrong')
except Exception as error:
    sentry_sdk.capture_exception(error)

# Capture message
sentry_sdk.capture_message('User performed action X')

# Capture with context
sentry_sdk.capture_exception(
    error,
    tags={
        'component': 'database',
        'action': 'connect'
    },
    user={
        'id': '123',
        'email': 'user@example.com'
    },
    extra={
        'database': 'production',
        'host': 'db.example.com'
    },
    level='warning'  # fatal, error, warning, log, info, debug
)
```

### Error Boundaries (React)

```tsx
// ErrorBoundary.tsx
import React, { Component, ErrorInfo, ReactNode } from 'react';
import * as Sentry from '@sentry/react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(): State {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    Sentry.captureException(error, {
      contexts: {
        react: {
          componentStack: errorInfo.componentStack,
        },
      },
    });
  }

  render(): ReactNode {
    if (this.state.hasError) {
      return this.props.fallback || <div>Something went wrong.</div>;
    }

    return this.props.children;
  }
}

// Usage
<ErrorBoundary fallback={<ErrorFallback />}>
  <App />
</ErrorBoundary>
```

---

## Source Maps

### Upload Source Maps

```bash
# Using Sentry CLI
npm install -g @sentry/cli

sentry-cli releases \
  files VERSION \
  upload-sourcemaps ./build \
  --url-prefix '~/static/js' \
  --validate
```

```typescript
// webpack.config.js
const SentryWebpackPlugin = require('@sentry/webpack-plugin');

module.exports = {
  // ... other config
  devtool: 'source-map',
  plugins: [
    new SentryWebpackPlugin({
      authToken: process.env.SENTRY_AUTH_TOKEN,
      org: 'your-org',
      project: 'your-project',
      release: process.env.APP_VERSION,
      include: './build',
      ignore: ['node_modules'],
      urlPrefix: '~/',
    }),
  ],
};
```

### Vite Configuration

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import sentryVitePlugin from '@sentry/vite-plugin';

export default defineConfig({
  plugins: [
    sentryVitePlugin({
      org: 'your-org',
      project: 'your-project',
      authToken: process.env.SENTRY_AUTH_TOKEN,
    }),
  ],
  build: {
    sourcemap: true,
  },
});
```

---

## Releases and Environments

### Create Release

```bash
# Using Sentry CLI
sentry-cli releases new VERSION
sentry-cli releases set-commits --auto VERSION
sentry-cli releases finalize VERSION
sentry-cli releases deploy VERSION --env production
```

```typescript
// Node.js
Sentry.setRelease(process.env.APP_VERSION);
Sentry.setEnvironment(process.env.NODE_ENV);
```

```python
# Python
sentry_sdk.set_release(os.getenv('APP_VERSION'))
sentry_sdk.set_environment(os.getenv('NODE_ENV'))
```

### Release Health

```typescript
// Track release health
Sentry.captureMessage('Release deployed', {
  level: 'info',
  release: process.env.APP_VERSION,
  environment: process.env.NODE_ENV,
});
```

---

## User Feedback

### User Feedback Widget

```tsx
// UserFeedback.tsx
import * as Sentry from '@sentry/react';
import { useFeedback } from '@sentry/react';

function UserFeedbackButton() {
  const { feedback } = useFeedback();

  return (
    <button
      onClick={() => {
        feedback({
          name: 'Report Issue',
          email: 'user@example.com',
          message: 'Describe the issue...',
        });
      }}
    >
      Report Issue
    </button>
  );
}
```

### Custom Feedback Form

```tsx
// CustomFeedback.tsx
import * as Sentry from '@sentry/react';

function CustomFeedback() {
  const [message, setMessage] = React.useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    Sentry.captureFeedback({
      name: 'User Feedback',
      email: 'user@example.com',
      comments: message,
    });

    setMessage('');
  };

  return (
    <form onSubmit={handleSubmit}>
      <textarea
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Describe the issue..."
      />
      <button type="submit">Submit</button>
    </form>
  );
}
```

---

## Performance Monitoring

### Web Vitals

```tsx
// WebVitals.tsx
import { onCLS, onFID, onFCP, onLCP, onTTFB } from 'web-vitals';
import * as Sentry from '@sentry/react';

onCLS((metric) => {
  Sentry.captureMessage('CLS', {
    level: 'info',
    extra: { metric },
  });
});

onFID((metric) => {
  Sentry.captureMessage('FID', {
    level: 'info',
    extra: { metric },
  });
});

onFCP((metric) => {
  Sentry.captureMessage('FCP', {
    level: 'info',
    extra: { metric },
  });
});

onLCP((metric) => {
  Sentry.captureMessage('LCP', {
    level: 'info',
    extra: { metric },
  });
});

onTTFB((metric) => {
  Sentry.captureMessage('TTFB', {
    level: 'info',
    extra: { metric },
  });
});
```

### Custom Performance Metrics

```typescript
// performance.ts
import * as Sentry from '@sentry/react';

// Start a transaction
const transaction = Sentry.startTransaction({
  op: 'http',
  name: 'GET /api/users',
});

// Add spans
const dbSpan = transaction.startChild({
  op: 'db',
  description: 'SELECT * FROM users',
});

await db.query('SELECT * FROM users');
dbSpan.finish();

// Finish transaction
transaction.finish();
```

---

## Alerts and Notifications

### Alert Rules

```typescript
// Configure in Sentry UI
// 1. Go to Settings > Alerts
// 2. Create new alert rule
// 3. Configure conditions (e.g., error rate > 10%)
// 4. Set notification channels
```

### Notification Channels

```typescript
// Slack
// Configure in Sentry UI
// Settings > Integrations > Slack

// Email
// Configure in Sentry UI
// Settings > Notifications > Email

// PagerDuty
// Configure in Sentry UI
// Settings > Integrations > PagerDuty
```

---

## Custom Error Handlers

### Express Error Handler

```typescript
// express-error-handler.ts
import express from 'express';
import * as Sentry from '@sentry/node';

app.use((err: Error, req: express.Request, res: express.Response, next: express.NextFunction) => {
  // Capture error
  Sentry.captureException(err, {
    tags: {
      route: req.path,
      method: req.method,
    },
    extra: {
      body: req.body,
      query: req.query,
      headers: req.headers,
    },
  });

  // Send response
  res.status(500).json({
    error: 'Internal server error',
    requestId: res.getHeader('x-request-id'),
  });
});
```

### Flask Error Handler

```python
# flask_error_handler.py
from flask import Flask, jsonify
import sentry_sdk

app = Flask(__name__)

@app.errorhandler(Exception)
def handle_exception(error):
    # Capture error
    sentry_sdk.capture_exception(error)
    
    # Send response
    return jsonify({
        'error': 'Internal server error',
        'request_id': request.headers.get('X-Request-ID')
    }), 500
```

---

## Privacy Considerations

### PII Redaction

```typescript
// pii-redaction.ts
import * as Sentry from '@sentry/react';

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  beforeSend(event, hint) {
    // Redact PII
    if (event.user) {
      delete event.user.email;
      delete event.user.ip_address;
    }

    // Redact sensitive data
    if (event.request?.headers) {
      delete event.request.headers.authorization;
      delete event.request.headers.cookie;
    }

    // Redact request body
    if (event.request?.data) {
      event.request.data = redactPII(event.request.data);
    }

    return event;
  },
});

function redactPII(data: any): any {
  if (typeof data !== 'object' || data === null) {
    return data;
  }

  const sensitiveFields = ['password', 'creditCard', 'ssn', 'token'];

  const redacted: any = {};
  for (const [key, value] of Object.entries(data)) {
    if (sensitiveFields.some(field => key.toLowerCase().includes(field))) {
      redacted[key] = '[REDACTED]';
    } else {
      redacted[key] = redactPII(value);
    }
  }

  return redacted;
}
```

```python
# pii_redaction.py
import sentry_sdk

SENSITIVE_FIELDS = ['password', 'credit_card', 'ssn', 'token']

def redact_pii(data):
    """Redact personally identifiable information."""
    if not isinstance(data, dict):
        return data
    
    redacted = {}
    for key, value in data.items():
        if any(field in key.lower() for field in SENSITIVE_FIELDS):
            redacted[key] = '[REDACTED]'
        else:
            redacted[key] = redact_pii(value)
    
    return redacted

def before_send(event, hint):
    """Redact PII before sending event."""
    if event.get('user'):
        event['user'].pop('email', None)
        event['user'].pop('ip_address', None)
    
    if event.get('request', {}).get('headers'):
        event['request']['headers'].pop('authorization', None)
        event['request']['headers'].pop('cookie', None)
    
    if event.get('request', {}).get('data'):
        event['request']['data'] = redact_pii(event['request']['data'])
    
    return event

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    before_send=before_send
)
```

### GDPR Compliance

```typescript
// gdpr-compliance.ts
import * as Sentry from '@sentry/react';

// Delete user data
async function deleteUserData(userId: string): Promise<void> {
  // Delete from your database
  await db.user.delete({ where: { id: userId }});

  // Delete from Sentry
  await fetch(`https://sentry.io/api/0/organizations/ORG/users/${userId}/`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${process.env.SENTRY_AUTH_TOKEN}`,
    },
  });
}
```

---

## Best Practices

### 1. Use Appropriate Error Levels

```typescript
// error-levels.ts
// Fatal: Application cannot continue
Sentry.captureException(fatalError, { level: 'fatal' });

// Error: Application can continue but functionality is broken
Sentry.captureException(error, { level: 'error' });

// Warning: Application works but something is wrong
Sentry.captureException(warning, { level: 'warning' });

// Info: Important information
Sentry.captureMessage('User logged in', { level: 'info' });

// Debug: Detailed debugging information
Sentry.captureMessage('Cache hit', { level: 'debug' });
```

### 2. Add Context to Errors

```typescript
// error-context.ts
Sentry.captureException(error, {
  tags: {
    component: 'api',
    route: '/users',
    method: 'GET',
  },
  user: {
    id: userId,
    username: user.username,
  },
  extra: {
    request_id: requestId,
    timestamp: new Date().toISOString(),
  },
});
```

### 3. Filter Noise

```typescript
// filter-noise.ts
Sentry.init({
  beforeSend(event, hint) {
    // Filter out third-party errors
    if (event.exception) {
      const error = hint.originalException as Error;
      if (error.message.includes('ResizeObserver')) {
        return null;
      }
      if (error.message.includes('Non-Error promise rejection')) {
        return null;
      }
    }

    return event;
  },
});
```

### 4. Set Release and Environment

```typescript
// release-env.ts
Sentry.init({
  release: process.env.APP_VERSION,
  environment: process.env.NODE_ENV,
});
```

### 5. Use Breadcrumbs

```typescript
// breadcrumbs.ts
import * as Sentry from '@sentry/react';

// Add breadcrumb
Sentry.addBreadcrumb({
  category: 'user',
  message: 'User clicked button',
  level: 'info',
  data: {
    button: 'submit',
    form: 'login',
  },
});

// Automatic breadcrumbs (navigation, HTTP requests, etc.)
// are enabled by default
```

---

## Summary

This skill covers comprehensive error tracking implementation including:

- **Error Tracking Concepts**: Why track errors and key concepts
- **Sentry Setup**: Frontend (React), backend (Node.js, Python)
- **Error Capture**: Automatic and manual error capture, error boundaries
- **Source Maps**: Uploading and configuring source maps
- **Releases and Environments**: Creating releases and tracking health
- **User Feedback**: Feedback widget and custom forms
- **Performance Monitoring**: Web vitals and custom performance metrics
- **Alerts and Notifications**: Alert rules and notification channels
- **Custom Error Handlers**: Express and Flask error handlers
- **Privacy Considerations**: PII redaction and GDPR compliance
- **Best Practices**: Error levels, context, filtering, releases, breadcrumbs
