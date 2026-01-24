# Material-UI (MUI) Best Practices

---

## 1. Executive Summary & Strategic Necessity

### 1.1 Context (ภาษาไทย)

Material-UI (MUI) คือ component library ที่ใช้ Google's Material Design สำหรับ React ซึ่งมี components ที่พร้อมใช้งานและมี customization ที่ยืดหยุ่น MUI ใช้ Emotion สำหรับ CSS-in-JS และมี theme system ที่ทรงพลังสำหรับการจัดการ design tokens และ styling

MUI ให้ components ที่มี accessibility และ responsive design ที่ดี พร้อมกับ TypeScript support และ internationalization (i18n) ซึ่งเหมาะสำหรับ enterprise applications ที่ต้องการ consistency และ scalability

### 1.2 Business Impact (ภาษาไทย)

**ผลกระทบทางธุรกิจ:**

1. **ลด Development Time** - MUI มี components ที่พร้อมใช้งาน ช่วยลดเวลาในการพัฒนา UI ได้ถึง 40-60%
2. **เพิ่ม User Experience** - Material Design principles ช่วยเพิ่ม UX และ consistency
3. **ลด Maintenance Cost** - Component reuse และ theme system ช่วยลด maintenance cost
4. **เพิ่ม Accessibility** - Built-in accessibility ช่วยให้ผู้ใช้ทุกคนเข้าถึงได้
5. **ปรับปรุง Time-to-Market** - Rapid prototyping และ development ช่วยลด time-to-market

### 1.3 Product Thinking (ภาษาไทย)

**มุมมองด้านผลิตภัณฑ์:**

1. **Design System** - MUI เป็น design system ที่สมบูรณ์พร้อมใช้งาน
2. **Customization** - Theme system ช่วยให้ customization ง่ายและยืดหยุ่น
3. **Accessibility First** - Components มี accessibility ที่ดีตั้งแต่เริ่ม
4. **Responsive Design** - Built-in responsive design สำหรับทุก devices
5. **Internationalization** - Support สำหรับ multiple languages และ RTL

---

## 2. Technical Deep Dive (The "How-to")

### 2.1 Core Logic

MUI ประกอบด้วย:

1. **Core Components** - 50+ components ที่พร้อมใช้งาน
2. **Theme System** - จัดการ design tokens และ styling
3. **Styled Components** - `sx` prop และ `styled()` API
4. **Layout System** - Grid, Container, Stack สำหรับ responsive layouts
5. **Form Components** - TextField, Select, Checkbox และอื่นๆ
6. **Data Display** - Table, Card, List สำหรับแสดงข้อมูล

### 2.2 Architecture Diagram Requirements

```
┌─────────────────────────────────────────────────────────┐
│              MUI Architecture                           │
├─────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Application Layer                       │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │   Pages      │  │  Features   │  │  Layouts  │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Theme Provider Layer                   │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  Theme      │  │  Color      │  │  Design   │  │   │
│  │  │  Context    │  │  Mode       │  │  Tokens   │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Component Library Layer                 │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  Layout     │  │  Navigation │  │  Feedback  │  │   │
│  │  │  Components │  │  Components │  │  Components│  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  Form       │  │  Data       │  │  Surface   │  │   │
│  │  │  Components │  │  Display    │  │  Components│  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Styling System Layer                   │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  sx Prop    │  │  styled()   │  │  System   │  │   │
│  │  │  API        │  │  API        │  │  Props    │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
│  ┌───────────────────────────────────────────────────┐   │
│  │              CSS-in-JS Engine Layer                  │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │   Emotion   │  │  Cache      │  │  Server    │  │   │
│  │  │   Runtime   │  │  Provider   │  │  Rendering │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
└─────────────────────────────────────────────────────────┘
```

### 2.3 Implementation Workflow

**Step 1: Setup Theme Provider**

```typescript
// theme.ts
import { createTheme, responsiveFontSizes } from '@mui/material/styles'

let theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", sans-serif',
  },
})

theme = responsiveFontSizes(theme)

export default theme
```

```typescript
// ThemeRegistry.tsx
'use client'

import * as React from 'react'
import { ThemeProvider } from '@mui/material/styles'
import CssBaseline from '@mui/material/CssBaseline'
import theme from './theme'

export default function ThemeRegistry({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      {children}
    </ThemeProvider>
  )
}
```

---

## 3. Tooling & Tech Stack

### 3.1 Enterprise Tools

| Tool | Purpose | Version | License |
|------|---------|---------|---------|
| @mui/material | Core Component Library | ^5.0.0 | MIT |
| @mui/icons-material | Icons | ^5.0.0 | MIT |
| @emotion/react | CSS-in-JS Engine | ^11.0.0 | MIT |
| @emotion/styled | Styled Components | ^11.0.0 | MIT |
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

---

## 4. Standards, Compliance & Security

