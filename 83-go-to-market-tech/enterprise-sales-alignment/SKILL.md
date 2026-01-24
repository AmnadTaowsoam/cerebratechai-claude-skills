---
name: Enterprise Sales Alignment
description: Aligning product capabilities with enterprise sales requirements and processes
---

# Enterprise Sales Alignment

## Current Level: Expert (Enterprise Scale)

## Domain: Go-to-Market Tech
## Skill ID: 149

---

## Executive Summary

Enterprise Sales Alignment enables aligning product capabilities with enterprise sales requirements and processes. This capability is essential for winning enterprise deals, meeting enterprise requirements, and accelerating sales cycles.

### Strategic Necessity

- **Deal Acceleration**: Accelerate enterprise sales cycles
- **Requirement Alignment**: Align product with enterprise needs
- **Sales Enablement**: Enable sales with product knowledge
- **Competitive Win**: Win against competitors
- **Revenue Growth**: Drive enterprise revenue

---

## Technical Deep Dive

### Alignment Framework

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Enterprise Sales Alignment Framework                │
│                                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│  │   Enterprise │    │   Product    │    │   Sales     │                  │
│  │   Requirements│───▶│   Capability  │───▶│   Process    │                  │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘                  │
│         │                   │                   │                           │
│         ▼                   ▼                   ▼                           │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Gap Analysis                                 │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Feature  │  │  Security  │  │  Integration│  │  Compliance │            │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘            │   │
│  └───────┼────────────┼────────────┼────────────┼────────────────────┘   │
│          │            │            │            │                         │
│          ▼            ▼            ▼            ▼                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Enablement Activities                           │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Training  │  │  Materials │  │  Tools     │  │  Support   │            │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘            │   │
│  └───────┼────────────┼────────────┼────────────┼────────────────────┘   │
│          │            │            │            │                         │
│          ▼            ▼            ▼            ▼                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Sales Support                                │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  RFP      │  │  Demo      │  │  PoC       │  │  Contract   │            │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Enterprise Requirements

