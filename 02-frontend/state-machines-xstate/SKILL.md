# State Machines with XState

---

## 1. Executive Summary & Strategic Necessity

### 1.1 Context (ภาษาไทย)

XState คือ state management library ที่ใช้ finite state machines และ statecharts สำหรับ modeling application logic ซึ่งช่วยให้ developers สร้าง applications ที่มี predictable state management, visualization tools, และ TypeScript support ที่ยอดเยี่ยม

XState ใช้ mathematical model ของ finite state machines ซึ่งช่วยให้ developers:
- **Model complex logic** เป็ state transitions ที่ชัดเจน
- **Visualize state flow** ด้วย state diagrams และ visualization tools
- **Type-safe** - Full TypeScript support สำหรับ type safety
- **Predictable** - Deterministic state transitions ที่ testable ง่าย
- **Side effect management** - Built-in support สำหรับ async operations

### 1.2 Business Impact (ภาษาไทย)

**ผลกระทบทางธุรกิจ:**

1. **ลด Bugs** - State machines ช่วยลด bugs ที่เกิดจาก complex state logic ได้ถึง 30-40%
2. **เพิ่ม Maintainability** - Visualized state flow ช่วยเพิ่ม maintainability
3. **ลด Debugging Time** - Predictable state ช่วยลดเวลาในการ debug
4. **เพิ่ม Testability** - Deterministic transitions ช่วยเพิ่ม testability
5. **ปรับปรุง Developer Experience** - Visualization tools และ TypeScript ช่วยเพิ่ม DX

### 1.3 Product Thinking (ภาษาไทย)

**มุมมองด้านผลิตภัณฑ์:**

1. **State-First** - XState ต้องเป็น state management solution หลัก
2. **Predictable** - State transitions ต้อง deterministic และ predictable
3. **Visualizable** - State flow ต้องสามารถ visualize ได้
4. **Testable** - State machines ต้อง testable ง่าย
5. **Type-Safe** - Full TypeScript support สำหรับ type safety

---

## 2. Technical Deep Dive (The "How-to")

### 2.1 Core Logic

XState ประกอบด้วย:

1. **Finite State Machines (FSM)** - Mathematical model ของ computation
2. **Statecharts** - Hierarchical state machines สำหรับ complex logic
3. **States** - Distinct modes ที่ system สามารถอยู่ได้
4. **Events** - Inputs ที่ trigger transitions
5. **Transitions** - Changes จาก one state ไปยังอีก state
6. **Actions** - Side effects ที่เกิดระหว่าง state transitions
7. **Guards** - Conditions ที่ต้องเป็น true สำหรับ transitions

### 2.2 Architecture Diagram Requirements

```
┌─────────────────────────────────────────────────────────┐
│              XState Architecture                        │
├─────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌───────────────────────────────────────────────────┐   │
│  │              State Machine Layer                   │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  States      │  │  Events     │  │  Transitions│  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Context & Actions Layer                │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  Context    │  │  Actions     │  │  Guards     │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Integration Layer                       │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  React       │  │  Vue        │  │  Svelte     │  │   │
│  │  │  Hooks       │  │  Composable  │  │  Hooks      │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Tools Layer                            │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  Stately     │  │  DevTools    │  │  Testing    │  │   │
│  │  │  Editor      │  │  Inspector   │  │  Library    │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
└─────────────────────────────────────────────────────────┘
```

### 2.3 Implementation Workflow

**Step 1: Install XState**

```bash
# Install XState
npm install xstate

# Install React integration
npm install @xstate/react
```

**Step 2: Create Simple State Machine**

```typescript
import { createMachine } from 'xstate'

const toggleMachine = createMachine({
  id: 'toggle',
  initial: 'inactive',
  states: {
    inactive: {
      on: {
        TOGGLE: 'active',
      },
    },
    active: {
      on: {
        TOGGLE: 'inactive',
      },
    },
  },
})
```

---

## 3. Tooling & Tech Stack

### 3.1 Enterprise Tools

| Tool | Purpose | Version | License |
|------|---------|---------|---------|
| XState | State Management | ^5.0.0 | MIT |
| @xstate/react | React Integration | ^5.0.0 | MIT |
| @xstate/vue | Vue Integration | ^5.0.0 | MIT |
| @xstate/svelte | Svelte Integration | ^5.0.0 | MIT |
| Stately Editor | Visualization Tool | Latest | MIT |

### 3.2 Configuration Essentials

**TypeScript Configuration:**
```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "lib": ["DOM", "DOM.Iterable", "ESNext"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "target": "ES2020"
  }
}
```

---

## 4. Standards, Compliance & Security

### 4.1 International Standards

