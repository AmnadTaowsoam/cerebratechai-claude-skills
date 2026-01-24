---
name: GitOps for IoT Infrastructure
description: GitOps methodology for managing IoT infrastructure with continuous delivery and automated synchronization
---

# GitOps for IoT Infrastructure

## Current Level: Expert (Enterprise Scale)

## Domain: IoT Infrastructure
## Skill ID: 88

---

## Executive Summary

GitOps for IoT Infrastructure enables declarative infrastructure management where the desired state is defined in Git and automatically synchronized to the actual infrastructure. This approach provides version control, auditability, and automated deployment for distributed IoT systems spanning edge devices, edge servers, and cloud resources.

### Strategic Necessity

- **Declarative Management**: Define infrastructure as code
- **Version Control**: Track all infrastructure changes
- **Automated Deployment**: Continuous delivery of infrastructure changes
- **Audit Trail**: Complete history of all changes
- **Consistency**: Ensure infrastructure matches Git state

---

## Technical Deep Dive

### GitOps Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        GitOps Architecture for IoT                         │
│                                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│  │   Git Repo   │    │   CI/CD     │    │   GitOps    │                  │
│  │   (Source)   │───▶│   Pipeline   │───▶│   Operator  │                  │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘                  │
│         │                   │                   │                           │
│         ▼                   ▼                   ▼                           │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Infrastructure Layers                             │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Cloud   │  │  Edge    │  │  IoT     │  │ Network  │            │   │
│  │  │  AWS/Azure│  │  K3s/K8s │  │Devices   │  │  SD-WAN  │            │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘            │   │
│  └───────┼────────────┼────────────┼────────────┼────────────────────┘   │
│          │            │            │            │                         │
│          ▼            ▼            ▼            ▼                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Sync & Reconciliation                            │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Diff    │  │  Apply   │  │  Verify  │  │  Report  │            │   │
│  │  │  Detect  │  │  Changes │  │  State   │  │  Status  │            │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Monitoring & Feedback                             │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Health  │  │  Metrics │  │  Alerts  │  │  Logs    │            │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### GitOps Components

**1. Git Repository Structure:**

```
iot-infrastructure/
├── README.md
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
├── environments/
│   ├── development/
│   │   ├── terraform/
│   │   │   ├── main.tf
│   │   │   ├── variables.tf
│   │   │   └── terraform.tfvars
│   │   ├── k8s/
│   │   │   ├── namespace.yaml
│   │   │   ├── deployments/
│   │   │   ├── services/
│   │   │   └── configmaps/
│   │   └── ansible/
│   │       ├── inventory/
│   │       └── playbooks/
│   ├── staging/
│   │   └── (same structure)
│   └── production/
│       └── (same structure)
├── modules/
│   ├── iot-gateway/
│   ├── edge-server/
│   └── cloud-resources/
├── charts/
│   ├── iot-gateway/
│   ├── edge-services/
│   └── cloud-platform/
└── docs/
    ├── architecture.md
    ├── operations.md
    └── troubleshooting.md
```

**2. ArgoCD Application Definition:**

```yaml
# environments/production/k8s/argocd/iot-gateway-application.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: iot-gateway
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
  labels:
    app: iot-gateway
    environment: production
spec:
  project: iot-infrastructure
  
  source:
    repoURL: https://github.com/example/iot-infrastructure.git
    targetRevision: main
    path: environments/production/k8s/iot-gateway
  
  destination:
    server: https://kubernetes.default.svc
    namespace: iot-gateway
  
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
      allowEmpty: false
    syncOptions:
      - CreateNamespace=true
      - PrunePropagationPolicy=foreground
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
  
  ignoreDifferences:
    - group: apps
      kind: Deployment
      jsonPointers:
        - /spec/replicas
  
  healthCheck:
    minHealthy: 80
```

**3. ApplicationSet for Multi-Environment:**

