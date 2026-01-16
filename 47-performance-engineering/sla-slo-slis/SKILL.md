---
name: SLA, SLO, and SLIs
description: Comprehensive guide to Service Level Agreements, Objectives, and Indicators for measuring and maintaining system reliability
---

# SLA, SLO, and SLIs

## Definitions

### SLA (Service Level Agreement)

**What:** Contract with consequences (legal/financial)

**Example:**
> "We guarantee 99.9% uptime. If we fail to meet this, you get a 10% credit."

**Characteristics:**
- External promise to customers
- Legal/financial consequences
- Conservative (easier to meet)
- Typically 99.5% - 99.9%

### SLO (Service Level Objective)

**What:** Internal target (more strict than SLA)

**Example:**
> "Our internal target is 99.95% uptime (stricter than our 99.9% SLA)."

**Characteristics:**
- Internal goal
- No legal consequences
- More ambitious than SLA
- Provides buffer before SLA breach
- Typically 99.9% - 99.99%

### SLI (Service Level Indicator)

**What:** Actual measurement

**Example:**
> "Last month, we achieved 99.97% uptime."

**Characteristics:**
- Quantitative metric
- Measured continuously
- Compared against SLO
- Examples: Availability, latency, error rate

---

## Why SLOs Matter

### 1. Quantify Reliability

**Before SLOs:**
> "Our system is pretty reliable."

**With SLOs:**
> "We have 99.95% availability, P95 latency of 150ms, and 0.1% error rate."

### 2. Balance Reliability vs Velocity

**Problem:**
- 100% reliability = no innovation (too risky to deploy)
- 0% reliability = no users (system always down)

**Solution:**
- SLOs define "good enough" reliability
- Error budget allows controlled risk-taking

### 3. Error Budget Concept

**Formula:**
```
Error Budget = 100% - SLO
```

**Example:**
- SLO: 99.9% uptime
- Error Budget: 0.1% downtime
- Per month: 43.2 minutes of allowed downtime

**Usage:**
- **Budget remaining:** Deploy new features, take risks
- **Budget exhausted:** Freeze deployments, focus on reliability

### 4. Prioritize Work (What to Improve)

**Without SLOs:**
> "We should improve everything!"

**With SLOs:**
> "We're meeting our latency SLO but missing our availability SLO. Focus on availability."

---

## Common SLIs

### 1. Availability: % of Successful Requests

**Formula:**
```
Availability = (Successful Requests / Total Requests) × 100%
```

**Example:**
```
Total Requests: 1,000,000
Successful (2xx, 3xx): 999,500
Failed (4xx, 5xx): 500

Availability = (999,500 / 1,000,000) × 100% = 99.95%
```

**SLO Example:**
> "99.9% of requests return 2xx or 3xx status codes."

### 2. Latency: % of Requests Under Threshold

**Formula:**
```
Latency SLI = (Requests < Threshold / Total Requests) × 100%
```

**Example:**
```
Total Requests: 1,000,000
Requests < 200ms: 950,000
Requests ≥ 200ms: 50,000

P95 Latency SLI = (950,000 / 1,000,000) × 100% = 95%
```

**SLO Example:**
> "95% of requests complete in < 200ms (P95 latency)."

**Why P95/P99 (Not Average):**
- Average hides outliers
- P95 = 95% of users have good experience
- P99 = 99% of users have good experience

### 3. Throughput: Requests Per Second

**Formula:**
```
Throughput = Total Requests / Time Period
```

**Example:**
```
Total Requests: 3,600,000
Time Period: 1 hour (3600 seconds)

Throughput = 3,600,000 / 3600 = 1000 req/s
```

**SLO Example:**
> "System handles at least 1000 req/s."

### 4. Error Rate: % of Failed Requests

**Formula:**
```
Error Rate = (Failed Requests / Total Requests) × 100%
```

**Example:**
```
Total Requests: 1,000,000
Failed (5xx): 1,000

Error Rate = (1,000 / 1,000,000) × 100% = 0.1%
```

**SLO Example:**
> "Error rate < 0.1% (99.9% success rate)."

