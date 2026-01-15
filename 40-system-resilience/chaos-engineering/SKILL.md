---
name: Chaos Engineering
description: Systematic approach to testing system resilience through controlled failure injection and experimentation
---

# Chaos Engineering

## Overview

Chaos Engineering is the discipline of experimenting on a system to build confidence in its capability to withstand turbulent conditions in production. By proactively injecting failures, you discover weaknesses before they cause outages.

**Core Principle**: "Break things on purpose to learn how to make them stronger."

## 1. Principles of Chaos Engineering

### The Netflix Origin Story

Netflix pioneered Chaos Engineering with **Chaos Monkey** (2011):
- Randomly terminates EC2 instances in production
- Forces engineers to build resilient services
- Runs during business hours (maximum learning)
- Cultural shift: failures are expected, not exceptional

### The Four Principles

```
1. Build a Hypothesis Around Steady State Behavior
   Define what "normal" looks like (metrics, SLIs)

2. Vary Real-World Events
   Inject failures that could actually happen

3. Run Experiments in Production
   Staging doesn't have real traffic patterns

4. Automate Experiments to Run Continuously
   Make chaos part of CI/CD
```

### Chaos Engineering vs Traditional Testing

| Traditional Testing | Chaos Engineering |
|---------------------|-------------------|
| Known failure scenarios | Unknown failure scenarios |
| Controlled environment | Production environment |
| Pass/fail assertions | Hypothesis validation |
| Pre-deployment | Continuous in production |
| Synthetic load | Real user traffic |

## 2. Hypothesis-Driven Experimentation

### Experiment Template

```markdown
# Chaos Experiment: [Name]

## Hypothesis
**Given**: [Current system state]
**When**: [Failure injected]
**Then**: [Expected system behavior]

Example:
Given: API Gateway is serving 1000 req/s with p99 latency < 200ms
When: One of three API Gateway instances is terminated
Then: Traffic redistributes to remaining instances with p99 latency < 300ms

## Steady State
Metrics that define normal operation:
- Request rate: 900-1100 req/s
- Error rate: < 0.1%
- p99 latency: < 200ms
- CPU usage: < 70%

## Blast Radius
- Scope: Single availability zone
- Users affected: Max 33% (if hypothesis fails)
- Duration: 5 minutes
- Rollback: Terminate experiment, restore instance

## Experiment Steps
1. Verify steady state (5 min baseline)
2. Inject failure (terminate instance)
3. Observe system behavior (5 min)
4. Restore system (if needed)
5. Verify return to steady state

## Success Criteria
- [ ] Error rate stays < 0.5%
- [ ] p99 latency stays < 300ms
- [ ] No manual intervention required
- [ ] System auto-recovers within 2 minutes

## Abort Conditions
- Error rate > 1%
- p99 latency > 500ms
- Manual intervention required
```

### Hypothesis Examples

```
Hypothesis 1: Database Failover
Given: Primary database is serving 500 queries/s
When: Primary database instance is terminated
Then: Replica promotes to primary within 30 seconds with no data loss

Hypothesis 2: Network Latency
Given: Service A calls Service B with p99 latency 50ms
When: 100ms latency injected between A and B
Then: Circuit breaker opens after 10 failures, fallback cache is used

Hypothesis 3: Memory Pressure
Given: Service is using 2GB RAM with GC pauses < 10ms
When: Memory limit reduced to 1GB
Then: Service triggers OOM kill and restarts within 30 seconds
```

## 3. Types of Chaos Experiments

### 3.1 Infrastructure Chaos

#### Kill Instances

```bash
# Chaos Monkey style: Random instance termination
aws ec2 terminate-instances \
  --instance-ids $(aws ec2 describe-instances \
    --filters "Name=tag:Service,Values=api-gateway" \
    --query 'Reservations[0].Instances[0].InstanceId' \
    --output text)
```

```typescript
// Kubernetes pod deletion
import * as k8s from '@kubernetes/client-node';

async function killRandomPod(namespace: string, labelSelector: string) {
  const kc = new k8s.KubeConfig();
  kc.loadFromDefault();
  const k8sApi = kc.makeApiClient(k8s.CoreV1Api);

  const pods = await k8sApi.listNamespacedPod(
    namespace,
    undefined,
    undefined,
    undefined,
    undefined,
    labelSelector
  );

  const randomPod = pods.body.items[
    Math.floor(Math.random() * pods.body.items.length)
  ];

  await k8sApi.deleteNamespacedPod(randomPod.metadata!.name!, namespace);
  console.log(`Killed pod: ${randomPod.metadata!.name}`);
}

// Usage
await killRandomPod('production', 'app=api-gateway');
```

