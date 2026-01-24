---
name: Business Intelligence
description: Transforming raw data into actionable insights through reporting, analytics, and visualization using BI tools like Tableau, Looker, Power BI, and Metabase to support data-driven decision making.
---

# Business Intelligence

> **Current Level:** Intermediate  
> **Domain:** Business Analytics / Data Engineering

---

## Overview

Business Intelligence (BI) is the process of transforming raw data into actionable insights through reporting, analytics, and visualization to support data-driven decision making. Effective BI systems integrate data from multiple sources, transform it into a usable format, and present it through dashboards and reports.

## What is Business Intelligence

### Core Components

```
┌─────────────────────────────────────────────────────────────────┐
│                        Business Intelligence                      │
├─────────────────────────────────────────────────────────────────┤
│  Data Sources → ETL/ELT → Data Warehouse → BI Tools → Insights   │
│                                                                  │
│  • Databases    • Extract      • Centralized  • Tableau        │
│  • APIs         • Transform    • Storage      • Looker         │
│  • Files        • Load         • OLAP         • Power BI       │
│  • Spreadsheets • Schedule     • Star schema  • Metabase       │
└─────────────────────────────────────────────────────────────────┘
```

### BI Value Proposition

| Benefit | Description |
|---------|-------------|
| **Data-Driven Decisions** | Replace intuition with evidence |
| **Single Source of Truth** | Consistent metrics across organization |
| **Real-Time Monitoring** | Track performance as it happens |
| **Self-Service Analytics** | Empower non-technical users |
| **Competitive Advantage** | Identify trends and opportunities faster |

## BI Components

### 1. Data Sources

| Type | Examples | Characteristics |
|------|----------|-----------------|
| **Databases** | PostgreSQL, MySQL, MySQL, SQL Server | Structured data, real-time |
| **SaaS APIs** | Salesforce, Stripe, HubSpot | Third-party data |
| **Files** | CSV, Excel, JSON | Manual uploads, exports |
| **Web Analytics** | Google Analytics, Mixpanel | User behavior data |
| **Event Streams** | Kafka, Kinesis | Real-time events |

### 2. ETL/ELT (Extract, Transform, Load)

| Aspect | ETL (Extract-Transform-Load) | ELT (Extract-Load-Transform) |
|--------|------------------------------|------------------------------|
| **Process** | Extract → Transform → Load | Extract → Load → Transform |
| **Where** | Transform in staging area | Transform in warehouse |
| **Speed** | Slower (transform before load) | Faster (load raw, transform later) |
| **Use Case** | Legacy systems | Modern cloud warehouses |
| **Tools** | Informatica, Talend | Fivetran, Airbyte, dbt |

### 3. Data Warehouse

Centralized storage for structured and semi-structured data optimized for analytics.

| Warehouse | Strengths | Use Case |
|-----------|-----------|----------|
| **Snowflake** | Cloud-native, separation of compute/storage | Enterprise analytics |
| **BigQuery** | Serverless, integrates with GCP | Google ecosystem |
| **Redshift** | AWS integration, columnar storage | AWS ecosystem |
| **Databricks** | Lakehouse, ML integration | Data science + BI |
| **PostgreSQL** | Open-source, familiar | Small to medium teams |

### 4. BI Tools

| Tool | Strengths | Pricing |
|------|-----------|---------|
| **Tableau** | Powerful visualizations, enterprise | $$$ |
| **Looker** | SQL-based, embedded analytics | $$$ |
| **Power BI** | Microsoft ecosystem, affordable | $$ |
| **Metabase** | Open-source, simple | Free/$ |
| **Redash** | SQL-focused, lightweight | Free/$ |
| **Grafana** | Time-series, monitoring | Free |

### 5. Dashboards and Reports

- **Dashboards**: Interactive, real-time, visual
- **Reports**: Static, scheduled, detailed

## BI Architecture

### Traditional Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Sources   │────▶│   ETL Tool  │────▶│ Data Mart   │────▶│   Reports   │
│  (OLTP DB)  │     │             │     │  (OLAP)     │     │             │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

