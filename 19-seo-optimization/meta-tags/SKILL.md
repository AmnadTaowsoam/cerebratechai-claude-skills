# Meta Tags

## Overview

Meta tags are HTML elements that provide metadata about your webpage. They are crucial for SEO, social media sharing, and user experience.

---

## 1. Essential Meta Tags

### Title Tag

```html
<!-- Basic title tag -->
<title>Page Title | Site Name</title>

<!-- Recommended length: 50-60 characters -->
<title>How to Optimize Your Website for SEO | SEO Guide</title>

<!-- With separator -->
<title>Page Title - Site Name</title>

<!-- With branding -->
<title>Page Title | Brand Name</title>
```

### Best Practices

```markdown
# Title Tag Best Practices

## Length
- **Optimal**: 50-60 characters
- **Maximum**: 600 pixels (varies by device)
- **Mobile**: Shorter is better

## Structure
- **Primary keyword**: Front of title
- **Secondary keyword**: Middle of title
- **Brand name**: End of title
- **Separator**: Use | or -

## Examples

### Good Titles
```
How to Optimize SEO | Complete Guide
Best Running Shoes 2023 | Reviews & Comparison
Web Development Services | Company Name
```

### Bad Titles
```
Home
Untitled Page
Welcome to our website
SEO, Web Development, Marketing, Design, Services
```

## Tips
- Put important keywords first
- Make it compelling for users
- Include brand name
- Use unique titles for each page
- Avoid keyword stuffing
- Match user search intent
```

### Meta Description

```html
<!-- Basic meta description -->
<meta name="description" content="A brief description of your page content.">

<!-- Recommended length: 150-160 characters -->
<meta name="description" content="Learn how to optimize your website for search engines with our comprehensive SEO guide covering technical SEO, on-page optimization, and link building strategies.">

<!-- With call to action -->
<meta name="description" content="Discover the best running shoes of 2023. Read our expert reviews and find your perfect pair today!">

<!-- For product pages -->
<meta name="description" content="Shop our collection of premium running shoes. Free shipping on orders over $50. 30-day money-back guarantee.">
```

### Best Practices

```markdown
# Meta Description Best Practices

## Length
- **Optimal**: 150-160 characters
- **Maximum**: 920 pixels (varies by device)
- **Mobile**: Shorter is better

## Content
- **Compelling**: Encourage clicks
- **Relevant**: Match page content
- **Keywords**: Include naturally
- **CTA**: Include call to action

## Examples

### Good Descriptions
```
Learn how to optimize your website for search engines with our comprehensive SEO guide covering technical SEO, on-page optimization, and link building strategies.

Discover the best running shoes of 2023. Read our expert reviews and find your perfect pair today!

Shop our collection of premium running shoes. Free shipping on orders over $50. 30-day money-back guarantee.
```

### Bad Descriptions
```
This is a webpage about SEO.
Welcome to our website.
We sell shoes and other products.
SEO, SEO, SEO, SEO, SEO, SEO, SEO.
```

## Tips
- Write for humans, not robots
- Include target keywords naturally
- Make it compelling and click-worthy
- Match user search intent
- Include unique description for each page
- Avoid keyword stuffing
- Use active voice
```

---

## 2. Open Graph Tags (Facebook)

### Basic Open Graph Tags

```html
<!-- Basic Open Graph tags -->
<meta property="og:title" content="Page Title">
<meta property="og:description" content="Page description">
<meta property="og:image" content="https://example.com/image.jpg">
<meta property="og:url" content="https://example.com/page">
<meta property="og:type" content="website">

<!-- Full implementation -->
<meta property="og:title" content="How to Optimize Your Website for SEO">
<meta property="og:description" content="Learn how to optimize your website for search engines with our comprehensive SEO guide.">
<meta property="og:image" content="https://example.com/images/og-image.jpg">
<meta property="og:url" content="https://example.com/seo-guide">
<meta property="og:type" content="article">
<meta property="og:site_name" content="My Website">
<meta property="og:locale" content="en_US">
```

### Open Graph for Different Content Types

