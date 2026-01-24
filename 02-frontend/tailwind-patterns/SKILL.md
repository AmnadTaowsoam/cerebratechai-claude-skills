# Tailwind CSS Patterns and Best Practices

---

## 1. Executive Summary & Strategic Necessity

### 1.1 Context (ภาษาไทย)

Tailwind CSS คือ utility-first CSS framework ที่ช่วยให้ developers สร้าง UI ได้รวดเร็วและ maintainable โดยใช้ utility classes แทน custom CSS ซึ่งช่วยลด context switching ระหว่าง HTML และ CSS files

Tailwind CSS ใช้ utility-first approach ซึ่งช่วยให้ developers:
- **Rapid Development** - สร้าง UI ได้รวดเร็วด้วย utility classes
- **Consistent Design** - รักษา consistency ด้วย design tokens
- **Responsive Design** - สร้าง responsive layouts ได้ง่าย
- **Dark Mode** - Built-in dark mode support
- **Customizable** - Fully customizable ด้วย configuration files
- **Production-Ready** - Optimized สำหรับ production ด้วย JIT mode

### 1.2 Business Impact (ภาษาไทย)

**ผลกระทบทางธุรกิจ:**

1. **เพิ่ม Development Velocity** - ลดเวลาในการพัฒนา UI ได้ถึง 30-50%
2. **ลด CSS Bundle Size** - Purge unused styles ช่วยลด bundle size ได้ถึง 80%
3. **เพิ่ม Maintainability** - Consistent design tokens ช่วยเพิ่ม maintainability
4. **ลด Context Switching** - Utility classes ช่วยลดการสลับระหว่าง HTML และ CSS
5. **ปรับปรุง Consistency** - Design system ที่ consistent ช่วยเพิ่ม UX

### 1.3 Product Thinking (ภาษาไทย)

**มุมมองด้านผลิตภัณฑ์:**

1. **Utility-First** - Tailwind ต้องเป็น CSS framework หลัก
2. **Responsive** - UI ต้อง responsive ทุก devices
3. **Dark Mode** - Dark mode support ต้อง built-in
4. **Customizable** - Design system ต้อง customizable
5. **Performance** - CSS bundle ต้อง optimized สำหรับ production

---

## 2. Technical Deep Dive (The "How-to")

### 2.1 Core Logic

Tailwind CSS ประกอบด้วย:

1. **Utility Classes** - Small, single-purpose CSS classes
2. **Design Tokens** - Consistent values สำหรับ colors, spacing, typography
3. **Responsive Modifiers** - Breakpoint prefixes สำหรับ responsive design
4. **State Modifiers** - Hover, focus, active states
5. **Dark Mode** - Dark mode support ด้วย class หรือ media query
6. **JIT Mode** - Just-In-Time compiler สำหรับ production optimization
7. **Plugins** - Extensible plugin system

### 2.2 Architecture Diagram Requirements

```
┌─────────────────────────────────────────────────────────┐
│              Tailwind CSS Architecture                 │
├─────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Configuration Layer                   │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  tailwind   │  │  Theme      │  │  Plugins    │  │   │
│  │  │  config    │  │  Extension  │  │             │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Utility Layer                          │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  Layout     │  │  Typography │  │  Colors     │  │   │
│  │  │  Utilities  │  │  Utilities  │  │  Utilities  │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Modifier Layer                        │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  Responsive │  │  State      │  │  Dark       │  │   │
│  │  │  Modifiers  │  │  Modifiers  │  │  Mode       │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Build Layer                            │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  JIT Mode   │  │  Purge      │  │  Minify     │  │   │
│  │  │  Compiler   │  │  Unused     │  │  Output     │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
└─────────────────────────────────────────────────────────┘
```

### 2.3 Implementation Workflow

**Step 1: Install Tailwind CSS**

```bash
# Install Tailwind CSS
npm install -D tailwindcss postcss autoprefixer

# Initialize Tailwind
npx tailwindcss init -p
```

**Step 2: Configure Tailwind**

