---
name: AI Agents
description: Autonomous systems that use language models to perform tasks, make decisions, and interact with users or other systems using ReAct patterns, tool calling, and memory systems.
---

# AI Agents

> **Current Level:** Expert (Enterprise Scale)
> **Domain:** AI / Agent Systems

---

## Overview

AI agents are autonomous systems that use language models to perform tasks, make decisions, and interact with users or other systems. They combine reasoning (thinking) with action (doing) in iterative loops, enabling them to solve complex problems by breaking them down into smaller steps, using tools, and learning from feedback.

---

## 1. Executive Summary & Strategic Necessity

* **Context:** ในปี 2025-2026 AI Agents ได้กลายเป็นเทคโนโลยีที่จำเป็นสำหรับองค์องค์อัตโนมาติ การและการตัดสินใจ (Autonomous AI Agents) ด้วย ReAct Pattern และ Tool Calling ซึ่งเป็นมาตรฐานสำหรับ Enterprise Scale

* **Business Impact:** AI Agents ช่วยลด Downtime ของระบบ Customer Support ผ่านการตอบคำถามอัตโนมา (24/7), ลดต้นทุนการจัดการทีม (Reduce manual effort), เพิ่มอัตรากำไร Gross Margin ผ่านการทำงานอัตโนมาติ (Automated workflows), และปรับประสบทการทำงาน (Consistent quality)

* **Product Thinking:** AI Agents ช่วยแก้ปัญหา (Pain Point) ความต้องการมีระบบที่ซับซ้อนและต้องการทำงานซ้ำๆ (Repetitive tasks) ผ่านการทำงานอัตโนมาติ และการตัดสินใจ (Autonomous decision-making)

---

## 2. Technical Deep Dive (The "How-to")

* **Core Logic:** AI Agents ใช้ ReAct Pattern (Reason + Act) ซึ่งทำงานอัตโนมาติ โดยการวนลูปแบบ:
  1. **Thought**: Agent คิดคิดว่าจะทำอะไร (Think about what to do)
  2. **Action**: Agent ทำการกระทำตามที่คิด (Execute action based on thought)
  3. **Observation**: Agent สังเกตผลลัพธ์จากการกระทำ (Observe result of action)
  4. **Loop**: วนซ้ำจนกว่าจนถึงเป้าหรือไม่ (Repeat until goal achieved)

* **Architecture Diagram Requirements:** แผนผังระบบ AI Agent ต้องมีองค์ประกอบ:
  1. **LLM Integration**: Language Model สำหรับการคิดคิด (OpenAI GPT-4, Anthropic Claude, etc.)
  2. **Tool Registry**: เก็บเครื่องมือ (Tools) ที่ Agent สามารถใช้ (API calls, Database queries, File operations)
  3. **Memory System**: ระบบความจำ (Short-term: ConversationBuffer, Long-term: Vector Store)
  4. **Agent Executor**: ส่วนส่งคำสั่งและจัดการลำดับ (Max iterations, Timeout handling)
  5. **State Management**: จัดการสถานะของ Agent และ Conversation context
  6. **Observability**: Logging, Monitoring, Tracing สำหรับการ debug และปรับสิทท

* **Implementation Workflow:** ขั้นตอนการนำ AI Agent ไปใช้งานจริง:
  1. **Planning Phase**: กำหนด Requirement และเลือก Model ที่เหมาะสม
  2. **Tool Development**: สร้าง Tools ที่จำเป็นต้องสำหรับ Domain (Database, API, File system)
  3. **Memory Design**: ออกแบบ Memory architecture (Token-based, Vector-based, Hybrid)
  4. **Agent Implementation**: สร้าง Agent ด้วย LangChain หรือ Custom framework
  5. **Testing Phase**: Unit test Tools, Integration test Agent, E2E test ด้วยจริง Scenario
  6. **Deployment**: Deploy ด้วย API Gateway, Set up Rate limiting, Configure Monitoring
  7. **Optimization**: Tune prompts, Optimize token usage, Cache embeddings
  8. **Maintenance**: Monitor performance, Update Tools, Handle edge cases

---

## 3. Tooling & Tech Stack

