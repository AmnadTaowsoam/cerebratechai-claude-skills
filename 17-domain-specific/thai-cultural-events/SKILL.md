# Thai Cultural Event Planning

## Overview

Domain knowledge for Thai ceremonies, rituals, and cultural practices including weddings, ordinations, funerals, merit-making ceremonies, and regional customs. This skill provides guidance for event planning platforms serving Thai cultural events.

---

## 1. Thai Wedding Ceremonies

### Traditional Thai Wedding Structure

```markdown
# Thai Wedding Ceremony (งานแต่งงานแบบไทย)

## Main Ceremonies

### 1. Khan Maak Procession (ขันหมาก)
- **Time**: Morning, before main ceremony
- **Duration**: 30-60 minutes
- **Participants**: Groom's family, friends
- **Items Needed**:
  - Khan Maak trays (ขันหมาก)
  - Betel nuts and leaves
  - Flowers and decorations
  - Traditional Thai musical instruments
  - Dancers (optional)

### 2. Door Ceremony (รดน้ำสังข์)
- **Purpose**: Groom proves worthiness
- **Activities**:
  - Answer riddles
  - Pass through symbolic gates
  - Pay "gate fees" (เงินกั้นประตู)
- **Duration**: 15-30 minutes

### 3. Merit-Making Ceremony (ทำบุญ)
- **Time**: Early morning (6:00-8:00 AM)
- **Participants**: 9 monks (auspicious number)
- **Items Needed**:
  - Monk robes and alms
  - Food offerings
  - Flowers, candles, incense
  - Holy water
- **Duration**: 1-2 hours

### 4. Water Pouring Ceremony (รดน้ำสังข์)
- **Time**: After merit-making
- **Significance**: Blessings from elders
- **Setup**:
  - Conch shell for water
  - Flower garlands
  - Cushions for couple
  - Blessing station
- **Duration**: 30-60 minutes

### 5. Reception (งานเลี้ยง)
- **Time**: Evening
- **Duration**: 3-4 hours
- **Activities**:
  - Dinner
  - Entertainment
  - Photo opportunities
  - Gift giving
```

### Regional Wedding Variations

```typescript
// Regional Wedding Customs
interface RegionalWeddingCustoms {
  region: 'north' | 'northeast' | 'central' | 'south'
  customs: WeddingCustom[]
  specialRequirements: string[]
}

const regionalWeddings: Record<string, RegionalWeddingCustoms> = {
  north: {
    region: 'north',
    customs: [
      {
        name: 'Tung (ตุง)',
        description: 'Northern Thai flags for decoration',
        timing: 'Throughout ceremony',
        items: ['Colorful flags', 'Bamboo poles', 'Decorative papers'],
      },
      {
        name: 'Khan Tok Dinner',
        description: 'Traditional Northern Thai dining style',
        timing: 'Reception',
        items: ['Low round tables', 'Floor cushions', 'Northern Thai food'],
      },
    ],
    specialRequirements: [
      'Traditional Lanna music',
      'Northern Thai costumes',
      'Khan Tok dining setup',
    ],
  },
  northeast: {
    region: 'northeast',
    customs: [
      {
        name: 'Baci Ceremony (บายศรี)',
        description: 'String tying ceremony for blessings',
        timing: 'Before main ceremony',
        items: ['White strings', 'Baci centerpiece', 'Offerings'],
      },
      {
        name: 'Sin Sod Negotiation',
        description: 'Bride price discussion',
        timing: 'Before wedding day',
        items: ['Cash', 'Gold jewelry', 'Negotiation gifts'],
      },
    ],
    specialRequirements: [
      'Mor Lam music',
      'Isaan traditional dress',
      'Sticky rice and Isaan food',
    ],
  },
  central: {
    region: 'central',
    customs: [
      {
        name: 'Standard Thai Wedding',
        description: 'Most common format',
        timing: 'Full day',
        items: ['Standard wedding items'],
      },
    ],
    specialRequirements: [
      'Traditional Thai music',
      'Central Thai cuisine',
      'Formal attire',
    ],
  },
  south: {
    region: 'south',
    customs: [
      {
        name: 'Mahr (มัฮร์) - for Muslim weddings',
        description: 'Bride price in Islamic tradition',
        timing: 'During Nikah ceremony',
        items: ['Cash or gold', 'Quran', 'Prayer items'],
      },
      {
        name: 'Southern Thai Feast',
        description: 'Spicy Southern cuisine',
        timing: 'Reception',
        items: ['Southern Thai dishes', 'Seafood', 'Spicy curries'],
      },
    ],
    specialRequirements: [
      'Southern Thai music',
      'Halal food options (for Muslim weddings)',
      'Southern Thai costumes',
    ],
  },
}

interface WeddingCustom {
  name: string
  description: string
  timing: string
  items: string[]
}
```

