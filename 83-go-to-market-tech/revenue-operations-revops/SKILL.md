---
name: Revenue Operations (RevOps)
description: Aligning marketing, sales, and customer success for revenue growth
---

# Revenue Operations (RevOps)

## Current Level: Expert (Enterprise Scale)

## Domain: Go-to-Market Tech
## Skill ID: 156

---

## Executive Summary

Revenue Operations (RevOps) enables aligning marketing, sales, and customer success for revenue growth. This capability is essential for breaking down silos, improving operational efficiency, increasing revenue predictability, and driving sustainable growth.

### Strategic Necessity

- **Alignment**: Align marketing, sales, and customer success
- **Efficiency**: Improve operational efficiency
- **Predictability**: Increase revenue predictability
- **Growth**: Drive sustainable revenue growth
- **Visibility**: Improve end-to-end visibility

---

## Technical Deep Dive

### RevOps Framework

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Revenue Operations (RevOps) Framework                    │
│                                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│  │   Marketing  │    │    Sales     │    │   Customer   │                  │
│  │   Ops       │───▶│    Ops       │───▶│   Success    │                  │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘                  │
│         │                   │                   │                           │
│         ▼                   ▼                   ▼                           │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Revenue Alignment                             │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Goals      │  │  Processes  │  │  Data       │  │  Metrics    │            │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘            │   │
│  └───────┼────────────┼────────────┼────────────┼────────────┼────────────────────┘   │
│          │            │            │            │                         │
│          ▼            ▼            ▼            ▼                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Process Alignment                             │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Lead       │  │  Opportunity │  │  Customer   │  │  Revenue    │            │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘            │   │
│  └───────┼────────────┼────────────┼────────────┼────────────┼────────────────────┘   │
│          │            │            │            │                         │
│          ▼            ▼            ▼            ▼                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Data Alignment                                │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  CRM        │  │  Marketing  │  │  Sales      │  │  Success    │            │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘            │   │
│  └───────┼────────────┼────────────┼────────────┼────────────┼────────────────────┘   │
│          │            │            │            │                         │
│          ▼            ▼            ▼            ▼                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Revenue Analytics                             │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Pipeline    │  │  Forecast   │  │  ARR        │  │  LTV        │            │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘            │   │
│  └───────┼────────────┼────────────┼────────────┼────────────┼────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Revenue Alignment

