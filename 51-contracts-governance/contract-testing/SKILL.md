---
name: Contract Testing
description: Comprehensive guide to consumer-driven contract testing with Pact, bi-directional contracts, and integration with CI/CD pipelines
---

# Contract Testing

## What is Contract Testing?

**Definition:** Testing agreements between services where consumers define expectations and providers verify they meet them.

### Model
```
Consumer (Mobile App) defines contract:
"When I call GET /users/123, I expect { id, name, email }"

Provider (API) verifies:
"I can provide { id, name, email } for GET /users/123"

Contract = Agreement between consumer and provider
```

### Example
```
Consumer Test (Pact):
expect(GET /users/123).toReturn({
  id: '123',
  name: 'John Doe',
  email: 'john@example.com'
})

Provider Verification:
GET /users/123 → { id: '123', name: 'John Doe', email: 'john@example.com' }
✅ Contract satisfied
```

---

## Why Contract Testing Matters

### 1. Avoid Breaking Consumers

**Without Contract Testing:**
```
Provider changes response:
- name: string (removed)
+ firstName: string

Deploy → All consumers break
```

**With Contract Testing:**
```
Provider tries to change response
→ Contract verification fails (consumer expects 'name')
→ Deploy blocked
→ Consumer not broken
```

### 2. Test Independently (No Integrated Env)

**Integration Testing:**
```
Need:
- Running provider service
- Running consumer service
- Database
- Message queue
- Slow, fragile
```

**Contract Testing:**
```
Need:
- Contract file (JSON)
- Fast, isolated
```

### 3. Faster Feedback (No Coordinated Testing)

**Integration Testing:**
```
1. Deploy provider to staging
2. Deploy consumer to staging
3. Run integration tests
4. Find issues
5. Fix and repeat
Timeline: Days
```

**Contract Testing:**
```
1. Consumer writes contract
2. Provider verifies contract
3. Both pass → Safe to deploy
Timeline: Minutes
```

### 4. Documentation (Contracts = Specs)

**Contracts Document:**
- What endpoints exist
- What requests/responses look like
- Who uses what

---

## Contract Testing vs Integration Testing

### Integration Testing

**What:** Test actual integration between services

**Process:**
```
1. Deploy both services to test environment
2. Consumer calls provider
3. Verify response
```

**Pros:**
- Tests real integration
- Catches environment issues

**Cons:**
- Slow (need running services)
- Fragile (network, database, etc.)
- Requires coordination

### Contract Testing

**What:** Test against contract (not actual service)

**Process:**
```
1. Consumer writes contract (expected behavior)
2. Provider verifies it can satisfy contract
3. No actual integration needed
```

**Pros:**
- Fast (no running services)
- Isolated (no dependencies)
- Independent (no coordination)

**Cons:**
- Doesn't test actual integration
- Doesn't catch environment issues

### Use Both

**Strategy:**
```
Contract tests: Most scenarios (fast, isolated)
Integration tests: Critical paths (slow, comprehensive)

Example:
- Contract tests: 100 scenarios
- Integration tests: 5 critical scenarios
```

---

## Consumer-Driven Contract (CDC)

### Consumer Defines What It Needs

**Consumer (Mobile App):**
```javascript
// I need GET /users/123 to return { id, name, email }
const contract = {
  request: {
    method: 'GET',
    path: '/users/123'
  },
  response: {
    status: 200,
    body: {
      id: '123',
      name: 'John Doe',
      email: 'john@example.com'
    }
  }
};
```

### Provider Verifies It Can Provide

**Provider (API):**
```javascript
// Verify I can provide what consumer expects
GET /users/123 → { id: '123', name: 'John Doe', email: 'john@example.com' }
✅ Matches contract
```

### vs Provider-Driven

**Provider-Driven:**
```
Provider defines API
→ Consumers must adapt
→ "Take it or leave it"
```

**Consumer-Driven:**
```
Consumers define needs
→ Provider must satisfy
→ "We'll provide what you need"
```

**Recommendation:** Consumer-driven (more flexible)

---

## Pact Framework

### Popular CDC Tool

