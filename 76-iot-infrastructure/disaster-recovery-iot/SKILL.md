---
name: Disaster Recovery for IoT
description: Comprehensive disaster recovery planning and implementation for IoT infrastructure and systems
---

# Disaster Recovery for IoT

## Current Level: Expert (Enterprise Scale)

## Domain: IoT Infrastructure
## Skill ID: 90

---

## Executive Summary

Disaster Recovery for IoT provides comprehensive strategies and implementations for recovering IoT infrastructure from catastrophic failures, including data loss, service outages, and regional disasters. This capability is essential for maintaining business continuity and minimizing downtime for mission-critical IoT deployments.

### Strategic Necessity

- **Business Continuity**: Maintain operations during disasters
- **Data Protection**: Prevent permanent data loss
- **Service Availability**: Minimize downtime
- **Compliance**: Meet regulatory requirements for disaster recovery
- **Customer Trust**: Demonstrate reliability and resilience

---

## Technical Deep Dive

### Disaster Recovery Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    IoT Disaster Recovery Architecture                        │
│                                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│  │   Primary    │    │   Secondary  │    │   Tertiary  │                  │
│  │   Region    │    │   Region    │    │   Region    │                  │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘                  │
│         │                   │                   │                           │
│         ▼                   ▼                   ▼                           │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Replication Layer                               │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Data     │  │  Config   │  │  State    │  │  Backup  │            │   │
│  │  │  Replication│  │  Sync     │  │  Sync     │  │  Storage │            │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘            │   │
│  └───────┼────────────┼────────────┼────────────┼────────────────────┘   │
│          │            │            │            │                         │
│          ▼            ▼            ▼            ▼                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Failover Layer                                 │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  DNS      │  │  Load     │  │  Service  │  │  Auto    │            │   │
│  │  │  Failover │  │  Balancer │  │  Mesh     │  │  Scaling │            │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘            │   │
│  └───────┼────────────┼────────────┼────────────┼────────────────────┘   │
│          │            │            │            │                         │
│          ▼            ▼            ▼            ▼                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Monitoring & Recovery                           │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Health   │  │  Metrics  │  │  Alerts   │  │  Recovery│            │   │
│  │  │  Checks   │  │  Collection│  │  & Notify │  │  Scripts │            │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Disaster Recovery Planning