```html
<!-- Website -->
<meta property="og:type" content="website">

<!-- Article -->
<meta property="og:type" content="article">
<meta property="article:published_time" content="2023-12-01T00:00:00+00:00">
<meta property="article:modified_time" content="2023-12-01T00:00:00+00:00">
<meta property="article:author" content="John Doe">
<meta property="article:section" content="SEO">
<meta property="article:tag" content="Technical SEO">
<meta property="article:tag" content="On-Page SEO">

<!-- Product -->
<meta property="og:type" content="product">
<meta property="product:price:amount" content="99.99">
<meta property="product:price:currency" content="USD">
<meta property="product:availability" content="in stock">
<meta property="product:brand" content="Brand Name">
<meta property="product:retailer_item_id" content="product-123">

<!-- Video -->
<meta property="og:type" content="video">
<meta property="og:video:url" content="https://example.com/video.mp4">
<meta property="og:video:secure_url" content="https://example.com/video.mp4">
<meta property="og:video:type" content="video/mp4">
<meta property="og:video:width" content="1920">
<meta property="og:video:height" content="1080">
```

### Open Graph Image Specifications

```markdown
# Open Graph Image Best Practices

## Image Size
- **Recommended**: 1200 x 630 pixels
- **Minimum**: 200 x 200 pixels
- **Aspect Ratio**: 1.91:1

## File Format
- **Preferred**: PNG or JPG
- **Size**: Under 8MB

## Content
- **Relevant**: Match page content
- **High Quality**: Clear and professional
- **Text**: Minimal or no text
- **Brand**: Include logo if appropriate

## Multiple Images
```html
<!-- Primary image -->
<meta property="og:image" content="https://example.com/image1.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">

<!-- Secondary image -->
<meta property="og:image" content="https://example.com/image2.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
```

## Tips
- Use high-quality images
- Test with Facebook Sharing Debugger
- Use absolute URLs
- Ensure images are accessible
- Consider mobile dimensions
```

---

## 3. Twitter Cards

### Twitter Card Types

```html
<!-- Summary Card -->
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="Page Title">
<meta name="twitter:description" content="Page description">
<meta name="twitter:image" content="https://example.com/image.jpg">

<!-- Summary Card with Large Image -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Page Title">
<meta name="twitter:description" content="Page description">
<meta name="twitter:image" content="https://example.com/image.jpg">

<!-- App Card -->
<meta name="twitter:card" content="app">
<meta name="twitter:site" content="@sitehandle">
<meta name="twitter:title" content="App Title">
<meta name="twitter:description" content="App description">
<meta name="twitter:image" content="https://example.com/image.jpg">
<meta name="twitter:app:name:iphone" content="App Name">
<meta name="twitter:app:id:iphone" content="123456789">
<meta name="twitter:app:url:iphone" content="myapp://path">
<meta name="twitter:app:name:ipad" content="App Name">
<meta name="twitter:app:id:ipad" content="123456789">
<meta name="twitter:app:url:ipad" content="myapp://path">
<meta name="twitter:app:name:googleplay" content="App Name">
<meta name="twitter:app:id:googleplay" content="com.example.app">
<meta name="twitter:app:url:googleplay" content="https://play.google.com/store/apps/details?id=com.example.app">

<!-- Player Card -->
<meta name="twitter:card" content="player">
<meta name="twitter:site" content="@sitehandle">
<meta name="twitter:title" content="Video Title">
<meta name="twitter:description" content="Video description">
<meta name="twitter:image" content="https://example.com/image.jpg">
<meta name="twitter:player" content="https://example.com/player.html">
<meta name="twitter:player:width" content="480">
<meta name="twitter:player:height" content="480">
<meta name="twitter:player:stream" content="https://example.com/video.mp4">
<meta name="twitter:player:stream:content_type" content="video/mp4">
```

### Twitter Card Image Specifications