```yaml
# environments/production/k8s/argocd/applicationset.yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: iot-infrastructure
  namespace: argocd
spec:
  generators:
    # Generator for environments
    - git:
        repoURL: https://github.com/example/iot-infrastructure.git
        revision: main
        directories:
          - path: environments/*
    
    # Generator for edge locations
    - list:
        elements:
          - location: site-a
            cluster: https://k8s-site-a.example.com
          - location: site-b
            cluster: https://k8s-site-b.example.com
          - location: site-c
            cluster: https://k8s-site-c.example.com
  
  template:
    metadata:
      name: '{{path.basename}}-{{location}}'
      labels:
        app: iot-infrastructure
        environment: '{{path.basename}}'
        location: '{{location}}'
    spec:
      project: iot-infrastructure
      source:
        repoURL: https://github.com/example/iot-infrastructure.git
        targetRevision: main
        path: '{{path}}/k8s/{{location}}'
      destination:
        server: '{{cluster}}'
        namespace: iot-infrastructure
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
        syncOptions:
          - CreateNamespace=true
```

### GitOps Operator Implementation

```python
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import asyncio
import logging
import hashlib
import json

logger = logging.getLogger(__name__)

class SyncStatus(Enum):
    """Synchronization status"""
    SYNCED = "synced"
    OUT_OF_SYNC = "out_of_sync"
    UNKNOWN = "unknown"
    ERROR = "error"

@dataclass
class ResourceState:
    """Resource state"""
    kind: str
    name: str
    namespace: str
    git_hash: str
    cluster_hash: str
    status: SyncStatus

class GitOpsOperator:
    """GitOps operator for IoT infrastructure"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.git_client = GitClient(config['git'])
        self.k8s_client = KubernetesClient(config['k8s'])
        self.monitoring = MonitoringSystem(config['monitoring'])
        self.state_cache = {}
        self.running = False
        
    async def start(self):
        """Start GitOps operator"""
        logger.info("Starting GitOps operator...")
        self.running = True
        
        # Start reconciliation loop
        asyncio.create_task(self._reconciliation_loop())
        
        # Start monitoring
        await self.monitoring.start()
        
        logger.info("GitOps operator started")
    
    async def stop(self):
        """Stop GitOps operator"""
        logger.info("Stopping GitOps operator...")
        self.running = False
        await self.monitoring.stop()
        logger.info("GitOps operator stopped")
    
    async def _reconciliation_loop(self):
        """Main reconciliation loop"""
        while self.running:
            try:
                await self._reconcile()
                await asyncio.sleep(self.config['sync_interval'])
            except Exception as e:
                logger.error(f"Reconciliation failed: {e}")
                await asyncio.sleep(10)  # Wait before retry
    
    async def _reconcile(self):
        """Reconcile Git state with cluster state"""
        logger.info("Starting reconciliation...")
        
        # Step 1: Get Git state
        git_state = await self._get_git_state()
        
        # Step 2: Get cluster state
        cluster_state = await self._get_cluster_state()
        
        # Step 3: Compare states
        diff = self._compare_states(git_state, cluster_state)
        
        # Step 4: Apply changes
        if diff['needs_sync']:
            logger.info(f"Applying {len(diff['changes'])} changes...")
            await self._apply_changes(diff['changes'])
        
        # Step 5: Verify state
        await self._verify_state()
        
        # Step 6: Report status
        await self._report_status(diff)
        
        logger.info("Reconciliation completed")
    
    async def _get_git_state(self) -> Dict[str, Any]:
        """Get desired state from Git"""
        logger.info("Getting Git state...")
        
        # Get latest commit
        latest_commit = await self.git_client.get_latest_commit()
        
        # Get all manifests
        manifests = await self.git_client.get_manifests(
            self.config['git']['path']
        )
        
        # Parse manifests
        resources = []
        for manifest in manifests:
            try:
                resource = self._parse_manifest(manifest)
                resource['git_hash'] = self._compute_hash(manifest)
                resources.append(resource)
            except Exception as e:
                logger.error(f"Failed to parse manifest: {e}")
        
        return {
            'commit': latest_commit,
            'resources': resources
        }
    
    async def _get_cluster_state(self) -> Dict[str, Any]:
        """Get current state from cluster"""
        logger.info("Getting cluster state...")
        
        resources = []
        
        # Get all resources in namespace
        namespaces = self.config['k8s']['namespaces']
        
        for namespace in namespaces:
            # Get deployments
            deployments = await self.k8s_client.get_deployments(namespace)
            for deployment in deployments:
                resource = {
                    'kind': 'Deployment',
                    'name': deployment.metadata.name,
                    'namespace': namespace,
                    'spec': deployment.spec,
                    'status': deployment.status
                }
                resource['cluster_hash'] = self._compute_hash(resource['spec'])
                resources.append(resource)
            
            # Get services
            services = await self.k8s_client.get_services(namespace)
            for service in services:
                resource = {
                    'kind': 'Service',
                    'name': service.metadata.name,
                    'namespace': namespace,
                    'spec': service.spec,
                    'status': service.status
                }
                resource['cluster_hash'] = self._compute_hash(resource['spec'])
                resources.append(service)
        
        return {
            'resources': resources
        }
    
    def _compare_states(
        self, 
        git_state: Dict[str, Any],
        cluster_state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compare Git state with cluster state"""
        logger.info("Comparing states...")
        
        changes = []
        needs_sync = False
        
        # Create lookup for cluster resources
        cluster_resources = {}
        for resource in cluster_state['resources']:
            key = f"{resource['kind']}/{resource['namespace']}/{resource['name']}"
            cluster_resources[key] = resource
        
        # Compare Git resources
        for git_resource in git_state['resources']:
            key = f"{git_resource['kind']}/{git_resource['namespace']}/{git_resource['name']}"
            
            if key not in cluster_resources:
                # Resource exists in Git but not in cluster - needs to be created
                changes.append({
                    'action': 'create',
                    'resource': git_resource
                })
                needs_sync = True
            else:
                cluster_resource = cluster_resources[key]
                
                # Compare hashes
                if git_resource['git_hash'] != cluster_resource['cluster_hash']:
                    # Resource exists but is different - needs to be updated
                    changes.append({
                        'action': 'update',
                        'resource': git_resource
                    })
                    needs_sync = True
        
        # Check for resources in cluster but not in Git
        for key, cluster_resource in cluster_resources.items():
            git_key = f"{cluster_resource['kind']}/{cluster_resource['namespace']}/{cluster_resource['name']}"
            git_exists = any(
                r['kind'] == cluster_resource['kind'] and
                r['namespace'] == cluster_resource['namespace'] and
                r['name'] == cluster_resource['name']
                for r in git_state['resources']
            )
            
            if not git_exists:
                # Resource exists in cluster but not in Git - needs to be deleted
                changes.append({
                    'action': 'delete',
                    'resource': cluster_resource
                })
                needs_sync = True
        
        return {
            'needs_sync': needs_sync,
            'changes': changes
        }
    
    async def _apply_changes(self, changes: List[Dict[str, Any]]):
        """Apply changes to cluster"""
        logger.info(f"Applying {len(changes)} changes...")
        
        for change in changes:
            action = change['action']
            resource = change['resource']
            
            try:
                if action == 'create':
                    await self.k8s_client.create_resource(resource)
                elif action == 'update':
                    await self.k8s_client.update_resource(resource)
                elif action == 'delete':
                    await self.k8s_client.delete_resource(resource)
                
                logger.info(f"Successfully {action}d {resource['kind']}/{resource['name']}")
                
            except Exception as e:
                logger.error(f"Failed to {action} {resource['kind']}/{resource['name']}: {e}")
                await self.monitoring.alert(
                    f"Failed to {action} resource",
                    {'resource': resource, 'error': str(e)}
                )
    
    async def _verify_state(self):
        """Verify that cluster state matches Git state"""
        logger.info("Verifying state...")
        
        # Get current states
        git_state = await self._get_git_state()
        cluster_state = await self._get_cluster_state()
        
        # Compare
        diff = self._compare_states(git_state, cluster_state)
        
        # Report verification status
        if diff['needs_sync']:
            logger.warning(f"Verification failed: {len(diff['changes'])} differences found")
            await self.monitoring.alert(
                "State verification failed",
                {'differences': diff['changes']}
            )
        else:
            logger.info("Verification successful: state is synchronized")
    
    async def _report_status(self, diff: Dict[str, Any]):
        """Report synchronization status"""
        status = {
            'timestamp': asyncio.get_event_loop().time(),
            'synced': not diff['needs_sync'],
            'changes': len(diff['changes']),
            'details': diff['changes']
        }
        
        # Update monitoring
        await self.monitoring.update_status(status)
        
        # Update cache
        self.state_cache['status'] = status
    
    def _parse_manifest(self, manifest: str) -> Dict[str, Any]:
        """Parse Kubernetes manifest"""
        import yaml
        
        # Parse YAML
        data = yaml.safe_load(manifest)
        
        # Extract resource info
        return {
            'kind': data['kind'],
            'name': data['metadata']['name'],
            'namespace': data['metadata'].get('namespace', 'default'),
            'spec': data.get('spec', {}),
            'manifest': data
        }
    
    def _compute_hash(self, data: Any) -> str:
        """Compute hash of data"""
        # Convert to JSON string
        json_str = json.dumps(data, sort_keys=True)
        
        # Compute SHA256 hash
        return hashlib.sha256(json_str.encode()).hexdigest()

class GitClient:
    """Git client for accessing repository"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.repo_url = config['repo_url']
        self.branch = config.get('branch', 'main')
        
    async def get_latest_commit(self) -> str:
        """Get latest commit hash"""
        # Implementation would use Git API or CLI
        return "abc123"
    
    async def get_manifests(self, path: str) -> List[str]:
        """Get all manifests from path"""
        # Implementation would list and read files from Git
        return []

class KubernetesClient:
    """Kubernetes client for cluster operations"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def get_deployments(self, namespace: str) -> List[Any]:
        """Get deployments in namespace"""
        # Implementation would use Kubernetes Python client
        return []
    
    async def get_services(self, namespace: str) -> List[Any]:
        """Get services in namespace"""
        # Implementation would use Kubernetes Python client
        return []
    
    async def create_resource(self, resource: Dict[str, Any]):
        """Create resource in cluster"""
        # Implementation would use Kubernetes Python client
        pass
    
    async def update_resource(self, resource: Dict[str, Any]):
        """Update resource in cluster"""
        # Implementation would use Kubernetes Python client
        pass
    
    async def delete_resource(self, resource: Dict[str, Any]):
        """Delete resource from cluster"""
        # Implementation would use Kubernetes Python client
        pass

class MonitoringSystem:
    """Monitoring system for GitOps operator"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def start(self):
        """Start monitoring"""
        pass
    
    async def stop(self):
        """Stop monitoring"""
        pass
    
    async def update_status(self, status: Dict[str, Any]):
        """Update synchronization status"""
        pass
    
    async def alert(self, message: str, details: Dict[str, Any]):
        """Send alert"""
        pass
```

