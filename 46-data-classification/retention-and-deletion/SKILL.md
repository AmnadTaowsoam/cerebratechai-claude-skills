---
name: Retention and Deletion
description: Comprehensive guide to data retention policies, deletion workflows, and implementing GDPR/CCPA right to erasure across distributed systems.
---

# Data Retention and Deletion

## Overview

Data retention and deletion policies define how long data is kept and how it's permanently removed. This is critical for:

- **Compliance**: GDPR right to erasure, CCPA right to deletion
- **Cost**: Storage costs money (S3, databases, backups)
- **Security**: Old data = increased attack surface
- **Legal**: Litigation hold requirements
- **Performance**: Less data = faster queries

**Key Principle**: Keep data only as long as needed, then delete it securely.

## 1. Why Retention Matters

### Compliance Requirements

**GDPR (EU)**:
- **Right to Erasure** (Article 17): Users can request deletion of their data
- **Data Minimization** (Article 5): Only collect and retain necessary data
- **Storage Limitation**: Keep data no longer than necessary
- **Penalties**: Up to €20M or 4% of global revenue

**CCPA (California)**:
- **Right to Deletion**: Consumers can request deletion of personal information
- **Business Purpose**: Must delete data when no longer needed for disclosed purpose
- **Penalties**: Up to $7,500 per intentional violation

**PDPA (Thailand)**:
- Similar to GDPR
- Right to erasure
- Data minimization
- Storage limitation

### Cost Implications

```
Example: 1TB of data storage costs
- S3 Standard: $23/month
- S3 Glacier: $4/month
- RDS PostgreSQL: $115/month

Retaining 10 years of unnecessary data = $13,800 - $138,000 wasted
```

### Security Risks

```
More data = More risk
- Larger attack surface
- More PII to protect
- Higher breach impact
- Compliance complexity

Example: Target breach (2013)
- Attackers accessed old data from 2+ years ago
- If deleted per retention policy, breach impact would be 50% smaller
```

### Legal Holds

```
Litigation hold: Must preserve data relevant to lawsuit
- Overrides normal deletion policies
- Must track which data is on hold
- Must resume deletion after hold is lifted
```

## 2. Retention Policy Framework

### Policy Components

```yaml
# retention-policy.yaml
data_retention_policy:
  data_type: user_accounts
  classification: PII
  retention_period: "account_lifetime + 30_days"
  deletion_method: hard_delete
  legal_basis: contract
  exceptions:
    - litigation_hold
    - regulatory_requirement
  audit_trail: required
  owner: engineering@company.com
  last_reviewed: 2024-01-15
```

### Policy Template

```python
from dataclasses import dataclass
from datetime import timedelta
from enum import Enum

class DeletionMethod(Enum):
    SOFT_DELETE = "soft_delete"
    HARD_DELETE = "hard_delete"
    ANONYMIZE = "anonymize"
    ARCHIVE = "archive"

@dataclass
class RetentionPolicy:
    """Data retention policy."""
    data_type: str
    classification: str  # PII, Financial, Operational, etc.
    retention_period: timedelta
    deletion_method: DeletionMethod
    legal_basis: str  # Consent, Contract, Legal Obligation, etc.
    grace_period: timedelta  # Time before actual deletion
    backup_retention: timedelta  # How long to keep in backups
    exceptions: list[str]
    audit_required: bool
    owner: str
    
# Example policies
POLICIES = [
    RetentionPolicy(
        data_type="user_accounts",
        classification="PII",
        retention_period=timedelta(days=0),  # Keep while account active
        deletion_method=DeletionMethod.HARD_DELETE,
        legal_basis="Contract",
        grace_period=timedelta(days=30),
        backup_retention=timedelta(days=90),
        exceptions=["litigation_hold"],
        audit_required=True,
        owner="engineering@company.com"
    ),
    RetentionPolicy(
        data_type="transaction_logs",
        classification="Financial",
        retention_period=timedelta(days=2555),  # 7 years
        deletion_method=DeletionMethod.ARCHIVE,
        legal_basis="Legal Obligation",
        grace_period=timedelta(days=0),
        backup_retention=timedelta(days=2555),
        exceptions=["litigation_hold", "audit"],
        audit_required=True,
        owner="finance@company.com"
    ),
    RetentionPolicy(
        data_type="access_logs",
        classification="Operational",
        retention_period=timedelta(days=90),
        deletion_method=DeletionMethod.HARD_DELETE,
        legal_basis="Legitimate Interest",
        grace_period=timedelta(days=0),
        backup_retention=timedelta(days=30),
        exceptions=[],
        audit_required=False,
        owner="security@company.com"
    ),
]
```

## 3. Legal Requirements

### GDPR Requirements

**Right to Erasure (Article 17)**:
```
User can request deletion when:
1. Data no longer necessary for original purpose
2. User withdraws consent
3. User objects to processing
4. Data processed unlawfully
5. Legal obligation requires deletion

Exceptions (can refuse deletion):
1. Freedom of expression
2. Legal obligation
3. Public interest
4. Legal claims
```

