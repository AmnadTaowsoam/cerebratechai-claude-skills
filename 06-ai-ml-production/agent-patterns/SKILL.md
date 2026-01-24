---
name: AI Agent Patterns
description: Design patterns for building autonomous AI agents that can reason, plan, and execute tasks.
---

# AI Agent Patterns

## Overview

AI agents are autonomous systems that use Large Language Models (LLMs) to reason, plan, and execute tasks. Unlike simple chatbots, agents can break down complex problems into steps, use tools to interact with external systems, and adapt their behavior based on feedback. This skill covers agent architectures (ReAct, Plan-and-Execute, Tree of Thoughts, Reflexion), core components (memory, planning, tool use), frameworks (LangChain, AutoGPT, CrewAI, Semantic Kernel), tool design, multi-agent systems, error recovery, guardrails, evaluation, and production deployment.

## Prerequisites

- Understanding of LLMs and their capabilities
- Knowledge of prompt engineering and system prompts
- Familiarity with function calling and tool APIs
- Understanding of agent architectures and design patterns
- Basic knowledge of vector databases and embeddings
- Understanding of safety and guardrails for AI systems

## Key Concepts

### Agent Characteristics

- **Autonomy**: Can make decisions without human intervention
- **Reasoning**: Can break down complex tasks into subtasks
- **Planning**: Can create and execute multi-step plans
- **Tool Use**: Can interact with external systems via function calling
- **Memory**: Can maintain context across interactions
- **Adaptation**: Can learn from feedback and adjust behavior

### Simple vs Complex Agents

- **Simple Agent**: Single-step execution (e.g., weather query → result)
- **Complex Agent**: Multi-step planning (e.g., trip planning → search → book → confirm)

### Agent Architectures

- **ReAct**: Reasoning + Acting in a loop
- **Plan-and-Execute**: Create plan first, then execute step by step
- **Tree of Thoughts**: Explore multiple reasoning paths before deciding
- **Reflexion**: Reflect on actions and learn from mistakes

### Core Components

- **Memory**: Short-term (conversation history), Long-term (knowledge base), Episodic (specific experiences)
- **Planning**: Break down goals into actionable steps
- **Tool Use**: Register, validate, and execute tools safely
- **Reflection**: Analyze actions and improve behavior

### Deployment Patterns

- **FastAPI Server**: REST API for agent inference
- **Docker Deployment**: Containerized agent service
- **Kubernetes**: Scalable deployment with GPU support
- **Multi-Agent Systems**: Agent collaboration and delegation

## Implementation Guide

### Agent Architectures

#### ReAct (Reasoning + Acting)

The ReAct pattern combines reasoning and acting in a loop.

```python
from openai import OpenAI

class ReActAgent:
    def __init__(self, llm_client, tools):
        self.client = llm_client
        self.tools = tools
        self.max_iterations = 10

    def run(self, query):
        thoughts = []

        for i in range(self.max_iterations):
            # Thought: What should I do?
            thought_response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.get_system_prompt()},
                    *thoughts,
                    {"role": "user", "content": query}
                ],
                tools=self.tools
            )

            thought = thought_response.choices[0].message.content
            thoughts.append({"role": "assistant", "content": thought})

            # Check if agent wants to use a tool
            if thought_response.choices[0].finish_reason == "function_calls":
                fc = thought_response.choices[0].message.function_calls[0]

                # Action: Execute tool
                tool_result = self.execute_tool(fc.name, fc.arguments)

                # Observation: What did I observe?
                observation = f"Tool {fc.name} returned: {json.dumps(tool_result)}"
                thoughts.append({"role": "assistant", "content": observation})
            else:
                # No more actions needed
                break

        return thoughts

    def get_system_prompt(self):
        return """You are a helpful assistant with access to tools.
Use the following format:

Thought: your thought about what to do
Action: action to take (tool call or final answer)
Observation: result of the action
... (repeat Thought/Action/Observation as needed)"""

    def execute_tool(self, tool_name, arguments):
        # Execute tool
        for tool in self.tools:
            if tool["name"] == tool_name:
                handler = tool["handler"]
                return handler(**arguments)
        return None

# Usage
tools = [
    {
        "type": "function",
        "function": {
            "name": "search",
            "description": "Search for information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        },
        "handler": search_tool
    }
]

agent = ReActAgent(client, tools)
conversation = agent.run("What is the capital of France?")
```

#### Plan-and-Execute

The agent creates a plan first, then executes it step by step.

```python
class PlanAndExecuteAgent:
    def __init__(self, llm_client, tools):
        self.client = llm_client
        self.tools = tools

    def run(self, query):
        # Phase 1: Planning
        plan_response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": """You are a planning agent.
Break down the user's request into a numbered list of steps.
Each step should be actionable and use available tools.

Available tools:
- search: Search for information
- calculate: Perform calculations
- database: Query database

Format your response as:
Step 1: [action]
Step 2: [action]
..."""
                },
                {"role": "user", "content": query}
            ],
            tools=self.tools
        )

        plan_text = plan_response.choices[0].message.content
        steps = self.parse_plan(plan_text)

        # Phase 2: Execution
        results = []
        for step in steps:
            result = self.execute_step(step)
            results.append(result)

        # Phase 3: Synthesis
        synthesis_response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "Synthesize the results into a final answer."
                },
                {"role": "user", "content": query},
                {"role": "assistant", "content": plan_text},
                *[{"role": "assistant", "content": f"Step {i+1} result: {json.dumps(r)}"} 
                   for i, r in enumerate(results)]
            ]
        )

        return synthesis_response.choices[0].message.content

    def parse_plan(self, plan_text):
        steps = []
        lines = plan_text.split('\n')
        for line in lines:
            if line.strip().startswith('Step'):
                steps.append(line.strip())
        return steps

    def execute_step(self, step):
        # Extract tool name and arguments from step
        tool_name = self.extract_tool_name(step)
        arguments = self.extract_arguments(step)

        # Execute tool
        for tool in self.tools:
            if tool["name"] == tool_name:
                handler = tool["handler"]
                return handler(**arguments)

        return None
```

#### Tree of Thoughts

The agent explores multiple reasoning paths before deciding.

