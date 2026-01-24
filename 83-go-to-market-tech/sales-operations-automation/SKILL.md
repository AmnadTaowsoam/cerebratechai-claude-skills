---
name: Sales Operations Automation
description: Automating sales processes, forecasting, and pipeline management
---

# Sales Operations Automation

## Current Level: Expert (Enterprise Scale)

## Domain: Go-to-Market Tech
## Skill ID: 155

---

## Executive Summary

Sales Operations Automation enables automating sales processes, forecasting, and pipeline management. This capability is essential for improving sales efficiency, increasing forecast accuracy, reducing manual effort, and driving revenue growth.

### Strategic Necessity

- **Sales Efficiency**: Improve sales efficiency
- **Forecast Accuracy**: Increase forecast accuracy
- **Pipeline Visibility**: Improve pipeline visibility
- **Revenue Growth**: Drive revenue through sales
- **Sales Enablement**: Enable sales with tools

---

## Technical Deep Dive

### Sales Operations Framework

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Sales Operations Automation Framework                   │
│                                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│  │   Sales      │    │   Sales      │    │   Pipeline   │                  │
│  │   Process    │───▶│   Forecasting│───▶│   Management│                  │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘                  │
│         │                   │                   │                           │
│         ▼                   ▼                   ▼                           │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Sales Process Automation                         │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Lead       │  │  Opportunity  │  │  Quote      │  │  Contract   │            │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘            │   │
│  └───────┼────────────┼────────────┼────────────┼────────────┼────────────────────┘   │
│          │            │            │            │                         │
│          ▼            ▼            ▼            ▼                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Sales Forecasting                             │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Pipeline    │  │  Trend      │  │  Seasonal   │  │  ML Model   │            │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘            │   │
│  └───────┼────────────┼────────────┼────────────┼────────────┼────────────────────┘   │
│          │            │            │            │                         │
│          ▼            ▼            ▼            ▼                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Pipeline Management                            │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Tracking    │  │  Reporting   │  │  Analytics   │  │  Insights   │            │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘            │   │
│  └───────┼────────────┼────────────┼────────────┼────────────┼────────────────────┘   │
│          │            │            │            │                         │
│          ▼            ▼            ▼            ▼                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Sales Enablement                              │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Training    │  │  Content     │  │  Tools      │  │  Playbooks  │            │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘            │   │
│  └───────┼────────────┼────────────┼────────────┼────────────┼────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Sales Process Automation

