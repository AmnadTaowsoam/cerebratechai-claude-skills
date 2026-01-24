---
name: Skill Discovery & Chaining
description: Discover relevant skills for tasks, analyze skill compatibility, chain skills together, handle skill failures, and optimize skill sequences
---

# Skill Discovery & Chaining

## Overview

Skill discovery and chaining คือการค้นหา skills ที่เหมาะสมสำหรับงาน วิเคราะห์ compatibility ระหว่าง skills และ chain skills เข้าด้วยกันเพื่อแก้ปัญหาที่ซับซ้อน รวมถึงการจัดการ failures และ optimize sequences

## Why This Matters

- **Efficiency**: เลือก skills ที่เหมาะสมที่สุดสำหรับแต่ละงาน
- **Flexibility**: Chain skills ได้หลายแบบ ไม่จำกัด patterns
- **Reliability**: Handle failures อย่าง graceful
- **Optimization**: Reduce redundant skill calls และ improve performance

---

## Core Concepts

### 1. Skill Discovery

```typescript
interface SkillMatch {
  skill: Skill
  relevance: number
  confidence: number
  reasons: string[]
}

class SkillDiscovery {
  private registry: SkillRegistry
  private embeddings: Map<string, number[]> = new Map()

  constructor(registry: SkillRegistry) {
    this.registry = registry
  }

  async discover(query: string): Promise<SkillMatch[]> {
    const queryEmbedding = await this.getEmbedding(query)
    const matches: SkillMatch[] = []

    for (const skill of this.registry.getAll()) {
      const match = await this.matchSkill(query, queryEmbedding, skill)
      if (match.relevance > 0.5) {
        matches.push(match)
      }
    }

    // Sort by relevance
    return matches.sort((a, b) => b.relevance - a.relevance)
  }

  private async matchSkill(
    query: string,
    queryEmbedding: number[],
    skill: Skill
  ): Promise<SkillMatch> {
    const reasons: string[] = []
    let relevance = 0
    let confidence = 0.5

    // Semantic similarity
    const skillEmbedding = await this.getEmbedding(skill.description)
    const similarity = this.cosineSimilarity(queryEmbedding, skillEmbedding)
    relevance += similarity * 0.4
    reasons.push(`Semantic similarity: ${similarity.toFixed(2)}`)

    // Keyword matching
    const queryKeywords = this.extractKeywords(query)
    const skillKeywords = this.extractKeywords(skill.description)
    const keywordMatch = this.jaccardSimilarity(queryKeywords, skillKeywords)
    relevance += keywordMatch * 0.3
    reasons.push(`Keyword match: ${(keywordMatch * 100).toFixed(0)}%`)

    // Capability matching
    const capabilityMatch = this.matchCapabilities(query, skill)
    relevance += capabilityMatch * 0.3
    if (capabilityMatch > 0) {
      reasons.push(`Capability match: ${skill.capabilities.join(', ')}`)
    }

    return {
      skill,
      relevance: Math.min(1, relevance),
      confidence,
      reasons,
    }
  }

  private async getEmbedding(text: string): Promise<number[]> {
    // Get embedding from LLM or embedding model
    // This is a placeholder
    return []
  }

  private cosineSimilarity(a: number[], b: number[]): number {
    let dotProduct = 0
    let normA = 0
    let normB = 0

    for (let i = 0; i < a.length; i++) {
      dotProduct += a[i] * b[i]
      normA += a[i] * a[i]
      normB += b[i] * b[i]
    }

    return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB))
  }

  private extractKeywords(text: string): Set<string> {
    const words = text.toLowerCase().split(/\W+/)
    const stopWords = new Set(['the', 'a', 'an', 'is', 'are', 'to', 'for'])
    return new Set(words.filter(w => w.length > 2 && !stopWords.has(w)))
  }

  private jaccardSimilarity(a: Set<string>, b: Set<string>): number {
    const intersection = new Set([...a].filter(x => b.has(x)))
    const union = new Set([...a, ...b])
    return intersection.size / union.size
  }

  private matchCapabilities(query: string, skill: Skill): number {
    const queryLower = query.toLowerCase()
    let matchCount = 0

    for (const capability of skill.capabilities) {
      if (queryLower.includes(capability.toLowerCase())) {
        matchCount++
      }
    }

    return matchCount / skill.capabilities.length
  }
}

// Usage
const discovery = new SkillDiscovery(registry)

const matches = await discovery.discover('Generate a REST API for user management')
console.log('Matching skills:', matches)
```