```python
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import asyncio
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class RequirementCategory(Enum):
    """Requirement categories"""
    FUNCTIONAL = "functional"
    TECHNICAL = "technical"
    SECURITY = "security"
    INTEGRATION = "integration"
    COMPLIANCE = "compliance"
    PERFORMANCE = "performance"
    SUPPORT = "support"

class RequirementPriority(Enum):
    """Requirement priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class EnterpriseRequirement:
    """Enterprise requirement definition"""
    requirement_id: str
    name: str
    description: str
    category: RequirementCategory
    priority: RequirementPriority
    source: str  # Customer, RFP, Sales
    status: str  # New, In Progress, Completed, Blocked
    owner: str
    created_at: str
    updated_at: str

@dataclass
class ProductCapability:
    """Product capability definition"""
    capability_id: str
    name: str
    description: str
    category: RequirementCategory
    supported: bool
    gap_analysis: Optional[str]
    roadmap_item: Optional[str]
    created_at: str
    updated_at: str

class EnterpriseRequirementAnalyzer:
    """Enterprise requirement analysis specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.requirement_store = RequirementStore(config['requirement_store'])
        self.capability_store = CapabilityStore(config['capability_store'])
        self.gap_analyzer = GapAnalyzer(config['gap_analysis'])
        
    async def analyze_enterprise_requirements(
        self,
        opportunity_id: str,
        requirements: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze enterprise requirements"""
        logger.info(f"Analyzing enterprise requirements for opportunity: {opportunity_id}")
        
        # Step 1: Categorize requirements
        logger.info("Step 1: Categorizing requirements...")
        categorized = await self._categorize_requirements(requirements)
        
        # Step 2: Prioritize requirements
        logger.info("Step 2: Prioritizing requirements...")
        prioritized = await self._prioritize_requirements(categorized)
        
        # Step 3: Analyze product fit
        logger.info("Step 3: Analyzing product fit...")
        product_fit = await self._analyze_product_fit(prioritized)
        
        # Step 4: Identify gaps
        logger.info("Step 4: Identifying gaps...")
        gaps = await self._identify_gaps(product_fit)
        
        # Step 5: Recommend solutions
        logger.info("Step 5: Recommending solutions...")
        solutions = await self._recommend_solutions(gaps)
        
        # Compile analysis
        analysis = {
            'opportunity_id': opportunity_id,
            'requirements': prioritized,
            'product_fit': product_fit,
            'gaps': gaps,
            'solutions': solutions,
            'analyzed_at': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Enterprise requirements analyzed: {len(prioritized)} requirements")
        
        return analysis
    
    async def _categorize_requirements(
        self,
        requirements: List[Dict[str, Any]]
    ) -> List[EnterpriseRequirement]:
        """Categorize requirements"""
        categorized = []
        
        for i, req in enumerate(requirements):
            # Determine category
            category = self._determine_category(req)
            
            # Determine priority
            priority = self._determine_priority(req)
            
            # Create requirement
            requirement = EnterpriseRequirement(
                requirement_id=f"req_{i+1}",
                name=req['name'],
                description=req['description'],
                category=category,
                priority=priority,
                source=req.get('source', 'customer'),
                status='New',
                owner=req.get('owner', 'Product Team'),
                created_at=datetime.utcnow().isoformat(),
                updated_at=datetime.utcnow().isoformat()
            )
            categorized.append(requirement)
        
        return categorized
    
    def _determine_category(self, requirement: Dict[str, Any]) -> RequirementCategory:
        """Determine requirement category"""
        # Implementation would use NLP or keyword matching
        if 'security' in requirement['description'].lower():
            return RequirementCategory.SECURITY
        elif 'integration' in requirement['description'].lower():
            return RequirementCategory.INTEGRATION
        elif 'compliance' in requirement['description'].lower():
            return RequirementCategory.COMPLIANCE
        elif 'performance' in requirement['description'].lower():
            return RequirementCategory.PERFORMANCE
        elif 'support' in requirement['description'].lower():
            return RequirementCategory.SUPPORT
        elif 'technical' in requirement['description'].lower():
            return RequirementCategory.TECHNICAL
        else:
            return RequirementCategory.FUNCTIONAL
    
    def _determine_priority(self, requirement: Dict[str, Any]) -> RequirementPriority:
        """Determine requirement priority"""
        # Implementation would assess priority
        if 'critical' in requirement.get('priority', '').lower():
            return RequirementPriority.CRITICAL
        elif 'high' in requirement.get('priority', '').lower():
            return RequirementPriority.HIGH
        elif 'medium' in requirement.get('priority', '').lower():
            return RequirementPriority.MEDIUM
        else:
            return RequirementPriority.LOW
    
    async def _prioritize_requirements(
        self,
        requirements: List[EnterpriseRequirement]
    ) -> List[EnterpriseRequirement]:
        """Prioritize requirements"""
        # Sort by priority
        priority_order = {
            RequirementPriority.CRITICAL: 0,
            RequirementPriority.HIGH: 1,
            RequirementPriority.MEDIUM: 2,
            RequirementPriority.LOW: 3
        }
        
        prioritized = sorted(
            requirements,
            key=lambda r: priority_order[r.priority]
        )
        
        return prioritized
    
    async def _analyze_product_fit(
        self,
        requirements: List[EnterpriseRequirement]
    ) -> Dict[str, Any]:
        """Analyze product fit for requirements"""
        fit_analysis = {
            'supported': [],
            'partially_supported': [],
            'not_supported': []
        }
        
        for requirement in requirements:
            # Check if product supports requirement
            capability = await self.capability_store.get_capability_by_name(requirement.name)
            
            if capability:
                if capability.supported:
                    fit_analysis['supported'].append(requirement)
                else:
                    fit_analysis['partially_supported'].append(requirement)
            else:
                fit_analysis['not_supported'].append(requirement)
        
        return fit_analysis
    
    async def _identify_gaps(
        self,
        product_fit: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Identify gaps between requirements and capabilities"""
        gaps = []
        
        # Identify not supported requirements
        for requirement in product_fit['not_supported']:
            gap = {
                'requirement': requirement,
                'gap_type': 'missing_capability',
                'severity': requirement.priority.value,
                'impact': 'Cannot meet requirement',
                'estimated_effort': self._estimate_gap_effort(requirement)
            }
            gaps.append(gap)
        
        # Identify partially supported requirements
        for requirement in product_fit['partially_supported']:
            gap = {
                'requirement': requirement,
                'gap_type': 'partial_capability',
                'severity': requirement.priority.value,
                'impact': 'Partially meets requirement',
                'estimated_effort': self._estimate_gap_effort(requirement)
            }
            gaps.append(gap)
        
        return gaps
    
    def _estimate_gap_effort(self, requirement: EnterpriseRequirement) -> str:
        """Estimate effort to close gap"""
        if requirement.priority == RequirementPriority.CRITICAL:
            return "high"
        elif requirement.priority == RequirementPriority.HIGH:
            return "medium"
        elif requirement.priority == RequirementPriority.MEDIUM:
            return "low"
        else:
            return "minimal"
    
    async def _recommend_solutions(
        self,
        gaps: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Recommend solutions for gaps"""
        solutions = []
        
        for gap in gaps:
            # Recommend solution based on gap type
            if gap['gap_type'] == 'missing_capability':
                solution = {
                    'gap': gap,
                    'solution': 'Develop new feature',
                    'approach': self._recommend_development_approach(gap),
                    'timeline': self._estimate_development_timeline(gap),
                    'cost': self._estimate_development_cost(gap)
                }
            elif gap['gap_type'] == 'partial_capability':
                solution = {
                    'gap': gap,
                    'solution': 'Enhance existing feature',
                    'approach': self._recommend_enhancement_approach(gap),
                    'timeline': self._estimate_enhancement_timeline(gap),
                    'cost': self._estimate_enhancement_cost(gap)
                }
            
            solutions.append(solution)
        
        return solutions
    
    def _recommend_development_approach(self, gap: Dict[str, Any]) -> str:
        """Recommend development approach for gap"""
        if gap['severity'] == 'critical':
            return 'dedicated_sprint'
        elif gap['severity'] == 'high':
            return 'feature_team'
        else:
            return 'backlog'
    
    def _recommend_enhancement_approach(self, gap: Dict[str, Any]) -> str:
        """Recommend enhancement approach for gap"""
        if gap['severity'] == 'critical':
            return 'hotfix'
        elif gap['severity'] == 'high':
            return 'next_sprint'
        else:
            return 'backlog'
    
    def _estimate_development_timeline(self, gap: Dict[str, Any]) -> str:
        """Estimate development timeline for gap"""
        if gap['severity'] == 'critical':
            return '4-6 weeks'
        elif gap['severity'] == 'high':
            return '6-8 weeks'
        elif gap['severity'] == 'medium':
            return '8-12 weeks'
        else:
            return '12-16 weeks'
    
    def _estimate_enhancement_timeline(self, gap: Dict[str, Any]) -> str:
        """Estimate enhancement timeline for gap"""
        if gap['severity'] == 'critical':
            return '2-4 weeks'
        elif gap['severity'] == 'high':
            return '4-6 weeks'
        elif gap['severity'] == 'medium':
            return '6-8 weeks'
        else:
            return '8-12 weeks'
    
    def _estimate_development_cost(self, gap: Dict[str, Any]) -> float:
        """Estimate development cost for gap"""
        # Implementation would estimate cost
        return 0.0
    
    def _estimate_enhancement_cost(self, gap: Dict[str, Any]) -> float:
        """Estimate enhancement cost for gap"""
        # Implementation would estimate cost
        return 0.0

class RequirementStore:
    """Requirement storage specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def create_requirement(self, requirement: EnterpriseRequirement):
        """Create requirement"""
        # Implementation would store in database
        pass
    
    async def get_requirement(self, requirement_id: str) -> EnterpriseRequirement:
        """Get requirement"""
        # Implementation would query database
        return None
    
    async def update_requirement(self, requirement: EnterpriseRequirement):
        """Update requirement"""
        # Implementation would update database
        pass

class CapabilityStore:
    """Capability storage specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def get_capability_by_name(self, name: str) -> Optional[ProductCapability]:
        """Get capability by name"""
        # Implementation would query database
        return None
    
    async def list_capabilities(self, category: Optional[RequirementCategory] = None) -> List[ProductCapability]:
        """List capabilities"""
        # Implementation would query database
        return []

class GapAnalyzer:
    """Gap analysis specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
```

