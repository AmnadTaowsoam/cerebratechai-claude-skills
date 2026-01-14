# State Management Patterns in React

## 1. When to Use Each Solution

### Decision Matrix

| Solution | Best For | Complexity | Bundle Size | Learning Curve |
|----------|-----------|-------------|-------------|----------------|
| React State | Local component state | Low | Built-in | Easy |
| React Context | Global app state, themes, auth | Medium | Built-in | Medium |
| Zustand | Simple global state, minimal boilerplate | Low | ~1KB | Easy |
| Redux Toolkit | Complex apps, time-travel debugging | High | ~10KB | Medium-Hard |
| TanStack Query | Server state, caching, synchronization | Medium | ~13KB | Medium |
| Jotai | Atomic state, fine-grained reactivity | Medium | ~3KB | Medium |

### Quick Guide

```typescript
// Use React useState/useReducer for:
// - Form state
// - UI toggle states
const [isOpen, setIsOpen] = useState(false)

// Use React Context for:
// - Theme (dark/light mode)
// - Authentication state
// - User preferences

// Use Zustand for:
// - Simple global state
// - Cross-component state sharing
// - When you want minimal boilerplate

// Use Redux Toolkit for:
// - Large-scale applications
// - Complex state logic
// - When you need devtools and middleware

// Use TanStack Query for:
// - Server data fetching
// - Caching and synchronization
// - Optimistic updates

// Use Jotai for:
// - Atomic state management
// - Fine-grained reactivity
// - Composable state
```

## 2. React Context

### Setup
```typescript
// contexts/ThemeContext.tsx
"use client"

import { createContext, useContext, useState, ReactNode } from "react"

type Theme = "light" | "dark"

interface ThemeContextValue {
  theme: Theme
  toggleTheme: () => void
}

const ThemeContext = createContext<ThemeContextValue | undefined>(undefined)

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<Theme>("light")

  const toggleTheme = () => {
    setTheme((prev) => (prev === "light" ? "dark" : "light"))
  }

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}

export function useTheme() {
  const context = useContext(ThemeContext)
  if (!context) {
    throw new Error("useTheme must be used within ThemeProvider")
  }
  return context
}
```

### Usage Patterns
```typescript
// contexts/AuthContext.tsx
"use client"

import { createContext, useContext, useState, ReactNode, useCallback } from "react"

interface User {
  id: string
  name: string
  email: string
}

interface AuthContextValue {
  user: User | null
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  isAuthenticated: boolean
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)

  const login = useCallback(async (email: string, password: string) => {
    const response = await fetch("/api/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    })
    const data = await response.json()
    setUser(data.user)
  }, [])

  const logout = useCallback(() => {
    setUser(null)
  }, [])

  return (
    <AuthContext.Provider
      value={{
        user,
        login,
        logout,
        isAuthenticated: !!user,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider")
  }
  return context
}

// Usage in components
function UserProfile() {
  const { user, logout } = useAuth()

  return (
    <div>
      <h1>Welcome, {user?.name}</h1>
      <button onClick={logout}>Logout</button>
    </div>
  )
}
```

### Performance Considerations
```typescript
// Problem: Context causes all consumers to re-render
const ThemeContext = createContext<ThemeValue | undefined>(undefined)

// Solution: Split contexts to prevent unnecessary re-renders
const ColorModeContext = createContext<ColorMode | undefined>(undefined)
const FontSizeContext = createContext<FontSize | undefined>(undefined)

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [colorMode, setColorMode] = useState<ColorMode>("light")
  const [fontSize, setFontSize] = useState<FontSize>("medium")

  return (
    <ColorModeContext.Provider value={colorMode}>
      <FontSizeContext.Provider value={fontSize}>
        {children}
      </FontSizeContext.Provider>
    </ColorModeContext.Provider>
  )
}

// Components only subscribe to what they use
function ColorModeToggle() {
  const colorMode = useContext(ColorModeContext)
  // Only re-renders when colorMode changes
}

function FontSizeSelector() {
  const fontSize = useContext(FontSizeContext)
  // Only re-renders when fontSize changes
}
```