---

## 2. Buddhist Ordination Ceremonies

### Ordination Structure

```markdown
# Buddhist Ordination (บวช)

## Types of Ordination

### 1. Temporary Ordination (บวชชั่วคราว)
- **Duration**: 7-15 days typical
- **Purpose**: Merit-making for parents
- **Common Age**: 20+ years old

### 2. Permanent Ordination (บวชถาวร)
- **Duration**: Lifelong commitment
- **Requirements**: More strict

## Ordination Ceremony Phases

### Phase 1: Preparation (1-2 weeks before)
- Hair cutting ceremony (โกนผม)
- Eyebrow shaving
- Preparation of monk robes
- Invitation of monks
- Preparation of offerings

### Phase 2: Procession Day (วันแห่)
- **Time**: Morning
- **Activities**:
  - Dress in white
  - Parade around temple
  - Traditional music and dancing
  - Photo opportunities
- **Items Needed**:
  - White clothing
  - Flower garlands
  - Decorative umbrellas
  - Traditional Thai band

### Phase 3: Ordination Ceremony (วันบวช)
- **Time**: Early morning
- **Location**: Temple ordination hall (โบสถ์)
- **Participants**:
  - Preceptor monk (พระอุปัชฌาย์)
  - Teacher monk (พระกรรมวาจาจารย์)
  - Witness monks (พระสงฆ์พยาน) - minimum 5
- **Duration**: 1-2 hours

### Phase 4: Post-Ordination Celebration
- **Activities**:
  - Merit-making feast
  - Gifts to monks
  - Family celebration
  - Photo sessions
```

### Ordination Checklist

```typescript
// Ordination Planning Checklist
interface OrdinationRequirements {
  category: string
  items: OrdinationItem[]
}

const ordinationChecklist: OrdinationRequirements[] = [
  {
    category: 'Monk Robes and Items',
    items: [
      { item: 'Monk robes (3 pieces)', quantity: 1, required: true },
      { item: 'Alms bowl', quantity: 1, required: true },
      { item: 'Water filter', quantity: 1, required: true },
      { item: 'Razor', quantity: 1, required: true },
      { item: 'Umbrella', quantity: 1, required: true },
      { item: 'Sandals', quantity: 1, required: true },
    ],
  },
  {
    category: 'Ceremony Offerings',
    items: [
      { item: 'Flowers, candles, incense', quantity: 1, required: true },
      { item: 'Food for monks', quantity: 1, required: true },
      { item: 'Monk robes for donation', quantity: 9, required: false },
      { item: 'Cash offerings', quantity: 1, required: true },
    ],
  },
  {
    category: 'Procession Items',
    items: [
      { item: 'White clothing', quantity: 1, required: true },
      { item: 'Flower garlands', quantity: 5, required: true },
      { item: 'Decorative umbrellas', quantity: 2, required: false },
      { item: 'Traditional Thai band', quantity: 1, required: false },
    ],
  },
  {
    category: 'Temple Arrangements',
    items: [
      { item: 'Temple booking', quantity: 1, required: true },
      { item: 'Monk coordination', quantity: 1, required: true },
      { item: 'Ordination hall reservation', quantity: 1, required: true },
    ],
  },
]

interface OrdinationItem {
  item: string
  quantity: number
  required: boolean
}
```

---

## 3. Funeral Rites

### Thai Buddhist Funeral