### 5. Freshness: Data Age for Analytics

**Formula:**
```
Freshness = % of Data Updated Within Threshold
```

**Example:**
```
Total Records: 10,000
Updated < 5 min ago: 9,900
Updated ≥ 5 min ago: 100

Freshness = (9,900 / 10,000) × 100% = 99%
```

**SLO Example:**
> "99% of analytics data is fresh within 5 minutes."

---

## Choosing Good SLIs

### 1. User-Centric (Not System-Centric)

**Bad (System-Centric):**
> "CPU usage < 80%"

**Good (User-Centric):**
> "95% of API requests complete in < 200ms"

**Why:**
- Users care about response time, not CPU usage
- System metrics are means, not ends

### 2. Measurable

**Bad (Not Measurable):**
> "System is fast"

**Good (Measurable):**
> "P95 latency < 200ms"

### 3. Actionable

**Bad (Not Actionable):**
> "Users are happy"

**Good (Actionable):**
> "Error rate < 0.1%"

**Why:**
- Can identify what to fix
- Can track improvement

### 4. Proportional to User Pain

**Example:**
- 1 failed request out of 1,000,000 = low pain
- 1,000 failed requests out of 1,000,000 = high pain

**SLI should reflect this:**
> "99.9% availability" (allows 0.1% failures)

---

## Setting SLO Targets

### 1. Historical Performance Baseline

**Process:**
1. Measure current performance for 30 days
2. Calculate P50, P95, P99
3. Set SLO slightly better than current P95

**Example:**
```
Current Performance:
- P50 latency: 50ms
- P95 latency: 180ms
- P99 latency: 450ms

SLO Target:
- P95 latency < 200ms (slightly better than current 180ms)
```

### 2. User Expectations

**Research:**
- User surveys
- Competitor benchmarks
- Industry standards

**Example:**
- Google: 53% of mobile users abandon sites that take > 3 seconds
- Target: P95 latency < 1 second for page load

### 3. Cost of Improvement

**Trade-off:**
- 99% → 99.9% = 10x cost
- 99.9% → 99.99% = 10x cost
- 99.99% → 99.999% = 10x cost

**Example:**
```
99% uptime:
- Downtime: 7.2 hours/month
- Cost: $10,000/month

99.9% uptime:
- Downtime: 43 minutes/month
- Cost: $100,000/month (10x)

99.99% uptime:
- Downtime: 4.3 minutes/month
- Cost: $1,000,000/month (100x)
```

### 4. Industry Standards

**Common SLO Targets:**

| Service Type | Availability | Latency (P95) |
|--------------|--------------|---------------|
| **Internal API** | 99.9% | < 200ms |
| **Public API** | 99.95% | < 500ms |
| **E-commerce** | 99.99% | < 1s |
| **Payments** | 99.999% | < 100ms |
| **Analytics** | 99% | < 5s |

---

## SLO Examples

### Example 1: API Availability

**SLO:**
> "99.9% of API requests return 2xx or 3xx status codes over a 30-day window."

**Measurement:**
```
Total Requests (30 days): 100,000,000
Successful (2xx, 3xx): 99,950,000
Failed (4xx, 5xx): 50,000

Availability = 99.95% ✅ (meets 99.9% SLO)
```

### Example 2: Latency

**SLO:**
> "95% of API requests complete in < 200ms (P95 latency)."

**Measurement:**
```
Total Requests: 1,000,000
Requests < 200ms: 960,000
Requests ≥ 200ms: 40,000

P95 Latency SLI = 96% ✅ (meets 95% SLO)
```

### Example 3: Search Quality

**SLO:**
> "99% of searches return results in < 500ms."

**Measurement:**
```
Total Searches: 10,000,000
Searches < 500ms: 9,920,000
Searches ≥ 500ms: 80,000

Search Latency SLI = 99.2% ✅ (meets 99% SLO)
```

### Example 4: Data Freshness

**SLO:**
> "Data is fresh within 5 minutes 99% of the time."

