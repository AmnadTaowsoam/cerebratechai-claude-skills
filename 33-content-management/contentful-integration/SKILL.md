---
name: Contentful Integration
description: Integrating with Contentful headless CMS platform for content management, including setup, content modeling, API integration, and Next.js patterns.
---

# Contentful Integration

> **Current Level:** Intermediate  
> **Domain:** Content Management / Frontend

---

## Overview

Contentful is a headless CMS platform that provides content via APIs. This guide covers setup, content modeling, API integration, and Next.js patterns for building content-driven applications with flexibility and developer-friendly APIs.

---

## Contentful Setup

```bash
# Install Contentful CLI
npm install -g contentful-cli

# Login
contentful login

# Create space
contentful space create --name "My Space"

# Install SDK
npm install contentful contentful-management
```

## Content Models

```typescript
// Define content model programmatically
import { createClient } from 'contentful-management';

const client = createClient({
  accessToken: process.env.CONTENTFUL_MANAGEMENT_TOKEN!
});

async function createBlogPostModel() {
  const space = await client.getSpace(process.env.CONTENTFUL_SPACE_ID!);
  const environment = await space.getEnvironment('master');

  const contentType = await environment.createContentTypeWithId('blogPost', {
    name: 'Blog Post',
    fields: [
      {
        id: 'title',
        name: 'Title',
        type: 'Symbol',
        required: true
      },
      {
        id: 'slug',
        name: 'Slug',
        type: 'Symbol',
        required: true,
        unique: true
      },
      {
        id: 'content',
        name: 'Content',
        type: 'RichText',
        required: true
      },
      {
        id: 'excerpt',
        name: 'Excerpt',
        type: 'Text'
      },
      {
        id: 'coverImage',
        name: 'Cover Image',
        type: 'Link',
        linkType: 'Asset',
        required: true
      },
      {
        id: 'author',
        name: 'Author',
        type: 'Link',
        linkType: 'Entry',
        validations: [{
          linkContentType: ['author']
        }]
      },
      {
        id: 'categories',
        name: 'Categories',
        type: 'Array',
        items: {
          type: 'Link',
          linkType: 'Entry',
          validations: [{
            linkContentType: ['category']
          }]
        }
      },
      {
        id: 'publishedAt',
        name: 'Published At',
        type: 'Date'
      }
    ]
  });

  await contentType.publish();
}
```

## Content Delivery API

```typescript
// lib/contentful.ts
import { createClient, Entry } from 'contentful';

const client = createClient({
  space: process.env.CONTENTFUL_SPACE_ID!,
  accessToken: process.env.CONTENTFUL_ACCESS_TOKEN!
});

export async function getAllPosts(): Promise<BlogPost[]> {
  const entries = await client.getEntries<BlogPostFields>({
    content_type: 'blogPost',
    order: '-fields.publishedAt',
    limit: 100
  });

  return entries.items.map(parsePost);
}

export async function getPost(slug: string): Promise<BlogPost | null> {
  const entries = await client.getEntries<BlogPostFields>({
    content_type: 'blogPost',
    'fields.slug': slug,
    limit: 1
  });

  return entries.items.length > 0 ? parsePost(entries.items[0]) : null;
}

export async function getPostsByCategory(categorySlug: string): Promise<BlogPost[]> {
  const entries = await client.getEntries<BlogPostFields>({
    content_type: 'blogPost',
    'fields.categories.sys.contentType.sys.id': 'category',
    'fields.categories.fields.slug': categorySlug
  });

  return entries.items.map(parsePost);
}

function parsePost(entry: Entry<BlogPostFields>): BlogPost {
  return {
    id: entry.sys.id,
    title: entry.fields.title,
    slug: entry.fields.slug,
    content: entry.fields.content,
    excerpt: entry.fields.excerpt,
    coverImage: {
      url: entry.fields.coverImage.fields.file.url,
      title: entry.fields.coverImage.fields.title,
      width: entry.fields.coverImage.fields.file.details.image?.width || 0,
      height: entry.fields.coverImage.fields.file.details.image?.height || 0
    },
    author: entry.fields.author ? {
      name: entry.fields.author.fields.name,
      avatar: entry.fields.author.fields.avatar?.fields.file.url
    } : null,
    categories: entry.fields.categories?.map(cat => ({
      name: cat.fields.name,
      slug: cat.fields.slug
    })) || [],
    publishedAt: entry.fields.publishedAt
  };
}

interface BlogPostFields {
  title: string;
  slug: string;
  content: any;
  excerpt: string;
  coverImage: any;
  author: any;
  categories: any[];
  publishedAt: string;
}
```

