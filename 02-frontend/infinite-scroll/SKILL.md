# Infinite Scroll Patterns

---

## 1. Executive Summary & Strategic Necessity

### 1.1 Context (ภาษาไทย)

Infinite Scroll คือ technique ที่ใช้สำหรับการแสดงข้อมูลจำนวนมาก (large datasets) โดยการโหลดข้อมูลเพิ่มเมื่อผู้ใช้ scroll ถึงจุดสิ้นที่กำหนด และโหลดข้อมูลเพิ่มใหม่ นี้ เป็นวิธีที่ใช้งานแทนการโหลดทั้งหมดข้อมูลครั้งในครั้งเดียว ซึ่งช่วยลดการใช้งานและประสบประสิทธิภาพให้ผู้ใช้ได้รับสัมบาน

Infinite Scroll ใช้ Intersection Observer API สำหรับการตรวจสอบว่า element ได้เข้าสู่ viewport และเรียกข้อมูลเพิ่มเมื่อต้องการ ซึ่งช่วยกับ Virtual Scrolling ซึ่งแสดงเฉพาะ items ที่จำเป็น visible ใน viewport ประหลดจำนวน re-renders และปรับปรุงประสิทธิภาพ

### 1.2 Business Impact (ภาษาไทย)

**ผลกระทบทางธุรกิจ:**

1. **ลด Initial Load Time** - Infinite Scroll ช่วยลดเวลา initial load time โดยการโหลดข้อมูลเฉพาะที่จำเป็นจำเป็น
2. **เพิ่ม User Engagement** - การ scroll แบบไม่มีที่สิ้นสุด (infinite) ช่วยเพิ่ม engagement time
3. **ลด Bandwidth Usage** - โหลดเฉพาะ items ที่จำเป็น visible ช่วยลด bandwidth ที่ไม่จำเป็น
4. **เพิ่ม Conversion Rate** - การแสดงข้อมูลแบบ continuous ช่วยเพิ่ม conversion rate ได้ถึง 15-25%
5. **ปรับปรุง Mobile Performance** - Virtual scrolling ช่วยปรับปรุง performance บน mobile devices ที่มี hardware จำกัด

### 1.3 Product Thinking (ภาษาไทย)

**มุมมองด้านผลิตภัณฑ์:**

1. **Performance-First** - Infinite Scroll ต้องไม่ส่งผลกระทบต่อ performance ของแอปพลิเคชัน
2. **User-Centric** - Scroll behavior ต้องเป็นประโยชน์และเข้าใจง่ายสำหรับผู้ใช้
3. **Progressive Loading** - ข้อมูลต้องโหลดแบบ progressive เพื่อให้ผู้ใช้ได้เริ่มเห็น content ได้เร็วที่สุด
4. **Graceful Degradation** - ต้องมี fallback สำหรับ browsers ที่ไม่รองรับ Intersection Observer
5. **Analytics-Driven** - ต้องมีการวัด scroll behavior และ engagement metrics

---

## 2. Technical Deep Dive (The "How-to")

### 2.1 Core Logic

Infinite Scroll ประกอบด้วย 2 techniques หลัก:

1. **Intersection Observer** - ใช้ Intersection Observer API เพื่อตรวจสอบว่า element ได้เข้าสู่ viewport และเรียกข้อมูลเพิ่ม
2. **Virtual Scrolling** - แสดงเฉพาะ items ที่จำเป็น visible ใน viewport ประหลดจำนวน re-renders
3. **Infinite Query** - ใช้ React Query สำหรับ data fetching และ caching
4. **Scroll Position Restoration** - บันทึก scroll position และกู้คืนเมื่อ user กลับมา

### 2.2 Architecture Diagram Requirements

