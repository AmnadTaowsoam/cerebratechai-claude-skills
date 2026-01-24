---
name: Prompt Engineering
description: Comprehensive guide for LLM prompt engineering techniques and best practices
---

# Prompt Engineering

## Overview
Comprehensive guide for LLM prompt engineering techniques and best practices.

## Prerequisites

- Basic understanding of Large Language Models (LLMs)
- Familiarity with AI/ML concepts
- Experience with using AI assistants or chatbots
- Understanding of natural language communication
- Knowledge of programming concepts (for code generation tasks)

## Key Concepts

- **Zero-Shot Prompting**: Asking the model to perform a task without providing examples
- **Few-Shot Prompting**: Providing examples to guide the model's understanding and output
- **Chain-of-Thought (CoT)**: Guiding the model to show its reasoning process step by step
- **ReAct (Reasoning + Acting)**: Combining reasoning with action-oriented prompts for problem solving
- **Self-Consistency**: Generating multiple reasoning paths and finding consensus
- **Prompt Templates**: Reusable prompt patterns with variable substitution
- **System Messages**: Setting behavior and personality of the AI assistant
- **Context Management**: Handling long conversations and documents within token limits
- **Output Formatting**: Guiding the model to produce structured, parseable output
- **Constraints and Controls**: Setting clear boundaries on what the model should and shouldn't do
- **Temperature**: Controls randomness in model output (low = deterministic, high = creative)
- **Top P (Nucleus Sampling)**: Controls cumulative probability threshold for output diversity
- **Max Tokens**: Controls maximum length of output
- **Stop Sequences**: Define strings that stop generation for structured output
- **Prompt Versioning**: Managing different versions of prompts for testing and deployment
- **Anti-Patterns**: Common prompt engineering mistakes to avoid
- **Model-Specific Tips**: Optimization strategies for different LLM providers (GPT, Claude, Llama, Mistral)

---

## 1. Prompt Design Principles

### 1.1 Core Principles

```python
"""
Prompt Engineering Core Principles:

1. CLARITY - Be specific and unambiguous
2. CONTEXT - Provide relevant background information
3. CONSTRAINTS - Set clear boundaries and expectations
4. EXAMPLES - Show, don't just tell
5. FORMAT - Specify desired output structure
6. ITERATION - Refine and test prompts
"""

# Example of a well-structured prompt
WELL_STRUCTURED_PROMPT = """
You are a senior software engineer with expertise in Python and web development.

TASK:
Write a REST API endpoint for user registration.

REQUIREMENTS:
- Use FastAPI framework
- Include input validation
- Hash passwords using bcrypt
- Return proper HTTP status codes
- Handle duplicate email errors

CONTEXT:
This is part of a larger application with existing user models.
The User model has fields: id, email, password_hash, created_at.

OUTPUT FORMAT:
Return the complete Python code with imports and type hints.
"""

# Example of a poorly structured prompt
POORLY_STRUCTURED_PROMPT = """
Write a user registration API.
"""
```

### 1.2 Prompt Structure Template

```python
class PromptTemplate:
    """Template for structuring prompts."""

    @staticmethod
    def create_prompt(
        role: str,
        task: str,
        context: str = None,
        requirements: list = None,
        examples: list = None,
        output_format: str = None,
        constraints: list = None
    ) -> str:
        """Create a well-structured prompt."""
        parts = []

        # Role
        parts.append(f"You are {role}.")

        # Context
        if context:
            parts.append(f"\nCONTEXT:\n{context}")

        # Task
        parts.append(f"\nTASK:\n{task}")

        # Requirements
        if requirements:
            parts.append("\nREQUIREMENTS:")
            for req in requirements:
                parts.append(f"- {req}")

        # Examples
        if examples:
            parts.append("\nEXAMPLES:")
            for i, example in enumerate(examples, 1):
                parts.append(f"\nExample {i}:")
                parts.append(example)

        # Output format
        if output_format:
            parts.append(f"\nOUTPUT FORMAT:\n{output_format}")

        # Constraints
        if constraints:
            parts.append("\nCONSTRAINTS:")
            for constraint in constraints:
                parts.append(f"- {constraint}")

        return "\n".join(parts)

# Usage
prompt = PromptTemplate.create_prompt(
    role="a data scientist with expertise in machine learning",
    task="Create a data preprocessing pipeline for tabular data",
    context="The dataset contains customer information with missing values and outliers.",
    requirements=[
        "Handle missing values appropriately",
        "Detect and handle outliers",
        "Normalize numerical features",
        "Encode categorical variables"
    ],
    output_format="Return Python code using pandas and scikit-learn",
    constraints=[
        "Do not use external libraries beyond pandas and scikit-learn",
        "Include type hints",
        "Add docstrings to functions"
    ]
)

print(prompt)
```

---

## 2. Prompting Techniques

### 2.1 Zero-Shot Prompting

```python
"""
Zero-Shot: Ask the model to perform a task without examples.
Useful when the task is straightforward and the model has prior knowledge.
"""

# Simple zero-shot prompt
ZERO_SHOT_PROMPT = """
Classify the following email as spam or not spam:

Email: "Congratulations! You've won a free iPhone. Click here to claim your prize."

Classification:
"""

# Zero-shot with reasoning
ZERO_SHOT_REASONING = """
Analyze the sentiment of the following customer review:

Review: "The product arrived quickly and works perfectly. I'm very satisfied with my purchase."

Provide your reasoning and then the final sentiment label (positive, negative, neutral).
"""

# Zero-shot code generation
ZERO_SHOT_CODE = """
Write a Python function that checks if a number is prime.

Function signature: def is_prime(n: int) -> bool:
"""

# Zero-shot with role
ZERO_SHOT_ROLE = """
As a legal assistant, summarize the following contract clause in plain English:

Clause: "The Parties agree that any dispute arising out of or relating to this Agreement shall be resolved through binding arbitration in accordance with the rules of the American Arbitration Association."

Summary:
"""
```

### 2.2 Few-Shot Prompting

