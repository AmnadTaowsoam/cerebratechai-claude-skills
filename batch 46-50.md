# Final 5 Enterprise Skills - Production Reality Prompts

Complete prompts for creating 5 critical enterprise skills that bridge the gap between "compliance checkbox" and "production implementation".

---

## Batch 46: Privacy, Data Classification, and Redaction

### Skill 1: PII Detection

```
Create a comprehensive SKILL.md for PII (Personally Identifiable Information) Detection.

Location: 46-data-classification/pii-detection/SKILL.md

Cover:
1. What is PII (legal definitions):
   - GDPR definition (EU)
   - CCPA definition (California)
   - PDPA definition (Thailand)
   - HIPAA PHI (healthcare)
2. Types of PII:
   - Direct identifiers: Name, ID number, passport, SSN
   - Indirect identifiers: IP address, device ID, cookies
   - Sensitive PII: Health, financial, biometric, political
   - Quasi-identifiers: Combination reveals identity
3. Domain-specific PII:
   - Financial: Account numbers, credit cards, routing numbers
   - Healthcare: Medical records, diagnoses, prescriptions
   - HR: Salary, performance reviews, background checks
   - E-commerce: Purchase history, payment methods
4. PII detection methods:
   - Regex patterns (email, phone, credit card, SSN)
   - Named Entity Recognition (NER) models
   - Dictionary matching
   - Statistical detection
   - ML-based classification
5. Tools and libraries:
   - Python: presidio-analyzer, scrubadub, piicatcher
   - Cloud: AWS Macie, GCP DLP API, Azure Purview
   - Open-source: Microsoft Presidio
6. Detection patterns:
   - Email: `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}`
   - Phone: Various formats (US, international)
   - Credit card: Luhn algorithm validation
   - SSN: `\d{3}-\d{2}-\d{4}`
   - Thai ID: 13-digit with checksum
7. Context-aware detection:
   - "James" alone is not PII
   - "James with email james@company.com" is PII
   - Field name hints (email_address, phone_number)
8. False positive handling:
   - Sample emails (test@example.com)
   - Dummy credit cards (4111111111111111)
   - Test phone numbers
9. Scanning strategies:
   - Database scanning (batch)
   - Log file scanning
   - API request/response scanning
   - File upload scanning
10. PII inventory creation:
    - What PII do we collect?
    - Where is it stored?
    - Who has access?
    - Retention period?
11. Automated PII discovery in:
    - Databases (PostgreSQL, MongoDB)
    - S3 buckets
    - Log files (CloudWatch, Datadog)
    - Git repositories (truffleHog for secrets)
12. PII detection SLA (scan frequency)
13. Reporting and alerting on PII:
    - New PII detected
    - PII in unencrypted storage
    - PII in logs (should never happen!)
14. Implementation examples:
    - Python with Presidio
    - TypeScript with regex patterns
    - Database scanning queries
15. Real-world detection scenarios

Format: Include detection patterns (regex), code examples (Python, TypeScript), and scanning workflows.

Create the file now.
```

### Skill 2: Logging Redaction

```
Create a comprehensive SKILL.md for Logging Redaction (preventing PII/secrets in logs).

Location: 46-data-classification/logging-redaction/SKILL.md

Cover:
1. Why redaction matters:
   - PII in logs = compliance violation
   - Secrets in logs = security breach
   - Logs are long-lived and widely accessible
2. What to redact:
   - PII: Names, emails, phone numbers, addresses
   - Authentication: Passwords, API keys, tokens, session IDs
   - Financial: Credit cards, bank accounts, CVV
   - Healthcare: Medical record numbers, diagnoses
   - Business secrets: Proprietary algorithms, pricing
3. Redaction strategies:
   - Complete removal: "password": "******"
   - Partial masking: "4532****1234" for credit cards
   - Hashing: Consistent for correlation without revealing
   - Tokenization: Replace with placeholder tokens
4. Redaction patterns:
   - Before logging (preferred)
   - At logging time (middleware)
   - After logging (log processors)
   - At query time (least preferred)
5. Application-level redaction:
   - Structured logging with redaction
   - Log formatters with PII detection
   - Safe-by-default logging practices
6. Redaction libraries:
   - Python: logging redaction, scrubadub
   - Node.js: pino-redaction, winston-redact
   - Go: zap with custom encoders
7. Log aggregation redaction:
   - Datadog: Sensitive Data Scanner
   - Splunk: Data anonymization
   - ELK: Logstash filters
   - CloudWatch: Logs Insights redaction
8. Configuration-driven redaction:
   - JSON paths to redact
   - Field name patterns
   - Regex patterns
   - Custom redaction functions
9. Performance considerations:
   - Redaction overhead
   - Caching redaction decisions
   - Sampling vs full redaction
10. Testing redaction:
    - Unit tests with PII samples
    - Log review audits
    - Automated PII detection in logs
11. Redaction for different log types:
    - Application logs
    - Access logs (IP addresses?)
    - Database query logs
    - Audit logs (selective redaction)
    - Error logs (stack traces with context)
12. Trade-offs:
    - Debugging vs privacy
    - Correlation vs security
    - Performance vs completeness
13. Redaction policies:
    - What gets redacted
    - What stays (for debugging)
    - Retention after redaction
14. Common mistakes:
    - Logging request.body without redaction
    - Exception messages with user input
    - SQL queries with parameters
    - API responses with full user objects
15. Implementation examples:
    - Python logging with redaction
    - Node.js Winston redaction
    - Structured logging best practices

Format: Include code examples (Python, Node.js), configuration templates, and redaction patterns.

Create the file now.
```

### Skill 3: Retention and Deletion

```
Create a comprehensive SKILL.md for Data Retention and Deletion policies.

Location: 46-data-classification/retention-and-deletion/SKILL.md

Cover:
1. Why retention matters:
   - Compliance (GDPR, CCPA right to deletion)
   - Cost (storage costs money)
   - Security (old data = risk)
   - Legal (litigation hold)
2. Retention policy framework:
   - Data classification (what data?)
   - Retention period (how long?)
   - Deletion method (how to delete?)
   - Legal holds (exceptions)
   - Audit trail (proof of deletion)
3. Legal requirements:
   - GDPR: Right to erasure, data minimization
   - CCPA: Right to deletion
   - PDPA (Thailand): Similar to GDPR
   - Industry-specific: HIPAA (6 years), SOX (7 years)
4. Retention schedules by data type:
   - User accounts: 30 days after deletion request
   - Transaction logs: 7 years (financial)
   - Access logs: 90 days (security)
   - Backups: 30 days (operational)
   - Analytics: 13 months (GDPR)
   - Audit logs: 7 years (compliance)
5. Data lifecycle states:
   - Active: In production use
   - Archived: Cold storage, rarely accessed
   - Deleted: Permanently removed
6. Deletion types:
   - Soft delete: Marked as deleted, recoverable
   - Hard delete: Permanently removed
   - Anonymization: Remove identifying info
   - Pseudonymization: Replace with pseudonyms
7. Right to erasure implementation:
   - User deletion request flow
   - Verification (prevent impersonation)
   - Grace period (30 days?)
   - Cascade deletion (all related data)
   - Backup deletion (delayed)
8. Deletion challenges:
   - Distributed systems (eventual consistency)
   - Backups (how to delete from backups?)
   - Data lakes (immutable logs)
   - Third-party systems (notify partners)
   - Analytics aggregates (anonymized already?)
9. Automated retention:
   - TTL (Time To Live) in databases
   - S3 lifecycle policies
   - Database partitioning by date
   - Scheduled deletion jobs
   - Audit log cleanup
10. Legal hold procedures:
    - Suspend deletion for litigation
    - Legal hold tracking
    - Release from hold
11. Deletion verification:
    - Proof of deletion
    - Deletion audits
    - User-facing deletion confirmation
12. Tools and implementation:
    - PostgreSQL: Partitioning + DROP
    - MongoDB: TTL indexes
    - S3: Lifecycle rules
    - Data warehouse: Retention policies
13. Deletion for different systems:
    - Relational databases
    - NoSQL databases
    - Object storage (S3, GCS)
    - Search indexes (Elasticsearch)
    - Caches (Redis)
    - CDN (Cloudflare, CloudFront)
    - Third-party SaaS (Stripe, Salesforce)
14. Monitoring retention compliance:
    - Data age reports
    - Retention SLA tracking
    - Deletion job success rates
15. Real-world scenarios:
    - User requests account deletion
    - GDPR deletion request (30 days)
    - Expired trial accounts (auto-delete)
    - Inactive accounts (6 months)

Format: Include retention policy templates, deletion workflows, and implementation code.

Create the file now.
```

### Skill 4: Access Audit and Reviews