```python
class TreeOfThoughtsAgent:
    def __init__(self, llm_client, tools):
        self.client = llm_client
        self.tools = tools
        self.max_depth = 3
        self.max_branches = 5

    def run(self, query):
        # Generate multiple candidate thoughts
        thoughts_response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": f"""You are a thoughtful agent.
Generate {self.max_branches} different possible thoughts/paths to answer the query.

Each thought should explore a different approach.

Format as:
Thought 1: [description]
Thought 2: [description]
...
"""
                },
                {"role": "user", "content": query}
            ],
            tools=self.tools
        )

        thoughts_text = thoughts_response.choices[0].message.content
        thoughts = thoughts_text.split('\n')

        # Evaluate each thought
        evaluations = []
        for i, thought in enumerate(thoughts):
            evaluation = self.evaluate_thought(thought, query)
            evaluations.append((i, evaluation))

        # Select best thought
        best = max(evaluations, key=lambda x: x[1])
        best_thought = thoughts[best[0]]

        # Execute best thought
        result = self.execute_thought(best_thought)

        return result

    def evaluate_thought(self, thought, query):
        # Score thought based on various criteria
        score = 0

        # Clarity
        if "clear" in thought.lower():
            score += 2

        # Completeness
        if "step" in thought.lower():
            score += 2

        # Efficiency
        if "quick" in thought.lower() or "fast" in thought.lower():
            score += 1

        return score

    def execute_thought(self, thought):
        # Extract tool calls from thought
        tool_calls = self.extract_tool_calls(thought)

        # Execute all tool calls
        results = []
        for tc in tool_calls:
            result = self.execute_tool(tc["name"], tc["arguments"])
            results.append(result)

        return results
```

#### Reflexion

The agent reflects on its actions and learns from mistakes.

```python
class ReflexionAgent:
    def __init__(self, llm_client, tools):
        self.client = llm_client
        self.tools = tools
        self.memory = []
        self.reflections = []

    def run(self, query):
        while True:
            # Act: Generate action
            action_response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant. Answer the user's query."
                    },
                    *self.memory,
                    {"role": "user", "content": query}
                ],
                tools=self.tools
            )

            action = action_response.choices[0].message
            self.memory.append({"role": "assistant", "content": action})

            # Check if action was taken
            if action_response.choices[0].finish_reason == "function_calls":
                fc = action_response.choices[0].message.function_calls[0]

                # Execute action
                result = self.execute_tool(fc.name, fc.arguments)

                # Reflect: Was this action successful?
                reflection = self.reflect(action, result)
                self.reflections.append(reflection)

                # Update memory with reflection
                self.memory.append({
                    "role": "system",
                    "content": f"Reflection: {reflection}"
                })

                # If action failed, try again
                if "failed" in reflection.lower():
                    continue
                else:
                    # Success - generate final answer
                    final_response = self.client.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            *self.memory,
                            {
                                "role": "user",
                                "content": query
                            },
                            {
                                "role": "function",
                                "name": fc.name,
                                "content": json.dumps(result)
                            }
                        ]
                    )
                    return final_response.choices[0].message.content
            else:
                # No action needed - return answer
                return action

    def reflect(self, action, result):
        # Analyze action and result
        reflection_parts = []

        # Did the action achieve its goal?
        if result.get("success", False):
            reflection_parts.append("The action failed.")

        # What went wrong?
        if "error" in result:
            reflection_parts.append(f"Error: {result['error']}")

        # How could it be improved?
        if "error" in result:
            reflection_parts.append("Next time, validate parameters first.")

        return " ".join(reflection_parts)
```

### Core Components

#### Memory (Short-term, Long-term)

```python
from typing import List, Dict, Any
from datetime import datetime

class AgentMemory:
    def __init__(self):
        self.short_term = []  # Conversation history
        self.long_term = {}  # Persistent knowledge
        self.episodic = []  # Specific episodes/experiences

    def add_to_short_term(self, role, content):
        """Add to conversation history"""
        self.short_term.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })

        # Keep last 10 messages
        if len(self.short_term) > 10:
            self.short_term = self.short_term[-10:]

    def add_to_long_term(self, key, value):
        """Add to persistent knowledge base"""
        self.long_term[key] = {
            "value": value,
            "timestamp": datetime.now().isoformat(),
            "access_count": self.long_term.get(key, {}).get("access_count", 0) + 1
        }

    def add_episode(self, episode_type, data):
        """Add a specific experience/episode"""
        self.episodic.append({
            "type": episode_type,
            "data": data,
            "timestamp": datetime.now().isoformat()
        })

    def retrieve_relevant(self, query, max_results=5):
        """Retrieve relevant information based on query"""
        # Simple keyword matching for long-term memory
        relevant = []
        query_lower = query.lower()

        for key, value in self.long_term.items():
            if query_lower in key.lower() or key.lower() in query_lower():
                relevant.append({
                    "key": key,
                    "value": value["value"],
                    "relevance": self.calculate_relevance(query, key)
                })

        # Sort by relevance and return top results
        relevant.sort(key=lambda x: x["relevance"], reverse=True)
        return relevant[:max_results]

    def calculate_relevance(self, query, key):
        """Calculate relevance score"""
        query_words = set(query.lower().split())
        key_words = set(key.lower().split())

        # Jaccard similarity
        intersection = len(query_words & key_words)
        union = len(query_words | key_words)

        return intersection / union if union > 0 else 0

    def get_context(self, max_messages=10):
        """Get recent conversation context"""
        return self.short_term[-max_messages:]
```

#### Planning

```python
from typing import List, Dict

class Planner:
    def __init__(self, llm_client):
        self.client = llm_client

    def create_plan(self, goal, constraints=None):
        """Create a step-by-step plan to achieve the goal"""

        system_prompt = f"""You are a planning agent.
Create a detailed plan to achieve the goal: {goal}

Constraints:
{constraints if constraints else "None"}

Available operations:
- search: Search for information
- query_database: Query database
- calculate: Perform calculations
- api_call: Call external APIs

Format your plan as:
1. [Operation] - [Description]
2. [Operation] - [Description]
...

Each step should be specific and actionable.
"""

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": goal}
            ],
            tools=self.tools
        )

        plan_text = response.choices[0].message.content
        return self.parse_plan(plan_text)

    def parse_plan(self, plan_text):
        """Parse the plan into structured format"""
        steps = []
        lines = plan_text.split('\n')

        for line in lines:
            if line.strip() and line.strip()[0].isdigit():
                parts = line.split('-', 1)
                if len(parts) == 2:
                    operation = parts[0].strip()
                    description = parts[1].strip()
                    steps.append({
                        "step": int(operation[0]),
                        "operation": operation,
                        "description": description
                    })

        return steps

    def update_plan(self, plan, completed_step, new_step=None):
        """Update plan after completing a step"""
        updated_plan = []

        for step in plan:
            if step["step"] == completed_step:
                continue  # Skip completed step

            if new_step:
                # Insert new step after completed step
                if step["step"] == completed_step - 1:
                    updated_plan.append(step)
                    updated_step = {
                        "step": completed_step,
                        "operation": new_step["operation"],
                        "description": new_step["description"]
                    }
                    # Renumber remaining steps
                    for s in plan[step["step"]:]:
                        updated_step = s.copy()
                        updated_step["step"] = len(updated_plan) + 1
                    updated_plan.append(updated_step)
                    break
            else:
                updated_plan.append(step)

        return updated_plan
```

