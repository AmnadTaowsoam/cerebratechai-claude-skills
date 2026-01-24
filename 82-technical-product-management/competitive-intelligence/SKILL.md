---
name: Competitive Intelligence
description: Gathering, analyzing, and acting on competitive intelligence for strategic advantage
---

# Competitive Intelligence

## Current Level: Expert (Enterprise Scale)

## Domain: Technical Product Management
## Skill ID: 143

---

## Executive Summary

Competitive Intelligence enables systematic gathering, analysis, and action on competitive intelligence to gain strategic advantage. This capability is essential for understanding market dynamics, identifying competitive threats, finding differentiation opportunities, and making informed strategic decisions.

### Strategic Necessity

- **Market Awareness**: Understand competitive landscape
- **Strategic Advantage**: Identify differentiation opportunities
- **Threat Detection**: Identify and mitigate competitive threats
- **Innovation**: Learn from competitor innovations
- **Decision Making**: Make informed strategic decisions

---

## Technical Deep Dive

### Competitive Intelligence Framework

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Competitive Intelligence Framework                     │
│                                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│  │   Data       │    │   Analysis   │    │   Action     │                  │
│  │   Collection │───▶│   & Insight  │───▶│   Planning   │                  │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘                  │
│         │                   │                   │                           │
│         ▼                   ▼                   ▼                           │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Data Sources                                  │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Public   │  │  Social   │  │  Customer │  │  Internal │            │   │
│  │  │  Sources  │  │  Media    │  │  Feedback │  │  Sources  │            │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘            │   │
│  └───────┼────────────┼────────────┼────────────┼────────────────────┘   │
│          │            │            │            │                         │
│          ▼            ▼            ▼            ▼                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Analysis Methods                               │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Feature  │  │  Pricing  │  │  Market   │  │  SWOT      │            │   │
│  │  │  Analysis │  │  Analysis │  │  Analysis │  │  Analysis  │            │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘            │   │
│  └───────┼────────────┼────────────┼────────────┼────────────────────┘   │
│          │            │            │            │                         │
│          ▼            ▼            ▼            ▼                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Action Planning                               │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Strategy │  │  Product  │  │  Pricing  │  │  Marketing │            │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Data Collection