```python
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import asyncio
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class RevenueStage(Enum):
    """Revenue stages"""
    LEAD = "lead"
    MQL = "mql"
    SQL = "sql"
    OPPORTUNITY = "opportunity"
    CUSTOMER = "customer"
    CHURNED = "churned"

class RevenueMetric(Enum):
    """Revenue metrics"""
    MRR = "mrr"
    ARR = "arr"
    LTV = "ltv"
    CAC = "cac"
    LTV_CAC_RATIO = "ltv_cac_ratio"
    CHURN_RATE = "churn_rate"
    NET_RETENTION = "net_retention"

@dataclass
class RevenueGoal:
    """Revenue goal definition"""
    goal_id: str
    name: str
    metric: RevenueMetric
    target: float
    period: str
    department: str
    status: str
    progress: float
    created_at: str
    updated_at: str

@dataclass
class RevenueProcess:
    """Revenue process definition"""
    process_id: str
    name: str
    stages: List[str]
    handoffs: List[Dict[str, Any]]
    owners: List[str]
    metrics: List[str]
    created_at: str
    updated_at: str

class RevenueAligner:
    """Revenue alignment specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.goal_manager = GoalManager(config['goals'])
        self.process_manager = ProcessManager(config['processes'])
        self.data_manager = DataManager(config['data'])
        self.metrics_manager = MetricsManager(config['metrics'])
        
    async def align_revenue(self) -> Dict[str, Any]:
        """Align revenue across marketing, sales, and customer success"""
        logger.info("Aligning revenue...")
        
        # Align goals
        goals = await self._align_goals()
        
        # Align processes
        processes = await self._align_processes()
        
        # Align data
        data = await self._align_data()
        
        # Align metrics
        metrics = await self._align_metrics()
        
        # Compile results
        results = {
            'goals': goals,
            'processes': processes,
            'data': data,
            'metrics': metrics,
            'aligned_at': datetime.utcnow().isoformat()
        }
        
        logger.info("Revenue aligned")
        
        return results
    
    async def _align_goals(self) -> Dict[str, Any]:
        """Align revenue goals"""
        logger.info("Aligning revenue goals...")
        
        # Get goals from all departments
        marketing_goals = await self.goal_manager.get_goals('marketing')
        sales_goals = await self.goal_manager.get_goals('sales')
        success_goals = await self.goal_manager.get_goals('customer_success')
        
        # Align goals
        aligned_goals = self._calculate_aligned_goals(
            marketing_goals,
            sales_goals,
            success_goals
        )
        
        logger.info(f"Aligned {len(aligned_goals)} revenue goals")
        
        return {
            'marketing': marketing_goals,
            'sales': sales_goals,
            'customer_success': success_goals,
            'aligned': aligned_goals
        }
    
    async def _align_processes(self) -> Dict[str, Any]:
        """Align revenue processes"""
        logger.info("Aligning revenue processes...")
        
        # Get processes from all departments
        marketing_processes = await self.process_manager.get_processes('marketing')
        sales_processes = await self.process_manager.get_processes('sales')
        success_processes = await self.process_manager.get_processes('customer_success')
        
        # Align processes
        aligned_processes = self._calculate_aligned_processes(
            marketing_processes,
            sales_processes,
            success_processes
        )
        
        logger.info(f"Aligned {len(aligned_processes)} revenue processes")
        
        return {
            'marketing': marketing_processes,
            'sales': sales_processes,
            'customer_success': success_processes,
            'aligned': aligned_processes
        }
    
    async def _align_data(self) -> Dict[str, Any]:
        """Align revenue data"""
        logger.info("Aligning revenue data...")
        
        # Get data from all departments
        marketing_data = await self.data_manager.get_data('marketing')
        sales_data = await self.data_manager.get_data('sales')
        success_data = await self.data_manager.get_data('customer_success')
        
        # Align data
        aligned_data = self._calculate_aligned_data(
            marketing_data,
            sales_data,
            success_data
        )
        
        logger.info("Revenue data aligned")
        
        return {
            'marketing': marketing_data,
            'sales': sales_data,
            'customer_success': success_data,
            'aligned': aligned_data
        }
    
    async def _align_metrics(self) -> Dict[str, Any]:
        """Align revenue metrics"""
        logger.info("Aligning revenue metrics...")
        
        # Get metrics from all departments
        marketing_metrics = await self.metrics_manager.get_metrics('marketing')
        sales_metrics = await self.metrics_manager.get_metrics('sales')
        success_metrics = await self.metrics_manager.get_metrics('customer_success')
        
        # Align metrics
        aligned_metrics = self._calculate_aligned_metrics(
            marketing_metrics,
            sales_metrics,
            success_metrics
        )
        
        logger.info(f"Aligned {len(aligned_metrics)} revenue metrics")
        
        return {
            'marketing': marketing_metrics,
            'sales': sales_metrics,
            'customer_success': success_metrics,
            'aligned': aligned_metrics
        }
    
    def _calculate_aligned_goals(
        self,
        marketing_goals: List[RevenueGoal],
        sales_goals: List[RevenueGoal],
        success_goals: List[RevenueGoal]
    ) -> List[Dict[str, Any]]:
        """Calculate aligned goals"""
        # Implementation would calculate aligned goals
        return []
    
    def _calculate_aligned_processes(
        self,
        marketing_processes: List[RevenueProcess],
        sales_processes: List[RevenueProcess],
        success_processes: List[RevenueProcess]
    ) -> List[Dict[str, Any]]:
        """Calculate aligned processes"""
        # Implementation would calculate aligned processes
        return []
    
    def _calculate_aligned_data(
        self,
        marketing_data: Dict[str, Any],
        sales_data: Dict[str, Any],
        success_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate aligned data"""
        # Implementation would calculate aligned data
        return {}
    
    def _calculate_aligned_metrics(
        self,
        marketing_metrics: Dict[str, Any],
        sales_metrics: Dict[str, Any],
        success_metrics: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Calculate aligned metrics"""
        # Implementation would calculate aligned metrics
        return []

class GoalManager:
    """Goal management specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.goal_store = GoalStore(config['goal_store'])
        
    async def get_goals(self, department: str) -> List[RevenueGoal]:
        """Get goals for department"""
        logger.info(f"Getting goals for department: {department}")
        
        # Query goals from store
        goals = await self.goal_store.list_goals(department)
        
        logger.info(f"Retrieved {len(goals)} goals for {department}")
        
        return goals
    
    async def create_goal(self, goal: RevenueGoal):
        """Create goal"""
        # Implementation would store in database
        pass
    
    async def update_goal(self, goal: RevenueGoal):
        """Update goal"""
        # Implementation would update database
        pass

class ProcessManager:
    """Process management specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.process_store = ProcessStore(config['process_store'])
        
    async def get_processes(self, department: str) -> List[RevenueProcess]:
        """Get processes for department"""
        logger.info(f"Getting processes for department: {department}")
        
        # Query processes from store
        processes = await self.process_store.list_processes(department)
        
        logger.info(f"Retrieved {len(processes)} processes for {department}")
        
        return processes
    
    async def create_process(self, process: RevenueProcess):
        """Create process"""
        # Implementation would store in database
        pass
    
    async def update_process(self, process: RevenueProcess):
        """Update process"""
        # Implementation would update database
        pass

class DataManager:
    """Data management specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.data_store = DataStore(config['data_store'])
        self.data_sync = DataSync(config['sync'])
        
    async def get_data(self, department: str) -> Dict[str, Any]:
        """Get data for department"""
        logger.info(f"Getting data for department: {department}")
        
        # Query data from store
        data = await self.data_store.get_department_data(department)
        
        logger.info(f"Retrieved data for {department}")
        
        return data
    
    async def sync_data(self):
        """Sync data across departments"""
        logger.info("Syncing data across departments...")
        
        # Sync data
        await self.data_sync.sync_all_data()
        
        logger.info("Data synced")
    
    async def integrate_data(self) -> Dict[str, Any]:
        """Integrate data across departments"""
        logger.info("Integrating data across departments...")
        
        # Get data from all departments
        marketing_data = await self.get_data('marketing')
        sales_data = await self.get_data('sales')
        success_data = await self.get_data('customer_success')
        
        # Integrate data
        integrated_data = self._integrate_data(
            marketing_data,
            sales_data,
            success_data
        )
        
        logger.info("Data integrated")
        
        return integrated_data
    
    def _integrate_data(
        self,
        marketing_data: Dict[str, Any],
        sales_data: Dict[str, Any],
        success_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Integrate data"""
        # Implementation would integrate data
        return {}

class MetricsManager:
    """Metrics management specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.metrics_calculator = MetricsCalculator(config['calculator'])
        
    async def get_metrics(self, department: str) -> Dict[str, Any]:
        """Get metrics for department"""
        logger.info(f"Getting metrics for department: {department}")
        
        # Calculate metrics
        metrics = await self.metrics_calculator.calculate_metrics(department)
        
        logger.info(f"Calculated metrics for {department}")
        
        return metrics
    
    async def calculate_revenue_metrics(self) -> Dict[str, Any]:
        """Calculate revenue metrics"""
        logger.info("Calculating revenue metrics...")
        
        # Calculate metrics from all departments
        marketing_metrics = await self.get_metrics('marketing')
        sales_metrics = await self.get_metrics('sales')
        success_metrics = await self.get_metrics('customer_success')
        
        # Calculate revenue metrics
        revenue_metrics = self._calculate_revenue_metrics(
            marketing_metrics,
            sales_metrics,
            success_metrics
        )
        
        logger.info("Revenue metrics calculated")
        
        return revenue_metrics
    
    def _calculate_revenue_metrics(
        self,
        marketing_metrics: Dict[str, Any],
        sales_metrics: Dict[str, Any],
        success_metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate revenue metrics"""
        # Implementation would calculate revenue metrics
        return {}

class MetricsCalculator:
    """Metrics calculation specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def calculate_metrics(self, department: str) -> Dict[str, Any]:
        """Calculate metrics for department"""
        logger.info(f"Calculating metrics for department: {department}")
        # Implementation would calculate metrics
        return {}

class GoalStore:
    """Goal storage specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def list_goals(self, department: str) -> List[RevenueGoal]:
        """List goals"""
        # Implementation would query database
        return []

class ProcessStore:
    """Process storage specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def list_processes(self, department: str) -> List[RevenueProcess]:
        """List processes"""
        # Implementation would query database
        return []

class DataStore:
    """Data storage specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def get_department_data(self, department: str) -> Dict[str, Any]:
        """Get department data"""
        # Implementation would query database
        return {}

class DataSync:
    """Data sync specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def sync_all_data(self):
        """Sync all data"""
        # Implementation would sync data
        pass
```

