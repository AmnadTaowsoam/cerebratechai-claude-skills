---
name: Contract Test Gates
description: Gates สำหรับ enforce API contract testing ระหว่าง services ด้วย Pact หรือ OpenAPI validation
---

# Contract Test Gates

## Overview

Gates สำหรับ enforce API contract testing - ทำให้แน่ใจว่า producer และ consumer ใช้ contract เดียวกัน

## Why This Matters

- **Integration safety**: ไม่ break consumers
- **Early detection**: รู้ก่อน deploy
- **Documentation**: Contract = living docs
- **Confidence**: Deploy independently

---

## Contract Testing

### Producer Side
```typescript
// API must match contract
describe('User API Contract', () => {
  it('GET /users/:id matches contract', async () => {
    const response = await request(app).get('/users/123');
    
    // Validate against OpenAPI spec
    expect(response).toMatchOpenAPISchema('User');
    expect(response.body).toHaveProperty('id');
    expect(response.body).toHaveProperty('email');
  });
});
```

### Consumer Side
```typescript
// Consumer expectations
const userPact = new Pact({
  consumer: 'frontend',
  provider: 'user-api'
});

it('can get user by ID', async () => {
  await userPact
    .given('user 123 exists')
    .uponReceiving('a request for user 123')
    .withRequest({
      method: 'GET',
      path: '/users/123'
    })
    .willRespondWith({
      status: 200,
      body: {
        id: '123',
        email: 'test@example.com'
      }
    });
  
  // Test consumer code
  const user = await userService.getUser('123');
  expect(user.id).toBe('123');
});
```

---

## CI Pipeline

```yaml
# .github/workflows/contract-tests.yml
name: Contract Tests
on: [pull_request]

jobs:
  contract:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Contract Tests
        run: npm run test:contract
      
      - name: Publish Pacts
        run: npm run pact:publish
      
      - name: Verify Contracts
        run: npm run pact:verify
```

---

## Summary

**Contract Test Gates:** Enforce API contracts

**Types:**
- Producer tests (API matches spec)
- Consumer tests (expectations met)
- Contract verification (both sides agree)

**Tools:**
- Pact (consumer-driven)
- OpenAPI validation
- Postman/Bruno collections

**Policy:** Must pass before merge
