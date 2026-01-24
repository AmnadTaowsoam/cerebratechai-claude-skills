---
name: Multi-Agent Orchestration & Governance
description: Orchestrate and govern multiple AI agents working together, including inter-agent communication, conflict resolution, human-in-the-loop gateways, and policy enforcement to ensure safe and compliant multi-agent operations.
skill-id: 162
domain: AI Agents / Governance / Enterprise Operations
level: Expert (Enterprise Scale)
maturity: Emerging (2026-2027)
---

# Multi-Agent Orchestration & Governance

> **Current Level:** Expert (Enterprise Scale)
> **Domain:** AI Agents / Governance / Enterprise Operations
> **Skill ID:** 162
> **Maturity:** Emerging - เตรียมความพร้อมสำหรับ 2026-2027

---

## Overview

Multi-Agent Orchestration & Governance ต่อยอดจาก Skill 116 (Agentic AI Frameworks) และ Skill 118 (Multi-Agent Systems) เมื่อคุณมี AI Agent หลายตัวทำงานร่วมกัน ความท้าทายคือการควบคุมไม่ให้พวกมันขัดแย้งกันเอง และมีกลไกกำกับดูแลที่เหมาะสม

---

## Why This Matters / Strategic Necessity

### Context

Multi-Agent Systems กำลังกลายเป็นมาตรฐาน:
- **Complex Tasks:** งานที่ซับซ้อนต้องการหลาย Agents
- **Enterprise Scale:** องค์กรใช้ Agents หลายตัวพร้อมกัน
- **Risk Management:** ต้องควบคุม Agents ไม่ให้ทำผิดพลาด
- **Compliance:** ต้องมี Audit Trail และ Human Oversight

### Business Impact

- **Risk Mitigation:** ลดความเสี่ยงจากการตัดสินใจผิดพลาดของ AI
- **Scalability:** Scale AI Operations โดยไม่สูญเสีย Control
- **Compliance:** รองรับ Enterprise Compliance Requirements
- **Trust:** เพิ่มความโปร่งใสในการทำงานของ AI Agents

### Product Thinking

ทักษะนี้ช่วยแก้ปัญหา:
- **Operations Teams:** ต้องการควบคุม Agents หลายตัว
- **Compliance Teams:** ต้องการ Audit Trail และ Governance
- **Product Teams:** ต้องการ Agents ที่ทำงานร่วมกันได้ดี
- **End Users:** ต้องการผลลัพธ์ที่ถูกต้องและปลอดภัย

---

## Core Concepts / Technical Deep Dive

### 1. Inter-agent Communication Protocols

มาตรฐานการสื่อสารระหว่าง Agents