**Measurement:**
```
Total Data Points: 1,000,000
Fresh (< 5 min): 995,000
Stale (≥ 5 min): 5,000

Freshness SLI = 99.5% ✅ (meets 99% SLO)
```

---

## Error Budgets

### Concept

**Definition:**
> Error budget is the amount of unreliability you can tolerate while still meeting your SLO.

**Formula:**
```
Error Budget = 100% - SLO
```

### Example Calculation

**SLO:** 99.9% uptime over 30 days

**Error Budget:**
```
Error Budget = 100% - 99.9% = 0.1%

30 days = 30 × 24 × 60 = 43,200 minutes
0.1% of 43,200 minutes = 43.2 minutes

Error Budget = 43.2 minutes of downtime per month
```

### Usage

**Scenario 1: Budget Remaining**
```
Error Budget: 43.2 minutes/month
Used: 10 minutes
Remaining: 33.2 minutes

Action: Can deploy new features, take risks
```

**Scenario 2: Budget Exhausted**
```
Error Budget: 43.2 minutes/month
Used: 45 minutes
Remaining: -1.8 minutes (over budget!)

Action: Freeze deployments, focus on reliability
```

### Error Budget Policy

**Example Policy:**

| Budget Remaining | Actions |
|------------------|---------|
| **> 50%** | Deploy freely, innovate |
| **25% - 50%** | Deploy with caution, increase testing |
| **10% - 25%** | Freeze non-critical deployments |
| **< 10%** | Freeze all deployments, incident response mode |

---

## Measuring SLIs

### 1. Request Logs (Success/Failure)

**Example (Node.js):**
```javascript
let totalRequests = 0;
let successfulRequests = 0;

app.use((req, res, next) => {
  totalRequests++;
  
  res.on('finish', () => {
    if (res.statusCode >= 200 && res.statusCode < 400) {
      successfulRequests++;
    }
  });
  
  next();
});

// Calculate SLI
app.get('/metrics', (req, res) => {
  const availability = (successfulRequests / totalRequests) * 100;
  res.json({
    totalRequests,
    successfulRequests,
    availability: availability.toFixed(2) + '%'
  });
});
```

### 2. Latency Percentiles (P50, P95, P99)

**Example (Prometheus):**
```javascript
const promClient = require('prom-client');

const httpRequestDuration = new promClient.Histogram({
  name: 'http_request_duration_ms',
  help: 'Duration of HTTP requests in ms',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [10, 50, 100, 200, 500, 1000, 2000, 5000]
});

app.use((req, res, next) => {
  const start = Date.now();
  
  res.on('finish', () => {
    const duration = Date.now() - start;
    httpRequestDuration.labels(req.method, req.route?.path || req.path, res.statusCode).observe(duration);
  });
  
  next();
});

// Query P95 latency in Prometheus:
// histogram_quantile(0.95, rate(http_request_duration_ms_bucket[5m]))
```

### 3. Synthetic Monitoring (External Probes)

**Example (Uptime Robot, Pingdom):**
```
External probe every 1 minute:
- Send request to https://api.example.com/health
- Record response time and status code
- Alert if down or slow
```

**Benefits:**
- Measures user experience (from outside)
- Detects issues before users report them
- Geographic distribution (measure from multiple locations)

### 4. Real User Monitoring (RUM)

**Example (Browser):**
```javascript
// Measure page load time
window.addEventListener('load', () => {
  const perfData = performance.timing;
  const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
  
  // Send to analytics
  fetch('/api/metrics', {
    method: 'POST',
    body: JSON.stringify({
      metric: 'page_load_time',
      value: pageLoadTime
    })
  });
});
```

**Benefits:**
- Real user data (not synthetic)
- Captures actual user experience
- Includes network latency, device performance

---

## SLO Dashboards

### Key Components

1. **Current SLI Value**
   - Real-time measurement
   - Example: "99.95% availability"

2. **SLO Target Line**
   - Visual indicator of target
   - Example: Horizontal line at 99.9%

3. **Error Budget Remaining**
   - How much budget is left
   - Example: "32.1 minutes remaining (74%)"