### CI/CD Pipeline Integration

```yaml
# .github/workflows/cd.yml
name: Continuous Deployment

on:
  push:
    branches:
      - main
    paths:
      - 'environments/production/**'
      - 'charts/**'
      - 'modules/**'

env:
  AWS_REGION: us-west-2
  EKS_CLUSTER: iot-production

jobs:
  validate:
    name: Validate Changes
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Setup kubectl
        uses: azure/setup-kubectl@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_REGION }}
      
      - name: Update kubeconfig
        run: |
          aws eks update-kubeconfig --name ${{ env.EKS_CLUSTER }} --region ${{ env.AWS_REGION }}
      
      - name: Validate Kubernetes manifests
        run: |
          kubectl apply --dry-run=client -f environments/production/k8s/
      
      - name: Validate Helm charts
        run: |
          helm lint charts/iot-gateway/
          helm lint charts/edge-services/

  plan:
    name: Plan Terraform Changes
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_REGION }}
      
      - name: Terraform Init
        run: |
          cd environments/production/terraform
          terraform init
      
      - name: Terraform Plan
        run: |
          cd environments/production/terraform
          terraform plan -out=tfplan
      
      - name: Save Plan
        uses: actions/upload-artifact@v3
        with:
          name: terraform-plan
          path: environments/production/terraform/tfplan

  deploy:
    name: Deploy to Production
    needs: [validate, plan]
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Setup kubectl
        uses: azure/setup-kubectl@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_REGION }}
      
      - name: Update kubeconfig
        run: |
          aws eks update-kubeconfig --name ${{ env.EKS_CLUSTER }} --region ${{ env.AWS_REGION }}
      
      - name: Apply Kubernetes manifests
        run: |
          kubectl apply -f environments/production/k8s/
      
      - name: Wait for rollout
        run: |
          kubectl rollout status deployment/iot-gateway -n iot-gateway
      
      - name: Verify deployment
        run: |
          kubectl get pods -n iot-gateway
          kubectl get services -n iot-gateway
      
      - name: Run smoke tests
        run: |
          python tests/smoke_test.py

  notify:
    name: Notify Team
    needs: [deploy]
    runs-on: ubuntu-latest
    if: always()
    steps:
      - name: Send Slack notification
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: |
            Deployment to production completed with status: ${{ job.status }}
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

---

## Tooling & Tech Stack

### GitOps Tools
- **ArgoCD**: Kubernetes-native GitOps
- **Flux**: GitOps toolkit for Kubernetes
- **Weaveworks GitOps**: Enterprise GitOps platform
- **Rancher Fleet**: Multi-cluster GitOps

### Version Control
- **Git**: Source control
- **GitHub**: Git hosting
- **GitLab**: Git hosting with CI/CD
- **Bitbucket**: Git hosting

### CI/CD Tools
- **GitHub Actions**: CI/CD pipeline
- **GitLab CI**: GitLab CI/CD
- **Jenkins**: Build automation
- **CircleCI**: Continuous integration

### Monitoring Tools
- **Prometheus**: Metrics collection
- **Grafana**: Visualization
- **ArgoCD Notifications**: Alerting
- **Slack**: Team communication

---

## Configuration Essentials

### ArgoCD Configuration

```yaml
# argocd/argocd-cm.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-cm
  namespace: argocd