```python
from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
import json

class MessageType(Enum):
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"
    ERROR = "error"

@dataclass
class AgentMessage:
    """Standardized message format for agent communication"""
    message_id: str
    from_agent: str
    to_agent: str
    message_type: MessageType
    payload: Dict[str, Any]
    timestamp: datetime
    correlation_id: Optional[str] = None
    requires_response: bool = False
    priority: int = 5  # 1-10, 10 is highest
    signature: Optional[str] = None  # For authentication

class AgentCommunicationBus:
    """Message bus for inter-agent communication"""
    
    def __init__(self):
        self.agents = {}
        self.message_queue = []
        self.subscriptions = {}  # agent -> list of topics
    
    def register_agent(
        self,
        agent_id: str,
        agent_type: str,
        capabilities: List[str]
    ):
        """Register an agent with the communication bus"""
        self.agents[agent_id] = {
            "id": agent_id,
            "type": agent_type,
            "capabilities": capabilities,
            "status": "active",
            "registered_at": datetime.utcnow()
        }
    
    def send_message(
        self,
        from_agent: str,
        to_agent: str,
        message_type: MessageType,
        payload: Dict,
        requires_response: bool = False
    ) -> str:
        """
        Send message from one agent to another.
        
        Returns message_id for tracking.
        """
        message = AgentMessage(
            message_id=self._generate_message_id(),
            from_agent=from_agent,
            to_agent=to_agent,
            message_type=message_type,
            payload=payload,
            timestamp=datetime.utcnow(),
            requires_response=requires_response
        )
        
        # Sign message for authentication
        message.signature = self._sign_message(message)
        
        # Validate agents exist
        if from_agent not in self.agents:
            raise ValueError(f"Agent {from_agent} not registered")
        if to_agent not in self.agents:
            raise ValueError(f"Agent {to_agent} not registered")
        
        # Route message
        if to_agent in self.agents:
            self._deliver_message(message)
        else:
            # Queue for later if agent offline
            self.message_queue.append(message)
        
        return message.message_id
    
    def publish_event(
        self,
        from_agent: str,
        topic: str,
        event_data: Dict
    ):
        """Publish event to all subscribed agents"""
        subscribers = self.subscriptions.get(topic, [])
        
        for subscriber_id in subscribers:
            self.send_message(
                from_agent=from_agent,
                to_agent=subscriber_id,
                message_type=MessageType.NOTIFICATION,
                payload={
                    "topic": topic,
                    "event": event_data
                }
            )
    
    def subscribe(self, agent_id: str, topic: str):
        """Subscribe agent to topic"""
        if topic not in self.subscriptions:
            self.subscriptions[topic] = []
        if agent_id not in self.subscriptions[topic]:
            self.subscriptions[topic].append(agent_id)
```

### 2. Conflict Resolution Logic

จัดการเมื่อ Agents ขัดแย้งกัน

```python
class ConflictResolver:
    """Resolve conflicts between agents"""
    
    def __init__(self):
        self.conflict_history = []
        self.resolution_strategies = {
            "priority": self._resolve_by_priority,
            "consensus": self._resolve_by_consensus,
            "rollback": self._resolve_by_rollback,
            "human": self._escalate_to_human
        }
    
    def resolve_conflict(
        self,
        conflict: Dict,
        strategy: str = "priority"
    ) -> Dict:
        """
        Resolve conflict between agents.
        
        Example conflict:
        {
            "type": "resource_conflict",
            "agents": ["sales_agent", "inventory_agent"],
            "issue": "sales_agent wants to sell 100 units, inventory_agent says only 50 available",
            "actions": [
                {"agent": "sales_agent", "action": "create_order", "params": {"quantity": 100}},
                {"agent": "inventory_agent", "action": "reserve_stock", "params": {"quantity": 50}}
            ]
        }
        """
        resolver = self.resolution_strategies.get(strategy)
        if not resolver:
            raise ValueError(f"Unknown strategy: {strategy}")
        
        resolution = resolver(conflict)
        
        # Log conflict and resolution
        self.conflict_history.append({
            "conflict": conflict,
            "strategy": strategy,
            "resolution": resolution,
            "resolved_at": datetime.utcnow()
        })
        
        return resolution
    
    def _resolve_by_priority(
        self,
        conflict: Dict
    ) -> Dict:
        """Resolve by agent priority"""
        agents = conflict["agents"]
        
        # Get agent priorities
        priorities = {}
        for agent_id in agents:
            agent_info = self._get_agent_info(agent_id)
            priorities[agent_id] = agent_info.get("priority", 5)
        
        # Highest priority wins
        winner = max(priorities.items(), key=lambda x: x[1])[0]
        
        return {
            "resolution": "priority_based",
            "winner": winner,
            "action": conflict["actions"][agents.index(winner)],
            "losers": [a for a in agents if a != winner],
            "reason": f"{winner} has higher priority"
        }
    
    def _resolve_by_consensus(
        self,
        conflict: Dict
    ) -> Dict:
        """Resolve by consensus algorithm"""
        agents = conflict["agents"]
        
        # Request proposals from all agents
        proposals = []
        for agent_id in agents:
            proposal = self._request_proposal(agent_id, conflict)
            proposals.append({
                "agent": agent_id,
                "proposal": proposal,
                "score": self._score_proposal(proposal, conflict)
            })
        
        # Select best proposal
        best = max(proposals, key=lambda x: x["score"])
        
        return {
            "resolution": "consensus",
            "selected_proposal": best["proposal"],
            "selected_agent": best["agent"],
            "all_proposals": proposals
        }
    
    def _resolve_by_rollback(
        self,
        conflict: Dict
    ) -> Dict:
        """Rollback conflicting actions"""
        return {
            "resolution": "rollback",
            "actions": [
                {"action": "rollback", "agent": agent}
                for agent in conflict["agents"]
            ],
            "reason": "Conflicting actions rolled back, manual intervention required"
        }
    
    def _escalate_to_human(
        self,
        conflict: Dict
    ) -> Dict:
        """Escalate to human for resolution"""
        escalation = {
            "resolution": "human_escalation",
            "escalated_at": datetime.utcnow(),
            "conflict": conflict,
            "human_approval_required": True,
            "approval_id": self._create_approval_request(conflict)
        }
        
        return escalation
```

