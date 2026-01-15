# Next.js SEO

## Overview

Next.js provides excellent SEO capabilities out of the box. This guide covers all aspects of SEO optimization in Next.js applications.

---

## 1. Next.js SEO Advantages

### Why Next.js is Great for SEO

```markdown
# Next.js SEO Advantages

## 1. Server-Side Rendering (SSR)
- Content is rendered on the server
- Search engines can crawl content easily
- Faster initial page load
- Better Core Web Vitals

## 2. Static Site Generation (SSG)
- Pre-rendered at build time
- Instant page loads
- Perfect for static content
- CDN-ready

## 3. Incremental Static Regeneration (ISR)
- Static pages with dynamic updates
- Best of both worlds
- Fast loading with fresh content
- Reduced server load

## 4. Built-in Optimization
- Automatic code splitting
- Image optimization
- Font optimization
- Prefetching

## 5. Metadata API
- Type-safe metadata
- Dynamic metadata generation
- Social media optimization
- Structured data support

## 6. File-Based Routing
- Clean URLs
- Automatic sitemap generation
- Easy robots.txt creation
- Built-in routing
```

---

## 2. Metadata API

### Static Metadata

```typescript
// app/layout.tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'My Website',
  description: 'A description of my website',
  keywords: ['nextjs', 'seo', 'react'],
  authors: [{ name: 'John Doe' }],
  creator: 'John Doe',
  publisher: 'John Doe',
  
  // Open Graph
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://example.com',
    title: 'My Website',
    description: 'A description of my website',
    siteName: 'My Website',
    images: [
      {
        url: 'https://example.com/og.jpg',
        width: 1200,
        height: 630,
        alt: 'My Website',
      },
    ],
  },
  
  // Twitter
  twitter: {
    card: 'summary_large_image',
    title: 'My Website',
    description: 'A description of my website',
    images: ['https://example.com/og.jpg'],
    creator: '@johndoe',
  },
  
  // Icons
  icons: {
    icon: '/favicon.ico',
    shortcut: '/favicon-16x16.png',
    apple: '/apple-touch-icon.png',
  },
  
  // Manifest
  manifest: '/manifest.json',
  
  // Verification
  verification: {
    google: 'google-site-verification-code',
    yandex: 'yandex-verification-code',
  },
  
  // Other
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
```

### Dynamic Metadata

```typescript
// app/products/[id]/page.tsx
import type { Metadata } from 'next'

type Props = {
  params: { id: string }
}

// Generate metadata for dynamic routes
export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const product = await getProduct(params.id)
  
  return {
    title: product.name,
    description: product.description,
    keywords: product.tags,
    
    openGraph: {
      title: product.name,
      description: product.description,
      images: [
        {
          url: product.image,
          width: 1200,
          height: 630,
          alt: product.name,
        },
      ],
    },
    
    twitter: {
      title: product.name,
      description: product.description,
      images: [product.image],
    },
  }
}

export default async function ProductPage({ params }: Props) {
  const product = await getProduct(params.id)
  
  return (
    <div>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
    </div>
  )
}
```

### Metadata Resolving

```typescript
// Metadata from child routes override parent metadata
// app/layout.tsx (parent)
export const metadata: Metadata = {
  title: 'My Website',
  description: 'Parent description',
}

// app/about/page.tsx (child)
export const metadata: Metadata = {
  title: 'About Us', // Overrides parent title
  // Inherits parent description
}
```

---

## 3. generateMetadata Function

### Advanced Metadata Generation

