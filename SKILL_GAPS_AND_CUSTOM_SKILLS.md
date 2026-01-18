# Skill Gaps & Custom Skills for Malai Platform

**Date**: 2026-01-17  
**Project**: Malai Platform  
**Purpose**: Document missing skills and create custom implementations

---

## 📊 Gap Analysis Summary

### Skills Found in cerebratechai-claude-skills: 473+
### Skills Needed for Malai: 520+
### **Gap**: 47 skills

---

## 🔴 Critical Gaps (Must Create)

### 1. Thai Payment Integration
**Category**: `71-infrastructure-patterns`  
**File**: `thai-payment-integration/SKILL.md`

**Description**:
Integration with Thai payment systems including PromptPay, Thai QR, SCB Easy, and local payment gateways.

**Topics to Cover**:
- PromptPay QR code generation
- Thai QR Payment Standard
- Bank of Thailand regulations
- Omise/2C2P integration
- Payment reconciliation
- Refund workflows
- Multi-currency support (THB primary)

**Code Examples Needed**:
```typescript
// PromptPay QR generation
// Thai QR payment verification
// Webhook handling for Thai banks
```

**Assigned To**: Roo Code (ROO-004)

---

### 2. LINE Platform Integration
**Category**: `20-ai-integration`  
**File**: `line-platform-integration/SKILL.md`

**Description**:
Complete integration with LINE ecosystem including LINE OA, LIFF, and Messaging API.

**Topics to Cover**:
- LINE Official Account setup
- LIFF (LINE Front-end Framework) development
- Messaging API integration
- Rich menus and flex messages
- LINE Login integration
- LINE Pay integration
- Webhook handling

**Code Examples Needed**:
```typescript
// LIFF initialization
// Send flex messages
// LINE Login flow
// Webhook verification
```

**Assigned To**: Codex (CODEX-008), Roo Code (ROO-006)

---

### 3. Escrow Workflow Patterns
**Category**: `09-microservices`  
**File**: `escrow-workflow/SKILL.md`

**Description**:
Patterns for implementing escrow and milestone-based payment systems.

**Topics to Cover**:
- Escrow state machine
- Milestone definition and tracking
- Dispute resolution workflow
- Automated payout triggers
- Compliance and audit trails
- Refund and cancellation handling

**Code Examples Needed**:
```typescript
// Escrow state machine
// Milestone payout logic
// Dispute workflow
```

**Assigned To**: Roo Code (ROO-004)

---

### 4. QR Code Features
**Category**: `17-domain-specific`  
**File**: `qr-code-features/SKILL.md`

**Description**:
QR code generation, scanning, validation, and use cases for events.

**Topics to Cover**:
- QR code generation (various formats)
- QR code scanning and validation
- Dynamic QR codes
- QR code security
- Guest check-in with QR
- Payment QR codes
- Ticket/invitation QR codes

**Code Examples Needed**:
```typescript
// Generate QR code
// Validate QR code
// QR-based check-in
```

**Assigned To**: Roo Code (ROO-008), Codex (CODEX-008)

---

## 🟡 Important Gaps (Should Create)

### 5. Thai Cultural Event Planning
**Category**: `17-domain-specific`  
**File**: `thai-cultural-events/SKILL.md`

**Description**:
Domain knowledge for Thai ceremonies, rituals, and cultural practices.

**Topics to Cover**:
- Thai wedding ceremonies (regional variations)
- Buddhist ordination ceremonies
- Funeral rites
- Merit-making ceremonies
- Auspicious date calculation (Thai astrology)
- Regional customs (North, Northeast, Central, South)
- Vendor types and roles

**Assigned To**: Antigravity (ANTI-002 - AI Service)

---

### 6. Multi-Step Form Patterns
**Category**: `02-frontend`  
**File**: `multi-step-forms/SKILL.md`

**Description**:
Patterns for building complex multi-step forms with state management.

**Topics to Cover**:
- Wizard pattern implementation
- Form state persistence
- Validation per step
- Progress indicators
- Back/forward navigation
- Draft saving
- Conditional steps

**Code Examples Needed**:
```typescript
// Multi-step form hook
// Step validation
// Progress tracking
```