### Process Alignment

```python
class ProcessAligner:
    """Process alignment specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.process_manager = ProcessManager(config['processes'])
        self.handoff_manager = HandoffManager(config['handoffs'])
        self.workflow_manager = WorkflowManager(config['workflows'])
        
    async def align_processes(self) -> Dict[str, Any]:
        """Align processes across departments"""
        logger.info("Aligning processes...")
        
        # Map end-to-end process
        end_to_end_process = await self._map_end_to_end_process()
        
        # Define handoffs
        handoffs = await self._define_handoffs()
        
        # Create workflows
        workflows = await self._create_workflows()
        
        # Compile results
        results = {
            'end_to_end_process': end_to_end_process,
            'handoffs': handoffs,
            'workflows': workflows,
            'aligned_at': datetime.utcnow().isoformat()
        }
        
        logger.info("Processes aligned")
        
        return results
    
    async def _map_end_to_end_process(self) -> Dict[str, Any]:
        """Map end-to-end process"""
        logger.info("Mapping end-to-end process...")
        
        # Define stages
        stages = [
            {'stage': 'lead', 'department': 'marketing'},
            {'stage': 'mql', 'department': 'marketing'},
            {'stage': 'sql', 'department': 'sales'},
            {'stage': 'opportunity', 'department': 'sales'},
            {'stage': 'customer', 'department': 'customer_success'}
        ]
        
        # Define transitions
        transitions = [
            {'from': 'lead', 'to': 'mql', 'criteria': 'lead_score > 50'},
            {'from': 'mql', 'to': 'sql', 'criteria': 'sales_acceptance'},
            {'from': 'sql', 'to': 'opportunity', 'criteria': 'opportunity_created'},
            {'from': 'opportunity', 'to': 'customer', 'criteria': 'deal_closed_won'}
        ]
        
        end_to_end_process = {
            'stages': stages,
            'transitions': transitions,
            'mapped_at': datetime.utcnow().isoformat()
        }
        
        logger.info("End-to-end process mapped")
        
        return end_to_end_process
    
    async def _define_handoffs(self) -> List[Dict[str, Any]]:
        """Define handoffs between departments"""
        logger.info("Defining handoffs...")
        
        # Define handoffs
        handoffs = [
            {
                'handoff_id': 'marketing_to_sales',
                'from_department': 'marketing',
                'to_department': 'sales',
                'stage': 'mql_to_sql',
                'criteria': {
                    'lead_score': '> 50',
                    'company_size': '>',
                    'industry': 'in target list'
                },
                'process': {
                    'notify_sales_rep': True,
                    'create_opportunity': True,
                    'transfer_data': True
                },
                'sla': {
                    'response_time': '24 hours',
                    'acceptance_rate': '> 80%'
                }
            },
            {
                'handoff_id': 'sales_to_success',
                'from_department': 'sales',
                'to_department': 'customer_success',
                'stage': 'opportunity_to_customer',
                'criteria': {
                    'deal_closed': True,
                    'contract_signed': True,
                    'payment_received': True
                },
                'process': {
                    'notify_success_manager': True,
                    'create_customer': True,
                    'transfer_data': True,
                    'schedule_onboarding': True
                },
                'sla': {
                    'onboarding_start': '24 hours',
                    'first_contact': '48 hours'
                }
            }
        ]
        
        logger.info(f"Defined {len(handoffs)} handoffs")
        
        return handoffs
    
    async def _create_workflows(self) -> List[Dict[str, Any]]:
        """Create workflows for processes"""
        logger.info("Creating workflows...")
        
        # Define workflows
        workflows = [
            {
                'workflow_id': 'lead_to_customer',
                'name': 'Lead to Customer',
                'stages': [
                    'lead',
                    'mql',
                    'sql',
                    'opportunity',
                    'customer'
                ],
                'handoffs': [
                    'marketing_to_sales',
                    'sales_to_success'
                ],
                'automation': {
                    'lead_scoring': True,
                    'opportunity_creation': True,
                    'customer_creation': True,
                    'notifications': True
                },
                'created_at': datetime.utcnow().isoformat()
            }
        ]
        
        logger.info(f"Created {len(workflows)} workflows")
        
        return workflows

class HandoffManager:
    """Handoff management specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.notification_service = NotificationService(config['notifications'])
        
    async def execute_handoff(
        self,
        handoff_id: str,
        entity_id: str
    ) -> Dict[str, Any]:
        """Execute handoff"""
        logger.info(f"Executing handoff: {handoff_id} for entity: {entity_id}")
        
        # Get handoff definition
        handoff = await self._get_handoff(handoff_id)
        
        # Execute handoff process
        result = await self._execute_handoff_process(handoff, entity_id)
        
        logger.info(f"Handoff executed: {handoff_id}")
        
        return result
    
    async def _get_handoff(self, handoff_id: str) -> Dict[str, Any]:
        """Get handoff definition"""
        # Implementation would get handoff definition
        return {}
    
    async def _execute_handoff_process(
        self,
        handoff: Dict[str, Any],
        entity_id: str
    ) -> Dict[str, Any]:
        """Execute handoff process"""
        # Implementation would execute handoff process
        return {}

class WorkflowManager:
    """Workflow management specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def execute_workflow(
        self,
        workflow_id: str,
        entity_id: str
    ) -> Dict[str, Any]:
        """Execute workflow"""
        logger.info(f"Executing workflow: {workflow_id} for entity: {entity_id}")
        
        # Get workflow definition
        workflow = await self._get_workflow(workflow_id)
        
        # Execute workflow
        result = await self._execute_workflow_process(workflow, entity_id)
        
        logger.info(f"Workflow executed: {workflow_id}")
        
        return result
    
    async def _get_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Get workflow definition"""
        # Implementation would get workflow definition
        return {}
    
    async def _execute_workflow_process(
        self,
        workflow: Dict[str, Any],
        entity_id: str
    ) -> Dict[str, Any]:
        """Execute workflow process"""
        # Implementation would execute workflow process
        return {}

class NotificationService:
    """Notification service specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def notify(self, recipient: str, message: str):
        """Send notification"""
        # Implementation would send notification
        pass
```

