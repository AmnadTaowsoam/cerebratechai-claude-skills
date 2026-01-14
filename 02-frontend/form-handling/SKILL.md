# Form Handling with React Hook Form and Zod

## 1. Setup (React Hook Form + Zod)

### Installation
```bash
# Install dependencies
npm install react-hook-form @hookform/resolvers zod

# For TypeScript
npm install --save-dev @types/react-hook-form
```

### Basic Setup
```typescript
// components/basic-form.tsx
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

export function BasicForm() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormValues>({
    resolver: zodResolver(formSchema),
  })

  const onSubmit = (data: FormValues) => {
    console.log(data)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <label>Username</label>
        <input {...register("username")} />
        {errors.username && <span>{errors.username.message}</span>}
      </div>
      
      <div>
        <label>Email</label>
        <input type="email" {...register("email")} />
        {errors.email && <span>{errors.email.message}</span>}
      </div>
      
      <button type="submit">Submit</button>
    </form>
  )
}
```

## 2. Validation Schemas

### Basic Schema
```typescript
import { z } from "zod"

const basicSchema = z.object({
  name: z.string().min(1, "Name is required"),
  age: z.number().min(18, "Must be at least 18"),
  email: z.string().email("Invalid email"),
  url: z.string().url("Invalid URL"),
  phone: z.string().regex(/^[\d\s-()+]+$/, "Invalid phone number"),
})

type BasicSchemaType = z.infer<typeof basicSchema>
```

### Advanced Validation
```typescript
const advancedSchema = z.object({
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
    errorMap: () => ({ message: "You must accept the terms" }),
  }),
  
  bio: z.string().max(500, "Bio must be less than 500 characters").optional(),
  
  newsletter: z.boolean().optional(),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
})

type AdvancedSchemaType = z.infer<typeof advancedSchema>
```

### Nested Objects
```typescript
const addressSchema = z.object({
  street: z.string().min(1, "Street is required"),
  city: z.string().min(1, "City is required"),
  state: z.string().length(2, "State must be 2 characters"),
  zipCode: z.string().regex(/^\d{5}(-\d{4})?$/, "Invalid ZIP code"),
})

const userSchema = z.object({
  name: z.string().min(1, "Name is required"),
  email: z.string().email("Invalid email"),
  address: addressSchema,
  workAddress: addressSchema.optional(),
})

type UserSchemaType = z.infer<typeof userSchema>
```

### Arrays
```typescript
const todoSchema = z.object({
  id: z.string(),
  text: z.string().min(1, "Todo text is required"),
  completed: z.boolean().default(false),
})

const todoListSchema = z.object({
  title: z.string().min(1, "Title is required"),
  todos: z.array(todoSchema).min(1, "At least one todo is required"),
})

type TodoListSchemaType = z.infer<typeof todoListSchema>
```

### Custom Validators
```typescript
const customSchema = z.object({
  username: z
    .string()
    .min(3, "Username must be at least 3 characters")
    .max(20, "Username must be at most 20 characters")
    .regex(/^[a-zA-Z0-9_]+$/, "Only letters, numbers, and underscores"),
  
  email: z
    .string()
    .email("Invalid email")
    .refine(async (email) => {
      // Async validation - check if email exists
      const exists = await checkEmailExists(email)
      return !exists
    }, "Email already registered"),
  
  password: z
    .string()
    .min(8, "Password must be at least 8 characters")
    .refine((password) => {
      // Custom validation logic
      const hasUpperCase = /[A-Z]/.test(password)
      const hasLowerCase = /[a-z]/.test(password)
      const hasNumber = /[0-9]/.test(password)
      return hasUpperCase && hasLowerCase && hasNumber
    }, "Password must contain uppercase, lowercase, and number"),
  
  discountCode: z
    .string()
    .optional()
    .refine(async (code) => {
      if (!code) return true
      const valid = await validateDiscountCode(code)
      return valid
    }, "Invalid discount code"),
})

// Helper function for async validation
async function checkEmailExists(email: string): Promise<boolean> {
  const response = await fetch(`/api/check-email?email=${email}`)
  const data = await response.json()
  return data.exists
}

async function validateDiscountCode(code: string): Promise<boolean> {
  const response = await fetch(`/api/validate-code?code=${code}`)
  const data = await response.json()
  return data.valid
}
```

## 3. Form Implementation