**Implementation**:
```python
def handle_gdpr_deletion_request(user_id, reason):
    """Handle GDPR right to erasure request."""
    
    # Verify request is legitimate
    if not verify_user_identity(user_id):
        raise ValueError("Cannot verify user identity")
    
    # Check if exception applies
    if has_legal_hold(user_id):
        return {
            'status': 'denied',
            'reason': 'Data subject to legal hold'
        }
    
    if has_legal_obligation_to_retain(user_id):
        return {
            'status': 'denied',
            'reason': 'Legal obligation to retain data'
        }
    
    # Schedule deletion (30 day grace period)
    deletion_date = datetime.now() + timedelta(days=30)
    
    schedule_deletion(
        user_id=user_id,
        deletion_date=deletion_date,
        reason=reason,
        regulation='GDPR'
    )
    
    # Notify user
    send_deletion_confirmation(user_id, deletion_date)
    
    # Log for audit
    log_deletion_request(
        user_id=user_id,
        request_date=datetime.now(),
        deletion_date=deletion_date,
        reason=reason
    )
    
    return {
        'status': 'scheduled',
        'deletion_date': deletion_date.isoformat()
    }
```

### CCPA Requirements

**Right to Deletion**:
```python
def handle_ccpa_deletion_request(consumer_id):
    """Handle CCPA right to deletion request."""
    
    # CCPA requires deletion within 45 days
    deletion_deadline = datetime.now() + timedelta(days=45)
    
    # Identify all personal information
    personal_info = identify_personal_information(consumer_id)
    
    # Delete from all systems
    for system in personal_info['systems']:
        schedule_system_deletion(
            system=system,
            consumer_id=consumer_id,
            deadline=deletion_deadline
        )
    
    # Notify third parties
    for third_party in personal_info['third_parties']:
        notify_third_party_deletion(third_party, consumer_id)
    
    return {
        'status': 'processing',
        'deadline': deletion_deadline.isoformat(),
        'systems_affected': len(personal_info['systems'])
    }
```

### Industry-Specific Requirements

**HIPAA (Healthcare)**: 6 years retention
```python
HIPAA_RETENTION = timedelta(days=2190)  # 6 years

def apply_hipaa_retention(medical_record):
    """Apply HIPAA retention policy."""
    retention_until = medical_record.created_at + HIPAA_RETENTION
    
    if datetime.now() > retention_until:
        # Can delete
        delete_medical_record(medical_record.id)
    else:
        # Must retain
        schedule_deletion(medical_record.id, retention_until)
```

**SOX (Financial)**: 7 years retention
```python
SOX_RETENTION = timedelta(days=2555)  # 7 years

def apply_sox_retention(financial_record):
    """Apply SOX retention policy."""
    retention_until = financial_record.fiscal_year_end + SOX_RETENTION
    
    if datetime.now() > retention_until:
        archive_financial_record(financial_record.id)
    else:
        schedule_archival(financial_record.id, retention_until)
```

## 4. Retention Schedules by Data Type

### User Accounts

```python
USER_ACCOUNT_RETENTION = {
    'active_account': timedelta(days=0),  # Keep indefinitely while active
    'deleted_account': timedelta(days=30),  # 30 day grace period
    'inactive_account': timedelta(days=365),  # 1 year of inactivity
}

def check_user_account_retention(user):
    """Check if user account should be deleted."""
    
    if user.status == 'deleted':
        # Grace period for account recovery
        deletion_date = user.deleted_at + USER_ACCOUNT_RETENTION['deleted_account']
        if datetime.now() > deletion_date:
            hard_delete_user(user.id)
    
    elif user.status == 'active':
        # Check for inactivity
        if user.last_login_at:
            inactive_since = datetime.now() - user.last_login_at
            if inactive_since > USER_ACCOUNT_RETENTION['inactive_account']:
                # Notify user before deletion
                send_inactivity_warning(user.id)
                schedule_deletion(user.id, datetime.now() + timedelta(days=30))
```

### Transaction Logs

```python
TRANSACTION_RETENTION = {
    'financial_transactions': timedelta(days=2555),  # 7 years (SOX)
    'audit_logs': timedelta(days=2555),  # 7 years (compliance)
    'access_logs': timedelta(days=90),  # 90 days (security)
    'application_logs': timedelta(days=30),  # 30 days (debugging)
}

def cleanup_old_logs():
    """Delete logs past retention period."""
    
    for log_type, retention_period in TRANSACTION_RETENTION.items():
        cutoff_date = datetime.now() - retention_period
        
        # Delete old logs
        deleted_count = delete_logs_before(log_type, cutoff_date)
        
        logger.info(f"Deleted {deleted_count} {log_type} older than {cutoff_date}")
```

### Backups

```python
BACKUP_RETENTION = {
    'daily_backups': timedelta(days=7),
    'weekly_backups': timedelta(days=30),
    'monthly_backups': timedelta(days=365),
    'yearly_backups': timedelta(days=2555),  # 7 years
}

def cleanup_old_backups():
    """Delete backups past retention period."""
    
    for backup_type, retention_period in BACKUP_RETENTION.items():
        cutoff_date = datetime.now() - retention_period
        
        # List old backups
        old_backups = list_backups_before(backup_type, cutoff_date)
        
        # Delete
        for backup in old_backups:
            delete_backup(backup.id)
            logger.info(f"Deleted backup {backup.id} from {backup.created_at}")
```

