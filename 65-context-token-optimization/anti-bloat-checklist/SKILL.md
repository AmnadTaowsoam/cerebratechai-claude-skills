---
name: Anti-Bloat Checklist
description: Checklist สำหรับตรวจสอบและกำจัด bloat ใน context, prompt, และ response เพื่อลด token cost และเพิ่ม signal-to-noise ratio
---

# Anti-Bloat Checklist

## Overview

Checklist สำหรับตรวจสอบว่า context/prompt/response มี "bloat" หรือไม่ - ข้อมูลที่ไม่จำเป็น ซ้ำซ้อน หรือกิน token โดยไม่เพิ่ม value

## Why This Matters

- **Token cost**: ทุก token มีค่าใช้จ่าย
- **Context limit**: Window มีจำกัด ใช้ให้คุ้ม
- **Signal-to-noise**: Bloat ทำให้ AI หลุด focus
- **Speed**: น้อย token = response เร็วขึ้น

---

## Common Bloat Types

### 1. Filler Words
```
❌ Bloat:
"Basically, I think we should essentially try to implement this feature"

✅ Clean:
"Implement this feature"

Common fillers:
- basically, essentially, actually
- just, simply, really
- kind of, sort of
- very, quite, rather
```

### 2. Redundancy
```
❌ Bloat:
"The API endpoint returns a JSON response in JSON format"

✅ Clean:
"The API returns JSON"

Redundant patterns:
- "JSON response in JSON format"
- "database DB"
- "API endpoint API"
- Repeating same info in multiple places
```

### 3. Unnecessary Context
```
❌ Bloat:
Including entire file when only need 10 lines

✅ Clean:
Include only relevant snippet with line numbers

Example:
"See lines 45-55 in auth.ts for implementation"
```

---

## Prompt Bloat Detection

### Verbose Instructions
```
❌ Bloat (87 tokens):
"I would like you to please help me write a function that can calculate 
the sum of two numbers. Could you please make sure to include proper 
error handling and also add some comments explaining what the code does? 
Thank you very much for your assistance."

✅ Clean (15 tokens):
"Write a function to sum two numbers. Include error handling and comments."

Savings: 72 tokens (83%)
```

### Over-Explanation
```
❌ Bloat:
"I need this because we're building a calculator app and users need to 
add numbers together. This is a critical feature for our MVP..."

✅ Clean:
"Write a sum function for calculator app"

Rule: Don't explain WHY unless it affects HOW
```

### Repeated Instructions
```
❌ Bloat:
"Use TypeScript. Make it type-safe. Add TypeScript types. Ensure type safety."

✅ Clean:
"Use TypeScript with strict types"

Rule: Say it once, clearly
```

---

## Context Bloat Detection

### Irrelevant Files
```
❌ Bloat:
Including package.json, tsconfig.json, README.md for simple bug fix

✅ Clean:
Include only the file with the bug

Question to ask:
"Will AI need this to complete the task?"
If no → exclude
```

### Stale Information
```
❌ Bloat:
Including old implementation that was replaced

✅ Clean:
Include only current implementation

Check:
- Is this code still used?
- Is this doc still accurate?
- Is this comment still relevant?
```

### Full Files vs Snippets
```
❌ Bloat:
Entire 500-line file when only need 1 function

✅ Clean:
Extract relevant function + imports

Example:
```typescript
// From auth.ts lines 45-60
export function validateToken(token: string): boolean {
  // implementation
}
```
```

---

## Response Bloat Prevention

### Concise Instructions
```
Add to prompt:
"Be concise. No preambles. Direct answers only."

Example:
❌ "Here's what I did: First, I analyzed your code and then..."
✅ "Fixed by adding null check at line 45"
```

### Output Limits
```
Specify constraints:
"Max 100 words"
"Code only, no explanation"
"Summary in 3 bullet points"

Example:
"Explain in ≤50 words"
```

