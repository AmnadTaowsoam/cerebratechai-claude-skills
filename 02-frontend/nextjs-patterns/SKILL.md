# Next.js 14+ App Router Patterns

## 1. App Router Structure and Conventions

### Directory Structure
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

### File Conventions
- `page.tsx` - Route page component
- `layout.tsx` - Layout component (wraps child routes)
- `loading.tsx` - Loading UI for Suspense boundaries
- `error.tsx` - Error boundary UI
- `not-found.tsx` - 404 page
- `route.ts` - API route handler
- `template.tsx` - Like layout but remounts on navigation

## 2. Server Components vs Client Components

### Server Components (Default)
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

### Client Components
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

### Component Composition Pattern
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

## 3. Data Fetching Patterns

### Server Components Data Fetching
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

### Client Components Data Fetching
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

### Streaming and Suspense
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

### Streaming with fetch
```typescript
// app/dashboard/UserStats.tsx
export async function UserStats() {
  // This will stream the response
  const stats = await fetch('https://api.example.com/stats', {
    cache: 'no-store'
  }).then(res => res.json())
  
  return (
    <div className="grid grid-cols-3 gap-4">
      <StatCard label="Users" value={stats.users} />
      <StatCard label="Revenue" value={stats.revenue} />
      <StatCard label="Orders" value={stats.orders} />
    </div>
  )
}
```

## 4. Caching Strategies

### force-cache (Default)
```typescript
// Cached until manually revalidated
export default async function ProductsPage() {
  const products = await fetch('https://api.example.com/products', {
    cache: 'force-cache' // Default
  }).then(res => res.json())
  
  return <ProductList products={products} />
}
```

### no-store
```typescript
// Always fetch fresh data
export default async function LivePricePage() {
  const prices = await fetch('https://api.example.com/prices', {
    cache: 'no-store'
  }).then(res => res.json())
  
  return <PriceList prices={prices} />
}
```

### revalidate (Time-based)
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

### on-demand Revalidation
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

### Route Handlers Caching
```typescript
// app/api/products/route.ts
import { NextResponse } from 'next/server'

export const dynamic = 'force-dynamic' // Disable caching

export async function GET() {
  const products = await db.product.findMany()
  return NextResponse.json(products)
}

// Or with revalidation
export const revalidate = 300 // 5 minutes

export async function GET() {
  const products = await db.product.findMany()
  return NextResponse.json(products)
}
```

## 5. API Routes (Route Handlers)

### Basic Route Handler
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

### Dynamic Route Handler
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

### Route Handler with CORS
```typescript
// app/api/webhook/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function OPTIONS(request: NextRequest) {
  return new NextResponse(null, {
    status: 204,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization'
    }
  })
}

export async function POST(request: NextRequest) {
  const body = await request.json()
  
  // Process webhook...
  
  return NextResponse.json({ received: true })
}
```

## 6. Metadata API

### Static Metadata
```typescript
// app/about/page.tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'About Us',
  description: 'Learn more about our company',
  openGraph: {
    title: 'About Us',
    description: 'Learn more about our company',
    images: ['/og-image.jpg']
  }
}

export default function AboutPage() {
  return <div>About page content</div>
}
```

### Dynamic Metadata
```typescript
// app/blog/[slug]/page.tsx
import type { Metadata } from 'next'
import { db } from '@/lib/db'

type Props = {
  params: { slug: string }
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const post = await db.post.findUnique({
    where: { slug: params.slug }
  })
  
  return {
    title: post?.title || 'Blog Post',
    description: post?.excerpt || '',
    openGraph: {
      title: post?.title,
      description: post?.excerpt,
      images: post?.coverImage ? [post.coverImage] : []
    }
  }
}

export default async function BlogPostPage({ params }: Props) {
  const post = await db.post.findUnique({
    where: { slug: params.slug }
  })
  
  return <article>{post?.content}</article>
}
```

