---
name: State Machines with XState
description: Implementing robust state management using finite state machines and statecharts with XState.
---

# State Machines with XState

## Overview

XState is a state management library that allows you to model your application logic as finite state machines and statecharts. It provides predictable state management, visualization tools, and excellent TypeScript support.

## Finite State Machines (FSM) Fundamentals

### What is a State Machine?

A state machine is a mathematical model of computation. It consists of:

1. **States**: Distinct modes the system can be in
2. **Events**: Inputs that trigger transitions
3. **Transitions**: Changes from one state to another
4. **Initial State**: The starting state
5. **Final States**: States that terminate the machine

### Simple Example

```typescript
// A simple toggle state machine
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
});
```

### State Diagram

```
┌─────────────┐
│  inactive  │◄───┐
└──────┬──────┘    │
       │            │ TOGGLE
       │ TOGGLE     │
       ▼            │
┌─────────────┐    │
│   active    │────┘
└─────────────┘
```

## Statecharts and Hierarchical States

### Hierarchical States

States can be nested, allowing for more complex state modeling.

```typescript
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
});
```

### Statechart Diagram

```
┌─────────────────────────────┐
│       loggedOut            │
└──────┬──────────────────────┘
       │ LOGIN
       ▼
┌─────────────────────────────┐
│       loggedIn             │
│  ┌──────────────────────┐ │
│  │  idle   ◄─────────┤ │
│  └───┬──────────────┘ │
│      │ FETCH_USER        │
│      ▼                  │
│  ┌──────────────────────┐ │
│  │ fetching            │ │
│  └───┬──────────────┘ │
│      │ SUCCESS          │
│      ▼                  │
│  ┌──────────────────────┐ │
│  │ idle               │ │
│  └───┬──────────────┘ │
│      │ FAILURE          │
│      ▼                  │
│  ┌──────────────────────┐ │
│  │ error              │ │
│  └───┬──────────────┘ │
│      │ RETRY           │
│      ▼                  │
│  ┌──────────────────────┐ │
│  │ fetching            │ │
│  └──────────────────────┘ │
│      │ LOGOUT           │
│      └───────────────────┘ │
└─────────────────────────────┘
```

## XState Core Concepts

### States

States represent the different conditions or modes your application can be in.

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
});
```

### Events

Events trigger transitions between states.

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
});
```

### Transitions

Transitions define how the machine moves from one state to another.

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
});
```

### Actions (Entry, Exit, Transition)

Actions are side effects that occur during state transitions.

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
});
```

### Guards (Conditional Transitions)

Guards are conditions that must be true for a transition to occur.

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
});
```

### Context (Extended State)

Context holds data that persists across state changes.

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
});
```

## Parallel States

Parallel states allow multiple regions to be active simultaneously.

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
});
```

## History States

History states allow returning to a previous state.

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
});

// Using history to go back
const service = interpret(machine).start();
service.send({ type: 'BACK' });  // Goes to previous step
```

## Delayed Transitions

Transitions can be delayed using `after`.

```typescript
const notificationMachine = createMachine({
  id: 'notification',
  initial: 'hidden',
  states: {
    hidden: {
      on: {
        SHOW: 'visible',
      },
    },
    visible: {
      after: {
        5000: 'hidden',  // Auto-hide after 5 seconds
      },
      on: {
        DISMISS: 'hidden',
      },
    },
  },
});
```

## Invoking Services and Actors

### Invoking Services

Services are asynchronous operations that can be invoked from states.

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
      const response = await fetch('/api/data');
      return await response.json();
    },
  },
});
```

### Actor Model in XState

Actors are independent state machines that can communicate with each other.

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
});

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
});
```

## XState with React (@xstate/react)

### Installation

```bash
npm install xstate @xstate/react
```

### useMachine Hook

```typescript
import { useMachine } from '@xstate/react';
import { toggleMachine } from './machines/toggleMachine';

function ToggleButton() {
  const [state, send] = useMachine(toggleMachine);
  
  return (
    <button
      onClick={() => send({ type: 'TOGGLE' })}
      className={state.matches('active') ? 'active' : 'inactive'}
    >
      {state.matches('active') ? 'ON' : 'OFF'}
    </button>
  );
}
```

### useActor Hook

