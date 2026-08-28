# Fidel Design System — Monopo Saigon Editorial Reference
> Liquid iridescence behind editorial silence — a monochrome editorial gallery floating on molten light.

**Theme:** Light & Editorial Monochrome (with Iridescent Hero Backdrop)

Fidel runs on radical monochrome discipline: pure black and white with whisper-thin grays, wrapped around massive Roobert/Inter typography that breathes across full-bleed canvases. The signature contrast lives between austere editorial restraint (sharp 0px corners on navigation, cards, tables, and text links, generous whitespace, 4px-based rhythm) and a single expressive gesture — full-pill 75px-radius buttons that float like liquid over imagery. Hero environments lean into iridescent, fluid, chromatic atmospheres (greens dissolving into amber into deep oxblood) while the interface itself never picks up a hue, creating the feeling of a black-and-white editorial gallery floating on a river of liquid light.

---

## 1. Color Tokens

| Name | Value | Token | Role |
|------|-------|-------|------|
| Obsidian | `#000000` | `--color-obsidian` | Primary text, SVG strokes, overlay fills — pure black carries foreground information |
| Paper | `#ffffff` | `--color-paper` | Light text on dark surfaces, inverse labels, high-contrast captions |
| Inkstone | `#181818` | `--color-inkstone` | Footer body copy and secondary headings — softened black for long-form blocks |
| Felt Gray | `#6d6d6d` | `--color-felt-gray` | Muted helper text, address blocks, legal copy — quiet annotations |
| Slate Pill | `#636363` | `--color-slate-pill` | Filled neutral button background — compliance / neutral actions |
| Ash Mist | `#9a9a9a` | `--color-ash-mist` | Mid-tone neutral for low-contrast surfaces |
| Pewter | `#808080` | `--color-pewter` | Secondary mid-tone neutral for hover layers |
| Iridescent Fade | `linear-gradient(90deg, rgb(160, 224, 171), rgb(255, 172, 46) 50%, rgb(165, 45, 37))` | `--gradient-iridescent-fade` | Chromatic accent appearing exclusively inside hero media / fluid backdrops |

---

## 2. Typography

Primary Typeface: **Inter** / **Roobert** (Geometric-humanist sans with wide weight range from 300 whisper through 600 anchor).

### Type Scale
| Role | Size | Line Height | Weight | Token |
|------|------|-------------|--------|-------|
| caption | 12px | 1.19 | 400 | `--text-caption` |
| body-sm | 16px | 1.15 | 400 | `--text-body-sm` |
| body | 18px | 1.21 | 400 | `--text-body` |
| subheading | 39px | 1.19 | 400 | `--text-subheading` |
| subheading-lg | 45px | 1.15 | 400 | `--text-subheading-lg` |
| heading-sm | 54px | 1.39 | 400 | `--text-heading-sm` |
| heading (whisper) | 78px | 1.10 | 300 | `--text-heading` |
| heading-lg (anchor) | 94px | 0.76 | 400 | `--text-heading-lg` |
| display | 140px-225px | 1.25 | 400 | `--text-display` |

---

## 3. Spacing & Shapes

- **Base unit:** 4px
- **Density:** Spacious editorial pacing (section gaps 46px, card padding 34px, element gaps 14px)
- **Container Max-Width:** 1078px
- **Border Radius:**
  - Cards: `0px`
  - Images: `0px`
  - Inputs: `0px`
  - Tables: `0px`
  - Buttons: `75px` (Full Pill)
  - Tags / Badges: `75px` (Full Pill)

---

## 4. Components

### Ghost Pill Button (Dark Surface)
Transparent background, 1px solid `rgba(255, 255, 255, 0.3)` border, `#ffffff` text, 75px border-radius, 11px vertical and 33px horizontal padding.

### Ghost Pill Button (Light Surface)
Transparent background, 1px solid `#000000` border, `#000000` text, 75px border-radius, 11px vertical and 33px horizontal padding.

### Iridescent Hero Backdrop
Full-viewport organic gradient: soft sage green (`rgb(160, 224, 171)`) dissolving through molten amber (`rgb(255, 172, 46)`) into deep oxblood (`rgb(165, 45, 37)`). Applied as fluid backdrop behind monumental typography.

---

## 5. Absolute Rules

- Zero Emojis anywhere in the codebase, UI, labels, or documentation.
- No shadows or elevation — flat surfaces with hairline 1px borders.
- Strict 0px vs 75px binary radius discipline.
