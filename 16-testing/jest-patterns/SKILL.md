# Jest Patterns

A comprehensive guide to Jest testing patterns for JavaScript/TypeScript applications.

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

### Installation

```bash
# Install Jest
npm install --save-dev jest

# Install TypeScript support
npm install --save-dev ts-jest @types/jest

# Install React testing utilities
npm install --save-dev @testing-library/react @testing-library/jest-dom

# Install additional matchers
npm install --save-dev @testing-library/jest-dom
```

### Configuration

```javascript
// jest.config.js
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
  },
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/*.stories.{js,jsx,ts,tsx}',
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
};
```

```javascript
// jest.setup.js
import '@testing-library/jest-dom';

// Global mocks
global.matchMedia = jest.fn().mockImplementation((query) => ({
  matches: false,
  media: query,
  onchange: null,
  addListener: jest.fn(),
  removeListener: jest.fn(),
  addEventListener: jest.fn(),
  removeEventListener: jest.fn(),
  dispatchEvent: jest.fn(),
}));
```

### Package.json Scripts

```json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "test:ci": "jest --ci"
  }
}
```

---

## Test Structure

### Basic Test Structure

```typescript
describe('MyComponent', () => {
  it('should render correctly', () => {
    // Test implementation
  });

  test('should handle user interaction', () => {
    // Test implementation
  });
});
```

### Nested Describe Blocks

```typescript
describe('UserService', () => {
  describe('getUser', () => {
    it('should return user when found', () => {
      // Test implementation
    });

    it('should throw error when not found', () => {
      // Test implementation
    });
  });

  describe('createUser', () => {
    it('should create user with valid data', () => {
      // Test implementation
    });
  });
});
```

### Test File Organization

```
src/
├── components/
│   ├── Button.tsx
│   └── Button.test.tsx
├── services/
│   ├── UserService.ts
│   └── UserService.test.ts
└── utils/
    ├── format.ts
    └── format.test.ts
```

---

## Assertions and Matchers

### Common Matchers

```typescript
// Equality
expect(value).toBe(expected);
expect(value).toEqual(expected);
expect(value).toStrictEqual(expected);

// Truthiness
expect(value).toBeTruthy();
expect(value).toBeFalsy();
expect(value).toBeNull();
expect(value).toBeUndefined();
expect(value).toBeDefined();

// Numbers
expect(value).toBeGreaterThan(10);
expect(value).toBeGreaterThanOrEqual(10);
expect(value).toBeLessThan(20);
expect(value).toBeLessThanOrEqual(20);
expect(value).toBeCloseTo(0.3, 2);

// Strings
expect(value).toMatch(/pattern/);
expect(value).toContain('substring');
expect(value).toHaveLength(10);

// Arrays
expect(array).toContain(item);
expect(array).toHaveLength(5);
expect(array).toEqual(expectedArray);
expect(array).toContainEqual(expectedItem);

// Objects
expect(object).toHaveProperty('key');
expect(object).toHaveProperty('key', value);
expect(object).toMatchObject(expected);

// Exceptions
expect(() => {
  throw new Error('message');
}).toThrow('message');
expect(() => {
  throw new Error('message');
}).toThrowError(Error);
```

### Custom Matchers

```typescript
// jest.setup.js
expect.extend({
  toBeWithinRange(received, floor, ceiling) {
    const pass = received >= floor && received <= ceiling;
    if (pass) {
      return {
        message: () =>
          `expected ${received} not to be within range ${floor} - ${ceiling}`,
        pass: true,
      };
    } else {
      return {
        message: () =>
          `expected ${received} to be within range ${floor} - ${ceiling}`,
        pass: false,
      };
    }
  },
});

// Usage
test('number is within range', () => {
  expect(5).toBeWithinRange(1, 10);
});
```

---

## Mocking

### Function Mocking

```typescript
// Mock a function
const mockFn = jest.fn();

// Mock implementation
mockFn.mockReturnValue(42);
mockFn.mockResolvedValue({ id: 1 });
mockFn.mockRejectedValue(new Error('Failed'));

// Mock implementation with function
mockFn.mockImplementation((a, b) => a + b);

// Mock implementation once
mockFn.mockImplementationOnce((a, b) => a + b);
mockFn.mockImplementationOnce((a, b) => a * b);

// Reset mock
mockFn.mockReset();
mockFn.mockClear();
mockFn.mockRestore();

// Get mock calls
expect(mockFn).toHaveBeenCalled();
expect(mockFn).toHaveBeenCalledTimes(2);
expect(mockFn).toHaveBeenCalledWith('arg1', 'arg2');
expect(mockFn).toHaveBeenLastCalledWith('arg1', 'arg2');

// Get mock return values
mockFn.mock.results;
mockFn.mock.calls;
```

### Module Mocking

