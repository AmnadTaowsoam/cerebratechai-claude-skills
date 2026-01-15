# CDN Integration

## Overview

Content Delivery Networks (CDNs) distribute content across multiple geographical locations to reduce latency, improve load times, and reduce bandwidth costs. This skill covers CloudFront and Cloudflare CDN integration patterns.

## Table of Contents

1. [CDN Concepts](#cdn-concepts)
2. [CloudFront Setup](#cloudfront-setup)
3. [Cloudflare Setup](#cloudflare-setup)
4. [Cache Control Headers](#cache-control-headers)
5. [Invalidation](#invalidation)
6. [Signed URLs/Cookies](#signed-urlscookies)
7. [Custom Domains](#custom-domains)
8. [SSL/TLS](#ssltls)
9. [Performance Optimization](#performance-optimization)
10. [Cost Optimization](#cost-optimization)
11. [Monitoring](#monitoring)

---

## CDN Concepts

### How CDNs Work

```
User Request
    ↓
Nearest Edge Location
    ↓
    ├─ Cached? → Serve from Cache
    └─ Not Cached? → Fetch from Origin → Cache → Serve
```

### Key Benefits

1. **Reduced Latency**: Content served from edge locations near users
2. **Improved Performance**: Faster load times
3. **Reduced Bandwidth Costs**: Less traffic to origin servers
4. **High Availability**: Distributed infrastructure
5. **DDoS Protection**: Built-in security features

### CDN Terminology

| Term | Description |
|------|-------------|
| **Origin** | The source server where original content is stored |
| **Edge Location** | CDN server locations distributed globally |
| **Distribution** | The configuration that connects origin to CDN |
| **Cache Hit** | Content served from CDN cache |
| **Cache Miss** | Content fetched from origin |
| **TTL** | Time To Live - how long content is cached |
| **Invalidation** | Removing content from CDN cache |

---

## CloudFront Setup

### Distribution Creation

#### Terraform Configuration

```hcl
# cloudfront.tf
resource "aws_cloudfront_distribution" "main" {
  enabled             = true
  is_ipv6_enabled     = true
  price_class         = "PriceClass_All" # All edge locations

  origin {
    domain_name = aws_s3_bucket.website.bucket_regional_domain_name
    origin_id   = "S3-${aws_s3_bucket.website.id}"

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.main.cloudfront_access_identity_path
    }
  }

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3-${aws_s3_bucket.website.id}"

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 86400  # 1 day
    max_ttl                = 31536000  # 1 year
    compress               = true
  }

  ordered_cache_behavior {
    path_pattern     = "/api/*"
    allowed_methods  = ["GET", "HEAD", "POST", "PUT", "DELETE", "OPTIONS"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "api-origin"

    forwarded_values {
      query_string = true
      headers      = ["Authorization", "Content-Type"]
      cookies {
        forward = "all"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 0
    max_ttl                = 0
    compress               = false
  }

  viewer_certificate {
    acm_certificate_arn      = aws_acm_certificate.main.arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  custom_error_response {
    error_code            = 404
    response_code         = 200
    response_page_path    = "/index.html"
  }
}

resource "aws_cloudfront_origin_access_identity" "main" {
  comment = "Access identity for S3 bucket"
}
```

#### AWS CLI

```bash
# Create CloudFront distribution
aws cloudfront create-distribution \
  --distribution-config file://distribution-config.json
```

```json
// distribution-config.json
{
  "CallerReference": "unique-reference",
  "Comment": "Main website distribution",
  "DefaultCacheBehavior": {
    "TargetOriginId": "S3-bucket-name",
    "ViewerProtocolPolicy": "redirect-to-https",
    "MinTTL": 0,
    "DefaultTTL": 86400,
    "MaxTTL": 31536000,
    "ForwardedValues": {
      "QueryString": false,
      "Cookies": { "Forward": "none" }
    },
    "Compress": true,
    "AllowedMethods": ["GET", "HEAD", "OPTIONS"],
    "CachedMethods": ["GET", "HEAD"]
  },
  "Origins": {
    "Items": [
      {
        "Id": "S3-bucket-name",
        "DomainName": "bucket-name.s3.amazonaws.com",
        "S3OriginConfig": {
          "OriginAccessIdentity": "origin-access-identity/cloudfront/IDENTITY_ID"
        }
      }
    ],
    "Quantity": 1
  },
  "DefaultRootObject": "index.html",
  "Enabled": true,
  "PriceClass": "PriceClass_All",
  "ViewerCertificate": {
    "ACMCertificateArn": "arn:aws:acm:us-east-1:123456789012:certificate/abcd1234",
    "SSLSupportMethod": "sni-only",
    "MinimumProtocolVersion": "TLSv1.2_2021"
  },
  "CustomErrorResponses": {
    "Quantity": 1,
    "Items": [
      {
        "ErrorCode": 404,
        "ResponsePagePath": "/index.html",
        "ResponseCode": "200"
      }
    ]
  }
}
```

### Origin Configuration

#### S3 Origin with OAI

```typescript
// s3-origin.ts
import { S3Client, PutBucketPolicyCommand } from '@aws-sdk/client-s3';

const s3Client = new S3Client({ region: 'us-east-1' });

async function configureS3ForCloudFront(
  bucketName: string,
  cloudFrontOriginAccessIdentity: string
): Promise<void> {
  const policy = {
    Version: '2012-10-17',
    Statement: [
      {
        Sid: 'AllowCloudFrontAccess',
        Effect: 'Allow',
        Principal: {
          AWS: cloudFrontOriginAccessIdentity,
        },
        Action: 's3:GetObject',
        Resource: `arn:aws:s3:::${bucketName}/*`,
      },
    ],
  };

  await s3Client.send(new PutBucketPolicyCommand({
    Bucket: bucketName,
    Policy: JSON.stringify(policy),
  }));
}
```

#### Custom Origin (Load Balancer)

```hcl
# custom-origin.tf
resource "aws_cloudfront_distribution" "api" {
  origin {
    domain_name = aws_lb.api.dns_name
    origin_id   = "api-lb"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "https-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  default_cache_behavior {
    target_origin_id       = "api-lb"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods        = ["GET", "HEAD", "POST", "PUT", "DELETE", "OPTIONS"]
    cached_methods         = ["GET", "HEAD"]
    
    forwarded_values {
      query_string = true
      headers      = ["Authorization", "Content-Type", "Host"]
      cookies {
        forward = "all"
      }
    }
    
    min_ttl     = 0
    default_ttl = 0
    max_ttl     = 0
  }
}
```

### Behaviors

#### Multiple Cache Behaviors

```hcl
# cache-behaviors.tf
resource "aws_cloudfront_distribution" "main" {
  # ... origin configuration ...

  ordered_cache_behavior {
    path_pattern           = "/images/*"
    target_origin_id       = "S3-images"
    viewer_protocol_policy = "redirect-to-https"
    
    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }
    
    min_ttl     = 86400    # 1 day
    default_ttl = 604800   # 1 week
    max_ttl     = 31536000 # 1 year
    compress    = false
  }

  ordered_cache_behavior {
    path_pattern           = "/api/*"
    target_origin_id       = "api-origin"
    viewer_protocol_policy = "redirect-to-https"
    
    forwarded_values {
      query_string = true
      headers      = ["Authorization", "Content-Type"]
      cookies {
        forward = "all"
      }
    }
    
    min_ttl     = 0
    default_ttl = 0
    max_ttl     = 0
    compress    = false
  }

  ordered_cache_behavior {
    path_pattern           = "/static/*"
    target_origin_id       = "S3-assets"
    viewer_protocol_policy = "redirect-to-https"
    
    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }
    
    min_ttl     = 604800   # 1 week
    default_ttl = 2592000  # 30 days
    max_ttl     = 31536000 # 1 year
    compress    = true
  }
}
```

---

## Cloudflare Setup

### Zone Configuration

#### Terraform

```hcl
# cloudflare.tf
resource "cloudflare_zone" "main" {
  zone = "example.com"
}

resource "cloudflare_record" "www" {
  zone_id = cloudflare_zone.main.id
  name    = "www"
  value   = "192.0.2.1" # Your origin IP
  type    = "A"
  proxied = true
}

resource "cloudflare_record" "api" {
  zone_id = cloudflare_zone.main.id
  name    = "api"
  value   = "api.example.com"
  type    = "CNAME"
  proxied = true
}
```

### Page Rules

```hcl
# page-rules.tf
resource "cloudflare_page_rule" "cache_static" {
  zone_id  = cloudflare_zone.main.id
  target   = "example.com/static/*"
  priority = 1

  actions {
    cache_level              = "cache_everything"
    edge_cache_ttl           = 2592000 # 30 days
    browser_cache_ttl        = 2592000
    bypass_cache_on_cookie  = false
  }
}

resource "cloudflare_page_rule" "no_cache_api" {
  zone_id  = cloudflare_zone.main.id
  target   = "example.com/api/*"
  priority = 2

  actions {
    cache_level     = "bypass"
    disable_performance = true
  }
}

resource "cloudflare_page_rule" "redirect_https" {
  zone_id  = cloudflare_zone.main.id
  target   = "example.com/*"
  priority = 3

  actions {
    always_use_https = true
  }
}
```

### Workers

```javascript
// worker.js
// Cloudflare Worker for custom caching logic

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // Add custom headers
    const response = await fetch(request);
    
    // Cache API responses for 5 minutes
    if (url.pathname.startsWith('/api/')) {
      const newResponse = new Response(response.body, response);
      newResponse.headers.set('Cache-Control', 'public, max-age=300');
      return newResponse;
    }
    
    return response;
  }
};
```

---

## Cache Control Headers

### HTTP Cache Headers

```typescript
// cache-headers.ts

// Static assets (long cache)
const staticAssetHeaders = {
  'Cache-Control': 'public, max-age=31536000, immutable',
  'Vary': 'Accept-Encoding',
};

// HTML files (short cache)
const htmlHeaders = {
  'Cache-Control': 'public, max-age=0, must-revalidate',
  'Vary': 'Accept-Encoding',
};

// API responses (conditional cache)
const apiHeaders = {
  'Cache-Control': 'public, max-age=300, s-maxage=600',
  'Vary': 'Accept, Accept-Encoding, Authorization',
};

// No cache
const noCacheHeaders = {
  'Cache-Control': 'no-store, no-cache, must-revalidate, proxy-revalidate',
  'Pragma': 'no-cache',
  'Expires': '0',
};

// Express middleware
import express from 'express';

function cacheControl(maxAge: number, options: { public?: boolean; immutable?: boolean } = {}) {
  return (req: express.Request, res: express.Response, next: express.NextFunction) => {
    const directives: string[] = [];

    if (options.public !== false) {
      directives.push('public');
    }

    directives.push(`max-age=${maxAge}`);

    if (options.immutable) {
      directives.push('immutable');
    }

    res.setHeader('Cache-Control', directives.join(', '));
    res.setHeader('Vary', 'Accept-Encoding');
    next();
  };
}

// Usage
app.use('/static', cacheControl(31536000, { immutable: true }));
app.use('/api', cacheControl(300));
```

### Cache Strategies

| Content Type | Cache Strategy | TTL |
|--------------|----------------|-----|
| Images, Fonts, CSS, JS | Long cache, immutable | 1 year |
| HTML | Short cache, revalidate | 0-5 minutes |
| API GET responses | Conditional cache | 1-10 minutes |
| API POST/PUT/DELETE | No cache | 0 |
| User-specific content | No cache | 0 |

---

## Invalidation

### CloudFront Invalidation

#### AWS CLI

```bash
# Invalidate single file
aws cloudfront create-invalidation \
  --distribution-id DISTRIBUTION_ID \
  --paths "/index.html"

# Invalidate directory
aws cloudfront create-invalidation \
  --distribution-id DISTRIBUTION_ID \
  --paths "/images/*"

# Invalidate multiple paths
aws cloudfront create-invalidation \
  --distribution-id DISTRIBUTION_ID \
  --paths "/index.html" "/css/*" "/js/*"
```

#### Node.js SDK

```typescript
// invalidation.ts
import { CloudFrontClient, CreateInvalidationCommand } from '@aws-sdk/client-cloudfront';

const cloudFront = new CloudFrontClient({ region: 'us-east-1' });

async function createInvalidation(
  distributionId: string,
  paths: string[],
  callerReference?: string
): Promise<string> {
  const command = new CreateInvalidationCommand({
    DistributionId: distributionId,
    InvalidationBatch: {
      CallerReference: callerReference || Date.now().toString(),
      Paths: {
        Quantity: paths.length,
        Items: paths,
      },
    },
  });

  const response = await cloudFront.send(command);
  return response.Invalidation?.Id || '';
}

// Usage
const invalidationId = await createInvalidation(
  'DISTRIBUTION_ID',
  ['/index.html', '/css/*', '/js/*']
);

console.log(`Invalidation created: ${invalidationId}`);
```

### Cloudflare Cache Purge

#### API

```typescript
// cloudflare-purge.ts
async function purgeCloudflareCache(
  zoneId: string,
  apiToken: string,
  files: string[]
): Promise<void> {
  const response = await fetch(
    `https://api.cloudflare.com/client/v4/zones/${zoneId}/purge_cache`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ files }),
    }
  );

  if (!response.ok) {
    throw new Error('Failed to purge cache');
  }
}

// Purge entire zone
async function purgeEntireZone(
  zoneId: string,
  apiToken: string
): Promise<void> {
  const response = await fetch(
    `https://api.cloudflare.com/client/v4/zones/${zoneId}/purge_cache`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ purge_everything: true }),
    }
  );

  if (!response.ok) {
    throw new Error('Failed to purge cache');
  }
}
```

### Automated Invalidation

```typescript
// auto-invalidation.ts
import { S3Client, ListObjectsV2Command } from '@aws-sdk/client-s3';

async function invalidateChangedFiles(
  distributionId: string,
  bucketName: string,
  prefix: string
): Promise<void> {
  const s3 = new S3Client({ region: 'us-east-1' });

  // List files in bucket
  const listCommand = new ListObjectsV2Command({
    Bucket: bucketName,
    Prefix: prefix,
  });

  const response = await s3.send(listCommand);
  const files = response.Contents?.map(obj => `/${obj.Key}`) || [];

  if (files.length > 0) {
    await createInvalidation(distributionId, files);
    console.log(`Invalidated ${files.length} files`);
  }
}

// Invalidation on deployment
import { execSync } from 'child_process';

function deployAndInvalidate(): void {
  // Deploy to S3
  execSync('aws s3 sync ./dist s3://my-bucket --delete');

  // Invalidate CloudFront
  execSync('aws cloudfront create-invalidation --distribution-id DISTRIBUTION_ID --paths "/*"');
}
```

---

## Signed URLs/Cookies

### CloudFront Signed URLs

```typescript
// signed-url.ts
import crypto from 'crypto';

interface SignedUrlOptions {
  url: string;
  privateKey: string;
  keyPairId: string;
  expires: number; // Unix timestamp
}

function createSignedURL(options: SignedUrlOptions): string {
  const { url, privateKey, keyPairId, expires } = options;

  const parsedUrl = new URL(url);
  const expiresEpoch = Math.floor(expires / 1000);

  const policy = {
    Statement: [
      {
        Resource: parsedUrl.pathname,
        Condition: {
          DateLessThan: {
            'AWS:EpochTime': expiresEpoch,
          },
        },
      },
    ],
  };

  const policyBase64 = Buffer.from(JSON.stringify(policy)).toString('base64');
  const signature = crypto
    .createSign('RSA-SHA1')
    .update(policyBase64)
    .sign(privateKey, 'base64');

  parsedUrl.searchParams.set('Policy', policyBase64);
  parsedUrl.searchParams.set('Signature', signature);
  parsedUrl.searchParams.set('Key-Pair-Id', keyPairId);

  return parsedUrl.toString();
}

// Usage
const signedUrl = createSignedURL({
  url: 'https://d123456.cloudfront.net/private/video.mp4',
  privateKey: process.env.CLOUDFRONT_PRIVATE_KEY!,
  keyPairId: process.env.CLOUDFRONT_KEY_PAIR_ID!,
  expires: Date.now() + 3600000, // 1 hour from now
});
```

### CloudFront Signed Cookies

```typescript
// signed-cookie.ts
import crypto from 'crypto';

interface SignedCookieOptions {
  domain: string;
  privateKey: string;
  keyPairId: string;
  expires: number;
}

function createSignedCookies(options: SignedCookieOptions): Record<string, string> {
  const { domain, privateKey, keyPairId, expires } = options;
  const expiresEpoch = Math.floor(expires / 1000);

  const policy = {
    Statement: [
      {
        Resource: `https://${domain}/*`,
        Condition: {
          DateLessThan: {
            'AWS:EpochTime': expiresEpoch,
          },
        },
      },
    ],
  };

  const policyBase64 = Buffer.from(JSON.stringify(policy)).toString('base64');
  const signature = crypto
    .createSign('RSA-SHA1')
    .update(policyBase64)
    .sign(privateKey, 'base64');

  return {
    'CloudFront-Policy': policyBase64,
    'CloudFront-Signature': signature,
    'CloudFront-Key-Pair-Id': keyPairId,
  };
}

// Express middleware
function signedCookieMiddleware(options: SignedCookieOptions) {
  return (req: express.Request, res: express.Response, next: express.NextFunction) => {
    const cookies = createSignedCookies(options);

    for (const [name, value] of Object.entries(cookies)) {
      res.cookie(name, value, {
        domain: options.domain,
        path: '/',
        httpOnly: true,
        secure: true,
        sameSite: 'strict',
      });
    }

    next();
  };
}
```

---

## Custom Domains

### CloudFront Custom Domain

```hcl
# custom-domain.tf
resource "aws_cloudfront_distribution" "main" {
  aliases = ["www.example.com", "example.com"]

  viewer_certificate {
    acm_certificate_arn      = aws_acm_certificate.main.arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }
}

resource "aws_acm_certificate" "main" {
  domain_name       = "example.com"
  validation_method = "DNS"

  subject_alternative_names = [
    "www.example.com",
  ]

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_route53_record" "cert_validation" {
  for_each = {
    for dvo in aws_acm_certificate.main.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = aws_route53_zone.main.zone_id
}

resource "aws_route53_record" "www" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "www"
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.main.domain_name
    zone_id                = aws_cloudfront_distribution.main.hosted_zone_id
    evaluate_target_health = true
  }
}
```

### Cloudflare Custom Domain

```hcl
# cloudflare-domain.tf
resource "cloudflare_zone" "main" {
  zone = "example.com"
}

resource "cloudflare_record" "www" {
  zone_id = cloudflare_zone.main.id
  name    = "www"
  value   = "192.0.2.1"
  type    = "A"
  proxied = true
}

resource "cloudflare_record" "root" {
  zone_id = cloudflare_zone.main.id
  name    = "@"
  value   = "192.0.2.1"
  type    = "A"
  proxied = true
}
```

---

## SSL/TLS

### CloudFront SSL Configuration

```hcl
# ssl.tf
resource "aws_acm_certificate" "main" {
  domain_name       = "example.com"
  validation_method = "DNS"

  subject_alternative_names = [
    "*.example.com",
    "example.com",
  ]

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_cloudfront_distribution" "main" {
  viewer_certificate {
    acm_certificate_arn      = aws_acm_certificate.main.arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }
}
```

### Cloudflare SSL

```hcl
# cloudflare-ssl.tf
resource "cloudflare_zone_settings_override" "ssl" {
  zone_id = cloudflare_zone.main.id

  settings {
    id = "ssl"
    value = "full" # or "strict", "flexible", "off"
  }

  settings {
    id = "always_use_https"
    value = "on"
  }

  settings {
    id = "min_tls_version"
    value = "1.2"
  }
}
```

---

## Performance Optimization

### Image Optimization

```typescript
// image-optimization.ts

// CloudFront with Lambda@Edge for image optimization
export const handler = async (event: any) => {
  const request = event.Records[0].cf.request;
  const uri = request.uri;

  if (!uri.match(/\.(jpg|jpeg|png|webp)$/i)) {
    return request;
  }

  // Parse query parameters for transformations
  const query = request.querystring;
  const width = query.width ? parseInt(query.width[0].value) : null;
  const quality = query.quality ? parseInt(query.quality[0].value) : 80;

  if (width || quality) {
    // Add transformation parameters
    request.querystring = {
      ...request.querystring,
      width: width ? [{ value: width.toString() }] : undefined,
      quality: [{ value: quality.toString() }],
    };
  }

  return request;
};
```

### Brotli Compression

```hcl
# compression.tf
resource "aws_cloudfront_distribution" "main" {
  default_cache_behavior {
    compress = true
  }

  # CloudFront automatically supports Brotli compression
  # No additional configuration needed
}
```

### HTTP/3 (QUIC)

```hcl
# http3.tf
resource "aws_cloudfront_distribution" "main" {
  http_version = "http3" # or "http2", "http2and3"
}
```

---

## Cost Optimization

### Price Classes

```hcl
# price-class.tf
resource "aws_cloudfront_distribution" "main" {
  price_class = "PriceClass_100" # Options:
  # PriceClass_All: All edge locations (most expensive)
  # PriceClass_200: Most popular locations
  # PriceClass_100: Least expensive locations
}
```

### Cache Optimization

```typescript
// cache-optimization.ts

// Set appropriate cache headers
const cacheHeaders = {
  // Static assets: Long cache
  '/static/*': 'public, max-age=31536000, immutable',
  
  // API responses: Short cache
  '/api/*': 'public, max-age=300, s-maxage=600',
  
  // HTML: No cache
  '/*.html': 'public, max-age=0, must-revalidate',
};

// Implement cache warming
async function warmCache(urls: string[]): Promise<void> {
  for (const url of urls) {
    await fetch(url);
    console.log(`Warmed: ${url}`);
  }
}
```

### Cloudflare Argo Smart Routing

```hcl
# argo.tf
resource "cloudflare_zone_settings_override" "argo" {
  zone_id = cloudflare_zone.main.id

  settings {
    id = "argo_smart_routing"
    value = "on"
  }

  settings {
    id = "always_online"
    value = "on"
  }
}
```

---

## Monitoring

### CloudFront Metrics

```typescript
// cloudfront-monitoring.ts
import { CloudWatchClient, GetMetricStatisticsCommand } from '@aws-sdk/client-cloudwatch';

const cloudWatch = new CloudWatchClient({ region: 'us-east-1' });

async function getCloudFrontMetrics(
  distributionId: string,
  metricName: string,
  period: number = 3600
): Promise<any[]> {
  const endTime = new Date();
  const startTime = new Date(endTime.getTime() - 24 * 60 * 60 * 1000); // 24 hours ago

  const command = new GetMetricStatisticsCommand({
    Namespace: 'AWS/CloudFront',
    MetricName: metricName,
    Dimensions: [
      {
        Name: 'DistributionId',
        Value: distributionId,
      },
      {
        Name: 'Region',
        Value: 'Global',
      },
    ],
    StartTime: startTime,
    EndTime: endTime,
    Period: period,
    Statistics: ['Sum', 'Average'],
  });

  const response = await cloudWatch.send(command);
  return response.Datapoints || [];
}

// Key metrics to monitor
const metrics = [
  'Requests',           // Total requests
  'BytesDownloaded',    // Total bytes transferred
  'BytesUploaded',      // Total bytes uploaded to origin
  '4xxErrorRate',       // Client error rate
  '5xxErrorRate',       // Server error rate
  'TotalErrorRate',     // Overall error rate
  'CacheHitRate',       // Cache hit ratio
];

// Usage
for (const metric of metrics) {
  const data = await getCloudFrontMetrics('DISTRIBUTION_ID', metric);
  console.log(`${metric}:`, data);
}
```

### Cloudflare Analytics

```typescript
// cloudflare-analytics.ts
async function getCloudflareAnalytics(
  zoneId: string,
  apiToken: string,
  since: Date,
  until: Date
): Promise<any> {
  const response = await fetch(
    `https://api.cloudflare.com/client/v4/zones/${zoneId}/analytics/dashboard?since=${since.toISOString()}&until=${until.toISOString()}`,
    {
      headers: {
        'Authorization': `Bearer ${apiToken}`,
      },
    }
  );

  if (!response.ok) {
    throw new Error('Failed to fetch analytics');
  }

  return response.json();
}

// Usage
const analytics = await getCloudflareAnalytics(
  'ZONE_ID',
  'API_TOKEN',
  new Date(Date.now() - 24 * 60 * 60 * 1000), // 24 hours ago
  new Date()
);

console.log('Analytics:', analytics);
```

---

## Summary

This skill covers comprehensive CDN integration patterns including:

- **CDN Concepts**: How CDNs work, key benefits, and terminology
- **CloudFront Setup**: Distribution creation, origin configuration, and cache behaviors
- **Cloudflare Setup**: Zone configuration, page rules, and workers
- **Cache Control Headers**: HTTP cache headers and strategies
- **Invalidation**: CloudFront and Cloudflare cache invalidation
- **Signed URLs/Cookies**: Securing content with signed URLs and cookies
- **Custom Domains**: Setting up custom domains with SSL/TLS
- **SSL/TLS**: Certificate management and SSL configuration
- **Performance Optimization**: Image optimization, compression, and HTTP/3
- **Cost Optimization**: Price classes and cache optimization
- **Monitoring**: CloudFront and Cloudflare analytics