### 4.1 International Standards

- **WCAG 2.1 Level AA** - Components มี accessibility ที่ดี
- **Material Design Guidelines** - ปฏิบัติตาม Google's Material Design
- **ISO 9241-11** - Usability Standards สำหรับ UI Components
- **GDPR** - Data Protection สำหรับ User Data

### 4.2 Security Protocol

MUI ต้องปฏิบัติตามหลักความปลอดภัย:

1. **XSS Prevention** - Sanitize user input ใน form components
2. **CSRF Protection** - ใช้ CSRF tokens สำหรับ forms
3. **Secure Storage** - ไม่เก็บ sensitive data ใน localStorage
4. **Content Security** - ใช้ Content Security Policy

```typescript
// Secure form handling
import { TextField } from '@mui/material'

function SecureForm() {
  const [value, setValue] = React.useState('')

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    // Sanitize input if needed
    const sanitized = e.target.value.replace(/[<>]/g, '')
    setValue(sanitized)
  }

  return (
    <TextField
      value={value}
      onChange={handleChange}
      label="Secure Input"
    />
  )
}
```

### 4.3 Explainability

MUI ต้องสามารถอธิบายได้ว่า:

1. **Component Behavior** - ทำไม component ทำงานอย่างไร
2. **Theme System** - ทำไม theme ใช้งานอย่างไร
3. **Styling Approach** - ทำไมใช้ `sx` prop หรือ `styled()`
4. **Accessibility** - ทำไม components มี accessibility ที่ดี

---

## 5. Unit Economics & Performance Metrics (KPIs)

### 5.1 Cost Calculation

| Metric | Calculation | Target |
|--------|-------------|--------|
| Bundle Size | JavaScript bundle size | < 300 KB |
| Initial Load Time | Time to first render | < 2s |
| Component Render Time | Time per component render | < 50ms |
| Theme Update Time | Time to update theme | < 100ms |
| Accessibility Score | WCAG compliance score | > 95% |

### 5.2 Key Performance Indicators

**Technical Metrics:**

1. **Bundle Size** - JavaScript bundle ที่ใช้งาน
2. **Render Performance** - Component render time
3. **Theme Performance** - Theme update time
4. **Accessibility Score** - WCAG compliance score

**Business Metrics:**

1. **Development Velocity** - เวลาในการพัฒนา features
2. **UI Consistency** - Consistency ของ UI ทั่วแอป
3. **User Satisfaction** - ความพึงพอใจของผู้ใช้
4. **Accessibility Compliance** - Accessibility compliance rate

---

## 6. Strategic Recommendations (CTO Insights)

### 6.1 Phase Rollout

**Phase 1: Foundation (Week 1-2)**
- Setup theme provider
- Create base layout components
- Implement color system
- Setup typography

**Phase 2: Core Components (Week 3-4)**
- Implement navigation components
- Add form components
- Create data display components
- Setup feedback components

**Phase 3: Advanced Features (Week 5-6)**
- Implement dark mode
- Add custom theme tokens
- Create reusable components
- Setup responsive design

**Phase 4: Production (Week 7-8)**
- Performance optimization
- Accessibility audit
- Documentation and training
- Component library

### 6.2 Pitfalls to Avoid

1. **Over-customization** - ไม่ customize components มากเกินไป
2. **Theme Bloat** - ไม่เพิ่ม theme tokens ที่ไม่จำเป็น
3. **Accessibility Issues** - ไม่คำนึงถึง accessibility
4. **Performance Issues** - ไม่ optimize bundle size
5. **Inconsistent Usage** - ไม่ใช้ components อย่างสม่ำเสมอ
6. **Legacy Patterns** - ใช้ `makeStyles` แทน `sx` prop

### 6.3 Best Practices Checklist

- [ ] ใช้ `sx` prop สำหรับ styling แบบ inline
- [ ] ใช้ `styled()` API สำหรับ reusable components
- [ ] Implement theme provider สำหรับ consistent styling
- [ ] ใช้ responsive design สำหรับทุก devices
- [ ] คำนึงถึง accessibility ในทุก components
- [ ] Optimize bundle size ด้วย tree-shaking
- [ ] ใช้ TypeScript สำหรับ type safety
- [ ] Implement dark mode สำหรับ user preference
- [ ] ใช้ system props สำหรับ responsive layouts
- [ ] Create custom theme tokens สำหรับ brand consistency
- [ ] ใช้ memoization สำหรับ performance
- [ ] Implement lazy loading สำหรับ heavy components
- [ ] Test บนทุก browsers และ devices
- [ ] คำนึงถึง internationalization (i18n)

---

## 7. Implementation Examples

### 7.1 Theme Setup and Customization

**Basic Theme Setup:**
```typescript
// theme.ts
import { createTheme, responsiveFontSizes } from '@mui/material/styles'

let theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", sans-serif',
  },
})

theme = responsiveFontSizes(theme)

export default theme
```

