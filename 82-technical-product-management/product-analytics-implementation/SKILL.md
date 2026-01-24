---
name: Product Analytics Implementation
description: Implementing product analytics, metrics, and dashboards for data-driven product decisions
---

# Product Analytics Implementation

## Current Level: Expert (Enterprise Scale)

## Domain: Technical Product Management
## Skill ID: 140

---

## Executive Summary

Product Analytics Implementation enables systematic tracking, measurement, and analysis of product usage data to drive data-driven product decisions. This capability is essential for understanding user behavior, measuring feature adoption, optimizing conversion funnels, and identifying growth opportunities.

### Strategic Necessity

- **Data-Driven Decisions**: Make decisions based on real data
- **User Insight**: Understand user behavior and preferences
- **Feature Optimization**: Measure and improve feature adoption
- **Growth Optimization**: Identify and capitalize on growth opportunities
- **Performance Monitoring**: Track product KPIs and metrics

---

## Technical Deep Dive

### Analytics Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Product Analytics Architecture                         │
│                                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│  │   Data       │    │   Event      │    │   User       │                  │
│  │   Collection │───▶│   Tracking   │───▶│   Identity   │                  │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘                  │
│         │                   │                   │                           │
│         ▼                   ▼                   ▼                           │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Analytics Pipeline                              │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Ingest   │  │  Process  │  │  Store    │  │  Index    │            │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘            │   │
│  └───────┼────────────┼────────────┼────────────┼────────────────────┘   │
│          │            │            │            │                         │
│          ▼            ▼            ▼            ▼                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Analytics Engine                                │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Query    │  │  Aggregate │  │  Segment  │  │  Funnel   │            │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘            │   │
│  └───────┼────────────┼────────────┼────────────┼────────────────────┘   │
│          │            │            │            │                         │
│          ▼            ▼            ▼            ▼                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Visualization Layer                            │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Dashboards│  │  Reports  │  │  Alerts   │  │  Exports  │            │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Event Tracking