```
Create a comprehensive SKILL.md for Access Audits and Periodic Reviews.

Location: 46-data-classification/access-audit-and-reviews/SKILL.md

Cover:
1. Why access audits matter:
   - Compliance (SOC2, ISO 27001)
   - Security (detect unauthorized access)
   - Least privilege enforcement
   - Insider threat detection
2. What to audit:
   - User access (who can access what)
   - Admin access (privileged accounts)
   - Service account access (API keys, tokens)
   - Database access (direct DB connections)
   - File system access (sensitive directories)
   - Third-party access (vendor accounts)
3. Audit frequency:
   - Quarterly access reviews (standard)
   - Monthly for critical systems
   - Real-time monitoring for anomalies
   - Annual comprehensive audit
4. Access review process:
   - Generate access report
   - Manager review (team access)
   - Security review (admin access)
   - Remediate excessive access
   - Document findings
5. Access review questions:
   - Does this user still need access?
   - Is access level appropriate?
   - Are there dormant accounts?
   - Are service accounts documented?
6. Automation for access reviews:
   - Automated access report generation
   - Manager notifications
   - Self-service access requests
   - Approval workflows
7. Access logging and monitoring:
   - Who accessed what, when?
   - Failed access attempts
   - Privilege escalations
   - After-hours access
   - Geographic anomalies
8. Tools for access auditing:
   - AWS IAM Access Analyzer
   - GCP Access Transparency
   - Azure AD Access Reviews
   - Database audit logs (PostgreSQL, MySQL)
   - Application audit logs
9. Audit log requirements:
   - Immutable (cannot be modified)
   - Tamper-evident
   - Long retention (7 years for compliance)
   - Centralized collection
10. Access anomaly detection:
    - Unusual access patterns
    - Access from new locations
    - Access outside business hours
    - Bulk data downloads
    - Privilege escalation attempts
11. Remediation workflows:
    - Revoke excessive access
    - Disable dormant accounts
    - Rotate compromised credentials
    - Update access documentation
12. Access certification:
    - Managers certify team access (quarterly)
    - Security certifies admin access
    - Service account owners certify usage
13. Segregation of duties (SoD):
    - No single person has complete control
    - Separate dev/prod access
    - Multi-person approval for critical changes
14. Audit reporting:
    - Access review summary
    - Remediation tracking
    - Compliance dashboard
    - Executive reporting
15. Real-world audit scenarios:
    - Quarterly IAM review
    - Post-departure access revocation
    - Contractor offboarding
    - Compliance audit preparation
16. Implementation:
    - Access report generation (SQL queries)
    - IAM policy analysis (AWS, GCP)
    - Audit log analysis

Format: Include access report templates, SQL queries, IAM analysis scripts, and review checklists.

Create the file now.
```

---

## Batch 47: Performance Engineering

### Skill 1: Profiling (Node.js & Python)

```
Create a comprehensive SKILL.md for CPU and Memory Profiling in Node.js and Python.

Location: 47-performance-engineering/profiling-node-python/SKILL.md

Cover:
1. Why profiling matters:
   - Identify bottlenecks (not guessing)
   - Optimize hot paths
   - Reduce resource usage
   - Improve user experience
2. Types of profiling:
   - CPU profiling (where time is spent)
   - Memory profiling (allocation and leaks)
   - I/O profiling (network, disk)
   - Lock profiling (concurrency issues)
3. Node.js CPU profiling:
   - Built-in profiler: `node --prof`
   - Chrome DevTools
   - Clinic.js Doctor
   - 0x (flamegraph generator)
   - v8-profiler
4. Node.js memory profiling:
   - Chrome DevTools Heap Snapshot
   - clinic-heapprofiler
   - memwatch-next
   - node --inspect
5. Python CPU profiling:
   - cProfile (built-in)
   - py-spy (sampling profiler)
   - line_profiler (line-by-line)
   - pyinstrument (flamegraphs)
6. Python memory profiling:
   - memory_profiler
   - tracemalloc (built-in)
   - pympler
   - guppy3
7. Profiling in development:
   - Local profiling
   - Representative workload
   - Profiling specific endpoints
8. Profiling in production:
   - Continuous profiling (Datadog, Pyroscope)
   - Sampling profiling (low overhead)
   - On-demand profiling (trigger manually)
9. Reading flamegraphs:
   - X-axis: Alphabetical order (not time!)
   - Y-axis: Stack depth
   - Width: Time spent
   - Colors: Usually random or by library
10. Common bottlenecks:
    - Synchronous I/O (blocking event loop)
    - N+1 queries
    - Inefficient algorithms (O(n²))
    - JSON parsing large objects
    - Regular expressions (catastrophic backtracking)
    - Memory leaks (unreleased references)
11. Memory leak detection:
    - Heap growth over time
    - Retained size analysis
    - Retainer paths (what's holding reference)
12. Profiling workflow:
    - Baseline measurement
    - Profile with realistic load
    - Identify hot paths (>5% of time)
    - Optimize top offenders
    - Re-profile to verify improvement
13. Optimization strategies:
    - Caching
    - Algorithm improvement
    - Lazy loading
    - Batch processing
    - Asynchronous operations
14. Tools comparison:
    - CLI profilers vs GUI profilers
    - Production profilers (low overhead)
    - Flamegraphs vs call trees
15. Real profiling examples:
    - Slow API endpoint
    - Memory leak in long-running process
    - High CPU usage investigation
16. Implementation:
    - Node.js profiling scripts
    - Python profiling decorators
    - CI/CD integration (performance regression detection)

Format: Include profiling commands, flamegraph examples, and optimization case studies.

Create the file now.
```

### Skill 2: Database Query Optimization

```
Create a comprehensive SKILL.md for Database Query Optimization.

Location: 47-performance-engineering/db-query-optimization/SKILL.md

Cover:
1. Why query optimization matters:
   - Slow queries = slow application
   - Database is often the bottleneck
   - Exponential cost of unoptimized queries
2. Query analysis tools:
   - PostgreSQL: EXPLAIN, EXPLAIN ANALYZE, pg_stat_statements
   - MySQL: EXPLAIN, slow query log
   - MongoDB: explain(), profiler
   - Redis: SLOWLOG
3. Understanding EXPLAIN:
   - Seq Scan (bad for large tables)
   - Index Scan (good)
   - Bitmap Scan (intermediate)
   - Nested Loop vs Hash Join
   - Cost estimates
4. Index fundamentals:
   - B-tree indexes (default, most common)
   - Hash indexes (equality only)
   - GiST/GIN (full-text, arrays)
   - Partial indexes (filtered)
   - Covering indexes (include columns)
5. When to add indexes:
   - Frequent WHERE conditions
   - JOIN columns
   - ORDER BY columns
   - Foreign keys
6. When NOT to add indexes:
   - Write-heavy tables (indexes slow writes)
   - Low-cardinality columns (e.g., boolean)
   - Small tables (<1000 rows)
7. Index maintenance:
   - Unused indexes (drop them)
   - Duplicate indexes
   - Index bloat (REINDEX)
8. Query optimization techniques:
   - SELECT only needed columns (not SELECT *)
   - Proper WHERE filtering
   - Avoid functions on indexed columns
   - Use EXISTS instead of COUNT
   - Batch queries (avoid N+1)
   - Connection pooling
9. N+1 query problem:
   - Problem: Loop with query per iteration
   - Solution: JOIN or IN clause
   - ORM: Eager loading (Prisma include, SQLAlchemy joinedload)
10. Pagination optimization:
    - LIMIT/OFFSET (simple but slow for large offsets)
    - Keyset pagination (cursor-based, faster)
    - Avoid COUNT(*) on every page
11. Aggregate optimization:
    - Materialized views
    - Summary tables
    - Pre-computed aggregates
12. PostgreSQL specific:
    - Parallel queries
    - Partitioning (range, list, hash)
    - Extensions (pg_trgm for fuzzy search)
13. MongoDB specific:
    - Compound indexes
    - Covered queries
    - Aggregation pipeline optimization
14. Query caching:
    - Application-level cache (Redis)
    - Database query cache (MySQL, deprecated in 8.0)
    - Materialized views (PostgreSQL)
15. Monitoring query performance:
    - Slow query log
    - pg_stat_statements
    - APM tools (Datadog, New Relic)
16. Real optimization examples:
    - Slow JOIN query
    - Missing index detection
    - N+1 query elimination
    - Pagination improvement
17. Tools:
    - PostgreSQL: pgAdmin, pgBadger
    - MySQL: MySQL Workbench
    - General: DataGrip, DBeaver

Format: Include EXPLAIN output examples, before/after queries, and optimization checklists.

Create the file now.
```

### Skill 3: Caching Strategies

