# Final 8 Production-Ready Skills - Complete Prompts

Complete prompts for creating 8 critical production skills covering data contracts, AI evaluation, requirements management, orchestration, and cost estimation.

---

## Batch 51: Data Contracts & API Governance

### Skill 1: OpenAPI Governance

```
Create a comprehensive SKILL.md for OpenAPI Governance and API standards.

Location: 51-contracts-governance/openapi-governance/SKILL.md

Cover:
1. What is OpenAPI governance:
   - Enforcing API design standards
   - Consistent API patterns across organization
   - Automated validation and linting
   - API lifecycle management
2. Why governance matters:
   - Consistency (developers know what to expect)
   - Quality (catch issues before production)
   - Documentation (auto-generated, always in sync)
   - Breaking change prevention
3. OpenAPI Specification (OAS) 3.0/3.1:
   - Structure (info, servers, paths, components, security)
   - Data types and schemas
   - Request/response definitions
   - Authentication schemes
4. API design standards:
   - RESTful conventions (resource naming, HTTP methods)
   - URL structure (/api/v1/resources/:id)
   - Query parameters (pagination, filtering, sorting)
   - Request/response format (JSON, consistent structure)
   - Error format (RFC 7807 Problem Details)
   - Date format (ISO 8601)
   - Pagination (cursor vs offset)
5. Naming conventions:
   - Resource names: Plural nouns (users, projects, orders)
   - Fields: camelCase or snake_case (be consistent)
   - Enums: UPPER_SNAKE_CASE
   - Boolean fields: is/has prefix (isActive, hasAccess)
6. OpenAPI linting:
   - Spectral (popular linter)
   - Custom rules (organization-specific)
   - CI/CD integration (fail build on violations)
7. Common linting rules:
   - All operations have description
   - All parameters have description
   - All responses have schema
   - No empty descriptions
   - Consistent naming conventions
   - Security schemes defined
   - Examples provided
8. Breaking change detection:
   - openapiDiff tool
   - Breaking: Remove field, change type, remove endpoint
   - Non-breaking: Add field, add endpoint, add enum value
   - Semver for API versions
9. API documentation generation:
   - Swagger UI (interactive docs)
   - ReDoc (beautiful static docs)
   - Stoplight (design-first platform)
   - Postman (import OpenAPI)
10. Design-first vs code-first:
    - Design-first: Write OpenAPI spec, generate code
    - Code-first: Write code, generate OpenAPI spec
    - Hybrid: Write spec + code, keep in sync
11. OpenAPI tooling:
    - Editor: Swagger Editor, Stoplight Studio
    - Linter: Spectral
    - Validator: openapi-validator
    - Generator: openapi-generator (clients, servers)
    - Diff: oasdiff, openapi-diff
12. Governance workflow:
    - Developer writes/updates OpenAPI spec
    - Automated linting (CI)
    - Breaking change check (CI)
    - Review by API guild
    - Merge to main
    - Auto-publish docs
13. API versioning strategy:
    - URL versioning (/v1/, /v2/)
    - Header versioning (Accept-Version: v1)
    - No versioning (only non-breaking changes)
    - Deprecation policy (6-12 months notice)
14. Deprecation headers:
    - Sunset header (RFC 8594)
    - Link to migration guide
    - Warnings in response headers
15. Multi-team API governance:
    - Centralized API registry
    - API review board
    - Style guide document
    - Shared Spectral ruleset
16. Monitoring API compliance:
    - Spec coverage (% of endpoints documented)
    - Linting violations over time
    - Breaking changes deployed
17. Real-world governance examples:
    - Stripe API (excellent consistency)
    - GitHub API (comprehensive docs)
    - Internal API gateway patterns
18. Implementation:
    - Spectral ruleset (YAML)
    - CI/CD pipeline (GitHub Actions)
    - OpenAPI spec templates

Format: Include OpenAPI spec examples, Spectral rules, and CI/CD integration configs.

Create the file now.
```

### Skill 2: Event Schema Registry

```
Create a comprehensive SKILL.md for Event Schema Registry and event-driven architecture governance.

Location: 51-contracts-governance/event-schema-registry/SKILL.md

Cover:
1. What is event schema registry:
   - Centralized repository of event schemas
   - Versioning and evolution management
   - Validation of events at runtime
   - Compatibility checking
2. Why schema registry matters:
   - Prevents breaking changes in event streams
   - Self-documenting events
   - Type safety across producers/consumers
   - Contract between services
3. Schema formats:
   - JSON Schema (flexible, widely supported)
   - Avro (compact, schema evolution)
   - Protobuf (efficient, strongly typed)
   - Comparison: When to use each
4. Schema registry implementations:
   - Confluent Schema Registry (for Kafka)
   - AWS Glue Schema Registry
   - Azure Schema Registry
   - Custom registry (database + API)
5. Schema structure:
   - Event metadata (id, timestamp, version)
   - Event type (user.created, order.placed)
   - Event payload (actual data)
   - Schema version
6. Schema evolution rules:
   - Forward compatibility (new consumer, old producer)
   - Backward compatibility (old consumer, new producer)
   - Full compatibility (both directions)
   - Breaking changes (require major version)
7. Compatible changes:
   - Add optional field
   - Remove optional field
   - Add new event type
   - Add enum value (at end)
8. Breaking changes:
   - Remove required field
   - Change field type
   - Rename field
   - Change field semantics
9. Schema versioning:
   - Semantic versioning (MAJOR.MINOR.PATCH)
   - Major: Breaking changes
   - Minor: Backward-compatible additions
   - Patch: Bug fixes (no schema change)
10. Event naming conventions:
    - Format: domain.entity.action
    - Examples: user.account.created, order.payment.processed
    - Past tense (event already happened)
    - Specific (not too generic)
11. Schema validation:
    - Producer-side validation (before publish)
    - Consumer-side validation (after receive)
    - Schema registry enforcement
12. Schema discovery:
    - Searchable registry UI
    - Documentation generation
    - Example events
    - Consumer/producer tracking (who uses what)
13. Multi-environment schemas:
    - Dev, staging, prod registries
    - Schema promotion workflow
    - Testing schema changes
14. Schema governance workflow:
    - Developer proposes schema (PR)
    - Automated compatibility check (CI)
    - Review by data team
    - Register schema in registry
    - Deploy producer/consumer code
15. Dead letter queue (DLQ):
    - Invalid events go to DLQ
    - Monitor DLQ for schema violations
    - Fix and replay
16. Schema migration:
    - Dual publishing (old + new schema)
    - Consumer migration
    - Deprecate old schema
17. Tools and libraries:
    - Confluent Schema Registry
    - JSON Schema validators
    - Avro/Protobuf libraries
    - Schema registry clients
18. Real-world event schemas:
    - Kafka event schemas
    - Webhook payloads
    - CloudEvents standard
19. Implementation examples:
    - Schema registry setup
    - Producer with schema validation
    - Consumer with schema validation
    - Compatibility testing

Format: Include schema examples (JSON Schema, Avro), registry API examples, and validation code.

Create the file now.
```

### Skill 3: Backward Compatibility Rules

```
Create a comprehensive SKILL.md for Backward Compatibility Rules in APIs and data contracts.

Location: 51-contracts-governance/backward-compat-rules/SKILL.md

Cover:
1. What is backward compatibility:
   - New version works with old clients
   - No breaking changes
   - Evolutionary design
2. Why backward compatibility matters:
   - Avoid breaking existing integrations
   - Gradual migration (not big bang)
   - Reduce coordination overhead
   - Customer trust (stable APIs)
3. Compatibility levels:
   - Backward compatible (new server, old client)
   - Forward compatible (old server, new client)
   - Full compatible (both directions)
   - Breaking change (incompatible)
4. REST API backward compatibility:
   - Safe changes:
     * Add new endpoint
     * Add optional field to request
     * Add field to response
     * Add enum value (at end)
     * Relax validation (accept more)
   - Breaking changes:
     * Remove endpoint
     * Remove field from response
     * Add required field to request
     * Change field type
     * Rename field
     * Change semantics
5. Database schema compatibility:
   - Safe migrations:
     * Add nullable column
     * Add table
     * Add index
   - Breaking migrations:
     * Drop column (requires multi-step migration)
     * Rename column (use views/aliases)
     * Change column type
6. Event/message compatibility:
   - Safe changes:
     * Add optional field
     * Add new event type
   - Breaking changes:
     * Remove field
     * Change field type
     * Rename field
7. GraphQL compatibility:
   - Safe changes:
     * Add new field to type
     * Add new type
     * Add new query/mutation
   - Breaking changes:
     * Remove field
     * Change field type
     * Change field arguments
8. Deprecation strategy:
   - Mark as deprecated (in docs, code, headers)
   - Provide migration guide
   - Set sunset date (6-12 months)
   - Warn clients (in response headers)
   - Monitor usage
   - Remove after sunset
9. Multi-step migrations:
   - Step 1: Add new field, both fields populated
   - Step 2: Clients migrate to new field
   - Step 3: Stop populating old field (still present)
   - Step 4: Remove old field
10. API versioning strategies:
    - URL versioning (/v1/, /v2/)
    - Header versioning (Accept-Version: v1)
    - No versioning (only non-breaking changes)
11. Testing backward compatibility:
    - Contract tests (Pact)
    - Integration tests with old clients
    - Schema compatibility checks (automated)
    - Canary deployments
12. Compatibility checking tools:
    - OpenAPI: oasdiff, openapi-diff
    - GraphQL: graphql-inspector
    - Protobuf: buf breaking
    - JSON Schema: schema validators
13. Communicating breaking changes:
    - Changelog (what changed)
    - Migration guide (how to update)
    - Deprecation notice (when will it break)
    - Direct outreach (email major clients)
14. Handling inevitable breaking changes:
    - Major version bump (v1 → v2)
    - Maintain v1 for transition period
    - Clear migration path
    - Tools to help migrate
15. Real-world examples:
    - Stripe API evolution
    - AWS API backward compatibility
    - GraphQL schema evolution
16. Best practices checklist:
    - [ ] All changes reviewed for compatibility
    - [ ] Automated compatibility checks in CI
    - [ ] Deprecation process defined
    - [ ] Migration guides for breaking changes
    - [ ] Versioning strategy documented
17. Implementation:
    - Compatibility check scripts
    - CI/CD integration
    - Deprecation header middleware

Format: Include compatibility matrices, migration examples, and testing strategies.

Create the file now.
```

