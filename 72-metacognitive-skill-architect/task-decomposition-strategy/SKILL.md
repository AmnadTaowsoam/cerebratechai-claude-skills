---
name: Task Decomposition Strategy
description: Break down complex tasks into manageable subtasks: task analysis, dependency mapping, parallel execution planning, and subtask coordination
---

# Task Decomposition Strategy

## Overview

Task decomposition strategy คือการแยกงานที่ซับซ้อนออกเป็น subtasks ที่จัดการได้ รวมถึง task analysis, dependency mapping, parallel execution planning, และ subtask coordination

## Why This Matters

- **Manageability**: งานใหญ่แยกเป็นส่วนเล็กๆ จัดการง่ายขึ้น
- **Parallelism**: Subtasks ที่ไม่ dependent กันสามารถ execute พร้อมกันได้
- **Progress Tracking**: Track progress ได้ละเอียดกว่า
- **Error Isolation**: Failures ใน subtask ไม่กระทบทั้งงาน

---

## Core Concepts

### 1. Task Analysis

```typescript
interface Task {
  id: string
  description: string
  type: 'simple' | 'complex' | 'compound'
  priority: 'low' | 'medium' | 'high' | 'critical'
  estimatedDuration: number
  dependencies: string[]
  subtasks: Task[]
}

interface TaskAnalysis {
  complexity: number
  estimatedSubtasks: number
  suggestedDecomposition: string[]
  riskFactors: string[]
}

class TaskAnalyzer {
  analyze(task: string): TaskAnalysis {
    const complexity = this.assessComplexity(task)
    const estimatedSubtasks = this.estimateSubtasks(task, complexity)
    const suggestedDecomposition = this.suggestDecomposition(task)
    const riskFactors = this.identifyRisks(task)

    return {
      complexity,
      estimatedSubtasks,
      suggestedDecomposition,
      riskFactors,
    }
  }

  private assessComplexity(task: string): number {
    let complexity = 1

    // Length
    if (task.length > 100) complexity += 1
    if (task.length > 500) complexity += 1

    // Number of clauses
    const clauses = task.split(/[.,;!?]/).filter(c => c.trim())
    if (clauses.length > 5) complexity += 1
    if (clauses.length > 10) complexity += 1

    // Keywords indicating complexity
    const complexityKeywords = [
      'and then', 'after that', 'also', 'additionally',
      'create and', 'build and', 'implement and',
    ]
    for (const keyword of complexityKeywords) {
      if (task.toLowerCase().includes(keyword)) {
        complexity += 1
      }
    }

    // Multiple requirements
    const requirements = task.match(/require|need|must|should/gi) || []
    if (requirements.length > 3) complexity += 1

    return Math.min(5, complexity)
  }

  private estimateSubtasks(task: string, complexity: number): number {
    // Estimate based on complexity
    const baseSubtasks = Math.max(2, Math.floor(complexity * 1.5))

    // Adjust for specific patterns
    if (task.toLowerCase().includes('and')) {
      return baseSubtasks + 1
    }

    return baseSubtasks
  }

  private suggestDecomposition(task: string): string[] {
    const suggestions: string[] = []

    // Identify action verbs
    const actions = this.extractActions(task)
    if (actions.length > 1) {
      suggestions.push(`Split into separate actions: ${actions.join(', ')}`)
    }

    // Identify and/or conditions
    if (task.toLowerCase().includes(' and ')) {
      const parts = task.split(/ and /i)
      suggestions.push(`Separate into: ${parts.join(' + ')}`)
    }

    // Identify sequential requirements
    if (task.toLowerCase().includes('then') || task.toLowerCase().includes('after')) {
      suggestions.push('Identify sequential dependencies')
    }

    // Identify conditional requirements
    if (task.toLowerCase().includes('if') || task.toLowerCase().includes('when')) {
      suggestions.push('Handle conditional logic separately')
    }

    return suggestions
  }

  private identifyRisks(task: string): string[] {
    const risks: string[] = []

    // Ambiguous requirements
    if (task.toLowerCase().includes('maybe') || task.toLowerCase().includes('possibly')) {
      risks.push('Ambiguous requirements detected')
    }

    // Conflicting requirements
    const positives = task.match(/(must|should|need|require)/gi) || []
    const negatives = task.match(/(must not|should not|shouldn't|don't)/gi) || []
    if (positives.length > 0 && negatives.length > 0) {
      risks.push('Potential conflicting requirements')
    }

    // Overly broad requirements
    if (task.toLowerCase().includes('everything') || task.toLowerCase().includes('all')) {
      risks.push('Overly broad scope may cause issues')
    }

    return risks
  }

  private extractActions(task: string): string[] {
    const actionVerbs = [
      'create', 'build', 'implement', 'develop', 'design',
      'test', 'deploy', 'configure', 'setup', 'install',
      'update', 'modify', 'refactor', 'optimize',
    ]

    const actions: string[] = []
    const lowerTask = task.toLowerCase()

    for (const verb of actionVerbs) {
      if (lowerTask.includes(verb)) {
        actions.push(verb)
      }
    }

    return actions
  }
}

// Usage
const analyzer = new TaskAnalyzer()

const analysis = analyzer.analyze(
  'Create a REST API for user management with authentication, then add unit tests, and deploy to production'
)

console.log('Task analysis:', analysis)
```

