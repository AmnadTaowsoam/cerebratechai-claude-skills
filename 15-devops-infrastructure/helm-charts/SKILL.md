# Helm Charts

A comprehensive guide to Helm charts for Kubernetes package management.

## Table of Contents

1. [Helm Concepts](#helm-concepts)
2. [Chart Structure](#chart-structure)
3. [Templates](#templates)
4. [Values Files](#values-files)
5. [Chart Dependencies](#chart-dependencies)
6. [Hooks](#hooks)
7. [Chart Testing](#chart-testing)
8. [Chart Repository](#chart-repository)
9. [Release Management](#release-management)
10. [Production Patterns](#production-patterns)
11. [Best Practices](#best-practices)

---

## Helm Concepts

### What is Helm?

Helm is a package manager for Kubernetes that helps you manage Kubernetes applications.

```
┌─────────────────────────────────────────────────────────────┐
│                      Helm Architecture                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌──────────┐       ┌──────────┐       ┌──────────┐    │
│   │   Helm   │──────>│  Chart   │──────>│ Kubernetes│   │
│   │  Client  │       │          │       │ Cluster  │    │
│   └──────────┘       └──────────┘       └──────────┘    │
│                                                             │
│   Chart = Templates + Values + Metadata                      │
│   Release = Instance of a Chart                              │
│   Repository = Collection of Charts                          │
└─────────────────────────────────────────────────────────────┘
```

### Key Concepts

| Concept | Description |
|---------|-------------|
| **Chart** | A package of pre-configured Kubernetes resources |
| **Release** | A specific instance of a chart deployed to a cluster |
| **Repository** | A collection of charts available for download |
| **Template** | A Go template file that generates Kubernetes manifests |
| **Values** | Configuration values that override defaults in templates |
| **Hook** | A special annotation that allows actions at specific points |
| **Chart.yaml** | Metadata about the chart |
| **requirements.yaml** | Chart dependencies |

---

## Chart Structure

### Standard Chart Structure

```
myapp/
├── Chart.yaml              # Chart metadata
├── values.yaml            # Default configuration values
├── values.schema.json     # Values schema validation
├── .helmignore            # Files to ignore when packaging
├── charts/                # Chart dependencies
├── templates/             # Template files
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── hpa.yaml
│   ├── _helpers.tpl       # Template helpers
│   └── NOTES.txt         # Post-install notes
└── templates/tests/       # Test templates
    └── test-connection.yaml
```

### Chart.yaml

```yaml
apiVersion: v2
name: myapp
description: A Helm chart for my application
type: application
version: 0.1.0
appVersion: "1.0.0"
keywords:
  - myapp
  - web
maintainers:
  - name: John Doe
    email: john@example.com
icon: https://example.com/icon.png
home: https://example.com
sources:
  - https://github.com/example/myapp
dependencies:
  - name: postgresql
    version: 12.x.x
    repository: https://charts.bitnami.com/bitnami
```

### values.yaml

```yaml
# Default values for myapp
replicaCount: 3

image:
  repository: myapp
  pullPolicy: IfNotPresent
  tag: "1.0.0"

imagePullSecrets: []

serviceAccount:
  create: true
  annotations: {}
  name: ""

podAnnotations: {}

podSecurityContext: {}

securityContext: {}

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: false
  className: ""
  annotations: {}
  hosts:
    - host: chart-example.local
      paths:
        - path: /
          pathType: Prefix
  tls: []

resources: {}

autoscaling:
  enabled: false
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80
  targetMemoryUtilizationPercentage: 80

nodeSelector: {}

tolerations: []

affinity: {}
```

---

## Templates

### Template Syntax

```yaml
# Variables
{{ .Values.replicaCount }}

# Conditional
{{ if .Values.ingress.enabled }}
# ... content ...
{{ end }}

# Loop
{{ range .Values.hosts }}
# ... content ...
{{ end }}

# With
{{ with .Values.service }}
# ... use . to refer to service ...
{{ end }}

# Include
{{ include "myapp.fullname" . }}

# Default
{{ .Values.someValue | default "default-value" }}

# Quote
{{ .Values.someValue | quote }}

# ToYaml
{{ .Values.someConfig | toYaml }}
```

### Deployment Template

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "myapp.fullname" . }}
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "myapp.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      annotations:
        checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
        {{- with .Values.podAnnotations }}
        {{- toYaml . | nindent 8 }}
        {{- end }}
      labels:
        {{- include "myapp.selectorLabels" . | nindent 8 }}
    spec:
      {{- with .Values.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      serviceAccountName: {{ include "myapp.serviceAccountName" . }}
      securityContext:
        {{- toYaml .Values.podSecurityContext | nindent 8 }}
      containers:
      - name: {{ .Chart.Name }}
        securityContext:
          {{- toYaml .Values.securityContext | nindent 10 }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
        imagePullPolicy: {{ .Values.image.pullPolicy }}
        ports:
        - name: http
          containerPort: {{ .Values.service.port }}
          protocol: TCP
        livenessProbe:
          httpGet:
            path: /
            port: http
        readinessProbe:
          httpGet:
            path: /
            port: http
        resources:
          {{- toYaml .Values.resources | nindent 10 }}
      {{- with .Values.nodeSelector }}
      nodeSelector:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.affinity }}
      affinity:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.tolerations }}
      tolerations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
```

### Service Template

```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ include "myapp.fullname" . }}
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
spec:
  type: {{ .Values.service.type }}
  ports:
    - port: {{ .Values.service.port }}
      targetPort: http
      protocol: TCP
      name: http
  selector:
    {{- include "myapp.selectorLabels" . | nindent 4 }}
```

### Ingress Template

```yaml
{{- if .Values.ingress.enabled -}}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ include "myapp.fullname" . }}
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
  {{- with .Values.ingress.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  {{- if .Values.ingress.className }}
  ingressClassName: {{ .Values.ingress.className }}
  {{- end }}
  {{- if .Values.ingress.tls }}
  tls:
    {{- range .Values.ingress.tls }}
    - hosts:
        {{- range .hosts }}
        - {{ . | quote }}
        {{- end }}
      secretName: {{ .secretName }}
    {{- end }}
  {{- end }}
  rules:
    {{- range .Values.ingress.hosts }}
    - host: {{ .host | quote }}
      http:
        paths:
          {{- range .paths }}
          - path: {{ .path }}
            pathType: {{ .pathType }}
            backend:
              service:
                name: {{ include "myapp.fullname" $ }}
                port:
                  number: {{ $.Values.service.port }}
          {{- end }}
    {{- end }}
{{- end }}
```

### ConfigMap Template

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "myapp.fullname" . }}
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
data:
  config.yaml: |
    {{- toYaml .Values.config | nindent 4 }}
```

### Secret Template

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: {{ include "myapp.fullname" . }}
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
type: Opaque
data:
  {{- range $key, $value := .Values.secrets }}
  {{ $key }}: {{ $value | b64enc }}
  {{- end }}
```

### HPA Template

```yaml
{{- if .Values.autoscaling.enabled }}
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {{ include "myapp.fullname" . }}
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {{ include "myapp.fullname" . }}
  minReplicas: {{ .Values.autoscaling.minReplicas }}
  maxReplicas: {{ .Values.autoscaling.maxReplicas }}
  metrics:
    {{- if .Values.autoscaling.targetCPUUtilizationPercentage }}
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: {{ .Values.autoscaling.targetCPUUtilizationPercentage }}
    {{- end }}
    {{- if .Values.autoscaling.targetMemoryUtilizationPercentage }}
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: {{ .Values.autoscaling.targetMemoryUtilizationPercentage }}
    {{- end }}
{{- end }}
```

### Helper Templates (_helpers.tpl)

```yaml
{{/*
Expand the name of the chart.
*/}}
{{- define "myapp.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "myapp.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "myapp.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "myapp.labels" -}}
helm.sh/chart: {{ include "myapp.chart" . }}
{{ include "myapp.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "myapp.selectorLabels" -}}
app.kubernetes.io/name: {{ include "myapp.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "myapp.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "myapp.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}
```

---

## Values Files

### Production Values

```yaml
# values-production.yaml
replicaCount: 5

image:
  repository: registry.example.com/myapp
  pullPolicy: Always
  tag: "1.0.0"

imagePullSecrets:
  - name: registry-credentials

resources:
  limits:
    cpu: 1000m
    memory: 1Gi
  requests:
    cpu: 500m
    memory: 512Mi

autoscaling:
  enabled: true
  minReplicas: 5
  maxReplicas: 20
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"
  hosts:
    - host: myapp.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: myapp-tls
      hosts:
        - myapp.example.com

nodeSelector:
  node.kubernetes.io/instance-type: m5.large

tolerations:
  - key: "dedicated"
    operator: "Equal"
    value: "app"
    effect: "NoSchedule"
```

### Staging Values

```yaml
# values-staging.yaml
replicaCount: 2

image:
  repository: registry.example.com/myapp
  pullPolicy: Always
  tag: "1.0.0-staging"

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 5
  targetCPUUtilizationPercentage: 80
  targetMemoryUtilizationPercentage: 80

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-staging
  hosts:
    - host: myapp-staging.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: myapp-staging-tls
      hosts:
        - myapp-staging.example.com
```

### Development Values

```yaml
# values-development.yaml
replicaCount: 1

image:
  repository: myapp
  pullPolicy: Never
  tag: "dev"

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 100m
    memory: 128Mi

autoscaling:
  enabled: false

ingress:
  enabled: false
```

---

## Chart Dependencies

### requirements.yaml (Helm 2)

```yaml
dependencies:
  - name: postgresql
    version: 12.x.x
    repository: https://charts.bitnami.com/bitnami
    condition: postgresql.enabled
    tags:
      - database

  - name: redis
    version: 17.x.x
    repository: https://charts.bitnami.com/bitnami
    condition: redis.enabled
    tags:
      - cache
```

### Chart.yaml (Helm 3)

```yaml
apiVersion: v2
name: myapp
version: 0.1.0

dependencies:
  - name: postgresql
    version: 12.x.x
    repository: https://charts.bitnami.com/bitnami
    condition: postgresql.enabled

  - name: redis
    version: 17.x.x
    repository: https://charts.bitnami.com/bitnami
    condition: redis.enabled
```

### Using Dependencies

```yaml
# In values.yaml
postgresql:
  enabled: true
  auth:
    postgresPassword: secret
    database: myapp

redis:
  enabled: true
  auth:
    enabled: false
```

### Aliasing Dependencies

```yaml
dependencies:
  - name: postgresql
    version: 12.x.x
    repository: https://charts.bitnami.com/bitnami
    alias: db
```

---

## Hooks

### Pre-Install Hook

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: {{ include "myapp.fullname" . }}-pre-install
  annotations:
    "helm.sh/hook": pre-install
    "helm.sh/hook-weight": "-5"
    "helm.sh/hook-delete-policy": before-hook-creation
spec:
  template:
    spec:
      containers:
      - name: pre-install
        image: busybox
        command: ["/bin/sh", "-c", "echo Pre-install hook"]
      restartPolicy: OnFailure
```

### Post-Install Hook

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: {{ include "myapp.fullname" . }}-post-install
  annotations:
    "helm.sh/hook": post-install
    "helm.sh/hook-weight": "5"
    "helm.sh/hook-delete-policy": hook-succeeded
spec:
  template:
    spec:
      containers:
      - name: post-install
        image: busybox
        command: ["/bin/sh", "-c", "echo Post-install hook"]
      restartPolicy: OnFailure
```

### Pre-Upgrade Hook

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: {{ include "myapp.fullname" . }}-pre-upgrade
  annotations:
    "helm.sh/hook": pre-upgrade
    "helm.sh/hook-delete-policy": before-hook-creation
spec:
  template:
    spec:
      containers:
      - name: pre-upgrade
        image: busybox
        command: ["/bin/sh", "-c", "echo Pre-upgrade hook"]
      restartPolicy: OnFailure
```

### Post-Upgrade Hook

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: {{ include "myapp.fullname" . }}-post-upgrade
  annotations:
    "helm.sh/hook": post-upgrade
    "helm.sh/hook-delete-policy": hook-succeeded
spec:
  template:
    spec:
      containers:
      - name: post-upgrade
        image: busybox
        command: ["/bin/sh", "-c", "echo Post-upgrade hook"]
      restartPolicy: OnFailure
```

### Pre-Delete Hook

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: {{ include "myapp.fullname" . }}-pre-delete
  annotations:
    "helm.sh/hook": pre-delete
    "helm.sh/hook-delete-policy": before-hook-creation
spec:
  template:
    spec:
      containers:
      - name: pre-delete
        image: busybox
        command: ["/bin/sh", "-c", "echo Pre-delete hook"]
      restartPolicy: OnFailure
```

---

## Chart Testing

### Test Template

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: {{ include "myapp.fullname" . }}-test-connection
  annotations:
    "helm.sh/hook": test
spec:
  containers:
  - name: wget
    image: busybox
    command: ["/bin/sh", "-c", "wget --no-verbose --tries=1 --spider http://{{ include "myapp.fullname" . }}:{{ .Values.service.port }}/health"]
  restartPolicy: Never
```

### Running Tests

```bash
# Lint chart
helm lint ./myapp

# Template chart
helm template ./myapp

# Dry run
helm install myapp ./myapp --dry-run --debug

# Run tests
helm test myapp
```

### Automated Testing

```yaml
# .github/workflows/helm-test.yml
name: Helm Chart CI

on:
  push:
    paths:
      - 'charts/**'
    branches:
      - main

jobs:
  lint-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Helm
        uses: azure/setup-helm@v3
        with:
          version: 'v3.12.0'
      - name: Run helm lint
        run: |
          helm lint ./charts/myapp
      - name: Run helm template
        run: |
          helm template ./charts/myapp
```

---

## Chart Repository

### Creating a Chart Repository

```bash
# Create index.yaml
helm repo index .

# Serve with GitHub Pages
# Upload charts to gh-pages branch
```

### index.yaml

```yaml
apiVersion: v1
entries:
  myapp:
    - apiVersion: v2
      appVersion: 1.0.0
      created: "2024-01-01T00:00:00.000Z"
      description: A Helm chart for my application
      digest: abc123def456...
      name: myapp
      urls:
        - https://example.com/charts/myapp-0.1.0.tgz
      version: 0.1.0
generated: "2024-01-01T00:00:00.000Z"
```

### Publishing Charts

```bash
# Package chart
helm package ./myapp

# Update index
helm repo index .

# Upload to GitHub
git add myapp-0.1.0.tgz index.yaml
git commit -m "Release myapp-0.1.0"
git push
```

### Adding Repository

```bash
# Add repository
helm repo add myrepo https://example.com/charts

# Update repository
helm repo update

# Search charts
helm search repo myrepo

# Install from repository
helm install myapp myrepo/myapp
```

---

## Release Management

### Install Release

```bash
# Install with default values
helm install myapp ./myapp

# Install with custom values
helm install myapp ./myapp -f values-production.yaml

# Install with set values
helm install myapp ./myapp --set replicaCount=5 --set image.tag=1.0.0

# Install in specific namespace
helm install myapp ./myapp -n production

# Install with create namespace
helm install myapp ./myapp -n production --create-namespace
```

### Upgrade Release

```bash
# Upgrade with new values
helm upgrade myapp ./myapp -f values-production.yaml

# Upgrade with new image
helm upgrade myapp ./myapp --set image.tag=2.0.0

# Upgrade with reuse values
helm upgrade myapp ./myapp --reuse-values

# Dry run upgrade
helm upgrade myapp ./myapp --dry-run --debug
```

### Rollback Release

```bash
# List revisions
helm history myapp

# Rollback to previous revision
helm rollback myapp

# Rollback to specific revision
helm rollback myapp 2

# Rollback with timeout
helm rollback myapp --timeout 5m
```

### Uninstall Release

```bash
# Uninstall release
helm uninstall myapp

# Uninstall with keep history
helm uninstall myapp --keep-history

# Uninstall with timeout
helm uninstall myapp --timeout 5m
```

### List Releases

```bash
# List all releases
helm list

# List releases in all namespaces
helm list -A

# List releases with filter
helm list -l app=myapp

# List releases in specific namespace
helm list -n production
```

---

## Production Patterns

### Production Deployment

```bash
# Install production release
helm install myapp ./myapp \
  -n production \
  --create-namespace \
  -f values-production.yaml \
  --wait \
  --timeout 10m
```

### Blue/Green Deployment

```bash
# Install blue release
helm install myapp-blue ./myapp \
  -n production \
  -f values-production.yaml \
  --set ingress.hosts[0].host=myapp-blue.example.com

# Install green release
helm install myapp-green ./myapp \
  -n production \
  -f values-production.yaml \
  --set image.tag=2.0.0 \
  --set ingress.hosts[0].host=myapp-green.example.com

# Switch traffic to green
# Update ingress to point to green service
```

### Canary Deployment

```bash
# Install main release
helm install myapp ./myapp \
  -n production \
  -f values-production.yaml \
  --set replicaCount=9

# Install canary release
helm install myapp-canary ./myapp \
  -n production \
  -f values-production.yaml \
  --set image.tag=2.0.0 \
  --set replicaCount=1
```

---

## Best Practices

### 1. Use Semantic Versioning

```yaml
# Chart version
version: 1.0.0

# App version
appVersion: "1.0.0"
```

### 2. Use Values Files

```bash
# Use separate values files per environment
helm install myapp ./myapp -f values-production.yaml
```

### 3. Use Labels and Annotations

```yaml
metadata:
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
  annotations:
    checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
```

### 4. Use Hooks for Initialization

```yaml
annotations:
  "helm.sh/hook": pre-install
```

### 5. Use Tests

```yaml
annotations:
  "helm.sh/hook": test
```

### 6. Use Secrets for Sensitive Data

```yaml
data:
  password: {{ .Values.password | b64enc }}
```

### 7. Use Resource Limits

```yaml
resources:
  limits:
    cpu: 1000m
    memory: 1Gi
  requests:
    cpu: 500m
    memory: 512Mi
```

### 8. Use Health Checks

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: http
readinessProbe:
  httpGet:
    path: /ready
    port: http
```

### 9. Use Notes.txt

```yaml
# templates/NOTES.txt
Thank you for installing {{ .Chart.Name }}!

Your release is named {{ .Release.Name }}.

To learn more about the release, try:

  $ helm status {{ .Release.Name }}
  $ helm get all {{ .Release.Name }}
```

### 10. Document Your Chart

```yaml
# Chart.yaml
description: A Helm chart for my application
home: https://example.com
sources:
  - https://github.com/example/myapp
keywords:
  - myapp
  - web
maintainers:
  - name: John Doe
    email: john@example.com
```

---

## Resources

- [Helm Documentation](https://helm.sh/docs/)
- [Helm Best Practices](https://helm.sh/docs/chart_best_practices/)
- [Helm Charts](https://helm.sh/docs/topics/charts/)
- [Helm Template Guide](https://helm.sh/docs/chart_template_guide/)
