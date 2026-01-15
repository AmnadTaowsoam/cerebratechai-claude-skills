---
name: Deprecation Policy
description: Structured approach to deprecating features, APIs, and systems with clear timelines and migration paths.
---

# Deprecation Policy

## Overview

Deprecation Policy defines how features, APIs, and systems are phased out in a controlled manner, giving users time to migrate while reducing maintenance burden.

**Core Principle**: "Deprecate gracefully. Give users time, tools, and alternatives."

---

## 1. Deprecation Timeline

```markdown
## Standard Deprecation Timeline (6 months)

**Month 0**: Announcement
- Announce deprecation publicly
- Document replacement
- Add deprecation warnings

**Month 2**: Sunset for new users
- Block new integrations
- Existing users can continue

**Month 4**: Final warning
- Increase warning visibility
- Email all affected users

**Month 6**: Removal
- Remove deprecated feature
- Monitor for issues
```

---

## 2. Deprecation Announcement Template

```markdown
# Deprecation Notice: Legacy Authentication API

## Summary
The legacy authentication API (`/api/v1/auth`) will be deprecated on **July 15, 2024**.

## Reason
The legacy API lacks modern security features (OAuth2, MFA) and is difficult to maintain.

## Replacement
Use the new authentication API (`/api/v2/auth`) which provides:
- OAuth2 support
- Multi-factor authentication
- Better rate limiting
- Improved error messages

## Migration Guide
See [Migration Guide](./migration-guide.md) for step-by-step instructions.

## Timeline
- **Jan 15, 2024**: Deprecation announced
- **Apr 15, 2024**: New integrations blocked
- **Jul 15, 2024**: API removed

## Support
Contact support@company.com for migration assistance.
```

---

## 3. Deprecation Warnings

### API Response Headers
```typescript
app.get('/api/v1/auth/login', (req, res) => {
  // Add deprecation headers
  res.set('Deprecation', 'true');
  res.set('Sunset', 'Sat, 15 Jul 2024 00:00:00 GMT');
  res.set('Link', '</api/v2/auth/login>; rel="successor-version"');
  
  // Log usage for tracking
  logger.warn('Deprecated API called', {
    endpoint: '/api/v1/auth/login',
    userId: req.user?.id,
    ip: req.ip
  });
  
  // Return response
  res.json({ token: generateToken() });
});
```

### Code Warnings (TypeScript)
```typescript
/**
 * @deprecated Use `newFunction()` instead. Will be removed in v3.0.0
 */
export function oldFunction() {
  console.warn('oldFunction is deprecated. Use newFunction instead.');
  return newFunction();
}
```

### Runtime Warnings (Python)
```python
import warnings

def old_function():
    warnings.warn(
        "old_function is deprecated, use new_function instead",
        DeprecationWarning,
        stacklevel=2
    )
    return new_function()
```

---

## 4. Migration Guide Template

