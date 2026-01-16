# Routing Rules

## Overview

Routing rules are the decision logic that maps task characteristics to appropriate skills. They automate skill selection, ensuring the right skills are used for each task efficiently and consistently.

## What Are Routing Rules

Routing rules are:

- **Decision logic** to select relevant skills
- **Maps triggers** (task descriptions) to skills
- **Automates skill selection** - no manual selection needed
- **Ensures consistency** - same trigger → same skills
- **Scales efficiently** - handle many skills without overhead

## Why Routing Matters

| Benefit | Description |
|---------|-------------|
| **Efficiency** - Don't read irrelevant skills |
| **Accuracy** - Use right skills for task |
| **Consistency** - Same trigger → same skills |
| **Scalability** - Handle many skills effectively |
| **Speed** - Quick skill selection |
| **Quality** - Better results from relevant skills |

---

## Routing Dimensions

Key dimensions for routing decisions.

### 1. Task Type

What kind of work is being done?

```
Task Type Routing:

"Create" → Design + development skills
- Example: "Create user registration API"
  → api-design, authentication, database-design

"Fix bug" → Debugging + testing skills
- Example: "Fix login bug"
  → debugging, testing, error-handling

"Optimize" → Performance + profiling skills
- Example: "Optimize database queries"
  → db-query-optimization, performance-engineering, caching

"Deploy" → DevOps + deployment skills
- Example: "Deploy to production"
  → ci-cd, deployment-strategies, monitoring

"Review" → Code review + quality skills
- Example: "Review pull request"
  → code-review-standards, lint-format-typecheck
```

### 2. Domain

What area or industry?

```
Domain Routing:

"AI" → ML, RAG, LLM skills
- Example: "Build AI chatbot"
  → rag-evaluation, llm-patterns, prompt-engineering

"Frontend" → React, CSS, accessibility skills
- Example: "Build user dashboard"
  → react-patterns, css-patterns, accessibility

"Backend" → API, database, security skills
- Example: "Build payment API"
  → api-design, database-design, security

"Data" → ETL, data quality, analytics skills
- Example: "Build data pipeline"
  → data-pipeline, data-quality, sql-for-analytics

"Mobile" → Mobile development skills
- Example: "Build iOS app"
  → react-native-patterns, mobile-ci-cd, offline-mode
```

### 3. Technology

What tech stack is being used?

```
Technology Routing:

"TypeScript" → TypeScript standards, Node.js skills
- Example: "Build TypeScript API"
  → typescript-standards, nodejs-best-practices

"Python" → Python best practices, FastAPI skills
- Example: "Build Python API"
  → python-best-practices, fastapi-patterns

"React" → React patterns, hooks skills
- Example: "Build React component"
  → react-patterns, react-hooks

"PostgreSQL" → Database optimization, SQL skills
- Example: "Optimize PostgreSQL"
  → db-query-optimization, sql-for-analytics

"Kubernetes" → DevOps, orchestration skills
- Example: "Deploy to Kubernetes"
  → kubernetes-patterns, devops-infrastructure
```

### 4. Phase

What phase of the project?

```
Phase Routing:

Planning → Requirements, scope, estimation skills
- Example: "Plan new feature"
  → discovery-questions, requirement-to-scope, estimation

Development → Coding, testing, Git skills
- Example: "Implement feature"
  → code-quality, testing, git-workflow

Deployment → CI/CD, monitoring, incident skills
- Example: "Deploy to production"
  → ci-cd, monitoring, incident-management

Maintenance → Debugging, optimization, refactoring skills
- Example: "Fix performance issue"
  → debugging, performance-engineering, refactoring
```

---

## Task Type Routing

Map task verbs to skill categories.

### Create Tasks

```
Trigger: "Create [X]"

Routing:
- Design skills (if new feature)
- Development skills
- Testing skills
- Documentation skills

Examples:
"Create user API" → api-design, authentication, database-design, testing
"Create dashboard" → react-patterns, data-visualization, accessibility
"Create data pipeline" → data-pipeline, data-quality, etl-patterns
```

### Fix Tasks

