---
name: WordPress API
description: Using WordPress REST API for headless WordPress implementations including authentication, endpoints, custom post types, media management, and Next.js integration.
---

# WordPress API

> **Current Level:** Intermediate  
> **Domain:** Content Management / Backend

---

## Overview

WordPress REST API enables headless WordPress implementations. This guide covers authentication, endpoints, custom post types, and Next.js integration for building content-driven applications with WordPress as a headless CMS.

## WordPress REST API Overview

**Base URL:** `https://yoursite.com/wp-json/wp/v2/`

**Endpoints:**
- `/posts` - Blog posts
- `/pages` - Pages
- `/categories` - Categories
- `/tags` - Tags
- `/media` - Media files
- `/users` - Users
- `/comments` - Comments

## Authentication

### Application Passwords

```typescript
// services/wordpress-client.service.ts
import axios, { AxiosInstance } from 'axios';

export class WordPressClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: `${process.env.WORDPRESS_URL}/wp-json/wp/v2`,
      auth: {
        username: process.env.WORDPRESS_USERNAME!,
        password: process.env.WORDPRESS_APP_PASSWORD!
      }
    });
  }

  async getPosts(params?: QueryParams): Promise<Post[]> {
    const response = await this.client.get('/posts', { params });
    return response.data;
  }

  async getPost(id: number): Promise<Post> {
    const response = await this.client.get(`/posts/${id}`);
    return response.data;
  }

  async createPost(data: CreatePostDto): Promise<Post> {
    const response = await this.client.post('/posts', data);
    return response.data;
  }

  async updatePost(id: number, data: Partial<Post>): Promise<Post> {
    const response = await this.client.put(`/posts/${id}`, data);
    return response.data;
  }

  async deletePost(id: number): Promise<void> {
    await this.client.delete(`/posts/${id}`);
  }
}

interface QueryParams {
  page?: number;
  per_page?: number;
  search?: string;
  categories?: number[];
  tags?: number[];
  orderby?: 'date' | 'title' | 'relevance';
  order?: 'asc' | 'desc';
  _embed?: boolean;
}
```

### JWT Authentication

```typescript
// Install JWT plugin first
// https://wordpress.org/plugins/jwt-authentication-for-wp-rest-api/

export class WordPressJWTClient {
  private token: string | null = null;

  async login(username: string, password: string): Promise<string> {
    const response = await axios.post(
      `${process.env.WORDPRESS_URL}/wp-json/jwt-auth/v1/token`,
      { username, password }
    );

    this.token = response.data.token;
    return this.token;
  }

  async validateToken(): Promise<boolean> {
    try {
      await axios.post(
        `${process.env.WORDPRESS_URL}/wp-json/jwt-auth/v1/token/validate`,
        {},
        {
          headers: {
            'Authorization': `Bearer ${this.token}`
          }
        }
      );
      return true;
    } catch {
      return false;
    }
  }

  async makeAuthenticatedRequest(endpoint: string, method: string = 'GET', data?: any): Promise<any> {
    const response = await axios({
      method,
      url: `${process.env.WORDPRESS_URL}/wp-json/wp/v2${endpoint}`,
      data,
      headers: {
        'Authorization': `Bearer ${this.token}`
      }
    });

    return response.data;
  }
}
```

## Posts and Pages