data:
  # Repository credentials
  repositories: |
    - url: https://github.com/example/iot-infrastructure.git
      name: iot-infrastructure
      sshPrivateKeySecret:
        name: iot-infrastructure-ssh-key
  
  # Cluster credentials
  clusters: |
    - name: production
      server: https://k8s-production.example.com
      config:
        bearerToken: ${{ bearerToken }}
        tlsClientConfig:
          insecure: false
  
  # OIDC configuration
  oidc.config: |
    name: Okta
    issuer: https://dev-12345.okta.com/oauth2/default
    clientId: ${{ clientId }}
    clientSecret: ${{ clientSecret }}
    requestedScopes: ["openid", "profile", "email", "groups"]
    requestedIDTokenClaims: {"groups": {"essential": true}}
  
  # Application controller settings
  application.instanceLabelKey: argocd.argoproj.io/instance
  
  # Server settings
  server.insecure: "false"
  server.baseurl: https://argocd.example.com
  
  # Resource tracking
  resourceTrackingMethod: "label"
  
  # Sync settings
  timeout.reconciliation: 180s
  timeout.hard.reconciliation: 600s
```

### Flux Configuration

```yaml
# flux/kustomization.yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: iot-infrastructure
  namespace: flux-system
spec:
  interval: 5m
  sourceRef:
    kind: GitRepository
    name: iot-infrastructure
  path: ./environments/production/k8s
  prune: true
  validation: client
  healthChecks:
    - apiVersion: apps/v1
      kind: Deployment
      name: iot-gateway
      namespace: iot-gateway
