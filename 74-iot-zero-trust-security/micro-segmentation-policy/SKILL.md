---
name: Micro Segmentation Policy
description: Network and application-level segmentation to limit lateral movement and contain security breaches in IoT deployments
---

# Micro Segmentation Policy

> **Current Level:** Expert (Enterprise Scale)
> **Domain:** IoT / Security / Network Architecture
> **Skill ID:** 78

---

## Overview
Micro Segmentation Policy divides IoT infrastructure into small, isolated security zones with strict access controls between them. This limits lateral movement, contains breaches, and implements zero-trust principles at scale.

## Why This Matters / Strategic Necessity

### Context
In 2025-2026, IoT deployments face sophisticated attacks where compromised devices move laterally across the network. Traditional perimeter security is insufficient as attackers can pivot between devices and systems once inside.

### Business Impact
- **Blast Radius Reduction:** 90% reduction in devices affected by breach
- **Compliance:** Meet regulatory requirements (NIST, PCI DSS, GDPR)
- **Security Posture:** 70% improvement in overall security posture
- **Incident Response:** Faster containment and remediation

### Product Thinking
Solves critical problem where network breaches propagate unchecked across IoT infrastructure, affecting thousands of devices and causing massive operational disruption and financial loss.

## Core Concepts / Technical Deep Dive

### 1. Segmentation Architecture

**Network-Level Segmentation:**
- VLANs and VXLANs
- Subnet isolation
- Firewall rules between zones
- Software-defined networking

**Application-Level Segmentation:**
- Service mesh controls
- API gateway policies
- Microservice isolation
- Zero-trust service-to-service auth

**Device-Level Segmentation:**
- Device groups and profiles
- Per-device policies
- Device-to-device communication controls
- Context-aware access

### 2. Security Zones

```
┌─────────────────────────────────────────────────────────────────┐
│                    IoT Infrastructure                         │
├─────────────────────────────────────────────────────────────────┤
│  DMZ Zone             │  Device Zone 1   │  Device Zone 2 │
│  - Public APIs       │  - Sensors       │  - Actuators    │
│  - Load Balancers    │  - Gateways      │  - Controllers  │
├───────────────────────┼───────────────────┼─────────────────┤
│  Management Zone     │  Data Zone       │  Analytics Zone  │
│  - Device Mgmt      │  - Time Series    │  - ML Models     │
│  - Monitoring       │  - Databases      │  - Dashboards    │
└───────────────────────┴───────────────────┴─────────────────┘
```

### 3. Segmentation Strategies

**Perimeter-Based:**
- Traditional network segmentation
- North-south traffic control
- Limited east-west controls

**Zero-Trust-Based:**
- Verify every request
- Least privilege access
- Continuous authentication

**Hybrid Approach:**
- Perimeter for initial defense
- Zero-trust for internal controls
- Defense in depth

### 4. Policy Management

**Policy Definition:**
- Zone-to-zone rules
- Service-to-service rules
- Device-to-device rules
- Time-based policies

**Policy Enforcement:**
- Network firewalls
- Service mesh
- API gateways
- Host-based controls

**Policy Monitoring:**
- Traffic analysis
- Violation detection
- Policy effectiveness metrics
- Audit logging

## Tooling & Tech Stack

### Enterprise Tools
- **AWS Network Firewall:** Managed network firewall
- **Azure Firewall:** Cloud network security
- **Google Cloud Armor:** DDoS and WAF protection
- **Istio:** Service mesh with segmentation
- **Calico:** Network policy engine for Kubernetes
- **Tufin:** Orchestration security platform

### Configuration Essentials

