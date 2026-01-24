---
name: Design Handoff
description: Transferring designs from designers to developers for implementation using design tools, specifications, assets, and clear communication to ensure accurate implementation.
---

# Design Handoff

> **Current Level:** Intermediate  
> **Domain:** UX/UI Design / Collaboration

---

## Overview

Design handoff is the process of transferring designs from designers to developers for implementation. Effective design handoff uses design tools, detailed specifications, organized assets, and clear communication to ensure designs are implemented accurately and efficiently.

---

## Core Concepts

### 1. Handoff Importance

### Why Handoff Matters

```markdown
# Handoff Importance

## Benefits

### 1. Accurate Implementation
- Designs implemented correctly
- Fidelity maintained
- Consistent with vision
- Meets user needs

### 2. Faster Development
- Clear specifications
- Fewer questions
- Less back-and-forth
- Quicker time to market

### 3. Better Collaboration
- Shared understanding
- Clear expectations
- Open communication
- Team alignment

### 4. Quality Assurance
- Standards documented
- Requirements clear
- Testing criteria defined
- Success metrics established

## Consequences of Poor Handoff

### 1. Implementation Issues
- Designs not implemented correctly
- Inconsistent with vision
- Missing features
- Poor quality

### 2. Delays and Rework
- Frequent questions
- Misunderstandings
- Revisions needed
- Timeline extended

### 3. Team Friction
- Designer frustration
- Developer frustration
- Blame game
- Poor morale

### 4. Quality Issues
- Bugs and errors
- Inconsistent experience
- Poor performance
- User dissatisfaction
```

---

## 2. Design Specifications

### Component Specifications

```markdown
# Design Specifications

## 1. Component Documentation

### Button Component

#### Visual Specifications
```
Size: Medium
Width: Auto
Height: 44px
Padding: 12px 24px
Border Radius: 6px
Border: None
Font: Inter, Medium, 16px
```

#### Colors
```
Primary: #0EA5E9
Hover: #0284C7
Active: #0369A1
Disabled: #9CA3AF
Text: #FFFFFF
```

#### States
```
Default: Primary color
Hover: Darker primary
Active: Even darker
Disabled: Gray, no interaction
Focus: Blue outline, 2px
```

#### Spacing
```
Icon: 16px
Icon to text: 8px
Multiple buttons: 16px gap
```

#### Accessibility
```
Role: button
Keyboard: Enter/Space to activate
Focus: Visible outline
Screen Reader: Announced as button
Minimum touch target: 44x44px
```

#### Code
```tsx
<button className="btn btn-primary btn-medium">
  Button Text
</button>
```

### Input Component

#### Visual Specifications
```
Size: Medium
Width: 100%
Height: 44px
Padding: 12px 16px
Border Radius: 6px
Border: 1px solid #D1D5DB
Font: Inter, Regular, 16px
```

#### Colors
```
Background: #FFFFFF
Border: #D1D5DB
Border Focus: #0EA5E9
Border Error: #EF4444
Text: #111827
Placeholder: #9CA3AF
```

#### States
```
Default: Gray border
Focus: Blue border, 2px outline
Error: Red border
Disabled: Gray background, gray text
```

#### Accessibility
```
Role: textbox
Label: Associated with label element
Error: Associated with error message
Keyboard: Tab to focus, type to input
Screen Reader: Announced with label
```

#### Code
```tsx
<label htmlFor="email">Email</label>
<input
  id="email"
  type="email"
  className="input input-medium"
  placeholder="Enter your email"
/>
```

## 2. Layout Specifications

#### Grid System
```
Columns: 12
Gutter: 16px
Margin: 24px
Max Width: 1280px
Breakpoints: 640px, 768px, 1024px, 1280px
```

#### Spacing Scale
```
4px: 0.25rem
8px: 0.5rem
12px: 0.75rem
16px: 1rem
24px: 1.5rem
32px: 2rem
48px: 3rem
64px: 4rem
```

#### Typography Scale
```
H1: 48px, Bold, Line Height 1.2
H2: 36px, Bold, Line Height 1.3
H3: 24px, Semibold, Line Height 1.4
H4: 20px, Semibold, Line Height 1.5
Body: 16px, Regular, Line Height 1.6
Small: 14px, Regular, Line Height 1.5
```
```