```python
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import asyncio
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class DisasterType(Enum):
    """Types of disasters"""
    REGIONAL_OUTAGE = "regional_outage"
    DATA_CORRUPTION = "data_corruption"
    NETWORK_FAILURE = "network_failure"
    SECURITY_BREACH = "security_breach"
    NATURAL_DISASTER = "natural_disaster"
    HUMAN_ERROR = "human_error"

class RecoveryTier(Enum):
    """Recovery tiers"""
    TIER_1 = "tier_1"  # Hot standby, < 1 hour RTO
    TIER_2 = "tier_2"  # Warm standby, < 4 hour RTO
    TIER_3 = "tier_3"  # Cold standby, < 24 hour RTO
    TIER_4 = "tier_4"  # Backup only, < 72 hour RTO

@dataclass
class RecoveryObjective:
    """Recovery objectives"""
    rto_hours: float  # Recovery Time Objective
    rpo_hours: float  # Recovery Point Objective
    tier: RecoveryTier

@dataclass
class DisasterRecoveryPlan:
    """Disaster recovery plan"""
    plan_id: str
    name: str
    description: str
    disaster_types: List[DisasterType]
    recovery_objectives: RecoveryObjective
    primary_region: str
    secondary_region: str
    tertiary_region: Optional[str]
    failover_procedures: List[str]
    rollback_procedures: List[str]
    contact_list: Dict[str, List[str]]
    test_schedule: str

class DisasterRecoveryPlanner:
    """Disaster recovery planner"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.plans = {}
        self.testing_manager = TestingManager(config['testing'])
        self.orchestrator = RecoveryOrchestrator(config['orchestration'])
        
    def create_plan(
        self,
        plan_config: Dict[str, Any]
    ) -> DisasterRecoveryPlan:
        """Create disaster recovery plan"""
        logger.info(f"Creating disaster recovery plan: {plan_config['name']}")
        
        plan = DisasterRecoveryPlan(
            plan_id=plan_config['plan_id'],
            name=plan_config['name'],
            description=plan_config['description'],
            disaster_types=[
                DisasterType(dt) for dt in plan_config['disaster_types']
            ],
            recovery_objectives=RecoveryObjective(
                rto_hours=plan_config['rto_hours'],
                rpo_hours=plan_config['rpo_hours'],
                tier=RecoveryTier(plan_config['tier'])
            ),
            primary_region=plan_config['primary_region'],
            secondary_region=plan_config['secondary_region'],
            tertiary_region=plan_config.get('tertiary_region'),
            failover_procedures=plan_config['failover_procedures'],
            rollback_procedures=plan_config['rollback_procedures'],
            contact_list=plan_config['contact_list'],
            test_schedule=plan_config['test_schedule']
        )
        
        self.plans[plan.plan_id] = plan
        
        logger.info(f"Plan created: {plan.plan_id}")
        
        return plan
    
    def get_plan(self, plan_id: str) -> DisasterRecoveryPlan:
        """Get disaster recovery plan"""
        if plan_id not in self.plans:
            raise ValueError(f"Plan not found: {plan_id}")
        return self.plans[plan_id]
    
    async def execute_plan(
        self,
        plan_id: str,
        disaster_type: DisasterType,
        affected_resources: List[str]
    ) -> Dict[str, Any]:
        """Execute disaster recovery plan"""
        logger.info(
            f"Executing disaster recovery plan: {plan_id} "
            f"for disaster: {disaster_type.value}"
        )
        
        plan = self.get_plan(plan_id)
        
        # Validate disaster type
        if disaster_type not in plan.disaster_types:
            raise ValueError(
                f"Disaster type {disaster_type.value} not covered by plan"
            )
        
        # Execute failover
        result = await self.orchestrator.execute_failover(
            plan,
            disaster_type,
            affected_resources
        )
        
        # Log execution
        await self._log_execution(plan_id, disaster_type, result)
        
        return result
    
    async def _log_execution(
        self,
        plan_id: str,
        disaster_type: DisasterType,
        result: Dict[str, Any]
    ):
        """Log disaster recovery execution"""
        # Log to audit system
        # Send notifications
        # Update metrics
        pass

class RecoveryOrchestrator:
    """Recovery orchestrator"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.dns_manager = DNSManager(config['dns'])
        self.load_balancer = LoadBalancerManager(config['load_balancer'])
        self.service_mesh = ServiceMeshManager(config['service_mesh'])
        self.backup_manager = BackupManager(config['backup'])
        self.monitoring = MonitoringSystem(config['monitoring'])
        
    async def execute_failover(
        self,
        plan: DisasterRecoveryPlan,
        disaster_type: DisasterType,
        affected_resources: List[str]
    ) -> Dict[str, Any]:
        """Execute failover procedures"""
        logger.info("Starting failover procedures...")
        
        start_time = datetime.utcnow()
        
        try:
            # Step 1: Assess impact
            logger.info("Assessing disaster impact...")
            impact_assessment = await self._assess_impact(
                disaster_type,
                affected_resources
            )
            
            # Step 2: Notify stakeholders
            logger.info("Notifying stakeholders...")
            await self._notify_stakeholders(plan, impact_assessment)
            
            # Step 3: Activate secondary region
            logger.info(f"Activating secondary region: {plan.secondary_region}...")
            await self._activate_secondary_region(plan, impact_assessment)
            
            # Step 4: Failover DNS
            logger.info("Failing over DNS...")
            await self._failover_dns(plan, plan.secondary_region)
            
            # Step 5: Update load balancer
            logger.info("Updating load balancer...")
            await self._update_load_balancer(plan, plan.secondary_region)
            
            # Step 6: Restore data
            logger.info("Restoring data...")
            await self._restore_data(plan, impact_assessment)
            
            # Step 7: Verify recovery
            logger.info("Verifying recovery...")
            verification_result = await self._verify_recovery(plan)
            
            # Step 8: Monitor recovery
            logger.info("Monitoring recovery...")
            await self._monitor_recovery(plan)
            
            end_time = datetime.utcnow()
            rto = (end_time - start_time).total_seconds() / 3600.0
            
            result = {
                'status': 'success',
                'rto_hours': rto,
                'rto_met': rto <= plan.recovery_objectives.rto_hours,
                'verification_result': verification_result,
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat()
            }
            
            logger.info(f"Failover completed in {rto:.2f} hours")
            
            return result
            
        except Exception as e:
            logger.error(f"Failover failed: {e}")
            
            # Attempt rollback
            logger.info("Attempting rollback...")
            await self._execute_rollback(plan)
            
            return {
                'status': 'failed',
                'error': str(e),
                'rollback_attempted': True
            }
    
    async def _assess_impact(
        self,
        disaster_type: DisasterType,
        affected_resources: List[str]
    ) -> Dict[str, Any]:
        """Assess disaster impact"""
        # Determine affected services
        # Estimate data loss
        # Calculate business impact
        # Identify dependencies
        
        return {
            'affected_services': affected_resources,
            'estimated_data_loss_hours': 1.0,
            'business_impact': 'high',
            'dependencies': []
        }
    
    async def _notify_stakeholders(
        self,
        plan: DisasterRecoveryPlan,
        impact_assessment: Dict[str, Any]
    ):
        """Notify stakeholders"""
        # Send notifications based on severity
        # Use multiple channels (email, SMS, Slack)
        # Include incident details and ETA
        
        for role, contacts in plan.contact_list.items():
            for contact in contacts:
                await self._send_notification(
                    contact,
                    role,
                    impact_assessment
                )
    
    async def _send_notification(
        self,
        contact: str,
        role: str,
        impact_assessment: Dict[str, Any]
    ):
        """Send notification to contact"""
        # Implementation depends on notification channel
        pass
    
    async def _activate_secondary_region(
        self,
        plan: DisasterRecoveryPlan,
        impact_assessment: Dict[str, Any]
    ):
        """Activate secondary region"""
        # Scale up secondary region
        # Start services
        # Configure networking
        # Connect to data sources
        
        # Use service mesh to route traffic
        await self.service_mesh.activate_region(plan.secondary_region)
    
    async def _failover_dns(
        self,
        plan: DisasterRecoveryPlan,
        target_region: str
    ):
        """Failover DNS to target region"""
        # Update DNS records
        # Reduce TTL for faster propagation
        # Verify DNS changes
        
        await self.dns_manager.update_records(
            plan.primary_region,
            target_region
        )
    
    async def _update_load_balancer(
        self,
        plan: DisasterRecoveryPlan,
        target_region: str
    ):
        """Update load balancer configuration"""
        # Add target region endpoints
        # Remove primary region endpoints
        # Update health checks
        
        await self.load_balancer.update_targets(
            target_region
        )
    
    async def _restore_data(
        self,
        plan: DisasterRecoveryPlan,
        impact_assessment: Dict[str, Any]
    ):
        """Restore data from backups"""
        # Determine recovery point
        # Restore from backup
        # Verify data integrity
        # Apply transaction logs
        
        rpo_hours = plan.recovery_objectives.rpo_hours
        recovery_point = datetime.utcnow() - timedelta(hours=rpo_hours)
        
        await self.backup_manager.restore(
            recovery_point,
            plan.secondary_region
        )
    
    async def _verify_recovery(
        self,
        plan: DisasterRecoveryPlan
    ) -> Dict[str, Any]:
        """Verify recovery was successful"""
        # Run health checks
        # Verify data integrity
        # Test functionality
        # Measure performance
        
        health_checks = await self.monitoring.run_health_checks(
            plan.secondary_region
        )
        
        return {
            'all_healthy': all(check['healthy'] for check in health_checks),
            'health_checks': health_checks,
            'data_integrity': await self._verify_data_integrity(plan)
        }
    
    async def _verify_data_integrity(
        self,
        plan: DisasterRecoveryPlan
    ) -> bool:
        """Verify data integrity"""
        # Compare checksums
        # Validate data consistency
        # Check for corruption
        
        return True
    
    async def _monitor_recovery(
        self,
        plan: DisasterRecoveryPlan
    ):
        """Monitor recovery progress"""
        # Monitor system health
        # Track performance metrics
        # Alert on issues
        # Generate reports
        
        await self.monitoring.start_monitoring(plan.secondary_region)
    
    async def _execute_rollback(
        self,
        plan: DisasterRecoveryPlan
    ):
        """Execute rollback procedures"""
        logger.info("Executing rollback procedures...")
        
        for procedure in plan.rollback_procedures:
            logger.info(f"Executing: {procedure}")
            # Execute rollback step
            await self._execute_procedure(procedure)
        
        # Failback DNS
        await self._failover_dns(plan, plan.primary_region)
        
        # Update load balancer
        await self._update_load_balancer(plan, plan.primary_region)
        
        logger.info("Rollback completed")

class BackupManager:
    """Backup manager for disaster recovery"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.backup_locations = config['backup_locations']
        
    async def create_backup(
        self,
        source_region: str,
        backup_type: str = "full"
    ) -> str:
        """Create backup of region data"""
        logger.info(f"Creating {backup_type} backup for {source_region}...")
        
        backup_id = f"backup_{source_region}_{int(datetime.utcnow().timestamp())}"
        
        # Create snapshot of databases
        # Copy configuration
        # Archive logs
        # Store in multiple locations
        
        # Store in primary backup location
        await self._store_backup(
            backup_id,
            source_region,
            self.backup_locations['primary']
        )
        
        # Replicate to secondary backup location
        await self._store_backup(
            backup_id,
            source_region,
            self.backup_locations['secondary']
        )
        
        logger.info(f"Backup created: {backup_id}")
        
        return backup_id
    
    async def _store_backup(
        self,
        backup_id: str,
        source_region: str,
        location: Dict[str, Any]
    ):
        """Store backup in specified location"""
        # Implementation depends on storage type
        # S3, Azure Blob, GCS, etc.
        pass
    
    async def restore(
        self,
        recovery_point: datetime,
        target_region: str
    ):
        """Restore backup to target region"""
        logger.info(f"Restoring backup to {target_region}...")
        
        # Find backup closest to recovery point
        backup_id = await self._find_backup(recovery_point)
        
        # Restore to target region
        await self._restore_backup(backup_id, target_region)
        
        logger.info("Backup restored")
    
    async def _find_backup(
        self,
        recovery_point: datetime
    ) -> str:
        """Find backup closest to recovery point"""
        # Search backup catalog
        # Find backup with RPO <= requested
        # Return backup ID
        pass
    
    async def _restore_backup(
        self,
        backup_id: str,
        target_region: str
    ):
        """Restore backup to target region"""
        # Download backup
        # Extract data
        # Restore to systems
        # Verify integrity
        pass

class TestingManager:
    """Disaster recovery testing manager"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.test_history = {}
        
    async def run_drill(
        self,
        plan_id: str,
        scenario: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Run disaster recovery drill"""
        logger.info(f"Running DR drill for plan: {plan_id}")
        
        drill_id = f"drill_{plan_id}_{int(datetime.utcnow().timestamp())}"
        
        # Simulate disaster
        logger.info("Simulating disaster...")
        affected_resources = await self._simulate_disaster(scenario)
        
        # Execute recovery plan
        logger.info("Executing recovery plan...")
        # This would call the recovery orchestrator
        result = await self._execute_recovery(plan_id, affected_resources)
        
        # Evaluate results
        logger.info("Evaluating drill results...")
        evaluation = self._evaluate_drill_result(result, scenario)
        
        # Record drill
        self.test_history[drill_id] = {
            'plan_id': plan_id,
            'scenario': scenario,
            'result': result,
            'evaluation': evaluation,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        return {
            'drill_id': drill_id,
            'result': result,
            'evaluation': evaluation
        }
    
    async def _simulate_disaster(
        self,
        scenario: Dict[str, Any]
    ) -> List[str]:
        """Simulate disaster scenario"""
        # Simulate regional outage
        # Simulate network failure
        # Simulate data corruption
        # Return affected resources
        
        return []
    
    async def _execute_recovery(
        self,
        plan_id: str,
        affected_resources: List[str]
    ) -> Dict[str, Any]:
        """Execute recovery plan"""
        # This would call the recovery orchestrator
        pass
    
    def _evaluate_drill_result(
        self,
        result: Dict[str, Any],
        scenario: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Evaluate drill results"""
        return {
            'rto_met': result.get('rto_met', False),
            'rpo_met': True,  # Assuming backup was recent enough
            'all_healthy': result.get('verification_result', {}).get('all_healthy', False),
            'lessons_learned': [],
            'improvements_needed': []
        }

class DNSManager:
    """DNS manager for failover"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def update_records(
        self,
        primary_region: str,
        target_region: str
    ):
        """Update DNS records for failover"""
        # Update A records
        # Update CNAME records
        # Set low TTL
        pass

class LoadBalancerManager:
    """Load balancer manager for failover"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def update_targets(
        self,
        target_region: str
    ):
        """Update load balancer targets"""
        # Add target region endpoints
        # Remove failed region endpoints
        # Update health checks
        pass

class ServiceMeshManager:
    """Service mesh manager for failover"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def activate_region(
        self,
        region: str
    ):
        """Activate region in service mesh"""
        # Update service mesh configuration
        # Route traffic to region
        # Update service discovery
        pass

class MonitoringSystem:
    """Monitoring system for disaster recovery"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def run_health_checks(
        self,
        region: str
    ) -> List[Dict[str, Any]]:
        """Run health checks for region"""
        # Check service health
        # Check database connectivity
        # Check network connectivity
        # Return results
        pass
    
    async def start_monitoring(
        self,
        region: str
    ):
        """Start monitoring for region"""
        # Start health checks
        # Collect metrics
        # Send alerts on issues
        pass
```