```python
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import asyncio
import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class DataSource(Enum):
    """Data source types"""
    PUBLIC = "public"
    SOCIAL_MEDIA = "social_media"
    CUSTOMER_FEEDBACK = "customer_feedback"
    INTERNAL = "internal"
    THIRD_PARTY = "third_party"

class Competitor:
    """Competitor definition"""
    def __init__(
        self,
        competitor_id: str,
        name: str,
        website: str,
        industry: str,
        size: str,
        founded_year: int
    ):
        self.competitor_id = competitor_id
        self.name = name
        self.website = website
        self.industry = industry
        self.size = size
        self.founded_year = founded_year
        self.features = []
        self.pricing = {}
        self.market_position = {}
        self.swot = {}

@dataclass
class CompetitiveData:
    """Competitive data item"""
    data_id: str
    source: DataSource
    competitor_id: str
    data_type: str
    content: Dict[str, Any]
    collected_at: str
    confidence: float

class CompetitiveIntelligenceCollector:
    """Competitive intelligence collection specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.public_collector = PublicDataCollector(config['public_data'])
        self.social_collector = SocialMediaCollector(config['social_media'])
        self.customer_collector = CustomerFeedbackCollector(config['customer_feedback'])
        self.internal_collector = InternalDataCollector(config['internal_data'])
        self.third_party_collector = ThirdPartyDataCollector(config['third_party'])
        self.data_store = CompetitiveDataStore(config['data_store'])
        
    async def collect_competitive_intelligence(
        self,
        competitors: List[Competitor],
        sources: List[DataSource] = None
    ) -> List[CompetitiveData]:
        """Collect competitive intelligence for competitors"""
        logger.info(f"Collecting competitive intelligence for {len(competitors)} competitors...")
        
        if sources is None:
            sources = [
                DataSource.PUBLIC,
                DataSource.SOCIAL_MEDIA,
                DataSource.CUSTOMER_FEEDBACK,
                DataSource.INTERNAL,
                DataSource.THIRD_PARTY
            ]
        
        all_data = []
        
        for competitor in competitors:
            logger.info(f"Collecting data for {competitor.name}...")
            
            # Collect from each source
            for source in sources:
                data = await self._collect_from_source(competitor, source)
                all_data.extend(data)
        
        # Store data
        await self.data_store.store_data(all_data)
        
        logger.info(f"Collected {len(all_data)} competitive data items")
        
        return all_data
    
    async def _collect_from_source(
        self,
        competitor: Competitor,
        source: DataSource
    ) -> List[CompetitiveData]:
        """Collect data from specific source"""
        if source == DataSource.PUBLIC:
            return await self.public_collector.collect(competitor)
        elif source == DataSource.SOCIAL_MEDIA:
            return await self.social_collector.collect(competitor)
        elif source == DataSource.CUSTOMER_FEEDBACK:
            return await self.customer_collector.collect(competitor)
        elif source == DataSource.INTERNAL:
            return await self.internal_collector.collect(competitor)
        elif source == DataSource.THIRD_PARTY:
            return await self.third_party_collector.collect(competitor)
        else:
            logger.warning(f"Unknown source: {source}")
            return []

class PublicDataCollector:
    """Public data collection specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def collect(
        self,
        competitor: Competitor
    ) -> List[CompetitiveData]:
        """Collect public data about competitor"""
        data_items = []
        
        # Collect website data
        website_data = await self._collect_website_data(competitor)
        data_items.extend(website_data)
        
        # Collect press releases
        press_data = await self._collect_press_releases(competitor)
        data_items.extend(press_data)
        
        # Collect job postings
        job_data = await self._collect_job_postings(competitor)
        data_items.extend(job_data)
        
        # Collect financial data
        financial_data = await self._collect_financial_data(competitor)
        data_items.extend(financial_data)
        
        return data_items
    
    async def _collect_website_data(
        self,
        competitor: Competitor
    ) -> List[CompetitiveData]:
        """Collect website data"""
        # Implementation would scrape competitor website
        # Extract features, pricing, messaging, etc.
        return []
    
    async def _collect_press_releases(
        self,
        competitor: Competitor
    ) -> List[CompetitiveData]:
        """Collect press releases"""
        # Implementation would search for press releases
        # Extract product announcements, partnerships, etc.
        return []
    
    async def _collect_job_postings(
        self,
        competitor: Competitor
    ) -> List[CompetitiveData]:
        """Collect job postings"""
        # Implementation would scrape job boards
        # Extract hiring trends, technology stack, etc.
        return []
    
    async def _collect_financial_data(
        self,
        competitor: Competitor
    ) -> List[CompetitiveData]:
        """Collect financial data"""
        # Implementation would collect from financial sources
        # Extract revenue, funding, valuation, etc.
        return []

class SocialMediaCollector:
    """Social media collection specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def collect(
        self,
        competitor: Competitor
    ) -> List[CompetitiveData]:
        """Collect social media data about competitor"""
        data_items = []
        
        # Collect Twitter data
        twitter_data = await self._collect_twitter_data(competitor)
        data_items.extend(twitter_data)
        
        # Collect LinkedIn data
        linkedin_data = await self._collect_linkedin_data(competitor)
        data_items.extend(linkedin_data)
        
        # Collect Facebook data
        facebook_data = await self._collect_facebook_data(competitor)
        data_items.extend(facebook_data)
        
        return data_items
    
    async def _collect_twitter_data(
        self,
        competitor: Competitor
    ) -> List[CompetitiveData]:
        """Collect Twitter data"""
        # Implementation would use Twitter API
        # Extract tweets, engagement, sentiment, etc.
        return []
    
    async def _collect_linkedin_data(
        self,
        competitor: Competitor
    ) -> List[CompetitiveData]:
        """Collect LinkedIn data"""
        # Implementation would use LinkedIn API
        # Extract company updates, employee count, etc.
        return []
    
    async def _collect_facebook_data(
        self,
        competitor: Competitor
    ) -> List[CompetitiveData]:
        """Collect Facebook data"""
        # Implementation would use Facebook API
        # Extract posts, engagement, ads, etc.
        return []

class CustomerFeedbackCollector:
    """Customer feedback collection specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def collect(
        self,
        competitor: Competitor
    ) -> List[CompetitiveData]:
        """Collect customer feedback about competitor"""
        data_items = []
        
        # Collect review data
        review_data = await self._collect_review_data(competitor)
        data_items.extend(review_data)
        
        # Collect forum data
        forum_data = await self._collect_forum_data(competitor)
        data_items.extend(forum_data)
        
        return data_items
    
    async def _collect_review_data(
        self,
        competitor: Competitor
    ) -> List[CompetitiveData]:
        """Collect review data"""
        # Implementation would collect from review sites
        # Extract ratings, reviews, complaints, etc.
        return []
    
    async def _collect_forum_data(
        self,
        competitor: Competitor
    ) -> List[CompetitiveData]:
        """Collect forum data"""
        # Implementation would collect from forums
        # Extract discussions, complaints, feature requests, etc.
        return []

class InternalDataCollector:
    """Internal data collection specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def collect(
        self,
        competitor: Competitor
    ) -> List[CompetitiveData]:
        """Collect internal data about competitor"""
        data_items = []
        
        # Collect sales data
        sales_data = await self._collect_sales_data(competitor)
        data_items.extend(sales_data)
        
        # Collect customer data
        customer_data = await self._collect_customer_data(competitor)
        data_items.extend(customer_data)
        
        # Collect partner data
        partner_data = await self._collect_partner_data(competitor)
        data_items.extend(partner_data)
        
        return data_items
    
    async def _collect_sales_data(
        self,
        competitor: Competitor
    ) -> List[CompetitiveData]:
        """Collect sales data"""
        # Implementation would query sales database
        # Extract win/loss data, objections, etc.
        return []
    
    async def _collect_customer_data(
        self,
        competitor: Competitor
    ) -> List[CompetitiveData]:
        """Collect customer data"""
        # Implementation would query customer database
        # Extract competitor usage, switching reasons, etc.
        return []
    
    async def _collect_partner_data(
        self,
        competitor: Competitor
    ) -> List[CompetitiveData]:
        """Collect partner data"""
        # Implementation would query partner database
        # Extract partner relationships, etc.
        return []

class ThirdPartyDataCollector:
    """Third-party data collection specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def collect(
        self,
        competitor: Competitor
    ) -> List[CompetitiveData]:
        """Collect third-party data about competitor"""
        data_items = []
        
        # Collect analyst reports
        analyst_data = await self._collect_analyst_reports(competitor)
        data_items.extend(analyst_data)
        
        # Collect market research
        market_data = await self._collect_market_research(competitor)
        data_items.extend(market_data)
        
        # Collect news articles
        news_data = await self._collect_news_articles(competitor)
        data_items.extend(news_data)
        
        return data_items
    
    async def _collect_analyst_reports(
        self,
        competitor: Competitor
    ) -> List[CompetitiveData]:
        """Collect analyst reports"""
        # Implementation would collect from analyst firms
        # Extract market position, strengths, weaknesses, etc.
        return []
    
    async def _collect_market_research(
        self,
        competitor: Competitor
    ) -> List[CompetitiveData]:
        """Collect market research"""
        # Implementation would collect from market research firms
        # Extract market share, growth, trends, etc.
        return []
    
    async def _collect_news_articles(
        self,
        competitor: Competitor
    ) -> List[CompetitiveData]:
        """Collect news articles"""
        # Implementation would collect from news sources
        # Extract recent news, announcements, etc.
        return []

class CompetitiveDataStore:
    """Competitive data storage specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def store_data(self, data: List[CompetitiveData]):
        """Store competitive data"""
        # Implementation would store in database
        pass
    
    async def get_data(
        self,
        competitor_id: str,
        data_type: Optional[str] = None
    ) -> List[CompetitiveData]:
        """Get competitive data"""
        # Implementation would query database
        return []
    
    async def get_latest_data(
        self,
        competitor_id: str,
        days: int = 30
    ) -> List[CompetitiveData]:
        """Get latest competitive data"""
        # Implementation would query database
        return []
```

