---
name: Feature Prioritization
description: Prioritizing features using data-driven frameworks like RICE, WSJF, and value vs. effort analysis
---

# Feature Prioritization

## Current Level: Expert (Enterprise Scale)

## Domain: Technical Product Management
## Skill ID: 141

---

## Executive Summary

Feature Prioritization enables systematic evaluation and ranking of features using data-driven frameworks like RICE (Reach, Impact, Confidence, Effort), WSJF (Weighted Shortest Job First), and Value vs. Effort analysis. This capability is essential for maximizing product value, optimizing resource allocation, and ensuring strategic alignment.

### Strategic Necessity

- **Value Maximization**: Focus on highest-value features
- **Resource Optimization**: Allocate resources efficiently
- **Strategic Alignment**: Align features with business goals
- **Stakeholder Alignment**: Get consensus on priorities
- **Faster Time-to-Market**: Deliver high-value features first

---

## Technical Deep Dive

### Prioritization Frameworks

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Feature Prioritization Frameworks                      │
│                                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│  │   RICE       │    │   WSJF       │    │   Value vs   │                  │
│  │   Framework  │    │   Framework  │    │   Effort     │                  │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘                  │
│         │                   │                   │                           │
│         ▼                   ▼                   ▼                           │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Input Data Sources                               │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  User     │  │  Market   │  │  Business │  │  Technical │            │   │
│  │  │  Feedback │  │  Research │  │  Goals    │  │  Constraints│            │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘            │   │
│  └───────┼────────────┼────────────┼────────────┼────────────────────┘   │
│          │            │            │            │                         │
│          ▼            ▼            ▼            ▼                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Scoring & Ranking                               │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Calculate│  │  Weight   │  │  Normalize│  │  Rank     │            │   │
│  │  │  Scores   │  │  Factors  │  │  Scores   │  │  Features │            │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘            │   │
│  └───────┼────────────┼────────────┼────────────┼────────────────────┘   │
│          │            │            │            │                         │
│          ▼            ▼            ▼            ▼                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Output & Decision                               │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Priority│  │  Roadmap  │  │  Resource │  │  Stakeholder│            │   │
│  │  │  List    │  │  Planning │  │  Allocation│  │  Communication│            │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### RICE Framework

