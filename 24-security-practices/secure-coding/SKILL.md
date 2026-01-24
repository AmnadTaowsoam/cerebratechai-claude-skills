---
name: Secure Coding
description: Writing secure code following security principles like least privilege, defense in depth, input validation, and secure design patterns to prevent vulnerabilities.
---

# Secure Coding

> **Current Level:** Intermediate  
> **Domain:** Security / Code Quality

---

## Overview

Secure coding practices prevent vulnerabilities and security breaches by following security principles from the start. Effective secure coding includes input validation, output encoding, proper error handling, and following security best practices throughout the development lifecycle.

## Secure Coding Principles

### Core Principles

| Principle | Description | Example |
|-----------|-------------|---------|
| **Principle of Least Privilege** | Grant minimum necessary access | Read-only DB user for reporting |
| **Defense in Depth** | Multiple security layers | Input validation + parameterized queries |
| **Fail Securely** | Errors don't expose information | Generic error messages |
| **Keep It Simple** | Complexity = bugs | Avoid over-engineering |
| **Don't Trust Input** | Validate and sanitize all input | Never trust client-side validation |

### Security by Design

**Build security from the start, not as an afterthought.**

```
┌─────────────────────────────────────────────────────────────────┐
│  Secure Development Lifecycle                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Requirements ──▶ Design ──▶ Implementation ──▶ Testing   │
│  (Threat model)   (Secure patterns) (Secure code) (Security tests) │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Input Validation and Sanitization

### Validation Principles

| Principle | Description |
|-----------|-------------|
| **Validate on Server** | Never trust client-side validation |
| **Use Allowlists** | Whitelist valid values (safer than blocklist) |
| **Validate Type** | Ensure data type is correct |
| **Validate Length** | Limit input length |
| **Validate Format** | Use regex for format validation |

### Input Validation Examples

```javascript
// Bad: No validation
app.post('/signup', (req, res) => {
    const { username, email, password } = req.body;
    // Direct use without validation!
    createUser(username, email, password);
});

// Good: Comprehensive validation
const { body } = require('express-validator');

app.post('/signup',
    body('username')
        .isLength({ min: 3, max: 20 })
        .matches(/^[a-zA-Z0-9_]+$/)
        .withMessage('Username must be 3-20 alphanumeric characters'),
    body('email')
        .isEmail()
        .normalizeEmail()
        .withMessage('Invalid email'),
    body('password')
        .isLength({ min: 8 })
        .matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/)
        .withMessage('Password must be 8+ chars with uppercase, lowercase, and number'),
    (req, res) => {
        const errors = validationResult(req);
        if (!errors.isEmpty()) {
            return res.status(400).json({ errors: errors.array() });
        }
        createUser(req.body);
        res.json({ success: true });
    }
);
```

### Sanitization

```javascript
// Bad: No sanitization
const userInput = req.query.search;
db.query(`SELECT * FROM products WHERE name LIKE '%${userInput}%'`);

// Good: Sanitize input
const { escape } = require('validator');
const userInput = escape(req.query.search);
db.query('SELECT * FROM products WHERE name LIKE $1', [`%${userInput}%`]);
```

### Allowlist vs Blocklist

```javascript
// Bad: Blocklist (can be bypassed)
const forbiddenChars = ['<', '>', '\'', '"'];
function sanitize(input) {
    return forbiddenChars.forEach(char => input.replace(char, ''));
}

// Good: Allowlist (only allow known safe characters)
function sanitize(input) {
    return input.replace(/[^a-zA-Z0-9_\-@.]/g, '');
}
```

## Output Encoding

### Prevent XSS

```javascript
// Bad: Direct output (vulnerable to XSS)
app.get('/profile', (req, res) => {
    const name = req.user.name;
    res.send(`<h1>Hello, ${name}</h1>`); // XSS vulnerability!
});

// Good: Template engine with auto-escaping
app.get('/profile', (req, res) => {
    res.render('profile', { name: req.user.name }); // Auto-escaped
});

// Good: Manual encoding
const escape = require('escape-html');
app.get('/profile', (req, res) => {
    const name = escape(req.user.name);
    res.send(`<h1>Hello, ${name}</h1>`);
});
```

### Context-Aware Encoding

```javascript
// HTML context
escapeHtml(userInput);

// JavaScript context
escapeJs(userInput);