### Modern Data Stack

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Sources   │────▶│  Ingestion  │────▶│ Warehouse   │────▶│   BI Tool   │
│  (API/DB)   │     │ (Fivetran)  │     │ (Snowflake) │     │  (Looker)   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                          │                  │
                          ▼                  ▼
                     ┌─────────────┐     ┌─────────────┐
                     │  Scheduler  │     │   dbt       │
                     │  (Airflow)  │     │(Transform)  │
                     └─────────────┘     └─────────────┘
```

### Layered Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Presentation Layer                          │
│                   (Tableau, Looker, Power BI)                    │
├─────────────────────────────────────────────────────────────────┤
│                      Semantic Layer                              │
│                    (LookML, dbt models)                         │
├─────────────────────────────────────────────────────────────────┤
│                    Data Warehouse Layer                          │
│                  (Snowflake, BigQuery, Redshift)                 │
├─────────────────────────────────────────────────────────────────┤
│                      Ingestion Layer                             │
│                   (Fivetran, Airbyte, dbt)                      │
├─────────────────────────────────────────────────────────────────┤
│                       Source Layer                               │
│         (PostgreSQL, Salesforce, Stripe, Google Analytics)      │
└─────────────────────────────────────────────────────────────────┘
```

## Data Warehouse Concepts

### Star Schema

The most common data warehouse schema pattern.

```
                    ┌─────────────────┐
                    │   Fact Table    │
                    │   (orders)      │
                    │                 │
                    │  order_id       │
                    │  user_id        │◄─────┐
                    │  product_id     │◄──┐  │
                    │  date_id        │◄──┼──┼──┐
                    │  quantity       │   │  │  │
                    │  revenue        │   │  │  │
                    └─────────────────┘   │  │  │
                                          │  │  │
                         ┌────────────────┼──┼──┼────────────────┐
                         │                │  │  │                │
                    ┌────▼────┐     ┌─────▼──▼──▼────┐     ┌────▼────┐
                    │  users  │     │   products     │     │  dates  │
                    │ (dim)   │     │    (dim)       │     │  (dim)  │
                    │         │     │                │     │         │
                    │ user_id │     │ product_id     │     │ date_id │
                    │ name    │     │ name           │     │ date    │
                    │ email   │     │ category       │     │ month   │
                    │ segment │     │ price          │     │ quarter │
                    └─────────┘     └────────────────┘     └─────────┘
```

### Schema Comparison

| Aspect | Star Schema | Snowflake Schema |
|--------|-------------|-----------------|
| **Structure** | Fact + denormalized dimensions | Fact + normalized dimensions |
| **Joins** | Fewer joins | More joins |
| **Query Speed** | Faster (denormalized) | Slower (normalized) |
| **Storage** | More redundancy | Less redundancy |
| **Maintenance** | Easier | More complex |
| **Use Case** | Most BI workloads | Highly complex hierarchies |

### Fact Table

Contains metrics and measures (quantitative data).

```sql
CREATE TABLE fact_orders (
    order_id          BIGINT PRIMARY KEY,
    user_id           BIGINT,
    product_id        BIGINT,
    date_id           INTEGER,
    quantity          INTEGER,
    revenue           DECIMAL(10,2),
    cost              DECIMAL(10,2),
    profit            DECIMAL(10,2),
    FOREIGN KEY (user_id) REFERENCES dim_users(user_id),
    FOREIGN KEY (product_id) REFERENCES dim_products(product_id),
    FOREIGN KEY (date_id) REFERENCES dim_dates(date_id)
);
```

### Dimension Table

Contains descriptive attributes (contextual data).

```sql
CREATE TABLE dim_users (
    user_id    BIGINT PRIMARY KEY,
    name       VARCHAR(100),
    email      VARCHAR(255),
    segment    VARCHAR(50),
    country    VARCHAR(50),
    created_at TIMESTAMP
);

CREATE TABLE dim_products (
    product_id    BIGINT PRIMARY KEY,
    name          VARCHAR(255),
    category      VARCHAR(100),
    price         DECIMAL(10,2),
    brand         VARCHAR(100)
);

CREATE TABLE dim_dates (
    date_id    INTEGER PRIMARY KEY,
    date       DATE,
    day        INTEGER,
    month      INTEGER,
    quarter    INTEGER,
    year       INTEGER,
    day_of_week VARCHAR(20)
);
```

