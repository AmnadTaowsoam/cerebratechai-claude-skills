---
name: Technical Debt Prioritization
description: Identifying, measuring, and prioritizing technical debt for systematic remediation
---

# Technical Debt Prioritization

## Current Level: Expert (Enterprise Scale)

## Domain: Technical Product Management
## Skill ID: 142

---

## Executive Summary

Technical Debt Prioritization enables systematic identification, measurement, and prioritization of technical debt for efficient remediation. This capability is essential for maintaining code quality, reducing maintenance costs, preventing accumulated debt, and ensuring long-term sustainability.

### Strategic Necessity

- **Code Quality**: Maintain high code quality standards
- **Maintenance Efficiency**: Reduce time spent on maintenance
- **Development Velocity**: Prevent debt from slowing development
- **Risk Mitigation**: Reduce risk of outages and bugs
- **Cost Optimization**: Reduce long-term maintenance costs

---

## Technical Deep Dive

### Technical Debt Framework

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Technical Debt Prioritization Framework                 │
│                                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│  │   Debt       │    │   Debt       │    │   Debt       │                  │
│  │   Discovery  │───▶│   Measurement│───▶│   Prioritization│                  │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘                  │
│         │                   │                   │                           │
│         ▼                   ▼                   ▼                           │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Debt Analysis Methods                           │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Code     │  │  Static   │  │  Runtime  │  │  Manual   │            │   │
│  │  │  Review   │  │  Analysis │  │  Metrics  │  │  Assessment│            │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘            │   │
│  └───────┼────────────┼────────────┼────────────┼────────────────────┘   │
│          │            │            │            │                         │
│          ▼            ▼            ▼            ▼                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Debt Scoring                                    │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Impact   │  │  Urgency  │  │  Effort   │  │  Risk     │            │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘            │   │
│  └───────┼────────────┼────────────┼────────────┼────────────────────┘   │
│          │            │            │            │                         │
│          ▼            ▼            ▼            ▼                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Remediation Planning                            │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Priority│  │  Roadmap  │  │  Resource │  │  Tracking │            │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Debt Discovery

