---
name: Storage and Egress Optimization
description: Strategies for reducing cloud storage costs and minimizing expensive data transfer (egress) fees.
---

# Storage and Egress Optimization

## Overview

Storage and Egress costs are often the "hidden killers" of cloud bills. While compute gets most of the attention, data transfer (egress) and long-term storage can silently consume 30-50% of your infrastructure budget.

**Core Principle**: "Store data in the cheapest tier that meets your access requirements. Move data as little as possible."

---

## 1. Understanding Egress Costs

### The Egress Pricing Model
Cloud providers typically charge for data leaving their network:

| Direction | AWS | GCP | Azure |
|-----------|-----|-----|-------|
| **Inbound (Internet → Cloud)** | Free | Free | Free |
| **Outbound (Cloud → Internet)** | $0.09/GB | $0.12/GB | $0.087/GB |
| **Inter-AZ (Same Region)** | $0.01/GB | $0.01/GB | $0.01/GB |
| **Inter-Region** | $0.02/GB | $0.01/GB | $0.02/GB |
| **To CDN (CloudFront/Cloud CDN)** | Free* | Free* | Free* |

*Free or significantly reduced when using the provider's CDN.

---

## 2. Storage Tier Optimization

### AWS S3 Storage Classes

| Class | Use Case | Cost (per GB/mo) | Retrieval Cost |
|-------|----------|------------------|----------------|
| **Standard** | Active data | $0.023 | Free |
| **Intelligent-Tiering** | Unknown access patterns | $0.023 + $0.0025 monitoring | Free |
| **Standard-IA** | Infrequent access (>30 days) | $0.0125 | $0.01/GB |
| **One Zone-IA** | Non-critical, infrequent | $0.01 | $0.01/GB |
| **Glacier Instant** | Archive, instant retrieval | $0.004 | $0.03/GB |
| **Glacier Flexible** | Archive, 1-5 min retrieval | $0.0036 | $0.02/GB + $0.03/1000 req |
| **Glacier Deep Archive** | Long-term (7-10 years) | $0.00099 | $0.02/GB + 12hr wait |

### Lifecycle Policy Example
```json
{
  "Rules": [
    {
      "ID": "OptimizeLogs",
      "Status": "Enabled",
      "Filter": { "Prefix": "logs/" },
      "Transitions": [
        { "Days": 30, "StorageClass": "STANDARD_IA" },
        { "Days": 90, "StorageClass": "GLACIER_IR" },
        { "Days": 365, "StorageClass": "DEEP_ARCHIVE" }
      ],
      "Expiration": { "Days": 2555 }
    }
  ]
}
```

---

## 3. Egress Reduction Strategies

### Strategy 1: Use a CDN
**Problem**: Serving 10TB of images directly from S3 costs $900/month in egress.
**Solution**: Use CloudFront. First 10TB costs $0.085/GB = $850, but subsequent requests are cached at the edge (no S3 egress).
**Savings**: 40-60% reduction in data transfer costs.

### Strategy 2: Regional Collocation
**Problem**: API in `us-east-1` calling database in `eu-west-1` generates inter-region egress.
**Solution**: Deploy API replicas in each region where you have significant users.
**Savings**: Eliminates cross-region transfer ($0.02/GB → $0.00).

### Strategy 3: Compression
**Problem**: Serving uncompressed JSON/CSV files.
**Solution**: Enable gzip compression on API responses and S3 objects.
**Savings**: 70-90% reduction in bytes transferred.

```javascript
// Express.js example
const compression = require('compression');
app.use(compression());
```

### Strategy 4: Smart Caching
**Problem**: Same data requested repeatedly from S3.
**Solution**: Implement Redis cache layer.
**Savings**: 95%+ reduction in S3 GET requests and egress.

---

## 4. Storage Optimization Techniques