**Assigned To**: Codex (CODEX-004)

---

### 7. Service Orchestration
**Category**: `15-devops-infrastructure`  
**File**: `service-orchestration/SKILL.md`

**Description**:
Patterns for orchestrating multiple microservices in Docker Compose and Kubernetes.

**Topics to Cover**:
- Service dependency management
- Health checks and readiness probes
- Service discovery
- Load balancing
- Rolling updates
- Blue-green deployment
- Canary releases

**Assigned To**: Antigravity (ANTI-004)

---

### 8. Infinite Scroll Patterns
**Category**: `02-frontend`  
**File**: `infinite-scroll/SKILL.md`

**Description**:
Implementation patterns for infinite scroll and virtual scrolling.

**Topics to Cover**:
- Intersection Observer API
- Virtual scrolling
- Performance optimization
- Loading states
- Error handling
- Scroll position restoration

**Code Examples Needed**:
```typescript
// useInfiniteScroll hook
// Virtual list component
```

**Assigned To**: Codex (CODEX-003)

---

## 🟢 Nice-to-Have Gaps (Optional)

### 9. Thai UI/UX Patterns
**Category**: `22-ux-ui-design`  
**File**: `thai-ux-patterns/SKILL.md`

**Description**:
UI/UX best practices for Thai users and cultural considerations.

**Topics to Cover**:
- Thai typography and fonts
- Color symbolism in Thai culture
- Layout preferences
- Mobile-first design for Thai users
- Accessibility for Thai language
- Cultural sensitivity in design

**Assigned To**: Codex (CODEX-011)

---

### 10. Event-Driven Testing
**Category**: `16-testing`  
**File**: `event-driven-testing/SKILL.md`

**Description**:
Testing strategies for event-driven architectures.

**Topics to Cover**:
- Event flow testing
- Saga testing
- Message queue testing
- Event replay testing
- Integration testing with events

**Assigned To**: Roo Code (ROO-012)

---

## 📝 Skill Creation Template

When creating new skills, use this template:

```markdown
---
name: [Skill Name]
category: [Category Number]-[Category Name]
description: [One-line description]
tags: [tag1, tag2, tag3]
difficulty: [beginner|intermediate|advanced]
---

# [Skill Name]

## Overview
[Detailed description of the skill]

## When to Use This Skill
- Use case 1
- Use case 2
- Use case 3

## Core Concepts
### Concept 1
[Explanation]

### Concept 2
[Explanation]

## Implementation Guide

### Step 1: [Step Name]
[Instructions]

```[language]
// Code example
```

### Step 2: [Step Name]
[Instructions]

## Best Practices
1. Best practice 1
2. Best practice 2
3. Best practice 3

## Common Pitfalls
- Pitfall 1 and how to avoid it
- Pitfall 2 and how to avoid it

## Testing Strategies
[How to test implementations using this skill]

## Performance Considerations
[Performance tips and optimization strategies]

## Security Considerations
[Security best practices]

## Real-World Examples
### Example 1: [Scenario]
[Code and explanation]

### Example 2: [Scenario]
[Code and explanation]

## Related Skills
- [Related Skill 1]
- [Related Skill 2]

## Resources
- [Resource 1]
- [Resource 2]

## Checklist
- [ ] Requirement 1
- [ ] Requirement 2
- [ ] Requirement 3
```

---

## 🔄 Skill Update Process

### 1. Identify Gap
- Agent encounters missing skill during implementation
- Document in daily standup
- Add to this file

### 2. Prioritize
- **P0 (Critical)**: Blocks current work
- **P1 (Important)**: Needed within sprint
- **P2 (Nice-to-have)**: Future enhancement

### 3. Create Skill
- Use template above
- Include code examples
- Add to appropriate category
- Test with real implementation

### 4. Share & Update
- Commit to cerebratechai-claude-skills repo
- Update SKILL_INDEX.md
- Notify team in Slack
- Update work orders if needed

### 5. Apply
- Use new skill in implementation
- Gather feedback
- Iterate and improve

---

## 📊 Skill Gap Tracking