```javascript
// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

**Step 3: Add Tailwind Directives**

```css
/* styles.css */
@tailwind base;
@tailwind components;
@tailwind utilities;
```

---

## 3. Tooling & Tech Stack

### 3.1 Enterprise Tools

| Tool | Purpose | Version | License |
|------|---------|---------|---------|
| Tailwind CSS | Utility-First CSS Framework | ^3.4.0 | MIT |
| PostCSS | CSS Post-Processor | ^8.4.0 | MIT |
| Autoprefixer | CSS Vendor Prefixing | ^10.4.0 | MIT |
| @tailwindcss/forms | Form Plugin | ^0.5.0 | MIT |
| @tailwindcss/typography | Typography Plugin | ^0.5.0 | MIT |
| @tailwindcss/aspect-ratio | Aspect Ratio Plugin | ^0.4.0 | MIT |
| Tailwind CSS IntelliSense | VS Code Extension | Latest | MIT |

### 3.2 Configuration Essentials

**PostCSS Configuration:**
```javascript
// postcss.config.js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

**Tailwind Configuration:**
```javascript
// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class', // or 'media'
  content: [
    './src/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['Fira Code', 'monospace'],
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}
```

---

## 4. Standards, Compliance & Security

### 4.1 International Standards

- **WCAG 2.1** - Web Content Accessibility Guidelines
- **W3C CSS Standards** - CSS Specification Standards
- **ISO 9241-11** - Usability Standards
- **GDPR** - Data Protection สำหรับ User Data

### 4.2 Security Protocol

Tailwind CSS ต้องปฏิบัติตามหลักความปลอดภัย:

1. **Content Security Policy** - ใช้ CSP headers สำหรับ inline styles
2. **Input Sanitization** - Validate ข้อมูลทั้ง client และ server
3. **XSS Prevention** - ไม่ใช้ inline styles จาก user input
4. **Secure Dependencies** - ตรวจสอบ dependencies สำหรับ vulnerabilities

### 4.3 Explainability

Tailwind CSS ต้องสามารถอธิบายได้ว่า:

1. **Utility Classes** - ทำไมใช้ utility classes อย่างไร
2. **Design Tokens** - ทำไมใช้ design tokens อย่างไร
3. **Responsive Design** - ทำไมใช้ responsive modifiers อย่างไร
4. **Dark Mode** - ทำไมใช้ dark mode อย่างไร

---

## 5. Unit Economics & Performance Metrics (KPIs)

### 5.1 Cost Calculation

| Metric | Calculation | Target |
|--------|-------------|--------|
| CSS Bundle Size | CSS bundle size | < 20 KB |
| Purge Efficiency | Unused styles removed | > 80% |
| Build Time | Tailwind build time | < 5s |
| Runtime Performance | CSS parsing time | < 50ms |
| Development Velocity | UI development time | -30% |

### 5.2 Key Performance Indicators

**Technical Metrics:**

1. **CSS Bundle Size** - CSS bundle ที่ใช้งาน
2. **Purge Efficiency** - Unused styles ที่ถูกลบ
3. **Build Time** - เวลาในการ build
4. **Runtime Performance** - CSS parsing time

**Business Metrics:**

1. **Development Velocity** - เวลาในการพัฒนา UI
2. **Maintainability** - Maintainability score
3. **Consistency** - Design consistency score
4. **User Experience** - UX metrics

---

## 6. Strategic Recommendations (CTO Insights)

### 6.1 Phase Rollout

**Phase 1: Foundation (Week 1-2)**
- Install Tailwind CSS
- Setup configuration files
- Create basic utility patterns
- Implement basic components

**Phase 2: Advanced Features (Week 3-4)**
- Implement responsive design
- Add dark mode support
- Create custom utilities
- Setup plugins

**Phase 3: Optimization (Week 5-6)**
- Optimize bundle size
- Implement purge strategy
- Setup build pipeline
- Performance testing

**Phase 4: Production (Week 7-8)**
- Documentation and training
- Design system creation
- Component library
- Best practices documentation

### 6.2 Pitfalls to Avoid

1. **Over-Engineering** - ไม่ใช้ Tailwind สำหรับ simple projects
2. **Poor Configuration** - ไม่ configure Tailwind อย่างเหมาะสม
3. **Missing Purge** - ไม่ purge unused styles
4. **Inconsistent Design** - ไม่ใช้ design tokens อย่าง consistent
5. **Poor Performance** - ไม่ optimize bundle size
6. **Accessibility Issues** - ไม่ consider accessibility

### 6.3 Best Practices Checklist

