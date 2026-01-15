# ELK Stack

A comprehensive guide to the ELK (Elasticsearch, Logstash, Kibana) stack for log management and analytics.

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

### Components

```
┌─────────────┐    Logs    ┌─────────────┐    Processed    ┌─────────────┐
│ Applications│────────────>│  Logstash   │────────────────>│Elasticsearch│
│             │             │  (Optional) │                 │             │
└─────────────┘             └─────────────┘                 └──────┬──────┘
                                                                  │
                                                                  │ Query
                                                                  ▼
                                                           ┌─────────────┐
                                                           │   Kibana    │
                                                           │  Dashboard  │
                                                           └─────────────┘
```

### Component Responsibilities

| Component | Purpose | Key Features |
|-----------|---------|--------------|
| Elasticsearch | Search and analytics engine | Distributed, RESTful, JSON |
| Logstash | Data processing pipeline | Input/Filter/Output plugins |
| Kibana | Visualization platform | Dashboards, Discover, Canvas |
| Filebeat | Log shipper | Lightweight, reliable |
| Beats | Data shippers | Metricbeat, Packetbeat, etc. |

---

## Elasticsearch Setup

### Docker Compose

```yaml
version: '3.8'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    container_name: elasticsearch
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms1g -Xmx1g"
    ports:
      - "9200:9200"
      - "9300:9300"
    volumes:
      - elasticsearch-data:/usr/share/elasticsearch/data
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
  elasticsearch-data:

networks:
  elk:
    driver: bridge
```

### Kubernetes Deployment

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: elasticsearch-config
  namespace: logging
data:
  elasticsearch.yml: |
    cluster.name: "k8s-logs"
    network.host: 0.0.0.0
    discovery.type: single-node
    xpack.security.enabled: false

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: elasticsearch
  namespace: logging
spec:
  replicas: 1
  selector:
    matchLabels:
      app: elasticsearch
  template:
    metadata:
      labels:
        app: elasticsearch
    spec:
      containers:
      - name: elasticsearch
        image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
        ports:
        - containerPort: 9200
        env:
        - name: discovery.type
          value: single-node
        - name: ES_JAVA_OPTS
          value: "-Xms1g -Xmx1g"
        volumeMounts:
        - name: data
          mountPath: /usr/share/elasticsearch/data
      volumes:
      - name: data
        emptyDir: {}

---
apiVersion: v1
kind: Service
metadata:
  name: elasticsearch
  namespace: logging
spec:
  selector:
    app: elasticsearch
  ports:
  - port: 9200
    targetPort: 9200
```

### Basic Configuration

```yaml
# elasticsearch.yml
cluster.name: production-cluster
node.name: node-1
network.host: 0.0.0.0
http.port: 9200
discovery.seed_hosts: ["node-1", "node-2"]
cluster.initial_master_nodes: ["node-1", "node-2"]

# Index settings
index.number_of_shards: 3
index.number_of_replicas: 1

# Security
xpack.security.enabled: true
xpack.security.transport.ssl.enabled: true
```

---

## Logstash Pipelines

### Basic Pipeline

```conf
# pipeline.conf
input {
  beats {
    port => 5044
  }
}

filter {
  # Parse JSON logs
  json {
    source => "message"
  }

  # Add timestamp
  date {
    match => ["timestamp", "ISO8601"]
  }

  # Add environment tag
  mutate {
    add_field => { "environment" => "production" }
  }
}

output {
  elasticsearch {
    hosts => ["http://elasticsearch:9200"]
    index => "logs-%{+YYYY.MM.dd}"
  }
}
```

### Multi-Pipeline Setup

```conf
# pipelines.yml
- pipeline.id: main
  path.config: "/usr/share/logstash/pipeline/main.conf"

- pipeline.id: nginx
  path.config: "/usr/share/logstash/pipeline/nginx.conf"

- pipeline.id: application
  path.config: "/usr/share/logstash/pipeline/application.conf"
```

### Nginx Log Pipeline

```conf
# nginx.conf
input {
  file {
    path => "/var/log/nginx/access.log"
    start_position => "beginning"
    type => "nginx-access"
  }
}

filter {
  if [type] == "nginx-access" {
    grok {
      match => {
        "message" => '%{IPORHOST:remote_addr} - %{DATA:remote_user} \[%{HTTPDATE:time_local}\] "%{WORD:method} %{DATA:request} HTTP/%{NUMBER:http_version}" %{NUMBER:status} %{NUMBER:body_bytes_sent} "%{DATA:http_referer}" "%{DATA:http_user_agent}"'
      }
    }

    geoip {
      source => "remote_addr"
      target => "geoip"
    }

    useragent {
      source => "http_user_agent"
      target => "ua"
    }
  }
}

