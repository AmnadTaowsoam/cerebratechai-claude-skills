---
name: Design Systems
description: Creating unified sets of design standards, reusable components, and comprehensive documentation for building consistent user interfaces across products and teams.
---

# Design Systems

> **Current Level:** Intermediate  
> **Domain:** UX/UI Design / Frontend

---

## Overview

Design systems provide a unified set of design standards, components, and documentation for building consistent user interfaces. Effective design systems include component libraries, style guides, usage guidelines, and design tokens that enable teams to build cohesive products efficiently.

---

## Core Concepts

### 1. Design System Concepts

### What is a Design System

```markdown
# Design System Concepts

## Definition

A design system is a collection of reusable components, guided by clear standards, that can be assembled to build any number of applications.

## Components of a Design System

### 1. Design Tokens
- Colors
- Typography
- Spacing
- Shadows
- Borders

### 2. Components
- Buttons
- Inputs
- Cards
- Modals
- Navigation

### 3. Patterns
- Layouts
- Templates
- User flows
- Best practices

### 4. Documentation
- Guidelines
- Examples
- Usage rules
- Code snippets

### 5. Governance
- Contribution process
- Review process
- Versioning
- Maintenance

## Benefits

### For Designers
- Consistency across products
- Faster design process
- Reusable components
- Clear guidelines

### For Developers
- Ready-to-use components
- Consistent implementation
- Reduced development time
- Clear documentation

### For Users
- Consistent experience
- Familiar patterns
- Better usability
- Improved accessibility

### For Business
- Faster time to market
- Reduced costs
- Better quality
- Scalable growth
```

---

## 2. Components

### Atomic Design

```markdown
# Atomic Design

## Hierarchy

### Atoms
The smallest building blocks of the design system.

**Examples:**
- Buttons
- Inputs
- Icons
- Labels
- Colors
- Typography

```typescript
// Atom: Button
export const Button = ({ children, variant = 'primary', ...props }) => {
  return (
    <button className={`btn btn-${variant}`} {...props}>
      {children}
    </button>
  )
}
```

### Molecules
Groups of atoms that work together.

**Examples:**
- Search bar (input + button)
- Form field (label + input + error)
- Card header (title + subtitle)
- List item (icon + text + action)

```typescript
// Molecule: SearchBar
export const SearchBar = ({ onSearch }) => {
  const [query, setQuery] = useState('')

  return (
    <div className="search-bar">
      <Input
        value={query}
        onChange={setQuery}
        placeholder="Search..."
      />
      <Button onClick={() => onSearch(query)}>
        Search
      </Button>
    </div>
  )
}
```

### Organisms
Complex components composed of molecules and atoms.

**Examples:**
- Header (logo + navigation + user menu)
- Footer (links + social + copyright)
- Card (image + title + description + actions)
- Form (multiple form fields)

```typescript
// Organism: Card
export const Card = ({ image, title, description, actions }) => {
  return (
    <div className="card">
      {image && <img src={image} alt={title} />}
      <div className="card-content">
        <h3>{title}</h3>
        <p>{description}</p>
        {actions && <div className="card-actions">{actions}</div>}
      </div>
    </div>
  )
}
```

### Templates
Page-level structures that organize organisms.

**Examples:**
- Page layout (header + main + footer)
- Dashboard layout (sidebar + content + header)
- Form layout (header + form + actions)

```typescript
// Template: PageLayout
export const PageLayout = ({ header, sidebar, children, footer }) => {
  return (
    <div className="page-layout">
      {header && <header className="page-header">{header}</header>}
      <div className="page-body">
        {sidebar && <aside className="page-sidebar">{sidebar}</aside>}
        <main className="page-content">{children}</main>
      </div>
      {footer && <footer className="page-footer">{footer}</footer>}
    </div>
  )
}
```

### Pages
Specific instances of templates with real content.

**Examples:**
- Home page
- About page
- Contact page
- Product page

```typescript
// Page: HomePage
export const HomePage = () => {
  return (
    <PageLayout
      header={<Header />}
      sidebar={<Sidebar />}
      footer={<Footer />}
    >
      <Hero />
      <Features />
      <Testimonials />
      <CTA />
    </PageLayout>
  )
}
```
```

