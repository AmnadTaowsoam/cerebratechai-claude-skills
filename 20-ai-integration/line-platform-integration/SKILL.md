---
name: LINE Platform Integration
description: Integrating AI-powered chatbots and services with the LINE platform for messaging, rich menus, and customer engagement in the Thai market.
---

# LINE Platform Integration

> **Current Level:** Expert (Enterprise Scale)
> **Domain:** AI Integration / Messaging Platforms

---

## Overview

LINE Platform integration enables AI-powered chatbots and services to leverage LINE's messaging platform, rich menus, and customer engagement features. This is particularly important for the Thai market where LINE is the dominant messaging platform with over 50 million users.

---

## 1. Executive Summary & Strategic Necessity

* **Context:** ในปี 2025-2026 LINE Platform ด้วย ReAct Pattern และ LLM Integration ช่วย Messaging Platform ที่มีอัตโนมาติการทำงานอัตโนมาติ (LINE Chatbots) ใน Enterprise Scale โดยเฉพาะในตลาดไทย

* **Business Impact:** LINE Platform ช่วยลด Downtime ของระบบ Customer Support ผ่านการตอบคำถามอัตโนมาติการสนทนา (Reduce response time), ลดต้นทุนการจัดการทีม (Increase engagement), เพิ่มอัตรากำไร Gross Margin ผ่านการทำงานอัตโนมาติ (Automated workflows), และปรับประสบทการทำงาน (Consistent experience)

* **Product Thinking:** LINE Platform ช่วยแก้ปัญหา (Pain Point) ความต้องการมีระบบสนทนาอัตโนมาติ (Users need LINE chatbots) ผ่านการทำงานอัตโนมาติ (LINE integration)

---

## 2. Technical Deep Dive (The "How-to")

* **Core Logic:** LINE Platform ใช้ ReAct Pattern และ LLM Integration ช่วย Messaging Platform ทำงานอัตโนมาติ:
  1. **Webhook Processing**: วิเคคิดความต้องการ (LINE webhook, Event processing)
  2. **Context Management**: จัดเก็บ Conversation history ด้วย Memory (Short-term, Long-term)
  3. **Response Generation**: สร้างคำตอบ ด้วย LLM (GPT-4, Claude)
  4. **LINE API Integration**: ส่งข้อความผ่าน LINE Messaging API (Text, Image, Rich menu)
  5. **State Management**: จัดการสถานะของ Conversation และ User session

* **Architecture Diagram Requirements:** แผนผังระบบ LINE Platform ต้องมีองค์ประกอบ:
  1. **LLM Integration**: Language Model สำหรับการคิดคิด (OpenAI GPT-4, Anthropic Claude)
  2. **Webhook Handler**: LINE webhook สำหรับรับข้อความ (Event processing, Signature verification)
  3. **Context Management**: Memory system สำหรับการจัดเก็บ Conversation history (Redis, Vector DB)
  4. **LINE Messaging API**: LINE API สำหรับการส่งข้อความ (Text, Image, Rich menu)
  5. **API Gateway**: REST API ด้วย Rate limiting และ Authentication
  6. **Observability**: Logging, Monitoring, Tracing สำหรับการ debug และปรับสิทท

* **Implementation Workflow:** ขั้นตอนการนำ LINE Platform ไปใช้งานจริง:
  1. **Planning Phase**: กำหนด Requirement และเลือก Model ที่เหมาะสม
  2. **LINE Developer Console**: สร้าง LINE Channel และ Webhook URL
  3. **Webhook Handler**: สร้าง Webhook handler สำหรับรับข้อความ
  4. **LLM Integration**: สร้าง LLM integration สำหรับการสร้างคำตอบ
  5. **LINE API Integration**: สร้าง LINE API integration สำหรับการส่งข้อความ
  6. **Testing Phase**: Unit test, Integration test, E2E test ด้วยจริง Scenario
  7. **Deployment**: Deploy ด้วย API Gateway, Set up Rate limiting, Configure Monitoring
  8. **Optimization**: Tune prompts, Optimize token usage, Cache embeddings
  9. **Maintenance**: Monitor performance, Update LINE API integration, Handle edge cases

---

## 3. Tooling & Tech Stack