* **Enterprise Tools:** เครื่องมือระดับอุตสาหกรรมที่เลือกใช้สำหรับ AI Agents:
  1. **LangChain**: Framework สำหรับสร้าง Agents ด้วย LLMs (Python, JavaScript)
  2. **AutoGPT**: Framework สำหรับ Autonomous Agents ด้วย Memory และ Tools
  3. **CrewAI**: Multi-agent orchestration สำหรับการจัดการหลาย Agents
  4. **OpenAI Assistants API**: Official API สำหรับสร้าง AI Assistants ด้วย Tools และ Code Interpreter
  5. **LangGraph**: Framework สำหรับ Stateful AI Agents ด้วย Graph-based workflows
  6. **Pinecone/Weaviate**: Vector Database สำหรับ Long-term Memory (Semantic search)
  7. **Redis**: Cache สำหรับ Short-term Memory และ Rate limiting
  8. **PostgreSQL**: Database สำหรับการจัดเก็บ Conversation History และ User data
  9. **Prometheus**: Monitoring สำหรับ Metrics (Token usage, Latency, Error rate)
  10. **Grafana**: Visualization dashboard สำหรับ Observability

* **Configuration Essentials:** การตั้งค่าสำคัญสำหรับให้ระบบเสถียร:
  1. **Model Configuration**: เลือก Model ตาม Use case (GPT-4 สำหรับ Complex reasoning, GPT-3.5-turbo สำหรับ Speed)
  2. **Token Budget**: ตั้ง max_tokens ตาม Budget และ Context window (4,000-8,000 tokens)
  3. **Temperature Settings**: 0.0-0.3 สำหรับ Creativity, 0.7 สำหรับ Deterministic
  4. **Rate Limiting**: 10-100 requests/minute ตาม User tier และ API limits
  5. **Timeout Configuration**: 30-60 seconds สำหรับ Agent execution, 5-10 seconds สำหรับ Tool calls
  6. **Memory Configuration**: 10-20 messages สำหรับ Short-term, 100-500 documents สำหรับ Vector search
  7. **Retry Policy**: Exponential backoff (base: 2, max: 5) ด้วย Jitter
  8. **Logging Level**: INFO สำหรับ Production, DEBUG สำหรับ Development
  9. **Monitoring**: Track success rate, token usage, latency, error rate ต่อเป้าหลาย
  10. **Secret Management**: Use Environment variables หรือ Secret Manager (AWS Secrets Manager, HashiCorp Vault)

---

## 4. Standards, Compliance & Security

* **International Standards:** มาตรฐานที่เกี่ยวข้อง:
  1. **ISO/IEC 27001**: Information Security Management - สำหรับการจัดการ Secrets และ Access Control
  2. **ISO/IEC 27017**: Code of Practice for Information Security Controls - สำหรับ Secure Development
  3. **GDPR**: General Data Protection Regulation - สำหรับการจัดการ Personal Data และ User Consent
  4. **SOC 2 Type II**: Security Controls - สำหรับการ Audit และ Compliance
  5. **OWASP Top 10**: Web Application Security - สำหรับการป้องกัน Prompt Injection และ Data Exposure

* **Security Protocol:** กลไกการป้องกัน AI Agents:
  1. **Input Validation**: Validate และ Sanitize ทุก Input ก่อนส่งให้ LLM หรือ Tools (Prevent prompt injection, SQL injection)
  2. **Output Sanitization**: Filter sensitive information จาก LLM output (PII, Secrets, Internal URLs)
  3. **Tool Permission Model**: RBAC (Role-Based Access Control) สำหรับ Tools - บาง Tools ต้องการ Admin permission, บาง Tools เปิดให้ทุก User
  4. **Audit Trail**: Log ทุก Agent action, Tool call, และ Decision ด้วย Timestamp, User ID, และ Result (สำหรับ Forensics และ Compliance)
  5. **Rate Limiting**: Per-user และ Per-API rate limits สำหรับป้องกัน Abuse (100-1000 requests/hour)
  6. **Secure Communication**: mTLS สำหรับ internal services, TLS 1.3 สำหรับ external APIs
  7. **Secret Rotation**: Rotate API keys ทุก 30-90 วัน (Automated key rotation)
  8. **Sandboxing**: Run Tools ใน isolated environment (Docker containers, Lambda functions)
  9. **Content Filtering**: Block malicious content, Adult content, และ Violations (Content moderation APIs)
  10. **Data Encryption**: Encrypt sensitive data ที่ rest ใน Database (AES-256 หรือ Customer-managed keys)