### 2. Dependency Mapping

```typescript
interface DependencyGraph {
  nodes: Map<string, Task>
  edges: Map<string, string[]>
  levels: Task[][]
}

class DependencyMapper {
  buildGraph(tasks: Task[]): DependencyGraph {
    const nodes = new Map<string, Task>()
    const edges = new Map<string, string[]>()

    // Build nodes and edges
    for (const task of tasks) {
      nodes.set(task.id, task)
      edges.set(task.id, [...task.dependencies])
    }

    // Calculate levels (topological sort)
    const levels = this.calculateLevels(nodes, edges)

    return { nodes, edges, levels }
  }

  private calculateLevels(
    nodes: Map<string, Task>,
    edges: Map<string, string[]>
  ): Task[][] {
    const levels: Task[][] = []
    const visited = new Set<string>()
    const inProgress = new Set<string>()

    for (const [taskId] of nodes) {
      if (!visited.has(taskId)) {
        this.visit(taskId, nodes, edges, visited, inProgress, levels, 0)
      }
    }

    return levels
  }

  private visit(
    taskId: string,
    nodes: Map<string, Task>,
    edges: Map<string, string[]>,
    visited: Set<string>,
    inProgress: Set<string>,
    levels: Task[][],
    currentLevel: number
  ): void {
    if (inProgress.has(taskId)) {
      throw new Error(`Circular dependency detected: ${taskId}`)
    }

    if (visited.has(taskId)) {
      return
    }

    inProgress.add(taskId)

    const dependencies = edges.get(taskId) || []

    for (const depId of dependencies) {
      this.visit(depId, nodes, edges, visited, inProgress, levels, currentLevel + 1)
    }

    inProgress.delete(taskId)
    visited.add(taskId)

    const task = nodes.get(taskId)!
    while (levels.length <= currentLevel) {
      levels.push([])
    }
    levels[currentLevel].push(task)
  }

  findCriticalPath(graph: DependencyGraph): string[] {
    const longestPath: string[] = []
    const longestDuration: Map<string, number> = new Map()

    // Calculate longest path to each node
    for (const level of graph.levels) {
      for (const task of level) {
        const dependencies = graph.edges.get(task.id) || []
        let maxDuration = 0

        for (const depId of dependencies) {
          const depDuration = longestDuration.get(depId) || 0
          maxDuration = Math.max(maxDuration, depDuration)
        }

        longestDuration.set(task.id, maxDuration + task.estimatedDuration)
      }
    }

    // Find tasks on critical path
    let maxTotalDuration = 0
    for (const [taskId, duration] of longestDuration) {
      if (duration > maxTotalDuration) {
        maxTotalDuration = duration
      }
    }

    // Trace back from max duration task
    // (implementation depends on tracing logic)

    return longestPath
  }

  detectCircularDependencies(graph: DependencyGraph): string[] {
    const cycles: string[] = []
    const visited = new Set<string>()
    const recursionStack = new Set<string>()

    for (const [taskId] of graph.nodes) {
      if (!visited.has(taskId)) {
        this.detectCycles(taskId, graph, visited, recursionStack, cycles)
      }
    }

    return cycles
  }

  private detectCycles(
    taskId: string,
    graph: DependencyGraph,
    visited: Set<string>,
    recursionStack: Set<string>,
    cycles: string[]
  ): void {
    visited.add(taskId)
    recursionStack.add(taskId)

    const dependencies = graph.edges.get(taskId) || []

    for (const depId of dependencies) {
      if (!visited.has(depId)) {
        this.detectCycles(depId, graph, visited, recursionStack, cycles)
      } else if (recursionStack.has(depId)) {
        cycles.push(depId)
      }
    }

    recursionStack.delete(taskId)
  }
}

// Usage
const mapper = new DependencyMapper()

const tasks = [
  {
    id: 'task-1',
    description: 'Setup database',
    dependencies: [],
    estimatedDuration: 60,
  },
  {
    id: 'task-2',
    description: 'Create API endpoints',
    dependencies: ['task-1'],
    estimatedDuration: 120,
  },
  {
    id: 'task-3',
    description: 'Write tests',
    dependencies: ['task-2'],
    estimatedDuration: 90,
  },
]

const graph = mapper.buildGraph(tasks)
console.log('Dependency graph:', graph)

const criticalPath = mapper.findCriticalPath(graph)
console.log('Critical path:', criticalPath)
```