### Skill 4: Contract Testing

```
Create a comprehensive SKILL.md for Contract Testing (Consumer-Driven Contracts).

Location: 51-contracts-governance/contract-testing/SKILL.md

Cover:
1. What is contract testing:
   - Testing agreements between services
   - Consumer defines expectations (contract)
   - Provider verifies it meets contract
   - Catch integration issues early
2. Why contract testing matters:
   - Avoid breaking consumers
   - Test independently (no integrated env)
   - Faster feedback (no coordinated testing)
   - Documentation (contracts = specs)
3. Contract testing vs integration testing:
   - Integration: Test actual integration (slower, fragile)
   - Contract: Test against contract (faster, isolated)
   - Use both (contracts for most, integration for critical paths)
4. Consumer-Driven Contract (CDC):
   - Consumer defines what it needs
   - Provider verifies it can provide
   - vs Provider-Driven (provider defines, take it or leave it)
5. Pact framework:
   - Popular CDC tool
   - Supports HTTP, messages, GraphQL
   - Consumer writes Pact tests
   - Provider verifies against Pact
   - Pact Broker (central registry)
6. Contract testing workflow:
   - Consumer writes contract test (Pact)
   - Consumer test runs, generates contract JSON
   - Contract published to Pact Broker
   - Provider pulls contract
   - Provider verification runs
   - Both sides pass → safe to deploy
7. Writing consumer contracts (Pact):
   - Mock provider in consumer tests
   - Define expectations (request + expected response)
   - Generate contract file
   - Publish to broker
8. Provider verification (Pact):
   - Pull contract from broker
   - Replay contract requests against provider
   - Verify responses match expectations
   - Publish verification results
9. Pact Broker:
   - Central registry of contracts
   - Version management
   - Can-I-Deploy check (are contracts compatible?)
   - Webhooks (trigger provider verification)
10. Can-I-Deploy:
    - Check before deploying
    - Is provider compatible with all consumers?
    - Is consumer compatible with provider?
    - Green = safe to deploy
11. Bi-directional contracts:
    - Provider defines OpenAPI spec
    - Consumer defines Pact
    - Both verified against each other
    - Best of both worlds
12. Testing event-driven contracts:
    - Message Pact (for async messages)
    - Consumer expects message format
    - Provider verifies it produces correct format
13. Contract testing best practices:
    - Test behavior, not implementation
    - One contract per consumer-provider pair
    - Version contracts
    - Run verification on every provider change
    - Use Can-I-Deploy in CI/CD
14. Common pitfalls:
    - Testing too much (test contracts, not business logic)
    - Not versioning contracts
    - Provider verification not in CI
    - Ignoring failed verifications
15. Tools:
    - Pact (most popular)
    - Spring Cloud Contract (Java)
    - Specmatic (OpenAPI contracts)
16. CI/CD integration:
    - Consumer tests generate contract
    - Publish to broker (if tests pass)
    - Provider verification triggered (webhook)
    - Can-I-Deploy gate before deployment
17. Real-world contract testing:
    - Microservices (service-to-service)
    - API consumers (mobile, web)
    - Event-driven (message contracts)
18. Implementation examples:
    - Pact consumer test (JavaScript, Python)
    - Pact provider verification
    - Pact Broker setup
    - CI/CD pipeline integration

Format: Include Pact test examples, verification configs, and workflow diagrams.

Create the file now.
```

### Skill 5: Deprecation Notices

```
Create a comprehensive SKILL.md for API Deprecation Notices and sunset processes.

Location: 51-contracts-governance/deprecation-notices/SKILL.md

Cover:
1. What is deprecation:
   - Announcing end-of-life for API/feature
   - Giving users time to migrate
   - Eventual removal
2. Why proper deprecation matters:
   - Avoid breaking users without warning
   - Maintain trust
   - Smooth migration
   - Legal compliance (if contractual)
3. Deprecation timeline:
   - Typical: 6-12 months for APIs
   - Critical systems: 12-24 months
   - Internal APIs: 3-6 months
   - Consider: Contract terms, user base size
4. Deprecation process:
   - Step 1: Mark as deprecated (code, docs)
   - Step 2: Announce (email, blog, changelog)
   - Step 3: Monitor usage
   - Step 4: Reach out to active users
   - Step 5: Sunset (stop working)
   - Step 6: Remove code
5. Deprecation headers (HTTP):
   - Deprecation: true (draft RFC)
   - Sunset: Sat, 31 Dec 2024 23:59:59 GMT (RFC 8594)
   - Link: <migration-guide-url>; rel="sunset"
   - Warning: "299 - 'Deprecated. See docs.'"
6. OpenAPI deprecation:
   - deprecated: true (in operation or parameter)
   - description: Migration guide link
7. GraphQL deprecation:
   - @deprecated directive
   - deprecationReason: "Use newField instead"
8. Code deprecation:
   - @deprecated annotation (Java)
   - @deprecated JSDoc (JavaScript)
   - warnings.warn (Python)
9. Communication channels:
   - In-app notifications (for logged-in users)
   - Email campaigns (to all API users)
   - Blog post (public announcement)
   - Changelog (detailed info)
   - Status page updates
   - Release notes
10. Migration guide:
    - Why deprecating (reason)
    - What to use instead (alternative)
    - How to migrate (step-by-step)
    - Code examples (before/after)
    - Timeline (when it stops working)
    - Support contact (if help needed)
11. Monitoring deprecated usage:
    - Track API calls to deprecated endpoints
    - Identify top users
    - Usage trends (is it declining?)
    - Alert when usage spikes
12. Outreach to users:
    - Email top users (direct outreach)
    - Offer migration support
    - Schedule calls with major customers
    - Provide early access to new version
13. Handling non-compliant users:
    - Repeated notices
    - Escalation (account manager)
    - Final warning (1 month before)
    - Hard cutoff (stop working)
14. Graceful degradation:
    - Return 410 Gone (after sunset)
    - Helpful error message (link to guide)
    - Optional: Temporary disable (test waters)
15. Versioning and deprecation:
    - v1 deprecated → use v2
    - Maintain v1 during transition
    - Eventually remove v1
16. Database schema deprecation:
    - Multi-step migration
    - Stop writing to old column
    - Stop reading (use new column)
    - Drop old column
17. Feature flag deprecation:
    - Mark feature as deprecated
    - Monitor usage
    - Reach out to enabled users
    - Force disable
    - Remove code
18. Real deprecation examples:
    - Twitter API v1 → v2
    - GitHub API v3 deprecations
    - Heroku free tier sunset
19. Templates:
    - Deprecation announcement (email, blog)
    - Migration guide
    - API response headers

Format: Include deprecation notice templates, communication timelines, and code examples.

Create the file now.
```

---

## Batch 52: AI Evaluation & Benchmarking

### Skill 1: RAG Evaluation

```
Create a comprehensive SKILL.md for RAG (Retrieval-Augmented Generation) Evaluation.

Location: 52-ai-evaluation/rag-evaluation/SKILL.md

Cover:
1. What is RAG evaluation:
   - Measuring quality of retrieval + generation
   - Both components need evaluation
   - End-to-end and per-component
2. Why RAG evaluation matters:
   - RAG quality varies widely
   - Retrieval errors → wrong context → bad answers
   - Need metrics to improve systematically
3. RAG components to evaluate:
   - Retrieval: Are relevant docs retrieved?
   - Context: Is context sufficient for answer?
   - Generation: Is answer correct, relevant, safe?
4. Retrieval evaluation metrics:
   - Precision@k: % of top-k results relevant
   - Recall@k: % of relevant docs in top-k
   - MRR (Mean Reciprocal Rank): Position of first relevant doc
   - NDCG (Normalized Discounted Cumulative Gain)
   - Context relevance score
5. Generation evaluation metrics:
   - Faithfulness: Answer grounded in context (no hallucination)
   - Answer relevance: Answer addresses the question
   - Correctness: Answer is factually correct
   - Completeness: Answer covers all aspects
6. Faithfulness evaluation:
   - Method 1: LLM-as-judge (does answer match context?)
   - Method 2: NLI model (entailment check)
   - Method 3: Citation checking (are claims cited?)
7. Answer relevance evaluation:
   - LLM-as-judge: "Does answer address question?"
   - Semantic similarity (answer vs expected answer)
   - User feedback (thumbs up/down)
8. Correctness evaluation:
   - Ground truth comparison (if available)
   - LLM-as-judge with rubric
   - Human evaluation (gold standard)
9. RAG-specific metrics:
   - Context precision: Relevant chunks in context
   - Context recall: All needed info retrieved
   - Context relevance: Context relevance to question
   - Answer faithfulness: No hallucinations
   - Answer relevance: On-topic answer
10. Creating evaluation dataset:
    - Question-answer pairs (ground truth)
    - Question-context-answer triples
    - Diverse questions (simple, complex, multi-hop)
    - Edge cases (ambiguous, no answer)
11. Evaluation frameworks:
    - RAGAS (popular framework)
    - TruLens
    - DeepEval
    - Langfuse
    - Custom evaluation scripts
12. RAGAS metrics:
    - Context Precision
    - Context Recall
    - Faithfulness
    - Answer Relevance
    - Answer Semantic Similarity
    - Answer Correctness
13. LLM-as-judge patterns:
    - Use GPT-4 or Claude to grade answers
    - Provide rubric (1-5 scale)
    - Check faithfulness, relevance, quality
    - Aggregate scores
14. Human evaluation:
    - Gold standard but expensive
    - Use for spot checks
    - Validate LLM-judge correlation
    - Annotation guidelines
15. A/B testing RAG systems:
    - Variant A vs Variant B
    - Same questions, different systems
    - Measure metrics for both
    - Statistical significance
16. Retrieval optimization:
    - Tune chunk size
    - Tune number of chunks (top-k)
    - Improve embeddings (fine-tuning)
    - Hybrid search (keyword + semantic)
    - Re-ranking
17. Generation optimization:
    - Prompt engineering
    - Model selection (GPT-4 vs Claude)
    - Temperature tuning
    - System prompts
18. Continuous evaluation:
    - Log all queries + answers
    - Sample for evaluation
    - Track metrics over time
    - Regression detection
19. Real-world RAG evaluation:
    - Customer support chatbot
    - Technical documentation Q&A
    - Legal document search
20. Implementation:
    - RAGAS evaluation script
    - Custom metrics
    - LLM-as-judge prompts

Format: Include evaluation metrics code, RAGAS examples, and judge prompts.

Create the file now.
```