* **Explainability:** (สำหรับ AI) ความสามารถในการอธิบายผลลัพธ์ผ่านเทคนิค:
  1. **Chain of Thought Logging**: เก็บ Thought process ของ Agent สำหรับ Debugging และ Transparency
  2. **Tool Call Tracing**: Log ทุก Tool call ด้วย Input, Output, และ Execution time
  3. **Decision Reasoning**: บันทึกเหตุผลการตัดสินใจของ Agent (Why chose this action?)
  4. **Confidence Scoring**: ให้คะแนน (0-1) กับทุก Decision สำหรับการประเมิน
  5. **SHAP/LIME Integration**: ใช้ Explainability techniques สำหรับ complex decisions (Local explanations)
  6. **Human-in-the-Loop**: จัดการ Approval สำหรับ critical actions ด้วย Audit trail

---

## 5. Unit Economics & Performance Metrics (KPIs)

* **Cost Calculation:** สูตรการคำนวณต้นทุนต่อหน่วย AI Agents:
  1. **LLM Cost per Request** = (Input Tokens + Output Tokens) × Price per 1K tokens
     - GPT-4: $0.03/1K input + $0.06/1K output
     - GPT-3.5-turbo: $0.001/1K input + $0.002/1K output
     - Claude 3 Opus: $0.015/1K input + $0.075/1K output
  2. **Tool Execution Cost** = API calls × Cost per call
     - Database Query: $0.001 per query (PostgreSQL RDS)
     - External API: $0.01-0.10 per call (varies by service)
  3. **Vector Search Cost** = $0.001 per query (Pinecone)
  4. **Total Cost per Agent Run** = LLM Cost + Tool Costs + Vector Search Cost
  5. **Monthly Cost** = (Cost per Run × Runs per Month) + Infrastructure Costs
  6. **Infrastructure Costs** = Compute ($20-100/month) + Storage ($0.023/GB/month) + Monitoring ($10/month)

* **Key Performance Indicators:** ตัวชี้วัดความสำเร็จทางเทคนิค:
  1. **Success Rate**: อัตราการสำเร็จของ Agent (Target: >95%)
  2. **Average Latency**: เวลาการตอบกลับ (Target: <5 seconds สำหรับ single-turn, <30 seconds สำหรับ multi-turn)
  3. **Token Usage per Request**: เฉลี่ย Token เฉลี่ย Request (Target: <2,000 tokens)
  4. **Tool Call Success Rate**: อัตราการสำเร็จของ Tool calls (Target: >98%)
  5. **Average Tool Execution Time**: เวลาการทำงาน Tool (Target: <2 seconds)
  6. **User Satisfaction Score**: 1-5 rating จาก User feedback (Target: >4.0)
  7. **Error Rate**: อัตราการ Error (Target: <1%)
  8. **Concurrent Users**: จำนวยผู้ใช้งานพร้อมกัน (Peak: 100-1,000 concurrent sessions)
  9. **Cache Hit Rate**: อัตราการ Cache hit (Target: >80% สำหรับ repeated queries)
  10. **Agent Iterations per Request**: จำนวย iteration เฉลี่ย Request (Target: <5 iterations)

---

## 6. Strategic Recommendations (CTO Insights)

* **Phase Rollout:** คำแนะนำในการทยอยเริ่มใช้งาน AI Agents เพื่อลดความเสี่ยง:
  1. **Phase 1: MVP (1-2 เดือน)**: Deploy Simple Agent ด้วย 1-2 Tools (Database lookup, Web search) สำหรับ Internal team ก่อนเปิดให้ Public
     - **Goal**: Validate Agent architecture และ gather feedback
     - **Success Criteria**: >80% success rate, <10s latency
     - **Risk Mitigation**: Rate limiting, Manual review ก่อน Auto-approve
  2. **Phase 2: Beta (2-3 เดือน)**: Expand ด้วย 5-10 Tools และ Memory system สำหรับ Selected customers
     - **Goal**: Test scalability และ Tool reliability
     - **Success Criteria**: >90% success rate, <5s latency
     - **Risk Mitigation**: Canary deployment, Feature flags, Gradual rollout
  3. **Phase 3: GA (3-6 เดือน)**: Full rollout ด้วย 10-20 Tools, Advanced Memory, และ Multi-agent orchestration
     - **Goal**: Enterprise-grade reliability และ Performance
     - **Success Criteria**: >95% success rate, <3s latency, 99.9% uptime
     - **Risk Mitigation**: Load testing, Disaster recovery, Blue-green deployment