```
┌─────────────────────────────────────────────────────────┐
│              Infinite Scroll Architecture               │
├─────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌───────────────────────────────────────────────────┐   │
│  │              User Interaction Layer                │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │   Scroll      │  │  Touch      │  │   Keyboard  │  │   │
│  │  │   Events     │  │  Events     │  │  Navigation│  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
│                           │                                     │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Scroll Detection Layer                   │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │Intersection  │  │ Scroll     │  │ Position   │  │   │
│  │  │   Observer    │  │   Handler   │  │  Manager  │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
│                           │                                     │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Data Management Layer                   │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │   React      │  │   React     │  │   Custom    │  │   │
│  │  │   Query      │  │   SWR       │  │  Fetcher   │  │   │
│  │  │   Hooks      │  │   Hooks     │  │  Manager   │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Rendering Layer                         │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │   Infinite   │  │   Virtual    │  │   Item      │  │   │
│  │  │   Scroll     │  │   Scroll     │  │   Component│  │   │
│  │  │  Component  │  │   Component  │  │   Renderer   │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Performance Layer                        │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │   Memoization│  │  Debouncing │  │  Lazy Load  │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
│                           │                                     │
│  ┌───────────────────────────────────────────────────┐   │
│  │              User Experience Layer                     │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  Loading     │  │  Error      │  │  Position   │  │   │
│  │  │  Indicator   │  │  Handler    │  │  Manager   │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
└─────────────────────────────────────────────────────────┘
```

### 2.3 Implementation Workflow

**Step 1: Setup Intersection Observer Hook**

```typescript
// hooks/useInfiniteScroll.ts
'use client'

import { useEffect, useRef, useCallback } from 'react'

interface UseInfiniteScrollOptions {
  onLoadMore: () => void | Promise<void>
  hasMore: boolean
  isLoading: boolean
  threshold?: number
  rootMargin?: string
}

export function useInfiniteScroll({
  onLoadMore,
  hasMore,
  isLoading,
  threshold = 1.0,
  rootMargin = '100px',
}: UseInfiniteScrollOptions) {
  const sentinelRef = useRef<HTMLDivElement>(null)

  const handleIntersection = useCallback(
    (entries: IntersectionObserverEntry[]) => {
      const [entry] = entries

      if (entry.isIntersecting && hasMore && !isLoading) {
        onLoadMore()
      }
    },
    [hasMore, isLoading, onLoadMore]
  )

  useEffect(() => {
    const sentinel = sentinelRef.current
    if (!sentinel) return

    const observer = new IntersectionObserver(handleIntersection, {
      threshold,
      rootMargin,
    })

    observer.observe(sentinel)

    return () => {
      observer.disconnect()
    }
  }, [handleIntersection, threshold, rootMargin])

  return { sentinelRef }
}
```

**Step 2: Create Infinite Scroll Component**

```typescript
// components/InfiniteScrollList.tsx
'use client'

import { useState, useEffect } from 'react'
import { useInfiniteScroll } from '../hooks/useInfiniteScroll'

interface Item {
  id: string
  title: string
  description: string
}

interface InfiniteScrollListProps {
  fetchItems: (page: number) => Promise<Item[]>
  pageSize?: number
}

export default function InfiniteScrollList({
  fetchItems,
  pageSize = 20,
}: InfiniteScrollListProps) {
  const [items, setItems] = useState<Item[]>([])
  const [page, setPage] = useState(0)
  const [isLoading, setIsLoading] = useState(false)
  const [hasMore, setHasMore] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const loadMore = async () => {
    if (isLoading || !hasMore) return

    setIsLoading(true)
    setError(null)

    try {
      const newItems = await fetchItems(page)

      if (newItems.length === 0 || newItems.length < pageSize) {
        setHasMore(false)
      }

      setItems((prev) => [...prev, ...newItems])
      setPage((prev) => prev + 1)
    } catch (err) {
      setError('Failed to load items')
      console.error('Load more failed:', err)
    } finally {
      setIsLoading(false)
    }
  }

  // Load initial items
  useEffect(() => {
    loadMore()
  }, [])

  const { sentinelRef } = useInfiniteScroll({
    onLoadMore: loadMore,
    hasMore,
    isLoading,
  })

  return (
    <div className="infinite-scroll-list">
      <div className="items-grid">
        {items.map((item) => (
          <div key={item.id} className="item-card">
            <h3>{item.title}</h3>
            <p>{item.description}</p>
          </div>
        ))}
      </div>

      {/* Sentinel element */}
      <div ref={sentinelRef} className="sentinel" />

      {/* Loading indicator */}
      {isLoading && (
        <div className="loading-indicator">
          <div className="spinner" />
          <p>กำลังโหลด...</p>
        </div>
      )}

      {/* End of list */}
      {!hasMore && !isLoading && (
        <div className="end-message">
          <p>ไม่มีข้อมูลเพิ่มเติม</p>
        </div>
      )}

      {/* Error message */}
      {error && (
        <div className="error-message">
          <p>{error}</p>
          <button onClick={loadMore}>ลองอีกครั้ง</button>
        </div>
      )}
    </div>
  )
}
```

