# Next.js 14+ App Router Patterns

---

## 1. Executive Summary & Strategic Necessity

### 1.1 Context (ภาษาไทย)

Next.js 14+ App Router คือ framework สำหรับ React ที่มี features ที่ทรงพลัง เช่น Server Components, Streaming, Server Actions, และ Improved Data Fetching App Router ใช้ file-based routing และ nested layouts ที่ช่วยให้การสร้าง complex applications ง่ายขึ้น

Next.js 14+ มี features ที่สำคัญ เช่น:
- **Server Components** - Components ที่ทำงานบน server และลด JavaScript bundle
- **Streaming** - ส่ง HTML และ data แบบ progressive ไปยัง client
- **Server Actions** - Functions ที่ทำงานบน server และเรียกจาก client components
- **Route Handlers** - API routes ที่ทำงานบน server
- **Middleware** - Intercept requests และ responses

### 1.2 Business Impact (ภาษาไทย)

**ผลกระทบทางธุรกิจ:**

1. **ลด Time-to-Market** - Next.js ช่วยลดเวลาในการพัฒนาได้ถึง 30-40%
2. **เพิ่ม Performance** - Server Components และ Streaming ช่วยเพิ่ม performance
3. **ลด Infrastructure Cost** - Edge runtime และ caching ช่วยลด cost
4. **เพิ่ม SEO** - Server-side rendering ช่วยเพิ่ม SEO
5. **ปรับปรุง Developer Experience** - Features ที่ทรงพลังช่วยเพิ่ม productivity

### 1.3 Product Thinking (ภาษาไทย)

**มุมมองด้านผลิตภัณฑ์:**

1. **Performance-First** - Next.js ต้องไม่ส่งผลกระทบต่อ performance ของแอปพลิเคชัน
2. **SEO-Ready** - Server-side rendering ช่วยเพิ่ม SEO
3. **Scalable** - Features ที่ทรงพลังช่วยให้แอปพลิเคชัน scalable
4. **Developer-Friendly** - Features ที่ใช้งานง่ายช่วยเพิ่ม productivity
5. **Future-Proof** - Next.js มี updates และ features ใหม่อย่างต่อเนื่อง

---

## 2. Technical Deep Dive (The "How-to")

### 2.1 Core Logic

Next.js 14+ App Router ประกอบด้วย:

1. **File-Based Routing** - Routes จาก directory structure
2. **Server Components** - Components ที่ทำงานบน server
3. **Client Components** - Components ที่ทำงานบน client
4. **Streaming** - Progressive rendering ด้วย Suspense
5. **Server Actions** - Functions ที่ทำงานบน server
6. **Route Handlers** - API routes ที่ทำงานบน server
7. **Middleware** - Intercept requests และ responses

### 2.2 Architecture Diagram Requirements

```
┌─────────────────────────────────────────────────────────┐
│              Next.js 14+ App Router Architecture       │
├─────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Client Layer                           │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  Browser    │  │  Client     │  │  React    │  │   │
│  │  │  APIs      │  │  Components│  │  Hooks    │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Server Layer                           │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  Server     │  │  Route      │  │  Server   │  │   │
│  │  │  Components│  │  Handlers   │  │  Actions  │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  Streaming  │  │  Caching    │  │  Middleware│  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Data Layer                            │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  Database   │  │  External   │  │  File     │  │   │
│  │  │  Access    │  │  APIs       │  │  System   │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Runtime Layer                         │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  Edge       │  │  Node.js    │  │  Serverless│  │   │
│  │  │  Runtime   │  │  Runtime    │  │  Functions│  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
└─────────────────────────────────────────────────────────┘
```

### 2.3 Implementation Workflow

**Step 1: Setup App Router Structure**

```typescript
// app/layout.tsx - Root Layout
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'My App',
  description: 'A Next.js application',
}

export default function RootLayout({
  children
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
```

---

## 3. Tooling & Tech Stack

### 3.1 Enterprise Tools

| Tool | Purpose | Version | License |
|------|---------|---------|---------|
| Next.js | React Framework | ^14.0.0 | MIT |
| React | UI Library | ^18.0.0 | MIT |
| TypeScript | Type Safety | ^5.0.0 | Apache 2.0 |
| Tailwind CSS | Styling | ^3.0.0 | MIT |
| Zod | Schema Validation | ^3.0.0 | MIT |

