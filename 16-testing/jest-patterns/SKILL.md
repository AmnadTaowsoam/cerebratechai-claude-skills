# Jest Patterns

## Overview

Jest is a JavaScript testing framework that focuses on simplicity. This skill covers Jest setup, test structure, mocking, and best practices.

## Table of Contents

1. [Jest Setup](#jest-setup)
2. [Test Structure](#test-structure)
3. [Assertions and Matchers](#assertions-and-matchers)
4. [Mocking](#mocking)
5. [Async Testing](#async-testing)
6. [Snapshot Testing](#snapshot-testing)
7. [Coverage](#coverage)
8. [Setup and Teardown](#setup-and-teardown)
9. [Testing React Components](#testing-react-components)
10. [Testing API Calls](#testing-api-calls)
11. [Best Practices](#best-practices)

---

## Jest Setup

### Basic Setup

```bash
npm install --save-dev jest @types/jest
```

```json
// package.json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage"
  },
  "devDependencies": {
    "jest": "^29.0.0",
    "@types/jest": "^29.0.0",
    "ts-jest": "^29.0.0",
    "ts-node": "^29.0.0"
  }
}
```

### TypeScript Configuration

```json
// jest.config.js
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/src'],
  testMatch: ['**/__tests__/**/*.ts', '**/?(*.)+(spec|test).ts'],
  collectCoverageFrom: [
    'src/**/*.{js,ts}',
  ],
  coverageDirectory: 'coverage',
  collectCoverage: true,
};
```

```json
// tsconfig.json
{
  "compilerOptions": {
    "types": ["node", "jest"]
  }
}
```

### React Testing Setup

```bash
npm install --save-dev jest @testing-library/react @testing-library/jest-dom @testing-library/user-event jest-environment-jsdom
```

```json
// jest.config.js
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.ts'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/node_modules/@$1',
  },
  testMatch: ['**/__tests__/**/*.test.tsx', '**/?(*.)+(spec|test).test.tsx'],
};
```

```typescript
// src/setupTests.ts
import '@testing-library/jest-dom';
```

---

## Test Structure

### Basic Test Structure

```typescript
// math.test.ts
describe('Math operations', () => {
  describe('addition', () => {
    it('should add two numbers', () => {
      expect(add(2, 3)).toBe(5);
    });

    it('should handle negative numbers', () => {
      expect(add(-2, 3)).toBe(1);
    });
  });

  describe('subtraction', () => {
    it('should subtract two numbers', () => {
      expect(subtract(5, 3)).toBe(2);
    });
  });
});
```

### Nested Describes

```typescript
// user.test.ts
describe('User', () => {
  describe('constructor', () => {
    it('should create a user with name', () => {
      const user = new User('John');
      expect(user.name).toBe('John');
    });

    it('should create a user with email', () => {
      const user = new User('John', 'john@example.com');
      expect(user.email).toBe('john@example.com');
    });
  });

  describe('methods', () => {
    let user: User;

    beforeEach(() => {
      user = new User('John', 'john@example.com');
    });

    it('should get full name', () => {
      expect(user.getFullName()).toBe('John');
    });

    it('should validate email', () => {
      expect(user.validateEmail()).toBe(true);
    });
  });
});
```

---

## Assertions and Matchers

### Common Matchers

```typescript
// matchers.test.ts
describe('Common matchers', () => {
  describe('toBe', () => {
    it('should check exact equality', () => {
      expect(2 + 2).toBe(4);
    });
  });

  describe('toEqual', () => {
    it('should check deep equality', () => {
      const obj1 = { a: 1, b: 2 };
      const obj2 = { a: 1, b: 2 };
      expect(obj1).toEqual(obj2);
    });
  });

  describe('toStrictEqual', () => {
    it('should check strict equality', () => {
      const obj1 = { a: 1, b: 2 };
      const obj2 = { a: 1, b: 2 };
      expect(obj1).toStrictEqual(obj2);
    });
  });

  describe('toBeNull', () => {
    it('should check for null', () => {
      expect(null).toBeNull();
    });
  });

  describe('toBeUndefined', () => {
    it('should check for undefined', () => {
      expect(undefined).toBeUndefined();
    });
  });

  describe('toBeDefined', () => {
    it('should check if defined', () => {
      const value = 'hello';
      expect(value).toBeDefined();
    });
  });

  describe('toBeTruthy', () => {
    it('should check for truthy', () => {
      expect(true).toBeTruthy();
      expect(1).toBeTruthy();
      expect('hello').toBeTruthy();
      expect({}).toBeTruthy();
    });
  });

  describe('toBeFalsy', () => {
    it('should check for falsy', () => {
      expect(false).toBeFalsy();
      expect(0).toBeFalsy();
      expect('').toBeFalsy();
      expect(null).toBeFalsy();
      expect(undefined).toBeFalsy();
    });
  });

  describe('toContain', () => {
    it('should check if array contains item', () => {
      const array = [1, 2, 3, 4, 5];
      expect(array).toContain(3);
    });
  });

  describe('toHaveLength', () => {
    it('should check array length', () => {
      const array = [1, 2, 3];
      expect(array).toHaveLength(3);
    });
  });

  describe('toThrow', () => {
    it('should check if function throws', () => {
      expect(() => {
        throw new Error('Test error');
      }).toThrow('Test error');
    });

    it('should check if function throws any error', () => {
      expect(() => {
        throw new Error('Test error');
      }).toThrow();
    });
  });
});
```

### String Matchers

```typescript
// string-matchers.test.ts
describe('String matchers', () => {
  describe('toMatch', () => {
    it('should match string', () => {
      expect('hello world').toMatch(/world/);
    });
  });

  describe('toContain', () => {
    it('should contain substring', () => {
      expect('hello world').toContain('world');
    });
  });

  describe('toHaveLength', () => {
    it('should have length', () => {
      expect('hello').toHaveLength(5);
    });
  });

  describe('toStartWith', () => {
    it('should start with', () => {
      expect('hello world').toStartWith('hello');
    });
  });

  describe('toEndWith', () => {
    it('should end with', () => {
      expect('hello world').toEndWith('world');
    });
  });
});
```

### Number Matchers

```typescript
// number-matchers.test.ts
describe('Number matchers', () => {
  describe('toBeGreaterThan', () => {
    it('should be greater than', () => {
      expect(5).toBeGreaterThan(3);
    });
  });

  describe('toBeGreaterThanOrEqual', () => {
    it('should be greater than or equal', () => {
      expect(5).toBeGreaterThanOrEqual(5);
    });
  });

  describe('toBeLessThan', () => {
    it('should be less than', () => {
      expect(3).toBeLessThan(5);
    });
  });

  describe('toBeLessThanOrEqual', () => {
    it('should be less than or equal', () => {
      expect(3).toBeLessThanOrEqual(3);
    });
  });

  describe('toBeCloseTo', () => {
    it('should be close to', () => {
      expect(0.1 + 0.2).toBeCloseTo(0.3, 5);
    });
  });

  describe('toBeFinite', () => {
    it('should be finite', () => {
      expect(42).toBeFinite();
    });
  });

  describe('toBeNaN', () => {
    it('should be NaN', () => {
      expect(NaN).toBeNaN();
    });
  });
});
```

---

## Mocking

### Mocking Functions

```typescript
// function-mock.test.ts
describe('Function mocking', () => {
  it('should mock a function', () => {
    const mockFn = jest.fn();
    mockFn('hello', 'world');

    expect(mockFn).toHaveBeenCalledWith('hello', 'world');
    expect(mockFn).toHaveBeenCalledTimes(1);
  });

  it('should return a value', () => {
    const mockFn = jest.fn().mockReturnValue(42);
    expect(mockFn()).toBe(42);
  });

  it('should resolve a promise', async () => {
    const mockFn = jest.fn().mockResolvedValue(42);
    const result = await mockFn();
    expect(result).toBe(42);
  });

  it('should reject a promise', async () => {
    const mockFn = jest.fn().mockRejectedValue(new Error('Test error'));
    await expect(mockFn()).rejects.toThrow('Test error');
  });
});
```

### Mocking Modules

```typescript
// module-mock.test.ts
import { fetchData } from './api';

jest.mock('./api');

describe('Module mocking', () => {
  it('should mock module', async () => {
    const mockFetchData = jest.mocked(fetchData).mockResolvedValue({ data: 'test' });
    const result = await mockFetchData();
    expect(result).toEqual({ data: 'test' });
  });
});
```

### Mocking Implementations

```typescript
// implementation-mock.test.ts
import { UserService } from './services';

jest.mock('./services');

describe('Implementation mocking', () => {
  it('should mock class methods', async () => {
    const mockUserService = jest.mocked(UserService);
    mockUserService.getUser.mockResolvedValue({ id: 1, name: 'John' });

    const user = await mockUserService.getUser(1);
    expect(user).toEqual({ id: 1, name: 'John' });
  });
});
```

---

## Async Testing

### Promise Testing

```typescript
// promise.test.ts
describe('Promise testing', () => {
  it('should resolve promise', async () => {
    const promise = Promise.resolve(42);
    await expect(promise).resolves.toBe(42);
  });

  it('should reject promise', async () => {
    const promise = Promise.reject(new Error('Test error'));
    await expect(promise).rejects.toThrow('Test error');
  });

  it('should handle multiple promises', async () => {
    const promises = [
      Promise.resolve(1),
      Promise.resolve(2),
      Promise.resolve(3),
    ];
    const result = await Promise.all(promises);
    expect(result).toEqual([1, 2, 3]);
  });
});
```

### Async/Await Testing

```typescript
// async-await.test.ts
describe('Async/await testing', () => {
  it('should handle async function', async () => {
    const result = await asyncFunction();
    expect(result).toBe('test');
  });

  it('should handle async error', async () => {
    await expect(asyncFunction()).rejects.toThrow('Test error');
  });
});

async function asyncFunction(): Promise<string> {
  return 'test';
}
```

### Callback Testing

```typescript
// callback.test.ts
describe('Callback testing', () => {
  it('should handle callback', (done) => {
    functionWithCallback((result: string) => {
      expect(result).toBe('test');
      done();
    });
  });
});

function functionWithCallback(callback: (result: string) => void): void {
  callback('test');
}
```

---

## Snapshot Testing

### Basic Snapshot

```typescript
// component.test.tsx
import { render } from '@testing-library/react';
import Component from './Component';

describe('Component snapshot', () => {
  it('should match snapshot', () => {
    const { asFragment } = render(<Component />);
    expect(asFragment()).toMatchSnapshot();
  });
});
```

### Inline Snapshot

```typescript
// inline-snapshot.test.tsx
describe('Inline snapshot', () => {
  it('should match inline snapshot', () => {
    const data = {
      name: 'John',
      age: 30,
      email: 'john@example.com',
    };
    expect(data).toMatchInlineSnapshot(`
      Object {
        "name": "John",
        "age": 30,
        "email": "john@example.com"
      }
    `);
  });
});
```

---

## Coverage

### Coverage Configuration

```json
// jest.config.js
module.exports = {
  collectCoverageFrom: [
    'src/**/*.{js,ts}',
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
    './src/components/': {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
};
```

### Coverage Exclusions

```json
// jest.config.js
module.exports = {
  collectCoverageFrom: [
    'src/**/*.{js,ts}',
  ],
  coveragePathIgnorePatterns: [
    '/node_modules/',
    '/dist/',
    '/coverage/',
    '/src/types/',
  ],
};
```

---

## Setup and Teardown

### beforeEach and afterEach

```typescript
// setup-teardown.test.ts
describe('Setup and teardown', () => {
  let counter: number;

  beforeEach(() => {
    counter = 0;
  });

  afterEach(() => {
    counter = 0;
  });

  it('should increment counter', () => {
    counter++;
    expect(counter).toBe(1);
  });

  it('should reset counter', () => {
    counter++;
    expect(counter).toBe(1);
  });
});
```

### beforeAll and afterAll

```typescript
// setup-teardown-all.test.ts
describe('Setup and teardown all', () => {
  let database: Database;

  beforeAll(async () => {
    database = new Database();
    await database.connect();
  });

  afterAll(async () => {
    await database.disconnect();
  });

  it('should query database', async () => {
    const result = await database.query('SELECT * FROM users');
    expect(result).toBeDefined();
  });
});
```

---

## Testing React Components

### Basic Component Test

```typescript
// Button.test.tsx
import { render, screen } from '@testing-library/react';
import Button from './Button';

describe('Button', () => {
  it('should render button', () => {
    render(<Button>Click me</Button>);
    const button = screen.getByRole('button');
    expect(button).toBeInTheDocument();
  });

  it('should render button text', () => {
    render(<Button>Click me</Button>);
    const button = screen.getByRole('button');
    expect(button).toHaveTextContent('Click me');
  });
});
```

### Event Testing

```typescript
// Button-event.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import Button from './Button';

describe('Button events', () => {
  it('should call onClick handler', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    const button = screen.getByRole('button');
    fireEvent.click(button);
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

### Props Testing

```typescript
// Button-props.test.tsx
import { render, screen } from '@testing-library/react';
import Button from './Button';

describe('Button props', () => {
  it('should render with custom className', () => {
    render(<Button className="custom-class">Click me</Button>);
    const button = screen.getByRole('button');
    expect(button).toHaveClass('custom-class');
  });

  it('should render with disabled state', () => {
    render(<Button disabled>Click me</Button>);
    const button = screen.getByRole('button');
    expect(button).toBeDisabled();
  });
});
```

### Form Testing

```typescript
// Form.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Form from './Form';

describe('Form', () => {
  it('should submit form', async () => {
    const handleSubmit = jest.fn();
    render(<Form onSubmit={handleSubmit} />);

    const nameInput = screen.getByLabelText('Name');
    const emailInput = screen.getByLabelText('Email');
    const submitButton = screen.getByRole('button', { name: 'submit' });

    fireEvent.change(nameInput, { target: { value: 'John' } });
    fireEvent.change(emailInput, { target: { value: 'john@example.com' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(handleSubmit).toHaveBeenCalledWith({
        name: 'John',
        email: 'john@example.com',
      });
    });
  });
});
```

---

## Testing API Calls

### Mocking API Calls

```typescript
// api.test.ts
import { fetchUser } from './api';
import { fetchUser as mockFetchUser } from './api';

jest.mock('./api');

describe('API calls', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should fetch user', async () => {
    const mockUser = { id: 1, name: 'John' };
    mockFetchUser.mockResolvedValue(mockUser);

    const user = await fetchUser(1);
    expect(user).toEqual(mockUser);
    expect(mockFetchUser).toHaveBeenCalledWith(1);
  });

  it('should handle API error', async () => {
    mockFetchUser.mockRejectedValue(new Error('Not found'));

    await expect(fetchUser(999)).rejects.toThrow('Not found');
  });
});
```

### Testing with MSW

```typescript
// api-msw.test.ts
import { rest } from 'msw';
import { fetchUser } from './api';

describe('API with MSW', () => {
  beforeAll(() => {
    server.listen();
  });

  afterAll(() => {
    server.close();
  });

  it('should fetch user', async () => {
    server.use(
      rest.get('https://api.example.com/users/:id', (req, res, ctx) => {
        res(ctx.json({ id: 1, name: 'John' }));
      })
    );

    const user = await fetchUser(1);
    expect(user).toEqual({ id: 1, name: 'John' });
  });
});
```

---

## Best Practices

### 1. Write Descriptive Tests

```typescript
// Good
describe('UserService', () => {
  describe('getUser', () => {
    it('should return user when user exists', async () => {
      const user = await userService.getUser(1);
      expect(user).toBeDefined();
    });
  });
});

// Bad
describe('UserService', () => {
  it('test 1', async () => {
    const user = await userService.getUser(1);
    expect(user).toBeDefined();
  });
});
```

### 2. Test One Thing Per Test

```typescript
// Good
it('should return user when user exists', async () => {
  const user = await userService.getUser(1);
  expect(user).toBeDefined();
});

it('should return null when user does not exist', async () => {
  const user = await userService.getUser(999);
  expect(user).toBeNull();
});

// Bad
it('should handle user existence', async () => {
  const user1 = await userService.getUser(1);
  expect(user1).toBeDefined();

  const user2 = await userService.getUser(999);
  expect(user2).toBeNull();
});
```

### 3. Use Arrange-Act-Assert Pattern

```typescript
describe('Arrange-Act-Assert', () => {
  it('should add two numbers', () => {
    // Arrange
    const a = 2;
    const b = 3;

    // Act
    const result = add(a, b);

    // Assert
    expect(result).toBe(5);
  });
});
```

### 4. Use Test Helpers

```typescript
// test-helpers.ts
export const createMockUser = (overrides: Partial<User> = {}): User => ({
  id: 1,
  name: 'John',
  email: 'john@example.com',
  ...overrides,
});

export const createMockUsers = (count: number): User[] => {
  return Array.from({ length: count }, (_, i) => createMockUser({ id: i + 1 }));
};

// test.ts
import { createMockUser } from './test-helpers';

describe('With helpers', () => {
  it('should use mock user', () => {
    const user = createMockUser({ name: 'Jane' });
    expect(user.name).toBe('Jane');
  });
});
```

### 5. Keep Tests Independent

```typescript
// Good
describe('Independent tests', () => {
  it('should create user', () => {
    const user = new User('John');
    expect(user.name).toBe('John');
  });

  it('should update user', () => {
    const user = new User('Jane');
    user.name = 'Updated';
    expect(user.name).toBe('Updated');
  });
});

// Bad - tests depend on each other
describe('Dependent tests', () => {
  let user: User;

  it('should create user', () => {
    user = new User('John');
    expect(user.name).toBe('John');
  });

  it('should update user', () => {
    user.name = 'Updated';
    expect(user.name).toBe('Updated');
  });
});
```

---

## Summary

This skill covers comprehensive Jest testing patterns including:

- **Jest Setup**: Basic setup, TypeScript configuration, React testing setup
- **Test Structure**: Basic and nested describe blocks
- **Assertions and Matchers**: Common, string, and number matchers
- **Mocking**: Functions, modules, and implementations
- **Async Testing**: Promises, async/await, and callbacks
- **Snapshot Testing**: Basic and inline snapshots
- **Coverage**: Configuration and exclusions
- **Setup and Teardown**: beforeEach, afterEach, beforeAll, afterAll
- **Testing React Components**: Basic component, events, props, and form testing
- **Testing API Calls**: Mocking API calls and MSW
- **Best Practices**: Descriptive tests, one thing per test, AAA pattern, helpers, independent tests