### Root Layout Metadata
```typescript
// app/layout.tsx
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: {
    default: 'My App',
    template: '%s | My App'
  },
  description: 'A Next.js application',
  icons: {
    icon: '/favicon.ico',
    apple: '/apple-icon.png'
  },
  manifest: '/manifest.json',
  themeColor: '#000000'
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

## 7. Loading and Error States

### Loading UI
```typescript
// app/dashboard/loading.tsx
export default function DashboardLoading() {
  return (
    <div className="space-y-6">
      <div className="h-8 w-64 bg-gray-200 animate-pulse rounded" />
      <div className="grid grid-cols-3 gap-4">
        {[1, 2, 3].map(i => (
          <div key={i} className="h-32 bg-gray-200 animate-pulse rounded" />
        ))}
      </div>
    </div>
  )
}
```

### Error UI
```typescript
// app/dashboard/error.tsx
'use client'

import { useEffect } from 'react'

type ErrorProps = {
  error: Error & { digest?: string }
  reset: () => void
}

export default function DashboardError({ error, reset }: ErrorProps) {
  useEffect(() => {
    console.error('Dashboard error:', error)
  }, [error])
  
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h2 className="text-2xl font-bold mb-4">Something went wrong!</h2>
      <p className="text-gray-600 mb-4">{error.message}</p>
      <button
        onClick={reset}
        className="px-4 py-2 bg-blue-500 text-white rounded"
      >
        Try again
      </button>
    </div>
  )
}
```

### Global Error UI
```typescript
// app/global-error.tsx
'use client'

export default function GlobalError({
  error,
  reset
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <html>
      <body>
        <div className="flex flex-col items-center justify-center min-h-screen">
          <h2 className="text-3xl font-bold mb-4">Application Error</h2>
          <button onClick={reset}>Reset application</button>
        </div>
      </body>
    </html>
  )
}
```

### Not Found UI
```typescript
// app/not-found.tsx
import Link from 'next/link'

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h2 className="text-4xl font-bold mb-4">404 - Page Not Found</h2>
      <p className="text-gray-600 mb-4">
        The page you're looking for doesn't exist.
      </p>
      <Link
        href="/"
        className="px-4 py-2 bg-blue-500 text-white rounded"
      >
        Go Home
      </Link>
    </div>
  )
}
```

## 8. Route Groups and Layouts

### Route Groups
```typescript
// app/(marketing)/about/page.tsx - /about
// app/(marketing)/contact/page.tsx - /contact
// app/(auth)/login/page.tsx - /login
// app/(auth)/register/page.tsx - /register

// Group layouts
// app/(marketing)/layout.tsx - Applies to about and contact
export default function MarketingLayout({
  children
}: {
  children: React.ReactNode
}) {
  return (
    <div>
      <MarketingHeader />
      <main>{children}</main>
      <MarketingFooter />
    </div>
  )
}
```

### Nested Layouts
```typescript
// app/layout.tsx - Root layout
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <body>
        <Navbar />
        {children}
        <Footer />
      </body>
    </html>
  )
}

// app/dashboard/layout.tsx - Dashboard layout
export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex">
      <Sidebar />
      <main className="flex-1">{children}</main>
    </div>
  )
}

// app/dashboard/settings/layout.tsx - Settings sub-layout
export default function SettingsLayout({ children }: { children: React.ReactNode }) {
  return (
    <div>
      <SettingsNav />
      {children}
    </div>
  )
}
```

### Template vs Layout
```typescript
// layout.tsx - Preserves state across navigation
export default function Layout({ children }: { children: React.ReactNode }) {
  return <div>{children}</div>
}

// template.tsx - Remounts on navigation (useful for animations)
export default function Template({ children }: { children: React.ReactNode }) {
  return <div className="animate-in">{children}</div>
}
```

## 9. Parallel and Intercepting Routes

### Parallel Routes
```typescript
// app/dashboard/@analytics/page.tsx - /dashboard
// app/dashboard/@settings/page.tsx - /dashboard

// app/dashboard/layout.tsx
export default function DashboardLayout({
  children,
  analytics,
  settings
}: {
  children: React.ReactNode
  analytics: React.ReactNode
  settings: React.ReactNode
}) {
  return (
    <div className="grid grid-cols-12 gap-4">
      <div className="col-span-8">{children}</div>
      <div className="col-span-4 space-y-4">
        {analytics}
        {settings}
      </div>
    </div>
  )
}
```

### Intercepting Routes
```typescript
// app/photo/[id]/page.tsx - Regular photo page
// app/(.)photo/[id]/page.tsx - Intercepted modal (same URL)
// app/(..)photo/[id]/page.tsx - Intercepted modal (one level up)
// app/(...)photo/[id]/page.tsx - Intercepted modal (root level)

