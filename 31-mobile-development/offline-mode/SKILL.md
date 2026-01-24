---
name: Offline-First Mobile App Patterns
description: Building apps that work without network connectivity by storing data locally and synchronizing when connectivity is restored, including local storage, data sync, conflict resolution, and cache strategies.
---

# Offline-First Mobile App Patterns

> **Current Level:** Advanced  
> **Domain:** Mobile Development / Architecture

---

## Overview

Offline-first apps work without network connectivity by storing data locally and synchronizing when connectivity is restored. This guide covers local storage, data sync, conflict resolution, and cache strategies for building resilient mobile applications that work in poor network conditions.

---

## Core Concepts

### Table of Contents

1. [Offline-First Concepts](#offline-first-concepts)
2. [Local Storage](#local-storage)
3. [Data Synchronization](#data-synchronization)
4. [Conflict Resolution](#conflict-resolution)
5. [Queue Management](#queue-management)
6. [Cache Strategies](#cache-strategies)
7. [Network Detection](#network-detection)
8. [Optimistic Updates](#optimistic-updates)
9. [Background Sync](#background-sync)
10. [Testing Offline Scenarios](#testing-offline-scenarios)
11. [Best Practices](#best-practices)

---

## Offline-First Concepts

### Offline-First Architecture

```typescript
enum SyncStatus {
  SYNCED = 'synced',
  PENDING = 'pending',
  CONFLICT = 'conflict',
  ERROR = 'error',
}

enum ConflictResolution {
  CLIENT_WINS = 'client_wins',
  SERVER_WINS = 'server_wins',
  MERGE = 'merge',
}
```

---

## Local Storage

### Storage Abstraction

```typescript
// src/storage/StorageService.ts
import AsyncStorage from '@react-native-async-storage/async-storage';
import { MMKV } from 'react-native-mmkv-storage';

interface StorageService {
  get<T>(key: string): Promise<T | null>;
  set<T>(key: string, value: T): Promise<void>;
  remove(key: string): Promise<void>;
  clear(): Promise<void>;
  getAllKeys(): Promise<string[]>;
}

class AsyncStorageService implements StorageService {
  async get<T>(key: string): Promise<T | null> {
    try {
      const value = await AsyncStorage.getItem(key);
      return value ? JSON.parse(value) : null;
    } catch (error) {
      console.error('Error getting from AsyncStorage:', error);
      return null;
    }
  }

  async set<T>(key: string, value: T): Promise<void> {
    try {
      await AsyncStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error('Error setting to AsyncStorage:', error);
    }
  }

  async remove(key: string): Promise<void> {
    try {
      await AsyncStorage.removeItem(key);
    } catch (error) {
      console.error('Error removing from AsyncStorage:', error);
    }
  }

  async clear(): Promise<void> {
    try {
      const keys = await this.getAllKeys();
      await AsyncStorage.multiRemove(keys);
    } catch (error) {
      console.error('Error clearing AsyncStorage:', error);
    }
  }

  async getAllKeys(): Promise<string[]> {
    try {
      return await AsyncStorage.getAllKeys();
    } catch (error) {
      console.error('Error getting keys from AsyncStorage:', error);
      return [];
    }
  }
}

class MMKVStorageService implements StorageService {
  storage: MMKV;

  constructor() {
    this.storage = new MMKV();
  }

  async get<T>(key: string): Promise<T | null> {
    try {
      const value = this.storage.getString(key);
      return value ? JSON.parse(value) : null;
    } catch (error) {
      console.error('Error getting from MMKV:', error);
      return null;
    }
  }

  async set<T>(key: string, value: T): Promise<void> {
    try {
      this.storage.set(key, JSON.stringify(value));
    } catch (error) {
      console.error('Error setting to MMKV:', error);
    }
  }

  async remove(key: string): Promise<void> {
    try {
      this.storage.delete(key);
    } catch (error) {
      console.error('Error removing from MMKV:', error);
    }
  }

  async clear(): Promise<void> {
    try {
      this.storage.clearAll();
    } catch (error) {
      console.error('Error clearing MMKV:', error);
    }
  }

  async getAllKeys(): Promise<string[]> {
    try {
      return this.storage.getAllKeys();
    } catch (error) {
      console.error('Error getting keys from MMKV:', error);
      return [];
    }
  }
}

// Factory
export function createStorageService(): StorageService {
  // Use MMKV for better performance
  return new MMKVStorageService();
}

// Singleton
let storageService: StorageService | null = null;

export function getStorageService(): StorageService {
  if (!storageService) {
    storageService = createStorageService();
  }
  return storageService;
}
```

### SQLite Storage

```typescript
// npm install react-native-quick-sqlite
import SQLite from 'react-native-quick-sqlite';

class SQLiteService {
  private db: SQLite.SQLiteDatabase | null = null;

  async init(): Promise<void> {
    this.db = await SQLite.open({
      name: 'myapp.db',
      location: 'default',
    });

    await this.createTables();
  }

  private async createTables(): Promise<void> {
    await this.db.executeSql(`
      CREATE TABLE IF NOT EXISTS products (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        description TEXT,
        syncStatus TEXT DEFAULT 'pending',
        updatedAt INTEGER
      );
    `);

    await this.db.executeSql(`
      CREATE TABLE IF NOT EXISTS sync_queue (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        action TEXT NOT NULL,
        data TEXT NOT NULL,
        createdAt INTEGER NOT NULL,
        syncedAt INTEGER,
        status TEXT DEFAULT 'pending'
      );
    `);
  }

  async getAll<T>(table: string): Promise<T[]> {
    if (!this.db) {
      await this.init();
    }

    const results = await this.db.executeSql(`SELECT * FROM ${table}`);
    return results.rows.raw() as T[];
  }

  async insert<T>(table: string, data: T): Promise<void> {
    if (!this.db) {
      await this.init();
    }

    const columns = Object.keys(data).join(', ');
    const values = Object.values(data).map(v => typeof v === 'string' ? `'${v}' : v).join(', ');

    await this.db.executeSql(`
      INSERT INTO ${table} (${columns})
      VALUES (${values})
    `);
  }

  async update<T>(
    table: string,
    where: string,
    data: T
  ): Promise<void> {
    if (!this.db) {
      await this.init();
    }

    const updates = Object.entries(data)
      .map(([key, value]) => `${key} = ${typeof value === 'string' ? `'${value}' : value}`)
      .join(', ');

    await this.db.executeSql(`
      UPDATE ${table}
      SET ${updates}
      WHERE ${where}
    `);
  }

  async delete(table: string, where: string): Promise<void> {
    if (!this.db) {
      await this.init();
    }

    await this.db.executeSql(`
      DELETE FROM ${table}
      WHERE ${where}
    `);
  }
}
```

---

## Data Synchronization

### Sync Manager

```typescript
// src/services/SyncManager.ts
import { NetInfo } from '@react-native-community/netinfo';

interface SyncConfig {
  endpoint: string;
  headers?: Record<string, string>;
  retryAttempts: number;
  retryDelay: number;
}

class SyncManager {
  constructor(
    private storage: StorageService,
    private apiService: ApiService,
    private config: SyncConfig
  ) {}

  /**
   * Sync all data
   */
  async syncAll(): Promise<{
    synced: number;
    failed: number;
    errors: string[];
  }> {
    const isConnected = await this.checkConnection();
    if (!isConnected) {
      return { synced: 0, failed: 0, errors: ['No internet connection'] };
    }

    const synced: { success: number, failed: number, errors: string[] } = {
      success: 0,
      failed: 0,
      errors: [],
    };

    // Get all pending sync items
    const queue = await this.getSyncQueue();

    for (const item of queue) {
      try {
        await this.syncItem(item);
        synced.success++;
      } catch (error) {
        synced.failed++;
        errors.push(error.message);
      }
    }

    return synced;
  }

  /**
   * Sync single item
   */
  async syncItem(item: SyncQueueItem): Promise<void> {
    let attempt = 0;

    while (attempt < this.config.retryAttempts) {
      try {
        await this.performSync(item);
        break;
      } catch (error) {
        attempt++;

        if (attempt >= this.config.retryAttempts) {
          throw error;
        }

        await this.delay(this.config.retryDelay * attempt);
      }
    }
  }

  /**
   * Perform sync
   */
  private async performSync(item: SyncQueueItem): Promise<void> {
    switch (item.action) {
      case 'create':
        await this.createResource(item);
        break;
      case 'update':
        await this.updateResource(item);
        break;
      case 'delete':
        await this.deleteResource(item);
        break;
    }

    // Mark as synced
    await this.markAsSynced(item.id);
  }

  /**
   * Create resource
   */
  private async createResource(item: SyncQueueItem): Promise<void> {
    const data = JSON.parse(item.data);

    const response = await this.apiService.post(
      `${this.config.endpoint}/${item.resourceType}`,
      data
    );

    // Update local storage
    await this.updateLocalResource(item.resourceType, data.id, response.data);
  }

  /**
   * Update resource
   */
  private async updateResource(item: SyncQueueItem): Promise<void> {
    const data = JSON.parse(item.data);

    const response = await this.apiService.put(
      `${this.config.endpoint}/${item.resourceType}/${item.resourceId}`,
      data
    );

    // Update local storage
    await this.updateLocalResource(item.resourceType, item.resourceId, response.data);
  }

  /**
   * Delete resource
   */
  private async deleteResource(item: SyncQueueItem): Promise<void> {
    await this.apiService.delete(
      `${this.config.endpoint}/${item.resourceType}/${item.resourceId}`
    );

    // Remove from local storage
    await this.removeLocalResource(item.resourceType, item.resourceId);
  }

  /**
   * Update local resource
   */
  private async updateLocalResource(
    resourceType: string,
    resourceId: string,
    data: any
  ): Promise<void> {
    const storage = getStorageService();

    const resources = await storage.get<{ [key: string]: any }>(`resources_${resourceType}`) || {};

    resources[resourceId] = {
      ...resources[resourceId],
      ...data,
      syncStatus: SyncStatus.SYNCED,
      updatedAt: Date.now(),
    };

    await storage.set(`resources_${resourceType}`, resources);
  }

  /**
   * Remove local resource
   */
  private async removeLocalResource(
    resourceType: string,
    resourceId: string
  ): Promise<void> {
    const storage = getStorageService();

    const resources = await storage.get<{ [key: string]: any }>(`resources_${resourceType}`) || {});

    delete resources[resourceId];

    await storage.set(`resources_${resourceType}`, resources);
  }

  /**
   * Get sync queue
   */
  async getSyncQueue(): Promise<SyncQueueItem[]> {
    const storage = getStorageService();
    const queue = await storage.get<SyncQueueItem[]>('sync_queue') || [];

    return queue.filter(item => item.status === 'pending');
  }

  /**
   * Add to sync queue
   */
  async addToSyncQueue(item: Omit<SyncQueueItem, 'id'>): Promise<void> {
    const storage = getStorageService();
    const queue = await storage.get<SyncQueueItem[]>('sync_queue') || [];

    const newItem: SyncQueueItem = {
      ...item,
      id: Date.now().toString(),
      createdAt: Date.now(),
      status: 'pending',
    };

    queue.push(newItem);

    await storage.set('sync_queue', queue);
  }

  /**
   * Mark as synced
   */
  private async markAsSynced(itemId: string): Promise<void> {
    const storage = getStorageService();
    const queue = await storage.get<SyncQueueItem[]>('sync_queue') || [];

    const item = queue.find(i => i.id === itemId);
    if (item) {
      item.status = 'synced';
      item.syncedAt = Date.now();
    }

    await storage.set('sync_queue', queue);
  }

  /**
   * Check connection
   */
  private async checkConnection(): Promise<boolean> {
    return await NetInfo.fetch().isConnected;
  }

  /**
   * Delay
   */
  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

interface SyncQueueItem {
  id: string;
  action: 'create' | 'update' | 'delete';
  resourceType: string;
  resourceId: string;
  data: string;
  createdAt: number;
  status: string;
  syncedAt?: number;
}
```

---

## Conflict Resolution

### Conflict Resolver

```typescript
// src/services/ConflictResolver.ts

class ConflictResolver {
  constructor(
    private storage: StorageService,
    private apiService: ApiService,
  ) {}

  /**
   * Resolve conflict
   */
  async resolveConflict(params: {
    resourceType: string;
    resourceId: string;
    localData: any;
    serverData: any;
    resolution: ConflictResolution;
  }): Promise<any> {
    switch (resolution) {
      case ConflictResolution.CLIENT_WINS:
        return this.clientWins(localData, serverData);

      case ConflictResolution.SERVER_WINS:
        return this.serverWins(localData, serverData);

      case ConflictResolution.MERGE:
        return this.merge(localData, serverData);

      default:
        return this.serverWins(localData, serverData);
    }
  }

  /**
   * Client wins resolution
   */
  private clientWins(localData: any, serverData: any): any {
    return localData;
  }

  /**
   * Server wins resolution
   */
  private serverWins(localData: any, serverData: any): any {
    return serverData;
  }

  /**
   * Merge resolution
   */
  private merge(localData: any, serverData: any): any {
    // Implement merge logic
    return {
      ...localData,
      ...serverData,
      mergedAt: Date.now(),
    };
  }

  /**
   * Detect conflict
   */
  async detectConflict(params: {
    resourceType: string;
    resourceId: string;
    localUpdatedAt: number;
    serverUpdatedAt: number;
  }): Promise<boolean> {
    const timeDiff = Math.abs(localUpdatedAt - serverUpdatedAt);

    // Consider it a conflict if data was modified on both sides
    return timeDiff > 0; // Any difference is a conflict
  }
}
```

---

## Queue Management

### Sync Queue

```typescript
// src/services/SyncQueue.ts

class SyncQueue {
  constructor(private storage: StorageService) {}

  /**
   * Enqueue action
   */
  async enqueue(params: {
    action: 'create' | 'update' | 'delete';
    resourceType: string;
    resourceId: string;
    data: any;
  }): Promise<void> {
    const storage = getStorageService();
    const queue = await storage.get<SyncQueueItem[]>('sync_queue') || [];

    const item: SyncQueueItem = {
      id: Date.now().toString(),
      action: params.action,
      resourceType: params.resourceType,
      resourceId: params.resourceId,
      data: JSON.stringify(params.data),
      createdAt: Date.now(),
      status: 'pending',
    };

    queue.push(item);

    await storage.set('sync_queue', queue);
  }

  /**
   * Dequeue next item
   */
  async dequeue(): Promise<SyncQueueItem | null> {
    const storage = getStorageService();
    const queue = await storage.get<SyncQueueItem[]>('sync_queue') || [];

    if (queue.length === 0) {
      return null;
    }

    const item = queue.shift();

    await storage.set('sync_queue', queue);

    return item;
  }

  /**
   * Get queue size
   */
  async getQueueSize(): Promise<number> {
    const storage = getStorageService();
    const queue = await storage.get<SyncQueueItem[]>('sync_queue') || [];

    return queue.length;
  }

  /**
   * Clear queue
   */
  async clearQueue(): Promise<void> {
    const storage = getStorageService();
    await storage.remove('sync_queue');
  }
}
```

---

## Cache Strategies

### Cache Manager

```typescript
// src/services/CacheManager.ts

interface CacheConfig {
  maxSize: number; // in bytes
  maxAge: number; // in milliseconds
}

class CacheManager {
  constructor(
    private storage: StorageService,
    private config: CacheConfig
  ) {}

  /**
   * Get cached item
   */
  async get<T>(key: string): Promise<T | null> {
    const storage = getStorageService();
    const cache = await storage.get<CacheItem<T>>(`cache_${key}`);

    if (!cache) {
      return null;
    }

    // Check if expired
    if (Date.now() - cache.timestamp > this.config.maxAge) {
      await this.remove(key);
      return null;
    }

    return cache.data;
  }

  /**
   * Set cached item
   */
  async set<T>(key: string, data: T): Promise<void> {
    const storage = getStorageService();

    const cache: CacheItem<T> = {
      data,
      timestamp: Date.now(),
      size: JSON.stringify(data).length,
    };

    await storage.set(`cache_${key}`, cache);

    // Check cache size and evict if needed
    await this.checkAndEvict();
  }

  /**
   * Remove cached item
   */
  async remove(key: string): Promise<void> {
    const storage = getStorageService();
    await storage.remove(`cache_${key}`);
  }

  /**
   * Clear all cache
   */
  async clear(): Promise<void> {
    const storage = getStorageService();
    const keys = await storage.getAllKeys();
    const cacheKeys = keys.filter(k => k.startsWith('cache_'));

    for (const key of cacheKeys) {
      await storage.remove(key);
    }
  }

  /**
   * Check and evict if needed
   */
  private async checkAndEvict(): Promise<void> {
    const storage = getStorageService();
    const keys = await storage.getAllKeys();
    const cacheKeys = keys.filter(k => k.startsWith('cache_'));

    let totalSize = 0;

    for (const key of cacheKeys) {
      const cache = await storage.get<CacheItem<any>>(key);
      if (cache) {
        totalSize += cache.size;
      }
    }

    // Evict oldest items if over size limit
    if (totalSize > this.config.maxSize) {
      const items: Array<{ key: string; timestamp: number }[]> = [];

      for (const key of cacheKeys) {
        const cache = await storage.get<CacheItem<any>>(key);
        if (cache) {
          items.push({ key, timestamp: cache.timestamp });
        }
      }

      // Sort by timestamp (oldest first)
      items.sort((a, b) => a.timestamp - b.timestamp);

      let currentSize = totalSize;

      for (const item of items) {
        const cache = await storage.get<CacheItem<any>>(item.key);
        if (cache) {
          currentSize -= cache.size;
          await storage.remove(item.key);
        }

        if (currentSize <= this.config.maxSize) {
          break;
        }
      }
    }
  }
}

interface CacheItem<T> {
  data: T;
  timestamp: number;
  size: number;
}
```

---

## Network Detection

### Network Monitor

```typescript
import { NetInfo, NetInfoSubscription } from '@react-native-community/netinfo';

class NetworkMonitor {
  private subscription: NetInfoSubscription | null = null;
  private listeners: Set<(isConnected: boolean) => void> = new Set();

  /**
   * Start monitoring
   */
  startMonitoring(): void {
    this.subscription = NetInfo.addEventListener(state => {
      const isConnected = state.isConnected;
      this.notifyListeners(isConnected);
    });
  }

  /**
   * Stop monitoring
   */
  stopMonitoring(): void {
    if (this.subscription) {
      this.subscription.remove();
      this.subscription = null;
    }
  }

  /**
   * Add listener
   */
  addListener(listener: (isConnected: boolean) => void): void {
    this.listeners.add(listener);

    // Immediately notify with current state
    NetInfo.fetch().then(state => listener(state.isConnected!));
  }

  /**
   * Remove listener
   */
  removeListener(listener: (isConnected: boolean) => void): void {
    this.listeners.delete(listener);
  }

  /**
   * Get current status
   */
  async isConnected(): Promise<boolean> {
    const state = await NetInfo.fetch();
    return state.isConnected!;
  }

  /**
   * Notify all listeners
   */
  private notifyListeners(isConnected: boolean): void {
    for (const listener of this.listeners) {
      listener(isConnected);
    }
  }
}

// Singleton
const networkMonitor = new NetworkMonitor();
```

---

## Optimistic Updates

### Optimistic UI

```typescript
import { useState, useCallback } from 'react';

function useOptimisticUpdate<T>(
  key: string,
  initialValue: T
): [T, (value: T) => void] {
  const [localValue, setLocalValue] = useState<T>(initialValue);
  const [serverValue, setServerValue] = useState<T>(initialValue);

  const updateValue = useCallback(async (newValue: T) => {
    // Optimistically update UI
    setLocalValue(newValue);

    // Update server
    try {
      await apiService.update(key, newValue);
      setServerValue(newValue);
    } catch (error) {
      // Revert to server value on error
      setLocalValue(serverValue);
    }
  }, [key, serverValue]);

  const syncWithServer = useCallback(async () => {
    try {
      const value = await apiService.get<T>(key);
      setServerValue(value);
      setLocalValue(value);
    } catch (error) {
      console.error('Sync error:', error);
    }
  }, [key]);

  return {
    value: localValue,
    updateValue,
    syncWithServer,
    isPending: localValue !== serverValue,
    isSynced: localValue === serverValue,
  };
}

// Usage
function ProductForm({ productId }: { productId: string }) {
  const { value, updateValue, syncWithServer, isPending, isSynced } = useOptimisticUpdate<string>(`product_${productId}`, '');

  const handleSubmit = async (data: any) => {
    await updateValue(data.description);
  };

  return (
    <View>
      <TextInput
        value={value}
        onChangeText={updateValue}
        placeholder="Product description"
        multiline
      />
      {isPending && (
        <ActivityIndicator />
      )}
      {!isSynced && (
        <TouchableOpacity onPress={syncWithServer}>
          <Text>Sync changes</Text>
        </TouchableOpacity>
      )}
    </View>
  );
}
```

---

## Background Sync

### Background Task Runner

```typescript
// npm install react-native-background-task

import BackgroundTask from 'react-native-background-task';

class BackgroundSyncService {
  /**
   * Schedule background sync
   */
  async scheduleBackgroundSync(): Promise<void> {
    const taskId = await BackgroundTask.schedule({
      taskName: 'backgroundSync',
      taskInfo: {
        delay: 1000, // 1 second
      periodic: 300000, // 5 minutes
      allowExecutionInForeground: false,
    },
    callback: this.syncInBackground,
    taskId: 'backgroundSync',
    allowed: true,
    stopOnTerminate: false,
    forceAlarmManager: true,
  });
  }

  /**
   * Sync in background
   */
  async syncInBackground(): Promise<void> {
    const syncManager = new SyncManager(
      getStorageService(),
      new ApiService(),
      {
        endpoint: API_URL,
        retryAttempts: 3,
        retryDelay: 5000,
      }
    );

    const result = await syncManager.syncAll();

    console.log('Background sync result:', result);
  }

  /**
   * Cancel background sync
   */
  async cancelBackgroundSync(): Promise<void> {
    await BackgroundTask.cancel('backgroundSync');
  }
}
```

---

## Testing Offline Scenarios

### Offline Test Runner

```typescript
class OfflineTestRunner {
  /**
   * Test offline scenario
   */
  async testOfflineScenario(params: {
    actions: Array<{
      action: () => Promise<void>;
      description: string;
    }>;
  }): Promise<{
    passed: boolean;
    failed: string[];
  }> {
    const failed: string[] = [];

    for (const action of params.actions) {
      try {
        await action.action();
      console.log(`✓ ${action.description}`);
      } catch (error) {
        failed.push(`${action.description}: ${error.message}`);
        console.error(`✗ ${action.description}: ${error.message}`);
      }
    }

    return {
      passed: failed.length === 0,
      failed,
    };
  }

  /**
   * Test create while offline
   */
  async testCreateOffline(): Promise<{
    passed: boolean;
    failed: string[];
  }> {
    const storage = getStorageService();

    // Simulate offline state
    const products = await storage.get<any[]>('products') || [];

    return await this.testOfflineScenario({
      actions: [
        {
          action: async () => {
            const newProduct = {
              id: 'offline-product-1',
              name: 'Offline Product',
              price: 99.99,
              description: 'Created offline',
              syncStatus: SyncStatus.PENDING,
            };

            products.push(newProduct);
            await storage.set('products', products);
          },
          description: 'Create product while offline',
        },
        {
          action: async () => {
            const products = await storage.get<any[]>('products') || [];
            const updated = [...products];
            updated[0].name = 'Updated offline';

            await storage.set('products', updated);
          },
          description: 'Update product while offline',
        },
        {
          action: async () => {
            const products = await storage.get<any[]>('products') || [];
            const filtered = products.filter(p => p.id !== 'offline-product-1');

            await storage.set('products', filtered);
          },
          description: 'Delete product while offline',
        },
      ],
    });
  }

  /**
   * Test sync after coming back online
   */
  async testSyncAfterOffline(): Promise<{
    passed: boolean;
    failed: string[];
  }> {
    const syncManager = new SyncManager(
      getStorageService(),
      new ApiService(),
      {
        endpoint: API_URL,
        retryAttempts: 3,
        retryDelay: 5000,
      }
    );

    const result = await syncManager.syncAll();

    return {
      passed: result.failed === 0,
      failed: result.errors,
    };
  }
}
```

---

## Best Practices

### Offline-First Best Practices

```typescript
// 1. Always check network before operations
async function withNetworkCheck<T>(
  onlineFn: () => Promise<T>,
  offlineFn: () => T | Promise<T>
): Promise<T> {
  const isConnected = await networkMonitor.isConnected();

  if (isConnected) {
    return await onlineFn();
  } else {
    return await offlineFn();
  }
}

// Usage
async function fetchProduct(productId: string) {
  return await withNetworkCheck(
    async () => await apiService.getProduct(productId),
    async () => {
      const storage = getStorageService();
      return await storage.get<Product>(`product_${productId}`);
    }
  );
}

// 2. Use proper error handling
async function safeSync(): Promise<void> {
  const syncManager = new SyncManager(
    getStorageService(),
    new ApiService(),
    {
      endpoint: API_URL,
      retryAttempts: 3,
      retryDelay: 5000,
    }
  );

  try {
    const result = await syncManager.syncAll();
    console.log('Sync completed:', result);
  } catch (error) {
    console.error('Sync failed:', error);

    // Queue for later
    const storage = getStorageService();
    await storage.set('sync_failed_at', Date.now());
  }
}

// 3. Implement proper cache invalidation
async function invalidateCache(key: string): Promise<void> {
  const cacheManager = new CacheManager(
    getStorageService(),
    {
      maxSize: 10 * 1024 * 1024, // 10MB
      maxAge: 24 * 60 * 60 * 1000, // 24 hours
    }
  );

  await cacheManager.remove(key);
}

// 4. Use optimistic updates with rollback
function useOptimisticUpdate<T>(
  key: string,
  initialValue: T
): [T, (value: T) => void] {
  const [localValue, setLocalValue] = useState<T>(initialValue);
  const [serverValue, setServerValue] = useState<T>(initialValue);

  const updateValue = useCallback(async (newValue: T) => {
    // Optimistically update
    setLocalValue(newValue);

    // Update server
    try {
      await apiService.update(key, newValue);
      setServerValue(newValue);
    } catch (error) {
      // Revert on error
      setLocalValue(serverValue);
    }
  }, [key, serverValue]);

  const syncWithServer = useCallback(async () => {
    try {
      const value = await apiService.get<T>(key);
      setServerValue(value);
      setLocalValue(value);
    } catch (error) {
      console.error('Sync error:', error);
    }
  }, [key]);

  return {
    value: localValue,
    updateValue,
    syncWithServer,
    isPending: localValue !== serverValue,
    isSynced: localValue === serverValue,
  };
}

// 5. Implement proper conflict detection
async function detectAndResolveConflict(
  resourceType: string,
  resourceId: string,
  localData: any,
  serverData: any
): Promise<any> {
  const resolver = new ConflictResolver(
    getStorageService(),
    new ApiService()
  );

  const isConflict = await resolver.detectConflict({
    resourceType,
    resourceId,
    localUpdatedAt: localData.updatedAt,
    serverUpdatedAt: serverData.updatedAt,
  });

  if (isConflict) {
    return await resolver.resolveConflict({
      resourceType,
      resourceId,
      localData,
      serverData,
      resolution: ConflictResolution.MERGE,
    });
  }

  return serverData;
}
```

---

---

## Quick Start

### AsyncStorage Setup

```javascript
import AsyncStorage from '@react-native-async-storage/async-storage'

// Save data
async function saveData(key, value) {
  try {
    await AsyncStorage.setItem(key, JSON.stringify(value))
  } catch (error) {
    console.error('Error saving data:', error)
  }
}

// Load data
async function loadData(key) {
  try {
    const value = await AsyncStorage.getItem(key)
    return value ? JSON.parse(value) : null
  } catch (error) {
    console.error('Error loading data:', error)
    return null
  }
}
```

### Sync Queue

```javascript
class SyncQueue {
  constructor() {
    this.queue = []
    this.syncing = false
  }
  
  async add(operation) {
    this.queue.push(operation)
    await this.saveQueue()
    this.sync()
  }
  
  async sync() {
    if (this.syncing || this.queue.length === 0) return
    
    this.syncing = true
    const operation = this.queue.shift()
    
    try {
      await this.executeOperation(operation)
      await this.saveQueue()
    } catch (error) {
      this.queue.unshift(operation)  // Retry
      await this.saveQueue()
    } finally {
      this.syncing = false
      if (this.queue.length > 0) {
        this.sync()
      }
    }
  }
}
```

---

## Production Checklist

- [ ] **Local Storage**: Choose appropriate storage (AsyncStorage, SQLite, MMKV)
- [ ] **Data Sync**: Implement data synchronization
- [ ] **Conflict Resolution**: Handle data conflicts
- [ ] **Queue Management**: Queue operations when offline
- [ ] **Network Detection**: Detect network connectivity
- [ ] **Optimistic Updates**: Update UI optimistically
- [ ] **Background Sync**: Sync in background
- [ ] **Error Handling**: Handle sync errors gracefully
- [ ] **Testing**: Test offline scenarios
- [ ] **Performance**: Optimize storage operations
- [ ] **Data Size**: Manage storage size
- [ ] **User Feedback**: Show sync status to users

---

## Anti-patterns

### ❌ Don't: No Conflict Resolution

```javascript
// ❌ Bad - Overwrite without checking
async function syncData(localData, serverData) {
  await saveData('key', serverData)  // Lost local changes!
}
```

```javascript
// ✅ Good - Conflict resolution
async function syncData(localData, serverData) {
  if (serverData.updatedAt > localData.updatedAt) {
    // Server is newer
    await saveData('key', serverData)
  } else if (localData.updatedAt > serverData.updatedAt) {
    // Local is newer, send to server
    await sendToServer('key', localData)
  } else {
    // Conflict - merge or ask user
    const merged = mergeData(localData, serverData)
    await saveData('key', merged)
  }
}
```

### ❌ Don't: No Queue

```javascript
// ❌ Bad - Operations lost when offline
async function createOrder(order) {
  await api.createOrder(order)  // Fails when offline!
}
```

```javascript
// ✅ Good - Queue operations
async function createOrder(order) {
  if (isOnline()) {
    await api.createOrder(order)
  } else {
    await syncQueue.add({ type: 'createOrder', data: order })
  }
}
```

---

## Integration Points

- **React Native Patterns** (`31-mobile-development/react-native-patterns/`) - App patterns
- **Push Notifications** (`31-mobile-development/push-notifications/`) - Sync notifications
- **Database** (`04-database/`) - Local database patterns

---

## Further Reading

- [React Native Offline Storage](https://react-native-async-storage/)
- [MMKV Storage](https://github.com/ammar-jamil/react-native-mmkv-storage)
- [React Native SQLite](https://github.com/andporobi/react-native-quick-sqlite)
- [Offline-First Architecture](https://offlinefirst.org/)
- [React Native Background Task](https://github.com/transistorsoft/react-native-background-task)
- [NetInfo](https://github.com/react-native-netinfo/)
