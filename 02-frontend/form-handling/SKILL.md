# Form Handling with React Hook Form and Zod

---

## 1. Executive Summary & Strategic Necessity

### 1.1 Context (ภาษาไทย)

การจัดการฟอร์ม (Form Handling) เป็นส่วนสำคัญในการพัฒนาแอปพลิเคชันเว็บที่ต้องการรับข้อมูลจากผู้ใช้ React Hook Form และ Zod เป็น combination ที่ทรงพลังสำหรับการจัดการฟอร์มใน React โดย React Hook Form ช่วยลด re-renders และปรับปรุงประสิทธิภาพ ในขณะที่ Zod ให้การ validation ที่ปลอดภัยและ type-safe

Skill นี้ครอบคลุมการใช้งาน React Hook Form และ Zod สำหรับการสร้างฟอร์มที่มีประสิทธิภาพสูง validation ที่ครบถ้วน และประสบการณ์ผู้ใช้ที่ดี รวมถึงการจัดการ errors, async validation, dynamic fields, และการรวมกับ UI libraries

### 1.2 Business Impact (ภาษาไทย)

**ผลกระทบทางธุรกิจ:**

1. **เพิ่ม Conversion Rate** - ฟอร์มที่ใช้งานง่ายและมี validation ที่ชัดเจนช่วยเพิ่ม conversion rate ได้ถึง 20-30%

2. **ลด Form Abandonment** - Validation แบบ real-time และ error messages ที่ชัดเจนช่วยลดจำนวนผู้ใช้ที่ละทิ้งฟอร์มระหว่างกรอกข้อมูล

3. **ปรับปรุง Data Quality** - Validation ที่เข้มงวดช่วยลดข้อมูลที่ไม่ถูกต้องและลดเวลาในการ data cleaning

4. **ลด Support Cost** - Error messages ที่ชัดเจนและใช้งานง่ายช่วยลดคำถามและปัญหาจากผู้ใช้

5. **เพิ่ม User Satisfaction** - ฟอร์มที่ใช้งานง่ายและตอบสนองไวช่วยสร้างความพึงพอใจในการใช้งาน

### 1.3 Product Thinking (ภาษาไทย)

**มุมมองด้านผลิตภัณฑ์:**

1. **User-Centric Validation** - Validation ต้องเป็นประโยชน์ต่อผู้ใช้ ไม่ใช่แค่การป้องกันข้อมูลที่ไม่ถูกต้อง

2. **Progressive Enhancement** - ฟอร์มต้องทำงานได้ดีในทุก browsers และ devices

3. **Accessibility** - ฟอร์มต้องเข้าถึงได้และใช้งานได้สำหรับผู้ใช้ทุกคน

4. **Performance** - ฟอร์มต้องไม่ส่งผลกระทบต่อประสิทธิภาพของแอปพลิเคชัน

5. **Consistent Experience** - ฟอร์มต้องมีประสบการณ์ที่สอดคล้องกันทั่วทั้งแอปพลิเคชัน

---

## 2. Technical Deep Dive (The "How-to")

### 2.1 Core Logic

React Hook Form และ Zod ทำงานร่วมกันเพื่อสร้างฟอร์มที่มีประสิทธิภาพสูง:

1. **React Hook Form** - จัดการ form state, validation, และ submission โดยลด re-renders
2. **Zod** - ให้ schema validation ที่ type-safe และยืดหยุ่น
3. **@hookform/resolvers/zod** - เชื่อมต่อ Zod schemas กับ React Hook Form

### 2.2 Architecture Diagram Requirements

```
┌─────────────────────────────────────────────────────────────────┐
│                    Form Architecture                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │              Form Component Layer                         │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │   Login     │  │  Register   │  │  Profile  │  │   │
│  │  │   Form      │  │   Form      │  │   Form    │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────────────┘   │
│                           │                                     │
│                           │                                     │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │              React Hook Form Layer                      │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │   useForm   │  │useFieldArray│  │Controller │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  │  ┌─────────────────────────────────────────────────┐    │   │
│  │  │         Form State Management               │    │   │
│  │  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  │    │   │
│  │  │  │ errors  │  │ touched │  │  dirty  │  │    │   │
│  │  │  └─────────┘  └─────────┘  └─────────┘  │    │   │
│  │  └─────────────────────────────────────────────────┘    │   │
│  └───────────────────────────────────────────────────────────┘   │
│                           │                                     │
│                           │                                     │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │              Validation Layer                            │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │    Zod     │  │  Zod       │  │  Custom   │  │   │
│  │  │   Schema    │  │  Resolver   │  │ Validators│  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  │  ┌─────────────────────────────────────────────────┐    │   │
│  │  │         Validation Types                   │    │   │
│  │  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  │    │   │
│  │  │  │  Sync   │  │  Async  │  │  Server │  │    │   │
│  │  │  └─────────┘  └─────────┘  └─────────┘  │    │   │
│  │  └─────────────────────────────────────────────────┘    │   │
│  └───────────────────────────────────────────────────────────┘   │
│                           │                                     │
│                           │                                     │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │              UI Integration Layer                        │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  shadcn/ui  │  │Material-UI │  │   Custom  │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.3 Implementation Workflow

**Step 1: Setup Dependencies**

```bash
# Install dependencies
npm install react-hook-form @hookform/resolvers zod