```python
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import asyncio
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class OpportunityStage(Enum):
    """Opportunity stages"""
    LEAD = "lead"
    QUALIFIED = "qualified"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"

class OpportunityStatus(Enum):
    """Opportunity status"""
    OPEN = "open"
    WON = "won"
    LOST = "lost"

@dataclass
class Opportunity:
    """Opportunity definition"""
    opportunity_id: str
    lead_id: str
    account_name: str
    amount: float
    stage: OpportunityStage
    status: OpportunityStatus
    probability: float
    close_date: str
    sales_rep: str
    created_at: str
    updated_at: str
    metadata: Dict[str, Any]

class SalesProcessAutomator:
    """Sales process automation specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.opportunity_store = OpportunityStore(config['opportunity_store'])
        self.lead_store = LeadStore(config['lead_store'])
        self.quoter = Quoter(config['quoting'])
        self.contract_manager = ContractManager(config['contracts'])
        self.notification_service = NotificationService(config['notifications'])
        
    async def automate_lead_to_opportunity(
        self,
        lead_id: str
    ) -> Opportunity:
        """Automate lead to opportunity conversion"""
        logger.info(f"Automating lead to opportunity: {lead_id}")
        
        # Get lead
        lead = await self.lead_store.get_lead(lead_id)
        
        # Create opportunity
        opportunity = Opportunity(
            opportunity_id=self._generate_opportunity_id(),
            lead_id=lead_id,
            account_name=lead.company,
            amount=self._estimate_amount(lead),
            stage=OpportunityStage.LEAD,
            status=OpportunityStatus.OPEN,
            probability=0.1,
            close_date=self._estimate_close_date(),
            sales_rep=self._assign_sales_rep(lead),
            created_at=datetime.utcnow().isoformat(),
            updated_at=datetime.utcnow().isoformat(),
            metadata={}
        )
        
        # Store opportunity
        await self.opportunity_store.create_opportunity(opportunity)
        
        # Notify sales rep
        await self.notification_service.notify_sales_rep(
            sales_rep=opportunity.sales_rep,
            opportunity=opportunity
        )
        
        logger.info(f"Opportunity created: {opportunity.opportunity_id}")
        
        return opportunity
    
    async def automate_stage_transition(
        self,
        opportunity_id: str,
        new_stage: OpportunityStage
    ) -> Opportunity:
        """Automate stage transition"""
        logger.info(f"Automating stage transition: {opportunity_id} to {new_stage.value}")
        
        # Get opportunity
        opportunity = await self.opportunity_store.get_opportunity(opportunity_id)
        
        # Update stage
        old_stage = opportunity.stage
        opportunity.stage = new_stage
        opportunity.updated_at = datetime.utcnow().isoformat()
        
        # Update probability based on stage
        opportunity.probability = self._calculate_stage_probability(new_stage)
        
        # Store opportunity
        await self.opportunity_store.update_opportunity(opportunity)
        
        # Execute stage-specific actions
        await self._execute_stage_actions(opportunity, old_stage, new_stage)
        
        logger.info(f"Stage transitioned: {opportunity_id} from {old_stage.value} to {new_stage.value}")
        
        return opportunity
    
    async def _execute_stage_actions(
        self,
        opportunity: Opportunity,
        old_stage: OpportunityStage,
        new_stage: OpportunityStage
    ):
        """Execute stage-specific actions"""
        # Create quote if moving to proposal stage
        if new_stage == OpportunityStage.PROPOSAL:
            await self._create_quote(opportunity)
        
        # Prepare contract if moving to negotiation stage
        if new_stage == OpportunityStage.NEGOTIATION:
            await self._prepare_contract(opportunity)
        
        # Close opportunity if moving to closed stage
        if new_stage in [OpportunityStage.CLOSED_WON, OpportunityStage.CLOSED_LOST]:
            await self._close_opportunity(opportunity)
    
    async def _create_quote(self, opportunity: Opportunity):
        """Create quote"""
        logger.info(f"Creating quote for opportunity: {opportunity.opportunity_id}")
        
        # Create quote
        quote = await self.quoter.create_quote(opportunity)
        
        # Notify sales rep
        await self.notification_service.notify_sales_rep(
            sales_rep=opportunity.sales_rep,
            message=f"Quote created for opportunity {opportunity.opportunity_id}"
        )
        
        logger.info(f"Quote created for opportunity: {opportunity.opportunity_id}")
    
    async def _prepare_contract(self, opportunity: Opportunity):
        """Prepare contract"""
        logger.info(f"Preparing contract for opportunity: {opportunity.opportunity_id}")
        
        # Prepare contract
        contract = await self.contract_manager.prepare_contract(opportunity)
        
        # Notify sales rep
        await self.notification_service.notify_sales_rep(
            sales_rep=opportunity.sales_rep,
            message=f"Contract prepared for opportunity {opportunity.opportunity_id}"
        )
        
        logger.info(f"Contract prepared for opportunity: {opportunity.opportunity_id}")
    
    async def _close_opportunity(self, opportunity: Opportunity):
        """Close opportunity"""
        logger.info(f"Closing opportunity: {opportunity.opportunity_id}")
        
        # Update status
        if opportunity.stage == OpportunityStage.CLOSED_WON:
            opportunity.status = OpportunityStatus.WON
        else:
            opportunity.status = OpportunityStatus.LOST
        
        opportunity.updated_at = datetime.utcnow().isoformat()
        
        # Store opportunity
        await self.opportunity_store.update_opportunity(opportunity)
        
        logger.info(f"Opportunity closed: {opportunity.opportunity_id}")
    
    def _generate_opportunity_id(self) -> str:
        """Generate unique opportunity ID"""
        import uuid
        return f"opp_{uuid.uuid4().hex}"
    
    def _estimate_amount(self, lead) -> float:
        """Estimate opportunity amount"""
        # Implementation would estimate based on lead data
        return 10000.0
    
    def _estimate_close_date(self) -> str:
        """Estimate close date"""
        from datetime import timedelta
        return (datetime.utcnow() + timedelta(days=90)).isoformat()
    
    def _assign_sales_rep(self, lead) -> str:
        """Assign sales rep"""
        # Implementation would assign based on criteria
        return "sales_rep_1"
    
    def _calculate_stage_probability(self, stage: OpportunityStage) -> float:
        """Calculate stage probability"""
        probabilities = {
            OpportunityStage.LEAD: 0.1,
            OpportunityStage.QUALIFIED: 0.3,
            OpportunityStage.PROPOSAL: 0.5,
            OpportunityStage.NEGOTIATION: 0.7,
            OpportunityStage.CLOSED_WON: 1.0,
            OpportunityStage.CLOSED_LOST: 0.0
        }
        return probabilities.get(stage, 0.0)

class Quoter:
    """Quoting specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def create_quote(
        self,
        opportunity: Opportunity
    ) -> Dict[str, Any]:
        """Create quote"""
        logger.info(f"Creating quote for opportunity: {opportunity.opportunity_id}")
        
        # Generate quote
        quote = {
            'quote_id': self._generate_quote_id(),
            'opportunity_id': opportunity.opportunity_id,
            'amount': opportunity.amount,
            'items': [],
            'discount': 0.0,
            'total': opportunity.amount,
            'valid_until': self._calculate_valid_until(),
            'created_at': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Quote created: {quote['quote_id']}")
        
        return quote
    
    def _generate_quote_id(self) -> str:
        """Generate unique quote ID"""
        import uuid
        return f"quote_{uuid.uuid4().hex}"
    
    def _calculate_valid_until(self) -> str:
        """Calculate valid until date"""
        from datetime import timedelta
        return (datetime.utcnow() + timedelta(days=30)).isoformat()

class ContractManager:
    """Contract management specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def prepare_contract(
        self,
        opportunity: Opportunity
    ) -> Dict[str, Any]:
        """Prepare contract"""
        logger.info(f"Preparing contract for opportunity: {opportunity.opportunity_id}")
        
        # Generate contract
        contract = {
            'contract_id': self._generate_contract_id(),
            'opportunity_id': opportunity.opportunity_id,
            'account_name': opportunity.account_name,
            'amount': opportunity.amount,
            'terms': self._get_terms(),
            'created_at': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Contract prepared: {contract['contract_id']}")
        
        return contract
    
    def _generate_contract_id(self) -> str:
        """Generate unique contract ID"""
        import uuid
        return f"contract_{uuid.uuid4().hex}"
    
    def _get_terms(self) -> str:
        """Get contract terms"""
        # Implementation would get contract terms
        return "Standard terms and conditions apply"

class NotificationService:
    """Notification service specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def notify_sales_rep(
        self,
        sales_rep: str,
        opportunity: Optional[Opportunity] = None,
        message: Optional[str] = None
    ):
        """Notify sales rep"""
        logger.info(f"Notifying sales rep: {sales_rep}")
        # Implementation would notify sales rep
        pass

class OpportunityStore:
    """Opportunity storage specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def create_opportunity(self, opportunity: Opportunity):
        """Create opportunity"""
        # Implementation would store in database
        pass
    
    async def get_opportunity(self, opportunity_id: str) -> Opportunity:
        """Get opportunity"""
        # Implementation would query database
        return None
    
    async def update_opportunity(self, opportunity: Opportunity):
        """Update opportunity"""
        # Implementation would update database
        pass
    
    async def list_opportunities(
        self,
        stage: Optional[OpportunityStage] = None
    ) -> List[Opportunity]:
        """List opportunities"""
        # Implementation would query database
        return []

class LeadStore:
    """Lead storage specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def get_lead(self, lead_id: str):
        """Get lead"""
        # Implementation would query database
        return None
```