```python
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import asyncio
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class Impact(Enum):
    """Impact levels"""
    MASSIVE = 3
    HIGH = 2
    MEDIUM = 1
    LOW = 0.25
    MINIMAL = 0.125

class Confidence(Enum):
    """Confidence levels"""
    HIGH = 1.0
    MEDIUM = 0.8
    LOW = 0.5

@dataclass
class Feature:
    """Feature definition"""
    feature_id: str
    name: str
    description: str
    category: str
    owner: str
    status: str
    created_at: str

@dataclass
class RICEScore:
    """RICE score components"""
    reach: int  # Number of users affected
    impact: float  # Impact on users (0-3)
    confidence: float  # Confidence in estimates (0-1)
    effort: int  # Person-months of work
    score: float  # RICE score

@dataclass
class WSJFScore:
    """WSJF score components"""
    user_business_value: int  # User/business value (1-20)
    time_criticality: int  # Time criticality (1-20)
    risk_reduction_or_opportunity_enablement: int  # Risk/opportunity (1-20)
    job_size: int  # Job size (1-20)
    score: float  # WSJF score

@dataclass
class PrioritizedFeature:
    """Prioritized feature with scores"""
    feature: Feature
    rice_score: Optional[RICEScore]
    wsjf_score: Optional[WSJFScore]
    value_effort_ratio: Optional[float]
    overall_score: float
    rank: int

class FeaturePrioritizer:
    """Feature prioritization specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.feature_store = FeatureStore(config['feature_store'])
        self.data_collector = DataCollector(config['data_collection'])
        self.stakeholder_manager = StakeholderManager(config['stakeholder'])
        
    async def prioritize_features(
        self,
        framework: str = "rice",
        filters: Optional[Dict[str, Any]] = None
    ) -> List[PrioritizedFeature]:
        """Prioritize features using specified framework"""
        logger.info(f"Prioritizing features using {framework.upper()} framework...")
        
        # Get features
        features = await self.feature_store.get_features(filters)
        
        # Collect data for features
        logger.info("Collecting feature data...")
        feature_data = await self._collect_feature_data(features)
        
        # Calculate scores
        logger.info("Calculating scores...")
        prioritized_features = []
        
        for feature in features:
            data = feature_data[feature.feature_id]
            
            if framework == "rice":
                rice_score = self._calculate_rice_score(feature, data)
                prioritized_feature = PrioritizedFeature(
                    feature=feature,
                    rice_score=rice_score,
                    wsjf_score=None,
                    value_effort_ratio=None,
                    overall_score=rice_score.score,
                    rank=0
                )
            elif framework == "wsjf":
                wsjf_score = self._calculate_wsjf_score(feature, data)
                prioritized_feature = PrioritizedFeature(
                    feature=feature,
                    rice_score=None,
                    wsjf_score=wsjf_score,
                    value_effort_ratio=None,
                    overall_score=wsjf_score.score,
                    rank=0
                )
            elif framework == "value_effort":
                ve_ratio = self._calculate_value_effort_ratio(feature, data)
                prioritized_feature = PrioritizedFeature(
                    feature=feature,
                    rice_score=None,
                    wsjf_score=None,
                    value_effort_ratio=ve_ratio,
                    overall_score=ve_ratio,
                    rank=0
                )
            else:
                raise ValueError(f"Unknown framework: {framework}")
            
            prioritized_features.append(prioritized_feature)
        
        # Sort by score
        prioritized_features.sort(key=lambda f: f.overall_score, reverse=True)
        
        # Assign ranks
        for i, feature in enumerate(prioritized_features):
            feature.rank = i + 1
        
        logger.info(f"Prioritized {len(prioritized_features)} features")
        
        return prioritized_features
    
    async def _collect_feature_data(
        self,
        features: List[Feature]
    ) -> Dict[str, Dict[str, Any]]:
        """Collect data for features"""
        feature_data = {}
        
        for feature in features:
            # Collect user feedback
            user_feedback = await self.data_collector.collect_user_feedback(feature)
            
            # Collect market research
            market_research = await self.data_collector.collect_market_research(feature)
            
            # Collect business goals alignment
            business_alignment = await self.data_collector.collect_business_alignment(feature)
            
            # Collect technical estimates
            technical_estimates = await self.data_collector.collect_technical_estimates(feature)
            
            feature_data[feature.feature_id] = {
                'user_feedback': user_feedback,
                'market_research': market_research,
                'business_alignment': business_alignment,
                'technical_estimates': technical_estimates
            }
        
        return feature_data
    
    def _calculate_rice_score(
        self,
        feature: Feature,
        data: Dict[str, Any]
    ) -> RICEScore:
        """Calculate RICE score for feature"""
        # Reach: Number of users affected
        reach = self._estimate_reach(feature, data)
        
        # Impact: Impact on users
        impact = self._estimate_impact(feature, data)
        
        # Confidence: Confidence in estimates
        confidence = self._estimate_confidence(feature, data)
        
        # Effort: Person-months of work
        effort = self._estimate_effort(feature, data)
        
        # Calculate RICE score
        score = (reach * impact * confidence) / effort if effort > 0 else 0
        
        return RICEScore(
            reach=reach,
            impact=impact,
            confidence=confidence,
            effort=effort,
            score=score
        )
    
    def _estimate_reach(
        self,
        feature: Feature,
        data: Dict[str, Any]
    ) -> int:
        """Estimate reach for feature"""
        # Use user feedback and market research
        user_feedback = data['user_feedback']
        market_research = data['market_research']
        
        # Estimate based on user interest
        interested_users = user_feedback.get('interested_users', 0)
        
        # Adjust for market size
        market_size = market_research.get('market_size', 0)
        
        # Return estimate
        return min(interested_users, market_size)
    
    def _estimate_impact(
        self,
        feature: Feature,
        data: Dict[str, Any]
    ) -> float:
        """Estimate impact for feature"""
        # Use user feedback and business alignment
        user_feedback = data['user_feedback']
        business_alignment = data['business_alignment']
        
        # Get user impact rating
        user_impact = user_feedback.get('user_impact', Impact.MEDIUM)
        
        # Get business impact rating
        business_impact = business_alignment.get('business_impact', Impact.MEDIUM)
        
        # Return higher of the two
        return max(user_impact.value, business_impact.value)
    
    def _estimate_confidence(
        self,
        feature: Feature,
        data: Dict[str, Any]
    ) -> float:
        """Estimate confidence for feature"""
        # Use technical estimates and data quality
        technical_estimates = data['technical_estimates']
        
        # Check if estimates are available
        has_estimates = technical_estimates.get('has_estimates', False)
        
        # Check data quality
        data_quality = data.get('data_quality', Confidence.MEDIUM)
        
        # Return confidence
        if has_estimates and data_quality == Confidence.HIGH:
            return Confidence.HIGH.value
        elif has_estimates:
            return Confidence.MEDIUM.value
        else:
            return Confidence.LOW.value
    
    def _estimate_effort(
        self,
        feature: Feature,
        data: Dict[str, Any]
    ) -> int:
        """Estimate effort for feature"""
        # Use technical estimates
        technical_estimates = data['technical_estimates']
        
        # Get effort estimate in person-months
        effort = technical_estimates.get('effort_months', 1)
        
        # Ensure minimum effort
        return max(1, effort)
    
    def _calculate_wsjf_score(
        self,
        feature: Feature,
        data: Dict[str, Any]
    ) -> WSJFScore:
        """Calculate WSJF score for feature"""
        # User/Business Value: Value to users or business
        user_business_value = self._estimate_user_business_value(feature, data)
        
        # Time Criticality: How urgent is this feature
        time_criticality = self._estimate_time_criticality(feature, data)
        
        # Risk Reduction/Opportunity Enablement: Risk or opportunity
        risk_opportunity = self._estimate_risk_opportunity(feature, data)
        
        # Job Size: Size of the job
        job_size = self._estimate_job_size(feature, data)
        
        # Calculate WSJF score
        cost_of_delay = user_business_value + time_criticality + risk_opportunity
        score = cost_of_delay / job_size if job_size > 0 else 0
        
        return WSJFScore(
            user_business_value=user_business_value,
            time_criticality=time_criticality,
            risk_reduction_or_opportunity_enablement=risk_opportunity,
            job_size=job_size,
            score=score
        )
    
    def _estimate_user_business_value(
        self,
        feature: Feature,
        data: Dict[str, Any]
    ) -> int:
        """Estimate user/business value"""
        # Use business alignment and user feedback
        business_alignment = data['business_alignment']
        user_feedback = data['user_feedback']
        
        # Get business value rating (1-20)
        business_value = business_alignment.get('business_value', 10)
        
        # Get user value rating (1-20)
        user_value = user_feedback.get('user_value', 10)
        
        # Return average
        return (business_value + user_value) // 2
    
    def _estimate_time_criticality(
        self,
        feature: Feature,
        data: Dict[str, Any]
    ) -> int:
        """Estimate time criticality"""
        # Use business alignment
        business_alignment = data['business_alignment']
        
        # Get time criticality rating (1-20)
        time_criticality = business_alignment.get('time_criticality', 5)
        
        return time_criticality
    
    def _estimate_risk_opportunity(
        self,
        feature: Feature,
        data: Dict[str, Any]
    ) -> int:
        """Estimate risk reduction or opportunity enablement"""
        # Use business alignment
        business_alignment = data['business_alignment']
        
        # Get risk reduction rating (1-20)
        risk_reduction = business_alignment.get('risk_reduction', 5)
        
        # Get opportunity enablement rating (1-20)
        opportunity_enablement = business_alignment.get('opportunity_enablement', 5)
        
        # Return higher of the two
        return max(risk_reduction, opportunity_enablement)
    
    def _estimate_job_size(
        self,
        feature: Feature,
        data: Dict[str, Any]
    ) -> int:
        """Estimate job size"""
        # Use technical estimates
        technical_estimates = data['technical_estimates']
        
        # Get job size rating (1-20)
        job_size = technical_estimates.get('job_size', 10)
        
        return job_size
    
    def _calculate_value_effort_ratio(
        self,
        feature: Feature,
        data: Dict[str, Any]
    ) -> float:
        """Calculate value/effort ratio"""
        # Value: User/business value
        value = self._estimate_user_business_value(feature, data)
        
        # Effort: Job size
        effort = self._estimate_job_size(feature, data)
        
        # Calculate ratio
        return value / effort if effort > 0 else 0
    
    async def create_roadmap(
        self,
        prioritized_features: List[PrioritizedFeature],
        capacity: Dict[str, int],
        timeframe: str = "quarter"
    ) -> Dict[str, Any]:
        """Create roadmap from prioritized features"""
        logger.info(f"Creating {timeframe} roadmap...")
        
        # Calculate capacity
        total_capacity = capacity.get('total', 0)
        available_capacity = total_capacity
        
        # Allocate features to roadmap
        roadmap = {
            'timeframe': timeframe,
            'features': [],
            'total_features': 0,
            'total_effort': 0,
            'remaining_capacity': total_capacity
        }
        
        for feature in prioritized_features:
            # Get effort
            if feature.rice_score:
                effort = feature.rice_score.effort
            elif feature.wsjf_score:
                effort = feature.wsjf_score.job_size
            else:
                effort = 1
            
            # Check if feature fits in capacity
            if effort <= available_capacity:
                roadmap['features'].append({
                    'feature_id': feature.feature.feature_id,
                    'name': feature.feature.name,
                    'score': feature.overall_score,
                    'rank': feature.rank,
                    'effort': effort
                })
                roadmap['total_features'] += 1
                roadmap['total_effort'] += effort
                available_capacity -= effort
        
        roadmap['remaining_capacity'] = available_capacity
        
        logger.info(f"Roadmap created: {roadmap['total_features']} features")
        
        return roadmap

class FeatureStore:
    """Feature storage specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def get_features(
        self,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Feature]:
        """Get features with optional filters"""
        # Implementation would query database
        return []
    
    async def create_feature(self, feature: Feature):
        """Create feature"""
        # Implementation would insert feature
        pass
    
    async def update_feature(self, feature: Feature):
        """Update feature"""
        # Implementation would update feature
        pass

class DataCollector:
    """Data collection specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def collect_user_feedback(
        self,
        feature: Feature
    ) -> Dict[str, Any]:
        """Collect user feedback for feature"""
        # Implementation would collect from surveys, interviews, etc.
        return {}
    
    async def collect_market_research(
        self,
        feature: Feature
    ) -> Dict[str, Any]:
        """Collect market research for feature"""
        # Implementation would collect from market research
        return {}
    
    async def collect_business_alignment(
        self,
        feature: Feature
    ) -> Dict[str, Any]:
        """Collect business alignment for feature"""
        # Implementation would collect from business stakeholders
        return {}
    
    async def collect_technical_estimates(
        self,
        feature: Feature
    ) -> Dict[str, Any]:
        """Collect technical estimates for feature"""
        # Implementation would collect from engineering team
        return {}

class StakeholderManager:
    """Stakeholder management specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def get_stakeholder_feedback(
        self,
        feature: Feature
    ) -> Dict[str, Any]:
        """Get stakeholder feedback for feature"""
        # Implementation would collect from stakeholders
        return {}
    
    async def communicate_priorities(
        self,
        prioritized_features: List[PrioritizedFeature]
    ):
        """Communicate priorities to stakeholders"""
        # Implementation would send notifications
        pass
```