### Component Library

```typescript
// Component Library Structure

// atoms/
export { Button } from './Button'
export { Input } from './Input'
export { Label } from './Label'
export { Icon } from './Icon'

// molecules/
export { SearchBar } from './SearchBar'
export { FormField } from './FormField'
export { CardHeader } from './CardHeader'

// organisms/
export { Header } from './Header'
export { Footer } from './Footer'
export { Card } from './Card'

// templates/
export { PageLayout } from './PageLayout'
export { DashboardLayout } from './DashboardLayout'
```

---

## 3. Design Tokens

### Token Structure

```typescript
// Design Tokens

// colors.ts
export const colors = {
  // Primary
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
  
  // Secondary
  secondary: {
    50: '#f5f3ff',
    100: '#ede9fe',
    200: '#ddd6fe',
    300: '#c4b5fd',
    400: '#a78bfa',
    500: '#8b5cf6',
    600: '#7c3aed',
    700: '#6d28d9',
    800: '#5b21b6',
    900: '#4c1d95',
  },
  
  // Neutral
  gray: {
    50: '#f9fafb',
    100: '#f3f4f6',
    200: '#e5e7eb',
    300: '#d1d5db',
    400: '#9ca3af',
    500: '#6b7280',
    600: '#4b5563',
    700: '#374151',
    800: '#1f2937',
    900: '#111827',
  },
  
  // Semantic
  success: '#10b981',
  warning: '#f59e0b',
  error: '#ef4444',
  info: '#3b82f6',
}

// typography.ts
export const typography = {
  fontFamily: {
    sans: 'Inter, -apple-system, BlinkMacSystemFont, sans-serif',
    mono: 'Fira Code, monospace',
  },
  
  fontSize: {
    xs: '0.75rem',    // 12px
    sm: '0.875rem',   // 14px
    base: '1rem',      // 16px
    lg: '1.125rem',    // 18px
    xl: '1.25rem',     // 20px
    '2xl': '1.5rem',   // 24px
    '3xl': '1.875rem', // 30px
    '4xl': '2.25rem',  // 36px
    '5xl': '3rem',     // 48px
  },
  
  fontWeight: {
    light: '300',
    normal: '400',
    medium: '500',
    semibold: '600',
    bold: '700',
  },
  
  lineHeight: {
    tight: '1.25',
    normal: '1.5',
    relaxed: '1.75',
  },
  
  letterSpacing: {
    tight: '-0.025em',
    normal: '0',
    wide: '0.025em',
  },
}

// spacing.ts
export const spacing = {
  0: '0',
  1: '0.25rem',   // 4px
  2: '0.5rem',    // 8px
  3: '0.75rem',   // 12px
  4: '1rem',      // 16px
  5: '1.25rem',   // 20px
  6: '1.5rem',    // 24px
  8: '2rem',      // 32px
  10: '2.5rem',   // 40px
  12: '3rem',     // 48px
  16: '4rem',     // 64px
  20: '5rem',     // 80px
  24: '6rem',     // 96px
}

// shadows.ts
export const shadows = {
  sm: '0 1px 2px 0 rgb(0 0 0 / 0.05)',
  base: '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)',
  md: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
  lg: '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
  xl: '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',
}

// borders.ts
export const borders = {
  none: 'none',
  base: '1px solid #e5e7eb',
  rounded: {
    none: '0',
    sm: '0.125rem',
    base: '0.25rem',
    md: '0.375rem',
    lg: '0.5rem',
    xl: '0.75rem',
    full: '9999px',
  },
}

// breakpoints.ts
export const breakpoints = {
  sm: '640px',
  md: '768px',
  lg: '1024px',
  xl: '1280px',
  '2xl': '1536px',
}
```

### Using Tokens

