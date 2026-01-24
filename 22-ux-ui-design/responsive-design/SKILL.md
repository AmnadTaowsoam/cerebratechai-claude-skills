---
name: Responsive Design
description: Creating websites and applications that work well on all devices and screen sizes using flexible layouts, media queries, and mobile-first approaches.
---

# Responsive Design

> **Current Level:** Intermediate  
> **Domain:** UX/UI Design / Frontend

---

## Overview

Responsive design ensures websites work well on all devices and screen sizes. Effective responsive design uses flexible layouts, CSS media queries, fluid typography, and mobile-first approaches to create seamless experiences across desktop, tablet, and mobile devices.

---

## Core Concepts

### 1. Responsive Design Principles

### Core Principles

```markdown
# Responsive Design Principles

## 1. Mobile-First Approach
Design for mobile devices first, then enhance for larger screens.

### Benefits
- Focus on essential content
- Faster load times on mobile
- Progressive enhancement
- Better performance

### Implementation
- Start with mobile styles
- Add breakpoints for larger screens
- Use min-width media queries
- Enhance experience progressively

## 2. Flexible Grids
Use flexible grid systems that adapt to screen size.

### Benefits
- Consistent layouts
- Easy to maintain
- Flexible content
- Scalable design

### Implementation
- Use CSS Grid or Flexbox
- Use percentage-based widths
- Use flexible units (fr, %)
- Use min/max constraints

## 3. Flexible Media
Make images and media scale appropriately.

### Benefits
- Images fit any screen
- No horizontal scrolling
- Better performance
- Consistent appearance

### Implementation
- Use max-width: 100%
- Use height: auto
- Use srcset for responsive images
- Use picture element for art direction

## 4. Flexible Typography
Make text scale appropriately.

### Benefits
- Readable on all devices
- Consistent line length
- Better readability
- Improved UX

### Implementation
- Use relative units (rem, em, %)
- Use fluid typography
- Use CSS clamp()
- Use modular scale

## 5. Touch-Friendly
Make elements easy to interact with on touch devices.

### Benefits
- Better mobile experience
- Easier to use
- Fewer errors
- Improved accessibility

### Implementation
- Minimum 44x44px touch targets
- Adequate spacing
- Large clickable areas
- Avoid hover-only interactions
```

---

## 2. Mobile-First Approach

### Mobile-First CSS

```css
/* Mobile-First CSS */

/* Base styles (mobile) */
.container {
  width: 100%;
  padding: 1rem;
  margin: 0 auto;
}

.grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

.card {
  width: 100%;
  padding: 1rem;
  border-radius: 0.5rem;
}

.button {
  width: 100%;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
}

/* Tablet (min-width: 768px) */
@media (min-width: 768px) {
  .container {
    max-width: 768px;
  }

  .grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .button {
    width: auto;
  }
}

/* Desktop (min-width: 1024px) */
@media (min-width: 1024px) {
  .container {
    max-width: 1024px;
  }

  .grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* Large Desktop (min-width: 1280px) */
@media (min-width: 1280px) {
  .container {
    max-width: 1280px;
  }

  .grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
```

### Mobile-First React Components

```tsx
// Mobile-First Component
export const ResponsiveGrid = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className="responsive-grid">
      {children}
    </div>
  )
}

// CSS
.responsive-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
  padding: 1rem;
}

@media (min-width: 768px) {
  .responsive-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .responsive-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (min-width: 1280px) {
  .responsive-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
```

---

## 3. Breakpoints Strategy

### Common Breakpoints

```css
/* Breakpoint Strategy */

/* Extra Small Devices (phones, less than 576px) */
@media (max-width: 575.98px) {
  /* Styles */
}

/* Small Devices (landscape phones, 576px and up) */
@media (min-width: 576px) {
  /* Styles */
}

/* Medium Devices (tablets, 768px and up) */
@media (min-width: 768px) {
  /* Styles */
}

/* Large Devices (desktops, 992px and up) */
@media (min-width: 992px) {
  /* Styles */
}

/* Extra Large Devices (large desktops, 1200px and up) */
@media (min-width: 1200px) {
  /* Styles */
}

/* Extra Extra Large Devices (very large desktops, 1400px and up) */
@media (min-width: 1400px) {
  /* Styles */
}
```