**Custom Theme Provider:**
```typescript
// ThemeRegistry.tsx
'use client'

import * as React from 'react'
import { ThemeProvider } from '@mui/material/styles'
import CssBaseline from '@mui/material/CssBaseline'
import theme from './theme'

export default function ThemeRegistry({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      {children}
    </ThemeProvider>
  )
}
```

**Advanced Theme Configuration:**
```typescript
import { createTheme } from '@mui/material/styles'

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#3b82f6',
      light: '#60a5fa',
      dark: '#1d4ed8',
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#8b5cf6',
    },
    background: {
      default: '#f5f5f5',
      paper: '#ffffff',
    },
  },
  typography: {
    h1: {
      fontSize: '2.5rem',
      fontWeight: 600,
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 600,
    },
    body1: {
      fontSize: '1rem',
      lineHeight: 1.6,
    },
  },
  shape: {
    borderRadius: 8,
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
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        },
      },
    },
  },
  breakpoints: {
    values: {
      xs: 0,
      sm: 600,
      md: 900,
      lg: 1200,
      xl: 1536,
    },
  },
})

export default theme
```

**Dark Mode Theme:**
```typescript
import { createTheme } from '@mui/material/styles'

const getDesignTokens = (mode: 'light' | 'dark') => ({
  palette: {
    mode,
    ...(mode === 'light'
      ? {
          primary: { main: '#1976d2' },
          background: {
            default: '#f5f5f5',
            paper: '#ffffff',
          },
        }
      : {
          primary: { main: '#90caf9' },
          background: {
            default: '#121212',
            paper: '#1e1e1e',
          },
        }),
  },
})

export default function createAppTheme(mode: 'light' | 'dark') {
  return createTheme(getDesignTokens(mode))
}
```

### 7.2 Component Styling Approaches

**sx Prop (Recommended):**
```typescript
import { Box, Button } from '@mui/material'

function StyledComponent() {
  return (
    <>
      <Box
        sx={{
          p: 2,
          bgcolor: 'background.paper',
          borderRadius: 1,
          boxShadow: 1,
        }}
      >
        Content
      </Box>

      <Button
        sx={{
          py: 1.5,
          px: 3,
          bgcolor: 'primary.main',
          color: 'primary.contrastText',
          '&:hover': {
            bgcolor: 'primary.dark',
          },
        }}
      >
        Styled Button
      </Button>

      {/* Using theme values */}
      <Box
        sx={{
          width: { xs: '100%', md: '50%' },
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          minHeight: 100,
        }}
      >
        Responsive Box
      </Box>
    </>
  )
}
```

**styled() API:**
```typescript
import { styled } from '@mui/material/styles'
import { Button, Card, CardContent, Typography } from '@mui/material'

const CustomButton = styled(Button)(({ theme }) => ({
  padding: theme.spacing(2, 4),
  backgroundColor: theme.palette.primary.main,
  color: theme.palette.primary.contrastText,
  borderRadius: 8,
  '&:hover': {
    backgroundColor: theme.palette.primary.dark,
  },
}))

const StyledCard = styled(Card)(({ theme }) => ({
  maxWidth: 345,
  margin: theme.spacing(2),
  boxShadow: theme.shadows[4],
  transition: 'transform 0.2s',
  '&:hover': {
    transform: 'translateY(-4px)',
  },
}))

function StyledComponents() {
  return (
    <>
      <CustomButton variant="contained">Custom Button</CustomButton>
      <StyledCard>
        <CardContent>
          <Typography variant="h5">Styled Card</Typography>
        </CardContent>
      </StyledCard>
    </>
  )
}
```

**Using System Props:**
```typescript
import { Box, Typography } from '@mui/material'

function SystemPropsExample() {
  return (
    <Box
      display="flex"
      justifyContent="center"
      alignItems="center"
      flexDirection={{ xs: 'column', md: 'row' }}
      gap={2}
      p={3}
      bgcolor="background.paper"
      borderRadius={2}
    >
      <Typography variant="h6">System Props</Typography>
      <Typography variant="body1">
        Using MUI system props for styling
      </Typography>
    </Box>
  )
}
```

### 7.3 Common Components