```typescript
import { useActor } from '@xstate/react';

function ParentComponent() {
  const [state, send] = useMachine(parentMachine);
  const childActorRef = useActor(state.context.childRef);
  const [childState] = useActor(childActorRef);
  
  return (
    <div>
      <p>Child state: {childState.value}</p>
      <button onClick={() => send({ type: 'START_CHILD' })}>
        Start Child
      </button>
    </div>
  );
}
```

### useService Hook

```typescript
import { useService } from '@xstate/react';

function DataComponent() {
  const [state, send] = useMachine(fetchMachine);
  const service = useService(state.context.serviceRef);
  
  return (
    <div>
      {state.matches('loading') && <p>Loading...</p>}
      {state.matches('success') && (
        <div>
          <pre>{JSON.stringify(state.context.data, null, 2)}</pre>
          <button onClick={() => send({ type: 'RESET' })}>
            Reset
          </button>
        </div>
      )}
      {state.matches('failure') && (
        <div>
          <p>Error: {state.context.error?.message}</p>
          <button onClick={() => send({ type: 'RETRY' })}>
            Retry
          </button>
        </div>
      )}
    </div>
  );
}
```

### useSelector Hook

```typescript
import { useSelector } from '@xstate/react';

function Counter() {
  const [state, send] = useMachine(counterMachine);
  const count = useSelector(state, state => state.context.count);
  const canIncrement = useSelector(state, state => state.matches('idle'));
  
  return (
    <div>
      <p>Count: {count}</p>
      <button
        onClick={() => send({ type: 'INCREMENT' })}
        disabled={!canIncrement}
      >
        Increment
      </button>
      <button onClick={() => send({ type: 'RESET' })}>
        Reset
      </button>
    </div>
  );
}
```

## XState with Vue, Svelte

### Vue Integration

```typescript
import { useMachine } from '@xstate/vue';
import { toggleMachine } from './machines/toggleMachine';

export default {
  setup() {
    const { state, send } = useMachine(toggleMachine);
    
    return {
      state,
      send,
    };
  },
  template: `
    <button
      @click="send({ type: 'TOGGLE' })"
      :class="{ active: state.matches('active') }"
    >
      {{ state.matches('active') ? 'ON' : 'OFF' }}
    </button>
  `,
};
```

### Svelte Integration

```typescript
import { useMachine } from '@xstate/svelte';
import { toggleMachine } from './machines/toggleMachine';

function ToggleButton() {
  const { state, send } = useMachine(toggleMachine);
  
  return (
    <button
      on:click={() => send({ type: 'TOGGLE' })}
      class={state.matches('active') ? 'active' : 'inactive'}
    >
      {state.matches('active') ? 'ON' : 'OFF'}
    </button>
  );
}
```

## Visualizing Machines (Stately Editor)

### Exporting for Stately

```typescript
import { createMachine } from 'xstate';

const machine = createMachine({
  id: 'trafficLight',
  initial: 'red',
  states: {
    red: {
      on: { TIMER: 'yellow' },
    },
    yellow: {
      on: { TIMER: 'green' },
    },
    green: {
      on: { TIMER: 'red' },
    },
  },
});

// Export for Stately Editor
export const machineDefinition = JSON.stringify(machine.definition, null, 2);
```

### Using Stately Editor