### Skill 2: LLM Judge Patterns

```
Create a comprehensive SKILL.md for LLM-as-Judge patterns in AI evaluation.

Location: 52-ai-evaluation/llm-judge-patterns/SKILL.md

Cover:
1. What is LLM-as-judge:
   - Using LLMs (GPT-4, Claude) to evaluate other LLM outputs
   - Automated evaluation at scale
   - Alternative to human evaluation
2. Why LLM-as-judge:
   - Human eval is slow and expensive
   - Need to evaluate thousands of outputs
   - Research shows high correlation with human judgment
   - Enables continuous evaluation
3. When to use LLM-as-judge:
   - Subjective quality (fluency, relevance, helpfulness)
   - Complex rubrics (multi-criteria)
   - Large-scale evaluation
   - Rapid iteration
4. When NOT to use LLM-as-judge:
   - Objective correctness (factual answers)
   - Mathematical reasoning (verify with computation)
   - Code correctness (run tests)
   - Safety-critical (use human evaluation)
5. Judge model selection:
   - GPT-4 (most commonly used)
   - Claude Sonnet 4 (excellent reasoning)
   - GPT-3.5 (cheaper, less accurate)
   - Open-source (Llama, Mixtral)
6. Judge prompt patterns:
   - Single-answer grading
   - Pairwise comparison (A vs B)
   - Multi-aspect evaluation (rubric)
   - Chain-of-thought reasoning
7. Single-answer grading:
   - Prompt: "Rate this answer on scale 1-5"
   - Include: Question, answer, rubric
   - Output: Score + reasoning
8. Pairwise comparison:
   - Prompt: "Which answer is better? A or B?"
   - More reliable than absolute scoring
   - Reduces judge bias
   - Aggregate via Elo ratings
9. Multi-aspect evaluation:
   - Evaluate multiple criteria (relevance, accuracy, style)
   - Score each criterion separately
   - Weighted aggregate
10. Chain-of-thought judging:
    - Ask judge to explain reasoning
    - Then provide score
    - Increases reliability
    - Catches judge mistakes
11. Judge prompt template:
    ```
    You are evaluating an AI assistant's response.
    
    Question: [question]
    Answer: [answer]
    
    Evaluate on these criteria:
    1. Relevance (1-5): Does it answer the question?
    2. Accuracy (1-5): Is information correct?
    3. Completeness (1-5): Covers all aspects?
    
    Provide:
    - Score for each criterion
    - Brief reasoning
    - Overall score (average)
    ```
12. Judge calibration:
    - Compare judge scores to human scores
    - Calculate correlation
    - Adjust prompt if low correlation
    - Test on multiple examples
13. Reducing judge bias:
    - Position bias (favors first option in A/B)
    - Length bias (favors longer answers)
    - Self-preference bias (favors own outputs)
    - Mitigation: Randomize order, normalize by length, use external judge
14. Multi-judge ensemble:
    - Use multiple judges (GPT-4 + Claude)
    - Aggregate scores (majority vote, average)
    - Increases reliability
15. Cost optimization:
    - Use cheaper judge for initial filtering
    - Use expensive judge for borderline cases
    - Cache judge results
16. Judge evaluation frameworks:
    - G-Eval (using GPT-4)
    - Prometheus (using Llama)
    - Custom implementation
17. Metrics to track:
    - Judge-human correlation
    - Inter-judge agreement (if multiple judges)
    - Judge consistency (same input → same output)
18. Real-world judge use cases:
    - RAG answer evaluation
    - Chatbot response quality
    - Content moderation
    - Translation quality
    - Summarization quality
19. Limitations:
    - Judge can be wrong (validate with humans)
    - Expensive (API costs)
    - Judge bias (needs careful prompting)
    - Not suitable for all tasks
20. Implementation:
    - Judge prompt templates
    - Multi-judge aggregation
    - Calibration scripts

Format: Include judge prompt templates, evaluation code, and comparison examples.

Create the file now.
```

### Skill 3: Ground Truth Management

```
Create a comprehensive SKILL.md for Ground Truth Management in AI evaluation.

Location: 52-ai-evaluation/ground-truth-management/SKILL.md

Cover:
1. What is ground truth:
   - Correct answers for evaluation
   - Human-verified data
   - Gold standard for measuring AI performance
2. Why ground truth matters:
   - Measure accuracy objectively
   - Train and validate models
   - Regression testing
   - Benchmarking
3. Types of ground truth:
   - Exact match: Single correct answer
   - Multiple acceptable answers
   - Rubric-based: Quality scale
   - Human preference: Comparison rankings
4. Creating ground truth:
   - Manual annotation (humans label)
   - Expert review (for specialized domains)
   - Crowdsourcing (Amazon MTurk)
   - Synthetic generation (for some tasks)
5. Ground truth dataset structure:
   - Input (question, document, image)
   - Expected output (answer, label, summary)
   - Metadata (difficulty, category, source)
   - Annotation info (who, when, confidence)
6. Annotation guidelines:
   - Clear instructions
   - Examples (good and bad)
   - Edge case handling
   - Consistency checks
7. Quality control:
   - Multiple annotators per example
   - Inter-annotator agreement (IAA)
   - Gold standard subset (known answers)
   - Spot checks by experts
8. Inter-annotator agreement:
   - Kappa score (Cohen's κ)
   - Fleiss' κ (multiple annotators)
   - Percentage agreement
   - Target: >0.7 (good agreement)
9. Resolving disagreements:
   - Majority vote
   - Expert adjudication
   - Discussion and consensus
   - Update guidelines
10. Ground truth for different tasks:
    - Classification: Category labels
    - Q&A: Correct answers + acceptable variants
    - Summarization: Reference summaries
    - RAG: Question + context + answer
    - Generation: Multiple acceptable outputs
11. Dataset size:
    - Evaluation set: 100-1000 examples (representative)
    - Test set: 500-5000 examples (comprehensive)
    - Quality > quantity
    - Cover edge cases
12. Dataset maintenance:
    - Version control (like code)
    - Regular updates (new examples)
    - Remove outdated examples
    - Track changes (changelog)
13. Stratified sampling:
    - Balance by difficulty
    - Balance by category
    - Include edge cases
    - Representative of production
14. Synthetic ground truth:
    - LLM-generated questions + answers
    - Careful validation needed
    - Good for scale, risky for quality
    - Use for augmentation, not sole source
15. Domain-specific ground truth:
    - Medical: Expert annotations
    - Legal: Lawyer review
    - Technical: Engineer verification
16. Ground truth storage:
    - JSON/JSONL files
    - Database (PostgreSQL, MongoDB)
    - Version control (Git)
    - Cloud storage (S3 + versioning)
17. Ground truth for RAG:
    - Question
    - Expected answer
    - Relevant document chunks (optional)
    - Evaluation criteria
18. Evaluation with ground truth:
    - Exact match accuracy
    - F1 score (for overlapping spans)
    - BLEU/ROUGE (for generation)
    - Semantic similarity (embedding distance)
19. Continuous ground truth:
    - Production feedback (user thumbs up/down)
    - Human review of flagged outputs
    - Incrementally add to dataset
20. Tools:
    - Annotation: Label Studio, Prodigy, CVAT
    - Management: DVC (Data Version Control)
    - Storage: S3, GCS, local files

Format: Include dataset schemas, annotation guidelines, and quality control processes.

Create the file now.
```

### Skill 4: Offline vs Online Evaluation

```
Create a comprehensive SKILL.md for Offline vs Online Evaluation strategies.

Location: 52-ai-evaluation/offline-vs-online-eval/SKILL.md

Cover:
1. Definitions:
   - Offline evaluation: Test on static dataset before deployment
   - Online evaluation: Measure in production with real users
2. Why both matter:
   - Offline: Fast iteration, controlled testing
   - Online: Real-world performance, actual user impact
   - Need both for complete picture
3. Offline evaluation:
   - When: During development, before deployment
   - Dataset: Ground truth test set
   - Metrics: Accuracy, F1, BLEU, RAG metrics
   - Pros: Fast, reproducible, safe
   - Cons: May not reflect real performance
4. Online evaluation:
   - When: In production with real users
   - Dataset: Live traffic
   - Metrics: User satisfaction, task success, engagement
   - Pros: Real performance, actual impact
   - Cons: Slower, risky, requires traffic
5. Offline evaluation process:
   - Create evaluation dataset
   - Run model on dataset
   - Compute metrics
   - Compare to baseline
   - Iterate until good enough
6. Online evaluation methods:
   - A/B testing (two variants)
   - Shadow mode (log but don't serve)
   - Canary deployment (small % of traffic)
   - Interleaving (mix results)
7. A/B testing:
   - Control (current model) vs Treatment (new model)
   - Random assignment of users
   - Measure metrics for both
   - Statistical significance test
   - Ship winner
8. Shadow mode:
   - New model runs in background
   - Logs predictions but doesn't serve
   - Compare to actual responses
   - No user impact
   - Great for risk mitigation
9. Canary deployment:
   - Deploy to small % (1-5%) of users
   - Monitor closely
   - Gradually increase %
   - Rollback if issues
10. Online metrics:
    - Engagement: Click-through rate, time on page
    - Satisfaction: Thumbs up/down, ratings
    - Task success: Did user achieve goal?
    - Efficiency: Time to complete, steps needed
    - Safety: Violations, flags, escalations
11. Implicit signals:
    - Did user click result? (relevance)
    - Did user reformulate query? (dissatisfaction)
    - Did user abandon? (failure)
    - Session length (engagement)
12. Explicit feedback:
    - Thumbs up/down
    - Star ratings (1-5)
    - Written feedback
    - Bug reports
13. Bridging offline and online:
    - Offline metrics should correlate with online
    - Validate offline improvements lead to online gains
    - Offline for filtering, online for final decision
14. When offline and online disagree:
    - Offline: Model A is better
    - Online: Model B performs better
    - Possible reasons:
      * Dataset not representative
      * Metric doesn't capture what matters
      * User behavior differs from test set
    - Trust online (but investigate why)
15. Continuous evaluation:
    - Log all predictions + outcomes
    - Offline eval on recent data
    - Online eval via A/B tests
    - Monitor metrics dashboard
16. Guardrails for online eval:
    - Automated rollback (if metrics drop)
    - Manual review (before wide rollout)
    - Sampling (don't test on all traffic)
    - Reversibility (easy to revert)
17. Offline-to-online workflow:
    - Develop: Offline eval on test set
    - Validate: Shadow mode (offline on live traffic)
    - Test: Canary to 1% (online, minimal risk)
    - Expand: Gradual rollout to 100%
    - Monitor: Continuous online evaluation
18. Real-world examples:
    - Search ranking (offline: NDCG, online: CTR)
    - Recommendation (offline: accuracy, online: engagement)
    - RAG (offline: faithfulness, online: thumbs up)
19. Tools:
    - Offline: Custom scripts, evaluation frameworks
    - Online: Experimentation platforms (Optimizely, LaunchDarkly)
    - Both: MLOps platforms (MLflow, Weights & Biases)

Format: Include evaluation workflow diagrams, A/B testing examples, and metrics tracking code.

Create the file now.
```