```python
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import asyncio
import logging
from datetime import datetime
from dataclasses_json import dataclass_json

logger = logging.getLogger(__name__)

class EventType(Enum):
    """Event types"""
    PAGE_VIEW = "page_view"
    CLICK = "click"
    SUBMIT = "submit"
    SIGN_UP = "sign_up"
    SIGN_IN = "sign_in"
    SIGN_OUT = "sign_out"
    FEATURE_USED = "feature_used"
    PURCHASE = "purchase"
    ERROR = "error"
    CUSTOM = "custom"

@dataclass_json
@dataclass
class Event:
    """Analytics event"""
    event_id: str
    event_type: str
    user_id: str
    session_id: str
    properties: Dict[str, Any]
    timestamp: str
    device: Dict[str, Any]
    location: Dict[str, Any]
    context: Dict[str, Any]

@dataclass
class UserSession:
    """User session"""
    session_id: str
    user_id: str
    start_time: str
    end_time: Optional[str]
    events: List[Event]
    properties: Dict[str, Any]

class EventTracker:
    """Event tracking specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.event_queue = asyncio.Queue()
        self.batch_size = config.get('batch_size', 100)
        self.flush_interval = config.get('flush_interval', 5)  # seconds
        self.storage = EventStorage(config['storage'])
        self.identity_resolver = IdentityResolver(config['identity'])
        
        # Start background flush task
        asyncio.create_task(self._flush_events())
    
    async def track_event(
        self,
        event_type: EventType,
        user_id: str,
        properties: Dict[str, Any],
        session_id: Optional[str] = None,
        device: Optional[Dict[str, Any]] = None,
        location: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Track analytics event"""
        logger.debug(f"Tracking event: {event_type.value} for user: {user_id}")
        
        # Resolve user identity
        resolved_user_id = await self.identity_resolver.resolve(user_id)
        
        # Get or create session
        if session_id is None:
            session_id = await self._get_or_create_session(resolved_user_id)
        
        # Create event
        event = Event(
            event_id=self._generate_event_id(),
            event_type=event_type.value,
            user_id=resolved_user_id,
            session_id=session_id,
            properties=properties,
            timestamp=datetime.utcnow().isoformat(),
            device=device or self._get_device_info(),
            location=location or self._get_location_info(),
            context=context or {}
        )
        
        # Add to queue
        await self.event_queue.put(event)
        
        # Update session
        await self._update_session(event)
        
        logger.debug(f"Event tracked: {event.event_id}")
        
        return event.event_id
    
    async def track_page_view(
        self,
        user_id: str,
        page_name: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> str:
        """Track page view event"""
        event_properties = {
            'page_name': page_name,
            'url': properties.get('url', ''),
            'referrer': properties.get('referrer', ''),
            **(properties or {})
        }
        
        return await self.track_event(
            EventType.PAGE_VIEW,
            user_id,
            event_properties
        )
    
    async def track_click(
        self,
        user_id: str,
        element_id: str,
        element_type: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> str:
        """Track click event"""
        event_properties = {
            'element_id': element_id,
            'element_type': element_type,
            **(properties or {})
        }
        
        return await self.track_event(
            EventType.CLICK,
            user_id,
            event_properties
        )
    
    async def track_feature_used(
        self,
        user_id: str,
        feature_name: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> str:
        """Track feature usage event"""
        event_properties = {
            'feature_name': feature_name,
            **(properties or {})
        }
        
        return await self.track_event(
            EventType.FEATURE_USED,
            user_id,
            event_properties
        )
    
    async def track_purchase(
        self,
        user_id: str,
        purchase_id: str,
        amount: float,
        currency: str,
        items: List[Dict[str, Any]],
        properties: Optional[Dict[str, Any]] = None
    ) -> str:
        """Track purchase event"""
        event_properties = {
            'purchase_id': purchase_id,
            'amount': amount,
            'currency': currency,
            'items': items,
            **(properties or {})
        }
        
        return await self.track_event(
            EventType.PURCHASE,
            user_id,
            event_properties
        )
    
    async def track_error(
        self,
        user_id: str,
        error_type: str,
        error_message: str,
        stack_trace: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> str:
        """Track error event"""
        event_properties = {
            'error_type': error_type,
            'error_message': error_message,
            'stack_trace': stack_trace,
            **(properties or {})
        }
        
        return await self.track_event(
            EventType.ERROR,
            user_id,
            event_properties
        )
    
    def _generate_event_id(self) -> str:
        """Generate unique event ID"""
        import uuid
        return f"evt_{uuid.uuid4().hex}"
    
    async def _get_or_create_session(self, user_id: str) -> str:
        """Get or create user session"""
        # Check for active session
        session_id = await self.storage.get_active_session(user_id)
        
        if session_id is None:
            # Create new session
            session_id = self._generate_session_id()
            session = UserSession(
                session_id=session_id,
                user_id=user_id,
                start_time=datetime.utcnow().isoformat(),
                end_time=None,
                events=[],
                properties={}
            )
            await self.storage.create_session(session)
        
        return session_id
    
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        import uuid
        return f"sess_{uuid.uuid4().hex}"
    
    async def _update_session(self, event: Event):
        """Update session with event"""
        await self.storage.add_event_to_session(event)
    
    def _get_device_info(self) -> Dict[str, Any]:
        """Get device information"""
        # Implementation would extract from request
        return {
            'type': 'web',
            'os': 'unknown',
            'browser': 'unknown',
            'screen_resolution': 'unknown'
        }
    
    def _get_location_info(self) -> Dict[str, Any]:
        """Get location information"""
        # Implementation would extract from IP
        return {
            'country': 'unknown',
            'region': 'unknown',
            'city': 'unknown'
        }
    
    async def _flush_events(self):
        """Flush events to storage"""
        while True:
            await asyncio.sleep(self.flush_interval)
            
            # Collect events
            events = []
            while not self.event_queue.empty() and len(events) < self.batch_size:
                event = await self.event_queue.get()
                events.append(event)
            
            if events:
                logger.info(f"Flushing {len(events)} events...")
                await self.storage.store_events(events)
                logger.info(f"Flushed {len(events)} events")

class IdentityResolver:
    """Identity resolution specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.storage = IdentityStorage(config['storage'])
        
    async def resolve(self, user_id: str) -> str:
        """Resolve user identity"""
        # Check if user exists
        resolved_id = await self.storage.resolve_identity(user_id)
        
        if resolved_id is None:
            # Create new identity
            resolved_id = self._generate_identity_id()
            await self.storage.create_identity(resolved_id, user_id)
        
        return resolved_id
    
    def _generate_identity_id(self) -> str:
        """Generate unique identity ID"""
        import uuid
        return f"id_{uuid.uuid4().hex}"

class EventStorage:
    """Event storage specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.db = self._initialize_database()
        
    def _initialize_database(self):
        """Initialize database connection"""
        # Implementation would connect to database
        pass
    
    async def store_events(self, events: List[Event]):
        """Store events in database"""
        # Implementation would batch insert events
        pass
    
    async def get_active_session(self, user_id: str) -> Optional[str]:
        """Get active session for user"""
        # Implementation would query database
        return None
    
    async def create_session(self, session: UserSession):
        """Create new session"""
        # Implementation would insert session
        pass
    
    async def add_event_to_session(self, event: Event):
        """Add event to session"""
        # Implementation would update session
        pass
    
    async def get_events(
        self,
        user_id: Optional[str] = None,
        event_type: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Event]:
        """Get events with filters"""
        # Implementation would query database
        return []
    
    async def get_user_events(self, user_id: str) -> List[Event]:
        """Get all events for user"""
        return await self.get_events(user_id=user_id)

class IdentityStorage:
    """Identity storage specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def resolve_identity(self, user_id: str) -> Optional[str]:
        """Resolve user identity"""
        # Implementation would query database
        return None
    
    async def create_identity(self, identity_id: str, user_id: str):
        """Create new identity"""
        # Implementation would insert identity
        pass
```

