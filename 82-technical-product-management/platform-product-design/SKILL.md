---
name: Platform Product Design
description: Designing multi-tenant platform products with extensibility, scalability, and ecosystem enablement
---

# Platform Product Design

## Current Level: Expert (Enterprise Scale)

## Domain: Technical Product Management
## Skill ID: 138

---

## Executive Summary

Platform Product Design enables creation of multi-tenant, extensible platforms that support third-party developers, partners, and ecosystem growth. This capability is essential for SaaS platforms, marketplaces, and any product requiring extensibility and scalability.

### Strategic Necessity

- **Multi-Tenancy**: Support multiple customers efficiently
- **Extensibility**: Enable third-party integrations
- **Scalability**: Handle growth across customers and users
- **Ecosystem Growth**: Foster partner and developer ecosystem
- **Revenue Diversity**: Multiple revenue streams (subscriptions, marketplace, etc.)

---

## Technical Deep Dive

### Platform Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Platform Product Architecture                       │
│                                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│  │   Tenant     │    │   Platform  │    │   Third     │                  │
│  │   Management │───▶│   Services  │───▶│   Party      │                  │
│  │   Layer      │    │   Layer     │    │   Integration │                  │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘                  │
│         │                   │                   │                           │
│         ▼                   ▼                   ▼                           │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Core Platform Services                           │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Auth     │  │  Identity  │  │  Billing   │  │  API       │            │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘            │   │
│  └───────┼────────────┼────────────┼────────────┼────────────────────┘   │
│          │            │            │            │                         │
│          ▼            ▼            ▼            ▼                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Application Layer                             │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Core     │  │  Tenant    │  │  Partner   │  │  Developer │            │   │
│  │  │  App      │  │  Apps      │  │  Apps      │  │  Apps      │            │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Infrastructure Layer                            │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Database  │  │  Cache     │  │  Message   │  │  Storage   │            │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Multi-Tenancy Architecture

