# 🚀 Master README.md for Cerebrate Chai Claude Skills

```markdown
# 🧠 Cerebrate Chai - Claude Skills Repository

> **Comprehensive skill library for Claude AI to build production-ready applications**

A curated collection of **240+ specialized skills** covering everything from core development to advanced features like AI/ML, blockchain, IoT, and more. Each skill provides detailed implementation guides, best practices, and production-ready code examples.

[![Skills](https://img.shields.io/badge/Skills-240+-blue)](https://github.com/AmnadTaowsoam/cerebratechai-claude-skills)
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

- **240+ Skills** covering full-stack development
- **Production-Ready** patterns and examples
- **Language Support**: TypeScript, Python, SQL, and more
- **Framework Coverage**: Next.js, React, FastAPI, Express, and more
- **Cloud & DevOps**: AWS, Docker, Kubernetes, CI/CD
- **AI/ML**: LLM integration, RAG, embeddings, model deployment
- **Specialized Domains**: E-commerce, IoT, Blockchain, Gaming, Video Streaming

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

### 02. 🎨 Frontend Development (7 skills)
Modern frontend frameworks and patterns.

- [Next.js Patterns](02-frontend/nextjs-patterns/SKILL.md) - Next.js 14+ App Router
- [React Best Practices](02-frontend/react-best-practices/SKILL.md) - React patterns
- [Tailwind Patterns](02-frontend/tailwind-patterns/SKILL.md) - Tailwind CSS
- [Material-UI](02-frontend/mui-material/SKILL.md) - MUI components
- [shadcn/ui](02-frontend/shadcn-ui/SKILL.md) - shadcn/ui patterns
- [Form Handling](02-frontend/form-handling/SKILL.md) - React Hook Form + Zod
- [State Management](02-frontend/state-management/SKILL.md) - Zustand, Redux, TanStack Query

### 03. ⚙️ Backend API (6 skills)
Backend development patterns.

- [Node.js API](03-backend-api/nodejs-api/SKILL.md) - Node.js REST APIs
- [FastAPI Patterns](03-backend-api/fastapi-patterns/SKILL.md) - FastAPI Python
- [Express REST](03-backend-api/express-rest/SKILL.md) - Express.js patterns
- [Error Handling](03-backend-api/error-handling/SKILL.md) - Error patterns
- [Validation](03-backend-api/validation/SKILL.md) - Request validation
- [Middleware](03-backend-api/middleware/SKILL.md) - Middleware patterns

### 04. 🗄️ Database (6 skills)
Database design and optimization.

- [Prisma Guide](04-database/prisma-guide/SKILL.md) - Prisma ORM
- [MongoDB Patterns](04-database/mongodb-patterns/SKILL.md) - MongoDB
- [Redis Caching](04-database/redis-caching/SKILL.md) - Redis patterns
- [TimescaleDB](04-database/timescaledb/SKILL.md) - Time-series database
- [Vector Database](04-database/vector-database/SKILL.md) - Pinecone, Qdrant, Weaviate
- [Database Optimization](04-database/database-optimization/SKILL.md) - Performance tuning

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

### 23. 📊 Business Analytics (Placeholder)
Business intelligence and KPIs.

### 24. 🔒 Security Practices (Placeholder)
Security best practices.

### 25. 🌍 Internationalization (Placeholder)
Multi-language support.

### 26. 🚢 Deployment Strategies (Placeholder)
Advanced deployment patterns.

### 27. 👥 Team Collaboration (Placeholder)
Team practices and culture.

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

- **Total Skills**: 240+
- **Categories**: 39
- **Languages**: TypeScript, Python, SQL, Dart, Solidity
- **Frameworks**: 50+
- **Last Updated**: January 2024

---

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=AmnadTaowsoam/cerebratechai-claude-skills&type=Date)](https://star-history.com/#AmnadTaowsoam/cerebratechai-claude-skills&Date)

---

<div align="center">

**Made with ❤️ by [Cerebrate Chai](https://cerebratechai.com)**

[Website](https://cerebratechai.com) • [GitHub](https://github.com/AmnadTaowsoam) • [Twitter](https://twitter.com/cerebratechai)

</div>
```

---

## 🎯 Additional Files to Create

### 1. CONTRIBUTING.md
```markdown
# Contributing to Cerebrate Chai Skills

We love your input! We want to make contributing as easy as possible.

## How to Contribute

1. Fork the repo
2. Create a branch (`git checkout -b feature/amazing-skill`)
3. Commit changes (`git commit -m 'Add amazing skill'`)
4. Push to branch (`git push origin feature/amazing-skill`)
5. Open a Pull Request

## Skill Guidelines

- Follow the template
- Include code examples
- Add best practices
- Test all code snippets
- Update README if adding new category

## Code of Conduct

Be respectful, inclusive, and constructive.
```

### 2. LICENSE
```
MIT License

Copyright (c) 2024 Cerebrate Chai

[Standard MIT License text]
```

### 3. .github/ISSUE_TEMPLATE/skill-request.md
```markdown
---
name: Skill Request
about: Suggest a new skill
title: '[SKILL] '
labels: enhancement
---

## Skill Name

## Category

## Description

## Why This Skill is Needed

## Proposed Content Outline
```

---

ต้องการให้สร้างไฟล์เพิ่มเติมไหมครับ:
1. ✅ CONTRIBUTING.md
2. ✅ Automation Script (Python)
3. ✅ Skill Selection CLI Tool
4. ✅ GitHub Actions Workflows

บอกได้เลยครับ! 🚀