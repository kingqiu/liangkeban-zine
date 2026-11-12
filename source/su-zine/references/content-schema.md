# Content and execution contract

## JSON schema

Use the complete minimal example in `assets/example.json`. All strings are plain UTF-8 text; newline creates a line break. HTML, including `<strong>` and `<br>`, is intentionally escaped. Do not paste source HTML into content.

- Root: `series` (masthead), `brand` (neutral or user-approved), `pages` (nonempty array, arbitrary count).
- Page required: `title`, `intro`, `source` (visible attribution including short URL when available), `blocks`.
- Page optional: `sub`, `checktitle`, `checks` (pairs of heading/body), `closing`.
- Block required: `title`, `paras` (paragraph strings), `kind`, `items` (diagram text), `caption` (identify conceptual diagrams).
- Block optional: `label`, `color` (palette index 0–5), `panel`, `rows` (label/body pairs).
- Diagram kind: `flow` for 2–4 short ordered steps; `stack` for 2–5 layers; `tags` for 2–6 categories; `papers` for a two-sided comparison. Do not imply a factual sequence/hierarchy unless supported. Choose another layout if labels are too long.

Start with 1–3 blocks per page, 1–2 paragraphs per block, 2–4 rows per panel, 2–4 action checks. These are density guidelines, not schema requirements. Split rather than force content to fit. Keep source details and claim ledger in `sources.md`; the footer should still let readers identify the original article without that sidecar.

## Dependencies and commands

Python 3.10+ (standard library only), Node.js 20+ and Playwright 1.62.1.
Install a compatible Chromium using Playwright, or provide CHROMIUM_PATH pointing to an existing Chrome/Chromium. Install suitable Chinese fonts separately, and check their licenses before redistribution.

```bash
npm install
npx playwright install chromium
python3 scripts/build.py assets/example.json --out output/example
node scripts/render.cjs output/example --scale 2
```

Only newly generated local HTML and style.css are allowed. Networking and page JavaScript are disabled. Use trusted local files, not arbitrary downloaded HTML. The renderer waits for fonts and directly screenshots .sheet. It never creates or reads a PDF.
A fresh output directory is required for building. Rendering refuses existing image/report files unless --overwrite is explicitly supplied.
Scale must be 0.25–4; height at most 10000 CSS pixels; raster output at most 80 million pixels. Overflow fails the run. A render report does not replace visual inspection.
For custom widths, update assets/style.css and recheck all output. Fonts and browser versions affect line breaks; record them when comparing output.