#### Network Latency

```bash
# Add 100ms latency using tc (Linux traffic control)
sudo tc qdisc add dev eth0 root netem delay 100ms

# Add variable latency (100ms ± 20ms)
sudo tc qdisc add dev eth0 root netem delay 100ms 20ms

# Remove latency
sudo tc qdisc del dev eth0 root
```

```typescript
// Toxiproxy: Network chaos proxy
import Toxiproxy from 'toxiproxy-node-client';

const toxiproxy = new Toxiproxy('http://localhost:8474');

// Add latency toxic
await toxiproxy.get('/proxies/api-gateway').toxics().create({
  type: 'latency',
  attributes: {
    latency: 1000, // 1 second
    jitter: 200    // ± 200ms
  }
});

// Remove toxic
await toxiproxy.get('/proxies/api-gateway').toxics().destroy('latency_downstream');
```

#### Packet Loss

```bash
# Drop 10% of packets
sudo tc qdisc add dev eth0 root netem loss 10%

# Drop packets with correlation (burst loss)
sudo tc qdisc add dev eth0 root netem loss 10% 25%
```

#### Network Partition

```bash
# Block traffic to specific IP
sudo iptables -A INPUT -s 10.0.1.50 -j DROP
sudo iptables -A OUTPUT -d 10.0.1.50 -j DROP

# Restore
sudo iptables -D INPUT -s 10.0.1.50 -j DROP
sudo iptables -D OUTPUT -d 10.0.1.50 -j DROP
```

### 3.2 Application Chaos

#### Inject Errors

```typescript
// Middleware to inject random errors
class ErrorInjectionMiddleware {
  constructor(
    private errorRate: number = 0.05, // 5% error rate
    private enabled: boolean = false
  ) {}

  handle(req: Request, res: Response, next: NextFunction) {
    if (this.enabled && Math.random() < this.errorRate) {
      const errorType = this.selectError();
      return res.status(errorType.code).json({
        error: errorType.message,
        chaos: true
      });
    }
    next();
  }

  private selectError() {
    const errors = [
      { code: 500, message: 'Internal Server Error' },
      { code: 503, message: 'Service Unavailable' },
      { code: 504, message: 'Gateway Timeout' }
    ];
    return errors[Math.floor(Math.random() * errors.length)];
  }
}

// Usage
app.use(new ErrorInjectionMiddleware(0.05, process.env.CHAOS_ENABLED === 'true').handle);
```

#### Slow Dependencies

```typescript
// Inject latency into external API calls
class LatencyInjector {
  constructor(
    private minLatency: number = 0,
    private maxLatency: number = 5000
  ) {}

  async wrap<T>(fn: () => Promise<T>): Promise<T> {
    const delay = Math.random() * (this.maxLatency - this.minLatency) + this.minLatency;
    await new Promise(resolve => setTimeout(resolve, delay));
    return fn();
  }
}

// Usage
const injector = new LatencyInjector(1000, 3000);
const result = await injector.wrap(() => externalAPI.call());
```

#### Exception Injection

```typescript
// Aspect-oriented chaos: Inject exceptions
function chaosDecorator(errorRate: number = 0.05) {
  return function (target: any, propertyKey: string, descriptor: PropertyDescriptor) {
    const originalMethod = descriptor.value;

    descriptor.value = async function (...args: any[]) {
      if (Math.random() < errorRate) {
        throw new Error(`Chaos: Injected exception in ${propertyKey}`);
      }
      return originalMethod.apply(this, args);
    };

    return descriptor;
  };
}

// Usage
class UserService {
  @chaosDecorator(0.05)
  async getUser(id: string) {
    return await db.users.findById(id);
  }
}
```

### 3.3 State Chaos

#### Corrupt Data

```typescript
// Inject corrupted data into cache
async function corruptCache(key: string) {
  const value = await cache.get(key);
  if (value) {
    const corrupted = JSON.stringify(value).replace(/\d/g, '0'); // Replace all digits with 0
    await cache.set(key, corrupted);
    console.log(`Corrupted cache key: ${key}`);
  }
}
```