### 3. Parallel Execution Planning

```typescript
interface ExecutionPlan {
  sequentialStages: Task[][]
  parallelGroups: Task[][]
  estimatedDuration: number
}

class ParallelPlanner {
  plan(graph: DependencyGraph): ExecutionPlan {
    const sequentialStages: Task[][] = []
    const parallelGroups: Task[][] = []

    // Group by levels (already calculated in graph)
    for (const level of graph.levels) {
      if (level.length === 1) {
        sequentialStages.push(level)
      } else {
        parallelGroups.push(level)
      }
    }

    // Calculate estimated duration
    const estimatedDuration = this.calculateDuration(graph)

    return {
      sequentialStages,
      parallelGroups,
      estimatedDuration,
    }
  }

  private calculateDuration(graph: DependencyGraph): number {
    let totalDuration = 0

    for (const level of graph.levels) {
      if (level.length === 1) {
        // Sequential - add duration
        totalDuration += level[0].estimatedDuration
      } else {
        // Parallel - use max duration
        const maxDuration = Math.max(...level.map(t => t.estimatedDuration))
        totalDuration += maxDuration
      }
    }

    return totalDuration
  }

  optimizeForResources(
    graph: DependencyGraph,
    maxParallelTasks: number
  ): ExecutionPlan {
    const optimizedStages: Task[][] = []
    const currentStage: Task[] = []
    const inProgress = new Set<string>()

    for (const level of graph.levels) {
      for (const task of level) {
        // Check if dependencies are done
        const dependenciesDone = task.dependencies.every(
          dep => inProgress.has(dep)
        )

        if (dependenciesDone && currentStage.length < maxParallelTasks) {
          currentStage.push(task)
          inProgress.add(task.id)
        } else {
          // Start new stage
          if (currentStage.length > 0) {
            optimizedStages.push([...currentStage])
            currentStage.length = 0
          }

          // Wait for dependencies
          const remainingDeps = task.dependencies.filter(
            dep => !inProgress.has(dep)
          )

          if (remainingDeps.length === 0) {
            currentStage.push(task)
            inProgress.add(task.id)
          }
        }
      }
    }

    if (currentStage.length > 0) {
      optimizedStages.push(currentStage)
    }

    return {
      sequentialStages: optimizedStages,
      parallelGroups: [],
      estimatedDuration: this.calculateOptimizedDuration(optimizedStages),
    }
  }

  private calculateOptimizedDuration(stages: Task[][]): number {
    return stages.reduce((total, stage) => {
      const maxDuration = Math.max(...stage.map(t => t.estimatedDuration))
      return total + maxDuration
    }, 0)
  }
}

// Usage
const planner = new ParallelPlanner()

const plan = planner.plan(graph)
console.log('Execution plan:', plan)

const optimizedPlan = planner.optimizeForResources(graph, 3)
console.log('Optimized plan (max 3 parallel):', optimizedPlan)
```

