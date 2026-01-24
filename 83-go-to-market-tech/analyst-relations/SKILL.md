---
name: Analyst Relations
description: Managing relationships with industry analysts, briefings, and research reports
---

# Analyst Relations

## Current Level: Expert (Enterprise Scale)

## Domain: Go-to-Market Tech
## Skill ID: 151

---

## Executive Summary

Analyst Relations enables managing relationships with industry analysts, briefings, and research reports. This capability is essential for building market credibility, influencing analyst reports, supporting sales cycles, and driving market awareness.

### Strategic Necessity

- **Market Credibility**: Build credibility with analysts
- **Influence**: Influence analyst reports and coverage
- **Sales Support**: Support sales with analyst interactions
- **Market Awareness**: Increase market visibility
- **Competitive Intelligence**: Gather competitive insights

---

## Technical Deep Dive

### Analyst Relations Framework

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Analyst Relations Framework                           │
│                                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│  │   Analyst    │    │   Briefing   │    │   Research   │                  │
│  │   Research   │───▶│   Management  │───▶│   Support    │                  │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘                  │
│         │                   │                   │                           │
│         ▼                   ▼                   ▼                           │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Analyst Identification                           │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Gartner    │  │  Forrester  │  │  Boutique   │  │  Industry   │            │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘            │   │
│  └───────┼────────────┼────────────┼────────────┼────────────────────┘   │
│          │            │            │            │                         │
│          ▼            ▼            ▼            ▼                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Briefing Management                             │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Inquiry    │  │  Briefing   │  │  Update    │  │  Review    │            │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘            │   │
│  └───────┼────────────┼────────────┼────────────┼────────────────────┘   │
│          │            │            │            │                         │
│          ▼            ▼            ▼            ▼                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Research Support                                 │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Data       │  │  Access     │  │  Insights  │  │  Feedback   │            │   │
│  │  └────┬─────┘  └────┬─────�  └────┬─────┘  └────┬─────┘            │   │
│  └───────┼────────────┼────────────┼────────────┼────────────────────┘   │
│          │            │            │            │                         │
│          ▼            ▼            ▼            ▼                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Relationship Management                         │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Tracking   │  │  Scoring    │  │  Engagement │  │  Reviews    │            │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘            │   │
│  └───────┼────────────┼────────────┼────────────┼────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Analyst Identification

