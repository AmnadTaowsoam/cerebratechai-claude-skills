---
name: Docs Indexing Strategy
description: How to organize and index documentation for humans and AI: taxonomy, metadata, cross-linking, freshness reviews, and automated index generation
---

# Docs Indexing Strategy

## Overview

Strategy สำหรับ organize และ index documentation ให้ค้นหาได้ง่าย ทั้งคนและ AI รวมถึง categorization, tagging, และ cross-linking ที่ทำให้ docs discoverable

## Why This Matters

- **Findability**: หา docs ที่ต้องการได้เร็ว
- **Completeness**: รู้ว่า docs ครบหรือยัง
- **AI retrieval**: AI ดึง docs ที่ relevant ได้
- **Maintenance**: รู้ว่า docs ไหนต้อง update

---

## Core Concepts

### 1. Documentation Types

- **Getting started**: setup, local dev, contributing
- **API reference**: OpenAPI/GraphQL, examples, error codes, auth
- **Architecture**: system overview, boundaries, data flows, diagrams
- **Runbooks/Operations**: incident response, dashboards, alerts, rollback
- **ADRs**: decisions + rationale + alternatives + status
- **Security/Compliance**: threat model, controls, data handling policies

### 2. Categorization System

- เลือก taxonomy เดียว: by domain (`billing/`, `auth/`) หรือ by audience (`dev/`, `ops/`) หรือ hybrid ที่ชัดเจน
- โครงสร้างต้อง stable และสอดคล้องกับ repo map (`REPO.md`/architecture)
- หลีกเลี่ยง deep nesting; ให้หาได้ภายใน 2–3 คลิก

### 3. Tagging Strategy

- ใช้ tags สำหรับ cross-cutting topics (`#security`, `#migration`, `#performance`)
- ใส่ keywords ใน title/first paragraph เพื่อให้ search/AI retrieval เจอ
- metadata ที่สำคัญ: owner, updated date, audience, status (draft/current/deprecated)

### 4. Cross-Linking

- ทุก doc ควรมี “Related/See also” (อย่างน้อย 2–5 ลิงก์)
- ลิงก์ bidirectional ในหัวข้อสำคัญ (guide ↔ runbook, ADR ↔ design doc)
- ใช้ link-check ใน CI เพื่อกัน 404

### 5. Search Optimization

- title ต้องเฉพาะเจาะจง (ไม่ใช้ “Guide”, “Notes” แบบลอย ๆ)
- ใส่ summary 2–3 บรรทัดแรก: บอก “ทำอะไร/สำหรับใคร/เมื่อไหร่ต้องใช้”
- ใช้ heading ที่สม่ำเสมอ เพื่อให้ snippet/search เดาง่าย (`## Troubleshooting`, `## Rollback`)

### 6. Freshness Tracking

- มี `updated` และ `reviewBy` (หรือ review cadence) สำหรับ doc สำคัญ
- สร้าง “stale docs report” (เช่น > 90 วันไม่ได้แตะ) และมี owner รับผิดชอบ

### 7. Audience Targeting

- แยก audience ชัด: developers / ops / security / product/support
- สำหรับ doc ที่หลาย audience ใช้: เริ่มด้วย TL;DR + ลิงก์ไปส่วนลึก

### 8. Index Generation

- ใช้ index file (`DOCS_INDEX.md`) เป็น entry point และอนุญาตให้ generate บางส่วนอัตโนมัติ
- เก็บ index ที่ “อ่านง่าย” (manual curation) และ “ครบ” (auto scan) ควบคู่กัน
- ทำงานร่วมกับ RAG/embedding ได้ดีขึ้นเมื่อมี metadata + stable links

## Quick Start

```markdown
# 1) เลือก taxonomy ของ docs (by domain / by audience / hybrid)
# 2) สร้าง `docs/DOCS_INDEX.md` เป็น entry point
# 3) บังคับ metadata ในทุก docs สำคัญ (owner, updated, tags, audience)
# 4) ทำ cross-linking + link check ใน CI
```

## Production Checklist

- [ ] Documentation categorized by type
- [ ] All docs have metadata (date, owner, tags)
- [ ] Index generated and maintained
- [ ] Cross-links verified
- [ ] Search-friendly titles
- [ ] Review schedule in place

## Documentation Index Template