# For TypeScript
npm install --save-dev @types/react-hook-form
```

**Step 2: Create Base Form Component**

```typescript
// components/BaseForm.tsx
"use client"

import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"

// Define schema
const formSchema = z.object({
  username: z.string().min(2, "Username must be at least 2 characters"),
  email: z.string().email("Invalid email address"),
})

type FormValues = z.infer<typeof formSchema>

export function BaseForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      username: "",
      email: "",
    },
  })

  const onSubmit = async (data: FormValues) => {
    try {
      const response = await fetch("/api/submit", {
        method: "POST",
        body: JSON.stringify(data),
      })
      // Handle response
    } catch (error) {
      console.error("Submission failed:", error)
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label htmlFor="username">Username</label>
        <input
          id="username"
          {...register("username")}
          className="border rounded px-3 py-2 w-full"
        />
        {errors.username && (
          <p className="text-red-500 text-sm">{errors.username.message}</p>
        )}
      </div>
      
      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          {...register("email")}
          className="border rounded px-3 py-2 w-full"
        />
        {errors.email && (
          <p className="text-red-500 text-sm">{errors.email.message}</p>
        )}
      </div>
      
      <button
        type="submit"
        disabled={isSubmitting}
        className="bg-blue-500 text-white px-4 py-2 rounded disabled:opacity-50"
      >
        {isSubmitting ? "Submitting..." : "Submit"}
      </button>
    </form>
  )
}
```

**Step 3: Create Validation Schemas**

```typescript
// schemas/formSchemas.ts
import * as z from "zod"

// Basic schema
export const basicSchema = z.object({
  name: z.string().min(1, "Name is required"),
  age: z.number().min(18, "Must be at least 18"),
  email: z.string().email("Invalid email"),
  url: z.string().url("Invalid URL"),
  phone: z.string().regex(/^[\d\s-()+]+$/, "Invalid phone number"),
})

// Advanced schema with custom validation
export const advancedSchema = z.object({
  password: z
    .string()
    .min(8, "Password must be at least 8 characters")
    .regex(/[A-Z]/, "Must contain uppercase letter")
    .regex(/[a-z]/, "Must contain lowercase letter")
    .regex(/[0-9]/, "Must contain number")
    .regex(/[^A-Za-z0-9]/, "Must contain special character"),
  
  confirmPassword: z.string(),
  
  birthDate: z
    .string()
    .refine((date) => {
      const birth = new Date(date)
      const minAge = new Date()
      minAge.setFullYear(minAge.getFullYear() - 18)
      return birth <= minAge
    }, "Must be at least 18 years old"),
  
  terms: z.literal(true, {
    errorMap: () => ({ message: "You must accept terms" }),
  }),
  
  bio: z.string().max(500, "Bio must be less than 500 characters").optional(),
  
  newsletter: z.boolean().optional(),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
})

// Nested object schema
export const addressSchema = z.object({
  street: z.string().min(1, "Street is required"),
  city: z.string().min(1, "City is required"),
  state: z.string().length(2, "State must be 2 characters"),
  zipCode: z.string().regex(/^\d{5}(-\d{4})?$/, "Invalid ZIP code"),
})

export const userSchema = z.object({
  name: z.string().min(1, "Name is required"),
  email: z.string().email("Invalid email"),
  address: addressSchema,
  workAddress: addressSchema.optional(),
})
```

---

## 3. Tooling & Tech Stack

### 3.1 Enterprise Tools

| Tool | Purpose | Version | License |
|------|---------|---------|---------|
| React Hook Form | Form State Management | ^7.0.0 | MIT |
| Zod | Schema Validation | ^3.0.0 | MIT |
| @hookform/resolvers | Resolver Integration | ^3.0.0 | MIT |
| React | UI Library | ^18.0.0 | MIT |
| TypeScript | Type Safety | ^5.0.0 | Apache 2.0 |

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

**ESLint Configuration:**
```json
// .eslintrc.json
{
  "extends": [
    "next/core-web-vitals",
    "plugin:@typescript-eslint/recommended"
  ],
  "rules": {
    "@typescript-eslint/no-unused-vars": "warn",
    "react-hooks/rules-of-hooks": "error",
    "react-hooks/exhaustive-deps": "warn"
  }
}
```

---

## 4. Standards, Compliance & Security

### 4.1 International Standards

- **WCAG 2.1 Level AA** - Forms ต้องเข้าถึงได้และใช้งานได้สำหรับผู้ใช้ทุกคน
- **ISO 9241-11** - Usability Standards สำหรับ Forms
- **GDPR** - Data Protection สำหรับ User Data

### 4.2 Security Protocol

Forms ต้องปฏิบัติตามหลักความปลอดภัย:

1. **Input Sanitization** - Sanitize user input ก่อนบันทึกหรือแสดง
2. **CSRF Protection** - ใช้ CSRF tokens สำหรับ form submissions
3. **Rate Limiting** - จำกัดจำนวน submissions ต่อผู้ใช้
4. **Secure Storage** - ไม่เก็บ sensitive data ใน localStorage

```typescript
// Secure form submission
export async function submitFormSecurely(data: any) {
  const csrfToken = getCsrfToken()
  
  const response = await fetch("/api/submit", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRF-Token": csrfToken,
    },
    body: JSON.stringify(sanitizeData(data)),
  })
  
  return response.json()
}