### 3. Human-in-the-Loop (HITL) Gateways

จุดตรวจสอบที่ต้องใช้มนุษย์อนุมัติ

```python
class HITLGateway:
    """Human-in-the-Loop gateway for agent actions"""
    
    def __init__(self):
        self.pending_approvals = {}
        self.approval_history = []
        self.risk_thresholds = {
            "financial": 1000,  # $1000 requires approval
            "data_access": "sensitive",  # Sensitive data requires approval
            "system_change": True,  # Any system change requires approval
            "customer_impact": "high"  # High customer impact requires approval
        }
    
    def check_requires_approval(
        self,
        agent_id: str,
        action: Dict
    ) -> bool:
        """
        Check if action requires human approval.
        
        Based on risk assessment.
        """
        risk = self._assess_action_risk(action)
        
        # Check thresholds
        if action.get("type") == "financial" and risk["amount"] > self.risk_thresholds["financial"]:
            return True
        
        if action.get("type") == "data_access" and risk["sensitivity"] == self.risk_thresholds["data_access"]:
            return True
        
        if action.get("type") == "system_change":
            return True
        
        if risk.get("customer_impact") == self.risk_thresholds["customer_impact"]:
            return True
        
        return False
    
    def request_approval(
        self,
        agent_id: str,
        action: Dict,
        context: Dict
    ) -> Dict:
        """
        Request human approval for agent action.
        
        Returns approval_id and blocks action until approved.
        """
        approval_id = self._generate_approval_id()
        
        approval_request = {
            "approval_id": approval_id,
            "agent_id": agent_id,
            "action": action,
            "context": context,
            "risk_assessment": self._assess_action_risk(action),
            "requested_at": datetime.utcnow(),
            "status": "pending",
            "approver": None,
            "approved_at": None,
            "rejection_reason": None
        }
        
        self.pending_approvals[approval_id] = approval_request
        
        # Notify approvers
        self._notify_approvers(approval_request)
        
        return {
            "approval_id": approval_id,
            "status": "pending",
            "action_blocked": True,
            "estimated_response_time": "2-4 hours"
        }
    
    def approve_action(
        self,
        approval_id: str,
        approver_id: str,
        comments: Optional[str] = None
    ) -> Dict:
        """Approve a pending action"""
        if approval_id not in self.pending_approvals:
            raise ValueError(f"Approval {approval_id} not found")
        
        approval = self.pending_approvals[approval_id]
        approval["status"] = "approved"
        approval["approver"] = approver_id
        approval["approved_at"] = datetime.utcnow()
        approval["comments"] = comments
        
        # Move to history
        self.approval_history.append(approval)
        del self.pending_approvals[approval_id]
        
        # Execute action
        result = self._execute_action(approval["action"])
        
        return {
            "approval_id": approval_id,
            "status": "approved",
            "action_executed": True,
            "result": result
        }
    
    def reject_action(
        self,
        approval_id: str,
        approver_id: str,
        reason: str
    ) -> Dict:
        """Reject a pending action"""
        approval = self.pending_approvals[approval_id]
        approval["status"] = "rejected"
        approval["approver"] = approver_id
        approval["rejected_at"] = datetime.utcnow()
        approval["rejection_reason"] = reason
        
        # Move to history
        self.approval_history.append(approval)
        del self.pending_approvals[approval_id]
        
        # Notify agent
        self._notify_agent(approval["agent_id"], {
            "type": "action_rejected",
            "approval_id": approval_id,
            "reason": reason
        })
        
        return {
            "approval_id": approval_id,
            "status": "rejected",
            "action_blocked": True
        }
```