```typescript
// Mock entire module
jest.mock('./myModule');

// Mock specific function
jest.mock('./myModule', () => ({
  myFunction: jest.fn().mockReturnValue(42),
}));

// Mock with partial implementation
jest.mock('./myModule', () => ({
  ...jest.requireActual('./myModule'),
  myFunction: jest.fn().mockReturnValue(42),
}));

// Mock in specific test
import { myFunction } from './myModule';

jest.mock('./myModule');

test('uses mocked function', () => {
  myFunction();
  expect(myFunction).toHaveBeenCalled();
});
```

### Async Function Mocking

```typescript
// Mock resolved promise
const mockFn = jest.fn().mockResolvedValue({ id: 1 });

// Mock rejected promise
const mockErrorFn = jest.fn().mockRejectedValue(new Error('Failed'));

// Mock async implementation
const mockAsyncFn = jest.fn().mockImplementation(async (id) => {
  return { id, name: 'User' };
});

// Usage
test('async function', async () => {
  const result = await mockAsyncFn(1);
  expect(result).toEqual({ id: 1, name: 'User' });
});
```

### Class Mocking

```typescript
// Mock class
jest.mock('./MyClass');

import { MyClass } from './MyClass';

test('mocks class', () => {
  const mockInstance = new MyClass();
  mockInstance.method.mockReturnValue(42);

  expect(mockInstance.method()).toBe(42);
});
```

---

## Async Testing

### Promise Testing

```typescript
test('async promise', async () => {
  const result = await asyncFunction();
  expect(result).toBe('value');
});

test('async promise with error', async () => {
  await expect(asyncFunction()).rejects.toThrow('Error message');
});
```

### Callback Testing

```typescript
test('async callback', (done) => {
  asyncCallback((error, result) => {
    expect(error).toBeNull();
    expect(result).toBe('value');
    done();
  });
});
```

### Async/Await Testing

```typescript
test('async/await', async () => {
  await expect(asyncFunction()).resolves.toBe('value');
  await expect(asyncFunction()).rejects.toThrow('Error');
});
```

### Timer Testing

```typescript
jest.useFakeTimers();

test('timer', () => {
  const callback = jest.fn();

  setTimeout(callback, 1000);

  jest.advanceTimersByTime(1000);

  expect(callback).toHaveBeenCalled();
});

afterEach(() => {
  jest.useRealTimers();
});
```

---

## Snapshot Testing

### Basic Snapshot

```typescript
test('snapshot', () => {
  const tree = renderer.create(<MyComponent />).toJSON();
  expect(tree).toMatchSnapshot();
});
```

### Inline Snapshot

```typescript
test('inline snapshot', () => {
  const tree = renderer.create(<MyComponent />).toJSON();
  expect(tree).toMatchInlineSnapshot(`
    <div>
      <span>Content</span>
    </div>
  `);
});
```

### Snapshot with Properties

```typescript
test('snapshot with props', () => {
  const tree = renderer.create(<MyComponent title="Hello" />).toJSON();
  expect(tree).toMatchSnapshot();
});
```

### Updating Snapshots

```bash
# Update all snapshots
npm test -- -u

# Update specific snapshot
npm test -- -t "MyComponent" -u
```

---

## Coverage

### Coverage Configuration

```javascript
// jest.config.js
module.exports = {
  collectCoverage: true,
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/*.stories.{js,jsx,ts,tsx}',
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
    './src/components/': {
      branches: 90,
      functions: 90,
      lines: 90,
      statements: 90,
    },
  },
  coverageReporters: ['text', 'lcov', 'html'],
};
```

### Running Coverage

```bash
# Generate coverage report
npm run test:coverage

# Generate coverage for specific files
npm test -- --coverage --collectCoverageFrom='src/utils/**/*.{ts,tsx}'
```

### Coverage Exclusions

```javascript
// jest.config.js
module.exports = {
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/*.stories.{js,jsx,ts,tsx}',
    '!src/index.ts',
    '!src/types/**',
  ],
};
```

---

## Setup and Teardown

### beforeEach/afterEach

```typescript
describe('MyComponent', () => {
  let component;

  beforeEach(() => {
    // Setup before each test
    component = render(<MyComponent />);
  });

  afterEach(() => {
    // Cleanup after each test
    component.unmount();
  });

  it('should render', () => {
    // Test implementation
  });
});
```

### beforeAll/afterAll

```typescript
describe('Database Tests', () => {
  let db;

  beforeAll(async () => {
    // Setup before all tests
    db = await connectDatabase();
  });

  afterAll(async () => {
    // Cleanup after all tests
    await db.disconnect();
  });

  it('should query database', async () => {
    // Test implementation
  });
});
```

---

## Testing React Components

### Basic Component Test

