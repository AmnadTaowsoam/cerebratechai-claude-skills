# Multi-Step Form Patterns

## Overview

Patterns for building complex multi-step forms with state management, validation, progress tracking, and user experience optimization. This skill covers wizard patterns, form persistence, conditional steps, and best practices for long-form data collection.

---

## 1. Multi-Step Form Architecture

### Form Structure

```markdown
# Multi-Step Form Architecture

## Components
1. **Form Container**: Manages overall state
2. **Step Navigator**: Controls step transitions
3. **Progress Indicator**: Shows completion status
4. **Step Components**: Individual form steps
5. **Validation Engine**: Per-step and global validation
6. **State Persistence**: Save/restore form data

## Form Flow
```
Step 1 → Validate → Step 2 → Validate → ... → Review → Submit
   ↓                  ↓                           ↓
 Save Draft       Save Draft                  Final Submit
```

## Use Cases
- Event creation wizards
- User onboarding
- Booking processes
- Survey forms
- Registration flows
```

---

## 2. Form State Management

### React Hook for Multi-Step Forms

```typescript
// useMultiStepForm Hook
'use client'

import { useState, useCallback } from 'react'

interface UseMultiStepFormOptions<T> {
  initialData: T
  steps: string[]
  onSubmit: (data: T) => Promise<void>
  validate?: (step: number, data: T) => Promise<ValidationErrors>
  onStepChange?: (step: number) => void
}

interface ValidationErrors {
  [key: string]: string
}

export function useMultiStepForm<T extends Record<string, any>>(
  options: UseMultiStepFormOptions<T>
) {
  const [currentStep, setCurrentStep] = useState(0)
  const [formData, setFormData] = useState<T>(options.initialData)
  const [errors, setErrors] = useState<ValidationErrors>({})
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [completedSteps, setCompletedSteps] = useState<Set<number>>(new Set())

  const totalSteps = options.steps.length

  const updateFormData = useCallback((updates: Partial<T>) => {
    setFormData((prev) => ({ ...prev, ...updates }))
  }, [])

  const validateCurrentStep = useCallback(async (): Promise<boolean> => {
    if (!options.validate) return true

    const stepErrors = await options.validate(currentStep, formData)
    setErrors(stepErrors)

    return Object.keys(stepErrors).length === 0
  }, [currentStep, formData, options])

  const goToStep = useCallback(
    async (step: number) => {
      if (step < 0 || step >= totalSteps) return

      // Validate current step before moving forward
      if (step > currentStep) {
        const isValid = await validateCurrentStep()
        if (!isValid) return
      }

      setCurrentStep(step)
      options.onStepChange?.(step)

      // Mark previous step as completed
      if (step > currentStep) {
        setCompletedSteps((prev) => new Set([...prev, currentStep]))
      }
    },
    [currentStep, totalSteps, validateCurrentStep, options]
  )

  const nextStep = useCallback(async () => {
    await goToStep(currentStep + 1)
  }, [currentStep, goToStep])

  const previousStep = useCallback(() => {
    goToStep(currentStep - 1)
  }, [currentStep, goToStep])

  const handleSubmit = useCallback(async () => {
    // Validate all steps
    const isValid = await validateCurrentStep()
    if (!isValid) return

    setIsSubmitting(true)

    try {
      await options.onSubmit(formData)
    } catch (error) {
      console.error('Form submission failed:', error)
      throw error
    } finally {
      setIsSubmitting(false)
    }
  }, [formData, validateCurrentStep, options])

  const resetForm = useCallback(() => {
    setCurrentStep(0)
    setFormData(options.initialData)
    setErrors({})
    setCompletedSteps(new Set())
  }, [options.initialData])

  return {
    currentStep,
    totalSteps,
    formData,
    errors,
    isSubmitting,
    completedSteps,
    updateFormData,
    nextStep,
    previousStep,
    goToStep,
    handleSubmit,
    resetForm,
    isFirstStep: currentStep === 0,
    isLastStep: currentStep === totalSteps - 1,
    progress: ((currentStep + 1) / totalSteps) * 100,
  }
}
```

### Form Container Component