```markdown
# Thai Buddhist Funeral (งานศพ)

## Funeral Duration
- **Short**: 3 days
- **Standard**: 7 days
- **Extended**: 100 days (for important persons)

## Daily Schedule

### Morning (6:00-8:00 AM)
- Merit-making with monks
- Chanting
- Food offerings

### Evening (7:00-9:00 PM)
- Monk chanting
- Sermon (if applicable)
- Guests pay respects
- Refreshments for guests

## Cremation Day (วันฌาปนกิจ)

### Schedule
- **Morning**: Final merit-making
- **Afternoon**: Procession to crematorium
- **Evening**: Cremation ceremony
- **After**: Bone collection (next day)

### Items Needed
- Coffin and decorations
- Funeral flowers
- Monk robes for donation
- Food for monks and guests
- Cremation arrangements
- Memorial booklets
- Thank you gifts for guests
```

### Funeral Planning

```typescript
// Funeral Planning System
interface FuneralPlan {
  duration: 3 | 7 | 100
  dailySchedule: DailySchedule[]
  cremationDay: Date
  budget: FuneralBudget
}

interface DailySchedule {
  day: number
  morning: {
    time: string
    activity: string
    monksNeeded: number
  }
  evening: {
    time: string
    activity: string
    monksNeeded: number
  }
}

interface FuneralBudget {
  templeExpenses: number
  monkOfferings: number
  coffinAndDecorations: number
  foodAndRefreshments: number
  cremationFees: number
  memorialBooklets: number
  miscellaneous: number
  total: number
}

function calculateFuneralBudget(
  duration: number,
  guestCount: number,
  cremationType: 'standard' | 'premium'
): FuneralBudget {
  const dailyMonkOffering = 500 * 9 // 9 monks per day
  const dailyFood = guestCount * 50 // 50 THB per guest per day

  return {
    templeExpenses: 10000,
    monkOfferings: dailyMonkOffering * duration,
    coffinAndDecorations: cremationType === 'premium' ? 50000 : 20000,
    foodAndRefreshments: dailyFood * duration * 2, // Morning and evening
    cremationFees: cremationType === 'premium' ? 30000 : 15000,
    memorialBooklets: guestCount * 100,
    miscellaneous: 10000,
    total: 0, // Calculate sum
  }
}
```

---

## 4. Merit-Making Ceremonies

### Common Merit-Making Events

```markdown
# Merit-Making Ceremonies (งานทำบุญ)

## Types of Merit-Making

### 1. House Blessing (ทำบุญบ้าน)
- **Occasion**: New house, moving in
- **Monks**: 9 monks
- **Time**: Morning (7:00-9:00 AM)
- **Items**:
  - Food offerings
  - Monk robes
  - Holy water
  - House blessing items

### 2. Birthday Merit-Making (ทำบุญวันเกิด)
- **Monks**: 9 monks (or age + 1)
- **Time**: Morning
- **Special**: Release birds/fish for long life

### 3. New Year Merit-Making (ทำบุญปีใหม่)
- **Time**: January 1st or Songkran
- **Activities**:
  - Monk feeding
  - Water pouring on Buddha images
  - Elderly respect ceremony

### 4. Memorial Merit-Making (ทำบุญอุทิศ)
- **Occasion**: Death anniversary
- **Duration**: 1 day or 7 days
- **Purpose**: Transfer merit to deceased

### 5. Kathin Ceremony (ทอดกฐิน)
- **Time**: After Buddhist Lent (October-November)
- **Purpose**: Offer robes to monks
- **Scale**: Community event
```

---

## 5. Auspicious Date Calculation

### Thai Astrology for Events