```typescript
import { render, screen } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  it('should render button text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('should call onClick handler', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);

    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

### Component with Props

```typescript
describe('Button', () => {
  it('should render with variant prop', () => {
    render(<Button variant="primary">Click me</Button>);
    expect(screen.getByRole('button')).toHaveClass('btn-primary');
  });

  it('should be disabled when disabled prop is true', () => {
    render(<Button disabled>Click me</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
```

### Component with State

```typescript
describe('Counter', () => {
  it('should increment count on button click', () => {
    render(<Counter />);
    const button = screen.getByRole('button', { name: 'Increment' });

    expect(screen.getByText('Count: 0')).toBeInTheDocument();

    fireEvent.click(button);

    expect(screen.getByText('Count: 1')).toBeInTheDocument();
  });
});
```

### Component with Async Data

```typescript
import { waitFor } from '@testing-library/react';

describe('UserProfile', () => {
  it('should display user data after loading', async () => {
    render(<UserProfile userId={1} />);

    expect(screen.getByText('Loading...')).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeInTheDocument();
    });
  });
});
```

### Component with Hooks

```typescript
import { renderHook, act } from '@testing-library/react';
import { useCounter } from './useCounter';

describe('useCounter', () => {
  it('should increment count', () => {
    const { result } = renderHook(() => useCounter());

    expect(result.current.count).toBe(0);

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(1);
  });
});
```

---

## Testing API Calls

### Mocking Fetch

```typescript
import { fetchUser } from './api';

global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () => Promise.resolve({ id: 1, name: 'John Doe' }),
  })
) as jest.Mock;

describe('fetchUser', () => {
  it('should fetch user data', async () => {
    const user = await fetchUser(1);
    expect(user).toEqual({ id: 1, name: 'John Doe' });
    expect(fetch).toHaveBeenCalledWith('/api/users/1');
  });
});
```

### Mocking Axios

```typescript
import axios from 'axios';
import { fetchUser } from './api';

jest.mock('axios');

describe('fetchUser', () => {
  it('should fetch user data', async () => {
    const mockData = { id: 1, name: 'John Doe' };
    (axios.get as jest.Mock).mockResolvedValue({ data: mockData });

    const user = await fetchUser(1);
    expect(user).toEqual(mockData);
    expect(axios.get).toHaveBeenCalledWith('/api/users/1');
  });
});
```

### Testing Error Handling

```typescript
describe('fetchUser', () => {
  it('should handle errors', async () => {
    (axios.get as jest.Mock).mockRejectedValue(new Error('Network error'));

    await expect(fetchUser(1)).rejects.toThrow('Network error');
  });
});
```

---

## Best Practices

### 1. Arrange, Act, Assert (AAA)

```typescript
test('user service', () => {
  // Arrange
  const userId = 1;
  const expectedUser = { id: 1, name: 'John Doe' };

  // Act
  const user = userService.getUser(userId);

  // Assert
  expect(user).toEqual(expectedUser);
});
```

### 2. Test One Thing

```typescript
// ❌ BAD: Testing multiple things
test('user service', () => {
  const user = userService.getUser(1);
  expect(user.id).toBe(1);
  expect(user.name).toBe('John Doe');
  expect(user.email).toBe('john@example.com');
});

// ✅ GOOD: Testing one thing
test('should return user with correct id', () => {
  const user = userService.getUser(1);
  expect(user.id).toBe(1);
});

test('should return user with correct name', () => {
  const user = userService.getUser(1);
  expect(user.name).toBe('John Doe');
});
```

### 3. Use Descriptive Test Names

```typescript
// ❌ BAD: Vague test name
test('user', () => {
  // ...
});

// ✅ GOOD: Descriptive test name
test('should return user when id exists', () => {
  // ...
});

test('should throw error when id does not exist', () => {
  // ...
});
```

### 4. Use Testing Library Queries

```typescript
// ❌ BAD: Implementation details
expect(container.querySelector('.btn-primary')).toBeInTheDocument();

// ✅ GOOD: User-centric queries
expect(screen.getByRole('button', { name: 'Submit' })).toBeInTheDocument();
```

### 5. Mock External Dependencies

```typescript
jest.mock('./api', () => ({
  fetchUser: jest.fn().mockResolvedValue({ id: 1, name: 'John Doe' }),
}));
```

### 6. Clean Up After Tests

```typescript
afterEach(() => {
  jest.clearAllMocks();
});
```

### 7. Test Edge Cases

```typescript
test('should handle empty input', () => {
  expect(() => validateUser({})).toThrow('Name is required');
});

test('should handle null input', () => {
  expect(() => validateUser(null)).toThrow('User is required');
});
```

### 8. Use Coverage Thresholds

```javascript
coverageThreshold: {
  global: {
    branches: 80,
    functions: 80,
    lines: 80,
    statements: 80,
  },
}
```

### 9. Run Tests in Watch Mode During Development

```bash
npm run test:watch
```

### 10. Keep Tests Independent

```typescript
// Each test should be able to run independently
test('test 1', () => {
  // Should not depend on test 2
});

test('test 2', () => {
  // Should not depend on test 1
});
```

---

## Resources

- [Jest Documentation](https://jestjs.io/docs/getting-started)
- [Testing Library](https://testing-library.com/docs/react-testing-library/intro)
- [Jest Matchers](https://jestjs.io/docs/expect)
- [Jest Mock Functions](https://jestjs.io/docs/mock-functions)