```markdown
# DOCS_INDEX.md

> Last updated: 2024-01-15 | Auto-generated: Partially

## Quick Navigation

| I want to... | Go to |
|--------------|-------|
| Set up dev environment | [Development Guide](./development.md) |
| Deploy to production | [Deployment Guide](./deployment.md) |
| Handle an incident | [Runbooks](./runbooks/) |
| Understand architecture | [Architecture](./architecture/) |

## By Category

### 📖 Getting Started
| Doc | Audience | Updated |
|-----|----------|---------|
| [README](../README.md) | All | 2024-01-15 |
| [Development Setup](./development.md) | Dev | 2024-01-10 |
| [Contributing Guide](./CONTRIBUTING.md) | Dev | 2024-01-08 |

### 🏗️ Architecture
| Doc | Audience | Updated |
|-----|----------|---------|
| [System Overview](./architecture/overview.md) | All | 2024-01-05 |
| [Database Design](./architecture/database.md) | Dev | 2024-01-03 |
| [API Design](./architecture/api.md) | Dev | 2024-01-02 |

### 📡 API Reference
| Doc | Audience | Updated |
|-----|----------|---------|
| [REST API](./api/rest.md) | Dev | 2024-01-12 |
| [GraphQL Schema](./api/graphql.md) | Dev | 2024-01-10 |
| [WebSocket Events](./api/websocket.md) | Dev | 2024-01-08 |

### 🚀 Operations
| Doc | Audience | Updated |
|-----|----------|---------|
| [Deployment Guide](./ops/deployment.md) | DevOps | 2024-01-14 |
| [Monitoring Guide](./ops/monitoring.md) | DevOps | 2024-01-10 |
| [Runbook Index](./runbooks/INDEX.md) | Ops | 2024-01-15 |

### 📝 ADRs (Architecture Decision Records)
| ADR | Status | Date |
|-----|--------|------|
| [ADR-001: Database Choice](./adr/001-database.md) | Accepted | 2023-06-15 |
| [ADR-002: Auth Strategy](./adr/002-auth.md) | Accepted | 2023-07-20 |
| [ADR-003: API Versioning](./adr/003-versioning.md) | Proposed | 2024-01-10 |

## By Tag

### #authentication
- [Auth Strategy ADR](./adr/002-auth.md)
- [Session Management](./architecture/sessions.md)
- [OAuth Setup](./guides/oauth.md)

### #database
- [Database Design](./architecture/database.md)
- [Migration Guide](./guides/migrations.md)
- [Backup Runbook](./runbooks/database-backup.md)

### #deployment
- [Deployment Guide](./ops/deployment.md)
- [Rollback Procedure](./runbooks/rollback.md)
- [Environment Setup](./ops/environments.md)

## Stale Docs (Need Review)
| Doc | Last Updated | Days Old |
|-----|--------------|----------|
| [Legacy API](./api/legacy.md) | 2023-06-01 | 228 |
| [Old Auth Flow](./guides/auth-v1.md) | 2023-08-15 | 153 |

## Missing Docs
- [ ] Error handling guide
- [ ] Performance tuning
- [ ] Security best practices
```

## Document Metadata

```markdown
---
title: Development Setup Guide
description: How to set up local development environment
author: @team-lead
created: 2024-01-01
updated: 2024-01-15
tags: [getting-started, development, setup]
audience: developers
status: current
related:
  - ./deployment.md
  - ./contributing.md
---
```

## Anti-patterns

1. **No index**: Docs scattered, unfindable
2. **Stale index**: Doesn't match actual docs
3. **No metadata**: Can't filter or sort
4. **Broken links**: Cross-references 404
5. **No audience**: One-size-fits-all confusion

## Search Optimization Tips

```markdown
# Good: Searchable title
"How to Set Up PostgreSQL Database"

# Bad: Vague title
"Database Guide"

# Good: Keywords in first paragraph
"This guide explains how to configure Redis caching
for session storage in production environments."

# Bad: No context
"Follow these steps to configure the system."
```

## Integration Points

- Documentation sites (Docusaurus, GitBook)
- AI RAG systems
- Search tools (Algolia, local search)
- CI/CD (link checking, freshness alerts)

## Further Reading

- [Divio Documentation System](https://documentation.divio.com/)
- [Write the Docs](https://www.writethedocs.org/)