4. **Trend Over Time**
   - Historical SLI values
   - Example: Line chart of last 30 days

5. **Burn Rate**
   - How fast budget is consumed
   - Example: "Burning at 2x normal rate"

### Example Dashboard (Grafana)

```json
{
  "dashboard": {
    "title": "API SLO Dashboard",
    "panels": [
      {
        "title": "Availability SLI",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{status=~\"2..|3..\"}[5m])) / sum(rate(http_requests_total[5m])) * 100"
          }
        ],
        "thresholds": [
          { "value": 99.9, "color": "green" },
          { "value": 99.5, "color": "yellow" },
          { "value": 0, "color": "red" }
        ]
      },
      {
        "title": "P95 Latency",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_ms_bucket[5m]))"
          }
        ],
        "thresholds": [
          { "value": 200, "color": "green" },
          { "value": 500, "color": "yellow" },
          { "value": 1000, "color": "red" }
        ]
      },
      {
        "title": "Error Budget Remaining",
        "targets": [
          {
            "expr": "(1 - (1 - 0.999) - (1 - sum(rate(http_requests_total{status=~\"2..|3..\"}[30d])) / sum(rate(http_requests_total[30d])))) / (1 - 0.999) * 100"
          }
        ]
      }
    ]
  }
}
```

---

## Alerting on SLOs

### 1. Don't Alert on Single Failed Request

**Bad:**
```
Alert: Single request failed!
```

**Why:**
- Too noisy
- Single failure is expected
- Wastes on-call time

### 2. Alert When Burning Budget Too Fast

**Good:**
```
Alert: Burning error budget at 10x normal rate!
```

**Why:**
- Indicates sustained problem
- Gives time to fix before SLO breach
- Actionable

### 3. Multi-Window, Multi-Burn-Rate Alerts

**Concept:**
- Short window (1 hour): Detect fast burns
- Long window (6 hours): Detect sustained issues
- Combination reduces false positives

**Example:**
```yaml
# Fast burn (1 hour window)
- alert: SLOFastBurn
  expr: |
    (
      1 - (
        sum(rate(http_requests_total{status=~"2..|3.."}[1h]))
        /
        sum(rate(http_requests_total[1h]))
      )
    ) > (1 - 0.999) * 10  # Burning at 10x rate
  for: 5m
  annotations:
    summary: "Fast error budget burn detected"

# Slow burn (6 hour window)
- alert: SLOSlowBurn
  expr: |
    (
      1 - (
        sum(rate(http_requests_total{status=~"2..|3.."}[6h]))
        /
        sum(rate(http_requests_total[6h]))
      )
    ) > (1 - 0.999) * 2  # Burning at 2x rate
  for: 30m
  annotations:
    summary: "Sustained error budget burn detected"
```

### 4. Focus on Sustained Problems

**Example:**
```
Alert if:
- Availability < 99.9% for 5 minutes (sustained)

Don't alert if:
- Single request failed (transient)
```

---

## SLO-Based Prioritization

### Decision Framework

**Scenario 1: Below SLO**
```
Current SLI: 99.85%
SLO: 99.9%
Status: ❌ Missing SLO

Action:
- Stop feature development
- Focus on reliability improvements
- Root cause analysis
- Incident postmortems
```

**Scenario 2: Above SLO**
```
Current SLI: 99.95%
SLO: 99.9%
Status: ✅ Meeting SLO

Action:
- Can take more risks
- Deploy new features
- Innovate faster
- Experiment with new technologies
```

**Scenario 3: Way Above SLO**
```
Current SLI: 99.99%
SLO: 99.9%
Status: ✅✅ Exceeding SLO

Action:
- Over-investing in reliability
- Could move faster
- Consider lowering SLO or increasing feature velocity
```

---

## Multi-Window Alerts

### Concept

**Problem:**
- Single window alerts are noisy or slow

**Solution:**
- Use multiple time windows
- Combine short and long windows

### Example

**Short Window (1 hour):**
- Detects fast burns
- High sensitivity
- May have false positives

**Long Window (6 hours):**
- Detects sustained issues
- Low sensitivity
- Fewer false positives

