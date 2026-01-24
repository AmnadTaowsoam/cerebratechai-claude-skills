---
name: Localization (l10n)
description: Adapting internationalized applications to specific languages and regions, going beyond translation to include cultural, regional, and technical adaptations.
---

# Localization (l10n)

> **Current Level:** Intermediate  
> **Domain:** Internationalization / UX

---

## Overview

Localization (l10n) is the process of adapting an internationalized application to specific languages and regions. It goes beyond translation to include cultural, regional, and technical adaptations like date formats, currency, timezones, and cultural preferences.

### l10n vs i18n

| Aspect | i18n | l10n |
|--------|-------|-------|
| **Focus** | Making app translatable | Adapting to specific locale |
| **When** | During development | After i18n is complete |
| **Who** | Developers | Translators |
| **Output** | Code with translation keys | Localized content |

### Beyond Translation

| Aspect | Description |
|--------|-------------|
| **Language** | Translate text content |

---

## Core Concepts
| **Cultural** | Adapt to cultural norms |
| **Regional** | Adapt to regional preferences |
| **Technical** | Format dates, numbers, currencies |
| **Visual** | Adapt images, colors, layouts |

## Cultural Considerations

### Colors

| Color | Western Meaning | Eastern Meaning |
|--------|-----------------|-----------------|
| **White** | Purity, peace | Death, mourning (some Asian cultures) |
| **Red** | Danger, love | Good fortune (China) |
| **Green** | Nature, go | Islam (some cultures) |
| **Yellow** | Happiness | Imperial (China) |

### Images and Symbols

| Element | Western | Eastern | Notes |
|---------|---------|---------|-------|
| **Hand gestures** | Thumbs up = good | Thumbs up = offensive (Middle East) |
| **Animals** | Dogs = pets | Dogs = unclean (some cultures) |
| **Food** | Beef = common | Beef = taboo (Hindu, Buddhist) |
| **Clothing** | Casual wear | Modest dress (conservative cultures) |

### Numbers and Numerology

| Culture | Lucky Numbers | Unlucky Numbers |
|----------|----------------|------------------|
| **Chinese** | 8 (wealth), 9 (longevity) | 4 (death) |
| **Japanese** | 7 (lucky) | 4 (death) |
| **Western** | 7 (lucky) | 13 (unlucky) |

### Names and Titles

| Culture | Naming Convention |
|----------|------------------|
| **Western** | First name + Last name |
| **East Asian** | Family name + Given name |
| **Hispanic** | First name + Father's surname + Mother's surname |
| **Arabic** | Personal name + Father's name + Grandfather's name |

## Date and Time Formats

### Date Formats

| Locale | Format | Example |
|--------|--------|---------|
| **en-US** | MM/DD/YYYY | 01/15/2024 |
| **en-GB** | DD/MM/YYYY | 15/01/2024 |
| **th-TH** | DD/MM/YYYY | 15/01/2567 |
| **ja-JP** | YYYY/MM/DD | 2024/01/15 |
| **de-DE** | DD.MM.YYYY | 15.01.2024 |

### Time Formats

| Locale | Format | Example |
|--------|--------|---------|
| **en-US** | 12-hour AM/PM | 2:30 PM |
| **en-GB** | 24-hour | 14:30 |
| **th-TH** | 24-hour | 14:30 |
| **ja-JP** | 12-hour | 午後2:30 |
| **de-DE** | 24-hour | 14:30 |

### Day and Month Names

| Locale | Day Names | Month Names |
|--------|-----------|-------------|
| **en-US** | Monday, Tuesday, ... | January, February, ... |
| **th-TH** | จันทร์, อังคาร, ... | มกราคม, กุมภาพันธุ, ... |
| **ja-JP** | 月曜日, 火曜日, ... | 1月, 2月, ... |
| **de-DE** | Montag, Dienstag, ... | Januar, Februar, ... |

## Number Formats

### Decimal Separators