```python
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import asyncio
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

class DebtType(Enum):
    """Types of technical debt"""
    CODE_QUALITY = "code_quality"
    ARCHITECTURE = "architecture"
    DEPENDENCIES = "dependencies"
    DOCUMENTATION = "documentation"
    TESTING = "testing"
    PERFORMANCE = "performance"
    SECURITY = "security"
    INFRASTRUCTURE = "infrastructure"

class DebtSeverity(Enum):
    """Debt severity levels"""
    CRITICAL = 4
    HIGH = 3
    MEDIUM = 2
    LOW = 1

@dataclass
class TechnicalDebt:
    """Technical debt item"""
    debt_id: str
    name: str
    description: str
    debt_type: DebtType
    severity: DebtSeverity
    location: str  # File, module, or component
    impact: float  # 0-10
    urgency: float  # 0-10
    effort: int  # Person-hours
    risk: float  # 0-10
    created_at: str
    updated_at: str
    status: str  # open, in_progress, resolved

class DebtDiscoverer:
    """Technical debt discovery specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.code_analyzer = CodeAnalyzer(config['code_analysis'])
        self.static_analyzer = StaticAnalyzer(config['static_analysis'])
        self.runtime_analyzer = RuntimeAnalyzer(config['runtime_analysis'])
        self.manual_assessor = ManualAssessor(config['manual_assessment'])
        
    async def discover_debt(
        self,
        project_path: str,
        discovery_methods: List[str] = None
    ) -> List[TechnicalDebt]:
        """Discover technical debt in project"""
        logger.info(f"Discovering technical debt in {project_path}...")
        
        if discovery_methods is None:
            discovery_methods = ['code_review', 'static_analysis', 'runtime_metrics', 'manual']
        
        discovered_debt = []
        
        # Code review
        if 'code_review' in discovery_methods:
            logger.info("Running code review...")
            code_debt = await self.code_analyzer.analyze_code(project_path)
            discovered_debt.extend(code_debt)
        
        # Static analysis
        if 'static_analysis' in discovery_methods:
            logger.info("Running static analysis...")
            static_debt = await self.static_analyzer.analyze_project(project_path)
            discovered_debt.extend(static_debt)
        
        # Runtime metrics
        if 'runtime_metrics' in discovery_methods:
            logger.info("Analyzing runtime metrics...")
            runtime_debt = await self.runtime_analyzer.analyze_runtime(project_path)
            discovered_debt.extend(runtime_debt)
        
        # Manual assessment
        if 'manual' in discovery_methods:
            logger.info("Running manual assessment...")
            manual_debt = await self.manual_assessor.assess_project(project_path)
            discovered_debt.extend(manual_debt)
        
        # Deduplicate debt items
        discovered_debt = self._deduplicate_debt(discovered_debt)
        
        logger.info(f"Discovered {len(discovered_debt)} technical debt items")
        
        return discovered_debt
    
    def _deduplicate_debt(
        self,
        debt_items: List[TechnicalDebt]
    ) -> List[TechnicalDebt]:
        """Deduplicate debt items"""
        # Group by location and type
        debt_map = {}
        
        for debt in debt_items:
            key = (debt.location, debt.debt_type)
            
            if key in debt_map:
                # Merge with existing
                existing = debt_map[key]
                existing.severity = max(existing.severity, debt.severity)
                existing.impact = max(existing.impact, debt.impact)
                existing.urgency = max(existing.urgency, debt.urgency)
                existing.risk = max(existing.risk, debt.risk)
                existing.description = f"{existing.description}\n{debt.description}"
            else:
                debt_map[key] = debt
        
        return list(debt_map.values())

class CodeAnalyzer:
    """Code analysis specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def analyze_code(
        self,
        project_path: str
    ) -> List[TechnicalDebt]:
        """Analyze code for technical debt"""
        debt_items = []
        
        # Analyze code complexity
        complexity_debt = await self._analyze_complexity(project_path)
        debt_items.extend(complexity_debt)
        
        # Analyze code duplication
        duplication_debt = await self._analyze_duplication(project_path)
        debt_items.extend(duplication_debt)
        
        # Analyze code smells
        smell_debt = await self._analyze_code_smells(project_path)
        debt_items.extend(smell_debt)
        
        return debt_items
    
    async def _analyze_complexity(
        self,
        project_path: str
    ) -> List[TechnicalDebt]:
        """Analyze code complexity"""
        debt_items = []
        
        # Calculate cyclomatic complexity
        complexity_results = await self._calculate_cyclomatic_complexity(project_path)
        
        # Identify high complexity functions
        for result in complexity_results:
            if result['complexity'] > 10:
                severity = DebtSeverity.HIGH if result['complexity'] > 20 else DebtSeverity.MEDIUM
                
                debt = TechnicalDebt(
                    debt_id=self._generate_debt_id(),
                    name=f"High Complexity: {result['function']}",
                    description=f"Function {result['function']} has cyclomatic complexity of {result['complexity']}",
                    debt_type=DebtType.CODE_QUALITY,
                    severity=severity,
                    location=result['file'],
                    impact=self._calculate_impact_from_complexity(result['complexity']),
                    urgency=self._calculate_urgency_from_complexity(result['complexity']),
                    effort=self._estimate_effort_from_complexity(result['complexity']),
                    risk=self._calculate_risk_from_complexity(result['complexity']),
                    created_at=datetime.utcnow().isoformat(),
                    updated_at=datetime.utcnow().isoformat(),
                    status="open"
                )
                debt_items.append(debt)
        
        return debt_items
    
    async def _calculate_cyclomatic_complexity(
        self,
        project_path: str
    ) -> List[Dict[str, Any]]:
        """Calculate cyclomatic complexity"""
        # Implementation would use tools like radon or lizard
        return []
    
    def _calculate_impact_from_complexity(self, complexity: int) -> float:
        """Calculate impact from complexity"""
        # Higher complexity = higher impact
        return min(10.0, complexity / 2)
    
    def _calculate_urgency_from_complexity(self, complexity: int) -> float:
        """Calculate urgency from complexity"""
        # Higher complexity = higher urgency
        return min(10.0, complexity / 3)
    
    def _estimate_effort_from_complexity(self, complexity: int) -> int:
        """Estimate effort from complexity"""
        # Higher complexity = more effort
        return complexity * 2  # hours
    
    def _calculate_risk_from_complexity(self, complexity: int) -> float:
        """Calculate risk from complexity"""
        # Higher complexity = higher risk
        return min(10.0, complexity / 2)
    
    async def _analyze_duplication(
        self,
        project_path: str
    ) -> List[TechnicalDebt]:
        """Analyze code duplication"""
        debt_items = []
        
        # Find duplicate code
        duplicates = await self._find_duplicates(project_path)
        
        for duplicate in duplicates:
            severity = DebtSeverity.HIGH if duplicate['similarity'] > 0.8 else DebtSeverity.MEDIUM
            
            debt = TechnicalDebt(
                debt_id=self._generate_debt_id(),
                name=f"Code Duplication: {duplicate['name']}",
                description=f"Duplicate code found with {duplicate['similarity']:.0%} similarity",
                debt_type=DebtType.CODE_QUALITY,
                severity=severity,
                location=duplicate['files'][0],
                impact=duplicate['similarity'] * 10,
                urgency=duplicate['similarity'] * 5,
                effort=len(duplicate['files']) * 2,  # hours
                risk=duplicate['similarity'] * 5,
                created_at=datetime.utcnow().isoformat(),
                updated_at=datetime.utcnow().isoformat(),
                status="open"
            )
            debt_items.append(debt)
        
        return debt_items
    
    async def _find_duplicates(
        self,
        project_path: str
    ) -> List[Dict[str, Any]]:
        """Find duplicate code"""
        # Implementation would use tools like jscpd or duplicate-code-detection-tool
        return []
    
    async def _analyze_code_smells(
        self,
        project_path: str
    ) -> List[TechnicalDebt]:
        """Analyze code smells"""
        debt_items = []
        
        # Find code smells
        smells = await self._find_code_smells(project_path)
        
        for smell in smells:
            severity = DebtSeverity.HIGH if smell['severity'] == 'critical' else DebtSeverity.MEDIUM
            
            debt = TechnicalDebt(
                debt_id=self._generate_debt_id(),
                name=f"Code Smell: {smell['name']}",
                description=smell['description'],
                debt_type=DebtType.CODE_QUALITY,
                severity=severity,
                location=smell['file'],
                impact=smell['impact'],
                urgency=smell['urgency'],
                effort=smell['effort'],
                risk=smell['risk'],
                created_at=datetime.utcnow().isoformat(),
                updated_at=datetime.utcnow().isoformat(),
                status="open"
            )
            debt_items.append(debt)
        
        return debt_items
    
    async def _find_code_smells(
        self,
        project_path: str
    ) -> List[Dict[str, Any]]:
        """Find code smells"""
        # Implementation would use tools like SonarQube or ESLint
        return []
    
    def _generate_debt_id(self) -> str:
        """Generate unique debt ID"""
        import uuid
        return f"debt_{uuid.uuid4().hex}"

class StaticAnalyzer:
    """Static analysis specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def analyze_project(
        self,
        project_path: str
    ) -> List[TechnicalDebt]:
        """Analyze project with static analysis"""
        debt_items = []
        
        # Analyze dependencies
        dependency_debt = await self._analyze_dependencies(project_path)
        debt_items.extend(dependency_debt)
        
        # Analyze security issues
        security_debt = await self._analyze_security(project_path)
        debt_items.extend(security_debt)
        
        # Analyze test coverage
        testing_debt = await self._analyze_test_coverage(project_path)
        debt_items.extend(testing_debt)
        
        return debt_items
    
    async def _analyze_dependencies(
        self,
        project_path: str
    ) -> List[TechnicalDebt]:
        """Analyze dependencies for debt"""
        debt_items = []
        
        # Find outdated dependencies
        outdated = await self._find_outdated_dependencies(project_path)
        
        for dep in outdated:
            severity = DebtSeverity.HIGH if dep['outdated_by'] > 2 else DebtSeverity.MEDIUM
            
            debt = TechnicalDebt(
                debt_id=self._generate_debt_id(),
                name=f"Outdated Dependency: {dep['name']}",
                description=f"Dependency {dep['name']} is outdated by {dep['outdated_by']} versions",
                debt_type=DebtType.DEPENDENCIES,
                severity=severity,
                location=dep['file'],
                impact=dep['security_impact'] * 10,
                urgency=dep['security_impact'] * 8,
                effort=2,  # hours
                risk=dep['security_impact'] * 10,
                created_at=datetime.utcnow().isoformat(),
                updated_at=datetime.utcnow().isoformat(),
                status="open"
            )
            debt_items.append(debt)
        
        return debt_items
    
    async def _find_outdated_dependencies(
        self,
        project_path: str
    ) -> List[Dict[str, Any]]:
        """Find outdated dependencies"""
        # Implementation would use tools like npm outdated or pip outdated
        return []
    
    async def _analyze_security(
        self,
        project_path: str
    ) -> List[TechnicalDebt]:
        """Analyze security issues"""
        debt_items = []
        
        # Find security vulnerabilities
        vulnerabilities = await self._find_vulnerabilities(project_path)
        
        for vuln in vulnerabilities:
            severity = DebtSeverity.CRITICAL if vuln['severity'] == 'critical' else DebtSeverity.HIGH
            
            debt = TechnicalDebt(
                debt_id=self._generate_debt_id(),
                name=f"Security Vulnerability: {vuln['name']}",
                description=vuln['description'],
                debt_type=DebtType.SECURITY,
                severity=severity,
                location=vuln['file'],
                impact=10.0,
                urgency=10.0,
                effort=vuln['effort'],
                risk=10.0,
                created_at=datetime.utcnow().isoformat(),
                updated_at=datetime.utcnow().isoformat(),
                status="open"
            )
            debt_items.append(debt)
        
        return debt_items
    
    async def _find_vulnerabilities(
        self,
        project_path: str
    ) -> List[Dict[str, Any]]:
        """Find security vulnerabilities"""
        # Implementation would use tools like Snyk or OWASP Dependency-Check
        return []
    
    async def _analyze_test_coverage(
        self,
        project_path: str
    ) -> List[TechnicalDebt]:
        """Analyze test coverage"""
        debt_items = []
        
        # Get test coverage
        coverage = await self._get_test_coverage(project_path)
        
        # Identify low coverage areas
        for area in coverage['low_coverage_areas']:
            severity = DebtSeverity.HIGH if area['coverage'] < 50 else DebtSeverity.MEDIUM
            
            debt = TechnicalDebt(
                debt_id=self._generate_debt_id(),
                name=f"Low Test Coverage: {area['name']}",
                description=f"Test coverage is {area['coverage']:.1f}%",
                debt_type=DebtType.TESTING,
                severity=severity,
                location=area['file'],
                impact=(100 - area['coverage']) / 10,
                urgency=(100 - area['coverage']) / 10,
                effort=area['size'] * 2,  # hours
                risk=(100 - area['coverage']) / 10,
                created_at=datetime.utcnow().isoformat(),
                updated_at=datetime.utcnow().isoformat(),
                status="open"
            )
            debt_items.append(debt)
        
        return debt_items
    
    async def _get_test_coverage(
        self,
        project_path: str
    ) -> Dict[str, Any]:
        """Get test coverage"""
        # Implementation would use tools like coverage.py or Jest
        return {}
    
    def _generate_debt_id(self) -> str:
        """Generate unique debt ID"""
        import uuid
        return f"debt_{uuid.uuid4().hex}"

class RuntimeAnalyzer:
    """Runtime analysis specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def analyze_runtime(
        self,
        project_path: str
    ) -> List[TechnicalDebt]:
        """Analyze runtime metrics for debt"""
        debt_items = []
        
        # Analyze performance
        performance_debt = await self._analyze_performance(project_path)
        debt_items.extend(performance_debt)
        
        # Analyze error rates
        error_debt = await self._analyze_errors(project_path)
        debt_items.extend(error_debt)
        
        return debt_items
    
    async def _analyze_performance(
        self,
        project_path: str
    ) -> List[TechnicalDebt]:
        """Analyze performance issues"""
        debt_items = []
        
        # Get performance metrics
        metrics = await self._get_performance_metrics(project_path)
        
        # Identify slow endpoints
        for endpoint in metrics['slow_endpoints']:
            severity = DebtSeverity.HIGH if endpoint['latency'] > 1000 else DebtSeverity.MEDIUM
            
            debt = TechnicalDebt(
                debt_id=self._generate_debt_id(),
                name=f"Performance Issue: {endpoint['name']}",
                description=f"Endpoint latency is {endpoint['latency']}ms",
                debt_type=DebtType.PERFORMANCE,
                severity=severity,
                location=endpoint['file'],
                impact=endpoint['latency'] / 100,
                urgency=endpoint['latency'] / 100,
                effort=endpoint['effort'],
                risk=endpoint['latency'] / 100,
                created_at=datetime.utcnow().isoformat(),
                updated_at=datetime.utcnow().isoformat(),
                status="open"
            )
            debt_items.append(debt)
        
        return debt_items
    
    async def _get_performance_metrics(
        self,
        project_path: str
    ) -> Dict[str, Any]:
        """Get performance metrics"""
        # Implementation would use tools like New Relic or Datadog
        return {}
    
    async def _analyze_errors(
        self,
        project_path: str
    ) -> List[TechnicalDebt]:
        """Analyze error rates"""
        debt_items = []
        
        # Get error metrics
        metrics = await self._get_error_metrics(project_path)
        
        # Identify high error areas
        for area in metrics['high_error_areas']:
            severity = DebtSeverity.CRITICAL if area['error_rate'] > 0.05 else DebtSeverity.HIGH
            
            debt = TechnicalDebt(
                debt_id=self._generate_debt_id(),
                name=f"High Error Rate: {area['name']}",
                description=f"Error rate is {area['error_rate']:.2%}",
                debt_type=DebtType.CODE_QUALITY,
                severity=severity,
                location=area['file'],
                impact=area['error_rate'] * 100,
                urgency=area['error_rate'] * 100,
                effort=area['effort'],
                risk=area['error_rate'] * 100,
                created_at=datetime.utcnow().isoformat(),
                updated_at=datetime.utcnow().isoformat(),
                status="open"
            )
            debt_items.append(debt)
        
        return debt_items
    
    async def _get_error_metrics(
        self,
        project_path: str
    ) -> Dict[str, Any]:
        """Get error metrics"""
        # Implementation would use tools like Sentry or Rollbar
        return {}
    
    def _generate_debt_id(self) -> str:
        """Generate unique debt ID"""
        import uuid
        return f"debt_{uuid.uuid4().hex}"

class ManualAssessor:
    """Manual assessment specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def assess_project(
        self,
        project_path: str
    ) -> List[TechnicalDebt]:
        """Assess project manually"""
        debt_items = []
        
        # Collect team feedback
        feedback = await self._collect_team_feedback(project_path)
        
        # Analyze architecture
        architecture_debt = await self._assess_architecture(project_path, feedback)
        debt_items.extend(architecture_debt)
        
        # Analyze documentation
        documentation_debt = await self._assess_documentation(project_path, feedback)
        debt_items.extend(documentation_debt)
        
        return debt_items
    
    async def _collect_team_feedback(
        self,
        project_path: str
    ) -> Dict[str, Any]:
        """Collect team feedback"""
        # Implementation would survey team members
        return {}
    
    async def _assess_architecture(
        self,
        project_path: str,
        feedback: Dict[str, Any]
    ) -> List[TechnicalDebt]:
        """Assess architecture for debt"""
        debt_items = []
        
        # Identify architectural issues
        issues = await self._identify_architectural_issues(project_path, feedback)
        
        for issue in issues:
            severity = DebtSeverity.HIGH if issue['impact'] > 7 else DebtSeverity.MEDIUM
            
            debt = TechnicalDebt(
                debt_id=self._generate_debt_id(),
                name=f"Architectural Issue: {issue['name']}",
                description=issue['description'],
                debt_type=DebtType.ARCHITECTURE,
                severity=severity,
                location=issue['component'],
                impact=issue['impact'],
                urgency=issue['urgency'],
                effort=issue['effort'],
                risk=issue['risk'],
                created_at=datetime.utcnow().isoformat(),
                updated_at=datetime.utcnow().isoformat(),
                status="open"
            )
            debt_items.append(debt)
        
        return debt_items
    
    async def _identify_architectural_issues(
        self,
        project_path: str,
        feedback: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Identify architectural issues"""
        # Implementation would analyze architecture
        return []
    
    async def _assess_documentation(
        self,
        project_path: str,
        feedback: Dict[str, Any]
    ) -> List[TechnicalDebt]:
        """Assess documentation for debt"""
        debt_items = []
        
        # Identify documentation gaps
        gaps = await self._identify_documentation_gaps(project_path, feedback)
        
        for gap in gaps:
            severity = DebtSeverity.MEDIUM
            
            debt = TechnicalDebt(
                debt_id=self._generate_debt_id(),
                name=f"Documentation Gap: {gap['name']}",
                description=gap['description'],
                debt_type=DebtType.DOCUMENTATION,
                severity=severity,
                location=gap['file'],
                impact=gap['impact'],
                urgency=gap['urgency'],
                effort=gap['effort'],
                risk=gap['risk'],
                created_at=datetime.utcnow().isoformat(),
                updated_at=datetime.utcnow().isoformat(),
                status="open"
            )
            debt_items.append(debt)
        
        return debt_items
    
    async def _identify_documentation_gaps(
        self,
        project_path: str,
        feedback: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Identify documentation gaps"""
        # Implementation would analyze documentation
        return []
    
    def _generate_debt_id(self) -> str:
        """Generate unique debt ID"""
        import uuid
        return f"debt_{uuid.uuid4().hex}"
```

