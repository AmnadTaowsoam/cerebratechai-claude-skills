# E2E Testing with Playwright

A comprehensive guide to end-to-end testing with Playwright.

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
# Install Playwright
npm init -y
npm install -D @playwright/test

# Install browsers
npx playwright install

# Install with TypeScript
npm install -D @playwright/test typescript

# Install additional dependencies
npm install -D @playwright/test
```

### Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html'],
    ['junit', { outputFile: 'test-results/junit.xml' }],
  ],
  use: {
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
  ],
  webServer: {
    command: 'npm run start',
    port: 3000,
    reuseExistingServer: !process.env.CI,
  },
});
```

### Basic Test

```typescript
import { test, expect } from '@playwright/test';

test('basic test', async ({ page }) => {
  await page.goto('https://example.com');
  await expect(page).toHaveTitle(/Example/);
});
```

---

## Browser Context and Pages

### Creating Context

```typescript
test('browser context', async ({ browser }) => {
  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 },
    locale: 'en-US',
    timezoneId: 'America/New_York',
    permissions: ['geolocation'],
    geolocation: { latitude: 52.52, longitude: 13.39 },
    colorScheme: 'dark',
    userAgent: 'Custom User Agent',
  });

  const page = await context.newPage();
  await page.goto('https://example.com');
});
```

### Multiple Pages

```typescript
test('multiple pages', async ({ context }) => {
  const page1 = await context.newPage();
  await page1.goto('https://example.com');

  const page2 = await context.newPage();
  await page2.goto('https://example.com/about');

  await expect(page1).toHaveTitle(/Example/);
  await expect(page2).toHaveTitle(/About/);
});
```

### Storage State

```typescript
test('login and save state', async ({ page, context }) => {
  await page.goto('https://example.com/login');
  await page.fill('input[name="email"]', 'user@example.com');
  await page.fill('input[name="password"]', 'password');
  await page.click('button[type="submit"]');

  // Save storage state
  await context.storageState({ path: 'auth.json' });
});

test('use saved state', async ({ browser }) => {
  const context = await browser.newContext({
    storageState: 'auth.json',
  });
  const page = await context.newPage();
  await page.goto('https://example.com/dashboard');
  // User is already logged in
});
```

---

## Locators

### Text Locators

```typescript
test('text locators', async ({ page }) => {
  await page.goto('https://example.com');

  // By exact text
  await page.getByText('Submit').click();

  // By text content (substring)
  await page.getByText('Subm').click();

  // By exact text
  await page.getByText('Submit', { exact: true }).click();
});
```

### Role Locators

```typescript
test('role locators', async ({ page }) => {
  await page.goto('https://example.com');

  // By role
  await page.getByRole('button', { name: 'Submit' }).click();
  await page.getByRole('link', { name: 'Learn more' }).click();
  await page.getByRole('textbox', { name: 'Email' }).fill('user@example.com');
});
```

### Label Locators

```typescript
test('label locators', async ({ page }) => {
  await page.goto('https://example.com');

  // By label
  await page.getByLabel('Email').fill('user@example.com');
  await page.getByLabel('Password', { exact: true }).fill('password');
});
```

### Placeholder Locators

```typescript
test('placeholder locators', async ({ page }) => {
  await page.goto('https://example.com');

  // By placeholder
  await page.getByPlaceholder('Enter your email').fill('user@example.com');
});
```

### Alt Text Locators

```typescript
test('alt text locators', async ({ page }) => {
  await page.goto('https://example.com');

  // By alt text
  await page.getByAltText('Logo').click();
});
```

### Test ID Locators

```typescript
test('test id locators', async ({ page }) => {
  await page.goto('https://example.com');

  // By test id
  await page.getByTestId('submit-button').click();
});
```

### CSS/XPath Locators

```typescript
test('css xpath locators', async ({ page }) => {
  await page.goto('https://example.com');

  // By CSS selector
  await page.locator('.submit-button').click();

  // By XPath
  await page.locator('//button[@type="submit"]').click();
});
```

### Chaining Locators

```typescript
test('chaining locators', async ({ page }) => {
  await page.goto('https://example.com');

  // Chain locators
  await page.getByRole('listitem')
    .filter({ hasText: 'Product A' })
    .getByRole('button', { name: 'Add to cart' })
    .click();
});
```

---

## Actions

### Click Actions

```typescript
test('click actions', async ({ page }) => {
  await page.goto('https://example.com');

  // Simple click
  await page.getByRole('button', { name: 'Submit' }).click();

  // Double click
  await page.getByText('Click me').dblclick();

  // Right click
  await page.getByText('Right click me').click({ button: 'right' });

  // Click with modifiers
  await page.getByText('Select me').click({ modifiers: ['Shift'] });
});
```