### Analytics Engine

```python
class AnalyticsEngine:
    """Analytics engine for querying and analyzing events"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.storage = EventStorage(config['storage'])
        self.query_engine = QueryEngine(config['query'])
        self.aggregation_engine = AggregationEngine(config['aggregation'])
        self.segmentation_engine = SegmentationEngine(config['segmentation'])
        self.funnel_engine = FunnelEngine(config['funnel'])
        
    async def query_events(
        self,
        filters: Dict[str, Any],
        dimensions: List[str],
        metrics: List[str],
        group_by: Optional[List[str]] = None,
        order_by: Optional[List[str]] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Query events with filters and aggregations"""
        logger.info(f"Querying events with filters: {filters}")
        
        # Build query
        query = self.query_engine.build_query(
            filters=filters,
            dimensions=dimensions,
            metrics=metrics,
            group_by=group_by,
            order_by=order_by,
            limit=limit
        )
        
        # Execute query
        results = await self.query_engine.execute_query(query)
        
        return results
    
    async def get_user_metrics(
        self,
        user_id: str,
        date_range: Dict[str, str]
    ) -> Dict[str, Any]:
        """Get metrics for user"""
        logger.info(f"Getting metrics for user: {user_id}")
        
        # Get user events
        events = await self.storage.get_user_events(user_id)
        
        # Calculate metrics
        metrics = {
            'total_events': len(events),
            'unique_days': self._calculate_unique_days(events),
            'session_count': self._calculate_session_count(events),
            'feature_usage': self._calculate_feature_usage(events),
            'page_views': self._calculate_page_views(events),
            'clicks': self._calculate_clicks(events),
            'purchases': self._calculate_purchases(events)
        }
        
        return metrics
    
    def _calculate_unique_days(self, events: List[Event]) -> int:
        """Calculate unique days"""
        dates = set()
        for event in events:
            date = event.timestamp.split('T')[0]
            dates.add(date)
        return len(dates)
    
    def _calculate_session_count(self, events: List[Event]) -> int:
        """Calculate session count"""
        sessions = set()
        for event in events:
            sessions.add(event.session_id)
        return len(sessions)
    
    def _calculate_feature_usage(self, events: List[Event]) -> Dict[str, int]:
        """Calculate feature usage"""
        usage = {}
        for event in events:
            if event.event_type == EventType.FEATURE_USED.value:
                feature_name = event.properties.get('feature_name', 'unknown')
                usage[feature_name] = usage.get(feature_name, 0) + 1
        return usage
    
    def _calculate_page_views(self, events: List[Event]) -> int:
        """Calculate page views"""
        return sum(1 for event in events if event.event_type == EventType.PAGE_VIEW.value)
    
    def _calculate_clicks(self, events: List[Event]) -> int:
        """Calculate clicks"""
        return sum(1 for event in events if event.event_type == EventType.CLICK.value)
    
    def _calculate_purchases(self, events: List[Event]) -> int:
        """Calculate purchases"""
        return sum(1 for event in events if event.event_type == EventType.PURCHASE.value)
    
    async def get_feature_adoption(
        self,
        feature_name: str,
        date_range: Dict[str, str]
    ) -> Dict[str, Any]:
        """Get feature adoption metrics"""
        logger.info(f"Getting adoption for feature: {feature_name}")
        
        # Query feature usage events
        filters = {
            'event_type': EventType.FEATURE_USED.value,
            'properties.feature_name': feature_name,
            'start_date': date_range['start'],
            'end_date': date_range['end']
        }
        
        events = await self.storage.get_events(**filters)
        
        # Calculate adoption metrics
        unique_users = set(event.user_id for event in events)
        total_users = await self._get_total_users(date_range)
        
        adoption_rate = len(unique_users) / total_users if total_users > 0 else 0
        
        return {
            'feature_name': feature_name,
            'unique_users': len(unique_users),
            'total_users': total_users,
            'adoption_rate': adoption_rate,
            'usage_count': len(events),
            'daily_usage': self._calculate_daily_usage(events)
        }
    
    async def _get_total_users(self, date_range: Dict[str, str]) -> int:
        """Get total users in date range"""
        # Implementation would query database
        return 1000
    
    def _calculate_daily_usage(self, events: List[Event]) -> Dict[str, int]:
        """Calculate daily usage"""
        daily_usage = {}
        for event in events:
            date = event.timestamp.split('T')[0]
            daily_usage[date] = daily_usage.get(date, 0) + 1
        return daily_usage
    
    async def get_conversion_funnel(
        self,
        funnel_steps: List[Dict[str, Any]],
        date_range: Dict[str, str]
    ) -> Dict[str, Any]:
        """Get conversion funnel analysis"""
        logger.info(f"Analyzing funnel with {len(funnel_steps)} steps")
        
        # Calculate funnel metrics
        funnel_results = await self.funnel_engine.analyze_funnel(
            funnel_steps,
            date_range
        )
        
        return funnel_results

class QueryEngine:
    """Query engine for analytics"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    def build_query(
        self,
        filters: Dict[str, Any],
        dimensions: List[str],
        metrics: List[str],
        group_by: Optional[List[str]] = None,
        order_by: Optional[List[str]] = None,
        limit: Optional[int] = None
    ) -> str:
        """Build query from parameters"""
        # Implementation would build SQL or NoSQL query
        return "SELECT * FROM events"
    
    async def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """Execute query and return results"""
        # Implementation would execute query
        return []

class AggregationEngine:
    """Aggregation engine for analytics"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def aggregate(
        self,
        events: List[Event],
        aggregations: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Aggregate events"""
        results = {}
        
        for agg in aggregations:
            agg_type = agg['type']
            field = agg['field']
            alias = agg.get('alias', f"{agg_type}_{field}")
            
            if agg_type == 'count':
                results[alias] = len(events)
            elif agg_type == 'sum':
                results[alias] = sum(e.properties.get(field, 0) for e in events)
            elif agg_type == 'avg':
                values = [e.properties.get(field, 0) for e in events]
                results[alias] = sum(values) / len(values) if values else 0
            elif agg_type == 'min':
                values = [e.properties.get(field, 0) for e in events]
                results[alias] = min(values) if values else 0
            elif agg_type == 'max':
                values = [e.properties.get(field, 0) for e in events]
                results[alias] = max(values) if values else 0
        
        return results

class SegmentationEngine:
    """Segmentation engine for analytics"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def segment_users(
        self,
        segment_definition: Dict[str, Any],
        date_range: Dict[str, str]
    ) -> List[str]:
        """Segment users based on criteria"""
        # Implementation would segment users
        return []

class FunnelEngine:
    """Funnel analysis engine"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def analyze_funnel(
        self,
        funnel_steps: List[Dict[str, Any]],
        date_range: Dict[str, str]
    ) -> Dict[str, Any]:
        """Analyze conversion funnel"""
        results = {
            'steps': [],
            'overall_conversion_rate': 0.0
        }
        
        # Get users for each step
        previous_users = set()
        
        for i, step in enumerate(funnel_steps):
            # Get users who completed this step
            step_users = await self._get_step_users(step, date_range)
            
            # Calculate conversion rate
            if i == 0:
                conversion_rate = 1.0
            else:
                conversion_rate = len(step_users & previous_users) / len(previous_users) if previous_users else 0
            
            results['steps'].append({
                'step': step['name'],
                'users': len(step_users),
                'conversion_rate': conversion_rate,
                'drop_off': 1.0 - conversion_rate if i > 0 else 0.0
            })
            
            previous_users = step_users
        
        # Calculate overall conversion rate
        if results['steps']:
            first_step_users = results['steps'][0]['users']
            last_step_users = results['steps'][-1]['users']
            results['overall_conversion_rate'] = last_step_users / first_step_users if first_step_users > 0 else 0
        
        return results
    
    async def _get_step_users(
        self,
        step: Dict[str, Any],
        date_range: Dict[str, str]
    ) -> set:
        """Get users who completed a step"""
        # Implementation would query database
        return set()
```