### Sales Enablement

```python
class SalesEnabler:
    """Sales enablement specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.training_manager = TrainingManager(config['training'])
        self.materials_manager = MaterialsManager(config['materials'])
        self.tools_manager = ToolsManager(config['tools'])
        self.support_manager = SupportManager(config['support'])
        
    async def enable_sales_team(
        self,
        sales_team_id: str,
        product_updates: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Enable sales team with product updates"""
        logger.info(f"Enabling sales team: {sales_team_id}")
        
        # Step 1: Create training materials
        logger.info("Step 1: Creating training materials...")
        training_materials = await self.training_manager.create_materials(product_updates)
        
        # Step 2: Create sales materials
        logger.info("Step 2: Creating sales materials...")
        sales_materials = await self.materials_manager.create_materials(product_updates)
        
        # Step 3: Configure sales tools
        logger.info("Step 3: Configuring sales tools...")
        tools_configured = await self.tools_manager.configure_tools(product_updates)
        
        # Step 4: Setup support
        logger.info("Step 4: Setting up support...")
        support_setup = await self.support_manager.setup_support(product_updates)
        
        # Compile enablement
        enablement = {
            'sales_team_id': sales_team_id,
            'training_materials': training_materials,
            'sales_materials': sales_materials,
            'tools_configured': tools_configured,
            'support_setup': support_setup,
            'enabled_at': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Sales team enabled: {sales_team_id}")
        
        return enablement

class TrainingManager:
    """Training management specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def create_materials(
        self,
        product_updates: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Create training materials"""
        materials = []
        
        for update in product_updates:
            # Create training module
            material = {
                'title': f"Training: {update['name']}",
                'description': f"Learn about {update['description']}",
                'type': 'training',
                'content': self._generate_training_content(update),
                'duration_minutes': 60,
                'format': 'video'
            }
            materials.append(material)
        
        return materials
    
    def _generate_training_content(self, update: Dict[str, Any]) -> str:
        """Generate training content"""
        return f"""
# {update['name']}

## Overview
{update['description']}

## Key Features
{self._list_features(update)}

## Use Cases
{self._list_use_cases(update)}

## Demo
{self._describe_demo(update)}

## Q&A
{self._generate_qa(update)}
"""
    
    def _list_features(self, update: Dict[str, Any]) -> str:
        """List features"""
        features = update.get('features', [])
        return '\n'.join([f"- {f}" for f in features])
    
    def _list_use_cases(self, update: Dict[str, Any]) -> str:
        """List use cases"""
        use_cases = update.get('use_cases', [])
        return '\n'.join([f"- {uc}" for uc in use_cases])
    
    def _describe_demo(self, update: Dict[str, Any]) -> str:
        """Describe demo"""
        return f"Demo shows {update['description']}"
    
    def _generate_qa(self, update: Dict[str, Any]) -> str:
        """Generate Q&A"""
        return """
## Common Questions

Q: How does this work?
A: [Answer]

Q: What are the benefits?
A: [Answer]

Q: How do I get started?
A: [Answer]
"""

class MaterialsManager:
    """Materials management specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def create_materials(
        self,
        product_updates: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Create sales materials"""
        materials = []
        
        for update in product_updates:
            # Create sales collateral
            material = {
                'title': f"Sales: {update['name']}",
                'description': f"Sales materials for {update['description']}",
                'type': 'sales',
                'content': self._generate_sales_content(update),
                'format': 'pdf'
            }
            materials.append(material)
        
        return materials
    
    def _generate_sales_content(self, update: Dict[str, Any]) -> str:
        """Generate sales content"""
        return f"""
# {update['name']} - Sales Deck

## Executive Summary
{update['description']}

## Problem Statement
[Problem statement]

## Solution
[Solution description]

## Value Proposition
[Value proposition]

## Features
{self._list_features(update)}

## Pricing
[Pricing information]

## Next Steps
[Call to action]
"""

class ToolsManager:
    """Tools management specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def configure_tools(
        self,
        product_updates: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Configure sales tools"""
        configured = []
        
        for update in product_updates:
            # Configure CRM
            crm_config = await self._configure_crm(update)
            configured.append(crm_config)
            
            # Configure demo environment
            demo_config = await self._configure_demo_environment(update)
            configured.append(demo_config)
        
        return configured
    
    async def _configure_crm(self, update: Dict[str, Any]) -> Dict[str, Any]:
        """Configure CRM"""
        return {
            'tool': 'CRM',
            'update': update['name'],
            'configured': True
        }
    
    async def _configure_demo_environment(self, update: Dict[str, Any]) -> Dict[str, Any]:
        """Configure demo environment"""
        return {
            'tool': 'Demo Environment',
            'update': update['name'],
            'configured': True
        }

class SupportManager:
    """Support management specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def setup_support(
        self,
        product_updates: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Setup support for sales team"""
        support = []
        
        for update in product_updates:
            # Setup support resources
            support_config = {
                'tool': 'Support',
                'update': update['name'],
                'configured': True
            }
            support.append(support_config)
        
        return support
```