* **Enterprise Tools:** เครื่องมือระดับอุตสาหกรรมที่เลือกใช้สำหรับ LINE Platform ใน Enterprise Scale:
  1. **OpenAI**: GPT-4, GPT-3.5-turbo, Embeddings (text-embedding-3-small, text-embedding-3-large)
  2. **Anthropic**: Claude 3 Opus, Claude 3 Sonnet, Claude 3 Haiku
  3. **LINE Messaging API**: LINE API สำหรับการส่งข้อความ (Text, Image, Rich menu)
  4. **LINE Bot SDK**: LINE SDK สำหรับ Python, Node.js, Java
  5. **LangChain**: Framework สำหรับสร้าง Conversational AI (Python, JavaScript)
  6. **Redis**: Cache สำหรับ Short-term Memory และ Rate limiting
  7. **PostgreSQL**: Database สำหรับการจัดเก็บ Conversation History และ User data
  8. **Prometheus**: Monitoring สำหรับ Metrics (Token usage, Latency, Error rate)
  9. **Grafana**: Visualization dashboard สำหรับ Observability
  10. **LINE Analytics**: LINE Analytics สำหรับการวิเคราะห์ User behavior

* **Configuration Essentials:** การตั้งค่าสำคัญสำหรับให้ระบบเสถียร LINE Platform:
  1. **Model Configuration**: เลือก Model ตาม Use case (GPT-4 สำหรับ Complex reasoning, GPT-3.5-turbo สำหรับ Speed)
  2. **Token Budget**: ตั้ง max_tokens ตาม Budget และ Context window (4,000-8,000 tokens)
  3. **Temperature Settings**: 0.0-0.3 สำหรับ Creativity, 0.7 สำหรับ Deterministic
  4. **Rate Limiting**: 10-100 requests/minute ตาม User tier และ API limits
  5. **Timeout Configuration**: 30-60 seconds สำหรับ Chatbot execution, 5-10 seconds สำหรับ Tool calls
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

* **Security Protocol:** กลไกการป้องกัน LINE Platform:
  1. **Input Validation**: Validate และ Sanitize ทุก Input ก่อน LLM หรือ Tools (Prevent prompt injection, SQL injection)
  2. **Output Sanitization**: Filter sensitive information จาก LLM output (PII, Secrets, Internal URLs)
  3. **Tool Permission Model**: RBAC (Role-Based Access Control) สำหรับ Tools - บาง Tools Admin permission, บาง Tools เปิดให้ทุก User
  4. **Audit Trail**: Log ทุก Chatbot action, Tool call, และ Decision ด้วย Timestamp, User ID, และ Result (สำหรับ Forensics และ Compliance)
  5. **Rate Limiting**: Per-user และ Per-API rate limits สำหรับป้องกัน Abuse (100-1000 requests/hour)
  6. **Secure Communication**: mTLS สำหรับ internal services, TLS 1.3 สำหรับ external APIs
  7. **Secret Rotation**: Rotate API keys ทุก 30-90 วัน (Automated key rotation)
  8. **Sandboxing**: Run Tools ใน isolated environment (Docker containers, Lambda functions)
  9. **Content Filtering**: Block malicious content, Adult content, และ Violations (Content moderation APIs)
  10. **Data Encryption**: Encrypt sensitive data ที่ rest ใน Database (AES-256 หรือ Customer-managed keys)

* **Explainability:** (สำหรับ AI) ความสามารถในการอธิบายผลลัพธ์ผ่านเทคนิค:
  1. **Chain of Thought Logging**: เก็บ Thought process ของ Chatbot สำหรับ Debugging และ Transparency
  2. **Tool Call Tracing**: Log ทุก Tool call ด้วย Input, Output, และ Execution time
  3. **Decision Reasoning**: บันทึกเหตุผลการตัดสินใจของ Chatbot (Why chose this response?)
  4. **Confidence Scoring**: ให้คะแนน (0-1) กับทุก Decision สำหรับการประเมิน
  5. **Human-in-the-Loop**: จัดการ Approval สำหรับ critical actions ด้วย Audit trail

---

## 5. Unit Economics & Performance Metrics (KPIs)