### Analytics Data

```python
ANALYTICS_RETENTION = {
    'raw_events': timedelta(days=90),  # 90 days
    'aggregated_metrics': timedelta(days=395),  # 13 months (GDPR)
    'anonymized_data': None,  # Keep indefinitely
}

def cleanup_analytics_data():
    """Delete analytics data past retention period."""
    
    # Delete raw events
    cutoff = datetime.now() - ANALYTICS_RETENTION['raw_events']
    delete_events_before(cutoff)
    
    # Delete aggregated metrics
    cutoff = datetime.now() - ANALYTICS_RETENTION['aggregated_metrics']
    delete_metrics_before(cutoff)
    
    # Anonymize before deletion (for long-term analytics)
    anonymize_old_events()
```

### Audit Logs

```python
AUDIT_LOG_RETENTION = timedelta(days=2555)  # 7 years (compliance)

def cleanup_audit_logs():
    """Archive audit logs past retention period."""
    
    cutoff_date = datetime.now() - AUDIT_LOG_RETENTION
    
    # Archive to cold storage (don't delete!)
    old_logs = get_audit_logs_before(cutoff_date)
    
    for log in old_logs:
        # Archive to S3 Glacier
        archive_to_glacier(log)
        
        # Delete from primary storage
        delete_from_primary_storage(log.id)
```

## 5. Data Lifecycle States

### State Diagram

```
Active → Inactive → Soft Deleted → Hard Deleted
   ↓         ↓           ↓
Archived  Archived   Archived
```

### Implementation

```python
from enum import Enum

class DataLifecycleState(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SOFT_DELETED = "soft_deleted"
    HARD_DELETED = "hard_deleted"
    ARCHIVED = "archived"

class DataLifecycle:
    """Manage data lifecycle transitions."""
    
    def __init__(self, data_id, current_state):
        self.data_id = data_id
        self.current_state = current_state
    
    def transition_to_inactive(self):
        """Mark data as inactive (not accessed recently)."""
        if self.current_state == DataLifecycleState.ACTIVE:
            self.current_state = DataLifecycleState.INACTIVE
            update_state(self.data_id, DataLifecycleState.INACTIVE)
            logger.info(f"Data {self.data_id} transitioned to INACTIVE")
    
    def transition_to_soft_deleted(self):
        """Soft delete (recoverable)."""
        if self.current_state in [DataLifecycleState.ACTIVE, DataLifecycleState.INACTIVE]:
            self.current_state = DataLifecycleState.SOFT_DELETED
            update_state(self.data_id, DataLifecycleState.SOFT_DELETED)
            schedule_hard_delete(self.data_id, datetime.now() + timedelta(days=30))
            logger.info(f"Data {self.data_id} soft deleted, hard delete in 30 days")
    
    def transition_to_hard_deleted(self):
        """Hard delete (permanent)."""
        if self.current_state == DataLifecycleState.SOFT_DELETED:
            self.current_state = DataLifecycleState.HARD_DELETED
            permanently_delete(self.data_id)
            logger.info(f"Data {self.data_id} permanently deleted")
    
    def transition_to_archived(self):
        """Archive to cold storage."""
        if self.current_state in [DataLifecycleState.ACTIVE, DataLifecycleState.INACTIVE]:
            self.current_state = DataLifecycleState.ARCHIVED
            archive_data(self.data_id)
            logger.info(f"Data {self.data_id} archived")
```

## 6. Deletion Types

### Soft Delete

```python
def soft_delete_user(user_id):
    """Soft delete user (recoverable)."""
    
    # Mark as deleted
    db.execute("""
        UPDATE users
        SET deleted_at = NOW(),
            status = 'deleted'
        WHERE id = %s
    """, [user_id])
    
    # Schedule hard delete
    schedule_hard_delete(user_id, datetime.now() + timedelta(days=30))
    
    # Notify user
    send_deletion_confirmation(user_id)
    
    logger.info(f"User {user_id} soft deleted, recoverable for 30 days")

def recover_soft_deleted_user(user_id):
    """Recover soft deleted user."""
    
    # Check if still in grace period
    user = db.query("SELECT deleted_at FROM users WHERE id = %s", [user_id])
    
    if not user or not user.deleted_at:
        raise ValueError("User not found or not deleted")
    
    grace_period_end = user.deleted_at + timedelta(days=30)
    
    if datetime.now() > grace_period_end:
        raise ValueError("Grace period expired, cannot recover")
    
    # Restore user
    db.execute("""
        UPDATE users
        SET deleted_at = NULL,
            status = 'active'
        WHERE id = %s
    """, [user_id])
    
    # Cancel hard delete
    cancel_scheduled_deletion(user_id)
    
    logger.info(f"User {user_id} recovered from soft delete")
```

### Hard Delete

