# Next.js Development Patterns

## App Router Structure
```
app/
├── (auth)/
│   ├── login/
│   └── register/
├── (dashboard)/
│   └── layout.tsx
└── api/
    └── [...]/route.ts
```

## Server vs Client Components
- Default: Server Component
- ใช้ "use client" เมื่อ:
  - ต้องการ useState, useEffect
  - ต้องการ event handlers
  - ต้องการ browser APIs

## Data Fetching
```typescript
// Server Component
async function getData() {
  const res = await fetch('...', { 
    cache: 'no-store' // or 'force-cache'
  });
  return res.json();
}
```

## API Routes Pattern
```typescript
// app/api/users/route.ts
export async function GET(request: Request) {
  try {
    const data = await prisma.user.findMany();
    return Response.json({ success: true, data });
  } catch (error) {
    return Response.json(
      { success: false, error: 'Internal error' },
      { status: 500 }
    );
  }
}
```