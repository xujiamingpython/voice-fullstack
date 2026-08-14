---
name: Profound Navigator
colors:
  surface: '#111317'
  surface-dim: '#111317'
  surface-bright: '#37393e'
  surface-container-lowest: '#0c0e12'
  surface-container-low: '#1a1c20'
  surface-container: '#1e2024'
  surface-container-high: '#282a2e'
  surface-container-highest: '#333539'
  on-surface: '#e2e2e8'
  on-surface-variant: '#c3c6d4'
  inverse-surface: '#e2e2e8'
  inverse-on-surface: '#2f3035'
  outline: '#8d909e'
  outline-variant: '#424752'
  surface-tint: '#aec6ff'
  primary: '#aec6ff'
  on-primary: '#002e6b'
  primary-container: '#5d8ef1'
  on-primary-container: '#00275e'
  inverse-primary: '#1e5bba'
  secondary: '#ccbeff'
  on-secondary: '#340098'
  secondary-container: '#4e24c0'
  on-secondary-container: '#beadff'
  tertiary: '#29e0ab'
  on-tertiary: '#003828'
  tertiary-container: '#00a47b'
  on-tertiary-container: '#003122'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#d8e2ff'
  primary-fixed-dim: '#aec6ff'
  on-primary-fixed: '#001a43'
  on-primary-fixed-variant: '#004397'
  secondary-fixed: '#e7deff'
  secondary-fixed-dim: '#ccbeff'
  on-secondary-fixed: '#1e0060'
  on-secondary-fixed-variant: '#4c20bd'
  tertiary-fixed: '#55fdc6'
  tertiary-fixed-dim: '#29e0ab'
  on-tertiary-fixed: '#002116'
  on-tertiary-fixed-variant: '#00513b'
  background: '#111317'
  on-background: '#e2e2e8'
  surface-variant: '#333539'
typography:
  display-navigation:
    fontFamily: Hanken Grotesk
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-main:
    fontFamily: Hanken Grotesk
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Hanken Grotesk
    fontSize: 21.3px
    fontWeight: '400'
    lineHeight: 32px
  body-md:
    fontFamily: Hanken Grotesk
    fontSize: 18.6px
    fontWeight: '400'
    lineHeight: 28px
  label-sm:
    fontFamily: Hanken Grotesk
    fontSize: 17.3px
    fontWeight: '400'
    lineHeight: 24px
  caption-xs:
    fontFamily: Hanken Grotesk
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 20px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  container-margin: 20px
  gutter: 12px
  stack-sm: 8px
  stack-md: 16px
  stack-lg: 32px
---

## Brand & Style
The design system is built for a high-performance AI voice navigation experience. The brand personality is focused, intelligent, and unobtrusive, ensuring that the interface never competes with the user's auditory focus.

The aesthetic follows a **Functional Minimalist** approach tailored for low-light driving or walking environments. It prioritizes high whitespace (negative space) to reduce cognitive load, utilizing a sophisticated dark-mode palette that minimizes glare. There is a total absence of decorative elements; every visual mark must serve a functional purpose. The interface relies on structural integrity and clear typographic hierarchy rather than gradients or skeuomorphic effects.

## Colors
The palette is optimized for high-contrast legibility in dark environments. 

- **Core Surfaces:** The base layer uses #0F1115 (Deep Space Black) to ensure the hardware bezel of OLED mobile screens disappears into the UI.
- **Elevation Layers:** Interactive elements and content containers use #1A1E27 to provide subtle depth without the need for shadows.
- **Accents:** #5B8DEF serves as the primary action color. #7C5BEF is reserved for high-intelligence states (like active AI listening) and should be used sparingly as a subtle accent rather than a dominant fill.
- **Status:** Standardized semantic colors (Green/Red) are used for success and error states, maintained at high saturation to ensure visibility against the dark background.

## Typography
This design system utilizes a clean, humanist sans-serif stack to ensure maximum legibility during movement. For the WeChat ecosystem, the system defaults to the system sans-serif (PingFang SC) for Chinese characters while using the defined tokens for Latin and Numeric characters.

- **Scale:** All sizes are derived from the 18pt/16pt/13pt/12pt requirements, converted to pixels for implementation.
- **Navigation Focus:** Directional text and distance metrics use `display-navigation` for immediate glanceability.
- **Weight:** Medium (600) is used for headers to stand out against dark surfaces; Regular (400) is used for all body and descriptive text to prevent "haloing" (text appearing to glow/blur) on high-brightness screens.

## Layout & Spacing
The layout follows a **Fixed Safe-Area** model. Because this is a navigation app, primary interaction zones are anchored to the bottom third of the screen for easy thumb reach.

- **Grid:** A 4-column responsive grid for mobile, with 20px outer margins.
- **Rhythm:** An 8px linear scale governs all vertical spacing.
- **Visual Breathing Room:** Maintain a minimum of 32px padding between the voice trigger icon and any other UI elements to prevent accidental touches and emphasize the AI-first nature of the interface.

## Elevation & Depth
In this design system, depth is communicated through **Tonal Layering** rather than shadows. 

- **Level 0 (Base):** #0F1115 for the main background.
- **Level 1 (Cards/Bubbles):** #1A1E27 for content grouping.
- **Interactive:** Active states are indicated by a 10% opacity increase or the primary blue tint.
- **Outlines:** Use 1px solid borders at 10% white opacity for secondary containers to define edges without adding visual weight. Avoid all drop shadows to maintain the minimalist "flat" aesthetic.

## Shapes
The shape language is consistently "Soft-Geometric." 

- **Corner Radius:** A standard 16px (12pt) radius is applied to all primary containers, buttons, and input fields to create a modern, approachable feel that balances the "coldness" of the dark theme.
- **Interactive Elements:** Buttons and input fields share the same radius to create a unified visual language for touch targets.

## Components

### Buttons
- **Primary Button:** Height: 58px (44pt). Background: #5B8DEF. Text: White (#FFFFFF). Bold/Medium weight. Radius: 16px. No shadow.
- **Secondary Button:** Height: 58px. Background: Transparent. Border: 1px Solid #5B8DEF. Text: #5B8DEF.
- **Voice Trigger:** A circular button (min 80px) centered at the bottom, utilizing the #5B8DEF color with a subtle #7C5BEF outer glow only when the AI is actively listening.

### Inputs & Selection
- **Input Field:** Height: 58px. Background: #1A1E27. Text: #E8EAF0. Placeholder: #8A8F9C. Radius: 16px. Padding-left: 16px.
- **Switch:** iOS style. Off-state: #2C3038. On-state: #5B8DEF. Thumb: #FFFFFF.
- **Selection Chips:** Used for quick-destination categories (e.g., "Gas Station", "Parking"). Filled #1A1E27 when inactive, Primary Blue when active.

### Feedback & Cards
- **Navigation Card:** Floating #1A1E27 container with 20px padding. Uses `display-navigation` for the primary turn instruction.
- **Lists:** Clean separation using subtle 1px dividers (#FFFFFF at 5% opacity). No icons unless they represent specific point-of-interest types.