### Automated Recovery Scripts

```bash
#!/bin/bash
# scripts/automated_recovery.sh

set -e

# Configuration
PLAN_ID="${PLAN_ID:-iot-primary-dr}"
DISASTER_TYPE="${DISASTER_TYPE:-regional_outage}"
AFFECTED_REGION="${AFFECTED_REGION:-us-west-2}"
TARGET_REGION="${TARGET_REGION:-us-east-1}"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# Step 1: Validate environment
log_info "Step 1: Validating environment..."
if [ -z "$PLAN_ID" ]; then
    log_error "PLAN_ID not set"
    exit 1
fi

if [ -z "$TARGET_REGION" ]; then
    log_error "TARGET_REGION not set"
    exit 1
fi

log_info "Environment validated"

# Step 2: Check primary region status
log_info "Step 2: Checking primary region status..."
PRIMARY_STATUS=$(aws ec2 describe-region-status --region-name $AFFECTED_REGION --query "RegionStatus[0].Status" --output text)

if [ "$PRIMARY_STATUS" != "impaired" ]; then
    log_warn "Primary region is not impaired. Aborting failover."
    exit 0
fi

log_info "Primary region is impaired. Proceeding with failover."

# Step 3: Activate secondary region
log_info "Step 3: Activating secondary region..."
kubectl config use-context $TARGET_REGION

# Scale up services
kubectl scale deployment iot-gateway --replicas=10 -n iot-gateway
kubectl scale deployment iot-data-processor --replicas=5 -n iot-data-processor

# Wait for pods to be ready
kubectl wait --for=condition=ready pod -l app=iot-gateway -n iot-gateway --timeout=300s
kubectl wait --for=condition=ready pod -l app=iot-data-processor -n iot-data-processor --timeout=300s

log_info "Secondary region activated"

# Step 4: Failover DNS
log_info "Step 4: Failing over DNS..."
# Update Route53 records
aws route53 change-resource-record-sets \
    --hosted-zone-id $HOSTED_ZONE_ID \
    --change-batch file://dns-failover.json

# Wait for DNS propagation
log_info "Waiting for DNS propagation..."
sleep 60

log_info "DNS failover completed"

# Step 5: Update load balancer
log_info "Step 5: Updating load balancer..."
# Update target groups
aws elbv2 modify-target-group-attributes \
    --target-group-arn $TARGET_GROUP_ARN \
    --attributes Key=deregistration_delay.timeout_seconds,Value=30

# Register targets in new region
aws elbv2 register-targets \
    --target-group-arn $TARGET_GROUP_ARN \
    --targets Id=$TARGET_INSTANCE_1,Port=8080 Id=$TARGET_INSTANCE_2,Port=8080

log_info "Load balancer updated"

# Step 6: Restore data
log_info "Step 6: Restoring data..."
# Restore from backup
python scripts/restore_backup.py \
    --backup-id $BACKUP_ID \
    --target-region $TARGET_REGION

log_info "Data restored"

# Step 7: Verify recovery
log_info "Step 7: Verifying recovery..."
# Run health checks
HEALTH_CHECK_URL="https://$TARGET_REGION.iot.example.com/health"

for i in {1..10}; do
    if curl -f -s $HEALTH_CHECK_URL > /dev/null; then
        log_info "Health check passed"
        break
    fi
    log_warn "Health check failed, retrying... ($i/10)"
    sleep 10
done

# Step 8: Start monitoring
log_info "Step 8: Starting monitoring..."
# Enable monitoring in new region
python scripts/enable_monitoring.py --region $TARGET_REGION

log_info "Monitoring enabled"

# Step 9: Notify stakeholders
log_info "Step 9: Notifying stakeholders..."
# Send notification
python scripts/notify_stakeholders.py \
    --plan-id $PLAN_ID \
    --status "recovered" \
    --region $TARGET_REGION

log_info "Stakeholders notified"

# Step 10: Log recovery
log_info "Step 10: Logging recovery..."
python scripts/log_recovery.py \
    --plan-id $PLAN_ID \
    --disaster-type $DISASTER_TYPE \
    --affected-region $AFFECTED_REGION \
    --target-region $TARGET_REGION

log_info "Recovery logged"

log_info "Automated recovery completed successfully!"
```