* **Pitfalls to Avoid:** ข้อควรระวังที่มักจะผิดพลาดในระดับ Enterprise Scale:
  1. **Over-engineering**: สร้าง Agent ที่ซับซ้อนเกินไป (Too many tools, Complex memory) → เริ่มจาก Simple และ iterate
  2. **No Rate Limiting**: ไม่มี Rate limits ทำให้ Cost blowout และ API abuse → Implement per-user และ per-endpoint limits ด้วย Redis
  3. **Infinite Loops**: Agent วนลูปไม่มีทางออก (Max iterations = ∞) → Set max_iterations=10 และ timeout=60s
  4. **Ignoring Tool Errors**: Tool failures crash Agent → Wrap Tools ด้วย try-catch และ return fallback response
  5. **No Context Management**: ส่งทุก message เป็น Independent → Implement sliding window และ summary
  6. **Hardcoding API Keys**: Keys ใน code ที่เปิดให้ Public → Use Environment variables หรือ Secret Manager
  7. **No Observability**: ไม่มี Logging/Tracing → Add structured logging ด้วย correlation IDs
  8. **Skipping Validation**: ไม่ Validate Tool inputs/outputs → Implement schema validation และ sanitization
  9. **Poor Prompt Design**: Vague prompts ทำให้ Agent hallucinate → Use specific, testable prompts ด้วย examples
  10. **Single Point of Failure**: ไม่มี Redundancy หรือ Fallback → Deploy multiple instances ด้วย Load balancer

---

## Core Concepts

### 1. AI Agent Concepts

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
Agent creates a plan first, then executes each step in the plan.

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
```

## Implementation
```python
from langchain.agents import Agent, Tool
from langchain.memory import ConversationBufferMemory

# Define tool
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
- **ConversationBufferWindowMemory**: Store last N tokens

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

# Create retriever
retriever = vectorstore.as_retriever()

