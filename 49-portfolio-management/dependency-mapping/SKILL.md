---
name: Dependency Mapping
description: Comprehensive guide to identifying, visualizing, and managing dependencies in complex projects to reduce risks and enable coordination
---

# Dependency Mapping

## What are Dependencies?

**Definition:** Work that relies on other work to complete.

### Simple Example
```
Task A: Design API
Task B: Implement API client
Dependency: B depends on A (can't implement client until API is designed)
```

### Why Dependencies Matter
- **Block work:** If A is delayed, B is blocked
- **Cascade delays:** One delay affects multiple tasks
- **Coordination needed:** Teams must sync
- **Risk:** Dependencies are points of failure

---

## Why Dependency Mapping Matters

### 1. Identify Risks (Blocked Work)

**Without Mapping:**
> "Why isn't the mobile app done?" → "Waiting for API from backend team" (surprise!)

**With Mapping:**
> Dependencies identified upfront → Coordinate with backend team → No surprises

### 2. Sequence Work Properly

**Bad Sequence:**
```
Week 1: Start mobile app
Week 2: Realize we need API first
Week 3: Wait for API
Week 4: Resume mobile app (wasted 2 weeks)
```

**Good Sequence:**
```
Week 1-2: API design and implementation
Week 3-4: Mobile app (no waiting)
```

### 3. Plan Capacity Realistically

**Without Dependencies:**
> "We can do 3 projects in parallel!" (all blocked on same dependency)

**With Dependencies:**
> "Project A must finish before B and C can start" (realistic plan)

### 4. Coordinate Cross-Team Work

**Example:**
```
Mobile team depends on:
• Backend team (API)
• Platform team (Push notifications)
• Design team (UI mockups)

→ Need coordination meetings, shared timeline
```

---

## Types of Dependencies

### 1. Finish-to-Start (Most Common)

**Definition:** B starts after A finishes

**Example:**
```
A: Design API ──finish──> B: Implement client
```

**Real-world:**
- API must be designed before client can be implemented
- Database schema must be created before migrations run
- Design must be approved before development starts

### 2. Start-to-Start

**Definition:** B starts when A starts

**Example:**
```
A: Backend development ──start together──> B: Frontend development
```

**Real-world:**
- Backend and frontend can start together (using API contract)
- Testing can start when development starts (test-driven development)

### 3. Finish-to-Finish

**Definition:** B finishes when A finishes

**Example:**
```
A: Feature development ──finish together──> B: Documentation
```

**Real-world:**
- Documentation finishes when feature finishes
- Testing finishes when development finishes

### 4. External Dependencies

**Definition:** Depends on vendor, partner, or outside team

**Example:**
```
Our work: Payment integration
External dependency: Stripe API availability
```

**Real-world:**
- Third-party API availability
- Vendor deliverables
- Legal/compliance approvals
- Partner integrations

---

## Dependency Identification

### 1. Technical Dependencies (Shared Libraries, APIs)

**Questions:**
- What shared code do we depend on?
- What APIs do we call?
- What libraries do we use?

**Example:**
```
Mobile app depends on:
• Auth library (shared)
• User API (backend team)
• Analytics SDK (platform team)
```

### 2. Data Dependencies (Schema Changes)

**Questions:**
- What database tables do we use?
- What schema changes are needed?
- Who else uses this data?

**Example:**
```
New feature: User profiles
Data dependencies:
• Add `bio` column to `users` table (DBA approval needed)
• Migrate existing users (data team)
• Update analytics queries (analytics team)
```

### 3. Team Dependencies (Need Another Team's Work)

**Questions:**
- What work from other teams do we need?
- When do we need it?
- What happens if it's delayed?

**Example:**
```
Mobile app launch depends on:
• Backend team: API endpoints (week 4)
• Platform team: Push notification service (week 8)
• Design team: UI mockups (week 2)
• QA team: Testing (week 10)
```

### 4. Resource Dependencies (Shared Resources)

**Questions:**
- What shared resources do we need?
- Who else needs them?
- Can we parallelize?