```typescript
// MultiStepFormContainer Component
'use client'

import { ReactNode } from 'react'

interface MultiStepFormContainerProps {
  children: ReactNode
  currentStep: number
  totalSteps: number
  onNext?: () => void
  onPrevious?: () => void
  onSubmit?: () => void
  isSubmitting?: boolean
  showProgress?: boolean
}

export default function MultiStepFormContainer({
  children,
  currentStep,
  totalSteps,
  onNext,
  onPrevious,
  onSubmit,
  isSubmitting = false,
  showProgress = true,
}: MultiStepFormContainerProps) {
  const progress = ((currentStep + 1) / totalSteps) * 100
  const isFirstStep = currentStep === 0
  const isLastStep = currentStep === totalSteps - 1

  return (
    <div className="multi-step-form-container">
      {showProgress && (
        <div className="progress-bar">
          <div className="progress-fill" style={{ width: `${progress}%` }} />
          <div className="progress-text">
            ขั้นตอนที่ {currentStep + 1} จาก {totalSteps}
          </div>
        </div>
      )}

      <div className="form-content">{children}</div>

      <div className="form-navigation">
        {!isFirstStep && (
          <button
            type="button"
            onClick={onPrevious}
            className="btn-secondary"
            disabled={isSubmitting}
          >
            ← ย้อนกลับ
          </button>
        )}

        {!isLastStep ? (
          <button
            type="button"
            onClick={onNext}
            className="btn-primary"
            disabled={isSubmitting}
          >
            ถัดไป →
          </button>
        ) : (
          <button
            type="button"
            onClick={onSubmit}
            className="btn-success"
            disabled={isSubmitting}
          >
            {isSubmitting ? 'กำลังส่ง...' : 'ส่งข้อมูล'}
          </button>
        )}
      </div>
    </div>
  )
}
```

---

## 3. Progress Indicators

### Step Progress Component

```typescript
// StepProgress Component
'use client'

interface Step {
  id: number
  title: string
  description?: string
}

interface StepProgressProps {
  steps: Step[]
  currentStep: number
  completedSteps: Set<number>
  onStepClick?: (step: number) => void
}

export default function StepProgress({
  steps,
  currentStep,
  completedSteps,
  onStepClick,
}: StepProgressProps) {
  return (
    <div className="step-progress">
      {steps.map((step, index) => {
        const isActive = index === currentStep
        const isCompleted = completedSteps.has(index)
        const isClickable = index < currentStep || isCompleted

        return (
          <div
            key={step.id}
            className={`step-item ${isActive ? 'active' : ''} ${
              isCompleted ? 'completed' : ''
            }`}
            onClick={() => isClickable && onStepClick?.(index)}
            style={{ cursor: isClickable ? 'pointer' : 'default' }}
          >
            <div className="step-indicator">
              {isCompleted ? (
                <span className="checkmark">✓</span>
              ) : (
                <span className="step-number">{index + 1}</span>
              )}
            </div>

            <div className="step-content">
              <div className="step-title">{step.title}</div>
              {step.description && (
                <div className="step-description">{step.description}</div>
              )}
            </div>

            {index < steps.length - 1 && (
              <div
                className={`step-connector ${
                  isCompleted ? 'completed' : ''
                }`}
              />
            )}
          </div>
        )
      })}
    </div>
  )
}
```

### Circular Progress

```typescript
// CircularProgress Component
interface CircularProgressProps {
  progress: number
  size?: number
  strokeWidth?: number
}

export default function CircularProgress({
  progress,
  size = 120,
  strokeWidth = 8,
}: CircularProgressProps) {
  const radius = (size - strokeWidth) / 2
  const circumference = radius * 2 * Math.PI
  const offset = circumference - (progress / 100) * circumference

  return (
    <div className="circular-progress">
      <svg width={size} height={size}>
        {/* Background circle */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="#e0e0e0"
          strokeWidth={strokeWidth}
        />

        {/* Progress circle */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="#4CAF50"
          strokeWidth={strokeWidth}
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          transform={`rotate(-90 ${size / 2} ${size / 2})`}
          style={{
            transition: 'stroke-dashoffset 0.3s ease',
          }}
        />
      </svg>

      <div className="progress-percentage">{Math.round(progress)}%</div>
    </div>
  )
}
```

