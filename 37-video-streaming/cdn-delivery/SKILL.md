---
name: CDN for Video Delivery
description: Distributing video content globally using Content Delivery Networks (CDNs) like CloudFront and Cloudflare for fast, reliable delivery with optimization strategies and caching.
---

# CDN for Video Delivery

> **Current Level:** Intermediate  
> **Domain:** Video Streaming / Infrastructure

---

## Overview

Content Delivery Networks (CDNs) distribute video content globally for fast, reliable delivery. This guide covers CloudFront, Cloudflare, and optimization strategies for building scalable video delivery systems that serve content from edge locations worldwide.

## CDN for Video Streaming

```
Origin Server → CDN Edge Locations → End Users
```

**Benefits:**
- Reduced latency
- Improved performance
- Scalability
- Cost savings
- DDoS protection

## CloudFront Setup

### Distribution Configuration

```typescript
// services/cloudfront.service.ts
import {
  CloudFrontClient,
  CreateDistributionCommand,
  CreateInvalidationCommand
} from '@aws-sdk/client-cloudfront';

export class CloudFrontService {
  private client: CloudFrontClient;

  constructor() {
    this.client = new CloudFrontClient({ region: 'us-east-1' });
  }

  async createDistribution(originDomain: string): Promise<string> {
    const command = new CreateDistributionCommand({
      DistributionConfig: {
        CallerReference: Date.now().toString(),
        Comment: 'Video streaming distribution',
        Enabled: true,
        
        Origins: {
          Quantity: 1,
          Items: [{
            Id: 'S3-Origin',
            DomainName: originDomain,
            S3OriginConfig: {
              OriginAccessIdentity: ''
            }
          }]
        },

        DefaultCacheBehavior: {
          TargetOriginId: 'S3-Origin',
          ViewerProtocolPolicy: 'redirect-to-https',
          AllowedMethods: {
            Quantity: 2,
            Items: ['GET', 'HEAD']
          },
          CachedMethods: {
            Quantity: 2,
            Items: ['GET', 'HEAD']
          },
          ForwardedValues: {
            QueryString: true,
            Cookies: { Forward: 'none' },
            Headers: {
              Quantity: 3,
              Items: ['Origin', 'Access-Control-Request-Method', 'Access-Control-Request-Headers']
            }
          },
          MinTTL: 0,
          DefaultTTL: 86400,
          MaxTTL: 31536000,
          Compress: true,
          TrustedSigners: {
            Enabled: false,
            Quantity: 0
          }
        },

        CacheBehaviors: {
          Quantity: 1,
          Items: [{
            PathPattern: '*.m3u8',
            TargetOriginId: 'S3-Origin',
            ViewerProtocolPolicy: 'redirect-to-https',
            AllowedMethods: {
              Quantity: 2,
              Items: ['GET', 'HEAD']
            },
            ForwardedValues: {
              QueryString: true,
              Cookies: { Forward: 'none' }
            },
            MinTTL: 0,
            DefaultTTL: 5,
            MaxTTL: 10,
            Compress: true
          }]
        },

        PriceClass: 'PriceClass_All',
        ViewerCertificate: {
          CloudFrontDefaultCertificate: true
        }
      }
    });

    const response = await this.client.send(command);
    return response.Distribution?.DomainName!;
  }

  async invalidateCache(distributionId: string, paths: string[]): Promise<void> {
    const command = new CreateInvalidationCommand({
      DistributionId: distributionId,
      InvalidationBatch: {
        CallerReference: Date.now().toString(),
        Paths: {
          Quantity: paths.length,
          Items: paths
        }
      }
    });

    await this.client.send(command);
  }
}
```

## Cloudflare Stream

