---
name: Agentic AI Frameworks
description: Frameworks and libraries for building autonomous AI agents with tool use and multi-agent coordination
---

# Agentic AI Frameworks

> **Current Level:** Expert (Enterprise Scale)
> **Domain:** AI / Agentic AI / Multi-Agent Systems
> **Skill ID:** 116

---

## Overview
Agentic AI Frameworks provide the foundation for building autonomous AI agents that can reason, plan, and execute tasks using tools. These frameworks enable multi-agent coordination, memory management, and tool integration for complex problem-solving.

## Why This Matters / Strategic Necessity

### Context
In 2025-2026, AI agents are becoming essential for automating complex workflows, decision-making, and task execution. Building agents from scratch is time-consuming and error-prone, requiring robust frameworks.

### Business Impact
- **Automation:** 70-90% reduction in manual task execution
- **Decision Quality:** 60-80% improvement in decision accuracy
- **Scalability:** Support for complex multi-agent workflows
- **Time-to-Value:** 50-70% faster agent development

### Product Thinking
Solves critical problem where building autonomous AI agents requires significant engineering effort, leading to long development cycles and unreliable agent behavior in production.

## Core Concepts / Technical Deep Dive

### 1. Agent Architecture

**Agent Components:**
- **Memory:** Short-term and long-term memory for context
- **Planning:** Task decomposition and execution planning
- **Execution:** Tool use and action execution
- **Observation:** Environment monitoring and feedback
- **Reflection:** Learning from experience

**Agent Types:**
- **ReAct:** Reasoning + Acting agents
- **AutoGPT:** Autonomous GPT-based agents
- **Toolformer:** Tool-using agents
- **CrewAI:** Multi-agent coordination
- **LangGraph:** Graph-based agent workflows

### 2. Framework Comparison

```
┌─────────────────────────────────────────────────────────────────┐
│                    Agent Frameworks                     │
├─────────────────────────────────────────────────────────────────┤
│  LangChain            │  LangGraph         │  AutoGPT       │  CrewAI        │
│  - Chained calls      │  - Graph workflow  │  - Autonomous     │  - Multi-agent   │
│  - Memory management  │  - State machines   │  - Tool use      │  - Role-based     │
│  - Tool integration   │  - Error handling   │  - Planning       │  - Coordination  │
└─────────────────────────────────────────────────────────────────┘
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
┌─────────────────────────────────────────────────────────────────┐
│  Toolformer          │  ReAct            │  Semantic Kernel │  MemGPT        │
│  - Tool use         │  - Reasoning       │  - Knowledge       │  - Memory        │
│  - Multi-modal       │  - Planning         │  - Reasoning       │  - Learning       │
└─────────────────────────────────────────────────────────────────┘
```

### 3. Tool Integration

**Tool Types:**
- **API Tools:** REST, GraphQL, gRPC
- **Database Tools:** SQL, NoSQL, Vector DB
- **File Operations:** Read, write, search
- **Code Execution:** Python, JavaScript, Shell
- **Web Scraping:** Browser automation

**Tool Calling:**
- **Function Description:** Tool capabilities and schemas
- **Argument Validation:** Type checking and constraints
- **Execution:** Async tool execution with timeout
- **Result Parsing:** Extract and format tool outputs
- **Error Handling:** Retry logic and fallback strategies

### 4. Multi-Agent Coordination

**Coordination Patterns:**
- **Hierarchical:** Manager agent coordinates worker agents
- **Flat:** Peer-to-peer coordination
- **Task Allocation:** Dynamic task assignment
- **Conflict Resolution:** Handle competing agent decisions

**Communication:**
- **Message Passing:** Direct agent-to-agent communication
- **Shared Memory:** Shared knowledge base
- **Blackboard:** Central coordination space
- **Broadcast:** One-to-many announcements

## Tooling & Tech Stack

### Enterprise Tools
- **LangChain:** Comprehensive LLM framework with agents
- **LangGraph:** Graph-based agent workflows
- **AutoGPT:** Autonomous GPT-based agents
- **CrewAI:** Multi-agent orchestration
- **LlamaIndex:** Agent framework for LLMs
- **Semantic Kernel:** Open-source agent framework
- **MemGPT:** Memory-augmented LLMs

### Configuration Essentials

