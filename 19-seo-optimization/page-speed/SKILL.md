# Page Speed Optimization

## Overview

Page speed is a critical ranking factor and user experience metric. This guide covers comprehensive page speed optimization techniques.

---

## 1. Why Page Speed Matters

### Impact on SEO

```markdown
# Page Speed Impact on SEO

## Google Ranking Factor
- **Direct Ranking Factor**: Page speed is a ranking signal
- **Mobile-First**: Especially important for mobile search
- **Core Web Vitals**: LCP, FID, CLS are ranking factors
- **User Experience**: Fast sites rank higher

## Search Engine Crawling
- **Crawl Budget**: Faster pages get crawled more often
- **Indexing**: Faster pages are indexed faster
- **Freshness**: Updated content is discovered sooner
- **Crawl Depth**: Faster sites get deeper crawling

## User Experience
- **Bounce Rate**: Faster pages have lower bounce rates
- **Conversion Rate**: Faster pages convert better
- **User Satisfaction**: Faster pages have happier users
- **Mobile Users**: Speed is critical for mobile
```

### Impact on User Experience

```markdown
# Page Speed Impact on UX

## User Expectations
- **2 Seconds**: Users expect pages to load in 2 seconds
- **3 Seconds**: 40% of users abandon after 3 seconds
- **5 Seconds**: 74% of users abandon after 5 seconds
- **10 Seconds**: Almost all users abandon after 10 seconds

## Conversion Impact
- **1 Second Delay**: 7% decrease in conversions
- **2 Second Delay**: 12% decrease in conversions
- **3 Second Delay**: 18% decrease in conversions
- **4 Second Delay**: 24% decrease in conversions

## Bounce Rate Impact
- **1-2 Seconds**: 9% bounce rate
- **2-3 Seconds**: 18% bounce rate
- **3-4 Seconds**: 32% bounce rate
- **4+ Seconds**: 50%+ bounce rate
```

---

## 2. Measurement Tools

### Lighthouse

```markdown
# Lighthouse

## What is Lighthouse?
Automated tool for improving web page quality.

## How to Use
1. Open Chrome DevTools
2. Go to Lighthouse tab
3. Click "Generate report"
4. Review results

## Scores
- **Performance**: 0-100 score
- **Accessibility**: 0-100 score
- **Best Practices**: 0-100 score
- **SEO**: 0-100 score

## Audits
- **Metrics**: LCP, FID, CLS, FCP, TTI, TBT, Speed Index
- **Opportunities**: Suggestions for improvement
- **Diagnostics**: Issues to investigate
- **Passed Audits**: Things you're doing right
```

### PageSpeed Insights

```markdown
# PageSpeed Insights

## What is PageSpeed Insights?
Google's tool for measuring page speed.

## Features
- **Lab Data**: Controlled environment testing
- **Field Data**: Real user experience data
- **Mobile Testing**: Test on mobile devices
- **Desktop Testing**: Test on desktop devices
- **Recommendations**: Specific suggestions

## How to Use
1. Go to https://pagespeed.web.dev/
2. Enter URL
3. Click "Analyze"
4. Review results

## Scores
- **0-49**: Poor
- **50-89**: Needs Improvement
- **90-100**: Good

## Metrics
- **LCP**: Largest Contentful Paint
- **FID**: First Input Delay
- **CLS**: Cumulative Layout Shift
- **FCP**: First Contentful Paint
- **TTI**: Time to Interactive
- **TBT**: Total Blocking Time
- **Speed Index**: Overall speed score
```

### WebPageTest

```markdown
# WebPageTest

## What is WebPageTest?
Advanced tool for web performance testing.

## Features
- **Multiple Locations**: Test from different locations
- **Multiple Browsers**: Test on different browsers
- **Multiple Devices**: Test on different devices
- **Waterfall View**: Visual representation of load
- **Video Capture**: Video of page loading

## How to Use
1. Go to https://www.webpagetest.org/
2. Enter URL
3. Select test location
4. Select browser
5. Click "Start Test"

## Metrics
- **Load Time**: Total page load time
- **First Byte**: Time to first byte
- **Start Render**: Time to first render
- **Speed Index**: Overall speed score
- **Requests**: Number of requests
- **Bytes In**: Total bytes downloaded
```

