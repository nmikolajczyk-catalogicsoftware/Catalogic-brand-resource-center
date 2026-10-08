# Catalogic / DPX / vStor / GuardMode Brand Resource Center

Static brand site for the **Catalogic** brand family. No framework and no runtime dependencies. Open `index.html` in a
browser or host the folder on any static host.

## Layout

```
dpx/
  index.html            generated page (do not edit by hand)
  index.template.html   page template: markup, CSS, copy
  variants.json         every download row + brand colours (drives the page, ZIPs and checks)
  assets/
    svg/                SOURCE OF TRUTH for every logo
    png/  docs/  source/  PNG (1x, 2x), PDF and AI exported from the SVGs
    packages/           ZIP downloads (generated)
    js/tabs.js          ARIA tabs + hash routing
  tools/                build, ZIP, check and test scripts (+ illustrator/ export script)
  tests/tabs.test.js    browser test
.github/workflows/ci.yml
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

Run from the `dpx/` folder. Everything uses the Python 3 standard library only.

| Task | Command |
|---|---|
| Rebuild the page after editing `index.template.html` or `variants.json` | `python3 tools/build.py` |
| Rebuild the ZIP packages after changing any asset | `python3 tools/build_zips.py` |
| Run all integrity checks (links, formats, colours, markup, ZIP contents) | `python3 tools/check.py` |
| Run the browser tests (needs Chrome; set `CHROME=` if not auto-detected) | `python3 tools/test_browser.py` |

**Add or change a variant:** put the SVG in `assets/svg/`, export the other formats, add a row to `variants.json`,
then run `build.py`, `build_zips.py` and `check.py`.

**Export from Illustrator** (macOS + Adobe Illustrator; macOS asks once to let the terminal control it):

```bash
tools/illustrator/run.sh export-variants.jsx /tmp/out assets/svg/dpx-color.svg   # AI + PDF + PNG 1x/2x
```

Copy the results from `/tmp/out/{ai,pdf,png}` into `assets/{source,docs,png}`. PNGs keep the artboard size.

## Quality gates

`.github/workflows/ci.yml` runs the generated-file checks, `tools/check.py` and the browser tests on every push and pull
request (`working-directory: dpx`).

## Known limitations / hand-over notes

- No official **CMYK/Pantone** for the family; the CMYK values above are conversions (see above).
- Illustrator-exported SVGs carry Adobe XMP metadata (document IDs); harmless, but it changes on every re-export.
- No `og:image` is set: Open Graph needs an absolute public URL, which depends on where the site is hosted.
- The CI workflow has been validated locally (YAML parses, every command passes from a clean clone) but was not run on GitHub yet.