**Features:**
- HTTP, messages, GraphQL support
- Consumer writes Pact tests
- Provider verifies against Pact
- Pact Broker (central registry)

**Languages:**
- JavaScript, Python, Java, Ruby, Go, .NET, PHP, Swift

### Consumer Writes Pact Tests

**Example (JavaScript):**
```javascript
const { Pact } = require('@pact-foundation/pact');
const { getUserById } = require('./api');

describe('User API', () => {
  const provider = new Pact({
    consumer: 'mobile-app',
    provider: 'user-api'
  });

  beforeAll(() => provider.setup());
  afterAll(() => provider.finalize());

  test('get user by ID', async () => {
    // Define expected interaction
    await provider.addInteraction({
      state: 'user 123 exists',
      uponReceiving: 'a request for user 123',
      withRequest: {
        method: 'GET',
        path: '/users/123',
        headers: {
          'Accept': 'application/json'
        }
      },
      willRespondWith: {
        status: 200,
        headers: {
          'Content-Type': 'application/json'
        },
        body: {
          id: '123',
          name: 'John Doe',
          email: 'john@example.com'
        }
      }
    });

    // Call API (against mock provider)
    const user = await getUserById('123');

    // Verify response
    expect(user.id).toBe('123');
    expect(user.name).toBe('John Doe');
    expect(user.email).toBe('john@example.com');

    // Verify interaction occurred
    await provider.verify();
  });
});
```

**Output:**
```
Pact file generated: pacts/mobile-app-user-api.json
```

### Provider Verifies Against Pact

**Example (JavaScript):**
```javascript
const { Verifier } = require('@pact-foundation/pact');
const app = require('./app');

describe('Pact Verification', () => {
  test('verify user-api satisfies mobile-app contract', async () => {
    const options = {
      provider: 'user-api',
      providerBaseUrl: 'http://localhost:3000',
      pactBrokerUrl: 'https://pact-broker.example.com',
      publishVerificationResult: true,
      providerVersion: process.env.GIT_COMMIT,
      stateHandlers: {
        'user 123 exists': async () => {
          // Setup: Create user 123 in database
          await db.users.create({
            id: '123',
            name: 'John Doe',
            email: 'john@example.com'
          });
        }
      }
    };

    await new Verifier(options).verifyProvider();
  });
});
```

**Output:**
```
Verifying pact between mobile-app and user-api
  GET /users/123
    ✓ returns user (200)

1 interaction verified
```

---

## Contract Testing Workflow

### Step 1: Consumer Writes Contract Test (Pact)

See "Consumer Writes Pact Tests" above

### Step 2: Consumer Test Runs, Generates Contract JSON

**Generated Pact File:**
```json
{
  "consumer": {
    "name": "mobile-app"
  },
  "provider": {
    "name": "user-api"
  },
  "interactions": [
    {
      "description": "a request for user 123",
      "providerState": "user 123 exists",
      "request": {
        "method": "GET",
        "path": "/users/123",
        "headers": {
          "Accept": "application/json"
        }
      },
      "response": {
        "status": 200,
        "headers": {
          "Content-Type": "application/json"
        },
        "body": {
          "id": "123",
          "name": "John Doe",
          "email": "john@example.com"
        }
      }
    }
  ],
  "metadata": {
    "pactSpecification": {
      "version": "2.0.0"
    }
  }
}
```

### Step 3: Contract Published to Pact Broker

**Publish:**
```bash
npx pact-broker publish \
  pacts/mobile-app-user-api.json \
  --consumer-app-version $GIT_COMMIT \
  --broker-base-url https://pact-broker.example.com \
  --broker-token $PACT_BROKER_TOKEN
```

### Step 4: Provider Pulls Contract

**Automatic:** Provider verification pulls from broker

### Step 5: Provider Verification Runs

See "Provider Verifies Against Pact" above

### Step 6: Both Sides Pass → Safe to Deploy

**Can-I-Deploy Check:**
```bash
npx pact-broker can-i-deploy \
  --pacticipant mobile-app \
  --version $GIT_COMMIT \
  --to production
```

**Output:**
```
Can mobile-app version abc123 be deployed to production?
✓ user-api (version def456) has verified pact
Result: Yes
```

---