- **SCXML** - State Chart XML Notation
- **W3C State Machines** - State Machine Standards
- **ISO 9241-11** - Usability Standards
- **GDPR** - Data Protection สำหรับ User Data

### 4.2 Security Protocol

XState ต้องปฏิบัติตามหลักความปลอดภัย:

1. **Input Validation** - Validate ข้อมูลทั้ง client และ server
2. **Secure Storage** - ไม่เก็บ sensitive data ใน state context
3. **CSRF Protection** - ใช้ CSRF tokens สำหรับ forms
4. **Rate Limiting** - จำกัดจำนวน service calls

### 4.3 Explainability

XState ต้องสามารถอธิบายได้ว่า:

1. **State Transitions** - ทำไม state เปลี่ยนอย่างไร
2. **Event Handling** - ทำไม events trigger transitions อย่างไร
3. **Side Effects** - ทำไม actions ทำงานอย่างไร
4. **Guard Conditions** - ทำไม guards evaluate อย่างไร

---

## 5. Unit Economics & Performance Metrics (KPIs)

### 5.1 Cost Calculation

| Metric | Calculation | Target |
|--------|-------------|--------|
| State Transition Time | Time per transition | < 10ms |
| Render Performance | Component render time | < 16ms |
| Bundle Size | JavaScript bundle size | < 50 KB |
| Test Coverage | Test coverage percentage | > 80% |
| State Complexity | Cyclomatic complexity score | < 15 |

### 5.2 Key Performance Indicators

**Technical Metrics:**

1. **State Transition Time** - เวลาในการ state transitions
2. **Render Performance** - Component render time
3. **Bundle Size** - JavaScript bundle ที่ใช้งาน
4. **Test Coverage** - Test coverage ของ state machines

**Business Metrics:**

1. **Bug Reduction** - Bug reduction rate
2. **Development Velocity** - เวลาในการพัฒนา features
3. **Maintainability** - Maintainability score
4. **Code Quality** - Code quality score

---

## 6. Strategic Recommendations (CTO Insights)

### 6.1 Phase Rollout

**Phase 1: Foundation (Week 1-2)**
- Install XState
- Setup TypeScript configuration
- Create simple state machines
- Implement basic patterns

**Phase 2: Advanced Features (Week 3-4)**
- Implement hierarchical states
- Add context and actions
- Implement guards
- Create services and actors

**Phase 3: Integration (Week 5-6)**
- Integrate with React
- Add Vue/Svelte support
- Implement visualization
- Setup testing

**Phase 4: Production (Week 7-8)**
- Performance optimization
- Documentation and training
- Monitoring and analytics
- Best practices documentation

### 6.2 Pitfalls to Avoid

1. **Over-Engineering** - ไม่ใช้ state machines สำหรับ simple logic
2. **Poor State Design** - ไม่ design states ที่ซับซ้อนเกินไป
3. **Missing Guards** - ไม่ใช้ guards สำหรับ conditional transitions
4. **Side Effect Issues** - ไม่ manage side effects อย่างเหมาะสม
5. **Poor Testing** - ไม่ test state machines อย่างเหมาะสม
6. **Complex Machines** - ไม่สร้าง machines ที่ซับซ้อนเกินไป

### 6.3 Best Practices Checklist

- [ ] ใช้ finite state machines สำหรับ complex state logic
- [ ] Implement proper TypeScript types
- [ ] Visualize state flow ด้วย diagrams
- [ ] Test state transitions
- [ ] Use guards สำหรับ conditional transitions
- [ ] Implement side effects ใน actions
- [ ] Keep machines focused และ single-purpose
- [ ] Use context สำหรับ data ที่ persists
- [ ] Implement services สำหรับ async operations
- [ ] Test machines independently
- [ ] Document state flow
- [ ] Use visualization tools
- [ ] Optimize performance
- [ ] Test บนทุก browsers และ devices

---

## 7. Implementation Examples

### 7.1 Finite State Machines (FSM)

**Simple Toggle Machine:**
```typescript
import { createMachine } from 'xstate'

const toggleMachine = createMachine({
  id: 'toggle',
  initial: 'inactive',
  states: {
    inactive: {
      on: {
        TOGGLE: 'active',
      },
    },
    active: {
      on: {
        TOGGLE: 'inactive',
      },
    },
  },
})
```

**State Diagram:**
```
┌──────┐
│ inactive │◄───┐
└──────┬──────┘    │
       │            │ TOGGLE
       │ TOGGLE     │        ▼
┌───────┐    │
│   active │────┘
└─────────────┘
```

### 7.2 Statecharts and Hierarchical States