```python
from typing import Dict, Any, List, Optional
from dataclass import dataclass
from enum import Enum
import asyncio
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class AnalystType(Enum):
    """Analyst types"""
    GARTNER = "gartner"
    FORRESTER = "forrester"
    BOUTIQUE = "boutique"
    INDUSTRY = "industry"
    INDEPENDENT = "independent"

class AnalystTier(Enum):
    """Analyst tiers"""
    TIER_1 = "tier_1"  # Top analysts
    TIER_2 = "tier_2"  # Major analysts
    TIER_3 = "tier_3"  # Mid-market analysts
    TIER_4 = "tier_4"  # Niche analysts

class CoverageArea(Enum):
    """Coverage areas"""
    TECHNOLOGY = "technology"
    INDUSTRY = "industry"
    REGION = "region"
    FUNCTION = "function"

@dataclass
class Analyst:
    """Analyst definition"""
    analyst_id: str
    name: str
    firm: str
    analyst_type: AnalystType
    tier: AnalystTier
    coverage_areas: List[CoverageArea]
    contact_name: str
    contact_email: str
    linkedin: str
    twitter: str
    website: str
    score: float
    engagement_level: str
    last_contact: str
    created_at: str
    updated_at: str

class AnalystIdentifier:
    """Analyst identification specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.analyst_store = AnalystStore(config['analyst_store'])
        self.researcher = AnalystResearcher(config['research'])
        
    async def identify_analysts(
        self,
        criteria: Dict[str, Any]
    ) -> List[Analyst]:
        """Identify relevant analysts"""
        logger.info("Identifying analysts...")
        
        # Identify Gartner analysts
        gartner_analysts = await self._identify_gartner_analysts(criteria)
        
        # Identify Forrester analysts
        forrester_analysts = await self._identify_forrester_analysts(criteria)
        
        # Identify Boutique analysts
        boutique_analysts = await self._identify_boutique_analysts(criteria)
        
        # Identify Industry analysts
        industry_analysts = await self._identify_industry_analysts(criteria)
        
        # Combine all analysts
        all_analysts = (
            gartner_analysts +
            forrester_analysts +
            boutique_analysts +
            industry_analysts
        )
        
        # Score and rank analysts
        scored_analysts = await self._score_analysts(all_analysts, criteria)
        
        # Store analysts
        for analyst in scored_analysts:
            await self.analyst_store.create_analyst(analyst)
        
        logger.info(f"Identified {len(scored_analysts)} analysts")
        
        return scored_analysts
    
    async def _identify_gartner_analysts(
        self,
        criteria: Dict[str, Any]
    ) -> List[Analyst]:
        """Identify Gartner analysts"""
        logger.info("Identifying Gartner analysts...")
        
        # Research Gartner analysts
        analysts = await self.researcher.search_gartner_analysts(
            criteria.get('industry', 'technology'),
            criteria.get('region', 'global'),
            criteria.get('coverage', 'enterprise')
        )
        
        return analysts
    
    async def _identify_forrester_analysts(
        self,
        criteria: Dict[str, Any]
    ) -> List[Analyst]:
        """Identify Forrester analysts"""
        logger.info("Identifying Forrester analysts...")
        
        # Research Forrester analysts
        analysts = await self.researcher.search_forrester_analysts(
            criteria.get('industry', 'technology'),
            criteria.get('region', 'global'),
            criteria.get('coverage', 'enterprise')
        )
        
        return analysts
    
    async def _identify_boutique_analysts(
        self,
        criteria: Dict[str, Any]
    ) -> List[Analyst]:
        """Identify Boutique analysts"""
        logger.info("Identifying Boutique analysts...")
        
        # Research Boutique analysts
        analysts = await self.researcher.search_boutique_analysts(
            criteria.get('industry', 'technology'),
            criteria.get('region', 'global'),
            criteria.get('coverage', 'enterprise')
        )
        
        return analysts
    
    async def _identify_industry_analysts(
        self,
        criteria: Dict[str, Any]
    ) -> List[Analyst]:
        """Identify Industry analysts"""
        logger.info("Identifying Industry analysts...")
        
        # Research Industry analysts
        analysts = await self.researcher.search_industry_analysts(
            criteria.get('industry', 'technology'),
            criteria.get('region', 'global'),
            criteria.get('coverage', 'enterprise')
        )
        
        return analysts
    
    async def _score_analysts(
        self,
        analysts: List[Analyst],
        criteria: Dict[str, Any]
    ) -> List[Analyst]:
        """Score and rank analysts"""
        logger.info("Scoring analysts...")
        
        for analyst in analysts:
            # Calculate relevance score
            relevance_score = self._calculate_relevance_score(analyst, criteria)
            
            # Calculate influence score
            influence_score = self._calculate_influence_score(analyst)
            
            # Calculate engagement score
            engagement_score = self._calculate_engagement_score(analyst)
            
            # Calculate overall score
            analyst.score = (
                relevance_score * 0.4 +
                influence_score * 0.3 +
                engagement_score * 0.3
            )
        
        # Sort by score
        analysts.sort(key=lambda a: a.score, reverse=True)
        
        # Assign tiers
        for i, analyst in enumerate(analysts):
            if i < 5:
                analyst.tier = AnalystTier.TIER_1
            elif i < 15:
                analyst.tier = AnalystTier.TIER_2
            elif i < 30:
                analyst.tier = AnalystTier.TIER_3
            else:
                analyst.tier = AnalystTier.TIER_4
        
        return analysts
    
    def _calculate_relevance_score(
        self,
        analyst: Analyst,
        criteria: Dict[str, Any]
    ) -> float:
        """Calculate relevance score"""
        score = 0.0
        
        # Check coverage areas
        target_coverage = criteria.get('coverage_areas', [])
        for area in target_coverage:
            if area in analyst.coverage_areas:
                score += 0.25
        
        return score
    
    def _calculate_influence_score(self, analyst: Analyst) -> float:
        """Calculate influence score"""
        score = 0.0
        
        # Check analyst tier
        if analyst.tier == AnalystTier.TIER_1:
            score += 1.0
        elif analyst.tier == AnalystTier.TIER_2:
            score += 0.75
        elif analyst.tier == AnalystTier.TIER_3:
            score += 0.5
        else:
            score += 0.25
        
        return score
    
    def _calculate_engagement_score(self, analyst: Analyst) -> float:
        """Calculate engagement score"""
        score = 0.0
        
        # Check engagement level
        if analyst.engagement_level == "high":
            score += 1.0
        elif analyst.engagement_level == "medium":
            score += 0.5
        elif analyst.engagement_level == "low":
            score += 0.25
        else:
            score += 0.0
        
        return score

class AnalystResearcher:
    """Analyst research specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def search_gartner_analysts(
        self,
        industry: str,
        region: str,
        coverage: str
    ) -> List[Analyst]:
        """Search Gartner analysts"""
        # Implementation would search Gartner website
        return []
    
    async def search_forrester_analysts(
        self,
        industry: str,
        region: str,
        coverage: str
    ) -> List[Analyst]:
        """Search Forrester analysts"""
        # Implementation would search Forrester website
        return []
    
    async def search_boutique_analysts(
        self,
        industry: str,
        region: str,
        coverage: str
    ) -> List[Analyst]:
        """Search Boutique analysts"""
        # Implementation would search for boutique firms
        return []
    
    async def search_industry_analysts(
        self,
        industry: str,
        region: str,
        coverage: str
    ) -> List[Analyst]:
        """Search Industry analysts"""
        # Implementation would search for industry analysts
        return []

class AnalystStore:
    """Analyst storage specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def create_analyst(self, analyst: Analyst):
        """Create analyst"""
        # Implementation would store in database
        pass
    
    async def get_analyst(self, analyst_id: str) -> Analyst:
        """Get analyst"""
        # Implementation would query database
        return None
    
    async def update_analyst(self, analyst: Analyst):
        """Update analyst"""
        # Implementation would update database
        pass
    
    async def list_analysts(
        self,
        analyst_type: Optional[AnalystType] = None
    ) -> List[Analyst]:
        """List analysts"""
        # Implementation would query database
        return []
```