```
Trigger: "Fix [bug]"

Routing:
- Debugging skills
- Testing skills
- Error handling skills
- Root cause analysis skills

Examples:
"Fix login bug" → debugging, testing, error-handling
"Fix performance issue" → debugging, performance-engineering, profiling
"Fix security vulnerability" → debugging, security-practices, penetration-testing
```

### Optimize Tasks

```
Trigger: "Optimize [X]"

Routing:
- Performance skills
- Profiling skills
- Caching skills
- Database optimization skills

Examples:
"Optimize database queries" → db-query-optimization, performance-engineering, caching
"Optimize frontend performance" → performance-engineering, caching-strategies
"Optimize API response time" → performance-engineering, caching, api-design
```

### Deploy Tasks

```
Trigger: "Deploy [X]"

Routing:
- DevOps skills
- CI/CD skills
- Deployment strategy skills
- Monitoring skills

Examples:
"Deploy to production" → ci-cd, deployment-strategies, monitoring
"Deploy database migration" → database-health-monitoring, deployment-strategies
"Deploy ML model" → ml-serving, monitoring, deployment-strategies
```

---

## Domain Routing

Map domain keywords to skill categories.

### AI Domain

```
Trigger Keywords: "AI", "ML", "machine learning", "chatbot", "LLM", "RAG"

Routing:
Must-Have:
- rag-evaluation
- llm-patterns
- prompt-engineering

Recommended:
- safety-guardrails
- cost-optimization
- monitoring

Optional:
- multi-agent
- function-calling
- fine-tuning

Examples:
"Build AI chatbot" → rag-evaluation, llm-patterns, prompt-engineering, safety-guardrails
"Implement RAG system" → rag-evaluation, vector-database, prompt-engineering
"Fine-tune LLM" → llm-patterns, fine-tuning, evaluation-framework
```

### Frontend Domain

```
Trigger Keywords: "frontend", "UI", "UX", "component", "React", "Vue"

Routing:
Must-Have:
- react-patterns (if React)
- css-patterns
- accessibility

Recommended:
- responsive-design
- performance-engineering
- ux-ui-design

Optional:
- state-management
- animation
- testing

Examples:
"Build React component" → react-patterns, css-patterns, accessibility
"Design user interface" → ux-ui-design, css-patterns, accessibility
"Optimize frontend performance" → performance-engineering, caching-strategies
```

### Backend Domain

```
Trigger Keywords: "backend", "API", "server", "service", "microservice"

Routing:
Must-Have:
- api-design
- error-handling
- security

Recommended:
- authentication
- rate-limiting
- caching

Optional:
- graphql
- websockets
- message-queue

Examples:
"Build REST API" → api-design, error-handling, security, authentication
"Create microservice" → microservices, api-design, monitoring
"Implement authentication" → authentication-jwt, security, api-design
```

### Data Domain

```
Trigger Keywords: "data", "ETL", "pipeline", "analytics", "database"

Routing:
Must-Have:
- data-pipeline
- data-quality
- sql-for-analytics

Recommended:
- data-visualization
- caching-strategies
- data-retention

Optional:
- data-engineering
- data-science
- ml-serving

Examples:
"Build data pipeline" → data-pipeline, data-quality, etl-patterns
"Create analytics dashboard" → data-visualization, sql-for-analytics, dashboard-design
"Optimize database queries" → db-query-optimization, performance-engineering, caching
```

---

## Technology Routing

Map technology keywords to skill categories.

### TypeScript Routing

```
Trigger Keywords: "TypeScript", "TS"

Routing:
Must-Have:
- typescript-standards
- lint-format-typecheck

Recommended:
- react-patterns (if React)
- nodejs-best-practices (if Node.js)

Optional:
- type-definitions
- generic-types

Examples:
"Build TypeScript API" → typescript-standards, lint-format-typecheck, nodejs-best-practices
"Create TypeScript component" → typescript-standards, react-patterns, lint-format-typecheck
```

### Python Routing

```
Trigger Keywords: "Python", "FastAPI", "Django"

Routing:
Must-Have:
- python-best-practices

Recommended:
- fastapi-patterns (if FastAPI)
- data-pipeline (if data work)

Optional:
- async-patterns
- type-hints

Examples:
"Build Python API" → python-best-practices, fastapi-patterns, api-design
"Create data pipeline" → python-best-practices, data-pipeline, data-quality
```

