---
name: LLM Text Protocol
description: Standardized protocol for text-based interactions with language models, including prompt engineering, response formatting, and text processing patterns.
---

# LLM Text Protocol

> **Current Level:** Expert (Enterprise Scale)
> **Domain:** AI Integration / Language Models

---

## Overview

LLM Text Protocol provides standardized patterns for text-based interactions with language models. It encompasses prompt engineering, response formatting, and text processing patterns that ensure consistent, reliable, and effective communication with LLMs in production environments.

---

## 1. Executive Summary & Strategic Necessity

* **Context:** ในปี 2025-2026 LLM Text Protocol ด้วย ReAct Pattern และ Prompt Engineering ช่วย Text Processing ที่มีอัตโนมาติการทำงานอัตโนมาติ (LLM Text Protocol) ใน Enterprise Scale

* **Business Impact:** LLM Text Protocol ช่วยลด Downtime ของระบบ Customer Support ผ่านการตอบคำถามอัตโนมาติการประมวลผลข้อความ (Reduce processing time), ลดต้นทุนการจัดการทีม (Increase consistency), เพิ่มอัตรากำไร Gross Margin ผ่านการทำงานอัตโนมาติ (Automated workflows), และปรับประสบทการทำงาน (Consistent quality)

* **Product Thinking:** LLM Text Protocol ช่วยแก้ปัญหา (Pain Point) ความต้องการมีระบบประมวลผลข้อความอัตโนมาติ (Users need consistent text processing) ผ่านการทำงานอัตโนมาติ (Standardized protocols)

---

## 2. Technical Deep Dive (The "How-to")

* **Core Logic:** LLM Text Protocol ใช้ ReAct Pattern และ Prompt Engineering ช่วย Text Processing ทำงานอัตโนมาติ:
  1. **Prompt Engineering**: วิเคคิดความต้องการ (System prompt, User prompt, Few-shot examples)
  2. **Response Parsing**: แปลงข้อความเป็นโครงสร้าง (JSON, XML, YAML)
  3. **Validation**: ตรวจสอบผลลัพธ์ (Schema validation, Format validation)
  4. **Error Handling**: จัดการ Error (Retry, Fallback, Error messages)
  5. **State Management**: จัดการสถานะของ Conversation และ Context

* **Architecture Diagram Requirements:** แผนผังระบบ LLM Text Protocol ต้องมีองค์ประกอบ:
  1. **LLM Integration**: Language Model สำหรับการคิดคิด (OpenAI GPT-4, Anthropic Claude)
  2. **Prompt Template Engine**: Prompt templates สำหรับการสร้าง prompts (Jinja2, Mustache)
  3. **Response Parser**: Response parser สำหรับการแปลงข้อความ (JSON, XML, YAML)
  4. **Validator**: Validator สำหรับการตรวจสอบผลลัพธ์ (Schema validation, Format validation)
  5. **Error Handler**: Error handler สำหรับการจัดการ Error (Retry, Fallback)
  6. **API Gateway**: REST API ด้วย Rate limiting และ Authentication
  7. **Observability**: Logging, Monitoring, Tracing สำหรับการ debug และปรับสิทท

* **Implementation Workflow:** ขั้นตอนการนำ LLM Text Protocol ไปใช้งานจริง:
  1. **Planning Phase**: กำหนด Requirement และเลือก Model ที่เหมาะสม
  2. **Prompt Design**: ออกแบบ Prompt templates สำหรับการสร้าง prompts
  3. **Response Parsing**: สร้าง Response parser สำหรับการแปลงข้อความ
  4. **Validation**: สร้าง Validator สำหรับการตรวจสอบผลลัพธ์
  5. **Error Handling**: สร้าง Error handler สำหรับการจัดการ Error
  6. **Testing Phase**: Unit test, Integration test, E2E test ด้วยจริง Scenario
  7. **Deployment**: Deploy ด้วย API Gateway, Set up Rate limiting, Configure Monitoring
  8. **Optimization**: Tune prompts, Optimize token usage, Cache embeddings
  9. **Maintenance**: Monitor performance, Update Prompt templates, Handle edge cases

---

## 3. Tooling & Tech Stack

