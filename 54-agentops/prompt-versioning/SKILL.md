---
name: Prompt Versioning
description: Comprehensive guide to versioning, testing, and managing prompts for AI agents including A/B testing, rollback strategies, and prompt registries
---

# Prompt Versioning

## Why Version Prompts?

**Problem:** Prompts change frequently, need to track what works

### Without Versioning
```
Change prompt → Deploy → Breaks agent → No way to rollback
```

### With Versioning
```
Change prompt → Test → Deploy v2 → Issues? → Rollback to v1
```

---

## Versioning Strategies

### Semantic Versioning
```
v1.0.0: Initial prompt
v1.1.0: Add new instruction (minor change)
v1.1.1: Fix typo (patch)
v2.0.0: Complete rewrite (major change)
```

### Git-Based Versioning
```
prompts/
├── agent_system_prompt.md
├── tool_selection_prompt.md
└── response_format_prompt.md

Git commit: abc123 → Prompt version
```

### Timestamp Versioning
```
prompt_v20240116_120000
prompt_v20240116_130000
```

---

## Prompt Registry

### Database Schema
```sql
CREATE TABLE prompts (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    version VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB,
    created_by VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    is_active BOOLEAN DEFAULT FALSE,
    UNIQUE(name, version)
);

CREATE INDEX idx_name_active ON prompts(name, is_active);
```

### Store Prompt
```python
def save_prompt(name, version, content, metadata=None):
    db.execute("""
        INSERT INTO prompts (name, version, content, metadata, created_by)
        VALUES (%s, %s, %s, %s, %s)
    """, (name, version, content, json.dumps(metadata), current_user))

# Example
save_prompt(
    name="agent_system_prompt",
    version="v1.2.0",
    content="You are a helpful assistant...",
    metadata={
        "description": "Added multi-language support",
        "tested_on": "2024-01-16"
    }
)
```

### Retrieve Prompt
```python
def get_prompt(name, version=None):
    if version:
        # Get specific version
        return db.query_one("""
            SELECT content FROM prompts
            WHERE name = %s AND version = %s
        """, (name, version))
    else:
        # Get active version
        return db.query_one("""
            SELECT content FROM prompts
            WHERE name = %s AND is_active = TRUE
        """, (name,))

# Usage
prompt = get_prompt("agent_system_prompt")  # Active version
prompt_v1 = get_prompt("agent_system_prompt", "v1.0.0")  # Specific version
```

---

## A/B Testing Prompts

### Traffic Splitting
```python
import random

def get_prompt_variant(name, user_id):
    # Consistent assignment (same user always gets same variant)
    if hash(user_id) % 2 == 0:
        return get_prompt(name, version="v1.0.0")  # Control
    else:
        return get_prompt(name, version="v2.0.0")  # Treatment

# Usage
prompt = get_prompt_variant("agent_system_prompt", user_id="user_123")
```

### Measure Performance
```python
def log_prompt_performance(version, user_id, success, duration_ms):
    db.execute("""
        INSERT INTO prompt_metrics (version, user_id, success, duration_ms)
        VALUES (%s, %s, %s, %s)
    """, (version, user_id, success, duration_ms))

# Analyze results
def compare_prompt_versions(version_a, version_b):
    results = db.query("""
        SELECT
            version,
            COUNT(*) as total,
            SUM(CASE WHEN success THEN 1 ELSE 0 END) as successes,
            AVG(duration_ms) as avg_duration
        FROM prompt_metrics
        WHERE version IN (%s, %s)
        GROUP BY version
    """, (version_a, version_b))
    
    return results
```

---

## Rollback Strategy

### Activate Previous Version
```python
def rollback_prompt(name, to_version):
    # Deactivate current
    db.execute("""
        UPDATE prompts
        SET is_active = FALSE
        WHERE name = %s AND is_active = TRUE
    """, (name,))
    
    # Activate target version
    db.execute("""
        UPDATE prompts
        SET is_active = TRUE
        WHERE name = %s AND version = %s
    """, (name, to_version))
    
    log_event(f"Rolled back {name} to {to_version}")

# Usage
rollback_prompt("agent_system_prompt", "v1.0.0")
```

### Automated Rollback
```python
def monitor_and_rollback(name, current_version, previous_version, threshold=0.8):
    # Check success rate
    success_rate = db.query_one("""
        SELECT
            SUM(CASE WHEN success THEN 1 ELSE 0 END)::float / COUNT(*)
        FROM prompt_metrics
        WHERE version = %s
          AND created_at > NOW() - INTERVAL '1 hour'
    """, (current_version,))
    
    if success_rate < threshold:
        rollback_prompt(name, previous_version)
        send_alert(f"Auto-rolled back {name} (success rate: {success_rate:.2%})")
```

---

## Prompt Templates

### Jinja2 Templates
```python
from jinja2 import Template

# Template with variables
template_str = """
You are a {{ role }} assistant.

User's language: {{ language }}
User's preferences: {{ preferences }}

Instructions:
{% for instruction in instructions %}
- {{ instruction }}
{% endfor %}
"""

template = Template(template_str)

# Render prompt
prompt = template.render(
    role="helpful",
    language="English",
    preferences="concise responses",
    instructions=["Be polite", "Provide examples", "Cite sources"]
)
```