### Optimized Context with useReducer
```typescript
// contexts/TodoContext.tsx
"use client"

import { createContext, useContext, useReducer, ReactNode } from "react"

type Todo = {
  id: string
  text: string
  completed: boolean
}

type TodoState = {
  todos: Todo[]
  filter: "all" | "active" | "completed"
}

type TodoAction =
  | { type: "ADD_TODO"; text: string }
  | { type: "TOGGLE_TODO"; id: string }
  | { type: "DELETE_TODO"; id: string }
  | { type: "SET_FILTER"; filter: TodoState["filter"] }

function todoReducer(state: TodoState, action: TodoAction): TodoState {
  switch (action.type) {
    case "ADD_TODO":
      return {
        ...state,
        todos: [
          ...state.todos,
          {
            id: Date.now().toString(),
            text: action.text,
            completed: false,
          },
        ],
      }
    case "TOGGLE_TODO":
      return {
        ...state,
        todos: state.todos.map((todo) =>
          todo.id === action.id ? { ...todo, completed: !todo.completed } : todo
        ),
      }
    case "DELETE_TODO":
      return {
        ...state,
        todos: state.todos.filter((todo) => todo.id !== action.id),
      }
    case "SET_FILTER":
      return { ...state, filter: action.filter }
    default:
      return state
  }
}

const TodoContext = createContext<{
  state: TodoState
  dispatch: React.Dispatch<TodoAction>
} | null>(null)

export function TodoProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(todoReducer, {
    todos: [],
    filter: "all",
  })

  return (
    <TodoContext.Provider value={{ state, dispatch }}>
      {children}
    </TodoContext.Provider>
  )
}

export function useTodos() {
  const context = useContext(TodoContext)
  if (!context) {
    throw new Error("useTodos must be used within TodoProvider")
  }
  return context
}
```

## 3. Zustand

### Store Creation
```typescript
// stores/useCounterStore.ts
import { create } from "zustand"

interface CounterState {
  count: number
  increment: () => void
  decrement: () => void
  reset: () => void
}

export const useCounterStore = create<CounterState>((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
  reset: () => set({ count: 0 }),
}))
```

### Usage
```typescript
// components/Counter.tsx
"use client"

import { useCounterStore } from "@/stores/useCounterStore"

export function Counter() {
  const { count, increment, decrement, reset } = useCounterStore()

  return (
    <div>
      <h1>Count: {count}</h1>
      <button onClick={decrement}>-</button>
      <button onClick={increment}>+</button>
      <button onClick={reset}>Reset</button>
    </div>
  )
}

// Selective subscription (only re-renders when count changes)
function CountDisplay() {
  const count = useCounterStore((state) => state.count)
  return <span>{count}</span>
}

// Multiple selectors
function CounterControls() {
  const increment = useCounterStore((state) => state.increment)
  const decrement = useCounterStore((state) => state.decrement)
  
  return (
    <>
      <button onClick={decrement}>-</button>
      <button onClick={increment}>+</button>
    </>
  )
}
```

### Async Actions
```typescript
// stores/useUserStore.ts
import { create } from "zustand"

interface User {
  id: string
  name: string
  email: string
}

interface UserState {
  user: User | null
  loading: boolean
  error: string | null
  fetchUser: (id: string) => Promise<void>
  updateUser: (data: Partial<User>) => Promise<void>
}

export const useUserStore = create<UserState>((set) => ({
  user: null,
  loading: false,
  error: null,
  
  fetchUser: async (id: string) => {
    set({ loading: true, error: null })
    try {
      const response = await fetch(`/api/users/${id}`)
      const user = await response.json()
      set({ user, loading: false })
    } catch (error) {
      set({ error: "Failed to fetch user", loading: false })
    }
  },
  
  updateUser: async (data: Partial<User>) => {
    set({ loading: true, error: null })
    try {
      const response = await fetch(`/api/users/${data.id}`, {
        method: "PATCH",
        body: JSON.stringify(data),
      })
      const user = await response.json()
      set({ user, loading: false })
    } catch (error) {
      set({ error: "Failed to update user", loading: false })
    }
  },
}))
```