# Create memory with retrieval
memory = VectorStoreRetrieverMemory(
    retriever=retriever,
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

# Create memory with retrieval
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
from langchain.tools import DuckDuckGoSearchRun

# Define tools
search_tool = DuckDuckGoSearchRun()

# Create agent
agent = Agent(
    tools=[search_tool],
    llm=OpenAI(temperature=0),
    verbose=True
)

# Run agent
result = agent.run("What is Python?")
print(result)
```

### Custom Agent

```python
from langchain.agents import AgentExecutor, Agent, Tool
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
result = executor.run("Perform custom action")
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
                        "description": "The city and state"
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
    instructions="You are a weather assistant.",
    tools=functions,
    model="gpt-4"
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
from langchain.agents import AgentExecutor, Agent, Tool

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

## Quick Start

### Minimal Setup

```python
from langchain.agents import Agent, Tool
from langchain.llms import OpenAI

# 1. Define a simple tool
def search_tool(query: str) -> str:
    """Search for information"""
    return f"Results for: {query}"

# 2. Create tool wrapper
search = Tool(
    name="Search",
    func=search_tool,
    description="Search for information"
)

# 3. Initialize LLM
llm = OpenAI(temperature=0)

# 4. Create agent
agent = Agent(
    tools=[search],
    llm=llm,
    verbose=True
)

# 5. Run agent
result = agent.run("What is Python?")
print(result)
```

### Installation

```bash
pip install langchain openai
export OPENAI_API_KEY="your-api-key"
```

### Next Steps

1. Add more tools (APIs, databases, file systems)
2. Implement memory for context retention
3. Add error handling and fallbacks
4. Set up monitoring and logging
```

---

## Production Checklist

- [ ] **Error Handling**: Implement try-catch blocks for all tool calls
- [ ] **Rate Limiting**: Add rate limits to prevent API abuse
- [ ] **Token Budget**: Set maximum token limits per agent run
- [ ] **Timeout**: Configure timeouts to prevent infinite loops
- [ ] **Logging**: Set up structured logging for all agent actions
- [ ] **Monitoring**: Add metrics for success rate, latency, token usage
- [ ] **Security**: Validate and sanitize all inputs
- [ ] **Cost Tracking**: Monitor API costs per agent execution
- [ ] **Max Iterations**: Set max_iterations to prevent infinite loops
- [ ] **Memory Management**: Implement context window for conversation history
- [ ] **Tool Permissions**: Implement RBAC for tool access control
- [ ] **Audit Trail**: Log all agent decisions and tool calls
- [ ] **Fallback Strategy**: Implement fallback mechanisms for failures
- [ ] **Input Validation**: Validate all inputs before processing
- [ ] **Output Sanitization**: Filter sensitive data from outputs
- [ ] **Retry Logic**: Implement exponential backoff for retries
- [ ] **Observability**: Add tracing and correlation IDs
- [ ] **Load Testing**: Test with expected traffic patterns
- [ ] **Disaster Recovery**: Implement backup and recovery procedures

---

## Anti-patterns

### ❌ Don't: Infinite Loops Without Limits

```python
# ❌ Bad - No max iterations
agent = Agent(
    tools=[tool1, tool2],
    llm=llm,
    # Missing max_iterations parameter
)
```

```python
# ✅ Good - Set iteration limits
agent = Agent(
    tools=[tool1, tool2],
    llm=llm,
    max_iterations=10,  # Prevent infinite loops
    max_execution_time=60  # Timeout after 60 seconds
)
```

### ❌ Don't: Ignore Tool Errors

```python
# ❌ Bad - No error handling
def tool_function(input: str) -> str:
    result = external_api.call(input)  # Can fail
    return result
```

```python
# ✅ Good - Handle errors gracefully
def tool_function(input: str) -> str:
    try:
        result = external_api.call(input)
        return result
    except APIError as e:
        logger.error(f"Tool error: {e}")
        return f"Error: {str(e)}"
```

### ❌ Don't: Expose Sensitive Data in Tool Descriptions

```python
# ❌ Bad - Exposes API keys
tool = Tool(
    name="Database",
    func=db_query,
    description=f"Query database at {DB_HOST} with key {API_KEY}"  # Security risk!
)
```

```python
# ✅ Good - Generic descriptions
tool = Tool(
    name="Database",
    func=db_query,
    description="Query the internal database for user information"
)
```

### ❌ Don't: No Memory Management

```python
# ❌ Bad - Each message is independent
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": input}]  # No history!
)
```

```python
# ✅ Good - Maintain conversation context
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        ...conversationHistory,  # Previous messages
        {"role": "user", "content": input}
    ]
)
```

### ❌ Don't: No Fallback Strategy

```python
# ❌ Bad - Fails if vector search fails
def search(query: str):
    return vector_search(query)  # No fallback
```

```python
# ✅ Good - Fallback to keyword search
def search(query: str):
    try:
        return vector_search(query)
    except Exception as e:
        logger.error(f"Vector search failed: {e}")
        return keyword_search(query)  # Fallback
```

### ❌ Don't: Trust Agent Output Without Validation

```python
# ❌ Bad - Direct execution
result = agent.run(user_input)
execute_code(result)  # Dangerous!
```

```python
# ✅ Good - Validate before execution
result = agent.run(user_input)
if validate_output(result):
    execute_code(result)
else:
    raise ValidationError("Agent output failed validation")
```

---

## Integration Points

- **LLM Integration** (`06-ai-ml-production/llm-integration/`) - Setting up LLM providers
- **Function Calling** (`06-ai-ml-production/llm-function-calling/`) - Tool and function definitions
- **RAG Implementation** (`06-ai-ml-production/rag-implementation/`) - Adding knowledge retrieval
- **Vector Search** (`06-ai-ml-production/vector-search/`) - Semantic memory systems
- **Error Handling** (`03-backend-api/error-handling/`) - Production error patterns

---

## Further Reading

- [LangChain Agents Documentation](https://python.langchain.com/docs/modules/agents/)
- [OpenAI Assistants API](https://platform.openai.com/docs/assistants/overview)
- [ReAct Paper](https://arxiv.org/abs/2210.03629)
- [Agent Patterns](https://github.com/langchain-ai/langchain/tree/master/templates)
