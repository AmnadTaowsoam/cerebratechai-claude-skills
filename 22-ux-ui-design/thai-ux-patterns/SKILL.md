# Thai UI/UX Patterns

## Overview

UI/UX best practices and design patterns specifically tailored for Thai users, including typography, color symbolism, layout preferences, cultural considerations, and accessibility guidelines for Thai language interfaces.

---

## 1. Thai Typography

### Font Selection

```markdown
# Thai Font Guidelines

## Recommended Thai Fonts

### Web-Safe Fonts
1. **Sarabun** - Modern, clean, highly readable
2. **Prompt** - Contemporary, professional
3. **Kanit** - Bold, distinctive
4. **Mitr** - Friendly, approachable
5. **Bai Jamjuree** - Elegant, traditional

### Google Fonts (Free)
- Sarabun (most popular for web)
- Prompt
- Kanit
- Mitr
- Bai Jamjuree
- Chakra Petch
- K2D
- Maitree

### Premium Fonts
- DB Helvethaica X
- Sukhumvit Set
- Thonburi
- Ayuthaya

## Font Pairing

### Thai + English Combinations
- Sarabun (Thai) + Inter (English)
- Prompt (Thai) + Roboto (English)
- Kanit (Thai) + Montserrat (English)
- Mitr (Thai) + Open Sans (English)
```

### Typography Implementation

```css
/* Thai Typography CSS */

/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

:root {
  /* Font Families */
  --font-thai: 'Sarabun', sans-serif;
  --font-english: 'Inter', sans-serif;
  --font-combined: 'Sarabun', 'Inter', sans-serif;
  
  /* Font Sizes - Thai text needs slightly larger size */
  --text-xs: 0.75rem;    /* 12px */
  --text-sm: 0.875rem;   /* 14px */
  --text-base: 1rem;     /* 16px */
  --text-lg: 1.125rem;   /* 18px */
  --text-xl: 1.25rem;    /* 20px */
  --text-2xl: 1.5rem;    /* 24px */
  --text-3xl: 1.875rem;  /* 30px */
  --text-4xl: 2.25rem;   /* 36px */
  
  /* Line Heights - Thai needs more space */
  --leading-tight: 1.4;
  --leading-normal: 1.6;
  --leading-relaxed: 1.8;
  
  /* Letter Spacing */
  --tracking-tight: -0.01em;
  --tracking-normal: 0;
  --tracking-wide: 0.02em;
}

body {
  font-family: var(--font-combined);
  font-size: var(--text-base);
  line-height: var(--leading-normal);
  letter-spacing: var(--tracking-normal);
}

/* Thai-specific adjustments */
:lang(th) {
  font-family: var(--font-thai);
  line-height: var(--leading-relaxed);
}

/* Headings */
h1 {
  font-size: var(--text-4xl);
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 1rem;
}

h2 {
  font-size: var(--text-3xl);
  font-weight: 600;
  line-height: 1.3;
  margin-bottom: 0.875rem;
}

h3 {
  font-size: var(--text-2xl);
  font-weight: 600;
  line-height: 1.4;
  margin-bottom: 0.75rem;
}

/* Body text */
p {
  margin-bottom: 1rem;
  line-height: var(--leading-relaxed);
}

/* Small text */
small {
  font-size: var(--text-sm);
  line-height: var(--leading-normal);
}

/* Responsive Typography */
@media (max-width: 768px) {
  :root {
    --text-base: 0.9375rem; /* 15px - slightly smaller on mobile */
    --text-lg: 1.0625rem;   /* 17px */
    --text-xl: 1.1875rem;   /* 19px */
    --text-2xl: 1.375rem;   /* 22px */
    --text-3xl: 1.75rem;    /* 28px */
    --text-4xl: 2rem;       /* 32px */
  }
}
```

### Typography Component

