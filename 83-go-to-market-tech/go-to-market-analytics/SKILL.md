---
name: Go-to-Market Analytics
description: Analytics for marketing, sales, and customer success performance
---

# Go-to-Market Analytics

## Current Level: Expert (Enterprise Scale)

## Domain: Go-to-Market Tech
## Skill ID: 157

---

## Executive Summary

Go-to-Market Analytics enables analytics for marketing, sales, and customer success performance. This capability is essential for data-driven decision making, performance optimization, resource allocation, and revenue growth.

### Strategic Necessity

- **Data-Driven Decisions**: Enable data-driven decision making
- **Performance Optimization**: Optimize marketing, sales, and customer success performance
- **Resource Allocation**: Allocate resources effectively
- **Revenue Growth**: Drive revenue through insights
- **Visibility**: Improve end-to-end visibility

---

## Technical Deep Dive

### GTM Analytics Framework

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Go-to-Market Analytics Framework                       │
│                                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│  │   Marketing  │    │    Sales     │    │   Customer   │                  │
│  │   Analytics  │───▶│   Analytics  │───▶│   Success    │                  │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘                  │
│         │                   │                   │                           │
│         ▼                   ▼                   ▼                           │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Marketing Analytics                             │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Campaign   │  │  Lead       │  │  Conversion │  │  Attribution │            │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘            │   │
│  └───────┼────────────┼────────────┼────────────┼────────────┼────────────────────┘   │
│          │            │            │            │                         │
│          ▼            ▼            ▼            ▼                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Sales Analytics                                 │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Pipeline   │  │  Forecast   │  │  Deal       │  │  Rep        │            │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘            │   │
│  └───────┼────────────┼────────────┼────────────┼────────────┼────────────────────┘   │
│          │            │            │            │                         │
│          ▼            ▼            ▼            ▼                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Customer Success Analytics                     │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Health     │  │  Churn      │  │  Retention   │  │  LTV        │            │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘            │   │
│  └───────┼────────────┼────────────┼────────────┼────────────┼────────────────────┘   │
│          │            │            │            │                         │
│          ▼            ▼            ▼            ▼                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Revenue Analytics                              │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  ARR        │  │  MRR        │  │  LTV        │  │  CAC        │            │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘            │   │
│  └───────┼────────────┼────────────┼────────────┼────────────┼────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Marketing Analytics