## Content Management API

```typescript
// lib/contentful-management.ts
import { createClient } from 'contentful-management';

const client = createClient({
  accessToken: process.env.CONTENTFUL_MANAGEMENT_TOKEN!
});

export async function createPost(data: CreatePostDto): Promise<string> {
  const space = await client.getSpace(process.env.CONTENTFUL_SPACE_ID!);
  const environment = await space.getEnvironment('master');

  const entry = await environment.createEntry('blogPost', {
    fields: {
      title: { 'en-US': data.title },
      slug: { 'en-US': data.slug },
      content: { 'en-US': data.content },
      excerpt: { 'en-US': data.excerpt },
      publishedAt: { 'en-US': data.publishedAt }
    }
  });

  await entry.publish();

  return entry.sys.id;
}

export async function updatePost(entryId: string, data: Partial<CreatePostDto>): Promise<void> {
  const space = await client.getSpace(process.env.CONTENTFUL_SPACE_ID!);
  const environment = await space.getEnvironment('master');

  const entry = await environment.getEntry(entryId);

  Object.entries(data).forEach(([key, value]) => {
    entry.fields[key] = { 'en-US': value };
  });

  const updated = await entry.update();
  await updated.publish();
}

export async function deletePost(entryId: string): Promise<void> {
  const space = await client.getSpace(process.env.CONTENTFUL_SPACE_ID!);
  const environment = await space.getEnvironment('master');

  const entry = await environment.getEntry(entryId);
  await entry.unpublish();
  await entry.delete();
}

interface CreatePostDto {
  title: string;
  slug: string;
  content: any;
  excerpt: string;
  publishedAt: string;
}
```

## GraphQL API

```typescript
// lib/contentful-graphql.ts
import { GraphQLClient } from 'graphql-request';

const client = new GraphQLClient(
  `https://graphql.contentful.com/content/v1/spaces/${process.env.CONTENTFUL_SPACE_ID}`,
  {
    headers: {
      'Authorization': `Bearer ${process.env.CONTENTFUL_ACCESS_TOKEN}`
    }
  }
);

export async function getAllPostsGraphQL(): Promise<BlogPost[]> {
  const query = `
    query {
      blogPostCollection(order: publishedAt_DESC, limit: 100) {
        items {
          sys { id }
          title
          slug
          excerpt
          publishedAt
          coverImage {
            url
            title
            width
            height
          }
          author {
            name
            avatar {
              url
            }
          }
          categoriesCollection {
            items {
              name
              slug
            }
          }
        }
      }
    }
  `;

  const data = await client.request(query);
  return data.blogPostCollection.items;
}

export async function getPostGraphQL(slug: string): Promise<BlogPost> {
  const query = `
    query GetPost($slug: String!) {
      blogPostCollection(where: { slug: $slug }, limit: 1) {
        items {
          sys { id }
          title
          slug
          content {
            json
            links {
              assets {
                block {
                  sys { id }
                  url
                  title
                  width
                  height
                }
              }
            }
          }
          excerpt
          publishedAt
          coverImage {
            url
            title
            width
            height
          }
          author {
            name
            bio
            avatar {
              url
            }
          }
        }
      }
    }
  `;

  const data = await client.request(query, { slug });
  return data.blogPostCollection.items[0];
}
```

## Content Preview

```typescript
// lib/contentful-preview.ts
import { createClient } from 'contentful';