### Analysis & Insight

```python
class CompetitiveAnalyzer:
    """Competitive analysis specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.data_store = CompetitiveDataStore(config['data_store'])
        
    async def analyze_competitor(
        self,
        competitor: Competitor
    ) -> Dict[str, Any]:
        """Analyze competitor"""
        logger.info(f"Analyzing competitor: {competitor.name}")
        
        # Collect data
        data = await self.data_store.get_data(competitor.competitor_id)
        
        # Analyze features
        feature_analysis = await self._analyze_features(data)
        
        # Analyze pricing
        pricing_analysis = await self._analyze_pricing(data)
        
        # Analyze market position
        market_analysis = await self._analyze_market_position(data)
        
        # Analyze SWOT
        swot_analysis = await self._analyze_swot(data)
        
        # Compile analysis
        analysis = {
            'competitor_id': competitor.competitor_id,
            'name': competitor.name,
            'features': feature_analysis,
            'pricing': pricing_analysis,
            'market_position': market_analysis,
            'swot': swot_analysis,
            'analyzed_at': datetime.utcnow().isoformat()
        }
        
        return analysis
    
    async def _analyze_features(
        self,
        data: List[CompetitiveData]
    ) -> Dict[str, Any]:
        """Analyze competitor features"""
        features = {
            'core_features': [],
            'unique_features': [],
            'missing_features': [],
            'feature_quality': {}
        }
        
        # Extract features from data
        for item in data:
            if item.data_type == 'feature':
                feature_data = item.content
                
                # Categorize features
                if feature_data.get('is_core', False):
                    features['core_features'].append(feature_data)
                elif feature_data.get('is_unique', False):
                    features['unique_features'].append(feature_data)
                
                # Assess quality
                features['feature_quality'][feature_data['name']] = {
                    'quality': feature_data.get('quality', 0),
                    'user_satisfaction': feature_data.get('user_satisfaction', 0)
                }
        
        return features
    
    async def _analyze_pricing(
        self,
        data: List[CompetitiveData]
    ) -> Dict[str, Any]:
        """Analyze competitor pricing"""
        pricing = {
            'plans': [],
            'pricing_strategy': '',
            'price_comparison': {}
        }
        
        # Extract pricing from data
        for item in data:
            if item.data_type == 'pricing':
                pricing_data = item.content
                
                # Add plan
                pricing['plans'].append({
                    'name': pricing_data['name'],
                    'price': pricing_data['price'],
                    'features': pricing_data.get('features', [])
                })
        
        # Determine pricing strategy
        if len(pricing['plans']) > 0:
            prices = [p['price'] for p in pricing['plans']]
            avg_price = sum(prices) / len(prices)
            
            if avg_price < 50:
                pricing['pricing_strategy'] = 'low_cost'
            elif avg_price < 200:
                pricing['pricing_strategy'] = 'mid_market'
            else:
                pricing['pricing_strategy'] = 'premium'
        
        return pricing
    
    async def _analyze_market_position(
        self,
        data: List[CompetitiveData]
    ) -> Dict[str, Any]:
        """Analyze competitor market position"""
        position = {
            'market_share': 0.0,
            'growth_rate': 0.0,
            'customer_satisfaction': 0.0,
            'brand_strength': 0.0
        }
        
        # Extract market data from data
        for item in data:
            if item.data_type == 'market':
                market_data = item.content
                
                # Update position metrics
                position['market_share'] = market_data.get('market_share', 0.0)
                position['growth_rate'] = market_data.get('growth_rate', 0.0)
                position['customer_satisfaction'] = market_data.get('customer_satisfaction', 0.0)
                position['brand_strength'] = market_data.get('brand_strength', 0.0)
        
        return position
    
    async def _analyze_swot(
        self,
        data: List[CompetitiveData]
    ) -> Dict[str, Any]:
        """Analyze SWOT"""
        swot = {
            'strengths': [],
            'weaknesses': [],
            'opportunities': [],
            'threats': []
        }
        
        # Extract SWOT from data
        for item in data:
            if item.data_type == 'swot':
                swot_data = item.content
                
                # Add to SWOT
                swot['strengths'].extend(swot_data.get('strengths', []))
                swot['weaknesses'].extend(swot_data.get('weaknesses', []))
                swot['opportunities'].extend(swot_data.get('opportunities', []))
                swot['threats'].extend(swot_data.get('threats', []))
        
        return swot
    
    async def compare_competitors(
        self,
        competitors: List[Competitor]
    ) -> Dict[str, Any]:
        """Compare multiple competitors"""
        logger.info(f"Comparing {len(competitors)} competitors...")
        
        # Analyze each competitor
        analyses = {}
        for competitor in competitors:
            analysis = await self.analyze_competitor(competitor)
            analyses[competitor.competitor_id] = analysis
        
        # Compare features
        feature_comparison = self._compare_features(analyses)
        
        # Compare pricing
        pricing_comparison = self._compare_pricing(analyses)
        
        # Compare market position
        market_comparison = self._compare_market_position(analyses)
        
        # Compile comparison
        comparison = {
            'competitors': analyses,
            'feature_comparison': feature_comparison,
            'pricing_comparison': pricing_comparison,
            'market_comparison': market_comparison,
            'compared_at': datetime.utcnow().isoformat()
        }
        
        return comparison
    
    def _compare_features(
        self,
        analyses: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compare features across competitors"""
        comparison = {
            'common_features': [],
            'unique_features': {},
            'feature_matrix': {}
        }
        
        # Get all features
        all_features = set()
        feature_map = {}
        
        for competitor_id, analysis in analyses.items():
            features = analysis['features']['core_features']
            feature_names = [f['name'] for f in features]
            
            for name in feature_names:
                all_features.add(name)
                
                if name not in feature_map:
                    feature_map[name] = []
                
                feature_map[name].append(competitor_id)
        
        # Identify common features
        for feature_name, competitors in feature_map.items():
            if len(competitors) == len(analyses):
                comparison['common_features'].append(feature_name)
            else:
                comparison['unique_features'][feature_name] = competitors
        
        # Build feature matrix
        for feature_name in all_features:
            comparison['feature_matrix'][feature_name] = {}
            
            for competitor_id in analyses.keys():
                has_feature = feature_name in feature_map and competitor_id in feature_map[feature_name]
                comparison['feature_matrix'][feature_name][competitor_id] = has_feature
        
        return comparison
    
    def _compare_pricing(
        self,
        analyses: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compare pricing across competitors"""
        comparison = {
            'price_ranges': {},
            'pricing_strategies': {},
            'best_value': None
        }
        
        # Get pricing for each competitor
        for competitor_id, analysis in analyses.items():
            pricing = analysis['pricing']
            plans = pricing['plans']
            
            if len(plans) > 0:
                prices = [p['price'] for p in plans]
                comparison['price_ranges'][competitor_id] = {
                    'min': min(prices),
                    'max': max(prices),
                    'avg': sum(prices) / len(prices)
                }
                comparison['pricing_strategies'][competitor_id] = pricing['pricing_strategy']
        
        # Identify best value
        if comparison['price_ranges']:
            # Find lowest average price
            best_value = min(
                comparison['price_ranges'].items(),
                key=lambda x: x[1]['avg']
            )
            comparison['best_value'] = best_value[0]
        
        return comparison
    
    def _compare_market_position(
        self,
        analyses: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compare market position across competitors"""
        comparison = {
            'market_share': {},
            'growth_rate': {},
            'customer_satisfaction': {},
            'brand_strength': {},
            'rankings': {}
        }
        
        # Get market position for each competitor
        for competitor_id, analysis in analyses.items():
            position = analysis['market_position']
            
            comparison['market_share'][competitor_id] = position['market_share']
            comparison['growth_rate'][competitor_id] = position['growth_rate']
            comparison['customer_satisfaction'][competitor_id] = position['customer_satisfaction']
            comparison['brand_strength'][competitor_id] = position['brand_strength']
        
        # Calculate rankings
        comparison['rankings']['market_share'] = self._calculate_rankings(comparison['market_share'])
        comparison['rankings']['growth_rate'] = self._calculate_rankings(comparison['growth_rate'])
        comparison['rankings']['customer_satisfaction'] = self._calculate_rankings(comparison['customer_satisfaction'])
        comparison['rankings']['brand_strength'] = self._calculate_rankings(comparison['brand_strength'])
        
        return comparison
    
    def _calculate_rankings(
        self,
        metrics: Dict[str, float]
    ) -> Dict[str, int]:
        """Calculate rankings from metrics"""
        # Sort by value descending
        sorted_metrics = sorted(metrics.items(), key=lambda x: x[1], reverse=True)
        
        # Assign rankings
        rankings = {}
        for rank, (competitor_id, _) in enumerate(sorted_metrics, 1):
            rankings[competitor_id] = rank
        
        return rankings
```

