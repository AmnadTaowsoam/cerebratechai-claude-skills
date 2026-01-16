# Kafka Streams

## Overview

Comprehensive guide to Apache Kafka patterns and Kafka Streams for real-time data processing.

## Table of Contents

1. [Kafka Concepts](#kafka-concepts)
2. [Producers](#producers)
3. [Consumers](#consumers)
4. [Topics and Partitions](#topics-and-partitions)
5. [Consumer Groups](#consumer-groups)
6. [Kafka Streams](#kafka-streams)
7. [Error Handling](#error-handling)
8. [Exactly-Once Semantics](#exactly-once-semantics)
9. [Performance Tuning](#performance-tuning)
10. [Monitoring](#monitoring)

---

## Kafka Concepts

### Core Concepts

```python
# Kafka Core Concepts
"""
- Broker: Kafka server that stores and serves data
- Topic: Category/feed name to which records are published
- Partition: Topic is divided into partitions for parallelism
- Producer: Application that publishes records to topics
- Consumer: Application that subscribes to topics and processes records
- Consumer Group: Group of consumers that work together to consume a topic
- Offset: Unique identifier for each record within a partition
- Commit: Storing the current offset for a consumer
"""
```

### Basic Setup (Python)

```python
# kafka_config.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class KafkaConfig:
    bootstrap_servers: str = 'localhost:9092'
    group_id: str = 'default-group'
    auto_offset_reset: str = 'earliest'
    enable_auto_commit: bool = True
    auto_commit_interval_ms: int = 5000
    session_timeout_ms: int = 30000
    heartbeat_interval_ms: int = 3000
    max_poll_records: int = 500
    max_poll_interval_ms: int = 300000

# Default configuration
DEFAULT_CONFIG = KafkaConfig()

# Production configuration
PRODUCTION_CONFIG = KafkaConfig(
    bootstrap_servers='kafka-broker-1:9092,kafka-broker-2:9092,kafka-broker-3:9092',
    group_id='production-group',
    enable_auto_commit=False,  # Manual commit for reliability
    max_poll_records=100,
    max_poll_interval_ms=600000
)
```

---

## Producers

### Basic Producer

```python
# producer.py
from kafka import KafkaProducer
import json
import logging

class KafkaMessageProducer:
    def __init__(self, config: KafkaConfig):
        self.producer = KafkaProducer(
            bootstrap_servers=config.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: str(k).encode('utf-8') if k else None,
            acks='all',  # Wait for all replicas
            retries=3,
            compression_type='gzip',
            batch_size=16384,
            linger_ms=10
        )
    
    def send(
        self,
        topic: str,
        value: dict,
        key: str = None,
        headers: dict = None
    ) -> None:
        """Send message to Kafka topic"""
        try:
            future = self.producer.send(
                topic,
                value=value,
                key=key,
                headers=[(k, v.encode()) for k, v in (headers or {}).items()]
            )
            
            # Wait for delivery report
            record_metadata = future.get(timeout=10)
            logging.info(
                f"Message sent to {record_metadata.topic} "
                f"[partition: {record_metadata.partition}, offset: {record_metadata.offset}]"
            )
        except Exception as e:
            logging.error(f"Failed to send message: {e}")
            raise
    
    def send_async(
        self,
        topic: str,
        value: dict,
        key: str = None,
        callback: callable = None
    ) -> None:
        """Send message asynchronously"""
        def delivery_report(error, record_metadata):
            if error:
                logging.error(f"Message delivery failed: {error}")
            else:
                logging.info(f"Message delivered: {record_metadata}")
                if callback:
                    callback(record_metadata)
        
        self.producer.send(
            topic,
            value=value,
            key=key
        ).add_callback(delivery_report)
    
    def flush(self) -> None:
        """Flush all pending messages"""
        self.producer.flush()
    
    def close(self) -> None:
        """Close producer"""
        self.producer.close()

# Usage
producer = KafkaMessageProducer(DEFAULT_CONFIG)
producer.send('events', {'event': 'user_login', 'user_id': 123}, key='user_123')
producer.flush()
producer.close()
```

### Transactional Producer

```python
# transactional_producer.py
from kafka import KafkaProducer
import json

class TransactionalProducer:
    def __init__(self, config: KafkaConfig, transactional_id: str):
        self.producer = KafkaProducer(
            bootstrap_servers=config.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            transactional_id=transactional_id,
            enable_idempotence=True
        )
        # Initialize transactions
        self.producer.init_transactions()
    
    def send_in_transaction(
        self,
        messages: list,
        input_topic: str,
        output_topic: str
    ) -> None:
        """Send multiple messages in a transaction"""
        try:
            # Begin transaction
            self.producer.begin_transaction()
            
            # Consume from input topic (for processing)
            # Process messages
            # Send to output topic
            for message in messages:
                self.producer.send(output_topic, value=message)
            
            # Commit transaction
            self.producer.commit_transaction()
        except Exception as e:
            # Abort transaction on error
            self.producer.abort_transaction()
            raise
    
    def close(self) -> None:
        self.producer.close()
```

---

## Consumers

### Basic Consumer

```python
# consumer.py
from kafka import KafkaConsumer
import json
import logging

class KafkaMessageConsumer:
    def __init__(self, config: KafkaConfig, topics: list):
        self.consumer = KafkaConsumer(
            *topics,
            bootstrap_servers=config.bootstrap_servers,
            group_id=config.group_id,
            auto_offset_reset=config.auto_offset_reset,
            enable_auto_commit=config.enable_auto_commit,
            auto_commit_interval_ms=config.auto_commit_interval_ms,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            key_deserializer=lambda m: m.decode('utf-8') if m else None,
            session_timeout_ms=config.session_timeout_ms,
            heartbeat_interval_ms=config.heartbeat_interval_ms,
            max_poll_records=config.max_poll_records,
            max_poll_interval_ms=config.max_poll_interval_ms
        )
    
    def consume(self, handler: callable) -> None:
        """Consume messages and process with handler"""
        try:
            for message in self.consumer:
                try:
                    # Process message
                    result = handler(message)
                    
                    # Manual commit if auto-commit is disabled
                    if not self.consumer.config['enable_auto_commit']:
                        self.consumer.commit()
                    
                    logging.info(f"Processed message: {message.offset}")
                except Exception as e:
                    logging.error(f"Error processing message: {e}")
                    # Skip problematic message
                    if not self.consumer.config['enable_auto_commit']:
                        self.consumer.commit()
        except KeyboardInterrupt:
            logging.info("Stopping consumer...")
        finally:
            self.close()
    
    def consume_batch(self, handler: callable, batch_size: int = 10) -> None:
        """Consume messages in batches"""
        batch = []
        
        try:
            for message in self.consumer:
                batch.append(message)
                
                if len(batch) >= batch_size:
                    # Process batch
                    handler(batch)
                    
                    # Commit batch
                    self.consumer.commit()
                    batch = []
        finally:
            # Process remaining messages
            if batch:
                handler(batch)
                self.consumer.commit()
            self.close()
    
    def seek_to_beginning(self, topic: str, partition: int) -> None:
        """Seek to beginning of partition"""
        self.consumer.seek_to_beginning({partition: topic})
    
    def seek_to_end(self, topic: str, partition: int) -> None:
        """Seek to end of partition"""
        self.consumer.seek_to_end({partition: topic})
    
    def close(self) -> None:
        """Close consumer"""
        self.consumer.close()

# Usage
def message_handler(message):
    print(f"Received: {message.value}")
    return True

consumer = KafkaMessageConsumer(DEFAULT_CONFIG, ['events'])
consumer.consume(message_handler)
```

### Rebalancing Listener

```python
# rebalancing_consumer.py
from kafka import KafkaConsumer
from kafka.coordinator.assignor import RoundRobinPartitionAssignor
import logging

class RebalancingConsumer(KafkaMessageConsumer):
    def __init__(self, config: KafkaConfig, topics: list):
        super().__init__(config, topics)
        self.consumer.subscribe(
            topics,
            listener=self.RebalanceListener(self)
        )
    
    class RebalanceListener:
        def __init__(self, outer):
            self.outer = outer
        
        def on_partitions_revoked(self, revoked):
            """Called before partition rebalance"""
            logging.info(f"Partitions revoked: {revoked}")
            # Commit offsets before losing partitions
            self.outer.consumer.commit()
        
        def on_partitions_assigned(self, assigned):
            """Called after partition rebalance"""
            logging.info(f"Partitions assigned: {assigned}")
```

---

## Topics and Partitions

### Topic Management

```python
# topic_management.py
from kafka import KafkaAdminClient
from kafka.admin import ConfigResource, ConfigResourceType, NewTopic
import logging

class TopicManager:
    def __init__(self, config: KafkaConfig):
        self.admin_client = KafkaAdminClient(
            bootstrap_servers=config.bootstrap_servers
        )
    
    def create_topic(
        self,
        topic_name: str,
        num_partitions: int = 3,
        replication_factor: int = 1,
        config: dict = None
    ) -> None:
        """Create a new topic"""
        topic = NewTopic(
            name=topic_name,
            num_partitions=num_partitions,
            replication_factor=replication_factor
        )
        
        if config:
            topic.topic_configs = config
        
        try:
            future = self.admin_client.create_topics([topic])
            for topic_name, future_result in future.items():
                try:
                    future_result.result()
                    logging.info(f"Topic {topic_name} created successfully")
                except Exception as e:
                    logging.error(f"Failed to create topic {topic_name}: {e}")
        except Exception as e:
            logging.error(f"Error creating topic: {e}")
    
    def delete_topic(self, topic_name: str) -> None:
        """Delete a topic"""
        try:
            future = self.admin_client.delete_topics([topic_name])
            for topic, future_result in future.items():
                future_result.result()
                logging.info(f"Topic {topic} deleted successfully")
        except Exception as e:
            logging.error(f"Error deleting topic: {e}")
    
    def list_topics(self) -> list:
        """List all topics"""
        return list(self.admin_client.list_topics().keys())
    
    def describe_topic(self, topic_name: str) -> dict:
        """Get topic metadata"""
        metadata = self.admin_client.describe_topics([topic_name])
        return metadata[topic_name]
    
    def alter_topic_config(self, topic_name: str, config: dict) -> None:
        """Alter topic configuration"""
        resource = ConfigResource(ConfigResourceType.TOPIC, topic_name)
        future = self.admin_client.alter_configs({
            resource: config
        })
        
        for resource, future_result in future.items():
            future_result.result()
    
    def close(self) -> None:
        self.admin_client.close()

# Usage
topic_manager = TopicManager(DEFAULT_CONFIG)

# Create topic with retention
topic_manager.create_topic(
    'user-events',
    num_partitions=6,
    replication_factor=3,
    config={
        'retention.ms': '604800000',  # 7 days
        'segment.ms': '86400000',      # 1 day
        'cleanup.policy': 'delete'
    }
)
```

### Partition Management

```python
# partition_management.py
from kafka import KafkaConsumer
import logging

class PartitionManager:
    def __init__(self, config: KafkaConfig):
        self.config = config
    
    def get_partition_count(self, topic: str) -> int:
        """Get number of partitions for a topic"""
        consumer = KafkaConsumer(
            bootstrap_servers=self.config.bootstrap_servers
        )
        partitions = consumer.partitions_for_topic(topic)
        consumer.close()
        return len(partitions) if partitions else 0
    
    def get_partition_info(self, topic: str) -> dict:
        """Get information about topic partitions"""
        consumer = KafkaConsumer(
            bootstrap_servers=self.config.bootstrap_servers
        )
        partitions = consumer.partitions_for_topic(topic)
        
        info = {}
        for partition in partitions:
            tp = (topic, partition)
            beginning_offset = consumer.beginning_offsets([tp])[tp]
            end_offset = consumer.end_offsets([tp])[tp]
            
            info[partition] = {
                'beginning_offset': beginning_offset,
                'end_offset': end_offset,
                'message_count': end_offset - beginning_offset
            }
        
        consumer.close()
        return info
    
    def get_consumer_offsets(self, topic: str, group_id: str) -> dict:
        """Get consumer group offsets for topic"""
        from kafka import KafkaAdminClient
        
        admin_client = KafkaAdminClient(
            bootstrap_servers=self.config.bootstrap_servers
        )
        
        offsets = admin_client.list_consumer_group_offsets(group_id)
        consumer_offsets = {}
        
        for tp, offset_info in offsets.items():
            if tp.topic == topic:
                consumer_offsets[tp.partition] = {
                    'offset': offset_info.offset,
                    'metadata': offset_info.metadata
                }
        
        admin_client.close()
        return consumer_offsets

# Usage
partition_manager = PartitionManager(DEFAULT_CONFIG)
print(partition_manager.get_partition_info('user-events'))
```

---

## Consumer Groups

### Consumer Group Management

```python
# consumer_group.py
from kafka import KafkaAdminClient
from kafka.admin import NewTopic
import logging

class ConsumerGroupManager:
    def __init__(self, config: KafkaConfig):
        self.admin_client = KafkaAdminClient(
            bootstrap_servers=config.bootstrap_servers
        )
    
    def list_consumer_groups(self) -> list:
        """List all consumer groups"""
        return list(self.admin_client.list_consumer_groups().keys())
    
    def describe_consumer_group(self, group_id: str) -> dict:
        """Describe consumer group details"""
        return self.admin_client.describe_consumer_groups([group_id])[group_id]
    
    def delete_consumer_group(self, group_id: str) -> None:
        """Delete consumer group"""
        try:
            self.admin_client.delete_consumer_groups([group_id])
            logging.info(f"Consumer group {group_id} deleted")
        except Exception as e:
            logging.error(f"Error deleting consumer group: {e}")
    
    def reset_consumer_group_offset(
        self,
        group_id: str,
        topic: str,
        partition: int,
        new_offset: int
    ) -> None:
        """Reset consumer group offset to specific position"""
        from kafka import KafkaConsumer
        
        consumer = KafkaConsumer(
            bootstrap_servers=self.config.bootstrap_servers,
            group_id=group_id,
            enable_auto_commit=False
        )
        
        tp = (topic, partition)
        consumer.seek(tp, new_offset)
        consumer.commit()
        consumer.close()
    
    def reset_to_earliest(self, group_id: str, topic: str) -> None:
        """Reset consumer group to earliest offset"""
        from kafka import KafkaConsumer
        
        consumer = KafkaConsumer(
            bootstrap_servers=self.config.bootstrap_servers,
            group_id=group_id,
            enable_auto_commit=False
        )
        
        partitions = consumer.partitions_for_topic(topic)
        for partition in partitions:
            tp = (topic, partition)
            beginning_offset = consumer.beginning_offsets([tp])[tp]
            consumer.seek(tp, beginning_offset)
        
        consumer.commit()
        consumer.close()
    
    def close(self) -> None:
        self.admin_client.close()
```

---

## Kafka Streams

### Stream Processing with Python

```python
# kafka_streams.py
from kafka import KafkaConsumer, KafkaProducer
import json
import threading
import logging

class KafkaStreamProcessor:
    def __init__(
        self,
        input_topic: str,
        output_topic: str,
        config: KafkaConfig
    ):
        self.input_topic = input_topic
        self.output_topic = output_topic
        self.config = config
        
        self.consumer = KafkaConsumer(
            input_topic,
            bootstrap_servers=config.bootstrap_servers,
            group_id=f"{config.group_id}-processor",
            auto_offset_reset='earliest',
            enable_auto_commit=False,
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        
        self.producer = KafkaProducer(
            bootstrap_servers=config.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
    
    def process_stream(self, processor: callable) -> None:
        """Process stream of messages"""
        try:
            for message in self.consumer:
                try:
                    # Process message
                    result = processor(message.value)
                    
                    # Send to output topic
                    self.producer.send(self.output_topic, value=result)
                    
                    # Commit offset
                    self.consumer.commit()
                    
                    logging.info(f"Processed message: {message.offset}")
                except Exception as e:
                    logging.error(f"Error processing message: {e}")
        except KeyboardInterrupt:
            logging.info("Stopping stream processor...")
        finally:
            self.close()
    
    def aggregate_stream(
        self,
        window_size_ms: int,
        processor: callable
    ) -> None:
        """Aggregate messages within time window"""
        window = []
        last_flush_time = None
        
        try:
            for message in self.consumer:
                try:
                    window.append(message.value)
                    
                    current_time = message.timestamp
                    if last_flush_time is None:
                        last_flush_time = current_time
                    
                    # Flush window if time exceeded
                    if current_time - last_flush_time >= window_size_ms:
                        # Process window
                        result = processor(window)
                        self.producer.send(self.output_topic, value=result)
                        
                        # Clear window
                        window = []
                        last_flush_time = current_time
                        
                        # Commit offset
                        self.consumer.commit()
                except Exception as e:
                    logging.error(f"Error in aggregation: {e}")
        finally:
            # Flush remaining messages
            if window:
                result = processor(window)
                self.producer.send(self.output_topic, value=result)
            self.close()
    
    def close(self) -> None:
        """Close consumer and producer"""
        self.consumer.close()
        self.producer.close()

# Example processors
def uppercase_processor(message):
    """Convert text to uppercase"""
    message['text'] = message.get('text', '').upper()
    return message

def count_aggregator(messages):
    """Count messages in window"""
    return {
        'count': len(messages),
        'window_start': messages[0].get('timestamp'),
        'window_end': messages[-1].get('timestamp')
    }

# Usage
processor = KafkaStreamProcessor('input-topic', 'output-topic', DEFAULT_CONFIG)
processor.process_stream(uppercase_processor)
```

---

## Error Handling

### Error Handling Strategies

```python
# error_handling.py
from kafka import KafkaConsumer, KafkaProducer
import json
import logging
import time

class ResilientConsumer:
    def __init__(self, config: KafkaConfig, topics: list):
        self.config = config
        self.topics = topics
        self.max_retries = 3
        self.retry_delay = 1000  # ms
    
    def consume_with_retry(self, handler: callable) -> None:
        """Consume with retry logic"""
        retry_count = 0
        
        while retry_count < self.max_retries:
            try:
                consumer = KafkaConsumer(
                    *self.topics,
                    bootstrap_servers=self.config.bootstrap_servers,
                    group_id=self.config.group_id,
                    auto_offset_reset=self.config.auto_offset_reset,
                    enable_auto_commit=False,
                    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
                )
                
                for message in consumer:
                    try:
                        handler(message)
                        consumer.commit()
                        retry_count = 0  # Reset on success
                    except Exception as e:
                        logging.error(f"Processing error: {e}")
                        # Don't commit, message will be redelivered
                
                break
                
            except Exception as e:
                retry_count += 1
                logging.error(f"Consumer error (attempt {retry_count}): {e}")
                
                if retry_count < self.max_retries:
                    time.sleep(self.retry_delay * retry_count)
                else:
                    logging.error("Max retries exceeded, giving up")
                    raise

class DeadLetterProducer:
    def __init__(self, config: KafkaConfig, dlq_topic: str):
        self.producer = KafkaProducer(
            bootstrap_servers=config.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.dlq_topic = dlq_topic
    
    def send_to_dlq(self, original_message: dict, error: Exception) -> None:
        """Send failed message to dead letter queue"""
        dlq_message = {
            'original_message': original_message,
            'error': str(error),
            'timestamp': time.time() * 1000
        }
        self.producer.send(self.dlq_topic, value=dlq_message)
        self.producer.flush()
```

---

## Exactly-Once Semantics

### Exactly-Once Processing

```python
# exactly_once.py
from kafka import KafkaProducer
import json

class ExactlyOnceProcessor:
    def __init__(
        self,
        config: KafkaConfig,
        input_topic: str,
        output_topic: str,
        transactional_id: str
    ):
        self.input_topic = input_topic
        self.output_topic = output_topic
        
        # Configure producer for exactly-once
        self.producer = KafkaProducer(
            bootstrap_servers=config.bootstrap_servers,
            transactional_id=transactional_id,
            enable_idempotence=True,
            acks='all',
            max_in_flight_requests_per_connection=1,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        
        # Initialize transactions
        self.producer.init_transactions()
    
    def process_exactly_once(self, messages: list, processor: callable) -> None:
        """Process messages with exactly-once semantics"""
        try:
            # Begin transaction
            self.producer.begin_transaction()
            
            # Process messages
            for message in messages:
                result = processor(message)
                self.producer.send(self.output_topic, value=result)
            
            # Commit transaction
            self.producer.commit_transaction()
        except Exception as e:
            # Abort transaction on error
            self.producer.abort_transaction()
            raise
    
    def close(self) -> None:
        self.producer.close()
```

---

## Performance Tuning

### Producer Tuning

```python
# producer_tuning.py
from kafka import KafkaProducer
import json

class TunedProducer:
    def __init__(self, config: KafkaConfig):
        self.producer = KafkaProducer(
            bootstrap_servers=config.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            
            # Batching
            batch_size=32768,        # 32 KB
            linger_ms=10,              # Wait up to 10ms for batch
            
            # Compression
            compression_type='lz4',   # LZ4 for balance of speed/compression
            
            # Reliability
            acks='all',               # Wait for all replicas
            retries=3,
            max_in_flight_requests_per_connection=5,
            
            # Buffering
            buffer_memory=67108864,   # 64 MB buffer
            
            # Idempotence
            enable_idempotence=True,
            
            # Timeout
            request_timeout_ms=30000,
            metadata_fetch_timeout_ms=5000
        )
```

### Consumer Tuning

```python
# consumer_tuning.py
from kafka import KafkaConsumer
import json

class TunedConsumer:
    def __init__(self, config: KafkaConfig, topics: list):
        self.consumer = KafkaConsumer(
            *topics,
            bootstrap_servers=config.bootstrap_servers,
            group_id=config.group_id,
            
            # Fetch settings
            fetch_min_bytes=1,
            fetch_max_wait_ms=500,
            fetch_max_bytes=52428800,   # 50 MB
            
            # Session settings
            session_timeout_ms=30000,
            heartbeat_interval_ms=3000,
            max_poll_interval_ms=300000,
            
            # Poll settings
            max_poll_records=500,
            max_partition_fetch_bytes=1048576,  # 1 MB
            
            # Offset management
            enable_auto_commit=False,
            auto_offset_reset='earliest',
            
            # Network
            connections_max_idle_ms=540000,
            
            # Deserialization
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
```

---

## Monitoring

### Metrics Collection

```python
# monitoring.py
from kafka import KafkaConsumer
import time

class KafkaMonitor:
    def __init__(self, config: KafkaConfig):
        self.config = config
    
    def get_consumer_lag(self, topic: str, group_id: str) -> dict:
        """Get consumer lag for topic"""
        consumer = KafkaConsumer(
            bootstrap_servers=self.config.bootstrap_servers,
            group_id=group_id,
            enable_auto_commit=False
        )
        
        partitions = consumer.partitions_for_topic(topic)
        lag_info = {}
        
        for partition in partitions:
            tp = (topic, partition)
            
            # Get consumer offset
            committed = consumer.committed(tp)
            
            # Get latest offset
            end_offset = consumer.end_offsets([tp])[tp]
            
            if committed is not None:
                lag = end_offset - committed
                lag_info[partition] = {
                    'consumer_offset': committed,
                    'end_offset': end_offset,
                    'lag': lag
                }
        
        consumer.close()
        return lag_info
    
    def get_topic_metrics(self, topic: str) -> dict:
        """Get topic metrics"""
        consumer = KafkaConsumer(
            bootstrap_servers=self.config.bootstrap_servers
        )
        
        partitions = consumer.partitions_for_topic(topic)
        metrics = {
            'partition_count': len(partitions),
            'partitions': {}
        }
        
        for partition in partitions:
            tp = (topic, partition)
            beginning = consumer.beginning_offsets([tp])[tp]
            end = consumer.end_offsets([tp])[tp]
            
            metrics['partitions'][partition] = {
                'beginning_offset': beginning,
                'end_offset': end,
                'message_count': end - beginning
            }
        
        consumer.close()
        return metrics

# Usage
monitor = KafkaMonitor(DEFAULT_CONFIG)
print(monitor.get_consumer_lag('user-events', 'consumer-group-1'))
```

---

## Additional Resources

- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [kafka-python Documentation](https://kafka-python.readthedocs.io/)
- [Kafka Streams Documentation](https://kafka.apache.org/documentation/streams/)
- [Confluent Kafka Python](https://docs.confluent.io/platform/current/clients/confluent-kafka-python/)

## Best Practices

### Producer Configuration

- **Use appropriate `acks` setting**: `acks=all` for critical data, `acks=1` for high throughput
- **Configure batching**: Use `batch_size` and `linger_ms` for better throughput
- **Enable compression**: Use `lz4` or `gzip` to reduce network bandwidth
- **Set reasonable timeouts**: Configure `request_timeout_ms` and `delivery.timeout.ms`
- **Use idempotent producers**: Prevent duplicate messages on retries
- **Implement error handling**: Handle network errors and broker failures gracefully

### Consumer Configuration

- **Use manual offset commits**: Disable `enable_auto_commit` for better control
- **Set appropriate `session.timeout.ms`**: Balance between failure detection and processing time
- **Configure `max.poll.records`**: Limit batch size for predictable processing
- **Use consumer groups**: Enable parallel processing and load balancing
- **Implement rebalance listeners**: Handle partition reassignment gracefully
- **Monitor consumer lag**: Track offset lag to detect processing delays

### Topic Design

- **Choose appropriate partition count**: More partitions = more parallelism but more overhead
- **Set replication factor**: At least 3 for production environments
- **Configure retention**: Set `retention.ms` based on data freshness requirements
- **Use compacted topics**: For latest-value semantics (e.g., user profiles)
- **Plan partition growth**: Kafka doesn't support decreasing partitions
- **Use descriptive topic names**: Follow naming conventions for clarity

### Message Design

- **Use small message sizes**: Prefer <1MB messages for optimal performance
- **Include message keys**: For partitioning and ordering guarantees
- **Add message headers**: Include metadata for tracing and routing
- **Use consistent schemas**: Consider Avro/Protobuf for schema evolution
- **Include timestamps**: Use Kafka timestamps or custom timestamps
- **Design for idempotency**: Messages may be delivered multiple times

### Exactly-Once Semantics

- **Use transactional producers**: For exactly-once write semantics
- **Configure read_committed isolation**: Consumers only see committed transactions
- **Use idempotent producers**: Prevent duplicate message production
- **Monitor transaction coordinator**: Track transaction state and timeouts
- **Handle transaction failures**: Implement proper rollback logic
- **Test failure scenarios**: Verify exactly-once behavior under failures

### Performance Tuning

- **Tune batch sizes**: Larger batches improve throughput but increase latency
- **Adjust linger time**: Balance between batching and latency
- **Use appropriate compression**: `lz4` for speed, `gzip` for size
- **Configure fetch sizes**: Match `fetch.max.bytes` to message sizes
- **Use multiple consumers**: Scale consumer groups for parallel processing
- **Monitor broker metrics**: Track throughput, latency, and error rates

### Monitoring and Observability

- **Track consumer lag**: Monitor offset lag per partition
- **Monitor broker health**: Track CPU, memory, disk I/O, and network
- **Collect JMX metrics**: Use Prometheus/JMX exporter for metrics
- **Set up alerts**: Alert on high lag, broker failures, or partition imbalances
- **Log message processing**: Include correlation IDs for tracing
- **Use distributed tracing**: Integrate with OpenTelemetry or Jaeger

### Security

- **Enable SASL authentication**: Use SCRAM-SHA-256/512 for strong authentication
- **Configure TLS encryption**: Encrypt data in transit between clients and brokers
- **Use ACLs**: Restrict topic access based on user roles
- **Enable audit logging**: Track who is accessing which topics
- **Rotate credentials**: Regularly update passwords and certificates
- **Use separate clusters**: Isolate development, staging, and production

### Disaster Recovery

- **Configure replication**: Use replication factor ≥3 for high availability
- **Enable leader election**: Allow automatic leader failover
- **Monitor under-replicated partitions**: Alert on replication lag
- **Test failover scenarios**: Verify automatic recovery works
- **Backup critical topics**: Use mirror-maker for cross-cluster replication
- **Document recovery procedures**: Have clear runbooks for common failures

## Checklist

### Setup and Configuration
- [ ] Configure Kafka broker cluster with appropriate settings
- [ ] Set up Zookeeper/KRaft for cluster coordination
- [ ] Configure topic partitions and replication factors
- [ ] Enable authentication (SASL) and encryption (TLS)
- [ ] Set up JMX metrics and monitoring

### Producer Setup
- [ ] Configure producer with appropriate acks setting
- [ ] Enable batching and compression
- [ ] Set up idempotent producer
- [ ] Configure retry and timeout settings
- [ ] Implement error handling and logging

### Consumer Setup
- [ ] Configure consumer group and offset management
- [ ] Set manual offset commits
- [ ] Configure session and heartbeat timeouts
- [ ] Implement rebalance listeners
- [ ] Set up consumer lag monitoring

### Topic Management
- [ ] Create topics with appropriate partitions
- [ ] Configure retention policies
- [ ] Set up compacted topics if needed
- [ ] Configure topic ACLs
- [ ] Document topic naming conventions

### Message Design
- [ ] Define message schemas (Avro/Protobuf)
- [ ] Include message keys for partitioning
- [ ] Add message headers for metadata
- [ ] Design for idempotency
- [ ] Set up schema registry if using Avro

### Exactly-Once Processing
- [ ] Configure transactional producers
- [ ] Set read_committed isolation for consumers
- [ ] Implement transaction error handling
- [ ] Monitor transaction coordinator
- [ ] Test exactly-once behavior

### Performance Tuning
- [ ] Tune batch sizes and linger time
- [ ] Configure compression settings
- [ ] Adjust fetch sizes and poll intervals
- [ ] Scale consumers for parallel processing
- [ ] Monitor and optimize throughput/latency

### Monitoring and Alerting
- [ ] Set up JMX metrics collection
- [ ] Configure Grafana dashboards
- [ ] Set up alerts for consumer lag
- [ ] Monitor broker health metrics
- [ ] Track message throughput and error rates

### Security
- [ ] Enable SASL authentication
- [ ] Configure TLS encryption
- [ ] Set up ACLs for topic access
- [ ] Enable audit logging
- [ ] Rotate credentials regularly

### Disaster Recovery
- [ ] Configure replication factor ≥3
- [ ] Set up cross-cluster replication
- [ ] Test broker failover
- [ ] Document recovery procedures
- [ ] Set up automated backups

### Testing
- [ ] Test producer/consumer under load
- [ ] Verify exactly-once semantics
- [ ] Test rebalance scenarios
- [ ] Validate error handling
- [ ] Test failover and recovery

### Documentation
- [ ] Document cluster architecture
- [ ] Create topic design documentation
- [ ] Document monitoring and alerting setup
- [ ] Create runbooks for common issues
- [ ] Maintain API documentation
