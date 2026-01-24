---
name: LLM Integration
description: Comprehensive guide for LLM API integration covering OpenAI, Anthropic, Azure, and Cohere providers
---

# LLM Integration

## Overview
Comprehensive guide for LLM API integration covering OpenAI, Anthropic, Azure, and Cohere providers.

## Prerequisites

- Basic understanding of REST APIs and HTTP requests
- Python programming knowledge
- Familiarity with async/await patterns
- API key management concepts
- Understanding of rate limiting and retry patterns

## Key Concepts

- **LLM Providers**: OpenAI, Anthropic, Azure OpenAI, Cohere - different API services for accessing large language models
- **Unified Interface**: Abstraction layer that provides consistent API across different LLM providers
- **Streaming Responses**: Real-time token-by-token response delivery for better user experience
- **Error Handling**: Retry logic, exponential backoff, and fallback strategies for resilient API calls
- **Rate Limiting**: Token bucket algorithm to manage API request rates and avoid hitting limits
- **Cost Tracking**: Monitoring token usage and calculating API costs across providers
- **Response Caching**: Storing and retrieving cached responses to reduce API calls and costs
- **Prompt Templates**: Reusable prompt patterns with variable substitution
- **Token Counting**: Estimating and managing token usage for different models
- **Context Window Management**: Managing conversation history within model context limits
- **Multi-Provider Fallback**: Automatic switching between providers on failure
- **Batch Processing**: Efficient processing of multiple LLM requests concurrently

---

## 1. Provider Setup

### 1.1 OpenAI Setup

```python
import os
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    organization=os.getenv('OPENAI_ORG_ID'),  # Optional
    base_url=os.getenv('OPENAI_BASE_URL'),  # For custom endpoints
    timeout=60.0,
    max_retries=3
)

# Test connection
try:
    models = client.models.list()
    print(f"Connected! Available models: {len(models.data)}")
except Exception as e:
    print(f"Connection failed: {e}")
```

### 1.2 Anthropic Setup

```python
import anthropic

# Initialize Anthropic client
client = anthropic.Anthropic(
    api_key=os.getenv('ANTHROPIC_API_KEY'),
    base_url=os.getenv('ANTHROPIC_BASE_URL'),  # Optional
    timeout=60.0,
    max_retries=3
)

# Test connection
try:
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=10,
        messages=[{"role": "user", "content": "Hi"}]
    )
    print(f"Connected! Response: {message.content}")
except Exception as e:
    print(f"Connection failed: {e}")
```

### 1.3 Azure OpenAI Setup

```python
from openai import AzureOpenAI

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version=os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-15-preview'),
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
    timeout=60.0,
    max_retries=3
)

# Test connection
try:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hi"}],
        max_tokens=10
    )
    print(f"Connected! Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"Connection failed: {e}")
```

### 1.4 Cohere Setup

```python
import cohere

# Initialize Cohere client
client = cohere.Client(
    api_key=os.getenv('COHERE_API_KEY'),
    base_url=os.getenv('COHERE_BASE_URL'),  # Optional
    timeout=60.0,
    max_retries=3
)

# Test connection
try:
    response = client.chat(
        model='command',
        message='Hi',
        max_tokens=10
    )
    print(f"Connected! Response: {response.text}")
except Exception as e:
    print(f"Connection failed: {e}")
```

---

## 2. Unified Interface Pattern