```markdown
# Migration Guide: v1 to v2 Authentication API

## Overview
This guide helps you migrate from the deprecated v1 auth API to v2.

## Changes Summary
| Feature | v1 | v2 |
|---------|----|----|
| Endpoint | `/api/v1/auth/login` | `/api/v2/auth/login` |
| Auth Method | API Key | OAuth2 |
| Response Format | `{ token }` | `{ access_token, refresh_token }` |

## Step-by-Step Migration

### Step 1: Update Endpoint
```diff
- const response = await fetch('/api/v1/auth/login', {
+ const response = await fetch('/api/v2/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password })
  });
```

### Step 2: Handle New Response Format
```diff
  const data = await response.json();
- const token = data.token;
+ const accessToken = data.access_token;
+ const refreshToken = data.refresh_token;
```

### Step 3: Implement Token Refresh
```typescript
async function refreshAccessToken(refreshToken: string) {
  const response = await fetch('/api/v2/auth/refresh', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${refreshToken}` }
  });
  return await response.json();
}
```

## Testing
Test your integration in staging before deploying to production.

## Rollback Plan
If issues arise, you can temporarily revert to v1 until July 15, 2024.
```

---

## 5. Tracking Deprecated Usage

```typescript
// Track deprecated API usage
class DeprecationTracker {
  private usageStats = new Map<string, number>();
  
  track(endpoint: string, userId?: string) {
    const key = `${endpoint}:${userId || 'anonymous'}`;
    this.usageStats.set(key, (this.usageStats.get(key) || 0) + 1);
    
    // Log to analytics
    analytics.track('deprecated_api_usage', {
      endpoint,
      userId,
      timestamp: new Date()
    });
  }
  
  async getTopUsers(endpoint: string, limit: number = 10) {
    // Return top users still using deprecated endpoint
    return Array.from(this.usageStats.entries())
      .filter(([key]) => key.startsWith(endpoint))
      .sort((a, b) => b[1] - a[1])
      .slice(0, limit);
  }
}
```

---

## 6. Communicating Deprecation

### Email Template
```markdown
Subject: Action Required: Migrate from Legacy Auth API by July 15

Hi [Customer Name],

We're reaching out because your application is using our legacy authentication API, which will be deprecated on **July 15, 2024**.

**What you need to do:**
1. Review our [Migration Guide](link)
2. Update your integration to use the new v2 API
3. Test in staging
4. Deploy to production before July 15

**Why we're making this change:**
The new API provides better security, performance, and features.

**Need help?**
Our team is here to assist. Reply to this email or contact support@company.com.

Best regards,
Engineering Team
```

---

## 7. Deprecation Checklist

```markdown
## Deprecation Checklist for [Feature Name]

### Planning
- [ ] Identify replacement solution
- [ ] Set deprecation timeline (min 6 months)
- [ ] Create migration guide
- [ ] Identify affected users

### Announcement (Month 0)
- [ ] Publish deprecation notice
- [ ] Add deprecation warnings to code
- [ ] Update documentation
- [ ] Email affected users

### Monitoring (Month 0-6)
- [ ] Track usage of deprecated feature
- [ ] Identify top users
- [ ] Offer migration assistance
- [ ] Send reminder emails (Month 2, 4)

### Sunset (Month 6)
- [ ] Remove deprecated feature
- [ ] Monitor for issues
- [ ] Update documentation
- [ ] Announce completion
```

---

## 8. Deprecation Policy Document

```markdown
# Company Deprecation Policy

## Minimum Notice Period
- **Public APIs**: 12 months
- **Internal APIs**: 6 months
- **Experimental Features**: 3 months
- **Security Issues**: Immediate (with migration path)

## Communication Channels
1. Changelog
2. Email to affected users
3. In-app notifications
4. API response headers
5. Developer blog

## Migration Support
- Detailed migration guides
- Code examples
- Dedicated support channel
- Optional migration assistance

## Exceptions
Critical security vulnerabilities may require immediate deprecation with shorter notice.
```

---

## 9. Deprecation Metrics

```typescript
interface DeprecationMetrics {
  totalUsers: number;
  migratedUsers: number;
  remainingUsers: number;
  migrationRate: number;  // percentage
  daysUntilSunset: number;
}

function calculateMigrationProgress(): DeprecationMetrics {
  const total = getTotalUsersOfDeprecatedFeature();
  const migrated = getUsersOnNewVersion();
  
  return {
    totalUsers: total,
    migratedUsers: migrated,
    remainingUsers: total - migrated,
    migrationRate: (migrated / total) * 100,
    daysUntilSunset: getDaysUntilSunset()
  };
}
```

---

## 10. Deprecation Policy Checklist

- [ ] **Policy Documented**: Written deprecation policy exists?
- [ ] **Timeline Defined**: Minimum notice periods set?
- [ ] **Migration Guides**: Templates for migration docs?
- [ ] **Tracking**: Usage of deprecated features monitored?
- [ ] **Communication**: Multi-channel notification plan?
- [ ] **Support**: Migration assistance available?
- [ ] **Metrics**: Track migration progress?
- [ ] **Enforcement**: Automated checks prevent new usage?

---

## Related Skills
* `59-architecture-decision/versioning-strategy`
* `51-contracts-governance/api-contracts`
* `45-product-thinking/sunset-decision`