```python
"""
Few-Shot: Provide examples to guide the model's understanding.
Useful for complex tasks or when the model needs specific patterns.
"""

# Few-shot for classification
FEW_SHOT_CLASSIFICATION = """
Classify the following text as positive, negative, or neutral.

Example 1:
Text: "I love this product! It works great."
Classification: positive

Example 2:
Text: "The product arrived damaged and doesn't work."
Classification: negative

Example 3:
Text: "The product is okay, nothing special."
Classification: neutral

Now classify:
Text: "This exceeded all my expectations! Highly recommend."
Classification:
"""

# Few-shot for code generation
FEW_SHOT_CODE = """
Write a function to convert temperature between Celsius and Fahrenheit.

Example 1:
Input: Convert 25°C to Fahrenheit
Output: 77°F

Example 2:
Input: Convert 68°F to Celsius
Output: 20°C

Now convert:
Input: Convert 100°C to Fahrenheit
Output:
"""

# Few-shot with chain of thought
FEW_SHOT_COT = """
Solve the following math problems step by step.

Problem 1: If a shirt costs $20 and is on sale for 25% off, what is the sale price?
Solution:
Step 1: Calculate discount amount: $20 × 0.25 = $5
Step 2: Subtract discount from original: $20 - $5 = $15
Answer: $15

Problem 2: A store buys items at $50 each and sells them at a 40% markup. What is the selling price?
Solution:
Step 1: Calculate markup amount: $50 × 0.40 = $20
Step 2: Add markup to cost: $50 + $20 = $70
Answer: $70

Now solve:
Problem 3: A laptop costs $800 with a 15% discount and then an additional 5% tax. What is the final price?
Solution:
"""

# Few-shot for translation
FEW_SHOT_TRANSLATION = """
Translate the following English sentences to French.

Example 1:
English: "Hello, how are you?"
French: "Bonjour, comment allez-vous?"

Example 2:
English: "I would like a coffee, please."
French: "Je voudrais un café, s'il vous plaît."

Now translate:
English: "Where is the train station?"
French:
"""
```

### 2.3 Chain-of-Thought (CoT)

```python
"""
Chain-of-Thought: Guide the model to show its reasoning process.
Useful for complex reasoning tasks and debugging.
"""

# Basic CoT
CHAIN_OF_THOUGHT = """
Solve this problem step by step:

A farmer has chickens and cows. There are 30 animals total with 74 legs.
How many chickens and how many cows does the farmer have?

Let's think through this:
"""

# CoT with explicit steps
COT_EXPLICIT = """
Analyze whether the following business idea is viable. Provide your reasoning step by step.

Business Idea: A subscription service for renting luxury handbags.

Step 1: Identify the target market and demand
Step 2: Analyze the competitive landscape
Step 3: Evaluate the business model economics
Step 4: Identify potential risks and challenges
Step 5: Provide a final recommendation

Analysis:
"""

# CoT for debugging
COT_DEBUGGING = """
Debug the following code. Explain your thought process for each step.

Code:
```python
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)
```

The function fails with an empty list. Let's debug:
"""

# CoT for decision making
COT_DECISION = """
Should we migrate our application from a monolithic architecture to microservices?

Consider:
1. Team size and expertise
2. Application complexity
3. Deployment requirements
4. Scalability needs
5. Maintenance overhead

Provide a step-by-step analysis and recommendation:
"""
```

### 2.4 ReAct (Reasoning + Acting)

```python
"""
ReAct: Combine reasoning with action-oriented prompts.
Useful for tasks that require both analysis and execution.
"""

# ReAct for problem solving
REACT_PROMPT = """
You are a helpful assistant that can solve problems by thinking and acting.

Problem: A user reports that their web application is slow when loading large datasets.

Thought 1: What could be causing the slow performance?
Action 1: Identify potential causes (database queries, network, client-side rendering)

Thought 2: How would I diagnose this?
Action 2: List diagnostic steps (profiling, monitoring, load testing)

Thought 3: What solutions should I recommend?
Action 3: Propose solutions based on diagnosis

Provide your complete analysis:
"""

# ReAct for code review
REACT_CODE_REVIEW = """
Review the following code for potential issues.

Code:
```python
def process_user_data(user_id):
    user = db.query("SELECT * FROM users WHERE id = ?", user_id)
    orders = db.query("SELECT * FROM orders WHERE user_id = ?", user_id)
    return {"user": user, "orders": orders}
```

Thought: What security concerns exist?
Action: Identify SQL injection vulnerabilities

Thought: What performance issues exist?
Action: Identify N+1 query problems

Thought: What improvements can be made?
Action: Suggest refactoring and best practices

Provide your review:
"""

# ReAct for troubleshooting
REACT_TROUBLESHOOTING = """
A user cannot log into their account. Help troubleshoot this issue.

Thought 1: What are the possible causes?
Action 1: List potential causes (wrong password, account locked, server issues)

Thought 2: What information do I need?
Action 2: Ask clarifying questions

Thought 3: How do I resolve each cause?
Action 3: Provide step-by-step solutions

Provide your troubleshooting guide:
"""
```

### 2.5 Self-Consistency

```python
"""
Self-Consistency: Generate multiple reasoning paths and find consensus.
Useful for tasks where accuracy is critical and multiple approaches exist.
"""

# Self-consistency for math
SELF_CONSISTENCY_MATH = """
Solve this problem using three different methods and verify they give the same answer.

Problem: What is 15% of 240?

Method 1: Direct calculation
Method 2: Proportion method
Method 3: Decimal method

Show all three methods and verify the answer:
"""

# Self-consistency for reasoning
SELF_CONSISTENCY_REASONING = """
Analyze this scenario from multiple perspectives and reach a consensus.

Scenario: A company is considering remote work for all employees.

Perspective 1: Employee benefits and satisfaction
Perspective 2: Company culture and collaboration
Perspective 3: Business costs and productivity
Perspective 4: Client relationships and communication

Provide analysis from each perspective and a balanced conclusion:
"""

# Self-consistency for code review
SELF_CONSISTENCY_CODE = """
Review this code from three different angles: security, performance, and maintainability.

Code:
```python
def authenticate(username, password):
    user = db.find_one("users", {"username": username})
    if user and user["password"] == password:
        return {"success": True, "token": generate_token(user)}
    return {"success": False}
```

Security review:
Performance review:
Maintainability review:

Consolidated recommendations:
"""
```

---

## 3. Prompt Templates

### 3.1 Template System

```python
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class PromptTemplate:
    """Reusable prompt template with variables."""

    name: str
    template: str
    variables: List[str]

    def format(self, **kwargs) -> str:
        """Format template with provided variables."""
        missing_vars = set(self.variables) - set(kwargs.keys())
        if missing_vars:
            raise ValueError(f"Missing variables: {missing_vars}")
        return self.template.format(**kwargs)

# Define templates
PROMPT_TEMPLATES = {
    "code_review": PromptTemplate(
        name="code_review",
        template="""You are an expert code reviewer.

Review the following {language} code:

```{language}
{code}
```

Focus on:
- Code quality and style
- Potential bugs
- Performance issues
- Security vulnerabilities
- Best practices

Provide specific, actionable feedback:
""",
        variables=["language", "code"]
    ),

    "summarization": PromptTemplate(
        name="summarization",
        template="""Summarize the following text in {max_sentences} sentences.

Text:
{text}

Summary:
""",
        variables=["text", "max_sentences"]
    ),

    "translation": PromptTemplate(
        name="translation",
        template="""Translate the following text from {source_lang} to {target_lang}.

Text:
{text}

Translation:
""",
        variables=["source_lang", "target_lang", "text"]
    ),

    "extraction": PromptTemplate(
        name="extraction",
        template="""Extract the following information from the text:
{fields}

Text:
{text}

Extracted information (JSON format):
""",
        variables=["fields", "text"]
    )
}

# Usage
code_review_prompt = PROMPT_TEMPLATES["code_review"].format(
    language="Python",
    code="def add(a, b): return a + b"
)

summarization_prompt = PROMPT_TEMPLATES["summarization"].format(
    text="A long text here...",
    max_sentences=3
)

print(code_review_prompt)
```

