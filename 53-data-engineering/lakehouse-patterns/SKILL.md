---
name: Lakehouse Patterns
description: Comprehensive guide to data lakehouse architecture combining data lake flexibility with data warehouse performance using Delta Lake, Iceberg, and Hudi
---

# Lakehouse Patterns

## What is a Data Lakehouse?

**Data Lakehouse:** Architecture combining data lake (flexibility, low cost) with data warehouse (performance, ACID transactions).

### Evolution
```
Data Warehouse (2000s):
- Structured data only
- Expensive
- Fast queries

Data Lake (2010s):
- All data types (structured, semi-structured, unstructured)
- Cheap (object storage)
- Slow queries, no ACID

Data Lakehouse (2020s):
- All data types
- Cheap storage
- Fast queries + ACID transactions
```

### Key Features
- **ACID transactions:** Reliable writes
- **Schema enforcement:** Data quality
- **Time travel:** Query historical data
- **Unified storage:** Single copy for all workloads
- **Open formats:** Parquet, ORC (not proprietary)

---

## Lakehouse Technologies

### Delta Lake (Databricks)
```python
# Write Delta table
df.write.format("delta").save("/path/to/delta-table")

# Read Delta table
df = spark.read.format("delta").load("/path/to/delta-table")

# ACID transactions
df.write.format("delta").mode("append").save("/path/to/delta-table")

# Time travel
df = spark.read.format("delta").option("versionAsOf", 0).load("/path")
df = spark.read.format("delta").option("timestampAsOf", "2024-01-01").load("/path")
```

### Apache Iceberg (Netflix)
```python
# Create Iceberg table
spark.sql("""
    CREATE TABLE my_table (
        id BIGINT,
        name STRING,
        created_at TIMESTAMP
    ) USING iceberg
    PARTITIONED BY (days(created_at))
""")

# Write data
df.writeTo("my_table").append()

# Time travel
spark.read.option("snapshot-id", 123456).table("my_table")
```

### Apache Hudi (Uber)
```python
# Write Hudi table
df.write.format("hudi") \
    .option("hoodie.table.name", "my_table") \
    .option("hoodie.datasource.write.recordkey.field", "id") \
    .option("hoodie.datasource.write.partitionpath.field", "date") \
    .option("hoodie.datasource.write.precombine.field", "updated_at") \
    .mode("append") \
    .save("/path/to/hudi-table")

# Read Hudi table
df = spark.read.format("hudi").load("/path/to/hudi-table")
```

---

## Architecture Layers

### Bronze Layer (Raw)
```
Purpose: Store raw data as-is
Format: JSON, CSV, Parquet
Schema: Flexible (schema-on-read)
Retention: Long-term (years)

Example:
s3://lakehouse/bronze/salesforce/accounts/
s3://lakehouse/bronze/mysql/orders/
```

### Silver Layer (Cleaned)
```
Purpose: Cleaned, validated, deduplicated
Format: Delta/Iceberg/Hudi
Schema: Enforced
Retention: Medium-term (months to years)

Example:
s3://lakehouse/silver/customers/
s3://lakehouse/silver/orders/
```

### Gold Layer (Analytics)
```
Purpose: Business-ready, aggregated
Format: Delta/Iceberg/Hudi
Schema: Dimensional model
Retention: Long-term (years)

Example:
s3://lakehouse/gold/fct_orders/
s3://lakehouse/gold/dim_customers/
```

---

## Delta Lake Deep Dive

### Creating Delta Tables
```python
# From DataFrame
df.write.format("delta") \
    .mode("overwrite") \
    .save("/delta/customers")

# SQL
spark.sql("""
    CREATE TABLE customers
    USING DELTA
    LOCATION '/delta/customers'
    AS SELECT * FROM source_customers
""")
```

### ACID Transactions
```python
# Multiple writes are atomic
from delta.tables import DeltaTable

delta_table = DeltaTable.forPath(spark, "/delta/customers")

# Upsert (merge)
delta_table.alias("target").merge(
    source_df.alias("source"),
    "target.customer_id = source.customer_id"
).whenMatchedUpdateAll() \
 .whenNotMatchedInsertAll() \
 .execute()
```

### Time Travel
```python
# Read version 0
df = spark.read.format("delta").option("versionAsOf", 0).load("/delta/customers")

# Read as of timestamp
df = spark.read.format("delta") \
    .option("timestampAsOf", "2024-01-01 00:00:00") \
    .load("/delta/customers")

# Restore to previous version
delta_table = DeltaTable.forPath(spark, "/delta/customers")
delta_table.restoreToVersion(5)
```

### Schema Evolution
```python
# Add column
df_with_new_column.write.format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .save("/delta/customers")

# Schema enforcement (default)
# Prevents incompatible schema changes
```

### Optimize and Z-Order
```python
# Compact small files
spark.sql("OPTIMIZE delta.`/delta/customers`")

# Z-order (multi-dimensional clustering)
spark.sql("""
    OPTIMIZE delta.`/delta/customers`
    ZORDER BY (customer_id, created_at)
""")
```

### Vacuum (Delete Old Files)
```python
# Delete files older than 7 days (default retention)
spark.sql("VACUUM delta.`/delta/customers` RETAIN 168 HOURS")
```

---

## Iceberg Features

### Hidden Partitioning
```sql
-- Iceberg handles partitioning automatically
CREATE TABLE events (
    event_id BIGINT,
    event_time TIMESTAMP,
    user_id BIGINT
) USING iceberg
PARTITIONED BY (days(event_time))

-- Query without partition filter (still fast)
SELECT * FROM events WHERE user_id = 123
```