### Briefing Management

```python
class BriefingManager:
    """Briefing management specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.briefing_store = BriefingStore(config['briefing_store'])
        self.content_creator = ContentCreator(config['content'])
        
    async def schedule_briefing(
        self,
        analyst_id: str,
        briefing_type: str,
        date: str,
        participants: List[str]
    ) -> Dict[str, Any]:
        """Schedule analyst briefing"""
        logger.info(f"Scheduling briefing with analyst: {analyst_id}")
        
        # Get analyst
        analyst = await self.analyst_store.get_analyst(analyst_id)
        
        # Create briefing
        briefing_id = self._generate_briefing_id()
        
        briefing = {
            'briefing_id': briefing_id,
            'analyst_id': analyst_id,
            'analyst_name': analyst.name,
            'briefing_type': briefing_type,
            'date': date,
            'participants': participants,
            'status': 'scheduled',
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        # Store briefing
        await self.briefing_store.create_briefing(briefing)
        
        # Send calendar invitation
        await self._send_calendar_invitation(briefing, analyst)
        
        logger.info(f"Briefing scheduled: {briefing_id}")
        
        return briefing
    
    async def prepare_briefing_materials(
        self,
        briefing_id: str
    ) -> Dict[str, Any]:
        """Prepare briefing materials"""
        logger.info(f"Preparing briefing materials: {briefing_id}")
        
        # Get briefing
        briefing = await self.briefing_store.get_briefing(briefing_id)
        
        # Get analyst
        analyst = await self.analyst_store.get_analyst(briefing['analyst_id'])
        
        # Prepare materials based on analyst type
        materials = await self._prepare_analyst_specific_materials(briefing, analyst)
        
        # Update briefing with materials
        briefing['materials'] = materials
        briefing['updated_at'] = datetime.utcnow().isoformat()
        await self.briefing_store.update_briefing(briefing)
        
        logger.info(f"Briefing materials prepared: {briefing_id}")
        
        return materials
    
    async def _prepare_analyst_specific_materials(
        self,
        briefing: Dict[str, Any],
        analyst: Analyst
    ) -> Dict[str, Any]:
        """Prepare analyst-specific materials"""
        materials = {
            'deck': await self._create_deck(briefing, analyst),
            'one_pager': await self._create_one_pager(briefing, analyst),
            'demo': await self._create_demo(briefing, analyst)
        }
        
        return materials
    
    async def _create_deck(
        self,
        briefing: Dict[str, Any],
        analyst: Analyst
    ) -> str:
        """Create briefing deck"""
        # Implementation would create deck
        return "deck_content"
    
    async def _create_one_pager(
        self,
        briefing: Dict[str, Any],
        analyst: Analyst
    ) -> str:
        """Create one-pager"""
        # Implementation would create one-pager
        return "one_pager_content"
    
    async def _create_demo(
        self,
        briefing: Dict[str, Any],
        analyst: Analyst
    ) -> str:
        """Create demo"""
        # Implementation would create demo
        return "demo_content"
    
    def _generate_briefing_id(self) -> str:
        """Generate unique briefing ID"""
        import uuid
        return f"briefing_{uuid.uuid4().hex}"
    
    async def _send_calendar_invitation(
        self,
        briefing: Dict[str, Any],
        analyst: Analyst
    ):
        """Send calendar invitation"""
        # Implementation would send calendar invitation
        pass

class BriefingStore:
    """Briefing storage specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def create_briefing(self, briefing: Dict[str, Any]):
        """Create briefing"""
        # Implementation would store in database
        pass
    
    async def get_briefing(self, briefing_id: str) -> Dict[str, Any]:
        """Get briefing"""
        # Implementation would query database
        return {}
    
    async def update_briefing(self, briefing: Dict[str, Any]):
        """Update briefing"""
        # Implementation would update database
        pass
    
    async def list_briefings(
        self,
        analyst_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List briefings"""
        # Implementation would query database
        return []

class ContentCreator:
    """Content creation specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
```