```python
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import asyncio
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class CampaignStatus(Enum):
    """Campaign status"""
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"

class AttributionModel(Enum):
    """Attribution models"""
    FIRST_TOUCH = "first_touch"
    LAST_TOUCH = "last_touch"
    LINEAR = "linear"
    TIME_DECAY = "time_decay"
    POSITION_BASED = "position_based"
    MULTI_TOUCH = "multi_touch"

@dataclass
class CampaignMetrics:
    """Campaign metrics definition"""
    campaign_id: str
    name: str
    status: CampaignStatus
    impressions: int
    clicks: int
    leads: int
    conversions: int
    cost: float
    revenue: float
    roi: float
    created_at: str
    updated_at: str

class MarketingAnalyzer:
    """Marketing analytics specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.campaign_analyzer = CampaignAnalyzer(config['campaigns'])
        self.lead_analyzer = LeadAnalyzer(config['leads'])
        self.conversion_analyzer = ConversionAnalyzer(config['conversions'])
        self.attribution_analyzer = AttributionAnalyzer(config['attribution'])
        
    async def analyze_marketing(self) -> Dict[str, Any]:
        """Analyze marketing performance"""
        logger.info("Analyzing marketing performance...")
        
        # Analyze campaigns
        campaign_analysis = await self.campaign_analyzer.analyze_campaigns()
        
        # Analyze leads
        lead_analysis = await self.lead_analyzer.analyze_leads()
        
        # Analyze conversions
        conversion_analysis = await self.conversion_analyzer.analyze_conversions()
        
        # Analyze attribution
        attribution_analysis = await self.attribution_analyzer.analyze_attribution()
        
        # Compile results
        results = {
            'campaigns': campaign_analysis,
            'leads': lead_analysis,
            'conversions': conversion_analysis,
            'attribution': attribution_analysis,
            'analyzed_at': datetime.utcnow().isoformat()
        }
        
        logger.info("Marketing performance analyzed")
        
        return results

class CampaignAnalyzer:
    """Campaign analysis specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.campaign_store = CampaignStore(config['campaign_store'])
        
    async def analyze_campaigns(self) -> Dict[str, Any]:
        """Analyze campaigns"""
        logger.info("Analyzing campaigns...")
        
        # Get all campaigns
        campaigns = await self.campaign_store.list_campaigns()
        
        # Calculate metrics
        metrics = {
            'total_campaigns': len(campaigns),
            'active_campaigns': len([c for c in campaigns if c.status == CampaignStatus.ACTIVE]),
            'total_impressions': sum(c.impressions for c in campaigns),
            'total_clicks': sum(c.clicks for c in campaigns),
            'total_leads': sum(c.leads for c in campaigns),
            'total_conversions': sum(c.conversions for c in campaigns),
            'total_cost': sum(c.cost for c in campaigns),
            'total_revenue': sum(c.revenue for c in campaigns),
            'average_roi': sum(c.roi for c in campaigns) / len(campaigns) if campaigns else 0,
            'by_channel': self._calculate_by_channel(campaigns),
            'by_campaign': self._calculate_by_campaign(campaigns),
            'analyzed_at': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Campaigns analyzed: {len(campaigns)} campaigns")
        
        return metrics
    
    def _calculate_by_channel(
        self,
        campaigns: List[CampaignMetrics]
    ) -> Dict[str, Any]:
        """Calculate metrics by channel"""
        by_channel = {}
        for campaign in campaigns:
            channel = campaign.name.split('_')[0]
            if channel not in by_channel:
                by_channel[channel] = {
                    'impressions': 0,
                    'clicks': 0,
                    'leads': 0,
                    'conversions': 0,
                    'cost': 0.0,
                    'revenue': 0.0
                }
            by_channel[channel]['impressions'] += campaign.impressions
            by_channel[channel]['clicks'] += campaign.clicks
            by_channel[channel]['leads'] += campaign.leads
            by_channel[channel]['conversions'] += campaign.conversions
            by_channel[channel]['cost'] += campaign.cost
            by_channel[channel]['revenue'] += campaign.revenue
        return by_channel
    
    def _calculate_by_campaign(
        self,
        campaigns: List[CampaignMetrics]
    ) -> List[Dict[str, Any]]:
        """Calculate metrics by campaign"""
        return [
            {
                'campaign_id': c.campaign_id,
                'name': c.name,
                'status': c.status.value,
                'impressions': c.impressions,
                'clicks': c.clicks,
                'ctr': c.clicks / c.impressions if c.impressions > 0 else 0,
                'leads': c.leads,
                'conversions': c.conversions,
                'cost': c.cost,
                'revenue': c.revenue,
                'roi': c.roi
            }
            for c in campaigns
        ]

class LeadAnalyzer:
    """Lead analysis specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.lead_store = LeadStore(config['lead_store'])
        
    async def analyze_leads(self) -> Dict[str, Any]:
        """Analyze leads"""
        logger.info("Analyzing leads...")
        
        # Get all leads
        leads = await self.lead_store.list_leads()
        
        # Calculate metrics
        metrics = {
            'total_leads': len(leads),
            'by_source': self._calculate_by_source(leads),
            'by_status': self._calculate_by_status(leads),
            'by_channel': self._calculate_by_channel(leads),
            'conversion_rate': self._calculate_conversion_rate(leads),
            'analyzed_at': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Leads analyzed: {len(leads)} leads")
        
        return metrics
    
    def _calculate_by_source(self, leads: List[Any]) -> Dict[str, int]:
        """Calculate leads by source"""
        by_source = {}
        for lead in leads:
            source = lead.source if hasattr(lead, 'source') else 'unknown'
            by_source[source] = by_source.get(source, 0) + 1
        return by_source
    
    def _calculate_by_status(self, leads: List[Any]) -> Dict[str, int]:
        """Calculate leads by status"""
        by_status = {}
        for lead in leads:
            status = lead.status if hasattr(lead, 'status') else 'unknown'
            by_status[status] = by_status.get(status, 0) + 1
        return by_status
    
    def _calculate_by_channel(self, leads: List[Any]) -> Dict[str, int]:
        """Calculate leads by channel"""
        by_channel = {}
        for lead in leads:
            channel = lead.channel if hasattr(lead, 'channel') else 'unknown'
            by_channel[channel] = by_channel.get(channel, 0) + 1
        return by_channel
    
    def _calculate_conversion_rate(self, leads: List[Any]) -> float:
        """Calculate conversion rate"""
        converted = len([l for l in leads if hasattr(l, 'status') and l.status == 'converted'])
        return converted / len(leads) if leads else 0

class ConversionAnalyzer:
    """Conversion analysis specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def analyze_conversions(self) -> Dict[str, Any]:
        """Analyze conversions"""
        logger.info("Analyzing conversions...")
        # Implementation would analyze conversions
        return {}

class AttributionAnalyzer:
    """Attribution analysis specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def analyze_attribution(self) -> Dict[str, Any]:
        """Analyze attribution"""
        logger.info("Analyzing attribution...")
        
        # Analyze using different models
        first_touch = await self._analyze_first_touch()
        last_touch = await self._analyze_last_touch()
        linear = await self._analyze_linear()
        multi_touch = await self._analyze_multi_touch()
        
        attribution = {
            'first_touch': first_touch,
            'last_touch': last_touch,
            'linear': linear,
            'multi_touch': multi_touch,
            'analyzed_at': datetime.utcnow().isoformat()
        }
        
        logger.info("Attribution analyzed")
        
        return attribution
    
    async def _analyze_first_touch(self) -> Dict[str, Any]:
        """Analyze first touch attribution"""
        # Implementation would analyze first touch
        return {}
    
    async def _analyze_last_touch(self) -> Dict[str, Any]:
        """Analyze last touch attribution"""
        # Implementation would analyze last touch
        return {}
    
    async def _analyze_linear(self) -> Dict[str, Any]:
        """Analyze linear attribution"""
        # Implementation would analyze linear
        return {}
    
    async def _analyze_multi_touch(self) -> Dict[str, Any]:
        """Analyze multi-touch attribution"""
        # Implementation would analyze multi-touch
        return {}

class CampaignStore:
    """Campaign storage specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def list_campaigns(self) -> List[CampaignMetrics]:
        """List campaigns"""
        # Implementation would query database
        return []

class LeadStore:
    """Lead storage specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def list_leads(self) -> List[Any]:
        """List leads"""
        # Implementation would query database
        return []
```