---

## 3. Optimization Techniques

### Code Splitting

```typescript
// Dynamic import for code splitting
// Lazy load components
const Component = React.lazy(() => import('./Component'))

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Component />
    </Suspense>
  )
}

// Route-based code splitting (Next.js)
// app/page.tsx
// Automatically code splits by route

// Component-based code splitting
const HeavyComponent = React.lazy(() => import('./HeavyComponent'))

function Page() {
  return (
    <div>
      <Suspense fallback={<div>Loading...</div>}>
        <HeavyComponent />
      </Suspense>
    </div>
  )
}
```

### Lazy Loading

```html
<!-- Lazy load images -->
<img src="placeholder.jpg"
     data-src="image.jpg"
     loading="lazy"
     alt="Description">

<!-- Lazy load iframes -->
<iframe
  src="about:blank"
  data-src="https://example.com/embed"
  loading="lazy"
></iframe>

<!-- Lazy load videos -->
<video
  src="video.mp4"
  preload="none"
  loading="lazy"
></video>
```

### Image Optimization

```typescript
// Next.js Image component
import Image from 'next/image'

export default function Page() {
  return (
    <div>
      <Image
        src="/image.jpg"
        alt="Description"
        width={800}
        height={600}
        loading="lazy"
      />
    </div>
  )
}

// Responsive images
<Image
  src="/image.jpg"
  alt="Description"
  width={800}
  height={600}
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
  loading="lazy"
/>

// Modern image formats
<picture>
  <source type="image/webp" srcset="image.webp">
  <source type="image/avif" srcset="image.avif">
  <img src="image.jpg" alt="Description" loading="lazy">
</picture>
```

### Font Optimization

```typescript
// Next.js font optimization
import { Inter } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
})

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={inter.className}>
      <body>{children}</body>
    </html>
  )
}

// Font display strategies
// swap: Text is shown immediately with fallback font
// optional: Text is hidden until font loads
// fallback: Text is shown with fallback font, then swapped
// block: Text is hidden until font loads
```

### CSS Optimization

```css
/* Minify CSS */
/* Remove comments */
/* Remove whitespace */
/* Optimize selectors */
/* Use shorthand properties */

/* Critical CSS */
/* Inline critical CSS */
/* Load non-critical CSS asynchronously */

/* CSS best practices */
/* Avoid @import */
/* Use efficient selectors */
/* Minimize specificity */
/* Use CSS Grid/Flexbox instead of floats */
```

### JavaScript Optimization

```typescript
// Minify JavaScript
// Remove comments
// Remove whitespace
// Shorten variable names
// Remove dead code

// Code splitting
// Lazy load components
// Dynamic imports
// Route-based splitting

// Optimize bundle size
// Tree shaking
// Remove unused code
// Use smaller libraries

// Optimize execution
// Use requestAnimationFrame
// Use Web Workers
// Use async/await
// Avoid blocking operations
```

---

## 4. Caching Strategies

### Browser Caching

```apache
# Apache .htaccess
<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresByType image/jpg "access plus 1 year"
    ExpiresByType image/jpeg "access plus 1 year"
    ExpiresByType image/gif "access plus 1 year"
    ExpiresByType image/png "access plus 1 year"
    ExpiresByType image/webp "access plus 1 year"
    ExpiresByType text/css "access plus 1 month"
    ExpiresByType application/javascript "access plus 1 month"
    ExpiresByType application/json "access plus 1 month"
</IfModule>
```

```nginx
# Nginx
location ~* \.(jpg|jpeg|gif|png|webp|css|js)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### CDN Caching

```markdown
# CDN Caching

## CDN Configuration
- **Cache-Control Headers**: Set appropriate headers
- **Cache Keys**: Configure cache keys
- **Cache Rules**: Set cache rules
- **Purge**: Configure cache purging

## Cache Headers
```http
Cache-Control: public, max-age=31536000, immutable
Cache-Control: public, max-age=3600, s-maxage=86400
Cache-Control: no-cache, no-store, must-revalidate
```

