# React Best Practices and Patterns

## 1. Component Patterns

### Functional Components
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

### Custom Hooks
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

### Custom Hook with Async Operations
```typescript
// useFetch.ts
import { useState, useEffect, useCallback } from 'react'

type UseFetchResult<T> = {
  data: T | null
  loading: boolean
  error: Error | null
  refetch: () => Promise<void>
}

function useFetch<T>(url: string): UseFetchResult<T> {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)
  
  const fetchData = useCallback(async () => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await fetch(url)
      if (!response.ok) throw new Error('Network response was not ok')
      const result = await response.json()
      setData(result)
    } catch (err) {
      setError(err as Error)
    } finally {
      setLoading(false)
    }
  }, [url])
  
  useEffect(() => {
    fetchData()
  }, [fetchData])
  
  return { data, loading, error, refetch: fetchData }
}
```

### Composition Patterns
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

### Render Props Pattern
```typescript
// MouseTracker.tsx
import { useState, ReactNode } from 'react'

type MouseTrackerProps = {
  render: (position: { x: number; y: number }) => ReactNode
}

function MouseTracker({ render }: MouseTrackerProps) {
  const [position, setPosition] = useState({ x: 0, y: 0 })
  
  return (
    <div
      onMouseMove={e => setPosition({ x: e.clientX, y: e.clientY })}
      className="relative h-64 border"
    >
      {render(position)}
    </div>
  )
}

// Usage
<MouseTracker
  render={({ x, y }) => (
    <div>
      Mouse position: {x}, {y}
    </div>
  )}
/>
```

### Compound Components Pattern
```typescript
// Tabs.tsx
import { createContext, useContext, useState, ReactNode, cloneElement } from 'react'

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

## 2. State Management

### useState Pattern
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

### useReducer Pattern
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

### Lifting State Up
```typescript
// Parent component holds state
function TemperatureCalculator() {
  const [celsius, setCelsius] = useState('')
  const [fahrenheit, setFahrenheit] = useState('')
  
  const handleCelsiusChange = (value: string) => {
    setCelsius(value)
    setFahrenheit(value ? ((parseFloat(value) * 9) / 5 + 32).toString() : '')
  }
  
  const handleFahrenheitChange = (value: string) => {
    setFahrenheit(value)
    setCelsius(value ? (((parseFloat(value) - 32) * 5) / 9).toString() : '')
  }
  
  return (
    <div>
      <TemperatureInput
        label="Celsius"
        value={celsius}
        onChange={handleCelsiusChange}
      />
      <TemperatureInput
        label="Fahrenheit"
        value={fahrenheit}
        onChange={handleFahrenheitChange}
      />
    </div>
  )
}

type TemperatureInputProps = {
  label: string
  value: string
  onChange: (value: string) => void
}

function TemperatureInput({ label, value, onChange }: TemperatureInputProps) {
  return (
    <div>
      <label>{label}</label>
      <input
        type="number"
        value={value}
        onChange={e => onChange(e.target.value)}
      />
    </div>
  )
}
```

### Context API Usage
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

### Context with Multiple Values
```typescript
// AuthContext.tsx
import { createContext, useContext, useState, ReactNode } from 'react'

type User = {
  id: string
  name: string
  email: string
}

