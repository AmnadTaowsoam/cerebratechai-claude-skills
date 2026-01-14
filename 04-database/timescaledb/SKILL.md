# TimescaleDB (Time-Series Database) Patterns

## 1. TimescaleDB Setup

### Installation
```sql
-- Install TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Check TimescaleDB version
SELECT extversion FROM pg_extension WHERE extname = 'timescaledb';
```

### Database Initialization
```sql
-- Create database
CREATE DATABASE timeseries_db;

-- Connect to database
\c timeseries_db;

-- Enable TimescaleDB
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Verify installation
SELECT * FROM timescaledb_information.hypertables;
```

## 2. Hypertable Creation

### Basic Hypertable
```sql
-- Create a basic time-series table
CREATE TABLE sensor_data (
    time TIMESTAMPTZ NOT NULL,
    sensor_id INTEGER NOT NULL,
    temperature DOUBLE PRECISION,
    humidity DOUBLE PRECISION,
    pressure DOUBLE PRECISION
);

-- Convert to hypertable
SELECT create_hypertable('sensor_data', 'time');

-- Verify hypertable
SELECT * FROM timescaledb_information.hypertables WHERE hypertable_name = 'sensor_data';
```

### Hypertable with Multiple Dimensions
```sql
-- Create table with multiple dimensions
CREATE TABLE iot_metrics (
    time TIMESTAMPTZ NOT NULL,
    device_id INTEGER NOT NULL,
    location_id INTEGER NOT NULL,
    metric_type TEXT NOT NULL,
    value DOUBLE PRECISION,
    metadata JSONB
);

-- Create hypertable with time and space partitioning
SELECT create_hypertable(
    'iot_metrics',
    'time',
    partitioning_column => 'device_id',
    number_partitions => 4
);
```

### Hypertable with Custom Chunk Size
```sql
-- Create hypertable with custom chunk interval (1 day)
SELECT create_hypertable(
    'sensor_data',
    'time',
    chunk_time_interval => interval '1 day'
);

-- Create hypertable with custom chunk interval (1 hour for high-frequency data)
SELECT create_hypertable(
    'high_frequency_data',
    'time',
    chunk_time_interval => interval '1 hour'
);
```

## 3. Time-based Partitioning

### Automatic Partitioning
```sql
-- TimescaleDB automatically partitions data by time
-- Chunks are created based on the chunk_time_interval

-- View chunks for a hypertable
SELECT *
FROM timescaledb_information.chunks
WHERE hypertable_name = 'sensor_data'
ORDER BY range_start;

-- View chunk sizes
SELECT
    chunk_schema,
    chunk_name,
    range_start,
    range_end,
    pg_size_pretty(pg_total_relation_size(chunk_schema || '.' || chunk_name)) as size
FROM timescaledb_information.chunks
WHERE hypertable_name = 'sensor_data'
ORDER BY range_start;
```

### Manual Chunk Management
```sql
-- Show chunks
SELECT show_chunks('sensor_data');

-- Show chunks for specific time range
SELECT show_chunks('sensor_data', NOW() - INTERVAL '7 days');

-- Create chunk for future data
SELECT create_chunk('sensor_data', NOW() + INTERVAL '1 day');

-- Drop old chunks
SELECT drop_chunks('sensor_data', INTERVAL '30 days');
```

## 4. Continuous Aggregates

### Basic Continuous Aggregate
```sql
-- Create a continuous aggregate for hourly averages
CREATE MATERIALIZED VIEW sensor_hourly_avg
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 hour', time) AS bucket,
    sensor_id,
    AVG(temperature) AS avg_temperature,
    AVG(humidity) AS avg_humidity,
    AVG(pressure) AS avg_pressure,
    COUNT(*) AS count
FROM sensor_data
GROUP BY bucket, sensor_id;

-- Refresh continuous aggregate
CALL refresh_continuous_aggregate('sensor_hourly_avg', NULL, NULL);
```