```python
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class TenantIsolation(Enum):
    """Tenant isolation strategies"""
    SHARED_DATABASE = "shared_database"
    SHARED_SCHEMA = "shared_schema"
    SEPARATE_DATABASE = "separate_database"
    SEPARATE_SCHEMA = "separate_schema"

class TenantState(Enum):
    """Tenant states"""
    PROVISIONING = "provisioning"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"

@dataclass
class Tenant:
    """Tenant definition"""
    tenant_id: str
    name: str
    plan: str
    state: TenantState
    settings: Dict[str, Any]
    created_at: str
    updated_at: str

class MultiTenantArchitect:
    """Multi-tenant platform architect"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.isolation_strategy = TenantIsolation(
            config.get('isolation_strategy', 'shared_database')
        )
        self.tenant_store = TenantStore(config['tenant_store'])
        self.data_layer = DataLayer(config['data_layer'])
        self.cache_layer = CacheLayer(config['cache_layer'])
        
    def provision_tenant(
        self,
        tenant_config: Dict[str, Any]
    ) -> Tenant:
        """Provision new tenant"""
        logger.info(f"Provisioning tenant: {tenant_config['name']}")
        
        # Validate tenant configuration
        self._validate_tenant_config(tenant_config)
        
        # Create tenant record
        tenant_id = self._generate_tenant_id()
        tenant = Tenant(
            tenant_id=tenant_id,
            name=tenant_config['name'],
            plan=tenant_config['plan'],
            state=TenantState.PROVISIONING,
            settings=tenant_config.get('settings', {}),
            created_at=datetime.utcnow().isoformat(),
            updated_at=datetime.utcnow().isoformat()
        )
        
        # Store tenant
        self.tenant_store.create_tenant(tenant)
        
        # Provision infrastructure based on isolation strategy
        if self.isolation_strategy == TenantIsolation.SEPARATE_DATABASE:
            await self._provision_separate_database(tenant)
        elif self.isolation_strategy == TenantIsolation.SEPARATE_SCHEMA:
            await self._provision_separate_schema(tenant)
        elif self.isolation_strategy == TenantIsolation.SHARED_SCHEMA:
            await self._provision_shared_schema(tenant)
        else:
            await self._provision_shared_database(tenant)
        
        # Provision application resources
        await self._provision_application_resources(tenant)
        
        # Setup integrations
        await self._setup_integrations(tenant)
        
        # Update tenant state
        tenant.state = TenantState.ACTIVE
        tenant.updated_at = datetime.utcnow().isoformat()
        self.tenant_store.update_tenant(tenant)
        
        # Send welcome email
        await self._send_welcome_email(tenant)
        
        logger.info(f"Tenant provisioned: {tenant_id}")
        
        return tenant
    
    def _validate_tenant_config(self, config: Dict[str, Any]):
        """Validate tenant configuration"""
        required_fields = ['name', 'plan', 'admin_email']
        
        for field in required_fields:
            if field not in config:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate email format
        if not self._is_valid_email(config['admin_email']):
            raise ValueError(f"Invalid email: {config['admin_email']}")
    
    def _is_valid_email(self, email: str) -> bool:
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def _generate_tenant_id(self) -> str:
        """Generate unique tenant ID"""
        import uuid
        return f"tenant_{uuid.uuid4().hex[:8]}"
    
    async def _provision_separate_database(self, tenant: Tenant):
        """Provision separate database for tenant"""
        logger.info(f"Provisioning separate database for {tenant.tenant_id}")
        
        # Create database
        db_name = f"{tenant.tenant_id}_db"
        await self.data_layer.create_database(db_name)
        
        # Create schema
        await self.data_layer.create_schema(db_name, tenant.tenant_id)
        
        # Create user
        db_user = f"{tenant.tenant_id}_user"
        await self.data_layer.create_database_user(db_name, db_user)
        
        # Grant permissions
        await self.data_layer.grant_permissions(db_name, db_user)
        
        # Store connection string
        connection_string = f"postgresql://{db_user}:{self._generate_password()}@localhost/{db_name}"
        tenant.settings['database_connection'] = connection_string
        
        logger.info(f"Database provisioned: {db_name}")
    
    async def _provision_separate_schema(self, tenant: Tenant):
        """Provision separate schema for tenant"""
        logger.info(f"Provisioning separate schema for {tenant.tenant_id}")
        
        # Create schema in shared database
        schema_name = f"{tenant.tenant_id}_schema"
        await self.data_layer.create_schema(schema_name, tenant.tenant_id)
        
        # Create user
        db_user = f"{tenant.tenant_id}_user"
        await self.data_layer.create_database_user('shared_db', db_user)
        
        # Grant permissions on schema
        await self.data_layer.grant_schema_permissions(schema_name, db_user)
        
        # Store connection string
        connection_string = f"postgresql://{db_user}:{self._generate_password()}@localhost/shared_db?search_path={schema_name}"
        tenant.settings['database_connection'] = connection_string
        
        logger.info(f"Schema provisioned: {schema_name}")
    
    async def _provision_shared_schema(self, tenant: Tenant):
        """Provision shared schema for tenant"""
        logger.info(f"Provisioning shared schema for {tenant.tenant_id}")
        
        # Use shared schema with tenant_id column
        await self.data_layer.ensure_tenant_column('shared_db')
        
        # Create user
        db_user = f"{tenant.tenant_id}_user"
        await self.data_layer.create_database_user('shared_db', db_user)
        
        # Grant permissions
        await self.data_layer.grant_table_permissions('shared_db', db_user)
        
        # Store connection string
        connection_string = f"postgresql://{db_user}:{self._generate_password()}@localhost/shared_db"
        tenant.settings['database_connection'] = connection_string
        tenant.settings['tenant_id'] = tenant.tenant_id
        
        logger.info(f"Shared schema configured: {tenant.tenant_id}")
    
    async def _provision_shared_database(self, tenant: Tenant):
        """Provision shared database for tenant"""
        logger.info(f"Provisioning shared database for {tenant.tenant_id}")
        
        # Use shared database with tenant_id column
        await self.data_layer.ensure_tenant_column('shared_db')
        
        # Create user
        db_user = f"{tenant.tenant_id}_user"
        await self.data_layer.create_database_user('shared_db', db_user)
        
        # Grant permissions
        await self.data_layer.grant_table_permissions('shared_db', db_user)
        
        # Store connection string
        connection_string = f"postgresql://{db_user}:{self._generate_password()}@localhost/shared_db"
        tenant.settings['database_connection'] = connection_string
        tenant.settings['tenant_id'] = tenant.tenant_id
        
        logger.info(f"Shared database configured: {tenant.tenant_id}")
    
    def _generate_password(self) -> str:
        """Generate secure password"""
        import secrets
        import string
        
        alphabet = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(alphabet) for _ in range(32))
        
        return password
    
    async def _provision_application_resources(self, tenant: Tenant):
        """Provision application resources for tenant"""
        logger.info(f"Provisioning application resources for {tenant.tenant_id}")
        
        # Create application namespace
        await self._create_application_namespace(tenant)
        
        # Provision cache namespace
        await self.cache_layer.create_namespace(tenant.tenant_id)
        
        # Create storage bucket
        await self._create_storage_bucket(tenant)
        
        # Configure DNS
        await self._configure_dns(tenant)
        
        logger.info(f"Application resources provisioned: {tenant.tenant_id}")
    
    async def _create_application_namespace(self, tenant: Tenant):
        """Create application namespace for tenant"""
        # Create Kubernetes namespace
        # Configure resource quotas
        # Setup network policies
        pass
    
    async def _setup_integrations(self, tenant: Tenant):
        """Setup integrations for tenant"""
        logger.info(f"Setting up integrations for {tenant.tenant_id}")
        
        # Configure SSO
        await self._configure_sso(tenant)
        
        # Configure API keys
        await self._generate_api_keys(tenant)
        
        # Setup webhooks
        await self._setup_webhooks(tenant)
        
        logger.info(f"Integrations configured: {tenant.tenant_id}")
    
    async def _configure_sso(self, tenant: Tenant):
        """Configure SSO for tenant"""
        # Setup SAML/OAuth
        # Configure identity provider
        # Map user attributes
        pass
    
    async def _generate_api_keys(self, tenant: Tenant):
        """Generate API keys for tenant"""
        # Generate API keys
        # Store securely
        # Provide to tenant
        pass
    
    async def _setup_webhooks(self, tenant: Tenant):
        """Setup webhooks for tenant"""
        # Register webhook URLs
        # Configure event types
        # Setup retry logic
        pass
    
    async def _send_welcome_email(self, tenant: Tenant):
        """Send welcome email to tenant"""
        # Send welcome email with credentials
        # Provide getting started guide
        # Include support contact
        pass

class TenantStore:
    """Tenant store for multi-tenant platform"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.db = self._initialize_database()
        
    def _initialize_database(self):
        """Initialize database connection"""
        # Implementation would connect to database
        pass
    
    def create_tenant(self, tenant: Tenant):
        """Create tenant record"""
        # Insert tenant into database
        pass
    
    def update_tenant(self, tenant: Tenant):
        """Update tenant record"""
        # Update tenant in database
        pass
    
    def get_tenant(self, tenant_id: str) -> Optional[Tenant]:
        """Get tenant by ID"""
        # Query database
        pass
    
    def get_tenants_by_state(
        self,
        state: TenantState
    ) -> List[Tenant]:
        """Get tenants by state"""
        # Query database
        pass

class DataLayer:
    """Data layer for multi-tenant platform"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def create_database(self, db_name: str):
        """Create database"""
        pass
    
    async def create_schema(self, db_name: str, schema_name: str):
        """Create schema"""
        pass
    
    async def create_database_user(self, db_name: str, username: str):
        """Create database user"""
        pass
    
    async def grant_permissions(self, db_name: str, username: str):
        """Grant permissions"""
        pass
    
    async def grant_schema_permissions(self, schema_name: str, username: str):
        """Grant schema permissions"""
        pass
    
    async def grant_table_permissions(self, db_name: str, username: str):
        """Grant table permissions"""
        pass
    
    async def ensure_tenant_column(self, db_name: str):
        """Ensure tenant_id column exists"""
        pass

class CacheLayer:
    """Cache layer for multi-tenant platform"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def create_namespace(self, tenant_id: str):
        """Create cache namespace"""
        pass
    
    async def set(self, tenant_id: str, key: str, value: Any, ttl: int):
        """Set cache value"""
        pass
    
    async def get(self, tenant_id: str, key: str) -> Optional[Any]:
        """Get cache value"""
        pass
    
    async def delete(self, tenant_id: str, key: str):
        """Delete cache value"""
        pass
```

