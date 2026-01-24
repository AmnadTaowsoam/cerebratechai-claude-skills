---
name: Accessibility (a11y)
description: Ensuring websites and applications are usable by everyone, including people with disabilities, following WCAG guidelines and accessibility best practices.
---

# Accessibility (a11y)

> **Current Level:** Intermediate  
> **Domain:** UX/UI Design / Compliance

---

## Overview

Web accessibility ensures that websites and applications are usable by everyone, including people with disabilities. Following WCAG (Web Content Accessibility Guidelines) principles makes your applications perceivable, operable, understandable, and robust for all users.

---

## Core Concepts

### 1. WCAG Guidelines Overview

### WCAG 2.1 Principles

```markdown
# WCAG 2.1 Principles

## POUR Principles

### 1. Perceivable
Information and user interface components must be presentable to users in ways they can perceive.

#### Guidelines
- **1.1 Text Alternatives**: Provide text alternatives for any non-text content
- **1.2 Time-based Media**: Provide alternatives for time-based media
- **1.3 Adaptable**: Create content that can be presented in different ways
- **1.4 Distinguishable**: Make it easier for users to see and hear content

### 2. Operable
User interface components and navigation must be operable.

#### Guidelines
- **2.1 Keyboard Accessible**: Make all functionality available from a keyboard
- **2.2 Enough Time**: Provide users enough time to read and use content
- **2.3 Seizures and Physical Reactions**: Do not design content in a way that is known to cause seizures
- **2.4 Navigable**: Provide ways to help users navigate, find content, and determine where they are
- **2.5 Input Modalities**: Make it easier for users to operate functionality through various inputs

### 3. Understandable
Information and the operation of user interface must be understandable.

#### Guidelines
- **3.1 Readable**: Make text content readable and understandable
- **3.2 Predictable**: Make Web pages appear and operate in predictable ways
- **3.3 Input Assistance**: Help users avoid and correct mistakes

### 4. Robust
Content must be robust enough that it can be interpreted reliably by a wide variety of user agents, including assistive technologies.

#### Guidelines
- **4.1 Compatible**: Maximize compatibility with current and future user agents

## Conformance Levels

### Level A
- Minimum level of accessibility
- Basic accessibility features
- Most basic assistive technology support

### Level AA
- Recommended level
- Addresses major accessibility barriers
- Standard for most organizations

### Level AAA
- Highest level
- Most comprehensive accessibility
- May not be feasible for all content
```

---

## 2. Semantic HTML

### Using Semantic Elements

```html
<!-- Good: Semantic HTML -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Page Title</title>
</head>
<body>
  <header>
    <nav aria-label="Main navigation">
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/about">About</a></li>
        <li><a href="/contact">Contact</a></li>
      </ul>
    </nav>
  </header>
  
  <main>
    <article>
      <h1>Article Title</h1>
      <p>Article content...</p>
    </article>
    
    <aside>
      <h2>Related Articles</h2>
      <ul>
        <li><a href="/article-1">Article 1</a></li>
        <li><a href="/article-2">Article 2</a></li>
      </ul>
    </aside>
  </main>
  
  <footer>
    <p>&copy; 2024 Company Name</p>
  </footer>
</body>
</html>

<!-- Bad: Non-semantic HTML -->
<!DOCTYPE html>
<html>
<head>
  <title>Page Title</title>
</head>
<body>
  <div class="header">
    <div class="nav">
      <a href="/">Home</a>
      <a href="/about">About</a>
      <a href="/contact">Contact</a>
    </div>
  </div>
  
  <div class="content">
    <div class="article">
      <div class="title">Article Title</div>
      <div class="text">Article content...</div>
    </div>
    
    <div class="sidebar">
      <div class="title">Related Articles</div>
      <a href="/article-1">Article 1</a>
      <a href="/article-2">Article 2</a>
    </div>
  </div>
  
  <div class="footer">
    <p>&copy; 2024 Company Name</p>
  </div>
</body>
</html>
```

### Headings

```html
<!-- Good: Proper heading hierarchy -->
<h1>Main Page Title</h1>
<h2>Section Title</h2>
<h3>Subsection Title</h3>
<p>Content...</p>
<h3>Another Subsection</h3>
<p>Content...</p>
<h2>Another Section</h2>
<h3>Subsection Title</h3>
<p>Content...</p>

<!-- Bad: Skipped heading levels -->
<h1>Main Page Title</h1>
<h3>Subsection Title</h3>
<p>Content...</p>
<h4>Another Subsection</h4>
<p>Content...</p>

<!-- Bad: Using styling instead of headings -->
<div class="h1">Main Page Title</div>
<div class="h2">Section Title</div>
```

### Lists