```python
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union, AsyncIterator
from enum import Enum
import asyncio

class LLMProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    AZURE_OPENAI = "azure_openai"
    COHERE = "cohere"

class LLMResponse:
    """Unified LLM response."""
    def __init__(
        self,
        content: str,
        model: str,
        provider: LLMProvider,
        tokens_used: int = 0,
        finish_reason: str = None,
        metadata: Dict = None
    ):
        self.content = content
        self.model = model
        self.provider = provider
        self.tokens_used = tokens_used
        self.finish_reason = finish_reason
        self.metadata = metadata or {}

class BaseLLMClient(ABC):
    """Base LLM client interface."""

    @abstractmethod
    def chat(
        self,
        messages: List[Dict],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> LLMResponse:
        """Chat completion."""
        pass

    @abstractmethod
    async def achat(
        self,
        messages: List[Dict],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> LLMResponse:
        """Async chat completion."""
        pass

    @abstractmethod
    def stream_chat(
        self,
        messages: List[Dict],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> AsyncIterator[str]:
        """Stream chat completion."""
        pass

class OpenAIClient(BaseLLMClient):
    """OpenAI client implementation."""

    def __init__(self, api_key: str, **kwargs):
        self.client = OpenAI(api_key=api_key, **kwargs)
        self.provider = LLMProvider.OPENAI

    def chat(
        self,
        messages: List[Dict],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> LLMResponse:
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )

        return LLMResponse(
            content=response.choices[0].message.content,
            model=response.model,
            provider=self.provider,
            tokens_used=response.usage.total_tokens,
            finish_reason=response.choices[0].finish_reason
        )

    async def achat(
        self,
        messages: List[Dict],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> LLMResponse:
        response = await self.client.chat.completions.acreate(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )

        return LLMResponse(
            content=response.choices[0].message.content,
            model=response.model,
            provider=self.provider,
            tokens_used=response.usage.total_tokens,
            finish_reason=response.choices[0].finish_reason
        )

    async def stream_chat(
        self,
        messages: List[Dict],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> AsyncIterator[str]:
        stream = await self.client.chat.completions.acreate(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
            **kwargs
        )

        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

class AnthropicClient(BaseLLMClient):
    """Anthropic client implementation."""

    def __init__(self, api_key: str, **kwargs):
        self.client = anthropic.Anthropic(api_key=api_key, **kwargs)
        self.provider = LLMProvider.ANTHROPIC

    def chat(
        self,
        messages: List[Dict],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> LLMResponse:
        response = self.client.messages.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )

        content = response.content[0].text if response.content else ""

        return LLMResponse(
            content=content,
            model=response.model,
            provider=self.provider,
            tokens_used=response.usage.input_tokens + response.usage.output_tokens,
            finish_reason=response.stop_reason
        )

    async def achat(
        self,
        messages: List[Dict],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> LLMResponse:
        response = await self.client.messages.acreate(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )

        content = response.content[0].text if response.content else ""

        return LLMResponse(
            content=content,
            model=response.model,
            provider=self.provider,
            tokens_used=response.usage.input_tokens + response.usage.output_tokens,
            finish_reason=response.stop_reason
        )

    async def stream_chat(
        self,
        messages: List[Dict],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> AsyncIterator[str]:
        with self.client.messages.stream(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        ) as stream:
            for text in stream.text_stream:
                yield text

class UnifiedLLMClient:
    """Unified LLM client with provider fallback."""

    def __init__(self, providers: Dict[LLMProvider, BaseLLMClient]):
        self.providers = providers
        self.default_provider = list(providers.keys())[0]

    def chat(
        self,
        messages: List[Dict],
        model: str,
        provider: Optional[LLMProvider] = None,
        **kwargs
    ) -> LLMResponse:
        """Chat with specified or default provider."""
        provider = provider or self.default_provider
        client = self.providers[provider]
        return client.chat(messages, model, **kwargs)

    async def achat(
        self,
        messages: List[Dict],
        model: str,
        provider: Optional[LLMProvider] = None,
        **kwargs
    ) -> LLMResponse:
        """Async chat with specified or default provider."""
        provider = provider or self.default_provider
        client = self.providers[provider]
        return await client.achat(messages, model, **kwargs)

    async def stream_chat(
        self,
        messages: List[Dict],
        model: str,
        provider: Optional[LLMProvider] = None,
        **kwargs
    ) -> AsyncIterator[str]:
        """Stream chat with specified or default provider."""
        provider = provider or self.default_provider
        client = self.providers[provider]
        async for chunk in client.stream_chat(messages, model, **kwargs):
            yield chunk

# Usage
providers = {
    LLMProvider.OPENAI: OpenAIClient(api_key=os.getenv('OPENAI_API_KEY')),
    LLMProvider.ANTHROPIC: AnthropicClient(api_key=os.getenv('ANTHROPIC_API_KEY')),
}

unified_client = UnifiedLLMClient(providers)

response = unified_client.chat(
    messages=[{"role": "user", "content": "Hello!"}],
    model="gpt-4",
    provider=LLMProvider.OPENAI
)

print(response.content)
```

---

## 3. Streaming Responses

```python
import asyncio
from typing import AsyncIterator

class StreamingLLMClient:
    """Handle streaming LLM responses."""

    async def stream_with_callback(
        self,
        messages: List[Dict],
        model: str,
        callback: callable,
        provider: LLMProvider = None,
        **kwargs
    ):
        """Stream response with callback for each chunk."""
        full_response = ""

        async for chunk in self.client.stream_chat(
            messages, model, provider=provider, **kwargs
        ):
            full_response += chunk
            callback(chunk)

        return full_response

    async def stream_to_file(
        self,
        messages: List[Dict],
        model: str,
        output_path: str,
        provider: LLMProvider = None,
        **kwargs
    ):
        """Stream response to file."""
        with open(output_path, 'w', encoding='utf-8') as f:
            async for chunk in self.client.stream_chat(
                messages, model, provider=provider, **kwargs
            ):
                f.write(chunk)
                f.flush()

    async def stream_with_display(
        self,
        messages: List[Dict],
        model: str,
        provider: LLMProvider = None,
        **kwargs
    ):
        """Stream response with live display."""
        import sys

        full_response = ""
        sys.stdout.write("Response: ")
        sys.stdout.flush()

        async for chunk in self.client.stream_chat(
            messages, model, provider=provider, **kwargs
        ):
            full_response += chunk
            sys.stdout.write(chunk)
            sys.stdout.flush()

        sys.stdout.write("\n")
        return full_response

# Usage
streaming_client = StreamingLLMClient()
streaming_client.client = unified_client

# Stream with callback
async def on_chunk(chunk):
    print(f"Received: {chunk}")

await streaming_client.stream_with_callback(
    messages=[{"role": "user", "content": "Tell me a story"}],
    model="gpt-4",
    callback=on_chunk
)

# Stream to file
await streaming_client.stream_to_file(
    messages=[{"role": "user", "content": "Write a poem"}],
    model="gpt-4",
    output_path="response.txt"
)
```