### 4. Policy Enforcement for Agents

ใช้ OPA/Rego เพื่อบังคับใช้ Policy

```python
class AgentPolicyEnforcer:
    """Enforce policies on agent actions using OPA"""
    
    def __init__(self):
        self.policies = {}
        self.opa_client = self._init_opa_client()
    
    def define_policy(
        self,
        policy_id: str,
        policy_rego: str
    ):
        """
        Define policy in Rego language.
        
        Example policy:
        package agent.policy
        
        default allow = false
        
        allow {
            input.agent.role == "sales"
            input.action.type == "create_order"
            input.action.amount < 10000
        }
        """
        self.policies[policy_id] = policy_rego
        self.opa_client.create_policy(policy_id, policy_rego)
    
    def check_policy(
        self,
        agent_id: str,
        action: Dict,
        policy_id: str = "default"
    ) -> Dict:
        """
        Check if action is allowed by policy.
        
        Returns decision and explanation.
        """
        # Prepare input for OPA
        input_data = {
            "agent": self._get_agent_context(agent_id),
            "action": action,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Query OPA
        result = self.opa_client.query(
            policy_id,
            input_data
        )
        
        return {
            "allowed": result.get("allow", False),
            "policy_id": policy_id,
            "explanation": result.get("explanation", ""),
            "conditions_met": result.get("conditions", []),
            "violations": result.get("violations", [])
        }
    
    def enforce_policy(
        self,
        agent_id: str,
        action: Dict
    ) -> Dict:
        """
        Enforce policy - block if not allowed.
        
        Returns action result or error.
        """
        # Check all applicable policies
        policy_checks = []
        for policy_id in self.policies.keys():
            check = self.check_policy(agent_id, action, policy_id)
            policy_checks.append(check)
            
            if not check["allowed"]:
                return {
                    "allowed": False,
                    "error": "Policy violation",
                    "violated_policy": policy_id,
                    "explanation": check["explanation"],
                    "action_blocked": True
                }
        
        # All policies passed
        return {
            "allowed": True,
            "policy_checks": policy_checks,
            "action_proceed": True
        }
```

---

## Tooling & Tech Stack

### Enterprise Tools

- **Orchestration:**
  - LangGraph (Workflow orchestration)
  - AutoGen (Microsoft Multi-Agent Framework)
  - CrewAI (Role-based coordination)
  - Temporal (Durable execution)

- **Policy:**
  - Open Policy Agent (OPA)
  - Rego (Policy language)

- **Monitoring:**
  - LangSmith (LangChain monitoring)
  - Custom dashboards

### Configuration Essentials

```yaml
# multi-agent-governance-config.yaml
agents:
  communication:
    protocol: "json_rpc"
    authentication: "mutual_tls"
    message_queue: "redis"
  
  conflict_resolution:
    default_strategy: "priority"
    strategies: ["priority", "consensus", "rollback", "human"]
    escalation_threshold: "high_risk"
  
  hitl:
    enabled: true
    risk_thresholds:
      financial: 1000
      data_access: "sensitive"
      system_change: true
    approval_timeout: "4_hours"
  
  policy:
    engine: "opa"
    policies_path: "/policies"
    enforcement: "strict"
```

---