---

## Tooling & Tech Stack

### Sales Tools
- **Salesforce**: CRM
- **HubSpot**: CRM
- **Pipedrive**: CRM
- **Zoho CRM**: CRM
- **Monday.com**: Sales pipeline

### Demo Tools
- **Zoom**: Video conferencing
- **Google Meet**: Video conferencing
- **Loom**: Video recording
- **OBS Studio**: Screen recording
- **Figma**: Design

### Training Tools
- **Lessonly**: Training platform
- **Skilljar**: Training platform
- **Trainual**: Training platform
- **Thinkific**: Course platform
- **Teachable**: Course platform

### Documentation Tools
- **Notion**: Documentation
- **Confluence**: Documentation
- **GitBook**: Documentation
- **Read the Docs**: Documentation
- **Docusaurus**: Documentation

---

## Configuration Essentials

### Enterprise Sales Configuration

```yaml
# config/enterprise_sales_config.yaml
enterprise_sales:
  requirements:
    categories:
      - functional
      - technical
      - security
      - integration
      - compliance
      - performance
      - support
    
    priority_levels:
      - critical
      - high
      - medium
      - low
  
  product_fit:
    analysis:
      enabled: true
      frequency: "on_demand"
    
    gap_analysis:
      enabled: true
      auto_recommendations: true
  
  enablement:
    training:
      enabled: true
      format: "video"
      duration_minutes: 60
      frequency: "weekly"
    
    materials:
      enabled: true
      types:
        - sales_deck
        - one_pager
        - case_study
        - whitepaper
    
    tools:
      crm:
        enabled: true
        platform: "salesforce"
      
      demo:
        enabled: true
        platform: "zoom"
      
      analytics:
        enabled: true
        platform: "google_analytics"
    
    support:
      enabled: true
      channels:
        - email
        - slack
        - phone
      
      response_time:
        email: "4 hours"
        slack: "1 hour"
        phone: "immediate"
  
  rfp:
    enabled: true
    template: "enterprise_rfp"
    response_time: "5 business_days"
  
  poc:
    enabled: true
    duration_weeks: 4
    success_criteria:
      - functional_requirements_met
      - performance_benchmarks_met
      - security_requirements_met
      - user_acceptance
  
  contract:
    templates:
      - standard_sla
      - enterprise_sla
      - custom_sla
    
    terms:
      payment_terms:
        - net_30
        - net_60
        - annual_upfront
      
      support_levels:
        - standard
        - premium
        - enterprise
      
      sla_levels:
        - "99.5%"
        - "99.9%"
        - "99.99%"
```