| Locale | Decimal Separator | Thousands Separator | Example |
|--------|------------------|---------------------|---------|
| **en-US** | . | , | 1,234.56 |
| **de-DE** | , | . | 1,234.56 |
| **th-TH** | . | , | 1,234.56 |
| **ja-JP** | . | , | 1,234.56 |

### Currency Formats

| Locale | Symbol Position | Decimal Places | Example |
|--------|---------------|----------------|---------|
| **en-US** | Prefix | 2 | $1,234.56 |
| **de-DE** | Suffix | 2 | 1,234.56 € |
| **th-TH** | Prefix | 2 | ฿1,234.56 |
| **JPY** | Prefix | 0 | ¥1,235 |

## Currency Display

### Currency Symbols

| Currency | Symbol | Position | Example |
|----------|--------|-----------|---------|
| **USD** | $ | Prefix | $100.00 |
| **EUR** | € | Suffix | 100,00 € |
| **GBP** | £ | Prefix | £100.00 |
| **JPY** | ¥ | Prefix | ¥100 |
| **THB** | ฿ | Prefix | ฿100.00 |

### Currency Formatting

```javascript
function formatCurrency(amount, currency, locale) {
    return new Intl.NumberFormat(locale, {
        style: 'currency',
        currency: currency
    }).format(amount);
}

// Examples
formatCurrency(100, 'USD', 'en-US'); // $100.00
formatCurrency(100, 'EUR', 'de-DE'); // 100,00 €
formatCurrency(100, 'THB', 'th-TH'); // ฿100.00
```

## Address Formats

### Address Components

| Component | US | UK | Japan | Thailand |
|-----------|-----|-----|--------|----------|
| **Line 1** | Name | Name | Postal code | Name |
| **Line 2** | Street | Street | Prefecture | Address |
| **Line 3** | City, State | City, Postcode | Sub-district, District |
| **Line 4** | ZIP Code | Postcode | Country | Province, Postal code |

### Address Examples

```
US:
John Doe
123 Main Street
New York, NY 10001
USA

UK:
John Doe
123 Main Street
London
SW1A 1AA
United Kingdom

Japan:
山田 太郎
〒100-0001
東京都渋谷区
日本

Thailand:
สมชช ใจร์
123 ถนนเจริญ แขวน
แขวงหลัก 10101
กรุงเทพฯ 10100
ประเทศไทย
```

## Phone Number Formats

### International Dialing Codes

| Country | Code | Format | Example |
|---------|------|--------|---------|
| **US** | +1 | (XXX) XXX-XXXX | +1 (555) 123-4567 |
| **UK** | +44 | XXXX XXX XXXX | +44 20 7123 4567 |
| **Japan** | +81 | XX-XXXX-XXXX | +81 3-1234-5678 |
| **Thailand** | +66 | XXX-XXX-XXXX | +66 2-123-4567 |

### Phone Input

```html
<!-- Phone input with country code -->
<div class="phone-input">
    <select name="country_code">
        <option value="+1">+1 (US)</option>
        <option value="+44">+44 (UK)</option>
        <option value="+81">+81 (Japan)</option>
        <option value="+66">+66 (Thailand)</option>
    </select>
    <input type="tel" name="phone_number" placeholder="123-4567" />
</div>
```

## Name Formats

### Name Order

| Culture | Format | Example |
|---------|--------|---------|
| **Western** | First Last | John Doe |
| **East Asian** | Family Given | 山田 太郎 |
| **Hispanic** | First Paternal Maternal | Juan Carlos García Rodríguez |
| **Hungarian** | Family Given | Kovács János |

### Name Input

```html
<!-- Name input with cultural awareness -->
<div class="name-input">
    <label>First Name</label>
    <input type="text" name="first_name" />
    
    <label>Last Name</label>
    <input type="text" name="last_name" />
    
    <label>Family Name (if applicable)</label>
    <input type="text" name="family_name" />
</div>
```

## Measurement Units

### Metric vs Imperial