**Layout Components:**
```typescript
import { Container, Grid, Stack, Box, Paper } from '@mui/material'

function LayoutExample() {
  return (
    <>
      {/* Container */}
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <Typography variant="h4">Container Example</Typography>
      </Container>

      {/* Grid */}
      <Grid container spacing={2} sx={{ mt: 2 }}>
        <Grid item xs={12} sm={6} md={4}>
          <Paper sx={{ p: 2 }}>Item 1</Paper>
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <Paper sx={{ p: 2 }}>Item 2</Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>Item 3</Paper>
        </Grid>
      </Grid>

      {/* Stack */}
      <Stack direction="row" spacing={2} sx={{ mt: 2 }}>
        <Box sx={{ bgcolor: 'primary.main', p: 2, color: 'white' }}>Box 1</Box>
        <Box sx={{ bgcolor: 'secondary.main', p: 2, color: 'white' }}>Box 2</Box>
        <Box sx={{ bgcolor: 'success.main', p: 2, color: 'white' }}>Box 3</Box>
      </Stack>

      {/* Stack with responsive direction */}
      <Stack
        direction={{ xs: 'column', sm: 'row' }}
        spacing={2}
        sx={{ mt: 2 }}
      >
        <Paper sx={{ p: 2, flex: 1 }}>Responsive Stack Item 1</Paper>
        <Paper sx={{ p: 2, flex: 1 }}>Responsive Stack Item 2</Paper>
      </Stack>
    </>
  )
}
```

**Navigation Components:**
```typescript
import {
  AppBar,
  Toolbar,
  Drawer,
  Typography,
  IconButton,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Divider,
  Tabs,
  Tab,
} from '@mui/material'
import {
  Menu as MenuIcon,
  Dashboard,
  Settings,
  Person,
} from '@mui/icons-material'

function NavigationExample() {
  const [drawerOpen, setDrawerOpen] = React.useState(false)
  const [tabValue, setTabValue] = React.useState(0)

  const toggleDrawer = () => setDrawerOpen(!drawerOpen)

  return (
    <>
      {/* AppBar */}
      <AppBar position="static">
        <Toolbar>
          <IconButton
            edge="start"
            color="inherit"
            onClick={toggleDrawer}
            sx={{ mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            MyApp
          </Typography>
        </Toolbar>
      </AppBar>

      {/* Drawer */}
      <Drawer
        anchor="left"
        open={drawerOpen}
        onClose={toggleDrawer}
      >
        <Box sx={{ width: 250 }} role="presentation">
          <List>
            <ListItem disablePadding>
              <ListItemButton>
                <ListItemIcon>
                  <Dashboard />
                </ListItemIcon>
                <ListItemText primary="Dashboard" />
              </ListItemButton>
            </ListItem>
            <ListItem disablePadding>
              <ListItemButton>
                <ListItemIcon>
                  <Person />
                </ListItemIcon>
                <ListItemText primary="Profile" />
              </ListItemButton>
            </ListItem>
            <Divider />
            <ListItem disablePadding>
              <ListItemButton>
                <ListItemIcon>
                  <Settings />
                </ListItemIcon>
                <ListItemText primary="Settings" />
              </ListItemButton>
            </ListItem>
          </List>
        </Box>
      </Drawer>

      {/* Tabs */}
      <Box sx={{ width: '100%' }}>
        <Tabs value={tabValue} onChange={(_, newValue) => setTabValue(newValue)}>
          <Tab label="Tab 1" />
          <Tab label="Tab 2" />
          <Tab label="Tab 3" />
        </Tabs>
      </Box>
    </>
  )
}
```

**Form Components:**
```typescript
import {
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Checkbox,
  FormControlLabel,
  RadioGroup,
  Radio,
  Switch,
  Slider,
  Button,
  Box,
} from '@mui/material'

function FormExample() {
  const [name, setName] = React.useState('')
  const [age, setAge] = React.useState('')
  const [checked, setChecked] = React.useState(false)
  const [gender, setGender] = React.useState('male')
  const [enabled, setEnabled] = React.useState(false)
  const [value, setValue] = React.useState<number[]>([20, 37])

  return (
    <Box component="form" sx={{ maxWidth: 400, mx: 'auto', mt: 4 }}>
      {/* TextField */}
      <TextField
        fullWidth
        label="Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        margin="normal"
        variant="outlined"
      />

      {/* Select */}
      <FormControl fullWidth margin="normal">
        <InputLabel>Age</InputLabel>
        <Select
          value={age}
          label="Age"
          onChange={(e) => setAge(e.target.value)}
        >
          <MenuItem value="">Select Age</MenuItem>
          <MenuItem value={10}>Ten</MenuItem>
          <MenuItem value={20}>Twenty</MenuItem>
          <MenuItem value={30}>Thirty</MenuItem>
        </Select>
      </FormControl>

      {/* Checkbox */}
      <FormControlLabel
        control={
          <Checkbox
            checked={checked}
            onChange={(e) => setChecked(e.target.checked)}
          />
        }
        label="I agree to the terms"
      />

      {/* Radio Group */}
      <FormControl component="fieldset" margin="normal">
        <Typography component="legend">Gender</Typography>
        <RadioGroup
          value={gender}
          onChange={(e) => setGender(e.target.value)}
        >
          <FormControlLabel value="male" control={<Radio />} label="Male" />
          <FormControlLabel value="female" control={<Radio />} label="Female" />
        </RadioGroup>
      </FormControl>

      {/* Switch */}
      <FormControlLabel
        control={
          <Switch
            checked={enabled}
            onChange={(e) => setEnabled(e.target.checked)}
          />
        }
        label="Enable notifications"
      />

      {/* Slider */}
      <Box sx={{ mt: 2 }}>
        <Typography gutterBottom>Temperature range</Typography>
        <Slider
          value={value}
          onChange={(_, newValue) => setValue(newValue as number[])}
          valueLabelDisplay="auto"
          min={0}
          max={100}
        />
      </Box>

      {/* Button */}
      <Button
        fullWidth
        variant="contained"
        sx={{ mt: 3 }}
        type="submit"
      >
        Submit
      </Button>
    </Box>
  )
}
```