---

## 3. Tooling & Tech Stack

### 3.1 Enterprise Tools

| Tool | Purpose | Version | License |
|------|---------|---------|---------|
| React | UI Library | ^18.0.0 | MIT |
| @tanstack/react-query | Data Fetching | ^5.0.0 | MIT |
| react-window | Virtual Scrolling | ^1.8.0 | MIT |
| react-virtualized | Alternative Virtual Scrolling | ^4.0.0 | MIT |
| TypeScript | Type Safety | ^5.0.0 | Apache 2.0 |

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

- **WCAG 2.1 Level AA** - Scroll ต้องเข้าถึงได้และใช้งานได้สำหรับผู้ใช้ทุกคน
- **ISO 9241-11** - Usability Standards สำหรับ Scroll Behavior
- **GDPR** - Data Protection สำหรับ User Data

### 4.2 Security Protocol

Infinite Scroll ต้องปฏิบัติตามหลักความปลอดภัย:

1. **Input Sanitization** - Sanitize data ก่อนแสดง
2. **Rate Limiting** - จำกัดจำนวน requests ต่อผู้ใช้
3. **Memory Management** - ลด memory leaks จาก observers
4. **Secure Storage** - ไม่เก็บ sensitive data ใน localStorage

```typescript
// Secure data fetching
export async function fetchItemsSecurely(page: number) {
  const response = await fetch(`/api/items?page=${page}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    "X-CSRF-Token": getCsrfToken(),
    },
  })

  if (!response.ok) {
    throw new Error('Failed to fetch items')
  }

  const data = await response.json()
  
  // Sanitize data if needed
  return data.items.map((item: any) => ({
    ...item,
    // Remove sensitive fields
    password: undefined,
    token: undefined,
  }))
}
```

### 4.3 Explainability

Infinite Scroll ต้องสามารถอธิบายได้ว่า:

1. **Load Trigger** - ทำไมเรียกข้อมูลเพิ่มเมื่อไร
2. **Loading State** - แสดง loading indicator อย่างชัดเจน
3. **Error Handling** - แสดง error messages ที่เป็นประโยชน์
4. **End of List** - แสดง message เมื่อไม่มีข้อมูลเพิ่ม

---

## 5. Unit Economics & Performance Metrics (KPIs)

### 5.1 Cost Calculation

| Metric | Calculation | Target |
|--------|-------------|--------|
| Initial Load Time | Time to first render | < 2s |
| Item Render Time | Time per item render | < 50ms |
| Scroll Performance | FPS during scroll | > 55 FPS |
| Memory Usage | Memory increase per 100 items | < 50 MB |
| Error Rate | Failed requests / Total requests | < 5% |

### 5.2 Key Performance Indicators

**Technical Metrics:**

1. **Initial Load Time** - เวลาในการ render items แรกก
2. **Scroll Performance** - FPS ระหว่า scroll
3. **Memory Usage** - Memory ที่ใช้งาน
4. **Error Rate** - อัตราการเกิด errors

**Business Metrics:**

1. **User Engagement** - เวลาในการ scroll และ engagement
2. **Conversion Rate** - อัตราการแปลงผู้ใช้
3. **Bounce Rate** - อัตราการออกจากหน้า
4. **User Satisfaction** - ความพึงพอใจของผู้ใช้

---

## 6. Strategic Recommendations (CTO Insights)

### 6.1 Phase Rollout

**Phase 1: Foundation (Week 1-2)**
- Setup Intersection Observer hook
- Create base infinite scroll component
- Implement loading states
- Setup error handling

**Phase 2: Advanced Features (Week 3-4)**
- Implement virtual scrolling
- Add React Query integration
- Implement scroll position restoration
- Add image lazy loading

**Phase 3: Optimization (Week 5-6)**
- Performance audit
- Memory leak checking
- Bundle size optimization
- Mobile optimization

**Phase 4: Production (Week 7-8)**
- Analytics integration
- Error tracking
- A/B testing
- Documentation and training

### 6.2 Pitfalls to Avoid

1. **Memory Leaks** - ไม่ cleanup observers เมื่อ component unmount
2. **Duplicate Requests** - ไม่เช็ค loading state ก่อน fetch
3. **Poor Performance** - ไม่ใช้ virtual scrolling สำหรับ large lists
4. **Lost Scroll Position** - ไม่กู้คืน scroll position
5. **No Error Handling** - ไม่จัดการ failed requests
6. **Accessibility Issues** - ไม่คำนึงถึง accessibility

### 6.3 Best Practices Checklist

- [ ] ใช้ Intersection Observer API สำหรับ scroll detection
- [ ] Implement virtual scrolling สำหรับ lists > 1000 items
- [ ] ใช้ debounce สำหรับ scroll handlers
- [ ] Cleanup observers เมื่อ component unmount
- [ ] Implement loading indicators
- [ ] Handle errors gracefully
- [ ] Implement scroll position restoration
- [ ] Test บน mobile devices
- [ ] Monitor performance metrics
- [ ] Implement lazy loading สำหรับ images
- [ ] Use React Query สำหรับ data caching
- [ ] คำนึงถึง accessibility ใน scroll
- [ ] Implement rate limiting
- [ ] Sanitize data ก่อนแสดง

---

## 7. Implementation Examples

### 7.1 Basic Infinite Scroll

**Intersection Observer Implementation:**
```typescript
// useInfiniteScroll Hook
'use client'