| Unit | Metric | Imperial |
|------|--------|-----------|
| **Length** | Meters, Kilometers | Feet, Miles |
| **Weight** | Kilograms, Grams | Pounds, Ounces |
| **Temperature** | Celsius | Fahrenheit |
| **Volume** | Liters, Milliliters | Gallons, Quarts |

### Unit Conversion

```javascript
function convertTemperature(celsius, toFahrenheit) {
    return (celsius * 9/5) + 32;
}

function convertLength(kilometers, toMiles) {
    return kilometers * 0.621371;
}

function convertWeight(kilograms, toPounds) {
    return kilograms * 2.20462;
}

// Usage
const tempC = 25;
const tempF = convertTemperature(tempC, true); // 77°F
```

### Unit Display

```javascript
function formatMeasurement(value, unit, locale, system) {
    if (system === 'metric') {
        return `${value} ${unit}`;
    } else {
        // Convert to imperial
        const converted = convertToImperial(value, unit);
        return `${converted} ${imperialUnit}`;
    }
}

// Usage
formatMeasurement(100, 'kg', 'en-US', 'imperial'); // 220.46 lbs
```

## Legal and Compliance

### Privacy Laws

| Regulation | Region | Key Requirements |
|------------|--------|------------------|
| **GDPR** | EU | Consent, data portability, right to be forgotten |
| **CCPA** | California | Opt-out of sale, disclosure, deletion |
| **PDPA** | Thailand | Consent, data access, security |

### Cookie Consent

```html
<!-- GDPR-compliant cookie banner -->
<div class="cookie-banner">
    <p>We use cookies to improve your experience.</p>
    <button onclick="acceptCookies()">Accept</button>
    <button onclick="rejectCookies()">Reject</button>
    <a href="/privacy-policy">Privacy Policy</a>
</div>
```

### Terms of Service

```html
<!-- Localized terms of service -->
<div class="terms">
    <h1>Terms of Service</h1>
    <p>Last updated: {last_updated_date}</p>
    <h2>1. Acceptance</h2>
    <p>{terms_acceptance_text}</p>
    <h2>2. User Accounts</h2>
    <p>{user_accounts_text}</p>
    <h2>3. Privacy Policy</h2>
    <p>{privacy_policy_text}</p>
</div>
```

## Payment Methods

### Regional Preferences

| Region | Popular Payment Methods |
|---------|----------------------|
| **US** | Credit cards, PayPal, Apple Pay |
| **Europe** | Credit cards, PayPal, SEPA, iDEAL |
| **Asia** | Credit cards, Alipay, WeChat Pay |
| **Thailand** | Credit cards, PromptPay, TrueMoney |

### Payment Icons

```html
<!-- Localized payment methods -->
<div class="payment-methods">
    <div class="method">
        <img src="/images/visa.png" alt="Visa" />
        <img src="/images/mastercard.png" alt="Mastercard" />
    </div>
    <div class="method">
        <img src="/images/paypal.png" alt="PayPal" />
    </div>
    <div class="method thailand-only">
        <img src="/images/promptpay.png" alt="PromptPay" />
    </div>
</div>
```

## Holidays and Business Hours

### Regional Holidays

| Country | Major Holidays |
|---------|----------------|
| **US** | New Year, Independence Day, Thanksgiving, Christmas |
| **UK** | New Year, Easter, Christmas |
| **Japan** | New Year, Golden Week, Obon |
| **Thailand** | New Year, Songkran, Chakri Memorial Day, Visakha Puja, Coronation Day |

### Business Hours

| Country | Typical Hours |
|---------|---------------|
| **US** | 9 AM - 5 PM, Mon-Fri |
| **Europe** | 9 AM - 5 PM, Mon-Fri |
| **Japan** | 9 AM - 5 PM, Mon-Fri |
| **Thailand** | 9 AM - 5 PM, Mon-Fri |

### Holiday Display