### Continuous Aggregate with Multiple Time Buckets
```sql
-- Daily aggregates
CREATE MATERIALIZED VIEW sensor_daily_avg
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 day', time) AS bucket,
    sensor_id,
    AVG(temperature) AS avg_temperature,
    MIN(temperature) AS min_temperature,
    MAX(temperature) AS max_temperature,
    STDDEV(temperature) AS stddev_temperature,
    COUNT(*) AS count
FROM sensor_data
GROUP BY bucket, sensor_id;

-- Weekly aggregates
CREATE MATERIALIZED VIEW sensor_weekly_avg
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 week', time) AS bucket,
    sensor_id,
    AVG(temperature) AS avg_temperature,
    MIN(temperature) AS min_temperature,
    MAX(temperature) AS max_temperature,
    COUNT(*) AS count
FROM sensor_data
GROUP BY bucket, sensor_id;
```

### Continuous Aggregate with Real-time Aggregation
```sql
-- Create continuous aggregate with real-time aggregation
CREATE MATERIALIZED VIEW sensor_hourly_avg_realtime
WITH (timescaledb.continuous, timescaledb.materialized_only = false) AS
SELECT
    time_bucket('1 hour', time) AS bucket,
    sensor_id,
    AVG(temperature) AS avg_temperature,
    AVG(humidity) AS avg_humidity,
    COUNT(*) AS count
FROM sensor_data
GROUP BY bucket, sensor_id;

-- Query with real-time data
SELECT * FROM sensor_hourly_avg_realtime
WHERE bucket >= NOW() - INTERVAL '1 day';
```

### Continuous Aggregate with Custom Refresh Policy
```sql
-- Set refresh policy
SELECT add_continuous_aggregate_policy(
    'sensor_hourly_avg',
    start_offset => INTERVAL '1 hour',
    end_offset => INTERVAL '1 minute',
    schedule_interval => INTERVAL '5 minutes'
);

-- View continuous aggregate policies
SELECT * FROM timescaledb_information.jobs
WHERE hypertable_name = 'sensor_hourly_avg';

-- Remove policy
SELECT remove_continuous_aggregate_policy('sensor_hourly_avg');
```

## 5. Data Retention Policies

### Drop Chunks Policy
```sql
-- Create drop chunks policy to retain data for 30 days
SELECT add_drop_chunks_policy(
    'sensor_data',
    INTERVAL '30 days',
    schedule_interval => INTERVAL '1 day'
);

-- View drop chunks policies
SELECT * FROM timescaledb_information.jobs
WHERE hypertable_name = 'sensor_data';

-- Remove drop chunks policy
SELECT remove_drop_chunks_policy('sensor_data');
```

### Compress Chunks Policy
```sql
-- Enable compression on hypertable
ALTER TABLE sensor_data SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'sensor_id'
);

-- Create compress chunks policy
SELECT add_compression_policy(
    'sensor_data',
    INTERVAL '7 days',
    schedule_interval => INTERVAL '1 day'
);

-- View compression policies
SELECT * FROM timescaledb_information.jobs
WHERE hypertable_name = 'sensor_data';

-- Remove compression policy
SELECT remove_compression_policy('sensor_data');
```

### Combined Retention Policy
```sql
-- Create combined policy: compress after 7 days, drop after 90 days
SELECT add_compression_policy(
    'sensor_data',
    INTERVAL '7 days',
    schedule_interval => INTERVAL '1 day'
);

SELECT add_drop_chunks_policy(
    'sensor_data',
    INTERVAL '90 days',
    schedule_interval => INTERVAL '1 day'
);
```

## 6. Query Optimization for Time-Series

### Time Bucket Queries
```sql
-- Basic time bucket
SELECT
    time_bucket('5 minutes', time) AS bucket,
    sensor_id,
    AVG(temperature) AS avg_temperature
FROM sensor_data
WHERE time >= NOW() - INTERVAL '1 day'
GROUP BY bucket, sensor_id
ORDER BY bucket;

-- Time bucket with offset
SELECT
    time_bucket('1 hour', time, TIMESTAMP '2020-01-01 00:00:00') AS bucket,
    sensor_id,
    AVG(temperature) AS avg_temperature
FROM sensor_data
WHERE time >= NOW() - INTERVAL '1 day'
GROUP BY bucket, sensor_id
ORDER BY bucket;
```