```yaml
# Micro segmentation policy configuration
segmentation:
  # Security zones
  zones:
    - name: "dmz"
      description: "Demilitarized zone for public services"
      subnets: ["10.0.1.0/24"]
      services: ["load_balancer", "api_gateway"]
    
    - name: "device_zone_1"
      description: "IoT devices zone 1"
      subnets: ["10.0.10.0/24"]
      device_types: ["sensor", "gateway"]
    
    - name: "device_zone_2"
      description: "IoT devices zone 2"
      subnets: ["10.0.20.0/24"]
      device_types: ["actuator", "controller"]
    
    - name: "management"
      description: "Device management zone"
      subnets: ["10.0.100.0/24"]
      services: ["device_manager", "monitoring"]
    
    - name: "data"
      description: "Data storage zone"
      subnets: ["10.0.200.0/24"]
      services: ["database", "time_series"]
    
    - name: "analytics"
      description: "Analytics zone"
      subnets: ["10.0.210.0/24"]
      services: ["ml_service", "dashboard"]
  
  # Zone-to-zone policies
  policies:
    - name: "dmz_to_management"
      source_zone: "dmz"
      destination_zone: "management"
      allowed_services: ["https:443"]
      authentication: "mtls"
      rate_limit: 1000
    
    - name: "device_to_data"
      source_zone: "device_zone_1"
      destination_zone: "data"
      allowed_services: ["mqtt:1883", "https:443"]
      authentication: "certificate"
      rate_limit: 100
    
    - name: "data_to_analytics"
      source_zone: "data"
      destination_zone: "analytics"
      allowed_services: ["tcp:5432"]
      authentication: "mtls"
      rate_limit: 50
  
  # Service mesh policies
  service_mesh:
    enabled: true
    mesh_type: "istio"
    
    policies:
      - name: "device_to_api"
        source: "device_zone_1/*"
        destination: "dmz/api_gateway"
        methods: ["GET", "POST"]
        authentication: "jwt"
        authorization: "device_policy"
      
      - name: "api_to_data"
        source: "dmz/api_gateway"
        destination: "data/database"
        methods: ["SELECT", "INSERT"]
        authentication: "mtls"
        authorization: "data_policy"
  
  # Enforcement settings
  enforcement:
    mode: "enforce"  # enforce, monitor, audit
    default_action: "deny"
    log_all_traffic: true
    alert_on_violation: true
  
  # Monitoring settings
  monitoring:
    enabled: true
    traffic_analysis: true
    anomaly_detection: true
    alert_thresholds:
      - metric: "policy_violations"
        threshold: 10
        window: "5m"
      - metric: "unusual_traffic"
        threshold: 5
        window: "1h"
```

## Code Examples

### Good vs Bad Examples

```python
# ❌ Bad - Flat network, no segmentation
def configure_network():
    # All devices in same subnet
    return {
        "subnet": "10.0.0.0/16",
        "firewall": "allow all"
    }

# ✅ Good - Segmented network with policies
def configure_segmented_network():
    # Multiple zones with strict policies
    return {
        "zones": {
            "dmz": {"subnet": "10.0.1.0/24"},
            "devices": {"subnet": "10.0.10.0/24"},
            "data": {"subnet": "10.0.100.0/24"}
        },
        "policies": [
            {
                "source": "dmz",
                "destination": "devices",
                "action": "allow",
                "services": ["https:443"]
            },
            {
                "source": "devices",
                "destination": "data",
                "action": "allow",
                "services": ["mqtt:1883"]
            }
        ]
    }
```

```python
# ❌ Bad - No policy validation
def apply_policy(policy):
    # Apply policy without validation
    firewall.add_rule(policy)

# ✅ Good - Policy validation before application
def apply_policy_with_validation(policy):
    # Validate policy
    if not validate_policy(policy):
        raise ValueError("Invalid policy")
    
    # Test in monitor mode first
    firewall.add_rule(policy, mode="monitor")
    
    # Monitor for violations
    violations = monitor_violations(policy, duration="1h")
    
    # If no violations, enforce
    if len(violations) == 0:
        firewall.add_rule(policy, mode="enforce")
    else:
        logger.warning(f"Policy violations detected: {violations}")
```

### Implementation Example