* **Cost Calculation:** สูตรการคำนวณต้นทุนต่อหน่วย LINE Platform:
  1. **LLM Cost per Request** = (Input Tokens + Output Tokens) × Price per 1K tokens
     - GPT-4: $0.03/1K input + $0.06/1K output
     - GPT-3.5-turbo: $0.001/1K input + $0.002/1K output
     - Claude 3 Opus: $0.015/1K input + $0.075/1K output
  2. **Tool Execution Cost** = API calls × Cost per call
     - Database Query: $0.001 per query (PostgreSQL RDS)
     - External API: $0.01-0.10 per call (varies by service)
  3. **LINE API Cost** = LINE API calls × Cost per call (Free tier: 1,000 messages/month)
  4. **Total Cost per Message** = LLM Cost + Tool Costs + LINE API Cost
  5. **Monthly Cost** = (Cost per Message × Messages per Month) + Infrastructure Costs
  6. **Infrastructure Costs** = Compute ($20-100/month) + Storage ($0.023/GB/month) + Monitoring ($10/month)

* **Key Performance Indicators:** ตัวชี้วัดความสำเร็จทางเทคนิค:
  1. **Success Rate**: อัตราการสำเร็จของ Chatbot (Target: >95%)
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

* **Phase Rollout:** คำแนะนำในการทยอยเริ่มใช้งาน LINE Platform เพื่อลดความเสี่ยง:
  1. **Phase 1: MVP (1-2 เดือน)**: Deploy Simple LINE Chatbot ด้วย 1-2 Tools (Text response, Simple menu) สำหรับ Internal team ก่อนเปิดให้ Public
     - **Goal**: Validate LINE Chatbot architecture และ gather feedback
     - **Success Criteria**: >80% success rate, <10s latency
     - **Risk Mitigation**: Rate limiting, Manual review ก่อน Auto-approve
  2. **Phase 2: Beta (2-3 เดือน)**: Expand ด้วย 5-10 Tools และ Memory system (Rich menu, Quick replies) สำหรับ Selected customers
     - **Goal**: Test scalability และ Tool reliability
     - **Success Criteria**: >90% success rate, <5s latency
     - **Risk Mitigation**: Canary deployment, Feature flags, Gradual rollout
  3. **Phase 3: GA (3-6 เดือน)**: Full rollout ด้วย 10-20 Tools, Advanced Memory, และ Multi-agent orchestration
     - **Goal**: Enterprise-grade reliability และ Performance
     - **Success Criteria**: >95% success rate, <3s latency, 99.9% uptime
     - **Risk Mitigation**: Load testing, Disaster recovery, Blue-green deployment

* **Pitfalls to Avoid:** ข้อควรระวังที่มักจะผิดพลาดในระดับ Enterprise Scale:
  1. **Over-engineering**: สร้าง LINE Chatbot ที่ซ้อนเกินไป (Too many tools, Complex memory) → เริ่มจาก Simple และ iterate
  2. **No Rate Limiting**: ไม่มี Rate limits ทำให้ Cost blowout และ API abuse → Implement per-user และ per-endpoint limits ด้วย Redis
  3. **Infinite Loops**: Chatbot วนลูปไม่มีทางออก (Max iterations = ∞) → Set max_iterations=10 และ timeout=60s
  4. **Ignoring Tool Errors**: Tool failures crash Chatbot → Wrap Tools ด้วย try-catch และ return fallback response
  5. **No Context Management**: ส่งทุก message เป็น Independent → Implement sliding window และ summary
  6. **Hardcoding API Keys**: Keys ใน code ที่เปิดให้ Public → Use Environment variables หรือ Secret Manager
  7. **No Observability**: ไม่มี Logging/Tracing → Add structured logging ด้วย correlation IDs
  8. **Skipping Validation**: ไม่ Validate Tool inputs/outputs → Implement schema validation และ sanitization
  9. **Poor Prompt Design**: Vague prompts ทำให้ Chatbot hallucinate → Use specific, testable prompts ด้วย examples
  10. **Single Point of Failure**: ไม่มี Redundancy หรือ Fallback → Deploy multiple instances ด้วย Load balancer

---

## Core Concepts

### 1. LINE Platform Overview

### What is LINE Platform?

