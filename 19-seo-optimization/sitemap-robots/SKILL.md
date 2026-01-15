# Sitemap and Robots.txt Management

## Overview

Sitemaps and robots.txt are essential files for search engine optimization. They help search engines discover and understand your website structure.

---

## 1. XML Sitemap Structure

### Basic Sitemap Format

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/</loc>
    <lastmod>2023-12-01</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://example.com/about</loc>
    <lastmod>2023-12-01</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://example.com/contact</loc>
    <lastmod>2023-12-01</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.5</priority>
  </url>
</urlset>
```

### Sitemap Elements

```markdown
# Sitemap Elements

## urlset
- **Required**: Root element
- **Namespace**: http://www.sitemaps.org/schemas/sitemap/0.9

## url
- **Required**: Contains URL information
- **Multiple**: Can have multiple url elements

## loc
- **Required**: URL of the page
- **Format**: Absolute URL
- **Encoding**: URL encoded

## lastmod (Optional)
- **Purpose**: Date of last modification
- **Format**: YYYY-MM-DD or ISO 8601
- **Example**: 2023-12-01T00:00:00+00:00

## changefreq (Optional)
- **Purpose**: How frequently page changes
- **Values**: always, hourly, daily, weekly, monthly, yearly, never
- **Note**: Not used by Google

## priority (Optional)
- **Purpose**: Priority relative to other pages
- **Range**: 0.0 to 1.0
- **Note**: Not used by Google
```

---

## 2. Dynamic Sitemap Generation

### Next.js Sitemap Generation

```typescript
// app/sitemap.ts
import { MetadataRoute } from 'next'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = 'https://example.com'
  
  // Get all pages
  const pages = await getAllPages()
  const products = await getAllProducts()
  const posts = await getAllPosts()
  
  return [
    // Homepage
    {
      url: baseUrl,
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 1,
    },
    // Static pages
    ...pages.map((page) => ({
      url: `${baseUrl}/${page.slug}`,
      lastModified: page.updatedAt,
      changeFrequency: 'weekly',
      priority: 0.8,
    })),
    // Products
    ...products.map((product) => ({
      url: `${baseUrl}/products/${product.slug}`,
      lastModified: product.updatedAt,
      changeFrequency: 'daily',
      priority: 0.9,
    })),
    // Blog posts
    ...posts.map((post) => ({
      url: `${baseUrl}/blog/${post.slug}`,
      lastModified: post.publishedAt,
      changeFrequency: 'monthly',
      priority: 0.7,
    })),
  ]
}
```

### Dynamic Sitemap with Database

```typescript
// app/sitemap.ts
import { MetadataRoute } from 'next'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = 'https://example.com'
  
  // Fetch from database
  const products = await db.product.findMany({
    where: { published: true },
    select: {
      id: true,
      slug: true,
      updatedAt: true,
    },
  })
  
  return products.map((product) => ({
    url: `${baseUrl}/products/${product.slug}`,
    lastModified: product.updatedAt,
    changeFrequency: 'daily',
    priority: 0.9,
  }))
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

## 3. Sitemap Index for Large Sites

### Sitemap Index Format

```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://example.com/sitemap-pages.xml</loc>
    <lastmod>2023-12-01</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://example.com/sitemap-products.xml</loc>
    <lastmod>2023-12-01</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://example.com/sitemap-blog.xml</loc>
    <lastmod>2023-12-01</lastmod>
  </sitemap>
</sitemapindex>
```

### Next.js Sitemap Index

```typescript
// app/sitemap.ts
import { MetadataRoute } from 'next'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = 'https://example.com'
  
  return [
    {
      url: `${baseUrl}/sitemap-pages.xml`,
      lastModified: new Date(),
    },
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

// app/sitemap-pages.xml/route.ts
export async function GET() {
  const pages = await getAllPages()
  const baseUrl = 'https://example.com'
  
  const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${pages
  .map(
    (page) => `  <url>
    <loc>${baseUrl}/${page.slug}</loc>
    <lastmod>${page.updatedAt.toISOString()}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
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

