# shadcn/ui Component Patterns

---

## 1. Executive Summary & Strategic Necessity

### 1.1 Context (ภาษาไทย)

shadcn/ui คือ collection ของ accessible React components ที่ built on Radix UI primitives และ styled ด้วย Tailwind CSS ซึ่งช่วยให้ developers สร้าง UI ที่ beautiful และ consistent ได้ง่ายขึ้น โดยไม่ต้องเริ่มจากศูนย์

shadcn/ui ใช้ Radix UI primitives สำหรับ accessibility และ keyboard navigation พร้อมกับ Tailwind CSS สำหรับ styling ที่ยืดหยุ่น และ components ที่ copy-paste ได้ง่าย

### 1.2 Business Impact (ภาษาไทย)

**ผลกระทบทางธุรกิจ:**

1. **ลด Development Time** - shadcn/ui ช่วยลดเวลาในการพัฒนา UI ได้ถึง 50-60%
2. **เพิ่ม Accessibility** - Built-in accessibility ช่วยเพิ่ม accessibility compliance
3. **ลด Maintenance Cost** - Component reuse และ consistent styling ช่วยลด maintenance
4. **เพิ่ม Design Consistency** - Consistent design system ช่วยเพิ่ม brand consistency
5. **ปรับปรุง User Experience** - Smooth animations และ interactions ช่วยเพิ่ม UX

### 1.3 Product Thinking (ภาษาไทย)

**มุมมองด้านผลิตภัณฑ์:**

1. **Design System** - shadcn/ui เป็น design system ที่สมบูรณ์พร้อมใช้งาน
2. **Accessibility-First** - Components มี accessibility ที่ดีตั้งแต่เริ่ม
3. **Customizable** - Components สามารถ customize ง่าย
4. **Performance-First** - Components ที่ optimized สำหรับ performance
5. **Developer-Friendly** - Easy to use และ integrate

---

## 2. Technical Deep Dive (The "How-to")

### 2.1 Core Logic

shadcn/ui ประกอบด้วย:

1. **Radix UI Primitives** - Low-level accessible components
2. **Tailwind CSS** - Utility-first CSS framework
3. **Component Composition** - Composable components
4. **TypeScript Support** - Full type safety
5. **Customization** - Easy to customize styles
6. **Copy-Paste** - Components ที่ copy-paste ได้ง่าย
7. **Accessibility** - Built-in keyboard navigation และ screen reader support

### 2.2 Architecture Diagram Requirements

```
┌─────────────────────────────────────────────────────────┐
│              shadcn/ui Architecture                    │
├─────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Primitives Layer                   │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  Radix UI   │  │  Dialog     │  │  Dropdown  │  │   │
│  │  │  Primitives │  │  Primitives │  │  Primitives│  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Component Layer                     │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  Form       │  │  Overlay    │  │  Data      │  │   │
│  │  │  Components │  │  Components │  │  Display   │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  Feedback   │  │  Navigation │  │  Layout    │  │   │
│  │  │  Components │  │  Components │  │  Components│  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Styling Layer                       │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  Tailwind   │  │  CSS        │  │  cn        │  │   │
│  │  │  Classes    │  │  Variables  │  │  Utility   │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Integration Layer                    │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  React Hook │  │  Zod        │  │  TanStack   │  │   │
│  │  │  Form       │  │  Validation │  │  Table     │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
└─────────────────────────────────────────────────────────┘
```

### 2.3 Implementation Workflow

**Step 1: Initialize shadcn/ui**

```bash
# Initialize shadcn/ui in your project
npx shadcn-ui@latest init

# Select options:
# - Which style would you like to use? › Default
# - Which color would you like to use as base color? › Slate
# - Would you like to use CSS variables for colors? › yes
```

**Step 2: Add Components**

```bash
# Add individual components
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add input
npx shadcn-ui@latest add dialog

# Add multiple components
npx shadcn-ui@latest add button card input label select

# Add all components
npx shadcn-ui@latest add --all
```

---

## 3. Tooling & Tech Stack

### 3.1 Enterprise Tools

| Tool | Purpose | Version | License |
|------|---------|---------|---------|
| Radix UI | Accessible Primitives | ^1.0.0 | MIT |
| Tailwind CSS | Styling Framework | ^3.0.0 | MIT |
| React Hook Form | Form Management | ^7.0.0 | MIT |
| Zod | Schema Validation | ^3.0.0 | MIT |
| TanStack Table | Data Table | ^8.0.0 | MIT |

### 3.2 Configuration Essentials

**Tailwind Configuration:**
```javascript
// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}
```

---

## 4. Standards, Compliance & Security

### 4.1 International Standards