```markdown
# LINE Platform Overview

## What is LINE?
LINE is a popular messaging app in Asia, especially in Thailand, Japan, and Taiwan.

## Key Features
- **Messaging**: Send and receive messages
- **Rich Menus**: Custom menu interfaces
- **Quick Replies**: Suggested responses
- **Flex Messages**: Rich, interactive messages
- **Webhooks**: Receive events from LINE
- **Analytics**: Track user engagement

## LINE Bot SDK
- **Python**: line-bot-sdk
- **Node.js**: @line/bot-sdk
- **Java**: line-bot-sdk-java
```

### LINE Bot Types

```markdown
# LINE Bot Types

## Messaging API Bots
- **Use Case**: Customer support, Information delivery
- **Features**: Text, Image, Video, Audio messages
- **Pros**: Rich features, High engagement

## LIFF (LINE Front-end Framework)
- **Use Case**: Web apps within LINE
- **Features**: Custom UI, LINE login integration
- **Pros**: Seamless user experience

## LINE Login
- **Use Case**: User authentication
- **Features**: OAuth 2.0, Social login
- **Pros**: Easy integration

## LINE Beacon
- **Use Case**: Location-based services
- **Features**: Proximity detection
- **Pros**: Physical-digital integration
```

---

## 2. LINE Webhook Setup

### Webhook Handler (Python)

```python
# LINE Webhook Handler
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage

app = Flask(__name__)

# Initialize LINE API
line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')

@app.route("/webhook", methods=['POST'])
def webhook():
    # Get request body
    body = request.get_data(as_text=True)
    signature = request.headers['X-Line-Signature']

    # Verify signature
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # Get user message
    user_message = event.message.text
    
    # Generate response
    response = generate_response(user_message)
    
    # Send reply
    line_bot_api.reply_message(
        event.reply_token,
        TextMessage(text=response)
    )

def generate_response(message: str) -> str:
    # Implement your AI logic here
    return f"You said: {message}"

if __name__ == "__main__":
    app.run(port=5000)
```

### Webhook Handler (Node.js)

```javascript
// LINE Webhook Handler (Node.js)
const express = require('express');
const line = require('@line/bot-sdk');
const { Client } = require('@line/bot-sdk');

const app = express();

// Initialize LINE API
const config = {
    channelAccessToken: process.env.CHANNEL_ACCESS_TOKEN,
    channelSecret: process.env.CHANNEL_SECRET
};

const client = new Client(config);

// Webhook endpoint
app.post('/webhook', line.middleware(config), (req, res) => {
    Promise
        .all(req.body.events.map(handleEvent))
        .then((result) => res.json(result))
        .catch((err) => {
            console.error(err);
            res.status(500).end();
        });
});

// Handle events
async function handleEvent(event) {
    if (event.type !== 'message' || event.message.type !== 'text') {
        return Promise.resolve(null);
    }

    // Generate response
    const response = generateResponse(event.message.text);

    // Send reply
    return client.replyMessage(event.replyToken, {
        type: 'text',
        text: response
    });
}

function generateResponse(message) {
    // Implement your AI logic here
    return `You said: ${message}`;
}

app.listen(3000, () => {
    console.log('LINE bot is running on port 3000');
});
```

---

## 3. LINE Message Types

### Text Messages

```python
# Send Text Message
from linebot.models import TextMessage

# Simple text message
line_bot_api.push_message(
    'USER_ID',
    TextMessage(text='Hello, World!')
)

# Multiple text messages
line_bot_api.push_message(
    'USER_ID',
    [
        TextMessage(text='Hello!'),
        TextMessage(text='How can I help you?')
    ]
)
```

### Image Messages

```python
# Send Image Message
from linebot.models import ImageMessage

# Send image from URL
line_bot_api.push_message(
    'USER_ID',
    ImageMessage(
        original_content_url='https://example.com/image.jpg',
        preview_image_url='https://example.com/image-preview.jpg'
    )
)
```

### Flex Messages

```python
# Send Flex Message
from linebot.models import FlexSendMessage

flex_message = FlexSendMessage(
    alt_text='This is a flex message',
    contents={
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": "Hello,",
                    "size": "xl",
                    "weight": "bold"
                },
                {
                    "type": "text",
                    "text": "World",
                    "size": "xl",
                    "weight": "bold",
                    "color": "#FF0000"
                }
            ]
        }
    }
)

line_bot_api.push_message('USER_ID', flex_message)
```

