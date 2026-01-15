# llm.txt Protocol

## Overview

The llm.txt protocol is a standardized way for websites to provide information about their AI capabilities and endpoints to AI agents and language models.

---

## 1. What is llm.txt

### Definition

```markdown
# What is llm.txt?

## Definition
llm.txt is a text file that provides structured information about a website's AI capabilities, available endpoints, and usage guidelines for AI agents and language models.

## Purpose
- Enable AI agents to discover available capabilities
- Provide clear usage guidelines
- Specify rate limits and authentication
- Document available models and endpoints
- Enable programmatic access to AI features

## Location
- `/llm.txt` (root directory)
- `/.well-known/llm.txt` (standard location)
- Both locations can be used

## Format
- Plain text
- Key-value pairs
- Sections with headers
- Comments with #
```

### History and Context

```markdown
# llm.txt History

## Origins
- Inspired by robots.txt
- Designed for AI agents
- Standardized for LLM integration
- Community-driven specification

## Use Cases
- AI-powered search
- Content generation
- Chatbot integration
- Data analysis
- Automation workflows
```

---

## 2. Purpose and Benefits

### Benefits of llm.txt

```markdown
# Benefits of llm.txt

## For Website Owners
- **Control**: Control how AI agents interact with your site
- **Documentation**: Document AI capabilities clearly
- **Rate Limiting**: Specify rate limits proactively
- **Analytics**: Track AI agent usage
- **Compliance**: Ensure AI agents follow your policies

## For AI Agents
- **Discovery**: Easily discover AI capabilities
- **Integration**: Simplify integration process
- **Guidelines**: Follow best practices
- **Reliability**: Know what's supported
- **Efficiency**: Avoid unsupported features

## For Users
- **Better Experience**: Improved AI-powered features
- **Consistency**: Consistent behavior across agents
- **Transparency**: Know how AI is being used
- **Control**: Understand data usage
- **Privacy**: Know data handling practices
```

---

## 3. File Structure

### Basic Structure

```markdown
# llm.txt File Structure

## Basic Format
```
# Site Information
name: Site Name
version: 1.0
description: Site description
url: https://example.com

# AI Capabilities
models:
  - name: gpt-4
    provider: openai
    capabilities:
      - text-generation
      - summarization
      - translation
    rate_limit: 1000 requests/hour
    authentication: api_key

# Endpoints
endpoints:
  - path: /api/chat
    method: POST
    description: Chat endpoint
    authentication: required
    rate_limit: 100 requests/minute
  - path: /api/summarize
    method: POST
    description: Summarization endpoint
    authentication: required
    rate_limit: 50 requests/minute

# Usage Guidelines
usage:
  - Always include attribution
  - Respect rate limits
  - Follow content policies
  - Implement proper error handling
  - Cache responses when appropriate

# Contact
contact:
  email: ai@example.com
  documentation: https://example.com/docs/ai
```
```

### Advanced Structure

```markdown
# Advanced llm.txt Structure

## Sections
1. **Site Information**: Basic site details
2. **AI Capabilities**: Available models and features
3. **Endpoints**: API endpoints for AI features
4. **Rate Limits**: Usage limits and quotas
5. **Authentication**: Authentication requirements
6. **Usage Guidelines**: Best practices and policies
7. **Pricing**: Cost information
8. **Support**: Support resources
9. **Contact**: Contact information
10. **Legal**: Legal and compliance information
```

---

## 4. Location

### File Locations

```markdown
# llm.txt Locations

## Standard Locations
- `/llm.txt` - Root directory
- `/.well-known/llm.txt` - Standard location

## Recommended Location
Use both locations for maximum compatibility:
```
/llm.txt
/.well-known/llm.txt
```

## HTTP Headers
```
Content-Type: text/plain; charset=utf-8
Cache-Control: public, max-age=3600
```

## Access Control
- Should be publicly accessible
- No authentication required
- Allow CORS if needed
```

---

## 5. Content Format

### Site Information

```markdown
# Site Information Section

## Required Fields
```
name: Site Name
url: https://example.com
version: 1.0
```

## Optional Fields
```
description: Site description for AI integration
language: en
timezone: UTC
created: 2024-01-01
updated: 2024-01-01
```

## Example
```
# Site Information
name: Example AI Platform
url: https://example.com
version: 1.0
description: AI-powered content generation platform
language: en
timezone: UTC
created: 2024-01-01
updated: 2024-01-01
```
```

