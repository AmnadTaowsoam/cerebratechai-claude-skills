---
name: Real-time Dashboard
description: Displaying live data updates using WebSocket or SSE for real-time dashboards, including architecture, data streaming, state management, and React implementation patterns.
---

# Real-time Dashboard

> **Current Level:** Intermediate  
> **Domain:** Real-time / Frontend / Analytics

---

## Overview

Real-time dashboards display live data updates using WebSocket or SSE. This guide covers architecture, data streaming, and React implementation patterns for building dashboards that update in real-time without page refreshes.

## Architecture

```
Data Sources → Backend → WebSocket/SSE → Frontend → Charts
     ↓            ↓                           ↓
  Database    Aggregation                State Management
```

## WebSocket Integration

```typescript
// server/dashboard-socket.service.ts
import { Server, Socket } from 'socket.io';

export class DashboardSocketService {
  constructor(private io: Server) {
    this.setupHandlers();
  }

  private setupHandlers(): void {
    this.io.on('connection', (socket) => {
      console.log('Dashboard client connected');

      socket.on('subscribe-metrics', (dashboardId: string) => {
        socket.join(`dashboard:${dashboardId}`);
        this.sendInitialData(socket, dashboardId);
      });

      socket.on('unsubscribe-metrics', (dashboardId: string) => {
        socket.leave(`dashboard:${dashboardId}`);
      });

      socket.on('disconnect', () => {
        console.log('Dashboard client disconnected');
      });
    });
  }

  private async sendInitialData(socket: Socket, dashboardId: string): Promise<void> {
    const metrics = await this.getMetrics(dashboardId);
    socket.emit('initial-data', metrics);
  }

  async broadcastMetrics(dashboardId: string, metrics: Metrics): Promise<void> {
    this.io.to(`dashboard:${dashboardId}`).emit('metrics-update', metrics);
  }

  private async getMetrics(dashboardId: string): Promise<Metrics> {
    // Fetch from database or cache
    return {
      activeUsers: 1234,
      revenue: 50000,
      orders: 89,
      timestamp: Date.now()
    };
  }
}

interface Metrics {
  activeUsers: number;
  revenue: number;
  orders: number;
  timestamp: number;
}
```

## Data Streaming

```typescript
// services/metrics-stream.service.ts
export class MetricsStreamService {
  private intervals = new Map<string, NodeJS.Timeout>();

  startStreaming(dashboardId: string, interval: number = 5000): void {
    if (this.intervals.has(dashboardId)) {
      return; // Already streaming
    }

    const timer = setInterval(async () => {
      const metrics = await this.collectMetrics(dashboardId);
      await dashboardSocketService.broadcastMetrics(dashboardId, metrics);
    }, interval);

    this.intervals.set(dashboardId, timer);
  }

  stopStreaming(dashboardId: string): void {
    const timer = this.intervals.get(dashboardId);
    if (timer) {
      clearInterval(timer);
      this.intervals.delete(dashboardId);
    }
  }

  private async collectMetrics(dashboardId: string): Promise<Metrics> {
    const [users, revenue, orders] = await Promise.all([
      this.getActiveUsers(),
      this.getRevenue(),
      this.getOrders()
    ]);

    return {
      activeUsers: users,
      revenue,
      orders,
      timestamp: Date.now()
    };
  }

  private async getActiveUsers(): Promise<number> {
    // Query from Redis or database
    return Math.floor(Math.random() * 2000);
  }

  private async getRevenue(): Promise<number> {
    // Query from database
    return Math.floor(Math.random() * 100000);
  }

  private async getOrders(): Promise<number> {
    // Query from database
    return Math.floor(Math.random() * 200);
  }
}
```

## Live Charts

```typescript
// components/LiveChart.tsx
import { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

interface DataPoint {
  timestamp: number;
  value: number;
}

interface LiveChartProps {
  title: string;
  dataKey: string;
  maxDataPoints?: number;
}

export function LiveChart({ title, dataKey, maxDataPoints = 20 }: LiveChartProps) {
  const [dataPoints, setDataPoints] = useState<DataPoint[]>([]);

  useEffect(() => {
    const socket = getSocket();

    socket.on('metrics-update', (metrics: any) => {
      const newPoint: DataPoint = {
        timestamp: metrics.timestamp,
        value: metrics[dataKey]
      };

      setDataPoints(prev => {
        const updated = [...prev, newPoint];
        // Keep only last N points
        return updated.slice(-maxDataPoints);
      });
    });

    return () => {
      socket.off('metrics-update');
    };
  }, [dataKey, maxDataPoints]);

  const chartData = {
    labels: dataPoints.map(p => new Date(p.timestamp).toLocaleTimeString()),
    datasets: [
      {
        label: title,
        data: dataPoints.map(p => p.value),
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        tension: 0.4
      }
    ]
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    animation: {
      duration: 750
    },
    scales: {
      y: {
        beginAtZero: true
      }
    },
    plugins: {
      legend: {
        display: false
      }
    }
  };

  return (
    <div style={{ height: '300px' }}>
      <Line data={chartData} options={options} />
    </div>
  );
}
```