---

## 4. Form Validation

### Per-Step Validation

```typescript
// Form Validation
import { z } from 'zod'

// Define schemas for each step
const step1Schema = z.object({
  eventName: z.string().min(3, 'ชื่ออีเวนต์ต้องมีอย่างน้อย 3 ตัวอักษร'),
  eventType: z.enum(['wedding', 'party', 'merit'], {
    errorMap: () => ({ message: 'กรุณาเลือกประเภทอีเวนต์' }),
  }),
  eventDate: z.date({
    errorMap: () => ({ message: 'กรุณาเลือกวันที่จัดงาน' }),
  }),
})

const step2Schema = z.object({
  venueName: z.string().min(1, 'กรุณาระบุสถานที่'),
  venueAddress: z.string().min(10, 'กรุณาระบุที่อยู่อย่างละเอียด'),
  guestCount: z.number().min(1, 'จำนวนแขกต้องมากกว่า 0'),
})

const step3Schema = z.object({
  budget: z.number().min(1000, 'งบประมาณต้องมากกว่า 1,000 บาท'),
  services: z.array(z.string()).min(1, 'กรุณาเลือกบริการอย่างน้อย 1 รายการ'),
})

// Validation function
async function validateStep(
  step: number,
  data: any
): Promise<ValidationErrors> {
  const schemas = [step1Schema, step2Schema, step3Schema]
  const schema = schemas[step]

  if (!schema) return {}

  try {
    await schema.parseAsync(data)
    return {}
  } catch (error) {
    if (error instanceof z.ZodError) {
      const errors: ValidationErrors = {}
      error.errors.forEach((err) => {
        if (err.path[0]) {
          errors[err.path[0].toString()] = err.message
        }
      })
      return errors
    }
    return {}
  }
}
```

### Async Validation

```typescript
// Async Validation (e.g., checking availability)
async function validateVenueAvailability(
  venueName: string,
  date: Date
): Promise<boolean> {
  try {
    const response = await fetch('/api/venues/check-availability', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ venueName, date }),
    })

    const result = await response.json()
    return result.available
  } catch (error) {
    console.error('Availability check failed:', error)
    return false
  }
}

// Use in validation
async function validateStep2WithAvailability(
  data: any
): Promise<ValidationErrors> {
  const errors = await validateStep(1, data)

  // Additional async validation
  if (data.venueName && data.eventDate) {
    const isAvailable = await validateVenueAvailability(
      data.venueName,
      data.eventDate
    )

    if (!isAvailable) {
      errors.venueName = 'สถานที่นี้ไม่ว่างในวันที่เลือก'
    }
  }

  return errors
}
```

---

## 5. Form Persistence

### Local Storage Persistence

```typescript
// Form Persistence Hook
'use client'

import { useEffect } from 'react'

interface UseFormPersistenceOptions<T> {
  key: string
  data: T
  enabled?: boolean
}

export function useFormPersistence<T>({
  key,
  data,
  enabled = true,
}: UseFormPersistenceOptions<T>) {
  // Save to localStorage
  useEffect(() => {
    if (!enabled) return

    try {
      localStorage.setItem(key, JSON.stringify(data))
    } catch (error) {
      console.error('Failed to save form data:', error)
    }
  }, [key, data, enabled])

  // Load from localStorage
  const loadSavedData = (): T | null => {
    if (!enabled) return null

    try {
      const saved = localStorage.getItem(key)
      return saved ? JSON.parse(saved) : null
    } catch (error) {
      console.error('Failed to load form data:', error)
      return null
    }
  }

  // Clear saved data
  const clearSavedData = () => {
    try {
      localStorage.removeItem(key)
    } catch (error) {
      console.error('Failed to clear form data:', error)
    }
  }

  return { loadSavedData, clearSavedData }
}
```

### Auto-Save Feature

