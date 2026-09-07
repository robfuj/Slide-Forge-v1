---
name: slide-forge
description: "Generate presentation decks in five modes with embedded consultant frameworks."
version: "1.0.0"
author: "Fujita (robfuj), Hermes Agent"
license: "MIT"
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [decks, presentations, marp, slidev, pptx, consulting]
    related_skills: []
---

# SLIDE FORGE Skill

**One skill, five production modes, zero external dependencies.**

This skill packages the complete deck generation ecosystem: markdown authorship, native PPTX editing, illustrated courseware, image/PDF reconstruction, and full-process management — all with built-in validation loops and consultant-grade frameworks (McKinsey Pyramid Principle, SCQ, MECE, Storyboarding; Charlie Hills marketing framework).

---

## QUICK START

```bash
# Install (copy to your agent's skills directory)
cp -r slide-forge ~/.hermes/skills/creative/  # or ~/.claude/skills/, ~/.codex/skills/

# Use
"Use slide-forge skill. Build a 12-slide deck about <topic> from attached content using mode: <mode>."
```

**Modes:**
- `markdown` — Marp/Slidev/Guizang/Frontend (HTML or PPTX/PDF export)
- `native` — ppt-master/slide-skill/deck-dna (editable PPTX, live charts)
- `illustrated` — Baoyu/PPTAgent (blackboard, watercolor, comic, sketch)
- `reconstruct` — Gorden/LRriver/NBLM (images/PDFs → editable PPTX)
- `studio` — codex-slides/Presenton (full UI: outline→style→render→edit→export)

---

## ARCHITECTURE

```
deck-builder/
├── SKILL.md                    # This file (entry point)
├── modes/
│   ├── markdown/               # Markdown → slides
│   │   ├── workflow.md         # Phase 1-6: content→outline→style→render→QA→export
│   │   ├── templates/          # Marp, Slidev, Guizang A/B, Frontend presets
│   │   ├── validators/         # schema, visual QA, export checks
│   │   └── scripts/            # build, export, preview
│   ├── native/                 # Native PPTX (editable shapes, charts)
│   │   ├── workflow.md         # DNA extraction → word budget → build → QA
│   │   ├── templates/          # Consulting, academic, corporate presets
│   │   ├── validators/         # SVG gate, placeholder scan, chart bind check
│   │   └── scripts/            # extract-dna, measure-budget, build, qa-render
│   ├── illustrated/            # Courseware & knowledge cards
│   │   ├── workflow.md         # Style pick → copy first → generate → review
│   │   ├── styles/             # Blackboard, watercolor, chalkboard, comic
│   │   ├── validators/         # Visual consistency, text-image alignment
│   │   └── scripts/            # gen-images, compose-slides, export-pptx
│   ├── reconstruct/            # Images/PDFs → editable PPTX
│   │   ├── workflow.md         # OCR/VLM → layer separation → compose → validate
│   │   ├── pipelines/          # Image2PPTX, PDF2PPTX, hybrid
│   │   ├── validators/         # Layer fidelity, text positioning, chart recovery
│   │   └── scripts/            # ocr-extract, separate-layers, assemble, validate
│   └── studio/                 # Full production interface
│       ├── workflow.md         # Research→outline→style→render→edit→present→export
│       ├── templates/          # 20+ visual systems, brand kits
│       ├── validators/         # Real-time preview, export smoke test
│       └── scripts/            # project-init, generate, edit, export, deploy
├── consultants/                # Embedded frameworks (no external refs)
│   ├── pyramid-principle.md    # Answer-first, MECE grouping
│   ├── scq-framework.md        # Situation-Complication-Question-Answer
│   ├── mece.md                 # Mutually exclusive, collectively exhaustive
│   ├── storyboarding.md        # Slide titles tell the story
│   └── charlie-hills.md        # Hook→value→proof→CTA (marketing decks)
├── schemas/
│   ├── deck.json               # Universal deck schema (slides, layout, audience)
│   ├── slide.json              # Per-slide contract
│   └── dna-sheet.json          # Extracted design DNA
├── references/
│   ├── checklist.md            # P0/P1/P2/P3 preflight & postflight
│   ├── layouts.md              # All layout types with specs
│   ├── themes.md               # Color systems, font pairs, spacing scales
│   ├── presenter-mode.md       # Dual-window, notes, timer, rehearse
│   └── export-specs.md         # PPTX, PDF, HTML, PNG requirements
└── scripts/
    ├── preflight.py            # Environment, deps, font checks
    ├── build.py                # Orchestrates mode-specific build
    ├── qa_render.py            # PDF→images→visual diff→report
    ├── validate.py             # Schema, gates, publish criteria
    └── export.py               # Multi-format export with validation
```