### React Routing

```
Trigger Keywords: "React", "Next.js", "component"

Routing:
Must-Have:
- react-patterns
- css-patterns

Recommended:
- accessibility
- performance-engineering
- testing

Optional:
- state-management
- hooks-patterns
- animation

Examples:
"Build React component" → react-patterns, css-patterns, accessibility
"Create Next.js app" → react-patterns, nextjs-patterns, seo-optimization
```

### PostgreSQL Routing

```
Trigger Keywords: "PostgreSQL", "Postgres", "database", "DB"

Routing:
Must-Have:
- db-query-optimization
- sql-for-analytics

Recommended:
- database-health-monitoring
- data-quality

Optional:
- schema-management
- data-migration

Examples:
"Optimize PostgreSQL queries" → db-query-optimization, sql-for-analytics, performance-engineering
"Design database schema" → database-design, sql-for-analytics, data-quality
```

---

## Phase Routing

Map project phase to skill categories.

### Planning Phase

```
Trigger: "Plan", "design", "requirements", "scope"

Routing:
Must-Have:
- discovery-questions
- requirement-to-scope
- acceptance-criteria

Recommended:
- constraints-and-assumptions
- risk-and-dependencies
- estimation

Optional:
- architecture-decision
- investment-estimation

Examples:
"Plan new feature" → discovery-questions, requirement-to-scope, acceptance-criteria
"Design system architecture" → architecture-decision, system-thinking, trade-off-analysis
```

### Development Phase

```
Trigger: "Implement", "build", "create", "develop"

Routing:
Must-Have:
- code-quality
- testing
- git-workflow

Recommended:
- error-handling
- security
- documentation

Optional:
- refactoring
- performance-engineering

Examples:
"Implement user authentication" → authentication-jwt, security, testing, error-handling
"Build API endpoint" → api-design, error-handling, testing, code-quality
```

### Deployment Phase

```
Trigger: "Deploy", "release", "launch"

Routing:
Must-Have:
- ci-cd
- deployment-strategies
- monitoring

Recommended:
- incident-management
- rollback-strategies
- health-checks

Optional:
- canary-deployment
- blue-green-deployment

Examples:
"Deploy to production" → ci-cd, deployment-strategies, monitoring, incident-management
"Release new version" → ci-cd, deployment-strategies, release-workflow
```

### Maintenance Phase

```
Trigger: "Fix", "optimize", "debug", "maintain"

Routing:
Must-Have:
- debugging
- testing

Recommended:
- performance-engineering
- refactoring
- error-handling

Optional:
- profiling
- code-review-standards

Examples:
"Fix production bug" → debugging, testing, incident-management, error-handling
"Optimize slow queries" → db-query-optimization, performance-engineering, profiling
```

---

## Keyword-Based Routing

Map specific keywords to skills.

### Authentication Keywords

```
Trigger Keywords: "authentication", "auth", "login", "signup", "password"

Routing:
Must-Have:
- authentication-jwt
- security

Recommended:
- api-design (if API)
- database-design (if storing users)

Optional:
- oauth
- sso-saml-oidc
- 2fa

Examples:
"Implement user authentication" → authentication-jwt, security, api-design, database-design
"Add OAuth login" → oauth, sso-saml-oidc, authentication-jwt, security
```

### Payment Keywords

```
Trigger Keywords: "payment", "checkout", "billing", "subscription", "Stripe"

Routing:
Must-Have:
- security
- pci-dss (if card payments)

Recommended:
- api-design
- error-handling
- transaction-auditing

Optional:
- stripe-integration
- billing-subscription
- payment-security

Examples:
"Implement payment processing" → security, pci-dss, api-design, error-handling
"Add subscription billing" → billing-subscription, payment-security, api-design
```

### Search Keywords

```
Trigger Keywords: "search", "filter", "query", "Elasticsearch"

Routing:
Must-Have:
- db-query-optimization
- performance-engineering

Recommended:
- caching-strategies
- data-quality

Optional:
- elasticsearch
- full-text-search
- search-optimization

Examples:
"Implement product search" → db-query-optimization, performance-engineering, caching-strategies
"Add Elasticsearch integration" → elasticsearch, db-query-optimization, performance-engineering
```