---

## 4. Error Handling and Retries

```python
import time
import logging
from functools import wraps
from typing import Callable, Type
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMError(Exception):
    """Base LLM error."""
    pass

class RateLimitError(LLMError):
    """Rate limit exceeded."""
    pass

class TimeoutError(LLMError):
    """Request timeout."""
    pass

class AuthenticationError(LLMError):
    """Authentication failed."""
    pass

class RetryConfig:
    """Retry configuration."""

    def __init__(
        self,
        max_attempts: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0
    ):
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base

def with_retry(
    retry_config: RetryConfig = None,
    exceptions: tuple = (Exception,)
):
    """Decorator for retry logic."""

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            config = retry_config or RetryConfig()

            for attempt in range(config.max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == config.max_attempts - 1:
                        logger.error(f"Max retries reached for {func.__name__}: {e}")
                        raise

                    delay = min(
                        config.base_delay * (config.exponential_base ** attempt),
                        config.max_delay
                    )

                    logger.warning(
                        f"Attempt {attempt + 1} failed for {func.__name__}: {e}. "
                        f"Retrying in {delay:.2f}s"
                    )

                    time.sleep(delay)

        return wrapper
    return decorator

# Using tenacity for advanced retry logic
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=60),
    retry=retry_if_exception_type((RateLimitError, TimeoutError)),
    before_sleep=lambda retry_state: logger.warning(
        f"Retry {retry_state.attempt_number} for {retry_state.fn.__name__}"
    )
)
def llm_call_with_retry(messages, model):
    """LLM call with automatic retry."""
    return unified_client.chat(messages, model)

# Usage with custom retry
@with_retry(
    retry_config=RetryConfig(max_attempts=5, base_delay=2.0),
    exceptions=(RateLimitError, TimeoutError)
)
def safe_llm_call(messages, model):
    return unified_client.chat(messages, model)
```

---

## 5. Rate Limiting

```python
import time
from collections import deque
from threading import Lock
from typing import Optional

class RateLimiter:
    """Token bucket rate limiter."""

    def __init__(self, tokens_per_second: float, burst_size: int = 10):
        self.tokens_per_second = tokens_per_second
        self.burst_size = burst_size
        self.tokens = burst_size
        self.last_update = time.time()
        self.lock = Lock()

    def acquire(self, tokens: int = 1) -> bool:
        """Acquire tokens."""
        with self.lock:
            now = time.time()
            elapsed = now - self.last_update

            # Refill tokens
            self.tokens = min(
                self.burst_size,
                self.tokens + elapsed * self.tokens_per_second
            )
            self.last_update = now

            if self.tokens >= tokens:
                self.tokens -= tokens
                return True

            return False

    def wait_for_tokens(self, tokens: int = 1, timeout: Optional[float] = None):
        """Wait until tokens are available."""
        start_time = time.time()

        while True:
            if self.acquire(tokens):
                return True

            if timeout and (time.time() - start_time) > timeout:
                raise TimeoutError("Timeout waiting for rate limit")

            # Calculate wait time
            needed = tokens - self.tokens
            wait_time = needed / self.tokens_per_second
            time.sleep(wait_time)

class LLMRateLimiter:
    """Rate limiter for LLM calls."""

    def __init__(self):
        self.limiters = {
            LLMProvider.OPENAI: RateLimiter(tokens_per_second=3.0, burst_size=10),
            LLMProvider.ANTHROPIC: RateLimiter(tokens_per_second=5.0, burst_size=10),
        }

    def acquire(self, provider: LLMProvider, tokens: int = 1) -> bool:
        """Acquire tokens for provider."""
        limiter = self.limiters.get(provider)
        if limiter:
            return limiter.acquire(tokens)
        return True

    def wait_for_tokens(self, provider: LLMProvider, tokens: int = 1, timeout: float = 60.0):
        """Wait for tokens for provider."""
        limiter = self.limiters.get(provider)
        if limiter:
            limiter.wait_for_tokens(tokens, timeout)

# Usage
rate_limiter = LLMRateLimiter()

# Before making LLM call
rate_limiter.wait_for_tokens(LLMProvider.OPENAI, tokens=1)
response = unified_client.chat(messages, model="gpt-4", provider=LLMProvider.OPENAI)
```

---

## 6. Cost Tracking