---

## MODE 1: MARKDOWN (Marp / Slidev / Guizang / Frontend)

### When to Use
- Training, courseware, technical docs
- Version-controlled content (edit .md → regenerate)
- Need HTML *and* PPTX/PDF from same source
- Team collaboration on content, not design

### Workflow (6 Phases)

**Phase 1: Content Intake**
- Accept: raw markdown, outline, bullet points, or attached documents
- Extract: key messages, data points, narrative arc
- Output: `content.md` structured with slide boundaries (`---`)

**Phase 2: Outline & Storyboard**
- Apply **SCQ Framework** (consultants/scq-framework.md)
- Apply **Pyramid Principle** (consultants/pyramid-principle.md)
- Apply **Storyboarding** (consultants/storyboarding.md)
- Produce: `outline.json` with slide-level {title, layout, key_message, supporting_points}

**Phase 3: Style Selection**
| Style | Best For | Engine |
|-------|----------|--------|
| Marp Standard | Training, handouts | Marp CLI |
| Slidev Code | Live coding, formulas, demos | Slidev |
| Guizang Style A | Narrative, editorial, personal | Guizang (magazine/ink) |
| Guizang Style B | Analysis, methodology, product | Guizang (Swiss grid) |
| Frontend Presets | Custom visual, animation-rich | Frontend Slides |
- Test: render 1 body slide → verify fonts, spacing, contrast
- Output: `style.config.json`

**Phase 4: Render**
- Marp: `marp-cli content.md --pptx --pdf --html`
- Slidev: `slidev build content.md && slidev export`
- Guizang: `node scripts/build.js --style=A|B --input=content.md`
- Frontend: `node scripts/build.html --preset=<name> --input=content.md`
- Output: `deck.html`, `deck.pptx`, `deck.pdf`, `slides/*.png`

**Phase 5: QA Gate** (validators/)
- Schema: validate against `schemas/deck.json`
- Visual: render each slide → check overflow, alignment, contrast
- Export: verify PPTX opens, charts editable, fonts embedded
- Gate: **PASS** = all checks green; **FAIL** = auto-fix or escalate

**Phase 6: Export & Deliver**
- Primary: `deck.pptx` (Marp/Slidev) or `deck.html` (Guizang/Frontend)
- Secondary: `deck.pdf`, `slides/*.png`
- Metadata: `deck.json` manifest with slide map, styles, version

### Templates (Built-in)

**Marp Template** (`templates/marp-base.md`):
```markdown
---
marp: true
theme: uncover
paginate: true
header: '{{title}}'
footer: '{{org}} | {{date}}'
size: 16:9
---

# {{title}}
{{subtitle}}

---

## {{section_1}}
{{content_1}}

---
```

**Slidev Template** (`templates/slidev-base.md`):
```markdown
---
theme: seriph
highlighter: shiki
lineNumbers: true
drawings:
  persist: false
transition: slide-left
mdc: true
---

# {{title}}
{{subtitle}}

---

## {{section_1}}
{{content_1}}

---
```

**Guizang Style A** (`templates/guizang-a.html`): Magazine/ink, hero/non-hero rhythm, WebGL hero backgrounds

**Guizang Style B** (`templates/guizang-b.html`): Swiss grid, single anchor color, hairline rules, extreme type contrast

**Frontend Presets** (`templates/frontend-presets/`): 10 curated design systems (bold, minimal, data-dense, editorial, dark, light, corporate, startup, academic, creative)

---

## MODE 2: NATIVE PPTX (ppt-master / slide-skill / deck-dna)

### When to Use
- Client must edit text, charts, tables in PowerPoint
- Native charts that update when data changes
- Corporate template compliance (master slides)
- Repeated report generation (monthly, quarterly)

### Workflow (5 Phases)