### Skill 5: Regression Benchmarks

```
Create a comprehensive SKILL.md for Regression Benchmarks in AI systems.

Location: 52-ai-evaluation/regression-benchmarks/SKILL.md

Cover:
1. What are regression benchmarks:
   - Test suite to detect performance degradation
   - Runs on every change (like unit tests)
   - Catches regressions before deployment
2. Why regression benchmarks matter:
   - New features can break existing functionality
   - Model updates can reduce quality
   - Prompt changes can have unintended effects
   - Catch issues early (before production)
3. Components of regression suite:
   - Test cases (inputs + expected outputs)
   - Evaluation metrics (how to score)
   - Acceptance thresholds (what's acceptable)
   - Automated execution (CI/CD)
4. Creating regression test cases:
   - Representative examples (common queries)
   - Edge cases (where model struggles)
   - Historical failures (bugs that happened before)
   - Diverse coverage (different categories)
5. Test case structure:
   - Input (question, prompt, image)
   - Expected behavior (correct answer or quality criteria)
   - Context (if needed for evaluation)
   - Metadata (category, difficulty, priority)
6. Evaluation strategies:
   - Exact match (for deterministic outputs)
   - Semantic similarity (for generated text)
   - LLM-as-judge (for quality)
   - Human spot checks (sample validation)
7. Acceptance criteria:
   - Absolute threshold (e.g., accuracy >90%)
   - Relative threshold (e.g., no worse than -2% vs baseline)
   - Per-category thresholds (important categories stricter)
8. Regression test types:
   - Accuracy tests (correct answers)
   - Quality tests (output quality)
   - Latency tests (response time)
   - Safety tests (no harmful outputs)
   - Consistency tests (same input → same output)
9. Running regression suite:
   - Trigger: Every code change, prompt change, model update
   - Execution: Automated (CI/CD pipeline)
   - Duration: Fast enough for CI (minutes, not hours)
   - Reporting: Clear pass/fail + details
10. Handling failures:
    - Investigate root cause
    - Intended change (update benchmark)
    - Unintended regression (fix the issue)
    - Flaky test (improve test stability)
11. Golden set:
    - Curated subset of most important tests
    - High-quality ground truth
    - Regularly updated
    - Always passing (except when intentional)
12. Versioning benchmarks:
    - Benchmark version tied to model version
    - Update benchmarks when requirements change
    - Maintain history (track improvements over time)
13. Benchmark coverage:
    - Functional coverage (all features tested)
    - Edge case coverage (error conditions, boundaries)
    - Performance coverage (speed, cost)
14. Continuous benchmarking:
    - Run on every PR (fast subset)
    - Run nightly (full suite)
    - Run on model updates (comprehensive)
15. Benchmark metrics to track:
    - Pass rate (% of tests passing)
    - Performance vs baseline (% change)
    - Latency (P50, P95, P99)
    - Cost per test (LLM API calls)
16. Optimization:
    - Cache model responses (if deterministic)
    - Parallelize test execution
    - Sample large test suites (for fast feedback)
17. Integration with CI/CD:
    - GitHub Actions workflow
    - Required check (block merge if failing)
    - Clear error messages (which tests failed)
    - Link to details (full report)
18. Real-world regression examples:
    - RAG system (faithfulness, relevance)
    - Chatbot (quality, safety)
    - Code generation (correctness, style)
19. Tools:
    - pytest (test framework)
    - Custom evaluation scripts
    - CI/CD platforms (GitHub Actions, GitLab CI)
20. Implementation:
    - Test suite structure
    - CI/CD configuration
    - Reporting dashboard

Format: Include test case examples, CI/CD configs, and benchmark reporting templates.

Create the file now.
```

---

## Batch 56: Requirements Intake

### Skill 1: Discovery Questions

```
Create a comprehensive SKILL.md for Discovery Questions in requirements gathering.

Location: 56-requirements-intake/discovery-questions/SKILL.md

Cover:
1. What are discovery questions:
   - Structured questions to understand requirements
   - Uncover hidden needs and constraints
   - Clarify vague requirements
   - Identify risks and dependencies
2. Why discovery matters:
   - Avoid building the wrong thing
   - Understand true needs (not stated wants)
   - Surface constraints early
   - Set clear expectations
3. Discovery question categories:
   - Problem space (what problem are we solving?)
   - Users (who will use this?)
   - Success criteria (how do we know it works?)
   - Constraints (what limits us?)
   - Context (what else should we know?)
4. Problem space questions:
   - What problem are you trying to solve?
   - Why is this a problem? (5 Whys)
   - Who experiences this problem?
   - How often does it occur?
   - What is the impact of not solving it?
   - What have you tried already?
   - Why didn't previous solutions work?
5. User questions:
   - Who are the primary users?
   - Who are secondary users?
   - What is their technical skill level?
   - How many users (current and expected)?
   - Where are they located (regions, timezones)?
   - What devices/browsers do they use?
6. Success criteria questions:
   - How will we know this is successful?
   - What metrics will we track?
   - What is the desired outcome?
   - What would make this a failure?
   - When do you need this by? (hard deadline or flexible?)
7. Constraint questions:
   - What is the budget?
   - What is the timeline?
   - Who is available to work on this?
   - Are there technical constraints (existing systems, tech stack)?
   - Are there legal/compliance requirements?
   - Are there performance requirements?
8. Context questions:
   - What is the broader business goal?
   - How does this fit into the roadmap?
   - Who are the stakeholders?
   - Are there dependencies on other projects?
   - What is the competitive landscape?
9. Technical discovery questions:
   - What systems need to integrate?
   - What data needs to be accessed?
   - What is the expected traffic/load?
   - What are the availability requirements?
   - What are the security requirements?
   - What is the data retention policy?
10. Risk discovery questions:
    - What could go wrong?
    - What keeps you up at night about this project?
    - What is the biggest uncertainty?
    - What external dependencies exist?
11. Question techniques:
    - Open-ended (tell me about...)
    - Probing (why? can you elaborate?)
    - Hypothetical (what if...?)
    - Reflective (so what you're saying is...)
12. Avoiding bad questions:
    - Leading questions (don't you think...?)
    - Multiple questions at once
    - Yes/no when you need details
    - Jargon or technical terms (when talking to non-technical stakeholders)
13. Active listening:
    - Paraphrase back (confirm understanding)
    - Note what's not said
    - Ask follow-ups
    - Silence is okay (let them think)
14. Documenting discovery:
    - Take notes during conversation
    - Summarize key points
    - Identify ambiguities (need clarification)
    - Action items (follow-up needed)
15. Discovery meeting structure:
    - Intro (5 min): Set context, agenda
    - Problem space (15 min): Understand the problem
    - Solution space (15 min): Explore options
    - Constraints (10 min): Understand limits
    - Next steps (5 min): Clarify follow-ups
16. Domain-specific question templates:
    - New feature discovery
    - Bug fix discovery
    - Performance improvement
    - Integration project
    - Compliance project
17. Red flags in discovery:
    - Vague requirements ("make it better")
    - Solution masquerading as problem ("we need a chatbot")
    - Unrealistic timelines
    - Unclear success criteria
    - Too many stakeholders with conflicting needs
18. Post-discovery:
    - Write discovery summary
    - Share with stakeholders (confirm understanding)
    - Identify open questions
    - Create requirements document
19. Real discovery scenarios:
    - E-commerce feature request
    - Internal tool improvement
    - API integration project
20. Templates:
    - Discovery question checklist
    - Discovery meeting notes
    - Discovery summary document

Format: Include question templates for different project types and discovery documentation templates.

Create the file now.
```

### Skill 2: Requirement to Scope