## Standards, Compliance & Security

### International Standards

- **NIST AI RMF:** Risk management for AI systems
- **ISO/IEC 42001:** AI Management Systems
- **EU AI Act:** Requirements for High-Risk AI

### Security Protocol

- **Agent Authentication:** Mutual TLS between agents
- **Message Signing:** Cryptographic signatures
- **Access Control:** Role-based access for agents
- **Audit Logging:** Complete audit trail

---

## Quick Start / Getting Ready

### Phase 1: Communication Infrastructure (Week 1-2)

1. **Set Up Message Bus:**
   ```python
   bus = AgentCommunicationBus()
   bus.register_agent("sales_agent", "sales", ["create_order", "check_inventory"])
   bus.register_agent("inventory_agent", "inventory", ["reserve_stock", "check_stock"])
   ```

2. **Define Communication Protocols:**
   - Message formats
   - Authentication
   - Error handling

### Phase 2: Governance (Week 3-4)

1. **Implement HITL:**
   ```python
   gateway = HITLGateway()
   if gateway.check_requires_approval(agent_id, action):
       gateway.request_approval(agent_id, action, context)
   ```

2. **Set Up Policies:**
   - Define policies in Rego
   - Deploy to OPA
   - Test enforcement

---

## Production Checklist

- [ ] **Communication:**
  - [ ] Message bus deployed
  - [ ] Agents registered
  - [ ] Protocols defined

- [ ] **Conflict Resolution:**
  - [ ] Strategies implemented
  - [ ] Testing completed
  - [ ] Monitoring enabled

- [ ] **HITL:**
  - [ ] Gateways configured
  - [ ] Approval workflows set up
  - [ ] Approvers trained

- [ ] **Policy:**
  - [ ] Policies defined
  - [ ] Enforcement tested
  - [ ] Monitoring active

---

## Anti-patterns

### 1. **No Conflict Resolution**
❌ **Bad:** Let agents conflict without resolution
```python
# ❌ Bad - No conflict handling
sales_agent.create_order(quantity=100)
inventory_agent.reserve_stock(quantity=50)  # Conflict!
```

✅ **Good:** Detect and resolve conflicts
```python
# ✅ Good - Conflict resolution
conflict = detect_conflict(actions)
resolution = resolver.resolve_conflict(conflict)
execute(resolution)
```

### 2. **No Human Oversight**
❌ **Bad:** Agents act without human approval for high-risk actions
```python
# ❌ Bad - No approval
agent.transfer_money(amount=100000)  # High risk!
```

✅ **Good:** Require approval for high-risk actions
```python
# ✅ Good - HITL gateway
if gateway.check_requires_approval(agent_id, action):
    approval = gateway.request_approval(agent_id, action, context)
    wait_for_approval(approval)
```

---

## Timeline & Adoption Curve

### 2024-2025: Early Adopters
- Tech companies experimenting
- Frameworks maturing
- Best practices emerging

### 2025-2026: Mainstream
- Enterprise adoption increases
- Standards established
- Tools mature

### 2026-2027: Standard Practice
- Required for complex AI systems
- Regulatory requirements
- Industry standard

---

## Integration Points / Related Skills

- [Skill 116: Agentic AI Frameworks](../80-agentic-ai-advanced-learning/agentic-ai-frameworks/SKILL.md) - Agent foundations
- [Skill 118: Multi-Agent Systems](../80-agentic-ai-advanced-learning/multi-agent-systems/SKILL.md) - Multi-agent patterns
- [Skill 124: AI Workflow Orchestration](../80-agentic-ai-advanced-learning/ai-workflow-orchestration/SKILL.md) - Workflow patterns
- [Skill 158: AI Audit Trail](../85-future-compliance/ai-audit-trail/SKILL.md) - Audit requirements

---

## Further Reading

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [AutoGen Documentation](https://microsoft.github.io/autogen/)
- [Open Policy Agent](https://www.openpolicyagent.org/)
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework)