```typescript
// Using Design Tokens
import { colors, typography, spacing } from './design-tokens'

export const Card = ({ title, children }) => {
  return (
    <div style={{
      backgroundColor: colors.gray[50],
      padding: spacing[4],
      borderRadius: borders.rounded.lg,
      boxShadow: shadows.md,
    }}>
      <h3 style={{
        fontSize: typography.fontSize.lg,
        fontWeight: typography.fontWeight.semibold,
        color: colors.gray[900],
        marginBottom: spacing[2],
      }}>
        {title}
      </h3>
      <div style={{
        fontSize: typography.fontSize.base,
        color: colors.gray[700],
        lineHeight: typography.lineHeight.normal,
      }}>
        {children}
      </div>
    </div>
  )
}
```

---

## 4. Component Library

### Building a Component Library

```typescript
// Button Component
import { colors, spacing, typography, borders, shadows } from '../design-tokens'

interface ButtonProps {
  children: React.ReactNode
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
  onClick?: () => void
  type?: 'button' | 'submit' | 'reset'
}

export const Button = ({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  onClick,
  type = 'button',
}: ButtonProps) => {
  const baseStyles = {
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontWeight: typography.fontWeight.medium,
    borderRadius: borders.rounded.md,
    cursor: disabled ? 'not-allowed' : 'pointer',
    transition: 'all 0.2s ease',
    border: 'none',
    outline: 'none',
  }

  const variantStyles = {
    primary: {
      backgroundColor: disabled ? colors.gray[300] : colors.primary[600],
      color: colors.white,
      '&:hover': {
        backgroundColor: disabled ? colors.gray[300] : colors.primary[700],
      },
    },
    secondary: {
      backgroundColor: disabled ? colors.gray[200] : colors.secondary[600],
      color: colors.white,
      '&:hover': {
        backgroundColor: disabled ? colors.gray[200] : colors.secondary[700],
      },
    },
    outline: {
      backgroundColor: 'transparent',
      border: `1px solid ${colors.gray[300]}`,
      color: colors.gray[700],
      '&:hover': {
        backgroundColor: colors.gray[50],
      },
    },
    ghost: {
      backgroundColor: 'transparent',
      color: colors.gray[700],
      '&:hover': {
        backgroundColor: colors.gray[100],
      },
    },
  }

  const sizeStyles = {
    sm: {
      padding: `${spacing[2]} ${spacing[3]}`,
      fontSize: typography.fontSize.sm,
    },
    md: {
      padding: `${spacing[3]} ${spacing[4]}`,
      fontSize: typography.fontSize.base,
    },
    lg: {
      padding: `${spacing[4]} ${spacing[6]}`,
      fontSize: typography.fontSize.lg,
    },
  }

  return (
    <button
      type={type}
      disabled={disabled}
      onClick={onClick}
      style={{
        ...baseStyles,
        ...variantStyles[variant],
        ...sizeStyles[size],
      }}
    >
      {children}
    </button>
  )
}

// Input Component
interface InputProps {
  label?: string
  placeholder?: string
  value?: string
  onChange?: (value: string) => void
  error?: string
  disabled?: boolean
  type?: 'text' | 'email' | 'password' | 'number'
}

export const Input = ({
  label,
  placeholder,
  value,
  onChange,
  error,
  disabled = false,
  type = 'text',
}: InputProps) => {
  return (
    <div style={{ marginBottom: spacing[4] }}>
      {label && (
        <label
          style={{
            display: 'block',
            fontSize: typography.fontSize.sm,
            fontWeight: typography.fontWeight.medium,
            color: colors.gray[700],
            marginBottom: spacing[2],
          }}
        >
          {label}
        </label>
      )}
      <input
        type={type}
        value={value}
        onChange={(e) => onChange?.(e.target.value)}
        placeholder={placeholder}
        disabled={disabled}
        style={{
          width: '100%',
          padding: `${spacing[3]} ${spacing[4]}`,
          fontSize: typography.fontSize.base,
          border: error
            ? `1px solid ${colors.error}`
            : `1px solid ${colors.gray[300]}`,
          borderRadius: borders.rounded.md,
          backgroundColor: disabled ? colors.gray[100] : colors.white,
          color: colors.gray[900],
          outline: 'none',
          transition: 'border-color 0.2s ease',
          '&:focus': {
            borderColor: error ? colors.error : colors.primary[600],
            boxShadow: error
              ? `0 0 0 3px ${colors.error}20`
              : `0 0 0 3px ${colors.primary[600]}20`,
          },
        }}
      />
      {error && (
        <p
          style={{
            marginTop: spacing[2],
            fontSize: typography.fontSize.sm,
            color: colors.error,
          }}
        >
          {error}
        </p>
      )}
    </div>
  )
}
```