### Multi-Framework Analysis

```python
class MultiFrameworkAnalyzer:
    """Multi-framework analysis specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.prioritizer = FeaturePrioritizer(config)
        
    async def analyze_with_multiple_frameworks(
        self,
        features: List[Feature],
        frameworks: List[str] = ["rice", "wsjf", "value_effort"]
    ) -> Dict[str, List[PrioritizedFeature]]:
        """Analyze features with multiple frameworks"""
        logger.info(f"Analyzing with {len(frameworks)} frameworks...")
        
        results = {}
        
        for framework in frameworks:
            logger.info(f"Running {framework.upper()} analysis...")
            prioritized = await self.prioritizer.prioritize_features(
                framework=framework
            )
            results[framework] = prioritized
        
        logger.info("Multi-framework analysis complete")
        
        return results
    
    async def combine_framework_results(
        self,
        results: Dict[str, List[PrioritizedFeature]],
        weights: Optional[Dict[str, float]] = None
    ) -> List[PrioritizedFeature]:
        """Combine results from multiple frameworks"""
        logger.info("Combining framework results...")
        
        # Default weights
        if weights is None:
            weights = {
                'rice': 0.4,
                'wsjf': 0.4,
                'value_effort': 0.2
            }
        
        # Get all features
        all_features = set()
        for framework_results in results.values():
            for feature in framework_results:
                all_features.add(feature.feature.feature_id)
        
        # Calculate combined scores
        combined_features = []
        
        for feature_id in all_features:
            # Get feature from first framework
            feature = None
            for framework_results in results.values():
                for f in framework_results:
                    if f.feature.feature_id == feature_id:
                        feature = f.feature
                        break
                if feature:
                    break
            
            # Calculate combined score
            combined_score = 0.0
            total_weight = 0.0
            
            for framework, framework_results in results.items():
                for f in framework_results:
                    if f.feature.feature_id == feature_id:
                        combined_score += f.overall_score * weights.get(framework, 0)
                        total_weight += weights.get(framework, 0)
                        break
            
            # Normalize score
            if total_weight > 0:
                combined_score = combined_score / total_weight
            
            combined_features.append({
                'feature': feature,
                'combined_score': combined_score
            })
        
        # Sort by combined score
        combined_features.sort(key=lambda f: f['combined_score'], reverse=True)
        
        # Assign ranks
        for i, feature in enumerate(combined_features):
            feature['rank'] = i + 1
        
        logger.info(f"Combined {len(combined_features)} features")
        
        return combined_features
    
    async def identify_consensus(
        self,
        results: Dict[str, List[PrioritizedFeature]]
    ) -> Dict[str, Any]:
        """Identify consensus across frameworks"""
        logger.info("Identifying consensus...")
        
        # Get top 10 features from each framework
        top_features = {}
        
        for framework, framework_results in results.items():
            top_10 = framework_results[:10]
            top_features[framework] = [f.feature.feature_id for f in top_10]
        
        # Find features that appear in all frameworks
        consensus_features = set(top_features['rice'])
        
        for framework_features in top_features.values():
            consensus_features = consensus_features.intersection(set(framework_features))
        
        # Find features that appear in most frameworks
        frequent_features = {}
        
        for feature_id in all_features:
            count = 0
            for framework_features in top_features.values():
                if feature_id in framework_features:
                    count += 1
            frequent_features[feature_id] = count
        
        # Sort by frequency
        frequent_features = sorted(
            frequent_features.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return {
            'consensus_features': list(consensus_features),
            'frequent_features': frequent_features[:20]
        }
    
    async def identify_disagreements(
        self,
        results: Dict[str, List[PrioritizedFeature]]
    ) -> Dict[str, Any]:
        """Identify disagreements across frameworks"""
        logger.info("Identifying disagreements...")
        
        # Get features with high variance in ranking
        feature_ranks = {}
        
        for framework, framework_results in results.items():
            for feature in framework_results:
                feature_id = feature.feature.feature_id
                
                if feature_id not in feature_ranks:
                    feature_ranks[feature_id] = []
                
                feature_ranks[feature_id].append(feature.rank)
        
        # Calculate variance
        disagreements = []
        
        for feature_id, ranks in feature_ranks.items():
            if len(ranks) > 1:
                variance = sum((r - sum(ranks)/len(ranks))**2 for r in ranks) / len(ranks)
                
                if variance > 10:  # High variance threshold
                    disagreements.append({
                        'feature_id': feature_id,
                        'ranks': ranks,
                        'variance': variance
                    })
        
        # Sort by variance
        disagreements.sort(key=lambda x: x['variance'], reverse=True)
        
        logger.info(f"Found {len(disagreements)} disagreements")
        
        return {
            'disagreements': disagreements[:20]
        }
```