#### Remove Configuration

```typescript
// Temporarily remove config values
class ConfigChaos {
  private originalValues: Map<string, any> = new Map();

  corruptConfig(keys: string[]) {
    keys.forEach(key => {
      this.originalValues.set(key, process.env[key]);
      delete process.env[key];
    });
  }

  restoreConfig() {
    this.originalValues.forEach((value, key) => {
      process.env[key] = value;
    });
    this.originalValues.clear();
  }
}

// Usage
const chaos = new ConfigChaos();
chaos.corruptConfig(['DATABASE_URL', 'REDIS_URL']);
// ... observe behavior ...
chaos.restoreConfig();
```

### 3.4 Resource Chaos

#### CPU Pressure

```bash
# stress-ng: Generate CPU load
stress-ng --cpu 4 --cpu-load 80 --timeout 60s

# Docker: Limit CPU
docker run --cpus="0.5" myapp  # 50% of one CPU
```

```typescript
// Generate CPU load in Node.js
function generateCPULoad(durationMs: number, cores: number = 1) {
  const endTime = Date.now() + durationMs;
  
  for (let i = 0; i < cores; i++) {
    const worker = new Worker(`
      const endTime = ${endTime};
      while (Date.now() < endTime) {
        Math.sqrt(Math.random());
      }
    `, { eval: true });
  }
}

// Usage: 80% CPU load for 60 seconds
generateCPULoad(60000, 4);
```

#### Memory Pressure

```typescript
// Allocate memory to create pressure
function createMemoryPressure(sizeMB: number, durationMs: number) {
  const arrays: any[] = [];
  const targetSize = sizeMB * 1024 * 1024;
  let allocated = 0;

  const interval = setInterval(() => {
    if (allocated < targetSize) {
      const chunk = new Array(1024 * 1024).fill('X'); // 1MB
      arrays.push(chunk);
      allocated += 1024 * 1024;
    }
  }, 100);

  setTimeout(() => {
    clearInterval(interval);
    arrays.length = 0; // Release memory
  }, durationMs);
}

// Usage: Allocate 500MB for 60 seconds
createMemoryPressure(500, 60000);
```

#### Disk Pressure

```bash
# Fill disk with random data
dd if=/dev/urandom of=/tmp/fillfile bs=1M count=10000  # 10GB

# Clean up
rm /tmp/fillfile
```

## 4. Chaos Engineering Tools

### 4.1 Chaos Monkey (Netflix)

```yaml
# Spinnaker Chaos Monkey configuration
chaosMonkey:
  enabled: true
  schedule:
    enabled: true
    frequency: "0 */2 * * * ?" # Every 2 hours
  terminationStrategy:
    enabled: true
    probability: 0.5 # 50% chance
    grouping: cluster
    exceptions:
      - account: production
        stack: critical
```

**Features**:
- Random instance termination
- Scheduled chaos
- Cluster-aware (maintains minimum instances)
- Integration with Spinnaker

### 4.2 Gremlin

```bash
# Gremlin CLI: CPU attack
gremlin attack-container cpu \
  --length 60 \
  --cores 2 \
  --percent 80 \
  --container-ids abc123

# Network latency attack
gremlin attack-container latency \
  --length 300 \
  --delay 100 \
  --target api.example.com \
  --container-ids abc123
```

**Features**:
- SaaS platform with UI
- Pre-built attack types
- Blast radius controls
- Halting conditions
- Scheduling and automation
- Team collaboration

### 4.3 Chaos Mesh (Kubernetes)

```yaml
# PodChaos: Kill random pod
apiVersion: chaos-mesh.org/v1alpha1
kind: PodChaos
metadata:
  name: pod-kill-example
spec:
  action: pod-kill
  mode: one # one, all, fixed, fixed-percent, random-max-percent
  selector:
    namespaces:
      - production
    labelSelectors:
      app: api-gateway
  scheduler:
    cron: "@every 2h"
```

```yaml
# NetworkChaos: Add latency
apiVersion: chaos-mesh.org/v1alpha1
kind: NetworkChaos
metadata:
  name: network-delay
spec:
  action: delay
  mode: all
  selector:
    namespaces:
      - production
    labelSelectors:
      app: api-gateway
  delay:
    latency: "100ms"
    jitter: "20ms"
  duration: "5m"
```

