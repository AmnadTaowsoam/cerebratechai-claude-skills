# Grafana Dashboards

A comprehensive guide to creating and managing Grafana dashboards for monitoring and visualization.

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

### Installation

```bash
# Docker
docker run -d -p 3000:3000 \
  -e GF_SECURITY_ADMIN_PASSWORD=admin \
  -v grafana-storage:/var/lib/grafana \
  grafana/grafana:latest

# Kubernetes
kubectl apply -f grafana-deployment.yaml
```

### Basic Configuration

```yaml
# grafana.ini
[server]
http_port = 3000
root_url = https://grafana.example.com

[security]
admin_user = admin
admin_password = admin

[auth.anonymous]
enabled = false

[users]
default_theme = dark
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
    "timeInterval": "15s"
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
        "name": "TraceID",
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
    "esVersion": "7.10.0",
    "maxConcurrentShardRequests": 5,
    "timeField": "@timestamp"
  }
}
```

### InfluxDB Data Source

```json
{
  "name": "InfluxDB",
  "type": "influxdb",
  "url": "http://influxdb:8086",
  "access": "proxy",
  "database": "telegraf",
  "jsonData": {
    "version": "InfluxQL",
    "httpMode": "POST"
  }
}
```

---

## Dashboard Design Principles

### 1. Purpose-Driven Design

Each dashboard should have a clear, single purpose:

| Dashboard Type | Purpose | Audience |
|----------------|---------|----------|
| Overview | High-level health check | Executives, Managers |
| Application | Application performance | Developers, SREs |
| Infrastructure | Resource utilization | DevOps, SREs |
| Business | KPIs and metrics | Business, Product |

### 2. Information Hierarchy