### Sales Analytics

```python
class SalesAnalyzer:
    """Sales analytics specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.pipeline_analyzer = PipelineAnalyzer(config['pipeline'])
        self.forecast_analyzer = ForecastAnalyzer(config['forecast'])
        self.deal_analyzer = DealAnalyzer(config['deals'])
        self.rep_analyzer = RepAnalyzer(config['reps'])
        
    async def analyze_sales(self) -> Dict[str, Any]:
        """Analyze sales performance"""
        logger.info("Analyzing sales performance...")
        
        # Analyze pipeline
        pipeline_analysis = await self.pipeline_analyzer.analyze_pipeline()
        
        # Analyze forecast
        forecast_analysis = await self.forecast_analyzer.analyze_forecast()
        
        # Analyze deals
        deal_analysis = await self.deal_analyzer.analyze_deals()
        
        # Analyze reps
        rep_analysis = await self.rep_analyzer.analyze_reps()
        
        # Compile results
        results = {
            'pipeline': pipeline_analysis,
            'forecast': forecast_analysis,
            'deals': deal_analysis,
            'reps': rep_analysis,
            'analyzed_at': datetime.utcnow().isoformat()
        }
        
        logger.info("Sales performance analyzed")
        
        return results

class PipelineAnalyzer:
    """Pipeline analysis specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.opportunity_store = OpportunityStore(config['opportunity_store'])
        
    async def analyze_pipeline(self) -> Dict[str, Any]:
        """Analyze pipeline"""
        logger.info("Analyzing pipeline...")
        
        # Get all opportunities
        opportunities = await self.opportunity_store.list_opportunities()
        
        # Calculate metrics
        metrics = {
            'total_opportunities': len(opportunities),
            'total_pipeline_value': sum(opp.amount for opp in opportunities),
            'weighted_pipeline_value': sum(opp.amount * opp.probability for opp in opportunities),
            'by_stage': self._calculate_by_stage(opportunities),
            'by_rep': self._calculate_by_rep(opportunities),
            'by_month': self._calculate_by_month(opportunities),
            'conversion_rate': self._calculate_conversion_rate(opportunities),
            'velocity': self._calculate_velocity(opportunities),
            'analyzed_at': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Pipeline analyzed: {len(opportunities)} opportunities")
        
        return metrics
    
    def _calculate_by_stage(
        self,
        opportunities: List[Any]
    ) -> Dict[str, Any]:
        """Calculate metrics by stage"""
        by_stage = {}
        for opp in opportunities:
            stage = opp.stage if hasattr(opp, 'stage') else 'unknown'
            if stage not in by_stage:
                by_stage[stage] = {
                    'count': 0,
                    'amount': 0.0,
                    'weighted_amount': 0.0
                }
            by_stage[stage]['count'] += 1
            by_stage[stage]['amount'] += opp.amount
            by_stage[stage]['weighted_amount'] += opp.amount * opp.probability
        return by_stage
    
    def _calculate_by_rep(
        self,
        opportunities: List[Any]
    ) -> Dict[str, Any]:
        """Calculate metrics by rep"""
        by_rep = {}
        for opp in opportunities:
            rep = opp.sales_rep if hasattr(opp, 'sales_rep') else 'unknown'
            if rep not in by_rep:
                by_rep[rep] = {
                    'count': 0,
                    'amount': 0.0,
                    'weighted_amount': 0.0
                }
            by_rep[rep]['count'] += 1
            by_rep[rep]['amount'] += opp.amount
            by_rep[rep]['weighted_amount'] += opp.amount * opp.probability
        return by_rep
    
    def _calculate_by_month(
        self,
        opportunities: List[Any]
    ) -> Dict[str, Any]:
        """Calculate metrics by month"""
        by_month = {}
        for opp in opportunities:
            month = opp.close_date[:7] if hasattr(opp, 'close_date') else 'unknown'
            if month not in by_month:
                by_month[month] = {
                    'count': 0,
                    'amount': 0.0,
                    'weighted_amount': 0.0
                }
            by_month[month]['count'] += 1
            by_month[month]['amount'] += opp.amount
            by_month[month]['weighted_amount'] += opp.amount * opp.probability
        return by_month
    
    def _calculate_conversion_rate(
        self,
        opportunities: List[Any]
    ) -> float:
        """Calculate conversion rate"""
        won = len([o for o in opportunities if hasattr(o, 'status') and o.status == 'won'])
        return won / len(opportunities) if opportunities else 0
    
    def _calculate_velocity(
        self,
        opportunities: List[Any]
    ) -> float:
        """Calculate pipeline velocity"""
        # Implementation would calculate velocity
        return 0.0

class ForecastAnalyzer:
    """Forecast analysis specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def analyze_forecast(self) -> Dict[str, Any]:
        """Analyze forecast"""
        logger.info("Analyzing forecast...")
        # Implementation would analyze forecast
        return {}

class DealAnalyzer:
    """Deal analysis specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def analyze_deals(self) -> Dict[str, Any]:
        """Analyze deals"""
        logger.info("Analyzing deals...")
        # Implementation would analyze deals
        return {}

class RepAnalyzer:
    """Rep analysis specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def analyze_reps(self) -> Dict[str, Any]:
        """Analyze reps"""
        logger.info("Analyzing reps...")
        # Implementation would analyze reps
        return {}

class OpportunityStore:
    """Opportunity storage specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def list_opportunities(self) -> List[Any]:
        """List opportunities"""
        # Implementation would query database
        return []
```