### Platform Services

```python
class PlatformServices:
    """Core platform services"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.auth_service = AuthService(config['auth'])
        self.billing_service = BillingService(config['billing'])
        self.notification_service = NotificationService(config['notification'])
        self.analytics_service = AnalyticsService(config['analytics'])
        
    async def authenticate_tenant(
        self,
        tenant_id: str,
        credentials: Dict[str, str]
    ) -> Dict[str, Any]:
        """Authenticate tenant"""
        logger.info(f"Authenticating tenant: {tenant_id}")
        
        # Validate tenant credentials
        if not await self.auth_service.validate_credentials(tenant_id, credentials):
            raise AuthenticationError("Invalid credentials")
        
        # Check tenant state
        tenant = await self.tenant_store.get_tenant(tenant_id)
        if tenant.state != TenantState.ACTIVE:
            raise TenantNotActiveError(f"Tenant is {tenant.state.value}")
        
        # Generate JWT token
        token = await self.auth_service.generate_token(tenant_id, credentials)
        
        # Get tenant configuration
        tenant_config = await self._get_tenant_config(tenant_id)
        
        return {
            'token': token,
            'tenant_id': tenant_id,
            'tenant_name': tenant.name,
            'plan': tenant.plan,
            'settings': tenant.settings,
            'features': tenant_config['features']
        }
    
    async def _get_tenant_config(self, tenant_id: str) -> Dict[str, Any]:
        """Get tenant configuration"""
        # Get tenant from store
        tenant = await self.tenant_store.get_tenant(tenant_id)
        
        # Get plan features
        plan_features = await self.billing_service.get_plan_features(tenant.plan)
        
        # Merge with tenant settings
        config = {
            'features': plan_features,
            'custom_settings': tenant.settings
        }
        
        return config

class AuthService:
    """Authentication service"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def validate_credentials(
        self,
        tenant_id: str,
        credentials: Dict[str, str]
    ) -> bool:
        """Validate tenant credentials"""
        # Validate against database
        # Check account status
        # Verify password hash
        return True
    
    async def generate_token(
        self,
        tenant_id: str,
        credentials: Dict[str, str]
    ) -> str:
        """Generate JWT token"""
        # Create JWT payload
        # Sign with secret key
        # Return token
        return "jwt_token"

class BillingService:
    """Billing service"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def get_plan_features(self, plan: str) -> Dict[str, Any]:
        """Get features for plan"""
        # Query plan from database
        # Return feature list
        return {}

class NotificationService:
    """Notification service"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def send_notification(
        self,
        tenant_id: str,
        notification: Dict[str, Any]
    ):
        """Send notification to tenant"""
        # Send email
        # Send SMS
        # Send push notification
        pass

class AnalyticsService:
    """Analytics service"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def track_event(
        self,
        tenant_id: str,
        event: Dict[str, Any]
    ):
        """Track analytics event"""
        # Store event in analytics database
        # Update metrics
        # Trigger alerts if needed
        pass
```

