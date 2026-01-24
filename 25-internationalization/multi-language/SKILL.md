---
name: Multi-language Support
description: Supporting multiple languages in applications through language detection, language switching, content translation, and locale-aware formatting for global user bases.
---

# Multi-language Support

> **Current Level:** Intermediate  
> **Domain:** Internationalization / Frontend

---

## Overview

Multi-language support enables applications to serve content in multiple languages, allowing users to choose their preferred language and providing localized experiences. Effective multi-language support includes language detection, switching, content management, and locale-aware formatting.

## What is Multi-language Support

Multi-language support allows applications to display content in multiple languages based on user preferences. This includes language detection, language switching UI, content translation, and proper locale handling for dates, numbers, and currency.

### Core Concepts

```
User Request → Language Detection → Load Translations → Render in Language
     ↓
Language Preference (Browser/User Setting)
     ↓
Translation Files (en.json, th.json, etc.)
     ↓
Localized Content
```

### Language Detection Strategies

| Strategy | Description | Use Case |
|----------|-------------|----------|
| **Browser Language** | Detect from Accept-Language header | Default for new users |
| **User Preference** | Stored user preference | Returning users |
| **URL Parameter** | Language in URL (e.g., /en/, /th/) | SEO-friendly |
| **Geolocation** | Based on user location | Regional defaults |

---

## Core Concepts

### Language Detection

```typescript
// Detect language from browser
function detectLanguage(): string {
  // From browser
  const browserLang = navigator.language.split('-')[0]
  
  // From stored preference
  const storedLang = localStorage.getItem('language')
  
  // From URL
  const urlLang = window.location.pathname.split('/')[1]
  
  return urlLang || storedLang || browserLang || 'en'
}
```

### Translation Management

```typescript
// Translation files
// locales/en.json
{
  "welcome": "Welcome",
  "goodbye": "Goodbye",
  "greeting": "Hello, {{name}}!"
}

// locales/th.json
{
  "welcome": "ยินดีต้อนรับ",
  "goodbye": "ลาก่อน",
  "greeting": "สวัสดี, {{name}}!"
}

// Translation function
function t(key: string, params?: Record<string, string>): string {
  const lang = getCurrentLanguage()
  const translations = loadTranslations(lang)
  let text = translations[key] || key
  
  // Replace parameters
  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      text = text.replace(`{{${key}}}`, value)
    })
  }
  
  return text
}
```

---

## Quick Start

### React i18next

```bash
npm install i18next react-i18next i18next-browser-languagedetector
```

```typescript
// i18n.ts
import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'
import LanguageDetector from 'i18next-browser-languagedetector'

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources: {
      en: {
        translation: {
          welcome: 'Welcome',
          goodbye: 'Goodbye'
        }
      },
      th: {
        translation: {
          welcome: 'ยินดีต้อนรับ',
          goodbye: 'ลาก่อน'
        }
      }
    },
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false
    }
  })
```

### Usage

```tsx
import { useTranslation } from 'react-i18next'

function App() {
  const { t, i18n } = useTranslation()
  
  return (
    <div>
      <h1>{t('welcome')}</h1>
      <button onClick={() => i18n.changeLanguage('th')}>
        Switch to Thai
      </button>
    </div>
  )
}
```

---

## Production Checklist

- [ ] **Language Detection**: Auto-detect user language
- [ ] **Language Switching**: UI for language selection
- [ ] **Translation Files**: Organized translation files
- [ ] **Translation Keys**: Descriptive, hierarchical keys
- [ ] **Pluralization**: Handle plural forms
- [ ] **Variables**: Support variables in translations
- [ ] **Date/Time**: Format dates per locale
- [ ] **Numbers**: Format numbers per locale
- [ ] **Currency**: Format currency per locale
- [ ] **RTL Support**: Support RTL languages
- [ ] **Testing**: Test all languages
- [ ] **Fallback**: Fallback language configured

---

## Anti-patterns

### ❌ Don't: Hardcoded Strings

```tsx
// ❌ Bad - Hardcoded
<h1>Welcome</h1>
<p>Hello, user!</p>
```

```tsx
// ✅ Good - Translation keys
<h1>{t('welcome')}</h1>
<p>{t('greeting', { name: user.name })}</p>
```

### ❌ Don't: No Fallback

```typescript
// ❌ Bad - No fallback
const text = translations[key]
// Undefined if key missing!
```

```typescript
// ✅ Good - Fallback
const text = translations[key] || key || fallbackLng[key]
// Always returns something
```

---

## Integration Points

- **i18n Setup** (`25-internationalization/i18n-setup/`) - i18n configuration
- **Localization** (`25-internationalization/localization/`) - Content translation
- **Currency & Timezone** (`25-internationalization/currency-timezone/`) - Locale formatting

---

## Further Reading

- [i18next Documentation](https://www.i18next.com/)
- [React Intl](https://formatjs.io/docs/react-intl/)
- [Multi-language Best Practices](https://www.w3.org/International/techniques/developing-specs)
