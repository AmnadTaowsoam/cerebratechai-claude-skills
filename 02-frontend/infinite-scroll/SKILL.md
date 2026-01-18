# Infinite Scroll Patterns

## Overview

Implementation patterns for infinite scroll and virtual scrolling in web applications. This skill covers Intersection Observer API, virtual scrolling, performance optimization, loading states, and best practices for handling large datasets.

---

## 1. Infinite Scroll Architecture

### Infinite Scroll Concepts

```markdown
# Infinite Scroll Architecture

## Components
1. **Scroll Container**: Main scrollable area
2. **Item List**: Rendered items
3. **Sentinel Element**: Trigger for loading more
4. **Loading Indicator**: Shows loading state
5. **Data Fetcher**: Loads more data
6. **State Manager**: Manages scroll state

## Flow
```
User Scrolls → Sentinel Visible → Fetch Data → Append Items → Repeat
                    ↓
            Intersection Observer
                    ↓
            Loading Indicator
```

## Use Cases
- Social media feeds
- Product listings
- Search results
- News articles
- Image galleries
```

---

## 2. Basic Infinite Scroll

### Intersection Observer Implementation

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

### Infinite Scroll Component

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

---

## 3. Virtual Scrolling

### Virtual List Implementation

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

### Virtual List Component

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

// Usage Example
function EventList() {
  const events = [...] // Large array of events

  return (
    <VirtualList
      items={events}
      itemHeight={100}
      containerHeight={600}
      renderItem={(event, index) => (
        <div className="event-card">
          <h3>{event.title}</h3>
          <p>{event.date}</p>
        </div>
      )}
    />
  )
}
```

---

## 4. Advanced Patterns

### Infinite Scroll with React Query

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

  if (isLoading) {
    return <div>กำลังโหลด...</div>
  }

  if (isError) {
    return <div>เกิดข้อผิดพลาด</div>
  }

  const allEvents = data?.pages.flatMap((page) => page.events) ?? []

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

### Bidirectional Infinite Scroll

```typescript
// Bidirectional Infinite Scroll
'use client'

import { useState, useRef, useCallback } from 'react'

interface UseBidirectionalScrollOptions {
  onLoadMore: (direction: 'up' | 'down') => Promise<void>
  hasMoreUp: boolean
  hasMoreDown: boolean
  isLoading: boolean
}

export function useBidirectionalScroll({
  onLoadMore,
  hasMoreUp,
  hasMoreDown,
  isLoading,
}: UseBidirectionalScrollOptions) {
  const topSentinelRef = useRef<HTMLDivElement>(null)
  const bottomSentinelRef = useRef<HTMLDivElement>(null)
  const containerRef = useRef<HTMLDivElement>(null)

  const handleTopIntersection = useCallback(
    (entries: IntersectionObserverEntry[]) => {
      const [entry] = entries

      if (entry.isIntersecting && hasMoreUp && !isLoading) {
        const previousScrollHeight = containerRef.current?.scrollHeight || 0

        onLoadMore('up').then(() => {
          // Maintain scroll position
          if (containerRef.current) {
            const newScrollHeight = containerRef.current.scrollHeight
            const scrollDiff = newScrollHeight - previousScrollHeight
            containerRef.current.scrollTop += scrollDiff
          }
        })
      }
    },
    [hasMoreUp, isLoading, onLoadMore]
  )

  const handleBottomIntersection = useCallback(
    (entries: IntersectionObserverEntry[]) => {
      const [entry] = entries

      if (entry.isIntersecting && hasMoreDown && !isLoading) {
        onLoadMore('down')
      }
    },
    [hasMoreDown, isLoading, onLoadMore]
  )

  // Setup observers
  useEffect(() => {
    const topSentinel = topSentinelRef.current
    const bottomSentinel = bottomSentinelRef.current

    if (!topSentinel || !bottomSentinel) return

    const topObserver = new IntersectionObserver(handleTopIntersection, {
      threshold: 1.0,
    })

    const bottomObserver = new IntersectionObserver(handleBottomIntersection, {
      threshold: 1.0,
    })

    topObserver.observe(topSentinel)
    bottomObserver.observe(bottomSentinel)

    return () => {
      topObserver.disconnect()
      bottomObserver.disconnect()
    }
  }, [handleTopIntersection, handleBottomIntersection])

  return { topSentinelRef, bottomSentinelRef, containerRef }
}
```

---

## 5. Performance Optimization

### Debounced Scroll Handler

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

### Image Lazy Loading

```typescript
// Image Lazy Loading Component
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

    return () => {
      observer.disconnect()
    }
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

---

## 6. Scroll Position Restoration

### Scroll Position Manager

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

      return () => {
        container.removeEventListener('scroll', handleScroll)
      }
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

---

## 7. Error Handling

### Retry Logic

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

---

## Best Practices

1. **Performance**
   - Use virtual scrolling for large lists (>1000 items)
   - Implement lazy loading for images
   - Debounce scroll handlers
   - Use Intersection Observer over scroll events

2. **User Experience**
   - Show loading indicators
   - Handle errors gracefully
   - Provide retry options
   - Restore scroll position on navigation

3. **Accessibility**
   - Announce new content to screen readers
   - Provide keyboard navigation
   - Include skip links
   - Maintain focus management

4. **Data Management**
   - Implement pagination on backend
   - Cache loaded data
   - Handle duplicate items
   - Clean up old data

5. **Mobile Optimization**
   - Touch-friendly hit areas
   - Optimize for slower networks
   - Reduce bundle size
   - Test on real devices

---

## Common Pitfalls

1. **Memory Leaks**: Not cleaning up observers
2. **Duplicate Requests**: Not checking loading state
3. **Poor Performance**: Rendering too many items
4. **Lost Scroll Position**: Not restoring on navigation
5. **No Error Handling**: Not handling failed requests

---

## Production Checklist

- [ ] Intersection Observer implemented
- [ ] Loading states handled
- [ ] Error handling comprehensive
- [ ] Scroll position restoration
- [ ] Performance optimized
- [ ] Accessibility verified
- [ ] Mobile tested
- [ ] Analytics tracking
- [ ] Memory leaks checked
- [ ] Edge cases handled

---

## Tools & Libraries

| Tool | Purpose |
|------|---------|
| react-window | Virtual scrolling |
| react-virtualized | Alternative virtual scrolling |
| @tanstack/react-query | Data fetching and caching |
| intersection-observer | Polyfill for older browsers |

---

## Further Reading

- [Intersection Observer API](https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API)
- [Virtual Scrolling](https://web.dev/virtualize-long-lists-react-window/)
- [Infinite Scroll Best Practices](https://www.smashingmagazine.com/2013/05/infinite-scrolling-lets-get-to-the-bottom-of-this/)
- [React Query Infinite Queries](https://tanstack.com/query/latest/docs/react/guides/infinite-queries)
