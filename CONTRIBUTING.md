# Contributing to CerebraTechAI Claude Skills

First off, thank you for considering contributing to Cerebrate Chai Claude Skills! 🎉

It's people like you that make this repository a great resource for the Claude AI community.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Skill Guidelines](#skill-guidelines)
- [Style Guide](#style-guide)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)

---

## 🤝 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

### Our Pledge

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the community
- Show empathy towards other community members

---

## 💡 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce**
- **Expected vs actual behavior**
- **Screenshots** (if applicable)
- **Environment details** (OS, Claude version, etc.)

**Use this template:**
````markdown
## Bug Description
[Clear description of the bug]

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Environment
- OS: [e.g., macOS 14.0]
- Claude Version: [e.g., Desktop 0.7.0]
- Skill: [e.g., nextjs-patterns]
````

### Suggesting Skills

We love new skill ideas! Before suggesting:

1. **Check existing skills** - Maybe it already exists
2. **Search issues** - Someone might have suggested it
3. **Consider scope** - Is it broad enough to be useful?

**Use this template:**
````markdown
## Skill Name
[Proposed skill name]

## Category
[Which batch/category does this belong to?]

## Description
[Brief description of what this skill should cover]

## Why This Skill is Needed
[Explain the use case and importance]

## Proposed Content Outline
1. Section 1
2. Section 2
3. ...

## Related Skills
[List any related skills that exist]

## Target Audience
[Who will use this skill?]
````

### Improving Documentation

Documentation improvements are always welcome:

- Fix typos or grammatical errors
- Clarify confusing sections
- Add missing examples
- Update outdated information
- Improve code examples

### Contributing New Skills

This is the most valuable contribution! Follow these steps:

1. **Fork the repository**
2. **Create a branch** (`git checkout -b skill/your-skill-name`)
3. **Write the skill** (follow guidelines below)
4. **Test thoroughly** - Verify all code examples work
5. **Update README.md** - Add your skill to the appropriate category
6. **Commit your changes** (follow commit guidelines)
7. **Push to your fork** (`git push origin skill/your-skill-name`)
8. **Open a Pull Request**

---

## 📚 Skill Guidelines

### Skill Structure

Every skill MUST follow this structure (use `templates/skill-template.md`):
````markdown
---
name: <Human-readable skill name>
description: <1 sentence: what it covers + when to use it>
---

# [Skill Name]

## Overview
[2-3 sentences explaining what this skill covers and when to use it]

## Why This Matters
- **Benefit**: Short explanation

## Core Concepts
### 1. Concept
[Rules, patterns, examples]

## Quick Start
[Minimal steps + small runnable example if helpful]

## Production Checklist
- [ ] Item 1
- [ ] Item 2

## Anti-patterns
1. **Anti-pattern**: Why it’s bad

## Integration Points
- Related tools/processes/skills

## Further Reading
- Links

Format: Markdown with [Language] code examples.

Create the file now.
````

### Required Sections

Every skill MUST include:

1. ✅ **YAML frontmatter** (`name`, `description`)
2. ✅ **Overview** - Brief introduction (2-4 sentences)
3. ✅ **Core Concepts** - The actual guidance/patterns
4. ✅ **Quick Start** - Minimal “do this first” flow
5. ✅ **Production Checklist** - Operational checklist
6. ✅ **Anti-patterns** - Things to avoid

### Optional Sections (but recommended)

- **When to Use** - Specific use cases
- **When NOT to Use** - Situations to avoid this pattern
- **Performance Considerations**
- **Security Considerations**
- **Testing Strategies**
- **Troubleshooting**
- **Real-World Examples**
- **Tools and Libraries**

### Code Examples Requirements

All code examples MUST:

- ✅ Be **production-ready** (not just demos)
- ✅ Include **error handling**
- ✅ Follow **best practices**
- ✅ Include **type annotations** (TypeScript/Python)
- ✅ Be **tested** and working
- ✅ Include **comments** explaining key parts
- ✅ Show **both good and bad patterns** (❌ Bad vs ✅ Good)

**Example Format:**
````markdown
### Good vs Bad Examples
```typescript
// ❌ Bad - No error handling, poor naming
async function getData(id) {
  const data = await fetch(`/api/users/${id}`);
  return data.json();
}

// ✅ Good - Proper error handling, type safety
async function getUserById(userId: string): Promise<User> {
  try {
    const response = await fetch(`/api/users/${userId}`);
    
    if (!response.ok) {
      throw new Error(`Failed to fetch user: ${response.statusText}`);
    }
    
    const user: User = await response.json();
    return user;
  } catch (error) {
    logger.error('Error fetching user', { userId, error });
    throw new AppError('USER_FETCH_FAILED', error);
  }
}
```
````

### Language-Specific Guidelines

#### TypeScript
- Use `strict: true` in examples
- Include explicit return types
- Use modern ES2022+ syntax
- Prefer `async/await` over promises
- Use `interface` for object shapes, `type` for unions

#### Python
- Use Python 3.11+ features
- Include type hints (from `typing`)
- Follow PEP 8
- Use `async/await` where appropriate
- Prefer f-strings over `.format()`

#### SQL
- Use uppercase for SQL keywords
- Include indexes
- Show both Prisma and raw SQL where applicable

---

## 🏢 Enterprise Skill Guidelines (Skills 73-164)

Skills 73-164 เป็นส่วนของ Enterprise Architecture Capability Roadmap และต้องมีโครงสร้างเพิ่มเติมจาก Standard Skill

### Enhanced Structure for Enterprise Skills

````markdown
---
name: <Human-readable skill name>
description: <1 sentence: what it covers + when to use it>
skill-id: <73-164>
domain: <IoT / AI / Business Strategy / Security>
level: Expert (Enterprise Scale)
---

# [Skill Name]

## Overview
[2-3 sentences]

## Why This Matters / Strategic Necessity
- **Context:** เหตุผลความจำเป็นในโลกปี 2025-2026
- **Business Impact:** ผลกระทบต่อธุรกิจ
- **Product Thinking:** ทักษะนี้ช่วยแก้ปัญหาอะไร

## Core Concepts / Technical Deep Dive
[In-depth technical content]

## Tooling & Tech Stack
- **Enterprise Tools:** เครื่องมือระดับ Production
- **Configuration Essentials:** Best practices

## Standards, Compliance & Security
- **Standards:** ISO, NIST, etc.
- **Security:** Security considerations

## Unit Economics & KPIs (for Business skills 126+)
- **Cost Calculation:** สูตรการคำนวณต้นทุน
- **KPIs:** ตัวชี้วัดความสำเร็จ

## Quick Start
[Minimal steps]

## Production Checklist
- [ ] Checklist items

## Anti-patterns
[Things to avoid]

## Integration Points
[Related skills]

## Further Reading
[Resources]
````

### Domain-Specific Requirements

#### IoT Skills (73-90)
- Include hardware considerations (memory, power, connectivity)
- Reference platforms: AWS IoT Core, Azure IoT Hub, Mender.io
- Show OTA update patterns with rollback strategies
- Include security best practices (Zero Trust)

#### AI/ML Production Skills (91-125)
- Include cost considerations (GPU, inference costs)
- Show monitoring patterns (drift detection, model health)
- Include model versioning and lineage tracking
- Address bias and fairness where applicable

#### Business Skills (126-157)
- Connect technical concepts to business outcomes
- Include financial calculations with formulas
- Reference standards: ASC 606, GDPR, ESG
- Show metrics dashboards and KPIs

#### Future-Ready Skills (158-164)
- Explain why preparation is important NOW
- Include emerging standards and specifications
- Show concrete preparation steps
- Include timeline and adoption curve

### Code Example Requirements for Enterprise Skills

Enterprise skill code examples MUST include:

1. **Error Handling & Resilience**
   - Retry logic with exponential backoff
   - Circuit breaker patterns
   - Graceful degradation

2. **Observability**
   - Structured logging
   - Metrics emission
   - Tracing context

3. **Security**
   - Input validation
   - Authentication checks
   - Secure credential handling

4. **Cost Awareness** (comments about resource usage)

Example:
````python
# ❌ Bad - No error handling, no observability
def process_data(data):
    result = external_api.call(data)
    return result

# ✅ Good - Production-ready with all considerations
@retry(max_attempts=3, backoff=exponential(base=2))
@trace("process_data")
def process_data(data: DataInput) -> ProcessedResult:
    """
    Process data with external API.
    
    Cost: ~$0.001 per call (external API charges)
    Latency: p50=100ms, p99=500ms
    """
    # Validate input
    validated = validate_input(data)
    
    # Track metrics
    metrics.increment("process_data.calls")
    
    try:
        with Timer() as t:
            result = external_api.call(validated)
        
        metrics.histogram("process_data.latency", t.elapsed)
        logger.info("Processed data", extra={"duration": t.elapsed})
        
        return ProcessedResult(result)
        
    except APIError as e:
        metrics.increment("process_data.errors", tags={"error": e.code})
        logger.error("API call failed", exc_info=True)
        raise
````

---

## 🎨 Style Guide

### Markdown Formatting
````markdown
# Main Title (H1) - Only once per file

## Section (H2) - Main sections

### Subsection (H3) - Sub-topics

#### Detail (H4) - Specific details

**Bold** for emphasis
*Italic* for terms
`code` for inline code
````

### Emoji Usage

Use emojis **sparingly** and **consistently**:

- ✅ For "Good" examples
- ❌ For "Bad" examples
- 🔥 For critical/important points
- 💡 For tips
- ⚠️ For warnings
- 📝 For notes

**Don't** use emojis in code examples or section headers (except main title).

### Code Block Formatting

Always specify language:
````markdown
```typescript
// TypeScript code here
```
```python
# Python code here
```
```sql
-- SQL code here
```
```bash
# Shell commands here
```
````

### Link Formatting

Use relative links for internal references:
````markdown
See [TypeScript Standards](../01-foundations/typescript-standards/SKILL.md)
````

Use full URLs for external references:
````markdown
Learn more at [Next.js Docs](https://nextjs.org/docs)
````

---

## 📝 Commit Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/):

### Commit Message Format
````
<type>(<scope>): <subject>

<body>

<footer>
````

### Types

- **feat**: New skill or major feature
- **fix**: Bug fix or correction
- **docs**: Documentation changes
- **style**: Formatting, missing semicolons, etc.
- **refactor**: Code refactoring
- **test**: Adding tests
- **chore**: Maintenance tasks

### Scope

Use the skill name or category:

- `typescript-standards`
- `nextjs-patterns`
- `batch-06` (for batch-wide changes)
- `readme` (for README changes)

### Examples
````bash
# Adding a new skill
feat(nextjs-patterns): add server actions examples

# Fixing an error in existing skill
fix(prisma-guide): correct transaction syntax

# Updating documentation
docs(readme): add installation instructions

# Refactoring code examples
refactor(jwt-authentication): simplify token generation example
````

### Subject Line Rules

- Use imperative mood ("add" not "added")
- Don't capitalize first letter
- No period at the end
- Maximum 72 characters

---

## 🔄 Pull Request Process

### Before Submitting

1. ✅ **Test all code examples** - Make sure they work
2. ✅ **Run spell check** - Use a spell checker
3. ✅ **Update README.md** - Add your skill to the index
4. ✅ **Update CHANGELOG.md** - Document your changes
5. ✅ **Self-review** - Read through your changes
6. ✅ **Check links** - Ensure all links work

### PR Title Format

Follow commit message format:
````
feat(skill-name): add comprehensive guide
````

### PR Description Template
````markdown
## Description
[Describe what this PR does]

## Type of Change
- [ ] New skill
- [ ] Bug fix
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Other (please describe)

## Skill Details (if applicable)
- **Category**: [e.g., Backend API]
- **Skill Name**: [e.g., GraphQL Patterns]
- **Related Skills**: [List related skills]

## Checklist
- [ ] Code examples are tested and working
- [ ] All code follows style guidelines
- [ ] Documentation is clear and complete
- [ ] README.md is updated
- [ ] No typos or grammatical errors
- [ ] All links are working
- [ ] Commit messages follow guidelines

## Testing
[Describe how you tested the code examples]

## Screenshots (if applicable)
[Add screenshots if relevant]

## Additional Notes
[Any additional information]
````

### Review Process

1. **Automated Checks** - CI will run automatically
2. **Maintainer Review** - A maintainer will review within 3-5 days
3. **Address Feedback** - Make requested changes
4. **Approval** - Once approved, PR will be merged
5. **Celebration** - 🎉 You're now a contributor!

### After Your PR is Merged

- **Star the repo** ⭐ (if you haven't already)
- **Share your contribution** 📢
- **Look for more issues** to contribute to

---

## 🏆 Recognition

Contributors will be:

- Listed in our [CONTRIBUTORS.md](CONTRIBUTORS.md)
- Mentioned in release notes
- Featured on our website (with permission)

---

## 🐛 Issue Labels

We use these labels to organize issues:

- `good first issue` - Great for newcomers
- `help wanted` - Need community help
- `skill request` - New skill suggestions
- `bug` - Something isn't working
- `documentation` - Documentation improvements
- `enhancement` - New features
- `question` - Questions about usage

---

## 📞 Getting Help

Need help contributing?

- 💬 [GitHub Discussions](https://github.com/AmnadTaowsoam/cerebraSkills/discussions)
- 📧 Email: contribute@cerebratechai.com
- 🐦 Twitter: [@cerebratechai](https://twitter.com/cerebratechai)

---

## 🎓 Learning Resources

New to contributing to open source?

- [First Contributions](https://github.com/firstcontributions/first-contributions)
- [How to Contribute to Open Source](https://opensource.guide/how-to-contribute/)
- [GitHub Skills](https://skills.github.com/)

---

## 🌟 Skill Quality Standards

### Excellent Skills Have:

- ✅ Real-world, production-ready examples
- ✅ Multiple code examples showing different approaches
- ✅ Clear explanation of trade-offs
- ✅ Security considerations
- ✅ Performance tips
- ✅ Testing strategies
- ✅ Links to official documentation
- ✅ At least 3 "Good vs Bad" comparisons
- ✅ Implementation checklist
- ✅ Troubleshooting section

### Avoid:

- ❌ Theoretical concepts without examples
- ❌ Outdated patterns or deprecated syntax
- ❌ Copy-pasted content from other sources
- ❌ Incomplete code examples
- ❌ Missing error handling
- ❌ Untested code
- ❌ Vague or unclear instructions

---

## 📋 Skill Review Checklist

Before submitting, ensure your skill passes this checklist:

### Content Quality
- [ ] Overview is clear and concise (2-3 sentences)
- [ ] All sections are well-organized
- [ ] Content is accurate and up-to-date
- [ ] Explanations are clear and easy to understand
- [ ] No spelling or grammar errors

### Code Examples
- [ ] All code examples are tested and working
- [ ] Code follows language-specific best practices
- [ ] Error handling is included
- [ ] Type annotations are present (TS/Python)
- [ ] Comments explain complex logic
- [ ] At least 3 "Good vs Bad" examples

### Completeness
- [ ] Best practices section included
- [ ] Common pitfalls section included
- [ ] Implementation checklist included
- [ ] Security considerations (if applicable)
- [ ] Performance tips (if applicable)
- [ ] Testing strategies (if applicable)

### Formatting
- [ ] Proper markdown formatting
- [ ] Consistent heading levels
- [ ] Code blocks have language specified
- [ ] Links are working
- [ ] No broken images

### Integration
- [ ] Added to README.md index
- [ ] Placed in correct category folder
- [ ] Follows naming conventions
- [ ] Related skills are cross-referenced

---

## 🎯 Priority Skills

We're particularly looking for contributions in these areas:

### High Priority (Recently Added ✅)
- [x] GraphQL patterns - `03-backend-api/graphql-best-practices`
- [x] gRPC implementation - `03-backend-api/grpc-integration`
- [x] Saga Pattern - `09-microservices/saga-pattern`
- [x] Event Sourcing - `09-microservices/event-sourcing`
- [x] CQRS Pattern - `09-microservices/cqrs-pattern`
- [x] Database Transactions - `04-database/database-transactions`
- [x] Connection Pooling - `04-database/connection-pooling`
- [x] Load Balancing - `15-devops-infrastructure/load-balancing`
- [x] GitHub MCP skills - `60-github-mcp/*`

### Medium Priority (Recently Added ✅)
- [x] Cache Invalidation - `04-database/cache-invalidation`
- [x] Error Boundaries React - `02-frontend/error-boundaries-react`
- [x] State Machines XState - `02-frontend/state-machines-xstate`
- [x] Secrets Management - `24-security-practices/secrets-management`
- [x] Vector Search Patterns - `06-ai-ml-production/vector-search-patterns`
- [x] GitOps ArgoCD - `15-devops-infrastructure/gitops-argocd`
- [x] Contract Testing Pact - `16-testing/contract-testing-pact`
- [x] Multi-Cloud Patterns - `15-devops-infrastructure/multi-cloud-patterns`
- [x] Multi-Step Forms - `02-frontend/multi-step-forms`
- [x] Infinite Scroll - `02-frontend/infinite-scroll`
- [x] Escrow Workflow - `09-microservices/escrow-workflow`
- [x] Service Orchestration - `15-devops-infrastructure/service-orchestration`
- [x] Event-Driven Testing - `16-testing/event-driven-testing`
- [x] QR Code Features - `17-domain-specific/qr-code-features`
- [x] Thai Cultural Events - `17-domain-specific/thai-cultural-events`
- [x] LINE Platform Integration - `20-ai-integration/line-platform-integration`
- [x] Thai UX Patterns - `22-ux-ui-design/thai-ux-patterns`
- [x] Thai Payment Integration - `71-infrastructure-patterns/thai-payment-integration`

### Still Needed (Core Skills)
- [ ] CI/CD with GitLab
- [ ] Monitoring with Datadog
- [ ] Log aggregation with Loki
- [ ] Service mesh (Linkerd)
- [ ] WebAssembly integration
- [ ] Terraform advanced patterns
- [ ] Kubernetes security
- [ ] Database replication

### Language-Specific
- [ ] Go patterns
- [ ] Rust for performance
- [ ] Kotlin for Android
- [ ] Swift for iOS

---

### 🚀 NEW: Enterprise Architecture Skills (73-164)

> **Note:** กำลังรับ contributions สำหรับ Enterprise Skills ใหม่ตาม Enterprise Architecture Capability Roadmap 2025-2026

#### Critical Priority (Enterprise IoT & Cloud)
- [ ] `73-iot-fleet-management/differential-ota-updates` - OTA Delta Updates
- [ ] `74-iot-zero-trust-security/hardware-rooted-identity` - Hardware Root of Trust
- [ ] `74-iot-zero-trust-security/mtls-pki-management` - mTLS & PKI
- [ ] `75-edge-computing/lightweight-kubernetes` - K3s/MicroK8s for Edge

#### Critical Priority (AI & Data Architecture)
- [ ] `77-mlops-data-engineering/feature-store-implementation` - Feature Store (Feast/Tecton)
- [ ] `77-mlops-data-engineering/drift-detection-retraining` - Drift Detection & Auto-retraining
- [ ] `78-inference-model-serving/high-performance-inference` - Triton/TorchServe
- [ ] `80-agentic-ai-advanced-learning/agentic-ai-frameworks` - LangChain/LangGraph Agents

#### High Priority (Business & Product)
- [ ] `81-saas-finops-pricing/cloud-unit-economics` - FinOps & Unit Economics
- [ ] `81-saas-finops-pricing/usage-based-pricing` - Consumption-based Pricing
- [ ] `82-technical-product-management/business-to-technical-spec` - Business to Tech Spec
- [ ] `84-compliance-ai-governance/ai-explainability-ethics` - AI Explainability (SHAP/LIME)

#### Future-Ready Skills (High Priority)
- [ ] `86-sustainable-ai/green-computing-finops` - Sustainable AI & Carbon-aware Computing
- [ ] `87-multi-agent-governance/multi-agent-orchestration` - Multi-Agent Orchestration & HITL
- [ ] `88-ai-supply-chain-security/model-bom-security` - AI SBOM & Supply Chain Security
- [ ] `89-post-quantum-cryptography/pqc-for-iot` - Post-Quantum Cryptography

#### Extended Enterprise Skills (Medium Priority)
- [ ] `77-mlops-data-engineering/data-pipeline-orchestration` - Airflow/Dagster
- [ ] `77-mlops-data-engineering/experiment-tracking` - MLflow/W&B
- [ ] `78-inference-model-serving/model-caching-warmpool` - Model Caching
- [ ] `79-edge-ai-tinyml/on-device-model-training` - On-device Training
- [ ] `80-agentic-ai-advanced-learning/rag-advanced` - Advanced RAG
- [ ] `81-saas-finops-pricing/customer-lifetime-value` - CLV Modeling
- [ ] `82-technical-product-management/product-discovery-validation` - Product Discovery
- [ ] `83-go-to-market-tech/technical-content-marketing` - Technical Content

---

### 🚀 NEW: Enterprise Architecture Skills (73-164)

> **Note:** กำลังรับ contributions สำหรับ Enterprise Skills ใหม่ตาม Enterprise Architecture Capability Roadmap 2025-2026

#### Critical Priority (Enterprise IoT & Cloud)
- [ ] `73-iot-fleet-management/differential-ota-updates` - OTA Delta Updates
- [ ] `74-iot-zero-trust-security/hardware-rooted-identity` - Hardware Root of Trust
- [ ] `74-iot-zero-trust-security/mtls-pki-management` - mTLS & PKI
- [ ] `75-edge-computing/lightweight-kubernetes` - K3s/MicroK8s for Edge

#### Critical Priority (AI & Data Architecture)
- [ ] `77-mlops-data-engineering/feature-store-implementation` - Feature Store (Feast/Tecton)
- [ ] `77-mlops-data-engineering/drift-detection-retraining` - Drift Detection & Auto-retraining
- [ ] `78-inference-model-serving/high-performance-inference` - Triton/TorchServe
- [ ] `80-agentic-ai-advanced-learning/agentic-ai-frameworks` - LangChain/LangGraph Agents

#### High Priority (Business & Product)
- [ ] `81-saas-finops-pricing/cloud-unit-economics` - FinOps & Unit Economics
- [ ] `81-saas-finops-pricing/usage-based-pricing` - Consumption-based Pricing
- [ ] `82-technical-product-management/business-to-technical-spec` - Business to Tech Spec
- [ ] `84-compliance-ai-governance/ai-explainability-ethics` - AI Explainability (SHAP/LIME)

#### Future-Ready Skills (High Priority)
- [ ] `86-sustainable-ai/green-computing-finops` - Sustainable AI & Carbon-aware Computing
- [ ] `87-multi-agent-governance/multi-agent-orchestration` - Multi-Agent Orchestration & HITL
- [ ] `88-ai-supply-chain-security/model-bom-security` - AI SBOM & Supply Chain Security
- [ ] `89-post-quantum-cryptography/pqc-for-iot` - Post-Quantum Cryptography

---

## 🚀 Becoming a Core Contributor

Regular contributors may be invited to become core contributors with:

- Write access to the repository
- Ability to review and merge PRs
- Input on project direction
- Recognition as a maintainer

**Criteria:**
- 5+ merged PRs of high quality
- Active participation in discussions
- Help reviewing other PRs
- Demonstrated understanding of skill guidelines

---

## 📅 Release Cycle

- **Minor releases** (new skills): Weekly
- **Major releases** (new categories): Monthly
- **Patch releases** (fixes): As needed

---

## 🎉 Thank You!

Your contributions make this project better for everyone. We appreciate your time and effort!

---

<div align="center">

**Questions?** Open an issue or start a discussion!

Made with ❤️ by the Cerebrate Chai community

</div>