---

## 3. Asset Export

### Export Guidelines

```markdown
# Asset Export

## 1. Image Export

### Format Guidelines
- **Photos**: PNG for transparency, JPG for photos
- **Icons**: SVG for scalable, PNG for raster
- **Logos**: SVG for scalable, PNG for raster
- **Illustrations**: SVG for scalable, PNG for raster

### Size Guidelines
- **1x**: Standard resolution
- **2x**: Retina/High DPI
- **3x**: Super high DPI
- **4K**: Ultra high resolution

### Naming Conventions
```
[component]-[state]-[size]-[scale].png

Examples:
button-primary-medium-2x.png
input-error-medium-1x.png
icon-search-small-1x.svg
logo-brand-1x.svg
```

### Export Settings

#### PNG
- Color: RGB
- Resolution: 72 DPI (web), 300 DPI (print)
- Transparency: Yes (if needed)
- Interlaced: No

#### JPG
- Quality: 80-90%
- Progressive: Yes
- Color: sRGB

#### SVG
- Format: SVG 1.1
- Compression: Yes
- Optimize: Yes
- Remove metadata: Yes

## 2. Icon Export

### SVG Guidelines
- Use viewBox
- Remove unnecessary attributes
- Optimize paths
- Use proper fill/stroke
- Include title/desc

### Example SVG
```svg
<svg
  viewBox="0 0 24 24"
  width="24"
  height="24"
  fill="none"
  stroke="currentColor"
  stroke-width="2"
  stroke-linecap="round"
  stroke-linejoin="round"
>
  <title>Search Icon</title>
  <desc>Search icon with magnifying glass</desc>
  <circle cx="11" cy="11" r="8"></circle>
  <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
</svg>
```

## 3. Font Export

### Web Fonts
- Format: WOFF2 (primary), WOFF (fallback)
- Subset: Latin, Extended Latin
- Weight: Regular, Medium, Semibold, Bold
- Style: Normal, Italic

### Font Files
```
inter-regular.woff2
inter-medium.woff2
inter-semibold.woff2
inter-bold.woff2
inter-regular.woff
inter-medium.woff
inter-semibold.woff
inter-bold.woff
```
```

---

## 4. Design Tokens

### Token Documentation