---

## 5. Documentation

### Component Documentation

```markdown
# Button Component

## Overview

The Button component triggers an action or navigation when clicked.

## Usage

```tsx
import { Button } from '@design-system/components'

export default function Example() {
  return (
    <Button variant="primary" onClick={() => console.log('Clicked')}>
      Click me
    </Button>
  )
}
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `ReactNode` | - | Button content |
| `variant` | `'primary' \| 'secondary' \| 'outline' \| 'ghost'` | `'primary'` | Button style variant |
| `size` | `'sm' \| 'md' \| 'lg'` | `'md'` | Button size |
| `disabled` | `boolean` | `false` | Disable the button |
| `onClick` | `() => void` | - | Click handler |
| `type` | `'button' \| 'submit' \| 'reset'` | `'button'` | Button type |

## Variants

### Primary
```tsx
<Button variant="primary">Primary Button</Button>
```

### Secondary
```tsx
<Button variant="secondary">Secondary Button</Button>
```

### Outline
```tsx
<Button variant="outline">Outline Button</Button>
```

### Ghost
```tsx
<Button variant="ghost">Ghost Button</Button>
```

## Sizes

### Small
```tsx
<Button size="sm">Small Button</Button>
```

### Medium
```tsx
<Button size="md">Medium Button</Button>
```

### Large
```tsx
<Button size="lg">Large Button</Button>
```

## States

### Disabled
```tsx
<Button disabled>Disabled Button</Button>
```

### Loading
```tsx
<Button disabled>
  <Spinner />
  Loading...
</Button>
```

## Accessibility

- Keyboard navigable
- Focus visible
- ARIA attributes
- Screen reader support

## Best Practices

- Use descriptive button text
- Don't use buttons for navigation (use links)
- Provide loading state for async actions
- Use appropriate variants for actions
```

---

## 6. Versioning

### Design System Versioning

```markdown
# Versioning

## Semantic Versioning

### MAJOR (X.0.0)
- Breaking changes
- Removed components
- Changed APIs
- Updated design tokens

### MINOR (0.X.0)
- New components
- New variants
- New features
- Backward compatible

### PATCH (0.0.X)
- Bug fixes
- Small improvements
- Documentation updates
- Performance improvements

## Versioning Strategy

### 1.0.0 - Initial Release
- Core components
- Design tokens
- Documentation
- Examples

### 1.1.0 - New Components
- Add new components
- Add new variants
- Update documentation

### 2.0.0 - Breaking Changes
- Update design tokens
- Remove deprecated components
- Change component APIs
- Migration guide

## Migration Guide

### 1.0.0 → 2.0.0

#### Breaking Changes

**Button Component**
- `size="small"` → `size="sm"`
- `size="medium"` → `size="md"`
- `size="large"` → `size="lg"`

**Colors**
- `colors.blue` → `colors.primary`
- `colors.purple` → `colors.secondary`

#### Migration Steps

1. Update component imports
2. Update color references
3. Update size props
4. Test your application

#### Example

**Before:**
```tsx
<Button size="small">Click</Button>
<div style={{ color: colors.blue[500] }}>
```

**After:**
```tsx
<Button size="sm">Click</Button>
<div style={{ color: colors.primary[500] }}>
```
```

---

## 7. Figma to Code

### Figma Integration

```markdown
# Figma to Code

## Design Tokens in Figma

### 1. Create Design Tokens
- Define colors
- Define typography
- Define spacing
- Define effects

### 2. Create Components
- Build components
- Create variants
- Add auto-layout
- Document properties

### 3. Create Styles
- Text styles
- Color styles
- Effect styles
- Grid styles

## Exporting from Figma

### 1. Design Tokens
```json
// tokens.json
{
  "colors": {
    "primary": {
      "50": "#f0f9ff",
      "500": "#0ea5e9",
      "900": "#0c4a6e"
    }
  },
  "typography": {
    "fontSize": {
      "base": "16px",
      "lg": "18px"
    }
  }
}
```