type AuthContextValue = {
  user: User | null
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  isAuthenticated: boolean
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  
  const login = async (email: string, password: string) => {
    // Simulate API call
    const response = await fetch('/api/login', {
      method: 'POST',
      body: JSON.stringify({ email, password })
    })
    const data = await response.json()
    setUser(data.user)
  }
  
  const logout = () => {
    setUser(null)
  }
  
  return (
    <AuthContext.Provider
      value={{
        user,
        login,
        logout,
        isAuthenticated: !!user
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
```

## 3. Performance Optimization

### useMemo
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

### useCallback
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

### React.memo
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

### Code Splitting with React.lazy
```typescript
import { lazy, Suspense } from 'react'

// Lazy load heavy components
const HeavyChart = lazy(() => import('./HeavyChart'))
const AdminPanel = lazy(() => import('./AdminPanel'))

function Dashboard() {
  const [isAdmin, setIsAdmin] = useState(false)
  
  return (
    <div>
      <h1>Dashboard</h1>
      
      <Suspense fallback={<div>Loading chart...</div>}>
        <HeavyChart />
      </Suspense>
      
      {isAdmin && (
        <Suspense fallback={<div>Loading admin panel...</div>}>
          <AdminPanel />
        </Suspense>
      )}
    </div>
  )
}
```

### Virtualization for Long Lists
```typescript
import { FixedSizeList } from 'react-window'

function VirtualizedList({ items }: { items: string[] }) {
  const Row = ({ index, style }: { index: number; style: React.CSSProperties }) => (
    <div style={style} className="p-4 border-b">
      {items[index]}
    </div>
  )
  
  return (
    <FixedSizeList
      height={400}
      itemCount={items.length}
      itemSize={50}
      width="100%"
    >
      {Row}
    </FixedSizeList>
  )
}
```

## 4. Side Effects (useEffect)

### Basic useEffect
```typescript
import { useEffect, useState } from 'react'

function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  
  useEffect(() => {
    let cancelled = false
    
    async function fetchUser() {
      try {
        const response = await fetch(`/api/users/${userId}`)
        const data = await response.json()
        
        if (!cancelled) {
          setUser(data)
        }
      } catch (error) {
        console.error('Failed to fetch user:', error)
      } finally {
        if (!cancelled) {
          setLoading(false)
        }
      }
    }
    
    fetchUser()
    
    return () => {
      cancelled = true
    }
  }, [userId])
  
  if (loading) return <div>Loading...</div>
  return <div>{user?.name}</div>
}
```

### useEffect with Dependencies
```typescript
// Correct: All dependencies listed
function SearchComponent() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  
  useEffect(() => {
    if (query.length > 2) {
      fetch(`/api/search?q=${query}`)
        .then(res => res.json())
        .then(data => setResults(data))
    }
  }, [query]) // query is a dependency
  
  return (
    <div>
      <input value={query} onChange={e => setQuery(e.target.value)} />
      <ul>
        {results.map((item, i) => (
          <li key={i}>{item}</li>
        ))}
      </ul>
    </div>
  )
}

// Wrong: Missing dependency
function BadExample() {
  const [count, setCount] = useState(0)
  
  useEffect(() => {
    const interval = setInterval(() => {
      setCount(c => c + 1) // This works because of functional update
    }, 1000)
    
    return () => clearInterval(interval)
  }, []) // Empty array is correct here since we use functional update
}
```

### Cleanup Functions
```typescript
// Event listener cleanup
function WindowSize() {
  const [size, setSize] = useState({ width: 0, height: 0 })
  
  useEffect(() => {
    const handleResize = () => {
      setSize({
        width: window.innerWidth,
        height: window.innerHeight
      })
    }
    
    window.addEventListener('resize', handleResize)
    handleResize() // Initial call
    
    return () => {
      window.removeEventListener('resize', handleResize)
    }
  }, [])
  
  return (
    <div>
      Width: {size.width}, Height: {size.height}
    </div>
  )
}

// WebSocket cleanup
function ChatRoom({ roomId }: { roomId: string }) {
  const [messages, setMessages] = useState([])
  
  useEffect(() => {
    const ws = new WebSocket(`wss://api.example.com/rooms/${roomId}`)
    
    ws.onmessage = (event) => {
      const message = JSON.parse(event.data)
      setMessages(prev => [...prev, message])
    }
    
    return () => {
      ws.close()
    }
  }, [roomId])
  
  return (
    <div>
      {messages.map((msg, i) => (
        <div key={i}>{msg.text}</div>
      ))}
    </div>
  )
}
```

### Common Pitfalls
```typescript
// Pitfall 1: Infinite loop
function BadComponent() {
  const [count, setCount] = useState(0)
  
  useEffect(() => {
    setCount(count + 1) // This causes infinite loop
  }, [count]) // count changes, effect runs, count changes again...
  
  return <div>{count}</div>
}

// Fix: Use functional update
function GoodComponent() {
  const [count, setCount] = useState(0)
  
  useEffect(() => {
    setCount(c => c + 1)
  }, []) // No dependency needed
  
  return <div>{count}</div>
}

// Pitfall 2: Missing async function
function BadAsyncEffect() {
  useEffect(async () => { // Error: useEffect callback cannot be async
    const data = await fetchData()
  }, [])
}

// Fix: Define async function inside
function GoodAsyncEffect() {
  useEffect(() => {
    async function fetchData() {
      const data = await fetchData()
    }
    fetchData()
  }, [])
}

// Pitfall 3: Stale closure
function Counter() {
  const [count, setCount] = useState(0)
  
  useEffect(() => {
    const id = setInterval(() => {
      console.log(count) // Always logs 0 (stale closure)
    }, 1000)
    
    return () => clearInterval(id)
  }, []) // Empty dependency array
  
  return <button onClick={() => setCount(c => c + 1)}>Increment</button>
}

// Fix: Use ref or add count to dependencies
function CounterFixed() {
  const [count, setCount] = useState(0)
  const countRef = useRef(count)
  
  useEffect(() => {
    countRef.current = count
  }, [count])
  
  useEffect(() => {
    const id = setInterval(() => {
      console.log(countRef.current) // Always gets latest value
    }, 1000)
    
    return () => clearInterval(id)
  }, [])
  
  return <button onClick={() => setCount(c => c + 1)}>Increment</button>
}
```

## 5. Forms Handling

### Controlled Components
```typescript
function ContactForm() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: ''
  })
  
  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    console.log(formData)
    // Submit form data...
  }
  
  return (
    <form onSubmit={handleSubmit}>
      <input
        name="name"
        value={formData.name}
        onChange={handleChange}
        placeholder="Name"
        required
      />
      <input
        name="email"
        type="email"
        value={formData.email}
        onChange={handleChange}
        placeholder="Email"
        required
      />
      <textarea
        name="message"
        value={formData.message}
        onChange={handleChange}
        placeholder="Message"
        required
      />
      <button type="submit">Send</button>
    </form>
  )
}
```

### Form with Validation
```typescript
type FormErrors = {
  name?: string
  email?: string
  password?: string
}

