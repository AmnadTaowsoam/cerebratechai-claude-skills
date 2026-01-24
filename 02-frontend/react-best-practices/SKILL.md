# React Best Practices and Patterns

---

## 1. Executive Summary & Strategic Necessity

### 1.1 Context (ภาษาไทย)

React คือ JavaScript library สำหรับการสร้าง user interfaces ที่ใช้ component-based architecture และ virtual DOM สำหรับ performance ที่ดี React มี hooks สำหรับ state management และ side effects ซึ่งช่วยให้การจัดการ logic ที่ซับซ้อนง่ายขึ้น

React 18+ มี features ที่สำคัญ เช่น:
- **Functional Components** - Components แบบ functional ที่ใช้ hooks
- **Custom Hooks** - Reusable logic ที่แยกออกจาก components
- **Context API** - State management ที่ global
- **Suspense** - Async rendering และ loading states
- **Concurrent Features** - Improved performance ด้วย concurrent rendering

### 1.2 Business Impact (ภาษาไทย)

**ผลกระทบทางธุรกิจ:**

1. **ลด Development Time** - Component reuse และ hooks ช่วยลดเวลาพัฒนา
2. **เพิ่ม Maintainability** - Code ที่ organized ช่วยลด maintenance cost
3. **เพิ่ม Performance** - Virtual DOM และ optimization ช่วยเพิ่ม performance
4. **เพิ่ม User Experience** - Fast rendering และ smooth interactions
5. **ปรับปรุง Code Quality** - TypeScript และ patterns ช่วยเพิ่ม code quality

### 1.3 Product Thinking (ภาษาไทย)

**มุมมองด้านผลิตภัณฑ์:**

1. **Component-First** - React components ต้อง reusable และ composable
2. **State Management** - State ต้องจัดการอย่างเหมาะสม
3. **Performance-First** - React ต้องไม่ส่งผลกระทบต่อ performance
4. **Accessibility-First** - Components ต้องเข้าถึงได้และใช้งานได้สำหรับผู้ใช้ทุกคน
5. **Testable** - Components ต้อง testable ง่าย

---

## 2. Technical Deep Dive (The "How-to")

### 2.1 Core Logic

React ประกอบด้วย:

1. **Component Architecture** - Functional components ที่ใช้ hooks
2. **State Management** - useState, useReducer, Context API
3. **Side Effects** - useEffect สำหรับ side effects
4. **Performance Optimization** - useMemo, useCallback, React.memo
5. **Custom Hooks** - Reusable logic
6. **Composition Patterns** - Component composition สำหรับ reusability
7. **Error Boundaries** - Error handling สำหรับ React components

### 2.2 Architecture Diagram Requirements

```
┌─────────────────────────────────────────────────────────┐
│              React Architecture                       │
├─────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Component Layer                       │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  Functional │  │  Class      │  │  Custom    │  │   │
│  │  │  Components│  │  Components│  │  Hooks     │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
│  ┌───────────────────────────────────────────────────┐   │
│  │              State Management Layer                 │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  useState   │  │  useReducer │  │  Context   │  │   │
│  │  │  Hook      │  │  Hook       │  │  API       │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  External   │  │  Server     │  │  Optimized │  │   │
│  │  │  State      │  │  State      │  │  State     │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Effect Layer                          │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  useEffect   │  │  useLayout │  │  useInsert  │  │   │
│  │  │  Hook       │  │  Effect     │  │  Effect    │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Performance Layer                    │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  useMemo     │  │  useCallback │  │  React.memo│  │   │
│  │  │  Hook       │  │  Hook       │  │  HOC       │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Rendering Layer                       │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  Virtual    │  │  Fiber      │  │  Concurrent │  │   │
│  │  │  DOM        │  │  Architecture│  │  Rendering │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
└─────────────────────────────────────────────────────────┘
```

### 2.3 Implementation Workflow

**Step 1: Create Functional Component**

```typescript
// Simple presentational component
type ButtonProps = {
  children: React.ReactNode
  onClick?: () => void
  variant?: 'primary' | 'secondary'
  disabled?: boolean
}

export function Button({ 
  children, 
  onClick, 
  variant = 'primary',
  disabled = false 
}: ButtonProps) {
  const baseStyles = 'px-4 py-2 rounded font-medium transition-colors'
  const variantStyles = {
    primary: 'bg-blue-500 text-white hover:bg-blue-600',
    secondary: 'bg-gray-200 text-gray-800 hover:bg-gray-300'
  }
  
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`${baseStyles} ${variantStyles[variant]} ${
        disabled ? 'opacity-50 cursor-not-allowed' : ''
      }`}
    >
      {children}
    </button>
  )
}
```