### Dashboard & Reporting

```python
class DashboardManager:
    """Dashboard management specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.analytics_engine = AnalyticsEngine(config['analytics'])
        self.dashboard_store = DashboardStore(config['dashboard_store'])
        
    async def create_dashboard(
        self,
        name: str,
        widgets: List[Dict[str, Any]]
    ) -> str:
        """Create new dashboard"""
        logger.info(f"Creating dashboard: {name}")
        
        dashboard_id = self._generate_dashboard_id()
        
        dashboard = {
            'dashboard_id': dashboard_id,
            'name': name,
            'widgets': widgets,
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        await self.dashboard_store.create_dashboard(dashboard)
        
        logger.info(f"Dashboard created: {dashboard_id}")
        
        return dashboard_id
    
    async def get_dashboard_data(
        self,
        dashboard_id: str,
        date_range: Dict[str, str]
    ) -> Dict[str, Any]:
        """Get dashboard data"""
        logger.info(f"Getting dashboard data: {dashboard_id}")
        
        # Get dashboard definition
        dashboard = await self.dashboard_store.get_dashboard(dashboard_id)
        
        # Get data for each widget
        widget_data = []
        for widget in dashboard['widgets']:
            data = await self._get_widget_data(widget, date_range)
            widget_data.append(data)
        
        return {
            'dashboard_id': dashboard_id,
            'name': dashboard['name'],
            'widgets': widget_data
        }
    
    async def _get_widget_data(
        self,
        widget: Dict[str, Any],
        date_range: Dict[str, str]
    ) -> Dict[str, Any]:
        """Get data for widget"""
        widget_type = widget['type']
        
        if widget_type == 'metric':
            return await self._get_metric_widget_data(widget, date_range)
        elif widget_type == 'chart':
            return await self._get_chart_widget_data(widget, date_range)
        elif widget_type == 'funnel':
            return await self._get_funnel_widget_data(widget, date_range)
        elif widget_type == 'table':
            return await self._get_table_widget_data(widget, date_range)
        else:
            raise ValueError(f"Unknown widget type: {widget_type}")
    
    async def _get_metric_widget_data(
        self,
        widget: Dict[str, Any],
        date_range: Dict[str, str]
    ) -> Dict[str, Any]:
        """Get metric widget data"""
        # Query metric
        metric_value = await self.analytics_engine.query_events(
            filters=widget['filters'],
            dimensions=widget['dimensions'],
            metrics=widget['metrics'],
            date_range=date_range
        )
        
        return {
            'widget_id': widget['widget_id'],
            'type': 'metric',
            'title': widget['title'],
            'value': metric_value[0]['value'] if metric_value else 0,
            'trend': widget.get('trend')
        }
    
    async def _get_chart_widget_data(
        self,
        widget: Dict[str, Any],
        date_range: Dict[str, str]
    ) -> Dict[str, Any]:
        """Get chart widget data"""
        # Query chart data
        chart_data = await self.analytics_engine.query_events(
            filters=widget['filters'],
            dimensions=widget['dimensions'],
            metrics=widget['metrics'],
            group_by=widget['group_by'],
            order_by=widget['order_by'],
            date_range=date_range
        )
        
        return {
            'widget_id': widget['widget_id'],
            'type': 'chart',
            'title': widget['title'],
            'chart_type': widget['chart_type'],
            'data': chart_data
        }
    
    async def _get_funnel_widget_data(
        self,
        widget: Dict[str, Any],
        date_range: Dict[str, str]
    ) -> Dict[str, Any]:
        """Get funnel widget data"""
        # Query funnel data
        funnel_data = await self.analytics_engine.get_conversion_funnel(
            widget['funnel_steps'],
            date_range
        )
        
        return {
            'widget_id': widget['widget_id'],
            'type': 'funnel',
            'title': widget['title'],
            'data': funnel_data
        }
    
    async def _get_table_widget_data(
        self,
        widget: Dict[str, Any],
        date_range: Dict[str, str]
    ) -> Dict[str, Any]:
        """Get table widget data"""
        # Query table data
        table_data = await self.analytics_engine.query_events(
            filters=widget['filters'],
            dimensions=widget['dimensions'],
            metrics=widget['metrics'],
            order_by=widget['order_by'],
            limit=widget['limit'],
            date_range=date_range
        )
        
        return {
            'widget_id': widget['widget_id'],
            'type': 'table',
            'title': widget['title'],
            'columns': widget['columns'],
            'data': table_data
        }
    
    def _generate_dashboard_id(self) -> str:
        """Generate unique dashboard ID"""
        import uuid
        return f"dash_{uuid.uuid4().hex}"

class DashboardStore:
    """Dashboard storage specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def create_dashboard(self, dashboard: Dict[str, Any]):
        """Create dashboard"""
        # Implementation would store dashboard
        pass
    
    async def get_dashboard(self, dashboard_id: str) -> Dict[str, Any]:
        """Get dashboard"""
        # Implementation would retrieve dashboard
        return {}
    
    async def list_dashboards(self) -> List[Dict[str, Any]]:
        """List all dashboards"""
        # Implementation would list dashboards
        return []
```