```typescript
// Thai Auspicious Date Calculator
interface AuspiciousDate {
  date: Date
  score: number
  reasons: string[]
  warnings: string[]
}

class ThaiAstrologyCalculator {
  // Thai lunar calendar considerations
  getAuspiciousDates(
    startDate: Date,
    endDate: Date,
    eventType: 'wedding' | 'ordination' | 'housewarming'
  ): AuspiciousDate[] {
    const dates: AuspiciousDate[] = []

    // Iterate through dates
    for (
      let date = new Date(startDate);
      date <= endDate;
      date.setDate(date.getDate() + 1)
    ) {
      const score = this.calculateAuspiciousness(new Date(date), eventType)

      if (score > 70) {
        dates.push({
          date: new Date(date),
          score,
          reasons: this.getAuspiciousReasons(new Date(date), eventType),
          warnings: this.getWarnings(new Date(date)),
        })
      }
    }

    return dates.sort((a, b) => b.score - a.score)
  }

  private calculateAuspiciousness(date: Date, eventType: string): number {
    let score = 50 // Base score

    // Check day of week
    const dayOfWeek = date.getDay()
    const dayScores = {
      wedding: [60, 80, 70, 90, 75, 85, 65], // Sun-Sat
      ordination: [70, 85, 75, 80, 70, 90, 60],
      housewarming: [75, 80, 70, 85, 80, 90, 65],
    }

    score += (dayScores[eventType][dayOfWeek] - 50)

    // Avoid Buddhist holy days for weddings
    if (eventType === 'wedding' && this.isBuddhistHolyDay(date)) {
      score -= 30
    }

    // Prefer Buddhist holy days for ordinations
    if (eventType === 'ordination' && this.isBuddhistHolyDay(date)) {
      score += 20
    }

    // Check Thai lunar calendar
    const lunarDay = this.getThaiLunarDay(date)
    if (lunarDay === 15 || lunarDay === 1) {
      // Full moon or new moon
      score += 10
    }

    return Math.min(100, Math.max(0, score))
  }

  private isBuddhistHolyDay(date: Date): boolean {
    // Check if date is Wan Phra (Buddhist holy day)
    // Occurs on 8th and 15th of waxing/waning moon
    const lunarDay = this.getThaiLunarDay(date)
    return lunarDay === 8 || lunarDay === 15
  }

  private getThaiLunarDay(date: Date): number {
    // Simplified lunar calendar calculation
    // In production, use proper Thai lunar calendar library
    const daysSinceNewMoon = Math.floor(
      (date.getTime() - new Date('2000-01-06').getTime()) /
        (1000 * 60 * 60 * 24)
    ) % 29.5

    return Math.floor(daysSinceNewMoon) + 1
  }

  private getAuspiciousReasons(date: Date, eventType: string): string[] {
    const reasons: string[] = []

    const dayNames = [
      'วันอาทิตย์',
      'วันจันทร์',
      'วันอังคาร',
      'วันพุธ',
      'วันพฤหัสบดี',
      'วันศุกร์',
      'วันเสาร์',
    ]

    reasons.push(`${dayNames[date.getDay()]} เป็นวันมงคล`)

    if (this.isBuddhistHolyDay(date)) {
      reasons.push('ตรงกับวันพระ')
    }

    const lunarDay = this.getThaiLunarDay(date)
    if (lunarDay === 15) {
      reasons.push('วันเพ็ญ (ขึ้น 15 ค่ำ)')
    }

    return reasons
  }

  private getWarnings(date: Date): string[] {
    const warnings: string[] = []

    // Check for inauspicious periods
    // This is simplified - real implementation would be more complex

    return warnings
  }
}

// Usage
const calculator = new ThaiAstrologyCalculator()
const auspiciousDates = calculator.getAuspiciousDates(
  new Date('2026-06-01'),
  new Date('2026-12-31'),
  'wedding'
)

console.log('Top 5 auspicious dates for wedding:')
auspiciousDates.slice(0, 5).forEach((date) => {
  console.log(`${date.date.toLocaleDateString('th-TH')} - Score: ${date.score}`)
  console.log(`Reasons: ${date.reasons.join(', ')}`)
})
```

---

## 6. Vendor Types and Roles

### Thai Event Vendors