```markdown
# Design Tokens

## 1. Color Tokens

### Primary Colors
```css
--color-primary-50: #F0F9FF;
--color-primary-100: #E0F2FE;
--color-primary-200: #BAE6FD;
--color-primary-300: #7DD3FC;
--color-primary-400: #38BDF8;
--color-primary-500: #0EA5E9;
--color-primary-600: #0284C7;
--color-primary-700: #0369A1;
--color-primary-800: #075985;
--color-primary-900: #0C4A6E;
```

### Semantic Colors
```css
--color-success: #10B981;
--color-warning: #F59E0B;
--color-error: #EF4444;
--color-info: #3B82F6;
```

### Neutral Colors
```css
--color-gray-50: #F9FAFB;
--color-gray-100: #F3F4F6;
--color-gray-200: #E5E7EB;
--color-gray-300: #D1D5DB;
--color-gray-400: #9CA3AF;
--color-gray-500: #6B7280;
--color-gray-600: #4B5563;
--color-gray-700: #374151;
--color-gray-800: #1F2937;
--color-gray-900: #111827;
```

## 2. Typography Tokens

### Font Families
```css
--font-family-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
--font-family-mono: 'Fira Code', monospace;
```

### Font Sizes
```css
--font-size-xs: 0.75rem;    /* 12px */
--font-size-sm: 0.875rem;   /* 14px */
--font-size-base: 1rem;      /* 16px */
--font-size-lg: 1.125rem;    /* 18px */
--font-size-xl: 1.25rem;     /* 20px */
--font-size-2xl: 1.5rem;    /* 24px */
--font-size-3xl: 1.875rem;  /* 30px */
--font-size-4xl: 2.25rem;   /* 36px */
--font-size-5xl: 3rem;       /* 48px */
```

### Font Weights
```css
--font-weight-light: 300;
--font-weight-normal: 400;
--font-weight-medium: 500;
--font-weight-semibold: 600;
--font-weight-bold: 700;
```

### Line Heights
```css
--line-height-tight: 1.25;
--line-height-normal: 1.5;
--line-height-relaxed: 1.75;
```

## 3. Spacing Tokens

### Spacing Scale
```css
--spacing-0: 0;
--spacing-1: 0.25rem;   /* 4px */
--spacing-2: 0.5rem;    /* 8px */
--spacing-3: 0.75rem;   /* 12px */
--spacing-4: 1rem;      /* 16px */
--spacing-5: 1.25rem;   /* 20px */
--spacing-6: 1.5rem;    /* 24px */
--spacing-8: 2rem;      /* 32px */
--spacing-10: 2.5rem;   /* 40px */
--spacing-12: 3rem;     /* 48px */
--spacing-16: 4rem;     /* 64px */
--spacing-20: 5rem;     /* 80px */
--spacing-24: 6rem;     /* 96px */
```

## 4. Border Tokens

### Border Radius
```css
--border-radius-none: 0;
--border-radius-sm: 0.125rem;  /* 2px */
--border-radius-base: 0.25rem;  /* 4px */
--border-radius-md: 0.375rem;   /* 6px */
--border-radius-lg: 0.5rem;     /* 8px */
--border-radius-xl: 0.75rem;    /* 12px */
--border-radius-2xl: 1rem;      /* 16px */
--border-radius-full: 9999px;
```

### Border Width
```css
--border-width-thin: 1px;
--border-width-base: 2px;
--border-width-thick: 4px;
```

## 5. Shadow Tokens

### Shadows
```css
--shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
--shadow-base: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
--shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
--shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
--shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
```

## 6. Breakpoint Tokens

### Breakpoints
```css
--breakpoint-sm: 640px;
--breakpoint-md: 768px;
--breakpoint-lg: 1024px;
--breakpoint-xl: 1280px;
--breakpoint-2xl: 1536px;
```
```

---

## 5. Component Documentation

### Component Library

```markdown
# Component Documentation

## 1. Button Component

### Usage
```tsx
import { Button } from '@design-system/components'

<Button variant="primary" size="medium" onClick={handleClick}>
  Click me
</Button>
```

### Props
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `ReactNode` | - | Button content |
| `variant` | `'primary' \| 'secondary' \| 'outline' \| 'ghost'` | `'primary'` | Button style variant |
| `size` | `'sm' \| 'md' \| 'lg'` | `'md'` | Button size |
| `disabled` | `boolean` | `false` | Disable button |
| `onClick` | `() => void` | - | Click handler |
| `type` | `'button' \| 'submit' \| 'reset'` | `'button'` | Button type |

### Variants
#### Primary
```tsx
<Button variant="primary">Primary Button</Button>
```

#### Secondary
```tsx
<Button variant="secondary">Secondary Button</Button>
```

#### Outline
```tsx
<Button variant="outline">Outline Button</Button>
```

#### Ghost
```tsx
<Button variant="ghost">Ghost Button</Button>
```

### Sizes
#### Small
```tsx
<Button size="sm">Small Button</Button>
```

#### Medium
```tsx
<Button size="md">Medium Button</Button>
```

#### Large
```tsx
<Button size="lg">Large Button</Button>
```

### States
#### Disabled
```tsx
<Button disabled>Disabled Button</Button>
```

#### Loading
```tsx
<Button disabled>
  <Spinner />
  Loading...
