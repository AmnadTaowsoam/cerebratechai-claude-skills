# AI Agents

## Overview

AI agents are autonomous systems that use language models to perform tasks, make decisions, and interact with users or other systems.

---

## 1. AI Agent Concepts

### What is an AI Agent?

```markdown
# AI Agent Concepts

## Definition
An AI agent is a system that uses language models to perceive, reason, and act autonomously to achieve goals.

## Key Components
- **Perception**: Understanding inputs (text, images, etc.)
- **Reasoning**: Processing information and making decisions
- **Action**: Taking actions based on reasoning
- **Memory**: Storing and retrieving information
- **Learning**: Improving over time

## Agent Types
- **Reactive**: Responds to inputs without planning
- **Proactive**: Plans and executes tasks
- **Collaborative**: Works with other agents
- **Hierarchical**: Has sub-agents for specific tasks
```

### Agent Capabilities

```markdown
# Agent Capabilities

## Core Capabilities
- **Natural Language Understanding**: Parse and understand text
- **Reasoning**: Make logical decisions
- **Planning**: Create and execute plans
- **Tool Use**: Use external tools and APIs
- **Memory**: Store and retrieve information
- **Learning**: Improve from experience

## Advanced Capabilities
- **Multi-Modal**: Process text, images, audio, video
- **Self-Reflection**: Evaluate own performance
- **Adaptation**: Adjust behavior based on feedback
- **Creativity**: Generate novel solutions
- **Collaboration**: Work with other agents
```

---

## 2. Agent Architectures

### ReAct Architecture

```markdown
# ReAct (Reason + Act) Architecture

## Concept
ReAct combines reasoning and acting in a loop: think, act, observe, adjust.

## Process
1. **Thought**: Agent thinks about what to do
2. **Action**: Agent performs an action
3. **Observation**: Agent observes the result
4. **Loop**: Repeat until goal is achieved

## Example
```
Thought: I need to search for information about Python
Action: Search("Python programming")
Observation: Found results about Python
Thought: I need to summarize the results
Action: Summarize(results)
Observation: Summary created
Thought: Goal achieved
Action: Done
```

## Implementation
```python
from langchain.agents import Agent, Tool
from langchain.tools import DuckDuckGoSearchRun

# Define tools
search = DuckDuckGoSearchRun()

# Define agent
agent = Agent(
    tools=[search],
    llm=llm,
    agent_type="zero-shot-react-description"
)

# Run agent
result = agent.run("What is Python programming?")
print(result)
```
```

### Plan-and-Execute Architecture

```markdown
# Plan-and-Execute Architecture

## Concept
Agent creates a plan first, then executes each step.

## Process
1. **Planning**: Agent creates a plan to achieve goal
2. **Execution**: Agent executes each step in the plan
3. **Adjustment**: Agent adjusts plan if needed
4. **Completion**: Agent completes all steps

## Example
```
Goal: Create a blog post about AI

Plan:
1. Research AI topics
2. Choose a topic
3. Create outline
4. Write content
5. Review and edit

Execution:
- Step 1: Research AI topics ✓
- Step 2: Choose "AI Agents" as topic ✓
- Step 3: Create outline ✓
- Step 4: Write content ✓
- Step 5: Review and edit ✓

Result: Blog post created
```

## Implementation
```python
from langchain.agents import AgentExecutor, create_pandas_dataframe_agent

# Define agent
agent = create_pandas_dataframe_agent(
    llm=llm,
    verbose=True
)

# Run agent
result = agent.run("Create a blog post about AI")
print(result)
```
```

### Reflexion Architecture

```markdown
# Reflexion Architecture

## Concept
Agent reflects on its actions and learns from mistakes.

## Process
1. **Action**: Agent performs an action
2. **Observation**: Agent observes the result
3. **Reflection**: Agent reflects on what happened
4. **Adjustment**: Agent adjusts its behavior
5. **Learning**: Agent learns from the experience

## Example
```
Action: Generated code with error
Observation: Code has syntax error
Reflection: I need to check my code for syntax errors
Adjustment: Add syntax checking step
Learning: Always check code for errors before generating