### Middleware
```typescript
// stores/useStoreWithMiddleware.ts
import { create } from "zustand"
import { devtools, persist } from "zustand/middleware"

interface AppState {
  count: number
  increment: () => void
}

export const useStoreWithMiddleware = create<AppState>()(
  devtools(
    persist(
      (set) => ({
        count: 0,
        increment: () => set((state) => ({ count: state.count + 1 })),
      }),
      {
        name: "app-storage", // localStorage key
        partialize: (state) => ({ count: state.count }), // only persist count
      }
    )
  )
)

// Custom middleware for logging
const logger = (config) => (set, get, api) => config(
  (...args) => {
    console.log("  applying", args)
    set(...args)
    console.log("  new state", get())
  },
  get,
  api
)

export const useLoggedStore = create<AppState>()(
  logger(
    devtools((set) => ({
      count: 0,
      increment: () => set((state) => ({ count: state.count + 1 })),
    }))
  )
)
```

## 4. Redux Toolkit

### Slices
```typescript
// store/counterSlice.ts
import { createSlice, PayloadAction } from "@reduxjs/toolkit"

interface CounterState {
  value: number
}

const initialState: CounterState = {
  value: 0,
}

export const counterSlice = createSlice({
  name: "counter",
  initialState,
  reducers: {
    increment: (state) => {
      state.value += 1
    },
    decrement: (state) => {
      state.value -= 1
    },
    incrementByAmount: (state, action: PayloadAction<number>) => {
      state.value += action.payload
    },
    reset: (state) => {
      state.value = 0
    },
  },
})

export const { increment, decrement, incrementByAmount, reset } = counterSlice.actions
export default counterSlice.reducer
```

### Async Thunks
```typescript
// store/userSlice.ts
import { createSlice, createAsyncThunk, PayloadAction } from "@reduxjs/toolkit"

interface User {
  id: string
  name: string
  email: string
}

interface UserState {
  user: User | null
  loading: boolean
  error: string | null
}

const initialState: UserState = {
  user: null,
  loading: false,
  error: null,
}

export const fetchUser = createAsyncThunk(
  "user/fetchUser",
  async (userId: string) => {
    const response = await fetch(`/api/users/${userId}`)
    return await response.json()
  }
)

export const updateUser = createAsyncThunk(
  "user/updateUser",
  async (userData: Partial<User>) => {
    const response = await fetch(`/api/users/${userData.id}`, {
      method: "PATCH",
      body: JSON.stringify(userData),
    })
    return await response.json()
  }
)

const userSlice = createSlice({
  name: "user",
  initialState,
  reducers: {
    clearUser: (state) => {
      state.user = null
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch user
      .addCase(fetchUser.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(fetchUser.fulfilled, (state, action) => {
        state.loading = false
        state.user = action.payload
      })
      .addCase(fetchUser.rejected, (state, action) => {
        state.loading = false
        state.error = action.error.message || "Failed to fetch user"
      })
      // Update user
      .addCase(updateUser.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(updateUser.fulfilled, (state, action) => {
        state.loading = false
        state.user = action.payload
      })
      .addCase(updateUser.rejected, (state, action) => {
        state.loading = false
        state.error = action.error.message || "Failed to update user"
      })
  },
})

export const { clearUser } = userSlice.actions
export default userSlice.reducer
```

### Store Configuration
```typescript
// store/index.ts
import { configureStore } from "@reduxjs/toolkit"
import counterReducer from "./counterSlice"
import userReducer from "./userSlice"

export const store = configureStore({
  reducer: {
    counter: counterReducer,
    user: userReducer,
  },
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
```

### Typed Hooks
```typescript
// store/hooks.ts
import { TypedUseSelectorHook, useDispatch, useSelector } from "react-redux"
import type { RootState, AppDispatch } from "./store"

export const useAppDispatch: () => AppDispatch = useDispatch
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector
```