---

## Tooling & Tech Stack

### Analytics Platforms
- **Mixpanel**: Product analytics platform
- **Amplitude**: Analytics platform
- **Google Analytics**: Web analytics
- **Heap**: User analytics
- **FullStory**: User behavior analytics

### Data Infrastructure
- **PostgreSQL**: Database
- **ClickHouse**: OLAP database
- **Apache Kafka**: Event streaming
- **Apache Spark**: Data processing
- **Apache Airflow**: Workflow orchestration

### Visualization
- **Grafana**: Visualization platform
- **Metabase**: Open source BI
- **Superset**: Open source BI
- **Looker**: BI platform
- **Tableau**: BI platform

### Monitoring
- **Prometheus**: Metrics collection
- **Grafana**: Visualization
- **Alertmanager**: Alert management
- **PagerDuty**: Incident management

---

## Configuration Essentials

### Analytics Configuration

```yaml
# config/analytics_config.yaml
analytics:
  tracking:
    enabled: true
    batch_size: 100
    flush_interval: 5  # seconds
    
  events:
    page_view:
      enabled: true
      properties:
        - url
        - referrer
        - page_name
    
    click:
      enabled: true
      properties:
        - element_id
        - element_type
        - element_text
    
    feature_used:
      enabled: true
      properties:
        - feature_name
        - feature_version
    
    purchase:
      enabled: true
      properties:
        - purchase_id
        - amount
        - currency
        - items
    
    error:
      enabled: true
      properties:
        - error_type
        - error_message
        - stack_trace

  storage:
    type: "postgresql"
    connection:
      host: "localhost"
      port: 5432
      database: "analytics"
      username: "${DB_USERNAME}"
      password: "${DB_PASSWORD}"
    
    retention:
      events: 365  # days
      sessions: 90  # days
      users: 3650  # days

  identity:
    enabled: true
    merge_window: 30  # days

  privacy:
    anonymize_ip: true
    hash_user_id: false
    gdpr_compliance: true
```