---

## Code Examples

### Good: Complete Enterprise Sales Alignment Workflow

```python
# enterprise_sales/workflow.py
import asyncio
import logging
from typing import Dict, Any

from enterprise_sales.analyzer import EnterpriseRequirementAnalyzer
from enterprise_sales.enabler import SalesEnabler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_enterprise_sales_alignment():
    """Run enterprise sales alignment workflow"""
    logger.info("=" * 60)
    logger.info("Enterprise Sales Alignment Workflow")
    logger.info("=" * 60)
    
    # Load configuration
    config = load_config('config/enterprise_sales_config.yaml')
    
    # Create sample opportunity
    opportunity = create_sample_opportunity()
    
    # Step 1: Analyze enterprise requirements
    logger.info("\n" + "=" * 60)
    logger.info("Step 1: Analyzing Enterprise Requirements")
    logger.info("=" * 60)
    
    analyzer = EnterpriseRequirementAnalyzer(config)
    requirements = create_sample_requirements()
    
    analysis = await analyzer.analyze_enterprise_requirements(
        opportunity['opportunity_id'],
        requirements
    )
    
    logger.info("Enterprise requirements analyzed")
    print_analysis_summary(analysis)
    
    # Step 2: Enable sales team
    logger.info("\n" + "=" * 60)
    logger.info("Step 2: Enabling Sales Team")
    logger.info("=" * 60)
    
    enabler = SalesEnabler(config)
    product_updates = create_sample_product_updates()
    
    enablement = await enabler.enable_sales_team(
        sales_team_id="sales_team_1",
        product_updates=product_updates
    )
    
    logger.info("Sales team enabled")
    print_enablement_summary(enablement)
    
    # Print summary
    print_summary(opportunity, analysis, enablement)

def create_sample_opportunity() -> Dict[str, Any]:
    """Create sample opportunity"""
    return {
        'opportunity_id': "opp_enterprise_001",
        'account_name': "Fortune 500 Company",
        'contact_name': "CTO",
        'stage': "discovery",
        'value': 500000.0,
        'probability': 0.3
    }

def create_sample_requirements() -> List[Dict[str, Any]]:
    """Create sample requirements"""
    return [
        {
            'name': 'SSO Integration',
            'description': 'Support for SAML/OAuth SSO',
            'priority': 'critical',
            'source': 'customer'
        },
        {
            'name': 'Enterprise SLA',
            'description': '99.99% uptime SLA',
            'priority': 'high',
            'source': 'customer'
        },
        {
            'name': 'Data Residency',
            'description': 'Data must reside in EU',
            'priority': 'critical',
            'source': 'customer'
        },
        {
            'name': 'API Rate Limiting',
            'description': 'Custom rate limits per customer',
            'priority': 'medium',
            'source': 'customer'
        }
    ]

def create_sample_product_updates() -> List[Dict[str, Any]]:
    """Create sample product updates"""
    return [
        {
            'name': 'New Feature X',
            'description': 'Feature X enables enterprise use cases',
            'features': ['Feature A', 'Feature B', 'Feature C'],
            'use_cases': ['Use case 1', 'Use case 2']
        },
        {
            'name': 'Security Enhancement',
            'description': 'Enhanced security for enterprise',
            'features': ['Encryption', 'Audit logging', 'Compliance'],
            'use_cases': ['Enterprise security', 'Regulatory compliance']
        }
    ]

def print_analysis_summary(analysis: Dict[str, Any]):
    """Print analysis summary"""
    print(f"\nAnalysis Summary:")
    print(f"  Requirements: {len(analysis['requirements'])}")
    print(f"  Supported: {len(analysis['product_fit']['supported'])}")
    print(f"  Partially Supported: {len(analysis['product_fit']['partially_supported'])}")
    print(f"  Not Supported: {len(analysis['product_fit']['not_supported'])}")
    print(f"  Gaps: {len(analysis['gaps'])}")
    print(f"  Solutions: {len(analysis['solutions'])}")

def print_enablement_summary(enablement: Dict[str, Any]):
    """Print enablement summary"""
    print(f"\nEnablement Summary:")
    print(f"  Training Materials: {len(enablement['training_materials'])}")
    print(f"  Sales Materials: {len(enablement['sales_materials'])}")
    print(f"  Tools Configured: {len(enablement['tools_configured'])}")
    print(f"  Support Setup: {len(enablement['support_setup'])}")

def print_summary(
    opportunity: Dict[str, Any],
    analysis: Dict[str, Any],
    enablement: Dict[str, Any]
):
    """Print summary"""
    print("\n" + "=" * 60)
    print("Enterprise Sales Alignment Summary")
    print("=" * 60)
    print(f"Opportunity: {opportunity['account_name']}")
    print(f"Value: ${opportunity['value']:,.0f}")
    print(f"\nRequirements Analysis:")
    print(f"  Total: {len(analysis['requirements'])}")
    print(f"  Supported: {len(analysis['product_fit']['supported'])}")
    print(f"  Gaps: {len(analysis['gaps'])}")
    print(f"\nSales Enablement:")
    print(f"  Training: {len(enablement['training_materials'])} materials")
    print(f"  Sales Materials: {len(enablement['sales_materials'])} materials")
    print(f"  Tools: {len(enablement['tools_configured'])} configured")

def load_config(filename: str) -> Dict[str, Any]:
    """Load configuration from file"""
    import yaml
    with open(filename, 'r') as f:
        return yaml.safe_load(f)

async def main():
    """Main entry point"""
    await run_enterprise_sales_alignment()

if __name__ == "__main__":
    asyncio.run(main())
```