### Research Support

```python
class ResearchSupport:
    """Research support specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.data_provider = DataProvider(config['data'])
        self.insight_generator = InsightGenerator(config['insights'])
        
    async def provide_research_data(
        self,
        analyst_id: str,
        research_request: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Provide research data to analyst"""
        logger.info(f"Providing research data to analyst: {analyst_id}")
        
        # Gather required data
        data = await self._gather_research_data(research_request)
        
        # Generate insights
        insights = await self.insight_generator.generate_insights(data)
        
        # Compile response
        response = {
            'analyst_id': analyst_id,
            'request_id': research_request['request_id'],
            'data': data,
            'insights': insights,
            'provided_at': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Research data provided: {len(data)} data points")
        
        return response
    
    async def _gather_research_data(
        self,
        research_request: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Gather research data"""
        # Implementation would gather data from various sources
        return []
    
    async def collect_feedback(
        self,
        analyst_id: str
    ) -> Dict[str, Any]:
        """Collect feedback from analyst"""
        logger.info(f"Collecting feedback from analyst: {analyst_id}")
        
        # Get analyst
        analyst = await self.analyst_store.get_analyst(analyst_id)
        
        # Collect feedback from various sources
        feedback = {
            'briefing_feedback': await self._collect_briefing_feedback(analyst_id),
            'report_feedback': await self._collect_report_feedback(analyst_id),
            'relationship_feedback': await self._collect_relationship_feedback(analyst_id)
        }
        
        # Update analyst with feedback
        await self._update_analyst_feedback(analyst_id, feedback)
        
        logger.info(f"Feedback collected from {analyst_id}")
        
        return feedback
    
    async def _collect_briefing_feedback(self, analyst_id: str) -> List[str]:
        """Collect briefing feedback"""
        # Implementation would collect briefing feedback
        return []
    
    async def _collect_report_feedback(self, analyst_id: str) -> List[str]:
        """Collect report feedback"""
        # Implementation would collect report feedback
        return []
    
    async def _collect_relationship_feedback(self, analyst_id: str) -> List[str]:
        """Collect relationship feedback"""
        # Implementation would collect relationship feedback
        return []
    
    async def _update_analyst_feedback(
        self,
        analyst_id: str,
        feedback: Dict[str, Any]
    ):
        """Update analyst with feedback"""
        # Implementation would update analyst in database
        pass

class DataProvider:
    """Data provider specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def get_data(
        self,
        data_type: str,
        filters: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Get data"""
        # Implementation would query data sources
        return []

class InsightGenerator:
    """Insight generation specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def generate_insights(
        self,
        data: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate insights from data"""
        # Implementation would generate insights
        return []
```