### Dashboard Configuration

```yaml
# config/dashboard_config.yaml
dashboards:
  overview:
    name: "Product Overview"
    widgets:
      - widget_id: "total_users"
        type: "metric"
        title: "Total Users"
        filters:
          start_date: "30_days_ago"
          end_date: "today"
        metrics:
          - type: "count_distinct"
            field: "user_id"
        trend: "7_days"
      
      - widget_id: "active_users"
        type: "metric"
        title: "Active Users (7d)"
        filters:
          start_date: "7_days_ago"
          end_date: "today"
        metrics:
          - type: "count_distinct"
            field: "user_id"
        trend: "7_days"
      
      - widget_id: "feature_adoption"
        type: "chart"
        title: "Feature Adoption"
        chart_type: "bar"
        filters:
          start_date: "30_days_ago"
          end_date: "today"
          event_type: "feature_used"
        dimensions:
          - "properties.feature_name"
        metrics:
          - type: "count_distinct"
            field: "user_id"
        group_by:
          - "properties.feature_name"
        order_by:
          - "count DESC"
      
      - widget_id: "signup_funnel"
        type: "funnel"
        title: "Signup Funnel"
        funnel_steps:
          - name: "Page View"
            event_type: "page_view"
            filters:
              page_name: "signup"
          - name: "Click Signup"
            event_type: "click"
            filters:
              element_id: "signup_button"
          - name: "Submit Form"
            event_type: "submit"
            filters:
              form_name: "signup"
          - name: "Sign Up"
            event_type: "sign_up"
```

---

## Code Examples

### Good: Complete Analytics Implementation