* **Enterprise Tools:** เครื่องมือระดับอุตสาหกรรมที่เลือกใช้สำหรับ LLM Text Protocol ใน Enterprise Scale:
  1. **OpenAI**: GPT-4, GPT-3.5-turbo, Embeddings (text-embedding-3-small, text-embedding-3-large)
  2. **Anthropic**: Claude 3 Opus, Claude 3 Sonnet, Claude 3 Haiku
  3. **LangChain**: Framework สำหรับสร้าง Prompts และ Response parsing (Python, JavaScript)
  4. **Jinja2**: Template engine สำหรับ Prompt templates
  5. **Pydantic**: Data validation สำหรับ Response validation
  6. **Redis**: Cache สำหรับ Short-term Memory และ Rate limiting
  7. **PostgreSQL**: Database สำหรับการจัดเก็บ Prompt templates และ Response history
  8. **Prometheus**: Monitoring สำหรับ Metrics (Token usage, Latency, Error rate)
  9. **Grafana**: Visualization dashboard สำหรับ Observability
  10. **PromptLayer**: Prompt management สำหรับการจัดการ Prompt versions

* **Configuration Essentials:** การตั้งค่าสำคัญสำหรับให้ระบบเสถียร LLM Text Protocol:
  1. **Model Configuration**: เลือก Model ตาม Use case (GPT-4 สำหรับ Complex reasoning, GPT-3.5-turbo สำหรับ Speed)
  2. **Token Budget**: ตั้ง max_tokens ตาม Budget และ Context window (4,000-8,000 tokens)
  3. **Temperature Settings**: 0.0-0.3 สำหรับ Creativity, 0.7 สำหรับ Deterministic
  4. **Rate Limiting**: 10-100 requests/minute ตาม User tier และ API limits
  5. **Timeout Configuration**: 30-60 seconds สำหรับ LLM execution, 5-10 seconds สำหรับ Tool calls
  6. **Retry Policy**: Exponential backoff (base: 2, max: 5) ด้วย Jitter
  7. **Logging Level**: INFO สำหรับ Production, DEBUG สำหรับ Development
  8. **Monitoring**: Track success rate, token usage, latency, error rate ต่อเป้าหลาย
  9. **Secret Management**: Use Environment variables หรือ Secret Manager (AWS Secrets Manager, HashiCorp Vault)

---

## 4. Standards, Compliance & Security

* **International Standards:** มาตรฐานที่เกี่ยวข้อง:
  1. **ISO/IEC 27001**: Information Security Management - สำหรับการจัดการ Secrets และ Access Control
  2. **ISO/IEC 27017**: Code of Practice for Information Security Controls - สำหรับ Secure Development
  3. **GDPR**: General Data Protection Regulation - สำหรับการจัดการ Personal Data และ User Consent
  4. **SOC 2 Type II**: Security Controls - สำหรับการ Audit และ Compliance
  5. **OWASP Top 10**: Web Application Security - สำหรับการป้องกัน Prompt Injection และ Data Exposure

* **Security Protocol:** กลไกการป้องกัน LLM Text Protocol:
  1. **Input Validation**: Validate และ Sanitize ทุก Input ก่อน LLM หรือ Tools (Prevent prompt injection, SQL injection)
  2. **Output Sanitization**: Filter sensitive information จาก LLM output (PII, Secrets, Internal URLs)
  3. **Tool Permission Model**: RBAC (Role-Based Access Control) สำหรับ Tools - บาง Tools Admin permission, บาง Tools เปิดให้ทุก User
  4. **Audit Trail**: Log ทุก LLM action, Tool call, และ Decision ด้วย Timestamp, User ID, และ Result (สำหรับ Forensics และ Compliance)
  5. **Rate Limiting**: Per-user และ Per-API rate limits สำหรับป้องกัน Abuse (100-1000 requests/hour)
  6. **Secure Communication**: mTLS สำหรับ internal services, TLS 1.3 สำหรับ external APIs
  7. **Secret Rotation**: Rotate API keys ทุก 30-90 วัน (Automated key rotation)
  8. **Sandboxing**: Run Tools ใน isolated environment (Docker containers, Lambda functions)
  9. **Content Filtering**: Block malicious content, Adult content, และ Violations (Content moderation APIs)
  10. **Data Encryption**: Encrypt sensitive data ที่ rest ใน Database (AES-256 หรือ Customer-managed keys)

