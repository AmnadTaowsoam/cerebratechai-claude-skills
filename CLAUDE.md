# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a collection of Claude Code skills documentation organized by technical domain. Each skill provides reference material, code patterns, and best practices for specific technologies or patterns.

## Repository Structure

Skills are organized in numbered directories by domain:

- `01-foundations/` - Core standards (API design, code review, git, Python/TypeScript standards)
- `02-frontend/` - React, Next.js, state management, UI libraries (MUI, shadcn, Tailwind)
- `03-backend-api/` - Express, FastAPI, Node.js, error handling, validation
- `04-database/` - Prisma, MongoDB, Redis, TimescaleDB, vector databases, migrations
- `05-ai-ml-core/` - Data preprocessing, model training, YOLO, PyTorch, Label Studio
- `06-ai-ml-production/` - LLM integration, RAG, embeddings, prompt engineering, guardrails
- `07-document-processing/` - OCR (Tesseract, PaddleOCR), PDF processing, image preprocessing
- `08-messaging-queue/` - Kafka, RabbitMQ, Redis queues, MQTT
- `09-microservices/` - Service design, API gateway, circuit breaker, service mesh
- `10-authentication-authorization/` - JWT, OAuth2, RBAC, session management
- `11-billing-subscription/` - Stripe, subscriptions, usage metering, invoicing
- `12-compliance-governance/` - GDPR, PDPA, audit logging, data privacy
- `13-file-storage/` - S3, CDN, multipart uploads, image optimization
- `14-monitoring-observability/` - Prometheus, Grafana, ELK stack, distributed tracing
- `15-devops-infrastructure/` - Docker, Kubernetes, Helm, Terraform, GitHub Actions
- `16-testing/` - Jest, Pytest, Playwright, integration/load testing
- `17-domain-specific/` - Multi-tenancy, feature flags, rate limiting, notifications

Each skill directory contains a `SKILL.md` file with the skill documentation.

## Skill File Format

Each `SKILL.md` typically contains:
- Overview section describing the skill's purpose
- Key topics covered
- Code examples with TypeScript or Python patterns
- Best practices checklists where applicable

## Working with This Repository

When adding or modifying skills:
- Place new skills in the appropriate numbered domain directory
- Create a subdirectory with a descriptive kebab-case name
- Include a `SKILL.md` file following the established format
- Skills may contain bilingual content (English and Thai)