### Usage in Components
```typescript
// components/Counter.tsx
"use client"

import { useAppDispatch, useAppSelector } from "@/store/hooks"
import { increment, decrement, incrementByAmount } from "@/store/counterSlice"

export function Counter() {
  const count = useAppSelector((state) => state.counter.value)
  const dispatch = useAppDispatch()

  return (
    <div>
      <h1>Count: {count}</h1>
      <button onClick={() => dispatch(decrement())}>-</button>
      <button onClick={() => dispatch(increment())}>+</button>
      <button onClick={() => dispatch(incrementByAmount(5))}>+5</button>
    </div>
  )
}

// components/UserProfile.tsx
"use client"

import { useEffect } from "react"
import { useAppDispatch, useAppSelector } from "@/store/hooks"
import { fetchUser, clearUser } from "@/store/userSlice"

export function UserProfile({ userId }: { userId: string }) {
  const dispatch = useAppDispatch()
  const { user, loading, error } = useAppSelector((state) => state.user)

  useEffect(() => {
    dispatch(fetchUser(userId))
  }, [dispatch, userId])

  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error}</div>

  return (
    <div>
      <h1>{user?.name}</h1>
      <p>{user?.email}</p>
      <button onClick={() => dispatch(clearUser())}>Clear</button>
    </div>
  )
}
```

### RTK Query
```typescript
// store/apiSlice.ts
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react"

export const apiSlice = createApi({
  reducerPath: "api",
  baseQuery: fetchBaseQuery({ baseUrl: "/api" }),
  tagTypes: ["User", "Post"],
  endpoints: (builder) => ({
    getUsers: builder.query<User[], void>({
      query: () => "/users",
      providesTags: (result) =>
        result
          ? [...result.map(({ id }) => ({ type: "User" as const, id })), "User"]
          : ["User"],
    }),
    getUser: builder.query<User, string>({
      query: (id) => `/users/${id}`,
      providesTags: (_result, _error, id) => [{ type: "User", id }],
    }),
    createUser: builder.mutation<User, Partial<User>>({
      query: (body) => ({
        url: "/users",
        method: "POST",
        body,
      }),
      invalidatesTags: ["User"],
    }),
    updateUser: builder.mutation<User, Partial<User> & { id: string }>({
      query: ({ id, ...body }) => ({
        url: `/users/${id}`,
        method: "PATCH",
        body,
      }),
      invalidatesTags: (_result, _error, { id }) => [{ type: "User", id }],
    }),
    deleteUser: builder.mutation<void, string>({
      query: (id) => ({
        url: `/users/${id}`,
        method: "DELETE",
      }),
      invalidatesTags: (_result, _error, id) => [{ type: "User", id }],
    }),
  }),
})

export const {
  useGetUsersQuery,
  useGetUserQuery,
  useCreateUserMutation,
  useUpdateUserMutation,
  useDeleteUserMutation,
} = apiSlice

// Add the api reducer to the store
// store/index.ts
import { configureStore } from "@reduxjs/toolkit"
import { apiSlice } from "./apiSlice"
import counterReducer from "./counterSlice"

export const store = configureStore({
  reducer: {
    [apiSlice.reducerPath]: apiSlice.reducer,
    counter: counterReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(apiSlice.middleware),
})
```

### Using RTK Query
```typescript
// components/UserList.tsx
"use client"

import { useGetUsersQuery, useDeleteUserMutation } from "@/store/apiSlice"

export function UserList() {
  const { data: users, isLoading, error } = useGetUsersQuery()
  const [deleteUser] = useDeleteUserMutation()

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error loading users</div>

  return (
    <ul>
      {users?.map((user) => (
        <li key={user.id}>
          {user.name} - {user.email}
          <button onClick={() => deleteUser(user.id)}>Delete</button>
        </li>
      ))}
    </ul>
  )
}
```

## 5. TanStack Query (React Query)

### Queries
```typescript
// hooks/useUsers.ts
import { useQuery } from "@tanstack/react-query"

interface User {
  id: string
  name: string
  email: string
}

async function fetchUsers(): Promise<User[]> {
  const response = await fetch("/api/users")
  if (!response.ok) throw new Error("Failed to fetch users")
  return response.json()
}

export function useUsers() {
  return useQuery({
    queryKey: ["users"],
    queryFn: fetchUsers,
    staleTime: 5 * 60 * 1000, // 5 minutes
    cacheTime: 10 * 60 * 1000, // 10 minutes
  })
}

// Usage
function UserList() {
  const { data: users, isLoading, error, refetch } = useUsers()

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error loading users</div>

  return (
    <div>
      <button onClick={() => refetch()}>Refresh</button>
      <ul>
        {users?.map((user) => (
          <li key={user.id}>{user.name}</li>
        ))}
      </ul>
    </div>
  )
}
```