### Type Actions

```typescript
test('type actions', async ({ page }) => {
  await page.goto('https://example.com');

  // Fill input
  await page.getByLabel('Email').fill('user@example.com');

  // Type character by character
  await page.getByLabel('Email').type('user@example.com', { delay: 100 });

  // Clear and fill
  await page.getByLabel('Email').clear();
  await page.getByLabel('Email').fill('new@example.com');

  // Press keys
  await page.getByLabel('Search').fill('query');
  await page.getByLabel('Search').press('Enter');
});
```

### Select Options

```typescript
test('select options', async ({ page }) => {
  await page.goto('https://example.com');

  // Select option
  await page.getByLabel('Country').selectOption('United States');

  // Select multiple options
  await page.getByLabel('Interests').selectOption(['Sports', 'Music']);
});
```

### Checkbox and Radio

```typescript
test('checkbox radio', async ({ page }) => {
  await page.goto('https://example.com');

  // Check checkbox
  await page.getByLabel('Accept terms').check();

  // Uncheck checkbox
  await page.getByLabel('Accept terms').uncheck();

  // Check if checked
  const isChecked = await page.getByLabel('Accept terms').isChecked();
  expect(isChecked).toBe(true);

  // Select radio
  await page.getByLabel('Male').check();
});
```

### File Upload

```typescript
test('file upload', async ({ page }) => {
  await page.goto('https://example.com');

  // Upload file
  await page.getByLabel('Upload').setInputFiles('path/to/file.pdf');
});
```

### Hover Actions

```typescript
test('hover actions', async ({ page }) => {
  await page.goto('https://example.com');

  // Hover over element
  await page.getByText('Menu').hover();
});
```

### Drag and Drop

```typescript
test('drag and drop', async ({ page }) => {
  await page.goto('https://example.com');

  // Drag and drop
  await page.getByTestId('draggable').dragTo(page.getByTestId('droppable'));
});
```

---

## Assertions

### Basic Assertions

```typescript
test('basic assertions', async ({ page }) => {
  await page.goto('https://example.com');

  // Element is visible
  await expect(page.getByText('Welcome')).toBeVisible();

  // Element is hidden
  await expect(page.getByText('Hidden')).toBeHidden();

  // Element is attached
  await expect(page.getByText('Attached')).toBeAttached();

  // Element is detached
  await expect(page.getByText('Detached')).toBeDetached();
});
```

### Text Assertions

```typescript
test('text assertions', async ({ page }) => {
  await page.goto('https://example.com');

  // Text content
  await expect(page.getByTestId('title')).toHaveText('Welcome');

  // Text contains
  await expect(page.getByTestId('description')).toContainText('Lorem ipsum');

  // Text matches regex
  await expect(page.getByTestId('email')).toHaveText(/@example\.com$/);
});
```

### Attribute Assertions

```typescript
test('attribute assertions', async ({ page }) => {
  await page.goto('https://example.com');

  // Has attribute
  await expect(page.getByRole('button')).toHaveAttribute('type', 'submit');

  // Has class
  await expect(page.getByTestId('button')).toHaveClass('btn-primary');

  // Has id
  await expect(page.getByTestId('button')).toHaveId('submit-button');
});
```

### Value Assertions

```typescript
test('value assertions', async ({ page }) => {
  await page.goto('https://example.com');

  // Input value
  await expect(page.getByLabel('Email')).toHaveValue('user@example.com');

  // Input values
  await expect(page.getByLabel('Tags')).toHaveValues(['tag1', 'tag2']);
});
```

### URL Assertions

```typescript
test('url assertions', async ({ page }) => {
  await page.goto('https://example.com');

  // URL matches
  await expect(page).toHaveURL('https://example.com');

  // URL contains
  await expect(page).toHaveURL(/example\.com/);

  // URL path
  await expect(page).toHaveURL('/dashboard');
});
```

### Title Assertions

```typescript
test('title assertions', async ({ page }) => {
  await page.goto('https://example.com');

  // Page title
  await expect(page).toHaveTitle('Example Domain');
  await expect(page).toHaveTitle(/Example/);
});
```

### Screenshot Assertions

```typescript
test('screenshot assertions', async ({ page }) => {
  await page.goto('https://example.com');

  // Screenshot matches
  await expect(page).toHaveScreenshot('homepage.png');
});
```

### Custom Assertions