| Skill | Priority | Status | Assigned To | ETA |
|-------|----------|--------|-------------|-----|
| thai-payment-integration | P0 | 🟢 Complete | Roo Code | ✅ Completed |
| line-platform-integration | P0 | 🟢 Complete | Codex/Roo | ✅ Completed |
| escrow-workflow | P0 | 🟢 Complete | Roo Code | ✅ Completed |
| qr-code-features | P0 | 🟢 Complete | Roo Code | ✅ Completed |
| thai-cultural-events | P1 | 🟢 Complete | Antigravity | ✅ Completed |
| multi-step-forms | P1 | 🟢 Complete | Codex | ✅ Completed |
| service-orchestration | P1 | 🟢 Complete | Antigravity | ✅ Completed |
| infinite-scroll | P1 | 🟢 Complete | Codex | ✅ Completed |
| thai-ux-patterns | P2 | 🟢 Complete | Codex | ✅ Completed |
| event-driven-testing | P2 | 🟢 Complete | Roo Code | ✅ Completed |

**Status Legend**:
- 🔴 Not Started
- 🟡 In Progress
- 🟢 Complete
- ⚪ Blocked

---

## 🎯 Action Items

### Week 1
- [ ] Create `service-orchestration` skill (Antigravity)
- [ ] Create `line-platform-integration` skill outline (Codex)

### Week 2
- [ ] Complete `line-platform-integration` skill (Codex)
- [ ] Create `infinite-scroll` skill (Codex)

### Week 3
- [ ] Create `thai-payment-integration` skill (Roo Code)
- [ ] Create `thai-cultural-events` skill (Antigravity)
- [ ] Create `multi-step-forms` skill (Codex)

### Week 4
- [ ] Create `escrow-workflow` skill (Roo Code)

### Week 5
- [ ] Create `qr-code-features` skill (Roo Code)

---

## 📚 Existing Skills to Leverage

### From cerebratechai-claude-skills

**Can be used directly**:
- `payment-gateways` - Base for Thai payments
- `websocket-patterns` - For real-time features
- `saga-pattern` - For booking workflow
- `llm-integration` - For AI service
- `rag-implementation` - For knowledge base
- `nextjs-patterns` - For frontend
- `prisma-guide` - For database
- `docker-compose` - For infrastructure

**Need customization**:
- `notification-system` → Add LINE OA support
- `form-handling` → Extend for multi-step
- `api-gateway` → Add Thai-specific middleware
- `dashboard-design` → Add Thai language support

---

## 💡 Skill Enhancement Suggestions

### Enhance Existing Skills

1. **payment-gateways**
   - Add Thai payment gateway section
   - Include PromptPay examples
   - Add Thai QR standard

2. **notification-system**
   - Add LINE Messaging API
   - Include Thai SMS providers
   - Add Thai language templates

3. **form-handling**
   - Add multi-step wizard patterns
   - Include Thai form validation
   - Add Thai date/time pickers

4. **api-gateway**
   - Add Thai language middleware
   - Include Thai timezone handling
   - Add Thai currency conversion

---

## 🔗 Contribution to cerebratechai-claude-skills

### Skills to Contribute Back

After creating and testing, these skills should be contributed to the main repository:

1. **thai-payment-integration** - Useful for any Thai project
2. **line-platform-integration** - LINE is popular in Asia
3. **escrow-workflow** - General marketplace pattern
4. **qr-code-features** - Widely applicable
5. **multi-step-forms** - Common frontend pattern

### Contribution Process
1. Create skill following template
2. Test in real implementation (Malai)
3. Gather feedback from team
4. Refine and polish
5. Submit PR to cerebratechai-claude-skills
6. Update SKILL_INDEX.md

---

## 📞 Support & Questions

**For Skill Questions**:
- Post in `#malai-skills` Slack channel
- Tag relevant agent
- Reference this document

**For Skill Creation Help**:
- Review existing skills in cerebratechai-claude-skills
- Use template provided above
- Ask for peer review before finalizing

---

**Document Owner**: All Agents (Collaborative)  
**Last Updated**: 2026-01-17  
**Next Review**: Weekly during sprint retrospectives