// URL context
encodeURIComponent(userInput);

// CSS context
escapeCss(userInput);

// HTML attribute context
escapeHtmlAttr(userInput);
```

## SQL Injection Prevention

### Parameterized Queries

```javascript
// Bad: String concatenation (vulnerable)
app.get('/user/:id', (req, res) => {
    const query = `SELECT * FROM users WHERE id = ${req.params.id}`;
    db.query(query, (err, result) => {
        res.json(result);
    });
});

// Good: Parameterized query
app.get('/user/:id', (req, res) => {
    const query = 'SELECT * FROM users WHERE id = $1';
    db.query(query, [req.params.id], (err, result) => {
        res.json(result);
    });
});
```

### ORM Usage

```javascript
// Good: Using ORM (automatically parameterizes)
const User = require('./models/user');

app.get('/user/:id', async (req, res) => {
    const user = await User.findByPk(req.params.id);
    res.json(user);
});
```

### Stored Procedures

```sql
-- Create stored procedure
CREATE PROCEDURE get_user_by_id(IN user_id INT)
BEGIN
    SELECT * FROM users WHERE id = user_id;
END;
```

```javascript
// Call stored procedure
app.get('/user/:id', async (req, res) => {
    const user = await db.query('CALL get_user_by_id(?)', [req.params.id]);
    res.json(user);
});
```

## Authentication and Session Management

### Password Hashing

```javascript
// Bad: Plaintext or weak hashing
function hashPassword(password) {
    return md5(password); // MD5 is broken!
}

// Good: Strong password hashing
const bcrypt = require('bcrypt');

async function hashPassword(password) {
    const salt = await bcrypt.genSalt(10);
    return await bcrypt.hash(password, salt);
}

async function verifyPassword(password, hash) {
    return await bcrypt.compare(password, hash);
}
```

### Session Management

```javascript
// Bad: Weak session management
app.use(session({
    secret: 'weak-secret',
    cookie: {
        secure: false, // Should be true in production
        httpOnly: false, // Should be true
        maxAge: 86400000 // 24 hours
    }
}));

// Good: Secure session management
app.use(session({
    secret: process.env.SESSION_SECRET, // From environment
    cookie: {
        secure: true, // HTTPS only
        httpOnly: true, // Prevent XSS
        sameSite: 'strict', // Prevent CSRF
        maxAge: 3600000 // 1 hour
    },
    name: 'sessionId',
    resave: false,
    saveUninitialized: false
}));
```

### JWT Implementation

```javascript
const jwt = require('jsonwebtoken');

// Bad: Weak JWT secrets
function generateToken(user) {
    return jwt.sign(user, 'weak-secret'); // Predictable!
}

// Good: Strong JWT implementation
function generateToken(user) {
    return jwt.sign(
        { userId: user.id, role: user.role },
        process.env.JWT_SECRET,
        { expiresIn: '1h' }
    );
}

function verifyToken(token) {
    try {
        return jwt.verify(token, process.env.JWT_SECRET);
    } catch (err) {
        return null;
    }
}
```

## Authorization Checks

### Role-Based Access Control

```javascript
// Bad: No authorization check
app.delete('/user/:id', async (req, res) => {
    await User.destroy({ where: { id: req.params.id } });
    res.json({ success: true });
});

// Good: Authorization check
app.delete('/user/:id', requireAuth, requireAdmin, async (req, res) => {
    // Only admins can delete users
    await User.destroy({ where: { id: req.params.id } });
    res.json({ success: true });
});

function requireAuth(req, res, next) {
    if (!req.user) {
        return res.status(401).json({ error: 'Unauthorized' });
    }
    next();
}

function requireAdmin(req, res, next) {
    if (req.user.role !== 'admin') {
        return res.status(403).json({ error: 'Forbidden' });
    }
    next();
}
```

### Resource-Based Access Control

```javascript
// Good: Check user owns resource
app.delete('/document/:id', requireAuth, async (req, res) => {
    const document = await Document.findByPk(req.params.id);
    
    if (!document) {
        return res.status(404).json({ error: 'Not found' });
    }
    
    if (document.userId !== req.user.id && req.user.role !== 'admin') {
        return res.status(403).json({ error: 'Forbidden' });
    }
    
    await document.destroy();
    res.json({ success: true });
});
```

## Error Handling

### Don't Leak Information

```javascript
// Bad: Detailed error messages
app.use((err, req, res, next) => {
    res.status(500).json({
        error: err.message,
        stack: err.stack // Exposes internal details!
    });
});