- [ ] ใช้ utility classes สำหรับ rapid development
- [ ] Implement responsive design ด้วย breakpoints
- [ ] Add dark mode support
- [ ] Use design tokens สำหรับ consistency
- [ ] Purge unused styles สำหรับ production
- [ ] Optimize bundle size
- [ ] Use semantic HTML
- [ ] Consider accessibility
- [ ] Create reusable components
- [ ] Use plugins สำหรับ advanced features
- [ ] Test บนทุก browsers และ devices
- [ ] Document design system
- [ ] Use Tailwind IntelliSense
- [ ] Organize classes logically
- [ ] Use container queries สำหรับ component-level responsiveness

---

## 7. Implementation Examples

### 7.1 Configuration

**Basic Configuration:**
```javascript
// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

**Theme Customization:**
```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
        },
        secondary: {
          50: '#fdf4ff',
          100: '#fae8ff',
          500: '#d946ef',
          600: '#c026d3',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['Fira Code', 'monospace'],
      },
      spacing: {
        '128': '32rem',
        '144': '36rem',
      },
      borderRadius: {
        '4xl': '2rem',
      },
      boxShadow: {
        'glow': '0 0 20px rgba(59, 130, 246, 0.5)',
      },
    },
  },
}
```

**Custom Colors:**
```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        // Using CSS variables
        brand: {
          DEFAULT: 'var(--color-brand)',
          dark: 'var(--color-brand-dark)',
          light: 'var(--color-brand-light)',
        },
        // Using arbitrary values
        'custom-blue': '#1e40af',
        'custom-green': '#059669',
      },
    },
  },
}

// In CSS
@layer base {
  :root {
    --color-brand: #3b82f6;
    --color-brand-dark: #1d4ed8;
    --color-brand-light: #60a5fa;
  }
}
```

**Extending Utilities:**
```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      animation: {
        'fade-in': 'fadeIn 0.3s ease-in',
        'slide-up': 'slideUp 0.3s ease-out',
        'bounce-slow': 'bounce 2s infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
      },
    },
  },
}
```

**Plugin Configuration:**
```javascript
// tailwind.config.js
const plugin = require('tailwindcss/plugin')

module.exports = {
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/aspect-ratio'),
    // Custom plugin
    plugin(function({ addUtilities, addComponents, theme }) {
      addUtilities({
        '.text-shadow': {
          textShadow: '2px 2px 4px rgba(0,0,0,0.1)',
        },
        '.text-shadow-lg': {
          textShadow: '4px 4px 8px rgba(0,0,0,0.2)',
        },
      })

      addComponents({
        '.btn': {
          padding: theme('spacing.2'),
          borderRadius: theme('borderRadius.md'),
          fontWeight: theme('fontWeight.medium'),
        },
        '.btn-primary': {
          backgroundColor: theme('colors.blue.500'),
          color: theme('colors.white'),
        },
      })
    }),
  ],
}
```

### 7.2 Common Utility Patterns

**Layout (Flex):**
```html
<!-- Flex container -->
<div class="flex">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>

<!-- Flex with spacing -->
<div class="flex gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>

<!-- Flex with justify -->
<div class="flex justify-between">
  <div>Left</div>
  <div>Right</div>
</div>

<div class="flex justify-center items-center min-h-screen">
  <div>Centered content</div>
</div>

<!-- Flex column -->
<div class="flex flex-col gap-2">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>

<!-- Flex wrap -->
<div class="flex flex-wrap gap-2">
  <div class="w-1/3">Item 1</div>
  <div class="w-1/3">Item 2</div>
  <div class="w-1/3">Item 3</div>
</div>
```

**Layout (Grid):**
```html
<!-- Basic grid -->
<div class="grid grid-cols-3 gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>

<!-- Responsive grid -->
<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
  <div>Item 4</div>
</div>

<!-- Grid with spanning -->
<div class="grid grid-cols-3 gap-4">
  <div class="col-span-2">Span 2 columns</div>
  <div>Item 2</div>
  <div>Item 3</div>
  <div class="col-span-2">Span 2 columns</div>
</div>

<!-- Grid with auto-fit -->
<div class="grid grid-cols-[repeat(auto-fit,minmax(250px,1fr))] gap-4">
  <div>Auto width item 1</div>
  <div>Auto width item 2</div>
  <div>Auto width item 3</div>
</div>