## CDN Best Practices
- Use CDN for static assets
- Set appropriate cache headers
- Use cache versioning
- Implement cache purging
- Monitor cache hit rate
```

### Service Worker Caching

```typescript
// Service Worker for caching
const CACHE_NAME = 'v1'
const urlsToCache = [
  '/',
  '/styles/main.css',
  '/scripts/main.js',
]

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(urlsToCache)
    })
  )
})

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request)
    })
  )
})
```

---

## 5. CDN Usage

### CDN Configuration

```markdown
# CDN Configuration

## Popular CDNs
- **Cloudflare**: Free tier available
- **AWS CloudFront**: AWS integration
- **Google Cloud CDN**: Google Cloud integration
- **Azure CDN**: Azure integration
- **Fastly**: Enterprise CDN
- **Akamai**: Enterprise CDN

## CDN Setup
1. Sign up for CDN service
2. Add your domain
3. Configure DNS
4. Upload assets
5. Configure caching rules
6. Test CDN

## CDN Best Practices
- Use CDN for all static assets
- Configure cache headers
- Use HTTP/2 or HTTP/3
- Enable compression
- Use edge caching
- Monitor performance
```

### CDN Integration

```typescript
// Next.js with CDN
// next.config.ts
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'cdn.example.com',
        pathname: '/images/**',
      },
    ],
  },
  assetPrefix: 'https://cdn.example.com',
}

export default nextConfig

// CDN for images
<Image
  src="https://cdn.example.com/image.jpg"
  alt="Description"
  width={800}
  height={600}
/>
```

---

## 6. Resource Hints

### Preload

```html
<!-- Preload critical resources -->
<link rel="preload" href="/styles/main.css" as="style">
<link rel="preload" href="/scripts/main.js" as="script">
<link rel="preload" href="/font.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/image.jpg" as="image">

<!-- Preload with media query -->
<link rel="preload" href="/mobile.css" as="style" media="(max-width: 768px)">
```

### Prefetch

```html
<!-- Prefetch next page resources -->
<link rel="prefetch" href="/page2.js">
<link rel="prefetch" href="/page2.css">

<!-- Prefetch DNS -->
<link rel="dns-prefetch" href="https://cdn.example.com">
```

### Preconnect

```html
<!-- Preconnect to important origins -->
<link rel="preconnect" href="https://api.example.com">
<link rel="preconnect" href="https://cdn.example.com">

<!-- Preconnect with crossorigin -->
<link rel="preconnect" href="https://fonts.googleapis.com" crossorigin>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
```

---

## 7. Third-Party Script Optimization

### Third-Party Script Management

```markdown
# Third-Party Script Optimization

## Common Issues
- **Blocking Scripts**: Block page rendering
- **Large Scripts**: Slow down page load
- **Multiple Scripts**: Too many requests
- **Unoptimized Scripts**: Not minified or bundled
- **Tracking Scripts**: Analytics and marketing scripts

## Optimization Strategies

### 1. Defer Non-Critical Scripts
```html
<script defer src="/script.js"></script>
```

### 2. Async Load Scripts
```html
<script async src="/script.js"></script>
```

### 3. Load Scripts Dynamically
```typescript
// Load script when needed
function loadScript(src: string) {
  const script = document.createElement('script')
  script.src = src
  script.async = true
  document.body.appendChild(script)
}

// Load script on user interaction
document.addEventListener('click', () => {
  loadScript('/analytics.js')
}, { once: true })
```

### 4. Use Tag Managers
```html
<!-- Google Tag Manager -->
<noscript>
  <iframe
    src="https://www.googletagmanager.com/ns.html?id=GTM_ID"
    height="0"
    width="0"
    style="display:none;visibility:hidden"
  />
</noscript>
```

### 5. Optimize Third-Party Scripts
- Use lightweight alternatives
- Remove unused scripts
- Defer non-critical scripts
- Use script loading strategies
- Monitor script performance
```

---

## 8. Next.js Specific Optimizations

### Next.js Optimization Techniques

```typescript
// next.config.ts
const nextConfig = {
  // Enable compression
  compress: true,

  // Optimize images
  images: {
    formats: ['image/avif', 'image/webp'],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
  },

  // Optimize fonts
  optimizeFonts: true,

  // Enable SWC minification
  swcMinify: true,

  // Enable React strict mode
  reactStrictMode: true,

  // Enable production source maps
  productionBrowserSourceMaps: false,

  // Optimize CSS
  optimizeCss: true,

  // Enable experimental features
  experimental: {
    optimizeCss: true,
    optimizePackageImports: ['lucide-react'],
  },
}