```html
<!-- Good: Semantic lists -->
<ul>
  <li>Item 1</li>
  <li>Item 2</li>
  <li>Item 3</li>
</ul>

<ol>
  <li>Step 1</li>
  <li>Step 2</li>
  <li>Step 3</li>
</ol>

<dl>
  <dt>Term 1</dt>
  <dd>Definition 1</dd>
  <dt>Term 2</dt>
  <dd>Definition 2</dd>
</dl>

<!-- Bad: Non-semantic lists -->
<div class="list">
  <div class="item">Item 1</div>
  <div class="item">Item 2</div>
  <div class="item">Item 3</div>
</div>
```

---

## 3. ARIA Attributes

### ARIA Roles

```html
<!-- Landmark Roles -->
<nav aria-label="Main navigation">
  <ul>
    <li><a href="/">Home</a></li>
    <li><a href="/about">About</a></li>
  </ul>
</nav>

<main role="main">
  <h1>Main Content</h1>
  <p>Content...</p>
</main>

<aside aria-label="Sidebar">
  <h2>Related Content</h2>
  <p>Content...</p>
</aside>

<footer role="contentinfo">
  <p>&copy; 2024 Company</p>
</footer>

<!-- Widget Roles -->
<button aria-pressed="false" onclick="toggle()">
  Toggle Button
</button>

<div role="tablist">
  <button role="tab" aria-selected="true" aria-controls="panel1">
    Tab 1
  </button>
  <button role="tab" aria-selected="false" aria-controls="panel2">
    Tab 2
  </button>
</div>

<div role="tabpanel" id="panel1">
  <p>Tab 1 content</p>
</div>

<div role="tabpanel" id="panel2" hidden>
  <p>Tab 2 content</p>
</div>

<!-- Live Regions -->
<div aria-live="polite" aria-atomic="true">
  Status messages will appear here
</div>

<div aria-live="assertive">
  Important alerts will appear here
</div>
```

### ARIA States and Properties

```html
<!-- Expanded/Collapsed -->
<button aria-expanded="false" aria-controls="menu">
  Menu
</button>
<ul id="menu" hidden>
  <li><a href="/item1">Item 1</a></li>
  <li><a href="/item2">Item 2</a></li>
</ul>

<!-- Disabled -->
<button aria-disabled="true">
  Disabled Button
</button>

<!-- Required -->
<input
  type="email"
  required
  aria-required="true"
  aria-invalid="false"
  aria-describedby="email-error"
/>
<p id="email-error" class="error-message">
  Please enter a valid email address
</p>

<!-- Labels -->
<label for="username">Username</label>
<input
  id="username"
  type="text"
  aria-label="Username"
/>

<!-- Descriptions -->
<input
  type="password"
  aria-describedby="password-help"
/>
<p id="password-help">
  Password must be at least 8 characters
</p>

<!-- Current Value -->
<div role="progressbar" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100">
  75% complete
</div>

<!-- Selected -->
<ul role="listbox">
  <li role="option" aria-selected="true">Option 1</li>
  <li role="option" aria-selected="false">Option 2</li>
  <li role="option" aria-selected="false">Option 3</li>
</ul>
```

---

## 4. Keyboard Navigation

### Keyboard Accessible Components

```tsx
// Keyboard Accessible Button
export const Button = ({ children, onClick, disabled }: ButtonProps) => {
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault()
      onClick?.()
    }
  }

  return (
    <button
      onClick={onClick}
      onKeyDown={handleKeyDown}
      disabled={disabled}
      tabIndex={disabled ? -1 : 0}
      aria-disabled={disabled}
    >
      {children}
    </button>
  )
}

// Keyboard Accessible Dropdown
export const Dropdown = ({ options, onSelect }: DropdownProps) => {
  const [isOpen, setIsOpen] = useState(false)
  const [focusedIndex, setFocusedIndex] = useState(-1)
  const containerRef = useRef<HTMLDivElement>(null)

  const handleKeyDown = (e: React.KeyboardEvent) => {
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault()
        setFocusedIndex((prev) => 
          prev < options.length - 1 ? prev + 1 : prev
        )
        break
      case 'ArrowUp':
        e.preventDefault()
        setFocusedIndex((prev) => 
          prev > 0 ? prev - 1 : prev
        )
        break
      case 'Enter':
      case ' ':
        e.preventDefault()
        if (focusedIndex >= 0) {
          onSelect(options[focusedIndex])
          setIsOpen(false)
        }
        break
      case 'Escape':
        setIsOpen(false)
        setFocusedIndex(-1)
        break
    }
  }

  return (
    <div ref={containerRef} onKeyDown={handleKeyDown}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        aria-expanded={isOpen}
        aria-haspopup="listbox"
      >
        Select Option
      </button>
      {isOpen && (
        <ul role="listbox" aria-activedescendant={`option-${focusedIndex}`}>
          {options.map((option, index) => (
            <li
              key={option.value}
              id={`option-${index}`}
              role="option"
              aria-selected={focusedIndex === index}
              onClick={() => {
                onSelect(option)
                setIsOpen(false)
              }}
              style={{
                background: focusedIndex === index ? '#e0f2fe' : 'transparent',
              }}
            >
              {option.label}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
```