### Sales Forecasting

```python
class SalesForecaster:
    """Sales forecasting specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.opportunity_store = OpportunityStore(config['opportunity_store'])
        self.pipeline_analyzer = PipelineAnalyzer(config['pipeline'])
        self.trend_analyzer = TrendAnalyzer(config['trends'])
        self.seasonal_analyzer = SeasonalAnalyzer(config['seasonal'])
        self.ml_forecaster = MLForecaster(config['ml'])
        
    async def forecast_sales(
        self,
        period: str,
        method: str = "hybrid"
    ) -> Dict[str, Any]:
        """Forecast sales"""
        logger.info(f"Forecasting sales for period: {period}, method: {method}")
        
        # Get pipeline data
        pipeline_data = await self.opportunity_store.list_opportunities()
        
        # Calculate forecast based on method
        if method == "pipeline":
            forecast = await self._pipeline_forecast(pipeline_data, period)
        elif method == "trend":
            forecast = await self._trend_forecast(pipeline_data, period)
        elif method == "seasonal":
            forecast = await self._seasonal_forecast(pipeline_data, period)
        elif method == "ml":
            forecast = await self._ml_forecast(pipeline_data, period)
        else:
            forecast = await self._hybrid_forecast(pipeline_data, period)
        
        logger.info(f"Sales forecast completed: {forecast['total']}")
        
        return forecast
    
    async def _pipeline_forecast(
        self,
        pipeline_data: List[Opportunity],
        period: str
    ) -> Dict[str, Any]:
        """Calculate pipeline-based forecast"""
        logger.info("Calculating pipeline-based forecast...")
        
        # Analyze pipeline
        pipeline_analysis = await self.pipeline_analyzer.analyze_pipeline(pipeline_data)
        
        # Calculate forecast
        forecast = {
            'method': 'pipeline',
            'period': period,
            'by_stage': {},
            'by_sales_rep': {},
            'total': 0.0,
            'confidence': 0.7,
            'calculated_at': datetime.utcnow().isoformat()
        }
        
        # Calculate forecast by stage
        for stage, data in pipeline_analysis['by_stage'].items():
            stage_forecast = data['amount'] * data['weighted_probability']
            forecast['by_stage'][stage] = stage_forecast
            forecast['total'] += stage_forecast
        
        logger.info(f"Pipeline forecast calculated: {forecast['total']}")
        
        return forecast
    
    async def _trend_forecast(
        self,
        pipeline_data: List[Opportunity],
        period: str
    ) -> Dict[str, Any]:
        """Calculate trend-based forecast"""
        logger.info("Calculating trend-based forecast...")
        
        # Analyze trends
        trend_analysis = await self.trend_analyzer.analyze_trends(period)
        
        # Calculate forecast
        forecast = {
            'method': 'trend',
            'period': period,
            'trend': trend_analysis['trend'],
            'growth_rate': trend_analysis['growth_rate'],
            'forecast': trend_analysis['forecast'],
            'total': trend_analysis['forecast'],
            'confidence': 0.6,
            'calculated_at': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Trend forecast calculated: {forecast['total']}")
        
        return forecast
    
    async def _seasonal_forecast(
        self,
        pipeline_data: List[Opportunity],
        period: str
    ) -> Dict[str, Any]:
        """Calculate seasonal forecast"""
        logger.info("Calculating seasonal forecast...")
        
        # Analyze seasonality
        seasonal_analysis = await self.seasonal_analyzer.analyze_seasonality(period)
        
        # Calculate forecast
        forecast = {
            'method': 'seasonal',
            'period': period,
            'seasonal_factor': seasonal_analysis['seasonal_factor'],
            'forecast': seasonal_analysis['forecast'],
            'total': seasonal_analysis['forecast'],
            'confidence': 0.65,
            'calculated_at': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Seasonal forecast calculated: {forecast['total']}")
        
        return forecast
    
    async def _ml_forecast(
        self,
        pipeline_data: List[Opportunity],
        period: str
    ) -> Dict[str, Any]:
        """Calculate ML-based forecast"""
        logger.info("Calculating ML-based forecast...")
        
        # Run ML model
        ml_forecast = await self.ml_forecaster.predict(pipeline_data, period)
        
        forecast = {
            'method': 'ml',
            'period': period,
            'forecast': ml_forecast['forecast'],
            'total': ml_forecast['forecast'],
            'confidence': ml_forecast['confidence'],
            'calculated_at': datetime.utcnow().isoformat()
        }
        
        logger.info(f"ML forecast calculated: {forecast['total']}")
        
        return forecast
    
    async def _hybrid_forecast(
        self,
        pipeline_data: List[Opportunity],
        period: str
    ) -> Dict[str, Any]:
        """Calculate hybrid forecast"""
        logger.info("Calculating hybrid forecast...")
        
        # Get all forecasts
        pipeline_forecast = await self._pipeline_forecast(pipeline_data, period)
        trend_forecast = await self._trend_forecast(pipeline_data, period)
        seasonal_forecast = await self._seasonal_forecast(pipeline_data, period)
        ml_forecast = await self._ml_forecast(pipeline_data, period)
        
        # Calculate weighted average
        weights = {
            'pipeline': 0.3,
            'trend': 0.2,
            'seasonal': 0.2,
            'ml': 0.3
        }
        
        total_forecast = (
            pipeline_forecast['total'] * weights['pipeline'] +
            trend_forecast['total'] * weights['trend'] +
            seasonal_forecast['total'] * weights['seasonal'] +
            ml_forecast['total'] * weights['ml']
        )
        
        # Calculate confidence
        confidence = (
            pipeline_forecast['confidence'] * weights['pipeline'] +
            trend_forecast['confidence'] * weights['trend'] +
            seasonal_forecast['confidence'] * weights['seasonal'] +
            ml_forecast['confidence'] * weights['ml']
        )
        
        forecast = {
            'method': 'hybrid',
            'period': period,
            'pipeline': pipeline_forecast['total'],
            'trend': trend_forecast['total'],
            'seasonal': seasonal_forecast['total'],
            'ml': ml_forecast['total'],
            'total': total_forecast,
            'confidence': confidence,
            'calculated_at': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Hybrid forecast calculated: {forecast['total']}")
        
        return forecast

class PipelineAnalyzer:
    """Pipeline analysis specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def analyze_pipeline(
        self,
        pipeline_data: List[Opportunity]
    ) -> Dict[str, Any]:
        """Analyze pipeline"""
        logger.info("Analyzing pipeline...")
        
        # Group by stage
        by_stage = {}
        for opp in pipeline_data:
            if opp.stage.value not in by_stage:
                by_stage[opp.stage.value] = {
                    'count': 0,
                    'amount': 0.0,
                    'weighted_probability': 0.0
                }
            by_stage[opp.stage.value]['count'] += 1
            by_stage[opp.stage.value]['amount'] += opp.amount
            by_stage[opp.stage.value]['weighted_probability'] += opp.probability
        
        # Calculate weighted probability
        for stage, data in by_stage.items():
            if data['count'] > 0:
                data['weighted_probability'] /= data['count']
        
        # Calculate total pipeline
        total_pipeline = sum(data['amount'] for data in by_stage.values())
        
        analysis = {
            'by_stage': by_stage,
            'total': total_pipeline,
            'analyzed_at': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Pipeline analyzed: {total_pipeline}")
        
        return analysis

class TrendAnalyzer:
    """Trend analysis specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def analyze_trends(self, period: str) -> Dict[str, Any]:
        """Analyze trends"""
        logger.info("Analyzing trends...")
        # Implementation would analyze historical trends
        return {
            'trend': 'increasing',
            'growth_rate': 0.15,
            'forecast': 100000.0
        }

class SeasonalAnalyzer:
    """Seasonal analysis specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def analyze_seasonality(self, period: str) -> Dict[str, Any]:
        """Analyze seasonality"""
        logger.info("Analyzing seasonality...")
        # Implementation would analyze seasonal patterns
        return {
            'seasonal_factor': 1.2,
            'forecast': 120000.0
        }

class MLForecaster:
    """ML forecasting specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def predict(
        self,
        pipeline_data: List[Opportunity],
        period: str
    ) -> Dict[str, Any]:
        """Predict using ML model"""
        logger.info("Predicting using ML model...")
        # Implementation would use ML model to predict
        return {
            'forecast': 110000.0,
            'confidence': 0.8
        }
```

