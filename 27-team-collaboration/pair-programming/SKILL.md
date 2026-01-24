---
name: Pair Programming
description: Software development technique where two developers work together at one workstation, with one writing code (driver) while the other reviews and guides (navigator) for better code quality and knowledge sharing.
---

# Pair Programming

> **Current Level:** Intermediate  
> **Domain:** Team Collaboration / Development Practices

---

## Overview

Pair programming is a software development technique where two developers work together at one workstation. One writes code (driver) while the other reviews and guides (navigator). This practice improves code quality, reduces bugs, facilitates knowledge sharing, and improves team collaboration.

## What is Pair Programming

### Core Concept

```
┌─────────────────────────────────────────────────────────────────┐
│  Pair Programming Setup                                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  Driver (Typing)          Navigator (Reviewing)        │     │
│  │  ┌─────────────┐         ┌─────────────┐           │     │
│  │  │  Keyboard   │         │  Reviewing  │           │     │
│  │  │  & Mouse    │         │  Code       │           │     │
│  │  └─────────────┘         └─────────────┘           │     │
│  │                                                          │     │
│  │  Roles:                                                  │     │
│  │  - Driver: Types code, focuses on details                  │     │
│  │  - Navigator: Reviews, focuses on big picture               │     │
│  └─────────────────────────────────────────────────────────┘     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Benefits

| Benefit | Impact |
|---------|---------|
| **Code Quality** | Fewer bugs, better design |
| **Knowledge Sharing** | Team learns from each other |
| **Focus** | Less distraction, more productive |
| **Collaboration** | Better team communication |
| **Learning** | Faster skill development |

## Roles

### Driver

```javascript
// Driver: Types code, focuses on details
function calculateTotal(items) {
    // Driver types the code
    return items.reduce((sum, item) => sum + item.price, 0);
}
```

**Responsibilities:**
- Types code
- Focuses on syntax and details
- Implements the solution
- Follows navigator's guidance

### Navigator

```javascript
// Navigator: Reviews, focuses on big picture
// "I noticed we're not handling empty arrays. 
// Should we add a check?"

function calculateTotal(items) {
    // Navigator reviews the code
    if (!items || items.length === 0) return 0;
    return items.reduce((sum, item) => sum + item.price, 0);
}
```

**Responsibilities:**
- Reviews code in real-time
- Focuses on design and architecture
- Thinks about edge cases
- Guides the driver

## Benefits

### Code Quality

```javascript
// Before pairing (single developer)
function calculateTotal(items) {
    // Bug: Doesn't handle empty array
    return items.reduce((sum, item) => sum + item.price, 0);
}

// After pairing (two developers)
function calculateTotal(items) {
    // Navigator catches the bug
    if (!items || items.length === 0) return 0;
    return items.reduce((sum, item) => sum + item.price, 0);
}
```

### Knowledge Sharing

```javascript
// Senior developer teaches junior
// Junior: "How do I use reduce?"
// Senior: "Let me show you..."

function calculateTotal(items) {
    // Senior explains reduce
    return items.reduce((sum, item) => sum + item.price, 0);
}
```

### Focus

```javascript
// Pairing reduces distraction
// Two developers keep each other focused

function calculateTotal(items) {
    // Driver focuses on typing
    // Navigator focuses on reviewing
    // Less distraction, more productivity
    return items.reduce((sum, item) => sum + item.price, 0);
}
```

### Collaboration

```javascript
// Better communication
// Two developers discuss approach

function calculateTotal(items) {
    // Driver: "Should we use reduce or for loop?"
    // Navigator: "Reduce is more functional"
    // Driver: "OK, let's use reduce"
    return items.reduce((sum, item) => sum + item.price, 0);
}
```

## When to Pair

### Complex Features

```javascript
// Complex feature: Payment processing
function processPayment(order) {
    // Complex logic
    // Multiple edge cases
    // Good for pairing
}
```

### Onboarding

```javascript
// Onboarding: Teach new developer
function calculateTotal(items) {
    // Senior teaches junior
    // Junior learns codebase
    // Good for onboarding
    return items.reduce((sum, item) => sum + item.price, 0);
}
```

### Debugging

```javascript
// Debugging: Hard to find bug
function processOrder(order) {
    // Bug somewhere
    // Two pairs of eyes
    // Good for debugging
}
```

### Critical Code

```javascript
// Critical code: Security, payments
function processPayment(order) {
    // Security critical
    // No room for mistakes
    // Good for pairing
}
```

## Pairing Styles

### Driver-Navigator

```javascript
// Traditional pairing
// Driver types, navigator reviews