#### Tool Use

```python
from typing import Dict, Callable, Any

class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Dict] = {}

    def register(self, name: str, handler: Callable, description: str, parameters: Dict):
        """Register a tool"""
        self.tools[name] = {
            "handler": handler,
            "description": description,
            "parameters": parameters
        }

    def get_tool(self, name: str) -> Dict:
        """Get a tool by name"""
        return self.tools.get(name)

    def list_tools(self) -> List[Dict]:
        """List all available tools"""
        return list(self.tools.values())

    def execute(self, name: str, arguments: Dict) -> Any:
        """Execute a tool with given arguments"""
        tool = self.get_tool(name)
        if not tool:
            raise ValueError(f"Tool not found: {name}")

        handler = tool["handler"]
        return handler(**arguments)

    def get_openai_schema(self):
        """Convert tools to OpenAI function calling format"""
        return [
            {
                "type": "function",
                "function": {
                    "name": name,
                    "description": tool["description"],
                    "parameters": tool["parameters"]
                }
            }
            for name, tool in self.tools.items()
        ]

# Usage
def search_database(query: str) -> Dict:
    """Search database"""
    # Implementation
    return {"results": [], "query": query}

def calculate(expression: str) -> float:
    """Calculate a mathematical expression"""
    # Implementation
    return eval(expression)

registry = ToolRegistry()
registry.register("search", search_database, "Search for database", {
    "type": "object",
    "properties": {
        "query": {"type": "string"}
    },
    "required": ["query"]
})
registry.register("calculate", calculate, "Perform calculations", {
    "type": "object",
    "properties": {
        "expression": {"type": "string"}
    },
    "required": ["expression"]
})
```

#### Reflection

```python
class ReflectionEngine:
    def __init__(self, llm_client):
        self.client = llm_client
        self.reflection_history = []

    def reflect_on_action(self, action, result, context):
        """Reflect on an action and its result"""

        reflection_prompt = f"""
You are a reflection engine. Analyze the following action and result:

Action: {action}
Result: {result}
Context: {context}

Provide a reflection that includes:
1. What was the goal of this action?
2. Was the action successful?
3. If not successful, what went wrong?
4. How could this be improved for next time?
5. Should we try a different approach?

Format your reflection as:
Analysis: [Your analysis here]
Recommendation: [Your recommendation here]
"""

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": reflection_prompt}]
        )

        reflection = response.choices[0].message.content
        self.reflection_history.append(reflection)

        return reflection

    def get_improvement_suggestion(self, recent_reflections):
        """Get improvement suggestions from recent reflections"""
        if not recent_reflections:
            return None

        # Analyze patterns in reflections
        suggestions = []

        for reflection in recent_reflections:
            if "improve" in reflection.lower() or "better" in reflection.lower():
                # Extract improvement suggestion
                lines = reflection.split('\n')
                for line in lines:
                    if "recommendation" in line.lower():
                        suggestions.append(line.split(':', 1)[1].strip())

        return suggestions if suggestions else None
```

### Agent Frameworks

#### LangChain Agents

```python
from langchain.agents import initialize_agent, Tool, AgentExecutor
from langchain.chat_models import ChatOpenAI
from langchain.utilities import SerpAPIWrapper

# Initialize LLM
llm = ChatOpenAI(temperature=0)

# Define tools
search = SerpAPIWrapper()
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="Search for recent information"
    )
]

# Initialize agent
agent = initialize_agent(
    tools,
    llm=llm,
    agent="chat-zero-shot-react-description",
    verbose=True
)

# Create executor
executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True
)

# Run agent
result = executor.run("What is the latest news about AI?")
print(result)
```

#### AutoGPT Patterns

```python
from langchain.experimental import AutoGPT
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(temperature=0)

# Define tools
tools = [
    {
        "name": "google_search",
        "description": "Search Google for information",
        "func": google_search,
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string"}
            },
            "required": ["query"]
        }
    }
]

# Create AutoGPT agent
agent = AutoGPT.from_llm_and_tools(
    llm,
    tools,
    agent_type="zero-shot-react-description",
    verbose=True
)

# Run agent
result = agent.run([
    "Research latest developments in AI",
    "Summarize key findings",
    "Provide recommendations"
])
print(result)
```

#### CrewAI

```python
from crewai import Agent, Task, Crew, Process
from crewai.tools import SerperDevTool

# Define agents
researcher = Agent(
    role='Researcher',
    goal='Find and analyze information',
    backstory='You are an expert researcher.',
    verbose=True,
    tools=[SerperDevTool()]
)

writer = Agent(
    role='Writer',
    goal='Create engaging content based on research',
    backstory='You are a skilled writer.',
    verbose=True
)

# Define tasks
research_task = Task(
    description='Research latest AI developments',
    agent=researcher,
    expected_output='Detailed research findings'
)

write_task = Task(
    description='Write a blog post about AI developments',
    agent=writer,
    context=[research_task],
    expected_output='Final blog post'
)

# Create crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential,
    verbose=True
)

# Execute crew
result = crew.kickoff()
print(result)
```

#### Semantic Kernel

```python
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureOpenAIChatCompletion

# Initialize kernel
kernel = sk.Kernel()

kernel.add_chat_service("chat-gpt", AzureOpenAIChatCompletion())

# Define plugin
class WeatherPlugin:
    @sk.kernel_function(
        description="Get the current weather for a location",
        name="get_weather"
    )
    def get_weather(location: str) -> str:
        # Call weather API
        return f"Weather in {location}: Sunny, 22°C"

# Add plugin to kernel
kernel.add_plugin(WeatherPlugin())

# Create agent
agent = sk.ChatCompletionAgent(
    service_id="chat-gpt",
    kernel=kernel,
    instructions="You are a helpful assistant with access to weather information."
)

# Run agent
result = agent.chat("What's the weather in Tokyo?")
print(result)
```