### Custom Breakpoints

```css
/* Custom Breakpoints */

/* Define custom breakpoints */
:root {
  --breakpoint-xs: 480px;
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
  --breakpoint-2xl: 1536px;
}

/* Use custom breakpoints */
@media (min-width: var(--breakpoint-sm)) {
  /* Small screens and up */
}

@media (min-width: var(--breakpoint-md)) {
  /* Medium screens and up */
}

@media (min-width: var(--breakpoint-lg)) {
  /* Large screens and up */
}

/* Range breakpoints */
@media (min-width: var(--breakpoint-sm)) and (max-width: calc(var(--breakpoint-md) - 1px)) {
  /* Small to medium screens only */
}
```

---

## 4. Flexible Grids

### CSS Grid

```css
/* CSS Grid Layout */
.grid {
  display: grid;
  gap: 1rem;
  padding: 1rem;
}

/* Mobile: 1 column */
.grid {
  grid-template-columns: 1fr;
}

/* Tablet: 2 columns */
@media (min-width: 768px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Desktop: 3 columns */
@media (min-width: 1024px) {
  .grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* Large Desktop: 4 columns */
@media (min-width: 1280px) {
  .grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

/* Auto-fit grid */
.grid-auto-fit {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  padding: 1rem;
}

/* Masonry-like grid */
.grid-masonry {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  grid-auto-rows: 10px;
  gap: 1rem;
  padding: 1rem;
}

.grid-masonry > * {
  grid-row: span 5;
}
```

### Flexbox Layout

```css
/* Flexbox Layout */
.flex-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  padding: 1rem;
}

/* Mobile: Column direction */
.flex-container {
  flex-direction: column;
}

/* Tablet: Row direction */
@media (min-width: 768px) {
  .flex-container {
    flex-direction: row;
  }
}

/* Flex items */
.flex-item {
  flex: 1 1 100%;
  min-width: 0;
}

/* Equal width items */
.flex-equal {
  display: flex;
  gap: 1rem;
}

.flex-equal > * {
  flex: 1;
}

/* Center alignment */
.flex-center {
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Space between */
.flex-between {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
```

---

## 5. Flexible Media

### Responsive Images

```html
<!-- Responsive Images with srcset -->
<img
  src="image-800.jpg"
  srcset="image-400.jpg 400w,
          image-800.jpg 800w,
          image-1200.jpg 1200w,
          image-1600.jpg 1600w"
  sizes="(max-width: 600px) 400px,
         (max-width: 900px) 800px,
         (max-width: 1200px) 1200px,
         1600px"
  alt="Responsive image"
  loading="lazy"
/>

<!-- Picture Element for Art Direction -->
<picture>
  <source media="(min-width: 1024px)" srcset="large.jpg">
  <source media="(min-width: 768px)" srcset="medium.jpg">
  <img src="small.jpg" alt="Responsive image">
</picture>

<!-- Responsive Background Images -->
<div class="hero">
  <h1>Hero Title</h1>
</div>

<style>
.hero {
  background-image: url('hero-small.jpg');
  background-size: cover;
  background-position: center;
  min-height: 400px;
}

@media (min-width: 768px) {
  .hero {
    background-image: url('hero-medium.jpg');
    min-height: 500px;
  }
}

@media (min-width: 1024px) {
  .hero {
    background-image: url('hero-large.jpg');
    min-height: 600px;
  }
}
</style>
```

### Responsive Video

```html
<!-- Responsive Video Container -->
<div class="video-container">
  <iframe
    src="https://www.youtube.com/embed/dQw4w9WgXcQ"
    title="Video"
    allowfullscreen
  ></iframe>
</div>

<style>
.video-container {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 aspect ratio */
  height: 0;
  overflow: hidden;
}

.video-container iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
</style>
```

---

## 6. Responsive Typography

### Fluid Typography