---

## 4. Next.js Sitemap Generation

### App Router Sitemap

```typescript
// app/sitemap.ts
import { MetadataRoute } from 'next'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = 'https://example.com'
  
  // Static routes
  const routes = ['', 'about', 'contact', 'blog']
  
  return routes.map((route) => ({
    url: `${baseUrl}/${route}`,
    lastModified: new Date(),
    changeFrequency: 'weekly',
    priority: route === '' ? 1 : 0.8,
  }))
}
```

### Dynamic Routes Sitemap

```typescript
// app/sitemap.ts
import { MetadataRoute } from 'next'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = 'https://example.com'
  
  // Get all slugs
  const posts = await db.post.findMany({
    select: { slug: true, updatedAt: true },
  })
  
  return posts.map((post) => ({
    url: `${baseUrl}/blog/${post.slug}`,
    lastModified: post.updatedAt,
    changeFrequency: 'monthly',
    priority: 0.7,
  }))
}
```

### Multilingual Sitemap

```typescript
// app/[locale]/sitemap.ts
import { MetadataRoute } from 'next'

type Props = {
  params: { locale: string }
}

export default async function sitemap({ params }: Props): Promise<MetadataRoute.Sitemap> {
  const baseUrl = 'https://example.com'
  const { locale } = params
  
  const posts = await getPosts(locale)
  
  return posts.map((post) => ({
    url: `${baseUrl}/${locale}/blog/${post.slug}`,
    lastModified: post.updatedAt,
    changeFrequency: 'monthly',
    priority: 0.7,
    alternates: {
      languages: {
        en: `${baseUrl}/en/blog/${post.slug}`,
        es: `${baseUrl}/es/blog/${post.slug}`,
        fr: `${baseUrl}/fr/blog/${post.slug}`,
      },
    },
  }))
}
```

---

## 5. Robots.txt Syntax

### Basic Robots.txt

```txt
# Allow all bots
User-agent: *
Allow: /

# Block all bots
User-agent: *
Disallow: /

# Block specific paths
User-agent: *
Disallow: /admin/
Disallow: /private/
Disallow: /temp/

# Allow specific bot
User-agent: Googlebot
Allow: /

# Block specific bot
User-agent: *
Disallow: /
```

### Advanced Robots.txt

```txt
# Crawl-delay
User-agent: *
Crawl-delay: 1

# Sitemap location
Sitemap: https://example.com/sitemap.xml

# Multiple sitemaps
Sitemap: https://example.com/sitemap1.xml
Sitemap: https://example.com/sitemap2.xml

# Wildcards
User-agent: *
Disallow: /*.pdf$
Disallow: /admin/*/
Disallow: /temp/*.html

# Allow specific files
User-agent: *
Allow: /public/file.pdf
Disallow: /private/

# Block specific file types
User-agent: *
Disallow: /*.pdf$
Disallow: /*.doc$
```

### Environment-Specific Robots.txt

```typescript
// app/robots.ts
import { MetadataRoute } from 'next'

export default function robots(): MetadataRoute.Robots {
  const isProduction = process.env.NODE_ENV === 'production'
  
  return {
    rules: [
      {
        userAgent: '*',
        allow: isProduction ? '/' : '',
        disallow: isProduction ? ['/api/', '/admin/'] : '/',
      },
    ],
    sitemap: isProduction ? 'https://example.com/sitemap.xml' : undefined,
  }
}
```

---

## 6. Crawl Directives

### User-Agent Directives

```markdown
# User-Agent Directives

## User-agent: *
- Applies to all bots
- Most common directive
- Used for general rules

## User-agent: Googlebot
- Applies only to Googlebot
- Google-specific rules
- Can override general rules

## User-agent: Bingbot
- Applies only to Bingbot
- Bing-specific rules
- Can override general rules

## Common User-Agents
- **Googlebot**: Google's web crawler
- **Bingbot**: Microsoft's web crawler
- **Slurp**: Yahoo's web crawler
- **DuckDuckBot**: DuckDuckGo's web crawler
- **Baiduspider**: Baidu's web crawler
- **YandexBot**: Yandex's web crawler
```