```
┌─────────────────────────────────────────────────────┐
│  Title: Production API Overview                      │
├─────────────────────────────────────────────────────┤
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐   │
│  │   Uptime    │ │   Errors    │ │   Latency   │   │
│  │   99.9%     │ │   0.01%     │ │    45ms     │   │
│  └─────────────┘ └─────────────┘ └─────────────┘   │
├─────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────┐   │
│  │         Request Rate (Top Level)             │   │
│  │  ┌───────────────────────────────────────┐  │   │
│  │  │  Time Series Graph                    │  │   │
│  │  │                                       │  │   │
│  │  └───────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────┐   │
│  │         Error Rate by Endpoint              │   │
│  │  ┌───────────────────────────────────────┐  │   │
│  │  │  Time Series Graph                    │  │   │
│  │  │                                       │  │   │
│  │  └───────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

### 3. Color Coding

- **Green**: Healthy/Normal
- **Yellow**: Warning/Degraded
- **Red**: Critical/Error
- **Blue**: Informational
- **Purple**: Secondary metrics

### 4. Time Range Selection

```json
{
  "time": {
    "from": "now-1h",
    "to": "now"
  },
  "timepicker": {
    "refresh_intervals": [
      "5s",
      "10s",
      "30s",
      "1m",
      "5m",
      "15m",
      "30m",
      "1h",
      "2h",
      "1d"
    ],
    "time_options": [
      "5m",
      "15m",
      "1h",
      "6h",
      "12h",
      "24h",
      "2d",
      "7d",
      "30d"
    ]
  }
}
```

---

## Panel Types

### Time Series Panel

```json
{
  "type": "timeseries",
  "title": "Request Rate",
  "gridPos": {
    "h": 8,
    "w": 12,
    "x": 0,
    "y": 0
  },
  "targets": [
    {
      "expr": "sum(rate(http_requests_total[5m])) by (route)",
      "legendFormat": "{{route}}",
      "refId": "A"
    }
  ],
  "fieldConfig": {
    "defaults": {
      "color": {
        "mode": "palette-classic"
      },
      "custom": {
        "lineWidth": 2,
        "fillOpacity": 10
      }
    }
  }
}
```

### Stat Panel

```json
{
  "type": "stat",
  "title": "Current Requests/sec",
  "gridPos": {
    "h": 4,
    "w": 4,
    "x": 0,
    "y": 0
  },
  "targets": [
    {
      "expr": "sum(rate(http_requests_total[1m]))",
      "refId": "A"
    }
  ],
  "fieldConfig": {
    "defaults": {
      "color": {
        "mode": "thresholds"
      },
      "mappings": [],
      "thresholds": {
        "steps": [
          {
            "color": "green",
            "value": null
          },
          {
            "color": "yellow",
            "value": 1000
          },
          {
            "color": "red",
            "value": 5000
          }
        ]
      },
      "unit": "reqps"
    }
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

### Table Panel

```json
{
  "type": "table",
  "title": "Top 10 Slow Endpoints",
  "gridPos": {
    "h": 8,
    "w": 12,
    "x": 12,
    "y": 0
  },
  "targets": [
    {
      "expr": "topk(10, histogram_quantile(0.95, sum by (le, route) (rate(http_request_duration_seconds_bucket[5m]))))",
      "format": "table",
      "instant": true,
      "refId": "A"
    }
  ],
  "transformations": [
    {
      "id": "organize",
      "options": {
        "excludeByName": {
          "Time": true
        },
        "renameByName": {
          "Value": "95th Percentile",
          "route": "Endpoint"
        }
      }
    }
  ],
  "fieldConfig": {
    "defaults": {
      "custom": {
        "align": "left",
        "width": 200
      }
    }
  }
}
```

### Logs Panel

```json
{
  "type": "logs",
  "title": "Application Logs",
  "gridPos": {
    "h": 8,
    "w": 12,
    "x": 0,
    "y": 8
  },
  "targets": [
    {
      "expr": "{app=\"api\",level=\"error\"}",
      "refId": "A"
    }
  ],
  "options": {
    "showLabels": true,
    "showTime": true,
    "wrapLogMessage": false,
    "sortOrder": "Descending",
    "dedupStrategy": "none"
  }
}
```

### Gauge Panel

```json
{
  "type": "gauge",
  "title": "CPU Usage",
  "gridPos": {
    "h": 6,
    "w": 6,
    "x": 0,
    "y": 0
  },
  "targets": [
    {
      "expr": "100 - (avg by (instance) (irate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)",
      "refId": "A"
    }
  ],
  "fieldConfig": {
    "defaults": {
      "unit": "percent",
      "min": 0,
      "max": 100,
      "thresholds": {
        "steps": [
          {
            "color": "green",
            "value": null
          },
          {
            "color": "yellow",
            "value": 70
          },
          {
            "color": "red",
            "value": 90
          }
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

### Pie Chart Panel

```json
{
  "type": "piechart",
  "title": "Requests by Status Code",
  "gridPos": {
    "h": 8,
    "w": 6,
    "x": 6,
    "y": 0
  },
  "targets": [
    {
      "expr": "sum by (status_code) (http_requests_total)",
      "refId": "A"
    }
  ],
  "options": {
    "legend": {
      "displayMode": "table",
      "placement": "right"
    },
    "pieType": "pie",
    "tooltip": {
      "mode": "single"
    }
  }
}
```

---

## Variables and Templating

### Query Variable

```json
{
  "name": "instance",
  "type": "query",
  "datasource": "Prometheus",
  "refresh": 1,
  "query": "label_values(up, instance)",
  "sort": 1,
  "multi": true,
  "includeAll": true,
  "allValue": ".*"
}
```

### Custom Variable

```json
{
  "name": "environment",
  "type": "custom",
  "query": "production,staging,development",
  "multi": false,
  "options": [
    {
      "value": "production",
      "text": "Production",
      "selected": true
    },
    {
      "value": "staging",
      "text": "Staging"
    },
    {
      "value": "development",
      "text": "Development"
    }
  ]
}
```

### Interval Variable

```json
{
  "name": "interval",
  "type": "interval",
  "query": "1m,5m,10m,30m,1h,6h,12h,1d",
  "auto": false,
  "auto_count": 30,
  "auto_min": "10s"
}
```

### Using Variables in Queries

```json
{
  "targets": [
    {
      "expr": "rate(http_requests_total{instance=~\"$instance\"}[$interval])",
      "legendFormat": "{{instance}}",
      "refId": "A"
    }
  ]
}
```

### Chained Variables

```json
[
  {
    "name": "region",
    "type": "query",
    "query": "label_values(up, region)"
  },
  {
    "name": "instance",
    "type": "query",
    "query": "label_values(up{region=\"$region\"}, instance)"
  }
]
```

---

## Alerts

### Alert Rule

```json
{
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
  "name": "High Error Rate Alert",
  "noDataState": "no_data",
  "notifications": []
}
```

### Alert Notification Channel

```json
{
  "name": "Slack",
  "type": "slack",
  "settings": {
    "url": "https://hooks.slack.com/services/XXX/YYY/ZZZ",
    "uploadImage": false
  },
  "secureSettings": {}
}
```

### Alert Query

```json
{
  "targets": [
    {
      "expr": "sum(rate(http_requests_total{status_code=~\"5..\"}[5m])) / sum(rate(http_requests_total[5m]))",
      "refId": "A",
      "hide": false
    }
  ],
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
    "name": "High Error Rate",
    "noDataState": "no_data",
    "notifications": []
  }
}
```

---

## Common Dashboard Patterns

### Application Metrics Dashboard

```json
{
  "dashboard": {
    "title": "Application Metrics",
    "panels": [
      {
        "title": "Request Rate",
        "type": "timeseries",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total[5m])) by (route)"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "timeseries",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{status_code=~\"5..\"}[5m])) by (route)"
          }
        ]
      },
      {
        "title": "P95 Latency",
        "type": "timeseries",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, sum by (le, route) (rate(http_request_duration_seconds_bucket[5m])))"
          }
        ]
      },
      {
        "title": "Active Connections",
        "type": "stat",
        "targets": [
          {
            "expr": "active_connections"
          }
        ]
      }
    ]
  }
}
```

### System Metrics Dashboard

```json
{
  "dashboard": {
    "title": "System Metrics",
    "panels": [
      {
        "title": "CPU Usage",
        "type": "timeseries",
        "targets": [
          {
            "expr": "100 - (avg by (instance) (irate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)"
          }
        ]
      },
      {
        "title": "Memory Usage",
        "type": "timeseries",
        "targets": [
          {
            "expr": "1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)"
          }
        ]
      },
      {
        "title": "Disk Usage",
        "type": "timeseries",
        "targets": [
          {
            "expr": "1 - (node_filesystem_avail_bytes{fstype!=\"tmpfs\"} / node_filesystem_size_bytes)"
          }
        ]
      },
      {
        "title": "Network Traffic",
        "type": "timeseries",
        "targets": [
          {
            "expr": "rate(node_network_receive_bytes_total[5m])",
            "legendFormat": "{{instance}} RX"
          },
          {
            "expr": "rate(node_network_transmit_bytes_total[5m])",
            "legendFormat": "{{instance}} TX"
          }
        ]
      }
    ]
  }
}
```

### Business Metrics Dashboard

```json
{
  "dashboard": {
    "title": "Business Metrics",
    "panels": [
      {
        "title": "Daily Active Users",
        "type": "stat",
        "targets": [
          {
            "expr": "count_over_time(active_users[1d])"
          }
        ]
      },
      {
        "title": "Revenue (Today)",
        "type": "stat",
        "targets": [
          {
            "expr": "increase(revenue_usd[1d])"
          }
        ]
      },
      {
        "title": "Conversion Rate",
        "type": "gauge",
        "targets": [
          {
            "expr": "increase(signups_total[1d]) / increase(visits_total[1d]) * 100"
          }
        ]
      },
      {
        "title": "Revenue Trend",
        "type": "timeseries",
        "targets": [
          {
            "expr": "increase(revenue_usd[1h])"
          }
        ]
      }
    ]
  }
}
```

---

## Dashboard as Code

### Terraform Provider

```hcl
resource "grafana_dashboard" "api_metrics" {
  config_json = file("${path.module}/dashboards/api-metrics.json")
  folder      = grafana_folder.production.id
}