export default nextConfig
```

### ISR for Performance

```typescript
// app/page.tsx
// Revalidate every hour
export const revalidate = 3600

// Tag-based revalidation
export const revalidate = {
  tags: ['homepage'],
}

// On-demand revalidation
// app/api/revalidate/route.ts
import { revalidateTag } from 'next/cache'

export async function POST() {
  revalidateTag('homepage')
  return Response.json({ revalidated: true })
}
```

---

## 9. Performance Budgets

### Setting Performance Budgets

```typescript
// .eslintrc.json
{
  "rules": {
    "next/next-img-inline-script": "error",
    "next/next-script-for-gtm": "error",
    "next/next-img-inline-script": "error"
  }
}

// next.config.ts
const nextConfig = {
  experimental: {
    // Set performance budgets
    optimizeCss: true,
    optimizePackageImports: ['lucide-react'],
  },
}

export default nextConfig
```

### Performance Budget Tools

```markdown
# Performance Budget Tools

## Lighthouse CI
- **Purpose**: Enforce performance budgets in CI/CD
- **Features**:
  - Run Lighthouse tests
  - Set budget thresholds
  - Fail builds if budgets exceeded
  - Generate reports

## Webpack Bundle Analyzer
- **Purpose**: Analyze bundle size
- **Features**:
  - Visualize bundle size
  - Identify large modules
  - Find optimization opportunities

## Bundlephobia
- **Purpose**: Analyze bundle size
- **Features**:
  - Analyze bundle size
  - Compare to benchmarks
  - Identify optimization opportunities
```

---

## 10. Monitoring

### Performance Monitoring

```typescript
// Web Vitals monitoring
import { onCLS, onFID, onFCP, onLCP, onTTFB } from 'web-vitals'

export function reportWebVitals(metric) {
  // Send to analytics
  fetch('/api/analytics', {
    method: 'POST',
    body: JSON.stringify(metric),
  })
}

onCLS(reportWebVitals)
onFID(reportWebVitals)
onFCP(reportWebVitals)
onLCP(reportWebVitals)
onTTFB(reportWebVitals)
```

### Real User Monitoring (RUM)

```typescript
// RUM implementation
import { getCLS, getFID, getLCP } from 'web-vitals'

export function collectWebVitals() {
  const vitals = {
    cls: getCLS(),
    fid: getFID(),
    lcp: getLCP(),
  }

  // Send to analytics
  navigator.sendBeacon('/api/vitals', JSON.stringify(vitals))
}

// Call on page load
if (typeof window !== 'undefined') {
  collectWebVitals()
}
```

---

## Best Practices

### Page Speed Best Practices

```markdown
# Page Speed Best Practices

## 1. Optimize Images
- Use modern formats (WebP, AVIF)
- Compress images
- Use responsive images
- Lazy load images
- Use CDN for images

## 2. Minify Resources
- Minify CSS
- Minify JavaScript
- Minify HTML
- Remove comments
- Remove whitespace

## 3. Use Caching
- Set appropriate cache headers
- Use CDN
- Use service workers
- Cache critical resources
- Implement cache invalidation

## 4. Optimize Code
- Use code splitting
- Lazy load components
- Remove unused code
- Use tree shaking
- Optimize bundle size

## 5. Use Resource Hints
- Preload critical resources
- Prefetch next page resources
- Preconnect to important origins
- Use DNS prefetch

## 6. Optimize Third-Party Scripts
- Defer non-critical scripts
- Async load scripts
- Remove unused scripts
- Use lightweight alternatives
- Monitor script performance

## 7. Monitor Performance
- Track Core Web Vitals
- Monitor page load times
- Analyze performance data
- Identify performance issues
- Optimize based on data

## 8. Test Regularly
- Use Lighthouse
- Use PageSpeed Insights
- Test on different devices
- Test on different networks
- Test on different browsers

## 9. Set Performance Budgets
- Define budget thresholds
- Monitor budget compliance
- Fail builds if exceeded
- Optimize if exceeded

## 10. Stay Updated
- Follow performance blogs
- Learn about new techniques
- Test new optimizations
- Share knowledge with team
```