### Focus Management

```tsx
// Focus Trap
export const Modal = ({ isOpen, onClose, children }: ModalProps) => {
  const modalRef = useRef<HTMLDivElement>(null)
  const previousFocusRef = useRef<HTMLElement | null>(null)

  useEffect(() => {
    if (isOpen) {
      // Store previous focus
      previousFocusRef.current = document.activeElement as HTMLElement
      
      // Focus modal
      modalRef.current?.focus()
      
      // Trap focus
      const handleKeyDown = (e: KeyboardEvent) => {
        if (e.key === 'Tab') {
          const focusableElements = modalRef.current?.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
          ) as NodeListOf<HTMLElement>
          
          const firstElement = focusableElements[0]
          const lastElement = focusableElements[focusableElements.length - 1]
          
          if (e.shiftKey) {
            if (document.activeElement === firstElement) {
              e.preventDefault()
              lastElement?.focus()
            }
          } else {
            if (document.activeElement === lastElement) {
              e.preventDefault()
              firstElement?.focus()
            }
          }
        }
      }
      
      document.addEventListener('keydown', handleKeyDown)
      
      return () => {
        document.removeEventListener('keydown', handleKeyDown)
        // Restore focus
        previousFocusRef.current?.focus()
      }
    }
  }, [isOpen])

  if (!isOpen) return null

  return (
    <div
      ref={modalRef}
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
      tabIndex={-1}
    >
      <h2 id="modal-title">Modal Title</h2>
      {children}
      <button onClick={onClose}>Close</button>
    </div>
  )
}
```

---

## 5. Screen Reader Support

### Screen Reader Best Practices

```tsx
// Screen Reader Announcements
export const LiveAnnouncer = () => {
  const [announcement, setAnnouncement] = useState('')

  const announce = (message: string) => {
    setAnnouncement('')
    setTimeout(() => setAnnouncement(message), 100)
  }

  return (
    <div
      role="status"
      aria-live="polite"
      aria-atomic="true"
      className="sr-only"
    >
      {announcement}
    </div>
  )
}

// Usage
const announcer = useLiveAnnouncer()

// Announce changes
announcer.announce('Item added to cart')

// Skip Link
export const SkipLink = () => {
  return (
    <a
      href="#main-content"
      className="skip-link"
    >
      Skip to main content
    </a>
  )
}

// Hidden Content
export const ScreenReaderOnly = ({ children }: { children: React.ReactNode }) => {
  return (
    <span
      style={{
        position: 'absolute',
        width: '1px',
        height: '1px',
        padding: 0,
        margin: '-1px',
        overflow: 'hidden',
        clip: 'rect(0, 0, 0, 0)',
        whiteSpace: 'nowrap',
        borderWidth: 0,
      }}
    >
      {children}
    </span>
  )
}

// Usage
<ScreenReaderOnly>Current page: Page 1 of 5</ScreenReaderOnly>
```

---

## 6. Color Contrast

### Contrast Requirements

```typescript
// Color Contrast Checker
function getContrastRatio(color1: string, color2: string): number {
  const luminance1 = getLuminance(color1)
  const luminance2 = getLuminance(color2)
  
  const lighter = Math.max(luminance1, luminance2)
  const darker = Math.min(luminance1, luminance2)
  
  return (lighter + 0.05) / (darker + 0.05)
}

function getLuminance(color: string): number {
  const rgb = hexToRgb(color)
  
  const [r, g, b] = rgb.map(c => {
    c = c / 255
    return c <= 0.03928
      ? c / 12.92
      : Math.pow((c + 0.055) / 1.055, 2.4)
  })
  
  return 0.2126 * r + 0.7152 * g + 0.0722 * b
}

function hexToRgb(hex: string): [number, number, number] {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex)
  return result
    ? [
        parseInt(result[1], 16),
        parseInt(result[2], 16),
        parseInt(result[3], 16),
      ]
    : [0, 0, 0]
}

// WCAG Requirements
function meetsWCAG(foreground: string, background: string, level: 'AA' | 'AAA', size: 'normal' | 'large'): boolean {
  const ratio = getContrastRatio(foreground, background)
  
  if (level === 'AA') {
    return size === 'normal'
      ? ratio >= 4.5
      : ratio >= 3
  } else if (level === 'AAA') {
    return size === 'normal'
      ? ratio >= 7
      : ratio >= 4.5
  }
  
  return false
}

// Examples
const ratio = getContrastRatio('#000000', '#ffffff') // 21:1
const meetsAA = meetsWCAG('#000000', '#ffffff', 'AA', 'normal') // true
const meetsAAA = meetsWCAG('#000000', '#ffffff', 'AAA', 'normal') // true
```