---
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: iot-infrastructure
  namespace: flux-system
spec:
  interval: 5m
  url: https://github.com/example/iot-infrastructure.git
  ref:
    branch: main
  secretRef:
    name: iot-infrastructure-ssh-key
```

---

## Code Examples

### Good: Complete GitOps Setup

```bash
#!/bin/bash
# scripts/setup-gitops.sh

set -e

# Configuration
CLUSTER_NAME="${CLUSTER_NAME:-iot-production}"
ARGOCD_VERSION="${ARGOCD_VERSION:-v2.8.0}"
NAMESPACE="argocd"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# Step 1: Install ArgoCD
log_info "Step 1: Installing ArgoCD..."
kubectl create namespace argocd --dry-run=client -o yaml | kubectl apply -f -
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/${ARGOCD_VERSION}/manifests/install.yaml

# Wait for ArgoCD to be ready
log_info "Waiting for ArgoCD to be ready..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=argocd-server -n argocd --timeout=300s

# Step 2: Configure ArgoCD
log_info "Step 2: Configuring ArgoCD..."
kubectl apply -f argocd/argocd-cm.yaml
kubectl apply -f argocd/argocd-secret.yaml

# Step 3: Create GitOps project
log_info "Step 3: Creating GitOps project..."
kubectl apply -f argocd/project.yaml