### Email Keywords

```
Trigger Keywords: "email", "notification", "SendGrid", "newsletter"

Routing:
Must-Have:
- email-sending
- data-quality (validate email addresses)

Recommended:
- deliverability-optimization
- email-templates

Optional:
- marketing-integration
- newsletter-management

Examples:
"Send welcome emails" → email-sending, email-templates, deliverability-optimization
"Implement email notifications" → email-sending, email-templates, data-quality
```

---

## Pattern-Based Routing

Map common patterns to skills.

### Create Resource API Pattern

```
Pattern: "Create [resource] API"

Routing:
Must-Have:
- api-design
- database-design
- error-handling

Recommended:
- authentication
- authorization
- rate-limiting

Optional:
- openapi-governance
- caching
- versioning

Examples:
"Create user API" → api-design, database-design, error-handling, authentication
"Create product API" → api-design, database-design, error-handling, caching
```

### Implement Feature for Platform Pattern

```
Pattern: "Implement [feature] for [platform]"

Routing:
Must-Have:
- [platform]-patterns
- testing
- code-quality

Recommended:
- accessibility (if web/mobile)
- performance-engineering
- error-handling

Optional:
- platform-specific skills

Examples:
"Implement search for mobile app" → mobile-development, mobile-ci-cd, offline-mode
"Implement dashboard for web" → react-patterns, data-visualization, accessibility
```

### Optimize Metric Pattern

```
Pattern: "Optimize [metric]"

Routing:
Must-Have:
- performance-engineering
- profiling

Recommended:
- caching-strategies
- db-query-optimization (if database)

Optional:
- sla-slo-slis
- cost-engineering

Examples:
"Optimize page load time" → performance-engineering, profiling, caching-strategies
"Optimize API latency" → performance-engineering, profiling, db-query-optimization
```

---

## Hierarchical Routing

Multi-level routing for comprehensive coverage.

### Level 1: Universal (Always)

```
Always Include:
- system-thinking
- trade-off-analysis
- risk-assessment
- security-considerations
- error-handling
```

### Level 2: Domain (Based on Area)

```
AI Domain:
- rag-evaluation
- llm-patterns
- prompt-engineering

Frontend Domain:
- react-patterns
- css-patterns
- accessibility

Backend Domain:
- api-design
- error-handling
- security

Data Domain:
- data-pipeline
- data-quality
- sql-for-analytics
```

### Level 3: Specific (Based on Tech/Feature)

```
React + TypeScript:
- react-patterns
- typescript-standards
- lint-format-typecheck

PostgreSQL + Performance:
- db-query-optimization
- performance-engineering
- caching-strategies

Authentication + Security:
- authentication-jwt
- security
- oauth
```

---

## Multi-Skill Routing

Complex tasks need multiple skill categories.

### Example: AI Chatbot

```
Task: "Build AI chatbot for customer support"

Routing Analysis:
- Task Type: Create → Design + development
- Domain: AI → ML, RAG, LLM
- Technology: Python + React → Python + React skills
- Phase: Development → Coding + testing

Skills Selected:
Must-Have:
- rag-evaluation
- llm-patterns
- prompt-engineering
- api-design (backend)
- react-patterns (frontend)

Recommended:
- safety-guardrails
- cost-optimization
- monitoring
- authentication
- error-handling

Optional:
- multi-agent
- function-calling
- caching
```

### Example: E-Commerce Platform

```
Task: "Build e-commerce platform"

Routing Analysis:
- Task Type: Create → Design + development
- Domain: E-commerce → Payment, cart
- Technology: React + Node.js + PostgreSQL
- Phase: Development → Coding + testing

Skills Selected:
Must-Have:
- shopping-cart (cart handling)
- payment-security (PCI-DSS)
- api-design
- database-design
- react-patterns
- authentication

Recommended:
- caching-strategies
- error-handling
- security
- monitoring
- testing

Optional:
- product-recommendations
- wishlist
- reviews
```

---

## Conditional Routing

Adjust skills based on context.

### Production Routing

```
Condition: "production" or "prod"

Additional Skills:
- monitoring
- incident-management
- postmortem-analysis
- security-audit
- performance-engineering

Example:
"Deploy API to production"
→ ci-cd, deployment-strategies, monitoring, incident-management, security-audit
```