### 3.2 Dynamic Prompt Building

```python
class PromptBuilder:
    """Build prompts dynamically based on context."""

    def __init__(self):
        self.sections = []

    def add_role(self, role: str):
        """Add role definition."""
        self.sections.append(f"You are {role}.")
        return self

    def add_context(self, context: str):
        """Add context information."""
        self.sections.append(f"\nCONTEXT:\n{context}")
        return self

    def add_task(self, task: str):
        """Add task description."""
        self.sections.append(f"\nTASK:\n{task}")
        return self

    def add_requirements(self, requirements: List[str]):
        """Add requirements as bullet points."""
        self.sections.append("\nREQUIREMENTS:")
        for req in requirements:
            self.sections.append(f"- {req}")
        return self

    def add_examples(self, examples: List[str]):
        """Add examples."""
        self.sections.append("\nEXAMPLES:")
        for i, example in enumerate(examples, 1):
            self.sections.append(f"\nExample {i}:\n{example}")
        return self

    def add_constraints(self, constraints: List[str]):
        """Add constraints."""
        self.sections.append("\nCONSTRAINTS:")
        for constraint in constraints:
            self.sections.append(f"- {constraint}")
        return self

    def add_output_format(self, format_spec: str):
        """Add output format specification."""
        self.sections.append(f"\nOUTPUT FORMAT:\n{format_spec}")
        return self

    def build(self) -> str:
        """Build the final prompt."""
        return "\n".join(self.sections)

# Usage
prompt = (PromptBuilder()
    .add_role("a senior Python developer")
    .add_context("We're building a REST API for a task management application.")
    .add_task("Create an endpoint to update a task by ID.")
    .add_requirements([
        "Use FastAPI",
        "Include input validation",
        "Handle non-existent tasks gracefully",
        "Return updated task in response"
    ])
    .add_constraints([
        "Do not modify other fields",
        "Maintain audit trail"
    ])
    .add_output_format("Return complete Python code with imports")
    .build())

print(prompt)
```

---

## 4. System Messages

### 4.1 System Message Patterns

```python
"""
System Messages: Set the behavior and personality of the AI assistant.
These are sent at the start of the conversation and persist throughout.
"""

# Professional assistant
SYSTEM_PROFESSIONAL = """
You are a professional, helpful assistant. Provide accurate, well-structured responses.
Be concise but thorough. Use proper formatting with markdown.
If you're uncertain about something, acknowledge it rather than guessing.
"""

# Technical expert
SYSTEM_TECHNICAL = """
You are a senior software engineer with 15+ years of experience.
Provide technical solutions with best practices, security considerations, and performance optimization.
Include code examples when relevant. Explain trade-offs between different approaches.
"""

# Creative writer
SYSTEM_CREATIVE = """
You are a creative writer with expertise in storytelling, world-building, and character development.
Use vivid descriptions, engaging dialogue, and compelling narratives.
Adapt your style to match the requested genre and tone.
"""

# Teacher
SYSTEM_TEACHER = """
You are a patient, encouraging teacher. Explain concepts clearly with examples.
Break down complex topics into manageable parts. Check for understanding.
Adapt your explanations to the learner's level.
"""

# Code reviewer
SYSTEM_CODE_REVIEWER = """
You are a meticulous code reviewer. Focus on:
- Code quality and readability
- Potential bugs and edge cases
- Performance and scalability
- Security vulnerabilities
- Adherence to best practices
Provide constructive, specific feedback with suggestions for improvement.
"""

# Data analyst
SYSTEM_ANALYST = """
You are a data analyst with expertise in statistical analysis and data visualization.
Interpret data accurately, identify patterns, and provide actionable insights.
Use appropriate statistical methods and explain your reasoning clearly.
"""

# Customer service
SYSTEM_CUSTOMER_SERVICE = """
You are a helpful customer service representative. Be empathetic, patient, and solution-oriented.
Address customer concerns professionally. Escalate issues when necessary.
Maintain a positive, professional tone at all times.
"""
```

### 4.2 System Message + User Prompt

```python
class ConversationManager:
    """Manage conversations with system messages."""

    def __init__(self, system_message: str):
        self.system_message = system_message
        self.conversation = [{"role": "system", "content": system_message}]

    def add_user_message(self, message: str):
        """Add user message to conversation."""
        self.conversation.append({"role": "user", "content": message})

    def add_assistant_message(self, message: str):
        """Add assistant message to conversation."""
        self.conversation.append({"role": "assistant", "content": message})

    def get_conversation(self) -> List[Dict]:
        """Get full conversation history."""
        return self.conversation

    def reset(self):
        """Reset conversation, keeping system message."""
        self.conversation = [{"role": "system", "content": self.system_message}]

# Usage
conversation = ConversationManager(SYSTEM_TECHNICAL)

conversation.add_user_message("How do I implement a REST API in Python?")
conversation.add_assistant_message("I'll help you implement a REST API...")

conversation.add_user_message("What about authentication?")

# Get full conversation for API call
full_conversation = conversation.get_conversation()
```

---

## 5. Context Management

### 5.1 Context Window Strategies

```python
"""
Context Window Management: Handle long conversations and documents.
Different models have different context limits (4K, 8K, 32K, 128K tokens).
"""

class ContextManager:
    """Manage context within token limits."""

    def __init__(self, max_tokens: int = 4000):
        self.max_tokens = max_tokens
        self.conversation = []

    def add_message(self, role: str, content: str):
        """Add message to conversation."""
        self.conversation.append({"role": role, "content": content})
        self._trim_if_needed()

    def _trim_if_needed(self):
        """Trim conversation if it exceeds token limit."""
        # Estimate tokens (rough approximation: 1 token ≈ 4 characters)
        total_chars = sum(len(msg["content"]) for msg in self.conversation)
        estimated_tokens = total_chars // 4

        while estimated_tokens > self.max_tokens and len(self.conversation) > 2:
            # Remove oldest non-system message
            self.conversation.pop(1)  # Keep system message at index 0
            total_chars = sum(len(msg["content"]) for msg in self.conversation)
            estimated_tokens = total_chars // 4

    def get_context(self) -> List[Dict]:
        """Get current context."""
        return self.conversation

# Usage
context = ContextManager(max_tokens=4000)

context.add_message("system", "You are a helpful assistant.")
context.add_message("user", "Hello!")
context.add_message("assistant", "Hi! How can I help?")

# Add many messages - will automatically trim
for i in range(100):
    context.add_message("user", f"Message {i}")
    context.add_message("assistant", f"Response {i}")

print(f"Context length: {len(context.get_context())} messages")
```