```typescript
// app/blog/[slug]/page.tsx
import type { Metadata, ResolvingMetadata } from 'next'

type Props = {
  params: { slug: string }
}

// Generate metadata with parent metadata
export async function generateMetadata(
  { params }: Props,
  parent: ResolvingMetadata
): Promise<Metadata> {
  const post = await getPost(params.slug)
  const previousImages = (await parent).openGraph?.images || []
  
  return {
    title: post.title,
    description: post.excerpt,
    alternates: {
      canonical: `https://example.com/blog/${post.slug}`,
      languages: {
        'en-US': `https://example.com/en/blog/${post.slug}`,
        'es-ES': `https://example.com/es/blog/${post.slug}`,
      },
    },
    openGraph: {
      title: post.title,
      description: post.excerpt,
      url: `https://example.com/blog/${post.slug}`,
      siteName: 'My Blog',
      images: [
        {
          url: post.featuredImage,
          width: 1200,
          height: 630,
          alt: post.title,
        },
        ...previousImages,
      ],
      type: 'article',
      publishedTime: post.publishedAt,
      modifiedTime: post.updatedAt,
      authors: [post.author.name],
    },
    twitter: {
      card: 'summary_large_image',
      title: post.title,
      description: post.excerpt,
      images: [post.featuredImage],
      creator: post.author.twitter,
    },
  }
}
```

### Conditional Metadata

```typescript
// app/[locale]/page.tsx
import type { Metadata } from 'next'

type Props = {
  params: { locale: string }
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const isDefaultLocale = params.locale === 'en'
  
  return {
    title: isDefaultLocale ? 'Home' : 'Inicio',
    description: isDefaultLocale 
      ? 'Welcome to our website'
      : 'Bienvenido a nuestro sitio web',
    alternates: {
      canonical: `https://example.com/${params.locale}`,
      languages: {
        'en': 'https://example.com/en',
        'es': 'https://example.com/es',
        'fr': 'https://example.com/fr',
      },
    },
  }
}
```

---

## 4. JSON-LD Structured Data

### Implementing JSON-LD in Next.js

```typescript
// app/products/[id]/page.tsx
import { Product } from 'schema-dts'

type Props = {
  params: { id: string }
}

export default async function ProductPage({ params }: Props) {
  const product = await getProduct(params.id)
  
  const jsonLd: Product = {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: product.name,
    image: product.images,
    description: product.description,
    sku: product.sku,
    brand: {
      '@type': 'Brand',
      name: product.brand,
    },
    offers: {
      '@type': 'Offer',
      url: `https://example.com/products/${product.id}`,
      priceCurrency: 'USD',
      price: product.price,
      availability: product.inStock
        ? 'https://schema.org/InStock'
        : 'https://schema.org/OutOfStock',
    },
    aggregateRating: product.rating
      ? {
          '@type': 'AggregateRating',
          ratingValue: product.rating,
          reviewCount: product.reviewCount,
        }
      : undefined,
  }
  
  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <div>
        <h1>{product.name}</h1>
        <p>{product.description}</p>
      </div>
    </>
  )
}
```

### Article Schema

```typescript
// app/blog/[slug]/page.tsx
import { Article } from 'schema-dts'

type Props = {
  params: { slug: string }
}

export default async function BlogPage({ params }: Props) {
  const post = await getPost(params.slug)
  
  const jsonLd: Article = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: post.title,
    image: post.featuredImage,
    datePublished: post.publishedAt,
    dateModified: post.updatedAt,
    author: {
      '@type': 'Person',
      name: post.author.name,
      url: post.author.url,
    },
    publisher: {
      '@type': 'Organization',
      name: 'My Blog',
      logo: {
        '@type': 'ImageObject',
        url: 'https://example.com/logo.png',
      },
    },
    description: post.excerpt,
  }
  
  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <article>
        <h1>{post.title}</h1>
        <p>{post.content}</p>
      </article>
    </>
  )
}
```

### Breadcrumb Schema

```typescript
// app/products/[category]/[id]/page.tsx
import { BreadcrumbList } from 'schema-dts'

type Props = {
  params: { category: string; id: string }
}