---

## Tooling & Tech Stack

### Analyst Research Tools
- **Gartner**: Analyst research
- **Forrester**: Analyst research
- **CB Insights**: Analyst insights
- **IDC**: Analyst research
- **Klearbit**: Analyst research

### Briefing Tools
- **Zoom**: Video conferencing
- **Google Meet**: Video conferencing
- **Microsoft Teams**: Collaboration
- **Notion**: Documentation
- **Figma**: Design

### Content Tools
- **PowerPoint**: Presentation
- **Google Slides**: Presentation
- **Keynote**: Presentation
- **Canva**: Design
- **Visme**: Design

### CRM Tools
- **Salesforce**: CRM
- **HubSpot**: CRM
- **Pipedrive**: CRM
- **Monday.com**: Sales pipeline

---

## Configuration Essentials

### Analyst Relations Configuration

```yaml
# config/analyst_relations_config.yaml
analyst_relations:
  identification:
    industries:
      - "technology"
      - "enterprise"
      - "saas"
      - "cloud_native"
    
    regions:
      - "global"
      - "north_america"
      - "emea"
      - "apac"
      - "latam"
    
    coverage_areas:
      - "technology"
      - "industry"
      - "region"
      - "function"
    
    scoring:
      weights:
        relevance: 0.4
        influence: 0.3
        engagement: 0.3
      
      tiers:
        tier_1:
          count: 5
          score_threshold: 0.8
        
        tier_2:
          count: 10
          score_threshold: 0.6
        
        tier_3:
          count: 15
          score_threshold: 0.4
        
        tier_4:
          count: 20
          score_threshold: 0.2
  
  briefing:
    types:
      - "inquiry"
      - "update"
      - "review"
      "launch"
    
    preparation_time: "2-4 weeks"
    participants:
      - "product_manager"
      - "cto"
      - "founder"
      - "sales_engineer"
    
    materials:
      - deck: true
      - one_pager: true
      - demo: true
      - data_package: true
  
  research_support:
    data_sources:
      - "product_analytics"
      - "usage_metrics"
      "customer_feedback"
      "market_data"
    
    feedback_collection:
      channels:
        - "post_briefing_survey"
        - "quarterly_checkin"
        - "annual_review"
      
      frequency:
        post_briefing: "1_week"
        quarterly_checkin: "3_months"
        annual_review: "12_months"
```