## ETL Process

### ETL Pipeline

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Extract   │───▶│  Transform  │───▶│    Load     │───▶│  Warehouse  │
│             │    │             │    │             │    │             │
│ • Pull data │    │ • Clean     │    │ • Insert    │    │ • Fact      │
│ • Increment │    │ • Dedupe    │    │ • Update    │    │ • Dimension │
│ • Validate  │    │ • Aggregate │    │ • Upsert    │    │ • Index     │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

### Extract

Pull data from source systems.

| Method | Description | Use Case |
|--------|-------------|----------|
| **Full load** | Extract all data each run | Small datasets, initial load |
| **Incremental** | Extract only new/changed data | Large datasets, ongoing sync |
| **CDC** | Change Data Capture | Real-time sync |

```sql
-- Incremental extract (PostgreSQL)
SELECT *
FROM orders
WHERE updated_at > :last_extract_time;
```

### Transform

Clean, validate, and prepare data.

| Transformation | Example |
|----------------|---------|
| **Data cleaning** | Remove duplicates, handle NULLs |
| **Data validation** | Check data types, ranges |
| **Data enrichment** | Add calculated fields |
| **Data aggregation** | Summarize by time period |
| **Data type conversion** | String to date, etc. |

```sql
-- Transform: Clean and enrich
SELECT
    order_id,
    user_id,
    product_id,
    order_date,
    quantity,
    revenue,
    revenue * 0.8 AS cost,  -- Calculate cost
    revenue - (revenue * 0.8) AS profit,  -- Calculate profit
    UPPER(country) AS country  -- Normalize
FROM raw_orders
WHERE order_date >= '2024-01-01';
```

### Load

Insert transformed data into warehouse.

| Method | Description | Use Case |
|--------|-------------|----------|
| **Insert** | Add new rows | New data only |
| **Update** | Update existing rows | Changed data |
| **Upsert** | Insert or update | Idempotent loads |
| **Bulk load** | Fast batch insert | Large datasets |

```sql
-- Upsert (PostgreSQL)
INSERT INTO fact_orders (order_id, user_id, product_id, quantity, revenue)
VALUES (1, 100, 200, 5, 99.99)
ON CONFLICT (order_id)
DO UPDATE SET
    user_id = EXCLUDED.user_id,
    product_id = EXCLUDED.product_id,
    quantity = EXCLUDED.quantity,
    revenue = EXCLUDED.revenue;
```

### Scheduling

| Frequency | Use Case |
|-----------|----------|
| **Real-time** | Streaming data, monitoring |
| **Hourly** | Operational metrics |
| **Daily** | Most common, overnight |
| **Weekly** | Strategic reporting |

## Modern Data Stack

### Components

```
┌─────────────────────────────────────────────────────────────────┐
│                      Modern Data Stack                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Sources              Ingestion         Warehouse   Transform   │
│  ┌──────┐           ┌─────────┐       ┌─────────┐  ┌─────────┐ │
│  │Sales │──────────▶│Fivetran │──────▶│Snowflake│──▶│   dbt   │ │
│  │Force │           │Airbyte  │       │BigQuery │  │         │ │
│  └──────┘           └─────────┘       └─────────┘  └─────────┘ │
│                                                                  │
│  Visualization                                                   │
│  ┌─────────┐     ┌─────────┐     ┌─────────┐                    │
│  │ Tableau │     │  Looker │     │Metabase │                    │
│  └─────────┘     └─────────┘     └─────────┘                    │
│                                                                  │
│  Orchestration                                                   │
│  ┌─────────┐                                                      │
│  │ Airflow │                                                      │
│  │ Prefect │                                                      │
│  └─────────┘                                                      │
└─────────────────────────────────────────────────────────────────┘
```

### Tool Comparison

