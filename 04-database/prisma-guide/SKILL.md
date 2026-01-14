# Prisma Best Practices

## Schema Conventions
```prisma
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  createdAt DateTime @default(now()) @map("created_at")
  updatedAt DateTime @updatedAt @map("updated_at")
  
  @@map("users")
}
```

## Query Patterns
```typescript
// ใช้ transactions สำหรับ related operations
await prisma.$transaction(async (tx) => {
  const user = await tx.user.create({...});
  await tx.profile.create({...});
});

// Error handling
try {
  await prisma.user.create({...});
} catch (error) {
  if (error.code === 'P2002') {
    // Unique constraint violation
  }
}
```

## Migration Workflow
1. แก้ schema.prisma
2. `npx prisma migrate dev --name description`
3. `npx prisma generate`