## Pact Broker

### Central Registry of Contracts

**Features:**
- Store contracts
- Version management
- Verification results
- Can-I-Deploy checks
- Webhooks

**Setup (Docker):**
```bash
docker run -d \
  --name pact-broker \
  -p 9292:9292 \
  -e PACT_BROKER_DATABASE_URL=postgres://... \
  pactfoundation/pact-broker
```

**Hosted Options:**
- Pactflow (official, $$$)
- Self-hosted (free, open source)

### Version Management

**Contracts Versioned by:**
- Consumer version (git commit)
- Provider version (git commit)

**Example:**
```
mobile-app (v1.0.0) → user-api (v2.3.0)
Contract: mobile-app-user-api.json
```

### Can-I-Deploy Check

**Question:** Is it safe to deploy this version?

**Check:**
```bash
# Can I deploy mobile-app version abc123?
npx pact-broker can-i-deploy \
  --pacticipant mobile-app \
  --version abc123 \
  --to production

# Check if provider has verified contract
# If yes → Safe to deploy
# If no → Not safe
```

**CI/CD Gate:**
```yaml
- name: Can I deploy?
  run: |
    npx pact-broker can-i-deploy \
      --pacticipant mobile-app \
      --version $GIT_COMMIT \
      --to production
    
    if [ $? -ne 0 ]; then
      echo "Cannot deploy: Provider has not verified contract"
      exit 1
    fi
```

### Webhooks (Trigger Provider Verification)

**Setup:**
```
When: Contract published
Then: Trigger provider verification (webhook to CI)
```

**Example:**
```
Consumer publishes contract
→ Webhook triggers provider CI
→ Provider verification runs
→ Results published to broker
```

---

## Bi-Directional Contracts

### Provider Defines OpenAPI Spec

**Provider:**
```yaml
openapi: 3.0.0
paths:
  /users/{id}:
    get:
      responses:
        '200':
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: string
                  name:
                    type: string
                  email:
                    type: string
```

### Consumer Defines Pact

**Consumer:**
```javascript
// Pact test (see above)
```

### Both Verified Against Each Other

**Process:**
```
1. Provider publishes OpenAPI spec to broker
2. Consumer publishes Pact to broker
3. Broker verifies Pact is compatible with OpenAPI spec
4. If compatible → Both can deploy
```

**Benefits:**
- Provider defines capabilities (OpenAPI)
- Consumer defines needs (Pact)
- Broker ensures compatibility

**Tools:**
- Pactflow (supports bi-directional contracts)

---

## Testing Event-Driven Contracts

### Message Pact (for Async Messages)

**Consumer Expects Message Format:**
```javascript
const { MessageConsumerPact } = require('@pact-foundation/pact');

describe('User Created Event', () => {
  const messagePact = new MessageConsumerPact({
    consumer: 'email-service',
    provider: 'user-service'
  });

  test('receive user created event', async () => {
    await messagePact
      .given('user 123 is created')
      .expectsToReceive('user created event')
      .withContent({
        id: '123',
        email: 'john@example.com',
        name: 'John Doe'
      })
      .verify(async (message) => {
        // Handle message
        await handleUserCreated(message);
        
        // Verify email sent
        expect(emailSent).toBe(true);
      });
  });
});
```

### Provider Verifies It Produces Correct Format

**Provider:**
```javascript
const { MessageProviderPact } = require('@pact-foundation/pact');

describe('Message Provider Verification', () => {
  test('verify user-service produces user created events', async () => {
    await new MessageProviderPact({
      messageProviders: {
        'user created event': () => {
          // Return message that would be published
          return {
            id: '123',
            email: 'john@example.com',
            name: 'John Doe'
          };
        }
      },
      provider: 'user-service',
      pactUrls: ['pacts/email-service-user-service.json']
    }).verify();
  });
});
```

---

## Contract Testing Best Practices

### Test Behavior, Not Implementation

**Good:**
```javascript
// Test that API returns user with expected fields
expect(user).toHaveProperty('id');
expect(user).toHaveProperty('name');
expect(user).toHaveProperty('email');
```

**Bad:**
```javascript
// Don't test implementation details
expect(database.query).toHaveBeenCalledWith('SELECT * FROM users WHERE id = 123');
```