```markdown
# Twitter Card Image Best Practices

## Summary Card
- **Size**: 120 x 120 pixels
- **Format**: PNG, JPG, GIF, WEBP

## Summary Card with Large Image
- **Size**: 280 x 150 pixels
- **Format**: PNG, JPG, GIF, WEBP

## Player Card
- **Size**: 280 x 150 pixels
- **Format**: PNG, JPG, GIF, WEBP

## Tips
- Use high-quality images
- Test with Card Validator
- Use absolute URLs
- Ensure images are accessible
```

---

## 4. LinkedIn Tags

### LinkedIn Share Tags

```html
<!-- Basic LinkedIn tags -->
<meta property="og:title" content="Page Title">
<meta property="og:description" content="Page description">
<meta property="og:image" content="https://example.com/image.jpg">
<meta property="og:url" content="https://example.com/page">

<!-- LinkedIn specific -->
<meta property="linkedin:owner" content="company-id">
<meta property="linkedin:published_at" content="2023-12-01T00:00:00+00:00">
```

### LinkedIn Image Specifications

```markdown
# LinkedIn Image Best Practices

## Image Size
- **Recommended**: 1200 x 627 pixels
- **Minimum**: 200 x 200 pixels
- **Aspect Ratio**: 1.91:1

## File Format
- **Preferred**: PNG or JPG
- **Size**: Under 5MB

## Tips
- Use professional images
- Include logo if appropriate
- Test with LinkedIn Post Inspector
- Use absolute URLs
```

---

## 5. Pinterest Tags

### Pinterest Rich Pins

```html
<!-- Product Pin -->
<meta property="og:title" content="Product Name">
<meta property="og:description" content="Product description">
<meta property="og:image" content="https://example.com/product-image.jpg">
<meta property="og:url" content="https://example.com/product">
<meta property="og:type" content="product">
<meta property="product:price:amount" content="99.99">
<meta property="product:price:currency" content="USD">
<meta property="product:availability" content="in stock">

<!-- Article Pin -->
<meta property="og:title" content="Article Title">
<meta property="og:description" content="Article description">
<meta property="og:image" content="https://example.com/article-image.jpg">
<meta property="og:url" content="https://example.com/article">
<meta property="og:type" content="article">
```

### Pinterest Image Specifications

```markdown
# Pinterest Image Best Practices

## Image Size
- **Recommended**: 1000 x 1500 pixels (2:3 ratio)
- **Minimum**: 600 x 900 pixels
- **Aspect Ratio**: 1:2 to 1:3.5

## File Format
- **Preferred**: PNG or JPG
- **Size**: Under 10MB

## Tips
- Use vertical images
- High quality is important
- Include text overlay
- Test with Pinterest Rich Pin Validator
```

---

## 6. WhatsApp Preview

### WhatsApp Link Preview

```html
<!-- WhatsApp uses Open Graph tags -->
<meta property="og:title" content="Page Title">
<meta property="og:description" content="Page description">
<meta property="og:image" content="https://example.com/image.jpg">
<meta property="og:url" content="https://example.com/page">
```

### WhatsApp Image Specifications

```markdown
# WhatsApp Image Best Practices

## Image Size
- **Recommended**: 1200 x 630 pixels
- **Minimum**: 300 x 200 pixels
- **Aspect Ratio**: 1.91:1

## File Format
- **Preferred**: JPG
- **Size**: Under 300KB

## Tips
- Use high-quality images
- Keep file size small
- Test with WhatsApp link preview
- Use absolute URLs
```

---

## 7. Favicon and App Icons

### Favicon Implementation

```html
<!-- Basic favicon -->
<link rel="icon" href="/favicon.ico">

<!-- PNG favicon -->
<link rel="icon" type="image/png" href="/favicon-32x32.png" sizes="32x32">
<link rel="icon" type="image/png" href="/favicon-16x16.png" sizes="16x16">

<!-- Apple touch icon -->
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon-180x180.png">

<!-- Android icon -->
<link rel="icon" type="image/png" sizes="192x192" href="/android-icon-192x192.png">

<!-- Mask icon (Safari) -->
<link rel="mask-icon" href="/safari-pinned-tab.svg" color="#000000">

```

### Favicon Generator