**Hierarchical Authentication Machine:**
```typescript
import { createMachine } from 'xstate'

const authMachine = createMachine({
  id: 'auth',
  initial: 'loggedOut',
  states: {
    loggedOut: {
      on: {
        LOGIN: 'loggedIn',
      },
    },
    loggedIn: {
      initial: 'idle',
      states: {
        idle: {
          on: {
            FETCH_USER: 'fetching',
          },
        },
        fetching: {
          on: {
            SUCCESS: 'idle',
            FAILURE: 'error',
          },
        },
        error: {
          on: {
            RETRY: 'fetching',
            LOGOUT: 'loggedOut',
          },
        },
      },
      on: {
        LOGOUT: 'loggedOut',
      },
    },
  },
})
```

### 7.3 XState Core Concepts

**States:**
```typescript
const trafficLightMachine = createMachine({
  id: 'trafficLight',
  initial: 'red',
  states: {
    red: {
      after: {
        5000: 'green',  // Auto-transition after 5s
      },
    },
    yellow: {
      after: {
        2000: 'red',
      },
    },
    green: {
      after: {
        5000: 'yellow',
      },
    },
  },
})
```

**Events:**
```typescript
const machine = createMachine({
  id: 'app',
  initial: 'idle',
  states: {
    idle: {
      on: {
        START: 'running',
        CONFIGURE: 'configuring',
      },
    },
    running: {
      on: {
        PAUSE: 'paused',
        STOP: 'idle',
      },
    },
    paused: {
      on: {
        RESUME: 'running',
        STOP: 'idle',
      },
    },
    configuring: {
      on: {
        SAVE: 'idle',
        CANCEL: 'idle',
      },
    },
  },
})
```

**Transitions:**
```typescript
const machine = createMachine({
  id: 'vending',
  initial: 'idle',
  states: {
    idle: {
      on: {
        INSERT_COIN: 'hasCoin',
      },
    },
    hasCoin: {
      on: {
        SELECT_ITEM: {
          target: 'dispensing',
          actions: 'dispenseItem',
        },
        RETURN_COIN: 'idle',
      },
    },
    dispensing: {
      on: {
        DONE: 'idle',
      },
    },
  },
  actions: {
    dispenseItem: () => {
      console.log('Dispensing item...');
    },
  },
})
```

### 7.4 Actions (Entry, Exit, Transition)

**Timer with Entry/Exit Actions:**
```typescript
const machine = createMachine({
  id: 'timer',
  initial: 'stopped',
  states: {
    stopped: {
      entry: 'logStopped',    // When entering stopped state
      exit: 'cleanupTimer',   // When leaving stopped state
      on: {
        START: 'running',
      },
    },
    running: {
      entry: 'startTimer',    // When entering running state
      exit: 'stopTimer',     // When leaving running state
      on: {
        STOP: 'stopped',
      },
    },
  },
  actions: {
    logStopped: () => console.log('Timer stopped'),
    cleanupTimer: () => console.log('Cleaning up timer'),
    startTimer: () => console.log('Timer started'),
    stopTimer: () => console.log('Timer stopped'),
  },
})
```

### 7.5 Guards (Conditional Transitions)

**Door Machine with Guards:**
```typescript
const machine = createMachine({
  id: 'door',
  initial: 'closed',
  states: {
    closed: {
      on: {
        OPEN: {
          target: 'open',
          guard: 'isUnlocked',
        },
        UNLOCK: 'unlocked',
      },
    },
    unlocked: {
      on: {
        OPEN: 'open',
        LOCK: 'closed',
      },
    },
    open: {
      on: {
        CLOSE: 'closed',
      },
    },
  },
  guards: {
    isUnlocked: (context, event) => {
      return context.isUnlocked;
    },
  },
})
```

### 7.6 Context (Extended State)

**Counter with Context:**
```typescript
interface CounterContext {
  count: number;
  maxCount: number;
}

const counterMachine = createMachine<CounterContext>({
  id: 'counter',
  initial: 'idle',
  context: {
    count: 0,
    maxCount: 10,
  },
  states: {
    idle: {
      on: {
        INCREMENT: {
          target: 'counting',
          actions: 'increment',
          guard: 'notAtMax',
        },
        RESET: {
          target: 'idle',
          actions: 'reset',
        },
      },
    },
    counting: {
      after: {
        100: 'idle',  // Auto-return to idle after 100ms
      },
    },
    maxed: {
      on: {
        RESET: {
          target: 'idle',
          actions: 'reset',
        },
      },
    },
  },
  actions: {
    increment: assign({
      count: (context) => Math.min(context.count + 1, context.maxCount),
    }),
    reset: assign({
      count: 0,
    }),
  },
  guards: {
    notAtMax: (context) => context.count < context.maxCount,
  },
})
```