const previewClient = createClient({
  space: process.env.CONTENTFUL_SPACE_ID!,
  accessToken: process.env.CONTENTFUL_PREVIEW_TOKEN!,
  host: 'preview.contentful.com'
});

export async function getPreviewPost(slug: string): Promise<BlogPost | null> {
  const entries = await previewClient.getEntries<BlogPostFields>({
    content_type: 'blogPost',
    'fields.slug': slug,
    limit: 1
  });

  return entries.items.length > 0 ? parsePost(entries.items[0]) : null;
}

// pages/api/preview.ts
export default async function handler(req: any, res: any) {
  const { secret, slug } = req.query;

  if (secret !== process.env.CONTENTFUL_PREVIEW_SECRET) {
    return res.status(401).json({ message: 'Invalid token' });
  }

  const post = await getPreviewPost(slug);

  if (!post) {
    return res.status(404).json({ message: 'Post not found' });
  }

  res.setPreviewData({});
  res.redirect(`/blog/${slug}`);
}

// pages/blog/[slug].tsx
export async function getStaticProps({ params, preview = false }: any) {
  const post = preview
    ? await getPreviewPost(params.slug)
    : await getPost(params.slug);

  if (!post) {
    return { notFound: true };
  }

  return {
    props: { post, preview },
    revalidate: 60
  };
}
```

## Image API

```typescript
// components/ContentfulImage.tsx
import Image from 'next/image';

interface ContentfulImageProps {
  src: string;
  alt: string;
  width: number;
  height: number;
  quality?: number;
}

export function ContentfulImage({
  src,
  alt,
  width,
  height,
  quality = 75
}: ContentfulImageProps) {
  const imageUrl = `https:${src}?w=${width}&h=${height}&q=${quality}&fm=webp`;

  return (
    <Image
      src={imageUrl}
      alt={alt}
      width={width}
      height={height}
      quality={quality}
    />
  );
}

// Responsive image
export function ResponsiveContentfulImage({ src, alt }: { src: string; alt: string }) {
  const srcSet = [
    `https:${src}?w=640&fm=webp 640w`,
    `https:${src}?w=750&fm=webp 750w`,
    `https:${src}?w=828&fm=webp 828w`,
    `https:${src}?w=1080&fm=webp 1080w`,
    `https:${src}?w=1200&fm=webp 1200w`
  ].join(', ');

  return (
    <img
      src={`https:${src}?w=1200&fm=webp`}
      srcSet={srcSet}
      sizes="(max-width: 640px) 640px, (max-width: 1200px) 1200px, 100vw"
      alt={alt}
      loading="lazy"
    />
  );
}
```

## Webhooks

```typescript
// pages/api/webhooks/contentful.ts
import crypto from 'crypto';

export default async function handler(req: any, res: any) {
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Method not allowed' });
  }

  // Verify webhook signature
  const signature = req.headers['x-contentful-signature'];
  const body = JSON.stringify(req.body);
  
  const hash = crypto
    .createHmac('sha256', process.env.CONTENTFUL_WEBHOOK_SECRET!)
    .update(body)
    .digest('base64');

  if (signature !== hash) {
    return res.status(401).json({ message: 'Invalid signature' });
  }

  const { sys, fields } = req.body;

  switch (sys.type) {
    case 'Entry':
      if (sys.contentType.sys.id === 'blogPost') {
        await handleBlogPostUpdate(fields.slug['en-US']);
      }
      break;

    case 'Asset':
      await handleAssetUpdate(sys.id);
      break;
  }

  res.json({ received: true });
}