### Pipeline Management

```python
class PipelineManager:
    """Pipeline management specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.opportunity_store = OpportunityStore(config['opportunity_store'])
        self.pipeline_tracker = PipelineTracker(config['tracking'])
        self.pipeline_reporter = PipelineReporter(config['reporting'])
        self.pipeline_analytics = PipelineAnalytics(config['analytics'])
        self.pipeline_insights = PipelineInsights(config['insights'])
        
    async def manage_pipeline(self) -> Dict[str, Any]:
        """Manage pipeline"""
        logger.info("Managing pipeline...")
        
        # Track pipeline
        tracking = await self.pipeline_tracker.track_pipeline()
        
        # Generate reports
        reports = await self.pipeline_reporter.generate_reports()
        
        # Analyze pipeline
        analytics = await self.pipeline_analytics.analyze_pipeline()
        
        # Generate insights
        insights = await self.pipeline_insights.generate_insights()
        
        # Compile results
        results = {
            'tracking': tracking,
            'reports': reports,
            'analytics': analytics,
            'insights': insights,
            'managed_at': datetime.utcnow().isoformat()
        }
        
        logger.info("Pipeline managed")
        
        return results

class PipelineTracker:
    """Pipeline tracking specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.opportunity_store = OpportunityStore(config['opportunity_store'])
        
    async def track_pipeline(self) -> Dict[str, Any]:
        """Track pipeline"""
        logger.info("Tracking pipeline...")
        
        # Get all opportunities
        opportunities = await self.opportunity_store.list_opportunities()
        
        # Calculate pipeline metrics
        metrics = {
            'total_opportunities': len(opportunities),
            'total_pipeline_value': sum(opp.amount for opp in opportunities),
            'weighted_pipeline_value': sum(opp.amount * opp.probability for opp in opportunities),
            'by_stage': self._calculate_by_stage(opportunities),
            'by_sales_rep': self._calculate_by_sales_rep(opportunities),
            'by_month': self._calculate_by_month(opportunities),
            'tracked_at': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Pipeline tracked: {metrics['total_pipeline_value']}")
        
        return metrics
    
    def _calculate_by_stage(
        self,
        opportunities: List[Opportunity]
    ) -> Dict[str, Any]:
        """Calculate metrics by stage"""
        by_stage = {}
        for opp in opportunities:
            stage = opp.stage.value
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
    
    def _calculate_by_sales_rep(
        self,
        opportunities: List[Opportunity]
    ) -> Dict[str, Any]:
        """Calculate metrics by sales rep"""
        by_sales_rep = {}
        for opp in opportunities:
            rep = opp.sales_rep
            if rep not in by_sales_rep:
                by_sales_rep[rep] = {
                    'count': 0,
                    'amount': 0.0,
                    'weighted_amount': 0.0
                }
            by_sales_rep[rep]['count'] += 1
            by_sales_rep[rep]['amount'] += opp.amount
            by_sales_rep[rep]['weighted_amount'] += opp.amount * opp.probability
        return by_sales_rep
    
    def _calculate_by_month(
        self,
        opportunities: List[Opportunity]
    ) -> Dict[str, Any]:
        """Calculate metrics by month"""
        by_month = {}
        for opp in opportunities:
            month = opp.close_date[:7]  # YYYY-MM
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

class PipelineReporter:
    """Pipeline reporting specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def generate_reports(self) -> Dict[str, Any]:
        """Generate pipeline reports"""
        logger.info("Generating pipeline reports...")
        
        # Generate reports
        reports = {
            'pipeline_summary': await self._generate_pipeline_summary(),
            'stage_report': await self._generate_stage_report(),
            'sales_rep_report': await self._generate_sales_rep_report(),
            'trend_report': await self._generate_trend_report(),
            'generated_at': datetime.utcnow().isoformat()
        }
        
        logger.info("Pipeline reports generated")
        
        return reports
    
    async def _generate_pipeline_summary(self) -> Dict[str, Any]:
        """Generate pipeline summary"""
        # Implementation would generate pipeline summary
        return {}
    
    async def _generate_stage_report(self) -> Dict[str, Any]:
        """Generate stage report"""
        # Implementation would generate stage report
        return {}
    
    async def _generate_sales_rep_report(self) -> Dict[str, Any]:
        """Generate sales rep report"""
        # Implementation would generate sales rep report
        return {}
    
    async def _generate_trend_report(self) -> Dict[str, Any]:
        """Generate trend report"""
        # Implementation would generate trend report
        return {}

class PipelineAnalytics:
    """Pipeline analytics specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def analyze_pipeline(self) -> Dict[str, Any]:
        """Analyze pipeline"""
        logger.info("Analyzing pipeline...")
        # Implementation would analyze pipeline
        return {}

class PipelineInsights:
    """Pipeline insights specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def generate_insights(self) -> Dict[str, Any]:
        """Generate insights"""
        logger.info("Generating insights...")
        # Implementation would generate insights
        return {}
```