# Step 4: Register cluster
log_info "Step 4: Registering cluster..."
argocd cluster add ${CLUSTER_NAME} --kube-context ${CLUSTER_NAME}

# Step 5: Create application
log_info "Step 5: Creating application..."
kubectl apply -f environments/production/k8s/argocd/iot-gateway-application.yaml

# Step 6: Sync application
log_info "Step 6: Syncing application..."
argocd app sync iot-gateway

# Step 7: Verify deployment
log_info "Step 7: Verifying deployment..."
argocd app get iot-gateway

log_info "GitOps setup completed successfully!"
```

### Bad: Anti-pattern Example

```bash
# BAD: Manual deployment
kubectl apply -f deployment.yaml

# BAD: No version control
# Directly editing resources
kubectl edit deployment iot-gateway

# BAD: No validation
kubectl apply -f deployment.yaml --dry-run=false

# BAD: No rollback
kubectl apply -f new-deployment.yaml

# BAD: No monitoring
kubectl apply -f deployment.yaml
# No health checks
```

---

## Standards, Compliance & Security

### Industry Standards
- **GitOps Principles**: GitOps methodology
- **Kubernetes Best Practices**: K8s best practices
- **Security Standards**: CIS benchmarks
- **Compliance**: SOC 2, ISO 27001

### Security Best Practices
- **Secrets Management**: Use sealed secrets or external secrets
- **Access Control**: RBAC for GitOps
- **Audit Logging**: Track all changes
- **Branch Protection**: Require PRs for changes

### Compliance Requirements
- **Change Management**: Document all changes
- **Approval Process**: Require approval for production
- **Audit Trail**: Complete change history
- **Disaster Recovery**: Rollback procedures

---

## Quick Start

### 1. Install ArgoCD

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### 2. Access ArgoCD UI

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
# Open http://localhost:8080
```

### 3. Create Application

```bash
kubectl apply -f argocd/iot-gateway-application.yaml
```

### 4. Sync Application

```bash
argocd app sync iot-gateway
```

---

## Production Checklist

### GitOps Setup
- [ ] Git repository configured
- [ ] Branch protection enabled
- [ ] CI/CD pipeline configured
- [ ] ArgoCD/Flux installed
- [ ] Applications defined

### Security
- [ ] Secrets managed properly
- [ ] RBAC configured
- [ ] Audit logging enabled
- [ ] Access control implemented
- [ ] Security scan enabled

### Monitoring
- [ ] Health checks configured
- [ ] Metrics collection enabled
- [ ] Alerting configured
- [ ] Dashboard configured
- [ ] Logging enabled

### Operations
- [ ] Rollback procedures documented
- [ ] Incident response plan
- [ ] Team trained
- [ ] Documentation complete
- [ ] Support plan in place

---

## Anti-patterns

### ❌ Avoid These Practices

1. **Manual Deployment**
   ```bash
   # BAD: Manual deployment
   kubectl apply -f deployment.yaml
   ```