---

## Tooling & Tech Stack

### Prioritization Tools
- **Productboard**: Product prioritization platform
- **Aha!**: Product roadmap software
- **Roadmunk**: Roadmap planning tool
- **Pendo**: Product analytics and prioritization
- **Canny**: Feature request management

### Collaboration Tools
- **Notion**: Documentation and collaboration
- **Miro**: Visual collaboration
- **Figma**: Design collaboration
- **Mural**: Visual collaboration
- **Slack**: Team communication

### Analytics Tools
- **Mixpanel**: Product analytics
- **Amplitude**: Analytics platform
- **Google Analytics**: Web analytics
- **Heap**: User analytics

### Project Management
- **Jira**: Issue tracking
- **Asana**: Project management
- **Monday.com**: Work management
- **Linear**: Issue tracking

---

## Configuration Essentials

### Prioritization Configuration

```yaml
# config/prioritization_config.yaml
prioritization:
  framework: "rice"  # rice, wsjf, value_effort, multi
  
  rice:
    weights:
      reach: 1.0
      impact: 1.0
      confidence: 1.0
      effort: 1.0
  
  wsjf:
    weights:
      user_business_value: 1.0
      time_criticality: 1.0
      risk_reduction_or_opportunity_enablement: 1.0
      job_size: 1.0
  
  value_effort:
    weights:
      value: 1.0
      effort: 1.0
  
  multi_framework:
    frameworks:
      - rice
      - wsjf
      - value_effort
    
    weights:
      rice: 0.4
      wsjf: 0.4
      value_effort: 0.2
  
  filters:
    status:
      - "backlog"
      - "proposed"
    
    category:
      - "core"
      - "enhancement"
      - "new_feature"

  scoring:
    min_score: 0.0
    max_score: 100.0
    
    thresholds:
      high: 75.0
      medium: 50.0
      low: 25.0

  roadmap:
    timeframe: "quarter"
    capacity:
      total: 12  # person-months
      team_size: 4
      sprint_length: 2  # weeks
    
    allocation:
      new_features: 0.6
      enhancements: 0.3
      technical_debt: 0.1
```

