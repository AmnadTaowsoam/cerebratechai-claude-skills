---
name: SSO (SAML & OIDC)
description: Comprehensive guide to implementing Single Sign-On with SAML 2.0 and OpenID Connect for enterprise authentication
---

# SSO (SAML & OIDC)

## What is SSO?

**Single Sign-On (SSO):** Single authentication for multiple applications.

### How It Works
```
User logs in once → Identity Provider (IdP) → Access to all connected apps

Example:
1. User logs into Okta (IdP)
2. Clicks on Slack → Automatically logged in
3. Clicks on GitHub → Automatically logged in
4. Clicks on Salesforce → Automatically logged in

One login, access to all apps!
```

### Key Benefits

1. **Centralized Identity Management**
   - One source of truth for user identities
   - IT controls all user access from one place

2. **Better Security**
   - One strong password (enforced by IT)
   - vs many weak passwords (user-chosen)
   - Multi-factor authentication (MFA) enforced centrally

3. **Better User Experience**
   - No password fatigue
   - Seamless access to all apps

---

## Why Enterprises Require SSO

### 1. IT Control Over User Access

**Without SSO:**
```
Employee joins → Create account in 20 different apps manually
Employee leaves → Deactivate 20 accounts manually (often missed!)
```

**With SSO:**
```
Employee joins → Create account in IdP → Access to all apps
Employee leaves → Deactivate in IdP → Access removed from all apps
```

### 2. Audit and Compliance

**Requirements:**
- Who has access to what?
- When did they access it?
- Centralized audit logs

**SSO Provides:**
- Single audit trail (all logins in IdP)
- Access reviews (who has access to each app)
- Compliance reports (SOC2, ISO 27001)

### 3. Onboarding/Offboarding Automation

**Onboarding:**
```
1. Create user in IdP (Okta, Azure AD)
2. Assign to groups (Engineering, Sales, etc.)
3. Automatic access to all apps for that group
```

**Offboarding:**
```
1. Deactivate user in IdP
2. Access removed from all apps immediately
3. No orphaned accounts
```

### 4. Better Security

**Enforced Policies:**
- Password complexity (12+ characters, special chars)
- Multi-factor authentication (MFA)
- Session timeout (re-authenticate after 8 hours)
- IP restrictions (only from office network)

---

## SSO Protocols

### SAML 2.0 (Older, XML-Based, Enterprise Standard)

**Characteristics:**
- Released: 2005
- Format: XML
- Use case: Enterprise applications
- Complexity: High (XML, certificates)

**Pros:**
- Enterprise standard (all IdPs support it)
- Mature and well-tested
- Strong security (signed assertions)

**Cons:**
- Complex (XML, certificates)
- Verbose (large payloads)
- Harder to implement

### OpenID Connect (OIDC) (Modern, JSON-Based, OAuth 2.0)

**Characteristics:**
- Released: 2014
- Format: JSON (JWT)
- Use case: Modern web/mobile apps
- Complexity: Medium

**Pros:**
- Modern and simple
- JSON-based (easy to parse)
- Built on OAuth 2.0 (familiar)
- Mobile-friendly

**Cons:**
- Less universal in enterprise (but growing)
- Newer (less battle-tested)

### Comparison: When to Use Each

| Use Case | Protocol | Why |
|----------|----------|-----|
| **Enterprise B2B SaaS** | SAML 2.0 | Enterprise standard, required by most |
| **Modern web app** | OIDC | Simpler, JSON-based |
| **Mobile app** | OIDC | Mobile-friendly, OAuth 2.0 |
| **Consumer app** | OIDC | Social login (Google, Facebook) |
| **Legacy enterprise** | SAML 2.0 | Only protocol they support |

**Recommendation:** Support both SAML and OIDC for maximum compatibility.

---

## SAML Flow

### SP-Initiated (Service Provider Starts)

**Most Common Flow:**

```
1. User visits YourApp.com
2. Clicks "Login with SSO"
3. YourApp redirects to IdP (Okta)
4. User logs into Okta (if not already)
5. Okta generates SAML assertion (signed XML)
6. Okta redirects back to YourApp with assertion
7. YourApp validates assertion
8. User is logged in!
```

**Diagram:**
```
User → YourApp → IdP (Okta) → YourApp
       (1)       (2,3,4)      (5,6,7,8)
```

### IdP-Initiated (Identity Provider Starts)

**Less Common:**

```
1. User logs into Okta
2. Clicks on YourApp icon in Okta dashboard
3. Okta generates SAML assertion
4. Okta redirects to YourApp with assertion
5. YourApp validates assertion
6. User is logged in!
```

### SAML Assertion (Signed XML Token)

