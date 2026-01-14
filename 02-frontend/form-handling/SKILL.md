# Form Handling with React Hook Form + Zod

## Overview
Type-safe form validation และ state management

## Setup
```typescript
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
```

## Validation Schema Patterns

### Basic Schema
```typescript
const userSchema = z.object({
  email: z.string().email("Invalid email format"),
  password: z.string().min(8, "Password must be at least 8 characters"),
  age: z.number().min(18).max(100),
  terms: z.boolean().refine((val) => val === true, {
    message: "You must accept terms",
  }),
})

type UserFormData = z.infer<typeof userSchema>
```

### Advanced Validation
```typescript
const profileSchema = z.object({
  username: z.string()
    .min(3)
    .max(20)
    .regex(/^[a-zA-Z0-9_]+$/, "Only alphanumeric and underscore"),
  
  password: z.string().min(8),
  confirmPassword: z.string(),
  
  phone: z.string()
    .regex(/^\+?[1-9]\d{1,14}$/, "Invalid phone number"),
  
  website: z.string()
    .url()
    .optional()
    .or(z.literal("")),
    
  dateOfBirth: z.date()
    .max(new Date(), "Date of birth cannot be in the future"),
    
  tags: z.array(z.string()).min(1, "Select at least one tag"),
  
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
})
```

## Form Implementation

### Basic Form
```typescript
function UserForm() {
  const form = useForm<UserFormData>({
    resolver: zodResolver(userSchema),
    defaultValues: {
      email: "",
      password: "",
      age: 18,
      terms: false,
    },
  })

  const onSubmit = async (data: UserFormData) => {
    try {
      await createUser(data)
      toast.success("User created!")
    } catch (error) {
      toast.error("Failed to create user")
    }
  }

  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      <input {...form.register("email")} />
      {form.formState.errors.email && (
        <span>{form.formState.errors.email.message}</span>
      )}
      
      <button type="submit" disabled={form.formState.isSubmitting}>
        {form.formState.isSubmitting ? "Submitting..." : "Submit"}
      </button>
    </form>
  )
}
```

### Multi-step Form
```typescript
const steps = [
  z.object({ step1Field: z.string() }),
  z.object({ step2Field: z.number() }),
  z.object({ step3Field: z.boolean() }),
]

function MultiStepForm() {
  const [step, setStep] = useState(0)
  const currentSchema = steps[step]
  
  const form = useForm({
    resolver: zodResolver(currentSchema),
  })
  
  const onNext = async (data: any) => {
    if (step < steps.length - 1) {
      setStep(step + 1)
    } else {
      await submitForm(data)
    }
  }
}
```

### Dynamic Fields
```typescript
const { fields, append, remove } = useFieldArray({
  control: form.control,
  name: "items",
})

return (
  <>
    {fields.map((field, index) => (
      <div key={field.id}>
        <input {...form.register(`items.${index}.name`)} />
        <button onClick={() => remove(index)}>Remove</button>
      </div>
    ))}
    <button onClick={() => append({ name: "" })}>Add Item</button>
  </>
)
```

## Error Handling Patterns
- Field-level errors
- Form-level errors
- Server-side errors
- Async validation

## Performance Optimization
- Use `mode: "onBlur"` for validation
- Debounce async validation
- Memoize heavy computations