---

## Tooling & Tech Stack

### CRM Tools
- **Salesforce**: CRM platform
- **HubSpot**: CRM platform
- **Pipedrive**: CRM platform
- **Zoho CRM**: CRM platform
- **Monday.com**: Sales pipeline

### Forecasting Tools
- **Clari**: Sales forecasting
- **InsightSquared**: Sales analytics
- **Aviso**: AI forecasting
- **People.ai**: Sales AI
- **Gong**: Conversation intelligence

### Automation Tools
- **Zapier**: Automation
- **Make**: Automation
- **n8n**: Automation
- **Airflow**: Workflow automation
- **Prefect**: Workflow automation

### Analytics Tools
- **Tableau**: Business intelligence
- **Power BI**: Business intelligence
- **Looker**: Business intelligence
- **Google Analytics**: Web analytics
- **Mixpanel**: Product analytics

---

## Configuration Essentials

### Sales Operations Configuration

```yaml
# config/sales_operations_config.yaml
sales_operations:
  process_automation:
    lead_to_opportunity:
      enabled: true
      auto_assign: true
      auto_notify: true
    
    stage_transitions:
      lead_to_qualified:
        enabled: true
        auto_transition: false
      
      qualified_to_proposal:
        enabled: true
        auto_quote: true
      
      proposal_to_negotiation:
        enabled: true
        auto_contract: true
      
      negotiation_to_closed:
        enabled: true
        auto_close: false
    
    quoting:
      enabled: true
      auto_generate: true
      valid_days: 30
    
    contracts:
      enabled: true
      auto_prepare: true
      template: "standard"
  
  forecasting:
    methods:
      - pipeline
      - trend
      - seasonal
      - ml
      - hybrid
    
    pipeline:
      enabled: true
      weight: 0.3
    
    trend:
      enabled: true
      weight: 0.2
      historical_periods: 12
    
    seasonal:
      enabled: true
      weight: 0.2
      seasonal_periods: 4
    
    ml:
      enabled: true
      weight: 0.3
      model: "random_forest"
    
    hybrid:
      enabled: true
      weights:
        pipeline: 0.3
        trend: 0.2
        seasonal: 0.2
        ml: 0.3
    
    periods:
      - "month"
      - "quarter"
      - "year"
  
  pipeline_management:
    tracking:
      enabled: true
      metrics:
        - total_opportunities
        - total_pipeline_value
        - weighted_pipeline_value
        - by_stage
        - by_sales_rep
        - by_month
    
    reporting:
      enabled: true
      reports:
        - pipeline_summary
        - stage_report
        - sales_rep_report
        - trend_report
      
      schedule: "daily"
    
    analytics:
      enabled: true
      metrics:
        - conversion_rate
        - velocity
        - deal_size
        - win_rate
    
    insights:
      enabled: true
      alerts:
        - pipeline_health
        - stage_bottlenecks
        - at_risk_deals
        - forecast_variance
  
  sales_enablement:
    training:
      enabled: true
      modules:
        - product_training
        - sales_training
        - tools_training
      
      frequency: "quarterly"
    
    content:
      enabled: true
      types:
        - playbooks
        - templates
        - scripts
        - case_studies
    
    tools:
      enabled: true
      tools:
        - crm
        - forecasting
        - analytics
        - automation
    
    playbooks:
      enabled: true
      stages:
        - lead
        - qualified
        - proposal
        - negotiation
        - closed
```