import { useEffect, useRef, useCallback } from 'react'

interface UseInfiniteScrollOptions {
  onLoadMore: () => void | Promise<void>
  hasMore: boolean
  isLoading: boolean
  threshold?: number
  rootMargin?: string
}

export function useInfiniteScroll({
  onLoadMore,
  hasMore,
  isLoading,
  threshold = 1.0,
  rootMargin = '100px',
}: UseInfiniteScrollOptions) {
  const sentinelRef = useRef<HTMLDivElement>(null)

  const handleIntersection = useCallback(
    (entries: IntersectionObserverEntry[]) => {
      const [entry] = entries

      if (entry.isIntersecting && hasMore && !isLoading) {
        onLoadMore()
      }
    },
    [hasMore, isLoading, onLoadMore]
  )

  useEffect(() => {
    const sentinel = sentinelRef.current
    if (!sentinel) return

    const observer = new IntersectionObserver(handleIntersection, {
      threshold,
      rootMargin,
    })

    observer.observe(sentinel)

    return () => {
      observer.disconnect()
    }
  }, [handleIntersection, threshold, rootMargin])

  return { sentinelRef }
}
```

**Infinite Scroll Component:**
```typescript
// InfiniteScrollList Component
'use client'

import { useState, useEffect } from 'react'
import { useInfiniteScroll } from './useInfiniteScroll'