2. **No Version Control**
   ```bash
   # BAD: No version control
   kubectl edit deployment iot-gateway
   ```

3. **No Validation**
   ```bash
   # BAD: No validation
   kubectl apply -f deployment.yaml --dry-run=false
   ```

4. **No Rollback**
   ```bash
   # BAD: No rollback
   kubectl apply -f new-deployment.yaml
   ```

5. **No Monitoring**
   ```bash
   # BAD: No monitoring
   kubectl apply -f deployment.yaml
   # No health checks
   ```

### ✅ Follow These Practices

1. **GitOps Workflow**
   ```bash
   # GOOD: GitOps workflow
   git add .
   git commit -m "Update deployment"
   git push
   # ArgoCD syncs automatically
   ```

2. **Version Control**
   ```bash
   # GOOD: Version control
   git checkout -b feature/new-feature
   # Make changes
   git commit -am "Add new feature"
   git push origin feature/new-feature
   # Create PR
   ```

3. **Validation**
   ```bash
   # GOOD: Validate before apply
   kubectl apply --dry-run=client -f deployment.yaml
   ```

4. **Rollback**
   ```bash
   # GOOD: Rollback with Git
   git revert HEAD
   git push
   # ArgoCD syncs rollback
   ```

5. **Monitoring**
   ```bash
   # GOOD: Monitor deployment
   argocd app get iot-gateway
   argocd app logs iot-gateway
   ```

---

## Unit Economics & KPIs

### Development Costs
- **Initial Setup**: 40-80 hours
- **Pipeline Development**: 60-100 hours
- **Testing & Validation**: 40-60 hours
- **Total**: 140-240 hours

### Operational Costs
- **ArgoCD**: $0 (open source)
- **Monitoring**: $50-200/month
- **CI/CD**: $50-200/month
- **Support**: 10-20 hours/month

### ROI Metrics
- **Deployment Time**: 80-95% reduction
- **Configuration Drift**: Eliminated
- **Human Error**: 70-90% reduction
- **Team Productivity**: 40-60% improvement

### KPI Targets
- **Sync Time**: < 5 minutes
- **Deployment Success Rate**: > 99%
- **Configuration Drift**: 0%
- **Rollback Time**: < 5 minutes
- **Compliance**: 100%

---

## Integration Points / Related Skills

### Upstream Skills
- **86. Advanced IaC IoT**: Infrastructure provisioning
- **87. Chaos Engineering IoT**: Resilience testing
- **89. Multi-Cloud IoT**: Multi-cloud strategy

### Parallel Skills
- **90. Disaster Recovery IoT**: DR planning
- **73. Differential OTA Updates**: OTA deployment
- **74. Atomic AB Partitioning**: Firmware updates
- **75. Fleet Campaign Management**: Fleet management

### Downstream Skills
- **14. Monitoring and Observability**: Metrics and tracing
- **24. Security Practices**: Infrastructure security
- **81. SaaS FinOps Pricing**: Cost optimization
- **84. Compliance AI Governance**: Compliance

### Cross-Domain Skills
- **15. DevOps Infrastructure**: CI/CD pipelines
- **59. Architecture Decision**: Architecture decisions
- **64. Meta Standards**: Coding standards
- **72. Metacognitive Skill Architect**: System design

---

## References & Resources

### Documentation
- [ArgoCD Documentation](https://argoproj.github.io/argo-cd/)
- [Flux Documentation](https://fluxcd.io/docs/)
- [GitOps Principles](https://www.weave.works/technologies/gitops/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)

### Best Practices
- [GitOps Best Practices](https://www.weave.works/blog/gitops-operations-by-pull-request/)
- [ArgoCD Best Practices](https://argoproj.github.io/argo-cd/operator-manual/best-practices/)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)

### Tools & Libraries
- [ArgoCD](https://argoproj.github.io/argo-cd/)
- [Flux](https://fluxcd.io/)
- [Helm](https://helm.sh/)
- [Kustomize](https://kustomize.io/)