* **Explainability:** (สำหรับ AI) ความสามารถในการอธิบายผลลัพธ์ผ่านเทคนิค:
  1. **Chain of Thought Logging**: เก็บ Thought process ของ LLM สำหรับ Debugging และ Transparency
  2. **Tool Call Tracing**: Log ทุก Tool call ด้วย Input, Output, และ Execution time
  3. **Decision Reasoning**: บันทึกเหตุผลการตัดสินใจของ LLM (Why chose this response?)
  4. **Confidence Scoring**: ให้คะแนน (0-1) กับทุก Decision สำหรับการประเมิน
  5. **Human-in-the-Loop**: จัดการ Approval สำหรับ critical actions ด้วย Audit trail

---

## 5. Unit Economics & Performance Metrics (KPIs)

* **Cost Calculation:** สูตรการคำนวณต้นทุนต่อหน่วย LLM Text Protocol:
  1. **LLM Cost per Request** = (Input Tokens + Output Tokens) × Price per 1K tokens
     - GPT-4: $0.03/1K input + $0.06/1K output
     - GPT-3.5-turbo: $0.001/1K input + $0.002/1K output
     - Claude 3 Opus: $0.015/1K input + $0.075/1K output
  2. **Tool Execution Cost** = API calls × Cost per call
     - Database Query: $0.001 per query (PostgreSQL RDS)
     - External API: $0.01-0.10 per call (varies by service)
  3. **Total Cost per Request** = LLM Cost + Tool Costs
  4. **Monthly Cost** = (Cost per Request × Requests per Month) + Infrastructure Costs
  5. **Infrastructure Costs** = Compute ($20-100/month) + Storage ($0.023/GB/month) + Monitoring ($10/month)

* **Key Performance Indicators:** ตัวชี้วัดความสำเร็จทางเทคนิค:
  1. **Success Rate**: อัตราการสำเร็จของ LLM (Target: >95%)
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

* **Phase Rollout:** คำแนะนำในการทยอยเริ่มใช้งาน LLM Text Protocol เพื่อลดความเสี่ยง:
  1. **Phase 1: MVP (1-2 เดือน)**: Deploy Simple LLM Text Protocol ด้วย 1-2 Prompt templates (Simple prompt, Response parsing) สำหรับ Internal team ก่อนเปิดให้ Public
     - **Goal**: Validate LLM Text Protocol architecture และ gather feedback
     - **Success Criteria**: >80% success rate, <10s latency
     - **Risk Mitigation**: Rate limiting, Manual review ก่อน Auto-approve
  2. **Phase 2: Beta (2-3 เดือน)**: Expand ด้วย 5-10 Prompt templates และ Response parsing (Complex prompts, JSON parsing) สำหรับ Selected customers
     - **Goal**: Test scalability และ Tool reliability
     - **Success Criteria**: >90% success rate, <5s latency
     - **Risk Mitigation**: Canary deployment, Feature flags, Gradual rollout
  3. **Phase 3: GA (3-6 เดือน)**: Full rollout ด้วย 10-20 Prompt templates, Advanced Response parsing, และ Multi-agent orchestration
     - **Goal**: Enterprise-grade reliability และ Performance
     - **Success Criteria**: >95% success rate, <3s latency, 99.9% uptime
     - **Risk Mitigation**: Load testing, Disaster recovery, Blue-green deployment

* **Pitfalls to Avoid:** ข้อควรระวังที่มักจะผิดพลาดในระดับ Enterprise Scale:
  1. **Over-engineering**: สร้าง LLM Text Protocol ที่ซ้อนเกินไป (Too many prompts, Complex parsing) → เริ่มจาก Simple และ iterate
  2. **No Rate Limiting**: ไม่มี Rate limits ทำให้ Cost blowout และ API abuse → Implement per-user และ per-endpoint limits ด้วย Redis
  3. **Infinite Loops**: LLM วนลูปไม่มีทางออก (Max iterations = ∞) → Set max_iterations=10 และ timeout=60s
  4. **Ignoring Tool Errors**: Tool failures crash LLM → Wrap Tools ด้วย try-catch และ return fallback response
  5. **No Context Management**: ส่งทุก message เป็น Independent → Implement sliding window และ summary
  6. **Hardcoding API Keys**: Keys ใน code ที่เปิดให้ Public → Use Environment variables หรือ Secret Manager
  7. **No Observability**: ไม่มี Logging/Tracing → Add structured logging ด้วย correlation IDs
  8. **Skipping Validation**: ไม่ Validate Tool inputs/outputs → Implement schema validation และ sanitization
  9. **Poor Prompt Design**: Vague prompts ทำให้ LLM hallucinate → Use specific, testable prompts ด้วย examples
  10. **Single Point of Failure**: ไม่มี Redundancy หรือ Fallback → Deploy multiple instances ด้วย Load balancer