```yaml
# StressChaos: CPU pressure
apiVersion: chaos-mesh.org/v1alpha1
kind: StressChaos
metadata:
  name: cpu-stress
spec:
  mode: one
  selector:
    namespaces:
      - production
    labelSelectors:
      app: worker
  stressors:
    cpu:
      workers: 2
      load: 80
  duration: "10m"
```

### 4.4 Litmus (Kubernetes)

```yaml
# Litmus ChaosEngine
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: api-chaos
spec:
  appinfo:
    appns: production
    applabel: "app=api-gateway"
    appkind: deployment
  chaosServiceAccount: litmus-admin
  experiments:
    - name: pod-delete
      spec:
        components:
          env:
            - name: TOTAL_CHAOS_DURATION
              value: "60"
            - name: CHAOS_INTERVAL
              value: "10"
            - name: FORCE
              value: "false"
```

### 4.5 AWS Fault Injection Simulator (FIS)

```json
{
  "description": "Terminate EC2 instances",
  "targets": {
    "Instances": {
      "resourceType": "aws:ec2:instance",
      "resourceTags": {
        "Environment": "production",
        "Service": "api-gateway"
      },
      "selectionMode": "COUNT(1)"
    }
  },
  "actions": {
    "TerminateInstances": {
      "actionId": "aws:ec2:terminate-instances",
      "parameters": {},
      "targets": {
        "Instances": "Instances"
      }
    }
  },
  "stopConditions": [
    {
      "source": "aws:cloudwatch:alarm",
      "value": "arn:aws:cloudwatch:us-east-1:123456789012:alarm:HighErrorRate"
    }
  ],
  "roleArn": "arn:aws:iam::123456789012:role/FISRole"
}
```

### Tool Comparison

| Tool | Environment | Ease of Use | Attack Types | Cost |
|------|-------------|-------------|--------------|------|
| Chaos Monkey | AWS | Medium | Instance termination | Free |
| Gremlin | Any | Easy | Comprehensive | Paid |
| Chaos Mesh | Kubernetes | Medium | Comprehensive | Free |
| Litmus | Kubernetes | Medium | Comprehensive | Free |
| AWS FIS | AWS | Easy | AWS-specific | Pay per experiment |
| Toxiproxy | Any | Easy | Network only | Free |

## 5. Experiment Design

### 5.1 Steady State Definition

```typescript
// Define steady state metrics
interface SteadyState {
  requestRate: { min: number; max: number };
  errorRate: { max: number };
  latencyP99: { max: number };
  cpuUsage: { max: number };
  memoryUsage: { max: number };
}

const steadyState: SteadyState = {
  requestRate: { min: 900, max: 1100 },
  errorRate: { max: 0.001 }, // 0.1%
  latencyP99: { max: 200 },
  cpuUsage: { max: 70 },
  memoryUsage: { max: 80 }
};

async function verifySteadyState(): Promise<boolean> {
  const metrics = await getMetrics();
  
  return (
    metrics.requestRate >= steadyState.requestRate.min &&
    metrics.requestRate <= steadyState.requestRate.max &&
    metrics.errorRate <= steadyState.errorRate.max &&
    metrics.latencyP99 <= steadyState.latencyP99.max &&
    metrics.cpuUsage <= steadyState.cpuUsage.max &&
    metrics.memoryUsage <= steadyState.memoryUsage.max
  );
}
```

### 5.2 Hypothesis Formulation

```
Template:
"We believe that [system] will [expected behavior] when [failure condition]"

Good Hypotheses:
✓ "We believe that the API Gateway will maintain <1% error rate when one instance is terminated"
✓ "We believe that the database will failover within 30 seconds when the primary fails"
✓ "We believe that the cache will serve stale data when Redis is unavailable"

Bad Hypotheses:
✗ "The system will be resilient" (too vague)
✗ "Nothing bad will happen" (not measurable)
✗ "It should work" (not specific)
```

### 5.3 Blast Radius Control

