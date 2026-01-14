# LLM API Integration Guide

## Overview
การเชื่อมต่อกับ LLM providers (OpenAI, Anthropic, Cohere, etc.) แบบ production-ready

## Supported Providers

### 1. OpenAI
```typescript
import OpenAI from 'openai'

const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
})

async function generateCompletion(prompt: string) {
  const completion = await client.chat.completions.create({
    model: 'gpt-4-turbo-preview',
    messages: [{ role: 'user', content: prompt }],
    temperature: 0.7,
    max_tokens: 1000,
  })
  
  return completion.choices[0].message.content
}
```

### 2. Anthropic Claude
```typescript
import Anthropic from '@anthropic-ai/sdk'

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
})

async function generateCompletion(prompt: string) {
  const message = await client.messages.create({
    model: 'claude-3-opus-20240229',
    max_tokens: 1024,
    messages: [{ role: 'user', content: prompt }],
  })
  
  return message.content[0].text
}
```

### 3. Azure OpenAI
```typescript
import { OpenAIClient, AzureKeyCredential } from '@azure/openai'

const client = new OpenAIClient(
  process.env.AZURE_OPENAI_ENDPOINT!,
  new AzureKeyCredential(process.env.AZURE_OPENAI_KEY!)
)

async function generateCompletion(prompt: string) {
  const result = await client.getCompletions(
    'gpt-4-deployment', // Your deployment name
    [prompt],
    { maxTokens: 1000 }
  )
  
  return result.choices[0].text
}
```

## Unified LLM Interface Pattern
```typescript
// Abstract interface
interface LLMProvider {
  generateCompletion(prompt: string, options?: CompletionOptions): Promise<string>
  generateStream(prompt: string, options?: CompletionOptions): AsyncIterable<string>
}

interface CompletionOptions {
  temperature?: number
  maxTokens?: number
  topP?: number
  model?: string
}

// OpenAI Implementation
class OpenAIProvider implements LLMProvider {
  constructor(private client: OpenAI) {}
  
  async generateCompletion(
    prompt: string,
    options: CompletionOptions = {}
  ): Promise<string> {
    const completion = await this.client.chat.completions.create({
      model: options.model || 'gpt-4-turbo-preview',
      messages: [{ role: 'user', content: prompt }],
      temperature: options.temperature ?? 0.7,
      max_tokens: options.maxTokens ?? 1000,
    })
    
    return completion.choices[0].message.content || ''
  }
  
  async *generateStream(
    prompt: string,
    options: CompletionOptions = {}
  ): AsyncIterable<string> {
    const stream = await this.client.chat.completions.create({
      model: options.model || 'gpt-4-turbo-preview',
      messages: [{ role: 'user', content: prompt }],
      temperature: options.temperature ?? 0.7,
      max_tokens: options.maxTokens ?? 1000,
      stream: true,
    })
    
    for await (const chunk of stream) {
      const content = chunk.choices[0]?.delta?.content
      if (content) yield content
    }
  }
}

// Anthropic Implementation
class AnthropicProvider implements LLMProvider {
  constructor(private client: Anthropic) {}
  
  async generateCompletion(
    prompt: string,
    options: CompletionOptions = {}
  ): Promise<string> {
    const message = await this.client.messages.create({
      model: options.model || 'claude-3-opus-20240229',
      max_tokens: options.maxTokens ?? 1024,
      messages: [{ role: 'user', content: prompt }],
      temperature: options.temperature,
    })
    
    const textContent = message.content.find(c => c.type === 'text')
    return textContent?.text || ''
  }
  
  async *generateStream(
    prompt: string,
    options: CompletionOptions = {}
  ): AsyncIterable<string> {
    const stream = await this.client.messages.create({
      model: options.model || 'claude-3-opus-20240229',
      max_tokens: options.maxTokens ?? 1024,
      messages: [{ role: 'user', content: prompt }],
      temperature: options.temperature,
      stream: true,
    })
    
    for await (const event of stream) {
      if (event.type === 'content_block_delta' && event.delta.type === 'text_delta') {
        yield event.delta.text
      }
    }
  }
}

// Factory Pattern
class LLMFactory {
  static create(provider: 'openai' | 'anthropic' | 'azure'): LLMProvider {
    switch (provider) {
      case 'openai':
        return new OpenAIProvider(new OpenAI({
          apiKey: process.env.OPENAI_API_KEY,
        }))
      case 'anthropic':
        return new AnthropicProvider(new Anthropic({
          apiKey: process.env.ANTHROPIC_API_KEY,
        }))
      case 'azure':
        // Azure implementation
        throw new Error('Not implemented')
      default:
        throw new Error(`Unknown provider: ${provider}`)
    }
  }
}
```