function calculateTotal(items) {
    // Driver types
    return items.reduce((sum, item) => sum + item.price, 0);
    
    // Navigator reviews
    // "Should we handle empty array?"
}
```

### Ping-Pong

```javascript
// Ping-pong pairing
// Switch roles after each test

// Person A writes test
it('calculates total correctly', () => {
    expect(calculateTotal([{ price: 10 }, { price: 20 }])).toBe(30);
});

// Person B writes implementation
function calculateTotal(items) {
    return items.reduce((sum, item) => sum + item.price, 0);
}

// Switch roles
```

### Strong-Style

```javascript
// Strong-style pairing
// Navigator tells driver what to type

// Navigator: "Create a function called calculateTotal"
function calculateTotal(items) {
    // Navigator: "Use reduce to sum prices"
    return items.reduce((sum, item) => sum + item.price, 0);
}
```

## Pairing Best Practices

### Switch Roles

```markdown
# Switch Roles Regularly

## How Often
- Every 30 minutes
- After completing a feature
- After writing a test

## Why Switch
- Prevents fatigue
- Gives equal experience
- Keeps both engaged
```

### Take Breaks

```markdown
# Take Breaks

## How Often
- Every 60-90 minutes
- Pomodoro technique

## Why Breaks
- Prevents fatigue
- Maintains focus
- Reduces mistakes
```

### Communicate

```markdown
# Communicate Effectively

## Best Practices
- Talk through decisions
- Explain your thinking
- Ask questions
- Listen actively

## What to Discuss
- Approach to problem
- Design decisions
- Edge cases
- Alternatives
```

## Remote Pairing

### Tools

| Tool | Description |
|-------|-------------|
| **VS Code Live Share** | Real-time code sharing |
| **Tuple** | Remote pairing platform |
| **Zoom** | Video + screen sharing |
| **Google Meet** | Video + screen sharing |
| **Discord** | Voice + screen sharing |

### VS Code Live Share

```bash
# Install Live Share extension
# VS Code: Extensions → Live Share

# Start Live Share
# Click "Share" button
# Copy link and send to partner

# Join Live Share
# Click "Join" button
# Paste link
```

### Tuple

```bash
# Install Tuple
# https://tuple.app

# Start Tuple
# Invite partner
# Share screen
```

## Pairing Challenges

### Fatigue

```markdown
# Fatigue

## Symptoms
- Loss of focus
- Irritability
- Mistakes increase

## Solutions
- Take regular breaks
- Switch roles often
- Limit pairing sessions
```

### Personality Conflicts

```markdown
# Personality Conflicts

## Symptoms
- Disagreements
- Frustration
- Tension

## Solutions
- Communicate openly
- Respect differences
- Take breaks
- Switch partners
```

### Skill Mismatch

```markdown
# Skill Mismatch

## Symptoms
- One dominates
- One feels useless
- Unequal contribution

## Solutions
- Adjust roles
- Take turns leading
- Be patient
- Learn from each other
```

## Measuring Pairing Effectiveness

### Metrics

```javascript
// Track pairing metrics
const pairingMetrics = {
    sessions: 10,
    bugsFound: 5,
    featuresCompleted: 8,
    satisfaction: 4.5
};
```

### Feedback

```markdown
# Pairing Feedback

## Questions
- Did pairing help?
- What worked well?
- What didn't work?
- How can we improve?

## Collect Feedback
- After each session
- Anonymous surveys
- Regular check-ins
```

## Tools

### VS Code Live Share

```bash
# Install Live Share
code --install-extension ms-vsliveshare.vsliveshare

# Start Live Share
# Click "Share" button in status bar