</Button>
```

## 2. Input Component

### Usage
```tsx
import { Input } from '@design-system/components'

<Input
  label="Email"
  placeholder="Enter your email"
  value={email}
  onChange={setEmail}
  error={errors.email}
/>
```

### Props
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `string` | - | Input label |
| `placeholder` | `string` | - | Placeholder text |
| `value` | `string` | - | Input value |
| `onChange` | `(value: string) => void` | - | Change handler |
| `error` | `string` | - | Error message |
| `disabled` | `boolean` | `false` | Disable input |
| `type` | `'text' \| 'email' \| 'password' \| 'number'` | `'text'` | Input type |

### States
#### Default
```tsx
<Input
  label="Email"
  placeholder="Enter your email"
/>
```

#### Error
```tsx
<Input
  label="Email"
  error="Please enter a valid email"
/>
```

#### Disabled
```tsx
<Input
  label="Email"
  disabled
/>
```
```

---

## 6. Interaction Specifications

### Interaction Behavior

```markdown
# Interaction Specifications

## 1. Hover States

### Button Hover
```
Primary Button:
- Background: Darker primary color
- Transform: Scale 1.02
- Transition: 200ms ease

Secondary Button:
- Background: Darker secondary color
- Transform: Scale 1.02
- Transition: 200ms ease

Outline Button:
- Background: Light gray
- Border: Darker gray
- Transition: 200ms ease
```

### Link Hover
```
- Color: Darker link color
- Text Decoration: Underline
- Transition: 200ms ease
```

### Card Hover
```
- Shadow: Larger shadow
- Transform: TranslateY(-4px)
- Transition: 300ms ease
```

## 2. Focus States

### Button Focus
```
- Outline: 2px solid primary color
- Outline Offset: 2px
- Border Radius: 6px
- Transition: 200ms ease
```

### Input Focus
```
- Border: Primary color
- Outline: 2px solid primary color
- Outline Offset: 2px
- Border Radius: 6px
- Transition: 200ms ease
```

## 3. Active States

### Button Active
```
- Background: Even darker color
- Transform: Scale 0.98
- Transition: 100ms ease
```

### Link Active
```
- Color: Even darker color
- Text Decoration: Underline
- Transition: 100ms ease
```

## 4. Loading States

### Button Loading
```
- Spinner: 16px, rotating
- Text: "Loading..."
- Disabled: Yes
- Cursor: Not allowed
```

### Page Loading
```
- Spinner: Centered, 32px
- Background: Semi-transparent overlay
- Text: "Loading..."
- Cursor: Wait
```

## 5. Error States

### Input Error
```
- Border: Error color
- Outline: 2px solid error color
- Error Message: Below input, error color
- Icon: Warning icon in input
```

### Form Error
```
- Alert Box: Error color background
- Icon: Error icon
- Text: Error message
- Border: Error color
```
```

---

## 7. Responsive Behavior

### Responsive Specifications

```markdown
# Responsive Behavior

## 1. Navigation

### Mobile (< 768px)
```
- Type: Hamburger menu
- Position: Fixed, top right
- Behavior: Slide in from right
- Animation: 300ms ease
- Backdrop: Semi-transparent overlay
```

### Tablet (768px - 1024px)
```
- Type: Horizontal menu
- Position: Below header
- Behavior: Visible
- Animation: None
```

### Desktop (> 1024px)
```
- Type: Horizontal menu
- Position: In header
- Behavior: Visible
- Animation: None
```

## 2. Grid Layout

### Mobile (< 768px)
```
- Columns: 1
- Gutter: 16px
- Margin: 16px
```

### Tablet (768px - 1024px)
```
- Columns: 2
- Gutter: 16px
- Margin: 24px
```

### Desktop (> 1024px)
```
- Columns: 3
- Gutter: 24px
- Margin: 32px
```

### Large Desktop (> 1280px)
```
- Columns: 4
- Gutter: 24px
- Margin: 40px
```

## 3. Typography

### Mobile (< 768px)
```
- H1: 32px
- H2: 24px
- H3: 20px
- Body: 16px
- Line Height: 1.5
```

### Tablet (768px - 1024px)
```
- H1: 40px
- H2: 32px
- H3: 24px
- Body: 16px
- Line Height: 1.5
```

### Desktop (> 1024px)
```
- H1: 48px
- H2: 36px
- H3: 24px
- Body: 16px
- Line Height: 1.6
```
```