```typescript
// Blast radius controls
interface BlastRadiusControl {
  scope: 'single-instance' | 'single-az' | 'single-region' | 'global';
  maxUsersAffected: number;
  maxDuration: number; // seconds
  canaryPercentage?: number;
}

const blastRadius: BlastRadiusControl = {
  scope: 'single-az',
  maxUsersAffected: 1000,
  maxDuration: 300, // 5 minutes
  canaryPercentage: 5 // Start with 5% of instances
};

// Progressive blast radius
async function runProgressiveExperiment() {
  // Phase 1: Single instance (1%)
  await runExperiment({ scope: 'single-instance', duration: 60 });
  if (!success) return abort();

  // Phase 2: 5% of instances
  await runExperiment({ scope: 'canary', percentage: 5, duration: 300 });
  if (!success) return abort();

  // Phase 3: Single AZ (33%)
  await runExperiment({ scope: 'single-az', duration: 600 });
}
```

### 5.4 Rollback Mechanisms

```typescript
// Automatic rollback on failure
class ChaosExperiment {
  private abortController = new AbortController();
  private rollbackActions: (() => Promise<void>)[] = [];

  async run() {
    try {
      // Set up abort conditions
      this.setupAbortConditions();

      // Run experiment
      await this.injectFailure();

      // Monitor
      await this.monitor();

    } catch (error) {
      console.error('Experiment failed:', error);
    } finally {
      // Always rollback
      await this.rollback();
    }
  }

  private setupAbortConditions() {
    // Abort if error rate > 5%
    const checkInterval = setInterval(async () => {
      const metrics = await getMetrics();
      if (metrics.errorRate > 0.05) {
        console.log('Abort condition met: High error rate');
        this.abortController.abort();
      }
    }, 5000);

    this.rollbackActions.push(async () => {
      clearInterval(checkInterval);
    });
  }

  private async rollback() {
    console.log('Rolling back experiment...');
    for (const action of this.rollbackActions.reverse()) {
      await action();
    }
  }
}
```

## 6. Progressive Chaos (Game Days)

### Game Day Structure

```
Game Day: "Database Failover Drill"

Participants:
- SRE team (facilitators)
- Engineering team (responders)
- Product team (observers)

Schedule:
09:00 - Briefing and hypothesis review
09:30 - Verify steady state
10:00 - Inject failure (terminate primary database)
10:00-10:30 - Observe and respond
10:30 - Restore system (if needed)
11:00 - Debrief and lessons learned

Scenarios:
1. Primary database failure
2. Network partition between app and database
3. Slow queries causing connection pool exhaustion
4. Replica lag causing stale reads

Success Criteria:
- Automatic failover within 30 seconds
- No data loss
- Error rate < 1% during failover
- Team follows runbook correctly
```

### Game Day Checklist

```markdown
## Pre-Game Day
- [ ] Define hypothesis and success criteria
- [ ] Notify stakeholders
- [ ] Prepare rollback plan
- [ ] Set up monitoring dashboards
- [ ] Review runbooks
- [ ] Ensure team availability

## During Game Day
- [ ] Verify steady state (15 min baseline)
- [ ] Inject failure
- [ ] Monitor metrics
- [ ] Document observations
- [ ] Test rollback if needed
- [ ] Verify return to steady state

## Post-Game Day
- [ ] Debrief meeting
- [ ] Document learnings
- [ ] Create action items
- [ ] Update runbooks
- [ ] Schedule follow-up experiments
```

## 7. Chaos in Different Environments

### Production Chaos

**Pros**:
- Real traffic patterns
- Real dependencies
- Real user impact (validates hypothesis)
- Cultural shift (failures are normal)

**Cons**:
- Risk of customer impact
- Requires mature monitoring
- Needs strong rollback mechanisms

**Best Practices**:
```
1. Start small (single instance, short duration)
2. Run during business hours (team available)
3. Notify stakeholders
4. Have abort conditions
5. Monitor closely
6. Gradual rollout (canary → single AZ → region)
```

### Staging Chaos

**Pros**:
- Safe environment
- No customer impact
- Can run aggressive experiments

**Cons**:
- Doesn't have real traffic
- May not have all dependencies
- Different configuration than production

**Best Practices**:
```
1. Mirror production configuration
2. Use production-like load
3. Include all dependencies
4. Treat staging failures seriously
```

### Development Chaos

**Pros**:
- Very safe
- Fast iteration
- Learning environment

**Cons**:
- Least realistic
- May not catch real issues

**Best Practices**:
```
1. Use for learning and experimentation
2. Test new chaos scenarios here first
3. Validate tooling and automation
```