Next Action:
- Check code for syntax errors ✓
- Generate code ✓
- Verify code compiles ✓
```

## Implementation
```python
from langchain.agents import Agent, Tool
from langchain.memory import ConversationBufferMemory

# Define tools
code_tool = Tool(
    name="CodeExecutor",
    func=execute_code,
    description="Execute code and return output"
)

# Define agent with memory
agent = Agent(
    tools=[code_tool],
    llm=llm,
    memory=ConversationBufferMemory(),
    verbose=True
)

# Run agent
result = agent.run("Write a function to calculate factorial")
print(result)
```
```

---

## 3. Tools and Function Calling

### Tool Definition

```markdown
# Tool Definition

## What are Tools?
Tools are functions that agents can use to interact with external systems.

## Tool Structure
```python
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

class SearchInput(BaseModel):
    query: str = Field(description="Search query")

class SearchTool(BaseTool):
    name = "Search"
    description = "Search for information"
    args_schema = SearchInput
    
    def _run(self, query: str) -> str:
        # Implement search logic
        results = search_engine.search(query)
        return str(results)
```

## Tool Types
- **Search**: Search the web or databases
- **API**: Call external APIs
- **File**: Read and write files
- **Database**: Query and update databases
- **Code**: Execute code
- **System**: Perform system operations
```

### Function Calling

```markdown
# Function Calling

## Concept
Language models can call functions with structured arguments.

## OpenAI Function Calling
```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

# Define functions
functions = [
    {
        "name": "get_weather",
        "description": "Get the current weather",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state"
                }
            },
            "required": ["location"]
        }
    }
]

# Call function
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "What's the weather in San Francisco?"}],
    functions=functions
)

# Extract function call
if response.choices[0].message.function_call:
    function_name = response.choices[0].message.function_call.name
    function_args = json.loads(response.choices[0].message.function_call.arguments)
    
    # Call the function
    if function_name == "get_weather":
        result = get_weather(**function_args)
```

## LangChain Function Calling
```python
from langchain.tools import Tool
from langchain.agents import initialize_agent

# Define tool
class WeatherTool(Tool):
    name = "Weather"
    description = "Get weather information"
    
    def _run(self, location: str) -> str:
        # Implement weather API call
        return f"Weather in {location}"

# Initialize agent
agent = initialize_agent(
    tools=[WeatherTool()],
    llm=llm,
    agent_type="OPENAI_FUNCTIONS"
)

# Run agent
result = agent.run("What's the weather in New York?")
print(result)
```
```

---

## 4. Memory Systems

### Short-Term Memory

```markdown
# Short-Term Memory

## Purpose
Store recent interactions for context.

## Types
- **ConversationBuffer**: Store last N messages
- **ConversationBufferWindow**: Store last N tokens
- **ConversationSummaryMemory**: Summarize old conversations

## Implementation
```python
from langchain.memory import ConversationBufferMemory

# Create memory
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# Use memory
memory.save_context({"input": "Hello"})
memory.load_memory_variables({})
```

### Long-Term Memory

```markdown
# Long-Term Memory

## Purpose
Store important information across sessions.

## Types
- **Vector Memory**: Store embeddings for retrieval
- **Document Memory**: Store documents with metadata
- **Entity Memory**: Store information about entities
- **Summary Memory**: Store summaries of conversations

## Implementation
```python
from langchain.memory import VectorStoreRetrieverMemory
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

# Create vector store
vectorstore = Chroma.from_texts(
    texts=["text1", "text2", "text3"],
    embedding=OpenAIEmbeddings()
)

# Create memory with retrieval
memory = VectorStoreRetrieverMemory(
    retriever=vectorstore.as_retriever(),
    memory_key="chat_history"
)

# Use memory
memory.save_context({"input": "Tell me about text1"})
memory.load_memory_variables({})
```