### 4. Subtask Coordination

```typescript
interface SubtaskCoordinator {
  tasks: Map<string, Task>
  status: Map<string, TaskStatus>
  results: Map<string, any>
}

interface TaskStatus {
  state: 'pending' | 'running' | 'completed' | 'failed' | 'skipped'
  startTime?: Date
  endTime?: Date
  error?: Error
  retryCount: number
}

class SubtaskCoordinator {
  private coordinator: SubtaskCoordinator = {
    tasks: new Map(),
    status: new Map(),
    results: new Map(),
  }

  register(task: Task): void {
    this.coordinator.tasks.set(task.id, task)
    this.coordinator.status.set(task.id, {
      state: 'pending',
      retryCount: 0,
    })
  }

  async execute(
    executionPlan: ExecutionPlan,
    onProgress?: (taskId: string, status: TaskStatus) => void
  ): Promise<Map<string, any>> {
    // Execute sequential stages
    for (const stage of executionPlan.sequentialStages) {
      await this.executeStage(stage, onProgress)
    }

    // Execute parallel groups
    for (const group of executionPlan.parallelGroups) {
      await this.executeParallel(group, onProgress)
    }

    return this.coordinator.results
  }

  private async executeStage(
    tasks: Task[],
    onProgress?: (taskId: string, status: TaskStatus) => void
  ): Promise<void> {
    for (const task of tasks) {
      await this.executeTask(task, onProgress)
    }
  }

  private async executeParallel(
    tasks: Task[],
    onProgress?: (taskId: string, status: TaskStatus) => void
  ): Promise<void> {
    await Promise.all(
      tasks.map(task => this.executeTask(task, onProgress))
    )
  }

  private async executeTask(
    task: Task,
    onProgress?: (taskId: string, status: TaskStatus) => void
  ): Promise<void> {
    const status = this.coordinator.status.get(task.id)!

    // Update status to running
    status.state = 'running'
    status.startTime = new Date()
    if (onProgress) onProgress(task.id, { ...status })

    try {
      // Execute task
      const result = await this.executeTaskLogic(task)

      // Update status to completed
      status.state = 'completed'
      status.endTime = new Date()
      this.coordinator.results.set(task.id, result)

      if (onProgress) onProgress(task.id, { ...status })
    } catch (error) {
      // Update status to failed
      status.state = 'failed'
      status.endTime = new Date()
      status.error = error as Error

      if (onProgress) onProgress(task.id, { ...status })

      // Check if should retry
      if (status.retryCount < 3) {
        status.retryCount++
        console.log(`Retrying task ${task.id} (attempt ${status.retryCount})`)
        await this.sleep(1000 * status.retryCount) // Exponential backoff
        await this.executeTask(task, onProgress)
      }
    }
  }

  private async executeTaskLogic(task: Task): Promise<any> {
    // Execute task logic (implementation depends on task type)
    console.log(`Executing task: ${task.description}`)
    return {}
  }

  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms))
  }

  getProgress(): { total: number; completed: number; failed: number } {
    const total = this.coordinator.tasks.size
    const completed = Array.from(this.coordinator.status.values()).filter(
      s => s.state === 'completed'
    ).length
    const failed = Array.from(this.coordinator.status.values()).filter(
      s => s.state === 'failed'
    ).length

    return { total, completed, failed }
  }

  skipTask(taskId: string, reason: string): void {
    const status = this.coordinator.status.get(taskId)
    if (status) {
      status.state = 'skipped'
      console.log(`Task ${taskId} skipped: ${reason}`)
    }
  }
}

// Usage
const coordinator = new SubtaskCoordinator()

// Register tasks
for (const task of tasks) {
  coordinator.register(task)
}

// Execute with progress tracking
const results = await coordinator.execute(plan, (taskId, status) => {
  console.log(`Task ${taskId}: ${status.state}`)
  const progress = coordinator.getProgress()
  console.log(`Progress: ${progress.completed}/${progress.total}`)
})
```