### 3.2 Configuration Essentials

**TypeScript Configuration:**
```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "lib": ["DOM", "DOM.Iterable", "ESNext"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "target": "ES2020",
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```

**Next.js Configuration:**
```typescript
// next.config.ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  images: {
    domains: ['example.com'],
  },
  experimental: {
    serverActions: {
      bodySizeLimit: '2mb',
    },
  },
}

export default nextConfig
```

---

## 4. Standards, Compliance & Security

### 4.1 International Standards

- **WCAG 2.1 Level AA** - Accessibility สำหรับทุก users
- **ISO 9241-11** - Usability Standards
- **GDPR** - Data Protection สำหรับ User Data
- **PCI DSS** - Security Standards สำหรับ Payment

### 4.2 Security Protocol

Next.js ต้องปฏิบัติตามหลักความปลอดภัย:

1. **Input Validation** - Validate ข้อมูลทั้ง client และ server
2. **CSRF Protection** - ใช้ built-in CSRF protection
3. **Secure Headers** - ใช้ security headers ที่เหมาะสม
4. **Rate Limiting** - จำกัดจำนวน requests ต่อผู้ใช้

```typescript
// middleware.ts - Security Headers
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const response = NextResponse.next()
  
  // Security headers
  response.headers.set('X-Frame-Options', 'DENY')
  response.headers.set('X-Content-Type-Options', 'nosniff')
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin')
  response.headers.set('Permissions-Policy', 'camera=(), microphone=(), geolocation=()')
  
  return response
}
```

### 4.3 Explainability

Next.js ต้องสามารถอธิบายได้ว่า:

1. **Routing Logic** - ทำไม route ถูก match อย่างไร
2. **Data Fetching** - ทำไม data ถูก fetch เมื่อไร
3. **Caching Strategy** - ทำไม cache ถูกใช้งานอย่างไร
4. **Error Handling** - ทำไม error ถูก handle อย่างไร

---

## 5. Unit Economics & Performance Metrics (KPIs)

### 5.1 Cost Calculation

| Metric | Calculation | Target |
|--------|-------------|--------|
| Time to First Byte (TTFB) | Server response time | < 200ms |
| First Contentful Paint (FCP) | First paint time | < 1.8s |
| Largest Contentful Paint (LCP) | Largest element paint | < 2.5s |
| Cumulative Layout Shift (CLS) | Layout stability | < 0.1 |
| Time to Interactive (TTI) | Interactive time | < 3.8s |

### 5.2 Key Performance Indicators

**Technical Metrics:**

1. **Core Web Vitals** - LCP, FID, CLS
2. **Bundle Size** - JavaScript bundle ที่ใช้งาน
3. **Server Response Time** - Server response time
4. **Cache Hit Rate** - Cache hit rate

**Business Metrics:**

1. **Conversion Rate** - อัตราการแปลงผู้ใช้
2. **Bounce Rate** - อัตราการออกจากหน้า
3. **User Engagement** - Engagement time
4. **SEO Rankings** - Search engine rankings

---

## 6. Strategic Recommendations (CTO Insights)

### 6.1 Phase Rollout

**Phase 1: Foundation (Week 1-2)**
- Setup Next.js project
- Configure TypeScript and ESLint
- Setup routing structure
- Implement basic layouts

**Phase 2: Data Fetching (Week 3-4)**
- Implement Server Components
- Add data fetching patterns
- Setup caching strategies
- Implement streaming

**Phase 3: Advanced Features (Week 5-6)**
- Add Server Actions
- Implement Route Handlers
- Setup Middleware
- Add error handling

**Phase 4: Production (Week 7-8)**
- Performance optimization
- Security hardening
- Analytics integration
- Documentation and training

### 6.2 Pitfalls to Avoid

1. **Overusing Client Components** - ไม่ใช้ Client Components มากเกินไป
2. **Poor Caching** - ไม่ใช้ caching อย่างเหมาะสม
3. **Ignoring SEO** - ไม่คำนึงถึง SEO
4. **Security Issues** - ไม่ implement security measures
5. **Performance Issues** - ไม่ optimize performance
6. **Accessibility Issues** - ไม่คำนึงถึง accessibility

### 6.3 Best Practices Checklist