- **WCAG 2.1 Level AA** - Components มี accessibility ที่ดี
- **WAI-ARIA** - Proper ARIA attributes
- **ISO 9241-11** - Usability Standards
- **GDPR** - Data Protection สำหรับ User Data

### 4.2 Security Protocol

shadcn/ui ต้องปฏิบัติตามหลักความปลอดภัย:

1. **XSS Prevention** - React escapes content โดย default
2. **Input Validation** - Validate ข้อมูลทั้ง client และ server
3. **Secure Storage** - ไม่เก็บ sensitive data ใน localStorage
4.4. **CSRF Protection** - ใช้ CSRF tokens สำหรับ forms

### 4.3 Explainability

shadcn/ui ต้องสามารถอธิบายได้ว่า:

1. **Component Behavior** - ทำไม component ทำงานอย่างไร
2. **Styling Approach** - ทำไมใช้ Tailwind classes อย่างไร
3. **Accessibility Features** - ทำไมมี accessibility features อย่างไร
4. **Customization** - ทำไมสามารถ customize อย่างไร

---

## 5. Unit Economics & Performance Metrics (KPIs)

### 5.1 Cost Calculation

| Metric | Calculation | Target |
|--------|-------------|--------|
| Component Render Time | Time per component render | < 16ms |
| Bundle Size | JavaScript bundle size | < 200 KB |
| Accessibility Score | WCAG compliance score | > 95% |
| Customization Time | Time to customize component | < 30 min |
| Integration Time | Time to integrate with app | < 1 hour |

### 5.2 Key Performance Indicators

**Technical Metrics:**

1. **Component Performance** - Render time ของ components
2. **Bundle Size** - JavaScript bundle ที่ใช้งาน
3. **Accessibility Score** - WCAG compliance score
4. **Customization Time** - เวลาในการ customize components

**Business Metrics:**

1. **Development Velocity** - เวลาในการพัฒนา features
2. **Design Consistency** - Consistency ของ UI ทั่วแอป
3. **User Experience** - User experience score
4. **Accessibility Compliance** - Accessibility compliance rate

---

## 6. Strategic Recommendations (CTO Insights)

### 6.1 Phase Rollout

**Phase 1: Foundation (Week 1-2)**
- Initialize shadcn/ui
- Setup Tailwind configuration
- Add base components
- Create design tokens

**Phase 2: Core Components (Week 3-4)**
- Add form components
- Implement overlay components
- Create data display components
- Setup navigation components

**Phase 3: Advanced Features (Week 5-6)**
- Integrate React Hook Form
- Add Zod validation
- Implement TanStack Table
- Create custom components

**Phase 4: Production (Week 7-8)**
- Performance optimization
- Accessibility audit
- Documentation and training
- Component library

### 6.2 Pitfalls to Avoid

1. **Over-customization** - ไม่ customize components มากเกินไป
2. **Poor Accessibility** - ไม่คำนึงถึง accessibility
3. **Bundle Bloat** - ไม่ optimize bundle size
4. **Inconsistent Styling** - ไม่ใช้ consistent styling
5. **Poor Type Safety** - ไม่ใช้ TypeScript อย่างเหมาะสม
6. **Performance Issues** - ไม่ optimize performance

### 6.3 Best Practices Checklist

- [ ] Initialize shadcn/ui อย่างถูกต้อง
- [ ] ใช้ Radix UI primitives สำหรับ accessibility
- [ ] Implement proper TypeScript types
- [ ] ใช้ cn utility สำหรับ conditional classes
- [ ] Extend components ไม่ modify originals
- [ ] คำนึงถึง accessibility ในทุก components
- [ ] Test บนทุก browsers และ devices
- [ ] Optimize bundle size
- [ ] Implement proper form validation
- [ ] ใช้ consistent styling
- [ ] Document custom components
- [ ] Test keyboard navigation
- [ ] Test with screen readers

---

## 7. Implementation Examples

### 7.1 Form Components

**Input Component:**
```typescript
// components/ui/input.tsx
import * as React from "react"
import { cn } from "@/lib/utils"

export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, ...props }, ref) => {
    return (
      <input
        type={type}
        className={cn(
          "flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
          className
        )}
        ref={ref}
        {...props}
      />
    )
  }
)
Input.displayName = "Input"

export { Input }
```

**Label Component:**
```typescript
// components/ui/label.tsx
import * as React from "react"
import { cn } from "@/lib/utils"

export interface LabelProps
  extends React.LabelHTMLAttributes<HTMLLabelElement> {}

const Label = React.forwardRef<HTMLLabelElement, LabelProps>(
  ({ className, ...props }, ref) => (
    <label
      ref={ref}
      className={cn(
        "text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70",
        className
      )}
      {...props}
    />
  )
)
Label.displayName = "Label"

export { Label }
```