### 2. Component Properties
```json
// button-props.json
{
  "variant": "primary",
  "size": "md",
  "disabled": false
}
```

## Code Generation

### 1. Use Plugins
- Figma to Code
- Anima
- Figma Tokens
- Design Tokens Plugin

### 2. Generate Components
```tsx
// Generated Button Component
export const Button = ({
  variant = 'primary',
  size = 'md',
  disabled = false,
  children,
}: ButtonProps) => {
  return (
    <button
      className={`btn btn-${variant} btn-${size} ${disabled ? 'btn-disabled' : ''}`}
    >
      {children}
    </button>
  )
}
```

### 3. Generate Styles
```css
/* Generated CSS */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 500;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
  outline: none;
}

.btn-primary {
  background-color: #0ea5e9;
  color: white;
}

.btn-sm {
  padding: 0.5rem 0.75rem;
  font-size: 0.875rem;
}

.btn-md {
  padding: 0.75rem 1rem;
  font-size: 1rem;
}
```
```

---

## 8. Tools

### Design System Tools

```markdown
# Tools

## 1. Storybook

### Features
- Component development
- Interactive documentation
- Visual testing
- Addons ecosystem

### Best For
- Component libraries
- Design systems
- Documentation

### Pricing
- Free and open source

## 2. Figma

### Features
- Design tools
- Component libraries
- Prototyping
- Collaboration

### Best For
- Design
- Prototyping
- Handoff

### Pricing
- Freemium

## 3. Zeroheight

### Features
- Design system documentation
- Figma integration
- Code snippets
- Collaboration

### Best For
- Documentation
- Collaboration
- Enterprise

### Pricing
- Paid

## 4. Chromatic

### Features
- Visual testing
- Component testing
- CI/CD integration
- Visual regression

### Best For
- Testing
- CI/CD
- Visual regression

### Pricing
- Freemium

## 5. Style Dictionary

### Features
- Design token management
- Multi-platform output
- Transformations
- Build process

### Best For
- Design tokens
- Multi-platform
- Build automation

### Pricing
- Free and open source
```

---

## 9. Governance

### Design System Governance

```markdown
# Governance

## Contribution Process

### 1. Propose Changes
- Create issue
- Describe change
- Provide rationale
- Attach designs

### 2. Review Process
- Design review
- Technical review
- Accessibility review
- Approval

### 3. Implementation
- Create PR
- Update documentation
- Add examples
- Test changes

### 4. Release
- Version bump
- Release notes
- Announce changes
- Update docs

## Review Checklist

### Design Review
- [ ] Follows design principles
- [ ] Consistent with system
- [ ] Accessible
- [ ] Responsive
- [ ] Well documented

### Technical Review
- [ ] Code quality
- [ ] Performance
- [ ] Accessibility
- [ ] Browser support
- [ ] Tests included

### Documentation Review
- [ ] Clear description
- [ ] Examples provided
- [ ] Props documented
- [ ] Best practices included

## Maintenance

### Regular Tasks
- Review issues
- Update components
- Fix bugs
- Improve documentation

### Periodic Tasks
- Audit components
- Update dependencies
- Review metrics
- Gather feedback

## Metrics

### Adoption
- Component usage
- Team adoption
- Project usage
- Feedback scores

### Quality
- Bug reports
- Performance metrics
- Accessibility scores
- Test coverage

### Satisfaction
- User feedback
- NPS scores
- Survey results
- Support tickets
```

---

## 10. Adoption Strategies

### Driving Adoption

```markdown
# Adoption Strategies

## 1. Start Small

### Pilot Projects
- Choose 1-2 projects
- Work closely with teams
- Gather feedback
- Iterate quickly

### Quick Wins
- Focus on high-impact components
- Show immediate value
- Build momentum
- Share success stories

## 2. Provide Support

### Training
- Workshops
- Documentation
- Tutorials
- Office hours

### Tools
- Storybook
- Figma plugins
- Code generators
- Templates

### Support
- Slack channel
- Office hours
- One-on-one help
- Design reviews

## 3. Incentivize Adoption