**Feedback Components:**
```typescript
import {
  Snackbar,
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
  Button,
  CircularProgress,
  LinearProgress,
  Chip,
} from '@mui/material'

function FeedbackExample() {
  const [snackbarOpen, setSnackbarOpen] = React.useState(false)
  const [dialogOpen, setDialogOpen] = React.useState(false)
  const [loading, setLoading] = React.useState(false)

  return (
    <>
      {/* Snackbar */}
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={6000}
        onClose={() => setSnackbarOpen(false)}
      >
        <Alert severity="success" onClose={() => setSnackbarOpen(false)}>
          Operation completed successfully!
        </Alert>
      </Snackbar>

      {/* Dialog */}
      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)}>
        <DialogTitle>Confirm Action</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Are you sure you want to proceed with this action?
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>Cancel</Button>
          <Button onClick={() => setDialogOpen(false)} variant="contained">
            Confirm
          </Button>
        </DialogActions>
      </Dialog>

      {/* Loading indicators */}
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mt: 2 }}>
        <CircularProgress size={24} />
        <CircularProgress variant="determinate" value={75} />
        <Box sx={{ width: '100%' }}>
          <LinearProgress />
        </Box>
      </Box>

      {/* Chips */}
      <Box sx={{ display: 'flex', gap: 1, mt: 2, flexWrap: 'wrap' }}>
        <Chip label="Default" />
        <Chip label="Clickable" onClick={() => {}} />
        <Chip label="Deletable" onDelete={() => {}} />
        <Chip label="Primary" color="primary" />
        <Chip label="Success" color="success" />
      </Box>
    </>
  )
}
```

**Data Display Components:**
```typescript
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Card,
  CardContent,
  CardActions,
  CardMedia,
  Avatar,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Divider,
  Typography,
  Chip,
  Box,
} from '@mui/material'

interface User {
  id: number
  name: string
  email: string
  role: string
}

const users: User[] = [
  { id: 1, name: 'John Doe', email: 'john@example.com', role: 'Admin' },
  { id: 2, name: 'Jane Smith', email: 'jane@example.com', role: 'User' },
  { id: 3, name: 'Bob Johnson', email: 'bob@example.com', role: 'User' },
]

function DataDisplayExample() {
  return (
    <>
      {/* Table */}
      <TableContainer component={Paper} sx={{ mt: 2 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Email</TableCell>
              <TableCell>Role</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {users.map((user) => (
              <TableRow key={user.id}>
                <TableCell>{user.name}</TableCell>
                <TableCell>{user.email}</TableCell>
                <TableCell>
                  <Chip
                    label={user.role}
                    color={user.role === 'Admin' ? 'primary' : 'default'}
                  />
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Card */}
      <Card sx={{ maxWidth: 345, mt: 2 }}>
        <CardMedia
          component="img"
          height="140"
          image="/static/images/cards/contemplative-reptile.jpg"
          alt="green iguana"
        />
        <CardContent>
          <Typography gutterBottom variant="h5" component="div">
            Lizard
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Lizards are a widespread group of squamate reptiles.
          </Typography>
        </CardContent>
        <CardActions>
          <Button size="small">Share</Button>
          <Button size="small">Learn More</Button>
        </CardActions>
      </Card>

      {/* List */}
      <List sx={{ mt: 2 }}>
        <ListItem>
          <ListItemAvatar>
            <Avatar>A</Avatar>
          </ListItemAvatar>
          <ListItemText primary="Alice" secondary="alice@example.com" />
        </ListItem>
        <Divider variant="inset" component="li" />
        <ListItem>
          <ListItemAvatar>
            <Avatar>B</Avatar>
          </ListItemAvatar>
          <ListItemText primary="Bob" secondary="bob@example.com" />
        </ListItem>
      </List>
    </>
  )
}
```

### 7.4 Responsive Design with MUI

