# Catalogic / DPX / vStor / GuardMode Brand Resource Center

Static brand site for the **Catalogic** brand family. No framework and no runtime dependencies. Open `index.html` in a
browser or host the folder on any static host.

## Layout

```
dpx/
  index.html            generated page (do not edit by hand)
  index.template.html   page template: markup and copy
  variants.json         every download row + brand colours (drives the page, ZIPs and checks)
  vercel.json           security headers (strict CSP) served in production
  .vercelignore         dev files that are not deployed
  assets/
    svg/                SOURCE OF TRUTH for every logo
    png/  docs/  source/  PNG (1x, 2x), PDF and AI exported from the SVGs
    css/  js/           one stylesheet, one script (ARIA tabs + hash routing)
    packages/           ZIP downloads (generated)
  tools/                build, ZIP and check scripts, lint config (package.json), illustrator/ export script
  tests/                Playwright end-to-end tests (own package.json) and the local static server
.github/                CI workflow and Dependabot (at the repository root)
```

A variant is `<product>-<kind>` (`catalogic`, `dpx`, `vstor`, `guardmode` x `color`, `white`, `all-white`, `icon`,
`icon-white`) and always exists in five files: `svg/<name>.svg`, `png/<name>.png`, `png/<name>@2x.png`,
`docs/<name>.pdf`, `source/<name>.ai`.

## Brand colours

| Name | HEX | RGB | CMYK |
|---|---|---|---|
| Catalogic Blue | `#2D3494` | 45, 52, 148 | 99, 95, 2, 0 |
| Catalogic Green | `#8BBE41` | 139, 190, 65 | 51, 4, 99, 0 |
| Near Black | `#272727` | 39, 39, 39 | 71, 65, 64, 69 |

The CMYK values are conversions from RGB (U.S. Web Coated SWOP v2, done in Illustrator). No official CMYK or Pantone
values exist for this family yet. `tools/check.py` fails if an SVG contains a colour other than blue, green or white.

## Everyday tasks

Run from the `dpx/` folder. The build and checks use only the Python 3 standard library. Lint and tests need Node (CI uses Node 22).

| Task | Command |
|---|---|
| Rebuild the page after editing `index.template.html` or `variants.json` | `python3 tools/build.py` |
| Rebuild the ZIP packages after changing any asset | `python3 tools/build_zips.py` |
| File and markup integrity (links, formats, colours, signatures, proportions, headers) | `python3 tools/check.py` |
| Install lint tooling, then lint (ESLint, Stylelint, html-validate, Prettier) | `npm ci --prefix tools && npm run lint --prefix tools` |
| Auto-format code | `npm run format --prefix tools` |
| Install test tooling and browsers (once) | `cd tests && npm ci && npx playwright install chromium webkit` |
| Run the end-to-end tests | `cd tests && npm test` |
| Pixel-compare against the local baselines (macOS only) / refresh them | `npm run test:visual` / `npm run test:update-visual` |

**Add or change a variant:** put the SVG in `assets/svg/`, export the other formats (below), add the kind to a group in
`variants.json`, then run `build.py`, `build_zips.py` and `check.py`.

**Export from Illustrator** (macOS + Adobe Illustrator; macOS asks once to let the terminal control it):

```bash
tools/illustrator/run.sh export-variants.jsx /tmp/out assets/svg/dpx-color.svg   # AI + PDF + PNG 1x/2x
```

Copy the results from `/tmp/out/{ai,pdf,png}` into `assets/{source,docs,png}`. PNGs keep the artboard size.

## Quality gates

CI (`.github/workflows/ci.yml`, `working-directory: dpx`) runs on every push and pull request:

1. **Generated files are current:** `build.py --check`, `build_zips.py --check`.
2. **`tools/check.py`:** every local link resolves; every variant has SVG, PNG, PNG 2x, PDF and AI; SVGs use only brand
   colours; files have the right signature (PNG, `%PDF-`, well-formed SVG); PNG, PDF and AI proportions match the SVG;
   the CSP has no `unsafe-*` and the security headers exist;
   no inline `style`/`onclick`/`<style>`, every `<img>` has `alt`/`width`/`height`, one `h1`, one `header`/`main`/`footer`.
3. **Lint:** ESLint, Stylelint, html-validate (incl. WCAG rules), Prettier.
4. **Playwright**, in Chromium, Firefox, WebKit (Safari engine), mobile Chrome and mobile Safari. Every test also
   fails on any console message, uncaught error, failed request, HTTP >= 400 or CSP violation:
   - tabs: ARIA state, keyboard (arrows/Home/End), hash routing, malformed hashes, Back/Forward, skip link, landmarks;
   - accessibility: axe-core with WCAG 2.2 AA + best practices on every tab, focus visibility, reduced motion;
   - downloads: every referenced asset returns the right type and file signature, every row offers 5 formats, ZIPs exist;
   - deployment: the exact headers from `vercel.json`, dev files return 404, size budget, image dimensions/lazy loading;
   - responsive: no horizontal scroll at 320-1440 px on every tab, 24x24 px minimum targets; works without JavaScript.

Pixel baselines (`npm run test:visual`) are stored for macOS only and are not run in CI (font rendering differs per OS).

Accessibility decisions worth knowing: secondary text is `#5F6C6D` (AA on white and on the page background); white text on
the brand green `#8BBE41` is only 2.2:1, so the green swatch label is dark.

## Known limitations / hand-over notes

- No official **CMYK/Pantone** for the family; the CMYK values above are conversions (see above).
- Illustrator-exported SVGs carry Adobe XMP metadata (document IDs); harmless, but it changes on every re-export.
- No `og:image` is set: Open Graph needs an absolute public URL.
- **Firefox is only exercised in CI.** Playwright's Firefox build hung on the macOS 27.0.1 machine used for development, so
  the Firefox results of the test suite were never seen locally. The other four profiles passed locally.
- Fonts come from Google Fonts (allowed explicitly in the CSP). Self-hosting them would remove the third-party request.
- The two brand-center repositories share `tabs.js` and the tooling as copies; keep them in sync when changing one.