### MVP Routing

```
Condition: "MVP" or "minimum viable product"

Focus: Core functionality only
Defer: Nice-to-haves

Example:
"Build MVP for e-commerce"
→ shopping-cart, payment-security, api-design
(Defer: recommendations, wishlist, reviews)
```

### Enterprise Routing

```
Condition: "enterprise" or "B2B"

Additional Skills:
- sso-saml-oidc
- scim-provisioning
- enterprise-rbac-models
- security-questionnaires
- vendor-onboarding

Example:
"Build enterprise dashboard"
→ sso-saml-oidc, enterprise-rbac-models, api-design, authentication
```

---

## Routing Rules Engine

Process for applying routing rules.

### Engine Flow

```
Input:
- Task description
- Context (technology, domain, phase)

Processing:
1. Parse task description for keywords
2. Identify task type
3. Identify domain
4. Identify technology
5. Identify phase
6. Apply hierarchical routing
7. Apply conditional routing
8. Combine and deduplicate skills

Output:
- List of relevant skills (prioritized)
  - Must-have
  - Recommended
  - Optional
```

### Example Processing

```
Input Task: "Build user authentication API for production"

Processing:
1. Keywords: "build", "authentication", "API", "production"
2. Task Type: Create → Design + development
3. Domain: Backend → API, security
4. Technology: API → REST, database
5. Phase: Development → Coding + testing
6. Condition: Production → Monitoring, incident management

Output Skills:
Must-Have:
- api-design
- authentication-jwt
- security
- database-design
- error-handling

Recommended:
- rate-limiting
- monitoring
- testing
- ci-cd

Optional:
- oauth
- sso-saml-oidc
- 2fa
```

---

## Rule Priority

Define priority levels for skills.

### Priority Levels

| Level | Definition | When to Include |
|-------|------------|----------------|
| **Must-Have** | Critical, directly addresses task | Always include |
| **Recommended** | Important, usually helpful | Include unless explicitly excluded |
| **Optional** | Sometimes helpful | Include if relevant |

### Priority Assignment

```
Must-Have Criteria:
- Core to task completion
- Without it, task cannot be done properly
- Directly addresses primary requirement

Recommended Criteria:
- Important for quality
- Best practice
- Usually needed for similar tasks

Optional Criteria:
- Nice to have
- Enhances quality but not required
- Specific edge cases
```

---

## Routing Rule Examples

### Example 1: Create API

```yaml
rules:
  - trigger: "create API"
    skills:
      must:
        - api-design
        - error-handling
        - security
      recommended:
        - authentication
        - rate-limiting
        - openapi-governance
        - testing
      optional:
        - graphql
        - webhooks
        - caching
```

### Example 2: AI Chatbot

```yaml
rules:
  - trigger: "AI chatbot"
    skills:
      must:
        - rag-evaluation
        - llm-patterns
        - prompt-engineering
        - api-design
      recommended:
        - safety-guardrails
        - cost-optimization
        - monitoring
        - authentication
      optional:
        - multi-agent
        - function-calling
        - caching
```

### Example 3: Optimize Performance

```yaml
rules:
  - trigger: "optimize performance"
    skills:
      must:
        - performance-engineering
        - profiling
      recommended:
        - caching-strategies
        - db-query-optimization
        - sla-slo-slis
      optional:
        - cost-engineering
        - autoscaling
```

### Example 4: Deploy to Production

```yaml
rules:
  - trigger: "deploy to production"
    skills:
      must:
        - ci-cd
        - deployment-strategies
        - monitoring
      recommended:
        - incident-management
        - rollback-strategies
        - health-checks
      optional:
        - canary-deployment
        - blue-green-deployment
```

---

## Routing Configuration

Store routing rules in configuration files.

### YAML Configuration