### Allow/Disallow Directives

```markdown
# Allow/Disallow Directives

## Allow
- **Purpose**: Allow crawling of path
- **Format**: Allow: /path/
- **Default**: All paths allowed

## Disallow
- **Purpose**: Block crawling of path
- **Format**: Disallow: /path/
- **Example**: Disallow: /admin/

## Wildcards
- ** ***: Matches any sequence
- **$**: End of URL
- **Examples**:
  - Disallow: /*.pdf$ (blocks all PDFs)
  - Disallow: /admin/* (blocks admin subdirectories)

## Path Matching
- **Exact match**: /admin
- **Prefix match**: /admin/
- **Trailing slash**: Important
```

### Crawl-Delay Directive

```markdown
# Crawl-Delay Directive

## Purpose
- Control crawl rate
- Delay in seconds
- Not supported by all bots

## Format
```txt
User-agent: *
Crawl-delay: 1
```

## Notes
- **Google**: Doesn't support crawl-delay
- **Bing**: Supports crawl-delay
- **Yahoo**: Supports crawl-delay
- **Alternative**: Use Search Console

## Best Practices
- Don't use crawl-delay for Google
- Use server-side rate limiting
- Use Search Console for Google
```

---

## 7. Sitemap Reference in Robots.txt

### Referencing Sitemap

```txt
# Single sitemap
Sitemap: https://example.com/sitemap.xml

# Multiple sitemaps
Sitemap: https://example.com/sitemap1.xml
Sitemap: https://example.com/sitemap2.xml
Sitemap: https://example.com/sitemap3.xml

# Sitemap index
Sitemap: https://example.com/sitemap-index.xml

# Compressed sitemap
Sitemap: https://example.com/sitemap.xml.gz

# Different domain sitemap
Sitemap: https://cdn.example.com/sitemap.xml
```

### Next.js Robots.txt with Sitemap

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
    ],
    sitemap: `${baseUrl}/sitemap.xml`,
    host: baseUrl,
  }
}
```

---

## 8. Dynamic Robots.txt

### Server-Side Robots.txt

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
      {
        userAgent: 'Googlebot',
        allow: '/',
        disallow: ['/private/'],
      },
    ],
    sitemap: `${baseUrl}/sitemap.xml`,
    host: baseUrl,
  }
}
```

### Conditional Robots.txt

```typescript
// app/robots.ts
import { MetadataRoute } from 'next'

export default function robots(): MetadataRoute.Robots {
  const baseUrl = 'https://example.com'
  const isProduction = process.env.NODE_ENV === 'production'
  const isMaintenance = await checkMaintenanceMode()
  
  return {
    rules: [
      {
        userAgent: '*',
        allow: isMaintenance ? '' : isProduction ? '/' : '',
        disallow: isMaintenance ? '/' : isProduction ? ['/api/', '/admin/'] : '/',
      },
    ],
    sitemap: isMaintenance ? undefined : `${baseUrl}/sitemap.xml`,
    host: baseUrl,
  }
}
```

---

## 9. Handling Different Environments

### Environment-Specific Sitemap

```typescript
// app/sitemap.ts
import { MetadataRoute } from 'next'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = process.env.NEXT_PUBLIC_BASE_URL || 'https://example.com'
  const isProduction = process.env.NODE_ENV === 'production'
  
  if (!isProduction) {
    return []
  }
  
  const pages = await getAllPages()
  
  return pages.map((page) => ({
    url: `${baseUrl}/${page.slug}`,
    lastModified: page.updatedAt,
    changeFrequency: 'weekly',
    priority: 0.8,
  }))
}
```

### Environment-Specific Robots.txt