### Debt Prioritization

```python
class DebtPrioritizer:
    """Technical debt prioritization specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.debt_store = DebtStore(config['debt_store'])
        
    async def prioritize_debt(
        self,
        debt_items: List[TechnicalDebt],
        framework: str = "weighted"
    ) -> List[TechnicalDebt]:
        """Prioritize technical debt items"""
        logger.info(f"Prioritizing {len(debt_items)} debt items using {framework} framework...")
        
        # Calculate scores
        for debt in debt_items:
            debt.score = self._calculate_debt_score(debt, framework)
        
        # Sort by score
        debt_items.sort(key=lambda d: d.score, reverse=True)
        
        # Assign ranks
        for i, debt in enumerate(debt_items):
            debt.rank = i + 1
        
        logger.info(f"Prioritized {len(debt_items)} debt items")
        
        return debt_items
    
    def _calculate_debt_score(
        self,
        debt: TechnicalDebt,
        framework: str
    ) -> float:
        """Calculate debt score"""
        if framework == "weighted":
            return self._calculate_weighted_score(debt)
        elif framework == "risk_based":
            return self._calculate_risk_based_score(debt)
        elif framework == "impact_effort":
            return self._calculate_impact_effort_score(debt)
        else:
            raise ValueError(f"Unknown framework: {framework}")
    
    def _calculate_weighted_score(self, debt: TechnicalDebt) -> float:
        """Calculate weighted score"""
        # Weighted sum of impact, urgency, risk
        weights = self.config.get('weights', {
            'impact': 0.4,
            'urgency': 0.3,
            'risk': 0.3
        })
        
        score = (
            debt.impact * weights['impact'] +
            debt.urgency * weights['urgency'] +
            debt.risk * weights['risk']
        )
        
        # Adjust for effort (higher effort = lower score)
        score = score / (debt.effort ** 0.5)
        
        return score
    
    def _calculate_risk_based_score(self, debt: TechnicalDebt) -> float:
        """Calculate risk-based score"""
        # Focus on risk
        score = debt.risk * 10
        
        # Adjust for severity
        score *= debt.severity.value
        
        # Adjust for effort
        score = score / (debt.effort ** 0.5)
        
        return score
    
    def _calculate_impact_effort_score(self, debt: TechnicalDebt) -> float:
        """Calculate impact/effort score"""
        # Impact to effort ratio
        score = debt.impact / debt.effort if debt.effort > 0 else 0
        
        # Adjust for urgency
        score *= (1 + debt.urgency / 10)
        
        # Adjust for risk
        score *= (1 + debt.risk / 10)
        
        return score
    
    async def create_remediation_plan(
        self,
        prioritized_debt: List[TechnicalDebt],
        capacity: Dict[str, int]
    ) -> Dict[str, Any]:
        """Create remediation plan from prioritized debt"""
        logger.info("Creating remediation plan...")
        
        # Calculate capacity
        total_capacity = capacity.get('total_hours', 0)
        available_capacity = total_capacity
        
        # Allocate debt to plan
        plan = {
            'total_debt': len(prioritized_debt),
            'planned_debt': 0,
            'total_effort': 0,
            'remaining_capacity': total_capacity,
            'items': []
        }
        
        for debt in prioritized_debt:
            # Check if debt fits in capacity
            if debt.effort <= available_capacity:
                plan['items'].append({
                    'debt_id': debt.debt_id,
                    'name': debt.name,
                    'score': debt.score,
                    'rank': debt.rank,
                    'effort': debt.effort,
                    'severity': debt.severity.value
                })
                plan['planned_debt'] += 1
                plan['total_effort'] += debt.effort
                available_capacity -= debt.effort
        
        plan['remaining_capacity'] = available_capacity
        
        logger.info(f"Remediation plan created: {plan['planned_debt']} items")
        
        return plan

class DebtStore:
    """Technical debt storage specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def store_debt(self, debt: TechnicalDebt):
        """Store debt item"""
        # Implementation would store in database
        pass
    
    async def get_debt(
        self,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[TechnicalDebt]:
        """Get debt items with filters"""
        # Implementation would query database
        return []
    
    async def update_debt(self, debt: TechnicalDebt):
        """Update debt item"""
        # Implementation would update database
        pass
    
    async def delete_debt(self, debt_id: str):
        """Delete debt item"""
        # Implementation would delete from database
        pass
```