// Good: Generic error messages
app.use((err, req, res, next) => {
    console.error(err); // Log full error for debugging
    res.status(500).json({
        error: 'Internal server error'
    });
});
```

### Custom Error Classes

```javascript
class AppError extends Error {
    constructor(message, statusCode) {
        super(message);
        this.statusCode = statusCode;
        this.isOperational = true;
    }
}

class NotFoundError extends AppError {
    constructor(message = 'Not found') {
        super(message, 404);
    }
}

class UnauthorizedError extends AppError {
    constructor(message = 'Unauthorized') {
        super(message, 401);
    }
}

class ForbiddenError extends AppError {
    constructor(message = 'Forbidden') {
        super(message, 403);
    }
}
```

## Cryptography Best Practices

### Encryption

```javascript
const crypto = require('crypto');

// Good: AES-256 encryption
function encrypt(text, key) {
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv('aes-256-cbc', Buffer.from(key), iv);
    let encrypted = cipher.update(text);
    encrypted = Buffer.concat([encrypted, cipher.final()]);
    return { iv: iv.toString('hex'), content: encrypted.toString('hex') };
}

function decrypt(encrypted, iv, key) {
    const decipher = crypto.createDecipheriv('aes-256-cbc', Buffer.from(key), Buffer.from(iv, 'hex'));
    let decrypted = decipher.update(Buffer.from(encrypted, 'hex'));
    decrypted = Buffer.concat([decrypted, decipher.final()]);
    return decrypted.toString();
}
```

### Key Management

```javascript
// Bad: Hardcoded keys
const apiKey = 'sk_live_1234567890abcdef';

// Good: Environment variables
const apiKey = process.env.API_KEY;

// Better: Key management service
const apiKey = await keyManagementService.getKey('api-key');
```

### Secure Random

```javascript
// Bad: Predictable random
const token = Math.random().toString(36);

// Good: Cryptographically secure random
const crypto = require('crypto');
const token = crypto.randomBytes(32).toString('hex');
```

## Secure File Handling

### File Upload Validation

```javascript
const multer = require('multer');
const path = require('path');

// Good: Secure file upload configuration
const upload = multer({
    dest: 'uploads/',
    limits: {
        fileSize: 5 * 1024 * 1024 // 5MB limit
    },
    fileFilter: (req, file, cb) => {
        const allowedTypes = ['image/jpeg', 'image/png', 'application/pdf'];
        if (!allowedTypes.includes(file.mimetype)) {
            return cb(new Error('Invalid file type'), false);
        }
        
        const ext = path.extname(file.originalname);
        const allowedExts = ['.jpg', '.jpeg', '.png', '.pdf'];
        if (!allowedExts.includes(ext.toLowerCase())) {
            return cb(new Error('Invalid file extension'), false);
        }
        
        cb(null, true);
    }
});

app.post('/upload', upload.single('file'), (req, res) => {
    // File is validated and saved
    res.json({ success: true, filename: req.file.filename });
});
```

### File Access Control

```javascript
const fs = require('fs');
const path = require('path');

// Good: Validate file path
app.get('/files/:filename', (req, res) => {
    const filename = req.params.filename;
    const safeFilename = path.basename(filename); // Prevent path traversal
    const filepath = path.join('uploads', safeFilename);
    
    // Verify file is within uploads directory
    const realPath = path.resolve(filepath);
    const uploadsPath = path.resolve('uploads');
    
    if (!realPath.startsWith(uploadsPath)) {
        return res.status(403).json({ error: 'Forbidden' });
    }
    
    res.download(filepath);
});
```

## API Security

### API Authentication

```javascript
const jwt = require('jsonwebtoken');

// Good: API authentication middleware
function authenticateApiKey(req, res, next) {
    const apiKey = req.headers['x-api-key'];
    
    if (!apiKey) {
        return res.status(401).json({ error: 'API key required' });
    }
    
    const validKey = await ApiKey.findOne({ where: { key: apiKey } });
    if (!validKey || !validKey.isActive) {
        return res.status(401).json({ error: 'Invalid API key' });
    }
    
    req.apiKey = validKey;
    next();
}