## Data Aggregation

```typescript
// services/data-aggregation.service.ts
export class DataAggregationService {
  async aggregateMetrics(
    startTime: Date,
    endTime: Date,
    interval: 'minute' | 'hour' | 'day'
  ): Promise<AggregatedMetrics[]> {
    const query = `
      SELECT 
        DATE_TRUNC('${interval}', timestamp) as period,
        COUNT(*) as count,
        SUM(amount) as total,
        AVG(amount) as average
      FROM metrics
      WHERE timestamp BETWEEN $1 AND $2
      GROUP BY period
      ORDER BY period
    `;

    const result = await db.query(query, [startTime, endTime]);
    return result.rows;
  }

  async getRealTimeStats(): Promise<RealTimeStats> {
    const [activeUsers, activeOrders, revenue] = await Promise.all([
      this.getActiveUserCount(),
      this.getActiveOrderCount(),
      this.getTodayRevenue()
    ]);

    return {
      activeUsers,
      activeOrders,
      revenue,
      timestamp: Date.now()
    };
  }

  private async getActiveUserCount(): Promise<number> {
    const result = await redis.get('active_users_count');
    return parseInt(result || '0');
  }

  private async getActiveOrderCount(): Promise<number> {
    const count = await db.order.count({
      where: {
        status: 'processing',
        createdAt: {
          gte: new Date(Date.now() - 24 * 60 * 60 * 1000)
        }
      }
    });
    return count;
  }

  private async getTodayRevenue(): Promise<number> {
    const result = await db.order.aggregate({
      where: {
        status: 'completed',
        createdAt: {
          gte: new Date(new Date().setHours(0, 0, 0, 0))
        }
      },
      _sum: {
        total: true
      }
    });
    return result._sum.total || 0;
  }
}

interface AggregatedMetrics {
  period: Date;
  count: number;
  total: number;
  average: number;
}

interface RealTimeStats {
  activeUsers: number;
  activeOrders: number;
  revenue: number;
  timestamp: number;
}
```

## State Management

```typescript
// store/dashboard.store.ts
import create from 'zustand';

interface DashboardState {
  metrics: Metrics | null;
  history: DataPoint[];
  connected: boolean;
  loading: boolean;
  
  setMetrics: (metrics: Metrics) => void;
  addDataPoint: (key: string, value: number) => void;
  setConnected: (connected: boolean) => void;
  setLoading: (loading: boolean) => void;
  reset: () => void;
}

export const useDashboardStore = create<DashboardState>((set) => ({
  metrics: null,
  history: [],
  connected: false,
  loading: true,

  setMetrics: (metrics) => set({ metrics, loading: false }),

  addDataPoint: (key, value) => set((state) => ({
    history: [
      ...state.history,
      { timestamp: Date.now(), key, value }
    ].slice(-100) // Keep last 100 points
  })),

  setConnected: (connected) => set({ connected }),

  setLoading: (loading) => set({ loading }),

  reset: () => set({
    metrics: null,
    history: [],
    connected: false,
    loading: true
  })
}));

// Usage in component
function Dashboard() {
  const { metrics, connected, setMetrics, setConnected } = useDashboardStore();

  useEffect(() => {
    const socket = getSocket();

    socket.on('connect', () => setConnected(true));
    socket.on('disconnect', () => setConnected(false));
    socket.on('metrics-update', setMetrics);

    socket.emit('subscribe-metrics', 'main-dashboard');

    return () => {
      socket.emit('unsubscribe-metrics', 'main-dashboard');
      socket.off('metrics-update');
    };
  }, []);

  return (
    <div>
      <div>Status: {connected ? 'Connected' : 'Disconnected'}</div>
      {metrics && (
        <div>
          <MetricCard title="Active Users" value={metrics.activeUsers} />
          <MetricCard title="Revenue" value={metrics.revenue} />
          <MetricCard title="Orders" value={metrics.orders} />
        </div>
      )}
    </div>
  );
}
```