```
Create a comprehensive SKILL.md for Caching Strategies.

Location: 47-performance-engineering/caching-strategies/SKILL.md

Cover:
1. Why caching matters:
   - Reduce database load
   - Improve response time
   - Reduce costs (fewer compute resources)
   - Scale to more users
2. Types of caches:
   - In-memory cache (application-level)
   - Distributed cache (Redis, Memcached)
   - Database query cache
   - CDN cache (edge caching)
   - Browser cache (HTTP caching)
3. Cache layers:
   - L1: Application memory (fastest, smallest)
   - L2: Redis (fast, larger)
   - L3: Database (slower, largest)
   - Edge: CDN (geographic distribution)
4. What to cache:
   - Frequent reads, infrequent writes
   - Expensive computations
   - Database query results
   - API responses
   - Static assets
5. What NOT to cache:
   - User-specific data (unless keyed properly)
   - Frequently changing data
   - Large datasets (cache memory is limited)
   - Security-sensitive data
6. Caching strategies:
   - Cache-aside (lazy loading)
   - Read-through cache
   - Write-through cache
   - Write-behind (write-back) cache
   - Refresh-ahead
7. Cache invalidation (hardest problem):
   - Time-based expiration (TTL)
   - Event-based invalidation (on update/delete)
   - Tag-based invalidation (invalidate related keys)
   - Cache stampede prevention (locking)
8. Cache keys design:
   - Unique and descriptive
   - Include version (for schema changes)
   - Namespace by feature
   - Example: `user:profile:123:v2`
9. TTL strategies:
   - Short TTL for changing data (seconds)
   - Long TTL for static data (hours/days)
   - No TTL for immutable data
   - Stale-while-revalidate pattern
10. Cache warming:
    - Pre-populate cache on startup
    - Background refresh of popular keys
    - Predictive caching (what users will request next)
11. Cache performance:
    - Hit rate (goal: >80%)
    - Miss rate
    - Eviction rate
    - Memory usage
12. Eviction policies:
    - LRU (Least Recently Used) - most common
    - LFU (Least Frequently Used)
    - FIFO (First In First Out)
    - Random
13. Distributed caching:
    - Redis cluster
    - Consistent hashing
    - Cache replication
    - Cache failover
14. Application-level caching:
    - Node.js: node-cache, lru-cache
    - Python: functools.lru_cache, cachetools
    - In-process vs shared cache
15. HTTP caching headers:
    - Cache-Control (max-age, no-cache, no-store)
    - ETag (validation)
    - Last-Modified
    - Expires (legacy)
16. Common caching mistakes:
    - Cache stampede (thundering herd)
    - Stale data issues
    - Cache key collisions
    - Memory leaks (unbounded caches)
17. Real caching scenarios:
    - API response caching
    - Database query caching
    - User session caching
    - Product catalog caching
18. Implementation examples:
    - Redis caching in Node.js
    - Redis caching in Python
    - Cache-aside pattern
    - Write-through pattern

Format: Include caching patterns, Redis code examples, and cache key design guides.

Create the file now.
```

### Skill 4: Concurrency and Throughput

```
Create a comprehensive SKILL.md for Concurrency and Throughput optimization.

Location: 47-performance-engineering/concurrency-and-throughput/SKILL.md

Cover:
1. Concurrency vs parallelism:
   - Concurrency: Dealing with many things at once (structure)
   - Parallelism: Doing many things at once (execution)
2. Throughput vs latency:
   - Throughput: Requests per second
   - Latency: Time per request
   - Trade-off: Often inverse relationship
3. Node.js concurrency model:
   - Single-threaded event loop
   - Non-blocking I/O
   - Worker threads for CPU-intensive tasks
   - Cluster mode (multiple processes)
4. Python concurrency:
   - asyncio (async/await)
   - Threading (I/O-bound tasks)
   - Multiprocessing (CPU-bound tasks)
   - GIL (Global Interpreter Lock) limitations
5. Concurrency patterns:
   - Worker pools (fixed number of workers)
   - Task queues (Redis Queue, Celery, Bull)
   - Rate limiting (control concurrency)
   - Backpressure (slow down when overwhelmed)
6. Queue-based architecture:
   - Decouple request from processing
   - Handle traffic spikes
   - Retry failed jobs
   - Priority queues
7. Task queue systems:
   - Node.js: Bull, BullMQ (Redis-based)
   - Python: Celery (RabbitMQ/Redis)
   - General: RabbitMQ, Amazon SQS
8. Worker pool sizing:
   - I/O-bound: More workers than CPU cores
   - CPU-bound: Workers = CPU cores
   - Mixed: Separate pools for each type
9. Connection pooling:
   - Database connections (Prisma, SQLAlchemy)
   - HTTP connections (keep-alive)
   - Redis connections
   - Pool size tuning
10. Async/await patterns:
    - Promise.all() for parallel execution
    - Sequential vs parallel operations
    - Error handling in async code
    - Avoiding async overhead for sync operations
11. Batching strategies:
    - Batch API requests
    - Batch database writes
    - Debouncing/throttling
    - DataLoader pattern (GraphQL)
12. Streaming for large datasets:
    - Stream processing (not loading all in memory)
    - Backpressure handling
    - Node.js streams
    - Python generators/iterators
13. Load balancing:
    - Round-robin
    - Least connections
    - Consistent hashing
    - Sticky sessions (when needed)
14. Horizontal scaling:
    - Stateless services (can add more instances)
    - Distributed task queues
    - Shared nothing architecture
15. Measuring concurrency:
    - Concurrent requests (active at one time)
    - Queue depth
    - Worker utilization
    - P95/P99 latency under load
16. Benchmarking tools:
    - Apache Bench (ab)
    - wrk, wrk2
    - Gatling
    - k6
    - autocannon (Node.js)
17. Concurrency anti-patterns:
    - Blocking the event loop (Node.js)
    - Unbounded concurrency (resource exhaustion)
    - Race conditions
    - Deadlocks
18. Real-world scenarios:
    - High-throughput API
    - Batch job processing
    - WebSocket connections
    - File processing pipeline
19. Implementation examples:
    - Worker pool in Node.js
    - Celery task queue in Python
    - Connection pooling configuration

Format: Include concurrency patterns, code examples, and benchmarking results.

Create the file now.
```

### Skill 5: SLA, SLO, and SLI

```
Create a comprehensive SKILL.md for SLA, SLO, and SLI (Service Level objectives).

Location: 47-performance-engineering/sla-slo-slis/SKILL.md

Cover:
1. Definitions:
   - SLA (Service Level Agreement): Contract with consequences
   - SLO (Service Level Objective): Internal target (more strict than SLA)
   - SLI (Service Level Indicator): Actual measurement
2. Why SLOs matter:
   - Quantify reliability
   - Balance reliability vs velocity
   - Error budget concept
   - Prioritize work (what to improve)
3. Common SLIs:
   - Availability: % of successful requests
   - Latency: % of requests under threshold (P95, P99)
   - Throughput: Requests per second
   - Error rate: % of failed requests
   - Freshness: Data age for analytics
4. Choosing good SLIs:
   - User-centric (not system-centric)
   - Measurable
   - Actionable
   - Proportional to user pain
5. Setting SLO targets:
   - Historical performance baseline
   - User expectations
   - Cost of improvement
   - Industry standards (99.9%, 99.95%, 99.99%)
6. SLO examples:
   - "95% of API requests complete in <200ms (P95)"
   - "99.9% uptime over 30 days"
   - "99% of searches return results in <500ms"
   - "Data is fresh within 5 minutes 99% of the time"
7. Error budgets:
   - If SLO is 99.9%, error budget is 0.1% (43 minutes/month)
   - Spend budget on innovation vs reliability
   - When budget exhausted, focus on reliability
8. Measuring SLIs:
   - Request logs (success/failure)
   - Latency percentiles (P50, P95, P99)
   - Synthetic monitoring (external probes)
   - Real User Monitoring (RUM)
9. SLO dashboards:
   - Current SLI value
   - SLO target line
   - Error budget remaining
   - Trend over time
   - Burn rate (how fast budget is consumed)
10. Alerting on SLOs:
    - Alert when burning budget too fast
    - Multi-window, multi-burn-rate alerts
    - Don't alert on single failed request
    - Focus on sustained problems
11. SLO-based prioritization:
    - Below SLO: Stop features, fix reliability
    - Above SLO: Can take more risks, innovate faster
12. Multi-window alerts:
    - Short window (1 hour): Fast burn detection
    - Long window (6 hours): Sustained issues
    - Combination reduces false positives
13. Tools for SLO management:
    - Datadog SLO tracking
    - Google Cloud SLO monitoring
    - Prometheus + Grafana (custom)
    - Nobl9, Rootly
14. SLA vs SLO:
    - SLA: 99.5% (external promise)
    - SLO: 99.9% (internal target, buffer for SLA)
    - If SLO is breached, still have buffer before SLA breach
15. Common mistakes:
    - Too many SLOs (focus on 3-5 key ones)
    - SLOs that don't matter to users
    - SLO targets too ambitious (99.999%)
    - No error budget policy
16. Real-world SLO examples:
    - E-commerce: Checkout availability 99.95%
    - API: P95 latency <200ms
    - Data pipeline: Freshness <5 minutes
17. Implementation:
    - Prometheus queries for SLIs
    - Alert rules
    - Dashboard JSON
    - Error budget calculation

Format: Include SLO templates, Prometheus queries, dashboard examples, and alert configurations.

Create the file now.
```