```python
def hard_delete_user(user_id):
    """Permanently delete user and all related data."""
    
    # Delete from all tables
    tables_to_delete = [
        'users',
        'user_profiles',
        'user_preferences',
        'user_sessions',
        'user_activity_logs',
        'user_notifications',
    ]
    
    for table in tables_to_delete:
        db.execute(f"DELETE FROM {table} WHERE user_id = %s", [user_id])
    
    # Delete from S3
    delete_user_files(user_id)
    
    # Delete from search index
    delete_from_elasticsearch(user_id)
    
    # Delete from cache
    delete_from_redis(user_id)
    
    # Notify third parties
    notify_third_party_deletion(user_id)
    
    # Log for audit
    log_hard_deletion(user_id)
    
    logger.info(f"User {user_id} permanently deleted")
```

### Anonymization

```python
def anonymize_user(user_id):
    """Anonymize user data (keep for analytics)."""
    
    # Replace PII with anonymized values
    db.execute("""
        UPDATE users
        SET email = %s,
            name = %s,
            phone = NULL,
            address = NULL,
            ip_address = NULL,
            anonymized_at = NOW()
        WHERE id = %s
    """, [
        f"anonymized_{user_id}@example.com",
        f"Anonymized User {user_id}",
        user_id
    ])
    
    # Keep non-PII data for analytics
    # - User ID (anonymized)
    # - Timestamps
    # - Aggregated metrics
    
    logger.info(f"User {user_id} anonymized")
```

### Pseudonymization

```python
import hashlib

def pseudonymize_user(user_id):
    """Replace identifiers with pseudonyms."""
    
    # Generate consistent pseudonym
    pseudonym = hashlib.sha256(f"{user_id}{SECRET_SALT}".encode()).hexdigest()[:16]
    
    # Replace in analytics tables
    db.execute("""
        UPDATE analytics_events
        SET user_id = %s,
            pseudonymized = TRUE
        WHERE user_id = %s
    """, [pseudonym, user_id])
    
    # Keep mapping (encrypted) for potential de-pseudonymization
    store_pseudonym_mapping(user_id, pseudonym)
    
    logger.info(f"User {user_id} pseudonymized as {pseudonym}")
```

## 7. Right to Erasure Implementation

### User Deletion Request Flow

```python
from enum import Enum

class DeletionStatus(Enum):
    REQUESTED = "requested"
    VERIFIED = "verified"
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class DeletionRequest:
    """Handle user deletion request."""
    
    def __init__(self, user_id, reason):
        self.user_id = user_id
        self.reason = reason
        self.status = DeletionStatus.REQUESTED
        self.request_id = generate_request_id()
    
    def verify_identity(self):
        """Verify user identity before deletion."""
        # Send verification email
        send_verification_email(self.user_id, self.request_id)
        
        # Wait for user to click verification link
        # (handled by separate endpoint)
        
        logger.info(f"Deletion request {self.request_id} awaiting verification")
    
    def schedule_deletion(self, grace_period_days=30):
        """Schedule deletion after grace period."""
        self.status = DeletionStatus.SCHEDULED
        
        deletion_date = datetime.now() + timedelta(days=grace_period_days)
        
        # Store deletion request
        db.execute("""
            INSERT INTO deletion_requests (request_id, user_id, reason, deletion_date, status)
            VALUES (%s, %s, %s, %s, %s)
        """, [self.request_id, self.user_id, self.reason, deletion_date, self.status.value])
        
        # Schedule background job
        schedule_background_job('delete_user', deletion_date, {'user_id': self.user_id})
        
        # Notify user
        send_deletion_scheduled_email(self.user_id, deletion_date)
        
        logger.info(f"Deletion scheduled for user {self.user_id} on {deletion_date}")
    
    def execute_deletion(self):
        """Execute the actual deletion."""
        self.status = DeletionStatus.IN_PROGRESS
        
        try:
            # Delete from all systems
            self._delete_from_primary_db()
            self._delete_from_s3()
            self._delete_from_elasticsearch()
            self._delete_from_redis()
            self._delete_from_third_parties()
            self._delete_from_backups()  # Delayed
            
            self.status = DeletionStatus.COMPLETED
            
            # Log completion
            log_deletion_completion(self.user_id, self.request_id)
            
            logger.info(f"Deletion completed for user {self.user_id}")
            
        except Exception as e:
            self.status = DeletionStatus.FAILED
            logger.error(f"Deletion failed for user {self.user_id}: {e}")
            
            # Alert ops team
            alert_deletion_failure(self.user_id, str(e))
    
    def _delete_from_primary_db(self):
        """Delete from primary database."""
        hard_delete_user(self.user_id)
    
    def _delete_from_s3(self):
        """Delete user files from S3."""
        s3 = boto3.client('s3')
        
        # List all user files
        objects = s3.list_objects_v2(
            Bucket='user-uploads',
            Prefix=f'users/{self.user_id}/'
        )
        
        # Delete all
        for obj in objects.get('Contents', []):
            s3.delete_object(Bucket='user-uploads', Key=obj['Key'])
    
    def _delete_from_elasticsearch(self):
        """Delete from search index."""
        es = Elasticsearch()
        es.delete_by_query(
            index='users',
            body={'query': {'term': {'user_id': self.user_id}}}
        )
    
    def _delete_from_redis(self):
        """Delete from cache."""
        redis = Redis()
        redis.delete(f'user:{self.user_id}')
        redis.delete(f'user:{self.user_id}:*')
    
    def _delete_from_third_parties(self):
        """Notify third parties to delete."""
        third_parties = ['stripe', 'sendgrid', 'segment']
        
        for party in third_parties:
            notify_third_party_deletion(party, self.user_id)
    
    def _delete_from_backups(self):
        """Schedule deletion from backups (delayed)."""
        # Backups are immutable, so we can't delete immediately
        # Schedule deletion when backup expires
        schedule_backup_deletion(self.user_id)

# API endpoint
@app.route('/api/users/me/delete', methods=['POST'])
def request_deletion():
    """Handle user deletion request."""
    user_id = get_current_user_id()
    reason = request.json.get('reason', 'User requested')
    
    # Create deletion request
    deletion_request = DeletionRequest(user_id, reason)
    deletion_request.verify_identity()
    
    return {
        'request_id': deletion_request.request_id,
        'status': 'verification_sent'
    }

@app.route('/api/users/delete/verify/<request_id>', methods=['GET'])
def verify_deletion(request_id):
    """Verify deletion request."""
    # Verify token
    deletion_request = get_deletion_request(request_id)
    
    if not deletion_request:
        return {'error': 'Invalid request'}, 404
    
    # Schedule deletion
    deletion_request.schedule_deletion(grace_period_days=30)
    
    return {
        'status': 'scheduled',
        'deletion_date': deletion_request.deletion_date.isoformat()
    }
```