### Time Bucket Gap Filling
```sql
-- Fill missing time buckets with NULL
SELECT
    time_bucket('5 minutes', time) AS bucket,
    sensor_id,
    AVG(temperature) AS avg_temperature
FROM sensor_data
WHERE time >= NOW() - INTERVAL '1 hour'
GROUP BY bucket, sensor_id
ORDER BY bucket;

-- Fill missing time buckets with previous value (LOCF)
SELECT
    time_bucket('5 minutes', time) AS bucket,
    sensor_id,
    locf(AVG(temperature)) AS avg_temperature
FROM sensor_data
WHERE time >= NOW() - INTERVAL '1 hour'
GROUP BY bucket, sensor_id
ORDER BY bucket;

-- Fill missing time buckets with linear interpolation
SELECT
    time_bucket('5 minutes', time) AS bucket,
    sensor_id,
    interpolate(AVG(temperature)) AS avg_temperature
FROM sensor_data
WHERE time >= NOW() - INTERVAL '1 hour'
GROUP BY bucket, sensor_id
ORDER BY bucket;
```

### Latest Data Query
```sql
-- Get latest data for each sensor
SELECT DISTINCT ON (sensor_id)
    sensor_id,
    time,
    temperature,
    humidity,
    pressure
FROM sensor_data
ORDER BY sensor_id, time DESC;

-- Using LAST() function
SELECT
    sensor_id,
    last(temperature, time) AS latest_temperature,
    last(humidity, time) AS latest_humidity,
    last(pressure, time) AS latest_pressure
FROM sensor_data
WHERE time >= NOW() - INTERVAL '1 day'
GROUP BY sensor_id;
```

### First/Last Data Query
```sql
-- Get first data point in time range
SELECT
    sensor_id,
    first(temperature, time) AS first_temperature,
    first(humidity, time) AS first_humidity
FROM sensor_data
WHERE time >= NOW() - INTERVAL '1 day'
GROUP BY sensor_id;

-- Get last data point in time range
SELECT
    sensor_id,
    last(temperature, time) AS last_temperature,
    last(humidity, time) AS last_humidity
FROM sensor_data
WHERE time >= NOW() - INTERVAL '1 day'
GROUP BY sensor_id;
```

### Delta and Rate Calculations
```sql
-- Calculate delta between consecutive values
SELECT
    time_bucket('1 hour', time) AS bucket,
    sensor_id,
    AVG(temperature) AS avg_temperature,
    delta(AVG(temperature)) OVER (
        PARTITION BY sensor_id
        ORDER BY bucket
    ) AS temperature_delta
FROM sensor_data
WHERE time >= NOW() - INTERVAL '1 day'
GROUP BY bucket, sensor_id
ORDER BY sensor_id, bucket;

-- Calculate rate of change
SELECT
    time_bucket('1 hour', time) AS bucket,
    sensor_id,
    AVG(temperature) AS avg_temperature,
    rate(AVG(temperature), bucket) OVER (
        PARTITION BY sensor_id
        ORDER BY bucket
    ) AS temperature_rate
FROM sensor_data
WHERE time >= NOW() - INTERVAL '1 day'
GROUP BY bucket, sensor_id
ORDER BY sensor_id, bucket;
```

## 7. Compression

### Enable Compression
```sql
-- Enable compression on hypertable
ALTER TABLE sensor_data SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'sensor_id',
    timescaledb.compress_orderby = 'time'
);

-- View compression settings
SELECT *
FROM timescaledb_information.compression_settings
WHERE hypertable_name = 'sensor_data';
```

### Manual Compression
```sql
-- Compress a specific chunk
SELECT compress_chunk(
    (SELECT chunk_name FROM timescaledb_information.chunks
     WHERE hypertable_name = 'sensor_data'
     AND range_start < NOW() - INTERVAL '7 days'
     LIMIT 1)
);

-- Decompress a chunk
SELECT decompress_chunk(
    (SELECT chunk_name FROM timescaledb_information.chunks
     WHERE hypertable_name = 'sensor_data'
     AND range_start < NOW() - INTERVAL '7 days'
     LIMIT 1)
);
```