---

## Batch 48: Product Discovery & Experimentation

### Skill 1: Hypothesis Writing

```
Create a comprehensive SKILL.md for Hypothesis Writing in product development.

Location: 48-product-discovery/hypothesis-writing/SKILL.md

Cover:
1. What is a product hypothesis:
   - A testable statement about user behavior and business outcomes
   - Structure: If [action], then [outcome], because [reasoning]
2. Why hypotheses matter:
   - Forces clarity before building
   - Makes assumptions explicit
   - Enables learning (confirm or invalidate)
   - Prevents "build trap" (building without validation)
3. Hypothesis structure (AARRR):
   - If we [change/feature]
   - For [target users]
   - We will see [measurable outcome]
   - Because [underlying belief]
   - We'll measure success with [metric]
4. Good hypothesis characteristics:
   - Specific (not vague)
   - Measurable (quantifiable outcome)
   - Falsifiable (can be proven wrong)
   - Time-bound (test duration)
   - Focused (one variable at a time)
5. Hypothesis types:
   - Value hypothesis: Will users find this valuable?
   - Usability hypothesis: Can users use this easily?
   - Feasibility hypothesis: Can we build this technically?
   - Viability hypothesis: Is this sustainable for business?
6. Example hypotheses:
   - "If we add social login, 30% more users will complete signup within 2 weeks because password creation is a friction point"
   - "If we show product recommendations, average order value will increase by 15% within 1 month because users discover more products they like"
7. Identifying assumptions:
   - What must be true for this hypothesis to be correct?
   - Riskiest assumptions (test first)
   - Knowns vs unknowns
8. Hypothesis prioritization:
   - Impact (big vs small outcome)
   - Confidence (likely vs unlikely)
   - Ease (easy vs hard to test)
   - ICE score = Impact × Confidence × Ease
9. Hypothesis validation methods:
   - User interviews
   - Surveys
   - A/B tests
   - MVPs
   - Prototypes
   - Analytics
10. Hypothesis canvas:
    - Problem statement
    - Target users
    - Proposed solution
    - Expected outcome
    - Success metrics
    - Test method
11. Common mistakes:
    - Hypothesis is actually a solution ("We need a chatbot")
    - Not measurable ("Users will be happier")
    - Too ambitious ("Revenue will double")
    - No time frame
12. Learning from invalidated hypotheses:
    - Why was our assumption wrong?
    - What did we learn?
    - What's the next hypothesis?
13. Hypothesis tracking:
    - Hypothesis log (all hypotheses)
    - Status (testing, validated, invalidated)
    - Learnings
14. Tools: Miro, FigJam, Google Docs, Notion
15. Real hypothesis examples from successful products

Format: Include hypothesis templates, examples, and prioritization frameworks.

Create the file now.
```

### Skill 2: Experiment Design

```
Create a comprehensive SKILL.md for Experiment Design (A/B testing and beyond).

Location: 48-product-discovery/experiment-design/SKILL.md

Cover:
1. Types of experiments:
   - A/B test (two variants)
   - Multivariate test (multiple changes)
   - Sequential testing
   - Holdout groups (long-term effects)
2. When to experiment:
   - Significant features (high impact)
   - Uncertain outcomes
   - Multiple solution options
   - Optimization opportunities
3. Experiment design process:
   - Define hypothesis
   - Choose metric (primary + secondary)
   - Determine sample size
   - Set test duration
   - Design variants
   - Launch test
   - Analyze results
   - Decide (ship, iterate, kill)
4. Choosing metrics:
   - Primary metric (what we're optimizing)
   - Secondary metrics (guardrails, side effects)
   - Counter metrics (watch for negatives)
   - Example: Primary = Conversion rate, Secondary = Revenue, Counter = Bounce rate
5. Statistical significance:
   - P-value <0.05 (95% confidence)
   - Statistical power (80%+)
   - Minimum detectable effect (MDE)
6. Sample size calculation:
   - Baseline conversion rate
   - Expected improvement (e.g., 10% relative lift)
   - Significance level (α = 0.05)
   - Power (β = 0.80)
   - Tools: Evan Miller's calculator, Optimizely sample size calculator
7. Test duration:
   - At least 1-2 weeks (capture weekly patterns)
   - Full business cycles
   - Enough data for significance
   - Not too long (opportunity cost)
8. Experiment variants:
   - Control (current experience)
   - Treatment (new experience)
   - Multiple treatments (if testing different approaches)
9. Randomization:
   - User-level randomization (consistent experience)
   - Session-level (for anonymous users)
   - Stratified sampling (for segments)
10. Common pitfalls:
    - Peeking (stopping test early when "winning")
    - Sample ratio mismatch (uneven splits)
    - Novelty effect (users trying new thing)
    - Seasonality (testing during holidays)
11. Sequential testing:
    - Allows early stopping (when clear winner)
    - Adjusts significance threshold
    - Tools support: Statsig, GrowthBook
12. Holdout groups:
    - Keep small % of users on old experience
    - Measure long-term effects
    - Detect delayed negative impacts
13. Experiment analysis:
    - Compare primary metric
    - Check secondary metrics
    - Segment analysis (did it work for everyone?)
    - Statistical significance
    - Practical significance (is improvement meaningful?)
14. Decision framework:
    - Ship if: Positive, significant, no red flags
    - Iterate if: Mixed results, some segments good
    - Kill if: Negative, not significant, opportunity cost too high
15. Tools:
    - Feature flags: LaunchDarkly, Split.io, Unleash
    - Experimentation: Optimizely, VWO, GrowthBook, Statsig
    - Analytics: Amplitude, Mixpanel, PostHog
16. A/B testing for engineers:
    - Feature flag implementation
    - Metric instrumentation
    - Data pipeline
    - Results dashboard
17. Real experiment examples:
    - Button color test (classic example)
    - Checkout flow optimization
    - Pricing page variants
    - Onboarding flow
18. Advanced: Bayesian A/B testing

Format: Include experiment templates, statistical calculation examples, and implementation code.

Create the file now.
```

### Skill 3: MVP Scope Control

```
(DUPLICATE - Already covered in Batch 45)
This skill was already defined in the Product Thinking batch.
Skip this one.
```

### Skill 4: User Interviews

```
Create a comprehensive SKILL.md for conducting User Interviews.

Location: 48-product-discovery/user-interviews/SKILL.md

Cover:
1. Why user interviews matter:
   - Understand problems deeply
   - Validate assumptions
   - Uncover needs users can't articulate
   - Build empathy
2. When to conduct interviews:
   - Problem discovery (before building)
   - Solution validation (prototype testing)
   - Usability testing (after building)
   - Continuous learning (ongoing)
3. Types of user interviews:
   - Problem interviews (discover problems)
   - Solution interviews (test solutions)
   - Usability tests (observe product use)
   - Jobs-to-be-Done interviews (deep context)
4. Recruiting participants:
   - Current users (easiest)
   - Target users (not yet customers)
   - Lost users (churned, understand why)
   - Non-users (why they don't use product)
   - Sample size: 5-10 per segment (diminishing returns after)
5. Interview preparation:
   - Research question (what to learn)
   - Interview guide (questions, not script)
   - Recording setup (with permission)
   - Note-taking plan (second person?)
6. Interview structure (60 minutes):
   - Intro (5 min): Build rapport, explain purpose
   - Background (10 min): Context about user
   - Main questions (35 min): Core topics
   - Demo/test (if applicable) (5 min)
   - Wrap-up (5 min): Thank you, next steps
7. Asking good questions:
   - Open-ended ("Tell me about..." not "Do you...")
   - Avoid leading questions ("Don't you think X is frustrating?")
   - Ask about past behavior (not future hypotheticals)
   - "5 Whys" to dig deeper
   - Silence is okay (let them think)
8. Problem interview questions:
   - "Tell me about the last time you [struggled with X]"
   - "What have you tried to solve this?"
   - "If you had a magic wand, what would you change?"
   - "Who else deals with this problem?"
9. Solution interview questions:
   - "What do you think of this approach?"
   - "How would you use this?"
   - "What's missing?"
   - "Would you pay for this? How much?"
10. Usability testing:
    - Give task, observe (don't help)
    - Think-aloud protocol
    - Note where they struggle
    - Ask what they expected vs what happened
11. Interview anti-patterns:
    - Pitching your solution
    - Asking leading questions
    - Ignoring body language/tone
    - Not following up on interesting points
    - Interviewing only friendly users
12. Taking notes:
    - Record audio (with permission)
    - Take written notes (key quotes, observations)
    - Note non-verbal cues
    - Flag surprises/contradictions
13. Analysis and synthesis:
    - Transcribe key parts
    - Highlight insights
    - Look for patterns (themes across interviews)
    - Create user personas or journey maps
    - Share findings with team
14. From interviews to action:
    - What did we learn?
    - What hypotheses were validated/invalidated?
    - What should we build/change/kill?
15. Tools:
    - Recording: Zoom, Google Meet (with consent)
    - Transcription: Otter.ai, Rev
    - Analysis: Dovetail, Miro, Notion
16. Interview scripts and templates
17. Real interview examples and learnings

Format: Include interview guide templates, question banks, and analysis frameworks.

Create the file now.
```