async function handleBlogPostUpdate(slug: string): Promise<void> {
  // Revalidate Next.js page
  await fetch(`${process.env.NEXT_URL}/api/revalidate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ slug })
  });
}

async function handleAssetUpdate(assetId: string): Promise<void> {
  // Invalidate cache for pages using this asset
}
```

## Localization

```typescript
// lib/contentful-i18n.ts
export async function getLocalizedPost(slug: string, locale: string): Promise<BlogPost | null> {
  const entries = await client.getEntries<BlogPostFields>({
    content_type: 'blogPost',
    'fields.slug': slug,
    locale,
    limit: 1
  });

  return entries.items.length > 0 ? parsePost(entries.items[0]) : null;
}

export async function getAllLocales(): Promise<string[]> {
  const space = await client.getSpace();
  return space.locales.map(locale => locale.code);
}

// pages/[locale]/blog/[slug].tsx
export async function getStaticPaths() {
  const locales = await getAllLocales();
  const posts = await getAllPosts();

  const paths = locales.flatMap(locale =>
    posts.map(post => ({
      params: { locale, slug: post.slug }
    }))
  );

  return { paths, fallback: 'blocking' };
}

export async function getStaticProps({ params }: any) {
  const post = await getLocalizedPost(params.slug, params.locale);

  if (!post) {
    return { notFound: true };
  }

  return {
    props: { post },
    revalidate: 60
  };
}
```

## Content Migrations

```typescript
// migrations/add-reading-time.ts
import { createClient } from 'contentful-management';

const client = createClient({
  accessToken: process.env.CONTENTFUL_MANAGEMENT_TOKEN!
});

async function addReadingTimeField() {
  const space = await client.getSpace(process.env.CONTENTFUL_SPACE_ID!);
  const environment = await space.getEnvironment('master');

  const contentType = await environment.getContentType('blogPost');

  contentType.fields.push({
    id: 'readingTime',
    name: 'Reading Time',
    type: 'Number'
  });

  const updated = await contentType.update();
  await updated.publish();
}

async function calculateReadingTime() {
  const space = await client.getSpace(process.env.CONTENTFUL_SPACE_ID!);
  const environment = await space.getEnvironment('master');

  const entries = await environment.getEntries({
    content_type: 'blogPost'
  });

  for (const entry of entries.items) {
    const content = entry.fields.content?.['en-US'];
    const wordCount = countWords(content);
    const readingTime = Math.ceil(wordCount / 200); // 200 words per minute

    entry.fields.readingTime = { 'en-US': readingTime };
    const updated = await entry.update();
    await updated.publish();
  }
}

function countWords(richText: any): number {
  // Implementation
  return 0;
}

addReadingTimeField()
  .then(() => calculateReadingTime())
  .then(() => console.log('Migration complete'));
```

## Next.js Integration with ISR

```typescript
// pages/blog/index.tsx
export async function getStaticProps() {
  const posts = await getAllPosts();

  return {
    props: { posts },
    revalidate: 60 // Revalidate every 60 seconds
  };
}

// pages/blog/[slug].tsx
export async function getStaticPaths() {
  const posts = await getAllPosts();

  return {
    paths: posts.map(post => ({
      params: { slug: post.slug }
    })),
    fallback: 'blocking'
  };
}

export async function getStaticProps({ params }: any) {
  const post = await getPost(params.slug);

  if (!post) {
    return { notFound: true };
  }

  return {
    props: { post },
    revalidate: 60
  };
}

// pages/api/revalidate.ts
export default async function handler(req: any, res: any) {
  if (req.query.secret !== process.env.REVALIDATE_SECRET) {
    return res.status(401).json({ message: 'Invalid token' });
  }

  try {
    await res.revalidate(`/blog/${req.body.slug}`);
    await res.revalidate('/blog');
    return res.json({ revalidated: true });
  } catch (err) {
    return res.status(500).send('Error revalidating');
  }
}
```

---

## Quick Start

### Contentful Client Setup

```javascript
const contentful = require('contentful')

const client = contentful.createClient({
  space: process.env.CONTENTFUL_SPACE_ID,
  accessToken: process.env.CONTENTFUL_ACCESS_TOKEN
})

// Fetch entries
const entries = await client.getEntries({
  content_type: 'blogPost',
  order: '-sys.createdAt'
})
```

### Next.js Integration

```javascript
// pages/blog/[slug].js
import { createClient } from 'contentful'

export async function getStaticProps({ params }) {
  const client = createClient({
    space: process.env.CONTENTFUL_SPACE_ID,
    accessToken: process.env.CONTENTFUL_ACCESS_TOKEN
  })
  
  const entries = await client.getEntries({
    content_type: 'blogPost',
    'fields.slug': params.slug
  })
  
  return {
    props: {
      post: entries.items[0]
    },
    revalidate: 60  // ISR: revalidate every 60 seconds
  }
}
```

---

## Production Checklist

- [ ] **Content Model**: Design flexible content models
- [ ] **API Keys**: Secure API keys (environment variables)
- [ ] **GraphQL**: Use GraphQL for efficient queries
- [ ] **Caching**: Cache content appropriately
- [ ] **Preview Mode**: Enable preview mode for draft content
- [ ] **Webhooks**: Set up webhooks for content updates
- [ ] **Images**: Use Contentful's Image API for optimization
- [ ] **Localization**: Support multi-language content
- [ ] **Error Handling**: Handle API errors gracefully
- [ ] **Rate Limiting**: Respect API rate limits
- [ ] **Testing**: Test content fetching
- [ ] **Documentation**: Document content structure

---

## Anti-patterns

### ❌ Don't: Fetch on Every Request

```javascript
// ❌ Bad - No caching
export async function getServerSideProps() {
  const entries = await client.getEntries()  // Every request!
  return { props: { entries } }
}
```

```javascript
// ✅ Good - Cache with ISR
export async function getStaticProps() {
  const entries = await client.getEntries()
  return {
    props: { entries },
    revalidate: 60  // Revalidate every 60 seconds
  }
}
```

### ❌ Don't: Expose API Keys

```javascript
// ❌ Bad - API key in client code
const client = createClient({
  space: 'public-space',
  accessToken: 'secret-token'  // Exposed!
})
```

```javascript
// ✅ Good - Use backend proxy
// Frontend
fetch('/api/contentful/posts')

// Backend
app.get('/api/contentful/posts', async (req, res) => {
  const client = createClient({
    space: process.env.CONTENTFUL_SPACE_ID,
    accessToken: process.env.CONTENTFUL_ACCESS_TOKEN
  })
  const posts = await client.getEntries()
  res.json(posts)
})
```

---

## Integration Points

- **Headless CMS** (`33-content-management/headless-cms/`) - CMS patterns
- **Next.js Patterns** (`02-frontend/nextjs-patterns/`) - ISR and SSG
- **API Design** (`01-foundations/api-design/`) - API patterns

---

## Further Reading

- [Contentful Documentation](https://www.contentful.com/developers/docs/)
- [Contentful GraphQL API](https://www.contentful.com/developers/docs/references/graphql/)
- [Next.js Contentful Example](https://github.com/vercel/next.js/tree/canary/examples/cms-contentful)
5. **Webhooks** - Use webhooks for real-time updates
6. **ISR** - Use Incremental Static Regeneration
7. **Localization** - Support multi-language content
8. **Migrations** - Version control content model changes
9. **Caching** - Implement caching strategies
10. **Security** - Secure API keys and webhooks

## Resources

- [Contentful Documentation](https://www.contentful.com/developers/docs/)
- [Content Delivery API](https://www.contentful.com/developers/docs/references/content-delivery-api/)
- [Content Management API](https://www.contentful.com/developers/docs/references/content-management-api/)
- [GraphQL API](https://www.contentful.com/developers/docs/references/graphql/)