```typescript
test('custom assertions', async ({ page }) => {
  await page.goto('https://example.com');

  // Custom assertion
  await expect(async () => {
    const element = page.getByTestId('dynamic-content');
    await element.waitFor();
    const text = await element.textContent();
    return text !== '';
  }).resolves.toBe(true);
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

  async goto(url: string) {
    await this.page.goto(url);
  }

  async click(locator: Locator) {
    await locator.click();
  }

  async fill(locator: Locator, value: string) {
    await locator.fill(value);
  }

  async waitFor(locator: Locator) {
    await locator.waitFor();
  }
}
```

### Login Page

```typescript
// pages/LoginPage.ts
import { Page } from '@playwright/test';
import { BasePage } from './BasePage';

export class LoginPage extends BasePage {
  readonly emailInput = this.page.getByLabel('Email');
  readonly passwordInput = this.page.getByLabel('Password');
  readonly submitButton = this.page.getByRole('button', { name: 'Login' });

  constructor(page: Page) {
    super(page);
  }

  async login(email: string, password: string) {
    await this.fill(this.emailInput, email);
    await this.fill(this.passwordInput, password);
    await this.click(this.submitButton);
  }
}
```

### Dashboard Page

```typescript
// pages/DashboardPage.ts
import { Page } from '@playwright/test';
import { BasePage } from './BasePage';

export class DashboardPage extends BasePage {
  readonly welcomeMessage = this.page.getByText('Welcome');
  readonly logoutButton = this.page.getByRole('button', { name: 'Logout' });

  constructor(page: Page) {
    super(page);
  }

  async logout() {
    await this.click(this.logoutButton);
  }
}
```

### Using Page Objects

```typescript
// e2e/login.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';
import { DashboardPage } from '../pages/DashboardPage';

test('login flow', async ({ page }) => {
  const loginPage = new LoginPage(page);
  const dashboardPage = new DashboardPage(page);

  await loginPage.goto('https://example.com/login');
  await loginPage.login('user@example.com', 'password');

  await expect(dashboardPage.welcomeMessage).toBeVisible();
  await dashboardPage.logout();
});
```

---

## Fixtures

### Basic Fixture

```typescript
// e2e/fixtures.ts
import { test as base } from '@playwright/test';

type MyFixtures = {
  authenticatedPage: Page;
};

const test = base.extend<MyFixtures>({
  authenticatedPage: async ({ page }, use) => {
    // Setup
    await page.goto('https://example.com/login');
    await page.fill('input[name="email"]', 'user@example.com');
    await page.fill('input[name="password"]', 'password');
    await page.click('button[type="submit"]');

    // Use fixture
    await use(page);

    // Teardown
    await page.goto('https://example.com/logout');
  },
});

export { test };
```

### Using Custom Fixtures

```typescript
// e2e/dashboard.spec.ts
import { test, expect } from '../fixtures';

test('dashboard test', async ({ authenticatedPage }) => {
  await authenticatedPage.goto('https://example.com/dashboard');
  await expect(authenticatedPage.getByText('Dashboard')).toBeVisible();
});
```

### Database Fixture

```typescript
// e2e/fixtures.ts
import { test as base } from '@playwright/test';
import { Database } from '../utils/database';

type MyFixtures = {
  db: Database;
};

const test = base.extend<MyFixtures>({
  db: async ({}, use) => {
    const db = new Database();
    await db.connect();
    await db.seed();

    await use(db);

    await db.cleanup();
    await db.disconnect();
  },
});

export { test };
```

---

## Parallel Execution

### Parallel Tests

```typescript
// playwright.config.ts
export default defineConfig({
  fullyParallel: true,
  workers: 4, // Number of parallel workers
});
```

### Parallel Projects

```typescript
// playwright.config.ts
export default defineConfig({
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],
});
```

### Sharding

```bash
# Run tests in shards
npx playwright test --shard=1/4
npx playwright test --shard=2/4
npx playwright test --shard=3/4
npx playwright test --shard=4/4
```

---

## Visual Regression

### Basic Screenshot

```typescript
test('visual regression', async ({ page }) => {
  await page.goto('https://example.com');

  // Take screenshot
  await page.screenshot({ path: 'screenshots/homepage.png' });
});
```

### Screenshot Comparison

```typescript
test('visual comparison', async ({ page }) => {
  await page.goto('https://example.com');

  // Compare with baseline
  await expect(page).toHaveScreenshot('homepage.png');
});
```

### Full Page Screenshot

```typescript
test('full page screenshot', async ({ page }) => {
  await page.goto('https://example.com');

  // Full page screenshot
  await page.screenshot({
    path: 'screenshots/fullpage.png',
    fullPage: true,
  });
});
```

### Element Screenshot

```typescript
test('element screenshot', async ({ page }) => {
  await page.goto('https://example.com');

  // Element screenshot
  await page.getByTestId('header').screenshot({
    path: 'screenshots/header.png',
  });
});
```

---