### Dependent Queries
```typescript
// hooks/useUserTodos.ts
import { useQuery } from "@tanstack/react-query"

interface Todo {
  id: string
  text: string
  completed: boolean
}

async function fetchUserTodos(userId: string): Promise<Todo[]> {
  const response = await fetch(`/api/users/${userId}/todos`)
  if (!response.ok) throw new Error("Failed to fetch todos")
  return response.json()
}

export function useUserTodos(userId: string | undefined) {
  return useQuery({
    queryKey: ["todos", userId],
    queryFn: () => fetchUserTodos(userId!),
    enabled: !!userId, // Only run query when userId exists
  })
}
```

### Mutations
```typescript
// hooks/useCreateUser.ts
import { useMutation, useQueryClient } from "@tanstack/react-query"

interface CreateUserInput {
  name: string
  email: string
}

interface User {
  id: string
  name: string
  email: string
}

async function createUser(input: CreateUserInput): Promise<User> {
  const response = await fetch("/api/users", {
    method: "POST",
    body: JSON.stringify(input),
  })
  if (!response.ok) throw new Error("Failed to create user")
  return response.json()
}

export function useCreateUser() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: createUser,
    onSuccess: (newUser) => {
      // Invalidate and refetch users list
      queryClient.invalidateQueries({ queryKey: ["users"] })
      
      // Or update the cache directly (optimistic update)
      queryClient.setQueryData(["users"], (old: User[] | undefined) => {
        return old ? [...old, newUser] : [newUser]
      })
    },
    onError: (error) => {
      console.error("Failed to create user:", error)
    },
  })
}

// Usage
function CreateUserForm() {
  const createUser = useCreateUser()
  const [name, setName] = useState("")
  const [email, setEmail] = useState("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    createUser.mutate({ name, email })
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Name"
      />
      <input
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
      />
      <button type="submit" disabled={createUser.isPending}>
        {createUser.isPending ? "Creating..." : "Create User"}
      </button>
    </form>
  )
}
```

### Cache Management
```typescript
// hooks/useUser.ts
import { useQuery, useQueryClient } from "@tanstack/react-query"

interface User {
  id: string
  name: string
  email: string
}

async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`)
  if (!response.ok) throw new Error("Failed to fetch user")
  return response.json()
}

export function useUser(id: string) {
  const queryClient = useQueryClient()

  const query = useQuery({
    queryKey: ["user", id],
    queryFn: () => fetchUser(id),
    staleTime: 5 * 60 * 1000,
  })

  // Prefetch related data
  const prefetchUserTodos = () => {
    queryClient.prefetchQuery({
      queryKey: ["todos", id],
      queryFn: () => fetch(`/api/users/${id}/todos`).then(r => r.json()),
    })
  }

  // Invalidate related queries
  const invalidateUserQueries = () => {
    queryClient.invalidateQueries({ queryKey: ["user", id] })
    queryClient.invalidateQueries({ queryKey: ["todos", id] })
  }

  return { ...query, prefetchUserTodos, invalidateUserQueries }
}
```

### Optimistic Updates
```typescript
// hooks/useUpdateTodo.ts
import { useMutation, useQueryClient } from "@tanstack/react-query"

interface Todo {
  id: string
  text: string
  completed: boolean
}

async function updateTodo(todo: Todo): Promise<Todo> {
  const response = await fetch(`/api/todos/${todo.id}`, {
    method: "PATCH",
    body: JSON.stringify(todo),
  })
  if (!response.ok) throw new Error("Failed to update todo")
  return response.json()
}

