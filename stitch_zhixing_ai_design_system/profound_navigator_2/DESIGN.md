---
name: Profound Navigator
colors:
  surface: '#f9f9ff'
  surface-dim: '#d8d9e3'
  surface-bright: '#f9f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f3fd'
  surface-container: '#ecedf7'
  surface-container-high: '#e6e8f2'
  surface-container-highest: '#e0e2ec'
  on-surface: '#191c22'
  on-surface-variant: '#424752'
  inverse-surface: '#2d3038'
  inverse-on-surface: '#eff0fa'
  outline: '#737784'
  outline-variant: '#c3c6d4'
  surface-tint: '#1e5bba'
  primary: '#1a58b7'
  on-primary: '#ffffff'
  primary-container: '#3d72d2'
  on-primary-container: '#fefcff'
  inverse-primary: '#aec6ff'
  secondary: '#623dd3'
  on-secondary: '#ffffff'
  secondary-container: '#7b5aee'
  on-secondary-container: '#fffbff'
  tertiary: '#825100'
  on-tertiary: '#ffffff'
  tertiary-container: '#a46700'
  on-tertiary-container: '#fffbff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d8e2ff'
  primary-fixed-dim: '#aec6ff'
  on-primary-fixed: '#001a43'
  on-primary-fixed-variant: '#004397'
  secondary-fixed: '#e7deff'
  secondary-fixed-dim: '#ccbeff'
  on-secondary-fixed: '#1e0060'
  on-secondary-fixed-variant: '#4c20bd'
  tertiary-fixed: '#ffddb8'
  tertiary-fixed-dim: '#ffb960'
  on-tertiary-fixed: '#2a1700'
  on-tertiary-fixed-variant: '#653e00'
  background: '#f9f9ff'
  on-background: '#191c22'
  surface-variant: '#e0e2ec'
typography:
  display-lg:
    fontFamily: Hanken Grotesk
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Hanken Grotesk
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Hanken Grotesk
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Hanken Grotesk
    fontSize: 17px
    fontWeight: '400'
    lineHeight: 26px
  body-md:
    fontFamily: Hanken Grotesk
    fontSize: 15px
    fontWeight: '400'
    lineHeight: 22px
  label-lg:
    fontFamily: Hanken Grotesk
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-md:
    fontFamily: Hanken Grotesk
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
  headline-lg-mobile:
    fontFamily: Hanken Grotesk
    fontSize: 22px
    fontWeight: '600'
    lineHeight: 28px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 4px
  margin-mobile: 16px
  gutter-mobile: 12px
  padding-card: 16px
  stack-sm: 8px
  stack-md: 16px
  stack-lg: 24px
---

## Brand & Style
The design system embodies a "Profound Navigator" persona—a reliable, intelligent, and unobtrusive assistant. The target audience is modern, mobile-first users who value efficiency and clarity during navigation and voice-assisted tasks. 

The visual style is **Minimalist / Modern**, drawing inspiration from the WeChat Mini-program ecosystem. It prioritizes high legibility, generous negative space, and a refined functional aesthetic. The emotional response is one of calm confidence and clarity, achieved through a restricted color palette, soft elevation, and a systematic grid that avoids visual clutter.

## Colors
The palette is centered on "Navigation Blue" (Primary) and "Intelligence Violet" (Accent). 

- **Primary & Accent:** Use the Primary blue for core actions and navigation paths. Use the Accent violet for AI-specific interactions, voice processing states, and secondary highlights.
- **Surface Strategy:** The background uses a cool-toned off-white to reduce glare. Cards and primary surfaces are pure white to create a distinct "layered" appearance against the background.
- **Functional Colors:** Success and Error colors are saturated to ensure immediate recognition in high-stakes navigation contexts.

## Typography
This design system utilizes **Hanken Grotesk** for its exceptional legibility and contemporary geometry. 

- **Hierarchy:** Use `display-lg` sparingly for arrival states or major location names. `headline-md` is the standard for card titles and section headers.
- **Body Text:** `body-lg` (17px) is optimized for readability in mobile contexts where the device may be at arm's length (e.g., in a car mount).
- **Secondary Info:** Use `label-md` for metadata like distances, estimated times, or status timestamps, always paired with the secondary text color.

## Layout & Spacing
The layout follows a **Fluid Grid** model optimized for mobile devices, mirroring the spatial logic of top-tier mini-programs.

- **Margins:** A consistent 16px lateral margin is maintained across all mobile views.
- **Rhythm:** All vertical spacing should be a multiple of the 4px base unit. Use 16px (`stack-md`) for related elements and 24px (`stack-lg`) to separate distinct sections or cards.
- **Safe Areas:** Ensure interactive elements (buttons) are at least 44px in height to maintain accessibility during motion.

## Elevation & Depth
Depth is conveyed through a combination of **Tonal Layers** and **Ambient Shadows**.

- **Cards:** Use a 1pt border (`#E5E8EF`) as the primary container definition. 
- **Shadows:** Apply a very soft, diffused shadow to floating elements: `box-shadow: 0 4px 12px rgba(26, 29, 36, 0.05)`.
- **Z-Index Strategy:** Navigation bars and "Next Turn" instructions sit at the highest elevation (z-index 1000) with a light backdrop blur to maintain focus on the map or core content underneath.

## Shapes
The shape language is "Softly Geometric." 

- **Buttons:** Use a 12px radius to balance professional structure with approachability.
- **Speech Bubbles / AI Cards:** Use a larger 16px radius to create a friendlier, conversation-oriented appearance.
- **Inputs:** Follow the 12px button radius for consistency across the interaction layer.

## Components
- **Buttons:** 
  - *Primary:* Blue background, white text, 12px radius, 48px height for main actions.
  - *Secondary:* White background, 1pt border (`#E5E8EF`), Primary Blue text.
- **AI Voice Bubbles:** 16px radius. AI responses use the Accent Violet as a subtle top-border accent or icon color to distinguish from system messages.
- **Cards:** White background, 1pt border, 16px corner radius. Padding is strictly 16px.
- **Input Fields:** 12px radius, `#F7F8FA` background with a subtle border that darkens on focus.
- **Chips/Tags:** Used for "Quick Replies" or "Categories." 32px height, pill-shaped, using a light tint of the Primary color for the background.
- **Navigation Progress:** A thin linear progress bar using Primary Blue, located at the very top of the content area.