| Layer | Traditional | Modern |
|-------|------------|--------|
| **Ingestion** | Custom scripts, Informatica | Fivetran, Airbyte |
| **Warehouse** | On-premise, Oracle | Snowflake, BigQuery |
| **Transform** | Stored procedures, SSIS | dbt, SQL |
| **Visualization** | Excel, SSRS | Looker, Tableau |
| **Orchestration** | Cron jobs | Airflow, Prefect |

### dbt (Data Build Tool)

Modern SQL-based transformation tool.

```sql
-- models/fact_orders.sql
WITH raw_orders AS (
    SELECT * FROM {{ source('raw', 'orders') }}
),

enriched AS (
    SELECT
        order_id,
        user_id,
        product_id,
        order_date,
        quantity,
        revenue,
        revenue * 0.8 AS cost,
        revenue - (revenue * 0.8) AS profit
    FROM raw_orders
    WHERE order_date >= '2024-01-01'
)

SELECT * FROM enriched
```

```yaml
# models/schema.yml
version: 2

models:
  - name: fact_orders
    description: "Order fact table"
    columns:
      - name: order_id
        description: "Unique order identifier"
        tests:
          - unique
          - not_null
      - name: revenue
        description: "Order revenue"
        tests:
          - not_negative
```

## BI Tools

### Tool Comparison Matrix

| Feature | Tableau | Looker | Power BI | Metabase |
|---------|---------|--------|----------|----------|
| **Ease of Use** | High | Medium | High | Very High |
| **SQL Required** | No | Yes | No | Optional |
| **Embedded Analytics** | Limited | Excellent | Good | Good |
| **Data Source Support** | Excellent | Good | Excellent | Good |
| **Cost** | $$$ | $$$ | $$ | Free/$ |
| **Best For** | Visual exploration | Enterprise analytics | Microsoft shops | Small teams |

### Tableau

**Strengths**:
- Powerful visualizations
- Drag-and-drop interface
- Large community

**Use Cases**:
- Ad-hoc data exploration
- Complex visualizations
- Executive dashboards

### Looker

**Strengths**:
- SQL-based (LookML)
- Embedded analytics
- Single source of truth

**Use Cases**:
- Enterprise analytics
- Embedded dashboards
- Data governance

```lookml
# LookML example
view: orders {
  sql_table_name: public.orders ;;

  dimension: order_id {
    primary_key: yes
    type: number
    sql: ${TABLE}.order_id ;;
  }

  dimension: user_id {
    type: number
    sql: ${TABLE}.user_id ;;
  }

  measure: total_revenue {
    type: sum
    sql: ${revenue} ;;
    value_format_name: usd
  }

  measure: order_count {
    type: count
  }
}
```

### Power BI

**Strengths**:
- Microsoft ecosystem integration
- Affordable
- Good for Excel users

**Use Cases**:
- Microsoft shops
- Small to medium businesses
- Excel replacement

### Metabase

**Strengths**:
- Open-source
- Simple to set up
- SQL editor

**Use Cases**:
- Startups
- Small teams
- Quick dashboards

## Metrics and KPIs

### North Star Metric

The single metric that best captures the core value your product delivers to customers.

| Product Type | North Star Metric |
|--------------|-------------------|
| **SaaS** | Weekly Active Users (WAU) |
| **E-commerce** | Orders per week |
| **Marketplace** | Gross Merchandise Value (GMV) |
| **Social Media** | Daily Active Users (DAU) |
| **Streaming** | Hours watched per week |

### Leading vs Lagging Indicators

| Type | Description | Example |
|------|-------------|---------|
| **Leading** | Predicts future performance | Pipeline, trials, signups |
| **Lagging** | Measures past performance | Revenue, churn, profit |

**Balance both**: Leading indicators help you anticipate; lagging indicators confirm results.

### Vanity vs Actionable Metrics

| Vanity Metric | Actionable Metric |
|---------------|-------------------|
| Total signups | Activation rate |
| Page views | Engagement time |
| Social media followers | Conversion rate |
| App downloads | Daily active users |

**Rule**: If the metric goes up/down, would you take different action? If no, it's vanity.

### Common KPIs by Department