### Format Specification
```
❌ Bloat:
"Explain the changes you made and why, then show the code, 
then explain how to test it..."

✅ Clean:
"Output format:
1. Changed: [one line]
2. Code: [code block]
3. Test: [command]"
```

---

## Documentation Bloat

### Obvious Statements
```
❌ Bloat:
"This document describes the API documentation for our API"
"The database stores data in a database"

✅ Clean:
"API Documentation"
"Database Schema"

Rule: No meta-documentation
```

### Filler Paragraphs
```
❌ Bloat:
"In this section, we will discuss the various aspects of authentication 
and authorization, including but not limited to..."

✅ Clean:
"## Authentication
- JWT tokens
- OAuth 2.0
- Session management"

Rule: Tables and lists > prose
```

### Excessive Examples
```
❌ Bloat:
10 examples showing same pattern

✅ Clean:
1-2 examples covering edge cases

Rule: Examples should teach, not repeat
```

---

## Code Comment Bloat

### Obvious Comments
```typescript
❌ Bloat:
// Increment counter by 1
counter++;

// Return the result
return result;

✅ Clean:
counter++;
return result;

Rule: Comment WHY, not WHAT
```

### Dead Code
```typescript
❌ Bloat:
// Old implementation (deprecated)
// function oldCalculate() { ... }

// TODO: Remove this later
// const unused = 123;

✅ Clean:
[Delete it]

Rule: Delete, don't comment out
```

### Verbose Variable Names
```typescript
❌ Bloat:
const userAuthenticationTokenExpirationTimeInMilliseconds = 3600000;

✅ Clean:
const tokenExpiryMs = 3600000;

Rule: Clear but concise
```

---

## Configuration Bloat

### Unused Configs
```json
❌ Bloat:
{
  "feature_a": true,
  "feature_b": false,  // Never used
  "feature_c": null,   // Deprecated
  "debug_mode": false  // Default value
}

✅ Clean:
{
  "feature_a": true
}

Rule: Only non-default, actively used configs
```

### Default Values
```
❌ Bloat:
Explicitly setting every default

✅ Clean:
Only override non-defaults

Example:
// Don't include if it's the default
timeout: 30000  // ← This is default, skip it
```

---

## Measurement & Tracking

### Token Budgets
```typescript
// Define budgets
const TOKEN_BUDGETS = {
  systemPrompt: 200,
  userPrompt: 150,
  contextPerFile: 500,
  totalContext: 4000,
  maxResponse: 1000
};

// Track usage
function trackTokens(content: string, type: string) {
  const tokens = countTokens(content);
  const budget = TOKEN_BUDGETS[type];
  
  if (tokens > budget) {
    console.warn(`${type} exceeds budget: ${tokens}/${budget}`);
  }
  
  return tokens;
}
```

### Bloat Metrics
```typescript
interface BloatMetrics {
  avgPromptTokens: number;
  avgContextTokens: number;
  avgResponseTokens: number;
  bloatPercentage: number;  // Estimated waste
  costPerRequest: number;
}

// Calculate bloat
function calculateBloat(before: number, after: number): number {
  return ((before - after) / before) * 100;
}

// Example:
// Before optimization: 2000 tokens
// After optimization: 800 tokens
// Bloat removed: 60%
```

---

## Anti-Bloat Checklist

### Prompt Review
```
☐ No "Please" or "Could you" (use imperative)
☐ No explanation of why task is needed
☐ No repeated instructions
☐ Output format specified once, clearly
☐ Examples only if truly needed (≤2)
☐ Under 150 tokens for simple tasks
☐ No filler words (basically, essentially)
☐ Active voice, not passive
```

### Context Review
```
☐ Only files directly relevant to task
☐ No entire files when snippets suffice
☐ No outdated/stale information
☐ No redundant documentation
☐ Context budget defined and followed
☐ Total context under 50% of window
☐ No duplicate information across files
☐ Removed commented-out code
```

### Response Review
```
☐ No "Here's what I did:" preambles
☐ No repetition of the question
☐ No unnecessary caveats
☐ Code without excessive comments
☐ Direct answers, no padding
☐ Summary at top if long response
☐ No filler words or hedge words
☐ Specified max length followed
```