```javascript
function getHolidays(country) {
    const holidays = {
        'US': [
            '2024-01-01', // New Year's Day
            '2024-07-04', // Independence Day
            '2024-11-28', // Thanksgiving
            '2024-12-25'  // Christmas Day
        ],
        'TH': [
            '2024-01-01', // New Year's Day
            '2024-04-13', // Songkran Festival
            '2024-05-06', // Coronation Day
            '2024-05-20', // Visakha Puja
            '2024-07-28', // H.M. The King's Birthday
            '2024-10-23', // Chulalongkorn Day
        ]
    };
    
    return holidays[country] || [];
}

function isBusinessDay(date, country) {
    const holidays = getHolidays(country);
    const dayOfWeek = date.getDay();
    const isWeekend = dayOfWeek === 0 || dayOfWeek === 6;
    const isHoliday = holidays.includes(date.toISOString().split('T')[0]);
    
    return !isWeekend && !isHoliday;
}
```

## Locale-Specific Content

### Cultural Adaptations

| Element | US | Japan | Thailand |
|---------|-----|--------|----------|
| **Colors** | Red = danger | Red = good fortune | Red = good fortune |
| **Images** | Handshakes | Bowing | Wai |
| **Layout** | Left-to-right | Top-to-bottom | Left-to-right |
| **Text** | Direct address | Formal address | Formal address |

### Content Examples

```html
<!-- US version -->
<div class="content">
    <h1>Welcome!</h1>
    <p>Sign up for our newsletter to get 10% off.</p>
    <button>Sign Up</button>
</div>

<!-- Japan version -->
<div class="content">
    <h1>ようこそ！</h1>
    <p>ニュースレターにご登録いただくと10%の割引がございます。</p>
    <button>登録</button>
</div>

<!-- Thailand version -->
<div class="content">
    <h1>ยินดีต้อนรับ!</h1>
    <p>สมัครในรับรับจดหนัสเพื่อรับส่วนลด 10%</p>
    <button>ลงทะเบียน</button>
</div>
```

## Testing Localization

### Test Checklist

| Category | Items |
|----------|-------|
| **Language** | All text translated |
| **Dates** | Format correct for locale |
| **Numbers** | Format correct for locale |
| **Currency** | Symbol and format correct |
| **Layout** | Works for RTL/LTR |
| **Images** | Culturally appropriate |
| **Forms** | Input order correct |
| **Holidays** | Holiday dates correct |

### Visual Testing

```bash
# Take screenshots in different locales
npm run test:visual --locale=en-US
npm run test:visual --locale=ja-JP
npm run test:visual --locale=th-TH
```

### Automated Testing

```javascript
describe('Localization', () => {
    const locales = ['en-US', 'ja-JP', 'th-TH'];
    
    locales.forEach(locale => {
        describe(`Locale: ${locale}`, () => {
            test('Date formatting', () => {
                const date = new Date('2024-01-15');
                const formatted = formatDate(date, locale);
                expect(formatted).toBeDefined();
            });
            
            test('Number formatting', () => {
                const number = 1234.56;
                const formatted = formatNumber(number, locale);
                expect(formatted).toBeDefined();
            });
            
            test('Currency formatting', () => {
                const amount = 100;
                const currency = getCurrencyForLocale(locale);
                const formatted = formatCurrency(amount, currency, locale);
                expect(formatted).toBeDefined();
            });
        });
    });
});
```

## Real Examples

### US vs Europe vs Asia Localization

#### E-commerce Product Page

```
US Version:
Price: $99.99
Shipping: 5-7 business days
Returns: 30 days
Contact: support@example.com

Europe (Germany) Version:
Preis: 99,99 €
Versand: 5-7 Werktage
Rücksendungen: 30 Tage
Kontakt: support@example.de

Asia (Japan) Version:
価格: 9,999円
配送: 5-7営業日
返品: 30日
お問い合わせ: support@example.jp

Asia (Thailand) Version:
ราคา: ฿3,499.-
การจัดส่ง: 5-7 วันทำการ
การคืนสินค้า: 30 วัน
ติดต่อ: support@example.co.th
```

#### Signup Form