---

## Code Examples

### Good: Complete Sales Operations Workflow

```python
# sales_operations/workflow.py
import asyncio
import logging
from typing import Dict, Any

from sales_operations.process import SalesProcessAutomator
from sales_operations.forecasting import SalesForecaster
from sales_operations.pipeline import PipelineManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_sales_operations():
    """Run sales operations workflow"""
    logger.info("=" * 60)
    logger.info("Sales Operations Automation Workflow")
    logger.info("=" * 60)
    
    # Load configuration
    config = load_config('config/sales_operations_config.yaml')
    
    # Step 1: Automate sales process
    logger.info("\n" + "=" * 60)
    logger.info("Step 1: Automating Sales Process")
    logger.info("=" * 60)
    
    process_automator = SalesProcessAutomator(config)
    
    lead_id = "lead_123"
    
    opportunity = await process_automator.automate_lead_to_opportunity(lead_id)
    
    logger.info(f"Opportunity created: {opportunity.opportunity_id}")
    print_opportunity_summary(opportunity)
    
    # Step 2: Forecast sales
    logger.info("\n" + "=" * 60)
    logger.info("Step 2: Forecasting Sales")
    logger.info("=" * 60)
    
    sales_forecaster = SalesForecaster(config)
    
    forecast = await sales_forecaster.forecast_sales(
        period="quarter",
        method="hybrid"
    )
    
    logger.info(f"Sales forecast: {forecast['total']}")
    print_forecast_summary(forecast)
    
    # Step 3: Manage pipeline
    logger.info("\n" + "=" * 60)
    logger.info("Step 3: Managing Pipeline")
    logger.info("=" * 60)
    
    pipeline_manager = PipelineManager(config)
    
    pipeline_results = await pipeline_manager.manage_pipeline()
    
    logger.info("Pipeline managed")
    print_pipeline_summary(pipeline_results)
    
    # Print summary
    print_summary(opportunity, forecast, pipeline_results)

def print_opportunity_summary(opportunity: Opportunity):
    """Print opportunity summary"""
    print(f"\nOpportunity Summary:")
    print(f"  ID: {opportunity.opportunity_id}")
    print(f"  Account: {opportunity.account_name}")
    print(f"  Amount: ${opportunity.amount:,.2f}")
    print(f"  Stage: {opportunity.stage.value}")
    print(f"  Probability: {opportunity.probability * 100:.0f}%")
    print(f"  Sales Rep: {opportunity.sales_rep}")

def print_forecast_summary(forecast: Dict[str, Any]):
    """Print forecast summary"""
    print(f"\nForecast Summary:")
    print(f"  Method: {forecast['method']}")
    print(f"  Period: {forecast['period']}")
    print(f"  Total: ${forecast['total']:,.2f}")
    print(f"  Confidence: {forecast['confidence'] * 100:.0f}%")
    if forecast['method'] == 'hybrid':
        print(f"  Pipeline: ${forecast['pipeline']:,.2f}")
        print(f"  Trend: ${forecast['trend']:,.2f}")
        print(f"  Seasonal: ${forecast['seasonal']:,.2f}")
        print(f"  ML: ${forecast['ml']:,.2f}")

def print_pipeline_summary(results: Dict[str, Any]):
    """Print pipeline summary"""
    tracking = results['tracking']
    print(f"\nPipeline Summary:")
    print(f"  Total Opportunities: {tracking['total_opportunities']}")
    print(f"  Total Pipeline: ${tracking['total_pipeline_value']:,.2f}")
    print(f"  Weighted Pipeline: ${tracking['weighted_pipeline_value']:,.2f}")

def print_summary(
    opportunity: Opportunity,
    forecast: Dict[str, Any],
    pipeline_results: Dict[str, Any]
):
    """Print summary"""
    print("\n" + "=" * 60)
    print("Sales Operations Summary")
    print("=" * 60)
    print(f"Opportunity ID: {opportunity.opportunity_id}")
    print(f"Opportunity Amount: ${opportunity.amount:,.2f}")
    print(f"Forecast: ${forecast['total']:,.2f}")
    print(f"Pipeline: ${pipeline_results['tracking']['total_pipeline_value']:,.2f}")

def load_config(filename: str) -> Dict[str, Any]:
    """Load configuration from file"""
    import yaml
    with open(filename, 'r') as f:
        return yaml.safe_load(f)

async def main():
    """Main entry point"""
    await run_sales_operations()

if __name__ == "__main__":
    asyncio.run(main())
```