interface Item {
  id: string
  title: string
  description: string
}

interface InfiniteScrollListProps {
  fetchItems: (page: number) => Promise<Item[]>
  pageSize?: number
}

export default function InfiniteScrollList({
  fetchItems,
  pageSize = 20,
}: InfiniteScrollListProps) {
  const [items, setItems] = useState<Item[]>([])
  const [page, setPage] = useState(0)
  const [isLoading, setIsLoading] = useState(false)
  const [hasMore, setHasMore] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const loadMore = async () => {
    if (isLoading || !hasMore) return

    setIsLoading(true)
    setError(null)

    try {
      const newItems = await fetchItems(page)

      if (newItems.length === 0 || newItems.length < pageSize) {
        setHasMore(false)
      }

      setItems((prev) => [...prev, ...newItems])
      setPage((prev) => prev + 1)
    } catch (err) {
      setError('Failed to load items')
      console.error('Load more failed:', err)
    } finally {
      setIsLoading(false)
    }
  }

  // Load initial items
  useEffect(() => {
    loadMore()
  }, [])

  const { sentinelRef } = useInfiniteScroll({
    onLoadMore: loadMore,
    hasMore,
    isLoading,
  })

  return (
    <div className="infinite-scroll-list">
      <div className="items-grid">
        {items.map((item) => (
          <div key={item.id} className="item-card">
            <h3>{item.title}</h3>
            <p>{item.description}</p>
          </div>
        ))}
      </div>

      {/* Sentinel element */}
      <div ref={sentinelRef} className="sentinel" />

      {/* Loading indicator */}
      {isLoading && (
        <div className="loading-indicator">
          <div className="spinner" />
          <p>กำลังโหลด...</p>
        </div>
      )}

      {/* End of list */}
      {!hasMore && !isLoading && (
        <div className="end-message">
          <p>ไม่มีข้อมูลเพิ่มเติม</p>
        </div>
      )}

      {/* Error message */}
      {error && (
        <div className="error-message">
          <p>{error}</p>
          <button onClick={loadMore}>ลองอีกครั้ง</button>
        </div>
      )}
    </div>
  )
}
```

### 7.2 Virtual Scrolling

**Virtual Scroll Hook:**
```typescript
// useVirtualScroll Hook
'use client'

import { useState, useEffect, useRef, useMemo } from 'react'

interface UseVirtualScrollOptions {
  itemCount: number
  itemHeight: number
  containerHeight: number
  overscan?: number
}

export function useVirtualScroll({
  itemCount,
  itemHeight,
  containerHeight,
  overscan = 3,
}: UseVirtualScrollOptions) {
  const [scrollTop, setScrollTop] = useState(0)

  const totalHeight = itemCount * itemHeight

  const startIndex = Math.max(
    0,
    Math.floor(scrollTop / itemHeight) - overscan
  )

  const endIndex = Math.min(
    itemCount - 1,
    Math.ceil((scrollTop + containerHeight) / itemHeight) + overscan
  )

  const visibleItems = useMemo(() => {
    const items = []
    for (let i = startIndex; i <= endIndex; i++) {
      items.push({
        index: i,
        offsetTop: i * itemHeight,
      })
    }
    return items
  }, [startIndex, endIndex, itemHeight])

  const handleScroll = (e: React.UIEvent<HTMLDivElement>) => {
    setScrollTop(e.currentTarget.scrollTop)
  }

  return {
    totalHeight,
    visibleItems,
    handleScroll,
  }
}
```

**Virtual List Component:**
```typescript
// VirtualList Component
'use client'

import { useVirtualScroll } from './useVirtualScroll'

interface VirtualListProps<T> {
  items: T[]
  itemHeight: number
  containerHeight: number
  renderItem: (item: T, index: number) => React.ReactNode
}