### Version Templates
```python
def save_prompt_template(name, version, template_str, variables):
    db.execute("""
        INSERT INTO prompt_templates (name, version, template, variables)
        VALUES (%s, %s, %s, %s)
    """, (name, version, template_str, json.dumps(variables)))

def render_prompt(name, version, **kwargs):
    template_str = db.query_one("""
        SELECT template FROM prompt_templates
        WHERE name = %s AND version = %s
    """, (name, version))
    
    template = Template(template_str)
    return template.render(**kwargs)
```

---

## Testing Prompts

### Unit Tests
```python
def test_prompt_generates_valid_json():
    prompt = get_prompt("json_output_prompt", "v1.0.0")
    response = llm.generate(prompt + "\nGenerate user profile")
    
    # Verify JSON format
    try:
        data = json.loads(response)
        assert "name" in data
        assert "email" in data
    except:
        pytest.fail("Response is not valid JSON")

def test_prompt_follows_instructions():
    prompt = get_prompt("concise_prompt", "v1.0.0")
    response = llm.generate(prompt + "\nExplain quantum computing")
    
    # Verify conciseness (< 100 words)
    word_count = len(response.split())
    assert word_count < 100, f"Response too long: {word_count} words"
```

### Regression Tests
```python
# Golden dataset
test_cases = [
    {"input": "Book a flight", "expected_tool": "search_flights"},
    {"input": "What's the weather?", "expected_tool": "get_weather"},
    {"input": "Send an email", "expected_tool": "send_email"}
]

def test_prompt_regression(version):
    prompt = get_prompt("tool_selection_prompt", version)
    
    for case in test_cases:
        response = llm.generate(prompt + f"\nUser: {case['input']}")
        tool = extract_tool_from_response(response)
        
        assert tool == case["expected_tool"], \
            f"Expected {case['expected_tool']}, got {tool}"
```

---

## Prompt Optimization

### Track Metrics
```python
def track_prompt_metrics(version, tokens_used, cost, latency_ms, success):
    db.execute("""
        INSERT INTO prompt_metrics
        (version, tokens_used, cost, latency_ms, success)
        VALUES (%s, %s, %s, %s, %s)
    """, (version, tokens_used, cost, latency_ms, success))

# Analyze
def get_prompt_stats(version):
    return db.query_one("""
        SELECT
            AVG(tokens_used) as avg_tokens,
            AVG(cost) as avg_cost,
            AVG(latency_ms) as avg_latency,
            SUM(CASE WHEN success THEN 1 ELSE 0 END)::float / COUNT(*) as success_rate
        FROM prompt_metrics
        WHERE version = %s
    """, (version,))
```

### Optimize for Cost
```python
# Shorter prompt = fewer tokens = lower cost
# v1.0.0: 500 tokens
# v1.1.0: 300 tokens (optimized, same quality)

# Compare costs
v1_cost = get_prompt_stats("v1.0.0")["avg_cost"]
v2_cost = get_prompt_stats("v1.1.0")["avg_cost"]
savings = (v1_cost - v2_cost) / v1_cost

print(f"Cost savings: {savings:.1%}")
```

---

## Best Practices

### 1. Version Every Change
```python
# Good
save_prompt("agent_prompt", "v1.1.0", new_content)

# Bad
# Overwrite without versioning
```

### 2. Test Before Deploying
```python
# Good
test_prompt("v1.1.0")  # Run tests
if tests_pass:
    activate_prompt("agent_prompt", "v1.1.0")

# Bad
activate_prompt("agent_prompt", "v1.1.0")  # No testing
```

### 3. A/B Test Major Changes
```python
# Good
# Deploy v2.0.0 to 10% of users
# Monitor for 24 hours
# If good, increase to 100%

# Bad
# Deploy v2.0.0 to 100% immediately
```

### 4. Keep Prompt History
```python
# Good
# Never delete old versions
# Can always rollback

# Bad
# Delete old versions (can't rollback)
```

### 5. Document Changes
```python
save_prompt(
    name="agent_prompt",
    version="v1.1.0",
    content=new_content,
    metadata={
        "changes": "Added multi-language support",
        "tested_by": "john@example.com",
        "approved_by": "jane@example.com"
    }
)
```

---

## Tools

### LangSmith
```python
from langsmith import Client

client = Client()

# Create prompt
client.create_prompt(
    prompt_name="agent_system_prompt",
    prompt_template="You are a helpful assistant...",
    is_public=False
)

# Get prompt
prompt = client.pull_prompt("agent_system_prompt")

# Version automatically managed
```

### PromptLayer
```python
import promptlayer

promptlayer.api_key = "..."

# Track prompt
response = promptlayer.openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "system", "content": prompt}],
    pl_tags=["agent_v1.0.0"]
)

# View in PromptLayer dashboard
```

---

## Summary

**Prompt Versioning:** Track and manage prompt changes

**Strategies:**
- Semantic versioning (v1.0.0)
- Git-based (commit hash)
- Timestamp (v20240116)

**Prompt Registry:**
- Store prompts in database
- Track versions
- Mark active version

**A/B Testing:**
- Split traffic between versions
- Measure performance
- Deploy winner

**Rollback:**
- Activate previous version
- Automated rollback on failures

**Testing:**
- Unit tests (format, instructions)
- Regression tests (golden dataset)

**Best Practices:**
- Version every change
- Test before deploying
- A/B test major changes
- Keep history
- Document changes
