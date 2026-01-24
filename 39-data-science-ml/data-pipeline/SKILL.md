---
name: Data Pipeline
description: Automating the flow of data from sources to destinations using ETL/ELT patterns, Apache Airflow orchestration, data transformation, and best practices for scalable data pipelines.
---

# Data Pipeline

> **Current Level:** Advanced  
> **Domain:** Data Engineering / ETL

---

## Overview

Data pipelines automate the flow of data from sources to destinations. This guide covers ETL/ELT, Apache Airflow, orchestration, and best practices for building reliable, scalable data pipelines that process and transform data efficiently.

## Data Pipeline Architecture

```
Data Sources → Extract → Transform → Load → Data Warehouse → Analytics
```

**Components:**
- **Sources**: Databases, APIs, files, streams
- **Extract**: Pull data from sources
- **Transform**: Clean, enrich, aggregate
- **Load**: Store in destination
- **Orchestration**: Schedule and monitor

## ETL vs ELT

| Aspect | ETL | ELT |
|--------|-----|-----|
| **Transform** | Before loading | After loading |
| **Processing** | External tool | Data warehouse |
| **Speed** | Slower | Faster |
| **Cost** | Higher compute | Higher storage |
| **Use Case** | Legacy systems | Modern cloud DWH |

## Apache Airflow

### Installation

```bash
pip install apache-airflow
airflow db init
airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com
airflow webserver -p 8080
airflow scheduler
```

### DAG Definition

```python
# dags/data_pipeline.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email': ['alerts@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'data_pipeline',
    default_args=default_args,
    description='Daily data pipeline',
    schedule_interval='0 2 * * *',  # 2 AM daily
    catchup=False,
    tags=['data', 'etl']
)

def extract_data(**context):
    """Extract data from source"""
    import pandas as pd
    import requests
    
    # Extract from API
    response = requests.get('https://api.example.com/data')
    data = response.json()
    
    # Save to temporary location
    df = pd.DataFrame(data)
    df.to_csv('/tmp/extracted_data.csv', index=False)
    
    # Push metadata to XCom
    context['ti'].xcom_push(key='row_count', value=len(df))

def transform_data(**context):
    """Transform extracted data"""
    import pandas as pd
    
    # Load extracted data
    df = pd.read_csv('/tmp/extracted_data.csv')
    
    # Data cleaning
    df = df.dropna()
    df = df.drop_duplicates()
    
    # Data transformation
    df['created_date'] = pd.to_datetime(df['created_at']).dt.date
    df['amount_usd'] = df['amount'] * df['exchange_rate']
    
    # Aggregation
    daily_summary = df.groupby('created_date').agg({
        'amount_usd': 'sum',
        'transaction_id': 'count'
    }).reset_index()
    
    # Save transformed data
    daily_summary.to_csv('/tmp/transformed_data.csv', index=False)
    
    context['ti'].xcom_push(key='transformed_rows', value=len(daily_summary))

def load_data(**context):
    """Load data to warehouse"""
    import pandas as pd
    from sqlalchemy import create_engine
    
    # Load transformed data
    df = pd.read_csv('/tmp/transformed_data.csv')
    
    # Connect to warehouse
    engine = create_engine('postgresql://user:pass@localhost:5432/warehouse')
    
    # Load to database
    df.to_sql('daily_transactions', engine, if_exists='append', index=False)
    
    print(f"Loaded {len(df)} rows to warehouse")

# Define tasks
extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag
)

quality_check = PostgresOperator(
    task_id='data_quality_check',
    postgres_conn_id='warehouse',
    sql="""
        SELECT COUNT(*) as row_count
        FROM daily_transactions
        WHERE created_date = CURRENT_DATE - INTERVAL '1 day'
        HAVING COUNT(*) > 0
    """,
    dag=dag
)

# Set dependencies
extract_task >> transform_task >> load_task >> quality_check
```

### Operators