```typescript
// services/wordpress-posts.service.ts
export class WordPressPostsService {
  constructor(private client: WordPressClient) {}

  async getAllPosts(): Promise<Post[]> {
    return this.client.getPosts({
      per_page: 100,
      _embed: true
    });
  }

  async getPostBySlug(slug: string): Promise<Post | null> {
    const posts = await this.client.getPosts({
      slug,
      _embed: true
    });

    return posts.length > 0 ? posts[0] : null;
  }

  async getPostsByCategory(categorySlug: string): Promise<Post[]> {
    // Get category ID first
    const categories = await this.client.get('/categories', {
      params: { slug: categorySlug }
    });

    if (categories.data.length === 0) return [];

    return this.client.getPosts({
      categories: [categories.data[0].id],
      _embed: true
    });
  }

  async searchPosts(query: string): Promise<Post[]> {
    return this.client.getPosts({
      search: query,
      _embed: true
    });
  }
}

interface Post {
  id: number;
  date: string;
  slug: string;
  status: string;
  title: {
    rendered: string;
  };
  content: {
    rendered: string;
  };
  excerpt: {
    rendered: string;
  };
  author: number;
  featured_media: number;
  categories: number[];
  tags: number[];
  _embedded?: {
    author: Author[];
    'wp:featuredmedia': Media[];
    'wp:term': Term[][];
  };
}
```

## Custom Post Types

```php
// functions.php - Register custom post type
function register_portfolio_post_type() {
    register_post_type('portfolio', array(
        'labels' => array(
            'name' => 'Portfolio',
            'singular_name' => 'Portfolio Item'
        ),
        'public' => true,
        'has_archive' => true,
        'show_in_rest' => true, // Enable REST API
        'rest_base' => 'portfolio',
        'supports' => array('title', 'editor', 'thumbnail', 'custom-fields')
    ));
}
add_action('init', 'register_portfolio_post_type');
```

```typescript
// services/wordpress-custom-post-types.service.ts
export class WordPressCustomPostTypesService {
  async getPortfolioItems(): Promise<PortfolioItem[]> {
    const response = await axios.get(
      `${process.env.WORDPRESS_URL}/wp-json/wp/v2/portfolio`,
      {
        params: { _embed: true }
      }
    );

    return response.data;
  }

  async getPortfolioItem(slug: string): Promise<PortfolioItem | null> {
    const response = await axios.get(
      `${process.env.WORDPRESS_URL}/wp-json/wp/v2/portfolio`,
      {
        params: { slug, _embed: true }
      }
    );

    return response.data.length > 0 ? response.data[0] : null;
  }
}

interface PortfolioItem {
  id: number;
  slug: string;
  title: { rendered: string };
  content: { rendered: string };
  featured_media: number;
  acf?: any; // Advanced Custom Fields
}
```

## Taxonomies

```typescript
// services/wordpress-taxonomies.service.ts
export class WordPressTaxonomiesService {
  async getCategories(): Promise<Category[]> {
    const response = await axios.get(
      `${process.env.WORDPRESS_URL}/wp-json/wp/v2/categories`,
      {
        params: { per_page: 100 }
      }
    );

    return response.data;
  }

  async getTags(): Promise<Tag[]> {
    const response = await axios.get(
      `${process.env.WORDPRESS_URL}/wp-json/wp/v2/tags`,
      {
        params: { per_page: 100 }
      }
    );

    return response.data;
  }

  async createCategory(name: string, slug: string): Promise<Category> {
    const response = await this.client.post('/categories', {
      name,
      slug
    });

    return response.data;
  }
}

interface Category {
  id: number;
  count: number;
  name: string;
  slug: string;
  description: string;
  parent: number;
}

interface Tag {
  id: number;
  count: number;
  name: string;
  slug: string;
}
```

## Media

```typescript
// services/wordpress-media.service.ts
export class WordPressMediaService {
  async uploadMedia(file: File): Promise<Media> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post(
      `${process.env.WORDPRESS_URL}/wp-json/wp/v2/media`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization': `Bearer ${token}`
        }
      }
    );

    return response.data;
  }

  async getMedia(id: number): Promise<Media> {
    const response = await axios.get(
      `${process.env.WORDPRESS_URL}/wp-json/wp/v2/media/${id}`
    );

    return response.data;
  }

  async deleteMedia(id: number): Promise<void> {
    await this.client.delete(`/media/${id}`, {
      params: { force: true }
    });
  }
}

interface Media {
  id: number;
  date: string;
  slug: string;
  title: { rendered: string };
  alt_text: string;
  media_type: string;
  mime_type: string;
  media_details: {
    width: number;
    height: number;
    file: string;
    sizes: {
      [key: string]: {
        file: string;
        width: number;
        height: number;
        source_url: string;
      };
    };
  };
  source_url: string;
}
```