output {
  elasticsearch {
    hosts => ["http://elasticsearch:9200"]
    index => "nginx-access-%{+YYYY.MM.dd}"
  }
}
```

### Application Log Pipeline

```conf
# application.conf
input {
  tcp {
    port => 5000
    codec => json_lines
  }
}

filter {
  # Add application name
  mutate {
    add_field => { "application" => "api-server" }
  }

  # Parse error stack traces
  if [level] == "error" {
    multiline {
      pattern => "^\\s"
      what => "previous"
    }
  }

  # Remove sensitive data
  mutate {
    remove_field => ["password", "token", "secret"]
  }
}

output {
  elasticsearch {
    hosts => ["http://elasticsearch:9200"]
    index => "application-%{application}-%{+YYYY.MM.dd}"
  }
}
```

---

## Kibana Configuration

### Basic Configuration

```yaml
# kibana.yml
server.name: kibana
server.host: "0.0.0.0"
server.port: 5601

elasticsearch.hosts: ["http://elasticsearch:9200"]

# Security
xpack.security.enabled: true
xpack.encryptedSavedObjects.encryptionKey: "something_at_least_32_characters"

# Logging
logging.dest: stdout
logging.verbose: false
```

### Index Pattern Creation

```json
POST /api/saved_objects/index-pattern/logs-*
{
  "attributes": {
    "title": "logs-*",
    "timeFieldName": "@timestamp",
    "fields": "[{\"name\":\"@timestamp\",\"type\":\"date\",\"searchable\":true,\"aggregatable\":true},{\"name\":\"level\",\"type\":\"string\",\"searchable\":true,\"aggregatable\":true},{\"name\":\"message\",\"type\":\"text\",\"searchable\":true,\"aggregatable\":false}]"
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
      - /var/log/*.log
    fields:
      app: myapp
      environment: production
    fields_under_root: true

  - type: log
    enabled: true
    paths:
      - /var/log/nginx/*.log
    fields:
      app: nginx
    fields_under_root: true

output.logstash:
  hosts: ["logstash:5044"]

# Or direct to Elasticsearch
# output.elasticsearch:
#   hosts: ["elasticsearch:9200"]
#   index: "filebeat-%{[agent.version]}-%{+yyyy.MM.dd}"

processors:
  - add_host_metadata:
      when.not.contains.tags: forwarded
  - add_cloud_metadata: ~
  - add_docker_metadata: ~
  - add_kubernetes_metadata: ~
```

### Kubernetes Log Shipping

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: filebeat-config
  namespace: logging
data:
  filebeat.yml: |-
    filebeat.inputs:
    - type: container
      paths:
        - /var/log/containers/*.log
      processors:
        - add_kubernetes_metadata:
            host: ${NODE_NAME}
            matchers:
            - logs_path:
                logs_path: "/var/log/containers/"

    output.elasticsearch:
      hosts: ["elasticsearch:9200"]
      indices:
        - index: "kubernetes-%{[kubernetes.namespace]}-%{+yyyy.MM.dd}"

    setup.kibana:
      host: "kibana:5601"

---
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: filebeat
  namespace: logging
spec:
  selector:
    matchLabels:
      app: filebeat
  template:
    metadata:
      labels:
        app: filebeat
    spec:
      serviceAccountName: filebeat
      containers:
      - name: filebeat
        image: docker.elastic.co/beats/filebeat:8.11.0
        args:
        - "-c"
        - "/etc/filebeat.yml"
        - "-e"
        volumeMounts:
        - name: config
          mountPath: /etc/filebeat.yml
          subPath: filebeat.yml
        - name: varlog
          mountPath: /var/log
          readOnly: true
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
      volumes:
      - name: config
        configMap:
          name: filebeat-config
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers
```

### Application Log Shipping (Node.js)

```typescript
import winston from 'winston';
import { ElasticsearchTransport } from 'winston-elasticsearch';

const esTransport = new ElasticsearchTransport({
  level: 'info',
  clientOpts: {
    node: 'http://elasticsearch:9200',
  },
  index: 'application-logs',
});

const logger = winston.createLogger({
  transports: [
    new winston.transports.Console(),
    esTransport,
  ],
});

// Usage
logger.info('User logged in', {
  userId: '123',
  ip: '192.168.1.1',
  userAgent: 'Mozilla/5.0...',
});
```

### Application Log Shipping (Python)

```python
import logging
from logstash_async.handler import AsynchronousLogstashHandler

logger = logging.getLogger('myapp')
logger.setLevel(logging.INFO)

logstash_handler = AsynchronousLogstashHandler(
    host='logstash',
    port=5959,
    database_path=None,
    transport='logstash_async.transport.TcpTransport'
)

logger.addHandler(logstash_handler)

# Usage
logger.info('User logged in', extra={
    'user_id': '123',
    'ip': '192.168.1.1',
    'user_agent': 'Mozilla/5.0...'
})
```

---

## Index Patterns

### Creating Index Patterns via API

```bash
# Create index pattern
curl -X POST "localhost:5601/api/saved_objects/index-pattern/logs-*" \
  -H 'kbn-xsrf: true' \
  -H 'Content-Type: application/json' \
  -d '{
    "attributes": {
      "title": "logs-*",
      "timeFieldName": "@timestamp"
    }
  }'

# Get index patterns
curl -X GET "localhost:5601/api/saved_objects/_find?type=index-pattern"
```

### Index Lifecycle Management

```json
PUT _ilm/policy/logs_policy
{
  "policy": {
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
          "force_merge": {
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
}
```

---

## Queries and Filters

### Basic Queries

```json
// Match all
GET logs-*/_search
{
  "query": {
    "match_all": {}
  }
}

// Match text
GET logs-*/_search
{
  "query": {
    "match": {
      "message": "error"
    }
  }
}

// Term query
GET logs-*/_search
{
  "query": {
    "term": {
      "level": "error"
    }
  }
}

// Range query
GET logs-*/_search
{
  "query": {
    "range": {
      "@timestamp": {
        "gte": "now-1h",
        "lte": "now"
      }
    }
  }
}
```

### Boolean Queries

```json
// AND query
GET logs-*/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "level": "error" } },
        { "match": { "service": "api" } }
      ]
    }
  }
}