### 5.2 Document Chunking for Context

```python
from typing import List

class DocumentChunker:
    """Chunk documents for context window."""

    def __init__(self, chunk_size: int = 1000, overlap: int = 100):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_by_size(self, text: str) -> List[str]:
        """Chunk text by size."""
        chunks = []
        start = 0

        while start < len(text):
            end = start + self.chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start = end - self.overlap

        return chunks

    def chunk_by_sentences(self, text: str, sentences_per_chunk: int = 5) -> List[str]:
        """Chunk text by sentences."""
        import re
        sentences = re.split(r'(?<=[.!?])\s+', text)

        chunks = []
        for i in range(0, len(sentences), sentences_per_chunk):
            chunk = ' '.join(sentences[i:i + sentences_per_chunk])
            chunks.append(chunk)

        return chunks

    def chunk_by_paragraphs(self, text: str, paragraphs_per_chunk: int = 3) -> List[str]:
        """Chunk text by paragraphs."""
        paragraphs = text.split('\n\n')

        chunks = []
        for i in range(0, len(paragraphs), paragraphs_per_chunk):
            chunk = '\n\n'.join(paragraphs[i:i + paragraphs_per_chunk])
            chunks.append(chunk)

        return chunks

# Usage
document = """
This is a long document with multiple paragraphs.
Each paragraph contains important information.
We need to process this document in chunks.

The second paragraph continues the discussion.
It provides more details about the topic.
Chunking helps manage context windows.

Finally, the third paragraph concludes the document.
It summarizes the key points made earlier.
This approach works well for long texts.
"""

chunker = DocumentChunker(chunk_size=200, overlap=20)
chunks = chunker.chunk_by_size(document)

print(f"Created {len(chunks)} chunks")
```

---

## 6. Output Formatting

### 6.1 Structured Output

```python
"""
Output Formatting: Guide the model to produce structured, parseable output.
"""

# JSON output
JSON_OUTPUT = """
Extract the following information from the text and return as JSON:
- Name
- Email
- Phone
- Company

Text:
"John Smith works at Acme Corp. You can reach him at john.smith@acme.com or call 555-123-4567."

JSON output:
"""

# Markdown output
MARKDOWN_OUTPUT = """
Create a markdown report with the following sections:
## Executive Summary
## Key Findings
## Recommendations
## Next Steps

Topic: "Remote Work Productivity Study"

Report:
"""

# Table output
TABLE_OUTPUT = """
Create a comparison table of the following programming languages:
- Python
- JavaScript
- Java
- Go

Include columns: Use Cases, Performance, Learning Curve, Ecosystem

Format as markdown table:
"""

# Code block output
CODE_OUTPUT = """
Write a Python function to validate email addresses.
Include proper regex pattern and error handling.

Return the code in a markdown code block with syntax highlighting:
"""

# List output
LIST_OUTPUT = """
List the top 10 best practices for API security.
Format as a numbered list with brief explanations for each:
"""
```

### 6.2 Output Validation

```python
import json
import re

class OutputValidator:
    """Validate and parse model outputs."""

    @staticmethod
    def extract_json(output: str) -> dict:
        """Extract and parse JSON from output."""
        # Try to find JSON in code blocks
        json_match = re.search(r'```json\s*(.*?)\s*```', output, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1))

        # Try to find JSON without code blocks
        try:
            return json.loads(output.strip())
        except json.JSONDecodeError:
            raise ValueError("No valid JSON found in output")

    @staticmethod
    def extract_code(output: str, language: str = None) -> str:
        """Extract code from markdown code blocks."""
        if language:
            pattern = rf'```{language}\s*(.*?)\s*```'
        else:
            pattern = r'```\s*(.*?)\s*```'

        match = re.search(pattern, output, re.DOTALL)
        if match:
            return match.group(1).strip()

        raise ValueError("No code block found in output")

    @staticmethod
    def extract_table(output: str) -> list:
        """Extract table data from markdown table."""
        lines = output.strip().split('\n')
        table = []

        for line in lines:
            if '|' in line and not line.strip().startswith('|---'):
                cells = [cell.strip() for cell in line.split('|')[1:-1]]
                if cells:
                    table.append(cells)

        return table

    @staticmethod
    def validate_format(output: str, expected_format: str) -> bool:
        """Validate if output matches expected format."""
        if expected_format == "json":
            try:
                json.loads(output)
                return True
            except json.JSONDecodeError:
                return False

        elif expected_format == "code":
            return "```" in output

        elif expected_format == "list":
            return bool(re.match(r'^\s*\d+\.', output))

        return False

# Usage
output = """
```json
{
  "name": "John Smith",
  "email": "john@example.com",
  "phone": "555-123-4567"
}
```
"""

validator = OutputValidator()
data = validator.extract_json(output)
print(data)
```

---

## 7. Constraints and Controls

### 7.1 Setting Boundaries

```python
"""
Constraints: Set clear boundaries on what the model should and shouldn't do.
"""

# Length constraints
LENGTH_CONSTRAINTS = """
Write a summary of the article in exactly 3 sentences.
Each sentence should be no more than 20 words.

Article:
[Long article text]

Summary:
"""

# Content constraints
CONTENT_CONSTRAINTS = """
Explain quantum computing to a 12-year-old.
Constraints:
- Do not use technical jargon
- Use simple analogies
- Keep it under 200 words
- Focus on the concept, not the math

Explanation:
"""

# Format constraints
FORMAT_CONSTRAINTS = """
Create a product description with these constraints:
- Must include exactly 3 bullet points
- Each bullet point must start with a verb
- Total length must be under 100 words
- No exclamation marks

Product: Wireless Bluetooth Headphones

Description:
"""

# Negative constraints (what NOT to do)
NEGATIVE_CONSTRAINTS = """
Critique this code constructively.
Constraints:
- Do not use harsh language
- Do not point out style preferences
- Do not suggest complete rewrites
- Focus only on functional issues

Code:
```python
def process(data):
    result = []
    for item in data:
        if item:
            result.append(item * 2)
    return result
```

Critique:
"""