1. Go to [https://stately.ai/editor](https://stately.ai/editor)
2. Import your machine definition
3. Visualize and edit the statechart
4. Export back to TypeScript

## Testing State Machines

### Unit Testing

```typescript
import { createMachine } from 'xstate';
import { counterMachine } from './counterMachine';

describe('Counter Machine', () => {
  it('should start at idle state', () => {
    const service = interpret(counterMachine).start();
    expect(service.getSnapshot().value).toBe('idle');
  });
  
  it('should increment count on INCREMENT event', () => {
    const service = interpret(counterMachine).start();
    service.send({ type: 'INCREMENT' });
    expect(service.getSnapshot().context.count).toBe(1);
  });
  
  it('should not increment beyond max', () => {
    const service = interpret(counterMachine).start();
    
    // Increment to max
    for (let i = 0; i < 10; i++) {
      service.send({ type: 'INCREMENT' });
    }
    
    expect(service.getSnapshot().value).toBe('maxed');
    expect(service.getSnapshot().context.count).toBe(10);
  });
});
```

### Testing with React Testing Library

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { Counter } from './Counter';

describe('Counter Component', () => {
  it('should render count', () => {
    render(<Counter />);
    expect(screen.getByText('Count: 0')).toBeInTheDocument();
  });
  
  it('should increment on button click', () => {
    render(<Counter />);
    const button = screen.getByText('Increment');
    fireEvent.click(button);
    expect(screen.getByText('Count: 1')).toBeInTheDocument();
  });
});
```

## TypeScript Integration

### Type-Safe Machines

```typescript
import { createMachine, assign } from 'xstate';

interface AppContext {
  user: User | null;
  error: Error | null;
  isLoading: boolean;
}

type AppEvent = 
  | { type: 'LOGIN'; username: string; password: string }
  | { type: 'LOGOUT' }
  | { type: 'FETCH_USER' }
  | { type: 'FETCH_SUCCESS'; user: User }
  | { type: 'FETCH_ERROR'; error: Error };

const appMachine = createMachine<AppContext, AppEvent>({
  id: 'app',
  initial: 'idle',
  context: {
    user: null,
    error: null,
    isLoading: false,
  },
  states: {
    idle: {
      on: {
        LOGIN: 'authenticating',
        FETCH_USER: 'fetching',
      },
    },
    authenticating: {
      entry: assign({
        isLoading: true,
        error: null,
      }),
      invoke: {
        src: 'authenticate',
        onDone: {
          target: 'authenticated',
          actions: assign({
            user: (context, event) => event.data,
            isLoading: false,
          }),
        },
        onError: {
          target: 'idle',
          actions: assign({
            error: (context, event) => event.data,
            isLoading: false,
          }),
        },
      },
    },
    authenticated: {
      on: {
        LOGOUT: 'idle',
      },
    },
    fetching: {
      entry: assign({
        isLoading: true,
        error: null,
      }),
      invoke: {
        src: 'fetchUser',
        onDone: {
          target: 'idle',
          actions: assign({
            user: (context, event) => event.data,
            isLoading: false,
          }),
        },
        onError: {
          target: 'idle',
          actions: assign({
            error: (context, event) => event.data,
            isLoading: false,
          }),
        },
      },
    },
  },
  services: {
    authenticate: async (context, event) => {
      if (event.type !== 'LOGIN') return null;
      const response = await fetch('/api/auth', {
        method: 'POST',
        body: JSON.stringify({
          username: event.username,
          password: event.password,
        }),
      });
      return await response.json();
    },
    fetchUser: async () => {
      const response = await fetch('/api/user');
      return await response.json();
    },
  },
});
```

## Common Patterns

### Form Validation Machine

```typescript
interface FormContext {
  values: Record<string, any>;
  errors: Record<string, string>;
  touched: Record<string, boolean>;
  isValid: boolean;
}

const formMachine = createMachine<FormContext>({
  id: 'form',
  initial: 'idle',
  context: {
    values: {},
    errors: {},
    touched: {},
    isValid: false,
  },
  states: {
    idle: {
      on: {
        FOCUS: 'editing',
      },
    },
    editing: {
      on: {
        CHANGE: {
          actions: ['updateValue', 'validateField'],
        },
        BLUR: {
          actions: ['markTouched', 'validateField'],
        },
        SUBMIT: {
          target: 'submitting',
          actions: 'validateAll',
        },
      },
    },
    submitting: {
      invoke: {
        src: 'submitForm',
        onDone: {
          target: 'success',
        },
        onError: {
          target: 'editing',
          actions: 'showErrors',
        },
      },
    },
    success: {
      on: {
        RESET: 'idle',
        actions: 'resetForm',
      },
    },
  },
  actions: {
    updateValue: assign({
      values: (context, event) => ({
        ...context.values,
        [event.field]: event.value,
      }),
    }),
    markTouched: assign({
      touched: (context, event) => ({
        ...context.touched,
        [event.field]: true,
      }),
    }),
    validateField: assign({
      errors: (context, event) => {
        const error = validateField(event.field, event.value);
        return {
          ...context.errors,
          [event.field]: error,
        };
      },
      isValid: (context) => {
        return Object.values(context.errors).every(e => !e);
      },
    }),
    validateAll: assign({
      errors: (context) => {
        const errors = {};
        for (const field in context.values) {
          errors[field] = validateField(field, context.values[field]);
        }
        return errors;
      },
      isValid: (context) => {
        return Object.values(context.errors).every(e => !e);
      },
    }),
    showErrors: assign({
      errors: (context, event) => event.data,
    }),
    resetForm: assign({
      values: {},
      errors: {},
      touched: {},
      isValid: false,
    }),
  },
});
```

### Async Data Fetching Machine

```typescript
interface DataContext {
  data: any[] | null;
  error: Error | null;
  page: number;
  hasMore: boolean;
}

const dataMachine = createMachine<DataContext>({
  id: 'data',
  initial: 'idle',
  context: {
    data: null,
    error: null,
    page: 1,
    hasMore: true,
  },
  states: {
    idle: {
      on: {
        LOAD: 'loading',
      },
    },
    loading: {
      invoke: {
        src: 'fetchData',
        onDone: {
          target: 'loaded',
          actions: assign({
            data: (context, event) => {
              const existing = context.data || [];
              return [...existing, ...event.data];
            },
            hasMore: (context, event) => event.hasMore,
          }),
        },
        onError: {
          target: 'error',
          actions: assign({
            error: (context, event) => event.data,
          }),
        },
      },
    },
    loaded: {
      on: {
        LOAD_MORE: 'loadingMore',
        REFRESH: 'loading',
      },
    },
    loadingMore: {
      entry: assign({
        page: (context) => context.page + 1,
      }),
      invoke: {
        src: 'fetchMoreData',
        onDone: {
          target: 'loaded',
          actions: assign({
            data: (context, event) => {
              const existing = context.data || [];
              return [...existing, ...event.data];
            },
            hasMore: (context, event) => event.hasMore,
          }),
        },
        onError: {
          target: 'loaded',
          actions: assign({
            error: (context, event) => event.data,
          }),
        },
      },
    },
    error: {
      on: {
        RETRY: 'loading',
        RESET: 'idle',
      },
    },
  },
  services: {
    fetchData: async (context) => {
      const response = await fetch(`/api/data?page=${context.page}`);
      const result = await response.json();
      return {
        data: result.items,
        hasMore: result.hasMore,
      };
    },
    fetchMoreData: async (context) => {
      const response = await fetch(`/api/data?page=${context.page}`);
      const result = await response.json();
      return {
        data: result.items,
        hasMore: result.hasMore,
      };
    },
  },
});
```

### Multi-Step Wizard Machine

```typescript
interface WizardContext {
  step: number;
  data: Record<string, any>;
  errors: Record<string, string>;
}

const wizardMachine = createMachine<WizardContext>({
  id: 'wizard',
  initial: 'step1',
  context: {
    step: 1,
    data: {},
    errors: {},
  },
  states: {
    step1: {
      on: {
        NEXT: {
          target: 'step2',
          actions: ['validateStep1', 'saveStep1'],
          guard: 'step1Valid',
        },
      },
    },
    step2: {
      on: {
        NEXT: {
          target: 'step3',
          actions: ['validateStep2', 'saveStep2'],
          guard: 'step2Valid',
        },
        PREV: 'step1',
      },
    },
    step3: {
      on: {
        NEXT: {
          target: 'step4',
          actions: ['validateStep3', 'saveStep3'],
          guard: 'step3Valid',
        },
        PREV: 'step2',
      },
    },
    step4: {
      on: {
        FINISH: {
          target: 'complete',
          actions: ['validateStep4', 'submitWizard'],
          guard: 'step4Valid',
        },
        PREV: 'step3',
      },
    },
    complete: {
      on: {
        RESET: 'step1',
        actions: 'resetWizard',
      },
    },
  },
  actions: {
    validateStep1: assign({
      errors: (context) => ({
        ...context.errors,
        ...validateStep1(context.data),
      }),
    }),
    saveStep1: assign({
      data: (context, event) => ({
        ...context.data,
        ...event.data,
      }),
    }),
    validateStep2: assign({
      errors: (context) => ({
        ...context.errors,
        ...validateStep2(context.data),
      }),
    }),
    saveStep2: assign({
      data: (context, event) => ({
        ...context.data,
        ...event.data,
      }),
    }),
    validateStep3: assign({
      errors: (context) => ({
        ...context.errors,
        ...validateStep3(context.data),
      }),
    }),
    saveStep3: assign({
      data: (context, event) => ({
        ...context.data,
        ...event.data,
      }),
    }),
    validateStep4: assign({
      errors: (context) => ({
        ...context.errors,
        ...validateStep4(context.data),
      }),
    }),
    submitWizard: async () => {
      await fetch('/api/wizard', {
        method: 'POST',
        body: JSON.stringify(context.data),
      });
    },
    resetWizard: assign({
      data: {},
      errors: {},
      step: 1,
    }),
  },
  guards: {
    step1Valid: (context) => !hasErrors(context.errors, 1),
    step2Valid: (context) => !hasErrors(context.errors, 2),
    step3Valid: (context) => !hasErrors(context.errors, 3),
    step4Valid: (context) => !hasErrors(context.errors, 4),
  },
});
```

### Authentication Flow Machine

```typescript
interface AuthContext {
  user: User | null;
  token: string | null;
  error: Error | null;
}

const authMachine = createMachine<AuthContext>({
  id: 'auth',
  initial: 'unauthenticated',
  context: {
    user: null,
    token: null,
    error: null,
  },
  states: {
    unauthenticated: {
      on: {
        LOGIN: 'authenticating',
        REGISTER: 'registering',
      },
    },
    authenticating: {
      invoke: {
        src: 'login',
        onDone: {
          target: 'authenticated',
          actions: assign({
            user: (context, event) => event.data.user,
            token: (context, event) => event.data.token,
            error: null,
          }),
        },
        onError: {
          target: 'unauthenticated',
          actions: assign({
            error: (context, event) => event.data,
          }),
        },
      },
    },
    registering: {
      invoke: {
        src: 'register',
        onDone: {
          target: 'authenticated',
          actions: assign({
            user: (context, event) => event.data.user,
            token: (context, event) => event.data.token,
            error: null,
          }),
        },
        onError: {
          target: 'unauthenticated',
          actions: assign({
            error: (context, event) => event.data,
          }),
        },
      },
    },
    authenticated: {
      on: {
        LOGOUT: 'unauthenticated',
        actions: assign({
          user: null,
          token: null,
        }),
      },
    },
  },
  services: {
    login: async (context, event) => {
      if (event.type !== 'LOGIN') return null;
      const response = await fetch('/api/login', {
        method: 'POST',
        body: JSON.stringify({
          username: event.username,
          password: event.password,
        }),
      });
      return await response.json();
    },
    register: async (context, event) => {
      if (event.type !== 'REGISTER') return null;
      const response = await fetch('/api/register', {
        method: 'POST',
        body: JSON.stringify({
          username: event.username,
          email: event.email,
          password: event.password,
        }),
      });
      return await response.json();
    },
  },
});
```

### UI Component States Machine

```typescript
interface UIContext {
  isOpen: boolean;
  isLoading: boolean;
  hasError: boolean;
  error: Error | null;
}

const uiMachine = createMachine<UIContext>({
  id: 'ui',
  initial: 'closed',
  context: {
    isOpen: false,
    isLoading: false,
    hasError: false,
    error: null,
  },
  states: {
    closed: {
      on: {
        OPEN: 'opening',
      },
    },
    opening: {
      invoke: {
        src: 'loadData',
        onDone: {
          target: 'open',
          actions: assign({
            isOpen: true,
            isLoading: false,
          }),
        },
        onError: {
          target: 'error',
          actions: assign({
            hasError: true,
            error: (context, event) => event.data,
          }),
        },
      },
    },
    open: {
      on: {
        CLOSE: 'closed',
        actions: assign({
          isOpen: false,
        }),
      },
    },
    error: {
      on: {
        RETRY: 'opening',
        CLOSE: 'closed',
        actions: assign({
          hasError: false,
          error: null,
        }),
      },
    },
  },
  services: {
    loadData: async () => {
      const response = await fetch('/api/data');
      return await response.json();
    },
  },
});
```

## When to Use State Machines vs Other Solutions

### Use State Machines When:

- **Complex State Logic**: Multiple states with complex transitions
- **Side Effects**: Need to manage side effects (API calls, timers)
- **Predictable Behavior**: Need predictable, testable state management
- **Visualization**: Want to visualize state flow
- **Type Safety**: Need strong TypeScript support

### Use Other Solutions When:

- **Simple State**: Just a few boolean flags
- **Local Component State**: State doesn't need to be shared
- **Performance Critical**: Need maximum performance (Redux might be faster)
- **Team Familiarity**: Team is more familiar with other solutions

### Comparison

| Feature | XState | Redux | Zustand | Context API |
|----------|---------|---------|-------------|
| **Learning Curve** | Medium | Low | Very Low | Low |
| **Type Safety** | Excellent | Good | Good | Basic |
| **DevTools** | Excellent | Good | Good | Basic |
| **Visualization** | Excellent | None | None | None |
| **Boilerplate** | Medium | Low | Very Low | None |
| **Async Handling** | Built-in | Middleware | Middleware | Manual |
| **Testability** | Excellent | Good | Good | Good |

## Migration from useState/useReducer

### From useState

```typescript
// Before: useState
function Counter() {
  const [count, setCount] = useState(0);
  
  return (
    <div>
      <p>{count}</p>
      <button onClick={() => setCount(c => c + 1)}>+</button>
      <button onClick={() => setCount(c => c - 1)}>-</button>
    </div>
  );
}

// After: XState
const counterMachine = createMachine({
  id: 'counter',
  initial: 'idle',
  context: { count: 0 },
  states: {
    idle: {
      on: {
        INCREMENT: { actions: assign({ count: ctx => ctx.count + 1 }) },
        DECREMENT: { actions: assign({ count: ctx => ctx.count - 1 }) },
      },
    },
  },
});

function Counter() {
  const [state, send] = useMachine(counterMachine);
  
  return (
    <div>
      <p>{state.context.count}</p>
      <button onClick={() => send({ type: 'INCREMENT' })}>+</button>
      <button onClick={() => send({ type: 'DECREMENT' })}>-</button>
    </div>
  );
}
```

### From useReducer

```typescript
// Before: useReducer
interface State {
  count: number;
  step: number;
}

type Action = 
  | { type: 'INCREMENT' }
  | { type: 'DECREMENT' }
  | { type: 'SET_STEP'; step: number };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'INCREMENT':
      return { ...state, count: state.count + 1 };
    case 'DECREMENT':
      return { ...state, count: state.count - 1 };
    case 'SET_STEP':
      return { ...state, step: action.step };
    default:
      return state;
  }
}