```
Create a comprehensive SKILL.md for converting Requirements to Scope (In-scope vs Out-of-scope).

Location: 56-requirements-intake/requirement-to-scope/SKILL.md

Cover:
1. What is scoping:
   - Defining what will be delivered (in-scope)
   - Explicitly stating what won't be delivered (out-of-scope)
   - Setting clear boundaries
2. Why scoping matters:
   - Prevent scope creep
   - Set expectations
   - Estimate effort accurately
   - Avoid misunderstandings
3. Scope definition components:
   - In-scope (what we will do)
   - Out-of-scope (what we won't do)
   - Assumptions (what we assume is true)
   - Dependencies (what we rely on)
4. From requirements to scope:
   - Gather all requirements
   - Prioritize (MoSCoW: Must, Should, Could, Won't)
   - Define MVP (minimum viable scope)
   - Defer nice-to-haves (future phases)
5. Prioritization frameworks:
   - MoSCoW: Must have, Should have, Could have, Won't have
   - RICE: Reach, Impact, Confidence, Effort
   - Value vs Effort (2x2 matrix)
   - Kano model (basic, performance, delighters)
6. In-scope examples:
   - "User can sign up with email and password"
   - "Admin can view user list with pagination"
   - "System sends email notifications for orders"
7. Out-of-scope examples:
   - "Social login (deferred to Phase 2)"
   - "Mobile app (web only for now)"
   - "Multi-language support (English only in MVP)"
8. Why out-of-scope matters:
   - Prevents "I thought you were doing X"
   - Manages expectations
   - Documents what was considered but deferred
9. Assumptions:
   - "Assume we have access to existing user database"
   - "Assume third-party API will be available"
   - "Assume users have modern browsers (Chrome, Firefox, Safari)"
10. Dependencies:
   - Internal: "Depends on authentication service being ready"
   - External: "Depends on Stripe API for payments"
   - Data: "Depends on product data being available"
11. Scope document structure:
    - Project overview
    - Goals and objectives
    - In-scope (features, functionality)
    - Out-of-scope (explicit exclusions)
    - Assumptions
    - Dependencies
    - Constraints (budget, timeline, resources)
    - Success criteria
12. Handling scope creep:
    - Document all new requests
    - Assess impact (time, cost)
    - Re-prioritize (what gets deferred?)
    - Get approval for changes
    - Update scope document
13. Communicating scope:
    - Written scope document (shared doc)
    - Kickoff meeting (present scope)
    - Regular check-ins (confirm still aligned)
    - Visual scope (user story map, feature matrix)
14. User story mapping:
    - Visualize scope as user journey
    - Horizontal: User flow (left to right)
    - Vertical: Priority (top = must-have)
    - Easy to see MVP (top row)
15. Scope negotiation:
    - Stakeholder wants everything
    - You explain constraints (time/budget/quality triangle)
    - Prioritize together (what matters most?)
    - Defer lower-priority items
16. MVP scoping:
    - Core value proposition (must-have)
    - Remove nice-to-haves (add later)
    - Simplify (basic version first)
    - Example: E-commerce MVP = browse + checkout (no wishlists, reviews, recommendations)
17. Phased delivery:
    - Phase 1 (MVP): Core functionality
    - Phase 2: Enhanced features
    - Phase 3: Advanced features
    - Clearly document what's in each phase
18. Red flags in scoping:
    - "Everything is must-have" (need prioritization)
    - "We'll figure it out later" (define now)
    - Scope keeps changing (need change control)
19. Scope approval:
    - Stakeholders sign off
    - Document approval (email, signature)
    - Baseline for change control
20. Real scoping examples:
    - E-commerce project scope
    - Internal dashboard scope
    - API integration scope

Format: Include scope document templates, prioritization matrices, and user story mapping examples.

Create the file now.
```

### Skill 3: Acceptance Criteria

```
Create a comprehensive SKILL.md for defining Acceptance Criteria.

Location: 56-requirements-intake/acceptance-criteria/SKILL.md

Cover:
1. What are acceptance criteria:
   - Specific conditions that must be met for work to be considered complete
   - Testable and measurable
   - Shared understanding of "done"
2. Why acceptance criteria matter:
   - Prevent misunderstandings
   - Enable testing
   - Clarify requirements
   - Enable sign-off
3. Good acceptance criteria characteristics:
   - Specific (not vague)
   - Measurable (can verify)
   - Achievable (realistic)
   - Relevant (to the requirement)
   - Testable (can be validated)
4. Format options:
   - Given-When-Then (BDD style)
   - Checklist format
   - Scenario format
   - Rule-based format
5. Given-When-Then format:
   - Given [context/precondition]
   - When [action/event]
   - Then [expected outcome]
   - Example: Given user is logged in, When user clicks "Add to Cart", Then product is added to cart and cart count increases by 1
6. Checklist format:
   - [ ] User can sign up with email and password
   - [ ] System validates email format
   - [ ] System sends verification email
   - [ ] Error message shown for invalid inputs
7. Scenario format:
   - Scenario: User signs up successfully
   - User enters valid email and password
   - User clicks "Sign Up"
   - Account is created
   - Confirmation email is sent
   - User is redirected to dashboard
8. Writing good acceptance criteria:
   - Focus on "what" not "how"
   - Include happy path and error cases
   - Be specific about data formats
   - Define validation rules
   - Specify user feedback (messages, notifications)
9. Common mistakes:
   - Too vague ("works well", "looks good")
   - Implementation details ("uses React hooks")
   - No error cases
   - Not measurable ("fast", "intuitive")
10. Acceptance criteria for different work types:
    - Features: User actions, system responses, validation
    - Bug fixes: Reproduction steps no longer fail
    - Performance: Specific metrics (P95 latency <200ms)
    - Refactoring: No behavior change, tests still pass
11. Definition of Done (DoD):
    - Acceptance criteria met
    - Code reviewed
    - Tests written and passing
    - Documentation updated
    - Deployed to staging
    - Stakeholder approval
12. Verification methods:
    - Manual testing (QA follows criteria)
    - Automated tests (e2e tests for each criterion)
    - Demo to stakeholder (show it works)
13. Handling ambiguity:
    - If unclear, write multiple scenarios
    - Add "Questions" section
    - Get stakeholder clarification
    - Update criteria with answers
14. Example acceptance criteria:
    - User registration feature
    - Payment processing
    - Search functionality
    - Admin dashboard
15. Acceptance criteria in user stories:
    - User story: "As a user, I want to reset my password so I can regain access"
    - Acceptance criteria:
      * User can click "Forgot Password" link
      * User enters email address
      * System sends reset link to email
      * Link expires after 24 hours
      * User can set new password via link
      * Error shown if email not found
16. Sign-off process:
    - Developer marks as ready
    - QA verifies against criteria
    - Product owner reviews
    - All criteria met → approved
17. Traceability:
    - Link criteria to tests
    - Link criteria to requirements
    - Track which criteria passed/failed
18. Real-world examples:
    - E-commerce checkout
    - User authentication
    - Data export feature

Format: Include acceptance criteria templates, examples for different feature types, and verification checklists.

Create the file now.
```

### Skill 4: Constraints and Assumptions

```
Create a comprehensive SKILL.md for documenting Constraints and Assumptions.

Location: 56-requirements-intake/constraints-and-assumptions/SKILL.md

Cover:
1. Definitions:
   - Constraints: Fixed limitations (must work within)
   - Assumptions: Things we believe to be true (need validation)
2. Why documenting them matters:
   - Surface hidden risks
   - Clarify expectations
   - Guide decisions
   - Identify validation needs
3. Types of constraints:
   - Budget constraints ($ limit)
   - Time constraints (deadline)
   - Resource constraints (team size, skills)
   - Technical constraints (existing tech stack, systems)
   - Legal/compliance constraints (GDPR, HIPAA)
   - Business constraints (brand guidelines, policies)
4. Budget constraints:
   - Total budget available
   - Infrastructure costs (cloud, SaaS)
   - Development costs (team time)
   - Third-party costs (APIs, services)
5. Time constraints:
   - Hard deadline (event, contract)
   - Soft deadline (preferred but flexible)
   - Milestones (phased delivery)
   - Dependency deadlines (other projects)
6. Resource constraints:
   - Team size and composition
   - Skills available (need training?)
   - Tools and infrastructure
   - Third-party dependencies
7. Technical constraints:
   - Existing tech stack (must use)
   - Integration requirements (must connect to)
   - Performance requirements (must achieve)
   - Scalability requirements (must support X users)
   - Browser/device support (must work on)
8. Legal/compliance constraints:
   - Data privacy (GDPR, CCPA, PDPA)
   - Industry regulations (HIPAA, SOX, PCI-DSS)
   - Accessibility (WCAG 2.1)
   - Security standards (SOC2, ISO 27001)
9. Business constraints:
   - Brand guidelines (colors, fonts, tone)
   - Approval processes (who signs off)
   - Communication channels (how to update stakeholders)
   - Existing commitments (contracts, agreements)
10. Types of assumptions:
    - Technical assumptions (API will be available)
    - User assumptions (users have modern browsers)
    - Data assumptions (data is accurate and complete)
    - Availability assumptions (team members available)
    - Third-party assumptions (vendor delivers on time)
11. Documenting assumptions:
    - Clearly state assumption
    - Note impact if assumption is wrong
    - Identify how to validate
    - Assign owner to validate
12. Example assumptions:
    - "Assume users have internet connection" (impact: offline mode not needed)
    - "Assume Stripe API uptime >99.9%" (impact: payment processing reliability)
    - "Assume design team provides assets by Week 2" (impact: development timeline)
13. Validating assumptions:
    - Early in project (before committing)
    - Methods: Testing, prototyping, research, asking experts
    - Document results (validated or invalidated)
14. Risk of invalid assumptions:
    - If assumption is wrong → project at risk
    - Example: Assumed API would support feature X, but it doesn't → need different approach
15. Constraints and assumptions document:
    - Section in project charter or requirements doc
    - Table format (easy to scan)
    - Reviewed and updated regularly
16. Template structure:
    ```
    Constraints:
    - Budget: $50,000
    - Timeline: 3 months (hard deadline: June 30)
    - Team: 2 developers, 1 designer (no QA dedicated)
    - Tech stack: Must use existing React + Node.js
    - Compliance: Must comply with GDPR
    
    Assumptions:
    - Users have modern browsers (Chrome, Firefox, Safari)
    - Third-party API will be available and reliable
    - Design team will provide assets by Week 2
    - No major scope changes during development
    ```
17. Change management:
    - If constraint changes (more budget, more time) → update plan
    - If assumption invalidated → assess impact, replan
18. Communication:
    - Share constraints with team (so they understand limits)
    - Flag risky assumptions to stakeholders
    - Regular reviews (are assumptions still valid?)
19. Real-world examples:
    - E-commerce project constraints and assumptions
    - Mobile app development
    - API integration project

Format: Include constraints and assumptions templates, validation checklists, and impact analysis frameworks.

Create the file now.
```

### Skill 5: Risk and Dependencies