### One Contract Per Consumer-Provider Pair

**Structure:**
```
mobile-app → user-api (one contract)
web-app → user-api (separate contract)
email-service → user-service (separate contract)
```

### Version Contracts

**Use Git Commit:**
```
Consumer version: abc123 (git commit)
Provider version: def456 (git commit)
```

### Run Verification on Every Provider Change

**CI/CD:**
```yaml
# Provider CI
on: [push]

jobs:
  verify-contracts:
    runs-on: ubuntu-latest
    steps:
      - name: Verify contracts
        run: npm run test:pact:verify
```

### Use Can-I-Deploy in CI/CD

See "Can-I-Deploy Check" above

---

## Common Pitfalls

### Testing Too Much (Test Contracts, Not Business Logic)

**Good:**
```javascript
// Test contract (structure)
expect(user).toHaveProperty('id');
expect(user).toHaveProperty('name');
```

**Bad:**
```javascript
// Don't test business logic in contract tests
expect(user.name).toBe('John Doe');  // Too specific
expect(user.email).toMatch(/@example.com$/);  // Business rule
```

### Not Versioning Contracts

**Bad:**
```
Contract published without version
→ Can't track which version is compatible
```

**Good:**
```
Contract published with git commit
→ Can track compatibility by version
```

### Provider Verification Not in CI

**Bad:**
```
Provider verification run manually
→ Easy to forget
→ Contracts not verified
```

**Good:**
```
Provider verification in CI
→ Runs on every commit
→ Contracts always verified
```

### Ignoring Failed Verifications

**Bad:**
```
Verification fails
→ Ignored
→ Deploy anyway
→ Consumer breaks
```

**Good:**
```
Verification fails
→ Deploy blocked
→ Fix issue
→ Re-verify
→ Deploy
```

---

## Tools

### Pact (Most Popular)

**Languages:**
- JavaScript: @pact-foundation/pact
- Python: pact-python
- Java: pact-jvm
- Ruby: pact-ruby
- Go: pact-go
- .NET: pact-net

**Broker:**
- Self-hosted (free)
- Pactflow (hosted, $$$)

### Spring Cloud Contract (Java)

**Features:**
- Contract testing for Spring Boot
- Groovy DSL for contracts
- Stub generation

**Example:**
```groovy
Contract.make {
  request {
    method 'GET'
    url '/users/123'
  }
  response {
    status 200
    body([
      id: '123',
      name: 'John Doe'
    ])
  }
}
```

### Specmatic (OpenAPI Contracts)

**Features:**
- Uses OpenAPI spec as contract
- Auto-generates tests
- Stub server

**Example:**
```bash
# Use OpenAPI spec as contract
specmatic test openapi.yaml
```

---

## CI/CD Integration

### Consumer Tests Generate Contract

**GitHub Actions (Consumer):**
```yaml
name: Consumer Tests

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Run Pact tests
        run: npm run test:pact
      
      - name: Publish contract
        run: |
          npx pact-broker publish \
            pacts/ \
            --consumer-app-version $GITHUB_SHA \
            --broker-base-url $PACT_BROKER_URL \
            --broker-token $PACT_BROKER_TOKEN
```

### Publish to Broker (If Tests Pass)

See above

### Provider Verification Triggered (Webhook)

**Pact Broker Webhook:**
```
When: Contract published
Trigger: POST https://ci.example.com/trigger-build
Body: { "provider": "user-api", "consumer": "mobile-app" }
```

### Can-I-Deploy Gate Before Deployment

**GitHub Actions (Consumer):**
```yaml
deploy:
  runs-on: ubuntu-latest
  needs: test
  steps:
    - name: Can I deploy?
      run: |
        npx pact-broker can-i-deploy \
          --pacticipant mobile-app \
          --version $GITHUB_SHA \
          --to production
    
    - name: Deploy
      if: success()
      run: ./deploy.sh
```

---

## Real-World Contract Testing

### Microservices (Service-to-Service)

**Example:**
```
order-service → payment-service
order-service → inventory-service
order-service → notification-service

Each pair has a contract
```