### Tool Design for Agents

#### Tool Naming Conventions

```python
# Good tool names
GOOD_TOOL_NAMES = [
    "search_database",      # Clear, descriptive
    "calculate_sum",        # Action-oriented
    "get_user_profile",     # Get + resource
    "send_email",          # Action + resource
    "validate_address",    # Action + resource
]

# Bad tool names
BAD_TOOL_NAMES = [
    "tool1",              # Not descriptive
    "do_stuff",           # Vague
    "helper",             # Generic
    "func",               # Abbreviated
]
```

#### Tool Documentation

```python
def search_products(
    query: str,
    category: str = None,
    min_price: float = None,
    max_price: float = None,
    limit: int = 10
) -> dict:
    """
    Search for products in catalog.

    Args:
        query: Search query - can include product name, category, or keywords
        category: Filter by specific category (optional)
        min_price: Minimum price filter (optional)
        max_price: Maximum price filter (optional)
        limit: Maximum number of results to return (default: 10)

    Returns:
        dict: Dictionary containing:
            - success: Whether the search was successful
            - results: List of matching products
            - total: Total number of matches
            - error: Error message if unsuccessful
    """

    # Implementation
    try:
        # Build query
        db_query = "SELECT * FROM products WHERE name LIKE ?"
        params = [f"%{query}%"]

        if category:
            db_query += " AND category = ?"
            params.append(category)

        if min_price is not None:
            db_query += " AND price >= ?"
            params.append(min_price)

        if max_price is not None:
            db_query += " AND price <= ?"
            params.append(max_price)

        db_query += f" LIMIT {limit}"

        # Execute query
        cursor.execute(db_query, params)
        results = cursor.fetchall()

        return {
            "success": True,
            "results": results,
            "total": len(results)
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
```

#### Error Handling in Tools

```python
from typing import Optional, Dict, Any

class ToolError(Exception):
    """Custom exception for tool errors"""
    pass

def safe_tool_execute(tool_name: str, arguments: Dict, tool_handler) -> Dict[str, Any]:
    """
    Execute a tool with comprehensive error handling

    Args:
        tool_name: Name of tool to execute
        arguments: Arguments to pass to the tool
        tool_handler: The tool handler function

    Returns:
        dict: Result dictionary with success status and either result or error
    """

    try:
        # Validate arguments
        validation_result = validate_tool_arguments(tool_name, arguments)
        if not validation_result["valid"]:
            return {
                "success": False,
                "error": validation_result["error"],
                "error_code": "VALIDATION_ERROR"
            }

        # Execute tool
        result = tool_handler(**arguments)

        return {
            "success": True,
            "result": result
        }

    except ToolError as e:
        return {
            "success": False,
            "error": e.message,
            "error_code": "TOOL_ERROR"
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
            "error_code": "UNEXPECTED_ERROR"
        }

def validate_tool_arguments(tool_name: str, arguments: Dict) -> Dict[str, Any]:
    """Validate tool arguments"""
    errors = []

    # Check for missing required parameters
    required_params = get_required_params(tool_name)
    for param in required_params:
        if param not in arguments:
            errors.append(f"Missing required parameter: {param}")

    # Validate parameter types
    param_types = get_param_types(tool_name)
    for param, value in arguments.items():
        if param in param_types:
            expected_type = param_types[param]
            if not isinstance(value, expected_type):
                errors.append(f"Parameter {param} should be {expected_type.__name__}")

    return {
        "valid": len(errors) == 0,
        "error": "; ".join(errors) if errors else None
    }
```

### Memory Patterns

#### Conversation Buffer

```python
class ConversationBuffer:
    def __init__(self, max_messages=20):
        self.messages = []
        self.max_messages = max_messages

    def add(self, role, content):
        """Add a message to the buffer"""
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })

        # Trim if exceeds max
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

    def get_recent(self, n=10):
        """Get n most recent messages"""
        return self.messages[-n:]

    def get_all(self):
        """Get all messages"""
        return self.messages

    def clear(self):
        """Clear all messages"""
        self.messages = []

    def get_context_string(self):
        """Get formatted context for LLM"""
        if not self.messages:
            return ""

        return "\n".join([
            f"{msg['role']}: {msg['content']}"
            for msg in self.messages
        ])
```

#### Summary Memory

```python
class SummaryMemory:
    def __init__(self, llm_client):
        self.client = llm_client
        self.summaries = {}

    def add_messages(self, messages):
        """Add messages and create summary"""
        if not messages:
            return

        # Create summary
        text = "\n".join([m["content"] for m in messages])

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "Summarize the following conversation in 2-3 sentences."
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )

        summary = response.choices[0].message.content
        key = self.generate_key(messages)

        self.summaries[key] = {
            "summary": summary,
            "messages": messages,
            "timestamp": datetime.now().isoformat()
        }

    def create_summary(self, messages):
        """Create a summary of messages"""
        text = "\n".join([m["content"] for m in messages])

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "Summarize the following conversation in 2-3 sentences."
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )

        return response.choices[0].message.content

    def generate_key(self, messages):
        """Generate a key for storing the summary"""
        # Use first message as key
        if messages:
            return messages[0]["content"][:50]  # First 50 chars
        return "default"
```

#### Vector Memory

```python
class VectorMemory:
    def __init__(self, vector_db):
        self.vector_db = vector_db
        self.embeddings = {}

    def add(self, key: str, value: str, metadata: dict = None):
        """Add a memory with embedding"""
        # Generate embedding
        embedding = self.generate_embedding(value)

        # Store in vector database
        self.vector_db.upsert([{
            "id": key,
            "values": embedding,
            "metadata": metadata or {"text": value}
        }])

        self.embeddings[key] = {
            "value": value,
            "embedding": embedding,
            "metadata": metadata,
            "timestamp": datetime.now().isoformat()
        }

    def search(self, query: str, top_k: int = 5):
        """Search for relevant memories"""
        query_embedding = self.generate_embedding(query)

        results = self.vector_db.query(
            vector=query_embedding.tolist(),
            top_k=top_k
        )

        return [
            {
                "key": r["id"],
                "value": r["metadata"]["text"],
                "score": r["score"],
                "metadata": r["metadata"]
            }
            for r in results["matches"]
        ]

    def generate_embedding(self, text: str):
        """Generate embedding for text"""
        # Use cached embeddings if available
        if text in self.embeddings:
            return self.embeddings[text]["embedding"]

        # Generate new embedding
        # Implementation depends on embedding model
        embedding = get_embedding_from_model(text)
        return embedding
```