```
US Version:
First Name: [John]
Last Name: [Doe]
Email: [john@example.com]
Password: [•••••••]
Sign Up

Japan Version:
名前: [田中]
名: [太郎]
メールアドレス: [tanaka@example.com]
パスワード: [•••••••]
登録

Thailand Version:
ชื่อ: [สมชช]
นามสกุล: [ใจร์]
อีเมล: [somchai@example.com]
รหัสผ่าน: [•••••••]
ลงทะเบียน
```

## Summary Checklist

### Planning

- [ ] Target locales identified
- [ ] Cultural requirements documented
- [ ] Legal requirements researched
- [ ] Budget allocated for translation

### Content

- [ ] All text translated
- [ ] Images adapted culturally
- [ ] Dates formatted correctly
- [ ] Numbers formatted correctly
- [ ] Currency displayed correctly
- [ ] Addresses formatted correctly
```

---

## Quick Start

### Basic Localization Setup

```javascript
// i18n configuration
import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'

i18n.use(initReactI18next).init({
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
  lng: 'en',
  fallbackLng: 'en'
})
```

### Using Translations

```jsx
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

### Date/Number Formatting

```javascript
// Date formatting
const date = new Date()
const formatted = new Intl.DateTimeFormat('th-TH', {
  year: 'numeric',
  month: 'long',
  day: 'numeric'
}).format(date)

// Number formatting
const number = 1234.56
const formatted = new Intl.NumberFormat('th-TH', {
  style: 'currency',
  currency: 'THB'
}).format(number)  // ฿1,234.56
```

---

## Production Checklist

- [ ] **i18n Setup**: Internationalization framework configured
- [ ] **Translation Keys**: All text uses translation keys
- [ ] **Translations**: Content translated for target languages
- [ ] **Date Formatting**: Dates formatted per locale
- [ ] **Number Formatting**: Numbers formatted per locale
- [ ] **Currency**: Currency displayed correctly
- [ ] **RTL Support**: Right-to-left languages supported
- [ ] **Cultural Adaptation**: Images and content culturally appropriate
- [ ] **Testing**: Tested with native speakers
- [ ] **Fallbacks**: Fallback language configured
- [ ] **Performance**: Translations loaded efficiently
- [ ] **Updates**: Translation process for updates

---

## Anti-patterns

### ❌ Don't: Hardcoded Text

```jsx
// ❌ Bad - Hardcoded
<h1>Welcome</h1>
<p>Hello, user!</p>
```

```jsx
// ✅ Good - Translation keys
<h1>{t('welcome')}</h1>
<p>{t('greeting', { name: user.name })}</p>
```

### ❌ Don't: Ignore Date Formats

```javascript
// ❌ Bad - US format everywhere
const date = '01/15/2024'  // Confusing for non-US users
```

```javascript
// ✅ Good - Locale-aware
const date = new Intl.DateTimeFormat(locale, {
  year: 'numeric',
  month: 'long',
  day: 'numeric'
}).format(new Date())
```

### ❌ Don't: No RTL Support

```css
/* ❌ Bad - Left-aligned only */
.text {
  text-align: left;
}
```

```css
/* ✅ Good - RTL-aware */
.text {
  text-align: start;  /* Adapts to direction */
}

[dir="rtl"] .text {
  text-align: right;
}
```

---

## Integration Points

- **i18n Setup** (`25-internationalization/i18n-setup/`) - Internationalization setup
- **Multi-language** (`25-internationalization/multi-language/`) - Multi-language support
- **RTL Support** (`25-internationalization/rtl-support/`) - Right-to-left languages

---

## Further Reading

- [i18next Documentation](https://www.i18next.com/)
- [React Intl](https://formatjs.io/docs/react-intl/)
- [Localization Best Practices](https://www.w3.org/International/techniques/developing-specs)

### Technical

- [ ] RTL support implemented
- [ ] Timezone handling correct
- [ ] Character encoding correct (UTF-8)
- [ ] Font supports all characters
- [ ] Layout works for all locales

### Testing

- [ ] All locales tested
- [ ] Visual testing completed
- [ ] Automated tests passing
- [ ] User acceptance testing
- [ ] Browser compatibility verified
