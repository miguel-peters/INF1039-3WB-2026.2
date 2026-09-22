---
name: Academic Warmth
colors:
  surface: '#fcf9f1'
  surface-dim: '#dcdad2'
  surface-bright: '#fcf9f1'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f6f3eb'
  surface-container: '#f1eee6'
  surface-container-high: '#ebe8e0'
  surface-container-highest: '#e5e2da'
  on-surface: '#1c1c17'
  on-surface-variant: '#45464e'
  inverse-surface: '#31312b'
  inverse-on-surface: '#f3f1e9'
  outline: '#75777f'
  outline-variant: '#c5c6cf'
  surface-tint: '#505d84'
  primary: '#061639'
  on-primary: '#ffffff'
  primary-container: '#1d2b4f'
  on-primary-container: '#8593bd'
  inverse-primary: '#b8c5f2'
  secondary: '#7f5700'
  on-secondary: '#ffffff'
  secondary-container: '#febe51'
  on-secondary-container: '#724d00'
  tertiary: '#001c17'
  on-tertiary: '#ffffff'
  tertiary-container: '#00332b'
  on-tertiary-container: '#609f91'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dae2ff'
  primary-fixed-dim: '#b8c5f2'
  on-primary-fixed: '#0a1a3d'
  on-primary-fixed-variant: '#38466b'
  secondary-fixed: '#ffdead'
  secondary-fixed-dim: '#fabb4f'
  on-secondary-fixed: '#281900'
  on-secondary-fixed-variant: '#604100'
  tertiary-fixed: '#aeefdf'
  tertiary-fixed-dim: '#93d3c3'
  on-tertiary-fixed: '#00201a'
  on-tertiary-fixed-variant: '#045045'
  background: '#fcf9f1'
  on-background: '#1c1c17'
  surface-variant: '#e5e2da'
typography:
  display-lg:
    fontFamily: Newsreader
    fontSize: 3.5rem
    fontWeight: '600'
    lineHeight: 4rem
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Newsreader
    fontSize: 2.25rem
    fontWeight: '600'
    lineHeight: 2.75rem
    letterSpacing: -0.015em
  headline-lg:
    fontFamily: Newsreader
    fontSize: 2.25rem
    fontWeight: '600'
    lineHeight: 2.75rem
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Newsreader
    fontSize: 1.75rem
    fontWeight: '600'
    lineHeight: 2.25rem
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Newsreader
    fontSize: 1.5rem
    fontWeight: '500'
    lineHeight: 2rem
    letterSpacing: 0em
  headline-sm:
    fontFamily: Newsreader
    fontSize: 1.25rem
    fontWeight: '500'
    lineHeight: 1.75rem
    letterSpacing: 0em
  title-md:
    fontFamily: IBM Plex Sans
    fontSize: 1.125rem
    fontWeight: '600'
    lineHeight: 1.5rem
    letterSpacing: -0.005em
  body-lg:
    fontFamily: IBM Plex Sans
    fontSize: 1.125rem
    fontWeight: '400'
    lineHeight: 1.75rem
  body-md:
    fontFamily: IBM Plex Sans
    fontSize: 1rem
    fontWeight: '400'
    lineHeight: 1.5rem
  body-sm:
    fontFamily: IBM Plex Sans
    fontSize: 0.875rem
    fontWeight: '400'
    lineHeight: 1.25rem
  label-lg:
    fontFamily: IBM Plex Sans
    fontSize: 0.875rem
    fontWeight: '600'
    lineHeight: 1.25rem
    letterSpacing: 0.01em
  label-md:
    fontFamily: IBM Plex Sans
    fontSize: 0.75rem
    fontWeight: '600'
    lineHeight: 1rem
    letterSpacing: 0.04em
  code-sm:
    fontFamily: IBM Plex Sans
    fontSize: 0.8125rem
    fontWeight: '500'
    lineHeight: 1.125rem
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  gutter: 1.5rem
  gutter-sm: 1rem
  margin: 3rem
  margin-sm: 1.25rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style