## 8. Observability Requirements for Chaos

### Essential Metrics

```typescript
// Metrics to track during chaos experiments
interface ChaosMetrics {
  // Golden Signals
  requestRate: number;
  errorRate: number;
  latencyP50: number;
  latencyP99: number;
  saturation: number; // Resource usage

  // System Health
  instanceCount: number;
  healthyInstances: number;
  cpuUsage: number;
  memoryUsage: number;
  diskUsage: number;

  // Application Specific
  activeConnections: number;
  queueDepth: number;
  cacheHitRate: number;
  databaseConnections: number;
}

// Collect metrics before, during, and after
class MetricsCollector {
  private baseline: ChaosMetrics[] = [];
  private during: ChaosMetrics[] = [];
  private after: ChaosMetrics[] = [];

  async collectBaseline(durationMs: number) {
    const endTime = Date.now() + durationMs;
    while (Date.now() < endTime) {
      this.baseline.push(await this.collect());
      await sleep(5000); // Every 5 seconds
    }
  }

  async collectDuring(durationMs: number) {
    const endTime = Date.now() + durationMs;
    while (Date.now() < endTime) {
      this.during.push(await this.collect());
      await sleep(5000);
    }
  }

  async collectAfter(durationMs: number) {
    const endTime = Date.now() + durationMs;
    while (Date.now() < endTime) {
      this.after.push(await this.collect());
      await sleep(5000);
    }
  }

  analyze() {
    return {
      baseline: this.calculateStats(this.baseline),
      during: this.calculateStats(this.during),
      after: this.calculateStats(this.after)
    };
  }
}
```

### Distributed Tracing

```typescript
// Track request flow during chaos
import { trace, context } from '@opentelemetry/api';

async function chaosAwareRequest(req: Request) {
  const span = trace.getTracer('chaos').startSpan('request');
  
  span.setAttribute('chaos.experiment.active', isChaosActive());
  span.setAttribute('chaos.experiment.id', getCurrentExperimentId());

  try {
    const result = await processRequest(req);
    span.setStatus({ code: SpanStatusCode.OK });
    return result;
  } catch (error) {
    span.setStatus({ code: SpanStatusCode.ERROR });
    span.setAttribute('chaos.failure.detected', true);
    throw error;
  } finally {
    span.end();
  }
}
```

## 9. Safety Mechanisms and Safeguards

### Abort Conditions

```typescript
// Automatic experiment abort
class SafetyMonitor {
  private abortConditions = [
    {
      name: 'High Error Rate',
      check: async () => (await getErrorRate()) > 0.05,
      severity: 'critical'
    },
    {
      name: 'High Latency',
      check: async () => (await getP99Latency()) > 1000,
      severity: 'high'
    },
    {
      name: 'Low Instance Count',
      check: async () => (await getHealthyInstances()) < 2,
      severity: 'critical'
    }
  ];

  async monitor(abortCallback: () => void) {
    const interval = setInterval(async () => {
      for (const condition of this.abortConditions) {
        if (await condition.check()) {
          console.error(`Abort condition met: ${condition.name}`);
          abortCallback();
          clearInterval(interval);
          return;
        }
      }
    }, 5000);
  }
}
```

### Manual Kill Switch

```typescript
// Emergency stop button
class ChaosController {
  private experiments: Map<string, ChaosExperiment> = new Map();

  async startExperiment(id: string, experiment: ChaosExperiment) {
    this.experiments.set(id, experiment);
    await experiment.run();
  }

  async emergencyStop() {
    console.log('EMERGENCY STOP: Aborting all experiments');
    for (const [id, experiment] of this.experiments) {
      await experiment.abort();
      console.log(`Aborted experiment: ${id}`);
    }
    this.experiments.clear();
  }
}

// HTTP endpoint for emergency stop
app.post('/chaos/emergency-stop', async (req, res) => {
  await chaosController.emergencyStop();
  res.json({ status: 'All experiments aborted' });
});
```

## 10. Learning from Experiments

### Experiment Report Template