### Customer Success Analytics

```python
class CustomerSuccessAnalyzer:
    """Customer success analytics specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.health_analyzer = HealthAnalyzer(config['health'])
        self.churn_analyzer = ChurnAnalyzer(config['churn'])
        self.retention_analyzer = RetentionAnalyzer(config['retention'])
        self.ltv_analyzer = LTVAnalyzer(config['ltv'])
        
    async def analyze_customer_success(self) -> Dict[str, Any]:
        """Analyze customer success performance"""
        logger.info("Analyzing customer success performance...")
        
        # Analyze health
        health_analysis = await self.health_analyzer.analyze_health()
        
        # Analyze churn
        churn_analysis = await self.churn_analyzer.analyze_churn()
        
        # Analyze retention
        retention_analysis = await self.retention_analyzer.analyze_retention()
        
        # Analyze LTV
        ltv_analysis = await self.ltv_analyzer.analyze_ltv()
        
        # Compile results
        results = {
            'health': health_analysis,
            'churn': churn_analysis,
            'retention': retention_analysis,
            'ltv': ltv_analysis,
            'analyzed_at': datetime.utcnow().isoformat()
        }
        
        logger.info("Customer success performance analyzed")
        
        return results

class HealthAnalyzer:
    """Health analysis specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def analyze_health(self) -> Dict[str, Any]:
        """Analyze health"""
        logger.info("Analyzing health...")
        # Implementation would analyze health
        return {}

class ChurnAnalyzer:
    """Churn analysis specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def analyze_churn(self) -> Dict[str, Any]:
        """Analyze churn"""
        logger.info("Analyzing churn...")
        # Implementation would analyze churn
        return {}

class RetentionAnalyzer:
    """Retention analysis specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def analyze_retention(self) -> Dict[str, Any]:
        """Analyze retention"""
        logger.info("Analyzing retention...")
        # Implementation would analyze retention
        return {}

class LTVAnalyzer:
    """LTV analysis specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def analyze_ltv(self) -> Dict[str, Any]:
        """Analyze LTV"""
        logger.info("Analyzing LTV...")
        # Implementation would analyze LTV
        return {}
```

### Revenue Analytics