### Action Planning

```python
class ActionPlanner:
    """Action planning specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def create_action_plan(
        self,
        comparison: Dict[str, Any],
        our_company_id: str
    ) -> Dict[str, Any]:
        """Create action plan from competitive analysis"""
        logger.info("Creating action plan...")
        
        # Identify opportunities
        opportunities = self._identify_opportunities(comparison, our_company_id)
        
        # Identify threats
        threats = self._identify_threats(comparison, our_company_id)
        
        # Create strategic actions
        strategic_actions = self._create_strategic_actions(opportunities, threats)
        
        # Create product actions
        product_actions = self._create_product_actions(comparison, our_company_id)
        
        # Create pricing actions
        pricing_actions = self._create_pricing_actions(comparison, our_company_id)
        
        # Create marketing actions
        marketing_actions = self._create_marketing_actions(comparison, our_company_id)
        
        # Compile action plan
        action_plan = {
            'opportunities': opportunities,
            'threats': threats,
            'strategic_actions': strategic_actions,
            'product_actions': product_actions,
            'pricing_actions': pricing_actions,
            'marketing_actions': marketing_actions,
            'created_at': datetime.utcnow().isoformat()
        }
        
        return action_plan
    
    def _identify_opportunities(
        self,
        comparison: Dict[str, Any],
        our_company_id: str
    ) -> List[Dict[str, Any]]:
        """Identify opportunities from competitive analysis"""
        opportunities = []
        
        # Feature gaps
        feature_comparison = comparison['feature_comparison']
        
        # Identify features we have that competitors don't
        for feature_name, competitors in feature_comparison['unique_features'].items():
            if our_company_id in competitors:
                opportunities.append({
                    'type': 'feature_advantage',
                    'description': f"We have {feature_name} which competitors don't",
                    'impact': 'high',
                    'action': 'Highlight in marketing'
                })
        
        # Identify features competitors have that we don't
        for feature_name, competitors in feature_comparison['unique_features'].items():
            if our_company_id not in competitors:
                opportunities.append({
                    'type': 'feature_gap',
                    'description': f"Competitors have {feature_name} which we don't",
                    'impact': 'medium',
                    'action': 'Consider adding this feature'
                })
        
        # Pricing opportunities
        pricing_comparison = comparison['pricing_comparison']
        
        # If we're not the best value
        if pricing_comparison['best_value'] != our_company_id:
            opportunities.append({
                'type': 'pricing_opportunity',
                'description': 'Competitors offer better value',
                'impact': 'high',
                'action': 'Consider pricing adjustment or value add'
            })
        
        return opportunities
    
    def _identify_threats(
        self,
        comparison: Dict[str, Any],
        our_company_id: str
    ) -> List[Dict[str, Any]]:
        """Identify threats from competitive analysis"""
        threats = []
        
        # Market position threats
        market_comparison = comparison['market_comparison']
        
        # If we're not #1 in market share
        if market_comparison['rankings']['market_share'].get(our_company_id, 0) > 1:
            threats.append({
                'type': 'market_share_threat',
                'description': 'Competitors have larger market share',
                'impact': 'high',
                'action': 'Increase marketing and sales efforts'
            })
        
        # If competitors are growing faster
        our_growth = market_comparison['growth_rate'].get(our_company_id, 0)
        for competitor_id, growth_rate in market_comparison['growth_rate'].items():
            if competitor_id != our_company_id and growth_rate > our_growth:
                threats.append({
                    'type': 'growth_threat',
                    'description': f'{competitor_id} is growing faster',
                    'impact': 'medium',
                    'action': 'Analyze and replicate success factors'
                })
        
        return threats
    
    def _create_strategic_actions(
        self,
        opportunities: List[Dict[str, Any]],
        threats: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Create strategic actions"""
        actions = []
        
        # Prioritize high impact opportunities
        high_impact_opportunities = [o for o in opportunities if o['impact'] == 'high']
        
        for opportunity in high_impact_opportunities:
            actions.append({
                'type': 'opportunity',
                'description': opportunity['description'],
                'priority': 'high',
                'action': opportunity['action'],
                'owner': 'Product Strategy',
                'timeline': '3 months'
            })
        
        # Prioritize high impact threats
        high_impact_threats = [t for t in threats if t['impact'] == 'high']
        
        for threat in high_impact_threats:
            actions.append({
                'type': 'threat',
                'description': threat['description'],
                'priority': 'high',
                'action': threat['action'],
                'owner': 'Product Strategy',
                'timeline': '3 months'
            })
        
        return actions
    
    def _create_product_actions(
        self,
        comparison: Dict[str, Any],
        our_company_id: str
    ) -> List[Dict[str, Any]]:
        """Create product actions"""
        actions = []
        
        # Feature gap actions
        feature_comparison = comparison['feature_comparison']
        
        for feature_name, competitors in feature_comparison['unique_features'].items():
            if our_company_id not in competitors:
                actions.append({
                    'type': 'feature_add',
                    'description': f"Add {feature_name} feature",
                    'priority': 'medium',
                    'owner': 'Product Team',
                    'timeline': '6 months'
                })
        
        return actions
    
    def _create_pricing_actions(
        self,
        comparison: Dict[str, Any],
        our_company_id: str
    ) -> List[Dict[str, Any]]:
        """Create pricing actions"""
        actions = []
        
        # Pricing adjustment actions
        pricing_comparison = comparison['pricing_comparison']
        
        if pricing_comparison['best_value'] != our_company_id:
            actions.append({
                'type': 'pricing_review',
                'description': 'Review and adjust pricing',
                'priority': 'high',
                'owner': 'Product Team',
                'timeline': '1 month'
            })
        
        return actions
    
    def _create_marketing_actions(
        self,
        comparison: Dict[str, Any],
        our_company_id: str
    ) -> List[Dict[str, Any]]:
        """Create marketing actions"""
        actions = []
        
        # Feature advantage actions
        feature_comparison = comparison['feature_comparison']
        
        for feature_name, competitors in feature_comparison['unique_features'].items():
            if our_company_id in competitors:
                actions.append({
                    'type': 'marketing_highlight',
                    'description': f"Highlight {feature_name} in marketing",
                    'priority': 'medium',
                    'owner': 'Marketing Team',
                    'timeline': '1 month'
                })
        
        return actions
```