### Basic Form
```typescript
"use client"

import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"

const loginSchema = z.object({
  email: z.string().email("Invalid email"),
  password: z.string().min(6, "Password must be at least 6 characters"),
})

type LoginValues = z.infer<typeof loginSchema>

export function LoginForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginValues>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: "",
      password: "",
    },
  })

  const onSubmit = async (data: LoginValues) => {
    try {
      const response = await fetch("/api/login", {
        method: "POST",
        body: JSON.stringify(data),
      })
      // Handle response
    } catch (error) {
      console.error("Login failed:", error)
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
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
      
      <div>
        <label htmlFor="password">Password</label>
        <input
          id="password"
          type="password"
          {...register("password")}
          className="border rounded px-3 py-2 w-full"
        />
        {errors.password && (
          <p className="text-red-500 text-sm">{errors.password.message}</p>
        )}
      </div>
      
      <button
        type="submit"
        disabled={isSubmitting}
        className="bg-blue-500 text-white px-4 py-2 rounded disabled:opacity-50"
      >
        {isSubmitting ? "Logging in..." : "Login"}
      </button>
    </form>
  )
}
```

### Multi-step Form
```typescript
"use client"

import { useForm, FormProvider } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { useState } from "react"

const personalInfoSchema = z.object({
  firstName: z.string().min(1, "First name is required"),
  lastName: z.string().min(1, "Last name is required"),
  email: z.string().email("Invalid email"),
})

const addressSchema = z.object({
  street: z.string().min(1, "Street is required"),
  city: z.string().min(1, "City is required"),
  zipCode: z.string().regex(/^\d{5}$/, "Invalid ZIP code"),
})

const completeSchema = personalInfoSchema.merge(addressSchema)

type CompleteFormValues = z.infer<typeof completeSchema>

function Step1() {
  const { register, formState: { errors } } = useFormContext<CompleteFormValues>()
  
  return (
    <div className="space-y-4">
      <div>
        <label>First Name</label>
        <input {...register("firstName")} className="border rounded px-3 py-2 w-full" />
        {errors.firstName && <p className="text-red-500">{errors.firstName.message}</p>}
      </div>
      <div>
        <label>Last Name</label>
        <input {...register("lastName")} className="border rounded px-3 py-2 w-full" />
        {errors.lastName && <p className="text-red-500">{errors.lastName.message}</p>}
      </div>
      <div>
        <label>Email</label>
        <input type="email" {...register("email")} className="border rounded px-3 py-2 w-full" />
        {errors.email && <p className="text-red-500">{errors.email.message}</p>}
      </div>
    </div>
  )
}

function Step2() {
  const { register, formState: { errors } } = useFormContext<CompleteFormValues>()
  
  return (
    <div className="space-y-4">
      <div>
        <label>Street</label>
        <input {...register("street")} className="border rounded px-3 py-2 w-full" />
        {errors.street && <p className="text-red-500">{errors.street.message}</p>}
      </div>
      <div>
        <label>City</label>
        <input {...register("city")} className="border rounded px-3 py-2 w-full" />
        {errors.city && <p className="text-red-500">{errors.city.message}</p>}
      </div>
      <div>
        <label>ZIP Code</label>
        <input {...register("zipCode")} className="border rounded px-3 py-2 w-full" />
        {errors.zipCode && <p className="text-red-500">{errors.zipCode.message}</p>}
      </div>
    </div>
  )
}

export function MultiStepForm() {
  const [step, setStep] = useState(1)
  const methods = useForm<CompleteFormValues>({
    resolver: zodResolver(completeSchema),
    defaultValues: {
      firstName: "",
      lastName: "",
      email: "",
      street: "",
      city: "",
      zipCode: "",
    },
  })

  const onSubmit = async (data: CompleteFormValues) => {
    console.log("Form submitted:", data)
    // Submit to API
  }

  const nextStep = async () => {
    const valid = await methods.trigger(
      step === 1 ? ["firstName", "lastName", "email"] : ["street", "city", "zipCode"]
    )
    if (valid) setStep(step + 1)
  }

  const prevStep = () => setStep(step - 1)

  return (
    <FormProvider {...methods}>
      <form onSubmit={methods.handleSubmit(onSubmit)}>
        {step === 1 && <Step1 />}
        {step === 2 && <Step2 />}
        
        <div className="mt-4 flex gap-2">
          {step > 1 && (
            <button type="button" onClick={prevStep} className="px-4 py-2 border rounded">
              Previous
            </button>
          )}
          {step < 2 ? (
            <button type="button" onClick={nextStep} className="px-4 py-2 bg-blue-500 text-white rounded">
              Next
            </button>
          ) : (
            <button type="submit" className="px-4 py-2 bg-green-500 text-white rounded">
              Submit
            </button>
          )}
        </div>
      </form>
    </FormProvider>
  )
}
```