function sanitizeData(data: any): any {
  // Remove sensitive fields
  const { password, confirmPassword, ...sanitized } = data
  return sanitized
}
```

### 4.3 Explainability

Forms ต้องสามารถอธิบายได้ว่า:

1. **Validation Rules** - ทำไม input นี้ไม่ผ่าน validation
2. **Error Messages** - Error messages ต้องชัดเจนและเป็นประโยชน์
3. **Data Usage** - ข้อมูลที่รวบรวมจะถูกใช้อย่างไร
4. **Privacy Policy** - ความเป็นส่วนตัวของข้อมูล

---

## 5. Unit Economics & Performance Metrics (KPIs)

### 5.1 Cost Calculation

| Metric | Calculation | Target |
|--------|-------------|--------|
| Form Completion Rate | Completed Forms / Started Forms | > 70% |
| Validation Time | Time to validate form | < 100ms |
| Submission Time | Time to submit form | < 2s |
| Error Rate | Errors / Total Submissions | < 5% |
| Re-render Count | Re-renders per form interaction | < 5 |

### 5.2 Key Performance Indicators

**Technical Metrics:**

1. **Form Completion Rate** - อัตราการเสร็จสิ้นฟอร์ม
2. **Validation Performance** - เวลาในการ validate
3. **Submission Success Rate** - อัตราการส่งข้อมูลสำเร็จ
4. **Error Rate** - อัตราการเกิด errors

**Business Metrics:**

1. **Conversion Rate** - อัตราการแปลงผู้ใช้เป็นลูกค้า
2. **Form Abandonment Rate** - อัตราการละทิ้งฟอร์ม
3. **User Satisfaction** - ความพึงพอใจของผู้ใช้
4. **Data Quality** - คุณภาพของข้อมูลที่ได้รับ

---

## 6. Strategic Recommendations (CTO Insights)

### 6.1 Phase Rollout

**Phase 1: Foundation (Week 1-2)**
- Setup React Hook Form and Zod
- Create base form components
- Implement basic validation schemas
- Setup form state management

**Phase 2: Advanced Features (Week 3-4)**
- Implement async validation
- Add dynamic fields (useFieldArray)
- Create multi-step forms
- Add file upload support

**Phase 3: UI Integration (Week 5-6)**
- Integrate with UI libraries (shadcn/ui, Material-UI)
- Create reusable form components
- Implement form patterns (auto-save, confirmation)
- Add accessibility features

**Phase 4: Optimization (Week 7-8)**
- Performance audit
- Form analytics
- User feedback collection
- Documentation and training

### 6.2 Pitfalls to Avoid

1. **Over-Validation** - Validation มากเกินไปทำให้ผู้ใช้รำคาญ
2. **Poor Error Messages** - Error messages ที่ไม่ชัดเจนหรือไม่เป็นประโยชน์
3. **Ignoring Accessibility** - ไม่คำนึงถึง accessibility ในฟอร์ม
4. **Performance Issues** - Form ที่ช้าหรือมี re-renders มากเกินไป
5. **Security Vulnerabilities** - ไม่ sanitizing input หรือไม่มี CSRF protection

### 6.3 Best Practices Checklist

- [ ] ใช้ React Hook Form สำหรับ form state management
- [ ] ใช้ Zod สำหรับ schema validation
- [ ] ให้ error messages ที่ชัดเจนและเป็นประโยชน์
- [ ] Implement async validation สำหรับ unique constraints
- [ ] ใช้ debounce สำหรับ async validation
- [ ] คำนึงถึง accessibility ในฟอร์ม
- [ ] Sanitize user input ก่อนบันทึก
- [ ] ใช้ CSRF tokens สำหรับ form submissions
- [ ] Test forms บน browsers และ devices หลายแบบ
- [ ] Monitor form performance และ completion rates

---

## 7. Related Skills

- `02-frontend/react-best-practices`
- `02-frontend/state-management`
- `01-foundations/typescript-standards`
- `03-backend-api/validation`
- `02-frontend/shadcn-ui`