```typescript
// Typography Component with Thai Support
import { ReactNode } from 'react'

interface TypographyProps {
  variant?: 'h1' | 'h2' | 'h3' | 'h4' | 'body' | 'small' | 'caption'
  children: ReactNode
  className?: string
  lang?: 'th' | 'en'
}

export default function Typography({
  variant = 'body',
  children,
  className = '',
  lang = 'th',
}: TypographyProps) {
  const baseClasses = `font-thai ${lang === 'th' ? 'leading-relaxed' : 'leading-normal'}`

  const variantClasses = {
    h1: 'text-4xl font-bold mb-4',
    h2: 'text-3xl font-semibold mb-3',
    h3: 'text-2xl font-semibold mb-2',
    h4: 'text-xl font-medium mb-2',
    body: 'text-base',
    small: 'text-sm',
    caption: 'text-xs text-gray-600',
  }

  const Component = variant.startsWith('h') ? variant : 'p'

  return (
    <Component
      className={`${baseClasses} ${variantClasses[variant]} ${className}`}
      lang={lang}
    >
      {children}
    </Component>
  )
}
```

---

## 2. Color Symbolism in Thai Culture

### Thai Color Meanings

```typescript
// Thai Color Palette with Cultural Meanings
interface ThaiColor {
  name: string
  hex: string
  meaning: string
  usage: string[]
  dayOfWeek?: string
}

const thaiColors: ThaiColor[] = [
  {
    name: 'Yellow (เหลือง)',
    hex: '#FFD700',
    meaning: 'Royal color, Monday, prosperity, wisdom',
    usage: ['Royal events', 'Monday promotions', 'Auspicious occasions'],
    dayOfWeek: 'Monday',
  },
  {
    name: 'Pink (ชมพู)',
    hex: '#FF69B4',
    meaning: 'Tuesday, love, harmony, King Rama IX',
    usage: ['Tuesday events', 'Romantic occasions', 'Royal tributes'],
    dayOfWeek: 'Tuesday',
  },
  {
    name: 'Green (เขียว)',
    hex: '#228B22',
    meaning: 'Wednesday (day), nature, growth, fertility',
    usage: ['Wednesday morning events', 'Environmental themes', 'Health'],
    dayOfWeek: 'Wednesday (Day)',
  },
  {
    name: 'Gray (เทา)',
    hex: '#808080',
    meaning: 'Wednesday (night), neutrality',
    usage: ['Wednesday evening events', 'Formal occasions'],
    dayOfWeek: 'Wednesday (Night)',
  },
  {
    name: 'Orange (ส้ม)',
    hex: '#FF8C00',
    meaning: 'Thursday, Buddhism, monks, spirituality',
    usage: ['Religious events', 'Thursday promotions', 'Merit-making'],
    dayOfWeek: 'Thursday',
  },
  {
    name: 'Blue (น้ำเงิน)',
    hex: '#4169E1',
    meaning: 'Friday, Queen Sirikit, loyalty, stability',
    usage: ['Friday events', 'Royal occasions', 'Trust-building'],
    dayOfWeek: 'Friday',
  },
  {
    name: 'Purple (ม่วง)',
    hex: '#800080',
    meaning: 'Saturday, mystery, luxury',
    usage: ['Saturday events', 'Premium products', 'Luxury services'],
    dayOfWeek: 'Saturday',
  },
  {
    name: 'Red (แดง)',
    hex: '#DC143C',
    meaning: 'Sunday, power, energy, celebration',
    usage: ['Sunday events', 'Celebrations', 'Important announcements'],
    dayOfWeek: 'Sunday',
  },
  {
    name: 'White (ขาว)',
    hex: '#FFFFFF',
    meaning: 'Purity, cleanliness, mourning (in some contexts)',
    usage: ['Weddings', 'Religious ceremonies', 'Funerals'],
  },
  {
    name: 'Black (ดำ)',
    hex: '#000000',
    meaning: 'Formality, mourning, sophistication',
    usage: ['Formal events', 'Funerals', 'Luxury branding'],
  },
]

// Get color by day of week
function getColorForDay(dayOfWeek: string): ThaiColor | undefined {
  return thaiColors.find((color) => color.dayOfWeek === dayOfWeek)
}

// Get auspicious color for today
function getTodayColor(): ThaiColor | undefined {
  const days = [
    'Sunday',
    'Monday',
    'Tuesday',
    'Wednesday (Day)',
    'Thursday',
    'Friday',
    'Saturday',
  ]
  const today = new Date()
  const dayIndex = today.getDay()
  const dayName = days[dayIndex]

  return getColorForDay(dayName)
}
```