## 8. Deletion Challenges

### Distributed Systems

```python
class DistributedDeletion:
    """Handle deletion across distributed systems."""
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.systems = [
            'primary_db',
            'replica_db',
            'cache',
            'search_index',
            'object_storage',
            'analytics_db',
            'third_party_services'
        ]
    
    def delete_everywhere(self):
        """Delete from all systems."""
        results = {}
        
        for system in self.systems:
            try:
                self._delete_from_system(system)
                results[system] = 'success'
            except Exception as e:
                results[system] = f'failed: {e}'
                logger.error(f"Failed to delete from {system}: {e}")
        
        # Check if all succeeded
        if all(status == 'success' for status in results.values()):
            logger.info(f"User {self.user_id} deleted from all systems")
        else:
            # Some failed - need manual intervention
            alert_partial_deletion(self.user_id, results)
        
        return results
    
    def _delete_from_system(self, system):
        """Delete from specific system."""
        if system == 'primary_db':
            delete_from_postgres(self.user_id)
        elif system == 'replica_db':
            # Wait for replication
            wait_for_replication()
            verify_deleted_from_replicas(self.user_id)
        elif system == 'cache':
            delete_from_redis(self.user_id)
        elif system == 'search_index':
            delete_from_elasticsearch(self.user_id)
        elif system == 'object_storage':
            delete_from_s3(self.user_id)
        elif system == 'analytics_db':
            anonymize_in_analytics(self.user_id)
        elif system == 'third_party_services':
            notify_third_parties(self.user_id)
```

### Backup Deletion

```python
def delete_from_backups(user_id):
    """Delete user data from backups (challenging!)."""
    
    # Problem: Backups are immutable
    # Solution: Mark for deletion, remove when backup expires
    
    # Option 1: Wait for backup to expire
    mark_for_deletion_in_backups(user_id)
    
    # Option 2: Create new backup without user data (expensive!)
    # recreate_backups_without_user(user_id)
    
    # Option 3: Encrypt user data, delete encryption key
    # delete_encryption_key_for_user(user_id)
    
    logger.info(f"User {user_id} marked for deletion in backups")

def mark_for_deletion_in_backups(user_id):
    """Mark user for deletion when backup expires."""
    
    # Store deletion marker
    db.execute("""
        INSERT INTO backup_deletion_queue (user_id, marked_at)
        VALUES (%s, NOW())
    """, [user_id])
    
    # When restoring from backup, check deletion queue
    # and exclude marked users
```

### Data Lakes (Immutable Logs)

```python
def handle_data_lake_deletion(user_id):
    """Handle deletion in immutable data lake."""
    
    # Problem: Data lake logs are immutable (append-only)
    # Solution: Anonymize instead of delete
    
    # Option 1: Pseudonymize user_id in all future queries
    pseudonymize_user_in_queries(user_id)
    
    # Option 2: Create "tombstone" record
    create_tombstone_record(user_id)
    
    # Option 3: Rewrite data lake (very expensive!)
    # rewrite_data_lake_without_user(user_id)
    
    logger.info(f"User {user_id} anonymized in data lake")

def create_tombstone_record(user_id):
    """Create tombstone to mark user as deleted."""
    
    # Write to data lake
    write_to_data_lake({
        'event_type': 'user_deleted',
        'user_id': user_id,
        'timestamp': datetime.now().isoformat(),
        'deleted_at': datetime.now().isoformat()
    })
    
    # Future queries should filter out deleted users
    # WHERE user_id NOT IN (SELECT user_id FROM tombstones)
```