```python
# analytics/implementation.py
import asyncio
import logging
from typing import Dict, Any

from analytics.tracker import EventTracker
from analytics.engine import AnalyticsEngine
from analytics.dashboard import DashboardManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def setup_analytics():
    """Setup analytics implementation"""
    logger.info("=" * 60)
    logger.info("Product Analytics Implementation")
    logger.info("=" * 60)
    
    # Load configuration
    config = load_config('config/analytics_config.yaml')
    
    # Step 1: Initialize event tracker
    logger.info("\n" + "=" * 60)
    logger.info("Step 1: Initializing Event Tracker")
    logger.info("=" * 60)
    
    tracker = EventTracker(config['tracking'])
    
    logger.info("Event tracker initialized")
    
    # Step 2: Initialize analytics engine
    logger.info("\n" + "=" * 60)
    logger.info("Step 2: Initializing Analytics Engine")
    logger.info("=" * 60)
    
    engine = AnalyticsEngine(config['analytics'])
    
    logger.info("Analytics engine initialized")
    
    # Step 3: Initialize dashboard manager
    logger.info("\n" + "=" * 60)
    logger.info("Step 3: Initializing Dashboard Manager")
    logger.info("=" * 60)
    
    dashboard_manager = DashboardManager(config['dashboard'])
    
    logger.info("Dashboard manager initialized")
    
    # Step 4: Create dashboard
    logger.info("\n" + "=" * 60)
    logger.info("Step 4: Creating Dashboard")
    logger.info("=" * 60)
    
    dashboard_config = load_config('config/dashboard_config.yaml')
    dashboard_id = await dashboard_manager.create_dashboard(
        dashboard_config['dashboards']['overview']['name'],
        dashboard_config['dashboards']['overview']['widgets']
    )
    
    logger.info(f"Dashboard created: {dashboard_id}")
    
    # Step 5: Test event tracking
    logger.info("\n" + "=" * 60)
    logger.info("Step 5: Testing Event Tracking")
    logger.info("=" * 60)
    
    # Track page view
    event_id = await tracker.track_page_view(
        user_id="user_123",
        page_name="home",
        properties={
            'url': 'https://example.com/home',
            'referrer': 'https://google.com'
        }
    )
    logger.info(f"Page view tracked: {event_id}")
    
    # Track feature usage
    event_id = await tracker.track_feature_used(
        user_id="user_123",
        feature_name="search",
        properties={
            'query': 'analytics',
            'results_count': 10
        }
    )
    logger.info(f"Feature usage tracked: {event_id}")
    
    # Step 6: Query analytics
    logger.info("\n" + "=" * 60)
    logger.info("Step 6: Querying Analytics")
    logger.info("=" * 60)
    
    # Get user metrics
    user_metrics = await engine.get_user_metrics(
        user_id="user_123",
        date_range={
            'start': '30_days_ago',
            'end': 'today'
        }
    )
    
    logger.info(f"User metrics: {user_metrics}")
    
    # Get feature adoption
    feature_adoption = await engine.get_feature_adoption(
        feature_name="search",
        date_range={
            'start': '30_days_ago',
            'end': 'today'
        }
    )
    
    logger.info(f"Feature adoption: {feature_adoption}")
    
    # Step 7: Get dashboard data
    logger.info("\n" + "=" * 60)
    logger.info("Step 7: Getting Dashboard Data")
    logger.info("=" * 60)
    
    dashboard_data = await dashboard_manager.get_dashboard_data(
        dashboard_id,
        date_range={
            'start': '30_days_ago',
            'end': 'today'
        }
    )
    
    logger.info(f"Dashboard data: {len(dashboard_data['widgets'])} widgets")
    
    # Print summary
    print_summary(dashboard_id, dashboard_data, user_metrics, feature_adoption)

def load_config(filename: str) -> Dict[str, Any]:
    """Load configuration from file"""
    import yaml
    with open(filename, 'r') as f:
        return yaml.safe_load(f)

def print_summary(
    dashboard_id: str,
    dashboard_data: Dict[str, Any],
    user_metrics: Dict[str, Any],
    feature_adoption: Dict[str, Any]
):
    """Print implementation summary"""
    print("\n" + "=" * 60)
    print("Analytics Implementation Summary")
    print("=" * 60)
    print(f"Dashboard ID: {dashboard_id}")
    print(f"Widgets: {len(dashboard_data['widgets'])}")
    print(f"\nUser Metrics:")
    print(f"  Total Events: {user_metrics['total_events']}")
    print(f"  Unique Days: {user_metrics['unique_days']}")
    print(f"  Sessions: {user_metrics['session_count']}")
    print(f"  Page Views: {user_metrics['page_views']}")
    print(f"  Clicks: {user_metrics['clicks']}")
    print(f"  Purchases: {user_metrics['purchases']}")
    print(f"\nFeature Adoption:")
    print(f"  Feature: {feature_adoption['feature_name']}")
    print(f"  Unique Users: {feature_adoption['unique_users']}")
    print(f"  Total Users: {feature_adoption['total_users']}")
    print(f"  Adoption Rate: {feature_adoption['adoption_rate']:.2%}")

async def main():
    """Main entry point"""
    await setup_analytics()

if __name__ == "__main__":
    asyncio.run(main())
```

### Bad: Anti-pattern Example

```python
# BAD: No event tracking
def bad_analytics():
    # No tracking
    pass

# BAD: No data storage
def bad_analytics():
    # Track events but don't store
    track_event()

# BAD: No analytics
def bad_analytics():
    # Store events but don't analyze
    store_events()

# BAD: No dashboards
def bad_analytics():
    # Analyze but don't visualize
    analyze_events()

# BAD: No privacy
def bad_analytics():
    # Track everything without privacy
    track_all_data()
```

---

## Standards, Compliance & Security

### Industry Standards
- **GDPR**: Data protection and privacy
- **CCPA**: California Consumer Privacy Act
- **SOC 2 Type II**: Security and availability
- **ISO 27001**: Information security

### Security Best Practices
- **Data Encryption**: Encrypt all data at rest and in transit
- **Access Control**: RBAC for analytics data
- **Audit Logging**: Log all analytics activities
- **Data Minimization**: Collect only necessary data

### Compliance Requirements
- **User Consent**: Obtain user consent for tracking
- **Data Anonymization**: Anonymize sensitive data
- **Data Retention**: Implement data retention policies
- **Right to be Forgotten**: Support GDPR requirements

---

## Quick Start

### 1. Install Dependencies

```bash
pip install pyyaml
pip install asyncpg
pip install pandas
```

### 2. Configure Analytics

```bash
# Copy example config
cp config/analytics_config.yaml.example config/analytics_config.yaml

# Edit configuration
vim config/analytics_config.yaml
```

### 3. Initialize Database

```bash
# Run migrations
python analytics/migrate.py

# Create tables
python analytics/init_db.py
```

### 4. Start Tracking

```bash
# Start event tracker
python analytics/tracker.py
```

---

## Production Checklist