```python
from dataclasses import dataclass
from typing import Dict, Optional
from datetime import datetime
import json

@dataclass
class LLMUsage:
    """LLM usage tracking."""
    provider: str
    model: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    timestamp: datetime
    cost: float = 0.0

class CostTracker:
    """Track LLM API costs."""

    # Pricing (example prices per 1K tokens)
    PRICING = {
        LLMProvider.OPENAI: {
            'gpt-4': {'input': 0.03, 'output': 0.06},
            'gpt-4-turbo': {'input': 0.01, 'output': 0.03},
            'gpt-3.5-turbo': {'input': 0.0005, 'output': 0.0015},
        },
        LLMProvider.ANTHROPIC: {
            'claude-3-opus': {'input': 0.015, 'output': 0.075},
            'claude-3-sonnet': {'input': 0.003, 'output': 0.015},
            'claude-3-haiku': {'input': 0.00025, 'output': 0.00125},
        },
    }

    def __init__(self):
        self.usage_history: List[LLMUsage] = []
        self.total_cost: float = 0.0

    def calculate_cost(
        self,
        provider: LLMProvider,
        model: str,
        input_tokens: int,
        output_tokens: int
    ) -> float:
        """Calculate cost for usage."""
        pricing = self.PRICING.get(provider, {}).get(model, {})
        input_cost = (input_tokens / 1000) * pricing.get('input', 0)
        output_cost = (output_tokens / 1000) * pricing.get('output', 0)
        return input_cost + output_cost

    def track_usage(
        self,
        provider: LLMProvider,
        model: str,
        input_tokens: int,
        output_tokens: int
    ):
        """Track LLM usage."""
        total_tokens = input_tokens + output_tokens
        cost = self.calculate_cost(provider, model, input_tokens, output_tokens)

        usage = LLMUsage(
            provider=provider.value,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            timestamp=datetime.now(),
            cost=cost
        )

        self.usage_history.append(usage)
        self.total_cost += cost

    def get_summary(self) -> Dict:
        """Get usage summary."""
        if not self.usage_history:
            return {}

        summary = {
            'total_cost': self.total_cost,
            'total_tokens': sum(u.total_tokens for u in self.usage_history),
            'total_requests': len(self.usage_history),
            'by_provider': {},
            'by_model': {}
        }

        for usage in self.usage_history:
            # By provider
            if usage.provider not in summary['by_provider']:
                summary['by_provider'][usage.provider] = {
                    'cost': 0.0,
                    'tokens': 0,
                    'requests': 0
                }
            summary['by_provider'][usage.provider]['cost'] += usage.cost
            summary['by_provider'][usage.provider]['tokens'] += usage.total_tokens
            summary['by_provider'][usage.provider]['requests'] += 1

            # By model
            if usage.model not in summary['by_model']:
                summary['by_model'][usage.model] = {
                    'cost': 0.0,
                    'tokens': 0,
                    'requests': 0
                }
            summary['by_model'][usage.model]['cost'] += usage.cost
            summary['by_model'][usage.model]['tokens'] += usage.total_tokens
            summary['by_model'][usage.model]['requests'] += 1

        return summary

    def export_history(self, filepath: str):
        """Export usage history to JSON."""
        data = [
            {
                'provider': u.provider,
                'model': u.model,
                'input_tokens': u.input_tokens,
                'output_tokens': u.output_tokens,
                'total_tokens': u.total_tokens,
                'timestamp': u.timestamp.isoformat(),
                'cost': u.cost
            }
            for u in self.usage_history
        ]

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

# Usage
cost_tracker = CostTracker()

# Track usage after each call
response = unified_client.chat(
    messages=[{"role": "user", "content": "Hello"}],
    model="gpt-4",
    provider=LLMProvider.OPENAI
)

# Get token usage from response
input_tokens = response.metadata.get('prompt_tokens', 0)
output_tokens = response.metadata.get('completion_tokens', 0)

cost_tracker.track_usage(
    provider=LLMProvider.OPENAI,
    model="gpt-4",
    input_tokens=input_tokens,
    output_tokens=output_tokens
)

# Get summary
summary = cost_tracker.get_summary()
print(f"Total cost: ${summary['total_cost']:.4f}")
```

---

## 7. Response Caching

