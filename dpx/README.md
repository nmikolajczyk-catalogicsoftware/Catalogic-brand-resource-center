# Catalogic / DPX / vStor / GuardMode Brand Resource Center

Static brand site. Open `dpx/index.html` in a browser; there is no runtime dependency.

## Editing the download rows

`dpx/index.html` is **generated**. Do not edit the download sections by hand.

- `dpx/variants.json` lists every download row (section, file, name, description).
- `dpx/index.template.html` holds the rest of the page.
- Build from `dpx/`: `python3 tools/build.py` (add `--check` to verify `index.html` is up to date).

Each row `<file>` expects: `assets/svg/<file>.svg`, `assets/png/<file>.png`, `assets/png/<file>@2x.png`,
`assets/docs/<file>.pdf`, `assets/source/<file>.ai`.

## Tabs

`assets/js/tabs.js` implements the ARIA tab pattern (arrow keys, Home/End) and hash routing: `#colors` opens a tab and
`#dl-dpx` deep-links to a download section. The same file is used by the CloudCasa brand center; keep both copies identical.
