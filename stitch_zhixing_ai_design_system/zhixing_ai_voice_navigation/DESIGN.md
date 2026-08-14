---
name: ZhiXing AI Voice Navigation
colors:
  surface: '#0f131c'
  surface-dim: '#0f131c'
  surface-bright: '#353943'
  surface-container-lowest: '#0a0e17'
  surface-container-low: '#181c24'
  surface-container: '#1c2029'
  surface-container-high: '#262a33'
  surface-container-highest: '#31353e'
  on-surface: '#dfe2ef'
  on-surface-variant: '#c3c6d4'
  inverse-surface: '#dfe2ef'
  inverse-on-surface: '#2c303a'
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
  background: '#0f131c'
  on-background: '#dfe2ef'
  surface-variant: '#31353e'
typography:
  page-title:
    fontFamily: notoSans
    fontSize: 24px
    fontWeight: '500'
    lineHeight: 32px
  body-main:
    fontFamily: notoSans
    fontSize: 21px
    fontWeight: '400'
    lineHeight: 30px
  caption:
    fontFamily: notoSans
    fontSize: 17px
    fontWeight: '400'
    lineHeight: 24px
  label-bold:
    fontFamily: notoSans
    fontSize: 16px
    fontWeight: '500'
    lineHeight: 20px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 4px
  xs: 8px
  sm: 12px
  md: 16px
  lg: 24px
  xl: 32px
  gutter: 16px
  margin: 20px
---

## Brand & Style
The design system is built for a high-utility, AI-driven navigation experience. It adopts a **Minimalist** and **Corporate/Modern** aesthetic, prioritizing clarity and speed of comprehension. The interface is characterized by a "Dark Mode" first approach to reduce glare during night driving and maintain a professional, tech-forward atmosphere. 

Visual decorative elements and gradients are strictly avoided. Instead, hierarchy is established through precise typography, structural alignment, and the purposeful use of functional color against high-contrast backgrounds.

## Colors
The palette uses a deep **Space Black** for the canvas to ensure the UI recedes, making map data and AI responses prominent. 

- **Primary (Tech Blue):** Reserved for primary actions, active navigation paths, and system-critical states.
- **Secondary (Accent Purple):** Used for AI-specific features or secondary data highlights.
- **Success Cyan & Danger Red:** Used strictly for status indicators (e.g., "Arrived," "Traffic Jam," "Rerouting").
- **Surface Colors:** "Card Dark Gray" is used to define interactive surfaces and containers against the pure black background.

## Typography
The system utilizes a clean, humanist Sans-serif (Heiti style) for maximum legibility. 
- **Page Titles:** Should be centered or left-aligned with ample top-margin to define the view context.
- **Body:** Sized for readability at arm's length (phone mounted on a dashboard).
- **Captions:** Used for metadata like "ETA" or "Distance Remaining."
- **Labels:** Specifically tuned for high-contrast visibility within buttons and navigation badges.

## Layout & Spacing
This design system employs a **Fluid Grid** model optimized for the WeChat Mini Program viewport. 
- **Margins:** A consistent 20px side margin is maintained for all content blocks.
- **Safe Areas:** Adhere to bottom safe areas for navigation gestures.
- **Vertical Rhythm:** Components are spaced in increments of 8px to maintain a structured, logical flow. 
- **Alignment:** Navigation elements are bottom-heavy for easy thumb-reachability during one-handed use.

## Elevation & Depth
Depth is communicated through **Tonal Layers** rather than shadows. 
- **Level 0 (Base):** #0F1115 (Background).
- **Level 1 (Cards/Inputs):** #1A1E27 (Surface).
- **Level 2 (Popups/Modals):** #242935 (Slightly lighter than Card Dark Gray).

No drop shadows are used. Boundaries between elements are defined by color contrast or 1pt solid borders in secondary text colors (#8A8F9C at 20% opacity).

## Shapes
The shape language is "Rounded," striking a balance between modern tech and approachable utility. 
- **Standard Radius:** 12pt (16px) for cards, input fields, and primary buttons.
- **Small Radius:** 4pt (5px) for small badges or status tags.
- **Pill:** Reserved for active AI listening states and voice waveform containers.

## Components
- **Primary Button:** Solid #5B8DEF, White Text. Height: 44pt. Used for the main "Start Navigation" or "Confirm" actions.
- **Secondary Button:** Transparent background with a 1pt #5B8DEF border and #5B8DEF text. Used for "Cancel" or "Settings."
- **Input Field:** Background #1A1E27 with 12pt radius. Text color #E8EAF0. Placeholder text #8A8F9C.
- **Switch:** iOS-style toggle. Track color is #5B8DEF when ON, and #242935 when OFF.
- **Cards:** Used to group destination info or AI suggestions. Background #1A1E27, no border, 12pt radius.
- **AI Voice Indicator:** A centered, pulsing circular element or horizontal pill that appears when the system is listening, using the primary Tech Blue.
- **Lists:** Clean rows with 1pt divider lines (#8A8F9C at 10% opacity) and right-pointing chevrons for drill-down navigation.