**Example:**
```
Both projects need:
• Senior engineer (can't work on both simultaneously)
• Staging environment (can't deploy both at once)
• Database migration window (only one migration at a time)
```

### 5. Knowledge Dependencies (Need Expertise)

**Questions:**
- What expertise do we need?
- Who has it?
- Can they be available?

**Example:**
```
Blockchain integration depends on:
• Crypto expert (only 1 person on team)
• Security review (external consultant)
• Legal review (compliance team)
```

---

## Dependency Mapping Techniques

### 1. Dependency Matrix (Grid of Projects)

**Format:**
```
         │ Proj A │ Proj B │ Proj C │ Proj D
─────────┼────────┼────────┼────────┼────────
Proj A   │   -    │   X    │        │
Proj B   │        │   -    │   X    │   X
Proj C   │        │        │   -    │
Proj D   │        │        │   X    │   -

X = Depends on (row depends on column)
```

**Reading:**
- Proj A depends on Proj B
- Proj B depends on Proj C and Proj D
- Proj D depends on Proj C

**Pros:**
- Shows all dependencies at once
- Easy to spot circular dependencies

**Cons:**
- Hard to read with many projects
- Doesn't show timing

### 2. Network Diagram (Nodes and Edges)

**Format:**
```
[API Design] ──> [Mobile App] ──> [Beta Launch]
      │              │
      └──> [Web App] ┘
```

**Pros:**
- Visual and intuitive
- Shows flow of work
- Easy to identify critical path

**Cons:**
- Can get messy with many dependencies

### 3. Gantt Chart with Dependency Lines

**Format:**
```
Task         │ Week 1 │ Week 2 │ Week 3 │ Week 4
─────────────┼────────┼────────┼────────┼────────
API Design   │████████│        │        │
Mobile App   │        │████████│████████│
Web App      │        │████████│████████│
Beta Launch  │        │        │        │████████
             │        │   ↑    │        │   ↑
             │        │   └────────────────┘
             │        │  (dependency)
```

**Pros:**
- Shows timeline
- Shows dependencies and sequence

**Cons:**
- Implies specific dates (may be too rigid)

### 4. Story Mapping with Dependencies

**Format:**
```
Epic: Mobile App Launch

User Story 1: API Design ──┐
User Story 2: UI Design    │
User Story 3: Mobile Dev ──┘ (depends on 1 and 2)
User Story 4: Testing ─────┘ (depends on 3)
User Story 5: Launch ──────┘ (depends on 4)
```

**Pros:**
- Connects to agile workflow
- Shows user value

**Cons:**
- Less visual than network diagram

---

## Visualizing Dependencies

### Color Coding by Type