```css
/* Fluid Typography */
:root {
  --font-size-min: 16px;
  --font-size-max: 24px;
  --viewport-min: 320px;
  --viewport-max: 1200px;
}

/* Using CSS clamp() */
.fluid-text {
  font-size: clamp(
    var(--font-size-min),
    calc(
      var(--font-size-min) + (
        (var(--font-size-max) - var(--font-size-min)) * (
          (100vw - var(--viewport-min)) /
          (var(--viewport-max) - var(--viewport-min))
        )
      )
    ),
    var(--font-size-max)
  );
}

/* Using container queries */
@container (min-width: 400px) {
  .container-text {
    font-size: 1.25rem;
  }
}

@container (min-width: 800px) {
  .container-text {
    font-size: 1.5rem;
  }
}

/* Responsive line height */
.responsive-text {
  font-size: clamp(1rem, 2.5vw, 1.5rem);
  line-height: clamp(1.5, 3vw, 1.8);
}

/* Responsive spacing */
.responsive-spacing {
  padding: clamp(1rem, 5vw, 2rem);
  margin: clamp(0.5rem, 2vw, 1rem);
}
```

### Modular Scale

```css
/* Modular Scale */
:root {
  --scale: 1.25; /* Major third */
  --base-size: 16px;
}

--size-1: calc(var(--base-size) * var(--scale));
--size-2: calc(var(--size-1) * var(--scale));
--size-3: calc(var(--size-2) * var(--scale));
--size-4: calc(var(--size-3) * var(--scale));
--size-5: calc(var(--size-4) * var(--scale));

h1 { font-size: var(--size-5); }
h2 { font-size: var(--size-4); }
h3 { font-size: var(--size-3); }
h4 { font-size: var(--size-2); }
h5 { font-size: var(--size-1); }
h6 { font-size: var(--base-size); }
```

---

## 7. Touch Targets

### Touch-Friendly Design

```css
/* Touch Targets */
.button {
  min-width: 44px;
  min-height: 44px;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
}

.link {
  display: inline-block;
  padding: 0.5rem 1rem;
  min-height: 44px;
  line-height: 44px;
}

.icon-button {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.input {
  min-height: 44px;
  padding: 0.75rem 1rem;
  font-size: 1rem;
}

.checkbox {
  width: 44px;
  height: 44px;
}

/* Touch-friendly spacing */
.touch-spaced {
  gap: 1rem;
  padding: 1rem;
}

/* Touch-friendly lists */
.touch-list {
  list-style: none;
  padding: 0;
}

.touch-list li {
  padding: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.touch-list li:active {
  background-color: #f3f4f6;
}
```

---

## 8. Performance Considerations

### Performance Tips

```markdown
# Performance Considerations

## 1. Optimize Images
- Use appropriate image sizes
- Use modern formats (WebP, AVIF)
- Lazy load images
- Use srcset for responsive images

## 2. Minimize HTTP Requests
- Combine CSS and JS files
- Use CSS sprites or icon fonts
- Minify assets
- Use CDN

## 3. Optimize CSS
- Use critical CSS
- Minify CSS
- Remove unused CSS
- Use CSS containment

## 4. Optimize JavaScript
- Minify JavaScript
- Use code splitting
- Lazy load components
- Defer non-critical JS

## 5. Use Caching
- Set cache headers
- Use service workers
- Cache API responses
- Use local storage

## 6. Optimize Fonts
- Use font-display: swap
- Subset fonts
- Use WOFF2 format
- Preload critical fonts
```

---

## 9. Testing on Devices

### Testing Checklist

```markdown
# Testing Checklist

## Device Testing
- [ ] iPhone (various sizes)
- [ ] iPad (various sizes)
- [ ] Android phones
- [ ] Android tablets
- [ ] Desktop (various resolutions)
- [ ] Laptop (various resolutions)

## Browser Testing
- [ ] Chrome
- [ ] Firefox
- [ ] Safari
- [ ] Edge
- [ ] Mobile browsers
- [ ] Tablet browsers

## Orientation Testing
- [ ] Portrait mode
- [ ] Landscape mode
- [ ] Orientation changes

## Feature Testing
- [ ] Touch interactions
- [ ] Keyboard navigation
- [ ] Mouse interactions
- [ ] Screen reader support

## Performance Testing
- [ ] Load time on mobile
- [ ] Load time on desktop
- [ ] Image optimization
- [ ] Resource optimization
```

---

## 10. Tools

### Responsive Design Tools

