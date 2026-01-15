# Core Web Vitals

## Overview

Core Web Vitals are a set of metrics that measure real-world user experience. They are part of Google's page experience signals.

---

## 1. Core Web Vitals Overview

### What Are Core Web Vitals?

```markdown
# Core Web Vitals Overview

## Definition
Core Web Vitals are the subset of Web Vitals that are most important for user experience.

## Purpose
- Measure real-world user experience
- Provide unified guidance
- Ensure consistent metrics
- Guide performance improvements

## Current Core Web Vitals
- **LCP**: Largest Contentful Paint
- **FID**: First Input Delay (being replaced by INP)
- **CLS**: Cumulative Layout Shift

## Thresholds
- **Good**: 75th percentile of page loads
- **Needs Improvement**: Between good and poor
- **Poor**: Worst 25% of page loads
```

---

## 2. Largest Contentful Paint (LCP)

### What LCP Measures

```markdown
# LCP Overview

## Definition
LCP measures the time from when the user initiates loading the page to when the largest image or text block is rendered within the viewport.

## What It Measures
- The render time of the largest content element
- Largest by size, not importance
- Within the viewport
- Excludes iframes, web fonts, or hidden elements

## Good LCP
- **Good**: < 2.5s
- **Needs Improvement**: 2.5s - 4s
- **Poor**: > 4s

## Common LCP Elements
- Hero images
- Large text blocks
- Background images with text
- Video elements
```

### LCP Optimization

```markdown
# LCP Optimization

## 1. Optimize Images
- Use modern formats (WebP, AVIF)
- Compress images
- Use responsive images
- Lazy load below-the-fold images
- Preload critical images

## 2. Optimize Server Response
- Use CDN
- Optimize server configuration
- Use HTTP/2 or HTTP/3
- Cache responses
- Reduce TTFB

## 3. Remove Blocking Resources
- Defer non-critical CSS
- Defer non-critical JavaScript
- Inline critical CSS
- Use async/defer for scripts

## 4. Optimize Rendering
- Minimize DOM size
- Avoid complex CSS
- Optimize JavaScript execution
- Use efficient CSS selectors

## 5. Preload Critical Resources
```html
<link rel="preload" href="/hero-image.jpg" as="image">
<link rel="preload" href="/critical.css" as="style">
<link rel="preload" href="/critical.js" as="script">
```

## 6. Use Content Delivery Network
- Serve assets from CDN
- Use edge caching
- Use geographic distribution
- Optimize CDN configuration
```

---

## 3. First Input Delay (FID) / Interaction to Next Paint (INP)

### What FID Measures

```markdown
# FID Overview

## Definition
FID measures the time from when a user first interacts with your site to when the browser is able to respond to that interaction.

## What It Measures
- First interaction time
- Browser responsiveness
- Main thread blocking
- JavaScript execution

## Good FID
- **Good**: < 100ms
- **Needs Improvement**: 100ms - 300ms
- **Poor**: > 300ms

## Common Interactions
- Clicking a link
- Tapping a button
- Selecting a checkbox
- Entering text in a field
```

### What INP Measures

```markdown
# INP Overview

## Definition
INP measures the time from when a user first interacts with your site to when the browser is able to respond to that interaction.

## Why INP Replaces FID
- Better measure of interactivity
- Captures all interactions
- More accurate metric
- Better reflects user experience

## Good INP
- **Good**: < 200ms
- **Needs Improvement**: 200ms - 500ms
- **Poor**: > 500ms
```

### FID/INP Optimization

```markdown
# FID/INP Optimization

## 1. Reduce JavaScript Execution
- Code split JavaScript
- Lazy load components
- Use Web Workers
- Remove unused JavaScript

## 2. Minimize Main Thread Work
- Use requestAnimationFrame
- Use setTimeout for non-critical work
- Use Web Workers for heavy computation
- Optimize long tasks

## 3. Defer Non-Critical JavaScript
```html
<script defer src="/non-critical.js"></script>
```

## 4. Use Efficient JavaScript
- Avoid synchronous XHR
- Use async/await
- Avoid blocking operations
- Optimize event handlers

## 5. Optimize Third-Party Scripts
- Defer non-critical scripts
- Load scripts asynchronously
- Remove unused scripts
- Use lightweight alternatives

## 6. Use Web Workers
```javascript
// Offload work to web worker
const worker = new Worker('worker.js')
worker.postMessage(data)
```
```

---

## 4. Cumulative Layout Shift (CLS)

### What CLS Measures