### Vector Memory

```markdown
# Vector Memory

## Purpose
Store embeddings for semantic search and retrieval.

## Implementation
```python
from langchain.memory import VectorStoreRetrieverMemory
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain

# Create vector store
vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=OpenAIEmbeddings()
)

# Create retriever
retriever = vectorstore.as_retriever()

# Create memory
memory = VectorStoreRetrieverMemory(
    retriever=retriever,
    memory_key="chat_history"
)

# Create chain with memory
qa = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory
)

# Use chain
result = qa("What is the capital of France?")
print(result)
```
```

---

## 5. LangChain Agents

### Basic LangChain Agent

```python
from langchain.agents import Agent, Tool
from langchain.llms import OpenAI

# Define tools
search_tool = Tool(
    name="Search",
    func=search_function,
    description="Search for information"
)

calculator_tool = Tool(
    name="Calculator",
    func=calculator_function,
    description="Perform calculations"
)

# Create agent
agent = Agent(
    tools=[search_tool, calculator_tool],
    llm=OpenAI(temperature=0),
    verbose=True
)

# Run agent
result = agent.run("What is 25 * 42?")
print(result)
```

### Custom Agent

```python
from langchain.agents import AgentExecutor, Agent
from langchain.tools import Tool

# Define custom tools
class CustomTool(Tool):
    name = "CustomTool"
    description = "Perform custom action"
    
    def _run(self, input: str) -> str:
        # Implement custom logic
        return f"Custom action performed on {input}"

# Create agent
agent = Agent(
    tools=[CustomTool()],
    llm=llm,
    verbose=True
)

# Create executor
executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=[CustomTool()],
    verbose=True
)

# Run executor
result = executor.run("Perform custom action on data")
print(result)
```

### Multi-Agent System

```python
from langchain.agents import AgentExecutor, Agent, Tool

# Define specialized agents
researcher = Agent(
    tools=[search_tool],
    llm=llm,
    name="Researcher",
    verbose=True
)

writer = Agent(
    tools=[text_tool],
    llm=llm,
    name="Writer",
    verbose=True
)

# Create multi-agent executor
multi_agent = AgentExecutor.from_agents(
    agents=[researcher, writer],
    verbose=True
)

# Run multi-agent
result = multi_agent.run(
    "Research Python and write a blog post about it"
)
print(result)
```

---

## 6. OpenAI Assistants API

### Assistant Creation

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

# Create assistant
assistant = client.beta.assistants.create(
    name="Code Assistant",
    instructions="You are a helpful coding assistant.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4"
)

print(assistant.id)
```

### Thread Management

```python
# Create thread
thread = client.beta.threads.create()

# Add message to thread
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Write a function to calculate factorial"
)

# Run assistant on thread
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
)

# Check run status
run = client.beta.threads.runs.retrieve(
    thread_id=thread.id,
    run_id=run.id
)

# Get messages
messages = client.beta.threads.messages.list(thread_id=thread.id)
for msg in messages.data:
    print(msg.content)
```

### Function Calling with Assistants

```python
# Define functions
functions = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather information",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City and state"
                    }
                },
                "required": ["location"]
            }
        }
    }
]

# Create assistant with functions
assistant = client.beta.assistants.create(
    name="Weather Assistant",
    instructions="You are a helpful weather assistant.",
    tools=functions,
    model="gpt-4"
)

# Run assistant
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
)
```

---

## 7. Agent Planning and Reasoning

### Chain of Thought

```markdown
# Chain of Thought

## Concept
Agent thinks through problems step-by-step before answering.