### Multi-Agent Systems

#### Agent Collaboration

```python
class MultiAgentSystem:
    def __init__(self, agents):
        self.agents = agents
        self.message_bus = []

    def send_message(self, from_agent: str, to_agent: str, message: dict):
        """Send a message from one agent to another"""
        msg = {
            "from": from_agent,
            "to": to_agent,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        self.message_bus.append(msg)

    def get_messages_for_agent(self, agent_name: str):
        """Get messages for a specific agent"""
        return [
            msg for msg in self.message_bus
            if msg["to"] == agent_name
        ]

    def broadcast(self, from_agent: str, message: dict):
        """Broadcast a message to all agents"""
        for agent in self.agents:
            if agent != from_agent:
                self.send_message(from_agent, agent, message)

# Usage
system = MultiAgentSystem(["researcher", "analyzer", "writer"])

# Researcher sends findings to analyzer
system.send_message("researcher", "analyzer", {
    "type": "research_complete",
    "data": {"topic": "AI trends", "findings": "..."}
})

# Analyzer sends summary to writer
system.send_message("analyzer", "writer", {
    "type": "analysis_complete",
    "summary": "Key trends: ..."
})
```

#### Agent Delegation

```python
class DelegatingAgent:
    def __init__(self, llm_client, sub_agents):
        self.client = llm_client
        self.sub_agents = sub_agents

    def delegate_task(self, task: str, context: dict):
        """Delegate a task to appropriate sub-agent"""

        # Determine which agent should handle the task
        agent = self.select_agent(task, context)

        # Delegate to agent
        result = agent.execute(task, context)

        return {
            "delegated_to": agent.name,
            "result": result
        }

    def select_agent(self, task: str, context: dict):
        """Select best agent for the task"""
        task_lower = task.lower()

        # Simple keyword matching
        scores = []
        for agent in self.sub_agents:
            score = 0
            for keyword in agent.keywords:
                if keyword in task_lower:
                    score += 1

            scores.append((score, agent))

        # Return agent with highest score
        if scores:
            return max(scores, key=lambda x: x[0])[1]

        # Default to first agent
        return self.sub_agents[0]

# Usage
delegator = DelegatingAgent(client, [searcher, analyzer, writer])
result = delegator.delegate_task("Search for Python tutorials", {})
```

#### Supervisor Pattern

```python
class SupervisorAgent:
    def __init__(self, llm_client, workers):
        self.client = llm_client
        self.workers = workers
        self.task_queue = []
        self.completed_tasks = []

    def assign_task(self, task: dict):
        """Assign a task to an available worker"""
        # Find best worker for task
        worker = self.select_worker(task)

        # Assign task
        task["worker"] = worker.name
        task["status"] = "assigned"
        task["assigned_at"] = datetime.now().isoformat()

        self.task_queue.append(task)

        return worker.execute(task)

    def select_worker(self, task: dict):
        """Select best worker for a task"""
        task_type = task.get("type", "")

        # Find workers that can handle this task type
        eligible_workers = [
            w for w in self.workers
            if task_type in w.capabilities
        ]

        if not eligible_workers:
            return self.workers[0]

        # Select worker with lowest load
        return min(eligible_workers, key=lambda w: w.current_tasks)

    def get_status(self):
        """Get overall status"""
        assigned = len([t for t in self.task_queue if t["status"] == "assigned"])
        completed = len(self.completed_tasks)

        return {
            "total_tasks": assigned + completed,
            "assigned": assigned,
            "completed": completed,
            "workers": {w.name: w.current_tasks for w in self.workers}
        }
```

### Error Recovery and Self-Correction

#### Retry with Backoff

```python
import time
import random

class RetryHandler:
    def __init__(self, max_retries=3, base_delay=1, max_delay=60):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay

    def execute_with_retry(self, func, *args, **kwargs):
        """Execute function with exponential backoff retry"""
        last_exception = None

        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                if attempt < self.max_retries - 1:
                    # Calculate delay with jitter
                    delay = min(
                        self.base_delay * (2 ** attempt),
                        self.max_delay
                    )
                    jitter = random.uniform(0.8, 1.2)
                    time.sleep(delay * jitter)
                else:
                    # Last attempt failed
                    raise e

        # All retries failed
        raise last_exception

# Usage
@RetryHandler(max_retries=3)
def unreliable_tool_call(data):
    # May fail occasionally
    if random.random() < 0.3:
        raise Exception("Random failure")
    return {"result": data}

result = unreliable_tool_call("test data")
```

#### Fallback Strategies

```python
class FallbackManager:
    def __init__(self):
        self.primary_tools = {}
        self.fallback_tools = {}

    def register_tool(self, name, primary, fallback):
        """Register a tool with primary and fallback"""
        self.primary_tools[name] = primary
        self.fallback_tools[name] = fallback

    def execute(self, tool_name, arguments):
        """Execute tool with fallback"""
        # Try primary tool
        try:
            result = self.primary_tools[tool_name](**arguments)
            return {
                "success": True,
                "result": result,
                "method": "primary"
            }
        except Exception as e:
            # Use fallback
            if tool_name in self.fallback_tools:
                try:
                    result = self.fallback_tools[tool_name](**arguments)
                    return {
                        "success": True,
                        "result": result,
                        "method": "fallback",
                        "warning": f"Primary tool failed: {str(e)}"
                    }
                except Exception as fe:
                    return {
                        "success": False,
                        "error": f"Both primary and fallback failed: {str(fe)}"
                    }
            else:
                return {
                    "success": False,
                    "error": f"Tool failed: {str(e)}"
                }

# Usage
def primary_search(query):
    # May fail
    if random.random() < 0.2:
        raise Exception("Search service unavailable")
    return {"results": []}

def fallback_search(query):
    # Simpler, more reliable
    return {"results": ["fallback result"]}

manager = FallbackManager()
manager.register_tool("search", primary_search, fallback_search)
```

#### Learning from Failures