```python
class RevenueAnalyzer:
    """Revenue analytics specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.arr_analyzer = ARRAnalyzer(config['arr'])
        self.mrr_analyzer = MRRAnalyzer(config['mrr'])
        self.ltv_analyzer = LTVAnalyzer(config['ltv'])
        self.cac_analyzer = CACAnalyzer(config['cac'])
        
    async def analyze_revenue(self) -> Dict[str, Any]:
        """Analyze revenue"""
        logger.info("Analyzing revenue...")
        
        # Analyze ARR
        arr_analysis = await self.arr_analyzer.analyze_arr()
        
        # Analyze MRR
        mrr_analysis = await self.mrr_analyzer.analyze_mrr()
        
        # Analyze LTV
        ltv_analysis = await self.ltv_analyzer.analyze_ltv()
        
        # Analyze CAC
        cac_analysis = await self.cac_analyzer.analyze_cac()
        
        # Compile results
        results = {
            'arr': arr_analysis,
            'mrr': mrr_analysis,
            'ltv': ltv_analysis,
            'cac': cac_analysis,
            'ltv_cac_ratio': ltv_analysis.get('average', 0) / cac_analysis.get('average', 1),
            'analyzed_at': datetime.utcnow().isoformat()
        }
        
        logger.info("Revenue analyzed")
        
        return results

class ARRAnalyzer:
    """ARR analysis specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def analyze_arr(self) -> Dict[str, Any]:
        """Analyze ARR"""
        logger.info("Analyzing ARR...")
        # Implementation would analyze ARR
        return {}

class MRRAnalyzer:
    """MRR analysis specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def analyze_mrr(self) -> Dict[str, Any]:
        """Analyze MRR"""
        logger.info("Analyzing MRR...")
        # Implementation would analyze MRR
        return {}

class CACAnalyzer:
    """CAC analysis specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def analyze_cac(self) -> Dict[str, Any]:
        """Analyze CAC"""
        logger.info("Analyzing CAC...")
        # Implementation would analyze CAC
        return {}
```

---

## Tooling & Tech Stack

### Analytics Tools
- **Google Analytics**: Web analytics
- **Mixpanel**: Product analytics
- **Amplitude**: Analytics platform
- **Heap**: Product analytics
- **Segment**: Data collection

### Business Intelligence
- **Tableau**: Business intelligence
- **Power BI**: Business intelligence
- **Looker**: Business intelligence
- **Metabase**: Open source BI
- **Superset**: Open source BI

### Data Warehousing
- **Snowflake**: Data warehouse
- **BigQuery**: Data warehouse
- **Redshift**: Data warehouse
- **Databricks**: Data platform
- **ClickHouse**: Open source database

### Data Pipeline
- **Airflow**: Workflow automation
- **Prefect**: Workflow automation
- **Dagster**: Data orchestration
- **dbt**: Data transformation
- **Fivetran**: Data integration

---

## Configuration Essentials

### GTM Analytics Configuration

```yaml
# config/gtm_analytics_config.yaml
gtm_analytics:
  marketing:
    campaigns:
      enabled: true
      metrics:
        - impressions
        - clicks
        - leads
        - conversions
        - cost
        - revenue
        - roi
      
      dimensions:
        - channel
        - campaign
        - source
        - medium
    
    leads:
      enabled: true
      metrics:
        - total_leads
        - by_source
        - by_status
        - by_channel
        - conversion_rate
    
    conversions:
      enabled: true
      metrics:
        - total_conversions
        - conversion_rate
        - by_source
        - by_channel
    
    attribution:
      enabled: true
      models:
        - first_touch
        - last_touch
        - linear
        - time_decay
        - position_based
        - multi_touch
      
      default_model: "multi_touch"
  
  sales:
    pipeline:
      enabled: true
      metrics:
        - total_opportunities
        - total_pipeline_value
        - weighted_pipeline_value
        - by_stage
        - by_rep
        - by_month
        - conversion_rate
        - velocity
    
    forecast:
      enabled: true
      metrics:
        - forecast_accuracy
        - forecast_variance
        - by_rep
        - by_month
    
    deals:
      enabled: true
      metrics:
        - total_deals
        - won_deals
        - lost_deals
        - win_rate
        - deal_size
        - deal_velocity
    
    reps:
      enabled: true
      metrics:
        - total_reps
        - by_rep
        - quota_attainment
        - activity_metrics
  
  customer_success:
    health:
      enabled: true
      metrics:
        - average_health_score
        - by_segment
        - by_tier
    
    churn:
      enabled: true
      metrics:
        - churn_rate
        - by_segment
        - by_tier
        - by_reason
    
    retention:
      enabled: true
      metrics:
        - retention_rate
        - net_retention
        - gross_retention
        - by_segment
    
    ltv:
      enabled: true
      metrics:
        - average_ltv
        - by_segment
        - by_cohort
  
  revenue:
    arr:
      enabled: true
      metrics:
        - total_arr
        - new_arr
        - expansion_arr
        - churn_arr
        - net_arr
        - growth_rate
    
    mrr:
      enabled: true
      metrics:
        - total_mrr
        - new_mrr
        - expansion_mrr
        - churn_mrr
        - net_mrr
        - growth_rate
    
    ltv:
      enabled: true
      metrics:
        - average_ltv
        - by_segment
        - by_cohort
    
    cac:
      enabled: true
      metrics:
        - average_cac
        - by_channel
        - by_segment
    
    ltv_cac_ratio:
      enabled: true
      target: 3.0
```