### Bad: Anti-pattern Example

```python
# BAD: No requirements analysis
def bad_enterprise_sales():
    # No requirements analysis
    pass

# BAD: No enablement
def bad_enterprise_sales():
    # No enablement
    analyze_requirements()

# BAD: No sales support
def bad_enterprise_sales():
    # No sales support
    analyze_requirements()
    enable_sales()

# BAD: No gap analysis
def bad_enterprise_sales():
    # No gap analysis
    analyze_requirements()
    enable_sales()
    support_sales()
```

---

## Standards, Compliance & Security

### Industry Standards
- **Enterprise Sales**: Enterprise sales best practices
- **Sales Enablement**: Sales enablement best practices
- **RFP Management**: RFP management best practices
- **Contract Management**: Contract management best practices

### Security Best Practices
- **Data Protection**: Protect customer data
- **Access Control**: RBAC for sales tools
- **Audit Logging**: Log all sales activities
- **Confidentiality**: Maintain confidentiality

### Compliance Requirements
- **GDPR**: Data protection compliance
- **SOC 2**: Security and availability
- **ISO 27001**: Information security
- **Industry Regulations**: Follow industry regulations

---

## Quick Start

### 1. Install Dependencies

```bash
pip install pyyaml
```

### 2. Configure Enterprise Sales