### Color Palette Implementation

```css
/* Thai Cultural Color Palette */
:root {
  /* Day Colors */
  --color-sunday: #DC143C;      /* Red */
  --color-monday: #FFD700;      /* Yellow */
  --color-tuesday: #FF69B4;     /* Pink */
  --color-wednesday-day: #228B22; /* Green */
  --color-wednesday-night: #808080; /* Gray */
  --color-thursday: #FF8C00;    /* Orange */
  --color-friday: #4169E1;      /* Blue */
  --color-saturday: #800080;    /* Purple */
  
  /* Cultural Colors */
  --color-royal: #FFD700;       /* Gold/Yellow */
  --color-monk: #FF8C00;        /* Orange */
  --color-auspicious: #DC143C;  /* Red */
  --color-mourning: #000000;    /* Black */
  
  /* Modern Thai Palette */
  --color-primary: #FF6B6B;     /* Coral Red */
  --color-secondary: #4ECDC4;   /* Turquoise */
  --color-accent: #FFD93D;      /* Golden Yellow */
  --color-success: #6BCF7F;     /* Green */
  --color-warning: #FFB84D;     /* Orange */
  --color-error: #FF6B6B;       /* Red */
  
  /* Neutral Colors */
  --color-gray-50: #F9FAFB;
  --color-gray-100: #F3F4F6;
  --color-gray-200: #E5E7EB;
  --color-gray-300: #D1D5DB;
  --color-gray-400: #9CA3AF;
  --color-gray-500: #6B7280;
  --color-gray-600: #4B5563;
  --color-gray-700: #374151;
  --color-gray-800: #1F2937;
  --color-gray-900: #111827;
}

/* Day-specific themes */
.theme-sunday { --theme-color: var(--color-sunday); }
.theme-monday { --theme-color: var(--color-monday); }
.theme-tuesday { --theme-color: var(--color-tuesday); }
.theme-wednesday { --theme-color: var(--color-wednesday-day); }
.theme-thursday { --theme-color: var(--color-thursday); }
.theme-friday { --theme-color: var(--color-friday); }
.theme-saturday { --theme-color: var(--color-saturday); }
```

---

## 3. Layout Preferences

### Thai Layout Patterns

```markdown
# Thai Layout Guidelines

## Reading Direction
- **Left to Right**: Thai text flows left to right
- **Top to Bottom**: Vertical hierarchy is important
- **Visual Hierarchy**: Clear distinction between levels

## Spacing
- **Generous Whitespace**: Thai text needs more breathing room
- **Line Height**: Minimum 1.6, recommended 1.8
- **Paragraph Spacing**: 1.5-2em between paragraphs
- **Section Spacing**: Clear visual breaks between sections

## Grid System
- **12-column grid**: Standard for desktop
- **4-column grid**: Mobile layouts
- **Gutters**: 16-24px for comfortable reading

## Content Density
- **Less Dense**: Thai users prefer less crowded interfaces
- **Clear Sections**: Distinct visual separation
- **Progressive Disclosure**: Show information gradually
```

### Responsive Layout

```css
/* Thai-Optimized Layout */

/* Container */
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

/* Grid System */
.grid {
  display: grid;
  gap: 1.5rem;
}

.grid-cols-1 { grid-template-columns: repeat(1, 1fr); }
.grid-cols-2 { grid-template-columns: repeat(2, 1fr); }
.grid-cols-3 { grid-template-columns: repeat(3, 1fr); }
.grid-cols-4 { grid-template-columns: repeat(4, 1fr); }

/* Responsive Grid */
@media (max-width: 1024px) {
  .grid-cols-4 { grid-template-columns: repeat(2, 1fr); }
  .grid-cols-3 { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 640px) {
  .grid-cols-4,
  .grid-cols-3,
  .grid-cols-2 {
    grid-template-columns: 1fr;
  }
  
  .container {
    padding: 0 1rem;
  }
}

/* Card Layout - Popular in Thai UX */
.card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: box-shadow 0.3s ease;
}

.card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}

/* Section Spacing */
.section {
  padding: 4rem 0;
}

@media (max-width: 768px) {
  .section {
    padding: 2.5rem 0;
  }
}

/* Thai-style spacing */
.space-y-thai > * + * {
  margin-top: 1.5rem;
}

.space-y-thai-lg > * + * {
  margin-top: 2.5rem;
}
```