- [ ] ใช้ Server Components โดย default
- [ ] Implement caching strategies อย่างเหมาะสม
- [ ] ใช้ Suspense สำหรับ streaming
- [ ] Implement error boundaries
- [ ] ใช้ loading states
- [ ] Optimize images ด้วย next/image
- [ ] ใช้ TypeScript สำหรับ type safety
- [ ] Implement security headers
- [ ] ใช้ middleware สำหรับ auth
- [ ] Optimize bundle size
- [ ] Test บนทุก browsers และ devices
- [ ] Monitor Core Web Vitals
- [ ] Implement analytics tracking
- [ ] คำนึงถึง accessibility
- [ ] Document API routes

---

## 7. Implementation Examples

### 7.1 App Router Structure and Conventions

**Directory Structure:**
```
app/
├── (auth)/              # Route group - doesn't affect URL
│   ├── login/
│   │   └── page.tsx
│   └── register/
│       └── page.tsx
├── (dashboard)/         # Route group
│   ├── layout.tsx       # Shared layout for this group
│   ├── page.tsx         # /dashboard
│   ├── settings/
│   │   └── page.tsx
│   └── users/
│       └── page.tsx
├── api/                 # Route handlers
│   ├── users/
│   │   └── route.ts
│   └── webhooks/
│       └── route.ts
├── layout.tsx           # Root layout
├── page.tsx             # Home page (/)
├── loading.tsx          # Loading UI
├── error.tsx            # Error UI
├── not-found.tsx        # 404 UI
├── globals.css          # Global styles
└── favicon.ico
```

**File Conventions:**
- `page.tsx` - Route page component
- `layout.tsx` - Layout component (wraps child routes)
- `loading.tsx` - Loading UI for Suspense boundaries
- `error.tsx` - Error boundary UI
- `not-found.tsx` - 404 page
- `route.ts` - API route handler
- `template.tsx` - Like layout but remounts on navigation

### 7.2 Server Components vs Client Components

**Server Components (Default):**
```typescript
// Default - Server Component
import { db } from '@/lib/db'

export default async function UserList() {
  const users = await db.user.findMany()
  
  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  )
}
```

**When to use Server Components:**
- Fetching data directly from database/API
- Accessing backend resources (files, environment variables)
- Keeping sensitive data on server
- Reducing client-side JavaScript bundle

**Client Components:**
```typescript
'use client'

import { useState } from 'react'

export default function Counter() {
  const [count, setCount] = useState(0)
  
  return (
    <button onClick={() => setCount(c => c + 1)}>
      Count: {count}
    </button>
  )
}
```

**When to use Client Components:**
- Using React hooks (useState, useEffect, etc.)
- Browser APIs (window, document, localStorage)
- Event handlers (onClick, onChange, etc.)
- State management libraries (Zustand, Redux)

**Component Composition Pattern:**
```typescript
// Server Component
import { db } from '@/lib/db'
import { UserList } from './UserList' // Client Component

export default async function UsersPage() {
  const users = await db.user.findMany()
  
  return <UserList users={users} />
}

// UserList.tsx - Client Component
'use client'

import { useState } from 'react'

type UserListProps = {
  users: Array<{ id: string; name: string }>
}

export function UserList({ users }: UserListProps) {
  const [filter, setFilter] = useState('')
  
  const filtered = users.filter(u => 
    u.name.toLowerCase().includes(filter.toLowerCase())
  )
  
  return (
    <div>
      <input 
        value={filter} 
        onChange={e => setFilter(e.target.value)}
        placeholder="Search users..."
      />
      <ul>
        {filtered.map(user => (
          <li key={user.id}>{user.name}</li>
        ))}
      </ul>
    </div>
  )
}
```

### 7.3 Data Fetching Patterns

**Server Components Data Fetching:**
```typescript
// app/users/page.tsx
import { db } from '@/lib/db'

// Static generation with revalidation
export const revalidate = 3600 // Revalidate every hour

export default async function UsersPage() {
  const users = await db.user.findMany({
    orderBy: { createdAt: 'desc' }
  })
  
  return (
    <div>
      <h1>Users</h1>
      <UserList users={users} />
    </div>
  )
}
```