### Skill 5: Validation Metrics

```
Create a comprehensive SKILL.md for choosing and tracking Validation Metrics.

Location: 48-product-discovery/validation-metrics/SKILL.md

Cover:
1. What are validation metrics:
   - Quantifiable proof that hypothesis is correct
   - Leading indicators of success
   - Different from vanity metrics
2. Validation vs vanity metrics:
   - Vanity: "1M signups" (impressive but not actionable)
   - Validation: "30% of signups are active weekly" (actionable)
3. Choosing validation metrics:
   - Tied directly to hypothesis
   - Measurable with current tools
   - Leading (predict future success)
   - Actionable (can optimize)
4. Metric types by stage:
   - Problem validation: Interview requests, survey responses
   - Solution validation: Prototype interactions, waitlist signups
   - MVP validation: Activation, retention, revenue
   - Growth: DAU, WAU, MAU, churn, virality
5. AARRR metrics (Pirate Metrics):
   - Acquisition: Where users come from
   - Activation: First experience, aha moment
   - Retention: Come back and use regularly
   - Referral: Tell others
   - Revenue: Pay for product
6. North Star metric:
   - Single most important metric
   - Aligns with value delivered
   - Examples: Airbnb (nights booked), Slack (messages sent), LinkedIn (endorsements)
7. Input vs output metrics:
   - Input: What we control (features shipped, tests run)
   - Output: What users do (signups, retention)
   - Focus on outputs
8. Leading vs lagging indicators:
   - Leading: Predict future (activation rate → retention)
   - Lagging: Measure past (revenue, churn)
   - Use leading indicators for faster iteration
9. Metrics for different product types:
   - SaaS: MRR, churn, NPS, activation rate
   - E-commerce: Cart abandonment, conversion rate, AOV, repeat purchase
   - Marketplace: Supply/demand balance, GMV, take rate
   - Social: DAU/MAU, posts per user, connections
10. Setting metric targets:
    - Baseline (current state)
    - Target (desired state)
    - Time frame (by when)
    - Example: "Increase activation rate from 20% to 35% in 8 weeks"
11. Metric instrumentation:
    - Event tracking (Segment, Amplitude, Mixpanel)
    - Custom events (user_signed_up, feature_used)
    - User properties (plan, signup_date)
    - Conversion funnels
12. Cohort analysis:
    - Group users by time (signup week)
    - Track retention over time
    - Identify improving/declining cohorts
13. Segmentation:
    - By user type (free vs paid)
    - By channel (organic vs paid)
    - By feature usage (power users vs casual)
14. Metric dashboards:
    - Key metrics visible at all times
    - Daily/weekly/monthly views
    - Trends and anomalies
    - Segmented views
15. Common metric mistakes:
    - Tracking too many metrics (focus on 3-5)
    - Vanity metrics (look good but not useful)
    - Metrics without targets
    - Not segmenting (averages hide insights)
16. From metrics to action:
    - Metric drops → Investigate (what changed?)
    - Metric flat → Experiment (try new approaches)
    - Metric improves → Double down (do more)
17. Tools: Amplitude, Mixpanel, PostHog, Segment, Google Analytics
18. Real metric examples from successful products

Format: Include metric definition templates, instrumentation code, and dashboard examples.

Create the file now.
```

---

## Batch 49: Program/Portfolio Management

### Skill 1: Roadmap Planning

```
Create a comprehensive SKILL.md for technical and product Roadmap Planning.

Location: 49-portfolio-management/roadmap-planning/SKILL.md

Cover:
1. What is a roadmap:
   - Visual plan of work over time
   - Strategic alignment tool
   - Communication device (stakeholders, team)
2. Types of roadmaps:
   - Product roadmap (features, outcomes)
   - Technology roadmap (tech debt, infrastructure)
   - Platform roadmap (shared services)
   - Go-to-market roadmap (launches, marketing)
3. Roadmap timeframes:
   - Now (current quarter): Committed
   - Next (next quarter): Likely
   - Later (beyond 2 quarters): Exploratory
4. Roadmap formats:
   - Timeline roadmap (Gantt-style)
   - Now-Next-Later (flexible)
   - Theme-based (group by goal)
   - Outcome-based (avoid specific features)
5. Roadmap inputs:
   - Company strategy and OKRs
   - User feedback and requests
   - Technical debt and scalability
   - Competitive landscape
   - Platform capabilities
6. Prioritization frameworks:
   - RICE (Reach, Impact, Confidence, Effort)
   - Value vs Effort (2x2 matrix)
   - MoSCoW (Must, Should, Could, Won't)
   - Weighted scoring
7. Creating a roadmap:
   - Start with goals (what to achieve)
   - Identify themes (groups of work)
   - List initiatives (major projects)
   - Estimate effort (t-shirt sizes: S, M, L, XL)
   - Sequence work (dependencies, capacity)
8. Capacity planning:
   - Team velocity (story points or time)
   - Available capacity (minus meetings, support, etc.)
   - Buffer for unknowns (20-30%)
9. Dependencies management:
   - Identify cross-team dependencies
   - Visualize dependencies (network diagram)
   - Risk of blocked work
10. Communicating roadmaps:
    - Executive view (outcomes, business impact)
    - Team view (specific projects, timelines)
    - Customer view (features, benefits)
11. Roadmap tools:
    - ProductBoard
    - Aha!
    - Jira (Roadmap view)
    - Monday.com
    - Miro/FigJam (manual)
12. Roadmap anti-patterns:
    - Feature factory (no outcome focus)
    - Too detailed (Gantt chart with specific dates)
    - Ignoring technical debt
    - Over-committing (no buffer)
    - Not reviewing/updating (stale roadmap)
13. Quarterly planning:
    - Review previous quarter (what shipped, learnings)
    - Align on goals for next quarter
    - Prioritize work
    - Commit to deliverables
14. Roadmap review and updates:
    - Monthly review (are we on track?)
    - Adjust for learnings
    - Rebalance priorities
15. Real roadmap examples (anonymized)
16. Templates: Now-Next-Later, Theme-based, Timeline

Format: Include roadmap templates, prioritization matrices, and communication examples.

Create the file now.
```

### Skill 2: Dependency Mapping

```
Create a comprehensive SKILL.md for Dependency Mapping in complex projects.

Location: 49-portfolio-management/dependency-mapping/SKILL.md

Cover:
1. What are dependencies:
   - Work that relies on other work to complete
   - Types: Technical, team, external, sequential
2. Why dependency mapping matters:
   - Identify risks (blocked work)
   - Sequence work properly
   - Plan capacity realistically
   - Coordinate cross-team work
3. Types of dependencies:
   - Finish-to-Start (most common): B starts after A finishes
   - Start-to-Start: B starts when A starts
   - Finish-to-Finish: B finishes when A finishes
   - External: Depends on vendor, partner, or outside team
4. Dependency identification:
   - Technical dependencies (shared libraries, APIs)
   - Data dependencies (schema changes)
   - Team dependencies (need another team's work)
   - Resource dependencies (shared resources)
   - Knowledge dependencies (need expertise)
5. Dependency mapping techniques:
   - Dependency matrix (grid of projects)
   - Network diagram (nodes and edges)
   - Gantt chart with dependency lines
   - Story mapping with dependencies
6. Visualizing dependencies:
   - Color coding by type
   - Arrows showing direction
   - Critical path highlighting
   - Dependency strength (hard vs soft)
7. Critical path analysis:
   - Longest chain of dependencies
   - Determines minimum project duration
   - Focus optimization here
8. Managing dependencies:
   - Make dependencies explicit (document)
   - Prioritize breaking dependencies (reduce coupling)
   - Coordinate with dependent teams
   - Have contingency plans
9. Reducing dependencies:
   - API contracts (agree interface, implement independently)
   - Feature flags (deploy independently, enable together)
   - Mocks/stubs (develop against fake dependencies)
   - Modular architecture (loose coupling)
10. Dependency risks:
    - Blocked work (upstream not delivered)
    - Cascading delays (one delay affects many)
    - Integration issues (parts don't fit together)
11. Dependency tracking:
    - Dependency register (list all dependencies)
    - Status tracking (blocked, in progress, resolved)
    - Regular check-ins
12. Cross-team coordination:
    - Shared roadmaps
    - Integration meetings
    - Slack channels for coordination
    - Written contracts/agreements
13. Dependency anti-patterns:
    - Hidden dependencies (not documented)
    - Circular dependencies (A → B → A)
    - Too many dependencies (tight coupling)
    - Ignored dependencies (surprise at integration time)
14. Tools:
    - Jira (issue linking)
    - Monday.com (dependency columns)
    - Microsoft Project (Gantt)
    - Miro (visual mapping)
15. Real dependency mapping examples
16. Templates: Dependency matrix, network diagram

Format: Include dependency mapping templates, visualization examples, and coordination workflows.

Create the file now.
```