---

## 4. Mobile-First Design for Thai Users

### Mobile Optimization

```typescript
// Mobile-First Component
'use client'

import { useState, useEffect } from 'react'

export function useIsMobile() {
  const [isMobile, setIsMobile] = useState(false)

  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768)
    }

    checkMobile()
    window.addEventListener('resize', checkMobile)

    return () => window.removeEventListener('resize', checkMobile)
  }, [])

  return isMobile
}

// Mobile-Optimized Navigation
export default function MobileNav() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <nav className="mobile-nav">
      {/* Hamburger Menu */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="hamburger"
        aria-label="เมนู"
      >
        <span></span>
        <span></span>
        <span></span>
      </button>

      {/* Mobile Menu */}
      {isOpen && (
        <div className="mobile-menu">
          <a href="/" className="menu-item">
            หน้าแรก
          </a>
          <a href="/events" className="menu-item">
            อีเวนต์
          </a>
          <a href="/vendors" className="menu-item">
            ผู้ให้บริการ
          </a>
          <a href="/about" className="menu-item">
            เกี่ยวกับเรา
          </a>
        </div>
      )}
    </nav>
  )
}
```

### Touch-Friendly Design

```css
/* Touch-Friendly UI */

/* Minimum touch target size: 44x44px (iOS) or 48x48px (Android) */
.btn,
.link,
.input,
.checkbox {
  min-height: 48px;
  min-width: 48px;
}

/* Larger tap targets for primary actions */
.btn-primary {
  min-height: 56px;
  padding: 0 2rem;
  font-size: 1.125rem;
}

/* Spacing between interactive elements */
.btn + .btn {
  margin-left: 12px;
}

/* Mobile-optimized forms */
.form-field {
  margin-bottom: 1.5rem;
}

.form-input {
  width: 100%;
  min-height: 48px;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  border: 2px solid var(--color-gray-300);
  border-radius: 8px;
}

.form-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(255, 107, 107, 0.1);
}

/* Mobile-friendly checkboxes and radios */
.checkbox,
.radio {
  width: 24px;
  height: 24px;
  margin-right: 12px;
}

/* Bottom navigation (popular in Thai apps) */
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 64px;
  background: white;
  border-top: 1px solid var(--color-gray-200);
  display: flex;
  justify-content: space-around;
  align-items: center;
  z-index: 1000;
}

.bottom-nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px 12px;
  min-width: 64px;
  color: var(--color-gray-600);
  text-decoration: none;
  font-size: 0.75rem;
}

.bottom-nav-item.active {
  color: var(--color-primary);
}

.bottom-nav-icon {
  width: 24px;
  height: 24px;
  margin-bottom: 4px;
}
```

---

## 5. Thai Language Accessibility

### Text Input Optimization

```typescript
// Thai Input Component
'use client'

import { useState } from 'react'

interface ThaiInputProps {
  label: string
  placeholder?: string
  value: string
  onChange: (value: string) => void
  maxLength?: number
  showCharCount?: boolean
}

export default function ThaiInput({
  label,
  placeholder,
  value,
  onChange,
  maxLength,
  showCharCount = false,
}: ThaiInputProps) {
  const [isFocused, setIsFocused] = useState(false)

  // Thai character count (including tone marks and vowels)
  const getThaiCharCount = (text: string): number => {
    // Remove combining characters for accurate count
    return text.normalize('NFC').length
  }

  const charCount = getThaiCharCount(value)

  return (
    <div className="thai-input-wrapper">
      <label className="input-label">{label}</label>
      
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onFocus={() => setIsFocused(true)}
        onBlur={() => setIsFocused(false)}
        placeholder={placeholder}
        maxLength={maxLength}
        lang="th"
        className={`thai-input ${isFocused ? 'focused' : ''}`}
      />

      {showCharCount && maxLength && (
        <div className="char-count">
          {charCount} / {maxLength}
        </div>
      )}
    </div>
  )
}
```