### Compression Statistics
```sql
-- View compression statistics
SELECT
    chunk_schema,
    chunk_name,
    range_start,
    range_end,
    is_compressed,
    pg_size_pretty(pg_total_relation_size(chunk_schema || '.' || chunk_name)) as size,
    pg_size_pretty(pg_total_relation_size(chunk_schema || '.' || chunk_name || '_compressed')) as compressed_size
FROM timescaledb_information.chunks
WHERE hypertable_name = 'sensor_data'
ORDER BY range_start;

-- View compression ratio
SELECT
    hypertable_name,
    COUNT(*) as total_chunks,
    SUM(CASE WHEN is_compressed THEN 1 ELSE 0 END) as compressed_chunks,
    ROUND(100.0 * SUM(CASE WHEN is_compressed THEN 1 ELSE 0 END) / COUNT(*), 2) as compression_percentage
FROM timescaledb_information.chunks
WHERE hypertable_name = 'sensor_data'
GROUP BY hypertable_name;
```

## 8. Common Time-Series Queries

### Aggregation Over Time
```sql
-- Hourly aggregation
SELECT
    time_bucket('1 hour', time) AS bucket,
    sensor_id,
    AVG(temperature) AS avg_temperature,
    MIN(temperature) AS min_temperature,
    MAX(temperature) AS max_temperature,
    STDDEV(temperature) AS stddev_temperature,
    COUNT(*) AS count
FROM sensor_data
WHERE time >= NOW() - INTERVAL '1 day'
GROUP BY bucket, sensor_id
ORDER BY bucket;

-- Daily aggregation
SELECT
    time_bucket('1 day', time) AS bucket,
    sensor_id,
    AVG(temperature) AS avg_temperature,
    MIN(temperature) AS min_temperature,
    MAX(temperature) AS max_temperature,
    COUNT(*) AS count
FROM sensor_data
WHERE time >= NOW() - INTERVAL '30 days'
GROUP BY bucket, sensor_id
ORDER BY bucket;
```

### Rolling Aggregations
```sql
-- Rolling average using window functions
SELECT
    time,
    sensor_id,
    temperature,
    AVG(temperature) OVER (
        PARTITION BY sensor_id
        ORDER BY time
        RANGE BETWEEN INTERVAL '1 hour' PRECEDING AND CURRENT ROW
    ) AS rolling_avg_1h
FROM sensor_data
WHERE time >= NOW() - INTERVAL '1 day'
ORDER BY sensor_id, time;

-- Rolling sum
SELECT
    time_bucket('1 hour', time) AS bucket,
    sensor_id,
    SUM(temperature) OVER (
        PARTITION BY sensor_id
        ORDER BY bucket
        RANGE BETWEEN INTERVAL '24 hours' PRECEDING AND CURRENT ROW
    ) AS rolling_sum_24h
FROM sensor_data
WHERE time >= NOW() - INTERVAL '7 days'
GROUP BY bucket, sensor_id
ORDER BY sensor_id, bucket;
```

### Percentile Calculations
```sql
-- Using percentile_cont
SELECT
    time_bucket('1 hour', time) AS bucket,
    sensor_id,
    percentile_cont(0.5) WITHIN GROUP (ORDER BY temperature) AS median_temperature,
    percentile_cont(0.95) WITHIN GROUP (ORDER BY temperature) AS p95_temperature,
    percentile_cont(0.99) WITHIN GROUP (ORDER BY temperature) AS p99_temperature
FROM sensor_data
WHERE time >= NOW() - INTERVAL '1 day'
GROUP BY bucket, sensor_id
ORDER BY bucket;

-- Using percentile_disc
SELECT
    time_bucket('1 day', time) AS bucket,
    sensor_id,
    percentile_disc(0.5) WITHIN GROUP (ORDER BY temperature) AS median_temperature,
    percentile_disc(0.95) WITHIN GROUP (ORDER BY temperature) AS p95_temperature
FROM sensor_data
WHERE time >= NOW() - INTERVAL '30 days'
GROUP BY bucket, sensor_id
ORDER BY bucket;
```