```typescript
// services/cloudflare-stream.service.ts
export class CloudflareStreamService {
  private accountId = process.env.CLOUDFLARE_ACCOUNT_ID!;
  private apiToken = process.env.CLOUDFLARE_API_TOKEN!;
  private baseUrl = `https://api.cloudflare.com/client/v4/accounts/${this.accountId}/stream`;

  async uploadVideo(file: File): Promise<CloudflareVideo> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(this.baseUrl, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.apiToken}`
      },
      body: formData
    });

    const data = await response.json();
    return data.result;
  }

  async uploadFromUrl(url: string): Promise<CloudflareVideo> {
    const response = await fetch(this.baseUrl, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.apiToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ url })
    });

    const data = await response.json();
    return data.result;
  }

  async getVideo(videoId: string): Promise<CloudflareVideo> {
    const response = await fetch(`${this.baseUrl}/${videoId}`, {
      headers: {
        'Authorization': `Bearer ${this.apiToken}`
      }
    });

    const data = await response.json();
    return data.result;
  }

  async deleteVideo(videoId: string): Promise<void> {
    await fetch(`${this.baseUrl}/${videoId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${this.apiToken}`
      }
    });
  }

  getPlaybackUrl(videoId: string): string {
    return `https://customer-${this.accountId}.cloudflarestream.com/${videoId}/manifest/video.m3u8`;
  }
}

interface CloudflareVideo {
  uid: string;
  status: {
    state: string;
    pctComplete: number;
  };
  playback: {
    hls: string;
    dash: string;
  };
  thumbnail: string;
  duration: number;
}
```

## Origin Shield

```typescript
// Origin Shield configuration
const originShieldConfig = {
  enabled: true,
  region: 'us-east-1', // Closest to origin
  
  // Benefits:
  // - Reduces load on origin
  // - Improves cache hit ratio
  // - Protects origin from traffic spikes
};

// CloudFront with Origin Shield
const distributionConfig = {
  Origins: {
    Items: [{
      Id: 'S3-Origin',
      DomainName: 's3.amazonaws.com',
      OriginShield: {
        Enabled: true,
        OriginShieldRegion: 'us-east-1'
      }
    }]
  }
};
```

## Cache Control

```typescript
// services/cache-control.service.ts
export class CacheControlService {
  getCacheHeaders(fileType: string): Record<string, string> {
    switch (fileType) {
      case 'm3u8':
        // Playlist files - short cache
        return {
          'Cache-Control': 'public, max-age=5, s-maxage=5',
          'Content-Type': 'application/vnd.apple.mpegurl'
        };

      case 'ts':
      case 'm4s':
        // Video segments - long cache (immutable)
        return {
          'Cache-Control': 'public, max-age=31536000, immutable',
          'Content-Type': 'video/mp2t'
        };

      case 'mp4':
        // Progressive download - medium cache
        return {
          'Cache-Control': 'public, max-age=86400',
          'Content-Type': 'video/mp4'
        };

      case 'jpg':
      case 'png':
        // Thumbnails - long cache
        return {
          'Cache-Control': 'public, max-age=604800',
          'Content-Type': `image/${fileType}`
        };

      default:
        return {
          'Cache-Control': 'public, max-age=3600'
        };
    }
  }

  async uploadWithCacheHeaders(s3Key: string, filePath: string, fileType: string): Promise<void> {
    const headers = this.getCacheHeaders(fileType);

    await s3Client.send(new PutObjectCommand({
      Bucket: process.env.S3_BUCKET!,
      Key: s3Key,
      Body: fs.createReadStream(filePath),
      CacheControl: headers['Cache-Control'],
      ContentType: headers['Content-Type']
    }));
  }
}
```

## Token Authentication

```typescript
// services/signed-url.service.ts
import { getSignedUrl } from '@aws-sdk/cloudfront-signer';

export class SignedUrlService {
  private keyPairId = process.env.CLOUDFRONT_KEY_PAIR_ID!;
  private privateKey = process.env.CLOUDFRONT_PRIVATE_KEY!;

  generateSignedUrl(url: string, expiresIn: number = 3600): string {
    const expires = new Date(Date.now() + expiresIn * 1000);

    return getSignedUrl({
      url,
      keyPairId: this.keyPairId,
      privateKey: this.privateKey,
      dateLessThan: expires.toISOString()
    });
  }

  generateSignedCookie(domain: string, expiresIn: number = 3600): SignedCookies {
    const expires = new Date(Date.now() + expiresIn * 1000);

    const policy = {
      Statement: [{
        Resource: `https://${domain}/*`,
        Condition: {
          DateLessThan: {
            'AWS:EpochTime': Math.floor(expires.getTime() / 1000)
          }
        }
      }]
    };

    const policyString = JSON.stringify(policy);
    const signature = this.sign(policyString);

    return {
      'CloudFront-Policy': Buffer.from(policyString).toString('base64'),
      'CloudFront-Signature': signature,
      'CloudFront-Key-Pair-Id': this.keyPairId
    };
  }