```markdown
# Tools

## 1. Chrome DevTools

### Features
- Device simulation
- Network throttling
- Responsive design mode
- Inspect element

### Best For
- Quick testing
- Debugging
- Responsive design

### Cost
- Free (built-in)

## 2. Responsively App

### Features
- Multiple device preview
- Synchronized scrolling
- URL sharing
- Local testing

### Best For
- Testing on multiple devices
- Visual testing
- Quick previews

### Cost
- Free

## 3. BrowserStack

### Features
- Real device testing
- Multiple browsers
- Automated testing
- Debugging tools

### Best For
- Real device testing
- Cross-browser testing
- Professional testing

### Cost
- Paid

## 4. LambdaTest

### Features
- Real device testing
- Multiple browsers
- Automated testing
- Visual regression

### Best For
- Real device testing
- Cross-browser testing
- Team collaboration

### Cost
- Freemium

## 5. Figma

### Features
- Device frames
- Responsive design
- Prototyping
- Collaboration

### Best For
- Design
- Prototyping
- Team collaboration

### Cost
- Freemium
```

---

## 11. Common Patterns

### Responsive Patterns

```markdown
# Common Patterns

## 1. Column Drop
Content drops to new columns as screen size increases.

## 2. Mostly Fluid
Content flows with flexible widths.

## 3. Layout Shifter
Layout changes completely at breakpoints.

## 4. Off Canvas
Navigation slides in from off-screen.

## 5. Tiny Tweaks
Minor adjustments at breakpoints.

## 6. Content Zoom
Content scales with viewport.

## 7. Fluid Grid
Grid uses flexible units.

## 8. Cards to List
Cards become list items on mobile.

## 9. Hamburger Menu
Navigation collapses to hamburger icon.

## 10. Sticky Header
Header stays visible while scrolling.
```

---

## 12. Best Practices

### Responsive Design Best Practices

```markdown
# Best Practices

## 1. Mobile-First
- Design for mobile first
- Enhance for larger screens
- Focus on essential content
- Progressive enhancement

## 2. Flexible Layouts
- Use flexible grids
- Use flexible media
- Use flexible typography
- Use flexible spacing

## 3. Touch-Friendly
- Minimum 44x44px touch targets
- Adequate spacing
- Large clickable areas
- Avoid hover-only interactions

## 4. Performance
- Optimize images
- Minimize HTTP requests
- Use caching
- Optimize assets

## 5. Test Thoroughly
- Test on real devices
- Test on different browsers
- Test different orientations
- Test different connections

## 6. Use Semantic HTML
- Use proper elements
- Maintain heading hierarchy
- Use landmarks
- Provide accessibility

## 7. Consider Accessibility
- Keyboard navigation
- Screen reader support
- Color contrast
- Focus indicators

## 8. Optimize Images
- Use appropriate sizes
- Use modern formats
- Lazy load images
- Use srcset

## 9. Use Media Queries Wisely
- Use mobile-first approach
- Use logical breakpoints
- Test all breakpoints
- Document breakpoints

## 10. Iterate and Improve
- Gather feedback
- Monitor analytics
- Make improvements
- Stay updated
```

---

## Quick Reference

### Quick Tips

```markdown
# Quick Tips

## Do's
- ✓ Use mobile-first approach
- ✓ Use flexible layouts
- ✓ Make touch targets large
- ✓ Optimize images
- ✓ Test on real devices
- ✓ Use semantic HTML
- ✓ Consider performance
- ✓ Test accessibility

## Don'ts
- ✓ Don't use fixed widths
- ✓ Don't ignore mobile users
- ✓ Don't make touch targets small
- ✓ Don't use large images
- ✓ Don't test only on desktop
- ✓ Don't use non-semantic HTML
- ✓ Don't ignore performance
- ✓ Don't forget accessibility
```

### Media Query Quick Reference

```css
/* Mobile First */
@media (min-width: 768px) {
  /* Tablet and up */
}

@media (min-width: 1024px) {
  /* Desktop and up */
}

/* Desktop First */
@media (max-width: 1023px) {
  /* Tablet and down */
}

@media (max-width: 767px) {
  /* Mobile only */
}

/* Range */
@media (min-width: 768px) and (max-width: 1023px) {
  /* Tablet only */
}

/* Orientation */
@media (orientation: portrait) {
  /* Portrait mode */
}

@media (orientation: landscape) {
  /* Landscape mode */
}

/* High DPI */
@media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
  /* Retina displays */
}
```