```markdown
# CLS Overview

## Definition
CLS measures the sum total of all individual layout shift scores for every unexpected layout shift that occurs during the entire lifespan of the page.

## What It Measures
- Visual stability
- Layout shifts
- Unexpected movement
- User experience

## Good CLS
- **Good**: < 0.1
- **Needs Improvement**: 0.1 - 0.25
- **Poor**: > 0.25

## CLS Score Formula
```
CLS Score = Impact Fraction × Distance Fraction
```

## Common CLS Causes
- Images without dimensions
- Ads and embeds
- Dynamic content
- Fonts causing layout shift
- DOM injections
```

### CLS Optimization

```markdown
# CLS Optimization

## 1. Reserve Space for Images
```html
<!-- Always include width and height -->
<img src="image.jpg" width="800" height="600" alt="Description">
```

## 2. Reserve Space for Ads
```css
.ad-container {
  min-height: 250px;
  width: 300px;
}
```

## 3. Reserve Space for Embeds
```css
.embed-container {
  aspect-ratio: 16 / 9;
}
```

## 4. Avoid Injected Content
- Don't insert content above existing content
- Use skeleton screens
- Load content in place
- Reserve space for dynamic content

## 5. Use CSS Transitions
```css
.element {
  transition: all 0.3s ease;
}
```

## 6. Font Optimization
```css
/* Use font-display: swap */
@font-face {
  font-family: 'Font Name';
  src: url('font.woff2') format('woff2');
  font-display: swap;
}
```
```

---

## 5. Measurement Tools

### Lighthouse

```markdown
# Lighthouse for Core Web Vitals

## How to Use
1. Open Chrome DevTools
2. Go to Lighthouse tab
3. Click "Generate report"
4. Review Core Web Vitals section

## What It Measures
- LCP with score
- FID/INP with score
- CLS with score
- Overall performance score

## Scoring
- **0-49**: Poor
- **50-89**: Needs Improvement
- **90-100**: Good
```

### PageSpeed Insights

```markdown
# PageSpeed Insights for Core Web Vitals

## How to Use
1. Go to https://pagespeed.web.dev/
2. Enter your URL
3. Click "Analyze"
4. Review Core Web Vitals section

## What It Provides
- Lab data (controlled environment)
- Field data (real user experience)
- Mobile and desktop scores
- Optimization suggestions
```

### Chrome User Experience Report

```markdown
# CrUX Report

## What is CrUX?
Chrome User Experience Report provides real-world user experience data.

## How to Access
1. Go to https://pagespeed.web.dev/crux
2. Enter your URL
3. Review Core Web Vitals data

## What It Provides
- Real user experience data
- Mobile and desktop data
- Geographic distribution
- Device distribution
```

---

## 6. Real User Monitoring (RUM)

### Implementing RUM

```typescript
// Web Vitals monitoring
import { onCLS, onFID, onINP, onLCP } from 'web-vitals'

export function reportWebVitals(metric) {
  // Send to analytics
  fetch('/api/analytics', {
    method: 'POST',
    body: JSON.stringify(metric),
    headers: {
      'Content-Type': 'application/json',
    },
  })
}

// Monitor Core Web Vitals
onCLS(reportWebVitals)
onFID(reportWebVitals)
onINP(reportWebVitals)
onLCP(reportWebVitals)
```

### RUM Best Practices

```markdown
# RUM Best Practices

## 1. Sample Rate
- Don't sample too much (5-10% is typical)
- Sample all for critical pages
- Sample more for performance monitoring
- Sample less for cost optimization

## 2. Data Collection
- Collect all Core Web Vitals
- Collect additional metrics
- Collect user context
- Collect device information

## 3. Data Privacy
- Anonymize data
- Don't collect PII
- Follow privacy regulations
- Get user consent

## 4. Data Analysis
- Aggregate data
- Calculate percentiles
- Identify performance issues
- Track trends over time

## 5. Alerting
- Set up alerts for poor performance
- Alert on threshold breaches
- Alert on sudden degradation
- Alert on performance regressions
```

---

## 7. Lab Data vs Field Data

### Lab Data

```markdown
# Lab Data

## What is Lab Data?
Data collected in a controlled environment using simulated devices and network conditions.

## Tools
- Lighthouse
- WebPageTest
- PageSpeed Insights

## Advantages
- Consistent environment
- Reproducible results
- Detailed diagnostics
- Easy to debug

## Disadvantages
- Not real user experience
- Simulated conditions
- May not reflect real world
- Limited device diversity
```

### Field Data

```markdown
# Field Data

## What is Field Data?
Data collected from real users in the wild.

## Tools
- Chrome User Experience Report
- PageSpeed Insights Field Data
- Real User Monitoring (RUM)

## Advantages
- Real user experience
- Real devices and networks
- Real geographic distribution
- Real usage patterns

## Disadvantages
- Inconsistent conditions
- Not reproducible
- Limited diagnostics
- Harder to debug
```