---

## Tooling & Tech Stack

### Code Analysis Tools
- **SonarQube**: Code quality and security analysis
- **ESLint**: JavaScript linting
- **Pylint**: Python linting
- **RuboCop**: Ruby linting
- **Checkstyle**: Java code style checker

### Static Analysis Tools
- **Snyk**: Security vulnerability scanning
- **OWASP Dependency-Check**: Dependency vulnerability scanning
- **npm audit**: Node.js dependency audit
- **pip-audit**: Python dependency audit
- **Maven**: Java dependency management

### Runtime Analysis Tools
- **New Relic**: Application performance monitoring
- **Datadog**: Infrastructure and application monitoring
- **Sentry**: Error tracking
- **Rollbar**: Error tracking
- **Prometheus**: Metrics collection

### Documentation Tools
- **Sphinx**: Python documentation
- **Javadoc**: Java documentation
- **Doxygen**: Multi-language documentation
- **Swagger**: API documentation
- **MkDocs**: Static site generator

---

## Configuration Essentials

### Debt Discovery Configuration

```yaml
# config/debt_discovery_config.yaml
debt_discovery:
  project_path: "./src"
  
  discovery_methods:
    - code_review
    - static_analysis
    - runtime_metrics
    - manual
  
  code_analysis:
    enabled: true
    tools:
      - sonarqube
      - eslint
      - pylint
    
    complexity:
      enabled: true
      threshold:
        medium: 10
        high: 20
    
    duplication:
      enabled: true
      threshold:
        medium: 0.5
        high: 0.8
    
    code_smells:
      enabled: true
      severity:
        - critical
        - high
        - medium
  
  static_analysis:
    enabled: true
    tools:
      - snyk
      - owasp_dependency_check
      - npm_audit
      - pip_audit
    
    dependencies:
      enabled: true
      outdated_threshold: 2
      security_impact: true
    
    security:
      enabled: true
      severity:
        - critical
        - high
        - medium
    
    test_coverage:
      enabled: true
      threshold:
        medium: 70
        high: 50
  
  runtime_analysis:
    enabled: true
    tools:
      - new_relic
      - datadog
      - sentry
    
    performance:
      enabled: true
      threshold:
        medium: 500  # ms
        high: 1000  # ms
    
    errors:
      enabled: true
      threshold:
        medium: 0.01  # 1%
        high: 0.05  # 5%
  
  manual_assessment:
    enabled: true
    team_survey: true
    architecture_review: true
    documentation_review: true
```