export function useUpdateTodo() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: updateTodo,
    onMutate: async (newTodo) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: ["todos"] })

      // Snapshot previous value
      const previousTodos = queryClient.getQueryData<Todo[]>(["todos"])

      // Optimistically update to the new value
      queryClient.setQueryData<Todo[]>(["todos"], (old) =>
        old?.map((todo) => (todo.id === newTodo.id ? newTodo : todo))
      )

      // Return context with previous value
      return { previousTodos }
    },
    onError: (err, newTodo, context) => {
      // Rollback to previous value on error
      queryClient.setQueryData(["todos"], context?.previousTodos)
    },
    onSettled: () => {
      // Always refetch after error or success
      queryClient.invalidateQueries({ queryKey: ["todos"] })
    },
  })
}
```

### Infinite Queries
```typescript
// hooks/useInfiniteUsers.ts
import { useInfiniteQuery } from "@tanstack/react-query"

interface User {
  id: string
  name: string
}

interface UsersResponse {
  users: User[]
  nextCursor: string | null
}

async function fetchUsers({ pageParam }: { pageParam?: string }): Promise<UsersResponse> {
  const url = pageParam ? `/api/users?cursor=${pageParam}` : "/api/users"
  const response = await fetch(url)
  return response.json()
}

export function useInfiniteUsers() {
  return useInfiniteQuery({
    queryKey: ["users", "infinite"],
    queryFn: fetchUsers,
    initialPageParam: undefined,
    getNextPageParam: (lastPage) => lastPage.nextCursor,
  })
}

// Usage
function InfiniteUserList() {
  const {
    data,
    isLoading,
    isFetchingNextPage,
    hasNextPage,
    fetchNextPage,
  } = useInfiniteUsers()

  const users = data?.pages.flatMap((page) => page.users) || []

  return (
    <div>
      <ul>
        {users.map((user) => (
          <li key={user.id}>{user.name}</li>
        ))}
      </ul>
      <button
        onClick={() => fetchNextPage()}
        disabled={!hasNextPage || isFetchingNextPage}
      >
        {isFetchingNextPage ? "Loading more..." : "Load more"}
      </button>
    </div>
  )
}
```

## 6. Jotai (Atoms)

### Basic Atoms
```typescript
// atoms.ts
import { atom } from "jotai"

// Primitive atom
export const countAtom = atom(0)

// Read-only atom
export const doubledCountAtom = atom((get) => get(countAtom) * 2)

// Write-only atom
export const incrementAtom = atom(null, (get, set) => {
  set(countAtom, get(countAtom) + 1)
})

// Read-write atom
export const textAtom = atom("hello")
export const uppercaseTextAtom = atom(
  (get) => get(textAtom).toUpperCase(),
  (get, set, newValue) => {
    set(textAtom, newValue.toLowerCase())
  }
)
```

### Usage
```typescript
// components/Counter.tsx
"use client"

import { useAtom, useAtomValue, useSetAtom } from "jotai/react"
import { countAtom, doubledCountAtom, incrementAtom } from "@/atoms"

export function Counter() {
  const [count, setCount] = useAtom(countAtom)
  const doubled = useAtomValue(doubledCountAtom)
  const increment = useSetAtom(incrementAtom)

  return (
    <div>
      <h1>Count: {count}</h1>
      <h2>Doubled: {doubled}</h2>
      <button onClick={() => setCount((c) => c + 1)}>+</button>
      <button onClick={() => setCount((c) => c - 1)}>-</button>
      <button onClick={increment}>Increment via atom</button>
    </div>
  )
}
```

### Async Atoms
```typescript
// atoms/user.ts
import { atom } from "jotai"

interface User {
  id: string
  name: string
  email: string
}

// Base atom for user ID
export const userIdAtom = atom<string | null>(null)

// Async atom to fetch user
export const userAtom = atom(async (get) => {
  const id = get(userIdAtom)
  if (!id) return null
  
  const response = await fetch(`/api/users/${id}`)
  if (!response.ok) throw new Error("Failed to fetch user")
  return response.json()
})

// Derived atom with loading state
export const userWithLoadingAtom = atom((get) => {
  const userPromise = get(userAtom)
  return {
    user: null,
    loading: true,
    error: null,
  }
})

// Better approach with separate atoms
export const userLoadingAtom = atom(false)
export const userErrorAtom = atom<string | null>(null)
export const userDataAtom = atom<User | null>(null)