```typescript
// app/robots.ts
import { MetadataRoute } from 'next'

export default function robots(): MetadataRoute.Robots {
  const baseUrl = process.env.NEXT_PUBLIC_BASE_URL || 'https://example.com'
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
    host: baseUrl,
  }
}
```

### Development vs Production

```markdown
# Environment Configuration

## Development
- **Sitemap**: Not needed
- **Robots.txt**: Block all crawlers
- **Purpose**: Prevent indexing

## Staging
- **Sitemap**: Optional
- **Robots.txt**: Block all crawlers
- **Purpose**: Prevent indexing

## Production
- **Sitemap**: Required
- **Robots.txt**: Allow appropriate crawlers
- **Purpose**: Enable indexing
```

---

## 10. Testing and Validation

### Sitemap Testing

```markdown
# Sitemap Testing Tools

## Google Search Console
- **URL**: https://search.google.com/search-console/
- **Features**:
  - Submit sitemaps
  - Check sitemap errors
  - View indexed pages
  - Monitor coverage

## Bing Webmaster Tools
- **URL**: https://www.bing.com/webmasters/
- **Features**:
  - Submit sitemaps
  - Check sitemap errors
  - View indexed pages
  - Monitor coverage

## Online Validators
- **XML Sitemap Validator**: https://www.xml-sitemaps.com/validate-xml-sitemap.html
- **Sitemap Generator**: https://www.xml-sitemaps.com/
- **Sitemap Inspector**: https://www.xml-sitemaps.com/inspect-xml-sitemap.html

## Validation Checklist
- [ ] XML is well-formed
- [ ] All URLs are valid
- [ ] All URLs are accessible
- [ ] No duplicate URLs
- [ ] Lastmod dates are valid
- [ ] Priority values are valid
- [ ] Changefreq values are valid
- [ ] Sitemap size < 50MB
- [ ] URL count < 50,000
```

### Robots.txt Testing

```markdown
# Robots.txt Testing Tools

## Google Robots.txt Tester
- **URL**: https://search.google.com/search-console/robots-tester
- **Features**:
  - Test robots.txt
  - Test specific URLs
  - Check for errors
  - View allowed/disallowed paths

## Online Validators
- **Robots.txt Checker**: https://tools.seobook.com/robots-txt/
- **Robots.txt Validator**: https://technicalseo.com/tools/robots-txt-validator/

## Validation Checklist
- [ ] File is accessible
- [ ] File is at root
- [ ] Syntax is correct
- [ ] User-agent is valid
- [ ] Paths are correct
- [ ] Sitemap is referenced
- [ ] No syntax errors
- [ ] Rules are working as expected
```

---

## 11. Submission to Search Engines

### Google Submission

```markdown
# Submitting to Google

## Method 1: Search Console
1. Go to Google Search Console
2. Select property
3. Go to "Sitemaps"
4. Enter sitemap URL
5. Click "Submit"

## Method 2: Ping
```
GET https://www.google.com/ping?sitemap=https://example.com/sitemap.xml
```

## Method 3: robots.txt
- Add sitemap to robots.txt
- Google will discover automatically

## Best Practices
- Submit main sitemap
- Submit sitemap index
- Monitor coverage report
- Fix errors immediately
```

### Bing Submission

```markdown
# Submitting to Bing

## Method 1: Bing Webmaster Tools
1. Go to Bing Webmaster Tools
2. Add website
3. Verify ownership
4. Go to "Sitemaps"
5. Enter sitemap URL
6. Click "Submit"

## Method 2: Ping
```
GET https://www.bing.com/ping?sitemap=https://example.com/sitemap.xml
```

## Method 3: robots.txt
- Add sitemap to robots.txt
- Bing will discover automatically

## Best Practices
- Submit main sitemap
- Submit sitemap index
- Monitor coverage report
- Fix errors immediately
```

### Other Search Engines

