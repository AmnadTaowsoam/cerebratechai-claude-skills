# Structured Data (Schema.org)

## Overview

Structured data (Schema.org) is a standardized format for providing information about a page and classifying the page content.

---

## 1. Structured Data Concepts

### What is Structured Data?

```markdown
# Structured Data Basics

## Definition
Structured data is code in a specific format that helps search engines understand your content better.

## Benefits
- **Rich Snippets**: Enhanced search result appearance
- **Better Rankings**: Improved understanding of content
- **Higher CTR**: More attractive search results
- **Voice Search**: Better voice search results
- **Knowledge Graph**: Inclusion in Google Knowledge Graph

## Formats
- **JSON-LD**: Recommended by Google
- **Microdata**: HTML5 specification
- **RDFa**: Resource Description Framework

## JSON-LD Format
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Thing",
  "name": "Name of Thing",
  "description": "Description of Thing"
}
</script>
```

## Where to Place
- In the `<head>` section
- After opening `<body>` tag
- In a specific container
- Multiple blocks allowed
```

---

## 2. Schema.org Types

### Article Schema

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Article Title",
  "image": [
    "https://example.com/image-1x1.jpg",
    "https://example.com/image-4x3.jpg"
  ],
  "datePublished": "2023-12-01T00:00:00+00:00",
  "dateModified": "2023-12-01T00:00:00+00:00",
  "author": {
    "@type": "Person",
    "name": "John Doe",
    "url": "https://example.com/authors/john-doe"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Publisher Name",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  },
  "description": "Article description",
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://example.com/article"
  }
}
</script>
```

### BlogPosting Schema

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "Blog Post Title",
  "image": "https://example.com/blog-image.jpg",
  "datePublished": "2023-12-01T00:00:00+00:00",
  "dateModified": "2023-12-01T00:00:00+00:00",
  "author": {
    "@type": "Person",
    "name": "Jane Smith"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Blog Name",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  },
  "description": "Blog post description"
}
</script>
```

### Product Schema

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Product Name",
  "image": [
    "https://example.com/product-1.jpg",
    "https://example.com/product-2.jpg"
  ],
  "description": "Product description",
  "sku": "product-123",
  "brand": {
    "@type": "Brand",
    "name": "Brand Name"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://example.com/product",
    "priceCurrency": "USD",
    "price": "99.99",
    "priceValidUntil": "2023-12-31",
    "availability": "https://schema.org/InStock",
    "seller": {
      "@type": "Organization",
      "name": "Seller Name"
    }
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.5",
    "reviewCount": "125"
  },
  "review": [
    {
      "@type": "Review",
      "reviewRating": {
        "@type": "Rating",
        "ratingValue": "5"
      },
      "author": {
        "@type": "Person",
        "name": "John Doe"
      },
      "reviewBody": "Great product!"
    }
  ]
}
</script>
```

### Organization Schema

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Organization Name",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "description": "Organization description",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main St",
    "addressLocality": "City",
    "addressRegion": "State",
    "postalCode": "12345",
    "addressCountry": "USA"
  },
  "contactPoint": [
    {
      "@type": "ContactPoint",
      "telephone": "+1-555-555-5555",
      "contactType": "customer service"
    },
    {
      "@type": "ContactPoint",
      "email": "contact@example.com",
      "contactType": "customer service"
    }
  ],
  "sameAs": [
    "https://www.facebook.com/example",
    "https://www.twitter.com/example",
    "https://www.linkedin.com/company/example"
  ]
}
</script>
```

### Person Schema

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "John Doe",
  "url": "https://example.com/authors/john-doe",
  "image": "https://example.com/john-doe.jpg",
  "jobTitle": "Software Engineer",
  "worksFor": {
    "@type": "Organization",
    "name": "Company Name"
  },
  "sameAs": [
    "https://www.facebook.com/johndoe",
    "https://www.twitter.com/johndoe",
    "https://www.linkedin.com/in/johndoe"
  ]
}
</script>
```

### BreadcrumbList Schema

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://example.com"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Category",
      "item": "https://example.com/category"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "Product",
      "item": "https://example.com/category/product"
    }
  ]
}
</script>
```

### FAQ Schema

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is your return policy?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "We offer a 30-day return policy for all items in their original condition."
      }
    },
    {
      "@type": "Question",
      "name": "How long does shipping take?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Standard shipping takes 3-5 business days. Express shipping takes 1-2 business days."
      }
    }
  ]
}
</script>
```