```yaml
# routing-rules.yaml

version: 1.0

baseline_skills:
  - system-thinking
  - trade-off-analysis
  - risk-assessment
  - security-considerations
  - error-handling

task_type_routing:
  create:
    must:
      - code-quality
      - testing
    recommended:
      - documentation
      - git-workflow

  fix:
    must:
      - debugging
      - testing
    recommended:
      - error-handling
      - root-cause-analysis

  optimize:
    must:
      - performance-engineering
      - profiling
    recommended:
      - caching-strategies
      - db-query-optimization

domain_routing:
  ai:
    must:
      - rag-evaluation
      - llm-patterns
    recommended:
      - safety-guardrails
      - cost-optimization

  frontend:
    must:
      - react-patterns
      - css-patterns
    recommended:
      - accessibility
      - performance-engineering

  backend:
    must:
      - api-design
      - error-handling
    recommended:
      - authentication
      - security

technology_routing:
  typescript:
    must:
      - typescript-standards
      - lint-format-typecheck

  react:
    must:
      - react-patterns
    recommended:
      - hooks-patterns
      - state-management

  postgresql:
    must:
      - db-query-optimization
      - sql-for-analytics

conditional_routing:
  production:
    additional:
      - monitoring
      - incident-management
      - security-audit

  mvp:
    focus: core
    defer:
      - nice-to-haves

  enterprise:
    additional:
      - sso-saml-oidc
      - enterprise-rbac-models
      - scim-provisioning
```

### JSON Configuration

```json
{
  "version": "1.0",
  "baseline_skills": [
    "system-thinking",
    "trade-off-analysis",
    "risk-assessment",
    "security-considerations",
    "error-handling"
  ],
  "rules": [
    {
      "trigger": "create API",
      "skills": {
        "must": [
          "api-design",
          "error-handling",
          "security"
        ],
        "recommended": [
          "authentication",
          "rate-limiting",
          "openapi-governance"
        ],
        "optional": [
          "graphql",
          "webhooks",
          "caching"
        ]
      }
    },
    {
      "trigger": "AI chatbot",
      "skills": {
        "must": [
          "rag-evaluation",
          "llm-patterns",
          "prompt-engineering"
        ],
        "recommended": [
          "safety-guardrails",
          "cost-optimization",
          "monitoring"
        ],
        "optional": [
          "multi-agent",
          "function-calling"
        ]
      }
    }
  ]
}
```

---

## Fallback Routing

What to do when no specific match.

### Fallback Strategy

```
1. Use baseline skills
   - Always include universal baseline

2. Apply general task type routing
   - Create → Design + development
   - Fix → Debugging + testing
   - Optimize → Performance + profiling

3. Ask clarifying questions
   - What technology?
   - What domain?
   - What phase?

4. Suggest possible matches
   - Show similar tasks
   - Let user select
```

### Example Fallback

```
Input Task: "Build something"

No specific match → Fallback

Output:
Baseline Skills:
- system-thinking
- trade-off-analysis
- risk-assessment
- security-considerations
- error-handling

Clarification Needed:
- What type of task? (create, fix, optimize, deploy)
- What domain? (AI, frontend, backend, data)
- What technology? (React, Python, PostgreSQL)

Suggested Matches:
- "Build API" → api-design, error-handling, security
- "Build UI component" → react-patterns, css-patterns, accessibility
- "Build data pipeline" → data-pipeline, data-quality, etl-patterns
```

---

## Learning from Usage

Improve routing rules over time.

### Tracking Usage

```
Track:
- Which skills were used
- Which skills were skipped
- Which skills were most helpful
- Which skills were irrelevant

Metrics:
- Skill usage frequency
- Skill relevance score
- Task-skill match accuracy
```

### Refining Rules

```
Process:
1. Analyze usage data
2. Identify patterns
3. Adjust routing rules
4. Test changes
5. Deploy updates

Example:
Data shows "authentication" is always needed for API tasks
→ Add "authentication" to recommended skills for "create API" rule
```

### Adding New Patterns

```
Process:
1. Identify new pattern from usage
2. Create routing rule
3. Test with sample tasks
4. Deploy to production

Example:
Pattern: "Implement OAuth"
→ Create rule: "oauth" → oauth, sso-saml-oidc, authentication-jwt
```

---

## Real-World Routing Examples

### Example 1: Web App Feature Request