### Dynamic Fields (useFieldArray)
```typescript
"use client"

import { useForm, useFieldArray } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"

const itemSchema = z.object({
  name: z.string().min(1, "Item name is required"),
  quantity: z.number().min(1, "Quantity must be at least 1"),
  price: z.number().min(0, "Price must be positive"),
})

const invoiceSchema = z.object({
  invoiceNumber: z.string().min(1, "Invoice number is required"),
  items: z.array(itemSchema).min(1, "At least one item is required"),
})

type InvoiceValues = z.infer<typeof invoiceSchema>

export function InvoiceForm() {
  const { register, control, handleSubmit } = useForm<InvoiceValues>({
    resolver: zodResolver(invoiceSchema),
    defaultValues: {
      invoiceNumber: "",
      items: [{ name: "", quantity: 1, price: 0 }],
    },
  })

  const { fields, append, remove } = useFieldArray({
    control,
    name: "items",
  })

  const onSubmit = (data: InvoiceValues) => {
    console.log(data)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <div>
        <label>Invoice Number</label>
        <input {...register("invoiceNumber")} className="border rounded px-3 py-2 w-full" />
      </div>

      <div className="space-y-4">
        <h3 className="font-semibold">Items</h3>
        {fields.map((field, index) => (
          <div key={field.id} className="flex gap-2 items-start">
            <div className="flex-1">
              <input
                {...register(`items.${index}.name`)}
                placeholder="Item name"
                className="border rounded px-3 py-2 w-full"
              />
            </div>
            <div className="w-24">
              <input
                type="number"
                {...register(`items.${index}.quantity`, { valueAsNumber: true })}
                placeholder="Qty"
                className="border rounded px-3 py-2 w-full"
              />
            </div>
            <div className="w-32">
              <input
                type="number"
                step="0.01"
                {...register(`items.${index}.price`, { valueAsNumber: true })}
                placeholder="Price"
                className="border rounded px-3 py-2 w-full"
              />
            </div>
            <button
              type="button"
              onClick={() => remove(index)}
              className="px-3 py-2 bg-red-500 text-white rounded"
            >
              Remove
            </button>
          </div>
        ))}
        <button
          type="button"
          onClick={() => append({ name: "", quantity: 1, price: 0 })}
          className="px-4 py-2 bg-blue-500 text-white rounded"
        >
          Add Item
        </button>
      </div>

      <button type="submit" className="px-6 py-2 bg-green-500 text-white rounded">
        Create Invoice
      </button>
    </form>
  )
}
```

### File Uploads
```typescript
"use client"

import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"

const MAX_FILE_SIZE = 5 * 1024 * 1024 // 5MB
const ACCEPTED_IMAGE_TYPES = ["image/jpeg", "image/jpg", "image/png", "image/webp"]

const fileSchema = z
  .instanceof(File)
  .refine((file) => file.size <= MAX_FILE_SIZE, "Max file size is 5MB")
  .refine(
    (file) => ACCEPTED_IMAGE_TYPES.includes(file.type),
    "Only .jpg, .jpeg, .png and .webp formats are supported"
  )

const uploadSchema = z.object({
  name: z.string().min(1, "Name is required"),
  avatar: fileSchema.optional(),
  documents: z.array(fileSchema).max(5, "Maximum 5 documents"),
})

type UploadValues = z.infer<typeof uploadSchema>

export function FileUploadForm() {
  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
  } = useForm<UploadValues>({
    resolver: zodResolver(uploadSchema),
  })

  const avatarFile = watch("avatar")

  const onSubmit = async (data: UploadValues) => {
    const formData = new FormData()
    formData.append("name", data.name)
    
    if (data.avatar) {
      formData.append("avatar", data.avatar)
    }
    
    data.documents.forEach((file, index) => {
      formData.append(`document-${index}`, file)
    })

    try {
      const response = await fetch("/api/upload", {
        method: "POST",
        body: formData,
      })
      // Handle response
    } catch (error) {
      console.error("Upload failed:", error)
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <div>
        <label htmlFor="name">Name</label>
        <input
          id="name"
          {...register("name")}
          className="border rounded px-3 py-2 w-full"
        />
        {errors.name && <p className="text-red-500">{errors.name.message}</p>}
      </div>

      <div>
        <label htmlFor="avatar">Avatar</label>
        <input
          id="avatar"
          type="file"
          accept="image/*"
          {...register("avatar")}
          className="border rounded px-3 py-2 w-full"
        />
        {errors.avatar && <p className="text-red-500">{errors.avatar.message}</p>}
        {avatarFile && (
          <div className="mt-2">
            <img
              src={URL.createObjectURL(avatarFile)}
              alt="Preview"
              className="w-20 h-20 object-cover rounded"
            />
          </div>
        )}
      </div>

      <div>
        <label htmlFor="documents">Documents (max 5)</label>
        <input
          id="documents"
          type="file"
          multiple
          accept=".pdf,.doc,.docx"
          {...register("documents")}
          className="border rounded px-3 py-2 w-full"
        />
        {errors.documents && <p className="text-red-500">{errors.documents.message}</p>}
      </div>

      <button type="submit" className="px-6 py-2 bg-blue-500 text-white rounded">
        Upload
      </button>
    </form>
  )
}
```