---

## Code Examples

### Good: Complete Analyst Relations Workflow

```python
# analyst_relations/workflow.py
import asyncio
import logging
from typing import Dict, Any

from analyst_relations.identifier import AnalystIdentifier
from analyst_relations.briefing import BriefingManager
from analyst_relations.research import ResearchSupport

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_analyst_relations():
    """Run analyst relations workflow"""
    logger.info("=" * 60)
    logger.info("Analyst Relations Workflow")
    logger.info("=" * 60)
    
    # Load configuration
    config = load_config('config/analyst_relations_config.yaml')
    
    # Step 1: Identify analysts
    logger.info("\n" + "=" * 60)
    logger.info("Step 1: Identifying Analysts")
    logger.info("=" * 60)
    
    identifier = AnalystIdentifier(config)
    
    criteria = {
        'industry': 'technology',
        'region': 'global',
        'coverage_areas': ['technology', 'enterprise']
    }
    
    analysts = await identifier.identify_analysts(criteria)
    
    logger.info(f"Identified {len(analysts)} analysts")
    print_analysts_summary(analysts)
    
    # Step 2: Select target analysts
    logger.info("\n" + "=" * 60)
    logger.info("Step 2: Selecting Target Analysts")
    target_analysts = analysts[:10]  # Top 10 analysts
    
    logger.info(f"Selected {len(target_analysts)} target analysts")
    print_target_analysts_summary(target_analysts)
    
    # Step 3: Schedule briefings
    logger.info("\n" + "=" * 60)
    logger.info("Step 3: Scheduling Briefings")
    logger.info("=" * 60)
    
    briefing_manager = BriefingManager(config)
    
    briefings = []
    for analyst in target_analysts:
        briefing = await briefing_manager.schedule_briefing(
            analyst_id=analyst.analyst_id,
            briefing_type="inquiry",
            date=calculate_briefing_date(),
            participants=["product_manager", "cto", "founder"]
        )
        briefings.append(briefing)
    
    logger.info(f"Scheduled {len(briefings)} briefings")
    print_briefings_summary(briefings)
    
    # Step 4: Prepare briefing materials
    logger.info("\n" + "=" * 60)
    logger.info("Step 4: Preparing Briefing Materials")
    logger.info("=" * 60)
    
    for briefing in briefings[:3]:  # Prepare for first 3
        materials = await briefing_manager.prepare_briefing_materials(briefing['briefing_id'])
        
        logger.info(f"Materials prepared for briefing: {briefing['briefing_id']}")
    
    # Step 5: Provide research support
    logger.info("\n" + "=" * 60)
    logger.info("Step 5: Providing Research Support")
    logger.info("=" * 60)
    
    research_support = ResearchSupport(config)
    
    for analyst in target_analysts:
        research_request = {
            'request_id': f"req_{analyst.analyst_id}",
            'analyst_id': analyst.analyst_id,
            'data_types': ['product_analytics', 'usage_metrics']
        }
        
        response = await research_support.provide_research_data(
            analyst.analyst_id,
            research_request
        )
        
        logger.info(f"Research data provided to {analyst.analyst_id}")
    
    # Print summary
    print_summary(analysts, target_analysts, briefings)

def calculate_briefing_date() -> str:
    """Calculate briefing date"""
    from datetime import timedelta
    return (datetime.utcnow() + timedelta(weeks=2)).isoformat()

def print_analysts_summary(analysts: list):
    """Print analysts summary"""
    print(f"\nAnalysts Summary:")
    print(f"  Total: {len(analysts)}")
    print(f"  Tier 1: {len([a for a in analysts if a.tier == 'tier_1'])}")
    print(f"  Tier 2: {len([a for a in analysts if a.tier == 'tier_2'])}")
    print(f"  Tier 3: {len([a for a in analysts if a.tier == 'tier_3'])}")
    print(f"  Tier 4: {len([a for a in analysts if a.tier == 'tier_4'])}")

def print_target_analysts_summary(analysts: list):
    """Print target analysts summary"""
    print(f"\nTarget Analysts Summary:")
    for i, analyst in enumerate(analysts, 1):
        print(f"  {i}. {analyst.name} ({analyst.firm}) - {analyst.tier.value})")

def print_briefings_summary(briefings: list):
    """Print briefings summary"""
    print(f"\nBriefings Summary:")
    for i, briefing in enumerate(briefings, 1):
        print(f"  {i}. {briefing['analyst_name']} - {briefing['date']}")

def print_summary(
    analysts: list,
    target_analysts: list,
    briefings: list
):
    """Print summary"""
    print("\n" + "=" * 60)
    print("Analyst Relations Summary")
    print("=" * 60)
    print(f"Total Analysts: {len(analysts)}")
    print(f"Target Analysts: {len(target_analysts)}")
    print(f"Briefings Scheduled: {len(briefings)}")

def load_config(filename: str) -> Dict[str, Any]:
    """Load configuration from file"""
    import yaml
    with open(filename, 'r') as f:
        return yaml.safe_load(f)

async def main():
    """Main entry point"""
    await run_analyst_relations()

if __name__ == "__main__":
    asyncio.run(main())
```