---

## Tooling & Tech Stack

### Backup & Recovery
- **AWS Backup**: AWS backup service
- **Azure Backup**: Azure backup service
- **Google Cloud Backup**: GCP backup service
- **Veeam**: Enterprise backup solution

### DNS & Load Balancing
- **Route53**: AWS DNS
- **Azure DNS**: Azure DNS
- **Cloud DNS**: GCP DNS
- **Cloudflare**: Global DNS

### Monitoring & Alerting
- **Prometheus**: Metrics collection
- **Grafana**: Visualization
- **PagerDuty**: Incident response
- **Opsgenie**: Incident management

### Automation
- **Terraform**: Infrastructure as code
- **Ansible**: Configuration management
- **AWS Lambda**: Serverless functions
- **Azure Functions**: Serverless functions

---

## Configuration Essentials

### Disaster Recovery Configuration

```yaml
# config/disaster_recovery.yaml
plans:
  iot-primary-dr:
    plan_id: "iot-primary-dr"
    name: "IoT Primary Disaster Recovery"
    description: "Primary disaster recovery plan for IoT infrastructure"
    
    disaster_types:
      - "regional_outage"
      - "data_corruption"
      - "network_failure"
    
    recovery_objectives:
      rto_hours: 1.0
      rpo_hours: 1.0
      tier: "tier_1"
    
    primary_region: "us-west-2"
    secondary_region: "us-east-1"
    tertiary_region: "eu-west-1"
    
    failover_procedures:
      - "Assess disaster impact"
      - "Notify stakeholders"
      - "Activate secondary region"
      - "Failover DNS"
      - "Update load balancer"
      - "Restore data"
      - "Verify recovery"
      - "Monitor recovery"
    
    rollback_procedures:
      - "Verify primary region recovery"
      - "Restore primary region"
      - "Failback DNS"
      - "Update load balancer"
      - "Verify failback"
    
    contact_list:
      executive:
        - "exec@example.com"
      operations:
        - "ops@example.com"
      engineering:
        - "eng@example.com"
      support:
        - "support@example.com"
    
    test_schedule: "quarterly"

backup:
  locations:
    primary:
      provider: "aws"
      region: "us-east-1"
      bucket: "iot-backups-primary"
    
    secondary:
      provider: "azure"
      region: "eastus"
      container: "iot-backups-secondary"
  
  retention:
    daily: 7
    weekly: 4
    monthly: 12
    yearly: 3
  
  encryption:
    enabled: true
    algorithm: "AES-256"
  
  compression:
    enabled: true
    algorithm: "gzip"

monitoring:
  health_check_interval: 60  # seconds
  alert_thresholds:
    error_rate: 0.05
    latency_ms: 5000
    availability: 0.95
  
  alert_channels:
    - type: "slack"
      webhook: "${SLACK_WEBHOOK_URL}"
    - type: "pagerduty"
      integration_key: "${PAGERDUTY_INTEGRATION_KEY}"
    - type: "email"
      recipients: ["team@example.com"]

testing:
  schedule: "quarterly"
  scenarios:
    - name: "regional_outage"
      type: "regional_outage"
      affected_region: "us-west-2"
      duration_hours: 1
    
    - name: "data_corruption"
      type: "data_corruption"
      affected_services: ["database"]
      duration_hours: 2
```

