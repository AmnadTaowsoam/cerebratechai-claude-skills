# shadcn/ui Component Patterns

## Overview
Copy-paste component library built on Radix UI และ Tailwind CSS
คุณเป็นเจ้าของโค้ด ไม่ใช่ dependency

## Installation
```bash
npx shadcn-ui@latest init
npx shadcn-ui@latest add button
```

## Component Categories
- Form (Input, Select, Checkbox)
- Overlay (Dialog, Popover, Tooltip)
- Data Display (Table, Card, Badge)
- Navigation (Tabs, Command)
- Feedback (Toast, Alert)

## Composition Patterns

### Form with Validation
```typescript
import { z } from "zod"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"

const formSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
})

function LoginForm() {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
  })

  return (
    <Form {...form}>
      <FormField
        control={form.control}
        name="email"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Email</FormLabel>
            <FormControl>
              <Input {...field} />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />
    </Form>
  )
}
```

### Data Table with Sorting
```typescript
import {
  ColumnDef,
  flexRender,
  getCoreRowModel,
  getSortedRowModel,
  useReactTable,
} from "@tanstack/react-table"
```

## Customization
- Modify components directly in `components/ui/`
- Adjust Tailwind config for design system
- Extend with custom variants

## Best Practices
- Keep components in `components/ui/`
- Use composition over configuration
- Leverage Tailwind for styling
- Type-safe with TypeScript