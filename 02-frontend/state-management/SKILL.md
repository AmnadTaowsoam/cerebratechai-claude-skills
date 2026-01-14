# State Management Patterns

## Overview
เลือก state management ตามความซับซ้อนของ app

## Options & When to Use

### 1. React Context (Simple)
**Use for**: Theme, Auth, Locale
```typescript
const AuthContext = createContext<AuthContextType | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  
  return (
    <AuthContext.Provider value={{ user, setUser }}>
      {children}
    </AuthContext.Provider>
  )
}
```

### 2. Zustand (Medium Complexity)
**Use for**: Client state, Simple global state
```typescript
import create from 'zustand'

interface UserStore {
  user: User | null
  setUser: (user: User) => void
  logout: () => void
}

export const useUserStore = create<UserStore>((set) => ({
  user: null,
  setUser: (user) => set({ user }),
  logout: () => set({ user: null }),
}))

// Usage
function Profile() {
  const user = useUserStore((state) => state.user)
  const logout = useUserStore((state) => state.logout)
}
```

### 3. Redux Toolkit (Complex)
**Use for**: Large apps, Time-travel debugging
```typescript
import { createSlice, configureStore } from '@reduxjs/toolkit'

const userSlice = createSlice({
  name: 'user',
  initialState: { user: null },
  reducers: {
    setUser: (state, action) => {
      state.user = action.payload
    },
  },
})

export const store = configureStore({
  reducer: { user: userSlice.reducer },
})
```

### 4. TanStack Query (Server State)
**Use for**: API data, Caching
```typescript
import { useQuery, useMutation } from '@tanstack/react-query'

function Users() {
  const { data, isLoading } = useQuery({
    queryKey: ['users'],
    queryFn: fetchUsers,
  })
  
  const mutation = useMutation({
    mutationFn: createUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] })
    },
  })
}
```

## Decision Matrix

| State Type | Tool | Example |
|------------|------|---------|
| UI State | useState/useReducer | Modal open/close |
| Shared UI | Context/Zustand | Theme, Sidebar |
| Server Data | TanStack Query | API responses |
| Complex Logic | Redux Toolkit | Shopping cart |
| Form State | React Hook Form | Form fields |

## Best Practices
- Separate server state from client state
- Use TanStack Query for API calls
- Avoid prop drilling with Context
- Keep state close to where it's used
- Use TypeScript for type safety