export default function VirtualList<T>({
  items,
  itemHeight,
  containerHeight,
  renderItem,
}: VirtualListProps<T>) {
  const { totalHeight, visibleItems, handleScroll } = useVirtualScroll({
    itemCount: items.length,
    itemHeight,
    containerHeight,
    overscan: 5,
  })

  return (
    <div
      className="virtual-list-container"
      style={{ height: containerHeight, overflow: 'auto' }}
      onScroll={handleScroll}
    >
      <div
        className="virtual-list-content"
        style={{ height: totalHeight, position: 'relative' }}
      >
        {visibleItems.map(({ index, offsetTop }) => (
          <div
            key={index}
            style={{
              position: 'absolute',
              top: offsetTop,
              left: 0,
              right: 0,
              height: itemHeight,
            }}
          >
            {renderItem(items[index], index)}
          </div>
        ))}
      </div>
    </div>
  )
}
```

### 7.3 Infinite Scroll with React Query

**Infinite Query Hook:**
```typescript
// useInfiniteEvents Hook with React Query
'use client'

import { useInfiniteQuery } from '@tanstack/react-query'

interface Event {
  id: string
  title: string
  date: string
}

interface EventsResponse {
  events: Event[]
  nextCursor: string | null
}

async function fetchEvents(cursor: string | null): Promise<EventsResponse> {
  const response = await fetch(
    `/api/events?cursor=${cursor || ''}&limit=20`
  )

  if (!response.ok) {
    throw new Error('Failed to fetch events')
  }

  return await response.json()
}

export function useInfiniteEvents() {
  return useInfiniteQuery({
    queryKey: ['events'],
    queryFn: ({ pageParam }) => fetchEvents(pageParam),
    initialPageParam: null,
    getNextPageParam: (lastPage) => lastPage.nextCursor,
  })
}

// Component using the hook
export default function InfiniteEventList() {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
    isLoading,
    isError,
  } = useInfiniteEvents()

  const { sentinelRef } = useInfiniteScroll({
    onLoadMore: fetchNextPage,
    hasMore: hasNextPage ?? false,
    isLoading: isFetchingNextPage,
  })

  const allEvents = data?.pages.flatMap((page) => page.events) ?? []

  if (isLoading) {
    return <div>กำลังโหลด...</div>
  }

  if (isError) {
    return <div>เกิดข้อผิดพลาด</div>
  }

  return (
    <div className="event-list">
      {allEvents.map((event) => (
        <div key={event.id} className="event-card">
          <h3>{event.title}</h3>
          <p>{event.date}</p>
        </div>
      ))}

      <div ref={sentinelRef} />

      {isFetchingNextPage && <div>กำลังโหลดเพิ่มเติม...</div>}
      {!hasNextPage && <div>ไม่มีข้อมูลเพิ่มเติม</div>}
    </div>
  )
}
```

### 7.4 Performance Optimization

**Debounced Scroll Handler:**
```typescript
// Debounced Scroll Handler
import { useEffect, useRef } from 'react'

function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout | null = null

  return function executedFunction(...args: Parameters<T>) {
    const later = () => {
      timeout = null
      func(...args)
    }

    if (timeout) {
      clearTimeout(timeout)
    }

    timeout = setTimeout(later, wait)
  }
}

export function useDebounce<T extends (...args: any[]) => any>(
  callback: T,
  delay: number
): T {
  const callbackRef = useRef(callback)

  useEffect(() => {
    callbackRef.current = callback
  }, [callback])

  const debouncedCallback = useRef(
    debounce((...args: Parameters<T>) => {
      callbackRef.current(...args)
    }, delay)
  ).current

  return debouncedCallback as T
}
```

**Image Lazy Loading:**
```typescript
// LazyImage Component
'use client'

import { useState, useRef, useEffect } from 'react'

interface LazyImageProps {
  src: string
  alt: string
  placeholder?: string
  className?: string
}