```python
import hashlib
import json
from typing import Optional, Dict
from datetime import datetime, timedelta
import pickle
from pathlib import Path

class ResponseCache:
    """Cache LLM responses."""

    def __init__(self, cache_dir: str = './llm_cache', ttl_seconds: int = 3600):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl_seconds = ttl_seconds

    def _get_cache_key(
        self,
        messages: List[Dict],
        model: str,
        temperature: float,
        **kwargs
    ) -> str:
        """Generate cache key."""
        cache_data = {
            'messages': messages,
            'model': model,
            'temperature': temperature,
            **kwargs
        }

        data_str = json.dumps(cache_data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()

    def get(
        self,
        messages: List[Dict],
        model: str,
        temperature: float = 0.7,
        **kwargs
    ) -> Optional[str]:
        """Get cached response."""
        cache_key = self._get_cache_key(messages, model, temperature, **kwargs)
        cache_file = self.cache_dir / f"{cache_key}.pkl"

        if not cache_file.exists():
            return None

        # Check TTL
        file_time = datetime.fromtimestamp(cache_file.stat().st_mtime)
        if (datetime.now() - file_time).total_seconds() > self.ttl_seconds:
            cache_file.unlink()
            return None

        # Load cached response
        with open(cache_file, 'rb') as f:
            cached_data = pickle.load(f)

        return cached_data['response']

    def set(
        self,
        messages: List[Dict],
        model: str,
        response: str,
        temperature: float = 0.7,
        **kwargs
    ):
        """Cache response."""
        cache_key = self._get_cache_key(messages, model, temperature, **kwargs)
        cache_file = self.cache_dir / f"{cache_key}.pkl"

        cached_data = {
            'response': response,
            'timestamp': datetime.now().isoformat()
        }

        with open(cache_file, 'wb') as f:
            pickle.dump(cached_data, f)

    def clear(self):
        """Clear all cache."""
        for file in self.cache_dir.glob('*.pkl'):
            file.unlink()

# Usage with caching
cache = ResponseCache(ttl_seconds=3600)  # 1 hour TTL

def cached_llm_call(messages, model, **kwargs):
    """LLM call with caching."""
    # Check cache
    cached_response = cache.get(messages, model, **kwargs)
    if cached_response:
        return cached_response

    # Make API call
    response = unified_client.chat(messages, model, **kwargs)
    content = response.content

    # Cache response
    cache.set(messages, model, content, **kwargs)

    return content
```

---

## 8. Prompt Templates

```python
from typing import Dict, List, Optional
from string import Template
import json

class PromptTemplate:
    """Prompt template management."""

    def __init__(self, template: str, variables: List[str] = None):
        self.template = template
        self.variables = variables or self._extract_variables(template)
        self.template_obj = Template(template)

    def _extract_variables(self, template: str) -> List[str]:
        """Extract variables from template."""
        import re
        return list(set(re.findall(r'\{(\w+)\}', template)))

    def render(self, **kwargs) -> str:
        """Render template with variables."""
        missing_vars = set(self.variables) - set(kwargs.keys())
        if missing_vars:
            raise ValueError(f"Missing variables: {missing_vars}")

        return self.template_obj.substitute(**kwargs)

class PromptLibrary:
    """Library of prompt templates."""

    def __init__(self):
        self.templates: Dict[str, PromptTemplate] = {}

    def add_template(self, name: str, template: str, variables: List[str] = None):
        """Add template to library."""
        self.templates[name] = PromptTemplate(template, variables)

    def get_template(self, name: str) -> PromptTemplate:
        """Get template from library."""
        if name not in self.templates:
            raise ValueError(f"Template '{name}' not found")
        return self.templates[name]

    def render(self, name: str, **kwargs) -> str:
        """Render template from library."""
        template = self.get_template(name)
        return template.render(**kwargs)

    def load_from_file(self, filepath: str):
        """Load templates from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)

        for name, template_data in data.items():
            self.add_template(
                name=name,
                template=template_data['template'],
                variables=template_data.get('variables')
            )

# Example templates
library = PromptLibrary()

# Simple Q&A
library.add_template(
    name='simple_qa',
    template='Question: {question}\n\nAnswer:',
    variables=['question']
)

# Few-shot learning
library.add_template(
    name='few_shot',
    template='''Examples:
{examples}

Question: {question}
Answer:''',
    variables=['examples', 'question']
)

# Chain of thought
library.add_template(
    name='chain_of_thought',
    template='''Let's think step by step.

{question}

Step 1: {step1}
Step 2: {step2}
Final Answer:''',
    variables=['question', 'step1', 'step2']
)

# Usage
prompt = library.render(
    'simple_qa',
    question='What is the capital of France?'
)

print(prompt)
```

---

## 9. Token Counting

```python
import tiktoken
from typing import Dict, List

class TokenCounter:
    """Count tokens for different models."""

    def __init__(self):
        self.encoders = {
            'gpt-4': tiktoken.encoding_for_model('gpt-4'),
            'gpt-3.5-turbo': tiktoken.encoding_for_model('gpt-3.5-turbo'),
            'text-davinci-003': tiktoken.encoding_for_model('text-davinci-003'),
        }

    def count_tokens(self, text: str, model: str = 'gpt-4') -> int:
        """Count tokens for text."""
        encoder = self.encoders.get(model, self.encoders['gpt-4'])
        return len(encoder.encode(text))

    def count_messages_tokens(
        self,
        messages: List[Dict],
        model: str = 'gpt-4'
    ) -> Dict[str, int]:
        """Count tokens for messages."""
        encoder = self.encoders.get(model, self.encoders['gpt-4'])

        tokens_per_message = 3
        tokens_per_name = 1

        num_tokens = 0

        for message in messages:
            num_tokens += tokens_per_message
            for key, value in message.items():
                num_tokens += tokens_per_name
                num_tokens += len(encoder.encode(value))

        return {
            'total_tokens': num_tokens,
            'input_tokens': num_tokens
        }

    def estimate_output_tokens(
        self,
        input_tokens: int,
        output_length_ratio: float = 1.5
    ) -> int:
        """Estimate output tokens based on input."""
        return int(input_tokens * output_length_ratio)

    def truncate_to_max_tokens(
        self,
        text: str,
        max_tokens: int,
        model: str = 'gpt-4'
    ) -> str:
        """Truncate text to max tokens."""
        encoder = self.encoders.get(model, self.encoders['gpt-4'])
        tokens = encoder.encode(text)

        if len(tokens) <= max_tokens:
            return text

        truncated_tokens = tokens[:max_tokens]
        return encoder.decode(truncated_tokens)

# Usage
counter = TokenCounter()

text = "Hello, how are you today? I hope you're doing well."
token_count = counter.count_tokens(text, model='gpt-4')
print(f"Token count: {token_count}")

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
]

message_tokens = counter.count_messages_tokens(messages, model='gpt-4')
print(f"Message tokens: {message_tokens}")
```