function RegistrationForm() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: ''
  })
  const [errors, setErrors] = useState<FormErrors>({})
  const [touched, setTouched] = useState<Record<string, boolean>>({})
  
  const validate = (): boolean => {
    const newErrors: FormErrors = {}
    
    if (!formData.name.trim()) {
      newErrors.name = 'Name is required'
    } else if (formData.name.length < 2) {
      newErrors.name = 'Name must be at least 2 characters'
    }
    
    if (!formData.email.trim()) {
      newErrors.email = 'Email is required'
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Invalid email format'
    }
    
    if (!formData.password) {
      newErrors.password = 'Password is required'
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters'
    }
    
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }
  
  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
    
    // Clear error when user starts typing
    if (errors[name as keyof FormErrors]) {
      setErrors(prev => ({ ...prev, [name]: undefined }))
    }
  }
  
  const handleBlur = (e: React.FocusEvent<HTMLInputElement>) => {
    const { name } = e.target
    setTouched(prev => ({ ...prev, [name]: true }))
    validate()
  }
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    
    if (validate()) {
      // Submit form...
      console.log('Form submitted:', formData)
    }
  }
  
  return (
    <form onSubmit={handleSubmit}>
      <div>
        <input
          name="name"
          value={formData.name}
          onChange={handleChange}
          onBlur={handleBlur}
          placeholder="Name"
        />
        {touched.name && errors.name && (
          <span className="error">{errors.name}</span>
        )}
      </div>
      
      <div>
        <input
          name="email"
          type="email"
          value={formData.email}
          onChange={handleChange}
          onBlur={handleBlur}
          placeholder="Email"
        />
        {touched.email && errors.email && (
          <span className="error">{errors.email}</span>
        )}
      </div>
      
      <div>
        <input
          name="password"
          type="password"
          value={formData.password}
          onChange={handleChange}
          onBlur={handleBlur}
          placeholder="Password"
        />
        {touched.password && errors.password && (
          <span className="error">{errors.password}</span>
        )}
      </div>
      
      <button type="submit">Register</button>
    </form>
  )
}
```

## 6. Error Boundaries

```typescript
// ErrorBoundary.tsx
import { Component, ReactNode } from 'react'

type ErrorBoundaryState = {
  hasError: boolean
  error: Error | null
}

type ErrorBoundaryProps = {
  children: ReactNode
  fallback?: ReactNode
  onError?: (error: Error, errorInfo: any) => void
}

class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props)
    this.state = { hasError: false, error: null }
  }
  
  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error }
  }
  
  componentDidCatch(error: Error, errorInfo: any) {
    console.error('Error caught by boundary:', error, errorInfo)
    this.props.onError?.(error, errorInfo)
  }
  
  render() {
    if (this.state.hasError) {
      return (
        this.props.fallback || (
          <div className="error-boundary">
            <h2>Something went wrong</h2>
            <p>{this.state.error?.message}</p>
            <button onClick={() => window.location.reload()}>
              Reload page
            </button>
          </div>
        )
      )
    }
    
    return this.props.children
  }
}