### Bad: Anti-pattern Example

```python
# BAD: No analyst identification
def bad_analyst_relations():
    # No analyst identification
    pass

# BAD: No briefings
def bad_analyst_relations():
    # No briefings
    identify_analysts()

# BAD: No research support
def bad_analyst_relations():
    # No research support
    identify_analysts()
    schedule_briefings()

# BAD: No feedback
def bad_analyst_relations():
    # No feedback
    identify_analysts()
    schedule_briefings()
    provide_research_data()
```

---

## Standards, Compliance & Security

### Industry Standards
- **Analyst Relations**: Analyst relations best practices
- **Briefing Management**: Briefing management best practices
- **Research Support**: Research support best practices
- **Relationship Management**: Relationship management best practices

### Security Best Practices
- **Data Protection**: Protect company data
- **Access Control**: RBAC for analyst data
- **Audit Logging**: Log all analyst activities
- **Confidentiality**: Maintain confidentiality

### Compliance Requirements
- **GDPR**: Data protection compliance
- **Data Privacy**: Protect analyst privacy
- **Confidentiality**: Maintain confidentiality
- **Industry Regulations**: Follow industry regulations

---

## Quick Start

### 1. Install Dependencies

```bash
pip install pyyaml
```

### 2. Configure Analyst Relations

```bash
# Copy example config
cp config/analyst_relations_config.yaml.example config/analyst_relations_config.yaml

# Edit configuration
vim config/analyst_relations_config.yaml
```

### 3. Run Analyst Relations

```bash
python analyst_relations/workflow.py
```

### 4. View Results

```bash
# View analysts
cat analyst_relations/results/analysts.json

# View briefings
cat analyst_relations/results/briefings/
```

---

## Production Checklist

### Analyst Identification
- [ ] Analyst types defined
- [ ] Research sources configured
- [ ] Scoring framework defined
- [ ] Tiers defined
- [ ] Target analysts selected

### Briefing Management
- [ ] Briefing types defined
- [ ] Scheduling process defined
- [ ] Materials templates created
- [ ] Calendar integration configured
- [ ] Follow-up process defined

### Research Support
- [ ] Data sources configured
- [ ] Insight generation configured
- ] Feedback collection defined
- ] Data access controls defined
- ] Support processes defined

### Relationship Management
- [ ] Engagement tracking configured
- [ ] Scoring system defined
- [ ] Feedback loops defined
- ] Review cadence defined
- ] Success metrics defined