---

## 10. Context Window Management

```python
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class ContextWindow:
    """Context window configuration."""
    max_tokens: int
    reserved_tokens: int = 100  # For system messages and output

    @property
    def available_tokens(self) -> int:
        return self.max_tokens - self.reserved_tokens

class ContextManager:
    """Manage context window for LLM calls."""

    def __init__(self, token_counter: TokenCounter, context_window: ContextWindow):
        self.token_counter = token_counter
        self.context_window = context_window

    def fit_messages(
        self,
        messages: List[Dict],
        model: str = 'gpt-4'
    ) -> Tuple[List[Dict], int]:
        """Fit messages into context window."""
        fitted_messages = []
        total_tokens = 0

        # Add system messages first
        system_messages = [m for m in messages if m.get('role') == 'system']
        for msg in system_messages:
            msg_tokens = self.token_counter.count_tokens(msg['content'], model)
            total_tokens += msg_tokens
            fitted_messages.append(msg)

        # Add other messages from newest to oldest
        other_messages = [m for m in messages if m.get('role') != 'system']
        for msg in reversed(other_messages):
            msg_tokens = self.token_counter.count_tokens(msg['content'], model)

            if total_tokens + msg_tokens > self.context_window.available_tokens:
                break

            fitted_messages.insert(0, msg)
            total_tokens += msg_tokens

        return fitted_messages, total_tokens

    def truncate_message(
        self,
        message: Dict,
        model: str = 'gpt-4'
    ) -> Dict:
        """Truncate message to fit context."""
        content = message['content']
        max_tokens = self.context_window.available_tokens

        current_tokens = self.token_counter.count_tokens(content, model)

        if current_tokens <= max_tokens:
            return message

        truncated_content = self.token_counter.truncate_to_max_tokens(
            content, max_tokens, model
        )

        return {**message, 'content': truncated_content}

# Context windows for different models
CONTEXT_WINDOWS = {
    'gpt-4': ContextWindow(max_tokens=8192, reserved_tokens=500),
    'gpt-4-turbo': ContextWindow(max_tokens=128000, reserved_tokens=500),
    'gpt-3.5-turbo': ContextWindow(max_tokens=16385, reserved_tokens=500),
    'claude-3-opus': ContextWindow(max_tokens=200000, reserved_tokens=500),
    'claude-3-sonnet': ContextWindow(max_tokens=200000, reserved_tokens=500),
}

# Usage
counter = TokenCounter()
context_manager = ContextManager(
    token_counter=counter,
    context_window=CONTEXT_WINDOWS['gpt-4']
)

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"},
    {"role": "assistant", "content": "Hi there!"},
    {"role": "user", "content": "How are you?"},
]

fitted_messages, tokens_used = context_manager.fit_messages(messages)
print(f"Fitted {len(fitted_messages)} messages using {tokens_used} tokens")
```

---

## 11. Multi-Provider Fallback

```python
from typing import List, Optional, Callable
import logging

logger = logging.getLogger(__name__)

class FallbackStrategy:
    """Strategy for provider fallback."""

    def __init__(
        self,
        providers: List[LLMProvider],
        fallback_condition: Optional[Callable] = None
    ):
        self.providers = providers
        self.fallback_condition = fallback_condition

    def get_provider(
        self,
        attempt: int,
        last_error: Optional[Exception] = None
    ) -> LLMProvider:
        """Get provider for current attempt."""
        if self.fallback_condition and last_error:
            # Use custom fallback logic
            return self.fallback_condition(attempt, last_error)

        # Sequential fallback
        return self.providers[min(attempt, len(self.providers) - 1)]

class FallbackLLMClient:
    """LLM client with automatic fallback."""

    def __init__(
        self,
        clients: Dict[LLMProvider, BaseLLMClient],
        strategy: FallbackStrategy
    ):
        self.clients = clients
        self.strategy = strategy

    def chat(
        self,
        messages: List[Dict],
        model: str,
        max_attempts: int = 3,
        **kwargs
    ) -> LLMResponse:
        """Chat with fallback between providers."""
        last_error = None

        for attempt in range(max_attempts):
            provider = self.strategy.get_provider(attempt, last_error)
            client = self.clients.get(provider)

            try:
                logger.info(f"Attempt {attempt + 1} using {provider.value}")
                return client.chat(messages, model, **kwargs)

            except Exception as e:
                last_error = e
                logger.warning(
                    f"Attempt {attempt + 1} failed with {provider.value}: {e}"
                )

                # Check if we should retry with same provider
                if attempt < max_attempts - 1:
                    continue

        raise last_error or Exception("All attempts failed")

# Usage
clients = {
    LLMProvider.OPENAI: OpenAIClient(api_key=os.getenv('OPENAI_API_KEY')),
    LLMProvider.ANTHROPIC: AnthropicClient(api_key=os.getenv('ANTHROPIC_API_KEY')),
}

strategy = FallbackStrategy(
    providers=[LLMProvider.OPENAI, LLMProvider.ANTHROPIC],
    fallback_condition=lambda attempt, error: LLMProvider.ANTHROPIC if attempt > 0 else LLMProvider.OPENAI
)

fallback_client = FallbackLLMClient(clients, strategy)

response = fallback_client.chat(
    messages=[{"role": "user", "content": "Hello!"}],
    model="gpt-4",
    max_attempts=3
)
```