### Debt Prioritization Configuration

```yaml
# config/debt_prioritization_config.yaml
debt_prioritization:
  framework: "weighted"  # weighted, risk_based, impact_effort
  
  weights:
    impact: 0.4
    urgency: 0.3
    risk: 0.3
  
  severity_weights:
    critical: 4.0
    high: 3.0
    medium: 2.0
    low: 1.0
  
  debt_types:
    code_quality:
      weight: 1.0
    
    architecture:
      weight: 1.2
    
    dependencies:
      weight: 0.8
    
    documentation:
      weight: 0.6
    
    testing:
      weight: 0.9
    
    performance:
      weight: 1.1
    
    security:
      weight: 1.5
    
    infrastructure:
      weight: 1.0
  
  remediation:
    capacity:
      total_hours: 40  # per sprint
      team_size: 4
      sprint_length: 2  # weeks
    
    allocation:
      new_features: 0.6
      technical_debt: 0.3
      bug_fixes: 0.1
    
    thresholds:
      high_priority: 75.0
      medium_priority: 50.0
      low_priority: 25.0
```

---

## Code Examples

### Good: Complete Debt Prioritization Workflow

```python
# debt_prioritization/workflow.py
import asyncio
import logging
from typing import Dict, Any

from debt_prioritization.discoverer import DebtDiscoverer
from debt_prioritization.prioritizer import DebtPrioritizer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_debt_prioritization():
    """Run technical debt prioritization workflow"""
    logger.info("=" * 60)
    logger.info("Technical Debt Prioritization Workflow")
    logger.info("=" * 60)
    
    # Load configuration
    config = load_config('config/debt_discovery_config.yaml')
    
    # Step 1: Discover technical debt
    logger.info("\n" + "=" * 60)
    logger.info("Step 1: Discovering Technical Debt")
    logger.info("=" * 60)
    
    discoverer = DebtDiscoverer(config)
    debt_items = await discoverer.discover_debt(
        project_path=config['debt_discovery']['project_path']
    )
    
    logger.info(f"Discovered {len(debt_items)} technical debt items")
    
    # Step 2: Analyze debt distribution
    logger.info("\n" + "=" * 60)
    logger.info("Step 2: Analyzing Debt Distribution")
    logger.info("=" * 60)
    
    debt_analysis = analyze_debt_distribution(debt_items)
    
    print_debt_analysis(debt_analysis)
    
    # Step 3: Prioritize debt
    logger.info("\n" + "=" * 60)
    logger.info("Step 3: Prioritizing Technical Debt")
    logger.info("=" * 60)
    
    prioritizer_config = load_config('config/debt_prioritization_config.yaml')
    prioritizer = DebtPrioritizer(prioritizer_config)
    
    prioritized_debt = await prioritizer.prioritize_debt(
        debt_items,
        framework=prioritizer_config['debt_prioritization']['framework']
    )
    
    logger.info(f"Prioritized {len(prioritized_debt)} debt items")
    print_top_debt(prioritized_debt[:10])
    
    # Step 4: Create remediation plan
    logger.info("\n" + "=" * 60)
    logger.info("Step 4: Creating Remediation Plan")
    logger.info("=" * 60)
    
    remediation_plan = await prioritizer.create_remediation_plan(
        prioritized_debt,
        capacity=prioritizer_config['debt_prioritization']['remediation']['capacity']
    )
    
    logger.info(f"Remediation plan created: {remediation_plan['planned_debt']} items")
    print_remediation_plan(remediation_plan)
    
    # Print summary
    print_summary(debt_items, prioritized_debt, remediation_plan, debt_analysis)

def analyze_debt_distribution(debt_items: list) -> Dict[str, Any]:
    """Analyze debt distribution"""
    from collections import Counter
    
    analysis = {
        'total_debt': len(debt_items),
        'by_type': Counter(d.debt_type.value for d in debt_items),
        'by_severity': Counter(d.severity.value for d in debt_items),
        'total_effort': sum(d.effort for d in debt_items),
        'avg_effort': sum(d.effort for d in debt_items) / len(debt_items) if debt_items else 0
    }
    
    return analysis

def print_debt_analysis(analysis: Dict[str, Any]):
    """Print debt analysis"""
    print(f"\nDebt Distribution:")
    print(f"  Total Debt Items: {analysis['total_debt']}")
    print(f"  Total Effort: {analysis['total_effort']} hours")
    print(f"  Average Effort: {analysis['avg_effort']:.1f} hours")
    print(f"\n  By Type:")
    for debt_type, count in analysis['by_type'].items():
        print(f"    {debt_type}: {count}")
    print(f"\n  By Severity:")
    for severity, count in analysis['by_severity'].items():
        print(f"    {severity}: {count}")

def print_top_debt(debt_items: list):
    """Print top debt items"""
    print(f"\nTop 10 Technical Debt Items:")
    print("-" * 60)
    for i, debt in enumerate(debt_items, 1):
        print(f"{i}. {debt.name} (Score: {debt.score:.2f})")
        print(f"   Type: {debt.debt_type.value}, Severity: {debt.severity.value}")
        print(f"   Impact: {debt.impact:.1f}, Urgency: {debt.urgency:.1f}, Risk: {debt.risk:.1f}")
        print(f"   Effort: {debt.effort} hours, Location: {debt.location}")

def print_remediation_plan(plan: Dict[str, Any]):
    """Print remediation plan"""
    print(f"\nRemediation Plan:")
    print(f"  Total Debt: {plan['total_debt']}")
    print(f"  Planned Debt: {plan['planned_debt']}")
    print(f"  Total Effort: {plan['total_effort']} hours")
    print(f"  Remaining Capacity: {plan['remaining_capacity']} hours")
    print(f"\n  Planned Items:")
    for i, item in enumerate(plan['items'][:10], 1):
        print(f"    {i}. {item['name']} (Rank: {item['rank']}, Effort: {item['effort']}h)")

def print_summary(
    debt_items: list,
    prioritized_debt: list,
    remediation_plan: Dict[str, Any],
    debt_analysis: Dict[str, Any]
):
    """Print summary"""
    print("\n" + "=" * 60)
    print("Technical Debt Prioritization Summary")
    print("=" * 60)
    print(f"Total Debt Items: {len(debt_items)}")
    print(f"Total Effort: {debt_analysis['total_effort']} hours")
    print(f"Average Effort: {debt_analysis['avg_effort']:.1f} hours")
    print(f"\nRemediation Plan:")
    print(f"  Planned Items: {remediation_plan['planned_debt']}")
    print(f"  Total Effort: {remediation_plan['total_effort']} hours")
    print(f"  Remaining Capacity: {remediation_plan['remaining_capacity']} hours")

def load_config(filename: str) -> Dict[str, Any]:
    """Load configuration from file"""
    import yaml
    with open(filename, 'r') as f:
        return yaml.safe_load(f)

async def main():
    """Main entry point"""
    await run_debt_prioritization()

if __name__ == "__main__":
    asyncio.run(main())
```