### 7.2 Overlay Components

**Dialog Component:**
```typescript
// components/ui/dialog.tsx
import * as React from "react"
import * as DialogPrimitive from "@radix-ui/react-dialog"
import { X } from "lucide-react"
import { cn } from "@/lib/utils"

const Dialog = DialogPrimitive.Root
const DialogTrigger = DialogPrimitive.Trigger
const DialogPortal = DialogPrimitive.Portal
const DialogClose = DialogPrimitive.Close

const DialogOverlay = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Overlay>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Overlay>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Overlay
    ref={ref}
    className={cn(
      "fixed inset-0 z-50 bg-black/80 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0",
      className
    )}
    {...props}
  />
))
DialogOverlay.displayName = DialogPrimitive.Overlay.displayName

const DialogContent = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Content>
>(({ className, children, ...props }, ref) => (
  <DialogPortal>
    <DialogOverlay />
    <DialogPrimitive.Content
      ref={ref}
      className={cn(
        "fixed left-[50%] top-[50%] z-50 grid w-full max-w-lg translate-x-[-50%] translate-y-[-50%] gap-4 border bg-background p-6 shadow-lg duration-200 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%] data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%] sm:rounded-lg",
        className
      )}
      {...props}
    >
      {children}
      <DialogPrimitive.Close className="absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none data-[state=open]:bg-accent data-[state=open]:text-muted-foreground">
        <X className="h-4 w-4" />
        <span className="sr-only">Close</span>
      </DialogPrimitive.Close>
    </DialogPrimitive.Content>
  </DialogPortal>
))
DialogContent.displayName = DialogPrimitive.Content.displayName

const DialogHeader = ({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) => (
  <div
    className={cn(
      "flex flex-col space-y-1.5 text-center sm:text-left",
      className
    )}
    {...props}
  />
)
DialogHeader.displayName = "DialogHeader"

const DialogFooter = ({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) => (
  <div
    className={cn(
      "flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2",
      className
    )}
    {...props}
  />
)
DialogFooter.displayName = "DialogFooter"

const DialogTitle = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Title>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Title>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Title
    ref={ref}
    className={cn(
      "text-lg font-semibold leading-none tracking-tight",
      className
    )}
    {...props}
  />
))
DialogTitle.displayName = DialogPrimitive.Title.displayName

const DialogDescription = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Description>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Description>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Description
    ref={ref}
    className={cn("text-sm text-muted-foreground", className)}
    {...props}
  />
))
DialogDescription.displayName = DialogPrimitive.Description.displayName

export {
  Dialog,
  DialogPortal,
  DialogOverlay,
  DialogClose,
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogFooter,
  DialogTitle,
  DialogDescription,
}
```

### 7.3 Data Display Components

**Table Component:**
```typescript
// components/ui/table.tsx
import * as React from "react"
import { cn } from "@/lib/utils"

const Table = React.forwardRef<
  HTMLTableElement,
  React.HTMLAttributes<HTMLTableElement>
>(({ className, ...props }, ref) => (
  <div className="relative w-full overflow-auto">
    <table
      ref={ref}
      className={cn("w-full caption-bottom text-sm", className)}
      {...props}
    />
  </div>
))
Table.displayName = "Table"

const TableHeader = React.forwardRef<
  HTMLTableSectionElement,
  React.HTMLAttributes<HTMLTableSectionElement>
>(({ className, ...props }, ref) => (
  <thead ref={ref} className={cn("[&_tr]:border-b", className)} {...props} />
))
TableHeader.displayName = "TableHeader"

const TableBody = React.forwardRef<
  HTMLTableSectionElement,
  React.HTMLAttributes<HTMLTableSectionElement>
>(({ className, ...props }, ref) => (
  <tbody
    ref={ref}
    className={cn("[&_tr:last-child]:border-0", className)}
    {...props}
  />
))
TableBody.displayName = "TableBody"

const TableRow = React.forwardRef<
  HTMLTableRowElement,
  React.HTMLAttributes<HTMLTableRowElement>
>(({ className, ...props }, ref) => (
  <tr
    ref={ref}
    className={cn(
      "border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted",
      className
    )}
    {...props}
  />
))
TableRow.displayName = "TableRow"

const TableHead = React.forwardRef<
  HTMLTableCellElement,
  React.ThHTMLAttributes<HTMLTableCellElement>
>(({ className, ...props }, ref) => (
  <th
    ref={ref}
    className={cn(
      "h-10 px-2 text-left align-middle font-medium text-muted-foreground [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-[2px]",
      className
    )}
    {...props}
  />
))
TableHead.displayName = "TableHead"

const TableCell = React.forwardRef<
  HTMLTableCellElement,
  React.TdHTMLAttributes<HTMLTableCellElement>
>(({ className, ...props }, ref) => (
  <td
    ref={ref}
    className={cn(
      "p-2 align-middle [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-[2px]",
      className
    )}
    {...props}
  />
))
TableCell.displayName = "TableCell"

export {
  Table,
  TableHeader,
  TableBody,
  TableHead,
  TableRow,
  TableCell,
}
```