## 4. Error Handling

### Field-level Errors
```typescript
"use client"

import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"

const schema = z.object({
  username: z.string().min(3, "Username must be at least 3 characters"),
  email: z.string().email("Invalid email"),
})

type SchemaValues = z.infer<typeof schema>

export function FieldErrorsForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, touchedFields, dirtyFields },
  } = useForm<SchemaValues>({
    resolver: zodResolver(schema),
  })

  return (
    <form onSubmit={handleSubmit(console.log)} className="space-y-4">
      <div>
        <label>Username</label>
        <input
          {...register("username")}
          className={`border rounded px-3 py-2 w-full ${
            errors.username ? "border-red-500" : "border-gray-300"
          }`}
        />
        {errors.username && (
          <p className="text-red-500 text-sm">{errors.username.message}</p>
        )}
        {touchedFields.username && !errors.username && (
          <p className="text-green-500 text-sm">Username looks good!</p>
        )}
      </div>

      <div>
        <label>Email</label>
        <input
          type="email"
          {...register("email")}
          className={`border rounded px-3 py-2 w-full ${
            errors.email ? "border-red-500" : "border-gray-300"
          }`}
        />
        {errors.email && (
          <p className="text-red-500 text-sm">{errors.email.message}</p>
        )}
      </div>

      <button type="submit" className="px-4 py-2 bg-blue-500 text-white rounded">
        Submit
      </button>
    </form>
  )
}
```

### Form-level Errors
```typescript
"use client"

import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"

const schema = z.object({
  email: z.string().email("Invalid email"),
  password: z.string().min(6, "Password must be at least 6 characters"),
})

type SchemaValues = z.infer<typeof schema>

export function FormLevelErrorsForm() {
  const {
    register,
    handleSubmit,
    setError,
    clearErrors,
    formState: { errors },
  } = useForm<SchemaValues>({
    resolver: zodResolver(schema),
  })

  const onSubmit = async (data: SchemaValues) => {
    clearErrors()
    
    try {
      const response = await fetch("/api/login", {
        method: "POST",
        body: JSON.stringify(data),
      })
      
      if (!response.ok) {
        const errorData = await response.json()
        
        // Set form-level error
        setError("root", {
          type: "manual",
          message: errorData.message || "Login failed",
        })
        
        // Or set field-level error from server
        if (errorData.field === "email") {
          setError("email", {
            type: "manual",
            message: errorData.message,
          })
        }
      }
    } catch (error) {
      setError("root", {
        type: "manual",
        message: "Network error. Please try again.",
      })
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      {errors.root && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {errors.root.message}
        </div>
      )}

      <div>
        <label>Email</label>
        <input {...register("email")} className="border rounded px-3 py-2 w-full" />
        {errors.email && <p className="text-red-500">{errors.email.message}</p>}
      </div>

      <div>
        <label>Password</label>
        <input type="password" {...register("password")} className="border rounded px-3 py-2 w-full" />
        {errors.password && <p className="text-red-500">{errors.password.message}</p>}
      </div>

      <button type="submit" className="px-4 py-2 bg-blue-500 text-white rounded">
        Login
      </button>
    </form>
  )
}
```

