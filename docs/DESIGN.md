---
name: Cyber-Modern IDE
colors:
  surface: '#131314'
  surface-dim: '#131314'
  surface-bright: '#3a393a'
  surface-container-lowest: '#0e0e0f'
  surface-container-low: '#1c1b1c'
  surface-container: '#201f20'
  surface-container-high: '#2a2a2b'
  surface-container-highest: '#353436'
  on-surface: '#e5e2e3'
  on-surface-variant: '#b9cacb'
  inverse-surface: '#e5e2e3'
  inverse-on-surface: '#313031'
  outline: '#849495'
  outline-variant: '#3a494b'
  surface-tint: '#00dce6'
  primary: '#e3fdff'
  on-primary: '#00373a'
  primary-container: '#00f3ff'
  on-primary-container: '#006b71'
  inverse-primary: '#00696f'
  secondary: '#adc7ff'
  on-secondary: '#002e68'
  secondary-container: '#4a8eff'
  on-secondary-container: '#00285b'
  tertiary: '#fef5ff'
  on-tertiary: '#490080'
  tertiary-container: '#ecd2ff'
  on-tertiary-container: '#862dd4'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#6ff6ff'
  primary-fixed-dim: '#00dce6'
  on-primary-fixed: '#002022'
  on-primary-fixed-variant: '#004f53'
  secondary-fixed: '#d8e2ff'
  secondary-fixed-dim: '#adc7ff'
  on-secondary-fixed: '#001a41'
  on-secondary-fixed-variant: '#004493'
  tertiary-fixed: '#f0dbff'
  tertiary-fixed-dim: '#ddb7ff'
  on-tertiary-fixed: '#2c0051'
  on-tertiary-fixed-variant: '#6900b3'
  background: '#131314'
  on-background: '#e5e2e3'
  surface-variant: '#353436'
typography:
  display-lg:
    fontFamily: Geist
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Geist
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Geist
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-base:
    fontFamily: Geist
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  code-sm:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-caps:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  xs: 4px
  sm: 12px
  md: 24px
  lg: 48px
  xl: 80px
  gutter: 24px
  margin: 32px
---

## Brand & Style

The design system is engineered for a high-energy, global programming audience. The brand personality is **Tech-Forward** and **Cyber-Modern**, prioritizing technical precision with a futuristic edge. The UI is designed to evoke a sense of "Flow State"—the immersive psychological state of a developer deep in code.

The visual style is a hybrid of **Glassmorphism** and **Corporate Modern**, utilizing frosted-glass surfaces, subtle neon glows, and structural grid patterns that mimic digital blueprints. The interface should feel like a premium Integrated Development Environment (IDE) translated into a seamless educational experience. Interactivity is key; every action should feel responsive, utilizing motion cues like terminal cursors and syntax-style color shifts.

## Colors

The design system defaults to a deep **dark mode** to reduce eye strain during long coding sessions. 

- **Primary & Action:** Neon Cyan (#00F3FF) serves as the high-visibility primary color for calls-to-action and active states, while Deep Electric Blue (#007BFF) provides a stable structural pairing.
- **Surface & Neutrals:** Dark Obsidian (#00A0A0B) is the bedrock for the background, with Slate Gray (#1E293B) used for secondary containers and borders to maintain a low-friction, high-contrast hierarchy.
- **Accents:** Vibrant Purple (#A855F7) is reserved for gamification, progress tracking, and specialized technical categories. Emerald Green (#10B981) is strictly for success states and validated code submissions.

## Typography

Typography in the design system balances sleek readability with technical utility. 

**Geist** is the primary typeface for all UI elements, offering a clean, minimal, and developer-friendly aesthetic that remains legible at various scales. It is used for all headlines, subheaders, and body copy to provide a modern, structural feel.

**JetBrains Mono** is employed for all code blocks, technical metadata, and labels. Its increased x-height and distinct characters are optimized for technical clarity. Use `label-caps` for small tags, category identifiers, and "system-status" messages to reinforce the "cyber-modern" aesthetic.

## Layout & Spacing

The design system utilizes a **12-column fluid grid** for desktop, collapsing to a **4-column grid** on mobile. The spacing rhythm is based on a strict 8px increment system to ensure alignment with standard developer tooling.

- **Desktop:** 32px margins with 24px gutters. Content blocks should align to the grid to create a structured, "modular" look.
- **Mobile:** 16px margins with 12px gutters.
- **Safe Zones:** Use `spacing.lg` for section breathing room and `spacing.md` for internal card padding.

The layout philosophy emphasizes **modular density**, where information is grouped into clear, logical blocks (containers) separated by consistent gutters, mimicking the layout of a multi-pane IDE.

## Elevation & Depth

Depth is achieved through **Glassmorphism** and **Backdrop Blurs** rather than traditional heavy shadows.

- **Level 1 (Base):** Obsidian background with a subtle grid pattern overlay (1px lines, 5% opacity).
- **Level 2 (Containers):** Slate Gray with 60% opacity and a `20px` backdrop blur. Borders should be 1px solid with 10% white opacity to define edges.
- **Level 3 (Floating Elements):** Popovers and modals use a higher opacity background with a subtle **Neon Cyan glow** (`box-shadow: 0 0 20px rgba(0, 243, 255, 0.15)`).
- **Interactions:** Hover states on interactive cards should increase the border brightness and the intensity of the colored glow.

## Shapes

The shape language is consistently **Rounded**, using a 12px-16px radius for primary UI containers.

- **Standard Elements:** 8px (`0.5rem`) for inputs and smaller buttons.
- **Main Cards/Containers:** 16px (`1rem`) for primary content areas and glassmorphic modules.
- **Feature Highlights:** 24px (`1.5rem`) for large promotional banners or hero sections.

This roundedness balances the "hard" technical feel of the monospace type and grid patterns, making the platform feel approachable and modern rather than cold and industrial.

## Components

- **Buttons:** Primary buttons use a solid Neon Cyan fill with Dark Obsidian text. Secondary buttons are "ghost" style with a Cyan border and a subtle glow on hover.
- **Chips/Tags:** Use JetBrains Mono. Tags should have a 1px border matching the accent color (e.g., Purple for 'Advanced', Green for 'Completed').
- **Input Fields:** Styled to look like terminal lines. A solid bottom border that glows when focused, and a "blinking cursor" vertical bar for the active state.
- **Cards:** The core of the UI. Must use the Glassmorphism style: semi-transparent Slate Gray background, 16px rounded corners, and a 1px border.
- **Progress Bars:** Thin, high-contrast bars using a Neon Cyan to Deep Blue gradient. Completed sections should "pulse" with Emerald Green.
- **Code Editor:** Custom syntax highlighting using the full palette (Purple for keywords, Cyan for variables, Green for strings).
- **Interactive Grids:** Dashboard elements should snap to the grid, with "active" modules showing a faint cyan outline.