### Revenue Analytics

```python
class RevenueAnalyzer:
    """Revenue analytics specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.pipeline_analyzer = PipelineAnalyzer(config['pipeline'])
        self.forecast_analyzer = ForecastAnalyzer(config['forecast'])
        self.arr_analyzer = ARRAnalyzer(config['arr'])
        self.ltv_analyzer = LTVAnalyzer(config['ltv'])
        
    async def analyze_revenue(self) -> Dict[str, Any]:
        """Analyze revenue"""
        logger.info("Analyzing revenue...")
        
        # Analyze pipeline
        pipeline_analysis = await self.pipeline_analyzer.analyze_pipeline()
        
        # Analyze forecast
        forecast_analysis = await self.forecast_analyzer.analyze_forecast()
        
        # Analyze ARR
        arr_analysis = await self.arr_analyzer.analyze_arr()
        
        # Analyze LTV
        ltv_analysis = await self.ltv_analyzer.analyze_ltv()
        
        # Compile results
        results = {
            'pipeline': pipeline_analysis,
            'forecast': forecast_analysis,
            'arr': arr_analysis,
            'ltv': ltv_analysis,
            'analyzed_at': datetime.utcnow().isoformat()
        }
        
        logger.info("Revenue analyzed")
        
        return results

class PipelineAnalyzer:
    """Pipeline analysis specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def analyze_pipeline(self) -> Dict[str, Any]:
        """Analyze pipeline"""
        logger.info("Analyzing pipeline...")
        # Implementation would analyze pipeline
        return {}

class ForecastAnalyzer:
    """Forecast analysis specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def analyze_forecast(self) -> Dict[str, Any]:
        """Analyze forecast"""
        logger.info("Analyzing forecast...")
        # Implementation would analyze forecast
        return {}

class ARRAnalyzer:
    """ARR analysis specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def analyze_arr(self) -> Dict[str, Any]:
        """Analyze ARR"""
        logger.info("Analyzing ARR...")
        # Implementation would analyze ARR
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

---

## Tooling & Tech Stack

### RevOps Tools
- **Clari**: Revenue operations platform
- **InsightSquared**: Sales analytics
- **Aviso**: AI forecasting
- **People.ai**: Sales AI
- **Gong**: Conversation intelligence

### CRM Tools
- **Salesforce**: CRM platform
- **HubSpot**: CRM platform
- **Pipedrive**: CRM platform
- **Zoho CRM**: CRM platform

### Analytics Tools
- **Tableau**: Business intelligence
- **Power BI**: Business intelligence
- **Looker**: Business intelligence
- **Google Analytics**: Web analytics
- **Mixpanel**: Product analytics

### Automation Tools
- **Zapier**: Automation
- **Make**: Automation
- **n8n**: Automation
- **Airflow**: Workflow automation
- **Prefect**: Workflow automation

---

## Configuration Essentials

### RevOps Configuration

```yaml
# config/revops_config.yaml
revops:
  alignment:
    goals:
      enabled: true
      departments:
        - marketing
        - sales
        - customer_success
      
      metrics:
        - mrr
        - arr
        - ltv
        - cac
        - ltv_cac_ratio
        - churn_rate
        - net_retention
    
    processes:
      enabled: true
      departments:
        - marketing
        - sales
        - customer_success
      
      stages:
        - lead
        - mql
        - sql
        - opportunity
        - customer
    
    data:
      enabled: true
      sync:
        enabled: true
        frequency: "hourly"
      
      integration:
        enabled: true
        sources:
          - crm
          - marketing_automation
          - sales_intelligence
          - customer_success_platform
    
    metrics:
      enabled: true
      departments:
        - marketing
        - sales
        - customer_success
      
      shared_metrics:
        - pipeline_value
        - forecast_accuracy
        - conversion_rate
        - win_rate
        - churn_rate
        - net_retention
  
  process_alignment:
    end_to_end_process:
      enabled: true
      stages:
        - name: "lead"
          department: "marketing"
          owner: "marketing_manager"
        - name: "mql"
          department: "marketing"
          owner: "marketing_manager"
        - name: "sql"
          department: "sales"
          owner: "sales_rep"
        - name: "opportunity"
          department: "sales"
          owner: "sales_rep"
        - name: "customer"
          department: "customer_success"
          owner: "csm"
      
      transitions:
        - from: "lead"
          to: "mql"
          criteria: "lead_score > 50"
        - from: "mql"
          to: "sql"
          criteria: "sales_acceptance"
        - from: "sql"
          to: "opportunity"
          criteria: "opportunity_created"
        - from: "opportunity"
          to: "customer"
          criteria: "deal_closed_won"
    
    handoffs:
      marketing_to_sales:
        enabled: true
        criteria:
          lead_score: "> 50"
          company_size: ">"
          industry: "in target list"
        
        process:
          notify_sales_rep: true
          create_opportunity: true
          transfer_data: true
        
        sla:
          response_time: "24 hours"
          acceptance_rate: "> 80%"
      
      sales_to_success:
        enabled: true
        criteria:
          deal_closed: true
          contract_signed: true
          payment_received: true
        
        process:
          notify_success_manager: true
          create_customer: true
          transfer_data: true
          schedule_onboarding: true
        
        sla:
          onboarding_start: "24 hours"
          first_contact: "48 hours"
    
    workflows:
      lead_to_customer:
        enabled: true
        stages:
          - lead
          - mql
          - sql
          - opportunity
          - customer
        
        handoffs:
          - marketing_to_sales
          - sales_to_success
        
        automation:
          lead_scoring: true
          opportunity_creation: true
          customer_creation: true
          notifications: true
  
  analytics:
    pipeline:
      enabled: true
      metrics:
        - total_pipeline_value
        - weighted_pipeline_value
        - by_stage
        - by_sales_rep
        - by_month
      
      alerts:
        - pipeline_health
        - stage_bottlenecks
        - at_risk_deals
    
    forecast:
      enabled: true
      methods:
        - pipeline
        - trend
        - seasonal
        - ml
        - hybrid
      
      accuracy_target: 0.9
    
    arr:
      enabled: true
      metrics:
        - new_arr
        - expansion_arr
        - churn_arr
        - net_arr
      
      growth_target: 0.2
    
    ltv:
      enabled: true
      metrics:
        - ltv
        - cac
        - ltv_cac_ratio
        - payback_period
      
      ltv_cac_ratio_target: 3.0