### Screen Reader Support

```typescript
// Accessible Thai Component
interface AccessibleTextProps {
  children: string
  ariaLabel?: string
  role?: string
}

export function AccessibleText({
  children,
  ariaLabel,
  role,
}: AccessibleTextProps) {
  return (
    <span
      lang="th"
      aria-label={ariaLabel || children}
      role={role}
    >
      {children}
    </span>
  )
}

// Usage
<AccessibleText ariaLabel="ยินดีต้อนรับสู่ Malai Platform">
  ยินดีต้อนรับ
</AccessibleText>
```

---

## 6. Cultural Considerations

### Date and Time Formatting

```typescript
// Thai Date Formatter
class ThaiDateFormatter {
  private static thaiMonths = [
    'มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน',
    'พฤษภาคม', 'มิถุนายน', 'กรกฎาคม', 'สิงหาคม',
    'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม',
  ]

  private static thaiDays = [
    'อาทิตย์', 'จันทร์', 'อังคาร', 'พุธ',
    'พฤหัสบดี', 'ศุกร์', 'เสาร์',
  ]

  static formatDate(date: Date, format: 'short' | 'long' | 'full' = 'long'): string {
    const day = date.getDate()
    const month = date.getMonth()
    const year = date.getFullYear() + 543 // Buddhist Era
    const dayOfWeek = date.getDay()

    switch (format) {
      case 'short':
        return `${day}/${month + 1}/${year}`
      
      case 'long':
        return `${day} ${this.thaiMonths[month]} ${year}`
      
      case 'full':
        return `วัน${this.thaiDays[dayOfWeek]}ที่ ${day} ${this.thaiMonths[month]} พ.ศ. ${year}`
      
      default:
        return date.toLocaleDateString('th-TH')
    }
  }

  static formatTime(date: Date, use24Hour: boolean = true): string {
    const hours = date.getHours()
    const minutes = date.getMinutes()

    if (use24Hour) {
      return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')} น.`
    } else {
      const period = hours >= 12 ? 'PM' : 'AM'
      const hours12 = hours % 12 || 12
      return `${hours12}:${minutes.toString().padStart(2, '0')} ${period}`
    }
  }

  static formatDateTime(date: Date): string {
    return `${this.formatDate(date, 'long')} เวลา ${this.formatTime(date)}`
  }
}