### Accessible Color Palettes

```css
/* Accessible Color Palette */
:root {
  /* Primary Colors - AA compliant */
  --color-primary-500: #0ea5e9;
  --color-primary-600: #0284c7;
  --color-primary-700: #0369a1;
  
  /* Text Colors - AA compliant */
  --color-text-primary: #111827;
  --color-text-secondary: #4b5563;
  --color-text-tertiary: #9ca3af;
  
  /* Background Colors */
  --color-bg-primary: #ffffff;
  --color-bg-secondary: #f9fafb;
  --color-bg-tertiary: #f3f4f6;
  
  /* Semantic Colors */
  --color-success: #10b981;
  --color-warning: #f59e0b;
  --color-error: #ef4444;
  --color-info: #3b82f6;
}

/* Accessible Text */
.text-primary {
  color: var(--color-text-primary);
}

.text-secondary {
  color: var(--color-text-secondary);
}

.text-tertiary {
  color: var(--color-text-tertiary);
}

/* Accessible Buttons */
.btn-primary {
  background-color: var(--color-primary-600);
  color: #ffffff;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
}

.btn-primary:hover {
  background-color: var(--color-primary-700);
}

.btn-primary:focus {
  outline: 2px solid var(--color-primary-500);
  outline-offset: 2px;
}

/* Accessible Links */
a {
  color: var(--color-primary-600);
  text-decoration: underline;
}

a:hover {
  color: var(--color-primary-700);
}

a:focus {
  outline: 2px solid var(--color-primary-500);
  outline-offset: 2px;
}
```

---

## 7. Focus Management

### Focus Styles

```css
/* Focus Styles */
:focus {
  outline: 2px solid #0ea5e9;
  outline-offset: 2px;
}

/* Focus Visible - Only for keyboard focus */
:focus-visible {
  outline: 2px solid #0ea5e9;
  outline-offset: 2px;
}

/* Focus Within - When child is focused */
:focus-within {
  border-color: #0ea5e9;
}

/* Remove Focus for Mouse */
button:focus:not(:focus-visible) {
  outline: none;
}

/* Custom Focus Styles */
.custom-focus:focus-visible {
  box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.3);
  border-color: #0ea5e9;
}

/* Focus Order */
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: #0ea5e9;
  color: white;
  padding: 8px;
  text-decoration: none;
  z-index: 100;
}

.skip-link:focus {
  top: 0;
}
```

### Focus Management in React

```tsx
// Focus Management Hook
export function useFocusManagement() {
  const focusableElementsRef = useRef<HTMLElement[]>([])

  const addFocusable = (element: HTMLElement) => {
    focusableElementsRef.current.push(element)
  }

  const removeFocusable = (element: HTMLElement) => {
    focusableElementsRef.current = focusableElementsRef.current.filter(
      el => el !== element
    )
  }

  const focusFirst = () => {
    const first = focusableElementsRef.current[0]
    first?.focus()
  }

  const focusLast = () => {
    const last = focusableElementsRef.current[
      focusableElementsRef.current.length - 1
    ]
    last?.focus()
  }

  const focusNext = (current: HTMLElement) => {
    const index = focusableElementsRef.current.indexOf(current)
    const next = focusableElementsRef.current[index + 1]
    next?.focus()
  }

  const focusPrevious = (current: HTMLElement) => {
    const index = focusableElementsRef.current.indexOf(current)
    const previous = focusableElementsRef.current[index - 1]
    previous?.focus()
  }

  return {
    addFocusable,
    removeFocusable,
    focusFirst,
    focusLast,
    focusNext,
    focusPrevious,
  }
}
```

---

## 8. Form Accessibility

### Accessible Forms