---

## 4. Rich Menu

### Create Rich Menu

```python
# Create Rich Menu
from linebot.models import RichMenu, RichMenuArea, RichMenuBounds, RichMenuSize, URIAction

# Define rich menu
rich_menu = RichMenu(
    size=RichMenuSize(width=2500, height=1686),
    selected=False,
    name="Main Menu",
    chatBarText="Tap to open menu",
    areas=[
        RichMenuArea(
            bounds=RichMenuBounds(x=0, y=0, width=1250, height=843),
            action=URIAction(label="Website", uri="https://example.com")
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=1250, y=0, width=1250, height=843),
            action=URIAction(label="Contact", uri="https://example.com/contact")
        )
    ]
)

# Create rich menu
rich_menu_id = line_bot_api.create_rich_menu(rich_menu)

# Upload rich menu image
with open('rich_menu.png', 'rb') as f:
    line_bot_api.set_rich_menu_image(rich_menu_id, 'image/png', f)

# Set rich menu for all users
line_bot_api.set_default_rich_menu(rich_menu_id)
```

### Set Rich Menu for User

```python
# Set Rich Menu for Specific User
line_bot_api.link_rich_menu_to_user('USER_ID', 'RICH_MENU_ID')

# Unlink rich menu from user
line_bot_api.unlink_rich_menu_from_user('USER_ID')
```

---

## 5. Quick Replies

### Quick Replies

```python
# Quick Replies
from linebot.models import QuickReply, QuickReplyButton, MessageAction, PostbackAction

quick_reply = QuickReply(
    items=[
        QuickReplyButton(
            action=MessageAction(label="Yes", text="Yes")
        ),
        QuickReplyButton(
            action=MessageAction(label="No", text="No")
        ),
        QuickReplyButton(
            action=PostbackAction(label="More info", data="info")
        )
    ]
)

line_bot_api.push_message(
    'USER_ID',
    TextMessage(text='Do you like this?', quick_reply=quick_reply)
)
```

---

## 6. Postback Events

### Handle Postback

```python
# Handle Postback Event
from linebot.models import PostbackEvent

@handler.add(PostbackEvent)
def handle_postback(event):
    # Get postback data
    data = event.postback.data
    
    # Handle based on data
    if data == 'info':
        line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text='Here is more information...')
        )
    elif data == 'subscribe':
        line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text='You have subscribed!')
        )
```

---

## 7. LLM Integration

### OpenAI Integration

```python
# OpenAI Integration with LINE
from openai import OpenAI
from linebot.models import TextMessage

# Initialize OpenAI
client = OpenAI(api_key='YOUR_OPENAI_API_KEY')

# Generate response with OpenAI
def generate_response(message: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": message
            }
        ],
        temperature=0.7,
        max_tokens=500
    )
    
    return response.choices[0].message.content

# Handle message with LLM
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # Generate response
    response = generate_response(event.message.text)
    
    # Send reply
    line_bot_api.reply_message(
        event.reply_token,
        TextMessage(text=response)
    )
```

### Conversation Memory

```python
# Conversation Memory with Redis
import redis
import json

# Initialize Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Save message to memory
def save_message(user_id: str, role: str, content: str):
    key = f"conversation:{user_id}"
    message = {
        'role': role,
        'content': content,
        'timestamp': datetime.now().isoformat()
    }
    r.lpush(key, json.dumps(message))
    r.expire(key, 86400)  # Expire after 24 hours

# Get conversation history
def get_conversation(user_id: str) -> list:
    key = f"conversation:{user_id}"
    messages = r.lrange(key, 0, 9)  # Get last 10 messages
    return [json.loads(msg) for msg in messages]

# Generate response with memory
def generate_response(user_id: str, message: str) -> str:
    # Get conversation history
    history = get_conversation(user_id)
    
    # Build messages for LLM
    messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    
    # Add history
    for msg in reversed(history):
        messages.append({
            "role": msg['role'],
            "content": msg['content']
        })
    
    # Add current message
    messages.append({"role": "user", "content": message})
    
    # Generate response
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
        max_tokens=500
    )
    
    # Save messages
    save_message(user_id, 'user', message)
    save_message(user_id, 'assistant', response.choices[0].message.content)
    
    return response.choices[0].message.content
```

