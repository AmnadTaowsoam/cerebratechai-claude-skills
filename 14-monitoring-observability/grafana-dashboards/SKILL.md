# Grafana Dashboards

## Overview

Grafana is an open-source analytics and interactive visualization platform that allows you to query, visualize, alert on, and understand your metrics. This skill covers Grafana setup, dashboard design, and common patterns.

## Table of Contents

1. [Grafana Setup](#grafana-setup)
2. [Data Sources](#data-sources)
3. [Dashboard Design Principles](#dashboard-design-principles)
4. [Panel Types](#panel-types)
5. [Variables and Templating](#variables-and-templating)
6. [Alerts](#alerts)
7. [Common Dashboard Patterns](#common-dashboard-patterns)
8. [Dashboard as Code](#dashboard-as-code)
9. [Best Practices](#best-practices)

---

## Grafana Setup

### Docker Installation

```yaml
# docker-compose.yml
version: '3.8'

services:
  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
    volumes:
      - grafana_data:/var/lib/grafana
      - grafana_provisioning:/etc/grafana/provisioning
    restart: unless-stopped

volumes:
  grafana_data:
  grafana_provisioning:
```

### Provisioning Data Sources

```yaml
# provisioning/datasources/prometheus.yml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true
    jsonData:
      httpMethod: POST
      timeInterval: 15s
```

### Provisioning Dashboards

```yaml
# provisioning/dashboards/dashboard.yml
apiVersion: 1

providers:
  - name: 'Default'
    orgId: 1
    folder: ''
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    allowUiUpdates: true
    options:
      path: /etc/grafana/provisioning/dashboards
```

---

## Data Sources

### Prometheus Data Source

```json
{
  "name": "Prometheus",
  "type": "prometheus",
  "url": "http://prometheus:9090",
  "access": "proxy",
  "isDefault": true,
  "jsonData": {
    "httpMethod": "POST",
    "timeInterval": "15s",
    "exemplarTraceIdDestinations": [
      {
        "datasourceUid": "jaeger",
        "name": "traceID"
      }
    ]
  }
}
```

### Loki Data Source

```json
{
  "name": "Loki",
  "type": "loki",
  "url": "http://loki:3100",
  "access": "proxy",
  "jsonData": {
    "maxLines": 1000,
    "derivedFields": [
      {
        "datasourceUid": "jaeger",
        "matcherRegex": "traceID=(\\w+)",
        "name": "traceID",
        "url": "$${__value.raw}"
      }
    ]
  }
}
```

### Elasticsearch Data Source

```json
{
  "name": "Elasticsearch",
  "type": "elasticsearch",
  "url": "http://elasticsearch:9200",
  "access": "proxy",
  "database": "logs-*",
  "jsonData": {
    "esVersion": "7.0.0",
    "timeField": "@timestamp",
    "maxConcurrentShardRequests": 5
  }
}
```

---

## Dashboard Design Principles

### Layout Guidelines

1. **Important metrics at the top**
2. **Related metrics grouped together**
3. **Consistent color schemes**
4. **Clear labels and titles**
5. **Appropriate time ranges**

### Dashboard Structure

```
┌─────────────────────────────────────────────────────────┐
│  Title: Application Overview                          │
├─────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────┐ │
│  │ Requests│  │ Errors  │  │ Latency │  │ Uptime│ │
│  └─────────┘  └─────────┘  └─────────┘  └─────┘ │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────┐ │
│  │         Request Rate (Time Series)               │ │
│  └─────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────┐ │
│  │         Error Rate (Time Series)                │ │
│  └─────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────┐ │
│  │         Response Time (Histogram)               │ │
│  └─────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### Color Schemes

```json
{
  "colors": {
    "success": "#50fa7b",
    "warning": "#ffb86c",
    "error": "#ff5555",
    "info": "#8be9fd"
  }
}
```

---

## Panel Types

### Time Series

```json
{
  "type": "timeseries",
  "title": "Request Rate",
  "gridPos": { "h": 8, "w": 12, "x": 0, "y": 0 },
  "targets": [
    {
      "expr": "sum by (job) (rate(http_requests_total[5m]))",
      "legendFormat": "{{job}}"
    }
  ],
  "fieldConfig": {
    "defaults": {
      "custom": {
        "lineWidth": 2,
        "fillOpacity": 10,
        "thresholdsStyle": {
          "mode": "line"
        }
      },
      "color": {
        "mode": "palette-classic"
      },
      "thresholds": {
        "steps": [
          { "color": "green", "value": null },
          { "color": "red", "value": 100 }
        ]
      }
    }
  }
}
```

### Stat Panel

```json
{
  "type": "stat",
  "title": "Total Requests",
  "gridPos": { "h": 4, "w": 4, "x": 0, "y": 0 },
  "targets": [
    {
      "expr": "sum(increase(http_requests_total[1h]))",
      "legendFormat": "Total"
    }
  ],
  "fieldConfig": {
    "defaults": {
      "color": {
        "mode": "thresholds"
      },
      "thresholds": {
        "steps": [
          { "color": "green", "value": null },
          { "color": "yellow", "value": 1000 },
          { "color": "red", "value": 5000 }
        ]
      },
      "mappings": []
    },
    "overrides": []
  },
  "options": {
    "graphMode": "area",
    "orientation": "auto",
    "reduceOptions": {
      "values": false,
      "calcs": ["lastNotNull"],
      "fields": ""
    }
  }
}
```

### Gauge Panel

```json
{
  "type": "gauge",
  "title": "Error Rate",
  "gridPos": { "h": 4, "w": 4, "x": 4, "y": 0 },
  "targets": [
    {
      "expr": "sum(rate(http_requests_total{status=~\"5..\"}[5m])) / sum(rate(http_requests_total[5m]))",
      "legendFormat": "Error Rate"
    }
  ],
  "fieldConfig": {
    "defaults": {
      "unit": "percentunit",
      "min": 0,
      "max": 1,
      "thresholds": {
        "steps": [
          { "color": "green", "value": null },
          { "color": "yellow", "value": 0.01 },
          { "color": "red", "value": 0.05 }
        ]
      }
    }
  },
  "options": {
    "orientation": "auto",
    "reduceOptions": {
      "values": false,
      "calcs": ["lastNotNull"],
      "fields": ""
    },
    "showThresholdLabels": false,
    "showThresholdMarkers": true
  }
}
```

### Table Panel

```json
{
  "type": "table",
  "title": "Top Endpoints by Error Rate",
  "gridPos": { "h": 8, "w": 12, "x": 0, "y": 8 },
  "targets": [
    {
      "expr": "topk(10, sum by (path) (rate(http_requests_total{status=~\"5..\"}[5m])) / sum by (path) (rate(http_requests_total[5m])))",
      "format": "table",
      "instant": true
    }
  ],
  "transformations": [
    {
      "id": "organize",
      "options": {
        "excludeByName": { "Time": true, "__name__": true },
        "indexByName": {},
        "renameByName": {}
      }
    }
  ],
  "fieldConfig": {
    "defaults": {
      "color": {
        "mode": "thresholds"
      },
      "thresholds": {
        "steps": [
          { "color": "green", "value": null },
          { "color": "yellow", "value": 0.01 },
          { "color": "red", "value": 0.05 }
        ]
      },
      "unit": "percentunit"
    }
  }
}
```

### Logs Panel

```json
{
  "type": "logs",
  "title": "Application Logs",
  "gridPos": { "h": 8, "w": 12, "x": 12, "y": 8 },
  "targets": [
    {
      "expr": "{job=\"nodejs-app\"}",
      "refId": "A"
    }
  ],
  "options": {
    "showLabels": false,
    "showCommonLabels": false,
    "showTime": true,
    "wrapLogMessage": false,
    "sortOrder": "Descending",
    "dedupStrategy": "none",
    "enableLogDetails": true,
    "prettifyLogMessage": false
  }
}
```

---

## Variables and Templating

### Query Variable

```json
{
  "name": "job",
  "type": "query",
  "datasource": "Prometheus",
  "refresh": 1,
  "query": {
    "query": "label_values(up, job)",
    "refId": "StandardVariableQuery"
  },
  "includeAll": true,
  "multi": true,
  "allValue": ".+"
}
```

### Interval Variable

```json
{
  "name": "interval",
  "type": "interval",
  "query": "1m,5m,10m,30m,1h,6h,12h,1d",
  "auto": true,
  "auto_count": 30,
  "auto_min": "10s"
}
```

### Custom Variable

```json
{
  "name": "environment",
  "type": "custom",
  "query": "production,staging,development",
  "multi": false,
  "includeAll": false
}
```

### Using Variables in Queries

```json
{
  "targets": [
    {
      "expr": "sum by (job) (rate(http_requests_total{job=~\"$job\"}[$interval]))",
      "legendFormat": "{{job}}"
    }
  ]
}
```

### Variable Chaining

```json
{
  "name": "instance",
  "type": "query",
  "datasource": "Prometheus",
  "refresh": 2,
  "query": {
    "query": "label_values(up{job=\"$job\"}, instance)",
    "refId": "StandardVariableQuery"
  },
  "includeAll": true,
  "multi": true
}
```

---

## Alerts

### Panel Alert

```json
{
  "type": "timeseries",
  "title": "Error Rate",
  "alert": {
    "conditions": [
      {
        "evaluator": {
          "params": [0.05],
          "type": "gt"
        },
        "operator": {
          "type": "and"
        },
        "query": {
          "params": ["A", "5m", "now"]
        },
        "reducer": {
          "params": [],
          "type": "avg"
        },
        "type": "query"
      }
    ],
    "executionErrorState": "alerting",
    "frequency": "1m",
    "handler": 1,
    "message": "Error rate is {{ $value }}",
    "name": "High Error Rate",
    "noDataState": "no_data"
  },
  "targets": [
    {
      "expr": "sum(rate(http_requests_total{status=~\"5..\"}[5m])) / sum(rate(http_requests_total[5m]))",
      "refId": "A"
    }
  ]
}
```

### Alert Notification Channels

```json
{
  "name": "Email",
  "type": "email",
  "settings": {
    "addresses": "alerts@example.com"
  },
  "secureSettings": {}
}
```

```json
{
  "name": "Slack",
  "type": "slack",
  "settings": {
    "url": "https://hooks.slack.com/services/...",
    "recipient": "#alerts",
    "uploadImage": true
  }
}
```

---

## Common Dashboard Patterns

### Application Metrics Dashboard

```json
{
  "title": "Application Metrics",
  "panels": [
    {
      "type": "stat",
      "title": "Requests/sec",
      "gridPos": { "h": 4, "w": 4, "x": 0, "y": 0 },
      "targets": [
        {
          "expr": "sum(rate(http_requests_total[1m]))"
        }
      ]
    },
    {
      "type": "stat",
      "title": "Error Rate",
      "gridPos": { "h": 4, "w": 4, "x": 4, "y": 0 },
      "targets": [
        {
          "expr": "sum(rate(http_requests_total{status=~\"5..\"}[1m])) / sum(rate(http_requests_total[1m]))"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "unit": "percentunit"
        }
      }
    },
    {
      "type": "stat",
      "title": "P95 Latency",
      "gridPos": { "h": 4, "w": 4, "x": 8, "y": 0 },
      "targets": [
        {
          "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])))"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "unit": "s"
        }
      }
    },
    {
      "type": "timeseries",
      "title": "Request Rate",
      "gridPos": { "h": 8, "w": 12, "x": 0, "y": 4 },
      "targets": [
        {
          "expr": "sum by (path) (rate(http_requests_total[5m]))",
          "legendFormat": "{{path}}"
        }
      ]
    },
    {
      "type": "timeseries",
      "title": "Error Rate",
      "gridPos": { "h": 8, "w": 12, "x": 12, "y": 4 },
      "targets": [
        {
          "expr": "sum by (status) (rate(http_requests_total{status=~\"5..\"}[5m]))",
          "legendFormat": "{{status}}"
        }
      ]
    }
  ]
}
```

### System Metrics Dashboard

```json
{
  "title": "System Metrics",
  "panels": [
    {
      "type": "timeseries",
      "title": "CPU Usage",
      "gridPos": { "h": 8, "w": 12, "x": 0, "y": 0 },
      "targets": [
        {
          "expr": "100 - (avg by (instance) (rate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)",
          "legendFormat": "{{instance}}"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "unit": "percent",
          "max": 100,
          "min": 0
        }
      }
    },
    {
      "type": "timeseries",
      "title": "Memory Usage",
      "gridPos": { "h": 8, "w": 12, "x": 12, "y": 0 },
      "targets": [
        {
          "expr": "(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100",
          "legendFormat": "{{instance}}"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "unit": "percent",
          "max": 100,
          "min": 0
        }
      }
    },
    {
      "type": "timeseries",
      "title": "Disk Usage",
      "gridPos": { "h": 8, "w": 12, "x": 0, "y": 8 },
      "targets": [
        {
          "expr": "(1 - (node_filesystem_avail_bytes{fstype!=\"tmpfs\"} / node_filesystem_size_bytes{fstype!=\"tmpfs\"})) * 100",
          "legendFormat": "{{instance}}:{{mountpoint}}"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "unit": "percent",
          "max": 100,
          "min": 0
        }
      }
    },
    {
      "type": "timeseries",
      "title": "Network Traffic",
      "gridPos": { "h": 8, "w": 12, "x": 12, "y": 8 },
      "targets": [
        {
          "expr": "rate(node_network_receive_bytes_total[5m])",
          "legendFormat": "{{instance}}:rx"
        },
        {
          "expr": "rate(node_network_transmit_bytes_total[5m])",
          "legendFormat": "{{instance}}:tx"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "unit": "Bps"
        }
      }
    }
  ]
}
```

### Business Metrics Dashboard

```json
{
  "title": "Business Metrics",
  "panels": [
    {
      "type": "stat",
      "title": "Active Users",
      "gridPos": { "h": 4, "w": 4, "x": 0, "y": 0 },
      "targets": [
        {
          "expr": "sum(active_users)"
        }
      ]
    },
    {
      "type": "stat",
      "title": "Registrations Today",
      "gridPos": { "h": 4, "w": 4, "x": 4, "y": 0 },
      "targets": [
        {
          "expr": "increase(user_registrations_total[1d])"
        }
      ]
    },
    {
      "type": "stat",
      "title": "Revenue Today",
      "gridPos": { "h": 4, "w": 4, "x": 8, "y": 0 },
      "targets": [
        {
          "expr": "sum(increase(order_total_usd[1d]))"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "unit": "currencyUSD"
        }
      }
    },
    {
      "type": "timeseries",
      "title": "User Registrations",
      "gridPos": { "h": 8, "w": 12, "x": 0, "y": 4 },
      "targets": [
        {
          "expr": "sum by (plan) (rate(user_registrations_total[5m]))",
          "legendFormat": "{{plan}}"
        }
      ]
    },
    {
      "type": "timeseries",
      "title": "Order Value Distribution",
      "gridPos": { "h": 8, "w": 12, "x": 12, "y": 4 },
      "targets": [
        {
          "expr": "histogram_quantile(0.5, sum(rate(order_value_usd_bucket[1h])))",
          "legendFormat": "P50"
        },
        {
          "expr": "histogram_quantile(0.95, sum(rate(order_value_usd_bucket[1h])))",
          "legendFormat": "P95"
        },
        {
          "expr": "histogram_quantile(0.99, sum(rate(order_value_usd_bucket[1h])))",
          "legendFormat": "P99"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "unit": "currencyUSD"
        }
      }
    }
  ]
}
```

---

## Dashboard as Code

### Terraform Provider

```hcl
# terraform/grafana.tf
terraform {
  required_providers {
    grafana = {
      source  = "grafana/grafana"
      version = "~> 1.0"
    }
  }
}

provider "grafana" {
  url  = "http://grafana:3000"
  auth = "admin:admin"
}

resource "grafana_data_source" "prometheus" {
  name = "Prometheus"
  type = "prometheus"
  url  = "http://prometheus:9090"

  json_data_encoded = jsonencode({
    httpMethod = "POST"
    timeInterval = "15s"
  })
}

resource "grafana_dashboard" "application" {
  config_json = file("${path.module}/dashboards/application.json")
}
```

### Dashboard JSON Template

```json
{
  "dashboard": {
    "title": "Application Metrics",
    "uid": "application-metrics",
    "tags": ["application"],
    "timezone": "browser",
    "schemaVersion": 27,
    "version": 1,
    "refresh": "30s",
    "panels": [
      {
        "type": "timeseries",
        "title": "Request Rate",
        "gridPos": { "h": 8, "w": 12, "x": 0, "y": 0 },
        "targets": [
          {
            "expr": "sum(rate(http_requests_total[5m]))"
          }
        ]
      }
    ]
  }
}
```

---

## Best Practices

### 1. Use Descriptive Titles

```json
{
  "title": "HTTP Request Rate (req/s)"
}
```

### 2. Set Appropriate Time Ranges

```json
{
  "time": {
    "from": "now-1h",
    "to": "now"
  }
}
```

### 3. Use Thresholds

```json
{
  "fieldConfig": {
    "defaults": {
      "thresholds": {
        "steps": [
          { "color": "green", "value": null },
          { "color": "yellow", "value": 0.01 },
          { "color": "red", "value": 0.05 }
        ]
      }
    }
  }
}
```

### 4. Use Variables for Flexibility

```json
{
  "variables": [
    {
      "name": "job",
      "type": "query",
      "query": "label_values(up, job)"
    }
  ]
}
```

### 5. Organize Panels Logically

```json
{
  "panels": [
    { "title": "Overview", "gridPos": { "y": 0 } },
    { "title": "Details", "gridPos": { "y": 4 } }
  ]
}
```

---

## Summary

This skill covers comprehensive Grafana dashboard creation including:

- **Grafana Setup**: Docker installation and provisioning
- **Data Sources**: Prometheus, Loki, Elasticsearch
- **Dashboard Design Principles**: Layout, structure, color schemes
- **Panel Types**: Time series, stat, gauge, table, logs
- **Variables and Templating**: Query, interval, custom variables
- **Alerts**: Panel alerts and notification channels
- **Common Dashboard Patterns**: Application, system, business metrics
- **Dashboard as Code**: Terraform provider and JSON templates
- **Best Practices**: Titles, time ranges, thresholds, variables, organization