### Combining Lab and Field Data

```markdown
# Combining Lab and Field Data

## Best Approach
- Use lab data for debugging
- Use field data for monitoring
- Correlate lab and field data
- Optimize based on both

## Workflow
1. Monitor field data
2. Identify performance issues
3. Use lab data to debug
4. Implement fixes
5. Monitor field data again
6. Verify improvements
```

---

## 8. Next.js Optimizations

### Next.js Core Web Vitals

```typescript
// next.config.ts
const nextConfig = {
  // Optimize images
  images: {
    formats: ['image/avif', 'image/webp'],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
  },

  // Optimize fonts
  optimizeFonts: true,

  // Optimize CSS
  optimizeCss: true,

  // Optimize JavaScript
  swcMinify: true,

  // Enable compression
  compress: true,

  // Enable HTTP/2
  http2: true,
}

export default nextConfig
```

### Next.js LCP Optimization

```typescript
// app/layout.tsx
import { Inter } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
})

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={inter.className}>
      <body>{children}</body>
    </html>
  )
}

// app/page.tsx
import Image from 'next/image'
import Link from 'next/link'

export default function HomePage() {
  return (
    <div>
      <Image
        src="/hero.jpg"
        alt="Hero image"
        width={1920}
        height={1080}
        priority
      />
      <Link href="/about" prefetch>About</Link>
    </div>
  )
}
```

### Next.js FID/INP Optimization

```typescript
// Use dynamic imports for code splitting
import dynamic from 'next/dynamic'

const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <div>Loading...</div>,
})

// Use Suspense for lazy loading
import { Suspense } from 'react'

export default function Page() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <HeavyComponent />
    </Suspense>
  )
}
```

### Next.js CLS Optimization

```typescript
// Use next/image with dimensions
import Image from 'next/image'

export default function ProductPage({ product }: { product: Product }) {
  return (
    <div>
      <Image
        src={product.image}
        alt={product.name}
        width={800}
        height={600}
      />
    </div>
  )
}
```

---

## 9. Common Issues and Fixes

### Common LCP Issues

```markdown
# Common LCP Issues and Fixes

## Issue 1: Slow Server Response
**Problem**: High TTFB
**Fix**:
- Use CDN
- Optimize server configuration
- Use HTTP/2 or HTTP/3
- Cache responses

## Issue 2: Large Images
**Problem**: Large hero images
**Fix**:
- Compress images
- Use modern formats
- Use responsive images
- Preload critical images

## Issue 3: Blocking CSS/JS
**Problem**: Resources blocking rendering
**Fix**:
- Inline critical CSS
- Defer non-critical CSS
- Defer non-critical JavaScript
- Use async/defer

## Issue 4: Slow Rendering
**Problem**: Complex DOM/CSS
**Fix**:
- Minimize DOM size
- Optimize CSS
- Reduce JavaScript
- Use efficient selectors
```

### Common FID/INP Issues

```markdown
# Common FID/INP Issues and Fixes

## Issue 1: Large JavaScript Bundle
**Problem**: Too much JavaScript
**Fix**:
- Code split
- Tree shake
- Remove unused code
- Use lighter libraries

## Issue 2: Long Tasks
**Problem**: Blocking main thread
**Fix**:
- Break up long tasks
- Use requestAnimationFrame
- Use Web Workers
- Use setTimeout

## Issue 3: Third-Party Scripts
**Problem**: Blocking scripts
**Fix**:
- Defer non-critical scripts
- Load asynchronously
- Remove unused scripts
- Use lightweight alternatives
```

### Common CLS Issues

```markdown
# Common CLS Issues and Fixes

## Issue 1: Images Without Dimensions
**Problem**: Layout shift when images load
**Fix**:
- Always include width and height
- Use aspect-ratio CSS
- Reserve space for images

## Issue 2: Dynamic Content
**Problem**: Content inserted causing shift
**Fix**:
- Reserve space for dynamic content
- Use skeleton screens
- Load content in place

## Issue 3: Fonts
**Problem**: Font loading causing shift
**Fix**:
- Use font-display: swap
- Preload critical fonts
- Use system fonts as fallback
- Reserve space for text
```

---

## 10. Continuous Monitoring

### Setting Up Monitoring