---

## 12. Production Patterns

### 12.1 Async Batch Processing

```python
import asyncio
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor

class BatchLLMProcessor:
    """Process multiple LLM requests efficiently."""

    def __init__(self, client: UnifiedLLMClient, max_concurrent: int = 5):
        self.client = client
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def process_single(
        self,
        messages: List[Dict],
        model: str,
        **kwargs
    ) -> LLMResponse:
        """Process single request."""
        async with self.semaphore:
            return await self.client.achat(messages, model, **kwargs)

    async def process_batch(
        self,
        requests: List[Dict],
        model: str,
        **kwargs
    ) -> List[LLMResponse]:
        """Process batch of requests."""
        tasks = [
            self.process_single(req['messages'], model, **kwargs)
            for req in requests
        ]

        return await asyncio.gather(*tasks, return_exceptions=True)

    def process_batch_sync(
        self,
        requests: List[Dict],
        model: str,
        **kwargs
    ) -> List[LLMResponse]:
        """Process batch synchronously."""
        with ThreadPoolExecutor(max_workers=self.max_concurrent) as executor:
            futures = [
                executor.submit(
                    self.client.chat,
                    req['messages'],
                    model,
                    **kwargs
                )
                for req in requests
            ]

            results = []
            for future in futures:
                try:
                    results.append(future.result())
                except Exception as e:
                    logger.error(f"Request failed: {e}")
                    results.append(None)

            return results

# Usage
processor = BatchLLMProcessor(unified_client, max_concurrent=5)

requests = [
    {"messages": [{"role": "user", "content": f"Hello {i}!"}], "model": "gpt-4"}
    for i in range(10)
]

# Async batch processing
results = asyncio.run(processor.process_batch(requests, "gpt-4"))

# Sync batch processing
results = processor.process_batch_sync(requests, "gpt-4")
```

### 12.2 Request Queue

```python
import queue
import threading
from typing import Callable, Optional

class LLMRequestQueue:
    """Queue for LLM requests with worker threads."""

    def __init__(
        self,
        client: UnifiedLLMClient,
        num_workers: int = 3,
        callback: Optional[Callable] = None
    ):
        self.client = client
        self.num_workers = num_workers
        self.callback = callback
        self.queue = queue.Queue()
        self.workers = []
        self.running = False

    def start(self):
        """Start worker threads."""
        self.running = True
        for i in range(self.num_workers):
            worker = threading.Thread(target=self._worker, daemon=True)
            worker.start()
            self.workers.append(worker)

    def stop(self):
        """Stop worker threads."""
        self.running = False
        for worker in self.workers:
            worker.join()

    def _worker(self):
        """Worker thread function."""
        while self.running:
            try:
                # Get request from queue
                request = self.queue.get(timeout=1.0)

                # Process request
                response = self.client.chat(
                    request['messages'],
                    request['model'],
                    **request.get('kwargs', {})
                )

                # Callback
                if self.callback:
                    self.callback(request, response)

                self.queue.task_done()

            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Worker error: {e}")

    def enqueue(
        self,
        messages: List[Dict],
        model: str,
        request_id: str = None,
        **kwargs
    ):
        """Enqueue request."""
        self.queue.put({
            'messages': messages,
            'model': model,
            'request_id': request_id,
            'kwargs': kwargs
        })

# Usage
def on_response(request, response):
    """Callback for completed requests."""
    print(f"Request {request.get('request_id')}: {response.content[:50]}...")

queue = LLMRequestQueue(unified_client, num_workers=3, callback=on_response)
queue.start()

# Enqueue requests
for i in range(10):
    queue.enqueue(
        messages=[{"role": "user", "content": f"Hello {i}!"}],
        model="gpt-4",
        request_id=f"req_{i}"
    )
```

---

## 13. Monitoring and Logging