### Bad: Anti-pattern Example

```python
# BAD: No discovery
def bad_debt_prioritization():
    # No debt discovery
    pass

# BAD: No measurement
def bad_debt_prioritization():
    # No debt measurement
    guess_debt()

# BAD: No prioritization
def bad_debt_prioritization():
    # Random prioritization
    random.shuffle(debt_items)

# BAD: No remediation
def bad_debt_prioritization():
    # No remediation plan
    ignore_debt()

# BAD: No tracking
def bad_debt_prioritization():
    # No tracking
    fix_and_forget()
```

---

## Standards, Compliance & Security

### Industry Standards
- **Code Quality**: Code quality best practices
- **Static Analysis**: Static analysis standards
- **Security**: Security best practices
- **Documentation**: Documentation standards

### Security Best Practices
- **Vulnerability Scanning**: Regular vulnerability scanning
- **Dependency Management**: Keep dependencies up to date
- **Code Review**: Mandatory code reviews
- **Security Testing**: Regular security testing

### Compliance Requirements
- **OWASP**: OWASP security standards
- **GDPR**: Data protection compliance
- **SOC 2**: Security and availability
- **ISO 27001**: Information security

---

## Quick Start

### 1. Install Dependencies

```bash
pip install pyyaml
pip install radon
pip install pylint
```