### Deduplication
Identify and eliminate duplicate files before storing.
```python
import hashlib

def get_file_hash(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        hasher.update(f.read())
    return hasher.hexdigest()

# Store hash as metadata to detect duplicates
```

### Compression at Rest
Store data in compressed formats:
- **Parquet** instead of CSV (80-90% smaller)
- **WebP** instead of PNG for images (25-35% smaller)
- **Brotli** instead of gzip for text (15-20% better compression)

### Object Versioning Cleanup
S3 versioning can silently accumulate costs.
```bash
# List all versions of an object
aws s3api list-object-versions --bucket my-bucket --prefix logs/

# Delete old versions
aws s3api delete-object --bucket my-bucket --key logs/app.log --version-id <version-id>
```

---

## 5. Data Transfer Acceleration

### AWS S3 Transfer Acceleration
Uses CloudFront edge locations to speed up uploads to S3 (and reduce egress when downloading).
- **Cost**: +$0.04/GB for uploads, +$0.04/GB for downloads
- **Benefit**: 50-500% faster for distant regions

### Direct Connect / Dedicated Interconnect
For high-volume, predictable data transfer (>100TB/month), a dedicated line is cheaper than internet egress.
- **AWS Direct Connect**: $0.02/GB (vs $0.09/GB internet egress)
- **GCP Dedicated Interconnect**: $0.02/GB

---

## 6. Monitoring Storage and Egress

### Key Metrics to Track
```
Storage Metrics:
- Total storage by bucket/class
- Growth rate (GB/day)
- Access frequency (GET requests per object)

Egress Metrics:
- Egress by service (S3, EC2, RDS)
- Egress by destination (Internet, Inter-region, Inter-AZ)
- Top egress-heavy objects/endpoints
```

### CloudWatch Metrics (AWS)
```bash
# Monitor S3 egress
aws cloudwatch get-metric-statistics \
  --namespace AWS/S3 \
  --metric-name BytesDownloaded \
  --dimensions Name=BucketName,Value=my-bucket \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-31T23:59:59Z \
  --period 86400 \
  --statistics Sum
```

---

## 7. Real-World Cost Savings Examples

### Case Study 1: Video Streaming Platform
- **Problem**: 500TB/month egress from S3 = $45,000/month
- **Solution**: 
  - Implemented CloudFront CDN (cache hit rate: 85%)
  - Moved to Glacier for videos >6 months old
- **Result**: Egress cost dropped to $12,000/month (73% savings)

### Case Study 2: Data Analytics Company
- **Problem**: Storing 2PB of raw CSV logs in S3 Standard = $47,000/month
- **Solution**:
  - Converted to Parquet (90% compression)
  - Moved to Intelligent-Tiering
- **Result**: Storage cost dropped to $8,000/month (83% savings)

---

## 8. Storage and Egress Checklist

- [ ] **Lifecycle Policies**: Are all S3/GCS buckets using automated tiering?
- [ ] **CDN**: Are static assets served via CloudFront/Fastly instead of origin?
- [ ] **Compression**: Is gzip/brotli enabled on all API responses?
- [ ] **Caching**: Do we cache frequently accessed data in Redis/Memcached?
- [ ] **Regional Strategy**: Are we serving users from the nearest region?
- [ ] **Versioning**: Have we cleaned up old S3 object versions?
- [ ] **Format**: Are we using columnar formats (Parquet) for analytics data?
- [ ] **Monitoring**: Do we have alerts for unusual egress spikes?

---

## 9. Tools for Optimization

- **AWS S3 Storage Lens**: Analytics and recommendations for S3 optimization
- **CloudHealth / Cloudability**: Multi-cloud cost analysis with egress breakdowns
- **Kubecost**: Kubernetes-specific storage and network cost attribution
- **s3-pit-restore**: Point-in-time restore without keeping all versions

---

## Related Skills
- `42-cost-engineering/cloud-cost-models`
- `42-cost-engineering/cost-observability`
- `43-data-reliability/data-retention-archiving`