---

## Tooling & Tech Stack

### Multi-Tenancy Tools
- **Kubernetes Namespaces**: Tenant isolation
- **PostgreSQL Row Level Security**: Database isolation
- **Redis Namespaces**: Cache isolation
- **VPC Peering**: Network isolation

### Platform Services
- **Keycloak**: Identity and access management
- **Stripe**: Billing and payments
- **SendGrid**: Email notifications
- **Segment**: Analytics and tracking

### Infrastructure
- **AWS**: Cloud infrastructure
- **Kubernetes**: Container orchestration
- **PostgreSQL**: Database
- **Redis**: Cache

### Monitoring
- **Prometheus**: Metrics collection
- **Grafana**: Visualization
- **Jaeger**: Distributed tracing
- **ELK Stack**: Logging

---

## Configuration Essentials

### Platform Configuration

```yaml
# config/platform_config.yaml
platform:
  name: "My Platform"
  version: "1.0.0"
  
  multi_tenancy:
    isolation_strategy: "separate_database"  # shared_database, shared_schema, separate_database, separate_schema
    max_tenants: 10000
    default_plan: "basic"
  
  plans:
    basic:
      name: "Basic"
      price: 29  # USD per month
      features:
        - "5_users"
        - "10gb_storage"
        - "basic_analytics"
        - "email_support"
    
    pro:
      name: "Pro"
      price: 99  # USD per month
      features:
        - "25_users"
        - "100gb_storage"
        - "advanced_analytics"
        - "priority_support"
        - "api_access"
        - "custom_domain"
    
    enterprise:
      name: "Enterprise"
      price: 299  # USD per month
      features:
        - "unlimited_users"
        - "1tb_storage"
        - "enterprise_analytics"
        - "24_7_support"
        - "api_access"
        - "custom_domain"
        - "sso_integration"
        - "sla_guarantee"

  services:
    auth:
      provider: "keycloak"
      realm: "platform"
      url: "https://auth.example.com"
    
    billing:
      provider: "stripe"
      api_key: "${STRIPE_API_KEY}"
      webhook_secret: "${STRIPE_WEBHOOK_SECRET}"
    
    notification:
      email:
        provider: "sendgrid"
        api_key: "${SENDGRID_API_KEY}"
      sms:
        provider: "twilio"
        account_sid: "${TWILIO_ACCOUNT_SID}"
        auth_token: "${TWILIO_AUTH_TOKEN}"
    
    analytics:
      provider: "segment"
      write_key: "${SEGMENT_WRITE_KEY}"
    
    cache:
      provider: "redis"
      url: "redis://localhost:6379"
      ttl: 3600  # seconds
    
    storage:
      provider: "s3"
      bucket: "platform-storage"
      region: "us-west-2"
      access_key: "${AWS_ACCESS_KEY_ID}"
      secret_key: "${AWS_SECRET_ACCESS_KEY}"

limits:
  api:
    rate_limiting:
      enabled: true
      default_limit: 1000  # requests per hour
      burst_limit: 100  # requests per minute
    
    storage:
      per_tenant:
        basic: "10gb"
        pro: "100gb"
        enterprise: "1tb"
    
    users:
      per_plan:
        basic: 5
        pro: 25
        enterprise: "unlimited"
```