**Using Grid for Responsive Layouts:**
```typescript
import { Grid, Paper, Typography } from '@mui/material'

function ResponsiveGrid() {
  return (
    <Grid container spacing={2}>
      {/* Full width on mobile, half on tablet, third on desktop */}
      <Grid item xs={12} sm={6} md={4}>
        <Paper sx={{ p: 2, height: '100%' }}>
          <Typography>Responsive Item 1</Typography>
        </Paper>
      </Grid>
      <Grid item xs={12} sm={6} md={4}>
        <Paper sx={{ p: 2, height: '100%' }}>
          <Typography>Responsive Item 2</Typography>
        </Paper>
      </Grid>
      <Grid item xs={12} md={4}>
        <Paper sx={{ p: 2, height: '100%' }}>
          <Typography>Responsive Item 3</Typography>
        </Paper>
      </Grid>
    </Grid>
  )
}
```

**Responsive Typography:**
```typescript
import { Typography } from '@mui/material'

function ResponsiveTypography() {
  return (
    <>
      <Typography
        variant="h3"
        sx={{
          fontSize: { xs: '1.5rem', sm: '2rem', md: '3rem' },
        }}
      >
        Responsive Heading
      </Typography>

      <Typography
        sx={{
          fontSize: { xs: '0.875rem', md: '1rem' },
        }}
      >
        Responsive paragraph text
      </Typography>
    </>
  )
}
```

### 7.5 Dark Mode Implementation

**Theme Context for Dark Mode:**
```typescript
// ColorModeContext.tsx
import React, { createContext, useContext, useState } from 'react'
import { createTheme, ThemeProvider as MuiThemeProvider } from '@mui/material/styles'

type ColorMode = 'light' | 'dark'

interface ColorModeContextType {
  toggleColorMode: () => void
  mode: ColorMode
}

const ColorModeContext = createContext<ColorModeContextType | undefined>(undefined)

export function ColorModeProvider({ children }: { children: React.ReactNode }) {
  const [mode, setMode] = useState<ColorMode>('light')

  const colorMode = React.useMemo(
    () => ({
      toggleColorMode: () => {
        setMode((prevMode) => (prevMode === 'light' ? 'dark' : 'light'))
      },
      mode,
    }),
    [mode]
  )

  const theme = React.useMemo(() => createTheme({ palette: { mode } }), [mode])

  return (
    <ColorModeContext.Provider value={colorMode}>
      <MuiThemeProvider theme={theme}>{children}</MuiThemeProvider>
    </ColorModeContext.Provider>
  )
}

export const useColorMode = () => {
  const context = useContext(ColorModeContext)
  if (!context) throw new Error('useColorMode must be used within ColorModeProvider')
  return context
}
```

**Dark Mode Toggle:**
```typescript
import { IconButton, useTheme } from '@mui/material'
import { Brightness4, Brightness7 } from '@mui/icons-material'
import { useColorMode } from './ColorModeContext'

function DarkModeToggle() {
  const theme = useTheme()
  const { toggleColorMode, mode } = useColorMode()

  return (
    <IconButton onClick={toggleColorMode} color="inherit">
      {mode === 'dark' ? <Brightness7 /> : <Brightness4 />}
    </IconButton>
  )
}
```

### 7.6 Custom Theme Tokens

**Extending Theme with Custom Tokens:**
```typescript
import { createTheme } from '@mui/material/styles'

const theme = createTheme({
  palette: {
    primary: {
      main: '#3b82f6',
    },
  },
  typography: {
    fontFamily: '"Inter", sans-serif',
  },
  components: {
    MuiButton: {
      variants: [
        {
          props: { variant: 'dashed' },
          style: {
            border: '2px dashed currentColor',
            backgroundColor: 'transparent',
          },
        },
      ],
    },
  },
  customShadows: {
    card: '0 4px 12px rgba(0,0,0,0.08)',
  },
})

declare module '@mui/material/styles' {
  interface Theme {
    customShadows: {
      card: string
    }
  }
  interface ThemeOptions {
    customShadows?: {
      card?: string
    }
  }
}

export default theme
```

**Using Custom Tokens:**
```typescript
import { Box, useTheme } from '@mui/material'

function CustomTokenExample() {
  const theme = useTheme()

  return (
    <Box
      sx={{
        boxShadow: theme.customShadows.card,
        p: 2,
        borderRadius: 2,
      }}
    >
      Content with custom shadow
    </Box>
  )
}
```

### 7.7 Performance Optimization

**Lazy Loading Components:**
```typescript
import { lazy, Suspense } from 'react'
import { CircularProgress, Box } from '@mui/material'

const HeavyComponent = lazy(() => import('./HeavyComponent'))

function LazyLoadExample() {
  return (
    <Suspense
      fallback={
        <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
          <CircularProgress />
        </Box>
      }
    >
      <HeavyComponent />
    </Suspense>
  )
}
```