---

## 8. Thai Language Support

### Thai Language Processing

```python
# Thai Language Support
from openai import OpenAI

# Initialize OpenAI
client = OpenAI(api_key='YOUR_OPENAI_API_KEY')

# Generate Thai response
def generate_thai_response(message: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "คุณคือผู้ช่วยที่พูดภาษาไทย ช่วยตอบคำถามของผู้ใช้ด้วยภาษาไทย"
            },
            {
                "role": "user",
                "content": message
            }
        ],
        temperature=0.7,
        max_tokens=500
    )
    
    return response.choices[0].message.content

# Example usage
response = generate_thai_response("สวัสดีครับ")
print(response)  # "สวัสดีครับ มีอะไรให้ช่วยไหมครับ?"
```

### Thai Quick Replies

```python
# Thai Quick Replies
quick_reply = QuickReply(
    items=[
        QuickReplyButton(
            action=MessageAction(label="ใช่", text="ใช่")
        ),
        QuickReplyButton(
            action=MessageAction(label="ไม่", text="ไม่")
        ),
        QuickReplyButton(
            action=MessageAction(label="ขอข้อมูลเพิ่มเติม", text="ขอข้อมูลเพิ่มเติม")
        )
    ]
)

line_bot_api.push_message(
    'USER_ID',
    TextMessage(text='คุณชอบสินค้านี้หรือไม่?', quick_reply=quick_reply)
)
```

---

## 9. Analytics and Monitoring

### LINE Analytics

```python
# Track LINE Bot Analytics
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Track message
def track_message(user_id: str, message_type: str, content: str):
    logger.info({
        'timestamp': datetime.now().isoformat(),
        'user_id': user_id,
        'type': message_type,
        'content': content
    })

# Track response
def track_response(user_id: str, response: str, latency: float):
    logger.info({
        'timestamp': datetime.now().isoformat(),
        'user_id': user_id,
        'response': response,
        'latency': latency
    })

# Track error
def track_error(user_id: str, error: str):
    logger.error({
        'timestamp': datetime.now().isoformat(),
        'user_id': user_id,
        'error': error
    })
```

### Metrics Dashboard

```python
# Metrics with Prometheus
from prometheus_client import Counter, Histogram, start_http_server

# Define metrics
message_counter = Counter('line_messages_total', 'Total LINE messages', ['type'])
response_latency = Histogram('line_response_latency_seconds', 'Response latency')
error_counter = Counter('line_errors_total', 'Total errors', ['error_type'])

# Track message
def track_message(message_type: str):
    message_counter.labels(type=message_type).inc()

# Track latency
def track_latency(latency: float):
    response_latency.observe(latency)

# Track error
def track_error(error_type: str):
    error_counter.labels(error_type=error_type).inc()

# Start metrics server
start_http_server(8000)
```

---

## 10. Testing

### Unit Testing

```python
# Unit Testing LINE Bot
import pytest
from linebot.models import MessageEvent, TextMessage

def test_generate_response():
    response = generate_response("Hello")
    assert len(response) > 0
    assert "Hello" in response or "hello" in response.lower()

def test_thai_response():
    response = generate_thai_response("สวัสดี")
    assert len(response) > 0

def test_conversation_memory():
    user_id = "test_user"
    save_message(user_id, "user", "Hello")
    save_message(user_id, "assistant", "Hi there!")
    
    history = get_conversation(user_id)
    assert len(history) == 2
    assert history[0]['role'] == "assistant"
    assert history[1]['role'] == "user"
```

---

## Quick Start

### Minimal LINE Bot Setup

```python
# Minimal LINE Bot
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from openai import OpenAI

app = Flask(__name__)

# Initialize LINE API
line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')

# Initialize OpenAI
client = OpenAI(api_key='YOUR_OPENAI_API_KEY')

@app.route("/webhook", methods=['POST'])
def webhook():
    body = request.get_data(as_text=True)
    signature = request.headers['X-Line-Signature']
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # Generate response with OpenAI
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": event.message.text}
        ]
    )
    
    # Send reply
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response.choices[0].message.content)
    )

if __name__ == "__main__":
    app.run(port=5000)
```