### 2. Configure Debt Discovery

```bash
# Copy example config
cp config/debt_discovery_config.yaml.example config/debt_discovery_config.yaml

# Edit configuration
vim config/debt_discovery_config.yaml
```

### 3. Run Debt Discovery

```bash
python debt_prioritization/workflow.py
```

### 4. View Results

```bash
# View discovered debt
cat debt_prioritization/results/discovered_debt.json

# View remediation plan
cat debt_prioritization/results/remediation_plan.json
```

---

## Production Checklist

### Discovery
- [ ] Code analysis configured
- [ ] Static analysis configured
- [ ] Runtime analysis configured
- [ ] Manual assessment configured
- [ ] Discovery scheduled

### Measurement
- [ ] Metrics defined
- [ ] Thresholds configured
- [ ] Scoring framework defined
- [ ] Weights configured
- [ ] Validation completed

### Prioritization
- [ ] Framework selected
- [ ] Scores calculated
- [ ] Results validated
- [ ] Stakeholders informed
- [ ] Plan created

### Remediation
- [ ] Capacity allocated
- [ ] Items scheduled
- [ ] Progress tracked
- [ ] Results measured
- [ ] Feedback collected

### Tracking
- [ ] Dashboard configured
- [ ] Alerts configured
- [ ] Reports scheduled
- [ ] Review meetings scheduled
- [ ] Continuous improvement