## Implementation
```python
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate

# Define CoT prompt
cot_prompt = PromptTemplate.from_template(
    """Let's think step by step.

Question: {question}

Step 1: {step1}
Step 2: {step2}
Step 3: {step3}

Answer: {answer}"""
)

# Create chain
chain = ConversationChain(
    llm=llm,
    prompt=cot_prompt,
    verbose=True
)

# Run chain
result = chain.run(question="What is 25 * 42?")
print(result)
```

### ReAct Prompting

```python
from langchain.agents import Agent, Tool
from langchain.prompts import PromptTemplate

# Define ReAct prompt
react_prompt = PromptTemplate.from_template(
    """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Observation: the result of the action
... (this Thought/Action/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
{agent_scratchpad}"""
)

# Create agent with ReAct
agent = Agent(
    tools=[tool1, tool2, tool3],
    llm=llm,
    prompt=react_prompt,
    verbose=True
)

# Run agent
result = agent.run("What is the capital of France?")
print(result)
```

---

## 8. Error Handling and Fallbacks

### Error Handling

```python
from langchain.agents import Agent, Tool
from langchain.schema import OutputParserException

# Define tool with error handling
class SafeTool(Tool):
    name = "SafeTool"
    description = "Tool with error handling"
    
    def _run(self, input: str) -> str:
        try:
            # Implement tool logic
            result = self._execute(input)
            return result
        except Exception as e:
            # Handle error
            return f"Error: {str(e)}"

# Create agent with error handling
agent = Agent(
    tools=[SafeTool()],
    llm=llm,
    handle_parsing_errors=True,
    verbose=True
)

# Run agent
result = agent.run("Perform action")
print(result)
```

### Fallback Strategies

```python
from langchain.agents import Agent, Tool
from langchain.chains import LLMChain

# Define fallback LLM
fallback_llm = OpenAI(model="gpt-3.5-turbo")

# Create fallback chain
fallback_chain = LLMChain(llm=fallback_llm)

# Define agent with fallback
class FallbackAgent(Agent):
    def run(self, input: str):
        try:
            # Try primary agent
            result = super().run(input)
            return result
        except Exception as e:
            # Fallback to simpler model
            result = fallback_chain.run(input)
            return result

# Use fallback agent
agent = FallbackAgent(
    tools=[tool1, tool2],
    llm=llm,
    verbose=True
)

# Run agent
result = agent.run("What is the capital of France?")
print(result)
```

---

## 9. Human-in-the-Loop

### Human Feedback

```python
from langchain.agents import Agent, Tool
from langchain.schema import HumanMessage

# Define human feedback tool
class HumanFeedbackTool(Tool):
    name = "HumanFeedback"
    description = "Get human feedback on actions"
    
    def _run(self, action: str) -> str:
        # Request human feedback
        feedback = input(f"Was this action correct? {action} (yes/no): ")
        return feedback

# Create agent with human feedback
agent = Agent(
    tools=[tool1, tool2, HumanFeedbackTool()],
    llm=llm,
    verbose=True
)

# Run agent with human feedback
result = agent.run("Perform action that requires approval")
print(result)
```

### Interactive Agent

```python
from langchain.agents import AgentExecutor, Agent
from langchain.tools import Tool

# Define interactive agent
class InteractiveAgent(Agent):
    def run(self, input: str):
        while True:
            # Get agent's action
            action = self.plan(input)
            
            # Show action to human
            print(f"Agent wants to: {action}")
            
            # Get human approval
            approval = input("Approve? (yes/no): ")
            
            if approval.lower() == "yes":
                # Execute action
                result = self.execute(action)
                return result
            else:
                # Get feedback and adjust
                feedback = input("What should I do instead? ")
                self.adjust(feedback)

# Use interactive agent
agent = InteractiveAgent(
    tools=[tool1, tool2],
    llm=llm,
    verbose=True
)

# Run agent
result = agent.run("Perform complex task")
print(result)
```

---

## 10. Evaluation and Testing

### Agent Evaluation