## Error Handling & Retry Logic
```typescript
import pRetry from 'p-retry'

async function generateWithRetry(
  provider: LLMProvider,
  prompt: string,
  options?: CompletionOptions
): Promise<string> {
  return pRetry(
    async () => {
      try {
        return await provider.generateCompletion(prompt, options)
      } catch (error) {
        // Retry on rate limit or server errors
        if (error.status === 429 || error.status >= 500) {
          throw error // Retry
        }
        // Don't retry on client errors
        throw new pRetry.AbortError(error.message)
      }
    },
    {
      retries: 3,
      factor: 2,
      minTimeout: 1000,
      maxTimeout: 10000,
      onFailedAttempt: (error) => {
        console.log(
          `Attempt ${error.attemptNumber} failed. ${error.retriesLeft} retries left.`
        )
      },
    }
  )
}
```

## Rate Limiting
```typescript
import Bottleneck from 'bottleneck'

class RateLimitedLLMProvider implements LLMProvider {
  private limiter: Bottleneck
  
  constructor(
    private provider: LLMProvider,
    options: {
      maxConcurrent?: number
      minTime?: number  // ms between requests
      reservoir?: number  // max requests
      reservoirRefreshAmount?: number
      reservoirRefreshInterval?: number  // ms
    }
  ) {
    this.limiter = new Bottleneck({
      maxConcurrent: options.maxConcurrent ?? 5,
      minTime: options.minTime ?? 200,
      reservoir: options.reservoir,
      reservoirRefreshAmount: options.reservoirRefreshAmount,
      reservoirRefreshInterval: options.reservoirRefreshInterval,
    })
  }
  
  async generateCompletion(
    prompt: string,
    options?: CompletionOptions
  ): Promise<string> {
    return this.limiter.schedule(() =>
      this.provider.generateCompletion(prompt, options)
    )
  }
  
  async *generateStream(
    prompt: string,
    options?: CompletionOptions
  ): AsyncIterable<string> {
    // Stream doesn't go through rate limiter
    yield* this.provider.generateStream(prompt, options)
  }
}

// Usage
const baseProvider = LLMFactory.create('openai')
const limitedProvider = new RateLimitedLLMProvider(baseProvider, {
  maxConcurrent: 5,
  minTime: 200,
  reservoir: 100,           // 100 requests
  reservoirRefreshAmount: 100,
  reservoirRefreshInterval: 60 * 1000,  // per minute
})
```