### Bad: Anti-pattern Example

```python
# BAD: No process automation
def bad_sales_operations():
    # No process automation
    pass

# BAD: No forecasting
def bad_sales_operations():
    # No forecasting
    automate_process()

# BAD: No pipeline management
def bad_sales_operations():
    # No pipeline management
    automate_process()
    forecast_sales()

# BAD: No automation
def bad_sales_operations():
    # No automation
    automate_process()
    forecast_sales()
    manage_pipeline()
```

---

## Standards, Compliance & Security

### Industry Standards
- **Sales Operations**: Sales operations best practices
- **Forecasting**: Forecasting best practices
- **Pipeline Management**: Pipeline management best practices
- **Sales Enablement**: Sales enablement best practices
- **CRM**: CRM best practices

### Security Best Practices
- **Data Protection**: Protect sales data
- **Access Control**: RBAC for sales data
- **Audit Logging**: Log all sales activities
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

### 2. Configure Sales Operations

```bash
# Copy example config
cp config/sales_operations_config.yaml.example config/sales_operations_config.yaml

# Edit configuration
vim config/sales_operations_config.yaml
```

### 3. Run Sales Operations

```bash
python sales_operations/workflow.py
```

### 4. View Results

```bash
# View opportunities
cat sales_operations/results/opportunities.json

# View forecasts
cat sales_operations/results/forecasts.json

# View pipeline
cat sales_operations/results/pipeline.json
```

