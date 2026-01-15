# Error Tracking

A comprehensive guide to error tracking with Sentry and custom solutions for production applications.

## Table of Contents

1. [Error Tracking Concepts](#error-tracking-concepts)
2. [Sentry Setup](#sentry-setup)
3. [Frontend Integration (React)](#frontend-integration-react)
4. [Backend Integration (Node.js)](#backend-integration-nodejs)
5. [Backend Integration (Python)](#backend-integration-python)
6. [Error Capture](#error-capture)
7. [Source Maps](#source-maps)
8. [Releases and Environments](#releases-and-environments)
9. [User Feedback](#user-feedback)
10. [Performance Monitoring](#performance-monitoring)
11. [Alerts and Notifications](#alerts-and-notifications)
12. [Custom Error Handlers](#custom-error-handlers)
13. [Privacy Considerations](#privacy-considerations)
14. [Best Practices](#best-practices)

---

## Error Tracking Concepts

### Why Error Tracking Matters

```
Without Error Tracking:
- Users encounter errors → frustration → churn
- Developers unaware → bugs persist → technical debt
- No context → difficult to debug → slow resolution

With Error Tracking:
- Real-time alerts → immediate awareness
- Stack traces & context → faster debugging
- User impact analysis → prioritize fixes
- Trend analysis → prevent regressions
```

### Key Features

| Feature | Description |
|---------|-------------|
| **Real-time Alerts** | Get notified immediately when errors occur |
| **Stack Traces** | Detailed call stack with source code context |
| **Breadcrumbs** | User actions leading up to the error |
| **User Context** | User info, device, browser, IP |
| **Release Tracking** | Correlate errors with deployments |
| **Grouping** | Similar errors grouped together |
| **Performance Monitoring** | Track slow requests and transactions |
| **Source Maps** | Debug minified production code |

---

## Sentry Setup

### Self-Hosted Sentry

```yaml
# docker-compose.yml
version: '3.8'
services:
  sentry:
    image: sentry:latest
    container_name: sentry
    ports:
      - "9000:9000"
    environment:
      - SENTRY_SECRET_KEY=your-secret-key
      - SENTRY_POSTGRES_HOST=postgres
      - SENTRY_POSTGRES_PORT=5432
      - SENTRY_DB_USER=sentry
      - SENTRY_DB_PASSWORD=sentry
      - SENTRY_REDIS_HOST=redis
      - SENTRY_REDIS_PORT=6379
    depends_on:
      - postgres
      - redis
    volumes:
      - sentry-data:/var/lib/sentry/files

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_USER=sentry
      - POSTGRES_PASSWORD=sentry
      - POSTGRES_DB=sentry
    volumes:
      - postgres-data:/var/lib/postgresql/data

  redis:
    image: redis:7
    volumes:
      - redis-data:/data

volumes:
  sentry-data:
  postgres-data:
  redis-data:
```

### Cloud Sentry (SaaS)

```bash
# Create project at https://sentry.io
# Get DSN (Data Source Name)
# Example DSN: https://examplePublicKey@o0.ingest.sentry.io/0
```

### Configuration

```typescript
// sentry.config.ts
import * as Sentry from '@sentry/node';

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV || 'development',
  release: process.env.GIT_SHA || '1.0.0',
  tracesSampleRate: 0.1, // 10% of transactions
  integrations: [
    new Sentry.Integrations.Http({ tracing: true }),
    new Sentry.Integrations.Express({ app }),
    new Sentry.Integrations.Postgres(),
  ],
  beforeSend(event, hint) {
    // Filter out certain errors
    if (event.exception) {
      const error = hint.originalException;
      if (error instanceof Error && error.message.includes('ResizeObserver')) {
        return null; // Don't send this error
      }
    }
    return event;
  },
});
```

```python
# sentry.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration

sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    environment=os.environ.get('ENVIRONMENT', 'development'),
    release=os.environ.get('GIT_SHA', '1.0.0'),
    traces_sample_rate=0.1,
    integrations=[
        DjangoIntegration(),
        RedisIntegration(),
    ],
    before_send=event, hint=None:
        # Filter out certain errors
        if event.get('exception'):
            exception = event['exception']['values'][0]
            if 'ResizeObserver' in exception.get('value', ''):
                return None
        return event
)
```

---

## Frontend Integration (React)

### Installation

```bash
npm install @sentry/react @sentry/tracing
```

### Basic Setup

```tsx
// index.tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import * as Sentry from '@sentry/react';
import { BrowserTracing } from '@sentry/react';
import App from './App';

Sentry.init({
  dsn: process.env.REACT_APP_SENTRY_DSN,
  environment: process.env.NODE_ENV,
  release: process.env.REACT_APP_VERSION,
  integrations: [
    new BrowserTracing({
      tracingOrigins: ['localhost', 'https://api.example.com'],
    }),
  ],
  tracesSampleRate: 0.1,
});

const root = ReactDOM.createRoot(document.getElementById('root')!);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

### Error Boundary

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
  eventId?: string;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(): State {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    const eventId = Sentry.captureException(error, {
      contexts: {
        react: {
          componentStack: errorInfo.componentStack,
        },
      },
    });
    this.setState({ eventId });
  }

  render() {
    if (this.state.hasError) {
      return (
        this.props.fallback || (
          <div className="error-fallback">
            <h1>Something went wrong</h1>
            <p>We've been notified and are working on a fix.</p>
            <button onClick={() => window.location.reload()}>
              Reload Page
            </button>
          </div>
        )
      );
    }

    return this.props.children;
  }
}

// Usage
<ErrorBoundary>
  <App />
</ErrorBoundary>
```

### User Feedback

```tsx
// UserFeedbackDialog.tsx
import React from 'react';
import * as Sentry from '@sentry/react';

export function UserFeedbackDialog({ eventId }: { eventId: string }) {
  const [email, setEmail] = React.useState('');
  const [message, setMessage] = React.useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    Sentry.captureUserFeedback({
      event_id: eventId,
      email,
      comments: message,
    });
    alert('Thank you for your feedback!');
  };

  return (
    <form onSubmit={handleSubmit}>
      <h3>Report Issue</h3>
      <input
        type="email"
        placeholder="your@email.com"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <textarea
        placeholder="What happened?"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
      />
      <button type="submit">Submit</button>
    </form>
  );
}
```

---

## Backend Integration (Node.js)

### Express Integration

```typescript
// app.ts
import express from 'express';
import * as Sentry from '@sentry/node';
import { ProfilingIntegration } from '@sentry/profiling-node';

const app = express();

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,
  release: process.env.GIT_SHA,
  integrations: [
    new Sentry.Integrations.Http({ tracing: true }),
    new Sentry.Integrations.Express({ app }),
    new ProfilingIntegration(),
  ],
  tracesSampleRate: 0.1,
  profilesSampleRate: 0.1,
});

// Request handler
app.use(Sentry.Handlers.requestHandler());

// Error handler
app.use(Sentry.Handlers.errorHandler());

// Routes
app.get('/', (req, res) => {
  res.send('Hello World');
});

// 404 handler
app.use(Sentry.Handlers.errorHandler());

app.listen(3000);
```

### Custom Error Capture

```typescript
import * as Sentry from '@sentry/node';

class CustomError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number = 500
  ) {
    super(message);
    this.name = 'CustomError';
  }
}

async function handleRequest(req, res) {
  try {
    // ... do work ...
  } catch (error) {
    if (error instanceof CustomError) {
      Sentry.captureException(error, {
        tags: {
          error_code: error.code,
        },
        extra: {
          statusCode: error.statusCode,
        },
      });
      res.status(error.statusCode).json({ error: error.message });
    } else {
      Sentry.captureException(error);
      res.status(500).json({ error: 'Internal server error' });
    }
  }
}
```

### Async Error Tracking

```typescript
import * as Sentry from '@sentry/node';

// Track unhandled promise rejections
process.on('unhandledRejection', (reason, promise) => {
  Sentry.captureException(reason, {
    tags: {
      rejection: true,
    },
    extra: {
      promise: String(promise),
    },
  });
});

// Track uncaught exceptions
process.on('uncaughtException', (error) => {
  Sentry.captureException(error);
  process.exit(1);
});
```

---

## Backend Integration (Python)

### Django Integration

```python
# settings.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    environment=os.environ.get('ENVIRONMENT'),
    release=os.environ.get('GIT_SHA'),
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.1,
)

# views.py
from django.http import JsonResponse
import sentry_sdk

def my_view(request):
    try:
        # ... do work ...
        pass
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return JsonResponse({'error': str(e)}, status=500)
```

### FastAPI Integration

```python
# main.py
from fastapi import FastAPI
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    integrations=[FastApiIntegration()],
    traces_sample_rate=0.1,
)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

### Custom Error Capture

```python
import sentry_sdk

class CustomError(Exception):
    def __init__(self, message, code, status_code=500):
        super().__init__(message)
        self.code = code
        self.status_code = status_code

def handle_request():
    try:
        # ... do work ...
        pass
    except CustomError as e:
        sentry_sdk.capture_exception(e, tags={
            'error_code': e.code
        }, extra={
            'status_code': e.status_code
        })
        raise
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise
```

---

## Error Capture

### Manual Capture

```typescript
import * as Sentry from '@sentry/node';

// Capture exception
try {
  // ... code that may throw ...
} catch (error) {
  Sentry.captureException(error);
}

// Capture message
Sentry.captureMessage('User clicked button', 'info');

// Capture with context
Sentry.captureException(error, {
  tags: {
    section: 'checkout',
    user_type: 'premium',
  },
  extra: {
    userId: '123',
    cartItems: 5,
  },
  user: {
    id: '123',
    email: 'user@example.com',
  },
});
```

```python
import sentry_sdk

# Capture exception
try:
    # ... code that may raise ...
except Exception as e:
    sentry_sdk.capture_exception(e)

# Capture message
sentry_sdk.capture_message('User clicked button', level='info')

# Capture with context
sentry_sdk.capture_exception(e, tags={
    'section': 'checkout',
    'user_type': 'premium'
}, extra={
    'user_id': '123',
    'cart_items': 5
}, user={
    'id': '123',
    'email': 'user@example.com'
})
```

### Breadcrumbs

```typescript
// Add breadcrumb
Sentry.addBreadcrumb({
  category: 'user',
  message: 'User clicked checkout button',
  level: 'info',
  data: {
    userId: '123',
    cartValue: 99.99,
  },
});

// Automatic breadcrumbs from navigation
Sentry.addBreadcrumb({
  category: 'navigation',
  message: 'Navigated to /checkout',
  level: 'info',
});
```

```python
# Add breadcrumb
sentry_sdk.add_breadcrumb(
    category='user',
    message='User clicked checkout button',
    level='info',
    data={
        'user_id': '123',
        'cart_value': 99.99
    }
)
```

### Context Management

```typescript
// Set user context
Sentry.setUser({
  id: '123',
  email: 'user@example.com',
  username: 'johndoe',
  ip_address: '192.168.1.1',
});

// Set tags
Sentry.setTag('environment', 'production');
Sentry.setTag('plan', 'premium');

// Set extra context
Sentry.setContext('cart', {
  items: 5,
  total: 99.99,
  currency: 'USD',
});

// Clear context
Sentry.setUser(null);
```

```python
# Set user context
sentry_sdk.set_user({
    'id': '123',
    'email': 'user@example.com',
    'username': 'johndoe',
    'ip_address': '192.168.1.1'
})

# Set tags
sentry_sdk.set_tag('environment', 'production')
sentry_sdk.set_tag('plan', 'premium')

# Set extra context
sentry_sdk.set_context('cart', {
    'items': 5,
    'total': 99.99,
    'currency': 'USD'
})

# Clear context
sentry_sdk.set_user(None)
```

---

## Source Maps

### Uploading Source Maps

```bash
# Using Sentry CLI
npm install -g @sentry/cli

sentry-cli releases new $VERSION
sentry-cli releases upload-sourcemaps $VERSION ./build
sentry-cli releases finalize $VERSION
```

### Webpack Integration

```javascript
// webpack.config.js
const { sentryWebpackPlugin } = require('@sentry/webpack-plugin');

module.exports = {
  plugins: [
    sentryWebpackPlugin({
      authToken: process.env.SENTRY_AUTH_TOKEN,
      org: 'your-org',
      project: 'your-project',
      release: process.env.GIT_SHA,
      include: './dist',
    }),
  ],
};
```

### Vite Integration

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import sentry from '@sentry/vite-plugin';

export default defineConfig({
  plugins: [
    sentry({
      org: 'your-org',
      project: 'your-project',
      authToken: process.env.SENTRY_AUTH_TOKEN,
      release: process.env.GIT_SHA,
    }),
  ],
});
```

---

## Releases and Environments

### Creating Releases

```typescript
// Set release in Sentry.init
Sentry.init({
  dsn: process.env.SENTRY_DSN,
  release: process.env.GIT_SHA || '1.0.0',
  environment: process.env.NODE_ENV || 'development',
});
```

### Deploying Releases

```bash
# Associate commits with release
sentry-cli releases set-commits $VERSION --auto

# Create deployment
sentry-cli releases deploys $VERSION new -e production
```

### Environment-Specific Configuration

```typescript
const config = {
  development: {
    dsn: process.env.SENTRY_DSN,
    environment: 'development',
    tracesSampleRate: 1.0, // Trace everything in dev
  },
  staging: {
    dsn: process.env.SENTRY_DSN,
    environment: 'staging',
    tracesSampleRate: 0.5,
  },
  production: {
    dsn: process.env.SENTRY_DSN,
    environment: 'production',
    tracesSampleRate: 0.1, // Sample 10% in production
  },
};

Sentry.init(config[process.env.NODE_ENV || 'development']);
```

---

## User Feedback

### Sentry User Feedback Widget

```tsx
import { useSentry } from '@sentry/react';

export function FeedbackButton() {
  const { showReportDialog } = useSentry();

  return (
    <button onClick={() => showReportDialog()}>
      Report an Issue
    </button>
  );
}
```

### Custom Feedback Form

```tsx
import React from 'react';
import * as Sentry from '@sentry/react';

export function CustomFeedbackForm({ eventId }: { eventId: string }) {
  const [email, setEmail] = React.useState('');
  const [comments, setComments] = React.useState('');
  const [submitted, setSubmitted] = React.useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    Sentry.captureUserFeedback({
      event_id: eventId,
      email,
      comments,
    });
    setSubmitted(true);
  };

  if (submitted) {
    return <p>Thank you for your feedback!</p>;
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        placeholder="Email (optional)"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <textarea
        placeholder="What happened?"
        value={comments}
        onChange={(e) => setComments(e.target.value)}
        required
      />
      <button type="submit">Submit Feedback</button>
    </form>
  );
}
```

---

## Performance Monitoring

### Transaction Tracking

```typescript
import * as Sentry from '@sentry/node';

async function processOrder(orderId: string) {
  const transaction = Sentry.startTransaction({
    op: 'processOrder',
    name: 'Process Order',
  });

  try {
    const validateSpan = transaction.startChild({
      op: 'validation',
      description: 'Validate order',
    });

    await validateOrder(orderId);
    validateSpan.finish();

    const paymentSpan = transaction.startChild({
      op: 'payment',
      description: 'Process payment',
    });

    await processPayment(orderId);
    paymentSpan.finish();

    return { success: true };
  } catch (error) {
    transaction.setStatus('internal_error');
    throw error;
  } finally {
    transaction.finish();
  }
}
```

### React Performance

```tsx
import * as Sentry from '@sentry/react';

export function UserProfile({ userId }: { userId: string }) {
  const transaction = Sentry.startTransaction({
    name: 'UserProfile',
    op: 'component',
  });

  React.useEffect(() => {
    return () => transaction.finish();
  }, []);

  return <div>User Profile</div>;
}
```

---

## Alerts and Notifications

### Alert Rules

```typescript
// Configure via Sentry UI or API
// Example: Alert when error rate > 1% for 5 minutes

// Create alert via API
const response = await fetch(
  `https://sentry.io/api/0/projects/${org}/${project}/rules/`,
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      name: 'High Error Rate Alert',
      conditions: [
        {
          id: 'sentry.rules.conditions.high_error_rate.HighErrorRateCondition',
          interval: '1h',
          threshold: 0.01,
        },
      ],
      actions: [
        {
          id: 'sentry.rules.actions.notify_event.NotifyEventAction',
          targetType: 'member',
          targetIdentifier: userId,
        },
      ],
    }),
  }
);
```

### Slack Integration

```typescript
// Configure Slack webhook in Sentry settings
// Or use custom notification

async function sendSlackAlert(error: Sentry.Event) {
  await fetch(process.env.SLACK_WEBHOOK_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text: `🚨 New Error: ${error.message}`,
      attachments: [
        {
          color: 'danger',
          fields: [
            { title: 'Environment', value: error.environment, short: true },
            { title: 'Release', value: error.release, short: true },
            { title: 'Error ID', value: error.event_id, short: true },
          ],
        },
      ],
    }),
  });
}

Sentry.init({
  beforeSend(event) {
    if (event.level === 'error') {
      sendSlackAlert(event);
    }
    return event;
  },
});
```

---

## Custom Error Handlers

### Express Error Handler

```typescript
import * as Sentry from '@sentry/node';

export function errorHandler(
  err: Error,
  req: express.Request,
  res: express.Response,
  next: express.NextFunction
) {
  // Capture error
  Sentry.captureException(err, {
    extra: {
      url: req.url,
      method: req.method,
      body: req.body,
      query: req.query,
      headers: req.headers,
    },
  });

  // Send response
  res.status(500).json({
    error: {
      message: process.env.NODE_ENV === 'production'
        ? 'Internal server error'
        : err.message,
      eventId: Sentry.lastEventId(),
    },
  });
}

// Usage
app.use(errorHandler);
```

### Django Error Handler

```python
# middleware.py
import sentry_sdk
from django.http import JsonResponse

class SentryErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        sentry_sdk.capture_exception(exception, extra={
            'url': request.path,
            'method': request.method,
            'user': str(request.user),
        })
        return JsonResponse({
            'error': 'Internal server error',
            'event_id': sentry_sdk.last_event_id()
        }, status=500)
```

---

## Privacy Considerations

### Filtering Sensitive Data

```typescript
Sentry.init({
  dsn: process.env.SENTRY_DSN,
  beforeSend(event, hint) {
    // Remove sensitive data
    if (event.request) {
      delete event.request.cookies;
      delete event.request.headers?.['authorization'];
      delete event.request.headers?.['cookie'];
    }

    // Scrub PII from extra data
    if (event.extra) {
      delete event.extra.password;
      delete event.extra.creditCard;
      delete event.extra.ssn;
    }

    return event;
  },
});
```

```python
sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    before_send=event, hint=None:
        # Remove sensitive data
        if 'request' in event:
            event['request'].pop('cookies', None)
            if 'headers' in event['request']:
                event['request']['headers'].pop('authorization', None)
                event['request']['headers'].pop('cookie', None)

        # Scrub PII from extra data
        if 'extra' in event:
            event['extra'].pop('password', None)
            event['extra'].pop('credit_card', None)
            event['extra'].pop('ssn', None)

        return event
)
```

### GDPR Compliance

```typescript
// User data deletion
async function deleteUser(userId: string) {
  // Delete from database
  await db.users.delete({ where: { id: userId } });

  // Delete from Sentry
  await fetch(
    `https://sentry.io/api/0/organizations/${org}/user-feedback/?query=${userId}`,
    {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${token}` },
    }
  );
}
```

---

## Best Practices

### 1. Set Appropriate Sampling Rates

```typescript
// Development: Capture everything
// Production: Sample to reduce costs
const tracesSampleRate = process.env.NODE_ENV === 'production' ? 0.1 : 1.0;
```

### 2. Use Meaningful Tags

```typescript
Sentry.setTag('feature', 'checkout');
Sentry.setTag('user_tier', 'premium');
Sentry.setTag('api_version', 'v2');
```

### 3. Add Context to Errors

```typescript
Sentry.captureException(error, {
  extra: {
    userId: user.id,
    cartValue: cart.total,
    paymentMethod: cart.method,
  },
});
```

### 4. Don't Capture Expected Errors

```typescript
try {
  const user = await getUser(id);
  if (!user) {
    // Expected error, don't send to Sentry
    throw new NotFoundError('User not found');
  }
} catch (error) {
  if (!(error instanceof NotFoundError)) {
    Sentry.captureException(error);
  }
  throw error;
}
```

### 5. Use Source Maps in Production

```bash
# Always upload source maps for production builds
sentry-cli releases upload-sourcemaps $VERSION ./dist
```

### 6. Monitor Performance

```typescript
// Track critical transactions
Sentry.startTransaction({
  name: 'checkout',
  op: 'transaction',
});
```

### 7. Set Up Alerts

```typescript
// Alert on critical errors
// Alert on high error rates
// Alert on performance degradation
```

### 8. Review Errors Regularly

```typescript
// Set up weekly error review meetings
// Prioritize by user impact
// Track error trends over time
```

---

## Resources

- [Sentry Documentation](https://docs.sentry.io/)
- [Sentry JavaScript SDK](https://docs.sentry.io/platforms/javascript/)
- [Sentry Python SDK](https://docs.sentry.io/platforms/python/)
- [Source Maps Guide](https://docs.sentry.io/platforms/javascript/sourcemaps/)