```

---

## Code Examples

### Good: Complete RevOps Workflow

```python
# revops/workflow.py
import asyncio
import logging
from typing import Dict, Any

from revops.alignment import RevenueAligner
from revops.process import ProcessAligner
from revops.analytics import RevenueAnalyzer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_revops():
    """Run RevOps workflow"""
    logger.info("=" * 60)
    logger.info("Revenue Operations (RevOps) Workflow")
    logger.info("=" * 60)
    
    # Load configuration
    config = load_config('config/revops_config.yaml')
    
    # Step 1: Align revenue
    logger.info("\n" + "=" * 60)
    logger.info("Step 1: Aligning Revenue")
    logger.info("=" * 60)
    
    revenue_aligner = RevenueAligner(config)
    
    alignment_results = await revenue_aligner.align_revenue()
    
    logger.info("Revenue aligned")
    print_alignment_summary(alignment_results)
    
    # Step 2: Align processes
    logger.info("\n" + "=" * 60)
    logger.info("Step 2: Aligning Processes")
    logger.info("=" * 60)
    
    process_aligner = ProcessAligner(config)
    
    process_results = await process_aligner.align_processes()
    
    logger.info("Processes aligned")
    print_process_summary(process_results)
    
    # Step 3: Analyze revenue
    logger.info("\n" + "=" * 60)
    logger.info("Step 3: Analyzing Revenue")
    logger.info("=" * 60)
    
    revenue_analyzer = RevenueAnalyzer(config)
    
    analytics_results = await revenue_analyzer.analyze_revenue()
    
    logger.info("Revenue analyzed")
    print_analytics_summary(analytics_results)
    
    # Print summary
    print_summary(alignment_results, process_results, analytics_results)