## CI/CD Integration

### GitHub Actions

```yaml
name: E2E Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    timeout-minutes: 60
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 18

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright Browsers
        run: npx playwright install --with-deps

      - name: Run E2E tests
        run: npx playwright test

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30

      - name: Upload screenshots
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-screenshots
          path: test-results/
          retention-days: 30
```

### Docker

```dockerfile
FROM mcr.microsoft.com/playwright:v1.40.0-jammy

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

RUN npx playwright install --with-deps

CMD ["npx", "playwright", "test"]
```

---

## Best Practices

### 1. Use Locators Over Selectors

```typescript
// ❌ BAD: Using CSS selectors
await page.click('.submit-button');

// ✅ GOOD: Using locators
await page.getByRole('button', { name: 'Submit' }).click();
```

### 2. Use Page Object Model

```typescript
// Encapsulate page interactions in page objects
const loginPage = new LoginPage(page);
await loginPage.login('user@example.com', 'password');
```

### 3. Use Wait for Actions

```typescript
// Wait for element to be ready
await page.getByRole('button', { name: 'Submit' }).waitFor();
await page.getByRole('button', { name: 'Submit' }).click();
```

### 4. Use Data-Driven Tests

```typescript
const testData = [
  { email: 'user1@example.com', password: 'pass1' },
  { email: 'user2@example.com', password: 'pass2' },
];

testData.forEach(({ email, password }) => {
  test(`login with ${email}`, async ({ page }) => {
    await page.goto('https://example.com/login');
    await page.fill('input[name="email"]', email);
    await page.fill('input[name="password"]', password);
    await page.click('button[type="submit"]');
  });
});
```

### 5. Use Fixtures for Setup

```typescript
// Use fixtures for common setup
test('authenticated test', async ({ authenticatedPage }) => {
  await authenticatedPage.goto('https://example.com/dashboard');
});
```

### 6. Use Assertions

```typescript
// Use Playwright assertions
await expect(page.getByText('Welcome')).toBeVisible();
```

### 7. Use Trace on Failure

```typescript
// playwright.config.ts
export default defineConfig({
  use: {
    trace: 'on-first-retry',
  },
});
```

### 8. Use Screenshots on Failure

```typescript
// playwright.config.ts
export default defineConfig({
  use: {
    screenshot: 'only-on-failure',
  },
});
```

### 9. Use Parallel Execution

```typescript
// playwright.config.ts
export default defineConfig({
  fullyParallel: true,
  workers: 4,
});
```

### 10. Keep Tests Independent

```typescript
// Each test should be able to run independently
test('test 1', async ({ page }) => {
  // ...
});

test('test 2', async ({ page }) => {
  // ...
});
```

---

## Common Patterns

### Login Flow

```typescript
test('login flow', async ({ page }) => {
  await page.goto('https://example.com/login');
  await page.fill('input[name="email"]', 'user@example.com');
  await page.fill('input[name="password"]', 'password');
  await page.click('button[type="submit"]');

  await expect(page).toHaveURL('https://example.com/dashboard');
});
```

### Form Submission

```typescript
test('form submission', async ({ page }) => {
  await page.goto('https://example.com/contact');

  await page.fill('input[name="name"]', 'John Doe');
  await page.fill('input[name="email"]', 'john@example.com');
  await page.fill('textarea[name="message"]', 'Hello World');
  await page.click('button[type="submit"]');

  await expect(page.getByText('Thank you')).toBeVisible();
});
```

### Navigation

```typescript
test('navigation', async ({ page }) => {
  await page.goto('https://example.com');

  await page.getByRole('link', { name: 'About' }).click();
  await expect(page).toHaveURL(/about/);

  await page.goBack();
  await expect(page).toHaveURL('https://example.com');

  await page.goForward();
  await expect(page).toHaveURL(/about/);
});
```

### File Download

```typescript
test('file download', async ({ page }) => {
  const downloadPromise = page.waitForEvent('download');
  await page.getByRole('button', { name: 'Download' }).click();
  const download = await downloadPromise;

  await download.saveAs('./downloads/file.pdf');
});
```

### File Upload

```typescript
test('file upload', async ({ page }) => {
  await page.goto('https://example.com/upload');

  await page.getByLabel('File').setInputFiles('path/to/file.pdf');
  await page.getByRole('button', { name: 'Upload' }).click();

  await expect(page.getByText('Upload successful')).toBeVisible();
});
```

---

## Resources

- [Playwright Documentation](https://playwright.dev/)
- [Playwright Test](https://playwright.dev/docs/intro)
- [Best Practices](https://playwright.dev/docs/best-practices)
- [API Reference](https://playwright.dev/docs/api/class-playwright)