---

## Code Examples

### Good: Complete DR Plan Execution

```python
# disaster_recovery/execute.py
import asyncio
import logging
from typing import Dict, Any

from disaster_recovery.planner import DisasterRecoveryPlanner
from disaster_recovery.orchestrator import RecoveryOrchestrator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def execute_disaster_recovery():
    """Execute disaster recovery plan"""
    logger.info("=" * 60)
    logger.info("Disaster Recovery Execution")
    logger.info("=" * 60)
    
    # Load configuration
    config = load_config('config/disaster_recovery.yaml')
    
    # Create planner
    planner = DisasterRecoveryPlanner(config)
    
    # Get plan
    plan = planner.get_plan('iot-primary-dr')
    
    # Define disaster scenario
    disaster_type = DisasterType.REGIONAL_OUTAGE
    affected_resources = [
        'iot-gateway',
        'iot-data-processor',
        'iot-database'
    ]
    
    # Execute plan
    logger.info(f"Executing plan: {plan.name}")
    logger.info(f"Disaster type: {disaster_type.value}")
    logger.info(f"Affected resources: {affected_resources}")
    
    result = await planner.execute_plan(
        plan.plan_id,
        disaster_type,
        affected_resources
    )
    
    # Print results
    logger.info("\n" + "=" * 60)
    logger.info("Recovery Results")
    logger.info("=" * 60)
    logger.info(f"Status: {result['status']}")
    logger.info(f"RTO: {result['rto_hours']:.2f} hours")
    logger.info(f"RTO Met: {result['rto_met']}")
    
    if result['status'] == 'success':
        verification = result['verification_result']
        logger.info(f"All Healthy: {verification['all_healthy']}")
        logger.info(f"Data Integrity: {verification['data_integrity']}")
        
        logger.info("\nRecovery completed successfully!")
    else:
        logger.error(f"Recovery failed: {result.get('error')}")
        logger.info(f"Rollback attempted: {result.get('rollback_attempted')}")

def load_config(filename: str) -> Dict[str, Any]:
    """Load configuration from file"""
    import yaml
    with open(filename, 'r') as f:
        return yaml.safe_load(f)

async def main():
    """Main entry point"""
    await execute_disaster_recovery()

if __name__ == "__main__":
    asyncio.run(main())
```

