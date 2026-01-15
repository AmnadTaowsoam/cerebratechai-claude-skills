---
name: Hot Reload and Fast Feedback Loops
description: Implementing fast feedback loops with hot reload, live reload, and rapid iteration to maximize developer productivity.
---

# Hot Reload and Fast Feedback Loops

## Overview

Hot Reload and Fast Feedback Loops enable developers to see changes instantly without restarting the application, dramatically improving productivity and iteration speed.

**Core Principle**: "The faster you see results, the faster you learn. Optimize for instant feedback."

---

## 1. Types of Reload

```markdown
## Reload Comparison

### Hot Module Replacement (HMR)
- **Speed**: Instant (< 100ms)
- **State**: Preserved
- **Use**: Frontend development
- **Example**: React Fast Refresh

### Live Reload
- **Speed**: Fast (1-3s)
- **State**: Lost (full page reload)
- **Use**: Static sites, simple apps
- **Example**: BrowserSync

### Server Restart
- **Speed**: Slow (5-10s)
- **State**: Lost
- **Use**: Backend development
- **Example**: Nodemon

### No Reload
- **Speed**: Very slow (manual restart)
- **State**: Lost
- **Use**: Production
- **Example**: Traditional deployment
```

---

## 2. Frontend Hot Reload

### Vite (Recommended)
```javascript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    open: true,
    hmr: {
      overlay: true,  // Show errors as overlay
    },
  },
  build: {
    sourcemap: true,
  },
});
```

### Next.js Fast Refresh
```javascript
// next.config.js
module.exports = {
  reactStrictMode: true,
  
  // Fast Refresh is enabled by default
  // Preserves React state during edits
  
  webpack: (config, { dev }) => {
    if (dev) {
      // Additional dev optimizations
      config.watchOptions = {
        poll: 1000,
        aggregateTimeout: 300,
      };
    }
    return config;
  },
};
```

### Webpack HMR
```javascript
// webpack.config.js
module.exports = {
  mode: 'development',
  devServer: {
    hot: true,
    port: 3000,
    open: true,
    historyApiFallback: true,
  },
  plugins: [
    new webpack.HotModuleReplacementPlugin(),
  ],
};

// In your app
if (module.hot) {
  module.hot.accept('./App', () => {
    // Handle hot update
    const NextApp = require('./App').default;
    render(<NextApp />, document.getElementById('root'));
  });
}
```

---

## 3. Backend Hot Reload

### Nodemon (Simple)
```json
// nodemon.json
{
  "watch": ["src"],
  "ext": "ts,js,json",
  "ignore": ["src/**/*.test.ts"],
  "exec": "ts-node src/index.ts",
  "delay": 1000
}

// package.json
{
  "scripts": {
    "dev": "nodemon"
  }
}
```

### tsx (Faster)
```json
// package.json
{
  "scripts": {
    "dev": "tsx watch src/index.ts"
  }
}

// Faster than ts-node + nodemon
// Built-in watch mode
// TypeScript support
```

### Node.js Native Watch (Node 18+)
```bash
# Built-in watch mode
node --watch src/index.js

# With TypeScript
node --watch --loader ts-node/esm src/index.ts
```

---

## 4. Database Hot Reload

### Prisma
```json
// package.json
{
  "scripts": {
    "db:dev": "prisma studio",
    "db:push": "prisma db push",
    "db:generate": "prisma generate --watch"
  }
}
```

```typescript
// Watch for schema changes
// Terminal 1: Watch schema
npm run db:generate

// Terminal 2: Push changes
npm run db:push

// Terminal 3: Run app
npm run dev
```

---

## 5. CSS Hot Reload

### Tailwind CSS
```javascript
// tailwind.config.js
module.exports = {
  content: [
    './src/**/*.{js,jsx,ts,tsx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};

// Watch mode
// package.json
{
  "scripts": {
    "css:watch": "tailwindcss -i ./src/input.css -o ./dist/output.css --watch"
  }
}
```

### CSS Modules
```javascript
// Vite automatically hot-reloads CSS modules
import styles from './Button.module.css';

export function Button() {
  return <button className={styles.button}>Click</button>;
}

// Edit Button.module.css → instant update
```

---

## 6. Test Hot Reload

### Jest Watch Mode
```json
// package.json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage --watch"
  }
}
```

```bash
# Run tests in watch mode
npm run test:watch

# Interactive commands:
# › Press f to run only failed tests.
# › Press o to only run tests related to changed files.
# › Press p to filter by a filename regex pattern.
# › Press t to filter by a test name regex pattern.
# › Press q to quit watch mode.
# › Press Enter to trigger a test run.
```

### Vitest (Faster)
```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'jsdom',
    watch: true,  // Always watch
    ui: true,     // Web UI
  },
});
```

```bash
# Run with UI
npm run test

# Opens browser with test results
# Auto-reruns on file changes
```

---

## 7. Docker Hot Reload

### Docker Compose with Volumes
```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    volumes:
      # Mount source code
      - ./src:/app/src
      - ./package.json:/app/package.json
      # Exclude node_modules
      - /app/node_modules
    environment:
      - NODE_ENV=development
    command: npm run dev
```