---

## Core Concepts

### 1. Prompt Engineering

### What is Prompt Engineering?

```markdown
# Prompt Engineering

## Definition
Prompt engineering is the art of crafting effective prompts to get desired outputs from language models.

## Key Principles
- **Be Specific**: Clear, unambiguous instructions
- **Provide Context**: Give relevant background information
- **Use Examples**: Show what you want
- **Format Output**: Specify desired output format
- **Iterate**: Test and refine prompts

## Prompt Components
- **System Prompt**: Sets the model's behavior
- **User Prompt**: The actual request
- **Few-Shot Examples**: Example inputs and outputs
- **Format Instructions**: How to format the output
```

### Prompt Patterns

```markdown
# Prompt Patterns

## 1. Zero-Shot Prompting
No examples provided.

Example:
"Translate the following to Thai: Hello"

## 2. One-Shot Prompting
One example provided.

Example:
"Translate to Thai:
English: Hello
Thai: สวัสดี

Translate: Good morning"

## 3. Few-Shot Prompting
Multiple examples provided.

Example:
"Translate to Thai:
English: Hello
Thai: สวัสดี

English: Good morning
Thai: อรุณสวัสดิ์

English: Goodbye
Thai: ลาก่อน

Translate: Thank you"

## 4. Chain of Thought
Step-by-step reasoning.

Example:
"Let's think step by step.
Question: 25 * 42 = ?
Step 1: 25 * 40 = 1000
Step 2: 25 * 2 = 50
Step 3: 1000 + 50 = 1050
Answer: 1050"

## 5. ReAct Pattern
Reason and act in a loop.

Example:
"Question: What is the capital of France?
Thought: I need to search for the capital of France.
Action: Search("capital of France")
Observation: Paris is the capital of France.
Thought: I now know the answer.
Final Answer: Paris"
```

---

## 2. Prompt Templates

### Jinja2 Templates

```python
# Prompt Template with Jinja2
from jinja2 import Template

# Define template
template = Template("""
You are a helpful assistant. Your task is to {{ task }}.

Context:
{{ context }}

Question:
{{ question }}

{{ format_instructions }}
""")

# Render template
prompt = template.render(
    task="answer questions about Python",
    context="Python is a high-level programming language.",
    question="What is Python?",
    format_instructions="Answer in a single sentence."
)

print(prompt)
```

### LangChain Prompt Templates

```python
# LangChain Prompt Template
from langchain.prompts import PromptTemplate

# Define template
prompt = PromptTemplate.from_template("""
You are a helpful assistant. Your task is to {task}.

Context:
{context}

Question:
{question}

{format_instructions}
""")

# Render template
prompt = prompt.format(
    task="answer questions about Python",
    context="Python is a high-level programming language.",
    question="What is Python?",
    format_instructions="Answer in a single sentence."
)

print(prompt)
```

---

## 3. Response Formatting

### JSON Response

```python
# JSON Response Format
from openai import OpenAI
import json

client = OpenAI(api_key='YOUR_API_KEY')

# Generate JSON response
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant. Respond in JSON format."
        },
        {
            "role": "user",
            "content": "What is Python? Include: name, description, and use_cases"
        }
    ],
    temperature=0.7
)

# Parse JSON
try:
    json_response = json.loads(response.choices[0].message.content)
    print(json_response)
except json.JSONDecodeError:
    print("Failed to parse JSON")
```

### Structured Output with Pydantic

```python
# Structured Output with Pydantic
from pydantic import BaseModel, Field
from openai import OpenAI

class PythonInfo(BaseModel):
    name: str = Field(description="Name of the programming language")
    description: str = Field(description="Description of the language")
    use_cases: list[str] = Field(description="Common use cases")

# Generate structured response
client = OpenAI(api_key='YOUR_API_KEY')

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant. Respond in JSON format."
        },
        {
            "role": "user",
            "content": "What is Python? Include: name, description, and use_cases"
        }
    ],
    temperature=0.7
)

# Parse and validate
try:
    python_info = PythonInfo(**json.loads(response.choices[0].message.content))
    print(python_info.json(indent=2))
except Exception as e:
    print(f"Error: {e}")
```