```bash
# Copy example config
cp config/enterprise_sales_config.yaml.example config/enterprise_sales_config.yaml

# Edit configuration
vim config/enterprise_sales_config.yaml
```

### 3. Run Enterprise Sales Alignment

```bash
python enterprise_sales/workflow.py
```

### 4. View Results

```bash
# View analysis
cat enterprise_sales/results/analysis.json

# View enablement
cat enterprise_sales/results/enablement.json
```

---

## Production Checklist

### Requirements Analysis
- [ ] Requirements collected
- [ ] Requirements categorized
- [ ] Requirements prioritized
- [ ] Product fit analyzed
- [ ] Gaps identified

### Enablement
- [ ] Training materials created
- [ ] Sales materials created
- [ ] Sales tools configured
- [ ] Support setup
- [ ] Training delivered

### RFP Management
- [ ] RFP template created
- [ ] Response process defined
- [ ] Approval workflow defined
- [ ] Timeline established
- [ ] Team trained

### PoC Management
- [ ] PoC process defined
- [ ] Success criteria defined
- [ ] Environment setup
- [ ] Monitoring configured
- [ ] Results documented

### Contract Management
- [ ] Contract templates created
- [ ] Terms defined
- [ ] SLA levels defined
- [ ] Legal review process
- [ ] Approval workflow defined

