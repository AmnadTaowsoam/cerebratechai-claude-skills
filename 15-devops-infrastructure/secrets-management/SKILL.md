# Secrets Management

A comprehensive guide to secrets management patterns for secure application deployment.

## Table of Contents

1. [Secrets Management Principles](#secrets-management-principles)
2. [Tools](#tools)
3. [.env Files (Development)](#env-files-development)
4. [Secrets Rotation](#secrets-rotation)
5. [Access Control](#access-control)
6. [Encryption at Rest](#encryption-at-rest)
7. [Application Integration](#application-integration)
8. [CI/CD Integration](#cicd-integration)
9. [Audit Logging](#audit-logging)
10. [Best Practices](#best-practices)

---

## Secrets Management Principles

### Why Secrets Management Matters

```
Without Proper Secrets Management:
- Secrets in code → exposed in Git history
- Secrets in environment → accessible to all
- Secrets in config files → accidentally committed
- No rotation → compromised credentials stay active
- No audit → can't track who accessed what

With Proper Secrets Management:
- Secrets encrypted at rest
- Secrets encrypted in transit
- Fine-grained access control
- Automatic rotation
- Complete audit trail
```

### Core Principles

| Principle | Description |
|-----------|-------------|
| **Least Privilege** | Only grant necessary access |
| **Encryption** | Encrypt at rest and in transit |
| **Rotation** | Regularly rotate secrets |
| **Audit** | Log all secret access |
| **Isolation** | Separate secrets by environment |
| **Versioning** | Track secret versions |
| **Revocation** | Ability to revoke secrets |

---

## Tools

### HashiCorp Vault

```hcl
# Vault configuration
storage "file" {
  path = "./vault/data"
}

listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_cert_file = "/etc/vault/tls.crt"
  tls_key_file  = "/etc/vault/tls.key"
}

ui = true
```

```bash
# Start Vault
vault server -config=vault.hcl

# Initialize Vault
vault operator init

# Unseal Vault
vault operator unseal <key1>
vault operator unseal <key2>
vault operator unseal <key3>

# Login
vault login <root-token>

# Enable KV secrets engine
vault secrets enable -path=secret kv

# Write secret
vault kv put secret/myapp database_url="postgresql://user:pass@localhost:5432/db"

# Read secret
vault kv get secret/myapp

# Delete secret
vault kv delete secret/myapp
```

### AWS Secrets Manager

```bash
# Create secret
aws secretsmanager create-secret \
  --name myapp/database \
  --secret-string '{"username":"admin","password":"secret"}'

# Get secret
aws secretsmanager get-secret-value \
  --secret-id myapp/database

# Update secret
aws secretsmanager put-secret-value \
  --secret-id myapp/database \
  --secret-string '{"username":"admin","password":"newsecret"}'

# Delete secret
aws secretsmanager delete-secret \
  --secret-id myapp/database \
  --force-delete-without-recovery
```

```python
# Python integration
import boto3

client = boto3.client('secretsmanager')

# Get secret
response = client.get_secret_value(SecretId='myapp/database')
secret = json.loads(response['SecretString'])

# Use secret
database_url = f"postgresql://{secret['username']}:{secret['password']}@localhost:5432/db"
```

```typescript
// TypeScript integration
import { SecretsManagerClient, GetSecretValueCommand } from '@aws-sdk/client-secrets-manager';

const client = new SecretsManagerClient({ region: 'us-east-1' });

async function getSecret(secretId: string) {
  const command = new GetSecretValueCommand({ SecretId: secretId });
  const response = await client.send(command);
  return JSON.parse(response.SecretString!);
}

// Use secret
const secret = await getSecret('myapp/database');
const databaseUrl = `postgresql://${secret.username}:${secret.password}@localhost:5432/db`;
```

### Kubernetes Secrets

```yaml
# Create secret from literal
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secret
type: Opaque
data:
  database_url: cG9zdGdyZXNxbDovL3VzZXI6cGFzc0Bsb2NhbGhvc3Q6NTQzMi9kYg==
  api_key: YXBpLWtleS12YWx1ZQ==
```

```bash
# Create secret from file
kubectl create secret generic myapp-secret \
  --from-file=database_url=./database_url.txt \
  --from-file=api_key=./api_key.txt

# Create secret from env file
kubectl create secret generic myapp-secret \
  --from-env-file=.env

# Get secret
kubectl get secret myapp-secret -o jsonpath='{.data}'

# Decode secret
kubectl get secret myapp-secret -o jsonpath='{.data.database_url}' | base64 -d

# Delete secret
kubectl delete secret myapp-secret
```

```yaml
# Use secret in pod
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
spec:
  containers:
  - name: myapp
    image: myapp:latest
    env:
    - name: DATABASE_URL
      valueFrom:
        secretKeyRef:
          name: myapp-secret
          key: database_url
    - name: API_KEY
      valueFrom:
        secretKeyRef:
          name: myapp-secret
          key: api_key
```

### Docker Secrets

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    image: myapp:latest
    secrets:
      - database_url
      - api_key

secrets:
  database_url:
    file: ./secrets/database_url.txt
  api_key:
    file: ./secrets/api_key.txt
```

```bash
# Create secret
echo "postgresql://user:pass@localhost:5432/db" | docker secret create database_url -

# Use secret in Dockerfile
# Not directly accessible, use Docker Compose
```

---

## .env Files (Development)

### Basic .env File

```bash
# .env
NODE_ENV=development
PORT=3000
DATABASE_URL=postgresql://user:pass@localhost:5432/db
API_KEY=dev-api-key
SECRET_KEY=dev-secret-key
```

### Multiple Environment Files

```bash
# .env.development
NODE_ENV=development
DATABASE_URL=postgresql://dev:devpass@localhost:5432/devdb
API_KEY=dev-api-key

# .env.staging
NODE_ENV=staging
DATABASE_URL=postgresql://staging:stagepass@staging-db:5432/stagedb
API_KEY=staging-api-key

# .env.production
NODE_ENV=production
# DATABASE_URL and API_KEY loaded from secrets manager
```

### .env Usage (Node.js)

```typescript
// Install dotenv
// npm install dotenv

import dotenv from 'dotenv';

// Load .env file
dotenv.config();

// Access environment variables
const databaseUrl = process.env.DATABASE_URL;
const apiKey = process.env.API_KEY;
```

### .env Usage (Python)

```python
# Install python-dotenv
# pip install python-dotenv

from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Access environment variables
database_url = os.getenv('DATABASE_URL')
api_key = os.getenv('API_KEY')
```

---

## Secrets Rotation

### Manual Rotation

```bash
# AWS Secrets Manager rotation
aws secretsmanager rotate-secret \
  --secret-id myapp/database \
  --rotation-lambda-arn arn:aws:lambda:us-east-1:123456789012:function:rotate-db-secret
```

### Automatic Rotation (Lambda)

```python
# Lambda function for rotating database credentials
import boto3
import json
import psycopg2

def lambda_handler(event, context):
    secret_id = event['SecretId']
    step = event['Step']

    client = boto3.client('secretsmanager')

    if step == 'createSecret':
        # Create new secret
        new_password = generate_password()
        client.put_secret_value(
            SecretId=secret_id,
            SecretString=json.dumps({
                'username': 'admin',
                'password': new_password
            })
        )
    elif step == 'setSecret':
        # Update database password
        secret = client.get_secret_value(SecretId=secret_id)
        creds = json.loads(secret['SecretString'])
        update_database_password(creds['username'], creds['password'])

    return {'Status': 'Success'}
```

### Kubernetes Secret Rotation

```yaml
# Create new secret version
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secret-v2
type: Opaque
data:
  database_url: cG9zdGdyZXNxbDovL3VzZXI6bmV3cGFzc0Bsb2NhbGhvc3Q6NTQzMi9kYg==
```

```bash
# Update deployment to use new secret
kubectl set env deployment/myapp \
  --from=secret/myapp-secret-v2 \
  --prefix=DATABASE_URL
```

---

## Access Control

### Vault Policies

```hcl
# policy.hcl
path "secret/myapp/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

path "secret/myapp/production/*" {
  capabilities = ["read"]
}
```

```bash
# Create policy
vault policy write myapp-policy -policy=policy.hcl

# Create token with policy
vault token create -policy=myapp-policy
```

### AWS IAM Policies

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue",
        "secretsmanager:DescribeSecret"
      ],
      "Resource": "arn:aws:secretsmanager:us-east-1:123456789012:secret:myapp/*"
    }
  ]
}
```

### Kubernetes RBAC

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: myapp-sa
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: secret-reader
rules:
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-secrets
subjects:
- kind: ServiceAccount
  name: myapp-sa
roleRef:
  kind: Role
  name: secret-reader
```

---

## Encryption at Rest

### Vault Encryption

```hcl
# Enable transit secrets engine
vault secrets enable transit

# Create encryption key
vault write -f transit/keys/myapp-key

# Encrypt data
vault write transit/encrypt/myapp-key \
  plaintext=$(base64 <<< "my secret data")

# Decrypt data
vault write transit/decrypt/myapp-key \
  ciphertext=<ciphertext>
```

### AWS KMS

```bash
# Create KMS key
aws kms create-key \
  --description "MyApp encryption key" \
  --key-usage ENCRYPT_DECRYPT

# Encrypt data
aws kms encrypt \
  --key-id <key-id> \
  --plaintext fileb://secret.txt \
  --output text \
  --query CiphertextBlob \
  --output text > encrypted.txt

# Decrypt data
aws kms decrypt \
  --ciphertext-blob fileb://encrypted.txt \
  --output text \
  --query Plaintext \
  --output text | base64 --decode
```

---

## Application Integration

### Node.js with Vault

```typescript
import { Vault } from 'node-vault';

const vault = new Vault({
  endpoint: 'http://vault:8200',
  token: process.env.VAULT_TOKEN,
});

async function getSecret(path: string) {
  const result = await vault.read(path);
  return result.data.data;
}

// Usage
const secret = await getSecret('secret/data/myapp');
const databaseUrl = secret.database_url;
```

### Python with Vault

```python
import hvac

client = hvac.Client(
    url='http://vault:8200',
    token=os.getenv('VAULT_TOKEN')
)

def get_secret(path):
    response = client.secrets.kv.v2.read_secret_version(path=path)
    return response['data']['data']

# Usage
secret = get_secret('secret/data/myapp')
database_url = secret['database_url']
```

### Node.js with AWS Secrets Manager

```typescript
import { SecretsManagerClient, GetSecretValueCommand } from '@aws-sdk/client-secrets-manager';

const client = new SecretsManagerClient({ region: 'us-east-1' });

async function getSecret(secretId: string) {
  const command = new GetSecretValueCommand({ SecretId: secretId });
  const response = await client.send(command);
  return JSON.parse(response.SecretString!);
}

// Usage
const secret = await getSecret('myapp/database');
const databaseUrl = `postgresql://${secret.username}:${secret.password}@localhost:5432/db`;
```

### Python with AWS Secrets Manager

```python
import boto3
import json

client = boto3.client('secretsmanager')

def get_secret(secret_id):
    response = client.get_secret_value(SecretId=secret_id)
    return json.loads(response['SecretString'])

# Usage
secret = get_secret('myapp/database')
database_url = f"postgresql://{secret['username']}:{secret['password']}@localhost:5432/db"
```

---

## CI/CD Integration

### GitHub Actions with Secrets

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Get secret from AWS Secrets Manager
        id: secret
        run: |
          SECRET=$(aws secretsmanager get-secret-value \
            --secret-id myapp/database \
            --query SecretString \
            --output text)
          echo "secret=$SECRET" >> $GITHUB_OUTPUT

      - name: Deploy
        env:
          DATABASE_URL: ${{ steps.secret.outputs.secret }}
        run: |
          # Deployment commands
```

### GitLab CI with Secrets

```yaml
deploy:
  stage: deploy
  script:
    - apk add --no-cache aws-cli
    - aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
    - aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
    - aws configure set region us-east-1
    - SECRET=$(aws secretsmanager get-secret-value --secret-id myapp/database --query SecretString --output text)
    - export DATABASE_URL=$SECRET
    - npm run deploy
  only:
    - main
```

### Jenkins with Secrets

```groovy
pipeline {
  agent any

  environment {
    DATABASE_URL = credentials('myapp-database-url')
    API_KEY = credentials('myapp-api-key')
  }

  stages {
    stage('Deploy') {
      steps {
        sh 'npm run deploy'
      }
    }
  }
}
```

---

## Audit Logging

### Vault Audit Logging

```hcl
# Enable audit logging
vault audit enable file file_path=/vault/logs/audit.log

# View audit logs
cat /vault/logs/audit.log
```

### AWS CloudTrail

```bash
# Create trail
aws cloudtrail create-trail \
  --name myapp-trail \
  --s3-bucket-name myapp-logs-bucket

# Enable logging
aws cloudtrail start-logging \
  --name myapp-trail

# View logs
aws logs tail /aws/cloudtrail/myapp-trail
```

### Kubernetes Audit Logging

```yaml
# Enable audit logging in API server
apiVersion: audit.k8s.io/v1
kind: Policy
rules:
- level: RequestResponse
  resources:
  - group: ""
    resources: ["secrets"]
```

---

## Best Practices

### 1. Never Commit Secrets

```gitignore
# .gitignore
.env
.env.local
.env.*.local
*.key
*.pem
secrets/
```

### 2. Use Environment-Specific Secrets

```bash
# .env.development
DATABASE_URL=postgresql://dev:devpass@localhost:5432/devdb

# .env.production
# Load from secrets manager
```

### 3. Rotate Secrets Regularly

```bash
# Set up automatic rotation
aws secretsmanager rotate-secret \
  --secret-id myapp/database \
  --rotation-lambda-arn arn:aws:lambda:us-east-1:123456789012:function:rotate-db-secret
```

### 4. Use Least Privilege

```json
{
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue"
      ],
      "Resource": "arn:aws:secretsmanager:us-east-1:123456789012:secret:myapp/*"
    }
  ]
}
```

### 5. Encrypt Secrets at Rest

```bash
# Use encryption
aws kms encrypt \
  --key-id <key-id> \
  --plaintext fileb://secret.txt
```

### 6. Use Secret Scanning

```bash
# Install gitleaks
brew install gitleaks

# Scan repository
gitleaks detect --source .
```

### 7. Use Secret Injection

```yaml
# Inject secrets at runtime
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: myapp
    envFrom:
    - secretRef:
        name: myapp-secret
```

### 8. Use Temporary Credentials

```python
# Use temporary credentials
sts_client = boto3.client('sts')
response = sts_client.assume_role(
    RoleArn='arn:aws:iam::123456789012:role/MyAppRole',
    RoleSessionName='MyAppSession'
)

credentials = response['Credentials']
```

### 9. Monitor Secret Access

```bash
# Enable CloudTrail
aws cloudtrail create-trail \
  --name myapp-trail \
  --s3-bucket-name myapp-logs-bucket
```

### 10. Have a Revocation Plan

```bash
# Quick revocation
aws secretsmanager delete-secret \
  --secret-id myapp/database \
  --force-delete-without-recovery
```

---

## Resources

- [HashiCorp Vault Documentation](https://www.vaultproject.io/docs)
- [AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/)
- [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
- [Docker Secrets](https://docs.docker.com/engine/swarm/secrets/)
- [Gitleaks](https://github.com/zricethezav/gitleaks)