```yaml
# Agentic AI framework configuration
agent_framework:
  # Framework selection
  framework: "langgraph"  # langchain, langgraph, autogpt, crewai, semantic_kernel
  
  # Agent configuration
  agent:
    name: "assistant_agent"
    model: "gpt-4"
    temperature: 0.7
    max_tokens: 2000
    memory_type: "summary"  # summary, vector, none
    memory_limit: 10
  
  # Tool configuration
  tools:
    - name: "search"
      type: "web_search"
      enabled: true
    
    - name: "code_execution"
      type: "python"
      enabled: true
      timeout: 30
    
    - name: "database_query"
      type: "sql"
      enabled: true
      connection_string: "${DB_CONNECTION}"
  
  # Multi-agent configuration
  multi_agent:
    enabled: false
    coordination: "hierarchical"  # hierarchical, flat, blackboard
    max_agents: 5
    task_allocation: "dynamic"
  
  # Planning configuration
  planning:
    max_iterations: 10
    planning_strategy: "react"  # react, proactive
    allow_replanning: true
  
  # Memory configuration
  memory:
    type: "summary"  # summary, vector, none
    max_entries: 100
    retention_hours: 24
    importance_threshold: 0.8
  
  # Monitoring
  monitoring:
    log_agent_actions: true
    track_tool_usage: true
    measure_reasoning_steps: true
    alert_on_errors: true
```

## Code Examples

### Good vs Bad Examples

```python
# ❌ Bad - No tool validation, security risk
def execute_tool(tool_name, arguments):
    # Execute tool without validation
    result = subprocess.run(arguments, shell=True)
    return result.stdout

# ✅ Good - Tool validation with error handling
def execute_tool_safe(tool_name, arguments):
    # Validate tool exists and is allowed
    if not is_tool_allowed(tool_name):
        raise ValueError(f"Tool not allowed: {tool_name}")
    
    # Validate arguments
    if not validate_arguments(tool_name, arguments):
        raise ValueError("Invalid arguments")
    
    # Execute with timeout and error handling
    try:
        result = subprocess.run(
            arguments,
            shell=True,
            timeout=30,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            raise RuntimeError(f"Tool failed: {result.stderr}")
        
        return result.stdout
        
    except subprocess.TimeoutExpired:
        raise TimeoutError(f"Tool timed out: {tool_name}")
```

```python
# ❌ Bad - No memory, agent forgets context
def agent_loop():
    while True:
        # No memory, can't learn from past
        action = decide_action()
        execute_action(action)

# ✅ Good - Memory-augmented agent
def agent_with_memory():
    memory = []
    
    while True:
        # Observe environment
        observation = observe_environment()
        
        # Update memory
        memory.append(observation)
        if len(memory) > 100:
            # Summarize old memories
            memory = summarize_memory(memory[-100:]) + memory[-100:]
        
        # Decide action based on memory
        action = decide_action(memory)
        result = execute_action(action)
        
        # Update memory with result
        memory.append({
            'observation': observation,
            'action': action,
            'result': result
        })
```

### Implementation Example