```python
"""
Production-ready Micro Segmentation Policy Manager
"""
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import ipaddress
import json
import logging
from dataclasses import dataclass, field
from enum import Enum
import hashlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PolicyAction(Enum):
    """Policy actions."""
    ALLOW = "allow"
    DENY = "deny"
    LOG = "log"


class PolicyMode(Enum):
    """Policy enforcement modes."""
    ENFORCE = "enforce"
    MONITOR = "monitor"
    AUDIT = "audit"


@dataclass
class SecurityZone:
    """Security zone definition."""
    name: str
    description: str
    subnets: List[str]
    device_types: List[str] = field(default_factory=list)
    services: List[str] = field(default_factory=list)
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class SegmentationPolicy:
    """Segmentation policy rule."""
    name: str
    source_zone: str
    destination_zone: str
    allowed_services: List[str]
    action: PolicyAction
    authentication: Optional[str] = None
    authorization: Optional[str] = None
    rate_limit: Optional[int] = None
    enabled: bool = True


@dataclass
class PolicyViolation:
    """Policy violation record."""
    policy_name: str
    source_ip: str
    destination_ip: str
    service: str
    timestamp: datetime
    violation_type: str


@dataclass
class TrafficRecord:
    """Network traffic record."""
    source_zone: str
    destination_zone: str
    source_ip: str
    destination_ip: str
    service: str
    bytes_transferred: int
    timestamp: datetime


class SegmentationManager:
    """
    Enterprise-grade micro segmentation manager.
    """
    
    def __init__(
        self,
        enforcement_mode: PolicyMode = PolicyMode.ENFORCE,
        default_action: PolicyAction = PolicyAction.DENY,
        log_all_traffic: bool = True
    ):
        """
        Initialize segmentation manager.
        
        Args:
            enforcement_mode: Default enforcement mode
            default_action: Default action for unmatched traffic
            log_all_traffic: Whether to log all traffic
        """
        self.enforcement_mode = enforcement_mode
        self.default_action = default_action
        self.log_all_traffic = log_all_traffic
        
        # Security zones
        self.zones: Dict[str, SecurityZone] = {}
        
        # Segmentation policies
        self.policies: Dict[str, SegmentationPolicy] = {}
        
        # Policy violations
        self.violations: List[PolicyViolation] = []
        
        # Traffic records
        self.traffic_records: List[TrafficRecord] = []
        
        logger.info("Segmentation manager initialized")
    
    def add_zone(self, zone: SecurityZone) -> None:
        """
        Add a security zone.
        
        Args:
            zone: Security zone to add
        """
        # Validate subnets
        for subnet in zone.subnets:
            try:
                ipaddress.ip_network(subnet)
            except ValueError as e:
                raise ValueError(f"Invalid subnet {subnet}: {e}")
        
        self.zones[zone.name] = zone
        logger.info(f"Zone added: {zone.name}")
    
    def add_policy(self, policy: SegmentationPolicy) -> None:
        """
        Add a segmentation policy.
        
        Args:
            policy: Policy to add
        """
        # Validate zones exist
        if policy.source_zone not in self.zones:
            raise ValueError(f"Source zone not found: {policy.source_zone}")
        if policy.destination_zone not in self.zones:
            raise ValueError(f"Destination zone not found: {policy.destination_zone}")
        
        # Validate services format
        for service in policy.allowed_services:
            if ':' not in service:
                raise ValueError(f"Invalid service format: {service}")
        
        self.policies[policy.name] = policy
        logger.info(f"Policy added: {policy.name}")
    
    def get_zone_for_ip(self, ip: str) -> Optional[str]:
        """
        Get zone for an IP address.
        
        Args:
            ip: IP address
            
        Returns:
            Zone name or None
        """
        ip_obj = ipaddress.ip_address(ip)
        
        for zone_name, zone in self.zones.items():
            for subnet in zone.subnets:
                network = ipaddress.ip_network(subnet)
                if ip_obj in network:
                    return zone_name
        
        return None
    
    def evaluate_policy(
        self,
        source_ip: str,
        destination_ip: str,
        service: str,
        timestamp: Optional[datetime] = None
    ) -> Tuple[PolicyAction, Optional[SegmentationPolicy]]:
        """
        Evaluate policy for traffic.
        
        Args:
            source_ip: Source IP address
            destination_ip: Destination IP address
            service: Service (protocol:port)
            timestamp: Timestamp of traffic
            
        Returns:
            Tuple of (action, matching_policy)
        """
        if timestamp is None:
            timestamp = datetime.utcnow()
        
        # Get zones
        source_zone = self.get_zone_for_ip(source_ip)
        destination_zone = self.get_zone_for_ip(destination_ip)
        
        if source_zone is None or destination_zone is None:
            logger.warning(f"IP not in any zone: {source_ip} -> {destination_ip}")
            return self.default_action, None
        
        # Log traffic
        if self.log_all_traffic:
            self.traffic_records.append(TrafficRecord(
                source_zone=source_zone,
                destination_zone=destination_zone,
                source_ip=source_ip,
                destination_ip=destination_ip,
                service=service,
                bytes_transferred=0,
                timestamp=timestamp
            ))
        
        # Find matching policy
        matching_policy = None
        for policy_name, policy in self.policies.items():
            if not policy.enabled:
                continue
            
            if (policy.source_zone == source_zone and
                policy.destination_zone == destination_zone):
                matching_policy = policy
                break
        
        # Evaluate policy
        if matching_policy:
            # Check if service is allowed
            if service in matching_policy.allowed_services:
                action = PolicyAction.ALLOW
            else:
                action = PolicyAction.DENY
                self._log_violation(
                    policy_name=matching_policy.name,
                    source_ip=source_ip,
                    destination_ip=destination_ip,
                    service=service,
                    violation_type="service_not_allowed"
                )
        else:
            # No matching policy, use default
            action = self.default_action
            self._log_violation(
                policy_name="default",
                source_ip=source_ip,
                destination_ip=destination_ip,
                service=service,
                violation_type="no_matching_policy"
            )
        
        return action, matching_policy
    
    def _log_violation(
        self,
        policy_name: str,
        source_ip: str,
        destination_ip: str,
        service: str,
        violation_type: str
    ) -> None:
        """
        Log policy violation.
        
        Args:
            policy_name: Name of policy
            source_ip: Source IP
            destination_ip: Destination IP
            service: Service
            violation_type: Type of violation
        """
        violation = PolicyViolation(
            policy_name=policy_name,
            source_ip=source_ip,
            destination_ip=destination_ip,
            service=service,
            timestamp=datetime.utcnow(),
            violation_type=violation_type
        )
        
        self.violations.append(violation)
        logger.warning(
            f"Policy violation: {policy_name} - {violation_type} "
            f"({source_ip} -> {destination_ip} : {service})"
        )
    
    def get_violations(
        self,
        since: Optional[datetime] = None
    ) -> List[PolicyViolation]:
        """
        Get policy violations.
        
        Args:
            since: Get violations since this time
            
        Returns:
            List of violations
        """
        if since is None:
            return self.violations
        
        return [
            v for v in self.violations
            if v.timestamp >= since
        ]
    
    def get_traffic_summary(
        self,
        zone: Optional[str] = None,
        since: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Get traffic summary.
        
        Args:
            zone: Filter by zone (optional)
            since: Get traffic since this time
            
        Returns:
            Traffic summary
        """
        traffic = self.traffic_records
        
        # Filter by time
        if since is not None:
            traffic = [t for t in traffic if t.timestamp >= since]
        
        # Filter by zone
        if zone is not None:
            traffic = [
                t for t in traffic
                if t.source_zone == zone or t.destination_zone == zone
            ]
        
        # Calculate summary
        summary = {
            "total_records": len(traffic),
            "bytes_transferred": sum(t.bytes_transferred for t in traffic),
            "zone_pairs": {},
            "services": {}
        }
        
        # Zone pairs
        for t in traffic:
            pair = f"{t.source_zone}->{t.destination_zone}"
            summary["zone_pairs"][pair] = summary["zone_pairs"].get(pair, 0) + 1
        
        # Services
        for t in traffic:
            summary["services"][t.service] = summary["services"].get(t.service, 0) + 1
        
        return summary
    
    def validate_policy(self, policy: SegmentationPolicy) -> bool:
        """
        Validate a policy.
        
        Args:
            policy: Policy to validate
            
        Returns:
            True if policy is valid
        """
        # Check zones exist
        if policy.source_zone not in self.zones:
            logger.error(f"Source zone not found: {policy.source_zone}")
            return False
        
        if policy.destination_zone not in self.zones:
            logger.error(f"Destination zone not found: {policy.destination_zone}")
            return False
        
        # Check services format
        for service in policy.allowed_services:
            if ':' not in service:
                logger.error(f"Invalid service format: {service}")
                return False
            
            protocol, port = service.split(':')
            if protocol not in ['tcp', 'udp', 'http', 'https', 'mqtt']:
                logger.error(f"Invalid protocol: {protocol}")
                return False
            
            try:
                int(port)
            except ValueError:
                logger.error(f"Invalid port: {port}")
                return False
        
        # Check rate limit
        if policy.rate_limit is not None and policy.rate_limit <= 0:
            logger.error(f"Invalid rate limit: {policy.rate_limit}")
            return False
        
        return True
    
    def export_config(self) -> Dict[str, Any]:
        """
        Export configuration.
        
        Returns:
            Configuration dictionary
        """
        return {
            "zones": {
                name: {
                    "description": zone.description,
                    "subnets": zone.subnets,
                    "device_types": zone.device_types,
                    "services": zone.services,
                    "tags": zone.tags
                }
                for name, zone in self.zones.items()
            },
            "policies": [
                {
                    "name": policy.name,
                    "source_zone": policy.source_zone,
                    "destination_zone": policy.destination_zone,
                    "allowed_services": policy.allowed_services,
                    "action": policy.action.value,
                    "authentication": policy.authentication,
                    "authorization": policy.authorization,
                    "rate_limit": policy.rate_limit,
                    "enabled": policy.enabled
                }
                for policy in self.policies.values()
            ],
            "enforcement": {
                "mode": self.enforcement_mode.value,
                "default_action": self.default_action.value,
                "log_all_traffic": self.log_all_traffic
            }
        }


# Example usage
if __name__ == "__main__":
    # Initialize segmentation manager
    manager = SegmentationManager(
        enforcement_mode=PolicyMode.ENFORCE,
        default_action=PolicyAction.DENY,
        log_all_traffic=True
    )
    
    # Add security zones
    manager.add_zone(SecurityZone(
        name="dmz",
        description="Demilitarized zone",
        subnets=["10.0.1.0/24"],
        services=["load_balancer", "api_gateway"]
    ))
    
    manager.add_zone(SecurityZone(
        name="devices",
        description="IoT devices zone",
        subnets=["10.0.10.0/24"],
        device_types=["sensor", "gateway"]
    ))
    
    manager.add_zone(SecurityZone(
        name="data",
        description="Data storage zone",
        subnets=["10.0.100.0/24"],
        services=["database", "time_series"]
    ))
    
    # Add segmentation policies
    manager.add_policy(SegmentationPolicy(
        name="dmz_to_devices",
        source_zone="dmz",
        destination_zone="devices",
        allowed_services=["https:443"],
        action=PolicyAction.ALLOW,
        authentication="mtls",
        rate_limit=1000
    ))
    
    manager.add_policy(SegmentationPolicy(
        name="devices_to_data",
        source_zone="devices",
        destination_zone="data",
        allowed_services=["mqtt:1883"],
        action=PolicyAction.ALLOW,
        authentication="certificate",
        rate_limit=100
    ))
    
    # Evaluate traffic
    action, policy = manager.evaluate_policy(
        source_ip="10.0.10.5",
        destination_ip="10.0.100.10",
        service="mqtt:1883"
    )
    
    print(f"\nTraffic Evaluation:")
    print(f"  Source IP: 10.0.10.5")
    print(f"  Destination IP: 10.0.100.10")
    print(f"  Service: mqtt:1883")
    print(f"  Action: {action.value}")
    print(f"  Policy: {policy.name if policy else 'None'}")
    
    # Get traffic summary
    summary = manager.get_traffic_summary()
    print(f"\nTraffic Summary:")
    print(f"  Total Records: {summary['total_records']}")
    print(f"  Zone Pairs: {summary['zone_pairs']}")
    
    # Export configuration
    config = manager.export_config()
    print(f"\nConfiguration exported with {len(config['zones'])} zones and {len(config['policies'])} policies")
```

