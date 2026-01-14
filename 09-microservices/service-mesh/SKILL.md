# Service Mesh

## Overview

Comprehensive guide to service mesh patterns using Istio and Linkerd for microservices communication.

## Table of Contents

1. [Service Mesh Concepts](#service-mesh-concepts)
2. [When to Use Service Mesh](#when-to-use-service-mesh)
3. [Istio](#istio)
4. [Linkerd](#linkerd)
5. [mTLS Between Services](#mtls-between-services)
6. [Circuit Breaking](#circuit-breaking)
7. [Retry Policies](#retry-policies)
8. [Canary Deployments](#canary-deployments)
9. [Distributed Tracing](#distributed-tracing)
10. [Production Considerations](#production-considerations)

---

## Service Mesh Concepts

### Core Concepts

```markdown
## Service Mesh Core Concepts

### What is a Service Mesh?
- Infrastructure layer for service-to-service communication
- Manages traffic between microservices
- Provides observability, security, and reliability

### Key Components
- Data Plane: Proxies that handle service communication
- Control Plane: Manages and configures the data plane
- Ingress: Manages external traffic
- Egress: Controls outbound traffic

### Benefits
- mTLS encryption between services
- Traffic management and routing
- Observability (metrics, logs, traces)
- Resilience (retries, circuit breakers)
- Policy enforcement
```

### Architecture

```yaml
# service-mesh-architecture.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: service-mesh
---
# Service Mesh Components
# 1. Control Plane (Istiod / Linkerd Control Plane)
# 2. Data Plane (Envoy Sidecars / Linkerd Proxies)
# 3. Ingress Gateway
# 4. Egress Gateway
# 5. Monitoring Stack (Prometheus, Grafana, Jaeger)
```

---

## When to Use Service Mesh

### Use Cases

```markdown
## When to Use Service Mesh

### Yes, Use Service Mesh When:
- You have many microservices (>10-20)
- Services use multiple protocols (HTTP, gRPC, TCP)
- You need fine-grained traffic control
- Security requirements (mTLS, policy enforcement)
- Complex deployment patterns (canary, blue-green)
- Need deep observability across services
- Multi-cloud or hybrid deployments

### No, Consider Alternatives When:
- Small number of services (<5)
- Simple architecture (monolith or few services)
- All services in same network/cluster
- Kubernetes Ingress is sufficient
- Cost/complexity concerns outweigh benefits
```

### Decision Matrix

```typescript
// service-mesh-decision.ts
export interface ServiceMeshDecision {
  useServiceMesh: boolean;
  reason: string;
  recommended: 'istio' | 'linkerd' | 'consul' | 'none';
}

export class ServiceMeshEvaluator {
  static evaluate(context: {
    serviceCount: number;
    protocols: string[];
    securityRequired: boolean;
    deploymentComplexity: 'simple' | 'moderate' | 'complex';
    observabilityNeeds: 'basic' | 'advanced';
    multiCloud: boolean;
  }): ServiceMeshDecision {
    const {
      serviceCount,
      protocols,
      securityRequired,
      deploymentComplexity,
      observabilityNeeds,
      multiCloud
    } = context;
    
    // Decision logic
    if (serviceCount < 5 && deploymentComplexity === 'simple') {
      return {
        useServiceMesh: false,
        reason: 'Small service count with simple deployment',
        recommended: 'none'
      };
    }
    
    if (securityRequired && (serviceCount > 10 || multiCloud)) {
      return {
        useServiceMesh: true,
        reason: 'Security requirements with multiple services or multi-cloud',
        recommended: 'istio'
      };
    }
    
    if (deploymentComplexity === 'complex' || observabilityNeeds === 'advanced') {
      return {
        useServiceMesh: true,
        reason: 'Complex deployment or advanced observability needs',
        recommended: protocols.includes('grpc') ? 'istio' : 'linkerd'
      };
    }
    
    return {
      useServiceMesh: false,
      reason: 'Current architecture doesn\'t require service mesh',
      recommended: 'none'
    };
  }
}

// Usage
const decision = ServiceMeshEvaluator.evaluate({
  serviceCount: 15,
  protocols: ['http', 'grpc'],
  securityRequired: true,
  deploymentComplexity: 'complex',
  observabilityNeeds: 'advanced',
  multiCloud: false
});

console.log(decision);
```

---

## Istio

### Installation

```bash
# istio-install.sh
#!/bin/bash

# Download Istio
curl -L https://istio.io/downloadIstio | sh -

# Move to istio directory
cd istio-*

# Add istioctl to PATH
export PATH=$PWD/bin:$PATH

# Install Istio with default profile
istioctl install --set profile=demo -y

# Verify installation
istioctl verify-install

# Enable automatic sidecar injection
kubectl label namespace default istio-injection=enabled
```

### Default Profile Configuration

```yaml
# istio-config.yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  name: istio-operator
  namespace: istio-system
spec:
  profile: default
  components:
    pilot:
      k8s:
        resources:
          requests:
            cpu: 500m
            memory: 2048Mi
          limits:
            cpu: 1000m
            memory: 4096Mi
    ingressGateways:
    - name: istio-ingressgateway
      enabled: true
      k8s:
        service:
          type: LoadBalancer
    egressGateways:
    - name: istio-egressgateway
      enabled: true
  values:
    global:
      mtls:
        enabled: true
      proxy:
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
```

### Traffic Management

```yaml
# istio-traffic-management.yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: reviews
spec:
  hosts:
  - reviews
  http:
  - match:
    - headers:
        end-user:
          exact: jason
    route:
    - destination:
        host: reviews
        subset: v2
  - route:
    - destination:
        host: reviews
        subset: v1
---
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: reviews
spec:
  host: reviews
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
  - name: v3
    labels:
      version: v3
---
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: bookinfo-gateway
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "*"
```

### Security Policies

```yaml
# istio-security.yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system
spec:
  mtls:
    mode: STRICT
---
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: allow-get-reviews
  namespace: default
spec:
  selector:
    matchLabels:
      app: reviews
  action: ALLOW
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/default/sa/bookinfo-productpage"]
    to:
    - operation:
        methods: ["GET"]
```

---

## Linkerd

### Installation

```bash
# linkerd-install.sh
#!/bin/bash

# Install Linkerd CLI
curl -sL https://run.linkerd.io/install | sh

# Verify installation
linkerd version

# Install Linkerd on cluster
linkerd install --crds | kubectl apply -f -
linkerd install | kubectl apply -f -

# Verify installation
linkerd check

# Install demo app
curl -sL https://run.linkerd.io/emojivoto.yml | kubectl apply -f -

# Inject Linkerd into namespace
kubectl get deploy -n emojivoto-frontend -o yaml | linkerd inject - | kubectl apply -f -
```

### Configuration

```yaml
# linkerd-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: linkerd-config
  namespace: linkerd
data:
  config.yaml: |-
    proxy:
      image:
        version: stable-2.12.0
      resources:
        cpu:
          request: 100m
          limit: 1
        memory:
          request: 20Mi
          limit: 200Mi
    identityTrustAnchorsPEM: |
      -----BEGIN CERTIFICATE-----
      ... trust anchor PEM ...
      -----END CERTIFICATE-----
    profile:
      type: default
---
apiVersion: v1
kind: ServiceProfile
metadata:
  name: emoji-svc
  namespace: emojivoto
spec:
  routes:
  - name: GET /api/list
    condition:
      method: GET
      pathRegex: /api/list
    responseClasses:
    - name: success
      isFailure: false
      statusCodes:
        - 200
    - name: server-error
      isFailure: true
      statusCodes:
        - 500
        - 502
        - 503
        - 504
```

---

## mTLS Between Services

### Istio mTLS

```yaml
# istio-mtls.yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: strict-mtls
  namespace: default
spec:
  selector:
    matchLabels:
      app: my-app
  mtls:
    mode: STRICT
---
# Permissive mode for gradual rollout
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: permissive-mtls
  namespace: default
spec:
  selector:
    matchLabels:
      app: my-app
  mtls:
    mode: PERMISSIVE
---
# Disable mTLS for specific service
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: disable-mtls
  namespace: default
spec:
  selector:
    matchLabels:
      app: legacy-app
  mtls:
    mode: DISABLE
```

### Linkerd mTLS

```bash
# Linkerd automatically enables mTLS
# Verify mTLS status
linkerd viz -n linkerd edges -o wide

# Check specific service
linkerd viz -n <namespace> edges svc/<service-name>

# Disable mTLS for specific service (not recommended)
kubectl annotate service <service-name> \
  config.linkerd.io/proxy-mode=disabled \
  -n <namespace>
```

---

## Circuit Breaking

### Istio Circuit Breaker

```yaml
# istio-circuit-breaker.yaml
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: httpbin
spec:
  host: httpbin
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 50
        maxRequestsPerConnection: 2
    outlierDetection:
      consecutiveGatewayFailure: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
      minHealthPercent: 40
```

### Linkerd Circuit Breaker

```yaml
# linkerd-circuit-breaker.yaml
apiVersion: v1
kind: ServiceProfile
metadata:
  name: my-service
  namespace: default
spec:
  routes:
  - name: api-route
    condition:
      method: GET
      pathRegex: /api/.*
    circuitBreakers:
      consecutiveErrors: 5
      interval: 30s
      trippingTimeout: 30s
      maxPendingRequests: 100
```

---

## Retry Policies

### Istio Retry

```yaml
# istio-retry.yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: reviews
spec:
  hosts:
  - reviews
  http:
  - route:
    - destination:
        host: reviews
        subset: v1
    retry:
      attempts: 3
      perTryTimeout: 2s
      retryOn:
      - 5xx
      - connect-failure
      - refused-stream
      - reset
      - retriable-4xx
```

### Linkerd Retry

```yaml
# linkerd-retry.yaml
apiVersion: v1
kind: ServiceProfile
metadata:
  name: my-service
  namespace: default
spec:
  routes:
  - name: retry-route
    condition:
      method: POST
      pathRegex: /api/.*
    retries:
      budget:
        retryRatio: 0.2
        minRetriesPerSecond: 10
        percentile: 0.9
      initialDelayMs: 100
      maxDelayMs: 1000
```

---

## Canary Deployments

### Istio Canary

```yaml
# istio-canary.yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: reviews
spec:
  hosts:
  - reviews
  http:
  - match:
    - headers:
        x-canary:
          exact: "true"
    route:
    - destination:
        host: reviews
        subset: v2
  - route:
    - destination:
        host: reviews
        subset: v1
      weight: 90
    - destination:
        host: reviews
        subset: v2
      weight: 10
---
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: reviews
spec:
  host: reviews
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
```

### Linkerd Canary

```yaml
# linkerd-canary.yaml
apiVersion: split.smi-spec.io/v1alpha2
kind: TrafficSplit
metadata:
  name: reviews-canary
  namespace: default
spec:
  service: reviews
  backends:
  - service: reviews-v1
    weight: 90
  - service: reviews-v2
    weight: 10
```

---

## Distributed Tracing

### Istio Tracing

```yaml
# istio-tracing.yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  name: istio-operator
  namespace: istio-system
spec:
  profile: default
  values:
    tracing:
      enabled: true
      sampling: 10.0
      provider: jaeger
      jaeger:
        # Use external Jaeger
        enabled: false
        agentHost: jaeger-collector.istio-system
        agentPort: 6831
```

### Linkerd Tracing

```yaml
# linkerd-tracing.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: linkerd-config
  namespace: linkerd
data:
  config.yaml: |-
    profiler:
      enabled: true
    traceCollector:
      host: collector.linkerd-jaeger
      port: 9411
      sampling: 1.0
```

---

## Production Considerations

### Resource Requirements

```yaml
# istio-production-resources.yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  name: istio-operator
  namespace: istio-system
spec:
  profile: production
  components:
    pilot:
      k8s:
        resources:
          requests:
            cpu: 1000m
            memory: 4096Mi
          limits:
            cpu: 2000m
            memory: 8192Mi
        replicas: 2
    ingressGateways:
    - name: istio-ingressgateway
      enabled: true
      k8s:
        service:
          type: LoadBalancer
        resources:
          requests:
            cpu: 500m
            memory: 512Mi
          limits:
            cpu: 1000m
            memory: 1024Mi
        replicas: 2
    egressGateways:
    - name: istio-egressgateway
      enabled: true
      k8s:
        resources:
          requests:
            cpu: 200m
            memory: 256Mi
          limits:
            cpu: 500m
            memory: 512Mi
        replicas: 2
  values:
    global:
      proxy:
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
```

### Monitoring Stack

```yaml
# istio-monitoring.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: monitoring
---
# Prometheus
apiVersion: v1
kind: Service
metadata:
  name: prometheus
  namespace: monitoring
spec:
  ports:
  - name: prometheus
    port: 9090
    targetPort: 9090
  selector:
    app: prometheus
---
# Grafana
apiVersion: v1
kind: Service
metadata:
  name: grafana
  namespace: monitoring
spec:
  ports:
  - name: grafana
    port: 3000
    targetPort: 3000
  selector:
    app: grafana
---
# Jaeger
apiVersion: v1
kind: Service
metadata:
  name: jaeger
  namespace: monitoring
spec:
  ports:
  - name: jaeger-query
    port: 16686
    targetPort: 16686
  - name: jaeger-collector
    port: 14268
    targetPort: 14268
  selector:
    app: jaeger
```

---

## Additional Resources

- [Istio Documentation](https://istio.io/latest/docs/)
- [Linkerd Documentation](https://linkerd.io/latest/getting-started/)
- [Service Mesh Patterns](https://servicemesh.es/)
- [CNCF Service Mesh Landscape](https://landscape.cncf.io/category=service-mesh&format=card-mode&grouping=category)