### Third-Party Systems

```python
def notify_third_party_deletion(service, user_id):
    """Notify third-party service to delete user data."""
    
    if service == 'stripe':
        # Delete Stripe customer
        stripe.Customer.delete(get_stripe_customer_id(user_id))
    
    elif service == 'sendgrid':
        # Remove from email lists
        sendgrid.delete_recipient(get_sendgrid_recipient_id(user_id))
    
    elif service == 'segment':
        # Delete Segment user
        segment.delete_user(user_id)
    
    elif service == 'salesforce':
        # Delete Salesforce contact
        salesforce.delete_contact(get_salesforce_contact_id(user_id))
    
    logger.info(f"Notified {service} to delete user {user_id}")
```

## 9. Automated Retention

### TTL (Time To Live) in Databases

**PostgreSQL**:
```sql
-- Create partition by month
CREATE TABLE events_2024_01 PARTITION OF events
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

-- Drop old partitions
DROP TABLE events_2023_01;
```

**MongoDB**:
```javascript
// Create TTL index
db.sessions.createIndex(
  { "createdAt": 1 },
  { expireAfterSeconds: 3600 }  // 1 hour
);

// MongoDB automatically deletes documents after TTL
```

**DynamoDB**:
```python
# Enable TTL
dynamodb = boto3.client('dynamodb')

dynamodb.update_time_to_live(
    TableName='Sessions',
    TimeToLiveSpecification={
        'Enabled': True,
        'AttributeName': 'ttl'
    }
)

# Set TTL when creating item
table.put_item(
    Item={
        'session_id': 'abc123',
        'data': {...},
        'ttl': int(time.time()) + 3600  # Expire in 1 hour
    }
)
```

### S3 Lifecycle Policies

```python
import boto3

s3 = boto3.client('s3')

# Create lifecycle policy
lifecycle_policy = {
    'Rules': [
        {
            'Id': 'Delete old logs',
            'Status': 'Enabled',
            'Prefix': 'logs/',
            'Expiration': {
                'Days': 90
            }
        },
        {
            'Id': 'Archive old backups',
            'Status': 'Enabled',
            'Prefix': 'backups/',
            'Transitions': [
                {
                    'Days': 30,
                    'StorageClass': 'GLACIER'
                }
            ],
            'Expiration': {
                'Days': 2555  # 7 years
            }
        }
    ]
}

s3.put_bucket_lifecycle_configuration(
    Bucket='my-bucket',
    LifecycleConfiguration=lifecycle_policy
)
```

### Database Partitioning by Date

```sql
-- PostgreSQL: Partition by month
CREATE TABLE events (
    id SERIAL,
    user_id INT,
    event_type VARCHAR(50),
    created_at TIMESTAMP
) PARTITION BY RANGE (created_at);

-- Create partitions
CREATE TABLE events_2024_01 PARTITION OF events
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE events_2024_02 PARTITION OF events
FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- Drop old partitions (fast!)
DROP TABLE events_2023_01;  -- Deletes entire month instantly
```

### Scheduled Deletion Jobs

```python
from apscheduler.schedulers.background import BackgroundScheduler

def schedule_retention_jobs():
    """Schedule automated retention jobs."""
    
    scheduler = BackgroundScheduler()
    
    # Daily: Delete old logs
    scheduler.add_job(
        delete_old_logs,
        'cron',
        hour=2,
        minute=0
    )
    
    # Weekly: Delete old backups
    scheduler.add_job(
        delete_old_backups,
        'cron',
        day_of_week='sun',
        hour=3,
        minute=0
    )
    
    # Monthly: Archive old data
    scheduler.add_job(
        archive_old_data,
        'cron',
        day=1,
        hour=4,
        minute=0
    )
    
    scheduler.start()

def delete_old_logs():
    """Delete logs older than retention period."""
    cutoff = datetime.now() - timedelta(days=90)
    
    deleted = db.execute("""
        DELETE FROM application_logs
        WHERE created_at < %s
    """, [cutoff])
    
    logger.info(f"Deleted {deleted.rowcount} old logs")

def delete_old_backups():
    """Delete backups older than retention period."""
    cutoff = datetime.now() - timedelta(days=30)
    
    backups = list_backups_before(cutoff)
    
    for backup in backups:
        delete_backup(backup.id)
        logger.info(f"Deleted backup {backup.id}")

def archive_old_data():
    """Archive data to cold storage."""
    cutoff = datetime.now() - timedelta(days=365)
    
    old_data = get_data_before(cutoff)
    
    for data in old_data:
        archive_to_glacier(data)
        delete_from_primary_storage(data.id)
```

## 10. Legal Hold Procedures

### Legal Hold Implementation