**Memoizing Styled Components:**
```typescript
import { memo } from 'react'
import { styled } from '@mui/material/styles'
import { Card, CardContent, Typography } from '@mui/material'

const StyledCard = styled(Card)(({ theme }) => ({
  padding: theme.spacing(2),
  marginBottom: theme.spacing(2),
}))

const MemoizedCard = memo(function MemoizedCard({ title, content }: { title: string; content: string }) {
  return (
    <StyledCard>
      <CardContent>
        <Typography variant="h6">{title}</Typography>
        <Typography variant="body2">{content}</Typography>
      </CardContent>
    </StyledCard>
  )
})
```

**Virtualization with react-window:**
```typescript
import { FixedSizeList } from 'react-window'
import { List, ListItem, ListItemText, Paper } from '@mui/material'

const Row = ({ index, style }: { index: number; style: React.CSSProperties }) => (
  <div style={style}>
    <List>
      <ListItem>
        <ListItemText primary={`Item ${index}`} />
      </ListItem>
    </List>
  </div>
)

function VirtualizedList({ items }: { items: any[] }) {
  return (
    <Paper sx={{ height: 400, width: '100%' }}>
      <FixedSizeList
        height={400}
        itemCount={items.length}
        itemSize={46}
        width="100%"
      >
        {Row}
      </FixedSizeList>
    </Paper>
  )
}
```

### 7.8 TypeScript Integration

**Typing Custom Props:**
```typescript
import { Button, ButtonProps } from '@mui/material'

interface CustomButtonProps extends ButtonProps {
  customProp?: string
}

function CustomButton({ customProp, ...props }: CustomButtonProps) {
  return <Button {...props}>{customProp || 'Default'}</Button>
}

// Usage
<CustomButton customProp="Hello" variant="contained" />
```

**Typing Form Values:**
```typescript
import { useForm, Controller } from 'react-hook-form'
import { TextField, Button } from '@mui/material'

interface FormData {
  name: string
  email: string
}

function TypedForm() {
  const { control, handleSubmit } = useForm<FormData>({
    defaultValues: {
      name: '',
      email: '',
    },
  })

  const onSubmit = (data: FormData) => {
    console.log(data)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Controller
        name="name"
        control={control}
        render={({ field }) => (
          <TextField {...field} label="Name" fullWidth margin="normal" />
        )}
      />
      <Controller
        name="email"
        control={control}
        render={({ field }) => (
          <TextField {...field} label="Email" fullWidth margin="normal" />
        )}
      />
      <Button type="submit" variant="contained">
        Submit
      </Button>
    </form>
  )
}
```

### 7.9 Common Patterns and Recipes

**Data Table with Selection:**
```typescript
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Checkbox,
  TablePagination,
} from '@mui/material'

interface DataTableProps {
  rows: any[]
  columns: { id: string; label: string }[]
}

function DataTable({ rows, columns }: DataTableProps) {
  const [selected, setSelected] = React.useState<readonly number[]>([])
  const [page, setPage] = React.useState(0)
  const [rowsPerPage, setRowsPerPage] = React.useState(5)

  const handleSelectAllClick = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.checked) {
      const newSelected = rows.map((n) => n.id)
      setSelected(newSelected)
      return
    }
    setSelected([])
  }

  const handleClick = (event: React.MouseEvent<unknown>, id: number) => {
    const selectedIndex = selected.indexOf(id)
    let newSelected: readonly number[] = []

    if (selectedIndex === -1) {
      newSelected = newSelected.concat(selected, id)
    } else if (selectedIndex === 0) {
      newSelected = newSelected.concat(selected.slice(1))
    } else if (selectedIndex === selected.length - 1) {
      newSelected = newSelected.concat(selected.slice(0, -1))
    } else if (selectedIndex > 0) {
      newSelected = newSelected.concat(
        selected.slice(0, selectedIndex),
        selected.slice(selectedIndex + 1)
      )
    }

    setSelected(newSelected)
  }

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage)
  }

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10))
    setPage(0)
  }

  const isSelected = (id: number) => selected.indexOf(id) !== -1

  return (
    <Paper>
      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell padding="checkbox">
                <Checkbox
                  indeterminate={selected.length > 0 && selected.length < rows.length}
                  checked={rows.length > 0 && selected.length === rows.length}
                  onChange={handleSelectAllClick}
                />
              </TableCell>
              {columns.map((column) => (
                <TableCell key={column.id}>{column.label}</TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {rows
              .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
              .map((row, index) => {
                const isItemSelected = isSelected(row.id)
                const labelId = `enhanced-table-checkbox-${index}`

                return (
                  <TableRow
                    hover
                    onClick={(event) => handleClick(event, row.id)}
                    role="checkbox"
                    aria-checked={isItemSelected}
                    tabIndex={-1}
                    key={row.id}
                    selected={isItemSelected}
                  >
                    <TableCell padding="checkbox">
                      <Checkbox checked={isItemSelected} />
                    </TableCell>
                    {columns.map((column) => (
                      <TableCell key={column.id}>{row[column.id]}</TableCell>
                    ))}
                  </TableRow>
                )
              })}
          </TableBody>
        </Table>
      </TableContainer>
      <TablePagination
        rowsPerPageOptions={[5, 10, 25]}
        component="div"
        count={rows.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={handleChangePage}
        onRowsPerPageChange={handleChangeRowsPerPage}
      />
    </Paper>
  )
}
```