### AI Capabilities

```markdown
# AI Capabilities Section

## Model Information
```
models:
  - name: gpt-4
    provider: openai
    version: latest
    capabilities:
      - text-generation
      - summarization
      - translation
      - question-answering
    context_window: 128000
    max_tokens: 4096
    rate_limit: 1000 requests/hour
    authentication: api_key
    pricing: $0.03/1k tokens
  - name: claude-3
    provider: anthropic
    version: latest
    capabilities:
      - text-generation
      - summarization
      - question-answering
    context_window: 200000
    max_tokens: 4096
    rate_limit: 500 requests/hour
    authentication: api_key
    pricing: $0.015/1k tokens
```

## Capabilities List
- text-generation
- summarization
- translation
- question-answering
- code-generation
- image-generation
- audio-transcription
- audio-generation
- data-analysis
```

### Available Endpoints

```markdown
# Endpoints Section

## Endpoint Format
```
endpoints:
  - path: /api/chat
    method: POST
    description: Chat with AI model
    authentication: required
    rate_limit: 100 requests/minute
    parameters:
      - name: model
        type: string
        required: true
        description: AI model to use
      - name: messages
        type: array
        required: true
        description: Chat messages
      - name: temperature
        type: number
        required: false
        description: Sampling temperature
        default: 0.7
      - name: max_tokens
        type: integer
        required: false
        description: Maximum tokens to generate
        default: 2048
    response:
      - name: message
        type: object
        description: AI response
      - name: usage
        type: object
        description: Token usage
    errors:
      - code: 429
        message: Rate limit exceeded
      - code: 401
        message: Invalid API key
```

## Common Endpoint Types
- `/api/chat` - Chat completion
- `/api/completion` - Text completion
- `/api/summarize` - Text summarization
- `/api/translate` - Translation
- `/api/embeddings` - Text embeddings
- `/api/image` - Image generation
```

### Usage Guidelines

```markdown
# Usage Guidelines Section

## Required Guidelines
```
usage:
  - Always include proper attribution
  - Respect rate limits
  - Implement exponential backoff on errors
  - Cache responses when appropriate
  - Handle errors gracefully
  - Follow content policies
  - Respect user privacy
  - Implement proper logging
  - Monitor usage and costs
```

## Best Practices
- Implement proper error handling
- Use appropriate retry logic
- Cache responses when possible
- Monitor API usage
- Implement rate limiting on client side
- Use appropriate models for tasks
- Optimize token usage
- Handle streaming responses
- Implement proper logging
```

### Rate Limits

```markdown
# Rate Limits Section

## Rate Limit Format
```
rate_limits:
  global:
    requests_per_hour: 10000
    requests_per_minute: 100
  per_endpoint:
    /api/chat:
      requests_per_minute: 50
      requests_per_hour: 1000
    /api/completion:
      requests_per_minute: 30
      requests_per_hour: 500
```

## Rate Limit Headers
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

## Handling Rate Limits
- Implement exponential backoff
- Respect rate limit headers
- Queue requests appropriately
- Monitor rate limit usage
```

### Authentication

```markdown
# Authentication Section

## Authentication Methods
```
authentication:
  type: api_key
  header_name: Authorization
  header_format: Bearer {api_key}
  api_key_endpoint: /api/keys
  documentation: https://example.com/docs/authentication
```

## API Key Management
- Generate API keys
- Rotate keys regularly
- Revoke compromised keys
- Monitor key usage
- Implement key permissions
```

---

## 6. Implementation Examples

### Example 1: Simple llm.txt

```markdown
# Simple llm.txt Example

# Site Information
name: My Blog
url: https://myblog.com
version: 1.0

# AI Capabilities
models:
  - name: gpt-4
    provider: openai
    capabilities:
      - text-generation
      - summarization
    rate_limit: 1000 requests/hour
    authentication: api_key

# Endpoints
endpoints:
  - path: /api/ai/generate
    method: POST
    description: Generate blog content
    authentication: required
    rate_limit: 50 requests/minute

# Usage Guidelines
usage:
  - Always include attribution
  - Respect rate limits
  - Follow content policies
```

### Example 2: Advanced llm.txt