### Schema Evolution
```sql
-- Add column
ALTER TABLE events ADD COLUMN event_type STRING

-- Rename column
ALTER TABLE events RENAME COLUMN event_time TO timestamp

-- Drop column
ALTER TABLE events DROP COLUMN user_id
```

### Snapshot Isolation
```sql
-- Read from specific snapshot
SELECT * FROM events VERSION AS OF 123456

-- Time travel
SELECT * FROM events TIMESTAMP AS OF '2024-01-01 00:00:00'
```

---

## Hudi Features

### Copy-on-Write vs Merge-on-Read

**Copy-on-Write (COW):**
```
Writes: Slow (rewrite entire file)
Reads: Fast (no merge needed)
Use case: Read-heavy workloads
```

**Merge-on-Read (MOR):**
```
Writes: Fast (append to log)
Reads: Slower (merge log with base file)
Use case: Write-heavy workloads
```

### Incremental Queries
```python
# Read only new data since last query
incremental_df = spark.read.format("hudi") \
    .option("hoodie.datasource.query.type", "incremental") \
    .option("hoodie.datasource.read.begin.instanttime", "20240101000000") \
    .load("/path/to/hudi-table")
```

---

## Lakehouse vs Data Warehouse

### Data Warehouse (Snowflake, BigQuery, Redshift)
```
Pros:
- Fast SQL queries
- ACID transactions
- Mature ecosystem

Cons:
- Expensive storage
- Structured data only
- Vendor lock-in
```

### Data Lakehouse (Delta Lake, Iceberg, Hudi)
```
Pros:
- Cheap storage (S3, GCS, ADLS)
- All data types
- Open formats
- ACID transactions

Cons:
- Newer technology
- Requires more setup
- Performance tuning needed
```

**Recommendation:** Use both (lakehouse for raw/historical, warehouse for analytics)

---

## Best Practices

### 1. Use Partitioning Wisely
```python
# Good: Partition by date (common filter)
df.write.format("delta") \
    .partitionBy("date") \
    .save("/delta/events")

# Bad: Too many partitions (millions)
# Bad: Partition by high-cardinality column (user_id)
```

### 2. Compact Small Files
```python
# Run OPTIMIZE regularly
spark.sql("OPTIMIZE delta.`/delta/events`")

# Schedule: Daily or weekly
```

### 3. Use Z-Ordering for Multi-Column Filters
```python
# If you filter by customer_id AND date
spark.sql("""
    OPTIMIZE delta.`/delta/orders`
    ZORDER BY (customer_id, order_date)
""")
```

### 4. Set Retention Period
```python
# Keep 30 days of history
spark.conf.set("spark.databricks.delta.retentionDurationCheck.enabled", "false")
spark.sql("VACUUM delta.`/delta/events` RETAIN 720 HOURS")
```

### 5. Monitor Table Stats
```python
# Check table size, files, partitions
spark.sql("DESCRIBE DETAIL delta.`/delta/events`")
```

---

## Medallion Architecture

### Bronze → Silver → Gold
```
Bronze (Raw):
- Ingest all data as-is
- No transformations
- Append-only

Silver (Cleaned):
- Deduplicate
- Validate
- Standardize
- Enrich

Gold (Analytics):
- Aggregate
- Dimensional model
- Business logic
```

### Example Pipeline
```python
# Bronze: Ingest raw data
raw_df.write.format("delta").mode("append").save("/bronze/events")

# Silver: Clean and validate
bronze_df = spark.read.format("delta").load("/bronze/events")
cleaned_df = bronze_df.dropDuplicates(["event_id"]) \
    .filter("event_time IS NOT NULL")
cleaned_df.write.format("delta").mode("append").save("/silver/events")

# Gold: Aggregate
silver_df = spark.read.format("delta").load("/silver/events")
aggregated_df = silver_df.groupBy("user_id", "date").agg(
    count("*").alias("event_count"),
    sum("revenue").alias("total_revenue")
)
aggregated_df.write.format("delta").mode("overwrite").save("/gold/user_daily_stats")
```

---

## Governance and Security

### Data Catalog
```
Tools:
- AWS Glue Catalog
- Databricks Unity Catalog
- Apache Atlas

Features:
- Metadata management
- Data lineage
- Search and discovery
```

### Access Control
```sql
-- Grant permissions
GRANT SELECT ON TABLE customers TO user@example.com

-- Row-level security
CREATE ROW ACCESS POLICY customer_policy
ON customers
GRANT TO ('user@example.com')
FILTER USING (region = 'US')
```

### Data Quality
```python
# Great Expectations
from great_expectations.dataset import SparkDFDataset

ge_df = SparkDFDataset(df)
ge_df.expect_column_values_to_not_be_null("customer_id")
ge_df.expect_column_values_to_be_unique("customer_id")
results = ge_df.validate()
```

---

## Summary

**Data Lakehouse:** Combines data lake + data warehouse

**Technologies:**
- Delta Lake (Databricks)
- Apache Iceberg (Netflix)
- Apache Hudi (Uber)

**Key Features:**
- ACID transactions
- Schema enforcement
- Time travel
- Open formats

**Layers:**
- Bronze: Raw data
- Silver: Cleaned data
- Gold: Analytics-ready

**Best Practices:**
- Partition wisely
- Compact small files
- Use Z-ordering
- Set retention period
- Monitor table stats

**vs Data Warehouse:**
- Cheaper storage
- All data types
- Open formats
- Requires more setup