---

## 3. Tooling & Tech Stack

### 3.1 Enterprise Tools

| Tool | Purpose | Version | License |
|------|---------|---------|---------|
| React | UI Library | ^18.0.0 | MIT |
| TypeScript | Type Safety | ^5.0.0 | Apache 2.0 |
| @testing-library/react | Testing | ^14.0.0 | MIT |
| react-error-boundary | Error Handling | ^4.0.0 | MIT |
| react-window | Virtualization | ^1.8.0 | MIT |

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

- **WCAG 2.1 Level AA** - Components ต้องเข้าถึงได้และใช้งานได้สำหรับผู้ใช้ทุกคน
- **ISO 9241-11** - Usability Standards สำหรับ UI Components
- **GDPR** - Data Protection สำหรับ User Data

### 4.2 Security Protocol

React ต้องปฏิบัติตามหลักความปลอดภัย:

1. **XSS Prevention** - React escapes content โดย default
2. **Input Validation** - Validate ข้อมูลทั้ง client และ server
3. **Secure Storage** - ไม่เก็บ sensitive data ใน localStorage
4. **CSRF Protection** - ใช้ CSRF tokens สำหรับ forms

```typescript
// Secure form handling
function SecureForm() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
  })
  
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    // Sanitize input if needed
    const sanitized = value.replace(/[<>]/g, '')
    setFormData(prev => ({ ...prev, [name]: sanitized }))
  }
  
  return (
    <form>
      <input
        name="name"
        value={formData.name}
        onChange={handleChange}
      />
    </form>
  )
}
```

### 4.3 Explainability

React ต้องสามารถอธิบายได้ว่า:

1. **Component Behavior** - ทำไม component render อย่างไร
2. **State Changes** - ทำไม state เปลี่ยน
3. **Effect Execution** - ทำไม effect ทำงาน
4. **Performance** - ทำไม re-render เกิดขึ้น

---

## 5. Unit Economics & Performance Metrics (KPIs)

### 5.1 Cost Calculation

| Metric | Calculation | Target |
|--------|-------------|--------|
| Component Render Time | Time per component render | < 16ms |
| Re-render Count | Number of re-renders | < 5/interaction |
| Bundle Size | JavaScript bundle size | < 300 KB |
| Time to Interactive | Interactive time | < 3.8s |
| Accessibility Score | WCAG compliance score | > 95% |

### 5.2 Key Performance Indicators

**Technical Metrics:**

1. **Component Render Time** - เวลาในการ render components
2. **Re-render Count** - จำนวน re-renders
3. **Bundle Size** - JavaScript bundle ที่ใช้งาน
4. **Memory Usage** - Memory ที่ใช้งาน

**Business Metrics:**

1. **Development Velocity** - เวลาในการพัฒนา features
2. **Code Quality** - Code quality score
3. **User Experience** - User experience score
4. **Accessibility Compliance** - Accessibility compliance rate

---

## 6. Strategic Recommendations (CTO Insights)

### 6.1 Phase Rollout

**Phase 1: Foundation (Week 1-2)**
- Setup React project
- Configure TypeScript and ESLint
- Create base components
- Implement component patterns

**Phase 2: State Management (Week 3-4)**
- Implement useState patterns
- Add useReducer for complex state
- Create Context API setup
- Implement custom hooks

**Phase 3: Performance (Week 5-6)**
- Add performance optimization
- Implement React.memo
- Add useMemo and useCallback
- Create virtualization for lists

**Phase 4: Production (Week 7-8)**
- Add error boundaries
- Implement accessibility
- Testing setup
- Documentation and training

### 6.2 Pitfalls to Avoid

1. **Mutating State Directly** - ไม่ mutate state โดยตรง
2. **Missing Dependencies** - ไม่ลืม dependencies ใน useEffect
3. **Over-optimization** - ไม่ optimize เกินไป
4. **Poor Component Design** - ไม่ design components ให้ reusable
5. **Ignoring Accessibility** - ไม่คำนึงถึง accessibility
6. **Complex State** - ไม่ใช้ state ที่ซับซ้อนเกินไป

### 6.3 Best Practices Checklist