// app/(.)photo/[id]/page.tsx
import { useRouter } from 'next/navigation'

export default function PhotoModal({ params }: { params: { id: string } }) {
  const router = useRouter()
  
  return (
    <div className="fixed inset-0 bg-black/80 flex items-center justify-center">
      <div className="bg-white p-4 rounded-lg">
        <img src={`/photos/${params.id}.jpg`} alt="Photo" />
        <button onClick={() => router.back()}>Close</button>
      </div>
    </div>
  )
}
```

## 10. Server Actions

### Basic Server Action
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

### Server Action with Validation
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

### Using Server Actions in Forms
```typescript
'use client'

import { useFormState, useFormStatus } from 'react-dom'
import { createUser } from '@/app/actions'

function SubmitButton() {
  const { pending } = useFormStatus()
  
  return (
    <button disabled={pending} type="submit">
      {pending ? 'Creating...' : 'Create User'}
    </button>
  )
}

export function CreateUserForm() {
  const [state, formAction] = useFormState(createUser, null)
  
  return (
    <form action={formAction}>
      <input name="name" type="text" placeholder="Name" />
      {state?.errors?.name && (
        <p className="text-red-500">{state.errors.name[0]}</p>
      )}
      
      <input name="email" type="email" placeholder="Email" />
      {state?.errors?.email && (
        <p className="text-red-500">{state.errors.email[0]}</p>
      )}
      
      <SubmitButton />
      
      {state?.message && (
        <p className="text-green-500">{state.message}</p>
      )}
    </form>
  )
}
```

### Server Actions with Direct Invocation
```typescript
'use client'

import { createUser } from '@/app/actions'

export function CreateUserButton() {
  const handleClick = async () => {
    await createUser({
      name: 'John Doe',
      email: 'john@example.com'
    })
  }
  
  return <button onClick={handleClick}>Create User</button>
}
```

## 11. Middleware

### Basic Middleware
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

### Middleware with Response Headers
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

### Middleware with Locale
```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

const locales = ['en', 'th', 'ja']
const defaultLocale = 'en'

export function middleware(request: NextRequest) {
  const pathname = request.nextUrl.pathname
  
  // Check if there is any supported locale in the pathname
  const pathnameIsMissingLocale = locales.every(
    locale => !pathname.startsWith(`/${locale}/`) && pathname !== `/${locale}`
  )
  
  // Redirect if there is no locale
  if (pathnameIsMissingLocale) {
    return NextResponse.redirect(
      new URL(`/${defaultLocale}${pathname}`, request.url)
    )
  }
  
  return NextResponse.next()
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)']
}
```

## 12. Performance Optimization

### Dynamic Imports
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

### Image Optimization
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

### Font Optimization
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

### Script Optimization
```typescript
import Script from 'next/script'

export default function Analytics() {
  return (
    <>
      <Script
        src="https://www.googletagmanager.com/gtag/js"
        strategy="afterInteractive"
      />
      <Script id="google-analytics" strategy="afterInteractive">
        {`
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
          gtag('config', 'GA_MEASUREMENT_ID');
        `}
      </Script>
    </>
  )
}
```

### Preloading Data
```typescript
// app/dashboard/page.tsx
import { Suspense } from 'react'

async function getData() {
  const res = await fetch('https://api.example.com/data', {
    next: { revalidate: 60 }
  })
  return res.json()
}

export default async function DashboardPage() {
  // Start fetching data early
  const dataPromise = getData()
  
  return (
    <div>
      <h1>Dashboard</h1>
      <Suspense fallback={<Loading />}>
        <DashboardContent dataPromise={dataPromise} />
      </Suspense>
    </div>
  )
}

async function DashboardContent({ dataPromise }: { dataPromise: Promise<any> }) {
  const data = await dataPromise
  return <div>{/* Render data */}</div>
}
```

### Route Segment Config
```typescript
// app/products/page.tsx

// Disable caching
export const dynamic = 'force-dynamic'

// Set runtime
export const runtime = 'edge' // or 'nodejs'

// Set revalidation time
export const revalidate = 3600

// Set fetch cache
export const fetchCache = 'force-no-store'

export default async function ProductsPage() {
  const products = await fetch('https://api.example.com/products', {
    cache: 'no-store'
  }).then(res => res.json())
  
  return <ProductList products={products} />
}
```