### Time-Series Joins
```sql
-- Join sensor data with sensor metadata
SELECT
    sd.time,
    sd.sensor_id,
    sm.name AS sensor_name,
    sm.location,
    sd.temperature,
    sd.humidity
FROM sensor_data sd
JOIN sensor_metadata sm ON sd.sensor_id = sm.id
WHERE sd.time >= NOW() - INTERVAL '1 day'
ORDER BY sd.time;

-- Join with time bucket alignment
SELECT
    time_bucket('1 hour', sd.time) AS bucket,
    sd.sensor_id,
    sm.name AS sensor_name,
    AVG(sd.temperature) AS avg_temperature,
    AVG(sd.humidity) AS avg_humidity
FROM sensor_data sd
JOIN sensor_metadata sm ON sd.sensor_id = sm.id
WHERE sd.time >= NOW() - INTERVAL '1 day'
GROUP BY bucket, sd.sensor_id, sm.name
ORDER BY bucket;
```

### Anomaly Detection
```sql
-- Simple anomaly detection using z-score
WITH stats AS (
    SELECT
        sensor_id,
        AVG(temperature) AS avg_temp,
        STDDEV(temperature) AS stddev_temp
    FROM sensor_data
    WHERE time >= NOW() - INTERVAL '7 days'
    GROUP BY sensor_id
)
SELECT
    sd.time,
    sd.sensor_id,
    sd.temperature,
    s.avg_temp,
    s.stddev_temp,
    (sd.temperature - s.avg_temp) / s.stddev_temp AS z_score
FROM sensor_data sd
JOIN stats s ON sd.sensor_id = s.sensor_id
WHERE sd.time >= NOW() - INTERVAL '1 day'
AND ABS((sd.temperature - s.avg_temp) / s.stddev_temp) > 3
ORDER BY sd.time;
```

## 9. Downsampling Strategies

### Basic Downsampling
```sql
-- Create downsampled table
CREATE TABLE sensor_data_downsampled (
    time TIMESTAMPTZ NOT NULL,
    sensor_id INTEGER NOT NULL,
    avg_temperature DOUBLE PRECISION,
    min_temperature DOUBLE PRECISION,
    max_temperature DOUBLE PRECISION,
    avg_humidity DOUBLE PRECISION,
    min_humidity DOUBLE PRECISION,
    max_humidity DOUBLE PRECISION,
    count BIGINT
);

-- Create hypertable
SELECT create_hypertable('sensor_data_downsampled', 'time');

-- Insert downsampled data
INSERT INTO sensor_data_downsampled
SELECT
    time_bucket('1 hour', time) AS time,
    sensor_id,
    AVG(temperature) AS avg_temperature,
    MIN(temperature) AS min_temperature,
    MAX(temperature) AS max_temperature,
    AVG(humidity) AS avg_humidity,
    MIN(humidity) AS min_humidity,
    MAX(humidity) AS max_humidity,
    COUNT(*) AS count
FROM sensor_data
WHERE time >= NOW() - INTERVAL '1 day'
GROUP BY time, sensor_id;
```

### Downsampling with Continuous Aggregates
```sql
-- Create continuous aggregate for downsampling
CREATE MATERIALIZED VIEW sensor_data_hourly
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 hour', time) AS time,
    sensor_id,
    AVG(temperature) AS avg_temperature,
    MIN(temperature) AS min_temperature,
    MAX(temperature) AS max_temperature,
    STDDEV(temperature) AS stddev_temperature,
    AVG(humidity) AS avg_humidity,
    MIN(humidity) AS min_humidity,
    MAX(humidity) AS max_humidity,
    COUNT(*) AS count
FROM sensor_data
GROUP BY time, sensor_id;

-- Set refresh policy
SELECT add_continuous_aggregate_policy(
    'sensor_data_hourly',
    start_offset => INTERVAL '1 hour',
    end_offset => INTERVAL '1 minute',
    schedule_interval => INTERVAL '5 minutes'
);
```