```markdown
# Advanced llm.txt Example

# Site Information
name: AI Content Platform
url: https://aiplatform.com
version: 2.0
description: AI-powered content generation platform
language: en
timezone: UTC
created: 2024-01-01
updated: 2024-01-15

# AI Capabilities
models:
  - name: gpt-4
    provider: openai
    version: latest
    capabilities:
      - text-generation
      - summarization
      - translation
      - question-answering
      - code-generation
    context_window: 128000
    max_tokens: 4096
    rate_limit:
      requests_per_hour: 1000
      tokens_per_minute: 150000
    authentication: api_key
    pricing:
      input: $0.03/1k tokens
      output: $0.06/1k tokens
  - name: claude-3
    provider: anthropic
    version: latest
    capabilities:
      - text-generation
      - summarization
      - question-answering
    context_window: 200000
    max_tokens: 4096
    rate_limit:
      requests_per_hour: 500
      tokens_per_minute: 50000
    authentication: api_key
    pricing:
      input: $0.015/1k tokens
      output: $0.075/1k tokens

# Endpoints
endpoints:
  - path: /api/v1/chat
    method: POST
    description: Chat with AI model
    authentication: required
    rate_limit: 100 requests/minute
    parameters:
      - name: model
        type: string
        required: true
        enum: [gpt-4, claude-3]
      - name: messages
        type: array
        required: true
        min_items: 1
        max_items: 50
      - name: temperature
        type: number
        required: false
        minimum: 0
        maximum: 2
        default: 0.7
      - name: max_tokens
        type: integer
        required: false
        minimum: 1
        maximum: 4096
        default: 2048
      - name: stream
        type: boolean
        required: false
        default: false
    response:
      - name: id
        type: string
        description: Request ID
      - name: choices
        type: array
        description: Chat completions
      - name: usage
        type: object
        description: Token usage
    errors:
      - code: 400
        message: Invalid request
      - code: 401
        message: Invalid API key
      - code: 429
        message: Rate limit exceeded
      - code: 500
        message: Internal server error
  - path: /api/v1/completions
    method: POST
    description: Text completion
    authentication: required
    rate_limit: 50 requests/minute
    parameters:
      - name: model
        type: string
        required: true
      - name: prompt
        type: string
        required: true
        max_length: 4000
      - name: max_tokens
        type: integer
        required: false
        default: 2048
    response:
      - name: text
        type: string
        description: Generated text
      - name: usage
        type: object
        description: Token usage
    errors:
      - code: 400
        message: Invalid request
      - code: 401
        message: Invalid API key
      - code: 429
        message: Rate limit exceeded
      - code: 500
        message: Internal server error

# Rate Limits
rate_limits:
  global:
    requests_per_hour: 10000
    requests_per_minute: 200
  per_model:
    gpt-4:
      requests_per_hour: 1000
      tokens_per_minute: 150000
    claude-3:
      requests_per_hour: 500
      tokens_per_minute: 50000

# Usage Guidelines
usage:
  - Always include proper attribution
  - Respect rate limits
  - Implement exponential backoff on errors
  - Cache responses when appropriate
  - Handle errors gracefully
  - Follow content policies
  - Respect user privacy
  - Implement proper logging
  - Monitor usage and costs
  - Use appropriate models for tasks
  - Optimize token usage

# Pricing
pricing:
  currency: USD
  models:
    gpt-4:
      input: $0.03/1k tokens
      output: $0.06/1k tokens
    claude-3:
      input: $0.015/1k tokens
      output: $0.075/1k tokens

# Support
support:
  email: support@example.com
  documentation: https://example.com/docs
  status_page: https://status.example.com
  community: https://community.example.com

# Contact
contact:
  email: ai@example.com
  twitter: @example_ai
  github: https://github.com/example
```

---

## 7. Best Practices

### Writing llm.txt

```markdown
# llm.txt Best Practices

## 1. Keep It Updated
- Update when capabilities change
- Update when models change
- Update when pricing changes
- Update when endpoints change

## 2. Be Specific
- Be clear about capabilities
- Be specific about rate limits
- Be detailed about parameters
- Be explicit about errors

## 3. Provide Examples
- Include request examples
- Include response examples
- Include error examples
- Include code examples

## 4. Document Everything
- Document all endpoints
- Document all parameters
- Document all errors
- Document all rate limits

## 5. Use Standard Format
- Follow the specification
- Use consistent formatting
- Use standard sections
- Use standard field names

## 6. Include Contact Info
- Provide support email
- Provide documentation link
- Provide status page
- Provide community link

## 7. Be Transparent
- Be honest about limitations
- Be clear about pricing
- Be explicit about policies
- Be open about changes
```