### 2. Skill Compatibility Analysis

```typescript
interface CompatibilityResult {
  compatible: boolean
  score: number
  issues: string[]
  warnings: string[]
}

class SkillCompatibilityAnalyzer {
  analyze(skillA: Skill, skillB: Skill): CompatibilityResult {
    const issues: string[] = []
    const warnings: string[] = []
    let score = 1.0

    // Check output-input compatibility
    const outputInputMatch = this.checkOutputInputCompatibility(skillA, skillB)
    score *= outputInputMatch.score
    issues.push(...outputInputMatch.issues)
    warnings.push(...outputInputMatch.warnings)

    // Check dependency conflicts
    const depConflict = this.checkDependencyConflicts(skillA, skillB)
    score *= depConflict.score
    issues.push(...depConflict.issues)
    warnings.push(...depConflict.warnings)

    // Check resource conflicts
    const resourceConflict = this.checkResourceConflicts(skillA, skillB)
    score *= resourceConflict.score
    issues.push(...resourceConflict.issues)
    warnings.push(...resourceConflict.warnings)

    return {
      compatible: issues.length === 0,
      score,
      issues,
      warnings,
    }
  }

  private checkOutputInputCompatibility(
    skillA: Skill,
    skillB: Skill
  ): { score: number; issues: string[]; warnings: string[] } {
    const issues: string[] = []
    const warnings: string[] = []
    let score = 1.0

    // Check if skillA outputs can feed skillB inputs
    const requiredInputs = skillB.inputs.filter(i => i.required)
    const availableOutputs = skillA.outputs

    for (const input of requiredInputs) {
      const matchingOutput = availableOutputs.find(o => o.name === input.name)
      if (!matchingOutput) {
        issues.push(`Missing output: ${input.name} required by ${skillB.name}`)
        score -= 0.3
      } else if (matchingOutput.type !== input.type) {
        warnings.push(
          `Type mismatch: ${input.name} is ${input.type}, expected ${matchingOutput.type}`
        )
        score -= 0.1
      }
    }

    return { score: Math.max(0, score), issues, warnings }
  }

  private checkDependencyConflicts(
    skillA: Skill,
    skillB: Skill
  ): { score: number; issues: string[]; warnings: string[] } {
    const issues: string[] = []
    const warnings: string[] = []
    let score = 1.0

    // Check for conflicting dependencies
    const depsA = new Set(skillA.dependencies)
    const depsB = new Set(skillB.dependencies)

    // Check if skills depend on each other (circular dependency)
    if (depsA.has(skillB.id) && depsB.has(skillA.id)) {
      issues.push('Circular dependency detected')
      score = 0
    }

    // Check for version conflicts
    const commonDeps = [...depsA].filter(d => depsB.has(d))
    for (const dep of commonDeps) {
      // Check if versions are compatible
      // (implementation depends on dependency management system)
    }

    return { score: Math.max(0, score), issues, warnings }
  }

  private checkResourceConflicts(
    skillA: Skill,
    skillB: Skill
  ): { score: number; issues: string[]; warnings: string[] } {
    const issues: string[] = []
    const warnings: string[] = []
    let score = 1.0

    // Check if skills use conflicting resources
    // (implementation depends on resource tracking)

    return { score, issues, warnings }
  }
}

// Usage
const analyzer = new SkillCompatibilityAnalyzer()

const compatibility = analyzer.analyze(skill1, skill2)
console.log('Compatibility:', compatibility)
```

### 3. Skill Chaining