### HowTo Schema

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to Optimize Your Website for SEO",
  "description": "A step-by-step guide to optimizing your website for search engines.",
  "image": "https://example.com/how-to-seo.jpg",
  "totalTime": "PT1H",
  "estimatedCost": {
    "@type": "MonetaryAmount",
    "currency": "USD",
    "value": "0"
  },
  "supply": [
    {
      "@type": "HowToSupply",
      "name": "Computer with internet access"
    }
  ],
  "tool": [
    {
      "@type": "HowToTool",
      "name": "Google Search Console"
    }
  ],
  "step": [
    {
      "@type": "HowToStep",
      "name": "Set up Google Search Console",
      "text": "Create an account and verify your website.",
      "image": "https://example.com/step1.jpg"
    },
    {
      "@type": "HowToStep",
      "name": "Submit your sitemap",
      "text": "Upload your XML sitemap to Google Search Console.",
      "image": "https://example.com/step2.jpg"
    },
    {
      "@type": "HowToStep",
      "name": "Monitor your performance",
      "text": "Check your search performance regularly.",
      "image": "https://example.com/step3.jpg"
    }
  ]
}
</script>
```

### Review Schema

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Review",
  "itemReviewed": {
    "@type": "Thing",
    "name": "Product Name"
  },
  "reviewRating": {
    "@type": "Rating",
    "ratingValue": "5",
    "bestRating": "5"
  },
  "author": {
    "@type": "Person",
    "name": "John Doe"
  },
  "reviewBody": "This is an excellent product. Highly recommended!",
  "datePublished": "2023-12-01"
}
</script>
```

### Event Schema

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "Tech Conference 2024",
  "startDate": "2024-03-15T09:00:00+00:00",
  "endDate": "2024-03-17T18:00:00+00:00",
  "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
  "eventStatus": "https://schema.org/EventScheduled",
  "location": {
    "@type": "Place",
    "name": "Convention Center",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "123 Main St",
      "addressLocality": "City",
      "addressRegion": "State",
      "postalCode": "12345",
      "addressCountry": "USA"
    }
  },
  "image": [
    "https://example.com/event-1x1.jpg",
    "https://example.com/event-4x3.jpg"
  ],
  "description": "Join us for the biggest tech conference of the year!",
  "offers": {
    "@type": "Offer",
    "url": "https://example.com/registration",
    "price": "299",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "validFrom": "2023-12-01"
  },
  "organizer": {
    "@type": "Organization",
    "name": "Tech Events Inc.",
    "url": "https://example.com"
  }
}
</script>
```

---

## 3. JSON-LD Format

### Basic JSON-LD Structure

```markdown
# JSON-LD Structure

## Required Properties
- **@context**: Always "https://schema.org"
- **@type**: The schema type (e.g., Article, Product)
- **name** or **headline**: The name of the entity

## Optional Properties
- **description**: Description of the entity
- **image**: Image URL(s)
- **url**: Canonical URL
- **sameAs**: Links to social profiles
- **datePublished**: Publication date
- **dateModified**: Last modified date
- **author**: Author information
- **publisher**: Publisher information

## Nested Objects
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Article Title",
  "author": {
    "@type": "Person",
    "name": "John Doe"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Publisher Name",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  }
}
</script>
```

## Arrays
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Product Name",
  "image": [
    "https://example.com/image1.jpg",
    "https://example.com/image2.jpg",
    "https://example.com/image3.jpg"
  ],
  "offers": [
    {
      "@type": "Offer",
      "price": "99.99",
      "priceCurrency": "USD"
    },
    {
      "@type": "Offer",
      "price": "89.99",
      "priceCurrency": "USD"
    }
  ]
}
</script>
```
```

---

## 4. Implementation in Next.js/React

### React Component with JSON-LD

```typescript
import Head from 'next/head'

interface ArticleProps {
  title: string
  description: string
  image: string
  publishedAt: Date
  author: {
    name: string
    url: string
  }
}

export default function Article({ title, description, image, publishedAt, author }: ArticleProps) {
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: title,
    image: [image],
    datePublished: publishedAt.toISOString(),
    author: {
      '@type': 'Person',
      name: author.name,
      url: author.url,
    },
  }
  
  return (
    <>
      <Head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
      </Head>
      <article>
        <h1>{title}</h1>
        <p>{description}</p>
      </article>
    </>
  )
}
```

### Dynamic JSON-LD Generation

```typescript
import Head from 'next/head'

interface ProductProps {
  product: {
    id: string
    name: string
    description: string
    image: string
    price: number
    currency: string
    inStock: boolean
    rating: number
    reviewCount: number
    brand: string
  }
}