<!-- Grid with areas -->
<div class="grid grid-cols-[200px_1fr] grid-rows-[auto_1fr] gap-4">
  <div class="col-span-2">Header</div>
  <div>Sidebar</div>
  <div>Main content</div>
</div>
```

**Spacing:**
```html
<!-- Padding -->
<div class="p-4">All sides</div>
<div class="px-4 py-2">Horizontal and vertical</div>
<div class="pt-4 pr-2 pb-4 pl-2">Individual sides</div>

<!-- Margin -->
<div class="m-4">All sides</div>
<div class="mx-auto my-4">Horizontal auto, vertical</div>
<div class="mt-4 mr-2 mb-4 ml-2">Individual sides</div>

<!-- Gap (for flex and grid) -->
<div class="flex gap-2">Small gap</div>
<div class="flex gap-4">Medium gap</div>
<div class="grid gap-x-4 gap-y-2">Different gaps</div>

<!-- Space between (for direct children) -->
<div class="space-y-4">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>

<div class="space-x-4 flex">
  <span>Item 1</span>
  <span>Item 2</span>
  <span>Item 3</span>
</div>
```

**Typography:**
```html
<!-- Font size -->
<h1 class="text-4xl font-bold">Heading 1</h1>
<h2 class="text-3xl font-semibold">Heading 2</h2>
<h3 class="text-2xl font-medium">Heading 3</h3>
<p class="text-base">Paragraph text</p>
<p class="text-sm">Small text</p>
<p class="text-xs">Extra small text</p>

<!-- Text color -->
<p class="text-gray-900">Dark text</p>
<p class="text-gray-500">Medium text</p>
<p class="text-gray-300">Light text</p>
<p class="text-blue-500">Blue text</p>

<!-- Text alignment -->
<p class="text-left">Left aligned</p>
<p class="text-center">Center aligned</p>
<p class="text-right">Right aligned</p>

<!-- Text transform -->
<p class="uppercase">Uppercase</p>
<p class="lowercase">Lowercase</p>
<p class="capitalize">Capitalize</p>

<!-- Line height and letter spacing -->
<p class="leading-relaxed tracking-wide">Relaxed line height with wide letter spacing</p>
<p class="leading-tight tracking-tight">Tight line height with tight letter spacing</p>

<!-- Text decoration -->
<p class="underline">Underlined text</p>
<p class="line-through">Strikethrough text</p>

<!-- Truncation -->
<p class="truncate max-w-xs">This text will be truncated if it's too long...</p>
<p class="line-clamp-2">This text will show only 2 lines and truncate the rest...</p>
```

**Colors and Backgrounds:**
```html
<!-- Background colors -->
<div class="bg-white">White background</div>
<div class="bg-gray-100">Light gray background</div>
<div class="bg-blue-500">Blue background</div>

<!-- Background with opacity -->
<div class="bg-blue-500/50">Blue with 50% opacity</div>
<div class="bg-black/20">Black with 20% opacity</div>

<!-- Gradient backgrounds -->
<div class="bg-gradient-to-r from-blue-500 to-purple-500">Horizontal gradient</div>
<div class="bg-gradient-to-b from-blue-500 to-purple-500">Vertical gradient</div>
<div class="bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500">Diagonal gradient</div>

<!-- Text colors -->
<p class="text-white">White text</p>
<p class="text-gray-900">Dark gray text</p>
<p class="text-blue-600">Blue text</p>

<!-- Text with opacity -->
<p class="text-white/50">White text with 50% opacity</p>

<!-- Border colors -->
<div class="border-2 border-blue-500">Blue border</div>
<div class="border-l-4 border-r-4 border-red-500">Left and right red border</div>

<!-- Ring (focus ring) -->
<input class="ring-2 ring-blue-500" />
<input class="ring-offset-2 ring-offset-blue-100 ring-2 ring-blue-500" />
```

### 7.3 Responsive Design

**Breakpoints:**
```html
<!-- Default breakpoint classes (mobile-first) -->
<div class="w-full md:w-1/2 lg:w-1/3 xl:w-1/4">
  Responsive width
</div>

<!-- Breakpoint values -->
<!-- sm: 640px -->
<!-- md: 768px -->
<!-- lg: 1024px -->
<!-- xl: 1280px -->
<!-- 2xl: 1536px -->

<!-- Responsive display -->
<div class="hidden md:block">
  Hidden on mobile, visible on tablet and up