**Example:**
```xml
<saml:Assertion xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion">
  <saml:Issuer>https://idp.example.com</saml:Issuer>
  <saml:Subject>
    <saml:NameID>john.doe@example.com</saml:NameID>
  </saml:Subject>
  <saml:Conditions NotBefore="2024-01-15T10:00:00Z" NotOnOrAfter="2024-01-15T10:05:00Z">
    <saml:AudienceRestriction>
      <saml:Audience>https://yourapp.com</saml:Audience>
    </saml:AudienceRestriction>
  </saml:Conditions>
  <saml:AttributeStatement>
    <saml:Attribute Name="email">
      <saml:AttributeValue>john.doe@example.com</saml:AttributeValue>
    </saml:Attribute>
    <saml:Attribute Name="firstName">
      <saml:AttributeValue>John</saml:AttributeValue>
    </saml:Attribute>
    <saml:Attribute Name="lastName">
      <saml:AttributeValue>Doe</saml:AttributeValue>
    </saml:Attribute>
    <saml:Attribute Name="groups">
      <saml:AttributeValue>Engineering</saml:AttributeValue>
      <saml:AttributeValue>Admins</saml:AttributeValue>
    </saml:Attribute>
  </saml:AttributeStatement>
  <ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
    <!-- Digital signature -->
  </ds:Signature>
</saml:Assertion>
```

**Key Parts:**
- **Issuer:** Who created this assertion (IdP)
- **Subject:** Who is this assertion about (user email)
- **Conditions:** When is this valid (5 minute window)
- **Audience:** Who is this for (YourApp)
- **Attributes:** User info (email, name, groups)
- **Signature:** Cryptographic signature (proves authenticity)

---

## OIDC Flow

### Authorization Code Flow (Most Common for Web Apps)

**Flow:**
```
1. User clicks "Login with Google"
2. YourApp redirects to Google (with client_id, redirect_uri, scope)
3. User logs into Google (if not already)
4. Google redirects back to YourApp with authorization code
5. YourApp exchanges code for tokens (ID token, access token)
6. YourApp validates ID token
7. User is logged in!
```

**Diagram:**
```
User → YourApp → Google → YourApp (code) → Google (tokens) → YourApp
       (1)       (2,3)     (4)              (5)               (6,7)
```

### ID Token (JWT with User Claims)

**Example:**
```json
{
  "iss": "https://accounts.google.com",
  "sub": "110169484474386276334",
  "aud": "your-client-id.apps.googleusercontent.com",
  "exp": 1705315200,
  "iat": 1705311600,
  "email": "john.doe@example.com",
  "email_verified": true,
  "name": "John Doe",
  "picture": "https://lh3.googleusercontent.com/...",
  "given_name": "John",
  "family_name": "Doe"
}
```

**Key Claims:**
- **iss:** Issuer (Google)
- **sub:** Subject (unique user ID)
- **aud:** Audience (your app)
- **exp:** Expiration (Unix timestamp)
- **email:** User email
- **name:** User name

### Access Token (For API Calls)

**Use:** Call APIs on behalf of user

**Example:**
```
GET https://www.googleapis.com/oauth2/v1/userinfo
Authorization: Bearer <access_token>
```

### Refresh Token (Long-Lived Access)

**Use:** Get new access token without re-authenticating

**Flow:**
```
1. Access token expires (after 1 hour)
2. Use refresh token to get new access token
3. Continue using app (no re-login)
```

---

## Popular Identity Providers

### Okta

**Features:**
- SAML 2.0, OIDC
- SCIM provisioning
- MFA (SMS, authenticator app, hardware token)
- Lifecycle management

**Pricing:** $2-15/user/month

### Auth0

**Features:**
- OIDC, SAML 2.0
- Social login (Google, Facebook, GitHub)
- Passwordless (email magic link, SMS)
- Custom UI

**Pricing:** Free tier, then $23-240/month

### Azure AD (Entra ID)

**Features:**
- SAML 2.0, OIDC
- Integrated with Microsoft 365
- Conditional access (IP restrictions, device compliance)
- B2B collaboration

**Pricing:** Included with Microsoft 365, or $6/user/month

### Google Workspace

**Features:**
- SAML 2.0, OIDC
- Integrated with Google apps
- Simple setup
- Free for Google users

**Pricing:** Included with Google Workspace

### OneLogin

**Features:**
- SAML 2.0, OIDC
- SCIM provisioning
- Desktop SSO (Windows, Mac)
- MFA

**Pricing:** $2-8/user/month

### JumpCloud

**Features:**
- SAML 2.0, OIDC
- Directory-as-a-Service
- Device management (MDM)
- LDAP, RADIUS

**Pricing:** Free tier, then $8-20/user/month

---

## Implementing SAML

### Libraries

**Node.js:**
```bash
npm install passport-saml
```

**Python:**
```bash
pip install python3-saml
```

**Ruby:**
```bash
gem install ruby-saml
```

### Metadata Exchange

**IdP Metadata (From Okta):**
```xml
<EntityDescriptor entityID="http://www.okta.com/exk123">
  <IDPSSODescriptor>
    <KeyDescriptor use="signing">
      <KeyInfo>
        <X509Data>
          <X509Certificate>MIIDpDCCAoygAwIBAgIGAV...</X509Certificate>
        </X509Data>
      </KeyInfo>
    </KeyDescriptor>
    <SingleSignOnService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
                         Location="https://example.okta.com/app/exk123/sso/saml"/>
  </IDPSSODescriptor>
</EntityDescriptor>
```