export default async function ProductPage({ params }: Props) {
  const product = await getProduct(params.id)
  const category = await getCategory(params.category)
  
  const jsonLd: BreadcrumbList = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      {
        '@type': 'ListItem',
        position: 1,
        name: 'Home',
        item: 'https://example.com',
      },
      {
        '@type': 'ListItem',
        position: 2,
        name: category.name,
        item: `https://example.com/products/${category.slug}`,
      },
      {
        '@type': 'ListItem',
        position: 3,
        name: product.name,
        item: `https://example.com/products/${category.slug}/${product.slug}`,
      },
    ],
  }
  
  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <div>
        <nav aria-label="Breadcrumb">
          <ol>
            <li><a href="/">Home</a></li>
            <li><a href={`/products/${category.slug}`}>{category.name}</a></li>
            <li>{product.name}</li>
          </ol>
        </nav>
        <h1>{product.name}</h1>
      </div>
    </>
  )
}
```

---

## 5. Dynamic Sitemap Generation

### Creating a Sitemap

```typescript
// app/sitemap.ts
import { MetadataRoute } from 'next'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = 'https://example.com'
  
  // Get all pages
  const pages = await getAllPages()
  
  // Get all products
  const products = await getAllProducts()
  
  // Get all blog posts
  const posts = await getAllPosts()
  
  return [
    {
      url: baseUrl,
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 1,
    },
    ...pages.map((page) => ({
      url: `${baseUrl}/${page.slug}`,
      lastModified: page.updatedAt,
      changeFrequency: 'weekly' as const,
      priority: 0.8,
    })),
    ...products.map((product) => ({
      url: `${baseUrl}/products/${product.slug}`,
      lastModified: product.updatedAt,
      changeFrequency: 'daily' as const,
      priority: 0.9,
    })),
    ...posts.map((post) => ({
      url: `${baseUrl}/blog/${post.slug}`,
      lastModified: post.publishedAt,
      changeFrequency: 'weekly' as const,
      priority: 0.7,
    })),
  ]
}
```

### Sitemap with Multiple Sitemaps

```typescript
// app/sitemap.ts
import { MetadataRoute } from 'next'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = 'https://example.com'
  
  // For very large sites, use sitemap index
  return [
    {
      url: `${baseUrl}/sitemap-products.xml`,
      lastModified: new Date(),
    },
    {
      url: `${baseUrl}/sitemap-blog.xml`,
      lastModified: new Date(),
    },
  ]
}