---

## 8. Tools

### Handoff Tools

```markdown
# Handoff Tools

## 1. Figma

### Features
- Dev Mode
- Inspect panel
- Code export
- Component documentation
- Collaboration

### Best For
- Design systems
- Component libraries
- Team collaboration
- Developer handoff

### Cost
- Freemium

## 2. Zeplin

### Features
- Design inspection
- Code snippets
- Version history
- Style guides
- Project organization

### Best For
- Design handoff
- Style guides
- Team collaboration
- Project management

### Cost
- Paid

## 3. Storybook

### Features
- Component development
- Interactive documentation
- Visual testing
- Addon ecosystem
- Code export

### Best For
- Component libraries
- Design systems
- Documentation
- Testing

### Cost
- Free and open source

## 4. Abstract

### Features
- Design handoff
- Code generation
- Design tokens
- Version control
- Team collaboration

### Best For
- Design systems
- Component libraries
- Token management
- Team collaboration

### Cost
- Paid

## 5. Zeroheight

### Features
- Design system documentation
- Figma integration
- Code snippets
- Collaboration
- Version control

### Best For
- Design systems
- Documentation
- Team collaboration
- Enterprise

### Cost
- Paid
```

---

## 9. Developer Collaboration

### Collaboration Process

```markdown
# Developer Collaboration

## 1. Handoff Meeting

### Preparation
- Prepare design files
- Document specifications
- Prepare questions
- Schedule meeting
- Share materials in advance

### Meeting Agenda
1. Overview of designs
2. Walk through components
3. Discuss technical constraints
4. Answer questions
5. Agree on approach
6. Define next steps

### Follow-up
- Send meeting notes
- Share recordings
- Update documentation
- Answer follow-up questions
- Schedule check-ins

## 2. Communication Channels

### Slack/Discord
- Quick questions
- Daily updates
- Blockers
- Casual discussions

### Email
- Formal communication
- Documentation sharing
- Meeting summaries
- Decisions

### Project Management
- Task tracking
- Progress updates
- Blockers
- Dependencies

### Design Review
- Design feedback
- Implementation review
- Quality assurance
- Sign-off

## 3. Feedback Loop

### Design Review
- Review implementation
- Provide feedback
- Discuss deviations
- Agree on changes
- Update designs if needed

### Iteration
- Implement feedback
- Review changes
- Test thoroughly
- Document decisions
- Sign off
```

---

## 10. QA Process

### Quality Assurance

```markdown
# QA Process

## 1. Design QA

### Visual QA
- [ ] Matches design specifications
- [ ] Colors are correct
- [ ] Typography is correct
- [ ] Spacing is correct
- [ ] Alignment is correct

### Interactive QA
- [ ] Hover states work
- [ ] Focus states work
- [ ] Active states work
- [ ] Loading states work
- [ ] Error states work

### Responsive QA
- [ ] Mobile works correctly
- [ ] Tablet works correctly
- [ ] Desktop works correctly
- [ ] Large desktop works correctly
- [ ] Orientation changes work

### Accessibility QA
- [ ] Keyboard navigation works
- [ ] Screen reader works
- [ ] Color contrast is sufficient
- [ ] Focus indicators are visible
- [ ] ARIA attributes are correct

## 2. Functional QA

### User Flow QA
- [ ] User can complete tasks
- [ ] Navigation works
- [ ] Forms work correctly
- [ ] Error handling works
- [ ] Success states work

### Cross-Browser QA
- [ ] Chrome works
- [ ] Firefox works
- [ ] Safari works
- [ ] Edge works
- [ ] Mobile browsers work

### Performance QA
- [ ] Page load time is acceptable
- [ ] Interactions are smooth
- [ ] No console errors
- [ ] No memory leaks
- [ ] Animations are smooth

## 3. Sign-off

### Approval Criteria
- [ ] All QA items passed
- [ ] Stakeholder approval
- [ ] Design sign-off
- [ ] Documentation complete
- [ ] Ready for release
```