### Feature Configuration

```yaml
# config/feature_config.yaml
features:
  categories:
    - name: "core"
      description: "Core product features"
      priority_weight: 1.2
    
    - name: "enhancement"
      description: "Feature enhancements"
      priority_weight: 1.0
    
    - name: "new_feature"
      description: "New features"
      priority_weight: 1.1
    
    - name: "technical_debt"
      description: "Technical debt items"
      priority_weight: 0.8

  impact_levels:
    massive:
      value: 3.0
      description: "Massive impact on users"
    
    high:
      value: 2.0
      description: "High impact on users"
    
    medium:
      value: 1.0
      description: "Medium impact on users"
    
    low:
      value: 0.25
      description: "Low impact on users"
    
    minimal:
      value: 0.125
      description: "Minimal impact on users"

  confidence_levels:
    high:
      value: 1.0
      description: "High confidence in estimates"
    
    medium:
      value: 0.8
      description: "Medium confidence in estimates"
    
    low:
      value: 0.5
      description: "Low confidence in estimates"

  effort_scale:
    unit: "person_months"
    min: 1
    max: 12
    default: 3
```

---

## Code Examples

### Good: Complete Prioritization Workflow

```python
# prioritization/workflow.py
import asyncio
import logging
from typing import Dict, Any

from prioritization.prioritizer import FeaturePrioritizer
from prioritization.multi_framework import MultiFrameworkAnalyzer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_prioritization():
    """Run feature prioritization workflow"""
    logger.info("=" * 60)
    logger.info("Feature Prioritization Workflow")
    logger.info("=" * 60)
    
    # Load configuration
    config = load_config('config/prioritization_config.yaml')
    
    # Create prioritizer
    prioritizer = FeaturePrioritizer(config)
    
    # Step 1: Prioritize with RICE
    logger.info("\n" + "=" * 60)
    logger.info("Step 1: RICE Framework")
    logger.info("=" * 60)
    
    rice_results = await prioritizer.prioritize_features(framework="rice")
    
    logger.info(f"RICE prioritized {len(rice_results)} features")
    print_top_features(rice_results[:10], "RICE")
    
    # Step 2: Prioritize with WSJF
    logger.info("\n" + "=" * 60)
    logger.info("Step 2: WSJF Framework")
    logger.info("=" * 60)
    
    wsjf_results = await prioritizer.prioritize_features(framework="wsjf")
    
    logger.info(f"WSJF prioritized {len(wsjf_results)} features")
    print_top_features(wsjf_results[:10], "WSJF")
    
    # Step 3: Prioritize with Value/Effort
    logger.info("\n" + "=" * 60)
    logger.info("Step 3: Value/Effort Framework")
    logger.info("=" * 60)
    
    ve_results = await prioritizer.prioritize_features(framework="value_effort")
    
    logger.info(f"Value/Effort prioritized {len(ve_results)} features")
    print_top_features(ve_results[:10], "Value/Effort")
    
    # Step 4: Multi-framework analysis
    logger.info("\n" + "=" * 60)
    logger.info("Step 4: Multi-Framework Analysis")
    logger.info("=" * 60)
    
    analyzer = MultiFrameworkAnalyzer(config)
    multi_results = await analyzer.analyze_with_multiple_frameworks(
        features=[f.feature for f in rice_results],
        frameworks=['rice', 'wsjf', 'value_effort']
    )
    
    # Combine results
    combined_results = await analyzer.combine_framework_results(multi_results)
    
    logger.info(f"Combined {len(combined_results)} features")
    print_top_features(combined_results[:10], "Combined")
    
    # Step 5: Identify consensus
    logger.info("\n" + "=" * 60)
    logger.info("Step 5: Consensus Analysis")
    logger.info("=" * 60)
    
    consensus = await analyzer.identify_consensus(multi_results)
    
    logger.info(f"Consensus features: {len(consensus['consensus_features'])}")
    for feature_id in consensus['consensus_features'][:5]:
        logger.info(f"  - {feature_id}")
    
    # Step 6: Create roadmap
    logger.info("\n" + "=" * 60)
    logger.info("Step 6: Roadmap Creation")
    logger.info("=" * 60)
    
    roadmap = await prioritizer.create_roadmap(
        combined_results,
        capacity=config['roadmap']['capacity'],
        timeframe=config['roadmap']['timeframe']
    )
    
    logger.info(f"Roadmap created: {roadmap['total_features']} features")
    logger.info(f"Total effort: {roadmap['total_effort']} person-months")
    logger.info(f"Remaining capacity: {roadmap['remaining_capacity']} person-months")
    
    # Print summary
    print_summary(rice_results, wsjf_results, ve_results, combined_results, roadmap, consensus)

def print_top_features(features: list, framework: str):
    """Print top features"""
    print(f"\n{framework} Top 10 Features:")
    print("-" * 60)
    for i, feature in enumerate(features, 1):
        print(f"{i}. {feature.feature.name} (Score: {feature.overall_score:.2f})")
        if feature.rice_score:
            print(f"   RICE: Reach={feature.rice_score.reach}, Impact={feature.rice_score.impact}, "
                  f"Confidence={feature.rice_score.confidence}, Effort={feature.rice_score.effort}")
        elif feature.wsjf_score:
            print(f"   WSJF: Value={feature.wsjf_score.user_business_value}, "
                  f"Time={feature.wsjf_score.time_criticality}, "
                  f"Risk={feature.wsjf_score.risk_reduction_or_opportunity_enablement}, "
                  f"Size={feature.wsjf_score.job_size}")

def print_summary(
    rice_results: list,
    wsjf_results: list,
    ve_results: list,
    combined_results: list,
    roadmap: Dict[str, Any],
    consensus: Dict[str, Any]
):
    """Print prioritization summary"""
    print("\n" + "=" * 60)
    print("Prioritization Summary")
    print("=" * 60)
    print(f"Total Features: {len(rice_results)}")
    print(f"\nFramework Results:")
    print(f"  RICE: {len(rice_results)} features")
    print(f"  WSJF: {len(wsjf_results)} features")
    print(f"  Value/Effort: {len(ve_results)} features")
    print(f"  Combined: {len(combined_results)} features")
    print(f"\nConsensus Features: {len(consensus['consensus_features'])}")
    print(f"\nRoadmap:")
    print(f"  Timeframe: {roadmap['timeframe']}")
    print(f"  Features: {roadmap['total_features']}")
    print(f"  Total Effort: {roadmap['total_effort']} person-months")
    print(f"  Remaining Capacity: {roadmap['remaining_capacity']} person-months")

def load_config(filename: str) -> Dict[str, Any]:
    """Load configuration from file"""
    import yaml
    with open(filename, 'r') as f:
        return yaml.safe_load(f)

async def main():
    """Main entry point"""
    await run_prioritization()

if __name__ == "__main__":
    asyncio.run(main())
```