- [ ] ใช้ functional components โดย default
- [ ] Implement custom hooks สำหรับ reusable logic
- [ ] ใช้ Context API สำหรับ global state
- [ ] Implement performance optimization ด้วย useMemo/useCallback
- [ ] ใช้ React.memo สำหรับ expensive components
- [ ] Implement error boundaries สำหรับ error handling
- [ ] คำนึงถึง accessibility ในทุก components
- [ ] Test components ด้วย React Testing Library
- [ ] ใช้ TypeScript สำหรับ type safety
- [ ] Implement proper cleanup ใน useEffect
- [ ] ใช้ composition patterns สำหรับ reusable components
- [ ] Avoid anti-patterns ใน React
- [ ] Implement proper form handling
- [ ] ใช้ virtualization สำหรับ long lists
- [ ] Monitor performance metrics

---

## 7. Implementation Examples

### 7.1 Component Patterns

**Functional Components:**
```typescript
// Simple presentational component
type ButtonProps = {
  children: React.ReactNode
  onClick?: () => void
  variant?: 'primary' | 'secondary'
  disabled?: boolean
}

export function Button({ 
  children, 
  onClick, 
  variant = 'primary',
  disabled = false 
}: ButtonProps) {
  const baseStyles = 'px-4 py-2 rounded font-medium transition-colors'
  const variantStyles = {
    primary: 'bg-blue-500 text-white hover:bg-blue-600',
    secondary: 'bg-gray-200 text-gray-800 hover:bg-gray-300'
  }
  
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`${baseStyles} ${variantStyles[variant]} ${
        disabled ? 'opacity-50 cursor-not-allowed' : ''
      }`}
    >
      {children}
    </button>
  )
}
```

**Custom Hooks:**
```typescript
// useLocalStorage.ts - Persist state to localStorage
import { useState, useEffect } from 'react'

function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    if (typeof window === 'undefined') return initialValue
    
    try {
      const item = window.localStorage.getItem(key)
      return item ? JSON.parse(item) : initialValue
    } catch (error) {
      console.error(error)
      return initialValue
    }
  })
  
  const setValue = (value: T | ((val: T) => T)) => {
    try {
      const valueToStore = value instanceof Function 
        ? value(storedValue) 
        : value
      
      setStoredValue(valueToStore)
      
      if (typeof window !== 'undefined') {
        window.localStorage.setItem(key, JSON.stringify(valueToStore))
      }
    } catch (error) {
      console.error(error)
    }
  }
  
  return [storedValue, setValue] as const
}

// Usage
function ThemeToggle() {
  const [theme, setTheme] = useLocalStorage('theme', 'light')
  
  return (
    <button onClick={() => setTheme(t => t === 'light' ? 'dark' : 'light')}>
      Current theme: {theme}
    </button>
  )
}
```

**Composition Patterns:**
```typescript
// Card component with composition
type CardProps = {
  children: React.ReactNode
  className?: string
}

function Card({ children, className = '' }: CardProps) {
  return (
    <div className={`bg-white rounded-lg shadow-md ${className}`}>
      {children}
    </div>
  )
}

function CardHeader({ children }: { children: React.ReactNode }) {
  return (
    <div className="px-6 py-4 border-b">
      {children}
    </div>
  )
}

function CardTitle({ children }: { children: React.ReactNode }) {
  return (
    <h3 className="text-lg font-semibold">
      {children}
    </h3>
  )
}

function CardBody({ children }: { children: React.ReactNode }) {
  return (
    <div className="px-6 py-4">
      {children}
    </div>
  )
}

function CardFooter({ children }: { children: React.ReactNode }) {
  return (
    <div className="px-6 py-4 bg-gray-50 rounded-b-lg">
      {children}
    </div>
  )
}

// Usage
<Card>
  <CardHeader>
    <CardTitle>User Profile</CardTitle>
  </CardHeader>
  <CardBody>
    <p>User information goes here...</p>
  </CardBody>
  <CardFooter>
    <Button>Save Changes</Button>
  </CardFooter>
</Card>
```