### API Consumers (Mobile, Web)

**Example:**
```
mobile-app → user-api
web-app → user-api
partner-api → user-api

Each consumer has its own contract
```

### Event-Driven (Message Contracts)

**Example:**
```
user-service publishes: user.created
email-service consumes: user.created

Message contract between them
```

---

## Implementation Examples

### Pact Consumer Test (Python)

```python
from pact import Consumer, Provider

pact = Consumer('mobile-app').has_pact_with(Provider('user-api'))

pact.given('user 123 exists') \
    .upon_receiving('a request for user 123') \
    .with_request('GET', '/users/123') \
    .will_respond_with(200, body={
        'id': '123',
        'name': 'John Doe',
        'email': 'john@example.com'
    })

with pact:
    user = get_user_by_id('123')
    assert user['id'] == '123'
    assert user['name'] == 'John Doe'
```

### Pact Provider Verification

See "Provider Verifies Against Pact" above

### Pact Broker Setup

See "Pact Broker" section above

---

## Summary

### Quick Reference

**Contract Testing:** Testing agreements between services

**Why:**
- Avoid breaking consumers
- Test independently
- Faster feedback
- Documentation

**Consumer-Driven:**
- Consumer defines needs
- Provider verifies it can provide

**Pact:**
- Popular CDC tool
- Consumer writes Pact tests
- Provider verifies against Pact
- Pact Broker (central registry)

**Workflow:**
1. Consumer writes contract test
2. Test generates contract JSON
3. Publish to broker
4. Provider pulls contract
5. Provider verification runs
6. Both pass → Safe to deploy

**Pact Broker:**
- Central registry
- Version management
- Can-I-Deploy checks
- Webhooks

**Bi-Directional:**
- Provider: OpenAPI spec
- Consumer: Pact
- Both verified

**Message Pact:**
- For async messages
- Consumer expects format
- Provider verifies

**Best Practices:**
- Test behavior, not implementation
- One contract per pair
- Version contracts
- Run verification on every change
- Use Can-I-Deploy

**Tools:**
- Pact (most popular)
- Spring Cloud Contract (Java)
- Specmatic (OpenAPI)

**CI/CD:**
- Consumer tests generate contract
- Publish to broker
- Provider verification triggered
- Can-I-Deploy gate
## Overview

Contract Testing is the practice of testing agreements between services where consumers define expectations and providers verify they meet them.

### Model

Consumer (Mobile App) defines contract:
"When I call GET /users/123, I expect { id, name, email }"

Provider (API) verifies:
"I can provide { id, name, email } for GET /users/123"

Contract = Agreement between consumer and provider

### Example

Consumer Test (Pact):
expect(GET /users/123).toReturn({
  id: '123',
  name: 'John Doe',
  email: 'john@example.com'
})

Provider Verification:
GET /users/123 → { id: '123', name: 'John Doe', email: 'john@example.com' }
✅ Contract satisfied

---

## Why Contract Testing Matters

### 1. Avoid Breaking Consumers

**Without Contract Testing:**
```
Provider changes response:
- name: string (removed)
+ firstName: string

Deploy → All consumers break
```

**With Contract Testing:**
```
Provider tries to change response:
→ Contract verification fails (consumer expects 'name')
→ Deploy blocked
→ Consumer not broken
```

### 2. Test Independently (No Integrated Env)

**Integration Testing:**
Need:
- Running provider service
- Running consumer service
- Database
- Message queue
- Slow, fragile