```tsx
// Accessible Form Component
export const FormField = ({
  label,
  id,
  error,
  hint,
  required,
  children,
}: FormFieldProps) => {
  const fieldId = id || `field-${Math.random()}`
  const errorId = `${fieldId}-error`
  const hintId = `${fieldId}-hint`

  return (
    <div className="form-field">
      <label htmlFor={fieldId} className="form-label">
        {label}
        {required && <span className="required">*</span>}
      </label>
      
      {hint && (
        <p id={hintId} className="form-hint">
          {hint}
        </p>
      )}
      
      {React.cloneElement(children as React.ReactElement, {
        id: fieldId,
        'aria-describedby': `${hint ? hintId : ''} ${error ? errorId : ''}`,
        'aria-invalid': !!error,
        'aria-required': required,
      })}
      
      {error && (
        <p id={errorId} className="form-error" role="alert">
          {error}
        </p>
      )}
    </div>
  )
}

// Usage
<FormField
  label="Email"
  id="email"
  error={errors.email}
  hint="We'll never share your email"
  required
>
  <input
    type="email"
    value={email}
    onChange={e => setEmail(e.target.value)}
  />
</FormField>

// Accessible Radio Group
export const RadioGroup = ({ label, name, options, value, onChange }: RadioGroupProps) => {
  const groupId = `radio-group-${Math.random()}`

  return (
    <fieldset className="radio-group">
      <legend className="radio-group-label">{label}</legend>
      
      {options.map((option, index) => (
        <div key={option.value} className="radio-item">
          <input
            type="radio"
            id={`${groupId}-${index}`}
            name={name}
            value={option.value}
            checked={value === option.value}
            onChange={() => onChange(option.value)}
            aria-describedby={`${groupId}-hint`}
          />
          <label htmlFor={`${groupId}-${index}`}>
            {option.label}
          </label>
        </div>
      ))}
    </fieldset>
  )
}

// Accessible Checkbox Group
export const CheckboxGroup = ({ label, name, options, value, onChange }: CheckboxGroupProps) => {
  const groupId = `checkbox-group-${Math.random()}`

  return (
    <fieldset className="checkbox-group">
      <legend className="checkbox-group-label">{label}</legend>
      
      {options.map((option, index) => (
        <div key={option.value} className="checkbox-item">
          <input
            type="checkbox"
            id={`${groupId}-${index}`}
            name={name}
            value={option.value}
            checked={value.includes(option.value)}
            onChange={(e) => {
              if (e.target.checked) {
                onChange([...value, option.value])
              } else {
                onChange(value.filter(v => v !== option.value))
              }
            }}
            aria-describedby={`${groupId}-hint`}
          />
          <label htmlFor={`${groupId}-${index}`}>
            {option.label}
          </label>
        </div>
      ))}
    </fieldset>
  )
}
```

---

## 9. Image Alt Text

### Writing Alt Text

```html
<!-- Informative Images -->
<img
  src="/chart.png"
  alt="Bar chart showing 50% increase in sales from 2023 to 2024"
/>

<!-- Decorative Images -->
<img
  src="/decoration.png"
  alt=""
  role="presentation"
/>

<!-- Functional Images -->
<button>
  <img src="/search-icon.png" alt="Search" />
</button>

<a href="/profile">
  <img src="/profile.png" alt="View John Doe's profile" />
</a>

<!-- Complex Images -->
<img
  src="/infographic.png"
  alt="Infographic showing company growth: 2020: $1M, 2021: $2M, 2022: $5M, 2023: $10M"
/>
<p>Detailed description available in text format below.</p>

<!-- Images with Text -->
<img
  src="/banner.png"
  alt="Banner text: '50% off all items this weekend only'"
/>

<!-- Data Tables -->
<img
  src="/table.png"
  alt="Data table showing quarterly results: Q1: $1.2M, Q2: $1.5M, Q3: $1.8M, Q4: $2.1M"
/>
<table>
  <caption>Quarterly Results</caption>
  <thead>
    <tr>
      <th>Quarter</th>
      <th>Revenue</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Q1</td>
      <td>$1.2M</td>
    </tr>
    <tr>
      <td>Q2</td>
      <td>$1.5M</td>
    </tr>
    <tr>
      <td>Q3</td>
      <td>$1.8M</td>
    </tr>
    <tr>
      <td>Q4</td>
      <td>$2.1M</td>
    </tr>
  </tbody>
</table>
```

---

## 10. Skip Links

### Skip Navigation Links

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Page Title</title>
  <style>
    .skip-link {
      position: absolute;
      top: -40px;
      left: 0;
      background: #0ea5e9;
      color: white;
      padding: 8px;
      text-decoration: none;
      z-index: 100;
      transition: top 0.3s;
    }

    .skip-link:focus {
      top: 0;
    }
  </style>
</head>
<body>
  <!-- Skip Links -->
  <a href="#main-content" class="skip-link">
    Skip to main content
  </a>
  <a href="#navigation" class="skip-link">
    Skip to navigation
  </a>

  <!-- Navigation -->
  <nav id="navigation" aria-label="Main navigation">
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/about">About</a></li>
      <li><a href="/contact">Contact</a></li>
    </ul>
  </nav>

  <!-- Main Content -->
  <main id="main-content">
    <h1>Main Content</h1>
    <p>Content...</p>
  </main>
</body>
</html>
```

---

## 11. Testing Tools

### Accessibility Testing Tools

```markdown
# Testing Tools

## 1. Browser Extensions

### axe DevTools
- **Features**: Automated testing, detailed reports
- **Best For**: Quick testing during development
- **Cost**: Free