### Multi-level Downsampling
```sql
-- Hourly level
CREATE MATERIALIZED VIEW sensor_data_hourly
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 hour', time) AS time,
    sensor_id,
    AVG(temperature) AS avg_temperature,
    MIN(temperature) AS min_temperature,
    MAX(temperature) AS max_temperature,
    COUNT(*) AS count
FROM sensor_data
GROUP BY time, sensor_id;

-- Daily level (based on hourly)
CREATE MATERIALIZED VIEW sensor_data_daily
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 day', time) AS time,
    sensor_id,
    AVG(avg_temperature) AS avg_temperature,
    MIN(min_temperature) AS min_temperature,
    MAX(max_temperature) AS max_temperature,
    SUM(count) AS count
FROM sensor_data_hourly
GROUP BY time, sensor_id;

-- Weekly level (based on daily)
CREATE MATERIALIZED VIEW sensor_data_weekly
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 week', time) AS time,
    sensor_id,
    AVG(avg_temperature) AS avg_temperature,
    MIN(min_temperature) AS min_temperature,
    MAX(max_temperature) AS max_temperature,
    SUM(count) AS count
FROM sensor_data_daily
GROUP BY time, sensor_id;
```

## 10. Monitoring and Alerting

### Query Performance Monitoring
```sql
-- Enable query stats
ALTER DATABASE timeseries_db SET timescaledb.enable_telemetry = on;

-- View query statistics
SELECT * FROM pg_stat_statements WHERE query LIKE '%sensor_data%';

-- View hypertable statistics
SELECT * FROM timescaledb_information.hypertable_size;

-- View chunk statistics
SELECT
    chunk_schema,
    chunk_name,
    range_start,
    range_end,
    pg_size_pretty(pg_total_relation_size(chunk_schema || '.' || chunk_name)) as size
FROM timescaledb_information.chunks
WHERE hypertable_name = 'sensor_data'
ORDER BY range_start;
```

### Data Ingestion Monitoring
```sql
-- Monitor data ingestion rate
SELECT
    time_bucket('1 minute', time) AS bucket,
    COUNT(*) AS rows_per_minute
FROM sensor_data
WHERE time >= NOW() - INTERVAL '1 hour'
GROUP BY bucket
ORDER BY bucket;

-- Monitor data by sensor
SELECT
    sensor_id,
    COUNT(*) AS row_count,
    MIN(time) AS first_seen,
    MAX(time) AS last_seen
FROM sensor_data
WHERE time >= NOW() - INTERVAL '1 day'
GROUP BY sensor_id
ORDER BY row_count DESC;
```

### Storage Monitoring
```sql
-- View storage usage by hypertable
SELECT
    hypertable_name,
    pg_size_pretty(pg_total_relation_size(hypertable_schema || '.' || hypertable_name)) AS total_size,
    pg_size_pretty(pg_total_relation_size(hypertable_schema || '.' || hypertable_name || '_compressed')) AS compressed_size
FROM timescaledb_information.hypertables;

-- View storage usage by chunk
SELECT
    chunk_schema,
    chunk_name,
    range_start,
    range_end,
    is_compressed,
    pg_size_pretty(pg_total_relation_size(chunk_schema || '.' || chunk_name)) AS size
FROM timescaledb_information.chunks
WHERE hypertable_name = 'sensor_data'
ORDER BY range_start DESC
LIMIT 10;
```

### Alert Queries
```sql
-- Alert on missing data
SELECT
    sensor_id,
    MAX(time) AS last_data_time,
    NOW() - MAX(time) AS time_since_last_data
FROM sensor_data
GROUP BY sensor_id
HAVING NOW() - MAX(time) > INTERVAL '1 hour'
ORDER BY time_since_last_data DESC;

-- Alert on anomalous values
WITH sensor_stats AS (
    SELECT
        sensor_id,
        AVG(temperature) AS avg_temp,
        STDDEV(temperature) AS stddev_temp
    FROM sensor_data
    WHERE time >= NOW() - INTERVAL '1 day'
    GROUP BY sensor_id
)
SELECT
    sd.time,
    sd.sensor_id,
    sd.temperature,
    ss.avg_temp,
    ss.stddev_temp,
    (sd.temperature - ss.avg_temp) / ss.stddev_temp AS z_score
FROM sensor_data sd
JOIN sensor_stats ss ON sd.sensor_id = ss.sensor_id
WHERE sd.time >= NOW() - INTERVAL '1 hour'
AND ABS((sd.temperature - ss.avg_temp) / ss.stddev_temp) > 3
ORDER BY sd.time;
```