## Connection Recovery

```typescript
// hooks/useDashboardConnection.ts
import { useEffect, useState } from 'react';
import { io, Socket } from 'socket.io-client';

export function useDashboardConnection(dashboardId: string) {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [connected, setConnected] = useState(false);
  const [reconnecting, setReconnecting] = useState(false);

  useEffect(() => {
    const socketInstance = io(process.env.NEXT_PUBLIC_WS_URL!, {
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      reconnectionAttempts: Infinity
    });

    socketInstance.on('connect', () => {
      console.log('Connected to dashboard');
      setConnected(true);
      setReconnecting(false);
      
      // Resubscribe after reconnection
      socketInstance.emit('subscribe-metrics', dashboardId);
    });

    socketInstance.on('disconnect', () => {
      console.log('Disconnected from dashboard');
      setConnected(false);
    });

    socketInstance.on('reconnect_attempt', () => {
      console.log('Attempting to reconnect...');
      setReconnecting(true);
    });

    socketInstance.on('reconnect', (attemptNumber) => {
      console.log(`Reconnected after ${attemptNumber} attempts`);
      setReconnecting(false);
    });

    setSocket(socketInstance);

    return () => {
      socketInstance.close();
    };
  }, [dashboardId]);

  return { socket, connected, reconnecting };
}
```

## Caching Strategies

```typescript
// services/dashboard-cache.service.ts
import { Redis } from 'ioredis';

export class DashboardCacheService {
  private redis: Redis;

  constructor() {
    this.redis = new Redis(process.env.REDIS_URL!);
  }

  async cacheMetrics(dashboardId: string, metrics: Metrics): Promise<void> {
    const key = `dashboard:${dashboardId}:metrics`;
    await this.redis.setex(key, 60, JSON.stringify(metrics));
  }

  async getCachedMetrics(dashboardId: string): Promise<Metrics | null> {
    const key = `dashboard:${dashboardId}:metrics`;
    const cached = await this.redis.get(key);
    return cached ? JSON.parse(cached) : null;
  }

  async cacheHistoricalData(
    dashboardId: string,
    data: DataPoint[]
  ): Promise<void> {
    const key = `dashboard:${dashboardId}:history`;
    await this.redis.setex(key, 300, JSON.stringify(data));
  }

  async getHistoricalData(dashboardId: string): Promise<DataPoint[] | null> {
    const key = `dashboard:${dashboardId}:history`;
    const cached = await this.redis.get(key);
    return cached ? JSON.parse(cached) : null;
  }
}
```

## Alert System

```typescript
// services/alert.service.ts
export class AlertService {
  async checkThresholds(metrics: Metrics): Promise<Alert[]> {
    const alerts: Alert[] = [];

    // Check active users threshold
    if (metrics.activeUsers > 5000) {
      alerts.push({
        type: 'warning',
        metric: 'activeUsers',
        message: 'High number of active users',
        value: metrics.activeUsers,
        threshold: 5000
      });
    }

    // Check revenue drop
    const previousRevenue = await this.getPreviousRevenue();
    if (metrics.revenue < previousRevenue * 0.5) {
      alerts.push({
        type: 'critical',
        metric: 'revenue',
        message: 'Revenue dropped significantly',
        value: metrics.revenue,
        threshold: previousRevenue * 0.5
      });
    }

    // Notify if alerts exist
    if (alerts.length > 0) {
      await this.sendAlerts(alerts);
    }

    return alerts;
  }

  private async sendAlerts(alerts: Alert[]): Promise<void> {
    // Send via WebSocket
    io.emit('alerts', alerts);

    // Send email for critical alerts
    const criticalAlerts = alerts.filter(a => a.type === 'critical');
    if (criticalAlerts.length > 0) {
      await emailService.sendAlertEmail(criticalAlerts);
    }
  }

  private async getPreviousRevenue(): Promise<number> {
    // Get revenue from 1 hour ago
    return 45000;
  }
}

interface Alert {
  type: 'info' | 'warning' | 'critical';
  metric: string;
  message: string;
  value: number;
  threshold: number;
}
```

## Example: Metrics Dashboard