---

## Quick Start

### Mobile-First Responsive Layout

```css
/* Base styles (mobile) */
.container {
  width: 100%;
  padding: 16px;
}

.column {
  width: 100%;
  margin-bottom: 16px;
}

/* Tablet and up */
@media (min-width: 768px) {
  .container {
    max-width: 750px;
    margin: 0 auto;
  }
  
  .columns {
    display: flex;
    gap: 16px;
  }
  
  .column {
    flex: 1;
  }
}

/* Desktop and up */
@media (min-width: 1024px) {
  .container {
    max-width: 1200px;
  }
}
```

### Flexible Images

```html
<!-- Responsive image -->
<img 
  src="image.jpg" 
  srcset="image-small.jpg 480w, image-medium.jpg 768w, image-large.jpg 1200w"
  sizes="(max-width: 480px) 100vw, (max-width: 768px) 50vw, 33vw"
  alt="Description"
>

<!-- Or use CSS -->
<style>
  img {
    max-width: 100%;
    height: auto;
  }
</style>
```

### Viewport Meta Tag

```html
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
```

---

## Production Checklist

- [ ] **Viewport Meta**: Include viewport meta tag
- [ ] **Mobile-First**: Design mobile-first, enhance for larger screens
- [ ] **Flexible Layouts**: Use flexible units (%, em, rem, vw, vh)
- [ ] **Media Queries**: Use appropriate breakpoints
- [ ] **Responsive Images**: Use srcset and sizes attributes
- [ ] **Touch Targets**: Ensure touch targets are at least 44x44px
- [ ] **Typography**: Use relative units (rem, em) for text
- [ ] **Testing**: Test on real devices, not just browser resize
- [ ] **Performance**: Optimize images for different screen sizes
- [ ] **Navigation**: Adapt navigation for mobile (hamburger menu)
- [ ] **Forms**: Make forms mobile-friendly
- [ ] **Tables**: Make tables scrollable or responsive on mobile

---

## Anti-patterns

### ❌ Don't: Fixed Widths

```css
/* ❌ Bad - Fixed width breaks on mobile */
.container {
  width: 1200px;  /* Too wide for mobile! */
}
```

```css
/* ✅ Good - Flexible width */
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}
```

### ❌ Don't: Missing Viewport Meta

```html
<!-- ❌ Bad - No viewport meta -->
<head>
  <title>My Site</title>
</head>
```

```html
<!-- ✅ Good - Viewport meta included -->
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My Site</title>
</head>
```

### ❌ Don't: Desktop-First Approach

```css
/* ❌ Bad - Desktop styles override mobile */
.desktop-layout {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
}

@media (max-width: 768px) {
  .desktop-layout {
    display: block;  /* Override needed */
  }
}
```

```css
/* ✅ Good - Mobile-first */
.mobile-layout {
  display: block;
}

@media (min-width: 768px) {
  .mobile-layout {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
  }
}
```

### ❌ Don't: Non-Responsive Images

```html
<!-- ❌ Bad - Fixed size image -->
<img src="large-image.jpg" width="1200" height="800">
```

```html
<!-- ✅ Good - Responsive image -->
<img 
  src="image.jpg" 
  srcset="image-small.jpg 480w, image-large.jpg 1200w"
  sizes="100vw"
  alt="Description"
  style="max-width: 100%; height: auto;"
>
```

---

## Integration Points

- **CSS/Tailwind** (`02-frontend/tailwind-patterns/`) - Responsive utilities
- **Accessibility** (`22-ux-ui-design/accessibility/`) - Mobile accessibility
- **Design Systems** (`22-ux-ui-design/design-systems/`) - Responsive components

---

## Further Reading

- [Responsive Web Design Basics](https://web.dev/responsive-web-design-basics/)
- [MDN Responsive Design](https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Responsive_Design)
- [A List Apart: Responsive Web Design](https://alistapart.com/article/responsive-web-design/)