def print_alignment_summary(results: Dict[str, Any]):
    """Print alignment summary"""
    print(f"\nAlignment Summary:")
    print(f"  Goals: {len(results['goals']['aligned'])} aligned")
    print(f"  Processes: {len(results['processes']['aligned'])} aligned")
    print(f"  Metrics: {len(results['metrics']['aligned'])} aligned")

def print_process_summary(results: Dict[str, Any]):
    """Print process summary"""
    print(f"\nProcess Summary:")
    print(f"  End-to-End Process: {len(results['end_to_end_process']['stages'])} stages")
    print(f"  Handoffs: {len(results['handoffs'])} defined")
    print(f"  Workflows: {len(results['workflows'])} created")

def print_analytics_summary(results: Dict[str, Any]):
    """Print analytics summary"""
    print(f"\nAnalytics Summary:")
    print(f"  Pipeline: Analyzed")
    print(f"  Forecast: Analyzed")
    print(f"  ARR: Analyzed")
    print(f"  LTV: Analyzed")

def print_summary(
    alignment_results: Dict[str, Any],
    process_results: Dict[str, Any],
    analytics_results: Dict[str, Any]
):
    """Print summary"""
    print("\n" + "=" * 60)
    print("RevOps Summary")
    print("=" * 60)
    print(f"Goals Aligned: {len(alignment_results['goals']['aligned'])}")
    print(f"Processes Aligned: {len(alignment_results['processes']['aligned'])}")
    print(f"Metrics Aligned: {len(alignment_results['metrics']['aligned'])}")
    print(f"Handoffs: {len(process_results['handoffs'])}")
    print(f"Workflows: {len(process_results['workflows'])}")