### Server-side Errors
```typescript
"use client"

import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"

const schema = z.object({
  email: z.string().email("Invalid email"),
  password: z.string().min(6, "Password must be at least 6 characters"),
})

type SchemaValues = z.infer<typeof schema>

interface ServerError {
  field?: string
  message: string
  code?: string
}

export function ServerErrorsForm() {
  const {
    register,
    handleSubmit,
    setError,
    formState: { errors, isSubmitting },
  } = useForm<SchemaValues>({
    resolver: zodResolver(schema),
  })

  const handleServerErrors = (serverErrors: ServerError[]) => {
    serverErrors.forEach((error) => {
      if (error.field) {
        setError(error.field as keyof SchemaValues, {
          type: "server",
          message: error.message,
        })
      }
    })
  }

  const onSubmit = async (data: SchemaValues) => {
    try {
      const response = await fetch("/api/register", {
        method: "POST",
        body: JSON.stringify(data),
        headers: { "Content-Type": "application/json" },
      })

      const result = await response.json()

      if (!response.ok) {
        if (result.errors) {
          handleServerErrors(result.errors)
        } else {
          setError("root", {
            type: "server",
            message: result.message || "Registration failed",
          })
        }
      } else {
        // Success
        console.log("Registration successful", result)
      }
    } catch (error) {
      setError("root", {
        type: "server",
        message: "Network error. Please try again.",
      })
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      {errors.root && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {errors.root.message}
        </div>
      )}

      <div>
        <label>Email</label>
        <input {...register("email")} className="border rounded px-3 py-2 w-full" />
        {errors.email && <p className="text-red-500">{errors.email.message}</p>}
      </div>

      <div>
        <label>Password</label>
        <input type="password" {...register("password")} className="border rounded px-3 py-2 w-full" />
        {errors.password && <p className="text-red-500">{errors.password.message}</p>}
      </div>

      <button
        type="submit"
        disabled={isSubmitting}
        className="px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
      >
        {isSubmitting ? "Registering..." : "Register"}
      </button>
    </form>
  )
}
```

### Async Validation
```typescript
"use client"

import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { useState } from "react"

const schema = z.object({
  username: z.string().min(3, "Username must be at least 3 characters"),
  email: z.string().email("Invalid email"),
})

type SchemaValues = z.infer<typeof schema>

export function AsyncValidationForm() {
  const [checkingUsername, setCheckingUsername] = useState(false)
  const [checkingEmail, setCheckingEmail] = useState(false)

  const {
    register,
    handleSubmit,
    setError,
    formState: { errors, isSubmitting },
  } = useForm<SchemaValues>({
    resolver: zodResolver(schema),
    mode: "onBlur", // Validate on blur for async checks
  })

  const checkUsernameAvailability = async (username: string) => {
    if (username.length < 3) return
    
    setCheckingUsername(true)
    try {
      const response = await fetch(`/api/check-username?username=${username}`)
      const data = await response.json()
      
      if (data.exists) {
        setError("username", {
          type: "manual",
          message: "Username is already taken",
        })
      }
    } catch (error) {
      console.error("Username check failed:", error)
    } finally {
      setCheckingUsername(false)
    }
  }

  const checkEmailAvailability = async (email: string) => {
    if (!email.includes("@")) return
    
    setCheckingEmail(true)
    try {
      const response = await fetch(`/api/check-email?email=${email}`)
      const data = await response.json()
      
      if (data.exists) {
        setError("email", {
          type: "manual",
          message: "Email is already registered",
        })
      }
    } catch (error) {
      console.error("Email check failed:", error)
    } finally {
      setCheckingEmail(false)
    }
  }

  const onSubmit = async (data: SchemaValues) => {
    console.log("Form submitted:", data)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label>Username</label>
        <div className="relative">
          <input
            {...register("username", {
              onBlur: (e) => checkUsernameAvailability(e.target.value),
            })}
            className="border rounded px-3 py-2 w-full pr-10"
          />
          {checkingUsername && (
            <span className="absolute right-3 top-2">
              <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
            </span>
          )}
        </div>
        {errors.username && <p className="text-red-500">{errors.username.message}</p>}
      </div>

      <div>
        <label>Email</label>
        <div className="relative">
          <input
            type="email"
            {...register("email", {
              onBlur: (e) => checkEmailAvailability(e.target.value),
            })}
            className="border rounded px-3 py-2 w-full pr-10"
          />
          {checkingEmail && (
            <span className="absolute right-3 top-2">
              <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
            </span>
          )}
        </div>
        {errors.email && <p className="text-red-500">{errors.email.message}</p>}
      </div>

      <button
        type="submit"
        disabled={isSubmitting}
        className="px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
      >
        {isSubmitting ? "Submitting..." : "Submit"}
      </button>
    </form>
  )
}
```

