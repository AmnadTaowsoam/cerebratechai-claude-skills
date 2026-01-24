# Multi-Step Form Patterns

---

## 1. Executive Summary & Strategic Necessity

### 1.1 Context (ภาษาไทย)

Multi-Step Form คือ pattern สำหรับการสร้าง forms ที่มีหลายขั้นตอน (wizard pattern) ซึ่งช่วยให้ผู้ใช้กรอกข้อมูลที่ซับซ้อนได้ง่ายขึ้น โดยแบ่งข้อมูลออกเป็น steps ที่เล็กลง และมีการตรวจสอบ (validation) และบันทึกข้อมูล (persistence) ตลอดเวลา

Multi-Step Form ใช้ React Hook Form สำหรับ state management และ Zod สำหรับ validation พร้อมกับ auto-save และ progress indicators ที่ช่วยให้ผู้ใช้เข้าใจสถานะของ form และสามารถกลับมาทำต่อได้

### 1.2 Business Impact (ภาษาไทย)

**ผลกระทบทางธุรกิจ:**

1. **เพิ่ม Completion Rate** - Multi-step forms ช่วยเพิ่ม completion rate ได้ถึง 20-30%
2. **ลด Form Abandonment** - การแบ่งขั้นตอนช่วยลด form abandonment rate
3. **เพิ่ม Data Quality** - Per-step validation ช่วยเพิ่มคุณภาพข้อมูล
4. **เพิ่ม User Experience** - Progress indicators และ auto-save ช่วยเพิ่ม UX
5. **ปรับปรุง Conversion** - การกรอกข้อมูลที่ง่ายขึ้นช่วยเพิ่ม conversion rate

### 1.3 Product Thinking (ภาษาไทย)

**มุมมองด้านผลิตภัณฑ์:**

1. **User-Centric** - Form ต้องเป็นประโยชน์และเข้าใจง่ายสำหรับผู้ใช้
2. **Progressive Disclosure** - แสดงข้อมูลทีละ step เพื่อลด cognitive load
3. **Data Persistence** - บันทึกข้อมูลอัตโนมัติเพื่อป้องกัน data loss
4. **Validation First** - Validate ข้อมูลทุก step เพื่อป้องกัน errors
5. **Accessibility** - Form ต้องเข้าถึงได้และใช้งานได้สำหรับผู้ใช้ทุกคน

---

## 2. Technical Deep Dive (The "How-to")

### 2.1 Core Logic

Multi-Step Form ประกอบด้วย 6 components หลัก:

1. **Form Container** - จัดการ overall state ของ form
2. **Step Navigator** - ควบคุมการเปลี่ยน step
3. **Progress Indicator** - แสดงสถานะ completion
4. **Step Components** - Components สำหรับแต่ละ step
5. **Validation Engine** - Per-step และ global validation
6. **State Persistence** - Save/restore form data

### 2.2 Architecture Diagram Requirements

```
┌─────────────────────────────────────────────────────────┐
│              Multi-Step Form Architecture               │
├─────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌───────────────────────────────────────────────────┐   │
│  │              User Interface Layer                   │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  Progress    │  │  Step       │  │  Form      │  │   │
│  │  │  Indicator  │  │  Navigator  │  │  Content  │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
│  ┌───────────────────────────────────────────────────┐   │
│  │              State Management Layer                 │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  Form       │  │  Step       │  │  Error     │  │   │
│  │  │  State      │  │  State      │  │  State     │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  Completed   │  │  Submitting │  │  Draft     │  │   │
│  │  │  Steps      │  │  State      │  │  State     │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Validation Layer                        │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  Per-Step   │  │  Global     │  │  Async     │  │   │
│  │  │  Validation │  │  Validation │  │  Validation│  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Persistence Layer                      │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  Local      │  │  Session    │  │  Server    │  │   │
│  │  │  Storage    │  │  Storage    │  │  Storage   │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Auto-Save Layer                        │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  Debounced  │  │  Throttled  │  │  Manual    │  │   │
│  │  │  Save       │  │  Save       │  │  Save      │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
└─────────────────────────────────────────────────────────┘
```

### 2.3 Implementation Workflow

**Step 1: Create Multi-Step Form Hook**

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

---

## 3. Tooling & Tech Stack

### 3.1 Enterprise Tools

| Tool | Purpose | Version | License |
|------|---------|---------|---------|
| React Hook Form | Form State Management | ^7.0.0 | MIT |
| Zod | Schema Validation | ^3.0.0 | MIT |
| React | UI Library | ^18.0.0 | MIT |
| TypeScript | Type Safety | ^5.0.0 | Apache 2.0 |
| Lodash | Utility Functions | ^4.0.0 | MIT |

### 3.2 Configuration Essentials

**TypeScript Configuration:**
```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "lib": ["DOM", "DOM.Iterable", "ESNext"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "target": "ES2020"
  }
}
```

---

## 4. Standards, Compliance & Security

### 4.1 International Standards

- **WCAG 2.1 Level AA** - Forms ต้องเข้าถึงได้และใช้งานได้สำหรับผู้ใช้ทุกคน
- **ISO 9241-11** - Usability Standards สำหรับ Form Design
- **GDPR** - Data Protection สำหรับ User Data
- **PCI DSS** - Security Standards สำหรับ Payment Forms

### 4.2 Security Protocol

Multi-Step Form ต้องปฏิบัติตามหลักความปลอดภัย:

1. **Input Sanitization** - Sanitize data ก่อนบันทึก
2. **CSRF Protection** - ใช้ CSRF tokens สำหรับ forms
3. **Secure Storage** - ไม่เก็บ sensitive data ใน localStorage
4. **Rate Limiting** - จำกัดจำนวน submissions ต่อผู้ใช้

```typescript
// Secure form handling
import { z } from 'zod'

// Sanitize input before validation
const sanitizeInput = (input: string): string => {
  return input
    .replace(/[<>]/g, '') // Remove potential XSS
    .trim()
}

// Secure schema validation
const secureSchema = z.object({
  email: z.string().email().transform(sanitizeInput),
  password: z.string().min(8),
})
```

### 4.3 Explainability

Multi-Step Form ต้องสามารถอธิบายได้ว่า:

1. **Validation Logic** - ทำไม field ถูก validate อย่างไร
2. **Step Transition** - ทำไม step ถูก skip หรือ show
3. **Auto-Save** - ทำไมข้อมูลถูกบันทึกเมื่อไร
4. **Error Messages** - ทำไมเกิด error และวิธีแก้ไข

---

## 5. Unit Economics & Performance Metrics (KPIs)

### 5.1 Cost Calculation

| Metric | Calculation | Target |
|--------|-------------|--------|
| Form Completion Rate | Completed forms / Started forms | > 70% |
| Time to Complete | Average time to complete form | < 5 min |
| Error Rate | Failed validations / Total attempts | < 10% |
| Abandonment Rate | Abandoned forms / Started forms | < 30% |
| Auto-Save Success | Successful saves / Total saves | > 95% |

### 5.2 Key Performance Indicators

**Technical Metrics:**

1. **Form Completion Rate** - อัตราการเสร็จสิ้น form
2. **Time to Complete** - เวลาในการกรอก form
3. **Error Rate** - อัตราการเกิด errors
4. **Abandonment Rate** - อัตราการละทิ้ง form

**Business Metrics:**

1. **Conversion Rate** - อัตราการแปลงผู้ใช้
2. **Data Quality** - คุณภาพข้อมูลที่ได้
3. **User Satisfaction** - ความพึงพอใจของผู้ใช้
4. **Return Rate** - อัตราการกลับมากรอกซ้ำ

---

## 6. Strategic Recommendations (CTO Insights)

### 6.1 Phase Rollout

**Phase 1: Foundation (Week 1-2)**
- Create multi-step form hook
- Implement basic step navigation
- Add progress indicators
- Setup form validation

**Phase 2: Advanced Features (Week 3-4)**
- Implement auto-save
- Add form persistence
- Create conditional steps
- Implement async validation

**Phase 3: Optimization (Week 5-6)**
- Performance audit
- Accessibility testing
- Error handling improvement
- Mobile optimization

**Phase 4: Production (Week 7-8)**
- Analytics integration
- A/B testing
- Documentation and training
- Component library

### 6.2 Pitfalls to Avoid

1. **Lost Data** - ไม่ implement persistence
2. **Confusing Navigation** - Progress indicators ที่ไม่ชัดเจน
3. **Validation Timing** - Validate ไม่ถูกจังหวะ
4. **Performance** - ไม่ optimize re-renders
5. **Accessibility** - ลืม keyboard navigation
6. **Poor UX** - Steps ที่ยาวเกินไป

### 6.3 Best Practices Checklist

- [ ] ใช้ progress indicators ที่ชัดเจน
- [ ] Implement per-step validation
- [ ] ใช้ form persistence สำหรับ auto-save
- [ ] อนุญาตให้ navigate กลับไป steps ก่อนหน้า
- [ ] ใช้ appropriate validation timing
- [ ] Lazy load step components
- [ ] Debounce auto-save
- [ ] Optimize validation
- [ ] Cache validation results
- [ ] Implement keyboard navigation
- [ ] Add screen reader support
- [ ] Manage focus properly
- [ ] Announce errors to screen readers
- [ ] Test บน mobile devices
- [ ] Implement conditional steps

---

## 7. Implementation Examples

### 7.1 Form State Management

**React Hook for Multi-Step Forms:**
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

**Form Container Component:**
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

### 7.2 Progress Indicators

**Step Progress Component:**
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

**Circular Progress:**
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

### 7.3 Form Validation

**Per-Step Validation:**
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

**Async Validation:**
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

### 7.4 Form Persistence

**Local Storage Persistence:**
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

**Auto-Save Feature:**
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

### 7.5 Conditional Steps

**Dynamic Step Flow:**
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

### 7.6 Complete Example: Event Creation Form

**Event Creation Wizard:**
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
```

### 7.7 Best Practices

**User Experience:**
- Show clear progress indicators
- Allow navigation to previous steps
- Provide save/draft functionality
- Use appropriate validation timing

**Performance:**
- Lazy load step components
- Debounce auto-save
- Optimize validation
- Cache validation results

**Accessibility:**
- Keyboard navigation
- Screen reader support
- Focus management
- Error announcements

**Data Management:**
- Persist form state
- Handle browser refresh
- Implement auto-save
- Validate before transitions

**Error Handling:**
- Clear error messages
- Field-level validation
- Step-level validation
- Global validation

---

## 8. Related Skills

- `02-frontend/form-handling`
- `02-frontend/react-best-practices`
- `02-frontend/state-management`
- `22-ux-ui-design/user-research`
- `16-testing`