**Compound Components Pattern:**
```typescript
// Tabs.tsx
import { createContext, useContext, useState, ReactNode } from 'react'

type TabsContextValue = {
  activeTab: string
  setActiveTab: (tab: string) => void
}

const TabsContext = createContext<TabsContextValue | undefined>(undefined)

function useTabsContext() {
  const context = useContext(TabsContext)
  if (!context) {
    throw new Error('Tabs components must be used within Tabs provider')
  }
  return context
}

type TabsProps = {
  children: ReactNode
  defaultTab: string
}

function Tabs({ children, defaultTab }: TabsProps) {
  const [activeTab, setActiveTab] = useState(defaultTab)
  
  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      {children}
    </TabsContext.Provider>
  )
}

function TabList({ children }: { children: ReactNode }) {
  return <div className="flex border-b">{children}</div>
}

type TabProps = {
  value: string
  children: ReactNode
}

function Tab({ value, children }: TabProps) {
  const { activeTab, setActiveTab } = useTabsContext()
  const isActive = activeTab === value
  
  return (
    <button
      onClick={() => setActiveTab(value)}
      className={`px-4 py-2 border-b-2 transition-colors ${
        isActive 
          ? 'border-blue-500 text-blue-500' 
          : 'border-transparent text-gray-500 hover:text-gray-700'
      }`}
    >
      {children}
    </button>
  )
}

function TabPanels({ children }: { children: ReactNode }) {
  return <div className="mt-4">{children}</div>
}

type TabPanelProps = {
  value: string
  children: ReactNode
}

function TabPanel({ value, children }: TabPanelProps) {
  const { activeTab } = useTabsContext()
  
  if (activeTab !== value) return null
  
  return <div>{children}</div>
}

// Usage
<Tabs defaultTab="profile">
  <TabList>
    <Tab value="profile">Profile</Tab>
    <Tab value="settings">Settings</Tab>
    <Tab value="notifications">Notifications</Tab>
  </TabList>
  <TabPanels>
    <TabPanel value="profile">Profile content...</TabPanel>
    <TabPanel value="settings">Settings content...</TabPanel>
    <TabPanel value="notifications">Notifications content...</TabPanel>
  </TabPanels>
</Tabs>
```

### 7.2 State Management

**useState Pattern:**
```typescript
// Simple state
function Counter() {
  const [count, setCount] = useState(0)
  
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(c => c + 1)}>Increment</button>
    </div>
  )
}

// State with object
function UserForm() {
  const [user, setUser] = useState({
    name: '',
    email: '',
    age: 0
  })
  
  const handleChange = (field: keyof typeof user) => (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    setUser(prev => ({ ...prev, [field]: e.target.value }))
  }
  
  return (
    <form>
      <input
        value={user.name}
        onChange={handleChange('name')}
        placeholder="Name"
      />
      <input
        value={user.email}
        onChange={handleChange('email')}
        placeholder="Email"
      />
    </form>
  )
}
```

**useReducer Pattern:**
```typescript
// Complex state with reducer
type State = {
  todos: Array<{ id: number; text: string; completed: boolean }>
  filter: 'all' | 'active' | 'completed'
}

type Action =
  | { type: 'ADD_TODO'; text: string }
  | { type: 'TOGGLE_TODO'; id: number }
  | { type: 'DELETE_TODO'; id: number }
  | { type: 'SET_FILTER'; filter: State['filter'] }

function todoReducer(state: State, action: Action): State {
  switch (action.type) {
    case 'ADD_TODO':
      return {
        ...state,
        todos: [
          ...state.todos,
          {
            id: Date.now(),
            text: action.text,
            completed: false
          }
        ]
      }
    case 'TOGGLE_TODO':
      return {
        ...state,
        todos: state.todos.map(todo =>
          todo.id === action.id
            ? { ...todo, completed: !todo.completed }
            : todo
        )
      }
    case 'DELETE_TODO':
      return {
        ...state,
        todos: state.todos.filter(todo => todo.id !== action.id)
      }
    case 'SET_FILTER':
      return { ...state, filter: action.filter }
    default:
      return state
  }
}

function TodoApp() {
  const [state, dispatch] = useReducer(todoReducer, {
    todos: [],
    filter: 'all'
  })
  
  const [input, setInput] = useState('')
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (input.trim()) {
      dispatch({ type: 'ADD_TODO', text: input.trim() })
      setInput('')
    }
  }
  
  const filteredTodos = state.todos.filter(todo => {
    if (state.filter === 'active') return !todo.completed
    if (state.filter === 'completed') return todo.completed
    return true
  })
  
  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Add a todo..."
        />
        <button type="submit">Add</button>
      </form>
      
      <div>
        <button onClick={() => dispatch({ type: 'SET_FILTER', filter: 'all' })}>
          All
        </button>
        <button onClick={() => dispatch({ type: 'SET_FILTER', filter: 'active' })}>
          Active
        </button>
        <button onClick={() => dispatch({ type: 'SET_FILTER', filter: 'completed' })}>
          Completed
        </button>
      </div>
      
      <ul>
        {filteredTodos.map(todo => (
          <li key={todo.id}>
            <input
              type="checkbox"
              checked={todo.completed}
              onChange={() => dispatch({ type: 'TOGGLE_TODO', id: todo.id })}
            />
            <span style={{ textDecoration: todo.completed ? 'line-through' : 'none' }}>
              {todo.text}
            </span>
            <button onClick={() => dispatch({ type: 'DELETE_TODO', id: todo.id })}>
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}
```