```typescript
// Thai Event Vendor Categories
interface VendorCategory {
  category: string
  vendors: VendorType[]
  essential: boolean
}

const thaiEventVendors: VendorCategory[] = [
  {
    category: 'Religious',
    essential: true,
    vendors: [
      {
        type: 'Temple/Monks',
        description: 'Buddhist monks for ceremonies',
        typical Cost: '5,000-20,000 THB',
        notes: 'Book 1-2 months in advance',
      },
      {
        type: 'Brahmin Priest',
        description: 'For Hindu-influenced ceremonies',
        typicalCost: '10,000-30,000 THB',
        notes: 'Required for some traditional weddings',
      },
    ],
  },
  {
    category: 'Traditional Performance',
    essential: false,
    vendors: [
      {
        type: 'Khan Maak Procession',
        description: 'Traditional wedding procession',
        typicalCost: '15,000-50,000 THB',
        notes: 'Includes dancers, musicians, decorations',
      },
      {
        type: 'Traditional Thai Band',
        description: 'Live traditional music',
        typicalCost: '10,000-30,000 THB',
        notes: 'For processions and ceremonies',
      },
      {
        type: 'Classical Thai Dancers',
        description: 'Traditional dance performance',
        typicalCost: '20,000-80,000 THB',
        notes: 'For entertainment',
      },
    ],
  },
  {
    category: 'Ceremonial Items',
    essential: true,
    vendors: [
      {
        type: 'Khan Maak Shop',
        description: 'Traditional wedding trays and items',
        typicalCost: '5,000-20,000 THB',
        notes: 'Can rent or buy',
      },
      {
        type: 'Flower Garland Maker',
        description: 'Traditional Thai flower garlands',
        typicalCost: '2,000-10,000 THB',
        notes: 'Fresh flowers daily',
      },
      {
        type: 'Monk Robe Shop',
        description: 'Robes and monk supplies',
        typicalCost: '3,000-15,000 THB',
        notes: 'For ordinations and merit-making',
      },
    ],
  },
  {
    category: 'Food and Catering',
    essential: true,
    vendors: [
      {
        type: 'Traditional Thai Caterer',
        description: 'Authentic Thai cuisine',
        typicalCost: '300-1,500 THB per person',
        notes: 'Regional specialties available',
      },
      {
        type: 'Monk Food Preparation',
        description: 'Vegetarian food for monks',
        typicalCost: '200-500 THB per monk',
        notes: 'Must be prepared before noon',
      },
    ],
  },
]

interface VendorType {
  type: string
  description: string
  typicalCost: string
  notes: string
}
```

---

## Best Practices

1. **Cultural Sensitivity**
   - Respect religious customs
   - Follow traditional protocols
   - Consult with elders
   - Hire experienced coordinators

2. **Timing**
   - Book temples early (2-3 months)
   - Consider auspicious dates
   - Respect Buddhist holy days
   - Plan for weather (rainy season)

3. **Budget Planning**
   - Monk offerings are essential
   - Quality over quantity for religious items
   - Regional price variations
   - Hidden costs (transportation, etc.)

4. **Regional Awareness**
   - Research local customs
   - Hire local vendors
   - Respect regional differences
   - Language considerations

5. **Documentation**
   - Photo/video permissions at temples
   - Respect sacred spaces
   - Preserve traditions
   - Share knowledge

---

## Common Pitfalls

1. **Scheduling Conflicts**: Not checking Buddhist calendar
2. **Insufficient Monks**: Not booking enough monks in advance
3. **Cultural Misunderstandings**: Not consulting with elders
4. **Budget Underestimation**: Forgetting traditional items
5. **Regional Differences**: Applying central customs to all regions

---

## Production Checklist

- [ ] Cultural research completed
- [ ] Regional customs identified
- [ ] Auspicious dates calculated
- [ ] Temple/monks booked
- [ ] Traditional items sourced
- [ ] Vendor coordination confirmed
- [ ] Budget approved
- [ ] Timeline established
- [ ] Backup plans prepared
- [ ] Cultural advisor consulted

---

## Resources

- Thai Astrology Calendar
- Temple Directory
- Traditional Vendor Networks
- Regional Custom Guides
- Buddhist Calendar
- Cultural Consultants

---

## Further Reading

- [Thai Wedding Customs](https://www.tourismthailand.org/Articles/thai-wedding-customs)
- [Buddhist Ceremonies in Thailand](https://www.buddhanet.net/e-learning/buddhistworld/thai-txt.htm)
- [Thai Lunar Calendar](https://www.thaicalendar.com/)
- [Regional Thai Cultures](https://www.sac.or.th/)