```python
class LearningAgent:
    def __init__(self, llm_client):
        self.client = llm_client
        self.failure_history = []
        self.success_patterns = {}

    def record_failure(self, action, error):
        """Record a failure for learning"""
        self.failure_history.append({
            "action": action,
            "error": str(error),
            "timestamp": datetime.now().isoformat()
        })

    def record_success(self, action, result):
        """Record a successful action"""
        pattern = self.extract_pattern(action)

        if pattern not in self.success_patterns:
            self.success_patterns[pattern] = 0

        self.success_patterns[pattern] += 1

    def extract_pattern(self, action):
        """Extract pattern from action"""
        # Simple pattern extraction
        if "search" in action.lower():
            return "search"
        elif "calculate" in action.lower():
            return "calculate"
        else:
            return "unknown"

    def get_recommendation(self, action):
        """Get recommendation based on failure history"""
        pattern = self.extract_pattern(action)

        # Find similar failures
        similar_failures = [
            f for f in self.failure_history
            if pattern in f["action"].lower()
        ]

        if similar_failures:
            # Analyze common failure reasons
            error_types = [f["error"] for f in similar_failures]
            from collections import Counter
            common_error = Counter(error_types).most_common(1)[0]

            # Get most common error
            suggestions = {
                "timeout": "Try increasing timeout or using a faster endpoint",
                "rate_limit": "Implement rate limiting and retry with backoff",
                "invalid_input": "Add better input validation",
                "permission": "Check user permissions before executing",
                "network": "Check network connectivity and try alternative endpoint"
            }

            return suggestions.get(common_error, "Try again with different parameters")
```

## Guardrails and Safety

### Output Validation

```python
import re

class OutputValidator:
    def __init__(self):
        self.rules = {
            "no_code_execution": True,
            "no_pii": True,
            "max_length": 1000,
            "allowed_patterns": []
        }

    def validate(self, output: str) -> dict:
        """Validate agent output against rules"""
        violations = []

        # Check for code execution
        if self.rules["no_code_execution"]:
            code_patterns = [
                r'```.*?python',
                r'```.*?javascript',
                r'```.*?bash',
                r'exec\(',
                r'eval\('
            ]
            for pattern in code_patterns:
                if re.search(pattern, output, re.IGNORECASE):
                    violations.append("Contains code execution attempt")

        # Check for PII
        if self.rules["no_pii"]:
            pii_patterns = [
                r'\b\d{3}[-.\d{2}[-.\d{4}\b',  # SSN
                r'\b\d{3}[-.\d{2}[-.\d{4}\b',  # Phone
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',  # Email
                r'\b\d{16}\b'  # Credit card
            ]
            for pattern in pii_patterns:
                if re.search(pattern, output):
                    violations.append("Contains potential PII")

        # Check length
        if len(output) > self.rules["max_length"]:
            violations.append(f"Output too long ({len(output)} chars)")

        # Check allowed patterns
        if self.rules["allowed_patterns"]:
            for pattern in self.rules["allowed_patterns"]:
                if not re.search(pattern, output):
                    violations.append(f"Does not match required pattern: {pattern}")

        return {
            "valid": len(violations) == 0,
            "violations": violations
        }
```

### Action Limits

```python
class ActionLimiter:
    def __init__(self, max_actions_per_minute=10, max_actions_per_hour=100):
        self.max_per_minute = max_actions_per_minute
        self.max_per_hour = max_actions_per_hour
        self.action_log = []

    def check_limit(self, action_type: str) -> bool:
        """Check if action is allowed"""
        now = datetime.now()
        minute_ago = now - timedelta(minutes=1)
        hour_ago = now - timedelta(hours=1)

        # Count actions in last minute
        recent_minute = [
            a for a in self.action_log
            if a["type"] == action_type and a["timestamp"] > minute_ago.isoformat()
        ]

        if len(recent_minute) >= self.max_per_minute:
            return False

        # Count actions in last hour
        recent_hour = [
            a for a in self.action_log
            if a["type"] == action_type and a["timestamp"] > hour_ago.isoformat()
        ]

        if len(recent_hour) >= self.max_per_hour:
            return False

        return True

    def record_action(self, action_type: str, details: dict = None):
        """Record an action"""
        self.action_log.append({
            "type": action_type,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })

        # Clean old logs (keep last 24 hours)
        day_ago = (datetime.now() - timedelta(hours=24)).isoformat()
        self.action_log = [
            a for a in self.action_log
            if a["timestamp"] > day_ago
        ]
```

### Human-in-the-Loop

```python
class HumanApprovalFlow:
    def __init__(self):
        self.pending_approvals = {}
        self.approved_actions = {}

    def request_approval(self, agent_name: str, action: dict, user_id: str):
        """Request human approval for an action"""
        approval_id = f"{agent_name}_{datetime.now().timestamp()}"

        self.pending_approvals[approval_id] = {
            "agent": agent_name,
            "action": action,
            "user_id": user_id,
            "requested_at": datetime.now().isoformat(),
            "status": "pending"
        }

        # Notify user (implementation depends on your notification system)
        self.notify_user(user_id, approval_id, action)

        return {
            "approval_id": approval_id,
            "status": "pending"
        }

    def approve_action(self, approval_id: str):
        """Approve a pending action"""
        if approval_id not in self.pending_approvals:
            return {"error": "Approval not found"}

        approval = self.pending_approvals[approval_id]

        # Execute action
        result = self.execute_action(approval["action"])

        # Record approval
        self.approved_actions[approval_id] = {
            "approval": approval,
            "executed_at": datetime.now().isoformat(),
            "result": result
        }

        # Remove from pending
        del self.pending_approvals[approval_id]

        return result

    def reject_action(self, approval_id: str, reason: str):
        """Reject a pending action"""
        if approval_id not in self.pending_approvals:
            return {"error": "Approval not found"}

        approval = self.pending_approvals[approval_id]

        # Record rejection
        self.approved_actions[approval_id] = {
            "approval": approval,
            "rejected_at": datetime.now().isoformat(),
            "reason": reason
        }

        # Remove from pending
        del self.pending_approvals[approval_id]

        return {"status": "rejected", "reason": reason}
```

## Evaluation and Testing

### Unit Testing Agents

```python
import pytest
from unittest.mock import Mock, patch

def test_agent_tool_execution():
    """Test agent tool execution"""
    # Mock LLM response
    with patch('openai.OpenAI') as mock_openai:
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message = Mock()
        mock_response.choices[0].message.function_calls = [
            Mock(name="test_tool", arguments='{"param": "value"}')
        ]

        mock_client.chat.completions.create.return_value = mock_response

        # Test
        agent = Agent(mock_client, [test_tool])
        result = agent.run("Test query")

        # Verify tool was called
        assert mock_response.choices[0].message.function_calls[0].name == "test_tool"