**Combined:**
```
Alert if:
  (Short window burn rate > 10x) OR (Long window burn rate > 2x)
```

### Burn Rate Table

| SLO | Error Budget | 1h Burn (10x) | 6h Burn (2x) |
|-----|--------------|---------------|--------------|
| 99.9% | 0.1% | 1% error rate | 0.2% error rate |
| 99.95% | 0.05% | 0.5% error rate | 0.1% error rate |
| 99.99% | 0.01% | 0.1% error rate | 0.02% error rate |

---

## Tools for SLO Management

### 1. Datadog SLO Tracking

**Features:**
- Visual SLO dashboard
- Error budget tracking
- Burn rate alerts
- Historical trends

**Configuration:**
```yaml
slos:
  - name: "API Availability"
    type: metric
    query: "sum:http.requests{status:2xx,status:3xx}.as_count() / sum:http.requests.as_count()"
    target: 99.9
    timeframe: 30d
```

### 2. Google Cloud SLO Monitoring

**Features:**
- Integrated with Cloud Monitoring
- Automatic SLI calculation
- Error budget alerts

**Configuration:**
```yaml
serviceLevelObjective:
  displayName: "API Availability SLO"
  serviceLevelIndicator:
    requestBased:
      goodTotalRatio:
        goodServiceFilter: "metric.type=\"loadbalancing.googleapis.com/https/request_count\" AND metric.label.response_code_class=\"2xx\""
        totalServiceFilter: "metric.type=\"loadbalancing.googleapis.com/https/request_count\""
  goal: 0.999
  rollingPeriod: 2592000s  # 30 days
```

### 3. Prometheus + Grafana (Custom)

**Prometheus Queries:**
```promql
# Availability SLI
sum(rate(http_requests_total{status=~"2..|3.."}[30d]))
/
sum(rate(http_requests_total[30d]))

# P95 Latency SLI
histogram_quantile(0.95, rate(http_request_duration_ms_bucket[30d]))

# Error Budget Remaining
(1 - (1 - 0.999) - (1 - availability_sli)) / (1 - 0.999) * 100
```

### 4. Nobl9, Rootly

**Features:**
- Dedicated SLO platforms
- Multi-cloud support
- Advanced alerting
- Error budget policies

---

## SLA vs SLO

### Relationship

```
┌─────────────────────────────────────┐
│  SLA: 99.5% (External Promise)      │
│  ↑                                  │
│  │ Buffer                           │
│  ↓                                  │
│  SLO: 99.9% (Internal Target)       │
│  ↑                                  │
│  │ Actual Performance               │
│  ↓                                  │
│  SLI: 99.95% (Measurement)          │
└─────────────────────────────────────┘
```

### Example

**SLA (External):**
> "We guarantee 99.5% uptime. If we fail, you get a 10% credit."

**SLO (Internal):**
> "Our internal target is 99.9% uptime."

**SLI (Measurement):**
> "Last month, we achieved 99.95% uptime."

**Analysis:**
- SLI (99.95%) > SLO (99.9%) ✅ Meeting internal target
- SLI (99.95%) > SLA (99.5%) ✅ Meeting customer promise
- Buffer: 99.9% - 99.5% = 0.4% (protects against SLA breach)

---

## Common Mistakes

### 1. Too Many SLOs

**Problem:**
- Tracking 50 SLOs
- Can't focus on what matters
- Alert fatigue

**Solution:**
- Focus on 3-5 key SLOs
- User-facing metrics only
- Example: Availability, Latency, Error Rate

### 2. SLOs That Don't Matter to Users

**Bad:**
> "CPU usage < 80%"

**Good:**
> "P95 latency < 200ms"

**Why:**
- Users don't care about CPU usage
- Users care about response time

### 3. SLO Targets Too Ambitious

**Problem:**
- SLO: 99.999% (five nines)
- Requires massive investment
- Slows down innovation

**Solution:**
- Start with achievable targets (99.9%)
- Increase gradually based on need
- Balance reliability vs velocity

### 4. No Error Budget Policy