```python
import logging
import time
from typing import Dict, Any
from datetime import datetime
import json

class LLMLogger:
    """Logger for LLM interactions."""

    def __init__(self, log_file: str = 'llm_interactions.jsonl'):
        self.log_file = log_file
        self.logger = logging.getLogger('llm_logger')
        self.logger.setLevel(logging.INFO)

        # File handler
        handler = logging.FileHandler(log_file)
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)

    def log_interaction(
        self,
        request: Dict[str, Any],
        response: LLMResponse,
        duration_ms: float,
        metadata: Dict[str, Any] = None
    ):
        """Log LLM interaction."""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'duration_ms': duration_ms,
            'request': {
                'messages': request.get('messages'),
                'model': request.get('model'),
                'temperature': request.get('temperature'),
                'max_tokens': request.get('max_tokens'),
            },
            'response': {
                'content': response.content,
                'model': response.model,
                'provider': response.provider.value,
                'tokens_used': response.tokens_used,
                'finish_reason': response.finish_reason,
            },
            'metadata': metadata or {}
        }

        self.logger.info(json.dumps(log_entry))

    def log_error(
        self,
        request: Dict[str, Any],
        error: Exception,
        duration_ms: float
    ):
        """Log LLM error."""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'duration_ms': duration_ms,
            'error': {
                'type': type(error).__name__,
                'message': str(error),
            },
            'request': {
                'messages': request.get('messages'),
                'model': request.get('model'),
            }
        }

        self.logger.error(json.dumps(log_entry))

# Usage
llm_logger = LLMLogger()

start_time = time.time()
try:
    response = unified_client.chat(
        messages=[{"role": "user", "content": "Hello!"}],
        model="gpt-4"
    )
    duration = (time.time() - start_time) * 1000

    llm_logger.log_interaction(
        request={'messages': [{"role": "user", "content": "Hello!"}], 'model': "gpt-4"},
        response=response,
        duration_ms=duration
    )
except Exception as e:
    duration = (time.time() - start_time) * 1000
    llm_logger.log_error(
        request={'messages': [{"role": "user", "content": "Hello!"}], 'model': "gpt-4"},
        error=e,
        duration_ms=duration
    )
```

---

## 14. Best Practices

### 14.1 API Key Management

```python
import os
from typing import Dict

class APIKeyManager:
    """Secure API key management."""

    def __init__(self):
        self.keys: Dict[str, str] = {}

    def load_from_env(self):
        """Load keys from environment variables."""
        self.keys = {
            'OPENAI': os.getenv('OPENAI_API_KEY'),
            'ANTHROPIC': os.getenv('ANTHROPIC_API_KEY'),
            'AZURE_OPENAI': os.getenv('AZURE_OPENAI_API_KEY'),
            'COHERE': os.getenv('COHERE_API_KEY'),
        }

    def get_key(self, provider: str) -> str:
        """Get API key for provider."""
        key = self.keys.get(provider)
        if not key:
            raise ValueError(f"API key not found for {provider}")
        return key

    def rotate_key(self, provider: str, new_key: str):
        """Rotate API key."""
        self.keys[provider] = new_key
        # Update environment variable
        os.environ[f"{provider.upper()}_API_KEY"] = new_key

# Usage
key_manager = APIKeyManager()
key_manager.load_from_env()

openai_key = key_manager.get_key('OPENAI')
```

### 14.2 Error Recovery

```python
class ErrorRecoveryStrategy:
    """Error recovery strategies."""

    @staticmethod
    def should_retry(error: Exception) -> bool:
        """Determine if error is retryable."""
        retryable_errors = (
            RateLimitError,
            TimeoutError,
            ConnectionError,
        )
        return isinstance(error, retryable_errors)

    @staticmethod
    def get_backoff_delay(attempt: int, max_delay: float = 60.0) -> float:
        """Calculate exponential backoff delay."""
        return min(2 ** attempt, max_delay)

    @staticmethod
    def handle_rate_limit(error: RateLimitError) -> float:
        """Handle rate limit errors."""
        # Extract retry-after from error if available
        retry_after = getattr(error, 'retry_after', None)
        if retry_after:
            return retry_after
        return ErrorRecoveryStrategy.get_backoff_delay(3)
```

---

## Related Skills

- [`06-ai-ml-production/prompt-engineering`](06-ai-ml-production/prompt-engineering/SKILL.md)
- [`06-ai-ml-production/llm-function-calling`](06-ai-ml-production/llm-function-calling/SKILL.md)
- [`06-ai-ml-production/llm-guardrails`](06-ai-ml-production/llm-guardrails/SKILL.md)
- [`06-ai-ml-production/agent-patterns`](06-ai-ml-production/agent-patterns/SKILL.md)
- [`06-ai-ml-production/ai-observability`](06-ai-ml-production/ai-observability/SKILL.md)
- [`06-ai-ml-production/embedding-models`](06-ai-ml-production/embedding-models/SKILL.md)

## Additional Resources

- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [Anthropic API Documentation](https://docs.anthropic.com/)
- [Azure OpenAI Documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [Cohere API Documentation](https://docs.cohere.com/)