// Usage
function App() {
  return (
    <ErrorBoundary
      onError={(error, errorInfo) => {
        // Log to error tracking service
        logErrorToService(error, errorInfo)
      }}
    >
      <MainContent />
    </ErrorBoundary>
  )
}

// Functional Error Boundary (with react-error-boundary)
import { ErrorBoundary } from 'react-error-boundary'

function ErrorFallback({ error, resetErrorBoundary }: any) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <pre>{error.message}</pre>
      <button onClick={resetErrorBoundary}>Try again</button>
    </div>
  )
}

function App() {
  return (
    <ErrorBoundary FallbackComponent={ErrorFallback}>
      <MainContent />
    </ErrorBoundary>
  )
}
```

## 7. Accessibility (a11y)

### Semantic HTML
```typescript
function AccessibleForm() {
  return (
    <form>
      <fieldset>
        <legend>Personal Information</legend>
        
        <div>
          <label htmlFor="name">Full Name</label>
          <input
            id="name"
            name="name"
            type="text"
            required
            aria-required="true"
          />
        </div>
        
        <div>
          <label htmlFor="email">Email Address</label>
          <input
            id="email"
            name="email"
            type="email"
            required
            aria-required="true"
            aria-describedby="email-hint"
          />
          <span id="email-hint">We'll never share your email</span>
        </div>
      </fieldset>
      
      <button type="submit">Submit</button>
    </form>
  )
}
```

### ARIA Attributes
```typescript
function AccessibleModal({ isOpen, onClose, children }: any) {
  if (!isOpen) return null
  
  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
    >
      <h2 id="modal-title">Modal Title</h2>
      <button
        onClick={onClose}
        aria-label="Close modal"
      >
        ×
      </button>
      {children}
    </div>
  )
}

function AccessibleTabs({ tabs, activeTab, onTabChange }: any) {
  return (
    <div role="tablist">
      {tabs.map((tab: string, index: number) => (
        <button
          key={tab}
          role="tab"
          aria-selected={activeTab === index}
          aria-controls={`panel-${index}`}
          id={`tab-${index}`}
          onClick={() => onTabChange(index)}
        >
          {tab}
        </button>
      ))}
      
      {tabs.map((tab: string, index: number) => (
        <div
          key={tab}
          role="tabpanel"
          id={`panel-${index}`}
          aria-labelledby={`tab-${index}`}
          hidden={activeTab !== index}
        >
          {tab} content
        </div>
      ))}
    </div>
  )
}
```

### Focus Management
```typescript
import { useRef, useEffect } from 'react'

function FocusTrap({ children, isActive }: any) {
  const containerRef = useRef<HTMLDivElement>(null)
  const firstFocusableRef = useRef<HTMLElement | null>(null)
  const lastFocusableRef = useRef<HTMLElement | null>(null)
  
  useEffect(() => {
    if (!isActive || !containerRef.current) return
    
    const focusableElements = containerRef.current.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    )
    
    firstFocusableRef.current = focusableElements[0] as HTMLElement
    lastFocusableRef.current = focusableElements[
      focusableElements.length - 1
    ] as HTMLElement
    
    firstFocusableRef.current?.focus()
    
    const handleTab = (e: KeyboardEvent) => {
      if (e.key !== 'Tab') return
      
      if (e.shiftKey) {
        if (document.activeElement === firstFocusableRef.current) {
          e.preventDefault()
          lastFocusableRef.current?.focus()
        }
      } else {
        if (document.activeElement === lastFocusableRef.current) {
          e.preventDefault()
          firstFocusableRef.current?.focus()
        }
      }
    }
    
    document.addEventListener('keydown', handleTab)
    return () => document.removeEventListener('keydown', handleTab)
  }, [isActive])
  
  return <div ref={containerRef}>{children}</div>
}
```

## 8. Testing Components

### Testing with React Testing Library
```typescript
// Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react'
import { Button } from './Button'

describe('Button', () => {
  it('renders children correctly', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })
  
  it('calls onClick when clicked', () => {
    const handleClick = jest.fn()
    render(<Button onClick={handleClick}>Click me</Button>)
    
    fireEvent.click(screen.getByText('Click me'))
    expect(handleClick).toHaveBeenCalledTimes(1)
  })
  
  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Click me</Button>)
    expect(screen.getByText('Click me')).toBeDisabled()
  })
})