---

## Code Examples

### Good: Complete GTM Analytics Workflow

```python
# gtm_analytics/workflow.py
import asyncio
import logging
from typing import Dict, Any

from gtm_analytics.marketing import MarketingAnalyzer
from gtm_analytics.sales import SalesAnalyzer
from gtm_analytics.customer_success import CustomerSuccessAnalyzer
from gtm_analytics.revenue import RevenueAnalyzer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_gtm_analytics():
    """Run GTM analytics workflow"""
    logger.info("=" * 60)
    logger.info("Go-to-Market Analytics Workflow")
    logger.info("=" * 60)
    
    # Load configuration
    config = load_config('config/gtm_analytics_config.yaml')
    
    # Step 1: Analyze marketing
    logger.info("\n" + "=" * 60)
    logger.info("Step 1: Analyzing Marketing")
    logger.info("=" * 60)
    
    marketing_analyzer = MarketingAnalyzer(config)
    
    marketing_results = await marketing_analyzer.analyze_marketing()
    
    logger.info("Marketing analyzed")
    print_marketing_summary(marketing_results)
    
    # Step 2: Analyze sales
    logger.info("\n" + "=" * 60)
    logger.info("Step 2: Analyzing Sales")
    logger.info("=" * 60)
    
    sales_analyzer = SalesAnalyzer(config)
    
    sales_results = await sales_analyzer.analyze_sales()
    
    logger.info("Sales analyzed")
    print_sales_summary(sales_results)
    
    # Step 3: Analyze customer success
    logger.info("\n" + "=" * 60)
    logger.info("Step 3: Analyzing Customer Success")
    logger.info("=" * 60)
    
    customer_success_analyzer = CustomerSuccessAnalyzer(config)
    
    customer_success_results = await customer_success_analyzer.analyze_customer_success()
    
    logger.info("Customer success analyzed")
    print_customer_success_summary(customer_success_results)
    
    # Step 4: Analyze revenue
    logger.info("\n" + "=" * 60)
    logger.info("Step 4: Analyzing Revenue")
    logger.info("=" * 60)
    
    revenue_analyzer = RevenueAnalyzer(config)
    
    revenue_results = await revenue_analyzer.analyze_revenue()
    
    logger.info("Revenue analyzed")
    print_revenue_summary(revenue_results)
    
    # Print summary
    print_summary(
        marketing_results,
        sales_results,
        customer_success_results,
        revenue_results
    )

def print_marketing_summary(results: Dict[str, Any]):
    """Print marketing summary"""
    campaigns = results['campaigns']
    print(f"\nMarketing Summary:")
    print(f"  Campaigns: {campaigns['total_campaigns']}")
    print(f"  Active: {campaigns['active_campaigns']}")
    print(f"  Impressions: {campaigns['total_impressions']:,}")
    print(f"  Clicks: {campaigns['total_clicks']:,}")
    print(f"  Leads: {campaigns['total_leads']:,}")
    print(f"  Conversions: {campaigns['total_conversions']:,}")
    print(f"  Cost: ${campaigns['total_cost']:,.2f}")
    print(f"  Revenue: ${campaigns['total_revenue']:,.2f}")
    print(f"  ROI: {campaigns['average_roi'] * 100:.1f}%")

def print_sales_summary(results: Dict[str, Any]):
    """Print sales summary"""
    pipeline = results['pipeline']
    print(f"\nSales Summary:")
    print(f"  Opportunities: {pipeline['total_opportunities']}")
    print(f"  Pipeline: ${pipeline['total_pipeline_value']:,.2f}")
    print(f"  Weighted Pipeline: ${pipeline['weighted_pipeline_value']:,.2f}")
    print(f"  Conversion Rate: {pipeline['conversion_rate'] * 100:.1f}%")

def print_customer_success_summary(results: Dict[str, Any]):
    """Print customer success summary"""
    print(f"\nCustomer Success Summary:")
    print(f"  Health: Analyzed")
    print(f"  Churn: Analyzed")
    print(f"  Retention: Analyzed")
    print(f"  LTV: Analyzed")

def print_revenue_summary(results: Dict[str, Any]):
    """Print revenue summary"""
    print(f"\nRevenue Summary:")
    print(f"  ARR: Analyzed")
    print(f"  MRR: Analyzed")
    print(f"  LTV: Analyzed")
    print(f"  CAC: Analyzed")
    print(f"  LTV:CAC Ratio: {results['ltv_cac_ratio']:.2f}")

def print_summary(
    marketing_results: Dict[str, Any],
    sales_results: Dict[str, Any],
    customer_success_results: Dict[str, Any],
    revenue_results: Dict[str, Any]
):
    """Print summary"""
    print("\n" + "=" * 60)
    print("GTM Analytics Summary")
    print("=" * 60)
    print(f"Marketing: Analyzed")
    print(f"Sales: Analyzed")
    print(f"Customer Success: Analyzed")
    print(f"Revenue: Analyzed")
    print(f"LTV:CAC Ratio: {revenue_results['ltv_cac_ratio']:.2f}")

def load_config(filename: str) -> Dict[str, Any]:
    """Load configuration from file"""
    import yaml
    with open(filename, 'r') as f:
        return yaml.safe_load(f)

async def main():
    """Main entry point"""
    await run_gtm_analytics()

if __name__ == "__main__":
    asyncio.run(main())
```