def load_config(filename: str) -> Dict[str, Any]:
    """Load configuration from file"""
    import yaml
    with open(filename, 'r') as f:
        return yaml.safe_load(f)

async def main():
    """Main entry point"""
    await run_revops()

if __name__ == "__main__":
    asyncio.run(main())
```

### Bad: Anti-pattern Example

```python
# BAD: No alignment
def bad_revops():
    # No alignment
    pass

# BAD: No process alignment
def bad_revops():
    # No process alignment
    align_revenue()

# BAD: No analytics
def bad_revops():
    # No analytics
    align_revenue()
    align_processes()

# BAD: No integration
def bad_revops():
    # No integration
    align_revenue()
    align_processes()
    analyze_revenue()
```

---

## Standards, Compliance & Security

### Industry Standards
- **RevOps**: Revenue operations best practices
- **Process Alignment**: Process alignment best practices
- **Data Integration**: Data integration best practices
- **Metrics**: Metrics best practices
- **Forecasting**: Forecasting best practices

### Security Best Practices
- **Data Protection**: Protect revenue data
- **Access Control**: RBAC for revenue data
- **Audit Logging**: Log all revenue activities
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

### 2. Configure RevOps

```bash
# Copy example config
cp config/revops_config.yaml.example config/revops_config.yaml

# Edit configuration
vim config/revops_config.yaml
```

### 3. Run RevOps

```bash
python revops/workflow.py
```

### 4. View Results

```bash
# View alignment results
cat revops/results/alignment.json

# View process results
cat revops/results/processes.json

