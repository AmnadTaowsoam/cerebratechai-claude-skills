# E2E Testing with Playwright

## Overview

Playwright is a Node.js library to automate Chromium, Firefox, and WebKit with a single API. This skill covers Playwright setup, locators, actions, and best practices.

## Table of Contents

1. [Playwright Setup](#playwright-setup)
2. [Browser Context and Pages](#browser-context-and-pages)
3. [Locators](#locators)
4. [Actions](#actions)
5. [Assertions](#assertions)
6. [Page Object Model](#page-object-model)
7. [Fixtures](#fixtures)
8. [Parallel Execution](#parallel-execution)
9. [Visual Regression](#visual-regression)
10. [CI/CD Integration](#cicd-integration)
11. [Best Practices](#best-practices)
12. [Common Patterns](#common-patterns)

---

## Playwright Setup

### Installation

```bash
npm install -D @playwright/test
npx playwright install
```

### Basic Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  use: {
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: devices['Desktop Chrome'],
    },
    {
      name: 'firefox',
      use: devices['Desktop Firefox'],
    },
    {
      name: 'webkit',
      use: devices['Desktop Safari'],
    },
  ],
});
```

### Test File Structure

```
tests/
├── e2e/
│   ├── home-page.spec.ts
│   ├── login.spec.ts
│   └── checkout.spec.ts
├── fixtures/
│   ├── auth.fixture.ts
│   └── data.fixture.ts
└── pages/
    ├── BasePage.ts
    ├── HomePage.ts
    ├── LoginPage.ts
    └── CheckoutPage.ts
```

---

## Browser Context and Pages

### Basic Browser Context

```typescript
// e2e/home-page.spec.ts
import { test, expect } from '@playwright/test';

test('home page loads', async ({ page }) => {
  await page.goto('https://example.com');
  await expect(page).toHaveTitle(/Example Site/);
});
```

### Multiple Pages

```typescript
// e2e/multi-page.spec.ts
import { test, expect } from '@playwright/test';

test('navigate through pages', async ({ page }) => {
  await page.goto('https://example.com');
  await page.click('text=Products');
  await expect(page).toHaveURL(/products/);
  
  await page.click('text=Product 1');
  await expect(page).toHaveURL(/products/1/);
});
```

### Browser Context Options

```typescript
// e2e/browser-options.spec.ts
import { test, expect } from '@playwright/test';

test.use('viewport', async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 720 });
  await page.goto('https://example.com');
  
  const title = await page.title();
  expect(title).toBeTruthy();
});

test.use('locale', async ({ page }) => {
  await page.goto('https://example.com');
  await page.evaluate(() => {
    document.documentElement.lang = 'en';
  });
  
  const lang = await page.evaluate(() => document.documentElement.lang);
  expect(lang).toBe('en');
});
```

---

## Locators

### Text Locator

```typescript
// e2e/text-locator.spec.ts
import { test, expect } from '@playwright/test';

test('text locator', async ({ page }) => {
  await page.goto('https://example.com');
  
  const heading = page.getByText('Welcome to our site');
  await expect(heading).toBeVisible();
});
```

### CSS Selector Locator

```typescript
// e2e/css-locator.spec.ts
import { test, expect } from '@playwright/test';

test('CSS selector locator', async ({ page }) => {
  await page.goto('https://example.com');
  
  const button = page.locator('.submit-button');
  await expect(button).toBeVisible();
});
```

### Role Locator

```typescript
// e2e/role-locator.spec.ts
import { test, expect } from '@playwright/test';

test('role locator', async ({ page }) => {
  await page.goto('https://example.com');
  
  const heading = page.getByRole('heading', { level: 1 });
  await expect(heading).toBeVisible();
});
```

### Test ID Locator

```typescript
// e2e/testid-locator.spec.ts
import { test, expect } from '@playwright/test';

test('test ID locator', async ({ page }) => {
  await page.goto('https://example.com');
  
  const element = page.getByTestId('submit-button');
  await expect(element).toBeVisible();
});
```

### XPath Locator

```typescript
// e2e/xpath-locator.spec.ts
import { test, expect } from '@playwright/test';

test('XPath locator', async ({ page }) => {
  await page.goto('https://example.com');
  
  const element = page.locator('//button[@type="submit"]');
  await expect(element).toBeVisible();
});
```

### Combined Locators

```typescript
// e2e/combined-locator.spec.ts
import { test, expect } from '@playwright/test';

test('combined locators', async ({ page }) => {
  await page.goto('https://example.com');
  
  const button = page.locator('button').filter({ hasText: 'Submit' });
  await expect(button).toBeVisible();
});
```

---

## Actions

### Click

```typescript
// e2e/click.spec.ts
import { test, expect } from '@playwright/test';

test('click button', async ({ page }) => {
  await page.goto('https://example.com');
  
  await page.click('text=Submit');
  await expect(page).toHaveURL(/success/);
});
```

### Type

```typescript
// e2e/type.spec.ts
import { test, expect } from '@playwright/test';

test('type in input', async ({ page }) => {
  await page.goto('https://example.com/contact');
  
  await page.fill('input[name="name"]', 'John');
  await page.fill('input[name="email"]', 'john@example.com');
  await page.fill('textarea[name="message"]', 'Hello World');
});
```

### Select Option

```typescript
// e2e/select.spec.ts
import { test, expect } from '@playwright/test';

test('select option', async ({ page }) => {
  await page.goto('https://example.com');
  
  await page.selectOption('select[name="country"]', 'United States');
  await expect(page.locator('select[name="country"]')).toHaveValue('US');
});
```

### Check Checkbox

```typescript
// e2e/checkbox.spec.ts
import { test, expect } from '@playwright/test';

test('check checkbox', async ({ page }) => {
  await page.goto('https://example.com');
  
  await page.check('input[type="checkbox"]');
  await expect(page.locator('input[type="checkbox"]')).toBeChecked();
});
```

### Upload File

```typescript
// e2e/upload.spec.ts
import { test, expect } from '@playwright/test';

test('upload file', async ({ page }) => {
  await page.goto('https://example.com/upload');
  
  const fileInput = page.locator('input[type="file"]');
  await fileInput.setInputFiles('./test-file.txt');
  
  await expect(fileInput).toHaveJSProperty('files.0.name', 'test-file.txt');
});
```

### Hover

```typescript
// e2e/hover.spec.ts
import { test, expect } from '@playwright/test';

test('hover element', async ({ page }) => {
  await page.goto('https://example.com');
  
  const button = page.getByText('Hover me');
  await button.hover();
  
  await expect(page.locator('.tooltip')).toBeVisible();
});
```

---

## Assertions

### Visibility Assertions

```typescript
// e2e/visibility.spec.ts
import { test, expect } from '@playwright/test';

test('element visibility', async ({ page }) => {
  await page.goto('https://example.com');
  
  const element = page.getByText('Submit');
  
  await expect(element).toBeVisible();
  await expect(element).toBeEnabled();
  await expect(element).toHaveAttribute('type', 'submit');
});
```

### Text Content Assertions

```typescript
// e2e/text-content.spec.ts
import { test, expect } from '@playwright/test';

test('text content', async ({ page }) => {
  await page.goto('https://example.com');
  
  const heading = page.getByRole('heading');
  
  await expect(heading).toContainText('Welcome');
  await expect(heading).toHaveText('Welcome to our site');
});
```

### URL Assertions

```typescript
// e2e/url.spec.ts
import { test, expect } from '@playwright/test';

test('URL assertion', async ({ page }) => {
  await page.goto('https://example.com');
  
  await expect(page).toHaveURL('https://example.com/');
  await expect(page).toHaveTitle(/Example Site/);
});
```

### Attribute Assertions

```typescript
// e2e/attribute.spec.ts
import { test, expect } from '@playwright/test';

test('attribute assertion', async ({ page }) => {
  await page.goto('https://example.com');
  
  const button = page.getByRole('button');
  
  await expect(button).toHaveAttribute('type', 'submit');
  await expect(button).toHaveAttribute('disabled', 'false');
});
```

### Count Assertions

```typescript
// e2e/count.spec.ts
import { test, expect } from '@playwright/test';

test('count assertions', async ({ page }) => {
  await page.goto('https://example.com');
  
  const items = page.locator('.list-item');
  
  await expect(items).toHaveCount(3);
  await expect(items).toHaveCount(3); // Count of elements
});
```

---

## Page Object Model

### Base Page

```typescript
// pages/BasePage.ts
import { Page, Locator } from '@playwright/test';

export class BasePage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  async goto(url: string): Promise<void> {
    await this.page.goto(url);
  }

  async waitForLoad(): Promise<void> {
    await this.page.waitForLoadState('networkidle');
  }

  async screenshot(path: string): Promise<void> {
    await this.page.screenshot({ path });
  }
}
```

### Home Page

```typescript
// pages/HomePage.ts
import { Page, Locator } from '@playwright/test';
import { BasePage } from './BasePage';

export class HomePage extends BasePage {
  readonly heading: Locator;
  readonly productsLink: Locator;
  readonly contactLink: Locator;

  constructor(page: Page) {
    super(page);
    this.heading = page.getByRole('heading');
    this.productsLink = page.getByText('Products');
    this.contactLink = page.getByText('Contact');
  }

  async navigate(): Promise<void> {
    await this.goto('https://example.com');
    await this.waitForLoad();
  }

  async clickProductsLink(): Promise<void> {
    await this.productsLink.click();
  }

  async clickContactLink(): Promise<void> {
    await this.contactLink.click();
  }
}
```

### Login Page

```typescript
// pages/LoginPage.ts
import { Page, Locator } from '@playwright/test';
import { BasePage } from './BasePage';

export class LoginPage extends BasePage {
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    super(page);
    this.emailInput = page.locator('input[name="email"]');
    this.passwordInput = page.locator('input[type="password"]');
    this.submitButton = page.locator('button[type="submit"]');
    this.errorMessage = page.locator('.error-message');
  }

  async login(email: string, password: string): Promise<void> {
    await this.goto('https://example.com/login');
    await this.waitForLoad();

    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }

  async getErrorMessage(): Promise<string | null> {
    const visible = await this.errorMessage.isVisible().catch(() => false);
    if (!visible) return null;
    
    return await this.errorMessage.textContent();
  }
}
```

### Checkout Page

```typescript
// pages/CheckoutPage.ts
import { Page, Locator } from '@playwright/test';
import { BasePage } from './BasePage';

export class CheckoutPage extends BasePage {
  readonly cartItems: Locator;
  readonly checkoutButton: Locator;
  readonly totalAmount: Locator;

  constructor(page: Page) {
    super(page);
    this.cartItems = page.locator('.cart-item');
    this.checkoutButton = page.getByRole('button', { name: 'checkout' });
    this.totalAmount = page.locator('.total-amount');
  }

  async navigate(): Promise<void> {
    await this.goto('https://example.com/checkout');
    await this.waitForLoad();
  }

  async getCartItemCount(): Promise<number> {
    return await this.cartItems.count();
  }

  async getTotalAmount(): Promise<string> {
    return await this.totalAmount.textContent();
  }

  async clickCheckout(): Promise<void> {
    await this.checkoutButton.click();
  }
}
```

---

## Fixtures

### Auth Fixture

```typescript
// fixtures/auth.fixture.ts
import { test as base } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';

base.extend<{ loginPage: LoginPage }>({
  loginPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await use(loginPage, async () => {
      await loginPage.navigate();
      await loginPage.login('test@example.com', 'password123');
    });
    return loginPage;
  },
});
```

### Data Fixture

```typescript
// fixtures/data.fixture.ts
import { test as base } from '@playwright/test';

export const testUser = {
  name: 'Test User',
  email: 'test@example.com',
  password: 'password123',
};

export const testProduct = {
  name: 'Test Product',
  price: 99.99,
  description: 'Test product description',
};

base.extend<{ testUser: typeof testUser; testProduct: typeof testProduct }>({
  testUser: async ({}, use) => {
    await use(async () => {
      // Setup test user in database
    });
    return testUser;
  },
});

base.extend<{ testProduct: typeof testProduct }>({
  testProduct: async ({}, use) => {
    await use(async () => {
      // Setup test product in database
    });
    return testProduct;
  },
});
```

---

## Parallel Execution

### Parallel Tests

```typescript
// e2e/parallel.spec.ts
import { test } from '@playwright/test';

test.describe('parallel tests', () => {
  test('test 1', async ({ page }) => {
    await page.goto('https://example.com');
    await expect(page).toHaveTitle(/Example Site/);
  });

  test('test 2', async ({ page }) => {
    await page.goto('https://example.com');
    await expect(page).toHaveTitle(/Example Site/);
  });

  test('test 3', async ({ page }) => {
    await page.goto('https://example.com');
    await expect(page).toHaveTitle(/Example Site/);
  });
});
```

### Worker Index

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  workers: 4, // Number of parallel workers
});
```

---

## Visual Regression

### Screenshot Comparison

```typescript
// e2e/visual.spec.ts
import { test, expect } from '@playwright/test';

test('visual regression', async ({ page }) => {
  await page.goto('https://example.com');
  await page.waitForLoadState('networkidle');
  
  await page.screenshot({ path: 'screenshots/home.png' });
  
  // Compare with baseline screenshot
  // Use a tool like Playwright's visual regression feature
  // or a third-party tool like Percy, Applitools
});
```

### Visual Regression with Playwright

```typescript
// e2e/visual-regression.spec.ts
import { test, expect } from '@playwright/test';

test('visual regression with Playwright', async ({ page }) => {
  await page.goto('https://example.com');
  await page.waitForLoadState('networkidle');
  
  const screenshot = await page.screenshot();
  
  expect(screenshot).toMatchSnapshot('home-page.png');
});
```

---

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/e2e.yml
name: E2E Tests

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright browsers
        run: npx playwright install --with-deps

      - name: Run E2E tests
        run: npx playwright test

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-results
          path: playwright-report/
```

### GitLab CI

```yaml
# .gitlab-ci.yml
image: node:18

stages:
  test:
    stage: test
    script:
      - npm ci
      - npx playwright install --with-deps
      - npx playwright test
    artifacts:
      when: always
      paths:
        - playwright-report/
        - test-results/
      expire_in: 1 week
```

### CircleCI

```yaml
# .circleci/config.yml
version: 2.1

jobs:
  test:
  docker:
    - image: mcr.microsoft.com/playwright:latest
      steps:
        - checkout
        - run: npm ci
        - run: npx playwright install --with-deps
        - run: npx playwright test
```

---

## Best Practices

### 1. Use Page Object Model

```typescript
// Good: Page Object Model
class LoginPage extends BasePage {
  async login(email: string, password: string): Promise<void> {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }
}

// Bad: Inline locators
test('login', async ({ page }) => {
  await page.goto('https://test.com/login');
  await page.fill('input[name="email"]', 'test@example.com');
  await page.fill('input[type="password"]', 'password123');
  await page.click('button[type="submit"]');
});
```

### 2. Use Explicit Waits

```typescript
// Good: Explicit waits
test('navigation', async ({ page }) => {
  await page.goto('https://example.com/products');
  await page.waitForLoadState('networkidle');
  
  const product = page.getByText('Product 1');
  await expect(product).toBeVisible();
});

// Bad: No explicit wait
test('navigation', async ({ page }) => {
  await page.goto('https://example.com/products');
  const product = page.getByText('Product 1');
  await expect(product).toBeVisible();
});
```

### 3. Use Descriptive Test Names

```typescript
// Good: Descriptive test names
test('should display error message when login fails', async ({ page }) => {
  await page.goto('https://example.com/login');
  await page.fill('input[name="email"]', 'invalid-email');
  await page.click('button[type="submit"]');
  await expect(page.locator('.error-message')).toBeVisible();
});

// Bad: Non-descriptive test names
test('login error', async ({ page }) => {
  await page.goto('https://example.com/login');
  await page.fill('input[name="email"]', 'invalid-email');
  await page.click('button[type="submit"]');
  await expect(page.locator('.error-message')).toBeVisible();
});
```

### 4. Use Fixtures Effectively

```typescript
// Good: Reusable fixtures
test('login with valid credentials', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.navigate();
  await loginPage.login('test@example.com', 'password123');
  
  await expect(page).toHaveURL(/dashboard/);
});

// Bad: Duplicated code
test('login 1', async ({ page }) => {
  await page.goto('https://test.com/login');
  await page.fill('input[name="email"]', 'test@example.com');
  await page.fill('input[type="password"]', 'password123');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL(/dashboard/);
});

test('login 2', async ({ page }) => {
  await page.goto('https://test.com/login');
  await page.fill('input[name="email"]', 'test@example.com');
  await page.fill('input[type="password"]', 'password123');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL(/dashboard/);
});
```

### 5. Use Soft Assertions

```typescript
// Good: Soft assertions for debugging
test('debugging', async ({ page }) => {
  await page.goto('https://example.com');
  
  await page.screenshot({ path: 'debug.png' });
  
  const element = page.getByText('Submit');
  await expect(element).toBeVisible();
});

// Bad: No debugging
test('submit button', async ({ page }) => {
  await page.goto('https://test.com');
  const element = page.getByText('Submit');
  await expect(element).toBeVisible();
});
```

---

## Common Patterns

### Login Flow

```typescript
// e2e/login-flow.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';
import { DashboardPage } from '../pages/DashboardPage';

test('successful login flow', async ({ page }) => {
  const loginPage = new LoginPage(page);
  const dashboardPage = new DashboardPage(page);
  
  await loginPage.navigate();
  await loginPage.login('test@example.com', 'password123');
  
  await expect(dashboardPage.heading).toBeVisible();
});
```

### Checkout Flow

```typescript
// e2e/checkout-flow.spec.ts
import { test, expect } from '@playwright/test';
import { HomePage } from '../pages/HomePage';
import { CheckoutPage } from '../pages/CheckoutPage';

test('complete checkout flow', async ({ page }) => {
  const homePage = new HomePage(page);
  const checkoutPage = new CheckoutPage(page);
  
  await homePage.navigate();
  await homePage.clickProductsLink();
  
  await page.getByText('Add to cart').click();
  
  await homePage.clickCheckoutLink();
  
  await checkoutPage.clickCheckout();
  
  await expect(page.locator('.success-message')).toBeVisible();
});
```

### Form Validation

```typescript
// e2e/form-validation.spec.ts
import { test, expect } from '@playwright/test';

test('form validation', async ({ page }) => {
  await page.goto('https://example.com/contact');
  
  await page.fill('input[name="email"]', 'invalid-email');
  await page.click('button[type="submit"]');
  
  await expect(page.locator('.error-message')).toHaveText('Please enter a valid email');
});
```

---

## Summary

This skill covers comprehensive E2E testing with Playwright including:

- **Playwright Setup**: Installation, configuration, test structure
- **Browser Context and Pages**: Basic context, multiple pages, browser options
- **Locators**: Text, CSS selector, role, test ID, XPath, combined locators
- **Actions**: Click, type, select option, check checkbox, upload file, hover
- **Assertions**: Visibility, text content, URL, attribute, count assertions
- **Page Object Model**: Base page, home page, login page, checkout page
- **Fixtures**: Auth fixture, data fixture
- **Parallel Execution**: Parallel tests, worker index
- **Visual Regression**: Screenshot comparison, Playwright visual regression
- **CI/CD Integration**: GitHub Actions, GitLab CI, CircleCI
- **Best Practices**: Page Object Model, explicit waits, descriptive names, fixtures, soft assertions
- **Common Patterns**: Login flow, checkout flow, form validation