### WAVE
- **Features**: Visual feedback, detailed errors
- **Best For**: Visual testing
- **Cost**: Free

### Lighthouse
- **Features**: Performance, accessibility, SEO
- **Best For**: Comprehensive testing
- **Cost**: Free

## 2. Online Tools

### WAVE Web Accessibility Evaluation Tool
- **URL**: https://wave.webaim.org/
- **Features**: Visual feedback, detailed reports
- **Best For**: Quick website testing

### axe DevTools Browser Extension
- **URL**: https://www.deque.com/axe/
- **Features**: Automated testing, detailed reports
- **Best For**: Browser-based testing

### WebAIM Contrast Checker
- **URL**: https://webaim.org/resources/contrastchecker/
- **Features**: Color contrast testing
- **Best For**: Color testing

## 3. Screen Readers

### NVDA (Windows)
- **Features**: Free, powerful
- **Best For**: Windows testing
- **Cost**: Free

### JAWS (Windows)
- **Features**: Comprehensive, enterprise
- **Best For**: Enterprise testing
- **Cost**: Paid

### VoiceOver (Mac)
- **Features**: Built-in, comprehensive
- **Best For**: Mac testing
- **Cost**: Free (built-in)

### TalkBack (Android)
- **Features**: Built-in, comprehensive
- **Best For**: Android testing
- **Cost**: Free (built-in)

## 4. Automated Testing

### Jest + jest-axe
```javascript
import { axe, toHaveNoViolations } from 'jest-axe'

expect.extend(toHaveNoViolations)

test('accessibility', async () => {
  const render = () => ReactDOM.render(<App />, container)
  const results = await axe(container)
  
  expect(results).toHaveNoViolations()
})
```

### Cypress + cypress-axe
```javascript
import 'cypress-axe'

describe('Accessibility', () => {
  beforeEach(() => {
    cy.injectAxe()
  })

  it('has no detectable a11y violations on load', () => {
    cy.checkA11y()
  })

  it('has no detectable a11y violations on navigation', () => {
    cy.get('nav').checkA11y()
  })
})
```
```

---

## 12. Automated Testing

### Automated Accessibility Testing

```typescript
// Automated Accessibility Testing
import { axe, toHaveNoViolations } from 'jest-axe'

expect.extend(toHaveNoViolations)

describe('Button Component', () => {
  it('should have no accessibility violations', async () => {
    const { container } = render(<Button>Click me</Button>)
    const results = await axe(container)
    
    expect(results).toHaveNoViolations()
  })

  it('should be keyboard accessible', () => {
    const { getByRole } = render(<Button>Click me</Button>)
    const button = getByRole('button')
    
    // Should be focusable
    expect(button).toHaveAttribute('tabIndex', '0')
    
    // Should have role
    expect(button).toHaveAttribute('role', 'button')
  })

  it('should have proper ARIA attributes when disabled', () => {
    const { getByRole } = render(<Button disabled>Click me</Button>)
    const button = getByRole('button')
    
    expect(button).toHaveAttribute('aria-disabled', 'true')
    expect(button).toHaveAttribute('tabIndex', '-1')
  })
})

describe('Form Component', () => {
  it('should have no accessibility violations', async () => {
    const { container } = render(
      <Form>
        <FormField label="Email" required>
          <input type="email" />
        </FormField>
      </Form>
    )
    const results = await axe(container)
    
    expect(results).toHaveNoViolations()
  })

  it('should have proper labels', () => {
    const { getByLabelText } = render(
      <Form>
        <FormField label="Email">
          <input type="email" />
        </FormField>
      </Form>
    )
    
    const input = getByLabelText('Email')
    expect(input).toBeInTheDocument()
  })

  it('should have proper error messages', () => {
    const { getByRole, getByText } = render(
      <Form>
        <FormField label="Email" error="Invalid email">
          <input type="email" />
        </FormField>
      </Form>
    )
    
    const input = getByRole('textbox')
    expect(input).toHaveAttribute('aria-invalid', 'true')
    expect(getByText('Invalid email')).toBeInTheDocument()
  })
})
```

---

## 13. Manual Testing

### Manual Testing Checklist

```markdown
# Manual Testing Checklist

## Keyboard Navigation
- [ ] Can navigate using Tab key
- [ ] Can navigate using Shift+Tab
- [ ] Can activate elements using Enter/Space
- [ ] Can escape modals using Escape
- [ ] Focus order is logical
- [ ] Focus indicators are visible

## Screen Reader
- [ ] All content is announced
- [ ] Images have alt text
- [ ] Forms have labels
- [ ] Errors are announced
- [ ] Status updates are announced
- [ ] Navigation is clear

## Color Contrast
- [ ] Text meets WCAG AA contrast ratio
- [ ] Links are distinguishable from text
- [ ] Focus indicators are visible
- [ ] Error messages are visible