**SP Metadata (Your App):**
```xml
<EntityDescriptor entityID="https://yourapp.com">
  <SPSSODescriptor>
    <AssertionConsumerService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
                              Location="https://yourapp.com/auth/saml/callback"
                              index="0"/>
  </SPSSODescriptor>
</EntityDescriptor>
```

### Certificate Management

**Signing Certificate:**
- IdP signs SAML assertion with private key
- Your app verifies with IdP's public key (from metadata)

**Encryption Certificate (Optional):**
- IdP encrypts assertion with your public key
- Your app decrypts with private key

**Certificate Rotation:**
```
1. Generate new certificate
2. Add to SP metadata (both old and new)
3. Update IdP with new metadata
4. Wait 30 days (for old cert to expire)
5. Remove old certificate
```

### Attribute Mapping

**IdP Sends:**
```xml
<saml:Attribute Name="email">
  <saml:AttributeValue>john.doe@example.com</saml:AttributeValue>
</saml:Attribute>
<saml:Attribute Name="firstName">
  <saml:AttributeValue>John</saml:AttributeValue>
</saml:Attribute>
```

**Your App Maps:**
```javascript
const user = {
  email: assertion.attributes.email,
  firstName: assertion.attributes.firstName,
  lastName: assertion.attributes.lastName,
  groups: assertion.attributes.groups || []
};
```

### Implementation Example (Node.js + Passport)

```javascript
const passport = require('passport');
const SamlStrategy = require('passport-saml').Strategy;

passport.use(new SamlStrategy({
  entryPoint: 'https://example.okta.com/app/exk123/sso/saml',
  issuer: 'https://yourapp.com',
  callbackUrl: 'https://yourapp.com/auth/saml/callback',
  cert: fs.readFileSync('./idp-cert.pem', 'utf-8'), // IdP public key
  identifierFormat: null
}, async (profile, done) => {
  // Find or create user
  let user = await db.users.findOne({ email: profile.email });
  
  if (!user) {
    // Just-In-Time (JIT) provisioning
    user = await db.users.create({
      email: profile.email,
      firstName: profile.firstName,
      lastName: profile.lastName,
      ssoProvider: 'okta'
    });
  } else {
    // Update user attributes
    await db.users.update(user.id, {
      firstName: profile.firstName,
      lastName: profile.lastName
    });
  }
  
  done(null, user);
}));

// Routes
app.get('/auth/saml', passport.authenticate('saml'));

app.post('/auth/saml/callback',
  passport.authenticate('saml', { failureRedirect: '/login' }),
  (req, res) => {
    res.redirect('/dashboard');
  }
);
```

---

## Implementing OIDC

### Libraries

**Node.js:**
```bash
npm install passport-openidconnect
```

**Python:**
```bash
pip install authlib
```

### Discovery Endpoint

**URL:** `https://idp.example.com/.well-known/openid-configuration`

**Response:**
```json
{
  "issuer": "https://accounts.google.com",
  "authorization_endpoint": "https://accounts.google.com/o/oauth2/v2/auth",
  "token_endpoint": "https://oauth2.googleapis.com/token",
  "userinfo_endpoint": "https://openidconnect.googleapis.com/v1/userinfo",
  "jwks_uri": "https://www.googleapis.com/oauth2/v3/certs",
  "response_types_supported": ["code", "token", "id_token"],
  "subject_types_supported": ["public"],
  "id_token_signing_alg_values_supported": ["RS256"]
}
```

### Client ID and Secret

**Configuration:**
```javascript
const config = {
  clientID: 'your-client-id',
  clientSecret: 'your-client-secret',
  redirectURI: 'https://yourapp.com/auth/callback',
  scope: 'openid email profile'
};
```

### Redirect URIs (Whitelist)

**IdP Configuration:**
```
Allowed redirect URIs:
• https://yourapp.com/auth/callback
• https://staging.yourapp.com/auth/callback
• http://localhost:3000/auth/callback (for development)
```

**Security:** IdP only redirects to whitelisted URIs

### Claims (Standard)

**Standard Claims:**
- **sub:** Subject (unique user ID)
- **email:** Email address
- **email_verified:** Email verified (boolean)
- **name:** Full name
- **given_name:** First name
- **family_name:** Last name
- **picture:** Profile picture URL

**Custom Claims:**
```json
{
  "sub": "123",
  "email": "john@example.com",
  "custom:role": "admin",
  "custom:department": "Engineering"
}
```

### Implementation Example (Node.js + Passport)

```javascript
const passport = require('passport');
const OpenIDConnectStrategy = require('passport-openidconnect').Strategy;

passport.use(new OpenIDConnectStrategy({
  issuer: 'https://accounts.google.com',
  authorizationURL: 'https://accounts.google.com/o/oauth2/v2/auth',
  tokenURL: 'https://oauth2.googleapis.com/token',
  userInfoURL: 'https://openidconnect.googleapis.com/v1/userinfo',
  clientID: process.env.GOOGLE_CLIENT_ID,
  clientSecret: process.env.GOOGLE_CLIENT_SECRET,
  callbackURL: 'https://yourapp.com/auth/callback',
  scope: ['openid', 'email', 'profile']
}, async (issuer, profile, done) => {
  // Find or create user
  let user = await db.users.findOne({ email: profile.emails[0].value });
  
  if (!user) {
    user = await db.users.create({
      email: profile.emails[0].value,
      firstName: profile.name.givenName,
      lastName: profile.name.familyName,
      picture: profile.photos[0].value
    });
  }
  
  done(null, user);
}));

// Routes
app.get('/auth/google', passport.authenticate('openidconnect'));

app.get('/auth/callback',
  passport.authenticate('openidconnect', { failureRedirect: '/login' }),
  (req, res) => {
    res.redirect('/dashboard');
  }
);
```