## 11. Integration with Grafana

### TimescaleDB Datasource Configuration
```typescript
// Grafana datasource configuration
{
  "name": "TimescaleDB",
  "type": "postgres",
  "url": "localhost:5432",
  "database": "timeseries_db",
  "user": "postgres",
  "password": "password",
  "sslMode": "disable",
  "timescaledb": true
}
```

### Grafana Query Examples
```sql
-- Time series query for Grafana
SELECT
    time_bucket('$__interval', time) AS time,
    sensor_id,
    AVG(temperature) AS avg_temperature
FROM sensor_data
WHERE time >= $__timeFrom() AND time <= $__timeTo()
    AND sensor_id = $sensor_id
GROUP BY time, sensor_id
ORDER BY time;

-- Multi-sensor query
SELECT
    time_bucket('$__interval', time) AS time,
    sensor_id,
    AVG(temperature) AS avg_temperature
FROM sensor_data
WHERE time >= $__timeFrom() AND time <= $__timeTo()
    AND sensor_id IN ($sensor_ids)
GROUP BY time, sensor_id
ORDER BY time;
```

## 12. Best Practices

### 1. Choose Appropriate Chunk Intervals
```sql
-- Good: Match chunk interval to data retention
SELECT create_hypertable(
    'sensor_data',
    'time',
    chunk_time_interval => interval '1 day'  -- For 30-day retention
);

-- Bad: Too small chunk interval causes overhead
SELECT create_hypertable(
    'sensor_data',
    'time',
    chunk_time_interval => interval '1 minute'  -- Too small
);
```

### 2. Use Continuous Aggregates for Pre-computed Data
```sql
-- Good: Pre-compute aggregations
CREATE MATERIALIZED VIEW sensor_hourly_avg
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 hour', time) AS bucket,
    sensor_id,
    AVG(temperature) AS avg_temperature
FROM sensor_data
GROUP BY bucket, sensor_id;

-- Bad: Compute aggregations on every query
SELECT
    time_bucket('1 hour', time) AS bucket,
    sensor_id,
    AVG(temperature) AS avg_temperature
FROM sensor_data
WHERE time >= NOW() - INTERVAL '30 days'
GROUP BY bucket, sensor_id;
```

### 3. Use Compression for Historical Data
```sql
-- Good: Compress old data
SELECT add_compression_policy(
    'sensor_data',
    INTERVAL '7 days',
    schedule_interval => INTERVAL '1 day'
);

-- Bad: Keep all data uncompressed
```

### 4. Use Appropriate Time Buckets
```sql
-- Good: Use appropriate bucket size for query
SELECT
    time_bucket('1 hour', time) AS bucket,
    AVG(temperature) AS avg_temperature
FROM sensor_data
WHERE time >= NOW() - INTERVAL '1 day'
GROUP BY bucket;

-- Bad: Use too small bucket for large time range
SELECT
    time_bucket('1 second', time) AS bucket,
    AVG(temperature) AS avg_temperature
FROM sensor_data
WHERE time >= NOW() - INTERVAL '30 days'
GROUP BY bucket;
```

### 5. Use Indexes Wisely
```sql
-- Good: Create indexes on frequently queried columns
CREATE INDEX idx_sensor_data_sensor_id ON sensor_data(sensor_id);
CREATE INDEX idx_sensor_data_time ON sensor_data(time DESC);

-- Bad: Create too many indexes
```

### 6. Monitor Performance
```sql
-- Regularly monitor query performance
SELECT * FROM pg_stat_statements
WHERE query LIKE '%sensor_data%'
ORDER BY total_time DESC
LIMIT 10;
```

### 7. Use Partitioning for Large Datasets
```sql
-- Good: Use multiple dimensions for partitioning
SELECT create_hypertable(
    'iot_metrics',
    'time',
    partitioning_column => 'device_id',
    number_partitions => 4
);

-- Bad: Use only time partitioning for multi-tenant data
```