## Standards, Compliance & Security

### International Standards
- **NIST SP 800-41:** Network segmentation guidelines
- **ISO/IEC 27001:** Information security management
- **PCI DSS:** Network security requirements
- **SOC 2 Type II:** Security and availability controls

### Security Protocol
- **Default Deny:** Deny all traffic by default
- **Least Privilege:** Grant minimum necessary access
- **Defense in Depth:** Multiple layers of security
- **Audit Logging:** Complete audit trail of all traffic
- **Continuous Monitoring:** Real-time threat detection

### Explainability
- **Policy Documentation:** Clear documentation of all policies
- **Traffic Visualization:** Visual representation of traffic flows
- **Violation Reports:** Detailed violation analysis

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install netaddr ipaddress
   ```

2. **Initialize segmentation manager:**
   ```python
   manager = SegmentationManager(
       enforcement_mode=PolicyMode.ENFORCE,
       default_action=PolicyAction.DENY
   )
   ```

3. **Add security zones:**
   ```python
   manager.add_zone(SecurityZone(
       name="devices",
       subnets=["10.0.10.0/24"]
   ))
   ```

4. **Add segmentation policies:**
   ```python
   manager.add_policy(SegmentationPolicy(
       name="devices_to_data",
       source_zone="devices",
       destination_zone="data",
       allowed_services=["mqtt:1883"],
       action=PolicyAction.ALLOW
   ))
   ```

## Production Checklist

- [ ] Security zones defined and documented
- [ ] Segmentation policies implemented
- [ ] Default deny policy configured
- [ ] Traffic logging enabled
- [ ] Violation monitoring configured
- [ ] Policy validation implemented
- [ ] Regular policy reviews scheduled
- [ ] Incident response procedures documented
- [ ] Backup and recovery procedures tested
- [ ] Compliance requirements met

## Anti-patterns

1. **Flat Network:** No segmentation, all devices in same zone
   - **Why it's bad:** Lateral movement unchecked
   - **Solution:** Implement micro segmentation

2. **Overly Permissive Policies:** Allow all traffic between zones
   - **Why it's bad:** Defeats purpose of segmentation
   - **Solution:** Implement least privilege policies

3. **No Monitoring:** Not logging or monitoring traffic
   - **Why it's bad:** Can't detect violations
   - **Solution:** Enable comprehensive logging

4. **Static Policies:** Policies never updated
   - **Why it's bad:** Doesn't adapt to changes
   - **Solution:** Regular policy reviews and updates

## Unit Economics & KPIs

### Cost Calculation
```
Total Cost = Infrastructure + Operations + Compliance