### Security Considerations

```markdown
# Security Best Practices

## 1. Authentication
- Require API keys for sensitive operations
- Implement key rotation
- Revoke compromised keys
- Use HTTPS only

## 2. Rate Limiting
- Implement rate limiting
- Use exponential backoff
- Respect rate limit headers
- Monitor abuse

## 3. Data Privacy
- Don't log sensitive data
- Anonymize logs
- Follow privacy regulations
- Get user consent

## 4. Input Validation
- Validate all inputs
- Sanitize user input
- Limit input size
- Prevent injection attacks

## 5. Error Handling
- Don't expose sensitive info
- Use generic error messages
- Log errors securely
- Monitor for attacks
```

---

## 8. Integration with AI Agents

### Agent Discovery

```markdown
# AI Agent Integration

## Discovery Process
1. AI agent requests /llm.txt
2. Parses capabilities and endpoints
3. Determines appropriate model
4. Makes API calls
5. Handles responses

## Discovery Libraries
- Python: llm-txt-parser
- JavaScript: llm-txt-parser-js
- Go: llm-txt-parser-go
- Rust: llm-txt-parser-rust
```

### Integration Example

```python
# Python integration example
import requests
import json

def discover_ai_capabilities(url):
    """Discover AI capabilities from llm.txt"""
    try:
        response = requests.get(f"{url}/llm.txt")
        response.raise_for_status()
        
        # Parse llm.txt
        capabilities = parse_llm_txt(response.text)
        
        return capabilities
    except requests.RequestException as e:
        print(f"Error fetching llm.txt: {e}")
        return None

def use_ai_endpoint(url, endpoint, data, api_key):
    """Use AI endpoint"""
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        }
        
        response = requests.post(
            f"{url}{endpoint}",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        
        return response.json()
    except requests.RequestException as e:
        print(f"Error calling endpoint: {e}")
        return None

# Usage
capabilities = discover_ai_capabilities("https://example.com")

if capabilities and 'endpoints' in capabilities:
    chat_endpoint = capabilities['endpoints'][0]
    
    response = use_ai_endpoint(
        "https://example.com",
        chat_endpoint['path'],
        {
            "model": "gpt-4",
            "messages": [{"role": "user", "content": "Hello!"}]
        },
        "your-api-key"
    )
    
    print(response)
```

---

## 9. Real-World Examples

### Example 1: Content Platform

```markdown
# Content Platform llm.txt

```
# Site Information
name: ContentHub AI
url: https://contenthub.ai
version: 1.0

# AI Capabilities
models:
  - name: gpt-4
    provider: openai
    capabilities:
      - article-writing
      - blog-post-generation
      - social-media-content
    rate_limit: 500 requests/hour

# Endpoints
endpoints:
  - path: /api/v1/generate-article
    method: POST
    description: Generate article content
    authentication: required
    rate_limit: 50 requests/minute

# Usage Guidelines
usage:
  - Always include attribution
  - Respect rate limits
  - Follow content guidelines
```
```

### Example 2: Chatbot Platform

```markdown
# Chatbot Platform llm.txt

```
# Site Information
name: ChatBot Pro
url: https://chatbotpro.com
version: 2.0

# AI Capabilities
models:
  - name: claude-3
    provider: anthropic
    capabilities:
      - chat
      - question-answering
    rate_limit: 1000 requests/hour

# Endpoints
endpoints:
  - path: /api/v1/chat
    method: POST
    description: Chat with AI assistant
    authentication: required
    rate_limit: 100 requests/minute
    streaming: true

# Usage Guidelines
usage:
  - Implement proper error handling
  - Respect rate limits
  - Handle streaming responses
```
```

---

## Quick Reference

### llm.txt Template

```markdown
# llm.txt Template

# Site Information
name: Your Site Name
url: https://example.com
version: 1.0

# AI Capabilities
models:
  - name: model-name
    provider: provider-name
    capabilities:
      - capability-1
      - capability-2
    rate_limit: X requests/hour
    authentication: api_key

# Endpoints
endpoints:
  - path: /api/endpoint
    method: POST
    description: Endpoint description
    authentication: required
    rate_limit: X requests/minute

# Usage Guidelines
usage:
  - Guideline 1
  - Guideline 2
  - Guideline 3

# Contact
contact:
  email: contact@example.com
  documentation: https://example.com/docs
```