---

## Production Checklist

### Process Automation
- [ ] Lead to opportunity automation configured
- [ ] Stage transitions automated
- [ ] Quoting automation configured
- [ ] Contract automation configured
- [ ] Notifications configured
- [ ] Sales rep assignment configured

### Forecasting
- [ ] Pipeline forecasting configured
- [ ] Trend forecasting configured
- [ ] Seasonal forecasting configured
- [ ] ML forecasting configured
- [ ] Hybrid forecasting configured
- [ ] Forecast accuracy monitored

### Pipeline Management
- [ ] Pipeline tracking configured
- [ ] Pipeline reporting configured
- [ ] Pipeline analytics configured
- [ ] Pipeline insights configured
- [ ] Pipeline alerts configured
- [ ] Pipeline dashboards created

### Sales Enablement
- [ ] Training modules created
- [ ] Content library created
- [ ] Tools configured
- [ ] Playbooks created
- [ ] Sales rep onboarding configured
- [ ] Sales rep training scheduled

### Integration
- [ ] CRM integration configured
- [ ] Forecasting integration configured
- [ ] Analytics integration configured
- [ ] Notification integration configured
- [ ] Data synchronization configured
- [ ] API endpoints configured

---

## Anti-patterns

### ❌ Avoid These Practices

1. **No Process Automation**
   ```python
   # BAD: No process automation
   pass
   ```

2. **No Forecasting**
   ```python
   # BAD: No forecasting
   automate_process()
   ```

3. **No Pipeline Management**
   ```python
   # BAD: No pipeline management
   automate_process()
   forecast_sales()
   ```

4. **No Automation**
   ```python
   # BAD: No automation
   automate_process()
   forecast_sales()
   manage_pipeline()
   ```

### ✅ Follow These Practices

1. **Automate Process**
   ```python
   # GOOD: Automate process
   process_automator = SalesProcessAutomator(config)
   opportunity = await process_automator.automate_lead_to_opportunity(lead_id)
   ```

2. **Automate Forecasting**
   ```python
   # GOOD: Automate forecasting
   sales_forecaster = SalesForecaster(config)
   forecast = await sales_forecaster.forecast_sales(period, method)
   ```

3. **Automate Pipeline Management**
   ```python
   # GOOD: Automate pipeline management
   pipeline_manager = PipelineManager(config)
   results = await pipeline_manager.manage_pipeline()
   ```

4. **Automate Everything**
   ```python
   # GOOD: Automate everything
   process_automator = SalesProcessAutomator(config)
   sales_forecaster = SalesForecaster(config)
   pipeline_manager = PipelineManager(config)
   ```

---

## Unit Economics & KPIs

### Development Costs
- **Initial Setup**: 20-40 hours
- **Process Automation**: 20-40 hours
- **Forecasting**: 20-40 hours
- **Pipeline Management**: 20-40 hours
- **Total**: 80-160 hours

### Operational Costs
- **CRM Tools**: $100-500/month
- **Forecasting Tools**: $200-1000/month
- **Automation Tools**: $50-200/month
- **Analytics Tools**: $100-300/month

### ROI Metrics
- **Sales Efficiency**: 30-50% improvement
- **Forecast Accuracy**: 20-40% improvement
- **Pipeline Visibility**: 50-70% improvement
- **Revenue Growth**: 20-40% improvement

### KPI Targets
- **Forecast Accuracy**: > 90%
- **Pipeline Coverage**: > 3x
- **Sales Cycle Time**: < 90 days
- **Win Rate**: > 30%
- **Deal Size**: > $10,000
- **Sales Rep Productivity**: > 5 deals/month

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
- [Sales Operations Guide](https://www.salesforce.com/)
- [Sales Forecasting Guide](https://www.clari.com/)
- [Pipeline Management Guide](https://www.hubspot.com/)
- [Sales Enablement Guide](https://www.gong.io/)

### Best Practices
- [Sales Operations Framework](https://www.salesforce.com/)
- [Forecasting Best Practices](https://www.insightsquared.com/)
- [Pipeline Management](https://www.pipedrive.com/)
- [Sales Enablement](https://www.people.ai/)

### Tools & Libraries
- [Salesforce](https://www.salesforce.com/)
- [HubSpot](https://www.hubspot.com/)
- [Pipedrive](https://www.pipedrive.com/)
- [Clari](https://www.clari.com/)
- [InsightSquared](https://www.insightsquared.com/)
- [Aviso](https://www.aviso.com/)
- [People.ai](https://www.people.ai/)
- [Gong](https://www.gong.io/)