## Cost Tracking
```typescript
interface UsageMetrics {
  promptTokens: number
  completionTokens: number
  totalTokens: number
  cost: number
}

class TrackedLLMProvider implements LLMProvider {
  private totalUsage: UsageMetrics = {
    promptTokens: 0,
    completionTokens: 0,
    totalTokens: 0,
    cost: 0,
  }
  
  // Token costs per 1K tokens (example prices)
  private costs = {
    'gpt-4-turbo-preview': { prompt: 0.01, completion: 0.03 },
    'gpt-3.5-turbo': { prompt: 0.0015, completion: 0.002 },
    'claude-3-opus-20240229': { prompt: 0.015, completion: 0.075 },
  }
  
  constructor(private provider: LLMProvider, private model: string) {}
  
  async generateCompletion(
    prompt: string,
    options?: CompletionOptions
  ): Promise<string> {
    const result = await this.provider.generateCompletion(prompt, options)
    
    // Track usage (you'd get this from the API response in real implementation)
    const promptTokens = this.estimateTokens(prompt)
    const completionTokens = this.estimateTokens(result)
    
    const cost = this.calculateCost(promptTokens, completionTokens)
    
    this.totalUsage.promptTokens += promptTokens
    this.totalUsage.completionTokens += completionTokens
    this.totalUsage.totalTokens += promptTokens + completionTokens
    this.totalUsage.cost += cost
    
    // Log to database or metrics system
    await this.logUsage({
      model: this.model,
      promptTokens,
      completionTokens,
      cost,
      timestamp: new Date(),
    })
    
    return result
  }
  
  private calculateCost(promptTokens: number, completionTokens: number): number {
    const pricing = this.costs[this.model]
    return (
      (promptTokens / 1000) * pricing.prompt +
      (completionTokens / 1000) * pricing.completion
    )
  }
  
  private estimateTokens(text: string): number {
    // Rough estimation: ~4 chars per token
    return Math.ceil(text.length / 4)
  }
  
  private async logUsage(usage: any): Promise<void> {
    // Log to your metrics system
    await db.llmUsage.create({ data: usage })
  }
  
  getUsage(): UsageMetrics {
    return { ...this.totalUsage }
  }
}
```

## Caching Responses
```typescript
import { createHash } from 'crypto'

class CachedLLMProvider implements LLMProvider {
  constructor(
    private provider: LLMProvider,
    private cache: Redis
  ) {}
  
  async generateCompletion(
    prompt: string,
    options?: CompletionOptions
  ): Promise<string> {
    // Generate cache key
    const cacheKey = this.getCacheKey(prompt, options)
    
    // Check cache
    const cached = await this.cache.get(cacheKey)
    if (cached) {
      console.log('Cache hit')
      return cached
    }
    
    // Generate completion
    const result = await this.provider.generateCompletion(prompt, options)
    
    // Cache result (TTL: 1 hour)
    await this.cache.setEx(cacheKey, 3600, result)
    
    return result
  }
  
  private getCacheKey(prompt: string, options?: CompletionOptions): string {
    const data = JSON.stringify({ prompt, options })
    return `llm:${createHash('sha256').update(data).digest('hex')}`
  }
  
  async *generateStream(
    prompt: string,
    options?: CompletionOptions
  ): AsyncIterable<string> {
    // Streams are not cached
    yield* this.provider.generateStream(prompt, options)
  }
}
```

## Complete Usage Example
```typescript
// Setup providers with all features
async function setupLLMService() {
  // 1. Base provider
  const baseProvider = LLMFactory.create('openai')
  
  // 2. Add rate limiting
  const rateLimited = new RateLimitedLLMProvider(baseProvider, {
    maxConcurrent: 5,
    minTime: 200,
  })
  
  // 3. Add caching
  const redis = await createClient({ url: process.env.REDIS_URL }).connect()
  const cached = new CachedLLMProvider(rateLimited, redis)
  
  // 4. Add usage tracking
  const tracked = new TrackedLLMProvider(cached, 'gpt-4-turbo-preview')
  
  return tracked
}

// Use the service
const llm = await setupLLMService()

const response = await generateWithRetry(llm, 'Explain quantum computing', {
  temperature: 0.7,
  maxTokens: 500,
})

console.log(response)
console.log('Total usage:', llm.getUsage())
```

## Best Practices

- [ ] Always use retry logic for production
- [ ] Implement rate limiting per provider limits
- [ ] Track token usage and costs
- [ ] Cache responses where appropriate
- [ ] Use streaming for long responses
- [ ] Handle errors gracefully
- [ ] Set reasonable timeouts
- [ ] Log all API calls for debugging
- [ ] Monitor API quotas
- [ ] Have fallback providers