**Problem:**
- SLO defined but no action when breached
- No consequences for missing SLO

**Solution:**
- Define clear error budget policy
- Example: "If budget < 10%, freeze deployments"

---

## Real-World SLO Examples

### Example 1: E-Commerce (Checkout)

**SLOs:**
1. **Availability:** 99.95% of checkout requests succeed
2. **Latency:** 95% of checkouts complete in < 2 seconds
3. **Error Rate:** < 0.05% payment failures

**Why:**
- Checkout is critical (revenue-generating)
- Higher SLO than other pages
- Stricter latency requirement

### Example 2: API Service

**SLOs:**
1. **Availability:** 99.9% of API requests return 2xx/3xx
2. **Latency:** 95% of requests complete in < 200ms (P95)
3. **Throughput:** Handle at least 1000 req/s

**Why:**
- Standard API SLOs
- Balances reliability and cost

### Example 3: Data Pipeline

**SLOs:**
1. **Freshness:** 99% of data updated within 5 minutes
2. **Completeness:** 99.9% of records processed successfully
3. **Availability:** 99% of pipeline runs succeed

**Why:**
- Freshness matters for analytics
- Some data loss acceptable (99.9%)
- Lower availability OK (batch processing)

---

## Implementation

### Prometheus Queries for SLIs

**Availability:**
```promql
# Availability SLI (last 30 days)
sum(rate(http_requests_total{status=~"2..|3.."}[30d]))
/
sum(rate(http_requests_total[30d]))
* 100
```

**P95 Latency:**
```promql
# P95 latency (last 30 days)
histogram_quantile(0.95, rate(http_request_duration_ms_bucket[30d]))
```

**Error Rate:**
```promql
# Error rate (last 30 days)
sum(rate(http_requests_total{status=~"5.."}[30d]))
/
sum(rate(http_requests_total[30d]))
* 100
```

**Error Budget Remaining:**
```promql
# Error budget remaining (%)
(1 - (1 - 0.999) - (1 - sum(rate(http_requests_total{status=~"2..|3.."}[30d])) / sum(rate(http_requests_total[30d])))) / (1 - 0.999) * 100
```

### Alert Rules

**prometheus-alerts.yml:**
```yaml
groups:
  - name: slo_alerts
    interval: 1m
    rules:
      # Fast burn (1 hour window)
      - alert: SLOFastBurn
        expr: |
          (
            1 - (
              sum(rate(http_requests_total{status=~"2..|3.."}[1h]))
              /
              sum(rate(http_requests_total[1h]))
            )
          ) > 0.01  # 1% error rate (10x burn for 99.9% SLO)
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Fast error budget burn detected"
          description: "Error budget burning at 10x normal rate"
      
      # Slow burn (6 hour window)
      - alert: SLOSlowBurn
        expr: |
          (
            1 - (
              sum(rate(http_requests_total{status=~"2..|3.."}[6h]))
              /
              sum(rate(http_requests_total[6h]))
            )
          ) > 0.002  # 0.2% error rate (2x burn for 99.9% SLO)
        for: 30m
        labels:
          severity: warning
        annotations:
          summary: "Sustained error budget burn detected"
          description: "Error budget burning at 2x normal rate"
      
      # SLO breach
      - alert: SLOBreach
        expr: |
          (
            sum(rate(http_requests_total{status=~"2..|3.."}[30d]))
            /
            sum(rate(http_requests_total[30d]))
          ) < 0.999
        for: 1h
        labels:
          severity: critical
        annotations:
          summary: "SLO breached"
          description: "Availability SLO (99.9%) not met over 30 days"
```

### Dashboard JSON (Grafana)