resource "grafana_folder" "production" {
  title = "Production"
}

resource "grafana_data_source" "prometheus" {
  name                = "Prometheus"
  type                = "prometheus"
  url                 = "http://prometheus:9090"
  access_mode         = "proxy"
  is_default          = true
}
```

### Grafana Operator (Kubernetes)

```yaml
apiVersion: grafana.integreatly.org/v1beta1
kind: GrafanaDashboard
metadata:
  name: api-metrics
  namespace: monitoring
spec:
  instanceSelector:
    matchLabels:
      dashboards: "grafana"
  json: |
    {
      "title": "API Metrics",
      "panels": [...]
    }
```

### Ansible

```yaml
- name: Deploy Grafana dashboard
  community.grafana.grafana_dashboard:
    grafana_url: "http://grafana:3000"
    grafana_user: "admin"
    grafana_password: "admin"
    state: present
    dashboard_id: 1
    commit_message: "Updated via Ansible"
    overwrite: yes
    path: "dashboards/api-metrics.json"
```

---

## Best Practices

### 1. Use Consistent Naming

```
✅ Good:
- Production API Overview
- Development System Metrics
- Staging Business KPIs

❌ Bad:
- API
- Metrics
- Dashboard 1
```

### 2. Organize in Folders

```
├── Production/
│   ├── Application Metrics
│   ├── Infrastructure
│   └── Business KPIs
├── Staging/
│   └── Application Metrics
└── Development/
    └── Application Metrics