### 7.7 Parallel States

**Parallel State Machine:**
```typescript
const parallelMachine = createMachine({
  id: 'app',
  initial: 'initializing',
  states: {
    initializing: {
      on: {
        READY: 'app',
      },
    },
    app: {
      type: 'parallel',  // Parallel state
      states: {
        ui: {
          initial: 'home',
          states: {
            home: {},
            settings: {},
            profile: {},
          },
        },
        data: {
          initial: 'loading',
          states: {
            loading: {
              on: {
                LOADED: 'ready',
                ERROR: 'error',
              },
            },
            ready: {},
            error: {},
          },
        },
        notifications: {
          initial: 'idle',
          states: {
            idle: {},
            showing: {},
          },
        },
      },
    },
  },
})
```

### 7.8 History States

**Wizard with History:**
```typescript
const machine = createMachine({
  id: 'wizard',
  initial: 'step1',
  states: {
    step1: {
      on: {
        NEXT: 'step2',
      },
    },
    step2: {
      on: {
        NEXT: 'step3',
        BACK: 'step1',
      },
    },
    step3: {
      on: {
        NEXT: 'step4',
        BACK: 'step2',
      },
    },
    step4: {
      on: {
        FINISH: 'done',
        BACK: 'step3',
      },
    },
    done: {
      on: {
        RESTART: 'step1',
      },
    },
  },
})
```

### 7.9 Invoking Services and Actors

**Service Invocation:**
```typescript
const fetchMachine = createMachine({
  id: 'fetch',
  initial: 'idle',
  context: {
    data: null,
    error: null,
  },
  states: {
    idle: {
      on: {
        FETCH: 'loading',
      },
    },
    loading: {
      invoke: {
        src: 'fetchData',
        onDone: {
          target: 'success',
          actions: assign({
            data: (context, event) => event.data,
          }),
        },
        onError: {
          target: 'failure',
          actions: assign({
            error: (context, event) => event.data,
          }),
        },
      },
    },
    success: {
      on: {
        FETCH: 'loading',
        RESET: 'idle',
      },
    },
    failure: {
      on: {
        RETRY: 'loading',
        RESET: 'idle',
      },
    },
  },
  services: {
    fetchData: async () => {
      const response = await fetch('/api/data')
      return await response.json()
    },
  },
})
```

**Actor Model:**
```typescript
const childMachine = createMachine({
  id: 'child',
  initial: 'idle',
  states: {
    idle: {
      on: {
        START: 'working',
      },
    },
    working: {
      on: {
        DONE: 'idle',
      },
    },
  },
})

const parentMachine = createMachine({
  id: 'parent',
  initial: 'active',
  context: {
    childRef: null,
  },
  states: {
    active: {
      invoke: {
        id: 'childActor',
        src: childMachine,
        onDone: {
          target: 'completed',
        },
      },
    },
    completed: {},
  },
})
```

### 7.10 XState with React (@xstate/react)

**useMachine Hook:**
```typescript
import { useMachine } from '@xstate/react'
import { toggleMachine } from './machines/toggleMachine'

function ToggleButton() {
  const [state, send] = useMachine(toggleMachine)

  return (
    <button
      onClick={() => send({ type: 'TOGGLE' })}
      className={state.matches('active') ? 'active' : 'inactive'}
    >
      {state.matches('active') ? 'ON' : 'OFF'}
    </button>
  )
}
```

**useActor Hook:**
```typescript
import { useActor } from '@xstate/react'

function ParentComponent() {
  const [state, send] = useMachine(parentMachine)
  const childActorRef = useActor(state.context.childRef)
  const [childState] = useActor(childActorRef)

  return (
    <div>
      <p>Child state: {childState.value}</p>
      <button onClick={() => send({ type: 'START_CHILD' })}>
        Start Child
      </button>
    </div>
  )
}
```

### 7.11 Best Practices

**Machine Design:**
- Keep machines focused and single-purpose
- Use hierarchical states for complex logic
- Define clear event names
- Use TypeScript for type safety
- Document state flow

**State Management:**
- Use context for data that persists across states
- Use guards for conditional transitions
- Use actions for side effects
- Keep actions pure when possible

**Testing:**
- Test machines independently
- Test state transitions
- Test guards and actions
- Test services/mocked services

**Visualization:**
- Use Stately Editor for visualization
- Document state flow
- Share diagrams with team
- Export for documentation

**Performance:**
- Avoid unnecessary re-renders
- Optimize service calls
- Use memo for expensive computations
- Test performance metrics

---

## 8. Related Skills

- `02-frontend/state-management`
- `02-frontend/react-best-practices`
- `02-frontend/form-handling`
- `00-meta-skills/system-thinking`