## Forms
- [ ] All form fields have labels
- [ ] Required fields are indicated
- [ ] Error messages are clear
- [ ] Help text is available
- [ ] Success messages are provided

## Responsive Design
- [ ] Works on mobile devices
- [ ] Works on tablet devices
- [ ] Works on desktop devices
- [ ] Touch targets are large enough
- [ ] Content is readable at all sizes

## Multimedia
- [ ] Videos have captions
- [ ] Audio has transcripts
- [ ] Auto-play is disabled
- [ ] Controls are accessible
- [ ] Alternatives are provided
```

---

## 14. Common Issues and Fixes

### Common Accessibility Issues

```markdown
# Common Issues and Fixes

## 1. Missing Alt Text

**Issue**: Images without alt text

**Fix**:
```html
<!-- Bad -->
<img src="/image.png" />

<!-- Good -->
<img src="/image.png" alt="Description of image" />
```

## 2. Missing Form Labels

**Issue**: Form inputs without labels

**Fix**:
```html
<!-- Bad -->
<input type="text" placeholder="Name" />

<!-- Good -->
<label for="name">Name</label>
<input id="name" type="text" />
```

## 3. Poor Color Contrast

**Issue**: Text and background don't have enough contrast

**Fix**:
```css
/* Bad */
.text {
  color: #cccccc;
  background-color: #ffffff;
}

/* Good */
.text {
  color: #111827;
  background-color: #ffffff;
}
```

## 4. Keyboard Inaccessibility

**Issue**: Elements can't be accessed via keyboard

**Fix**:
```tsx
// Bad
<div onClick={handleClick}>Click me</div>

// Good
<button onClick={handleClick}>Click me</button>
```

## 5. Missing Focus Indicators

**Issue**: No visual indication of focus

**Fix**:
```css
/* Bad */
button:focus {
  outline: none;
}

/* Good */
button:focus-visible {
  outline: 2px solid #0ea5e9;
  outline-offset: 2px;
}
```

## 6. Empty Links

**Issue**: Links without descriptive text

**Fix**:
```html
<!-- Bad -->
<a href="/page">Click here</a>

<!-- Good -->
<a href="/page">Read more about our products</a>
```

## 7. Auto-playing Media

**Issue**: Audio/video auto-plays

**Fix**:
```html
<!-- Bad -->
<video autoplay>
  <source src="/video.mp4" type="video/mp4" />
</video>

<!-- Good -->
<video controls>
  <source src="/video.mp4" type="video/mp4" />
</video>
```

## 8. Heading Hierarchy

**Issue**: Incorrect heading levels

**Fix**:
```html
<!-- Bad -->
<h1>Title</h1>
<h3>Subtitle</h3>

<!-- Good -->
<h1>Title</h1>
<h2>Subtitle</h2>
```
```

---

## 15. Best Practices

### Accessibility Best Practices

```markdown
# Best Practices

## 1. Use Semantic HTML
- Use proper HTML elements
- Maintain heading hierarchy
- Use semantic lists
- Provide landmarks

## 2. Provide Alternative Text
- All images need alt text
- Describe functional images
- Mark decorative images
- Provide text alternatives

## 3. Ensure Keyboard Access
- All elements keyboard accessible
- Logical focus order
- Visible focus indicators
- Keyboard shortcuts documented

## 4. Support Screen Readers
- Use ARIA attributes
- Provide live regions
- Announce changes
- Test with screen readers

## 5. Ensure Color Contrast
- Meet WCAG AA requirements
- Don't rely on color alone
- Test with color blindness
- Provide high contrast options

## 6. Make Forms Accessible
- Provide clear labels
- Indicate required fields
- Show error messages
- Provide help text

## 7. Test Thoroughly
- Test with keyboard
- Test with screen readers
- Test with different browsers
- Test on different devices

## 8. Use Testing Tools
- Automated testing
- Manual testing
- User testing
- Regular audits

## 9. Document Accessibility
- Document accessibility features
- Provide accessibility guides
- Train team members
- Share best practices

## 10. Iterate and Improve
- Gather feedback
- Monitor issues
- Make improvements
- Stay updated
```

---

## Quick Reference

### Quick Tips

```markdown
# Quick Tips

## Do's
- ✓ Use semantic HTML
- ✓ Provide alt text for images
- ✓ Ensure keyboard accessibility
- ✓ Test with screen readers
- ✓ Meet color contrast requirements
- ✓ Provide form labels
- ✓ Use ARIA attributes
- ✓ Test regularly

## Don'ts
- ✗ Use divs for buttons
- ✗ Skip alt text
- ✗ Rely on color alone
- ✗ Hide focus indicators
- ✗ Use auto-playing media
- ✗ Skip form labels
- ✗ Ignore keyboard users
- ✗ Forget to test
```

### ARIA Quick Reference

```markdown
# ARIA Quick Reference