```
Create a comprehensive SKILL.md for identifying Risk and Dependencies in requirements.

Location: 56-requirements-intake/risk-and-dependencies/SKILL.md

Cover:
1. Definitions:
   - Risk: Potential problem that may occur
   - Dependency: Reliance on external factor
2. Why identify early:
   - Plan mitigation strategies
   - Avoid surprises
   - Set realistic timelines
   - Communicate to stakeholders
3. Types of risks:
   - Technical risk (can we build it?)
   - Schedule risk (will we finish on time?)
   - Resource risk (do we have the people/skills?)
   - Integration risk (will systems connect?)
   - Third-party risk (will vendor deliver?)
   - Compliance risk (will we meet regulations?)
4. Risk identification techniques:
   - Brainstorming (team discussion)
   - Pre-mortem ("what could go wrong?")
   - Checklist (common risks)
   - Past projects (what went wrong before?)
5. Risk assessment:
   - Probability: Low, Medium, High (or %)
   - Impact: Low, Medium, High (or $)
   - Risk level: Probability × Impact
   - Focus on high probability + high impact
6. Risk matrix:
   ```
             Low Impact | Medium Impact | High Impact
   Low Prob:    Green   |    Green     |   Yellow
   Med Prob:    Green   |    Yellow    |   Red
   High Prob:   Yellow  |    Red       |   Red
   ```
7. Risk register:
   - Table of all identified risks
   - Columns: Risk, Probability, Impact, Mitigation, Owner
   - Reviewed regularly
8. Common technical risks:
   - New technology (unfamiliar to team)
   - Complex integration (many systems)
   - Performance at scale (can it handle load?)
   - Data migration (old system to new)
   - Third-party API limitations
9. Mitigation strategies:
   - Avoid: Change plan to eliminate risk
   - Reduce: Take actions to lower probability/impact
   - Transfer: Use vendor, insurance
   - Accept: Acknowledge and monitor
10. Example risk mitigations:
    - Risk: "New framework, team unfamiliar"
    - Mitigation: "Allocate 2 weeks for training, build prototype"
    - Risk: "Third-party API may change"
    - Mitigation: "Abstract API behind our own interface"
11. Types of dependencies:
    - Internal: Other teams, internal systems
    - External: Vendors, partners, clients
    - Technical: Libraries, frameworks, platforms
    - Data: Existing databases, data sources
12. Dependency mapping:
    - List all dependencies
    - Identify critical path (longest chain)
    - Note dependency owners
    - Track dependency status
13. Dependency risks:
    - Dependency delayed → our project delayed
    - Dependency changes → need to adapt
    - Dependency fails → need backup plan
14. Managing dependencies:
    - Clear agreements (what, when, who)
    - Regular check-ins (is it on track?)
    - Contingency plans (what if delayed?)
    - Reduce dependencies (decouple where possible)
15. Red flags:
    - Many high-probability, high-impact risks
    - Critical dependencies on unreliable sources
    - Tight coupling to external factors
16. Communicating risks:
    - To stakeholders: High-level (top 3-5 risks)
    - To team: Detailed (all risks, mitigations)
    - Regular updates (risk status changes)
17. Risk and dependency document structure:
    ```
    Risks:
    1. Technical risk: Unfamiliar with GraphQL
       - Probability: Medium
       - Impact: High (could delay project)
       - Mitigation: 1 week training + prototype
       - Owner: Tech Lead
    
    Dependencies:
    1. Design team to provide mockups by Week 2
       - Critical: Yes (blocks development)
       - Status: On track
       - Contingency: Use wireframes if delayed
    ```
18. Real-world examples:
    - Integration project risks and dependencies
    - New product development
    - System migration

Format: Include risk register templates, dependency tracking sheets, and mitigation strategy examples.

Create the file now.
```

---

## Batch 57: Skill Orchestration

### Skill 1: Baseline Policy

```
Create a comprehensive SKILL.md for Baseline Policy (default skills that should always be considered).

Location: 57-skill-orchestration/baseline-policy/SKILL.md

Cover:
1. What is baseline policy:
   - Default set of skills to consider for every task
   - Foundation knowledge that's always relevant
   - Prevents forgetting critical aspects
2. Why baseline policy matters:
   - Consistency across projects
   - Don't forget fundamentals
   - Reduce cognitive load (don't reinvent process)
   - Quality baseline
3. Universal baseline skills (always relevant):
   - System thinking (holistic view)
   - Trade-off analysis (evaluate options)
   - Risk assessment (what could go wrong)
   - Security considerations (protect data, users)
   - Error handling (graceful failures)
4. Project kickoff baseline:
   - Requirements intake (discovery questions)
   - Constraint identification
   - Risk and dependencies
   - Acceptance criteria
   - Scope definition
5. Development baseline:
   - Code quality (linting, testing)
   - Git workflow (branching, PRs)
   - Documentation (README, comments)
   - Error handling (try-catch, logging)
   - Security (input validation, auth)
6. API development baseline:
   - API design standards (REST conventions)
   - OpenAPI documentation
   - Versioning strategy
   - Error responses (consistent format)
   - Rate limiting
7. Data handling baseline:
   - Data validation (input sanitization)
   - PII detection (privacy)
   - Logging redaction (no secrets in logs)
   - Backup strategy
   - Data retention policy
8. Deployment baseline:
   - CI/CD pipeline (automated)
   - Environment variables (no hardcoded secrets)
   - Health checks (monitoring)
   - Rollback plan (if deployment fails)
   - Deployment checklist
9. AI/ML project baseline:
   - Evaluation framework (metrics defined)
   - Ground truth dataset (for testing)
   - Safety guardrails (harmful content filtering)
   - Monitoring (model performance)
   - Cost tracking (LLM usage)
10. Frontend baseline:
    - Accessibility (WCAG compliance)
    - Responsive design (mobile-friendly)
    - Performance (load time)
    - Browser compatibility
    - Error states (loading, empty, error)
11. Security baseline:
    - Authentication (who are you)
    - Authorization (what can you do)
    - Input validation (prevent injection)
    - Output encoding (prevent XSS)
    - HTTPS only
12. Compliance baseline (if applicable):
    - GDPR (data privacy)
    - SOC2 (security controls)
    - Accessibility (WCAG)
    - Industry-specific (HIPAA, PCI-DSS)
13. Domain-specific baselines:
    - E-commerce: Payment security, cart handling
    - Healthcare: HIPAA compliance, PHI protection
    - Finance: PCI-DSS, transaction auditing
14. Customizing baseline:
    - Start with universal baseline
    - Add domain-specific skills
    - Add organization-specific standards
    - Document and share
15. Baseline enforcement:
    - Checklist (manual review)
    - Automated checks (linters, CI tests)
    - Code review (reviewer checklist)
    - Project templates (pre-configured)
16. Baseline evolution:
    - Review quarterly
    - Add learnings from incidents
    - Remove outdated items
    - Get team input
17. Baseline documentation:
    - Written baseline policy document
    - Checklist format (easy to follow)
    - Examples (for clarity)
    - Linked to skills (for details)
18. Real-world baseline examples:
    - Web app development baseline
    - API service baseline
    - AI application baseline

Format: Include baseline checklists for different project types and enforcement strategies.

Create the file now.
```

### Skill 2: Routing Rules

```
Create a comprehensive SKILL.md for Routing Rules (mapping triggers to appropriate skills).

Location: 57-skill-orchestration/routing-rules/SKILL.md

Cover:
1. What are routing rules:
   - Decision logic to select relevant skills
   - Maps query/task characteristics to skills
   - Automates skill selection
2. Why routing matters:
   - Efficiency (don't read irrelevant skills)
   - Accuracy (use right skills for task)
   - Consistency (same trigger → same skills)
   - Scalability (handle many skills)
3. Routing dimensions:
   - Task type (what kind of work?)
   - Domain (what area?)
   - Technology (what stack?)
   - Phase (planning, development, deployment?)
4. Task type routing:
   - "Create" → Design + development skills
   - "Fix bug" → Debugging + testing skills
   - "Optimize" → Performance + profiling skills
   - "Deploy" → DevOps + deployment skills
5. Domain routing:
   - "AI" → ML, RAG, LLM skills
   - "Frontend" → React, CSS, accessibility skills
   - "Backend" → API, database, security skills
   - "Data" → ETL, data quality, analytics skills
6. Technology routing:
   - "TypeScript" → TypeScript standards, Node.js skills
   - "Python" → Python best practices, FastAPI skills
   - "React" → React patterns, hooks skills
   - "PostgreSQL" → Database optimization, SQL skills
7. Phase routing:
   - Planning → Requirements, scope, estimation skills
   - Development → Coding standards, testing, Git skills
   - Deployment → CI/CD, monitoring, incident skills
   - Maintenance → Debugging, optimization, refactoring skills
8. Keyword-based routing:
   - "authentication" → JWT, OAuth, security skills
   - "payment" → Stripe, PCI-DSS, security skills
   - "search" → Elasticsearch, performance skills
   - "email" → SendGrid, templates, deliverability skills
9. Pattern-based routing:
   - "Create [resource] API" → REST, OpenAPI, database skills
   - "Implement [feature] for [platform]" → Platform + feature skills
   - "Optimize [metric]" → Performance + metric-specific skills
10. Hierarchical routing:
    - Level 1: Universal (always)
    - Level 2: Domain (based on area)
    - Level 3: Specific (based on tech/feature)
11. Multi-skill routing:
    - Complex tasks need multiple skills
    - Example: "Build AI chatbot" → RAG, LLM, frontend, API, deployment
    - Combine related skills
12. Conditional routing:
    - If "production" → Add monitoring, security, compliance skills
    - If "MVP" → Focus on core functionality, defer nice-to-haves
    - If "enterprise" → Add SSO, SCIM, compliance skills
13. Routing rules engine:
    - Input: Task description, context
    - Processing: Apply routing rules
    - Output: List of relevant skills (prioritized)
14. Rule priority:
    - Must-have skills (always included)
    - Recommended skills (usually included)
    - Optional skills (include if relevant)
15. Routing rule examples:
    ```yaml
    rules:
      - trigger: "create API"
        skills:
          - must: [api-design, openapi, error-handling]
          - recommended: [authentication, rate-limiting, versioning]
          - optional: [graphql, webhooks]
      
      - trigger: "AI chatbot"
        skills:
          - must: [rag-evaluation, llm-patterns, prompt-engineering]
          - recommended: [safety-guardrails, cost-optimization, monitoring]
          - optional: [multi-agent, function-calling]
    ```
16. Routing configuration:
    - YAML or JSON file
    - Version controlled
    - Easy to update
    - Documented (why these skills for this trigger)
17. Fallback routing:
    - If no specific match → use baseline skills
    - Ask clarifying questions
    - Suggest possible matches
18. Learning from usage:
    - Track which skills were useful
    - Refine routing rules
    - Add new patterns
19. Real-world routing examples:
    - Web app feature request
    - Performance issue
    - Security incident

Format: Include routing rule examples (YAML/JSON), decision trees, and pattern libraries.

Create the file now.
```