---

## Tooling & Tech Stack

### Data Collection Tools
- **BeautifulSoup**: Web scraping
- **Scrapy**: Web scraping framework
- **Selenium**: Browser automation
- **Puppeteer**: Browser automation
- **Twitter API**: Social media data

### Analysis Tools
- **Pandas**: Data analysis
- **NumPy**: Numerical computing
- **Scikit-learn**: Machine learning
- **NLTK**: Natural language processing
- **SpaCy**: Natural language processing

### Visualization Tools
- **Matplotlib**: Data visualization
- **Plotly**: Interactive charts
- **Tableau**: Business intelligence
- **Power BI**: Business intelligence
- **Grafana**: Visualization

### Storage Tools
- **PostgreSQL**: Database
- **MongoDB**: Document database
- **Elasticsearch**: Search and analytics
- **Redis**: Cache

---

## Configuration Essentials

### Competitive Intelligence Configuration

```yaml
# config/competitive_intelligence_config.yaml
competitive_intelligence:
  competitors:
    - name: "Competitor A"
      website: "https://competitor-a.com"
      industry: "Technology"
      size: "Enterprise"
      founded_year: 2010
    
    - name: "Competitor B"
      website: "https://competitor-b.com"
      industry: "Technology"
      size: "Mid-Market"
      founded_year: 2015

  data_collection:
    sources:
      - public
      - social_media
      - customer_feedback
      - internal
      - third_party
    
    frequency:
      public: "daily"
      social_media: "daily"
      customer_feedback: "weekly"
      internal: "weekly"
      third_party: "monthly"
    
    retention:
      public: 365  # days
      social_media: 30  # days
      customer_feedback: 365  # days
      internal: 365  # days
      third_party: 365  # days

  analysis:
    feature_analysis:
      enabled: true
      quality_threshold: 0.7
    
    pricing_analysis:
      enabled: true
      comparison_method: "value_based"
    
    market_analysis:
      enabled: true
      metrics:
        - market_share
        - growth_rate
        - customer_satisfaction
        - brand_strength

  action_planning:
    opportunities:
      enabled: true
      priority_threshold: "medium"
    
    threats:
      enabled: true
      priority_threshold: "high"
    
    actions:
      auto_create: true
      assign_owners: true
      set_timelines: true
```