```markdown
# Submitting to Other Search Engines

## Yahoo
- Uses Bing search
- Submit to Bing Webmaster Tools
- No separate submission needed

## DuckDuckGo
- Uses Bing and other sources
- Submit to Bing Webmaster Tools
- No separate submission needed

## Baidu
- Submit to Baidu Webmaster Tools
- URL: http://zhanzhang.baidu.com/
- Requires Baidu account

## Yandex
- Submit to Yandex Webmaster
- URL: https://webmaster.yandex.com/
- Requires Yandex account
```

---

## 12. Best Practices

### Sitemap Best Practices

```markdown
# Sitemap Best Practices

## 1. Keep It Updated
- Update when content changes
- Use automated generation
- Set up regular updates
- Monitor for errors

## 2. Use Correct Format
- Follow XML specification
- Use proper encoding
- Include required elements
- Validate with tools

## 3. Optimize Size
- Keep under 50MB
- Keep under 50,000 URLs
- Use sitemap index for large sites
- Compress if needed

## 4. Include Important Pages
- Homepage
- Category pages
- Product pages
- Blog posts
- Important static pages

## 5. Exclude Unnecessary Pages
- Admin pages
- Login pages
- Search result pages
- Filter pages
- Duplicate content

## 6. Use Absolute URLs
- Include protocol (https://)
- Include domain
- Use full path
- Avoid relative URLs

## 7. Set Appropriate Priority
- Homepage: 1.0
- Category pages: 0.8-0.9
- Product pages: 0.7-0.9
- Blog posts: 0.5-0.7

## 8. Set Appropriate Change Frequency
- Homepage: daily/weekly
- Category pages: weekly
- Product pages: weekly/daily
- Blog posts: monthly/yearly
- Static pages: yearly

## 9. Submit to Search Engines
- Submit to Google Search Console
- Submit to Bing Webmaster Tools
- Submit to other engines
- Monitor coverage

## 10. Monitor Regularly
- Check coverage reports
- Fix errors immediately
- Monitor indexed pages
- Update as needed
```

### Robots.txt Best Practices

```markdown
# Robots.txt Best Practices

## 1. Keep It Simple
- Use clear rules
- Avoid complex patterns
- Test regularly
- Document rules

## 2. Block Only What's Needed
- Don't block CSS/JS
- Don't block images
- Don't block important pages
- Test before blocking

## 3. Use Specific User-Agents
- Use * for general rules
- Use specific bots for specific rules
- Test with different bots
- Monitor bot behavior

## 4. Include Sitemap
- Reference sitemap
- Use absolute URL
- Keep sitemap updated
- Test sitemap

## 5. Test Regularly
- Use Google tester
- Use online validators
- Test with different bots
- Monitor crawl behavior

## 6. Keep It Accessible
- Place at root
- Use correct filename
- Ensure it's accessible
- Check HTTP status

## 7. Use Crawl-Delay Carefully
- Not supported by Google
- Use server-side rate limiting
- Use Search Console
- Monitor crawl rate

## 8. Document Rules
- Comment complex rules
- Explain why blocking
- Keep documentation updated
- Share with team

## 9. Monitor Regularly
- Check crawl stats
- Monitor coverage
- Review logs
- Update as needed

## 10. Stay Updated
- Follow search engine updates
- Read SEO blogs
- Join communities
- Learn from others
```

---

## Quick Reference

### Sitemap Template

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/</loc>
    <lastmod>2023-12-01</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
```

### Robots.txt Template

```txt
User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/
Disallow: /private/

Sitemap: https://example.com/sitemap.xml
```

### Next.js Sitemap

```typescript
// app/sitemap.ts
import { MetadataRoute } from 'next'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = 'https://example.com'
  
  return [
    {
      url: baseUrl,
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 1,
    },
  ]
}
```

### Next.js Robots.txt

```typescript
// app/robots.ts
import { MetadataRoute } from 'next'

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: '*',
        allow: '/',
        disallow: ['/api/', '/admin/'],
      },
    ],
    sitemap: 'https://example.com/sitemap.xml',
  }
}
```