### Recognition
- Showcase projects
- Feature adopters
- Share success stories
- Reward contributions

### Benefits
- Faster development
- Consistent designs
- Better quality
- Less maintenance

## 4. Measure Success

### Metrics
- Adoption rate
- Component usage
- Time saved
- Quality improved

### Feedback
- User surveys
- Interviews
- Analytics
- Support tickets

## 5. Iterate and Improve

### Continuous Improvement
- Gather feedback
- Analyze metrics
- Make improvements
- Communicate changes

### Community Building
- Foster collaboration
- Share knowledge
- Celebrate successes
- Build relationships
```

---

## 11. Examples

### Real-World Design Systems

```markdown
# Examples

## 1. Material Design

### Overview
- Google's design system
- Comprehensive components
- Extensive documentation
- Multiple platforms

### Key Features
- Material components
- Design tokens
- Guidelines
- Resources

### Website
https://material.io

## 2. Carbon Design System

### Overview
- IBM's design system
- Enterprise-focused
- Comprehensive components
- Accessibility-first

### Key Features
- Carbon components
- Design tokens
- Guidelines
- Resources

### Website
https://carbondesignsystem.com

## 3. Ant Design

### Overview
- Enterprise UI design language
- React components
- Comprehensive library
- Chinese origins

### Key Features
- Ant components
- Design tokens
- Guidelines
- Resources

### Website
https://ant.design

## 4. Tailwind CSS

### Overview
- Utility-first CSS framework
- Design tokens as classes
- Highly customizable
- Popular in React ecosystem

### Key Features
- Utility classes
- Design tokens
- Plugins
- Resources

### Website
https://tailwindcss.com

## 5. Chakra UI

### Overview
- React component library
- Accessible components
- Design tokens
- Simple API

### Key Features
- Chakra components
- Design tokens
- Guidelines
- Resources

### Website
https://chakra-ui.com
```

---

## 12. Best Practices

### Design System Best Practices

```markdown
# Best Practices

## 1. Start with Principles
- Define your principles
- Make them actionable
- Reference them often
- Keep them visible

## 2. Build for Accessibility
- Follow WCAG guidelines
- Test with screen readers
- Support keyboard navigation
- Ensure color contrast

## 3. Make It Modular
- Use atomic design
- Build reusable components
- Keep components focused
- Enable composition

## 4. Document Everything
- Provide examples
- Explain usage
- Include best practices
- Keep docs updated

## 5. Test Thoroughly
- Unit tests
- Integration tests
- Visual tests
- Accessibility tests

## 6. Version Carefully
- Use semantic versioning
- Provide migration guides
- Communicate changes
- Support multiple versions

## 7. Foster Community
- Encourage contributions
- Provide support
- Share knowledge
- Celebrate successes

## 8. Iterate Continuously
- Gather feedback
- Analyze metrics
- Make improvements
- Communicate changes

## 9. Keep It Simple
- Don't over-engineer
- Focus on value
- Ship early, ship often
- Learn and adapt

## 10. Measure Success
- Track adoption
- Gather feedback
- Analyze metrics
- Improve continuously
```

---

## Quick Reference

### Component Quick Reference

```markdown
# Quick Reference

## Common Components

### Button
```tsx
<Button variant="primary" size="md">
  Click me
</Button>
```

### Input
```tsx
<Input
  label="Email"
  placeholder="Enter email"
  value={email}
  onChange={setEmail}
/>
```

### Card
```tsx
<Card
  title="Card Title"
  image="/image.jpg"
  description="Card description"
  actions={<Button>Action</Button>}
/>
```

### Modal
```tsx
<Modal isOpen={isOpen} onClose={() => setIsOpen(false)}>
  <h2>Modal Title</h2>
  <p>Modal content</p>
</Modal>
```

## Design Tokens

### Colors
- `colors.primary[500]`
- `colors.gray[900]`
- `colors.error`

### Typography
- `typography.fontSize.lg`
- `typography.fontWeight.semibold`
- `typography.lineHeight.normal`