# Join Live Share
# Click "Join" button in status bar
```

### Tuple

```bash
# Install Tuple
# https://tuple.app/download

# Start Tuple
# Sign in
# Invite partner
```

### Zoom

```bash
# Start Zoom meeting
# Share screen
# Enable audio
```

## Real Examples

### Pairing Scenarios

```markdown
# Pairing Scenarios

## Scenario 1: Complex Feature
- Task: Implement payment processing
- Pairing: Senior + Junior
- Duration: 2 hours
- Outcome: Feature completed, junior learned

## Scenario 2: Debugging
- Task: Fix bug in checkout
- Pairing: Two seniors
- Duration: 1 hour
- Outcome: Bug fixed, root cause identified

## Scenario 3: Onboarding
- Task: Teach new developer
- Pairing: Senior + New hire
- Duration: 4 hours
- Outcome: New hire onboarded, code learned
```

## Summary Checklist

### Before Pairing

- [ ] Partner selected
- [ ] Goal defined
- [ ] Tools prepared
- [ ] Time allocated
- [ ] Breaks scheduled

### During Pairing

- [ ] Roles defined
- [ ] Communication clear
- [ ] Switch roles regularly
- [ ] Take breaks
- [ ] Stay focused
```

---

## Quick Start

### Pair Programming Setup

```markdown
# Pair Programming Session

## Setup
- [ ] Choose driver and navigator
- [ ] Set up screen sharing (VS Code Live Share, Tuple, etc.)
- [ ] Agree on goal and approach
- [ ] Set timer for role switching (30-60 min)

## During Session
- Driver: Types code, focuses on implementation
- Navigator: Reviews code, thinks about design, catches bugs
- Both: Discuss approach, ask questions

## After Session
- [ ] Review what was accomplished
- [ ] Document decisions
- [ ] Commit code with pair attribution
```

### VS Code Live Share

```bash
# Install Live Share extension
# Share session
# Collaborator joins and can edit together
```

---

## Production Checklist

- [ ] **Partner Selection**: Choose appropriate pairing partner
- [ ] **Goal Definition**: Clear goal for pairing session
- [ ] **Tool Setup**: Screen sharing and collaboration tools
- [ ] **Time Allocation**: Allocate sufficient time
- [ ] **Role Switching**: Regular role switching (30-60 min)
- [ ] **Communication**: Clear communication during pairing
- [ ] **Breaks**: Take regular breaks
- [ ] **Focus**: Stay focused on goal
- [ ] **Documentation**: Document decisions and learnings
- [ ] **Code Review**: Pair programming is continuous review
- [ ] **Knowledge Sharing**: Share knowledge during pairing
- [ ] **Feedback**: Provide feedback after session

---

## Anti-patterns

### ❌ Don't: Driver Only

```markdown
# ❌ Bad - Navigator not engaged
Driver: Types code
Navigator: Browsing internet
```

```markdown
# ✅ Good - Both engaged
Driver: Types code
Navigator: Reviews, suggests improvements, catches bugs
Both: Discuss approach
```

### ❌ Don't: No Role Switching

```markdown
# ❌ Bad - Same person always driver
Session 1: Alice (driver), Bob (navigator)
Session 2: Alice (driver), Bob (navigator)
# Bob never gets to code!
```

```markdown
# ✅ Good - Regular role switching
Session 1: Alice (driver), Bob (navigator)
After 30 min: Bob (driver), Alice (navigator)
```

---

## Integration Points

- **Code Review Culture** (`27-team-collaboration/code-review-culture/`) - Review practices
- **Knowledge Sharing** (`27-team-collaboration/knowledge-sharing/`) - Knowledge transfer
- **Onboarding** (`27-team-collaboration/onboarding/`) - Pair with new team members

---

## Further Reading

- [Pair Programming Guide](https://martinfowler.com/articles/on-pair-programming.html)
- [VS Code Live Share](https://code.visualstudio.com/learn/collaboration/live-share)
- [Tuple](https://tuple.app/)

### After Pairing

- [ ] Review work
- [ ] Document learnings
- [ ] Provide feedback
- [ ] Plan next session
- [ ] Celebrate success