```markdown
# Chaos Experiment Report: [Name]

## Executive Summary
One-paragraph summary of what was tested and what was learned.

## Hypothesis
**Expected**: System will maintain <1% error rate when one instance is terminated
**Actual**: Error rate spiked to 15% for 2 minutes before recovering

## Experiment Details
- **Date**: 2024-01-15
- **Duration**: 10 minutes
- **Blast Radius**: Single AZ (33% of instances)
- **Participants**: SRE team, Backend team

## Results

### Metrics Comparison
| Metric | Baseline | During Chaos | After Recovery |
|--------|----------|--------------|----------------|
| Error Rate | 0.1% | 15% | 0.2% |
| p99 Latency | 150ms | 800ms | 180ms |
| Request Rate | 1000/s | 850/s | 980/s |

### Timeline
- 10:00:00 - Baseline established
- 10:05:00 - Instance terminated
- 10:05:15 - Error rate spike detected
- 10:07:00 - System recovered
- 10:15:00 - Returned to steady state

## Findings

### What Went Well
- Automatic instance replacement worked
- Monitoring detected issue quickly
- No data loss occurred

### What Went Wrong
- Load balancer took 2 minutes to detect unhealthy instance
- No circuit breaker to prevent cascading failures
- Alerts fired too late

### Unexpected Behaviors
- Database connection pool exhausted during recovery
- Cache invalidation caused additional load

## Action Items
1. [ ] Reduce load balancer health check interval (Owner: @alice, Due: 2024-01-20)
2. [ ] Implement circuit breaker (Owner: @bob, Due: 2024-01-25)
3. [ ] Tune database connection pool (Owner: @charlie, Due: 2024-01-22)
4. [ ] Update alert thresholds (Owner: @diana, Due: 2024-01-18)

## Recommendations
- Run follow-up experiment after fixes
- Test multi-instance failure next
- Add this scenario to CI/CD pipeline
```

## 11. Building Chaos into CI/CD

### Automated Chaos Tests

```yaml
# GitHub Actions: Chaos testing
name: Chaos Tests

on:
  schedule:
    - cron: '0 */6 * * *' # Every 6 hours
  workflow_dispatch:

jobs:
  chaos-pod-kill:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy to test environment
        run: kubectl apply -f k8s/

      - name: Wait for steady state
        run: |
          sleep 60
          ./scripts/verify-steady-state.sh

      - name: Run pod kill experiment
        run: |
          kubectl apply -f chaos/pod-kill.yaml
          sleep 300

      - name: Verify system recovered
        run: ./scripts/verify-steady-state.sh

      - name: Cleanup
        if: always()
        run: kubectl delete -f chaos/pod-kill.yaml
```

### Pre-Deployment Chaos

```yaml
# Validate resilience before production deployment
name: Pre-Deploy Chaos

on:
  pull_request:
    branches: [main]

jobs:
  chaos-validation:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to staging
        run: ./deploy-staging.sh

      - name: Run chaos suite
        run: |
          ./chaos/run-suite.sh \
            --experiments pod-kill,network-latency,cpu-stress \
            --duration 300 \
            --abort-on-failure

      - name: Validate results
        run: |
          if [ $(cat chaos-results.json | jq '.failures') -gt 0 ]; then
            echo "Chaos tests failed - blocking deployment"
            exit 1
          fi
```

## 12. Cultural Aspects of Chaos Engineering

### Building a Chaos Culture

```
1. Start with Education
   - Lunch & learns about chaos engineering
   - Share Netflix and other case studies
   - Explain the "why" not just the "how"

2. Get Buy-In
   - Start with volunteer teams
   - Show quick wins
   - Celebrate learning from failures

3. Make it Safe
   - Blameless culture
   - Failures are learning opportunities
   - Focus on system improvement, not blame

4. Start Small
   - Dev environment first
   - Single service experiments
   - Short duration
   - Gradually increase scope

5. Automate and Scale
   - Build chaos into CI/CD
   - Regular Game Days
   - Chaos as part of definition of done
```

### Common Objections and Responses

```
Objection: "We can't break production!"
Response: "Production is already breaking. Chaos helps us find and fix issues before customers do."

Objection: "We don't have time for this."
Response: "Outages cost more time than chaos experiments. This is an investment in reliability."

Objection: "Our system is too fragile."
Response: "That's exactly why we need chaos engineering - to make it less fragile."

Objection: "What if we cause an outage?"
Response: "We start small with controlled experiments and abort conditions. Better to find issues in a controlled way than during a real incident."
```

## 13. Real Examples

### Netflix Chaos Practices