---

## Just-In-Time (JIT) Provisioning

### What is JIT?

**Definition:** Create user on first SSO login (instead of pre-creating)

**Flow:**
```
1. User logs in via SSO (first time)
2. SAML assertion contains email, name, groups
3. Your app checks: Does user exist?
4. No → Create user with info from assertion
5. Yes → Update user attributes
6. User is logged in
```

### Implementation

```javascript
async function handleSAMLAssertion(assertion) {
  const email = assertion.attributes.email;
  
  let user = await db.users.findOne({ email });
  
  if (!user) {
    // JIT provisioning: Create user
    user = await db.users.create({
      email: assertion.attributes.email,
      firstName: assertion.attributes.firstName,
      lastName: assertion.attributes.lastName,
      groups: assertion.attributes.groups || [],
      ssoProvider: 'okta',
      createdVia: 'jit'
    });
    
    console.log(`JIT provisioned user: ${email}`);
  } else {
    // Update user attributes on each login
    await db.users.update(user.id, {
      firstName: assertion.attributes.firstName,
      lastName: assertion.attributes.lastName,
      groups: assertion.attributes.groups || []
    });
  }
  
  return user;
}
```

### JIT vs SCIM

**JIT (Pull):**
- User created on first login
- Simple to implement
- No user management API needed

**SCIM (Push):**
- IdP creates user proactively
- User exists before first login
- Requires SCIM API implementation

**When to Use:**
- **JIT:** Small/medium customers, simple setup
- **SCIM:** Enterprise customers, need pre-provisioning

---

## Group/Role Mapping

### IdP Sends Group Claims

**SAML:**
```xml
<saml:Attribute Name="groups">
  <saml:AttributeValue>Engineering</saml:AttributeValue>
  <saml:AttributeValue>Admins</saml:AttributeValue>
</saml:Attribute>
```

**OIDC:**
```json
{
  "groups": ["Engineering", "Admins"]
}
```

### Map IdP Groups to Application Roles

**Mapping Configuration:**
```javascript
const groupRoleMapping = {
  'Admins': 'admin',
  'Engineering': 'member',
  'Sales': 'member',
  'Viewers': 'viewer'
};

function mapGroupsToRoles(groups) {
  const roles = groups
    .map(group => groupRoleMapping[group])
    .filter(role => role !== undefined);
  
  // Default to 'member' if no groups match
  return roles.length > 0 ? roles : ['member'];
}

// Usage
const userRoles = mapGroupsToRoles(assertion.attributes.groups);
await db.users.update(user.id, { roles: userRoles });
```

### Common Roles

- **Admin:** Full control (create, edit, delete everything)
- **Manager:** Create and edit (but not delete)
- **Member:** Create and edit own content
- **Viewer:** Read-only access

---

## Multi-Tenancy with SSO

### Different IdP Per Customer

**Challenge:** Each customer has their own IdP (Okta, Azure AD, etc.)

**Solution:** Store IdP configuration per tenant

**Database Schema:**
```sql
CREATE TABLE sso_configs (
  id UUID PRIMARY KEY,
  tenant_id UUID REFERENCES tenants(id),
  provider VARCHAR(50), -- 'saml' or 'oidc'
  idp_entity_id VARCHAR(255),
  idp_sso_url VARCHAR(255),
  idp_certificate TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### Tenant Identification

**Option 1: Domain-Based**
```
User enters email: john@acme.com
→ Look up tenant by domain: acme.com
→ Redirect to Acme's IdP
```

**Option 2: Custom URL**
```
https://acme.yourapp.com/login
→ Identify tenant from subdomain: acme
→ Redirect to Acme's IdP
```

**Option 3: Tenant Selector**
```
User selects tenant from dropdown
→ Redirect to selected tenant's IdP
```

### Multiple SAML/OIDC Configs

**Implementation:**
```javascript
app.get('/auth/saml/:tenantId', async (req, res, next) => {
  const { tenantId } = req.params;
  
  // Load SSO config for this tenant
  const ssoConfig = await db.ssoConfigs.findOne({ tenantId });
  
  if (!ssoConfig) {
    return res.status(404).send('SSO not configured for this tenant');
  }
  
  // Create SAML strategy with tenant-specific config
  const strategy = new SamlStrategy({
    entryPoint: ssoConfig.idpSsoUrl,
    issuer: `https://yourapp.com/${tenantId}`,
    callbackUrl: `https://yourapp.com/auth/saml/${tenantId}/callback`,
    cert: ssoConfig.idpCertificate
  }, (profile, done) => {
    // Handle authentication
  });
  
  passport.use(`saml-${tenantId}`, strategy);
  passport.authenticate(`saml-${tenantId}`)(req, res, next);
});
```

---

## SSO Debugging

### SAML Tracer (Browser Extension)

**Tool:** SAML-tracer (Firefox/Chrome extension)

**What It Shows:**
- SAML requests (from your app to IdP)
- SAML responses (from IdP to your app)
- Assertion contents (decoded XML)
- Signatures (valid or invalid)

**How to Use:**
1. Install SAML-tracer extension
2. Open extension
3. Perform SSO login
4. Review captured SAML messages

### JWT Decoder (jwt.io)

**Tool:** https://jwt.io

**What It Shows:**
- Decoded JWT header
- Decoded JWT payload (claims)
- Signature verification

**How to Use:**
1. Copy ID token from network tab
2. Paste into jwt.io
3. Review claims
4. Verify signature (paste public key)

### Logs (Authentication Attempts)

**What to Log:**
```javascript
console.log('SSO login attempt', {
  tenantId,
  email: assertion.attributes.email,
  timestamp: new Date(),
  success: true
});