```typescript
// Auto-Save Component
'use client'

import { useEffect, useState } from 'react'
import { debounce } from 'lodash'

interface AutoSaveProps<T> {
  data: T
  onSave: (data: T) => Promise<void>
  delay?: number
}

export function AutoSave<T>({ data, onSave, delay = 2000 }: AutoSaveProps<T>) {
  const [saving, setSaving] = useState(false)
  const [lastSaved, setLastSaved] = useState<Date | null>(null)

  useEffect(() => {
    const debouncedSave = debounce(async () => {
      setSaving(true)

      try {
        await onSave(data)
        setLastSaved(new Date())
      } catch (error) {
        console.error('Auto-save failed:', error)
      } finally {
        setSaving(false)
      }
    }, delay)

    debouncedSave()

    return () => {
      debouncedSave.cancel()
    }
  }, [data, onSave, delay])

  return (
    <div className="auto-save-indicator">
      {saving ? (
        <span>กำลังบันทึก...</span>
      ) : lastSaved ? (
        <span>
          บันทึกล่าสุด: {lastSaved.toLocaleTimeString('th-TH')}
        </span>
      ) : null}
    </div>
  )
}
```

---

## 6. Conditional Steps

### Dynamic Step Flow

```typescript
// Conditional Steps Logic
interface ConditionalStepConfig {
  id: number
  title: string
  condition?: (data: any) => boolean
}

function getActiveSteps(
  allSteps: ConditionalStepConfig[],
  formData: any
): ConditionalStepConfig[] {
  return allSteps.filter((step) => {
    if (!step.condition) return true
    return step.condition(formData)
  })
}

// Example: Event form with conditional steps
const eventFormSteps: ConditionalStepConfig[] = [
  {
    id: 0,
    title: 'ข้อมูลพื้นฐาน',
  },
  {
    id: 1,
    title: 'สถานที่',
  },
  {
    id: 2,
    title: 'งบประมาณ',
  },
  {
    id: 3,
    title: 'พิธีการ',
    condition: (data) => data.eventType === 'wedding',
  },
  {
    id: 4,
    title: 'อาหารและเครื่องดื่ม',
    condition: (data) => data.guestCount > 50,
  },
  {
    id: 5,
    title: 'ตรวจสอบข้อมูล',
  },
]

// Usage
const activeSteps = getActiveSteps(eventFormSteps, formData)
```

---

## 7. Complete Example: Event Creation Form

### Event Creation Wizard