**Modal Form:**
```typescript
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  Box,
} from '@mui/material'

interface ModalFormProps {
  open: boolean
  onClose: () => void
  onSubmit: (data: any) => void
}

function ModalForm({ open, onClose, onSubmit }: ModalFormProps) {
  const [formData, setFormData] = React.useState({
    name: '',
    email: '',
  })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = () => {
    onSubmit(formData)
    onClose()
    setFormData({ name: '', email: '' })
  }

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Add New Item</DialogTitle>
      <DialogContent>
        <Box sx={{ mt: 2 }}>
          <TextField
            fullWidth
            label="Name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            margin="normal"
          />
          <TextField
            fullWidth
            label="Email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            margin="normal"
          />
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button onClick={handleSubmit} variant="contained">
          Submit
        </Button>
      </DialogActions>
    </Dialog>
  )
}
```

**Searchable List:**
```typescript
import {
  List,
  ListItem,
  ListItemText,
  TextField,
  Box,
  InputAdornment,
} from '@mui/material'
import { Search } from '@mui/icons-material'

function SearchableList({ items }: { items: string[] }) {
  const [searchTerm, setSearchTerm] = React.useState('')

  const filteredItems = items.filter((item) =>
    item.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <Box>
      <TextField
        fullWidth
        placeholder="Search..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <Search />
            </InputAdornment>
          ),
        }}
        sx={{ mb: 2 }}
      />
      <List>
        {filteredItems.map((item, index) => (
          <ListItem key={index}>
            <ListItemText primary={item} />
          </ListItem>
        ))}
      </List>
    </Box>
  )
}
```

**Stepper Form:**
```typescript
import {
  Stepper,
  Step,
  StepLabel,
  StepContent,
  Button,
  Paper,
  Typography,
  Box,
} from '@mui/material'

const steps = [
  {
    label: 'Select campaign settings',
    description: 'For each ad campaign that you create, you can control how much you are willing to spend.',
  },
  {
    label: 'Create an ad group',
    description: 'An ad group contains one or more ads which target a shared set of keywords.',
  },
  {
    label: 'Create an ad',
    description: 'Try out different ad text to see what brings in the most customers.',
  },
]

function StepperForm() {
  const [activeStep, setActiveStep] = React.useState(0)

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1)
  }

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1)
  }

  const handleReset = () => {
    setActiveStep(0)
  }

  return (
    <Box sx={{ maxWidth: 400 }}>
      <Stepper activeStep={activeStep} orientation="vertical">
        {steps.map((step, index) => (
          <Step key={step.label}>
            <StepLabel>{step.label}</StepLabel>
            <StepContent>
              <Typography>{step.description}</Typography>
              <Box sx={{ mb: 2 }}>
                <Button
                  variant="contained"
                  onClick={handleNext}
                  sx={{ mt: 1, mr: 1 }}
                >
                  {index === steps.length - 1 ? 'Finish' : 'Continue'}
                </Button>
                <Button
                  disabled={index === 0}
                  onClick={handleBack}
                  sx={{ mt: 1, mr: 1 }}
                >
                  Back
                </Button>
              </Box>
            </StepContent>
          </Step>
        ))}
      </Stepper>
      {activeStep === steps.length && (
        <Paper square elevation={0} sx={{ p: 3 }}>
          <Typography>All steps completed - you're finished</Typography>
          <Button onClick={handleReset} sx={{ mt: 1, mr: 1 }}>
            Reset
          </Button>
        </Paper>
      )}
    </Box>
  )
}
```

### 7.10 Best Practices

**Styling:**
- Use `sx` prop for inline styling
- Use `styled()` API for reusable components
- Leverage theme tokens for consistency
- Use system props for responsive layouts

**Performance:**
- Lazy load heavy components
- Memoize expensive components
- Use virtualization for large lists
- Optimize bundle size with tree-shaking

**Accessibility:**
- Use semantic HTML elements
- Provide ARIA labels where needed
- Ensure keyboard navigation works
- Test with screen readers

**TypeScript:**
- Type custom props properly
- Use generics for reusable components
- Leverage MUI's built-in types
- Use `Controller` with React Hook Form

**Theme:**
- Keep theme tokens organized
- Use responsive font sizes
- Implement dark mode properly
- Extend theme with custom tokens

---

## 8. Related Skills

- `02-frontend/react-best-practices`
- `02-frontend/state-management`
- `02-frontend/responsive-design`
- `02-frontend/accessibility`
- `22-ux-ui-design/design-systems`