</div>

<div class="block md:hidden">
  Visible on mobile, hidden on tablet and up
</div>

<!-- Responsive flex direction -->
<div class="flex flex-col md:flex-row">
  <div>Column on mobile, row on desktop</div>
</div>

<!-- Responsive grid -->
<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
  <div>1 col on mobile, 2 on small, 3 on medium, 4 on large</div>
</div>

<!-- Responsive spacing -->
<div class="p-4 md:p-8 lg:p-12">
  Different padding on different screens
</div>

<!-- Responsive text -->
<h1 class="text-2xl md:text-3xl lg:text-4xl">
  Responsive heading size
</h1>
```

**Mobile-First Approach:**
```html
<!-- Mobile-first: Start with mobile styles, add breakpoints for larger screens -->
<div class="
  w-full           /* Mobile: full width */
  md:w-3/4        /* Tablet: 75% width */
  lg:w-2/3        /* Desktop: 66% width */
  xl:w-1/2        /* Large desktop: 50% width */
">
  Content
</div>

<!-- Navigation example -->
<nav class="
  flex
  flex-col        /* Mobile: column layout */
  md:flex-row     /* Desktop: row layout */
  gap-4
  md:gap-8
">
  <a href="#">Home</a>
  <a href="#">About</a>
  <a href="#">Contact</a>
</nav>

<!-- Card grid -->
<div class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
  <div class="card">Card 1</div>
  <div class="card">Card 2</div>
  <div class="card">Card 3</div>
</div>
```

### 7.4 Component Patterns

**Buttons:**
```html
<!-- Primary button -->
<button class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors">
  Primary Button
</button>

<!-- Secondary button -->
<button class="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300 transition-colors">
  Secondary Button
</button>

<!-- Outline button -->
<button class="px-4 py-2 border-2 border-blue-500 text-blue-500 rounded hover:bg-blue-500 hover:text-white transition-colors">
  Outline Button
</button>

<!-- Danger button -->
<button class="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition-colors">
  Delete
</button>

<!-- Button with icon -->
<button class="flex items-center gap-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
  </svg>
  Add Item
</button>

<!-- Loading button -->
<button class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 flex items-center gap-2">
  <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
  </svg>
  Loading...
</button>

<!-- Button sizes -->
<button class="px-2 py-1 text-sm bg-blue-500 text-white rounded">Small</button>
<button class="px-4 py-2 bg-blue-500 text-white rounded">Medium</button>
<button class="px-6 py-3 text-lg bg-blue-500 text-white rounded">Large</button>

<!-- Disabled button -->
<button class="px-4 py-2 bg-gray-300 text-gray-500 rounded cursor-not-allowed" disabled>
  Disabled
</button>
```

**Cards:**
```html
<!-- Basic card -->
<div class="bg-white rounded-lg shadow-md p-6">
  <h2 class="text-xl font-bold mb-2">Card Title</h2>
  <p class="text-gray-600">Card content goes here...</p>
</div>

<!-- Card with image -->
<div class="bg-white rounded-lg shadow-md overflow-hidden">
  <img src="image.jpg" alt="Card image" class="w-full h-48 object-cover" />
  <div class="p-6">
    <h2 class="text-xl font-bold mb-2">Card Title</h2>
    <p class="text-gray-600">Card content goes here...</p>
  </div>
</div>

<!-- Card with hover effect -->
<div class="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 p-6">
  <h2 class="text-xl font-bold mb-2">Card Title</h2>
  <p class="text-gray-600">Card content goes here...</p>
</div>

<!-- Horizontal card -->
<div class="bg-white rounded-lg shadow-md overflow-hidden flex">
  <img src="image.jpg" alt="Card image" class="w-48 h-48 object-cover" />
  <div class="p-6 flex-1">
    <h2 class="text-xl font-bold mb-2">Card Title</h2>
    <p class="text-gray-600">Card content goes here...</p>
  </div>
</div>

<!-- Card with badge -->
<div class="bg-white rounded-lg shadow-md p-6 relative">
  <span class="absolute top-4 right-4 bg-blue-500 text-white text-xs px-2 py-1 rounded">New</span>
  <h2 class="text-xl font-bold mb-2">Card Title</h2>
  <p class="text-gray-600">Card content goes here...</p>