// OR query
GET logs-*/_search
{
  "query": {
    "bool": {
      "should": [
        { "match": { "level": "error" } },
        { "match": { "level": "warning" } }
      ]
    }
  }
}

// NOT query
GET logs-*/_search
{
  "query": {
    "bool": {
      "must_not": [
        { "match": { "level": "debug" } }
      ]
    }
  }
}
```

### Aggregations

```json
// Terms aggregation
GET logs-*/_search
{
  "size": 0,
  "aggs": {
    "by_level": {
      "terms": {
        "field": "level"
      }
    }
  }
}

// Date histogram
GET logs-*/_search
{
  "size": 0,
  "aggs": {
    "over_time": {
      "date_histogram": {
        "field": "@timestamp",
        "interval": "1h"
      }
    }
  }
}

// Stats aggregation
GET logs-*/_search
{
  "size": 0,
  "aggs": {
    "response_time_stats": {
      "stats": {
        "field": "response_time"
      }
    }
  }
}
```

---

## Visualizations

### Line Chart

```json
POST /api/saved_objects/visualization
{
  "attributes": {
    "title": "Request Rate Over Time",
    "visState": "{\"title\":\"Request Rate Over Time\",\"type\":\"line\",\"params\":{\"grid\":{\"categoryLines\":false,\"style\":{\"color\":\"#eee\"}},\"categoryAxes\":[{\"id\":\"CategoryAxis-1\",\"type\":\"category\",\"position\":\"bottom\",\"show\":true,\"style\":{},\"scale\":{\"type\":\"linear\"},\"labels\":{\"show\":true,\"truncate\":100},\"title\":{}}],\"valueAxes\":[{\"id\":\"ValueAxis-1\",\"name\":\"LeftAxis-1\",\"type\":\"value\",\"position\":\"left\",\"show\":true,\"style\":{},\"scale\":{\"type\":\"linear\",\"mode\":\"normal\"},\"labels\":{\"show\":true,\"rotate\":0,\"filter\":false,\"truncate\":100},\"title\":{\"text\":\"Count\"}}],\"seriesParams\":[{\"show\":\"true\",\"type\":\"line\",\"mode\":\"normal\",\"data\":{\"label\":\"Count\",\"id\":\"1\"},\"valueAxis\":\"ValueAxis-1\",\"drawLinesBetweenPoints\":true,\"showCircles\":true,\"interpolate\":\"linear\",\"radius\":2,\"lines\":{\"show\":true,\"fill\":0.5,\"width\":2,\"smooth\":false},\"circles\":{\"show\":true,\"radius\":2}}],\"addTooltip\":true,\"addLegend\":true,\"legendPosition\":\"right\",\"times\":[],\"addTimeMarker\":false},\"aggs\":[{\"id\":\"1\",\"enabled\":true,\"type\":\"count\",\"schema\":\"metric\",\"params\":{}},{\"id\":\"2\",\"enabled\":true,\"type\":\"date_histogram\",\"schema\":\"segment\",\"params\":{\"field\":\"@timestamp\",\"interval\":\"auto\",\"customInterval\":\"2h\",\"min_doc_count\":1,\"extended_bounds\":{}}}]}"
  }
}
```

### Pie Chart

```json
POST /api/saved_objects/visualization
{
  "attributes": {
    "title": "Logs by Level",
    "visState": "{\"title\":\"Logs by Level\",\"type\":\"pie\",\"params\":{\"addTooltip\":true,\"addLegend\":true,\"legendPosition\":\"right\",\"isDonut\":false,\"labels\":{\"show\":false,\"values\":true,\"last_level\":true,\"truncate\":100}},\"aggs\":[{\"id\":\"1\",\"enabled\":true,\"type\":\"count\",\"schema\":\"metric\",\"params\":{}},{\"id\":\"2\",\"enabled\":true,\"type\":\"terms\",\"schema\":\"segment\",\"params\":{\"field\":\"level\",\"size\":10,\"order\":\"desc\",\"orderBy\":\"1\"}}]}"
  }
}
```

### Data Table

```json
POST /api/saved_objects/visualization
{
  "attributes": {
    "title": "Top 10 Error Messages",
    "visState": "{\"title\":\"Top 10 Error Messages\",\"type\":\"table\",\"params\":{\"perPage\":10,\"showPartialRows\":false,\"showMetricsAtAllLevels\":false,\"sort\":{\"columnIndex\":null,\"direction\":null},\"showTotal\":false,\"totalFunc\":\"sum\"},\"aggs\":[{\"id\":\"1\",\"enabled\":true,\"type\":\"count\",\"schema\":\"metric\",\"params\":{}},{\"id\":\"2\",\"enabled\":true,\"type\":\"terms\",\"schema\":\"bucket\",\"params\":{\"field\":\"message\",\"size\":10,\"order\":\"desc\",\"orderBy\":\"1\"}}]}"
  }
}
```

---

## Dashboards

### Creating Dashboard via API

```bash
# Create dashboard
curl -X POST "localhost:5601/api/saved_objects/dashboard" \
  -H 'kbn-xsrf: true' \
  -H 'Content-Type: application/json' \
  -d '{
    "attributes": {
      "title": "Application Logs Dashboard",
      "panelsJSON": "[{\"gridData\":{\"x\":0,\"y\":0,\"w\":24,\"h\":15},\"panelIndex\":\"1\",\"embeddableConfig\":{\"enhancements\":{}},\"panelRefName\":\"panel_0\",\"version\":\"8.11.0\",\"type\":\"visualization\",\"state\":{\"type\":\"visualization\",\"filters\":[]}}]",
      "optionsJSON": "{\"useMargins\":true,\"syncColors\":false,\"syncCursor\":true,\"syncTooltips\":false}",
      "version": "8.11.0"
    }
  }'