**grafana-slo-dashboard.json:**
```json
{
  "dashboard": {
    "title": "SLO Dashboard",
    "panels": [
      {
        "id": 1,
        "title": "Availability SLI",
        "type": "stat",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{status=~\"2..|3..\"}[30d])) / sum(rate(http_requests_total[30d])) * 100"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "percent",
            "thresholds": {
              "steps": [
                { "value": 0, "color": "red" },
                { "value": 99.5, "color": "yellow" },
                { "value": 99.9, "color": "green" }
              ]
            }
          }
        }
      },
      {
        "id": 2,
        "title": "Error Budget Remaining",
        "type": "gauge",
        "targets": [
          {
            "expr": "(1 - (1 - 0.999) - (1 - sum(rate(http_requests_total{status=~\"2..|3..\"}[30d])) / sum(rate(http_requests_total[30d])))) / (1 - 0.999) * 100"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "percent",
            "min": 0,
            "max": 100,
            "thresholds": {
              "steps": [
                { "value": 0, "color": "red" },
                { "value": 25, "color": "yellow" },
                { "value": 50, "color": "green" }
              ]
            }
          }
        }
      },
      {
        "id": 3,
        "title": "Availability Trend (30 days)",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{status=~\"2..|3..\"}[1h])) / sum(rate(http_requests_total[1h])) * 100",
            "legendFormat": "Availability"
          }
        ],
        "yaxes": [
          {
            "format": "percent",
            "min": 99,
            "max": 100
          }
        ],
        "alert": {
          "conditions": [
            {
              "evaluator": {
                "params": [99.9],
                "type": "lt"
              },
              "query": {
                "params": ["A", "5m", "now"]
              }
            }
          ]
        }
      }
    ]
  }
}
```

### Error Budget Calculation Script

**calculate-error-budget.js:**
```javascript
const prometheus = require('prom-client');

async function calculateErrorBudget(slo, windowDays = 30) {
  const gateway = new prometheus.Pushgateway('http://localhost:9091');
  
  // Query Prometheus
  const query = `
    sum(rate(http_requests_total{status=~"2..|3.."}[${windowDays}d]))
    /
    sum(rate(http_requests_total[${windowDays}d]))
  `;
  
  const response = await fetch(`http://localhost:9090/api/v1/query?query=${encodeURIComponent(query)}`);
  const data = await response.json();
  const availability = parseFloat(data.data.result[0].value[1]);
  
  // Calculate error budget
  const errorBudget = 1 - slo;
  const actualErrors = 1 - availability;
  const budgetRemaining = (errorBudget - actualErrors) / errorBudget * 100;
  
  console.log(`SLO: ${(slo * 100).toFixed(2)}%`);
  console.log(`Availability: ${(availability * 100).toFixed(2)}%`);
  console.log(`Error Budget: ${(errorBudget * 100).toFixed(2)}%`);
  console.log(`Budget Remaining: ${budgetRemaining.toFixed(2)}%`);
  
  return {
    slo,
    availability,
    errorBudget,
    budgetRemaining
  };
}

// Usage
calculateErrorBudget(0.999, 30);
```

---

## Summary

### Quick Reference

**Definitions:**
- **SLA:** External promise with consequences (99.5% - 99.9%)
- **SLO:** Internal target, stricter than SLA (99.9% - 99.99%)
- **SLI:** Actual measurement (e.g., 99.95%)

**Common SLIs:**
- Availability: % successful requests
- Latency: % requests under threshold (P95, P99)
- Error rate: % failed requests
- Throughput: Requests per second
- Freshness: Data age

**Error Budget:**
- Formula: `100% - SLO`
- Example: 99.9% SLO = 0.1% error budget = 43.2 min/month
- Use: Balance reliability vs velocity

**Best Practices:**
1. Focus on 3-5 key SLOs
2. User-centric metrics (not system metrics)
3. Set achievable targets (start with 99.9%)
4. Define error budget policy
5. Alert on burn rate (not single failures)
6. Use multi-window alerts (short + long)

**Tools:**
- Datadog SLO Tracking
- Google Cloud SLO Monitoring
- Prometheus + Grafana
- Nobl9, Rootly

**Common Mistakes:**
- Too many SLOs
- SLOs that don't matter to users
- Targets too ambitious (99.999%)
- No error budget policy

**SLO Examples:**
- API: 99.9% availability, P95 < 200ms
- E-commerce: 99.95% availability, P95 < 2s
- Analytics: 99% freshness within 5 min