// On error
console.error('SSO login failed', {
  tenantId,
  error: err.message,
  assertionIssuer: assertion.issuer,
  timestamp: new Date()
});
```

### Common Errors

**1. Certificate Mismatch**
```
Error: Invalid signature
Cause: IdP certificate in your config doesn't match actual IdP certificate
Fix: Update IdP certificate in your config
```

**2. Clock Skew**
```
Error: Assertion expired
Cause: Server clocks out of sync (>5 minutes)
Fix: Sync server clocks with NTP
```

**3. Invalid Signature**
```
Error: Signature verification failed
Cause: Assertion tampered with, or wrong certificate
Fix: Verify IdP certificate, check for MITM
```

**4. Audience Mismatch**
```
Error: Audience validation failed
Cause: Assertion audience doesn't match your app's entity ID
Fix: Update entity ID in IdP config
```

---

## Security Considerations

### 1. Validate Signatures

**SAML:**
```javascript
// Verify SAML assertion signature
const isValid = saml.validateSignature(assertion, idpCertificate);
if (!isValid) {
  throw new Error('Invalid SAML signature');
}
```

**OIDC (JWT):**
```javascript
const jwt = require('jsonwebtoken');

// Verify JWT signature
try {
  const decoded = jwt.verify(idToken, publicKey, {
    algorithms: ['RS256'],
    issuer: 'https://accounts.google.com',
    audience: 'your-client-id'
  });
} catch (err) {
  throw new Error('Invalid JWT signature');
}
```

### 2. Check Token Expiration

```javascript
// SAML
if (new Date() > new Date(assertion.conditions.notOnOrAfter)) {
  throw new Error('SAML assertion expired');
}

// OIDC
if (Date.now() / 1000 > decoded.exp) {
  throw new Error('JWT expired');
}
```

### 3. Audience Validation

```javascript
// SAML
if (assertion.audience !== 'https://yourapp.com') {
  throw new Error('Assertion not intended for this app');
}

// OIDC
if (decoded.aud !== 'your-client-id') {
  throw new Error('Token not intended for this app');
}
```

### 4. HTTPS Only

```
❌ http://yourapp.com/auth/saml/callback (insecure!)
✅ https://yourapp.com/auth/saml/callback (secure)
```

### 5. Secure Session Management

```javascript
// Set secure session cookie
app.use(session({
  secret: process.env.SESSION_SECRET,
  cookie: {
    secure: true,      // HTTPS only
    httpOnly: true,    // No JavaScript access
    sameSite: 'lax',   // CSRF protection
    maxAge: 8 * 60 * 60 * 1000  // 8 hours
  }
}));
```

---

## Testing SSO

### Test IdP Accounts

**Create Test Accounts:**
```
test-admin@example.com (Admin role)
test-user@example.com (User role)
test-viewer@example.com (Viewer role)
```

### Mock IdP for Development

**Tools:**
- **saml-idp:** Mock SAML IdP (Node.js)
- **mock-oauth2-server:** Mock OIDC provider

**Example (saml-idp):**
```javascript
const { runServer } = require('saml-idp');

runServer({
  acsUrl: 'http://localhost:3000/auth/saml/callback',
  audience: 'http://localhost:3000',
  config: {
    user: 'test@example.com',
    email: 'test@example.com',
    firstName: 'Test',
    lastName: 'User'
  }
});
```

### Manual Testing with Customer IdP

**Process:**
1. Customer provides test account
2. Configure SSO with customer's IdP
3. Test login with test account
4. Verify user attributes (email, name, groups)
5. Test role mapping
6. Test logout

### Automated Tests (Headless Browser)

**Example (Puppeteer):**
```javascript
const puppeteer = require('puppeteer');