**Colors:**
- 🔴 **Red:** Critical dependency (blocks multiple tasks)
- 🟡 **Yellow:** Important dependency (blocks one task)
- 🟢 **Green:** Nice-to-have dependency (doesn't block)
- 🔵 **Blue:** External dependency (outside our control)

**Example:**
```
[API Design] ──🔴──> [Mobile App] (critical: blocks mobile and web)
[UI Design] ──🟡──> [Mobile App] (important: blocks mobile only)
[Analytics] ──🟢──> [Mobile App] (nice-to-have: doesn't block launch)
[Stripe API] ──🔵──> [Payment] (external: vendor dependency)
```

### Arrows Showing Direction

**Convention:**
```
A ──> B  (B depends on A)
A <── B  (A depends on B)
A <──> B (mutual dependency, circular!)
```

### Critical Path Highlighting

**Critical Path:** Longest chain of dependencies (determines minimum project duration)

**Example:**
```
Path 1: API (2w) → Mobile (4w) → Testing (1w) = 7 weeks
Path 2: UI (1w) → Mobile (4w) → Testing (1w) = 6 weeks
Path 3: Analytics (2w) = 2 weeks

Critical Path: Path 1 (7 weeks) ← Optimize this!
```

**Highlight:**
```
[API Design] ══> [Mobile App] ══> [Testing] ══> [Launch]
     2w             4w              1w           (7w total)
     ══ = Critical path (bold/highlighted)
```

### Dependency Strength (Hard vs Soft)

**Hard Dependency:** Must have, blocks work
**Soft Dependency:** Nice to have, doesn't block

**Example:**
```
[API] ═══> [Mobile App] (hard: can't build without API)
[Analytics] ···> [Mobile App] (soft: can launch without analytics)

═══ = Hard dependency (solid line)
··· = Soft dependency (dotted line)
```

---

## Critical Path Analysis

### What is Critical Path?

**Definition:** Longest chain of dependencies that determines minimum project duration.

**Why It Matters:**
- Determines earliest completion date
- Shows where to focus optimization
- Identifies highest-risk dependencies

### Finding Critical Path

**Steps:**
1. List all tasks and durations
2. Map dependencies
3. Calculate all possible paths
4. Identify longest path

**Example:**
```
Tasks:
A: API Design (2 weeks)
B: UI Design (1 week)
C: Mobile Dev (4 weeks, depends on A and B)
D: Testing (1 week, depends on C)
E: Analytics (2 weeks, independent)

Paths:
Path 1: A (2w) → C (4w) → D (1w) = 7 weeks ← Critical path!
Path 2: B (1w) → C (4w) → D (1w) = 6 weeks
Path 3: E (2w) = 2 weeks

Critical Path: A → C → D (7 weeks)
```

### Optimizing Critical Path

**Strategies:**
1. **Reduce task duration:** Make critical tasks faster
2. **Parallelize:** Do tasks concurrently
3. **Remove dependencies:** Break coupling
4. **Add resources:** More people on critical tasks

**Example:**
```
Before:
A (2w) → C (4w) → D (1w) = 7 weeks

After optimization:
• Reduce A from 2w to 1w (use API contract, start C early)
• Parallelize D with C (test while developing)

A (1w) → C (4w) = 5 weeks (2 weeks saved!)
       → D (concurrent)
```

---

## Managing Dependencies

### 1. Make Dependencies Explicit (Document)

**Dependency Register:**
```markdown
| Dependency | Type | Owner | Needed By | Status | Risk |
|------------|------|-------|-----------|--------|------|
| API endpoints | Technical | Backend team | Week 4 | In progress | Medium |
| UI mockups | Team | Design team | Week 2 | Done | Low |
| Push service | Platform | Platform team | Week 8 | Not started | High |
```

### 2. Prioritize Breaking Dependencies (Reduce Coupling)

**Strategies:**
- Use API contracts (agree interface, implement independently)
- Feature flags (deploy independently, enable together)
- Mocks/stubs (develop against fake dependencies)

**Example:**
```
Before:
Mobile app waits for API to be fully implemented (4 weeks blocked)

After:
1. Define API contract (1 day)
2. Mobile team builds against mock API (no waiting)
3. Backend team implements real API (parallel work)
4. Integration testing (1 week)

Result: 3 weeks saved
```

### 3. Coordinate with Dependent Teams

**Coordination Mechanisms:**
- Shared roadmap (visibility)
- Weekly sync meetings (alignment)
- Slack channel (quick questions)
- Written agreements (SLAs, contracts)

**Example:**
```
Mobile team + Backend team coordination:
• Shared roadmap: Both teams see API deadline (week 4)
• Weekly sync: Monday 10am, review progress
• Slack: #mobile-backend-integration
• Agreement: API contract signed, backend commits to week 4 delivery
```

### 4. Have Contingency Plans

**Risk Mitigation:**
- Plan B if dependency is delayed
- Workarounds
- Fallback options

**Example:**
```
Dependency: Push notification service (week 8)
Risk: Platform team may delay

Contingency plans:
• Plan B: Use third-party service (Firebase)
• Workaround: Launch without push, add later
• Fallback: Email notifications instead
```

---

## Reducing Dependencies

### 1. API Contracts (Agree Interface, Implement Independently)

**Process:**
1. Define API contract (input, output, errors)
2. Both teams agree on contract
3. Teams implement independently
4. Integration testing

**Example:**
```yaml
# API Contract
POST /api/users
Request:
  {
    "email": "user@example.com",
    "name": "John Doe"
  }
Response:
  {
    "id": "123",
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": "2024-01-15T10:00:00Z"
  }
Errors:
  400: Invalid email
  409: Email already exists
```

**Benefits:**
- Teams work in parallel
- No waiting
- Clear expectations

### 2. Feature Flags (Deploy Independently, Enable Together)

**Process:**
1. Backend deploys API (feature flag off)
2. Frontend deploys client (feature flag off)
3. Both teams test independently
4. Enable feature flags together

**Example:**
```javascript
// Backend
if (featureFlags.isEnabled('new-api')) {
  return newAPI(req);
} else {
  return oldAPI(req);
}

// Frontend
if (featureFlags.isEnabled('new-api')) {
  callNewAPI();
} else {
  callOldAPI();
}
```

**Benefits:**
- Deploy anytime
- No coordination needed for deployment
- Can rollback independently

### 3. Mocks/Stubs (Develop Against Fake Dependencies)

**Process:**
1. Create mock service (fake API)
2. Develop against mock
3. Swap mock for real service later

**Example:**
```javascript
// Mock API for development
const mockAPI = {
  getUser: (id) => ({
    id,
    name: 'Mock User',
    email: 'mock@example.com'
  })
};

// Real API for production
const realAPI = {
  getUser: (id) => fetch(`/api/users/${id}`)
};

// Use mock in development, real in production
const api = process.env.NODE_ENV === 'development' ? mockAPI : realAPI;
```

**Benefits:**
- No waiting for real API
- Faster development
- Can test edge cases

### 4. Modular Architecture (Loose Coupling)

**Principles:**
- Each module has clear interface
- Modules don't depend on internals of other modules
- Changes in one module don't affect others

**Example:**
```
Before (Tight Coupling):
Mobile app directly queries backend database (high dependency)

After (Loose Coupling):
Mobile app calls API → API queries database (low dependency)
```

**Benefits:**
- Easier to change
- Easier to test
- Easier to parallelize work

---

## Dependency Risks

### 1. Blocked Work (Upstream Not Delivered)

**Risk:**
```
Mobile app ready to start (week 3)
API not delivered until week 6
Result: Mobile team blocked for 3 weeks
```

**Mitigation:**
- Identify dependencies early
- Use mocks to unblock
- Have contingency plans

### 2. Cascading Delays (One Delay Affects Many)

**Risk:**
```
API delayed by 2 weeks
→ Mobile app delayed by 2 weeks
→ Web app delayed by 2 weeks
→ Beta launch delayed by 2 weeks
```

**Mitigation:**
- Reduce dependencies (break coupling)
- Parallelize work where possible
- Buffer time in schedule

### 3. Integration Issues (Parts Don't Fit Together)

**Risk:**
```
Backend implements API one way
Frontend expects API another way
Result: Integration fails, rework needed
```

**Mitigation:**
- API contracts (agree upfront)
- Integration testing (test early)
- Regular syncs (catch issues early)

---

## Dependency Tracking

### Dependency Register

**Template:**
```markdown
# Dependency Register

| ID | Dependency | Type | Owner | Dependent | Needed By | Status | Risk | Notes |
|----|------------|------|-------|-----------|-----------|--------|------|-------|
| D1 | API endpoints | Technical | Backend | Mobile | Week 4 | In progress | Medium | On track |
| D2 | UI mockups | Team | Design | Mobile | Week 2 | Done | Low | Completed |
| D3 | Push service | Platform | Platform | Mobile | Week 8 | Not started | High | Risk of delay |
| D4 | Stripe API | External | Stripe | Payment | Week 6 | Blocked | High | Waiting for approval |
```

### Status Tracking

**Statuses:**
- **Not Started:** Dependency work hasn't begun
- **In Progress:** Dependency work is ongoing
- **Blocked:** Dependency is blocked by something else
- **At Risk:** Dependency may be delayed
- **Done:** Dependency is complete
- **Resolved:** Dependency is no longer needed

### Regular Check-Ins

**Weekly Dependency Review:**
1. Review dependency register
2. Update statuses
3. Identify new dependencies
4. Escalate blocked dependencies
5. Adjust plans if needed

**Example Agenda:**
```
Weekly Dependency Review (Mondays, 10am)

1. Review each dependency (5 min each)
   - Status update
   - Any blockers?
   - On track for deadline?

2. New dependencies (10 min)
   - Any new dependencies identified?
   - Add to register

3. Escalations (10 min)
   - Which dependencies are at risk?
   - Who can help unblock?

4. Action items (5 min)
   - What needs to happen this week?
```

---

## Cross-Team Coordination

### 1. Shared Roadmaps

**Purpose:** All teams see each other's plans

**Example:**
```
Q1 2024 Roadmap (All Teams)

Backend Team:
• API v2 (weeks 1-4)
• Database migration (weeks 5-8)

Mobile Team:
• Mobile app (weeks 3-10, depends on API v2)

Platform Team:
• Push notifications (weeks 1-8)
• Analytics (weeks 9-12)

Dependencies:
• Mobile depends on Backend (API v2, week 4)
• Mobile depends on Platform (Push, week 8)
```

### 2. Integration Meetings

**Purpose:** Coordinate work across teams

**Frequency:** Weekly or bi-weekly

**Agenda:**
```
Integration Meeting (Wednesdays, 2pm)

1. Progress updates (10 min)
   - Each team shares progress
   - Highlight any delays

2. Dependency review (15 min)
   - Review dependency register
   - Update statuses
   - Identify blockers

3. Integration planning (15 min)
   - When will integration happen?
   - Who will do integration testing?
   - What's the rollback plan?

4. Action items (5 min)
```

### 3. Slack Channels for Coordination

**Purpose:** Quick questions and updates

**Example:**
```
#mobile-backend-integration
• Quick questions about API
• Status updates
• Blocker notifications

#platform-integrations
• All teams integrating with platform
• Announcements (new services, breaking changes)
```

### 4. Written Contracts/Agreements

**Purpose:** Clear expectations and commitments

**Example:**
```markdown
# API Integration Agreement

**Backend Team Commits:**
- Deliver API v2 by week 4 (Feb 1)
- API will support 1000 req/s
- 99.9% uptime SLA
- Breaking changes communicated 2 weeks in advance

**Mobile Team Commits:**
- Provide API requirements by week 1 (Jan 8)
- Test against staging API (week 3)
- Report bugs within 24 hours

**Escalation:**
- If API delayed: Escalate to Engineering Manager
- If bugs not fixed: Escalate to Product Manager
```

---

## Dependency Anti-Patterns

### 1. Hidden Dependencies (Not Documented)

**Problem:**
```
Week 8: "Why isn't the mobile app done?"
Team: "We're waiting for the push notification service"
Manager: "I didn't know about that dependency!"
```

**Solution:** Document all dependencies upfront

### 2. Circular Dependencies (A → B → A)

**Problem:**
```
A depends on B
B depends on C
C depends on A
→ Deadlock! Nothing can start.
```

**Solution:** Break the cycle (redesign to remove circular dependency)

### 3. Too Many Dependencies (Tight Coupling)

**Problem:**
```
Mobile app depends on:
• 5 backend APIs
• 3 platform services
• 2 external vendors
• 4 shared libraries

→ High risk of being blocked
```

**Solution:** Reduce dependencies (use mocks, break coupling)

### 4. Ignored Dependencies (Surprise at Integration Time)

**Problem:**
```
Week 10: Integration time
"The API returns XML, but we expected JSON!"
→ Rework needed, 2 weeks delay
```

**Solution:** API contracts, integration testing early

---

## Tools

### Jira (Issue Linking)

**Features:**
- Link issues (blocks, is blocked by)
- Dependency visualization
- Roadmap view with dependencies

**Example:**
```
MOBILE-123: Mobile app
  Blocked by: BACKEND-456 (API v2)
  Blocked by: PLATFORM-789 (Push service)
```

### Monday.com (Dependency Columns)

**Features:**
- Dependency columns
- Gantt chart with dependencies
- Automation (notify when dependency is done)

### Microsoft Project (Gantt)

**Features:**
- Gantt chart with dependency lines
- Critical path analysis
- Resource leveling

### Miro (Visual Mapping)

**Features:**
- Visual dependency mapping
- Collaborative
- Flexible (can create any format)

---

## Real Dependency Mapping Examples

### Example 1: Mobile App Launch

```
Dependency Map:

[API Design] ──> [API Implementation] ──> [Mobile App] ──> [Beta Launch]
     2w                 4w                     6w              1w
     
[UI Design] ──> [Mobile App]
     1w            6w

[Push Service] ──> [Mobile App]
     8w               6w

Critical Path: API Design → API Implementation → Mobile App → Beta Launch (13 weeks)

Risks:
• Push Service (8w) may not be ready when Mobile App needs it (week 6)
• Mitigation: Start Push Service earlier, or launch without push initially
```

### Example 2: Platform Migration

```
Dependency Matrix:

              │ DB Migration │ API v2 │ Mobile │ Web │ Analytics
──────────────┼──────────────┼────────┼────────┼─────┼──────────
DB Migration  │      -       │   X    │        │     │
API v2        │              │   -    │   X    │  X  │
Mobile        │              │        │   -    │     │
Web           │              │        │        │  -  │
Analytics     │      X       │   X    │        │     │    -

Dependencies:
• API v2 depends on DB Migration
• Mobile depends on API v2
• Web depends on API v2
• Analytics depends on DB Migration and API v2

Critical Path: DB Migration → API v2 → Mobile (longest chain)
```

---

## Templates

### Template 1: Dependency Matrix

```markdown
# Dependency Matrix

|          | Proj A | Proj B | Proj C | Proj D |
|----------|--------|--------|--------|--------|
| Proj A   |   -    |        |        |        |
| Proj B   |   X    |   -    |        |        |
| Proj C   |        |   X    |   -    |        |
| Proj D   |        |   X    |   X    |   -    |

X = Row depends on Column
```

### Template 2: Network Diagram

```markdown
# Dependency Network

```
[Task A] ──> [Task B] ──> [Task D]
    │            │
    └──> [Task C]┘
```

Critical Path: A → B → D
```

### Template 3: Dependency Register

```markdown
# Dependency Register

| ID | Dependency | Type | Owner | Dependent | Needed By | Status | Risk | Mitigation |
|----|------------|------|-------|-----------|-----------|--------|------|------------|
| D1 | [Name] | [Technical/Team/External] | [Team] | [Project] | [Date] | [Status] | [High/Med/Low] | [Plan] |
```

---

## Summary

### Quick Reference

**Dependency Types:**
- Finish-to-Start: B starts after A finishes (most common)
- Start-to-Start: B starts when A starts
- Finish-to-Finish: B finishes when A finishes
- External: Vendor, partner, outside team

**Mapping Techniques:**
- Dependency matrix (grid)
- Network diagram (nodes and edges)
- Gantt chart (timeline with dependencies)
- Story mapping (agile-friendly)

**Critical Path:**
- Longest chain of dependencies
- Determines minimum duration
- Focus optimization here

**Managing Dependencies:**
- Make explicit (document)
- Prioritize breaking (reduce coupling)
- Coordinate with teams (meetings, Slack)
- Have contingency plans (Plan B)

**Reducing Dependencies:**
- API contracts (agree interface)
- Feature flags (deploy independently)
- Mocks/stubs (fake dependencies)
- Modular architecture (loose coupling)

**Risks:**
- Blocked work
- Cascading delays
- Integration issues

**Tools:**
- Jira (issue linking)
- Monday.com (dependency columns)
- Microsoft Project (Gantt)
- Miro (visual mapping)

**Anti-Patterns:**
- Hidden dependencies
- Circular dependencies
- Too many dependencies
- Ignored dependencies