---

## Code Examples

### Good: Complete Competitive Intelligence Workflow

```python
# competitive_intelligence/workflow.py
import asyncio
import logging
from typing import Dict, Any

from competitive_intelligence.collector import CompetitiveIntelligenceCollector
from competitive_intelligence.analyzer import CompetitiveAnalyzer
from competitive_intelligence.planner import ActionPlanner

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_competitive_intelligence():
    """Run competitive intelligence workflow"""
    logger.info("=" * 60)
    logger.info("Competitive Intelligence Workflow")
    logger.info("=" * 60)
    
    # Load configuration
    config = load_config('config/competitive_intelligence_config.yaml')
    
    # Define competitors
    competitors = define_competitors(config)
    
    # Step 1: Collect competitive intelligence
    logger.info("\n" + "=" * 60)
    logger.info("Step 1: Collecting Competitive Intelligence")
    logger.info("=" * 60)
    
    collector = CompetitiveIntelligenceCollector(config)
    competitive_data = await collector.collect_competitive_intelligence(competitors)
    
    logger.info(f"Collected {len(competitive_data)} data items")
    
    # Step 2: Analyze competitors
    logger.info("\n" + "=" * 60)
    logger.info("Step 2: Analyzing Competitors")
    logger.info("=" * 60)
    
    analyzer = CompetitiveAnalyzer(config)
    
    # Analyze individual competitors
    for competitor in competitors:
        analysis = await analyzer.analyze_competitor(competitor)
        logger.info(f"Analyzed {competitor.name}")
        print_competitor_analysis(analysis)
    
    # Step 3: Compare competitors
    logger.info("\n" + "=" * 60)
    logger.info("Step 3: Comparing Competitors")
    logger.info("=" * 60)
    
    comparison = await analyzer.compare_competitors(competitors)
    
    logger.info(f"Compared {len(competitors)} competitors")
    print_competitor_comparison(comparison)
    
    # Step 4: Create action plan
    logger.info("\n" + "=" * 60)
    logger.info("Step 4: Creating Action Plan")
    logger.info("=" * 60)
    
    planner = ActionPlanner(config)
    our_company_id = "our_company"
    
    action_plan = await planner.create_action_plan(comparison, our_company_id)
    
    logger.info(f"Action plan created")
    print_action_plan(action_plan)
    
    # Print summary
    print_summary(competitors, competitive_data, comparison, action_plan)

def define_competitors(config: Dict[str, Any]) -> List[Competitor]:
    """Define competitors from config"""
    competitors = []
    
    for i, comp_config in enumerate(config['competitive_intelligence']['competitors']):
        competitor = Competitor(
            competitor_id=f"competitor_{i+1}",
            name=comp_config['name'],
            website=comp_config['website'],
            industry=comp_config['industry'],
            size=comp_config['size'],
            founded_year=comp_config['founded_year']
        )
        competitors.append(competitor)
    
    return competitors

def print_competitor_analysis(analysis: Dict[str, Any]):
    """Print competitor analysis"""
    print(f"\nCompetitor: {analysis['name']}")
    print(f"  Features: {len(analysis['features']['core_features'])} core, "
          f"{len(analysis['features']['unique_features'])} unique")
    print(f"  Pricing: {analysis['pricing']['pricing_strategy']}")
    print(f"  Market Share: {analysis['market_position']['market_share']:.1%}")
    print(f"  Growth Rate: {analysis['market_position']['growth_rate']:.1%}")

def print_competitor_comparison(comparison: Dict[str, Any]):
    """Print competitor comparison"""
    print(f"\nCompetitor Comparison:")
    print(f"  Common Features: {len(comparison['feature_comparison']['common_features'])}")
    print(f"  Unique Features: {len(comparison['feature_comparison']['unique_features'])}")
    print(f"  Best Value: {comparison['pricing_comparison']['best_value']}")
    print(f"\n  Rankings:")
    rankings = comparison['market_comparison']['rankings']
    print(f"    Market Share: {rankings['market_share']}")
    print(f"    Growth Rate: {rankings['growth_rate']}")
    print(f"    Customer Satisfaction: {rankings['customer_satisfaction']}")

def print_action_plan(action_plan: Dict[str, Any]):
    """Print action plan"""
    print(f"\nAction Plan:")
    print(f"  Opportunities: {len(action_plan['opportunities'])}")
    print(f"  Threats: {len(action_plan['threats'])}")
    print(f"\n  Strategic Actions: {len(action_plan['strategic_actions'])}")
    for action in action_plan['strategic_actions'][:5]:
        print(f"    - {action['description']} ({action['priority']})")
    print(f"\n  Product Actions: {len(action_plan['product_actions'])}")
    for action in action_plan['product_actions'][:5]:
        print(f"    - {action['description']}")
    print(f"\n  Pricing Actions: {len(action_plan['pricing_actions'])}")
    for action in action_plan['pricing_actions']:
        print(f"    - {action['description']}")
    print(f"\n  Marketing Actions: {len(action_plan['marketing_actions'])}")
    for action in action_plan['marketing_actions'][:5]:
        print(f"    - {action['description']}")

def print_summary(
    competitors: list,
    competitive_data: list,
    comparison: Dict[str, Any],
    action_plan: Dict[str, Any]
):
    """Print summary"""
    print("\n" + "=" * 60)
    print("Competitive Intelligence Summary")
    print("=" * 60)
    print(f"Competitors Analyzed: {len(competitors)}")
    print(f"Data Collected: {len(competitive_data)} items")
    print(f"\nAction Plan:")
    print(f"  Opportunities: {len(action_plan['opportunities'])}")
    print(f"  Threats: {len(action_plan['threats'])}")
    print(f"  Strategic Actions: {len(action_plan['strategic_actions'])}")
    print(f"  Product Actions: {len(action_plan['product_actions'])}")
    print(f"  Pricing Actions: {len(action_plan['pricing_actions'])}")
    print(f"  Marketing Actions: {len(action_plan['marketing_actions'])}")

def load_config(filename: str) -> Dict[str, Any]:
    """Load configuration from file"""
    import yaml
    with open(filename, 'r') as f:
        return yaml.safe_load(f)

async def main():
    """Main entry point"""
    await run_competitive_intelligence()

if __name__ == "__main__":
    asyncio.run(main())
```

