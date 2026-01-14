# Project Context: [Project Name]

## Project Overview
**Type**: [SaaS / E-commerce / Mobile App / AI Product / etc.]
**Description**: [Brief description of the project]
**Target Users**: [Who will use this application]

## Tech Stack

### Frontend
- Framework: [Next.js 14 / React / Vue / etc.]
- UI Library: [TailwindCSS / MUI / shadcn/ui]
- State Management: [Zustand / Redux / TanStack Query]
- Form Handling: [React Hook Form + Zod]

### Backend
- Language: [Node.js / Python / Go]
- Framework: [Express / Fastify / FastAPI]
- Database: [PostgreSQL / MongoDB / etc.]
- ORM: [Prisma / TypeORM / SQLAlchemy]

### Infrastructure
- Hosting: [Vercel / AWS / GCP / Azure]
- Database Hosting: [Supabase / PlanetScale / AWS RDS]
- File Storage: [S3 / Cloudflare R2 / Google Cloud Storage]
- CDN: [CloudFront / Cloudflare]

## Required Skills

### Essential (Must Have)
- [ ] 01-foundations/typescript-standards
- [ ] 02-frontend/nextjs-patterns
- [ ] 03-backend-api/nodejs-api
- [ ] 04-database/prisma-guide
- [ ] 10-authentication-authorization/jwt-authentication

### Important (High Priority)
- [ ] 11-billing-subscription/stripe-integration
- [ ] 12-compliance-governance/pdpa-compliance
- [ ] 14-monitoring-observability/prometheus-metrics
- [ ] 15-devops-infrastructure/docker-patterns

### Optional (Nice to Have)
- [ ] 20-ai-integration/chatbot-integration
- [ ] 34-real-time-features/websocket-patterns

## Key Features

### Phase 1 (MVP)
1. User authentication (email/password)
2. User profile management
3. [Feature 1]
4. [Feature 2]

### Phase 2
1. [Feature 3]
2. [Feature 4]

### Phase 3
1. [Feature 5]
2. [Feature 6]

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh token
- `POST /api/auth/logout` - Logout

### Users
- `GET /api/users/:id` - Get user profile
- `PUT /api/users/:id` - Update user profile
- `DELETE /api/users/:id` - Delete user account

### [Other Endpoints]
[Add more endpoint groups as needed]

## Database Schema

### Core Tables
- `users` - User accounts
- `profiles` - User profiles
- `sessions` - Active sessions
- [Other tables]

## Security Requirements
- [ ] HTTPS in production
- [ ] JWT token expiration (15 min access, 7 day refresh)
- [ ] Password hashing (bcrypt, cost factor 10)
- [ ] Rate limiting on auth endpoints
- [ ] CSRF protection
- [ ] XSS prevention
- [ ] SQL injection prevention (using ORM)
- [ ] Environment variables for secrets

## Compliance Requirements
- [ ] PDPA compliance (if Thailand users)
- [ ] GDPR compliance (if EU users)
- [ ] Data retention policy
- [ ] User consent management
- [ ] Data export capability
- [ ] Data deletion capability

## Performance Targets
- API response time: < 200ms (p95)
- Page load time: < 2s
- Time to Interactive: < 3s
- Core Web Vitals: All green

## Development Workflow
1. Feature branch from `develop`
2. Implement following skills
3. Write tests (unit + integration)
4. Create PR with description
5. Code review
6. Merge to `develop`
7. Deploy to staging
8. QA testing
9. Merge to `main`
10. Deploy to production

## Deployment Strategy
- **Environment**: Development → Staging → Production
- **CI/CD**: GitHub Actions
- **Database Migrations**: Automated with Prisma
- **Rollback**: Blue-green deployment

## Monitoring & Logging
- Application logs: [CloudWatch / Datadog]
- Error tracking: [Sentry]
- Performance monitoring: [New Relic / Datadog APM]
- Uptime monitoring: [Pingdom / UptimeRobot]

## Team & Communication
- Project Manager: [Name]
- Tech Lead: [Name]
- Frontend Developers: [Names]
- Backend Developers: [Names]
- DevOps: [Name]

- Daily Standup: [Time]
- Sprint Planning: [Schedule]
- Sprint Review: [Schedule]
- Retrospective: [Schedule]

## Documentation
- API Documentation: [Swagger URL]
- Technical Documentation: [Confluence / Notion URL]
- User Documentation: [Link]
- Runbooks: [Link]

## Timeline
- **Phase 1 (MVP)**: [Date range]
- **Phase 2**: [Date range]
- **Phase 3**: [Date range]
- **Launch**: [Target date]

## Success Metrics
- User registration: [Target number]
- Monthly Active Users: [Target number]
- API uptime: 99.9%
- Customer satisfaction: > 4.5/5

---

**Instructions for Claude:**
When implementing features for this project, always:
1. Reference the appropriate skills from the list above
2. Follow the tech stack specifications
3. Implement security requirements
4. Include error handling and logging
5. Write tests for all functionality
6. Update API documentation
7. Consider performance implications