```markdown
# Favicon Best Practices

## Sizes Needed
- **Favicon**: 16x16, 32x32, 48x48
- **Apple Touch**: 180x180
- **Android**: 192x192
- **Microsoft**: 270x270

## Tools
- Favicon.io
- RealFaviconGenerator
- Favicon Generator
- Canva

## Tips
- Use simple design
- High contrast
- Test on different devices
- Include in manifest.json
```

---

## 8. Theme Color

### Theme Color Implementation

```html
<!-- Theme color for mobile browsers -->
<meta name="theme-color" content="#000000">

<!-- Theme color with media query -->
<meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#000000" media="(prefers-color-scheme: dark)">

<!-- Theme color for Safari -->
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
```

### Best Practices

```markdown
# Theme Color Best Practices

## When to Use
- Mobile browsers
- PWA (Progressive Web Apps)
- Mobile web apps

## Tips
- Match your brand colors
- Consider accessibility
- Test on different devices
- Support dark mode
```

---

## 9. Manifest.json

### Web App Manifest

```json
{
  "name": "My App",
  "short_name": "App",
  "description": "My progressive web app",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#000000",
  "orientation": "portrait",
  "icons": [
    {
      "src": "/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ],
  "categories": ["business", "productivity"],
  "shortcuts": [
    {
      "name": "Open Settings",
      "short_name": "Settings",
      "description": "Open app settings",
      "url": "/settings",
      "icons": [{ "src": "/settings-icon.png", "sizes": "96x96" }]
    }
  ]
}
```

### Linking Manifest

```html
<link rel="manifest" href="/manifest.json">
```

---

## 10. Dynamic Meta Tags

### Dynamic Meta Tags in Next.js

```typescript
// app/products/[id]/page.tsx
import type { Metadata } from 'next'

type Props = {
  params: { id: string }
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const product = await getProduct(params.id)
  
  return {
    title: product.name,
    description: product.description,
    openGraph: {
      title: product.name,
      description: product.description,
      images: [product.image],
      type: 'product',
    },
    twitter: {
      card: 'summary_large_image',
      title: product.name,
      description: product.description,
      images: [product.image],
    },
  }
}
```

### Dynamic Meta Tags in React

```typescript
import Head from 'next/head'
import { useEffect } from 'react'

export default function ProductPage({ product }: { product: Product }) {
  useEffect(() => {
    document.title = product.name
    document.querySelector('meta[name="description"]')?.setAttribute('content', product.description)
  }, [product])
  
  return (
    <Head>
      <title>{product.name}</title>
      <meta name="description" content={product.description} />
      <meta property="og:title" content={product.name} />
      <meta property="og:description" content={product.description} />
      <meta property="og:image" content={product.image} />
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content={product.name} />
      <meta name="twitter:description" content={product.description} />
      <meta name="twitter:image" content={product.image} />
    </Head>
  )
}
```

---

## 11. Testing Tools

### Meta Tag Testing Tools

```markdown
# Meta Tag Testing Tools

## Social Media Testing

### Facebook Sharing Debugger
- URL: https://developers.facebook.com/tools/debug/
- Features:
  - Preview how content appears on Facebook
  - Debug Open Graph tags
  - Clear cache
  - Check for errors

### Twitter Card Validator
- URL: https://cards-dev.twitter.com/validator
- Features:
  - Preview Twitter cards
  - Validate Twitter card tags
  - Check for errors
  - Test different card types

### LinkedIn Post Inspector
- URL: https://www.linkedin.com/post-inspector/
- Features:
  - Preview on LinkedIn
  - Validate Open Graph tags
  - Check for errors

### Pinterest Rich Pin Validator
- URL: https://developers.pinterest.com/tools/url-debugger/
- Features:
  - Preview on Pinterest
  - Validate rich pin tags
  - Check for errors

## SEO Testing

### Google Rich Results Test
- URL: https://search.google.com/test/rich-results
- Features:
  - Test structured data
  - Preview rich snippets
  - Validate markup
  - Check for errors

### Meta Tag Analyzer
- URL: https://www.seomofo.com/tools/metadata/analyzer
- Features:
  - Analyze meta tags
  - Check title length
  - Check description length
  - Provide recommendations

## Browser Testing

### Chrome DevTools
- Check meta tags in Elements tab
- View network requests
- Test mobile preview

### Firefox Developer Tools
- Check meta tags in Inspector
- View network requests
- Test responsive design
```