# Safety constraints
SAFETY_CONSTRAINTS = """
Provide information about cybersecurity best practices.
Constraints:
- Do not provide instructions for malicious activities
- Do not suggest exploiting vulnerabilities
- Focus only on defensive measures
- If asked about attacks, explain how to prevent them

Topic: SQL Injection Prevention

Response:
"""
```

### 7.2 Output Controls

```python
# Temperature control (randomness)
"""
Temperature: Controls randomness in model output.
- Low (0.0-0.3): More deterministic, focused
- Medium (0.4-0.7): Balanced creativity and coherence
- High (0.8-1.0): More creative, diverse
"""

# Top P (nucleus sampling)
"""
Top P: Controls the cumulative probability threshold.
- Lower (0.1-0.5): More focused, conservative
- Higher (0.6-0.9): More diverse, creative
"""

# Max tokens
"""
Max Tokens: Controls the maximum length of output.
- Set based on expected response length
- Prevents overly long responses
"""

# Stop sequences
"""
Stop Sequences: Define strings that stop generation.
- Useful for structured output
- Prevents the model from continuing unnecessarily
"""

# Example with controls
OUTPUT_CONTROLS = """
Write a creative story about a robot learning to paint.
Controls:
- Temperature: 0.8 (more creative)
- Max tokens: 500
- Stop sequence: "THE END"

Story:
"""
```

---

## 8. Testing Prompts

### 8.1 Prompt Testing Framework

```python
from typing import List, Dict, Callable
from dataclasses import dataclass

@dataclass
class PromptTest:
    """Test case for prompt evaluation."""
    name: str
    prompt: str
    expected_output_type: str
    validation_fn: Callable[[str], bool]
    test_inputs: List[Dict]

class PromptTester:
    """Test prompts systematically."""

    def __init__(self):
        self.tests = []

    def add_test(self, test: PromptTest):
        """Add a test case."""
        self.tests.append(test)

    def run_test(self, test: PromptTest, model_fn: Callable) -> Dict:
        """Run a single test."""
        results = {
            "name": test.name,
            "passed": 0,
            "failed": 0,
            "errors": []
        }

        for input_data in test.test_inputs:
            try:
                # Format prompt with input data
                prompt = test.prompt.format(**input_data)

                # Get model output
                output = model_fn(prompt)

                # Validate output
                if test.validation_fn(output):
                    results["passed"] += 1
                else:
                    results["failed"] += 1
                    results["errors"].append({
                        "input": input_data,
                        "output": output,
                        "reason": "Validation failed"
                    })

            except Exception as e:
                results["failed"] += 1
                results["errors"].append({
                    "input": input_data,
                    "error": str(e)
                })

        return results

    def run_all_tests(self, model_fn: Callable) -> List[Dict]:
        """Run all tests."""
        return [self.run_test(test, model_fn) for test in self.tests]

# Usage
def validate_json_output(output: str) -> bool:
    """Validate output is valid JSON."""
    try:
        json.loads(output)
        return True
    except json.JSONDecodeError:
        return False

def validate_list_output(output: str) -> bool:
    """Validate output is a numbered list."""
    return bool(re.match(r'^\s*\d+\.', output.strip()))

# Create tests
tester = PromptTester()

# Test 1: JSON extraction
test1 = PromptTest(
    name="JSON Extraction",
    prompt="Extract name and email from: {text}\nJSON:",
    expected_output_type="json",
    validation_fn=validate_json_output,
    test_inputs=[
        {"text": "Contact: John Doe at john@example.com"},
        {"text": "Email jane@test.com from Jane Smith"}
    ]
)

# Test 2: List generation
test2 = PromptTest(
    name="List Generation",
    prompt="List 3 benefits of {topic}:",
    expected_output_type="list",
    validation_fn=validate_list_output,
    test_inputs=[
        {"topic": "exercise"},
        {"topic": "meditation"}
    ]
)

tester.add_test(test1)
tester.add_test(test2)

# Run tests (mock model function)
def mock_model(prompt: str) -> str:
    return '{"name": "John Doe", "email": "john@example.com"}'

results = tester.run_all_tests(mock_model)
for result in results:
    print(f"{result['name']}: {result['passed']} passed, {result['failed']} failed")
```

### 8.2 A/B Testing Prompts

```python
class PromptABTest:
    """A/B test different prompt variations."""

    def __init__(self, prompt_a: str, prompt_b: str):
        self.prompt_a = prompt_a
        self.prompt_b = prompt_b
        self.results_a = []
        self.results_b = []

    def test_prompt(
        self,
        prompt: str,
        test_cases: List[Dict],
        model_fn: Callable,
        evaluator: Callable
    ) -> List[float]:
        """Test a prompt against multiple cases."""
        scores = []

        for test_case in test_cases:
            formatted_prompt = prompt.format(**test_case)
            output = model_fn(formatted_prompt)
            score = evaluator(output, test_case.get("expected", {}))
            scores.append(score)

        return scores

    def run_ab_test(
        self,
        test_cases: List[Dict],
        model_fn: Callable,
        evaluator: Callable
    ) -> Dict:
        """Run A/B test."""
        scores_a = self.test_prompt(self.prompt_a, test_cases, model_fn, evaluator)
        scores_b = self.test_prompt(self.prompt_b, test_cases, model_fn, evaluator)

        return {
            "prompt_a": {
                "average_score": sum(scores_a) / len(scores_a),
                "all_scores": scores_a
            },
            "prompt_b": {
                "average_score": sum(scores_b) / len(scores_b),
                "all_scores": scores_b
            },
            "winner": "A" if sum(scores_a) > sum(scores_b) else "B"
        }

# Usage
prompt_a = "Summarize this in 1 sentence: {text}"
prompt_b = "Provide a one-sentence summary: {text}"

test_cases = [
    {"text": "The cat sat on the mat and looked around."},
    {"text": "Python is a popular programming language for data science."}
]

def mock_model(prompt: str) -> str:
    return "A simple summary."

def evaluate_summary(output: str, expected: Dict) -> float:
    """Evaluate summary quality (0-1)."""
    # In practice, use more sophisticated evaluation
    return 0.8

ab_test = PromptABTest(prompt_a, prompt_b)
results = ab_test.run_ab_test(test_cases, mock_model, evaluate_summary)

print(f"Winner: {results['winner']}")
```

---

## 9. Prompt Versioning

### 9.1 Version Control

```python
from typing import Dict, List
from datetime import datetime