**Phase 1: DNA Extraction** (deck-dna method)
- Input: 2-3 approved reference PPTX files (designer-built, signed off)
- Extract:
  - Layout grammar: image/text ratios, grid positions, divider rules
  - Color reality: actual slide colors (not theme XML)
  - Type scale: heading/body/caption sizes, weights, line heights
  - Icon treatment: stroke weight, corner radius, fill vs outline
  - Chart style: axis treatment, data labels, legend position
  - Word budget: median words/slide across references (hard ceiling)
- Output: `dna-sheet.json` (schemas/dna-sheet.json)

**Phase 2: Content Planning**
- Apply **Pyramid Principle** + **MECE** (consultants/)
- Draft outline with slide-level word counts ≤ measured budget
- Assign layout type per slide (cover, bullets, metric, 2x2, chart, divider, etc.)
- Output: `plan.json`

**Phase 3: Build on Blank Base**
- Start from empty PPTX (no template baggage)
- Programmatically apply DNA:
  - Create slide layouts matching extracted grammar
  - Apply exact color values, type scales, spacing
  - Build native charts (python-pptx chart objects, not images)
  - Insert native tables, smart art shapes
- Output: `draft.pptx`

**Phase 4: QA Render Loop**
- Convert `draft.pptx` → PDF → PNG per slide (LibreOffice + Poppler)
- Agent reviews each slide image:
  - Text overflow / clipping
  - Element collisions
  - Margin alignment
  - Font substitution artifacts
  - Chart render fidelity
- Fix → re-render → repeat until clean
- Output: `final.pptx` + `qa-report.json`

**Phase 5: Template Fill (Optional)**
- If client provides strict `.potx` master:
  - `slide-skill template-fill master.potx --content plan.json -o branded.pptx`
  - Reports: text overflow risks, leftover placeholders
  - Preserves master design 1:1

### Templates (Built-in)

**Consulting Exhibit DNA** — dense, chart-heavy, small multiples, footer metadata
**Academic Defense DNA** — structured, numbered, appendix-ready, school-template compatible
**Corporate Quarterly DNA** — KPI cards, trend charts, consistent divider rhythm
**Minimalist Keynote DNA** — large type, whitespace, single anchor color per section

---

## MODE 3: ILLUSTRATED (Baoyu / PPTAgent)

### When to Use
- Science communication, knowledge cards, social media decks
- Blackboard, watercolor, chalkboard, comic aesthetics
- Research papers → presentation (PPTAgent)
- Visual storytelling > data density

### Workflow (4 Phases)

**Phase 1: Style Lock**
- Pick ONE style: Blackboard, Watercolor, Chalkboard, Comic, Sketch, XHS-card
- Test: generate 1 body slide → verify illustration style, text legibility
- Lock: style config frozen for full deck

**Phase 2: Copy First, Images Second**
- Write ALL slide copy in `content.md` first (no images yet)
- Apply **Storyboarding** — slide titles must read as coherent narrative
- Word budget: stricter (illustrated slides hold less text)

**Phase 3: Generate & Compose**
- Baoyu Slide Deck: `baoyu-slide-deck --style=<name> --input=content.md`
  - Generates full-page backgrounds + illustrations + text overlay
  - Text changes → re-generate page (illustration regenerates)
- Baoyu Design: `baoyu-design --export=pptx --input=deck.html`
  - Edit in HTML first (adjust layouts, animations)
  - Export via Playwright + PptxGenJS (editable or screenshot mode)
- PPTAgent: `pptagent --paper=<pdf> --refs=<reference_decks> --output=deck.pptx`
  - Analyzes reference decks for slide types & schemas
  - Two-stage: outline → iterative edit actions → final deck
  - Verify: conclusions/numbers vs original paper

**Phase 4: Validate & Export**
- Visual consistency: same style markers across all slides
- Text-image alignment: no text on busy background areas
- Export: PPTX (editable layers) or HTML (browser playback)

### Styles (Built-in)
| Style | Vibe | Best For |
|-------|------|----------|
| Blackboard | Chalk on dark, hand-drawn | Teaching, math, concepts |
| Watercolor | Soft washes, organic edges | Storytelling, intros, covers |
| Chalkboard | Structured chalk, grid lines | Technical, process, formulas |
| Comic | Panels, speech bubbles, bold lines | Engaging, sequential, youth |
| Sketch | Pencil lines, loose | Ideation, workshops, drafts |
| XHS Card | Xiaohongshu ratio, emoji, emoji | Social, knowledge cards |