## Custom Endpoints

```php
// functions.php - Register custom endpoint
function register_custom_routes() {
    register_rest_route('custom/v1', '/popular-posts', array(
        'methods' => 'GET',
        'callback' => 'get_popular_posts',
        'permission_callback' => '__return_true'
    ));
}
add_action('rest_api_init', 'register_custom_routes');

function get_popular_posts($request) {
    $args = array(
        'post_type' => 'post',
        'posts_per_page' => 10,
        'meta_key' => 'post_views_count',
        'orderby' => 'meta_value_num',
        'order' => 'DESC'
    );

    $posts = get_posts($args);

    return rest_ensure_response($posts);
}
```

```typescript
// Usage
async function getPopularPosts(): Promise<Post[]> {
  const response = await axios.get(
    `${process.env.WORDPRESS_URL}/wp-json/custom/v1/popular-posts`
  );

  return response.data;
}
```

## ACF Integration

```php
// Install Advanced Custom Fields plugin
// Add fields to post type

// functions.php - Expose ACF fields in REST API
function add_acf_to_rest_api() {
    register_rest_field('post', 'acf', array(
        'get_callback' => function($post) {
            return get_fields($post['id']);
        }
    ));
}
add_action('rest_api_init', 'add_acf_to_rest_api');
```

```typescript
// Access ACF fields
interface PostWithACF extends Post {
  acf: {
    subtitle?: string;
    reading_time?: number;
    custom_field?: string;
  };
}

async function getPostWithACF(slug: string): Promise<PostWithACF> {
  const response = await axios.get(
    `${process.env.WORDPRESS_URL}/wp-json/wp/v2/posts`,
    {
      params: { slug }
    }
  );

  return response.data[0];
}
```

## Headless WordPress

```typescript
// lib/wordpress.ts
export async function getAllPosts(): Promise<Post[]> {
  const response = await fetch(
    `${process.env.WORDPRESS_URL}/wp-json/wp/v2/posts?_embed&per_page=100`
  );

  return response.json();
}

export async function getPost(slug: string): Promise<Post> {
  const response = await fetch(
    `${process.env.WORDPRESS_URL}/wp-json/wp/v2/posts?slug=${slug}&_embed`
  );

  const posts = await response.json();
  return posts[0];
}

// Parse WordPress content
export function parsePost(post: Post): ParsedPost {
  return {
    id: post.id,
    title: post.title.rendered,
    content: post.content.rendered,
    excerpt: post.excerpt.rendered,
    slug: post.slug,
    date: post.date,
    author: post._embedded?.author[0],
    featuredImage: post._embedded?.['wp:featuredmedia']?.[0],
    categories: post._embedded?.['wp:term']?.[0] || [],
    tags: post._embedded?.['wp:term']?.[1] || []
  };
}
```

## Next.js + WordPress

```typescript
// pages/blog/[slug].tsx
import { GetStaticProps, GetStaticPaths } from 'next';

export const getStaticPaths: GetStaticPaths = async () => {
  const posts = await getAllPosts();

  return {
    paths: posts.map(post => ({
      params: { slug: post.slug }
    })),
    fallback: 'blocking'
  };
};

export const getStaticProps: GetStaticProps = async ({ params }) => {
  const post = await getPost(params!.slug as string);

  if (!post) {
    return { notFound: true };
  }

  return {
    props: {
      post: parsePost(post)
    },
    revalidate: 60
  };
};

// Component
export default function BlogPost({ post }: { post: ParsedPost }) {
  return (
    <article>
      <h1>{post.title}</h1>
      <div dangerouslySetInnerHTML={{ __html: post.content }} />
    </article>
  );
}
```