## 5. Performance Optimization

### Debounce Validation
```typescript
"use client"

import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { useCallback } from "react"

const schema = z.object({
  search: z.string().min(2, "Search must be at least 2 characters"),
})

type SchemaValues = z.infer<typeof schema>

function useDebounce<T extends (...args: any[]) => any>(
  callback: T,
  delay: number
): (...args: Parameters<T>) => void {
  let timeoutId: NodeJS.Timeout

  return useCallback(
    (...args: Parameters<T>) => {
      clearTimeout(timeoutId)
      timeoutId = setTimeout(() => callback(...args), delay)
    },
    [callback, delay]
  )
}

export function DebouncedForm() {
  const { register, trigger, formState: { errors } } = useForm<SchemaValues>({
    resolver: zodResolver(schema),
    mode: "onChange",
  })

  const debouncedValidate = useDebounce(
    () => trigger("search"),
    500
  )

  return (
    <form className="space-y-4">
      <div>
        <label>Search</label>
        <input
          {...register("search", {
            onChange: () => debouncedValidate(),
          })}
          className="border rounded px-3 py-2 w-full"
        />
        {errors.search && <p className="text-red-500">{errors.search.message}</p>}
      </div>
    </form>
  )
}
```

### Memoized Components
```typescript
"use client"

import { useForm, Controller } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { memo } from "react"

const schema = z.object({
  firstName: z.string().min(1, "First name is required"),
  lastName: z.string().min(1, "Last name is required"),
  email: z.string().email("Invalid email"),
})

type SchemaValues = z.infer<typeof schema>

const MemoizedInput = memo(function MemoizedInput({
  label,
  error,
  ...props
}: any) {
  return (
    <div>
      <label>{label}</label>
      <input {...props} className="border rounded px-3 py-2 w-full" />
      {error && <p className="text-red-500">{error}</p>}
    </div>
  )
})

export function OptimizedForm() {
  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm<SchemaValues>({
    resolver: zodResolver(schema),
  })

  const onSubmit = (data: SchemaValues) => {
    console.log(data)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <Controller
        name="firstName"
        control={control}
        render={({ field }) => (
          <MemoizedInput
            label="First Name"
            error={errors.firstName?.message}
            {...field}
          />
        )}
      />
      
      <Controller
        name="lastName"
        control={control}
        render={({ field }) => (
          <MemoizedInput
            label="Last Name"
            error={errors.lastName?.message}
            {...field}
          />
        )}
      />
      
      <Controller
        name="email"
        control={control}
        render={({ field }) => (
          <MemoizedInput
            label="Email"
            error={errors.email?.message}
            type="email"
            {...field}
          />
        )}
      />
      
      <button type="submit" className="px-4 py-2 bg-blue-500 text-white rounded">
        Submit
      </button>
    </form>
  )
}
```

## 6. Integration with UI Libraries

### With shadcn/ui
```typescript
"use client"

import { useForm, Controller } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Checkbox } from "@/components/ui/checkbox"

const schema = z.object({
  name: z.string().min(1, "Name is required"),
  email: z.string().email("Invalid email"),
  subscribe: z.boolean().default(false),
})

type SchemaValues = z.infer<typeof schema>

export function ShadcnForm() {
  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm<SchemaValues>({
    resolver: zodResolver(schema),
  })

  const onSubmit = (data: SchemaValues) => {
    console.log(data)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <Controller
        name="name"
        control={control}
        render={({ field }) => (
          <div className="space-y-2">
            <Label htmlFor="name">Name</Label>
            <Input id="name" {...field} />
            {errors.name && (
              <p className="text-sm text-destructive">{errors.name.message}</p>
            )}
          </div>
        )}
      />
      
      <Controller
        name="email"
        control={control}
        render={({ field }) => (
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input id="email" type="email" {...field} />
            {errors.email && (
              <p className="text-sm text-destructive">{errors.email.message}</p>
            )}
          </div>
        )}
      />
      
      <Controller
        name="subscribe"
        control={control}
        render={({ field }) => (
          <div className="flex items-center space-x-2">
            <Checkbox
              id="subscribe"
              checked={field.value}
              onCheckedChange={field.onChange}
            />
            <Label htmlFor="subscribe">Subscribe to newsletter</Label>
          </div>
        )}
      />
      
      <Button type="submit">Submit</Button>
    </form>
  )
}
```