---

## 11. Feedback Loops

### Managing Feedback

```markdown
# Feedback Loops

## 1. Feedback Types

### Design Feedback
- Visual issues
- UX issues
- Accessibility issues
- Performance issues

### Developer Feedback
- Technical constraints
- Implementation challenges
- Better approaches
- Missing specifications

### Stakeholder Feedback
- Business requirements
- User feedback
- Market feedback
- Competitive insights

## 2. Feedback Process

### Collect Feedback
- Document all feedback
- Categorize feedback
- Prioritize feedback
- Assign owners
- Set deadlines

### Analyze Feedback
- Identify patterns
- Determine impact
- Assess feasibility
- Estimate effort

### Implement Feedback
- Make changes
- Test changes
- Document changes
- Communicate changes

### Validate Feedback
- Test with users
- Get stakeholder approval
- Verify requirements met
- Document decisions

## 3. Feedback Management

### Tools
- Issue tracking
- Design review meetings
- Feedback forms
- Surveys
- User testing

### Best Practices
- Be open to feedback
- Respond promptly
- Document decisions
- Communicate clearly
- Follow up
```

---

## 12. Best Practices

### Handoff Best Practices

```markdown
# Best Practices

## 1. Prepare Thoroughly
- Document everything
- Provide clear specs
- Include examples
- Test thoroughly
- Prepare questions

## 2. Communicate Clearly
- Use clear language
- Provide context
- Explain decisions
- Be available
- Respond promptly

## 3. Use Tools Effectively
- Choose right tools
- Set up properly
- Train team
- Document processes
- Iterate on tools

## 4. Collaborate Actively
- Involve developers early
- Get feedback
- Make decisions together
- Build relationships
- Share knowledge

## 5. Document Everything
- Design specifications
- Component documentation
- Interaction behaviors
- Responsive behavior
- Accessibility requirements

## 6. Test Thoroughly
- Visual QA
- Interactive QA
- Responsive QA
- Accessibility QA
- Cross-browser QA

## 7. Be Flexible
- Adapt to constraints
- Consider alternatives
- Compromise when needed
- Iterate based on feedback
- Learn from mistakes

## 8. Follow Up
- Check on progress
- Answer questions
- Provide feedback
- Address issues
- Sign off on work

## 9. Maintain Relationships
- Build trust
- Be respectful
- Communicate openly
- Share credit
- Celebrate successes

## 10. Continuously Improve
- Learn from each project
- Refine processes
- Update documentation
- Train team
- Share knowledge
```

---

## Quick Reference

### Quick Tips

```markdown
# Quick Tips

## Do's
- ✓ Document thoroughly
- ✓ Provide clear specs
- ✓ Include examples
- ✓ Test before handoff
- ✓ Be available for questions
- ✓ Respond promptly
- ✓ Collaborate actively
- ✓ Test thoroughly
- ✓ Follow up
- ✓ Learn from feedback

## Don'ts
- ✗ Assume developers understand
- ✗ Skip documentation
- ✗ Be vague
- ✗ Ignore feedback
- ✗ Be unavailable
- ✗ Delay responses
- ✗ Work in isolation
- ✗ Skip testing
- ✗ Forget follow-up
- ✗ Ignore learning opportunities
```

### Handoff Checklist