```
Task: "Add user profile page to web app"

Routing Analysis:
- Task Type: Create → Design + development
- Domain: Frontend → React, CSS
- Technology: React + TypeScript
- Phase: Development → Coding + testing

Skills Selected:
Must-Have:
- react-patterns
- typescript-standards
- css-patterns
- accessibility

Recommended:
- testing
- error-handling
- performance-engineering
- lint-format-typecheck

Optional:
- state-management
- animation
```

### Example 2: Performance Issue

```
Task: "Fix slow page load time"

Routing Analysis:
- Task Type: Fix + Optimize → Debugging + performance
- Domain: Frontend → Performance
- Technology: Web
- Phase: Maintenance → Debugging + optimization

Skills Selected:
Must-Have:
- debugging
- performance-engineering
- profiling

Recommended:
- caching-strategies
- performance-engineering
- db-query-optimization (if database)

Optional:
- cost-engineering
- sla-slo-slis
```

### Example 3: Security Incident

```
Task: "Investigate and fix security vulnerability"

Routing Analysis:
- Task Type: Fix → Debugging + security
- Domain: Security → Security practices
- Technology: N/A (general)
- Phase: Maintenance → Debugging + fixing

Skills Selected:
Must-Have:
- debugging
- security-practices
- penetration-testing

Recommended:
- security-audit
- incident-management
- error-handling

Optional:
- vulnerability-management
- owasp-top-10
```

---

## Templates

### Routing Rule Template

```yaml
# Routing Rule: [Rule Name]

trigger: "[trigger phrase]"

skills:
  must:
    - [skill-1]
    - [skill-2]

  recommended:
    - [skill-3]
    - [skill-4]

  optional:
    - [skill-5]
    - [skill-6]

# Documentation
# Why these skills for this trigger:
# [Explanation]

# Examples:
# - [Example 1]
# - [Example 2]
```

### Routing Configuration Template

```yaml
# Routing Configuration

version: 1.0
last_updated: [Date]

baseline_skills:
  - system-thinking
  - trade-off-analysis
  - risk-assessment
  - security-considerations
  - error-handling

# Task Type Routing
task_type_routing:
  create:
    must:
      - code-quality
      - testing
    recommended:
      - documentation
      - git-workflow

  fix:
    must:
      - debugging
      - testing
    recommended:
      - error-handling

  optimize:
    must:
      - performance-engineering
      - profiling
    recommended:
      - caching-strategies

  deploy:
    must:
      - ci-cd
      - deployment-strategies
    recommended:
      - monitoring
      - incident-management

# Domain Routing
domain_routing:
  ai:
    must:
      - rag-evaluation
      - llm-patterns
    recommended:
      - safety-guardrails

  frontend:
    must:
      - react-patterns
      - css-patterns
    recommended:
      - accessibility

  backend:
    must:
      - api-design
      - error-handling
    recommended:
      - authentication
      - security

  data:
    must:
      - data-pipeline
      - data-quality
    recommended:
      - sql-for-analytics

# Technology Routing
technology_routing:
  typescript:
    must:
      - typescript-standards
      - lint-format-typecheck

  react:
    must:
      - react-patterns
    recommended:
      - hooks-patterns

  postgresql:
    must:
      - db-query-optimization
      - sql-for-analytics

# Conditional Routing
conditional_routing:
  production:
    additional:
      - monitoring
      - incident-management

  mvp:
    focus: core
    defer:
      - nice-to-haves

  enterprise:
    additional:
      - sso-saml-oidc
      - enterprise-rbac-models
```

---

## Best Practices

1. **Start with baseline** - Always include universal baseline skills
2. **Be specific** - Clear trigger phrases for accurate routing
3. **Document rules** - Explain why skills are selected
4. **Test rules** - Verify rules produce expected results
5. **Version control** - Track changes to routing rules
6. **Review regularly** - Update rules based on usage patterns
7. **Use hierarchies** - Universal → Domain → Specific
8. **Handle edge cases** - Fallback for unclear tasks
9. **Learn from data** - Improve rules based on usage
10. **Keep it simple** - Don't over-engineer routing logic

---

## Related Skills

- [Baseline Policy](../baseline-policy/SKILL.md) - Universal baseline skills
- [Scoring and Prioritization](../scoring-and-prioritization/SKILL.md) - Prioritize routed skills
- [Output Templates](../output-templates/SKILL.md) - Document selected skills