### Bad: Anti-pattern Example

```bash
# BAD: No automated recovery
# Manual failover required

# BAD: No testing
# Never test DR plan

# BAD: No monitoring
# Can't detect failures

# BAD: No backups
# No data protection

# BAD: No documentation
# No procedures documented
```

---

## Standards, Compliance & Security

### Industry Standards
- **ISO 22301**: Business continuity management
- **NIST SP 800-34**: Contingency planning
- **SOC 2**: Security and availability
- **HIPAA**: Healthcare data protection

### Security Best Practices
- **Encryption**: Encrypt all backups
- **Access Control**: Restrict backup access
- **Audit Logging**: Track all recovery actions
- **Multi-Factor**: Require MFA for recovery

### Compliance Requirements
- **RTO/RPO**: Documented and tested
- **Data Retention**: Meet regulatory requirements
- **Testing**: Regular DR drills
- **Documentation**: Complete procedures

---

## Quick Start

### 1. Create DR Plan

```python
from disaster_recovery.planner import DisasterRecoveryPlanner

config = load_config('config/disaster_recovery.yaml')
planner = DisasterRecoveryPlanner(config)

plan_config = {
    'plan_id': 'iot-primary-dr',
    'name': 'IoT Primary Disaster Recovery',
    'description': 'Primary DR plan for IoT',
    'disaster_types': ['regional_outage', 'data_corruption'],
    'rto_hours': 1.0,
    'rpo_hours': 1.0,
    'tier': 'tier_1',
    'primary_region': 'us-west-2',
    'secondary_region': 'us-east-1',
    'failover_procedures': [...],
    'rollback_procedures': [...],
    'contact_list': {...},
    'test_schedule': 'quarterly'
}

plan = planner.create_plan(plan_config)
```