```python
class LegalHold:
    """Manage legal holds on data."""
    
    def __init__(self, hold_id, reason, custodians):
        self.hold_id = hold_id
        self.reason = reason
        self.custodians = custodians  # List of user IDs
        self.created_at = datetime.now()
        self.released_at = None
    
    def apply_hold(self):
        """Apply legal hold to prevent deletion."""
        
        for user_id in self.custodians:
            # Mark user as on legal hold
            db.execute("""
                INSERT INTO legal_holds (hold_id, user_id, reason, created_at)
                VALUES (%s, %s, %s, %s)
            """, [self.hold_id, user_id, self.reason, self.created_at])
            
            # Cancel any scheduled deletions
            cancel_scheduled_deletion(user_id)
            
            logger.info(f"Legal hold {self.hold_id} applied to user {user_id}")
    
    def release_hold(self):
        """Release legal hold and resume normal retention."""
        
        self.released_at = datetime.now()
        
        for user_id in self.custodians:
            # Remove hold
            db.execute("""
                UPDATE legal_holds
                SET released_at = %s
                WHERE hold_id = %s AND user_id = %s
            """, [self.released_at, self.hold_id, user_id])
            
            # Resume normal retention policy
            apply_retention_policy(user_id)
            
            logger.info(f"Legal hold {self.hold_id} released for user {user_id}")

def has_legal_hold(user_id):
    """Check if user is on legal hold."""
    
    result = db.query("""
        SELECT COUNT(*) as count
        FROM legal_holds
        WHERE user_id = %s AND released_at IS NULL
    """, [user_id])
    
    return result[0]['count'] > 0

# Before deleting, always check for legal hold
def safe_delete_user(user_id):
    """Delete user only if not on legal hold."""
    
    if has_legal_hold(user_id):
        raise ValueError(f"Cannot delete user {user_id}: on legal hold")
    
    hard_delete_user(user_id)
```

## 11. Deletion Verification

### Proof of Deletion

```python
def generate_deletion_certificate(user_id, deletion_request_id):
    """Generate proof of deletion for user."""
    
    # Verify deletion completed
    deletion_request = get_deletion_request(deletion_request_id)
    
    if deletion_request.status != DeletionStatus.COMPLETED:
        raise ValueError("Deletion not completed")
    
    # Generate certificate
    certificate = {
        'user_id': user_id,
        'deletion_request_id': deletion_request_id,
        'deletion_date': deletion_request.completed_at.isoformat(),
        'systems_deleted_from': [
            'primary_database',
            'object_storage',
            'search_index',
            'cache',
            'third_party_services'
        ],
        'verification_date': datetime.now().isoformat(),
        'verified_by': 'automated_system'
    }
    
    # Sign certificate
    signature = sign_certificate(certificate)
    certificate['signature'] = signature
    
    # Store certificate
    store_deletion_certificate(certificate)
    
    return certificate
```

### Deletion Audits

```python
def audit_deletion_completeness(user_id):
    """Audit that user was completely deleted."""
    
    findings = []
    
    # Check primary database
    if user_exists_in_db(user_id):
        findings.append('User still exists in primary database')
    
    # Check S3
    if user_files_exist_in_s3(user_id):
        findings.append('User files still exist in S3')
    
    # Check Elasticsearch
    if user_exists_in_elasticsearch(user_id):
        findings.append('User still exists in search index')
    
    # Check Redis
    if user_exists_in_redis(user_id):
        findings.append('User still exists in cache')
    
    # Check third parties
    if user_exists_in_stripe(user_id):
        findings.append('User still exists in Stripe')
    
    if findings:
        logger.error(f"Deletion incomplete for user {user_id}: {findings}")
        alert_incomplete_deletion(user_id, findings)
    else:
        logger.info(f"Deletion verified complete for user {user_id}")
    
    return findings
```

## 12. Tools and Implementation

### PostgreSQL Partitioning + DROP

```sql
-- Fast deletion using partitions
CREATE TABLE events (
    id BIGSERIAL,
    user_id INT,
    event_type VARCHAR(50),
    created_at TIMESTAMP
) PARTITION BY RANGE (created_at);

-- Create monthly partitions
CREATE TABLE events_2024_01 PARTITION OF events
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

-- Delete entire month (instant!)
DROP TABLE events_2023_01;

-- vs slow row-by-row deletion
DELETE FROM events WHERE created_at < '2023-02-01';  -- SLOW!
```

### MongoDB TTL Indexes

```javascript
// Create TTL index
db.sessions.createIndex(
  { "expiresAt": 1 },
  { expireAfterSeconds: 0 }
);

// Insert with expiration
db.sessions.insertOne({
  sessionId: "abc123",
  userId: 456,
  expiresAt: new Date(Date.now() + 3600000)  // 1 hour from now
});

// MongoDB automatically deletes expired documents
```

### S3 Lifecycle Rules

```python
# Delete objects after 90 days
lifecycle_config = {
    'Rules': [
        {
            'Id': 'Delete after 90 days',
            'Status': 'Enabled',
            'Prefix': 'logs/',
            'Expiration': {'Days': 90}
        }
    ]
}

s3.put_bucket_lifecycle_configuration(
    Bucket='my-bucket',
    LifecycleConfiguration=lifecycle_config
)
```