// app/sitemap-products.xml/route.ts
export async function GET() {
  const products = await getAllProducts()
  const baseUrl = 'https://example.com'
  
  const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${products
  .map(
    (product) => `  <url>
    <loc>${baseUrl}/products/${product.slug}</loc>
    <lastmod>${product.updatedAt.toISOString()}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.9</priority>
  </url>`
  )
  .join('\n')}
</urlset>`
  
  return new Response(sitemap, {
    headers: {
      'Content-Type': 'application/xml',
      'Cache-Control': 'public, s-maxage=3600, stale-while-revalidate=86400',
    },
  })
}
```

### Dynamic Sitemap with Pagination

```typescript
// app/sitemap.ts
import { MetadataRoute } from 'next'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = 'https://example.com'
  const products = await getAllProducts()
  const productsPerPage = 20
  const totalPages = Math.ceil(products.length / productsPerPage)
  
  const urls: MetadataRoute.Sitemap = [
    {
      url: baseUrl,
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 1,
    },
  ]
  
  // Add paginated product pages
  for (let page = 1; page <= totalPages; page++) {
    urls.push({
      url: `${baseUrl}/products?page=${page}`,
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 0.8,
    })
  }
  
  return urls
}
```

---

## 6. Robots.txt Generation

### Creating Robots.txt

```typescript
// app/robots.ts
import { MetadataRoute } from 'next'

export default function robots(): MetadataRoute.Robots {
  const baseUrl = 'https://example.com'
  
  return {
    rules: [
      {
        userAgent: '*',
        allow: '/',
        disallow: ['/api/', '/admin/', '/private/'],
      },
      {
        userAgent: 'Googlebot',
        allow: '/',
        disallow: ['/private/'],
      },
    ],
    sitemap: `${baseUrl}/sitemap.xml`,
  }
}
```

### Dynamic Robots.txt

```typescript
// app/robots.ts
import { MetadataRoute } from 'next'

export default async function robots(): Promise<MetadataRoute.Robots> {
  const baseUrl = 'https://example.com'
  const blockedPaths = await getBlockedPaths()
  
  return {
    rules: [
      {
        userAgent: '*',
        allow: '/',
        disallow: ['/api/', '/admin/', ...blockedPaths],
      },
    ],
    sitemap: `${baseUrl}/sitemap.xml`,
    host: baseUrl,
  }
}
```

### Environment-Specific Robots.txt

```typescript
// app/robots.ts
import { MetadataRoute } from 'next'

export default function robots(): MetadataRoute.Robots {
  const baseUrl = 'https://example.com'
  const isProduction = process.env.NODE_ENV === 'production'
  
  return {
    rules: [
      {
        userAgent: '*',
        allow: isProduction ? '/' : '',
        disallow: isProduction ? ['/api/', '/admin/'] : '/',
      },
    ],
    sitemap: isProduction ? `${baseUrl}/sitemap.xml` : undefined,
  }
}
```

---

## 7. Image Optimization

### Using Next.js Image Component

```typescript
import Image from 'next/image'

export default function ProductPage() {
  return (
    <div>
      <Image
        src="/product.jpg"
        alt="Product description"
        width={800}
        height={600}
        priority
      />
    </div>
  )
}
```

### Dynamic Images

```typescript
import Image from 'next/image'

type Props = {
  params: { id: string }
}

export default async function ProductPage({ params }: Props) {
  const product = await getProduct(params.id)
  
  return (
    <div>
      <Image
        src={product.image}
        alt={product.name}
        width={800}
        height={600}
        priority
      />
    </div>
  )
}
```

### Responsive Images

```typescript
import Image from 'next/image'

export default function ProductPage() {
  return (
    <div>
      <Image
        src="/product.jpg"
        alt="Product description"
        width={800}
        height={600}
        sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
        priority
      />
    </div>
  )
}
```

### Remote Images

```typescript
// next.config.ts
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'example.com',
        pathname: '/images/**',
      },
    ],
  },
}

export default nextConfig

// app/page.tsx
import Image from 'next/image'

export default function Page() {
  return (
    <Image
      src="https://example.com/images/product.jpg"
      alt="Product description"
      width={800}
      height={600}
    />
  )
}
```

---

## 8. Font Optimization

### Using next/font

```typescript
// app/layout.tsx
import { Inter } from 'next/font/google'
import localFont from 'next/font/local'

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
})

const myFont = localFont({
  src: './my-font.woff2',
  variable: '--font-my-font',
  display: 'swap',
})

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={`${inter.variable} ${myFont.variable}`}>
      <body className={inter.className}>{children}</body>
    </html>
  )
}
```

### Multiple Fonts

```typescript
// app/layout.tsx
import { Inter, Roboto } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
})

const roboto = Roboto({
  weight: ['400', '700'],
  subsets: ['latin'],
  variable: '--font-roboto',
  display: 'swap',
})

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={`${inter.variable} ${roboto.variable}`}>
      <body className={inter.className}>{children}</body>
    </html>
  )
}
```

---

## 9. Link Prefetching

### Using Link Component

```typescript
import Link from 'next/link'

export default function Navigation() {
  return (
    <nav>
      <Link href="/" prefetch={true}>Home</Link>
      <Link href="/about" prefetch={true}>About</Link>
      <Link href="/contact" prefetch={true}>Contact</Link>
    </nav>
  )
}
```

### Conditional Prefetching

```typescript
import Link from 'next/link'

export default function Navigation() {
  return (
    <nav>
      <Link href="/" prefetch>Home</Link>
      <Link href="/about" prefetch={false}>About</Link>
      <Link href="/contact" prefetch={false}>Contact</Link>
    </nav>
  )
}
```

### Prefetching on Hover

```typescript
'use client'

import Link from 'next/link'
import { useState } from 'react'

export default function Navigation() {
  const [hovered, setHovered] = useState(false)
  
  return (
    <nav>
      <Link
        href="/about"
        prefetch={hovered}
        onMouseEnter={() => setHovered(true)}
      >
        About
      </Link>
    </nav>
  )
}
```

---

## 10. ISR for SEO

### Incremental Static Regeneration

```typescript
// app/blog/[slug]/page.tsx
export const revalidate = 3600 // Revalidate every hour

type Props = {
  params: { slug: string }
}

export default async function BlogPage({ params }: Props) {
  const post = await getPost(params.slug)
  
  return (
    <article>
      <h1>{post.title}</h1>
      <p>{post.content}</p>
    </article>
  )
}
```

### On-Demand Revalidation

```typescript
// app/api/revalidate/route.ts
import { revalidatePath } from 'next/cache'
import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  const { path } = await request.json()
  
  revalidatePath(path)
  
  return NextResponse.json({ revalidated: true })
}

// Usage
fetch('/api/revalidate', {
  method: 'POST',
  body: JSON.stringify({ path: '/blog/my-post' }),
})
```

### Tag-Based Revalidation

```typescript
// app/blog/[slug]/page.tsx
export const revalidate = {
  tags: ['blog'],
}

type Props = {
  params: { slug: string }
}

export default async function BlogPage({ params }: Props) {
  const post = await getPost(params.slug)
  
  return (
    <article>
      <h1>{post.title}</h1>
      <p>{post.content}</p>
    </article>
  )
}

// app/api/revalidate/route.ts
import { revalidateTag } from 'next/cache'
import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  revalidateTag('blog')
  
  return NextResponse.json({ revalidated: true })
}
```

---

## 11. App Router SEO Patterns

### SEO Component Pattern

```typescript
// components/SEO.tsx
import { Metadata } from 'next'

type SEOProps = {
  title?: string
  description?: string
  image?: string
  noIndex?: boolean
}

export function SEO({ title, description, image, noIndex }: SEOProps) {
  return (
    <>
      <title>{title}</title>
      <meta name="description" content={description} />
      {image && <meta property="og:image" content={image} />}
      {noIndex && <meta name="robots" content="noindex, nofollow" />}
    </>
  )
}
```

### Head Management

```typescript
// app/layout.tsx
import type { Metadata } from 'next'
import Head from 'next/head'

export const metadata: Metadata = {
  title: {
    default: 'My Website',
    template: '%s | My Website',
  },
  description: 'A description of my website',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" href="/favicon.ico" />
      </head>
      <body>{children}</body>
    </html>
  )
}
```

### Dynamic Head

```typescript
// app/products/[id]/page.tsx
import Head from 'next/head'

type Props = {
  params: { id: string }
}

export default async function ProductPage({ params }: Props) {
  const product = await getProduct(params.id)
  
  return (
    <>
      <Head>
        <title>{product.name}</title>
        <meta name="description" content={product.description} />
        <meta property="og:title" content={product.name} />
        <meta property="og:description" content={product.description} />
        <meta property="og:image" content={product.image} />
      </Head>
      <div>
        <h1>{product.name}</h1>
        <p>{product.description}</p>
      </div>
    </>
  )
}
```

---

## 12. Analytics Integration

### Google Analytics

```typescript
// app/layout.tsx
import GoogleAnalytics from '@/components/GoogleAnalytics'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        {children}
        <GoogleAnalytics />
      </body>
    </html>
  )
}

// components/GoogleAnalytics.tsx
'use client'

import Script from 'next/script'

export default function GoogleAnalytics() {
  return (
    <>
      <Script
        src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"
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

### Google Tag Manager

```typescript
// app/layout.tsx
import GoogleTagManager from '@/components/GoogleTagManager'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <GoogleTagManager />
        {children}
      </body>
    </html>
  )
}