### Bad: Anti-pattern Example

```python
# BAD: No data collection
def bad_competitive_intelligence():
    # No data collection
    guess_competitors()

# BAD: No analysis
def bad_competitive_intelligence():
    # No analysis
    collect_data()

# BAD: No action planning
def bad_competitive_intelligence():
    # No action planning
    analyze_data()

# BAD: No monitoring
def bad_competitive_intelligence():
    # No monitoring
    analyze_once()

# BAD: No automation
def bad_competitive_intelligence():
    # No automation
    manual_collection()
```

---

## Standards, Compliance & Security

### Industry Standards
- **Market Research**: Market research best practices
- **Data Collection**: Ethical data collection
- **Privacy**: Data privacy regulations
- **Competitive Intelligence**: Competitive intelligence ethics

### Security Best Practices
- **Data Encryption**: Encrypt all collected data
- **Access Control**: RBAC for competitive data
- **Audit Logging**: Log all data collection activities
- **Data Retention**: Follow data retention policies

### Compliance Requirements
- **GDPR**: Data protection compliance
- **CCPA**: California Consumer Privacy Act
- **Terms of Service**: Respect competitor ToS
- **Ethical Guidelines**: Follow ethical guidelines

---

## Quick Start

### 1. Install Dependencies

```bash
pip install pyyaml
pip install beautifulsoup4
pip install pandas
```