**Contract Testing:**
Need:
- Contract file (JSON)
- Fast, isolated
```

### 3. Faster Feedback (No Coordinated Testing)

**Integration Testing:**
1. Deploy provider to staging
2. Deploy consumer to staging
3. Run integration tests
4. Find issues
5. Fix and repeat
Timeline: Days

**Contract Testing:**
1. Consumer writes contract
2. Provider verifies contract
3. Both pass → Safe to deploy
Timeline: Minutes

---

## Contract Testing vs Integration Testing

### Integration Testing
**What:** Test actual integration between services

**Process:**
1. Deploy both services to test environment
2. Consumer calls provider
3. Verify response
4. Find issues
5. Fix and repeat

**Pros:**
- Tests real integration
- Catches environment issues

**Cons:**
- Slow (need running services)
- Fragile (network, database, etc.)
- Requires coordination

### Contract Testing
**What:** Test against contract (not actual service)

**Process:**
1. Consumer writes contract (expected behavior)
2. Provider verifies it can satisfy contract
3. No actual integration needed

**Pros:**
- Fast (no running services)
- Isolated (no dependencies)
- Independent (no coordination)

**Cons:**
- Doesn't test actual integration
- Doesn't catch environment issues

### Use Both
**Strategy:**
Contract tests: Most scenarios (fast, isolated)
Integration tests: Critical paths (slow, comprehensive)

Example:
- Contract tests: 100 scenarios
- Integration tests: 5 critical scenarios

---

## Consumer-Driven Contract (CDC)

### Consumer Defines What It Needs

**Consumer (Mobile App):**
```javascript
// I need GET /users/123 to return { id, name, email }
const contract = {
  request: {
    method: 'GET',
    path: '/users/123'
  },
  response: {
    status: 200,
    body: {
      id: '123',
      name: 'John Doe',
      email: 'john@example.com'
    }
  }
};
```

### Provider Verifies It Can Provide

**Provider (API):**
```javascript
// Verify I can provide what consumer expects
GET /users/123 → { id: '123', name: 'John Doe', email: 'john@example.com' }
✅ Matches contract
```

### vs Provider-Driven

**Provider-Driven:**
Provider defines API → Consumers must adapt
"Take it or leave it"

**Consumer-Driven:**
Consumers define needs → Provider must satisfy
"We'll provide what you need"

**Recommendation:** Consumer-driven (more flexible)

---

## Pact Framework

### Popular CDC Tool

**Features:**
- HTTP, messages, GraphQL support
- Consumer writes Pact tests
- Provider verifies against Pact
- Pact Broker (central registry)

**Languages:**
- JavaScript, Python, Java, Ruby, Go, .NET, PHP, Swift

---

## Consumer Writes Pact Tests

**Example (JavaScript):**
```javascript
const { Pact } = require('@pact-foundation/pact');
const { getUserById } = require('./api');