```markdown
# Handoff Checklist

## Preparation
- [ ] Design files ready
- [ ] Specifications documented
- [ ] Assets exported
- [ ] Code snippets prepared
- [ ] Questions prepared

## Handoff Meeting
- [ ] Walk through designs
- [ ] Explain decisions
- [ ] Answer questions
- [ ] Agree on approach
- [ ] Define next steps

## Follow-up
- [ ] Meeting notes sent
- [ ] Questions answered
- [ ] Implementation started
```

---

## Quick Start

### Figma Handoff Checklist

```markdown
# Design Handoff Checklist

## Design Files
- [ ] Designs organized in Figma
- [ ] All screens/views included
- [ ] States documented (hover, active, error)
- [ ] Responsive breakpoints defined

## Specifications
- [ ] Spacing documented (8px grid)
- [ ] Colors with hex codes
- [ ] Typography (font, size, weight)
- [ ] Component dimensions
- [ ] Border radius values
- [ ] Shadow specifications

## Assets
- [ ] Icons exported (SVG, PNG)
- [ ] Images optimized
- [ ] Fonts provided
- [ ] Naming convention followed

## Documentation
- [ ] Component descriptions
- [ ] Interaction notes
- [ ] Animation specs
- [ ] Accessibility notes
```

---

## Production Checklist

- [ ] **Design Organization**: Designs organized and labeled clearly
- [ ] **Specifications**: All design specs documented (spacing, colors, typography)
- [ ] **Assets**: All assets exported and organized
- [ ] **States**: All component states documented (default, hover, active, disabled)
- [ ] **Responsive**: Breakpoints and responsive behavior documented
- [ ] **Interactions**: Animations and transitions specified
- [ ] **Accessibility**: Accessibility requirements documented
- [ ] **Handoff Meeting**: Schedule handoff meeting with developers
- [ ] **Questions**: Address developer questions promptly
- [ ] **Follow-up**: Review implementation and provide feedback
- [ ] **Documentation**: Maintain design system documentation
- [ ] **Tools**: Use appropriate handoff tools (Figma, Zeplin, etc.)

---

## Anti-patterns

### ❌ Don't: Missing Specifications

```markdown
# ❌ Bad - No specs
[Design file with no measurements or colors documented]
```

```markdown
# ✅ Good - Detailed specs
## Button Component
- Width: 120px
- Height: 40px
- Background: #007bff
- Border radius: 4px
- Padding: 8px 16px
- Font: Inter, 16px, 500
```

### ❌ Don't: Unorganized Assets

```markdown
# ❌ Bad - Random file names
icon1.png
image2.jpg
button.svg
```

```markdown
# ✅ Good - Organized naming
icons/button-primary.svg
images/hero-banner.jpg
components/button-active.png
```

### ❌ Don't: No Handoff Meeting

```markdown
# ❌ Bad - Just send files
[Email with design files, no explanation]
```

```markdown
# ✅ Good - Meeting + documentation
1. Schedule handoff meeting
2. Walk through designs
3. Explain decisions
4. Answer questions
5. Provide written documentation
```

---

## Integration Points

- **Design Systems** (`22-ux-ui-design/design-systems/`) - Component documentation
- **Technical Writing** (`21-documentation/technical-writing/`) - Clear specifications
- **Team Collaboration** (`27-team-collaboration/`) - Design-dev collaboration

---

## Further Reading

- [Figma Developer Handoff](https://help.figma.com/hc/en-us/articles/360055204213)
- [Design Handoff Best Practices](https://www.invisionapp.com/inside-design/design-handoff/)
- [Zeplin Documentation](https://support.zeplin.io/)
- [ ] Documentation updated
- [ ] Questions answered
- [ ] Check-ins scheduled
- [ ] Progress tracked

## QA
- [ ] Visual QA complete
- [ ] Interactive QA complete
- [ ] Responsive QA complete
- [ ] Accessibility QA complete
- [ ] Cross-browser QA complete

## Sign-off
- [ ] All QA passed
- [ ] Stakeholder approval
- [ ] Design sign-off
- [ ] Documentation complete
- [ ] Ready for release
```