| Department | Key KPIs |
|------------|----------|
| **Sales** | Pipeline, conversion rate, revenue, forecast accuracy |
| **Marketing** | Traffic, leads, CAC, ROAS, conversion rate |
| **Product** | DAU/WAU/MAU, retention, feature adoption, NPS |
| **Finance** | Revenue, expenses, cash flow, burn rate |
| **Customer Success** | Churn, health score, response time, CSAT |

## Dashboard Design

### Dashboard Types

| Type | Audience | Update Frequency | Purpose |
|------|----------|------------------|---------|
| **Strategic** | Executives | Monthly/Quarterly | High-level KPIs, trends |
| **Operational** | Managers/Operators | Real-time/Hourly | Day-to-day operations |
| **Analytical** | Analysts | Weekly/Ad-hoc | Deep dive exploration |
| **Tactical** | Teams | Daily | Team-specific metrics |

### Design Principles

1. **Most Important First**: Top-left is prime real estate
2. **Visual Hierarchy**: Use size, color, position
3. **Consistent Layout**: Grid-based design
4. **White Space**: Don't clutter
5. **Actionable Insights**: Not just numbers

### KPI Card Design

```
┌─────────────────────────────────────┐
│  Total Revenue                      │
│  $1,234,567                         │
│  ─────────────────────────────────  │
│  ▲ 12.3% vs last month              │
│  ─────────────────────────────────  │
│  ▂▃▅▇█▇▅▃▂ (sparkline)             │
└─────────────────────────────────────┘
```

### Layout Patterns

**F-Pattern** (Western reading):
```
┌─────────────────────────────────────┐
│  [KPI 1]  [KPI 2]  [KPI 3]  [KPI 4] │  ← Primary
│                                     │
│  [Chart 1]           [Chart 2]      │  ← Secondary
│                                     │
│  [Table]                             │  ← Detail
└─────────────────────────────────────┘
```

**Z-Pattern**:
```
┌─────────────────────────────────────┐
│  [KPI 1] ─────────────────▶ [KPI 2] │
│                              │       │
│                              ▼       │
│                        [Chart 1]     │
│                              │       │
│  [Table] ◀──────────────────┘       │
└─────────────────────────────────────┘
```

## Self-Service BI

### What is Self-Service BI?

Empowering non-technical users to create their own reports and dashboards without IT involvement.

### Components

| Component | Description |
|-----------|-------------|
| **Semantic Layer** | Business-friendly names for data |
| **Pre-built Reports** | Templates users can customize |
| **Data Catalog** | Searchable data dictionary |
| **Training** | User education and documentation |

### Semantic Layer Example

| Technical Name | Business Name |
|----------------|---------------|
| `fact_orders.order_date` | Order Date |
| `dim_users.segment` | Customer Segment |
| `SUM(fact_orders.revenue)` | Total Revenue |

### Benefits

- Reduced IT backlog
- Faster insights
- Increased data literacy
- Better alignment with business needs

## Data Governance

### Key Components

| Component | Description |
|-----------|-------------|
| **Single Source of Truth** | One definition for each metric |
| **Data Quality** | Validation and monitoring |
| **Access Controls** | Who can see what |
| **Data Lineage** | Track data origin and transformations |

### Data Quality Checks

```sql
-- Example data quality checks
SELECT
    'Null check' AS check_type,
    COUNT(*) AS failed_count
FROM fact_orders
WHERE order_id IS NULL

UNION ALL

SELECT
    'Duplicate check' AS check_type,
    COUNT(*) - COUNT(DISTINCT order_id) AS failed_count
FROM fact_orders

UNION ALL

SELECT
    'Negative revenue' AS check_type,
    COUNT(*) AS failed_count
FROM fact_orders
WHERE revenue < 0;
```

### Data Lineage

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Source    │────▶│  Staging    │────▶│  Warehouse  │────▶│   Report    │
│  Salesforce │     │   (Raw)     │     │  (Cleaned)  │     │  Dashboard  │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

## BI Best Practices

### 1. Start with Business Questions

❌ Bad: "Let's build a dashboard for sales."

✅ Good: "What questions does sales need to answer daily?"

### 2. Iterate with Stakeholders

- Build MVP dashboard
- Get feedback
- Iterate

### 3. Document Metrics