### 2. Create Backup

```python
from disaster_recovery.backup import BackupManager

config = load_config('config/disaster_recovery.yaml')
backup_manager = BackupManager(config['backup'])

backup_id = await backup_manager.create_backup(
    'us-west-2',
    'full'
)
```

### 3. Run DR Drill

```python
from disaster_recovery.testing import TestingManager

config = load_config('config/disaster_recovery.yaml')
testing_manager = TestingManager(config['testing'])

scenario = {
    'name': 'regional_outage',
    'type': 'regional_outage',
    'affected_region': 'us-west-2',
    'duration_hours': 1
}

result = await testing_manager.run_drill(
    'iot-primary-dr',
    scenario
)
```

---

## Production Checklist

### Planning
- [ ] DR plans documented
- [ ] RTO/RPO defined
- [ ] Contact lists updated
- [ ] Procedures documented
- [ ] Stakeholders trained

### Backup
- [ ] Regular backups scheduled
- [ ] Backups encrypted
- [ ] Offsite copies
- [ ] Backup verification
- [ ] Retention policy

### Testing
- [ ] DR drills scheduled
- [ ] Test scenarios defined
- [ ] Results documented
- [ ] Improvements implemented
- [ ] Team trained

### Monitoring
- [ ] Health checks configured
- [ ] Alerting configured
- [ ] Metrics collected
- [ ] Dashboards configured
- [ ] Runbooks documented