---

## Code Examples

### Good: Complete Platform Implementation

```python
# platform/tenant.py
import asyncio
import logging
from typing import Dict, Any

from platform.architect import MultiTenantArchitect
from platform.services import PlatformServices
from config.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def provision_new_tenant():
    """Provision new tenant"""
    logger.info("=" * 60)
    logger.info("Tenant Provisioning")
    logger.info("=" * 60)
    
    # Load tenant configuration
    tenant_config = load_config('config/tenant_config.yaml')
    
    # Step 1: Validate configuration
    logger.info("\n" + "=" * 60)
    logger.info("Step 1: Validating Configuration")
    logger.info("=" * 60)
    
    validate_tenant_config(tenant_config)
    
    logger.info("Configuration validated")
    
    # Step 2: Provision tenant
    logger.info("\n" + "=" * 60)
    logger.info("Step 2: Provisioning Tenant")
    logger.info("=" * 60)
    
    architect = MultiTenantArchitect(settings.platform_config)
    tenant = await architect.provision_tenant(tenant_config)
    
    logger.info(f"Tenant provisioned: {tenant.tenant_id}")
    
    # Step 3: Setup integrations
    logger.info("\n" + "=" * 60)
    logger.info("Step 3: Setting Up Integrations")
    logger.info("=" * 60)
    
    await setup_tenant_integrations(tenant)
    
    logger.info("Integrations configured")
    
    # Step 4: Send welcome email
    logger.info("\n" + "=" * 60)
    logger.info("Step 4: Sending Welcome Email")
    logger.info("=" * 60)
    
    await send_welcome_email(tenant, tenant_config)
    
    logger.info("Welcome email sent")
    
    # Print summary
    logger.info("\n" + "=" * 60)
    logger.info("Tenant Provisioning Summary")
    logger.info("=" * 60)
    logger.info(f"Tenant ID: {tenant.tenant_id}")
    logger.info(f"Tenant Name: {tenant.name}")
    logger.info(f"Plan: {tenant.plan}")
    logger.info(f"State: {tenant.state.value}")
    logger.info(f"Database: {tenant.settings.get('database_connection', 'N/A')}")
    logger.info(f"Features: {tenant_config.get('features', [])}")

def load_config(filename: str) -> Dict[str, Any]:
    """Load configuration from file"""
    import yaml
    with open(filename, 'r') as f:
        return yaml.safe_load(f)

def validate_tenant_config(config: Dict[str, Any]):
    """Validate tenant configuration"""
    required_fields = ['name', 'plan', 'admin_email', 'admin_password']
    
    for field in required_fields:
        if field not in config:
            raise ValueError(f"Missing required field: {field}")
    
    # Validate email
    if not is_valid_email(config['admin_email']):
        raise ValueError(f"Invalid email: {config['admin_email']}")
    
    # Validate plan
    if config['plan'] not in ['basic', 'pro', 'enterprise']:
        raise ValueError(f"Invalid plan: {config['plan']}")

def is_valid_email(email: str) -> bool:
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

async def setup_tenant_integrations(tenant: Tenant):
    """Setup tenant integrations"""
    # Configure SSO
    await configure_sso(tenant)
    
    # Generate API keys
    await generate_api_keys(tenant)
    
    # Setup webhooks
    await setup_webhooks(tenant)
    
    # Configure analytics
    await configure_analytics(tenant)

async def configure_sso(tenant: Tenant):
    """Configure SSO for tenant"""
    logger.info(f"Configuring SSO for {tenant.tenant_id}")
    # Implementation would configure SAML/OAuth
    pass

async def generate_api_keys(tenant: Tenant):
    """Generate API keys for tenant"""
    logger.info(f"Generating API keys for {tenant.tenant_id}")
    # Implementation would generate and store API keys
    pass

async def setup_webhooks(tenant: Tenant):
    """Setup webhooks for tenant"""
    logger.info(f"Setting up webhooks for {tenant.tenant_id}")
    # Implementation would configure webhook endpoints
    pass

async def configure_analytics(tenant: Tenant):
    """Configure analytics for tenant"""
    logger.info(f"Configuring analytics for {tenant.tenant_id}")
    # Implementation would configure analytics tracking
    pass

async def send_welcome_email(tenant: Tenant, config: Dict[str, Any]):
    """Send welcome email to tenant"""
    logger.info(f"Sending welcome email to {tenant.tenant_id}")
    # Implementation would send welcome email with credentials
    pass

async def main():
    """Main entry point"""
    await provision_new_tenant()

if __name__ == "__main__":
    asyncio.run(main())
```