```typescript
interface SkillChain {
  id: string
  skills: Skill[]
  connections: SkillConnection[]
  inputSchema: any
  outputSchema: any
}

class SkillChainer {
  private discovery: SkillDiscovery
  private analyzer: SkillCompatibilityAnalyzer

  constructor(
    discovery: SkillDiscovery,
    analyzer: SkillCompatibilityAnalyzer
  ) {
    this.discovery = discovery
    this.analyzer = analyzer
  }

  async buildChain(
    task: string,
    maxSkills: number = 5
  ): Promise<SkillChain> {
    const chain: Skill[] = []
    const connections: SkillConnection[] = []

    // Discover initial skills
    const matches = await this.discovery.discover(task)

    // Select best skill
    const firstSkill = matches[0].skill
    chain.push(firstSkill)

    // Build chain iteratively
    let currentSkill = firstSkill
    let currentContext = this.extractContext(task)

    while (chain.length < maxSkills) {
      // Find next skill that can use current output
      const nextSkill = await this.findNextSkill(currentSkill, currentContext)

      if (!nextSkill) {
        break
      }

      // Check compatibility
      const compatibility = this.analyzer.analyze(currentSkill, nextSkill)
      if (!compatibility.compatible) {
        console.warn('Incompatible skills:', compatibility.issues)
        break
      }

      // Add connection
      connections.push({
        from: { skillId: currentSkill.id, output: currentSkill.outputs[0].name },
        to: { skillId: nextSkill.id, input: nextSkill.inputs[0].name },
      })

      chain.push(nextSkill)
      currentSkill = nextSkill

      // Check if task is complete
      if (this.isTaskComplete(task, chain)) {
        break
      }
    }

    return {
      id: `chain-${Date.now()}`,
      skills: chain,
      connections,
      inputSchema: chain[0].inputs,
      outputSchema: chain[chain.length - 1].outputs,
    }
  }

  private async findNextSkill(
    currentSkill: Skill,
    context: any
  ): Promise<Skill | null> {
    // Discover skills that can use current output
    const query = `Skills that can accept ${currentSkill.outputs[0].type} input`
    const matches = await this.discovery.discover(query)

    // Filter out already used skills
    const available = matches.filter(
      m => !context.usedSkills?.includes(m.skill.id)
    )

    return available.length > 0 ? available[0].skill : null
  }

  private extractContext(task: string): any {
    return {
      usedSkills: [],
    }
  }

  private isTaskComplete(task: string, chain: Skill[]): boolean {
    // Check if the chain can complete the task
    // (implementation depends on task analysis)
    return false
  }
}

// Usage
const chainer = new SkillChainer(discovery, analyzer)

const chain = await chainer.buildChain('Generate a REST API with authentication')
console.log('Skill chain:', chain)
```

### 4. Chain Execution

```typescript
class ChainExecutor {
  private registry: SkillRegistry

  constructor(registry: SkillRegistry) {
    this.registry = registry
  }

  async execute(chain: SkillChain, input: any): Promise<any> {
    let currentInput = input
    const results: any[] = []

    for (let i = 0; i < chain.skills.length; i++) {
      const skill = chain.skills[i]
      const result = await this.executeSkill(skill, currentInput)

      results.push({
        skillId: skill.id,
        result,
        timestamp: new Date(),
      })

      // Prepare input for next skill
      if (i < chain.skills.length - 1) {
        const connection = chain.connections.find(
          c => c.from.skillId === skill.id
        )
        if (connection) {
          currentInput = {
            [connection.to.input]: result[connection.from.output],
          }
        }
      }
    }

    return {
      results,
      finalResult: results[results.length - 1].result,
    }
  }

  private async executeSkill(skill: Skill, input: any): Promise<any> {
    // Execute skill (implementation depends on skill type)
    console.log(`Executing skill: ${skill.name}`)
    return {}
  }
}

// Usage
const executor = new ChainExecutor(registry)

const result = await executor.execute(chain, {
  task: 'Generate a REST API',
  language: 'typescript',
})
```

### 5. Failure Handling

