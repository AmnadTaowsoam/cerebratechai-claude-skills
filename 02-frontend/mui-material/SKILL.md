# Material-UI (MUI) Best Practices

## Overview
Component library ที่ implement Material Design สำหรับ React

## Core Concepts
- Theme customization
- Styled components
- sx prop usage
- Responsive design
- Dark mode

## Component Patterns

### Theme Setup
```typescript
import { createTheme, ThemeProvider } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: { main: '#1976d2' },
    secondary: { main: '#dc004e' },
    mode: 'light', // or 'dark'
  },
  typography: {
    fontFamily: 'Inter, sans-serif',
    h1: { fontSize: '2.5rem', fontWeight: 600 },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          borderRadius: 8,
        },
      },
    },
  },
});
```

### Common Components
- Button variants
- Form controls
- Data display (Table, Card, List)
- Layout (Grid, Stack, Container)
- Navigation (AppBar, Drawer, Tabs)

### sx Prop Pattern
```typescript
<Box
  sx={{
    display: 'flex',
    gap: 2,
    p: 3,
    bgcolor: 'background.paper',
    borderRadius: 2,
    boxShadow: 1,
    '&:hover': { boxShadow: 3 },
  }}
>
```

### Responsive Design
```typescript
<Grid container spacing={2}>
  <Grid item xs={12} sm={6} md={4}>
    <Card />
  </Grid>
</Grid>
```

## Performance Tips
- Use `sx` for one-off styles
- Use `styled()` for reusable components
- Lazy load heavy components
- Optimize bundle size

## Common Patterns
- Form layouts
- Dashboard layouts
- Modal/Dialog patterns
- Snackbar notifications
- Loading states