---

## 4. Response Validation

### Schema Validation

```python
# Schema Validation
from pydantic import BaseModel, Field, validator

class Response(BaseModel):
    answer: str = Field(description="The answer to the question")
    confidence: float = Field(description="Confidence score (0-1)")
    sources: list[str] = Field(description="Sources used")
    
    @validator('confidence')
    def validate_confidence(cls, v):
        if not 0 <= v <= 1:
            raise ValueError('Confidence must be between 0 and 1')
        return v

# Validate response
def validate_response(response: str) -> Response:
    try:
        return Response(**json.loads(response))
    except Exception as e:
        raise ValueError(f"Invalid response: {e}")
```

### Format Validation

```python
# Format Validation
import re

def validate_json_format(text: str) -> bool:
    """Check if text is valid JSON"""
    try:
        json.loads(text)
        return True
    except json.JSONDecodeError:
        return False

def validate_email_format(email: str) -> bool:
    """Check if email is valid"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone_format(phone: str) -> bool:
    """Check if phone number is valid"""
    pattern = r'^\+?[\d\s-]{10,}$'
    return re.match(pattern, phone) is not None
```

---

## 5. Error Handling

### Retry with Exponential Backoff

```python
# Retry with Exponential Backoff
import time
from typing import Callable, TypeVar, Type
from functools import wraps

T = TypeVar('T')

def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exceptions: tuple[Type[Exception], ...] = (Exception,)
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator for retrying with exponential backoff"""
    
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    if attempt < max_retries - 1:
                        delay = min(base_delay * (2 ** attempt), max_delay)
                        time.sleep(delay)
            
            raise last_exception  # type: ignore
        
        return wrapper
    return decorator

# Usage
@retry_with_backoff(max_retries=3, base_delay=1.0)
def call_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
```

### Fallback Strategy

```python
# Fallback Strategy
from typing import Optional

class LLMClient:
    def __init__(self):
        self.primary_client = OpenAI(api_key='PRIMARY_API_KEY')
        self.fallback_client = OpenAI(api_key='FALLBACK_API_KEY')
    
    def generate(self, prompt: str) -> Optional[str]:
        # Try primary client
        try:
            response = self.primary_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Primary client failed: {e}")
        
        # Try fallback client
        try:
            response = self.fallback_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Fallback client failed: {e}")
        
        return None
```

---

## 6. Text Processing Patterns

### Text Summarization

```python
# Text Summarization
def summarize_text(text: str, max_length: int = 200) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"You are a helpful assistant. Summarize the text in at most {max_length} words."
            },
            {
                "role": "user",
                "content": text
            }
        ],
        temperature=0.7
    )
    
    return response.choices[0].message.content
```

### Text Extraction

```python
# Text Extraction
def extract_entities(text: str) -> dict:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Extract entities from the text. Return as JSON with keys: names, dates, locations, organizations"
            },
            {
                "role": "user",
                "content": text
            }
        ],
        temperature=0.3
    )
    
    return json.loads(response.choices[0].message.content)
```

### Text Classification

```python
# Text Classification
def classify_text(text: str, categories: list[str]) -> dict:
    categories_str = ", ".join(categories)
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"Classify the text into one of these categories: {categories_str}. Return as JSON with keys: category, confidence"
            },
            {
                "role": "user",
                "content": text
            }
        ],
        temperature=0.3
    )
    
    return json.loads(response.choices[0].message.content)
```

---

## 7. Thai Language Support

### Thai Prompt Engineering

```python
# Thai Prompt Engineering
def generate_thai_response(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "คุณคือผู้ช่วยที่พูดภาษาไทย ช่วยตอบคำถามของผู้ใช้ด้วยภาษาไทย"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7
    )
    
    return response.choices[0].message.content

# Example
print(generate_thai_response("สวัสดีครับ มีอะไรให้ช่วยไหมครับ?"))
```

### Thai Text Processing

```python
# Thai Text Processing
def extract_thai_entities(text: str) -> dict:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "แยกข้อมูลจากข้อความภาษาไทย คืนค่าเป็น JSON ด้วยคีย์: ชื่อ, วันที่, สถานที่, องค์กร"
            },
            {
                "role": "user",
                "content": text
            }
        ],
        temperature=0.3
    )
    
    return json.loads(response.choices[0].message.content)
```