**Context API Usage:**
```typescript
// ThemeContext.tsx
import { createContext, useContext, useState, ReactNode } from 'react'

type Theme = 'light' | 'dark'

type ThemeContextValue = {
  theme: Theme
  toggleTheme: () => void
}

const ThemeContext = createContext<ThemeContextValue | undefined>(undefined)

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<Theme>('light')
  
  const toggleTheme = () => {
    setTheme(t => (t === 'light' ? 'dark' : 'light'))
  }
  
  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      <div className={theme}>{children}</div>
    </ThemeContext.Provider>
  )
}

export function useTheme() {
  const context = useContext(ThemeContext)
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider')
  }
  return context
}

// Usage
function App() {
  return (
    <ThemeProvider>
      <Header />
      <MainContent />
    </ThemeProvider>
  )
}

function Header() {
  const { theme, toggleTheme } = useTheme()
  
  return (
    <header>
      <button onClick={toggleTheme}>
        Switch to {theme === 'light' ? 'dark' : 'light'} mode
      </button>
    </header>
  )
}
```

### 7.3 Performance Optimization

**useMemo:**
```typescript
import { useMemo } from 'react'

function ExpensiveCalculation({ numbers }: { numbers: number[] }) {
  const sum = useMemo(() => {
    console.log('Calculating sum...')
    return numbers.reduce((acc, num) => acc + num, 0)
  }, [numbers])
  
  return <div>Sum: {sum}</div>
}

// Memoizing objects
function UserProfile({ user }: { user: { id: string; name: string } }) {
  const userStyles = useMemo(
    () => ({
      backgroundColor: user.id % 2 === 0 ? '#f0f0f0' : '#ffffff',
      padding: '1rem'
    }),
    [user.id]
  )
  
  return <div style={userStyles}>{user.name}</div>
}
```

**useCallback:**
```typescript
import { useCallback } from 'react'

function ParentComponent() {
  const [count, setCount] = useState(0)
  
  const handleClick = useCallback(() => {
    console.log('Button clicked!')
  }, [])
  
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(c => c + 1)}>Increment</button>
      <ChildComponent onClick={handleClick} />
    </div>
  )
}

// ChildComponent won't re-render if handleClick is memoized
const ChildComponent = React.memo(function ChildComponent({
  onClick
}: {
  onClick: () => void
}) {
  console.log('ChildComponent rendered')
  return <button onClick={onClick}>Click me</button>
})
```

**React.memo:**
```typescript
import { memo } from 'react'

type UserCardProps = {
  user: { id: string; name: string; email: string }
  onUpdate: (id: string) => void
}

const UserCard = memo(function UserCard({ user, onUpdate }: UserCardProps) {
  console.log(`Rendering UserCard: ${user.id}`)
  
  return (
    <div>
      <h3>{user.name}</h3>
      <p>{user.email}</p>
      <button onClick={() => onUpdate(user.id)}>Update</button>
    </div>
  )
})

// Custom comparison function
const UserCardWithCustomCompare = memo(
  function UserCard({ user, onUpdate }: UserCardProps) {
    return (
      <div>
        <h3>{user.name}</h3>
        <button onClick={() => onUpdate(user.id)}>Update</button>
      </div>
    )
  },
  (prevProps, nextProps) => {
    // Only re-render if user.id or user.name changes
    return (
      prevProps.user.id === nextProps.user.id &&
      prevProps.user.name === nextProps.user.name
    )
  }
)
```

### 7.4 Best Practices

**Component Design:**
- Use functional components by default
- Implement proper TypeScript types
- Create reusable components
- Use composition patterns

**State Management:**
- Use useState for simple state
- Use useReducer for complex state
- Use Context API for global state
- Implement custom hooks for reusable logic

**Performance:**
- Use useMemo for expensive calculations
- Use useCallback for event handlers
- Use React.memo for expensive components
- Implement virtualization for long lists

**Error Handling:**
- Implement error boundaries
- Handle errors gracefully
- Log errors to tracking service
- Provide fallback UI

**Accessibility:**
- Use semantic HTML
- Implement keyboard navigation
- Add ARIA attributes
- Test with screen readers

---

## 8. Related Skills

- `02-frontend/nextjs-patterns`
- `02-frontend/state-management`
- `02-frontend/form-handling`
- `02-frontend/error-boundaries-react`
- `22-ux-ui-design/accessibility`
