# 🧠 Cerebrate Chai - Claude Skills Repository

> **Comprehensive skill library for Claude AI to build production-ready applications**

A curated collection of **346+ specialized skills** across **58 categories** covering everything from core development to advanced features like AI/ML, blockchain, IoT, system resilience, cost engineering, and more. Each skill provides detailed implementation guides, best practices, and production-ready code examples.

[![Skills](https://img.shields.io/badge/Skills-346+-blue)](https://github.com/AmnadTaowsoam/cerebratechai-claude-skills)
[![Categories](https://img.shields.io/badge/Categories-58-purple)](https://github.com/AmnadTaowsoam/cerebratechai-claude-skills)
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

- **346+ Skills** covering full-stack development across **58 categories**
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

### For Claude Desktop/CLI Users

1. **Clone the repository**
```bash
git clone https://github.com/AmnadTaowsoam/cerebratechai-claude-skills.git
cd cerebratechai-claude-skills
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

### For Claude.ai Web Users

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

### 02. 🎨 Frontend Development (8 skills)
Modern frontend frameworks and patterns.

- [Next.js Patterns](02-frontend/nextjs-patterns/SKILL.md) - Next.js 14+ App Router
- [React Best Practices](02-frontend/react-best-practices/SKILL.md) - React patterns
- [Tailwind Patterns](02-frontend/tailwind-patterns/SKILL.md) - Tailwind CSS
- [Material-UI](02-frontend/mui-material/SKILL.md) - MUI components
- [shadcn/ui](02-frontend/shadcn-ui/SKILL.md) - shadcn/ui patterns
- [Form Handling](02-frontend/form-handling/SKILL.md) - React Hook Form + Zod
- [State Management](02-frontend/state-management/SKILL.md) - Zustand, Redux, TanStack Query
- [Animation](02-frontend/animation/SKILL.md) - Framer Motion, CSS animations

### 03. ⚙️ Backend API (7 skills)
Backend development patterns.

- [Node.js API](03-backend-api/nodejs-api/SKILL.md) - Node.js REST APIs
- [FastAPI Patterns](03-backend-api/fastapi-patterns/SKILL.md) - FastAPI Python
- [Express REST](03-backend-api/express-rest/SKILL.md) - Express.js patterns
- [Fastify REST API](03-backend-api/fastify-rest-api/SKILL.md) - Fastify patterns
- [Error Handling](03-backend-api/error-handling/SKILL.md) - Error patterns
- [Validation](03-backend-api/validation/SKILL.md) - Request validation
- [Middleware](03-backend-api/middleware/SKILL.md) - Middleware patterns

### 04. 🗄️ Database (7 skills)
Database design and optimization.

- [Prisma Guide](04-database/prisma-guide/SKILL.md) - Prisma ORM
- [MongoDB Patterns](04-database/mongodb-patterns/SKILL.md) - MongoDB
- [Redis Caching](04-database/redis-caching/SKILL.md) - Redis patterns
- [TimescaleDB](04-database/timescaledb/SKILL.md) - Time-series database
- [Vector Database](04-database/vector-database/SKILL.md) - Pinecone, Qdrant, Weaviate
- [Database Optimization](04-database/database-optimization/SKILL.md) - Performance tuning
- [Database Migrations](04-database/database-migrations/SKILL.md) - Schema migrations

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

### 06. 🚀 AI/ML Production (8 skills)
Production AI/ML systems.

- [LLM Integration](06-ai-ml-production/llm-integration/SKILL.md) - OpenAI, Anthropic, Azure
- [Local LLM Deployment](06-ai-ml-production/llm-local-deployment/SKILL.md) - Ollama, vLLM
- [RAG Implementation](06-ai-ml-production/rag-implementation/SKILL.md) - Retrieval-Augmented Generation
- [Embedding Models](06-ai-ml-production/embedding-models/SKILL.md) - Text embeddings
- [Vector Search](06-ai-ml-production/vector-search/SKILL.md) - Semantic search
- [Prompt Engineering](06-ai-ml-production/prompt-engineering/SKILL.md) - Prompt patterns
- [LLM Guardrails](06-ai-ml-production/llm-guardrails/SKILL.md) - NeMo Guardrails
- [AI Observability](06-ai-ml-production/ai-observability/SKILL.md) - Monitoring

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

### 09. 🔧 Microservices (6 skills)
Microservices architecture.

- [Service Design](09-microservices/service-design/SKILL.md) - Design principles
- [API Gateway](09-microservices/api-gateway/SKILL.md) - Kong, NGINX
- [Service Mesh](09-microservices/service-mesh/SKILL.md) - Istio, Linkerd
- [Circuit Breaker](09-microservices/circuit-breaker/SKILL.md) - Resilience patterns
- [Service Discovery](09-microservices/service-discovery/SKILL.md) - Consul, etcd
- [Event-Driven](09-microservices/event-driven/SKILL.md) - Event sourcing, CQRS

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

### 15. 🐳 DevOps & Infrastructure (7 skills)
Infrastructure as code and CI/CD.

- [Docker Patterns](15-devops-infrastructure/docker-patterns/SKILL.md) - Docker
- [Docker Compose](15-devops-infrastructure/docker-compose/SKILL.md) - Multi-container
- [Kubernetes](15-devops-infrastructure/kubernetes-deployment/SKILL.md) - K8s deployment
- [Helm Charts](15-devops-infrastructure/helm-charts/SKILL.md) - Helm
- [GitHub Actions](15-devops-infrastructure/ci-cd-github-actions/SKILL.md) - CI/CD
- [Terraform](15-devops-infrastructure/terraform-infrastructure/SKILL.md) - IaC
- [Secrets Management](15-devops-infrastructure/secrets-management/SKILL.md) - Vault

### 16. 🧪 Testing (7 skills)
Testing strategies and frameworks.

- [Jest Patterns](16-testing/jest-patterns/SKILL.md) - Jest testing
- [Pytest Patterns](16-testing/pytest-patterns/SKILL.md) - Python testing
- [E2E Playwright](16-testing/e2e-playwright/SKILL.md) - End-to-end testing
- [Integration Testing](16-testing/integration-testing/SKILL.md) - Integration tests
- [Load Testing](16-testing/load-testing/SKILL.md) - k6, Artillery
- [ML Model Testing](16-testing/ml-model-testing/SKILL.md) - Model validation
- [Test Data Factory](16-testing/test-data-factory/SKILL.md) - Test data

### 17. 🎯 Domain-Specific (6 skills)
Cross-cutting concerns.

- [Multi-Tenancy](17-domain-specific/multi-tenancy/SKILL.md) - Multi-tenant architecture
- [Rate Limiting](17-domain-specific/rate-limiting/SKILL.md) - Rate limiting
- [API Versioning](17-domain-specific/api-versioning/SKILL.md) - Versioning strategies
- [Feature Flags](17-domain-specific/feature-flags/SKILL.md) - Feature toggles
- [Analytics Tracking](17-domain-specific/analytics-tracking/SKILL.md) - Analytics
- [Notification System](17-domain-specific/notification-system/SKILL.md) - Notifications

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

### 20. 🤖 AI Integration (5 skills)
AI-powered features.

- [llm.txt Protocol](20-ai-integration/llm-txt-protocol/SKILL.md) - llm.txt
- [AI Agents](20-ai-integration/ai-agents/SKILL.md) - LangChain agents
- [Chatbot](20-ai-integration/chatbot-integration/SKILL.md) - Chatbot UI
- [AI Search](20-ai-integration/ai-search/SKILL.md) - Semantic search
- [Conversational UI](20-ai-integration/conversational-ui/SKILL.md) - Chat interfaces

### 21. 📝 Documentation (6 skills)
Technical documentation.

- [Technical Writing](21-documentation/technical-writing/SKILL.md) - Writing guides
- [API Documentation](21-documentation/api-documentation/SKILL.md) - API docs
- [User Guides](21-documentation/user-guides/SKILL.md) - User documentation
- [Architecture Docs](21-documentation/system-architecture-docs/SKILL.md) - System design
- [Runbooks](21-documentation/runbooks/SKILL.md) - Operational runbooks
- [Changelog](21-documentation/changelog-management/SKILL.md) - Changelog management

### 22. 🎨 UX/UI Design (6 skills)
User experience and design.

- [Design Systems](22-ux-ui-design/design-systems/SKILL.md) - Design systems
- [Accessibility](22-ux-ui-design/accessibility/SKILL.md) - Web accessibility
- [Responsive Design](22-ux-ui-design/responsive-design/SKILL.md) - Responsive design
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

### 24. 🔒 Security Practices (6 skills)
Security best practices.

- [Incident Response](24-security-practices/incident-response/SKILL.md) - Security incident handling
- [OWASP Top 10](24-security-practices/owasp-top-10/SKILL.md) - Common vulnerabilities
- [Penetration Testing](24-security-practices/penetration-testing/SKILL.md) - Security testing
- [Secure Coding](24-security-practices/secure-coding/SKILL.md) - Secure development
- [Security Audit](24-security-practices/security-audit/SKILL.md) - Security assessments
- [Vulnerability Management](24-security-practices/vulnerability-management/SKILL.md) - Vulnerability tracking

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

### 40. 🛡️ System Resilience (7 skills)
Building resilient and fault-tolerant systems.

- [Circuit Breaker & Bulkhead](40-system-resilience/circuit-breaker-bulkhead/SKILL.md) - Resilience patterns
- [Disaster Recovery](40-system-resilience/disaster-recovery/SKILL.md) - DR planning
- [Failure Modes and Effects](40-system-resilience/failure-modes-and-effects/SKILL.md) - FMEA analysis
- [Graceful Degradation](40-system-resilience/graceful-degradation/SKILL.md) - Degradation strategies
- [Idempotency and Dedup](40-system-resilience/idempotency-and-dedup/SKILL.md) - Idempotent operations
- [Postmortems and RCA](40-system-resilience/postmortems-and-rca/SKILL.md) - Root cause analysis
- [Retry, Timeout, Backoff](40-system-resilience/retry-timeout-backoff/SKILL.md) - Retry patterns

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
git clone https://github.com/AmnadTaowsoam/cerebratechai-claude-skills.git
cd cerebratechai-claude-skills

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

- **Issues**: [GitHub Issues](https://github.com/AmnadTaowsoam/cerebratechai-claude-skills/issues)
- **Discussions**: [GitHub Discussions](https://github.com/AmnadTaowsoam/cerebratechai-claude-skills/discussions)
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

- **Total Skills**: 346+
- **Categories**: 58
- **Languages**: TypeScript, Python, SQL, Dart, Solidity, Go
- **Frameworks**: 60+
- **Last Updated**: January 2026

---

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=AmnadTaowsoam/cerebratechai-claude-skills&type=Date)](https://star-history.com/#AmnadTaowsoam/cerebratechai-claude-skills&Date)

---

<div align="center">

**Made with ❤️ by [Cerebrate Chai](https://cerebratechai.com)**

[Website](https://cerebratechai.com) • [GitHub](https://github.com/AmnadTaowsoam) • [Twitter](https://twitter.com/cerebratechai)

</div>