// Combined atom
export const userStateAtom = atom(
  (get) => ({
    data: get(userDataAtom),
    loading: get(userLoadingAtom),
    error: get(userErrorAtom),
  }),
  async (get, set, id: string) => {
    set(userLoadingAtom, true)
    set(userErrorAtom, null)
    try {
      const response = await fetch(`/api/users/${id}`)
      const user = await response.json()
      set(userDataAtom, user)
    } catch (error) {
      set(userErrorAtom, (error as Error).message)
    } finally {
      set(userLoadingAtom, false)
    }
  }
)
```

### Atom Families
```typescript
// atoms/todos.ts
import { atom } from "jotai"

interface Todo {
  id: string
  text: string
  completed: boolean
}

// Atom family for individual todos
export const todoAtomFamily = atom((id: string) => ({
  id,
  text: "",
  completed: false,
}))

// Atom for all todo IDs
export const todoIdsAtom = atom<string[]>([])

// Derived atom for all todos
export const todosAtom = atom((get) => {
  const ids = get(todoIdsAtom)
  return ids.map((id) => get(todoAtomFamily(id)))
})

// Actions
export const addTodoAtom = atom(null, (get, set, text: string) => {
  const id = Date.now().toString()
  set(todoIdsAtom, (ids) => [...ids, id])
  set(todoAtomFamily(id), { id, text, completed: false })
})

export const toggleTodoAtom = atom(null, (get, set, id: string) => {
  const todo = get(todoAtomFamily(id))
  set(todoAtomFamily(id), { ...todo, completed: !todo.completed })
})

export const removeTodoAtom = atom(null, (get, set, id: string) => {
  set(todoIdsAtom, (ids) => ids.filter((i) => i !== id))
})
```

## 7. Decision Matrix

### Choosing the Right Solution

```typescript
// Simple local state
function Component() {
  const [isOpen, setIsOpen] = useState(false)
  // Use for: UI toggles, form inputs, component-specific state
}

// Global state with minimal setup
function Component() {
  const { count, increment } = useCounterStore()
  // Use Zustand for: Simple global state, cross-component sharing
}

// Complex state with devtools
function Component() {
  const count = useAppSelector((state) => state.counter.value)
  const dispatch = useAppDispatch()
  // Use Redux Toolkit for: Large apps, time-travel, complex state logic
}

// Server state with caching
function Component() {
  const { data, isLoading } = useUsers()
  // Use TanStack Query for: API calls, caching, synchronization
}

// Atomic state
function Component() {
  const [count, setCount] = useAtom(countAtom)
  // Use Jotai for: Fine-grained reactivity, composable state
}
```

### Migration Guide

```typescript
// From useState to Zustand
// Before
const [count, setCount] = useState(0)

// After
const count = useCounterStore((state) => state.count)
const setCount = useCounterStore((state) => state.setCount)

// From Context to Zustand
// Before
const { user, login } = useAuth()

// After
const user = useAuthStore((state) => state.user)
const login = useAuthStore((state) => state.login)

// From useState to TanStack Query
// Before
const [users, setUsers] = useState([])
const [loading, setLoading] = useState(false)

useEffect(() => {
  setLoading(true)
  fetchUsers().then(data => {
    setUsers(data)
    setLoading(false)
  })
}, [])

// After
const { data: users, isLoading } = useUsers()
```

## 8. Best Practices per Solution

### React Context
- Split contexts to prevent unnecessary re-renders
- Use memo for expensive computations
- Consider using useReducer for complex state logic
- Keep context values as stable as possible

### Zustand
- Use selective subscriptions to prevent re-renders
- Combine related state in a single store
- Use middleware for logging, persistence, and devtools
- Keep actions simple and focused

### Redux Toolkit
- Use RTK Query for server state
- Keep slices focused and small
- Use typed hooks for type safety
- Leverage createAsyncThunk for async operations

### TanStack Query
- Use staleTime and cacheTime appropriately
- Implement optimistic updates for better UX
- Use query keys consistently
- Handle errors gracefully with error boundaries

### Jotai
- Keep atoms small and focused
- Use atom families for collections
- Leverage derived atoms for computed values
- Use useAtomValue and useSetAtom for optimization