</div>

<!-- Card with actions -->
<div class="bg-white rounded-lg shadow-md p-6">
  <h2 class="text-xl font-bold mb-2">Card Title</h2>
  <p class="text-gray-600 mb-4">Card content goes here...</p>
  <div class="flex gap-2">
    <button class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">Action</button>
    <button class="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300">Cancel</button>
  </div>
</div>
```

**Forms:**
```html
<!-- Form container -->
<form class="max-w-md mx-auto space-y-4">
  <!-- Text input -->
  <div>
    <label for="name" class="block text-sm font-medium text-gray-700 mb-1">Name</label>
    <input
      type="text"
      id="name"
      name="name"
      class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
      placeholder="Enter your name"
    />
  </div>

  <!-- Email input -->
  <div>
    <label for="email" class="block text-sm font-medium text-gray-700 mb-1">Email</label>
    <input
      type="email"
      id="email"
      name="email"
      class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
      placeholder="Enter your email"
    />
  </div>

  <!-- Password input -->
  <div>
    <label for="password" class="block text-sm font-medium text-gray-700 mb-1">Password</label>
    <input
      type="password"
      id="password"
      name="password"
      class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
      placeholder="Enter your password"
    />
  </div>

  <!-- Select dropdown -->
  <div>
    <label for="country" class="block text-sm font-medium text-gray-700 mb-1">Country</label>
    <select
      id="country"
      name="country"
      class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
    >
      <option value="">Select a country</option>
      <option value="us">United States</option>
      <option value="uk">United Kingdom</option>
      <option value="th">Thailand</option>
    </select>
  </div>

  <!-- Textarea -->
  <div>
    <label for="message" class="block text-sm font-medium text-gray-700 mb-1">Message</label>
    <textarea
      id="message"
      name="message"
      rows="4"
      class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
      placeholder="Enter your message"
    ></textarea>
  </div>

  <!-- Checkbox -->
  <div class="flex items-center">
    <input
      type="checkbox"
      id="terms"
      name="terms"
      class="w-4 h-4 text-blue-500 border-gray-300 rounded focus:ring-blue-500"
    />
    <label for="terms" class="ml-2 text-sm text-gray-700">I agree to the terms and conditions</label>
  </div>

  <!-- Radio buttons -->
  <div>
    <label class="block text-sm font-medium text-gray-700 mb-2">Gender</label>
    <div class="space-y-2">
      <label class="flex items-center">
        <input type="radio" name="gender" value="male" class="w-4 h-4 text-blue-500" />
        <span class="ml-2">Male</span>
      </label>
      <label class="flex items-center">
        <input type="radio" name="gender" value="female" class="w-4 h-4 text-blue-500" />
        <span class="ml-2">Female</span>
      </label>
    </div>
  </div>

  <!-- Submit button -->
  <button
    type="submit"
    class="w-full px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors"
  >
    Submit
  </button>
</form>

<!-- Inline form -->
<form class="flex gap-2">
  <input
    type="text"
    placeholder="Search..."
    class="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
  />
  <button type="submit" class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600">
    Search
  </button>
</form>
```

**Navigation:**
```html
<!-- Simple nav -->
<nav class="flex items-center justify-between p-4 bg-white shadow">
  <div class="text-xl font-bold">Logo</div>
  <div class="flex gap-4">
    <a href="#" class="text-gray-700 hover:text-blue-500">Home</a>
    <a href="#" class="text-gray-700 hover:text-blue-500">About</a>
    <a href="#" class="text-gray-700 hover:text-blue-500">Contact</a>
  </div>
</nav>

<!-- Responsive nav with mobile menu -->
<nav class="flex items-center justify-between p-4 bg-white shadow">
  <div class="text-xl font-bold">Logo</div>

  <!-- Desktop menu -->
  <div class="hidden md:flex gap-4">
    <a href="#" class="text-gray-700 hover:text-blue-500">Home</a>
    <a href="#" class="text-gray-700 hover:text-blue-500">About</a>
    <a href="#" class="text-gray-700 hover:text-blue-500">Contact</a>
  </div>

  <!-- Mobile menu button -->
  <button class="md:hidden">
    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
    </svg>
  </button>
</nav>