// Usage
const now = new Date()
console.log(ThaiDateFormatter.formatDate(now, 'full'))
// Output: "วันเสาร์ที่ 18 มกราคม พ.ศ. 2569"
```

### Number Formatting

```typescript
// Thai Number Formatter
class ThaiNumberFormatter {
  static formatCurrency(amount: number, showSymbol: boolean = true): string {
    const formatted = new Intl.NumberFormat('th-TH', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(amount)

    return showSymbol ? `${formatted} บาท` : formatted
  }

  static formatNumber(num: number): string {
    return new Intl.NumberFormat('th-TH').format(num)
  }

  static formatPercent(value: number): string {
    return `${value.toFixed(1)}%`
  }
}

// Usage
console.log(ThaiNumberFormatter.formatCurrency(1500.50))
// Output: "1,500.50 บาท"

console.log(ThaiNumberFormatter.formatNumber(1000000))
// Output: "1,000,000"
```

---

## 7. Design Patterns

### Thai Card Design

```typescript
// Thai-Style Event Card
interface EventCardProps {
  title: string
  date: Date
  location: string
  price: number
  imageUrl: string
  category: string
}

export default function ThaiEventCard({
  title,
  date,
  location,
  price,
  imageUrl,
  category,
}: EventCardProps) {
  return (
    <div className="thai-event-card">
      <div className="card-image">
        <img src={imageUrl} alt={title} />
        <div className="card-badge">{category}</div>
      </div>

      <div className="card-content">
        <h3 className="card-title">{title}</h3>

        <div className="card-info">
          <div className="info-item">
            <span className="icon">📅</span>
            <span>{ThaiDateFormatter.formatDate(date, 'long')}</span>
          </div>

          <div className="info-item">
            <span className="icon">📍</span>
            <span>{location}</span>
          </div>

          <div className="info-item">
            <span className="icon">💰</span>
            <span className="price">
              {ThaiNumberFormatter.formatCurrency(price)}
            </span>
          </div>
        </div>

        <button className="btn-primary">
          ดูรายละเอียด
        </button>
      </div>
    </div>
  )
}
```

### Thai Form Design

```css
/* Thai-Optimized Form Styles */
.thai-form {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.form-header {
  text-align: center;
  margin-bottom: 2rem;
}

.form-title {
  font-size: 1.875rem;
  font-weight: 700;
  color: var(--color-gray-900);
  margin-bottom: 0.5rem;
}

.form-subtitle {
  font-size: 1rem;
  color: var(--color-gray-600);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  font-size: 1rem;
  font-weight: 500;
  color: var(--color-gray-700);
  margin-bottom: 0.5rem;
}

.form-label-required::after {
  content: ' *';
  color: var(--color-error);
}

.form-input {
  width: 100%;
  padding: 0.875rem 1rem;
  font-size: 1rem;
  font-family: var(--font-thai);
  border: 2px solid var(--color-gray-300);
  border-radius: 8px;
  transition: all 0.2s ease;
}

.form-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 4px rgba(255, 107, 107, 0.1);
}

.form-input.error {
  border-color: var(--color-error);
}

.form-error {
  display: block;
  margin-top: 0.5rem;
  font-size: 0.875rem;
  color: var(--color-error);
}

.form-help {
  display: block;
  margin-top: 0.5rem;
  font-size: 0.875rem;
  color: var(--color-gray-600);
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.btn-submit {
  flex: 1;
  padding: 1rem 2rem;
  font-size: 1.125rem;
  font-weight: 600;
  color: white;
  background: var(--color-primary);
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-submit:hover {
  background: #FF5252;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 107, 107, 0.3);
}

.btn-submit:active {
  transform: translateY(0);
}
```

---

## Best Practices

1. **Typography**
   - Use Thai-optimized fonts (Sarabun, Prompt)
   - Increase line height (1.6-1.8)
   - Larger font sizes for readability
   - Proper font pairing for Thai+English

2. **Colors**
   - Respect cultural color meanings
   - Use day-of-week colors appropriately
   - Avoid white for celebrations (mourning color)
   - Consider royal colors for formal events

3. **Layout**
   - Generous whitespace
   - Clear visual hierarchy
   - Mobile-first approach
   - Touch-friendly targets (48px minimum)

4. **Language**
   - Buddhist Era (พ.ศ.) for dates
   - Thai number formatting
   - Proper tone mark handling
   - Screen reader support

5. **Cultural Sensitivity**
   - Respect religious symbols
   - Appropriate imagery
   - Formal vs. informal language
   - Regional considerations

---

## Common Pitfalls

1. **Font Issues**: Using non-Thai fonts causing readability problems
2. **Color Misuse**: Using mourning colors for celebrations
3. **Date Format**: Forgetting to convert to Buddhist Era
4. **Touch Targets**: Too small for mobile users
5. **Text Overflow**: Not accounting for longer Thai text

---

## Production Checklist

- [ ] Thai fonts loaded and applied
- [ ] Line heights optimized for Thai
- [ ] Colors culturally appropriate
- [ ] Dates in Buddhist Era format
- [ ] Numbers formatted Thai style
- [ ] Touch targets 48px minimum
- [ ] Mobile-responsive layout
- [ ] Screen reader tested
- [ ] RTL not applied (Thai is LTR)
- [ ] Cultural review completed

---

## Tools & Libraries

| Tool | Purpose |
|------|---------|
| Google Fonts | Thai web fonts |
| Intl API | Number/date formatting |
| date-fns | Date manipulation |
| react-i18next | Internationalization |

---

## Further Reading

- [Thai Typography Guidelines](https://www.f0nt.com/thai-typography/)
- [Thai Color Symbolism](https://www.tourismthailand.org/Articles/thai-colors)
- [Thai Web Design Trends](https://www.designil.com/thai-web-design)
- [Accessibility in Thai](https://www.w3.org/WAI/translations/th/)