```
Chaos Monkey: Randomly terminates instances
Chaos Kong: Simulates entire AWS region failure
Chaos Gorilla: Simulates entire availability zone failure
Latency Monkey: Induces artificial delays
Doctor Monkey: Checks for unhealthy instances
Janitor Monkey: Cleans up unused resources
Conformity Monkey: Shuts down non-conforming instances

Philosophy:
- Run in production during business hours
- Failures are expected, not exceptional
- Build systems that assume failure
- Continuous chaos, not one-time tests
```

### Amazon Chaos Engineering

```
GameDay Program:
- Regular scheduled failure injection
- Cross-team participation
- Simulates major failures (region loss, service outages)
- Tests incident response procedures
- Validates runbooks

Practices:
- Chaos in production
- Automated recovery testing
- Dependency failure injection
- Load testing with chaos
```

### Google SRE Chaos Practices

```
DiRT (Disaster Recovery Testing):
- Annual company-wide exercise
- Simulates catastrophic failures
- Tests backup systems
- Validates disaster recovery plans
- Involves all teams

Practices:
- Chaos in production
- Automated rollback testing
- Multi-region failure testing
- Dependency isolation testing
```

## 14. Getting Started with Chaos (Crawl, Walk, Run)

### Crawl Phase (Weeks 1-4)

```
Goals:
- Learn chaos engineering principles
- Build team confidence
- Establish baseline metrics

Activities:
1. Read chaos engineering resources
2. Set up monitoring and observability
3. Document steady state metrics
4. Run first experiment in dev environment
5. Simple experiment: Kill a single pod

Example First Experiment:
- Environment: Development
- Scope: Single pod
- Duration: 5 minutes
- Hypothesis: "System will recover automatically when one pod is killed"
- Success: Pod restarts, traffic redistributes, no manual intervention
```

### Walk Phase (Weeks 5-12)

```
Goals:
- Run experiments in staging
- Increase experiment complexity
- Automate experiments

Activities:
1. Run experiments in staging environment
2. Test multiple failure types (network, resource, state)
3. Automate experiment execution
4. Build chaos into CI/CD pipeline
5. Conduct first Game Day

Example Experiments:
- Network latency injection
- CPU/memory pressure
- Database connection failures
- Cache unavailability
- Multi-pod failures
```

### Run Phase (Week 13+)

```
Goals:
- Run chaos in production
- Continuous chaos
- Advanced scenarios

Activities:
1. Run controlled experiments in production
2. Schedule regular Game Days
3. Test complex failure scenarios
4. Measure and improve MTTR
5. Build chaos culture

Example Advanced Experiments:
- Multi-region failures
- Cascading failure scenarios
- Byzantine failure injection
- Time-based failures (leap second, clock skew)
- Dependency chain failures
```

### Chaos Maturity Model

```
Level 0: No Chaos
- No failure testing
- Hope for the best

Level 1: Ad-hoc Chaos
- Occasional manual tests
- Dev/staging only
- No automation

Level 2: Systematic Chaos
- Regular scheduled experiments
- Automated execution
- Staging and limited production

Level 3: Continuous Chaos
- Chaos in CI/CD
- Production chaos
- Game Days
- Chaos culture

Level 4: Advanced Chaos
- Continuous production chaos
- Complex scenarios
- Chaos as part of development
- Organization-wide practice
```

## Summary

Chaos Engineering is essential for building confidence in system resilience:

1. **Start with a hypothesis** - Define expected behavior
2. **Define steady state** - Know what "normal" looks like
3. **Inject realistic failures** - Test what could actually happen
4. **Start small** - Dev → Staging → Production
5. **Control blast radius** - Limit potential impact
6. **Monitor closely** - Observe system behavior
7. **Have abort conditions** - Know when to stop
8. **Learn and improve** - Document findings and fix issues
9. **Automate** - Make chaos continuous
10. **Build culture** - Make failure injection normal

**Remember**: The goal isn't to break things - it's to build confidence that your system can handle failures gracefully.

## Related Skills

- `40-system-resilience/failure-modes` - Understanding what can fail
- `40-system-resilience/retry-timeout-strategies` - Handling transient failures
- `40-system-resilience/postmortem-analysis` - Learning from incidents
- `40-system-resilience/disaster-recovery` - Recovering from catastrophic failures