class PromptVersionManager:
    """Manage prompt versions."""

    def __init__(self):
        self.versions = {}

    def save_version(
        self,
        prompt_id: str,
        version: str,
        prompt: str,
        description: str = None,
        tags: List[str] = None
    ):
        """Save a prompt version."""
        if prompt_id not in self.versions:
            self.versions[prompt_id] = {}

        self.versions[prompt_id][version] = {
            "prompt": prompt,
            "description": description,
            "tags": tags or [],
            "created_at": datetime.now().isoformat()
        }

    def get_version(self, prompt_id: str, version: str) -> Dict:
        """Get a specific prompt version."""
        return self.versions.get(prompt_id, {}).get(version)

    def get_latest(self, prompt_id: str) -> Dict:
        """Get the latest version of a prompt."""
        versions = self.versions.get(prompt_id, {})
        if not versions:
            return None

        latest_version = max(versions.keys())
        return versions[latest_version]

    def list_versions(self, prompt_id: str) -> List[str]:
        """List all versions of a prompt."""
        return list(self.versions.get(prompt_id, {}).keys())

    def compare_versions(
        self,
        prompt_id: str,
        version_a: str,
        version_b: str
    ) -> Dict:
        """Compare two prompt versions."""
        return {
            "version_a": self.get_version(prompt_id, version_a),
            "version_b": self.get_version(prompt_id, version_b)
        }

# Usage
manager = PromptVersionManager()

manager.save_version(
    "code_review",
    "1.0",
    "Review this code: {code}",
    description="Initial version",
    tags=["v1", "initial"]
)

manager.save_version(
    "code_review",
    "1.1",
    "Review this {language} code for security and performance: {code}",
    description="Added language and focus areas",
    tags=["v1", "improved"]
)

manager.save_version(
    "code_review",
    "2.0",
    """Review the following code:
Language: {language}
Focus: {focus_areas}

```{language}
{code}
```

Provide specific, actionable feedback.""",
    description="Complete redesign with structured format",
    tags=["v2", "structured"]
)

# Get latest version
latest = manager.get_latest("code_review")
print(f"Latest version: {latest['description']}")
```

### 9.2 Prompt Rollback

```python
class PromptRollbackManager:
    """Manage prompt rollbacks."""

    def __init__(self, version_manager: PromptVersionManager):
        self.version_manager = version_manager
        self.deployment_history = {}

    def deploy(self, prompt_id: str, version: str, environment: str = "production"):
        """Deploy a prompt version."""
        if prompt_id not in self.deployment_history:
            self.deployment_history[prompt_id] = {}

        self.deployment_history[prompt_id][environment] = {
            "version": version,
            "deployed_at": datetime.now().isoformat()
        }

    def rollback(self, prompt_id: str, environment: str = "production") -> str:
        """Rollback to previous version."""
        history = self.deployment_history.get(prompt_id, {})
        if environment not in history:
            raise ValueError(f"No deployment found for {environment}")

        current_version = history[environment]["version"]
        version_list = self.version_manager.list_versions(prompt_id)

        # Find previous version
        current_idx = version_list.index(current_version)
        if current_idx == 0:
            raise ValueError("No previous version to rollback to")

        previous_version = version_list[current_idx - 1]

        # Deploy previous version
        self.deploy(prompt_id, previous_version, environment)

        return previous_version

    def get_deployed_version(self, prompt_id: str, environment: str = "production") -> str:
        """Get currently deployed version."""
        history = self.deployment_history.get(prompt_id, {})
        return history.get(environment, {}).get("version")

# Usage
rollback_manager = PromptRollbackManager(manager)

# Deploy version 2.0
rollback_manager.deploy("code_review", "2.0", "production")

# Rollback to 1.1
previous = rollback_manager.rollback("code_review", "production")
print(f"Rolled back to: {previous}")
```

---

## 10. Anti-Patterns

### 10.1 Common Mistakes

```python
"""
ANTI-PATTERNS: Common prompt engineering mistakes to avoid.
"""

# 1. Too vague
BAD_VAGUE = """
Write code for a website.
"""

GOOD_SPECIFIC = """
Write a Python Flask application with the following endpoints:
- GET /api/users - List all users
- POST /api/users - Create a new user
- GET /api/users/<id> - Get user by ID
Use SQLAlchemy for database operations.
"""

# 2. Too much context
BAD_TOO_MUCH = """
[1000 lines of irrelevant text]

Based on the above, what is the capital of France?
"""

GOOD_CONCISE = """
What is the capital of France?
"""

# 3. Conflicting instructions
BAD_CONFLICTING = """
Write a short response.
Provide a detailed explanation.
Keep it under 50 words.
Include all relevant details.
"""

GOOD_CLEAR = """
Provide a concise explanation in under 50 words.
"""

# 4. Missing examples
BAD_NO_EXAMPLES = """
Convert the following dates to ISO format.
Date: January 15, 2024
"""

GOOD_WITH_EXAMPLES = """
Convert dates to ISO format (YYYY-MM-DD).

Example: January 1, 2024 → 2024-01-01
Example: March 15, 2024 → 2024-03-15

Convert: January 15, 2024
"""

# 5. Assuming knowledge
BAD_ASSUME = """
Fix the bug in this code.
```python
# [incomplete code snippet]
```
"""

GOOD_COMPLETE = """
This function is supposed to sort a list in descending order but doesn't work.
```python
def sort_descending(items):
    return sorted(items)
```

What's wrong and how do we fix it?
"""

# 6. No output format
BAD_NO_FORMAT = """
Summarize this article.
[Article text]
"""

GOOD_WITH_FORMAT = """
Summarize the article in 3 bullet points.
Each point should be under 20 words.

[Article text]

Summary:
"""

# 7. Over-constraining
BAD_OVER_CONSTRAINT = """
Write a story about a cat.
Constraints:
- Must be exactly 100 words
- Must use each letter of the alphabet
- Must include 5 different colors
- Must rhyme
- Must be in iambic pentameter
"""

GOOD_REASONABLE = """
Write a short story (100-150 words) about a cat's adventure.
Include at least 2 colors and make it engaging.
"""

# 8. No role context
BAD_NO_ROLE = """
How do I secure my API?
"""

GOOD_WITH_ROLE = """
As a security expert, explain how to secure a REST API.
Focus on authentication, authorization, and common vulnerabilities.
"""

# 9. Ambiguous terms
BAD_AMBIGUOUS = """
Make it better.
"""

GOOD_PRECISE = """
Improve the code's performance by reducing time complexity.
"""

# 10. Chain of vague prompts
BAD_CHAIN = """
Write code.
Make it faster.
Add error handling.
Make it secure.
"""

