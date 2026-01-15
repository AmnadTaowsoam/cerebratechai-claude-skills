---
name: Tech Stack Selection
description: Systematic approach to choosing technologies, frameworks, and tools based on requirements, team capabilities, and long-term sustainability.
---

# Tech Stack Selection

## Overview

Tech Stack Selection is the process of choosing programming languages, frameworks, databases, and tools that will form the foundation of your system. Good choices enable productivity; poor choices create years of technical debt.

**Core Principle**: "Choose boring technology. Optimize for team productivity and long-term maintainability, not resume-driven development."

---

## 1. Selection Criteria Framework

### Primary Criteria
| Criterion | Questions to Ask |
|-----------|------------------|
| **Problem Fit** | Does this technology solve our specific problem well? |
| **Team Expertise** | Can our team learn and use this effectively? |
| **Community & Support** | Is there an active community? Good documentation? |
| **Maturity** | Is it production-ready or still experimental? |
| **Ecosystem** | Are there libraries/tools we need? |
| **Performance** | Does it meet our performance requirements? |
| **Cost** | Licensing, hosting, training costs? |
| **Hiring** | Can we hire developers with this skill? |
| **Long-term Viability** | Will it be maintained in 5 years? |

---

## 2. The "Boring Technology" Rule

```markdown
## Dan McKinley's "Choose Boring Technology"

**Rule**: You have ~3 "innovation tokens" per project. Spend them wisely.

### Example: E-commerce Startup

**Boring (Safe) Choices**:
- ✅ PostgreSQL (database) - Proven, reliable
- ✅ React (frontend) - Widely adopted, stable
- ✅ Node.js (backend) - Team knows it well

**Innovation Tokens Spent**:
- 🎫 Token 1: Kubernetes (new to team, but needed for scaling)
- 🎫 Token 2: GraphQL (better than REST for our use case)
- 🎫 Token 3: [Reserved for future needs]

**Avoided**:
- ❌ Rust backend (team doesn't know it)
- ❌ CockroachDB (PostgreSQL works fine)
- ❌ Svelte (React is good enough)
```

---

## 3. Technology Evaluation Matrix

```markdown
## Example: Choosing a Frontend Framework

| Criteria | React | Vue | Svelte | Weight | Winner |
|----------|-------|-----|--------|--------|--------|
| **Team Expertise** | 5/5 (everyone knows) | 2/5 (1 person) | 1/5 (nobody) | 30% | React |
| **Ecosystem** | 5/5 (huge) | 4/5 (good) | 3/5 (growing) | 20% | React |
| **Performance** | 4/5 | 4/5 | 5/5 (fastest) | 15% | Svelte |
| **Hiring** | 5/5 (easy) | 4/5 | 2/5 (harder) | 15% | React |
| **Documentation** | 5/5 | 5/5 | 4/5 | 10% | React/Vue |
| **Bundle Size** | 3/5 | 4/5 | 5/5 (smallest) | 10% | Svelte |

**Weighted Score**:
- React: 4.5/5
- Vue: 3.6/5
- Svelte: 3.2/5

**Decision**: React (best fit for team and ecosystem)
```

---

## 4. Database Selection Guide

### Relational (SQL)
```markdown
**Choose PostgreSQL when**:
- Complex relationships between entities
- ACID transactions required
- Strong consistency needed
- Rich query capabilities (JOINs, CTEs)

**Examples**: E-commerce, Banking, ERP

**Choose MySQL when**:
- Read-heavy workloads
- Simpler data model
- Need master-slave replication

**Examples**: Content sites, Blogs
```

### NoSQL
```markdown
**Choose MongoDB when**:
- Flexible schema needed
- Document-oriented data
- Rapid prototyping

**Examples**: Content management, Catalogs

**Choose Redis when**:
- Caching layer
- Session storage
- Real-time features (pub/sub)

**Examples**: Cache, Leaderboards, Rate limiting

**Choose Cassandra when**:
- Massive write throughput
- Multi-datacenter replication
- Time-series data

**Examples**: IoT, Analytics, Logs
```

---

## 5. Language Selection

### Backend Language Decision Tree
```
Do you need maximum performance?
├─ YES → Go, Rust
└─ NO → Continue

Do you have a large existing codebase?
├─ YES → Stick with current language
└─ NO → Continue

What's your team's expertise?
├─ JavaScript → Node.js/TypeScript
├─ Python → Python (Django/FastAPI)
├─ Java → Java/Kotlin (Spring Boot)
└─ None → TypeScript (easiest to hire)

Special requirements?
├─ ML/Data Science → Python
├─ Real-time/Gaming → Go, Rust
├─ Enterprise → Java
└─ Startups → TypeScript, Python
```

---

## 6. Framework Selection

