# Service Discovery

## Overview

Comprehensive guide to service discovery patterns using Consul and etcd for microservices.

## Table of Contents

1. [Service Discovery Concepts](#service-discovery-concepts)
2. [Client-Side vs Server-Side Discovery](#client-side-vs-server-side-discovery)
3. [Consul](#consul)
4. [etcd](#etcd)
5. [Registration Patterns](#registration-patterns)
6. [Health Checks](#health-checks)
7. [Load Balancing Integration](#load-balancing-integration)
8. [Failure Handling](#failure-handling)
9. [Production Deployment](#production-deployment)
10. [Best Practices](#best-practices)

---

## Service Discovery Concepts

### Core Concepts

```markdown
## Service Discovery Core Concepts

### What is Service Discovery?
- Mechanism for services to find and communicate with each other
- Dynamic service registration and discovery
- Handles service instances coming and going

### Types
- **Client-Side**: Client discovers and selects service instance
- **Server-Side**: Load balancer/discovery service handles routing

### Benefits
- Dynamic scaling without config changes
- Automatic failover
- Load balancing
- Service health awareness
```

### Discovery Architecture

```typescript
// service-discovery-types.ts
export enum DiscoveryType {
  CLIENT_SIDE = 'client_side',
  SERVER_SIDE = 'server_side'
}

export interface ServiceInstance {
  id: string;
  name: string;
  address: string;
  port: number;
  metadata: Record<string, any>;
  health: 'healthy' | 'unhealthy';
  lastSeen: Date;
}

export interface ServiceDiscovery {
  register(instance: ServiceInstance): Promise<void>;
  deregister(instanceId: string): Promise<void>;
  discover(serviceName: string): Promise<ServiceInstance[]>;
  getHealthy(serviceName: string): Promise<ServiceInstance>;
  watch(serviceName: string, callback: (instances: ServiceInstance[]) => void): void;
}
```

---

## Client-Side vs Server-Side Discovery

### Comparison

```markdown
## Discovery Type Comparison

### Client-Side Discovery
**Pros:**
- No single point of failure
- Lower latency (direct connection)
- More control over routing

**Cons:**
- Client complexity
- Each client needs discovery logic
- Load balancing per client

**Use Cases:**
- High-performance requirements
- Simple service topology
- Low-latency requirements

### Server-Side Discovery
**Pros:**
- Simpler clients
- Centralized control
- Easier to implement features

**Cons:**
- Single point of failure
- Additional network hop
- Higher latency

**Use Cases:**
- Complex service topology
- Need for advanced routing
- Easier client implementation
```

---

## Consul

### Consul Setup

```bash
# consul-install.sh
#!/bin/bash

# Download Consul
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list

# Install Consul
sudo apt update && sudo apt install consul

# Start Consul
sudo systemctl start consul
sudo systemctl enable consul

# Verify installation
consul version
consul members
```

### Docker Setup

```yaml
# docker-compose.yml
version: '3.8'

services:
  consul:
    image: consul:1.15
    ports:
      - "8300:8300"   # Server RPC
      - "8301:8301"   # Serf LAN
      - "8302:8302"   # Serf WAN
      - "8500:8500"   # HTTP API
      - "8600:8600/udp"   # DNS
    volumes:
      - consul-data:/consul/data
    command: >
      consul agent
      -server
      -bootstrap-expect=1
      -ui
      -client=0.0.0.0
      -bind=0.0.0.0
      -data-dir=/consul/data
      -config-dir=/consul/config
    networks:
      - consul-net

volumes:
  consul-data:

networks:
  consul-net:
    driver: bridge
```

### Service Registration

```typescript
// consul-service.ts
import axios from 'axios';

export interface ConsulServiceConfig {
  id: string;
  name: string;
  address: string;
  port: number;
  tags?: string[];
  meta?: Record<string, string>;
  check?: ConsulHealthCheck;
}

export interface ConsulHealthCheck {
  http?: string;
  tcp?: string;
  interval: string;
  timeout: string;
  deregister_critical_service_after: string;
}

export class ConsulServiceRegistry {
  private consulUrl: string;
  
  constructor(consulUrl: string = 'http://localhost:8500') {
    this.consulUrl = consulUrl;
  }
  
  async register(config: ConsulServiceConfig): Promise<void> {
    const serviceData = {
      ID: config.id,
      Name: config.name,
      Address: config.address,
      Port: config.port,
      Tags: config.tags || [],
      Meta: config.meta || {},
      Check: config.check ? {
        HTTP: config.check.http,
        TCP: config.check.tcp,
        Interval: config.check.interval,
        Timeout: config.check.timeout,
        DeregisterCriticalServiceAfter: config.check.deregister_critical_service_after
      } : undefined
    };
    
    await axios.put(`${this.consulUrl}/v1/agent/service/register`, serviceData);
    console.log(`Service ${config.name} registered with Consul`);
  }
  
  async deregister(serviceId: string): Promise<void> {
    await axios.put(`${this.consulUrl}/v1/agent/service/deregister/${serviceId}`);
    console.log(`Service ${serviceId} deregistered from Consul`);
  }
  
  async discover(serviceName: string): Promise<any[]> {
    const response = await axios.get(
      `${this.consulUrl}/v1/health/service/${serviceName}?passing`
    );
    return response.data.map((service: any) => ({
      id: service.Service.ID,
      name: service.Service.Service,
      address: service.Service.Address || service.Node.Address,
      port: service.Service.Port,
      tags: service.Service.Tags,
      meta: service.Service.Meta,
      health: service.Checks.every((c: any) => c.Status === 'passing') ? 'healthy' : 'unhealthy'
    }));
  }
  
  async getAllServices(): Promise<any[]> {
    const response = await axios.get(`${this.consulUrl}/v1/catalog/services`);
    return response.data;
  }
  
  async watchService(serviceName: string, callback: (instances: any[]) => void): Promise<void> {
    const index = await this.getServiceIndex(serviceName);
    
    const poll = async () => {
      const currentIndex = await this.getServiceIndex(serviceName);
      
      if (currentIndex !== index) {
        const instances = await this.discover(serviceName);
        callback(instances);
      }
      
      setTimeout(poll, 1000);
    };
    
    poll();
  }
  
  private async getServiceIndex(serviceName: string): Promise<number> {
    const response = await axios.get(
      `${this.consulUrl}/v1/health/service/${serviceName}?index`
    );
    return parseInt(response.headers['x-consul-index'] || '0');
  }
}

// Usage
const registry = new ConsulServiceRegistry('http://localhost:8500');

// Register service
await registry.register({
  id: 'user-service-1',
  name: 'user-service',
  address: '10.0.0.1',
  port: 3000,
  tags: ['api', 'v1'],
  meta: {
    version: '1.0.0',
    environment: 'production'
  },
  check: {
    http: 'http://10.0.0.1:3000/health',
    interval: '10s',
    timeout: '5s',
    deregister_critical_service_after: '30s'
  }
});

// Discover service
const instances = await registry.discover('user-service');
console.log('Service instances:', instances);
```

### DNS Interface

```typescript
// consul-dns.ts
import { Resolver } from 'dns';
import { promisify } from 'util';

const resolve = promisify(Resolver().resolve4);

export class ConsulDNS {
  private consulDomain: string;
  
  constructor(consulDomain: string = 'service.consul') {
    this.consulDomain = consulDomain;
  }
  
  async resolveService(serviceName: string): Promise<string[]> {
    const fqdn = `${serviceName}.${this.consulDomain}`;
    const addresses = await resolve(fqdn);
    return addresses;
  }
  
  async resolveServiceWithTag(serviceName: string, tag: string): Promise<string[]> {
    const fqdn = `${tag}.${serviceName}.${this.consulDomain}`;
    const addresses = await resolve(fqdn);
    return addresses;
  }
}

// Usage
const dns = new ConsulDNS();
const addresses = await dns.resolveService('user-service');
console.log('Service addresses:', addresses);

// Resolve with tag
const apiAddresses = await dns.resolveServiceWithTag('user-service', 'api');
console.log('API addresses:', apiAddresses);
```

---

## etcd

### etcd Setup

```bash
# etcd-install.sh
#!/bin/bash

# Download etcd
ETCD_VER=v3.5.0

wget https://github.com/etcd-io/etcd/releases/download/${ETCD_VER}/etcd-${ETCD_VER}-linux-amd64.tar.gz

# Extract
tar xzvf etcd-${ETCD_VER}-linux-amd64.tar.gz
cd etcd-${ETCD_VER}-linux-amd64

# Move binaries
sudo cp etcd etcdctl /usr/local/bin/

# Verify installation
etcd --version
etcdctl version
```

### Docker Setup

```yaml
# docker-compose.yml
version: '3.8'

services:
  etcd:
    image: quay.io/coreos/etcd:v3.5.0
    ports:
      - "2379:2379"   # Client requests
      - "2380:2380"   # Peer communication
    volumes:
      - etcd-data:/etcd-data
    command: >
      etcd
      -name etcd0
      -data-dir /etcd-data
      -listen-client-urls http://0.0.0.0:2379
      -advertise-client-urls http://etcd:2379
      -listen-peer-urls http://0.0.0.0:2380
      -initial-advertise-peer-urls http://etcd:2380
      -initial-cluster etcd0=http://etcd:2380
    networks:
      - etcd-net

volumes:
  etcd-data:

networks:
  etcd-net:
    driver: bridge
```

### Service Registration

```typescript
// etcd-service.ts
import { Etcd3 } from 'etcd3';

export interface EtcdServiceConfig {
  id: string;
  name: string;
  address: string;
  port: number;
  metadata?: Record<string, any>;
  ttl: number; // Time to live in seconds
}

export class EtcdServiceRegistry {
  private client: Etcd3;
  private leaseId: string | null = null;
  
  constructor(etcdUrl: string = 'http://localhost:2379') {
    this.client = new Etcd3({
      hosts: [etcdUrl]
    });
  }
  
  async register(config: EtcdServiceConfig): Promise<void> {
    const key = `/services/${config.name}/${config.id}`;
    const value = JSON.stringify({
      id: config.id,
      name: config.name,
      address: config.address,
      port: config.port,
      metadata: config.metadata || {},
      registeredAt: new Date().toISOString()
    });
    
    // Create lease for TTL
    const lease = await this.client.lease(config.ttl);
    this.leaseId = lease.leaseID;
    
    // Register service with lease
    await this.client.put(key, value, { lease: this.leaseId });
    
    // Keep lease alive
    this.keepLeaseAlive(lease);
    
    console.log(`Service ${config.name} registered with etcd`);
  }
  
  private async keepLeaseAlive(lease: any): Promise<void> {
    setInterval(async () => {
      await lease.keepAlive();
    }, (lease.ttl / 2) * 1000);
  }
  
  async deregister(serviceName: string, serviceId: string): Promise<void> {
    const key = `/services/${serviceName}/${serviceId}`;
    await this.client.delete().key(key);
    console.log(`Service ${serviceId} deregistered from etcd`);
  }
  
  async discover(serviceName: string): Promise<any[]> {
    const key = `/services/${serviceName}`;
    const instances = await this.client.getAll().prefix(key);
    
    return instances.map(([key, value]) => {
      const data = JSON.parse(value);
      return {
        ...data,
        health: 'healthy' // Assume healthy if registered
      };
    });
  }
  
  async watchService(serviceName: string, callback: (instances: any[]) => void): Promise<void> {
    const key = `/services/${serviceName}`;
    
    const watcher = await this.client.watch().prefix(key);
    
    watcher.on('put', async () => {
      const instances = await this.discover(serviceName);
      callback(instances);
    });
    
    watcher.on('delete', async () => {
      const instances = await this.discover(serviceName);
      callback(instances);
    });
  }
  
  async close(): Promise<void> {
    if (this.leaseId) {
      await this.client.lease().revoke(this.leaseId);
    }
    await this.client.close();
  }
}

// Usage
const registry = new EtcdServiceRegistry('http://localhost:2379');

// Register service
await registry.register({
  id: 'user-service-1',
  name: 'user-service',
  address: '10.0.0.1',
  port: 3000,
  metadata: {
    version: '1.0.0',
    environment: 'production'
  },
  ttl: 30 // 30 seconds TTL
});

// Discover service
const instances = await registry.discover('user-service');
console.log('Service instances:', instances);
```

---

## Registration Patterns

### Self-Registration

```typescript
// self-registration.ts
export class SelfRegistrationService {
  constructor(
    private registry: ServiceDiscovery,
    private serviceConfig: ServiceInstance
  ) {}
  
  async start(): Promise<void> {
    await this.registry.register(this.serviceConfig);
    
    // Setup heartbeat
    this.setupHeartbeat();
    
    // Handle shutdown
    this.setupShutdownHandler();
  }
  
  private setupHeartbeat(): void {
    setInterval(async () => {
      // Re-register to keep service alive
      await this.registry.register(this.serviceConfig);
    }, 10000); // Every 10 seconds
  }
  
  private setupShutdownHandler(): void {
    const shutdown = async () => {
      await this.registry.deregister(this.serviceConfig.id);
      process.exit(0);
    };
    
    process.on('SIGTERM', shutdown);
    process.on('SIGINT', shutdown);
  }
}

// Usage
const selfRegistrar = new SelfRegistrationService(
  registry,
  {
    id: 'user-service-1',
    name: 'user-service',
    address: '10.0.0.1',
    port: 3000,
    metadata: { version: '1.0.0' },
    health: 'healthy',
    lastSeen: new Date()
  }
);

await selfRegistrar.start();
```

### Third-Party Registration

```typescript
// third-party-registration.ts
export class ThirdPartyRegistrationService {
  constructor(
    private registry: ServiceDiscovery,
    private services: ServiceInstance[]
  ) {}
  
  async registerAll(): Promise<void> {
    for (const service of this.services) {
      await this.registry.register(service);
    }
  }
  
  async deregisterAll(): Promise<void> {
    for (const service of this.services) {
      await this.registry.deregister(service.id);
    }
  }
  
  async syncServices(): Promise<void> {
    const currentServices = await this.registry.discover('*');
    const currentIds = new Set(currentServices.map(s => s.id));
    
    // Register missing services
    for (const service of this.services) {
      if (!currentIds.has(service.id)) {
        await this.registry.register(service);
      }
    }
    
    // Deregister unknown services
    for (const service of currentServices) {
      if (!this.services.find(s => s.id === service.id)) {
        await this.registry.deregister(service.id);
      }
    }
  }
}
```

---

## Health Checks

### Health Check Configuration

```typescript
// health-check.ts
export interface HealthCheckConfig {
  type: 'http' | 'tcp' | 'script';
  endpoint?: string;
  interval: number; // seconds
  timeout: number; // seconds
  deregisterAfter: number; // seconds
  threshold: number; // consecutive failures
}

export class HealthChecker {
  private healthStatus: Map<string, boolean> = new Map();
  private failureCount: Map<string, number> = new Map();
  
  async checkHealth(service: ServiceInstance, config: HealthCheckConfig): Promise<boolean> {
    const isHealthy = await this.performHealthCheck(service, config);
    
    const serviceId = service.id;
    const previousStatus = this.healthStatus.get(serviceId);
    
    if (isHealthy) {
      this.failureCount.set(serviceId, 0);
      this.healthStatus.set(serviceId, true);
    } else {
      const failures = (this.failureCount.get(serviceId) || 0) + 1;
      this.failureCount.set(serviceId, failures);
      
      if (failures >= config.threshold) {
        this.healthStatus.set(serviceId, false);
      }
    }
    
    // Notify on status change
    if (previousStatus !== undefined && previousStatus !== isHealthy) {
      this.notifyStatusChange(service, isHealthy);
    }
    
    return isHealthy;
  }
  
  private async performHealthCheck(
    service: ServiceInstance,
    config: HealthCheckConfig
  ): Promise<boolean> {
    try {
      if (config.type === 'http' && config.endpoint) {
        const response = await fetch(
          `http://${service.address}:${service.port}${config.endpoint}`,
          { method: 'GET', signal: AbortSignal.timeout(config.timeout * 1000) }
        );
        return response.ok;
      } else if (config.type === 'tcp') {
        return await this.checkTCP(service.address, service.port, config.timeout * 1000);
      }
      
      return false;
    } catch (error) {
      return false;
    }
  }
  
  private async checkTCP(host: string, port: number, timeout: number): Promise<boolean> {
    return new Promise((resolve) => {
      const socket = require('net').createConnection(port, host);
      
      socket.setTimeout(timeout, () => {
        socket.destroy();
        resolve(false);
      });
      
      socket.on('connect', () => {
        socket.destroy();
        resolve(true);
      });
      
      socket.on('error', () => {
        resolve(false);
      });
    });
  }
  
  private notifyStatusChange(service: ServiceInstance, isHealthy: boolean): void {
    console.log(`Service ${service.name} (${service.id}) is now ${isHealthy ? 'healthy' : 'unhealthy'}`);
  }
}
```

---

## Load Balancing Integration

### Round-Robin Load Balancer

```typescript
// load-balancer.ts
export interface LoadBalancer {
  select(instances: ServiceInstance[]): ServiceInstance;
}

export class RoundRobinBalancer implements LoadBalancer {
  private currentIndex = 0;
  
  select(instances: ServiceInstance[]): ServiceInstance {
    const healthyInstances = instances.filter(i => i.health === 'healthy');
    
    if (healthyInstances.length === 0) {
      throw new Error('No healthy instances available');
    }
    
    const selected = healthyInstances[this.currentIndex % healthyInstances.length];
    this.currentIndex++;
    
    return selected;
  }
}

export class LeastConnectionsBalancer implements LoadBalancer {
  private connectionCounts: Map<string, number> = new Map();
  
  select(instances: ServiceInstance[]): ServiceInstance {
    const healthyInstances = instances.filter(i => i.health === 'healthy');
    
    if (healthyInstances.length === 0) {
      throw new Error('No healthy instances available');
    }
    
    // Find instance with least connections
    let selected = healthyInstances[0];
    let minConnections = this.connectionCounts.get(selected.id) || 0;
    
    for (const instance of healthyInstances) {
      const connections = this.connectionCounts.get(instance.id) || 0;
      if (connections < minConnections) {
        minConnections = connections;
        selected = instance;
      }
    }
    
    // Increment connection count
    this.connectionCounts.set(selected.id, minConnections + 1);
    
    return selected;
  }
  
  releaseConnection(instanceId: string): void {
    const count = this.connectionCounts.get(instanceId) || 0;
    this.connectionCounts.set(instanceId, Math.max(0, count - 1));
  }
}

export class RandomBalancer implements LoadBalancer {
  select(instances: ServiceInstance[]): ServiceInstance {
    const healthyInstances = instances.filter(i => i.health === 'healthy');
    
    if (healthyInstances.length === 0) {
      throw new Error('No healthy instances available');
    }
    
    const randomIndex = Math.floor(Math.random() * healthyInstances.length);
    return healthyInstances[randomIndex];
  }
}
```

---

## Failure Handling

### Retry with Discovery

```typescript
// retry-with-discovery.ts
export class DiscoveryRetryClient {
  constructor(
    private registry: ServiceDiscovery,
    private loadBalancer: LoadBalancer
  ) {}
  
  async callService<T>(
    serviceName: string,
    request: () => Promise<T>,
    maxRetries: number = 3
  ): Promise<T> {
    let lastError: Error | null = null;
    
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      try {
        const instances = await this.registry.discover(serviceName);
        const instance = this.loadBalancer.select(instances);
        
        console.log(`Attempt ${attempt}: Calling ${serviceName} at ${instance.address}:${instance.port}`);
        
        return await request();
      } catch (error) {
        lastError = error as Error;
        console.error(`Attempt ${attempt} failed:`, error);
        
        // Backoff before retry
        if (attempt < maxRetries) {
          await this.sleep(1000 * attempt);
        }
      }
    }
    
    throw lastError || new Error('All retry attempts failed');
  }
  
  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// Usage
const client = new DiscoveryRetryClient(registry, new RoundRobinBalancer());

try {
  const result = await client.callService('user-service', async () => {
    const response = await fetch('http://user-service:3000/api/users');
    return response.json();
  });
  console.log(result);
} catch (error) {
  console.error('Service call failed:', error);
}
```

---

## Production Deployment

### Consul Cluster

```yaml
# consul-cluster.yml
version: '3.8'

services:
  consul-server-1:
    image: consul:1.15
    ports:
      - "8500:8500"
      - "8600:8600/udp"
    volumes:
      - consul1-data:/consul/data
    command: >
      consul agent
      -server
      -bootstrap-expect=3
      -node=consul-server-1
      -bind=0.0.0.0
      -client=0.0.0.0
      -data-dir=/consul/data
      -config-dir=/consul/config
      -retry-join=consul-server-2
      -retry-join=consul-server-3
    networks:
      - consul-net

  consul-server-2:
    image: consul:1.15
    ports:
      - "8501:8500"
      - "8601:8600/udp"
    volumes:
      - consul2-data:/consul/data
    command: >
      consul agent
      -server
      -bootstrap-expect=3
      -node=consul-server-2
      -bind=0.0.0.0
      -client=0.0.0.0
      -data-dir=/consul/data
      -config-dir=/consul/config
      -retry-join=consul-server-1
      -retry-join=consul-server-3
    networks:
      - consul-net

  consul-server-3:
    image: consul:1.15
    ports:
      - "8502:8500"
      - "8602:8600/udp"
    volumes:
      - consul3-data:/consul/data
    command: >
      consul agent
      -server
      -bootstrap-expect=3
      -node=consul-server-3
      -bind=0.0.0.0
      -client=0.0.0.0
      -data-dir=/consul/data
      -config-dir=/consul/config
      -retry-join=consul-server-1
      -retry-join=consul-server-2
    networks:
      - consul-net

volumes:
  consul1-data:
  consul2-data:
  consul3-data:

networks:
  consul-net:
    driver: bridge
```

---

## Best Practices

### Service Discovery Checklist

```markdown
## Service Discovery Best Practices Checklist

### Registration
- [ ] Automatic service registration on startup
- [ ] Heartbeat/lease renewal
- [ ] Graceful deregistration on shutdown
- [ ] Service metadata (version, environment)
- [ ] Unique service IDs

### Health Checks
- [ ] Appropriate health check endpoints
- [ ] Configurable intervals and timeouts
- [ ] Automatic deregistration after failures
- [ ] Multiple health check types
- [ ] Health check logging

### Discovery
- [ ] Client-side load balancing
- [ ] Caching of service instances
- [ ] Watch for service changes
- [ ] Fallback for no healthy instances
- [ ] Retry logic with backoff

### Security
- [ ] Authentication for registration
- [ ] TLS for communication
- [ ] Service ACLs
- [ ] Network segmentation

### Monitoring
- [ ] Service registration metrics
- [ ] Health check metrics
- [ ] Discovery latency metrics
- [ ] Alert on service unavailability
```

---

## Additional Resources

- [Consul Documentation](https://www.consul.io/docs)
- [etcd Documentation](https://etcd.io/docs/)
- [Service Discovery Patterns](https://microservices.io/patterns/service-discovery.html)
- [Kubernetes Service Discovery](https://kubernetes.io/docs/concepts/services-networking/service-discovery/)