```markdown
# Metric Definition: Monthly Recurring Revenue (MRR)

**Definition**: Sum of all monthly subscription revenue.

**Calculation**: SUM(monthly_subscription_amount) for active subscriptions

**Excludes**: One-time fees, annual subscriptions (prorated)

**Owner**: Finance Team

**Update Frequency**: Daily
```

### 4. Monitor Data Quality

- Automated checks
- Alerts on anomalies
- Regular audits

### 5. Version Control

- Use Git for dbt models
- Track dashboard changes
- Document schema changes

## Common BI Use Cases

### Sales Dashboard

| Metric | Description |
|--------|-------------|
| Pipeline | Total value of open deals |
| Conversion Rate | Deals won / deals created |
| Revenue | Actual revenue vs target |
| Forecast | Predicted revenue |

### Marketing Dashboard

| Metric | Description |
|--------|-------------|
| Traffic | Website visitors |
| Leads | Form submissions, signups |
| CAC | Customer Acquisition Cost |
| ROAS | Return on Ad Spend |
| Conversion | Lead to customer rate |

### Product Analytics Dashboard

| Metric | Description |
|--------|-------------|
| DAU/WAU/MAU | Daily/Weekly/Monthly Active Users |
| Retention | D1, D7, D30 retention |
| Feature Adoption | % users using feature |
| NPS | Net Promoter Score |

### Financial Dashboard

| Metric | Description |
|--------|-------------|
| Revenue | Total revenue by period |
| Expenses | Operating expenses |
| Gross Margin | Revenue - COGS |
| Burn Rate | Monthly cash spent |
| Runway | Months until cash runs out |

## Real-Time vs Batch BI

### Comparison

| Aspect | Batch BI | Real-Time BI |
|--------|----------|--------------|
| **Latency** | Hours to days | Seconds to minutes |
| **Cost** | Lower | Higher |
| **Complexity** | Simpler | More complex |
| **Use Cases** | Strategic reporting | Operational monitoring |

### Real-Time Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Events    │────▶│   Kafka     │────▶│  ClickHouse │────▶│  Grafana    │
│   (Apps)    │     │  (Stream)   │     │  (Real-time)│     │  (Monitor)  │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

### Batch Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Sources   │────▶│   ETL Job   │────▶│ Snowflake   │────▶│  Looker     │
│  (Databases)│     │  (Nightly)  │     │  (Warehouse)│     │  (Dashboard)│
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

## BI Performance

### Optimization Techniques

| Technique | Description |
|-----------|-------------|
| **Pre-aggregation** | Pre-calculate summaries |
| **Materialized Views** | Cached query results |
| **Incremental Updates** | Update only new data |
| **Query Optimization** | Indexes, query tuning |
| **Caching** | Redis, CDN for dashboards |

### Materialized View Example

```sql
-- Create materialized view
CREATE MATERIALIZED VIEW mv_daily_revenue AS
SELECT
    DATE(order_date) AS date,
    SUM(revenue) AS total_revenue,
    COUNT(*) AS order_count
FROM fact_orders
GROUP BY DATE(order_date);

-- Refresh
REFRESH MATERIALIZED VIEW mv_daily_revenue;

-- Query (fast)
SELECT * FROM mv_daily_revenue WHERE date >= '2024-01-01';
```

## Embedded Analytics

### What is Embedded Analytics?

White-label BI integrated directly into your product.

### Use Cases

- Customer-facing dashboards
- Internal tool integrations
- Partner portals

### Tools

| Tool | Embedded Support |
|------|------------------|
| **Looker** | Excellent (Looker Embed) |
| **Metabase** | Good (iframe/API) |
| **Cube.js** | Designed for embedding |
| **Recharts** | Custom (React) |

### Example: Embedded Dashboard

```javascript
// Looker embed example
import { LookerEmbedSDK } from '@looker/embed-sdk';

LookerEmbedSDK.init('https://your-looker-instance.com')
  .createDashboardWithId(123)
  .appendTo('#dashboard-container')
  .build()
  .connect()
  .then(() => console.log('Dashboard embedded'))
  .catch(err => console.error('Error:', err));
```

## Implementation

### BI Stack Setup