```

### Integration Testing

```python
def test_end_to_end_agent_workflow():
    """Test complete agent workflow"""
    # Setup test environment
    llm_client = OpenAI()
    tools = [search_tool, database_tool]

    # Create agent
    agent = ReActAgent(llm_client, tools)

    # Test scenario
    user_query = "Find me information about Python programming"

    # Run agent
    result = agent.run(user_query)

    # Verify workflow
    assert len(result) > 0  # Agent produced output

    # Check if tools were called
    tool_calls = [msg for msg in result if msg.get("role") == "function"]
    assert len(tool_calls) > 0  # Tools were used

    # Verify final answer
    final_answer = [msg for msg in result if msg.get("role") == "assistant"]][-1]
    assert "Python" in final_answer.get("content", "")  # Answer is relevant
```

### Cost Management

```python
class AgentCostTracker:
    def __init__(self):
        self.tool_costs = {}
        self.llm_costs = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_cost": 0
        }

    def track_tool_call(self, tool_name: str, arguments: dict):
        """Track tool execution cost"""
        # Estimate tool cost (could be API calls, compute time, etc.)
        cost = self.estimate_tool_cost(tool_name, arguments)

        self.tool_costs[tool_name] = self.tool_costs.get(tool_name, 0) + cost
        return cost

    def track_llm_call(self, prompt_tokens: int, completion_tokens: int):
        """Track LLM API cost"""
        # GPT-4 pricing (example)
        prompt_cost = prompt_tokens * 0.00003  # $0.03 per 1K tokens
        completion_cost = completion_tokens * 0.00006  # $0.06 per 1K tokens

        self.llm_costs["prompt_tokens"] += prompt_tokens
        self.llm_costs["completion_tokens"] += completion_tokens
        self.llm_costs["total_cost"] += prompt_cost + completion_cost

        return prompt_cost + completion_cost

    def get_total_cost(self):
        """Get total cost of agent execution"""
        tool_cost = sum(self.tool_costs.values())
        llm_cost = self.llm_costs["total_cost"]

        return {
            "tool_calls": tool_cost,
            "llm_calls": llm_cost,
            "total": tool_cost + llm_cost
        }
```

## Observability and Debugging

### Agent Logging

```python
import logging

class AgentLogger:
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.logger = logging.getLogger(f"agent.{agent_name}")
        self.logger.setLevel(logging.DEBUG)

        # File handler
        handler = logging.FileHandler(f'logs/{agent_name}.log')
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_thought(self, thought: str):
        """Log agent thought process"""
        self.logger.debug(f"Thought: {thought}")

    def log_action(self, action: str, details: dict):
        """Log agent action"""
        self.logger.info(f"Action: {action}, Details: {details}")

    def log_tool_call(self, tool_name: str, arguments: dict, result):
        """Log tool execution"""
        self.logger.info(f"Tool: {tool_name}, Args: {arguments}, Result: {result}")

    def log_error(self, error: str, context: dict):
        """Log error"""
        self.logger.error(f"Error: {error}, Context: {context}")

    def log_completion(self, result: str):
        """Log task completion"""
        self.logger.info(f"Completed: {result}")
```

### Debugging Tools

```python
class AgentDebugger:
    def __init__(self, agent):
        self.agent = agent
        self.step_history = []

    def trace_execution(self, query: str):
        """Trace agent execution step by step"""
        self.step_history = []

        # Run agent with tracing
        original_run = self.agent.run

        # Capture each step
        for step in original_run:
            self.step_history.append({
                "step": len(self.step_history) + 1,
                "type": self.get_step_type(step),
                "content": step,
                "timestamp": datetime.now().isoformat()
            })

        return {
            "steps": self.step_history,
            "final_result": original_run[-1] if original_run else None
        }

    def get_step_type(self, step):
        """Determine step type"""
        content = str(step)

        if "Thought:" in content:
            return "thought"
        elif "Action:" in content:
            return "action"
        elif "Observation:" in content:
            return "observation"
        elif "Function:" in content:
            return "function_call"
        else:
            return "other"

    def visualize_trace(self):
        """Generate visualization of execution trace"""
        mermaid_diagram = "graph TD;\n"

        for step in self.step_history:
            step_num = step["step"]
            content = step["content"][:50]  # Truncate

            step_type = step["type"]

            if step_type == "thought":
                mermaid_diagram += f'S{step_num}[Thought: "{content}"]\n'
            elif step_type == "action":
                mermaid_diagram += f'S{step_num}[Action: "{content}"]\n'
            elif step_type == "observation":
                mermaid_diagram += f'S{step_num}[Observation: "{content}"]\n'
            elif step_type == "function_call":
                mermaid_diagram += f'S{step_num}[Function: "{content}"]\n'

        mermaid_diagram += "end;"

        return mermaid_diagram
```

## Production Deployment

### Deployment Considerations

```python
class ProductionAgentConfig:
    def __init__(self):
        self.config = {
            # LLM settings
            "model": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 4096,
            "timeout": 30,

            # Agent settings
            "max_iterations": 10,
            "max_tools_per_call": 5,

            # Safety settings
            "enable_guardrails": True,
            "require_human_approval_for": ["delete", "transfer"],
            "max_cost_per_session": 1.00,

            # Monitoring
            "enable_logging": True,
            "enable_tracing": True,
            "log_level": "INFO",

            # Performance
            "enable_caching": True,
            "cache_ttl": 300,
            "log_level": "INFO"
        }

    def validate(self) -> bool:
        """Validate configuration"""
        # Check for required settings
        required = ["model"]

        for key in required:
            if key not in self.config:
                return False

        # Validate values
        if self.config["temperature"] < 0 or self.config["temperature"] > 2:
            return False

        return True

    def get_llm_config(self) -> dict:
        """Get LLM configuration"""
        return {
            "model": self.config["model"],
            "temperature": self.config["temperature"],
            "max_tokens": self.config["max_tokens"],
            "timeout": self.config["timeout"]
        }
```

### Scaling Strategies

```python
class AgentPool:
    def __init__(self, agent_factory, pool_size=5):
        self.agent_factory = agent_factory
        self.pool_size = pool_size
        self.agents = []
        self.current_index = 0

    def initialize_pool(self):
        """Initialize agent pool"""
        for i in range(self.pool_size):
            agent = self.agent_factory(f"agent_{i}")
            self.agents.append(agent)

        return self.agents

    def get_agent(self) -> object:
        """Get next available agent (round-robin)"""
        if not self.agents:
            raise Exception("Agent pool not initialized")

        agent = self.agents[self.current_index]
        self.current_index = (self.current_index + 1) % self.pool_size

        return agent

    def get_all_agents(self) -> list:
        """Get all agents in pool"""
        return self.agents