### Spacing
- `spacing[4]` (16px)
- `spacing[8]` (32px)
- `spacing[12]` (48px)
```

---

## Quick Start

### Basic Design System Structure

```typescript
// Design tokens
export const tokens = {
  colors: {
    primary: {
      50: '#f0f9ff',
      500: '#3b82f6',
      900: '#1e3a8a'
    },
    gray: {
      50: '#f9fafb',
      500: '#6b7280',
      900: '#111827'
    }
  },
  spacing: {
    1: '4px',
    2: '8px',
    4: '16px',
    8: '32px'
  },
  typography: {
    fontFamily: {
      sans: ['Inter', 'sans-serif'],
      mono: ['Fira Code', 'monospace']
    },
    fontSize: {
      sm: '14px',
      base: '16px',
      lg: '18px',
      xl: '24px'
    }
  }
}

// Component example
export const Button = ({ variant = 'primary', children, ...props }) => {
  return (
    <button
      className={`btn btn-${variant}`}
      style={{
        backgroundColor: tokens.colors.primary[500],
        padding: tokens.spacing[4],
        fontSize: tokens.typography.fontSize.base
      }}
      {...props}
    >
      {children}
    </button>
  )
}
```

### Component Library Setup

```bash
# Create design system package
mkdir design-system
cd design-system

# Initialize
npm init -y
npm install react react-dom
npm install --save-dev @types/react typescript

# Structure
src/
  components/
    Button/
    Input/
    Card/
  tokens/
    colors.ts
    spacing.ts
    typography.ts
  index.ts
```

---

## Production Checklist

- [ ] **Design Tokens**: Define colors, spacing, typography, shadows
- [ ] **Component Library**: Build reusable UI components
- [ ] **Documentation**: Document component usage and props
- [ ] **Storybook**: Set up Storybook for component showcase
- [ ] **Versioning**: Version design system releases
- [ ] **Distribution**: Publish as npm package or internal package
- [ ] **Usage Guidelines**: Provide clear usage guidelines
- [ ] **Accessibility**: Ensure components meet accessibility standards
- [ ] **Testing**: Test components across browsers and devices
- [ ] **Design-Dev Sync**: Maintain sync between design and code
- [ ] **Migration Guide**: Provide migration guides for updates
- [ ] **Feedback Loop**: Collect and incorporate user feedback

---

## Anti-patterns

### ❌ Don't: Inconsistent Tokens

```typescript
// ❌ Bad - Hardcoded values
<button style={{ backgroundColor: '#3b82f6', padding: '16px' }}>
```

```typescript
// ✅ Good - Use design tokens
<button style={{
  backgroundColor: tokens.colors.primary[500],
  padding: tokens.spacing[4]
}}>
```

### ❌ Don't: No Documentation

```typescript
// ❌ Bad - No usage docs
export const Button = ({ variant, children }) => {
  // ...
}
```

```typescript
// ✅ Good - Documented component
/**
 * Button component for user actions
 * 
 * @param variant - Button style variant ('primary' | 'secondary' | 'danger')
 * @param size - Button size ('sm' | 'md' | 'lg')
 * @param children - Button content
 */
export const Button = ({ variant = 'primary', size = 'md', children }) => {
  // ...
}
```

### ❌ Don't: Breaking Changes Without Migration

```typescript
// ❌ Bad - Breaking change without notice
// v2.0.0 - Changed prop name from 'type' to 'variant'
export const Button = ({ variant }) => {
  // Old code breaks!
}
```

```typescript
// ✅ Good - Backward compatible or migration guide
// v2.0.0 - Support both 'type' and 'variant' for migration period
export const Button = ({ type, variant = type, ...props }) => {
  // Supports both
}
```

---

## Integration Points

- **Accessibility** (`22-ux-ui-design/accessibility/`) - Accessible components
- **React Best Practices** (`02-frontend/react-best-practices/`) - Component patterns
- **TypeScript Standards** (`01-foundations/typescript-standards/`) - Type safety

---

## Further Reading

- [Design Systems Handbook](https://www.designbetter.co/design-systems-handbook)
- [Storybook](https://storybook.js.org/)
- [Material Design](https://material.io/design)
- [Ant Design](https://ant.design/)

### Shadows
- `shadows.sm`
- `shadows.md`
- `shadows.lg`
```