export default async function ProductPage({ params }: { params: { id: string } }) {
  const product = await getProduct(params.id)
  
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: product.name,
    image: [product.image],
    description: product.description,
    sku: product.id,
    brand: {
      '@type': 'Brand',
      name: product.brand,
    },
    offers: {
      '@type': 'Offer',
      url: `https://example.com/products/${product.id}`,
      priceCurrency: product.currency,
      price: product.price,
      availability: product.inStock
        ? 'https://schema.org/InStock'
        : 'https://schema.org/OutOfStock',
    },
    aggregateRating: {
      '@type': 'AggregateRating',
      ratingValue: product.rating,
      reviewCount: product.reviewCount,
    },
  }
  
  return (
    <>
      <Head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
      </Head>
      <div>
        <h1>{product.name}</h1>
        <p>{product.description}</p>
      </div>
    </>
  )
}
```

### Reusable JSON-LD Component

```typescript
import Head from 'next/head'

interface JsonLdProps {
  data: Record<string, any>
}

export default function JsonLd({ data }: JsonLdProps) {
  return (
    <Head>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }}
      />
    </Head>
  )
}

// Usage
import JsonLd from '@/components/JsonLd'

export default function ArticlePage() {
  const article = await getArticle()
  
  const articleSchema = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: article.title,
    description: article.description,
  }
  
  return (
    <>
      <JsonLd data={articleSchema} />
      <article>
        <h1>{article.title}</h1>
      </article>
    </>
  )
}
```

---

## 5. Dynamic Structured Data

### Server-Side Generation

```typescript
// app/products/[id]/page.tsx
import Head from 'next/head'

export default async function ProductPage({ params }: { params: { id: string } }) {
  const product = await getProduct(params.id)
  const reviews = await getProductReviews(params.id)
  
  const jsonLd = {
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
    aggregateRating: {
      '@type': 'AggregateRating',
      ratingValue: product.rating,
      reviewCount: product.reviewCount,
    },
    review: reviews.map(review => ({
      '@type': 'Review',
      reviewRating: {
        '@type': 'Rating',
        ratingValue: review.rating,
      },
      author: {
        '@type': 'Person',
        name: review.author,
      },
      reviewBody: review.content,
    })),
  }
  
  return (
    <>
      <Head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
      </Head>
      <div>
        <h1>{product.name}</h1>
      </div>
    </>
  )
}
```

### Client-Side Generation

```typescript
'use client'

import { useEffect } from 'react'

interface ProductProps {
  product: {
    id: string
    name: string
    description: string
    image: string
    price: number
  }
}

export default function Product({ product }: ProductProps) {
  useEffect(() => {
    const jsonLd = {
      '@context': 'https://schema.org',
      '@type': 'Product',
      name: product.name,
      image: [product.image],
      description: product.description,
      offers: {
        '@type': 'Offer',
        priceCurrency: 'USD',
        price: product.price,
      },
    }
    
    const script = document.createElement('script')
    script.type = 'application/ld+json'
    script.text = JSON.stringify(jsonLd)
    document.head.appendChild(script)
    
    return () => {
      document.head.removeChild(script)
    }
  }, [product])
  
  return (
    <div>
      <h1>{product.name}</h1>
    </div>
  )
}
```

---

## 6. Rich Snippets

### Types of Rich Snippets

```markdown
# Rich Snippets Types

## Article Rich Snippet
- **Schema**: Article, BlogPosting, NewsArticle
- **Features**: Title, image, publisher, date, author
- **Best for**: Blog posts, news articles

## Product Rich Snippet
- **Schema**: Product
- **Features**: Name, image, price, availability, rating, reviews
- **Best for**: E-commerce products

## Review Rich Snippet
- **Schema**: Review, AggregateRating
- **Features**: Rating, review count, reviews
- **Best for**: Products, services, local businesses

## FAQ Rich Snippet
- **Schema**: FAQPage
- **Features**: Questions and answers
- **Best for**: FAQ pages, help articles

## How-To Rich Snippet
- **Schema**: HowTo
- **Features**: Steps, time, cost, tools
- **Best for**: Tutorials, guides

## Event Rich Snippet
- **Schema**: Event
- **Features**: Name, date, time, location, price
- **Best for**: Events, conferences, concerts

## Breadcrumb Rich Snippet
- **Schema**: BreadcrumbList
- **Features**: Breadcrumb navigation
- **Best for**: All pages with navigation

## Local Business Rich Snippet
- **Schema**: LocalBusiness
- **Features**: Name, address, phone, hours, reviews
- **Best for**: Local businesses

## Recipe Rich Snippet
- **Schema**: Recipe
- **Features**: Name, image, ingredients, cooking time
- **Best for**: Food blogs, recipe sites

## Video Rich Snippet
- **Schema**: VideoObject
- **Features**: Title, description, thumbnail, duration
- **Best for**: Video content

## Job Posting Rich Snippet
- **Schema**: JobPosting
- **Features**: Title, company, location, salary, date
- **Best for**: Job boards, career pages
```

---

## 7. Testing Tools

### Google Rich Results Test

```markdown
# Google Rich Results Test