```yaml
# docker-compose.yml example
version: '3.8'

services:
  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: warehouse
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"

  metabase:
    image: metabase/metabase:latest
    ports:
      - "3000:3000"
    environment:
      MB_DB_TYPE: postgres
      MB_DB_DBNAME: warehouse
      MB_DB_PORT: 5432
      MB_DB_USER: admin
      MB_DB_PASS: password
      MB_DB_HOST: postgres
```

### Data Modeling Example

```sql
-- Star schema implementation

-- Date dimension
CREATE TABLE dim_dates (
    date_id INTEGER PRIMARY KEY,
    date DATE NOT NULL,
    day INTEGER NOT NULL,
    month INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    year INTEGER NOT NULL,
    day_of_week VARCHAR(20) NOT NULL,
    is_weekend BOOLEAN NOT NULL,
    is_holiday BOOLEAN NOT NULL
);

-- User dimension
CREATE TABLE dim_users (
    user_id BIGINT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    segment VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    is_active BOOLEAN NOT NULL
);

-- Product dimension
CREATE TABLE dim_products (
    product_id BIGINT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    brand VARCHAR(100) NOT NULL
);

-- Order fact
CREATE TABLE fact_orders (
    order_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    date_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    revenue DECIMAL(10,2) NOT NULL,
    cost DECIMAL(10,2) NOT NULL,
    profit DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES dim_users(user_id),
    FOREIGN KEY (product_id) REFERENCES dim_products(product_id),
    FOREIGN KEY (date_id) REFERENCES dim_dates(date_id)
);

-- Create indexes
CREATE INDEX idx_fact_orders_user ON fact_orders(user_id);
CREATE INDEX idx_fact_orders_product ON fact_orders(product_id);
CREATE INDEX idx_fact_orders_date ON fact_orders(date_id);
CREATE INDEX idx_fact_orders_date_id ON fact_orders(date_id);
```

### Dashboard Creation (Metabase API)

```python
import requests

# Create dashboard
def create_dashboard(name, description):
    response = requests.post(
        'http://localhost:3000/api/dashboard',
        json={
            'name': name,
            'description': description
        },
        headers={'X-Metabase-Session': 'your-session-token'}
    )
    return response.json()

# Add card to dashboard
def add_card(dashboard_id, card_id):
    response = requests.post(
        f'http://localhost:3000/api/dashboard/{dashboard_id}/cards',
        json={'cardId': card_id},
        headers={'X-Metabase-Session': 'your-session-token'}
    )
    return response.json()
```

## Real Examples

### SaaS Metrics Dashboard

```
┌─────────────────────────────────────────────────────────────────┐
│  SaaS Metrics Dashboard                                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │    MRR      │  │   ARR       │  │   Churn     │  │  NPS    │ │
│  │  $125,000   │  │ $1,500,000  │  │   2.5%      │  │   +45   │ │
│  │  ▲ 8.2%     │  │  ▲ 10.1%    │  │  ▼ 0.3%     │  │  ▲ 5    │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
│                                                                  │
│  Monthly Recurring Revenue Trend                                 │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  $150k ┤                                                    │ │
│  │  $125k ┤  ●───●───●───●───●                                  │ │
│  │  $100k ┤                                                    │ │
│  │   $75k ┤                                                    │ │
│  │   $50k ┤                                                    │ │
│  │   $25k ┤                                                    │ │
│  │    $0  └──────────────────────────────────────────────────│ │
│  │        Jan  Feb  Mar  Apr  May  Jun                         │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  Churn by Plan                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  Enterprise ████████████████  1.2%                          │ │
│  │  Business   ████████████████  2.8%                          │ │
│  │  Starter    ████████████████  4.5%                          │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### E-commerce BI System

```
┌─────────────────────────────────────────────────────────────────┐
│  E-commerce Analytics                                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │  Revenue    │  │  Orders     │  │  AOV        │  │ Conv.   │ │
│  │  $45,234    │  │    1,234    │  │   $36.67    │  │  2.5%   │ │
│  │  ▲ 12.3%    │  │  ▲ 8.5%     │  │  ▲ 3.2%     │  │  ▲ 0.5% │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
│                                                                  │
│  Revenue by Category                                             │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  Electronics  ████████████████████████████████████  $15,000  │ │
│  │  Clothing     ██████████████████████                  $10,000  │ │
│  │  Home         ████████████████                         $8,000  │ │
│  │  Books        ██████████                                 $4,000  │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  Top Products                                                    │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  Product          │  Sales  │  Revenue  │  Growth           │ │
│  ├───────────────────┼─────────┼──────────┼───────────────────┤ │
│  │  Wireless Mouse   │   234   │  $4,680   │  ▲ 15.3%          │ │
│  │  USB-C Cable      │   189   │  $1,890   │  ▲ 8.7%           │ │
│  │  Laptop Stand     │   156   │  $3,120   │  ▲ 22.1%          │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Summary Checklist