---

## 8. Testing and Evaluation

### Prompt Testing

```python
# Prompt Testing
def test_prompt(prompt: str, test_cases: list[dict]) -> dict:
    results = {
        "total": len(test_cases),
        "passed": 0,
        "failed": 0,
        "errors": []
    }
    
    for test_case in test_cases:
        try:
            response = generate_response(prompt, test_case["input"])
            
            # Validate response
            if validate_response(response, test_case["expected"]):
                results["passed"] += 1
            else:
                results["failed"] += 1
                results["errors"].append({
                    "input": test_case["input"],
                    "expected": test_case["expected"],
                    "actual": response
                })
        except Exception as e:
            results["failed"] += 1
            results["errors"].append({
                "input": test_case["input"],
                "error": str(e)
            })
    
    return results
```

### Response Evaluation

```python
# Response Evaluation
def evaluate_response(
    response: str,
    expected: str,
    criteria: list[str]
) -> dict:
    evaluation_prompt = f"""
    Evaluate the following response based on these criteria:
    {', '.join(criteria)}
    
    Response: {response}
    Expected: {expected}
    
    Return as JSON with keys: score (0-1), feedback
    """
    
    evaluation = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": evaluation_prompt}],
        temperature=0.3
    )
    
    return json.loads(evaluation.choices[0].message.content)
```

---

## 9. Monitoring and Analytics

### Prompt Performance Tracking

```python
# Prompt Performance Tracking
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class PromptMetrics:
    prompt_id: str
    timestamp: datetime
    input_tokens: int
    output_tokens: int
    latency: float
    success: bool
    error: Optional[str] = None

class PromptTracker:
    def __init__(self):
        self.metrics: list[PromptMetrics] = []
    
    def track(self, metrics: PromptMetrics):
        self.metrics.append(metrics)
    
    def get_stats(self, prompt_id: str) -> dict:
        prompt_metrics = [m for m in self.metrics if m.prompt_id == prompt_id]
        
        if not prompt_metrics:
            return {}
        
        return {
            "total_requests": len(prompt_metrics),
            "success_rate": sum(1 for m in prompt_metrics if m.success) / len(prompt_metrics),
            "avg_latency": sum(m.latency for m in prompt_metrics) / len(prompt_metrics),
            "avg_input_tokens": sum(m.input_tokens for m in prompt_metrics) / len(prompt_metrics),
            "avg_output_tokens": sum(m.output_tokens for m in prompt_metrics) / len(prompt_metrics),
        }
```

### Cost Tracking

```python
# Cost Tracking
class CostTracker:
    PRICES = {
        "gpt-4": {"input": 0.03, "output": 0.06},
        "gpt-3.5-turbo": {"input": 0.001, "output": 0.002},
    }
    
    def __init__(self):
        self.costs: dict = {}
    
    def track_cost(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int
    ) -> float:
        if model not in self.PRICES:
            raise ValueError(f"Unknown model: {model}")
        
        input_cost = (input_tokens / 1000) * self.PRICES[model]["input"]
        output_cost = (output_tokens / 1000) * self.PRICES[model]["output"]
        total_cost = input_cost + output_cost
        
        if model not in self.costs:
            self.costs[model] = 0.0
        
        self.costs[model] += total_cost
        
        return total_cost
    
    def get_total_cost(self) -> float:
        return sum(self.costs.values())
    
    def get_cost_by_model(self) -> dict:
        return self.costs.copy()
```

---

## 10. Best Practices

### Prompt Engineering Best Practices

```markdown
# Prompt Engineering Best Practices

## 1. Be Specific and Clear
- Use precise language
- Avoid ambiguity
- Specify desired output format

## 2. Provide Context
- Give relevant background information
- Explain the task clearly
- Set expectations

## 3. Use Examples
- Provide few-shot examples
- Show desired output format
- Include edge cases

## 4. Iterate and Test
- Test prompts with various inputs
- Measure performance
- Refine based on results

## 5. Handle Edge Cases
- Consider unusual inputs
- Plan for failures
- Provide fallback options

## 6. Optimize for Cost
- Minimize token usage
- Use appropriate models
- Cache when possible

## 7. Ensure Safety
- Sanitize inputs
- Filter outputs
- Monitor for abuse

## 8. Document Prompts
- Explain prompt design
- Track versions
- Share best practices
```