The design system establishes an environment of scholarly rigor balanced with personal warmth. Aimed at university students, graduate researchers, and peer tutors, the interface rejects cold, hyper-corporate edtech tropes in favor of an editorial, campus-inspired atmosphere. 

Visual direction balances editorial minimalism with tactile academic grounding:
- **Tone:** Studious, focused, encouraging, and intellectually credible.
- **Aesthetic Movement:** Modern Editorial Academic. Crisp typography, disciplined grid structures, muted paper-like foundations, and purposeful highlights inspired by archival reading rooms and collegiate libraries.
- **Emotion:** Reduces cognitive fatigue and academic anxiety, fostering confidence, deep study sessions, and straightforward scheduling.

## Colors

The palette is derived from collegiate library materiality—aged paper, deep midnight ink, warm reading lamps, and historic bookcloth bindings.

### Palette Architecture
- **Canvas / Background (`#f6f3eb`):** Off-White Amadeirado. Mimics heavy cream book stock, cutting glare during extended study periods.
- **Primary / Structural (`#1d2b4f`):** Azul Tempestade. Deep scholarly navy utilized for high-contrast typography, primary buttons, structural lines, and focused states.
- **Secondary / Accent (`#e2a63b`):** Âmbar Dourado. Applied sparingly for ratings, tutor verification badges, booking alerts, and interactive highlights.
- **Tertiary / Success (`#2f6f62`):** Azul Petróleo Escuro. Replaces aggressive neon greens with an authoritative, restrained academic teal for confirmed sessions, paid statuses, and positive feedback.
- **Critical / Error (`#A83f32`):** Carmim Médio. Used for missed sessions, cancellations, input validation failures, and urgent deadlines.
- **Secondary Text (`rgba(0, 0, 0, 0.72)`):** Muted black ensuring legibility standards (WCAG AAA) across the off-white ground without harsh visual fragmentation.

### Functional Ratios
Maintain a strict 70-20-10 distribution: 70% canvas and light surface cards (`#f6f3eb`, `#ffffff`), 20% primary structural ink (`#1d2b4f`), and 10% combined accent or status indicators (`#e2a63b`, `#2f6f62`, `#A83f32`).

## Typography

The typographical pairing unites academic heritage with technical precision:
- **Headlines (Newsreader):** Chosen for its sturdy, literary serif construction that retains clarity and elegance at display scales while referencing classic university publications and reference monographs.
- **Body & Controls (IBM Plex Sans):** An engineered grotesque with clear letterforms, open counters, and high distinction between ambiguous characters (`1`, `l`, `I`), critical for syllabi, session logs, timestamps, and equations.

### Hierarchy & Rules
- Headings larger than 32px automatically compress via mobile tokens on viewports below 768px.
- Use sentence case across all headings and interfaces to maintain an approachable, conversational tone.
- Small labels and data tags utilize `label-md` with slight letter spacing (`0.04em`) and uppercase styling only when denoting status or department categorizations.

## Layout & Spacing

Layout adheres to an architectural rhythm built on an 8px modular baseline (0.5rem intervals). 

### Grid Rules
- **Desktop (1024px+):** 12-column layout, 48px (`margin`) outer bounds, 24px (`gutter`) column separation. Max-width locked at 1280px for balanced reading spans.
- **Tablet (640px–1023px):** 8-column layout, 32px outer bounds, 20px column separation.
- **Mobile (<640px):** 4-column layout, 20px (`margin-sm`) outer boundaries, 16px (`gutter-sm`) gutters.

### Spacing Behaviors
- Use `space-md` for standard component internals (button padding, input field padding).
- Use `space-lg` to separate modular cards, form field groups, and mentor biography segments.
- Use `space-xl` strictly for distinct section milestones on dashboard and overview templates.

## Elevation & Depth

To preserve an authentic paper-and-desk tactile experience, this design system avoids synthetic, blurry elevation drop shadows. Depth is communicated strictly through surface layering and delicate border contrasts:

- **Base Ground:** `#f6f3eb` (Off-White canvas).
- **Surface Elevation 1 (Cards, Modules):** Crisp `#ffffff` backed by a 1px solid stroke in `rgba(29, 43, 79, 0.08)`.
- **Surface Elevation 2 (Dropdowns, Floating Palettes, Modals):** Crisp `#ffffff` with a double perimeter: a 1px border of `rgba(29, 43, 79, 0.12)` complemented by a soft, directional ambient shadow tinted in deep navy: `0 8px 24px -4px rgba(29, 43, 79, 0.08)`.
- **Active / Dragged Items:** Raised via `0 12px 32px -4px rgba(29, 43, 79, 0.14)`.

## Shapes

The interface embraces a restrained, architectural curvature (`roundedness: 1`). 

- **Inputs, Buttons, Badges:** 4px (`0.25rem`) border radius. This subtle curvature softens interactions while maintaining the disciplined alignment of printed texts.
- **Cards, Panels, Modals:** 8px (`0.5rem`) border radius (`rounded-lg`). Prevents large panels from looking aggressive while preserving clean vertical axes.
- **Avatars & Status Indicators:** Full circle (`50%` / pill) reserved exclusively for profile imagery and real-time availability indicator dots.

## Components

### Buttons
- **Primary:** Background `#1d2b4f`, label `#ffffff` (`label-lg`), height 44px, padding 0 20px, radius 4px. Hover transforms to `#131d36`. Focus displays a 2px offset outline in `#e2a63b`.
- **Secondary / Outline:** Background transparent, 1.5px solid stroke `#1d2b4f`, label `#1d2b4f`. Hover fills with `rgba(29, 43, 79, 0.04)`.
- **Tertiary / Subtle:** Background transparent, label `#1d2b4f`, underlined on hover.
- **Accent (Schedule / Book Session):** Background `#e2a63b`, label `#1d2b4f` (`font-weight: 600`). Hover transforms to `#cca32f`.

### Chips & Subject Badges
- **Discipline Tag:** Height 28px, background `rgba(29, 43, 79, 0.06)`, label `#1d2b4f` (`label-md`), radius 4px, padding 0 10px.
- **Status Badges:** 
  - Verified Tutor: `#e2a63b` background at 15% opacity, text `#9c6d1a`, with a solid star glyph.
  - Confirmed Session: `#2f6f62` background at 12% opacity, text `#2f6f62`.
  - Cancelled / Overdue: `#A83f32` background at 12% opacity, text `#A83f32`.

### Inputs & Selectors
- **Text Inputs:** Height 44px, background `#ffffff`, 1px solid border in `rgba(29, 43, 79, 0.2)`. Internal text `#000000` (`body-md`), placeholder `rgba(0, 0, 0, 0.45)`. Radius 4px.
- **Focus State:** Border shifts to 1.5px solid `#1d2b4f` with no blurry glow.
- **Error State:** Border shifts to 1.5px solid `#A83f32`, with helper text rendering in Carmim Médio below the field.

### Selection Controls
- **Checkboxes & Radios:** 18px square (checkbox) or circle (radio), 1.5px border `#1d2b4f`. Checked state fills `#1d2b4f` with crisp white checkmark/dot.

### Cards & Lesson Slots
- **Tutor Profile Card:** Background `#ffffff`, 1px border `rgba(29, 43, 79, 0.08)`, radius 8px, padding 20px. Displays tutor avatar (48px circle), name in `headline-sm`, departmental chips, hourly rate in `IBM Plex Sans`, and primary action button.
- **Calendar Time-Slot:** Background `#ffffff`, border 1px solid `rgba(29, 43, 79, 0.12)`, radius 4px. Selected state switches background to `#1d2b4f`, text `#ffffff`.

### Academic Document & Resource List
- Inset table with alternating light rows (`transparent` vs `rgba(29, 43, 79, 0.02)`), bottom borders of 1px `rgba(29, 43, 79, 0.06)`, with file format icons (PDF, Code, Tex) tinted in `#1d2b4f`.