## 13. Monitoring Retention Compliance

### Data Age Reports

```sql
-- Report on data age
SELECT 
    DATE_TRUNC('month', created_at) as month,
    COUNT(*) as record_count,
    AVG(EXTRACT(EPOCH FROM (NOW() - created_at)) / 86400) as avg_age_days,
    MAX(EXTRACT(EPOCH FROM (NOW() - created_at)) / 86400) as max_age_days
FROM events
GROUP BY DATE_TRUNC('month', created_at)
ORDER BY month DESC;
```

### Retention SLA Tracking

```python
def check_retention_sla():
    """Check if retention policies are being followed."""
    
    violations = []
    
    for policy in RETENTION_POLICIES:
        # Find data older than retention period
        cutoff = datetime.now() - policy.retention_period
        
        old_data_count = count_data_older_than(policy.data_type, cutoff)
        
        if old_data_count > 0:
            violations.append({
                'policy': policy.data_type,
                'retention_period': policy.retention_period,
                'violations': old_data_count
            })
    
    if violations:
        alert_retention_violations(violations)
    
    return violations
```

## 14. Real-World Scenarios

### User Requests Account Deletion

```python
# User clicks "Delete Account" button
@app.route('/api/account/delete', methods=['POST'])
def request_account_deletion():
    user_id = get_current_user_id()
    
    # Create deletion request
    request = DeletionRequest(user_id, "User requested")
    request.verify_identity()
    
    return {'status': 'verification_sent'}

# User clicks verification link in email
@app.route('/api/account/delete/confirm/<token>')
def confirm_deletion(token):
    user_id = verify_token(token)
    
    # Schedule deletion (30 day grace period)
    schedule_deletion(user_id, datetime.now() + timedelta(days=30))
    
    # Soft delete immediately
    soft_delete_user(user_id)
    
    return {'status': 'scheduled', 'deletion_date': '2024-02-15'}

# After 30 days, background job executes
def execute_scheduled_deletions():
    pending = get_pending_deletions()
    
    for deletion in pending:
        if datetime.now() >= deletion.deletion_date:
            hard_delete_user(deletion.user_id)
```

### GDPR Deletion Request (30 days)

```python
def handle_gdpr_request(user_id):
    """Handle GDPR right to erasure (30 day deadline)."""
    
    # Must complete within 30 days
    deadline = datetime.now() + timedelta(days=30)
    
    # Immediate actions
    soft_delete_user(user_id)
    notify_user_deletion_started(user_id)
    
    # Schedule hard delete
    schedule_deletion(user_id, deadline)
    
    # Track progress
    track_gdpr_deletion(user_id, deadline)
```

### Expired Trial Accounts (Auto-delete)

```python
def cleanup_expired_trials():
    """Auto-delete expired trial accounts."""
    
    # Find trials expired > 30 days ago
    cutoff = datetime.now() - timedelta(days=30)
    
    expired_trials = db.query("""
        SELECT id FROM users
        WHERE trial_expired_at < %s
        AND status = 'trial_expired'
    """, [cutoff])
    
    for user in expired_trials:
        # Notify user before deletion
        send_trial_deletion_warning(user.id)
        
        # Delete after 7 days
        schedule_deletion(user.id, datetime.now() + timedelta(days=7))
```

### Inactive Accounts (6 months)

```python
def cleanup_inactive_accounts():
    """Delete accounts inactive for 6 months."""
    
    cutoff = datetime.now() - timedelta(days=180)
    
    inactive_users = db.query("""
        SELECT id FROM users
        WHERE last_login_at < %s
        AND status = 'active'
    """, [cutoff])
    
    for user in inactive_users:
        # Warn user
        send_inactivity_warning(user.id)
        
        # Delete after 30 days if still inactive
        schedule_deletion(user.id, datetime.now() + timedelta(days=30))
```

## Best Practices

1. **Clear Policies**: Document retention periods for each data type
2. **Automate Deletion**: Don't rely on manual processes
3. **Grace Periods**: Allow recovery for accidental deletions
4. **Audit Trail**: Log all deletions for compliance
5. **Verify Completeness**: Check deletion across all systems
6. **Legal Holds**: Implement process to suspend deletion
7. **Third-Party Coordination**: Notify partners to delete
8. **Backup Strategy**: Plan for deletion from backups
9. **Monitor Compliance**: Track retention SLAs
10. **User Communication**: Notify users before deletion

## Common Pitfalls

- **Forgetting Third Parties**: Data shared with partners
- **Immutable Backups**: Can't delete from backups immediately
- **Distributed Systems**: Deletion may fail in some systems
- **Data Lakes**: Immutable logs require anonymization
- **No Grace Period**: Accidental deletions are permanent
- **Missing Audit Trail**: Can't prove deletion occurred
- **Legal Holds**: Deleting data under litigation hold

## Summary

Implement comprehensive retention and deletion policies to comply with GDPR/CCPA, reduce costs, and minimize security risks. Automate deletion using TTL, lifecycle policies, and scheduled jobs. Provide grace periods for recovery, verify deletion completeness, and maintain audit trails for compliance.