describe('User API', () => {
  const provider = new Pact({
    consumer: 'mobile-app',
    provider: 'user-api'
  });

beforeAll(() => provider.setup());

test('get user by ID', async () => {
  // Define expected interaction
  await provider.addInteraction({
    state: 'user 123 exists',
    uponReceiving: 'a request for user 123',
    withRequest: {
      method: 'GET',
      path: '/users/123',
      headers: {
        'Accept': 'application/json'
      }
    },
    willRespondWith: {
      status: 200,
      headers: {
        'Content-Type': 'application/json'
      },
      body: {
        id: '123',
        name: 'John Doe',
        email: 'john@example.com'
      }
    }
  });

  // Call API (against mock provider)
  const user = await getUserById('123');

  // Verify response
  expect(user.id).toBe('123');
  expect(user.name).toBe('John Doe');
  expect(user.email).toBe('john@example.com');

  // Verify interaction occurred
  await provider.verify();
});
```

---

## Provider Verifies Against Pact

**Example (JavaScript):**
```javascript
const { Verifier } = require('@pact-foundation/pact');
const app = require('./app');

describe('Pact Verification', () => {
  test('verify user-api satisfies mobile-app contract', async () => {
    const options = {
      provider: 'user-api',
      providerBaseUrl: 'http://localhost:3000',
      pactBrokerUrl: 'https://pact-broker.example.com',
      publishVerificationResult: true,
      providerVersion: process.env.GIT_COMMIT,
      stateHandlers: {
        'user 123 exists': async () => {
          // Setup: Create user 123 in database
          await db.users.create({
            id: '123',
            name: 'John Doe',
            email: 'john@example.com'
          });
        }
      }
    };

    await new Verifier(options).verifyProvider();
  });
});
```

---

## Contract Testing Best Practices

### Test Behavior, Not Implementation

**Good:**
```javascript
// Test that API returns user with expected fields
expect(user).toHaveProperty('id');
expect(user).toHaveProperty('name');
expect(user).toHaveProperty('email');
```

**Bad:**
```javascript
// Don't test implementation details
expect(database.query).toHaveBeenCalledWith('SELECT * FROM users WHERE id = 123');
```

### One Contract Per Consumer-Provider Pair

**Structure:**
```
mobile-app → user-api (one contract)
web-app → user-api (separate contract)
email-service → user-service (separate contract)
```

### Version Contracts

**Use Git Commit:**
Consumer version: abc123 (git commit)
Provider version: def456 (git commit)

---

## Contract Testing Workflow

### Step 1: Consumer Writes Contract Test (Pact)

See "Consumer Writes Pact Tests" above

### Step 2: Consumer Test Runs, Generates Contract JSON

**Generated Pact File:**
```json
{
  "consumer": {
    "name": "mobile-app"
  },
  "provider": {
    "name": "user-api"
  },
  "interactions": [
    {
      "description": "a request for user 123",
      "providerState": "user 123 exists",
      "request": {
        "method": "GET",
        "path": "/users/123",
        "headers": {
          "Accept": "application/json"
        }
      },
      "response": {
        "status": 200,
        "headers": {
          "Content-Type": "application/json"
        },
        "body": {
          "id": "123",
          "name": "John Doe",
          "email": "john@example.com"
        }
      }
    }
  ],
  "metadata": {
    "pactSpecification": {
      "version": "2.0.0"
    }
  }
}
```

### Step 3: Contract Published to Pact Broker

**Publish:**
```bash
npx pact-broker publish \
  pacts/mobile-app-user-api.json \
  --consumer-app-version $GIT_COMMIT \
  --broker-base-url https://pact-broker.example.com \
  --broker-token $PACT_BROKER_TOKEN
```

### Step 4: Provider Pulls Contract

**Automatic:** Provider verification pulls from broker

### Step 5: Provider Verification Runs

See "Provider Verifies Against Pact" above

### Step 6: Both Sides Pass → Safe to Deploy

**Can-I-Deploy Check:**
```bash
npx pact-broker can-i-deploy \
  --pacticipant mobile-app \
  --version $GIT_COMMIT \
  --to production
```

---

## Pact Broker

### Central Registry of Contracts

**Features:**
- Store contracts
- Version management
- Verification results
- Can-I-Deploy checks
- Webhooks

---

## Bi-Directional Contracts

### Provider Defines OpenAPI Spec

**Provider:**
```yaml
openapi: 3.0.0
paths:
  /users/{id}:
    get:
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
```

### Consumer Defines Pact

**Consumer:**
```javascript
// Pact test (see above)
```

### Both Verified Against Each Other

**Process:**
1. Provider publishes OpenAPI spec to broker
2. Consumer publishes Pact to broker
3. Broker verifies Pact is compatible with OpenAPI spec
4. If compatible → Both can deploy

---

## Testing Event-Driven Contracts

### Message Pact (for Async Messages)

**Consumer Expects Message Format:**
```javascript
const { MessageConsumerPact } = require('@pact-foundation/pact');

describe('User Created Event', () => {
  const messagePact = new MessageConsumerPact({
    consumer: 'email-service',
    provider: 'user-service'
  });

  test('receive user created event', async () => {
    await messagePact
      .given('user 123 is created')
      .expectsToReceive('user created event')
      .withContent({
        id: '123',
        email: 'john@example.com',
        name: 'John Doe'
      })
      .verify(async (message) => {
        // Handle message
        await handleUserCreated(message);
        
        // Verify email sent
        expect(emailSent).toBe(true);
      });
  });
});
```

---

## Contract Testing Best Practices

### Test Behavior, Not Implementation

**Good:**
```javascript
// Test that API returns user with expected fields
expect(user).toHaveProperty('id');
expect(user).toHaveProperty('name');
expect(user).toHaveProperty('email');
```

**Bad:**
```javascript
// Don't test implementation details
expect(database.query).toHaveBeenCalledWith('SELECT * FROM users WHERE id = 123');
```

### One Contract Per Consumer-Provider Pair

**Structure:**
```
mobile-app → user-api (one contract)
web-app → user-api (separate contract)
email-service → user-service (separate contract)
```

### Version Contracts

**Use Git Commit:**
Consumer version: abc123 (git commit)
Provider version: def456 (git commit)

---

## Tools

### Pact (Most Popular)

**Languages:**
- JavaScript: @pact-foundation/pact
- Python: pact-python
- Java: pact-jvm
- Ruby: pact-ruby
- Go: pact-go
- .NET: pact-net
- PHP: pact-php
- Swift: pact-swift

**Broker:**
- Self-hosted (free)
- Pactflow (hosted, $$$)

### Spring Cloud Contract (Java)

**Features:**
- Contract testing for Spring Boot
- Groovy DSL for contracts
- Stub generation

---

## CI/CD Integration

### Consumer Tests Generate Contract

**GitHub Actions (Consumer):**
```yaml
name: Consumer Tests
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Run Pact tests
        run: npm run test:pact
      
      - name: Publish contract
        run: |
          npx pact-broker publish \
            pacts/ \
            --consumer-app-version $GITHUB_SHA \
            --broker-base-url $PACT_BROKER_URL \
            --broker-token $PACT_BROKER_TOKEN
```

### Publish to Broker (If Tests Pass)

See above

### Provider Verification Triggered (Webhook)

**Pact Broker Webhook:**
When: Contract published
Then: Trigger provider verification (webhook to CI)

---

## Common Pitfalls

### Testing Too Much (Test Contracts, Not Business Logic)

**Good:**
```javascript
// Test contract (structure)
expect(user).toHaveProperty('id');
expect(user).toHaveProperty('name');
expect(user).toHaveProperty('email');
```

**Bad:**
```javascript
// Don't test business logic in contract tests
expect(user.name).toBe('John Doe');  // Too specific
expect(user.email).toMatch(/@example.com$/);  // Business rule
```

### Not Versioning Contracts

**Bad:**
```
Contract published without version
→ Can't track which version is compatible
```

**Good:**
```
Contract published with git commit
→ Can track compatibility by version
```

### Provider Verification Not in CI

**Bad:**
```
Provider verification run manually
→ Easy to forget
→ Contracts not verified
```

**Good:**
```
Provider verification in CI
→ Runs on every commit
→ Contracts always verified
```

---

## Real-World Contract Testing Examples

### Microservices (Service-to-Service)

**Example:**
```
order-service → payment-service
order-service → inventory-service
order-service → notification-service

Each pair has a contract
```

### API Consumers (Mobile, Web)

**Example:**
```
mobile-app → user-api
web-app → user-api
partner-api → user-api

Each consumer has its own contract
```

### Event-Driven (Message Contracts)

**Example:**
```
user-service publishes: user.created
email-service consumes: user.created

Message contract between them
```

---

## Implementation Examples

### Pact Consumer Test (Python)
```python
from pact import Consumer, Provider

pact = Consumer('mobile-app').has_pact_with(Provider('user-api'))

user = get_user_by_id('123')

assert user['id'] == '123'
assert user['name'] == 'John Doe'
assert user['email'] == 'john@example.com'
```

### Pact Provider Verification
See "Provider Verifies Against Pact" above

---

## Summary

### Quick Reference

**Contract Testing:** Testing agreements between services

**Why:**
- Avoid breaking consumers
- Test independently
- Faster feedback
- Documentation

**Consumer-Driven:**
- Consumer defines needs
- Provider verifies it can provide

**Pact:**
- Popular CDC tool
- Consumer writes Pact tests
- Provider verifies against Pact
- Pact Broker (central registry)

**Workflow:**
1. Consumer writes contract test
2. Test generates contract JSON
3. Publish to broker
4. Provider pulls contract
5. Provider verification runs
6. Both pass → Safe to deploy

**Tools:**
- Pact (most popular)
- Spring Cloud Contract (Java)
- Specmatic (OpenAPI)
- openapi-validator

**CI/CD:**
- Consumer tests generate contract
- Publish to broker
- Provider verification triggered
- Can-I-Deploy gate

**Best Practices:**
- Test behavior, not implementation
- One contract per pair
- Version contracts
- Run verification on every change
- Use Can-I-Deploy
- Test independently
- Use consumer-driven for flexibility