```

### Dashboard Export/Import

```bash
# Export dashboard
curl -X GET "localhost:5601/api/saved_objects/_export" \
  -H 'kbn-xsrf: true' \
  -H 'Content-Type: application/json' \
  -d '{
    "type": ["dashboard"],
    "exportType": "export"
  }' > dashboard-export.ndjson

# Import dashboard
curl -X POST "localhost:5601/api/saved_objects/_import" \
  -H 'kbn-xsrf: true' \
  --form file=@dashboard-export.ndjson
```

---

## Alerts

### Creating Alert via API

```json
POST /api/alerting/rule
{
  "name": "High Error Rate",
  "consumer": "alerts",
  "enabled": true,
  "rule_type_id": ".es-query",
  "schedule": {
    "interval": "1m"
  },
  "actions": [],
  "params": {
    "size": 100,
    "timeWindowSize": 1,
    "timeWindowUnit": "m",
    "thresholdComparator": "gt",
    "threshold": [10],
    "index": ["logs-*"],
    "timeField": "@timestamp",
    "esQuery": "{\"query\":{\"bool\":{\"must\":[{\"match\":{\"level\":\"error\"}}]}}}"
  },
  "throttle": "1m"
}
```

### Kibana Alerting

```yaml
# Kibana Watcher (deprecated, use Alerting instead)
PUT _watcher/watch/error_rate_watch
{
  "trigger": {
    "schedule": {
      "interval": "1m"
    }
  },
  "input": {
    "search": {
      "request": {
        "indices": ["logs-*"],
        "body": {
          "query": {
            "bool": {
              "must": [
                { "match": { "level": "error" } }
              ]
            }
          }
        }
      }
    }
  },
  "condition": {
    "compare": {
      "ctx.payload.hits.total": {
        "gt": 10
      }
    }
  },
  "actions": {
    "email_admin": {
      "email": {
        "to": "admin@example.com",
        "subject": "High Error Rate Detected",
        "body": "Found {{ctx.payload.hits.total}} error logs in the last minute."
      }
    }
  }
}
```

---

## Production Setup

### High Availability Setup

```yaml
# elasticsearch-cluster.yml
version: '3.8'
services:
  elasticsearch1:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    container_name: elasticsearch1
    environment:
      - cluster.name=production-cluster
      - node.name=elasticsearch1
      - discovery.seed_hosts=elasticsearch2,elasticsearch3
      - cluster.initial_master_nodes=elasticsearch1,elasticsearch2,elasticsearch3
      - "ES_JAVA_OPTS=-Xms2g -Xmx2g"
    ports:
      - "9200:9200"
    volumes:
      - es1-data:/usr/share/elasticsearch/data
    networks:
      - elk

  elasticsearch2:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    container_name: elasticsearch2
    environment:
      - cluster.name=production-cluster
      - node.name=elasticsearch2
      - discovery.seed_hosts=elasticsearch1,elasticsearch3
      - cluster.initial_master_nodes=elasticsearch1,elasticsearch2,elasticsearch3
      - "ES_JAVA_OPTS=-Xms2g -Xmx2g"
    ports:
      - "9201:9200"
    volumes:
      - es2-data:/usr/share/elasticsearch/data
    networks:
      - elk

  elasticsearch3:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    container_name: elasticsearch3
    environment:
      - cluster.name=production-cluster
      - node.name=elasticsearch3
      - discovery.seed_hosts=elasticsearch1,elasticsearch2
      - cluster.initial_master_nodes=elasticsearch1,elasticsearch2,elasticsearch3
      - "ES_JAVA_OPTS=-Xms2g -Xmx2g"
    ports:
      - "9202:9200"
    volumes:
      - es3-data:/usr/share/elasticsearch/data
    networks:
      - elk