### Installation

```bash
pip install flask line-bot-sdk openai
export CHANNEL_ACCESS_TOKEN="your-channel-access-token"
export CHANNEL_SECRET="your-channel-secret"
export OPENAI_API_KEY="your-openai-api-key"
```

### Next Steps

1. Set up LINE Developer Console and webhook URL
2. Add conversation memory for multi-turn conversations
3. Implement rich menus and quick replies
4. Set up analytics and monitoring
```

---

## Production Checklist

- [ ] **Error Handling**: Implement try-catch blocks for all operations
- [ ] **Rate Limiting**: Add rate limits to prevent API abuse
- [ ] **Token Budget**: Set maximum token limits per conversation
- [ ] **Timeout**: Configure timeouts to prevent infinite loops
- [ ] **Logging**: Set up structured logging for all interactions
- [ ] **Monitoring**: Add metrics for success rate, latency, token usage
- [ ] **Security**: Validate and sanitize all inputs
- [ ] **Cost Tracking**: Monitor API costs per conversation
- [ ] **Memory Management**: Implement context window for conversation history
- [ ] **Fallback Strategy**: Implement fallback mechanisms for failures
- [ ] **Signature Verification**: Verify LINE webhook signatures
- [ ] **Input Validation**: Validate all inputs before processing
- [ ] **Output Sanitization**: Filter sensitive data from outputs
- [ ] **Retry Logic**: Implement exponential backoff for retries
- [ ] **Observability**: Add tracing and correlation IDs

---

## Anti-patterns

### ❌ Don't: No Signature Verification

```python
# ❌ Bad - No signature verification
@app.route("/webhook", methods=['POST'])
def webhook():
    body = request.get_data(as_text=True)
    # Process webhook without verifying signature!
    return 'OK'
```

```python
# ✅ Good - Verify signature
@app.route("/webhook", methods=['POST'])
def webhook():
    body = request.get_data(as_text=True)
    signature = request.headers['X-Line-Signature']
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    return 'OK'
```

### ❌ Don't: No Error Handling

```python
# ❌ Bad - No error handling
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    response = generate_response(event.message.text)
    line_bot_api.reply_message(event.reply_token, TextMessage(text=response))
```

```python
# ✅ Good - With error handling
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        response = generate_response(event.message.text)
        line_bot_api.reply_message(event.reply_token, TextMessage(text=response))
    except Exception as e:
        logger.error(f"Error handling message: {e}")
        line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text="Sorry, something went wrong. Please try again.")
        )
```

### ❌ Don't: No Rate Limiting

```python
# ❌ Bad - No rate limiting
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # Process message without rate limiting!
    response = generate_response(event.message.text)
    line_bot_api.reply_message(event.reply_token, TextMessage(text=response))
```

```python
# ✅ Good - Implement rate limiting
from redis import Redis
from datetime import timedelta

redis = Redis()

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    key = f"rate_limit:{user_id}"
    
    # Check rate limit
    if redis.exists(key):
        line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text="Please wait before sending another message.")
        )
        return
    
    # Set rate limit
    redis.setex(key, timedelta(seconds=10), "1")
    
    # Process message
    response = generate_response(event.message.text)
    line_bot_api.reply_message(event.reply_token, TextMessage(text=response))
```

---

## Integration Points

- **LLM Integration** (`06-ai-ml-production/llm-integration/`) - Setting up LLM providers
- **Chatbot Integration** (`20-ai-integration/chatbot-integration/`) - Backend chatbot logic
- **Conversational UI** (`20-ai-integration/conversational-ui/`) - UI patterns
- **Error Handling** (`03-backend-api/error-handling/`) - Production error patterns
- **Thai Language Support** (`25-internationalization/multi-language/`) - Localization

---

## Further Reading

- [LINE Messaging API Documentation](https://developers.line.biz/en/docs/messaging-api/)
- [LINE Bot SDK Python](https://github.com/line/line-bot-sdk-python)
- [LINE Bot SDK Node.js](https://github.com/line/line-bot-sdk-nodejs)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [Thai NLP Resources](https://github.com/PyThaiNLP/pythainlp)