```python
from langchain.evaluation import load_dataset, EvaluatorType
from langchain.smith import AgentExecutor, Tool

# Load evaluation dataset
dataset = load_dataset("agent-evaluation")

# Create evaluator
evaluator = AgentExecutor(
    agent=agent,
    tools=[tool1, tool2],
    llm=llm,
    verbose=True
)

# Evaluate agent
results = evaluator.evaluate_dataset(dataset)

# Calculate metrics
accuracy = sum(1 for r in results if r['success']) / len(results)
print(f"Accuracy: {accuracy}")
```

### Testing Strategies

```python
# Unit test agent tools
def test_tool():
    tool = MyTool()
    result = tool.run("test input")
    assert result == expected_output

# Integration test agent
def test_agent():
    agent = MyAgent()
    result = agent.run("test input")
    assert result['success'] == True

# End-to-end test agent
def test_e2e():
    agent = MyAgent()
    result = agent.run("complex task")
    assert result['output'] == expected_output
```

---

## 11. Production Considerations

### Deployment

```python
# Deploy agent as API
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Request(BaseModel):
    input: str

@app.post("/agent")
async def run_agent(request: Request):
    # Run agent
    result = agent.run(request.input)
    
    return result

# Run with uvicorn
# uvicorn main:app --host 0.0.0.0 --port 8000
```

### Monitoring

```python
# Monitor agent performance
import time

def monitored_agent_run(agent, input: str):
    start_time = time.time()
    
    # Run agent
    result = agent.run(input)
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Log metrics
    log_metrics({
        "input": input,
        "duration": duration,
        "success": result['success'],
        "tokens_used": result.get('tokens_used', 0)
    })
    
    return result

# Use monitored agent
result = monitored_agent_run(agent, "test input")
print(result)
```

### Cost Optimization

```python
# Optimize token usage
from langchain.callbacks import get_openai_callback

# Track token usage
token_tracker = get_openai_callback()

# Create agent with token tracking
agent = Agent(
    tools=[tool1, tool2],
    llm=llm,
    callbacks=[token_tracker],
    verbose=True
)

# Run agent
result = agent.run("test input")

# Get token usage
total_tokens = token_tracker.total_tokens
total_cost = total_tokens * 0.00002  # $0.02 per 1k tokens
print(f"Total tokens: {total_tokens}")
print(f"Total cost: ${total_cost}")
```

---

## 12. Example Use Cases

### Customer Service Agent

```python
from langchain.agents import Agent, Tool
from langchain.tools import Tool

# Define tools
search_knowledge_base = Tool(
    name="SearchKnowledgeBase",
    func=search_kb,
    description="Search customer knowledge base"
)

create_ticket = Tool(
    name="CreateTicket",
    func=create_support_ticket,
    description="Create support ticket"
)

# Create customer service agent
customer_service_agent = Agent(
    tools=[search_knowledge_base, create_ticket],
    llm=llm,
    instructions="You are a helpful customer service agent.",
    verbose=True
)

# Run agent
result = customer_service_agent.run("I need help with my order")
print(result)
```

### Research Agent

```python
from langchain.agents import Agent, Tool
from langchain.tools import DuckDuckGoSearchRun

# Define tools
search = DuckDuckGoSearchRun()

# Create research agent
research_agent = Agent(
    tools=[search],
    llm=llm,
    instructions="You are a research assistant. Search for information and provide detailed answers.",
    verbose=True
)

# Run agent
result = research_agent.run("Research the latest developments in AI")
print(result)
```

### Code Assistant Agent

```python
from langchain.agents import Agent, Tool
from langchain.tools import Tool

# Define tools
code_executor = Tool(
    name="CodeExecutor",
    func=execute_code,
    description="Execute code and return output"
)

# Create code assistant
code_assistant = Agent(
    tools=[code_executor],
    llm=llm,
    instructions="You are a coding assistant. Write code and execute it.",
    verbose=True
)

# Run agent
result = code_assistant.run("Write a function to calculate factorial")
print(result)
```