```typescript
// Web Vitals monitoring setup
import { onCLS, onFID, onINP, onLCP, onTTFB } from 'web-vitals'

// Store metrics
const metrics = {
  lcp: null as number | null,
  fid: null as number | null,
  inp: null as number | null,
  cls: null as number | null,
  ttfb: null as number | null,
}

// Collect metrics
onLCP((metric) => {
  metrics.lcp = metric.value
  reportMetric('lcp', metric)
})

onFID((metric) => {
  metrics.fid = metric.value
  reportMetric('fid', metric)
})

onINP((metric) => {
  metrics.inp = metric.value
  reportMetric('inp', metric)
})

onCLS((metric) => {
  metrics.cls = metric.value
  reportMetric('cls', metric)
})

onTTFB((metric) => {
  metrics.ttfb = metric.value
  reportMetric('ttfb', metric)
})

// Report to analytics
function reportMetric(name: string, metric: any) {
  // Send to your analytics service
  fetch('/api/analytics', {
    method: 'POST',
    body: JSON.stringify({
      name,
      value: metric.value,
      rating: metric.rating,
      delta: metric.delta,
      id: metric.id,
    }),
  })
}
```

### Alerting Setup

```typescript
// Alerting for poor performance
const thresholds = {
  lcp: { good: 2500, needsImprovement: 4000 },
  fid: { good: 100, needsImprovement: 300 },
  inp: { good: 200, needsImprovement: 500 },
  cls: { good: 0.1, needsImprovement: 0.25 },
}

function checkPerformanceMetrics(metrics: any) {
  const alerts = []

  if (metrics.lcp > thresholds.lcp.needsImprovement) {
    alerts.push({
      type: 'lcp',
      severity: metrics.lcp > thresholds.lcp.good ? 'warning' : 'critical',
      value: metrics.lcp,
    })
  }

  if (metrics.fid && metrics.fid > thresholds.fid.needsImprovement) {
    alerts.push({
      type: 'fid',
      severity: metrics.fid > thresholds.fid.good ? 'warning' : 'critical',
      value: metrics.fid,
    })
  }

  if (metrics.inp && metrics.inp > thresholds.inp.needsImprovement) {
    alerts.push({
      type: 'inp',
      severity: metrics.inp > thresholds.inp.good ? 'warning' : 'critical',
      value: metrics.inp,
    })
  }

  if (metrics.cls > thresholds.cls.needsImprovement) {
    alerts.push({
      type: 'cls',
      severity: metrics.cls > thresholds.cls.good ? 'warning' : 'critical',
      value: metrics.cls,
    })
  }

  // Send alerts
  alerts.forEach(alert => {
    sendAlert(alert)
  })
}
```

---

## 11. Best Practices

### Core Web Vitals Best Practices

```markdown
# Core Web Vitals Best Practices

## 1. Monitor Regularly
- Use RUM for real user data
- Use lab data for debugging
- Monitor trends over time
- Set up alerts

## 2. Optimize for Mobile
- Mobile performance is critical
- Test on real devices
- Optimize for slow networks
- Consider mobile constraints

## 3. Focus on User Experience
- Optimize for real users
- Consider different contexts
- Test on different devices
- Test on different networks

## 4. Use Progressive Enhancement
- Start with basic functionality
- Add enhancements progressively
- Ensure core functionality works
- Optimize for slow connections

## 5. Test Across Devices
- Test on mobile devices
- Test on desktop devices
- Test on different browsers
- Test on different networks

## 6. Set Realistic Targets
- Aim for good ratings
- Consider your audience
- Consider your constraints
- Iterate over time

## 7. Prioritize Critical Pages
- Optimize landing pages first
- Optimize checkout pages
- Optimize high-traffic pages
- Optimize conversion pages

## 8. Use Performance Budgets
- Set budget thresholds
- Monitor budget compliance
- Fail builds if exceeded
- Optimize if exceeded

## 9. Stay Updated
- Follow Core Web Vitals updates
- Read performance blogs
- Join communities
- Learn from others

## 10. Iterate and Improve
- Monitor performance
- Identify issues
- Implement fixes
- Verify improvements
```

---

## Quick Reference

### Core Web Vitals Quick Reference

```markdown
# Core Web Vitals Quick Reference

## Metrics and Thresholds

### LCP (Largest Contentful Paint)
- **Good**: < 2.5s
- **Needs Improvement**: 2.5s - 4s
- **Poor**: > 4s

### FID (First Input Delay)
- **Good**: < 100ms
- **Needs Improvement**: 100ms - 300ms
- **Poor**: > 300ms

### INP (Interaction to Next Paint)
- **Good**: < 200ms
- **Needs Improvement**: 200ms - 500ms
- **Poor**: > 500ms

### CLS (Cumulative Layout Shift)
- **Good**: < 0.1
- **Needs Improvement**: 0.1 - 0.25
- **Poor**: > 0.25

## Quick Fixes

### LCP
- Compress images
- Use CDN
- Reduce TTFB
- Preload critical resources

### FID/INP
- Reduce JavaScript
- Defer non-critical scripts
- Use Web Workers
- Break up long tasks

### CLS
- Reserve space for images
- Reserve space for ads
- Avoid injected content
- Use font-display: swap
```