GOOD_SINGLE = """
Write a Python function that:
- Processes a list of user IDs
- Fetches user data from an API
- Handles network errors gracefully
- Uses caching for performance
- Validates input data
"""
```

---

## 11. Model-Specific Tips

### 11.1 GPT Models

```python
"""
GPT-SPECIFIC TIPS: Optimizing for OpenAI GPT models.
"""

# GPT-4 optimizations
GPT4_TIPS = """
GPT-4 Best Practices:

1. Use system messages effectively
   - Set clear role and behavior
   - Specify output format in system message

2. Leverage GPT-4's reasoning
   - Use chain-of-thought for complex tasks
   - Ask for step-by-step explanations

3. Structure complex prompts
   - Use clear section headers
   - Number requirements
   - Provide examples

4. GPT-4 handles long context well
   - Can use longer prompts (up to 8K tokens)
   - Good for document analysis

5. Use function calling for structured output
   - Define clear function schemas
   - Let GPT-4 choose appropriate functions
"""

# GPT-3.5 optimizations
GPT35_TIPS = """
GPT-3.5 Best Practices:

1. Keep prompts concise
   - GPT-3.5 has 4K token limit
   - Be more direct and specific

2. Use more examples
   - GPT-3.5 benefits from few-shot
   - Provide clear patterns

3. Simpler instructions
   - Avoid complex reasoning requests
   - Break down complex tasks

4. Temperature matters more
   - Lower temperature (0.3-0.5) for consistency
   - Higher temperature (0.7-0.9) for creativity

5. Use structured output
   - Specify JSON format explicitly
   - Use code blocks for code
"""

# Example optimized for GPT-4
GPT4_OPTIMIZED = """
You are a senior software architect.

TASK: Design a microservices architecture for an e-commerce platform.

REQUIREMENTS:
1. Service decomposition
2. Inter-service communication
3. Data storage strategy
4. Authentication and authorization
5. Scalability considerations

OUTPUT FORMAT:
Provide a structured response with:
- Architecture diagram (ASCII art)
- Service list with responsibilities
- Technology recommendations
- Potential challenges and mitigations

Think through this step by step:
"""

# Example optimized for GPT-3.5
GPT35_OPTIMIZED = """
Design microservices for e-commerce.

Services needed:
- Product catalog
- Order management
- Payment processing
- User accounts

List each service with:
1. Main responsibility
2. Required APIs
3. Database choice

Example format:
Product Catalog:
- Responsibility: Manage products
- APIs: GET /products, POST /products
- Database: PostgreSQL

Your design:
"""
```

### 11.2 Claude Models

```python
"""
CLAUDE-SPECIFIC TIPS: Optimizing for Anthropic Claude models.
"""

# Claude optimizations
CLAUDE_TIPS = """
Claude Best Practices:

1. Use XML-style tags
   - Claude responds well to <tags>
   - Use for structure and emphasis

2. Be conversational
   - Claude is more conversational than GPT
   - Can use natural language instructions

3. Leverage Claude's long context
   - Claude supports 100K+ tokens
   - Great for document analysis

4. Use Claude's strengths
   - Good at analysis and reasoning
   - Strong at following complex instructions

5. Claude 3 capabilities
   - Haiku: Fast, cost-effective
   - Sonnet: Balanced performance
   - Opus: Highest capability
"""

# Claude-optimized prompt
CLAUDE_OPTIMIZED = """
<task>
Analyze this document and extract key information.
</task>

<context>
This is a legal contract between two parties.
Focus on obligations, deadlines, and penalties.
</context>

<document>
[Document text]
</document>

<output_format>
Provide analysis in this structure:
- Parties Involved
- Key Obligations
- Important Deadlines
- Potential Risks
- Recommendations
</output_format>

<instructions>
Be thorough but concise.
Use bullet points for clarity.
Highlight any concerning clauses.
</instructions>
"""
```

### 11.3 Other Models

```python
"""
OTHER MODELS: Tips for various LLM providers.
"""

# Llama models
LLAMA_TIPS = """
Llama Best Practices:

1. Llama is instruction-tuned
   - Use "### Instruction:" format
   - Clear "### Response:" separator

2. Good for local deployment
   - Can run on consumer hardware
   - Lower cost than API models

3. Shorter context window
   - Typically 4K-8K tokens
   - Manage context carefully

4. Less capable than GPT-4
   - Simpler tasks work better
   - More examples help
"""

# Mistral models
MISTRAL_TIPS = """
Mistral Best Practices:

1. Strong performance for size
   - 7B model competitive with larger models
   - Good balance of speed and quality

2. Good at code
   - Strong coding capabilities
   - Useful for development tasks

3. Efficient inference
   - Fast generation
   - Lower latency
"""

# Example for Llama
LLAMA_FORMAT = """
### Instruction:
Write a Python function to calculate the Fibonacci sequence.

### Response:
"""

# Example for Mistral
MISTRAL_FORMAT = """
[INST]
Write a Python function to calculate the Fibonacci sequence.
Include type hints and docstring.
[/INST]
"""
```

---

## 12. Production Patterns

### 12.1 Prompt Management System

```python
from typing import Dict, List, Optional
from enum import Enum