### With Material-UI
```typescript
"use client"

import { useForm, Controller } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { TextField, Button, Checkbox, FormControlLabel } from "@mui/material"

const schema = z.object({
  firstName: z.string().min(1, "First name is required"),
  lastName: z.string().min(1, "Last name is required"),
  email: z.string().email("Invalid email"),
  agreeTerms: z.literal(true, {
    errorMap: () => ({ message: "You must agree to the terms" }),
  }),
})

type SchemaValues = z.infer<typeof schema>

export function MuiForm() {
  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm<SchemaValues>({
    resolver: zodResolver(schema),
  })

  const onSubmit = (data: SchemaValues) => {
    console.log(data)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <Controller
        name="firstName"
        control={control}
        render={({ field }) => (
          <TextField
            {...field}
            label="First Name"
            fullWidth
            error={!!errors.firstName}
            helperText={errors.firstName?.message}
          />
        )}
      />
      
      <Controller
        name="lastName"
        control={control}
        render={({ field }) => (
          <TextField
            {...field}
            label="Last Name"
            fullWidth
            error={!!errors.lastName}
            helperText={errors.lastName?.message}
          />
        )}
      />
      
      <Controller
        name="email"
        control={control}
        render={({ field }) => (
          <TextField
            {...field}
            label="Email"
            type="email"
            fullWidth
            error={!!errors.email}
            helperText={errors.email?.message}
          />
        )}
      />
      
      <Controller
        name="agreeTerms"
        control={control}
        render={({ field }) => (
          <FormControlLabel
            control={
              <Checkbox
                checked={field.value}
                onChange={field.onChange}
              />
            }
            label="I agree to the terms and conditions"
          />
        )}
      />
      {errors.agreeTerms && (
        <p className="text-red-500">{errors.agreeTerms.message}</p>
      )}
      
      <Button type="submit" variant="contained" fullWidth>
        Submit
      </Button>
    </form>
  )
}
```

## 7. Common Patterns

### Auto-save Form
```typescript
"use client"

import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { useEffect } from "react"

const schema = z.object({
  title: z.string().min(1, "Title is required"),
  content: z.string().min(1, "Content is required"),
})

type SchemaValues = z.infer<typeof schema>

export function AutoSaveForm() {
  const {
    register,
    handleSubmit,
    watch,
    formState: { isDirty, isSubmitting },
  } = useForm<SchemaValues>({
    resolver: zodResolver(schema),
    defaultValues: {
      title: "",
      content: "",
    },
  })

  const watchedValues = watch()

  // Auto-save on change
  useEffect(() => {
    const timer = setTimeout(() => {
      if (isDirty) {
        saveDraft(watchedValues)
      }
    }, 1000)

    return () => clearTimeout(timer)
  }, [watchedValues, isDirty])

  const saveDraft = async (data: SchemaValues) => {
    try {
      await fetch("/api/drafts", {
        method: "POST",
        body: JSON.stringify(data),
      })
      console.log("Draft saved")
    } catch (error) {
      console.error("Failed to save draft:", error)
    }
  }

  const onSubmit = async (data: SchemaValues) => {
    console.log("Form submitted:", data)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label>Title</label>
        <input {...register("title")} className="border rounded px-3 py-2 w-full" />
      </div>
      
      <div>
        <label>Content</label>
        <textarea
          {...register("content")}
          rows={10}
          className="border rounded px-3 py-2 w-full"
        />
      </div>
      
      <div className="flex items-center justify-between">
        <span className="text-sm text-gray-500">
          {isDirty ? "Saving..." : "Saved"}
        </span>
        <button
          type="submit"
          disabled={isSubmitting}
          className="px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
        >
          {isSubmitting ? "Publishing..." : "Publish"}
        </button>
      </div>
    </form>
  )
}
```

