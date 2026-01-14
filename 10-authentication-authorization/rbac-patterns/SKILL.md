# RBAC Patterns

## Overview

Comprehensive guide to Role-Based Access Control (RBAC) patterns for web applications.

## Table of Contents

1. [RBAC Concepts](#rbac-concepts)
2. [Database Schema Design](#database-schema-design)
3. [Implementation](#implementation)
4. [Role Hierarchy](#role-hierarchy)
5. [Permission Checking](#permission-checking)
6. [Dynamic Permissions](#dynamic-permissions)
7. [UI-Based Authorization](#ui-based-authorization)
8. [API Authorization](#api-authorization)
9. [Testing RBAC](#testing-rbac)
10. [Common Patterns](#common-patterns)
11. [Best Practices](#best-practices)

---

## RBAC Concepts

### Core Concepts

```typescript
// rbac-types.ts
export interface User {
  id: string;
  email: string;
  name: string;
  roles: Role[];
}

export interface Role {
  id: string;
  name: string;
  description: string;
  permissions: Permission[];
  parentRoles?: Role[]; // For role hierarchy
}

export interface Permission {
  id: string;
  name: string;
  resource: string;
  action: string;
  description: string;
}

export interface Resource {
  name: string;
  actions: string[];
}

// Common resources and actions
export const Resources = {
  users: {
    name: 'users',
    actions: ['create', 'read', 'update', 'delete', 'list']
  },
  posts: {
    name: 'posts',
    actions: ['create', 'read', 'update', 'delete', 'publish', 'list']
  },
  settings: {
    name: 'settings',
    actions: ['read', 'update']
  },
  admin: {
    name: 'admin',
    actions: ['*'] // All actions
  }
};
```

### RBAC Model

```markdown
## RBAC Model

### Users
- Individual users in the system
- Can have multiple roles
- Can have direct permissions

### Roles
- Collection of permissions
- Can inherit from other roles
- Define user responsibilities

### Permissions
- Granular access control
- Resource + action combination
- Can be assigned to roles or users directly

### Example
**Roles:**
- Admin: All permissions
- Editor: Create, read, update posts
- Viewer: Read posts only

**Permissions:**
- users:read, users:update
- posts:create, posts:read, posts:update, posts:delete
```

---

## Database Schema Design

### SQL Schema

```sql
-- rbac-schema.sql

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Roles table
CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Permissions table
CREATE TABLE permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) UNIQUE NOT NULL,
    resource VARCHAR(100) NOT NULL,
    action VARCHAR(50) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User roles junction table
CREATE TABLE user_roles (
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    role_id UUID REFERENCES roles(id) ON DELETE CASCADE,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, role_id)
);

-- Role permissions junction table
CREATE TABLE role_permissions (
    role_id UUID REFERENCES roles(id) ON DELETE CASCADE,
    permission_id UUID REFERENCES permissions(id) ON DELETE CASCADE,
    PRIMARY KEY (role_id, permission_id)
);

-- User permissions junction table (for direct permissions)
CREATE TABLE user_permissions (
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    permission_id UUID REFERENCES permissions(id) ON DELETE CASCADE,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, permission_id)
);

-- Role hierarchy table
CREATE TABLE role_hierarchy (
    parent_id UUID REFERENCES roles(id) ON DELETE CASCADE,
    child_id UUID REFERENCES roles(id) ON DELETE CASCADE,
    PRIMARY KEY (parent_id, child_id)
);

-- Indexes
CREATE INDEX idx_user_roles_user_id ON user_roles(user_id);
CREATE INDEX idx_user_roles_role_id ON user_roles(role_id);
CREATE INDEX idx_role_permissions_role_id ON role_permissions(role_id);
CREATE INDEX idx_role_permissions_permission_id ON role_permissions(permission_id);
```

### MongoDB Schema

```typescript
// rbac-mongodb.ts
export interface UserDocument {
  _id: string;
  email: string;
  passwordHash: string;
  name: string;
  roles: string[];
  permissions: string[];
  createdAt: Date;
  updatedAt: Date;
}

export interface RoleDocument {
  _id: string;
  name: string;
  description: string;
  permissions: string[];
  parentRoles: string[];
  createdAt: Date;
}

export interface PermissionDocument {
  _id: string;
  name: string;
  resource: string;
  action: string;
  description: string;
  createdAt: Date;
}
```

---

## Implementation

### Middleware Implementation

```typescript
// rbac-middleware.ts
import { Request, Response, NextFunction } from 'express';

export interface RBACRequest extends Request {
  user?: any;
}

export class RBACMiddleware {
  constructor(private rbacService: RBACService) {}
  
  requirePermission(resource: string, action: string) {
    return (req: RBACRequest, res: Response, next: NextFunction) => {
      if (!req.user) {
        return res.status(401).json({ error: 'Authentication required' });
      }
      
      const hasPermission = this.rbacService.hasPermission(
        req.user.id,
        resource,
        action
      );
      
      if (!hasPermission) {
        return res.status(403).json({ 
          error: 'Insufficient permissions',
          required: `${resource}:${action}`
        });
      }
      
      next();
    };
  }
  
  requireRole(roleName: string) {
    return (req: RBACRequest, res: Response, next: NextFunction) => {
      if (!req.user) {
        return res.status(401).json({ error: 'Authentication required' });
      }
      
      const hasRole = this.rbacService.hasRole(req.user.id, roleName);
      
      if (!hasRole) {
        return res.status(403).json({ 
          error: 'Insufficient role',
          required: roleName
        });
      }
      
      next();
    };
  }
  
  requireAnyRole(roleNames: string[]) {
    return (req: RBACRequest, res: Response, next: NextFunction) => {
      if (!req.user) {
        return res.status(401).json({ error: 'Authentication required' });
      }
      
      const hasAnyRole = this.rbacService.hasAnyRole(req.user.id, roleNames);
      
      if (!hasAnyRole) {
        return res.status(403).json({ 
          error: 'Insufficient role',
          required: roleNames.join(' or ')
        });
      }
      
      next();
    };
  }
}
```

### Service Implementation

```typescript
// rbac-service.ts
export class RBACService {
  constructor(
    private userRepository: UserRepository,
    private roleRepository: RoleRepository,
    private permissionRepository: PermissionRepository
  ) {}
  
  async hasPermission(userId: string, resource: string, action: string): Promise<boolean> {
    const user = await this.userRepository.findById(userId);
    if (!user) return false;
    
    // Check direct user permissions
    const userPermissions = await this.getUserPermissions(userId);
    const hasDirectPermission = userPermissions.some(
      p => p.resource === resource && (p.action === action || p.action === '*')
    );
    if (hasDirectPermission) return true;
    
    // Check role permissions
    const roles = await this.getUserRoles(userId);
    for (const role of roles) {
      const rolePermissions = await this.getRolePermissions(role.id);
      const hasRolePermission = rolePermissions.some(
        p => p.resource === resource && (p.action === action || p.action === '*')
      );
      if (hasRolePermission) return true;
    }
    
    return false;
  }
  
  async hasRole(userId: string, roleName: string): Promise<boolean> {
    const roles = await this.getUserRoles(userId);
    return roles.some(r => r.name === roleName);
  }
  
  async hasAnyRole(userId: string, roleNames: string[]): Promise<boolean> {
    const roles = await this.getUserRoles(userId);
    return roles.some(r => roleNames.includes(r.name));
  }
  
  async assignRole(userId: string, roleId: string): Promise<void> {
    await this.userRepository.addRole(userId, roleId);
  }
  
  async removeRole(userId: string, roleId: string): Promise<void> {
    await this.userRepository.removeRole(userId, roleId);
  }
  
  async assignPermission(userId: string, permissionId: string): Promise<void> {
    await this.userRepository.addPermission(userId, permissionId);
  }
  
  async removePermission(userId: string, permissionId: string): Promise<void> {
    await this.userRepository.removePermission(userId, permissionId);
  }
  
  private async getUserPermissions(userId: string): Promise<Permission[]> {
    return await this.userRepository.getPermissions(userId);
  }
  
  private async getUserRoles(userId: string): Promise<Role[]> {
    return await this.userRepository.getRoles(userId);
  }
  
  private async getRolePermissions(roleId: string): Promise<Permission[]> {
    return await this.roleRepository.getPermissions(roleId);
  }
}
```

---

## Role Hierarchy

### Hierarchical Roles

```typescript
// role-hierarchy.ts
export class RoleHierarchy {
  constructor(private roleRepository: RoleRepository) {}
  
  async getEffectiveRoles(userId: string): Promise<Role[]> {
    const directRoles = await this.roleRepository.getUserRoles(userId);
    const effectiveRoles = new Set<string>();
    
    // Add direct roles
    for (const role of directRoles) {
      await this.collectParentRoles(role.id, effectiveRoles);
    }
    
    return Array.from(effectiveRoles).map(id => ({ id }));
  }
  
  private async collectParentRoles(roleId: string, collected: Set<string>): Promise<void> {
    if (collected.has(roleId)) return;
    
    collected.add(roleId);
    
    // Get parent roles
    const parentRoles = await this.roleRepository.getParentRoles(roleId);
    
    for (const parentRole of parentRoles) {
      await this.collectParentRoles(parentRole.id, collected);
    }
  }
  
  async getEffectivePermissions(userId: string): Promise<Permission[]> {
    const effectiveRoles = await this.getEffectiveRoles(userId);
    const permissions = new Set<string>();
    
    for (const role of effectiveRoles) {
      const rolePermissions = await this.roleRepository.getPermissions(role.id);
      for (const permission of rolePermissions) {
        permissions.add(permission.id);
      }
    }
    
    // Add direct user permissions
    const userPermissions = await this.roleRepository.getUserPermissions(userId);
    for (const permission of userPermissions) {
      permissions.add(permission.id);
    }
    
    return Array.from(permissions).map(id => ({ id }));
  }
}

// Example role hierarchy
// Admin -> Editor -> Viewer
// Admin has all permissions
// Editor inherits from Viewer
// Viewer has read-only permissions
```

---

## Permission Checking

### Permission Checker

```typescript
// permission-checker.ts
export class PermissionChecker {
  constructor(private rbacService: RBACService) {}
  
  can(resource: string, action: string): MethodDecorator {
    return (target: any, propertyKey: string, descriptor: PropertyDescriptor) => {
      const originalMethod = descriptor.value;
      
      descriptor.value = async function (...args: any[]) {
        const userId = this['user']?.id;
        
        if (!userId) {
          throw new Error('Authentication required');
        }
        
        const hasPermission = await this.rbacService.hasPermission(
          userId,
          resource,
          action
        );
        
        if (!hasPermission) {
          throw new Error(`Permission denied: ${resource}:${action}`);
        }
        
        return originalMethod.apply(this, args);
      };
      
      return descriptor;
    };
  }
  
  hasRole(roleName: string): MethodDecorator {
    return (target: any, propertyKey: string, descriptor: PropertyDescriptor) => {
      const originalMethod = descriptor.value;
      
      descriptor.value = async function (...args: any[]) {
        const userId = this['user']?.id;
        
        if (!userId) {
          throw new Error('Authentication required');
        }
        
        const hasRole = await this.rbacService.hasRole(userId, roleName);
        
        if (!hasRole) {
          throw new Error(`Role required: ${roleName}`);
        }
        
        return originalMethod.apply(this, args);
      };
      
      return descriptor;
    };
  }
}

// Usage example
class UserService {
  constructor(private rbacService: RBACService) {}
  
  @PermissionChecker.prototype.can('users', 'read')
  async getUsers() {
    // This method requires users:read permission
    return await User.find();
  }
  
  @PermissionChecker.prototype.hasRole('admin')
  async deleteUser(userId: string) {
    // This method requires admin role
    return await User.delete(userId);
  }
}
```

---

## Dynamic Permissions

### Dynamic Permission Assignment

```typescript
// dynamic-permissions.ts
export class DynamicPermissionManager {
  constructor(
    private permissionRepository: PermissionRepository,
    private userRepository: UserRepository
  ) {}
  
  async createPermission(
    resource: string,
    action: string,
    description: string
  ): Promise<Permission> {
    return await this.permissionRepository.create({
      name: `${resource}:${action}`,
      resource,
      action,
      description
    });
  }
  
  async grantPermissionToUser(
    userId: string,
    resource: string,
    action: string
  ): Promise<void> {
    const permission = await this.permissionRepository.findByResourceAction(
      resource,
      action
    );
    
    if (!permission) {
      permission = await this.createPermission(resource, action, '');
    }
    
    await this.userRepository.addPermission(userId, permission.id);
  }
  
  async grantPermissionToRole(
    roleId: string,
    resource: string,
    action: string
  ): Promise<void> {
    const permission = await this.permissionRepository.findByResourceAction(
      resource,
      action
    );
    
    if (!permission) {
      permission = await this.createPermission(resource, action, '');
    }
    
    await this.roleRepository.addPermission(roleId, permission.id);
  }
  
  async revokePermissionFromUser(
    userId: string,
    resource: string,
    action: string
  ): Promise<void> {
    const permission = await this.permissionRepository.findByResourceAction(
      resource,
      action
    );
    
    if (permission) {
      await this.userRepository.removePermission(userId, permission.id);
    }
  }
}
```

---

## UI-Based Authorization

### Frontend Permission Check

```typescript
// ui-authorization.ts
export class UIAuthorization {
  static hasPermission(userPermissions: string[], resource: string, action: string): boolean {
    const permission = `${resource}:${action}`;
    return userPermissions.includes(permission) || userPermissions.includes('*:*');
  }
  
  static hasRole(userRoles: string[], roleName: string): boolean {
    return userRoles.includes(roleName);
  }
  
  static canAccess(userPermissions: string[], resource: string, action: string): boolean {
    return this.hasPermission(userPermissions, resource, action);
  }
}

// React component
import { useEffect, useState } from 'react';

interface PermissionGateProps {
  userPermissions: string[];
  resource: string;
  action: string;
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

export function PermissionGate({
  userPermissions,
  resource,
  action,
  children,
  fallback
}: PermissionGateProps) {
  const [canAccess, setCanAccess] = useState(false);
  
  useEffect(() => {
    const allowed = UIAuthorization.hasPermission(
      userPermissions,
      resource,
      action
    );
    setCanAccess(allowed);
  }, [userPermissions, resource, action]);
  
  return canAccess ? <>{children}</> : <>{fallback}</>;
}

// Usage
function UserList({ user }) {
  return (
    <div>
      <PermissionGate
        userPermissions={user.permissions}
        resource="users"
        action="read"
        fallback={<div>You don't have permission to view users</div>}
      >
        <UserTable />
      </PermissionGate>
      
      <PermissionGate
        userPermissions={user.permissions}
        resource="users"
        action="create"
        fallback={null}
      >
        <Button>Create User</Button>
      </PermissionGate>
    </div>
  );
}
```

---

## API Authorization

### Express API

```typescript
// api-authorization.ts
import express from 'express';
import { RBACMiddleware, RBACRequest } from './rbac-middleware';

const app = express();
const rbac = new RBACMiddleware(rbacService);

// Protected routes
app.get('/api/users', rbac.requirePermission('users', 'list'), async (req, res) => {
  const users = await User.find();
  res.json(users);
});

app.get('/api/users/:id', rbac.requirePermission('users', 'read'), async (req, res) => {
  const user = await User.findById(req.params.id);
  res.json(user);
});

app.post('/api/users', rbac.requirePermission('users', 'create'), async (req, res) => {
  const user = await User.create(req.body);
  res.status(201).json(user);
});

app.put('/api/users/:id', rbac.requirePermission('users', 'update'), async (req, res) => {
  const user = await User.update(req.params.id, req.body);
  res.json(user);
});

app.delete('/api/users/:id', rbac.requirePermission('users', 'delete'), async (req, res) => {
  await User.delete(req.params.id);
  res.status(204).send();
});

// Admin routes
app.get('/api/admin/stats', rbac.requireRole('admin'), async (req, res) => {
  const stats = await getAdminStats();
  res.json(stats);
});
```

### FastAPI

```python
# api_authorization.py
from fastapi import Depends, HTTPException, status
from typing import List
from functools import wraps

class RBACMiddleware:
    def __init__(self, rbac_service):
        self.rbac_service = rbac_service
    
    def require_permission(self, resource: str, action: str):
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                user = kwargs.get('current_user')
                
                if not user:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail='Authentication required'
                    )
                
                has_permission = await self.rbac_service.has_permission(
                    user['id'],
                    resource,
                    action
                )
                
                if not has_permission:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f'Permission denied: {resource}:{action}'
                    )
                
                return await func(*args, **kwargs)
            return wrapper
        return decorator
    
    def require_role(self, role_name: str):
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                user = kwargs.get('current_user')
                
                if not user:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail='Authentication required'
                    )
                
                has_role = await self.rbac_service.has_role(user['id'], role_name)
                
                if not has_role:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f'Role required: {role_name}'
                    )
                
                return await func(*args, **kwargs)
            return wrapper
        return decorator

# Usage
rbac = RBACMiddleware(rbac_service)

@app.get('/api/users')
@rbac.require_permission('users', 'list')
async def list_users(current_user: dict = Depends(get_current_user)):
    users = await User.find_all()
    return users

@app.get('/api/users/{user_id}')
@rbac.require_permission('users', 'read')
async def get_user(user_id: str, current_user: dict = Depends(get_current_user)):
    user = await User.find_by_id(user_id)
    return user

@app.post('/api/users')
@rbac.require_permission('users', 'create')
async def create_user(user_data: dict, current_user: dict = Depends(get_current_user)):
    user = await User.create(user_data)
    return user

@app.get('/api/admin/stats')
@rbac.require_role('admin')
async def get_admin_stats(current_user: dict = Depends(get_current_user)):
    stats = await get_admin_stats()
    return stats
```

---

## Testing RBAC

### Unit Tests

```typescript
// rbac.test.ts
import { describe, it, expect, beforeEach } from '@jest/globals';
import { RBACService } from './rbac-service';

describe('RBAC Service', () => {
  let rbacService: RBACService;
  
  beforeEach(() => {
    rbacService = new RBACService(
      mockUserRepository,
      mockRoleRepository,
      mockPermissionRepository
    );
  });
  
  describe('Permission Checking', () => {
    it('should grant permission when user has direct permission', async () => {
      mockUserRepository.getPermissions.mockResolvedValue([
        { resource: 'users', action: 'read' }
      ]);
      
      const hasPermission = await rbacService.hasPermission('user-1', 'users', 'read');
      
      expect(hasPermission).toBe(true);
    });
    
    it('should grant permission when user has role with permission', async () => {
      mockUserRepository.getRoles.mockResolvedValue([
        { id: 'role-1', name: 'editor' }
      ]);
      mockRoleRepository.getPermissions.mockResolvedValue([
        { resource: 'users', action: 'read' }
      ]);
      
      const hasPermission = await rbacService.hasPermission('user-1', 'users', 'read');
      
      expect(hasPermission).toBe(true);
    });
    
    it('should deny permission when user lacks permission', async () => {
      mockUserRepository.getPermissions.mockResolvedValue([]);
      mockUserRepository.getRoles.mockResolvedValue([]);
      
      const hasPermission = await rbacService.hasPermission('user-1', 'users', 'delete');
      
      expect(hasPermission).toBe(false);
    });
  });
  
  describe('Role Hierarchy', () => {
    it('should inherit permissions from parent roles', async () => {
      mockUserRepository.getUserRoles.mockResolvedValue([
        { id: 'viewer', name: 'viewer' }
      ]);
      mockRoleRepository.getParentRoles.mockResolvedValue([
        { id: 'editor', name: 'editor' }
      ]);
      mockRoleRepository.getPermissions.mockImplementation(async (roleId) => {
        if (roleId === 'viewer') return [];
        if (roleId === 'editor') return [{ resource: 'posts', action: 'read' }];
        return [];
      });
      
      const effectivePermissions = await rbacService.getEffectivePermissions('user-1');
      
      expect(effectivePermissions).toContainEqual(
        { id: expect.any(String), resource: 'posts', action: 'read' }
      );
    });
  });
});
```

---

## Common Patterns

### Resource Owner Pattern

```typescript
// resource-owner.ts
export class ResourceOwnerPattern {
  constructor(private rbacService: RBACService) {}
  
  async checkResourceOwnership(
    userId: string,
    resourceType: string,
    resourceId: string
  ): Promise<boolean> {
    // Check if user owns the resource
    const resource = await this.findResource(resourceType, resourceId);
    
    if (!resource) return false;
    
    // Owner always has full access
    if (resource.ownerId === userId) {
      return true;
    }
    
    // Otherwise check permissions
    return await this.rbacService.hasPermission(userId, resourceType, 'update');
  }
  
  async requireResourceOwnership(resourceType: string, resourceIdParam: string) {
    return (req: RBACRequest, res: Response, next: NextFunction) => {
      const userId = req.user?.id;
      
      if (!userId) {
        return res.status(401).json({ error: 'Authentication required' });
      }
      
      const resourceId = req.params[resourceIdParam];
      const hasAccess = await this.checkResourceOwnership(
        userId,
        resourceType,
        resourceId
      );
      
      if (!hasAccess) {
        return res.status(403).json({ 
          error: 'Access denied: you don't own this resource'
        });
      }
      
      next();
    };
  }
  
  private async findResource(resourceType: string, resourceId: string): Promise<any> {
    // Implementation
    return { ownerId: 'user-123' };
  }
}

// Usage
app.put(
  '/api/posts/:id',
  resourceOwnerPattern.requireResourceOwnership('posts', 'id'),
  async (req, res) => {
    const post = await Post.update(req.params.id, req.body);
    res.json(post);
  }
);
```

---

## Best Practices

### RBAC Checklist

```markdown
## RBAC Best Practices Checklist

### Design
- [ ] Use principle of least privilege
- [ ] Define clear resource-action pairs
- [ ] Implement role hierarchy
- [ ] Keep roles focused and specific
- [ ] Avoid overly broad permissions

### Implementation
- [ ] Cache permissions for performance
- [ ] Implement permission inheritance
- [ ] Support dynamic permissions
- [ ] Log permission checks
- [ ] Implement permission revocation

### Security
- [ ] Validate all permission checks
- [ ] Use middleware for enforcement
- [ ] Implement audit logging
- [ ] Regular permission audits
- [ ] Monitor for permission escalation

### Testing
- [ ] Test permission grants
- [ ] Test permission denials
- [ ] Test role inheritance
- [ ] Test edge cases
- [ ] Test performance

### UI
- [ ] Hide/show features based on permissions
- [ ] Provide clear error messages
- [ ] Implement permission-based navigation
- [ ] Cache permissions on client
- [ ] Update permissions on login
```

---

## Additional Resources

- [NIST RBAC](https://csrc.nist.gov/projects/role-based-access-control)
- [OWASP Access Control](https://owasp.org/www-project-access-control)
- [Casbin](https://casbin.org/)
- [Node-Casbin](https://github.com/casbin/node-casbin)
- [Casbin Python](https://github.com/casbin/pycasbin)