volumes:
  es1-data:
  es2-data:
  es3-data:

networks:
  elk:
    driver: bridge
```

### Security Configuration

```yaml
# Enable security
xpack.security.enabled: true
xpack.security.transport.ssl.enabled: true
xpack.security.transport.ssl.verification_mode: certificate
xpack.security.transport.ssl.keystore.path: elastic-certificates.p12
xpack.security.transport.ssl.truststore.path: elastic-certificates.p12
xpack.security.http.ssl.enabled: true
xpack.security.http.ssl.keystore.path: elastic-certificates.p12
```

---

## Performance Tuning

### Heap Size Configuration

```bash
# Set heap size to 50% of available RAM, max 31GB
ES_JAVA_OPTS="-Xms16g -Xmx16g"
```

### Index Settings

```json
PUT /logs-*/_settings
{
  "index": {
    "refresh_interval": "30s",
    "number_of_replicas": "1",
    "translog.durability": "async"
  }
}
```

### Query Optimization

```json
// Use filter instead of query for exact matches
GET logs-*/_search
{
  "query": {
    "bool": {
      "filter": [
        { "term": { "level": "error" } },
        { "range": { "@timestamp": { "gte": "now-1h" } } }
      ]
    }
  }
}
```

### Caching

```json
// Enable query cache
PUT /logs-*/_settings
{
  "index.queries.cache.enabled": true
}
```

---

## Resources

- [Elasticsearch Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [Logstash Documentation](https://www.elastic.co/guide/en/logstash/current/index.html)
- [Kibana Documentation](https://www.elastic.co/guide/en/kibana/current/index.html)
- [Filebeat Documentation](https://www.elastic.co/guide/en/beats/filebeat/current/index.html)