```typescript
// components/MetricsDashboard.tsx
import { useEffect } from 'react';
import { useDashboardStore } from '@/store/dashboard.store';
import { useDashboardConnection } from '@/hooks/useDashboardConnection';

export function MetricsDashboard() {
  const { metrics, connected } = useDashboardStore();
  const { socket } = useDashboardConnection('main-dashboard');

  return (
    <div className="dashboard">
      <header>
        <h1>Real-time Metrics Dashboard</h1>
        <ConnectionStatus connected={connected} />
      </header>

      <div className="metrics-grid">
        <MetricCard
          title="Active Users"
          value={metrics?.activeUsers || 0}
          icon="👥"
          trend={calculateTrend('activeUsers')}
        />
        <MetricCard
          title="Revenue"
          value={formatCurrency(metrics?.revenue || 0)}
          icon="💰"
          trend={calculateTrend('revenue')}
        />
        <MetricCard
          title="Orders"
          value={metrics?.orders || 0}
          icon="📦"
          trend={calculateTrend('orders')}
        />
      </div>

      <div className="charts-grid">
        <LiveChart title="Active Users" dataKey="activeUsers" />
        <LiveChart title="Revenue" dataKey="revenue" />
        <LiveChart title="Orders" dataKey="orders" />
      </div>
    </div>
  );
}
```

## Best Practices

1. **Connection Management** - Handle reconnection gracefully
2. **Data Throttling** - Limit update frequency
3. **Caching** - Cache metrics for performance
4. **State Management** - Use proper state management
5. **Error Handling** - Handle connection errors
6. **Performance** - Optimize chart rendering
7. **Alerts** - Implement threshold alerts
8. **Monitoring** - Monitor WebSocket health
9. **Fallback** - Provide polling fallback
10. **Testing** - Test with simulated data

---

## Quick Start

### WebSocket Dashboard

```typescript
// Server
io.on('connection', (socket) => {
  // Send initial data
  socket.emit('dashboard:data', getDashboardData())
  
  // Send updates every second
  const interval = setInterval(() => {
    socket.emit('dashboard:update', getDashboardData())
  }, 1000)
  
  socket.on('disconnect', () => {
    clearInterval(interval)
  })
})

// Client
const socket = io()

socket.on('dashboard:update', (data) => {
  setDashboardData(data)  // Update React state
})
```

---

## Production Checklist

- [ ] **WebSocket/SSE**: Set up real-time connection
- [ ] **Data Aggregation**: Aggregate data on backend
- [ ] **State Management**: Manage dashboard state
- [ ] **Chart Library**: Choose chart library (Chart.js, Recharts)
- [ ] **Performance**: Optimize chart rendering
- [ ] **Error Handling**: Handle connection errors
- [ ] **Reconnection**: Auto-reconnect on disconnect
- [ ] **Throttling**: Throttle updates if needed
- [ ] **Caching**: Cache initial data
- [ ] **Testing**: Test with real-time data
- [ ] **Monitoring**: Monitor WebSocket health
- [ ] **Fallback**: Polling fallback for old browsers

---

## Anti-patterns

### ❌ Don't: Too Frequent Updates

```typescript
// ❌ Bad - Update every millisecond
setInterval(() => {
  socket.emit('update', data)  // Too frequent!
}, 1)
```

```typescript
// ✅ Good - Throttled updates
const throttle = require('lodash/throttle')

const sendUpdate = throttle((data) => {
  socket.emit('update', data)
}, 1000)  // Max once per second
```

### ❌ Don't: No Error Handling

```typescript
// ❌ Bad - No error handling
socket.on('update', (data) => {
  setData(data)  // What if connection fails?
})
```

```typescript
// ✅ Good - Error handling
socket.on('connect', () => {
  console.log('Connected')
})

socket.on('disconnect', () => {
  console.log('Disconnected, reconnecting...')
  // Show offline indicator
})

socket.on('error', (error) => {
  console.error('Error:', error)
  // Fallback to polling
})
```

---

## Integration Points

- **WebSocket Patterns** (`34-real-time-features/websocket-patterns/`) - WebSocket implementation
- **Server-Sent Events** (`34-real-time-features/server-sent-events/`) - SSE alternative
- **Dashboard Design** (`23-business-analytics/dashboard-design/`) - Dashboard layouts

---

## Further Reading

- [Chart.js](https://www.chartjs.org/)
- [Recharts](https://recharts.org/)
- [Socket.io](https://socket.io/)

## Resources
- [Socket.IO](https://socket.io/)
- [Zustand](https://github.com/pmndrs/zustand)