## Tool
- **URL**: https://search.google.com/test/rich-results
- **Features**:
  - Test structured data
  - Preview rich snippets
  - Check for errors
  - Validate markup

## How to Use
1. Enter your URL
2. Click "Test URL"
3. Review results
4. Fix any errors
5. Re-test

## Common Errors
- **Missing required fields**: Add required properties
- **Invalid values**: Use correct format
- **Multiple types**: Use one type per block
- **Duplicate data**: Remove duplicates
```

### Schema Markup Validator

```markdown
# Schema Markup Validator

## Tool
- **URL**: https://validator.schema.org/
- **Features**:
  - Validate Schema.org markup
  - Check for errors
  - Show warnings
  - Test different formats

## How to Use
1. Enter your URL or code
2. Click "Run Test"
3. Review results
4. Fix any errors
5. Re-test

## Common Warnings
- **Missing recommended fields**: Add recommended properties
- **Deprecated properties**: Use current properties
- **Invalid format**: Use correct format
```

---

## 8. Common Patterns

### Multi-Type Schema

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "name": "Company Name",
      "url": "https://example.com"
    },
    {
      "@type": "WebSite",
      "name": "Company Name",
      "url": "https://example.com"
    }
  ]
}
</script>
```

### Nested Schema

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Product Name",
  "offers": {
    "@type": "Offer",
    "price": "99.99",
    "priceCurrency": "USD",
    "seller": {
      "@type": "Organization",
      "name": "Seller Name"
    }
  }
}
</script>
```

### Conditional Schema

```typescript
import Head from 'next/head'

export default function ProductPage({ product }: { product: Product }) {
  const jsonLd: any = {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: product.name,
    description: product.description,
  }
  
  // Add rating if available
  if (product.rating) {
    jsonLd.aggregateRating = {
      '@type': 'AggregateRating',
      ratingValue: product.rating,
      reviewCount: product.reviewCount,
    }
  }
  
  // Add offer if available
  if (product.price) {
    jsonLd.offers = {
      '@type': 'Offer',
      priceCurrency: 'USD',
      price: product.price,
      availability: product.inStock
        ? 'https://schema.org/InStock'
        : 'https://schema.org/OutOfStock',
    }
  }
  
  return (
    <>
      <Head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
      </Head>
      <div>
        <h1>{product.name}</h1>
      </div>
    </>
  )
}
```

---

## 9. Best Practices

### Structured Data Best Practices

```markdown
# Structured Data Best Practices

## 1. Use JSON-LD
- Recommended by Google
- Easy to implement
- Separated from HTML
- Can be placed anywhere

## 2. Validate Your Markup
- Use Google Rich Results Test
- Use Schema Markup Validator
- Test regularly
- Fix errors immediately

## 3. Keep It Accurate
- Match page content
- Use real data
- Don't mislead users
- Update regularly

## 4. Use Required Properties
- Include all required fields
- Add recommended fields
- Use correct formats
- Validate data types

## 5. One Type Per Block
- Don't mix types
- Use @graph for multiple
- Keep it organized
- Make it readable

## 6. Use Absolute URLs
- Use full URLs
- Include protocol
- Use HTTPS
- Test links

## 7. Optimize Images
- Use high-quality images
- Use correct dimensions
- Use appropriate formats
- Optimize file size

## 8. Test on Mobile
- Test on mobile devices
- Check rich snippet display
- Verify functionality
- Optimize for mobile

## 9. Monitor Performance
- Track rich snippet clicks
- Monitor search appearance
- Analyze user behavior
- Optimize based on data

## 10. Stay Updated
- Follow Schema.org updates
- Read Google guidelines
- Join communities
- Learn from others
```

---

## Quick Reference

### Schema.org Quick Reference

```markdown
# Schema.org Quick Reference

## Common Types
- **Article**: Blog posts, news articles
- **Product**: E-commerce products
- **Organization**: Companies, businesses
- **Person**: Authors, team members
- **LocalBusiness**: Local businesses
- **Event**: Events, conferences
- **FAQPage**: FAQ pages
- **HowTo**: Tutorials, guides
- **Review**: Product reviews
- **Recipe**: Food recipes

## Required Properties
- **@context**: "https://schema.org"
- **@type**: Schema type
- **name** or **headline**: Entity name

## Common Properties
- **description**: Description
- **image**: Image URL(s)
- **url**: Canonical URL
- **datePublished**: Publication date
- **dateModified**: Last modified date
- **author**: Author information
- **publisher**: Publisher information
- **offers**: Product offers
- **aggregateRating**: Rating information

## Testing Tools
- Google Rich Results Test: https://search.google.com/test/rich-results
- Schema Markup Validator: https://validator.schema.org/
```