class PromptEnvironment(Enum):
    """Prompt environments."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

class PromptManager:
    """Production prompt management system."""

    def __init__(self):
        self.prompts = {}
        self.deployments = {}

    def register_prompt(
        self,
        prompt_id: str,
        version: str,
        prompt: str,
        environment: PromptEnvironment = PromptEnvironment.DEVELOPMENT,
        metadata: Dict = None
    ):
        """Register a new prompt version."""
        if prompt_id not in self.prompts:
            self.prompts[prompt_id] = {}

        self.prompts[prompt_id][version] = {
            "prompt": prompt,
            "environment": environment.value,
            "metadata": metadata or {},
            "created_at": datetime.now().isoformat()
        }

    def deploy(
        self,
        prompt_id: str,
        version: str,
        environment: PromptEnvironment = PromptEnvironment.PRODUCTION
    ):
        """Deploy a prompt version to an environment."""
        if prompt_id not in self.prompts:
            raise ValueError(f"Prompt {prompt_id} not found")

        if version not in self.prompts[prompt_id]:
            raise ValueError(f"Version {version} not found for {prompt_id}")

        env_key = f"{prompt_id}:{environment.value}"
        self.deployments[env_key] = {
            "version": version,
            "deployed_at": datetime.now().isoformat()
        }

    def get_prompt(
        self,
        prompt_id: str,
        environment: PromptEnvironment = PromptEnvironment.PRODUCTION
    ) -> str:
        """Get the currently deployed prompt."""
        env_key = f"{prompt_id}:{environment.value}"

        if env_key not in self.deployments:
            raise ValueError(f"No prompt deployed for {env_key}")

        version = self.deployments[env_key]["version"]
        return self.prompts[prompt_id][version]["prompt"]

    def get_prompt_with_fallback(
        self,
        prompt_id: str,
        environments: List[PromptEnvironment] = None
    ) -> Optional[str]:
        """Get prompt with environment fallback."""
        environments = environments or [
            PromptEnvironment.PRODUCTION,
            PromptEnvironment.STAGING,
            PromptEnvironment.DEVELOPMENT
        ]

        for env in environments:
            try:
                return self.get_prompt(prompt_id, env)
            except ValueError:
                continue

        return None

    def list_prompts(self) -> List[Dict]:
        """List all registered prompts."""
        result = []

        for prompt_id, versions in self.prompts.items():
            for version, data in versions.items():
                result.append({
                    "prompt_id": prompt_id,
                    "version": version,
                    "environment": data["environment"],
                    "metadata": data["metadata"]
                })

        return result

# Usage
manager = PromptManager()

# Register prompts
manager.register_prompt(
    "code_review",
    "1.0",
    "Review this code: {code}",
    PromptEnvironment.DEVELOPMENT
)

manager.register_prompt(
    "code_review",
    "1.1",
    "Review this {language} code: {code}",
    PromptEnvironment.STAGING
)

manager.register_prompt(
    "code_review",
    "2.0",
    "Review the following code for security: {code}",
    PromptEnvironment.PRODUCTION
)

# Deploy to production
manager.deploy("code_review", "2.0", PromptEnvironment.PRODUCTION)

# Get production prompt
prompt = manager.get_prompt("code_review", PromptEnvironment.PRODUCTION)
print(prompt)
```

### 12.2 Prompt Monitoring

```python
from typing import Dict, List
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class PromptMetrics:
    """Metrics for prompt performance."""
    prompt_id: str
    version: str
    total_calls: int
    total_tokens: int
    avg_latency_ms: float
    error_rate: float
    satisfaction_score: float

class PromptMonitor:
    """Monitor prompt performance in production."""

    def __init__(self):
        self.metrics = {}
        self.call_history = []

    def record_call(
        self,
        prompt_id: str,
        version: str,
        tokens: int,
        latency_ms: float,
        success: bool,
        satisfaction: float = None
    ):
        """Record a prompt call."""
        key = f"{prompt_id}:{version}"

        if key not in self.metrics:
            self.metrics[key] = {
                "prompt_id": prompt_id,
                "version": version,
                "total_calls": 0,
                "total_tokens": 0,
                "total_latency": 0,
                "errors": 0,
                "satisfaction_scores": []
            }

        metrics = self.metrics[key]
        metrics["total_calls"] += 1
        metrics["total_tokens"] += tokens
        metrics["total_latency"] += latency_ms

        if not success:
            metrics["errors"] += 1

        if satisfaction is not None:
            metrics["satisfaction_scores"].append(satisfaction)

        self.call_history.append({
            "prompt_id": prompt_id,
            "version": version,
            "tokens": tokens,
            "latency_ms": latency_ms,
            "success": success,
            "timestamp": datetime.now().isoformat()
        })

    def get_metrics(
        self,
        prompt_id: str,
        version: str = None,
        time_window: timedelta = None
    ) -> PromptMetrics:
        """Get metrics for a prompt."""
        if version:
            key = f"{prompt_id}:{version}"
            if key not in self.metrics:
                return None
            metrics_data = [self.metrics[key]]
        else:
            # Aggregate all versions
            metrics_data = [
                self.metrics[k] for k in self.metrics
                if k.startswith(f"{prompt_id}:")
            ]

        if not metrics_data:
            return None

        # Aggregate metrics
        total_calls = sum(m["total_calls"] for m in metrics_data)
        total_tokens = sum(m["total_tokens"] for m in metrics_data)
        total_latency = sum(m["total_latency"] for m in metrics_data)
        total_errors = sum(m["errors"] for m in metrics_data)
        all_scores = []
        for m in metrics_data:
            all_scores.extend(m["satisfaction_scores"])

        return PromptMetrics(
            prompt_id=prompt_id,
            version=version or "all",
            total_calls=total_calls,
            total_tokens=total_tokens,
            avg_latency_ms=total_latency / total_calls if total_calls else 0,
            error_rate=total_errors / total_calls if total_calls else 0,
            satisfaction_score=sum(all_scores) / len(all_scores) if all_scores else 0
        )

    def get_anomalies(self, threshold: float = 2.0) -> List[Dict]:
        """Detect anomalies in prompt performance."""
        anomalies = []

        for key, metrics in self.metrics.items():
            if metrics["total_calls"] < 10:
                continue

            avg_latency = metrics["total_latency"] / metrics["total_calls"]
            error_rate = metrics["errors"] / metrics["total_calls"]

            # Check for high latency
            if avg_latency > 5000:  # 5 seconds
                anomalies.append({
                    "type": "high_latency",
                    "prompt_id": metrics["prompt_id"],
                    "version": metrics["version"],
                    "value": avg_latency
                })

            # Check for high error rate
            if error_rate > 0.1:  # 10%
                anomalies.append({
                    "type": "high_error_rate",
                    "prompt_id": metrics["prompt_id"],
                    "version": metrics["version"],
                    "value": error_rate
                })

        return anomalies

# Usage
monitor = PromptMonitor()

# Record some calls
monitor.record_call("code_review", "1.0", 100, 500, True, 0.8)
monitor.record_call("code_review", "1.0", 150, 600, True, 0.9)
monitor.record_call("code_review", "1.0", 120, 400, False, 0.5)

# Get metrics
metrics = monitor.get_metrics("code_review", "1.0")
print(f"Average latency: {metrics.avg_latency_ms:.2f}ms")
print(f"Error rate: {metrics.error_rate:.2%}")
print(f"Satisfaction: {metrics.satisfaction_score:.2f}")

# Check for anomalies
anomalies = monitor.get_anomalies()
for anomaly in anomalies:
    print(f"Anomaly: {anomaly}")
```

---

## Related Skills

- [`06-ai-ml-production/llm-integration`](06-ai-ml-production/llm-integration/SKILL.md)
- [`06-ai-ml-production/llm-function-calling`](06-ai-ml-production/llm-function-calling/SKILL.md)
- [`06-ai-ml-production/llm-guardrails`](06-ai-ml-production/llm-guardrails/SKILL.md)
- [`06-ai-ml-production/agent-patterns`](06-ai-ml-production/agent-patterns/SKILL.md)
- [`06-ai-ml-production/embedding-models`](06-ai-ml-production/embedding-models/SKILL.md)

## Additional Resources

- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Anthropic Prompt Library](https://docs.anthropic.com/claude/prompt-library)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [Learn Prompting](https://learnprompting.org/)