  private sign(data: string): string {
    const crypto = require('crypto');
    const sign = crypto.createSign('RSA-SHA1');
    sign.update(data);
    return sign.sign(this.privateKey, 'base64');
  }
}

interface SignedCookies {
  'CloudFront-Policy': string;
  'CloudFront-Signature': string;
  'CloudFront-Key-Pair-Id': string;
}
```

## Geographic Distribution

```typescript
// Geographic routing configuration
const geoDistribution = {
  regions: [
    {
      name: 'North America',
      edgeLocations: ['us-east-1', 'us-west-1', 'ca-central-1'],
      priceClass: 'PriceClass_100'
    },
    {
      name: 'Europe',
      edgeLocations: ['eu-west-1', 'eu-central-1'],
      priceClass: 'PriceClass_200'
    },
    {
      name: 'Asia Pacific',
      edgeLocations: ['ap-southeast-1', 'ap-northeast-1'],
      priceClass: 'PriceClass_All'
    }
  ]
};

// Geo-restriction
const geoRestriction = {
  RestrictionType: 'whitelist', // or 'blacklist'
  Quantity: 2,
  Items: ['US', 'CA'] // ISO country codes
};
```

## Cost Optimization

```typescript
// services/cdn-cost-optimizer.service.ts
export class CDNCostOptimizer {
  async optimizeCosts(videoId: string): Promise<void> {
    const video = await db.video.findUnique({ where: { id: videoId } });

    if (!video) return;

    // Use cheaper price class for low-traffic videos
    if (video.views < 1000) {
      await this.setPriceClass(videoId, 'PriceClass_100');
    }

    // Compress videos
    await this.enableCompression(videoId);

    // Set appropriate cache TTLs
    await this.optimizeCacheTTL(videoId);

    // Use origin shield for popular videos
    if (video.views > 10000) {
      await this.enableOriginShield(videoId);
    }
  }

  private async setPriceClass(videoId: string, priceClass: string): Promise<void> {
    // Update CloudFront distribution
  }

  private async enableCompression(videoId: string): Promise<void> {
    // Enable Gzip/Brotli compression
  }

  private async optimizeCacheTTL(videoId: string): Promise<void> {
    // Set optimal cache TTLs
  }

  private async enableOriginShield(videoId: string): Promise<void> {
    // Enable origin shield
  }
}
```

## Performance Monitoring

```typescript
// services/cdn-monitoring.service.ts
export class CDNMonitoringService {
  async getPerformanceMetrics(distributionId: string): Promise<CDNMetrics> {
    // Get CloudWatch metrics
    const metrics = await cloudwatch.getMetricStatistics({
      Namespace: 'AWS/CloudFront',
      MetricName: 'Requests',
      Dimensions: [{
        Name: 'DistributionId',
        Value: distributionId
      }],
      StartTime: new Date(Date.now() - 24 * 60 * 60 * 1000),
      EndTime: new Date(),
      Period: 3600,
      Statistics: ['Sum', 'Average']
    });

    return {
      requests: metrics.Datapoints?.reduce((sum, dp) => sum + (dp.Sum || 0), 0) || 0,
      cacheHitRate: await this.getCacheHitRate(distributionId),
      bandwidth: await this.getBandwidth(distributionId),
      errors: await this.getErrorRate(distributionId)
    };
  }

  private async getCacheHitRate(distributionId: string): Promise<number> {
    // Calculate cache hit rate
    return 0;
  }

  private async getBandwidth(distributionId: string): Promise<number> {
    // Get bandwidth usage
    return 0;
  }

  private async getErrorRate(distributionId: string): Promise<number> {
    // Get error rate
    return 0;
  }
}

interface CDNMetrics {
  requests: number;
  cacheHitRate: number;
  bandwidth: number;
  errors: number;
}
```

## Failover Strategies

```typescript
// Multi-CDN failover
export class CDNFailoverService {
  private primaryCDN = 'cloudfront.net';
  private secondaryCDN = 'cloudflare.com';

  async getVideoUrl(videoId: string): Promise<string> {
    // Try primary CDN
    const primaryUrl = `https://${this.primaryCDN}/videos/${videoId}.m3u8`;
    
    if (await this.isAvailable(primaryUrl)) {
      return primaryUrl;
    }

    // Fallback to secondary CDN
    const secondaryUrl = `https://${this.secondaryCDN}/videos/${videoId}.m3u8`;
    
    if (await this.isAvailable(secondaryUrl)) {
      return secondaryUrl;
    }

    // Fallback to origin
    return `https://origin.example.com/videos/${videoId}.m3u8`;
  }

