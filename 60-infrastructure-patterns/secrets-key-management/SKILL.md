# Secrets & Key Management

## Overview

Secrets management encompasses secure storage, rotation, and access control for API keys, credentials, certificates, and encryption keys. Proper implementation prevents data breaches and ensures compliance.

## Why This Matters

- **Security**: Prevent credential leaks and unauthorized access
- **Compliance**: Meet SOC2, GDPR, HIPAA requirements
- **Rotation**: Automated key rotation reduces risk
- **Audit**: Track who accessed what secrets when

## Core Concepts

### 1. Secret Types
<!-- TODO: API keys, passwords, certificates, encryption keys -->

### 2. Secret Storage Solutions
<!-- TODO: Vault, AWS Secrets Manager, Azure Key Vault -->

### 3. Key Rotation Strategies
<!-- TODO: Automatic rotation, zero-downtime rotation -->

### 4. Access Control
<!-- TODO: RBAC, policies, least privilege -->

### 5. Secret Injection
<!-- TODO: Environment variables, sidecars, CSI drivers -->

### 6. Encryption at Rest
<!-- TODO: KMS, envelope encryption -->

### 7. Certificate Management
<!-- TODO: TLS certs, mTLS, cert-manager -->

### 8. Audit Logging
<!-- TODO: Access logs, compliance reporting -->

## Quick Start

```typescript
// TODO: Basic secrets retrieval
```

## Production Checklist

- [ ] No secrets in code or git
- [ ] Secret rotation automated
- [ ] Access policies defined (least privilege)
- [ ] Audit logging enabled
- [ ] Emergency rotation procedure documented
- [ ] Secrets encrypted at rest and in transit

## Tools & Libraries

| Tool | Type | Best For |
|------|------|----------|
| HashiCorp Vault | Self-hosted | Full-featured, multi-cloud |
| AWS Secrets Manager | Cloud | AWS-native workloads |
| Azure Key Vault | Cloud | Azure-native workloads |
| GCP Secret Manager | Cloud | GCP-native workloads |
| SOPS | Tool | Git-encrypted secrets |
| External Secrets | K8s | Kubernetes secret sync |

## Anti-patterns

1. **Hardcoded secrets**: Credentials in source code
2. **Shared credentials**: Single key for multiple services
3. **No rotation**: Same keys for years
4. **Over-permissive access**: Everyone can read all secrets

## Real-World Examples

### Example 1: Vault Integration
<!-- TODO: HashiCorp Vault setup and usage -->

### Example 2: AWS Secrets Manager with Rotation
<!-- TODO: Automatic rotation Lambda -->

### Example 3: Kubernetes External Secrets
<!-- TODO: K8s secret synchronization -->

## Common Mistakes

1. Committing .env files to git
2. Logging secrets in application logs
3. Not rotating after employee departure
4. Using same key for dev and production

## Integration Points

- CI/CD pipelines
- Kubernetes clusters
- Application runtime
- Infrastructure as Code

## Further Reading

- [HashiCorp Vault Documentation](https://www.vaultproject.io/docs)
- [AWS Secrets Manager Best Practices](https://docs.aws.amazon.com/secretsmanager/)
- [12-Factor App: Config](https://12factor.net/config)
