---
name: Versioning Strategy
description: API and system versioning strategies to enable evolution while maintaining backward compatibility.
---

# Versioning Strategy

## Overview

Versioning Strategy defines how systems evolve over time while maintaining compatibility with existing clients. Good versioning enables innovation without breaking existing integrations.

**Core Principle**: "Never break existing clients. Version explicitly, deprecate gracefully."

---

## 1. API Versioning Strategies

### URL Path Versioning
```
GET /api/v1/users
GET /api/v2/users
GET /api/v3/users

Pros: Clear, easy to route
Cons: URL pollution, harder to deprecate
```

### Header Versioning
```
GET /api/users
Header: API-Version: 2024-01-15

Pros: Clean URLs
Cons: Less visible, harder to test in browser
```

### Query Parameter Versioning
```
GET /api/users?version=2

Pros: Easy to test
Cons: Can be forgotten, mixes with other params
```

### Content Negotiation
```
GET /api/users
Accept: application/vnd.myapi.v2+json

Pros: RESTful, flexible
Cons: Complex, less discoverable
```

---

## 2. Semantic Versioning (SemVer)

```
MAJOR.MINOR.PATCH

1.0.0 → 1.0.1  (Patch: Bug fix, backward compatible)
1.0.1 → 1.1.0  (Minor: New feature, backward compatible)
1.1.0 → 2.0.0  (Major: Breaking change)
```

### Examples
```
1.0.0: Initial release
1.0.1: Fix authentication bug
1.1.0: Add pagination to /users endpoint
1.2.0: Add /products endpoint
2.0.0: Remove deprecated /legacy endpoint
```

---

## 3. Breaking vs Non-Breaking Changes

### Non-Breaking (Safe)
```typescript
// ✅ Adding optional field
interface User {
  id: string;
  name: string;
  email?: string;  // New optional field
}

// ✅ Adding new endpoint
GET /api/v1/users/:id/preferences  // New endpoint

// ✅ Adding new query parameter (optional)
GET /api/v1/users?sort=name  // New optional param
```

### Breaking (Dangerous)
```typescript
// ❌ Removing field
interface User {
  id: string;
  // name: string;  // REMOVED - breaks clients expecting this
}

// ❌ Changing field type
interface User {
  id: number;  // Was string, now number - BREAKING
}

// ❌ Renaming endpoint
GET /api/v1/accounts  // Was /users - BREAKING

// ❌ Making optional field required
interface User {
  email: string;  // Was optional, now required - BREAKING
}
```

---

## 4. Versioning in Code

### Version Routing (Express)
```typescript
import express from 'express';

const app = express();

// V1 routes
app.get('/api/v1/users', v1.getUsers);
app.get('/api/v1/users/:id', v1.getUser);

// V2 routes (with new features)
app.get('/api/v2/users', v2.getUsers);  // Includes pagination
app.get('/api/v2/users/:id', v2.getUser);  // Includes preferences
```

### Shared Logic
```typescript
// Shared business logic
class UserService {
  async getUser(id: string): Promise<User> {
    return await db.users.findById(id);
  }
}

// V1 controller
class V1UserController {
  async getUser(req, res) {
    const user = await userService.getUser(req.params.id);
    res.json({ id: user.id, name: user.name });  // V1 response format
  }
}

// V2 controller
class V2UserController {
  async getUser(req, res) {
    const user = await userService.getUser(req.params.id);
    res.json({
      id: user.id,
      name: user.name,
      email: user.email,  // V2 includes email
      preferences: user.preferences  // V2 includes preferences
    });
  }
}
```

---

## 5. Database Schema Versioning

### Expand-Contract Pattern
```sql
-- Phase 1: Expand (add new column)
ALTER TABLE users ADD COLUMN email_address VARCHAR(255);

-- Dual writes (write to both old and new)
UPDATE users SET email = ?, email_address = ? WHERE id = ?;

-- Phase 2: Migrate data
UPDATE users SET email_address = email WHERE email_address IS NULL;

-- Phase 3: Contract (remove old column)
ALTER TABLE users DROP COLUMN email;
```

### Migration Scripts
```typescript
// migrations/001_add_email.ts
export async function up(db: Database) {
  await db.schema.alterTable('users', (table) => {
    table.string('email_address');
  });
}

export async function down(db: Database) {
  await db.schema.alterTable('users', (table) => {
    table.dropColumn('email_address');
  });
}
```

---

## 6. Deprecation Strategy

### Deprecation Timeline
```markdown
## Deprecation Timeline for /api/v1/users

- **2024-01-15**: Announce deprecation (6 months notice)
- **2024-04-15**: Add deprecation headers
- **2024-07-15**: Remove from documentation
- **2024-07-15**: Sunset endpoint (stop accepting new clients)
```

### Deprecation Headers
```typescript
app.get('/api/v1/users', (req, res) => {
  res.set('Deprecation', 'true');
  res.set('Sunset', 'Sat, 15 Jul 2024 00:00:00 GMT');
  res.set('Link', '</api/v2/users>; rel="successor-version"');
  
  // Return data
  res.json(users);
});
```

---

## 7. Client SDK Versioning

```typescript
// SDK v1
import { UserClient } from '@myapi/sdk';

const client = new UserClient({ version: 'v1' });
const user = await client.getUser('123');

// SDK v2
import { UserClient } from '@myapi/sdk';

const client = new UserClient({ version: 'v2' });
const user = await client.getUser('123');  // Returns more fields
```

---

## 8. Versioning Checklist

- [ ] **Strategy Chosen**: URL path, header, or content negotiation?
- [ ] **SemVer Adopted**: Using semantic versioning?
- [ ] **Breaking Changes Identified**: Clear what breaks compatibility?
- [ ] **Deprecation Policy**: Timeline for sunsetting old versions?
- [ ] **Documentation**: All versions documented?
- [ ] **Monitoring**: Track usage of each version?
- [ ] **Migration Guide**: Help clients upgrade?
- [ ] **Backward Compatibility**: Maintain for at least 6 months?

---

## Related Skills
* `59-architecture-decision/deprecation-policy`
* `51-contracts-governance/api-contracts`
* `45-developer-experience/release-workflow`