### Documentation Review
```
☐ No "This document describes..."
☐ No obvious statements
☐ No filler paragraphs
☐ Tables over prose where applicable
☐ Links over inline duplication
☐ Max 500 words per topic
☐ Examples are necessary, not redundant
☐ No meta-documentation
```

### Code Review
```
☐ No comments stating the obvious
☐ No commented-out code
☐ No dead code
☐ No verbose variable names (within reason)
☐ No unnecessary type annotations
☐ No copy-paste with minor variations
☐ Removed unused imports
☐ Removed unused variables
```

---

## Bloat Audit Process

### Step 1: Measure Current Usage
```typescript
// Collect baseline metrics
const baseline = {
  avgPromptTokens: measureAverage(prompts),
  avgContextTokens: measureAverage(contexts),
  avgResponseTokens: measureAverage(responses),
  totalCost: calculateCost(allTokens)
};

console.log('Baseline:', baseline);
```

### Step 2: Identify Top Bloat Sources
```typescript
// Find biggest offenders
const analysis = {
  longestPrompts: prompts.sort((a, b) => b.tokens - a.tokens).slice(0, 10),
  mostIncludedFiles: countFileInclusions(),
  repeatedContent: findDuplicates(),
  fillerWordCount: countFillerWords()
};
```

### Step 3: Apply Checklist
```
For each item:
1. Review against checklist
2. Mark violations
3. Calculate potential savings
4. Prioritize by impact
```

### Step 4: Implement Fixes
```
High-impact fixes first:
1. Remove entire unnecessary files
2. Replace full files with snippets
3. Rewrite verbose prompts
4. Add output constraints
5. Remove filler words
```

### Step 5: Measure Improvement
```typescript
const after = {
  avgPromptTokens: measureAverage(optimizedPrompts),
  avgContextTokens: measureAverage(optimizedContexts),
  avgResponseTokens: measureAverage(optimizedResponses),
  totalCost: calculateCost(allOptimizedTokens)
};

const improvement = {
  tokensSaved: baseline.totalTokens - after.totalTokens,
  costSaved: baseline.totalCost - after.totalCost,
  percentageReduction: calculateBloat(baseline.totalTokens, after.totalTokens)
};

console.log('Improvement:', improvement);
// Example: 60% reduction, $500/month saved
```

---

## Token Budget Guidelines

| Content Type | Max Tokens | Notes |
|--------------|------------|-------|
| System prompt | 200 | Core instructions only |
| User prompt | 150 | Task + context ref |
| Context per file | 500 | Snippet, not whole file |
| Total context | 4000 | For 8k window (50%) |
| Response | 1000 | Unless explicitly needed |
| Documentation | 300 | Per section |

---

## Quick Wins

### 1. Remove Filler Words
```
Find and replace:
- "basically" → ""
- "essentially" → ""
- "just" → ""
- "simply" → ""
- "really" → ""

Typical savings: 5-10%
```

### 2. Use Imperative Mood
```
❌ "Could you please write..."
✅ "Write..."

❌ "I would like you to..."
✅ "Create..."

Savings: 30-50% in prompts
```

### 3. Snippets Over Full Files
```
❌ Include entire 500-line file
✅ Include 20-line relevant function

Savings: 90%+ per file
```

---

## Summary

**Anti-Bloat:** กำจัดข้อมูลไม่จำเป็นเพื่อลด token cost

**Common Bloat:**
- Filler words
- Redundancy
- Unnecessary context
- Verbose instructions
- Obvious comments

**Quick Wins:**
- Remove filler words (5-10% savings)
- Use imperative mood (30-50% savings)
- Snippets over full files (90%+ savings)

**Process:**
1. Measure baseline
2. Identify bloat sources
3. Apply checklist
4. Implement fixes
5. Measure improvement

**Target:**
- 50-60% token reduction typical
- Maintain or improve quality
- Faster responses
- Lower costs