### 2. Configure Competitive Intelligence

```bash
# Copy example config
cp config/competitive_intelligence_config.yaml.example config/competitive_intelligence_config.yaml

# Edit configuration
vim config/competitive_intelligence_config.yaml
```

### 3. Run Competitive Intelligence

```bash
python competitive_intelligence/workflow.py
```

### 4. View Results

```bash
# View competitive data
cat competitive_intelligence/results/competitive_data.json

# View action plan
cat competitive_intelligence/results/action_plan.json
```

---

## Production Checklist

### Data Collection
- [ ] Competitors defined
- [ ] Data sources configured
- [ ] Collection scheduled
- [ ] Data validation implemented
- [ ] Error handling implemented

### Analysis
- [ ] Analysis framework configured
- [ ] Metrics defined
- [ ] Thresholds configured
- [ ] Automated analysis implemented
- [ ] Results validated

### Action Planning
- [ ] Opportunities identified
- [ ] Threats identified
- [ ] Actions created
- [ ] Owners assigned
- [ ] Timelines set

### Monitoring
- [ ] Monitoring configured
- [ ] Alerts configured
- [ ] Reports scheduled
- [ ] Review meetings scheduled
- [ ] Continuous improvement

### Compliance
- [ ] Privacy policy reviewed
- [ ] Terms of service reviewed
- [ ] Data retention policies defined
- [ ] Audit logging enabled
- [ ] Ethical guidelines followed

---

## Anti-patterns

### ❌ Avoid These Practices

1. **No Data Collection**
   ```python
   # BAD: No data collection
   guess_competitors()
   ```

2. **No Analysis**
   ```python
   # BAD: No analysis
   collect_data()
   ```

3. **No Action Planning**
   ```python
   # BAD: No action planning
   analyze_data()
   ```

4. **No Monitoring**
   ```python
   # BAD: No monitoring
   analyze_once()
   ```

5. **No Automation**
   ```python
   # BAD: No automation
   manual_collection()
   ```

### ✅ Follow These Practices

1. **Systematic Collection**
   ```python
   # GOOD: Systematic collection
   collector = CompetitiveIntelligenceCollector(config)
   data = await collector.collect_competitive_intelligence(competitors)
   ```

2. **Data-Driven Analysis**
   ```python
   # GOOD: Data-driven analysis
   analyzer = CompetitiveAnalyzer(config)
   analysis = await analyzer.analyze_competitor(competitor)
   ```

3. **Action Planning**
   ```python
   # GOOD: Action planning
   planner = ActionPlanner(config)
   action_plan = await planner.create_action_plan(comparison, our_company_id)
   ```

4. **Continuous Monitoring**
   ```python
   # GOOD: Continuous monitoring
   while True:
       data = await collect_competitive_intelligence()
       analysis = await analyze(data)
       action_plan = await create_actions(analysis)
       await sleep(24 * 3600)  # Daily
   ```

5. **Automation**
   ```python
   # GOOD: Automation
   scheduler.schedule_daily(collect_competitive_intelligence)
   ```

---

## Unit Economics & KPIs

### Development Costs
- **Initial Setup**: 20-40 hours
- **Data Collection**: 40-80 hours
- **Analysis**: 20-40 hours
- **Action Planning**: 20-40 hours
- **Total**: 100-200 hours

### Operational Costs
- **Data Sources**: $100-500/month
- **Analysis Tools**: $50-200/month
- **Monitoring Tools**: $50-100/month
- **Review Time**: 10-20 hours/month

### ROI Metrics
- **Strategic Decisions**: 60-80% improvement
- **Market Awareness**: 70-90% improvement
- **Competitive Advantage**: 50-70% improvement
- **Time-to-Response**: 70-90% faster

### KPI Targets
- **Data Collection Rate**: > 95%
- **Analysis Accuracy**: > 85%
- **Action Completion Rate**: > 70%
- **Response Time**: < 48 hours
- **Market Awareness**: > 90%

---

## Integration Points / Related Skills

### Upstream Skills
- **136. Business to Technical Spec**: Requirements
- **137. API-First Product Strategy**: API design
- **138. Platform Product Design**: Platform design
- **139. Product Discovery Validation**: Validation

### Parallel Skills
- **140. Product Analytics Implementation**: Analytics
- **141. Feature Prioritization**: Prioritization
- **142. Technical Debt Prioritization**: Debt management

### Downstream Skills
- **144. Product Roadmap Communication**: Roadmap
- **145. Cross-Functional Leadership**: Leadership

### Cross-Domain Skills
- **18. Project Management**: Project planning
- **81. SaaS FinOps Pricing**: Pricing strategy
- **83. Go-to-Market Tech**: Go-to-market
- **84. Compliance AI Governance**: Compliance

---

## References & Resources

### Documentation
- [Competitive Intelligence Guide](https://www.scip.org/)
- [Market Research Best Practices](https://www.esomar.org/)
- [Data Collection Ethics](https://www.ama.org/)

### Best Practices
- [Competitive Intelligence Best Practices](https://www.forrester.com/)
- [Market Research Guide](https://www.mra-net.org/)
- [Strategic Planning](https://www.strategyzer.com/)

### Tools & Libraries
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [Scrapy](https://scrapy.org/)
- [Pandas](https://pandas.pydata.org/)
- [Tableau](https://www.tableau.com/)
- [Power BI](https://powerbi.microsoft.com/)
