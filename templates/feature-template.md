# Feature: [Feature Name]

## Overview
**Description**: [Brief description of the feature]
**Priority**: [High / Medium / Low]
**Estimated Time**: [Hours/Days]
**Status**: [Planning / In Progress / Review / Done]

## User Story
As a [type of user],
I want to [action],
So that [benefit].

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Technical Approach

### Required Skills
- [ ] [Skill 1]
- [ ] [Skill 2]
- [ ] [Skill 3]

### Architecture
[Describe the technical approach]

### Database Changes
```sql
-- Add new table or modify existing
CREATE TABLE feature_table (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### API Endpoints
```typescript
// POST /api/feature
interface CreateFeatureRequest {
  field1: string;
  field2: number;
}

interface FeatureResponse {
  success: boolean;
  data?: Feature;
  error?: string;
}
```

### Frontend Components
- `FeatureList` - Display list of features
- `FeatureDetail` - Show feature details
- `FeatureForm` - Create/edit feature

## Implementation Checklist

### Backend
- [ ] Create database migration
- [ ] Create Prisma schema
- [ ] Create API route handlers
- [ ] Add input validation (Zod)
- [ ] Implement business logic
- [ ] Add error handling
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Update API documentation

### Frontend
- [ ] Create components
- [ ] Add form validation
- [ ] Implement API integration
- [ ] Add loading states
- [ ] Add error handling
- [ ] Add success messages
- [ ] Write component tests
- [ ] Update UI documentation

### Security
- [ ] Authentication required?
- [ ] Authorization rules
- [ ] Input sanitization
- [ ] Rate limiting
- [ ] CSRF protection

### Testing Scenarios
1. Happy path: [Describe]
2. Error case 1: [Describe]
3. Error case 2: [Describe]
4. Edge case: [Describe]

## Dependencies
- Depends on: [Other features/tasks]
- Blocks: [Features that depend on this]

## Deployment Notes
- [ ] Environment variables needed
- [ ] Database migration required
- [ ] Cache invalidation needed
- [ ] Feature flag required
- [ ] Rollback plan documented

## Documentation Updates
- [ ] API documentation
- [ ] User guide
- [ ] Technical documentation
- [ ] Changelog entry

---

**Claude Instructions:**
When implementing this feature:
1. Follow the technical approach outlined above
2. Use the specified skills
3. Implement all items in the checklist
4. Write comprehensive tests
5. Update all documentation