```python
# Common Airflow operators
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.email import EmailOperator
from airflow.sensors.filesystem import FileSensor

# Python operator
python_task = PythonOperator(
    task_id='run_python',
    python_callable=my_function,
    op_kwargs={'param1': 'value1'}
)

# Bash operator
bash_task = BashOperator(
    task_id='run_script',
    bash_command='python /scripts/process.py'
)

# SQL operator
sql_task = PostgresOperator(
    task_id='run_query',
    postgres_conn_id='my_postgres',
    sql='SELECT * FROM users WHERE created_at > {{ ds }}'
)

# HTTP operator
api_task = SimpleHttpOperator(
    task_id='call_api',
    http_conn_id='my_api',
    endpoint='/data',
    method='GET'
)

# File sensor (wait for file)
file_sensor = FileSensor(
    task_id='wait_for_file',
    filepath='/data/input.csv',
    poke_interval=60,
    timeout=3600
)
```

### Scheduling

```python
# Cron expressions
dag_configs = {
    'hourly': '0 * * * *',
    'daily_2am': '0 2 * * *',
    'weekly_monday': '0 0 * * 1',
    'monthly_1st': '0 0 1 * *',
    'every_15min': '*/15 * * * *'
}

# Dynamic scheduling
from airflow.timetables.interval import CronDataIntervalTimetable

dag = DAG(
    'dynamic_schedule',
    schedule=CronDataIntervalTimetable('0 2 * * *', timezone='UTC'),
    start_date=datetime(2024, 1, 1)
)

# Conditional scheduling
from airflow.operators.python import BranchPythonOperator

def decide_branch(**context):
    """Decide which branch to take"""
    execution_date = context['execution_date']
    
    if execution_date.weekday() == 0:  # Monday
        return 'weekly_task'
    else:
        return 'daily_task'

branch_task = BranchPythonOperator(
    task_id='branch',
    python_callable=decide_branch
)
```

## Data Extraction

```python
# Extract from various sources
import pandas as pd
import requests
from sqlalchemy import create_engine

class DataExtractor:
    def extract_from_api(self, url: str, params: dict = None) -> pd.DataFrame:
        """Extract data from REST API"""
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        return pd.DataFrame(data)
    
    def extract_from_database(self, query: str, connection_string: str) -> pd.DataFrame:
        """Extract data from database"""
        engine = create_engine(connection_string)
        return pd.read_sql(query, engine)
    
    def extract_from_csv(self, filepath: str) -> pd.DataFrame:
        """Extract data from CSV file"""
        return pd.read_csv(filepath)
    
    def extract_from_s3(self, bucket: str, key: str) -> pd.DataFrame:
        """Extract data from S3"""
        import boto3
        
        s3 = boto3.client('s3')
        obj = s3.get_object(Bucket=bucket, Key=key)
        
        return pd.read_csv(obj['Body'])
    
    def extract_incremental(
        self,
        query: str,
        connection_string: str,
        last_updated: str
    ) -> pd.DataFrame:
        """Extract only new/updated records"""
        query_with_filter = f"{query} WHERE updated_at > '{last_updated}'"
        
        engine = create_engine(connection_string)
        return pd.read_sql(query_with_filter, engine)
```

## Data Transformation

```python
# Data transformation functions
class DataTransformer:
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean data"""
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Handle missing values
        df = df.fillna({
            'numeric_col': 0,
            'string_col': 'Unknown'
        })
        
        # Remove outliers
        df = self.remove_outliers(df, 'amount', threshold=3)
        
        return df
    
    def remove_outliers(
        self,
        df: pd.DataFrame,
        column: str,
        threshold: float = 3
    ) -> pd.DataFrame:
        """Remove outliers using z-score"""
        from scipy import stats
        
        z_scores = stats.zscore(df[column])
        return df[abs(z_scores) < threshold]
    
    def enrich_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Enrich data with additional features"""
        # Add derived columns
        df['year'] = pd.to_datetime(df['date']).dt.year
        df['month'] = pd.to_datetime(df['date']).dt.month
        df['day_of_week'] = pd.to_datetime(df['date']).dt.dayofweek
        
        # Add calculated fields
        df['profit_margin'] = (df['revenue'] - df['cost']) / df['revenue']
        
        return df
    
    def aggregate_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aggregate data"""
        return df.groupby(['date', 'category']).agg({
            'amount': ['sum', 'mean', 'count'],
            'quantity': 'sum'
        }).reset_index()
```