### Skill 3: Cross-Team Interfaces

```
Create a comprehensive SKILL.md for defining and managing Cross-Team Interfaces.

Location: 49-portfolio-management/cross-team-interfaces/SKILL.md

Cover:
1. What are cross-team interfaces:
   - Contracts between teams
   - APIs, events, data schemas
   - Responsibilities and expectations
2. Why interfaces matter:
   - Enable independent work
   - Reduce miscommunication
   - Allow parallel development
   - Clear ownership
3. Types of interfaces:
   - Technical: REST APIs, GraphQL, gRPC, events
   - Data: Database schemas, file formats, message formats
   - Process: Handoffs, approval workflows, escalations
4. Defining good interfaces:
   - Clear contract (input, output, behavior)
   - Versioned (avoid breaking changes)
   - Documented (API docs, runbooks)
   - Stable (don't change frequently)
   - Testable (integration tests)
5. API design for cross-team:
   - RESTful conventions
   - Consistent naming
   - Error handling standards
   - Authentication/authorization
   - Rate limiting
6. Interface documentation:
   - OpenAPI/Swagger spec
   - Example requests/responses
   - Error codes and meanings
   - Changelog (version history)
   - Contact info (who owns this)
7. Versioning strategies:
   - Semantic versioning (MAJOR.MINOR.PATCH)
   - URL versioning (/v1/, /v2/)
   - Header versioning (Accept-Version)
   - Deprecation policy (notice period)
8. Breaking vs non-breaking changes:
   - Non-breaking: Add optional field, new endpoint
   - Breaking: Remove field, change data type, rename endpoint
   - Communicate breaking changes early
9. Interface agreements (contracts):
   - What each team provides
   - SLAs (response time, uptime)
   - Support process (who to contact)
   - Review process (approvals needed)
10. Integration patterns:
    - Synchronous (REST, gRPC)
    - Asynchronous (message queue, events)
    - Batch (file transfer, scheduled jobs)
11. Testing cross-team integrations:
    - Contract testing (Pact)
    - Integration tests
    - Staging environment tests
    - Mock services for development
12. Communication channels:
    - Shared Slack channel
    - Regular sync meetings
    - Written interface docs
    - Incident escalation path
13. Onboarding to interface:
    - Getting started guide
    - Sample code
    - Sandbox environment
    - Contact for questions
14. Monitoring interfaces:
    - Usage metrics (who's calling, how often)
    - Error rates
    - Latency
    - Breaking change impact
15. Interface anti-patterns:
    - Undocumented interfaces
    - Frequent breaking changes
    - Tight coupling (team B directly queries team A's DB)
    - No versioning
16. Real cross-team interface examples:
    - Payment team API for checkout team
    - Auth team SSO for all teams
    - Data platform events for analytics
17. Templates: API contract template, integration checklist

Format: Include API contract templates, versioning examples, and integration testing patterns.

Create the file now.
```

### Skill 4: Delivery Governance

```
Create a comprehensive SKILL.md for Delivery Governance (ensuring quality and consistency).

Location: 49-portfolio-management/delivery-governance/SKILL.md

Cover:
1. What is delivery governance:
   - Standards and processes for shipping software
   - Quality gates
   - Risk management
   - Compliance checks
2. Why governance matters:
   - Consistent quality
   - Reduce incidents
   - Meet compliance requirements
   - Stakeholder confidence
3. Types of governance:
   - Technical governance (architecture, code quality)
   - Process governance (agile practices, ceremonies)
   - Risk governance (security, compliance)
   - Portfolio governance (prioritization, budget)
4. Quality gates:
   - Code review (required approvals)
   - Automated tests (% coverage, passing)
   - Security scans (vulnerabilities)
   - Performance tests (load testing)
   - Accessibility checks (WCAG compliance)
5. Pre-deployment checklist:
   - [ ] Tests pass (unit, integration, e2e)
   - [ ] Code reviewed and approved
   - [ ] Security scan clean
   - [ ] Performance acceptable
   - [ ] Documentation updated
   - [ ] Runbook created
   - [ ] Rollback plan defined
   - [ ] Stakeholders notified
6. Architecture governance:
   - Architecture Decision Records (ADRs)
   - Design review process
   - Technology standards (approved languages, frameworks)
   - Architecture review board (for major decisions)
7. Code quality standards:
   - Linting (ESLint, Pylint)
   - Formatting (Prettier, Black)
   - Test coverage (>80%)
   - Code complexity (cyclomatic complexity <10)
   - SonarQube/CodeClimate checks
8. Security governance:
   - Dependency scanning (Snyk, Dependabot)
   - SAST (Static Application Security Testing)
   - DAST (Dynamic Application Security Testing)
   - Secret scanning (no API keys in code)
   - Penetration testing (annually)
9. Compliance governance:
   - GDPR/CCPA requirements
   - SOC2 controls
   - HIPAA (if healthcare)
   - Industry-specific regulations
10. Release governance:
    - Change management process
    - Deployment windows (avoid Friday deploys)
    - Staged rollouts (canary, blue-green)
    - Post-deployment monitoring
11. Incident management governance:
    - Severity definitions
    - Escalation procedures
    - Postmortem requirements (SEV0/1)
    - Communication protocols
12. Portfolio governance:
    - Prioritization framework (RICE, Value/Effort)
    - Budget allocation
    - Resource planning
    - Progress tracking (OKRs, KPIs)
13. Governance tools:
    - Jira (workflow enforcement)
    - GitHub (branch protection, required reviews)
    - SonarQube (code quality gates)
    - ServiceNow (change management)
14. Balancing governance and agility:
    - Lightweight processes
    - Automate checks (CI/CD)
    - Risk-based (higher governance for critical systems)
    - Continuous improvement (retrospectives)
15. Governance anti-patterns:
    - Too much bureaucracy (slows down delivery)
    - Too little governance (quality issues, incidents)
    - Manual gates (automate instead)
    - Governance as blocker (should be enabler)
16. Metrics to track:
    - Deployment frequency
    - Lead time for changes
    - Change failure rate
    - Time to restore service
17. Real governance frameworks:
    - COBIT
    - ITIL
    - SAFe (Scaled Agile)
    - Custom lightweight governance
18. Templates: Pre-deployment checklist, ADR template, change request form

Format: Include governance checklists, process diagrams, and quality gate configurations.

Create the file now.
```

---

## Batch 50: Enterprise Integrations & Procurement Reality

### Skill 1: SSO (SAML & OIDC)

```
Create a comprehensive SKILL.md for Single Sign-On (SSO) implementation with SAML and OpenID Connect.

Location: 50-enterprise-integrations/sso-saml-oidc/SKILL.md

Cover:
1. What is SSO:
   - Single authentication for multiple applications
   - Centralized identity management
   - Better security (one strong password vs many weak)
2. Why enterprises require SSO:
   - IT control over user access
   - Audit and compliance
   - Onboarding/offboarding automation
   - Better security
3. SSO protocols:
   - SAML 2.0 (older, XML-based, enterprise standard)
   - OpenID Connect (OIDC) (modern, JSON-based, OAuth 2.0)
   - Comparison: When to use each
4. SAML flow:
   - SP-initiated (Service Provider starts)
   - IdP-initiated (Identity Provider starts)
   - Assertion (signed XML token with user info)
5. OIDC flow:
   - Authorization Code flow (most common for web apps)
   - ID Token (JWT with user claims)
   - Access Token (for API calls)
   - Refresh Token (long-lived access)
6. Popular identity providers:
   - Okta
   - Auth0
   - Azure AD (Entra ID)
   - Google Workspace
   - OneLogin
   - JumpCloud
7. Implementing SAML:
   - Libraries: passport-saml (Node.js), python-saml, ruby-saml
   - Metadata exchange (IdP metadata, SP metadata)
   - Certificate management (signing, encryption)
   - Attribute mapping (email, name, groups)
8. Implementing OIDC:
   - Libraries: passport-openidconnect, authlib (Python)
   - Discovery endpoint (.well-known/openid-configuration)
   - Client ID and secret
   - Redirect URIs (whitelist)
   - Claims (standard: sub, email, name)
9. Just-In-Time (JIT) provisioning:
   - Create user on first SSO login
   - Update user attributes on each login
   - vs SCIM (push provisioning)
10. Group/role mapping:
    - IdP sends group claims
    - Map IdP groups to application roles
    - Admin, User, Viewer, etc.
11. Multi-tenancy with SSO:
    - Different IdP per customer
    - Tenant identification (domain, custom URL)
    - Multiple SAML/OIDC configs
12. SSO debugging:
    - SAML tracer (browser extension)
    - JWT decoder (jwt.io)
    - Logs (authentication attempts)
    - Common errors (certificate mismatch, clock skew, invalid signature)
13. Security considerations:
    - Validate signatures (SAML assertion, JWT)
    - Check token expiration
    - Audience validation (token is for your app)
    - HTTPS only
    - Secure session management
14. Testing SSO:
    - Test IdP accounts
    - Mock IdP for development
    - Manual testing with customer IdP
    - Automated tests (headless browser)
15. SSO for different user types:
    - Enterprise customers (required)
    - Small business (optional, Google/Microsoft social login)
    - Consumers (social login, not SSO)
16. Pricing SSO (common B2B SaaS pattern):
    - Basic plan: No SSO
    - Business plan: SAML SSO
    - Enterprise plan: SAML + SCIM
17. Implementation examples:
    - Node.js + Passport + SAML
    - Python + Flask + OIDC
    - Next.js + NextAuth.js
18. Real SSO integration scenarios

Format: Include SAML/OIDC flow diagrams, configuration examples, and implementation code.

Create the file now.
```