### Event Tracking
- [ ] Event types defined
- [ ] Event properties defined
- [ ] Tracking implemented
- [ ] Batch processing configured
- [ ] Error handling implemented

### Data Storage
- [ ] Database schema created
- [ ] Indexes configured
- [ ] Retention policies defined
- [ ] Backup procedures documented
- [ ] Privacy controls implemented

### Analytics Engine
- [ ] Query engine configured
- [ ] Aggregation functions defined
- [ ] Segmentation rules defined
- [ ] Funnel analysis configured
- [ ] Performance optimized

### Dashboards
- [ ] Dashboards created
- [ ] Widgets configured
- [ ] Alerts configured
- [ ] Access controls defined
- [ ] Performance optimized

### Compliance
- [ ] User consent implemented
- [ ] Data anonymization configured
- [ ] Retention policies enforced
- [ ] Right to be forgotten implemented
- [ ] Audit logging enabled

---

## Anti-patterns

### ❌ Avoid These Practices

1. **No Event Tracking**
   ```python
   # BAD: No tracking
   pass
   ```

2. **No Data Storage**
   ```python
   # BAD: No storage
   track_event()
   ```

3. **No Analytics**
   ```python
   # BAD: No analytics
   store_events()
   ```

4. **No Dashboards**
   ```python
   # BAD: No dashboards
   analyze_events()
   ```

5. **No Privacy**
   ```python
   # BAD: No privacy
   track_all_data()
   ```

### ✅ Follow These Practices

1. **Event Tracking**
   ```python
   # GOOD: Event tracking
   tracker = EventTracker(config)
   await tracker.track_event(event_type, user_id, properties)
   ```

2. **Data Storage**
   ```python
   # GOOD: Data storage
   storage = EventStorage(config)
   await storage.store_events(events)
   ```

3. **Analytics**
   ```python
   # GOOD: Analytics
   engine = AnalyticsEngine(config)
   results = await engine.query_events(filters, dimensions, metrics)
   ```

4. **Dashboards**
   ```python
   # GOOD: Dashboards
   dashboard_manager = DashboardManager(config)
   data = await dashboard_manager.get_dashboard_data(dashboard_id, date_range)
   ```

5. **Privacy**
   ```python
   # GOOD: Privacy
   tracker = EventTracker(config)
   await tracker.track_event(event_type, user_id, properties, anonymize=True)
   ```

---

## Unit Economics & KPIs

### Development Costs
- **Initial Setup**: 40-60 hours
- **Event Tracking**: 20-40 hours
- **Analytics Engine**: 40-60 hours
- **Dashboards**: 20-40 hours
- **Total**: 120-200 hours

### Operational Costs
- **Analytics Platform**: $200-1000/month
- **Data Storage**: $100-500/month
- **Compute**: $50-200/month
- **Monitoring**: $50-100/month

### ROI Metrics
- **Decision Quality**: 60-80% improvement
- **Feature Adoption**: 40-60% improvement
- **User Engagement**: 30-50% improvement
- **Revenue Impact**: 20-40% improvement

### KPI Targets
- **Event Tracking Accuracy**: > 99.9%
- **Query Performance**: < 5 seconds
- **Dashboard Load Time**: < 2 seconds
- **Data Freshness**: < 5 minutes
- **User Adoption**: > 80%

---

## Integration Points / Related Skills

### Upstream Skills
- **136. Business to Technical Spec**: Requirements
- **137. API-First Product Strategy**: API design
- **138. Platform Product Design**: Platform design

### Parallel Skills
- **139. Product Discovery Validation**: Validation
- **141. Feature Prioritization**: Prioritization
- **142. Technical Debt Prioritization**: Debt management

### Downstream Skills
- **143. Competitive Intelligence**: Competitive analysis
- **144. Product Roadmap Communication**: Roadmap
- **145. Cross-Functional Leadership**: Leadership

### Cross-Domain Skills
- **14. Monitoring and Observability**: Monitoring
- **15. DevOps Infrastructure**: Infrastructure
- **81. SaaS FinOps Pricing**: Pricing strategy
- **84. Compliance AI Governance**: Compliance

---

## References & Resources

### Documentation
- [Mixpanel Documentation](https://help.mixpanel.com/hc/en-us)
- [Amplitude Documentation](https://help.amplitude.com/hc/en-us)
- [Google Analytics Documentation](https://support.google.com/analytics/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

### Best Practices
- [Product Analytics Best Practices](https://www.productanalyticsbook.com/)
- [Event Tracking Best Practices](https://segment.com/blog/what-is-event-tracking/)
- [Analytics Dashboard Design](https://www.uxdesign.cc/)

### Tools & Libraries
- [Mixpanel](https://mixpanel.com/)
- [Amplitude](https://amplitude.com/)
- [Google Analytics](https://analytics.google.com/)
- [Grafana](https://grafana.com/)
- [Metabase](https://www.metabase.com/)