<!-- Tab navigation -->
<div class="border-b border-gray-200">
  <nav class="flex gap-4">
    <a href="#" class="px-4 py-2 border-b-2 border-blue-500 text-blue-500">Tab 1</a>
    <a href="#" class="px-4 py-2 border-b-2 border-transparent text-gray-500 hover:text-gray-700">Tab 2</a>
    <a href="#" class="px-4 py-2 border-b-2 border-transparent text-gray-500 hover:text-gray-700">Tab 3</a>
  </nav>
</div>

<!-- Sidebar navigation -->
<div class="flex min-h-screen">
  <aside class="w-64 bg-gray-900 text-white">
    <div class="p-4">
      <h1 class="text-xl font-bold">Logo</h1>
    </div>
    <nav class="mt-4">
      <a href="#" class="flex items-center gap-3 px-4 py-3 bg-gray-800">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
        </svg>
        Dashboard
      </a>
      <a href="#" class="flex items-center gap-3 px-4 py-3 hover:bg-gray-800">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
        </svg>
        Users
      </a>
      <a href="#" class="flex items-center gap-3 px-4 py-3 hover:bg-gray-800">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
        Settings
      </a>
    </nav>
  </aside>
  <main class="flex-1 p-6">
    <!-- Main content -->
  </main>
</div>
```

### 7.5 Dark Mode Implementation

**Using Class Strategy:**
```javascript
// tailwind.config.js
module.exports = {
  darkMode: 'class', // or 'media' for system preference
  // ...
}
```

```html
<!-- Dark mode toggle button -->
<button id="darkModeToggle" class="p-2 rounded bg-gray-200 dark:bg-gray-700">
  <svg class="w-6 h-6 hidden dark:block" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
  </svg>
  <svg class="w-6 h-6 block dark:hidden" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
  </svg>
</button>

<script>
  // Toggle dark mode
  const toggle = document.getElementById('darkModeToggle')
  toggle.addEventListener('click', () => {
    document.documentElement.classList.toggle('dark')
  })
</script>
```

**Dark Mode Styles:**
```html
<!-- Text colors -->
<p class="text-gray-900 dark:text-gray-100">Adaptive text color</p>

<!-- Background colors -->
<div class="bg-white dark:bg-gray-900">Adaptive background</div>

<!-- Borders -->
<div class="border-gray-200 dark:border-gray-700">Adaptive border</div>

<!-- Complete card example -->
<div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
  <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-2">Card Title</h2>
  <p class="text-gray-600 dark:text-gray-300">Card content...</p>
  <button class="mt-4 px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded">
    Action
  </button>
</div>

<!-- Form inputs -->
<input
  type="text"
  class="w-full px-3 py-2 bg-white dark:bg-gray-800 border-gray-300 dark:border-gray-600 text-gray-900 dark:text-white rounded-md focus:ring-blue-500"
  placeholder="Enter text"
/>

<!-- Navigation -->
<nav class="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700">
  <a href="#" class="text-gray-700 dark:text-gray-300 hover:text-blue-500">Link</a>