### Backend Framework
```typescript
// Example: Node.js Framework Selection

// Express - Minimalist, flexible
app.get('/users', (req, res) => {
  // Manual validation, error handling
});

// Fastify - Performance-focused
fastify.get('/users', {
  schema: { /* validation */ }
}, async (req, reply) => {
  // Built-in validation, serialization
});

// NestJS - Enterprise, opinionated
@Controller('users')
export class UsersController {
  @Get()
  findAll(): Promise<User[]> {
    // Dependency injection, decorators
  }
}

// Decision: 
// - Express: Small projects, maximum flexibility
// - Fastify: Performance-critical APIs
// - NestJS: Large teams, enterprise apps
```

---

## 7. Cloud Provider Selection

```markdown
## Cloud Provider Comparison

| Feature | AWS | GCP | Azure |
|---------|-----|-----|-------|
| **Market Leader** | ✅ Yes | ❌ No | ❌ No |
| **Best for ML** | ❌ No | ✅ Yes (TensorFlow) | ❌ No |
| **Best for .NET** | ❌ No | ❌ No | ✅ Yes |
| **Pricing** | Complex | Simpler | Complex |
| **Enterprise Support** | ✅ Excellent | ✅ Good | ✅ Excellent |
| **Kubernetes** | EKS | GKE (best) | AKS |

**Decision Factors**:
- Existing contracts/credits
- Team expertise
- Specific service needs (e.g., BigQuery on GCP)
- Geographic requirements
```

---

## 8. Proof of Concept (POC)

```markdown
## POC Template for Technology Evaluation

### Objective
Evaluate [Technology X] for [Use Case]

### Success Criteria
- [ ] Can handle 10K requests/second
- [ ] Team can build basic CRUD in 1 day
- [ ] Integrates with existing auth system
- [ ] Deployment to staging works

### Timeline
- Day 1-2: Setup and basic implementation
- Day 3: Performance testing
- Day 4: Integration testing
- Day 5: Team review and decision

### Deliverables
- Working prototype
- Performance benchmarks
- Integration documentation
- Recommendation (Go/No-Go)
```

---

## 9. Technology Radar

```markdown
## Company Technology Radar (ThoughtWorks Style)

### Adopt (Use for new projects)
- PostgreSQL
- TypeScript
- React
- Docker
- GitHub Actions

### Trial (Experiment in non-critical projects)
- Bun (JavaScript runtime)
- Turso (Edge database)
- Astro (Static site generator)

### Assess (Keep watching)
- Deno 2.0
- HTMX
- Rust for backend

### Hold (Don't use for new projects)
- jQuery
- AngularJS
- MongoDB (for transactional data)
```

---

## 10. Common Selection Mistakes

### Anti-patterns
```markdown
❌ **Resume-Driven Development**
"Let's use Rust because it's cool"
→ Team doesn't know Rust, project delayed 6 months

❌ **Hype-Driven Development**
"Everyone's using NoSQL, let's use MongoDB"
→ Needed ACID transactions, had to migrate to PostgreSQL

❌ **Not-Invented-Here Syndrome**
"Let's build our own auth system"
→ Security vulnerabilities, 6 months wasted

❌ **Analysis Paralysis**
"Let's evaluate 10 more frameworks"
→ Never ship, competitors win

✅ **Better Approach**
- Use what team knows
- Choose proven technologies
- Validate with small POC
- Ship and iterate
```

---

## 11. Technology Selection Checklist

- [ ] **Requirements Clear**: What problem are we solving?
- [ ] **Team Expertise**: Can team learn this in reasonable time?
- [ ] **POC Completed**: Have we validated it works for our use case?
- [ ] **Ecosystem Evaluated**: Are there libraries/tools we need?
- [ ] **Performance Tested**: Meets our performance requirements?
- [ ] **Cost Analyzed**: Total cost of ownership acceptable?
- [ ] **Hiring Considered**: Can we hire developers with this skill?
- [ ] **Long-term Plan**: What's the 3-5 year outlook?
- [ ] **Exit Strategy**: Can we migrate away if needed?
- [ ] **Documented**: Decision recorded in ADR?

---

## 12. Tech Stack Decision Template

```markdown
# Tech Stack Decision: [Component Name]

## Context
We need to choose a [database/framework/language] for [use case].

## Requirements
- Performance: [specific metrics]
- Scale: [expected load]
- Team: [current expertise]
- Budget: [constraints]

## Options Evaluated

### Option 1: [Technology A]
**Pros**: [list]
**Cons**: [list]
**POC Results**: [link to POC]
**Score**: 7/10

### Option 2: [Technology B]
**Pros**: [list]
**Cons**: [list]
**POC Results**: [link to POC]
**Score**: 8/10

## Decision
We chose [Technology B] because [rationale].

## Mitigations
To address the cons:
- [Mitigation 1]
- [Mitigation 2]

## Next Steps
- [ ] Setup development environment
- [ ] Train team
- [ ] Update documentation
```

---

## Related Skills
* `59-architecture-decision/adr-templates`
* `59-architecture-decision/tradeoff-analysis`
* `59-architecture-decision/architecture-review`