## Roles
- `role="button"` - Button
- `role="link"` - Link
- `role="navigation"` - Navigation
- `role="main"` - Main content
- `role="search"` - Search
- `role="alert"` - Alert
- `role="dialog"` - Dialog/Modal

## States
- `aria-expanded` - Expanded/collapsed
- `aria-pressed` - Pressed/unpressed
- `aria-selected` - Selected/unselected
- `aria-checked` - Checked/unchecked
- `aria-disabled` - Disabled
- `aria-invalid` - Invalid

## Properties
- `aria-label` - Accessible label
- `aria-labelledby` - Labelled by element
- `aria-describedby` - Described by element
- `aria-hidden` - Hidden from screen readers
- `aria-live` - Live region
- `aria-controls` - Controlled element
```

---

## Quick Start

### Basic Accessibility Checklist

```html
<!-- 1. Semantic HTML -->
<header>
  <nav aria-label="Main navigation">
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/about">About</a></li>
    </ul>
  </nav>
</header>

<main>
  <!-- 2. Proper heading hierarchy -->
  <h1>Page Title</h1>
  <h2>Section Title</h2>
  
  <!-- 3. Alt text for images -->
  <img src="photo.jpg" alt="Description of image">
  
  <!-- 4. Form labels -->
  <form>
    <label for="email">Email</label>
    <input type="email" id="email" name="email" required>
    
    <button type="submit">Submit</button>
  </form>
  
  <!-- 5. Skip link -->
  <a href="#main-content" class="skip-link">Skip to main content</a>
</main>
```

### Testing with Screen Reader

```bash
# Install screen reader testing tools
npm install --save-dev @axe-core/react

# Run accessibility tests
npm run test:a11y
```

---

## Production Checklist

- [ ] **WCAG Compliance**: Meet WCAG 2.1 Level AA minimum
- [ ] **Semantic HTML**: Use proper HTML5 semantic elements
- [ ] **ARIA Attributes**: Add ARIA when needed, but prefer semantic HTML
- [ ] **Keyboard Navigation**: All functionality accessible via keyboard
- [ ] **Focus Management**: Visible focus indicators, logical tab order
- [ ] **Color Contrast**: Minimum 4.5:1 for normal text, 3:1 for large text
- [ ] **Alt Text**: All images have descriptive alt text
- [ ] **Form Labels**: All form inputs have associated labels
- [ ] **Error Messages**: Clear, accessible error messages
- [ ] **Skip Links**: Skip navigation links for keyboard users
- [ ] **Screen Reader Testing**: Test with NVDA, JAWS, or VoiceOver
- [ ] **Automated Testing**: Run axe-core or similar tools in CI/CD
- [ ] **Manual Testing**: Keyboard-only navigation testing
- [ ] **Documentation**: Document accessibility features

---

## Anti-patterns

### ❌ Don't: Missing Alt Text

```html
<!-- ❌ Bad - No alt text -->
<img src="photo.jpg">
```

```html
<!-- ✅ Good - Descriptive alt text -->
<img src="photo.jpg" alt="A red bicycle parked outside a coffee shop">
```

### ❌ Don't: Div Buttons

```html
<!-- ❌ Bad - Not keyboard accessible -->
<div onclick="handleClick()">Click me</div>
```

```html
<!-- ✅ Good - Use button element -->
<button onclick="handleClick()">Click me</button>
```

### ❌ Don't: Poor Color Contrast

```css
/* ❌ Bad - Low contrast */
.text {
  color: #ccc;
  background: #fff;
}
```

```css
/* ✅ Good - WCAG AA compliant */
.text {
  color: #333;
  background: #fff;
}
```

### ❌ Don't: Missing Form Labels

```html
<!-- ❌ Bad - No label -->
<input type="email" name="email">
```

```html
<!-- ✅ Good - Associated label -->
<label for="email">Email</label>
<input type="email" id="email" name="email">
```

### ❌ Don't: No Focus Indicators

```css
/* ❌ Bad - No visible focus */
button:focus {
  outline: none;
}
```

```css
/* ✅ Good - Visible focus */
button:focus {
  outline: 2px solid #0066cc;
  outline-offset: 2px;
}
```

---

## Integration Points

- **Form Handling** (`02-frontend/form-handling/`) - Accessible form patterns
- **React Best Practices** (`02-frontend/react-best-practices/`) - Accessible React components
- **Design Systems** (`22-ux-ui-design/design-systems/`) - Accessible component libraries
- **Testing** (`16-testing/`) - Accessibility testing strategies

---

## Further Reading

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [WebAIM](https://webaim.org/)
- [A11y Project](https://www.a11yproject.com/)
- [axe DevTools](https://www.deque.com/axe/devtools/)