---

## Anti-patterns

### ❌ Avoid These Practices

1. **No Requirements Analysis**
   ```python
   # BAD: No requirements analysis
   pass
   ```

2. **No Enablement**
   ```python
   # BAD: No enablement
   analyze_requirements()
   ```

3. **No Sales Support**
   ```python
   # BAD: No sales support
   analyze_requirements()
   enable_sales()
   ```

4. **No Gap Analysis**
   ```python
   # BAD: No gap analysis
   analyze_requirements()
   enable_sales()
   support_sales()
   ```

### ✅ Follow These Practices

1. **Analyze Requirements**
   ```python
   # GOOD: Analyze requirements
   analyzer = EnterpriseRequirementAnalyzer(config)
   analysis = await analyzer.analyze_enterprise_requirements(opportunity_id, requirements)
   ```

2. **Enable Sales**
   ```python
   # GOOD: Enable sales
   enabler = SalesEnabler(config)
   enablement = await enabler.enable_sales_team(sales_team_id, product_updates)
   ```

3. **Support Sales**
   ```python
   # GOOD: Support sales
   support = SalesSupport(config)
   results = await support.handle_objections(opportunity, objections)
   ```

4. **Analyze Gaps**
   ```python
   # GOOD: Analyze gaps
   gap_analyzer = GapAnalyzer(config)
   gaps = await gap_analyzer.analyze_gaps(requirements, capabilities)
   ```

---

## Unit Economics & KPIs

### Development Costs
- **Initial Setup**: 20-40 hours
- **Requirements Analysis**: 20-40 hours
- **Enablement**: 40-80 hours
- **Sales Support**: 40-80 hours
- **Total**: 120-240 hours

### Operational Costs
- **Sales Tools**: $200-1000/month
- **Training Platform**: $100-500/month
- **Demo Environment**: $100-500/month
- **Support Tools**: $50-200/month

### ROI Metrics
- **Win Rate**: 20-40% improvement
- **Deal Size**: 30-50% improvement
- **Sales Cycle**: 30-50% reduction
- **Customer Satisfaction**: 40-60% improvement

### KPI Targets
- **Requirements Coverage**: > 90%
- **Product Fit Score**: > 80%
- **Gap Resolution Rate**: > 70%
- **Enablement Completion**: > 90%
- **Win Rate**: > 30%

---

## Integration Points / Related Skills

### Upstream Skills
- **136. Business to Technical Spec**: Requirements
- **137. API-First Product Strategy**: API design
- **138. Platform Product Design**: Platform design
- **146. Developer Relations & Community**: Community building
- **147. Technical Content Marketing**: Content marketing

### Parallel Skills
- **148. Sales Engineering**: Sales engineering

### Downstream Skills
- **150. Partner Program Design**: Partner programs
- **151. Analyst Relations**: Analyst relations
- **152. Launch Strategy Execution**: Launch strategy

### Cross-Domain Skills
- **18. Project Management**: Project planning
- **81. SaaS FinOps Pricing**: Pricing strategy
- **82. Technical Product Management**: Product management
- **84. Compliance AI Governance**: Compliance

---

## References & Resources

### Documentation
- [Enterprise Sales Guide](https://www.gartner.com/)
- [Sales Enablement Best Practices](https://www.forrester.com/)
- [RFP Management Guide](https://www.rfp-database.com/)
- [Contract Management Guide](https://www.legalzoom.com/)

### Best Practices
- [Enterprise Sales Best Practices](https://www.salesforce.com/)
- [Sales Enablement](https://www.hubspot.com/)
- [Enterprise Negotiation](https://www.hbr.org/topic/sales)

### Tools & Libraries
- [Salesforce](https://www.salesforce.com/)
- [HubSpot](https://www.hubspot.com/)
- [Zoom](https://zoom.us/)
- [Lessonly](https://www.lessonly.com/)
- [Notion](https://www.notion.so/)