```

### 3. Use Descriptive Titles

```json
{
  "title": "API Response Time - P95 (Last 24h)",
  "description": "95th percentile response time for API endpoints"
}
```

### 4. Set Appropriate Time Ranges

```json
{
  "time": {
    "from": "now-6h",
    "to": "now"
  },
  "refresh": "30s"
}
```

### 5. Use Annotations

```json
{
  "annotations": {
    "list": [
      {
        "builtIn": 1,
        "datasource": "-- Grafana --",
        "enable": true,
        "hide": true,
        "iconColor": "rgba(0, 211, 255, 1)",
        "name": "Annotations & Alerts",
        "type": "dashboard"
      },
      {
        "datasource": "Prometheus",
        "enable": true,
        "expr": "changes(deployments_total[1h]) > 0",
        "name": "Deployments"
      }
    ]
  }
}
```

### 6. Limit Panel Count

- Overview dashboards: 6-12 panels
- Detailed dashboards: 12-20 panels
- Too many panels = cognitive overload

### 7. Use Thresholds

```json
{
  "thresholds": {
    "steps": [
      {
        "color": "green",
        "value": null
      },
      {
        "color": "yellow",
        "value": 70
      },
      {
        "color": "orange",
        "value": 85
      },
      {
        "color": "red",
        "value": 95
      }
    ]
  }
}
```

### 8. Document Your Dashboards

```json
{
  "description": "This dashboard monitors the production API server. It shows request rate, error rate, latency, and resource utilization. Alert thresholds: Error rate > 1%, P95 latency > 500ms, CPU > 80%",
  "tags": ["production", "api", "metrics"]
}
```

### 9. Use Row Repeating

```json
{
  "rows": [
    {
      "repeat": "instance",
      "repeatIteration": "1",
      "repeatPanelId": 2,
      "title": "$instance"
    }
  ]
}
```

### 10. Test Your Queries

```bash
# Test queries in Prometheus before adding to Grafana
curl 'http://prometheus:9090/api/v1/query?query=sum(rate(http_requests_total[5m]))'
```

---

## Resources

- [Grafana Documentation](https://grafana.com/docs/)
- [Grafana Panel Options](https://grafana.com/docs/grafana/latest/panels/)
- [PromQL Examples](https://prometheus.io/docs/prometheus/latest/querying/examples/)
- [Grafana Terraform Provider](https://registry.terraform.io/providers/grafana/grafana/latest/docs)