```python
"""
Production-ready Agentic AI Framework
"""
from typing import Dict, List, Optional, Any, Callable, Union
from datetime import datetime
import json
import logging
from dataclasses import dataclass, field
from enum import Enum
import asyncio
from abc import ABC, abstractmethod

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ToolType(Enum):
    """Tool types."""
    WEB_SEARCH = "web_search"
    CODE_EXECUTION = "code_execution"
    DATABASE_QUERY = "database_query"
    FILE_OPERATION = "file_operation"
    API_CALL = "api_call"


@dataclass
class Tool:
    """Tool definition."""
    name: str
    description: str
    tool_type: ToolType
    function: Callable
    schema: Dict[str, Any]
    enabled: bool = True


@dataclass
class ToolExecution:
    """Tool execution result."""
    tool_name: str
    arguments: Dict[str, Any]
    result: Any
    execution_time: float
    success: bool
    error_message: Optional[str] = None


@dataclass
class AgentMemory:
    """Agent memory entry."""
    timestamp: datetime
    observation: str
    action: str
    result: Any
    importance: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentPlan:
    """Agent plan."""
    goal: str
    steps: List[Dict[str, Any]]
    current_step: int = 0
    status: str = "pending"


class BaseAgent(ABC):
    """Base class for AI agents."""
    
    def __init__(self, name: str, tools: List[Tool] = None):
        """
        Initialize agent.
        
        Args:
            name: Agent name
            tools: Available tools
        """
        self.name = name
        self.tools = tools or []
        self.memory: List[AgentMemory] = []
        self.current_plan: Optional[AgentPlan] = None
        self.max_memory_entries = 100
        
        logger.info(f"Agent initialized: {name}")
    
    @abstractmethod
    async def think(self, observation: str) -> Dict[str, Any]:
        """
        Think about what to do given observation.
        
        Args:
            observation: Current observation
            
        Returns:
            Thought process and decision
        """
        pass
    
    @abstractmethod
    async def act(self, action: Dict[str, Any]) -> Any:
        """
        Execute an action.
        
        Args:
            action: Action to execute
            
        Returns:
            Result of action
        """
        pass
    
    async def observe(self) -> str:
        """
        Observe the environment.
        
        Returns:
            Observation string
        """
        return "Environment observation"
    
    async def run(self) -> None:
        """
        Main agent loop.
        """
        while True:
            # Observe
            observation = await self.observe()
            
            # Think
            thought = await self.think(observation)
            
            # Act
            result = await self.act(thought['action'])
            
            # Update memory
            self._update_memory(observation, thought, result)
            
            # Plan next steps if needed
            if self.current_plan and self.current_plan.status == "pending":
                await self._execute_plan()
    
    def _update_memory(self, observation: str, thought: Dict[str, Any], result: Any) -> None:
        """Update agent memory."""
        memory_entry = AgentMemory(
            timestamp=datetime.utcnow(),
            observation=observation,
            action=thought.get('action', ''),
            result=result,
            importance=thought.get('importance', 1.0)
        )
        
        self.memory.append(memory_entry)
        
        # Prune memory if needed
        if len(self.memory) > self.max_memory_entries:
            self._prune_memory()
    
    def _prune_memory(self) -> None:
        """Prune old memory entries."""
        # Sort by importance and keep top N
        self.memory.sort(key=lambda m: m.importance, reverse=True)
        self.memory = self.memory[:self.max_memory_entries]
    
    async def _execute_plan(self) -> None:
        """Execute current plan."""
        if not self.current_plan:
            return
        
        step = self.current_plan.steps[self.current_plan.current_step]
        
        # Execute step
        result = await self.act(step)
        
        # Update plan
        self.current_plan.current_step += 1
        
        if self.current_plan.current_step >= len(self.current_plan.steps):
            self.current_plan.status = "completed"
    
    def add_tool(self, tool: Tool) -> None:
        """Add a tool to the agent."""
        self.tools.append(tool)
        logger.info(f"Tool added to {self.name}: {tool.name}")
    
    async def use_tool(
        self,
        tool_name: str,
        arguments: Dict[str, Any]
    ) -> Any:
        """
        Use a tool.
        
        Args:
            tool_name: Name of tool to use
            arguments: Tool arguments
            
        Returns:
            Tool result
        """
        tool = next((t for t in self.tools if t.name == tool_name), None)
        
        if not tool:
            raise ValueError(f"Tool not found: {tool_name}")
        
        if not tool.enabled:
            raise ValueError(f"Tool not enabled: {tool_name}")
        
        # Validate arguments
        if not self._validate_arguments(tool, arguments):
            raise ValueError("Invalid arguments")
        
        # Execute tool
        start_time = datetime.utcnow()
        
        try:
            result = await tool.function(**arguments)
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            
            return ToolExecution(
                tool_name=tool_name,
                arguments=arguments,
                result=result,
                execution_time=execution_time,
                success=True
            )
            
        except Exception as e:
            return ToolExecution(
                tool_name=tool_name,
                arguments=arguments,
                result=None,
                execution_time=0.0,
                success=False,
                error_message=str(e)
            )
    
    def _validate_arguments(self, tool: Tool, arguments: Dict[str, Any]) -> bool:
        """Validate tool arguments."""
        for param_name, param_schema in tool.schema.items():
            if param_name not in arguments:
                if param_schema.get('required', False):
                    continue
                return False
            
            value = arguments[param_name]
            expected_type = param_schema.get('type', 'str')
            
            if expected_type == 'str' and not isinstance(value, str):
                return False
            elif expected_type == 'int' and not isinstance(value, int):
                return False
            elif expected_type == 'float' and not isinstance(value, (int, float)):
                return False
            elif expected_type == 'bool' and not isinstance(value, bool):
                return False
            elif expected_type == 'list' and not isinstance(value, list):
                return False
            elif expected_type == 'dict' and not isinstance(value, dict):
                return False
        
        return True


class ReActAgent(BaseAgent):
    """
    ReAct-style agent with reasoning and acting.
    """
    
    def __init__(self, name: str, tools: List[Tool] = None):
        super().__init__(name, tools)
        self.max_iterations = 10
    
    async def think(self, observation: str) -> Dict[str, Any]:
        """
        Think about what to do using ReAct pattern.
        
        Args:
            observation: Current observation
            
        Returns:
            Thought process and action
        """
        # ReAct: Reason + Act loop
        for iteration in range(self.max_iterations):
            # Thought: What should I do?
            thought = f"Observation: {observation}. "
            thought += "I need to analyze this and decide on an action."
            
            # Search memory for relevant context
            relevant_memory = self._search_memory(observation)
            
            if relevant_memory:
                thought += f"Relevant context from memory: {relevant_memory}"
            
            # Decide action
            action = self._decide_action(observation, relevant_memory)
            
            if action:
                thought += f"Action: {action['type']} - {action['description']}"
                
                # Check if we need to use a tool
                if action.get('use_tool'):
                    thought += f"Tool to use: {action['tool_name']}"
                    
                    return {
                        'thought': thought,
                        'action': action,
                        'use_tool': True,
                        'tool_name': action.get('tool_name'),
                        'tool_arguments': action.get('tool_arguments', {})
                        'iterations': iteration + 1
                    }
            
            # If we've reached max iterations without action
            if iteration >= self.max_iterations - 1:
                return {
                    'thought': thought + " Max iterations reached.",
                    'action': None,
                    'use_tool': False
                }
        
        # No action decided
        return {
            'thought': thought + " No action needed.",
            'action': None,
            'use_tool': False
        }
    
    def _search_memory(self, query: str) -> Optional[str]:
        """Search memory for relevant context."""
        query_lower = query.lower()
        
        for memory in reversed(self.memory):
            memory_text = f"{memory.observation} {memory.action} {memory.result}".lower()
            
            if query_lower in memory_text:
                return memory.observation
        
        return None
    
    def _decide_action(self, observation: str, memory: Optional[str] = None) -> Dict[str, Any]:
        """Decide on an action."""
        # Analyze observation
        if "search" in observation.lower():
            return {
                'type': 'search',
                'description': 'Search for information',
                'tool_name': 'web_search',
                'tool_arguments': {'query': observation.split('search')[1] if 'search' in observation else observation}
            }
        elif "code" in observation.lower() or "execute" in observation.lower():
            return {
                'type': 'code_execution',
                'description': 'Execute code',
                'tool_name': 'code_execution',
                'tool_arguments': {'code': observation.split('execute')[1] if 'execute' in observation else observation}
            }
        else:
            return {
                'type': 'think',
                'description': 'Continue thinking',
                'use_tool': False
            }


class AgentOrchestrator:
    """
    Orchestrates multiple agents for complex tasks.
    """
    
    def __init__(self, agents: List[BaseAgent]):
        """
        Initialize agent orchestrator.
        
        Args:
            agents: List of agents to orchestrate
        """
        self.agents = agents
        self.task_queue = asyncio.Queue()
        self.completed_tasks: Dict[str, Any] = {}
        
        logger.info(f"Agent orchestrator initialized with {len(agents)} agents")
    
    async def assign_task(self, task: Dict[str, Any]) -> str:
        """
        Assign a task to an agent.
        
        Args:
            task: Task to assign
            
        Returns:
            Task ID
        """
        task_id = f"task_{datetime.utcnow().timestamp()}"
        
        # Find best agent for task
        best_agent = self._find_best_agent(task)
        
        # Assign task
        await best_agent.observe()  # Trigger agent
        self.completed_tasks[task_id] = {
            'task': task,
            'agent': best_agent.name,
            'status': 'in_progress'
        }
        
        logger.info(f"Task {task_id} assigned to {best_agent.name}")
        return task_id
    
    def _find_best_agent(self, task: Dict[str, Any]) -> BaseAgent:
        """Find best agent for a task."""
        # Simple strategy: first available agent
        for agent in self.agents:
            return agent
        
        return self.agents[0]
    
    async def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task status."""
        return self.completed_tasks.get(task_id)
    
    async def get_orchestrator_status(self) -> Dict[str, Any]:
        """Get orchestrator status."""
        return {
            'total_agents': len(self.agents),
            'active_tasks': sum(1 for t in self.completed_tasks.values() if t['status'] == 'in_progress'),
            'completed_tasks': sum(1 for t in self.completed_tasks.values() if t['status'] == 'completed'),
            'agents': [agent.name for agent in self.agents]
        }


# Example usage
async def main():
    # Create tools
    web_search_tool = Tool(
        name="web_search",
        description="Search the web for information",
        tool_type=ToolType.WEB_SEARCH,
        function=lambda query: f"Search results for: {query}",
        schema={'query': {'type': 'str', 'required': True}}
    )
    
    code_tool = Tool(
        name="code_execution",
        description="Execute Python code",
        tool_type=ToolType.CODE_EXECUTION,
        function=lambda code: exec(code),
        schema={'code': {'type': 'str', 'required': True}}
    )
    
    # Create ReAct agent
    agent = ReActAgent(
        name="assistant",
        tools=[web_search_tool, code_tool]
    )
    
    # Run agent
    print("Starting agent...")
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())
```