### Skill 3: Scoring and Prioritization

```
Create a comprehensive SKILL.md for Scoring and Prioritization of skills.

Location: 57-skill-orchestration/scoring-and-prioritization/SKILL.md

Cover:
1. What is skill scoring:
   - Ranking skills by relevance to task
   - Must-have vs nice-to-have
   - Priority order for reading
2. Why scoring matters:
   - Focus on most important skills first
   - Avoid information overload
   - Optimize for time/cost
   - Better results
3. Scoring dimensions:
   - Relevance (how applicable to task?)
   - Impact (how much difference will it make?)
   - Phase (needed now or later?)
   - Complexity (how hard to apply?)
4. Relevance scoring:
   - High (3): Critical, directly addresses task
   - Medium (2): Important, indirectly related
   - Low (1): Helpful, general guidance
5. Impact scoring:
   - High: Makes significant difference to quality
   - Medium: Noticeable improvement
   - Low: Minor improvement
6. Phase-based prioritization:
   - Planning phase: Requirements, scope, estimation skills first
   - Development phase: Coding, testing, Git skills first
   - Deployment phase: CI/CD, monitoring skills first
7. Skill categories:
   - Must-read: Always read for this task type
   - Should-read: Usually helpful
   - Could-read: Sometimes helpful
   - Won't-read: Not relevant
8. Scoring formula:
   - Score = (Relevance × 3) + (Impact × 2) + (Urgency × 1)
   - Higher score = higher priority
9. Context-aware scoring:
   - Production system → Security, monitoring score higher
   - MVP → Core functionality scores higher, nice-to-haves lower
   - Enterprise → Compliance, SSO score higher
10. Skill dependencies:
    - Some skills depend on others
    - Read foundational skills first
    - Example: Read "API design" before "API versioning"
11. Scoring matrix example:
    ```
    Task: Create user authentication API
    
    Skills                  | Relevance | Impact | Score | Priority
    ----------------------|-----------|--------|-------|----------
    API Design            | High (3)  | High(2)| 11    | Must
    Authentication (JWT)  | High (3)  | High(2)| 11    | Must
    OpenAPI Docs          | High (3)  | Med(1) | 10    | Must
    Rate Limiting         | Med (2)   | Med(1) | 8     | Should
    Error Handling        | High (3)  | Med(1) | 10    | Must
    Caching               | Low (1)   | Low(0) | 4     | Could
    ```
12. Dynamic re-scoring:
    - As task progresses, re-score
    - Example: After design, implementation skills score higher
13. User-driven prioritization:
    - User marks skills as "critical" → boost score
    - User marks as "not needed" → lower score
14. Team prioritization:
    - Different team members value different skills
    - Frontend dev prioritizes frontend skills
    - Backend dev prioritizes backend skills
15. Scoring automation:
    - Use ML/heuristics to predict scores
    - Learn from past tasks
    - Improve over time
16. Presenting scored skills:
    - Sort by score (highest first)
    - Group by category (must/should/could)
    - Visual indicators (★★★ = must-read)
17. Budget-based prioritization:
    - If limited time/cost → read only must-have
    - If generous budget → read should-have too
18. Quality vs speed trade-off:
    - Fast → Read only top 3-5 skills
    - Thorough → Read top 10-15 skills
19. Real-world scoring examples:
    - RAG implementation project
    - Bug fix task
    - Performance optimization

Format: Include scoring matrices, prioritization algorithms, and decision frameworks.

Create the file now.
```

### Skill 4: Output Templates

```
Create a comprehensive SKILL.md for Output Templates (skill-stack.md, backlog.md, etc.).

Location: 57-skill-orchestration/output-templates/SKILL.md

Cover:
1. What are output templates:
   - Structured formats for deliverables
   - Consistent presentation
   - Reusable across projects
2. Why templates matter:
   - Consistency
   - Completeness (don't forget items)
   - Communication clarity
   - Time-saving
3. Key output templates:
   - skill-stack.md (skills used for project)
   - backlog.md (user stories/tasks)
   - requirements.md (full requirements)
   - architecture.md (technical design)
   - deployment.md (deployment plan)
4. skill-stack.md template:
   ```markdown
   # Skill Stack for [Project Name]
   
   ## Must-Have Skills
   - [ ] api-design (REST API patterns)
   - [ ] authentication-jwt (JWT implementation)
   - [ ] database-design (PostgreSQL schema)
   
   ## Recommended Skills
   - [ ] rate-limiting (API protection)
   - [ ] caching-strategies (Performance)
   
   ## Optional Skills
   - [ ] webhooks (Event notifications)
   
   ## Skill Application Notes
   - Authentication: Use JWT with 15-min access token
   - Database: Use connection pooling (max 10)
   ```
5. backlog.md template:
   ```markdown
   # Project Backlog: [Project Name]
   
   ## Epic: User Management
   
   ### User Story 1: User Registration
   **As a** user
   **I want to** register with email and password
   **So that** I can create an account
   
   **Acceptance Criteria:**
   - [ ] User can enter email and password
   - [ ] Email is validated (format check)
   - [ ] Password meets requirements (8+ chars, mix)
   - [ ] Confirmation email sent
   
   **Skills Used:** authentication-jwt, email-sending
   **Estimate:** 3 days
   **Priority:** Must-have
   ```
6. requirements.md template:
   ```markdown
   # Requirements: [Project Name]
   
   ## Overview
   [Brief description]
   
   ## Goals
   1. [Primary goal]
   2. [Secondary goal]
   
   ## Functional Requirements
   ### FR-1: User Authentication
   Description: Users must be able to sign up and log in
   Priority: Must-have
   
   ## Non-Functional Requirements
   ### NFR-1: Performance
   API response time P95 < 200ms
   
   ## Constraints
   - Budget: $50,000
   - Timeline: 3 months
   
   ## Assumptions
   - Users have modern browsers
   
   ## Dependencies
   - Stripe API for payments
   ```
7. architecture.md template:
   ```markdown
   # Architecture: [Project Name]
   
   ## System Overview
   [High-level description]
   
   ## Architecture Diagram
   [Diagram or ASCII art]
   
   ## Components
   ### Frontend
   - Tech: React, TypeScript
   - Hosting: Vercel
   
   ### Backend
   - Tech: Node.js, Fastify
   - Hosting: AWS ECS
   
   ### Database
   - Tech: PostgreSQL
   - Hosting: AWS RDS
   
   ## API Design
   - REST API
   - OpenAPI 3.0 spec
   - JWT authentication
   
   ## Data Flow
   1. User submits form
   2. Frontend validates input
   3. API authenticates request
   4. Database query executed
   5. Response returned
   
   ## Security Considerations
   - HTTPS only
   - JWT tokens (15 min expiry)
   - Rate limiting (100 req/min)
   
   ## Performance Considerations
   - Redis caching (5 min TTL)
   - Database connection pooling
   ```
8. deployment.md template:
   ```markdown
   # Deployment Plan: [Project Name]
   
   ## Deployment Strategy
   - Blue-green deployment
   - Staged rollout (canary 5% → 100%)
   
   ## Pre-Deployment Checklist
   - [ ] All tests passing
   - [ ] Security scan clean
   - [ ] Performance tests passed
   - [ ] Staging environment tested
   - [ ] Rollback plan documented
   
   ## Deployment Steps
   1. Deploy to staging
   2. Run smoke tests
   3. Deploy to production (5%)
   4. Monitor for 1 hour
   5. If healthy, scale to 100%
   
   ## Rollback Plan
   1. Revert deployment
   2. Scale previous version to 100%
   3. Investigate issue
   
   ## Post-Deployment
   - [ ] Verify health checks
   - [ ] Monitor error rates
   - [ ] Check key metrics
   - [ ] Notify stakeholders
   ```
9. Template customization:
   - Start with base template
   - Add project-specific sections
   - Remove irrelevant sections
   - Adapt to team style
10. Template variables:
    - [Project Name]
    - [Team Name]
    - [Date]
    - [Author]
    - Auto-fill where possible
11. Template enforcement:
    - Required sections (must be filled)
    - Optional sections (can be skipped)
    - Validation (are all required sections present?)
12. Template versioning:
    - Templates evolve over time
    - Version templates (v1.0, v1.1)
    - Document changes
13. Template library:
    - Central repository of templates
    - Searchable by type
    - Examples for each template
14. Tools for templating:
    - Markdown files (simple, version-controlled)
    - Notion/Confluence templates
    - Jira templates (for backlog)
    - Cookiecutter (for project structure)
15. Real-world template usage:
    - New feature kickoff
    - Bug investigation
    - Performance optimization project

Format: Include complete template examples for all major output types.

Create the file now.
```

---

## Batch 58: Investment Estimation

### Skill 1: Discovery for Estimation