---

## MODE 4: RECONSTRUCT (Gorden / LRriver / NBLM)

### When to Use
- Only have PDF/PNG/JPG of existing slides
- Need editable PPTX (text, shapes, charts separated)
- Reverse-engineer legacy decks
- NotebookLM exports → PPTX

### Workflow (4 Phases)

**Phase 1: Input Classification**
- PDF (native text) → PDF.js extraction + layout analysis
- Images (JPG/PNG) → Gemini OCR + VLM layout analysis
- Mixed → hybrid pipeline per page

**Phase 2: Layer Separation** (Gorden 4-layer method)
1. **Background** — full-slide image, no text/UI
2. **Skeleton/Frame** — containers, dividers, grid lines, shapes
3. **Icons & Decorations** — individual graphic elements
4. **Text** — OCR'd text blocks with font/size/color/position
- Each layer saved as separate asset

**Phase 3: Re-assemble in PPTX**
- Create blank slide matching source dimensions
- Place background → skeleton → icons → text boxes (position-matched)
- Native charts: attempt VLM chart reconstruction → python-pptx chart object
- Tables: reconstruct as native PPTX tables
- Font embedding: extract used fonts → embed in PPTX

**Phase 4: Validate & Polish**
- Side-by-side: original vs reconstructed (pixel diff)
- Text edit test: change a number → verify chart updates (if native)
- Font fallback check: open on clean machine
- Output: `reconstructed.pptx` + `fidelity-report.json`

### Pipelines (Built-in)
- **Image2PPTX** (Gorden): GPT-4V vision → 4-layer extraction → python-pptx compose
- **PDF2PPTX** (NBLM): PDF.js text + Gemini OCR for images → hybrid layer sep
- **VLM-First** (LRriver/AIPPT): OCR + VLM analysis → manifest → validation → export
- **Generative Editable** (LRriver): full reconstruction with element grouping, layer ordering

---

## MODE 5: STUDIO (codex-slides / Presenton)

### When to Use
- Ongoing, repeated deck production
- Team collaboration (outline → review → generate → edit)
- Need browser UI for non-technical stakeholders
- Model/router management, deployment, cost control

### Workflow (7 Phases)

**Phase 1: Project Init**
- `codex-slides init <project>` or Presenton web UI
- Creates: `project.json`, `styles/`, `templates/`, `assets/`

**Phase 2: Research & Outline**
- Deep research (integrated web search, document parsing)
- Outline editor: drag-drop sections, slide count estimator
- Stakeholder review: comment threads on outline

**Phase 3: Style Discovery** ("show, don't tell")
- Generate 3-5 visual preview cards per style
- Stakeholder picks → style locked
- Style = layout system + color palette + font pair + component library

**Phase 4: Render**
- Fast mode: parallel page generation (10+ slides in 4-5 min)
- Each slide = full visual canvas (image-native)
- Live preview: watch chain research→outline→style→render

**Phase 5: Edit & Steer**
- Per-slide: edit text, swap images, adjust layout
- Global: theme swap, font swap, color swap (instant re-render)
- Version history: every edit checkpointed

**Phase 6: Present & Rehearse**
- Dual-window presenter mode (notes, timer, annotations)
- Rehearse: timing analysis, slide transition practice
- Auto-advance with speaker notes

**Phase 7: Export & Deploy**
- Export: PPTX (editable), PDF, HTML (static site), PNG sequence
- Deploy: Vercel (codex-slides) or Presenton cloud
- API: `POST /generate` → `presentation_id`, `edit_path`, `path`

### Templates (Built-in)
- 20+ visual systems (business, data, product, editorial, dark, light, corporate, startup, academic, creative + variants)
- Brand kit import: upload 2-3 reference decks → auto-extract DNA
- Template v2: metric infographics, textless layouts, component library

---

## CONSULTANT FRAMEWORKS (Embedded)

All frameworks inlined — no external references needed.

### Pyramid Principle (`consultants/pyramid-principle.md`)
- **Answer First**: Lead with the conclusion
- **MECE Grouping**: Supporting arguments mutually exclusive, collectively exhaustive
- **Vertical Logic**: Each level summarizes the level below
- **Horizontal Logic**: Same-level ideas form logical argument
- **Application**: Slide titles = answer; body = MECE support