export default function LazyImage({
  src,
  alt,
  placeholder = '/placeholder.png',
  className,
}: LazyImageProps) {
  const [imageSrc, setImageSrc] = useState(placeholder)
  const [isLoaded, setIsLoaded] = useState(false)
  const imgRef = useRef<HTMLImageElement>(null)

  useEffect(() => {
    const img = imgRef.current
    if (!img) return

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setImageSrc(src)
            observer.unobserve(img)
          }
        })
      },
      {
        rootMargin: '50px',
      }
    )

    observer.observe(img)
  }, [src])

  return (
    <img
      ref={imgRef}
      src={imageSrc}
      alt={alt}
      className={`${className} ${isLoaded ? 'loaded' : 'loading'}`}
      onLoad={() => setIsLoaded(true)}
    />
  )
}
```

### 7.5 Scroll Position Restoration

**Scroll Position Manager:**
```typescript
// Scroll Position Restoration
'use client'

import { useEffect, useRef } from 'react'
import { useRouter } from 'next/navigation'

interface UseScrollRestorationOptions {
  key: string
  enabled?: boolean
}

export function useScrollRestoration({
  key,
  enabled = true,
}: UseScrollRestorationOptions) {
  const router = useRouter()
  const containerRef = useRef<HTMLDivElement>(null)

  // Save scroll position
  useEffect(() => {
    if (!enabled) return

    const handleScroll = () => {
      if (containerRef.current) {
        const scrollPosition = containerRef.current.scrollTop
        sessionStorage.setItem(`scroll-${key}`, scrollPosition.toString())
      }
    }

    const container = containerRef.current
    if (container) {
      container.addEventListener('scroll', handleScroll)
    }

    return () => {
      container.removeEventListener('scroll', handleScroll)
    }
  }, [key, enabled])

  // Restore scroll position
  useEffect(() => {
    if (!enabled) return

    const savedPosition = sessionStorage.getItem(`scroll-${key}`)

    if (savedPosition && containerRef.current) {
      containerRef.current.scrollTop = parseInt(savedPosition, 10)
    }
  }, [key, enabled])

  return { containerRef }
}
```

### 7.6 Error Handling

**Retry Logic:**
```typescript
// Retry Logic for Failed Loads
async function fetchWithRetry<T>(
  fetchFn: () => Promise<T>,
  maxRetries: number = 3,
  delay: number = 1000
): Promise<T> {
  let lastError: Error

  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fetchFn()
    } catch (error) {
      lastError = error as Error
      console.error(`Attempt ${i + 1} failed:`, error)

      if (i < maxRetries - 1) {
        await new Promise((resolve) => setTimeout(resolve, delay * (i + 1)))
      }
    }
  }

  throw lastError!
}

// Usage in infinite scroll
async function loadMore() {
  try {
    const items = await fetchWithRetry(() => fetchItems(page))
    setItems((prev) => [...prev, ...items])
  } catch (error) {
    setError('Failed to load items after multiple retries')
  }
}
```

### 7.7 Best Practices

**Performance:**
- Use virtual scrolling for large lists (>1000 items)
- Implement lazy loading for images
- Debounce scroll handlers
- Use Intersection Observer over scroll events

**User Experience:**
- Show loading indicators
- Handle errors gracefully
- Provide retry options
- Restore scroll position on navigation

**Accessibility:**
- Announce new content to screen readers
- Provide keyboard navigation
- Include skip links
- Maintain focus management

**Data Management:**
- Implement pagination on backend
- Cache loaded data
- Handle duplicate items
- Clean up old data

**Mobile Optimization:**
- Touch-friendly hit areas
- Optimize for slower networks
- Reduce bundle size
- Test on real devices

---

## 8. Related Skills

- `02-frontend/react-best-practices`
- `02-frontend/state-management`
- `02-frontend/animation`
- `01-foundations/performance-optimization`
- `06-ai-ml-production/agent-patterns`