function Counter() {
  const [state, dispatch] = useReducer(reducer, { count: 0, step: 1 });
  
  return (
    <div>
      <p>Count: {state.count}</p>
      <p>Step: {state.step}</p>
      <button onClick={() => dispatch({ type: 'INCREMENT' })}>+</button>
      <button onClick={() => dispatch({ type: 'DECREMENT' })}>-</button>
      <button onClick={() => dispatch({ type: 'SET_STEP', step: 2 })}>
        Set Step 2
      </button>
    </div>
  );
}

// After: XState
const counterMachine = createMachine({
  id: 'counter',
  initial: 'step1',
  context: { count: 0 },
  states: {
    step1: {
      on: {
        INCREMENT: { actions: assign({ count: ctx => ctx.count + 1 }) },
        DECREMENT: { actions: assign({ count: ctx => ctx.count - 1 }) },
        SET_STEP_2: 'step2',
      },
    },
    step2: {
      on: {
        INCREMENT: { actions: assign({ count: ctx => ctx.count + 1 }) },
        DECREMENT: { actions: assign({ count: ctx => ctx.count - 1 }) },
        SET_STEP_1: 'step1',
      },
    },
  },
});

function Counter() {
  const [state, send] = useMachine(counterMachine);
  
  return (
    <div>
      <p>Count: {state.context.count}</p>
      <p>Step: {state.value}</p>
      <button onClick={() => send({ type: 'INCREMENT' })}>+</button>
      <button onClick={() => send({ type: 'DECREMENT' })}>-</button>
      <button onClick={() => send({ type: 'SET_STEP_2' })}>
        Set Step 2
      </button>
    </div>
  );
}
```

## Best Practices

1. **Machine Design**
   - Keep machines focused and single-purpose
   - Use hierarchical states for complex logic
   - Define clear event names
   - Use TypeScript for type safety

2. **State Management**
   - Use context for data that persists across states
   - Use guards for conditional transitions
   - Use actions for side effects
   - Keep actions pure when possible

3. **Testing**
   - Test machines independently
   - Test state transitions
   - Test guards and actions
   - Test services/mocked services

4. **Visualization**
   - Use Stately Editor for visualization
   - Document state flow
   - Share diagrams with team

5. **Performance**
   - Avoid unnecessary re-renders
   - Use memo for expensive computations
   - Optimize service calls

## Related Skills

- `02-frontend/react-patterns`
- `02-frontend/state-management`