```typescript
// EventCreationWizard Component
'use client'

import { useMultiStepForm } from './useMultiStepForm'
import MultiStepFormContainer from './MultiStepFormContainer'
import StepProgress from './StepProgress'
import { AutoSave } from './AutoSave'

interface EventFormData {
  // Step 1
  eventName: string
  eventType: 'wedding' | 'party' | 'merit' | ''
  eventDate: Date | null

  // Step 2
  venueName: string
  venueAddress: string
  guestCount: number

  // Step 3
  budget: number
  services: string[]

  // Step 4
  notes: string
}

const initialData: EventFormData = {
  eventName: '',
  eventType: '',
  eventDate: null,
  venueName: '',
  venueAddress: '',
  guestCount: 0,
  budget: 0,
  services: [],
  notes: '',
}

const steps = [
  { id: 0, title: 'ข้อมูลพื้นฐาน', description: 'ชื่อและประเภทงาน' },
  { id: 1, title: 'สถานที่', description: 'สถานที่จัดงาน' },
  { id: 2, title: 'งบประมาณ', description: 'งบประมาณและบริการ' },
  { id: 3, title: 'ตรวจสอบ', description: 'ตรวจสอบข้อมูล' },
]

export default function EventCreationWizard() {
  const form = useMultiStepForm({
    initialData,
    steps: steps.map((s) => s.title),
    onSubmit: async (data) => {
      // Submit to API
      const response = await fetch('/api/events', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      })

      if (!response.ok) {
        throw new Error('Failed to create event')
      }
    },
    validate: validateStep,
  })

  const handleAutoSave = async (data: EventFormData) => {
    // Save draft to server
    await fetch('/api/events/draft', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
  }

  return (
    <div className="event-creation-wizard">
      <h1>สร้างอีเวนต์ใหม่</h1>

      <StepProgress
        steps={steps}
        currentStep={form.currentStep}
        completedSteps={form.completedSteps}
        onStepClick={form.goToStep}
      />

      <AutoSave data={form.formData} onSave={handleAutoSave} />

      <MultiStepFormContainer
        currentStep={form.currentStep}
        totalSteps={form.totalSteps}
        onNext={form.nextStep}
        onPrevious={form.previousStep}
        onSubmit={form.handleSubmit}
        isSubmitting={form.isSubmitting}
      >
        {form.currentStep === 0 && (
          <Step1BasicInfo
            data={form.formData}
            errors={form.errors}
            onChange={form.updateFormData}
          />
        )}

        {form.currentStep === 1 && (
          <Step2Venue
            data={form.formData}
            errors={form.errors}
            onChange={form.updateFormData}
          />
        )}

        {form.currentStep === 2 && (
          <Step3Budget
            data={form.formData}
            errors={form.errors}
            onChange={form.updateFormData}
          />
        )}

        {form.currentStep === 3 && (
          <Step4Review data={form.formData} />
        )}
      </MultiStepFormContainer>
    </div>
  )
}

// Step Components
function Step1BasicInfo({ data, errors, onChange }: any) {
  return (
    <div className="form-step">
      <h2>ข้อมูลพื้นฐาน</h2>

      <div className="form-field">
        <label>ชื่ออีเวนต์</label>
        <input
          type="text"
          value={data.eventName}
          onChange={(e) => onChange({ eventName: e.target.value })}
        />
        {errors.eventName && <span className="error">{errors.eventName}</span>}
      </div>

      <div className="form-field">
        <label>ประเภทงาน</label>
        <select
          value={data.eventType}
          onChange={(e) => onChange({ eventType: e.target.value })}
        >
          <option value="">เลือกประเภท</option>
          <option value="wedding">งานแต่งงาน</option>
          <option value="party">งานเลี้ยง</option>
          <option value="merit">งานบุญ</option>
        </select>
        {errors.eventType && <span className="error">{errors.eventType}</span>}
      </div>

      <div className="form-field">
        <label>วันที่จัดงาน</label>
        <input
          type="date"
          value={data.eventDate?.toISOString().split('T')[0] || ''}
          onChange={(e) => onChange({ eventDate: new Date(e.target.value) })}
        />
        {errors.eventDate && <span className="error">{errors.eventDate}</span>}
      </div>
    </div>
  )
}

// ... Other step components
```

---

## Best Practices

1. **User Experience**
   - Show clear progress indicators
   - Allow navigation to previous steps
   - Provide save/draft functionality
   - Use appropriate validation timing

2. **Performance**
   - Lazy load step components
   - Debounce auto-save
   - Optimize validation
   - Cache validation results

3. **Accessibility**
   - Keyboard navigation
   - Screen reader support
   - Focus management
   - Error announcements

4. **Data Management**
   - Persist form state
   - Handle browser refresh
   - Implement auto-save
   - Validate before transitions

5. **Error Handling**
   - Clear error messages
   - Field-level validation
   - Step-level validation
   - Global validation

---

## Common Pitfalls

1. **Lost Data**: Not implementing persistence
2. **Confusing Navigation**: Unclear progress indicators
3. **Validation Timing**: Validating too early or too late
4. **Performance**: Not optimizing re-renders
5. **Accessibility**: Forgetting keyboard navigation

---

## Production Checklist

- [ ] Progress indicator implemented
- [ ] Validation per step working
- [ ] Form persistence enabled
- [ ] Auto-save configured
- [ ] Navigation tested
- [ ] Error handling comprehensive
- [ ] Accessibility verified
- [ ] Mobile responsive
- [ ] Performance optimized
- [ ] Analytics tracking

---

## Tools & Libraries

| Tool | Purpose |
|------|---------|
| React Hook Form | Form state management |
| Zod | Schema validation |
| Formik | Alternative form library |
| Yup | Alternative validation |

---

## Further Reading

- [Form Design Best Practices](https://www.nngroup.com/articles/web-form-design/)
- [Multi-Step Form UX](https://baymard.com/blog/checkout-flow-average-form-fields)
- [React Hook Form Documentation](https://react-hook-form.com/)
- [Zod Documentation](https://zod.dev/)