## Best Practices

1. **Authentication** - Use application passwords or JWT
2. **Caching** - Cache API responses
3. **Pagination** - Handle pagination properly
4. **Embedded Data** - Use `_embed` parameter
5. **Custom Endpoints** - Create custom endpoints for complex queries
6. **ACF** - Use Advanced Custom Fields for flexibility
7. **Security** - Secure authentication credentials
8. **Performance** - Optimize API requests
9. **Error Handling** - Handle API errors gracefully
10. **ISR** - Use Incremental Static Regeneration with Next.js

---

## Quick Start

### WordPress REST API Client

```typescript
const WORDPRESS_API = 'https://yoursite.com/wp-json/wp/v2'

// Fetch posts
async function getPosts() {
  const response = await fetch(`${WORDPRESS_API}/posts`)
  return await response.json()
}

// Create post
async function createPost(post: CreatePostDto) {
  const response = await fetch(`${WORDPRESS_API}/posts`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.WP_API_TOKEN}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(post)
  })
  return await response.json()
}
```

### Next.js Integration

```typescript
// pages/blog/[slug].js
export async function getStaticProps({ params }) {
  const post = await fetch(
    `${WORDPRESS_API}/posts?slug=${params.slug}`
  ).then(res => res.json())
  
  return {
    props: { post: post[0] },
    revalidate: 60
  }
}
```

---

## Production Checklist

- [ ] **Authentication**: Application passwords or JWT configured
- [ ] **API Access**: REST API enabled
- [ ] **Caching**: Cache API responses
- [ ] **Pagination**: Handle pagination
- [ ] **Embedded Data**: Use _embed parameter
- [ ] **Custom Post Types**: Custom post types if needed
- [ ] **Media**: Media library integration
- [ ] **Webhooks**: Webhooks for content updates
- [ ] **Error Handling**: Handle API errors
- [ ] **Testing**: Test API integration
- [ ] **Documentation**: Document API usage
- [ ] **Security**: Secure API access

---

## Anti-patterns

### ❌ Don't: No Caching

```typescript
// ❌ Bad - No caching
const posts = await fetch(`${WORDPRESS_API}/posts`)
// Every request hits WordPress!
```

```typescript
// ✅ Good - Cache responses
const cacheKey = 'wordpress_posts'
let posts = await cache.get(cacheKey)
if (!posts) {
  posts = await fetch(`${WORDPRESS_API}/posts`)
  await cache.set(cacheKey, posts, 3600)  // 1 hour
}
```

### ❌ Don't: Expose Admin Credentials

```typescript
// ❌ Bad - Admin credentials
const response = await fetch(`${WORDPRESS_API}/posts`, {
  headers: {
    'Authorization': `Basic ${btoa('admin:password')}`  // Exposed!
  }
})
```

```typescript
// ✅ Good - Application password
const response = await fetch(`${WORDPRESS_API}/posts`, {
  headers: {
    'Authorization': `Bearer ${process.env.WP_APP_PASSWORD}`  // Secure
  }
})
```

---

## Integration Points

- **Headless CMS** (`33-content-management/headless-cms/`) - CMS patterns
- **Contentful Integration** (`33-content-management/contentful-integration/`) - Alternative CMS
- **Next.js Patterns** (`02-frontend/nextjs-patterns/`) - SSG/ISR

---

## Further Reading

- [WordPress REST API](https://developer.wordpress.org/rest-api/)
- [WordPress Application Passwords](https://make.wordpress.org/core/2020/11/05/application-passwords-integration-guide/)

## Resources

- [WordPress REST API Handbook](https://developer.wordpress.org/rest-api/)
- [WP REST API Authentication](https://developer.wordpress.org/rest-api/using-the-rest-api/authentication/)
- [Advanced Custom Fields](https://www.advancedcustomfields.com/)
- [Headless WordPress](https://developer.wordpress.org/rest-api/using-the-rest-api/headless-wordpress/)