### Skill 2: SCIM Provisioning

```
Create a comprehensive SKILL.md for SCIM (System for Cross-domain Identity Management) user provisioning.

Location: 50-enterprise-integrations/scim-provisioning/SKILL.md

Cover:
1. What is SCIM:
   - Standard for automating user provisioning
   - Push-based (IdP pushes changes to your app)
   - REST API for user management
2. Why enterprises need SCIM:
   - Automate onboarding (create user in all apps)
   - Automate offboarding (deactivate user everywhere)
   - Keep user info in sync (name, email, role changes)
   - IT admin control
3. SCIM vs JIT provisioning:
   - JIT: User created on first login (pull)
   - SCIM: IdP creates user proactively (push)
   - SCIM is preferred for enterprise
4. SCIM 2.0 specification:
   - RFC 7643 (Core Schema)
   - RFC 7644 (Protocol)
   - Resources: Users, Groups
5. SCIM endpoints:
   - GET /Users - List users
   - POST /Users - Create user
   - GET /Users/:id - Get user
   - PUT/PATCH /Users/:id - Update user
   - DELETE /Users/:id - Deactivate user
   - GET /Groups - List groups
   - POST /Groups - Create group
6. SCIM User schema:
   - userName (unique identifier)
   - email (primary)
   - name (givenName, familyName)
   - active (boolean, for soft delete)
   - groups (array of group IDs)
7. SCIM authentication:
   - OAuth 2.0 Bearer token (recommended)
   - Basic auth (less secure)
   - API key (custom)
8. Implementing SCIM server:
   - Libraries: scim2-server (Java), django-scim2, express-scim
   - Database schema (users, groups, memberships)
   - Authentication (validate bearer token)
   - Pagination (startIndex, count)
   - Filtering (userName eq "john@example.com")
9. SCIM operations:
   - Create user → Create in your database
   - Update user → Update attributes
   - Deactivate user → Set active=false (soft delete)
   - Add to group → Update user's groups array
10. Error handling:
    - 400 Bad Request (invalid data)
    - 401 Unauthorized (invalid token)
    - 404 Not Found (user doesn't exist)
    - 409 Conflict (userName already exists)
    - 500 Internal Server Error
11. Testing SCIM:
    - Manual testing (Postman, curl)
    - SCIM test suite (Runscope SCIM validator)
    - Integration testing with actual IdP
12. SCIM IdP configuration:
    - SCIM endpoint URL (https://yourapp.com/scim/v2/)
    - Bearer token
    - Attribute mapping (IdP fields → SCIM fields)
13. Handling SCIM edge cases:
    - User already exists (return 409)
    - Email change (unique constraint)
    - Group doesn't exist (create it or error?)
    - Partial updates (PATCH with specific fields)
14. SCIM for multi-tenancy:
    - Tenant-specific SCIM endpoints
    - Or tenant ID in bearer token
    - Isolate users by tenant
15. Monitoring SCIM:
    - Provisioning success rate
    - Failed operations (log and alert)
    - Sync status (users in sync with IdP)
16. Common SCIM providers:
    - Okta (SCIM 2.0)
    - Azure AD (SCIM 2.0)
    - OneLogin (SCIM 2.0)
    - Google Workspace (custom, not full SCIM)
17. Implementation examples:
    - Node.js Express SCIM server
    - Python Flask SCIM server
    - Database schema for SCIM
18. Real SCIM integration scenarios

Format: Include SCIM endpoint examples, request/response samples, and implementation code.

Create the file now.
```

### Skill 3: Enterprise RBAC Models

```
Create a comprehensive SKILL.md for Enterprise Role-Based Access Control (RBAC) models.

Location: 50-enterprise-integrations/enterprise-rbac-models/SKILL.md

Cover:
1. What is RBAC:
   - Users → Roles → Permissions
   - vs ACL (Access Control List): Direct user permissions
   - vs ABAC (Attribute-Based): Policy-based decisions
2. Why enterprises need RBAC:
   - Scalable (assign role, not individual permissions)
   - Auditable (who has what access)
   - Least privilege principle
   - Segregation of duties
3. RBAC components:
   - Users (people or service accounts)
   - Roles (Admin, Manager, Member, Viewer)
   - Permissions (create_project, delete_user, view_reports)
   - Resources (projects, files, reports)
4. Common enterprise roles:
   - Owner/Admin (full control)
   - Manager/Editor (create, edit, delete)
   - Member/Contributor (create, edit own)
   - Viewer/Reader (read-only)
   - Billing Admin (manage billing only)
   - Support (limited access for support)
5. Permission naming conventions:
   - resource:action (project:create, user:delete)
   - Or action_resource (create_project, delete_user)
   - Consistent naming across application
6. Hierarchical roles:
   - Admin inherits all permissions of Manager
   - Manager inherits all of Member
   - Member inherits all of Viewer
7. Custom roles (enterprise feature):
   - Customer defines their own roles
   - Assign specific permissions
   - Example: "Auditor" with read-only access to logs and reports
8. Multi-level RBAC:
   - Organization level (org-wide admin)
   - Project/workspace level (project admin)
   - Resource level (document owner)
9. RBAC implementation patterns:
   - Database schema (users, roles, permissions, user_roles, role_permissions)
   - Junction tables for many-to-many
   - Check permission: Does user have role that has this permission?
10. Permission checking:
    - hasPermission(user, 'project:delete', projectId)
    - Middleware for API routes
    - UI components (hide buttons user can't use)
11. RBAC with teams:
    - Users belong to teams
    - Teams have roles in workspaces
    - User inherits permissions from team roles
12. RBAC with SSO:
    - Map SSO groups to application roles
    - Automatic role assignment on login
    - Override SSO-assigned roles (if allowed)
13. Permission inheritance:
    - Org admin → automatically admin of all projects
    - Project member → can view project and resources in it
14. Conditional permissions:
    - Resource owner (can edit own documents)
    - Time-based (temporary access)
    - Approval-based (request access)
15. RBAC testing:
    - Test each role has correct permissions
    - Test permission inheritance
    - Test permission checks in API
    - Test UI shows/hides correctly
16. RBAC audit logging:
    - Log permission changes
    - Log access attempts (allowed and denied)
    - Regular access reviews
17. Tools and libraries:
    - Casbin (policy engine)
    - Oso (authorization library)
    - AWS IAM (inspiration for design)
    - Custom implementation
18. Real RBAC models:
    - GitHub (Owner, Maintainer, Member, Reader)
    - Google Workspace (Super Admin, Admin, User)
    - Salesforce (System Admin, Standard User, custom)
19. Implementation examples:
    - Database schema for RBAC
    - Permission checking functions
    - Middleware for API routes

Format: Include RBAC model diagrams, database schemas, and permission checking code.

Create the file now.
```

### Skill 4: Security Questionnaires