# View analytics results
cat revops/results/analytics.json
```

---

## Production Checklist

### Alignment
- [ ] Goals aligned across departments
- [ ] Processes aligned across departments
- [ ] Data integrated across departments
- [ ] Metrics aligned across departments
- [ ] Shared KPIs defined
- [ ] Reporting cadence established

### Process Alignment
- [ ] End-to-end process mapped
- [ ] Handoffs defined
- [ ] Workflows created
- [ ] SLAs defined
- [ ] Automation configured
- [ ] Monitoring enabled

### Data Integration
- [ ] Data sources integrated
- [ ] Data sync configured
- [ ] Data quality validated
- [ ] Data governance defined
- [ ] Data lineage documented
- [ ] Data access controls configured

### Analytics
- [ ] Pipeline analytics configured
- [ ] Forecast analytics configured
- [ ] ARR analytics configured
- [ ] LTV analytics configured
- [ ] Dashboards created
- [ ] Reports scheduled

### Collaboration
- [ ] Cross-functional team established
- [ ] Communication channels defined
- [ ] Meeting cadence established
- [ ] Shared tools configured
- [ ] Documentation created
- [ ] Training completed

---

## Anti-patterns

### ❌ Avoid These Practices

1. **No Alignment**
   ```python
   # BAD: No alignment
   pass
   ```

2. **No Process Alignment**
   ```python
   # BAD: No process alignment
   align_revenue()
   ```

3. **No Analytics**
   ```python
   # BAD: No analytics
   align_revenue()
   align_processes()
   ```

4. **No Integration**
   ```python
   # BAD: No integration
   align_revenue()
   align_processes()
   analyze_revenue()
   ```

### ✅ Follow These Practices

1. **Align Revenue**
   ```python
   # GOOD: Align revenue
   revenue_aligner = RevenueAligner(config)
   results = await revenue_aligner.align_revenue()
   ```

2. **Align Processes**
   ```python
   # GOOD: Align processes
   process_aligner = ProcessAligner(config)
   results = await process_aligner.align_processes()
   ```

3. **Analyze Revenue**
   ```python
   # GOOD: Analyze revenue
   revenue_analyzer = RevenueAnalyzer(config)
   results = await revenue_analyzer.analyze_revenue()
   ```

4. **Integrate Everything**
   ```python
   # GOOD: Integrate everything
   revenue_aligner = RevenueAligner(config)
   process_aligner = ProcessAligner(config)
   revenue_analyzer = RevenueAnalyzer(config)
   ```

---

## Unit Economics & KPIs

### Development Costs
- **Initial Setup**: 20-40 hours
- **Alignment**: 20-40 hours
- **Process Alignment**: 20-40 hours
- **Analytics**: 20-40 hours
- **Total**: 80-160 hours

### Operational Costs
- **RevOps Tools**: $200-1000/month
- **CRM Tools**: $100-500/month
- **Analytics Tools**: $100-300/month
- **Automation Tools**: $50-200/month

### ROI Metrics
- **Alignment**: 50-70% improvement
- **Process Efficiency**: 40-60% improvement
- **Forecast Accuracy**: 30-50% improvement
- **Revenue Growth**: 20-40% improvement

### KPI Targets
- **Alignment Score**: > 80%
- **Process Efficiency**: > 90%
- **Forecast Accuracy**: > 90%
- **Pipeline Coverage**: > 3x
- **ARR Growth**: > 20%
- **Net Retention**: > 100%
- **LTV:CAC Ratio**: > 3.0

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
- [RevOps Guide](https://www.clari.com/)
- [Revenue Operations Framework](https://www.insightsquared.com/)
- [Process Alignment Guide](https://www.hubspot.com/)
- [Revenue Analytics Guide](https://www.salesforce.com/)

### Best Practices
- [RevOps Best Practices](https://www.clari.com/)
- [Revenue Operations](https://www.aviso.com/)
- [Process Alignment](https://www.people.ai/)
- [Revenue Analytics](https://www.gong.io/)

### Tools & Libraries
- [Clari](https://www.clari.com/)
- [InsightSquared](https://www.insightsquared.com/)
- [Aviso](https://www.aviso.com/)
- [People.ai](https://www.people.ai/)
- [Gong](https://www.gong.io/)
- [Salesforce](https://www.salesforce.com/)
- [HubSpot](https://www.hubspot.com/)
- [Tableau](https://www.tableau.com/)
- [Power BI](https://powerbi.microsoft.com/)
