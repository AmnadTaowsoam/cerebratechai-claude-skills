# ELK Stack

## Overview

The ELK Stack (Elasticsearch, Logstash, Kibana) is a powerful set of tools for searching, analyzing, and visualizing data in real-time. This skill covers ELK stack setup, configuration, and best practices.

## Table of Contents

1. [ELK Stack Overview](#elk-stack-overview)
2. [Elasticsearch Setup](#elasticsearch-setup)
3. [Logstash Pipelines](#logstash-pipelines)
4. [Kibana Configuration](#kibana-configuration)
5. [Log Shipping](#log-shipping)
6. [Index Patterns](#index-patterns)
7. [Queries and Filters](#queries-and-filters)
8. [Visualizations](#visualizations)
9. [Dashboards](#dashboards)
10. [Alerts](#alerts)
11. [Production Setup](#production-setup)
12. [Performance Tuning](#performance-tuning)

---

## ELK Stack Overview

### Architecture

```
┌─────────────┐
│   Sources   │
│  (Apps)     │
└──────┬──────┘
       │ Logs
       ↓
┌─────────────┐
│  Filebeat   │
│  (Ship)     │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│  Logstash   │
│  (Process)  │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│Elasticsearch│
│  (Store)    │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│   Kibana    │
│  (Visual)   │
└─────────────┘
```

### Components

| Component | Description |
|-----------|-------------|
| **Elasticsearch** | Distributed search and analytics engine |
| **Logstash** | Server-side data processing pipeline |
| **Kibana** | Visualization and exploration interface |
| **Beats** | Lightweight data shippers (Filebeat, Metricbeat, etc.) |

---

## Elasticsearch Setup

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    container_name: elasticsearch
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms1g -Xmx1g"
      - xpack.security.enabled=false
    ports:
      - "9200:9200"
      - "9300:9300"
    volumes:
      - es_data:/usr/share/elasticsearch/data
    networks:
      - elk

  logstash:
    image: docker.elastic.co/logstash/logstash:8.11.0
    container_name: logstash
    ports:
      - "5044:5044"
      - "5000:5000/tcp"
      - "5000:5000/udp"
      - "9600:9600"
    volumes:
      - ./logstash/pipeline:/usr/share/logstash/pipeline
    networks:
      - elk
    depends_on:
      - elasticsearch

  kibana:
    image: docker.elastic.co/kibana/kibana:8.11.0
    container_name: kibana
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    networks:
      - elk
    depends_on:
      - elasticsearch

volumes:
  es_data:

networks:
  elk:
    driver: bridge
```

### Index Template

```json
{
  "index_patterns": ["logs-*"],
  "template": {
    "settings": {
      "number_of_shards": 1,
      "number_of_replicas": 1,
      "index.lifecycle.name": "logs-policy",
      "index.lifecycle.rollover_alias": "logs"
    },
    "mappings": {
      "properties": {
        "@timestamp": {
          "type": "date"
        },
        "level": {
          "type": "keyword"
        },
        "message": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword"
            }
          }
        },
        "service": {
          "type": "keyword"
        },
        "environment": {
          "type": "keyword"
        },
        "host": {
          "type": "keyword"
        },
        "tags": {
          "type": "keyword"
        }
      }
    }
  }
}
```

### Index Lifecycle Policy

```json
{
  "policy": "logs-policy",
  "phases": {
    "hot": {
      "actions": {
        "rollover": {
          "max_size": "50GB",
          "max_age": "30d"
        }
      }
    },
    "warm": {
      "min_age": "30d",
      "actions": {
        "shrink": {
          "number_of_shards": 1
        },
        "forcemerge": {
          "max_num_segments": 1
        }
      }
    },
    "delete": {
      "min_age": "90d",
      "actions": {
        "delete": {}
      }
    }
  }
}
```

---

## Logstash Pipelines

### Basic Pipeline

```conf
# logstash/pipeline/logstash.conf
input {
  beats {
    port => 5044
  }
}

filter {
  # Parse JSON logs
  if [message] =~ /^\{.*\}$/ {
    json {
      source => "message"
    }
  }

  # Add timestamp
  date {
    match => ["timestamp", "ISO8601"]
  }

  # Add environment
  mutate {
    add_field => {
      "environment" => "${ENVIRONMENT:production}"
    }
  }

  # Add host info
  mutate {
    add_field => {
      "host" => "${HOSTNAME:unknown}"
    }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "logs-%{+YYYY.MM.dd}"
  }

  # Debug output
  stdout { codec => rubydebug }
}
```

### Advanced Pipeline

```conf
# logstash/pipeline/advanced.conf
input {
  beats {
    port => 5044
  }

  # HTTP input
  http {
    port => 8080
    codec => json
  }

  # TCP input
  tcp {
    port => 5000
    codec => json_lines
  }
}

filter {
  # Parse different log formats
  if [type] == "nginx" {
    grok {
      match => {
        "message" => '%{IPORHOST:remote_addr} - %{DATA:remote_user} \[%{HTTPDATE:time_local}\] "%{WORD:method} %{DATA:request} HTTP/%{NUMBER:http_version}" %{NUMBER:status} %{NUMBER:body_bytes_sent} "%{DATA:http_referer}" "%{DATA:http_user_agent}"'
      }
    }
  }

  if [type] == "application" {
    json {
      source => "message"
    }

    # Add application-specific fields
    mutate {
      add_field => {
        "service" => "api"
        "app_version" => "%{[version]}"
      }
    }
  }

  # Parse user agent
  if [http_user_agent] {
    useragent {
      source => "http_user_agent"
      target => "ua"
    }
  }

  # GeoIP lookup
  if [remote_addr] {
    geoip {
      source => "remote_addr"
      target => "geoip"
    }
  }

  # Drop debug logs in production
  if [level] == "debug" and [environment] == "production" {
    drop {}
  }

  # Add tags
  if [status] >= 400 {
    mutate {
      add_tag => ["error"]
    }
  }

  if [status] >= 500 {
    mutate {
      add_tag => ["server_error"]
    }
  }
}

output {
  # Elasticsearch output
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "logs-%{[service]}-%{+YYYY.MM.dd}"
    template => "/etc/logstash/templates/logstash-template.json"
    template_name => "logstash"
  }

  # Conditional output
  if "error" in [tags] {
    # Send errors to Slack
    http {
      url => "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
      http_method => "post"
      format => "json"
      mapping => {
        "text" => "%{message}"
      }
    }
  }
}
```

### Conditional Routing

```conf
# logstash/pipeline/routing.conf
input {
  beats {
    port => 5044
  }
}

filter {
  # Add service field based on path
  if [log][file][path] =~ /api/ {
    mutate {
      add_field => { "service" => "api" }
    }
  } else if [log][file][path] =~ /worker/ {
    mutate {
      add_field => { "service" => "worker" }
    }
  } else if [log][file][path] =~ /frontend/ {
    mutate {
      add_field => { "service" => "frontend" }
    }
  }
}

output {
  # Route to different indices
  if [service] == "api" {
    elasticsearch {
      hosts => ["elasticsearch:9200"]
      index => "logs-api-%{+YYYY.MM.dd}"
    }
  } else if [service] == "worker" {
    elasticsearch {
      hosts => ["elasticsearch:9200"]
      index => "logs-worker-%{+YYYY.MM.dd}"
    }
  } else if [service] == "frontend" {
    elasticsearch {
      hosts => ["elasticsearch:9200"]
      index => "logs-frontend-%{+YYYY.MM.dd}"
    }
  }
}
```

---

## Kibana Configuration

### kibana.yml

```yaml
# kibana.yml
server.name: kibana
server.host: "0.0.0.0"
server.port: 5601

elasticsearch.hosts: ["http://elasticsearch:9200"]

# Logging
logging.dest: stdout
logging.verbose: false

# Security (if enabled)
# elasticsearch.username: "kibana"
# elasticsearch.password: "changeme"

# Default app
kibana.defaultAppId: "discover"

# Timezone
i18n.locale: "en"
```

### Index Pattern

```json
{
  "attributes": {
    "title": "logs-*",
    "timeFieldName": "@timestamp",
    "fields": "[{\"name\":\"@timestamp\",\"type\":\"date\",\"searchable\":true,\"aggregatable\":true},{\"name\":\"level\",\"type\":\"keyword\",\"searchable\":true,\"aggregatable\":true},{\"name\":\"message\",\"type\":\"text\",\"searchable\":true,\"aggregatable\":false},{\"name\":\"service\",\"type\":\"keyword\",\"searchable\":true,\"aggregatable\":true}]"
  }
}
```

---

## Log Shipping

### Filebeat Configuration

```yaml
# filebeat.yml
filebeat.inputs:
  - type: log
    enabled: true
    paths:
      - /var/log/application/*.log
    fields:
      service: api
      environment: production
    fields_under_root: true
    multiline.pattern: '^\['
    multiline.negate: true
    multiline.match: after

  - type: log
    enabled: true
    paths:
      - /var/log/nginx/*.log
    fields:
      service: nginx
      environment: production
    fields_under_root: true

output.logstash:
  hosts: ["logstash:5044"]

# Processors
processors:
  - add_host_metadata: ~
  - add_cloud_metadata: ~
  - add_docker_metadata: ~
```

### Application Logs (Node.js)

```typescript
// logging.ts
import pino from 'pino';

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  formatters: {
    level: (label) => {
      return { level: label };
    },
  },
  timestamp: pino.stdTimeFunctions.isoTime,
});

// Usage
logger.info({ service: 'api', userId: '123' }, 'User logged in');
logger.error({ service: 'api', error: 'Database connection failed' }, 'Error occurred');
```

### Application Logs (Python)

```python
# logging.py
import logging
import json
from pythonjsonlogger import jsonlogger

# Configure JSON logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(
    '%(asctime)s %(name)s %(levelname)s %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Usage
logger.info({
    'service': 'api',
    'user_id': '123'
}, 'User logged in')

logger.error({
    'service': 'api',
    'error': 'Database connection failed'
}, 'Error occurred')
```

---

## Index Patterns

### Create Index Pattern

```bash
# Using API
curl -X POST "kibana:5601/api/saved_objects/index-pattern/logs-*" \
  -H 'kbn-xsrf: true' \
  -H 'Content-Type: application/json' \
  -d '{
    "attributes": {
      "title": "logs-*",
      "timeFieldName": "@timestamp"
    }
  }'
```

### Index Pattern with Fields

```json
{
  "attributes": {
    "title": "logs-*",
    "timeFieldName": "@timestamp",
    "fields": "[{\"name\":\"@timestamp\",\"type\":\"date\",\"searchable\":true,\"aggregatable\":true},{\"name\":\"level\",\"type\":\"keyword\",\"searchable\":true,\"aggregatable\":true},{\"name\":\"message\",\"type\":\"text\",\"searchable\":true,\"aggregatable\":false},{\"name\":\"service\",\"type\":\"keyword\",\"searchable\":true,\"aggregatable\":true},{\"name\":\"environment\",\"type\":\"keyword\",\"searchable\":true,\"aggregatable\":true},{\"name\":\"host\",\"type\":\"keyword\",\"searchable\":true,\"aggregatable\":true},{\"name\":\"tags\",\"type\":\"keyword\",\"searchable\":true,\"aggregatable\":true},{\"name\":\"status\",\"type\":\"keyword\",\"searchable\":true,\"aggregatable\":true},{\"name\":\"method\",\"type\":\"keyword\",\"searchable\":true,\"aggregatable\":true},{\"name\":\"path\",\"type\":\"keyword\",\"searchable\":true,\"aggregatable\":true}]"
  }
}
```

---

## Queries and Filters

### Query DSL

```json
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "message": "error"
          }
        }
      ],
      "filter": [
        {
          "range": {
            "@timestamp": {
              "gte": "now-1h"
            }
          }
        },
        {
          "term": {
            "level": "error"
          }
        }
      ]
    }
  }
}
```

### KQL (Kibana Query Language)

```
# Simple query
message: "error"

# Field query
level: "error"

# Range query
@timestamp: [now-1h TO now]

# Boolean query
level: "error" AND service: "api"

# Wildcard
message: "database*"

# Exists
_exists_: "userId"

# Nested
service: "api" AND (level: "error" OR level: "warning")
```

### Aggregations

```json
{
  "size": 0,
  "aggs": {
    "by_level": {
      "terms": {
        "field": "level",
        "size": 10
      }
    },
    "by_service": {
      "terms": {
        "field": "service",
        "size": 10
      }
    },
    "by_time": {
      "date_histogram": {
        "field": "@timestamp",
        "calendar_interval": "1h"
      }
    },
    "avg_response_time": {
      "avg": {
        "field": "response_time"
      }
    },
    "error_rate": {
      "filter": {
        "term": {
          "level": "error"
        }
      }
    }
  }
}
```

---

## Visualizations

### Line Chart

```json
{
  "type": "line",
  "title": "Request Rate Over Time",
  "params": {
    "grid": {
      "categoryLines": false,
      "style": {
        "color": "#eee"
      }
    },
    "legendPosition": "right",
    "seriesParams": [
      {
        "data": {
          "id": "1",
          "label": "Count"
        },
        "drawLinesBetweenPoints": true,
        "show": "true",
        "showPoints": "auto",
        "type": "line"
      }
    ],
    "timeRange": {
      "mode": "entire_time_range"
    },
    "valueAxes": [
      {
        "id": "ValueAxis-1",
        "name": "LeftAxis-1",
        "position": "left",
        "scale": {
          "type": "linear"
        },
        "style": {}
      }
    ]
  }
}
```

### Pie Chart

```json
{
  "type": "pie",
  "title": "Errors by Service",
  "params": {
    "addTooltip": true,
    "addLegend": true,
    "isDonut": false,
    "legendPosition": "right",
    "sliceLabels": {
      "show": false
    }
  }
}
```

### Bar Chart

```json
{
  "type": "bar",
  "title": "Top Error Messages",
  "params": {
    "addLegend": false,
    "addTooltip": true,
    "grid": {
      "categoryLines": false,
      "style": {
        "color": "#eee"
      }
    },
    "legendPosition": "right",
    "seriesParams": [
      {
        "data": {
          "id": "1",
          "label": "Count"
        },
        "drawLinesBetweenPoints": true,
        "show": "true",
        "showPoints": "auto",
        "type": "bar"
      }
    ],
    "valueAxes": [
      {
        "id": "ValueAxis-1",
        "name": "LeftAxis-1",
        "position": "left",
        "scale": {
          "type": "linear"
        },
        "style": {}
      }
    ]
  }
}
```

---

## Dashboards

### Dashboard JSON

```json
{
  "title": "Application Logs",
  "panelsJSON": "[{\"gridData\":{\"h\":6,\"i\":\"1\",\"w\":12,\"x\":0,\"y\":0},\"id\":\"1\",\"panelIndex\":\"1\",\"type\":\"metric\",\"version\":\"7.15.0\"},{\"gridData\":{\"h\":6,\"i\":\"2\",\"w\":12,\"x\":12,\"y\":0},\"id\":\"2\",\"panelIndex\":\"2\",\"type\":\"metric\",\"version\":\"7.15.0\"},{\"gridData\":{\"h\":12,\"i\":\"3\",\"w\":24,\"x\":0,\"y\":6},\"id\":\"3\",\"panelIndex\":\"3\",\"type\":\"line\",\"version\":\"7.15.0\"}]",
  "optionsJSON": "{\"darkTheme\":true,\"hidePanelTitles\":false,\"useMargins\":true}",
  "timeRestore": true,
  "timeTo": "now",
  "timeFrom": "now-1h"
}
```

---

## Alerts

### Alert Rule

```json
{
  "name": "High Error Rate",
  "type": "threshold",
  "throttle": "1m",
  "params": {
    "index": ["logs-*"],
    "timeField": "@timestamp",
    "timeWindowSize": 5,
    "timeWindowUnit": "m",
    "thresholdComparator": ">",
    "threshold": [100],
    "aggType": "count",
    "groupby": "service",
    "termSize": 10,
    "termField": "level.keyword",
    "termDirection": "desc",
    "filter": [
      {
        "query": {
          "query_string": {
            "query": "level: error"
          }
        }
      }
    ]
  },
  "actions": [
    {
      "id": "email-action",
      "type": "email",
      "email": ["alerts@example.com"]
    }
  ]
}
```

---

## Production Setup

### Security

```yaml
# elasticsearch.yml
xpack.security.enabled: true
xpack.security.transport.ssl.enabled: true
xpack.security.transport.ssl.verification_mode: certificate
xpack.security.transport.ssl.keystore.path: elastic-certificates.p12
xpack.security.transport.ssl.truststore.path: elastic-certificates.p12
xpack.security.http.ssl.enabled: true
xpack.security.http.ssl.keystore.path: elastic-certificates.p12
xpack.security.http.ssl.truststore.path: elastic-certificates.p12
```

### High Availability

```yaml
# docker-compose-ha.yml
version: '3.8'

services:
  elasticsearch1:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    container_name: elasticsearch1
    environment:
      - cluster.name=elasticsearch
      - node.name=elasticsearch1
      - discovery.seed_hosts=elasticsearch2,elasticsearch3
      - cluster.initial_master_nodes=elasticsearch1,elasticsearch2,elasticsearch3
      - "ES_JAVA_OPTS=-Xms2g -Xmx2g"
    ports:
      - "9200:9200"
    volumes:
      - es_data1:/usr/share/elasticsearch/data
    networks:
      - elk

  elasticsearch2:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    container_name: elasticsearch2
    environment:
      - cluster.name=elasticsearch
      - node.name=elasticsearch2
      - discovery.seed_hosts=elasticsearch1,elasticsearch3
      - cluster.initial_master_nodes=elasticsearch1,elasticsearch2,elasticsearch3
      - "ES_JAVA_OPTS=-Xms2g -Xmx2g"
    ports:
      - "9201:9200"
    volumes:
      - es_data2:/usr/share/elasticsearch/data
    networks:
      - elk

  elasticsearch3:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    container_name: elasticsearch3
    environment:
      - cluster.name=elasticsearch
      - node.name=elasticsearch3
      - discovery.seed_hosts=elasticsearch1,elasticsearch2
      - cluster.initial_master_nodes=elasticsearch1,elasticsearch2,elasticsearch3
      - "ES_JAVA_OPTS=-Xms2g -Xmx2g"
    ports:
      - "9202:9200"
    volumes:
      - es_data3:/usr/share/elasticsearch/data
    networks:
      - elk

volumes:
  es_data1:
  es_data2:
  es_data3:

networks:
  elk:
    driver: bridge
```

---

## Performance Tuning

### Elasticsearch Settings

```yaml
# elasticsearch.yml
# JVM Heap Size (should be 50% of available RAM, max 30GB)
"ES_JAVA_OPTS=-Xms8g -Xmx8g"

# Thread pool
thread_pool:
  write:
    queue_size: 1000

# Index settings
index:
  refresh_interval: "5s"
  translog:
    flush_threshold_size: "512mb"
    sync_interval: "5s"

# Cluster settings
cluster:
  routing:
    allocation:
      disk:
        watermark:
          low: "85%"
          high: "90%"
          flood_stage: "95%"
```

### Logstash Settings

```yaml
# logstash.yml
pipeline.workers: 4
pipeline.batch.size: 125
pipeline.batch.delay: 50
queue.type: persisted
queue.max_bytes: 1gb
```

---

## Summary

This skill covers comprehensive ELK stack implementation including:

- **ELK Stack Overview**: Architecture and components
- **Elasticsearch Setup**: Docker Compose, index templates, lifecycle policies
- **Logstash Pipelines**: Basic, advanced, and conditional routing
- **Kibana Configuration**: Settings and index patterns
- **Log Shipping**: Filebeat, Node.js, and Python logging
- **Index Patterns**: Creating and configuring index patterns
- **Queries and Filters**: Query DSL, KQL, and aggregations
- **Visualizations**: Line, pie, and bar charts
- **Dashboards**: Dashboard JSON configuration
- **Alerts**: Alert rule configuration
- **Production Setup**: Security and high availability
- **Performance Tuning**: Elasticsearch and Logstash settings