### Bad: Anti-pattern Example

```python
# BAD: No framework
def bad_prioritization():
    # Random prioritization
    random.shuffle(features)

# BAD: No data
def bad_prioritization():
    # Prioritize based on gut feeling
    prioritize_by_gut()

# BAD: Single stakeholder
def bad_prioritization():
    # Prioritize based on loudest stakeholder
    prioritize_by_loudest()

# BAD: No alignment
def bad_prioritization():
    # Prioritize without business alignment
    prioritize_without_alignment()

# BAD: No iteration
def bad_prioritization():
    # Prioritize once and never revisit
    prioritize_once()
```

---

## Standards, Compliance & Security

### Industry Standards
- **Product Management**: Product management best practices
- **Agile Methodology**: Agile development principles
- **Scrum**: Scrum framework for development
- **Kanban**: Kanban methodology

### Security Best Practices
- **Access Control**: RBAC for feature data
- **Audit Logging**: Log all prioritization activities
- **Data Privacy**: Protect sensitive feature data
- **Version Control**: Track all changes

### Compliance Requirements
- **Documentation**: Document all decisions
- **Audit Trail**: Maintain audit trail
- **Stakeholder Communication**: Communicate with stakeholders
- **Transparency**: Be transparent about process

---

## Quick Start

### 1. Install Dependencies