### Bad: Anti-pattern Example

```python
# BAD: No marketing analytics
def bad_gtm_analytics():
    # No marketing analytics
    pass

# BAD: No sales analytics
def bad_gtm_analytics():
    # No sales analytics
    analyze_marketing()

# BAD: No customer success analytics
def bad_gtm_analytics():
    # No customer success analytics
    analyze_marketing()
    analyze_sales()

# BAD: No revenue analytics
def bad_gtm_analytics():
    # No revenue analytics
    analyze_marketing()
    analyze_sales()
    analyze_customer_success()
```

---

## Standards, Compliance & Security

### Industry Standards
- **Analytics**: Analytics best practices
- **Data Privacy**: Data privacy best practices
- **Attribution**: Attribution best practices
- **Forecasting**: Forecasting best practices
- **Reporting**: Reporting best practices

### Security Best Practices
- **Data Protection**: Protect analytics data
- **Access Control**: RBAC for analytics data
- **Audit Logging**: Log all analytics activities
- **Privacy**: Maintain customer privacy

### Compliance Requirements
- **GDPR**: Data protection compliance
- **CCPA**: California privacy compliance
- **SOC 2**: Security and availability
- **ISO 27001**: Information security

---

## Quick Start

### 1. Install Dependencies

```bash
pip install pyyaml
```

### 2. Configure GTM Analytics

```bash
# Copy example config
cp config/gtm_analytics_config.yaml.example config/gtm_analytics_config.yaml

# Edit configuration
vim config/gtm_analytics_config.yaml
```

### 3. Run GTM Analytics

```bash
python gtm_analytics/workflow.py
```

### 4. View Results

```bash
# View marketing results
cat gtm_analytics/results/marketing.json

# View sales results
cat gtm_analytics/results/sales.json

# View customer success results
cat gtm_analytics/results/customer_success.json

# View revenue results
cat gtm_analytics/results/revenue.json
```

---

## Production Checklist

### Marketing Analytics
- [ ] Campaign tracking configured
- [ ] Lead tracking configured
- [ ] Conversion tracking configured
- [ ] Attribution model configured
- [ ] Data collection enabled
- [ ] Dashboards created

### Sales Analytics
- [ ] Pipeline tracking configured
- [ ] Forecast tracking configured
- [ ] Deal tracking configured
- [ ] Rep tracking configured
- [ ] Data collection enabled
- [ ] Dashboards created

### Customer Success Analytics
- [ ] Health tracking configured
- [ ] Churn tracking configured
- [ ] Retention tracking configured
- [ ] LTV tracking configured
- [ ] Data collection enabled
- [ ] Dashboards created

### Revenue Analytics
- [ ] ARR tracking configured
- [ ] MRR tracking configured
- [ ] LTV tracking configured
- [ ] CAC tracking configured
- [ ] Data collection enabled
- [ ] Dashboards created

### Integration
- [ ] Data sources integrated
- [ ] Data pipeline configured
- [ ] Data warehouse configured
- [ ] Data transformation configured
- [ ] Data quality validated
- [ ] Data governance defined

---

## Anti-patterns

### ❌ Avoid These Practices