---

## Quick Start

### Minimal LLM Text Protocol Setup

```python
from openai import OpenAI
from pydantic import BaseModel, Field
import json

# Initialize client
client = OpenAI(api_key='YOUR_API_KEY')

# Define response schema
class Response(BaseModel):
    answer: str = Field(description="The answer to the question")
    confidence: float = Field(description="Confidence score (0-1)")

# Generate response
def generate_response(prompt: str) -> Response:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Respond in JSON format with 'answer' and 'confidence' keys."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7
    )
    
    # Parse and validate
    return Response(**json.loads(response.choices[0].message.content))

# Usage
result = generate_response("What is Python?")
print(result.json(indent=2))
```

### Installation

```bash
pip install openai pydantic jinja2
export OPENAI_API_KEY="your-api-key"
```

### Next Steps

1. Create prompt templates for common tasks
2. Implement response validation with Pydantic
3. Add retry logic with exponential backoff
4. Set up monitoring and cost tracking
```

---

## Production Checklist

- [ ] **Error Handling**: Implement try-catch blocks for all operations
- [ ] **Rate Limiting**: Add rate limits to prevent API abuse
- [ ] **Token Budget**: Set maximum token limits per request
- [ ] **Timeout**: Configure timeouts to prevent infinite loops
- [ ] **Logging**: Set up structured logging for all interactions
- [ ] **Monitoring**: Add metrics for success rate, latency, token usage
- [ ] **Security**: Validate and sanitize all inputs
- [ ] **Cost Tracking**: Monitor API costs per request
- [ ] **Response Validation**: Validate all responses against schema
- [ ] **Fallback Strategy**: Implement fallback mechanisms for failures
- [ ] **Input Validation**: Validate all inputs before processing
- [ ] **Output Sanitization**: Filter sensitive data from outputs
- [ ] **Retry Logic**: Implement exponential backoff for retries
- [ ] **Observability**: Add tracing and correlation IDs
- [ ] **Prompt Versioning**: Track and manage prompt versions

---

## Anti-patterns

### ❌ Don't: No Response Validation

```python
# ❌ Bad - No validation
response = client.chat.completions.create(...)
json_data = json.loads(response.choices[0].message.content)  # Can fail!
```

```python
# ✅ Good - With validation
try:
    json_data = json.loads(response.choices[0].message.content)
    validated = Response(**json_data)
except (json.JSONDecodeError, ValidationError) as e:
    logger.error(f"Invalid response: {e}")
    raise
```

### ❌ Don't: No Error Handling

```python
# ❌ Bad - No error handling
response = client.chat.completions.create(...)
return response.choices[0].message.content
```

```python
# ✅ Good - With error handling
try:
    response = client.chat.completions.create(...)
    return response.choices[0].message.content
except Exception as e:
    logger.error(f"LLM error: {e}")
    raise
```

### ❌ Don't: Hardcoded Prompts

```python
# ❌ Bad - Hardcoded prompts
def generate_response(question: str):
    prompt = "Answer this question: " + question  # Hardcoded!
    return client.chat.completions.create(messages=[{"role": "user", "content": prompt}])
```

```python
# ✅ Good - Template-based prompts
from jinja2 import Template

PROMPT_TEMPLATE = Template("""
Answer this question: {{ question }}
""")

def generate_response(question: str):
    prompt = PROMPT_TEMPLATE.render(question=question)
    return client.chat.completions.create(messages=[{"role": "user", "content": prompt}])
```

---

## Integration Points

- **LLM Integration** (`06-ai-ml-production/llm-integration/`) - Setting up LLM providers
- **Prompt Engineering** (`06-ai-ml-production/prompt-engineering/`) - Advanced prompt techniques
- **Function Calling** (`06-ai-ml-production/llm-function-calling/`) - Tool and function definitions
- **Error Handling** (`03-backend-api/error-handling/`) - Production error patterns
- **Thai Language Support** (`25-internationalization/multi-language/`) - Localization

---

## Further Reading

- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [LangChain Prompts](https://python.langchain.com/docs/modules/prompts/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Prompt Engineering Best Practices](https://www.promptingguide.ai/)
- [Thai NLP Resources](https://github.com/PyThaiNLP/pythainlp)