// components/GoogleTagManager.tsx
'use client'

import Script from 'next/script'

export default function GoogleTagManager() {
  return (
    <noscript>
      <iframe
        src={`https://www.googletagmanager.com/ns.html?id=GTM_ID`}
        height="0"
        width="0"
        style={{ display: 'none', visibility: 'hidden' }}
      />
    </noscript>
  )
}

// app/layout.tsx (add this script)
<Script
  id="gtm-script"
  strategy="afterInteractive"
  dangerouslySetInnerHTML={{
    __html: `
      (function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
      new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
      j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
      'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
      })(window,document,'script','dataLayer','GTM_ID');
    `,
  }}
/>
```

---

## 13. SEO Monitoring

### Monitoring Tools

```typescript
// app/api/seo-check/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  const url = request.nextUrl.searchParams.get('url')
  
  if (!url) {
    return NextResponse.json({ error: 'URL required' }, { status: 400 })
  }
  
  // Check various SEO factors
  const checks = {
    title: await checkTitle(url),
    description: await checkDescription(url),
    h1: await checkH1(url),
    canonical: await checkCanonical(url),
    robots: await checkRobots(url),
    sitemap: await checkSitemap(url),
    structuredData: await checkStructuredData(url),
    mobileFriendly: await checkMobileFriendly(url),
    pageSpeed: await checkPageSpeed(url),
  }
  
  return NextResponse.json({ url, checks })
}