test('SSO login flow', async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  // Navigate to app
  await page.goto('http://localhost:3000/login');
  
  // Click SSO button
  await page.click('#sso-login');
  
  // Fill in IdP login form
  await page.waitForSelector('#username');
  await page.type('#username', 'test@example.com');
  await page.type('#password', 'password123');
  await page.click('#submit');
  
  // Verify redirected back to app
  await page.waitForNavigation();
  expect(page.url()).toBe('http://localhost:3000/dashboard');
  
  await browser.close();
});
```

---

## SSO for Different User Types

### Enterprise Customers (Required)

**Requirement:** SAML SSO (must-have for enterprise sales)

**Features:**
- SAML 2.0 support
- Custom IdP configuration per tenant
- Group/role mapping
- JIT provisioning

### Small Business (Optional)

**Recommendation:** Google/Microsoft social login (simpler than full SSO)

**Features:**
- OIDC with Google Workspace
- OIDC with Microsoft 365
- Easier setup (no IT admin needed)

### Consumers (Social Login, Not SSO)

**Recommendation:** Social login (Google, Facebook, GitHub)

**Features:**
- OIDC with social providers
- No enterprise features needed
- Simple signup flow

---

## Pricing SSO (Common B2B SaaS Pattern)

### Typical Pricing Tiers

**Basic Plan ($10/user/month):**
- Email/password login
- No SSO

**Business Plan ($25/user/month):**
- SAML SSO
- JIT provisioning
- Basic role mapping

**Enterprise Plan ($50/user/month):**
- SAML SSO
- SCIM provisioning
- Advanced role mapping
- Custom attributes
- Dedicated support

**Why SSO is Premium:**
- Enterprise feature (only large customers need it)
- Implementation cost (engineering time)
- Support cost (SSO troubleshooting)
- Value to customer (security, compliance)

---

## Implementation Examples

### Node.js + Passport + SAML

See "Implementing SAML" section above

### Python + Flask + OIDC

```python
from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = 'your-secret-key'

oauth = OAuth(app)
oauth.register(
    name='google',
    client_id='your-client-id',
    client_secret='your-client-secret',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    token = oauth.google.authorize_access_token()
    user_info = token['userinfo']
    
    # Find or create user
    user = User.query.filter_by(email=user_info['email']).first()
    if not user:
        user = User(
            email=user_info['email'],
            first_name=user_info['given_name'],
            last_name=user_info['family_name']
        )
        db.session.add(user)
        db.session.commit()
    
    session['user_id'] = user.id
    return redirect('/dashboard')
```

### Next.js + NextAuth.js

```javascript
// pages/api/auth/[...nextauth].js
import NextAuth from 'next-auth';
import GoogleProvider from 'next-auth/providers/google';

export default NextAuth({
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    }),
  ],
  callbacks: {
    async signIn({ user, account, profile }) {
      // Find or create user in database
      const dbUser = await db.users.findOne({ email: user.email });
      
      if (!dbUser) {
        await db.users.create({
          email: user.email,
          name: user.name,
          image: user.image,
        });
      }
      
      return true;
    },
    async session({ session, token }) {
      // Add user ID to session
      session.user.id = token.sub;
      return session;
    },
  },
});

// pages/login.js
import { signIn } from 'next-auth/react';