  private async isAvailable(url: string): Promise<boolean> {
    try {
      const response = await fetch(url, { method: 'HEAD', timeout: 2000 });
      return response.ok;
    } catch {
      return false;
    }
  }
}
```

## Best Practices

1. **Cache Control** - Set appropriate cache headers
2. **Compression** - Enable Gzip/Brotli compression
3. **Origin Shield** - Use for high-traffic content
4. **Signed URLs** - Secure premium content
5. **Geographic Distribution** - Use edge locations globally
6. **Cost Optimization** - Choose appropriate price class
7. **Monitoring** - Monitor CDN performance
8. **Failover** - Implement multi-CDN strategy
9. **Invalidation** - Invalidate cache when needed
10. **Testing** - Test from different regions

---

## Quick Start

### CloudFront Setup

```yaml
# CloudFormation
Resources:
  VideoDistribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      DistributionConfig:
        Origins:
          - DomainName: video.example.com
            Id: video-origin
            CustomOriginConfig:
              HTTPPort: 80
              OriginProtocolPolicy: https-only
        DefaultCacheBehavior:
          TargetOriginId: video-origin
          ViewerProtocolPolicy: redirect-to-https
          CachePolicyId: 4135ea2d-6df8-44a3-9df3-4b5a84be39ad  # CachingOptimized
          Compress: true
```

### Signed URLs

```typescript
import { CloudFrontSigner } from '@aws-sdk/cloudfront-signer'

const signer = new CloudFrontSigner({
  keyPairId: process.env.CF_KEY_PAIR_ID,
  privateKey: process.env.CF_PRIVATE_KEY
})

// Generate signed URL (valid for 1 hour)
const signedUrl = signer.getSignedUrl({
  url: 'https://cdn.example.com/video.mp4',
  expiresIn: 3600
})
```

---

## Production Checklist

- [ ] **CDN Setup**: CDN configured (CloudFront, Cloudflare)
- [ ] **Origin**: Origin server configured
- [ ] **Cache Control**: Appropriate cache headers
- [ ] **Compression**: Enable compression (Gzip/Brotli)
- [ ] **HTTPS**: HTTPS enabled
- [ ] **Signed URLs**: Signed URLs for premium content
- [ ] **Geographic Distribution**: Edge locations globally
- [ ] **Monitoring**: Monitor CDN performance
- [ ] **Analytics**: CDN analytics
- [ ] **Error Handling**: Handle CDN errors
- [ ] **Testing**: Test CDN delivery
- [ ] **Documentation**: Document CDN setup

---

## Anti-patterns

### ❌ Don't: No Caching

```http
# ❌ Bad - No cache headers
HTTP/1.1 200 OK
Content-Type: video/mp4
# No cache!
```

```http
# ✅ Good - Cache headers
HTTP/1.1 200 OK
Content-Type: video/mp4
Cache-Control: public, max-age=31536000
# Cached for 1 year
```

### ❌ Don't: Single Origin

```markdown
# ❌ Bad - Single origin
All users → Origin server
# High latency for distant users!
```

```markdown
# ✅ Good - CDN
Users → Nearest edge location → Origin (if needed)
# Low latency globally
```

---

## Integration Points

- **Adaptive Bitrate** (`37-video-streaming/adaptive-bitrate/`) - ABR delivery
- **Live Streaming** (`37-video-streaming/live-streaming/`) - Live CDN
- **Video Analytics** (`37-video-streaming/video-analytics/`) - CDN metrics

---

## Further Reading

- [AWS CloudFront](https://aws.amazon.com/cloudfront/)
- [Cloudflare CDN](https://www.cloudflare.com/cdn/)
- [CDN Best Practices](https://www.cloudflare.com/learning/cdn/what-is-a-cdn/)

## Resources

- [AWS CloudFront](https://aws.amazon.com/cloudfront/)
- [Cloudflare Stream](https://www.cloudflare.com/products/cloudflare-stream/)
- [Fastly](https://www.fastly.com/)
- [Akamai](https://www.akamai.com/)
- [CDN Performance Testing](https://www.cdnperf.com/)