### SCQ Framework (`consultants/scq-framework.md`)
- **Situation**: Undisputed context ("We operate in 12 markets")
- **Complication**: The change/problem ("Revenue flatlined in 3")
- **Question**: The decision to make ("Where to invest?")
- **Answer**: Your recommendation ("Double down on APAC")
- **Application**: Deck flow = S → C → Q → A (repeated per section)

### MECE (`consultants/mece.md`)
- **Mutually Exclusive**: No overlap between categories
- **Collectively Exhaustive**: No gaps — covers whole space
- **Test**: "Can any item fit in two buckets? Is any item missing?"
- **Application**: Slide groupings, chart series, argument trees

### Storyboarding (`consultants/storyboarding.md`)
- **Slide Titles Tell Story**: Read only titles → understand narrative
- **One Idea Per Slide**: If title has "and", split
- **Transition Logic**: Each slide answers "so what?" from previous
- **Application**: Outline phase — titles first, content second

### Charlie Hills (Marketing Decks) (`consultants/charlie-hills.md`)
- **Hook**: Stop the scroll (contrarian insight, bold claim)
- **Value**: What they get (not features — outcomes)
- **Proof**: Social, data, demo, logic
- **CTA**: Single, specific, low-friction next step
- **Application**: First 3 slides + closing slide of marketing decks

---

## UNIVERSAL SCHEMAS

### `schemas/deck.json`
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Universal Deck",
  "type": "object",
  "required": ["meta", "slides"],
  "properties": {
    "meta": {
      "type": "object",
      "required": ["title", "version", "mode", "created_at"],
      "properties": {
        "title": {"type": "string"},
        "subtitle": {"type": "string"},
        "version": {"type": "string"},
        "mode": {"type": "string", "enum": ["markdown", "native", "illustrated", "reconstruct", "studio"]},
        "created_at": {"type": "string", "format": "date-time"},
        "author": {"type": "string"},
        "audience": {"type": "string"},
        "format": {"type": "array", "items": {"type": "string", "enum": ["pptx", "pdf", "html", "png"]}}
      }
    },
    "slides": {
      "type": "array",
      "items": {"$ref": "slide.json"}
    }
  }
}
```

### `schemas/slide.json`
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Slide Contract",
  "type": "object",
  "required": ["index", "layout", "title", "content"],
  "properties": {
    "index": {"type": "integer"},
    "layout": {"type": "string", "enum": ["cover", "section", "bullets", "two-column", "metric", "chart", "table", "image", "divider", "appendix"]},
    "title": {"type": "string"},
    "content": {"type": "object"},
    "speaker_notes": {"type": "string"},
    "visual_spec": {
      "type": "object",
      "properties": {
        "background": {"type": "string"},
        "accent_color": {"type": "string"},
        "image_prompt": {"type": "string"}
      }
    }
  }
}
```