**Client Components Data Fetching:**
```typescript
'use client'

import { useEffect, useState } from 'react'

type User = {
  id: string
  name: string
  email: string
}

export function UsersFetcher() {
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)
  
  useEffect(() => {
    async function fetchUsers() {
      try {
        const res = await fetch('/api/users')
        const data = await res.json()
        setUsers(data)
      } catch (error) {
        console.error('Failed to fetch users:', error)
      } finally {
        setLoading(false)
      }
    }
    
    fetchUsers()
  }, [])
  
  if (loading) return <div>Loading...</div>
  
  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  )
}
```

**Streaming and Suspense:**
```typescript
// app/dashboard/page.tsx
import { Suspense } from 'react'
import { UserStats } from './UserStats'
import { RecentActivity } from './RecentActivity'

export default function DashboardPage() {
  return (
    <div>
      <h1>Dashboard</h1>
      
      <Suspense fallback={<StatsSkeleton />}>
        <UserStats />
      </Suspense>
      
      <Suspense fallback={<ActivitySkeleton />}>
        <RecentActivity />
      </Suspense>
    </div>
  )
}

function StatsSkeleton() {
  return (
    <div className="grid grid-cols-3 gap-4">
      {[1, 2, 3].map(i => (
        <div key={i} className="h-32 bg-gray-200 animate-pulse" />
      ))}
    </div>
  )
}

function ActivitySkeleton() {
  return (
    <div className="space-y-4">
      {[1, 2, 3, 4, 5].map(i => (
        <div key={i} className="h-16 bg-gray-200 animate-pulse" />
      ))}
    </div>
  )
}
```

### 7.4 Caching Strategies

**force-cache (Default):**
```typescript
// Cached until manually revalidated
export default async function ProductsPage() {
  const products = await fetch('https://api.example.com/products', {
    cache: 'force-cache' // Default
  }).then(res => res.json())
  
  return <ProductList products={products} />
}
```

**no-store:**
```typescript
// Always fetch fresh data
export default async function LivePricePage() {
  const prices = await fetch('https://api.example.com/prices', {
    cache: 'no-store'
  }).then(res => res.json())
  
  return <PriceList prices={prices} />
}
```

**revalidate (Time-based):**
```typescript
// Revalidate every 60 seconds
export const revalidate = 60

export default async function ArticlesPage() {
  const articles = await db.article.findMany()
  return <ArticleList articles={articles} />
}

// Or per-request
export default async function ProductsPage() {
  const products = await fetch('https://api.example.com/products', {
    next: { revalidate: 3600 } // 1 hour
  }).then(res => res.json())
  
  return <ProductList products={products} />
}
```

**on-demand Revalidation:**
```typescript
// app/api/revalidate/route.ts
import { revalidatePath, revalidateTag } from 'next/cache'
import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  const { path, tag } = await request.json()
  
  if (path) {
    revalidatePath(path)
  }
  
  if (tag) {
    revalidateTag(tag)
  }
  
  return NextResponse.json({ revalidated: true })
}

// Usage with tags
export default async function ProductsPage() {
  const products = await fetch('https://api.example.com/products', {
    next: { tags: ['products'] }
  }).then(res => res.json())
  
  return <ProductList products={products} />
}
```

### 7.5 API Routes (Route Handlers)

**Basic Route Handler:**
```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { db } from '@/lib/db'

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams
  const page = parseInt(searchParams.get('page') || '1')
  const limit = parseInt(searchParams.get('limit') || '10')
  
  const users = await db.user.findMany({
    skip: (page - 1) * limit,
    take: limit
  })
  
  return NextResponse.json({ users, page, limit })
}

export async function POST(request: NextRequest) {
  const body = await request.json()
  
  const user = await db.user.create({
    data: {
      name: body.name,
      email: body.email
    }
  })
  
  return NextResponse.json(user, { status: 201 })
}
```

**Dynamic Route Handler:**
```typescript
// app/api/users/[id]/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { db } from '@/lib/db'

type RouteContext = {
  params: { id: string }
}

export async function GET(
  request: NextRequest,
  context: RouteContext
) {
  const user = await db.user.findUnique({
    where: { id: context.params.id }
  })
  
  if (!user) {
    return NextResponse.json(
      { error: 'User not found' },
      { status: 404 }
    )
  }
  
  return NextResponse.json(user)
}

export async function PATCH(
  request: NextRequest,
  context: RouteContext
) {
  const body = await request.json()
  
  const user = await db.user.update({
    where: { id: context.params.id },
    data: body
  })
  
  return NextResponse.json(user)
}

export async function DELETE(
  request: NextRequest,
  context: RouteContext
) {
  await db.user.delete({
    where: { id: context.params.id }
  })
  
  return new NextResponse(null, { status: 204 })
}
```

