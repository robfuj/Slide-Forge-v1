# SLIDE FORGE

**One skill, five production modes, zero external dependencies.**

A complete presentation deck generation ecosystem for Hermes Agent (and compatible runtimes). Transform any input — raw notes, outlines, documents, data, legacy slides — into production-ready decks.

## Five Production Modes

| Mode | Engines | Output | Best For |
|------|---------|--------|----------|
| **Markdown** | Marp, Slidev, Guizang, Frontend | HTML, PPTX, PDF | Training, courseware, version-controlled content |
| **Native** | ppt-master, slide-skill, deck-dna | Editable PPTX (live charts) | Client-editable decks, corporate templates, recurring reports |
| **Illustrated** | Baoyu, PPTAgent | PPTX, HTML (browser) | Science comms, knowledge cards, social media decks |
| **Reconstruct** | Gorden, LRriver, NBLM | Editable PPTX | Legacy PDF/Image → editable slides, native charts |
| **Studio** | codex-slides, Presenton | PPTX, PDF, HTML, PNG | Ongoing production, team collaboration, browser UI |

## Embedded Consultant Frameworks (Inlined, No External Refs)

- **McKinsey Pyramid Principle** — Answer-first, MECE grouping, vertical/horizontal logic
- **McKinsey SCQ Framework** — Situation → Complication → Question → Answer deck flow
- **McKinsey/BCG MECE** — Mutually Exclusive, Collectively Exhaustive groupings
- **McKinsey/Accenture Storyboarding** — Slide titles tell the story; one idea per slide
- **Charlie Hills (Marketing)** — Hook → Value → Proof → CTA for marketing decks

All frameworks in `consultants/` — MIT-licensed, zero external dependencies.

## Quick Start

```bash
# Install
cp -r slide-forge ~/.hermes/skills/creative/

# Use
"Use slide-forge skill. Build a 12-slide deck about <topic> from attached content using mode: <mode>."
```

## Validation Gates (Every Mode)

- **Schema** — Universal deck/slide/DNA schemas validated
- **Visual QA** — Render → pixel diff → overflow/alignment/contrast checks
- **Functional** — PPTX opens in PowerPoint & LibreOffice; charts editable; text selectable
- **Fidelity** (Reconstruct) — SSIM ≥0.95 vs source; text position ≤2px drift

## License

MIT — Use it, modify it, share it. All embedded frameworks, templates, and scripts are MIT-licensed or permissive. No AGPL/GPL components.

## Repository Structure

```
slide-forge/
├── SKILL.md                    # Entry point (this skill)
├── modes/
│   ├── markdown/               # Marp/Slidev/Guizang/Frontend
│   ├── native/                 # Editable PPTX with DNA extraction
│   ├── illustrated/            # Courseware & knowledge cards
│   ├── reconstruct/            # Images/PDFs → editable PPTX
│   └── studio/                 # Full production UI
├── consultants/                # Embedded frameworks (5 files)
├── schemas/                    # deck.json, slide.json, dna-sheet.json
├── references/                 # Checklist, layouts, themes, export specs
└── scripts/                    # preflight, build, qa_render, validate, export
```

## Share on Hermes Discord

Users install with one command:
```bash
hermes skills install github.com/robfuj/slide-forge
```

Or copy locally:
```bash
git clone https://github.com/robfuj/slide-forge
cp -r slide-forge ~/.hermes/skills/creative/
```