app.get('/api/data', authenticateApiKey, (req, res) => {
    res.json({ data: 'protected data' });
});
```

### Rate Limiting

```javascript
const rateLimit = require('express-rate-limit');

// Good: Rate limiting for API
const apiLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // limit each IP to 100 requests per windowMs
    message: 'Too many requests from this IP, please try again later.'
});

app.use('/api/', apiLimiter);
```

### CORS Configuration

```javascript
const cors = require('cors');

// Bad: Allow all origins
app.use(cors());

// Good: Restrictive CORS
app.use(cors({
    origin: ['https://example.com', 'https://app.example.com'],
    methods: ['GET', 'POST'],
    allowedHeaders: ['Content-Type', 'Authorization'],
    credentials: true
}));
```

## Code Review for Security

### Security Review Checklist

| Category | Checks |
|-----------|---------|
| **Input Validation** | All user input validated? |
| **Output Encoding** | All output properly encoded? |
| **SQL Injection** | Parameterized queries used? |
| **Authentication** | Strong password hashing? |
| **Authorization** | Proper access controls? |
| **Error Handling** | No information leakage? |
| **Cryptography** | Strong algorithms used? |
| **Session Management** | Secure session configuration? |
| **File Handling** | File uploads validated? |

### Code Review Process

```
┌─────────────────────────────────────────────────────────────────┐
│  Secure Code Review Process                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Self-Review                                                 │
│     └─ Review your own code before submitting                  │
│                                                                  │
│  2. Peer Review                                                 │
│     └─ Another developer reviews the code                            │
│                                                                  │
│  3. Security Review                                              │
│     └─ Security expert reviews the code                              │
│                                                                  │
│  4. Automated Scanning                                           │
│     └─ Run SAST tools (SonarQube, Snyk)                      │
│                                                                  │
│  5. Fix Issues                                                   │
│     └─ Address all findings                                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## SAST Tools Integration

### SonarQube

```bash
# Scan code
sonar-scanner \
  -Dsonar.projectKey=my-project \
  -Dsonar.sources=src/ \
  -Dsonar.host.url=http://localhost:9000
```

### Snyk

```bash
# Scan for vulnerabilities
snyk test

# Monitor dependencies
snyk monitor
```

### ESLint Security

```json
{
  "extends": [
    "eslint:recommended",
    "plugin:security/recommended"
  ],
  "plugins": ["security"]
}
```

## Security Linting Rules

### ESLint Security Plugin

```javascript
// Bad: eval() usage
const userInput = req.body.code;
eval(userInput); // Security risk!

// Good: Avoid eval()
// Use alternative approach
```

### Custom Linting Rules

```javascript
// Rule: No hardcoded secrets
module.exports = {
    meta: {
        type: 'suggestion',
        docs: {
            description: 'Disallow hardcoded secrets',
            category: 'Security'
        }
    },
    create: function(context) {
        return {
            Program: function() {
                return {
                    node: node,
                    message: 'Hardcoded secret detected',
                    fix: 'Use environment variables'
                };
            }
        };
    }
};
```

## Language-Specific Security

### Node.js Security

```javascript
// Good: Use Helmet for security headers
const helmet = require('helmet');
app.use(helmet());

// Good: Use express-validator
const { body, validationResult } = require('express-validator');

// Good: Use bcrypt for passwords
const bcrypt = require('bcrypt');

// Good: Use rate limiting
const rateLimit = require('express-rate-limit');
```

### Python Security

```python
# Good: Use parameterized queries
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# Good: Use bcrypt for passwords
import bcrypt
hashed = bcrypt.hashpw(password, bcrypt.gensalt())

# Good: Use Flask-Security for auth
from flask_security import Security, UserMixin
```

### Java Security

```java
// Good: Use PreparedStatement
PreparedStatement stmt = conn.prepareStatement("SELECT * FROM users WHERE id = ?");
stmt.setInt(1, userId);

// Good: Use BCrypt for passwords
String hashed = BCrypt.hashpw(password, BCrypt.gensalt());

// Good: Use Spring Security
@Configuration
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {
    // Security configuration
}
```

## Real Code Examples

### Vulnerable vs Secure Code

#### SQL Injection

```javascript
// Vulnerable
app.get('/user/:id', (req, res) => {
    db.query(`SELECT * FROM users WHERE id = ${req.params.id}`);
});

// Secure
app.get('/user/:id', (req, res) => {
    db.query('SELECT * FROM users WHERE id = $1', [req.params.id]);
});
```