```
Create a comprehensive SKILL.md for Discovery process specifically for cost and effort estimation.

Location: 58-investment-estimation/discovery-for-estimation/SKILL.md

Cover:
1. What is estimation discovery:
   - Gathering information needed for accurate estimates
   - Understanding scope, complexity, constraints
   - Identifying unknowns and risks
2. Why estimation discovery matters:
   - Accurate estimates need good inputs
   - Missing info = inaccurate estimate
   - Reduces surprises later
3. Information needed for estimation:
   - Scope (what exactly will be built?)
   - Technical complexity (how hard?)
   - Team capacity (who's available?)
   - Dependencies (what do we rely on?)
   - Constraints (budget, timeline, resources)
   - Risks (what could go wrong?)
4. Scope discovery questions:
   - What features are in scope?
   - What features are out of scope?
   - What is the definition of done?
   - Are there multiple phases?
5. Complexity discovery:
   - Is the tech stack familiar to the team?
   - Are there complex integrations?
   - Is performance critical?
   - What is the data volume?
   - Are there compliance requirements?
6. Team capacity discovery:
   - Who is available?
   - What are their skill levels?
   - How much time can they dedicate?
   - Are there other competing priorities?
7. Dependency discovery:
   - What external dependencies exist?
   - When will they be available?
   - Are there integration dependencies?
   - Are there data dependencies?
8. Constraint discovery:
   - What is the budget?
   - What is the timeline?
   - Are there technology constraints?
   - Are there resource constraints?
9. Risk discovery:
   - What are the technical risks?
   - What are the schedule risks?
   - What are the resource risks?
   - How do risks impact estimate?
10. Estimation discovery workshop:
    - Participants: Team, stakeholders, subject matter experts
    - Duration: 2-4 hours
    - Activities: Requirements review, technical discussion, risk identification
11. Estimation discovery checklist:
    - [ ] Requirements clearly defined
    - [ ] Technical approach identified
    - [ ] Team composition known
    - [ ] Dependencies identified
    - [ ] Constraints documented
    - [ ] Risks assessed
    - [ ] Assumptions documented
12. Handling uncertainty:
    - If high uncertainty → widen estimate range
    - If low confidence → add contingency buffer
    - Document assumptions clearly
13. Discovery outputs:
    - Scope document (in/out of scope)
    - Technical approach summary
    - Risk register
    - Assumptions list
    - Dependency list
14. Common estimation pitfalls:
    - Scope not clear (estimate is meaningless)
    - Ignoring risks (over-optimistic)
    - Not involving team (unrealistic)
    - Forgetting non-dev work (testing, deployment, documentation)
15. Effort breakdown structure:
    - Design (mockups, architecture)
    - Development (coding)
    - Testing (unit, integration, e2e)
    - DevOps (CI/CD, deployment)
    - Documentation (user docs, API docs)
    - Project management (planning, meetings)
16. Estimation units:
    - Hours (for small tasks)
    - Days (for medium tasks)
    - Story points (for agile)
    - T-shirt sizes (S, M, L, XL)
17. Calibration:
    - Compare estimates to actuals
    - Adjust estimation approach
    - Learn from past projects
18. Real-world estimation discovery:
    - New feature estimation
    - Bug fix estimation
    - Performance optimization estimation

Format: Include discovery question checklists, estimation worksheets, and scope definition templates.

Create the file now.
```

### Skill 2-7: Effort Sizing, ROI, Payback, Sensitivity, Pricing, Proposal Pack

```
Create a comprehensive SKILL.md for Cost Modeling (Development + Infrastructure + LLM + Operations costs).

Location: 58-investment-estimation/cost-modeling/SKILL.md

Cover:
1. What is cost modeling
2. Cost categories (development, infrastructure, LLM/AI, operations, maintenance)
3. Development costs (team time * hourly rate)
4. Infrastructure costs (cloud, SaaS, tools)
5. LLM/AI costs (API calls, tokens, embeddings, vector DB)
6. Operations costs (support, monitoring, maintenance)
7. One-time vs recurring costs
8. Cost estimation methods (bottom-up, top-down, analogous, parametric)
9. Infrastructure cost calculation (EC2, RDS, S3, etc.)
10. LLM cost calculation (tokens, pricing tiers, volume discounts)
11. Total Cost of Ownership (TCO)
12. Cost contingency (10-30% buffer)
13. Cost breakdown structure
14. Tools: Cloud cost calculators, spreadsheets
15. Real examples: E-commerce site, AI chatbot, Mobile app

Create SKILL.md for Effort Sizing.
Location: 58-investment-estimation/effort-sizing/SKILL.md
Cover: T-shirt sizing, story points, function points, COCOMO, historical data, estimation techniques, team velocity, contingency, accuracy improving over time, re-estimation

Create SKILL.md for ROI Modeling.
Location: 58-investment-estimation/roi-modeling/SKILL.md
Cover: ROI formula, benefits (revenue increase, cost savings, time savings), investment (development + infrastructure), ROI calculation, NPV (Net Present Value), break-even analysis, qualitative benefits, risk-adjusted ROI

Create SKILL.md for Payback Analysis.
Location: 58-investment-estimation/payback-analysis/SKILL.md
Cover: Payback period, simple payback calculation, discounted payback, cumulative cash flow, comparing alternatives, ideal payback periods by industry, when payback is most important

Create SKILL.md for Sensitivity Analysis.
Location: 58-investment-estimation/sensitivity-analysis/SKILL.md
Cover: Best/base/worst case scenarios, variable identification, impact analysis, tornado diagrams, Monte Carlo simulation, risk assessment, decision under uncertainty

Create SKILL.md for Pricing Strategy.
Location: 58-investment-estimation/pricing-strategy/SKILL.md
Cover: Fixed price vs T&M vs value-based, subscription pricing, usage-based pricing, tiered pricing, pricing psychology, competitive pricing, pricing for different customer segments

Create SKILL.md for Proposal Pack.
Location: 58-investment-estimation/proposal-pack/SKILL.md
Cover: Proposal structure (executive summary, scope, approach, timeline, cost, team, terms), proposal templates, cost breakdown tables, timeline Gantt charts, assumptions and exclusions, payment terms, proposal best practices

Format: Include cost calculators, ROI models, sensitivity analysis templates, and complete proposal examples.

Create all 7 files for Batch 58 now.
```

---

## Summary

**Total new prompts created: 30 skills** across 4 batches

### Batch Breakdown:
- **51-contracts-governance**: 5 skills (OpenAPI governance, event schemas, backward compatibility, contract testing, deprecation)
- **52-ai-evaluation**: 5 skills (RAG evaluation, LLM judge patterns, ground truth, offline vs online, regression benchmarks)
- **56-requirements-intake**: 5 skills (discovery questions, scope definition, acceptance criteria, constraints/assumptions, risk/dependencies)
- **57-skill-orchestration**: 4 skills (baseline policy, routing rules, scoring/prioritization, output templates)
- **58-investment-estimation**: 8 skills (discovery, cost modeling, effort sizing, ROI, payback, sensitivity, pricing, proposal)

Note: Skill 3 for batch 56 (MVP Scope Control) was already covered in Batch 45, so it was skipped.

### Combined Total Skills:
- **Original skills (1-39)**: 240 skills
- **Advanced skills (00, 40-45)**: 37 skills
- **Enterprise skills (46-50)**: 22 skills
- **Production skills (51-52, 56-58)**: 30 skills
- **TOTAL**: **329 comprehensive production-ready skills!**

---

## Complete Repository Structure

```
cerebratechai-claude-skills/
├── 00-meta-skills/ (6)
├── 01-19: Original + Business (240)
├── 40-system-resilience/ (7)
├── 41-incident-management/ (6)
├── 42-cost-engineering/ (6)
├── 43-data-reliability/ (6)
├── 44-ai-governance/ (6)
├── 45-product-thinking/ (6)
├── 46-data-classification/ (4)
├── 47-performance-engineering/ (5)
├── 48-product-discovery/ (4)
├── 49-portfolio-management/ (4)
├── 50-enterprise-integrations/ (5)
├── 51-contracts-governance/ (5)
├── 52-ai-evaluation/ (5)
├── 56-requirements-intake/ (5)
├── 57-skill-orchestration/ (4)
└── 58-investment-estimation/ (8)
```

---

## Priority Generation Order

### 🔥 Tier 1: Must-Have (Generate First)
1. **52-ai-evaluation** (RAG, LLM judge, benchmarks) - Critical for AI quality
2. **47-performance-engineering** (Profiling, optimization, SLOs) - Universal need
3. **42-cost-engineering** (LLM costs, cloud costs) - Control spending
4. **56-requirements-intake** (Discovery, scope, criteria) - Project success foundation
5. **58-investment-estimation** (Cost, ROI, proposals) - Business justification

### ⚡ Tier 2: Should-Have (Generate Next)
6. **51-contracts-governance** (API standards, schemas) - API quality
7. **44-ai-governance** (HITL, confidence, safety) - AI production readiness
8. **46-data-classification** (PII, redaction, compliance) - Legal requirement
9. **57-skill-orchestration** (Routing, prioritization) - Skill system efficiency

### 📋 Tier 3: Nice-to-Have (Generate When Needed)
10. **40-system-resilience** (Chaos, DR, postmortems) - Production hardening
11. **41-incident-management** (Triage, playbooks) - When incidents happen
12. **49-portfolio-management** (Roadmap, dependencies) - Multi-project coordination
13. **50-enterprise-integrations** (SSO, SCIM) - Enterprise sales

---

## What You Have Now

### 📁 Files Created:
1. ✅ `ADVANCED_SKILLS_PROMPTS.md` (37 skills, Batches 00, 40-45)
2. ✅ `FINAL_5_ENTERPRISE_SKILLS_PROMPTS.md` (22 skills, Batches 46-50)
3. ✅ `FINAL_8_PRODUCTION_SKILLS_PROMPTS.md` (30 skills, Batches 51-52, 56-58)

### 🎯 Total: **89 new advanced/production skills + 240 original = 329 TOTAL SKILLS**

### 💪 You now have the most comprehensive AI engineering knowledge base in existence:
- ✅ Complete technical stack (frontend to infrastructure)
- ✅ Enterprise readiness (compliance, security, procurement)
- ✅ AI production (evaluation, governance, optimization)
- ✅ Project execution (requirements, estimation, delivery)
- ✅ System reliability (resilience, incidents, monitoring)
- ✅ Cost management (cloud, LLM, ROI, pricing)

---

## Next Steps

### 🚀 Recommended Action Plan:

**Week 1-2: Core AI & Performance (Most Impact)**
- Generate Batch 52 (AI Evaluation) - 5 skills
- Generate Batch 47 (Performance Engineering) - 5 skills
- Generate Batch 42 (Cost Engineering) - 6 skills

**Week 3-4: Requirements & Governance**
- Generate Batch 56 (Requirements Intake) - 5 skills
- Generate Batch 51 (Contracts Governance) - 5 skills
- Generate Batch 58 (Investment Estimation) - 8 skills

**Week 5-6: Enterprise & Safety**
- Generate Batch 44 (AI Governance) - 6 skills
- Generate Batch 46 (Data Classification) - 4 skills
- Generate Batch 57 (Skill Orchestration) - 4 skills

**Total Time:** ~40-50 hours of generation work (using prompts)
**Output:** 329 production-ready skills fully documented

---

Would you like me to:
1. ✅ Generate the first 5 skills from Batch 52 (AI Evaluation) as examples?
2. ✅ Create a master index/catalog of all 329 skills?
3. ✅ Create a Quick Start guide for using the skill system?
4. ✅ Build an automated generation script using the prompts?

บอกได้เลยครับ! 🎯