### Dockerfile for Development
```dockerfile
# Dockerfile.dev
FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy source (will be overridden by volume)
COPY . .

# Start with hot reload
CMD ["npm", "run", "dev"]
```

---

## 8. Multi-Service Hot Reload

### Turborepo
```json
// turbo.json
{
  "pipeline": {
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}

// package.json (root)
{
  "scripts": {
    "dev": "turbo run dev --parallel"
  }
}
```

```bash
# Runs all services in parallel with hot reload
npm run dev

# Output:
# • apps/web:dev: ready on http://localhost:3000
# • apps/api:dev: ready on http://localhost:4000
# • packages/ui:dev: watching for changes...
```

### Concurrently
```json
// package.json
{
  "scripts": {
    "dev:web": "cd apps/web && npm run dev",
    "dev:api": "cd apps/api && npm run dev",
    "dev": "concurrently \"npm:dev:*\""
  },
  "devDependencies": {
    "concurrently": "^8.0.0"
  }
}
```

---

## 9. Optimizing Feedback Speed

### Measure Build Time
```typescript
// measure-build.ts
const start = Date.now();

// Your build process
await build();

const duration = Date.now() - start;
console.log(`Build took ${duration}ms`);

// Target: < 1000ms for dev builds
```

### Speed Optimization Checklist
```markdown
## Build Speed Optimization

### Frontend
- [ ] Use Vite instead of Webpack (10x faster)
- [ ] Enable SWC/esbuild for transpilation
- [ ] Reduce bundle size (code splitting)
- [ ] Use shallow imports
- [ ] Exclude node_modules from watch

### Backend
- [ ] Use tsx instead of ts-node
- [ ] Use swc instead of tsc
- [ ] Enable incremental compilation
- [ ] Reduce file watch scope
- [ ] Use native Node.js watch (18+)

### Tests
- [ ] Use Vitest instead of Jest (10x faster)
- [ ] Run only changed tests
- [ ] Parallelize test execution
- [ ] Use test.only for focused testing
- [ ] Mock slow dependencies
```

---

## 10. Fast Feedback Metrics

```typescript
interface FeedbackMetrics {
  // Time from save to visible change
  hotReloadTime: number;  // Target: < 100ms
  
  // Time from save to test results
  testFeedbackTime: number;  // Target: < 1s
  
  // Time from commit to CI feedback
  ciFeedbackTime: number;  // Target: < 5min
  
  // Time from deploy to live
  deploymentTime: number;  // Target: < 10min
}

// Measure hot reload speed
const measureHotReload = () => {
  const start = performance.now();
  
  // Trigger hot reload
  // (save file)
  
  // Measure when change is visible
  const observer = new MutationObserver(() => {
    const duration = performance.now() - start;
    console.log(`Hot reload: ${duration}ms`);
    observer.disconnect();
  });
  
  observer.observe(document.body, { childList: true, subtree: true });
};
```

---

## 11. Developer Experience Enhancements

### Error Overlay
```typescript
// vite.config.ts
export default defineConfig({
  server: {
    hmr: {
      overlay: true,  // Show errors in browser
    },
  },
});

// Shows compilation errors as overlay
// No need to check terminal
```

### Auto-open Browser
```javascript
// vite.config.ts
export default defineConfig({
  server: {
    open: true,  // Auto-open browser on start
    port: 3000,
  },
});
```

### Terminal Notifications
```bash
# Install terminal-notifier (macOS)
brew install terminal-notifier

# Notify on build complete
npm run build && terminal-notifier -message "Build complete!"
```

---

## 12. Fast Feedback Checklist

- [ ] **Frontend HMR**: Hot reload working for React/Vue?
- [ ] **Backend Watch**: Server restarts on file changes?
- [ ] **CSS Hot Reload**: Styles update without refresh?
- [ ] **Test Watch**: Tests re-run on changes?
- [ ] **Docker Volumes**: Source code mounted for hot reload?
- [ ] **Build Speed**: Dev builds < 1 second?
- [ ] **Error Overlay**: Compilation errors shown in browser?
- [ ] **Auto-open**: Browser opens automatically?
- [ ] **Multi-service**: All services hot-reload together?
- [ ] **Metrics**: Feedback times measured and optimized?

---

## 13. Troubleshooting Slow Feedback

```markdown
## Common Issues

### HMR not working
- Check if HMR is enabled in config
- Verify file is being watched
- Check for syntax errors
- Restart dev server

### Slow hot reload (> 1s)
- Too many files being watched
- Large bundle size
- Slow transpilation (use esbuild/swc)
- Disable source maps in dev

### Changes not detected
- File outside watch directory
- .gitignore excluding files
- Docker volume not mounted
- WSL file system issues (Windows)

### Memory issues
- Too many files in watch
- Memory leak in dev server
- Restart dev server periodically
```

---

## Related Skills
* `45-developer-experience/dev-environment-setup`
* `45-developer-experience/local-dev-standard`
* `45-developer-experience/debugging-tools`