### 7.6 Server Actions

**Basic Server Action:**
```typescript
// app/actions.ts
'use server'

import { db } from '@/lib/db'
import { revalidatePath } from 'next/cache'

export async function createUser(formData: FormData) {
  const name = formData.get('name') as string
  const email = formData.get('email') as string
  
  const user = await db.user.create({
    data: { name, email }
  })
  
  revalidatePath('/users')
  return user
}

export async function deleteUser(id: string) {
  await db.user.delete({ where: { id } })
  revalidatePath('/users')
}
```

**Server Action with Validation:**
```typescript
// app/actions.ts
'use server'

import { z } from 'zod'
import { db } from '@/lib/db'

const createUserSchema = z.object({
  name: z.string().min(2),
  email: z.string().email()
})

export async function createUser(prevState: any, formData: FormData) {
  const validatedFields = createUserSchema.safeParse({
    name: formData.get('name'),
    email: formData.get('email')
  })
  
  if (!validatedFields.success) {
    return {
      errors: validatedFields.error.flatten().fieldErrors,
      message: 'Missing Fields. Failed to Create User.'
    }
  }
  
  const { name, email } = validatedFields.data
  
  try {
    await db.user.create({ data: { name, email } })
    return { message: 'User created successfully' }
  } catch (error) {
    return { message: 'Database Error: Failed to Create User.' }
  }
}
```

### 7.7 Middleware

**Basic Middleware:**
```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Check for auth token
  const token = request.cookies.get('token')
  
  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }
  
  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/protected/:path*']
}
```

**Middleware with Response Headers:**
```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const response = NextResponse.next()
  
  // Add custom headers
  response.headers.set('x-custom-header', 'value')
  
  // Add CORS headers
  response.headers.set('Access-Control-Allow-Origin', '*')
  response.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
  response.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization')
  
  return response
}
```

### 7.8 Performance Optimization

**Dynamic Imports:**
```typescript
'use client'

import dynamic from 'next/dynamic'

// Dynamically import heavy components
const HeavyChart = dynamic(() => import('@/components/HeavyChart'), {
  loading: () => <p>Loading chart...</p>,
  ssr: false // Disable server-side rendering
})

const Modal = dynamic(() => import('@/components/Modal'), {
  loading: () => null
})

export default function DashboardPage() {
  return (
    <div>
      <h1>Dashboard</h1>
      <HeavyChart />
      <Modal />
    </div>
  )
}
```

**Image Optimization:**
```typescript
import Image from 'next/image'

export default function ProductImage() {
  return (
    <Image
      src="/product.jpg"
      alt="Product"
      width={500}
      height={500}
      priority // Above the fold
      placeholder="blur"
      blurDataURL="data:image/jpeg;base64,..."
    />
  )
}
```

**Font Optimization:**
```typescript
import { Inter, Roboto } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap'
})

const roboto = Roboto({
  weight: ['400', '700'],
  subsets: ['latin'],
  variable: '--font-roboto',
  display: 'swap'
})

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html className={`${inter.variable} ${roboto.variable}`}>
      <body>{children}</body>
    </html>
  )
}
```

### 7.9 Best Practices

**Routing:**
- Use Server Components by default
- Implement proper error boundaries
- Use loading states for better UX
- Optimize route structure

**Data Fetching:**
- Use caching strategies appropriately
- Implement streaming with Suspense
- Fetch data as close to where it's used
- Use Server Actions for mutations

**Performance:**
- Use dynamic imports for heavy components
- Optimize images with next/image
- Use font optimization
- Monitor Core Web Vitals

**Security:**
- Implement proper authentication
- Use security headers
- Validate all inputs
- Sanitize user data

**Accessibility:**
- Use semantic HTML
- Implement keyboard navigation
- Add ARIA labels where needed
- Test with screen readers

---

## 8. Related Skills

- `02-frontend/react-best-practices`
- `02-frontend/state-management`
- `03-backend-api/express-rest`
- `03-backend-api/fastapi-patterns`
- `26-deployment-strategies`