### `schemas/dna-sheet.json`
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Design DNA Sheet",
  "type": "object",
  "required": ["layout_grammar", "colors", "type_scale", "word_budget", "chart_style", "icon_style"],
  "properties": {
    "layout_grammar": {"type": "object"},
    "colors": {"type": "object"},
    "type_scale": {"type": "object"},
    "word_budget": {"type": "integer"},
    "chart_style": {"type": "object"},
    "icon_style": {"type": "object"}
  }
}
```

---

## VALIDATION GATES

### Preflight (scripts/preflight.py)
- Python 3.11+, Node.js 20+ (if needed)
- python-pptx, Pillow, numpy
- LibreOffice + Poppler (for QA render) — optional, falls back to manual
- Fonts: source fonts installed or embeddable
- API keys: only for modes requiring VLM/OCR (reconstruct, illustrated)

### Build Gates (per mode)
| Mode | Gate 1 | Gate 2 | Gate 3 |
|------|--------|--------|--------|
| markdown | Schema valid | Visual QA clean | Export opens |
| native | DNA extracted | Word budget met | QA render clean |
| illustrated | Style locked | Copy complete | Visual consistent |
| reconstruct | Layers separated | Re-assembly fidelity ≥95% | Edit test passes |
| studio | Outline approved | Style locked | Export smoke test |

### Publish Criteria (validators/)
- **Schema**: `validate.py deck.json schemas/deck.json` → PASS
- **Visual**: `qa_render.py deck.pptx` → 0 critical, ≤2 minor
- **Functional**: Open in PowerPoint/LibreOffice → charts editable, text selectable
- **Fidelity** (reconstruct): SSIM ≥0.95 vs source, text position ≤2px drift

---

## CHECKLIST (references/checklist.md)

### P0 — Blockers (Must Fix)
- [ ] Schema validation passes
- [ ] No text overflow / clipping on any slide
- [ ] All charts native (not images) in native mode
- [ ] Fonts embedded or system-available
- [ ] PPTX opens in PowerPoint & LibreOffice
- [ ] Export formats generated without error

### P1 — Quality (Should Fix)
- [ ] Word count ≤ budget (native mode)
- [ ] Visual consistency across slides (colors, type, spacing)
- [ ] Speaker notes present for all slides
- [ ] Slide titles read as coherent story
- [ ] MECE groupings verified
- [ ] SCQ flow verified

### P2 — Polish (Nice to Fix)
- [ ] Animations/transitions purposeful (not default)
- [ ] Alt text on all images
- [ ] Color contrast ≥4.5:1
- [ ] Print/export test: grayscale readable
- [ ] File size <50MB (or documented exception)

### P3 — Process (Track)
- [ ] DNA sheet saved for reuse (native mode)
- [ ] Style config versioned (markdown/illustrated)
- [ ] QA report archived
- [ ] Stakeholder sign-off recorded

---

## USAGE EXAMPLES

### Example 1: Training Deck (Markdown Mode)
```
Use slide-forge skill mode:markdown.
Content: attached product-spec.md
Audience: new engineers
Style: marp (standard training)
Output: deck.pptx + deck.pdf + deck.html
```

### Example 2: Board Deck (Native Mode)
```
Use slide-forge skill mode:native.
Reference decks: ./refs/board-q1.pptx ./refs/board-q2.pptx
Content: attached q3-results.xlsx + narrative.md
Audience: board of directors
DNA: extract from refs, apply to new build
Output: final.pptx (editable charts) + qa-report.json
```

### Example 3: Science Communication (Illustrated Mode)
```
Use slide-forge skill mode:illustrated.
Style: watercolor
Content: attached research-paper.pdf
Copy first: I'll provide slide copy, you generate illustrations
Output: deck.html (browser) + deck.pptx (editable layers)
```

### Example 4: Legacy Deck Rescue (Reconstruct Mode)
```
Use slide-forge skill mode:reconstruct.
Input: ./legacy/old-deck.pdf (50 slides, no source)
Goal: fully editable PPTX with native charts
Pipeline: hybrid (PDF text + VLM for charts)
Output: reconstructed.pptx + fidelity-report.json
```

### Example 5: Monthly Marketing Report (Studio Mode)
```
Use slide-forge skill mode:studio.
Project: monthly-marketing
Template: marketing-brand-kit (from last month)
Data: GA4 export + CRM CSV + attached insights.md
Schedule: regenerate 1st of each month
Output: auto-deploy to Presenton + PPTX download
```

---

## EXPORT FORMATS

| Format | Markdown | Native | Illustrated | Reconstruct | Studio |
|--------|----------|--------|-------------|-------------|--------|
| PPTX | ✅ (Marp/Slidev) | ✅ (primary) | ✅ (Baoyu Design) | ✅ (primary) | ✅ |
| PDF | ✅ | ✅ | ✅ | ✅ | ✅ |
| HTML | ✅ (primary) | ❌ | ✅ (primary) | ❌ | ✅ |
| PNG | ✅ | ✅ | ✅ | ✅ | ✅ |
| Editable Charts | ❌ (image-based) | ✅ | ⚠️ (Baoyu Design) | ✅ (VLM) | ✅ |
| Native Tables | ❌ | ✅ | ❌ | ✅ | ✅ |
| Animations | ⚠️ (Slidev) | ✅ | ❌ | ❌ | ✅ |

---

## LICENSE

MIT — Use it, modify it, share it. All embedded frameworks, templates, and scripts are MIT-licensed or permissive. No AGPL/GPL components.

---

## CHANGELOG

### v1.0.0 (2026-09-06)
- Initial release: 5 modes, 4 consultant frameworks, universal schemas, full validation pipeline
- All templates, styles, and scripts inlined
- Zero external GitHub references
- Self-contained skill directory structure