export default function Login() {
  return (
    <button onClick={() => signIn('google')}>
      Sign in with Google
    </button>
  );
}
```

---

## Real SSO Integration Scenarios

### Scenario 1: Mid-Market Customer (Okta SAML)

**Customer:** 500-person company using Okta

**Requirements:**
- SAML SSO
- JIT provisioning
- Map Okta groups to app roles

**Implementation:**
1. Customer provides Okta metadata URL
2. Import metadata, extract IdP certificate and SSO URL
3. Configure SAML strategy with customer's IdP
4. Test with customer's test account
5. Map Okta groups to app roles (Admins → admin, Users → member)
6. Go live

**Timeline:** 1-2 weeks

### Scenario 2: Enterprise Customer (Azure AD + SCIM)

**Customer:** 10,000-person company using Azure AD

**Requirements:**
- SAML SSO
- SCIM provisioning (create users before first login)
- Custom role mapping
- Audit logs

**Implementation:**
1. Configure SAML with Azure AD
2. Implement SCIM API (see SCIM skill)
3. Azure AD pushes users via SCIM
4. Users log in via SAML
5. Custom role mapping (Azure AD groups → app roles)
6. Enable audit logging

**Timeline:** 4-8 weeks

### Scenario 3: Small Business (Google Workspace)

**Customer:** 50-person company using Google Workspace

**Requirements:**
- Simple SSO (no IT admin)
- Google login

**Implementation:**
1. Enable OIDC with Google
2. Customer admin adds app to Google Workspace
3. Users click app icon in Google → auto-login
4. JIT provisioning

**Timeline:** 1 day

---

## Summary

### Quick Reference

**SSO Protocols:**
- SAML 2.0: Enterprise standard, XML-based
- OIDC: Modern, JSON-based, OAuth 2.0

**SAML Flow:**
1. User → App → IdP
2. IdP authenticates user
3. IdP → App (SAML assertion)
4. App validates assertion
5. User logged in

**OIDC Flow:**
1. User → App → IdP
2. IdP authenticates user
3. IdP → App (authorization code)
4. App → IdP (exchange code for tokens)
5. App validates ID token
6. User logged in

**Popular IdPs:**
- Okta, Auth0, Azure AD, Google Workspace, OneLogin, JumpCloud

**Implementation:**
- Node.js: passport-saml, passport-openidconnect
- Python: python3-saml, authlib
- Next.js: NextAuth.js

**JIT Provisioning:**
- Create user on first SSO login
- Update attributes on each login

**Multi-Tenancy:**
- Different IdP per customer
- Store SSO config per tenant
- Tenant identification (domain, subdomain)

**Security:**
- Validate signatures (SAML, JWT)
- Check expiration
- Audience validation
- HTTPS only

**Pricing:**
- Basic: No SSO
- Business: SAML SSO
- Enterprise: SAML + SCIM

**Testing:**
- SAML tracer (browser extension)
- JWT decoder (jwt.io)
- Mock IdP (development)
- Automated tests (Puppeteer)

## Best Practices

### SAML Implementation Best Practices
- **Use Established Libraries**: Leverage existing SAML libraries (passport-saml for Node.js, python3-saml for Python, ruby-saml for Ruby) instead of implementing from scratch. This reduces bugs and speeds up development.
- **Validate Signatures**: Always verify SAML assertion signatures using the IdP's public certificate. Never trust unsigned assertions.
- **Check Expiration**: Validate assertion expiration time (`notOnOrAfter`) and reject expired assertions. This prevents replay attacks.
- **Audience Validation**: Verify that the assertion's audience matches your application's entity ID. This prevents assertion reuse across applications.
- **Clock Synchronization**: Ensure your server clocks are synchronized with NTP to prevent clock skew issues (assertions expire too quickly or appear expired).

### OIDC Implementation Best Practices
- **Use Discovery Endpoint**: Fetch OIDC configuration from the `.well-known/openid-configuration` endpoint instead of hardcoding URLs. This ensures you always use current endpoints.
- **Validate JWT Signatures**: Verify ID token signatures using the IdP's public keys from the JWKS endpoint. Never trust unsigned tokens.
- **Check Token Expiration**: Validate JWT `exp` claim and reject expired tokens. Implement refresh token flow for long-lived sessions.
- **Audience and Issuer Validation**: Verify that the token's `aud` matches your client ID and `iss` matches the expected issuer.
- **Secure Token Storage**: Store tokens securely on the client-side (httpOnly cookies, secure storage). Never store tokens in localStorage.

### SSO Configuration Best Practices
- **Metadata Exchange**: Use SAML metadata exchange for configuration. This reduces manual errors and ensures correct certificate and endpoint configuration.
- **Certificate Rotation**: Implement certificate rotation with overlap period. Add new certificate before removing old one to prevent downtime.
- **Redirect URI Whitelist**: Configure allowed redirect URIs in your IdP. Never redirect to untrusted URLs.
- **Attribute Mapping**: Map IdP attributes to your user model consistently. Handle missing attributes gracefully.
- **Error Handling**: Return clear, user-friendly error messages for SSO failures. Log detailed errors for debugging.

### JIT Provisioning Best Practices
- **Create on First Login**: Implement JIT provisioning to create users on first SSO login. This reduces manual user management.
- **Update on Each Login**: Sync user attributes from SSO on each login to keep data current.
- **Default Roles**: Assign default roles based on user attributes or group membership. Allow manual override if needed.
- **Handle Existing Users**: If user already exists, update their attributes instead of creating duplicate.
- **Log Provisioning**: Audit log all JIT provisioning events (user creation, attribute updates).

### Group/Role Mapping Best Practices
- **Map IdP Groups to App Roles**: Configure mapping between IdP groups and application roles. This allows IT admins to control access through their IdP.
- **Handle Multiple Groups**: Users may belong to multiple groups. Combine permissions from all mapped roles.
- **Default Role Fallback**: If no groups match, assign a default role (e.g., 'member'). Never leave users without any role.
- **Sync on Each Login**: Update user roles on each SSO login based on current group membership.
- **Document Mapping**: Maintain clear documentation of group-to-role mappings for customer reference.

### Multi-Tenancy Best Practices
- **Tenant-Specific SSO Config**: Store SAML/OIDC configuration per tenant. Each customer can have their own IdP.
- **Tenant Identification**: Identify tenant from subdomain, email domain, or explicit selection before redirecting to IdP.
- **Isolate User Data**: Ensure users from different tenants cannot access each other's data. Always filter by tenant ID.
- **Separate Sessions**: Use tenant-specific session cookies or include tenant ID in session to prevent cross-tenant access.
- **Audit by Tenant**: Maintain separate audit logs per tenant for compliance and troubleshooting.

### Security Best Practices
- **HTTPS Only**: Enforce HTTPS for all SSO endpoints. Never use HTTP for authentication flows.
- **Secure Session Management**: Use secure, httpOnly cookies with SameSite protection. Set appropriate session timeouts.
- **Validate All Inputs**: Validate all SAML/OIDC inputs (assertions, tokens, parameters) to prevent injection attacks.
- **Rate Limiting**: Implement rate limiting on SSO endpoints to prevent brute force attacks.
- **Monitor Suspicious Activity**: Alert on failed login attempts, unusual login patterns, or access from unusual locations.

### Testing Best Practices
- **Test with Real IdPs**: Test your SSO implementation with actual IdPs (Okta, Azure AD, Google Workspace, OneLogin).
- **Use SAML Tracer**: Install SAML-tracer browser extension to debug SAML flows. This shows assertions, signatures, and errors.
- **Use JWT Decoder**: Use jwt.io to decode and verify JWT tokens. This helps debug OIDC flows.
- **Test Edge Cases**: Test scenarios like expired tokens, invalid signatures, clock skew, and network failures.
- **Automated Testing**: Create automated tests for SSO flows using headless browsers (Puppeteer, Playwright).

### User Experience Best Practices
- **Clear Login Options**: Display clear SSO login buttons with IdP logos. Provide email/password as fallback.
- **Error Messages**: Show user-friendly error messages for SSO failures. Provide clear next steps (contact support, try again).
- **Loading States**: Show loading indicators during SSO redirect and token exchange. Users should know the system is working.
- **Session Persistence**: Maintain user session across browser tabs. Use consistent cookie domains and paths.
- **Logout Handling**: Implement proper logout (both local session and IdP logout) for complete sign-out.

## Checklist

### SAML Implementation Checklist
- [ ] Install SAML library for your platform
- [ ] Configure SAML strategy with IdP metadata
- [ ] Implement SAML assertion validation (signature, expiration, audience)
- [ ] Implement SAML callback endpoint
- [ ] Implement JIT provisioning for new users
- [ ] Implement user attribute mapping
- [ ] Implement group/role mapping
- [ ] Add error handling for SAML failures
- [ ] Add logging for SAML operations
- [ ] Test with Okta
- [ ] Test with Azure AD
- [ ] Test with OneLogin

### OIDC Implementation Checklist
- [ ] Install OIDC library for your platform
- [ ] Configure OIDC strategy with client credentials
- [ ] Implement authorization code flow
- [ ] Implement token exchange endpoint
- [ ] Implement JWT validation (signature, expiration, audience, issuer)
- [ ] Implement refresh token flow
- [ ] Implement JIT provisioning for new users
- [ ] Implement user attribute mapping
- [ ] Implement group/role mapping
- [ ] Add error handling for OIDC failures
- [ ] Add logging for OIDC operations
- [ ] Test with Google
- [ ] Test with Auth0

### SSO Configuration Checklist
- [ ] Obtain IdP metadata (SAML) or client credentials (OIDC)
- [ ] Configure redirect URIs in IdP
- [ ] Set up certificate rotation plan
- [ ] Configure attribute mapping
- [ ] Configure group/role mapping
- [ ] Set up error handling
- [ ] Configure HTTPS for all endpoints
- [ ] Document SSO configuration process

### JIT Provisioning Checklist
- [ ] Implement user creation on first login
- [ ] Implement user update on subsequent logins
- [ ] Assign default roles based on attributes/groups
- [ ] Handle existing users correctly
- [ ] Log all provisioning events
- [ ] Test JIT provisioning flow

### Multi-Tenancy Checklist
- [ ] Design tenant-specific SSO configuration storage
- [ ] Implement tenant identification (subdomain, email, selection)
- [ ] Ensure tenant data isolation
- [ ] Implement tenant-specific sessions
- [ ] Add tenant filtering to all queries
- [ ] Test multi-tenant SSO flows

### Security Checklist
- [ ] Enforce HTTPS for all SSO endpoints
- [ ] Implement secure session cookies (httpOnly, secure, SameSite)
- [ ] Validate all SAML assertions
- [ ] Validate all JWT tokens
- [ ] Implement rate limiting on SSO endpoints
- [ ] Set up monitoring for suspicious activity
- [ ] Implement proper logout (local + IdP)

### Testing Checklist
- [ ] Install SAML-tracer browser extension
- [ ] Install JWT decoder (jwt.io)
- [ ] Create test accounts in each IdP
- [ ] Test SAML flow with Okta
- [ ] Test SAML flow with Azure AD
- [ ] Test OIDC flow with Google
- [ ] Test OIDC flow with Auth0
- [ ] Test edge cases (expired tokens, invalid signatures)
- [ ] Create automated tests for SSO flows
- [ ] Test multi-tenant scenarios

### User Experience Checklist
- [ ] Design clear SSO login buttons
- [ ] Add IdP logos to login buttons
- [ ] Provide email/password fallback
- [ ] Implement loading indicators
- [ ] Write user-friendly error messages
- [ ] Test cross-tab session persistence
- [ ] Test logout flow (local + IdP)
- [ ] Test on mobile browsers

### Deployment Checklist
- [ ] Configure production IdP connections
- [ ] Set up SSL certificates
- [ ] Configure monitoring dashboards
- [ ] Set up error alerts
- [ ] Train support team on SSO issues
- [ ] Create troubleshooting guide
- [ ] Document SSO configuration for customers
- [ ] Test with production IdP before go-live

### Maintenance Checklist
- [ ] Monitor SSO success rates
- [ ] Monitor SSO error rates
- [ ] Track certificate expiration dates
- [ ] Review and update attribute mappings
- [ ] Review and update group/role mappings
- [ ] Schedule periodic SSO testing
- [ ] Keep libraries updated
- [ ] Review IdP configuration changes