async function checkTitle(url: string) {
  // Implementation
  return { present: true, length: 50, optimal: true }
}

async function checkDescription(url: string) {
  // Implementation
  return { present: true, length: 150, optimal: true }
}

async function checkH1(url: string) {
  // Implementation
  return { present: true, count: 1, optimal: true }
}

async function checkCanonical(url: string) {
  // Implementation
  return { present: true, matches: true, optimal: true }
}

async function checkRobots(url: string) {
  // Implementation
  return { accessible: true, valid: true, optimal: true }
}

async function checkSitemap(url: string) {
  // Implementation
  return { accessible: true, valid: true, pages: 100, optimal: true }
}

async function checkStructuredData(url: string) {
  // Implementation
  return { present: true, valid: true, types: ['Organization', 'Article'], optimal: true }
}

async function checkMobileFriendly(url: string) {
  // Implementation
  return { friendly: true, issues: [], optimal: true }
}

async function checkPageSpeed(url: string) {
  // Implementation
  return {
    lcp: 2.1,
    fid: 80,
    cls: 0.05,
    score: 95,
    optimal: true,
  }
}
```

---

## Best Practices

### Next.js SEO Best Practices

1. **Use Server Components by Default**
   - Better for SEO
   - Faster initial load
   - Easier for crawlers

2. **Implement Metadata API**
   - Type-safe metadata
   - Dynamic metadata generation
   - Social media optimization

3. **Optimize Images**
   - Use next/image component
   - Specify dimensions
   - Use appropriate formats
   - Implement lazy loading

4. **Generate Sitemaps**
   - Use dynamic sitemap generation
   - Keep sitemaps updated
   - Submit to search engines

5. **Implement Structured Data**
   - Use JSON-LD format
   - Validate with testing tools
   - Include relevant schema types

6. **Monitor Performance**
   - Track Core Web Vitals
   - Use PageSpeed Insights
   - Monitor regularly

7. **Use ISR for Dynamic Content**
   - Revalidate periodically
   - Use on-demand revalidation
   - Implement tag-based revalidation

8. **Implement Analytics**
   - Track user behavior
   - Monitor SEO metrics
   - Set up goals and events

9. **Test Regularly**
   - Use Google Search Console
   - Test with Rich Results Test
   - Monitor crawl errors

10. **Stay Updated**
    - Follow Next.js updates
    - Read SEO blogs
    - Join communities
