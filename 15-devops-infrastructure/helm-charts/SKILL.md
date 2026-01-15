# Helm Charts

## Overview

Helm is a package manager for Kubernetes that helps you manage Kubernetes applications. This skill covers Helm concepts, chart structure, templates, and best practices.

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

### Architecture

```
┌─────────────┐
│   Helm CLI  │
└──────┬──────┘
       │ Install/Upgrade
       ↓
┌─────────────┐
│   Tiller    │ (Helm 2)
│  (Server)    │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│ Kubernetes  │
│  Cluster    │
└─────────────┘
```

### Key Concepts

| Concept | Description |
|---------|-------------|
| **Chart** | A package of pre-configured Kubernetes resources |
| **Release** | An instance of a chart running in a cluster |
| **Repository** | A collection of charts |
| **Values** | Configuration values for a chart |
| **Template** | Go template files that generate Kubernetes manifests |
| **Hooks** | Actions that run at specific points in the release lifecycle |

---

## Chart Structure

### Basic Chart Structure

```
mychart/
├── Chart.yaml          # Chart metadata
├── values.yaml         # Default configuration values
├── values.schema.json  # Values schema validation
├── templates/          # Template files
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── _helpers.tpl    # Helper templates
│   └── NOTES.txt       # Post-install notes
├── charts/             # Chart dependencies
└── README.md           # Chart documentation
```

### Chart.yaml

```yaml
# Chart.yaml
apiVersion: v2
name: mychart
description: A Helm chart for my application
type: application
version: 1.0.0
appVersion: "1.0.0"
keywords:
  - myapp
  - application
maintainers:
  - name: My Name
    email: myemail@example.com
    url: https://github.com/myorg/mychart
icon: https://example.com/icon.png
annotations:
  category: Application
```

### values.yaml

```yaml
# values.yaml
replicaCount: 1

image:
  repository: myapp
  pullPolicy: IfNotPresent
  tag: ""

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
  targetPort: 3000

ingress:
  enabled: false
  className: ""
  annotations: {}
  hosts:
    - host: myapp.example.com
      paths:
        - path: /
          pathType: Prefix
  tls: []

resources: {}

autoscaling:
  enabled: false
  minReplicas: 1
  maxReplicas: 100
  targetCPUUtilizationPercentage: 80
  targetMemoryUtilizationPercentage: 80

nodeSelector: {}

tolerations: []

affinity: {}

config: {}
```

---

## Templates

### Deployment Template

```yaml
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "mychart.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      {{- with .Values.podAnnotations }}
      annotations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      labels:
        {{- include "mychart.selectorLabels" . | nindent 8 }}
    spec:
      {{- with .Values.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      serviceAccountName: {{ include "mychart.serviceAccountName" . }}
      securityContext:
        {{- toYaml .Values.podSecurityContext | nindent 8 }}
      containers:
        - name: {{ .Chart.Name }}
          securityContext:
            {{- toYaml .Values.securityContext | nindent 12 }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - name: http
              containerPort: {{ .Values.service.targetPort }}
              protocol: TCP
          livenessProbe:
            httpGet:
              path: /health
              port: http
          readinessProbe:
            httpGet:
              path: /ready
              port: http
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
          env:
            {{- range $key, $value := .Values.config }}
            - name: {{ $key | upper }}
              value: {{ $value | quote }}
            {{- end }}
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
# templates/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
spec:
  type: {{ .Values.service.type }}
  ports:
    - port: {{ .Values.service.port }}
      targetPort: http
      protocol: TCP
      name: http
  selector:
    {{- include "mychart.selectorLabels" . | nindent 4 }}
```

### Ingress Template

```yaml
# templates/ingress.yaml
{{- if .Values.ingress.enabled -}}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
  {{- with .Values.ingress.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  {{- with .Values.ingress.className }}
  ingressClassName: {{ . }}
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
                name: {{ include "mychart.fullname" $ }}
                port:
                  number: {{ $.Values.service.port }}
          {{- end }}
    {{- end }}
{{- end }}
```