### Recovery
- [ ] Automated scripts ready
- [ ] Rollback procedures
- [ ] Communication plan
- [ ] Post-recovery verification
- [ ] Lessons learned documented

---

## Anti-patterns

### ❌ Avoid These Practices

1. **No Automated Recovery**
   ```bash
   # BAD: Manual recovery
   # Requires manual intervention
   ```

2. **No Testing**
   ```bash
   # BAD: No testing
   # Never test DR plan
   ```

3. **No Monitoring**
   ```bash
   # BAD: No monitoring
   # Can't detect failures
   ```

4. **No Backups**
   ```bash
   # BAD: No backups
   # No data protection
   ```

5. **No Documentation**
   ```bash
   # BAD: No documentation
   # No procedures documented
   ```

### ✅ Follow These Practices

1. **Automated Recovery**
   ```bash
   # GOOD: Automated recovery
   ./scripts/automated_recovery.sh
   ```

2. **Regular Testing**
   ```bash
   # GOOD: Regular testing
   python scripts/run_drill.py
   ```

3. **Monitoring**
   ```bash
   # GOOD: Active monitoring
   ./scripts/enable_monitoring.py
   ```

4. **Regular Backups**
   ```bash
   # GOOD: Regular backups
   python scripts/create_backup.py
   ```

5. **Documentation**
   ```bash
   # GOOD: Complete documentation
   # All procedures documented
   ```

---

## Unit Economics & KPIs

### Development Costs
- **Initial Setup**: 60-100 hours
- **Plan Development**: 40-60 hours
- **Script Development**: 40-60 hours
- **Total**: 140-220 hours

### Operational Costs
- **Backup Storage**: $500-2000/month
- **Secondary Region**: $1000-5000/month
- **Monitoring**: $100-300/month
- **Testing**: 20-40 hours/quarter

### ROI Metrics
- **Downtime Reduction**: 90-95% reduction
- **Data Loss Prevention**: 100%
- **Recovery Time**: < 1 hour vs days
- **Customer Trust**: Significant improvement

### KPI Targets
- **RTO**: < 1 hour (Tier 1)
- **RPO**: < 1 hour (Tier 1)
- **Backup Success Rate**: > 99%
- **Recovery Success Rate**: > 95%
- **Test Coverage**: 100%

---

## Integration Points / Related Skills

### Upstream Skills
- **86. Advanced IaC IoT**: Infrastructure provisioning
- **87. Chaos Engineering IoT**: Resilience testing
- **88. GitOps IoT Infrastructure**: GitOps implementation

### Parallel Skills
- **89. Multi-Cloud IoT**: Multi-cloud strategy
- **73. Differential OTA Updates**: OTA deployment
- **74. Atomic AB Partitioning**: Firmware updates
- **75. Fleet Campaign Management**: Fleet management

### Downstream Skills
- **14. Monitoring and Observability**: Metrics and tracing
- **24. Security Practices**: Infrastructure security
- **81. SaaS FinOps Pricing**: Cost optimization
- **84. Compliance AI Governance**: Compliance

### Cross-Domain Skills
- **15. DevOps Infrastructure**: CI/CD pipelines
- **59. Architecture Decision**: Architecture decisions
- **64. Meta Standards**: Coding standards
- **72. Metacognitive Skill Architect**: System design

---

## References & Resources

### Documentation
- [AWS Disaster Recovery](https://aws.amazon.com/disaster-recovery/)
- [Azure Disaster Recovery](https://azure.microsoft.com/en-us/solutions/disaster-recovery/)
- [Google Cloud Disaster Recovery](https://cloud.google.com/solutions/disaster-recovery)
- [NIST SP 800-34](https://csrc.nist.gov/publications/detail/sp/800-34/rev-1/final)

### Best Practices
- [Disaster Recovery Best Practices](https://www.druva.com/resources/whitepapers/disaster-recovery-best-practices/)
- [AWS DR Best Practices](https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-workloads-on-aws.html)
- [Azure DR Best Practices](https://docs.microsoft.com/en-us/azure/architecture/resiliency/disaster-recovery-azure-applications)

### Tools & Libraries
- [AWS Backup](https://aws.amazon.com/backup/)
- [Azure Backup](https://azure.microsoft.com/en-us/services/backup/)
- [Veeam Backup](https://www.veeam.com/)
- [Rubrik](https://www.rubrik.com/)