```typescript
interface ChainExecutionResult {
  success: boolean
  results: any[]
  errors: Error[]
  fallbackUsed: boolean
}

class ResilientChainExecutor {
  private registry: SkillRegistry
  private fallbackSkills: Map<string, Skill[]> = new Map()

  constructor(registry: SkillRegistry) {
    this.registry = registry
  }

  registerFallback(skillId: string, fallback: Skill): void {
    if (!this.fallbackSkills.has(skillId)) {
      this.fallbackSkills.set(skillId, [])
    }
    this.fallbackSkills.get(skillId)!.push(fallback)
  }

  async execute(chain: SkillChain, input: any): Promise<ChainExecutionResult> {
    const results: any[] = []
    const errors: Error[] = []
    let fallbackUsed = false

    for (let i = 0; i < chain.skills.length; i++) {
      const skill = chain.skills[i]

      try {
        const result = await this.executeSkillWithRetry(skill, input)
        results.push({
          skillId: skill.id,
          result,
          timestamp: new Date(),
        })

        // Prepare input for next skill
        if (i < chain.skills.length - 1) {
          const connection = chain.connections.find(
            c => c.from.skillId === skill.id
          )
          if (connection) {
            input = {
              [connection.to.input]: result[connection.from.output],
            }
          }
        }
      } catch (error) {
        console.error(`Skill ${skill.id} failed:`, error)
        errors.push(error as Error)

        // Try fallback
        const fallbacks = this.fallbackSkills.get(skill.id)
        if (fallbacks && fallbacks.length > 0) {
          console.log(`Trying fallback for ${skill.id}`)
          fallbackUsed = true

          for (const fallback of fallbacks) {
            try {
              const result = await this.executeSkillWithRetry(fallback, input)
              results.push({
                skillId: skill.id,
                result,
                fallback: fallback.id,
                timestamp: new Date(),
              })
              break
            } catch (fallbackError) {
              console.error(`Fallback ${fallback.id} also failed:`, fallbackError)
            }
          }

          // If all fallbacks failed, continue with next skill
          if (i < chain.skills.length - 1) {
            const connection = chain.connections.find(
              c => c.from.skillId === skill.id
            )
            if (connection) {
              input = {
                [connection.to.input]: null, // Pass null to indicate failure
              }
            }
          }
        } else {
          // No fallback, stop execution
          return {
            success: false,
            results,
            errors,
            fallbackUsed,
          }
        }
      }
    }

    return {
      success: errors.length === 0,
      results,
      errors,
      fallbackUsed,
    }
  }

  private async executeSkillWithRetry(
    skill: Skill,
    input: any,
    maxRetries: number = 3
  ): Promise<any> {
    let lastError: Error | null = null

    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      try {
        return await this.executeSkill(skill, input)
      } catch (error) {
        lastError = error as Error
        if (attempt < maxRetries) {
          const delay = Math.pow(2, attempt) * 1000 // Exponential backoff
          await this.sleep(delay)
        }
      }
    }

    throw lastError
  }

  private async executeSkill(skill: Skill, input: any): Promise<any> {
    // Execute skill (implementation depends on skill type)
    return {}
  }

  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms))
  }
}

// Usage
const executor = new ResilientChainExecutor(registry)

// Register fallbacks
executor.registerFallback('skill-1', fallbackSkill1)
executor.registerFallback('skill-1', fallbackSkill2)

const result = await executor.execute(chain, input)
```

### 6. Chain Optimization