## Data Loading

```python
# Load data to various destinations
class DataLoader:
    def load_to_postgres(
        self,
        df: pd.DataFrame,
        table_name: str,
        connection_string: str,
        if_exists: str = 'append'
    ):
        """Load data to PostgreSQL"""
        from sqlalchemy import create_engine
        
        engine = create_engine(connection_string)
        df.to_sql(table_name, engine, if_exists=if_exists, index=False)
    
    def load_to_s3(
        self,
        df: pd.DataFrame,
        bucket: str,
        key: str
    ):
        """Load data to S3"""
        import boto3
        from io import StringIO
        
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        
        s3 = boto3.client('s3')
        s3.put_object(Bucket=bucket, Key=key, Body=csv_buffer.getvalue())
    
    def load_to_bigquery(
        self,
        df: pd.DataFrame,
        table_id: str,
        project_id: str
    ):
        """Load data to BigQuery"""
        from google.cloud import bigquery
        
        client = bigquery.Client(project=project_id)
        
        job_config = bigquery.LoadJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND
        )
        
        job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
        job.result()
```

## Error Handling

```python
# Error handling in Airflow
from airflow.exceptions import AirflowException

def robust_task(**context):
    """Task with error handling"""
    try:
        # Main logic
        result = process_data()
        
        # Validate result
        if not validate_result(result):
            raise AirflowException("Data validation failed")
        
        return result
        
    except Exception as e:
        # Log error
        print(f"Error in task: {str(e)}")
        
        # Send alert
        send_alert(f"Pipeline failed: {str(e)}")
        
        # Re-raise to mark task as failed
        raise

def on_failure_callback(context):
    """Callback on task failure"""
    task_instance = context['task_instance']
    exception = context.get('exception')
    
    # Send notification
    send_slack_message(
        f"Task {task_instance.task_id} failed: {exception}"
    )

task = PythonOperator(
    task_id='robust_task',
    python_callable=robust_task,
    on_failure_callback=on_failure_callback
)
```

## Data Quality Checks

```python
# Data quality validation
class DataQualityChecker:
    def check_completeness(self, df: pd.DataFrame, required_columns: list) -> bool:
        """Check if all required columns exist"""
        return all(col in df.columns for col in required_columns)
    
    def check_nulls(self, df: pd.DataFrame, columns: list, threshold: float = 0.1) -> bool:
        """Check null percentage"""
        for col in columns:
            null_pct = df[col].isnull().sum() / len(df)
            if null_pct > threshold:
                return False
        return True
    
    def check_duplicates(self, df: pd.DataFrame, subset: list = None) -> bool:
        """Check for duplicates"""
        return not df.duplicated(subset=subset).any()
    
    def check_schema(self, df: pd.DataFrame, expected_schema: dict) -> bool:
        """Check data types"""
        for col, dtype in expected_schema.items():
            if df[col].dtype != dtype:
                return False
        return True
    
    def check_range(self, df: pd.DataFrame, column: str, min_val: float, max_val: float) -> bool:
        """Check value range"""
        return df[column].between(min_val, max_val).all()
```

## Alternative Tools

### Prefect

```python
# Prefect flow
from prefect import flow, task
from datetime import timedelta

@task(retries=3, retry_delay_seconds=60)
def extract():
    """Extract data"""
    return extract_data_from_source()

@task
def transform(data):
    """Transform data"""
    return transform_data(data)

@task
def load(data):
    """Load data"""
    load_to_warehouse(data)

@flow(name="data-pipeline")
def data_pipeline():
    """Main pipeline flow"""
    data = extract()
    transformed = transform(data)
    load(transformed)

if __name__ == "__main__":
    data_pipeline()
```