### Planning Phase

- [ ] Identify business questions
- [ ] Define metrics and KPIs
- [ ] Select BI tool
- [ ] Design data model
- [ ] Plan ETL pipeline

### Implementation Phase

- [ ] Set up data warehouse
- [ ] Implement ETL/ELT
- [ ] Create semantic layer
- [ ] Build dashboards
- [ ] Test data quality

### Maintenance Phase

- [ ] Monitor data quality
- [ ] Update dashboards regularly
- [ ] Gather user feedback
- [ ] Optimize performance
```

---

## Quick Start

### Metabase Setup

```bash
# Docker setup
docker run -d -p 3000:3000 \
  -e MB_DB_TYPE=postgres \
  -e MB_DB_DBNAME=metabase \
  -e MB_DB_USER=metabase \
  -e MB_DB_PASS=password \
  metabase/metabase
```

### Create Dashboard

```sql
-- Sales dashboard query
SELECT 
  DATE_TRUNC('month', created_at) as month,
  SUM(total) as revenue,
  COUNT(*) as orders
FROM orders
WHERE created_at >= CURRENT_DATE - INTERVAL '12 months'
GROUP BY DATE_TRUNC('month', created_at)
ORDER BY month DESC
```

---

## Production Checklist

- [ ] **Data Sources**: Identify and connect all data sources
- [ ] **ETL/ELT**: Set up data transformation pipeline
- [ ] **Data Warehouse**: Configure data warehouse
- [ ] **BI Tool**: Select and configure BI tool
- [ ] **Dashboards**: Create key business dashboards
- [ ] **Access Control**: Set up user permissions
- [ ] **Performance**: Optimize query performance
- [ ] **Documentation**: Document data models and dashboards
- [ ] **Training**: Train users on BI tools
- [ ] **Monitoring**: Monitor BI system health
- [ ] **Backup**: Backup dashboards and configurations
- [ ] **Governance**: Establish data governance policies

---

## Anti-patterns

### ❌ Don't: No Data Model

```sql
-- ❌ Bad - Direct query on production
SELECT * FROM orders o
JOIN users u ON o.user_id = u.id
JOIN products p ON o.product_id = p.id
-- Complex joins, slow queries!
```

```sql
-- ✅ Good - Pre-aggregated in data warehouse
SELECT * FROM sales_summary_monthly
-- Fast, optimized for analytics
```

### ❌ Don't: Too Many Dashboards

```markdown
# ❌ Bad - Dashboard overload
- Dashboard 1
- Dashboard 2
- Dashboard 3
# ... 50 more dashboards
```

```markdown
# ✅ Good - Focused dashboards
- Executive Dashboard (KPIs)
- Sales Dashboard
- Marketing Dashboard
# 5-10 key dashboards
```

---

## Integration Points

- **Dashboard Design** (`23-business-analytics/dashboard-design/`) - Dashboard layouts
- **KPI Metrics** (`23-business-analytics/kpi-metrics/`) - Key metrics
- **SQL for Analytics** (`23-business-analytics/sql-for-analytics/`) - Query patterns

---

## Further Reading

- [Tableau Documentation](https://help.tableau.com/)
- [Looker Documentation](https://cloud.google.com/looker/docs)
- [Metabase Documentation](https://www.metabase.com/docs/)
- [ ] Document changes