## Standards, Compliance & Security

### International Standards
- **ISO/IEC 27001:** Information security management
- **GDPR:** Data protection and privacy
- **SOC 2 Type II:** Security and availability controls
- **NIST AI RMF:** AI risk management framework

### Security Protocol
- **Tool Validation:** Validate all tool inputs and outputs
- **Sandboxing:** Execute tools in isolated environments
- **Access Control:** Role-based access to tools
- **Audit Logging:** Complete audit trail of agent actions
- **Rate Limiting:** Prevent tool abuse

### Explainability
- **Agent Logs:** Detailed logs of all agent decisions
- **Tool Usage Tracking:** Track which tools are used and how
- **Reasoning Trace:** Complete trace of agent thought process
- **Memory Inspection:** View and analyze agent memory

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install langchain langgraph openai
   ```

2. **Create a ReAct agent:**
   ```python
   agent = ReActAgent(
       name="assistant",
       tools=[web_search_tool, code_tool]
   )
   ```

3. **Run agent:**
   ```python
   await agent.run()
   ```

4. **Orchestrate multiple agents:**
   ```python
   orchestrator = AgentOrchestrator(agents=[agent1, agent2])
   task_id = await orchestrator.assign_task(task)
   ```

## Production Checklist

- [ ] Agent framework selected and configured
- [ ] Tools defined and validated
- [ ] Memory management implemented
- [ ] Error handling and retry logic
- [ ] Monitoring and logging configured
- [ ] Tool sandboxing implemented
- [ ] Multi-agent coordination configured
- [ ] Security controls in place
- [ ] Performance testing completed

## Anti-patterns

1. **No Tool Validation:** Executing tools without validation
   - **Why it's bad:** Security risk, unpredictable behavior
   - **Solution:** Implement comprehensive tool validation

2. **No Memory:** Agent forgets context
   - **Why it's bad:** Can't learn from experience
   - **Solution:** Implement memory management

3. **Infinite Loops:** Agent gets stuck in loops
   - **Why it's bad:** Wastes resources, poor UX
   - **Solution:** Implement max iterations and timeout

4. **No Error Handling:** Tools fail without retry
   - **Why it's bad:** Unreliable agent behavior
   - **Solution:** Implement retry logic with exponential backoff

## Unit Economics & KPIs

### Cost Calculation
```
Total Cost = Infrastructure + Operations + LLM API Costs