---

## Anti-patterns

### ❌ Avoid These Practices

1. **No Analyst Identification**
   ```python
   # BAD: No analyst identification
   pass
   ```

2. **No Briefings**
   ```python
   # BAD: No briefings
   identify_analysts()
   ```

3. **No Research Support**
   ```python
   # BAD: No research support
   identify_analysts()
   schedule_briefings()
   ```

4. **No Feedback**
   ```python
   # BAD: No feedback
   identify_analysts()
   schedule_briefings()
   provide_research_data()
   ```

### ✅ Follow These Practices

1. **Identify Analysts**
   ```python
   # GOOD: Identify analysts
   identifier = AnalystIdentifier(config)
   analysts = await identifier.identify_analysts(criteria)
   ```

2. **Schedule Briefings**
   ```python
   # GOOD: Schedule briefings
   briefing_manager = BriefingManager(config)
   briefing = await briefing_manager.schedule_briefing(analyst_id, type, date, participants)
   ```

3. **Provide Research Support**
   ```python
   # GOOD: Provide research support
   research_support = ResearchSupport(config)
   response = await research_support.provide_research_data(analyst_id, request)
   ```

4. **Collect Feedback**
   ```python
   # GOOD: Collect feedback
   feedback = await research_support.collect_feedback(analyst_id)
   ```

---

## Unit Economics & KPIs

### Development Costs
- **Initial Setup**: 20-40 hours
- **Analyst Identification**: 20-40 hours
- **Briefing Management**: 20-40 hours
- **Research Support**: 20-40 hours
- **Total**: 80-160 hours

### Operational Costs
- **Research Tools**: $100-500/month
- **Briefing Tools**: $50-200/month
- **CRM Tools**: $100-500/month
- **Event Costs**: $200-1000/briefing

### ROI Metrics
- **Analyst Coverage**: 50-100% improvement
- **Report Mentions**: 40-60% improvement
- **Market Credibility**: 60-80% improvement
- **Deal Support**: 30-50% improvement

### KPI Targets
- **Analyst Coverage**: > 80% of target analysts
- **Briefing Completion**: > 90%
- **Research Data Quality**: > 95%
- **Analyst Satisfaction**: > 85%
- **Report Influence**: > 60%

---

## Integration Points / Related Skills

### Upstream Skills
- **136. Business to Technical Spec**: Requirements
- **137. API-First Product Strategy**: API design
- **138. Platform Product Design**: Platform design
- **146. Developer Relations & Community**: Community building
- **147. Technical Content Marketing**: Content marketing
- **148. Sales Engineering**: Sales engineering
- **149. Enterprise Sales Alignment**: Sales alignment
- **150. Partner Program Design**: Partner programs

### Parallel Skills
- **152. Launch Strategy Execution**: Launch strategy

### Downstream Skills
- None (Final skill in domain)

### Cross-Domain Skills
- **18. Project Management**: Project planning
- **81. SaaS FinOps Pricing**: Pricing strategy
- **82. Technical Product Management**: Product management
- **84. Compliance AI Governance**: Compliance

---

## References & Resources

### Documentation
- [Analyst Relations Guide](https://www.gartner.com/)
- [Briefing Best Practices](https://www.forrester.com/)
- [Research Support Guide](https://www.idc.com/)

### Best Practices
- [Analyst Relations Best Practices](https://www.cbinsights.com/)
- [Briefing Management](https://www.hbr.org/)
- [Research Support](https://www.mckinsey.com/)

### Tools & Libraries
- [Gartner](https://www.gartner.com/)
- [Forrester](https://www.forrester.com/)
- [IDC](https://www.idc.com/)
- [Zoom](https://zoom.us/)
- [PowerPoint](https://www.microsoft.com/en-us/microsoft-365/powerpoint)
- [Salesforce](https://www.salesforce.com/)