#### XSS

```javascript
// Vulnerable
app.get('/search', (req, res) => {
    res.send(`Results for: ${req.query.q}`);
});

// Secure
app.get('/search', (req, res) => {
    res.send(`Results for: ${escapeHtml(req.query.q)}`);
});
```

#### Path Traversal

```javascript
// Vulnerable
app.get('/file/:path', (req, res) => {
    res.sendFile(req.params.path);
});

// Secure
app.get('/file/:path', (req, res) => {
    const safePath = path.basename(req.params.path);
    res.sendFile(path.join('files', safePath));
});
```

#### Command Injection

```javascript
// Vulnerable
app.get('/ping/:host', (req, res) => {
    exec(`ping -c 1 ${req.params.host}`);
});

// Secure
app.get('/ping/:host', (req, res) => {
    const { spawn } = require('child_process');
    // Validate host is valid hostname
    if (!/^[a-zA-Z0-9.-]+$/.test(req.params.host)) {
        return res.status(400).json({ error: 'Invalid hostname' });
    }
    spawn('ping', ['-c', '1', req.params.host]);
});
```

---

## Quick Start

### Input Validation

```python
from pydantic import BaseModel, validator, EmailStr

class UserInput(BaseModel):
    email: EmailStr
    age: int
    
    @validator('age')
    def validate_age(cls, v):
        if v < 0 or v > 150:
            raise ValueError('Age must be between 0 and 150')
        return v

# Usage
try:
    user = UserInput(email="user@example.com", age=25)
except ValidationError as e:
    # Handle validation error
    pass
```

### Parameterized Queries

```python
# ❌ Bad - SQL injection risk
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

# ✅ Good - Parameterized query
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

---

## Production Checklist

- [ ] **Input Validation**: Validate and sanitize all user input
- [ ] **Output Encoding**: Encode output to prevent XSS
- [ ] **Parameterized Queries**: Use parameterized queries (no SQL injection)
- [ ] **Authentication**: Implement proper authentication
- [ ] **Authorization**: Implement proper authorization (RBAC)
- [ ] **Error Handling**: Don't expose sensitive info in errors
- [ ] **Secrets Management**: Never commit secrets to code
- [ ] **Dependencies**: Keep dependencies updated (vulnerability scanning)
- [ ] **SAST**: Run static analysis security testing
- [ ] **DAST**: Run dynamic analysis security testing
- [ ] **Code Review**: Security-focused code reviews
- [ ] **Security Training**: Team trained on secure coding

---

## Anti-patterns

### ❌ Don't: Trust User Input

```python
# ❌ Bad - No validation
def process_user_input(data):
    return f"Hello {data['name']}"  # XSS risk!
```

```python
# ✅ Good - Validate and encode
from html import escape

def process_user_input(data):
    name = validate_name(data['name'])  # Validate
    return f"Hello {escape(name)}"  # Encode
```

### ❌ Don't: SQL Injection

```python
# ❌ Bad - SQL injection
query = f"SELECT * FROM users WHERE name = '{name}'"
```

```python
# ✅ Good - Parameterized query
query = "SELECT * FROM users WHERE name = %s"
cursor.execute(query, (name,))
```

### ❌ Don't: Expose Secrets

```python
# ❌ Bad - Secret in code
api_key = "sk-1234567890"  # Committed to repo!
```

```python
# ✅ Good - Environment variable
api_key = os.getenv('API_KEY')  # From secrets manager
```

---

## Integration Points

- **Secrets Management** (`24-security-practices/secrets-management/`) - Secure secrets
- **OWASP Top 10** (`24-security-practices/owasp-top-10/`) - Common vulnerabilities
- **Security Audit** (`24-security-practices/security-audit/`) - Security reviews

---

## Further Reading

- [OWASP Secure Coding](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [Secure Coding Guidelines](https://cheatsheetseries.owasp.org/)
- [ ] Run dependency scan
- [ ] Review security headers
- [ ] Test for vulnerabilities
- [ ] Document security controls

### After Deployment

- [ ] Monitor for attacks
- [ ] Review logs regularly
- [ ] Stay updated on vulnerabilities
- [ ] Update dependencies regularly
- [ ] Conduct regular security reviews