```typescript
interface OptimizationMetrics {
  executionTime: number
  resourceUsage: number
  cost: number
  quality: number
}

class ChainOptimizer {
  private executor: ChainExecutor

  constructor(executor: ChainExecutor) {
    this.executor = executor
  }

  async optimize(chain: SkillChain): Promise<SkillChain> {
    // Analyze current chain
    const metrics = await this.measureChain(chain)
    console.log('Current metrics:', metrics)

    // Try optimizations
    const optimizations = await this.generateOptimizations(chain)

    // Evaluate each optimization
    let bestChain = chain
    let bestScore = this.calculateScore(metrics)

    for (const optimization of optimizations) {
      const optimizedChain = await this.applyOptimization(chain, optimization)
      const optimizedMetrics = await this.measureChain(optimizedChain)
      const optimizedScore = this.calculateScore(optimizedMetrics)

      if (optimizedScore > bestScore) {
        bestChain = optimizedChain
        bestScore = optimizedScore
        console.log('Better chain found:', optimization)
      }
    }

    return bestChain
  }

  private async measureChain(chain: SkillChain): Promise<OptimizationMetrics> {
    const startTime = Date.now()

    // Execute chain with test input
    const result = await this.executor.execute(chain, {})

    const executionTime = Date.now() - startTime

    return {
      executionTime,
      resourceUsage: 0, // Measure actual resource usage
      cost: 0, // Calculate based on API costs
      quality: 1.0, // Evaluate output quality
    }
  }

  private calculateScore(metrics: OptimizationMetrics): number {
    // Weighted score
    return (
      (1 / metrics.executionTime) * 0.4 +
      (1 / metrics.resourceUsage) * 0.3 +
      (1 / metrics.cost) * 0.2 +
      metrics.quality * 0.1
    )
  }

  private async generateOptimizations(
    chain: SkillChain
  ): Promise<string[]> {
    const optimizations: string[] = []

    // Check for redundant skills
    for (let i = 0; i < chain.skills.length - 1; i++) {
      const skill = chain.skills[i]
      const nextSkill = chain.skills[i + 1]

      if (this.areSkillsEquivalent(skill, nextSkill)) {
        optimizations.push(`Remove redundant skill at index ${i}`)
      }
    }

    // Check for parallelizable skills
    const parallelGroups = this.findParallelizableSkills(chain)
    for (const group of parallelGroups) {
      optimizations.push(`Parallelize skills: ${group.join(', ')}`)
    }

    // Check for reorderable skills
    const reorderings = this.findReorderableSkills(chain)
    for (const reordering of reorderings) {
      optimizations.push(`Reorder skills: ${reordering.join(', ')}`)
    }

    return optimizations
  }

  private areSkillsEquivalent(skillA: Skill, skillB: Skill): boolean {
    // Check if skills produce similar outputs
    return skillA.outputs[0].type === skillB.outputs[0].type
  }

  private findParallelizableSkills(chain: SkillChain): string[][] {
    // Find skills that can be executed in parallel
    return []
  }

  private findReorderableSkills(chain: SkillChain): string[][] {
    // Find skills that can be reordered
    return []
  }

  private async applyOptimization(
    chain: SkillChain,
    optimization: string
  ): Promise<SkillChain> {
    // Apply optimization to chain
    // (implementation depends on optimization type)
    return chain
  }
}

// Usage
const optimizer = new ChainOptimizer(executor)

const optimizedChain = await optimizer.optimize(chain)
console.log('Optimized chain:', optimizedChain)
```

## Quick Start

```typescript
// 1. Set up discovery
const discovery = new SkillDiscovery(registry)

// 2. Find skills for task
const matches = await discovery.discover('Generate API')

// 3. Build chain
const chainer = new SkillChainer(discovery, analyzer)
const chain = await chainer.buildChain('Generate API with auth')

// 4. Execute chain
const executor = new ChainExecutor(registry)
const result = await executor.execute(chain, input)
```

## Production Checklist

- [ ] Skill discovery implemented
- [ ] Compatibility analysis working
- [ ] Chain building functional
- [ ] Chain execution reliable
- [ ] Failure handling in place
- [ ] Fallback mechanisms defined
- [ ] Chain optimization enabled
- [ ] Monitoring/logging configured

## Anti-patterns

1. **No compatibility check**: Chain skills โดยไม่ validate
2. **No fallback**: Skill failures ทำให้ chain หยุด
3. **Over-chaining**: Chain เกินไปจน inefficient
4. **No optimization**: Execute chain โดยไม่ optimize
5. **Ignoring context**: ไม่ใช้ context จาก skills ก่อนหน้า

## Integration Points

- Skill registry
- Monitoring systems
- Logging frameworks
- Alerting systems
- Feedback loops

## Further Reading

- [Chain of Thought Prompting](https://arxiv.org/abs/2201.11903)
- [ReAct: Synergizing Reasoning and Acting](https://arxiv.org/abs/2210.03629)
- [Toolformer: Language Models Can Teach Themselves to Use Tools](https://arxiv.org/abs/2302.04761)
- [HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in Hugging Face](https://arxiv.org/abs/2303.17580)