```

## Common Use Cases

### Research Assistant

```python
class ResearchAssistantAgent:
    def __init__(self, llm_client, tools):
        self.client = llm_client
        self.tools = tools
        self.memory = ConversationBuffer(max_messages=20)

    def research(self, topic: str):
        """Conduct research on a topic"""
        # Phase 1: Plan research
        plan = self.create_research_plan(topic)

        # Phase 2: Execute research
        findings = []
        for step in plan:
            result = self.execute_research_step(step)
            findings.append(result)

        # Phase 3: Synthesize
        synthesis = self.synthesize_findings(findings)

        return {
            "topic": topic,
            "plan": plan,
            "findings": findings,
            "synthesis": synthesis
        }

    def create_research_plan(self, topic: str):
        """Create a research plan"""
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "Create a step-by-step research plan for: " + topic + "."
                },
                {"role": "user", "content": f"Research: {topic}"}
            ],
            tools=self.tools
        )

        return self.parse_plan(response.choices[0].message.content)

    def execute_research_step(self, step):
        """Execute a research step"""
        # Implementation
        return {"result": f"Research result for step"}

    def synthesize_findings(self, findings):
        """Synthesize findings into final answer"""
        return f"Synthesized report: {findings}"
```

### Code Generation Agent

```python
class CodeGenerationAgent:
    def __init__(self, llm_client):
        self.client = llm_client

    def generate_code(self, requirements: str, language: str = "python"):
        """Generate code based on requirements"""
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": f"""You are an expert {language} developer.
Generate clean, well-documented code based on requirements.
Include type hints and docstrings.
"""
                },
                {
                    "role": "user",
                    "content": f"Requirements: {requirements}"
                }
            ]
        )

        code = response.choices[0].message.content

        # Validate and format code
        return self.format_code(code)

    def format_code(self, code: str) -> str:
        """Format code with syntax highlighting"""
        # Add markdown code blocks
        if "```" not in code:
            code = f"```{language}\n{code}\n```"

        return code
```

### Customer Service Agent

```python
class CustomerServiceAgent:
    def __init__(self, llm_client, tools):
        self.client = llm_client
        self.tools = tools
        self.customer_db = None

    def handle_query(self, query: str, customer_id: str):
        """Handle customer service query"""
        # Get customer context
        customer = self.get_customer_context(customer_id)

        # Analyze query intent
        intent = self.analyze_intent(query)

        # Route to appropriate handler
        if intent == "order_status":
            return self.check_order_status(query, customer_id)
        elif intent == "refund_request":
            return self.process_refund(query, customer_id)
        elif intent == "product_info":
            return self.get_product_info(query)
        else:
            return self.general_inquiry(query)

    def analyze_intent(self, query: str) -> str:
        """Analyze customer query intent"""
        if "order" in query.lower() and "status" in query.lower():
            return "order_status"
        elif "refund" in query.lower():
            return "refund_request"
        elif "product" in query.lower():
            return "product_info"
        else:
            return "general_inquiry"

    def get_customer_context(self, customer_id: str):
        """Get customer context"""
        # Implementation
        return {"customer_id": customer_id, "data": {}}
```

### Data Analysis Agent

```python
class DataAnalysisAgent:
    def __init__(self, llm_client, tools):
        self.client = llm_client
        self.tools = tools

    def analyze_data(self, data: dict):
        """Analyze provided data"""
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": """You are a data analyst.
Analyze the provided data and provide insights.
Focus on trends, patterns, and actionable recommendations.

Available tools:
- search: Search for information
- calculate: Perform calculations
- database: Query database
"""
                },
                {
                    "role": "user",
                    "content": f"Data: {json.dumps(data)}"
                }
            ],
            tools=self.tools
        )

        analysis = response.choices[0].message.content

        return {
            "data": data,
            "analysis": analysis,
            "insights": self.extract_insights(analysis)
        }

    def extract_insights(self, analysis: str) -> list:
        """Extract key insights from analysis"""
        insights = []

        # Look for insight keywords
        insight_keywords = [
            "trend", "pattern", "recommendation", "anomaly", "increase", "decrease", "correlation"
        ]

        for keyword in insight_keywords:
            if keyword in analysis.lower():
                # Extract sentence containing keyword
                sentences = analysis.split('.')
                for sentence in sentences:
                    if keyword in sentence.lower():
                        insights.append(sentence.strip())

        return insights
```

## Best Practices

### Agent Design

- **Keep agents focused on specific tasks**
- **Use clear tool interfaces**
- **Implement proper error handling**
- **Add guardrails for safety**
- **Use appropriate memory types for your use case**
- **Implement memory retrieval strategies**
- **Regularly clean up old memories**
- **Index memories for efficient retrieval**
- **Log all agent decisions**
- - Track tool executions
- - Monitor costs
- - Set up alerts for anomalies
- **Implement debugging tools**

### Memory Management

- **Use appropriate memory types for your use case**
  - Short-term: For conversation context
  - Long-term: For persistent knowledge
  - Episodic: For specific experiences

- **Implement memory retrieval strategies**
  - Index memories for efficient retrieval
  - Regularly clean up old memories

### Tool Use

- **Design tools with clear interfaces**
- **Implement proper validation**
- **Use timeouts for tool execution**
- - Provide meaningful error messages**
- - Implement retry logic

### Planning

- **Break complex tasks into smaller steps**
- **Validate plans before execution**
- **Handle plan failures gracefully**
- **Allow for plan adjustments**

### Safety

- **Implement output validation**
- **Use human approval for critical actions**
- **Set action limits**
- **Monitor agent behavior**
- - Log all actions for audit
- - Set up alerts for anomalies

### Observability

- **Log all agent decisions**
- **Track tool executions**
- **Monitor costs**
- **Set up alerts for anomalies**
- **Implement debugging tools**

### Production Deployment

- **Use singleton pattern for model loading**
- **Configure appropriate timeouts**
- **Implement caching for performance**
- **Set up monitoring**
- **Use appropriate hardware**

## Related Skills

- [`06-ai-ml-production/llm-integration`](06-ai-ml-production/llm-integration/SKILL.md)
- [`06-ai-ml-production/prompt-engineering`](06-ai-ml-production/prompt-engineering/SKILL.md)
- [`06-ai-ml-production/llm-function-calling`](06-ai-ml-production/llm-function-calling/SKILL.md)
- [`54-agentops/tool-permission-model`](54-agentops/tool-permission-model/SKILL.md)