1. **No Marketing Analytics**
   ```python
   # BAD: No marketing analytics
   pass
   ```

2. **No Sales Analytics**
   ```python
   # BAD: No sales analytics
   analyze_marketing()
   ```

3. **No Customer Success Analytics**
   ```python
   # BAD: No customer success analytics
   analyze_marketing()
   analyze_sales()
   ```

4. **No Revenue Analytics**
   ```python
   # BAD: No revenue analytics
   analyze_marketing()
   analyze_sales()
   analyze_customer_success()
   ```

### ✅ Follow These Practices

1. **Analyze Marketing**
   ```python
   # GOOD: Analyze marketing
   marketing_analyzer = MarketingAnalyzer(config)
   results = await marketing_analyzer.analyze_marketing()
   ```

2. **Analyze Sales**
   ```python
   # GOOD: Analyze sales
   sales_analyzer = SalesAnalyzer(config)
   results = await sales_analyzer.analyze_sales()
   ```

3. **Analyze Customer Success**
   ```python
   # GOOD: Analyze customer success
   customer_success_analyzer = CustomerSuccessAnalyzer(config)
   results = await customer_success_analyzer.analyze_customer_success()
   ```

4. **Analyze Everything**
   ```python
   # GOOD: Analyze everything
   marketing_analyzer = MarketingAnalyzer(config)
   sales_analyzer = SalesAnalyzer(config)
   customer_success_analyzer = CustomerSuccessAnalyzer(config)
   revenue_analyzer = RevenueAnalyzer(config)
   ```

---

## Unit Economics & KPIs

### Development Costs
- **Initial Setup**: 20-40 hours
- **Marketing Analytics**: 20-40 hours
- **Sales Analytics**: 20-40 hours
- **Customer Success Analytics**: 20-40 hours
- **Revenue Analytics**: 20-40 hours
- **Total**: 100-200 hours

### Operational Costs
- **Analytics Tools**: $200-1000/month
- **BI Tools**: $100-500/month
- **Data Warehouse**: $500-2000/month
- **Data Pipeline**: $100-300/month

### ROI Metrics
- **Decision Making**: 50-70% improvement
- **Performance Optimization**: 40-60% improvement
- **Resource Allocation**: 30-50% improvement
- **Revenue Growth**: 20-40% improvement

### KPI Targets
- **Data Quality**: > 95%
- **Report Accuracy**: > 95%
- **Dashboard Usage**: > 80%
- **Decision Speed**: < 24 hours
- **LTV:CAC Ratio**: > 3.0
- **Forecast Accuracy**: > 90%

---

## Integration Points / Related Skills

### Upstream Skills
- **136. Business to Technical Spec**: Requirements
- **137. API-First Product Strategy**: API design
- **138. Platform Product Design**: Platform design
- **139. Product Discovery Validation**: Validation
- **140. Product Analytics Implementation**: Analytics
- **141. Feature Prioritization**: Prioritization

### Parallel Skills
- **146. Developer Relations & Community**: Community building
- **147. Technical Content Marketing**: Content marketing
- **148. Sales Engineering**: Sales engineering
- **149. Enterprise Sales Alignment**: Sales alignment
- **150. Partner Program Design**: Partner programs
- **151. Analyst Relations**: Analyst relations
- **152. Launch Strategy Execution**: Launch strategy
- **153. Customer Success Automation**: Customer success
- **154. Demand Generation Automation**: Demand generation
- **155. Sales Operations Automation**: Sales operations
- **156. Revenue Operations RevOps**: Revenue operations

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
- [Marketing Analytics Guide](https://www.googleanalytics.com/)
- [Sales Analytics Guide](https://www.salesforce.com/)
- [Customer Success Analytics Guide](https://www.gainsight.com/)
- [Revenue Analytics Guide](https://www.clari.com/)

### Best Practices
- [Analytics Framework](https://www.mixpanel.com/)
- [Attribution Best Practices](https://www.amplitude.com/)
- [Forecasting Best Practices](https://www.insightsquared.com/)
- [Revenue Analytics](https://www.aviso.com/)

### Tools & Libraries
- [Google Analytics](https://analytics.google.com/)
- [Mixpanel](https://mixpanel.com/)
- [Amplitude](https://amplitude.com/)
- [Heap](https://heap.io/)
- [Segment](https://segment.com/)
- [Tableau](https://www.tableau.com/)
- [Power BI](https://powerbi.microsoft.com/)
- [Looker](https://looker.com/)
- [Snowflake](https://www.snowflake.com/)
- [BigQuery](https://cloud.google.com/bigquery)
- [Airflow](https://airflow.apache.org/)
- [Prefect](https://www.prefect.io/)