Infrastructure = (Server + Storage + Network) / 3 years
Operations = (Development Time × Labor Rate)
LLM API Costs = (Token Usage × Token Rate) × Usage
```

### Key Performance Indicators
- **Task Success Rate:** > 95%
- **Tool Success Rate:** > 98%
- **Agent Response Time:** < 5 seconds for simple tasks
- **Memory Efficiency:** < 1000 entries per agent
- **Cost Per Task:** < $0.10 for simple tasks

## Integration Points / Related Skills
- [RAG Advanced](../80-agentic-ai-advanced-learning/rag-advanced/SKILL.md) - For knowledge retrieval
- [LLM Fine-tuning Alignment](../80-agentic-ai-advanced-learning/llm-finetuning-alignment/SKILL.md) - For model customization
- [AI Workflow Orchestration](../80-agentic-ai-advanced-learning/ai-workflow-orchestration/SKILL.md) - For workflow management
- [Knowledge Graph Integration](../80-agentic-ai-advanced-learning/knowledge-graph-integration/SKILL.md) - For knowledge management

## Further Reading
- [LangChain Documentation](https://python.langchain.com/docs/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [AutoGPT Documentation](https://github.com/Significant-Gravitas/Auto-GPT)
- [CrewAI Documentation](https://docs.crewai.com/)
- [Semantic Kernel](https://github.com/facebookresearch/semantic-kernel)
- [Agent Engineering](https://lilianweng.github.io/blog/2023/06/09/agent-intro/)