</nav>
```

### 7.6 Custom Utilities with @apply

**Creating Component Classes:**
```css
/* styles.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer components {
  .btn {
    @apply px-4 py-2 rounded font-medium transition-colors;
  }

  .btn-primary {
    @apply bg-blue-500 text-white hover:bg-blue-600;
  }

  .btn-secondary {
    @apply bg-gray-200 text-gray-800 hover:bg-gray-300;
  }

  .btn-danger {
    @apply bg-red-500 text-white hover:bg-red-600;
  }

  .card {
    @apply bg-white rounded-lg shadow-md p-6;
  }

  .input {
    @apply w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500;
  }
}

@layer utilities {
  .text-shadow {
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
  }

  .scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
  }

  .scrollbar-hide::-webkit-scrollbar {
    display: none;
  }
}
```

```html
<!-- Using custom classes -->
<button class="btn btn-primary">Primary Button</button>
<button class="btn btn-secondary">Secondary Button</button>

<div class="card">
  <h2>Card Title</h2>
  <p>Card content...</p>
</div>

<input type="text" class="input" placeholder="Enter text" />
```

### 7.7 Performance Optimization

**Purge Unused Styles:**
```javascript
// tailwind.config.js
module.exports = {
  content: [
    './src/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  // This automatically removes unused styles in production
}
```

**JIT Mode (Default in v3+):**
```javascript
// tailwind.config.js
module.exports = {
  // JIT is enabled by default in Tailwind CSS v3+
  mode: 'jit',
  // ...
}
```

**Minimize Arbitrary Values:**
```html
<!-- Avoid excessive arbitrary values -->
<div class="w-[123px] h-[456px] mt-[78px]">Not recommended</div>

<!-- Use theme values when possible -->
<div class="w-32 h-40 mt-20">Recommended</div>
```

**Group Related Utilities:**
```html
<!-- Group related utilities together -->
<div class="
  flex items-center justify-between
  p-4 bg-white rounded-lg shadow-md
  hover:shadow-lg transition-shadow
">
  Content
</div>
```

### 7.8 Common Layouts

**Center Layout:**
```html
<div class="min-h-screen flex items-center justify-center">
  <div>Centered content</div>
</div>
```

**Sidebar Layout:**
```html
<div class="flex min-h-screen">
  <aside class="w-64 bg-gray-900 text-white">
    <!-- Sidebar content -->
  </aside>
  <main class="flex-1 bg-gray-100">
    <!-- Main content -->
  </main>
</div>
```

**Header-Footer Layout:**
```html
<div class="min-h-screen flex flex-col">
  <header class="bg-white shadow">
    <!-- Header content -->
  </header>
  <main class="flex-1">
    <!-- Main content -->
  </main>
  <footer class="bg-gray-900 text-white">
    <!-- Footer content -->
  </footer>
</div>
```

**Masonry Grid:**
```html
<div class="columns-1 sm:columns-2 md:columns-3 lg:columns-4 gap-4">
  <div class="break-inside-avoid mb-4">
    <!-- Card 1 -->
  </div>
  <div class="break-inside-avoid mb-4">
    <!-- Card 2 -->
  </div>
  <div class="break-inside-avoid mb-4">
    <!-- Card 3 -->
  </div>
</div>
```

### 7.9 Best Practices

**Use Semantic HTML:**
```html
<!-- Good: Semantic HTML -->
<nav class="flex justify-between p-4">
  <a href="#" class="font-bold">Logo</a>
  <ul class="flex gap-4">
    <li><a href="#" class="hover:text-blue-500">Home</a></li>
    <li><a href="#" class="hover:text-blue-500">About</a></li>
  </ul>
</nav>

<!-- Avoid: Non-semantic div soup -->
<div class="flex justify-between p-4">
  <div class="font-bold">Logo</div>
  <div class="flex gap-4">
    <div><a href="#" class="hover:text-blue-500">Home</a></div>
    <div><a href="#" class="hover:text-blue-500">About</a></div>
  </div>
</div>
```

**Extract Reusable Components:**
```html
<!-- Instead of repeating button styles everywhere -->
<button class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">Button</button>

<!-- Create a component -->
<button class="btn btn-primary">Button</button>
```

**Use Responsive Prefixes Sparingly:**
```html
<!-- Good: Only override what changes -->
<div class="w-full md:w-1/2">
  Half width on desktop
</div>

<!-- Avoid: Over-specifying -->
<div class="w-full w-full w-full md:w-1/2 md:w-1/2 lg:w-1/2">
  Redundant classes
</div>
```

**Use Arbitrary Values Judiciously:**
```html
<!-- Good: For one-off values -->
<div class="w-[374px]">Specific width needed</div>

<!-- Better: Add to theme if used multiple times -->
<div class="w-sidebar">Sidebar width</div>
```

**Use the Tailwind IntelliSense Extension:**
- Install the Tailwind CSS IntelliSense extension for VS Code
- Provides autocomplete, hover previews, and linting

**Organize Classes Logically:**
```html
<div class="
  flex items-center justify-between
  p-4 bg-white rounded-lg shadow-md
  hover:shadow-lg transition-all duration-200
">
  <!-- Layout -->
  <!-- Spacing -->
  <!-- Colors -->
  <!-- Effects -->
</div>
```

**Use Container Queries (when supported):**
```html
<div class="@container">
  <div class="@lg:text-xl @md:text-base text-sm">
    Responsive text based on container
  </div>
</div>
```

---

## 8. Related Skills

- `02-frontend/react-best-practices`
- `02-frontend/nextjs-patterns`
- `02-frontend/shadcn-ui`
- `22-ux-ui-design/design-systems`
- `22-ux-ui-design/responsive-design`