```bash
pip install pyyaml
pip install pandas
```

### 2. Configure Prioritization

```bash
# Copy example config
cp config/prioritization_config.yaml.example config/prioritization_config.yaml

# Edit configuration
vim config/prioritization_config.yaml
```

### 3. Run Prioritization

```bash
python prioritization/workflow.py
```

### 4. View Results

```bash
# View prioritized features
cat prioritization/results/prioritized_features.json

# View roadmap
cat prioritization/results/roadmap.json
```

---

## Production Checklist

### Data Collection
- [ ] User feedback collected
- [ ] Market research completed
- [ ] Business alignment documented
- [ ] Technical estimates gathered
- [ ] Stakeholder input obtained

### Scoring
- [ ] Framework selected
- [ ] Weights configured
- [ ] Scores calculated
- [ ] Results validated
- [ ] Thresholds defined

### Analysis
- [ ] Multiple frameworks used
- [ ] Consensus identified
- [ ] Disagreements analyzed
- [ ] Recommendations made
- [ ] Stakeholders informed

### Roadmap
- [ ] Capacity calculated
- [ ] Features allocated
- [ ] Timeline defined
- [ ] Dependencies identified
- [ ] Risks documented

### Communication
- [ ] Results documented
- [ ] Roadmap communicated
- [ ] Stakeholders aligned
- [ ] Team informed
- [ ] Feedback collected