### ConfigMap Template

```yaml
# templates/configmap.yaml
{{- if .Values.config }}
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "mychart.fullname" . }}-config
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
data:
  app.properties: |
    {{- range $key, $value := .Values.config }}
    {{ $key }}={{ $value }}
    {{- end }}
{{- end }}
```

### Secret Template

```yaml
# templates/secret.yaml
{{- if .Values.secret }}
apiVersion: v1
kind: Secret
metadata:
  name: {{ include "mychart.fullname" . }}-secret
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
type: Opaque
stringData:
  {{- range $key, $value := .Values.secret }}
  {{ $key }}: {{ $value | quote }}
  {{- end }}
{{- end }}
```

### HPA Template

```yaml
# templates/hpa.yaml
{{- if .Values.autoscaling.enabled }}
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {{ include "mychart.fullname" . }}
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

### Helper Templates

```yaml
# templates/_helpers.tpl
{{/*
Expand the name of the chart.
*/}}
{{- define "mychart.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "mychart.fullname" -}}
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
{{- define "mychart.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "mychart.labels" -}}
helm.sh/chart: {{ include "mychart.chart" . }}
{{ include "mychart.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "mychart.selectorLabels" -}}
app.kubernetes.io/name: {{ include "mychart.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "mychart.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "mychart.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}
```

### NOTES.txt

```yaml
# templates/NOTES.txt
{{- /*
Thanks for installing {{ .Chart.Name }}!

Your release is named {{ .Release.Name }}.

To learn more about the release, try:

  $ helm status {{ .Release.Name }}
  $ helm get all {{ .Release.Name }}
*/}}

{{- if .Values.ingress.enabled }}
{{- else if contains "NodePort" .Values.service.type }}
  export NODE_PORT=$(kubectl get --namespace {{ .Release.Namespace }} -o jsonpath="{.spec.ports[0].nodePort}" services {{ include "mychart.fullname" . }})
  echo "Visit http://127.0.0.1:$NODE_PORT to use your application"
{{- else if contains "LoadBalancer" .Values.service.type }}
     NOTE: It may take a few minutes for the LoadBalancer IP to be available.
        You can watch the status by running 'kubectl get --namespace {{ .Release.Namespace }} svc -w {{ include "mychart.fullname' . }}'
  export SERVICE_IP=$(kubectl get svc --namespace {{ .Release.Namespace }} {{ include "mychart.fullname" . }} --template "{{"{{ (index .status.loadBalancer.ingress 0).ip }}" }}")
  echo "Visit http://$SERVICE_IP:{{ .Values.service.port }} to use your application"
{{- else if contains "ClusterIP" .Values.service.type }}
  export POD_NAME=$(kubectl get pods --namespace {{ .Release.Namespace }} -l "app.kubernetes.io/name={{ include "mychart.name" . }},app.kubernetes.io/instance={{ .Release.Name }}" -o jsonpath="{.items[0].metadata.name}")
  export CONTAINER_PORT=$(kubectl get pod --namespace {{ .Release.Namespace }} $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
  echo "Visit http://127.0.0.1:8080 to use your application"
  kubectl --namespace {{ .Release.Namespace }} port-forward $POD_NAME 8080:$CONTAINER_PORT
{{- end }}
```

---

## Values Files

### Production Values

```yaml
# values-production.yaml
replicaCount: 3

image:
  repository: myapp
  pullPolicy: Always
  tag: "1.0.0"

service:
  type: LoadBalancer
  port: 80
  targetPort: 3000

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: myapp.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: myapp-tls
      hosts:
        - myapp.example.com

resources:
  limits:
    cpu: 1000m
    memory: 1Gi
  requests:
    cpu: 500m
    memory: 512Mi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80

config:
  NODE_ENV: production
  LOG_LEVEL: info
```

### Development Values

```yaml
# values-development.yaml
replicaCount: 1

image:
  repository: myapp
  pullPolicy: IfNotPresent
  tag: "dev"

service:
  type: NodePort
  port: 80
  targetPort: 3000

ingress:
  enabled: false

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi

autoscaling:
  enabled: false

config:
  NODE_ENV: development
  LOG_LEVEL: debug
```

---

## Chart Dependencies

### Chart.yaml with Dependencies

```yaml
# Chart.yaml
apiVersion: v2
name: mychart
description: A Helm chart for my application
type: application
version: 1.0.0
appVersion: "1.0.0"

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

### Values with Dependencies

```yaml
# values.yaml
postgresql:
  enabled: true
  auth:
    postgresPassword: secretpassword
  primary:
    persistence:
      enabled: true

redis:
  enabled: true
  auth:
    password: secretpassword
  master:
    persistence:
      enabled: true
```

---

## Hooks

### Pre-Install Hook

```yaml
# templates/pre-install-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: {{ include "mychart.fullname" . }}-pre-install
  annotations:
    "helm.sh/hook": pre-install
    "helm.sh/hook-weight": "-5"
    "helm.sh/hook-delete-policy": hook-succeeded
spec:
  template:
    metadata:
      name: {{ include "mychart.fullname" . }}-pre-install
    spec:
      restartPolicy: OnFailure
      containers:
        - name: pre-install
          image: busybox
          command: ["sh", "-c", "echo 'Pre-install hook executed'"]
```

### Post-Install Hook

```yaml
# templates/post-install-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: {{ include "mychart.fullname" . }}-post-install
  annotations:
    "helm.sh/hook": post-install
    "helm.sh/hook-weight": "5"
    "helm.sh/hook-delete-policy": hook-succeeded
spec:
  template:
    metadata:
      name: {{ include "mychart.fullname" . }}-post-install
    spec:
      restartPolicy: OnFailure
      containers:
        - name: post-install
          image: busybox
          command: ["sh", "-c", "echo 'Post-install hook executed'"]
```

### Pre-Upgrade Hook

```yaml
# templates/pre-upgrade-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: {{ include "mychart.fullname" . }}-pre-upgrade
  annotations:
    "helm.sh/hook": pre-upgrade
    "helm.sh/hook-weight": "-5"
    "helm.sh/hook-delete-policy": hook-succeeded
spec:
  template:
    metadata:
      name: {{ include "mychart.fullname" . }}-pre-upgrade
    spec:
      restartPolicy: OnFailure
      containers:
        - name: pre-upgrade
          image: busybox
          command: ["sh", "-c", "echo 'Pre-upgrade hook executed'"]
```

### Post-Upgrade Hook

```yaml
# templates/post-upgrade-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: {{ include "mychart.fullname" . }}-post-upgrade
  annotations:
    "helm.sh/hook": post-upgrade
    "helm.sh/hook-weight": "5"
    "helm.sh/hook-delete-policy": hook-succeeded
spec:
  template:
    metadata:
      name: {{ include "mychart.fullname" . }}-post-upgrade
    spec:
      restartPolicy: OnFailure
      containers:
        - name: post-upgrade
          image: busybox
          command: ["sh", "-c", "echo 'Post-upgrade hook executed'"]
```

---

## Chart Testing

### Lint Chart

```bash
# Lint chart
helm lint ./mychart

# Lint with values
helm lint ./mychart --values values-production.yaml
```

### Template Rendering

```bash
# Render templates
helm template myapp ./mychart

# Render with values
helm template myapp ./mychart --values values-production.yaml

# Render with release name and namespace
helm template myapp ./mychart --values values-production.yaml --release myapp --namespace production
```

### Dry Run

```bash
# Dry run install
helm install myapp ./mychart --dry-run --debug

# Dry run upgrade
helm upgrade myapp ./mychart --dry-run --debug
```

---

## Chart Repository

### Create Chart Repository

```bash
# Create chart repository
helm repo add myrepo https://charts.example.com

# Update repository
helm repo update

# List charts
helm search repo myrepo
```

### Package Chart

```bash
# Package chart
helm package ./mychart

# Package with version
helm package ./mychart --version 1.0.0
```

### Index Chart Repository

```bash
# Create index
helm repo index .

# Upload to repository
# Using GitHub Pages, S3, etc.
```

---

## Release Management

### Install Chart

```bash
# Install chart
helm install myapp ./mychart

# Install with values
helm install myapp ./mychart --values values-production.yaml

# Install with release name and namespace
helm install myapp ./mychart --values values-production.yaml --namespace production
```

### Upgrade Chart

```bash
# Upgrade chart
helm upgrade myapp ./mychart

# Upgrade with values
helm upgrade myapp ./mychart --values values-production.yaml

# Upgrade with new version
helm upgrade myapp ./mychart --version 2.0.0
```

### Rollback

```bash
# Rollback to previous version
helm rollback myapp

# Rollback to specific revision
helm rollback myapp 2

# List revisions
helm history myapp
```

### Uninstall Chart

```bash
# Uninstall chart
helm uninstall myapp

# Uninstall with keep history
helm uninstall myapp --keep-history

# Uninstall with timeout
helm uninstall myapp --timeout 5m
```

---

## Production Patterns

### Production Deployment

```bash
# Install with production values
helm install myapp ./mychart \
  --values values-production.yaml \
  --namespace production \
  --create-namespace \
  --wait \
  --timeout 10m
```

### Upgrade Strategy

```bash
# Upgrade with production values
helm upgrade myapp ./mychart \
  --values values-production.yaml \
  --namespace production \
  --wait \
  --timeout 10m \
  --atomic
```

### Rollback Strategy

```bash
# Rollback on failure
helm upgrade myapp ./mychart \
  --values values-production.yaml \
  --namespace production \
  --wait \
  --timeout 10m \
  --atomic \
  --rollback-on-error
```

---

## Best Practices

### 1. Use Semantic Versioning

```yaml
# Chart.yaml
version: 1.0.0
appVersion: "1.0.0"
```

### 2. Document Your Chart

```markdown
# README.md
# My Chart

## Installation

```bash
helm install myapp ./mychart
```

## Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `replicaCount` | Number of replicas | `1` |
| `image.tag` | Image tag | `""` |
```

### 3. Use Values Schema

```json
// values.schema.json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "replicaCount": {
      "type": "integer",
      "minimum": 1
    },
    "image": {
      "type": "object",
      "properties": {
        "repository": {
          "type": "string"
        },
        "tag": {
          "type": "string"
        }
      },
      "required": ["repository"]
    }
  },
  "required": ["replicaCount", "image"]
}
```

### 4. Use Helper Templates

```yaml
# templates/_helpers.tpl
{{- define "mychart.labels" -}}
helm.sh/chart: {{ include "mychart.chart" . }}
{{ include "mychart.selectorLabels" . }}
{{- end }}
```

### 5. Use Hooks Carefully

```yaml
metadata:
  annotations:
    "helm.sh/hook": post-install
    "helm.sh/hook-weight": "5"
    "helm.sh/hook-delete-policy": hook-succeeded
```

---

## Summary

This skill covers comprehensive Helm charts implementation including:

- **Helm Concepts**: Architecture and key concepts
- **Chart Structure**: Basic chart structure, Chart.yaml, values.yaml
- **Templates**: Deployment, service, ingress, configmap, secret, HPA, helper templates, NOTES.txt
- **Values Files**: Production and development values
- **Chart Dependencies**: Chart.yaml with dependencies and values
- **Hooks**: Pre-install, post-install, pre-upgrade, post-upgrade hooks
- **Chart Testing**: Lint, template rendering, dry run
- **Chart Repository**: Create repo, package chart, index repo
- **Release Management**: Install, upgrade, rollback, uninstall
- **Production Patterns**: Production deployment, upgrade strategy, rollback strategy
- **Best Practices**: Semantic versioning, documentation, values schema, helper templates, hooks