### 5. Adaptive Decomposition

```typescript
interface AdaptiveDecomposition {
  initialPlan: ExecutionPlan
  adaptations: Adaptation[]
  finalPlan: ExecutionPlan
}

interface Adaptation {
  type: 'merge' | 'split' | 'reorder' | 'skip'
  taskId: string
  reason: string
  timestamp: Date
}

class AdaptiveDecomposer {
  private analyzer: TaskAnalyzer
  private mapper: DependencyMapper
  private planner: ParallelPlanner

  constructor() {
    this.analyzer = new TaskAnalyzer()
    this.mapper = new DependencyMapper()
    this.planner = new ParallelPlanner()
  }

  async decompose(task: string): Promise<AdaptiveDecomposition> {
    // Analyze task
    const analysis = this.analyzer.analyze(task)

    // Generate initial subtasks
    const subtasks = await this.generateSubtasks(task, analysis)

    // Build dependency graph
    const graph = this.mapper.buildGraph(subtasks)

    // Create initial plan
    const initialPlan = this.planner.plan(graph)

    return {
      initialPlan,
      adaptations: [],
      finalPlan: initialPlan,
    }
  }

  private async generateSubtasks(
    task: string,
    analysis: TaskAnalysis
  ): Promise<Task[]> {
    const subtasks: Task[] = []

    // Use LLM to generate subtasks
    const prompt = `Break down this task into subtasks:
Task: ${task}

Requirements:
- Generate ${analysis.estimatedSubtasks} subtasks
- Each subtask should be independently executable
- Identify dependencies between subtasks
- Estimate duration for each subtask (in minutes)

Return JSON array with: id, description, dependencies, estimatedDuration`

    const response = await llm.generate(prompt)
    const generatedTasks = JSON.parse(response)

    return generatedTasks.map((t: any, i: number) => ({
      id: `task-${i + 1}`,
      description: t.description,
      type: 'simple',
      priority: 'medium',
      estimatedDuration: t.estimatedDuration,
      dependencies: t.dependencies || [],
      subtasks: [],
    }))
  }

  async adapt(
    decomposition: AdaptiveDecomposition,
    executionStatus: Map<string, TaskStatus>
  ): Promise<AdaptiveDecomposition> {
    const adaptations: Adaptation[] = []

    // Check for failed tasks
    for (const [taskId, status] of executionStatus) {
      if (status.state === 'failed') {
        const adaptation = await this.handleFailure(taskId, status)
        adaptations.push(adaptation)
      }
    }

    // Check for slow tasks
    for (const [taskId, status] of executionStatus) {
      if (status.state === 'running') {
        const duration = Date.now() - status.startTime!.getTime()
        const task = decomposition.initialPlan.sequentialStages.flat().find(
          t => t.id === taskId
        )

        if (task && duration > task.estimatedDuration * 60000 * 2) {
          const adaptation = await this.handleSlowTask(taskId, duration)
          adaptations.push(adaptation)
        }
      }
    }

    // Rebuild plan with adaptations
    const adaptedPlan = await this.rebuildPlan(
      decomposition.initialPlan,
      adaptations
    )

    return {
      initialPlan: decomposition.initialPlan,
      adaptations,
      finalPlan: adaptedPlan,
    }
  }

  private async handleFailure(
    taskId: string,
    status: TaskStatus
  ): Promise<Adaptation> {
    // Analyze failure
    const prompt = `This task failed:
Task ID: ${taskId}
Error: ${status.error?.message}

Suggest an adaptation:
1. Should we retry? (if yes, suggest fix)
2. Should we skip? (if yes, what are the consequences?)
3. Should we split into smaller tasks? (if yes, suggest subtasks)

Return JSON with: type, taskId, reason`

    const response = await llm.generate(prompt)
    const suggestion = JSON.parse(response)

    return {
      type: suggestion.type,
      taskId,
      reason: suggestion.reason,
      timestamp: new Date(),
    }
  }

  private async handleSlowTask(
    taskId: string,
    duration: number
  ): Promise<Adaptation> {
    const prompt = `This task is taking too long:
Task ID: ${taskId}
Duration: ${duration}ms

Suggest an adaptation:
1. Should we skip and continue?
2. Should we split into smaller parallel tasks?

Return JSON with: type, taskId, reason`

    const response = await llm.generate(prompt)
    const suggestion = JSON.parse(response)

    return {
      type: suggestion.type,
      taskId,
      reason: suggestion.reason,
      timestamp: new Date(),
    }
  }

  private async rebuildPlan(
    initialPlan: ExecutionPlan,
    adaptations: Adaptation[]
  ): Promise<ExecutionPlan> {
    // Apply adaptations to plan
    // (implementation depends on adaptation types)

    return initialPlan
  }
}

// Usage
const decomposer = new AdaptiveDecomposer()

const decomposition = await decomposer.decompose(
  'Build a full-stack web application with authentication and database'
)

console.log('Initial plan:', decomposition.initialPlan)

// During execution, adapt based on status
const adapted = await decomposer.adapt(decomposition, executionStatus)
console.log('Adapted plan:', adapted.finalPlan)
```

## Quick Start

```typescript
// 1. Analyze task
const analyzer = new TaskAnalyzer()
const analysis = analyzer.analyze(task)

// 2. Generate subtasks
const subtasks = await generateSubtasks(task, analysis)

// 3. Build dependency graph
const mapper = new DependencyMapper()
const graph = mapper.buildGraph(subtasks)

// 4. Create execution plan
const planner = new ParallelPlanner()
const plan = planner.plan(graph)

// 5. Execute with coordinator
const coordinator = new SubtaskCoordinator()
for (const task of subtasks) {
  coordinator.register(task)
}

const results = await coordinator.execute(plan)
```

## Production Checklist

- [ ] Task analysis implemented
- [ ] Dependency mapping working
- [ ] Parallel planning functional
- [ ] Subtask coordination reliable
- [ ] Adaptive decomposition enabled
- [ ] Progress tracking in place
- [ ] Error handling configured
- [ ] Retry logic implemented

## Anti-patterns

1. **Over-decomposition**: แยกงานเล็กเกินไป
2. **No dependency tracking**: Execute tasks โดยไม่ check dependencies
3. **No parallelization**: Execute sequentially เมื่อสามารถ parallel ได้
4. **No adaptation**: ไม่ adapt plan เมื่อมี failures
5. **Ignoring progress**: ไม่ track progress หรือ report status

## Integration Points

- Task queues
- Monitoring systems
- Logging frameworks
- Alerting systems
- Feedback loops

## Further Reading

- [Task Decomposition in AI](https://arxiv.org/abs/2305.14314)
- [Chain of Thought Prompting](https://arxiv.org/abs/2201.11903)
- [Tree of Thoughts](https://arxiv.org/abs/2305.10601)
- [Task Planning](https://arxiv.org/abs/2306.05042)