---

## 12. Best Practices

### Meta Tag Best Practices

```markdown
# Meta Tag Best Practices

## General Best Practices

### 1. Keep It Relevant
- Match page content
- Use relevant keywords
- Be accurate and honest
- Avoid misleading information

### 2. Optimize Length
- Title: 50-60 characters
- Description: 150-160 characters
- Twitter: 280 characters
- Facebook: No strict limit

### 3. Make It Compelling
- Write for humans
- Include call to action
- Highlight benefits
- Stand out from competitors

### 4. Use Unique Tags
- Unique title per page
- Unique description per page
- Unique images per page
- Avoid duplicate content

### 5. Test Everything
- Test with social media tools
- Test on different devices
- Test with different browsers
- Monitor performance

## Platform-Specific Best Practices

### Facebook
- Use Open Graph tags
- Optimize image size
- Include site name
- Use appropriate type

### Twitter
- Use Twitter card tags
- Choose appropriate card type
- Optimize image size
- Include handle

### LinkedIn
- Use Open Graph tags
- Professional images
- Include company info
- Optimize for B2B

### Pinterest
- Use vertical images
- Include product info
- Use rich pin tags
- Optimize for discovery

## Technical Best Practices

### 1. Use Absolute URLs
```html
<!-- Good -->
<meta property="og:image" content="https://example.com/image.jpg">

<!-- Bad -->
<meta property="og:image" content="/image.jpg">
```

### 2. Use HTTPS
```html
<!-- Good -->
<meta property="og:url" content="https://example.com/page">

<!-- Bad -->
<meta property="og:url" content="http://example.com/page">
```

### 3. Use Proper Encoding
```html
<!-- Good -->
<meta charset="UTF-8">

<!-- Bad -->
<meta charset="ISO-8859-1">
```

### 4. Include Viewport
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

### 5. Use Canonical Tags
```html
<link rel="canonical" href="https://example.com/page">
```
```

---

## Quick Reference

### Meta Tag Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Basic Meta -->
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Page description">
  
  <!-- Title -->
  <title>Page Title | Site Name</title>
  
  <!-- Canonical -->
  <link rel="canonical" href="https://example.com/page">
  
  <!-- Open Graph -->
  <meta property="og:title" content="Page Title">
  <meta property="og:description" content="Page description">
  <meta property="og:image" content="https://example.com/image.jpg">
  <meta property="og:url" content="https://example.com/page">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Site Name">
  
  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Page Title">
  <meta name="twitter:description" content="Page description">
  <meta name="twitter:image" content="https://example.com/image.jpg">
  
  <!-- Favicon -->
  <link rel="icon" href="/favicon.ico">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  
  <!-- Theme Color -->
  <meta name="theme-color" content="#000000">
  
  <!-- Manifest -->
  <link rel="manifest" href="/manifest.json">
</head>
<body>
  <!-- Content -->
</body>
</html>
```

### Meta Tag Checklist

```markdown
# Meta Tag Checklist

## Essential Tags
- [ ] Title tag (50-60 characters)
- [ ] Meta description (150-160 characters)
- [ ] Charset declaration
- [ ] Viewport meta tag
- [ ] Canonical tag

## Social Media Tags
- [ ] Open Graph title
- [ ] Open Graph description
- [ ] Open Graph image (1200x630)
- [ ] Open Graph URL
- [ ] Open Graph type
- [ ] Twitter card type
- [ ] Twitter title
- [ ] Twitter description
- [ ] Twitter image

## Icons
- [ ] Favicon (16x16, 32x32)
- [ ] Apple touch icon (180x180)
- [ ] Android icon (192x192)
- [ ] Manifest.json

## Other Tags
- [ ] Theme color
- [ ] Robots meta tag (if needed)
- [ ] Author meta tag
- [ ] Keywords meta tag (optional, not used by Google)
```
