---
name: Multi-Cloud Patterns
description: Architecture patterns and strategies for multi-cloud deployments to avoid vendor lock-in.
---

# Multi-Cloud Patterns

## Overview

Multi-cloud strategies use more than one cloud provider to reduce risk,
avoid lock-in, and meet regulatory or availability requirements. This
guide covers patterns, tooling, and trade-offs.

## Table of Contents

1. [Why Multi-Cloud](#why-multi-cloud)
2. [Architecture Patterns](#architecture-patterns)
3. [Cloud-Agnostic Technologies](#cloud-agnostic-technologies)
4. [Abstraction Strategies](#abstraction-strategies)
5. [Data Considerations](#data-considerations)
6. [Networking](#networking)
7. [Identity and Access Management](#identity-and-access-management)
8. [Monitoring and Observability](#monitoring-and-observability)
9. [Cost Management](#cost-management)
10. [Challenges and Trade-Offs](#challenges-and-trade-offs)
11. [When Not to Use Multi-Cloud](#when-not-to-use-multi-cloud)
12. [Case Studies](#case-studies)

---

## Why Multi-Cloud

Common drivers:
- Vendor lock-in avoidance
- Best-of-breed services
- Compliance or data residency
- Disaster recovery
- Cost optimization and pricing leverage

## Architecture Patterns

- **Arbitrage**: Route traffic to the lowest-cost provider.
- **Segmented**: Different workloads per cloud (e.g., analytics vs web).
- **Portable**: Use abstraction to move workloads easily.
- **Redundant**: Active-active or active-passive across clouds.

## Cloud-Agnostic Technologies

- **Kubernetes**: Common deployment target.
- **Terraform/Pulumi**: IaC across providers.
- **Crossplane**: Kubernetes-native infrastructure orchestration.

## Abstraction Strategies

- **Infrastructure abstraction**: Standardize resource modules.
- **Service abstraction**: Wrap databases/queues behind internal APIs.
- **API abstraction**: Avoid provider-specific SDK lock-in.

## Data Considerations

- **Data gravity**: Keep compute close to data.
- **Cross-cloud sync**: Use CDC or replication tools.
- **Egress costs**: Evaluate traffic costs between clouds.

## Networking

- Multi-cloud connectivity via VPN or dedicated links.
- Global DNS routing and traffic management.
- Service mesh federation for service-to-service control.

## Identity and Access Management

Unify identity with SSO and map roles per provider. Prefer short-lived
credentials and central audit logging.

## Monitoring and Observability

Standardize telemetry:
- Centralized logs/metrics/traces
- Normalized labels and service naming
- Unified alerting rules

## Cost Management

- Normalize cost tags
- Compare services with equivalent pricing models
- Monitor egress and inter-cloud traffic

## Challenges and Trade-Offs

- Operational complexity
- Divergent cloud service features
- Increased testing and validation burden
- Potentially higher cost

## When Not to Use Multi-Cloud

Avoid if:
- Team is small or lacks ops maturity.
- Workloads depend on deep cloud-native features.
- Latency-sensitive systems cannot tolerate cross-cloud calls.

## Case Studies

Examples:
- Active-passive DR across AWS and GCP
- Segmented workloads: AI training on GCP, web apps on AWS

## Related Skills
- `15-devops-infrastructure/terraform-iac`
- `15-devops-infrastructure/kubernetes-helm`
- `42-cost-engineering/cloud-cost-models`