// Form.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { ContactForm } from './ContactForm'

describe('ContactForm', () => {
  it('submits form with valid data', async () => {
    const handleSubmit = jest.fn()
    render(<ContactForm onSubmit={handleSubmit} />)
    
    fireEvent.change(screen.getByLabelText(/name/i), {
      target: { value: 'John Doe' }
    })
    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: 'john@example.com' }
    })
    
    fireEvent.click(screen.getByRole('button', { name: /send/i }))
    
    await waitFor(() => {
      expect(handleSubmit).toHaveBeenCalledWith({
        name: 'John Doe',
        email: 'john@example.com'
      })
    })
  })
})
```

## 9. Common Anti-Patterns to Avoid

### Don't Mutate State Directly
```typescript
// Bad
function BadComponent() {
  const [items, setItems] = useState([1, 2, 3])
  
  const addItem = () => {
    items.push(4) // Mutation!
    setItems(items)
  }
}

// Good
function GoodComponent() {
  const [items, setItems] = useState([1, 2, 3])
  
  const addItem = () => {
    setItems([...items, 4]) // New array
  }
}
```

### Don't Use useEffect for Derived State
```typescript
// Bad
function BadComponent({ items }: { items: number[] }) {
  const [total, setTotal] = useState(0)
  
  useEffect(() => {
    setTotal(items.reduce((sum, item) => sum + item, 0))
  }, [items])
  
  return <div>Total: {total}</div>
}

// Good
function GoodComponent({ items }: { items: number[] }) {
  const total = items.reduce((sum, item) => sum + item, 0)
  
  return <div>Total: {total}</div>
}
```

### Don't Over-optimize
```typescript
// Bad: Premature optimization
function BadComponent({ data }: { data: string[] }) {
  const processed = useMemo(() => data.map(d => d.toUpperCase()), [data])
  return <div>{processed.join(', ')}</div>
}

// Good: Simple computation doesn't need memoization
function GoodComponent({ data }: { data: string[] }) {
  const processed = data.map(d => d.toUpperCase())
  return <div>{processed.join(', ')}</div>
}
```

## 10. TypeScript with React

### Type Definitions
```typescript
// Component props with TypeScript
type ButtonProps = {
  children: React.ReactNode
  variant?: 'primary' | 'secondary' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
  onClick?: () => void
  className?: string
}

export function Button({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  onClick,
  className = ''
}: ButtonProps) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`
        ${variantStyles[variant]}
        ${sizeStyles[size]}
        ${disabled ? 'opacity-50 cursor-not-allowed' : ''}
        ${className}
      `}
    >
      {children}
    </button>
  )
}

// Generic component
type ListProps<T> = {
  items: T[]
  renderItem: (item: T) => React.ReactNode
  keyExtractor: (item: T) => string
}

export function List<T>({ items, renderItem, keyExtractor }: ListProps<T>) {
  return (
    <ul>
      {items.map(item => (
        <li key={keyExtractor(item)}>{renderItem(item)}</li>
      ))}
    </ul>
  )
}

// Usage
<List
  items={users}
  renderItem={user => <span>{user.name}</span>}
  keyExtractor={user => user.id}
/>
```

### Type Guards
```typescript
function isUser(obj: any): obj is User {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    typeof obj.id === 'string' &&
    typeof obj.name === 'string'
  )
}

function UserProfile({ user }: { user: unknown }) {
  if (!isUser(user)) {
    return <div>Invalid user data</div>
  }
  
  return <div>{user.name}</div>
}
```

### Discriminated Unions
```typescript
type ApiResponse =
  | { status: 'success'; data: any }
  | { status: 'error'; error: string }

function handleResponse(response: ApiResponse) {
  if (response.status === 'success') {
    console.log(response.data) // TypeScript knows this is available
  } else {
    console.log(response.error) // TypeScript knows this is available
  }
}
```

### Event Handler Types
```typescript
function FormComponent() {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    console.log(e.target.value)
  }
  
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
  }
  
  const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    console.log('Clicked')
  }
  
  return (
    <form onSubmit={handleSubmit}>
      <input onChange={handleChange} />
      <button onClick={handleClick}>Submit</button>
    </form>
  )
}
```