### Dagster

```python
# Dagster pipeline
from dagster import asset, AssetExecutionContext

@asset
def extract_data(context: AssetExecutionContext):
    """Extract data asset"""
    context.log.info("Extracting data...")
    return extract_from_source()

@asset
def transform_data(context: AssetExecutionContext, extract_data):
    """Transform data asset"""
    context.log.info("Transforming data...")
    return transform(extract_data)

@asset
def load_data(context: AssetExecutionContext, transform_data):
    """Load data asset"""
    context.log.info("Loading data...")
    load_to_warehouse(transform_data)
```

## Best Practices

1. **Idempotency** - Make tasks idempotent
2. **Incremental** - Use incremental loads when possible
3. **Monitoring** - Monitor pipeline health
4. **Error Handling** - Handle errors gracefully
5. **Data Quality** - Validate data quality
6. **Documentation** - Document pipeline logic
7. **Testing** - Test pipelines before production
8. **Versioning** - Version control DAGs
9. **Scheduling** - Choose appropriate schedules
10. **Alerting** - Set up failure alerts

---

## Quick Start

### Airflow DAG

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def extract_data():
    # Extract from source
    pass

def transform_data():
    # Transform data
    pass

def load_data():
    # Load to destination
    pass

dag = DAG(
    'data_pipeline',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily'
)

extract_task = PythonOperator(
    task_id='extract',
    python_callable=extract_data,
    dag=dag
)

transform_task = PythonOperator(
    task_id='transform',
    python_callable=transform_data,
    dag=dag
)

load_task = PythonOperator(
    task_id='load',
    python_callable=load_data,
    dag=dag
)

extract_task >> transform_task >> load_task
```

---

## Production Checklist

- [ ] **Pipeline Design**: Design pipeline architecture
- [ ] **Orchestration**: Set up orchestration (Airflow, etc.)
- [ ] **ETL/ELT**: Choose ETL or ELT pattern
- [ ] **Error Handling**: Comprehensive error handling
- [ ] **Retry Logic**: Retry failed tasks
- [ ] **Data Quality**: Validate data quality
- [ ] **Documentation**: Document pipeline logic
- [ ] **Testing**: Test pipelines before production
- [ ] **Versioning**: Version control DAGs
- [ ] **Scheduling**: Appropriate schedules
- [ ] **Alerting**: Failure alerts
- [ ] **Monitoring**: Monitor pipeline health

---

## Anti-patterns

### ❌ Don't: No Error Handling

```python
# ❌ Bad - No error handling
def extract_data():
    data = fetch_from_api()  # What if fails?
    return data
```

```python
# ✅ Good - Error handling
def extract_data():
    try:
        data = fetch_from_api()
        return data
    except Exception as e:
        logger.error(f"Extract failed: {e}")
        send_alert("Extract failed")
        raise
```

### ❌ Don't: No Data Validation

```python
# ❌ Bad - No validation
def transform_data(data):
    return process(data)  # Invalid data possible!
```

```python
# ✅ Good - Validate
def transform_data(data):
    if not validate_data(data):
        raise ValueError("Invalid data")
    return process(data)
```

---

## Integration Points

- **Feature Engineering** (`39-data-science-ml/feature-engineering/`) - Feature pipelines
- **Model Training** (`05-ai-ml-core/model-training/`) - Training pipelines
- **CI/CD** (`15-devops-infrastructure/ci-cd-github-actions/`) - Pipeline automation

---

## Further Reading

- [Apache Airflow](https://airflow.apache.org/)
- [Data Pipeline Best Practices](https://www.astronomer.io/guides/data-pipeline-best-practices)

## Resources
- [Prefect](https://www.prefect.io/)
- [Dagster](https://dagster.io/)
- [dbt](https://www.getdbt.com/)