### Bad: Anti-pattern Example

```python
# BAD: No tenant isolation
def bad_platform():
    # All tenants share same database
    single_database()

# BAD: No resource limits
def bad_platform():
    # No quotas
    unlimited_resources()

# BAD: No billing
def bad_platform():
    # No metering
    free_platform()

# BAD: No monitoring
def bad_platform():
    # No observability
    no_monitoring()

# BAD: No security
def bad_platform():
    # No access control
    open_platform()
```

---

## Standards, Compliance & Security

### Industry Standards
- **GDPR**: Data protection and privacy
- **SOC 2 Type II**: Security and availability
- **PCI DSS**: Payment card security
- **ISO 27001**: Information security

### Security Best Practices
- **Tenant Isolation**: Separate tenant resources
- **Data Encryption**: Encrypt all data at rest and in transit
- **Access Control**: RBAC for tenant resources
- **Audit Logging**: Log all tenant activities

### Compliance Requirements
- **Data Residency**: Store data in specified regions
- **Data Retention**: Implement data retention policies
- **Right to be Forgotten**: Support GDPR requirements
- **SLA Compliance**: Meet service level agreements

---

## Quick Start

### 1. Install Dependencies

```bash
pip install pyyaml
pip install asyncpg
pip install redis
```

### 2. Configure Platform

```bash
# Copy example config
cp config/platform_config.yaml.example config/platform_config.yaml

# Edit configuration
vim config/platform_config.yaml
```

### 3. Provision Tenant

```bash
python platform/tenant.py --config config/tenant_config.yaml
```

### 4. Monitor Platform

```bash
# Check tenant status
python platform/monitor.py --tenant-id tenant_123456

# View metrics
python platform/analytics.py --tenant-id tenant_123456
```

---

## Production Checklist

### Multi-Tenancy
- [ ] Tenant isolation configured
- [ ] Resource quotas defined
- [ ] Database isolation implemented
- [ ] Cache isolation implemented
- [ ] Network isolation implemented