### 7.4 Navigation Components

**Tabs Component:**
```typescript
// components/ui/tabs.tsx
import * as React from "react"
import * as TabsPrimitive from "@radix-ui/react-tabs"
import { cn } from "@/lib/utils"

const Tabs = TabsPrimitive.Root
const TabsList = React.forwardRef<
  React.ElementRef<typeof TabsPrimitive.List>,
  React.ComponentPropsWithoutRef<typeof TabsPrimitive.List>
>(({ className, ...props }, ref) => (
  <TabsPrimitive.List
    ref={ref}
    className={cn(
      "inline-flex h-10 items-center justify-center rounded-md bg-muted p-1 text-muted-foreground",
      className
    )}
    {...props}
  />
))
TabsList.displayName = TabsPrimitive.List.displayName

const TabsTrigger = React.forwardRef<
  React.ElementRef<typeof TabsPrimitive.Trigger>,
  React.ComponentPropsWithoutRef<typeof TabsPrimitive.Trigger>
>(({ className, ...props }, ref) => (
  <TabsPrimitive.Trigger
    ref={ref}
    className={cn(
      "inline-flex items-center justify-center whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 data-[state=active]:bg-background data-[state=active]:text-foreground data-[state=active]:shadow-sm",
      className
    )}
    {...props}
  />
))
TabsTrigger.displayName = TabsPrimitive.Trigger.displayName

const TabsContent = React.forwardRef<
  React.ElementRef<typeof TabsPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof TabsPrimitive.Content>
>(({ className, ...props }, ref) => (
  <TabsPrimitive.Content
    ref={ref}
    className={cn(
      "mt-2 ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
      className
    )}
    {...props}
  />
))
TabsContent.displayName = TabsPrimitive.Content.displayName

export { Tabs, TabsList, TabsTrigger, TabsContent }
```

### 7.5 Composition Patterns

**Form with Validation (React Hook Form + Zod):**
```typescript
// lib/validations/user.ts
import { z } from "zod"

export const userFormSchema = z.object({
  username: z
    .string()
    .min(2, "Username must be at least 2 characters")
    .max(20, "Username must be at most 20 characters"),
  email: z.string().email("Invalid email address"),
  password: z
    .string()
    .min(8, "Password must be at least 8 characters")
    .regex(/[A-Z]/, "Password must contain at least one uppercase letter")
    .regex(/[0-9]/, "Password must contain at least one number"),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
}))

export type UserFormValues = z.infer<typeof userFormSchema>
```

**Custom Variants:**
```typescript
// Using class-variance-authority for variants
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const cardVariants = cva(
  "rounded-lg border bg-card text-card-foreground shadow-sm",
  {
    variants: {
      variant: {
        default: "border-border",
        elevated: "border-border shadow-md",
        outlined: "border-2",
        filled: "bg-muted border-transparent",
      },
      size: {
        sm: "p-4",
        default: "p-6",
        lg: "p-8",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

interface CardProps extends VariantProps<typeof cardVariants> {
  className?: string
  children: React.ReactNode
}

export function Card({ variant, size, className, children }: CardProps) {
  return (
    <div className={cn(cardVariants({ variant, size }), className)}>
      {children}
    </div>
  )
}
```

### 7.6 Best Practices

**Component Design:**
- Use Radix UI primitives for accessibility
- Implement proper TypeScript types
- Create reusable components
- Use composition patterns

**Styling:**
- Use Tailwind CSS for styling
- Use cn utility for conditional classes
- Implement CSS variables for theming
- Keep components small and composable

**Accessibility:**
- Test keyboard navigation
- Test with screen readers
- Implement proper ARIA attributes
- Ensure focus management

**Performance:**
- Optimize bundle size
- Use dynamic imports for heavy components
- Implement proper memoization
- Test performance metrics

---

## 8. Related Skills

- `02-frontend/react-best-practices`
- `02-frontend/mui-material`
- `02-frontend/form-handling`
- `22-ux-ui-design/design-systems`
- `22-ux-ui-design/accessibility`