Infrastructure = (Network Equipment + Software Licenses) / 3 years
Operations = (Management Time + Monitoring) × Labor Rate
Compliance = Audit Costs + Compliance Management
```

### Key Performance Indicators
- **Policy Violation Rate:** < 0.1% of total traffic
- **Blast Radius:** < 10 devices per breach
- **Containment Time:** < 5 minutes from detection
- **Policy Compliance:** > 95% of policies enforced
- **False Positive Rate:** < 5% of violations

## Integration Points / Related Skills
- [Hardware Rooted Identity](../74-iot-zero-trust-security/hardware-rooted-identity/SKILL.md) - For device authentication
- [mTLS PKI Management](../74-iot-zero-trust-security/mtls-pki-management/SKILL.md) - For certificate-based auth
- [Secure Device Provisioning](../74-iot-zero-trust-security/secure-device-provisioning/SKILL.md) - For device provisioning
- [Runtime Threat Detection](../74-iot-zero-trust-security/runtime-threat-detection/SKILL.md) - For threat detection

## Further Reading
- [NIST SP 800-41 - Network Segmentation](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-41.pdf)
- [Zero Trust Architecture](https://www.cisa.gov/zero-trust-maturity-model)
- [AWS Network Firewall](https://docs.aws.amazon.com/network-firewall/latest/developerguide/)
- [Istio Service Mesh](https://istio.io/latest/docs/concepts/security/)
- [Calico Network Policy](https://docs.projectcalico.org/security/network-policy/)