### Platform Services
- [ ] Authentication configured
- [ ] Billing configured
- [ ] Notifications configured
- [ ] Analytics configured
- [ ] Monitoring configured

### Security
- [ ] Encryption enabled
- [ ] Access control implemented
- [ ] Audit logging enabled
- [ ] Security audit completed
- [ ] Compliance verified

### Operations
- [ ] Backup procedures documented
- [ ] Disaster recovery plan
- [ ] Runbooks documented
- [ ] Team trained
- [ ] Support processes defined

---

## Anti-patterns

### ❌ Avoid These Practices

1. **No Tenant Isolation**
   ```python
   # BAD: No isolation
   single_database_for_all()
   ```

2. **No Resource Limits**
   ```python
   # BAD: No limits
   unlimited_resources()
   ```

3. **No Billing**
   ```python
   # BAD: No metering
   free_platform()
   ```

4. **No Monitoring**
   ```python
   # BAD: No observability
   no_monitoring()
   ```

5. **No Security**
   ```python
   # BAD: No access control
   open_platform()
   ```

### ✅ Follow These Practices

1. **Tenant Isolation**
   ```python
   # GOOD: Tenant isolation
   provision_separate_database(tenant)
   ```

2. **Resource Limits**
   ```python
   # GOOD: Resource quotas
   apply_resource_quotas(tenant)
   ```

3. **Billing**
   ```python
   # GOOD: Metering
   track_usage(tenant)
   ```

4. **Monitoring**
   ```python
   # GOOD: Observability
   monitor_tenant(tenant)
   ```

5. **Security**
   ```python
   # GOOD: Access control
   implement_rbac(tenant)
   ```

---

## Unit Economics & KPIs

### Development Costs
- **Initial Setup**: 80-120 hours
- **Multi-Tenancy**: 60-100 hours
- **Platform Services**: 80-120 hours
- **Testing & Validation**: 40-60 hours
- **Total**: 260-400 hours

### Operational Costs
- **Infrastructure**: $2000-10000/month
- **Platform Services**: $500-2000/month
- **Monitoring**: $100-300/month
- **Support**: 20-40 hours/month

### ROI Metrics
- **Revenue per Tenant**: $29-299/month
- **Customer Acquisition Cost**: $100-500
- **Lifetime Value**: $500-5000
- **Churn Rate**: 5-10% monthly

### KPI Targets
- **Tenant Provisioning Time**: < 5 minutes
- **Tenant Uptime**: > 99.9%
- **API Availability**: > 99.9%
- **Billing Accuracy**: > 99.9%
- **Customer Satisfaction**: > 4.5/5.0

---

## Integration Points / Related Skills

### Upstream Skills
- **136. Business to Technical Spec**: Requirements
- **137. API-First Product Strategy**: API design
- **18. Project Management**: Project planning

### Parallel Skills
- **139. Product Discovery Validation**: Validation
- **140. Product Analytics Implementation**: Analytics
- **141. Feature Prioritization**: Prioritization
- **142. Technical Debt Prioritization**: Debt management

### Downstream Skills
- **143. Competitive Intelligence**: Competitive analysis
- **144. Product Roadmap Communication**: Roadmap
- **145. Cross-Functional Leadership**: Leadership

### Cross-Domain Skills
- **14. Monitoring and Observability**: Platform monitoring
- **15. DevOps Infrastructure**: Infrastructure
- **81. SaaS FinOps Pricing**: Pricing strategy
- **84. Compliance AI Governance**: Compliance

---

## References & Resources

### Documentation
- [Multi-Tenancy Patterns](https://www.microsoft.com/en-us/azure/architecture/patterns/multi-tenancy)
- [PostgreSQL Row Level Security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
- [Kubernetes Multi-Tenancy](https://kubernetes.io/docs/concepts/security/multi-tenancy/)
- [Keycloak Documentation](https://www.keycloak.org/documentation/)

### Best Practices
- [SaaS Multi-Tenancy Best Practices](https://www.heroku.com/papers/saas-multi-tenancy)
- [Platform Design Best Practices](https://www.platformeddesign.com/)
- [SaaS Pricing Best Practices](https://www.pricing-design.com/)

### Tools & Libraries
- [Keycloak](https://www.keycloak.org/)
- [Stripe](https://stripe.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Redis](https://redis.io/)