---

## Anti-patterns

### ❌ Avoid These Practices

1. **No Discovery**
   ```python
   # BAD: No discovery
   pass
   ```

2. **No Measurement**
   ```python
   # BAD: No measurement
   guess_debt()
   ```

3. **No Prioritization**
   ```python
   # BAD: No prioritization
   random.shuffle(debt_items)
   ```

4. **No Remediation**
   ```python
   # BAD: No remediation
   ignore_debt()
   ```

5. **No Tracking**
   ```python
   # BAD: No tracking
   fix_and_forget()
   ```

### ✅ Follow These Practices

1. **Systematic Discovery**
   ```python
   # GOOD: Systematic discovery
   discoverer = DebtDiscoverer(config)
   debt_items = await discoverer.discover_debt(project_path)
   ```

2. **Data-Driven Measurement**
   ```python
   # GOOD: Data-driven measurement
   metrics = await analyzer.analyze_code(project_path)
   ```

3. **Prioritization Framework**
   ```python
   # GOOD: Prioritization framework
   prioritizer = DebtPrioritizer(config)
   prioritized = await prioritizer.prioritize_debt(debt_items, framework="weighted")
   ```

4. **Remediation Plan**
   ```python
   # GOOD: Remediation plan
   plan = await prioritizer.create_remediation_plan(prioritized, capacity)
   ```

5. **Continuous Tracking**
   ```python
   # GOOD: Continuous tracking
   while True:
       debt = await discover_debt()
       prioritize(debt)
       remediate(debt)
       track_progress()
   ```

---

## Unit Economics & KPIs

### Development Costs
- **Initial Setup**: 20-40 hours
- **Discovery**: 40-80 hours
- **Measurement**: 20-40 hours
- **Prioritization**: 20-40 hours
- **Total**: 100-200 hours

### Operational Costs
- **Analysis Tools**: $100-500/month
- **Monitoring Tools**: $50-200/month
- **Review Time**: 10-20 hours/month
- **Remediation Time**: 20-40 hours/month

### ROI Metrics
- **Development Velocity**: 30-50% improvement
- **Bug Reduction**: 40-60% reduction
- **Maintenance Time**: 50-70% reduction
- **Code Quality**: 60-80% improvement

### KPI Targets
- **Debt Discovery Rate**: > 90%
- **Remediation Rate**: > 70%
- **Debt Reduction**: > 50% per year
- **Code Quality Score**: > 80
- **Test Coverage**: > 80%

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
- **143. Competitive Intelligence**: Competitive analysis

### Downstream Skills
- **144. Product Roadmap Communication**: Roadmap
- **145. Cross-Functional Leadership**: Leadership

### Cross-Domain Skills
- **14. Monitoring and Observability**: Monitoring
- **15. DevOps Infrastructure**: Infrastructure
- **16. Testing**: Testing practices
- **64. Meta Standards**: Coding standards

---

## References & Resources

### Documentation
- [SonarQube Documentation](https://docs.sonarqube.org/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Technical Debt Primer](https://martinfowler.com/bliki/TechnicalDebt.html)
- [Code Quality Best Practices](https://www.sonarsource.com/)

### Best Practices
- [Technical Debt Management](https://www.thoughtworks.com/insights/blog/managing-technical-debt)
- [Code Quality Standards](https://www.python.org/dev/peps/pep-0008/)
- [Security Best Practices](https://owasp.org/www-project-top-ten/)

### Tools & Libraries
- [SonarQube](https://www.sonarqube.org/)
- [ESLint](https://eslint.org/)
- [Pylint](https://www.pylint.org/)
- [Snyk](https://snyk.io/)
- [New Relic](https://newrelic.com/)