### Form with Confirmation
```typescript
"use client"

import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { useState } from "react"

const schema = z.object({
  email: z.string().email("Invalid email"),
  action: z.enum(["delete", "archive"]),
})

type SchemaValues = z.infer<typeof schema>

export function ConfirmationForm() {
  const [showConfirm, setShowConfirm] = useState(false)
  const [pendingData, setPendingData] = useState<SchemaValues | null>(null)

  const {
    register,
    handleSubmit,
    formState: { isSubmitting },
  } = useForm<SchemaValues>({
    resolver: zodResolver(schema),
  })

  const onPreview = (data: SchemaValues) => {
    setPendingData(data)
    setShowConfirm(true)
  }

  const onConfirm = async () => {
    if (pendingData) {
      await handleSubmit(onPreview)(pendingData)
      setShowConfirm(false)
      setPendingData(null)
    }
  }

  const onCancel = () => {
    setShowConfirm(false)
    setPendingData(null)
  }

  return (
    <div>
      <form onSubmit={handleSubmit(onPreview)} className="space-y-4">
        <div>
          <label>Email</label>
          <input type="email" {...register("email")} className="border rounded px-3 py-2 w-full" />
        </div>
        
        <div>
          <label>Action</label>
          <select {...register("action")} className="border rounded px-3 py-2 w-full">
            <option value="archive">Archive</option>
            <option value="delete">Delete</option>
          </select>
        </div>
        
        <button type="submit" className="px-4 py-2 bg-blue-500 text-white rounded">
          Preview
        </button>
      </form>

      {showConfirm && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center">
          <div className="bg-white p-6 rounded-lg max-w-md w-full">
            <h2 className="text-xl font-bold mb-4">Confirm Action</h2>
            <p className="mb-4">
              Are you sure you want to {pendingData?.action} the account for {pendingData?.email}?
            </p>
            <div className="flex gap-2">
              <button
                onClick={onCancel}
                className="px-4 py-2 border rounded"
              >
                Cancel
              </button>
              <button
                onClick={onConfirm}
                disabled={isSubmitting}
                className="px-4 py-2 bg-red-500 text-white rounded disabled:opacity-50"
              >
                {isSubmitting ? "Processing..." : "Confirm"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
```

## 8. Testing Forms

### Testing with React Testing Library
```typescript
// BasicForm.test.tsx
import { render, screen, fireEvent, waitFor } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { BasicForm } from "./BasicForm"

describe("BasicForm", () => {
  it("renders form fields", () => {
    render(<BasicForm />)
    
    expect(screen.getByLabelText(/username/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument()
    expect(screen.getByRole("button", { name: /submit/i })).toBeInTheDocument()
  })

  it("shows validation errors for invalid input", async () => {
    const user = userEvent.setup()
    render(<BasicForm />)
    
    const submitButton = screen.getByRole("button", { name: /submit/i })
    await user.click(submitButton)
    
    await waitFor(() => {
      expect(screen.getByText(/username must be at least 2 characters/i)).toBeInTheDocument()
      expect(screen.getByText(/invalid email/i)).toBeInTheDocument()
    })
  })

  it("submits form with valid data", async () => {
    const user = userEvent.setup()
    const consoleSpy = jest.spyOn(console, "log")
    
    render(<BasicForm />)
    
    await user.type(screen.getByLabelText(/username/i), "testuser")
    await user.type(screen.getByLabelText(/email/i), "test@example.com")
    await user.click(screen.getByRole("button", { name: /submit/i }))
    
    await waitFor(() => {
      expect(consoleSpy).toHaveBeenCalledWith(
        expect.objectContaining({
          username: "testuser",
          email: "test@example.com",
        })
      )
    })
  })
})
```

### Testing Async Validation
```typescript
// AsyncValidationForm.test.tsx
import { render, screen, waitFor } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { AsyncValidationForm } from "./AsyncValidationForm"

// Mock fetch
global.fetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve({ exists: false }),
  })
) as jest.Mock

describe("AsyncValidationForm", () => {
  it("checks username availability on blur", async () => {
    const user = userEvent.setup()
    render(<AsyncValidationForm />)
    
    const usernameInput = screen.getByLabelText(/username/i)
    await user.type(usernameInput, "existinguser")
    await user.tab() // Trigger blur
    
    // Mock fetch response
    ;(global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ exists: true }),
    })
    
    await waitFor(() => {
      expect(screen.getByText(/username is already taken/i)).toBeInTheDocument()
    })
  })
})
```
