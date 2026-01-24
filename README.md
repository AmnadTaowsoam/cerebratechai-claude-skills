# 🧠 CerebraTechAI - Claude Skills Repository

> **Comprehensive skill library for Claude AI to build production-ready applications**

A curated collection of **483+ specialized skills** across **73 categories** covering everything from core development to advanced features like AI/ML, blockchain, IoT, system resilience, platform engineering, governance, and more. Each skill provides detailed implementation guides, best practices, and production-ready code examples.

[![Skills](https://img.shields.io/badge/Skills-483+-blue)](https://github.com/AmnadTaowsoam/cerebraSkills)
[![Categories](https://img.shields.io/badge/Categories-73-purple)](https://github.com/AmnadTaowsoam/cerebraSkills)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

## 📚 Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Skill Categories](#skill-categories)
- [Project Type Guide](#project-type-guide)
- [How to Use](#how-to-use)
- [Installation](#installation)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

This repository contains specialized skills that help Claude understand and implement best practices across various domains. Each skill is a comprehensive markdown document with:

- ✅ Detailed implementation guides
- ✅ Production-ready code examples
- ✅ Best practices and anti-patterns
- ✅ Testing strategies
- ✅ Security considerations
- ✅ Performance optimization tips

### 🌟 Key Features

- **483+ Skills** covering full-stack development across **73 categories**
- **Production-Ready** patterns and examples
- **Language Support**: TypeScript, Python, SQL, and more
- **Framework Coverage**: Next.js, React, FastAPI, Express, and more
- **Cloud & DevOps**: AWS, Docker, Kubernetes, CI/CD
- **AI/ML**: LLM integration, RAG, embeddings, model deployment, AI evaluation
- **Specialized Domains**: E-commerce, IoT, Blockchain, Gaming, Video Streaming
- **Enterprise**: System resilience, cost engineering, incident management
- **Product & Strategy**: Product discovery, portfolio management, investment estimation

---

## 🚀 Quick Start

### 🎯 Recommended: GitHub MCP Server Setup

**The easiest way to use these skills with Claude Desktop!**

📖 **Setup Guides:**
- 🇬🇧 **English**: [GITHUB_MCP_SETUP.md](./GITHUB_MCP_SETUP.md) - Complete setup guide (15-20 min)
- 🇹🇭 **ภาษาไทย**: [SETUP_TH.md](./SETUP_TH.md) - คู่มือภาษาไทยฉบับเต็ม (15-20 นาที)
- ⚡ **Quick Start**: [QUICKSTART_MCP.md](./QUICKSTART_MCP.md) - 5-minute setup (English/Thai)

**What you'll get:**
- ✅ Automatic sync across all devices
- ✅ Always up-to-date skills from GitHub
- ✅ Works with Claude Desktop & Claude Code (VS Code)
- ✅ No manual file copying needed

---

### 🤖 All AI Platforms Setup

**Use these skills with ANY AI coding assistant!**

📖 **Multi-Platform Guides:**
- 🌐 **All Platforms (English)**: [SETUP_ALL_PLATFORMS.md](./SETUP_ALL_PLATFORMS.md)
  - Claude Desktop (MCP)
  - Claude Code (VS Code)
  - GitHub Codex (Copilot)
  - Roo Code (Cursor)
  - Antigravity (Google DeepMind)

- 🇹🇭 **ทุก Platform (ภาษาไทย)**: [SETUP_ALL_PLATFORMS_TH.md](./SETUP_ALL_PLATFORMS_TH.md)
  - Claude Desktop (MCP)
  - Claude Code (VS Code)
  - GitHub Codex (Copilot)
  - Roo Code (Cursor)
  - Antigravity (Google DeepMind)

📖 **Platform-Specific Guides:**
- 🟢 **GitHub Codex (Copilot)**:
  - 🇬🇧 English: [SETUP_CODEX.md](./SETUP_CODEX.md) - Complete Copilot guide
  - 🇹🇭 ภาษาไทย: [SETUP_CODEX_TH.md](./SETUP_CODEX_TH.md) - คู่มือ Copilot ฉบับเต็ม

**Comparison:**
| Platform | Setup | Auto-sync | Best For |
|----------|-------|-----------|----------|
| Claude Desktop | ⭐⭐ Easy | ✅ Yes | Standalone use |
| Claude Code | ⭐ Very Easy | ✅ Yes | VS Code users |
| GitHub Codex | ⭐⭐⭐ Medium | ⚠️ Manual | Copilot users |
| Roo Code | ⭐⭐ Easy | ✅ Yes (MCP) | Cursor users |
| Antigravity | ⭐⭐ Easy | ⚠️ Manual | Local skills |

---

### Alternative: Manual Setup

#### For Claude Desktop/CLI Users

1. **Clone the repository**
```bash
git clone https://github.com/AmnadTaowsoam/cerebraSkills.git
cd cerebraSkills
```

2. **Link to Claude's skills directory**
```bash
# Create symbolic link (macOS/Linux)
ln -s $(pwd) /mnt/skills/user/cerebratechai

# Or copy directly
cp -r . /mnt/skills/user/cerebratechai
```

3. **Use in Claude**
```
User: "Create a Next.js API endpoint following our nextjs-patterns skill"
Claude: [reads skill and implements according to best practices]
```

#### For Claude.ai Web Users

Simply reference skills in your conversations:
```
"Following the typescript-standards and nextjs-patterns skills, 
create a user authentication system with JWT"
```

---

## 📦 Skill Categories

### 01. 🏗️ Foundations (5 skills)
Core development standards and practices.

- [TypeScript Standards](01-foundations/typescript-standards/SKILL.md) - TypeScript best practices
- [Python Standards](01-foundations/python-standards/SKILL.md) - Python coding standards
- [Code Review](01-foundations/code-review/SKILL.md) - Code review guidelines
- [Git Workflow](01-foundations/git-workflow/SKILL.md) - Git branching and commits
- [API Design](01-foundations/api-design/SKILL.md) - RESTful API principles

### 00. 🎯 Meta Skills (5 skills)
Strategic thinking and architectural practices.

- [Architectural Reviews](00-meta-skills/architectural-reviews/SKILL.md) - Architecture review process
- [Decision Records](00-meta-skills/decision-records/SKILL.md) - ADR documentation
- [Risk Assessment](00-meta-skills/risk-assessment/SKILL.md) - Technical risk evaluation
- [System Thinking](00-meta-skills/system-thinking/SKILL.md) - Holistic system analysis
- [Technical Debt Management](00-meta-skills/technical-debt-management/SKILL.md) - Managing tech debt

### 02. 🎨 Frontend Development (12 skills)
Modern frontend frameworks and patterns.

- [Next.js Patterns](02-frontend/nextjs-patterns/SKILL.md) - Next.js 14+ App Router
- [React Best Practices](02-frontend/react-best-practices/SKILL.md) - React patterns
- [Tailwind Patterns](02-frontend/tailwind-patterns/SKILL.md) - Tailwind CSS
- [Material-UI](02-frontend/mui-material/SKILL.md) - MUI components
- [shadcn/ui](02-frontend/shadcn-ui/SKILL.md) - shadcn/ui patterns
- [Form Handling](02-frontend/form-handling/SKILL.md) - React Hook Form + Zod
- [Multi-Step Forms](02-frontend/multi-step-forms/SKILL.md) - Wizard patterns, validation, progress tracking
- [State Management](02-frontend/state-management/SKILL.md) - Zustand, Redux, TanStack Query
- [Animation](02-frontend/animation/SKILL.md) - Framer Motion, CSS animations
- [Infinite Scroll](02-frontend/infinite-scroll/SKILL.md) - Virtual scrolling, Intersection Observer
- [Error Boundaries React](02-frontend/error-boundaries-react/SKILL.md) - React error boundaries
- [State Machines XState](02-frontend/state-machines-xstate/SKILL.md) - XState state machines

### 03. ⚙️ Backend API (10 skills)
Backend development patterns.

- [Node.js API](03-backend-api/nodejs-api/SKILL.md) - Node.js REST APIs
- [FastAPI Patterns](03-backend-api/fastapi-patterns/SKILL.md) - FastAPI Python
- [Express REST](03-backend-api/express-rest/SKILL.md) - Express.js patterns
- [Fastify REST API](03-backend-api/fastify-rest-api/SKILL.md) - Fastify patterns
- [GraphQL Best Practices](03-backend-api/graphql-best-practices/SKILL.md) - GraphQL patterns
- [gRPC Integration](03-backend-api/grpc-integration/SKILL.md) - gRPC integration
- [Error Handling](03-backend-api/error-handling/SKILL.md) - Error patterns
- [Validation](03-backend-api/validation/SKILL.md) - Request validation
- [Middleware](03-backend-api/middleware/SKILL.md) - Middleware patterns
- [WebSocket Patterns](03-backend-api/websocket-patterns/SKILL.md) - WebSocket implementation

### 04. 🗄️ Database (11 skills)
Database design and optimization.

- [Prisma Guide](04-database/prisma-guide/SKILL.md) - Prisma ORM
- [MongoDB Patterns](04-database/mongodb-patterns/SKILL.md) - MongoDB
- [Redis Caching](04-database/redis-caching/SKILL.md) - Redis patterns
- [TimescaleDB](04-database/timescaledb/SKILL.md) - Time-series database
- [Vector Database](04-database/vector-database/SKILL.md) - Pinecone, Qdrant, Weaviate
- [Database Optimization](04-database/database-optimization/SKILL.md) - Performance tuning
- [Database Migrations](04-database/database-migrations/SKILL.md) - Schema migrations
- [Database Transactions](04-database/database-transactions/SKILL.md) - Transaction management
- [Connection Pooling](04-database/connection-pooling/SKILL.md) - Connection pool management
- [Cache Invalidation](04-database/cache-invalidation/SKILL.md) - Cache invalidation patterns
- [Database Locking](04-database/database-locking/SKILL.md) - Locking strategies

### 05. 🤖 AI/ML Core (8 skills)
Machine learning and model development.

- [PyTorch Deployment](05-ai-ml-core/pytorch-deployment/SKILL.md) - PyTorch production
- [YOLO Integration](05-ai-ml-core/yolo-integration/SKILL.md) - YOLO object detection
- [Model Training](05-ai-ml-core/model-training/SKILL.md) - Training workflows
- [Model Optimization](05-ai-ml-core/model-optimization/SKILL.md) - Quantization, pruning
- [Model Versioning](05-ai-ml-core/model-versioning/SKILL.md) - MLflow registry
- [Data Preprocessing](05-ai-ml-core/data-preprocessing/SKILL.md) - Data pipelines
- [Data Augmentation](05-ai-ml-core/data-augmentation/SKILL.md) - Augmentation techniques
- [Label Studio](05-ai-ml-core/label-studio-setup/SKILL.md) - Data labeling

### 06. 🚀 AI/ML Production (11 skills)
Production AI/ML systems.

- [LLM Integration](06-ai-ml-production/llm-integration/SKILL.md) - OpenAI, Anthropic, Azure
- [Local LLM Deployment](06-ai-ml-production/llm-local-deployment/SKILL.md) - Ollama, vLLM
- [RAG Implementation](06-ai-ml-production/rag-implementation/SKILL.md) - Retrieval-Augmented Generation
- [Embedding Models](06-ai-ml-production/embedding-models/SKILL.md) - Text embeddings
- [Vector Search](06-ai-ml-production/vector-search/SKILL.md) - Semantic search
- [Prompt Engineering](06-ai-ml-production/prompt-engineering/SKILL.md) - Prompt patterns
- [LLM Guardrails](06-ai-ml-production/llm-guardrails/SKILL.md) - NeMo Guardrails
- [AI Observability](06-ai-ml-production/ai-observability/SKILL.md) - Monitoring
- [LLM Function Calling](06-ai-ml-production/llm-function-calling/SKILL.md) - Tool use with LLMs
- [Agent Patterns](06-ai-ml-production/agent-patterns/SKILL.md) - AI agent architectures
- [Vector Search Patterns](06-ai-ml-production/vector-search-patterns/SKILL.md) - Advanced vector search

### 07. 📄 Document Processing (5 skills)
OCR and document parsing.

- [Tesseract OCR](07-document-processing/ocr-tesseract/SKILL.md) - Tesseract
- [PaddleOCR](07-document-processing/ocr-paddleocr/SKILL.md) - PaddleOCR
- [Document Parsing](07-document-processing/document-parsing/SKILL.md) - Structured parsing
- [PDF Processing](07-document-processing/pdf-processing/SKILL.md) - PDF manipulation
- [Image Preprocessing](07-document-processing/image-preprocessing/SKILL.md) - OpenCV

### 08. 📨 Messaging & Queue (5 skills)
Message queuing systems.

- [RabbitMQ Patterns](08-messaging-queue/rabbitmq-patterns/SKILL.md) - RabbitMQ
- [MQTT Integration](08-messaging-queue/mqtt-integration/SKILL.md) - MQTT/IoT
- [Kafka Streams](08-messaging-queue/kafka-streams/SKILL.md) - Apache Kafka
- [Redis Queue](08-messaging-queue/redis-queue/SKILL.md) - Bull/BullMQ
- [Queue Monitoring](08-messaging-queue/queue-monitoring/SKILL.md) - Observability

### 09. 🔧 Microservices (10 skills)
Microservices architecture.

- [Service Design](09-microservices/service-design/SKILL.md) - Design principles
- [API Gateway](09-microservices/api-gateway/SKILL.md) - Kong, NGINX
- [Service Mesh](09-microservices/service-mesh/SKILL.md) - Istio, Linkerd
- [Circuit Breaker](09-microservices/circuit-breaker/SKILL.md) - Resilience patterns
- [Service Discovery](09-microservices/service-discovery/SKILL.md) - Consul, etcd
- [Event-Driven](09-microservices/event-driven/SKILL.md) - Event sourcing, CQRS
- [Escrow Workflow](09-microservices/escrow-workflow/SKILL.md) - Milestone payments, state machines
- [Saga Pattern](09-microservices/saga-pattern/SKILL.md) - Distributed transactions
- [Event Sourcing](09-microservices/event-sourcing/SKILL.md) - Event sourcing patterns
- [CQRS Pattern](09-microservices/cqrs-pattern/SKILL.md) - Command Query Responsibility Segregation

### 10. 🔐 Authentication & Authorization (5 skills)
Security and access control.

- [JWT Authentication](10-authentication-authorization/jwt-authentication/SKILL.md) - JWT
- [OAuth2](10-authentication-authorization/oauth2-implementation/SKILL.md) - OAuth 2.0
- [RBAC Patterns](10-authentication-authorization/rbac-patterns/SKILL.md) - Role-based access
- [API Key Management](10-authentication-authorization/api-key-management/SKILL.md) - API keys
- [Session Management](10-authentication-authorization/session-management/SKILL.md) - Sessions

### 11. 💳 Billing & Subscription (6 skills)
Payment and subscription systems.

- [Stripe Integration](11-billing-subscription/stripe-integration/SKILL.md) - Stripe
- [Subscription Plans](11-billing-subscription/subscription-plans/SKILL.md) - Plan management
- [Usage Metering](11-billing-subscription/usage-metering/SKILL.md) - API usage tracking
- [Billing Cycles](11-billing-subscription/billing-cycles/SKILL.md) - Billing automation
- [Invoice Generation](11-billing-subscription/invoice-generation/SKILL.md) - PDF invoices
- [Webhook Handling](11-billing-subscription/webhook-handling/SKILL.md) - Payment webhooks

### 12. ⚖️ Compliance & Governance (6 skills)
Legal compliance and data governance.

- [PDPA Compliance](12-compliance-governance/pdpa-compliance/SKILL.md) - Thai PDPA
- [GDPR Compliance](12-compliance-governance/gdpr-compliance/SKILL.md) - EU GDPR
- [Data Privacy](12-compliance-governance/data-privacy/SKILL.md) - Privacy patterns
- [Audit Logging](12-compliance-governance/audit-logging/SKILL.md) - Audit trails
- [Consent Management](12-compliance-governance/consent-management/SKILL.md) - User consent
- [Data Retention](12-compliance-governance/data-retention/SKILL.md) - Retention policies

### 13. 📁 File Storage (6 skills)
File management and CDN.

- [S3 Integration](13-file-storage/s3-integration/SKILL.md) - AWS S3, MinIO
- [File Upload](13-file-storage/file-upload-handling/SKILL.md) - Secure uploads
- [Multipart Upload](13-file-storage/multipart-upload/SKILL.md) - Large files
- [File Compression](13-file-storage/file-compression/SKILL.md) - Compression
- [CDN Integration](13-file-storage/cdn-integration/SKILL.md) - CloudFront, Cloudflare
- [Image Optimization](13-file-storage/image-optimization/SKILL.md) - Image processing

### 14. 📊 Monitoring & Observability (6 skills)
Application monitoring and logging.

- [Prometheus Metrics](14-monitoring-observability/prometheus-metrics/SKILL.md) - Metrics
- [Grafana Dashboards](14-monitoring-observability/grafana-dashboards/SKILL.md) - Dashboards
- [ELK Stack](14-monitoring-observability/elk-stack/SKILL.md) - Elasticsearch, Logstash, Kibana
- [Distributed Tracing](14-monitoring-observability/distributed-tracing/SKILL.md) - OpenTelemetry
- [Error Tracking](14-monitoring-observability/error-tracking/SKILL.md) - Sentry
- [Performance Monitoring](14-monitoring-observability/performance-monitoring/SKILL.md) - APM

### 15. 🐳 DevOps & Infrastructure (11 skills)
Infrastructure as code and CI/CD.

- [Docker Patterns](15-devops-infrastructure/docker-patterns/SKILL.md) - Docker
- [Docker Compose](15-devops-infrastructure/docker-compose/SKILL.md) - Multi-container
- [Kubernetes](15-devops-infrastructure/kubernetes-deployment/SKILL.md) - K8s deployment
- [Service Orchestration](15-devops-infrastructure/service-orchestration/SKILL.md) - Service discovery, deployment strategies
- [Helm Charts](15-devops-infrastructure/helm-charts/SKILL.md) - Helm
- [GitHub Actions](15-devops-infrastructure/ci-cd-github-actions/SKILL.md) - CI/CD
- [Terraform](15-devops-infrastructure/terraform-infrastructure/SKILL.md) - IaC
- [Secrets Management](15-devops-infrastructure/secrets-management/SKILL.md) - Vault
- [Load Balancing](15-devops-infrastructure/load-balancing/SKILL.md) - Load balancer patterns
- [GitOps ArgoCD](15-devops-infrastructure/gitops-argocd/SKILL.md) - GitOps with ArgoCD
- [Multi-Cloud Patterns](15-devops-infrastructure/multi-cloud-patterns/SKILL.md) - Multi-cloud strategies

### 16. 🧪 Testing (9 skills)
Testing strategies and frameworks.

- [Jest Patterns](16-testing/jest-patterns/SKILL.md) - Jest testing
- [Pytest Patterns](16-testing/pytest-patterns/SKILL.md) - Python testing
- [E2E Playwright](16-testing/e2e-playwright/SKILL.md) - End-to-end testing
- [Integration Testing](16-testing/integration-testing/SKILL.md) - Integration tests
- [Event-Driven Testing](16-testing/event-driven-testing/SKILL.md) - Saga testing, event replay
- [Load Testing](16-testing/load-testing/SKILL.md) - k6, Artillery
- [ML Model Testing](16-testing/ml-model-testing/SKILL.md) - Model validation
- [Test Data Factory](16-testing/test-data-factory/SKILL.md) - Test data
- [Contract Testing Pact](16-testing/contract-testing-pact/SKILL.md) - Consumer-driven contract testing

### 17. 🎯 Domain-Specific (10 skills)
Cross-cutting concerns.

- [Multi-Tenancy](17-domain-specific/multi-tenancy/SKILL.md) - Multi-tenant architecture
- [Multi-Tenancy Advanced](17-domain-specific/multi-tenancy-advanced/SKILL.md) - Advanced multi-tenant patterns
- [Rate Limiting](17-domain-specific/rate-limiting/SKILL.md) - Rate limiting
- [API Versioning](17-domain-specific/api-versioning/SKILL.md) - Versioning strategies
- [API Versioning Strategies](17-domain-specific/api-versioning-strategies/SKILL.md) - Advanced versioning patterns
- [Feature Flags](17-domain-specific/feature-flags/SKILL.md) - Feature toggles
- [Analytics Tracking](17-domain-specific/analytics-tracking/SKILL.md) - Analytics
- [Notification System](17-domain-specific/notification-system/SKILL.md) - Notifications
- [QR Code Features](17-domain-specific/qr-code-features/SKILL.md) - QR generation, scanning, security
- [Thai Cultural Events](17-domain-specific/thai-cultural-events/SKILL.md) - Thai weddings, ordinations, merit-making

### 18. 📋 Project Management (7 skills)
Agile and project planning.

- [Agile Scrum](18-project-management/agile-scrum/SKILL.md) - Scrum methodology
- [Project Planning](18-project-management/project-planning/SKILL.md) - Planning techniques
- [Requirement Analysis](18-project-management/requirement-analysis/SKILL.md) - Requirements
- [User Stories](18-project-management/user-stories/SKILL.md) - Story writing
- [Technical Specs](18-project-management/technical-specifications/SKILL.md) - Tech specs
- [Estimation](18-project-management/estimation-techniques/SKILL.md) - Estimation
- [Risk Management](18-project-management/risk-management/SKILL.md) - Risk management

### 19. 🔍 SEO Optimization (7 skills)
Search engine optimization.

- [Technical SEO](19-seo-optimization/technical-seo/SKILL.md) - Technical SEO
- [Next.js SEO](19-seo-optimization/nextjs-seo/SKILL.md) - Next.js optimization
- [Meta Tags](19-seo-optimization/meta-tags/SKILL.md) - Social media tags
- [Structured Data](19-seo-optimization/structured-data/SKILL.md) - Schema.org
- [Sitemap & Robots](19-seo-optimization/sitemap-robots/SKILL.md) - Sitemaps
- [Page Speed](19-seo-optimization/page-speed/SKILL.md) - Performance
- [Core Web Vitals](19-seo-optimization/core-web-vitals/SKILL.md) - Web vitals

### 20. 🤖 AI Integration (6 skills)
AI-powered features.

- [llm.txt Protocol](20-ai-integration/llm-txt-protocol/SKILL.md) - llm.txt
- [AI Agents](20-ai-integration/ai-agents/SKILL.md) - LangChain agents
- [Chatbot](20-ai-integration/chatbot-integration/SKILL.md) - Chatbot UI
- [AI Search](20-ai-integration/ai-search/SKILL.md) - Semantic search
- [Conversational UI](20-ai-integration/conversational-ui/SKILL.md) - Chat interfaces
- [LINE Platform Integration](20-ai-integration/line-platform-integration/SKILL.md) - LINE Messaging API, LIFF, Rich Menus

### 21. 📝 Documentation (6 skills)
Technical documentation.

- [Technical Writing](21-documentation/technical-writing/SKILL.md) - Writing guides
- [API Documentation](21-documentation/api-documentation/SKILL.md) - API docs
- [User Guides](21-documentation/user-guides/SKILL.md) - User documentation
- [Architecture Docs](21-documentation/system-architecture-docs/SKILL.md) - System design
- [Runbooks](21-documentation/runbooks/SKILL.md) - Operational runbooks
- [Changelog](21-documentation/changelog-management/SKILL.md) - Changelog management

### 22. 🎨 UX/UI Design (7 skills)
User experience and design.

- [Design Systems](22-ux-ui-design/design-systems/SKILL.md) - Design systems
- [Accessibility](22-ux-ui-design/accessibility/SKILL.md) - Web accessibility
- [Responsive Design](22-ux-ui-design/responsive-design/SKILL.md) - Responsive design
- [Thai UX Patterns](22-ux-ui-design/thai-ux-patterns/SKILL.md) - Thai typography, colors, cultural UX
- [User Research](22-ux-ui-design/user-research/SKILL.md) - User research
- [Wireframing](22-ux-ui-design/wireframing/SKILL.md) - Wireframing
- [Design Handoff](22-ux-ui-design/design-handoff/SKILL.md) - Design to dev

### 23. 📊 Business Analytics (9 skills)
Business intelligence and KPIs.

- [A/B Testing Analysis](23-business-analytics/ab-testing-analysis/SKILL.md) - Experiment analysis
- [Business Intelligence](23-business-analytics/business-intelligence/SKILL.md) - BI fundamentals
- [Cohort Analysis](23-business-analytics/cohort-analysis/SKILL.md) - User cohort tracking
- [Conversion Optimization](23-business-analytics/conversion-optimization/SKILL.md) - Conversion rate improvement
- [Dashboard Design](23-business-analytics/dashboard-design/SKILL.md) - Analytics dashboards
- [Data Visualization](23-business-analytics/data-visualization/SKILL.md) - Charts and graphs
- [Funnel Analysis](23-business-analytics/funnel-analysis/SKILL.md) - Conversion funnels
- [KPI Metrics](23-business-analytics/kpi-metrics/SKILL.md) - Key performance indicators
- [SQL for Analytics](23-business-analytics/sql-for-analytics/SKILL.md) - Analytics SQL patterns

### 24. 🔒 Security Practices (7 skills)
Security best practices.

- [Incident Response](24-security-practices/incident-response/SKILL.md) - Security incident handling
- [OWASP Top 10](24-security-practices/owasp-top-10/SKILL.md) - Common vulnerabilities
- [Penetration Testing](24-security-practices/penetration-testing/SKILL.md) - Security testing
- [Secure Coding](24-security-practices/secure-coding/SKILL.md) - Secure development
- [Security Audit](24-security-practices/security-audit/SKILL.md) - Security assessments
- [Vulnerability Management](24-security-practices/vulnerability-management/SKILL.md) - Vulnerability tracking
- [Secrets Management](24-security-practices/secrets-management/SKILL.md) - Secrets handling and rotation

### 25. 🌍 Internationalization (5 skills)
Multi-language support.

- [Currency & Timezone](25-internationalization/currency-timezone/SKILL.md) - Currency and time handling
- [i18n Setup](25-internationalization/i18n-setup/SKILL.md) - Internationalization setup
- [Localization](25-internationalization/localization/SKILL.md) - Content localization
- [Multi-language](25-internationalization/multi-language/SKILL.md) - Multi-language support
- [RTL Support](25-internationalization/rtl-support/SKILL.md) - Right-to-left languages

### 26. 🚢 Deployment Strategies (5 skills)
Advanced deployment patterns.

- [Blue-Green Deployment](26-deployment-strategies/blue-green-deployment/SKILL.md) - Zero-downtime deployment
- [Canary Deployment](26-deployment-strategies/canary-deployment/SKILL.md) - Gradual rollout
- [Feature Toggles](26-deployment-strategies/feature-toggles/SKILL.md) - Feature flags in deployment
- [Rollback Strategies](26-deployment-strategies/rollback-strategies/SKILL.md) - Safe rollback patterns
- [Rolling Deployment](26-deployment-strategies/rolling-deployment/SKILL.md) - Incremental updates

### 27. 👥 Team Collaboration (5 skills)
Team practices and culture.

- [Code Review Culture](27-team-collaboration/code-review-culture/SKILL.md) - Effective code reviews
- [Knowledge Sharing](27-team-collaboration/knowledge-sharing/SKILL.md) - Team knowledge management
- [Onboarding](27-team-collaboration/onboarding/SKILL.md) - Developer onboarding
- [Pair Programming](27-team-collaboration/pair-programming/SKILL.md) - Collaborative coding
- [Remote Work](27-team-collaboration/remote-work/SKILL.md) - Remote team practices

### 28. 📧 Marketing Integration (6 skills)
Marketing automation and analytics.

- [Email Marketing](28-marketing-integration/email-marketing/SKILL.md) - SendGrid, Mailchimp
- [Social Media](28-marketing-integration/social-media-integration/SKILL.md) - Social APIs
- [Marketing Automation](28-marketing-integration/marketing-automation/SKILL.md) - Automation
- [A/B Testing](28-marketing-integration/ab-testing/SKILL.md) - Experimentation
- [UTM Tracking](28-marketing-integration/utm-tracking/SKILL.md) - Campaign tracking
- [Campaign Management](28-marketing-integration/campaign-management/SKILL.md) - Campaigns

### 29. 💬 Customer Support (6 skills)
Customer support systems.

- [Helpdesk](29-customer-support/helpdesk-integration/SKILL.md) - Zendesk, Intercom
- [Live Chat](29-customer-support/live-chat/SKILL.md) - Real-time chat
- [Ticketing System](29-customer-support/ticketing-system/SKILL.md) - Ticket management
- [Knowledge Base](29-customer-support/knowledge-base/SKILL.md) - Self-service docs
- [Customer Feedback](29-customer-support/customer-feedback/SKILL.md) - Surveys, NPS
- [Support Analytics](29-customer-support/support-analytics/SKILL.md) - Support metrics

### 30. 🛒 E-commerce (8 skills)
E-commerce functionality.

- [Shopping Cart](30-ecommerce/shopping-cart/SKILL.md) - Cart implementation
- [Payment Gateways](30-ecommerce/payment-gateways/SKILL.md) - Stripe, PayPal, 2C2P
- [Order Management](30-ecommerce/order-management/SKILL.md) - Order lifecycle
- [Inventory](30-ecommerce/inventory-management/SKILL.md) - Stock management
- [Product Catalog](30-ecommerce/product-catalog/SKILL.md) - Product management
- [Shipping](30-ecommerce/shipping-integration/SKILL.md) - Carrier integration
- [Discounts](30-ecommerce/discount-promotions/SKILL.md) - Promotions
- [Fulfillment](30-ecommerce/order-fulfillment/SKILL.md) - Order fulfillment

### 31. 📱 Mobile Development (7 skills)
Mobile app development.

- [React Native](31-mobile-development/react-native-patterns/SKILL.md) - React Native
- [Flutter](31-mobile-development/flutter-patterns/SKILL.md) - Flutter
- [Push Notifications](31-mobile-development/push-notifications/SKILL.md) - FCM, APNs
- [Deep Linking](31-mobile-development/deep-linking/SKILL.md) - Universal links
- [Offline Mode](31-mobile-development/offline-mode/SKILL.md) - Offline-first
- [App Distribution](31-mobile-development/app-distribution/SKILL.md) - App stores
- [Mobile CI/CD](31-mobile-development/mobile-ci-cd/SKILL.md) - Fastlane

### 32. 🤝 CRM Integration (6 skills)
Customer relationship management.

- [Salesforce](32-crm-integration/salesforce-integration/SKILL.md) - Salesforce API
- [HubSpot](32-crm-integration/hubspot-integration/SKILL.md) - HubSpot API
- [Custom CRM](32-crm-integration/custom-crm/SKILL.md) - Build your own
- [Lead Management](32-crm-integration/lead-management/SKILL.md) - Lead lifecycle
- [Contact Management](32-crm-integration/contact-management/SKILL.md) - Contacts
- [Sales Pipeline](32-crm-integration/sales-pipeline/SKILL.md) - Pipeline management

### 33. 📰 Content Management (6 skills)
Headless CMS integration.

- [Headless CMS](33-content-management/headless-cms/SKILL.md) - CMS overview
- [Strapi](33-content-management/strapi-integration/SKILL.md) - Strapi CMS
- [Contentful](33-content-management/contentful-integration/SKILL.md) - Contentful
- [WordPress API](33-content-management/wordpress-api/SKILL.md) - WordPress headless
- [Content Versioning](33-content-management/content-versioning/SKILL.md) - Versioning
- [Media Library](33-content-management/media-library/SKILL.md) - Asset management

### 34. ⚡ Real-time Features (6 skills)
Real-time functionality.

- [WebSocket](34-real-time-features/websocket-patterns/SKILL.md) - WebSocket patterns
- [SSE](34-real-time-features/server-sent-events/SKILL.md) - Server-Sent Events
- [Real-time Dashboard](34-real-time-features/real-time-dashboard/SKILL.md) - Live dashboards
- [Collaborative Editing](34-real-time-features/collaborative-editing/SKILL.md) - Google Docs-like
- [Presence](34-real-time-features/presence-detection/SKILL.md) - Online/offline status
- [Live Notifications](34-real-time-features/live-notifications/SKILL.md) - Push notifications

### 35. ⛓️ Blockchain/Web3 (6 skills)
Web3 integration.

- [Web3 Integration](35-blockchain-web3/web3-integration/SKILL.md) - Web3.js, Ethers.js
- [Smart Contracts](35-blockchain-web3/smart-contracts/SKILL.md) - Contract integration
- [Wallet Connection](35-blockchain-web3/wallet-connection/SKILL.md) - MetaMask, WalletConnect
- [NFT Integration](35-blockchain-web3/nft-integration/SKILL.md) - NFTs
- [Crypto Payment](35-blockchain-web3/cryptocurrency-payment/SKILL.md) - Crypto payments
- [Blockchain Auth](35-blockchain-web3/blockchain-authentication/SKILL.md) - Sign-In with Ethereum

### 36. 🌐 IoT Integration (6 skills)
Internet of Things.

- [IoT Protocols](36-iot-integration/iot-protocols/SKILL.md) - MQTT, CoAP
- [Device Management](36-iot-integration/device-management/SKILL.md) - Device lifecycle
- [Sensor Data](36-iot-integration/sensor-data-processing/SKILL.md) - Data processing
- [Real-time Monitoring](36-iot-integration/real-time-monitoring/SKILL.md) - IoT dashboards
- [Edge Computing](36-iot-integration/edge-computing/SKILL.md) - Edge processing
- [IoT Security](36-iot-integration/iot-security/SKILL.md) - IoT security

### 37. 📹 Video Streaming (6 skills)
Video processing and streaming.

- [Video Upload](37-video-streaming/video-upload-processing/SKILL.md) - Upload & processing
- [Live Streaming](37-video-streaming/live-streaming/SKILL.md) - RTMP, HLS, WebRTC
- [Video Transcoding](37-video-streaming/video-transcoding/SKILL.md) - FFmpeg
- [Adaptive Bitrate](37-video-streaming/adaptive-bitrate/SKILL.md) - HLS, DASH
- [Video Analytics](37-video-streaming/video-analytics/SKILL.md) - Engagement tracking
- [CDN Delivery](37-video-streaming/cdn-delivery/SKILL.md) - Video CDN

### 38. 🎮 Gaming Features (6 skills)
Game mechanics and systems.

- [Leaderboards](38-gaming-features/leaderboards/SKILL.md) - Ranking systems
- [Achievements](38-gaming-features/achievements/SKILL.md) - Achievement systems
- [Matchmaking](38-gaming-features/matchmaking/SKILL.md) - Player matching
- [Real-time Multiplayer](38-gaming-features/real-time-multiplayer/SKILL.md) - Multiplayer
- [In-Game Purchases](38-gaming-features/in-game-purchases/SKILL.md) - Virtual goods
- [Game Analytics](38-gaming-features/game-analytics/SKILL.md) - Game metrics

### 39. 🔬 Data Science/ML (6 skills)
Data engineering and ML ops.

- [Data Pipeline](39-data-science-ml/data-pipeline/SKILL.md) - Airflow, ETL
- [Feature Engineering](39-data-science-ml/feature-engineering/SKILL.md) - Feature creation
- [Experiment Tracking](39-data-science-ml/model-experiments/SKILL.md) - MLflow, W&B
- [AutoML](39-data-science-ml/automl/SKILL.md) - Automated ML
- [Model Serving](39-data-science-ml/ml-serving/SKILL.md) - Model deployment
- [A/B Testing ML](39-data-science-ml/ab-testing-ml/SKILL.md) - Model experiments

### 40. 🛡️ System Resilience (5 skills)
Building resilient and fault-tolerant systems.

- [Bulkhead Patterns](40-system-resilience/bulkhead-patterns/SKILL.md) - Bulkhead isolation patterns
- [Disaster Recovery](40-system-resilience/disaster-recovery/SKILL.md) - DR planning
- [Failure Modes](40-system-resilience/failure-modes/SKILL.md) - Failure mode analysis
- [Graceful Degradation](40-system-resilience/graceful-degradation/SKILL.md) - Degradation strategies
- [Idempotency and Dedup](40-system-resilience/idempotency-and-dedup/SKILL.md) - Idempotent operations

### 41. 🚨 Incident Management (6 skills)
Handling production incidents effectively.

- [Communication Templates](41-incident-management/communication-templates/SKILL.md) - Incident communication
- [Escalation and Ownership](41-incident-management/escalation-and-ownership/SKILL.md) - Escalation paths
- [Incident Retrospective](41-incident-management/incident-retrospective/SKILL.md) - Learning from incidents
- [Incident Severity Levels](41-incident-management/incident-severity-levels/SKILL.md) - Severity classification
- [Runbook Templates](41-incident-management/runbook-templates/SKILL.md) - Operational runbooks
- [Triage Workflow](41-incident-management/triage-workflow/SKILL.md) - Incident triage

### 42. 💰 Cost Engineering (7 skills)
Cloud cost optimization and management.

- [Autoscaling and Rightsizing](42-cost-engineering/autoscaling-and-rightsizing/SKILL.md) - Resource optimization
- [Cost Guardrails](42-cost-engineering/cost-guardrails/SKILL.md) - Budget controls
- [Cost Modeling](42-cost-engineering/cost-modeling/SKILL.md) - Cost estimation
- [LLM Token Optimization](42-cost-engineering/llm-token-optimization/SKILL.md) - AI cost management
- [Pricing and Usage Meters](42-cost-engineering/pricing-and-usage-meters/SKILL.md) - Usage tracking
- [Storage Egress Optimization](42-cost-engineering/storage-egress-optimization/SKILL.md) - Data transfer costs

### 43. 📊 Data Reliability (5 skills)
Ensuring data quality and reliability.

- [Data Incident Response](43-data-reliability/data-incident-response/SKILL.md) - Data incident handling
- [Data Quality Rules](43-data-reliability/data-quality-rules/SKILL.md) - Quality validation
- [Freshness and Latency SLOs](43-data-reliability/freshness-latency-slos/SKILL.md) - Data SLOs
- [Lineage and Provenance](43-data-reliability/lineage-and-provenance/SKILL.md) - Data lineage
- [Schema Drift Handling](43-data-reliability/schema-drift-handling/SKILL.md) - Schema evolution

### 44. 📝 Architecture Decision (5 skills)
Architecture documentation and decisions.

- [ADR Templates](44-architecture-decision/adr-templates/SKILL.md) - Decision records
- [Deprecation Policy](44-architecture-decision/deprecation-policy/SKILL.md) - API deprecation
- [System Boundaries](44-architecture-decision/system-boundaries/SKILL.md) - Boundary definition
- [Tradeoff Analysis](44-architecture-decision/tradeoff-analysis/SKILL.md) - Technical tradeoffs
- [Versioning Strategy](44-architecture-decision/versioning-strategy/SKILL.md) - Version management

### 45. 🛠️ Developer Experience (5 skills)
Improving developer productivity.

- [Commit Conventions](45-developer-experience/commit-conventions/SKILL.md) - Commit standards
- [Lint, Format, Typecheck](45-developer-experience/lint-format-typecheck/SKILL.md) - Code quality tools
- [Local Dev Standard](45-developer-experience/local-dev-standard/SKILL.md) - Local development
- [Release Workflow](45-developer-experience/release-workflow/SKILL.md) - Release management
- [Repo Automation Scripts](45-developer-experience/repo-automation-scripts/SKILL.md) - Automation

### 46. 🔐 Data Classification (4 skills)
Data governance and classification.

- [Access Audit and Reviews](46-data-classification/access-audit-and-reviews/SKILL.md) - Access auditing
- [Logging Redaction](46-data-classification/logging-redaction/SKILL.md) - Log sanitization
- [PII Detection](46-data-classification/pii-detection/SKILL.md) - Personal data detection
- [Retention and Deletion](46-data-classification/retention-and-deletion/SKILL.md) - Data lifecycle

### 47. ⚡ Performance Engineering (5 skills)
Application performance optimization.

- [Caching Strategies](47-performance-engineering/caching-strategies/SKILL.md) - Cache patterns
- [Concurrency and Throughput](47-performance-engineering/concurrency-and-throughput/SKILL.md) - Concurrency
- [DB Query Optimization](47-performance-engineering/db-query-optimization/SKILL.md) - Query tuning
- [Profiling Node & Python](47-performance-engineering/profiling-node-python/SKILL.md) - Performance profiling
- [SLA, SLO, SLIs](47-performance-engineering/sla-slo-slis/SKILL.md) - Service level objectives

### 48. 🔍 Product Discovery (5 skills)
Product research and validation.

- [Experiment Design](48-product-discovery/experiment-design/SKILL.md) - Experimentation
- [Hypothesis Writing](48-product-discovery/hypothesis-writing/SKILL.md) - Product hypotheses
- [MVP Scope Control](48-product-discovery/mvp-scope-control/SKILL.md) - MVP scoping
- [User Interviews](48-product-discovery/user-interviews/SKILL.md) - User research
- [Validation Metrics](48-product-discovery/validation-metrics/SKILL.md) - Success metrics

### 49. 📈 Portfolio Management (4 skills)
Managing technical portfolios.

- [Cross-team Interfaces](49-portfolio-management/cross-team-interfaces/SKILL.md) - Team interfaces
- [Delivery Governance](49-portfolio-management/delivery-governance/SKILL.md) - Delivery management
- [Dependency Mapping](49-portfolio-management/dependency-mapping/SKILL.md) - Dependency tracking
- [Roadmap Planning](49-portfolio-management/roadmap-planning/SKILL.md) - Roadmap creation

### 50. 🏢 Enterprise Integrations (5 skills)
Enterprise system integrations.

- [Enterprise RBAC Models](50-enterprise-integrations/enterprise-rbac-models/SKILL.md) - Enterprise RBAC
- [SCIM Provisioning](50-enterprise-integrations/scim-provisioning/SKILL.md) - User provisioning
- [Security Questionnaires](50-enterprise-integrations/security-questionnaires/SKILL.md) - Security compliance
- [SSO SAML OIDC](50-enterprise-integrations/sso-saml-oidc/SKILL.md) - SSO integration
- [Vendor Onboarding](50-enterprise-integrations/vendor-onboarding/SKILL.md) - Vendor management

### 51. 📜 Contracts & Governance (5 skills)
API contracts and governance.

- [Backward Compat Rules](51-contracts-governance/backward-compat-rules/SKILL.md) - Compatibility rules
- [Contract Testing](51-contracts-governance/contract-testing/SKILL.md) - Contract tests
- [Deprecation Notices](51-contracts-governance/deprecation-notices/SKILL.md) - Deprecation handling
- [Event Schema Registry](51-contracts-governance/event-schema-registry/SKILL.md) - Schema registry
- [OpenAPI Governance](51-contracts-governance/openapi-governance/SKILL.md) - API governance

### 52. 🤖 AI Evaluation (5 skills)
Evaluating AI/ML systems.

- [Ground Truth Management](52-ai-evaluation/ground-truth-management/SKILL.md) - Ground truth data
- [LLM Judge Patterns](52-ai-evaluation/llm-judge-patterns/SKILL.md) - LLM evaluation
- [Offline vs Online Eval](52-ai-evaluation/offline-vs-online-eval/SKILL.md) - Evaluation methods
- [RAG Evaluation](52-ai-evaluation/rag-evaluation/SKILL.md) - RAG system evaluation
- [Regression Benchmarks](52-ai-evaluation/regression-benchmarks/SKILL.md) - ML benchmarks

### 53. 🔄 Data Engineering (5 skills)
Modern data engineering practices.

- [dbt Patterns](53-data-engineering/dbt-patterns/SKILL.md) - dbt best practices
- [ELT Modeling](53-data-engineering/elt-modeling/SKILL.md) - ELT patterns
- [Kafka Streaming](53-data-engineering/kafka-streaming/SKILL.md) - Kafka patterns
- [Lakehouse Patterns](53-data-engineering/lakehouse-patterns/SKILL.md) - Data lakehouse

### 54. 🤖 AgentOps (5 skills)
AI agent operations and management.

- [Audit Trails for Agents](54-agentops/audit-trails-for-agents/SKILL.md) - Agent auditing
- [Prompt Versioning](54-agentops/prompt-versioning/SKILL.md) - Prompt management
- [Rollout and Kill Switch](54-agentops/rollout-and-kill-switch/SKILL.md) - Agent deployment
- [Sandboxing](54-agentops/sandboxing/SKILL.md) - Agent isolation
- [Tool Permission Model](54-agentops/tool-permission-model/SKILL.md) - Tool access control

### 55. ✍️ UX Writing (4 skills)
User experience writing.

- [Error Messages](55-ux-writing/error-messages/SKILL.md) - Error copy
- [Microcopy](55-ux-writing/microcopy/SKILL.md) - UI microcopy
- [Onboarding Flows](55-ux-writing/onboarding-flows/SKILL.md) - Onboarding UX
- [Trust Pages Structure](55-ux-writing/trust-pages-structure/SKILL.md) - Trust and safety pages

### 56. 📋 Requirements Intake (5 skills)
Requirements gathering and analysis.

- [Acceptance Criteria](56-requirements-intake/acceptance-criteria/SKILL.md) - AC writing
- [Constraints and Assumptions](56-requirements-intake/constraints-and-assumptions/SKILL.md) - Documenting constraints
- [Discovery Questions](56-requirements-intake/discovery-questions/SKILL.md) - Requirements discovery
- [Requirement to Scope](56-requirements-intake/requirement-to-scope/SKILL.md) - Scope definition
- [Risk and Dependencies](56-requirements-intake/risk-and-dependencies/SKILL.md) - Risk identification

### 57. 🎯 Skill Orchestration (5 skills)
Orchestrating Claude skills.

- [Baseline Policy](57-skill-orchestration/baseline-policy/SKILL.md) - Skill policies
- [Output Templates](57-skill-orchestration/output-templates/SKILL.md) - Template patterns
- [Routing Rules](57-skill-orchestration/routing-rules/SKILL.md) - Skill routing
- [Scoring and Prioritization](57-skill-orchestration/scoring-and-prioritization/SKILL.md) - Skill scoring
- [Skill Improvement Loop](57-skill-orchestration/skill-improvement-loop/SKILL.md) - Continuous skill improvement from real-world usage

### 58. 💵 Investment Estimation (7 skills)
Investment and ROI analysis.

- [Discovery for Estimation](58-investment-estimation/discovery-for-estimation/SKILL.md) - Estimation discovery
- [Effort Sizing](58-investment-estimation/effort-sizing/SKILL.md) - Effort estimation
- [Payback Analysis](58-investment-estimation/payback-analysis/SKILL.md) - Payback calculation
- [Pricing Strategy](58-investment-estimation/pricing-strategy/SKILL.md) - Pricing models
- [Proposal Pack](58-investment-estimation/proposal-pack/SKILL.md) - Proposal templates
- [ROI Modeling](58-investment-estimation/roi-modeling/SKILL.md) - ROI calculation
- [Sensitivity Analysis](58-investment-estimation/sensitivity-analysis/SKILL.md) - Sensitivity modeling

### 71. 🏗️ Infrastructure Patterns (4 skills)
Core infrastructure patterns and integrations.

- [API Design & Contracts](71-infrastructure-patterns/api-design-contracts/SKILL.md) - API design standards
- [Caching Strategies](71-infrastructure-patterns/caching-strategies/SKILL.md) - Cache patterns
- [Secrets & Key Management](71-infrastructure-patterns/secrets-key-management/SKILL.md) - Secrets handling
- [Thai Payment Integration](71-infrastructure-patterns/thai-payment-integration/SKILL.md) - PromptPay, Thai QR, Omise, 2C2P

### 60. 🧩 GitHub MCP (8 skills)
GitHub repository automation via MCP.

- [GitHub Repo Navigation](60-github-mcp/github-repo-navigation/SKILL.md) - Repo discovery and file search
- [GitHub Issue Triage](60-github-mcp/github-issue-triage/SKILL.md) - Issue labeling and routing
- [GitHub PR Lifecycle](60-github-mcp/github-pr-lifecycle/SKILL.md) - PR creation and merge flow
- [GitHub Code Review](60-github-mcp/github-code-review/SKILL.md) - Diff review and risk analysis
- [GitHub Workflow Ops](60-github-mcp/github-workflow-ops/SKILL.md) - Workflow failure diagnosis
- [GitHub Release Management](60-github-mcp/github-release-management/SKILL.md) - Release notes and tags
- [GitHub Security Triage](60-github-mcp/github-security-triage/SKILL.md) - Security alert handling
- [GitHub Repo Governance](60-github-mcp/github-repo-governance/SKILL.md) - Rulesets and permissions

---

## 🎯 Project Type Guide

Choose skills based on your project type:

### 🌐 SaaS Application
**Essential**: 1-6, 10, 18, 19, 21
**Important**: 11, 12, 14, 15, 28, 29
**Nice to Have**: 17, 20

### 🛍️ E-commerce Platform
**Essential**: 1-6, 10, 11, 13, 30
**Important**: 12, 15, 19, 28
**Nice to Have**: 14, 29

### 📱 Mobile App
**Essential**: 1, 3, 4, 10, 31
**Important**: 6, 13, 14, 15
**Nice to Have**: 11, 20, 34

### 🤖 AI/ML Product
**Essential**: 1, 3-6
**Important**: 13, 14, 15, 20, 39
**Nice to Have**: 7, 19, 21

### 🏭 IoT Platform
**Essential**: 1, 3, 4, 8, 36
**Important**: 14, 15, 34
**Nice to Have**: 6, 39

### 🎮 Gaming Platform
**Essential**: 1, 3, 4, 8, 34, 38
**Important**: 10, 11, 14, 15
**Nice to Have**: 13, 37

### 📹 Video Platform
**Essential**: 1, 3, 4, 13, 37
**Important**: 10, 14, 15, 34
**Nice to Have**: 6, 11, 20

### ⛓️ Web3 Application
**Essential**: 1, 2, 3, 35
**Important**: 10, 13, 14, 15
**Nice to Have**: 11, 34

---

## 🛠️ How to Use

### Method 1: Reference in Prompts

```
User: Following the typescript-standards and nextjs-patterns skills,
create a user registration API with email verification.

Claude: [Reads both skills and implements accordingly]
```

### Method 2: Explicit Skill Loading

```
User: Load skills: typescript-standards, prisma-guide, jwt-authentication

User: Now create a complete authentication system

Claude: [Uses all three skills to build the system]
```

### Method 3: Project Context

Create a project-specific context file:

```markdown
# Project: MyApp

## Required Skills
- typescript-standards
- nextjs-patterns
- prisma-guide
- stripe-integration
- pdpa-compliance

## Tech Stack
- Frontend: Next.js 14, React, TailwindCSS
- Backend: Node.js, Prisma, PostgreSQL
- Deployment: Vercel, AWS RDS
```

Then reference: `"Following our project context, create the checkout flow"`

---

## 📥 Installation

### For Development

```bash
# Clone repository
git clone https://github.com/AmnadTaowsoam/cerebraSkills.git
cd cerebraSkills

# No build step required - skills are markdown files
```

### For Claude Desktop

```bash
# macOS/Linux
ln -s $(pwd) ~/.claude/skills/cerebratechai

# Windows (PowerShell as Admin)
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\skills\cerebratechai" -Target $PWD
```

### For Claude.ai Web

Skills are used via conversation references. No installation needed.

---

## 📝 Usage Examples

### Example 1: Full-Stack Feature

```
Create a complete user authentication system following these skills:
- typescript-standards
- nextjs-patterns  
- prisma-guide
- jwt-authentication
- pdpa-compliance

Include:
1. Registration with email verification
2. Login with JWT
3. Password reset
4. PDPA consent tracking
5. User profile management
```

### Example 2: API Development

```
Build a RESTful API for a blog platform using:
- nodejs-api
- prisma-guide
- error-handling
- validation
- api-documentation

Features:
- CRUD for posts
- Comments system
- User roles (author, editor, admin)
- Full OpenAPI documentation
```

### Example 3: E-commerce Cart

```
Implement a shopping cart system following:
- shopping-cart
- redis-caching
- stripe-integration
- inventory-management

Requirements:
- Guest and logged-in carts
- Real-time inventory checks
- Cart abandonment recovery
- Checkout with Stripe
```

---

## 🤝 Contributing

We welcome contributions! Here's how:

### Adding a New Skill

1. **Choose category** or create new one
2. **Create SKILL.md** following the template
3. **Submit PR** with description

### Skill Template

```markdown
# [Skill Name]

## Overview
Brief description of what this skill covers.

## [Section 1]
Content with code examples...

## [Section 2]
More content...

## Best Practices
- Practice 1
- Practice 2

Format: Markdown with code examples.
```

### Guidelines

- ✅ Production-ready patterns
- ✅ Real-world examples
- ✅ Security considerations
- ✅ Performance tips
- ✅ Testing strategies
- ❌ Avoid theoretical concepts only
- ❌ Include deprecated patterns

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Anthropic** - For Claude AI
- **Community Contributors** - For skill submissions
- **Open Source Projects** - For inspiration and patterns

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/AmnadTaowsoam/cerebraSkills/issues)
- **Discussions**: [GitHub Discussions](https://github.com/AmnadTaowsoam/cerebraSkills/discussions)
- **Email**: support@cerebratechai.com

---

## 🗺️ Roadmap

### Q1 2024
- [ ] Complete all 240 skills
- [ ] Add interactive skill selector
- [ ] Create video tutorials
- [ ] Build skill testing framework

### Q2 2024
- [ ] Community skill submissions
- [ ] Skill versioning system
- [ ] Integration with popular IDEs
- [ ] Multi-language skill translations

### Q3 2024
- [ ] AI-powered skill recommendations
- [ ] Skill dependency graph
- [ ] Automated skill updates
- [ ] Enterprise skill packs

---

## 📊 Statistics

- **Total Skills**: 473+
- **Categories**: 73
- **Languages**: TypeScript, Python, SQL, Dart, Solidity, Go
- **Frameworks**: 60+
- **Last Updated**: January 2026

---

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=AmnadTaowsoam/cerebraSkills&type=Date)](https://star-history.com/#AmnadTaowsoam/cerebraSkills&Date)

---

<div align="center">

**Made with ❤️ by [Cerebrate Chai](https://cerebratechai.com)**

[Website](https://cerebratechai.com) • [GitHub](https://github.com/AmnadTaowsoam) • [Twitter](https://twitter.com/cerebratechai)

</div>

<!-- SKILLS-START -->
## Skills Overview

**Total Skills:** 556


### 00. Meta Skills

| Skill | Description |
|-------|-------------|
| [architectural-reviews](00-meta-skills/architectural-reviews/SKILL.md) | Architecture Review: [Project Name] |
| [decision-records](00-meta-skills/decision-records/SKILL.md) | ADR-001: [Short Title] |
| [problem-framing](00-meta-skills/problem-framing/SKILL.md) | Untitled |
| [risk-assessment](00-meta-skills/risk-assessment/SKILL.md) | Risk Register: [Project Name] |
| [system-thinking](00-meta-skills/system-thinking/SKILL.md) | Untitled |
| [technical-debt-management](00-meta-skills/technical-debt-management/SKILL.md) | Install |

### 01. Foundations

| Skill | Description |
|-------|-------------|
| [api-design](01-foundations/api-design/SKILL.md) | Get all users (with pagination) |
| [code-review](01-foundations/code-review/SKILL.md) | BAD: Vague and unhelpful |
| [git-workflow](01-foundations/git-workflow/SKILL.md) | GOOD: Descriptive, lowercase, hyphen-separated |
| [python-standards](01-foundations/python-standards/SKILL.md) | ❌ Bad |
| [refactoring-strategies](01-foundations/refactoring-strategies/SKILL.md) | verify.sh - Run after each refactoring step |
| [typescript-standards](01-foundations/typescript-standards/SKILL.md) | Untitled |

### 02. Frontend

| Skill | Description |
|-------|-------------|
| [animation](02-frontend/animation/SKILL.md) | Animation Patterns in React |
| [error-boundaries-react](02-frontend/error-boundaries-react/SKILL.md) | Error Boundaries in React |
| [form-handling](02-frontend/form-handling/SKILL.md) | Form Handling with React Hook Form and Zod |
| [infinite-scroll](02-frontend/infinite-scroll/SKILL.md) | Infinite Scroll Patterns |
| [mui-material](02-frontend/mui-material/SKILL.md) | Material-UI (MUI) Best Practices |
| [multi-step-forms](02-frontend/multi-step-forms/SKILL.md) | Multi-Step Form Patterns |
| [nextjs-patterns](02-frontend/nextjs-patterns/SKILL.md) | Next.js 14+ App Router Patterns |
| [react-best-practices](02-frontend/react-best-practices/SKILL.md) | React Best Practices and Patterns |
| [shadcn-ui](02-frontend/shadcn-ui/SKILL.md) | shadcn/ui Component Patterns |
| [state-machines-xstate](02-frontend/state-machines-xstate/SKILL.md) | State Machines with XState |
| [state-management](02-frontend/state-management/SKILL.md) | State Management Patterns in React |
| [tailwind-patterns](02-frontend/tailwind-patterns/SKILL.md) | Tailwind CSS Patterns and Best Practices |

### 03. Backend Api

| Skill | Description |
|-------|-------------|
| [error-handling](03-backend-api/error-handling/SKILL.md) | Backend Error Handling Patterns |
| [express-rest](03-backend-api/express-rest/SKILL.md) | Express.js REST API Patterns |
| [fastapi-patterns](03-backend-api/fastapi-patterns/SKILL.md) | FastAPI Patterns and Best Practices |
| [fastify-rest-api](03-backend-api/fastify-rest-api/SKILL.md) | Fastify REST API Patterns |
| [graphql-best-practices](03-backend-api/graphql-best-practices/SKILL.md) | GraphQL Best Practices |
| [grpc-integration](03-backend-api/grpc-integration/SKILL.md) | gRPC Integration |
| [middleware](03-backend-api/middleware/SKILL.md) | Backend Middleware Patterns |
| [nodejs-api](03-backend-api/nodejs-api/SKILL.md) | Node.js REST API Patterns |
| [validation](03-backend-api/validation/SKILL.md) | API Request Validation |
| [websocket-patterns](03-backend-api/websocket-patterns/SKILL.md) | WebSocket Patterns |

### 04. Database

| Skill | Description |
|-------|-------------|
| [cache-invalidation](04-database/cache-invalidation/SKILL.md) | Cache Invalidation Strategies |
| [connection-pooling](04-database/connection-pooling/SKILL.md) | Connection Pooling |
| [database-locking](04-database/database-locking/SKILL.md) | Database Locking Strategies |
| [database-migrations](04-database/database-migrations/SKILL.md) | Database Migrations |
| [database-optimization](04-database/database-optimization/SKILL.md) | Database Optimization Techniques |
| [database-transactions](04-database/database-transactions/SKILL.md) | Database Transactions |
| [mongodb-patterns](04-database/mongodb-patterns/SKILL.md) | MongoDB Patterns and Best Practices |
| [prisma-guide](04-database/prisma-guide/SKILL.md) | Prisma ORM Guide |
| [redis-caching](04-database/redis-caching/SKILL.md) | Redis Caching Patterns |
| [timescaledb](04-database/timescaledb/SKILL.md) | TimescaleDB (Time-Series Database) Patterns |
| [vector-database](04-database/vector-database/SKILL.md) | Vector Database Patterns |

### 05. Ai Ml Core

| Skill | Description |
|-------|-------------|
| [data-augmentation](05-ai-ml-core/data-augmentation/SKILL.md) | Data Augmentation |
| [data-preprocessing](05-ai-ml-core/data-preprocessing/SKILL.md) | Data Preprocessing |
| [label-studio-setup](05-ai-ml-core/label-studio-setup/SKILL.md) | Label Studio Setup |
| [model-optimization](05-ai-ml-core/model-optimization/SKILL.md) | Model Optimization |
| [model-training](05-ai-ml-core/model-training/SKILL.md) | Model Training |
| [model-versioning](05-ai-ml-core/model-versioning/SKILL.md) | Model Versioning |
| [pytorch-deployment](05-ai-ml-core/pytorch-deployment/SKILL.md) | PyTorch Deployment |
| [yolo-integration](05-ai-ml-core/yolo-integration/SKILL.md) | YOLO Integration |

### 06. Ai Ml Production

| Skill | Description |
|-------|-------------|
| [agent-patterns](06-ai-ml-production/agent-patterns/SKILL.md) | AI Agent Patterns |
| [ai-observability](06-ai-ml-production/ai-observability/SKILL.md) | AI/ML Observability and Monitoring |
| [embedding-models](06-ai-ml-production/embedding-models/SKILL.md) | Embedding Models |
| [llm-function-calling](06-ai-ml-production/llm-function-calling/SKILL.md) | LLM Function Calling |
| [llm-guardrails](06-ai-ml-production/llm-guardrails/SKILL.md) | LLM Guardrails |
| [llm-integration](06-ai-ml-production/llm-integration/SKILL.md) | LLM Integration |
| [llm-local-deployment](06-ai-ml-production/llm-local-deployment/SKILL.md) | Local LLM Deployment |
| [prompt-engineering](06-ai-ml-production/prompt-engineering/SKILL.md) | Prompt Engineering |
| [rag-implementation](06-ai-ml-production/rag-implementation/SKILL.md) | RAG Implementation |
| [vector-search](06-ai-ml-production/vector-search/SKILL.md) | Vector Search |
| [vector-search-patterns](06-ai-ml-production/vector-search-patterns/SKILL.md) | Vector Search Patterns |

### 07. Document Processing

| Skill | Description |
|-------|-------------|
| [document-ingestion-pipeline](07-document-processing/document-ingestion-pipeline/SKILL.md) | Document Ingestion Pipeline |
| [document-parsing](07-document-processing/document-parsing/SKILL.md) | Document Parsing |
| [image-preprocessing](07-document-processing/image-preprocessing/SKILL.md) | Image Preprocessing |
| [ocr-paddleocr](07-document-processing/ocr-paddleocr/SKILL.md) | OCR with PaddleOCR |
| [ocr-tesseract](07-document-processing/ocr-tesseract/SKILL.md) | OCR with Tesseract |
| [pdf-processing](07-document-processing/pdf-processing/SKILL.md) | PDF Processing |
| [rag-architecture-patterns](07-document-processing/rag-architecture-patterns/SKILL.md) | RAG Architecture Patterns |
| [rag-chunking-metadata-strategy](07-document-processing/rag-chunking-metadata-strategy/SKILL.md) | RAG Chunking Metadata Strategy |
| [rag-citations-grounding](07-document-processing/rag-citations-grounding/SKILL.md) | RAG Citations Grounding |

### 08. Messaging Queue

| Skill | Description |
|-------|-------------|
| [kafka-streams](08-messaging-queue/kafka-streams/SKILL.md) | Kafka Streams |
| [mqtt-integration](08-messaging-queue/mqtt-integration/SKILL.md) | MQTT Integration |
| [queue-monitoring](08-messaging-queue/queue-monitoring/SKILL.md) | Queue Monitoring |
| [rabbitmq-patterns](08-messaging-queue/rabbitmq-patterns/SKILL.md) | RabbitMQ Patterns |
| [redis-queue](08-messaging-queue/redis-queue/SKILL.md) | Redis Queue |

### 09. Microservices

| Skill | Description |
|-------|-------------|
| [api-gateway](09-microservices/api-gateway/SKILL.md) | API Gateway |
| [circuit-breaker](09-microservices/circuit-breaker/SKILL.md) | Circuit Breaker Pattern |
| [cqrs-pattern](09-microservices/cqrs-pattern/SKILL.md) | CQRS Pattern (Command Query Responsibility Segregation) |
| [escrow-workflow](09-microservices/escrow-workflow/SKILL.md) | Escrow Workflow Patterns |
| [event-driven](09-microservices/event-driven/SKILL.md) | Event-Driven Architecture |
| [event-sourcing](09-microservices/event-sourcing/SKILL.md) | Event Sourcing |
| [saga-pattern](09-microservices/saga-pattern/SKILL.md) | Saga Pattern |
| [service-design](09-microservices/service-design/SKILL.md) | Service Design |
| [service-discovery](09-microservices/service-discovery/SKILL.md) | Service Discovery |
| [service-mesh](09-microservices/service-mesh/SKILL.md) | Service Mesh |

### 10. Authentication Authorization

| Skill | Description |
|-------|-------------|
| [api-key-management](10-authentication-authorization/api-key-management/SKILL.md) | API Key Management |
| [jwt-authentication](10-authentication-authorization/jwt-authentication/SKILL.md) | JWT Authentication |
| [oauth2-implementation](10-authentication-authorization/oauth2-implementation/SKILL.md) | OAuth 2.0 Implementation |
| [rbac-patterns](10-authentication-authorization/rbac-patterns/SKILL.md) | RBAC Patterns |
| [session-management](10-authentication-authorization/session-management/SKILL.md) | Session Management |

### 11. Billing Subscription

| Skill | Description |
|-------|-------------|
| [billing-cycles](11-billing-subscription/billing-cycles/SKILL.md) | Billing Cycles |
| [invoice-generation](11-billing-subscription/invoice-generation/SKILL.md) | Invoice Generation |
| [stripe-integration](11-billing-subscription/stripe-integration/SKILL.md) | Stripe Integration |
| [subscription-plans](11-billing-subscription/subscription-plans/SKILL.md) | Subscription Plans |
| [usage-metering](11-billing-subscription/usage-metering/SKILL.md) | Usage Metering |
| [webhook-handling](11-billing-subscription/webhook-handling/SKILL.md) | Webhook Handling |

### 12. Compliance Governance

| Skill | Description |
|-------|-------------|
| [audit-logging](12-compliance-governance/audit-logging/SKILL.md) | Audit Logging |
| [consent-management](12-compliance-governance/consent-management/SKILL.md) | Consent Management |
| [data-privacy](12-compliance-governance/data-privacy/SKILL.md) | Data Privacy |
| [data-retention](12-compliance-governance/data-retention/SKILL.md) | Data Retention |
| [gdpr-compliance](12-compliance-governance/gdpr-compliance/SKILL.md) | GDPR Compliance |
| [pdpa-compliance](12-compliance-governance/pdpa-compliance/SKILL.md) | PDPA Compliance |

### 13. File Storage

| Skill | Description |
|-------|-------------|
| [cdn-integration](13-file-storage/cdn-integration/SKILL.md) | CDN Integration |
| [file-compression](13-file-storage/file-compression/SKILL.md) | File Compression |
| [file-upload-handling](13-file-storage/file-upload-handling/SKILL.md) | File Upload Handling |
| [image-optimization](13-file-storage/image-optimization/SKILL.md) | Image Optimization |
| [multipart-upload](13-file-storage/multipart-upload/SKILL.md) | Multipart Upload |
| [s3-integration](13-file-storage/s3-integration/SKILL.md) | AWS S3 / MinIO Integration |

### 14. Monitoring Observability

| Skill | Description |
|-------|-------------|
| [distributed-tracing](14-monitoring-observability/distributed-tracing/SKILL.md) | Distributed Tracing |
| [elk-stack](14-monitoring-observability/elk-stack/SKILL.md) | ELK Stack |
| [error-tracking](14-monitoring-observability/error-tracking/SKILL.md) | Error Tracking |
| [grafana-dashboards](14-monitoring-observability/grafana-dashboards/SKILL.md) | Grafana Dashboards |
| [performance-monitoring](14-monitoring-observability/performance-monitoring/SKILL.md) | Performance Monitoring |
| [prometheus-metrics](14-monitoring-observability/prometheus-metrics/SKILL.md) | Prometheus Metrics |

### 15. Devops Infrastructure

| Skill | Description |
|-------|-------------|
| [ci-cd-github-actions](15-devops-infrastructure/ci-cd-github-actions/SKILL.md) | CI/CD GitHub Actions |
| [docker-compose](15-devops-infrastructure/docker-compose/SKILL.md) | Docker Compose |
| [docker-patterns](15-devops-infrastructure/docker-patterns/SKILL.md) | Docker Patterns |
| [gitops-argocd](15-devops-infrastructure/gitops-argocd/SKILL.md) | GitOps with ArgoCD |
| [helm-charts](15-devops-infrastructure/helm-charts/SKILL.md) | Helm Charts |
| [kubernetes-deployment](15-devops-infrastructure/kubernetes-deployment/SKILL.md) | Kubernetes Deployment |
| [load-balancing](15-devops-infrastructure/load-balancing/SKILL.md) | Load Balancing Strategies |
| [multi-cloud-patterns](15-devops-infrastructure/multi-cloud-patterns/SKILL.md) | Multi-Cloud Patterns |
| [secrets-management](15-devops-infrastructure/secrets-management/SKILL.md) | Secrets Management |
| [service-orchestration](15-devops-infrastructure/service-orchestration/SKILL.md) | Service Orchestration |
| [terraform-infrastructure](15-devops-infrastructure/terraform-infrastructure/SKILL.md) | Terraform Infrastructure |

### 16. Testing

| Skill | Description |
|-------|-------------|
| [contract-testing-pact](16-testing/contract-testing-pact/SKILL.md) | Contract Testing with Pact |
| [e2e-playwright](16-testing/e2e-playwright/SKILL.md) | E2E Testing with Playwright |
| [event-driven-testing](16-testing/event-driven-testing/SKILL.md) | Event-Driven Testing |
| [integration-testing](16-testing/integration-testing/SKILL.md) | Integration Testing |
| [jest-patterns](16-testing/jest-patterns/SKILL.md) | Jest Patterns |
| [load-testing](16-testing/load-testing/SKILL.md) | Load Testing |
| [ml-model-testing](16-testing/ml-model-testing/SKILL.md) | ML Model Testing |
| [pytest-patterns](16-testing/pytest-patterns/SKILL.md) | Pytest Patterns |
| [test-data-factory](16-testing/test-data-factory/SKILL.md) | Test Data Factory |
| [test-driven-development-agentic](16-testing/test-driven-development-agentic/SKILL.md) | Test-Driven Development for Agents |

### 17. Domain Specific

| Skill | Description |
|-------|-------------|
| [analytics-tracking](17-domain-specific/analytics-tracking/SKILL.md) | Analytics and Event Tracking |
| [api-versioning](17-domain-specific/api-versioning/SKILL.md) | API Versioning |
| [api-versioning-strategies](17-domain-specific/api-versioning-strategies/SKILL.md) | API Versioning Strategies |
| [feature-flags](17-domain-specific/feature-flags/SKILL.md) | Feature Flags |
| [multi-tenancy](17-domain-specific/multi-tenancy/SKILL.md) | Multi-Tenancy Architecture |
| [multi-tenancy-advanced](17-domain-specific/multi-tenancy-advanced/SKILL.md) | Multi-Tenancy Advanced Patterns |
| [notification-system](17-domain-specific/notification-system/SKILL.md) | Notification System |
| [qr-code-features](17-domain-specific/qr-code-features/SKILL.md) | QR Code Features |
| [rate-limiting](17-domain-specific/rate-limiting/SKILL.md) | Rate Limiting |
| [thai-cultural-events](17-domain-specific/thai-cultural-events/SKILL.md) | Thai Cultural Event Planning |

### 18. Project Management

| Skill | Description |
|-------|-------------|
| [agile-scrum](18-project-management/agile-scrum/SKILL.md) | Agile Scrum |
| [estimation-techniques](18-project-management/estimation-techniques/SKILL.md) | Estimation Techniques |
| [project-planning](18-project-management/project-planning/SKILL.md) | Project Planning |
| [requirement-analysis](18-project-management/requirement-analysis/SKILL.md) | Requirement Analysis |
| [risk-management](18-project-management/risk-management/SKILL.md) | Risk Management |
| [technical-specifications](18-project-management/technical-specifications/SKILL.md) | Technical Specifications |
| [user-stories](18-project-management/user-stories/SKILL.md) | User Stories |

### 19. Seo Optimization

| Skill | Description |
|-------|-------------|
| [core-web-vitals](19-seo-optimization/core-web-vitals/SKILL.md) | Core Web Vitals |
| [meta-tags](19-seo-optimization/meta-tags/SKILL.md) | Meta Tags |
| [nextjs-seo](19-seo-optimization/nextjs-seo/SKILL.md) | Next.js SEO |
| [page-speed](19-seo-optimization/page-speed/SKILL.md) | Page Speed Optimization |
| [sitemap-robots](19-seo-optimization/sitemap-robots/SKILL.md) | Sitemap and Robots.txt Management |
| [structured-data](19-seo-optimization/structured-data/SKILL.md) | Structured Data (Schema.org) |
| [technical-seo](19-seo-optimization/technical-seo/SKILL.md) | Technical SEO |

### 20. Ai Integration

| Skill | Description |
|-------|-------------|
| [ai-agents](20-ai-integration/ai-agents/SKILL.md) | AI Agents |
| [ai-search](20-ai-integration/ai-search/SKILL.md) | AI Search |
| [chatbot-integration](20-ai-integration/chatbot-integration/SKILL.md) | Chatbot Integration |
| [conversational-ui](20-ai-integration/conversational-ui/SKILL.md) | Conversational UI |
| [line-platform-integration](20-ai-integration/line-platform-integration/SKILL.md) | LINE Platform Integration |
| [llm-txt-protocol](20-ai-integration/llm-txt-protocol/SKILL.md) | LLM Text Protocol |

### 21. Documentation

| Skill | Description |
|-------|-------------|
| [api-documentation](21-documentation/api-documentation/SKILL.md) | API Documentation |
| [changelog-management](21-documentation/changelog-management/SKILL.md) | Changelog Management |
| [code-commentary-standards](21-documentation/code-commentary-standards/SKILL.md) | Code Commentary Standards |
| [runbooks](21-documentation/runbooks/SKILL.md) | Operational Runbooks |
| [system-architecture-docs](21-documentation/system-architecture-docs/SKILL.md) | System Architecture Documentation |
| [technical-writing](21-documentation/technical-writing/SKILL.md) | Technical Writing |
| [user-guides](21-documentation/user-guides/SKILL.md) | User Guides |

### 22. Ux Ui Design

| Skill | Description |
|-------|-------------|
| [accessibility](22-ux-ui-design/accessibility/SKILL.md) | Accessibility (a11y) |
| [design-handoff](22-ux-ui-design/design-handoff/SKILL.md) | Design Handoff |
| [design-systems](22-ux-ui-design/design-systems/SKILL.md) | Design Systems |
| [responsive-design](22-ux-ui-design/responsive-design/SKILL.md) | Responsive Design |
| [thai-ux-patterns](22-ux-ui-design/thai-ux-patterns/SKILL.md) | Thai UI/UX Patterns |
| [user-research](22-ux-ui-design/user-research/SKILL.md) | User Research |
| [wireframing](22-ux-ui-design/wireframing/SKILL.md) | Wireframing |

### 23. Business Analytics

| Skill | Description |
|-------|-------------|
| [ab-testing-analysis](23-business-analytics/ab-testing-analysis/SKILL.md) | A/B Testing Analysis |
| [business-intelligence](23-business-analytics/business-intelligence/SKILL.md) | Business Intelligence |
| [cohort-analysis](23-business-analytics/cohort-analysis/SKILL.md) | Cohort Analysis |
| [conversion-optimization](23-business-analytics/conversion-optimization/SKILL.md) | Conversion Optimization (CRO) |
| [dashboard-design](23-business-analytics/dashboard-design/SKILL.md) | Dashboard Design |
| [data-visualization](23-business-analytics/data-visualization/SKILL.md) | Data Visualization |
| [funnel-analysis](23-business-analytics/funnel-analysis/SKILL.md) | Funnel Analysis |
| [kpi-metrics](23-business-analytics/kpi-metrics/SKILL.md) | KPI (Key Performance Indicator) Metrics |
| [sql-for-analytics](23-business-analytics/sql-for-analytics/SKILL.md) | SQL for Analytics |

### 24. Security Practices

| Skill | Description |
|-------|-------------|
| [incident-response](24-security-practices/incident-response/SKILL.md) | Incident Response |
| [owasp-top-10](24-security-practices/owasp-top-10/SKILL.md) | OWASP Top 10 |
| [penetration-testing](24-security-practices/penetration-testing/SKILL.md) | Penetration Testing |
| [secrets-management](24-security-practices/secrets-management/SKILL.md) | Secrets Management |
| [secure-coding](24-security-practices/secure-coding/SKILL.md) | Secure Coding |
| [security-audit](24-security-practices/security-audit/SKILL.md) | Security Audit |
| [vulnerability-management](24-security-practices/vulnerability-management/SKILL.md) | Vulnerability Management |

### 25. Internationalization

| Skill | Description |
|-------|-------------|
| [currency-timezone](25-internationalization/currency-timezone/SKILL.md) | Currency and Timezone |
| [i18n-setup](25-internationalization/i18n-setup/SKILL.md) | i18n (Internationalization) Setup |
| [localization](25-internationalization/localization/SKILL.md) | Localization (l10n) |
| [multi-language](25-internationalization/multi-language/SKILL.md) | Multi-language Support |
| [rtl-support](25-internationalization/rtl-support/SKILL.md) | RTL (Right-to-Left) Support |

### 26. Deployment Strategies

| Skill | Description |
|-------|-------------|
| [blue-green-deployment](26-deployment-strategies/blue-green-deployment/SKILL.md) | Blue-Green Deployment |
| [canary-deployment](26-deployment-strategies/canary-deployment/SKILL.md) | Canary Deployment |
| [feature-toggles](26-deployment-strategies/feature-toggles/SKILL.md) | Feature Toggles (Feature Flags) |
| [rollback-strategies](26-deployment-strategies/rollback-strategies/SKILL.md) | Rollback Strategies |
| [rolling-deployment](26-deployment-strategies/rolling-deployment/SKILL.md) | Rolling Deployment |

### 27. Team Collaboration

| Skill | Description |
|-------|-------------|
| [code-review-culture](27-team-collaboration/code-review-culture/SKILL.md) | Code Review Culture |
| [knowledge-sharing](27-team-collaboration/knowledge-sharing/SKILL.md) | Knowledge Sharing |
| [onboarding](27-team-collaboration/onboarding/SKILL.md) | Developer Onboarding |
| [pair-programming](27-team-collaboration/pair-programming/SKILL.md) | Pair Programming |
| [remote-work](27-team-collaboration/remote-work/SKILL.md) | Remote Work Best Practices |

### 28. Marketing Integration

| Skill | Description |
|-------|-------------|
| [ab-testing](28-marketing-integration/ab-testing/SKILL.md) | A/B Testing Implementation |
| [campaign-management](28-marketing-integration/campaign-management/SKILL.md) | Marketing Campaign Management |
| [email-marketing](28-marketing-integration/email-marketing/SKILL.md) | Email Marketing Integration |
| [marketing-automation](28-marketing-integration/marketing-automation/SKILL.md) | Marketing Automation |
| [social-media-integration](28-marketing-integration/social-media-integration/SKILL.md) | Social Media API Integration |
| [utm-tracking](28-marketing-integration/utm-tracking/SKILL.md) | UTM Tracking and Campaign Tracking |

### 29. Customer Support

| Skill | Description |
|-------|-------------|
| [customer-feedback](29-customer-support/customer-feedback/SKILL.md) | Customer Feedback Collection and Management |
| [helpdesk-integration](29-customer-support/helpdesk-integration/SKILL.md) | Helpdesk System Integration |
| [knowledge-base](29-customer-support/knowledge-base/SKILL.md) | Knowledge Base Implementation |
| [live-chat](29-customer-support/live-chat/SKILL.md) | Live Chat Implementation |
| [support-analytics](29-customer-support/support-analytics/SKILL.md) | Customer Support Analytics |
| [ticketing-system](29-customer-support/ticketing-system/SKILL.md) | Ticketing System |

### 30. Ecommerce

| Skill | Description |
|-------|-------------|
| [discount-promotions](30-ecommerce/discount-promotions/SKILL.md) | Discount and Promotion Engine |
| [inventory-management](30-ecommerce/inventory-management/SKILL.md) | Inventory Management |
| [order-fulfillment](30-ecommerce/order-fulfillment/SKILL.md) | Order Fulfillment Workflow |
| [order-management](30-ecommerce/order-management/SKILL.md) | Order Management System (OMS) |
| [payment-gateways](30-ecommerce/payment-gateways/SKILL.md) | Payment Gateway Integration |
| [product-catalog](30-ecommerce/product-catalog/SKILL.md) | Product Catalog Management |
| [shipping-integration](30-ecommerce/shipping-integration/SKILL.md) | Shipping Carrier Integration |
| [shopping-cart](30-ecommerce/shopping-cart/SKILL.md) | Shopping Cart Implementation |

### 31. Mobile Development

| Skill | Description |
|-------|-------------|
| [app-distribution](31-mobile-development/app-distribution/SKILL.md) | Mobile App Distribution and Deployment |
| [deep-linking](31-mobile-development/deep-linking/SKILL.md) | Deep Linking and Universal Links |
| [flutter-patterns](31-mobile-development/flutter-patterns/SKILL.md) | Flutter Development Patterns |
| [mobile-ci-cd](31-mobile-development/mobile-ci-cd/SKILL.md) | Mobile CI/CD Pipelines |
| [offline-mode](31-mobile-development/offline-mode/SKILL.md) | Offline-First Mobile App Patterns |
| [push-notifications](31-mobile-development/push-notifications/SKILL.md) | Mobile Push Notifications |
| [react-native-patterns](31-mobile-development/react-native-patterns/SKILL.md) | React Native Development Patterns |

### 32. Crm Integration

| Skill | Description |
|-------|-------------|
| [contact-management](32-crm-integration/contact-management/SKILL.md) | Contact Management |
| [custom-crm](32-crm-integration/custom-crm/SKILL.md) | Custom CRM Development |
| [hubspot-integration](32-crm-integration/hubspot-integration/SKILL.md) | HubSpot Integration |
| [lead-management](32-crm-integration/lead-management/SKILL.md) | Lead Management |
| [sales-pipeline](32-crm-integration/sales-pipeline/SKILL.md) | Sales Pipeline |
| [salesforce-integration](32-crm-integration/salesforce-integration/SKILL.md) | Salesforce Integration |

### 33. Content Management

| Skill | Description |
|-------|-------------|
| [content-versioning](33-content-management/content-versioning/SKILL.md) | Content Versioning |
| [contentful-integration](33-content-management/contentful-integration/SKILL.md) | Contentful Integration |
| [headless-cms](33-content-management/headless-cms/SKILL.md) | Headless CMS Integration |
| [media-library](33-content-management/media-library/SKILL.md) | Media Library |
| [strapi-integration](33-content-management/strapi-integration/SKILL.md) | Strapi Integration |
| [wordpress-api](33-content-management/wordpress-api/SKILL.md) | WordPress API |

### 34. Real Time Features

| Skill | Description |
|-------|-------------|
| [collaborative-editing](34-real-time-features/collaborative-editing/SKILL.md) | Collaborative Editing |
| [live-notifications](34-real-time-features/live-notifications/SKILL.md) | Live Notifications |
| [presence-detection](34-real-time-features/presence-detection/SKILL.md) | Presence Detection |
| [real-time-dashboard](34-real-time-features/real-time-dashboard/SKILL.md) | Real-time Dashboard |
| [server-sent-events](34-real-time-features/server-sent-events/SKILL.md) | Server-Sent Events (SSE) |
| [websocket-patterns](34-real-time-features/websocket-patterns/SKILL.md) | WebSocket Patterns |

### 35. Blockchain Web3

| Skill | Description |
|-------|-------------|
| [blockchain-authentication](35-blockchain-web3/blockchain-authentication/SKILL.md) | Blockchain Authentication |
| [cryptocurrency-payment](35-blockchain-web3/cryptocurrency-payment/SKILL.md) | Cryptocurrency Payment |
| [nft-integration](35-blockchain-web3/nft-integration/SKILL.md) | NFT Integration |
| [smart-contracts](35-blockchain-web3/smart-contracts/SKILL.md) | Smart Contracts Integration |
| [wallet-connection](35-blockchain-web3/wallet-connection/SKILL.md) | Wallet Connection |
| [web3-integration](35-blockchain-web3/web3-integration/SKILL.md) | Web3 Integration |

### 36. Iot Integration

| Skill | Description |
|-------|-------------|
| [device-management](36-iot-integration/device-management/SKILL.md) | Device Management |
| [edge-computing](36-iot-integration/edge-computing/SKILL.md) | Edge Computing |
| [iot-protocols](36-iot-integration/iot-protocols/SKILL.md) | IoT Protocols |
| [iot-security](36-iot-integration/iot-security/SKILL.md) | IoT Security |
| [real-time-monitoring](36-iot-integration/real-time-monitoring/SKILL.md) | Real-time Monitoring |
| [sensor-data-processing](36-iot-integration/sensor-data-processing/SKILL.md) | Sensor Data Processing |

### 37. Video Streaming

| Skill | Description |
|-------|-------------|
| [adaptive-bitrate](37-video-streaming/adaptive-bitrate/SKILL.md) | Adaptive Bitrate Streaming |
| [cdn-delivery](37-video-streaming/cdn-delivery/SKILL.md) | CDN for Video Delivery |
| [live-streaming](37-video-streaming/live-streaming/SKILL.md) | Live Streaming |
| [video-analytics](37-video-streaming/video-analytics/SKILL.md) | Video Analytics |
| [video-transcoding](37-video-streaming/video-transcoding/SKILL.md) | Video Transcoding |
| [video-upload-processing](37-video-streaming/video-upload-processing/SKILL.md) | Video Upload & Processing |

### 38. Gaming Features

| Skill | Description |
|-------|-------------|
| [achievements](38-gaming-features/achievements/SKILL.md) | Achievements System |
| [game-analytics](38-gaming-features/game-analytics/SKILL.md) | Game Analytics |
| [in-game-purchases](38-gaming-features/in-game-purchases/SKILL.md) | In-Game Purchases |
| [leaderboards](38-gaming-features/leaderboards/SKILL.md) | Leaderboards |
| [matchmaking](38-gaming-features/matchmaking/SKILL.md) | Matchmaking |
| [real-time-multiplayer](38-gaming-features/real-time-multiplayer/SKILL.md) | Real-time Multiplayer |

### 39. Data Science Ml

| Skill | Description |
|-------|-------------|
| [ab-testing-ml](39-data-science-ml/ab-testing-ml/SKILL.md) | A/B Testing for ML |
| [automl](39-data-science-ml/automl/SKILL.md) | AutoML |
| [data-pipeline](39-data-science-ml/data-pipeline/SKILL.md) | Data Pipeline |
| [feature-engineering](39-data-science-ml/feature-engineering/SKILL.md) | Feature Engineering |
| [ml-serving](39-data-science-ml/ml-serving/SKILL.md) | ML Model Serving |
| [model-experiments](39-data-science-ml/model-experiments/SKILL.md) | ML Experiment Tracking |

### 40. System Resilience

| Skill | Description |
|-------|-------------|
| [bulkhead-patterns](40-system-resilience/bulkhead-patterns/SKILL.md) | Bulkhead Patterns |
| [chaos-engineering](40-system-resilience/chaos-engineering/SKILL.md) | Chaos Engineering |
| [disaster-recovery](40-system-resilience/disaster-recovery/SKILL.md) | Untitled |
| [failure-modes](40-system-resilience/failure-modes/SKILL.md) | Failure Modes Analysis |
| [graceful-degradation](40-system-resilience/graceful-degradation/SKILL.md) | Untitled |
| [idempotency-and-dedup](40-system-resilience/idempotency-and-dedup/SKILL.md) | Untitled |
| [postmortem-analysis](40-system-resilience/postmortem-analysis/SKILL.md) | Postmortem Analysis (Incident Review) |
| [retry-timeout-strategies](40-system-resilience/retry-timeout-strategies/SKILL.md) | Retry, Timeout & Backoff Strategies |

### 41. Incident Management

| Skill | Description |
|-------|-------------|
| [communication-templates](41-incident-management/communication-templates/SKILL.md) | Communication Templates |
| [escalation-and-ownership](41-incident-management/escalation-and-ownership/SKILL.md) | Escalation and Ownership |
| [escalation-paths](41-incident-management/escalation-paths/SKILL.md) | Escalation Paths |
| [incident-retrospective](41-incident-management/incident-retrospective/SKILL.md) | Untitled |
| [incident-severity-levels](41-incident-management/incident-severity-levels/SKILL.md) | Incident Severity Levels |
| [incident-triage](41-incident-management/incident-triage/SKILL.md) | Incident Triage |
| [oncall-playbooks](41-incident-management/oncall-playbooks/SKILL.md) | On-Call Playbooks and Runbooks |
| [runbook-templates](41-incident-management/runbook-templates/SKILL.md) | Runbook Templates |
| [severity-levels](41-incident-management/severity-levels/SKILL.md) | Incident Severity Levels |
| [stakeholder-communication](41-incident-management/stakeholder-communication/SKILL.md) | Stakeholder Communication During Incidents |
| [triage-workflow](41-incident-management/triage-workflow/SKILL.md) | Triage Workflow |

### 42. Cost Engineering

| Skill | Description |
|-------|-------------|
| [autoscaling-and-rightsizing](42-cost-engineering/autoscaling-and-rightsizing/SKILL.md) | Autoscaling and Right-Sizing |
| [budget-guardrails](42-cost-engineering/budget-guardrails/SKILL.md) | Budget Guardrails and Cost Controls |
| [cloud-cost-models](42-cost-engineering/cloud-cost-models/SKILL.md) | Cloud Cost Models and Pricing |
| [cost-guardrails](42-cost-engineering/cost-guardrails/SKILL.md) | Cost Guardrails |
| [cost-modeling](42-cost-engineering/cost-modeling/SKILL.md) | Cost Modeling |
| [cost-observability](42-cost-engineering/cost-observability/SKILL.md) | Cost Observability and Monitoring |
| [infra-sizing](42-cost-engineering/infra-sizing/SKILL.md) | Infrastructure Sizing and Capacity Planning |
| [llm-cost-optimization](42-cost-engineering/llm-cost-optimization/SKILL.md) | LLM and AI Cost Optimization |
| [llm-token-optimization](42-cost-engineering/llm-token-optimization/SKILL.md) | LLM Token Optimization |
| [pricing-and-usage-meters](42-cost-engineering/pricing-and-usage-meters/SKILL.md) | Pricing and Usage Meters |
| [storage-egress-optimization](42-cost-engineering/storage-egress-optimization/SKILL.md) | Storage and Egress Optimization |
| [usage-based-pricing](42-cost-engineering/usage-based-pricing/SKILL.md) | Usage-Based Pricing (Consumption Billing) |

### 43. Data Reliability

| Skill | Description |
|-------|-------------|
| [data-contracts](43-data-reliability/data-contracts/SKILL.md) | Data Contracts |
| [data-incident-response](43-data-reliability/data-incident-response/SKILL.md) | Data Incident Response |
| [data-lineage](43-data-reliability/data-lineage/SKILL.md) | Data Lineage |
| [data-quality-checks](43-data-reliability/data-quality-checks/SKILL.md) | Data Quality Checks and Validation |
| [data-quality-monitoring](43-data-reliability/data-quality-monitoring/SKILL.md) | Data Quality Monitoring |
| [data-quality-rules](43-data-reliability/data-quality-rules/SKILL.md) | Data Quality Rules |
| [data-retention-archiving](43-data-reliability/data-retention-archiving/SKILL.md) | Data Retention and Archiving |
| [data-validation-rules](43-data-reliability/data-validation-rules/SKILL.md) | Data Validation Rules |
| [database-health-monitoring](43-data-reliability/database-health-monitoring/SKILL.md) | Database Health Monitoring |
| [freshness-latency](43-data-reliability/freshness-latency/SKILL.md) | Data Freshness and Latency |
| [freshness-latency-slos](43-data-reliability/freshness-latency-slos/SKILL.md) | Freshness Latency SLOs |
| [lineage-and-provenance](43-data-reliability/lineage-and-provenance/SKILL.md) | Lineage and Provenance |
| [schema-drift](43-data-reliability/schema-drift/SKILL.md) | Schema Drift Detection |
| [schema-drift-handling](43-data-reliability/schema-drift-handling/SKILL.md) | Schema Drift Handling |
| [schema-management](43-data-reliability/schema-management/SKILL.md) | Schema Management |

### 44. Ai Governance

| Skill | Description |
|-------|-------------|
| [ai-data-privacy](44-ai-governance/ai-data-privacy/SKILL.md) | AI Data Privacy |
| [ai-ethics-compliance](44-ai-governance/ai-ethics-compliance/SKILL.md) | AI Ethics and Compliance |
| [ai-risk-assessment](44-ai-governance/ai-risk-assessment/SKILL.md) | AI Risk Assessment |
| [auditability](44-ai-governance/auditability/SKILL.md) | AI Auditability |
| [confidence-scoring](44-ai-governance/confidence-scoring/SKILL.md) | Confidence Scoring |
| [explainability](44-ai-governance/explainability/SKILL.md) | Explainability |
| [human-approval-flows](44-ai-governance/human-approval-flows/SKILL.md) | Human-in-the-Loop (HITL) Workflows |
| [model-bias-fairness](44-ai-governance/model-bias-fairness/SKILL.md) | Model Bias and Fairness |
| [model-explainability](44-ai-governance/model-explainability/SKILL.md) | Model Explainability (XAI) |
| [model-registry](44-ai-governance/model-registry/SKILL.md) | AI Model Registry |
| [model-risk-management](44-ai-governance/model-risk-management/SKILL.md) | Model Risk Management (MRM) |
| [override-mechanisms](44-ai-governance/override-mechanisms/SKILL.md) | Override Mechanisms |

### 45. Developer Experience

| Skill | Description |
|-------|-------------|
| [code-review-standards](45-developer-experience/code-review-standards/SKILL.md) | Code Review Standards |
| [commit-conventions](45-developer-experience/commit-conventions/SKILL.md) | Commit Conventions |
| [debugging-tools](45-developer-experience/debugging-tools/SKILL.md) | Debugging Tools and Techniques |
| [dev-environment-setup](45-developer-experience/dev-environment-setup/SKILL.md) | Development Environment Setup |
| [env-diagnosis](45-developer-experience/env-diagnosis/SKILL.md) | Environment Diagnosis & Repair |
| [hot-reload-fast-feedback](45-developer-experience/hot-reload-fast-feedback/SKILL.md) | Hot Reload and Fast Feedback Loops |
| [lint-format-typecheck](45-developer-experience/lint-format-typecheck/SKILL.md) | Lint, Format, and Type Check |
| [local-dev-standard](45-developer-experience/local-dev-standard/SKILL.md) | Local Development Standard |
| [onboarding-docs](45-developer-experience/onboarding-docs/SKILL.md) | Developer Onboarding Documentation |
| [release-workflow](45-developer-experience/release-workflow/SKILL.md) | Release Workflow |
| [repo-automation-scripts](45-developer-experience/repo-automation-scripts/SKILL.md) | Repository Automation Scripts |

### 46. Data Classification

| Skill | Description |
|-------|-------------|
| [access-audit-and-reviews](46-data-classification/access-audit-and-reviews/SKILL.md) | Access Audit and Reviews |
| [logging-redaction](46-data-classification/logging-redaction/SKILL.md) | Logging Redaction |
| [pii-detection](46-data-classification/pii-detection/SKILL.md) | PII Detection |
| [retention-and-deletion](46-data-classification/retention-and-deletion/SKILL.md) | Data Retention and Deletion |

### 47. Performance Engineering

| Skill | Description |
|-------|-------------|
| [caching-strategies](47-performance-engineering/caching-strategies/SKILL.md) | Caching Strategies |
| [concurrency-and-throughput](47-performance-engineering/concurrency-and-throughput/SKILL.md) | Concurrency and Throughput |
| [db-query-optimization](47-performance-engineering/db-query-optimization/SKILL.md) | Database Query Optimization |
| [profiling-node-python](47-performance-engineering/profiling-node-python/SKILL.md) | Profiling (Node.js & Python) |
| [sla-slo-slis](47-performance-engineering/sla-slo-slis/SKILL.md) | SLA, SLO, and SLIs |

### 48. Product Discovery

| Skill | Description |
|-------|-------------|
| [experiment-design](48-product-discovery/experiment-design/SKILL.md) | Experiment Design |
| [hypothesis-writing](48-product-discovery/hypothesis-writing/SKILL.md) | Hypothesis Writing |
| [mvp-scope-control](48-product-discovery/mvp-scope-control/SKILL.md) | Untitled |
| [user-interviews](48-product-discovery/user-interviews/SKILL.md) | User Interviews |
| [validation-metrics](48-product-discovery/validation-metrics/SKILL.md) | Validation Metrics |

### 49. Portfolio Management

| Skill | Description |
|-------|-------------|
| [cross-team-interfaces](49-portfolio-management/cross-team-interfaces/SKILL.md) | Cross-Team Interfaces |
| [delivery-governance](49-portfolio-management/delivery-governance/SKILL.md) | Delivery Governance |
| [dependency-mapping](49-portfolio-management/dependency-mapping/SKILL.md) | Dependency Mapping |
| [roadmap-planning](49-portfolio-management/roadmap-planning/SKILL.md) | Roadmap Planning |

### 50. Enterprise Integrations

| Skill | Description |
|-------|-------------|
| [enterprise-rbac-models](50-enterprise-integrations/enterprise-rbac-models/SKILL.md) | Enterprise RBAC Models |
| [scim-provisioning](50-enterprise-integrations/scim-provisioning/SKILL.md) | SCIM Provisioning |
| [security-questionnaires](50-enterprise-integrations/security-questionnaires/SKILL.md) | Security Questionnaires |
| [sso-saml-oidc](50-enterprise-integrations/sso-saml-oidc/SKILL.md) | SSO (SAML & OIDC) |
| [vendor-onboarding](50-enterprise-integrations/vendor-onboarding/SKILL.md) | Vendor Onboarding |

### 51. Contracts Governance

| Skill | Description |
|-------|-------------|
| [backward-compat-rules](51-contracts-governance/backward-compat-rules/SKILL.md) | Backward Compatibility Rules |
| [contract-testing](51-contracts-governance/contract-testing/SKILL.md) | Contract Testing |
| [deprecation-notices](51-contracts-governance/deprecation-notices/SKILL.md) | Deprecation Notices |
| [event-schema-registry](51-contracts-governance/event-schema-registry/SKILL.md) | Event Schema Registry |
| [openapi-governance](51-contracts-governance/openapi-governance/SKILL.md) | OpenAPI Governance |

### 52. Ai Evaluation

| Skill | Description |
|-------|-------------|
| [ground-truth-management](52-ai-evaluation/ground-truth-management/SKILL.md) | Ground Truth Management |
| [llm-judge-patterns](52-ai-evaluation/llm-judge-patterns/SKILL.md) | LLM Judge Patterns |
| [offline-vs-online-eval](52-ai-evaluation/offline-vs-online-eval/SKILL.md) | Offline vs Online Evaluation |
| [rag-evaluation](52-ai-evaluation/rag-evaluation/SKILL.md) | RAG Evaluation |
| [regression-benchmarks](52-ai-evaluation/regression-benchmarks/SKILL.md) | Regression Benchmarks |

### 53. Data Engineering

| Skill | Description |
|-------|-------------|
| [data-quality-checks](53-data-engineering/data-quality-checks/SKILL.md) | Data Quality Checks |
| [dbt-patterns](53-data-engineering/dbt-patterns/SKILL.md) | dbt Patterns |
| [elt-modeling](53-data-engineering/elt-modeling/SKILL.md) | ELT Modeling |
| [kafka-streaming](53-data-engineering/kafka-streaming/SKILL.md) | Kafka Streaming |
| [lakehouse-patterns](53-data-engineering/lakehouse-patterns/SKILL.md) | Lakehouse Patterns |

### 54. Agentops

| Skill | Description |
|-------|-------------|
| [audit-trails-for-agents](54-agentops/audit-trails-for-agents/SKILL.md) | Audit Trails for Agents |
| [prompt-versioning](54-agentops/prompt-versioning/SKILL.md) | Prompt Versioning |
| [rollout-and-kill-switch](54-agentops/rollout-and-kill-switch/SKILL.md) | Rollout and Kill Switch |
| [sandboxing](54-agentops/sandboxing/SKILL.md) | Sandboxing |
| [tool-creation-patterns](54-agentops/tool-creation-patterns/SKILL.md) | MCP Tool Creation Patterns |
| [tool-permission-model](54-agentops/tool-permission-model/SKILL.md) | Tool Permission Model |

### 55. Ux Writing

| Skill | Description |
|-------|-------------|
| [error-messages](55-ux-writing/error-messages/SKILL.md) | Error Messages |
| [microcopy](55-ux-writing/microcopy/SKILL.md) | Microcopy |
| [onboarding-flows](55-ux-writing/onboarding-flows/SKILL.md) | Onboarding Flows |
| [trust-pages-structure](55-ux-writing/trust-pages-structure/SKILL.md) | Trust Pages Structure |

### 56. Requirements Intake

| Skill | Description |
|-------|-------------|
| [acceptance-criteria](56-requirements-intake/acceptance-criteria/SKILL.md) | Acceptance Criteria |
| [constraints-and-assumptions](56-requirements-intake/constraints-and-assumptions/SKILL.md) | Constraints and Assumptions |
| [discovery-questions](56-requirements-intake/discovery-questions/SKILL.md) | Discovery Questions in Requirements Gathering |
| [requirement-to-scope](56-requirements-intake/requirement-to-scope/SKILL.md) | Requirement to Scope (In-Scope vs Out-of-Scope) |
| [risk-and-dependencies](56-requirements-intake/risk-and-dependencies/SKILL.md) | Risk and Dependencies |

### 57. Skill Orchestration

| Skill | Description |
|-------|-------------|
| [autonomous-gap-detector](57-skill-orchestration/autonomous-gap-detector/SKILL.md) | Autonomous Gap Detector Protocol |
| [baseline-policy](57-skill-orchestration/baseline-policy/SKILL.md) | Baseline Policy |
| [output-templates](57-skill-orchestration/output-templates/SKILL.md) | Output Templates |
| [routing-rules](57-skill-orchestration/routing-rules/SKILL.md) | Routing Rules |
| [scoring-and-prioritization](57-skill-orchestration/scoring-and-prioritization/SKILL.md) | Scoring and Prioritization |
| [skill-improvement-loop](57-skill-orchestration/skill-improvement-loop/SKILL.md) | Skill Improvement Loop - Auto-Update & Gap Detection |

### 58. Investment Estimation

| Skill | Description |
|-------|-------------|
| [discovery-for-estimation](58-investment-estimation/discovery-for-estimation/SKILL.md) | Untitled |
| [effort-sizing](58-investment-estimation/effort-sizing/SKILL.md) | Untitled |
| [payback-analysis](58-investment-estimation/payback-analysis/SKILL.md) | Untitled |
| [pricing-strategy](58-investment-estimation/pricing-strategy/SKILL.md) | Untitled |
| [proposal-pack](58-investment-estimation/proposal-pack/SKILL.md) | Untitled |
| [roi-modeling](58-investment-estimation/roi-modeling/SKILL.md) | Untitled |
| [sensitivity-analysis](58-investment-estimation/sensitivity-analysis/SKILL.md) | Untitled |

### 59. Architecture Decision

| Skill | Description |
|-------|-------------|
| [adr-templates](59-architecture-decision/adr-templates/SKILL.md) | Architecture Decision Records (ADR) |
| [architecture-review](59-architecture-decision/architecture-review/SKILL.md) | Architecture Review |
| [deprecation-policy](59-architecture-decision/deprecation-policy/SKILL.md) | Deprecation Policy |
| [migration-planning](59-architecture-decision/migration-planning/SKILL.md) | Migration Planning |
| [system-boundaries](59-architecture-decision/system-boundaries/SKILL.md) | System Boundaries |
| [tech-stack-selection](59-architecture-decision/tech-stack-selection/SKILL.md) | Tech Stack Selection |
| [tradeoff-analysis](59-architecture-decision/tradeoff-analysis/SKILL.md) | Trade-off Analysis |
| [versioning-strategy](59-architecture-decision/versioning-strategy/SKILL.md) | Versioning Strategy |

### 59. Release Engineering

| Skill | Description |
|-------|-------------|
| [feature-flags-experimentation](59-release-engineering/feature-flags-experimentation/SKILL.md) | Feature Flags & Experimentation |
| [legacy-migration-playbook](59-release-engineering/legacy-migration-playbook/SKILL.md) | Legacy Migration Playbook |
| [release-management](59-release-engineering/release-management/SKILL.md) | Release Management |

### 60. Github Mcp

| Skill | Description |
|-------|-------------|
| [github-code-review](60-github-mcp/github-code-review/SKILL.md) | GitHub Code Review |
| [github-issue-triage](60-github-mcp/github-issue-triage/SKILL.md) | GitHub Issue Triage |
| [github-pr-lifecycle](60-github-mcp/github-pr-lifecycle/SKILL.md) | GitHub Pull Request Lifecycle |
| [github-release-management](60-github-mcp/github-release-management/SKILL.md) | GitHub Release Management |
| [github-repo-governance](60-github-mcp/github-repo-governance/SKILL.md) | GitHub Repository Governance |
| [github-repo-navigation](60-github-mcp/github-repo-navigation/SKILL.md) | GitHub Repository Navigation |
| [github-security-triage](60-github-mcp/github-security-triage/SKILL.md) | GitHub Security Triage |
| [github-workflow-ops](60-github-mcp/github-workflow-ops/SKILL.md) | GitHub Workflow Operations |

### 61. Ai Production

| Skill | Description |
|-------|-------------|
| [llm-security-redteaming](61-ai-production/llm-security-redteaming/SKILL.md) | LLM Security & Red Teaming |
| [model-serving-inference](61-ai-production/model-serving-inference/SKILL.md) | Model Serving & Inference |
| [prompting-patterns](61-ai-production/prompting-patterns/SKILL.md) | Prompting Patterns |
| [retrieval-quality](61-ai-production/retrieval-quality/SKILL.md) | Retrieval Quality |

### 62. Scale Operations

| Skill | Description |
|-------|-------------|
| [data-migrations-backfill](62-scale-operations/data-migrations-backfill/SKILL.md) | Data Migrations & Backfill |
| [kubernetes-platform](62-scale-operations/kubernetes-platform/SKILL.md) | Kubernetes Platform Engineering |
| [multi-tenancy-saas](62-scale-operations/multi-tenancy-saas/SKILL.md) | Multi-Tenancy & SaaS Architecture |

### 63. Professional Services

| Skill | Description |
|-------|-------------|
| [proposal-sow-delivery](63-professional-services/proposal-sow-delivery/SKILL.md) | Proposal, SOW & Delivery Management |
| [runbooks-ops](63-professional-services/runbooks-ops/SKILL.md) | Runbooks & Ops |

### 64. Meta Standards

| Skill | Description |
|-------|-------------|
| [api-style-guide](64-meta-standards/api-style-guide/SKILL.md) | API Style Guide |
| [config-env-conventions](64-meta-standards/config-env-conventions/SKILL.md) | Config & Environment Conventions |
| [error-shape-taxonomy](64-meta-standards/error-shape-taxonomy/SKILL.md) | Error Shape Taxonomy |
| [event-style-guide](64-meta-standards/event-style-guide/SKILL.md) | Event Style Guide |
| [logging-metrics-tracing-standard](64-meta-standards/logging-metrics-tracing-standard/SKILL.md) | Logging, Metrics & Tracing Standard |
| [security-baseline-controls](64-meta-standards/security-baseline-controls/SKILL.md) | Security Baseline Controls |
| [service-standards-blueprint](64-meta-standards/service-standards-blueprint/SKILL.md) | Service Standards Blueprint |

### 65. Context Token Optimization

| Skill | Description |
|-------|-------------|
| [anti-bloat-checklist](65-context-token-optimization/anti-bloat-checklist/SKILL.md) | Anti-Bloat Checklist |
| [context-pack-format](65-context-token-optimization/context-pack-format/SKILL.md) | Context Pack Format |
| [prompt-library-minimal](65-context-token-optimization/prompt-library-minimal/SKILL.md) | Prompt Library Minimal |
| [retrieval-playbook-for-ai](65-context-token-optimization/retrieval-playbook-for-ai/SKILL.md) | Retrieval Playbook for AI |
| [summarization-rules-evidence-first](65-context-token-optimization/summarization-rules-evidence-first/SKILL.md) | Summarization Rules (Evidence First) |

### 66. Repo Navigation Knowledge Map

| Skill | Description |
|-------|-------------|
| [change-impact-map](66-repo-navigation-knowledge-map/change-impact-map/SKILL.md) | Change Impact Map |
| [codebase-learning](66-repo-navigation-knowledge-map/codebase-learning/SKILL.md) | Codebase Absorption Strategy |
| [docs-indexing-strategy](66-repo-navigation-knowledge-map/docs-indexing-strategy/SKILL.md) | Docs Indexing Strategy |
| [naming-and-folder-conventions](66-repo-navigation-knowledge-map/naming-and-folder-conventions/SKILL.md) | Naming & Folder Conventions |
| [repo-map-ssot](66-repo-navigation-knowledge-map/repo-map-ssot/SKILL.md) | Repo Map SSOT |
| [where-to-find-what](66-repo-navigation-knowledge-map/where-to-find-what/SKILL.md) | Where to Find What |

### 67. Codegen Scaffolding Automation

| Skill | Description |
|-------|-------------|
| [bruno-smoke-test-generator](67-codegen-scaffolding-automation/bruno-smoke-test-generator/SKILL.md) | Bruno Smoke Test Generator |
| [ci-pipeline-generator](67-codegen-scaffolding-automation/ci-pipeline-generator/SKILL.md) | CI Pipeline Generator |
| [db-migration-generator](67-codegen-scaffolding-automation/db-migration-generator/SKILL.md) | DB Migration Generator |
| [endpoint-generator](67-codegen-scaffolding-automation/endpoint-generator/SKILL.md) | Endpoint Generator |
| [event-contract-generator](67-codegen-scaffolding-automation/event-contract-generator/SKILL.md) | Event Contract Generator |
| [service-scaffold-generator](67-codegen-scaffolding-automation/service-scaffold-generator/SKILL.md) | Service Scaffold Generator |

### 68. Quality Gates Ci Policies

| Skill | Description |
|-------|-------------|
| [contract-test-gates](68-quality-gates-ci-policies/contract-test-gates/SKILL.md) | Contract Test Gates |
| [definition-of-done](68-quality-gates-ci-policies/definition-of-done/SKILL.md) | Definition of Done |
| [lint-test-typecheck-policy](68-quality-gates-ci-policies/lint-test-typecheck-policy/SKILL.md) | Lint, Test, Typecheck Policy |
| [performance-regression-gates](68-quality-gates-ci-policies/performance-regression-gates/SKILL.md) | Performance Regression Gates |
| [release-checklist-gate](68-quality-gates-ci-policies/release-checklist-gate/SKILL.md) | Release Checklist Gate |
| [security-scan-policy](68-quality-gates-ci-policies/security-scan-policy/SKILL.md) | Security Scan Policy |

### 69. Platform Engineering Lite

| Skill | Description |
|-------|-------------|
| [config-distribution](69-platform-engineering-lite/config-distribution/SKILL.md) | Config Distribution |
| [deployment-patterns](69-platform-engineering-lite/deployment-patterns/SKILL.md) | Deployment Patterns |
| [env-matrix-dev-stg-prod](69-platform-engineering-lite/env-matrix-dev-stg-prod/SKILL.md) | Environment Matrix: Dev/Stg/Prod |
| [observability-packaging](69-platform-engineering-lite/observability-packaging/SKILL.md) | Observability Packaging |
| [tenant-aware-ops](69-platform-engineering-lite/tenant-aware-ops/SKILL.md) | Tenant-Aware Ops |

### 70. Data Platform Governance

| Skill | Description |
|-------|-------------|
| [backfill-and-reconciliation-playbook](70-data-platform-governance/backfill-and-reconciliation-playbook/SKILL.md) | Backfill and Reconciliation Playbook |
| [data-contracts](70-data-platform-governance/data-contracts/SKILL.md) | Data Contracts |
| [lineage-and-provenance](70-data-platform-governance/lineage-and-provenance/SKILL.md) | Lineage and Provenance |
| [pii-policy-enforcement](70-data-platform-governance/pii-policy-enforcement/SKILL.md) | PII Policy Enforcement |
| [retention-archival](70-data-platform-governance/retention-archival/SKILL.md) | Retention and Archival |

### 71. Infrastructure Patterns

| Skill | Description |
|-------|-------------|
| [api-design-contracts](71-infrastructure-patterns/api-design-contracts/SKILL.md) | API Design Contracts |
| [caching-strategies](71-infrastructure-patterns/caching-strategies/SKILL.md) | Caching Strategies |
| [secrets-key-management](71-infrastructure-patterns/secrets-key-management/SKILL.md) | Secrets & Key Management |
| [thai-payment-integration](71-infrastructure-patterns/thai-payment-integration/SKILL.md) | Thai Payment Integration |

### 72. Metacognitive Skill Architect

| Skill | Description |
|-------|-------------|
| [agent-self-correction](72-metacognitive-skill-architect/agent-self-correction/SKILL.md) | Agent Self-Correction |
| [skill-architect](72-metacognitive-skill-architect/skill-architect/SKILL.md) | Skill Architect |
| [skill-discovery-and-chaining](72-metacognitive-skill-architect/skill-discovery-and-chaining/SKILL.md) | Skill Discovery & Chaining |
| [task-decomposition-strategy](72-metacognitive-skill-architect/task-decomposition-strategy/SKILL.md) | Task Decomposition Strategy |

### 73. Iot Fleet Management

| Skill | Description |
|-------|-------------|
| [atomic-ab-partitioning](73-iot-fleet-management/atomic-ab-partitioning/SKILL.md) | Atomic AB Partitioning |
| [differential-ota-updates](73-iot-fleet-management/differential-ota-updates/SKILL.md) | Differential OTA Updates |
| [fleet-campaign-management](73-iot-fleet-management/fleet-campaign-management/SKILL.md) | Fleet Campaign Management |

### 74. Iot Zero Trust Security

| Skill | Description |
|-------|-------------|
| [hardware-rooted-identity](74-iot-zero-trust-security/hardware-rooted-identity/SKILL.md) | Hardware Rooted Identity |
| [micro-segmentation-policy](74-iot-zero-trust-security/micro-segmentation-policy/SKILL.md) | Micro Segmentation Policy |
| [mtls-pki-management](74-iot-zero-trust-security/mtls-pki-management/SKILL.md) | mTLS PKI Management |

### 75. Edge Computing

| Skill | Description |
|-------|-------------|
| [edge-cloud-sync](75-edge-computing/edge-cloud-sync/SKILL.md) | Edge Cloud Sync |
| [lightweight-kubernetes](75-edge-computing/lightweight-kubernetes/SKILL.md) | Lightweight Kubernetes |

### 76. Iot Infrastructure

| Skill | Description |
|-------|-------------|
| [advanced-iac-iot](76-iot-infrastructure/advanced-iac-iot/SKILL.md) | Advanced IaC for IoT |
| [chaos-engineering-iot](76-iot-infrastructure/chaos-engineering-iot/SKILL.md) | Chaos Engineering for IoT |
| [disaster-recovery-iot](76-iot-infrastructure/disaster-recovery-iot/SKILL.md) | Disaster Recovery for IoT |
| [gitops-iot-infrastructure](76-iot-infrastructure/gitops-iot-infrastructure/SKILL.md) | GitOps for IoT Infrastructure |
| [multi-cloud-iot](76-iot-infrastructure/multi-cloud-iot/SKILL.md) | Multi-Cloud IoT Strategy |

### 77. Mlops Data Engineering

| Skill | Description |
|-------|-------------|
| [drift-detection-retraining](77-mlops-data-engineering/drift-detection-retraining/SKILL.md) | Drift Detection and Retraining |
| [feature-store-implementation](77-mlops-data-engineering/feature-store-implementation/SKILL.md) | Feature Store Implementation |
| [model-registry-versioning](77-mlops-data-engineering/model-registry-versioning/SKILL.md) | Model Registry and Versioning |

### 78. Inference Model Serving

| Skill | Description |
|-------|-------------|
| [high-performance-inference](78-inference-model-serving/high-performance-inference/SKILL.md) | High Performance Inference |
| [model-optimization-quantization](78-inference-model-serving/model-optimization-quantization/SKILL.md) | Model Optimization and Quantization |
| [serverless-inference](78-inference-model-serving/serverless-inference/SKILL.md) | Serverless Inference |

### 79. Edge Ai Tinyml

| Skill | Description |
|-------|-------------|
| [edge-ai-development-workflow](79-edge-ai-tinyml/edge-ai-development-workflow/SKILL.md) | Edge AI Development Workflow |
| [edge-model-compression](79-edge-ai-tinyml/edge-model-compression/SKILL.md) | Edge Model Compression |
| [hybrid-inference-architecture](79-edge-ai-tinyml/hybrid-inference-architecture/SKILL.md) | Hybrid Inference Architecture |
| [on-device-model-training](79-edge-ai-tinyml/on-device-model-training/SKILL.md) | On-Device Model Training |
| [tinyml-microcontroller-ai](79-edge-ai-tinyml/tinyml-microcontroller-ai/SKILL.md) | TinyML Microcontroller AI |

### 80. Agentic Ai Advanced Learning

| Skill | Description |
|-------|-------------|
| [agentic-ai-frameworks](80-agentic-ai-advanced-learning/agentic-ai-frameworks/SKILL.md) | Agentic AI Frameworks |

### 81. Saas Finops Pricing

| Skill | Description |
|-------|-------------|
| [cloud-unit-economics](81-saas-finops-pricing/cloud-unit-economics/SKILL.md) | Cloud Unit Economics |
| [hybrid-pricing-strategy](81-saas-finops-pricing/hybrid-pricing-strategy/SKILL.md) | Hybrid Pricing Strategy |
| [usage-based-pricing](81-saas-finops-pricing/usage-based-pricing/SKILL.md) | Usage-Based Pricing |

### 82. Technical Product Management

| Skill | Description |
|-------|-------------|
| [api-first-product-strategy](82-technical-product-management/api-first-product-strategy/SKILL.md) | API-First Product Strategy |
| [business-to-technical-spec](82-technical-product-management/business-to-technical-spec/SKILL.md) | Business to Technical Specification |
| [competitive-intelligence](82-technical-product-management/competitive-intelligence/SKILL.md) | Competitive Intelligence |
| [cross-functional-leadership](82-technical-product-management/cross-functional-leadership/SKILL.md) | Cross-Functional Leadership |
| [feature-prioritization](82-technical-product-management/feature-prioritization/SKILL.md) | Feature Prioritization |
| [platform-product-design](82-technical-product-management/platform-product-design/SKILL.md) | Platform Product Design |
| [product-analytics-implementation](82-technical-product-management/product-analytics-implementation/SKILL.md) | Product Analytics Implementation |
| [product-discovery-validation](82-technical-product-management/product-discovery-validation/SKILL.md) | Product Discovery & Validation |
| [product-roadmap-communication](82-technical-product-management/product-roadmap-communication/SKILL.md) | Product Roadmap Communication |
| [technical-debt-prioritization](82-technical-product-management/technical-debt-prioritization/SKILL.md) | Technical Debt Prioritization |

### 83. Go To Market Tech

| Skill | Description |
|-------|-------------|
| [analyst-relations](83-go-to-market-tech/analyst-relations/SKILL.md) | Analyst Relations |
| [customer-success-automation](83-go-to-market-tech/customer-success-automation/SKILL.md) | Customer Success Automation |
| [demand-generation-automation](83-go-to-market-tech/demand-generation-automation/SKILL.md) | Demand Generation Automation |
| [developer-relations-community](83-go-to-market-tech/developer-relations-community/SKILL.md) | Developer Relations & Community |
| [enterprise-sales-alignment](83-go-to-market-tech/enterprise-sales-alignment/SKILL.md) | Enterprise Sales Alignment |
| [go-to-market-analytics](83-go-to-market-tech/go-to-market-analytics/SKILL.md) | Go-to-Market Analytics |
| [launch-strategy-execution](83-go-to-market-tech/launch-strategy-execution/SKILL.md) | Launch Strategy & Execution |
| [partner-program-design](83-go-to-market-tech/partner-program-design/SKILL.md) | Partner Program Design |
| [revenue-operations-revops](83-go-to-market-tech/revenue-operations-revops/SKILL.md) | Revenue Operations (RevOps) |
| [sales-engineering](83-go-to-market-tech/sales-engineering/SKILL.md) | Sales Engineering |
| [sales-operations-automation](83-go-to-market-tech/sales-operations-automation/SKILL.md) | Sales Operations Automation |
| [technical-content-marketing](83-go-to-market-tech/technical-content-marketing/SKILL.md) | Technical Content Marketing |

### 85. Future Compliance

| Skill | Description |
|-------|-------------|
| [ai-audit-trail](85-future-compliance/ai-audit-trail/SKILL.md) | AI Audit Trail & Accountability |
| [algorithmic-accountability](85-future-compliance/algorithmic-accountability/SKILL.md) | Algorithmic Accountability |
| [cross-border-data-transfer](85-future-compliance/cross-border-data-transfer/SKILL.md) | Cross-border Data Transfer Compliance |

### 86. Sustainable Ai

| Skill | Description |
|-------|-------------|
| [green-computing-finops](86-sustainable-ai/green-computing-finops/SKILL.md) | Sustainable AI & Green Computing (FinOps 2.0) |

### 87. Multi Agent Governance

| Skill | Description |
|-------|-------------|
| [multi-agent-orchestration](87-multi-agent-governance/multi-agent-orchestration/SKILL.md) | Multi-Agent Orchestration & Governance |

### 88. Ai Supply Chain Security

| Skill | Description |
|-------|-------------|
| [model-bom-security](88-ai-supply-chain-security/model-bom-security/SKILL.md) | AI Supply Chain Security (Model BOM) |

### 89. Post Quantum Cryptography

| Skill | Description |
|-------|-------------|
| [pqc-for-iot](89-post-quantum-cryptography/pqc-for-iot/SKILL.md) | Post-Quantum Cryptography (PQC) for IoT |
<!-- SKILLS-END -->