---

## Anti-patterns

### ❌ Avoid These Practices

1. **No Framework**
   ```python
   # BAD: No framework
   random.shuffle(features)
   ```

2. **No Data**
   ```python
   # BAD: No data
   prioritize_by_gut()
   ```

3. **Single Stakeholder**
   ```python
   # BAD: Single stakeholder
   prioritize_by_loudest()
   ```

4. **No Alignment**
   ```python
   # BAD: No alignment
   prioritize_without_alignment()
   ```

5. **No Iteration**
   ```python
   # BAD: No iteration
   prioritize_once()
   ```

### ✅ Follow These Practices

1. **Use Framework**
   ```python
   # GOOD: Use framework
   prioritizer = FeaturePrioritizer(config)
   results = await prioritizer.prioritize_features(framework="rice")
   ```

2. **Collect Data**
   ```python
   # GOOD: Collect data
   data = await data_collector.collect_feature_data(features)
   ```

3. **Multiple Stakeholders**
   ```python
   # GOOD: Multiple stakeholders
   feedback = await stakeholder_manager.get_stakeholder_feedback(feature)
   ```

4. **Business Alignment**
   ```python
   # GOOD: Business alignment
   alignment = await data_collector.collect_business_alignment(feature)
   ```

5. **Iterate**
   ```python
   # GOOD: Iterate
   while True:
       results = await prioritize()
       feedback = await collect_feedback()
       adjust_priorities(feedback)
   ```

---

## Unit Economics & KPIs

### Development Costs
- **Initial Setup**: 20-40 hours
- **Data Collection**: 40-80 hours
- **Scoring**: 20-40 hours
- **Analysis**: 20-40 hours
- **Total**: 100-200 hours

### Operational Costs
- **Prioritization Tools**: $100-500/month
- **Analytics Tools**: $50-200/month
- **Collaboration Tools**: $50-100/month
- **Meeting Time**: 10-20 hours/month

### ROI Metrics
- **Value Delivered**: 60-80% improvement
- **Resource Efficiency**: 40-60% improvement
- **Stakeholder Alignment**: 70-90% improvement
- **Time-to-Market**: 30-50% faster

### KPI Targets
- **Prioritization Accuracy**: > 85%
- **Stakeholder Alignment**: > 90%
- **Resource Utilization**: > 85%
- **Feature Success Rate**: > 70%
- **Time to Prioritize**: < 2 weeks

---

## Integration Points / Related Skills

### Upstream Skills
- **136. Business to Technical Spec**: Requirements
- **137. API-First Product Strategy**: API design
- **138. Platform Product Design**: Platform design
- **139. Product Discovery Validation**: Validation

### Parallel Skills
- **140. Product Analytics Implementation**: Analytics
- **142. Technical Debt Prioritization**: Debt management
- **143. Competitive Intelligence**: Competitive analysis

### Downstream Skills
- **144. Product Roadmap Communication**: Roadmap
- **145. Cross-Functional Leadership**: Leadership

### Cross-Domain Skills
- **18. Project Management**: Project planning
- **19. Requirement Analysis**: Requirements gathering
- **81. SaaS FinOps Pricing**: Pricing strategy
- **84. Compliance AI Governance**: Compliance

---

## References & Resources

### Documentation
- [RICE Framework](https://www.intercom.com/blog/rice-scoring/)
- [WSJF Framework](https://www.scaledagileframework.com/wsjf/)
- [Product Prioritization Guide](https://www.productplan.com/)
- [Feature Prioritization Best Practices](https://www.productboard.com/)

### Best Practices
- [Product Management Best Practices](https://www.mindtheproduct.com/)
- [Agile Prioritization](https://www.agilealliance.org/)
- [Scrum Framework](https://www.scrum.org/)

### Tools & Libraries
- [Productboard](https://www.productboard.com/)
- [Aha!](https://www.aha.io/)
- [Roadmunk](https://roadmunk.com/)
- [Pendo](https://www.pendo.io/)
- [Canny](https://canny.io/)