```
Create a comprehensive SKILL.md for handling Enterprise Security Questionnaires.

Location: 50-enterprise-integrations/security-questionnaires/SKILL.md

Cover:
1. What are security questionnaires:
   - Long surveys (100-500 questions) from enterprise customers
   - Assess vendor security practices
   - Required before procurement approval
2. Why they matter:
   - Blocker for enterprise sales
   - Repeated for every large customer
   - Time-consuming (20-40 hours for first time)
3. Common questionnaire types:
   - Standard questionnaires (CAIQ, SIG, VSAQ)
   - Custom questionnaires (each customer's format)
   - Self-assessments (SOC2, ISO 27001)
4. Topics covered:
   - Company info (size, location, ownership)
   - Data security (encryption, access controls)
   - Infrastructure (cloud provider, DR, backups)
   - Compliance (GDPR, SOC2, ISO 27001, HIPAA)
   - Incident response (process, history)
   - Access management (SSO, MFA, RBAC)
   - Development practices (code review, testing, CI/CD)
   - Third-party vendors (subprocessors)
   - Physical security (datacenter security, if applicable)
   - HR practices (background checks, training)
5. Preparing for questionnaires:
   - Security documentation (policies, procedures)
   - Compliance certifications (SOC2, ISO 27001)
   - Standard responses library
   - Evidence files (screenshots, certificates)
6. Standard responses library:
   - Maintain document with answers to common questions
   - Update once, reuse many times
   - Example questions:
     * "Do you encrypt data at rest?" → "Yes, AES-256"
     * "Where is data stored?" → "AWS us-east-1 and us-west-2"
     * "Do you support SSO?" → "Yes, SAML 2.0 and OIDC"
7. Evidence collection:
   - Encryption certificates
   - SOC2 report (Type II)
   - ISO 27001 certificate
   - Penetration test results
   - Disaster recovery test results
   - Incident response plan document
8. Tools for questionnaires:
   - Whistic (questionnaire automation)
   - SafeBase (security portal)
   - Vanta (compliance + questionnaires)
   - Drata (similar to Vanta)
   - Manual (Google Docs/Sheets)
9. Streamlining the process:
   - Trust center (public security documentation)
   - Self-service security portal
   - Standard questionnaire (accept yours instead)
   - Pre-filled responses (share library)
10. Common challenging questions:
    - "Have you had any security breaches?" (honesty + mitigation)
    - "Do you have cyber insurance?" (get it if selling to enterprise)
    - "What's your RTO/RPO?" (need DR plan)
    - "Who has access to production data?" (need access logs)
11. Red flags to avoid:
    - "We don't know" (looks unprepared)
    - "N/A" without explanation
    - Inconsistent answers
    - Missing evidence
    - Outdated documentation
12. Questionnaire workflow:
    - Customer sends questionnaire
    - Assign sections to team members
    - Fill out answers with evidence
    - Internal review (security, legal)
    - Submit to customer
    - Follow-up calls/clarifications
    - Approval (hopefully!)
13. Maintaining questionnaire readiness:
    - Keep security documentation updated
    - Renew certifications (SOC2 annually)
    - Regular penetration tests
    - Incident response drills
    - Update standard responses library
14. Delegating questionnaire completion:
    - Sales team (basic questions)
    - Engineering (technical questions)
    - Security team (security controls)
    - Legal (contracts, privacy)
    - Finance (insurance, certifications)
15. Timeline expectations:
    - First questionnaire: 20-40 hours
    - Subsequent: 5-10 hours (with library)
    - Customer review: 1-2 weeks
    - Follow-up: 1-2 rounds
16. Real questionnaire examples (sanitized)
17. Templates: Standard response library, evidence checklist

Format: Include questionnaire examples, response templates, and workflow diagrams.

Create the file now.
```

### Skill 5: Vendor Onboarding

```
Create a comprehensive SKILL.md for Enterprise Vendor Onboarding processes.

Location: 50-enterprise-integrations/vendor-onboarding/SKILL.md

Cover:
1. What is vendor onboarding:
   - Process enterprise customers follow before using your product
   - Due diligence, approvals, contracts, technical setup
   - Can take 3-12 months for large enterprises
2. Why it matters:
   - Understanding customer timelines (sales cycle)
   - Anticipate requirements
   - Prepare documentation and support
   - Avoid surprises that delay deals
3. Vendor onboarding stages:
   - Discovery and evaluation (demos, POC)
   - Security review (questionnaires, audits)
   - Legal review (contracts, terms)
   - Procurement (PO, invoicing)
   - Technical onboarding (SSO, SCIM, integration)
   - User training and rollout
4. Security review stage:
   - Security questionnaires (100-500 questions)
   - Compliance certifications (SOC2, ISO 27001)
   - Penetration testing (yours or theirs)
   - Data Processing Agreement (DPA)
   - Business Associate Agreement (BAA for HIPAA)
5. Legal review stage:
   - Master Service Agreement (MSA)
   - Terms of Service (ToS)
   - Service Level Agreement (SLA)
   - Data Processing Agreement (DPA)
   - Negotiation (liability caps, indemnification)
6. Procurement stage:
   - Get into vendor database
   - Purchase Order (PO) process
   - Invoicing (specific formats required)
   - Payment terms (Net 30, Net 60, etc.)
7. Technical onboarding:
   - SSO configuration (SAML or OIDC)
   - SCIM provisioning setup
   - IP whitelisting (if required)
   - Subdomain or vanity URL
   - Integration with other systems
8. User training:
   - Admin training (configuration, user management)
   - End user training (how to use product)
   - Training materials (videos, docs, webinars)
   - Certification programs (for admins)
9. Vendor onboarding timeline:
   - Small business: 1-4 weeks
   - Mid-market: 4-12 weeks
   - Enterprise: 3-12 months
10. Requirements by customer size:
    - SMB: Credit card, basic ToS
    - Mid-market: Annual contract, basic security review
    - Enterprise: Everything (MSA, DPA, SOC2, SSO, SCIM)
11. Preparing for onboarding:
    - Standard contracts (MSA template)
    - Security documentation (trust center)
    - Compliance certifications (SOC2, ISO 27001)
    - Onboarding documentation (step-by-step guides)
    - Customer success team (for onboarding support)
12. Common blockers:
    - Missing SOC2 report (get one!)
    - No SSO support (must-have for enterprise)
    - Unacceptable contract terms (liability, indemnification)
    - Security concerns (unresolved questionnaire items)
    - Missing features (integration requirements)
13. Accelerating onboarding:
    - Self-service onboarding (for smaller customers)
    - Pre-approved security documentation
    - Standard contract (no negotiation)
    - White-glove onboarding (dedicated CSM for enterprise)
14. Onboarding checklist:
    - [ ] Security questionnaire completed
    - [ ] SOC2/ISO certification shared
    - [ ] MSA signed
    - [ ] DPA signed
    - [ ] Purchase Order received
    - [ ] SSO configured
    - [ ] SCIM configured (if applicable)
    - [ ] Admin training completed
    - [ ] Users provisioned
    - [ ] Go-live date confirmed
15. Tools for onboarding:
    - CRM (Salesforce, HubSpot) for tracking
    - Project management (Asana, Monday.com)
    - Document signing (DocuSign, PandaDoc)
    - Security portal (SafeBase, Whistic)
16. Customer success role:
    - Dedicated CSM for enterprise
    - Onboarding project plan
    - Regular check-ins
    - Success metrics (time to value)
17. Real vendor onboarding stories
18. Templates: Onboarding checklist, project plan

Format: Include onboarding timelines, checklists, and process diagrams.

Create the file now.
```

---

## Summary

Total new prompts created: **22 skills** across 5 batches

### Batch Breakdown:
- **46-data-classification**: 4 skills (PII detection, logging redaction, retention/deletion, access audits)
- **47-performance-engineering**: 5 skills (profiling, DB optimization, caching, concurrency, SLO/SLI)
- **48-product-discovery**: 4 skills (hypothesis writing, experiment design, user interviews, validation metrics)
- **49-portfolio-management**: 4 skills (roadmap planning, dependency mapping, cross-team interfaces, delivery governance)
- **50-enterprise-integrations**: 5 skills (SSO, SCIM, Enterprise RBAC, security questionnaires, vendor onboarding)

### Combined with Previous Batches:
- **Batch 00-45**: 37 skills
- **Batch 46-50**: 22 skills
- **Total**: **59 NEW enterprise skills**

These final 5 batches address the critical gap between "we're compliant on paper" and "we can actually sell to and operate in enterprise environments".

---

## Next Steps

### Recommended Generation Order:

**Week 1: Performance Engineering (47)**
- Most immediately useful for any production system
- Profiling → DB optimization → Caching → Concurrency → SLOs

**Week 2: Data Classification (46)**
- Required for GDPR/PDPA compliance in practice
- PII detection → Logging redaction → Retention → Audits

**Week 3: Product Discovery (48)**
- For product teams and engineers who want product thinking
- Hypothesis → Experiments → User interviews → Metrics

**Week 4: Enterprise Integration (50)**
- When selling to enterprise B2B
- SSO → SCIM → RBAC → Security questionnaires → Vendor onboarding

**Week 5: Portfolio Management (49)**
- For teams managing multiple projects
- Roadmap → Dependencies → Cross-team → Governance

---

Would you like me to:
1. ✅ Generate the first batch (Performance Engineering) as examples?
2. ✅ Create a combined master prompt file with all 59 skills?
3. ✅ Create a priority matrix (which skills to do first based on your needs)?
4. ✅ Update the GitHub repo structure document with all batches?

บอกได้เลยครับ! 🎯